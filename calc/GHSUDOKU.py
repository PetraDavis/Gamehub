# Sudoku: fill the grid so every row, column and box has 1 to 9.
# Number keys type a digit, ENTER also counts up, DEL erases.
from GHLIB import *
import random

S = 20
X0 = 20
Y0 = 15


def make(holes):
    base = 3
    r = list(range(3))
    rows = [g * 3 + i for g in random.sample(r, 3) for i in random.sample(r, 3)]
    cols = [g * 3 + i for g in random.sample(r, 3) for i in random.sample(r, 3)]
    nums = random.sample(range(1, 10), 9)
    sol = [nums[(base * (rr % base) + rr // base + cc) % 9] for rr in rows for cc in cols]
    puz = sol[:]
    for i in random.sample(range(81), holes):
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


def cell(b, fixed, i, cur):
    x = X0 + (i % 9) * S
    y = Y0 + (i // 9) * S
    bg = (70, 55, 10) if i == cur else BLACK
    rect(x + 1, y + 1, S - 2, S - 2, bg)
    v = b[i]
    if v:
        c = WHITE if fixed[i] else (RED if clash(b, i) else GOLD)
        text(x + 5, y + 17, str(v), c)


def grid():
    for i in range(10):
        c = WHITE if i % 3 == 0 else DARK
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
    cls()
    grid()
    text(214, 30, "SUDOKU", GOLD)
    text(214, 70, "0-9 type", GREY)
    text(214, 90, "ENTER +1", GREY)
    text(214, 110, "DEL erase", GREY)
    text(214, 130, "CLEAR quit", GREY)
    cur = 0
    while fixed[cur]:
        cur += 1
    for i in range(81):
        cell(b, fixed, i, cur)
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
                    if not fixed[i] and b[i]:
                        cell(b, fixed, i, cur)
                if 0 not in b and valid(b):
                    message(["Every row, column and", "box is complete."], "Solved!")
                    return
        cell(b, fixed, old, cur)
        cell(b, fixed, cur, cur)


def main():
    while True:
        c = choose("SUDOKU", ["Easy", "Medium", "Hard", "Back"])
        if c < 0 or c == 3:
            return
        game((36, 46, 54)[c])
