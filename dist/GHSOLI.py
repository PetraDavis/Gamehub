# GHSOLI from GAMEHUB, on its own. Run it.
from ti_draw import *
from ti_system import *
import time
import random
import math
UP = 25
DOWN = 34
LEFT = 24
RIGHT = 26
OK = 105
CLR = 45
SECOND = 21
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (230, 180, 40)
GREY = (110, 110, 110)
RED = (220, 50, 50)
H = 210
def wkey():
    return wait_key()
def col(c):
    set_color(c[0], c[1], c[2])
def rect(x, y, w, h, c):
    if w < 2 or h < 2:
        if w < 1 or h < 1:
            return
        col(c)
        draw_line(x, y, x + w - 1, y + h - 1)
        return
    col(c)
    fill_rect(x, y, w, h)
def cls(c=BLACK):
    col(c)
    fill_rect(-1, -1, 322, 212)
def text(x, y, s, c=WHITE):
    col(c)
    draw_text(x, y, s)
def ctext(y, s, c=WHITE, cx=160):
    col(c)
    draw_text(cx - len(s) * 5, y, s)
def circ(x, y, r, c):
    col(c)
    fill_circle(x, y, r)
def lt(c, k=0.35):
    return (int(c[0] + (255 - c[0]) * k), int(c[1] + (255 - c[1]) * k), int(c[2] + (255 - c[2]) * k))
def ring(x, y, r, c, t=2, inner=BLACK):
    col(c)
    fill_circle(x, y, r)
    col(inner)
    fill_circle(x, y, r - t)
def rrect(x, y, w, h, r, c):
    col(c)
    fill_rect(x + r, y, w - 2 * r, h)
    fill_rect(x, y + r, w, h - 2 * r)
    fill_circle(x + r, y + r, r)
    fill_circle(x + w - r - 1, y + r, r)
    fill_circle(x + r, y + h - r - 1, r)
    fill_circle(x + w - r - 1, y + h - r - 1, r)
def rbox(x, y, w, h, r, c, t=2, inner=BLACK):
    rrect(x, y, w, h, r, c)
    rrect(x + t, y + t, w - 2 * t, h - 2 * t, max(r - t, 2), inner)
def message(lines, title=None):
    n = len(lines) + (1 if title else 0)
    h = n * 18 + 30
    y = (H - h) // 2
    rbox(20, y, 280, h, 8, WHITE)
    yy = y + 24
    if title:
        ctext(yy, title, GOLD)
        yy += 18
    for s in lines:
        ctext(yy, s)
        yy += 18
    while True:
        k = wkey()
        if k in (OK, CLR):
            return k
def _wrap(s, n=30):
    out = []
    line = ''
    for w in s.split(' '):
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = (line + ' ' + w).strip()
    if line:
        out.append(line)
    return out
def how_to(title, rules, buttons):
    cls()
    ctext(20, 'HOW TO PLAY', GOLD)
    ctext(38, title, GREY)
    y = 60
    for ln in _wrap(rules):
        text(8, y, ln)
        y += 16
    y += 6
    text(8, y, 'BUTTONS', GOLD)
    y += 17
    for b in buttons:
        text(8, y, b)
        y += 16
    text(8, 206, 'ENTER: back', GREY)
    while wkey() not in (OK, CLR, UP, DOWN):
        pass
def home(mod, title, rules, buttons, opts=('Play', 'Back'), sel=0):
    n = len(opts)
    while True:
        cls()
        ring(160, 58, 36, GOLD, 3)
        try:
            circ(160, 58, 33, icons_bg(mod))
            icons_draw(mod, 160, 58, WHITE)
        except Exception:
            pass
        ctext(122, title, GOLD)
        ctext(146, 'Up/Down: how to play', GREY)
        bw = (300 - (n - 1) * 8) // n
        while True:
            for i in range(n):
                x = 10 + i * (bw + 8)
                c = GOLD if i == sel else WHITE
                rect(x, 166, bw, 28, BLACK)
                rbox(x, 166, bw, 28, 10, c)
                text(x + bw // 2 - len(opts[i]) * 5, 186, opts[i], c)
            k = wkey()
            if k == LEFT:
                sel = (sel - 1) % n
            elif k == RIGHT:
                sel = (sel + 1) % n
            elif k in (UP, DOWN):
                how_to(title, rules, buttons)
                break
            elif k == CLR:
                return -1
            elif k == OK:
                if opts[sel] == 'Back':
                    return -1
                return sel
icons_BLACK = (0, 0, 0)
icons_INK = (20, 20, 20)
icons_RED = (215, 40, 40)
icons_BG = {'GHSOLI': (25, 110, 55)}
def icons_c_(c):
    set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
    icons_c_(c)
    fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))
def icons_circ(x, y, r, c):
    icons_c_(c)
    fill_circle(int(x), int(y), int(r))
