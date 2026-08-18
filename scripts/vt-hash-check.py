#!/usr/bin/env python3
"""
Script percobaan: cek hash file WordPress ke VirusTotal Public API.
Cuma kirim hash (SHA256), bukan upload file, jadi lebih cepat dan gak expose isi file ke VirusTotal.

Cara pakai di VPS:
1. Simpan API key di environment variable, JANGAN hardcode di script:
   export VT_API_KEY="isi_api_key_kamu"
2. Jalankan: python3 vt-hash-check.py /path/ke/folder/wordpress

Batasan Public API (dari dokumentasi resmi VirusTotal):
- 500 request per hari
- 4 request per menit
- Dilarang dipakai untuk produk/layanan komersial (script ini untuk percobaan pribadi)

Script ini otomatis ngatur jeda antar request biar gak kena rate limit.
"""

import os
import sys
import hashlib
import time
import json
import urllib.request
import urllib.error

VT_API_KEY = os.environ.get("VT_API_KEY")
VT_BASE_URL = "https://www.virustotal.com/api/v3/files/"
RATE_LIMIT_DELAY = 16  # detik, biar aman di bawah 4 request/menit (60/4=15, dibulatkan ke atas)

def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

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
        elif e.code == 429:
            return {"error": "rate_limited"}
        else:
            return {"error": f"http_{e.code}"}
    except Exception as e:
        return {"error": str(e)}

def scan_directory(target_dir, extensions=(".php", ".phtml", ".php5")):
    if not VT_API_KEY:
        print("Error: environment variable VT_API_KEY belum di-set.")
        print('Jalankan dulu: export VT_API_KEY="isi_api_key_kamu"')
        sys.exit(1)

    files_to_check = []
    for root, _, files in os.walk(target_dir):
        for fname in files:
            if fname.lower().endswith(extensions):
                files_to_check.append(os.path.join(root, fname))

    print(f"Ditemukan {len(files_to_check)} file untuk dicek.")
    print(f"Estimasi waktu: ~{len(files_to_check) * RATE_LIMIT_DELAY // 60} menit (karena rate limit 4 req/menit).\n")

    results = []
    for i, filepath in enumerate(files_to_check, 1):
        file_hash = compute_sha256(filepath)
        print(f"[{i}/{len(files_to_check)}] Cek: {filepath}")
        result = check_hash_vt(file_hash)

        if result.get("error") == "rate_limited":
            print("  Kena rate limit, tunggu 60 detik...")
            time.sleep(60)
            result = check_hash_vt(file_hash)

        if result.get("found") is False:
            print("  Hash tidak ditemukan di database VirusTotal (belum tercatat, bukan jaminan aman).")
        elif result.get("malicious", 0) > 0 or result.get("suspicious", 0) > 0:
            print(f"  PERHATIAN: {result['malicious']} engine mendeteksi malicious, {result['suspicious']} suspicious dari {result['total_engines']} engine.")
            results.append({"file": filepath, "hash": file_hash, **result})
        else:
            print(f"  Bersih menurut {result.get('total_engines', 0)} engine.")

        if i < len(files_to_check):
            time.sleep(RATE_LIMIT_DELAY)

    print("\n=== Ringkasan ===")
    if results:
        print(f"{len(results)} file terdeteksi mencurigakan:")
        for r in results:
            print(f"  - {r['file']} (hash: {r['hash'][:16]}...)")
    else:
        print("Tidak ada file yang terdeteksi malicious/suspicious dari hasil lookup.")
        print("Catatan: ini bukan jaminan bersih 100%, cuma berarti hash-nya belum tercatat atau tidak dikenali sebagai malware oleh engine yang dipakai VirusTotal.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cara pakai: python3 vt-hash-check.py /path/ke/folder")
        sys.exit(1)
    scan_directory(sys.argv[1])
