# App icons for the GAMEHUB menu and home screens. Each fits in a circle of radius ~24.
from ti_draw import *
import random


def c_(c):
    set_color(c[0], c[1], c[2])


def box(x, y, w, h, c):
    c_(c)
    fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))


def line(x1, y1, x2, y2, c, t=1):
    c_(c)
    for o in range(t):
        draw_line(int(x1) + o, int(y1), int(x2) + o, int(y2))


def arc_pts(x, y, r, a0, a1, n=5):
    import math
    xs = [x]
    ys = [y]
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        xs.append(int(x + r * math.cos(a)))
        ys.append(int(y + r * math.sin(a)))
    return xs, ys


def solitaire(x, y, c):
    for i, dx in ((0, -12), (1, -4), (2, 4)):
        box(x + dx - 1, y - 14 + i * 2 - 1, 18, 26, (20, 20, 20))
        box(x + dx, y - 14 + i * 2, 16, 24, (245, 245, 240))
    c_((220, 50, 50))
    fill_circle(x + 9, y - 3, 3)
    fill_circle(x + 14, y - 3, 3)
    fill_poly([x + 6, x + 17, x + 11], [y - 2, y - 2, y + 4])


def blocks(x, y, c):
    s = 8
    cells = ((-2, 1, (220, 70, 70)), (-1, 1, (220, 70, 70)), (0, 1, (70, 110, 220)), (1, 1, (70, 110, 220)),
             (-2, 0, (80, 190, 90)), (0, 0, (70, 110, 220)), (1, 0, (230, 200, 60)),
             (-2, -1, (80, 190, 90)), (1, -1, (230, 200, 60)), (0, -2, (170, 90, 210)), (1, -2, (230, 200, 60)))
    for cx, cy, col in cells:
        box(x + cx * s, y + cy * s, s - 1, s - 1, col)


def sudoku(x, y, c):
    for i in range(4):
        t = 2 if i in (0, 3) else 1
        line(x - 15 + i * 10, y - 15, x - 15 + i * 10, y + 15, c, t)
        line(x - 15, y - 15 + i * 10, x + 15, y - 15 + i * 10, c, 1)
        if t == 2:
            line(x - 15, y - 14 + i * 10, x + 15, y - 14 + i * 10, c, 1)
    box(x - 12, y - 12, 4, 5, (230, 180, 40))
    box(x + 8, y + 8, 4, 5, (230, 180, 40))
    box(x - 2, y - 2, 4, 5, (255, 255, 255))


def anim(x, y, c):
    box(x - 20, y - 13, 40, 26, (35, 35, 40))
    for i in range(5):
        box(x - 18 + i * 8, y - 11, 4, 3, (240, 240, 240))
        box(x - 18 + i * 8, y + 8, 4, 3, (240, 240, 240))
    box(x - 16, y - 6, 14, 12, (80, 200, 230))
    box(x + 2, y - 6, 14, 12, (245, 140, 30))
    c_((250, 220, 50))
    fill_circle(x - 9, y, 3)
    fill_circle(x + 11, y - 1, 3)


def flap(x, y, c):
    c_((240, 220, 60))
    fill_circle(x - 2, y, 11)
    c_((255, 255, 255))
    fill_circle(x + 3, y - 4, 4)
    c_((0, 0, 0))
    fill_circle(x + 4, y - 4, 2)
    box(x + 8, y, 9, 4, (240, 140, 40))
    c_((255, 250, 220))
    fill_poly([x - 14, x - 2, x - 6], [y - 2, y + 1, y + 8])


def ttt(x, y, c):
    for i in (-1, 0, 1):
        cx = x + i * 12
        cy = y + i * 12
        line(cx - 4, cy - 4, cx + 4, cy + 4, c, 2)
        line(cx + 4, cy - 4, cx - 4, cy + 4, c, 2)


def g2048(x, y, c):
    c_((235, 185, 30))
    fill_rect(x - 22, y - 13, 44, 26)
    c_((255, 255, 255))
    draw_text(x - 20, y + 7, "2048")


