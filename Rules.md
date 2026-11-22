# Rules.md

Berlaku untuk semua scene. Tujuan: konsisten dan hemat token.

## Teknologi
- Python 3.9+, ffmpeg (program sistem).
- Satu-satunya library pihak ketiga: `numpy`. Selain itu hanya stdlib.
- Render murni: semua gambar dihitung dari rumus/numpy. Tidak memuat gambar, video, atau font dari luar.
- `ref/` hanya dibaca agent sebagai acuan visual, tidak dimuat oleh kode render.

## Kontrak file scene
- Tepat satu file di `src/`, nama `scene_NN_slug.py` (NN = nomor scene). Hasil: `output/scene_NN_slug.mp4`.
- Agent hanya menghasilkan file itu. Render dan penandaan `status=` dilakukan user. Bila agent punya akses file, hapus file lain di `src/`; bila tidak, user yang melakukannya.
- Awal file: `import kit as k`, `SKALA = "landscape"` (dari `scene.md`), `W, H = k.SIZE[SKALA]`, `FPS, T0, DUR = ...` (T0 dan DUR dari `waktu=`), lalu `k.init(W, H)`.
- `frame(t)` fungsi murni, `t` detik dalam scene. Semua gerak memakai waktu video utuh `T = T0 + t`. Mengembalikan `uint8` berbentuk `(H, W, 3)`.
- Posisi dan ukuran dihitung dari `W` dan `H` (misal `0.2 * H`), bukan angka piksel mati.
- Keadaan awal scene harus sama dengan `akhir=` scene sebelumnya. Hukum dunia yang berlaku sepanjang video (langit, gerak bendera, dsb.) ditulis di Global `scene.md` dan dihitung dari `T`.
- Hitung semua yang statis satu kali di luar `frame`.
- Dilarang: memanggil ffmpeg sendiri, `print`, `input`, `sys.exit`, `if __name__`, akses jaringan, menulis file apa pun.
- Dilarang loop per-piksel. Vektorkan dengan numpy.

## Penulisan
- Tanpa komentar. Tanpa docstring.
- Nama pendek, tanpa penjelasan berlebih.
- Gaya konsisten antar scene: bila tokoh/warna sudah ada di scene sebelumnya, pakai bentuk dan palet yang sama.

## Standar video (ubah di sini bila perlu)
- Ukuran mengikuti `skala`: landscape 960x540, portrait 540x960, square 720x720. 30 fps, H.264 yuv420p (diatur `kit.encode`).
- Tanpa fade per scene. Penyambungan dihaluskan di editor.

## Pustaka bersama `lib/kit.py`
Jangan diubah tanpa izin user. Jangan menulis ulang fungsi yang sudah ada.

| Fungsi | Guna |
|---|---|
| `k.init(w, h)` | siapkan grid `k.X` (1,W) dan `k.Y` (H,1) |
| `k.mask()` | mask kosong (H,W) float32 |
| `k.cap(m, p0, p1, r0, r1)` | kapsul meruncing (anggota badan, tali, batang) |
| `k.ell(m, c, rx, ry, ang)` | elips |
| `k.poly(m, pts)` | poligon cembung |
| `k.chain(m, pts, r0, r1)` | rantai kapsul (kurva) |
| `k.sag_line(m, a, b, sag, r)` | tali melengkung |
| `k.ik(hip, foot, l1, l2, sign)` | IK dua tulang, return (lutut, kaki) |
| `k.foot_path(phase, amp, lift)` | lintasan langkah (x, angkat) |
| `k.paint(img, m, rgb, y0, y1)` | warnai `img` memakai mask |
| `k.vgrad(stops_y, colors)` | gradasi vertikal (H,W,3) |
| `k.sstep(a, b, x)` | smoothstep |
| `k.SIZE[skala]` | (W, H) untuk landscape / portrait / square |
| `k.lerp(a, b, f)`, `k.ease(f)` | interpolasi, easing smoothstep |
| `k.keys(T, [(t, nilai), ...], easing)` | nilai (angka atau warna) berdasarkan keyframe waktu |
| `k.Cam(cx, cy, z)` | kamera: `.pt(p, f)`, `.r(r, f)`, `.grid(f)`; `f` = paralaks (1 dekat, <1 jauh) |

Primitif menggambar ke mask dengan tepi halus (anti-alias), nilai 0..1.

## Blok visual `lib/props.py`
Pakai dulu sebelum menulis sendiri. Semua menerima `Cam` dan waktu `T`.

| Fungsi | Guna |
|---|---|
| `props.backdrop(cam, T, "fajar", t0, t1)` | langit + matahari + bukit + tanah; return `(img, tint)`. `t0..t1` = rentang perubahan suasana |
| `props.pole(img, cam, x, y_top, y_bot, r, tint)` | tiang bendera |
| `props.flag(img, cam, x0, y0, fw, fh, T, amp, tint)` | bendera merah putih berkibar |
| `props.bird(img, x, y, T, fase, skala, arah)` | burung mengepak (koordinat layar) |

Preset suasana saat ini: `"fajar"`. Butuh yang lain: minta user menambah di `PRESET`, jangan mengubah yang ada.
