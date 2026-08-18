#!/usr/bin/env python3
"""
Script percobaan: cek hash file WordPress ke VirusTotal Public API.
Cuma kirim hash (SHA256), bukan upload file, jadi lebih cepat dan gak expose isi file ke VirusTotal.

Biar kuota Public API (500 request/hari) gak habis di file yang jelas bersih,
script ini filter dulu SEBELUM kirim ke VirusTotal:
1. File core WordPress yang match checksum resmi api.wordpress.org di-skip.
   File core yang TIDAK match checksum resmi = MODIFIED, dilaporkan langsung
   (ini temuan penting walau VirusTotal gak kenal hash-nya).
2. File plugin dari repo resmi yang match checksum downloads.wordpress.org di-skip.
3. Hash duplikat cuma dicek sekali.
4. Hasil lookup VirusTotal di-cache lokal, run ulang gak bakar kuota lagi.
5. Urutan cek diprioritaskan: wp-content/uploads dulu, lalu file core modified,
   baru sisanya.

Cara pakai di VPS:
1. Simpan API key di environment variable, JANGAN hardcode di script:
   export VT_API_KEY="isi_api_key_kamu"
2. Jalankan: python3 vt-hash-check.py /path/ke/folder/wordpress
   Opsional: python3 vt-hash-check.py /path/ke/folder/wordpress --report hasil.json

Batasan Public API (dari dokumentasi resmi VirusTotal):
- 500 request per hari
- 4 request per menit
- Dilarang dipakai untuk produk/layanan komersial (script ini untuk percobaan pribadi)

Script ini otomatis ngatur jeda antar request biar gak kena rate limit.
"""

import os
import re
import sys
import hashlib
import time
import json
import urllib.request
import urllib.error

VT_API_KEY = os.environ.get("VT_API_KEY")
VT_BASE_URL = "https://www.virustotal.com/api/v3/files/"
WP_CHECKSUM_URL = "https://api.wordpress.org/core/checksums/1.0/?version={version}&locale={locale}"
PLUGIN_CHECKSUM_URL = "https://downloads.wordpress.org/plugin-checksums/{slug}/{version}.json"
RATE_LIMIT_DELAY = 16  # detik, biar aman di bawah 4 request/menit (60/4=15, dibulatkan ke atas)
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".vt-cache.json")
EXTENSIONS = (".php", ".phtml", ".php5", ".php7", ".pht")


def compute_hashes(filepath):
    """Hitung MD5 (buat cocokin checksum WordPress.org) dan SHA256 (buat VirusTotal) sekali baca."""
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
            sha256.update(chunk)
    return md5.hexdigest(), sha256.hexdigest()


