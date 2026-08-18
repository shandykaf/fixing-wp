# Checklist: Bug Fungsional

Kalau di tengah investigasi ketemu indikasi kompromi (kode asing di functions.php, file backdoor, dll), STOP — pindah ke 01-security-malware.md.

Backup file & db (atau minimal file yang mau disentuh) sebelum edit apapun di live.

- Reproduce bug-nya dulu, catat langkah persis buat memicu masalah.
- Purge semua cache dulu (page cache, object cache, CDN) lalu reproduce lagi — bug yang "kadang muncul kadang enggak" sering cuma cache menyajikan versi lama, bukan bug beneran. Kalau hilang setelah purge, masalahnya di konfigurasi cache, bukan di kode fitur.
- Cek console browser (network tab + console log) kalau ini bug di sisi frontend/JS.
- Trace kode yang terkait fitur ini langsung (jangan scan menyeluruh, cari file/hook spesifik yang relevan: custom shortcode, form handler, hook JetEngine/Elementor, dll).
- Cek apakah ada perubahan terakhir di kode/config fitur ini sebelum bug muncul.
- Cek konflik dengan plugin lain yang mungkin override fungsi yang sama (hook priority, filter yang sama dipakai dua plugin).
- Buat isolasi konflik plugin di live tanpa ganggu pengunjung: pakai plugin Health Check & Troubleshooting (mode troubleshooting cuma berlaku di sesi kamu, pengunjung tetap lihat situs normal) — lebih aman daripada disable plugin beneran di live.
- Test di environment terpisah/staging kalau memungkinkan sebelum apply ke live.

Sebelum eksekusi:
Jelaskan akar masalah dan lokasi kode yang akan diubah. Tunggu konfirmasi sebelum edit.

Setelah selesai:
Test ulang skenario reproduce dari awal buat mastiin fix beneran jalan, bukan cuma nutup gejala. Purge cache lagi sebelum test biar hasilnya valid.
