# Solitaire (Klondike, draw one).
# Arrows move. ENTER picks up a card, ENTER again puts it down.
# Up/Down in a column chooses how many cards to pick up.
# 2nd sends the card under the cursor to the top row if it fits.
from GHLIB import *

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


# the four suits as 7x7 pictures: heart, diamond, spade, club
PICS = (
    (".##.##.", "#######", "#######", "#######", ".#####.", "..###..", "...#..."),
    ("...#...", "..###..", ".#####.", "#######", ".#####.", "..###..", "...#..."),
    ("...#...", "..###..", ".#####.", "#######", "#######", "..#.#..", ".#####."),
    ("..###..", "..###..", "##.#.##", "#######", "##.#.##", "...#...", ".#####."),
)


def _runs(pic):
    # the picture as rectangles: runs of # in a row, joined with the same run below
    out = []
    for r in range(7):
        row = pic[r]
        c = 0
        while c < 7:
            if row[c] == "#":
                e = c
                while e < 7 and row[e] == "#":
                    e += 1
                for k in range(len(out)):
                    a = out[k]
                    if a[0] == c and a[2] == e - c and a[1] + a[3] == r:
                        out[k] = (a[0], a[1], a[2], a[3] + 1)
                        break
                else:
                    out.append((c, r, e - c, 1))
                c = e
            else:
                c += 1
    return out


SUITS = [_runs(p) for p in PICS]


def suit(x, y, s, k=1):
    # suit s with its top left corner at x, y, k pixels per dot
    c = RED if s < 2 else BLACK
    for a, b, w, h in SUITS[s]:
        rect(x + a * k, y + b * k, w * k, h * k, c)


def card(x, y, cd, h=CHT):
    if cd is None:
        rbox(x, y, CW, CHT, 4, (60, 110, 80), 1, FELT)
        return
    r, s, up = cd
    rrect(x, y, CW, h, 4, BLACK)
    if not up:
        rrect(x + 1, y + 1, CW - 2, h - 2, 3, BACK)
        if h >= 12:
            rect(x + 4, y + 4, CW - 8, h - 8, lt(BACK, 0.15))
            for i in range(x + 7, x + CW - 6, 6):
                rect(i, y + 6, 2, h - 12, BACK)
        return
    rrect(x + 1, y + 1, CW - 2, h - 2, 3, CARD)
    if h >= 14:
        text(x + 3, y + 14, RANKS[r], RED if s < 2 else BLACK)
        suit(x + CW - 11, y + 4, s)
    if h >= CHT:
        suit(x + 13, y + 15, s, 2)


class G:
    pass


def new():
    g = G()
    deck = [[r, s, False] for s in range(4) for r in range(1, 14)]
    shuffle(deck)
    g.tab = []
    for c in range(7):
        pile = [deck.pop() for i in range(c + 1)]
        pile[-1][2] = True
        g.tab.append(pile)
    g.stock = deck
    g.waste = []
    g.found = [[], [], [], []]
    return g


def layout(pile):
    # where each card of a column starts: hidden cards overlap more, and the
    # face-up ones leave room to read their corner. Tighter when it's long.
    dn, fu = 5, 15
    while True:
        ys = []
        y = TABY
        for cd in pile:
            ys.append(y)
            y += fu if cd[2] else dn
        if not pile or ys[-1] + CHT <= 208 or fu <= 8:
            return ys
        fu -= 1
        if fu < 12:
            dn = 3


def draw_col(g, c, drawn):
    # draw only the cards of column c that changed since last time
    pile = g.tab[c]
    x = cx(c)
    ys = layout(pile)
    n = len(pile)
    d = drawn[c]
    start = 0
    if d is not None and n:
        old = d[0]
        while start < min(len(old), n) and old[start] == ys[start]:
            start += 1
        start = min(start, max(0, min(len(old), n) - 1))
    if not pile:
        card(x, TABY, None)
        bottom = TABY + CHT
    else:
        bottom = ys[-1] + CHT
        if d is not None and n < len(d[0]) and start == n - 1:
            # the card under the ones taken away shows in full again
            rect(x, bottom - 6, CW, 6, FELT)
        for i in range(start, n):
            card(x, ys[i], pile[i], CHT if i == n - 1 else ys[i + 1] - ys[i] + 4)
    if d is None or bottom < d[1]:
        rect(x, bottom, CW, 210 - bottom, FELT)
    drawn[c] = (ys, bottom)