def icons_poly(xs, ys, c):
    icons_c_(c)
    fill_poly([int(v) for v in xs], [int(v) for v in ys])
def icons_heart(x, y, s, c):
    icons_circ(x - s, y - 1, s, c)
    icons_circ(x + s, y - 1, s, c)
    icons_poly([x - 2 * s, x + 2 * s + 1, x], [y, y, y + 2 * s + 1], c)
def icons_diamond(x, y, s, c):
    icons_poly([x, x + s + 1, x, x - s - 1], [y - 2 * s, y, y + 2 * s, y], c)
def icons_spade(x, y, s, c):
    icons_circ(x - s, y + 1, s, c)
    icons_circ(x + s, y + 1, s, c)
    icons_poly([x - 2 * s, x + 2 * s + 1, x], [y + 1, y + 1, y - 2 * s - 1], c)
    icons_poly([x, x - s, x + s], [y + 1, y + 2 * s + 1, y + 2 * s + 1], c)
def icons_solitaire(x, y, c):
    suits = ((icons_spade, icons_INK), (icons_diamond, icons_RED), (icons_heart, icons_RED))
    for i in range(3):
        l = x - 18 + i * 10
        t = y - 12
        icons_box(l - 1, t - 1, 18, 26, icons_INK)
        icons_box(l, t, 16, 24, (250, 250, 245))
        f, col = suits[i]
        f(l + 4, t + 5, 2, col)
    icons_heart(x + 10, y + 3, 3, icons_RED)
icons_ICONS = {'GHSOLI': icons_solitaire}
def icons_bg(mod):
    return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
    f = icons_ICONS.get(mod)
    if f:
        f(x, y, c)
