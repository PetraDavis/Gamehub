# GHBENCH - measures how long each kind of drawing takes on this calculator.
# Run it, wait for the results screen, and tell Claude the numbers.
from ti_draw import *
from ti_system import *
import time
try:
    from time import monotonic as now
except Exception:
    now = time.time
N = 60
res = []


def t(name, f):
    a = now()
    for i in range(N):
        f(i)
    b = now()
    res.append((name, (b - a) * 1000.0 / N))


set_color(255, 255, 255)
fill_rect(-1, -1, 321, 211)
t("set_color", lambda i: set_color(i * 4 % 256, 100, 50))
set_color(200, 50, 50)
t("rect 4x4", lambda i: fill_rect(i * 5 % 300, 10, 4, 4))
t("rect 40x40", lambda i: fill_rect(i * 4 % 280, 20, 40, 40))
t("rect 320x60", lambda i: fill_rect(-1, 70, 321, 60))
t("circle r4", lambda i: fill_circle(10 + i * 5 % 300, 140, 4))
t("circle r20", lambda i: fill_circle(30 + i * 4 % 260, 160, 20))
t("line", lambda i: draw_line(0, 190, 319, 200))
t("text 5", lambda i: draw_text(10, 205, "Hello"))
t("poly 4", lambda i: fill_poly([10, 30, 30, 10], [120, 120, 135, 135]))
t("python loop", lambda i: sum(range(50)))
set_color(255, 255, 255)
fill_rect(-1, -1, 321, 211)
set_color(0, 0, 0)
draw_text(10, 20, "ms per call:")
y = 36
for name, ms in res:
    draw_text(10, y, name)
    draw_text(190, y, str(int(ms * 10) / 10))
    y += 16
draw_text(10, 208, "Press any key")
wait_key()
