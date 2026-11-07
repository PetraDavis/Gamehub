# enCRYPTed demo for GAMEHUB. Based on Petra's game:
# full game at petradavis.github.io/Encrypted/?ysolde=1
# Up/Down walk, Left/Right turn, ENTER use, 2nd flashlight,
# DEL journal, CLEAR pause.
from GHLIB import *
import math
import random
try:
    from time import monotonic as now
except Exception:
    now = None

MAP = [
    "#BBBB###SSS###",
    "B....#.......#",
    "B............k",
    "#####G.......#",
    "#....#.......#",
    "T....l.......j",
    "#....#.......C",
    "########PF####",
]
VW = 320
VH = 172
COLS = 40
CWID = VW // COLS
FOV = 1.0
WALL = (75, 95, 99)
DOOR = (110, 75, 45)
FLOOR = (42, 36, 32)
CEIL = (16, 16, 18)
LINK1 = "petradavis.github.io/"
LINK2 = "Encrypted/?ysolde=1"
CIPHER = "LI WKH OLJKWV GLH VKH LV LQ WKH URRP. GRQW UXQ. KLGH LQ WKH FRDW FORVHW. LWV FRGH LV HFKR"
TAPGRID = ("ABCDE", "FGHIK", "LMNOP", "QRSTU", "VWXYZ")
KNOCKS = ((4, 1), (4, 5), (2, 4), (1, 5), (4, 4))


class St:
    pass


# ---------- sprites: kind -> width, list of (u0, u1, v0, v1, color) ----------
SPR = {
    "couch": (1.3, ((0, 1, 0, .2, (150, 40, 45)), (.08, .92, .2, .36, (120, 30, 35)),
                    (0, .12, .2, .28, (150, 40, 45)), (.88, 1, .2, .28, (150, 40, 45)))),
    "table": (0.9, ((0, .12, 0, .28, (95, 65, 40)), (.88, 1, 0, .28, (95, 65, 40)),
                    (0, 1, .28, .33, (120, 85, 50)), (.3, .7, .33, .37, (140, 70, 180)))),
    "phone": (0.6, ((0, .15, 0, .3, (95, 65, 40)), (.85, 1, 0, .3, (95, 65, 40)),
                    (0, 1, .3, .34, (120, 85, 50)), (.25, .75, .34, .42, (20, 20, 20)))),
    "lamp": (0.6, ((.45, .55, 0, .55, (180, 150, 70)), (.15, .85, .55, .72, (235, 220, 170)))),
    "desk": (1.2, ((0, .1, 0, .3, (95, 65, 40)), (.9, 1, 0, .3, (95, 65, 40)),
                   (0, 1, .3, .35, (120, 85, 50)), (.2, .5, .35, .38, (200, 190, 150)))),
    "rack": (0.7, ((.46, .54, 0, .8, (80, 55, 35)), (.15, .45, .35, .75, (60, 70, 110)),
                   (.55, .85, .4, .72, (110, 50, 50)))),
    "vase": (0.7, ((.1, .9, 0, .25, (95, 65, 40)), (.35, .65, .25, .45, (60, 120, 140)),
                   (.3, .7, .45, .55, (90, 140, 70)))),
}
SPRITES = [
    (3.3, 5.5, "couch"), (1.9, 4.6, "table"), (4.4, 6.4, "phone"), (1.0, 6.5, "lamp"),
    (2.6, 1.5, "desk"), (12.4, 4.9, "rack"), (6.5, 1.4, "vase"),
]
ROOMS = (("Library", 0, 0, 5, 3), ("Living Room", 0, 3, 5, 8), ("Grand Foyer", 5, 0, 14, 8))


def tile(x, y):
    if 0 <= y < len(MAP) and 0 <= int(x) < 14:
        return MAP[int(y)][int(x)]
    return "#"


def solid(g, x, y):
    t = tile(x, y)
    if t == "l" and g.living:
        return False
    return t != "."


def room(g):
    for n, x0, y0, x1, y1 in ROOMS:
        if x0 <= g.x < x1 and y0 <= g.y < y1:
            return n
    return "Grand Foyer"


