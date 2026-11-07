# GHHANG from GAMEHUB, on its own. Run it.
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
icons_INK = (20, 20, 20)
icons_BG = {'GHHANG': icons_WHITE}
def icons_c_(c):
 set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
 icons_c_(c)
 fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))
def icons_line(x1, y1, x2, y2, c, t=1):
 icons_c_(c)
 for o in range(t):
  draw_line(int(x1) + o, int(y1), int(x2) + o, int(y2))
def icons_circ(x, y, r, c):
 icons_c_(c)
 fill_circle(int(x), int(y), int(r))
def icons_hangman(x, y, c):
 icons_box(x - 19, y + 15, 24, 3, icons_INK)
 icons_box(x - 13, y - 18, 3, 34, icons_INK)
 icons_box(x - 13, y - 18, 24, 3, icons_INK)
 icons_line(x - 11, y - 9, x - 3, y - 17, icons_INK, 2)
 icons_box(x + 8, y - 16, 2, 6, (140, 90, 40))
 icons_circ(x + 9, y - 6, 4, icons_INK)
 icons_circ(x + 9, y - 6, 2, icons_WHITE)
 icons_line(x + 9, y - 2, x + 9, y + 7, icons_INK, 2)
 icons_line(x + 9, y + 1, x + 4, y + 5, icons_INK)
 icons_line(x + 10, y + 1, x + 15, y + 5, icons_INK)
 icons_line(x + 9, y + 7, x + 5, y + 13, icons_INK)
 icons_line(x + 10, y + 7, x + 14, y + 13, icons_INK)
icons_ICONS = {'GHHANG': icons_hangman}
def icons_bg(mod):
 return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
 f = icons_ICONS.get(mod)
 if f:
  f(x, y, c)
hang_WORDS = 'PLANET ROCKET GALAXY COMET ORBIT JUNGLE TIGER PARROT DOLPHIN OCTOPUS PENGUIN CASTLE DRAGON WIZARD KNIGHT PIRATE TREASURE ISLAND VOLCANO DESERT GLACIER THUNDER RAINBOW BLIZZARD TORNADO PUZZLE RIDDLE SECRET MYSTERY CIPHER LANTERN CANDLE MIRROR LADDER BASKET GUITAR TRUMPET VIOLIN PIANO DRUMS PENCIL ERASER NOTEBOOK BACKPACK LOCKER SCIENCE HISTORY ALGEBRA GEOMETRY CALCULUS PIZZA PANCAKE WAFFLE NOODLE BURRITO PRETZEL COOKIE MUFFIN BANANA AVOCADO'.split()
hang_ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
hang_INK = (20, 20, 20)
hang_POST = (225, 175, 20)
hang_USED = (190, 190, 190)
def hang_letter_box(i, used, sel):
 x = 4 + i % 13 * 24
 y = 150 + i // 13 * 28
 c = GOLD if i == sel else hang_USED if hang_ABC[i] in used else hang_INK
 rect(x, y, 22, 24, WHITE)
 rbox(x, y, 22, 24, 5, c, 2, WHITE)
 text(x + 6, y + 18, hang_ABC[i], c)
def hang_word_line(w, used):
 rect(120, 60, 200, 30, WHITE)
 s = ''
 for ch in w:
  s += (ch if ch in used else '_') + ' '
 text(310 - len(s) * 10, 85, s.strip(), hang_INK)
def hang_figure(n):
 if n == 0:
  rrect(0, 136, 120, 12, 5, (110, 180, 90))
  rect(0, 140, 120, 4, (80, 150, 70))
  rect(8, 132, 74, 6, hang_POST)
  rect(8, 136, 74, 2, dk(hang_POST, 0.75))
  rect(24, 18, 5, 116, hang_POST)
  rect(27, 18, 2, 116, dk(hang_POST, 0.75))
  rect(24, 18, 52, 5, hang_POST)
  rect(24, 21, 52, 2, dk(hang_POST, 0.75))
  col(hang_POST)
  for o in range(4):
   draw_line(29 + o, 44, 50 + o, 23)
  rect(72, 23, 3, 13, (140, 90, 40))
  return
 col(hang_INK)
 if n == 1:
  ring(73, 46, 10, hang_INK, 2, WHITE)
  return
 a = ((73, 56, 73, 95), (73, 65, 60, 82), (73, 65, 86, 82), (73, 95, 62, 118), (73, 95, 84, 118))[n - 2]
 for o in (0, 1):
  draw_line(a[0] + o, a[1], a[2] + o, a[3])
def hang_game():
 w = random.choice(hang_WORDS)
 used = ''
 bad = 0
 sel = 0
 cls(WHITE)
 hang_figure(0)
 for i in range(26):
  hang_letter_box(i, used, sel)
 hang_word_line(w, used)
 while True:
  done = True
  for ch in w:
   if ch not in used:
    done = False
  if done:
   message(['You got it: ' + w], 'You win!')
   return
  if bad >= 6:
   message(['The word was ' + w], 'Out of guesses')
   return
  k = wkey()
  old = sel
  if k == LEFT:
   sel = (sel - 1) % 26
  elif k == RIGHT:
   sel = (sel + 1) % 26
  elif k == UP or k == DOWN:
   sel = (sel + 13) % 26
  elif k == CLR:
   return
  elif k == OK and hang_ABC[sel] not in used:
   used += hang_ABC[sel]
   if hang_ABC[sel] in w:
    hang_word_line(w, used)
   else:
    bad += 1
    hang_figure(bad)
  hang_letter_box(old, used, sel)
  hang_letter_box(sel, used, sel)
hang_RULES = 'Guess the hidden word one letter at a time. Six wrong guesses and the game is over.'
hang_KEYS = ['Arrows: pick a letter', 'ENTER: guess it', 'CLEAR: quit']
def hang_main():
 while True:
  c = home('GHHANG', 'HANGMAN', hang_RULES, hang_KEYS, ('Play', 'Back'))
  if c < 0:
   return
  hang_game()
hang_main()
RAN = True