def fetch_json(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "wp-incident-check/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None


def detect_wp_version(wp_root):
    """Baca versi dan locale dari wp-includes/version.php."""
    version_file = os.path.join(wp_root, "wp-includes", "version.php")
    if not os.path.isfile(version_file):
        return None, "en_US"
    try:
        with open(version_file, encoding="utf-8", errors="replace") as f:
            content = f.read()
    except OSError:
        return None, "en_US"
    version = None
    m = re.search(r"\$wp_version\s*=\s*'([^']+)'", content)
    if m:
        version = m.group(1)
    locale = "en_US"
    m = re.search(r"\$wp_local_package\s*=\s*'([^']+)'", content)
    if m:
        locale = m.group(1)
    return version, locale


def load_core_checksums(wp_root):
    """Ambil checksum MD5 resmi core dari api.wordpress.org. Return dict path relatif -> md5, atau None."""
    version, locale = detect_wp_version(wp_root)
    if not version:
        print("Peringatan: gak bisa deteksi versi WordPress (wp-includes/version.php gak ketemu). Skip filter core.")
        return None
    print(f"Versi WordPress terdeteksi: {version} (locale {locale})")
    data = fetch_json(WP_CHECKSUM_URL.format(version=version, locale=locale))
    if not data or not data.get("checksums"):
        # locale non-en_US kadang gak ada checksum-nya, fallback ke en_US
        if locale != "en_US":
            data = fetch_json(WP_CHECKSUM_URL.format(version=version, locale="en_US"))
    if not data or not data.get("checksums"):
        print("Peringatan: gagal ambil checksum resmi dari api.wordpress.org. Skip filter core.")
        return None
    return data["checksums"]


def detect_plugin_version(plugin_dir):
    """Cari header 'Version:' di file php level atas folder plugin."""
    try:
        entries = sorted(os.listdir(plugin_dir))
    except OSError:
        return None
    for fname in entries:
        if not fname.lower().endswith(".php"):
            continue
        path = os.path.join(plugin_dir, fname)
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                head = f.read(8192)
        except OSError:
            continue
        if "Plugin Name" not in head:
            continue
        m = re.search(r"^[ \t/*#@]*Version:\s*(\S+)", head, re.MULTILINE)
        if m:
            return m.group(1)
    return None


def load_plugin_checksums(wp_root):
    """Ambil checksum resmi tiap plugin dari downloads.wordpress.org (best-effort).
    Return dict path relatif (dari wp_root) -> md5. Plugin non-repo-resmi otomatis gak ketemu, itu gak apa-apa."""
    plugins_dir = os.path.join(wp_root, "wp-content", "plugins")
    checksums = {}
    if not os.path.isdir(plugins_dir):
        return checksums
    for slug in sorted(os.listdir(plugins_dir)):
        plugin_dir = os.path.join(plugins_dir, slug)
        if not os.path.isdir(plugin_dir):
            continue
        version = detect_plugin_version(plugin_dir)
        if not version:
            continue
        data = fetch_json(PLUGIN_CHECKSUM_URL.format(slug=slug, version=version))
        if not data or not data.get("files"):
            print(f"  Plugin {slug} {version}: gak ada checksum resmi (bukan dari repo wordpress.org, atau versi custom). Semua file-nya ikut dicek.")
            continue
        count = 0
        for rel_path, sums in data["files"].items():
            md5 = sums.get("md5")
            if isinstance(md5, list):  # kadang API balikin list kalau ada beberapa build valid
                md5 = md5[0] if md5 else None
            if md5:
                full_rel = os.path.join("wp-content", "plugins", slug, rel_path)
                checksums[full_rel.replace("\\", "/")] = md5
                count += 1
        print(f"  Plugin {slug} {version}: {count} checksum resmi dimuat.")
    return checksums


def load_cache():
    if os.path.isfile(CACHE_FILE):
        try:
            with open(CACHE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            pass
    return {}


def save_cache(cache):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    except OSError:
        pass


def check_hash_vt(file_hash):
    url = VT_BASE_URL + file_hash
    req = urllib.request.Request(url, headers={"x-apikey": VT_API_KEY})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            attributes = data.get("data", {}).get("attributes", {})
            stats = attributes.get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            return {
                "found": True,
                "malicious": malicious,
                "suspicious": suspicious,
                "total_engines": sum(stats.values()) if stats else 0,
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # Hash gak ketemu di database VirusTotal, artinya belum pernah tercatat
            # BUKAN berarti file ini pasti aman, cuma belum ada di database mereka
            return {"found": False}
        elif e.code == 401:
            return {"error": "unauthorized"}
        elif e.code == 429:
            return {"error": "rate_limited"}
        else:
            return {"error": f"http_{e.code}"}
    except Exception as e:
        return {"error": str(e)}


def priority_key(rel_path, is_modified_core):
    """Urutan cek: uploads paling dulu, lalu core yang modified, baru sisanya."""
    p = rel_path.replace("\\", "/")
    if p.startswith("wp-content/uploads/"):
        return 0
    if is_modified_core:
        return 1
    return 2


def scan_directory(target_dir, report_path=None):
    if not VT_API_KEY:
        print("Error: environment variable VT_API_KEY belum di-set.")
        print('Jalankan dulu: export VT_API_KEY="isi_api_key_kamu"')
        sys.exit(1)

    target_dir = os.path.abspath(target_dir)

    print("Muat checksum resmi core WordPress...")
    core_checksums = load_core_checksums(target_dir)
    print("Muat checksum resmi plugin (repo wordpress.org)...")
    plugin_checksums = load_plugin_checksums(target_dir)

    files_to_check = []      # (rel_path, filepath, sha256, is_modified_core)
    modified_core = []       # file core yang gak match checksum resmi — temuan langsung
    skipped_official = 0

    for root, _, files in os.walk(target_dir):
        for fname in files:
            if not fname.lower().endswith(EXTENSIONS):
                continue
            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, target_dir).replace("\\", "/")
            try:
                md5, sha256 = compute_hashes(filepath)
            except OSError as e:
                print(f"Peringatan: gagal baca {rel_path}: {e}")
                continue

            is_modified_core = False
            official_md5 = None
            if core_checksums and rel_path in core_checksums:
                official_md5 = core_checksums[rel_path]
            elif rel_path in plugin_checksums:
                official_md5 = plugin_checksums[rel_path]

            if official_md5 is not None:
                if md5 == official_md5:
                    skipped_official += 1
                    continue  # match resmi, gak perlu ke VirusTotal
                is_modified_core = rel_path in (core_checksums or {})
                if is_modified_core:
                    modified_core.append(rel_path)

            files_to_check.append((rel_path, filepath, sha256, is_modified_core))

    files_to_check.sort(key=lambda item: (priority_key(item[0], item[3]), item[0]))

    print(f"\n{skipped_official} file match checksum resmi, di-skip.")
    if modified_core:
        print(f"PERHATIAN: {len(modified_core)} file core TIDAK match checksum resmi (modified/injected):")
        for p in modified_core:
            print(f"  - {p}")
        print("File-file ini temuan penting walaupun nanti VirusTotal gak kenal hash-nya.")

    # Dedupe hash: file identik cuma perlu satu lookup
    unique_hashes = []
    hash_to_files = {}
    for rel_path, _, sha256, _ in files_to_check:
        if sha256 not in hash_to_files:
            hash_to_files[sha256] = []
            unique_hashes.append(sha256)
        hash_to_files[sha256].append(rel_path)

    cache = load_cache()
    to_lookup = [h for h in unique_hashes if h not in cache]

    print(f"\n{len(files_to_check)} file perlu dicek ({len(unique_hashes)} hash unik, {len(unique_hashes) - len(to_lookup)} sudah ada di cache, {len(to_lookup)} lookup baru ke VirusTotal).")
    print(f"Estimasi waktu: ~{len(to_lookup) * RATE_LIMIT_DELAY // 60} menit (karena rate limit 4 req/menit).")
    if len(to_lookup) > 500:
        print(f"Peringatan: {len(to_lookup)} lookup melebihi kuota harian Public API (500/hari). Sisa lookup bakal gagal, jalankan lagi besok — hasil hari ini ke-cache, gak diulang.\n")
    else:
        print()

    flagged = []
    for i, sha256 in enumerate(unique_hashes, 1):
        sample_file = hash_to_files[sha256][0]
        if sha256 in cache:
            result = cache[sha256]
            print(f"[{i}/{len(unique_hashes)}] (cache) {sample_file}")
        else:
            print(f"[{i}/{len(unique_hashes)}] Cek: {sample_file}")
            result = check_hash_vt(sha256)

            if result.get("error") == "rate_limited":
                print("  Kena rate limit, tunggu 60 detik...")
                time.sleep(60)
                result = check_hash_vt(sha256)

            if result.get("error") == "unauthorized":
                print("\nError: VirusTotal balas 401 Unauthorized — API key salah atau kadaluarsa.")
                print("Cek lagi isi VT_API_KEY, lalu jalankan ulang (hasil sejauh ini sudah ke-cache).")
                save_cache(cache)
                break

            if "error" not in result:
                cache[sha256] = result
                save_cache(cache)
            time.sleep(RATE_LIMIT_DELAY)

        if result.get("found") is False:
            print("  Hash tidak ditemukan di database VirusTotal (belum tercatat, bukan jaminan aman).")
        elif result.get("malicious", 0) > 0 or result.get("suspicious", 0) > 0:
            print(f"  PERHATIAN: {result['malicious']} engine mendeteksi malicious, {result['suspicious']} suspicious dari {result['total_engines']} engine.")
            for rel_path in hash_to_files[sha256]:
                flagged.append({"file": rel_path, "hash": sha256, **result})
        elif "error" in result:
            print(f"  Gagal lookup: {result['error']}")
        else:
            print(f"  Bersih menurut {result.get('total_engines', 0)} engine.")

    print("\n=== Ringkasan ===")
    print(f"File match checksum resmi (di-skip): {skipped_official}")
    print(f"File core modified (gak match checksum resmi): {len(modified_core)}")
    if flagged:
        print(f"{len(flagged)} file terdeteksi mencurigakan oleh VirusTotal:")
        for r in flagged:
            print(f"  - {r['file']} (hash: {r['hash'][:16]}...)")
    else:
        print("Tidak ada file yang terdeteksi malicious/suspicious dari hasil lookup.")
        print("Catatan: ini bukan jaminan bersih 100%, cuma berarti hash-nya belum tercatat atau tidak dikenali sebagai malware oleh engine yang dipakai VirusTotal.")

    if report_path:
        report = {
            "scanned_dir": target_dir,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "skipped_official_checksum": skipped_official,
            "modified_core_files": modified_core,
            "vt_flagged": flagged,
            "checked_files": len(files_to_check),
            "unique_hashes": len(unique_hashes),
        }
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\nLaporan JSON disimpan ke: {report_path} (bisa dilampirkan ke laporan klien / tiket unsuspend).")


if __name__ == "__main__":
    args = sys.argv[1:]
    report_path = None
    if "--report" in args:
        idx = args.index("--report")
        if idx + 1 >= len(args):
            print("Error: --report butuh nama file, contoh: --report hasil.json")
            sys.exit(1)
        report_path = args[idx + 1]
        del args[idx:idx + 2]
    if len(args) != 1:
        print("Cara pakai: python3 vt-hash-check.py /path/ke/folder [--report hasil.json]")
        sys.exit(1)
    scan_directory(args[0], report_path)
