# Sudoku: fill the grid so every row, column and box has 1 to 9.
# Number keys type a digit, ENTER also counts up, DEL erases.
from GHLIB import *
import random

S = 20
X0 = 20
Y0 = 15
INK = (20, 20, 20)
PEN = (40, 90, 200)


def make(holes):
    base = 3
    r = list(range(3))
    rows = [g * 3 + i for g in sample(r, 3) for i in sample(r, 3)]
    cols = [g * 3 + i for g in sample(r, 3) for i in sample(r, 3)]
    nums = sample(range(1, 10), 9)
    sol = [nums[(base * (rr % base) + rr // base + cc) % 9] for rr in rows for cc in cols]
    puz = sol[:]
    for i in sample(range(81), holes):
        puz[i] = 0
    return puz


def valid(b):
    for i in range(9):
        row = set(b[i * 9:i * 9 + 9])
        colm = set(b[i::9])
        bx = (i % 3) * 3 + (i // 3) * 27
        box = set(b[bx + o] for o in (0, 1, 2, 9, 10, 11, 18, 19, 20))
        for s in (row, colm, box):
            if s != set(range(1, 10)):
                return False
    return True


def clash(b, i):
    v = b[i]
    if not v:
        return False
    r = i // 9
    c = i % 9
    for j in range(81):
        if j != i and b[j] == v:
            if j // 9 == r or j % 9 == c or (j // 27 == i // 27 and (j % 9) // 3 == c // 3):
                return True
    return False


SHOWN = {}


def cell(b, fixed, i, cur):
    # draws only what changed in the cell: its number, the number's colour,
    # or the gold cursor outline (which sits around the number, never on it)
    x = X0 + (i % 9) * S
    y = Y0 + (i // 9) * S
    bg = FIX if fixed[i] else WHITE
    v = b[i]
    c = (INK if fixed[i] else (RED if clash(b, i) else PEN)) if v else None
    on = i == cur
    old = SHOWN.get(i)
    if old is None or old[0] != v:
        rect(x + 1, y + 1, S - 2, S - 2, bg)
        old = None
    if v and (old is None or old[1] != c):
        text(x + 5, y + 16, str(v), c)
    if old is None or old[2] != on:
        k = GOLD if on else bg
        rect(x + 1, y + 1, S - 2, 2, k)
        rect(x + 1, y + S - 3, S - 2, 2, k)
        rect(x + 1, y + 3, 2, S - 6, k)
        rect(x + S - 3, y + 3, 2, S - 6, k)
    SHOWN[i] = (v, c, on)


FIX = (236, 238, 246)


def first(b, fixed, cur):
    # the whole board in few calls (each one is slow on the calculator):
    # the shaded cells of a row joined into one strip, then the lines on top,
    # then each row's numbers as one line of text (cells are 20 px apart,
    # two characters)
    for r in range(9):
        c = 0
        while c < 9:
            if fixed[r * 9 + c]:
                e = c
                while e < 9 and fixed[r * 9 + e]:
                    e += 1
                rect(X0 + c * S, Y0 + r * S, (e - c) * S, S, FIX)
                c = e
            else:
                c += 1
    grid()
    for r in range(9):
        row = "".join([(str(b[r * 9 + c]) if b[r * 9 + c] else " ") + " " for c in range(9)])
        if row.strip():
            text(X0 + 5, Y0 + r * S + 16, row.rstrip(), INK)
    for i in range(81):
        v = b[i]
        SHOWN[i] = (v, (INK if fixed[i] else (RED if clash(b, i) else PEN)) if v else None, False)
    cell(b, fixed, cur, cur)


def grid():
    for i in range(10):
        c = INK if i % 3 == 0 else (150, 150, 150)
        t = 2 if i % 3 == 0 else 1
        if t == 2:
            rect(X0 + i * S - 1, Y0 - 1, 2, S * 9 + 2, c)
            rect(X0 - 1, Y0 + i * S - 1, S * 9 + 2, 2, c)
        else:
            col(c)
            draw_line(X0 + i * S, Y0, X0 + i * S, Y0 + S * 9)
            draw_line(X0, Y0 + i * S, X0 + S * 9, Y0 + i * S)


def game(holes):
    b = make(holes)
    fixed = [v != 0 for v in b]
    cls(WHITE)
    rbox(208, 12, 106, 30, 8, PEN, 2, (225, 235, 252))
    text(222, 33, "SUDOKU", PEN)
    text(214, 70, "0-9 type", GREY)
    text(214, 90, "ENTER +1", GREY)
    text(214, 110, "DEL erase", GREY)
    text(214, 130, "CLEAR quit", GREY)
    SHOWN.clear()
    cur = 0
    while fixed[cur]:
        cur += 1
    first(b, fixed, cur)
    while True:
        k = wkey()
        old = cur
        if k == LEFT and cur % 9:
            cur -= 1
        elif k == RIGHT and cur % 9 < 8:
            cur += 1
        elif k == UP and cur > 8:
            cur -= 9
        elif k == DOWN and cur < 72:
            cur += 9
        elif k == CLR:
            return
        elif not fixed[cur]:
            v = -1
            if k in NUMS:
                v = NUMS[k]
            elif k == OK:
                v = (b[cur] % 9) + 1
            elif k == DEL:
                v = 0
            if v >= 0:
                b[cur] = v
                for i in range(81):
                    if not fixed[i]:
                        cell(b, fixed, i, cur)
                if 0 not in b and valid(b):
                    message(["Every row, column and", "box is complete."], "Solved!")
                    return
        cell(b, fixed, old, cur)
        cell(b, fixed, cur, cur)


RULES = 'Fill the grid so every row, column and 3x3 box has the numbers 1 to 9 once. Red numbers clash.'
KEYS = ['Arrows: move', '0-9: type a number', 'ENTER: count up  DEL: erase', 'CLEAR: quit']


def main():
    while True:
        c = home("GHSUDOKU", 'SUDOKU', RULES, KEYS, ("Easy", "Medium", "Hard", "Back"))
        if c < 0:
            return
        game((36, 46, 54)[c])
