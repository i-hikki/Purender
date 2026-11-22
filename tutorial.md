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
Bawaan repo: `src/` berisi `scene_01_wide.py`. Contoh scene 2 sampai 4 ada di `examples/`.

## Alur kerja
1. Tulis video di `scene.md`: bagian Global (`skala`, `fps`, `gaya`), lalu scene bernomor dengan `waktu=`, `promp=`, `mp3=`.
2. Taruh gambar atau catatan acuan di `ref/` bila perlu, lalu tulis path-nya di `reff=`.
3. Beri tahu agent: **"baca route.md, kerjakan scene 1"**.
4. Agent mengeluarkan satu file kode. Simpan di `src/` (hapus file scene sebelumnya).
5. Jalankan `python main.py`, periksa hasilnya di `output/`, lalu ubah `status= selesai` di `scene.md`.
6. Ulangi dari langkah 3 untuk scene berikutnya.
7. Satukan klip dan rekam atau dubbing `mp3=` di editor video favoritmu.

Bila ada error, tempel pesan error ke agent dengan nomor scene-nya.

## Masalah umum
| Pesan | Penyebab / solusi |
|---|---|
| `No module named 'numpy'` | numpy belum terpasang. Ulangi langkah instalasi, pastikan venv aktif. |
| `ffmpeg tidak ditemukan` | Pasang ffmpeg dan pastikan ada di PATH. |
| `src/ harus berisi tepat 1 file .py` | Hapus file scene lama di `src/`. |
| Render lambat di HP | Turunkan `W, H` di file scene (misal 640x360). |
