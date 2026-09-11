# Prompt Awal

Copy template ini tiap mulai kasus baru, isi bagian `ISI_...`, lalu jalankan di Claude Code / opencode.

```
Saya butuh investigasi masalah website WordPress.
Akses repo ini dulu:
https://github.com/shandykaf/fixing-wp

Baca panduan kerja dari repo ini dan ikuti instruksinya:
https://raw.githubusercontent.com/shandykaf/fixing-wp/main/00-router.md

- Sumber file WordPress = ISI_PATH
- Sumber database = ISI_PATH
- Gejala yang saya lihat = ISI_GEJALA

Sumber di atas boleh berupa folder biasa, file .sql/.sql.gz, file .zip, atau backup
plugin (WPvivid/UpdraftPlus). Kalau file & db jadi satu di backup yang sama, tulis
path yang sama di dua baris itu. Kalau masih berbentuk arsip, ekstrak sendiri dulu
sesuai bagian "Sumber data berupa backup" di router, jangan minta saya ekstrak manual.

Jangan eksekusi apapun sebelum saya konfirmasi di tiap tahap yang diminta router.
```

## Catatan

- Repo ini private, pastikan Claude Code/opencode sudah punya autentikasi GitHub (misal `gh auth login`) sebelum menjalankan prompt di atas, kalau belum akan gagal akses (404).
- Path lokal (file WordPress, db dump) selalu path di mesin yang menjalankan Claude Code, bukan path di repo GitHub.
- Bentuk sumber data yang didukung: folder WordPress aktif, hasil ekstrak backup, file `.sql`/`.sql.gz`, file `.zip`, atau backup plugin (WPvivid, UpdraftPlus, dll). Kalau backup-nya displit jadi beberapa part (`_files_1.zip`, `_files_2.zip`, dst) atau dienkripsi, sebutkan di prompt — part-nya harus lengkap semua, dan yang dienkripsi butuh passwordnya.
- Kalau kamu punya beberapa backup dari tanggal berbeda, sebutkan juga. Backup dari sebelum masalah muncul dipakai sebagai baseline buat diff, dan ini biasanya cara tercepat nemuin akar masalahnya (berlaku di semua kategori, bukan cuma security).
- Kalau kasusnya bukan security/malware, kemungkinan besar Claude Code akan balik nanya data tambahan sesuai kategorinya (error log, langkah reproduce bug, dst) sebelum bisa audit, karena file & db saja tidak selalu cukup untuk kategori selain security.
- Kalau branch utama repo ternyata bernama `master` bukan `main`, ganti kata itu di URL raw-nya.
