# Tiny Quest: a short adventure. Walk with the arrows, fight with ENTER.
# Rest at the cottage, open chests, then find the Hollow King in the cave.
from GHLIB import *
import random

T = 20
MAPS = (
    ["TTTTTTTTTTTTTTTT",
     "T......TT......T",
     "T.HH...........T",
     "T.HH....C......T",
     "T..............>",
     "T....~~~.......>",
     "T....~~~...TT..T",
     "T..........TT..T",
     "T..............T",
     "TTTTTTTTTTTTTTTT"],
    ["TTTTTTTTTTTTTTTT",
     "T..T....TT...T.T",
     "T..T.C..TT...T.T",
     "<......T.....T.T",
     "<..TT..T..T....>",
     "T..TT.....T....>",
     "T.....T...TTT..T",
     "T.TT..T.C......T",
     "T.TT..T........T",
     "TTTTTTTTTTTTTTTT"],
    ["################",
     "#::::#:::::::::#",
     "#::C:#:###:###:#",
     "<::::#:#:::#:::#",
     "<::::::#:B:#:::#",
     "#::#####:::#:#:#",
     "#::::::::::::#:#",
     "#:####:#####:#:#",
     "#:::::::C::::::#",
     "################"],
)
NAMES = ("Meadow", "Whisper Woods", "Hollow Cave")
FOES = (
    (),
    (("Slime", 12, 4, 1, 6, (80, 200, 90)), ("Bat", 10, 5, 0, 7, (120, 90, 160))),
    (("Bone Rat", 18, 7, 2, 12, (220, 220, 200)), ("Cave Eye", 22, 8, 3, 15, (200, 60, 60))),
)
BOSS = ("Hollow King", 70, 12, 4, 0, (110, 80, 180))


GRASS = (40, 110, 50)
STONE = (60, 55, 50)


def grass(px, py, x, y):
    rect(px, py, T, T, GRASS)
    h = (x * 7 + y * 13) % 5
    rect(px + 3 + h * 2, py + 5 + h, 1, 3, (70, 150, 70))
    rect(px + 5 + h * 2, py + 6 + h, 1, 2, (70, 150, 70))
    rect(px + 13 - h, py + 14 - h, 1, 3, (30, 90, 40))
    if h == 2:
        rect(px + 14, py + 4, 2, 2, (240, 220, 90))
    elif h == 4:
        rect(px + 4, py + 15, 2, 2, (230, 120, 160))


def floor(px, py, x, y):
    rect(px, py, T, T, STONE)
    o = 0 if y % 2 else 10
    rect(px, py, T, 1, (45, 40, 38))
    rect(px + o, py, 1, T, (45, 40, 38))
    rect(px + 2, py + 2, 6, 1, (75, 70, 64))


