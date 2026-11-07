# Wing It: tap UP (or 2nd) to flap through the gaps between the trees.
from GHLIB import *
import random

GAP = 64
TW = 26
SKY = (110, 195, 240)
TREE = (50, 140, 60)
LEAF = (40, 115, 50)
INK = (20, 20, 20)


def _bar(x, y, w, h, c):
    # rect clipped to the screen
    x0 = max(0, x)
    w = min(320, x + w) - x0
    if w >= 2 and h >= 1:
        rect(x0, y, w, h, c)


def _blob(x, y, r, c):
    # a round clump of leaves, only when it fits on the screen
    if r <= x <= 319 - r:
        circ(x, y, r, c)


def tree(x, gy, c):
    if x > 322 or x + TW + 3 < 0:
        return
    hi = lt(c)
    lo = dk(c, 0.75)
    cx = x + TW // 2
    # clear what the last frame left around the round parts
    top = gy + GAP
    y0 = max(22, gy - 27)
    _bar(x - 3, y0, TW + 9, gy + 1 - y0, SKY)
    _bar(x - 3, top, TW + 9, 24, SKY)
    _bar(cx + 5, top + 18, 5, 196 - top - 18, SKY)
    # leaves hanging from above, with a bumpy lower edge
    if gy - 14 > 22:
        _bar(x, 22, TW, gy - 36, lo)
        _bar(x + 3, 22, TW - 6, gy - 36, c)
    for bx, by, r in ((x + 5, gy - 18, 8), (x + TW - 5, gy - 16, 8), (cx, gy - 9, 9)):
        if by - r >= 22:
            _blob(bx, by, r, c)
        else:
            _bar(bx - r, 22, 2 * r, by + r - 22, c)
    _blob(cx - 3, gy - 12, 3, hi)
    # a tree from the ground: round crown on a trunk
    trunk = (110, 75, 40)
    _bar(cx - 5, top + 18, 10, 196 - top - 18, trunk)
    _bar(cx + 2, top + 18, 3, 196 - top - 18, dk(trunk))
    for bx, by, r in ((x + 5, top + 14, 8), (x + TW - 5, top + 14, 8), (cx, top + 9, 10)):
        _blob(bx, by, r, c)
    _blob(cx - 3, top + 6, 3, hi)
    _blob(x + 6, top + 13, 2, hi)


def bird(x, y, c, wing):
    if c == SKY:
        rect(x - 8, max(22, y - 8), 20, 17, SKY)
        return
    circ(x, y, 8, (170, 120, 20))
    circ(x, y, 7, c)
    rect(x - 7, y - 1 + wing, 6, 3, (255, 245, 190))
    circ(x + 3, y - 3, 3, WHITE)
    circ(x + 4, y - 3, 1, BLACK)
    rect(x + 7, y - 1, 5, 3, (245, 140, 30))


def ground():
    rect(0, 196, 320, 5, (70, 170, 80))
    rect(0, 201, 320, 9, (120, 80, 40))
    for x in range(0, 320, 16):
        rect(x + 4, 197, 3, 1, (110, 200, 110))
        rect(x + 10, 198, 2, 2, (40, 120, 50))
        rect(x + 7, 204, 3, 2, (95, 60, 30))
        rect(x + 1, 207, 2, 2, (150, 105, 60))


def game():
    cls(SKY)
    ground()
    rect(0, 20, 320, 2, INK)
    trees = [[330, random.randint(40, 120)], [330 + 170, random.randint(40, 120)]]
    y = 100.0
    v = 0.0
    score = 0
    passed = [False, False]
    text(6, 17, "Score 0", INK)
    held = False
    wing = 0
    while True:
        k = key()
        if k == CLR:
            return
        if (k == UP or k == SECOND or k == OK) and not held:
            v = -5.2
            wing = 3
        held = k in (UP, SECOND, OK)
        oy = y
        v = min(7, v + 0.55)
        y += v
        bird(60, int(oy), SKY, 0)
        for i in range(2):
            t = trees[i]
            # erase the strip the tree leaves behind
            _bar(t[0] + TW - 1, 22, 6, 174, SKY)
            t[0] -= 4
            if t[0] + TW + 3 < 0:
                t[0] = 330
                t[1] = random.randint(40, 120)
                passed[i] = False
            tree(t[0], t[1], TREE)
            if not passed[i] and t[0] + TW < 52:
                passed[i] = True
                score += 1
                rect(0, 0, 320, 20, SKY)
                text(6, 17, "Score " + str(score), INK)
        wing = max(0, wing - 1)
        bird(60, int(y), YELLOW, wing)
        hit = y > 189 or y < 28
        for t in trees:
            if t[0] - 9 < 60 < t[0] + TW + 9 and not (t[1] + 7 < y < t[1] + GAP - 7):
                hit = True
        if hit:
            pause(0.4)
            message(["You passed " + str(score) + " trees."], "Crash!")
            return


RULES = "Flap to fly through the gaps between the trees. Don't hit the trees or the ground."
KEYS = ['Up, 2nd or ENTER: flap', 'CLEAR: quit']


def main():
    while True:
        c = home("GHFLAP", 'WING IT', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
