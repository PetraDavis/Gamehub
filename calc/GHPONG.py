# Pong vs the calculator. Up/Down move your paddle. First to 7 wins.
from GHLIB import *
import random

PH = 36
TOP = 24
TABLE = (30, 85, 165)
BALL = (250, 150, 40)


LINE = (150, 190, 235)


def net():
    col(LINE)
    draw_circle(160, 117, 28)
    for y in range(TOP + 2, 208, 14):
        rect(159, y, 2, 7, WHITE)


def court():
    cls(TABLE)
    rect(0, 207, 320, 3, LINE)
    rect(0, TOP + 1, 320, 1, LINE)
    net()


def paddle(x, y, c):
    # side by side pieces that never overlap, so redrawing it can't flash
    rect(x, y, 1, PH, lt(c))
    rect(x + 1, y, 1, PH, c)
    rect(x + 2, y, 2, 4, c)
    rect(x + 2, y + 4, 2, PH - 8, lt(c, 0.5))
    rect(x + 2, y + PH - 4, 2, 4, c)
    rect(x + 4, y, 1, PH, c)
    rect(x + 5, y, 1, PH, dk(c))


def puck(x, y):
    rect(x - 4, y - 4, 8, 8, BALL)
    rect(x - 2, y - 2, 2, 2, lt(BALL, 0.6))


def scores(a, b):
    rect(0, 0, 320, TOP - 2, TABLE)
    text(110, 18, str(a))
    text(200, 18, str(b), GOLD)
    rect(0, TOP - 2, 320, 2, WHITE)
    text(14, 18, "YOU", LINE)
    text(250, 18, "CALC", LINE)


def game():
    court()
    me = cpu = 0
    py = cy = 100
    scores(me, cpu)
    serve = 1
    while me < 7 and cpu < 7:
        bx, by = 160.0, 110.0
        vx = 4.0 * serve
        vy = random.choice((-2.5, -1.5, 1.5, 2.5))
        paddle(8, py, WHITE)
        paddle(306, cy, GOLD)
        pause(0.5)
        st = Steer((UP, DOWN))
        while True:
            k = key()
            if k == CLR:
                return
            opy, ocy = py, cy
            d = st.feed(k)
            if d == UP:
                py = max(TOP + 3, py - 6)
                if py == TOP + 3:
                    st.stop()
            elif d == DOWN:
                py = min(206 - PH, py + 6)
                if py == 206 - PH:
                    st.stop()
            target = by - PH / 2
            if vx > 0 and bx > 120:
                cy += max(-4, min(4, target - cy))
            cy = int(max(TOP + 3, min(206 - PH, cy)))
            obx, oby = bx, by
            bx += vx
            by += vy
            if by < TOP + 6 or by > 202:
                vy = -vy
                by = max(TOP + 6, min(202, by))
            if bx < 18 and vx < 0 and py - 4 < by < py + PH + 4:
                vx = min(9, -vx * 1.06)
                vy += (by - (py + PH / 2)) / 6
                bx = 18
            if bx > 302 and vx > 0 and cy - 4 < by < cy + PH + 4:
                vx = max(-9, -vx * 1.06)
                vy += (by - (cy + PH / 2)) / 6
                bx = 302
            vacate(int(obx) - 4, int(oby) - 4, int(bx) - 4, int(by) - 4, 8, 8, TABLE)
            if opy != py:
                vacate(8, opy, 8, py, 6, PH, TABLE)
            if ocy != cy:
                vacate(306, ocy, 306, cy, 6, PH, TABLE)
            if 126 < obx < 194:
                net()
            if opy != py or 0 < obx < 24:
                paddle(8, py, WHITE)
            if ocy != cy or 296 < obx < 320:
                paddle(306, cy, GOLD)
            puck(int(bx), int(by))
            if bx < 0:
                cpu += 1
                serve = 1
                break
            if bx > 320:
                me += 1
                serve = -1
                break
        rect(int(bx) - 4, int(by) - 4, 8, 8, TABLE)
        net()
        scores(me, cpu)
    message(["You " + str(me) + " - " + str(cpu) + " Calculator"], "You win!" if me > cpu else "Calculator wins")


RULES = "Bounce the ball past the calculator's paddle. First to 7 points wins."
KEYS = ['Up/Down: paddle glides that way', 'ENTER: stop the paddle', 'CLEAR: quit']


def main():
    while True:
        c = home("GHPONG", 'PONG', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
