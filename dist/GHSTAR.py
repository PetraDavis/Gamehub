# GHSTAR from GAMEHUB, on its own. Run it.
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
H=210
def key():
 return get_key(0)
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
I_BG={'GHSTAR':(8,10,32)}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_star(x,y,c):
 I_box(x-7,y-15,14,9,(120,230,90))
 I_box(x-7,y-15,3,3,(8,10,32))
 I_box(x+4,y-15,3,3,(8,10,32))
 I_box(x-4,y-11,8,2,(8,10,32))
 I_box(x-1,y-3,2,6,(255,230,90))
 I_box(x-10,y+7,20,10,(90,200,255))
 I_box(x-10,y+7,7,4,(8,10,32))
 I_box(x+3,y+7,7,4,(8,10,32))
I_ICONS={'GHSTAR':I_star}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
try:
 from time import monotonic as G_now
except Exception:
 G_now=None
G_BG=(8,10,32)
G_SHIP=(90,200,255)
G_ALIEN=(120,230,90)
G_SHOT=(255,230,90)
G_TOP=24
G_SY=190
G_SW,G_SH=(20,12)
G_AW,G_AH=(16,10)
G_MAXA=3
G_FIRE=0.35
G_SHOT_V=260.0
G_STEP=16
def G_ship_cuts(x):
 return((x,G_SY,7,5),(x+13,G_SY,7,5))
def G_alien_cuts(x,y):
 return((x,y,4,3),(x+12,y,4,3),(x+3,y+4,10,2),(x+5,y+8,6,2))
def G_paint(groups):
 for c,rs in groups:
  if rs:
   col(c)
   for x,y,w,h in rs:
    if w>0 and h>0:
     fr(x,y,w,h)
def G_strip(ox,oy,nx,ny,w,h,out):
 if abs(nx-ox)>=w or abs(ny-oy)>=h:
  out.append((ox,oy,w,h))
  return
 if ny>oy:
  out.append((ox,oy,w,ny-oy))
 elif ny<oy:
  out.append((ox,ny+h,w,oy-ny))
 y0=max(oy,ny)
 y1=min(oy,ny)+h
 if nx>ox:
  out.append((ox,y0,nx-ox,y1-y0))
 elif nx<ox:
  out.append((nx+w,y0,ox-nx,y1-y0))
G_HUD=[None,None]
def G_hud(score,lives):
 if G_HUD[0]is None:
  text(6,17,'Score')
  text(230,17,'Lives',GOLD)
 if score!=G_HUD[0]:
  if G_HUD[0]is not None:
   text(66,17,str(G_HUD[0]),G_BG)
  text(66,17,str(score))
 if lives!=G_HUD[1]:
  if G_HUD[1]is not None:
   text(290,17,str(G_HUD[1]),G_BG)
  text(290,17,str(lives),GOLD)
 G_HUD[0],G_HUD[1]=(score,lives)
def G_new_alien(aliens):
 for i in range(8):
  x=random.randint(4,316-G_AW)
  if all((abs(x-a[0])>G_AW+4 or a[1]>G_TOP+30 for a in aliens)):
   return[float(x),float(G_TOP+2),int(x),G_TOP+2]
 return None
def G_game():
 cls(G_BG)
 rect(0,22,320,2,(60,70,120))
 for x,y in((2,40),(314,70),(2,120),(314,160),(2,180)):
  rect(x,y,2,2,(200,200,230))
 G_HUD[0]=G_HUD[1]=None
 score=0
 lives=3
 G_hud(score,lives)
 sx=150.0
 shown_x=None
 aliens=[]
 shots=[]
 wait=1.0
 reload=0.0
 last=G_now()if G_now else 0
 while lives>0:
  k=key()
  if k==CLR:
   if message(['ENTER: quit','CLEAR: keep playing'],'Quit?')==OK:
    return
   cls(G_BG)
   rect(0,22,320,2,(60,70,120))
   G_HUD[0]=G_HUD[1]=None
   G_hud(score,lives)
   shown_x=None
   for a in aliens:
    a[3]=-100
   for s in shots:
    s[2]=-100
   last=G_now()if G_now else 0
   continue
  if G_now:
   t=G_now()
   dt=min(0.25,max(0.01,t-last))
   last=t
  else:
   dt=0.15
  if k==LEFT:
   sx-=G_STEP
  elif k==RIGHT:
   sx+=G_STEP
  sx=max(4.0,min(316.0-G_SW,sx))
  speed=min(80.0,22.0+score*1.5)
  wait-=dt
  if wait<=0 and len(aliens)<G_MAXA:
   a=G_new_alien(aliens)
   if a:
    aliens.append(a)
   wait=max(0.6,2.2-score*0.05)
  reload-=dt
  if reload<=0 and len(shots)<3:
   shots.append([sx+G_SW/2-1,float(G_SY-6),None])
   reload=G_FIRE
  green,blue,gold,back=([],[],[],[])
  for s in shots[:]:
   oy=s[1]
   s[1]-=G_SHOT_V*dt
   hit=None
   for a in aliens:
    if a[0]-1<=s[0]<=a[0]+G_AW and s[1]<=a[1]+G_AH and(oy+6>=a[1]):
     hit=a
   if hit or s[1]<G_TOP+2:
    if s[2]is not None and s[2]>=0:
     back.append((int(s[0]),s[2],2,6))
    shots.remove(s)
    if hit:
     aliens.remove(hit)
     if hit[3]>=0:
      back.append((hit[2],hit[3],G_AW,G_AH))
     score+=1
     G_hud(score,lives)
    continue
   ny=int(s[1])
   if s[2]is None or s[2]<0:
    gold.append((int(s[0]),ny,2,6))
   else:
    G_strip(int(s[0]),s[2],int(s[0]),ny,2,6,back)
    gold.append((int(s[0]),ny,2,6))
   s[2]=ny
  for a in aliens[:]:
   a[1]+=speed*dt
   nx,ny=(int(a[0]),int(a[1]))
   if ny+G_AH>=G_SY+G_SH:
    aliens.remove(a)
    if a[3]>=0:
     back.append((a[2],a[3],G_AW,G_AH))
    lives-=1
    G_hud(score,lives)
    continue
   if ny!=a[3]:
    if a[3]>=0:
     G_strip(a[2],a[3],nx,ny,G_AW,G_AH,back)
    green.append((nx,ny,G_AW,G_AH))
    back.extend(G_alien_cuts(nx,ny))
    a[2],a[3]=(nx,ny)
   if ny+G_AH>G_SY and nx<sx+G_SW and(nx+G_AW>sx):
    aliens.remove(a)
    back.append((nx,ny,G_AW,G_AH))
    lives-=1
    G_hud(score,lives)
  ix=int(sx)
  if ix!=shown_x:
   if shown_x is not None:
    G_strip(shown_x,G_SY,ix,G_SY,G_SW,G_SH,back)
   blue.append((ix,G_SY,G_SW,G_SH))
   back.extend(G_ship_cuts(ix))
   shown_x=ix
  G_paint(((G_ALIEN,green),(G_SHIP,blue),(G_SHOT,gold),(G_BG,back)))
 pause(0.4)
 message(['You stopped '+str(score)+' aliens.'],'Game over')
G_RULES='Aliens are drifting down toward the planet. Your ship fires by itself: move under them and stop them before they reach the bottom. 3 lives.'
G_KEYS=['Left/Right: move a step','CLEAR: quit']
def G_main():
 while True:
  c=home('GHSTAR','STAR PATROL',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