soli_CW = 40
soli_CHT = 30
soli_TOPY = 4
soli_TABY = 40
soli_RANKS = ('', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
soli_CARD = (245, 245, 240)
soli_BACK = (40, 80, 160)
soli_FELT = (15, 70, 40)
def soli_cx(c):
    return 6 + c * 44
def soli_suit(x, y, s):
    if s == 0:
        col(RED)
        fill_circle(x - 2, y - 1, 3)
        fill_circle(x + 2, y - 1, 3)
        fill_poly([x - 5, x + 5, x], [y, y, y + 5])
    elif s == 1:
        col(RED)
        fill_poly([x, x + 4, x, x - 4], [y - 5, y, y + 5, y])
    elif s == 2:
        col(BLACK)
        fill_circle(x - 2, y + 1, 3)
        fill_circle(x + 2, y + 1, 3)
        fill_poly([x - 5, x + 5, x], [y, y, y - 5])
        fill_rect(x - 1, y + 2, 2, 4)
    else:
        col(BLACK)
        fill_circle(x, y - 3, 2)
        fill_circle(x - 3, y + 1, 2)
        fill_circle(x + 3, y + 1, 2)
        fill_rect(x - 1, y + 2, 2, 4)
def soli_card(x, y, cd, h=soli_CHT, sel=False):
    if cd is None:
        rbox(x, y, soli_CW, soli_CHT, 4, (60, 110, 80), 1, soli_FELT)
        return
    r, s, up = cd
    edge = GOLD if sel else BLACK
    rrect(x, y, soli_CW, h, 4, edge)
    if not up:
        rrect(x + 1, y + 1, soli_CW - 2, h - 2, 3, soli_BACK)
        rect(x + 3, y + 3, soli_CW - 6, 1, lt(soli_BACK, 0.5))
        if h >= 12:
            rect(x + 4, y + 4, soli_CW - 8, h - 8, lt(soli_BACK, 0.15))
            for i in range(x + 6, x + soli_CW - 6, 6):
                rect(i, y + 6, 2, h - 12, soli_BACK)
        return
    rrect(x + 1, y + 1, soli_CW - 2, h - 2, 3, (255, 245, 200) if sel else soli_CARD)
    t = soli_RANKS[r]
    text(x + 3, y + 15, t, RED if s < 2 else BLACK)
    soli_suit(x + 31 - (5 if len(t) > 1 else 0) + (5 if len(t) > 1 else 0), y + 9, s)
    if h >= soli_CHT:
        soli_suit(x + soli_CW // 2, y + 22, s)
class soli_G:
    pass
def soli_new():
    g = soli_G()
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
def soli_gap(pile):
    n = len(pile)
    up = 12
    while n > 1 and soli_TABY + (n - 1) * up + soli_CHT > 208 and (up > 5):
        up -= 1
    return up
def soli_draw_col(g, c, cur, depth, held):
    x = soli_cx(c)
    rect(x, soli_TABY, soli_CW + 1, 210 - soli_TABY, soli_FELT)
    pile = g.tab[c]
    if not pile:
        soli_card(x, soli_TABY, None)
    up = soli_gap(pile)
    for i in range(len(pile)):
        cd = pile[i]
        sel = cur == 7 + c and i >= len(pile) - depth or (held and held[0] == 7 + c and (i >= len(pile) - held[1]))
        last = i == len(pile) - 1
        soli_card(x, soli_TABY + i * up, cd, soli_CHT if last else max(up + 4, 10), sel)
def soli_draw_top(g, cur, held):
    rect(0, 0, 320, soli_TABY - 2, soli_FELT)
    x = soli_cx(0)
    if g.stock:
        soli_card(x, soli_TOPY, [1, 0, False], soli_CHT, cur == 0)
    else:
        soli_card(x, soli_TOPY, None)
        if cur == 0:
            rbox(x, soli_TOPY, soli_CW, soli_CHT, 4, GOLD, 2, soli_FELT)
    x = soli_cx(1)
    if g.waste:
        soli_card(x, soli_TOPY, g.waste[-1], soli_CHT, cur == 1 or (held and held[0] == 1))
    else:
        soli_card(x, soli_TOPY, None)
    for f in range(4):
        x = soli_cx(3 + f)
        p = g.found[f]
        if p:
            soli_card(x, soli_TOPY, p[-1], soli_CHT, cur == 3 + f)
        else:
            soli_card(x, soli_TOPY, None)
            if cur == 3 + f:
                rbox(x, soli_TOPY, soli_CW, soli_CHT, 4, GOLD, 2, soli_FELT)
            soli_suit(x + 20, soli_TOPY + 15, f)
def soli_fits_found(cd, f, pile):
    if cd[1] != f:
        return False
    return cd[0] == (pile[-1][0] + 1 if pile else 1)
def soli_fits_tab(cd, pile):
    if not pile:
        return cd[0] == 13
    t = pile[-1]
    return t[2] and t[0] == cd[0] + 1 and ((t[1] < 2) != (cd[1] < 2))
def soli_take(g, src, n):
    if src == 1:
        return [g.waste[-1]]
    return g.tab[src - 7][-n:]
def soli_remove(g, src, n):
    if src == 1:
        g.waste.pop()
    else:
        p = g.tab[src - 7]
        del p[-n:]
        if p and (not p[-1][2]):
            p[-1][2] = True
def soli_try_move(g, src, n, dst):
    cards = soli_take(g, src, n)
    if 3 <= dst <= 6:
        if n != 1 or not soli_fits_found(cards[0], dst - 3, g.found[dst - 3]):
            return False
        soli_remove(g, src, n)
        g.found[dst - 3].append(cards[0])
        return True
    if dst >= 7 and dst != src and soli_fits_tab(cards[0], g.tab[dst - 7]):
        soli_remove(g, src, n)
        g.tab[dst - 7].extend(cards)
        return True
    return False
def soli_faceup(g, c):
    n = 0
    for cd in g.tab[c]:
        if cd[2]:
            n += 1
    return n
def soli_game():
    g = soli_new()
    cls(soli_FELT)
    cur = 7
    depth = 1
    held = None
    redraw = list(range(7))
    top = True
    while True:
        if top:
            soli_draw_top(g, cur, held)
        for c in redraw:
            soli_draw_col(g, c, cur, depth if held is None else 0, held)
        redraw = []
        top = False
        if sum((len(f) for f in g.found)) == 52:
            message(['All 52 cards are home.'], 'You win!')
            return
        k = wkey()
        old = cur
        if k == CLR:
            if held:
                held = None
                redraw = list(range(7))
                top = True
                continue
            if message(['ENTER: quit this game', 'CLEAR: keep playing'], 'Quit?') == OK:
                return
            cls(soli_FELT)
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
            if depth < soli_faceup(g, cur - 7) and held is None:
                depth += 1
            else:
                cur = cur - 7 if cur - 7 != 2 else 1
        elif k == DOWN and cur >= 7 and (depth > 1):
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
                elif cur >= 7 and g.tab[cur - 7] and (soli_faceup(g, cur - 7) >= depth):
                    held = (cur, depth)
                    redraw.append(cur - 7)
            else:
                src, n = held
                held = None
                soli_try_move(g, src, n, cur)
                redraw = list(range(7))
                top = True
        elif k == SECOND and held is None:
            src = cur if cur == 1 or cur >= 7 else -1
            if src >= 0 and (src == 1 and g.waste or (src >= 7 and g.tab[src - 7])):
                for f in range(4):
                    if soli_try_move(g, src, 1, 3 + f):
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
soli_RULES = 'Build four piles from Ace to King, one per suit. In the columns, stack cards down in alternating colors.'
soli_KEYS = ['Arrows: move   ENTER: pick/put', 'Up/Down in a column: more cards', 'ENTER on the deck: draw', '2nd: send card to top piles', 'CLEAR: quit']
def soli_main():
    while True:
        c = home('GHSOLI', 'SOLITAIRE', soli_RULES, soli_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        soli_game()
soli_main()
