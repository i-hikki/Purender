import math
import shutil
import subprocess
import sys

import numpy as np

W = H = 0
X = Y = None
BETA = 0.62


def init(w, h):
    global W, H, X, Y
    W, H = w, h
    X = np.arange(w, dtype=np.float32)[None, :]
    Y = np.arange(h, dtype=np.float32)[:, None]


def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def mask():
    return np.zeros((H, W), np.float32)


def vgrad(stops_y, colors):
    ys = np.arange(H, dtype=np.float32)
    c = np.array(colors, np.float32)
    col = np.stack([np.interp(ys, stops_y, c[:, i]) for i in range(3)], axis=1)
    return np.repeat(col[:, None, :], W, axis=1).astype(np.float32)


def paint(img, m, rgb, y0=0, y1=None):
    seg = img[y0:y1]
    mm = m[y0:y1, :, None]
    seg[:] = seg * (1 - mm) + np.array(rgb, np.float32) * mm


def _box(x0, y0, x1, y1):
    xa, xb = max(int(math.floor(x0)), 0), min(int(math.ceil(x1)) + 1, W)
    ya, yb = max(int(math.floor(y0)), 0), min(int(math.ceil(y1)) + 1, H)
    if xa >= xb or ya >= yb:
        return None
    return slice(ya, yb), slice(xa, xb)


def cap(m, p0, p1, r0, r1=None):
    if r1 is None:
        r1 = r0
    R = max(r0, r1) + 2
    b = _box(min(p0[0], p1[0]) - R, min(p0[1], p1[1]) - R, max(p0[0], p1[0]) + R, max(p0[1], p1[1]) + R)
    if b is None:
        return
    sy, sx = b
    px, py = X[:, sx], Y[sy, :]
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    t = np.clip(((px - p0[0]) * dx + (py - p0[1]) * dy) / max(dx * dx + dy * dy, 1e-6), 0, 1)
    dist = np.hypot(px - (p0[0] + t * dx), py - (p0[1] + t * dy))
    np.maximum(m[sy, sx], np.clip(0.5 - (dist - (r0 + (r1 - r0) * t)), 0, 1), out=m[sy, sx])


def ell(m, c, rx, ry, ang=0.0):
    R = max(rx, ry) + 2
    b = _box(c[0] - R, c[1] - R, c[0] + R, c[1] + R)
    if b is None:
        return
    sy, sx = b
    ca, sa = math.cos(ang), math.sin(ang)
    dx, dy = X[:, sx] - c[0], Y[sy, :] - c[1]
    u, v = dx * ca + dy * sa, -dx * sa + dy * ca
    k = np.sqrt((u / rx) ** 2 + (v / ry) ** 2)
    g = np.sqrt((u / (rx * rx)) ** 2 + (v / (ry * ry)) ** 2)
    sdf = (k - 1) * np.where(k > 1e-3, k / np.maximum(g, 1e-9), min(rx, ry))
    np.maximum(m[sy, sx], np.clip(0.5 - sdf, 0, 1), out=m[sy, sx])


