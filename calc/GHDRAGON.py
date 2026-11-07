# Dragon Tamer: explore three lands, find dragon eggs and hatch them, name
# your dragons, ride them over water, lava and mountains, and fight monsters.
# The Shadow Wyrm waits on an island in the Frost Peaks.
from GHLIB import *
import random

T = 20
MAPS = (
    ["TTTTTTTTTTTTT~~~",
     'T.....""".....~~',
     'T.H...""""...~~~',
     'T.....""".T...~~',
     "T..........E.~~~",
     "T....TT.......~~",
     'T.""".TT......~~',
     'T.""".........~~',
     "TTTTTTTTTTTTTT~~"],
    ["~^^^^^^^^^^^^^^^",
     '~...""""..LLL..^',
     '~..^"""..LLELL.^',
     "~.....^...LLL...",
     "~...............",
     '~...^^...."""...',
     '~..LL....."""..^',
     "~.....^^.......^",
     "~^^^^^^^^^^^^^^^"],
    ["^^^^^^^^^^^^^^^^",
     '...""".....^E^^^',
     "...........^^^^^",
     "......~~~~......",
     "....~~~~B~~~....",
     ".....~~~~~......",
     '.."""...........',
     '..""".....^^....',
     "^^^^^^^^^^^^^^^^"],
)
LANDS = ("Green Valley", "Fire Mountain", "Frost Peaks")
GROUND = ((50, 130, 60), (85, 65, 55), (215, 225, 240))
TALL = ((35, 100, 45), (120, 90, 60), (170, 190, 220))
WATER = (40, 90, 190)
LAVA = (230, 90, 20)
ROCK = (110, 105, 115)
LEAF = (25, 85, 35)
BARK = (90, 60, 30)

# elements: 0 fire, 1 water, 2 plant, 3 star. Fire burns plant, water puts
# out fire, plant drinks water, and star beats them all.
ECOL = ((220, 70, 40), (60, 130, 230), (70, 170, 70), (250, 240, 180))
ENAME = ("fire", "water", "plant", "star")
RARE = ("Common", "Uncommon", "Rare", "Epic", "Legendary")
RCOL = (WHITE, (120, 220, 120), (90, 160, 255), (200, 110, 240), GOLD)
# dragon types: name, element, rarity, colour. Each rarer level has fewer.
DT = (("Ember", 0, 0, (220, 70, 40)), ("Cinder", 0, 0, (235, 140, 40)),
      ("Puddle", 1, 0, (60, 130, 230)), ("Brook", 1, 0, (40, 170, 170)),
      ("Sprig", 2, 0, (70, 170, 70)), ("Mossy", 2, 0, (130, 150, 60)),
      ("Pebble", 2, 0, (150, 140, 120)),
      ("Magma", 0, 1, (170, 40, 30)), ("Frost", 1, 1, (160, 210, 245)),
      ("Thorn", 2, 1, (30, 110, 60)), ("Storm", 1, 1, (120, 100, 200)),
      ("Smoky", 0, 1, (90, 90, 100)),
      ("Sunscale", 0, 2, (240, 190, 40)), ("Coral", 1, 2, (240, 120, 150)),
      ("Jade", 2, 2, (60, 200, 150)), ("Blossom", 2, 2, (250, 160, 210)),
      ("Phoenix", 0, 3, (255, 90, 60)), ("Leviathan", 1, 3, (30, 60, 160)),
      ("Oakheart", 2, 3, (110, 80, 40)),
      ("Starwing", 3, 4, (250, 240, 180)))
NAMES = ("Blaze", "Splash", "Fern", "Spark", "Misty", "Clover", "Ziggy", "Nova",
         "Pebble", "Rocket", "Biscuit", "Luna", "Comet", "Pip", "Maple", "Echo",
         "Sunny", "Bolt", "Willow", "Ash", "Ripple", "Twig", "Ember", "Taro")
