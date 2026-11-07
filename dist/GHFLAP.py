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
def ring(x, y, r, c, t=2, inner=BLACK):
 col(c)
 fill_circle(x, y, r)
 col(inner)
 fill_circle(x, y, r - t)
def _corners(x, y, w, h, r, t):
 if r <= t:
  return ((x, y, w, t), (x, y + h - t, w, t), (x, y + t, t, h - 2 * t), (x + w - t, y + t, t, h - 2 * t))
 a = min(r // 2, 2 * t)
 return ((x + r, y, w - 2 * r, t), (x + r, y + h - t, w - 2 * r, t), (x, y + r, t, h - 2 * r), (x + w - t, y + r, t, h - 2 * r), (x + a, y + t, r - a, t), (x + w - r, y + t, r - a, t), (x + a, y + h - 2 * t, r - a, t), (x + w - r, y + h - 2 * t, r - a, t), (x + t, y + a, t, r - a), (x + w - 2 * t, y + a, t, r - a), (x + t, y + h - r, t, r - a), (x + w - 2 * t, y + h - r, t, r - a))
def rbox(x, y, w, h, r, c, t=2, inner=BLACK, fill=True):
 edge(x, y, w, h, r, c, t)
 if not fill:
  return
 col(inner)
 if r <= t:
  fr(x + t, y + t, w - 2 * t, h - 2 * t)
  return
 a = min(r // 2, 2 * t)
 fr(x + t, y + r, w - 2 * t, h - 2 * r)
 fr(x + r, y + t, w - 2 * r, t)
 fr(x + r, y + h - 2 * t, w - 2 * r, t)
 if r > 2 * t:
  fr(x + a, y + 2 * t, w - 2 * a, r - 2 * t)
  fr(x + a, y + h - r, w - 2 * a, r - 2 * t)
def edge(x, y, w, h, r, c, t=2, inner=BLACK):
 col(c)
 for bx, by, bw, bh in _corners(x, y, w, h, r, t):
  if bw > 0 and bh > 0:
   fr(bx, by, bw, bh)
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
  old = -1
  while True:
   for i in range(n):
    if not first and i != sel and (i != old):
     continue
    x = 10 + i * (bw + 8)
    c = GOLD if i == sel else WHITE
    if first:
     rbox(x, 166, bw, 28, 10, c, 2, BLACK, False)
    else:
     edge(x, 166, bw, 28, 10, c)
    text(x + bw // 2 - len(opts[i]) * 5, 186, opts[i], c)
   first = False
   old = sel
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
flap_INK = (20, 20, 20)
flap_BODY = (240, 200, 40)
flap_BEAK = (245, 140, 30)
flap_GRAV = 900.0
flap_FLAP = -265.0
flap_FALL = 430.0
flap_SPEED = 80.0
def flap_column(gy):
 return [(flap_TOP, gy, flap_LEAF), (gy, gy + flap_GAP, flap_SKY), (gy + flap_GAP, flap_GND, flap_LEAF)]
flap_SKYCOL = [(flap_TOP, flap_GND, flap_SKY)]
def flap_bg(p, trees):
 for t in trees:
  if 0 <= p - t[0] // 2 < flap_NP:
   return t[2]
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
def flap_spans(cols, out):
 run = {}
 for p, sp in cols:
  keep = {}
  for s in sp:
   if s in run and run[s][1] == p:
    keep[s] = (run[s][0], p + 1)
   else:
    keep[s] = (p, p + 1)
  for s in run:
   if s not in keep or keep[s][0] != run[s][0]:
    flap__span(s, run[s], out)
  run = keep
 for s in run:
  flap__span(s, run[s], out)
def flap__span(s, r, out):
 y0, y1, c = s
 if y1 > y0:
  out.append((c, r[0] * 2, y0, (r[1] - r[0]) * 2, y1 - y0))
def flap_clip(sp, a, b):
 out = []
 for y0, y1, c in sp:
  y0 = max(y0, a)
  y1 = min(y1, b)
  if y1 > y0:
   out.append((y0, y1, c))
 return out
def flap_batch(todo):
 todo.sort()
 for c, x, y, w, h in todo:
  rect(x, y, w, h, c)
def flap_bird(y):
 rect(flap_BX - 7, y - 6, 14, 12, flap_BODY)
 rect(flap_BX + 7, y - 1, 5, 4, flap_BEAK)
 rect(flap_BX + 2, y - 3, 3, 3, flap_INK)
def flap_ground():
 rect(0, 196, 320, 5, (70, 170, 80))
 rect(0, 201, 320, 9, (120, 80, 40))
 for x in range(0, 320, 20):
  rect(x + 6, 204, 4, 2, (95, 60, 30))
def flap_crashed(y, trees):
 if y + 7 >= flap_GND:
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
def flap_new_tree(x):
 gy = random.randint(20, 55) * 2
 return [x, gy, flap_column(gy)]
def flap_game():
 cls(flap_SKY)
 flap_ground()
 rect(0, 20, 320, 2, flap_INK)
 text(6, 17, 'Score', flap_INK)
 text(66, 17, '0', flap_INK)
 trees = [flap_new_tree(332), flap_new_tree(332 + 172)]
 shown = [flap_SKYCOL] * 160
 y = 100.0
 v = 0.0
 score = 0
 passed = [False, False]
 go = 0.0
 oy = int(y)
 flap_bird(oy)
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
  v = min(flap_FALL, v + flap_GRAV * dt)
  y += v * dt
  if y < flap_TOP + 7:
   y = flap_TOP + 7.0
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
    trees[i] = t = flap_new_tree(max(332, trees[1 - i][0] + 172))
    passed[i] = False
   for p in (a, t[0] // 2):
    lo = min(lo, max(0, p))
    hi = max(hi, min(160, p + flap_NP))
   if not passed[i] and t[0] + flap_TW < flap_BX - flap_BR:
    passed[i] = True
    text(66, 17, str(score), flap_SKY)
    score += 1
    text(66, 17, str(score), flap_INK)
  work = []
  hit = False
  for p in range(lo, hi):
   n = flap_bg(p, trees)
   if n is not shown[p]:
    d = flap_diff(shown[p], n)
    if d:
     work.append((p, d))
     if flap_BX - 8 <= p * 2 <= flap_BX + 12:
      hit = True
    shown[p] = n
  todo = []
  flap_spans(work, todo)
  ny = int(y)
  if ny != oy:
   a, b = (oy - 6, ny - 6) if ny > oy else (ny + 6, oy + 6)
   flap_spans([(p, flap_clip(shown[p], a, b)) for p in range((flap_BX - 8) // 2, (flap_BX + 13) // 2)], todo)
  flap_batch(todo)
  if ny != oy or hit:
   flap_bird(ny)
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
