# GHRPG from GAMEHUB, on its own. Run it.
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
DARK = (40, 40, 40)
RED = (220, 50, 50)
GREEN = (50, 190, 80)
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
icons_GOLD = (230, 180, 40)
icons_BG = {}
def icons_c_(c):
    set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
    icons_c_(c)
    fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))
def icons_circ(x, y, r, c):
    icons_c_(c)
    fill_circle(int(x), int(y), int(r))
def icons_rpg(x, y, c):
    icons_circ(x - 5, y - 8, 6, (240, 200, 160))
    icons_box(x - 11, y - 15, 13, 5, (110, 70, 30))
    icons_box(x - 11, y - 11, 3, 5, (110, 70, 30))
    icons_box(x - 8, y - 9, 2, 2, icons_BLACK)
    icons_box(x - 3, y - 9, 2, 2, icons_BLACK)
    icons_box(x - 11, y - 1, 13, 12, (60, 120, 230))
    icons_box(x - 11, y + 5, 13, 2, (110, 70, 30))
    icons_box(x - 14, y, 3, 8, (240, 200, 160))
    icons_box(x - 10, y + 11, 4, 6, (60, 40, 30))
    icons_box(x - 4, y + 11, 4, 6, (60, 40, 30))
    icons_box(x + 2, y + 1, 4, 3, (240, 200, 160))
    icons_box(x + 2, y - 23, 12, 26, (15, 45, 70))
    icons_box(x + 4, y - 22, 8, 24, (40, 110, 170))
    icons_box(x + 5, y - 21, 6, 22, (100, 200, 245))
    icons_box(x + 7, y - 21, 2, 21, (240, 252, 255))
    icons_box(x + 3, y + 1, 10, 2, icons_GOLD)
    icons_box(x + 7, y + 3, 2, 5, (120, 80, 40))
    for sx, sy in ((x + 16, y - 18), (x + 1, y - 14), (x + 15, y - 6)):
        icons_box(sx, sy, 2, 2, (200, 240, 255))
icons_ICONS = {'GHRPG': icons_rpg}
def icons_bg(mod):
    return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
    f = icons_ICONS.get(mod)
    if f:
        f(x, y, c)
rpg_T = 20
rpg_MAPS = (['TTTTTTTTTTTTTTTT', 'T......TT......T', 'T.HH...........T', 'T.HH....C......T', 'T..............>', 'T....~~~.......>', 'T....~~~...TT..T', 'T..........TT..T', 'T..............T', 'TTTTTTTTTTTTTTTT'], ['TTTTTTTTTTTTTTTT', 'T..T....TT...T.T', 'T..T.C..TT...T.T', '<......T.....T.T', '<..TT..T..T....>', 'T..TT.....T....>', 'T.....T...TTT..T', 'T.TT..T.C......T', 'T.TT..T........T', 'TTTTTTTTTTTTTTTT'], ['################', '#::::#:::::::::#', '#::C:#:###:###:#', '<::::#:#:::#:::#', '<::::::#:B:#:::#', '#::#####:::#:#:#', '#::::::::::::#:#', '#:####:#####:#:#', '#:::::::C::::::#', '################'])
rpg_NAMES = ('Meadow', 'Whisper Woods', 'Hollow Cave')
rpg_FOES = ((), (('Slime', 12, 4, 1, 6, (80, 200, 90)), ('Bat', 10, 5, 0, 7, (120, 90, 160))), (('Bone Rat', 18, 7, 2, 12, (220, 220, 200)), ('Cave Eye', 22, 8, 3, 15, (200, 60, 60))))
rpg_BOSS = ('Hollow King', 70, 12, 4, 0, (110, 80, 180))
def rpg_tile(m, x, y, ch):
    px = x * rpg_T
    py = 20 + y * rpg_T
    if ch in '.>< ':
        rect(px, py, rpg_T, rpg_T, (40, 110, 50))
    elif ch == 'T':
        rect(px, py, rpg_T, rpg_T, (40, 110, 50))
        circ(px + 10, py + 8, 8, (20, 70, 30))
        rect(px + 8, py + 13, 4, 6, (90, 60, 30))
    elif ch == '~':
        rect(px, py, rpg_T, rpg_T, (40, 90, 190))
    elif ch == 'H':
        rect(px, py, rpg_T, rpg_T, (40, 110, 50))
        rect(px + 2, py + 8, 16, 12, (200, 170, 120))
        col((170, 50, 40))
        fill_poly([px, px + 10, px + 20], [py + 9, py, py + 9])
        rect(px + 8, py + 13, 4, 7, (90, 60, 30))
    elif ch == 'C':
        rect(px, py, rpg_T, rpg_T, (40, 110, 50) if m < 2 else (60, 55, 50))
        rect(px + 4, py + 7, 12, 9, (160, 110, 40))
        rect(px + 4, py + 10, 12, 2, GOLD)
    elif ch == 'c':
        rect(px, py, rpg_T, rpg_T, (40, 110, 50) if m < 2 else (60, 55, 50))
        rect(px + 4, py + 10, 12, 6, (100, 70, 30))
    elif ch == '#':
        rect(px, py, rpg_T, rpg_T, (30, 28, 35))
    elif ch == ':':
        rect(px, py, rpg_T, rpg_T, (60, 55, 50))
    elif ch == 'B':
        rect(px, py, rpg_T, rpg_T, (60, 55, 50))
        circ(px + 10, py + 10, 8, (110, 80, 180))
        rect(px + 5, py + 7, 3, 3, RED)
        rect(px + 12, py + 7, 3, 3, RED)
