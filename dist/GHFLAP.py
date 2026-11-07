# GHFLAP from GAMEHUB, on its own. Run it.
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
SECOND = 21
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (230, 180, 40)
GREY = (110, 110, 110)
YELLOW = (240, 220, 60)
H = 210
def key():
 return get_key(0)
def wkey():
 return wait_key()
def col(c):
 set_color(c[0], c[1], c[2])
def rect(x, y, w, h, c):
 if w < 2 or h < 2:
  if w < 1 or h < 1:
   return
  col(c)
  draw_line(x, y, x + w - 1, y + h - 1)
  return
 col(c)
 fill_rect(x, y, w, h)
def cls(c=BLACK):
 col(c)
 fill_rect(-1, -1, 322, 212)
def text(x, y, s, c=WHITE):
 col(c)
 draw_text(x, y, s)
def ctext(y, s, c=WHITE, cx=160):
 col(c)
 draw_text(cx - len(s) * 5, y, s)
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
 col(c)
 fill_rect(x + r, y, w - 2 * r, h)
 fill_rect(x, y + r, w, h - 2 * r)
 fill_circle(x + r, y + r, r)
 fill_circle(x + w - r - 1, y + r, r)
 fill_circle(x + r, y + h - r - 1, r)
 fill_circle(x + w - r - 1, y + h - r - 1, r)
def rbox(x, y, w, h, r, c, t=2, inner=BLACK):
 rrect(x, y, w, h, r, c)
 rrect(x + t, y + t, w - 2 * t, h - 2 * t, max(r - t, 2), inner)
def pause(s):
 time.sleep(s)
def message(lines, title=None):
 n = len(lines) + (1 if title else 0)
 h = n * 18 + 30
 y = (H - h) // 2
 rbox(20, y, 280, h, 8, WHITE)
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
  while True:
   for i in range(n):
    x = 10 + i * (bw + 8)
    c = GOLD if i == sel else WHITE
    rect(x, 166, bw, 28, BLACK)
    rbox(x, 166, bw, 28, 10, c)
    text(x + bw // 2 - len(opts[i]) * 5, 186, opts[i], c)
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
icons_BG = {'GHFLAP': (110, 195, 240)}
def icons_c_(c):
 set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
 icons_c_(c)
 fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))
def icons_circ(x, y, r, c):
 icons_c_(c)
 fill_circle(int(x), int(y), int(r))
def icons_poly(xs, ys, c):
 icons_c_(c)
 fill_poly([int(v) for v in xs], [int(v) for v in ys])
def icons_ground(x, y, top, c, r=24):
 a = math.asin(top / r)
 xs = []
 ys = []
 for i in range(13):
  t = a + (math.pi - 2 * a) * i / 12
  xs.append(x + r * math.cos(t))
  ys.append(y + r * math.sin(t))
 icons_poly(xs, ys, c)
def icons_flap(x, y, c):
 icons_box(x - 14, y - 16, 10, 4, icons_WHITE)
 icons_circ(x - 12, y - 15, 3, icons_WHITE)
 icons_circ(x - 7, y - 17, 4, icons_WHITE)
 icons_ground(x, y, 15, (70, 170, 80))
 icons_box(x + 14, y + 4, 4, 12, (120, 80, 40))
 icons_circ(x + 16, y + 1, 6, (50, 140, 60))
 icons_circ(x - 2, y - 1, 11, (170, 120, 20))
 icons_circ(x - 2, y - 1, 10, (250, 215, 50))
 icons_poly([x - 14, x - 2, x - 6], [y - 1, y + 1, y + 8], (255, 245, 190))
 icons_circ(x + 3, y - 5, 4, icons_WHITE)
 icons_circ(x + 4, y - 5, 2, icons_BLACK)
 icons_poly([x + 7, x + 17, x + 7], [y - 2, y + 1, y + 2], (245, 140, 30))
 icons_poly([x + 7, x + 15, x + 7], [y + 2, y + 3, y + 5], (200, 100, 20))
icons_ICONS = {'GHFLAP': icons_flap}
def icons_bg(mod):
 return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
 f = icons_ICONS.get(mod)
 if f:
  f(x, y, c)
flap_GAP = 64
flap_TW = 26
flap_SKY = (110, 195, 240)
flap_TREE = (50, 140, 60)
flap_INK = (20, 20, 20)
def flap__bar(x, y, w, h, c):
 x0 = max(0, x)
 w = min(320, x + w) - x0
 if w >= 2 and h >= 1:
  rect(x0, y, w, h, c)
def flap__blob(x, y, r, c):
 if r <= x <= 319 - r:
  circ(x, y, r, c)