def clock():
    return now() if now else 0


# ---------- drawing ----------
def shade(c, k):
    return (min(255, int(c[0] * k)), min(255, int(c[1] * k)), min(255, int(c[2] * k)))


def light(g, i, d):
    if g.blackout:
        base = 0.0
    elif g.power:
        base = max(0.35, 1.0 - d / 14)
    else:
        base = 0.06
    if g.flash:
        off = abs(i - COLS / 2) / (COLS * 0.32)
        if off < 1:
            base += (1 - off) * max(0, 1 - d / 12) * (1.1 if not g.power else 0.35)
    return min(1.2, base)


def wall_detail(g, t, u, top, h, x, k):
    def band(v0, v1, c):
        y0 = int(top + h * (1 - v1))
        y1 = int(top + h * (1 - v0))
        if y1 - y0 >= 2:
            rect(x, max(0, y0), CWID, min(VH, y1) - max(0, y0), shade(c, k))
    if t in "lkjCF":
        if u < .12 or u > .88:
            band(0, .8, (70, 48, 30))
        band(.8, 1, WALL)
        if .7 < u < .85:
            band(.42, .47, (210, 180, 90))
        if t in "kC" and .12 < u < .3:
            on = (t == "C" and g.closet) or False
            band(.5, .6, (40, 40, 40))
            band(.53, .57, (40, 200, 70) if on else (200, 40, 40) if g.power else (30, 30, 30))
        if t == "F" and g.locked and .15 < u < .25:
            band(.6, .64, (255, 30, 40))
    elif t == "S":
        for n in range(6):
            band(n * .14, n * .14 + .07, (95, 70, 45))
        if .2 < u < .8:
            band(.25, .32, (150, 120, 80))
            band(.55, .62, (150, 120, 80))
    elif t == "B":
        for n in range(4):
            band(n * .25 + .02, n * .25 + .05, (70, 45, 25))
            cc = ((150, 50, 50), (50, 90, 150), (60, 130, 70), (170, 140, 60))[(int(u * 7) + n) % 4]
            band(n * .25 + .05, n * .25 + .2, cc)
    elif t == "T":
        if .1 < u < .9:
            band(.35, .7, (15, 15, 20) if not g.tv else (60, 90, 160))
    elif t == "G":
        if .28 < u < .72:
            band(0, .85, (70, 45, 30))
            band(.6, .75, (220, 210, 180))
            if .45 < u < .55:
                band(.2, .55, (180, 150, 70))
                if not g.note:
                    band(.25, .3, (240, 240, 230))
    elif t == "P":
        if .3 < u < .6:
            band(.38, .56, (130, 130, 135))
            if .4 < u < .5:
                band(.44 if g.power else .48, .54 if g.power else .58, (40, 40, 40))


def colour(t):
    if t in "lkjCF":
        return DOOR
    if t == "S":
        return (120, 90, 60)
    if t == "B":
        return (90, 60, 35)
    return WALL


def render(g):
    zb = [0] * COLS
    ca = math.cos(g.a)
    sa = math.sin(g.a)
    for i in range(COLS):
        cam = (i + 0.5) / COLS * 2 - 1
        rx = ca - sa * cam * FOV * 0.5 * 1.15
        ry = sa + ca * cam * FOV * 0.5 * 1.15
        mx = int(g.x)
        my = int(g.y)
        ddx = abs(1 / rx) if rx else 1e9
        ddy = abs(1 / ry) if ry else 1e9
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
        t = "#"
        for n in range(40):
            if sdx < sdy:
                sdx += ddx
                mx += sx
                side = 0
            else:
                sdy += ddy
                my += sy
                side = 1
            t = tile(mx, my)
            if t != "." and not (t == "l" and g.living):
                break
        d = (sdx - ddx) if side == 0 else (sdy - ddy)
        d = max(d, 0.05)
        zb[i] = d
        if side == 0:
            u = g.y + d * ry
        else:
            u = g.x + d * rx
        u -= int(u)
        h = int(VH * 1.35 / d)
        top = (VH - h) // 2
        x = i * CWID
        k = light(g, i, d) * (0.8 if side else 1.0)
        if top > 0:
            rect(x, 0, CWID, top, shade(CEIL, max(k, .3)))
            rect(x, top + h, CWID, VH - top - h, shade(FLOOR, max(k, .25)))
        rect(x, max(0, top), CWID, min(VH, top + h) - max(0, top), shade(colour(t), k))
        wall_detail(g, t, u, top, h, x, k)
    sprites(g, zb, ca, sa)


