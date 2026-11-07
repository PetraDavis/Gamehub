# GHBLOCKS from GAMEHUB, on its own. Run it.
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
def lt(c, k=0.35):
 return (int(c[0] + (255 - c[0]) * k), int(c[1] + (255 - c[1]) * k), int(c[2] + (255 - c[2]) * k))
def dk(c, k=0.65):
 return (int(c[0] * k), int(c[1] * k), int(c[2] * k))
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
icons_BG = {'GHBLOCKS': (40, 30, 90)}
def icons_c_(c):
 set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
 icons_c_(c)
 fill_rect(int(x) - 1, int(y) - 1, max(1, int(w)) + 1, max(1, int(h)) + 1)
def icons_line(x1, y1, x2, y2, c, t=1):
 icons_c_(c)
 for o in range(t):
  draw_line(int(x1) + o, int(y1), int(x2) + o, int(y2))
def icons_hline(x1, x2, y, c, t=1):
 icons_c_(c)
 for o in range(t):
  draw_line(int(x1), int(y) + o, int(x2), int(y) + o)
def icons_bevel(x, y, s, c):
 lt = tuple((min(255, v + 70) for v in c))
 dk = tuple((v // 2 for v in c))
 icons_box(x, y, s, s, c)
 icons_hline(x, x + s - 1, y, lt)
 icons_line(x, y, x, y + s - 1, lt)
 icons_hline(x, x + s - 1, y + s - 1, dk)
 icons_line(x + s - 1, y, x + s - 1, y + s - 1, dk)
def icons_blocks(x, y, c):
 s = 8
 cells = ((-2, 1, (220, 70, 70)), (-1, 1, (220, 70, 70)), (0, 1, (70, 110, 220)), (1, 1, (70, 110, 220)), (-2, 0, (80, 190, 90)), (0, 0, (70, 110, 220)), (1, 0, (230, 200, 60)), (-2, -1, (80, 190, 90)), (1, -1, (230, 200, 60)), (-1, -3, (170, 90, 210)), (0, -3, (170, 90, 210)), (0, -2, (170, 90, 210)))
 for cx, cy, col in cells:
  icons_bevel(x + cx * s, y + cy * s + 2, s, col)
icons_ICONS = {'GHBLOCKS': icons_blocks}
def icons_bg(mod):
 return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
 f = icons_ICONS.get(mod)
 if f:
  f(x, y, c)
try:
 from time import monotonic as blocks_now
except Exception:
 blocks_now = None
blocks_CW = 10
blocks_CH = 20
blocks_C = 9
blocks_OUT = (50, 20, 70)
blocks_WELL = (35, 30, 90)
blocks_PANEL = (70, 35, 100)
blocks_X0 = 115
blocks_Y0 = 22
blocks_SHAPES = (((0, 1), (1, 1), (2, 1), (3, 1)), ((0, 0), (1, 0), (0, 1), (1, 1)), ((1, 0), (0, 1), (1, 1), (2, 1)), ((0, 0), (0, 1), (1, 1), (2, 1)), ((2, 0), (0, 1), (1, 1), (2, 1)), ((1, 0), (2, 0), (0, 1), (1, 1)), ((0, 0), (1, 0), (1, 1), (2, 1)))
blocks_COLS = ((90, 200, 220), (230, 200, 60), (170, 90, 210), (70, 110, 220), (230, 140, 50), (80, 190, 90), (220, 70, 70))
def blocks_cells(p):
 s, r, x, y = p
 out = []
 for cx, cy in blocks_SHAPES[s]:
  rx, ry = (cx, cy)
  if s != 1:
   for i in range(r):
    rx, ry = (2 - ry, rx)
  out.append((x + rx, y + ry))
 return out
def blocks_cells_i(p):
 s, r, x, y = p
 if r % 2 == 0:
  return [(x + i, y + 1) for i in range(4)]
 return [(x + 2, y + i) for i in range(4)]
def blocks_get(p):
 return blocks_cells_i(p) if p[0] == 0 else blocks_cells(p)
def blocks_ok(b, p):
 for x, y in blocks_get(p):
  if x < 0 or x >= blocks_CW or y >= blocks_CH:
   return False
  if y >= 0 and b[y][x]:
   return False
 return True
def blocks_bevel(todo, c):
 lo, hi = (dk(c, 0.55), lt(c, 0.45))
 for px, py in todo:
  rect(px, py, blocks_C, blocks_C, lo)
 for px, py in todo:
  rect(px, py, blocks_C - 1, blocks_C - 1, hi)
 for px, py in todo:
  rect(px + 1, py + 1, blocks_C - 2, blocks_C - 2, c)
class blocks_Well:

 def __init__(self):
  self.s = [[0] * blocks_CW for i in range(blocks_CH)]
  self.last = []

 def show(self, b, p, full=False):
  new = [c for c in blocks_get(p) if c[1] >= 0] if p else []
  if full:
   cells = [(x, y) for y in range(blocks_CH) for x in range(blocks_CW)]
  else:
   cells = self.last + new
  self.last = new
  v = p[0] + 1 if p else 0
  ch = {}
  for c in cells:
   x, y = c
   w = v if c in new else b[y][x]
   if self.s[y][x] != w:
    self.s[y][x] = w
    ch[c] = w
  run = None
  for y in range(blocks_CH):
   for x in range(blocks_CW + 1):
    e = x < blocks_CW and ch.get((x, y)) == 0
    if e and run is None:
     run = x
    elif not e and run is not None:
     rect(blocks_X0 + run * blocks_C, blocks_Y0 + y * blocks_C, (x - run) * blocks_C, blocks_C, blocks_WELL)
     run = None
  for w in range(1, 8):
   todo = [(blocks_X0 + x * blocks_C, blocks_Y0 + y * blocks_C) for (x, y), u in ch.items() if u == w]
   if todo:
    blocks_bevel(todo, blocks_COLS[w - 1])
def blocks_side(score, lines, nxt, old):
 if old is None:
  for y, h in ((26, 64), (96, 40), (142, 40)):
   rbox(226, y, 88, h, 6, (150, 110, 190), 2, blocks_PANEL)
  text(234, 44, 'NEXT', (200, 185, 230))
  text(234, 114, 'SCORE', (200, 185, 230))
  text(234, 160, 'LINES', (200, 185, 230))
  old = (None, None, None)
 if nxt != old[2]:
  rect(240, 50, 40, 22, blocks_PANEL)
  blocks_bevel([(244 + x * 9, 54 + y * 9) for x, y in blocks_get((nxt, 0, 0, 0))], blocks_COLS[nxt])
 if score != old[0]:
  if old[0] is not None:
   text(234, 131, str(old[0]), blocks_PANEL)
  text(234, 131, str(score))
 if lines != old[1]:
  if old[1] is not None:
   text(234, 177, str(old[1]), blocks_PANEL)
  text(234, 177, str(lines))
 return (score, lines, nxt)
def blocks_game():
 b = [[0] * blocks_CW for i in range(blocks_CH)]
 cls(blocks_OUT)
 for i in range(0, 210, 30):
  rect(0, i, 320, 15, (58, 25, 80))
 rbox(blocks_X0 - 4, blocks_Y0 - 4, blocks_CW * blocks_C + 8, blocks_CH * blocks_C + 8, 4, WHITE, 2, blocks_WELL)
 well = blocks_Well()
 rbox(4, 26, 96, 56, 6, GOLD, 2, blocks_PANEL)
 text(14, 48, 'STACK', GOLD)
 text(14, 68, 'DROP', GOLD)
 for i, cc in enumerate(blocks_COLS[:5]):
  rect(12 + i * 16, 96, 11, 11, cc)
 rbox(4, 150, 96, 40, 6, (150, 110, 190), 2, blocks_PANEL)
 text(12, 167, '2nd key:', (200, 185, 230))
 text(12, 184, 'drop it', (200, 185, 230))
 score = 0
 lines = 0
 nxt = random.randint(0, 6)
 p = None
 t = 0
 held = 0
 hc = 0
 sd = blocks_side(score, lines, nxt, None)
 last = blocks_now() if blocks_now else 0
 while True:
  if p is None:
   p = [nxt, 0, 3, -1]
   nxt = random.randint(0, 6)
   sd = blocks_side(score, lines, nxt, sd)
   if not blocks_ok(b, p):
    message(['Score ' + str(score), 'Lines ' + str(lines)], 'Stacked to the top')
    return
   well.show(b, p)
  k = key()
  if k == CLR:
   return
  speed = max(2, 14 - lines // 5)
  q = list(p)
  if k == held and k:
   hc += 1
  else:
   hc = 0
  if k != held or k == DOWN or (k in (LEFT, RIGHT) and hc > 4 and (hc % 2 == 0)):
   if k == LEFT:
    q[2] -= 1
   elif k == RIGHT:
    q[2] += 1
   elif k == UP:
    q[1] = (q[1] + 1) % 4
    if not blocks_ok(b, q):
     q[2] -= 1
     if not blocks_ok(b, q):
      q[2] += 2
   elif k == DOWN:
    t = speed
   elif k == SECOND:
    while blocks_ok(b, [q[0], q[1], q[2], q[3] + 1]):
     q[3] += 1
    t = speed
  held = k
  if blocks_now:
   tn = blocks_now()
   fall = t >= speed or tn - last >= speed * 0.035
   if fall:
    last = tn
  else:
   t += 1
   fall = t >= speed
  if q != p and blocks_ok(b, q):
   p = q
   well.show(b, p)
  if fall:
   t = 0
   q = [p[0], p[1], p[2], p[3] + 1]
   if blocks_ok(b, q):
    p = q
    well.show(b, p)
   else:
    for x, y in blocks_get(p):
     if y >= 0:
      b[y][x] = p[0] + 1
    full = [y for y in range(blocks_CH) if 0 not in b[y]]
    if full:
     for y in full:
      del b[y]
      b.insert(0, [0] * blocks_CW)
     lines += len(full)
     score += (0, 100, 300, 500, 800)[len(full)]
     well.show(b, None, True)
     sd = blocks_side(score, lines, nxt, sd)
    p = None
  pause(0.02)
blocks_RULES = "Shapes fall from the top. Fit them together to fill whole rows, which then clear. Don't let the stack reach the top."
blocks_KEYS = ['Left/Right: move', 'Up: turn', 'Down: drop faster', '2nd: drop all the way', 'CLEAR: quit']
def blocks_main():
 while True:
  c = home('GHBLOCKS', 'STACK DROP', blocks_RULES, blocks_KEYS, ('Play', 'Back'))
  if c < 0:
   return
  blocks_game()
blocks_main()
RAN = True
