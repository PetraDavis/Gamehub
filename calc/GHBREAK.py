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


def brick(r, c, on):
    if on:
        block(10 + c * BW + 1, BY + r * BH + 1, BW - 2, BH - 2, RC[r], 2)
    else:
        rect(10 + c * BW + 1, BY + r * BH + 1, BW - 2, BH - 2, BG)


def walls():
    rect(0, 24, 4, 186, (200, 210, 230))
    rect(316, 24, 4, 186, (200, 210, 230))
    rect(3, 24, 1, 186, (120, 130, 160))
    rect(316, 24, 1, 186, (120, 130, 160))


PC = (230, 120, 60)
PL = (255, 200, 150)


def paddle(x):
    # pieces that never overlap, so drawing it again where it is can't flash
    rect(x + 1, 192, PW - 2, 1, PC)
    rect(x, 193, 4, 2, PC)
    rect(x + 4, 193, PW - 8, 2, PL)
    rect(x + PW - 4, 193, 4, 2, PC)
    rect(x, 195, PW, 4, PC)
    rect(x + 1, 199, PW - 2, 1, PC)
    for cx, cy in ((x, 192), (x + PW - 1, 192), (x, 199), (x + PW - 1, 199)):
        rect(cx, cy, 1, 1, BG)


def puck(x, y):
    rect(x - 3, y - 3, 6, 6, WHITE)
    rect(x - 2, y - 2, 2, 2, (200, 220, 255))


HUD = [None, None]


def hud(score, lives):
    # rub out only the old words, by writing them in the background colour
    a = "Score " + str(score)
    b = "Balls " + str(lives)
    if a != HUD[0]:
        if HUD[0]:
            text(6, 17, HUD[0], BG)
        text(6, 17, a)
    if b != HUD[1]:
        if HUD[1]:
            text(214, 17, HUD[1], BG)
        text(214, 17, b, GOLD)
    HUD[0], HUD[1] = a, b


def game():
    cls(BG)
    rect(0, 22, 320, 2, WHITE)
    walls()
    b = [[1] * COLS for r in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            brick(r, c, 1)
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
            if opx != px or oby > 186:
                paddle(px)
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
