# Solitaire (Klondike, draw one).
# Arrows move. ENTER picks up a card, ENTER again puts it down.
# Up/Down in a column chooses how many cards to pick up.
# 2nd sends the card under the cursor to the top row if it fits.
from GHLIB import *
import random

CW = 40
CHT = 30
TOPY = 4
TABY = 40
RANKS = ("", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
CARD = (245, 245, 240)
BACK = (40, 80, 160)
FELT = (15, 70, 40)


def cx(c):
    return 6 + c * 44


def suit(x, y, s):
    if s == 0:  # heart
        col(RED)
        fill_circle(x - 2, y - 1, 3)
        fill_circle(x + 2, y - 1, 3)
        fill_poly([x - 5, x + 5, x], [y, y, y + 5])
    elif s == 1:  # diamond
        col(RED)
        fill_poly([x, x + 4, x, x - 4], [y - 5, y, y + 5, y])
    elif s == 2:  # spade
        col(BLACK)
        fill_circle(x - 2, y + 1, 3)
        fill_circle(x + 2, y + 1, 3)
        fill_poly([x - 5, x + 5, x], [y, y, y - 5])
        fill_rect(x - 1, y + 2, 2, 4)
    else:  # club
        col(BLACK)
        fill_circle(x, y - 3, 2)
        fill_circle(x - 3, y + 1, 2)
        fill_circle(x + 3, y + 1, 2)
        fill_rect(x - 1, y + 2, 2, 4)


def card(x, y, cd, h=CHT, sel=False):
    if cd is None:
        rbox(x, y, CW, CHT, 4, (60, 110, 80), 1, FELT)
        return
    r, s, up = cd
    edge = GOLD if sel else BLACK
    rrect(x, y, CW, h, 4, edge)
    if not up:
        rrect(x + 1, y + 1, CW - 2, h - 2, 3, BACK)
        rect(x + 3, y + 3, CW - 6, 1, lt(BACK, 0.5))
        if h >= 12:
            rect(x + 4, y + 4, CW - 8, h - 8, lt(BACK, 0.15))
            for i in range(x + 6, x + CW - 6, 6):
                rect(i, y + 6, 2, h - 12, BACK)
        return
    rrect(x + 1, y + 1, CW - 2, h - 2, 3, (255, 245, 200) if sel else CARD)
    t = RANKS[r]
    text(x + 3, y + 15, t, RED if s < 2 else BLACK)
    suit(x + 31 - (5 if len(t) > 1 else 0) + (5 if len(t) > 1 else 0), y + 9, s)
    if h >= CHT:
        suit(x + CW // 2, y + 22, s)


class G:
    pass


def new():
    g = G()
    deck = [[r, s, False] for s in range(4) for r in range(1, 14)]
    random.shuffle(deck)
    g.tab = []
    for c in range(7):
        pile = [deck.pop() for i in range(c + 1)]
        pile[-1][2] = True
        g.tab.append(pile)
    g.stock = deck
    g.waste = []
    g.found = [[], [], [], []]
    return g


def gap(pile):
    n = len(pile)
    up = 12
    while n > 1 and TABY + (n - 1) * up + CHT > 208 and up > 5:
        up -= 1
    return up


def draw_col(g, c, cur, depth, held):
    x = cx(c)
    rect(x, TABY, CW + 1, 210 - TABY, FELT)
    pile = g.tab[c]
    if not pile:
        card(x, TABY, None)
    up = gap(pile)
    for i in range(len(pile)):
        cd = pile[i]
        sel = (cur == 7 + c and i >= len(pile) - depth) or (held and held[0] == 7 + c and i >= len(pile) - held[1])
        last = i == len(pile) - 1
        card(x, TABY + i * up, cd, CHT if last else max(up + 4, 10), sel)


def draw_top(g, cur, held):
    rect(0, 0, 320, TABY - 2, FELT)
    x = cx(0)
    if g.stock:
        card(x, TOPY, [1, 0, False], CHT, cur == 0)
    else:
        card(x, TOPY, None)
        if cur == 0:
            rbox(x, TOPY, CW, CHT, 4, GOLD, 2, FELT)
    x = cx(1)
    if g.waste:
        card(x, TOPY, g.waste[-1], CHT, cur == 1 or (held and held[0] == 1))
    else:
        card(x, TOPY, None)
    for f in range(4):
        x = cx(3 + f)
        p = g.found[f]
        if p:
            card(x, TOPY, p[-1], CHT, cur == 3 + f)
        else:
            card(x, TOPY, None)
            if cur == 3 + f:
                rbox(x, TOPY, CW, CHT, 4, GOLD, 2, FELT)
            suit(x + 20, TOPY + 15, f)


def fits_found(cd, f, pile):
    if cd[1] != f:
        return False
    return cd[0] == (pile[-1][0] + 1 if pile else 1)


def fits_tab(cd, pile):
    if not pile:
        return cd[0] == 13
    t = pile[-1]
    return t[2] and t[0] == cd[0] + 1 and (t[1] < 2) != (cd[1] < 2)


def take(g, src, n):
    if src == 1:
        return [g.waste[-1]]
    return g.tab[src - 7][-n:]


def remove(g, src, n):
    if src == 1:
        g.waste.pop()
    else:
        p = g.tab[src - 7]
        del p[-n:]
        if p and not p[-1][2]:
            p[-1][2] = True


def try_move(g, src, n, dst):
    cards = take(g, src, n)
    if 3 <= dst <= 6:
        if n != 1 or not fits_found(cards[0], dst - 3, g.found[dst - 3]):
            return False
        remove(g, src, n)
        g.found[dst - 3].append(cards[0])
        return True
    if dst >= 7 and dst != src and fits_tab(cards[0], g.tab[dst - 7]):
        remove(g, src, n)
        g.tab[dst - 7].extend(cards)
        return True
    return False


def faceup(g, c):
    n = 0
    for cd in g.tab[c]:
        if cd[2]:
            n += 1
    return n


def game():
    g = new()
    cls(FELT)
    cur = 7
    depth = 1
    held = None
    redraw = list(range(7))
    top = True
    while True:
        if top:
            draw_top(g, cur, held)
        for c in redraw:
            draw_col(g, c, cur, depth if held is None else 0, held)
        redraw = []
        top = False
        if sum(len(f) for f in g.found) == 52:
            message(["All 52 cards are home."], "You win!")
            return
        k = wkey()
        old = cur
        if k == CLR:
            if held:
                held = None
                redraw = list(range(7))
                top = True
                continue
            if message(["ENTER: quit this game", "CLEAR: keep playing"], "Quit?") == OK:
                return
            cls(FELT)
            redraw = list(range(7))
            top = True
            continue
        if k == LEFT:
            cur = cur - 1 if cur not in (0, 7) else cur + 6
            if cur == 2:
                cur = 1
        elif k == RIGHT:
            cur = cur + 1 if cur not in (6, 13) else cur - 6
            if cur == 2:
                cur = 3
        elif k == DOWN and cur < 7:
            cur = 7 + (cur if cur != 1 else 1)
        elif k == UP and cur >= 7:
            if depth < faceup(g, cur - 7) and held is None:
                depth += 1
            else:
                cur = cur - 7 if cur - 7 != 2 else 1
        elif k == DOWN and cur >= 7 and depth > 1:
            depth -= 1
        elif k == OK:
            if held is None:
                if cur == 0:
                    if g.stock:
                        cd = g.stock.pop()
                        cd[2] = True
                        g.waste.append(cd)
                    else:
                        g.stock = g.waste[::-1]
                        for cd in g.stock:
                            cd[2] = False
                        g.waste = []
                    top = True
                elif cur == 1 and g.waste:
                    held = (1, 1)
                    top = True
                elif cur >= 7 and g.tab[cur - 7] and faceup(g, cur - 7) >= depth:
                    held = (cur, depth)
                    redraw.append(cur - 7)
            else:
                src, n = held
                held = None
                try_move(g, src, n, cur)
                redraw = list(range(7))
                top = True
        elif k == SECOND and held is None:
            src = cur if (cur == 1 or cur >= 7) else -1
            if src >= 0 and (src == 1 and g.waste or src >= 7 and g.tab[src - 7]):
                for f in range(4):
                    if try_move(g, src, 1, 3 + f):
                        break
                redraw = list(range(7))
                top = True
        if cur != old:
            depth = 1
            top = True
            if old >= 7:
                redraw.append(old - 7)
            if cur >= 7:
                redraw.append(cur - 7)
        elif k in (UP, DOWN) and cur >= 7:
            redraw.append(cur - 7)


RULES = 'Build four piles from Ace to King, one per suit. In the columns, stack cards down in alternating colors.'
KEYS = ['Arrows: move   ENTER: pick/put', 'Up/Down in a column: more cards', 'ENTER on the deck: draw', '2nd: send card to top piles', 'CLEAR: quit']


def main():
    while True:
        c = home("GHSOLI", 'SOLITAIRE', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
