# enCRYPTed demo for GAMEHUB. Based on Petra's game:
# full game at petradavis.github.io/Encrypted/?ysolde=1
# Up/Down walk, Left/Right turn, ENTER use, 2nd flashlight,
# DEL journal, CLEAR pause.
from GHLIB import *
import math
import gc
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
COLS = 32
CWID = VW // COLS  # 32 columns of 10 pixels
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


# ---------- sprites: kind -> half width, list of (u0, u1, v0, v1, color) ----------
# The furniture and Ysolde are described in tools/ysdata.py, which packs them
# into the bytes below (values 0-255 stand for 0-1). Run it after a change.
SPRN = ('couch', 'desk', 'lamp', 'phone', 'rack', 'table', 'vase')
SPRD = b'\xa6\x04\x00\xff\x003\x96(-\x14\xeb3\\x\x1e#\x00\x1f3G\x96(-\xe0\xff3G\x96(-\x99\x04\x00\x1a\x00L_A(\xe6\xff\x00L_A(\x00\xffLYxU23\x80Ya\xc8\xbe\x96L\x02s\x8c\x00\x8c\xb4\x96F&\xd9\x8c\xb8\xeb\xdc\xaaL\x04\x00&\x00L_A(\xd9\xff\x00L_A(\x00\xffLWxU2@\xbfWk\x14\x14\x14Y\x03u\x8a\x00\xccP7#&sY\xbf<Fn\x8c\xd9f\xb8n22s\x04\x00\x1f\x00G_A(\xe0\xff\x00G_A(\x00\xffGTxU2L\xb2T^\x8cF\xb4Y\x03\x1a\xe6\x00@_A(Y\xa6@s<x\x8cL\xb2s\x8cZ\x8cF'
SPR = {}


def _unpack_spr():
    i = 0
    for name in SPRN:
        w, n = SPRD[i] / 255 * 2, SPRD[i + 1]
        i += 2
        parts = []
        for k in range(n):
            d = SPRD[i:i + 7]
            parts.append((d[0] / 255, d[1] / 255, d[2] / 255, d[3] / 255, (d[4], d[5], d[6])))
            i += 7
        SPR[name] = (w, parts)


_unpack_spr()
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
    # a colour as one number 0xRRGGBB: numbers need no memory of their own on
    # the calculator, colour tuples do, and the screen holds hundreds of them
    return min(255, int(c[0] * k)) << 16 | min(255, int(c[1] * k)) << 8 | min(255, int(c[2] * k))


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


def colour(t):
    if t in "lkjCF":
        return DOOR
    if t == "S":
        return (120, 90, 60)
    if t == "B":
        return (90, 60, 35)
    return WALL


def lq(k):
    # light comes in a few steps, so neighbouring columns share colours
    return int(k * 5 + .5) / 5


def put(sp, a, b, c):
    # paint colour c over rows a..b of a column's span list
    if b <= a:
        return sp
    out = []
    for y0, y1, cc in sp:
        if y0 < a:
            out.append((y0, min(y1, a), cc))
    out.append((a, b, c))
    for y0, y1, cc in sp:
        if y1 > b:
            out.append((max(y0, b), y1, cc))
    return out


def diff(old, new):
    # the parts of column spans new that differ from old, as (y0, y1, colour)
    if old is None:
        return new
    out = []
    i = j = 0
    y = 0
    while y < VH:
        o0, o1, oc = old[i]
        n0, n1, nc = new[j]
        e = min(o1, n1)
        if oc != nc:
            if out and out[-1][1] == y and out[-1][2] == nc:
                out[-1] = (out[-1][0], e, nc)
            else:
                out.append((y, e, nc))
        y = e
        if o1 == e:
            i += 1
        if n1 == e:
            j += 1
    return out


