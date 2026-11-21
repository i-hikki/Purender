# route.md (untuk agent)

1. Baca `Rules.md`.
2. Baca `scene.md`. Ambil scene bernomor terkecil dengan `status= belum`.
3. Bila ada `reff=`, lihat file itu di `ref/`.
4. Tulis `src/scene_NN_slug.py` sesuai `Rules.md`. Hapus file lain di `src/`.
5. Jalankan `python main.py`. Perbaiki sampai berhasil.
6. Cek hasil: ambil satu-dua frame dari `output/scene_NN_slug.mp4` dan lihat.
7. Ubah `status= selesai` pada scene itu, lalu laporkan singkat.
8. Berhenti. Lanjut ke nomor berikutnya hanya bila user bilang "lanjut" atau "kerjakan semua".

Bila prompt scene ambigu, tanya satu pertanyaan, lalu kerjakan.