def sprites(g, zb, ca, sa):
    lst = []
    for sx, sy, kind in SPRITES:
        lst.append((sx, sy, kind))
    if g.ys_vis:
        lst.append((g.yx, g.yy, "ys"))
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
        cx = (side / fwd) / (FOV * 0.5 * 1.15)
        scol = (cx + 1) / 2 * COLS
        w = 0.6 if kind == "ys" else SPR[kind][0]
        half = w / 2 / fwd / (FOV * 0.5 * 1.15) * COLS / 2
        h = VH * 1.35 / fwd
        top = (VH - h) / 2
        c0 = int(scol - half)
        c1 = int(scol + half) + 1
        k = 1.0 if kind == "ys" else light(g, int(scol), fwd)
        for i in range(max(0, c0), min(COLS, c1)):
            if zb[i] < fwd:
                continue
            u = (i + 0.5 - (scol - half)) / (2 * half) if half > 0 else .5
            if u < 0 or u > 1:
                continue
            x = i * CWID
            if kind == "ys":
                ys_column(x, (scol - half) * CWID, 2 * half * CWID, top, h)
                continue
            for u0, u1, v0, v1, c in SPR[kind][1]:
                if u0 <= u <= u1:
                    y0 = int(top + h * (1 - v1))
                    y1 = int(top + h * (1 - v0))
                    if y1 - y0 >= 2 and y0 < VH:
                        rect(x, max(0, y0), CWID, min(VH, y1) - max(0, y0), shade(c, k))


def bottom(g, prompt):
    if prompt == g.shown:
        return
    g.shown = prompt
    rect(0, VH, 320, 210 - VH, BLACK)
    text(4, VH + 15, room(g), GREY)
    if g.flash:
        text(250, VH + 15, "LIGHT", GOLD)
    text(4, VH + 33, prompt[:31], WHITE)


# Ysolde, drawn from the character sheet in the full game (a 256 x 640 picture):
# very thin and tall, small head tilted hard on a long neck, lank hair, short
# tattered dress, arms past the knees. Like the game's shader, her body is
# dark inside with faint blue-grey static, her outline glows with bright static,
# and two small cold blue eyes shine out of the dark. No face most of the time.
# Built once into thin slabs (u0, u1, v0, v1, kind); kind 4 is an eye.
YS = []


def _poly_slabs(pts, kind, step, top=True, bottom=True):
    ys = [p[1] for p in pts]
    y = min(ys)
    n = len(pts)
    first = len(YS)
    while y < max(ys):
        yc = y + step / 2
        xs = []
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            if (y1 <= yc < y2) or (y2 <= yc < y1):
                xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
        if len(xs) >= 2:
            YS.append((min(xs) / 256, max(xs) / 256, 1 - (y + step) / 640, 1 - y / 640, kind))
        y += step
    # the top and bottom slabs are outline too
    for i, on in ((first, top), (len(YS) - 1, bottom)):
        if on and i < len(YS):
            u0, u1, v0, v1, k = YS[i]
            YS[i] = (u0, u1, v0, v1, 5)


def _limb(pts, w, kind=0):
    for i in range(0, len(pts) - 2, 2):
        x1, y1, x2, y2 = pts[i], pts[i + 1], pts[i + 2], pts[i + 3]
        n = max(1, int(abs(y2 - y1) / 8))
        for k in range(n):
            t0 = k / n
            t1 = (k + 1) / n
            xm = x1 + (x2 - x1) * (t0 + t1) / 2
            ya = y1 + (y2 - y1) * t0
            yb = y1 + (y2 - y1) * t1
            hw = w * .4 + abs(x2 - x1) / n / 3
            YS.append(((xm - hw) / 256, (xm + hw) / 256, 1 - max(ya, yb) / 640 - .004, 1 - min(ya, yb) / 640 + .004, kind))


