# App icons for the GAMEHUB menu and home screens.
# Each icon sits on its own background disc (radius 25) and fits inside it.
from ti_draw import *
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
INK = (20, 20, 20)
RED = (215, 40, 40)
GOLD = (230, 180, 40)

BG = {"GHSOLI": (25, 110, 55), "GHBLOCKS": (40, 30, 90), "GHSUDOKU": WHITE, "GHANIM": WHITE,
      "GHFLAP": (110, 195, 240), "GHTTT": WHITE, "GHMERGE": (187, 173, 160), "GHPONG": (30, 85, 165),
      "GHBREAK": (30, 70, 170), "GHHANG": WHITE}

# 3x5 digits, read row by row
FONT = {"0": "111101101101111", "1": "010110010010111", "2": "111001111100111",
        "3": "111001111001111", "4": "101101111001001", "5": "111100111001111",
        "6": "111100111101111", "7": "111001001001001", "8": "111101111101111",
        "9": "111101111001111"}


def c_(c):
    set_color(c[0], c[1], c[2])


def box(x, y, w, h, c):
    c_(c)
    fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))


def line(x1, y1, x2, y2, c, t=1):
    c_(c)
    for o in range(t):
        draw_line(int(x1) + o, int(y1), int(x2) + o, int(y2))


def hline(x1, x2, y, c, t=1):
    c_(c)
    for o in range(t):
        draw_line(int(x1), int(y) + o, int(x2), int(y) + o)


def circ(x, y, r, c):
    c_(c)
    fill_circle(int(x), int(y), int(r))


def poly(xs, ys, c):
    c_(c)
    fill_poly([int(v) for v in xs], [int(v) for v in ys])


def rr(x, y, w, h, r, c):
    # rounded rectangle
    c_(c)
    fill_rect(x + r, y, w - 2 * r, h)
    fill_rect(x, y + r, w, h - 2 * r)
    for cx in (x + r, x + w - r - 1):
        for cy in (y + r, y + h - r - 1):
            fill_circle(cx, cy, r)


# 5x7 digits for small sharp numbers
FONT7 = {"1": "00100011000010000100001000010001110", "3": "11110000010000101110000010000111110",
         "5": "11111100001111000001000011000101110", "7": "11111000010001000100010000100001000",
         "9": "01110100011000101111000010001001100"}


def digit7(x, y, ch, c):
    c_(c)
    bits = FONT7[ch]
    for r in range(7):
        row = bits[r * 5:r * 5 + 5]
        k = 0
        while k < 5:
            if row[k] == "1":
                e = k
                while e + 1 < 5 and row[e + 1] == "1":
                    e += 1
                draw_line(x + k, y + r, x + e, y + r)
                k = e + 1
            else:
                k += 1