def flap_tree(x, gy, c):
 if x > 322 or x + flap_TW + 3 < 0:
  return
 hi = lt(c)
 lo = dk(c, 0.75)
 cx = x + flap_TW // 2
 top = gy + flap_GAP
 y0 = max(22, gy - 27)
 flap__bar(x - 3, y0, flap_TW + 9, gy + 1 - y0, flap_SKY)
 flap__bar(x - 3, top - 2, flap_TW + 9, min(26, 198 - top), flap_SKY)
 flap__bar(cx + 5, top + 18, 5, 196 - top - 18, flap_SKY)
 if gy - 14 > 22:
  flap__bar(x, 22, flap_TW, gy - 36, lo)
  flap__bar(x + 3, 22, flap_TW - 6, gy - 36, c)
 for bx, by, r in ((x + 5, gy - 18, 8), (x + flap_TW - 5, gy - 16, 8), (cx, gy - 9, 9)):
  if by - r >= 22:
   flap__blob(bx, by, r, c)
  else:
   flap__bar(bx - r, 22, 2 * r, by + r - 22, c)
 flap__blob(cx - 3, gy - 12, 3, hi)
 trunk = (110, 75, 40)
 flap__bar(cx - 5, top + 18, 10, 196 - top - 18, trunk)
 flap__bar(cx + 2, top + 18, 3, 196 - top - 18, dk(trunk))
 for bx, by, r in ((x + 5, top + 14, 8), (x + flap_TW - 5, top + 14, 8), (cx, top + 9, 10)):
  if by + r <= 196:
   flap__blob(bx, by, r, c)
  else:
   flap__bar(bx - r, by - r, 2 * r, 196 - by + r, c)
 flap__blob(cx - 3, top + 6, 3, hi)
 flap__blob(x + 6, top + 13, 2, hi)
def flap_bird(x, y, c, wing):
 if c == flap_SKY:
  rect(x - 8, max(22, y - 8), 20, 17, flap_SKY)
  return
 circ(x, y, 8, (170, 120, 20))
 circ(x, y, 7, c)
 rect(x - 7, y - 1 + wing, 6, 3, (255, 245, 190))
 circ(x + 3, y - 3, 3, WHITE)
 circ(x + 4, y - 3, 1, BLACK)
 rect(x + 7, y - 1, 5, 3, (245, 140, 30))
def flap_ground():
 rect(0, 196, 320, 5, (70, 170, 80))
 rect(0, 201, 320, 9, (120, 80, 40))
 for x in range(0, 320, 16):
  rect(x + 4, 197, 3, 1, (110, 200, 110))
  rect(x + 10, 198, 2, 2, (40, 120, 50))
  rect(x + 7, 204, 3, 2, (95, 60, 30))
  rect(x + 1, 207, 2, 2, (150, 105, 60))
def flap_game():
 cls(flap_SKY)
 flap_ground()
 rect(0, 20, 320, 2, flap_INK)
 trees = [[330, random.randint(40, 110)], [330 + 170, random.randint(40, 110)]]
 y = 100.0
 v = 0.0
 score = 0
 passed = [False, False]
 text(6, 17, 'Score 0', flap_INK)
 held = False
 wing = 0
 while True:
  k = key()
  if k == CLR:
   return
  if (k == UP or k == SECOND or k == OK) and (not held):
   v = -5.2
   wing = 3
  held = k in (UP, SECOND, OK)
  oy = y
  v = min(7, v + 0.55)
  y += v
  flap_bird(60, int(oy), flap_SKY, 0)
  for i in range(2):
   t = trees[i]
   flap__bar(t[0] + flap_TW - 1, 22, 6, 174, flap_SKY)
   t[0] -= 4
   if t[0] + flap_TW + 3 < 0:
    t[0] = 330
    t[1] = random.randint(40, 110)
    passed[i] = False
   flap_tree(t[0], t[1], flap_TREE)
   if not passed[i] and t[0] + flap_TW < 52:
    passed[i] = True
    score += 1
    rect(0, 0, 320, 20, flap_SKY)
    text(6, 17, 'Score ' + str(score), flap_INK)
  wing = max(0, wing - 1)
  flap_bird(60, int(y), YELLOW, wing)
  hit = y > 189 or y < 28
  for t in trees:
   if t[0] - 9 < 60 < t[0] + flap_TW + 9 and (not t[1] + 7 < y < t[1] + flap_GAP - 7):
    hit = True
  if hit:
   pause(0.4)
   message(['You passed ' + str(score) + ' trees.'], 'Crash!')
   return
flap_RULES = "Flap to fly through the gaps between the trees. Don't hit the trees or the ground."
flap_KEYS = ['Up, 2nd or ENTER: flap', 'CLEAR: quit']
def flap_main():
 while True:
  c = home('GHFLAP', 'WING IT', flap_RULES, flap_KEYS, ('Play', 'Back'))
  if c < 0:
   return
  flap_game()
flap_main()
RAN = True
