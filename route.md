# route.md (untuk agent)

1. Baca `Rules.md`.
2. Baca bagian Global di `scene.md`, lalu scene yang disebut user. Bila tidak disebut, ambil nomor terkecil dengan `status= belum`. Baca juga `akhir=` scene sebelumnya agar sambung.
3. Bila ada `reff=`, lihat file itu di `ref/`.
4. Tulis satu file `scene_NN_slug.py` untuk `src/`. Contoh bentuk yang benar ada di `examples/`.
5. Keluarkan hanya kode itu (satu blok kode atau satu file), tanpa penjelasan.

Jangan: menjalankan `main.py`, merender atau menganalisis frame, membuat zip, mengubah `scene.md`.
Bila prompt ambigu, tanya satu pertanyaan, lalu kerjakan.