def poly(m, pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    b = _box(min(xs) - 2, min(ys) - 2, max(xs) + 2, max(ys) + 2)
    if b is None:
        return
    sy, sx = b
    cx, cy = sum(xs) / len(pts), sum(ys) / len(pts)
    px, py = X[:, sx], Y[sy, :]
    sdf = None
    for i in range(len(pts)):
        a, c = pts[i], pts[(i + 1) % len(pts)]
        ex, ey = c[0] - a[0], c[1] - a[1]
        l = math.hypot(ex, ey)
        nx, ny = ey / l, -ex / l
        if (cx - a[0]) * nx + (cy - a[1]) * ny > 0:
            nx, ny = -nx, -ny
        d = (px - a[0]) * nx + (py - a[1]) * ny
        sdf = d if sdf is None else np.maximum(sdf, d)
    np.maximum(m[sy, sx], np.clip(0.5 - sdf, 0, 1), out=m[sy, sx])


def chain(m, pts, r0, r1):
    n = len(pts) - 1
    for i in range(n):
        cap(m, pts[i], pts[i + 1], r0 + (r1 - r0) * i / n, r0 + (r1 - r0) * (i + 1) / n)


def sag_line(m, a, b, sag, r, seg=10):
    chain(m, [(a[0] + (b[0] - a[0]) * s / seg, a[1] + (b[1] - a[1]) * s / seg + sag * math.sin(math.pi * s / seg))
              for s in range(seg + 1)], r, r)


def ik(hip, foot, l1, l2, sign):
    dx, dy = foot[0] - hip[0], foot[1] - hip[1]
    d0 = math.hypot(dx, dy)
    ux, uy = (dx / d0, dy / d0) if d0 > 1e-6 else (0.0, 1.0)
    d = min(max(d0, 1e-3), l1 + l2 - 0.01)
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(l1 * l1 - a * a, 0))
    knee = (hip[0] + ux * a - uy * h * sign, hip[1] + uy * a + ux * h * sign)
    return knee, (hip[0] + ux * d, hip[1] + uy * d)


def foot_path(p, amp, lift):
    p %= 1.0
    if p < BETA:
        return amp - 2 * amp * (p / BETA), 0.0
    s = (p - BETA) / (1 - BETA)
    return -amp + 2 * amp * s * s * (3 - 2 * s), lift * math.sin(math.pi * s)


SIZE = {"landscape": (960, 540), "portrait": (540, 960), "square": (720, 720)}


def lerp(a, b, f):
    return a + (b - a) * f


def ease(f):
    f = min(max(f, 0.0), 1.0)
    return f * f * (3 - 2 * f)


def keys(t, pts, easing=False):
    def arr(v):
        a = np.array(v, np.float32)
        return float(a) if a.ndim == 0 else a

    if t <= pts[0][0]:
        return arr(pts[0][1])
    if t >= pts[-1][0]:
        return arr(pts[-1][1])
    for i in range(len(pts) - 1):
        t0, t1 = pts[i][0], pts[i + 1][0]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            if easing:
                f = ease(f)
            a, b = np.array(pts[i][1], np.float32), np.array(pts[i + 1][1], np.float32)
            r = a + (b - a) * f
            return float(r) if r.ndim == 0 else r


class Cam:
    def __init__(self, cx, cy, z=1.0):
        self.cx, self.cy, self.z = cx, cy, z

    def eff(self, f=1.0):
        return 1 + (self.z - 1) * f, W / 2 + (self.cx - W / 2) * f, H / 2 + (self.cy - H / 2) * f

    def pt(self, p, f=1.0):
        z, cx, cy = self.eff(f)
        return (p[0] - cx) * z + W / 2, (p[1] - cy) * z + H / 2

    def r(self, r, f=1.0):
        return r * self.eff(f)[0]

    def grid(self, f=1.0):
        z, cx, cy = self.eff(f)
        return (X - W / 2) / z + cx, (Y - H / 2) / z + cy


def encode(frame, w, h, fps, dur, out):
    if shutil.which("ffmpeg") is None:
        sys.exit("ffmpeg tidak ditemukan. Lihat tutorial.md bagian instalasi.")
    n = int(round(fps * dur))
    p = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
         "-r", str(fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
         "-movflags", "+faststart", str(out)],
        stdin=subprocess.PIPE,
    )
    try:
        for i in range(n):
            f = frame(i / fps)
            if f.shape != (h, w, 3) or f.dtype != np.uint8:
                p.kill()
                sys.exit(f"frame(t) harus mengembalikan uint8 berbentuk ({h}, {w}, 3), dapat {f.dtype} {f.shape}")
            p.stdin.write(f.tobytes())
            if (i + 1) % fps == 0 or i + 1 == n:
                print(f"  {i + 1}/{n} frame", flush=True)
        p.stdin.close()
    except BrokenPipeError:
        pass
    if p.wait() != 0:
        sys.exit("ffmpeg gagal. Periksa pesan error di atas.")
    print(f"Selesai -> {out}")
