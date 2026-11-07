# Wing It: tap UP (or 2nd) to flap through the gaps between the trees.
from GHLIB import *
import random

GAP = 64
TW = 26
SKY = (10, 14, 30)
TREE = (40, 120, 60)


def tree(x, gy, c):
    if x > 319 or x + TW < 0:
        return
    x0 = max(0, x)
    w = min(320, x + TW) - x0
    if w < 2:
        return
    if gy > 24:
        rect(x0, 22, w, gy - 22, c)
    rect(x0, gy + GAP, w, 196 - gy - GAP, c)


def bird(x, y, c, wing):
    if c == SKY:
        rect(x - 8, max(22, y - 8), 20, 17, SKY)
        return
    circ(x, y, 7, c)
    if True:
        circ(x + 3, y - 2, 2, BLACK)
        rect(x + 6, y, 5, 3, (240, 140, 40))
        rect(x - 6, y - 1 + wing, 6, 3, WHITE)


def game():
    cls(SKY)
    rect(0, 196, 320, 14, (90, 60, 30))
    rect(0, 0, 320, 22, BLACK)
    trees = [[330, random.randint(40, 120)], [330 + 170, random.randint(40, 120)]]
    y = 100.0
    v = 0.0
    score = 0
    passed = [False, False]
    text(6, 17, "Score 0")
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
            rect(max(0, t[0] + TW - 4), 22, 4, 174, SKY)
            t[0] -= 4
            if t[0] + TW < 0:
                t[0] = 330
                t[1] = random.randint(40, 120)
                passed[i] = False
            tree(t[0], t[1], TREE)
            if not passed[i] and t[0] + TW < 52:
                passed[i] = True
                score += 1
                rect(0, 0, 320, 22, BLACK)
                text(6, 17, "Score " + str(score))
        wing = max(0, wing - 1)
        bird(60, int(y), YELLOW, wing)
        hit = y > 189 or y < 28
        for t in trees:
            if t[0] - 7 < 60 < t[0] + TW + 7 and not (t[1] + 7 < y < t[1] + GAP - 7):
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
