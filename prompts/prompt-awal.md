# Prompt Awal

Copy template ini tiap mulai kasus baru, isi bagian [ISI], lalu jalankan di Claude Code / opencode.

```
Saya butuh investigasi masalah website WordPress. Baca panduan kerja dari repo ini dulu: https://github.com/[username]/[repo]/00-router.md, ikuti instruksinya.

File WordPress lokal di [ISI PATH]. Database dump lokal di [ISI PATH]. Gejala yang saya lihat: [ISI].

Kalau checklist yang kepilih butuh cross-check VirusTotal, baca API key dari environment variable VT_API_KEY (sudah di-set di VPS/PC ini). Jangan minta saya ketik ulang key-nya di chat.

Jangan eksekusi apapun sebelum saya konfirmasi di tiap tahap yang diminta router.
```

## Catatan

- Ganti `[username]/[repo]` dengan URL repo GitHub kamu yang sebenarnya.
- Path lokal (file WordPress, db dump) selalu path di mesin yang menjalankan Claude Code, bukan path di repo GitHub.
- Kalau kasusnya bukan security/malware, kemungkinan besar Claude Code akan balik nanya data tambahan sesuai kategorinya (error log, langkah reproduce bug, dst) sebelum bisa audit, karena file & db saja tidak selalu cukup untuk kategori selain security.
