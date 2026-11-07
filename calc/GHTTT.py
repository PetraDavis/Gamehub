# Tic-Tac-Toe: play the calculator or a friend.
from GHLIB import *
import random

LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
X0 = 85
Y0 = 28
S = 50
INK = (20, 20, 20)


def winner(b):
    for a, c, d in LINES:
        if b[a] and b[a] == b[c] == b[d]:
            return b[a]
    if 0 not in b:
        return 3
    return 0


def cpu(b):
    for who in (2, 1):
        for a, c, d in LINES:
            v = [b[a], b[c], b[d]]
            if v.count(who) == 2 and v.count(0) == 1:
                return (a, c, d)[v.index(0)]
    if b[4] == 0:
        return 4
    free = [i for i in (0, 2, 6, 8) if b[i] == 0]
    if not free:
        free = [i for i in range(9) if b[i] == 0]
    return random.choice(free)


def cell(b, i, cur):
    x = X0 + (i % 3) * S
    y = Y0 + (i // 3) * S
    rect(x + 3, y + 3, S - 6, S - 6, WHITE)
    if i == cur:
        rbox(x + 3, y + 3, S - 6, S - 6, 6, GOLD, 3, WHITE)
    m = b[i]
    if m == 1:
        col(INK)
        for o in (-1, 0, 1):
            draw_line(x + 12 + o, y + 12, x + S - 12 + o, y + S - 12)
            draw_line(x + S - 12 + o, y + 12, x + 12 + o, y + S - 12)
    elif m == 2:
        ring(x + S // 2, y + S // 2, 15, INK, 3, WHITE)


def grid():
    for i in (1, 2):
        rect(X0 + i * S - 1, Y0, 3, S * 3, INK)
        rect(X0, Y0 + i * S - 1, S * 3, 3, INK)


def status(s):
    rect(0, 186, 320, 24, WHITE)
    ctext(203, s, INK)


def game(vs_cpu):
    b = [0] * 9
    cls(WHITE)
    grid()
    cur = 4
    turn = 1
    for i in range(9):
        cell(b, i, cur)
    while True:
        w = winner(b)
        if w:
            msg = "It's a draw" if w == 3 else ("X wins!" if w == 1 else ("Calculator wins" if vs_cpu else "O wins!"))
            status(msg + " - ENTER")
            while wkey() not in (OK, CLR):
                pass
            return
        if vs_cpu and turn == 2:
            status("Thinking...")
            pause(0.3)
            m = cpu(b)
            b[m] = 2
            cell(b, m, cur)
            turn = 1
            continue
        status(("X" if turn == 1 else "O") + " to move")
        k = wkey()
        old = cur
        if k == LEFT and cur % 3 > 0:
            cur -= 1
        elif k == RIGHT and cur % 3 < 2:
            cur += 1
        elif k == UP and cur > 2:
            cur -= 3
        elif k == DOWN and cur < 6:
            cur += 3
        elif k == CLR:
            return
        elif k == OK and b[cur] == 0:
            b[cur] = turn
            turn = 3 - turn
        cell(b, old, cur)
        cell(b, cur, cur)


RULES = 'Get three in a row (across, down or diagonal) before the other player. Play the calculator or pass to a friend.'
KEYS = ['Arrows: move', 'ENTER: place your mark', 'CLEAR: quit']


def main():
    while True:
        c = home("GHTTT", 'TIC-TAC-TOE', RULES, KEYS, ("vs Calc", "2 Players", "Back"))
        if c < 0:
            return
        game(c == 0)
