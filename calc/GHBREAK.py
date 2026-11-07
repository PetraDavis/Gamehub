# Breakout: bounce the ball to clear every brick. Left/Right move.
from GHLIB import *
import random

ROWS = 5
COLS = 10
BW = 30
BH = 10
BY = 34
RC = ((220, 60, 60), (235, 140, 50), (230, 210, 60), (70, 190, 90), (170, 90, 210))
PW = 46
BG = (30, 70, 170)


# Each drawing call is slow on the calculator, so a brick is three
# rectangles, a whole row of bricks starts as three long ones, and the
# paddle and ball are plain rectangles.
def brick(r, c, on):
    x = 10 + c * BW + 1
    y = BY + r * BH + 1
    if on:
        rect(x, y, BW - 2, BH - 2, RC[r])
        rect(x, y, BW - 2, 2, lt(RC[r]))
        rect(x, y + BH - 4, BW - 2, 2, dk(RC[r]))
    else:
        rect(x, y, BW - 2, BH - 2, BG)


def bricks():
    w = COLS * BW - 2
    for r in range(ROWS):
        y = BY + r * BH + 1
        rect(11, y, w, BH - 2, RC[r])
        rect(11, y, w, 2, lt(RC[r]))
        rect(11, y + BH - 4, w, 2, dk(RC[r]))
    # then the thin gaps between the bricks, top to bottom in one go each
    for c in range(1, COLS):
        rect(10 + c * BW - 1, BY + 1, 2, ROWS * BH - 2, BG)


def walls():
    rect(0, 24, 4, 186, (200, 210, 230))
    rect(316, 24, 4, 186, (200, 210, 230))
    rect(3, 24, 1, 186, (120, 130, 160))
    rect(316, 24, 1, 186, (120, 130, 160))


PC = (230, 120, 60)
PL = (255, 200, 150)


def paddle(x):
    rect(x, 192, PW, 8, PC)


def puck(x, y):
    rect(x - 3, y - 3, 6, 6, WHITE)


HUD = [None, None]


def hud(score, lives):
    # the words stay; only an old number is rubbed out, by writing it in
    # the background colour
    if HUD[0] is None:
        text(6, 17, "Score")
        text(214, 17, "Balls", GOLD)
    if score != HUD[0]:
        if HUD[0] is not None:
            text(66, 17, str(HUD[0]), BG)
        text(66, 17, str(score))
    if lives != HUD[1]:
        if HUD[1] is not None:
            text(274, 17, str(HUD[1]), BG)
        text(274, 17, str(lives), GOLD)
    HUD[0], HUD[1] = score, lives


def game():
    cls(BG)
    rect(0, 22, 320, 2, WHITE)
    walls()
    b = [[1] * COLS for r in range(ROWS)]
    bricks()
    left = ROWS * COLS
    score = 0
    lives = 3
    px = 137
    HUD[0] = HUD[1] = None
    hud(score, lives)
    while lives > 0 and left > 0:
        bx, by = px + PW / 2, 180.0
        vx = random.choice((-3.0, 3.0))
        vy = -3.0
        paddle(px)
        pause(0.5)
        st = Steer((LEFT, RIGHT))
        while True:
            k = key()
            if k == CLR:
                return
            opx = px
            d = st.feed(k)
            if d == LEFT:
                px = max(4, px - 7)
                if px == 4:
                    st.stop()
            elif d == RIGHT:
                px = min(316 - PW, px + 7)
                if px == 316 - PW:
                    st.stop()
            obx, oby = bx, by
            bx += vx
            by += vy
            if bx < 7 or bx > 312:
                vx = -vx
                bx = max(7, min(312, bx))
            if by < 26:
                vy = -vy
                by = 26
            if vy > 0 and 188 < by < 198 and px - 3 < bx < px + PW + 3:
                vy = -abs(vy)
                vx = (bx - (px + PW / 2)) / 5
                if abs(vx) < 1:
                    vx = 1 if vx >= 0 else -1
            r = int((by - BY) // BH)
            c = int((bx - 10) // BW)
            if 0 <= r < ROWS and 0 <= c < COLS and b[r][c]:
                b[r][c] = 0
                brick(r, c, 0)
                vy = -vy
                score += (ROWS - r) * 10
                left -= 1
                hud(score, lives)
                if left == 0:
                    break
            vacate(int(obx) - 3, int(oby) - 3, int(bx) - 3, int(by) - 3, 6, 6, BG)
            if oby < BY + ROWS * BH + 4:
                # mend any brick the ball's old spot touched
                for rr in range(max(0, int((oby - 3 - BY) // BH)), min(ROWS, int((oby + 3 - BY) // BH) + 1)):
                    for cc in range(max(0, int((obx - 3 - 10) // BW)), min(COLS, int((obx + 3 - 10) // BW) + 1)):
                        if b[rr][cc] and abs(rr * BH + BY + BH / 2 - by) + abs(cc * BW + 10 + BW / 2 - bx) > 0:
                            brick(rr, cc, 1)
            if opx != px:
                vacate(opx, 192, px, 192, PW, 8, BG)
            if oby > 186:
                paddle(px)
            elif opx != px:
                vacate(px, 192, opx, 192, PW, 8, PC)
            puck(int(bx), int(by))
            if by > 210:
                lives -= 1
                hud(score, lives)
                break
        rect(int(bx) - 3, int(by) - 3, 6, 6, BG)
        rect(4, 192, 312, 8, BG)
    if left == 0:
        message(["Score " + str(score)], "All bricks cleared!")
    else:
        message(["Score " + str(score)], "Game over")


RULES = 'Bounce the ball off your paddle to break every brick. You have 3 balls.'
KEYS = ['Left/Right: paddle glides that way', 'ENTER: stop the paddle', 'CLEAR: quit']


def main():
    while True:
        c = home("GHBREAK", 'BREAKOUT', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
