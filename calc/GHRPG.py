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
BASE = {".": GRASS, ">": GRASS, "<": GRASS, " ": GRASS, "T": GRASS, "H": GRASS,
        "~": (40, 90, 190), "#": (30, 28, 35), ":": STONE, "B": STONE}
LEAF = (25, 85, 35)
BARK = (90, 60, 30)
LINE = (45, 40, 38)
WOOD = (120, 75, 35)


# Each map cell is a base colour plus a few shapes, listed as
# (layer, colour, kind, args). The base colours of a row are joined into long
# rectangles, and the shapes are drawn layer by layer, one colour at a time,
# so a whole map takes few drawing calls.
def shapes(m, x, y, ch, out):
    px = x * T
    py = 20 + y * T
    if ch in ".>< ":
        h = (x * 7 + y * 13) % 5
        if h == 2:
            out.append((0, (240, 220, 90), 0, (px + 14, py + 4, 2, 2)))
        elif h == 4:
            out.append((0, (230, 120, 160), 0, (px + 4, py + 15, 2, 2)))
    elif ch == "T":
        out.append((0, BARK, 0, (px + 8, py + 14, 4, 6)))
        out.append((1, LEAF, 1, (px + 10, py + 8, 8)))
    elif ch == "~":
        o = (x * 5 + y * 3) % 8
        out.append((0, (110, 160, 235), 0, (px + o, py + 8, 6, 1)))
    elif ch == "H":
        out.append((0, (200, 170, 120), 0, (px + 2, py + 9, 16, 11)))
        out.append((1, (170, 50, 40), 2, ([px, px + 10, px + 20], [py + 9, py, py + 9])))
        out.append((2, BARK, 0, (px + 8, py + 13, 4, 7)))
        out.append((2, (250, 230, 140), 0, (px + 4, py + 11, 3, 3)))
        out.append((2, (250, 230, 140), 0, (px + 13, py + 11, 3, 3)))
    elif ch == "C" or ch == "c":
        if m == 2:
            out.append((0, LINE, 0, (px, py, T, 1)))
        if ch == "C":
            out.append((0, (60, 40, 20), 0, (px + 3, py + 6, 14, 11)))
            out.append((1, (160, 110, 40), 0, (px + 4, py + 7, 12, 9)))
            out.append((2, GOLD, 0, (px + 4, py + 10, 12, 2)))
        else:
            out.append((0, (100, 70, 30), 0, (px + 4, py + 10, 12, 6)))
    elif ch == "#":
        for yy in (6, 13):
            out.append((0, (50, 47, 58), 0, (px, py + yy, T, 1)))
    elif ch == ":":
        out.append((0, LINE, 0, (px, py, T, 1)))
    elif ch == "B":
        out.append((0, LINE, 0, (px, py, T, 1)))
        out.append((1, (110, 80, 180), 1, (px + 10, py + 11, 8)))
        out.append((2, GOLD, 2, ([px + 3, px + 6, px + 10, px + 14, px + 17], [py + 4, py - 1, py + 3, py - 1, py + 4])))
        out.append((3, RED, 0, (px + 5, py + 8, 3, 3)))
        out.append((3, RED, 0, (px + 12, py + 8, 3, 3)))


def base(m, ch):
    if ch in "Cc":
        return GRASS if m < 2 else STONE
    return BASE.get(ch, GRASS)


def hero(x, y, out):
    px = x * T
    py = 20 + y * T
    out.append((5, (240, 200, 160), 1, (px + 10, py + 5, 4)))
    out.append((6, WOOD, 0, (px + 6, py + 1, 8, 3)))
    out.append((6, BLACK, 0, (px + 8, py + 5, 1, 1)))
    out.append((6, BLACK, 0, (px + 11, py + 5, 1, 1)))
    out.append((6, (60, 120, 230), 0, (px + 6, py + 9, 8, 7)))
    out.append((6, (60, 40, 30), 0, (px + 6, py + 16, 3, 4)))
    out.append((6, (60, 40, 30), 0, (px + 11, py + 16, 3, 4)))
    out.append((6, (210, 215, 225), 0, (px + 15, py + 4, 2, 8)))
    out.append((6, GOLD, 0, (px + 14, py + 12, 4, 2)))


