# GHBREAK from GAMEHUB, on its own. Run it.
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
def block(x, y, w, h, c, e=2):
 rect(x, y, w, h, c)
 rect(x, y, w, e, lt(c))
 rect(x, y, e, h, lt(c))
 rect(x, y + h - e, w, e, dk(c))
 rect(x + w - e, y + e, e, h - e, dk(c))
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
icons_BG = {'GHBREAK': (30, 70, 170)}
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
def icons_rr(x, y, w, h, r, c):
 icons_c_(c)
 fill_rect(x + r - 1, y - 1, w - 2 * r + 1, h + 1)
 fill_rect(x - 1, y + r - 1, w + 1, h - 2 * r + 1)
 for cx in (x + r, x + w - r - 1):
  for cy in (y + r, y + h - r - 1):
   fill_circle(cx, cy, r)
def icons_breakout(x, y, c):
 cols = ((220, 60, 60), (235, 140, 50), (230, 210, 60), (70, 190, 90))
 for r in range(3):
  for i in range(4):
   bx = x - 19 + i * 10
   icons_box(bx, y - 15 + r * 6, 9, 5, cols[(i + r) % 4])
   icons_hline(bx, bx + 8, y - 15 + r * 6, tuple((min(255, v + 60) for v in cols[(i + r) % 4])))
 for i, (dx, dy) in enumerate(((-8, 12), (-5, 8))):
  icons_box(x + dx, y + dy, 2, 2, (120, 150, 230))
 icons_circ(x - 1, y + 5, 2, icons_WHITE)
 icons_rr(x - 11, y + 13, 22, 4, 1, icons_WHITE)
icons_ICONS = {'GHBREAK': icons_breakout}
def icons_bg(mod):
 return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
 f = icons_ICONS.get(mod)
 if f:
  f(x, y, c)
break_ROWS = 5
break_COLS = 10
break_BW = 30
break_BH = 10
break_BY = 34
break_RC = ((220, 60, 60), (235, 140, 50), (230, 210, 60), (70, 190, 90), (170, 90, 210))
break_PW = 46
break_BG = (30, 70, 170)
def break_brick(r, c, on):
 if on:
  block(10 + c * break_BW + 1, break_BY + r * break_BH + 1, break_BW - 2, break_BH - 2, break_RC[r], 2)
 else:
  rect(10 + c * break_BW + 1, break_BY + r * break_BH + 1, break_BW - 2, break_BH - 2, break_BG)
def break_walls():
 rect(0, 24, 4, 186, (200, 210, 230))
 rect(316, 24, 4, 186, (200, 210, 230))
 rect(3, 24, 1, 186, (120, 130, 160))
 rect(316, 24, 1, 186, (120, 130, 160))
break_PC = (230, 120, 60)
break_PL = (255, 200, 150)
def break_paddle(x):
 rect(x + 1, 192, break_PW - 2, 1, break_PC)
 rect(x, 193, 4, 2, break_PC)
 rect(x + 4, 193, break_PW - 8, 2, break_PL)
 rect(x + break_PW - 4, 193, 4, 2, break_PC)
 rect(x, 195, break_PW, 4, break_PC)
 rect(x + 1, 199, break_PW - 2, 1, break_PC)
 for cx, cy in ((x, 192), (x + break_PW - 1, 192), (x, 199), (x + break_PW - 1, 199)):
  rect(cx, cy, 1, 1, break_BG)
def break_puck(x, y):
 rect(x - 3, y - 3, 6, 6, WHITE)
 rect(x - 2, y - 2, 2, 2, (200, 220, 255))
break_HUD = [None, None]
def break_hud(score, lives):
 a = 'Score ' + str(score)
 b = 'Balls ' + str(lives)
 if a != break_HUD[0]:
  if break_HUD[0]:
   text(6, 17, break_HUD[0], break_BG)
  text(6, 17, a)
 if b != break_HUD[1]:
  if break_HUD[1]:
   text(214, 17, break_HUD[1], break_BG)
  text(214, 17, b, GOLD)
 break_HUD[0], break_HUD[1] = (a, b)
def break_game():
 cls(break_BG)
 rect(0, 22, 320, 2, WHITE)
 break_walls()
 b = [[1] * break_COLS for r in range(break_ROWS)]
 for r in range(break_ROWS):
  for c in range(break_COLS):
   break_brick(r, c, 1)
 left = break_ROWS * break_COLS
 score = 0
 lives = 3
 px = 137
 break_HUD[0] = break_HUD[1] = None
 break_hud(score, lives)
 while lives > 0 and left > 0:
  bx, by = (px + break_PW / 2, 180.0)
  vx = random.choice((-3.0, 3.0))
  vy = -3.0
  break_paddle(px)
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
    px = min(316 - break_PW, px + 7)
    if px == 316 - break_PW:
     st.stop()
   obx, oby = (bx, by)
   bx += vx
   by += vy
   if bx < 7 or bx > 312:
    vx = -vx
    bx = max(7, min(312, bx))
   if by < 26:
    vy = -vy
    by = 26
   if vy > 0 and 188 < by < 198 and (px - 3 < bx < px + break_PW + 3):
    vy = -abs(vy)
    vx = (bx - (px + break_PW / 2)) / 5
    if abs(vx) < 1:
     vx = 1 if vx >= 0 else -1
   r = int((by - break_BY) // break_BH)
   c = int((bx - 10) // break_BW)
   if 0 <= r < break_ROWS and 0 <= c < break_COLS and b[r][c]:
    b[r][c] = 0
    break_brick(r, c, 0)
    vy = -vy
    score += (break_ROWS - r) * 10
    left -= 1
    break_hud(score, lives)
    if left == 0:
     break
   vacate(int(obx) - 3, int(oby) - 3, int(bx) - 3, int(by) - 3, 6, 6, break_BG)
   if oby < break_BY + break_ROWS * break_BH + 4:
    for rr in range(max(0, int((oby - 3 - break_BY) // break_BH)), min(break_ROWS, int((oby + 3 - break_BY) // break_BH) + 1)):
     for cc in range(max(0, int((obx - 3 - 10) // break_BW)), min(break_COLS, int((obx + 3 - 10) // break_BW) + 1)):
      if b[rr][cc] and abs(rr * break_BH + break_BY + break_BH / 2 - by) + abs(cc * break_BW + 10 + break_BW / 2 - bx) > 0:
       break_brick(rr, cc, 1)
   if opx != px:
    vacate(opx, 192, px, 192, break_PW, 8, break_BG)
   if opx != px or oby > 186:
    break_paddle(px)
   break_puck(int(bx), int(by))
   if by > 210:
    lives -= 1
    break_hud(score, lives)
    break
  rect(int(bx) - 3, int(by) - 3, 6, 6, break_BG)
  rect(4, 192, 312, 8, break_BG)
 if left == 0:
  message(['Score ' + str(score)], 'All bricks cleared!')
 else:
  message(['Score ' + str(score)], 'Game over')
break_RULES = 'Bounce the ball off your paddle to break every brick. You have 3 balls.'
break_KEYS = ['Left/Right: paddle glides that way', 'ENTER: stop the paddle', 'CLEAR: quit']
def break_main():
 while True:
  c = home('GHBREAK', 'BREAKOUT', break_RULES, break_KEYS, ('Play', 'Back'))
  if c < 0:
   return
  break_game()
break_main()
RAN = True
