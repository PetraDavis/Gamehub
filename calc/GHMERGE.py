# 2048: slide the tiles and join matching numbers.
from GHLIB import *
import random

X0 = 90
Y0 = 26
S = 36
BOARD = (187, 173, 160)
TC = {0: (205, 193, 180), 2: (230, 225, 215), 4: (235, 220, 190), 8: (240, 170, 110), 16: (245, 140, 90),
      32: (245, 110, 85), 64: (245, 80, 50), 128: (235, 205, 110), 256: (235, 200, 90),
      512: (235, 195, 70), 1024: (235, 190, 50), 2048: (235, 185, 30)}


def add(b):
    e = [i for i in range(16) if b[i] == 0]
    if e:
        b[random.choice(e)] = 4 if random.random() < 0.1 else 2


def slide(row):
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
    return out + [0] * (4 - len(out)), pts


def move(b, d):
    # d: 0 left 1 right 2 up 3 down
    pts = 0
    nb = b[:]
    for j in range(4):
        if d < 2:
            idx = [j * 4 + i for i in range(4)]
        else:
            idx = [i * 4 + j for i in range(4)]
        if d == 1 or d == 3:
            idx.reverse()
        row, p = slide([b[i] for i in idx])
        pts += p
        for n in range(4):
            nb[idx[n]] = row[n]
    return nb, pts


def draw(b, score, old=None, oscore=-1):
    # only tiles that changed are drawn again, so the board doesn't flash.
    # Each drawing call is slow on the calculator, so a tile is two plain
    # rectangles and its number, and everything of one colour is drawn together.
    faces = []
    nums = []
    for i in range(16):
        v = b[i]
        if old and old[i] == v:
            continue
        x = X0 + (i % 4) * S
        y = Y0 + (i // 4) * S
        c = TC.get(v, (235, 180, 20))
        faces.append((c, x + 2, y + 2, S - 4, S - 6))
        faces.append((dk(c, 0.8), x + 2, y + S - 4, S - 4, 2))
        if v:
            s = str(v)
            if len(s) > 3:
                s = s[:2] + "k" if v >= 10000 else s
            nums.append(((60, 55, 50) if v < 8 else WHITE, x + S // 2 - len(s) * 5, y + 24, s))
    faces.sort()
    for c, x, y, w, h in faces:
        rect(x, y, w, h, c)
    nums.sort()
    for c, x, y, s in nums:
        text(x, y, s, c)
    if score != oscore:
        # only the number changes: write the old one in the pill colour
        if oscore >= 0:
            text(165, 200, str(oscore), BOARD)
        text(165, 200, str(score), WHITE)


def frame():
    cls(WHITE)
    rrect(12, 34, 64, 64, 8, dk((235, 185, 30), 0.8))
    rrect(12, 32, 64, 64, 8, (235, 185, 30))
    text(24, 70, "2048", WHITE)
    text(12, 128, "Join", (120, 110, 100))
    text(12, 146, "same", (120, 110, 100))
    text(12, 164, "tiles!", (120, 110, 100))
    text(250, 60, "Arrows", (120, 110, 100))
    text(250, 78, "slide", (120, 110, 100))
    rrect(X0 - 4, Y0 - 4, S * 4 + 8, S * 4 + 8, 8, BOARD)
    rrect(95, 182, 130, 24, 6, BOARD)
    text(105, 200, "Score", WHITE)


def game():
    b = [0] * 16
    add(b)
    add(b)
    score = 0
    frame()
    draw(b, score)
    won = False
    while True:
        k = wkey()
        d = {LEFT: 0, RIGHT: 1, UP: 2, DOWN: 3}.get(k, -1)
        if k == CLR:
            return
        if d < 0:
            continue
        nb, p = move(b, d)
        if nb != b:
            ob, osc = b, score
            b = nb
            score += p
            add(b)
            draw(b, score, ob, osc)
            if 2048 in b and not won:
                won = True
                message(["You made 2048!", "Keep going?"], "Amazing!")
                frame()
                draw(b, score)
        stuck = True
        for dd in range(4):
            if move(b, dd)[0] != b:
                stuck = False
        if stuck:
            message(["Final score " + str(score)], "No moves left")
            return


RULES = 'Slide the tiles. Two tiles with the same number join into one. Try to make 2048!'
KEYS = ['Arrows: slide all tiles', 'CLEAR: quit']


def main():
    while True:
        c = home("GHMERGE", '2048', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
