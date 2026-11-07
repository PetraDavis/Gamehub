# GHANIM from GAMEHUB, on its own. Run it.
from ti_draw import *
from ti_system import *
import time
import random
import math
from ti_system import store_list, recall_list
UP = 25
DOWN = 34
LEFT = 24
RIGHT = 26
OK = 105
CLR = 45
DEL = 23
SECOND = 21
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (230, 180, 40)
GREY = (110, 110, 110)
DARK = (40, 40, 40)
RED = (220, 50, 50)
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
def choose(title, opts, sel=0):
 cls()
 ctext(24, title, GOLD)
 n = len(opts)
 for i in range(n):
  y = 40 + i * 30
  c = GOLD if i == sel else WHITE
  rbox(60, y, 200, 24, 8, c)
  ctext(y + 18, opts[i], c)
 while True:
  k = wkey()
  old = sel
  if k == UP:
   sel = (sel - 1) % n
  elif k == DOWN:
   sel = (sel + 1) % n
  elif k == OK:
   return sel
  elif k == CLR:
   return -1
  for i in (old, sel):
   y = 40 + i * 30
   c = GOLD if i == sel else WHITE
   edge(60, y, 200, 24, 8, c)
   ctext(y + 18, opts[i], c)
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
icons_RED = (215, 40, 40)
icons_BG = {'GHANIM': icons_WHITE}
def icons_c_(c):
 set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
 icons_c_(c)
 fill_rect(int(x) - 1, int(y) - 1, max(1, int(w)) + 1, max(1, int(h)) + 1)
def icons_circ(x, y, r, c):
 icons_c_(c)
 fill_circle(int(x), int(y), int(r))
def icons_anim(x, y, c):
 icons_box(x - 20, y - 13, 41, 27, (35, 35, 40))
 for i in range(5):
  icons_box(x - 18 + i * 8, y - 11, 4, 3, icons_WHITE)
  icons_box(x - 18 + i * 8, y + 9, 4, 3, icons_WHITE)
 for i, by in enumerate((4, -2, 2)):
  fx = x - 17 + i * 12
  icons_box(fx, y - 6, 11, 13, (120, 200, 240))
  icons_box(fx, y + 4, 11, 3, (70, 170, 80))
  icons_circ(fx + 5, y + by, 2, (240, 120, 40))
 icons_circ(x + 17, y - 9, 1, icons_RED)
icons_ICONS = {'GHANIM': icons_anim}
def icons_bg(mod):
 return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
 f = icons_ICONS.get(mod)
 if f:
  f(x, y, c)
save_SLOTS = 3
save_PER = 100
save_B = 5
def save_hname(s):
 return 'A' + str(s) + 'H'
def save_dname(s, i):
 n = str(i)
 return 'A' + str(s) + '0' * (3 - len(n)) + n
def save_info(s):
 try:
  h = recall_list(save_hname(s))
  if len(h) >= 4 and int(h[0]) == 1:
   return (int(h[1]), int(h[2]))
 except Exception:
  pass
 return None
def save_save(s, data, frames, fps, show=None):
 nums = []
 n = len(data)
 i = 0
 while i < n:
  v = 0
  for j in range(save_B):
   v = v * 256 + (data[i + j] if i + j < n else 0)
  nums.append(v)
  i += save_B
 nl = (len(nums) + save_PER - 1) // save_PER
 for k in range(nl):
  if show:
   show(k, nl)
  store_list(save_dname(s, k), nums[k * save_PER:(k + 1) * save_PER])
 old = 0
 try:
  old = int(recall_list(save_hname(s))[3])
 except Exception:
  pass
 for k in range(nl, old):
  try:
   store_list(save_dname(s, k), [0])
  except Exception:
   pass
 store_list(save_hname(s), [1, frames, fps, nl, n])
 return nl
