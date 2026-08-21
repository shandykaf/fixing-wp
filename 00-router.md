# Router: WordPress Incident Response

Entry point tunggal. Isi [ISI] lalu jalankan prompt ini duluan sebelum baca checklist manapun.

---

## Prompt

Saya butuh investigasi masalah di website WordPress. Jangan baca atau eksekusi checklist apapun dulu, mulai dari klasifikasi.

Data situs:
Domain [ISI]. Akses [ISI: cPanel/SSH/WP admin/FTP]. Gejala [ISI: deskripsikan sedetail mungkin, kapan mulai, ada perubahan terakhir gak sebelum masalah muncul]. Screenshot/error message kalau ada [ISI atau "tidak ada"].

Klasifikasikan ke salah satu dari 5 kategori berikut, kasih alasan singkat kenapa pilih itu:

1. Security/malware — indikasi kompromi: rogue admin, redirect asing, file backdoor, situs disuspend hosting, spam SEO muncul di Google.
2. Error teknis/situs down — 500 error, white screen, fatal error PHP, timeout, situs gak bisa diakses tapi gak ada tanda kompromi.
3. Bug fungsional — fitur spesifik gak jalan sesuai harusnya (form, shortcode custom, checkout field), sisanya situs normal.
4. Integrasi/webhook bermasalah — payment gateway atau shipping API gak sync, callback gak diterima, data gak update otomatis.
5. Performance/konflik script — situs lambat, elemen visual rusak, JS error di console, biasanya abis pasang plugin optimasi baru.

Kalau gejala bisa masuk lebih dari satu kategori (contoh: error 500 tapi juga ada rogue admin), pilih kategori paling berisiko duluan (security selalu prioritas di atas yang lain).

Setelah klasifikasi, sebutkan nama file checklist yang harus dibaca:
- Kategori 1 → 01-security-malware.md
- Kategori 2 → 02-error-teknis.md
- Kategori 3 → 03-bug-fungsional.md
- Kategori 4 → 04-integrasi-webhook.md
- Kategori 5 → 05-performance-konflik.md

Tunggu konfirmasi saya sebelum baca file checklist itu dan mulai eksekusi.

---

## Sumber data berupa backup (WPvivid atau plugin backup lain)

Berlaku di semua kategori, bukan cuma security. Kalau file/db yang dikasih user bukan folder WordPress aktif tapi hasil backup dari plugin (WPvivid, UpdraftPlus, dll):

- Formatnya biasanya zip terpisah antara file dan db (contoh WPvivid: `wpvividbackup_*_files_*.zip` dan `wpvividbackup_*_db_*.zip` isinya `.sql`). Kalau situsnya besar, file zip-nya sering displit jadi beberapa part (`_files_1.zip`, `_files_2.zip`, dst) — ekstrak SEMUA part, jangan cuma yang pertama.
- Kalau backup di-enkripsi (fitur premium beberapa plugin backup), minta password enkripsinya ke user dulu sebelum bisa diekstrak.
- Backup gak otomatis berarti "bersih" — kalau diambil setelah masalah muncul, isinya ikut kebawa masalah yang sama. Tetap diperlakukan sesuai checklist kategori yang dipilih, bukan dilewati begitu aja.
- **Kalau ada beberapa backup dari tanggal berbeda**, ini baseline yang berharga: ekstrak backup paling lama (dari sebelum gejala muncul) dan bandingkan (diff nama file + hash, atau isi db) dengan kondisi situs sekarang. File/baris db yang beda antara backup lama vs sekarang biasanya nunjuk langsung ke penyebabnya — dipakai di tiap kategori sesuai konteksnya (lihat checklist masing-masing).

---

## Setup akses browser (dikerjakan Claude sendiri, bukan manual oleh user)

Berlaku di semua kategori — dibutuhkan tiap kali checklist nyebut "browser otomatis" atau trigger "situs sudah live". Repo ini dipakai lintas tool (Claude Code, opencode, dll), jadi caranya distandarkan pakai **Playwright MCP** — server MCP resmi Microsoft yang nyediain kontrol browser (navigate, klik, isi form, screenshot) lewat protokol MCP standar, didukung hampir semua coding agent modern.

Claude WAJIB cek dan setup ini sendiri, tanpa minta user ketik command:

1. Cek apakah tool browser udah tersedia (browser tool bawaan, atau MCP server Playwright yang udah keregister). Kalau udah ada, lanjut aja, gak perlu install ulang.
2. Kalau belum ada, install & register sendiri sesuai tool yang lagi dipakai. Servernya sama di semua tool (`npx -y @playwright/mcp@latest`), yang beda cuma cara daftarinnya:

   - **Claude Code** — jalankan lewat tool Bash:
     ```
     claude mcp add playwright -- npx -y @playwright/mcp@latest
     ```
     (tambah `-s user` kalau mau kepasang permanen buat semua project di mesin itu, bukan cuma project ini)

   - **opencode** — tulis/merge ke `opencode.json` (atau `opencode.jsonc`) via tool Write:
     ```json
     {
       "$schema": "https://opencode.ai/config.json",
       "mcp": {
         "playwright": {
           "type": "local",
           "command": ["npx", "-y", "@playwright/mcp@latest"],
           "enabled": true
         }
       }
     }
     ```

   - **Cursor** — tulis/merge ke `.cursor/mcp.json` (project) atau `~/.cursor/mcp.json` (global) via tool Write:
     ```json
     {
       "mcpServers": {
         "playwright": {
           "type": "stdio",
           "command": "npx",
           "args": ["-y", "@playwright/mcp@latest"]
         }
       }
     }
     ```

   - **Tool lain yang support MCP** (Windsurf, Cline, Zed, dll): formatnya mirip salah satu di atas — kebanyakan pakai pola `mcpServers` + `command`/`args` seperti Cursor. Cek dokumentasi MCP tool tersebut, lalu tulis entry-nya sendiri via tool Write.

   Penting: kalau file config-nya udah ada isinya, MERGE entry playwright ke dalamnya — jangan timpa seluruh file dan hilangin config user yang lain.
3. Setelah keregister, reconnect/restart sesi MCP kalau tool-nya butuh itu, lalu verifikasi tool browser beneran muncul dan bisa dipanggil sebelum lanjut ke audit/setup/fixing/verifikasi via browser.
4. Kalau ternyata tool yang dipakai gak support MCP sama sekali dan gak ada browser tool bawaan: infokan ke user bagian browser-otomatis di checklist yang dipakai gak bisa jalan, dan fallback ke mode dipandu manual (lihat checklist masing-masing kategori).