def pong(x, y, c):
    box(x - 18, y - 12, 4, 16, (255, 255, 255))
    box(x + 14, y - 4, 4, 16, (230, 180, 40))
    box(x - 3, y - 4, 5, 5, (255, 255, 255))
    for i in range(4):
        box(x, y - 16 + i * 9, 2, 4, (90, 90, 90))


def breakout(x, y, c):
    cols = ((220, 60, 60), (235, 140, 50), (230, 210, 60), (70, 190, 90))
    for r in range(2):
        for i in range(4):
            box(x - 19 + i * 10, y - 12 + r * 6, 9, 5, cols[(i + r) % 4])
    box(x - 2, y + 4, 4, 4, (230, 180, 40))
    box(x - 9, y + 13, 18, 3, (255, 255, 255))


def rpg(x, y, c):
    c_((240, 200, 160))
    fill_circle(x, y - 9, 6)
    box(x - 6, y - 9, 12, 3, (110, 70, 30))
    box(x - 7, y - 2, 14, 12, (60, 120, 230))
    box(x - 7, y + 10, 5, 7, (60, 40, 30))
    box(x + 2, y + 10, 5, 7, (60, 40, 30))
    box(x + 10, y - 12, 2, 20, (210, 210, 220))
    box(x + 7, y + 2, 8, 2, (150, 110, 50))


def simon(x, y, c):
    import math
    r = 18
    cols = ((40, 170, 60), (200, 40, 40), (40, 80, 200), (220, 180, 30))
    for q in range(4):
        xs, ys = arc_pts(x, y, r, -math.pi / 2 + q * math.pi / 2, q * math.pi / 2)
        c_(cols[q])
        fill_poly(xs, ys)
    c_((0, 0, 0))
    fill_circle(x, y, 5)
    fill_rect(x - 1, y - r, 2, 2 * r)
    fill_rect(x - r, y - 1, 2 * r, 2)


def hangman(x, y, c):
    line(x - 16, y + 16, x + 4, y + 16, c, 2)
    line(x - 10, y - 16, x - 10, y + 16, c, 2)
    line(x - 10, y - 16, x + 8, y - 16, c, 2)
    line(x + 8, y - 16, x + 8, y - 10, c, 1)
    c_((230, 180, 40))
    draw_circle(x + 8, y - 6, 4)
    line(x + 8, y - 2, x + 8, y + 8, (230, 180, 40))
    line(x + 8, y + 1, x + 3, y + 5, (230, 180, 40))
    line(x + 8, y + 1, x + 13, y + 5, (230, 180, 40))


def crypt(x, y, c):
    random.seed(7)
    for i in range(12):
        w = int(22 - abs(i - 6) * 2.4)
        g = random.randint(110, 230)
        box(x - w // 2, y - 18 + i * 3, w, 3, (g, g, g))
    box(x - 7, y - 6, 4, 3, (10, 10, 10))
    box(x + 3, y - 6, 4, 3, (10, 10, 10))
    box(x - 3, y + 6, 6, 2, (40, 40, 40))
    random.seed()


def keys(x, y, c):
    for i in range(3):
        for j in range(3):
            box(x - 14 + j * 10, y - 12 + i * 9, 8, 7, c)


def wipe(x, y, c):
    box(x - 10, y - 8, 20, 22, c)
    box(x - 13, y - 13, 26, 3, c)
    box(x - 4, y - 16, 8, 3, c)
    for i in (-5, 0, 5):
        box(x + i - 1, y - 4, 2, 15, (0, 0, 0))


def about(x, y, c):
    c_(c)
    fill_circle(x, y - 10, 3)
    fill_rect(x - 2, y - 4, 5, 18)


ICONS = {"GHSOLI": solitaire, "GHBLOCKS": blocks, "GHSUDOKU": sudoku, "GHANIM": anim,
         "GHFLAP": flap, "GHTTT": ttt, "GHMERGE": g2048, "GHPONG": pong, "GHBREAK": breakout,
         "GHRPG": rpg, "GHSIMON": simon, "GHHANG": hangman, "GHCRYPT": crypt,
         "*keys": keys, "*wipe": wipe, "*about": about}


def draw(mod, x, y, c):
    f = ICONS.get(mod)
    if f:
        f(x, y, c)