def _oval(cx, cy, rx, ry, kind, step, a=0.0):
    ca = math.cos(.55)
    sa = math.sin(.55)
    pts = []
    for i in range(16):
        t = 2 * math.pi * i / 16
        lx = cx + rx * math.cos(t) * math.cos(a) - ry * math.sin(t) * math.sin(a)
        ly = cy + rx * math.cos(t) * math.sin(a) + ry * math.sin(t) * math.cos(a)
        pts.append((140 + lx * ca - ly * sa, 50 + lx * sa + ly * ca))
    _poly_slabs(pts, kind, step)


def _build_ys():
    ca = math.cos(.55)
    sa = math.sin(.55)
    # body
    _limb([128, 120, 132, 88, 140, 66], 11)
    _poly_slabs([(98, 122), (128, 112), (160, 126), (150, 210), (146, 260), (110, 260), (106, 210)], 0, 8, True, False)
    hem = [(108, 250), (148, 250), (162, 330)]
    x = 162
    while x > 94:
        hem.append((x - 4.5, 330 + (18 if int(x) % 2 else 6)))
        x -= 9
    hem.append((94, 330))
    _poly_slabs(hem, 0, 6, False, True)
    _limb([118, 320, 112, 460, 120, 470, 108, 612, 98, 628], 9)
    _limb([140, 320, 146, 462, 136, 474, 150, 610, 162, 630], 9)
    _limb([100, 128, 84, 250, 92, 262, 76, 420], 7)
    _limb([158, 128, 176, 248, 166, 262, 184, 410], 7)
    for x0, y0, sg in ((76, 420, -1), (184, 410, 1)):
        for f in range(5):
            _limb([x0, y0, x0 + sg * (f * 4 - 6), y0 + 52 + (f % 2) * 8, x0 + sg * (f * 5 - 4), y0 + 70 + f * 3], 2.6)
    # lank hair hanging from the tilted head
    hair = [(-18, -6), (-27, 30), (-24, 96), (-6, 70), (8, 100), (20, 60), (17, -6), (10, -24), (-10, -24)]
    _poly_slabs([(140 + lx * ca - ly * sa, 50 + lx * sa + ly * ca) for lx, ly in hair], 0, 4)
    _oval(0, 0, 17, 25, 0, 4)
    for ex, ey in ((137.2, 41.2), (149.1, 48.55)):
        YS.append(((ex - 2) / 256, (ex + 2) / 256, 1 - (ey + 2) / 640, 1 - (ey - 2) / 640, 4))


