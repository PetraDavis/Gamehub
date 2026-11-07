# GAMEHUB shared helpers. Every game imports this.
from ti_draw import *
from ti_system import *
import time
import random

# Key codes for the TI-84 Evo (check them with Settings > Key test).
UP = 25
DOWN = 34
LEFT = 24
RIGHT = 26
OK = 105
CLR = 45
DEL = 23
SECOND = 21
NUMS = {102: 0, 92: 1, 93: 2, 94: 3, 82: 4, 83: 5, 84: 6, 72: 7, 73: 8, 74: 9}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (230, 180, 40)
GREY = (110, 110, 110)
DARK = (40, 40, 40)
RED = (220, 50, 50)
GREEN = (50, 190, 80)
BLUE = (60, 120, 230)
YELLOW = (240, 220, 60)

W = 320
H = 210


def key():
    return get_key(0)


class Steer:
    # The calculator reports an arrow once when it is pressed, not again while
    # it is held. So an arrow starts a glide that keeps going. The same arrow
    # keeps it going, the opposite arrow reverses it (or stops it when
    # stop_on_back is set), and any other key stops it.
    def __init__(self, keys, stop_on_back=False):
        self.keys = keys
        self.back = stop_on_back
        self.d = 0

    def feed(self, k):
        if k in self.keys:
            if self.back and self.d and k != self.d and self.keys.index(k) // 2 == self.keys.index(self.d) // 2:
                self.d = 0
            else:
                self.d = k
        elif k:
            self.d = 0
        return self.d

    def stop(self):
        self.d = 0


# The calculator's random module has no shuffle or sample, so here they are.
def shuffle(a):
    for i in range(len(a) - 1, 0, -1):
        j = random.randint(0, i)
        a[i], a[j] = a[j], a[i]


def sample(seq, k):
    a = list(seq)
    shuffle(a)
    return a[:k]


def wkey():
    return wait_key()


_C = [None]


def col(c):
    # changing the colour is slow on the calculator, so skip it when it's the same
    if c != _C[0]:
        _C[0] = c
        set_color(c[0], c[1], c[2])


def fr(x, y, w, h):
    # The calculator's fill_rect(x, y, w, h) skips the box's 1-pixel border,
    # so it covers x+1..x+w-1. This fills exactly x..x+w-1, y..y+h-1, and
    # works for 1-pixel lines too.
    fill_rect(x - 1, y - 1, w + 1, h + 1)


def rect(x, y, w, h, c):
    if w < 1 or h < 1:
        return
    col(c)
    fill_rect(x - 1, y - 1, w + 1, h + 1)


# counts screen clears and message boxes, so a game that only draws what
# changed knows when everything has to be drawn again
COVER = [0]


def cls(c=BLACK):
    COVER[0] += 1
    col(c)
    fill_rect(-1, -1, 321, 211)


# The calculator draws text in the rows y-17..y-3. Our layouts put the
# capital letters' bottom on y, so text is moved down by 6.
TY = 6


def text(x, y, s, c=WHITE):
    col(c)
    draw_text(x, y + TY, s)


def ctext(y, s, c=WHITE, cx=160):
    col(c)
    draw_text(cx - len(s) * 5, y + TY, s)


def circ(x, y, r, c):
    col(c)
    fill_circle(x, y, r)


def lt(c, k=0.35):
    # a lighter shade of c
    return (int(c[0] + (255 - c[0]) * k), int(c[1] + (255 - c[1]) * k), int(c[2] + (255 - c[2]) * k))


def dk(c, k=0.65):
    # a darker shade of c
    return (int(c[0] * k), int(c[1] * k), int(c[2] * k))


def block(x, y, w, h, c, e=2):
    # a raised block: light top and left edges, dark bottom and right edges
    rect(x, y, w, h, c)
    rect(x, y, w, e, lt(c))
    rect(x, y, e, h, lt(c))
    rect(x, y + h - e, w, e, dk(c))
    rect(x + w - e, y + e, e, h - e, dk(c))


