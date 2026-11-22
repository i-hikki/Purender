import math

import numpy as np

import kit as k

RED = np.array([206, 17, 38], np.float32)
WHITE = np.array([255, 255, 255], np.float32)
STOPS = [0, 0.45, 0.8, 1.0]

PRESET = {
    "fajar": {
        "sky": [
            (0.0, [(26, 28, 78), (86, 70, 140), (230, 120, 110), (255, 190, 120)]),
            (0.42, [(70, 100, 170), (150, 150, 200), (250, 180, 130), (255, 225, 150)]),
            (0.75, [(70, 140, 220), (130, 185, 240), (200, 225, 250), (255, 240, 200)]),
            (1.0, [(60, 135, 225), (120, 185, 245), (190, 222, 250), (240, 245, 235)]),
        ],
        "sun": [(0.0, (255, 150, 80)), (0.4, (255, 200, 110)), (1.0, (255, 246, 215))],
        "sun_y": [(0.0, 0.90), (0.42, 0.62), (1.0, 0.18)],
        "hill": [(0.0, (30, 32, 62)), (0.42, (96, 84, 110)), (1.0, (96, 140, 120))],
        "ground": [(0.0, (18, 22, 40)), (0.42, (60, 62, 62)), (1.0, (58, 104, 56))],
        "tint": [(0.0, (1.0, 0.82, 0.70)), (0.5, (1.0, 0.96, 0.90)), (1.0, (1.0, 1.0, 1.0))],
    },
}


def backdrop(cam, T, name="fajar", t0=0.0, t1=12.0):
    P = PRESET[name]
    p = float(np.clip((T - t0) / (t1 - t0), 0, 1))
    W, H = k.W, k.H
    yg = 0.92 * H

    z, cx, cy = cam.eff(0.6)
    wy = (k.Y[:, 0] - H / 2) / z + cy
    rel = np.clip((wy - (-1.2 * H)) / (yg + 1.2 * H), 0, 1)
    cols = k.keys(p, P["sky"])
    sky = np.stack([np.interp(rel, STOPS, cols[:, i]) for i in range(3)], axis=1)
    img = np.repeat(sky[:, None, :], W, axis=1).astype(np.float32)

    sx, sy = cam.pt((0.78 * W, k.keys(p, P["sun_y"]) * H), 0.6)
    rs = 0.065 * H * z
    d = np.hypot(k.X - sx, k.Y - sy)
    sc = np.array(k.keys(p, P["sun"]), np.float32)
    img += (0.55 * np.exp(-d / (rs * 2.2)) + 0.28 * np.exp(-d / (rs * 6)))[..., None] * sc * 0.5 * (1 - 0.55 * p)
    disc = np.clip((rs - d) / 1.5 + 0.5, 0, 1)[..., None]
    img = img * (1 - disc) + (sc * 0.4 + 153) * disc

    zh = cam.eff(0.45)[0]
    wxh, wyh = cam.grid(0.45)
    ridge = yg - 0.07 * H - 0.05 * H * np.sin(wxh / W * 6 + 0.5) - 0.03 * H * np.sin(wxh / W * 16 + 2)
    cov = np.clip((wyh - ridge) * zh + 0.5, 0, 1)[..., None]
    img = img * (1 - cov) + np.array(k.keys(p, P["hill"]), np.float32) * cov

    wx, wy2 = cam.grid()
    gline = yg + 0.012 * H * np.sin(wx / W * 14)
    cov = np.clip((wy2 - gline) * cam.eff()[0] + 0.5, 0, 1)[..., None]
    shade = 1 - 0.25 * np.clip((wy2 - yg) / (0.2 * H), 0, 1)[..., None]
    img = img * (1 - cov) + np.array(k.keys(p, P["ground"]), np.float32) * shade * cov

    return img.astype(np.float32), np.array(k.keys(p, P["tint"]), np.float32)


def pole(img, cam, x, y_top, y_bot, r, tint):
    z = cam.eff()[0]
    m = k.mask()
    k.cap(m, cam.pt((x, y_top)), cam.pt((x, y_bot)), r * z)
    k.paint(img, m, np.array((176, 170, 150), np.float32) * tint)
    b = k.mask()
    k.ell(b, cam.pt((x, y_top - 1.8 * r)), 1.9 * r * z, 1.9 * r * z)
    k.paint(img, b, np.array((235, 190, 60), np.float32) * tint)


def flag(img, cam, x0, y0, fw, fh, T, amp, tint):
    z = cam.eff()[0]
    wx, wy = cam.grid()
    u = (wx - x0) / fw
    uj = np.clip(u, 0, 1)
    fase = 2 * np.pi * (1.6 * u - T / 2)
    d = amp * uj * np.sin(fase) + 0.23 * amp * uj * np.sin(2 * np.pi * (0.7 * u - T) + 1.3)
    v = (wy - y0 - d) / fh
    px, pe = 1.2 / (z * fw), 1.2 / (z * fh)
    m = k.sstep(0, px, u) * k.sstep(0, px, 1 - u) * k.sstep(0, pe, v) * k.sstep(0, pe, 1 - v)
    wt = k.sstep(0.5 - pe, 0.5 + pe, v)[..., None]
    col = np.clip((RED * (1 - wt) + WHITE * wt) * (1 + 0.22 * np.cos(fase) * uj)[..., None] * tint, 0, 255)
    img[:] = img * (1 - m[..., None]) + col * m[..., None]


def bird(img, x, y, T, ph, s, d=-1, rgb=(40, 34, 60)):
    m = k.mask()
    k.ell(m, (x, y), 12 * s, 4.2 * s)
    k.cap(m, (x + d * 10 * s, y - 1 * s), (x + d * 22 * s, y - 3.5 * s), 2.6 * s, 1.8 * s)
    k.cap(m, (x + d * 22 * s, y - 3.5 * s), (x + d * 31 * s, y - 2.5 * s), 1.2 * s, 0.5 * s)
    k.cap(m, (x - d * 10 * s, y), (x - d * 20 * s, y + 1 * s), 2.6 * s, 1.4 * s)
    k.cap(m, (x - d * 8 * s, y + 2 * s), (x - d * 28 * s, y + 4.5 * s), 0.9 * s, 0.7 * s)
    for dph, dx in ((0.0, 0), (0.35, -3 * d)):
        flap = math.sin(2 * math.pi * 2.3 * T + ph + dph)
        lag = math.sin(2 * math.pi * 2.3 * T + ph + dph - 0.9)
        sx, sy = x + d * 2 * s + dx * s, y - 2 * s
        e1 = (-d * 0.3, -flap)
        n1 = math.hypot(*e1)
        el = (sx + 20 * s * e1[0] / n1, sy + 20 * s * e1[1] / n1)
        e2 = (-d * 0.55, -lag * 0.9 + 0.15)
        n2 = math.hypot(*e2)
        tip = (el[0] + 22 * s * e2[0] / n2, el[1] + 22 * s * e2[1] / n2)
        k.cap(m, (sx, sy), el, 5 * s, 4 * s)
        k.cap(m, el, tip, 4 * s, 0.8 * s)
    k.paint(img, m, rgb, max(0, int(y - 70 * s)), min(k.H, int(y + 70 * s)))