def tile(m, x, y, ch):
    px = x * T
    py = 20 + y * T
    if ch in ".>< ":
        grass(px, py, x, y)
    elif ch == "T":
        grass(px, py, x, y)
        rect(px + 8, py + 12, 4, 7, (90, 60, 30))
        rect(px + 10, py + 12, 2, 7, (65, 42, 22))
        circ(px + 10, py + 8, 8, (20, 70, 30))
        circ(px + 9, py + 7, 6, (35, 100, 45))
        rect(px + 6, py + 4, 3, 2, (70, 150, 70))
    elif ch == "~":
        rect(px, py, T, T, (40, 90, 190))
        o = (x * 5 + y * 3) % 8
        rect(px + o, py + 6, 6, 1, (110, 160, 235))
        rect(px + (o + 9) % 14, py + 14, 5, 1, (110, 160, 235))
    elif ch == "H":
        grass(px, py, x, y)
        rect(px + 2, py + 8, 16, 12, (200, 170, 120))
        rect(px + 2, py + 18, 16, 2, (160, 130, 90))
        col((170, 50, 40))
        fill_poly([px, px + 10, px + 20], [py + 9, py, py + 9])
        col((120, 35, 30))
        draw_line(px + 10, py, px + 20, py + 9)
        rect(px + 8, py + 13, 4, 7, (90, 60, 30))
        rect(px + 4, py + 11, 3, 3, (250, 230, 140))
        rect(px + 13, py + 11, 3, 3, (250, 230, 140))
    elif ch == "C":
        if m < 2:
            grass(px, py, x, y)
        else:
            floor(px, py, x, y)
        rect(px + 3, py + 6, 14, 11, (60, 40, 20))
        rect(px + 4, py + 7, 12, 9, (160, 110, 40))
        rect(px + 4, py + 7, 12, 2, (190, 140, 60))
        rect(px + 4, py + 10, 12, 2, GOLD)
        rect(px + 9, py + 11, 2, 3, GOLD)
    elif ch == "c":
        if m < 2:
            grass(px, py, x, y)
        else:
            floor(px, py, x, y)
        rect(px + 4, py + 10, 12, 6, (100, 70, 30))
        rect(px + 4, py + 10, 12, 1, (130, 95, 45))
    elif ch == "#":
        rect(px, py, T, T, (30, 28, 35))
        o = 0 if y % 2 else 5
        for yy in (0, 7, 14):
            rect(px, py + yy, T, 1, (50, 47, 58))
        for xx in (o, o + 10):
            rect(px + xx, py, 1, 6, (50, 47, 58))
            rect(px + (xx + 5) % T, py + 7, 1, 6, (50, 47, 58))
    elif ch == ":":
        floor(px, py, x, y)
    elif ch == "B":
        floor(px, py, x, y)
        circ(px + 10, py + 11, 8, (80, 55, 140))
        circ(px + 10, py + 10, 8, (110, 80, 180))
        col(GOLD)
        fill_poly([px + 3, px + 6, px + 10, px + 14, px + 17], [py + 4, py - 1, py + 3, py - 1, py + 4])
        rect(px + 5, py + 8, 3, 3, RED)
        rect(px + 12, py + 8, 3, 3, RED)
        rect(px + 6, py + 14, 8, 1, (40, 25, 70))


def hero(x, y):
    px = x * T
    py = 20 + y * T
    rect(px + 5, py + 18, 10, 2, (25, 60, 30))
    circ(px + 10, py + 5, 4, (240, 200, 160))
    rect(px + 6, py + 1, 8, 3, (120, 70, 30))
    rect(px + 8, py + 5, 1, 1, BLACK)
    rect(px + 11, py + 5, 1, 1, BLACK)
    rect(px + 6, py + 9, 8, 7, (60, 120, 230))
    rect(px + 6, py + 13, 8, 1, (120, 80, 40))
    rect(px + 6, py + 16, 3, 4, (60, 40, 30))
    rect(px + 11, py + 16, 3, 4, (60, 40, 30))
    rect(px + 15, py + 4, 2, 11, (210, 215, 225))
    rect(px + 14, py + 12, 4, 2, GOLD)


def draw_map(g):
    m = g.m
    for y in range(10):
        for x in range(16):
            tile(m, x, y, g.maps[m][y][x])
    hero(g.x, g.y)
    hud(g)


def hud(g):
    rect(0, 0, 320, 20, BLACK)
    text(4, 15, NAMES[g.m][:13], GOLD)
    text(140, 15, "HP" + str(g.hp) + "/" + str(g.mhp))
    text(240, 15, "LV" + str(g.lv) + " P" + str(g.pot))


class Game:
    pass


def bar(x, y, w, v, mx, c):
    rect(x, y, w, 6, DARK)
    if v > 0:
        rect(x, y, max(2, int(w * v / mx)), 6, c)


def foe_art(f):
    c = f[5]
    n = f[0]
    if n == "Slime":
        circ(220, 95, 30, c)
        rect(190, 95, 60, 30, c)
    elif n == "Bat":
        col(c)
        fill_poly([170, 220, 270, 220], [80, 100, 80, 120])
        circ(220, 100, 12, c)
    elif n == "Bone Rat":
        circ(220, 100, 22, c)
        circ(245, 85, 10, c)
        rect(170, 110, 30, 3, c)
    elif n == "Cave Eye":
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
    if n == "Slime":
        circ(210, 92, 3, BLACK)
        circ(230, 92, 3, BLACK)
    elif n == "Bone Rat":
        circ(245, 83, 2, BLACK)