PAINT = ((220, 70, 40), (60, 130, 230), (70, 170, 70), (240, 190, 40), (200, 110, 240), (240, 120, 150), (40, 40, 50), (240, 240, 245))
# shop: name, price, gear bit (0 = paint)
SHOP = (("Paint it", 20, 0), ("Saddle", 15, 1), ("Scarf", 25, 2), ("Crown", 60, 4))
# monster: name, hp, attack, xp, colour, element
FOES = ((("Goblin", 14, 4, 6, (110, 160, 60), 3), ("Bog Toad", 16, 4, 7, (60, 120, 160), 1)),
        (("Lava Imp", 26, 7, 12, (240, 120, 30), 0), ("Rock Troll", 32, 7, 14, (120, 110, 90), 2)),
        (("Ice Wraith", 34, 9, 16, (150, 200, 240), 1), ("Snow Yeti", 42, 9, 18, (235, 235, 245), 3)))
BOSS = ("Shadow Wyrm", 110, 12, 0, (90, 50, 140), 3)


def beats(a, b):
    return (a == 3 and b != 3) or (a < 3 and b == (a + 2) % 3)


def egg_type(m):
    # most eggs are common; the further you travel the luckier you get
    r = random.randint(0, 99) + m * 6
    rar = 4 if r >= 99 else 3 if r >= 92 else 2 if r >= 78 else 1 if r >= 52 else 0
    return random.choice([i for i in range(len(DT)) if DT[i][2] == rar])


def base(m, ch):
    if ch == "~":
        return WATER
    if ch == "L":
        return LAVA
    if ch == '"':
        return TALL[m]
    return GROUND[m]


def shapes(m, x, y, ch, out):
    px = x * T
    py = 20 + y * T
    if ch == "T":
        out.append((0, BARK, 0, (px + 8, py + 14, 4, 6)))
        out.append((1, LEAF, 1, (px + 10, py + 8, 8)))
    elif ch == "~":
        out.append((0, (110, 160, 235), 0, (px + (x * 5 + y * 3) % 8, py + 8, 6, 1)))
    elif ch == "L":
        out.append((0, (250, 200, 60), 0, (px + (x * 7 + y * 5) % 12, py + 6, 5, 3)))
    elif ch == '"':
        c = GROUND[m]
        for o in (3, 9, 15):
            out.append((0, c, 0, (px + o, py + 6 + o % 4, 2, 8)))
    elif ch == "^":
        out.append((0, ROCK, 2, ([px, px + 10, px + 20], [py + 20, py + 1, py + 20])))
        out.append((1, WHITE, 2, ([px + 6, px + 10, px + 14], [py + 8, py + 1, py + 8])))
    elif ch == "H":
        out.append((0, BARK, 1, (px + 10, py + 12, 9)))
        out.append((1, (60, 40, 20), 1, (px + 10, py + 12, 6)))
        out.append((2, (245, 235, 210), 1, (px + 7, py + 12, 3)))
        out.append((2, (245, 235, 210), 1, (px + 13, py + 11, 3)))
        out.append((3, (200, 160, 90), 0, (px + 1, py + 15, 18, 2)))
    elif ch == "E":
        c = RCOL[DT[EGGS.get((m, x, y), 0)][2]]
        out.append((0, BARK, 0, (px + 3, py + 15, 14, 4)))
        out.append((1, (245, 235, 210), 1, (px + 10, py + 10, 6)))
        out.append((2, c, 0, (px + 7, py + 8, 3, 3)))
        out.append((2, c, 0, (px + 11, py + 12, 3, 3)))
    elif ch == "B":
        out.append((0, (40, 30, 60), 1, (px + 10, py + 10, 9)))
        out.append((1, BOSS[4], 1, (px + 10, py + 10, 6)))
        out.append((2, (255, 60, 60), 0, (px + 6, py + 8, 3, 3)))
        out.append((2, (255, 60, 60), 0, (px + 11, py + 8, 3, 3)))


EGGS = {}  # (land, x, y): dragon type of the egg lying there


def el(d):
    return DT[d[1]][1]


