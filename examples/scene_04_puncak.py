import numpy as np

import kit as k
import props

SKALA = "landscape"
W, H = k.SIZE[SKALA]
FPS, T0, DUR = 30, 9, 3
k.init(W, H)

FH = 0.5 * min(W / 1.5, H)
FW = 1.5 * FH
X0 = (W - FW) / 2
GROUND = 0.92 * H
POLE_TOP = -0.60 * H
Y_LOW = GROUND - FH - 0.02 * H
Y_HIGH = POLE_TOP + 0.05 * H


def flag_y(T):
    return k.keys(T, [(0, Y_LOW), (9, Y_HIGH)], easing=True)


def fc(T):
    return flag_y(T) + FH / 2


BIRDS = [(0.0, 0.22, 1.0), (0.5, 0.15, 0.82), (0.95, 0.29, 0.7)]


def cam(T):
    cy = k.keys(T, [(9, fc(9)), (12, fc(9) + 0.14 * H)], easing=True)
    return k.Cam(W / 2, cy, k.keys(T, [(9, 1.15), (12, 1.0)], easing=True))


def frame(t):
    T = T0 + t
    c = cam(T)
    img, tint = props.backdrop(c, T, "fajar", 0, 12)
    props.pole(img, c, X0 - 0.016 * H, POLE_TOP, GROUND, 0.011 * H, tint)
    props.flag(img, c, X0, flag_y(T), FW, FH, T, 0.075 * FH, tint)
    for i, (dt, fy, s) in enumerate(BIRDS):
        x = W + 70 - 0.38 * W * (T - 9 - dt)
        if x < W + 80:
            props.bird(img, x, H * fy + 0.012 * H * np.sin(0.9 * T + i), T, i * 1.3, s * H / 540)
    return np.clip(img, 0, 255).astype(np.uint8)