def column(g, t, u, top, h, k):
    # what one wall column looks like, top to bottom, as spans
    cl = 0 if g.blackout else shade(CEIL, 1)
    fl = 0 if g.blackout else shade(FLOOR, .5 if not g.power else 1)
    y0 = max(0, top)
    y1 = min(VH, top + h)
    sp = [(0, y0, cl), (y0, y1, shade(colour(t), k)), (y1, VH, fl)]
    if y0 == 0:
        sp = sp[1:]
    if y1 == VH:
        sp = sp[:-1]
    sp = [s for s in sp if s[1] > s[0]]

    def band(v0, v1, c, glow=False):
        # glow: a light of its own, as bright in the dark as in the light
        a = int(top + h * (1 - v1)) & ~1
        b = int(top + h * (1 - v0)) & ~1
        if b - a >= 2:
            return put(sp, max(0, a), min(VH, b), shade(c, 1 if glow and not g.blackout else k))
        return sp
    if t in "lkjCF":
        if u < .12 or u > .88:
            sp = band(0, .8, (70, 48, 30))
        sp = band(.8, 1, WALL)
        if .7 < u < .85:
            sp = band(.42, .47, (210, 180, 90))
        if t in "kC" and .12 < u < .3:
            on = t == "C" and g.closet
            sp = band(.5, .6, (40, 40, 40))
            sp = band(.53, .57, (40, 200, 70) if on else (200, 40, 40) if g.power else (30, 30, 30))
        if t == "F":
            # the front door: moonlight through its window, so it shows in
            # the dark, and a red lock light once it has locked
            if .3 < u < .7:
                sp = band(.6, .74, (70, 85, 120), True)
                if .48 < u < .52:
                    sp = band(.6, .74, (30, 30, 40))
            if g.locked and .15 < u < .25:
                sp = band(.55, .6, (255, 30, 40), True)
    elif t == "S":
        for n in range(6):
            sp = band(n * .14, n * .14 + .07, (95, 70, 45))
        if .2 < u < .8:
            sp = band(.25, .32, (150, 120, 80))
            sp = band(.55, .62, (150, 120, 80))
    elif t == "B":
        for n in range(4):
            cc = ((150, 50, 50), (50, 90, 150), (60, 130, 70), (170, 140, 60))[(int(u * 4) + n) % 4]
            sp = band(n * .25 + .05, n * .25 + .2, cc)
    elif t == "T":
        if .1 < u < .9:
            sp = band(.35, .7, (15, 15, 20) if not g.tv else (60, 90, 160))
    elif t == "G":
        if .28 < u < .72:
            sp = band(0, .85, (70, 45, 30))
            sp = band(.6, .75, (220, 210, 180))
            if .45 < u < .55:
                sp = band(.2, .55, (180, 150, 70))
                if not g.note:
                    sp = band(.25, .3, (240, 240, 230))
    elif t == "P":
        # the power switch: a big panel with a glowing light, red while the
        # power is off and green once it is on, easy to spot in the dark
        if .25 < u < .75:
            sp = band(.3, .62, (150, 150, 155))
            if .4 < u < .6:
                sp = band(.38, .5, (40, 40, 40))
                sp = band(.44 if g.power else .38, .5 if g.power else .44, (200, 200, 205))
            if .42 < u < .58:
                sp = band(.54, .59, (60, 230, 90) if g.power else (255, 50, 40), True)
    return sp


def render(g, full=False):
    # Collect garbage every frame so memory stays in one piece. If the
    # calculator still runs out, forget what is on screen and paint it all.
    gc.collect()
    try:
        draw(g, full)
    except MemoryError:
        g.cols = None
        gc.collect()
        draw(g, True)


def draw(g, full):
    # Every screen column is a list of coloured spans. Only the spans that
    # differ from what is on screen are painted, side-by-side columns with the
    # same change become one rectangle, and each colour is set only once.
    if full or getattr(g, 'cols', None) is None or g.cover != COVER[0]:
        g.cover = COVER[0]
        g.cols = [None] * COLS
        g.ysk = None
    shown = g.cols
    new = []
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
        h = int(VH * 1.35 / d) & ~7
        top = (VH - h) // 2
        k = lq(light(g, i, d) * (0.8 if side else 1.0))
        new.append(column(g, t, u, top, h, k))
    sprites(g, zb, ca, sa, new)
    ys = ys_place(g, zb, ca, sa)
    if g.ysk is not None and (ys is None or ys[0] != g.ysk):
        # she moved or left: her old columns are painted afresh
        for i in range(g.ysa, g.ysb):
            shown[i] = None
    runs = {}
    hit = False
    for i in range(COLS):
        for y0, y1, c in diff(shown[i], new[i]):
            key = (y0, y1, c)
            r = runs.get(key)
            if r and r[-1][1] == i:
                r[-1][1] = i + 1
            elif r:
                r.append([i, i + 1])
            else:
                runs[key] = [[i, i + 1]]
            if ys and ys[1] <= i < ys[2]:
                hit = True
        shown[i] = new[i]
    for key in sorted(runs, key=lambda q: q[2]):
        y0, y1, c = key
        c = (c >> 16, c >> 8 & 255, c & 255)
        for a, b in runs[key]:
            rect(a * CWID, y0, (b - a) * CWID, y1 - y0, c)
    if ys:
        if ys[0] != g.ysk or hit:
            ys_draw(g, ys)
        else:
            ys_shimmer(g)
        g.ysk, g.ysa, g.ysb = ys[0], ys[1], ys[2]
    else:
        g.ysk = None


