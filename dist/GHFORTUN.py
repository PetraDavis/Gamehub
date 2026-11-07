# GHFORTUN from GAMEHUB, on its own. Run it.
from ti_draw import*
from ti_system import*
import time
import random
import math
UP=25
DOWN=34
LEFT=24
RIGHT=26
OK=105
CLR=45
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
GREY=(110,110,110)
RED=(220,50,50)
def shuffle(a):
 for i in range(len(a)-1,0,-1):
  j=random.randint(0,i)
  a[i],a[j]=(a[j],a[i])
def wkey():
 return wait_key()
_C=[None]
def col(c):
 if c!=_C[0]:
  _C[0]=c
  set_color(c[0],c[1],c[2])
def fr(x,y,w,h):
 fill_rect(x-1,y-1,w+1,h+1)
def rect(x,y,w,h,c):
 if w<1 or h<1:
  return
 col(c)
 fill_rect(x-1,y-1,w+1,h+1)
COVER=[0]
def cls(c=BLACK):
 COVER[0]+=1
 col(c)
 fill_rect(-1,-1,321,211)
TY=6
def text(x,y,s,c=WHITE):
 col(c)
 draw_text(x,y+TY,s)
def ctext(y,s,c=WHITE,cx=160):
 col(c)
 draw_text(cx-len(s)*5,y+TY,s)
def circ(x,y,r,c):
 col(c)
 fill_circle(x,y,r)
def dk(c,k=0.65):
 return(int(c[0]*k),int(c[1]*k),int(c[2]*k))
def ring(x,y,r,c,t=2,inner=BLACK):
 col(c)
 fill_circle(x,y,r)
 col(inner)
 fill_circle(x,y,r-t)
