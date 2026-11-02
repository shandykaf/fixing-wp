# Template Worklog

Catatan kerja berjalan, di-append selama pengerjaan. Bedanya dengan `laporan.md`: worklog itu catatan mentah per-kejadian yang ditulis **sambil jalan**, laporan itu ringkasan rapi yang disusun **di akhir** dari isi worklog ini.

**Kenapa perlu**, bukan sekadar nambah file:

- **Jejak pemulihan.** Kalau situs rusak setelah pembersihan, ini satu-satunya cara tahu persis apa yang dicabut dan backup-nya di mana. Tanpa ini, "kayaknya tadi ada file yang kehapus" itu gak bisa ditelusuri.
- **Sesi bisa putus.** Context ke-compact, kuota habis, atau lanjut besok — sesi baru tinggal baca worklog buat tahu posisi terakhir, gak perlu ngulang investigasi.
- **Laporan akhir gak ditulis dari ingatan.** Timeline dan daftar tindakan disalin dari sini, jadi gak ada detail yang melar atau hilang.

**Aturan sama kayak laporan:** simpan di folder kasus lokal (jangan di repo ini, jangan di-commit), dan jangan tulis password/API key di dalamnya. Nama yang disaranin: `worklog-<domain>-<YYYY-MM-DD>.md`.

**Jangan nulis tiap tool call** — itu cuma bikin noise. Append cuma di lima titik ini:

1. **Sebelum tiap tindakan destruktif** (hapus file, timpa file, ubah/hapus baris db, ganti setting di live). Wajib, dan ditulis SEBELUM dieksekusi, bukan sesudah.
2. **Tiap temuan dikonfirmasi** — jangan ditunda sampai akhir.
3. **Tiap pindah fase**, sekalian catat model yang dipakai.
4. **Tiap keputusan user** — approve daftar hapus, nolak sesuatu, minta skip langkah.
5. **Tiap kendala** — kuota VirusTotal habis, access log gak dikasih hosting, plugin gak bisa diupdate karena lisensi mati.

---

```markdown
# Worklog — <domain>

Kasus: <kategori> · Mulai: <YYYY-MM-DD HH:MM>
Folder kerja: <path copy yang dikerjakan>
Backup sebelum diutak-atik: <path>

---

## <YYYY-MM-DD HH:MM> — Fase: <nama fase> (model: <model yang dipakai>)

<Apa yang dikerjakan di fase ini, singkat aja.>

## <YYYY-MM-DD HH:MM> — Temuan: <judul singkat>

- Lokasi: <path file / tabel + row id>
- Isi/indikasi: <pola apa yang bikin dicurigai, kutip potongan kodenya kalau pendek>
- Tingkat keyakinan: <pasti malicious / perlu dicek lagi / kemungkinan false positive>
- Dasar: <match pola backdoor / checksum core gak cocok / terdeteksi N engine VirusTotal>

## <YYYY-MM-DD HH:MM> — AKAN HAPUS/UBAH: <target>

- Target: <path lengkap atau tabel+row>
- Alasan: <temuan yang mana>
- Backup salinannya ada di: <path> ← wajib diisi, ini yang dipakai kalau perlu rollback
- Disetujui user: <ya, jam berapa / belum>

## <YYYY-MM-DD HH:MM> — SUDAH DIEKSEKUSI: <target>

- Hasil: <berhasil / gagal + pesan errornya>
- Efek samping yang kelihatan: <situs masih normal / halaman X jadi error>

## <YYYY-MM-DD HH:MM> — Keputusan user

<Apa yang diputuskan, misal: "approve hapus 12 file di daftar, tapi minta plugin
premium X jangan diupdate dulu karena lisensinya mati.">

## <YYYY-MM-DD HH:MM> — Kendala

<Apa yang menghambat dan dampaknya ke hasil, misal: "kuota VirusTotal habis di
hash ke-412 dari 530, sisanya belum diverifikasi — dicatat juga di laporan akhir.">
```
