# Star Patrol: aliens drift down toward the planet. Your ship fires on its
# own; Left/Right glide it under them. Don't let an alien reach the bottom.
from GHLIB import *
import random

try:
    from time import monotonic as now
except Exception:
    now = None

BG = (8, 10, 32)
SHIP = (90, 200, 255)
ALIEN = (120, 230, 90)
SHOT = (255, 230, 90)
TOP = 24
SY = 190         # the ship's top edge
SW, SH = 20, 12
AW, AH = 16, 10
MAXA = 3         # aliens on screen at once
FIRE = 0.35      # seconds between shots
SHOT_V = 260.0   # pixels per second
SHIP_V = 160.0


# Every drawing call is slow on the calculator and so is every colour change,
# so each thing is one filled box with a few background-coloured cuts, and
# each frame draws all boxes of one colour, then the next colour, and all
# the background last. A box moves by painting back only the strip it left
# (GHLIB.vacate), so nothing is ever wiped and drawn again.
def ship_cuts(x):
    return ((x, SY, 7, 5), (x + 13, SY, 7, 5))


def alien_cuts(x, y):
    return ((x, y, 4, 3), (x + 12, y, 4, 3), (x + 3, y + 4, 10, 2), (x + 5, y + 8, 6, 2))


def paint(groups):
    # groups: [(colour, [(x, y, w, h), ...]), ...] drawn in that order
    for c, rs in groups:
        if rs:
            col(c)
            for x, y, w, h in rs:
                if w > 0 and h > 0:
                    fr(x, y, w, h)


def strip(ox, oy, nx, ny, w, h, out):
    # the part of the old box (ox, oy) that the new box (nx, ny) doesn't cover
    if abs(nx - ox) >= w or abs(ny - oy) >= h:
        out.append((ox, oy, w, h))
        return
    if ny > oy:
        out.append((ox, oy, w, ny - oy))
    elif ny < oy:
        out.append((ox, ny + h, w, oy - ny))
    y0 = max(oy, ny)
    y1 = min(oy, ny) + h
    if nx > ox:
        out.append((ox, y0, nx - ox, y1 - y0))
    elif nx < ox:
        out.append((nx + w, y0, ox - nx, y1 - y0))


HUD = [None, None]


def hud(score, lives):
    if HUD[0] is None:
        text(6, 17, "Score")
        text(230, 17, "Lives", GOLD)
    if score != HUD[0]:
        if HUD[0] is not None:
            text(66, 17, str(HUD[0]), BG)
        text(66, 17, str(score))
    if lives != HUD[1]:
        if HUD[1] is not None:
            text(290, 17, str(HUD[1]), BG)
        text(290, 17, str(lives), GOLD)
    HUD[0], HUD[1] = score, lives


def new_alien(aliens):
    # a free spot at the top, not on top of another alien
    for i in range(8):
        x = random.randint(4, 316 - AW)
        if all(abs(x - a[0]) > AW + 4 or a[1] > TOP + 30 for a in aliens):
            return [float(x), float(TOP + 2), int(x), TOP + 2]
    return None


