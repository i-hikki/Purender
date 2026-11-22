import numpy as np

import kit as k
import props

SKALA = "landscape"
W, H = k.SIZE[SKALA]
FPS, T0, DUR = 30, 5, 4
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


def cam(T):
    return k.Cam(W / 2, fc(T), k.keys(T, [(5, 1.8), (9, 1.15)], easing=True))


def frame(t):
    T = T0 + t
    c = cam(T)
    img, tint = props.backdrop(c, T, "fajar", 0, 12)
    props.pole(img, c, X0 - 0.016 * H, POLE_TOP, GROUND, 0.011 * H, tint)
    props.flag(img, c, X0, flag_y(T), FW, FH, T, 0.075 * FH, tint)
    return np.clip(img, 0, 255).astype(np.uint8)
