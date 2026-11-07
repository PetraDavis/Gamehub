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
INK = (20, 20, 20)
BODY = (240, 200, 40)
BEAK = (245, 140, 30)
# physics in pixels and seconds
GRAV = 620.0     # lighter than before: Petra found the bird too heavy
FLAP = -235.0
FALL = 330.0
SPEED = 80.0
# Every drawing call takes about 7 ms on the calculator, however big it is,
# and so does every colour change. So the trees are flat green and each frame
# only paints the thin strips at their edges, all of one colour together.


def column(gy):
    # one column of a tree, top to bottom, as (y0, y1, colour) spans
    return [(TOP, gy, LEAF), (gy, gy + GAP, SKY), (gy + GAP, GND, LEAF)]


SKYCOL = [(TOP, GND, SKY)]


def bg(p, trees):
    # the background of screen column pair p (x = 2p, 2p+1)
    for t in trees:
        if 0 <= p - t[0] // 2 < NP:
            return t[2]
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


def spans(cols, out):
    # cols: [(p, [(y0, y1, colour)...])] in order of p. Joins the same span in
    # neighbouring columns into one wider rectangle and adds it to out.
    run = {}
    for p, sp in cols:
        keep = {}
        for s in sp:
            if s in run and run[s][1] == p:
                keep[s] = (run[s][0], p + 1)
            else:
                keep[s] = (p, p + 1)
        for s in run:
            if s not in keep or keep[s][0] != run[s][0]:
                _span(s, run[s], out)
        run = keep
    for s in run:
        _span(s, run[s], out)


def _span(s, r, out):
    y0, y1, c = s
    if y1 > y0:
        out.append((c, r[0] * 2, y0, (r[1] - r[0]) * 2, y1 - y0))


def clip(sp, a, b):
    out = []
    for y0, y1, c in sp:
        y0 = max(y0, a)
        y1 = min(y1, b)
        if y1 > y0:
            out.append((y0, y1, c))
    return out


def batch(todo):
    # draw (colour, x, y, w, h) rectangles grouped by colour
    todo.sort()
    for c, x, y, w, h in todo:
        rect(x, y, w, h, c)


def bird(y):
    # three rectangles: body, beak and eye
    rect(BX - 7, y - 6, 14, 12, BODY)
    rect(BX + 7, y - 1, 5, 4, BEAK)
    rect(BX + 2, y - 3, 3, 3, INK)


def ground():
    rect(0, 196, 320, 5, (70, 170, 80))
    rect(0, 201, 320, 9, (120, 80, 40))
    for x in range(0, 320, 20):
        rect(x + 6, 204, 4, 2, (95, 60, 30))


def crashed(y, trees):
    if y + 7 >= GND:
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


def new_tree(x):
    gy = random.randint(20, 55) * 2
    return [x, gy, column(gy)]


def game():
    cls(SKY)
    ground()
    rect(0, 20, 320, 2, INK)
    text(6, 17, "Score", INK)
    text(66, 17, "0", INK)
    trees = [new_tree(332), new_tree(332 + 172)]
    shown = [SKYCOL] * 160
    y = 100.0
    v = 0.0
    score = 0
    passed = [False, False]
    go = 0.0
    oy = int(y)
    bird(oy)
    pause(0.4)
    last = now() if now else 0
    while True:
        k = key()
        if k == CLR:
            return
        if now:
            t = now()
            dt = min(0.12, max(0.01, t - last))
            last = t
        else:
            dt = 0.05
        if k in (UP, SECOND, OK):
            v = FLAP
        v = min(FALL, v + GRAV * dt)
        y += v * dt
        if y < TOP + 7:
            y = TOP + 7.0
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
                trees[i] = t = new_tree(max(332, trees[1 - i][0] + 172))
                passed[i] = False
            for p in (a, t[0] // 2):
                lo = min(lo, max(0, p))
                hi = max(hi, min(160, p + NP))
            if not passed[i] and t[0] + TW < BX - BR:
                passed[i] = True
                text(66, 17, str(score), SKY)
                score += 1
                text(66, 17, str(score), INK)
        work = []
        hit = False
        for p in range(lo, hi):
            n = bg(p, trees)
            if n is not shown[p]:
                d = diff(shown[p], n)
                if d:
                    work.append((p, d))
                    if BX - 8 <= p * 2 <= BX + 12:
                        hit = True
                shown[p] = n
        todo = []
        spans(work, todo)
        # the bird: paint back only the rows it moved away from
        ny = int(y)
        if ny != oy:
            a, b = (oy - 6, ny - 6) if ny > oy else (ny + 6, oy + 6)
            spans([(p, clip(shown[p], a, b)) for p in range((BX - 8) // 2, (BX + 13) // 2)], todo)
        batch(todo)
        if ny != oy or hit:
            bird(ny)
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