def ball(x, y, r, c):
    # a round ball with a small shine
    circ(x, y, r, c)
    s = max(1, r // 3)
    circ(x - s, y - s, s, lt(c, 0.6))


def ring(x, y, r, c, t=2, inner=BLACK):
    col(c)
    fill_circle(x, y, r)
    col(inner)
    fill_circle(x, y, r - t)


def rrect(x, y, w, h, r, c):
    # filled rectangle with round corners
    if w < 2 * r + 1 or h < 2 * r + 1:
        r = max(0, min(w, h) // 2 - 1)
    col(c)
    if w - 2 * r >= 1:
        fr(x + r, y, w - 2 * r, h)
    if h - 2 * r >= 1:
        fr(x, y + r, w, h - 2 * r)
    if r < 1:
        return
    fill_circle(x + r, y + r, r)
    fill_circle(x + w - r - 1, y + r, r)
    fill_circle(x + r, y + h - r - 1, r)
    fill_circle(x + w - r - 1, y + h - r - 1, r)


def rbox(x, y, w, h, r, c, t=2, inner=BLACK):
    # rounded outline box
    rrect(x, y, w, h, r, c)
    rrect(x + t, y + t, w - 2 * t, h - 2 * t, max(r - t, 2), inner)


def edge(x, y, w, h, r, c, t=2, inner=BLACK):
    # recolour the outline of an rbox without touching what's inside it, so
    # moving a highlight doesn't make the box flash
    col(c)
    fr(x + r, y, w - 2 * r, t)
    fr(x + r, y + h - t, w - 2 * r, t)
    fr(x, y + r, t, h - 2 * r)
    fr(x + w - t, y + r, t, h - 2 * r)
    for cx, cy, sx, sy in ((x + r, y + r, 1, 1), (x + w - r - 1, y + r, -1, 1),
                           (x + r, y + h - r - 1, 1, -1), (x + w - r - 1, y + h - r - 1, -1, -1)):
        col(c)
        fill_circle(cx, cy, r)
        col(inner)
        fill_circle(cx, cy, max(r - t, 2))
        # the coloured disc also spilled inwards; paint those parts back
        ax = cx + 1 if sx > 0 else cx - r
        ay = y + t if sy > 0 else cy - r
        fr(ax, ay, r, (cy + r + 1 - ay) if sy > 0 else (y + h - t - ay))
        ax = x + t if sx > 0 else cx - r
        ay = cy + 1 if sy > 0 else cy - r
        fr(ax, ay, (cx + r + 1 - ax) if sx > 0 else (x + w - t - ax), r)


def vacate(ox, oy, nx, ny, w, h, c):
    # paint colour c where a w x h box was (ox, oy) but no longer is (nx, ny),
    # so a moving thing is never erased and drawn again in the same place
    if abs(nx - ox) >= w or abs(ny - oy) >= h:
        rect(ox, oy, w, h, c)
        return
    if ny > oy:
        rect(ox, oy, w, ny - oy, c)
    elif ny < oy:
        rect(ox, ny + h, w, oy - ny, c)
    y0 = max(oy, ny)
    y1 = min(oy, ny) + h
    if nx > ox:
        rect(ox, y0, nx - ox, y1 - y0, c)
    elif nx < ox:
        rect(nx + w, y0, ox - nx, y1 - y0, c)


def halo(x, y, r, c, t=2):
    # a round outline of thickness t made of 1-pixel circles, so it can be
    # recoloured without touching the inside
    col(c)
    for i in range(t):
        draw_circle(x, y, r - i)


def pause(s):
    time.sleep(s)


MSG = [0, 0]  # where the last message box was: y, height


def message(lines, title=None):
    # Show a box with text; wait for ENTER or CLEAR. Returns the key.
    n = len(lines) + (1 if title else 0)
    h = n * 18 + 30
    y = (H - h) // 2
    rbox(20, y, 280, h, 8, WHITE)
    MSG[0], MSG[1] = y, h
    COVER[0] += 1
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


def choose(title, opts, sel=0):
    # Simple list menu. Returns the chosen index, or -1 for CLEAR.
    cls()
    ctext(24, title, GOLD)
    n = len(opts)
    for i in range(n):
        y = 40 + i * 30
        c = GOLD if i == sel else WHITE
        rbox(60, y, 200, 24, 8, c)
        ctext(y + 18, opts[i], c)
    while True:
        k = wkey()
        old = sel
        if k == UP:
            sel = (sel - 1) % n
        elif k == DOWN:
            sel = (sel + 1) % n
        elif k == OK:
            return sel
        elif k == CLR:
            return -1
        for i in (old, sel):
            y = 40 + i * 30
            c = GOLD if i == sel else WHITE
            edge(60, y, 200, 24, 8, c)
            ctext(y + 18, opts[i], c)


def _wrap(s, n=30):
    out = []
    line = ""
    for w in s.split(" "):
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


def how_to(title, rules, buttons):
    cls()
    ctext(20, "HOW TO PLAY", GOLD)
    ctext(38, title, GREY)
    y = 60
    for ln in _wrap(rules):
        text(8, y, ln)
        y += 16
    y += 6
    text(8, y, "BUTTONS", GOLD)
    y += 17
    for b in buttons:
        text(8, y, b)
        y += 16
    text(8, 206, "ENTER: back", GREY)
    while wkey() not in (OK, CLR, UP, DOWN):
        pass


def home(mod, title, rules, buttons, opts=("Play", "Back"), sel=0):
    # Game start screen. Returns the chosen option, or -1 for Back/CLEAR.
    n = len(opts)
    while True:
        cls()
        ring(160, 58, 36, GOLD, 3)
        try:
            import GHICONS
            circ(160, 58, 33, GHICONS.bg(mod))
            GHICONS.draw(mod, 160, 58, WHITE)
        except Exception:
            pass
        ctext(122, title, GOLD)
        ctext(146, "Up/Down: how to play", GREY)
        bw = (300 - (n - 1) * 8) // n
        first = True
        while True:
            for i in range(n):
                x = 10 + i * (bw + 8)
                c = GOLD if i == sel else WHITE
                if first:
                    rbox(x, 166, bw, 28, 10, c)
                else:
                    edge(x, 166, bw, 28, 10, c)
                text(x + bw // 2 - len(opts[i]) * 5, 186, opts[i], c)
            first = False
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
                if opts[sel] == "Back":
                    return -1
                return sel