def battle(g, f):
    name, fhp, fat, fdf, xp = f[0], f[1], f[2], f[3], f[4]
    mx = fhp
    cls()
    rbox(150, 30, 140, 120, 10, f[5], 2, BLACK)
    foe_art(f)
    ctext(26, name + " appears!", GOLD)
    opts = ["Attack", "Potion", "Run"]
    sel = 0
    log = ""
    while True:
        rect(0, 150, 320, 60, BLACK)
        rect(10, 40, 130, 100, BLACK)
        text(12, 56, "You", WHITE)
        bar(12, 62, 120, g.hp, g.mhp, GREEN)
        text(12, 86, name[:12], f[5])
        bar(12, 92, 120, fhp, mx, RED)
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
            log = "You hit for " + str(d) + "."
        elif sel == 1:
            if g.pot == 0:
                log = "No potions left."
                continue
            g.pot -= 1
            g.hp = min(g.mhp, g.hp + 25)
            log = "You feel better."
        else:
            if f is BOSS:
                log = "You can't run from him!"
            elif random.random() < 0.6:
                return True
            else:
                log = "Couldn't get away."
        if fhp <= 0:
            g.xp += xp
            msg = ["You won. +" + str(xp) + " XP"]
            while g.xp >= g.lv * 12:
                g.xp -= g.lv * 12
                g.lv += 1
                g.mhp += 8
                g.atk += 2
                g.dfn += 1
                g.hp = g.mhp
                msg.append("Level up! LV " + str(g.lv))
            message(msg, name + " defeated")
            return True
        d = max(1, fat + random.randint(0, 3) - g.dfn)
        g.hp -= d
        log = log + " It hits " + str(d) + "."
        if g.hp <= 0:
            message(["You fainted..."], "Game over")
            return False


def play():
    g = Game()
    g.maps = [[list(r) for r in mp] for mp in MAPS]
    g.m = 0
    g.x, g.y = 4, 4
    g.hp = g.mhp = 30
    g.atk = 6
    g.dfn = 1
    g.lv = 1
    g.xp = 0
    g.pot = 1
    steps = 0
    cls()
    draw_map(g)
    message(["The Hollow King took", "the village's light.", "Bring it back!"], "TINY QUEST")
    draw_map(g)
    while True:
        k = wkey()
        if k == CLR:
            if message(["ENTER: quit adventure", "CLEAR: keep going"], "Quit?") == OK:
                return
            draw_map(g)
            continue
        dx, dy = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, -1), DOWN: (0, 1)}.get(k, (0, 0))
        if dx == 0 and dy == 0:
            continue
        nx, ny = g.x + dx, g.y + dy
        mp = g.maps[g.m]
        if nx >= 16 or nx < 0:
            g.m += 1 if nx >= 16 else -1
            g.x = 0 if nx >= 16 else 15
            draw_map(g)
            continue
        ch = mp[ny][nx]
        if ch in "T~#":
            continue
        if ch == "H":
            g.hp = g.mhp
            hud(g)
            message(["You rest by the fire.", "HP restored."], "Cottage")
            draw_map(g)
            continue
        if ch == "C":
            mp[ny][nx] = "c"
            g.pot += 1
            message(["You found a potion!"], "Chest")
            draw_map(g)
            continue
        if ch == "B":
            if battle(g, BOSS):
                if g.hp > 0:
                    cls()
                    message(["The light returns to", "the village. You did it!"], "THE END")
                return
            return
        ox, oy = g.x, g.y
        g.x, g.y = nx, ny
        tile(g.m, ox, oy, mp[oy][ox])
        hero(g.x, g.y)
        steps += 1
        if FOES[g.m] and steps > 6 and random.random() < 0.12:
            steps = 0
            if not battle(g, random.choice(FOES[g.m])):
                return
            draw_map(g)


RULES = 'Walk the meadow, woods and cave. Rest at the cottage, open chests for potions, and defeat the Hollow King.'
KEYS = ['Arrows: walk', 'Fights: Left/Right + ENTER', 'CLEAR: quit']


def main():
    while True:
        c = home("GHRPG", 'TINY QUEST', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        play()