def rpg_hero(x, y):
    px = x * rpg_T
    py = 20 + y * rpg_T
    circ(px + 10, py + 5, 4, (240, 200, 160))
    rect(px + 6, py + 9, 8, 7, (60, 120, 230))
    rect(px + 6, py + 16, 3, 4, (60, 40, 30))
    rect(px + 11, py + 16, 3, 4, (60, 40, 30))
    rect(px + 15, py + 6, 2, 10, (200, 200, 210))
def rpg_draw_map(g):
    m = g.m
    for y in range(10):
        for x in range(16):
            rpg_tile(m, x, y, g.maps[m][y][x])
    rpg_hero(g.x, g.y)
    rpg_hud(g)
def rpg_hud(g):
    rect(0, 0, 320, 20, BLACK)
    text(4, 15, rpg_NAMES[g.m][:13], GOLD)
    text(140, 15, 'HP' + str(g.hp) + '/' + str(g.mhp))
    text(240, 15, 'LV' + str(g.lv) + ' P' + str(g.pot))
class rpg_Game:
    pass
def rpg_bar(x, y, w, v, mx, c):
    rect(x, y, w, 6, DARK)
    if v > 0:
        rect(x, y, max(2, int(w * v / mx)), 6, c)
def rpg_foe_art(f):
    c = f[5]
    n = f[0]
    if n == 'Slime':
        circ(220, 95, 30, c)
        rect(190, 95, 60, 30, c)
    elif n == 'Bat':
        col(c)
        fill_poly([170, 220, 270, 220], [80, 100, 80, 120])
        circ(220, 100, 12, c)
    elif n == 'Bone Rat':
        circ(220, 100, 22, c)
        circ(245, 85, 10, c)
        rect(170, 110, 30, 3, c)
    elif n == 'Cave Eye':
        circ(220, 95, 30, c)
        circ(220, 95, 14, WHITE)
        circ(220, 95, 6, BLACK)
    else:
        rect(195, 70, 50, 60, c)
        circ(220, 60, 18, c)
        col(GOLD)
        fill_poly([200, 205, 212, 220, 228, 235, 240], [45, 30, 42, 28, 42, 30, 45])
        rect(208, 55, 5, 5, RED)
        rect(227, 55, 5, 5, RED)
    if n == 'Slime':
        circ(210, 92, 3, BLACK)
        circ(230, 92, 3, BLACK)
    elif n == 'Bone Rat':
        circ(245, 83, 2, BLACK)
