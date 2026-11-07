# GHCRYPT from GAMEHUB, on its own. Run it.
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
DEL=23
SECOND=21
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
GREY=(110,110,110)
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
def pause(s):
 time.sleep(s)
def choose(title,opts,sel=0):
 cls()
 ctext(24,title,GOLD)
 n=len(opts)
 for i in range(n):
  y=40+i*30
  c=GOLD if i==sel else WHITE
  rbox(60,y,200,24,8,c,2,BLACK,False)
  ctext(y+18,opts[i],c)
 while True:
  k=wkey()
  old=sel
  if k==UP:
   sel=(sel-1)%n
  elif k==DOWN:
   sel=(sel+1)%n
  elif k==OK:
   return sel
  elif k==CLR:
   return-1
  if sel==old:
   continue
  for i in(old,sel):
   y=40+i*30
   c=GOLD if i==sel else WHITE
   edge(60,y,200,24,8,c)
   ctext(y+18,opts[i],c)
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
I_BG={}
def I_c_(c):
 set_color(c[0],c[1],c[2])
def I_line(x1,y1,x2,y2,c,t=1):
 I_c_(c)
 for o in range(t):
  draw_line(int(x1)+o,int(y1),int(x2)+o,int(y2))
def I_hline(x1,x2,y,c,t=1):
 I_c_(c)
 for o in range(t):
  draw_line(int(x1),int(y)+o,int(x2),int(y)+o)
