# GHCRYPTC: part of GHCRYPT. Keep it next to GHCRYPT.
from ti_draw import*
from ti_system import*
import time
import random
import math
UP=25
DOWN=34
RIGHT=26
OK=105
CLR=45
DEL=23
SECOND=21
BLACK=(0,0,0)
WHITE=(255,255,255)
GREY=(110,110,110)
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
COVER=[0]
TY=6
def _corners(x,y,w,h,r,t):
 if r<=t:
  return((x,y,w,t),(x,y+h-t,w,t),(x,y+t,t,h-2*t),(x+w-t,y+t,t,h-2*t))
 a=min(r//2,2*t)
 return((x+r,y,w-2*r,t),(x+r,y+h-t,w-2*r,t),(x,y+r,t,h-2*r),(x+w-t,y+r,t,h-2*r),(x+a,y+t,r-a,t),(x+w-r,y+t,r-a,t),(x+a,y+h-2*t,r-a,t),(x+w-r,y+h-2*t,r-a,t),(x+t,y+a,t,r-a),(x+w-2*t,y+a,t,r-a),(x+t,y+h-r,t,r-a),(x+w-2*t,y+h-r,t,r-a))
def pause(s):
 time.sleep(s)
I_BLACK=(0,0,0)
I_BG={}
def I_c_(c):
 col(c)
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
try:
 from time import monotonic as G_now
except Exception:
 G_now=None
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
class G_St:
 pass
def G_clock():
 return G_now()if G_now else 0
def G_lq(k):
 return int(k*5+0.5)/5
G_YS=[]
G_YG=4
G_INSIDE=(36,36,44)
G_RULES="Explore Ashgrove Manor, solve Ivy's codes and hide from Ysolde when the lights stutter."
G_KEYS=['Up/Down: start walking','Press the other one to stop','Left/Right: turn a step','ENTER: use  2nd: flashlight','DEL: journal  CLEAR: pause']
