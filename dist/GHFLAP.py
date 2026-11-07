# GHFLAP from GAMEHUB, on its own. Run it.
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
I_WHITE=(255,255,255)
I_BG={'GHFLAP':(110,195,240)}
def I_c_(c):
 set_color(c[0],c[1],c[2])
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_circ(x,y,r,c):
 I_c_(c)
 fill_circle(int(x),int(y),int(r))
def I_poly(xs,ys,c):
 I_c_(c)
 fill_poly([int(v)for v in xs],[int(v)for v in ys])
def I_ground(x,y,top,c,r=24):
 a=math.asin(top/r)
 xs=[]
 ys=[]
 for i in range(13):
  t=a+(math.pi-2*a)*i/12
  xs.append(x+r*math.cos(t))
  ys.append(y+r*math.sin(t))
 I_poly(xs,ys,c)
def I_flap(x,y,c):
 I_box(x-14,y-16,10,4,I_WHITE)
 I_circ(x-12,y-15,3,I_WHITE)
 I_circ(x-7,y-17,4,I_WHITE)
 I_ground(x,y,15,(70,170,80))
 I_box(x+14,y+4,4,12,(120,80,40))
 I_circ(x+16,y+1,6,(50,140,60))
 I_circ(x-2,y-1,11,(170,120,20))
 I_circ(x-2,y-1,10,(250,215,50))
 I_poly([x-14,x-2,x-6],[y-1,y+1,y+8],(255,245,190))
 I_circ(x+3,y-5,4,I_WHITE)
 I_circ(x+4,y-5,2,I_BLACK)
 I_poly([x+7,x+17,x+7],[y-2,y+1,y+2],(245,140,30))
 I_poly([x+7,x+15,x+7],[y+2,y+3,y+5],(200,100,20))
I_ICONS={'GHFLAP':I_flap}
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
G_GAP=64
G_NP=15
G_TW=G_NP*2
G_TOP=22
G_GND=196
G_BX=60
G_BR=7
G_SKY=(110,195,240)
G_LEAF=(50,140,60)
G_INK=(20,20,20)
G_BODY=(240,200,40)
G_BEAK=(245,140,30)
G_GRAV=900.0
G_FLAP=-265.0
G_FALL=430.0
G_SPEED=80.0
def G_column(gy):
 return[(G_TOP,gy,G_LEAF),(gy,gy+G_GAP,G_SKY),(gy+G_GAP,G_GND,G_LEAF)]
G_SKYCOL=[(G_TOP,G_GND,G_SKY)]
def G_bg(p,trees):
 for t in trees:
  if 0<=p-t[0]//2<G_NP:
   return t[2]
 return G_SKYCOL
def G_diff(old,new):
 cuts=sorted(set([a for a,b,c in old]+[b for a,b,c in old]+[a for a,b,c in new]+[b for a,b,c in new]))
 out=[]
 for i in range(len(cuts)-1):
  a,b=(cuts[i],cuts[i+1])
  if b<=a:
   continue
  m=(a+b)//2
  co=cn=None
  for y0,y1,c in old:
   if y0<=m<y1:
    co=c
  for y0,y1,c in new:
   if y0<=m<y1:
    cn=c
  if cn is not None and co!=cn:
   if out and out[-1][1]==a and(out[-1][2]==cn):
    out[-1]=(out[-1][0],b,cn)
   else:
    out.append((a,b,cn))
 return out
def G_spans(cols,out):
 run={}
 for p,sp in cols:
  keep={}
  for s in sp:
   if s in run and run[s][1]==p:
    keep[s]=(run[s][0],p+1)
   else:
    keep[s]=(p,p+1)
  for s in run:
   if s not in keep or keep[s][0]!=run[s][0]:
    G__span(s,run[s],out)
  run=keep
 for s in run:
  G__span(s,run[s],out)
def G__span(s,r,out):
 y0,y1,c=s
 if y1>y0:
  out.append((c,r[0]*2,y0,(r[1]-r[0])*2,y1-y0))
