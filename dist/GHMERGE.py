# GHMERGE from GAMEHUB, on its own. Run it.
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
icons_BG = {'GHMERGE': (187, 173, 160)}
icons_FONT = {'0': '111101101101111', '1': '010110010010111', '2': '111001111100111', '3': '111001111001111', '4': '101101111001001', '5': '111100111001111', '6': '111100111101111', '7': '111001001001001', '8': '111101111101111', '9': '111101111001111'}
def icons_c_(c):
 set_color(c[0], c[1], c[2])
def icons_rr(x, y, w, h, r, c):
 icons_c_(c)
 fill_rect(x + r, y, w - 2 * r, h)
 fill_rect(x, y + r, w, h - 2 * r)
 for cx in (x + r, x + w - r - 1):
  for cy in (y + r, y + h - r - 1):
   fill_circle(cx, cy, r)
def icons_digits(x, y, s, c, p=2):
 icons_c_(c)
 for i, ch in enumerate(s):
  bits = icons_FONT[ch]
  for n in range(15):
   if bits[n] == '1':
    fill_rect(x + i * 4 * p + n % 3 * p, y + n // 3 * p, p, p)
def icons_g2048(x, y, c):
 icons_rr(x - 20, y - 12, 41, 28, 4, (200, 160, 30))
 icons_rr(x - 20, y - 14, 41, 28, 4, (237, 194, 46))
 icons_digits(x - 14, y - 5, '2048', icons_WHITE)
icons_ICONS = {'GHMERGE': icons_g2048}
def icons_bg(mod):
 return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
 f = icons_ICONS.get(mod)
 if f:
  f(x, y, c)
merge_X0 = 90
merge_Y0 = 26
merge_S = 36
merge_BOARD = (187, 173, 160)
merge_TC = {0: (205, 193, 180), 2: (230, 225, 215), 4: (235, 220, 190), 8: (240, 170, 110), 16: (245, 140, 90), 32: (245, 110, 85), 64: (245, 80, 50), 128: (235, 205, 110), 256: (235, 200, 90), 512: (235, 195, 70), 1024: (235, 190, 50), 2048: (235, 185, 30)}
def merge_add(b):
 e = [i for i in range(16) if b[i] == 0]
 if e:
  b[random.choice(e)] = 4 if random.random() < 0.1 else 2
def merge_slide(row):
 r = [v for v in row if v]
 out = []
 pts = 0
 i = 0
 while i < len(r):
  if i + 1 < len(r) and r[i] == r[i + 1]:
   out.append(r[i] * 2)
   pts += r[i] * 2
   i += 2
  else:
   out.append(r[i])
   i += 1
 return (out + [0] * (4 - len(out)), pts)
def merge_move(b, d):
 pts = 0
 nb = b[:]
 for j in range(4):
  if d < 2:
   idx = [j * 4 + i for i in range(4)]
  else:
   idx = [i * 4 + j for i in range(4)]
  if d == 1 or d == 3:
   idx.reverse()
  row, p = merge_slide([b[i] for i in idx])
  pts += p
  for n in range(4):
   nb[idx[n]] = row[n]
 return (nb, pts)
def merge_draw(b, score):
 for i in range(16):
  v = b[i]
  x = merge_X0 + i % 4 * merge_S
  y = merge_Y0 + i // 4 * merge_S
  c = merge_TC.get(v, (235, 180, 20))
  rrect(x + 2, y + 4, merge_S - 4, merge_S - 5, 5, dk(c, 0.8))
  rrect(x + 2, y + 2, merge_S - 4, merge_S - 5, 5, c)
  if v:
   rect(x + 7, y + 4, merge_S - 14, 2, lt(c, 0.4))
  if v:
   s = str(v)
   if len(s) > 3:
    s = s[:2] + 'k' if v >= 10000 else s
   tc = (60, 55, 50) if v < 8 else WHITE
   text(x + merge_S // 2 - len(s) * 5, y + 25, s, tc)
 rect(0, 180, 320, 30, WHITE)
 rrect(110, 182, 100, 24, 6, merge_BOARD)
 ctext(200, 'Score ' + str(score), WHITE)
def merge_game():
 b = [0] * 16
 merge_add(b)
 merge_add(b)
 score = 0
 cls(WHITE)
 rrect(12, 34, 64, 64, 8, dk((235, 185, 30), 0.8))
 rrect(12, 32, 64, 64, 8, (235, 185, 30))
 text(24, 70, '2048', WHITE)
 text(12, 128, 'Join', (120, 110, 100))
 text(12, 146, 'same', (120, 110, 100))
 text(12, 164, 'tiles!', (120, 110, 100))
 text(250, 60, 'Arrows', (120, 110, 100))
 text(250, 78, 'slide', (120, 110, 100))
 rrect(merge_X0 - 4, merge_Y0 - 4, merge_S * 4 + 8, merge_S * 4 + 8, 8, merge_BOARD)
 merge_draw(b, score)
 won = False
 while True:
  k = wkey()
  d = {LEFT: 0, RIGHT: 1, UP: 2, DOWN: 3}.get(k, -1)
  if k == CLR:
   return
  if d < 0:
   continue
  nb, p = merge_move(b, d)
  if nb != b:
   b = nb
   score += p
   merge_add(b)
   merge_draw(b, score)
   if 2048 in b and (not won):
    won = True
    message(['You made 2048!', 'Keep going?'], 'Amazing!')
    cls(WHITE)
    rrect(merge_X0 - 4, merge_Y0 - 4, merge_S * 4 + 8, merge_S * 4 + 8, 8, merge_BOARD)
    merge_draw(b, score)
  stuck = True
  for dd in range(4):
   if merge_move(b, dd)[0] != b:
    stuck = False
  if stuck:
   message(['Final score ' + str(score)], 'No moves left')
   return
merge_RULES = 'Slide the tiles. Two tiles with the same number join into one. Try to make 2048!'
merge_KEYS = ['Arrows: slide all tiles', 'CLEAR: quit']
def merge_main():
 while True:
  c = home('GHMERGE', '2048', merge_RULES, merge_KEYS, ('Play', 'Back'))
  if c < 0:
   return
  merge_game()
merge_main()
RAN = True
