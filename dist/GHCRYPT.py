# GHCRYPT from GAMEHUB, on its own. Run it.
from ti_draw import *
from ti_system import *
import time
import random
import math
UP = 25
DOWN = 34
LEFT = 24
RIGHT = 26
OK = 105
CLR = 45
DEL = 23
SECOND = 21
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (230, 180, 40)
GREY = (110, 110, 110)
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
icons_BG = {}
def icons_c_(c):
    set_color(c[0], c[1], c[2])
def icons_line(x1, y1, x2, y2, c, t=1):
    icons_c_(c)
    for o in range(t):
        draw_line(int(x1) + o, int(y1), int(x2) + o, int(y2))
def icons_hline(x1, x2, y, c, t=1):
    icons_c_(c)
    for o in range(t):
        draw_line(int(x1), int(y) + o, int(x2), int(y) + o)
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
icons_ICONS = {'GHCRYPT': icons_crypt}
def icons_bg(mod):
    return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
    f = icons_ICONS.get(mod)
    if f:
        f(x, y, c)
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
crypt_main()