def sprites(g, zb, ca, sa, new):
    lst = []
    for sx, sy, kind in SPRITES:
        dx = sx - g.x
        dy = sy - g.y
        fwd = dx * ca + dy * sa
        if fwd < 0.2:
            continue
        lst.append((fwd, -dx * sa + dy * ca, kind))
    lst.sort(reverse=True)
    for fwd, side, kind in lst:
        cx = (side / fwd) / (FOV * 0.5 * 1.15)
        scol = (cx + 1) / 2 * COLS
        half = SPR[kind][0] / 2 / fwd / (FOV * 0.5 * 1.15) * COLS / 2
        h = VH * 1.35 / fwd
        top = (VH - h) / 2
        k = lq(light(g, int(scol), fwd))
        for i in range(max(0, int(scol - half)), min(COLS, int(scol + half) + 1)):
            if zb[i] < fwd:
                continue
            u = (i + 0.5 - (scol - half)) / (2 * half) if half > 0 else .5
            if u < 0 or u > 1:
                continue
            for u0, u1, v0, v1, c in SPR[kind][1]:
                if u0 <= u <= u1:
                    y0 = int(top + h * (1 - v1)) & ~1
                    y1 = int(top + h * (1 - v0)) & ~1
                    if y1 - y0 >= 2 and y0 < VH:
                        new[i] = put(new[i], max(0, y0), min(VH, y1), shade(c, k))


def bottom(g, prompt):
    if prompt == g.shown:
        return
    g.shown = prompt
    rect(0, VH, 320, 210 - VH, BLACK)
    text(4, VH + 15, room(g), GREY)
    if g.flash:
        text(250, VH + 15, "LIGHT", GOLD)
    text(4, VH + 33, prompt[:31], WHITE)


