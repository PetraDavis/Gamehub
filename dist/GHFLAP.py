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
icons_BG = {'GHFLAP': (110, 195, 240)}
def icons_c_(c):
 set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
 icons_c_(c)
 fill_rect(int(x) - 1, int(y) - 1, max(1, int(w)) + 1, max(1, int(h)) + 1)
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
try:
 from time import monotonic as flap_now
except Exception:
 flap_now = None
flap_GAP = 64
flap_NP = 15
flap_TW = flap_NP * 2
flap_TOP = 22
flap_GND = 196
flap_BX = 60
flap_BR = 7
flap_SKY = (110, 195, 240)
flap_LEAF = (50, 140, 60)
flap_LEAF2 = (44, 126, 54)
flap_LEAFHI = (90, 175, 95)
flap_LEAFLO = (30, 95, 40)
flap_TRUNK = (110, 75, 40)
flap_INK = (20, 20, 20)
flap_ROUND = (6, 2)
flap_GRAV = 900.0
flap_FLAP = -265.0
flap_FALL = 430.0
flap_SPEED = 80.0
def flap_column(j, gy):
 k = min(j, flap_NP - 1 - j)
 yt = gy + flap_GAP
 yc = min(flap_GND, yt + 26)
 if k < 2:
  sh = flap_ROUND[k]
  c = flap_LEAFLO if k == 0 else flap_LEAF
  out = [(flap_TOP, gy - sh, c), (gy - sh, yt + sh, flap_SKY), (yt + sh, yc - sh, c), (yc - sh, flap_GND, flap_SKY)]
 else:
  leaf = flap_LEAF if j % 2 == 0 else flap_LEAF2
  out = [(flap_TOP, gy - 4, leaf), (gy - 4, gy, flap_LEAFLO), (gy, yt, flap_SKY), (yt, yt + 4, flap_LEAFHI), (yt + 4, yc, leaf)]
  if 6 <= j <= 8:
   out.append((yc, flap_GND, flap_TRUNK if j < 8 else dk(flap_TRUNK)))
  else:
   out.append((yc, flap_GND, flap_SKY))
 return out
flap_SKYCOL = [(flap_TOP, flap_GND, flap_SKY)]
def flap_bg(p, trees):
 for t in trees:
  j = p - t[0] // 2
  if 0 <= j < flap_NP:
   return flap_column(j, t[1])
 return flap_SKYCOL
def flap_diff(old, new):
 cuts = sorted(set([a for a, b, c in old] + [b for a, b, c in old] + [a for a, b, c in new] + [b for a, b, c in new]))
 out = []
 for i in range(len(cuts) - 1):
  a, b = (cuts[i], cuts[i + 1])
  if b <= a:
   continue
  m = (a + b) // 2
  co = cn = None
  for y0, y1, c in old:
   if y0 <= m < y1:
    co = c
  for y0, y1, c in new:
   if y0 <= m < y1:
    cn = c
  if cn is not None and co != cn:
   if out and out[-1][1] == a and (out[-1][2] == cn):
    out[-1] = (out[-1][0], b, cn)
   else:
    out.append((a, b, cn))
 return out
def flap_paint(cols):
 run = {}
 for p, spans in cols:
  keep = {}
  for sp in spans:
   if sp in run and run[sp][1] == p:
    keep[sp] = (run[sp][0], p + 1)
   else:
    keep[sp] = (p, p + 1)
  for sp in run:
   if sp not in keep or keep[sp][0] != run[sp][0]:
    flap__span(sp, run[sp])
  run = keep
 for sp in run:
  flap__span(sp, run[sp])
def flap__span(sp, r):
 y0, y1, c = sp
 if y1 > y0:
  rect(r[0] * 2, y0, (r[1] - r[0]) * 2, max(2, y1 - y0), c)
def flap_clip(spans, a, b):
 out = []
 for y0, y1, c in spans:
  y0 = max(y0, a)
  y1 = min(y1, b)
  if y1 > y0:
   out.append((y0, y1, c))
 return out