def save_load(s, show=None):
 h = recall_list(save_hname(s))
 frames, fps, nl, n = (int(h[1]), int(h[2]), int(h[3]), int(h[4]))
 data = bytearray(n)
 p = 0
 for k in range(nl):
  if show:
   show(k, nl)
  for v in recall_list(save_dname(s, k)):
   v = int(v)
   chunk = []
   for j in range(save_B):
    chunk.append(v % 256)
    v //= 256
   for j in range(save_B - 1, -1, -1):
    if p < n:
     data[p] = chunk[j]
     p += 1
 return (data, frames, fps)
anim_CWD = 32
anim_CHG = 24
anim_N = anim_CWD * anim_CHG
anim_P = 6
anim_CX = 6
anim_CY = 26
anim_PAL = ((255, 255, 255), (0, 0, 0), (128, 128, 128), (200, 200, 200), (220, 40, 40), (245, 140, 30), (250, 220, 50), (60, 190, 70), (20, 100, 40), (80, 200, 230), (40, 80, 200), (20, 30, 90), (150, 60, 190), (245, 140, 190), (130, 80, 40), (245, 200, 160))
anim_INK = (20, 20, 20)
anim_HI = (200, 120, 0)
anim_MAXB = 60000
anim_KEYGAP = 15
def anim_enc_key(fr):
 out = bytearray([1])
 i = 0
 while i < anim_N:
  c = fr[i]
  n = 1
  while i + n < anim_N and fr[i + n] == c and (n < 255):
   n += 1
  out.append(n)
  out.append(c)
  i += n
 return bytes(out)
def anim_enc_delta(prev, fr):
 out = bytearray([0])
 pos = 0
 i = 0
 while i < anim_N:
  if fr[i] == prev[i]:
   i += 1
   continue
  j = i
  last = i
  while j < anim_N and j - i < 254:
   if fr[j] != prev[j]:
    j += 1
    last = j
   elif j + 1 < anim_N and fr[j + 1] != prev[j + 1]:
    j += 1
   else:
    break
  j = last
  skip = i - pos
  while skip > 255:
   out.append(255)
   out.append(0)
   skip -= 255
  out.append(skip)
  out.append(j - i)
  t = i
  while t < j:
   hi = fr[t]
   lo = fr[t + 1] if t + 1 < j else 0
   out.append(hi * 16 + lo)
   t += 2
  pos = j
  i = j
 return bytes(out)
