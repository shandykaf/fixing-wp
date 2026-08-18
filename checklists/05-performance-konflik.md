# Checklist: Performance/Konflik Script

- Cek console browser buat JS error spesifik dan file mana sumbernya.
- Kalau abis pasang plugin optimasi (WP Rocket, dll), disable fitur delay JS/minify satu per satu buat isolasi konfliknya.
- Cek elemen yang rusak secara visual, bandingkan sebelum/sesudah optimasi diaktifkan.
- Cek exclude list di plugin optimasi, biasanya script tertentu (popup, form validation) perlu di-exclude dari delay/minify.
- Cek waktu loading pakai PageSpeed/GTmetrix buat baseline sebelum dan sesudah perbaikan.
- Cek apakah masalahnya cuma di device/browser tertentu atau semua.

Sebelum eksekusi:
Sebutkan script/plugin mana yang jadi sumber konflik dan rencana fix-nya (exclude, reorder, atau downgrade). Tunggu konfirmasi.

Setelah selesai:
Bandingkan skor performance sebelum/sesudah, pastikan fix gak balikin masalah lambatnya lagi.
