# GHPONG from GAMEHUB, on its own. Run it.
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
class Steer:
 def __init__(self,keys,stop_on_back=False):
  self.keys=keys
  self.back=stop_on_back
  self.d=0
 def feed(self,k):
  if k in self.keys:
   if self.back and self.d and(k!=self.d)and(self.keys.index(k)//2==self.keys.index(self.d)//2):
    self.d=0
   else:
    self.d=k
  elif k:
   self.d=0
  return self.d
 def stop(self):
  self.d=0
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
def vacate(ox,oy,nx,ny,w,h,c):
 if abs(nx-ox)>=w or abs(ny-oy)>=h:
  rect(ox,oy,w,h,c)
  return
 if ny>oy:
  rect(ox,oy,w,ny-oy,c)
 elif ny<oy:
  rect(ox,ny+h,w,oy-ny,c)
 y0=max(oy,ny)
 y1=min(oy,ny)+h
 if nx>ox:
  rect(ox,y0,nx-ox,y1-y0,c)
 elif nx<ox:
  rect(nx+w,y0,ox-nx,y1-y0,c)
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
I_WHITE=(255,255,255)
I_BG={'GHPONG':(30,85,165)}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_hline(x1,x2,y,c,t=1):
 I_c_(c)
 for o in range(t):
  draw_line(int(x1),int(y)+o,int(x2),int(y)+o)
def I_circ(x,y,r,c):
 I_c_(c)
 fill_circle(int(x),int(y),int(r))
def I_pong(x,y,c):
 I_c_(I_WHITE)
 draw_rect(x-22,y-16,44,32)
 I_hline(x-21,x+21,y,(200,210,230))
 for i in range(6):
  I_box(x,y-15+i*6,2,3,I_WHITE)
 I_box(x-17,y-11,4,14,I_WHITE)
 I_box(x+14,y-3,4,14,I_WHITE)
 I_circ(x-6,y-5,2,(250,150,40))
I_ICONS={'GHPONG':I_pong}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_PH=36
G_TOP=24
G_TABLE=(30,85,165)
G_BALL=(250,150,40)
G_LINE=(150,190,235)
def G_net(box=None):
 if box is None or G_ring_hit(box):
  col(G_LINE)
  draw_circle(160,117,28)
 for y in range(G_TOP+2,208,14):
  if box is None or(box[1]<y+7 and y<box[1]+8 and(box[0]<161)and(159<box[0]+8)):
   rect(159,y,2,7,WHITE)
def G_ring_hit(b):
 x0,y0=b
 nx=min(max(160,x0),x0+7)-160
 ny=min(max(117,y0),y0+7)-117
 fx=max(abs(x0-160),abs(x0+7-160))
 fy=max(abs(y0-117),abs(y0+7-117))
 return nx*nx+ny*ny<=29*29 and fx*fx+fy*fy>=27*27
def G_court():
 cls(G_TABLE)
 rect(0,207,320,3,G_LINE)
 rect(0,G_TOP+1,320,1,G_LINE)
 G_net()
def G_paddle(x,y,c):
 rect(x,y,6,G_PH,c)
def G_puck(x,y):
 rect(x-4,y-4,8,8,G_BALL)
def G_scores(a,b):
 rect(0,0,320,G_TOP-2,G_TABLE)
 text(110,18,str(a))
 text(200,18,str(b),GOLD)
 rect(0,G_TOP-2,320,2,WHITE)
 text(14,18,'YOU',G_LINE)
 text(250,18,'CALC',G_LINE)
def G_game():
 G_court()
 me=cpu=0
 py=cy=100
 G_scores(me,cpu)
 serve=1
 while me<7 and cpu<7:
  bx,by=(160.0,110.0)
  vx=4.0*serve
  vy=random.choice((-2.5,-1.5,1.5,2.5))
  G_paddle(8,py,WHITE)
  G_paddle(306,cy,GOLD)
  pause(0.5)
  st=Steer((UP,DOWN))
  while True:
   k=key()
   if k==CLR:
    return
   opy,ocy=(py,cy)
   d=st.feed(k)
   if d==UP:
    py=max(G_TOP+3,py-6)
    if py==G_TOP+3:
     st.stop()
   elif d==DOWN:
    py=min(206-G_PH,py+6)
    if py==206-G_PH:
     st.stop()
   target=by-G_PH/2
   if vx>0 and bx>120:
    cy+=max(-4,min(4,target-cy))
   cy=int(max(G_TOP+3,min(206-G_PH,cy)))
   obx,oby=(bx,by)
   bx+=vx
   by+=vy
   if by<G_TOP+6 or by>202:
    vy=-vy
    by=max(G_TOP+6,min(202,by))
   if bx<18 and vx<0 and(py-4<by<py+G_PH+4):
    vx=min(9,-vx*1.06)
    vy+=(by-(py+G_PH/2))/6
    bx=18
   if bx>302 and vx>0 and(cy-4<by<cy+G_PH+4):
    vx=max(-9,-vx*1.06)
    vy+=(by-(cy+G_PH/2))/6
    bx=302
   ob=(int(obx)-4,int(oby)-4)
   vacate(ob[0],ob[1],int(bx)-4,int(by)-4,8,8,G_TABLE)
   if opy!=py:
    vacate(8,opy,8,py,6,G_PH,G_TABLE)
   if ocy!=cy:
    vacate(306,ocy,306,cy,6,G_PH,G_TABLE)
   if 0<obx<24:
    G_paddle(8,py,WHITE)
   elif opy!=py:
    vacate(8,py,8,opy,6,G_PH,WHITE)
   if 126<obx<194:
    G_net(ob)
   if 296<obx<320:
    G_paddle(306,cy,GOLD)
   elif ocy!=cy:
    vacate(306,cy,306,ocy,6,G_PH,GOLD)
   G_puck(int(bx),int(by))
   if bx<0:
    cpu+=1
    serve=1
    break
   if bx>320:
    me+=1
    serve=-1
    break
  rect(int(bx)-4,int(by)-4,8,8,G_TABLE)
  G_net()
  G_scores(me,cpu)
 message(['You '+str(me)+' - '+str(cpu)+' Calculator'],'You win!'if me>cpu else 'Calculator wins')
G_RULES="Bounce the ball past the calculator's paddle. First to 7 points wins."
G_KEYS=['Up/Down: paddle glides that way','ENTER: stop the paddle','CLEAR: quit']
def G_main():
 while True:
  c=home('GHPONG','PONG',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
