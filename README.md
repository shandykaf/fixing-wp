# WordPress Incident Response

Panduan kerja untuk investigasi masalah WordPress: security/malware, error teknis, bug fungsional, integrasi/webhook, dan performance. Dipakai di Claude Code atau opencode.

## Cara pakai

Gak perlu clone repo ini. Claude Code baca checklist langsung dari raw GitHub URL sesuai instruksi di `prompts/prompt-awal.md`.

1. Siapkan folder lokal berisi file dan/atau db website yang bermasalah (di VPS atau PC).
2. Simpan API key VirusTotal sekali di `~/.vt-apikey` (home directory, lihat bagian Setup di bawah).
3. Copy prompt dari `prompts/prompt-awal.md`, isi path lokal dan gejala yang dialami.
4. Jalankan di Claude Code atau opencode. Claude Code akan baca `00-router.md` dari repo ini, klasifikasi masalahnya, lalu minta konfirmasi kamu sebelum lanjut ke checklist yang sesuai. Kalau checklist security yang kepilih, Claude Code akan download `scripts/vt-hash-check.py` langsung dari raw GitHub URL buat dijalankan.

## Struktur

- `00-router.md` — entry point, klasifikasi masalah ke salah satu dari 5 kategori.
- `checklists/` — langkah investigasi per kategori (security, error teknis, bug fungsional, integrasi/webhook, performance).
- `scripts/vt-hash-check.py` — cek hash file ke VirusTotal Public API, dipakai kalau checklist security yang kepilih.
- `prompts/prompt-awal.md` — template prompt singkat untuk memulai tiap kasus baru.

## Prompt awal (cuplikan)

```
Saya butuh investigasi masalah website WordPress.
Akses repo ini dulu:
https://github.com/shandykaf/fixing-wp

Baca panduan kerja dari repo ini dan ikuti instruksinya:
https://raw.githubusercontent.com/shandykaf/fixing-wp/main/00-router.md

- File WordPress = [ISI PATH]
- Database dump = [ISI PATH]
- Gejala yang saya lihat: [ISI]

Jangan eksekusi apapun sebelum saya konfirmasi di tiap tahap yang diminta router.
```

Versi lengkap dan terbaru selalu ada di `prompts/prompt-awal.md`, edit di sana kalau ada perubahan, jangan di sini.

## Setup sebelum pakai

Sebelum jalanin prompt di Claude Code, simpan API key VirusTotal sekali di VPS/PC (gak perlu diulang tiap sesi, dan gak perlu clone repo ini):

```
echo "isi_api_key_kamu_sendiri" > ~/.vt-apikey
```

Disimpan di home directory, di luar repo mana pun, jadi gak akan pernah ke-commit ke GitHub. Kalau mau lokasi lain (folder kerja tempat kamu jalanin script, atau di dalam clone repo di `scripts/.vt-apikey`), script-nya otomatis coba cari di beberapa lokasi juga -- lihat komentar `APIKEY_LOCATIONS` di `scripts/vt-hash-check.py`.

Ambil API key-nya di https://www.virustotal.com/gui/my-apikey (daftar akun gratis dulu kalau belum punya).

## Batasan penting

- File & db website yang bermasalah, hasil audit per klien, dan API key TIDAK disimpan di repo ini. Simpan lokal saja, di luar folder yang di-track git.
- VirusTotal Public API dibatasi 500 request/hari dan 4 request/menit, serta tidak boleh dipakai untuk produk/layanan komersial sesuai TOS resminya. Gunakan untuk percobaan/verifikasi, bukan sebagai bagian resmi dari deliverable berbayar ke klien.
- Hasil audit AI (pattern-based) bukan pengganti scan signature-based dari tool khusus (VirusTotal, MalCare, Wordfence). Anggap sebagai audit awal, bukan keputusan final "bersih 100%".