def ys_column(x, left, wid, top, h):
    if not YS:
        _build_ys()
    x1 = x + CWID
    rim = max(1, int(wid * .03))
    eyes = []
    for p in (0, 1):
        for u0, u1, v0, v1, kind in YS:
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
            y1 = min(VH, int(top + h * (1 - v0)) + 1)
            if y1 - y0 < 1:
                continue
            if p == 0:
                g = random.randint(170, 255)
                c = (g * 4 // 5, g * 9 // 10, g)
            else:
                g = random.randint(0, 9)
                c = (6, 8, 12) if g < 7 else (40 + g * 4, 50 + g * 4, 62 + g * 4)
            rect(a, y0, b - a, y1 - y0, c)
    for pa, pb, v0, v1 in eyes:
        cx = (pa + pb) // 2
        cy = int(top + h * (1 - (v0 + v1) / 2))
        if x - 2 <= cx < x1 + 2 and 0 <= cy < VH - 2:
            ha = max(x, cx - 1)
            hb = min(x1, cx + 3)
            if hb - ha >= 1:
                rect(ha, cy - 1, hb - ha, 4, (40, 110, 210))
            if x <= cx < x1:
                rect(cx, cy, 2, 2, (230, 250, 255))


# ---------- text screens ----------
def wrap(s, n=30):
    out = []
    for para in s.split("\n"):
        line = ""
        for w in para.split(" "):
            if len(line) + len(w) + 1 > n:
                out.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
        out.append(line)
    return out


def page(title, body, color=WHITE):
    lines = wrap(body)
    per = 9
    for p in range(0, len(lines), per):
        cls()
        ctext(20, title, GOLD)
        y = 44
        for ln in lines[p:p + per]:
            text(10, y, ln, color)
            y += 17
        more = p + per < len(lines)
        text(10, 204, "ENTER: more" if more else "ENTER/CLEAR: close", GREY)
        while True:
            k = wkey()
            if k in (OK, CLR):
                break
        if k == CLR:
            return


def toast(g, lines):
    rbox(10, 50, 300, 30 + 18 * len(lines), 8, WHITE)
    y = 72
    for ln in lines:
        ctext(y, ln)
        y += 18
    while wkey() not in (OK, CLR):
        pass
    g.shown = None


def say(g, s):
    toast(g, wrap(s, 27))


def keypad(title, hint, n):
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cls()
    ctext(20, title, GOLD)
    y = 42
    for ln in wrap(hint, 30):
        text(10, y, ln, GREY)
        y += 17
    typed = ""
    sel = 0
    while True:
        rect(60, 96, 200, 26, BLACK)
        s = ""
        for i in range(n):
            s += (typed[i] if i < len(typed) else "_") + " "
        ctext(116, s.strip(), WHITE)
        for i in range(26):
            x = 4 + (i % 13) * 24
            yy = 140 + (i // 13) * 28
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


# ---------- story ----------
def objective(g):
    if not g.power:
        t = "It is pitch dark. Find the power switch by the front door."
    elif not g.note:
        t = "The door locked behind you. Look around the foyer."
    elif not g.closet:
        t = "Decode Ivy's note. The coat closet keypad wants four letters."
    elif not g.living:
        t = "Unlock the Living Room."
    elif not g.tapheard:
        t = "The TV in the Living Room switched itself on."
    elif not g.notebook:
        t = "Decode the knocks. Ivy's notebook might explain them."
    else:
        t = "Decode the knocks. The hallway keypad wants five letters."
    if g.awake:
        t += "\nShe is awake. Stay quiet. Hide when the lights stutter."
    return t


def short(g):
    if not g.power:
        return "Find the power switch"
    if not g.note:
        return "Look around the foyer"
    if not g.closet:
        return "Decode Ivy's note (DEL)"
    if not g.living:
        return "Unlock the Living Room"
    if not g.tapheard:
        return "The TV switched itself on"
    if not g.notebook:
        return "Find Ivy's notebook"
    return "Hallway keypad: 5 letters"


def journal(g):
    body = objective(g)
    if g.note:
        body += "\n\nIvy's note: " + CIPHER + "\nMy name is the key."
    if g.tapheard:
        body += "\n\nKnocks: 4-1 4-5 2-4 1-5 4-4"
    page("JOURNAL", body)
    if g.notebook:
        grid_page()
    g.shown = None


def grid_page():
    cls()
    ctext(20, "IVY'S NOTEBOOK", GOLD)
    text(10, 44, "For talking through walls.", GREY)
    text(10, 61, "Knocks: row, then column.", GREY)
    for r in range(5):
        text(110, 92 + r * 20, str(r + 1), GOLD)
        for c in range(5):
            if r == 0:
                text(140 + c * 24, 76, str(c + 1), GOLD)
            text(140 + c * 24, 92 + r * 20, TAPGRID[r][c])
    text(10, 204, "I and J share a box.  ENTER", GREY)
    while wkey() not in (OK, CLR):
        pass


def facing(g):
    # what is right in front of the player (tile char or sprite kind), within reach
    ca = math.cos(g.a)
    sa = math.sin(g.a)
    for n in range(1, 9):
        d = n * 0.2
        t = tile(g.x + ca * d, g.y + sa * d)
        if t != "." and not (t == "l" and g.living):
            return t
    best = None
    bd = 1.5
    for sx, sy, kind in SPRITES:
        dx = sx - g.x
        dy = sy - g.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < bd and (dx * ca + dy * sa) / max(dist, .01) > .8:
            best = kind
            bd = dist
    return best


def label(g, t):
    if t == "P":
        return "ENTER: power switch"
    if t == "F":
        return "ENTER: front door"
    if t == "G":
        return "ENTER: grandfather clock"
    if t == "C":
        return "ENTER: hide in closet" if g.closet else "ENTER: closet keypad"
    if t == "l":
        return "ENTER: Living Room door"
    if t == "k":
        return "ENTER: hallway keypad"
    if t == "j":
        return "ENTER: dining room door"
    if t == "S":
        return "ENTER: grand staircase"
    if t == "T":
        return "ENTER: smart TV"
    if t == "B":
        return "ENTER: bookshelf"
    if t == "table":
        return "ENTER: Ivy's notebook"
    if t in ("phone", "desk", "lamp", "couch", "rack", "vase"):
        return "ENTER: look"
    return ""


def use(g, t):
    if t == "P":
        if g.power:
            return say(g, "Power: on.")
        g.power = True
        for n in range(6):
            g.blackout = n % 2 == 0
            render(g)
        g.blackout = False
        say(g, "CLUNK. Years of dust rattle in the wiring.")
        g.locked = True
        render(g)
        toast(g, ["ASHGROVE SMART HOME:", "Welcome home.", "Front door LOCKED.", "You did not set that up."])
    elif t == "F":
        say(g, "SMART HOME: LOCKED. The handle doesn't move." if g.locked else "The door is stuck. Swollen in its frame.")
    elif t == "G":
        if not g.power:
            return say(g, "Too dark to make it out. Get the lights on first.")
        g.note = True
        page("IVY'S NOTE", "Folded paper, tucked behind the pendulum glass.\n\nDad never notices anything. Grandma taught me this one when I was six. My name is the key.\n\n" + CIPHER + "\n\n- I.V.Y.")
        g.armed = True
    elif t == "C":
        if g.closet:
            return hide(g)
        if not g.power:
            return say(g, "The keypad is dead.")
        a = keypad("COAT CLOSET KEYPAD", "A brass keypad. Four letters.", 4)
        if a == "ECHO":
            g.closet = True
            g.shown = None
            render(g)
            say(g, "The closet clicks open. On a hook: a brass key tagged LIVING ROOM. You take it.")
        elif a:
            say(g, "The keypad buzzes. Wrong code.")
    elif t == "l":
        if not g.closet:
            return say(g, "Locked. A brass keyhole, polished from use.")
        g.living = True
        render(g)
        say(g, "The brass key turns. Stiff, then all at once.")
        g.tv = True
        say(g, "Somewhere in the Living Room, a TV switches itself on.")
    elif t == "j":
        say(g, "Swollen shut in its frame.")
    elif t == "S":
        say(g, "Boarded, chained and padlocked. The padlock is engraved M.A.")
    elif t == "B":
        say(g, "Books on radios, codes and moths. Mildred's, mostly.")
    elif t == "T":
        if not g.power:
            return say(g, "The TV is dark.")
        tv(g)
    elif t == "table":
        g.notebook = True
        grid_page()
        page("IVY'S NOTEBOOK", "She can hear voices and screens. She's bad at knocks. I think it's too slow for her.\n\n- Ivy")
    elif t == "phone":
        say(g, "An old rotary phone. Silent. For now.")
    elif t == "desk":
        say(g, "Mildred's desk. Pages and pages of dots and dashes.")
    elif t == "lamp":
        say(g, "An old brass floor lamp.")
    elif t == "couch":
        say(g, "The cushions still hold the shape of someone.")
    elif t == "rack":
        say(g, "Coats on hooks. One is a child's raincoat.")
    elif t == "vase":
        say(g, "Dried flowers. They crumble when you breathe.")
    elif t == "k":
        if not g.power:
            return say(g, "The keypad is dark. No power.")
        a = keypad("ASHGROVE SMART LOCK", "A sticky note in Ivy's writing: \"the TV knows. listen.\"", 5)
        if a == "QUIET":
            g.won = True
        elif a:
            say(g, "The keypad buzzes. Wrong code.")
    g.shown = None


def tv(g):
    cls((10, 14, 30))
    ctext(24, "ASHGROVE SMART TV", GOLD)
    text(10, 48, "HDMI 3: for whoever comes next", GREY)
    text(10, 66, "Then black. Then knocking.", GREY)
    y = 100
    x = 20
    for r, c in KNOCKS:
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
    text(10, 170, "4-1  4-5  2-4  1-5  4-4", (160, 210, 255))
    text(10, 204, "Written in your journal. ENTER", GREY)
    g.tapheard = True
    while wkey() not in (OK, CLR):
        pass
    if not g.awake:
        g.awake = True
        g.ytimer = 6
        page("...", "The knocking stops.\nEvery screen in the house flickers at once.\n\nShe is awake. Hide when the lights stutter.", (200, 140, 140))


def hide(g):
    g.hidden = True
    cls()
    ctext(70, "You squeeze into the coat", WHITE)
    ctext(90, "closet. Breathe slowly.", WHITE)
    ctext(150, "ENTER: step out", GREY)
    t0 = 0
    while True:
        k = key()
        if k == OK:
            break
        pause(0.2)
        t0 += 1
        if g.ystate == "hunt" and t0 > 25:
            g.ystate = "dormant"
            g.ys_vis = False
            g.ytimer = random.randint(35, 55)
            rect(0, 110, 320, 30, BLACK)
            ctext(130, "The static fades. She's gone.", GREY)
    g.hidden = False
    g.shown = None


# ---------- Ysolde ----------
def sighting(g):
    g.sighted = True
    g.yx, g.yy = 9.5, 1.0
    for n in range(10):
        g.blackout = n < 3 and n % 2 == 0
        g.ys_vis = n >= 3
        g.yy = 1.0 + max(0, n - 3) * 0.08
        render(g)
        pause(0.2)
    g.ys_vis = False
    g.blackout = False
    render(g)
    say(g, "...it was a woman. Made of static. And she was looking at you.")


def ys_update(g, dt):
    if not g.awake or g.won:
        return
    if g.ystate == "dormant":
        g.ytimer -= dt
        if g.ytimer <= 0:
            g.ystate = "warn"
            g.ytimer = 4
            say(g, "Static hisses somewhere in the house. The lights stutter.")
    elif g.ystate == "warn":
        g.ytimer -= dt
        g.blackout = random.random() < 0.35
        if g.ytimer <= 0:
            g.blackout = False
            spots = ((2.5, 1.5), (9.5, 1.5), (2.5, 6.4), (11.5, 1.5), (6.5, 6.5))
            far = [p for p in spots if abs(p[0] - g.x) + abs(p[1] - g.y) > 5] or list(spots)
            g.yx, g.yy = random.choice(far)
            g.ystate = "hunt"
            g.ys_vis = True
            g.ytimer = 28
    elif g.ystate == "hunt":
        g.ytimer -= dt
        dx = g.x - g.yx
        dy = g.y - g.yy
        d = math.sqrt(dx * dx + dy * dy)
        sp = 0.55 * dt
        if d > 0.01:
            nx = g.yx + dx / d * sp
            ny = g.yy + dy / d * sp
            if not solid(g, nx, g.yy) or tile(nx, g.yy) in "l":
                g.yx = nx
            if not solid(g, g.yx, ny):
                g.yy = ny
        g.blackout = d < 3 and random.random() < 0.25
        if d < 0.6:
            caught(g)
        elif g.ytimer <= 0:
            g.ystate = "dormant"
            g.ys_vis = False
            g.blackout = False
            g.ytimer = random.randint(35, 55)


def caught(g):
    for n in range(8):
        for y in range(0, 176, 22):
            gv = random.randint(60, 230)
            rect(0, y, 320, 22, (gv, gv, gv))
    cls()
    ctext(90, "She found you.", (220, 120, 120))
    ctext(130, "ENTER", GREY)
    while wkey() not in (OK, CLR):
        pass
    g.x, g.y, g.a = 11.5, 5.5, math.pi
    g.ystate = "dormant"
    g.ys_vis = False
    g.blackout = False
    g.ytimer = 30
    g.shown = None


# ---------- main loop ----------
def ending():
    cls()
    ctext(40, "enCRYPTed", (200, 60, 60))
    ctext(70, "The keypad flashes green.")
    ctext(90, "End of the demo.")
    ctext(125, "Full game at", GOLD)
    ctext(147, LINK1, WHITE)
    ctext(167, LINK2, WHITE)
    ctext(203, "CLEAR: leave", GREY)
    while wkey() != CLR:
        pass


def pause_menu(g):
    c = choose("PAUSED", ["Resume", "Journal", "Quit demo"])
    g.shown = None
    if c == 1:
        journal(g)
    return c == 2


def play():
    g = St()
    g.x, g.y, g.a = 9.5, 6.4, -math.pi / 2
    g.power = g.locked = g.note = g.closet = g.living = g.tv = False
    g.tapheard = g.notebook = g.awake = g.armed = g.sighted = False
    g.flash = True
    g.blackout = False
    g.won = False
    g.hidden = False
    g.ys_vis = False
    g.ystate = "dormant"
    g.ytimer = 0
    g.yx = g.yy = 0
    g.shown = None
    cls()
    page("enCRYPTed", "Ashgrove Manor. Bought at government auction. Power off since the accident.\n\nIt is pitch dark. Find the power switch by the front door.")
    last = clock()
    dirty = True
    while not g.won:
        k = key()
        t = clock()
        dt = (t - last) if now else 0.25
        last = t
        dt = max(0.02, min(dt, 0.5))
        moved = False
        if k == CLR:
            if pause_menu(g):
                return
            dirty = True
            continue
        if k == DEL:
            journal(g)
            dirty = True
            continue
        if k == SECOND:
            g.flash = not g.flash
            g.shown = None
            dirty = True
            while key() == SECOND:
                pass
        if k == LEFT:
            g.a -= 2.0 * dt
            moved = True
        elif k == RIGHT:
            g.a += 2.0 * dt
            moved = True
        elif k == UP or k == DOWN:
            s = (1.6 if k == UP else -1.0) * dt
            nx = g.x + math.cos(g.a) * s
            ny = g.y + math.sin(g.a) * s
            r = 0.22 if s > 0 else -0.22
            if not solid(g, nx + math.cos(g.a) * r, g.y):
                g.x = nx
            if not solid(g, g.x, ny + math.sin(g.a) * r):
                g.y = ny
            moved = True
        elif k == OK:
            f = facing(g)
            if f:
                use(g, f)
                dirty = True
                while key() == OK:
                    pass
        if g.armed and not g.sighted and room(g) == "Grand Foyer":
            look = math.atan2(1.0 - g.y, 9.5 - g.x)
            diff = (look - g.a + math.pi) % (2 * math.pi) - math.pi
            if abs(diff) < 0.35:
                sighting(g)
                dirty = True
        before = g.ys_vis or g.blackout
        ys_update(g, dt)
        if moved or dirty or g.ys_vis or g.blackout or before:
            render(g)
            dirty = False
        f = facing(g)
        bottom(g, label(g, f) if f else short(g))
        if not moved:
            pause(0.03)
    ending()

RULES = "Explore Ashgrove Manor, solve Ivy's codes and hide from Ysolde when the lights stutter."
KEYS = ['Up/Down: walk  Left/Right: turn', 'ENTER: use  2nd: flashlight', 'DEL: journal  CLEAR: pause']


def main():
    while True:
        c = home("GHCRYPT", 'enCRYPTed DEMO', RULES, KEYS, ("Start", "Back"))
        if c < 0:
            return
        play()
