# Makes the packed picture data in calc/GHCRYPT.py: Ysolde's shape (YSD)
# and the furniture (SPRD). The shapes are described here as code that is
# easy to change; the calculator only gets the finished numbers as bytes,
# because the code that builds them was too big for its memory.
# Run from the repo root after changing a shape: python3 tools/ysdata.py
import math, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


def q(v):
    return max(0, min(255, int(round(v * 255))))


def packed():
    _build_ys()
    ys = bytes(b for u0, u1, v0, v1, k in YS for b in (q(u0), q(u1), q(v0), q(v1), k))
    out = []
    for name in sorted(SPR):
        w, parts = SPR[name]
        out += [q(w / 2), len(parts)]
        for u0, u1, v0, v1, c in parts:
            out += [q(u0), q(u1), q(v0), q(v1)] + list(c)
    return ys, bytes(out), sorted(SPR)


if __name__ == '__main__':
    ys, spr, names = packed()
    p = os.path.join(ROOT, 'calc', 'GHCRYPT.py')
    s = open(p).read()
    s = re.sub(r"^YSD = .*$", lambda m: 'YSD = ' + repr(ys), s, flags=re.M)
    s = re.sub(r"^SPRD = .*$", lambda m: 'SPRD = ' + repr(spr), s, flags=re.M)
    s = re.sub(r"^SPRN = .*$", lambda m: 'SPRN = ' + repr(tuple(names)), s, flags=re.M)
    open(p, 'w').write(s)
    print(len(ys) // 5, 'slabs,', len(spr), 'furniture bytes')
