# Pong vs the calculator. Up/Down move your paddle. First to 7 wins.
from GHLIB import *
import random

PH = 36
TOP = 24
TABLE = (30, 85, 165)
BALL = (250, 150, 40)


LINE = (150, 190, 235)


def net(box=None):
    # box: only repair the parts of the net an old ball square covered
    if box is None or ring_hit(box):
        col(LINE)
        draw_circle(160, 117, 28)
    for y in range(TOP + 2, 208, 14):
        if box is None or (box[1] < y + 7 and y < box[1] + 8 and box[0] < 161 and 159 < box[0] + 8):
            rect(159, y, 2, 7, WHITE)


def ring_hit(b):
    # does the 8x8 square at b touch the centre circle's line?
    x0, y0 = b
    nx = min(max(160, x0), x0 + 7) - 160
    ny = min(max(117, y0), y0 + 7) - 117
    fx = max(abs(x0 - 160), abs(x0 + 7 - 160))
    fy = max(abs(y0 - 117), abs(y0 + 7 - 117))
    return nx * nx + ny * ny <= 29 * 29 and fx * fx + fy * fy >= 27 * 27


def court():
    cls(TABLE)
    rect(0, 207, 320, 3, LINE)
    rect(0, TOP + 1, 320, 1, LINE)
    net()


# Each drawing call is slow on the calculator, so paddles and the ball are
# plain rectangles and a moving paddle only paints the strips it gains and
# leaves.
def paddle(x, y, c):
    rect(x, y, 6, PH, c)


def puck(x, y):
    rect(x - 4, y - 4, 8, 8, BALL)


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
            ob = (int(obx) - 4, int(oby) - 4)
            vacate(ob[0], ob[1], int(bx) - 4, int(by) - 4, 8, 8, TABLE)
            if opy != py:
                vacate(8, opy, 8, py, 6, PH, TABLE)
            if ocy != cy:
                vacate(306, ocy, 306, cy, 6, PH, TABLE)
            if 0 < obx < 24:
                paddle(8, py, WHITE)
            elif opy != py:
                vacate(8, py, 8, opy, 6, PH, WHITE)
            if 126 < obx < 194:
                net(ob)
            if 296 < obx < 320:
                paddle(306, cy, GOLD)
            elif ocy != cy:
                vacate(306, cy, 306, ocy, 6, PH, GOLD)
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
