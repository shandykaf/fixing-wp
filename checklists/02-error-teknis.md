# Checklist: Error Teknis/Situs Down

- Cek error log server (PHP error log, debug.log kalau WP_DEBUG aktif) untuk pesan error spesifik dan timestamp.
- Cocokkan timestamp error dengan riwayat update plugin/tema atau perubahan konfigurasi terakhir.
- Kalau abis update plugin/tema, disable satu per satu (kalau akses memungkinkan) atau cek changelog buat breaking changes.
- Cek versi PHP dan kompatibilitasnya dengan plugin/tema terpasang.
- Cek memory_limit dan max_execution_time kalau errornya terkait timeout/resource.
- Cek isi .htaccess kalau errornya terkait redirect atau 500 error level server.
- Cek koneksi database di wp-config.php kalau errornya "error establishing database connection".

Sebelum eksekusi:
Laporkan dugaan akar masalah beserta bukti pendukung (log, timestamp, versi). Tunggu konfirmasi sebelum ubah apapun.

Setelah selesai:
Ringkasan root cause + rekomendasi biar gak terulang (pin versi plugin, tambah monitoring, dll).
