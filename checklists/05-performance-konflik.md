# Checklist: Performance/Konflik Script

Kalau di tengah investigasi ketemu indikasi kompromi (proses aneh makan CPU, file asing, cryptominer), STOP — pindah ke 01-security-malware.md. Situs lambat mendadak kadang gejala malware.

## Tentukan arah dulu: masalah backend atau frontend?

- Ukur TTFB terpisah dari skor frontend (`curl -o /dev/null -w "%{time_starttransfer}\n" https://domain/`). TTFB tinggi (> ~1 detik) = masalah server/PHP/database — perbaikan minify/delay JS gak akan nolong. TTFB normal tapi loading lambat = masalah frontend/asset.
- Kalau ada backup dari sebelum situs jadi lambat (lihat "Sumber data berupa backup" di `00-router.md`): bandingkan daftar plugin aktif & file wp-content vs backup lama buat langsung nemuin plugin/script apa yang baru ditambah sekitar waktu situs mulai lambat.

## Kalau backend lambat

- Pasang Query Monitor: cari query lambat, hook yang boros, dan plugin yang makan waktu paling banyak per halaman.
- Cek ukuran autoload di wp_options (`SELECT SUM(LENGTH(option_value)) FROM wp_options WHERE autoload='yes'`) — autoload bloat (> ~1MB) bikin SEMUA halaman lambat. Cari option raksasa yang gak perlu autoload (sisa plugin lama, transient expired).
- Cek admin-ajax.php yang dipanggil bertubi-tubi (access log) — biasanya heartbeat atau plugin yang polling terlalu agresif.
- Cek WP-Cron numpuk (event terjadwal gagal jalan lalu antre) — pertimbangkan disable WP-Cron dan ganti cron server.

## Kalau frontend/konflik script

- Cek console browser buat JS error spesifik dan file mana sumbernya.
- Kalau abis pasang plugin optimasi (WP Rocket, dll), disable fitur delay JS/minify satu per satu buat isolasi konfliknya.
- Cek elemen yang rusak secara visual, bandingkan sebelum/sesudah optimasi diaktifkan.
- Cek exclude list di plugin optimasi, biasanya script tertentu (popup, form validation) perlu di-exclude dari delay/minify.
- Cek apakah masalahnya cuma di device/browser tertentu atau semua.

## Baseline & verifikasi

- Cek waktu loading pakai PageSpeed/GTmetrix buat baseline sebelum dan sesudah perbaikan.
- SEBELUM tiap pengukuran/verifikasi, purge semua layer cache (page cache, object cache, CDN) — tanpa ini perbandingan sebelum/sesudah menyesatkan (bisa jadi yang keukur versi cache lama).

## Sebelum eksekusi

Sebutkan sumber masalahnya (backend: query/plugin mana; frontend: script/plugin mana) dan rencana fix-nya (exclude, reorder, downgrade, atau optimasi db). Tunggu konfirmasi.

## Setelah selesai

Bandingkan skor performance sebelum/sesudah (cache sudah di-purge di kedua pengukuran), pastikan fix gak balikin masalah lambatnya lagi.

**Trigger verifikasi otomatis**: begitu user bilang fix-nya sudah dideploy ke live, Claude infokan dulu ("fix sudah live, saya ukur ulang performance-nya ya") lalu langsung buka situs via browser otomatis buat cek visual (elemen gak rusak) dan ukur ulang TTFB/skor performance — gak perlu diminta terpisah.
