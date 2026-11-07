# Simon: watch the colors light up, then repeat them with the arrow keys.
from GHLIB import *
import random

# arrow key -> pad index; pads: 0 up, 1 right, 2 down, 3 left
PADS = (
    (UP, 160, 60, (40, 160, 60), (120, 255, 140)),
    (RIGHT, 225, 110, (170, 40, 40), (255, 120, 120)),
    (DOWN, 160, 160, (40, 70, 170), (120, 170, 255)),
    (LEFT, 95, 110, (170, 140, 30), (255, 230, 100)),
)


def pad(i, lit):
    k, x, y, dim, bright = PADS[i]
    circ(x, y, 30, bright if lit else dim)
    if lit:
        ring(x, y, 30, WHITE, 3, bright)


def score(n):
    rect(0, 0, 320, 22, BLACK)
    text(6, 17, "Score " + str(n))
    text(204, 17, "CLEAR quit", GREY)


def flash(i, t):
    pad(i, True)
    pause(t)
    pad(i, False)
    pause(0.12)


def game():
    cls()
    for i in range(4):
        pad(i, False)
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