def top_state(g, s):
    if s == 0:
        return len(g.stock) > 0
    p = g.waste if s == 1 else g.found[s - 3]
    return tuple(p[-1]) if p else None


def draw_slot(g, s):
    x = cx(s)
    if s == 0:
        card(x, TOPY, [1, 0, False] if g.stock else None)
        return
    p = g.waste if s == 1 else g.found[s - 3]
    card(x, TOPY, p[-1] if p else None)
    if s > 1 and not p:
        suit(x + 13, TOPY + 8, s - 3, 2)


def frame(x, y, h, top=True):
    # a 2-pixel outline just outside a card, in the felt between the columns
    t = 2 if top else 0
    r = [(x - 2, y - t, 2, h + t + 2), (x + CW, y - t, 2, h + t + 2), (x, y + h, CW, 2)]
    if top:
        r.append((x, y - 2, CW, 2))
    return r


def marks(g, s, n):
    # the outline around slot s, or around the last n cards of a column
    if s < 7:
        return frame(cx(s), TOPY, CHT)
    p = g.tab[s - 7]
    if not p:
        return frame(cx(s - 7), TABY, CHT)
    ys = layout(p)
    i = max(0, len(p) - n)
    return frame(cx(s - 7), ys[i], ys[-1] + CHT - ys[i], i == 0)


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
    cols = [None] * 7
    tops = [-1] * 7
    shown = []
    while True:
        # what the outlines should be now: white for the held cards, gold for the cursor
        want = []
        if held:
            want += [(r, WHITE) for r in marks(g, held[0], held[1])]
        want += [(r, GOLD) for r in marks(g, cur, depth if held is None else 1)]
        busy = want != shown
        for r, c in shown:
            if (r, c) not in want:
                rect(r[0], r[1], r[2], r[3], FELT)
        for s in (0, 1, 3, 4, 5, 6):
            st = top_state(g, s)
            if st != tops[s]:
                draw_slot(g, s)
                tops[s] = st
                busy = True
        for c in range(7):
            p = g.tab[c]
            if cols[c] is None or cols[c][2] != [tuple(cd) for cd in p]:
                draw_col(g, c, cols)
                cols[c] = cols[c] + ([tuple(cd) for cd in p],)
                busy = True
        if busy:
            for r, c in want:
                rect(r[0], r[1], r[2], r[3], c)
            shown = want
        if sum(len(f) for f in g.found) == 52:
            message(["All 52 cards are home."], "You win!")
            return
        k = wkey()
        old = cur
        if k == CLR:
            if held:
                held = None
                continue
            if message(["ENTER: quit this game", "CLEAR: keep playing"], "Quit?") == OK:
                return
            cls(FELT)
            cols = [None] * 7
            tops = [-1] * 7
            shown = []
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
            cur = 7 + cur
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
                elif cur == 1 and g.waste:
                    held = (1, 1)
                elif cur >= 7 and g.tab[cur - 7] and faceup(g, cur - 7) >= depth:
                    held = (cur, depth)
            else:
                src, n = held
                held = None
                try_move(g, src, n, cur)
        elif k == SECOND and held is None:
            src = cur if (cur == 1 or cur >= 7) else -1
            if src >= 0 and (src == 1 and g.waste or src >= 7 and g.tab[src - 7]):
                for f in range(4):
                    if try_move(g, src, 1, 3 + f):
                        break
        if cur != old:
            depth = 1
        if cur >= 7 and depth > max(1, faceup(g, cur - 7)):
            depth = max(1, faceup(g, cur - 7))


RULES = 'Build four piles from Ace to King, one per suit. In the columns, stack cards down in alternating colors.'
KEYS = ['Arrows: move   ENTER: pick/put', 'Up/Down in a column: more cards', 'ENTER on the deck: draw', '2nd: send card to top piles', 'CLEAR: quit']


def main():
    while True:
        c = home("GHSOLI", 'SOLITAIRE', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
