# Checklist: Error Teknis/Situs Down

Kalau di tengah investigasi ketemu indikasi kompromi (file backdoor, admin asing, redirect aneh), STOP — pindah ke 01-security-malware.md. Error 500 kadang cuma gejala malware.

## Cek resource server duluan (cepat, sering jadi jawabannya)

- Disk penuh: `df -h` — disk 100% bikin situs down, db error, dan gagal tulis cache/log.
- Inode habis: `df -i` — bisa "penuh" walau disk masih lega (biasanya karena file cache/session numpuk).
- RAM/proses: cek apakah PHP-FPM/MySQL mati atau di-kill OOM (`free -m`, error log kernel/hosting).

## Diagnosis

- Cek error log server (PHP error log, debug.log kalau WP_DEBUG aktif) untuk pesan error spesifik dan timestamp. Kalau debug.log gak ada, aktifkan sementara WP_DEBUG_LOG di wp-config.php (WP_DEBUG true, WP_DEBUG_LOG true, WP_DEBUG_DISPLAY false biar error gak tampil ke pengunjung) — matikan lagi setelah selesai.
- Cocokkan timestamp error dengan riwayat update plugin/tema atau perubahan konfigurasi terakhir.
- Kalau ada backup dari sebelum situs down (lihat "Sumber data berupa backup" di `00-router.md`): diff file (terutama wp-config.php, .htaccess, dan plugin/tema yang baru diupdate) vs backup lama buat cepat nemuin perubahan yang memicu error, tanpa perlu nebak-nebak dari log doang.
- Cek versi PHP dan kompatibilitasnya dengan plugin/tema terpasang.
- Cek memory_limit dan max_execution_time kalau errornya terkait timeout/resource.
- Cek isi .htaccess kalau errornya terkait redirect atau 500 error level server.

## Isolasi (bisa tanpa akses wp-admin — saat white screen, wp-admin biasanya ikut mati)

- Disable SEMUA plugin sekaligus: rename folder `wp-content/plugins` ke `plugins-off` (atau `wp option update active_plugins ''` via WP-CLI). Kalau situs balik normal, rename balik lalu aktifkan plugin satu per satu sampai ketemu biangnya.
- Ganti tema ke default tanpa admin: ubah value `template` dan `stylesheet` di wp_options ke tema default (twentytwentyfour dll), atau rename folder tema aktif.
- Kalau abis update plugin/tema, cek changelog buat breaking changes sebelum nyalahin yang lain.

## Kalau errornya "error establishing database connection"

- Cek kredensial di wp-config.php (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST).
- Cek service MySQL-nya hidup atau enggak (`systemctl status mysql` / dari cPanel) — jangan asumsi masalahnya di kredensial.
- Cek tabel crashed: `wp db check` atau `mysqlcheck`, repair kalau perlu (`REPAIR TABLE`) — backup db dulu sebelum repair.

## Sebelum eksekusi

Laporkan dugaan akar masalah beserta bukti pendukung (log, timestamp, versi). Tunggu konfirmasi sebelum ubah apapun.

## Setelah selesai

- Balikin yang sifatnya sementara: WP_DEBUG off, folder yang di-rename, dll.
- **Trigger verifikasi otomatis**: begitu user bilang situs sudah live/normal lagi, Claude infokan dulu ("situs sudah live, saya cek ulang lewat browser ya") lalu langsung buka situsnya via browser otomatis buat mastiin bener-bener normal (halaman utama, halaman yang tadi error, console browser bersih) — gak perlu diminta terpisah. Ini cuma verifikasi (baca/screenshot), bukan ubah setting apapun. (Setup akses browser-nya lihat `00-router.md` — Claude yang urus sendiri.)
- Ringkasan root cause + rekomendasi biar gak terulang (pin versi plugin, tambah monitoring disk/uptime, dll).
