# Super Tic-Tac-Toe: a 2-player game. The big board has 9 boxes and each box
# holds a small tic-tac-toe board. Where you play inside a small board sends
# the other player to that big box. Win a small board to take its big box;
# get three big boxes in a row to win the game.
from GHLIB import *

LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
X0 = 74
Y0 = 10
C = 19          # one small square
B = C * 3       # one big box
INK = (20, 20, 20)
LINE = (190, 190, 200)
XC = (215, 40, 40)
OC = (40, 90, 210)
TINT = ((235, 235, 235), (250, 215, 215), (215, 225, 250))


def winner(b):
    # 1 or 2 when that player has three in a row, 3 when full, else 0
    for a, c, d in LINES:
        if b[a] in (1, 2) and b[a] == b[c] == b[d]:
            return b[a]
    if 0 not in b:
        return 3
    return 0


def pos(g, s):
    # top-left corner of small square s inside big box g
    return X0 + (g % 3) * B + (s % 3) * C, Y0 + (g // 3) * B + (s // 3) * C


def grid():
    for k in range(1, 9):
        if k % 3:
            rect(X0 + k * C, Y0, 1, B * 3, LINE)
            rect(X0, Y0 + k * C, B * 3, 1, LINE)
    for k in range(4):
        rect(X0 + k * B - 1, Y0 - 1, 3, B * 3 + 3, INK)
        rect(X0 - 1, Y0 + k * B - 1, B * 3 + 3, 3, INK)


def box_frame(g, c):
    # the thick lines around big box g (g = -1: the whole board)
    if g < 0:
        x, y, w = X0, Y0, B * 3
    else:
        x, y, w = X0 + (g % 3) * B, Y0 + (g // 3) * B, B
    rect(x - 1, y - 1, w + 3, 3, c)
    rect(x - 1, y + w - 1, w + 3, 3, c)
    rect(x - 1, y + 2, 3, w - 3, c)
    rect(x + w - 1, y + 2, 3, w - 3, c)


def cursor(g, s, c):
    x, y = pos(g, s)
    rect(x + 2, y + 2, 16, 2, c)
    rect(x + 2, y + 16, 16, 2, c)
    rect(x + 2, y + 4, 2, 12, c)
    rect(x + 16, y + 4, 2, 12, c)


def mark(x, y, w, p):
    # an X or an O filling a w-sized square at x, y
    a = w // 4 + (w == C)
    e = w - a
    t = max(1, w // 12)
    if p == 1:
        col(XC)
        fill_poly([x + a - t, x + a + t, x + e + t, x + e - t], [y + a, y + a, y + e, y + e])
        fill_poly([x + e - t, x + e + t, x + a + t, x + a - t], [y + a, y + a, y + e, y + e])
    else:
        ring(x + w // 2, y + w // 2, w * 3 // 10, OC, t + 1, WHITE if w == C else TINT[2])


def take(g, p):
    # big box g is won (p = 1 or 2) or tied (p = 3): cover it with one colour
    x, y = X0 + (g % 3) * B, Y0 + (g // 3) * B
    rect(x + 2, y + 2, B - 3, B - 3, TINT[0 if p == 3 else p])
    if p < 3:
        mark(x + 2, y + 2, B - 3, p)


SHOWN = [""]


def status(s):
    o = SHOWN[0]
    if s == o:
        return
    ctext(196, o, WHITE)
    ctext(196, s, INK)
    SHOWN[0] = s


def game():
    cells = [[0] * 9 for _ in range(9)]
    big = [0] * 9
    cls(WHITE)
    SHOWN[0] = ""
    grid()
    turn = 1
    need = -1       # the big box the player must play in, -1 = anywhere
    g, s = 4, 4
    box_frame(need, GOLD)
    cursor(g, s, GOLD)
    while True:
        w = winner(big)
        if w == 3 or (not w and all(big[k] or 0 not in cells[k] for k in range(9))):
            w = 3
        if w:
            box_frame(need, INK)
            if not big[g]:
                cursor(g, s, WHITE)
            status(("It's a draw" if w == 3 else ("X" if w == 1 else "O") + " wins!") + " - ENTER")
            while wkey() not in (OK, CLR):
                pass
            return
        who = "X" if turn == 1 else "O"
        status(who + (": go anywhere" if need < 0 else ": play in the gold box"))
        k = wkey()
        og, os_ = g, s
        gx, gy = (g % 3) * 3 + s % 3, (g // 3) * 3 + s // 3
        if k == CLR:
            return
        if k in (LEFT, RIGHT, UP, DOWN):
            dx = (k == RIGHT) - (k == LEFT)
            dy = (k == DOWN) - (k == UP)
            nx, ny = gx + dx, gy + dy
            if need >= 0:
                # stay inside the gold box
                lo_x, lo_y = (need % 3) * 3, (need // 3) * 3
                ok = lo_x <= nx < lo_x + 3 and lo_y <= ny < lo_y + 3
            else:
                # jump over big boxes that are already won or tied
                while 0 <= nx < 9 and 0 <= ny < 9 and big[(ny // 3) * 3 + nx // 3]:
                    nx, ny = nx + 3 * dx, ny + 3 * dy
                ok = 0 <= nx < 9 and 0 <= ny < 9
            if ok:
                g, s = (ny // 3) * 3 + nx // 3, (ny % 3) * 3 + nx % 3
        elif k == OK and not big[g] and cells[g][s] == 0:
            cells[g][s] = turn
            cursor(g, s, WHITE)
            x, y = pos(g, s)
            mark(x, y, C, turn)
            r = winner(cells[g])
            if r:
                big[g] = r
                take(g, r)
            old = need
            need = -1 if big[s] else s
            turn = 3 - turn
            if need != old:
                box_frame(old, INK)
                box_frame(need, GOLD)
            if need >= 0:
                g = need
            elif big[g]:
                # pick a free square to start from when going anywhere
                g = [k for k in range(9) if not big[k]][0] if 0 in big else g
            if cells[g][s]:
                s = [k for k in range(9) if cells[g][k] == 0][0] if 0 in cells[g] else s
            cursor(g, s, GOLD)
            continue
        if (g, s) != (og, os_):
            cursor(og, os_, WHITE)
            cursor(g, s, GOLD)


RULES = "Where you play in a small board sends your friend to that big box. Win small boards to take boxes. Get 3 in a row!"
KEYS = ["Arrows: move  ENTER: place", "CLEAR: quit"]


def main():
    while True:
        c = home("GHSUPER", "SUPER TIC-TAC-TOE", RULES, KEYS, ("2 Players", "Back"))
        if c < 0:
            return
        game()
