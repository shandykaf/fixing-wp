# Prompt Awal

Copy template ini tiap mulai kasus baru, isi bagian [ISI], lalu jalankan di Claude Code / opencode.

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

## Catatan

- Repo ini private, pastikan Claude Code/opencode sudah punya autentikasi GitHub (misal `gh auth login`) sebelum menjalankan prompt di atas, kalau belum akan gagal akses (404).
- Path lokal (file WordPress, db dump) selalu path di mesin yang menjalankan Claude Code, bukan path di repo GitHub.
- Kalau kasusnya bukan security/malware, kemungkinan besar Claude Code akan balik nanya data tambahan sesuai kategorinya (error log, langkah reproduce bug, dst) sebelum bisa audit, karena file & db saja tidak selalu cukup untuk kategori selain security.
- Kalau branch utama repo ternyata bernama `master` bukan `main`, ganti kata itu di URL raw-nya.
