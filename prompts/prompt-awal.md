# Prompt Awal

Copy template ini tiap mulai kasus baru, isi bagian `ISI_...`, lalu jalankan di Claude Code / opencode.

```
Saya butuh investigasi masalah website WordPress.
Akses repo ini dulu:
https://github.com/shandykaf/fixing-wp

Baca panduan kerja dari repo ini dan ikuti instruksinya:
https://raw.githubusercontent.com/shandykaf/fixing-wp/main/00-router.md

Data situs:
- Domain = ISI_DOMAIN
- Akses yang saya punya = ISI_AKSES (sebut yang ada aja: cPanel / SSH / WP admin / FTP)
- URL login kalau non-default (wp-admin diubah, port SSH beda, dll) = ISI_URL_LOGIN
- Gejala yang saya lihat = ISI_GEJALA

Sumber data (isi yang sesuai aja, sisanya hapus):
- Folder file WordPress = ISI_PATH
- File database (.sql / .sql.gz / .zip) = ISI_PATH
- Backup WPvivid/UpdraftPlus (path zip-nya, atau folder tempat zip-zip itu) = ISI_PATH_BACKUP

Kalau yang keisi baris backup, itu udah mencakup file + db sekaligus, dua baris di
atasnya gak perlu diisi. Ekstrak sendiri dulu sesuai bagian "Sumber data berupa
backup" di router, jangan minta saya unzip manual.

Password/kredensial sengaja gak saya tulis di sini. Minta ke saya pas tahap yang
memang butuh, jangan diminta di awal.

Jangan eksekusi apapun sebelum saya konfirmasi di tiap tahap yang diminta router.
```

## Contoh terisi (kasus pakai backup WPvivid)

```
Data situs:
- Domain = klienA.co.id
- Akses yang saya punya = cPanel + WP admin (SSH gak ada)
- URL login kalau non-default (wp-admin diubah, port SSH beda, dll) = default semua
- Gejala yang saya lihat = situs redirect ke domain judi kalau dibuka dari Google, tapi normal kalau diketik langsung. Mulai kira-kira 3 hari lalu.

Sumber data (isi yang sesuai aja, sisanya hapus):
- Backup WPvivid/UpdraftPlus (path zip-nya, atau folder tempat zip-zip itu) = /home/shandy/kasus-klienA/wpvivid
```

Di contoh itu `/home/shandy/kasus-klienA/wpvivid` adalah folder berisi semua zip WPvivid (file + db, termasuk part-part-nya). Dua baris sumber lainnya dihapus karena sudah tercakup di backup.

## Catatan

- Repo ini private, pastikan Claude Code/opencode sudah punya autentikasi GitHub (misal `gh auth login`) sebelum menjalankan prompt di atas, kalau belum akan gagal akses (404).
- Path lokal (file WordPress, db dump) selalu path di mesin yang menjalankan Claude Code, bukan path di repo GitHub.
- **Jangan tulis password/API key di prompt awal.** Cukup sebut akses apa yang kamu punya (cPanel, SSH, dll); kredensialnya dikasih belakangan pas ada tahap yang memang butuh — misal Claude mau login wp-admin lewat browser. Ingat apapun yang kamu ketik ke chat ikut kecatat di transcript sesi, jadi kasih seperlunya aja, dan ganti password setelah kasus selesai kalau kamu share kredensial yang sensitif.
- Bentuk sumber data yang didukung: folder WordPress aktif, hasil ekstrak backup, file `.sql`/`.sql.gz`, file `.zip`, atau backup plugin (WPvivid, UpdraftPlus, dll). Kalau backup-nya displit jadi beberapa part (`_files_1.zip`, `_files_2.zip`, dst) atau dienkripsi, sebutkan di prompt — part-nya harus lengkap semua, dan yang dienkripsi butuh passwordnya.
- Kalau kamu punya beberapa backup dari tanggal berbeda, sebutkan juga. Backup dari sebelum masalah muncul dipakai sebagai baseline buat diff, dan ini biasanya cara tercepat nemuin akar masalahnya (berlaku di semua kategori, bukan cuma security).
- Kalau kasusnya bukan security/malware, kemungkinan besar Claude Code akan balik nanya data tambahan sesuai kategorinya (error log, langkah reproduce bug, dst) sebelum bisa audit, karena file & db saja tidak selalu cukup untuk kategori selain security.
- Kalau branch utama repo ternyata bernama `master` bukan `main`, ganti kata itu di URL raw-nya.