def game():
    cls(BG)
    rect(0, 22, 320, 2, (60, 70, 120))
    # a few stars on the far edges, where nothing flies
    for x, y in ((2, 40), (314, 70), (2, 120), (314, 160), (2, 180)):
        rect(x, y, 2, 2, (200, 200, 230))
    HUD[0] = HUD[1] = None
    score = 0
    lives = 3
    hud(score, lives)
    sx = 150.0
    shown_x = None
    aliens = []      # [x, y, drawn x, drawn y]
    shots = []       # [x, y, drawn y]
    wait = 1.0       # seconds until the next alien
    reload = 0.0
    st = Steer((LEFT, RIGHT), True)
    last = now() if now else 0
    while lives > 0:
        k = key()
        if k == CLR:
            if message(["ENTER: quit", "CLEAR: keep playing"], "Quit?") == OK:
                return
            # the box covered the middle: paint it all back
            cls(BG)
            rect(0, 22, 320, 2, (60, 70, 120))
            HUD[0] = HUD[1] = None
            hud(score, lives)
            shown_x = None
            for a in aliens:
                a[3] = -100
            for s in shots:
                s[2] = -100
            last = now() if now else 0
            continue
        if now:
            t = now()
            dt = min(0.25, max(0.01, t - last))
            last = t
        else:
            dt = 0.15
        d = st.feed(k)
        if d == LEFT:
            sx -= SHIP_V * dt
        elif d == RIGHT:
            sx += SHIP_V * dt
        if sx < 4 or sx > 316 - SW:
            sx = max(4.0, min(316.0 - SW, sx))
            st.stop()
        speed = min(80.0, 22.0 + score * 1.5)
        # new aliens and shots
        wait -= dt
        if wait <= 0 and len(aliens) < MAXA:
            a = new_alien(aliens)
            if a:
                aliens.append(a)
            wait = max(0.6, 2.2 - score * 0.05)
        reload -= dt
        if reload <= 0 and len(shots) < 3:
            shots.append([sx + SW / 2 - 1, float(SY - 6), None])
            reload = FIRE
        green, blue, gold, back = [], [], [], []
        # move the shots and look for hits
        for s in shots[:]:
            oy = s[1]
            s[1] -= SHOT_V * dt
            # a shot can jump further than an alien is tall in one frame, so
            # it hits anything between where it was and where it is now
            hit = None
            for a in aliens:
                if a[0] - 1 <= s[0] <= a[0] + AW and s[1] <= a[1] + AH and oy + 6 >= a[1]:
                    hit = a
            if hit or s[1] < TOP + 2:
                if s[2] is not None and s[2] >= 0:
                    back.append((int(s[0]), s[2], 2, 6))
                shots.remove(s)
                if hit:
                    aliens.remove(hit)
                    if hit[3] >= 0:
                        back.append((hit[2], hit[3], AW, AH))
                    score += 1
                    hud(score, lives)
                continue
            ny = int(s[1])
            if s[2] is None or s[2] < 0:
                gold.append((int(s[0]), ny, 2, 6))
            else:
                strip(int(s[0]), s[2], int(s[0]), ny, 2, 6, back)
                gold.append((int(s[0]), ny, 2, 6))
            s[2] = ny
        # move the aliens
        for a in aliens[:]:
            a[1] += speed * dt
            nx, ny = int(a[0]), int(a[1])
            if ny + AH >= SY + SH:
                # it reached the planet
                aliens.remove(a)
                if a[3] >= 0:
                    back.append((a[2], a[3], AW, AH))
                lives -= 1
                hud(score, lives)
                continue
            if ny != a[3]:
                if a[3] >= 0:
                    strip(a[2], a[3], nx, ny, AW, AH, back)
                green.append((nx, ny, AW, AH))
                back.extend(alien_cuts(nx, ny))
                a[2], a[3] = nx, ny
            # touching the ship also costs a life
            if ny + AH > SY and nx < sx + SW and nx + AW > sx:
                aliens.remove(a)
                back.append((nx, ny, AW, AH))
                lives -= 1
                hud(score, lives)
        # the ship
        ix = int(sx)
        if ix != shown_x:
            if shown_x is not None:
                strip(shown_x, SY, ix, SY, SW, SH, back)
            blue.append((ix, SY, SW, SH))
            back.extend(ship_cuts(ix))
            shown_x = ix
        paint(((ALIEN, green), (SHIP, blue), (SHOT, gold), (BG, back)))
    pause(0.4)
    message(["You stopped " + str(score) + " aliens."], "Game over")


RULES = "Aliens are drifting down toward the planet. Your ship fires by itself: glide under them and stop them before they reach the bottom. 3 lives."
KEYS = ["Left/Right: glide", "Opposite arrow: stop", "CLEAR: quit"]


def main():
    while True:
        c = home("GHSTAR", "STAR PATROL", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
