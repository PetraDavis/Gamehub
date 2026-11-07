# GAMEHUB shared helpers. Every game imports this.
from ti_draw import *
from ti_system import *
import time

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


def ring(x, y, r, c, t=2, inner=BLACK):
    col(c)
    fill_circle(x, y, r)
    col(inner)
    fill_circle(x, y, r - t)


def rrect(x, y, w, h, r, c):
    # filled rectangle with round corners
    col(c)
    fill_rect(x + r, y, w - 2 * r, h)
    fill_rect(x, y + r, w, h - 2 * r)
    fill_circle(x + r, y + r, r)
    fill_circle(x + w - r - 1, y + r, r)
    fill_circle(x + r, y + h - r - 1, r)
    fill_circle(x + w - r - 1, y + h - r - 1, r)


def rbox(x, y, w, h, r, c, t=2, inner=BLACK):
    # rounded outline box
    rrect(x, y, w, h, r, c)
    rrect(x + t, y + t, w - 2 * t, h - 2 * t, max(r - t, 2), inner)


def pause(s):
    time.sleep(s)


def message(lines, title=None):
    # Show a box with text; wait for ENTER or CLEAR. Returns the key.
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


def choose(title, opts, sel=0):
    # Simple list menu. Returns the chosen index, or -1 for CLEAR.
    cls()
    ctext(24, title, GOLD)
    n = len(opts)
    while True:
        for i in range(n):
            y = 40 + i * 30
            c = GOLD if i == sel else WHITE
            rbox(60, y, 200, 24, 8, c)
            ctext(y + 18, opts[i], c)
        k = wkey()
        if k == UP:
            sel = (sel - 1) % n
        elif k == DOWN:
            sel = (sel + 1) % n
        elif k == OK:
            return sel
        elif k == CLR:
            return -1


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
                if opts[sel] == "Back":
                    return -1
                return sel