def digits(x, y, s, c, p=2):
    c_(c)
    for i, ch in enumerate(s):
        bits = FONT[ch]
        for n in range(15):
            if bits[n] == "1":
                fill_rect(x + i * 4 * p + (n % 3) * p, y + (n // 3) * p, p, p)


def bevel(x, y, s, c):
    # one block with a light top-left edge and a dark bottom-right edge
    lt = tuple(min(255, v + 70) for v in c)
    dk = tuple(v // 2 for v in c)
    box(x, y, s, s, c)
    hline(x, x + s - 1, y, lt)
    line(x, y, x, y + s - 1, lt)
    hline(x, x + s - 1, y + s - 1, dk)
    line(x + s - 1, y, x + s - 1, y + s - 1, dk)


def ground(x, y, top, c, r=24):
    # the part of the disc below the line y + top
    a = math.asin(top / r)
    xs = []
    ys = []
    for i in range(13):
        t = a + (math.pi - 2 * a) * i / 12
        xs.append(x + r * math.cos(t))
        ys.append(y + r * math.sin(t))
    poly(xs, ys, c)


# ---------- card suits ----------
def heart(x, y, s, c):
    circ(x - s, y - 1, s, c)
    circ(x + s, y - 1, s, c)
    poly([x - 2 * s, x + 2 * s + 1, x], [y, y, y + 2 * s + 1], c)


def diamond(x, y, s, c):
    poly([x, x + s + 1, x, x - s - 1], [y - 2 * s, y, y + 2 * s, y], c)


def spade(x, y, s, c):
    circ(x - s, y + 1, s, c)
    circ(x + s, y + 1, s, c)
    poly([x - 2 * s, x + 2 * s + 1, x], [y + 1, y + 1, y - 2 * s - 1], c)
    poly([x, x - s, x + s], [y + 1, y + 2 * s + 1, y + 2 * s + 1], c)


# ---------- icons ----------
def solitaire(x, y, c):
    suits = ((spade, INK), (diamond, RED), (heart, RED))
    for i in range(3):
        l = x - 18 + i * 10
        t = y - 12
        box(l - 1, t - 1, 18, 26, INK)
        box(l, t, 16, 24, (250, 250, 245))
        f, col = suits[i]
        f(l + 4, t + 5, 2, col)
    heart(x + 10, y + 3, 3, RED)


def blocks(x, y, c):
    s = 8
    cells = ((-2, 1, (220, 70, 70)), (-1, 1, (220, 70, 70)), (0, 1, (70, 110, 220)), (1, 1, (70, 110, 220)),
             (-2, 0, (80, 190, 90)), (0, 0, (70, 110, 220)), (1, 0, (230, 200, 60)),
             (-2, -1, (80, 190, 90)), (1, -1, (230, 200, 60)),
             (-1, -3, (170, 90, 210)), (0, -3, (170, 90, 210)), (0, -2, (170, 90, 210)))
    for cx, cy, col in cells:
        bevel(x + cx * s, y + cy * s + 2, s, col)


def sudoku(x, y, c):
    s = 11
    x0 = x - 16
    y0 = y - 16
    box(x0 + s + 1, y0 + 1, s - 1, s - 1, (250, 225, 140))
    nums = ("53 ", " 7 ", "1 9")
    for r in range(3):
        for k in range(3):
            ch = nums[r][k]
            if ch != " ":
                digit7(x0 + k * s + 3, y0 + r * s + 2, ch, INK if (r, k) != (1, 1) else (40, 90, 200))
    for i in (1, 2):
        line(x0 + i * s, y0, x0 + i * s, y0 + 3 * s, INK)
        hline(x0, x0 + 3 * s, y0 + i * s, INK)
    c_(INK)
    for o in (0, 1):
        draw_rect(x0 - o, y0 - o, 3 * s + 2 * o, 3 * s + 2 * o)


def anim(x, y, c):
    box(x - 20, y - 13, 41, 27, (35, 35, 40))
    for i in range(5):
        box(x - 18 + i * 8, y - 11, 4, 3, WHITE)
        box(x - 18 + i * 8, y + 9, 4, 3, WHITE)
    for i, by in enumerate((4, -2, 2)):
        fx = x - 17 + i * 12
        box(fx, y - 6, 11, 13, (120, 200, 240))
        box(fx, y + 4, 11, 3, (70, 170, 80))
        circ(fx + 5, y + by, 2, (240, 120, 40))
    circ(x + 17, y - 9, 1, RED)


def flap(x, y, c):
    box(x - 14, y - 16, 10, 4, WHITE)
    circ(x - 12, y - 15, 3, WHITE)
    circ(x - 7, y - 17, 4, WHITE)
    ground(x, y, 15, (70, 170, 80))
    box(x + 14, y + 4, 4, 12, (120, 80, 40))
    circ(x + 16, y + 1, 6, (50, 140, 60))
    circ(x - 2, y - 1, 11, (170, 120, 20))
    circ(x - 2, y - 1, 10, (250, 215, 50))
    poly([x - 14, x - 2, x - 6], [y - 1, y + 1, y + 8], (255, 245, 190))
    circ(x + 3, y - 5, 4, WHITE)
    circ(x + 4, y - 5, 2, BLACK)
    poly([x + 7, x + 17, x + 7], [y - 2, y + 1, y + 2], (245, 140, 30))
    poly([x + 7, x + 15, x + 7], [y + 2, y + 3, y + 5], (200, 100, 20))


def ttt(x, y, c):
    s = 12
    for i in (-1, 1):
        box(x + i * 6 - 1, y - 18, 2, 36, INK)
        box(x - 18, y + i * 6 - 1, 36, 2, INK)
    for i in (-1, 0, 1):
        cx = x + i * s
        cy = y + i * s
        line(cx - 4, cy - 4, cx + 3, cy + 3, INK, 2)
        line(cx + 3, cy - 4, cx - 4, cy + 3, INK, 2)


def g2048(x, y, c):
    rr(x - 20, y - 12, 41, 28, 4, (200, 160, 30))
    rr(x - 20, y - 14, 41, 28, 4, (237, 194, 46))
    digits(x - 14, y - 5, "2048", WHITE)


def pong(x, y, c):
    c_(WHITE)
    draw_rect(x - 21, y - 15, 43, 31)
    hline(x - 21, x + 21, y, (200, 210, 230))
    for i in range(6):
        box(x, y - 15 + i * 6, 2, 3, WHITE)
    box(x - 17, y - 11, 4, 14, WHITE)
    box(x + 14, y - 3, 4, 14, WHITE)
    circ(x - 6, y - 5, 2, (250, 150, 40))


def breakout(x, y, c):
    cols = ((220, 60, 60), (235, 140, 50), (230, 210, 60), (70, 190, 90))
    for r in range(3):
        for i in range(4):
            bx = x - 19 + i * 10
            box(bx, y - 15 + r * 6, 9, 5, cols[(i + r) % 4])
            hline(bx, bx + 8, y - 15 + r * 6, tuple(min(255, v + 60) for v in cols[(i + r) % 4]))
    for i, (dx, dy) in enumerate(((-8, 12), (-5, 8))):
        box(x + dx, y + dy, 2, 2, (120, 150, 230))
    circ(x - 1, y + 5, 2, WHITE)
    rr(x - 11, y + 13, 22, 4, 1, WHITE)


def rpg(x, y, c):
    # hero
    circ(x - 5, y - 8, 6, (240, 200, 160))
    box(x - 11, y - 15, 13, 5, (110, 70, 30))
    box(x - 11, y - 11, 3, 5, (110, 70, 30))
    box(x - 8, y - 9, 2, 2, BLACK)
    box(x - 3, y - 9, 2, 2, BLACK)
    box(x - 11, y - 1, 13, 12, (60, 120, 230))
    box(x - 11, y + 5, 13, 2, (110, 70, 30))
    box(x - 14, y, 3, 8, (240, 200, 160))
    box(x - 10, y + 11, 4, 6, (60, 40, 30))
    box(x - 4, y + 11, 4, 6, (60, 40, 30))
    box(x + 2, y + 1, 4, 3, (240, 200, 160))
    # glowing sword
    box(x + 2, y - 23, 12, 26, (15, 45, 70))
    box(x + 4, y - 22, 8, 24, (40, 110, 170))
    box(x + 5, y - 21, 6, 22, (100, 200, 245))
    box(x + 7, y - 21, 2, 21, (240, 252, 255))
    box(x + 3, y + 1, 10, 2, GOLD)
    box(x + 7, y + 3, 2, 5, (120, 80, 40))
    for sx, sy in ((x + 16, y - 18), (x + 1, y - 14), (x + 15, y - 6)):
        box(sx, sy, 2, 2, (200, 240, 255))


def simon(x, y, c):
    r = 18
    cols = ((40, 170, 60), (200, 40, 40), (40, 80, 200), (220, 180, 30))
    for q in range(4):
        a0 = -math.pi / 2 + q * math.pi / 2
        xs = [x]
        ys = [y]
        for i in range(6):
            a = a0 + (math.pi / 2) * i / 5
            xs.append(x + r * math.cos(a))
            ys.append(y + r * math.sin(a))
        poly(xs, ys, cols[q])
    circ(x, y, 5, BLACK)
    box(x - 1, y - r, 2, 2 * r, BLACK)
    box(x - r, y - 1, 2 * r, 2, BLACK)


def hangman(x, y, c):
    box(x - 19, y + 15, 24, 3, INK)
    box(x - 13, y - 18, 3, 34, INK)
    box(x - 13, y - 18, 24, 3, INK)
    line(x - 11, y - 9, x - 3, y - 17, INK, 2)
    box(x + 8, y - 16, 2, 6, (140, 90, 40))
    circ(x + 9, y - 6, 4, INK)
    circ(x + 9, y - 6, 2, WHITE)
    line(x + 9, y - 2, x + 9, y + 7, INK, 2)
    line(x + 9, y + 1, x + 4, y + 5, INK)
    line(x + 10, y + 1, x + 15, y + 5, INK)
    line(x + 9, y + 7, x + 5, y + 13, INK)
    line(x + 10, y + 7, x + 14, y + 13, INK)


def crypt(x, y, c):
    # Ysolde: a static woman, small head tilted hard on a long neck,
    # lank hair, gaunt face, small cold blue eyes, jaw hanging open.
    random.seed(7)
    hx = x + 3
    hy = y - 7
    ca = math.cos(0.55)
    sa = math.sin(0.55)

    def rot(px, py):
        return hx + px * ca - py * sa, hy + px * sa + py * ca

    def shape(pts, col):
        xs = []
        ys = []
        for px, py in pts:
            a, b = rot(px, py)
            xs.append(a)
            ys.append(b)
        poly(xs, ys, col)

    def oval(px, py, rx, ry, col, n=14):
        shape([(px + rx * math.cos(2 * math.pi * i / n), py + ry * math.sin(2 * math.pi * i / n)) for i in range(n)], col)

    # hair hanging behind
    shape([(-9, -4), (-14, 12), (-12, 24), (-4, 18), (3, 25), (9, 15), (9, -4), (0, -12)], (25, 22, 30))
    # neck and narrow sloped shoulders
    nx, ny = rot(0, 11)
    poly([nx - 3, nx + 3, x + 2, x - 4], [ny, ny, y + 16, y + 16], (150, 150, 155))
    poly([x - 13, x - 2, x + 11, x + 7, x - 9], [y + 22, y + 14, y + 20, y + 23, y + 23], (150, 150, 155))
    # head
    oval(0, 0, 8.5, 12.5, (200, 200, 205))
    # static
    for i in range(70):
        px = random.uniform(-8, 8)
        py = random.uniform(-12, 12)
        if (px / 8.5) ** 2 + (py / 12.5) ** 2 < 1:
            g = random.randint(110, 255)
            a, b = rot(px, py)
            box(a, b, 2, 2, (g, g, g))
    for i in range(16):
        g = random.randint(60, 200)
        box(x + random.randint(-14, 8), y + random.randint(-2, 20), 2, 2, (g, g, g))
    # glitch band
    a, b = rot(0, -6)
    box(a - 6, b, 14, 2, (235, 235, 240))
    # face
    for s in (-1, 1):
        oval(s * 3.5, -3, 2.4, 2.8, (10, 10, 15), 8)
        ex, ey = rot(s * 3.5, -3)
        circ(ex, ey, 1, (40, 110, 220))
        box(ex, ey, 2, 2, (150, 225, 255))
        t0 = rot(s * 3.5, 1)
        t1 = rot(s * 4, 6)
        line(t0[0], t0[1], t1[0], t1[1], (10, 10, 15))
    oval(0, 7, 2, 4, (15, 5, 5), 10)
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


def bg(mod):
    return BG.get(mod, BLACK)


def draw(mod, x, y, c):
    f = ICONS.get(mod)
    if f:
        f(x, y, c)
