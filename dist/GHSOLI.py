# GHSOLI from GAMEHUB, on its own. Run it.
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
RED = (220, 50, 50)
H = 210
def shuffle(a):
 for i in range(len(a) - 1, 0, -1):
  j = random.randint(0, i)
  a[i], a[j] = (a[j], a[i])
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
icons_INK = (20, 20, 20)
icons_RED = (215, 40, 40)
icons_BG = {'GHSOLI': (25, 110, 55)}
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
def icons_heart(x, y, s, c):
 icons_circ(x - s, y - 1, s, c)
 icons_circ(x + s, y - 1, s, c)
 icons_poly([x - 2 * s, x + 2 * s + 1, x], [y, y, y + 2 * s + 1], c)
def icons_diamond(x, y, s, c):
 icons_poly([x, x + s + 1, x, x - s - 1], [y - 2 * s, y, y + 2 * s, y], c)
def icons_spade(x, y, s, c):
 icons_circ(x - s, y + 1, s, c)
 icons_circ(x + s, y + 1, s, c)
 icons_poly([x - 2 * s, x + 2 * s + 1, x], [y + 1, y + 1, y - 2 * s - 1], c)
 icons_poly([x, x - s, x + s], [y + 1, y + 2 * s + 1, y + 2 * s + 1], c)
def icons_solitaire(x, y, c):
 suits = ((icons_spade, icons_INK), (icons_diamond, icons_RED), (icons_heart, icons_RED))
 for i in range(3):
  l = x - 18 + i * 10
  t = y - 12
  icons_box(l - 1, t - 1, 18, 26, icons_INK)
  icons_box(l, t, 16, 24, (250, 250, 245))
  f, col = suits[i]
  f(l + 4, t + 5, 2, col)
 icons_heart(x + 10, y + 3, 3, icons_RED)
icons_ICONS = {'GHSOLI': icons_solitaire}
def icons_bg(mod):
 return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
 f = icons_ICONS.get(mod)
 if f:
  f(x, y, c)
