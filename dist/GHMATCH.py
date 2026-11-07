# GHMATCH from GAMEHUB, on its own. Run it.
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
SECOND=21
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
GREY=(110,110,110)
RED=(220,50,50)
H=210
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
def lt(c,k=0.35):
 return(int(c[0]+(255-c[0])*k),int(c[1]+(255-c[1])*k),int(c[2]+(255-c[2])*k))
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
MSG=[0,0]
def message(lines,title=None):
 n=len(lines)+(1 if title else 0)
 h=n*18+30
 y=(H-h)//2
 rbox(20,y,280,h,8,WHITE)
 MSG[0],MSG[1]=(y,h)
 COVER[0]+=1
 yy=y+24
 if title:
  ctext(yy,title,GOLD)
  yy+=18
 for s in lines:
  ctext(yy,s)
  yy+=18
 while True:
  k=wkey()
  if k in(OK,CLR):
   return k
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
I_RED=(215,40,40)
I_BG={'GHMATCH':(30,90,80)}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_circ(x,y,r,c):
 I_c_(c)
 fill_circle(int(x),int(y),int(r))
def I_poly(xs,ys,c):
 I_c_(c)
 fill_poly([int(v)for v in xs],[int(v)for v in ys])
def I_match(x,y,c):
 I_box(x-19,y-12,17,24,(200,70,90))
 I_box(x-15,y-8,9,16,(225,120,135))
 I_box(x+2,y-12,17,24,(250,245,230))
 I_circ(x+8,y-2,3,I_RED)
 I_circ(x+13,y-2,3,I_RED)
 I_poly([x+4,x+17,x+10],[y-1,y-1,y+6],I_RED)
I_ICONS={'GHMATCH':I_match}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_TABLE=(30,90,80)
G_BACKC=(200,70,90)
G_FACE=(250,245,230)
G_CW,G_CH=(50,38)
G_X0,G_Y0=(37,30)
G_DX,G_DY=(64,45)
G_SYMS=('heart','star','moon','sun','drop','leaf','gem','bolt')
def G_pos(i):
 return(G_X0+i%4*G_DX,G_Y0+i//4*G_DY)
def G_back(i):
 x,y=G_pos(i)
 rect(x,y,G_CW,G_CH,G_BACKC)
 rect(x+5,y+5,G_CW-10,G_CH-10,lt(G_BACKC,0.25))
 rect(x+8,y+8,G_CW-16,G_CH-16,G_BACKC)
def G_pic(kind,x,y):
 if kind=='heart':
  circ(x-4,y-3,5,RED)
  circ(x+4,y-3,5,RED)
  fill_poly([x-9,x+9,x],[y-1,y-1,y+9])
 elif kind=='star':
  col(GOLD)
  fill_poly([x,x+3,x+10,x+4,x+6,x,x-6,x-4,x-10,x-3],[y-10,y-3,y-3,y+2,y+9,y+5,y+9,y+2,y-3,y-3])
 elif kind=='moon':
  circ(x,y,9,(120,110,200))
  circ(x+4,y-2,8,G_FACE)
 elif kind=='sun':
  rect(x-11,y-1,22,2,(245,150,30))
  rect(x-1,y-11,2,22,(245,150,30))
  circ(x,y,6,(245,190,40))
 elif kind=='drop':
  circ(x,y+3,6,(60,130,220))
  fill_poly([x-6,x+6,x],[y+2,y+2,y-10])
 elif kind=='leaf':
  col((60,160,70))
  fill_poly([x-9,x-2,x+9,x+2],[y+8,y-6,y-9,y+5])
  rect(x-10,y+7,3,3,(60,160,70))
 elif kind=='gem':
  col((170,80,210))
  fill_poly([x-9,x-5,x+5,x+9,x],[y-3,y-8,y-8,y-3,y+9])
  rect(x-5,y-5,10,2,lt((170,80,210),0.4))
 elif kind=='bolt':
  col((40,40,50))
  fill_poly([x+2,x-7,x-1,x-4,x+7,x+1],[y-10,y+1,y+1,y+10,y-2,y-2])
def G_face(i,kind):
 x,y=G_pos(i)
 rect(x,y,G_CW,G_CH,G_FACE)
 G_pic(kind,x+G_CW//2,y+G_CH//2)
def G_frame(i,c):
 x,y=G_pos(i)
 rect(x-3,y-3,G_CW+6,2,c)
 rect(x-3,y+G_CH+1,G_CW+6,2,c)
 rect(x-3,y-1,2,G_CH+2,c)
 rect(x+G_CW+1,y-1,2,G_CH+2,c)
G_HUD=[None]
def G_hud(tries):
 if G_HUD[0]is None:
  text(6,17,'Tries',GOLD)
 else:
  text(66,17,str(G_HUD[0]),G_TABLE)
 text(66,17,str(tries))
 G_HUD[0]=tries
def G_game():
 cards=list(G_SYMS)*2
 shuffle(cards)
 up=[False]*16
 cls(G_TABLE)
 text(190,17,'Pairs 0/8',WHITE)
 G_HUD[0]=None
 G_hud(0)
 for i in range(16):
  G_back(i)
 tries=0
 pairs=0
 sel=0
 first=-1
 G_frame(sel,GOLD)
 while pairs<8:
  k=wkey()
  old=sel
  if k==CLR:
   if message(['ENTER: quit this game','CLEAR: keep playing'],'Quit?')==OK:
    return
   cls(G_TABLE)
   G_HUD[0]=None
   G_hud(tries)
   text(190,17,'Pairs '+str(pairs)+'/8',WHITE)
   for i in range(16):
    if up[i]or i==first:
     G_face(i,cards[i])
    else:
     G_back(i)
   G_frame(sel,GOLD)
   continue
  if k==LEFT:
   sel=sel-1 if sel%4 else sel+3
  elif k==RIGHT:
   sel=sel+1 if sel%4<3 else sel-3
  elif k==UP:
   sel=(sel-4)%16
  elif k==DOWN:
   sel=(sel+4)%16
  elif k in(OK,SECOND)and(not up[sel])and(sel!=first):
   G_face(sel,cards[sel])
   if first<0:
    first=sel
    continue
   tries+=1
   G_hud(tries)
   if cards[first]==cards[sel]:
    up[first]=up[sel]=True
    pairs+=1
    text(190,17,'Pairs '+str(pairs-1)+'/8',G_TABLE)
    text(190,17,'Pairs '+str(pairs)+'/8',WHITE)
   else:
    pause(0.9)
    G_back(first)
    G_back(sel)
   first=-1
   continue
  if sel!=old:
   G_frame(old,G_TABLE)
   G_frame(sel,GOLD)
 pause(0.5)
 message(['You found all 8 pairs','in '+str(tries)+' tries.'],'Well done!')
G_RULES='Turn over two cards. If the pictures match, they stay face up. Find all 8 pairs in as few tries as you can.'
G_KEYS=['Arrows: move','ENTER: turn a card over','CLEAR: quit']
def G_main():
 while True:
  c=home('GHMATCH','MEMORY MATCH',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
