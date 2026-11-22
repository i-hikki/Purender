<div align="center">

# Purender

**basePlate** untuk animasi render murni: tulis scene dalam teks, agent AI menulis kode Python, hasilnya video MP4.

Tanpa aset gambar, tanpa editor, tanpa library berat. Semua frame dihitung dari rumus dengan `numpy` lalu di-encode oleh `ffmpeg`.

[![MIT license](https://img.shields.io/badge/license-MIT-f4c430?style=flat-square)](LICENSE)
[![](https://img.shields.io/discord/1224048331685101588?logo=discord&logoColor=white&label=Discord&color=5865F2&style=flat-square)](https://discord.gg/nYNDTSVZZG)

</div>

## Ide konsep
Satu `scene.md` = satu video. Video dipecah jadi beberapa scene bernomor, panjang tiap scene bebas (`waktu= 0:03-0:05`). Kamu menulis deskripsi dan dialognya di `scene.md`. Agent membaca `route.md` dan menulis satu file kode per scene. Kamu merender tiap scene jadi klip MP4 di `output/`, lalu menyatukannya di editor video bersama dubbing atau MP3 apa pun. Semua gerak dihitung dari waktu video utuh, jadi antar klip tetap nyambung.

## Struktur

```
Purender/
├── scene.md       daftar scene (judul, promp, mp3, reff, status)
├── Rules.md       aturan: library, penulisan, larangan, API kit
├── route.md       arahan singkat untuk agent
├── tutorial.md    instalasi (desktop & Termux) dan cara pakai
├── main.py        menjalankan satu file di src/
├── lib/kit.py     primitif gambar bersama (kapsul, elips, IK, kamera, keyframe, encoder)
├── lib/props.py   blok visual siap pakai (langit, matahari, bukit, tiang, bendera, burung)
├── src/           tepat 1 file scene aktif
├── examples/      contoh 4 scene (satu video 12 detik), salin ke src/ untuk mencoba
├── ref/           gambar atau catatan acuan
└── output/        hasil MP4
```

## Mulai cepat

```
pip install -r requirements.txt
python main.py
```

Hasil: `output/scene_01_wide.mp4`. Untuk mencoba scene lain, salin dari `examples/` ke `src/` (gantikan file yang ada). Instalasi lengkap (Windows, Linux, macOS, Termux) ada di [tutorial.md](tutorial.md).

## Cara pakai
1. Tulis scene dan berkreasilah di [scene.md](scene.md).
2. Lempar ke agent dan suruh: `baca route.md`.
3. Agent hanya mengeluarkan satu file `scene_NN_slug.py`. Kamu taruh di `src/`.
4. Kamu menjalankan `python main.py`, memeriksa hasilnya, dan menandai `status= selesai`.
5. Ulangi untuk scene berikutnya, lalu satukan klip di editor video.

Aturan yang dipatuhi agent ada di [Rules.md](Rules.md): hanya `numpy`, tanpa komentar di kode render, satu file scene di `src/`.

## Kebutuhan
Python 3.9+, numpy, ffmpeg.

## License
[MIT](LICENSE)
