# App icons for the GAMEHUB menu and home screens.
# Each icon sits on its own background disc (radius 25) and fits inside it.
from ti_draw import *
from GHLIB import col
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
INK = (20, 20, 20)
RED = (215, 40, 40)
GOLD = (230, 180, 40)

BG = {"GHSOLI": (25, 110, 55), "GHBLOCKS": (40, 30, 90), "GHSUDOKU": WHITE, "GHANIM": WHITE,
      "GHFLAP": (110, 195, 240), "GHTTT": WHITE, "GHMERGE": (187, 173, 160), "GHPONG": (30, 85, 165),
      "GHBREAK": (30, 70, 170), "GHHANG": WHITE, "GHSPACE": (15, 20, 50), "GHFORTUN": (55, 25, 85)}

# 3x5 digits, read row by row
FONT = {"0": "111101101101111", "1": "010110010010111", "2": "111001111100111",
        "3": "111001111001111", "4": "101101111001001", "5": "111100111001111",
        "6": "111100111101111", "7": "111001001001001", "8": "111101111101111",
        "9": "111101111001111"}


def c_(c):
    # GHLIB's col remembers the colour, so it stays right after an icon
    col(c)


def box(x, y, w, h, c):
    c_(c)
    fill_rect(int(x) - 1, int(y) - 1, max(1, int(w)) + 1, max(1, int(h)) + 1)


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
    fill_rect(x + r - 1, y - 1, w - 2 * r + 1, h + 1)
    fill_rect(x - 1, y + r - 1, w + 1, h - 2 * r + 1)
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
                fill_rect(x + i * 4 * p + (n % 3) * p - 1, y + (n // 3) * p - 1, p + 1, p + 1)


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
        draw_rect(x0 - o - 1, y0 - o - 1, 3 * s + 2 * o + 1, 3 * s + 2 * o + 1)


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
    draw_rect(x - 22, y - 16, 44, 32)
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
    # Ysolde as she looks in the full game: a thin dark shape full of faint
    # static, outlined in bright static, with two small cold blue eyes.
    # Same shape as her character sheet (256 x 640), head and shoulders only.
    # a fixed pattern of static, so the icon looks the same every time
    rs = [7]

    def rnd(a, b):
        rs[0] = (rs[0] * 1103515245 + 12345) % 2147483648
        return a + rs[0] % (b - a + 1)
    k = 0.21
    ox = x + 3
    oy = y - 17
    ca = math.cos(0.55)
    sa = math.sin(0.55)

    def m(cx, cy):
        return ox + (cx - 140) * k, oy + (cy - 50) * k

    def head(lx, ly):
        return m(140 + lx * ca - ly * sa, 50 + lx * sa + ly * ca)

    def band(pts, w):
        # a thick line through canvas points, as a polygon
        left = []
        right = []
        for i in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) or 1
            nx = -(y2 - y1) / d * w / 2
            ny = (x2 - x1) / d * w / 2
            left += [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny)]
            right += [(x1 - nx, y1 - ny), (x2 - nx, y2 - ny)]
        return [m(px, py) for px, py in left + right[::-1]]

    shapes = [
        [head(17 * math.cos(t * math.pi / 8), 25 * math.sin(t * math.pi / 8)) for t in range(16)],
        [head(px, py) for px, py in ((-18, -6), (-27, 30), (-24, 96), (-6, 70), (8, 100), (20, 60), (17, -6), (10, -24), (-10, -24))],
        band(((128, 125), (132, 88), (140, 66)), 11),
        [m(px, py) for px, py in ((98, 122), (128, 112), (160, 126), (150, 210), (148, 250), (108, 250), (106, 210))],
        band(((100, 128), (84, 250), (90, 260)), 7),
        band(((158, 128), (176, 248), (170, 258)), 7),
    ]

    def spans(pts):
        out = []
        ys = [p[1] for p in pts]
        n = len(pts)
        for row in range(int(min(ys)), int(max(ys)) + 1):
            yc = row + .5
            xs = []
            for i in range(n):
                (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
                if (y1 <= yc < y2) or (y2 <= yc < y1):
                    xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
            if len(xs) >= 2:
                out.append((row, int(min(xs) + .5), int(max(xs) + .5)))
        return out

    all_spans = [spans(sh) for sh in shapes]
    # bright static outline: everything bright first, then the dark inside
    for sp in all_spans:
        for row, a, b in sp:
            g = rnd(190, 255)
            hline(a, max(a, b - 1), row, (g, g * 19 // 20, g * 9 // 10))
    for sp in all_spans:
        for row, a, b in sp[1:-1]:
            if b - a > 2:
                g = rnd(28, 62)
                hline(a + 1, b - 2, row, (g, g, g + 8))
    # glowing blue eyes high in the head, like Ivy's video
    pts = []
    for ex, ey in ((137.2, 41.2), (149.1, 48.55)):
        a, b = m(ex, ey)
        pts.append((int(a), int(b)))
    for a, b in pts:
        hline(a - 1, a + 1, b - 1, (35, 80, 150))
        hline(a - 2, a + 2, b, (35, 80, 150))
        hline(a - 1, a + 1, b + 1, (35, 80, 150))
    for a, b in pts:
        hline(a - 1, a + 1, b, (80, 175, 245))
        line(a, b - 1, a, b + 1, (80, 175, 245))
    for a, b in pts:
        hline(a, a, b, (230, 250, 255))


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


def space(x, y, c):
    # an escape pod flying past a few stars
    for sx, sy in ((-15, -12), (12, -16), (16, 8), (-17, 10), (2, 17)):
        box(x + sx, y + sy, 2, 2, (255, 240, 180))
    poly([x - 4, x + 4, x + 8, x - 8], [y - 14, y - 14, y + 6, y + 6], (220, 225, 235))
    box(x - 3, y - 7, 6, 5, (90, 170, 230))
    poly([x - 8, x - 13, x - 8], [y - 2, y + 8, y + 6], (215, 40, 40))
    poly([x + 8, x + 13, x + 8], [y - 2, y + 8, y + 6], (215, 40, 40))
    poly([x - 5, x + 5, x], [y + 7, y + 7, y + 15], (250, 170, 40))


def fortune(x, y, c):
    # three cards fanned out, the middle one face up with a gold star
    box(x - 19, y - 10, 13, 20, (120, 40, 140))
    box(x + 6, y - 10, 13, 20, (120, 40, 140))
    box(x - 8, y - 15, 16, 25, (250, 240, 215))
    poly([x, x + 2, x + 6, x + 3, x + 4, x, x - 4, x - 3, x - 6, x - 2],
         [y - 9, y - 4, y - 4, y - 1, y + 4, y + 1, y + 4, y - 1, y - 4, y - 4], GOLD)


def about(x, y, c):
    c_(c)
    fill_circle(x, y - 10, 3)
    fill_rect(x - 3, y - 5, 6, 19)


ICONS = {"GHSOLI": solitaire, "GHBLOCKS": blocks, "GHSUDOKU": sudoku, "GHANIM": anim,
         "GHFLAP": flap, "GHTTT": ttt, "GHMERGE": g2048, "GHPONG": pong, "GHBREAK": breakout,
         "GHRPG": rpg, "GHSIMON": simon, "GHHANG": hangman, "GHCRYPT": crypt, "GHSPACE": space, "GHFORTUN": fortune,
         "*keys": keys, "*wipe": wipe, "*about": about}


def bg(mod):
    return BG.get(mod, BLACK)


def draw(mod, x, y, c):
    f = ICONS.get(mod)
    if f:
        f(x, y, c)
