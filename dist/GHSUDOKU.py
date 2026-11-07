# GHSUDOKU from GAMEHUB, on its own. Run it.
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
DEL = 23
NUMS = {102: 0, 92: 1, 93: 2, 94: 3, 82: 4, 83: 5, 84: 6, 72: 7, 73: 8, 74: 9}
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
icons_WHITE = (255, 255, 255)
icons_INK = (20, 20, 20)
icons_BG = {'GHSUDOKU': icons_WHITE}
def icons_c_(c):
    set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
    icons_c_(c)
    fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))
def icons_line(x1, y1, x2, y2, c, t=1):
    icons_c_(c)
    for o in range(t):
        draw_line(int(x1) + o, int(y1), int(x2) + o, int(y2))
def icons_hline(x1, x2, y, c, t=1):
    icons_c_(c)
    for o in range(t):
        draw_line(int(x1), int(y) + o, int(x2), int(y) + o)
icons_FONT7 = {'1': '00100011000010000100001000010001110', '3': '11110000010000101110000010000111110', '5': '11111100001111000001000011000101110', '7': '11111000010001000100010000100001000', '9': '01110100011000101111000010001001100'}
def icons_digit7(x, y, ch, c):
    icons_c_(c)
    bits = icons_FONT7[ch]
    for r in range(7):
        row = bits[r * 5:r * 5 + 5]
        k = 0
        while k < 5:
            if row[k] == '1':
                e = k
                while e + 1 < 5 and row[e + 1] == '1':
                    e += 1
                draw_line(x + k, y + r, x + e, y + r)
                k = e + 1
            else:
                k += 1
def icons_sudoku(x, y, c):
    s = 11
    x0 = x - 16
    y0 = y - 16
    icons_box(x0 + s + 1, y0 + 1, s - 1, s - 1, (250, 225, 140))
    nums = ('53 ', ' 7 ', '1 9')
    for r in range(3):
        for k in range(3):
            ch = nums[r][k]
            if ch != ' ':
                icons_digit7(x0 + k * s + 3, y0 + r * s + 2, ch, icons_INK if (r, k) != (1, 1) else (40, 90, 200))
    for i in (1, 2):
        icons_line(x0 + i * s, y0, x0 + i * s, y0 + 3 * s, icons_INK)
        icons_hline(x0, x0 + 3 * s, y0 + i * s, icons_INK)
    icons_c_(icons_INK)
    for o in (0, 1):
        draw_rect(x0 - o, y0 - o, 3 * s + 2 * o, 3 * s + 2 * o)
icons_ICONS = {'GHSUDOKU': icons_sudoku}
def icons_bg(mod):
    return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
    f = icons_ICONS.get(mod)
    if f:
        f(x, y, c)
sudoku_S = 20
sudoku_X0 = 20
sudoku_Y0 = 15
sudoku_INK = (20, 20, 20)
sudoku_PEN = (40, 90, 200)
def sudoku_make(holes):
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
def sudoku_valid(b):
    for i in range(9):
        row = set(b[i * 9:i * 9 + 9])
        colm = set(b[i::9])
        bx = i % 3 * 3 + i // 3 * 27
        box = set((b[bx + o] for o in (0, 1, 2, 9, 10, 11, 18, 19, 20)))
        for s in (row, colm, box):
            if s != set(range(1, 10)):
                return False
    return True
def sudoku_clash(b, i):
    v = b[i]
    if not v:
        return False
    r = i // 9
    c = i % 9
    for j in range(81):
        if j != i and b[j] == v:
            if j // 9 == r or j % 9 == c or (j // 27 == i // 27 and j % 9 // 3 == c // 3):
                return True
    return False
def sudoku_cell(b, fixed, i, cur):
    x = sudoku_X0 + i % 9 * sudoku_S
    y = sudoku_Y0 + i // 9 * sudoku_S
    bg = (250, 225, 140) if i == cur else WHITE
    rect(x + 1, y + 1, sudoku_S - 2, sudoku_S - 2, bg)
    v = b[i]
    if v:
        c = sudoku_INK if fixed[i] else RED if sudoku_clash(b, i) else sudoku_PEN
        text(x + 5, y + 17, str(v), c)
def sudoku_grid():
    for i in range(10):
        c = sudoku_INK if i % 3 == 0 else (150, 150, 150)
        t = 2 if i % 3 == 0 else 1
        if t == 2:
            rect(sudoku_X0 + i * sudoku_S - 1, sudoku_Y0 - 1, 2, sudoku_S * 9 + 2, c)
            rect(sudoku_X0 - 1, sudoku_Y0 + i * sudoku_S - 1, sudoku_S * 9 + 2, 2, c)
        else:
            col(c)
            draw_line(sudoku_X0 + i * sudoku_S, sudoku_Y0, sudoku_X0 + i * sudoku_S, sudoku_Y0 + sudoku_S * 9)
            draw_line(sudoku_X0, sudoku_Y0 + i * sudoku_S, sudoku_X0 + sudoku_S * 9, sudoku_Y0 + i * sudoku_S)
def sudoku_game(holes):
    b = sudoku_make(holes)
    fixed = [v != 0 for v in b]
    cls(WHITE)
    sudoku_grid()
    text(214, 30, 'SUDOKU', sudoku_INK)
    text(214, 70, '0-9 type', GREY)
    text(214, 90, 'ENTER +1', GREY)
    text(214, 110, 'DEL erase', GREY)
    text(214, 130, 'CLEAR quit', GREY)
    cur = 0
    while fixed[cur]:
        cur += 1
    for i in range(81):
        sudoku_cell(b, fixed, i, cur)
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
                v = b[cur] % 9 + 1
            elif k == DEL:
                v = 0
            if v >= 0:
                b[cur] = v
                for i in range(81):
                    if not fixed[i] and b[i]:
                        sudoku_cell(b, fixed, i, cur)
                if 0 not in b and sudoku_valid(b):
                    message(['Every row, column and', 'box is complete.'], 'Solved!')
                    return
        sudoku_cell(b, fixed, old, cur)
        sudoku_cell(b, fixed, cur, cur)
sudoku_RULES = 'Fill the grid so every row, column and 3x3 box has the numbers 1 to 9 once. Red numbers clash.'
sudoku_KEYS = ['Arrows: move', '0-9: type a number', 'ENTER: count up  DEL: erase', 'CLEAR: quit']
def sudoku_main():
    while True:
        c = home('GHSUDOKU', 'SUDOKU', sudoku_RULES, sudoku_KEYS, ('Easy', 'Medium', 'Hard', 'Back'))
        if c < 0:
            return
        sudoku_game((36, 46, 54)[c])
sudoku_main()
