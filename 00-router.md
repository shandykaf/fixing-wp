# Router: WordPress Incident Response

Entry point tunggal. Isi [ISI] lalu jalankan prompt ini duluan sebelum baca checklist manapun.

---

## Prompt

Saya butuh investigasi masalah di website WordPress. Jangan baca atau eksekusi checklist apapun dulu, mulai dari klasifikasi.

Data situs:
Domain [ISI]. Akses [ISI: cPanel/SSH/WP admin/FTP]. Gejala [ISI: deskripsikan sedetail mungkin, kapan mulai, ada perubahan terakhir gak sebelum masalah muncul]. Screenshot/error message kalau ada [ISI atau "tidak ada"].

Klasifikasikan ke salah satu dari 5 kategori berikut, kasih alasan singkat kenapa pilih itu:

1. Security/malware — indikasi kompromi: rogue admin, redirect asing, file backdoor, situs disuspend hosting, spam SEO muncul di Google.
2. Error teknis/situs down — 500 error, white screen, fatal error PHP, timeout, situs gak bisa diakses tapi gak ada tanda kompromi.
3. Bug fungsional — fitur spesifik gak jalan sesuai harusnya (form, shortcode custom, checkout field), sisanya situs normal.
4. Integrasi/webhook bermasalah — payment gateway atau shipping API gak sync, callback gak diterima, data gak update otomatis.
5. Performance/konflik script — situs lambat, elemen visual rusak, JS error di console, biasanya abis pasang plugin optimasi baru.

Kalau gejala bisa masuk lebih dari satu kategori (contoh: error 500 tapi juga ada rogue admin), pilih kategori paling berisiko duluan (security selalu prioritas di atas yang lain).

Setelah klasifikasi, sebutkan nama file checklist yang harus dibaca:
- Kategori 1 → 01-security-malware.md
- Kategori 2 → 02-error-teknis.md
- Kategori 3 → 03-bug-fungsional.md
- Kategori 4 → 04-integrasi-webhook.md
- Kategori 5 → 05-performance-konflik.md

Tunggu konfirmasi saya sebelum baca file checklist itu dan mulai eksekusi.