def I_crypt(x,y,c):
 rs=[7]
 def rnd(a,b):
  rs[0]=(rs[0]*1103515245+12345)%2147483648
  return a+rs[0]%(b-a+1)
 k=0.21
 ox=x+3
 oy=y-17
 ca=math.cos(0.55)
 sa=math.sin(0.55)
 def m(cx,cy):
  return(ox+(cx-140)*k,oy+(cy-50)*k)
 def head(lx,ly):
  return m(140+lx*ca-ly*sa,50+lx*sa+ly*ca)
 def band(pts,w):
  left=[]
  right=[]
  for i in range(len(pts)-1):
   (x1,y1),(x2,y2)=(pts[i],pts[i+1])
   d=math.sqrt((x2-x1)**2+(y2-y1)**2)or 1
   nx=-(y2-y1)/d*w/2
   ny=(x2-x1)/d*w/2
   left+=[(x1+nx,y1+ny),(x2+nx,y2+ny)]
   right+=[(x1-nx,y1-ny),(x2-nx,y2-ny)]
  return[m(px,py)for px,py in left+right[::-1]]
 shapes=[[head(17*math.cos(t*math.pi/8),25*math.sin(t*math.pi/8))for t in range(16)],[head(px,py)for px,py in((-18,-6),(-27,30),(-24,96),(-6,70),(8,100),(20,60),(17,-6),(10,-24),(-10,-24))],band(((128,125),(132,88),(140,66)),11),[m(px,py)for px,py in((98,122),(128,112),(160,126),(150,210),(148,250),(108,250),(106,210))],band(((100,128),(84,250),(90,260)),7),band(((158,128),(176,248),(170,258)),7)]
 def spans(pts):
  out=[]
  ys=[p[1]for p in pts]
  n=len(pts)
  for row in range(int(min(ys)),int(max(ys))+1):
   yc=row+0.5
   xs=[]
   for i in range(n):
    (x1,y1),(x2,y2)=(pts[i],pts[(i+1)%n])
    if y1<=yc<y2 or y2<=yc<y1:
     xs.append(x1+(yc-y1)*(x2-x1)/(y2-y1))
   if len(xs)>=2:
    out.append((row,int(min(xs)+0.5),int(max(xs)+0.5)))
  return out
 all_spans=[spans(sh)for sh in shapes]
 for sp in all_spans:
  for row,a,b in sp:
   g=rnd(190,255)
   I_hline(a,max(a,b-1),row,(g,g*19//20,g*9//10))
 for sp in all_spans:
  for row,a,b in sp[1:-1]:
   if b-a>2:
    g=rnd(28,62)
    I_hline(a+1,b-2,row,(g,g,g+8))
 pts=[]
 for ex,ey in((137.2,41.2),(149.1,48.55)):
  a,b=m(ex,ey)
  pts.append((int(a),int(b)))
 for a,b in pts:
  I_hline(a-1,a+1,b-1,(35,80,150))
  I_hline(a-2,a+2,b,(35,80,150))
  I_hline(a-1,a+1,b+1,(35,80,150))
 for a,b in pts:
  I_hline(a-1,a+1,b,(80,175,245))
  I_line(a,b-1,a,b+1,(80,175,245))
 for a,b in pts:
  I_hline(a,a,b,(230,250,255))
I_ICONS={'GHCRYPT':I_crypt}
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
G_MAP=['#BBBB###SSS###','B....#.......#','B............k','#####G.......#','#....#.......#','T....l.......j','#....#.......C','########PF####']
G_VW=320
G_VH=172
G_COLS=32
G_CWID=G_VW//G_COLS
G_FOV=1.0
G_WALL=(75,95,99)
G_DOOR=(110,75,45)
G_FLOOR=(42,36,32)
G_CEIL=(16,16,18)
G_LINK1='petradavis.github.io/'
G_LINK2='Encrypted/?ysolde=1'
G_CIPHER='LI WKH OLJKWV GLH VKH LV LQ WKH URRP. GRQW UXQ. KLGH LQ WKH FRDW FORVHW. LWV FRGH LV HFKR'
G_TAPGRID=('ABCDE','FGHIK','LMNOP','QRSTU','VWXYZ')
G_KNOCKS=((4,1),(4,5),(2,4),(1,5),(4,4))
class G_St:
 pass
G_SPR={'couch':(1.3,((0,1,0,0.2,(150,40,45)),(0.08,0.92,0.2,0.36,(120,30,35)),(0,0.12,0.2,0.28,(150,40,45)),(0.88,1,0.2,0.28,(150,40,45)))),'table':(0.9,((0,0.12,0,0.28,(95,65,40)),(0.88,1,0,0.28,(95,65,40)),(0,1,0.28,0.33,(120,85,50)),(0.3,0.7,0.33,0.37,(140,70,180)))),'phone':(0.6,((0,0.15,0,0.3,(95,65,40)),(0.85,1,0,0.3,(95,65,40)),(0,1,0.3,0.34,(120,85,50)),(0.25,0.75,0.34,0.42,(20,20,20)))),'lamp':(0.6,((0.45,0.55,0,0.55,(180,150,70)),(0.15,0.85,0.55,0.72,(235,220,170)))),'desk':(1.2,((0,0.1,0,0.3,(95,65,40)),(0.9,1,0,0.3,(95,65,40)),(0,1,0.3,0.35,(120,85,50)),(0.2,0.5,0.35,0.38,(200,190,150)))),'rack':(0.7,((0.46,0.54,0,0.8,(80,55,35)),(0.15,0.45,0.35,0.75,(60,70,110)),(0.55,0.85,0.4,0.72,(110,50,50)))),'vase':(0.7,((0.1,0.9,0,0.25,(95,65,40)),(0.35,0.65,0.25,0.45,(60,120,140)),(0.3,0.7,0.45,0.55,(90,140,70))))}
G_SPRITES=[(3.3,5.5,'couch'),(1.9,4.6,'table'),(4.4,6.4,'phone'),(1.0,6.5,'lamp'),(2.6,1.5,'desk'),(12.4,4.9,'rack'),(6.5,1.4,'vase')]
G_ROOMS=(('Library',0,0,5,3),('Living Room',0,3,5,8),('Grand Foyer',5,0,14,8))
def G_tile(x,y):
 if 0<=y<len(G_MAP)and 0<=int(x)<14:
  return G_MAP[int(y)][int(x)]
 return '#'
def G_solid(g,x,y):
 t=G_tile(x,y)
 if t=='l'and g.living:
  return False
 return t!='.'
def G_room(g):
 for n,x0,y0,x1,y1 in G_ROOMS:
  if x0<=g.x<x1 and y0<=g.y<y1:
   return n
 return 'Grand Foyer'
def G_clock():
 return G_now()if G_now else 0
def G_shade(c,k):
 return(min(255,int(c[0]*k)),min(255,int(c[1]*k)),min(255,int(c[2]*k)))
def G_light(g,i,d):
 if g.blackout:
  base=0.0
 elif g.power:
  base=max(0.35,1.0-d/14)
 else:
  base=0.06
 if g.flash:
  off=abs(i-G_COLS/2)/(G_COLS*0.32)
  if off<1:
   base+=(1-off)*max(0,1-d/12)*(1.1 if not g.power else 0.35)
 return min(1.2,base)
def G_colour(t):
 if t in 'lkjCF':
  return G_DOOR
 if t=='S':
  return(120,90,60)
 if t=='B':
  return(90,60,35)
 return G_WALL
def G_lq(k):
 return int(k*5+0.5)/5
def G_put(sp,a,b,c):
 if b<=a:
  return sp
 out=[]
 for y0,y1,cc in sp:
  if y0<a:
   out.append((y0,min(y1,a),cc))
 out.append((a,b,c))
 for y0,y1,cc in sp:
  if y1>b:
   out.append((max(y0,b),y1,cc))
 return out
def G_diff(old,new):
 if old is None:
  return new
 out=[]
 i=j=0
 y=0
 while y<G_VH:
  o0,o1,oc=old[i]
  n0,n1,nc=new[j]
  e=min(o1,n1)
  if oc!=nc:
   if out and out[-1][1]==y and(out[-1][2]==nc):
    out[-1]=(out[-1][0],e,nc)
   else:
    out.append((y,e,nc))
  y=e
  if o1==e:
   i+=1
  if n1==e:
   j+=1
 return out
def G_column(g,t,u,top,h,k):
 cl=(0,0,0)if g.blackout else G_CEIL
 fl=(0,0,0)if g.blackout else G_shade(G_FLOOR,0.5 if not g.power else 1)
 y0=max(0,top)
 y1=min(G_VH,top+h)
 sp=[(0,y0,cl),(y0,y1,G_shade(G_colour(t),k)),(y1,G_VH,fl)]
 if y0==0:
  sp=sp[1:]
 if y1==G_VH:
  sp=sp[:-1]
 sp=[s for s in sp if s[1]>s[0]]
 def band(v0,v1,c):
  a=int(top+h*(1-v1))&~1
  b=int(top+h*(1-v0))&~1
  if b-a>=2:
   return G_put(sp,max(0,a),min(G_VH,b),G_shade(c,k))
  return sp
 if t in 'lkjCF':
  if u<0.12 or u>0.88:
   sp=band(0,0.8,(70,48,30))
  sp=band(0.8,1,G_WALL)
  if 0.7<u<0.85:
   sp=band(0.42,0.47,(210,180,90))
  if t in 'kC'and 0.12<u<0.3:
   on=t=='C'and g.closet
   sp=band(0.5,0.6,(40,40,40))
   sp=band(0.53,0.57,(40,200,70)if on else(200,40,40)if g.power else(30,30,30))
  if t=='F'and g.locked and(0.15<u<0.25):
   sp=band(0.6,0.64,(255,30,40))
 elif t=='S':
  for n in range(6):
   sp=band(n*0.14,n*0.14+0.07,(95,70,45))
  if 0.2<u<0.8:
   sp=band(0.25,0.32,(150,120,80))
   sp=band(0.55,0.62,(150,120,80))
 elif t=='B':
  for n in range(4):
   cc=((150,50,50),(50,90,150),(60,130,70),(170,140,60))[(int(u*4)+n)%4]
   sp=band(n*0.25+0.05,n*0.25+0.2,cc)
 elif t=='T':
  if 0.1<u<0.9:
   sp=band(0.35,0.7,(15,15,20)if not g.tv else(60,90,160))
 elif t=='G':
  if 0.28<u<0.72:
   sp=band(0,0.85,(70,45,30))
   sp=band(0.6,0.75,(220,210,180))
   if 0.45<u<0.55:
    sp=band(0.2,0.55,(180,150,70))
    if not g.note:
     sp=band(0.25,0.3,(240,240,230))
 elif t=='P':
  if 0.3<u<0.6:
   sp=band(0.38,0.56,(130,130,135))
   if 0.4<u<0.5:
    sp=band(0.44 if g.power else 0.48,0.54 if g.power else 0.58,(40,40,40))
 return sp
def G_render(g,full=False):
 if full or not hasattr(g,'cols')or g.cover!=COVER[0]:
  g.cover=COVER[0]
  g.cols=[None]*G_COLS
  g.ysk=None
 shown=g.cols
 new=[]
 zb=[0]*G_COLS
 ca=math.cos(g.a)
 sa=math.sin(g.a)
 for i in range(G_COLS):
  cam=(i+0.5)/G_COLS*2-1
  rx=ca-sa*cam*G_FOV*0.5*1.15
  ry=sa+ca*cam*G_FOV*0.5*1.15
  mx=int(g.x)
  my=int(g.y)
  ddx=abs(1/rx)if rx else 1000000000.0
  ddy=abs(1/ry)if ry else 1000000000.0
  if rx<0:
   sx=-1
   sdx=(g.x-mx)*ddx
  else:
   sx=1
   sdx=(mx+1-g.x)*ddx
  if ry<0:
   sy=-1
   sdy=(g.y-my)*ddy
  else:
   sy=1
   sdy=(my+1-g.y)*ddy
  side=0
  t='#'
  for n in range(40):
   if sdx<sdy:
    sdx+=ddx
    mx+=sx
    side=0
   else:
    sdy+=ddy
    my+=sy
    side=1
   t=G_tile(mx,my)
   if t!='.'and(not(t=='l'and g.living)):
    break
  d=sdx-ddx if side==0 else sdy-ddy
  d=max(d,0.05)
  zb[i]=d
  if side==0:
   u=g.y+d*ry
  else:
   u=g.x+d*rx
  u-=int(u)
  h=int(G_VH*1.35/d)&~7
  top=(G_VH-h)//2
  k=G_lq(G_light(g,i,d)*(0.8 if side else 1.0))
  new.append(G_column(g,t,u,top,h,k))
 G_sprites(g,zb,ca,sa,new)
 ys=G_ys_place(g,zb,ca,sa)
 if g.ysk is not None and(ys is None or ys[0]!=g.ysk):
  for i in range(g.ysa,g.ysb):
   shown[i]=None
 runs={}
 hit=False
 for i in range(G_COLS):
  for y0,y1,c in G_diff(shown[i],new[i]):
   key=(y0,y1,c)
   r=runs.get(key)
   if r and r[-1][1]==i:
    r[-1][1]=i+1
   elif r:
    r.append([i,i+1])
   else:
    runs[key]=[[i,i+1]]
   if ys and ys[1]<=i<ys[2]:
    hit=True
  shown[i]=new[i]
 for key in sorted(runs,key=lambda q:q[2]):
  y0,y1,c=key
  for a,b in runs[key]:
   rect(a*G_CWID,y0,(b-a)*G_CWID,y1-y0,c)
 if ys:
  if ys[0]!=g.ysk or hit:
   G_ys_draw(g,ys)
  else:
   G_ys_shimmer(g)
  g.ysk,g.ysa,g.ysb=(ys[0],ys[1],ys[2])
 else:
  g.ysk=None
def G_sprites(g,zb,ca,sa,new):
 lst=[]
 for sx,sy,kind in G_SPRITES:
  dx=sx-g.x
  dy=sy-g.y
  fwd=dx*ca+dy*sa
  if fwd<0.2:
   continue
  lst.append((fwd,-dx*sa+dy*ca,kind))
 lst.sort(reverse=True)
 for fwd,side,kind in lst:
  cx=side/fwd/(G_FOV*0.5*1.15)
  scol=(cx+1)/2*G_COLS
  half=G_SPR[kind][0]/2/fwd/(G_FOV*0.5*1.15)*G_COLS/2
  h=G_VH*1.35/fwd
  top=(G_VH-h)/2
  k=G_lq(G_light(g,int(scol),fwd))
  for i in range(max(0,int(scol-half)),min(G_COLS,int(scol+half)+1)):
   if zb[i]<fwd:
    continue
   u=(i+0.5-(scol-half))/(2*half)if half>0 else 0.5
   if u<0 or u>1:
    continue
   for u0,u1,v0,v1,c in G_SPR[kind][1]:
    if u0<=u<=u1:
     y0=int(top+h*(1-v1))&~1
     y1=int(top+h*(1-v0))&~1
     if y1-y0>=2 and y0<G_VH:
      new[i]=G_put(new[i],max(0,y0),min(G_VH,y1),G_shade(c,k))
def G_bottom(g,prompt):
 if prompt==g.shown:
  return
 g.shown=prompt
 rect(0,G_VH,320,210-G_VH,BLACK)
 text(4,G_VH+15,G_room(g),GREY)
 if g.flash:
  text(250,G_VH+15,'LIGHT',GOLD)
 text(4,G_VH+33,prompt[:31],WHITE)
G_YS=[]
def G__poly_slabs(pts,kind,step,top=True,bottom=True):
 ys=[p[1]for p in pts]
 y=min(ys)
 n=len(pts)
 first=len(G_YS)
 while y<max(ys):
  yc=y+step/2
  xs=[]
  for i in range(n):
   x1,y1=pts[i]
   x2,y2=pts[(i+1)%n]
   if y1<=yc<y2 or y2<=yc<y1:
    xs.append(x1+(yc-y1)*(x2-x1)/(y2-y1))
  if len(xs)>=2:
   G_YS.append((min(xs)/256,max(xs)/256,1-(y+step)/640,1-y/640,kind))
  y+=step
 for i,on in((first,top),(len(G_YS)-1,bottom)):
  if on and i<len(G_YS):
   u0,u1,v0,v1,k=G_YS[i]
   G_YS[i]=(u0,u1,v0,v1,5)
def G__limb(pts,w,kind=0):
 for i in range(0,len(pts)-2,2):
  x1,y1,x2,y2=(pts[i],pts[i+1],pts[i+2],pts[i+3])
  n=max(1,int(abs(y2-y1)/8))
  for k in range(n):
   t0=k/n
   t1=(k+1)/n
   xm=x1+(x2-x1)*(t0+t1)/2
   ya=y1+(y2-y1)*t0
   yb=y1+(y2-y1)*t1
   hw=w*0.4+abs(x2-x1)/n/3
   G_YS.append(((xm-hw)/256,(xm+hw)/256,1-max(ya,yb)/640-0.004,1-min(ya,yb)/640+0.004,kind))
def G__oval(cx,cy,rx,ry,kind,step,a=0.0):
 ca=math.cos(0.55)
 sa=math.sin(0.55)
 pts=[]
 for i in range(16):
  t=2*math.pi*i/16
  lx=cx+rx*math.cos(t)*math.cos(a)-ry*math.sin(t)*math.sin(a)
  ly=cy+rx*math.cos(t)*math.sin(a)+ry*math.sin(t)*math.cos(a)
  pts.append((140+lx*ca-ly*sa,50+lx*sa+ly*ca))
 G__poly_slabs(pts,kind,step)
def G__build_ys():
 ca=math.cos(0.55)
 sa=math.sin(0.55)
 G__limb([128,120,132,88,140,66],11)
 G__poly_slabs([(98,122),(128,112),(160,126),(150,210),(146,260),(110,260),(106,210)],0,8,True,False)
 hem=[(108,250),(148,250),(162,330)]
 x=162
 while x>94:
  hem.append((x-4.5,330+(18 if int(x)%2 else 6)))
  x-=9
 hem.append((94,330))
 G__poly_slabs(hem,0,6,False,True)
 G__limb([118,320,112,460,120,470,108,612,98,628],9)
 G__limb([140,320,146,462,136,474,150,610,162,630],9)
 G__limb([100,128,84,250,92,262,76,420],7)
 G__limb([158,128,176,248,166,262,184,410],7)
 for x0,y0,sg in((76,420,-1),(184,410,1)):
  for f in range(5):
   G__limb([x0,y0,x0+sg*(f*4-6),y0+52+f%2*8,x0+sg*(f*5-4),y0+70+f*3],2.6)
 hair=[(-18,-6),(-27,30),(-24,96),(-6,70),(8,100),(20,60),(17,-6),(10,-24),(-10,-24)]
 G__poly_slabs([(140+lx*ca-ly*sa,50+lx*sa+ly*ca)for lx,ly in hair],0,4)
 G__oval(0,0,17,25,0,4)
 for ex,ey in((137.2,41.2),(149.1,48.55)):
  G_YS.append(((ex-2)/256,(ex+2)/256,1-(ey+2)/640,1-(ey-2)/640,4))
G_YG=4
G_RIM=((215,215,225),(170,175,190),(250,250,255))
G_INSIDE=(36,36,44)
def G_ys_place(g,zb,ca,sa):
 if not g.ys_vis:
  return None
 dx=g.yx-g.x
 dy=g.yy-g.y
 fwd=dx*ca+dy*sa
 if fwd<0.2:
  return None
 cx=(-dx*sa+dy*ca)/fwd/(G_FOV*0.5*1.15)
 scol=(cx+1)/2*G_COLS
 half=0.45/2/fwd/(G_FOV*0.5*1.15)*G_COLS/2
 h=int(G_VH*1.35/fwd)&~7
 top=(G_VH-h)//2
 a=None
 b=0
 for i in range(max(0,int(scol-half)),min(G_COLS,int(scol+half)+1)):
  if zb[i]>=fwd:
   if a is None:
    a=i
   b=i+1
 if a is None:
  return None
 left=int((scol-half)*G_CWID)&~3
 return((left,int(2*half*G_CWID)&~3,top,h,a,b),a,b)
def G_ys_draw(g,ys):
 if not G_YS:
  G__build_ys()
 left,wid,top,h,a,b=ys[0]
 lo=a*G_CWID
 hi=b*G_CWID
 rows={}
 eyes=[]
 for u0,u1,v0,v1,kind in G_YS:
  xa=max(lo,int(left+u0*wid))//G_YG
  xb=min(hi,int(left+u1*wid)+1+G_YG-1)//G_YG
  ya=int(top+h*(1-v1))
  yb=int(top+h*(1-v0))+1
  if kind==4:
   eyes.append(((xa+xb)*G_YG//2,(ya+yb)//2))
   continue
  if xb<=xa:
   continue
  for r in range(max(0,ya)//G_YG,(min(G_VH,yb)+G_YG-1)//G_YG):
   if r in rows:
    rows[r].append((xa,xb))
   else:
    rows[r]=[(xa,xb)]
 out=[]
 open_={}
 for r in range(G_VH//G_YG+1):
  cur={}
  segs=sorted(rows.get(r,()))
  m=[]
  for xa,xb in segs:
   if m and xa<=m[-1][1]:
    if xb>m[-1][1]:
     m[-1][1]=xb
   else:
    m.append([xa,xb])
  for xa,xb in m:
   if xb-xa>=3:
    cur[xa,xa+1,0]=1
    cur[xa+1,xb-1,1]=1
    cur[xb-1,xb,0]=1
   else:
    cur[xa,xb,0]=1
  for key in list(open_):
   if key not in cur:
    out.append((key,open_.pop(key),r))
  for key in cur:
   if key not in open_:
    open_[key]=r
 g.rim=[]
 for c in(0,1):
  for(xa,xb,kind),r0,r1 in out:
   if kind==c:
    x,y,w,hh=(xa*G_YG,r0*G_YG,(xb-xa)*G_YG,min(G_VH,r1*G_YG)-r0*G_YG)
    if hh>0:
     rect(x,y,w,hh,G_INSIDE if c else G_RIM[0])
     if not c:
      g.rim.append((x,y,w,hh))
 r=max(2,wid//12)
 eyes=[(x,y)for x,y in eyes if lo+r<=x<hi-r and r<=y<G_VH-r]
 for rr,c in((r,(35,80,150)),(r*2//3,(80,175,245)),(max(1,r//3),(230,250,255))):
  for x,y in eyes:
   circ(x,y,rr,c)
def G_ys_shimmer(g):
 if not g.rim:
  return
 for n in range(3):
  x,y,w,h=random.choice(g.rim)
  rect(x,y,w,h,random.choice(G_RIM))
def G_wrap(s,n=30):
 out=[]
 for para in s.split('\n'):
  line=''
  for w in para.split(' '):
   if len(line)+len(w)+1>n:
    out.append(line)
    line=w
   else:
    line=(line+' '+w).strip()
  out.append(line)
 return out
def G_page(title,body,color=WHITE):
 lines=G_wrap(body)
 per=9
 for p in range(0,len(lines),per):
  cls()
  ctext(20,title,GOLD)
  y=44
  for ln in lines[p:p+per]:
   text(10,y,ln,color)
   y+=17
  more=p+per<len(lines)
  text(10,204,'ENTER: more'if more else 'ENTER/CLEAR: close',GREY)
  while True:
   k=wkey()
   if k in(OK,CLR):
    break
  if k==CLR:
   return
def G_toast(g,lines):
 COVER[0]+=1
 rbox(10,50,300,30+18*len(lines),8,WHITE)
 y=72
 for ln in lines:
  ctext(y,ln)
  y+=18
 while wkey()not in(OK,CLR):
  pass
 g.shown=None
def G_say(g,s):
 G_toast(g,G_wrap(s,27))
def G_keypad(title,hint,n):
 abc='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
 cls()
 ctext(20,title,GOLD)
 y=42
 for ln in G_wrap(hint,30):
  text(10,y,ln,GREY)
  y+=17
 typed=''
 sel=0
 while True:
  rect(60,96,200,26,BLACK)
  s=''
  for i in range(n):
   s+=(typed[i]if i<len(typed)else '_')+' '
  ctext(116,s.strip(),WHITE)
  for i in range(26):
   x=4+i%13*24
   yy=140+i//13*28
   c=GOLD if i==sel else WHITE
   rect(x,yy,22,24,BLACK)
   rbox(x,yy,22,24,5,c)
   text(x+6,yy+18,abc[i],c)
  k=wkey()
  if k==LEFT:
   sel=(sel-1)%26
  elif k==RIGHT:
   sel=(sel+1)%26
  elif k in(UP,DOWN):
   sel=(sel+13)%26
  elif k==DEL:
   typed=typed[:-1]
  elif k==CLR:
   return None
  elif k==OK:
   typed+=abc[sel]
   if len(typed)==n:
    return typed
def G_objective(g):
 if not g.power:
  t='It is pitch dark. Find the power switch by the front door.'
 elif not g.note:
  t='The door locked behind you. Look around the foyer.'
 elif not g.closet:
  t="Decode Ivy's note. The coat closet keypad wants four letters."
 elif not g.living:
  t='Unlock the Living Room.'
 elif not g.tapheard:
  t='The TV in the Living Room switched itself on.'
 elif not g.notebook:
  t="Decode the knocks. Ivy's notebook might explain them."
 else:
  t='Decode the knocks. The hallway keypad wants five letters.'
 if g.awake:
  t+='\nShe is awake. Stay quiet. Hide when the lights stutter.'
 return t
def G_short(g):
 if not g.power:
  return 'Find the power switch'
 if not g.note:
  return 'Look around the foyer'
 if not g.closet:
  return "Decode Ivy's note (DEL)"
 if not g.living:
  return 'Unlock the Living Room'
 if not g.tapheard:
  return 'The TV switched itself on'
 if not g.notebook:
  return "Find Ivy's notebook"
 return 'Hallway keypad: 5 letters'
def G_journal(g):
 body=G_objective(g)
 if g.note:
  body+="\n\nIvy's note: "+G_CIPHER+'\nMy name is the key.'
 if g.tapheard:
  body+='\n\nKnocks: 4-1 4-5 2-4 1-5 4-4'
 G_page('JOURNAL',body)
 if g.notebook:
  G_grid_page()
 g.shown=None
def G_grid_page():
 cls()
 ctext(20,"IVY'S NOTEBOOK",GOLD)
 text(10,44,'For talking through walls.',GREY)
 text(10,61,'Knocks: row, then column.',GREY)
 for r in range(5):
  text(110,92+r*20,str(r+1),GOLD)
  for c in range(5):
   if r==0:
    text(140+c*24,76,str(c+1),GOLD)
   text(140+c*24,92+r*20,G_TAPGRID[r][c])
 text(10,204,'I and J share a box.  ENTER',GREY)
 while wkey()not in(OK,CLR):
  pass
def G_facing(g):
 ca=math.cos(g.a)
 sa=math.sin(g.a)
 for n in range(1,9):
  d=n*0.2
  t=G_tile(g.x+ca*d,g.y+sa*d)
  if t!='.'and(not(t=='l'and g.living)):
   return t
 best=None
 bd=1.5
 for sx,sy,kind in G_SPRITES:
  dx=sx-g.x
  dy=sy-g.y
  dist=math.sqrt(dx*dx+dy*dy)
  if dist<bd and(dx*ca+dy*sa)/max(dist,0.01)>0.8:
   best=kind
   bd=dist
 return best
def G_label(g,t):
 if t=='P':
  return 'ENTER: power switch'
 if t=='F':
  return 'ENTER: front door'
 if t=='G':
  return 'ENTER: grandfather clock'
 if t=='C':
  return 'ENTER: hide in closet'if g.closet else 'ENTER: closet keypad'
 if t=='l':
  return 'ENTER: Living Room door'
 if t=='k':
  return 'ENTER: hallway keypad'
 if t=='j':
  return 'ENTER: dining room door'
 if t=='S':
  return 'ENTER: grand staircase'
 if t=='T':
  return 'ENTER: smart TV'
 if t=='B':
  return 'ENTER: bookshelf'
 if t=='table':
  return "ENTER: Ivy's notebook"
 if t in('phone','desk','lamp','couch','rack','vase'):
  return 'ENTER: look'
 return ''
def G_use(g,t):
 if t=='P':
  if g.power:
   return G_say(g,'Power: on.')
  g.power=True
  for n in range(6):
   g.blackout=n%2==0
   G_render(g)
  g.blackout=False
  G_say(g,'CLUNK. Years of dust rattle in the wiring.')
  g.locked=True
  G_render(g)
  G_toast(g,['ASHGROVE SMART HOME:','Welcome home.','Front door LOCKED.','You did not set that up.'])
 elif t=='F':
  G_say(g,"SMART HOME: LOCKED. The handle doesn't move."if g.locked else 'The door is stuck. Swollen in its frame.')
 elif t=='G':
  if not g.power:
   return G_say(g,'Too dark to make it out. Get the lights on first.')
  g.note=True
  G_page("IVY'S NOTE",'Folded paper, tucked behind the pendulum glass.\n\nDad never notices anything. Grandma taught me this one when I was six. My name is the key.\n\n'+G_CIPHER+'\n\n- I.V.Y.')
  g.armed=True
 elif t=='C':
  if g.closet:
   return G_hide(g)
  if not g.power:
   return G_say(g,'The keypad is dead.')
  a=G_keypad('COAT CLOSET KEYPAD','A brass keypad. Four letters.',4)
  if a=='ECHO':
   g.closet=True
   g.shown=None
   G_render(g)
   G_say(g,'The closet clicks open. On a hook: a brass key tagged LIVING ROOM. You take it.')
  elif a:
   G_say(g,'The keypad buzzes. Wrong code.')
 elif t=='l':
  if not g.closet:
   return G_say(g,'Locked. A brass keyhole, polished from use.')
  g.living=True
  G_render(g)
  G_say(g,'The brass key turns. Stiff, then all at once.')
  g.tv=True
  G_say(g,'Somewhere in the Living Room, a TV switches itself on.')
 elif t=='j':
  G_say(g,'Swollen shut in its frame.')
 elif t=='S':
  G_say(g,'Boarded, chained and padlocked. The padlock is engraved M.A.')
 elif t=='B':
  G_say(g,"Books on radios, codes and moths. Mildred's, mostly.")
 elif t=='T':
  if not g.power:
   return G_say(g,'The TV is dark.')
  G_tv(g)
 elif t=='table':
  g.notebook=True
  G_grid_page()
  G_page("IVY'S NOTEBOOK","She can hear voices and screens. She's bad at knocks. I think it's too slow for her.\n\n- Ivy")
 elif t=='phone':
  G_say(g,'An old rotary phone. Silent. For now.')
 elif t=='desk':
  G_say(g,"Mildred's desk. Pages and pages of dots and dashes.")
 elif t=='lamp':
  G_say(g,'An old brass floor lamp.')
 elif t=='couch':
  G_say(g,'The cushions still hold the shape of someone.')
 elif t=='rack':
  G_say(g,"Coats on hooks. One is a child's raincoat.")
 elif t=='vase':
  G_say(g,'Dried flowers. They crumble when you breathe.')
 elif t=='k':
  if not g.power:
   return G_say(g,'The keypad is dark. No power.')
  a=G_keypad('ASHGROVE SMART LOCK','A sticky note in Ivy\'s writing: "the TV knows. listen."',5)
  if a=='QUIET':
   g.won=True
  elif a:
   G_say(g,'The keypad buzzes. Wrong code.')
 g.shown=None
def G_tv(g):
 cls((10,14,30))
 ctext(24,'ASHGROVE SMART TV',GOLD)
 text(10,48,'HDMI 3: for whoever comes next',GREY)
 text(10,66,'Then black. Then knocking.',GREY)
 y=100
 x=20
 for r,c in G_KNOCKS:
  for grp in(r,c):
   for n in range(grp):
    circ(x,y,4,WHITE)
    x+=11
    pause(0.25)
   x+=10
  x+=14
  if x>270:
   x=20
   y+=24
 text(10,170,'4-1  4-5  2-4  1-5  4-4',(160,210,255))
 text(10,204,'Written in your journal. ENTER',GREY)
 g.tapheard=True
 while wkey()not in(OK,CLR):
  pass
 if not g.awake:
  g.awake=True
  g.ytimer=6
  G_page('...','The knocking stops.\nEvery screen in the house flickers at once.\n\nShe is awake. Hide when the lights stutter.',(200,140,140))
def G_hide(g):
 g.hidden=True
 cls()
 ctext(70,'You squeeze into the coat',WHITE)
 ctext(90,'closet. Breathe slowly.',WHITE)
 ctext(150,'ENTER: step out',GREY)
 t0=0
 while True:
  k=key()
  if k==OK:
   break
  pause(0.2)
  t0+=1
  if g.ystate=='hunt'and t0>25:
   g.ystate='dormant'
   g.ys_vis=False
   g.ytimer=random.randint(35,55)
   rect(0,110,320,30,BLACK)
   ctext(130,"The static fades. She's gone.",GREY)
 g.hidden=False
 g.shown=None
def G_sighting(g):
 g.sighted=True
 g.yx,g.yy=(9.5,1.0)
 for n in range(10):
  g.blackout=n<3 and n%2==0
  g.ys_vis=n>=3
  g.yy=1.0+max(0,n-3)*0.08
  G_render(g)
  pause(0.2)
 g.ys_vis=False
 g.blackout=False
 G_render(g)
 G_say(g,'...it was a woman. Made of static. And she was looking at you.')
def G_ys_update(g,dt):
 if not g.awake or g.won:
  return
 if g.ystate=='dormant':
  g.ytimer-=dt
  if g.ytimer<=0:
   g.ystate='warn'
   g.ytimer=4
   G_say(g,'Static hisses somewhere in the house. The lights stutter.')
 elif g.ystate=='warn':
  g.ytimer-=dt
  g.blackout=random.random()<0.35
  if g.ytimer<=0:
   g.blackout=False
   spots=((2.5,1.5),(9.5,1.5),(2.5,6.4),(11.5,1.5),(6.5,6.5))
   far=[p for p in spots if abs(p[0]-g.x)+abs(p[1]-g.y)>5]or list(spots)
   g.yx,g.yy=random.choice(far)
   g.ystate='hunt'
   g.ys_vis=True
   g.ytimer=28
 elif g.ystate=='hunt':
  g.ytimer-=dt
  dx=g.x-g.yx
  dy=g.y-g.yy
  d=math.sqrt(dx*dx+dy*dy)
  sp=0.55*dt
  if d>0.01:
   nx=g.yx+dx/d*sp
   ny=g.yy+dy/d*sp
   if not G_solid(g,nx,g.yy)or G_tile(nx,g.yy)in 'l':
    g.yx=nx
   if not G_solid(g,g.yx,ny):
    g.yy=ny
  g.blackout=d<3 and random.random()<0.25
  if d<0.6:
   G_caught(g)
  elif g.ytimer<=0:
   g.ystate='dormant'
   g.ys_vis=False
   g.blackout=False
   g.ytimer=random.randint(35,55)
def G_caught(g):
 for n in range(8):
  for y in range(0,176,22):
   gv=random.randint(60,230)
   rect(0,y,320,22,(gv,gv,gv))
 cls()
 ctext(90,'She found you.',(220,120,120))
 ctext(130,'ENTER',GREY)
 while wkey()not in(OK,CLR):
  pass
 g.x,g.y,g.a=(11.5,5.5,math.pi)
 g.ystate='dormant'
 g.ys_vis=False
 g.blackout=False
 g.ytimer=30
 g.shown=None
def G_ending():
 cls()
 ctext(40,'enCRYPTed',(200,60,60))
 ctext(70,'The keypad flashes green.')
 ctext(90,'End of the demo.')
 ctext(125,'Full game at',GOLD)
 ctext(147,G_LINK1,WHITE)
 ctext(167,G_LINK2,WHITE)
 ctext(203,'CLEAR: leave',GREY)
 while wkey()!=CLR:
  pass
def G_pause_menu(g):
 c=choose('PAUSED',['Resume','Journal','Quit demo'])
 g.shown=None
 if c==1:
  G_journal(g)
 return c==2
def G_play():
 g=G_St()
 g.x,g.y,g.a=(9.5,6.4,-math.pi/2)
 g.power=g.locked=g.note=g.closet=g.living=g.tv=False
 g.tapheard=g.notebook=g.awake=g.armed=g.sighted=False
 g.flash=True
 g.blackout=False
 g.won=False
 g.hidden=False
 g.ys_vis=False
 g.ystate='dormant'
 g.ytimer=0
 g.yx=g.yy=0
 g.shown=None
 cls()
 G_page('enCRYPTed','Ashgrove Manor. Bought at government auction. Power off since the accident.\n\nIt is pitch dark. Find the power switch by the front door.')
 last=G_clock()
 dirty=True
 st=Steer((UP,DOWN),True)
 while not g.won:
  k=key()
  d=st.feed(k)if k not in(LEFT,RIGHT)else st.d
  t=G_clock()
  dt=t-last if G_now else 0.25
  last=t
  dt=max(0.02,min(dt,0.5))
  moved=False
  if k==CLR:
   if G_pause_menu(g):
    return
   dirty=True
   continue
  if k==DEL:
   G_journal(g)
   dirty=True
   continue
  if k==SECOND:
   g.flash=not g.flash
   g.shown=None
   dirty=True
   while key()==SECOND:
    pass
  if k==LEFT:
   g.a-=2.0*max(dt,0.25)
   moved=True
  elif k==RIGHT:
   g.a+=2.0*max(dt,0.25)
   moved=True
  if d==UP or d==DOWN:
   s=(1.6 if d==UP else-1.0)*dt
   nx=g.x+math.cos(g.a)*s
   ny=g.y+math.sin(g.a)*s
   r=0.22 if s>0 else-0.22
   ox,oy=(g.x,g.y)
   if not G_solid(g,nx+math.cos(g.a)*r,g.y):
    g.x=nx
   if not G_solid(g,g.x,ny+math.sin(g.a)*r):
    g.y=ny
   if abs(g.x-ox)+abs(g.y-oy)<0.001:
    st.stop()
   moved=True
  elif k==OK:
   f=G_facing(g)
   if f:
    G_use(g,f)
    dirty=True
    while key()==OK:
     pass
  if g.armed and(not g.sighted)and(G_room(g)=='Grand Foyer'):
   look=math.atan2(1.0-g.y,9.5-g.x)
   diff=(look-g.a+math.pi)%(2*math.pi)-math.pi
   if abs(diff)<0.35:
    G_sighting(g)
    st.stop()
    dirty=True
  before=g.ys_vis or g.blackout
  G_ys_update(g,dt)
  if moved or dirty or g.ys_vis or g.blackout or before:
   G_render(g)
   dirty=False
  f=G_facing(g)
  G_bottom(g,G_label(g,f)if f else G_short(g))
  if not moved:
   pause(0.03)
 G_ending()
G_RULES="Explore Ashgrove Manor, solve Ivy's codes and hide from Ysolde when the lights stutter."
G_KEYS=['Up/Down: start walking','Press the other one to stop','Left/Right: turn a step','ENTER: use  2nd: flashlight','DEL: journal  CLEAR: pause']
def G_main():
 while True:
  c=home('GHCRYPT','enCRYPTed DEMO',G_RULES,G_KEYS,('Start','Back'))
  if c<0:
   return
  G_play()
G_main()
RAN=True
