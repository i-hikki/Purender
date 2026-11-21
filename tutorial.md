# tutorial.md

## Kebutuhan
- Python 3.9 atau lebih baru
- numpy
- ffmpeg

## Instalasi: Desktop

### Windows
1. Unduh Python dari https://www.python.org/downloads/ lalu centang **Add python.exe to PATH** saat instalasi.
   Atau lewat terminal: `winget install Python.Python.3.12`
2. Pasang ffmpeg: `winget install Gyan.FFmpeg`
3. Tutup lalu buka ulang terminal, cek:
   ```
   python --version
   ffmpeg -version
   ```
   Bila `python` tidak dikenali, coba `py --version` dan pakai `py` sebagai pengganti `python`.
4. Di folder purender:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Linux / WSL (Ubuntu, Debian)
```
sudo apt update
sudo apt install -y python3 python3-venv ffmpeg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Jalankan `sudo apt update` lebih dulu supaya tidak muncul error 404 saat mengunduh paket.

### macOS
```
brew install python ffmpeg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Instalasi: Termux (Android)
Pasang Termux dari F-Droid atau source github, lalu:
```
pkg update && pkg upgrade
pkg install python python-numpy ffmpeg
termux-setup-storage
```
Gunakan `pkg install python-numpy`, bukan `pip install numpy`, karena pip di Termux membangun numpy dari sumber dan lama/gagal.
Tidak perlu venv.

## Menjalankan
```
python main.py
```
Di Termux dan Linux/macOS tanpa alias, pakai `python3 main.py`.
`main.py` menjalankan satu-satunya file di `src/` dan menyimpan MP4 ke `output/` dengan nama yang sama dengan file scene.

## Alur kerja
1. Tulis scene di `scene.md` (format ada di bagian atas file itu).
2. Taruh gambar atau catatan acuan di `ref/` bila perlu, lalu tulis path-nya di `reff=`.
3. Beri tahu agent: **"baca route.md"**.
4. Agent mengerjakan scene bernomor terkecil yang `status= belum`, menjalankan `python main.py`, lalu menandainya `selesai`.
5. Ambil MP4 dari `output/`, rekam atau dubbing `mp3=` di editor video favoritmu, lalu satukan.
6. Ketik "lanjut" untuk scene berikutnya.

## Masalah umum
| Pesan | Penyebab / solusi |
|---|---|
| `No module named 'numpy'` | numpy belum terpasang. Ulangi langkah instalasi, pastikan venv aktif. |
| `ffmpeg tidak ditemukan` | Pasang ffmpeg dan pastikan ada di PATH. |
| `src/ harus berisi tepat 1 file .py` | Hapus file scene lama di `src/`. |
| Render lambat di HP | Turunkan `W, H` di file scene (misal 640x360). |
