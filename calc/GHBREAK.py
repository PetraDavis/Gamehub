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
    rect(10 + c * BW + 1, BY + r * BH + 1, BW - 2, BH - 2, RC[r] if on else BG)


def hud(score, lives):
    rect(0, 0, 320, 22, BG)
    text(6, 17, "Score " + str(score))
    text(214, 17, "Balls " + str(lives), GOLD)


def game():
    cls(BG)
    rect(0, 22, 320, 2, WHITE)
    b = [[1] * COLS for r in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            brick(r, c, 1)
    left = ROWS * COLS
    score = 0
    lives = 3
    px = 137
    hud(score, lives)
    while lives > 0 and left > 0:
        bx, by = px + PW / 2, 180.0
        vx = random.choice((-3.0, 3.0))
        vy = -3.0
        rect(px, 192, PW, 6, WHITE)
        pause(0.5)
        while True:
            k = key()
            if k == CLR:
                return
            opx = px
            if k == LEFT:
                px = max(0, px - 8)
            elif k == RIGHT:
                px = min(320 - PW, px + 8)
            obx, oby = bx, by
            bx += vx
            by += vy
            if bx < 3 or bx > 316:
                vx = -vx
                bx = max(3, min(316, bx))
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
            rect(int(obx) - 2, int(oby) - 2, 5, 5, BG)
            if opx != px:
                rect(opx, 192, PW, 6, BG)
                rect(px, 192, PW, 6, WHITE)
            rect(int(bx) - 2, int(by) - 2, 5, 5, WHITE)
            if by > 210:
                lives -= 1
                hud(score, lives)
                break
        rect(int(bx) - 2, int(by) - 2, 5, 5, BG)
        rect(0, 192, 320, 6, BG)
    if left == 0:
        message(["Score " + str(score)], "All bricks cleared!")
    else:
        message(["Score " + str(score)], "Game over")


RULES = 'Bounce the ball off your paddle to break every brick. You have 3 balls.'
KEYS = ['Left/Right: move paddle', 'CLEAR: quit']


def main():
    while True:
        c = home("GHBREAK", 'BREAKOUT', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
