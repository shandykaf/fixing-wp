# Checklist: Integrasi/Webhook Bermasalah

Kalau di tengah investigasi ketemu indikasi kompromi, STOP — pindah ke 01-security-malware.md.

## Cek yang memblok request masuk duluan (penyebab paling umum webhook "gak nyampe")

- Security plugin / WAF (Wordfence, dll): cek log blocked requests, apakah IP provider kena blok atau rate limit. Allowlist IP/range resmi provider kalau perlu.
- Cloudflare / proxy di depan situs: challenge/captcha ke request non-browser bikin webhook gagal diam-diam. Cek firewall events, bikin rule bypass untuk path endpoint webhook.
- SSL/TLS dari sisi provider: sertifikat expired atau chain gak lengkap bikin provider gagal connect tanpa error yang kelihatan di server. Test dari luar: `curl -v https://domain/endpoint` dan cek chain (atau SSL Labs).

## Diagnosis rantai integrasi

- Cek log request masuk di endpoint webhook (kalau ada logging custom) atau di dashboard provider (Xendit/KiriminAja dashboard punya log delivery webhook).
- Cek response code yang dikirim balik ke provider saat webhook masuk, harus 200 kalau berhasil diterima, kalau bukan itu penyebab provider retry terus atau berhenti kirim.
- Cek signature/secret verification di kode webhook handler, sering jadi penyebab request ditolak diam-diam.
- Cek apakah endpoint URL di provider dashboard masih sesuai dengan yang aktif di server (ganti domain/SSL bisa bikin mismatch).
- Cek payload yang diterima vs yang diharapkan kode (field API kadang berubah setelah update dari provider).
- Kalau ada backup dari sebelum integrasi ini bermasalah (lihat "Sumber data berupa backup" di `00-router.md`): diff file webhook handler/config vs backup lama buat cek apakah ada perubahan kode yang gak disengaja (bukan cuma dugaan perubahan dari sisi provider).
- Cek status job/cron kalau prosesnya async (queue gak jalan, worker mati, dll).
- Replay webhook buat reproduce: pakai fitur resend/replay di dashboard provider kalau ada, atau simulasi via curl dengan payload contoh + signature valid. Ini dipakai sejak diagnosis, bukan cuma pas test akhir.

## Cek pemrosesan ganda (idempotency)

- Provider retry kalau gak dapat 200 — pastikan handler cek ID transaksi/order sebelum proses, biar retry gak bikin order diproses dua kali (dobel update status, dobel kirim email, dll).

## Sebelum eksekusi

Laporkan di titik mana rantai integrasi ini putus (provider gak kirim, request diblok sebelum sampai, endpoint gak nerima, atau nerima tapi salah proses). Tunggu konfirmasi sebelum ubah kode.

## Setelah selesai

Test end-to-end pakai transaksi/data dummy dulu sebelum dianggap fix di live. Test juga skenario retry (kirim payload sama dua kali) buat mastiin gak dobel proses.

**Trigger verifikasi otomatis**: begitu user bilang fix-nya sudah dideploy ke live, Claude infokan dulu ("fix sudah live, saya test end-to-end sekarang ya") lalu langsung jalanin test transaksi dummy via browser otomatis (checkout/flow yang relevan) — gak perlu diminta terpisah. Kalau testnya butuh transaksi beneran (bukan sandbox/dummy) yang bisa kena biaya nyata, konfirmasi dulu ke user sebelum jalan.
