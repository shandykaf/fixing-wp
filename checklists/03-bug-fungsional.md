# Checklist: Bug Fungsional

- Reproduce bug-nya dulu, catat langkah persis buat memicu masalah.
- Cek console browser (network tab + console log) kalau ini bug di sisi frontend/JS.
- Trace kode yang terkait fitur ini langsung (jangan scan menyeluruh, cari file/hook spesifik yang relevan: custom shortcode, form handler, hook JetEngine/Elementor, dll).
- Cek apakah ada perubahan terakhir di kode/config fitur ini sebelum bug muncul.
- Cek konflik dengan plugin lain yang mungkin override fungsi yang sama (hook priority, filter yang sama dipakai dua plugin).
- Test di environment terpisah/staging kalau memungkinkan sebelum apply ke live.

Sebelum eksekusi:
Jelaskan akar masalah dan lokasi kode yang akan diubah. Tunggu konfirmasi sebelum edit.

Setelah selesai:
Test ulang skenario reproduce dari awal buat mastiin fix beneran jalan, bukan cuma nutup gejala.
