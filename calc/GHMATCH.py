# Memory Match: 16 cards lie face down, 8 pairs of pictures. Turn two over;
# if they match they stay up. Find every pair in as few tries as you can.
from GHLIB import *

TABLE = (30, 90, 80)
BACKC = (200, 70, 90)
FACE = (250, 245, 230)
CW, CH = 50, 38
X0, Y0 = 37, 30
DX, DY = 64, 45
SYMS = ("heart", "star", "moon", "sun", "drop", "leaf", "gem", "bolt")


def pos(i):
    return X0 + (i % 4) * DX, Y0 + (i // 4) * DY


def back(i):
    x, y = pos(i)
    rect(x, y, CW, CH, BACKC)
    rect(x + 5, y + 5, CW - 10, CH - 10, lt(BACKC, 0.25))
    rect(x + 8, y + 8, CW - 16, CH - 16, BACKC)


def pic(kind, x, y):
    # each picture is a couple of shapes centred on x, y
    if kind == "heart":
        circ(x - 4, y - 3, 5, RED)
        circ(x + 4, y - 3, 5, RED)
        fill_poly([x - 9, x + 9, x], [y - 1, y - 1, y + 9])
    elif kind == "star":
        col(GOLD)
        fill_poly([x, x + 3, x + 10, x + 4, x + 6, x, x - 6, x - 4, x - 10, x - 3],
                  [y - 10, y - 3, y - 3, y + 2, y + 9, y + 5, y + 9, y + 2, y - 3, y - 3])
    elif kind == "moon":
        circ(x, y, 9, (120, 110, 200))
        circ(x + 4, y - 2, 8, FACE)
    elif kind == "sun":
        rect(x - 11, y - 1, 22, 2, (245, 150, 30))
        rect(x - 1, y - 11, 2, 22, (245, 150, 30))
        circ(x, y, 6, (245, 190, 40))
    elif kind == "drop":
        circ(x, y + 3, 6, (60, 130, 220))
        fill_poly([x - 6, x + 6, x], [y + 2, y + 2, y - 10])
    elif kind == "leaf":
        col((60, 160, 70))
        fill_poly([x - 9, x - 2, x + 9, x + 2], [y + 8, y - 6, y - 9, y + 5])
        rect(x - 10, y + 7, 3, 3, (60, 160, 70))
    elif kind == "gem":
        col((170, 80, 210))
        fill_poly([x - 9, x - 5, x + 5, x + 9, x], [y - 3, y - 8, y - 8, y - 3, y + 9])
        rect(x - 5, y - 5, 10, 2, lt((170, 80, 210), 0.4))
    elif kind == "bolt":
        col((40, 40, 50))
        fill_poly([x + 2, x - 7, x - 1, x - 4, x + 7, x + 1], [y - 10, y + 1, y + 1, y + 10, y - 2, y - 2])


def face(i, kind):
    x, y = pos(i)
    rect(x, y, CW, CH, FACE)
    pic(kind, x + CW // 2, y + CH // 2)


def frame(i, c):
    # a 2-pixel outline just outside a card, in the table between the cards
    x, y = pos(i)
    rect(x - 3, y - 3, CW + 6, 2, c)
    rect(x - 3, y + CH + 1, CW + 6, 2, c)
    rect(x - 3, y - 1, 2, CH + 2, c)
    rect(x + CW + 1, y - 1, 2, CH + 2, c)


HUD = [None]


def hud(tries):
    if HUD[0] is None:
        text(6, 17, "Tries", GOLD)
    else:
        text(66, 17, str(HUD[0]), TABLE)
    text(66, 17, str(tries))
    HUD[0] = tries


def game():
    cards = list(SYMS) * 2
    shuffle(cards)
    up = [False] * 16
    cls(TABLE)
    text(190, 17, "Pairs 0/8", WHITE)
    HUD[0] = None
    hud(0)
    for i in range(16):
        back(i)
    tries = 0
    pairs = 0
    sel = 0
    first = -1
    frame(sel, GOLD)
    while pairs < 8:
        k = wkey()
        old = sel
        if k == CLR:
            if message(["ENTER: quit this game", "CLEAR: keep playing"], "Quit?") == OK:
                return
            cls(TABLE)
            HUD[0] = None
            hud(tries)
            text(190, 17, "Pairs " + str(pairs) + "/8", WHITE)
            for i in range(16):
                if up[i] or i == first:
                    face(i, cards[i])
                else:
                    back(i)
            frame(sel, GOLD)
            continue
        if k == LEFT:
            sel = sel - 1 if sel % 4 else sel + 3
        elif k == RIGHT:
            sel = sel + 1 if sel % 4 < 3 else sel - 3
        elif k == UP:
            sel = (sel - 4) % 16
        elif k == DOWN:
            sel = (sel + 4) % 16
        elif k in (OK, SECOND) and not up[sel] and sel != first:
            face(sel, cards[sel])
            if first < 0:
                first = sel
                continue
            tries += 1
            hud(tries)
            if cards[first] == cards[sel]:
                up[first] = up[sel] = True
                pairs += 1
                text(190, 17, "Pairs " + str(pairs - 1) + "/8", TABLE)
                text(190, 17, "Pairs " + str(pairs) + "/8", WHITE)
            else:
                pause(0.9)
                back(first)
                back(sel)
            first = -1
            continue
        if sel != old:
            frame(old, TABLE)
            frame(sel, GOLD)
    pause(0.5)
    message(["You found all 8 pairs", "in " + str(tries) + " tries."], "Well done!")


RULES = "Turn over two cards. If the pictures match, they stay face up. Find all 8 pairs in as few tries as you can."
KEYS = ["Arrows: move", "ENTER: turn a card over", "CLEAR: quit"]


def main():
    while True:
        c = home("GHMATCH", "MEMORY MATCH", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
