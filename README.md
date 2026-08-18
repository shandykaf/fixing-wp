# WordPress Incident Response

Panduan kerja untuk investigasi masalah WordPress: security/malware, error teknis, bug fungsional, integrasi/webhook, dan performance. Dipakai di Claude Code atau opencode.

## Cara pakai

Gak perlu clone repo ini. Claude Code baca checklist langsung dari raw GitHub URL sesuai instruksi di `prompts/prompt-awal.md`.

1. Siapkan folder lokal berisi file dan/atau db website yang bermasalah (di VPS atau PC).
2. Copy prompt dari `prompts/prompt-awal.md`, isi path lokal dan gejala yang dialami.
3. Jalankan di Claude Code atau opencode. Claude Code akan baca `00-router.md` dari repo ini, klasifikasi masalahnya, lalu minta konfirmasi kamu sebelum lanjut ke checklist yang sesuai.
4. Kalau checklist security yang kepilih dan butuh VirusTotal: Claude Code yang urus semuanya sendiri (cek/bikin file API key di `~/.vt-apikey`, ambil script-nya, jalankan). Kalau API key belum ada, Claude bakal nanya di chat lalu bikinkan filenya sendiri — kamu gak perlu ketik command apa pun, tinggal kasih key-nya waktu ditanya.

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

Gak ada yang perlu disiapkan manual duluan. API key VirusTotal ditangani otomatis oleh Claude Code pas checklist security dijalankan (lihat bagian "Setup VirusTotal" di `checklists/01-security-malware.md`):

- Kalau `~/.vt-apikey` belum ada, Claude bakal nanya API key-nya ke kamu di chat, terus Claude sendiri yang bikin filenya.
- Kalau sudah pernah dibuatkan sebelumnya di mesin yang sama, Claude langsung pakai itu, gak nanya ulang.

Satu-satunya yang perlu kamu siapkan sendiri di luar chat: daftar akun VirusTotal gratis dan ambil API key-nya di https://www.virustotal.com/gui/my-apikey, biar ada yang bisa dikasih waktu ditanya Claude.

## Batasan penting

- File & db website yang bermasalah, hasil audit per klien, dan API key TIDAK disimpan di repo ini. Simpan lokal saja, di luar folder yang di-track git.
- VirusTotal Public API dibatasi 500 request/hari dan 4 request/menit, serta tidak boleh dipakai untuk produk/layanan komersial sesuai TOS resminya. Gunakan untuk percobaan/verifikasi, bukan sebagai bagian resmi dari deliverable berbayar ke klien.
- Hasil audit AI (pattern-based) bukan pengganti scan signature-based dari tool khusus (VirusTotal, MalCare, Wordfence). Anggap sebagai audit awal, bukan keputusan final "bersih 100%".