def G_clip(sp,a,b):
 out=[]
 for y0,y1,c in sp:
  y0=max(y0,a)
  y1=min(y1,b)
  if y1>y0:
   out.append((y0,y1,c))
 return out
def G_batch(todo):
 todo.sort()
 for c,x,y,w,h in todo:
  rect(x,y,w,h,c)
def G_bird(y):
 rect(G_BX-7,y-6,14,12,G_BODY)
 rect(G_BX+7,y-1,5,4,G_BEAK)
 rect(G_BX+2,y-3,3,3,G_INK)
def G_ground():
 rect(0,196,320,5,(70,170,80))
 rect(0,201,320,9,(120,80,40))
 for x in range(0,320,20):
  rect(x+6,204,4,2,(95,60,30))
def G_crashed(y,trees):
 if y+7>=G_GND:
  return True
 for p in range((G_BX-G_BR)//2,(G_BX+G_BR)//2+1):
  for y0,y1,c in G_bg(p,trees):
   if c==G_SKY:
    continue
   dx=abs(p*2+1-G_BX)
   if dx>G_BR:
    continue
   dy=int((G_BR*G_BR-dx*dx)**0.5)
   if y0<y+dy and y-dy<y1:
    return True
 return False
def G_new_tree(x):
 gy=random.randint(20,55)*2
 return[x,gy,G_column(gy)]
def G_game():
 cls(G_SKY)
 G_ground()
 rect(0,20,320,2,G_INK)
 text(6,17,'Score',G_INK)
 text(66,17,'0',G_INK)
 trees=[G_new_tree(332),G_new_tree(332+172)]
 shown=[G_SKYCOL]*160
 y=100.0
 v=0.0
 score=0
 passed=[False,False]
 go=0.0
 oy=int(y)
 G_bird(oy)
 pause(0.4)
 last=G_now()if G_now else 0
 while True:
  k=key()
  if k==CLR:
   return
  if G_now:
   t=G_now()
   dt=min(0.12,max(0.03,t-last))
   last=t
  else:
   dt=0.05
  if k in(UP,SECOND,OK):
   v=G_FLAP
  v=min(G_FALL,v+G_GRAV*dt)
  y+=v*dt
  if y<G_TOP+7:
   y=G_TOP+7.0
   v=0.0
  go+=G_SPEED*dt
  step=int(go/4)*4
  go-=step
  lo,hi=(160,0)
  for i in range(2):
   t=trees[i]
   a=t[0]//2
   t[0]-=step
   if t[0]+G_TW<0:
    trees[i]=t=G_new_tree(max(332,trees[1-i][0]+172))
    passed[i]=False
   for p in(a,t[0]//2):
    lo=min(lo,max(0,p))
    hi=max(hi,min(160,p+G_NP))
   if not passed[i]and t[0]+G_TW<G_BX-G_BR:
    passed[i]=True
    text(66,17,str(score),G_SKY)
    score+=1
    text(66,17,str(score),G_INK)
  work=[]
  hit=False
  for p in range(lo,hi):
   n=G_bg(p,trees)
   if n is not shown[p]:
    d=G_diff(shown[p],n)
    if d:
     work.append((p,d))
     if G_BX-8<=p*2<=G_BX+12:
      hit=True
    shown[p]=n
  todo=[]
  G_spans(work,todo)
  ny=int(y)
  if ny!=oy:
   a,b=(oy-6,ny-6)if ny>oy else(ny+6,oy+6)
   G_spans([(p,G_clip(shown[p],a,b))for p in range((G_BX-8)//2,(G_BX+13)//2)],todo)
  G_batch(todo)
  if ny!=oy or hit:
   G_bird(ny)
  oy=ny
  if G_crashed(y,trees):
   pause(0.4)
   message(['You passed '+str(score)+' trees.'],'Crash!')
   return
  pause(0.01)
G_RULES="Flap to fly through the gaps between the trees. Don't hit the trees or the ground."
G_KEYS=['Up, 2nd or ENTER: flap','CLEAR: quit']
def G_main():
 while True:
  c=home('GHFLAP','WING IT',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
