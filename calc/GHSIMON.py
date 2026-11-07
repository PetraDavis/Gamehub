# Simon: watch the colors light up, then repeat them with the arrow keys.
from GHLIB import *
import random

import math

# Looks like the round toy: four colored quarters around a dark center.
# arrow key -> pad, going clockwise from the top left
CX = 160
CY = 116
RO = 84
RI = 36
PADS = (
    (UP, 2, (30, 130, 50), (110, 255, 130)),
    (RIGHT, 3, (150, 30, 30), (255, 110, 110)),
    (DOWN, 0, (30, 60, 150), (120, 170, 255)),
    (LEFT, 1, (160, 130, 20), (255, 235, 100)),
)
SHAPE = []


def shapes():
    # quarter q spans angle q*90 .. q*90+90 (0 = bottom right, screen y down)
    for q in range(4):
        # the quarter stops short of the dark gaps, so lighting it up never
        # has to draw the gaps again
        xs = []
        ys = []
        for r, order in ((RO, range(9)), (RI + 3, range(8, -1, -1))):
            for i in order:
                a = math.pi / 2 * (q + i / 8)
                dx = r * math.cos(a)
                dy = r * math.sin(a)
                xs.append(int(CX + (max(dx, 4) if q in (0, 3) else min(dx, -5))))
                ys.append(int(CY + (max(dy, 4) if q in (0, 1) else min(dy, -5))))
        SHAPE.append((xs, ys))


def gaps():
    d = (15, 15, 15)
    rect(CX - 4, CY - RO - 1, 8, RO - RI + 1, d)
    rect(CX - 4, CY + RI, 8, RO - RI + 1, d)
    rect(CX - RO - 1, CY - 4, RO - RI + 1, 8, d)
    rect(CX + RI, CY - 4, RO - RI + 1, 8, d)
    col(d)
    for r in (RI, RI + 1, RI + 2):
        draw_circle(CX, CY, r)


def pad(i, lit):
    k, q, dim, bright = PADS[i]
    col(bright if lit else dim)
    xs, ys = SHAPE[q]
    fill_poly(xs, ys)


def body():
    if not SHAPE:
        shapes()
    circ(CX, CY, RO + 8, (60, 60, 65))
    circ(CX, CY, RO + 5, (15, 15, 15))
    for i in range(4):
        pad(i, False)
    gaps()
    ring(CX, CY, RI, (15, 15, 15), 3, (70, 70, 75))


def score(n):
    # rub out only the old number, by writing it in the background colour
    if n:
        text(66, 17, str(n - 1), BLACK)
    else:
        text(204, 17, "CLEAR quit", GREY)
        text(6, 17, "Score")
    text(66, 17, str(n))
    if n:
        s = str(n - 1)
        text(CX - len(s) * 5, CY + 7, s, (25, 25, 28))
    else:
        circ(CX, CY, RI - 6, (25, 25, 28))
    s = str(n)
    text(CX - len(s) * 5, CY + 7, s, WHITE)


def flash(i, t):
    pad(i, True)
    pause(t)
    pad(i, False)
    pause(0.12)


def game():
    cls()
    body()
    seq = []
    while True:
        score(len(seq))
        seq.append(random.randint(0, 3))
        pause(0.5)
        t = max(0.18, 0.5 - len(seq) * 0.02)
        for i in seq:
            flash(i, t)
        for want in seq:
            k = wkey()
            if k == CLR:
                return
            got = -1
            for i in range(4):
                if PADS[i][0] == k:
                    got = i
            if got < 0:
                got = -2
            if got >= 0:
                flash(got, 0.15)
            if got != want:
                if got >= 0:
                    pass
                message(["You got " + str(len(seq) - 1) + " in a row."], "Wrong color!")
                return


RULES = 'Watch the colors light up, then repeat them in the same order. Each round adds one more.'
KEYS = ['Up: green   Right: red', 'Down: blue  Left: yellow', 'CLEAR: quit']


def main():
    while True:
        c = home("GHSIMON", 'SIMON', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
