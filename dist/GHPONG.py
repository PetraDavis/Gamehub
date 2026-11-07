# GHPONG from GAMEHUB, on its own. Run it.
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
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (230, 180, 40)
GREY = (110, 110, 110)
H = 210
def key():
    return get_key(0)
class Steer:

    def __init__(self, keys, stop_on_back=False):
        self.keys = keys
        self.back = stop_on_back
        self.d = 0

    def feed(self, k):
        if k in self.keys:
            if self.back and self.d and (k != self.d) and (self.keys.index(k) // 2 == self.keys.index(self.d) // 2):
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
def pause(s):
    time.sleep(s)
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
icons_WHITE = (255, 255, 255)
icons_BG = {'GHPONG': (30, 85, 165)}
def icons_c_(c):
    set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
    icons_c_(c)
    fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))
def icons_hline(x1, x2, y, c, t=1):
    icons_c_(c)
    for o in range(t):
        draw_line(int(x1), int(y) + o, int(x2), int(y) + o)
def icons_circ(x, y, r, c):
    icons_c_(c)
    fill_circle(int(x), int(y), int(r))
def icons_pong(x, y, c):
    icons_c_(icons_WHITE)
    draw_rect(x - 21, y - 15, 43, 31)
    icons_hline(x - 21, x + 21, y, (200, 210, 230))
    for i in range(6):
        icons_box(x, y - 15 + i * 6, 2, 3, icons_WHITE)
    icons_box(x - 17, y - 11, 4, 14, icons_WHITE)
    icons_box(x + 14, y - 3, 4, 14, icons_WHITE)
    icons_circ(x - 6, y - 5, 2, (250, 150, 40))
icons_ICONS = {'GHPONG': icons_pong}
def icons_bg(mod):
    return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
    f = icons_ICONS.get(mod)
    if f:
        f(x, y, c)
pong_PH = 36
pong_TOP = 24
pong_TABLE = (30, 85, 165)
pong_BALL = (250, 150, 40)
def pong_net():
    for y in range(pong_TOP, 210, 14):
        rect(159, y, 2, 7, WHITE)
def pong_scores(a, b):
    rect(0, 0, 320, pong_TOP - 2, pong_TABLE)
    text(110, 18, str(a))
    text(200, 18, str(b), GOLD)
    rect(0, pong_TOP - 2, 320, 2, WHITE)
def pong_game():
    cls(pong_TABLE)
    me = cpu = 0
    py = cy = 100
    pong_scores(me, cpu)
    pong_net()
    serve = 1
    while me < 7 and cpu < 7:
        bx, by = (160.0, 110.0)
        vx = 4.0 * serve
        vy = random.choice((-2.5, -1.5, 1.5, 2.5))
        pause(0.5)
        st = Steer((UP, DOWN))
        while True:
            k = key()
            if k == CLR:
                return
            opy, ocy = (py, cy)
            d = st.feed(k)
            if d == UP:
                py = max(pong_TOP, py - 6)
                if py == pong_TOP:
                    st.stop()
            elif d == DOWN:
                py = min(210 - pong_PH, py + 6)
                if py == 210 - pong_PH:
                    st.stop()
            target = by - pong_PH / 2
            if vx > 0 and bx > 120:
                cy += max(-4, min(4, target - cy))
            cy = int(max(pong_TOP, min(210 - pong_PH, cy)))
            obx, oby = (bx, by)
            bx += vx
            by += vy
            if by < pong_TOP + 3 or by > 206:
                vy = -vy
                by = max(pong_TOP + 3, min(206, by))
            if bx < 18 and vx < 0 and (py - 4 < by < py + pong_PH + 4):
                vx = min(9, -vx * 1.06)
                vy += (by - (py + pong_PH / 2)) / 6
                bx = 18
            if bx > 302 and vx > 0 and (cy - 4 < by < cy + pong_PH + 4):
                vx = max(-9, -vx * 1.06)
                vy += (by - (cy + pong_PH / 2)) / 6
                bx = 302
            rect(int(obx) - 3, int(oby) - 3, 7, 7, pong_TABLE)
            if opy != py:
                rect(8, opy, 6, pong_PH, pong_TABLE)
            if ocy != cy:
                rect(306, ocy, 6, pong_PH, pong_TABLE)
            if 150 < obx < 170:
                pong_net()
            rect(8, py, 6, pong_PH, WHITE)
            rect(306, cy, 6, pong_PH, GOLD)
            rect(int(bx) - 3, int(by) - 3, 7, 7, pong_BALL)
            if bx < 0:
                cpu += 1
                serve = 1
                break
            if bx > 320:
                me += 1
                serve = -1
                break
        rect(int(bx) - 3, int(by) - 3, 7, 7, pong_TABLE)
        pong_scores(me, cpu)
    message(['You ' + str(me) + ' - ' + str(cpu) + ' Calculator'], 'You win!' if me > cpu else 'Calculator wins')
pong_RULES = "Bounce the ball past the calculator's paddle. First to 7 points wins."
pong_KEYS = ['Up/Down: paddle glides that way', 'ENTER: stop the paddle', 'CLEAR: quit']
def pong_main():
    while True:
        c = home('GHPONG', 'PONG', pong_RULES, pong_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        pong_game()
pong_main()