# Ysolde, from her character sheet: very thin and tall, small head tilted
# hard on a long neck, lank hair, short tattered dress, arms past the knees.
# Dark inside with faint static, an outline of bright static and two small
# cold blue eyes. tools/ysdata.py builds her as thin slabs and packs each one
# as 5 bytes: u0, u1, v0, v1 (0-255 for 0-1) and kind (4 is an eye, 5 an
# outline slab).
YSD = b"{\x85\xce\xd3\x00|\x86\xd1\xd7\x00}\x87\xd5\xda\x00~\x88\xd8\xdd\x00\x80\x8b\xdb\xe1\x00\x84\x8f\xdf\xe6\x00t\x89\xcf\xd2\x05b\x9b\xcc\xcf\x00c\x9f\xc9\xcc\x00c\x9e\xc6\xc9\x00d\x9d\xc2\xc6\x00e\x9c\xbf\xc2\x00e\x9b\xbc\xbf\x00f\x9a\xb9\xbc\x00g\x99\xb6\xb9\x00h\x98\xb2\xb6\x00h\x97\xaf\xb2\x00i\x96\xac\xaf\x00j\x95\xa9\xac\x00j\x95\xa6\xa9\x00k\x94\xa3\xa6\x00l\x93\x9f\xa3\x00l\x93\x9c\x9f\x00m\x92\x99\x9c\x00k\x94\x99\x9b\x00j\x95\x97\x99\x00i\x96\x94\x97\x00h\x97\x92\x94\x00g\x98\x8f\x92\x00f\x99\x8d\x8f\x00e\x9a\x8b\x8d\x00d\x9b\x88\x8b\x00c\x9c\x86\x88\x00b\x9d\x83\x86\x00a\x9e\x81\x83\x00`\x9f\x7f\x81\x00_\xa0|\x7f\x00^\xa1z|\x00^\x9cxz\x00^\x98ux\x05ry{\x81\x00qyx}\x00qxuz\x00qxqw\x00pxns\x00pwkp\x00pwhm\x00owdj\x00ovaf\x00nv^c\x00nvZ`\x00nuW\\\x00muTY\x00mtQV\x00mtMS\x00ltJO\x00lsGL\x00mzCI\x00s{?E\x00sz<A\x00rz9>\x00qy5;\x00qx27\x00pw/4\x00ow+1\x00nv(-\x00nu%*\x00mu!'\x00lt\x1e#\x00ls\x1b \x00ks\x17\x1d\x00jr\x14\x19\x00jq\x11\x16\x00ip\r\x13\x00hp\n\x10\x00dn\x07\x0c\x00_i\x04\t\x00\x88\x8f{\x81\x00\x88\x90x}\x00\x89\x90tz\x00\x89\x90qw\x00\x89\x91ns\x00\x8a\x91kp\x00\x8a\x91gm\x00\x8a\x92di\x00\x8b\x92af\x00\x8b\x92]c\x00\x8b\x93Z_\x00\x8c\x93W\\\x00\x8c\x94SY\x00\x8c\x94PU\x00\x8d\x94MR\x00\x8d\x95IO\x00\x8e\x95FK\x00\x86\x93AH\x00\x84\x8c>C\x00\x85\x8d;@\x00\x86\x8d8=\x00\x86\x8e4:\x00\x87\x8f16\x00\x88\x90.3\x00\x89\x91+0\x00\x8a\x91(-\x00\x8b\x92$*\x00\x8b\x93!&\x00\x8c\x94\x1e#\x00\x8d\x95\x1b \x00\x8e\x96\x18\x1d\x00\x8f\x96\x14\x1a\x00\x90\x97\x11\x17\x00\x90\x98\x0e\x13\x00\x91\x99\x0b\x10\x00\x93\x9e\x07\r\x00\x99\xa4\x03\t\x00`f\xc8\xcd\x00_e\xc4\xca\x00^d\xc1\xc7\x00]c\xbe\xc3\x00\\b\xbb\xc0\x00[a\xb8\xbd\x00Z`\xb4\xba\x00X_\xb1\xb6\x00W^\xae\xb3\x00V]\xab\xb0\x00U\\\xa7\xad\x00T[\xa4\xa9\x00SY\xa1\xa6\x00RX\x9e\xa3\x00QW\x9a\xa0\x00R]\x96\x9c\x00X^\x92\x98\x00W]\x8f\x94\x00V]\x8c\x91\x00V\\\x88\x8e\x00U[\x85\x8a\x00TZ\x82\x87\x00SY~\x84\x00RX{\x80\x00QXx}\x00QWtz\x00PVqv\x00OUns\x00NTkp\x00MSgm\x00LSdi\x00LRaf\x00KQ]c\x00JPZ_\x00IOW\\\x00\x9b\xa1\xc8\xcd\x00\x9c\xa2\xc5\xca\x00\x9d\xa4\xc1\xc7\x00\x9e\xa5\xbe\xc3\x00\xa0\xa6\xbb\xc0\x00\xa1\xa7\xb8\xbd\x00\xa2\xa8\xb5\xba\x00\xa3\xaa\xb1\xb7\x00\xa4\xab\xae\xb4\x00\xa6\xac\xab\xb0\x00\xa7\xad\xa8\xad\x00\xa8\xae\xa5\xaa\x00\xa9\xb0\xa2\xa7\x00\xaa\xb1\x9e\xa4\x00\xac\xb2\x9b\xa0\x00\xa4\xb0\x96\x9d\x00\xa3\xa9\x92\x98\x00\xa4\xaa\x8f\x94\x00\xa5\xab\x8c\x91\x00\xa6\xac\x88\x8e\x00\xa7\xad\x85\x8b\x00\xa8\xae\x82\x87\x00\xa9\xaf\x7f\x84\x00\xaa\xb0{\x81\x00\xab\xb1x}\x00\xac\xb2uz\x00\xad\xb3rw\x00\xae\xb4nt\x00\xaf\xb5kp\x00\xb0\xb6hm\x00\xb1\xb7dj\x00\xb2\xb8af\x00\xb3\xb9^c\x00\xb4\xba[`\x00KNSY\x00LOPU\x00MPLR\x00NQIN\x00OREK\x00PSBG\x00PS>D\x00OR;@\x00KMSY\x00KMPU\x00KNLR\x00LNIN\x00LNFK\x00LNBH\x00LO?D\x00JN:A\x00JMSY\x00JLPU\x00JLLR\x00ILIN\x00IKEK\x00IKBG\x00HK?D\x00FI<A\x00EH8>\x00JMSY\x00ILPU\x00HKLR\x00GJIN\x00GIFK\x00FHBH\x00EG?D\x00CF;A\x00@D7=\x00ILSY\x00HKPU\x00FILR\x00DGIN\x00CFEK\x00ADBG\x00?B>D\x00=@:@\x00;>6<\x00\xb5\xb8W]\x00\xb4\xb7TY\x00\xb3\xb6PV\x00\xb2\xb5MR\x00\xb1\xb4IO\x00\xb0\xb3FK\x00\xb0\xb3BH\x00\xb1\xb4?D\x00\xb6\xb8W]\x00\xb6\xb8TY\x00\xb5\xb8PV\x00\xb5\xb7MR\x00\xb5\xb7JO\x00\xb5\xb7FL\x00\xb4\xb7CH\x00\xb5\xb9>E\x00\xb6\xb9W]\x00\xb7\xb9TY\x00\xb7\xb9PV\x00\xb7\xbaMR\x00\xb8\xbaIO\x00\xb8\xbaFK\x00\xb8\xbbCH\x00\xba\xbd@E\x00\xbb\xbe<B\x00\xb6\xb9W]\x00\xb7\xbaTY\x00\xb8\xbbPV\x00\xb9\xbcMR\x00\xba\xbcJO\x00\xbb\xbdFL\x00\xbc\xbeCH\x00\xbd\xc0?E\x00\xbf\xc3;A\x00\xb7\xbaW]\x00\xb8\xbbTY\x00\xba\xbdPV\x00\xbc\xbfMR\x00\xbd\xc0IO\x00\xbf\xc2FK\x00\xc1\xc4BH\x00\xc3\xc6>D\x00\xc5\xc8:@\x00\x8d\x93\xf4\xf5\x05\x87\x99\xf2\xf4\x00\x81\xa0\xf1\xf2\x00|\xa0\xef\xf1\x00x\x9f\xed\xef\x00t\x9e\xec\xed\x00p\x9e\xea\xec\x00l\x9d\xe9\xea\x00h\x9b\xe7\xe9\x00d\x98\xe5\xe7\x00b\x96\xe4\xe5\x00`\x94\xe2\xe4\x00^\x92\xe1\xe2\x00\\\x90\xdf\xe1\x00Y\x8d\xdd\xdf\x00W\x8b\xdc\xdd\x00U\x89\xda\xdc\x00S\x87\xd9\xda\x00Q\x85\xd7\xd9\x00N\x82\xd5\xd7\x00L\x80\xd4\xd5\x00J~\xd2\xd4\x00Hz\xd1\xd2\x00Fv\xcf\xd1\x00`q\xcd\xcf\x00`m\xcc\xcd\x00_h\xca\xcc\x00_d\xc9\xca\x00^_\xc7\xc9\x05\x8a\x99\xf3\xf4\x05\x84\x9c\xf1\xf3\x00\x80\x9e\xef\xf1\x00}\x9f\xee\xef\x00{\x9e\xec\xee\x00z\x9e\xeb\xec\x00y\x9d\xe9\xeb\x00x\x9b\xe8\xe9\x00y\x98\xe6\xe8\x00z\x95\xe4\xe6\x00|\x90\xe3\xe4\x00\x84\x86\xe1\xe3\x05\x87\x8b\xee\xef\x04\x93\x97\xeb\xec\x04"
YG = 4  # Ysolde is drawn on a 4-pixel grid
RIM = ((215, 215, 225), (170, 175, 190), (250, 250, 255))
INSIDE = (36, 36, 44)


