# GHPONG from GAMEHUB, on its own. Run it.
from ti_draw import *
from ti_system import *
import time
import random
import math
UP = 25
DOWN = 34
LEFT = 24
RIGHT = 26
OK = 105
CLR = 45
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (230, 180, 40)
GREY = (110, 110, 110)
H = 210
def key():
 return get_key(0)
class Steer:

 def __init__(self, keys, stop_on_back=False):
  self.keys = keys
  self.back = stop_on_back
  self.d = 0

 def feed(self, k):
  if k in self.keys:
   if self.back and self.d and (k != self.d) and (self.keys.index(k) // 2 == self.keys.index(self.d) // 2):
    self.d = 0
   else:
    self.d = k
  elif k:
   self.d = 0
  return self.d

 def stop(self):
  self.d = 0
def wkey():
 return wait_key()
_C = [None]
def col(c):
 if c != _C[0]:
  _C[0] = c
  set_color(c[0], c[1], c[2])
def fr(x, y, w, h):
 fill_rect(x - 1, y - 1, w + 1, h + 1)
def rect(x, y, w, h, c):
 if w < 1 or h < 1:
  return
 col(c)
 fill_rect(x - 1, y - 1, w + 1, h + 1)
COVER = [0]
def cls(c=BLACK):
 COVER[0] += 1
 col(c)
 fill_rect(-1, -1, 321, 211)
TY = 6
def text(x, y, s, c=WHITE):
 col(c)
 draw_text(x, y + TY, s)
def ctext(y, s, c=WHITE, cx=160):
 col(c)
 draw_text(cx - len(s) * 5, y + TY, s)
def circ(x, y, r, c):
 col(c)
 fill_circle(x, y, r)
def lt(c, k=0.35):
 return (int(c[0] + (255 - c[0]) * k), int(c[1] + (255 - c[1]) * k), int(c[2] + (255 - c[2]) * k))
def dk(c, k=0.65):
 return (int(c[0] * k), int(c[1] * k), int(c[2] * k))
def ring(x, y, r, c, t=2, inner=BLACK):
 col(c)
 fill_circle(x, y, r)
 col(inner)
 fill_circle(x, y, r - t)
def rrect(x, y, w, h, r, c):
 if w < 2 * r + 1 or h < 2 * r + 1:
  r = max(0, min(w, h) // 2 - 1)
 col(c)
 if w - 2 * r >= 1:
  fr(x + r, y, w - 2 * r, h)
 if h - 2 * r >= 1:
  fr(x, y + r, w, h - 2 * r)
 if r < 1:
  return
 fill_circle(x + r, y + r, r)
 fill_circle(x + w - r - 1, y + r, r)
 fill_circle(x + r, y + h - r - 1, r)
 fill_circle(x + w - r - 1, y + h - r - 1, r)
def rbox(x, y, w, h, r, c, t=2, inner=BLACK):
 rrect(x, y, w, h, r, c)
 rrect(x + t, y + t, w - 2 * t, h - 2 * t, max(r - t, 2), inner)
def edge(x, y, w, h, r, c, t=2, inner=BLACK):
 col(c)
 fr(x + r, y, w - 2 * r, t)
 fr(x + r, y + h - t, w - 2 * r, t)
 fr(x, y + r, t, h - 2 * r)
 fr(x + w - t, y + r, t, h - 2 * r)
 for cx, cy, sx, sy in ((x + r, y + r, 1, 1), (x + w - r - 1, y + r, -1, 1), (x + r, y + h - r - 1, 1, -1), (x + w - r - 1, y + h - r - 1, -1, -1)):
  col(c)
  fill_circle(cx, cy, r)
  col(inner)
  fill_circle(cx, cy, max(r - t, 2))
  ax = cx + 1 if sx > 0 else cx - r
  ay = y + t if sy > 0 else cy - r
  fr(ax, ay, r, cy + r + 1 - ay if sy > 0 else y + h - t - ay)
  ax = x + t if sx > 0 else cx - r
  ay = cy + 1 if sy > 0 else cy - r
  fr(ax, ay, cx + r + 1 - ax if sx > 0 else x + w - t - ax, r)
def vacate(ox, oy, nx, ny, w, h, c):
 if abs(nx - ox) >= w or abs(ny - oy) >= h:
  rect(ox, oy, w, h, c)
  return
 if ny > oy:
  rect(ox, oy, w, ny - oy, c)
 elif ny < oy:
  rect(ox, ny + h, w, oy - ny, c)
 y0 = max(oy, ny)
 y1 = min(oy, ny) + h
 if nx > ox:
  rect(ox, y0, nx - ox, y1 - y0, c)
 elif nx < ox:
  rect(nx + w, y0, ox - nx, y1 - y0, c)
def pause(s):
 time.sleep(s)
MSG = [0, 0]
def message(lines, title=None):
 n = len(lines) + (1 if title else 0)
 h = n * 18 + 30
 y = (H - h) // 2
 rbox(20, y, 280, h, 8, WHITE)
 MSG[0], MSG[1] = (y, h)
 COVER[0] += 1
 yy = y + 24
 if title:
  ctext(yy, title, GOLD)
  yy += 18
 for s in lines:
  ctext(yy, s)
  yy += 18
 while True:
  k = wkey()
  if k in (OK, CLR):
   return k
def _wrap(s, n=30):
 out = []
 line = ''
 for w in s.split(' '):
  if len(line) + len(w) + 1 > n:
   out.append(line)
   line = w
  else:
   line = (line + ' ' + w).strip()
 if line:
  out.append(line)
 return out
def how_to(title, rules, buttons):
 cls()
 ctext(20, 'HOW TO PLAY', GOLD)
 ctext(38, title, GREY)
 y = 60
 for ln in _wrap(rules):
  text(8, y, ln)
  y += 16
 y += 6
 text(8, y, 'BUTTONS', GOLD)
 y += 17
 for b in buttons:
  text(8, y, b)
  y += 16
 text(8, 206, 'ENTER: back', GREY)
 while wkey() not in (OK, CLR, UP, DOWN):
  pass
def home(mod, title, rules, buttons, opts=('Play', 'Back'), sel=0):
 n = len(opts)
 while True:
  cls()
  ring(160, 58, 36, GOLD, 3)
  try:
   circ(160, 58, 33, icons_bg(mod))
   icons_draw(mod, 160, 58, WHITE)
  except Exception:
   pass
  ctext(122, title, GOLD)
  ctext(146, 'Up/Down: how to play', GREY)
  bw = (300 - (n - 1) * 8) // n
  first = True
  while True:
   for i in range(n):
    x = 10 + i * (bw + 8)
    c = GOLD if i == sel else WHITE
    if first:
     rbox(x, 166, bw, 28, 10, c)
    else:
     edge(x, 166, bw, 28, 10, c)
    text(x + bw // 2 - len(opts[i]) * 5, 186, opts[i], c)
   first = False
   k = wkey()
   if k == LEFT:
    sel = (sel - 1) % n
   elif k == RIGHT:
    sel = (sel + 1) % n
   elif k in (UP, DOWN):
    how_to(title, rules, buttons)
    break
   elif k == CLR:
    return -1
   elif k == OK:
    if opts[sel] == 'Back':
     return -1
    return sel
icons_BLACK = (0, 0, 0)
icons_WHITE = (255, 255, 255)
icons_BG = {'GHPONG': (30, 85, 165)}
def icons_c_(c):
 set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
 icons_c_(c)
 fill_rect(int(x) - 1, int(y) - 1, max(1, int(w)) + 1, max(1, int(h)) + 1)
def icons_hline(x1, x2, y, c, t=1):
 icons_c_(c)
 for o in range(t):
  draw_line(int(x1), int(y) + o, int(x2), int(y) + o)
def icons_circ(x, y, r, c):
 icons_c_(c)
 fill_circle(int(x), int(y), int(r))
def icons_pong(x, y, c):
 icons_c_(icons_WHITE)
 draw_rect(x - 22, y - 16, 44, 32)
 icons_hline(x - 21, x + 21, y, (200, 210, 230))
 for i in range(6):
  icons_box(x, y - 15 + i * 6, 2, 3, icons_WHITE)
 icons_box(x - 17, y - 11, 4, 14, icons_WHITE)
 icons_box(x + 14, y - 3, 4, 14, icons_WHITE)
 icons_circ(x - 6, y - 5, 2, (250, 150, 40))
icons_ICONS = {'GHPONG': icons_pong}
def icons_bg(mod):
 return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
 f = icons_ICONS.get(mod)
 if f:
  f(x, y, c)
pong_PH = 36
pong_TOP = 24
pong_TABLE = (30, 85, 165)
pong_BALL = (250, 150, 40)
pong_LINE = (150, 190, 235)
def pong_net():
 col(pong_LINE)
 draw_circle(160, 117, 28)
 for y in range(pong_TOP + 2, 208, 14):
  rect(159, y, 2, 7, WHITE)
def pong_court():
 cls(pong_TABLE)
 rect(0, 207, 320, 3, pong_LINE)
 rect(0, pong_TOP + 1, 320, 1, pong_LINE)
 pong_net()
def pong_paddle(x, y, c):
 rect(x, y, 1, pong_PH, lt(c))
 rect(x + 1, y, 1, pong_PH, c)
 rect(x + 2, y, 2, 4, c)
 rect(x + 2, y + 4, 2, pong_PH - 8, lt(c, 0.5))
 rect(x + 2, y + pong_PH - 4, 2, 4, c)
 rect(x + 4, y, 1, pong_PH, c)
 rect(x + 5, y, 1, pong_PH, dk(c))
def pong_puck(x, y):
 rect(x - 4, y - 4, 8, 8, pong_BALL)
 rect(x - 2, y - 2, 2, 2, lt(pong_BALL, 0.6))
def pong_scores(a, b):
 rect(0, 0, 320, pong_TOP - 2, pong_TABLE)
 text(110, 18, str(a))
 text(200, 18, str(b), GOLD)
 rect(0, pong_TOP - 2, 320, 2, WHITE)
 text(14, 18, 'YOU', pong_LINE)
 text(250, 18, 'CALC', pong_LINE)
def pong_game():
 pong_court()
 me = cpu = 0
 py = cy = 100
 pong_scores(me, cpu)
 serve = 1
 while me < 7 and cpu < 7:
  bx, by = (160.0, 110.0)
  vx = 4.0 * serve
  vy = random.choice((-2.5, -1.5, 1.5, 2.5))
  pong_paddle(8, py, WHITE)
  pong_paddle(306, cy, GOLD)
  pause(0.5)
  st = Steer((UP, DOWN))
  while True:
   k = key()
   if k == CLR:
    return
   opy, ocy = (py, cy)
   d = st.feed(k)
   if d == UP:
    py = max(pong_TOP + 3, py - 6)
    if py == pong_TOP + 3:
     st.stop()
   elif d == DOWN:
    py = min(206 - pong_PH, py + 6)
    if py == 206 - pong_PH:
     st.stop()
   target = by - pong_PH / 2
   if vx > 0 and bx > 120:
    cy += max(-4, min(4, target - cy))
   cy = int(max(pong_TOP + 3, min(206 - pong_PH, cy)))
   obx, oby = (bx, by)
   bx += vx
   by += vy
   if by < pong_TOP + 6 or by > 202:
    vy = -vy
    by = max(pong_TOP + 6, min(202, by))
   if bx < 18 and vx < 0 and (py - 4 < by < py + pong_PH + 4):
    vx = min(9, -vx * 1.06)
    vy += (by - (py + pong_PH / 2)) / 6
    bx = 18
   if bx > 302 and vx > 0 and (cy - 4 < by < cy + pong_PH + 4):
    vx = max(-9, -vx * 1.06)
    vy += (by - (cy + pong_PH / 2)) / 6
    bx = 302
   vacate(int(obx) - 4, int(oby) - 4, int(bx) - 4, int(by) - 4, 8, 8, pong_TABLE)
   if opy != py:
    vacate(8, opy, 8, py, 6, pong_PH, pong_TABLE)
   if ocy != cy:
    vacate(306, ocy, 306, cy, 6, pong_PH, pong_TABLE)
   if 126 < obx < 194:
    pong_net()
   if opy != py or 0 < obx < 24:
    pong_paddle(8, py, WHITE)
   if ocy != cy or 296 < obx < 320:
    pong_paddle(306, cy, GOLD)
   pong_puck(int(bx), int(by))
   if bx < 0:
    cpu += 1
    serve = 1
    break
   if bx > 320:
    me += 1
    serve = -1
    break
  rect(int(bx) - 4, int(by) - 4, 8, 8, pong_TABLE)
  pong_net()
  pong_scores(me, cpu)
 message(['You ' + str(me) + ' - ' + str(cpu) + ' Calculator'], 'You win!' if me > cpu else 'Calculator wins')
pong_RULES = "Bounce the ball past the calculator's paddle. First to 7 points wins."
pong_KEYS = ['Up/Down: paddle glides that way', 'ENTER: stop the paddle', 'CLEAR: quit']
def pong_main():
 while True:
  c = home('GHPONG', 'PONG', pong_RULES, pong_KEYS, ('Play', 'Back'))
  if c < 0:
   return
  pong_game()
pong_main()
RAN = True
