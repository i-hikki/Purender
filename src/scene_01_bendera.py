import numpy as np

import kit as k

W, H, FPS, DUR = 960, 540, 30, 2
k.init(W, H)

FX0, FY0, FW, FH = 250, 130, 520, 347
RED = np.array([206, 17, 38], np.float32)
WHITE = np.array([255, 255, 255], np.float32)
SKY = k.vgrad([0, H], [(120, 185, 235), (220, 238, 250)])

POLE = k.mask()
k.cap(POLE, (242, 108), (242, H + 10), 6)
BALL = k.mask()
k.ell(BALL, (242, 98), 11, 11)


def frame(t):
    img = SKY.copy()
    u = (k.X - FX0) / FW
    uj = np.clip(u, 0, 1)
    fase = 2 * np.pi * (1.6 * u - t / DUR)
    d = 26 * uj * np.sin(fase) + 6 * uj * np.sin(2 * np.pi * (0.7 * u - 2 * t / DUR) + 1.3)
    v = (k.Y - FY0 - d) / FH
    px, pe = 1.2 / FW, 1.2 / FH

    shadow = k.sstep(0, 0.04, u - 0.015) * k.sstep(0, 0.04, 1.015 - u) * k.sstep(0, 0.02, v + 0.02) * k.sstep(0, 0.02, 1.04 - v)
    img *= (1 - 0.10 * shadow)[..., None]

    m = k.sstep(0, px, u) * k.sstep(0, px, 1 - u) * k.sstep(0, pe, v) * k.sstep(0, pe, 1 - v)
    white = k.sstep(0.5 - pe, 0.5 + pe, v)[..., None]
    col = np.clip((RED * (1 - white) + WHITE * white) * (1 + 0.22 * np.cos(fase) * uj)[..., None], 0, 255)
    img = img * (1 - m[..., None]) + col * m[..., None]

    k.paint(img, POLE, (176, 170, 150))
    k.paint(img, BALL, (235, 190, 60))
    return np.clip(img, 0, 255).astype(np.uint8)
