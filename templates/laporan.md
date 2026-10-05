# Template Laporan

Template laporan hasil pengerjaan, dipakai di semua kategori. Isi blok yang sesuai kategorinya, hapus blok yang gak relevan.

**Penting soal penyimpanan:** laporan yang sudah terisi itu data klien — simpan di folder kasus lokal (sebelah file/db yang dikerjakan), **jangan** di dalam repo ini dan jangan di-commit. Nama file yang disaranin: `laporan-<domain>-<YYYY-MM-DD>.md`.

**Penting soal isi:** JANGAN tulis password, API key, atau isi kredensial apa pun di laporan. Laporan ini sering dilampirkan ke tiket support hosting atau dikirim ke klien. Cukup catat "sudah diganti" / "belum diganti", bukan nilainya.

---

```markdown
# Laporan Perbaikan WordPress — <domain>

| | |
|---|---|
| Domain | <domain> |
| Kategori masalah | <1 Security/malware · 2 Error teknis · 3 Bug fungsional · 4 Integrasi/webhook · 5 Performance> |
| Tanggal pengerjaan | <YYYY-MM-DD, sampai YYYY-MM-DD kalau lebih dari sehari> |
| Status akhir | <Selesai · Selesai dengan catatan · Belum tuntas> |
| Dikerjakan dengan | <tool + model, misal Claude Code (Sonnet untuk scan, Opus untuk penilaian)> |

## Ringkasan

<3-5 baris, bahasa awam. Apa yang rusak, apa penyebabnya, apa yang dilakukan,
situs sekarang bagaimana. Bagian ini saja harus cukup buat orang yang gak baca sisanya.>

## Data & akses yang dipakai

- Sumber data: <folder situs live / backup WPvivid tanggal X / db dump tanggal Y>
- Akses yang dipakai: <cPanel / SSH / wp-admin / FTP>
- Kerja di: <copy terpisah di folder X — atau langsung di live, sebutkan kalau iya>

## Timeline

| Waktu | Kejadian |
|---|---|
| <tanggal> | Gejala pertama muncul menurut laporan pemilik situs |
| <tanggal/jam> | Investigasi mulai |
| <tanggal/jam> | <temuan utama / titik infeksi teridentifikasi> |
| <tanggal/jam> | Pembersihan/perbaikan dieksekusi |
| <tanggal/jam> | Deploy ke live & verifikasi |

## Temuan

<!-- Pilih blok yang sesuai kategorinya, hapus sisanya -->

### Kategori 1 — Security/malware

File:

| File | Temuan | Tindakan |
|---|---|---|
| <path relatif> | <backdoor eval+base64 / core file dimodifikasi / shell di uploads> | <dihapus / dipulihkan ke versi resmi / dibersihkan sebagian> |

Database:

| Tabel & lokasi | Temuan | Tindakan |
|---|---|---|
| <wp_options / wp_posts row id> | <injeksi script / siteurl diubah / cron asing> | <dihapus / dikembalikan> |

Hasil scan VirusTotal: <X file dikirim, Y terdeteksi malicious, Z hash belum tercatat>.
File yang match checksum resmi WordPress.org/plugin repo: <N file, di-skip dari scan>.

### Kategori 2 — Error teknis/situs down

| Gejala | Penyebab | Tindakan |
|---|---|---|
| <500 error di semua halaman> | <disk penuh / plugin X versi Y gak kompatibel PHP 8.2> | <dibersihkan / di-downgrade / diperbaiki> |

### Kategori 3 — Bug fungsional

| Fitur | Perilaku salah | Penyebab | Tindakan |
|---|---|---|---|
| <form checkout> | <field tidak tersimpan> | <konflik hook priority plugin A vs B> | <priority diubah di ...> |

### Kategori 4 — Integrasi/webhook

| Titik rantai | Status | Tindakan |
|---|---|---|
| <provider kirim / WAF / endpoint terima / proses> | <putus di sini karena ...> | <...> |

### Kategori 5 — Performance

| Metrik | Sebelum | Sesudah |
|---|---|---|
| TTFB | <x.x s> | <x.x s> |
| Skor PageSpeed mobile | <xx> | <xx> |

Sumber lambat: <query/plugin/script yang jadi biang, dan apa yang diubah>.

## Akar masalah

<Untuk security: vektor masuk — plugin apa versi berapa yang vulnerable, bukti dari
access log (IP, timestamp, request), atau brute force. Kalau belum ketemu, tulis
"belum teridentifikasi" dan jelaskan apa yang sudah dicek — jangan dikosongkan,
karena ini yang nentuin bakal reinfeksi atau enggak.

Untuk kategori lain: penyebab teknisnya, bukan cuma gejalanya.>

## Tindakan pemulihan & pengamanan

| Tindakan | Status |
|---|---|
| Security keys/salts di wp-config.php diregenerate | <sudah / belum / tidak relevan> |
| Password diganti (WP admin, database, cPanel, FTP, email admin) | <sudah / belum — sebut mana yang belum> |
| Semua sesi login aktif di-destroy (session_tokens) | <sudah / belum> |
| Application passwords dihapus | <sudah / belum> |
| Akun admin asing dihapus / role diturunkan | <sudah / belum — sebut jumlah> |
| Core, plugin, tema diupdate ke versi patched | <sudah / belum — sebut mana yang belum dan kenapa> |
| Plugin/tema tidak terpakai dihapus | <sudah / belum> |
| File permissions dirapikan (folder 755, file 644, wp-config 600) | <sudah / belum> |
| Eksekusi PHP di wp-content/uploads diblok | <sudah / belum> |
| DISALLOW_FILE_EDIT diaktifkan | <sudah / belum> |
| xmlrpc.php diblok | <sudah / belum / sengaja dibiarkan karena dipakai X> |
| Sisa file/db lama yang belum bersih sudah dihapus dari server | <sudah / belum> |

(Catat status saja, jangan tulis password atau isi kredensialnya.)

## Baseline konfigurasi setelah perbaikan

Dicatat biar audit berikutnya punya pembanding.

- WordPress core: <versi>
- PHP: <versi>
- Plugin security: <nama + versi>, setting aktif: <firewall, login lockout, 2FA, file change detection>
- URL login: <default /wp-admin — atau URL baru kalau diubah plugin security>
- Proteksi level hosting: <ModSecurity aktif/tidak, disable_functions, SSL + auto-renew>
- Jumlah plugin aktif: <n> · tema aktif: <nama + versi>

## Verifikasi

| Yang dites | Hasil |
|---|---|
| Situs diakses normal (halaman utama + halaman yang tadi bermasalah) | <ok / catatan> |
| Cek cloaking (User-Agent Googlebot vs browser biasa) | <isi sama / masih beda> |
| File .php di wp-content/uploads tidak bisa dieksekusi | <ok / catatan> |
| Status blacklist Google Safe Browsing / Search Console | <bersih / masih kena flag, review diajukan tanggal X> |
| <test khusus kategori: reproduce bug, transaksi dummy, dll> | <...> |

## Yang belum tuntas / tindak lanjut

- Re-scan terjadwal: <tanggal, 3-7 hari setelah pembersihan> — buat deteksi reinfeksi. Kalau kembali kotor berarti vektor masuk belum ketemu.
- <Hal yang di luar scope atau butuh keputusan pemilik situs, misal plugin premium yang lisensinya mati jadi gak bisa diupdate.>
- <Rekomendasi pencegahan: backup terjadwal, hindari plugin nulled, dll.>

## Batasan laporan ini

- Audit berbasis pola (pattern-based) + lookup hash VirusTotal. Ini bukan pengganti scan signature-based dari tool khusus, dan **bukan jaminan "bersih 100%"**.
- Hash yang tidak ditemukan di database VirusTotal berarti belum pernah tercatat di sana — bukan berarti file tersebut sudah dipastikan aman.
- <Kalau ada bagian yang tidak bisa dicek, sebutkan di sini: misal access log tidak tersedia dari hosting, atau kuota VirusTotal habis sehingga N file belum diverifikasi.>
```