def ys_place(g, zb, ca, sa):
    # where Ysolde is on screen, or None
    if not g.ys_vis:
        return None
    dx = g.yx - g.x
    dy = g.yy - g.y
    fwd = dx * ca + dy * sa
    if fwd < 0.2:
        return None
    cx = (-dx * sa + dy * ca) / fwd / (FOV * 0.5 * 1.15)
    scol = (cx + 1) / 2 * COLS
    half = 0.45 / 2 / fwd / (FOV * 0.5 * 1.15) * COLS / 2
    # her size and place move in small steps, so she isn't drawn again for
    # every tiny step she takes
    h = int(VH * 1.35 / fwd) & ~7
    top = (VH - h) // 2
    a = None
    b = 0
    for i in range(max(0, int(scol - half)), min(COLS, int(scol + half) + 1)):
        if zb[i] >= fwd:
            if a is None:
                a = i
            b = i + 1
    if a is None:
        return None
    left = int((scol - half) * CWID) & ~3
    return ((left, int(2 * half * CWID) & ~3, top, h, a, b), a, b)


def ys_draw(g, ys):
    # her body: slabs merged into rows on a 4-pixel grid, an outline of
    # bright static and a dark inside; rows that match the row above
    # become one taller rectangle
    left, wid, top, h, a, b = ys[0]
    lo = a * CWID
    hi = b * CWID
    rows = {}
    eyes = []
    for i in range(0, len(YSD), 5):
        u0, u1, v0, v1, kind = YSD[i] / 255, YSD[i + 1] / 255, YSD[i + 2] / 255, YSD[i + 3] / 255, YSD[i + 4]
        xa = max(lo, int(left + u0 * wid)) // YG
        xb = min(hi, int(left + u1 * wid) + 1 + YG - 1) // YG
        ya = int(top + h * (1 - v1))
        yb = int(top + h * (1 - v0)) + 1
        if kind == 4:
            eyes.append(((xa + xb) * YG // 2, (ya + yb) // 2))
            continue
        if xb <= xa:
            continue
        for r in range(max(0, ya) // YG, (min(VH, yb) + YG - 1) // YG):
            if r in rows:
                rows[r].append((xa, xb))
            else:
                rows[r] = [(xa, xb)]
    out = []
    open_ = {}
    for r in range(VH // YG + 1):
        cur = {}
        segs = sorted(rows.get(r, ()))
        m = []
        for xa, xb in segs:
            if m and xa <= m[-1][1]:
                if xb > m[-1][1]:
                    m[-1][1] = xb
            else:
                m.append([xa, xb])
        for xa, xb in m:
            if xb - xa >= 3:
                cur[(xa, xa + 1, 0)] = 1
                cur[(xa + 1, xb - 1, 1)] = 1
                cur[(xb - 1, xb, 0)] = 1
            else:
                cur[(xa, xb, 0)] = 1
        for key in list(open_):
            if key not in cur:
                out.append((key, open_.pop(key), r))
        for key in cur:
            if key not in open_:
                open_[key] = r
    g.rim = []
    for c in (0, 1):
        for (xa, xb, kind), r0, r1 in out:
            if kind == c:
                x, y, w, hh = xa * YG, r0 * YG, (xb - xa) * YG, min(VH, r1 * YG) - r0 * YG
                if hh > 0:
                    rect(x, y, w, hh, INSIDE if c else RIM[0])
                    if not c:
                        g.rim.append((x, y, w, hh))
    r = max(2, wid // 12)
    eyes = [(x, y) for x, y in eyes if lo + r <= x < hi - r and r <= y < VH - r]
    for rr, c in ((r, (35, 80, 150)), (r * 2 // 3, (80, 175, 245)), (max(1, r // 3), (230, 250, 255))):
        for x, y in eyes:
            circ(x, y, rr, c)


def ys_shimmer(g):
    # the static crawls: a few pieces of her outline change shade
    if not g.rim:
        return
    for n in range(3):
        x, y, w, h = random.choice(g.rim)
        rect(x, y, w, h, random.choice(RIM))


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
    COVER[0] += 1
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
        t = "Find the red light by the door."
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
    st = Steer((UP, DOWN), True)
    while not g.won:
        k = key()
        d = st.feed(k) if k not in (LEFT, RIGHT) else st.d
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
            ox, oy = g.x, g.y
            if not solid(g, nx + math.cos(g.a) * r, g.y):
                g.x = nx
            if not solid(g, g.x, ny + math.sin(g.a) * r):
                g.y = ny
            if abs(g.x - ox) + abs(g.y - oy) < 0.001:
                st.stop()
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
                st.stop()
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
KEYS = ['Up/Down: start walking', 'Press the other one to stop', 'Left/Right: turn a step', 'ENTER: use  2nd: flashlight', 'DEL: journal  CLEAR: pause']


def main():
    while True:
        c = home("GHCRYPT", 'enCRYPTed DEMO', RULES, KEYS, ("Start", "Back"))
        if c < 0:
            return
        play()