def _corners(x,y,w,h,r,t):
 if r<=t:
  return((x,y,w,t),(x,y+h-t,w,t),(x,y+t,t,h-2*t),(x+w-t,y+t,t,h-2*t))
 a=min(r//2,2*t)
 return((x+r,y,w-2*r,t),(x+r,y+h-t,w-2*r,t),(x,y+r,t,h-2*r),(x+w-t,y+r,t,h-2*r),(x+a,y+t,r-a,t),(x+w-r,y+t,r-a,t),(x+a,y+h-2*t,r-a,t),(x+w-r,y+h-2*t,r-a,t),(x+t,y+a,t,r-a),(x+w-2*t,y+a,t,r-a),(x+t,y+h-r,t,r-a),(x+w-2*t,y+h-r,t,r-a))
def rbox(x,y,w,h,r,c,t=2,inner=BLACK,fill=True):
 edge(x,y,w,h,r,c,t)
 if not fill:
  return
 col(inner)
 if r<=t:
  fr(x+t,y+t,w-2*t,h-2*t)
  return
 a=min(r//2,2*t)
 fr(x+t,y+r,w-2*t,h-2*r)
 fr(x+r,y+t,w-2*r,t)
 fr(x+r,y+h-2*t,w-2*r,t)
 if r>2*t:
  fr(x+a,y+2*t,w-2*a,r-2*t)
  fr(x+a,y+h-r,w-2*a,r-2*t)
def edge(x,y,w,h,r,c,t=2,inner=BLACK):
 col(c)
 for bx,by,bw,bh in _corners(x,y,w,h,r,t):
  if bw>0 and bh>0:
   fr(bx,by,bw,bh)
def pause(s):
 time.sleep(s)
def _wrap(s,n=30):
 out=[]
 line=''
 for w in s.split(' '):
  if len(line)+len(w)+1>n:
   out.append(line)
   line=w
  else:
   line=(line+' '+w).strip()
 if line:
  out.append(line)
 return out
def how_to(title,rules,buttons):
 cls()
 ctext(20,'HOW TO PLAY',GOLD)
 ctext(38,title,GREY)
 y=60
 for ln in _wrap(rules):
  text(8,y,ln)
  y+=16
 y+=6
 text(8,y,'BUTTONS',GOLD)
 y+=17
 for b in buttons:
  text(8,y,b)
  y+=16
 text(8,206,'ENTER: back',GREY)
 while wkey()not in(OK,CLR,UP,DOWN):
  pass
def home(mod,title,rules,buttons,opts=('Play','Back'),sel=0):
 n=len(opts)
 while True:
  cls()
  ring(160,58,36,GOLD,3)
  try:
   circ(160,58,33,I_bg(mod))
   I_draw(mod,160,58,WHITE)
  except Exception:
   pass
  ctext(122,title,GOLD)
  ctext(146,'Up/Down: how to play',GREY)
  bw=(300-(n-1)*8)//n
  first=True
  old=-1
  while True:
   for i in range(n):
    if not first and i!=sel and(i!=old):
     continue
    x=10+i*(bw+8)
    c=GOLD if i==sel else WHITE
    if first:
     rbox(x,166,bw,28,10,c,2,BLACK,False)
    else:
     edge(x,166,bw,28,10,c)
    text(x+bw//2-len(opts[i])*5,186,opts[i],c)
   first=False
   old=sel
   k=wkey()
   if k==LEFT:
    sel=(sel-1)%n
   elif k==RIGHT:
    sel=(sel+1)%n
   elif k in(UP,DOWN):
    how_to(title,rules,buttons)
    break
   elif k==CLR:
    return-1
   elif k==OK:
    if opts[sel]=='Back':
     return-1
    return sel
I_BLACK=(0,0,0)
I_GOLD=(230,180,40)
I_BG={'GHFORTUN':(55,25,85)}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_poly(xs,ys,c):
 I_c_(c)
 fill_poly([int(v)for v in xs],[int(v)for v in ys])
def I_fortune(x,y,c):
 I_box(x-19,y-10,13,20,(120,40,140))
 I_box(x+6,y-10,13,20,(120,40,140))
 I_box(x-8,y-15,16,25,(250,240,215))
 I_poly([x,x+2,x+6,x+3,x+4,x,x-4,x-3,x-6,x-2],[y-9,y-4,y-4,y-1,y+4,y+1,y+4,y-1,y-4,y-4],I_GOLD)
I_ICONS={'GHFORTUN':I_fortune}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_TABLE=(55,25,85)
G_BACKC=(120,40,140)
G_FACE=(250,240,215)
G_INK=(40,30,50)
G_CW=36
G_CH=54
G_DECK=(('The Star','star','You made a wish that mattered.','Hope is shining on you.','A wish will come true.'),('The Moon','moon','You found a way in the dark.','Trust your dreams tonight.','A secret will be revealed.'),('The Sun','sun','You had a really good day.','You bring warmth to others.','Happy days are coming.'),('The Key','key','You unlocked something new.','An answer is close by.','A door will open for you.'),('The Cat','cat','You were braver than you knew.','Be curious and look around.','You will land on your feet.'),('The Bridge','bridge','You made a new friend.','Reach out to someone.','Two paths will meet.'),('The Lantern','lantern','Someone helped you see.','You are a light for a friend.','You will find what was lost.'),('The Crown','crown','You were proud of yourself.','Lead the way, others follow.','You will win something.'),('The Wave','wave','A big change washed over you.','Go with the flow today.','An adventure is on its way.'),('The Mountain','mountain','You climbed a hard hill.','Keep going, you are close.','You will reach the top.'),('The Bird','bird','You heard some good news.','Say what is on your mind.','A message will reach you.'),('The Clock','clock','You waited for something.','Now is the right time.','Good things take time.'),('The Tree','tree','You grew a lot this year.','Stay strong and steady.','Something you plant will grow.'),('The Heart','heart','Someone was kind to you.','You are loved more than you know.','A friendship will get closer.'),('The Ship','ship','You left something behind.',"Set your sails, it's time.",'A trip is in your future.'),('The Flame','flame','You stood up for yourself.','Your spark is bright today.','You will find a new passion.'),('The Rainbow','rainbow','A storm finally ended.','Look for the bright side.','A happy surprise is coming.'),('The Book','book','You learned a big lesson.','Ask, and you will find out.','You will discover a talent.'),('The Owl','owl','You noticed what others missed.','Listen more than you speak.','A wise choice will pay off.'),('The Feather','feather','You let go of a worry.','Take it easy today.','Things will feel lighter soon.'))
G_TIMES=('PAST','NOW','FUTURE')
def G_art(kind,x,y,s=1):
 def r(a,b,w,h,c):
  rect(x+a*s,y+b*s,w*s,h*s,c)
 if kind=='star':
  col(GOLD)
  fill_poly([x,x+3*s,x+10*s,x+4*s,x+6*s,x,x-6*s,x-4*s,x-10*s,x-3*s],[y-10*s,y-3*s,y-3*s,y+2*s,y+9*s,y+5*s,y+9*s,y+2*s,y-3*s,y-3*s])
 elif kind=='moon':
  circ(x,y,9*s,(230,225,170))
  circ(x+4*s,y-2*s,8*s,G_FACE)
 elif kind=='sun':
  r(-11,-1,22,2,(250,170,30))
  r(-1,-11,2,22,(250,170,30))
  circ(x,y,6*s,(250,200,40))
 elif kind=='key':
  circ(x-5*s,y,5*s,GOLD)
  r(-1,-1,12,3,GOLD)
  r(7,2,2,4,GOLD)
  circ(x-5*s,y,2*s,G_FACE)
 elif kind=='cat':
  col(G_INK)
  fill_poly([x-7*s,x-7*s,x-2*s],[y-4*s,y-11*s,y-6*s])
  fill_poly([x+7*s,x+7*s,x+2*s],[y-4*s,y-11*s,y-6*s])
  circ(x,y,7*s,G_INK)
  r(-4,-2,2,2,(120,220,90))
  r(2,-2,2,2,(120,220,90))
 elif kind=='bridge':
  r(-12,-2,24,3,(140,90,50))
  r(-10,1,3,8,(140,90,50))
  r(7,1,3,8,(140,90,50))
  r(-12,6,24,4,(80,140,220))
 elif kind=='lantern':
  r(-5,-6,10,13,(250,210,80))
  r(-6,-8,12,2,G_INK)
  r(-6,7,12,2,G_INK)
  r(-2,-11,4,3,G_INK)
 elif kind=='crown':
  col(GOLD)
  fill_poly([x-10*s,x-10*s,x-5*s,x,x+5*s,x+10*s,x+10*s],[y+6*s,y-6*s,y,y-8*s,y,y-6*s,y+6*s])
  r(-2,1,4,3,RED)
 elif kind=='wave':
  circ(x-4*s,y+2*s,7*s,(60,130,220))
  circ(x+6*s,y+4*s,5*s,(60,130,220))
  r(-12,6,24,4,(60,130,220))
 elif kind=='mountain':
  col((110,110,130))
  fill_poly([x-12*s,x,x+12*s],[y+9*s,y-10*s,y+9*s])
  col(WHITE)
  fill_poly([x-4*s,x,x+4*s],[y-4*s,y-10*s,y-4*s])
 elif kind=='bird':
  circ(x,y,6*s,(230,90,70))
  col((230,90,70))
  fill_poly([x-3*s,x-13*s,x-2*s],[y-2*s,y-8*s,y+3*s])
  col(GOLD)
  fill_poly([x+5*s,x+10*s,x+5*s],[y-2*s,y,y+2*s])
  r(1,-3,2,2,G_INK)
 elif kind=='tree':
  r(-2,2,4,9,(130,80,40))
  circ(x,y-3*s,8*s,(60,150,70))
 elif kind=='heart':
  circ(x-4*s,y-3*s,5*s,RED)
  circ(x+4*s,y-3*s,5*s,RED)
  col(RED)
  fill_poly([x-9*s,x+9*s,x],[y-1*s,y-1*s,y+9*s])
 elif kind=='ship':
  col((80,140,220))
  fill_poly([x-1*s,x-1*s,x-9*s],[y-11*s,y+2*s,y+2*s])
  fill_poly([x+1*s,x+1*s,x+8*s],[y-8*s,y+2*s,y+2*s])
  col((140,90,50))
  fill_poly([x-11*s,x+11*s,x+7*s,x-7*s],[y+4*s,y+4*s,y+9*s,y+9*s])
 elif kind=='flame':
  col((240,110,30))
  fill_poly([x,x+7*s,x+6*s,x-6*s,x-7*s],[y-11*s,y,y+8*s,y+8*s,y])
  col((250,210,60))
  fill_poly([x,x+4*s,x+3*s,x-3*s,x-4*s],[y-4*s,y+3*s,y+8*s,y+8*s,y+3*s])
 elif kind=='rainbow':
  for i,c in enumerate(((220,50,50),(245,150,30),(240,210,50),(70,170,80),(60,120,220))):
   circ(x,y+5*s,(12-2*i)*s,c)
  circ(x,y+5*s,2*s,G_FACE)
  r(-13,5,27,13,G_FACE)
 elif kind=='book':
  r(-11,-7,22,15,(60,90,170))
  r(-10,-6,9,13,WHITE)
  r(1,-6,9,13,WHITE)
  r(-8,-3,5,1,GREY)
  r(3,-3,5,1,GREY)
  r(-8,0,5,1,GREY)
  r(3,0,5,1,GREY)
 elif kind=='owl':
  circ(x,y+1*s,9*s,(140,95,60))
  circ(x-4*s,y-1*s,3*s,WHITE)
  circ(x+4*s,y-1*s,3*s,WHITE)
  r(-5,-2,2,2,G_INK)
  r(3,-2,2,2,G_INK)
  col(GOLD)
  fill_poly([x-2*s,x+2*s,x],[y+2*s,y+2*s,y+5*s])
 elif kind=='feather':
  col((90,170,160))
  fill_poly([x+8*s,x+4*s,x-6*s,x-9*s,x-3*s],[y-10*s,y-2*s,y+7*s,y+9*s,y-2*s])
  r(-8,6,2,4,G_INK)
 elif kind=='clock':
  circ(x,y,9*s,G_INK)
  circ(x,y,7*s,WHITE)
  r(-1,-6,2,7,G_INK)
  r(0,-1,5,2,G_INK)
def G_back(x,y):
 rect(x,y,G_CW,G_CH,G_BACKC)
 rect(x+G_CW//2-3,y+G_CH//2-3,6,6,GOLD)
def G_face(x,y,i):
 rect(x,y,G_CW,G_CH,G_FACE)
 G_art(G_DECK[i][1],x+G_CW//2,y+G_CH//2)
def G_frame(x,y,c):
 rect(x-3,y-3,G_CW+6,2,c)
 rect(x-3,y+G_CH+1,G_CW+6,2,c)
 rect(x-3,y-1,2,G_CH+2,c)
 rect(x+G_CW+1,y-1,2,G_CH+2,c)
def G_spot(i):
 return(14+i*42,40)
def G_reading():
 deck=list(range(len(G_DECK)))
 shuffle(deck)
 row=deck[:7]
 nxt=7
 cards=[]
 cls(G_TABLE)
 ctext(22,'Pick 3 cards',GOLD)
 for i in range(7):
  G_back(G_spot(i)[0],G_spot(i)[1])
 for t in range(3):
  x=50+t*90
  rect(x,120,G_CW+20,G_CH+20,dk(G_TABLE,0.8))
  text(x+28-len(G_TIMES[t])*5,208,G_TIMES[t],GREY)
 sel=0
 G_frame(G_spot(sel)[0],G_spot(sel)[1],GOLD)
 while len(cards)<3:
  k=wkey()
  old=sel
  if k==CLR:
   return False
  if k in(LEFT,RIGHT):
   sel=(sel+(1 if k==RIGHT else-1))%7
  elif k==OK:
   x=50+len(cards)*90+10
   cards.append(row[sel])
   rect(G_spot(sel)[0],G_spot(sel)[1],G_CW,G_CH,G_TABLE)
   G_face(x,130,row[sel])
   if len(cards)<3:
    row[sel]=deck[nxt]
    nxt+=1
    pause(0.25)
    G_back(G_spot(sel)[0],G_spot(sel)[1])
   continue
  if sel!=old:
   G_frame(G_spot(old)[0],G_spot(old)[1],G_TABLE)
   G_frame(G_spot(sel)[0],G_spot(sel)[1],GOLD)
 for t in range(3):
  name,kind=(G_DECK[cards[t]][0],G_DECK[cards[t]][1])
  cls(G_TABLE)
  ctext(20,G_TIMES[t],GREY)
  rect(124,34,72,92,G_FACE)
  G_art(kind,160,80,2)
  ctext(148,name,GOLD)
  ctext(172,G_DECK[cards[t]][2+t])
  ctext(206,'ENTER: next'if t<2 else 'ENTER: done',GREY)
  if wkey()==CLR:
   return False
 cls(G_TABLE)
 ctext(26,'YOUR FORTUNE',GOLD)
 y=60
 for t in range(3):
  text(10,y,G_TIMES[t],GREY)
  y+=18
  text(10,y,G_DECK[cards[t]][2+t])
  y+=26
 ctext(206,'ENTER: new reading  CLEAR: stop',GREY)
 return wkey()!=CLR
def G_game():
 while G_reading():
  pass
G_RULES='Shuffle the deck, pick three cards and find out what they say about your past, your present and your future. Just for fun!'
G_KEYS=['Left/Right: choose a card','ENTER: pick it / next','CLEAR: stop']
def G_main():
 while True:
  c=home('GHFORTUN','FORTUNE CARDS',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
