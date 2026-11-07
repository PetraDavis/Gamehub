# Wing It: tap UP (or 2nd) to flap through the gaps between the trees.
from GHLIB import *
import random

try:
    from time import monotonic as now
except Exception:
    now = None

GAP = 64
NP = 15          # a tree is 15 two-pixel columns wide (30 px)
TW = NP * 2
TOP = 22         # play area runs from y=22 down to the ground at y=196
GND = 196
BX = 60          # the bird stays at this x
BR = 7           # and is this round for crashes
SKY = (110, 195, 240)
LEAF = (50, 140, 60)
LEAF2 = (44, 126, 54)
LEAFHI = (90, 175, 95)
LEAFLO = (30, 95, 40)
TRUNK = (110, 75, 40)
INK = (20, 20, 20)
ROUND = (6, 2)
# physics in pixels and seconds
GRAV = 900.0
FLAP = -265.0
FALL = 430.0
SPEED = 80.0


def column(j, gy):
    # what one two-pixel column j of a tree looks like, top to bottom, as
    # (y0, y1, colour) spans covering TOP..GND. The middle columns repeat every
    # two columns, so when a tree moves by 4 px only its edges change.
    k = min(j, NP - 1 - j)
    yt = gy + GAP
    yc = min(GND, yt + 26)
    if k < 2:
        # the rounded edges: one colour, shorter
        sh = ROUND[k]
        c = LEAFLO if k == 0 else LEAF
        out = [(TOP, gy - sh, c), (gy - sh, yt + sh, SKY), (yt + sh, yc - sh, c), (yc - sh, GND, SKY)]
    else:
        leaf = LEAF if j % 2 == 0 else LEAF2
        out = [(TOP, gy - 4, leaf), (gy - 4, gy, LEAFLO), (gy, yt, SKY),
               (yt, yt + 4, LEAFHI), (yt + 4, yc, leaf)]
        if 6 <= j <= 8:
            out.append((yc, GND, TRUNK if j < 8 else dk(TRUNK)))
        else:
            out.append((yc, GND, SKY))
    return out


SKYCOL = [(TOP, GND, SKY)]


def bg(p, trees):
    # the background of screen column pair p (x = 2p, 2p+1)
    for t in trees:
        j = p - t[0] // 2
        if 0 <= j < NP:
            return column(j, t[1])
    return SKYCOL


def diff(old, new):
    # the parts of a column that change colour, as (y0, y1, colour)
    cuts = sorted(set([a for a, b, c in old] + [b for a, b, c in old] + [a for a, b, c in new] + [b for a, b, c in new]))
    out = []
    for i in range(len(cuts) - 1):
        a, b = cuts[i], cuts[i + 1]
        if b <= a:
            continue
        m = (a + b) // 2
        co = cn = None
        for y0, y1, c in old:
            if y0 <= m < y1:
                co = c
        for y0, y1, c in new:
            if y0 <= m < y1:
                cn = c
        if cn is not None and co != cn:
            if out and out[-1][1] == a and out[-1][2] == cn:
                out[-1] = (out[-1][0], b, cn)
            else:
                out.append((a, b, cn))
    return out


def paint(cols):
    # cols: [(p, [(y0, y1, colour)...])] in order of p. Joins the same span in
    # neighbouring columns into one wider rectangle, so there are few calls.
    run = {}
    for p, spans in cols:
        keep = {}
        for sp in spans:
            if sp in run and run[sp][1] == p:
                keep[sp] = (run[sp][0], p + 1)
            else:
                keep[sp] = (p, p + 1)
        for sp in run:
            if sp not in keep or keep[sp][0] != run[sp][0]:
                _span(sp, run[sp])
        run = keep
    for sp in run:
        _span(sp, run[sp])


def _span(sp, r):
    # every edge is on an even row, so spans are at least 2 tall
    y0, y1, c = sp
    if y1 > y0:
        rect(r[0] * 2, y0, (r[1] - r[0]) * 2, max(2, y1 - y0), c)


def clip(spans, a, b):
    out = []
    for y0, y1, c in spans:
        y0 = max(y0, a)
        y1 = min(y1, b)
        if y1 > y0:
            out.append((y0, y1, c))
    return out


