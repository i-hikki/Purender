# scene.md

Satu file ini = satu video. Video dipecah jadi beberapa scene bernomor, panjangnya bebas.
Yang wajib hanya nomor dan `promp=`. Isian lain boleh dihapus atau ditambah.
Kamu yang menandai `status=`. Agent tidak mengubah file ini.

## Global
```
judul= Fajar Merah Putih
skala= landscape
fps= 30
gaya= Fajar ke pagi cerah selama 12 detik (preset "fajar"). Bendera naik pelan dari dasar tiang (detik 0-9) sambil berkibar. Tanpa tokoh.
```
- `skala`: `landscape` 960x540, `portrait` 540x960, `square` 720x720.
- Posisi dan ukuran di kode dihitung dari `W` dan `H`, jadi ganti `skala` cukup mengubah satu baris.

## Format scene
```
## N. Judul (opsional)
waktu= mm:ss-mm:ss     posisi scene di timeline video utuh
promp= detail visual: apa yang tampak, bergerak, kamera, suasana
mp3= dialog/narasi yang kamu rekam atau dubbing di editor
reff= ref/nama_file    (opsional)
awal= keadaan di detik pertama     (opsional, untuk menyambung dengan scene sebelumnya)
akhir= keadaan di detik terakhir   (opsional)
status= belum | selesai
```
`waktu=` menentukan `T0` dan `DUR` di kode. Semua gerak dihitung dari waktu video utuh `T = T0 + t`,
sehingga kibaran, posisi, dan warna langit otomatis nyambung antar scene.

---

## 1. Bendera naik, tampak lebar
waktu= 0:00-0:03
promp= Tiang bendera dari dasar tanah, bukit gelap di belakang, langit fajar ungu-oranye, matahari baru terbit. Bendera merah putih mulai naik pelan dari bawah sambil berkibar. Kamera diam, tampak lebar.
mp3= -
awal= kamera lebar tengah (zoom 1.0). Bendera di dasar tiang.
akhir= bendera sudah naik sekitar sepertiga tiang. Kamera masih lebar.
status= belum

## 2. Mendekat ke kain
waktu= 0:03-0:05
promp= Kamera mendekat (push-in) ke bendera sampai kain memenuhi layar. Cahaya matahari terbit hangat dari belakang. Bendera terus naik.
mp3= -
awal= sama dengan akhir scene 1.
akhir= close-up bendera (zoom 1.8), bendera di tengah layar.
status= belum

## 3. Mengikuti bendera naik
waktu= 0:05-0:09
promp= Kamera mengikuti bendera naik ke puncak tiang sambil perlahan menjauh. Langit berubah dari fajar ke pagi cerah.
mp3= -
awal= sama dengan akhir scene 2.
akhir= bendera di puncak tiang, kamera agak lebar (zoom 1.15).
status= belum

## 4. Di puncak, burung lewat
waktu= 0:09-0:12
promp= Bendera berkibar di puncak tiang. Tiga burung terbang melintas dari kanan ke kiri. Kamera turun sedikit dan menjauh pelan, langit biru cerah.
mp3= -
awal= sama dengan akhir scene 3.
akhir= kamera zoom 1.0, bendera masih di puncak.
status= belum
