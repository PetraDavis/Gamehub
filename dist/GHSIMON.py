# GHSIMON from GAMEHUB, on its own. Run it.
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
def home(mod,title,rules,buttons,opts=('Play','Back'),sel=0,wipe=None):
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
    if opts[sel]=='Delete':
     wipe()
     break
    return sel
I_BLACK=(0,0,0)
I_BG={}
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
def I_simon(x,y,c):
 r=18
 cols=((40,170,60),(200,40,40),(40,80,200),(220,180,30))
 for q in range(4):
  a0=-math.pi/2+q*math.pi/2
  xs=[x]
  ys=[y]
  for i in range(6):
   a=a0+math.pi/2*i/5
   xs.append(x+r*math.cos(a))
   ys.append(y+r*math.sin(a))
  I_poly(xs,ys,cols[q])
 I_circ(x,y,5,I_BLACK)
 I_box(x-1,y-r,2,2*r,I_BLACK)
 I_box(x-r,y-1,2*r,2,I_BLACK)
I_ICONS={'GHSIMON':I_simon}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_CX=160
G_CY=116
G_RO=84
G_RI=36
G_PADS=((UP,2,(30,130,50),(110,255,130)),(RIGHT,3,(150,30,30),(255,110,110)),(DOWN,0,(30,60,150),(120,170,255)),(LEFT,1,(160,130,20),(255,235,100)))
G_SHAPE=[]
def G_shapes():
 for q in range(4):
  xs=[]
  ys=[]
  for r,order in((G_RO,range(9)),(G_RI+3,range(8,-1,-1))):
   for i in order:
    a=math.pi/2*(q+i/8)
    dx=r*math.cos(a)
    dy=r*math.sin(a)
    xs.append(int(G_CX+(max(dx,4)if q in(0,3)else min(dx,-5))))
    ys.append(int(G_CY+(max(dy,4)if q in(0,1)else min(dy,-5))))
  G_SHAPE.append((xs,ys))
def G_gaps():
 d=(15,15,15)
 rect(G_CX-4,G_CY-G_RO-1,8,G_RO-G_RI+1,d)
 rect(G_CX-4,G_CY+G_RI,8,G_RO-G_RI+1,d)
 rect(G_CX-G_RO-1,G_CY-4,G_RO-G_RI+1,8,d)
 rect(G_CX+G_RI,G_CY-4,G_RO-G_RI+1,8,d)
 col(d)
 for r in(G_RI,G_RI+1,G_RI+2):
  draw_circle(G_CX,G_CY,r)
def G_pad(i,lit):
 k,q,dim,bright=G_PADS[i]
 col(bright if lit else dim)
 xs,ys=G_SHAPE[q]
 fill_poly(xs,ys)
def G_body():
 if not G_SHAPE:
  G_shapes()
 circ(G_CX,G_CY,G_RO+8,(60,60,65))
 circ(G_CX,G_CY,G_RO+5,(15,15,15))
 for i in range(4):
  G_pad(i,False)
 G_gaps()
 ring(G_CX,G_CY,G_RI,(15,15,15),3,(70,70,75))
def G_score(n):
 if n:
  text(66,17,str(n-1),BLACK)
 else:
  text(204,17,'CLEAR quit',GREY)
  text(6,17,'Score')
 text(66,17,str(n))
 if n:
  s=str(n-1)
  text(G_CX-len(s)*5,G_CY+7,s,(25,25,28))
 else:
  circ(G_CX,G_CY,G_RI-6,(25,25,28))
 s=str(n)
 text(G_CX-len(s)*5,G_CY+7,s,WHITE)
def G_flash(i,t):
 G_pad(i,True)
 pause(t)
 G_pad(i,False)
 pause(0.12)
def G_game():
 cls()
 G_body()
 seq=[]
 while True:
  G_score(len(seq))
  seq.append(random.randint(0,3))
  pause(0.5)
  t=max(0.18,0.5-len(seq)*0.02)
  for i in seq:
   G_flash(i,t)
  for want in seq:
   k=wkey()
   if k==CLR:
    return
   got=-1
   for i in range(4):
    if G_PADS[i][0]==k:
     got=i
   if got<0:
    got=-2
   if got>=0:
    G_flash(got,0.15)
   if got!=want:
    if got>=0:
     pass
    message(['You got '+str(len(seq)-1)+' in a row.'],'Wrong color!')
    return
G_RULES='Watch the colors light up, then repeat them in the same order. Each round adds one more.'
G_KEYS=['Up: green   Right: red','Down: blue  Left: yellow','CLEAR: quit']
def G_main():
 while True:
  c=home('GHSIMON','SIMON',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