def hero(g, out):
    px = g.x * T
    py = 20 + g.y * T
    d = g.ride
    if d is not None:
        c = d[6]
        out.append((5, lt(c, 0.45), 2, ([px, px + 9, px + 4], [py + 2, py + 11, py + 14])))
        out.append((6, c, 0, (px + 2, py + 11, 13, 7)))
        out.append((6, c, 0, (px + 13, py + 6, 7, 7)))
        out.append((6, c, 0, (px, py + 15, 3, 3)))
        out.append((6, c, 0, (px + 4, py + 18, 3, 2)))
        out.append((6, c, 0, (px + 11, py + 18, 3, 2)))
        out.append((7, BLACK, 0, (px + 17, py + 8, 2, 2)))
        if d[7] & 1:
            out.append((7, BARK, 0, (px + 5, py + 11, 6, 3)))
        if d[7] & 2:
            out.append((7, RED, 0, (px + 12, py + 11, 3, 5)))
        if d[7] & 4:
            out.append((8, GOLD, 0, (px + 14, py + 3, 5, 3)))
        out.append((8, (240, 200, 160), 1, (px + 8, py + 5, 3)))
        out.append((8, (60, 120, 230), 0, (px + 6, py + 8, 5, 4)))
        return
    out.append((5, (240, 200, 160), 1, (px + 10, py + 5, 4)))
    out.append((6, BARK, 0, (px + 6, py + 1, 8, 3)))
    out.append((6, (60, 120, 230), 0, (px + 6, py + 9, 8, 7)))
    out.append((6, (60, 40, 30), 0, (px + 6, py + 16, 3, 4)))
    out.append((6, (60, 40, 30), 0, (px + 11, py + 16, 3, 4)))


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
        hero(g, ops)
    paint(ops)


