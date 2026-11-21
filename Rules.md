# Rules.md

Berlaku untuk semua scene. Tujuan: konsisten dan hemat token.

## Teknologi
- Python 3.9+, ffmpeg (program sistem).
- Satu-satunya library pihak ketiga: `numpy`. Selain itu hanya stdlib.
- Render murni: semua gambar dihitung dari rumus/numpy. Tidak memuat gambar, video, atau font dari luar.
- `ref/` hanya dibaca agent sebagai acuan visual, tidak dimuat oleh kode render.

## Kontrak file scene
- Tepat satu file di `src/`, nama `scene_NN_slug.py` (NN = nomor scene). Hapus file scene sebelumnya.
- Hasil: `output/scene_NN_slug.mp4`.
- Harus mendefinisikan: `W, H, FPS, DUR` dan `frame(t)`.
- Awal file: `import kit as k`, lalu `k.init(W, H)`.
- `frame(t)` fungsi murni (t dalam detik), mengembalikan `uint8` berbentuk `(H, W, 3)`. Tanpa state yang berubah antar panggilan.
- Hitung semua yang statis (langit, latar, mask) satu kali di luar `frame`.
- Dilarang: memanggil ffmpeg sendiri, `print`, `input`, `sys.exit`, `if __name__`, akses jaringan, menulis file apa pun.
- Dilarang loop per-piksel. Vektorkan dengan numpy. Target render per scene di bawah 3 menit.

## Penulisan
- Tanpa komentar. Tanpa docstring.
- Nama pendek, tanpa penjelasan berlebih.
- Gaya konsisten antar scene: bila tokoh/warna sudah ada di scene sebelumnya, pakai bentuk dan palet yang sama.

## Standar video (ubah di sini bila perlu)
- 960x540, 30 fps, H.264 yuv420p (diatur `kit.encode`).
- Fade in/out hanya bila diminta di promp.

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

Primitif menggambar ke mask dengan tepi halus (anti-alias), nilai 0..1.