def anim_apply(fr, d):
 if d[0] == 1:
  p = 1
  i = 0
  while p < len(d):
   n = d[p]
   c = d[p + 1]
   for t in range(n):
    fr[i + t] = c
   i += n
   p += 2
  return
 p = 1
 pos = 0
 L = len(d)
 while p < L:
  pos += d[p]
  n = d[p + 1]
  p += 2
  for t in range(n):
   b = d[p + t // 2]
   fr[pos + t] = b >> 4 if t % 2 == 0 else b & 15
  p += (n + 1) // 2
  pos += n
class anim_Studio:
 pass
def anim_dec(s, i):
 k = i
 while k > 0 and s.F[k][0] != 1:
  k -= 1
 fr = bytearray(anim_N)
 for j in range(k, i + 1):
  anim_apply(fr, s.F[j])
 return fr
def anim_chain(s, i):
 n = 0
 k = i
 while k > 0 and s.F[k][0] != 1:
  k -= 1
  n += 1
 return n
def anim_encode_at(s, i, fr, prev):
 if prev is None:
  return anim_enc_key(fr)
 d = anim_enc_delta(prev, fr)
 if i > 0 and anim_chain(s, i - 1) + 1 >= anim_KEYGAP:
  return anim_enc_key(fr)
 return d
def anim_commit(s):
 if not s.dirty:
  return
 i = s.ci
 nx = None
 if i + 1 < len(s.F) and s.F[i + 1][0] == 0:
  nx = anim_dec(s, i + 1)
 s.F[i] = anim_encode_at(s, i, s.cur, s.prv if i > 0 else None)
 if nx is not None:
  s.F[i + 1] = anim_enc_delta(s.cur, nx)
 s.dirty = False
def anim_used(s):
 t = 0
 for f in s.F:
  t += len(f) + 2
 return t
def anim_want(s, i):
 v = s.cur[i]
 if v == 0 and s.onion and (s.ci > 0) and s.prv[i]:
  return 16 + s.prv[i]
 return v
def anim_paint(s, i, v):
 x = anim_CX + i % anim_CWD * anim_P
 y = anim_CY + i // anim_CWD * anim_P
 if v >= 16:
  c = anim_PAL[v - 16]
  w = anim_PAL[0]
  rect(x, y, anim_P, 1, w)
  rect(x, y + anim_P - 1, anim_P, 1, w)
  rect(x, y + 1, 1, anim_P - 2, w)
  rect(x + anim_P - 1, y + 1, 1, anim_P - 2, w)
  rect(x + 1, y + 1, anim_P - 2, anim_P - 2, ((c[0] + 510) // 3, (c[1] + 510) // 3, (c[2] + 510) // 3))
 else:
  rect(x, y, anim_P, anim_P, anim_PAL[v])
 s.shown[i] = v
def anim_refresh(s, src=None):
 runs = {}
 onion = []
 hide = s.hide
 for r in range(anim_CHG):
  base = r * anim_CWD
  c = 0
  while c < anim_CWD:
   i = base + c
   v = src[i] if src is not None else anim_want(s, i)
   if v >= 16 or (i == hide and s.shown[i] == v):
    if s.shown[i] != v:
     onion.append((i, v))
    c += 1
    continue
   e = c
   dirty = False
   while e < anim_CWD:
    j = base + e
    w = src[j] if src is not None else anim_want(s, j)
    if w != v or (j == hide and s.shown[j] == v):
     break
    if s.shown[j] != v:
     dirty = True
     s.shown[j] = v
    e += 1
   if dirty:
    if v in runs:
     runs[v].append((c, r, e - c))
    else:
     runs[v] = [(c, r, e - c)]
   c = e
 for v in runs:
  for c, r, n in runs[v]:
   rect(anim_CX + c * anim_P, anim_CY + r * anim_P, n * anim_P, anim_P, anim_PAL[v])
 for i, v in onion:
  anim_paint(s, i, v)
def anim_cursor(s):
 x = anim_CX + s.cx * anim_P
 y = anim_CY + s.cy * anim_P
 v = s.cur[s.cy * anim_CWD + s.cx]
 col(BLACK if v in (0, 3, 6, 15) else WHITE)
 draw_rect(x, y, anim_P - 2, anim_P - 2)
 s.hide = s.cy * anim_CWD + s.cx
def anim_uncursor(s):
 i = s.cy * anim_CWD + s.cx
 s.hide = -1
 anim_paint(s, i, anim_want(s, i))
def anim_label(s, key, x, y, t, c, bg=WHITE):
 old = s.lab.get(key)
 s.lab[key] = (t, c)
 if old is None:
  text(x, y, t, c)
  return
 o, oc = old
 for k in range(max(len(o), len(t))):
  a = o[k] if k < len(o) else ' '
  b = t[k] if k < len(t) else ' '
  if a != b:
   if a != ' ':
    rect(x + k * 10, y - 12, 10, 16, bg)
   if b != ' ':
    text(x + k * 10, y, b, c)
  elif oc != c and b != ' ':
   text(x + k * 10, y, b, c)
def anim_swatch(s, c, sel=-1):
 x = 210 + c % 4 * 26
 y = 30 + c // 4 * 26
 e = anim_INK if c == sel else GOLD if c == s.col else WHITE
 rect(x - 2, y - 2, 26, 2, e)
 rect(x - 2, y + 22, 26, 2, e)
 rect(x - 2, y, 2, 22, e)
 rect(x + 22, y, 2, 22, e)
def anim_palette(s):
 for c in range(16):
  x = 210 + c % 4 * 26
  y = 30 + c // 4 * 26
  rect(x + 1, y + 1, 20, 20, anim_PAL[c])
  if c == 0:
   col(GREY)
   draw_rect(x, y, 20, 20)
  anim_swatch(s, c)
def anim_topbar(s):
 pct = anim_used(s) * 100 // anim_MAXB
 anim_label(s, 'fr', 4, 17, 'Frame ' + str(s.ci + 1) + '/' + str(len(s.F)), anim_INK)
 anim_label(s, 'fps', 160, 17, str(s.fps) + 'fps', GREY)
 anim_label(s, 'mem', 236, 17, 'Mem ' + str(pct) + '%', RED if pct > 90 else GREY)
def anim_botbar(s, a=None, b=None):
 if a is None:
  a = ('Pen up', 'PEN DOWN', 'ERASER')[s.pen]
  ca = anim_HI if s.pen else anim_INK
 else:
  ca = anim_HI
 anim_label(s, 'b1', 6, 190, a, ca)
 anim_label(s, 'b2', 6, 206, b or 'ENTER pen DEL eraser 2nd menu', GREY)
def anim_side(s):
 rect(anim_MX, 22, 320 - anim_MX, 154, WHITE)
 s.lab.pop('on', None)
 s.lab.pop('sv', None)
 anim_palette(s)
 anim_sidetext(s)
def anim_sidetext(s):
 anim_label(s, 'on', 210, 150, 'Onion ' + ('on' if s.onion else 'off'), GREY)
 anim_label(s, 'sv', 210, 168, 'Saved ' + (str(s.slot) if s.slot else '-'), GREY)
def anim_full(s):
 cls(WHITE)
 rect(anim_CX - 2, anim_CY - 2, anim_CWD * anim_P + 4, 2, DARK)
 rect(anim_CX - 2, anim_CY + anim_CHG * anim_P, anim_CWD * anim_P + 4, 2, DARK)
 rect(anim_CX - 2, anim_CY, 2, anim_CHG * anim_P, DARK)
 rect(anim_CX + anim_CWD * anim_P, anim_CY, 2, anim_CHG * anim_P, DARK)
 s.shown = bytearray(anim_N)
 s.hide = -1
 s.lab = {}
 anim_refresh(s)
 anim_side(s)
 anim_topbar(s)
 anim_botbar(s)
 anim_cursor(s)
def anim_update(s):
 anim_uncursor(s)
 anim_refresh(s)
 anim_topbar(s)
 anim_sidetext(s)
 anim_botbar(s)
 anim_cursor(s)
def anim_set_px(s, i, c):
 if s.cur[i] != c:
  if not s.dirty:
   s.undo = bytearray(s.cur)
  s.cur[i] = c
  s.dirty = True
  s.changed = True
def anim_fill(s):
 i0 = s.cy * anim_CWD + s.cx
 old = s.cur[i0]
 new = s.col
 if old == new:
  return
 s.undo = bytearray(s.cur)
 stack = [i0]
 while stack:
  i = stack.pop()
  if s.cur[i] != old:
   continue
  s.cur[i] = new
  x = i % anim_CWD
  if x > 0:
   stack.append(i - 1)
  if x < anim_CWD - 1:
   stack.append(i + 1)
  if i >= anim_CWD:
   stack.append(i - anim_CWD)
  if i < anim_N - anim_CWD:
   stack.append(i + anim_CWD)
 s.dirty = True
 s.changed = True
def anim_go(s, j):
 anim_commit(s)
 if j == s.ci + 1:
  s.prv = s.cur
  s.cur = bytearray(s.prv)
  anim_apply(s.cur, s.F[j])
 else:
  s.cur = anim_dec(s, j)
  s.prv = anim_dec(s, j - 1) if j > 0 else bytearray(anim_N)
 s.ci = j
 s.undo = None
def anim_add_frame(s, blank):
 if anim_used(s) > anim_MAXB:
  message(['Memory is full.', 'Save, or delete frames.'], "Can't add")
  s.broke = True
  return
 anim_commit(s)
 i = s.ci
 nx = anim_dec(s, i + 1) if i + 1 < len(s.F) else None
 new = bytearray(anim_N) if blank else bytearray(s.cur)
 s.F.insert(i + 1, anim_enc_delta(s.cur, new))
 if nx is not None and s.F[i + 2][0] == 0:
  s.F[i + 2] = anim_enc_delta(new, nx)
 s.prv = s.cur
 s.cur = new
 s.ci = i + 1
 s.changed = True
def anim_del_frame(s):
 if len(s.F) == 1:
  s.undo = bytearray(s.cur)
  s.cur = bytearray(anim_N)
  s.dirty = True
  return
 i = s.ci
 nx = anim_dec(s, i + 1) if i + 1 < len(s.F) else None
 p = anim_dec(s, i - 1) if i > 0 else None
 del s.F[i]
 if nx is not None:
  s.F[i] = anim_enc_key(nx) if p is None else anim_enc_delta(p, nx)
 if i >= len(s.F):
  i = len(s.F) - 1
 s.dirty = False
 s.ci = i
 s.cur = anim_dec(s, i)
 s.prv = anim_dec(s, i - 1) if i > 0 else bytearray(anim_N)
 s.changed = True
def anim_play(s):
 anim_commit(s)
 anim_uncursor(s)
 anim_botbar(s, 'Playing. Up/Down: speed', 'Any other key stops')
 i = 0
 fr = bytearray(anim_N)
 while True:
  if s.F[i][0] == 1 or i == 0:
   fr = bytearray(anim_N)
  anim_apply(fr, s.F[i])
  anim_refresh(s, fr)
  anim_label(s, 'fr', 4, 17, 'Frame ' + str(i + 1) + '/' + str(len(s.F)), anim_INK)
  steps = max(1, 12 // s.fps)
  stop = False
  for q in range(steps):
   k = key()
   if k == UP and s.fps < 12:
    s.fps += 1
    anim_topbar(s)
   elif k == DOWN and s.fps > 1:
    s.fps -= 1
    anim_topbar(s)
   elif k and k not in (UP, DOWN):
    stop = True
    break
   pause(1 / 12)
  if stop:
   break
  i = (i + 1) % len(s.F)
 while key():
  pass
 s.cur = anim_dec(s, s.ci)
 anim_update(s)
anim_ITEMS = ('Color', 'Fill area', 'Undo', 'Clear frame', 'Next frame', 'Prev frame', 'Add copy', 'Add blank', 'Del frame', 'Play', 'Speed', 'Onion skin', 'Save', 'Load', 'New', 'Quit')
anim_MX = 202
anim_MY = 24
anim_MH = 25
anim_MV = 6
def anim_mbox(x, y, w, h, c):
 rect(x + 4, y, w - 8, 2, c)
 rect(x + 4, y + h - 2, w - 8, 2, c)
 rect(x, y + 4, 2, h - 8, c)
 rect(x + w - 2, y + 4, 2, h - 8, c)
 rect(x + 2, y + 2, 2, 2, c)
 rect(x + w - 4, y + 2, 2, 2, c)
 rect(x + 2, y + h - 4, 2, 2, c)
 rect(x + w - 4, y + h - 4, 2, 2, c)
def anim_mrow(s, r, i, on):
 y = anim_MY + r * anim_MH
 c = GOLD if on else WHITE
 if s.lab.get(('mb', r)) != c:
  anim_mbox(anim_MX + 1, y, 116, 22, c)
  s.lab['mb', r] = c
 anim_label(s, ('m', r), anim_MX + 5, y + 16, anim_ITEMS[i], c, BLACK)
def anim_menu(s, sel):
 rect(anim_MX, 22, 320 - anim_MX, 154, BLACK)
 for r in range(anim_MV):
  s.lab.pop(('mb', r), None)
  s.lab.pop(('m', r), None)
 anim_botbar(s, 'MENU  Up/Down: pick', 'ENTER: do it  2nd: close')
 top = min(max(0, sel - 2), 16 - anim_MV)
 for r in range(anim_MV):
  anim_mrow(s, r, top + r, top + r == sel)
 while True:
  k = wkey()
  old = sel
  if k == UP:
   sel = (sel - 1) % 16
  elif k == DOWN:
   sel = (sel + 1) % 16
  elif k in (LEFT, RIGHT):
   sel = (sel + 8) % 16
  elif k == OK:
   break
  elif k in (CLR, SECOND):
   sel = -1
   break
  nt = top
  if sel < top:
   nt = sel
  elif sel >= top + anim_MV:
   nt = sel - anim_MV + 1
  top = nt
  for r in range(anim_MV):
   anim_mrow(s, r, top + r, top + r == sel)
 anim_side(s)
 anim_botbar(s)
 return sel
def anim_pick_color(s):
 sel = s.col
 anim_swatch(s, sel, sel)
 anim_botbar(s, 'Arrows: pick a colour', 'ENTER: use it  CLEAR: back')
 while True:
  k = wkey()
  old = sel
  if k == LEFT:
   sel = (sel - 1) % 16
  elif k == RIGHT:
   sel = (sel + 1) % 16
  elif k == UP:
   sel = (sel - 4) % 16
  elif k == DOWN:
   sel = (sel + 4) % 16
  elif k == OK:
   old = s.col
   s.col = sel
   anim_swatch(s, old)
   break
  elif k == CLR:
   break
  if sel != old:
   anim_swatch(s, old, sel)
   anim_swatch(s, sel, sel)
 anim_swatch(s, sel)
 anim_swatch(s, s.col)
 anim_botbar(s)
def anim_pick_speed(s):
 cls()
 ctext(80, 'PLAYBACK SPEED', GOLD)
 ctext(140, 'ENTER done', GREY)
 s.lab = {}
 while True:
  t = '< ' + str(s.fps) + ' frames a second >'
  anim_label(s, 'sp', 160 - len(t) * 5, 110, t, WHITE, BLACK)
  k = wkey()
  if k == LEFT and s.fps > 1:
   s.fps -= 1
  elif k == RIGHT and s.fps < 12:
   s.fps += 1
  elif k in (OK, CLR):
   return
def anim_pick_slot(title):
 opts = []
 for sl in range(1, save_SLOTS + 1):
  inf = save_info(sl)
  opts.append('Slot ' + str(sl) + (': ' + str(inf[0]) + ' fr' if inf else ': empty'))
 opts.append('Cancel')
 c = choose(title, opts)
 if c < 0 or c == save_SLOTS:
  return 0
 return c + 1
def anim_progress(k, n):
 rect(60, 120, 200, 30, BLACK)
 rbox(60, 120, 200, 16, 6, WHITE)
 rect(64, 124, max(2, 192 * (k + 1) // n), 8, GOLD)
def anim_do_save(s):
 anim_commit(s)
 sl = anim_pick_slot('SAVE TO')
 if not sl:
  return
 cls()
 ctext(100, 'Saving...', GOLD)
 data = bytearray()
 for f in s.F:
  data.append(len(f) // 256)
  data.append(len(f) % 256)
  data.extend(f)
 try:
  save_save(sl, data, len(s.F), s.fps, anim_progress)
  s.slot = sl
  s.changed = False
  message([str(len(s.F)) + ' frames saved', 'to slot ' + str(sl) + '.'], 'Saved')
 except Exception as e:
  message(['Could not save:', str(e)[:24]], 'Error')
def anim_do_load(s):
 sl = anim_pick_slot('LOAD FROM')
 if not sl or not save_info(sl):
  return
 if s.changed and message(['Unsaved changes will', 'be lost. ENTER: load', 'CLEAR: cancel'], 'Load?') != OK:
  return
 cls()
 ctext(100, 'Loading...', GOLD)
 try:
  data, frames, fps = save_load(sl, anim_progress)
 except Exception as e:
  message(['Could not load:', str(e)[:24]], 'Error')
  return
 F = []
 p = 0
 for k in range(frames):
  n = data[p] * 256 + data[p + 1]
  F.append(bytes(data[p + 2:p + 2 + n]))
  p += 2 + n
 anim_reset(s, F, fps)
 s.slot = sl
def anim_reset(s, F, fps):
 s.F = F
 s.fps = fps
 s.ci = 0
 s.cur = anim_dec(s, 0)
 s.prv = bytearray(anim_N)
 s.dirty = False
 s.changed = False
 s.undo = None
 s.slot = 0
def anim_studio():
 s = anim_Studio()
 anim_reset(s, [anim_enc_key(bytearray(anim_N))], 6)
 s.cx = 16
 s.cy = 12
 s.col = 1
 s.pen = 0
 s.onion = True
 s.shown = bytearray([255] * anim_N)
 s.hide = -1
 s.lab = {}
 msel = 0
 anim_full(s)
 held = 0
 hc = 0
 while True:
  k = key()
  if k == held and k:
   hc += 1
  else:
   hc = 0
  rep = k != held or (hc > 3 and hc % 1 == 0)
  held = k
  if not k:
   pause(0.01)
   continue
  if k in (LEFT, RIGHT, UP, DOWN) and rep:
   anim_uncursor(s)
   if k == LEFT and s.cx > 0:
    s.cx -= 1
   elif k == RIGHT and s.cx < anim_CWD - 1:
    s.cx += 1
   elif k == UP and s.cy > 0:
    s.cy -= 1
   elif k == DOWN and s.cy < anim_CHG - 1:
    s.cy += 1
   if s.pen:
    i = s.cy * anim_CWD + s.cx
    anim_set_px(s, i, s.col if s.pen == 1 else 0)
    anim_paint(s, i, anim_want(s, i))
   anim_cursor(s)
   continue
  if not rep:
   continue
  if k == OK or k == DEL:
   want_pen = 1 if k == OK else 2
   s.pen = 0 if s.pen == want_pen else want_pen
   if s.pen:
    i = s.cy * anim_CWD + s.cx
    anim_set_px(s, i, s.col if s.pen == 1 else 0)
    if s.shown[i] != anim_want(s, i):
     anim_uncursor(s)
     anim_cursor(s)
   anim_botbar(s)
   anim_topbar(s)
   continue
  if k == CLR and s.pen:
   s.pen = 0
   anim_botbar(s)
   continue
  if k == SECOND or k == CLR:
   s.pen = 0
   c = anim_menu(s, msel)
   if c >= 0:
    msel = c
   s.broke = False
   if c == 0:
    anim_pick_color(s)
   elif c == 1:
    anim_fill(s)
   elif c == 2 and s.undo is not None:
    u = s.undo
    s.undo = bytearray(s.cur)
    s.cur = u
    s.dirty = True
   elif c == 3:
    s.undo = bytearray(s.cur)
    s.cur = bytearray(anim_N)
    s.dirty = True
   elif c == 4:
    if s.ci + 1 < len(s.F):
     anim_go(s, s.ci + 1)
    else:
     anim_add_frame(s, False)
   elif c == 5 and s.ci > 0:
    anim_go(s, s.ci - 1)
   elif c == 6:
    anim_add_frame(s, False)
   elif c == 7:
    anim_add_frame(s, True)
   elif c == 8:
    anim_del_frame(s)
   elif c == 9:
    anim_play(s)
   elif c == 10:
    anim_pick_speed(s)
    s.broke = True
   elif c == 11:
    s.onion = not s.onion
   elif c == 12:
    anim_do_save(s)
    s.broke = True
   elif c == 13:
    anim_do_load(s)
    s.broke = True
   elif c == 14:
    if s.changed:
     s.broke = True
    if not s.changed or message(['Unsaved changes will', 'be lost. ENTER: new', 'CLEAR: cancel'], 'New?') == OK:
     anim_reset(s, [anim_enc_key(bytearray(anim_N))], 6)
   elif c == 15:
    if not s.changed or message(['Unsaved changes will', 'be lost. ENTER: quit', 'CLEAR: cancel'], 'Quit?') == OK:
     return
    s.broke = True
   if s.broke:
    anim_full(s)
   elif c != 9:
    anim_update(s)
anim_RULES = 'Draw a picture, add frames, and play them back. Saves stay on the calculator.'
anim_KEYS = ['Arrows: move  ENTER: pen', 'DEL: eraser  2nd: menu', 'Menu: colors, frames, play,', 'speed, save and load']
def anim_main():
 while True:
  c = home('GHANIM', 'ANIMATION STUDIO', anim_RULES, anim_KEYS, ('Play', 'Back'))
  if c < 0:
   return
  anim_studio()
anim_main()
RAN = True