def flap_bird(y, wing, tilt):
 x = flap_BX
 circ(x, y, 8, (170, 120, 20))
 circ(x, y, 7, YELLOW)
 rect(x - 7, y - 2 + wing, 7, 3, (255, 245, 190))
 circ(x + 3, y - 3, 3, WHITE)
 circ(x + 4, y - 3 + (1 if tilt > 0 else 0), 1, BLACK)
 rect(x + 7, y - 1 + tilt, 5, 3, (245, 140, 30))
def flap_ground():
 rect(0, 196, 320, 5, (70, 170, 80))
 rect(0, 201, 320, 9, (120, 80, 40))
 for x in range(0, 320, 16):
  rect(x + 4, 197, 3, 2, (110, 200, 110))
  rect(x + 10, 198, 2, 2, (40, 120, 50))
  rect(x + 7, 204, 3, 2, (95, 60, 30))
  rect(x + 1, 207, 2, 2, (150, 105, 60))
def flap_score_bar(score):
 rect(0, 0, 320, 20, flap_SKY)
 text(6, 17, 'Score ' + str(score), flap_INK)
def flap_crashed(y, trees):
 if y + 8 >= flap_GND:
  return True
 for p in range((flap_BX - flap_BR) // 2, (flap_BX + flap_BR) // 2 + 1):
  for y0, y1, c in flap_bg(p, trees):
   if c == flap_SKY:
    continue
   dx = abs(p * 2 + 1 - flap_BX)
   if dx > flap_BR:
    continue
   dy = int((flap_BR * flap_BR - dx * dx) ** 0.5)
   if y0 < y + dy and y - dy < y1:
    return True
 return False
def flap_game():
 cls(flap_SKY)
 flap_ground()
 rect(0, 20, 320, 2, flap_INK)
 flap_score_bar(0)
 trees = [[332, random.randint(20, 55) * 2], [332 + 172, random.randint(20, 55) * 2]]
 shown = [flap_SKYCOL] * 160
 y = 100.0
 v = 0.0
 score = 0
 passed = [False, False]
 wing = 0
 go = 0.0
 oy = int(y)
 flap_bird(oy, 0, 0)
 pause(0.4)
 last = flap_now() if flap_now else 0
 while True:
  k = key()
  if k == CLR:
   return
  if flap_now:
   t = flap_now()
   dt = min(0.12, max(0.03, t - last))
   last = t
  else:
   dt = 0.05
  if k in (UP, SECOND, OK):
   v = flap_FLAP
   wing = 3
  v = min(flap_FALL, v + flap_GRAV * dt)
  y += v * dt
  if y < flap_TOP + 9:
   y = flap_TOP + 9.0
   v = 0.0
  go += flap_SPEED * dt
  step = int(go / 4) * 4
  go -= step
  lo, hi = (160, 0)
  for i in range(2):
   t = trees[i]
   a = t[0] // 2
   t[0] -= step
   if t[0] + flap_TW < 0:
    t[0] = max(332, trees[1 - i][0] + 172)
    t[1] = random.randint(20, 55) * 2
    passed[i] = False
   for p in (a, t[0] // 2):
    lo = min(lo, max(0, p))
    hi = max(hi, min(160, p + flap_NP))
   if not passed[i] and t[0] + flap_TW < flap_BX - flap_BR:
    passed[i] = True
    score += 1
    flap_score_bar(score)
  work = []
  for p in range(lo, hi):
   n = flap_bg(p, trees)
   if n is not shown[p] and n != shown[p]:
    d = flap_diff(shown[p], n)
    if d:
     work.append((p, d))
   shown[p] = n
  flap_paint(work)
  ny = int(y)
  a = (min(oy, ny) - 10) // 2 * 2
  b = (max(oy, ny) + 11) // 2 * 2
  flap_paint([(p, flap_clip(shown[p], a, b)) for p in range((flap_BX - 9) // 2, (flap_BX + 13) // 2)])
  wing = max(0, wing - 1)
  flap_bird(ny, wing, 1 if v > 150 else -1 if v < -100 else 0)
  oy = ny
  if flap_crashed(y, trees):
   pause(0.4)
   message(['You passed ' + str(score) + ' trees.'], 'Crash!')
   return
  pause(0.01)
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
