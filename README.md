<div align="center">

# Purender

**basePlate** untuk animasi render murni: tulis scene dalam teks, agent AI menulis kode Python, hasilnya video MP4.

Tanpa aset gambar, tanpa editor, tanpa library berat. Semua frame dihitung dari rumus dengan `numpy` lalu di-encode oleh `ffmpeg`.

[![MIT license](https://img.shields.io/badge/license-MIT-f4c430?style=flat-square)](LICENSE)
[![](https://img.shields.io/discord/1224048331685101588?logo=discord&logoColor=white&label=Discord&color=5865F2&style=flat-square)](https://discord.gg/nYNDTSVZZG)

</div>

## Ide
Satu scene = satu video pendek. Kamu menulis deskripsi scene dan dialognya di `scene.md`. Agent membaca `route.md`, mengerjakan scene satu per satu, dan menyimpan MP4 ke `output/`. Dialog direkam sendiri di editor video, jadi animasi dan suara bisa disinkronkan per scene.

## Struktur

```
basePlate/
├── scene.md       daftar scene (judul, promp, mp3, reff, status)
├── Rules.md       aturan: library, penulisan, larangan, API kit
├── route.md       arahan singkat untuk agent
├── tutorial.md    instalasi (desktop & Termux) dan cara pakai
├── main.py        menjalankan satu file di src/
├── lib/kit.py     primitif gambar bersama (lingkaran, kapsul, IK, encoder)
├── src/           tepat 1 file scene aktif
├── ref/           gambar atau catatan acuan
└── output/        hasil MP4
```

## Mulai cepat

```
pip install -r requirements.txt
python main.py
```

Hasil: `output/scene_01_bendera.mp4`. Instalasi lengkap (Windows, Linux, macOS, Termux) ada di [tutorial.md](tutorial.md).

## Memakai agent
1. Tulis scene di `scene.md`.
2. Ketik ke agent: `baca route.md`.
3. Agent menulis `src/scene_NN_slug.py`, menjalankan `python main.py`, lalu menandai scene `selesai`.

Aturan yang dipatuhi agent ada di [Rules.md](Rules.md): hanya `numpy`, tanpa komentar di kode render, satu file scene di `src/`.

## Kebutuhan
Python 3.9+, numpy, ffmpeg.

## License
[MIT](LICENSE)
