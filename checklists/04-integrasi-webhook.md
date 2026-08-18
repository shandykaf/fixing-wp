# Checklist: Integrasi/Webhook Bermasalah

- Cek log request masuk di endpoint webhook (kalau ada logging custom) atau di dashboard provider (Xendit/KiriminAja dashboard punya log delivery webhook).
- Cek response code yang dikirim balik ke provider saat webhook masuk, harus 200 kalau berhasil diterima, kalau bukan itu penyebab provider retry terus atau berhenti kirim.
- Cek signature/secret verification di kode webhook handler, sering jadi penyebab request ditolak diam-diam.
- Cek apakah endpoint URL di provider dashboard masih sesuai dengan yang aktif di server (ganti domain/SSL bisa bikin mismatch).
- Cek payload yang diterima vs yang diharapkan kode (field API kadang berubah setelah update dari provider).
- Cek status job/cron kalau prosesnya async (queue gak jalan, worker mati, dll).

Sebelum eksekusi:
Laporkan di titik mana rantai integrasi ini putus (provider gak kirim, endpoint gak nerima, atau nerima tapi salah proses). Tunggu konfirmasi sebelum ubah kode.

Setelah selesai:
Test end-to-end pakai transaksi/data dummy dulu sebelum dianggap fix di live.
