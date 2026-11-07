# Pong vs the calculator. Up/Down move your paddle. First to 7 wins.
from GHLIB import *
import random

PH = 36
TOP = 24


def net():
    for y in range(TOP, 210, 14):
        rect(159, y, 2, 7, DARK)


def scores(a, b):
    rect(0, 0, 320, TOP - 2, BLACK)
    text(110, 18, str(a))
    text(200, 18, str(b), GOLD)
    rect(0, TOP - 2, 320, 2, WHITE)


def game():
    cls()
    me = cpu = 0
    py = cy = 100
    scores(me, cpu)
    net()
    serve = 1
    while me < 7 and cpu < 7:
        bx, by = 160.0, 110.0
        vx = 4.0 * serve
        vy = random.choice((-2.5, -1.5, 1.5, 2.5))
        pause(0.5)
        while True:
            k = key()
            if k == CLR:
                return
            opy, ocy = py, cy
            if k == UP:
                py = max(TOP, py - 7)
            elif k == DOWN:
                py = min(210 - PH, py + 7)
            target = by - PH / 2
            if vx > 0 and bx > 120:
                cy += max(-4, min(4, target - cy))
            cy = int(max(TOP, min(210 - PH, cy)))
            obx, oby = bx, by
            bx += vx
            by += vy
            if by < TOP + 3 or by > 206:
                vy = -vy
                by = max(TOP + 3, min(206, by))
            if bx < 18 and vx < 0 and py - 4 < by < py + PH + 4:
                vx = min(9, -vx * 1.06)
                vy += (by - (py + PH / 2)) / 6
                bx = 18
            if bx > 302 and vx > 0 and cy - 4 < by < cy + PH + 4:
                vx = max(-9, -vx * 1.06)
                vy += (by - (cy + PH / 2)) / 6
                bx = 302
            rect(int(obx) - 3, int(oby) - 3, 7, 7, BLACK)
            if opy != py:
                rect(8, opy, 6, PH, BLACK)
            if ocy != cy:
                rect(306, ocy, 6, PH, BLACK)
            if 150 < obx < 170:
                net()
            rect(8, py, 6, PH, WHITE)
            rect(306, cy, 6, PH, GOLD)
            rect(int(bx) - 3, int(by) - 3, 7, 7, WHITE)
            if bx < 0:
                cpu += 1
                serve = 1
                break
            if bx > 320:
                me += 1
                serve = -1
                break
        rect(int(bx) - 3, int(by) - 3, 7, 7, BLACK)
        scores(me, cpu)
    message(["You " + str(me) + " - " + str(cpu) + " Calculator"], "You win!" if me > cpu else "Calculator wins")


def main():
    while True:
        c = choose("PONG", ["Play", "Back"])
        if c != 0:
            return
        game()
