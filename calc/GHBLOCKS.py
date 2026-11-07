# Stack Drop: fit the falling shapes together and fill rows to clear them.
# Left/Right move, Up turns, Down drops faster, 2nd drops all the way.
from GHLIB import *
import random

CW = 10
CH = 20
C = 9
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
    if c == BLACK:
        rect(px, py, C, C, BLACK)
    else:
        rect(px, py, C - 1, C - 1, c)


def draw_piece(p, c=None):
    for x, y in get(p):
        sq(x, y, COLS[p[0]] if c is None else c)


def board(b):
    for y in range(CH):
        for x in range(CW):
            v = b[y][x]
            sq(x, y, COLS[v - 1] if v else BLACK)


def side(score, lines, nxt):
    rect(230, 30, 90, 150, BLACK)
    text(232, 44, "NEXT", GREY)
    for x, y in get((nxt, 0, 0, 0)):
        rect(240 + x * 9, 56 + y * 9, 8, 8, COLS[nxt])
    text(232, 110, "SCORE", GREY)
    text(232, 128, str(score))
    text(232, 156, "LINES", GREY)
    text(232, 174, str(lines))


def game():
    b = [[0] * CW for i in range(CH)]
    cls()
    rbox(X0 - 4, Y0 - 4, CW * C + 8, CH * C + 8, 4, WHITE)
    text(6, 44, "STACK", GOLD)
    text(6, 62, "DROP", GOLD)
    text(6, 160, "2nd:", GREY)
    text(6, 178, "drop", GREY)
    score = 0
    lines = 0
    nxt = random.randint(0, 6)
    p = None
    t = 0
    held = 0
    hc = 0
    side(score, lines, nxt)
    while True:
        if p is None:
            p = [nxt, 0, 3, -1]
            nxt = random.randint(0, 6)
            side(score, lines, nxt)
            if not ok(b, p):
                message(["Score " + str(score), "Lines " + str(lines)], "Stacked to the top")
                return
            draw_piece(p)
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
            draw_piece(p, BLACK)
            p = q
            draw_piece(p)
        if fall:
            t = 0
            q = [p[0], p[1], p[2], p[3] + 1]
            if ok(b, q):
                draw_piece(p, BLACK)
                p = q
                draw_piece(p)
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
                    board(b)
                p = None
        pause(0.02)


def main():
    while True:
        c = choose("STACK DROP", ["Play", "Back"])
        if c != 0:
            return
        game()
