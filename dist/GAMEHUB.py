# GAMEHUB - game center for the TI-84 Evo. One file: run it.
from ti_draw import *
from ti_system import *
import time
import random
import math
from ti_system import store_list, recall_list
import sys
import gc
UP = 25
DOWN = 34
LEFT = 24
RIGHT = 26
OK = 105
CLR = 45
DEL = 23
SECOND = 21
NUMS = {102: 0, 92: 1, 93: 2, 94: 3, 82: 4, 83: 5, 84: 6, 72: 7, 73: 8, 74: 9}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (230, 180, 40)
GREY = (110, 110, 110)
DARK = (40, 40, 40)
RED = (220, 50, 50)
GREEN = (50, 190, 80)
BLUE = (60, 120, 230)
YELLOW = (240, 220, 60)
W = 320
H = 210
def key():
    return get_key(0)
class Steer:

    def __init__(self, keys, stop_on_back=False):
        self.keys = keys
        self.back = stop_on_back
        self.d = 0

    def feed(self, k):
        if k in self.keys:
            if self.back and self.d and (k != self.d) and (self.keys.index(k) // 2 == self.keys.index(self.d) // 2):
                self.d = 0
            else:
                self.d = k
        elif k:
            self.d = 0
        return self.d

    def stop(self):
        self.d = 0
def wkey():
    return wait_key()
def col(c):
    set_color(c[0], c[1], c[2])
def rect(x, y, w, h, c):
    if w < 2 or h < 2:
        if w < 1 or h < 1:
            return
        col(c)
        draw_line(x, y, x + w - 1, y + h - 1)
        return
    col(c)
    fill_rect(x, y, w, h)
def cls(c=BLACK):
    col(c)
    fill_rect(-1, -1, 322, 212)
def text(x, y, s, c=WHITE):
    col(c)
    draw_text(x, y, s)
def ctext(y, s, c=WHITE, cx=160):
    col(c)
    draw_text(cx - len(s) * 5, y, s)
def circ(x, y, r, c):
    col(c)
    fill_circle(x, y, r)
def lt(c, k=0.35):
    return (int(c[0] + (255 - c[0]) * k), int(c[1] + (255 - c[1]) * k), int(c[2] + (255 - c[2]) * k))
def dk(c, k=0.65):
    return (int(c[0] * k), int(c[1] * k), int(c[2] * k))
def block(x, y, w, h, c, e=2):
    rect(x, y, w, h, c)
    rect(x, y, w, e, lt(c))
    rect(x, y, e, h, lt(c))
    rect(x, y + h - e, w, e, dk(c))
    rect(x + w - e, y + e, e, h - e, dk(c))
def ball(x, y, r, c):
    circ(x, y, r, c)
    s = max(1, r // 3)
    circ(x - s, y - s, s, lt(c, 0.6))
def ring(x, y, r, c, t=2, inner=BLACK):
    col(c)
    fill_circle(x, y, r)
    col(inner)
    fill_circle(x, y, r - t)
def rrect(x, y, w, h, r, c):
    col(c)
    fill_rect(x + r, y, w - 2 * r, h)
    fill_rect(x, y + r, w, h - 2 * r)
    fill_circle(x + r, y + r, r)
    fill_circle(x + w - r - 1, y + r, r)
    fill_circle(x + r, y + h - r - 1, r)
    fill_circle(x + w - r - 1, y + h - r - 1, r)
def rbox(x, y, w, h, r, c, t=2, inner=BLACK):
    rrect(x, y, w, h, r, c)
    rrect(x + t, y + t, w - 2 * t, h - 2 * t, max(r - t, 2), inner)
def pause(s):
    time.sleep(s)
def message(lines, title=None):
    n = len(lines) + (1 if title else 0)
    h = n * 18 + 30
    y = (H - h) // 2
    rbox(20, y, 280, h, 8, WHITE)
    yy = y + 24
    if title:
        ctext(yy, title, GOLD)
        yy += 18
    for s in lines:
        ctext(yy, s)
        yy += 18
    while True:
        k = wkey()
        if k in (OK, CLR):
            return k
def choose(title, opts, sel=0):
    cls()
    ctext(24, title, GOLD)
    n = len(opts)
    while True:
        for i in range(n):
            y = 40 + i * 30
            c = GOLD if i == sel else WHITE
            rbox(60, y, 200, 24, 8, c)
            ctext(y + 18, opts[i], c)
        k = wkey()
        if k == UP:
            sel = (sel - 1) % n
        elif k == DOWN:
            sel = (sel + 1) % n
        elif k == OK:
            return sel
        elif k == CLR:
            return -1
def _wrap(s, n=30):
    out = []
    line = ''
    for w in s.split(' '):
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = (line + ' ' + w).strip()
    if line:
        out.append(line)
    return out
def how_to(title, rules, buttons):
    cls()
    ctext(20, 'HOW TO PLAY', GOLD)
    ctext(38, title, GREY)
    y = 60
    for ln in _wrap(rules):
        text(8, y, ln)
        y += 16
    y += 6
    text(8, y, 'BUTTONS', GOLD)
    y += 17
    for b in buttons:
        text(8, y, b)
        y += 16
    text(8, 206, 'ENTER: back', GREY)
    while wkey() not in (OK, CLR, UP, DOWN):
        pass
def home(mod, title, rules, buttons, opts=('Play', 'Back'), sel=0):
    n = len(opts)
    while True:
        cls()
        ring(160, 58, 36, GOLD, 3)
        try:
            circ(160, 58, 33, icons_bg(mod))
            icons_draw(mod, 160, 58, WHITE)
        except Exception:
            pass
        ctext(122, title, GOLD)
        ctext(146, 'Up/Down: how to play', GREY)
        bw = (300 - (n - 1) * 8) // n
        while True:
            for i in range(n):
                x = 10 + i * (bw + 8)
                c = GOLD if i == sel else WHITE
                rect(x, 166, bw, 28, BLACK)
                rbox(x, 166, bw, 28, 10, c)
                text(x + bw // 2 - len(opts[i]) * 5, 186, opts[i], c)
            k = wkey()
            if k == LEFT:
                sel = (sel - 1) % n
            elif k == RIGHT:
                sel = (sel + 1) % n
            elif k in (UP, DOWN):
                how_to(title, rules, buttons)
                break
            elif k == CLR:
                return -1
            elif k == OK:
                if opts[sel] == 'Back':
                    return -1
                return sel
icons_BLACK = (0, 0, 0)
icons_WHITE = (255, 255, 255)
icons_INK = (20, 20, 20)
icons_RED = (215, 40, 40)
icons_GOLD = (230, 180, 40)
icons_BG = {'GHSOLI': (25, 110, 55), 'GHBLOCKS': (40, 30, 90), 'GHSUDOKU': icons_WHITE, 'GHANIM': icons_WHITE, 'GHFLAP': (110, 195, 240), 'GHTTT': icons_WHITE, 'GHMERGE': (187, 173, 160), 'GHPONG': (30, 85, 165), 'GHBREAK': (30, 70, 170), 'GHHANG': icons_WHITE}
icons_FONT = {'0': '111101101101111', '1': '010110010010111', '2': '111001111100111', '3': '111001111001111', '4': '101101111001001', '5': '111100111001111', '6': '111100111101111', '7': '111001001001001', '8': '111101111101111', '9': '111101111001111'}
def icons_c_(c):
    set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
    icons_c_(c)
    fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))
def icons_line(x1, y1, x2, y2, c, t=1):
    icons_c_(c)
    for o in range(t):
        draw_line(int(x1) + o, int(y1), int(x2) + o, int(y2))
def icons_hline(x1, x2, y, c, t=1):
    icons_c_(c)
    for o in range(t):
        draw_line(int(x1), int(y) + o, int(x2), int(y) + o)
def icons_circ(x, y, r, c):
    icons_c_(c)
    fill_circle(int(x), int(y), int(r))
def icons_poly(xs, ys, c):
    icons_c_(c)
    fill_poly([int(v) for v in xs], [int(v) for v in ys])
def icons_rr(x, y, w, h, r, c):
    icons_c_(c)
    fill_rect(x + r, y, w - 2 * r, h)
    fill_rect(x, y + r, w, h - 2 * r)
    for cx in (x + r, x + w - r - 1):
        for cy in (y + r, y + h - r - 1):
            fill_circle(cx, cy, r)
icons_FONT7 = {'1': '00100011000010000100001000010001110', '3': '11110000010000101110000010000111110', '5': '11111100001111000001000011000101110', '7': '11111000010001000100010000100001000', '9': '01110100011000101111000010001001100'}
def icons_digit7(x, y, ch, c):
    icons_c_(c)
    bits = icons_FONT7[ch]
    for r in range(7):
        row = bits[r * 5:r * 5 + 5]
        k = 0
        while k < 5:
            if row[k] == '1':
                e = k
                while e + 1 < 5 and row[e + 1] == '1':
                    e += 1
                draw_line(x + k, y + r, x + e, y + r)
                k = e + 1
            else:
                k += 1
def icons_digits(x, y, s, c, p=2):
    icons_c_(c)
    for i, ch in enumerate(s):
        bits = icons_FONT[ch]
        for n in range(15):
            if bits[n] == '1':
                fill_rect(x + i * 4 * p + n % 3 * p, y + n // 3 * p, p, p)
def icons_bevel(x, y, s, c):
    lt = tuple((min(255, v + 70) for v in c))
    dk = tuple((v // 2 for v in c))
    icons_box(x, y, s, s, c)
    icons_hline(x, x + s - 1, y, lt)
    icons_line(x, y, x, y + s - 1, lt)
    icons_hline(x, x + s - 1, y + s - 1, dk)
    icons_line(x + s - 1, y, x + s - 1, y + s - 1, dk)
def icons_ground(x, y, top, c, r=24):
    a = math.asin(top / r)
    xs = []
    ys = []
    for i in range(13):
        t = a + (math.pi - 2 * a) * i / 12
        xs.append(x + r * math.cos(t))
        ys.append(y + r * math.sin(t))
    icons_poly(xs, ys, c)
def icons_heart(x, y, s, c):
    icons_circ(x - s, y - 1, s, c)
    icons_circ(x + s, y - 1, s, c)
    icons_poly([x - 2 * s, x + 2 * s + 1, x], [y, y, y + 2 * s + 1], c)
def icons_diamond(x, y, s, c):
    icons_poly([x, x + s + 1, x, x - s - 1], [y - 2 * s, y, y + 2 * s, y], c)
def icons_spade(x, y, s, c):
    icons_circ(x - s, y + 1, s, c)
    icons_circ(x + s, y + 1, s, c)
    icons_poly([x - 2 * s, x + 2 * s + 1, x], [y + 1, y + 1, y - 2 * s - 1], c)
    icons_poly([x, x - s, x + s], [y + 1, y + 2 * s + 1, y + 2 * s + 1], c)
def icons_solitaire(x, y, c):
    suits = ((icons_spade, icons_INK), (icons_diamond, icons_RED), (icons_heart, icons_RED))
    for i in range(3):
        l = x - 18 + i * 10
        t = y - 12
        icons_box(l - 1, t - 1, 18, 26, icons_INK)
        icons_box(l, t, 16, 24, (250, 250, 245))
        f, col = suits[i]
        f(l + 4, t + 5, 2, col)
    icons_heart(x + 10, y + 3, 3, icons_RED)
def icons_blocks(x, y, c):
    s = 8
    cells = ((-2, 1, (220, 70, 70)), (-1, 1, (220, 70, 70)), (0, 1, (70, 110, 220)), (1, 1, (70, 110, 220)), (-2, 0, (80, 190, 90)), (0, 0, (70, 110, 220)), (1, 0, (230, 200, 60)), (-2, -1, (80, 190, 90)), (1, -1, (230, 200, 60)), (-1, -3, (170, 90, 210)), (0, -3, (170, 90, 210)), (0, -2, (170, 90, 210)))
    for cx, cy, col in cells:
        icons_bevel(x + cx * s, y + cy * s + 2, s, col)
def icons_sudoku(x, y, c):
    s = 11
    x0 = x - 16
    y0 = y - 16
    icons_box(x0 + s + 1, y0 + 1, s - 1, s - 1, (250, 225, 140))
    nums = ('53 ', ' 7 ', '1 9')
    for r in range(3):
        for k in range(3):
            ch = nums[r][k]
            if ch != ' ':
                icons_digit7(x0 + k * s + 3, y0 + r * s + 2, ch, icons_INK if (r, k) != (1, 1) else (40, 90, 200))
    for i in (1, 2):
        icons_line(x0 + i * s, y0, x0 + i * s, y0 + 3 * s, icons_INK)
        icons_hline(x0, x0 + 3 * s, y0 + i * s, icons_INK)
    icons_c_(icons_INK)
    for o in (0, 1):
        draw_rect(x0 - o, y0 - o, 3 * s + 2 * o, 3 * s + 2 * o)
def icons_anim(x, y, c):
    icons_box(x - 20, y - 13, 41, 27, (35, 35, 40))
    for i in range(5):
        icons_box(x - 18 + i * 8, y - 11, 4, 3, icons_WHITE)
        icons_box(x - 18 + i * 8, y + 9, 4, 3, icons_WHITE)
    for i, by in enumerate((4, -2, 2)):
        fx = x - 17 + i * 12
        icons_box(fx, y - 6, 11, 13, (120, 200, 240))
        icons_box(fx, y + 4, 11, 3, (70, 170, 80))
        icons_circ(fx + 5, y + by, 2, (240, 120, 40))
    icons_circ(x + 17, y - 9, 1, icons_RED)
def icons_flap(x, y, c):
    icons_box(x - 14, y - 16, 10, 4, icons_WHITE)
    icons_circ(x - 12, y - 15, 3, icons_WHITE)
    icons_circ(x - 7, y - 17, 4, icons_WHITE)
    icons_ground(x, y, 15, (70, 170, 80))
    icons_box(x + 14, y + 4, 4, 12, (120, 80, 40))
    icons_circ(x + 16, y + 1, 6, (50, 140, 60))
    icons_circ(x - 2, y - 1, 11, (170, 120, 20))
    icons_circ(x - 2, y - 1, 10, (250, 215, 50))
    icons_poly([x - 14, x - 2, x - 6], [y - 1, y + 1, y + 8], (255, 245, 190))
    icons_circ(x + 3, y - 5, 4, icons_WHITE)
    icons_circ(x + 4, y - 5, 2, icons_BLACK)
    icons_poly([x + 7, x + 17, x + 7], [y - 2, y + 1, y + 2], (245, 140, 30))
    icons_poly([x + 7, x + 15, x + 7], [y + 2, y + 3, y + 5], (200, 100, 20))
def icons_ttt(x, y, c):
    s = 12
    for i in (-1, 1):
        icons_box(x + i * 6 - 1, y - 18, 2, 36, icons_INK)
        icons_box(x - 18, y + i * 6 - 1, 36, 2, icons_INK)
    for i in (-1, 0, 1):
        cx = x + i * s
        cy = y + i * s
        icons_line(cx - 4, cy - 4, cx + 3, cy + 3, icons_INK, 2)
        icons_line(cx + 3, cy - 4, cx - 4, cy + 3, icons_INK, 2)
def icons_g2048(x, y, c):
    icons_rr(x - 20, y - 12, 41, 28, 4, (200, 160, 30))
    icons_rr(x - 20, y - 14, 41, 28, 4, (237, 194, 46))
    icons_digits(x - 14, y - 5, '2048', icons_WHITE)
def icons_pong(x, y, c):
    icons_c_(icons_WHITE)
    draw_rect(x - 21, y - 15, 43, 31)
    icons_hline(x - 21, x + 21, y, (200, 210, 230))
    for i in range(6):
        icons_box(x, y - 15 + i * 6, 2, 3, icons_WHITE)
    icons_box(x - 17, y - 11, 4, 14, icons_WHITE)
    icons_box(x + 14, y - 3, 4, 14, icons_WHITE)
    icons_circ(x - 6, y - 5, 2, (250, 150, 40))
def icons_breakout(x, y, c):
    cols = ((220, 60, 60), (235, 140, 50), (230, 210, 60), (70, 190, 90))
    for r in range(3):
        for i in range(4):
            bx = x - 19 + i * 10
            icons_box(bx, y - 15 + r * 6, 9, 5, cols[(i + r) % 4])
            icons_hline(bx, bx + 8, y - 15 + r * 6, tuple((min(255, v + 60) for v in cols[(i + r) % 4])))
    for i, (dx, dy) in enumerate(((-8, 12), (-5, 8))):
        icons_box(x + dx, y + dy, 2, 2, (120, 150, 230))
    icons_circ(x - 1, y + 5, 2, icons_WHITE)
    icons_rr(x - 11, y + 13, 22, 4, 1, icons_WHITE)
def icons_rpg(x, y, c):
    icons_circ(x - 5, y - 8, 6, (240, 200, 160))
    icons_box(x - 11, y - 15, 13, 5, (110, 70, 30))
    icons_box(x - 11, y - 11, 3, 5, (110, 70, 30))
    icons_box(x - 8, y - 9, 2, 2, icons_BLACK)
    icons_box(x - 3, y - 9, 2, 2, icons_BLACK)
    icons_box(x - 11, y - 1, 13, 12, (60, 120, 230))
    icons_box(x - 11, y + 5, 13, 2, (110, 70, 30))
    icons_box(x - 14, y, 3, 8, (240, 200, 160))
    icons_box(x - 10, y + 11, 4, 6, (60, 40, 30))
    icons_box(x - 4, y + 11, 4, 6, (60, 40, 30))
    icons_box(x + 2, y + 1, 4, 3, (240, 200, 160))
    icons_box(x + 2, y - 23, 12, 26, (15, 45, 70))
    icons_box(x + 4, y - 22, 8, 24, (40, 110, 170))
    icons_box(x + 5, y - 21, 6, 22, (100, 200, 245))
    icons_box(x + 7, y - 21, 2, 21, (240, 252, 255))
    icons_box(x + 3, y + 1, 10, 2, icons_GOLD)
    icons_box(x + 7, y + 3, 2, 5, (120, 80, 40))
    for sx, sy in ((x + 16, y - 18), (x + 1, y - 14), (x + 15, y - 6)):
        icons_box(sx, sy, 2, 2, (200, 240, 255))
def icons_simon(x, y, c):
    r = 18
    cols = ((40, 170, 60), (200, 40, 40), (40, 80, 200), (220, 180, 30))
    for q in range(4):
        a0 = -math.pi / 2 + q * math.pi / 2
        xs = [x]
        ys = [y]
        for i in range(6):
            a = a0 + math.pi / 2 * i / 5
            xs.append(x + r * math.cos(a))
            ys.append(y + r * math.sin(a))
        icons_poly(xs, ys, cols[q])
    icons_circ(x, y, 5, icons_BLACK)
    icons_box(x - 1, y - r, 2, 2 * r, icons_BLACK)
    icons_box(x - r, y - 1, 2 * r, 2, icons_BLACK)
def icons_hangman(x, y, c):
    icons_box(x - 19, y + 15, 24, 3, icons_INK)
    icons_box(x - 13, y - 18, 3, 34, icons_INK)
    icons_box(x - 13, y - 18, 24, 3, icons_INK)
    icons_line(x - 11, y - 9, x - 3, y - 17, icons_INK, 2)
    icons_box(x + 8, y - 16, 2, 6, (140, 90, 40))
    icons_circ(x + 9, y - 6, 4, icons_INK)
    icons_circ(x + 9, y - 6, 2, icons_WHITE)
    icons_line(x + 9, y - 2, x + 9, y + 7, icons_INK, 2)
    icons_line(x + 9, y + 1, x + 4, y + 5, icons_INK)
    icons_line(x + 10, y + 1, x + 15, y + 5, icons_INK)
    icons_line(x + 9, y + 7, x + 5, y + 13, icons_INK)
    icons_line(x + 10, y + 7, x + 14, y + 13, icons_INK)
def icons_crypt(x, y, c):
    random.seed(7)
    k = 0.21
    ox = x + 3
    oy = y - 17
    ca = math.cos(0.55)
    sa = math.sin(0.55)

    def m(cx, cy):
        return (ox + (cx - 140) * k, oy + (cy - 50) * k)

    def head(lx, ly):
        return m(140 + lx * ca - ly * sa, 50 + lx * sa + ly * ca)

    def band(pts, w):
        left = []
        right = []
        for i in range(len(pts) - 1):
            (x1, y1), (x2, y2) = (pts[i], pts[i + 1])
            d = math.hypot(x2 - x1, y2 - y1) or 1
            nx = -(y2 - y1) / d * w / 2
            ny = (x2 - x1) / d * w / 2
            left += [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny)]
            right += [(x1 - nx, y1 - ny), (x2 - nx, y2 - ny)]
        return [m(px, py) for px, py in left + right[::-1]]
    shapes = [[head(17 * math.cos(t * math.pi / 8), 25 * math.sin(t * math.pi / 8)) for t in range(16)], [head(px, py) for px, py in ((-18, -6), (-27, 30), (-24, 96), (-6, 70), (8, 100), (20, 60), (17, -6), (10, -24), (-10, -24))], band(((128, 125), (132, 88), (140, 66)), 11), [m(px, py) for px, py in ((98, 122), (128, 112), (160, 126), (150, 210), (148, 250), (108, 250), (106, 210))], band(((100, 128), (84, 250), (90, 260)), 7), band(((158, 128), (176, 248), (170, 258)), 7)]

    def spans(pts):
        out = []
        ys = [p[1] for p in pts]
        n = len(pts)
        for row in range(int(min(ys)), int(max(ys)) + 1):
            yc = row + 0.5
            xs = []
            for i in range(n):
                (x1, y1), (x2, y2) = (pts[i], pts[(i + 1) % n])
                if y1 <= yc < y2 or y2 <= yc < y1:
                    xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
            if len(xs) >= 2:
                out.append((row, int(min(xs) + 0.5), int(max(xs) + 0.5)))
        return out
    all_spans = [spans(sh) for sh in shapes]
    for sp in all_spans:
        for row, a, b in sp:
            g = random.randint(190, 255)
            icons_hline(a, max(a, b - 1), row, (g, g * 19 // 20, g * 9 // 10))
    for sp in all_spans:
        for row, a, b in sp[1:-1]:
            if b - a > 2:
                g = random.randint(28, 62)
                icons_hline(a + 1, b - 2, row, (g, g, g + 8))
    pts = []
    for ex, ey in ((137.2, 41.2), (149.1, 48.55)):
        a, b = m(ex, ey)
        pts.append((int(a), int(b)))
    for a, b in pts:
        icons_hline(a - 1, a + 1, b - 1, (35, 80, 150))
        icons_hline(a - 2, a + 2, b, (35, 80, 150))
        icons_hline(a - 1, a + 1, b + 1, (35, 80, 150))
    for a, b in pts:
        icons_hline(a - 1, a + 1, b, (80, 175, 245))
        icons_line(a, b - 1, a, b + 1, (80, 175, 245))
    for a, b in pts:
        icons_hline(a, a, b, (230, 250, 255))
    random.seed()
def icons_keys(x, y, c):
    for i in range(3):
        for j in range(3):
            icons_box(x - 14 + j * 10, y - 12 + i * 9, 8, 7, c)
def icons_wipe(x, y, c):
    icons_box(x - 10, y - 8, 20, 22, c)
    icons_box(x - 13, y - 13, 26, 3, c)
    icons_box(x - 4, y - 16, 8, 3, c)
    for i in (-5, 0, 5):
        icons_box(x + i - 1, y - 4, 2, 15, (0, 0, 0))
def icons_about(x, y, c):
    icons_c_(c)
    fill_circle(x, y - 10, 3)
    fill_rect(x - 2, y - 4, 5, 18)
icons_ICONS = {'GHSOLI': icons_solitaire, 'GHBLOCKS': icons_blocks, 'GHSUDOKU': icons_sudoku, 'GHANIM': icons_anim, 'GHFLAP': icons_flap, 'GHTTT': icons_ttt, 'GHMERGE': icons_g2048, 'GHPONG': icons_pong, 'GHBREAK': icons_breakout, 'GHRPG': icons_rpg, 'GHSIMON': icons_simon, 'GHHANG': icons_hangman, 'GHCRYPT': icons_crypt, '*keys': icons_keys, '*wipe': icons_wipe, '*about': icons_about}
def icons_bg(mod):
    return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
    f = icons_ICONS.get(mod)
    if f:
        f(x, y, c)
save_SLOTS = 3
save_PER = 100
save_B = 5
def save_hname(s):
    return 'A' + str(s) + 'H'
def save_dname(s, i):
    n = str(i)
    return 'A' + str(s) + '0' * (3 - len(n)) + n
def save_info(s):
    try:
        h = recall_list(save_hname(s))
        if len(h) >= 4 and int(h[0]) == 1:
            return (int(h[1]), int(h[2]))
    except Exception:
        pass
    return None
def save_save(s, data, frames, fps, show=None):
    nums = []
    n = len(data)
    i = 0
    while i < n:
        v = 0
        for j in range(save_B):
            v = v * 256 + (data[i + j] if i + j < n else 0)
        nums.append(v)
        i += save_B
    nl = (len(nums) + save_PER - 1) // save_PER
    for k in range(nl):
        if show:
            show(k, nl)
        store_list(save_dname(s, k), nums[k * save_PER:(k + 1) * save_PER])
    old = 0
    try:
        old = int(recall_list(save_hname(s))[3])
    except Exception:
        pass
    for k in range(nl, old):
        try:
            store_list(save_dname(s, k), [0])
        except Exception:
            pass
    store_list(save_hname(s), [1, frames, fps, nl, n])
    return nl
def save_load(s, show=None):
    h = recall_list(save_hname(s))
    frames, fps, nl, n = (int(h[1]), int(h[2]), int(h[3]), int(h[4]))
    data = bytearray(n)
    p = 0
    for k in range(nl):
        if show:
            show(k, nl)
        for v in recall_list(save_dname(s, k)):
            v = int(v)
            chunk = []
            for j in range(save_B):
                chunk.append(v % 256)
                v //= 256
            for j in range(save_B - 1, -1, -1):
                if p < n:
                    data[p] = chunk[j]
                    p += 1
    return (data, frames, fps)
def save_wipe():
    n = 0
    for s in range(1, save_SLOTS + 1):
        try:
            h = recall_list(save_hname(s))
            nl = int(h[3])
        except Exception:
            continue
        for k in range(nl):
            try:
                store_list(save_dname(s, k), [0])
                n += 1
            except Exception:
                pass
        store_list(save_hname(s), [0])
        n += 1
    return n
anim_CWD = 32
anim_CHG = 24
anim_N = anim_CWD * anim_CHG
anim_P = 6
anim_CX = 6
anim_CY = 26
anim_PAL = ((255, 255, 255), (0, 0, 0), (128, 128, 128), (200, 200, 200), (220, 40, 40), (245, 140, 30), (250, 220, 50), (60, 190, 70), (20, 100, 40), (80, 200, 230), (40, 80, 200), (20, 30, 90), (150, 60, 190), (245, 140, 190), (130, 80, 40), (245, 200, 160))
anim_INK = (20, 20, 20)
anim_HI = (200, 120, 0)
anim_MAXB = 60000
anim_KEYGAP = 15
def anim_enc_key(fr):
    out = bytearray([1])
    i = 0
    while i < anim_N:
        c = fr[i]
        n = 1
        while i + n < anim_N and fr[i + n] == c and (n < 255):
            n += 1
        out.append(n)
        out.append(c)
        i += n
    return bytes(out)
def anim_enc_delta(prev, fr):
    out = bytearray([0])
    pos = 0
    i = 0
    while i < anim_N:
        if fr[i] == prev[i]:
            i += 1
            continue
        j = i
        last = i
        while j < anim_N and j - i < 254:
            if fr[j] != prev[j]:
                j += 1
                last = j
            elif j + 1 < anim_N and fr[j + 1] != prev[j + 1]:
                j += 1
            else:
                break
        j = last
        skip = i - pos
        while skip > 255:
            out.append(255)
            out.append(0)
            skip -= 255
        out.append(skip)
        out.append(j - i)
        t = i
        while t < j:
            hi = fr[t]
            lo = fr[t + 1] if t + 1 < j else 0
            out.append(hi * 16 + lo)
            t += 2
        pos = j
        i = j
    return bytes(out)
def anim_apply(fr, d):
    if d[0] == 1:
        p = 1
        i = 0
        while p < len(d):
            n = d[p]
            c = d[p + 1]
            for t in range(n):
                fr[i + t] = c
            i += n
            p += 2
        return
    p = 1
    pos = 0
    L = len(d)
    while p < L:
        pos += d[p]
        n = d[p + 1]
        p += 2
        for t in range(n):
            b = d[p + t // 2]
            fr[pos + t] = b >> 4 if t % 2 == 0 else b & 15
        p += (n + 1) // 2
        pos += n
class anim_Studio:
    pass
def anim_dec(s, i):
    k = i
    while k > 0 and s.F[k][0] != 1:
        k -= 1
    fr = bytearray(anim_N)
    for j in range(k, i + 1):
        anim_apply(fr, s.F[j])
    return fr
def anim_chain(s, i):
    n = 0
    k = i
    while k > 0 and s.F[k][0] != 1:
        k -= 1
        n += 1
    return n
def anim_encode_at(s, i, fr, prev):
    if prev is None:
        return anim_enc_key(fr)
    d = anim_enc_delta(prev, fr)
    if i > 0 and anim_chain(s, i - 1) + 1 >= anim_KEYGAP:
        return anim_enc_key(fr)
    return d
def anim_commit(s):
    if not s.dirty:
        return
    i = s.ci
    nx = None
    if i + 1 < len(s.F) and s.F[i + 1][0] == 0:
        nx = anim_dec(s, i + 1)
    s.F[i] = anim_encode_at(s, i, s.cur, s.prv if i > 0 else None)
    if nx is not None:
        s.F[i + 1] = anim_enc_delta(s.cur, nx)
    s.dirty = False
def anim_used(s):
    t = 0
    for f in s.F:
        t += len(f) + 2
    return t
def anim_want(s, i):
    v = s.cur[i]
    if v == 0 and s.onion and (s.ci > 0) and s.prv[i]:
        return 16 + s.prv[i]
    return v
def anim_paint(s, i, v):
    x = anim_CX + i % anim_CWD * anim_P
    y = anim_CY + i // anim_CWD * anim_P
    if v >= 16:
        c = anim_PAL[v - 16]
        rect(x, y, anim_P, anim_P, anim_PAL[0])
        rect(x + 1, y + 1, anim_P - 2, anim_P - 2, ((c[0] + 510) // 3, (c[1] + 510) // 3, (c[2] + 510) // 3))
    else:
        rect(x, y, anim_P, anim_P, anim_PAL[v])
    s.shown[i] = v
def anim_refresh(s):
    for i in range(anim_N):
        v = anim_want(s, i)
        if s.shown[i] != v:
            anim_paint(s, i, v)
def anim_cursor(s):
    x = anim_CX + s.cx * anim_P
    y = anim_CY + s.cy * anim_P
    v = s.cur[s.cy * anim_CWD + s.cx]
    col(BLACK if v in (0, 3, 6, 15) else WHITE)
    draw_rect(x + 1, y + 1, anim_P - 3, anim_P - 3)
def anim_uncursor(s):
    i = s.cy * anim_CWD + s.cx
    anim_paint(s, i, anim_want(s, i))
def anim_palette(s, sel=-1):
    for c in range(16):
        x = 210 + c % 4 * 26
        y = 30 + c // 4 * 26
        rect(x - 2, y - 2, 26, 26, WHITE)
        if c == s.col:
            rbox(x - 2, y - 2, 26, 26, 5, GOLD, 2, WHITE)
        if c == sel:
            rbox(x - 2, y - 2, 26, 26, 5, anim_INK, 2, WHITE)
        rect(x + 1, y + 1, 20, 20, anim_PAL[c])
        if c == 0:
            col(GREY)
            draw_rect(x + 1, y + 1, 19, 19)
def anim_topbar(s):
    rect(0, 0, 320, 22, WHITE)
    text(4, 17, 'Frame ' + str(s.ci + 1) + '/' + str(len(s.F)), anim_INK)
    text(160, 17, str(s.fps) + 'fps', GREY)
    pct = anim_used(s) * 100 // anim_MAXB
    text(236, 17, 'Mem ' + str(pct) + '%', RED if pct > 90 else GREY)
def anim_botbar(s):
    rect(0, 176, 320, 34, WHITE)
    m = ('Pen up', 'PEN DOWN', 'ERASER')[s.pen]
    text(6, 190, m, anim_HI if s.pen else anim_INK)
    text(6, 205, 'ENTER pen DEL eraser 2nd menu', GREY)
def anim_full(s):
    cls(WHITE)
    rect(anim_CX - 2, anim_CY - 2, anim_CWD * anim_P + 4, anim_CHG * anim_P + 4, DARK)
    s.shown = bytearray([255] * anim_N)
    anim_refresh(s)
    anim_palette(s)
    anim_topbar(s)
    anim_botbar(s)
    rect(208, 136, 104, 36, WHITE)
    text(210, 150, 'Onion ' + ('on' if s.onion else 'off'), GREY)
    text(210, 168, 'Saved ' + (str(s.slot) if s.slot else '-'), GREY)
    anim_cursor(s)
def anim_set_px(s, i, c):
    if s.cur[i] != c:
        if not s.dirty:
            s.undo = bytearray(s.cur)
        s.cur[i] = c
        s.dirty = True
        s.changed = True
def anim_fill(s):
    i0 = s.cy * anim_CWD + s.cx
    old = s.cur[i0]
    new = s.col
    if old == new:
        return
    s.undo = bytearray(s.cur)
    stack = [i0]
    while stack:
        i = stack.pop()
        if s.cur[i] != old:
            continue
        s.cur[i] = new
        x = i % anim_CWD
        if x > 0:
            stack.append(i - 1)
        if x < anim_CWD - 1:
            stack.append(i + 1)
        if i >= anim_CWD:
            stack.append(i - anim_CWD)
        if i < anim_N - anim_CWD:
            stack.append(i + anim_CWD)
    s.dirty = True
    s.changed = True
def anim_go(s, j):
    anim_commit(s)
    if j == s.ci + 1:
        s.prv = s.cur
        s.cur = bytearray(s.prv)
        anim_apply(s.cur, s.F[j])
    else:
        s.cur = anim_dec(s, j)
        s.prv = anim_dec(s, j - 1) if j > 0 else bytearray(anim_N)
    s.ci = j
    s.undo = None
def anim_add_frame(s, blank):
    if anim_used(s) > anim_MAXB:
        message(['Memory is full.', 'Save, or delete frames.'], "Can't add")
        return
    anim_commit(s)
    i = s.ci
    nx = anim_dec(s, i + 1) if i + 1 < len(s.F) else None
    new = bytearray(anim_N) if blank else bytearray(s.cur)
    s.F.insert(i + 1, anim_enc_delta(s.cur, new))
    if nx is not None and s.F[i + 2][0] == 0:
        s.F[i + 2] = anim_enc_delta(new, nx)
    s.prv = s.cur
    s.cur = new
    s.ci = i + 1
    s.changed = True
def anim_del_frame(s):
    if len(s.F) == 1:
        s.undo = bytearray(s.cur)
        s.cur = bytearray(anim_N)
        s.dirty = True
        return
    i = s.ci
    nx = anim_dec(s, i + 1) if i + 1 < len(s.F) else None
    p = anim_dec(s, i - 1) if i > 0 else None
    del s.F[i]
    if nx is not None:
        s.F[i] = anim_enc_key(nx) if p is None else anim_enc_delta(p, nx)
    if i >= len(s.F):
        i = len(s.F) - 1
    s.dirty = False
    s.ci = i
    s.cur = anim_dec(s, i)
    s.prv = anim_dec(s, i - 1) if i > 0 else bytearray(anim_N)
    s.changed = True
def anim_play(s):
    anim_commit(s)
    onion = s.onion
    s.onion = False
    rect(0, 176, 320, 34, WHITE)
    text(6, 190, 'Playing. Up/Down: speed', anim_HI)
    text(6, 205, 'Any other key stops', GREY)
    i = 0
    fr = bytearray(anim_N)
    while True:
        if s.F[i][0] == 1 or i == 0:
            fr = bytearray(anim_N)
        anim_apply(fr, s.F[i])
        for p in range(anim_N):
            if s.shown[p] != fr[p]:
                anim_paint(s, p, fr[p])
        rect(0, 0, 150, 22, WHITE)
        text(4, 17, 'Frame ' + str(i + 1) + '/' + str(len(s.F)), anim_INK)
        t = 0
        steps = max(1, 12 // s.fps)
        stop = False
        for q in range(steps):
            k = key()
            if k == UP and s.fps < 12:
                s.fps += 1
                anim_topbar(s)
            elif k == DOWN and s.fps > 1:
                s.fps -= 1
                anim_topbar(s)
            elif k and k not in (UP, DOWN):
                stop = True
                break
            pause(1 / 12)
        if stop:
            break
        i = (i + 1) % len(s.F)
    while key():
        pass
    s.onion = onion
    s.cur = anim_dec(s, s.ci)
    anim_full(s)
anim_ITEMS = ('Color', 'Fill area', 'Undo', 'Clear frame', 'Next frame', 'Prev frame', 'Add copy', 'Add blank', 'Delete frame', 'Play', 'Speed', 'Onion skin', 'Save', 'Load', 'New', 'Quit')
def anim_menu(sel):
    cls()
    ctext(18, 'STUDIO MENU', GOLD)
    while True:
        for i in range(16):
            x = 8 + i // 8 * 156
            y = 26 + i % 8 * 23
            c = GOLD if i == sel else WHITE
            rect(x, y, 150, 21, BLACK)
            rbox(x, y, 148, 21, 8, c)
            text(x + 74 - len(anim_ITEMS[i]) * 5, y + 16, anim_ITEMS[i], c)
        k = wkey()
        if k == UP:
            sel = (sel - 1) % 16
        elif k == DOWN:
            sel = (sel + 1) % 16
        elif k in (LEFT, RIGHT):
            sel = (sel + 8) % 16
        elif k == OK:
            return sel
        elif k in (CLR, SECOND):
            return -1
def anim_pick_color(s):
    sel = s.col
    while True:
        anim_palette(s, sel)
        k = wkey()
        if k == LEFT:
            sel = (sel - 1) % 16
        elif k == RIGHT:
            sel = (sel + 1) % 16
        elif k == UP:
            sel = (sel - 4) % 16
        elif k == DOWN:
            sel = (sel + 4) % 16
        elif k == OK:
            s.col = sel
            break
        elif k == CLR:
            break
    anim_palette(s)
def anim_pick_speed(s):
    cls()
    while True:
        rect(0, 60, 320, 80, BLACK)
        ctext(80, 'PLAYBACK SPEED', GOLD)
        ctext(110, '< ' + str(s.fps) + ' frames a second >')
        ctext(140, 'ENTER done', GREY)
        k = wkey()
        if k == LEFT and s.fps > 1:
            s.fps -= 1
        elif k == RIGHT and s.fps < 12:
            s.fps += 1
        elif k in (OK, CLR):
            return
def anim_pick_slot(title):
    opts = []
    for sl in range(1, save_SLOTS + 1):
        inf = save_info(sl)
        opts.append('Slot ' + str(sl) + (': ' + str(inf[0]) + ' fr' if inf else ': empty'))
    opts.append('Cancel')
    c = choose(title, opts)
    if c < 0 or c == save_SLOTS:
        return 0
    return c + 1
def anim_progress(k, n):
    rect(60, 120, 200, 30, BLACK)
    rbox(60, 120, 200, 16, 6, WHITE)
    rect(64, 124, max(2, 192 * (k + 1) // n), 8, GOLD)
def anim_do_save(s):
    anim_commit(s)
    sl = anim_pick_slot('SAVE TO')
    if not sl:
        return
    cls()
    ctext(100, 'Saving...', GOLD)
    data = bytearray()
    for f in s.F:
        data.append(len(f) // 256)
        data.append(len(f) % 256)
        data.extend(f)
    try:
        save_save(sl, data, len(s.F), s.fps, anim_progress)
        s.slot = sl
        s.changed = False
        message([str(len(s.F)) + ' frames saved', 'to slot ' + str(sl) + '.'], 'Saved')
    except Exception as e:
        message(['Could not save:', str(e)[:24]], 'Error')
def anim_do_load(s):
    sl = anim_pick_slot('LOAD FROM')
    if not sl or not save_info(sl):
        return
    if s.changed and message(['Unsaved changes will', 'be lost. ENTER: load', 'CLEAR: cancel'], 'Load?') != OK:
        return
    cls()
    ctext(100, 'Loading...', GOLD)
    try:
        data, frames, fps = save_load(sl, anim_progress)
    except Exception as e:
        message(['Could not load:', str(e)[:24]], 'Error')
        return
    F = []
    p = 0
    for k in range(frames):
        n = data[p] * 256 + data[p + 1]
        F.append(bytes(data[p + 2:p + 2 + n]))
        p += 2 + n
    anim_reset(s, F, fps)
    s.slot = sl
def anim_reset(s, F, fps):
    s.F = F
    s.fps = fps
    s.ci = 0
    s.cur = anim_dec(s, 0)
    s.prv = bytearray(anim_N)
    s.dirty = False
    s.changed = False
    s.undo = None
    s.slot = 0
def anim_studio():
    s = anim_Studio()
    anim_reset(s, [anim_enc_key(bytearray(anim_N))], 6)
    s.cx = 16
    s.cy = 12
    s.col = 1
    s.pen = 0
    s.onion = True
    s.shown = bytearray([255] * anim_N)
    msel = 0
    anim_full(s)
    held = 0
    hc = 0
    while True:
        k = key()
        if k == held and k:
            hc += 1
        else:
            hc = 0
        rep = k != held or (hc > 3 and hc % 1 == 0)
        held = k
        if not k:
            pause(0.01)
            continue
        if k in (LEFT, RIGHT, UP, DOWN) and rep:
            anim_uncursor(s)
            if k == LEFT and s.cx > 0:
                s.cx -= 1
            elif k == RIGHT and s.cx < anim_CWD - 1:
                s.cx += 1
            elif k == UP and s.cy > 0:
                s.cy -= 1
            elif k == DOWN and s.cy < anim_CHG - 1:
                s.cy += 1
            if s.pen:
                i = s.cy * anim_CWD + s.cx
                anim_set_px(s, i, s.col if s.pen == 1 else 0)
                anim_paint(s, i, anim_want(s, i))
            anim_cursor(s)
            continue
        if not rep:
            continue
        if k == OK or k == DEL:
            want_pen = 1 if k == OK else 2
            s.pen = 0 if s.pen == want_pen else want_pen
            if s.pen:
                i = s.cy * anim_CWD + s.cx
                anim_set_px(s, i, s.col if s.pen == 1 else 0)
                anim_paint(s, i, anim_want(s, i))
                anim_cursor(s)
            anim_botbar(s)
            anim_topbar(s)
            continue
        if k == CLR and s.pen:
            s.pen = 0
            anim_botbar(s)
            continue
        if k == SECOND or k == CLR:
            c = anim_menu(msel)
            if c >= 0:
                msel = c
            s.pen = 0
            if c == 0:
                anim_full(s)
                anim_pick_color(s)
            elif c == 1:
                anim_fill(s)
            elif c == 2 and s.undo is not None:
                u = s.undo
                s.undo = bytearray(s.cur)
                s.cur = u
                s.dirty = True
            elif c == 3:
                s.undo = bytearray(s.cur)
                s.cur = bytearray(anim_N)
                s.dirty = True
            elif c == 4:
                if s.ci + 1 < len(s.F):
                    anim_go(s, s.ci + 1)
                else:
                    anim_add_frame(s, False)
            elif c == 5 and s.ci > 0:
                anim_go(s, s.ci - 1)
            elif c == 6:
                anim_add_frame(s, False)
            elif c == 7:
                anim_add_frame(s, True)
            elif c == 8:
                anim_del_frame(s)
            elif c == 9:
                anim_full(s)
                anim_play(s)
            elif c == 10:
                anim_pick_speed(s)
            elif c == 11:
                s.onion = not s.onion
            elif c == 12:
                anim_do_save(s)
            elif c == 13:
                anim_do_load(s)
            elif c == 14:
                if not s.changed or message(['Unsaved changes will', 'be lost. ENTER: new', 'CLEAR: cancel'], 'New?') == OK:
                    anim_reset(s, [anim_enc_key(bytearray(anim_N))], 6)
            elif c == 15:
                if not s.changed or message(['Unsaved changes will', 'be lost. ENTER: quit', 'CLEAR: cancel'], 'Quit?') == OK:
                    return
            if c != 0:
                anim_full(s)
anim_RULES = 'Draw a picture, add frames, and play them back. Saves stay on the calculator.'
anim_KEYS = ['Arrows: move  ENTER: pen', 'DEL: eraser  2nd: menu', 'Menu: colors, frames, play,', 'speed, save and load']
def anim_main():
    while True:
        c = home('GHANIM', 'ANIMATION STUDIO', anim_RULES, anim_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        anim_studio()
blocks_CW = 10
blocks_CH = 20
blocks_C = 9
blocks_OUT = (50, 20, 70)
blocks_WELL = (35, 30, 90)
blocks_DOT = (60, 55, 125)
blocks_PANEL = (70, 35, 100)
blocks_X0 = 115
blocks_Y0 = 22
blocks_SHAPES = (((0, 1), (1, 1), (2, 1), (3, 1)), ((0, 0), (1, 0), (0, 1), (1, 1)), ((1, 0), (0, 1), (1, 1), (2, 1)), ((0, 0), (0, 1), (1, 1), (2, 1)), ((2, 0), (0, 1), (1, 1), (2, 1)), ((1, 0), (2, 0), (0, 1), (1, 1)), ((0, 0), (1, 0), (1, 1), (2, 1)))
blocks_COLS = ((90, 200, 220), (230, 200, 60), (170, 90, 210), (70, 110, 220), (230, 140, 50), (80, 190, 90), (220, 70, 70))
def blocks_cells(p):
    s, r, x, y = p
    out = []
    for cx, cy in blocks_SHAPES[s]:
        rx, ry = (cx, cy)
        if s != 1:
            for i in range(r):
                rx, ry = (2 - ry, rx)
        out.append((x + rx, y + ry))
    return out
def blocks_cells_i(p):
    s, r, x, y = p
    if r % 2 == 0:
        return [(x + i, y + 1) for i in range(4)]
    return [(x + 2, y + i) for i in range(4)]
def blocks_get(p):
    return blocks_cells_i(p) if p[0] == 0 else blocks_cells(p)
def blocks_ok(b, p):
    for x, y in blocks_get(p):
        if x < 0 or x >= blocks_CW or y >= blocks_CH:
            return False
        if y >= 0 and b[y][x]:
            return False
    return True
def blocks_sq(x, y, c):
    if y < 0:
        return
    px = blocks_X0 + x * blocks_C
    py = blocks_Y0 + y * blocks_C
    if c == blocks_WELL:
        rect(px, py, blocks_C, blocks_C, blocks_WELL)
        rect(px + 4, py + 4, 1, 1, blocks_DOT)
    else:
        rect(px, py, blocks_C, blocks_C, dk(c, 0.55))
        rect(px, py, blocks_C - 1, blocks_C - 1, c)
        col(lt(c, 0.45))
        draw_line(px, py, px + blocks_C - 2, py)
        draw_line(px, py, px, py + blocks_C - 2)
        rect(px + 2, py + 2, 2, 2, lt(c, 0.7))
def blocks_draw_piece(p, c=None):
    for x, y in blocks_get(p):
        blocks_sq(x, y, blocks_COLS[p[0]] if c is None else c)
def blocks_board(b):
    for y in range(blocks_CH):
        for x in range(blocks_CW):
            v = b[y][x]
            blocks_sq(x, y, blocks_COLS[v - 1] if v else blocks_WELL)
def blocks_side(score, lines, nxt):
    for y, h in ((26, 64), (96, 40), (142, 40)):
        rbox(226, y, 88, h, 6, (150, 110, 190), 2, blocks_PANEL)
    text(234, 44, 'NEXT', (200, 185, 230))
    for x, y in blocks_get((nxt, 0, 0, 0)):
        c = blocks_COLS[nxt]
        rect(244 + x * 9, 54 + y * 9, 9, 9, dk(c, 0.55))
        rect(244 + x * 9, 54 + y * 9, 8, 8, c)
        rect(245 + x * 9, 55 + y * 9, 2, 2, lt(c, 0.7))
    text(234, 114, 'SCORE', (200, 185, 230))
    text(234, 131, str(score))
    text(234, 160, 'LINES', (200, 185, 230))
    text(234, 177, str(lines))
def blocks_game():
    b = [[0] * blocks_CW for i in range(blocks_CH)]
    cls(blocks_OUT)
    for i in range(0, 210, 30):
        rect(0, i, 320, 15, (58, 25, 80))
    rbox(blocks_X0 - 4, blocks_Y0 - 4, blocks_CW * blocks_C + 8, blocks_CH * blocks_C + 8, 4, WHITE, 2, blocks_WELL)
    blocks_board(b)
    rbox(4, 26, 96, 56, 6, GOLD, 2, blocks_PANEL)
    text(14, 48, 'STACK', GOLD)
    text(14, 68, 'DROP', GOLD)
    for i, cc in enumerate(blocks_COLS[:5]):
        rect(12 + i * 16, 96, 12, 12, dk(cc, 0.55))
        rect(12 + i * 16, 96, 11, 11, cc)
    rbox(4, 150, 96, 40, 6, (150, 110, 190), 2, blocks_PANEL)
    text(12, 167, '2nd key:', (200, 185, 230))
    text(12, 184, 'drop it', (200, 185, 230))
    score = 0
    lines = 0
    nxt = random.randint(0, 6)
    p = None
    t = 0
    held = 0
    hc = 0
    blocks_side(score, lines, nxt)
    while True:
        if p is None:
            p = [nxt, 0, 3, -1]
            nxt = random.randint(0, 6)
            blocks_side(score, lines, nxt)
            if not blocks_ok(b, p):
                message(['Score ' + str(score), 'Lines ' + str(lines)], 'Stacked to the top')
                return
            blocks_draw_piece(p)
        k = key()
        if k == CLR:
            return
        speed = max(2, 14 - lines // 5)
        q = list(p)
        if k == held and k:
            hc += 1
        else:
            hc = 0
        if k != held or k == DOWN or (k in (LEFT, RIGHT) and hc > 4 and (hc % 2 == 0)):
            if k == LEFT:
                q[2] -= 1
            elif k == RIGHT:
                q[2] += 1
            elif k == UP:
                q[1] = (q[1] + 1) % 4
                if not blocks_ok(b, q):
                    q[2] -= 1
                    if not blocks_ok(b, q):
                        q[2] += 2
            elif k == DOWN:
                t = speed
            elif k == SECOND:
                while blocks_ok(b, [q[0], q[1], q[2], q[3] + 1]):
                    q[3] += 1
                t = speed
        held = k
        t += 1
        fall = t >= speed
        if q != p and blocks_ok(b, q):
            blocks_draw_piece(p, blocks_WELL)
            p = q
            blocks_draw_piece(p)
        if fall:
            t = 0
            q = [p[0], p[1], p[2], p[3] + 1]
            if blocks_ok(b, q):
                blocks_draw_piece(p, blocks_WELL)
                p = q
                blocks_draw_piece(p)
            else:
                for x, y in blocks_get(p):
                    if y >= 0:
                        b[y][x] = p[0] + 1
                full = [y for y in range(blocks_CH) if 0 not in b[y]]
                if full:
                    for y in full:
                        del b[y]
                        b.insert(0, [0] * blocks_CW)
                    lines += len(full)
                    score += (0, 100, 300, 500, 800)[len(full)]
                    blocks_board(b)
                p = None
        pause(0.02)
blocks_RULES = "Shapes fall from the top. Fit them together to fill whole rows, which then clear. Don't let the stack reach the top."
blocks_KEYS = ['Left/Right: move', 'Up: turn', 'Down: drop faster', '2nd: drop all the way', 'CLEAR: quit']
def blocks_main():
    while True:
        c = home('GHBLOCKS', 'STACK DROP', blocks_RULES, blocks_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        blocks_game()
break_ROWS = 5
break_COLS = 10
break_BW = 30
break_BH = 10
break_BY = 34
break_RC = ((220, 60, 60), (235, 140, 50), (230, 210, 60), (70, 190, 90), (170, 90, 210))
break_PW = 46
break_BG = (30, 70, 170)
def break_brick(r, c, on):
    if on:
        block(10 + c * break_BW + 1, break_BY + r * break_BH + 1, break_BW - 2, break_BH - 2, break_RC[r], 2)
    else:
        rect(10 + c * break_BW + 1, break_BY + r * break_BH + 1, break_BW - 2, break_BH - 2, break_BG)
def break_walls():
    rect(0, 24, 4, 186, (200, 210, 230))
    rect(316, 24, 4, 186, (200, 210, 230))
    rect(3, 24, 1, 186, (120, 130, 160))
    rect(316, 24, 1, 186, (120, 130, 160))
def break_paddle(x, c=WHITE):
    if c == break_BG:
        rect(x, 192, break_PW, 8, break_BG)
        return
    rrect(x, 192, break_PW, 8, 3, (230, 120, 60))
    rect(x + 4, 193, break_PW - 8, 2, (255, 200, 150))
def break_hud(score, lives):
    rect(0, 0, 320, 22, break_BG)
    text(6, 17, 'Score ' + str(score))
    text(214, 17, 'Balls ' + str(lives), GOLD)
def break_game():
    cls(break_BG)
    rect(0, 22, 320, 2, WHITE)
    break_walls()
    b = [[1] * break_COLS for r in range(break_ROWS)]
    for r in range(break_ROWS):
        for c in range(break_COLS):
            break_brick(r, c, 1)
    left = break_ROWS * break_COLS
    score = 0
    lives = 3
    px = 137
    break_hud(score, lives)
    while lives > 0 and left > 0:
        bx, by = (px + break_PW / 2, 180.0)
        vx = random.choice((-3.0, 3.0))
        vy = -3.0
        break_paddle(px)
        pause(0.5)
        st = Steer((LEFT, RIGHT))
        while True:
            k = key()
            if k == CLR:
                return
            opx = px
            d = st.feed(k)
            if d == LEFT:
                px = max(4, px - 7)
                if px == 4:
                    st.stop()
            elif d == RIGHT:
                px = min(316 - break_PW, px + 7)
                if px == 316 - break_PW:
                    st.stop()
            obx, oby = (bx, by)
            bx += vx
            by += vy
            if bx < 7 or bx > 312:
                vx = -vx
                bx = max(7, min(312, bx))
            if by < 26:
                vy = -vy
                by = 26
            if vy > 0 and 188 < by < 198 and (px - 3 < bx < px + break_PW + 3):
                vy = -abs(vy)
                vx = (bx - (px + break_PW / 2)) / 5
                if abs(vx) < 1:
                    vx = 1 if vx >= 0 else -1
            r = int((by - break_BY) // break_BH)
            c = int((bx - 10) // break_BW)
            if 0 <= r < break_ROWS and 0 <= c < break_COLS and b[r][c]:
                b[r][c] = 0
                break_brick(r, c, 0)
                vy = -vy
                score += (break_ROWS - r) * 10
                left -= 1
                break_hud(score, lives)
                if left == 0:
                    break
            rect(int(obx) - 3, int(oby) - 3, 7, 7, break_BG)
            if opx != px or oby > 186:
                break_paddle(opx, break_BG)
                break_paddle(px)
            ball(int(bx), int(by), 3, WHITE)
            if by > 210:
                lives -= 1
                break_hud(score, lives)
                break
        rect(int(bx) - 3, int(by) - 3, 7, 7, break_BG)
        rect(4, 192, 312, 8, break_BG)
    if left == 0:
        message(['Score ' + str(score)], 'All bricks cleared!')
    else:
        message(['Score ' + str(score)], 'Game over')
break_RULES = 'Bounce the ball off your paddle to break every brick. You have 3 balls.'
break_KEYS = ['Left/Right: paddle glides that way', 'ENTER: stop the paddle', 'CLEAR: quit']
def break_main():
    while True:
        c = home('GHBREAK', 'BREAKOUT', break_RULES, break_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        break_game()
try:
    from time import monotonic as crypt_now
except Exception:
    crypt_now = None
crypt_MAP = ['#BBBB###SSS###', 'B....#.......#', 'B............k', '#####G.......#', '#....#.......#', 'T....l.......j', '#....#.......C', '########PF####']
crypt_VW = 320
crypt_VH = 172
crypt_COLS = 40
crypt_CWID = crypt_VW // crypt_COLS
crypt_FOV = 1.0
crypt_WALL = (75, 95, 99)
crypt_DOOR = (110, 75, 45)
crypt_FLOOR = (42, 36, 32)
crypt_CEIL = (16, 16, 18)
crypt_LINK1 = 'petradavis.github.io/'
crypt_LINK2 = 'Encrypted/?ysolde=1'
crypt_CIPHER = 'LI WKH OLJKWV GLH VKH LV LQ WKH URRP. GRQW UXQ. KLGH LQ WKH FRDW FORVHW. LWV FRGH LV HFKR'
crypt_TAPGRID = ('ABCDE', 'FGHIK', 'LMNOP', 'QRSTU', 'VWXYZ')
crypt_KNOCKS = ((4, 1), (4, 5), (2, 4), (1, 5), (4, 4))
class crypt_St:
    pass
crypt_SPR = {'couch': (1.3, ((0, 1, 0, 0.2, (150, 40, 45)), (0.08, 0.92, 0.2, 0.36, (120, 30, 35)), (0, 0.12, 0.2, 0.28, (150, 40, 45)), (0.88, 1, 0.2, 0.28, (150, 40, 45)))), 'table': (0.9, ((0, 0.12, 0, 0.28, (95, 65, 40)), (0.88, 1, 0, 0.28, (95, 65, 40)), (0, 1, 0.28, 0.33, (120, 85, 50)), (0.3, 0.7, 0.33, 0.37, (140, 70, 180)))), 'phone': (0.6, ((0, 0.15, 0, 0.3, (95, 65, 40)), (0.85, 1, 0, 0.3, (95, 65, 40)), (0, 1, 0.3, 0.34, (120, 85, 50)), (0.25, 0.75, 0.34, 0.42, (20, 20, 20)))), 'lamp': (0.6, ((0.45, 0.55, 0, 0.55, (180, 150, 70)), (0.15, 0.85, 0.55, 0.72, (235, 220, 170)))), 'desk': (1.2, ((0, 0.1, 0, 0.3, (95, 65, 40)), (0.9, 1, 0, 0.3, (95, 65, 40)), (0, 1, 0.3, 0.35, (120, 85, 50)), (0.2, 0.5, 0.35, 0.38, (200, 190, 150)))), 'rack': (0.7, ((0.46, 0.54, 0, 0.8, (80, 55, 35)), (0.15, 0.45, 0.35, 0.75, (60, 70, 110)), (0.55, 0.85, 0.4, 0.72, (110, 50, 50)))), 'vase': (0.7, ((0.1, 0.9, 0, 0.25, (95, 65, 40)), (0.35, 0.65, 0.25, 0.45, (60, 120, 140)), (0.3, 0.7, 0.45, 0.55, (90, 140, 70))))}
crypt_SPRITES = [(3.3, 5.5, 'couch'), (1.9, 4.6, 'table'), (4.4, 6.4, 'phone'), (1.0, 6.5, 'lamp'), (2.6, 1.5, 'desk'), (12.4, 4.9, 'rack'), (6.5, 1.4, 'vase')]
crypt_ROOMS = (('Library', 0, 0, 5, 3), ('Living Room', 0, 3, 5, 8), ('Grand Foyer', 5, 0, 14, 8))
def crypt_tile(x, y):
    if 0 <= y < len(crypt_MAP) and 0 <= int(x) < 14:
        return crypt_MAP[int(y)][int(x)]
    return '#'
def crypt_solid(g, x, y):
    t = crypt_tile(x, y)
    if t == 'l' and g.living:
        return False
    return t != '.'
def crypt_room(g):
    for n, x0, y0, x1, y1 in crypt_ROOMS:
        if x0 <= g.x < x1 and y0 <= g.y < y1:
            return n
    return 'Grand Foyer'
def crypt_clock():
    return crypt_now() if crypt_now else 0
def crypt_shade(c, k):
    return (min(255, int(c[0] * k)), min(255, int(c[1] * k)), min(255, int(c[2] * k)))
def crypt_light(g, i, d):
    if g.blackout:
        base = 0.0
    elif g.power:
        base = max(0.35, 1.0 - d / 14)
    else:
        base = 0.06
    if g.flash:
        off = abs(i - crypt_COLS / 2) / (crypt_COLS * 0.32)
        if off < 1:
            base += (1 - off) * max(0, 1 - d / 12) * (1.1 if not g.power else 0.35)
    return min(1.2, base)
def crypt_wall_detail(g, t, u, top, h, x, k):

    def band(v0, v1, c):
        y0 = int(top + h * (1 - v1))
        y1 = int(top + h * (1 - v0))
        if y1 - y0 >= 2:
            rect(x, max(0, y0), crypt_CWID, min(crypt_VH, y1) - max(0, y0), crypt_shade(c, k))
    if t in 'lkjCF':
        if u < 0.12 or u > 0.88:
            band(0, 0.8, (70, 48, 30))
        band(0.8, 1, crypt_WALL)
        if 0.7 < u < 0.85:
            band(0.42, 0.47, (210, 180, 90))
        if t in 'kC' and 0.12 < u < 0.3:
            on = t == 'C' and g.closet or False
            band(0.5, 0.6, (40, 40, 40))
            band(0.53, 0.57, (40, 200, 70) if on else (200, 40, 40) if g.power else (30, 30, 30))
        if t == 'F' and g.locked and (0.15 < u < 0.25):
            band(0.6, 0.64, (255, 30, 40))
    elif t == 'S':
        for n in range(6):
            band(n * 0.14, n * 0.14 + 0.07, (95, 70, 45))
        if 0.2 < u < 0.8:
            band(0.25, 0.32, (150, 120, 80))
            band(0.55, 0.62, (150, 120, 80))
    elif t == 'B':
        for n in range(4):
            band(n * 0.25 + 0.02, n * 0.25 + 0.05, (70, 45, 25))
            cc = ((150, 50, 50), (50, 90, 150), (60, 130, 70), (170, 140, 60))[(int(u * 7) + n) % 4]
            band(n * 0.25 + 0.05, n * 0.25 + 0.2, cc)
    elif t == 'T':
        if 0.1 < u < 0.9:
            band(0.35, 0.7, (15, 15, 20) if not g.tv else (60, 90, 160))
    elif t == 'G':
        if 0.28 < u < 0.72:
            band(0, 0.85, (70, 45, 30))
            band(0.6, 0.75, (220, 210, 180))
            if 0.45 < u < 0.55:
                band(0.2, 0.55, (180, 150, 70))
                if not g.note:
                    band(0.25, 0.3, (240, 240, 230))
    elif t == 'P':
        if 0.3 < u < 0.6:
            band(0.38, 0.56, (130, 130, 135))
            if 0.4 < u < 0.5:
                band(0.44 if g.power else 0.48, 0.54 if g.power else 0.58, (40, 40, 40))
def crypt_colour(t):
    if t in 'lkjCF':
        return crypt_DOOR
    if t == 'S':
        return (120, 90, 60)
    if t == 'B':
        return (90, 60, 35)
    return crypt_WALL
def crypt_render(g):
    zb = [0] * crypt_COLS
    ca = math.cos(g.a)
    sa = math.sin(g.a)
    for i in range(crypt_COLS):
        cam = (i + 0.5) / crypt_COLS * 2 - 1
        rx = ca - sa * cam * crypt_FOV * 0.5 * 1.15
        ry = sa + ca * cam * crypt_FOV * 0.5 * 1.15
        mx = int(g.x)
        my = int(g.y)
        ddx = abs(1 / rx) if rx else 1000000000.0
        ddy = abs(1 / ry) if ry else 1000000000.0
        if rx < 0:
            sx = -1
            sdx = (g.x - mx) * ddx
        else:
            sx = 1
            sdx = (mx + 1 - g.x) * ddx
        if ry < 0:
            sy = -1
            sdy = (g.y - my) * ddy
        else:
            sy = 1
            sdy = (my + 1 - g.y) * ddy
        side = 0
        t = '#'
        for n in range(40):
            if sdx < sdy:
                sdx += ddx
                mx += sx
                side = 0
            else:
                sdy += ddy
                my += sy
                side = 1
            t = crypt_tile(mx, my)
            if t != '.' and (not (t == 'l' and g.living)):
                break
        d = sdx - ddx if side == 0 else sdy - ddy
        d = max(d, 0.05)
        zb[i] = d
        if side == 0:
            u = g.y + d * ry
        else:
            u = g.x + d * rx
        u -= int(u)
        h = int(crypt_VH * 1.35 / d)
        top = (crypt_VH - h) // 2
        x = i * crypt_CWID
        k = crypt_light(g, i, d) * (0.8 if side else 1.0)
        if top > 0:
            m = top // 2
            rect(x, 0, crypt_CWID, top, crypt_shade(crypt_CEIL, max(k, 0.3)))
            if m >= 2:
                rect(x, top - m, crypt_CWID, m, crypt_shade(crypt_CEIL, max(k, 0.3) * 0.8))
            rect(x, top + h, crypt_CWID, crypt_VH - top - h, crypt_shade(crypt_FLOOR, max(k, 0.25)))
            if m >= 2:
                rect(x, top + h, crypt_CWID, m, crypt_shade(crypt_FLOOR, max(k, 0.25) * 0.75))
                if m >= 6:
                    rect(x, top + h + m + m // 2, crypt_CWID, 1, crypt_shade(crypt_FLOOR, max(k, 0.25) * 0.85))
        rect(x, max(0, top), crypt_CWID, min(crypt_VH, top + h) - max(0, top), crypt_shade(crypt_colour(t), k))
        crypt_wall_detail(g, t, u, top, h, x, k)
    crypt_sprites(g, zb, ca, sa)
def crypt_sprites(g, zb, ca, sa):
    lst = []
    for sx, sy, kind in crypt_SPRITES:
        lst.append((sx, sy, kind))
    if g.ys_vis:
        lst.append((g.yx, g.yy, 'ys'))
    order = []
    for sx, sy, kind in lst:
        dx = sx - g.x
        dy = sy - g.y
        fwd = dx * ca + dy * sa
        if fwd < 0.2:
            continue
        side = -dx * sa + dy * ca
        order.append((fwd, side, kind))
    order.sort(reverse=True)
    for fwd, side, kind in order:
        cx = side / fwd / (crypt_FOV * 0.5 * 1.15)
        scol = (cx + 1) / 2 * crypt_COLS
        w = 0.45 if kind == 'ys' else crypt_SPR[kind][0]
        half = w / 2 / fwd / (crypt_FOV * 0.5 * 1.15) * crypt_COLS / 2
        h = crypt_VH * 1.35 / fwd
        top = (crypt_VH - h) / 2
        c0 = int(scol - half)
        c1 = int(scol + half) + 1
        k = 1.0 if kind == 'ys' else crypt_light(g, int(scol), fwd)
        for i in range(max(0, c0), min(crypt_COLS, c1)):
            if zb[i] < fwd:
                continue
            u = (i + 0.5 - (scol - half)) / (2 * half) if half > 0 else 0.5
            if u < 0 or u > 1:
                continue
            x = i * crypt_CWID
            if kind == 'ys':
                crypt_ys_column(x, (scol - half) * crypt_CWID, 2 * half * crypt_CWID, top, h)
                continue
            for u0, u1, v0, v1, c in crypt_SPR[kind][1]:
                if u0 <= u <= u1:
                    y0 = int(top + h * (1 - v1))
                    y1 = int(top + h * (1 - v0))
                    if y1 - y0 >= 2 and y0 < crypt_VH:
                        rect(x, max(0, y0), crypt_CWID, min(crypt_VH, y1) - max(0, y0), crypt_shade(c, k))
def crypt_bottom(g, prompt):
    if prompt == g.shown:
        return
    g.shown = prompt
    rect(0, crypt_VH, 320, 210 - crypt_VH, BLACK)
    text(4, crypt_VH + 15, crypt_room(g), GREY)
    if g.flash:
        text(250, crypt_VH + 15, 'LIGHT', GOLD)
    text(4, crypt_VH + 33, prompt[:31], WHITE)
crypt_YS = []
def crypt__poly_slabs(pts, kind, step, top=True, bottom=True):
    ys = [p[1] for p in pts]
    y = min(ys)
    n = len(pts)
    first = len(crypt_YS)
    while y < max(ys):
        yc = y + step / 2
        xs = []
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            if y1 <= yc < y2 or y2 <= yc < y1:
                xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
        if len(xs) >= 2:
            crypt_YS.append((min(xs) / 256, max(xs) / 256, 1 - (y + step) / 640, 1 - y / 640, kind))
        y += step
    for i, on in ((first, top), (len(crypt_YS) - 1, bottom)):
        if on and i < len(crypt_YS):
            u0, u1, v0, v1, k = crypt_YS[i]
            crypt_YS[i] = (u0, u1, v0, v1, 5)
def crypt__limb(pts, w, kind=0):
    for i in range(0, len(pts) - 2, 2):
        x1, y1, x2, y2 = (pts[i], pts[i + 1], pts[i + 2], pts[i + 3])
        n = max(1, int(abs(y2 - y1) / 8))
        for k in range(n):
            t0 = k / n
            t1 = (k + 1) / n
            xm = x1 + (x2 - x1) * (t0 + t1) / 2
            ya = y1 + (y2 - y1) * t0
            yb = y1 + (y2 - y1) * t1
            hw = w * 0.4 + abs(x2 - x1) / n / 3
            crypt_YS.append(((xm - hw) / 256, (xm + hw) / 256, 1 - max(ya, yb) / 640 - 0.004, 1 - min(ya, yb) / 640 + 0.004, kind))
def crypt__oval(cx, cy, rx, ry, kind, step, a=0.0):
    ca = math.cos(0.55)
    sa = math.sin(0.55)
    pts = []
    for i in range(16):
        t = 2 * math.pi * i / 16
        lx = cx + rx * math.cos(t) * math.cos(a) - ry * math.sin(t) * math.sin(a)
        ly = cy + rx * math.cos(t) * math.sin(a) + ry * math.sin(t) * math.cos(a)
        pts.append((140 + lx * ca - ly * sa, 50 + lx * sa + ly * ca))
    crypt__poly_slabs(pts, kind, step)
def crypt__build_ys():
    ca = math.cos(0.55)
    sa = math.sin(0.55)
    crypt__limb([128, 120, 132, 88, 140, 66], 11)
    crypt__poly_slabs([(98, 122), (128, 112), (160, 126), (150, 210), (146, 260), (110, 260), (106, 210)], 0, 8, True, False)
    hem = [(108, 250), (148, 250), (162, 330)]
    x = 162
    while x > 94:
        hem.append((x - 4.5, 330 + (18 if int(x) % 2 else 6)))
        x -= 9
    hem.append((94, 330))
    crypt__poly_slabs(hem, 0, 6, False, True)
    crypt__limb([118, 320, 112, 460, 120, 470, 108, 612, 98, 628], 9)
    crypt__limb([140, 320, 146, 462, 136, 474, 150, 610, 162, 630], 9)
    crypt__limb([100, 128, 84, 250, 92, 262, 76, 420], 7)
    crypt__limb([158, 128, 176, 248, 166, 262, 184, 410], 7)
    for x0, y0, sg in ((76, 420, -1), (184, 410, 1)):
        for f in range(5):
            crypt__limb([x0, y0, x0 + sg * (f * 4 - 6), y0 + 52 + f % 2 * 8, x0 + sg * (f * 5 - 4), y0 + 70 + f * 3], 2.6)
    hair = [(-18, -6), (-27, 30), (-24, 96), (-6, 70), (8, 100), (20, 60), (17, -6), (10, -24), (-10, -24)]
    crypt__poly_slabs([(140 + lx * ca - ly * sa, 50 + lx * sa + ly * ca) for lx, ly in hair], 0, 4)
    crypt__oval(0, 0, 17, 25, 0, 4)
    for ex, ey in ((137.2, 41.2), (149.1, 48.55)):
        crypt_YS.append(((ex - 2) / 256, (ex + 2) / 256, 1 - (ey + 2) / 640, 1 - (ey - 2) / 640, 4))
def crypt_ys_column(x, left, wid, top, h):
    if not crypt_YS:
        crypt__build_ys()
    x1 = x + crypt_CWID
    rim = max(1, int(wid * 0.015))
    eyes = []
    for p in (0, 1):
        for u0, u1, v0, v1, kind in crypt_YS:
            pa = int(left + u0 * wid)
            pb = int(left + u1 * wid) + 1
            if kind == 4:
                if p == 0:
                    eyes.append((pa, pb, v0, v1))
                continue
            if p == 1:
                if kind == 5:
                    continue
                pa += rim
                pb -= rim
            a = max(x, pa)
            b = min(x1, pb)
            if b - a < 1:
                continue
            y0 = max(0, int(top + h * (1 - v1)))
            y1 = min(crypt_VH, int(top + h * (1 - v0)) + 1)
            if y1 - y0 < 1:
                continue
            if p == 0:
                g = random.randint(190, 255)
                c = (g, g * 19 // 20, g * 9 // 10)
            else:
                g = random.randint(28, 62)
                c = (g, g, g + 8)
            rect(a, y0, b - a, y1 - y0, c)
    pts = []
    for pa, pb, v0, v1 in eyes:
        cy = int(top + h * (1 - (v0 + v1) / 2))
        if 2 <= cy <= crypt_VH - 4:
            pts.append(((pa + pb) // 2, cy))
    for f, c in ((0.03, (35, 80, 150)), (0.016, (80, 175, 245)), (0.006, (230, 250, 255))):
        r = max(1 if f > 0.01 else 0, int(wid * f))
        for cx, cy in pts:
            ea = max(x, cx - r)
            eb = min(x1, cx + r + 1)
            if eb - ea < 1:
                continue
            for dx in range(ea - cx, eb - cx):
                hh = int((r * r - dx * dx) ** 0.5)
                rect(cx + dx, max(0, cy - hh), 1, 2 * hh + 1, c)
def crypt_wrap(s, n=30):
    out = []
    for para in s.split('\n'):
        line = ''
        for w in para.split(' '):
            if len(line) + len(w) + 1 > n:
                out.append(line)
                line = w
            else:
                line = (line + ' ' + w).strip()
        out.append(line)
    return out
def crypt_page(title, body, color=WHITE):
    lines = crypt_wrap(body)
    per = 9
    for p in range(0, len(lines), per):
        cls()
        ctext(20, title, GOLD)
        y = 44
        for ln in lines[p:p + per]:
            text(10, y, ln, color)
            y += 17
        more = p + per < len(lines)
        text(10, 204, 'ENTER: more' if more else 'ENTER/CLEAR: close', GREY)
        while True:
            k = wkey()
            if k in (OK, CLR):
                break
        if k == CLR:
            return
def crypt_toast(g, lines):
    rbox(10, 50, 300, 30 + 18 * len(lines), 8, WHITE)
    y = 72
    for ln in lines:
        ctext(y, ln)
        y += 18
    while wkey() not in (OK, CLR):
        pass
    g.shown = None
def crypt_say(g, s):
    crypt_toast(g, crypt_wrap(s, 27))
def crypt_keypad(title, hint, n):
    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cls()
    ctext(20, title, GOLD)
    y = 42
    for ln in crypt_wrap(hint, 30):
        text(10, y, ln, GREY)
        y += 17
    typed = ''
    sel = 0
    while True:
        rect(60, 96, 200, 26, BLACK)
        s = ''
        for i in range(n):
            s += (typed[i] if i < len(typed) else '_') + ' '
        ctext(116, s.strip(), WHITE)
        for i in range(26):
            x = 4 + i % 13 * 24
            yy = 140 + i // 13 * 28
            c = GOLD if i == sel else WHITE
            rect(x, yy, 22, 24, BLACK)
            rbox(x, yy, 22, 24, 5, c)
            text(x + 6, yy + 18, abc[i], c)
        k = wkey()
        if k == LEFT:
            sel = (sel - 1) % 26
        elif k == RIGHT:
            sel = (sel + 1) % 26
        elif k in (UP, DOWN):
            sel = (sel + 13) % 26
        elif k == DEL:
            typed = typed[:-1]
        elif k == CLR:
            return None
        elif k == OK:
            typed += abc[sel]
            if len(typed) == n:
                return typed
def crypt_objective(g):
    if not g.power:
        t = 'It is pitch dark. Find the power switch by the front door.'
    elif not g.note:
        t = 'The door locked behind you. Look around the foyer.'
    elif not g.closet:
        t = "Decode Ivy's note. The coat closet keypad wants four letters."
    elif not g.living:
        t = 'Unlock the Living Room.'
    elif not g.tapheard:
        t = 'The TV in the Living Room switched itself on.'
    elif not g.notebook:
        t = "Decode the knocks. Ivy's notebook might explain them."
    else:
        t = 'Decode the knocks. The hallway keypad wants five letters.'
    if g.awake:
        t += '\nShe is awake. Stay quiet. Hide when the lights stutter.'
    return t
def crypt_short(g):
    if not g.power:
        return 'Find the power switch'
    if not g.note:
        return 'Look around the foyer'
    if not g.closet:
        return "Decode Ivy's note (DEL)"
    if not g.living:
        return 'Unlock the Living Room'
    if not g.tapheard:
        return 'The TV switched itself on'
    if not g.notebook:
        return "Find Ivy's notebook"
    return 'Hallway keypad: 5 letters'
def crypt_journal(g):
    body = crypt_objective(g)
    if g.note:
        body += "\n\nIvy's note: " + crypt_CIPHER + '\nMy name is the key.'
    if g.tapheard:
        body += '\n\nKnocks: 4-1 4-5 2-4 1-5 4-4'
    crypt_page('JOURNAL', body)
    if g.notebook:
        crypt_grid_page()
    g.shown = None
def crypt_grid_page():
    cls()
    ctext(20, "IVY'S NOTEBOOK", GOLD)
    text(10, 44, 'For talking through walls.', GREY)
    text(10, 61, 'Knocks: row, then column.', GREY)
    for r in range(5):
        text(110, 92 + r * 20, str(r + 1), GOLD)
        for c in range(5):
            if r == 0:
                text(140 + c * 24, 76, str(c + 1), GOLD)
            text(140 + c * 24, 92 + r * 20, crypt_TAPGRID[r][c])
    text(10, 204, 'I and J share a box.  ENTER', GREY)
    while wkey() not in (OK, CLR):
        pass
def crypt_facing(g):
    ca = math.cos(g.a)
    sa = math.sin(g.a)
    for n in range(1, 9):
        d = n * 0.2
        t = crypt_tile(g.x + ca * d, g.y + sa * d)
        if t != '.' and (not (t == 'l' and g.living)):
            return t
    best = None
    bd = 1.5
    for sx, sy, kind in crypt_SPRITES:
        dx = sx - g.x
        dy = sy - g.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < bd and (dx * ca + dy * sa) / max(dist, 0.01) > 0.8:
            best = kind
            bd = dist
    return best
def crypt_label(g, t):
    if t == 'P':
        return 'ENTER: power switch'
    if t == 'F':
        return 'ENTER: front door'
    if t == 'G':
        return 'ENTER: grandfather clock'
    if t == 'C':
        return 'ENTER: hide in closet' if g.closet else 'ENTER: closet keypad'
    if t == 'l':
        return 'ENTER: Living Room door'
    if t == 'k':
        return 'ENTER: hallway keypad'
    if t == 'j':
        return 'ENTER: dining room door'
    if t == 'S':
        return 'ENTER: grand staircase'
    if t == 'T':
        return 'ENTER: smart TV'
    if t == 'B':
        return 'ENTER: bookshelf'
    if t == 'table':
        return "ENTER: Ivy's notebook"
    if t in ('phone', 'desk', 'lamp', 'couch', 'rack', 'vase'):
        return 'ENTER: look'
    return ''
def crypt_use(g, t):
    if t == 'P':
        if g.power:
            return crypt_say(g, 'Power: on.')
        g.power = True
        for n in range(6):
            g.blackout = n % 2 == 0
            crypt_render(g)
        g.blackout = False
        crypt_say(g, 'CLUNK. Years of dust rattle in the wiring.')
        g.locked = True
        crypt_render(g)
        crypt_toast(g, ['ASHGROVE SMART HOME:', 'Welcome home.', 'Front door LOCKED.', 'You did not set that up.'])
    elif t == 'F':
        crypt_say(g, "SMART HOME: LOCKED. The handle doesn't move." if g.locked else 'The door is stuck. Swollen in its frame.')
    elif t == 'G':
        if not g.power:
            return crypt_say(g, 'Too dark to make it out. Get the lights on first.')
        g.note = True
        crypt_page("IVY'S NOTE", 'Folded paper, tucked behind the pendulum glass.\n\nDad never notices anything. Grandma taught me this one when I was six. My name is the key.\n\n' + crypt_CIPHER + '\n\n- I.V.Y.')
        g.armed = True
    elif t == 'C':
        if g.closet:
            return crypt_hide(g)
        if not g.power:
            return crypt_say(g, 'The keypad is dead.')
        a = crypt_keypad('COAT CLOSET KEYPAD', 'A brass keypad. Four letters.', 4)
        if a == 'ECHO':
            g.closet = True
            g.shown = None
            crypt_render(g)
            crypt_say(g, 'The closet clicks open. On a hook: a brass key tagged LIVING ROOM. You take it.')
        elif a:
            crypt_say(g, 'The keypad buzzes. Wrong code.')
    elif t == 'l':
        if not g.closet:
            return crypt_say(g, 'Locked. A brass keyhole, polished from use.')
        g.living = True
        crypt_render(g)
        crypt_say(g, 'The brass key turns. Stiff, then all at once.')
        g.tv = True
        crypt_say(g, 'Somewhere in the Living Room, a TV switches itself on.')
    elif t == 'j':
        crypt_say(g, 'Swollen shut in its frame.')
    elif t == 'S':
        crypt_say(g, 'Boarded, chained and padlocked. The padlock is engraved M.A.')
    elif t == 'B':
        crypt_say(g, "Books on radios, codes and moths. Mildred's, mostly.")
    elif t == 'T':
        if not g.power:
            return crypt_say(g, 'The TV is dark.')
        crypt_tv(g)
    elif t == 'table':
        g.notebook = True
        crypt_grid_page()
        crypt_page("IVY'S NOTEBOOK", "She can hear voices and screens. She's bad at knocks. I think it's too slow for her.\n\n- Ivy")
    elif t == 'phone':
        crypt_say(g, 'An old rotary phone. Silent. For now.')
    elif t == 'desk':
        crypt_say(g, "Mildred's desk. Pages and pages of dots and dashes.")
    elif t == 'lamp':
        crypt_say(g, 'An old brass floor lamp.')
    elif t == 'couch':
        crypt_say(g, 'The cushions still hold the shape of someone.')
    elif t == 'rack':
        crypt_say(g, "Coats on hooks. One is a child's raincoat.")
    elif t == 'vase':
        crypt_say(g, 'Dried flowers. They crumble when you breathe.')
    elif t == 'k':
        if not g.power:
            return crypt_say(g, 'The keypad is dark. No power.')
        a = crypt_keypad('ASHGROVE SMART LOCK', 'A sticky note in Ivy\'s writing: "the TV knows. listen."', 5)
        if a == 'QUIET':
            g.won = True
        elif a:
            crypt_say(g, 'The keypad buzzes. Wrong code.')
    g.shown = None
def crypt_tv(g):
    cls((10, 14, 30))
    ctext(24, 'ASHGROVE SMART TV', GOLD)
    text(10, 48, 'HDMI 3: for whoever comes next', GREY)
    text(10, 66, 'Then black. Then knocking.', GREY)
    y = 100
    x = 20
    for r, c in crypt_KNOCKS:
        for grp in (r, c):
            for n in range(grp):
                circ(x, y, 4, WHITE)
                x += 11
                pause(0.25)
            x += 10
        x += 14
        if x > 270:
            x = 20
            y += 24
    text(10, 170, '4-1  4-5  2-4  1-5  4-4', (160, 210, 255))
    text(10, 204, 'Written in your journal. ENTER', GREY)
    g.tapheard = True
    while wkey() not in (OK, CLR):
        pass
    if not g.awake:
        g.awake = True
        g.ytimer = 6
        crypt_page('...', 'The knocking stops.\nEvery screen in the house flickers at once.\n\nShe is awake. Hide when the lights stutter.', (200, 140, 140))
def crypt_hide(g):
    g.hidden = True
    cls()
    ctext(70, 'You squeeze into the coat', WHITE)
    ctext(90, 'closet. Breathe slowly.', WHITE)
    ctext(150, 'ENTER: step out', GREY)
    t0 = 0
    while True:
        k = key()
        if k == OK:
            break
        pause(0.2)
        t0 += 1
        if g.ystate == 'hunt' and t0 > 25:
            g.ystate = 'dormant'
            g.ys_vis = False
            g.ytimer = random.randint(35, 55)
            rect(0, 110, 320, 30, BLACK)
            ctext(130, "The static fades. She's gone.", GREY)
    g.hidden = False
    g.shown = None
def crypt_sighting(g):
    g.sighted = True
    g.yx, g.yy = (9.5, 1.0)
    for n in range(10):
        g.blackout = n < 3 and n % 2 == 0
        g.ys_vis = n >= 3
        g.yy = 1.0 + max(0, n - 3) * 0.08
        crypt_render(g)
        pause(0.2)
    g.ys_vis = False
    g.blackout = False
    crypt_render(g)
    crypt_say(g, '...it was a woman. Made of static. And she was looking at you.')
def crypt_ys_update(g, dt):
    if not g.awake or g.won:
        return
    if g.ystate == 'dormant':
        g.ytimer -= dt
        if g.ytimer <= 0:
            g.ystate = 'warn'
            g.ytimer = 4
            crypt_say(g, 'Static hisses somewhere in the house. The lights stutter.')
    elif g.ystate == 'warn':
        g.ytimer -= dt
        g.blackout = random.random() < 0.35
        if g.ytimer <= 0:
            g.blackout = False
            spots = ((2.5, 1.5), (9.5, 1.5), (2.5, 6.4), (11.5, 1.5), (6.5, 6.5))
            far = [p for p in spots if abs(p[0] - g.x) + abs(p[1] - g.y) > 5] or list(spots)
            g.yx, g.yy = random.choice(far)
            g.ystate = 'hunt'
            g.ys_vis = True
            g.ytimer = 28
    elif g.ystate == 'hunt':
        g.ytimer -= dt
        dx = g.x - g.yx
        dy = g.y - g.yy
        d = math.sqrt(dx * dx + dy * dy)
        sp = 0.55 * dt
        if d > 0.01:
            nx = g.yx + dx / d * sp
            ny = g.yy + dy / d * sp
            if not crypt_solid(g, nx, g.yy) or crypt_tile(nx, g.yy) in 'l':
                g.yx = nx
            if not crypt_solid(g, g.yx, ny):
                g.yy = ny
        g.blackout = d < 3 and random.random() < 0.25
        if d < 0.6:
            crypt_caught(g)
        elif g.ytimer <= 0:
            g.ystate = 'dormant'
            g.ys_vis = False
            g.blackout = False
            g.ytimer = random.randint(35, 55)
def crypt_caught(g):
    for n in range(8):
        for y in range(0, 176, 22):
            gv = random.randint(60, 230)
            rect(0, y, 320, 22, (gv, gv, gv))
    cls()
    ctext(90, 'She found you.', (220, 120, 120))
    ctext(130, 'ENTER', GREY)
    while wkey() not in (OK, CLR):
        pass
    g.x, g.y, g.a = (11.5, 5.5, math.pi)
    g.ystate = 'dormant'
    g.ys_vis = False
    g.blackout = False
    g.ytimer = 30
    g.shown = None
def crypt_ending():
    cls()
    ctext(40, 'enCRYPTed', (200, 60, 60))
    ctext(70, 'The keypad flashes green.')
    ctext(90, 'End of the demo.')
    ctext(125, 'Full game at', GOLD)
    ctext(147, crypt_LINK1, WHITE)
    ctext(167, crypt_LINK2, WHITE)
    ctext(203, 'CLEAR: leave', GREY)
    while wkey() != CLR:
        pass
def crypt_pause_menu(g):
    c = choose('PAUSED', ['Resume', 'Journal', 'Quit demo'])
    g.shown = None
    if c == 1:
        crypt_journal(g)
    return c == 2
def crypt_play():
    g = crypt_St()
    g.x, g.y, g.a = (9.5, 6.4, -math.pi / 2)
    g.power = g.locked = g.note = g.closet = g.living = g.tv = False
    g.tapheard = g.notebook = g.awake = g.armed = g.sighted = False
    g.flash = True
    g.blackout = False
    g.won = False
    g.hidden = False
    g.ys_vis = False
    g.ystate = 'dormant'
    g.ytimer = 0
    g.yx = g.yy = 0
    g.shown = None
    cls()
    crypt_page('enCRYPTed', 'Ashgrove Manor. Bought at government auction. Power off since the accident.\n\nIt is pitch dark. Find the power switch by the front door.')
    last = crypt_clock()
    dirty = True
    st = Steer((UP, DOWN), True)
    while not g.won:
        k = key()
        d = st.feed(k) if k not in (LEFT, RIGHT) else st.d
        t = crypt_clock()
        dt = t - last if crypt_now else 0.25
        last = t
        dt = max(0.02, min(dt, 0.5))
        moved = False
        if k == CLR:
            if crypt_pause_menu(g):
                return
            dirty = True
            continue
        if k == DEL:
            crypt_journal(g)
            dirty = True
            continue
        if k == SECOND:
            g.flash = not g.flash
            g.shown = None
            dirty = True
            while key() == SECOND:
                pass
        if k == LEFT:
            g.a -= 2.0 * max(dt, 0.25)
            moved = True
        elif k == RIGHT:
            g.a += 2.0 * max(dt, 0.25)
            moved = True
        if d == UP or d == DOWN:
            s = (1.6 if d == UP else -1.0) * dt
            nx = g.x + math.cos(g.a) * s
            ny = g.y + math.sin(g.a) * s
            r = 0.22 if s > 0 else -0.22
            ox, oy = (g.x, g.y)
            if not crypt_solid(g, nx + math.cos(g.a) * r, g.y):
                g.x = nx
            if not crypt_solid(g, g.x, ny + math.sin(g.a) * r):
                g.y = ny
            if abs(g.x - ox) + abs(g.y - oy) < 0.001:
                st.stop()
            moved = True
        elif k == OK:
            f = crypt_facing(g)
            if f:
                crypt_use(g, f)
                dirty = True
                while key() == OK:
                    pass
        if g.armed and (not g.sighted) and (crypt_room(g) == 'Grand Foyer'):
            look = math.atan2(1.0 - g.y, 9.5 - g.x)
            diff = (look - g.a + math.pi) % (2 * math.pi) - math.pi
            if abs(diff) < 0.35:
                crypt_sighting(g)
                st.stop()
                dirty = True
        before = g.ys_vis or g.blackout
        crypt_ys_update(g, dt)
        if moved or dirty or g.ys_vis or g.blackout or before:
            crypt_render(g)
            dirty = False
        f = crypt_facing(g)
        crypt_bottom(g, crypt_label(g, f) if f else crypt_short(g))
        if not moved:
            pause(0.03)
    crypt_ending()
crypt_RULES = "Explore Ashgrove Manor, solve Ivy's codes and hide from Ysolde when the lights stutter."
crypt_KEYS = ['Up/Down: start walking', 'Press the other one to stop', 'Left/Right: turn a step', 'ENTER: use  2nd: flashlight', 'DEL: journal  CLEAR: pause']
def crypt_main():
    while True:
        c = home('GHCRYPT', 'enCRYPTed DEMO', crypt_RULES, crypt_KEYS, ('Start', 'Back'))
        if c < 0:
            return
        crypt_play()
flap_GAP = 64
flap_TW = 26
flap_SKY = (110, 195, 240)
flap_TREE = (50, 140, 60)
flap_LEAF = (40, 115, 50)
flap_INK = (20, 20, 20)
def flap__bar(x, y, w, h, c):
    x0 = max(0, x)
    w = min(320, x + w) - x0
    if w >= 2 and h >= 1:
        rect(x0, y, w, h, c)
def flap__blob(x, y, r, c):
    if r <= x <= 319 - r:
        circ(x, y, r, c)
def flap_tree(x, gy, c):
    if x > 322 or x + flap_TW + 3 < 0:
        return
    hi = lt(c)
    lo = dk(c, 0.75)
    cx = x + flap_TW // 2
    top = gy + flap_GAP
    y0 = max(22, gy - 27)
    flap__bar(x - 3, y0, flap_TW + 9, gy + 1 - y0, flap_SKY)
    flap__bar(x - 3, top - 2, flap_TW + 9, min(26, 198 - top), flap_SKY)
    flap__bar(cx + 5, top + 18, 5, 196 - top - 18, flap_SKY)
    if gy - 14 > 22:
        flap__bar(x, 22, flap_TW, gy - 36, lo)
        flap__bar(x + 3, 22, flap_TW - 6, gy - 36, c)
    for bx, by, r in ((x + 5, gy - 18, 8), (x + flap_TW - 5, gy - 16, 8), (cx, gy - 9, 9)):
        if by - r >= 22:
            flap__blob(bx, by, r, c)
        else:
            flap__bar(bx - r, 22, 2 * r, by + r - 22, c)
    flap__blob(cx - 3, gy - 12, 3, hi)
    trunk = (110, 75, 40)
    flap__bar(cx - 5, top + 18, 10, 196 - top - 18, trunk)
    flap__bar(cx + 2, top + 18, 3, 196 - top - 18, dk(trunk))
    for bx, by, r in ((x + 5, top + 14, 8), (x + flap_TW - 5, top + 14, 8), (cx, top + 9, 10)):
        if by + r <= 196:
            flap__blob(bx, by, r, c)
        else:
            flap__bar(bx - r, by - r, 2 * r, 196 - by + r, c)
    flap__blob(cx - 3, top + 6, 3, hi)
    flap__blob(x + 6, top + 13, 2, hi)
def flap_bird(x, y, c, wing):
    if c == flap_SKY:
        rect(x - 8, max(22, y - 8), 20, 17, flap_SKY)
        return
    circ(x, y, 8, (170, 120, 20))
    circ(x, y, 7, c)
    rect(x - 7, y - 1 + wing, 6, 3, (255, 245, 190))
    circ(x + 3, y - 3, 3, WHITE)
    circ(x + 4, y - 3, 1, BLACK)
    rect(x + 7, y - 1, 5, 3, (245, 140, 30))
def flap_ground():
    rect(0, 196, 320, 5, (70, 170, 80))
    rect(0, 201, 320, 9, (120, 80, 40))
    for x in range(0, 320, 16):
        rect(x + 4, 197, 3, 1, (110, 200, 110))
        rect(x + 10, 198, 2, 2, (40, 120, 50))
        rect(x + 7, 204, 3, 2, (95, 60, 30))
        rect(x + 1, 207, 2, 2, (150, 105, 60))
def flap_game():
    cls(flap_SKY)
    flap_ground()
    rect(0, 20, 320, 2, flap_INK)
    trees = [[330, random.randint(40, 110)], [330 + 170, random.randint(40, 110)]]
    y = 100.0
    v = 0.0
    score = 0
    passed = [False, False]
    text(6, 17, 'Score 0', flap_INK)
    held = False
    wing = 0
    while True:
        k = key()
        if k == CLR:
            return
        if (k == UP or k == SECOND or k == OK) and (not held):
            v = -5.2
            wing = 3
        held = k in (UP, SECOND, OK)
        oy = y
        v = min(7, v + 0.55)
        y += v
        flap_bird(60, int(oy), flap_SKY, 0)
        for i in range(2):
            t = trees[i]
            flap__bar(t[0] + flap_TW - 1, 22, 6, 174, flap_SKY)
            t[0] -= 4
            if t[0] + flap_TW + 3 < 0:
                t[0] = 330
                t[1] = random.randint(40, 110)
                passed[i] = False
            flap_tree(t[0], t[1], flap_TREE)
            if not passed[i] and t[0] + flap_TW < 52:
                passed[i] = True
                score += 1
                rect(0, 0, 320, 20, flap_SKY)
                text(6, 17, 'Score ' + str(score), flap_INK)
        wing = max(0, wing - 1)
        flap_bird(60, int(y), YELLOW, wing)
        hit = y > 189 or y < 28
        for t in trees:
            if t[0] - 9 < 60 < t[0] + flap_TW + 9 and (not t[1] + 7 < y < t[1] + flap_GAP - 7):
                hit = True
        if hit:
            pause(0.4)
            message(['You passed ' + str(score) + ' trees.'], 'Crash!')
            return
flap_RULES = "Flap to fly through the gaps between the trees. Don't hit the trees or the ground."
flap_KEYS = ['Up, 2nd or ENTER: flap', 'CLEAR: quit']
def flap_main():
    while True:
        c = home('GHFLAP', 'WING IT', flap_RULES, flap_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        flap_game()
hang_WORDS = 'PLANET ROCKET GALAXY COMET ORBIT JUNGLE TIGER PARROT DOLPHIN OCTOPUS PENGUIN CASTLE DRAGON WIZARD KNIGHT PIRATE TREASURE ISLAND VOLCANO DESERT GLACIER THUNDER RAINBOW BLIZZARD TORNADO PUZZLE RIDDLE SECRET MYSTERY CIPHER LANTERN CANDLE MIRROR LADDER BASKET GUITAR TRUMPET VIOLIN PIANO DRUMS PENCIL ERASER NOTEBOOK BACKPACK LOCKER SCIENCE HISTORY ALGEBRA GEOMETRY CALCULUS PIZZA PANCAKE WAFFLE NOODLE BURRITO PRETZEL COOKIE MUFFIN BANANA AVOCADO'.split()
hang_ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
hang_INK = (20, 20, 20)
hang_POST = (225, 175, 20)
hang_USED = (190, 190, 190)
def hang_letter_box(i, used, sel):
    x = 4 + i % 13 * 24
    y = 150 + i // 13 * 28
    c = GOLD if i == sel else hang_USED if hang_ABC[i] in used else hang_INK
    rect(x, y, 22, 24, WHITE)
    rbox(x, y, 22, 24, 5, c, 2, WHITE)
    text(x + 6, y + 18, hang_ABC[i], c)
def hang_word_line(w, used):
    rect(120, 60, 200, 30, WHITE)
    s = ''
    for ch in w:
        s += (ch if ch in used else '_') + ' '
    text(310 - len(s) * 10, 85, s.strip(), hang_INK)
def hang_figure(n):
    if n == 0:
        rrect(0, 136, 120, 12, 5, (110, 180, 90))
        rect(0, 140, 120, 4, (80, 150, 70))
        rect(8, 132, 74, 6, hang_POST)
        rect(8, 136, 74, 2, dk(hang_POST, 0.75))
        rect(24, 18, 5, 116, hang_POST)
        rect(27, 18, 2, 116, dk(hang_POST, 0.75))
        rect(24, 18, 52, 5, hang_POST)
        rect(24, 21, 52, 2, dk(hang_POST, 0.75))
        col(hang_POST)
        for o in range(4):
            draw_line(29 + o, 44, 50 + o, 23)
        rect(72, 23, 3, 13, (140, 90, 40))
        return
    col(hang_INK)
    if n == 1:
        ring(73, 46, 10, hang_INK, 2, WHITE)
        return
    a = ((73, 56, 73, 95), (73, 65, 60, 82), (73, 65, 86, 82), (73, 95, 62, 118), (73, 95, 84, 118))[n - 2]
    for o in (0, 1):
        draw_line(a[0] + o, a[1], a[2] + o, a[3])
def hang_game():
    w = random.choice(hang_WORDS)
    used = ''
    bad = 0
    sel = 0
    cls(WHITE)
    hang_figure(0)
    for i in range(26):
        hang_letter_box(i, used, sel)
    hang_word_line(w, used)
    while True:
        done = True
        for ch in w:
            if ch not in used:
                done = False
        if done:
            message(['You got it: ' + w], 'You win!')
            return
        if bad >= 6:
            message(['The word was ' + w], 'Out of guesses')
            return
        k = wkey()
        old = sel
        if k == LEFT:
            sel = (sel - 1) % 26
        elif k == RIGHT:
            sel = (sel + 1) % 26
        elif k == UP or k == DOWN:
            sel = (sel + 13) % 26
        elif k == CLR:
            return
        elif k == OK and hang_ABC[sel] not in used:
            used += hang_ABC[sel]
            if hang_ABC[sel] in w:
                hang_word_line(w, used)
            else:
                bad += 1
                hang_figure(bad)
        hang_letter_box(old, used, sel)
        hang_letter_box(sel, used, sel)
hang_RULES = 'Guess the hidden word one letter at a time. Six wrong guesses and the game is over.'
hang_KEYS = ['Arrows: pick a letter', 'ENTER: guess it', 'CLEAR: quit']
def hang_main():
    while True:
        c = home('GHHANG', 'HANGMAN', hang_RULES, hang_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        hang_game()
merge_X0 = 90
merge_Y0 = 26
merge_S = 36
merge_BOARD = (187, 173, 160)
merge_TC = {0: (205, 193, 180), 2: (230, 225, 215), 4: (235, 220, 190), 8: (240, 170, 110), 16: (245, 140, 90), 32: (245, 110, 85), 64: (245, 80, 50), 128: (235, 205, 110), 256: (235, 200, 90), 512: (235, 195, 70), 1024: (235, 190, 50), 2048: (235, 185, 30)}
def merge_add(b):
    e = [i for i in range(16) if b[i] == 0]
    if e:
        b[random.choice(e)] = 4 if random.random() < 0.1 else 2
def merge_slide(row):
    r = [v for v in row if v]
    out = []
    pts = 0
    i = 0
    while i < len(r):
        if i + 1 < len(r) and r[i] == r[i + 1]:
            out.append(r[i] * 2)
            pts += r[i] * 2
            i += 2
        else:
            out.append(r[i])
            i += 1
    return (out + [0] * (4 - len(out)), pts)
def merge_move(b, d):
    pts = 0
    nb = b[:]
    for j in range(4):
        if d < 2:
            idx = [j * 4 + i for i in range(4)]
        else:
            idx = [i * 4 + j for i in range(4)]
        if d == 1 or d == 3:
            idx.reverse()
        row, p = merge_slide([b[i] for i in idx])
        pts += p
        for n in range(4):
            nb[idx[n]] = row[n]
    return (nb, pts)
def merge_draw(b, score):
    for i in range(16):
        v = b[i]
        x = merge_X0 + i % 4 * merge_S
        y = merge_Y0 + i // 4 * merge_S
        c = merge_TC.get(v, (235, 180, 20))
        rrect(x + 2, y + 4, merge_S - 4, merge_S - 5, 5, dk(c, 0.8))
        rrect(x + 2, y + 2, merge_S - 4, merge_S - 5, 5, c)
        if v:
            rect(x + 7, y + 4, merge_S - 14, 2, lt(c, 0.4))
        if v:
            s = str(v)
            if len(s) > 3:
                s = s[:2] + 'k' if v >= 10000 else s
            tc = (60, 55, 50) if v < 8 else WHITE
            text(x + merge_S // 2 - len(s) * 5, y + 25, s, tc)
    rect(0, 180, 320, 30, WHITE)
    rrect(110, 182, 100, 24, 6, merge_BOARD)
    ctext(200, 'Score ' + str(score), WHITE)
def merge_game():
    b = [0] * 16
    merge_add(b)
    merge_add(b)
    score = 0
    cls(WHITE)
    rrect(12, 34, 64, 64, 8, dk((235, 185, 30), 0.8))
    rrect(12, 32, 64, 64, 8, (235, 185, 30))
    text(24, 70, '2048', WHITE)
    text(12, 128, 'Join', (120, 110, 100))
    text(12, 146, 'same', (120, 110, 100))
    text(12, 164, 'tiles!', (120, 110, 100))
    text(250, 60, 'Arrows', (120, 110, 100))
    text(250, 78, 'slide', (120, 110, 100))
    rrect(merge_X0 - 4, merge_Y0 - 4, merge_S * 4 + 8, merge_S * 4 + 8, 8, merge_BOARD)
    merge_draw(b, score)
    won = False
    while True:
        k = wkey()
        d = {LEFT: 0, RIGHT: 1, UP: 2, DOWN: 3}.get(k, -1)
        if k == CLR:
            return
        if d < 0:
            continue
        nb, p = merge_move(b, d)
        if nb != b:
            b = nb
            score += p
            merge_add(b)
            merge_draw(b, score)
            if 2048 in b and (not won):
                won = True
                message(['You made 2048!', 'Keep going?'], 'Amazing!')
                cls(WHITE)
                rrect(merge_X0 - 4, merge_Y0 - 4, merge_S * 4 + 8, merge_S * 4 + 8, 8, merge_BOARD)
                merge_draw(b, score)
        stuck = True
        for dd in range(4):
            if merge_move(b, dd)[0] != b:
                stuck = False
        if stuck:
            message(['Final score ' + str(score)], 'No moves left')
            return
merge_RULES = 'Slide the tiles. Two tiles with the same number join into one. Try to make 2048!'
merge_KEYS = ['Arrows: slide all tiles', 'CLEAR: quit']
def merge_main():
    while True:
        c = home('GHMERGE', '2048', merge_RULES, merge_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        merge_game()
pong_PH = 36
pong_TOP = 24
pong_TABLE = (30, 85, 165)
pong_BALL = (250, 150, 40)
pong_LINE = (150, 190, 235)
def pong_net():
    col(pong_LINE)
    draw_circle(160, 117, 28)
    for y in range(pong_TOP + 2, 208, 14):
        rect(159, y, 2, 7, WHITE)
def pong_court():
    cls(pong_TABLE)
    rect(0, 207, 320, 3, pong_LINE)
    rect(0, pong_TOP + 1, 320, 1, pong_LINE)
    pong_net()
def pong_paddle(x, y, c):
    block(x, y, 6, pong_PH, c, 1)
    rect(x + 2, y + 4, 2, pong_PH - 8, lt(c, 0.5))
def pong_scores(a, b):
    rect(0, 0, 320, pong_TOP - 2, pong_TABLE)
    text(110, 18, str(a))
    text(200, 18, str(b), GOLD)
    rect(0, pong_TOP - 2, 320, 2, WHITE)
    text(14, 18, 'YOU', pong_LINE)
    text(250, 18, 'CALC', pong_LINE)
def pong_game():
    pong_court()
    me = cpu = 0
    py = cy = 100
    pong_scores(me, cpu)
    serve = 1
    while me < 7 and cpu < 7:
        bx, by = (160.0, 110.0)
        vx = 4.0 * serve
        vy = random.choice((-2.5, -1.5, 1.5, 2.5))
        pong_paddle(8, py, WHITE)
        pong_paddle(306, cy, GOLD)
        pause(0.5)
        st = Steer((UP, DOWN))
        while True:
            k = key()
            if k == CLR:
                return
            opy, ocy = (py, cy)
            d = st.feed(k)
            if d == UP:
                py = max(pong_TOP + 3, py - 6)
                if py == pong_TOP + 3:
                    st.stop()
            elif d == DOWN:
                py = min(206 - pong_PH, py + 6)
                if py == 206 - pong_PH:
                    st.stop()
            target = by - pong_PH / 2
            if vx > 0 and bx > 120:
                cy += max(-4, min(4, target - cy))
            cy = int(max(pong_TOP + 3, min(206 - pong_PH, cy)))
            obx, oby = (bx, by)
            bx += vx
            by += vy
            if by < pong_TOP + 6 or by > 202:
                vy = -vy
                by = max(pong_TOP + 6, min(202, by))
            if bx < 18 and vx < 0 and (py - 4 < by < py + pong_PH + 4):
                vx = min(9, -vx * 1.06)
                vy += (by - (py + pong_PH / 2)) / 6
                bx = 18
            if bx > 302 and vx > 0 and (cy - 4 < by < cy + pong_PH + 4):
                vx = max(-9, -vx * 1.06)
                vy += (by - (cy + pong_PH / 2)) / 6
                bx = 302
            rect(int(obx) - 4, int(oby) - 4, 9, 9, pong_TABLE)
            if opy != py:
                rect(8, opy, 6, pong_PH, pong_TABLE)
            if ocy != cy:
                rect(306, ocy, 6, pong_PH, pong_TABLE)
            if 126 < obx < 194:
                pong_net()
            if opy != py or 0 < obx < 24:
                pong_paddle(8, py, WHITE)
            if ocy != cy or 296 < obx < 320:
                pong_paddle(306, cy, GOLD)
            ball(int(bx), int(by), 4, pong_BALL)
            if bx < 0:
                cpu += 1
                serve = 1
                break
            if bx > 320:
                me += 1
                serve = -1
                break
        rect(int(bx) - 4, int(by) - 4, 9, 9, pong_TABLE)
        pong_net()
        pong_scores(me, cpu)
    message(['You ' + str(me) + ' - ' + str(cpu) + ' Calculator'], 'You win!' if me > cpu else 'Calculator wins')
pong_RULES = "Bounce the ball past the calculator's paddle. First to 7 points wins."
pong_KEYS = ['Up/Down: paddle glides that way', 'ENTER: stop the paddle', 'CLEAR: quit']
def pong_main():
    while True:
        c = home('GHPONG', 'PONG', pong_RULES, pong_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        pong_game()
rpg_T = 20
rpg_MAPS = (['TTTTTTTTTTTTTTTT', 'T......TT......T', 'T.HH...........T', 'T.HH....C......T', 'T..............>', 'T....~~~.......>', 'T....~~~...TT..T', 'T..........TT..T', 'T..............T', 'TTTTTTTTTTTTTTTT'], ['TTTTTTTTTTTTTTTT', 'T..T....TT...T.T', 'T..T.C..TT...T.T', '<......T.....T.T', '<..TT..T..T....>', 'T..TT.....T....>', 'T.....T...TTT..T', 'T.TT..T.C......T', 'T.TT..T........T', 'TTTTTTTTTTTTTTTT'], ['################', '#::::#:::::::::#', '#::C:#:###:###:#', '<::::#:#:::#:::#', '<::::::#:B:#:::#', '#::#####:::#:#:#', '#::::::::::::#:#', '#:####:#####:#:#', '#:::::::C::::::#', '################'])
rpg_NAMES = ('Meadow', 'Whisper Woods', 'Hollow Cave')
rpg_FOES = ((), (('Slime', 12, 4, 1, 6, (80, 200, 90)), ('Bat', 10, 5, 0, 7, (120, 90, 160))), (('Bone Rat', 18, 7, 2, 12, (220, 220, 200)), ('Cave Eye', 22, 8, 3, 15, (200, 60, 60))))
rpg_BOSS = ('Hollow King', 70, 12, 4, 0, (110, 80, 180))
rpg_GRASS = (40, 110, 50)
rpg_STONE = (60, 55, 50)
def rpg_grass(px, py, x, y):
    rect(px, py, rpg_T, rpg_T, rpg_GRASS)
    h = (x * 7 + y * 13) % 5
    rect(px + 3 + h * 2, py + 5 + h, 1, 3, (70, 150, 70))
    rect(px + 5 + h * 2, py + 6 + h, 1, 2, (70, 150, 70))
    rect(px + 13 - h, py + 14 - h, 1, 3, (30, 90, 40))
    if h == 2:
        rect(px + 14, py + 4, 2, 2, (240, 220, 90))
    elif h == 4:
        rect(px + 4, py + 15, 2, 2, (230, 120, 160))
def rpg_floor(px, py, x, y):
    rect(px, py, rpg_T, rpg_T, rpg_STONE)
    o = 0 if y % 2 else 10
    rect(px, py, rpg_T, 1, (45, 40, 38))
    rect(px + o, py, 1, rpg_T, (45, 40, 38))
    rect(px + 2, py + 2, 6, 1, (75, 70, 64))
def rpg_tile(m, x, y, ch):
    px = x * rpg_T
    py = 20 + y * rpg_T
    if ch in '.>< ':
        rpg_grass(px, py, x, y)
    elif ch == 'T':
        rpg_grass(px, py, x, y)
        rect(px + 8, py + 12, 4, 7, (90, 60, 30))
        rect(px + 10, py + 12, 2, 7, (65, 42, 22))
        circ(px + 10, py + 8, 8, (20, 70, 30))
        circ(px + 9, py + 7, 6, (35, 100, 45))
        rect(px + 6, py + 4, 3, 2, (70, 150, 70))
    elif ch == '~':
        rect(px, py, rpg_T, rpg_T, (40, 90, 190))
        o = (x * 5 + y * 3) % 8
        rect(px + o, py + 6, 6, 1, (110, 160, 235))
        rect(px + (o + 9) % 14, py + 14, 5, 1, (110, 160, 235))
    elif ch == 'H':
        rpg_grass(px, py, x, y)
        rect(px + 2, py + 8, 16, 12, (200, 170, 120))
        rect(px + 2, py + 18, 16, 2, (160, 130, 90))
        col((170, 50, 40))
        fill_poly([px, px + 10, px + 20], [py + 9, py, py + 9])
        col((120, 35, 30))
        draw_line(px + 10, py, px + 20, py + 9)
        rect(px + 8, py + 13, 4, 7, (90, 60, 30))
        rect(px + 4, py + 11, 3, 3, (250, 230, 140))
        rect(px + 13, py + 11, 3, 3, (250, 230, 140))
    elif ch == 'C':
        if m < 2:
            rpg_grass(px, py, x, y)
        else:
            rpg_floor(px, py, x, y)
        rect(px + 3, py + 6, 14, 11, (60, 40, 20))
        rect(px + 4, py + 7, 12, 9, (160, 110, 40))
        rect(px + 4, py + 7, 12, 2, (190, 140, 60))
        rect(px + 4, py + 10, 12, 2, GOLD)
        rect(px + 9, py + 11, 2, 3, GOLD)
    elif ch == 'c':
        if m < 2:
            rpg_grass(px, py, x, y)
        else:
            rpg_floor(px, py, x, y)
        rect(px + 4, py + 10, 12, 6, (100, 70, 30))
        rect(px + 4, py + 10, 12, 1, (130, 95, 45))
    elif ch == '#':
        rect(px, py, rpg_T, rpg_T, (30, 28, 35))
        o = 0 if y % 2 else 5
        for yy in (0, 7, 14):
            rect(px, py + yy, rpg_T, 1, (50, 47, 58))
        for xx in (o, o + 10):
            rect(px + xx, py, 1, 6, (50, 47, 58))
            rect(px + (xx + 5) % rpg_T, py + 7, 1, 6, (50, 47, 58))
    elif ch == ':':
        rpg_floor(px, py, x, y)
    elif ch == 'B':
        rpg_floor(px, py, x, y)
        circ(px + 10, py + 11, 8, (80, 55, 140))
        circ(px + 10, py + 10, 8, (110, 80, 180))
        col(GOLD)
        fill_poly([px + 3, px + 6, px + 10, px + 14, px + 17], [py + 4, py - 1, py + 3, py - 1, py + 4])
        rect(px + 5, py + 8, 3, 3, RED)
        rect(px + 12, py + 8, 3, 3, RED)
        rect(px + 6, py + 14, 8, 1, (40, 25, 70))
def rpg_hero(x, y):
    px = x * rpg_T
    py = 20 + y * rpg_T
    rect(px + 5, py + 18, 10, 2, (25, 60, 30))
    circ(px + 10, py + 5, 4, (240, 200, 160))
    rect(px + 6, py + 1, 8, 3, (120, 70, 30))
    rect(px + 8, py + 5, 1, 1, BLACK)
    rect(px + 11, py + 5, 1, 1, BLACK)
    rect(px + 6, py + 9, 8, 7, (60, 120, 230))
    rect(px + 6, py + 13, 8, 1, (120, 80, 40))
    rect(px + 6, py + 16, 3, 4, (60, 40, 30))
    rect(px + 11, py + 16, 3, 4, (60, 40, 30))
    rect(px + 15, py + 4, 2, 11, (210, 215, 225))
    rect(px + 14, py + 12, 4, 2, GOLD)
def rpg_draw_map(g):
    m = g.m
    for y in range(10):
        for x in range(16):
            rpg_tile(m, x, y, g.maps[m][y][x])
    rpg_hero(g.x, g.y)
    rpg_hud(g)
def rpg_hud(g):
    rect(0, 0, 320, 20, BLACK)
    text(4, 15, rpg_NAMES[g.m][:13], GOLD)
    text(140, 15, 'HP' + str(g.hp) + '/' + str(g.mhp))
    text(240, 15, 'LV' + str(g.lv) + ' P' + str(g.pot))
class rpg_Game:
    pass
def rpg_bar(x, y, w, v, mx, c):
    rect(x, y, w, 6, DARK)
    if v > 0:
        rect(x, y, max(2, int(w * v / mx)), 6, c)
def rpg_foe_art(f):
    c = f[5]
    n = f[0]
    if n == 'Slime':
        circ(220, 95, 30, c)
        rect(190, 95, 60, 30, c)
    elif n == 'Bat':
        col(c)
        fill_poly([170, 220, 270, 220], [80, 100, 80, 120])
        circ(220, 100, 12, c)
    elif n == 'Bone Rat':
        circ(220, 100, 22, c)
        circ(245, 85, 10, c)
        rect(170, 110, 30, 3, c)
    elif n == 'Cave Eye':
        circ(220, 95, 30, c)
        circ(220, 95, 14, WHITE)
        circ(220, 95, 6, BLACK)
    else:
        rect(195, 70, 50, 60, c)
        circ(220, 60, 18, c)
        col(GOLD)
        fill_poly([200, 205, 212, 220, 228, 235, 240], [45, 30, 42, 28, 42, 30, 45])
        rect(208, 55, 5, 5, RED)
        rect(227, 55, 5, 5, RED)
    if n == 'Slime':
        circ(210, 92, 3, BLACK)
        circ(230, 92, 3, BLACK)
    elif n == 'Bone Rat':
        circ(245, 83, 2, BLACK)
def rpg_battle(g, f):
    name, fhp, fat, fdf, xp = (f[0], f[1], f[2], f[3], f[4])
    mx = fhp
    cls()
    rbox(150, 30, 140, 120, 10, f[5], 2, BLACK)
    rpg_foe_art(f)
    ctext(26, name + ' appears!', GOLD)
    opts = ['Attack', 'Potion', 'Run']
    sel = 0
    log = ''
    while True:
        rect(0, 150, 320, 60, BLACK)
        rect(10, 40, 130, 100, BLACK)
        text(12, 56, 'You', WHITE)
        rpg_bar(12, 62, 120, g.hp, g.mhp, GREEN)
        text(12, 86, name[:12], f[5])
        rpg_bar(12, 92, 120, fhp, mx, RED)
        for i in range(3):
            c = GOLD if i == sel else WHITE
            rbox(10 + i * 102, 154, 96, 24, 8, c)
            text(58 + i * 102 - len(opts[i]) * 5, 172, opts[i], c)
        text(10, 202, log[:31], GREY)
        k = wkey()
        if k == LEFT:
            sel = (sel - 1) % 3
            continue
        if k == RIGHT:
            sel = (sel + 1) % 3
            continue
        if k != OK:
            continue
        if sel == 0:
            d = max(1, g.atk + random.randint(0, 3) - fdf)
            fhp -= d
            log = 'You hit for ' + str(d) + '.'
        elif sel == 1:
            if g.pot == 0:
                log = 'No potions left.'
                continue
            g.pot -= 1
            g.hp = min(g.mhp, g.hp + 25)
            log = 'You feel better.'
        elif f is rpg_BOSS:
            log = "You can't run from him!"
        elif random.random() < 0.6:
            return True
        else:
            log = "Couldn't get away."
        if fhp <= 0:
            g.xp += xp
            msg = ['You won. +' + str(xp) + ' XP']
            while g.xp >= g.lv * 12:
                g.xp -= g.lv * 12
                g.lv += 1
                g.mhp += 8
                g.atk += 2
                g.dfn += 1
                g.hp = g.mhp
                msg.append('Level up! LV ' + str(g.lv))
            message(msg, name + ' defeated')
            return True
        d = max(1, fat + random.randint(0, 3) - g.dfn)
        g.hp -= d
        log = log + ' It hits ' + str(d) + '.'
        if g.hp <= 0:
            message(['You fainted...'], 'Game over')
            return False
def rpg_play():
    g = rpg_Game()
    g.maps = [[list(r) for r in mp] for mp in rpg_MAPS]
    g.m = 0
    g.x, g.y = (4, 4)
    g.hp = g.mhp = 30
    g.atk = 6
    g.dfn = 1
    g.lv = 1
    g.xp = 0
    g.pot = 1
    steps = 0
    cls()
    rpg_draw_map(g)
    message(['The Hollow King took', "the village's light.", 'Bring it back!'], 'TINY QUEST')
    rpg_draw_map(g)
    while True:
        k = wkey()
        if k == CLR:
            if message(['ENTER: quit adventure', 'CLEAR: keep going'], 'Quit?') == OK:
                return
            rpg_draw_map(g)
            continue
        dx, dy = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, -1), DOWN: (0, 1)}.get(k, (0, 0))
        if dx == 0 and dy == 0:
            continue
        nx, ny = (g.x + dx, g.y + dy)
        mp = g.maps[g.m]
        if nx >= 16 or nx < 0:
            g.m += 1 if nx >= 16 else -1
            g.x = 0 if nx >= 16 else 15
            rpg_draw_map(g)
            continue
        ch = mp[ny][nx]
        if ch in 'T~#':
            continue
        if ch == 'H':
            g.hp = g.mhp
            rpg_hud(g)
            message(['You rest by the fire.', 'HP restored.'], 'Cottage')
            rpg_draw_map(g)
            continue
        if ch == 'C':
            mp[ny][nx] = 'c'
            g.pot += 1
            message(['You found a potion!'], 'Chest')
            rpg_draw_map(g)
            continue
        if ch == 'B':
            if rpg_battle(g, rpg_BOSS):
                if g.hp > 0:
                    cls()
                    message(['The light returns to', 'the village. You did it!'], 'THE END')
                return
            return
        ox, oy = (g.x, g.y)
        g.x, g.y = (nx, ny)
        rpg_tile(g.m, ox, oy, mp[oy][ox])
        rpg_hero(g.x, g.y)
        steps += 1
        if rpg_FOES[g.m] and steps > 6 and (random.random() < 0.12):
            steps = 0
            if not rpg_battle(g, random.choice(rpg_FOES[g.m])):
                return
            rpg_draw_map(g)
rpg_RULES = 'Walk the meadow, woods and cave. Rest at the cottage, open chests for potions, and defeat the Hollow King.'
rpg_KEYS = ['Arrows: walk', 'Fights: Left/Right + ENTER', 'CLEAR: quit']
def rpg_main():
    while True:
        c = home('GHRPG', 'TINY QUEST', rpg_RULES, rpg_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        rpg_play()
simon_CX = 160
simon_CY = 116
simon_RO = 84
simon_RI = 36
simon_PADS = ((UP, 2, (30, 130, 50), (110, 255, 130)), (RIGHT, 3, (150, 30, 30), (255, 110, 110)), (DOWN, 0, (30, 60, 150), (120, 170, 255)), (LEFT, 1, (160, 130, 20), (255, 235, 100)))
simon_SHAPE = []
def simon_shapes():
    for q in range(4):
        xs = []
        ys = []
        for i in range(9):
            a = math.pi / 2 * (q + i / 8)
            xs.append(int(simon_CX + simon_RO * math.cos(a)))
            ys.append(int(simon_CY + simon_RO * math.sin(a)))
        for i in range(8, -1, -1):
            a = math.pi / 2 * (q + i / 8)
            xs.append(int(simon_CX + simon_RI * math.cos(a)))
            ys.append(int(simon_CY + simon_RI * math.sin(a)))
        simon_SHAPE.append((xs, ys))
def simon_gaps():
    d = (15, 15, 15)
    rect(simon_CX - 4, simon_CY - simon_RO - 1, 8, simon_RO - simon_RI + 1, d)
    rect(simon_CX - 4, simon_CY + simon_RI, 8, simon_RO - simon_RI + 1, d)
    rect(simon_CX - simon_RO - 1, simon_CY - 4, simon_RO - simon_RI + 1, 8, d)
    rect(simon_CX + simon_RI, simon_CY - 4, simon_RO - simon_RI + 1, 8, d)
    col(d)
    for r in (simon_RI, simon_RI + 1, simon_RI + 2):
        draw_circle(simon_CX, simon_CY, r)
def simon_pad(i, lit):
    k, q, dim, bright = simon_PADS[i]
    col(bright if lit else dim)
    xs, ys = simon_SHAPE[q]
    fill_poly(xs, ys)
    simon_gaps()
def simon_body():
    if not simon_SHAPE:
        simon_shapes()
    circ(simon_CX, simon_CY, simon_RO + 8, (60, 60, 65))
    circ(simon_CX, simon_CY, simon_RO + 5, (15, 15, 15))
    for i in range(4):
        simon_pad(i, False)
    ring(simon_CX, simon_CY, simon_RI, (15, 15, 15), 3, (70, 70, 75))
def simon_score(n):
    rect(0, 0, 320, 22, BLACK)
    text(6, 17, 'Score ' + str(n))
    text(204, 17, 'CLEAR quit', GREY)
    circ(simon_CX, simon_CY, simon_RI - 6, (25, 25, 28))
    s = str(n)
    text(simon_CX - len(s) * 5, simon_CY + 7, s, WHITE)
def simon_flash(i, t):
    simon_pad(i, True)
    pause(t)
    simon_pad(i, False)
    pause(0.12)
def simon_game():
    cls()
    simon_body()
    seq = []
    while True:
        simon_score(len(seq))
        seq.append(random.randint(0, 3))
        pause(0.5)
        t = max(0.18, 0.5 - len(seq) * 0.02)
        for i in seq:
            simon_flash(i, t)
        for want in seq:
            k = wkey()
            if k == CLR:
                return
            got = -1
            for i in range(4):
                if simon_PADS[i][0] == k:
                    got = i
            if got < 0:
                got = -2
            if got >= 0:
                simon_flash(got, 0.15)
            if got != want:
                if got >= 0:
                    pass
                message(['You got ' + str(len(seq) - 1) + ' in a row.'], 'Wrong color!')
                return
simon_RULES = 'Watch the colors light up, then repeat them in the same order. Each round adds one more.'
simon_KEYS = ['Up: green   Right: red', 'Down: blue  Left: yellow', 'CLEAR: quit']
def simon_main():
    while True:
        c = home('GHSIMON', 'SIMON', simon_RULES, simon_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        simon_game()
soli_CW = 40
soli_CHT = 30
soli_TOPY = 4
soli_TABY = 40
soli_RANKS = ('', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
soli_CARD = (245, 245, 240)
soli_BACK = (40, 80, 160)
soli_FELT = (15, 70, 40)
def soli_cx(c):
    return 6 + c * 44
def soli_suit(x, y, s):
    if s == 0:
        col(RED)
        fill_circle(x - 2, y - 1, 3)
        fill_circle(x + 2, y - 1, 3)
        fill_poly([x - 5, x + 5, x], [y, y, y + 5])
    elif s == 1:
        col(RED)
        fill_poly([x, x + 4, x, x - 4], [y - 5, y, y + 5, y])
    elif s == 2:
        col(BLACK)
        fill_circle(x - 2, y + 1, 3)
        fill_circle(x + 2, y + 1, 3)
        fill_poly([x - 5, x + 5, x], [y, y, y - 5])
        fill_rect(x - 1, y + 2, 2, 4)
    else:
        col(BLACK)
        fill_circle(x, y - 3, 2)
        fill_circle(x - 3, y + 1, 2)
        fill_circle(x + 3, y + 1, 2)
        fill_rect(x - 1, y + 2, 2, 4)
def soli_card(x, y, cd, h=soli_CHT, sel=False):
    if cd is None:
        rbox(x, y, soli_CW, soli_CHT, 4, GOLD if sel else (60, 110, 80), 2 if sel else 1, soli_FELT)
        return
    r, s, up = cd
    edge = GOLD if sel else BLACK
    e = 2 if sel else 1
    rrect(x, y, soli_CW, h, 4, edge)
    if not up:
        rrect(x + e, y + e, soli_CW - 2 * e, h - 2 * e, 3, soli_BACK)
        rect(x + 3, y + 3, soli_CW - 6, 1, lt(soli_BACK, 0.5))
        if h >= 12:
            rect(x + 4, y + 4, soli_CW - 8, h - 8, lt(soli_BACK, 0.15))
            for i in range(x + 6, x + soli_CW - 6, 6):
                rect(i, y + 6, 2, h - 12, soli_BACK)
        return
    rrect(x + e, y + e, soli_CW - 2 * e, h - 2 * e, 3, soli_CARD)
    t = soli_RANKS[r]
    text(x + 3, y + 15, t, RED if s < 2 else BLACK)
    soli_suit(x + 31 - (5 if len(t) > 1 else 0) + (5 if len(t) > 1 else 0), y + 9, s)
    if h >= soli_CHT:
        soli_suit(x + soli_CW // 2, y + 22, s)
class soli_G:
    pass
def soli_new():
    g = soli_G()
    deck = [[r, s, False] for s in range(4) for r in range(1, 14)]
    random.shuffle(deck)
    g.tab = []
    for c in range(7):
        pile = [deck.pop() for i in range(c + 1)]
        pile[-1][2] = True
        g.tab.append(pile)
    g.stock = deck
    g.waste = []
    g.found = [[], [], [], []]
    return g
def soli_gap(pile):
    n = len(pile)
    up = 12
    while n > 1 and soli_TABY + (n - 1) * up + soli_CHT > 208 and (up > 5):
        up -= 1
    return up
def soli_draw_col(g, c, cur, depth, held):
    x = soli_cx(c)
    rect(x, soli_TABY, soli_CW + 1, 210 - soli_TABY, soli_FELT)
    pile = g.tab[c]
    if not pile:
        soli_card(x, soli_TABY, None, soli_CHT, cur == 7 + c)
    up = soli_gap(pile)
    for i in range(len(pile)):
        cd = pile[i]
        sel = cur == 7 + c and i >= len(pile) - depth or (held and held[0] == 7 + c and (i >= len(pile) - held[1]))
        last = i == len(pile) - 1
        soli_card(x, soli_TABY + i * up, cd, soli_CHT if last else max(up + 4, 10), sel)
def soli_draw_top(g, cur, held):
    rect(0, 0, 320, soli_TABY - 2, soli_FELT)
    x = soli_cx(0)
    if g.stock:
        soli_card(x, soli_TOPY, [1, 0, False], soli_CHT, cur == 0)
    else:
        soli_card(x, soli_TOPY, None)
        if cur == 0:
            rbox(x, soli_TOPY, soli_CW, soli_CHT, 4, GOLD, 2, soli_FELT)
    x = soli_cx(1)
    if g.waste:
        soli_card(x, soli_TOPY, g.waste[-1], soli_CHT, cur == 1 or (held and held[0] == 1))
    else:
        soli_card(x, soli_TOPY, None, soli_CHT, cur == 1)
    for f in range(4):
        x = soli_cx(3 + f)
        p = g.found[f]
        if p:
            soli_card(x, soli_TOPY, p[-1], soli_CHT, cur == 3 + f)
        else:
            soli_card(x, soli_TOPY, None)
            if cur == 3 + f:
                rbox(x, soli_TOPY, soli_CW, soli_CHT, 4, GOLD, 2, soli_FELT)
            soli_suit(x + 20, soli_TOPY + 15, f)
def soli_fits_found(cd, f, pile):
    if cd[1] != f:
        return False
    return cd[0] == (pile[-1][0] + 1 if pile else 1)
def soli_fits_tab(cd, pile):
    if not pile:
        return cd[0] == 13
    t = pile[-1]
    return t[2] and t[0] == cd[0] + 1 and ((t[1] < 2) != (cd[1] < 2))
def soli_take(g, src, n):
    if src == 1:
        return [g.waste[-1]]
    return g.tab[src - 7][-n:]
def soli_remove(g, src, n):
    if src == 1:
        g.waste.pop()
    else:
        p = g.tab[src - 7]
        del p[-n:]
        if p and (not p[-1][2]):
            p[-1][2] = True
def soli_try_move(g, src, n, dst):
    cards = soli_take(g, src, n)
    if 3 <= dst <= 6:
        if n != 1 or not soli_fits_found(cards[0], dst - 3, g.found[dst - 3]):
            return False
        soli_remove(g, src, n)
        g.found[dst - 3].append(cards[0])
        return True
    if dst >= 7 and dst != src and soli_fits_tab(cards[0], g.tab[dst - 7]):
        soli_remove(g, src, n)
        g.tab[dst - 7].extend(cards)
        return True
    return False
def soli_faceup(g, c):
    n = 0
    for cd in g.tab[c]:
        if cd[2]:
            n += 1
    return n
def soli_game():
    g = soli_new()
    cls(soli_FELT)
    cur = 7
    depth = 1
    held = None
    redraw = list(range(7))
    top = True
    while True:
        if top:
            soli_draw_top(g, cur, held)
        for c in redraw:
            soli_draw_col(g, c, cur, depth if held is None else 0, held)
        redraw = []
        top = False
        if sum((len(f) for f in g.found)) == 52:
            message(['All 52 cards are home.'], 'You win!')
            return
        k = wkey()
        old = cur
        if k == CLR:
            if held:
                held = None
                redraw = list(range(7))
                top = True
                continue
            if message(['ENTER: quit this game', 'CLEAR: keep playing'], 'Quit?') == OK:
                return
            cls(soli_FELT)
            redraw = list(range(7))
            top = True
            continue
        if k == LEFT:
            cur = cur - 1 if cur not in (0, 7) else cur + 6
            if cur == 2:
                cur = 1
        elif k == RIGHT:
            cur = cur + 1 if cur not in (6, 13) else cur - 6
            if cur == 2:
                cur = 3
        elif k == DOWN and cur < 7:
            cur = 7 + (cur if cur != 1 else 1)
        elif k == UP and cur >= 7:
            if depth < soli_faceup(g, cur - 7) and held is None:
                depth += 1
            else:
                cur = cur - 7 if cur - 7 != 2 else 1
        elif k == DOWN and cur >= 7 and (depth > 1):
            depth -= 1
        elif k == OK:
            if held is None:
                if cur == 0:
                    if g.stock:
                        cd = g.stock.pop()
                        cd[2] = True
                        g.waste.append(cd)
                    else:
                        g.stock = g.waste[::-1]
                        for cd in g.stock:
                            cd[2] = False
                        g.waste = []
                    top = True
                elif cur == 1 and g.waste:
                    held = (1, 1)
                    top = True
                elif cur >= 7 and g.tab[cur - 7] and (soli_faceup(g, cur - 7) >= depth):
                    held = (cur, depth)
                    redraw.append(cur - 7)
            else:
                src, n = held
                held = None
                soli_try_move(g, src, n, cur)
                redraw = list(range(7))
                top = True
        elif k == SECOND and held is None:
            src = cur if cur == 1 or cur >= 7 else -1
            if src >= 0 and (src == 1 and g.waste or (src >= 7 and g.tab[src - 7])):
                for f in range(4):
                    if soli_try_move(g, src, 1, 3 + f):
                        break
                redraw = list(range(7))
                top = True
        if cur != old:
            depth = 1
            top = True
            if old >= 7:
                redraw.append(old - 7)
            if cur >= 7:
                redraw.append(cur - 7)
        elif k in (UP, DOWN) and cur >= 7:
            redraw.append(cur - 7)
soli_RULES = 'Build four piles from Ace to King, one per suit. In the columns, stack cards down in alternating colors.'
soli_KEYS = ['Arrows: move   ENTER: pick/put', 'Up/Down in a column: more cards', 'ENTER on the deck: draw', '2nd: send card to top piles', 'CLEAR: quit']
def soli_main():
    while True:
        c = home('GHSOLI', 'SOLITAIRE', soli_RULES, soli_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        soli_game()
sudoku_S = 20
sudoku_X0 = 20
sudoku_Y0 = 15
sudoku_INK = (20, 20, 20)
sudoku_PEN = (40, 90, 200)
def sudoku_make(holes):
    base = 3
    r = list(range(3))
    rows = [g * 3 + i for g in random.sample(r, 3) for i in random.sample(r, 3)]
    cols = [g * 3 + i for g in random.sample(r, 3) for i in random.sample(r, 3)]
    nums = random.sample(range(1, 10), 9)
    sol = [nums[(base * (rr % base) + rr // base + cc) % 9] for rr in rows for cc in cols]
    puz = sol[:]
    for i in random.sample(range(81), holes):
        puz[i] = 0
    return puz
def sudoku_valid(b):
    for i in range(9):
        row = set(b[i * 9:i * 9 + 9])
        colm = set(b[i::9])
        bx = i % 3 * 3 + i // 3 * 27
        box = set((b[bx + o] for o in (0, 1, 2, 9, 10, 11, 18, 19, 20)))
        for s in (row, colm, box):
            if s != set(range(1, 10)):
                return False
    return True
def sudoku_clash(b, i):
    v = b[i]
    if not v:
        return False
    r = i // 9
    c = i % 9
    for j in range(81):
        if j != i and b[j] == v:
            if j // 9 == r or j % 9 == c or (j // 27 == i // 27 and j % 9 // 3 == c // 3):
                return True
    return False
def sudoku_cell(b, fixed, i, cur):
    x = sudoku_X0 + i % 9 * sudoku_S
    y = sudoku_Y0 + i // 9 * sudoku_S
    bg = (250, 225, 140) if i == cur else (236, 238, 246) if fixed[i] else WHITE
    rect(x + 1, y + 1, sudoku_S - 2, sudoku_S - 2, bg)
    v = b[i]
    if v:
        c = sudoku_INK if fixed[i] else RED if sudoku_clash(b, i) else sudoku_PEN
        text(x + 5, y + 17, str(v), c)
def sudoku_grid():
    for i in range(10):
        c = sudoku_INK if i % 3 == 0 else (150, 150, 150)
        t = 2 if i % 3 == 0 else 1
        if t == 2:
            rect(sudoku_X0 + i * sudoku_S - 1, sudoku_Y0 - 1, 2, sudoku_S * 9 + 2, c)
            rect(sudoku_X0 - 1, sudoku_Y0 + i * sudoku_S - 1, sudoku_S * 9 + 2, 2, c)
        else:
            col(c)
            draw_line(sudoku_X0 + i * sudoku_S, sudoku_Y0, sudoku_X0 + i * sudoku_S, sudoku_Y0 + sudoku_S * 9)
            draw_line(sudoku_X0, sudoku_Y0 + i * sudoku_S, sudoku_X0 + sudoku_S * 9, sudoku_Y0 + i * sudoku_S)
def sudoku_game(holes):
    b = sudoku_make(holes)
    fixed = [v != 0 for v in b]
    cls(WHITE)
    sudoku_grid()
    rbox(208, 12, 106, 30, 8, sudoku_PEN, 2, (225, 235, 252))
    text(222, 33, 'SUDOKU', sudoku_PEN)
    text(214, 70, '0-9 type', GREY)
    text(214, 90, 'ENTER +1', GREY)
    text(214, 110, 'DEL erase', GREY)
    text(214, 130, 'CLEAR quit', GREY)
    cur = 0
    while fixed[cur]:
        cur += 1
    for i in range(81):
        sudoku_cell(b, fixed, i, cur)
    while True:
        k = wkey()
        old = cur
        if k == LEFT and cur % 9:
            cur -= 1
        elif k == RIGHT and cur % 9 < 8:
            cur += 1
        elif k == UP and cur > 8:
            cur -= 9
        elif k == DOWN and cur < 72:
            cur += 9
        elif k == CLR:
            return
        elif not fixed[cur]:
            v = -1
            if k in NUMS:
                v = NUMS[k]
            elif k == OK:
                v = b[cur] % 9 + 1
            elif k == DEL:
                v = 0
            if v >= 0:
                b[cur] = v
                for i in range(81):
                    if not fixed[i] and b[i]:
                        sudoku_cell(b, fixed, i, cur)
                if 0 not in b and sudoku_valid(b):
                    message(['Every row, column and', 'box is complete.'], 'Solved!')
                    return
        sudoku_cell(b, fixed, old, cur)
        sudoku_cell(b, fixed, cur, cur)
sudoku_RULES = 'Fill the grid so every row, column and 3x3 box has the numbers 1 to 9 once. Red numbers clash.'
sudoku_KEYS = ['Arrows: move', '0-9: type a number', 'ENTER: count up  DEL: erase', 'CLEAR: quit']
def sudoku_main():
    while True:
        c = home('GHSUDOKU', 'SUDOKU', sudoku_RULES, sudoku_KEYS, ('Easy', 'Medium', 'Hard', 'Back'))
        if c < 0:
            return
        sudoku_game((36, 46, 54)[c])
ttt_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
ttt_X0 = 85
ttt_Y0 = 28
ttt_S = 50
ttt_INK = (20, 20, 20)
def ttt_winner(b):
    for a, c, d in ttt_LINES:
        if b[a] and b[a] == b[c] == b[d]:
            return b[a]
    if 0 not in b:
        return 3
    return 0
def ttt_cpu(b):
    for who in (2, 1):
        for a, c, d in ttt_LINES:
            v = [b[a], b[c], b[d]]
            if v.count(who) == 2 and v.count(0) == 1:
                return (a, c, d)[v.index(0)]
    if b[4] == 0:
        return 4
    free = [i for i in (0, 2, 6, 8) if b[i] == 0]
    if not free:
        free = [i for i in range(9) if b[i] == 0]
    return random.choice(free)
def ttt_cell(b, i, cur):
    x = ttt_X0 + i % 3 * ttt_S
    y = ttt_Y0 + i // 3 * ttt_S
    rect(x + 3, y + 3, ttt_S - 6, ttt_S - 6, WHITE)
    if i == cur:
        rbox(x + 3, y + 3, ttt_S - 6, ttt_S - 6, 6, GOLD, 3, WHITE)
    m = b[i]
    if m == 1:
        col(ttt_INK)
        for o in (-1, 0, 1):
            draw_line(x + 12 + o, y + 12, x + ttt_S - 12 + o, y + ttt_S - 12)
            draw_line(x + ttt_S - 12 + o, y + 12, x + 12 + o, y + ttt_S - 12)
    elif m == 2:
        ring(x + ttt_S // 2, y + ttt_S // 2, 15, ttt_INK, 3, WHITE)
def ttt_grid():
    for i in (1, 2):
        rect(ttt_X0 + i * ttt_S - 1, ttt_Y0, 3, ttt_S * 3, ttt_INK)
        rect(ttt_X0, ttt_Y0 + i * ttt_S - 1, ttt_S * 3, 3, ttt_INK)
def ttt_status(s):
    rect(0, 186, 320, 24, WHITE)
    ctext(203, s, ttt_INK)
def ttt_game(vs_cpu):
    b = [0] * 9
    cls(WHITE)
    ttt_grid()
    cur = 4
    turn = 1
    for i in range(9):
        ttt_cell(b, i, cur)
    while True:
        w = ttt_winner(b)
        if w:
            msg = "It's a draw" if w == 3 else 'X wins!' if w == 1 else 'Calculator wins' if vs_cpu else 'O wins!'
            ttt_status(msg + ' - ENTER')
            while wkey() not in (OK, CLR):
                pass
            return
        if vs_cpu and turn == 2:
            ttt_status('Thinking...')
            pause(0.3)
            m = ttt_cpu(b)
            b[m] = 2
            ttt_cell(b, m, cur)
            turn = 1
            continue
        ttt_status(('X' if turn == 1 else 'O') + ' to move')
        k = wkey()
        old = cur
        if k == LEFT and cur % 3 > 0:
            cur -= 1
        elif k == RIGHT and cur % 3 < 2:
            cur += 1
        elif k == UP and cur > 2:
            cur -= 3
        elif k == DOWN and cur < 6:
            cur += 3
        elif k == CLR:
            return
        elif k == OK and b[cur] == 0:
            b[cur] = turn
            turn = 3 - turn
        ttt_cell(b, old, cur)
        ttt_cell(b, cur, cur)
ttt_RULES = 'Get three in a row (across, down or diagonal) before the other player. Play the calculator or pass to a friend.'
ttt_KEYS = ['Arrows: move', 'ENTER: place your mark', 'CLEAR: quit']
def ttt_main():
    while True:
        c = home('GHTTT', 'TIC-TAC-TOE', ttt_RULES, ttt_KEYS, ('vs Calc', '2 Players', 'Back'))
        if c < 0:
            return
        ttt_game(c == 0)
class _GameMod:

    def __init__(self, f):
        self.main = f
GAMES = {'GHANIM': anim_main, 'GHBLOCKS': blocks_main, 'GHBREAK': break_main, 'GHCRYPT': crypt_main, 'GHFLAP': flap_main, 'GHHANG': hang_main, 'GHMERGE': merge_main, 'GHPONG': pong_main, 'GHRPG': rpg_main, 'GHSIMON': simon_main, 'GHSOLI': soli_main, 'GHSUDOKU': sudoku_main, 'GHTTT': ttt_main}
mehub_CATS = [('Arcade', [('Wing It', 'GHFLAP'), ('Pong', 'GHPONG'), ('Breakout', 'GHBREAK')]), ('Puzzle', [('Stack Drop', 'GHBLOCKS'), ('2048', 'GHMERGE'), ('Sudoku', 'GHSUDOKU'), ('Simon', 'GHSIMON')]), ('Classics', [('Solitaire', 'GHSOLI'), ('Tic-Tac-Toe', 'GHTTT'), ('Hangman', 'GHHANG')]), ('Adventure', [('Tiny Quest', 'GHRPG'), ('Encrypted Demo', 'GHCRYPT')]), ('Create', [('Animation Studio', 'GHANIM')]), ('Settings', [('Key Test', '*keys'), ('Delete All Saves', '*wipe'), ('About', '*about')])]
mehub_BAR_Y = 34
mehub_BAR_H = 22
mehub_BAR_GAP = 27
def mehub_header():
    cls()
    ctext(22, 'GAMEHUB', WHITE)
def mehub_draw_bar(i, on):
    y = mehub_BAR_Y + i * mehub_BAR_GAP
    c = GOLD if on else WHITE
    rbox(50, y, 220, mehub_BAR_H, 9, c)
    ctext(y + 17, mehub_CATS[i][0], c)
def mehub_cat_screen(sel):
    mehub_header()
    for i in range(len(mehub_CATS)):
        mehub_draw_bar(i, i == sel)
    while True:
        k = wkey()
        old = sel
        if k == UP:
            sel = (sel - 1) % len(mehub_CATS)
        elif k == DOWN:
            sel = (sel + 1) % len(mehub_CATS)
        elif k == OK or k == RIGHT:
            return sel
        elif k == CLR:
            return -1
        if sel != old:
            mehub_draw_bar(old, False)
            mehub_draw_bar(sel, True)
def mehub_app_pos(i):
    return (50 + i % 4 * 73, 82 + i // 4 * 70)
def mehub_draw_app(app, i, on):
    x, y = mehub_app_pos(i)
    c = GOLD if on else WHITE
    try:
        ring(x, y, 27, c, 2, icons_bg(app[1]))
        icons_draw(app[1], x, y, WHITE)
    except Exception:
        ring(x, y, 27, c)
        ctext(y + 7, app[0][0], c, x)
def mehub_show_title(name):
    rect(0, 186, 320, 24, BLACK)
    ctext(203, name, GOLD)
def mehub_app_screen(ci, sel=0):
    cname, apps = mehub_CATS[ci]
    cls()
    rbox(90, 8, 140, 24, 9, WHITE)
    ctext(26, cname, WHITE)
    for i in range(len(apps)):
        mehub_draw_app(apps[i], i, i == sel)
    mehub_show_title(apps[sel][0])
    n = len(apps)
    while True:
        k = wkey()
        old = sel
        if k == LEFT:
            sel = (sel - 1) % n
        elif k == RIGHT:
            sel = (sel + 1) % n
        elif k == UP and sel >= 4:
            sel -= 4
        elif k == DOWN and sel + 4 < n:
            sel += 4
        elif k == OK:
            return sel
        elif k == CLR:
            return -1
        if sel != old:
            mehub_draw_app(apps[old], old, False)
            mehub_draw_app(apps[sel], sel, True)
            mehub_show_title(apps[sel][0])
def mehub_run_app(mod):
    if mod == '*keys':
        return mehub_key_test()
    if mod == '*wipe':
        return mehub_wipe()
    if mod == '*about':
        cls()
        message(['Game center for the', 'TI-84 Evo.', 'CLEAR goes back.'], 'GAMEHUB')
        return
    gc.collect()
    try:
        m = _GameMod(GAMES[mod])
        m.main()
    except Exception as e:
        cls()
        message([str(e)[:26], 'Is ' + mod + ' on the', 'calculator?'], 'Could not run')
    try:
        del sys.modules[mod]
    except Exception:
        pass
    m = None
    gc.collect()
def mehub_key_test():
    cls()
    ctext(30, 'KEY TEST', GOLD)
    ctext(60, 'Press any key to see')
    ctext(80, 'its code. CLEAR twice')
    ctext(100, 'in a row to leave.')
    last = 0
    while True:
        k = wkey()
        rect(60, 120, 200, 40, BLACK)
        ctext(150, 'Code: ' + str(k), WHITE)
        if k == CLR and last == CLR:
            return
        last = k
def mehub_wipe():
    cls()
    ctext(40, 'DELETE ALL SAVES', GOLD)
    ctext(70, 'This erases every')
    ctext(90, 'Animation Studio')
    ctext(110, 'animation.')
    ctext(150, 'ENTER: delete', RED)
    ctext(175, 'CLEAR: keep them')
    if wkey() != OK:
        return
    n = 0
    try:
        n = save_wipe()
    except Exception:
        pass
    cls()
    message([str(n) + ' save lists cleared.'], 'Done')
def mehub_main():
    ci = 0
    while True:
        ci = mehub_cat_screen(ci)
        if ci < 0:
            cls()
            return
        ai = 0
        while True:
            ai = mehub_app_screen(ci, ai)
            if ai < 0:
                break
            mehub_run_app(mehub_CATS[ci][1][ai][1])
mehub_main()