def bird(y, wing, tilt):
    x = BX
    circ(x, y, 8, (170, 120, 20))
    circ(x, y, 7, YELLOW)
    rect(x - 7, y - 2 + wing, 7, 3, (255, 245, 190))
    circ(x + 3, y - 3, 3, WHITE)
    circ(x + 4, y - 3 + (1 if tilt > 0 else 0), 1, BLACK)
    rect(x + 7, y - 1 + tilt, 5, 3, (245, 140, 30))


def ground():
    rect(0, 196, 320, 5, (70, 170, 80))
    rect(0, 201, 320, 9, (120, 80, 40))
    for x in range(0, 320, 16):
        rect(x + 4, 197, 3, 2, (110, 200, 110))
        rect(x + 10, 198, 2, 2, (40, 120, 50))
        rect(x + 7, 204, 3, 2, (95, 60, 30))
        rect(x + 1, 207, 2, 2, (150, 105, 60))


def score_bar(score):
    rect(0, 0, 320, 20, SKY)
    text(6, 17, "Score " + str(score), INK)


def crashed(y, trees):
    if y + 8 >= GND:
        return True
    for p in range((BX - BR) // 2, (BX + BR) // 2 + 1):
        for y0, y1, c in bg(p, trees):
            if c == SKY:
                continue
            dx = abs(p * 2 + 1 - BX)
            if dx > BR:
                continue
            dy = int((BR * BR - dx * dx) ** 0.5)
            if y0 < y + dy and y - dy < y1:
                return True
    return False


def game():
    cls(SKY)
    ground()
    rect(0, 20, 320, 2, INK)
    score_bar(0)
    trees = [[332, random.randint(20, 55) * 2], [332 + 172, random.randint(20, 55) * 2]]
    shown = [SKYCOL] * 160
    y = 100.0
    v = 0.0
    score = 0
    passed = [False, False]
    wing = 0
    go = 0.0
    oy = int(y)
    bird(oy, 0, 0)
    pause(0.4)
    last = now() if now else 0
    while True:
        k = key()
        if k == CLR:
            return
        if now:
            t = now()
            dt = min(0.12, max(0.03, t - last))
            last = t
        else:
            dt = 0.05
        if k in (UP, SECOND, OK):
            v = FLAP
            wing = 3
        v = min(FALL, v + GRAV * dt)
        y += v * dt
        if y < TOP + 9:
            y = TOP + 9.0
            v = 0.0
        # move the trees in steps of 4 px
        go += SPEED * dt
        step = int(go / 4) * 4
        go -= step
        lo, hi = 160, 0
        for i in range(2):
            t = trees[i]
            a = t[0] // 2
            t[0] -= step
            if t[0] + TW < 0:
                t[0] = max(332, trees[1 - i][0] + 172)
                t[1] = random.randint(20, 55) * 2
                passed[i] = False
            for p in (a, t[0] // 2):
                lo = min(lo, max(0, p))
                hi = max(hi, min(160, p + NP))
            if not passed[i] and t[0] + TW < BX - BR:
                passed[i] = True
                score += 1
                score_bar(score)
        work = []
        for p in range(lo, hi):
            n = bg(p, trees)
            if n is not shown[p] and n != shown[p]:
                d = diff(shown[p], n)
                if d:
                    work.append((p, d))
            shown[p] = n
        paint(work)
        # the bird: put the background back where it was, then draw it again
        ny = int(y)
        a = (min(oy, ny) - 10) // 2 * 2
        b = (max(oy, ny) + 11) // 2 * 2
        paint([(p, clip(shown[p], a, b)) for p in range((BX - 9) // 2, (BX + 13) // 2)])
        wing = max(0, wing - 1)
        bird(ny, wing, 1 if v > 150 else (-1 if v < -100 else 0))
        oy = ny
        if crashed(y, trees):
            pause(0.4)
            message(["You passed " + str(score) + " trees."], "Crash!")
            return
        pause(0.01)


RULES = "Flap to fly through the gaps between the trees. Don't hit the trees or the ground."
KEYS = ['Up, 2nd or ENTER: flap', 'CLEAR: quit']


def main():
    while True:
        c = home("GHFLAP", 'WING IT', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