def paint(ops):
    # rectangles of one colour that touch side by side become one
    ops.sort(key=lambda o: (o[0], o[1], o[2], o[3][1] if o[2] == 0 else 0, o[3][0]))
    last = None
    for layer, c, kind, a in ops:
        if kind == 0:
            if last and last[0] == (layer, c) and last[2] == a[1] and last[4] == a[3] and last[1] + last[3] == a[0]:
                last[3] += a[2]
                continue
            if last:
                rect(last[1], last[2], last[3], last[4], last[0][1])
            last = [(layer, c), a[0], a[1], a[2], a[3]]
            continue
        if last:
            rect(last[1], last[2], last[3], last[4], last[0][1])
            last = None
        if kind == 1:
            circ(a[0], a[1], a[2], c)
        else:
            col(c)
            fill_poly(a[0], a[1])
    if last:
        rect(last[1], last[2], last[3], last[4], last[0][1])


def cells(g, todo, with_hero):
    # draw the map cells in todo (x, y): their base colours joined along each
    # row, then their shapes, and the hero if with_hero
    mp = g.maps[g.m]
    ops = []
    rows = {}
    for x, y in todo:
        rows.setdefault(y, []).append(x)
    for y in rows:
        xs = sorted(rows[y])
        i = 0
        while i < len(xs):
            c = base(g.m, mp[y][xs[i]])
            j = i + 1
            while j < len(xs) and xs[j] == xs[j - 1] + 1 and base(g.m, mp[y][xs[j]]) == c:
                j += 1
            ops.append((-1, c, 0, (xs[i] * T, 20 + y * T, (j - i) * T, T)))
            i = j
    for x, y in todo:
        shapes(g.m, x, y, mp[y][x], ops)
    if with_hero:
        hero(g.x, g.y, ops)
    paint(ops)


def draw_map(g, after_msg=False):
    # after a message box, only the rows it covered are drawn again
    r0, r1 = 0, 10
    if after_msg:
        r0 = max(0, (MSG[0] - 20) // T)
        r1 = min(10, (MSG[0] + MSG[1] - 20) // T + 1)
    else:
        HUD[0] = None
    cells(g, [(x, y) for y in range(r0, r1) for x in range(16)], r0 <= g.y < r1)
    hud(g)


HUD = [None]


def hud(g):
    t = (NAMES[g.m][:13], "HP" + str(g.hp) + "/" + str(g.mhp), "LV" + str(g.lv) + " P" + str(g.pot))
    if t == HUD[0]:
        return
    if HUD[0] is None:
        rect(0, 0, 320, 20, BLACK)
        old = ("", "", "")
    else:
        old = HUD[0]
    for i, x, c in ((0, 4, GOLD), (1, 140, WHITE), (2, 240, WHITE)):
        if t[i] != old[i]:
            text(x, 15, old[i], BLACK)
            text(x, 15, t[i], c)
    HUD[0] = t


class Game:
    pass


def bar(x, y, w, v, mx, c):
    # filled part and empty part side by side, so nothing is painted twice
    f = max(0, min(w, int(w * v / mx))) if v > 0 else 0
    if v > 0:
        f = max(2, f)
    rect(x, y, f, 6, c)
    rect(x + f, y, w - f, 6, DARK)


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
    text(12, 56, "You", WHITE)
    text(12, 86, name[:12], f[5])
    for i in range(3):
        c = GOLD if i == sel else WHITE
        rbox(10 + i * 102, 154, 96, 24, 8, c)
        text(58 + i * 102 - len(opts[i]) * 5, 172, opts[i], c)
    was = None
    while True:
        # only what changed: the bars, the gold option, the last line
        now = (g.hp, fhp, sel, log)
        if was is None or was[0] != now[0]:
            bar(12, 62, 120, g.hp, g.mhp, GREEN)
        if was is None or was[1] != now[1]:
            bar(12, 92, 120, fhp, mx, RED)
        if was is not None and was[2] != sel:
            for i in (was[2], sel):
                c = GOLD if i == sel else WHITE
                edge(10 + i * 102, 154, 96, 24, 8, c)
                text(58 + i * 102 - len(opts[i]) * 5, 172, opts[i], c)
        if was is None or was[3] != log:
            if was is not None:
                text(10, 202, was[3][:31], BLACK)
            text(10, 202, log[:31], GREY)
        was = now
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
    draw_map(g, True)
    while True:
        k = wkey()
        if k == CLR:
            if message(["ENTER: quit adventure", "CLEAR: keep going"], "Quit?") == OK:
                return
            draw_map(g, True)
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
            draw_map(g, True)
            continue
        if ch == "C":
            mp[ny][nx] = "c"
            g.pot += 1
            message(["You found a potion!"], "Chest")
            draw_map(g, True)
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
        # the cell the hero left and the hero, drawn together colour by colour
        cells(g, [(ox, oy)], True)
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
