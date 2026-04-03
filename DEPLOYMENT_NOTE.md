# 📘 Gudang Bot - Panduan Pasang & Balik

## 🚀 1. Cara Pasang (Install)
Lakukan ini saat SETIAP pertama kali install di VPS:

1. **Clone Repository (Ambil Kode dari GitHub)**
   ```bash
   git clone https://github.com/Lebo-20/gdsdl.git
   cd gdsdl
   ```

2. **Install Depedensi (Bahan-bahan)**
   ```bash
   pip install httpx telethon tqdm python-dotenv
   cd proxy && npm install && cd ..
   ```

3. **Pastikan File Credentials (Penting!)**
   Karena `.env` dan `.session` file kita sembunyikan dari GitHub:
   - Buat file `.env` baru: `nano .env`
   - Isi dengan: `API_ID=xxx`, `API_HASH=xxx`, `BOT_TOKEN=xxx`, etc.
   - Pindahkan file `.session` lama Anda (jika ada) ke folder ini.

## 📁 2. Cara Balik (Management)
Lakukan ini saat SETIAP ingin memantau atau memperbaiki bot di PuTTY:

1. **Melihat Log (Mengetahui Apa yang Sedang Dikerjakan Bot)**
   Jangan jalankan bot dua kali! Cukup lihat log-nya:
   ```bash
   tail -f bot.log
   ```

2. **Cara Menjalankan di Background (Terus Aktif Setelah PuTTY DITUTUP)**
   - Jalankan PROXY dulu: `cd proxy && nohup node server.js > proxy.log 2>&1 &`
   - Jalankan BOT: `cd .. && nohup python3 main.py > bot.log 2>&1 &`

3. **Cara Stop Bot (Restart)**
   Cek ID bot yang sedang jalan: `ps aux | grep python3`
   Matikan dengan ID-nya: `kill -9 [NOMOR_PID]`

## 💡 3. Perintah Telegram (ADMIN)
Setelah bot jalan, Anda cukup kontrol lewat chat:

- **/panel**: Tombol Start/Stop Auto Scan.
- **/download [ID]**: Download drama tertentu.
- **/update**: Tarik update terbaru dari kode GitHub kita secara otomatis.

---
*Simpan catatan ini atau ketik `cat DEPLOYMENT_NOTE.md` di terminal Anda kapan saja.*
