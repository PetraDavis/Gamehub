# Stack Drop: fit the falling shapes together and fill rows to clear them.
# Left/Right move, Up turns, Down drops faster, 2nd drops all the way.
from GHLIB import *
import random

CW = 10
CH = 20
C = 9
OUT = (50, 20, 70)
WELL = (35, 30, 90)
DOT = (60, 55, 125)
PANEL = (70, 35, 100)
X0 = 115
Y0 = 22
SHAPES = (
    ((0, 1), (1, 1), (2, 1), (3, 1)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
    ((1, 0), (0, 1), (1, 1), (2, 1)),
    ((0, 0), (0, 1), (1, 1), (2, 1)),
    ((2, 0), (0, 1), (1, 1), (2, 1)),
    ((1, 0), (2, 0), (0, 1), (1, 1)),
    ((0, 0), (1, 0), (1, 1), (2, 1)),
)
COLS = ((90, 200, 220), (230, 200, 60), (170, 90, 210), (70, 110, 220),
        (230, 140, 50), (80, 190, 90), (220, 70, 70))


def cells(p):
    s, r, x, y = p
    out = []
    for cx, cy in SHAPES[s]:
        rx, ry = cx, cy
        if s != 1:
            for i in range(r):
                rx, ry = 2 - ry, rx
        out.append((x + rx, y + ry))
    return out


def cells_i(p):
    s, r, x, y = p
    if r % 2 == 0:
        return [(x + i, y + 1) for i in range(4)]
    return [(x + 2, y + i) for i in range(4)]


def get(p):
    return cells_i(p) if p[0] == 0 else cells(p)


def ok(b, p):
    for x, y in get(p):
        if x < 0 or x >= CW or y >= CH:
            return False
        if y >= 0 and b[y][x]:
            return False
    return True


def sq(x, y, c):
    if y < 0:
        return
    px = X0 + x * C
    py = Y0 + y * C
    # only filled rectangles that stay inside the cell, so erasing a cell
    # with one WELL square leaves nothing behind (lines can bleed outside)
    if c == WELL:
        rect(px, py, C, C, WELL)
        rect(px + 4, py + 4, 2, 2, DOT)
    else:
        rect(px, py, C, C, dk(c, 0.55))
        rect(px, py, C - 1, C - 1, c)
        rect(px, py, C - 1, 2, lt(c, 0.45))
        rect(px, py, 2, C - 1, lt(c, 0.45))
        rect(px + 3, py + 3, 2, 2, lt(c, 0.7))


class Well:
    # remembers what each cell shows, so only cells that change are drawn
    def __init__(self):
        self.s = [[-1] * CW for i in range(CH)]
        self.last = []

    def put(self, x, y, v):
        if 0 <= y and self.s[y][x] != v:
            self.s[y][x] = v
            sq(x, y, COLS[v - 1] if v else WELL)

    def show(self, b, p, full=False):
        # the piece's old and new cells, or every cell after rows clear
        new = [c for c in get(p) if c[1] >= 0] if p else []
        if full:
            cells = [(x, y) for y in range(CH) for x in range(CW)]
        else:
            cells = self.last + new
        self.last = new
        v = p[0] + 1 if p else 0
        want = [(v if c in new else b[c[1]][c[0]], c) for c in cells]
        # one colour at a time is quicker on the calculator
        want.sort()
        for w, c in want:
            self.put(c[0], c[1], w)


def side(score, lines, nxt, old):
    # only the parts that changed: the next shape, the score, the lines
    if old is None:
        for y, h in ((26, 64), (96, 40), (142, 40)):
            rbox(226, y, 88, h, 6, (150, 110, 190), 2, PANEL)
        text(234, 44, "NEXT", (200, 185, 230))
        text(234, 114, "SCORE", (200, 185, 230))
        text(234, 160, "LINES", (200, 185, 230))
        old = (None, None, None)
    if nxt != old[2]:
        rect(240, 50, 40, 22, PANEL)
        for x, y in get((nxt, 0, 0, 0)):
            c = COLS[nxt]
            rect(244 + x * 9, 54 + y * 9, 9, 9, dk(c, 0.55))
            rect(244 + x * 9, 54 + y * 9, 8, 8, c)
            rect(245 + x * 9, 55 + y * 9, 2, 2, lt(c, 0.7))
    if score != old[0]:
        if old[0] is not None:
            text(234, 131, str(old[0]), PANEL)
        text(234, 131, str(score))
    if lines != old[1]:
        if old[1] is not None:
            text(234, 177, str(old[1]), PANEL)
        text(234, 177, str(lines))
    return (score, lines, nxt)


def game():
    b = [[0] * CW for i in range(CH)]
    cls(OUT)
    for i in range(0, 210, 30):
        rect(0, i, 320, 15, (58, 25, 80))
    rbox(X0 - 4, Y0 - 4, CW * C + 8, CH * C + 8, 4, WHITE, 2, WELL)
    well = Well()
    well.show(b, None, True)
    rbox(4, 26, 96, 56, 6, GOLD, 2, PANEL)
    text(14, 48, "STACK", GOLD)
    text(14, 68, "DROP", GOLD)
    for i, cc in enumerate(COLS[:5]):
        rect(12 + i * 16, 96, 12, 12, dk(cc, 0.55))
        rect(12 + i * 16, 96, 11, 11, cc)
    rbox(4, 150, 96, 40, 6, (150, 110, 190), 2, PANEL)
    text(12, 167, "2nd key:", (200, 185, 230))
    text(12, 184, "drop it", (200, 185, 230))
    score = 0
    lines = 0
    nxt = random.randint(0, 6)
    p = None
    t = 0
    held = 0
    hc = 0
    sd = side(score, lines, nxt, None)
    while True:
        if p is None:
            p = [nxt, 0, 3, -1]
            nxt = random.randint(0, 6)
            sd = side(score, lines, nxt, sd)
            if not ok(b, p):
                message(["Score " + str(score), "Lines " + str(lines)], "Stacked to the top")
                return
            well.show(b, p)
        k = key()
        if k == CLR:
            return
        speed = max(2, 14 - lines // 5)
        q = list(p)
        if k == held and k:
            hc += 1
        else:
            hc = 0
        if k != held or k == DOWN or (k in (LEFT, RIGHT) and hc > 4 and hc % 2 == 0):
            if k == LEFT:
                q[2] -= 1
            elif k == RIGHT:
                q[2] += 1
            elif k == UP:
                q[1] = (q[1] + 1) % 4
                if not ok(b, q):
                    q[2] -= 1
                    if not ok(b, q):
                        q[2] += 2
            elif k == DOWN:
                t = speed
            elif k == SECOND:
                while ok(b, [q[0], q[1], q[2], q[3] + 1]):
                    q[3] += 1
                t = speed
        held = k
        t += 1
        fall = t >= speed
        if q != p and ok(b, q):
            p = q
            well.show(b, p)
        if fall:
            t = 0
            q = [p[0], p[1], p[2], p[3] + 1]
            if ok(b, q):
                p = q
                well.show(b, p)
            else:
                for x, y in get(p):
                    if y >= 0:
                        b[y][x] = p[0] + 1
                full = [y for y in range(CH) if 0 not in b[y]]
                if full:
                    for y in full:
                        del b[y]
                        b.insert(0, [0] * CW)
                    lines += len(full)
                    score += (0, 100, 300, 500, 800)[len(full)]
                    well.show(b, None, True)
                    sd = side(score, lines, nxt, sd)
                p = None
        pause(0.02)


RULES = "Shapes fall from the top. Fit them together to fill whole rows, which then clear. Don't let the stack reach the top."
KEYS = ['Left/Right: move', 'Up: turn', 'Down: drop faster', '2nd: drop all the way', 'CLEAR: quit']


def main():
    while True:
        c = home("GHBLOCKS", 'STACK DROP', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