def rpg_battle(g, f):
    name, fhp, fat, fdf, xp = (f[0], f[1], f[2], f[3], f[4])
    mx = fhp
    cls()
    rbox(150, 30, 140, 120, 10, f[5], 2, BLACK)
    rpg_foe_art(f)
    ctext(26, name + ' appears!', GOLD)
    opts = ['Attack', 'Potion', 'Run']
    sel = 0
    log = ''
    while True:
        rect(0, 150, 320, 60, BLACK)
        rect(10, 40, 130, 100, BLACK)
        text(12, 56, 'You', WHITE)
        rpg_bar(12, 62, 120, g.hp, g.mhp, GREEN)
        text(12, 86, name[:12], f[5])
        rpg_bar(12, 92, 120, fhp, mx, RED)
        for i in range(3):
            c = GOLD if i == sel else WHITE
            rbox(10 + i * 102, 154, 96, 24, 8, c)
            text(58 + i * 102 - len(opts[i]) * 5, 172, opts[i], c)
        text(10, 202, log[:31], GREY)
        k = wkey()
        if k == LEFT:
            sel = (sel - 1) % 3
            continue
        if k == RIGHT:
            sel = (sel + 1) % 3
            continue
        if k != OK:
            continue
        if sel == 0:
            d = max(1, g.atk + random.randint(0, 3) - fdf)
            fhp -= d
            log = 'You hit for ' + str(d) + '.'
        elif sel == 1:
            if g.pot == 0:
                log = 'No potions left.'
                continue
            g.pot -= 1
            g.hp = min(g.mhp, g.hp + 25)
            log = 'You feel better.'
        elif f is rpg_BOSS:
            log = "You can't run from him!"
        elif random.random() < 0.6:
            return True
        else:
            log = "Couldn't get away."
        if fhp <= 0:
            g.xp += xp
            msg = ['You won. +' + str(xp) + ' XP']
            while g.xp >= g.lv * 12:
                g.xp -= g.lv * 12
                g.lv += 1
                g.mhp += 8
                g.atk += 2
                g.dfn += 1
                g.hp = g.mhp
                msg.append('Level up! LV ' + str(g.lv))
            message(msg, name + ' defeated')
            return True
        d = max(1, fat + random.randint(0, 3) - g.dfn)
        g.hp -= d
        log = log + ' It hits ' + str(d) + '.'
        if g.hp <= 0:
            message(['You fainted...'], 'Game over')
            return False
def rpg_play():
    g = rpg_Game()
    g.maps = [[list(r) for r in mp] for mp in rpg_MAPS]
    g.m = 0
    g.x, g.y = (4, 4)
    g.hp = g.mhp = 30
    g.atk = 6
    g.dfn = 1
    g.lv = 1
    g.xp = 0
    g.pot = 1
    steps = 0
    cls()
    rpg_draw_map(g)
    message(['The Hollow King took', "the village's light.", 'Bring it back!'], 'TINY QUEST')
    rpg_draw_map(g)
    while True:
        k = wkey()
        if k == CLR:
            if message(['ENTER: quit adventure', 'CLEAR: keep going'], 'Quit?') == OK:
                return
            rpg_draw_map(g)
            continue
        dx, dy = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, -1), DOWN: (0, 1)}.get(k, (0, 0))
        if dx == 0 and dy == 0:
            continue
        nx, ny = (g.x + dx, g.y + dy)
        mp = g.maps[g.m]
        if nx >= 16 or nx < 0:
            g.m += 1 if nx >= 16 else -1
            g.x = 0 if nx >= 16 else 15
            rpg_draw_map(g)
            continue
        ch = mp[ny][nx]
        if ch in 'T~#':
            continue
        if ch == 'H':
            g.hp = g.mhp
            rpg_hud(g)
            message(['You rest by the fire.', 'HP restored.'], 'Cottage')
            rpg_draw_map(g)
            continue
        if ch == 'C':
            mp[ny][nx] = 'c'
            g.pot += 1
            message(['You found a potion!'], 'Chest')
            rpg_draw_map(g)
            continue
        if ch == 'B':
            if rpg_battle(g, rpg_BOSS):
                if g.hp > 0:
                    cls()
                    message(['The light returns to', 'the village. You did it!'], 'THE END')
                return
            return
        ox, oy = (g.x, g.y)
        g.x, g.y = (nx, ny)
        rpg_tile(g.m, ox, oy, mp[oy][ox])
        rpg_hero(g.x, g.y)
        steps += 1
        if rpg_FOES[g.m] and steps > 6 and (random.random() < 0.12):
            steps = 0
            if not rpg_battle(g, random.choice(rpg_FOES[g.m])):
                return
            rpg_draw_map(g)
rpg_RULES = 'Walk the meadow, woods and cave. Rest at the cottage, open chests for potions, and defeat the Hollow King.'
rpg_KEYS = ['Arrows: walk', 'Fights: Left/Right + ENTER', 'CLEAR: quit']
def rpg_main():
    while True:
        c = home('GHRPG', 'TINY QUEST', rpg_RULES, rpg_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        rpg_play()
rpg_main()