soli_CW = 40
soli_CHT = 30
soli_TOPY = 4
soli_TABY = 40
soli_RANKS = ('', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
soli_CARD = (245, 245, 240)
soli_BACK = (40, 80, 160)
soli_FELT = (15, 70, 40)
def soli_cx(c):
 return 6 + c * 44
soli_PICS = (('.##.##.', '#######', '#######', '#######', '.#####.', '..###..', '...#...'), ('...#...', '..###..', '.#####.', '#######', '.#####.', '..###..', '...#...'), ('...#...', '..###..', '.#####.', '#######', '#######', '..#.#..', '.#####.'), ('..###..', '..###..', '##.#.##', '#######', '##.#.##', '...#...', '.#####.'))
def soli__runs(pic):
 out = []
 for r in range(7):
  row = pic[r]
  c = 0
  while c < 7:
   if row[c] == '#':
    e = c
    while e < 7 and row[e] == '#':
     e += 1
    for k in range(len(out)):
     a = out[k]
     if a[0] == c and a[2] == e - c and (a[1] + a[3] == r):
      out[k] = (a[0], a[1], a[2], a[3] + 1)
      break
    else:
     out.append((c, r, e - c, 1))
    c = e
   else:
    c += 1
 return out
soli_SUITS = [soli__runs(p) for p in soli_PICS]
def soli_suit(x, y, s, k=1):
 c = RED if s < 2 else BLACK
 for a, b, w, h in soli_SUITS[s]:
  rect(x + a * k, y + b * k, w * k, h * k, c)
def soli_card(x, y, cd, h=soli_CHT):
 if cd is None:
  rbox(x, y, soli_CW, soli_CHT, 4, (60, 110, 80), 1, soli_FELT)
  return
 r, s, up = cd
 rrect(x, y, soli_CW, h, 4, BLACK)
 if not up:
  rrect(x + 1, y + 1, soli_CW - 2, h - 2, 3, soli_BACK)
  if h >= 12:
   rect(x + 4, y + 4, soli_CW - 8, h - 8, lt(soli_BACK, 0.15))
   for i in range(x + 7, x + soli_CW - 6, 6):
    rect(i, y + 6, 2, h - 12, soli_BACK)
  return
 rrect(x + 1, y + 1, soli_CW - 2, h - 2, 3, soli_CARD)
 if h >= 14:
  text(x + 3, y + 14, soli_RANKS[r], RED if s < 2 else BLACK)
  soli_suit(x + soli_CW - 11, y + 4, s)
 if h >= soli_CHT:
  soli_suit(x + 13, y + 15, s, 2)
class soli_G:
 pass
def soli_new():
 g = soli_G()
 deck = [[r, s, False] for s in range(4) for r in range(1, 14)]
 shuffle(deck)
 g.tab = []
 for c in range(7):
  pile = [deck.pop() for i in range(c + 1)]
  pile[-1][2] = True
  g.tab.append(pile)
 g.stock = deck
 g.waste = []
 g.found = [[], [], [], []]
 return g
def soli_layout(pile):
 dn, fu = (5, 15)
 while True:
  ys = []
  y = soli_TABY
  for cd in pile:
   ys.append(y)
   y += fu if cd[2] else dn
  if not pile or ys[-1] + soli_CHT <= 208 or fu <= 8:
   return ys
  fu -= 1
  if fu < 12:
   dn = 3
def soli_draw_col(g, c, drawn):
 pile = g.tab[c]
 x = soli_cx(c)
 ys = soli_layout(pile)
 n = len(pile)
 d = drawn[c]
 start = 0
 if d is not None and n:
  old = d[0]
  while start < min(len(old), n) and old[start] == ys[start]:
   start += 1
  start = min(start, max(0, min(len(old), n) - 1))
 if not pile:
  soli_card(x, soli_TABY, None)
  bottom = soli_TABY + soli_CHT
 else:
  bottom = ys[-1] + soli_CHT
  if d is not None and n < len(d[0]) and (start == n - 1):
   rect(x, bottom - 6, soli_CW, 6, soli_FELT)
  for i in range(start, n):
   soli_card(x, ys[i], pile[i], soli_CHT if i == n - 1 else ys[i + 1] - ys[i] + 4)
 if d is None or bottom < d[1]:
  rect(x, bottom, soli_CW, 210 - bottom, soli_FELT)
 drawn[c] = (ys, bottom)
def soli_top_state(g, s):
 if s == 0:
  return len(g.stock) > 0
 p = g.waste if s == 1 else g.found[s - 3]
 return tuple(p[-1]) if p else None
def soli_draw_slot(g, s):
 x = soli_cx(s)
 if s == 0:
  soli_card(x, soli_TOPY, [1, 0, False] if g.stock else None)
  return
 p = g.waste if s == 1 else g.found[s - 3]
 soli_card(x, soli_TOPY, p[-1] if p else None)
 if s > 1 and (not p):
  soli_suit(x + 13, soli_TOPY + 8, s - 3, 2)
def soli_frame(x, y, h, top=True):
 t = 2 if top else 0
 r = [(x - 2, y - t, 2, h + t + 2), (x + soli_CW, y - t, 2, h + t + 2), (x, y + h, soli_CW, 2)]
 if top:
  r.append((x, y - 2, soli_CW, 2))
 return r
def soli_marks(g, s, n):
 if s < 7:
  return soli_frame(soli_cx(s), soli_TOPY, soli_CHT)
 p = g.tab[s - 7]
 if not p:
  return soli_frame(soli_cx(s - 7), soli_TABY, soli_CHT)
 ys = soli_layout(p)
 i = max(0, len(p) - n)
 return soli_frame(soli_cx(s - 7), ys[i], ys[-1] + soli_CHT - ys[i], i == 0)
def soli_fits_found(cd, f, pile):
 if cd[1] != f:
  return False
 return cd[0] == (pile[-1][0] + 1 if pile else 1)
def soli_fits_tab(cd, pile):
 if not pile:
  return cd[0] == 13
 t = pile[-1]
 return t[2] and t[0] == cd[0] + 1 and ((t[1] < 2) != (cd[1] < 2))
def soli_take(g, src, n):
 if src == 1:
  return [g.waste[-1]]
 return g.tab[src - 7][-n:]
def soli_remove(g, src, n):
 if src == 1:
  g.waste.pop()
 else:
  p = g.tab[src - 7]
  del p[-n:]
  if p and (not p[-1][2]):
   p[-1][2] = True
def soli_try_move(g, src, n, dst):
 cards = soli_take(g, src, n)
 if 3 <= dst <= 6:
  if n != 1 or not soli_fits_found(cards[0], dst - 3, g.found[dst - 3]):
   return False
  soli_remove(g, src, n)
  g.found[dst - 3].append(cards[0])
  return True
 if dst >= 7 and dst != src and soli_fits_tab(cards[0], g.tab[dst - 7]):
  soli_remove(g, src, n)
  g.tab[dst - 7].extend(cards)
  return True
 return False
def soli_faceup(g, c):
 n = 0
 for cd in g.tab[c]:
  if cd[2]:
   n += 1
 return n
def soli_game():
 g = soli_new()
 cls(soli_FELT)
 cur = 7
 depth = 1
 held = None
 cols = [None] * 7
 tops = [-1] * 7
 shown = []
 while True:
  want = []
  if held:
   want += [(r, WHITE) for r in soli_marks(g, held[0], held[1])]
  want += [(r, GOLD) for r in soli_marks(g, cur, depth if held is None else 1)]
  busy = want != shown
  for r, c in shown:
   if (r, c) not in want:
    rect(r[0], r[1], r[2], r[3], soli_FELT)
  for s in (0, 1, 3, 4, 5, 6):
   st = soli_top_state(g, s)
   if st != tops[s]:
    soli_draw_slot(g, s)
    tops[s] = st
    busy = True
  for c in range(7):
   p = g.tab[c]
   if cols[c] is None or cols[c][2] != [tuple(cd) for cd in p]:
    soli_draw_col(g, c, cols)
    cols[c] = cols[c] + ([tuple(cd) for cd in p],)
    busy = True
  if busy:
   for r, c in want:
    rect(r[0], r[1], r[2], r[3], c)
   shown = want
  if sum((len(f) for f in g.found)) == 52:
   message(['All 52 cards are home.'], 'You win!')
   return
  k = wkey()
  old = cur
  if k == CLR:
   if held:
    held = None
    continue
   if message(['ENTER: quit this game', 'CLEAR: keep playing'], 'Quit?') == OK:
    return
   cls(soli_FELT)
   cols = [None] * 7
   tops = [-1] * 7
   shown = []
   continue
  if k == LEFT:
   cur = cur - 1 if cur not in (0, 7) else cur + 6
   if cur == 2:
    cur = 1
  elif k == RIGHT:
   cur = cur + 1 if cur not in (6, 13) else cur - 6
   if cur == 2:
    cur = 3
  elif k == DOWN and cur < 7:
   cur = 7 + cur
  elif k == UP and cur >= 7:
   if depth < soli_faceup(g, cur - 7) and held is None:
    depth += 1
   else:
    cur = cur - 7 if cur - 7 != 2 else 1
  elif k == DOWN and cur >= 7 and (depth > 1):
   depth -= 1
  elif k == OK:
   if held is None:
    if cur == 0:
     if g.stock:
      cd = g.stock.pop()
      cd[2] = True
      g.waste.append(cd)
     else:
      g.stock = g.waste[::-1]
      for cd in g.stock:
       cd[2] = False
      g.waste = []
    elif cur == 1 and g.waste:
     held = (1, 1)
    elif cur >= 7 and g.tab[cur - 7] and (soli_faceup(g, cur - 7) >= depth):
     held = (cur, depth)
   else:
    src, n = held
    held = None
    soli_try_move(g, src, n, cur)
  elif k == SECOND and held is None:
   src = cur if cur == 1 or cur >= 7 else -1
   if src >= 0 and (src == 1 and g.waste or (src >= 7 and g.tab[src - 7])):
    for f in range(4):
     if soli_try_move(g, src, 1, 3 + f):
      break
  if cur != old:
   depth = 1
  if cur >= 7 and depth > max(1, soli_faceup(g, cur - 7)):
   depth = max(1, soli_faceup(g, cur - 7))
soli_RULES = 'Build four piles from Ace to King, one per suit. In the columns, stack cards down in alternating colors.'
soli_KEYS = ['Arrows: move   ENTER: pick/put', 'Up/Down in a column: more cards', 'ENTER on the deck: draw', '2nd: send card to top piles', 'CLEAR: quit']
def soli_main():
 while True:
  c = home('GHSOLI', 'SOLITAIRE', soli_RULES, soli_KEYS, ('Play', 'Back'))
  if c < 0:
   return
  soli_game()
soli_main()
RAN = True