def draw_map(g, after_msg=False):
    # after a message box, only the rows it covered are drawn again
    r0, r1 = 0, 9
    if after_msg:
        r0 = max(0, (MSG[0] - 20) // T)
        r1 = min(9, (MSG[0] + MSG[1] - 20) // T + 1)
    else:
        cls()
        HUD[0] = None
    cells(g, [(x, y) for y in range(r0, r1) for x in range(16)], r0 <= g.y < r1)
    hud(g)


HUD = [None]


def hud(g):
    d = g.ride
    if d is not None:
        who = d[0] + " " + str(d[3]) + "/" + str(d[4])
    else:
        who = "You " + str(g.hp) + "/" + str(g.mhp)
    t = (LANDS[g.m], who, ("Egg " + str(g.warm)) if g.egg is not None else str(g.coins) + "c")
    if t == HUD[0]:
        return
    old = HUD[0] or ("", "", "")
    if HUD[0] is None:
        rect(0, 0, 320, 20, BLACK)
    for i, x, c in ((0, 4, GOLD), (1, 140, WHITE), (2, 262, YELLOW)):
        if t[i] != old[i]:
            text(x, 15, old[i], BLACK)
            text(x, 15, t[i], c)
    HUD[0] = t


class Game:
    pass


def bar(x, y, w, v, mx, c):
    f = max(0, min(w, int(w * v / mx))) if v > 0 else 0
    if v > 0:
        f = max(2, f)
    rect(x, y, f, 6, c)
    rect(x + f, y, w - f, 6, DARK)


def baby(x, y, c, big=1):
    # a dragon facing left: wings, body, head, eye
    col(lt(c, 0.4))
    fill_poly([x - 4 * big, x + 10 * big, x + 4 * big], [y - 6 * big, y - 22 * big, y])
    rect(x - 10 * big, y - 4 * big, 26 * big, 14 * big, c)
    rect(x - 22 * big, y - 12 * big, 14 * big, 11 * big, c)
    rect(x + 14 * big, y + 2 * big, 12 * big, 4 * big, c)
    rect(x - 18 * big, y - 9 * big, 3 * big, 3 * big, BLACK)


def foe_art(f):
    c = f[4]
    n = f[0]
    if n == "Shadow Wyrm":
        baby(225, 105, c, 3)
        rect(166, 79, 9, 9, RED)
    elif n in ("Goblin", "Rock Troll", "Snow Yeti"):
        s = 1 if n == "Goblin" else 2
        rect(220 - 12 * s, 100 - 10 * s, 24 * s, 30 * s, c)
        circ(220, 92 - 14 * s, 10 * s, c)
        rect(214 - 2 * s, 88 - 16 * s, 4, 4, BLACK)
        rect(222 + 2 * s, 88 - 16 * s, 4, 4, BLACK)
    elif n == "Bog Toad":
        circ(220, 105, 26, c)
        circ(206, 82, 8, c)
        circ(234, 82, 8, c)
        circ(206, 82, 3, BLACK)
        circ(234, 82, 3, BLACK)
    else:
        col(c)
        fill_poly([195, 245, 230, 220, 210], [80, 80, 130, 115, 130])
        circ(220, 78, 16, c)
        rect(212, 74, 4, 4, BLACK)
        rect(224, 74, 4, 4, BLACK)


def battle(g, f):
    # returns True when the monster is beaten or you got away, False when
    # you fainted
    name, fhp, fat, xp, fc, fe = f
    mx = fhp
    cls()
    rbox(150, 30, 140, 120, 10, fc, 2, BLACK)
    foe_art(f)
    ctext(24, name + " appears!", GOLD)
    log = ""
    sel = 0
    was = None
    while True:
        d = g.ride
        opts = ("Claw", "Breath", "Run") if d is not None else ("Sword", "Run")
        n = len(opts)
        w = 300 // n
        sel = min(sel, n - 1)
        now = (d[0] if d else "You", d[3] if d else g.hp, fhp, sel, log, n)
        if was is None or was[0] != now[0]:
            rect(0, 40, 148, 60, BLACK)
            rect(0, 150, 320, 34, BLACK)
            text(12, 56, now[0], d[6] if d else WHITE)
            text(12, 86, name[:12], fc)
            for i in range(n):
                cc = GOLD if i == sel else WHITE
                rbox(10 + i * w, 154, w - 6, 24, 8, cc)
                text(10 + i * w + (w - 6) // 2 - len(opts[i]) * 5, 172, opts[i], cc)
            was = None
        if was is None or was[1] != now[1]:
            bar(12, 62, 120, now[1], d[4] if d else g.mhp, GREEN)
        if was is None or was[2] != fhp:
            bar(12, 92, 120, fhp, mx, RED)
        if was is not None and was[3] != sel:
            for i in (was[3], sel):
                cc = GOLD if i == sel else WHITE
                edge(10 + i * w, 154, w - 6, 24, 8, cc)
                text(10 + i * w + (w - 6) // 2 - len(opts[i]) * 5, 172, opts[i], cc)
        if was is None or was[4] != log:
            rect(0, 186, 320, 24, BLACK)
            text(6, 202, log[:31], GREY)
        was = now
        k = wkey()
        if k in (LEFT, RIGHT):
            sel = (sel + (1 if k == RIGHT else -1)) % n
            continue
        if k != OK:
            continue
        o = opts[sel]
        if o == "Run":
            if f is BOSS:
                log = "The Wyrm blocks your way!"
                continue
            if random.random() < 0.6:
                return True
            log = "Couldn't get away."
        elif o == "Sword":
            dm = random.randint(3, 5)
            fhp -= dm
            log = "Sword hits for " + str(dm) + "."
        else:
            at = 5 + 2 * d[2] + 2 * DT[d[1]][2]
            if o == "Claw":
                dm = at + random.randint(0, 2)
                log = "Claw hits for " + str(dm) + "."
            else:
                dm = at + random.randint(2, 5)
                if beats(el(d), fe):
                    dm *= 2
                    log = "Super breath! " + str(dm) + "."
                elif beats(fe, el(d)):
                    dm //= 2
                    log = "Weak breath... " + str(dm) + "."
                else:
                    log = "Breath hits for " + str(dm) + "."
            fhp -= dm
        if fhp <= 0:
            msg = []
            for dd in g.pen:
                if dd[3] > 0 and (dd is d or dd is g.pick):
                    dd[5] += xp
                    while dd[5] >= dd[2] * 10:
                        dd[5] -= dd[2] * 10
                        dd[2] += 1
                        dd[4] += 6
                        dd[3] = dd[4]
                        msg.append(dd[0] + " is now level " + str(dd[2]) + "!")
            message(msg[:3] or ["You won!"], name + " beaten")
            if f is not BOSS:
                quest_step(g, 0, name)
                quest_step(g, 2, g.m)
            return True
        dm = max(1, fat + random.randint(0, 3) - (d[2] if d else 0))
        log += " It hits " + str(dm) + "."
        if d is not None:
            d[3] = max(0, d[3] - dm)
            if d[3] == 0:
                g.ride = None
                message([d[0] + " is too tired to fly.", "You fight on foot!"], "Oh no")
                cls()
                rbox(150, 30, 140, 120, 10, fc, 2, BLACK)
                foe_art(f)
                ctext(24, name, GOLD)
                was = None
        else:
            g.hp -= dm
            if g.hp <= 0:
                message(["You fainted...", "Your dragons carry you", "home to the nest."], "Ouch")
                go_home(g)
                return False


def go_home(g):
    g.m, g.x, g.y = 0, 3, 2
    rest(g)


def rest(g):
    g.hp = g.mhp
    g.ride = None
    for d in g.pen:
        d[3] = d[4]


# ---------- quests ----------
FOE_NAMES = [f[0] for l in FOES for f in l]


def new_quest(g):
    k = random.randint(0, 2)
    if k == 0:
        n = random.randint(2, 4)
        land = random.randint(0, g.seen)
        nm = random.choice(FOES[land])[0]
        return [0, nm, n, 0, 8 * n + 6 * land, "Beat " + str(n) + " " + nm + "s"]
    if k == 1:
        return [1, None, 1, 0, 20, "Hatch an egg"]
    land = random.randint(0, g.seen)
    n = random.randint(3, 5)
    return [2, land, n, 0, 7 * n + 6 * land, str(n) + " wins: " + LANDS[land]]


def quest_step(g, kind, what):
    q = g.quest
    if q is None or q[0] != kind or (q[1] is not None and q[1] != what):
        return
    q[3] += 1
    if q[3] >= q[2]:
        g.coins += q[4]
        g.quest = None
        message(["You finished:", q[5], "+" + str(q[4]) + " coins!"], "Quest done!")


def board(g):
    if g.quest is not None:
        q = g.quest
        c = choose(q[5] + " " + str(q[3]) + "/" + str(q[2]), ["Keep going", "Give up quest"])
        if c == 1:
            g.quest = None
        return
    qs = [new_quest(g) for i in range(3)]
    c = choose("Quests: pick one", [q[5][:15] + " " + str(q[4]) + "c" for q in qs] + ["Not now"])
    if 0 <= c < 3:
        g.quest = qs[c]


# ---------- the nest ----------
def stats(d):
    t = DT[d[1]]
    message([t[0] + " (" + RARE[t[2]] + ")", "Element: " + ENAME[t[1]], "Level " + str(d[2]) + "  HP " + str(d[3]) + "/" + str(d[4]),
             "Attack " + str(5 + 2 * d[2] + 2 * t[2])], d[0])


def pen(g):
    while g.pen:
        opts = [("> " if d is g.pick else "") + d[0] + " L" + str(d[2]) + " " + DT[d[1]][0][:6] for d in g.pen]
        c = choose("Dragon pen " + str(len(g.pen)) + "/7", opts + ["Back"])
        if c < 0 or c >= len(g.pen):
            return
        d = g.pen[c]
        a = choose(d[0] + " the " + DT[d[1]][0], ["Pick as partner", "See stats", "Let it go free", "Back"])
        if a == 0:
            g.pick = d
        elif a == 1:
            cls()
            baby(160, 60, d[6], 1)
            stats(d)
        elif a == 2 and len(g.pen) > 1:
            g.pen.remove(d)
            if g.pick is d:
                g.pick = g.pen[0]


def shop(g):
    while True:
        d = g.pick
        opts = []
        for nm, pr, bit in SHOP:
            opts.append(nm + (" (have)" if bit and d[7] & bit else " " + str(pr) + "c"))
        c = choose(d[0] + ": " + str(g.coins) + " coins", opts + ["Back"])
        if c < 0 or c >= len(SHOP):
            return
        nm, pr, bit = SHOP[c]
        if bit and d[7] & bit:
            continue
        if g.coins < pr:
            message(["You need " + str(pr) + " coins.", "Do quests to earn more."], "Not enough")
            continue
        if bit == 0:
            p = choose("Pick a colour", ["Red", "Blue", "Green", "Gold", "Purple", "Pink", "Black", "White"])
            if p < 0:
                continue
            d[6] = PAINT[p]
        else:
            d[7] |= bit
        g.coins -= pr
        cls()
        baby(160, 120, d[6], 2)
        message([d[0] + " looks great!"], nm)


def nest(g):
    rest(g)
    while True:
        opts = ["Dragon pen", "Quest board", "Shop", "Leave the nest"]
        c = choose("The Nest (all rested)", opts)
        if c == 0:
            pen(g)
        elif c == 1:
            board(g)
        elif c == 2:
            if g.pick is None:
                message(["Hatch a dragon first!"])
            else:
                shop(g)
        else:
            return


def hatch(g):
    e = g.egg
    g.egg = None
    t = DT[e]
    cls()
    ctext(30, "The egg is cracking!", GOLD)
    circ(160, 110, 30, (245, 235, 210))
    pause(0.8)
    rect(120, 70, 80, 80, BLACK)
    baby(160, 115, t[3], 2)
    ctext(190, RARE[t[2]] + " " + t[0] + " dragon!", RCOL[t[2]])
    pause(1.0)
    names = sample(NAMES, 4)
    i = choose("Name your " + t[0] + ":", names)
    nm = names[max(0, i)]
    d = [nm, e, 1, 20 + 6 * t[2], 20 + 6 * t[2], 0, t[3], 0]
    g.pen.append(d)
    msg = [nm + " joins your pen!"]
    if g.pick is None:
        g.pick = d
        msg += ["Press ENTER to ride.", "Dragons fly over water,", "lava and mountains."]
    draw_map(g)
    message(msg, RARE[t[2]] + " " + t[0])
    quest_step(g, 1, None)
    draw_map(g, True)


def menu(g):
    # ENTER on the map: ride or get off your partner, or fly home
    d = g.pick
    if g.ride is not None:
        first = "Get off " + d[0]
    else:
        first = "Ride " + d[0] + ("" if d[3] > 0 else " (tired)")
    c = choose(d[0] + " the " + DT[d[1]][0], [first, "Fly home to the nest", "Keep exploring"])
    if c == 0:
        if g.ride is not None:
            if g.maps[g.m][g.y][g.x] in "~L^":
                draw_map(g)
                message(["You can't get off here!"])
                draw_map(g, True)
                return
            g.ride = None
        elif d[3] == 0:
            draw_map(g)
            message([d[0] + " is too tired.", "Rest at the nest first."])
            draw_map(g, True)
            return
        else:
            g.ride = d
    elif c == 1:
        go_home(g)
    draw_map(g)


def spawn(g):
    # a new egg turns up somewhere in this land, now and then
    g.spawn = random.randint(25, 40)
    mp = g.maps[g.m]
    if sum(1 for k in EGGS if k[0] == g.m) >= 2:
        return
    for n in range(20):
        x = random.randint(1, 14)
        y = random.randint(1, 7)
        if mp[y][x] in '."' and abs(x - g.x) + abs(y - g.y) > 3:
            mp[y][x] = "E"
            EGGS[(g.m, x, y)] = egg_type(g.m)
            cells(g, [(x, y)], False)
            return


def play():
    g = Game()
    g.maps = [[list(r) for r in mp] for mp in MAPS]
    EGGS.clear()
    for m in range(3):
        for y in range(9):
            for x in range(16):
                if MAPS[m][y][x] == "E":
                    EGGS[(m, x, y)] = random.randint(0, 6) if m == 0 else egg_type(m)
    g.m, g.x, g.y = 0, 3, 2
    g.hp = g.mhp = 20
    g.pen = []
    g.pick = None
    g.ride = None
    g.egg = None
    g.warm = 0
    g.coins = 0
    g.quest = None
    g.seen = 0
    g.spawn = 30
    steps = 0
    draw_map(g)
    message(["The Shadow Wyrm scared", "the dragons away. Find", "eggs and raise a team!"], "DRAGON TAMER")
    draw_map(g, True)
    while True:
        k = wkey()
        if k == CLR:
            if message(["ENTER: quit adventure", "CLEAR: keep going"], "Quit?") == OK:
                return
            draw_map(g, True)
            continue
        if k in (OK, SECOND):
            if g.pick is not None:
                menu(g)
            continue
        dx, dy = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, -1), DOWN: (0, 1)}.get(k, (0, 0))
        if dx == 0 and dy == 0:
            continue
        nx, ny = g.x + dx, g.y + dy
        if nx < 0 or nx > 15:
            m = g.m + (1 if nx > 15 else -1)
            if 0 <= m < 3:
                ch = g.maps[m][ny][15 - g.x]
                if ch != "T" and (ch not in "~L^" or g.ride is not None):
                    g.m = m
                    g.seen = max(g.seen, m)
                    g.x = 15 - g.x
                    draw_map(g)
            continue
        if ny < 0 or ny > 8:
            continue
        mp = g.maps[g.m]
        ch = mp[ny][nx]
        if ch == "T" or (ch in "~L^" and g.ride is None):
            continue
        if ch == "B":
            if battle(g, BOSS):
                cls()
                baby(160, 120, g.ride[6] if g.ride else GOLD, 2)
                message(["The Shadow Wyrm flies far", "away. Dragons return to", "every land. You did it!"], "THE END")
                return
            draw_map(g)
            continue
        if ch == "E" and (g.egg is not None or len(g.pen) >= 7):
            draw_map(g)
            message(["You're already keeping", "an egg warm."] if g.egg is not None else ["Your pen is full (7).", "Let a dragon go first."], "Egg")
            draw_map(g, True)
            continue
        ox, oy = g.x, g.y
        g.x, g.y = nx, ny
        if ch == "E":
            mp[ny][nx] = "."
            cells(g, [(ox, oy), (nx, ny)], True)
            g.egg = EGGS.pop((g.m, nx, ny), 0)
            g.warm = 12
            hud(g)
            message(["You found an egg with", RARE[DT[g.egg][2]] + " spots! Keep", "walking and it will hatch."], "An egg!")
            draw_map(g, True)
            continue
        if ch == "H":
            nest(g)
            draw_map(g)
            continue
        cells(g, [(ox, oy), (nx, ny)], True)
        if g.egg is not None:
            g.warm -= 1
            if g.warm <= 0:
                hatch(g)
                continue
        g.spawn -= 1
        if g.spawn <= 0:
            spawn(g)
        hud(g)
        steps += 1
        if ch == '"' and steps > 3 and random.random() < 0.2:
            steps = 0
            battle(g, random.choice(FOES[g.m]))
            draw_map(g)


RULES = "Find eggs (new ones keep turning up), walk to hatch them and name your dragons. 20 kinds, Common to Legendary. Ride over water, lava and mountains. The nest has your pen, quests for coins and a shop. Fire beats plant, water beats fire, plant beats water."
KEYS = ["Arrows: walk or fly", "ENTER: ride or get off", "Fights: Left/Right + ENTER", "CLEAR: quit"]


def main():
    while True:
        c = home("GHDRAGON", "DRAGON TAMER", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        play()
