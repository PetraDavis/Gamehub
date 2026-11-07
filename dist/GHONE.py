# GHONE - all of GAMEHUB in one file (test). Run this file.
from ti_draw import*
from ti_system import*
import time
import random
import math
from ti_system import store_list,recall_list
import sys
import gc
UP=25
DOWN=34
LEFT=24
RIGHT=26
OK=105
CLR=45
DEL=23
SECOND=21
NUMS={102:0,92:1,93:2,94:3,82:4,83:5,84:6,72:7,73:8,74:9}
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
GREY=(110,110,110)
DARK=(40,40,40)
RED=(220,50,50)
GREEN=(50,190,80)
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
def shuffle(a):
 for i in range(len(a)-1,0,-1):
  j=random.randint(0,i)
  a[i],a[j]=(a[j],a[i])
def sample(seq,k):
 a=list(seq)
 shuffle(a)
 return a[:k]
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
def dk(c,k=0.65):
 return(int(c[0]*k),int(c[1]*k),int(c[2]*k))
def ring(x,y,r,c,t=2,inner=BLACK):
 col(c)
 fill_circle(x,y,r)
 col(inner)
 fill_circle(x,y,r-t)
def rrect(x,y,w,h,r,c):
 if w<2*r+1 or h<2*r+1:
  r=max(0,min(w,h)//2-1)
 col(c)
 if w-2*r>=1:
  fr(x+r,y,w-2*r,h)
 if h-2*r>=1:
  fr(x,y+r,w,h-2*r)
 if r<1:
  return
 fill_circle(x+r,y+r,r)
 fill_circle(x+w-r-1,y+r,r)
 fill_circle(x+r,y+h-r-1,r)
 fill_circle(x+w-r-1,y+h-r-1,r)
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
def halo(x,y,r,c,t=2):
 col(c)
 for i in range(t):
  draw_circle(x,y,r-i)
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
I_WHITE=(255,255,255)
I_INK=(20,20,20)
I_RED=(215,40,40)
I_GOLD=(230,180,40)
I_BG={'GHSOLI':(25,110,55),'GHBLOCKS':(40,30,90),'GHSUDOKU':I_WHITE,'GHANIM':I_WHITE,'GHFLAP':(110,195,240),'GHTTT':I_WHITE,'GHPONG':(30,85,165),'GHBREAK':(30,70,170),'GHHANG':I_WHITE}
def I_c_(c):
 set_color(c[0],c[1],c[2])
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_line(x1,y1,x2,y2,c,t=1):
 I_c_(c)
 for o in range(t):
  draw_line(int(x1)+o,int(y1),int(x2)+o,int(y2))
def I_hline(x1,x2,y,c,t=1):
 I_c_(c)
 for o in range(t):
  draw_line(int(x1),int(y)+o,int(x2),int(y)+o)
def I_circ(x,y,r,c):
 I_c_(c)
 fill_circle(int(x),int(y),int(r))
def I_poly(xs,ys,c):
 I_c_(c)
 fill_poly([int(v)for v in xs],[int(v)for v in ys])
def I_rr(x,y,w,h,r,c):
 I_c_(c)
 fill_rect(x+r-1,y-1,w-2*r+1,h+1)
 fill_rect(x-1,y+r-1,w+1,h-2*r+1)
 for cx in(x+r,x+w-r-1):
  for cy in(y+r,y+h-r-1):
   fill_circle(cx,cy,r)
I_FONT7={'1':'00100011000010000100001000010001110','3':'11110000010000101110000010000111110','5':'11111100001111000001000011000101110','7':'11111000010001000100010000100001000','9':'01110100011000101111000010001001100'}
def I_digit7(x,y,ch,c):
 I_c_(c)
 bits=I_FONT7[ch]
 for r in range(7):
  row=bits[r*5:r*5+5]
  k=0
  while k<5:
   if row[k]=='1':
    e=k
    while e+1<5 and row[e+1]=='1':
     e+=1
    draw_line(x+k,y+r,x+e,y+r)
    k=e+1
   else:
    k+=1
def I_bevel(x,y,s,c):
 lt=tuple((min(255,v+70)for v in c))
 dk=tuple((v//2 for v in c))
 I_box(x,y,s,s,c)
 I_hline(x,x+s-1,y,lt)
 I_line(x,y,x,y+s-1,lt)
 I_hline(x,x+s-1,y+s-1,dk)
 I_line(x+s-1,y,x+s-1,y+s-1,dk)
def I_ground(x,y,top,c,r=24):
 a=math.asin(top/r)
 xs=[]
 ys=[]
 for i in range(13):
  t=a+(math.pi-2*a)*i/12
  xs.append(x+r*math.cos(t))
  ys.append(y+r*math.sin(t))
 I_poly(xs,ys,c)
def I_heart(x,y,s,c):
 I_circ(x-s,y-1,s,c)
 I_circ(x+s,y-1,s,c)
 I_poly([x-2*s,x+2*s+1,x],[y,y,y+2*s+1],c)
def I_diamond(x,y,s,c):
 I_poly([x,x+s+1,x,x-s-1],[y-2*s,y,y+2*s,y],c)
def I_spade(x,y,s,c):
 I_circ(x-s,y+1,s,c)
 I_circ(x+s,y+1,s,c)
 I_poly([x-2*s,x+2*s+1,x],[y+1,y+1,y-2*s-1],c)
 I_poly([x,x-s,x+s],[y+1,y+2*s+1,y+2*s+1],c)
def I_solitaire(x,y,c):
 suits=((I_spade,I_INK),(I_diamond,I_RED),(I_heart,I_RED))
 for i in range(3):
  l=x-18+i*10
  t=y-12
  I_box(l-1,t-1,18,26,I_INK)
  I_box(l,t,16,24,(250,250,245))
  f,col=suits[i]
  f(l+4,t+5,2,col)
 I_heart(x+10,y+3,3,I_RED)
def I_blocks(x,y,c):
 s=8
 cells=((-2,1,(220,70,70)),(-1,1,(220,70,70)),(0,1,(70,110,220)),(1,1,(70,110,220)),(-2,0,(80,190,90)),(0,0,(70,110,220)),(1,0,(230,200,60)),(-2,-1,(80,190,90)),(1,-1,(230,200,60)),(-1,-3,(170,90,210)),(0,-3,(170,90,210)),(0,-2,(170,90,210)))
 for cx,cy,col in cells:
  I_bevel(x+cx*s,y+cy*s+2,s,col)
def I_sudoku(x,y,c):
 s=11
 x0=x-16
 y0=y-16
 I_box(x0+s+1,y0+1,s-1,s-1,(250,225,140))
 nums=('53 ',' 7 ','1 9')
 for r in range(3):
  for k in range(3):
   ch=nums[r][k]
   if ch!=' ':
    I_digit7(x0+k*s+3,y0+r*s+2,ch,I_INK if(r,k)!=(1,1)else(40,90,200))
 for i in(1,2):
  I_line(x0+i*s,y0,x0+i*s,y0+3*s,I_INK)
  I_hline(x0,x0+3*s,y0+i*s,I_INK)
 I_c_(I_INK)
 for o in(0,1):
  draw_rect(x0-o-1,y0-o-1,3*s+2*o+1,3*s+2*o+1)
def I_anim(x,y,c):
 I_box(x-20,y-13,41,27,(35,35,40))
 for i in range(5):
  I_box(x-18+i*8,y-11,4,3,I_WHITE)
  I_box(x-18+i*8,y+9,4,3,I_WHITE)
 for i,by in enumerate((4,-2,2)):
  fx=x-17+i*12
  I_box(fx,y-6,11,13,(120,200,240))
  I_box(fx,y+4,11,3,(70,170,80))
  I_circ(fx+5,y+by,2,(240,120,40))
 I_circ(x+17,y-9,1,I_RED)
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
def I_ttt(x,y,c):
 s=12
 for i in(-1,1):
  I_box(x+i*6-1,y-18,2,36,I_INK)
  I_box(x-18,y+i*6-1,36,2,I_INK)
 for i in(-1,0,1):
  cx=x+i*s
  cy=y+i*s
  I_line(cx-4,cy-4,cx+3,cy+3,I_INK,2)
  I_line(cx+3,cy-4,cx-4,cy+3,I_INK,2)
def I_pong(x,y,c):
 I_c_(I_WHITE)
 draw_rect(x-22,y-16,44,32)
 I_hline(x-21,x+21,y,(200,210,230))
 for i in range(6):
  I_box(x,y-15+i*6,2,3,I_WHITE)
 I_box(x-17,y-11,4,14,I_WHITE)
 I_box(x+14,y-3,4,14,I_WHITE)
 I_circ(x-6,y-5,2,(250,150,40))
def I_breakout(x,y,c):
 cols=((220,60,60),(235,140,50),(230,210,60),(70,190,90))
 for r in range(3):
  for i in range(4):
   bx=x-19+i*10
   I_box(bx,y-15+r*6,9,5,cols[(i+r)%4])
   I_hline(bx,bx+8,y-15+r*6,tuple((min(255,v+60)for v in cols[(i+r)%4])))
 for i,(dx,dy)in enumerate(((-8,12),(-5,8))):
  I_box(x+dx,y+dy,2,2,(120,150,230))
 I_circ(x-1,y+5,2,I_WHITE)
 I_rr(x-11,y+13,22,4,1,I_WHITE)
def I_rpg(x,y,c):
 I_circ(x-5,y-8,6,(240,200,160))
 I_box(x-11,y-15,13,5,(110,70,30))
 I_box(x-11,y-11,3,5,(110,70,30))
 I_box(x-8,y-9,2,2,I_BLACK)
 I_box(x-3,y-9,2,2,I_BLACK)
 I_box(x-11,y-1,13,12,(60,120,230))
 I_box(x-11,y+5,13,2,(110,70,30))
 I_box(x-14,y,3,8,(240,200,160))
 I_box(x-10,y+11,4,6,(60,40,30))
 I_box(x-4,y+11,4,6,(60,40,30))
 I_box(x+2,y+1,4,3,(240,200,160))
 I_box(x+2,y-23,12,26,(15,45,70))
 I_box(x+4,y-22,8,24,(40,110,170))
 I_box(x+5,y-21,6,22,(100,200,245))
 I_box(x+7,y-21,2,21,(240,252,255))
 I_box(x+3,y+1,10,2,I_GOLD)
 I_box(x+7,y+3,2,5,(120,80,40))
 for sx,sy in((x+16,y-18),(x+1,y-14),(x+15,y-6)):
  I_box(sx,sy,2,2,(200,240,255))
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
def I_hangman(x,y,c):
 I_box(x-19,y+15,24,3,I_INK)
 I_box(x-13,y-18,3,34,I_INK)
 I_box(x-13,y-18,24,3,I_INK)
 I_line(x-11,y-9,x-3,y-17,I_INK,2)
 I_box(x+8,y-16,2,6,(140,90,40))
 I_circ(x+9,y-6,4,I_INK)
 I_circ(x+9,y-6,2,I_WHITE)
 I_line(x+9,y-2,x+9,y+7,I_INK,2)
 I_line(x+9,y+1,x+4,y+5,I_INK)
 I_line(x+10,y+1,x+15,y+5,I_INK)
 I_line(x+9,y+7,x+5,y+13,I_INK)
 I_line(x+10,y+7,x+14,y+13,I_INK)
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
def I_keys(x,y,c):
 for i in range(3):
  for j in range(3):
   I_box(x-14+j*10,y-12+i*9,8,7,c)
def I_wipe(x,y,c):
 I_box(x-10,y-8,20,22,c)
 I_box(x-13,y-13,26,3,c)
 I_box(x-4,y-16,8,3,c)
 for i in(-5,0,5):
  I_box(x+i-1,y-4,2,15,(0,0,0))
def I_about(x,y,c):
 I_c_(c)
 fill_circle(x,y-10,3)
 fill_rect(x-3,y-5,6,19)
I_ICONS={'GHSOLI':I_solitaire,'GHBLOCKS':I_blocks,'GHSUDOKU':I_sudoku,'GHANIM':I_anim,'GHFLAP':I_flap,'GHTTT':I_ttt,'GHPONG':I_pong,'GHBREAK':I_breakout,'GHRPG':I_rpg,'GHSIMON':I_simon,'GHHANG':I_hangman,'GHCRYPT':I_crypt,'*keys':I_keys,'*wipe':I_wipe,'*about':I_about}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
S_SLOTS=3
S_PER=100
S_B=5
def S_hname(s):
 return 'A'+str(s)+'H'
def S_dname(s,i):
 n=str(i)
 return 'A'+str(s)+'0'*(3-len(n))+n
def S_info(s):
 try:
  h=recall_list(S_hname(s))
  if len(h)>=4 and int(h[0])==1:
   return(int(h[1]),int(h[2]))
 except Exception:
  pass
 return None
def S_save(s,data,frames,fps,show=None):
 nums=[]
 n=len(data)
 i=0
 while i<n:
  v=0
  for j in range(S_B):
   v=v*256+(data[i+j]if i+j<n else 0)
  nums.append(v)
  i+=S_B
 nl=(len(nums)+S_PER-1)//S_PER
 for k in range(nl):
  if show:
   show(k,nl)
  store_list(S_dname(s,k),nums[k*S_PER:(k+1)*S_PER])
 old=0
 try:
  old=int(recall_list(S_hname(s))[3])
 except Exception:
  pass
 for k in range(nl,old):
  try:
   store_list(S_dname(s,k),[0])
  except Exception:
   pass
 store_list(S_hname(s),[1,frames,fps,nl,n])
 return nl
def S_load(s,show=None):
 h=recall_list(S_hname(s))
 frames,fps,nl,n=(int(h[1]),int(h[2]),int(h[3]),int(h[4]))
 data=bytearray(n)
 p=0
 for k in range(nl):
  if show:
   show(k,nl)
  for v in recall_list(S_dname(s,k)):
   v=int(v)
   chunk=[]
   for j in range(S_B):
    chunk.append(v%256)
    v//=256
   for j in range(S_B-1,-1,-1):
    if p<n:
     data[p]=chunk[j]
     p+=1
 return(data,frames,fps)
def S_wipe():
 n=0
 for s in range(1,S_SLOTS+1):
  try:
   h=recall_list(S_hname(s))
   nl=int(h[3])
  except Exception:
   continue
  for k in range(nl):
   try:
    store_list(S_dname(s,k),[0])
    n+=1
   except Exception:
    pass
  store_list(S_hname(s),[0])
  n+=1
 return n
H_CATS=[('Arcade',[('Wing It','GHFLAP'),('Pong','GHPONG'),('Breakout','GHBREAK')]),('Puzzle',[('Stack Drop','GHBLOCKS'),('Sudoku','GHSUDOKU'),('Simon','GHSIMON')]),('Classics',[('Solitaire','GHSOLI'),('Tic-Tac-Toe','GHTTT'),('Hangman','GHHANG')]),('Adventure',[('Tiny Quest','GHRPG'),('Encrypted Demo','GHCRYPT')]),('Create',[('Animation Studio','GHANIM')]),('Settings',[('Key Test','*keys'),('Delete All Saves','*wipe'),('About','*about')])]
H_BAR_Y=34
H_BAR_H=22
H_BAR_GAP=27
def H_header():
 cls()
 ctext(22,'GAMEHUB',WHITE)
def H_draw_bar(i,on,first=False):
 y=H_BAR_Y+i*H_BAR_GAP
 c=GOLD if on else WHITE
 if first:
  rbox(50,y,220,H_BAR_H,9,c,2,BLACK,False)
 else:
  edge(50,y,220,H_BAR_H,9,c)
 ctext(y+17,H_CATS[i][0],c)
def H_cat_screen(sel):
 H_header()
 for i in range(len(H_CATS)):
  H_draw_bar(i,i==sel,True)
 while True:
  k=wkey()
  old=sel
  if k==UP:
   sel=(sel-1)%len(H_CATS)
  elif k==DOWN:
   sel=(sel+1)%len(H_CATS)
  elif k==OK or k==RIGHT:
   return sel
  elif k==CLR:
   return-1
  if sel!=old:
   H_draw_bar(old,False)
   H_draw_bar(sel,True)
def H_app_pos(i):
 return(50+i%4*73,82+i//4*70)
def H_draw_app(app,i,on,first=False):
 x,y=H_app_pos(i)
 c=GOLD if on else WHITE
 if first:
  try:
   circ(x,y,26,I_bg(app[1]))
   I_draw(app[1],x,y,WHITE)
  except Exception:
   ctext(y+7,app[0][0],WHITE,x)
 halo(x,y,27,c,3)
def H_show_title(name,old=None):
 if old:
  ctext(203,old,BLACK)
 ctext(203,name,GOLD)
def H_app_screen(ci,sel=0):
 cname,apps=H_CATS[ci]
 cls()
 rbox(90,8,140,24,9,WHITE,2,BLACK,False)
 ctext(26,cname,WHITE)
 for i in range(len(apps)):
  H_draw_app(apps[i],i,i==sel,True)
 H_show_title(apps[sel][0])
 n=len(apps)
 while True:
  k=wkey()
  old=sel
  if k==LEFT:
   sel=(sel-1)%n
  elif k==RIGHT:
   sel=(sel+1)%n
  elif k==UP and sel>=4:
   sel-=4
  elif k==DOWN and sel+4<n:
   sel+=4
  elif k==OK:
   return sel
  elif k==CLR:
   return-1
  if sel!=old:
   H_draw_app(apps[old],old,False)
   H_draw_app(apps[sel],sel,True)
   H_show_title(apps[sel][0],apps[old][0])
H_ALPH=''.join((chr(c)for c in range(35,127)if c not in(39,92,96)))
def H_unpack(s):
 out=bytearray()
 i=0
 n=len(s)
 nb=len(H_ALPH)
 while i<n:
  j=s.find('`',i)
  if j<0:
   j=n
  out.extend(s[i:j].encode())
  i=j
  if i<n:
   o=H_ALPH.find(s[i+1])*nb+H_ALPH.find(s[i+2])+1
   st=len(out)-o
   for k in range(H_ALPH.find(s[i+3])+4):
    out.append(out[st+k])
   i+=4
 return bytes(out).decode()
def H_run_app(mod):
 if mod=='*keys':
  return H_key_test()
 if mod=='*wipe':
  return H_wipe()
 if mod=='*about':
  cls()
  message(['Game center for the','TI-84 Evo.','CLEAR goes back.'],'GAMEHUB')
  return
 gc.collect()
 try:
  src=GAMESRC[mod]
 except Exception:
  src=None
 if src:
  try:
   ns=dict(globals())
   src=H_unpack(src)
   gc.collect()
   exec(src,ns)
  except Exception as e:
   cls()
   message([str(e)[:26]],'Could not run')
  ns=None
  src=None
  gc.collect()
  return
 try:
  m=__import__(mod)
  if not getattr(m,'RAN',False):
   m.main()
 except Exception as e:
  cls()
  message([str(e)[:26],'Is '+mod+' on the','calculator?'],'Could not run')
 try:
  del sys.modules[mod]
 except Exception:
  pass
 m=None
 gc.collect()
def H_key_test():
 cls()
 ctext(30,'KEY TEST',GOLD)
 ctext(60,'Press any key to see')
 ctext(80,'its code. CLEAR twice')
 ctext(100,'in a row to leave.')
 last=0
 while True:
  k=wkey()
  rect(60,120,200,40,BLACK)
  ctext(150,'Code: '+str(k),WHITE)
  if k==CLR and last==CLR:
   return
  last=k
def H_wipe():
 cls()
 ctext(40,'DELETE ALL SAVES',GOLD)
 ctext(70,'This erases every')
 ctext(90,'Animation Studio')
 ctext(110,'animation.')
 ctext(150,'ENTER: delete',RED)
 ctext(175,'CLEAR: keep them')
 if wkey()!=OK:
  return
 n=0
 try:
  n=S_wipe()
 except Exception:
  pass
 cls()
 message([str(n)+' save lists cleared.'],'Done')
def H_main():
 ci=0
 while True:
  ci=H_cat_screen(ci)
  if ci<0:
   cls()
   return
  ai=0
  while True:
   ai=H_app_screen(ci,ai)
   if ai<0:
    break
   H_run_app(H_CATS[ci][1][ai][1])
GAMESRC={}
GAMESRC['GHANIM']=r'''a_CWD=32
a_CHG=24
a_N=`#9$*`#6$
a_P=6
a_CX`#*%Y=26
a_PAL=((255,`#&&),(0,0,0),(128,`#&&),(200,`#&&),(220,40,4`#/$45,140,3`#0$50,220,50),(60,190,7`#<$0,10`#U&8`#p&`#U$40,`#3%`#H%30,9`$H$50,`#e%`$-+`#1%13`#V$`$G)200,160))
a_COL=`%H$+tuple((((r+1020)//5,(g`#/+b`#/))for r,g,b in `#d$`#r$INK=(20,`#%$)
a_HI=`%|$120,`#4$MAXB=60000
a_KEYGAP=15
def a_enc_key(fr):
 out=bytearray([1])
 i=0
 while i<a_N:
  c=fr[i]
  n=1
 `#B(+n<a_N and fr[i+n]==c and(n<255):
   n+`#V$out.append(n)`#3.c)
  i+=n
 return bytes(out)`%(+delta(prev,`%/50])
 pos=0`%66if`$r$]==prev[i]`$k$i`$k% continue
  j=i
  last`#,$`#l%j`%])j-i<254`#c%`#y$j]!`#y%j`#y% j`#z&`#j%j
   elif j+1`&J,j+1`#^)+1`#a/else`#5%break`$d$last
  skip=i-pos`$k)skip>255`#U$`&v+255)`#6/0`#4$skip-=255`(K.skip`(_/j-i)
  `&$,t<j`$3$hi=fr[t]
   lo`#/$+1]if t+1<j`%4$ 0`$I/hi*16+lo`$P$t+=2
 `(w$j
  i=j`)l:apply(fr,d):
 if d[0]==1:
  p`&L$`)]$`$o&p<len(`#N$  n=d[p`$r$c=d[p+1`#/$for t in range(n`#O%`,%%t]=c`*,&n
   p`$u%`$h%
`$:%`*{&L=`$4%`+$(p<L`$^$os+`$A(`$J$`$@%`#n&`$F6b`#K$t//2`$m%r[pos+t]=b>>4 if t%2==0`&s%b&15`#v%(n+1)//`&d&+=n
class a_Studio:
 pass`&b&dec(s,i):
 k=i`%&(k>0`+K$s.F[k][0]!`&t%k-=1
 fr`-n+a_N)
`%3$j`%3*k,i+1`%7$`(k+s.F[j])`):)fr`$N&chain`$P(n=0`$UK`0H&`#w&n`/s*ode_at(s,i,fr,prev`*5&prev is Non`-T$`#_&`2R-
 d=`0_4`#f$i`$[&`%)+-1)+1>=`3M(`#|:`#9&d`%l(ommit(s`$g&not s.dirty`#h*
 i=s.ci
 nx=None`$O%+1`,.$s.F)`&6(i+1]`,b$0:
  nx=`)D)+1)
`#F%]`%I%`&6+s.cur,s.prv`%O(`*_$None`%d%nx is`$i$`&L(`$8(`&=-`#n%nx`$5$`%6$=False`%^&used`%[%t=0`*>%f in s.F:
`/L$len(f)+2`&?)t`#_&wan`$x$):
 v=`$2$`6c$if v==`*,(onion`6Q$s.ci>0`&0&pr`4s(`#{&16+`#9(`$4)v`$4&pai`$5%,`*<$x=a_CX+i%`<v(P
 y=a_CY+i//`#8+rect(x,y,a_P`#&&COL[v]`&$$shown[i]=`$1(refresh(s,src`);$`&0%src if `#*$`(1*`/1&`7f*`&*+for i`-|*a_N)`$>$h=`$A&
 hb=s.hide`$$$`#-$>`&M(h[`#4%]==t`#.(else-1
 todo={}`(l%`$./:
  v=t`;*%if sh`8|$v`1V$`8n+r=`&@(`;]$i-r*`#1(e`;b+c+e<`#;$`$b$t[i+e]==v`)3$i+e!=hb`2X%e`8>%n=e`#a)n>1`%=(i+n-1`$Q)n`/s%best`-:&`%;$w in(e,n)if n<`&w%(e,`$*%h`9D%`$#%r+h<`BQ$`9c&=i+h`%0)  k`6A$`#P(k<w`%.&j+k`%.)j+k`%.*  k`;.(if k<w`#9&`:O(  h`#C&g`$$%for q`(8*h`#l&j=i+q`$S+for k`#J*w`$8(`(W%j+k]!`&+&   g`$-&if`&2$`2O( or g>best[0`<F&`&Q$(g,w,h)
  `#,$=be`<?$`$f6`$e/`$d7`$_&=v`*H%v in`*{$`#A$todo[v]`;C((c,r`$K$)
`=x+`#H&=[`#B)]`+Z%`#q-for `#C&`#:([v`%M%`.X$`/+$c*`.W&Y+r`#.$w`#)$h`#:(`.p&`4B&ursor`1e%`/m&s.cx`/j-s.cy`#4%`1H(`#5&CWD`#Q$]
 col(BLACK`%s((0,3,6,15)`/;$WHITE)
 draw_`0R,-2`#)%`0M$hide=`$&/`3X(n`$w,`5|$`#I-`#c(-1
`2:-`0P+`%g(label(s,key,x,y,t,c,bg=`$o%:
 old=s.lab.get(key`$h$lab[key]=(t,c`6&%old`9M,tex`%H%`#D%`7w)o,oc=old
 n=max(len(o),len(t))
 o=o+' '*(n-`#>%)
 t2=t`#8,`#L$segs=[`*%&`+;+`>x%if o[k]!=t2[k]or(oc!`HM% `#5$!=' '`+g%if`#q$`#?$k-segs[-1][1]<=2`,-&`#7*=k+`EZ/segs`,*([k,k+`JE$rub=[g`$h$g`85$egs`$a%g[0]:g[1]].strip(`,8(a`L8%rub`7U%ct(x+a*10,y-12,(b-a)*10,16,bg`?S&`#W&segs:
  w=t2[a:b`4I&w`$,(`-X%`(Q$`#w&,w,c`)k(swatch(s,c,sel=-`@@$x=210+c%4*26
 y=30+c//`#1%e=`M~$ if c==sel`7J%GOLD`#7(.co`#9&`*W$`8s(-2,y-2,26,2,e`>I$`#9(+2`#:5,2,2`#7,+2`#8,`:R(lette`,j%`/h$`)v*16`%p$`%?.`%@/`$$(1,y+1`PB%,`PZ$[c])`.y%GREY`.Z-21`RN$`Pq&`&^,`%n$`$g(topba`.P&pct=`>@)*100//`Q=%
`.0+'fr',4,17,'Frame '+str`=f$+1)+'/`#3%`A)(),`(I$`$L$`#h*ps',160,17,`#b%fps)+`#;%`%;&`#R+mem',236`$?$Mem`$=&pct)+'%',RE`)<$pct>9`AJ&`#j%`%T%bot`%T$,a`9]$,b`=d)if a`/e,a=('Pen up','PEN DOWN','ERASER')[s.pen]
  ca=a_HI`=C%pen`$@%`%]$
`.#)`#H&`%=-b1',6`W[$a,ca`%Y.b2',6,206,b or 'ENTER pen DEL eraser 2nd menu`&A(`-#&id`*n&`6;&MX,22,320-`#/$154,`4j(`2t%pop('on',`Dl&`#9+sv`#9)`+r,`*R$ide`.P$s`$D,`#5&:`%?-on',210,150,'O`Cy$'+`$=$`&M$`D0%`&O$'off')`)a3sv`#h&68,'Saved '+(`*?%slot)`#o$slot`#n&-`#l)`$i%full`$e%cls(`%t(`9S)`7V$CY`#*%`DM%+4,2,DARK`#K3+`?L$`9q(`#SB,`#*$`#U&`#G0+`#h)`#O9`DD&`Nv1`8m+`(w$`D&$`F$+`(k)`#.&`/4)
`,k+`#0$`9})`:4(pda`1F(`:B-`$*2`#z-`*#,`$.@set_px`:m$c`..&`J>(!=c`8J&`Mm/ s.undo`%}+`#V$)`LE$`#a%`U:$`L2(Tr`FN$s.changed`#4%`)|&i`)|(i0`<e2`;t%`#x$0]
 new`5g%`;h(==ne`D:$`;S(`$f9stack=`#l%`Zt&tack`%R$=`#.$`-r$`_h$`%v,old`Hf0`%U)new`5h$`LK&`#_%x>`PF$`$)%`:h(i-1`$#&x`Hz%-`T&$`#H/`Pp$`PL%`h<%`#n4`#<$`#K(<a_N`#5%`#t4`#N(`(G.`(F5go(s,j`*x%`SR)`($$j`9v$i+`$}$`OY$`(Q%`%|(`(+-prv)`WM+`Rs(`WP&`3x(`#[%`SZ(j`*E%prv`#6*-1)if j`SH(`-w2c`^a$`)T&`Kd$`^Y&dd_frame(s,blank`6:(`8z(>`8u%:
  message(['Memory is full.'`2#%, or delete `#y$s.'],"Can't add"`%*%broke`,?(`+<(`&_.`Vt*`VD,`Vz/`V&)`,C%`%g.if `%@$`&(0`,:).F.insert(i+1,`VI3ew)`W&4`[P)i+2`X=+`#5(`W:-new`W8(`)o+`)4%`,i$`(W$i+`2O$`*t3del`(](`(V&`%o(`d>&`0O?`3i1`0Y0`[%3`(0Fp`#K*`+/%`ZT-
 del`[4&`Za<`&F(key(nx)if p`P&)`<^&`_=+`&e%`/>%`$^(`1-%`#1(`64%`[?,`&|&`(4(`dD*`(S(`%88`-D3`(a2play`6O(`+u+`6]1`@*)'Playing. Up/Down: speed','Any other key stops'`qP(`en3`4%%Tru`&h$`3p$F[i`+E%1 or i`+M&`#b4`f80i]`#8%`[[*`c[$`D:B`D7? steps`Mk$1,12//`D-%`#<$op`(d(`U&0`#X$`J@%k=key`6E$`WZ$==UP`.)&fps<1`L|(.fps`X)(`:X-`q9&k==DOW`q9%`#P$>`6/%`#0%`ZD%`#^7`N?%`+q$in(UP,DOW`]l%`%6&`-L&`Y<+pause(1/12`8L(top`#U$`#F(i=`&R$%`&J(`j*)ey`M.%`l-$`+j/s.ci`*l%`=X(
a_ITEMS=('Color','Fill area','Undo','Wip`3}&','Next`#0)Prev`#0)Add copy`#.&`3)$','Del`#S*lay','S`+h&`Cs%skin`5:&','Load`$1$w','Quit'`z3$X=202
a_MY`~E%MH=25
a_MV`~7$MW=108
a_SBX=a_MX+a_MW+4`#5$H=a_MV*a_MH-3
a_THH=`#;$*a_MV//16`LG(humb_y(top`GB%`ki&MY+(`#T$-`#b$)*top//(16-a_MV`@?)crollbar(top,old`JT,`V=/`Cd&SBX,a_MY,5,`$*$`CU(`*G$`?-$`)a&`3S(`:M(a,b=(`$}*old),`%1.)
  vacate`$2(`$-$X,b`$7$TH`$7)`#J.b`#J&a`#J)`G.(`$O)`%.-`$>,`#V0`&0%mbox`Xy$w,h`CN%`RN(,y,w-4,2`Y6$`#8*+h-2`#<1,y+2,2,h-4`#Q,w`Sg%`#<*`$=&rows(s,top,sel):
 boxe`YD%`Wc$]
 word`YV*r`i7,MV`5R&top+r`S[$`)n$r`*R$`h|$`Ug(i`U{+`Ue&`39%`]<(('mb',r))`F.&`$T%`cM+y`(m$`]_&`#P%`Ey%`^+.('m`#l$`|8$`.c&`k#)old!`^<%`[5(old`0s$old`u_$t`0k%rub`$E)y`^%$`#D%)`$O%`&,$`$h,,`]w$`$j*`$i$`_L&`%:%sort(`ZJ&c,y in`#<%`+[$`)e%`.:$1`c/$MW,2`)=%for y,n`[U0`#O$5,y+4,n`[P&`d>$)`(r&`$:0,`{L$`#>$`aw)`#i)16`b#%`)~&enu(s`)y(`RM:`$:(`*#8`RO*`)B(`RS(`#>.`#=,`:@,MENU `:=*pick',`Tb%: do it  2nd: close')
 top=min(max(0,sel-2),`0x)`,L3`Mx$`1.,`:p1k=w`8I(`*w$el`*W%`8R$`H|%el=(sel-1)%16`k#$`89*`#E-+`#E. in(LEFT,RIGHT`+F%`#N)8`#r/OK`7c-`#g*CLR,SECOND`#g*-`9>$`#O(nt=top`-t&el<`8T(nt`%@&`#r$sel>`.s$a_MV`#C+`&U$`ei$`&C,nt,`&F%`(3$nt`+{%`&x4`S+*`Qn+`5o&sel`@H(ick_col`k0(sel`P&(`a2,el`#~)`*5*Arrows`*.% a colour`*7*use`*8$CLEAR: back'`)MLLEFT`)O>`)%$`)P<`*924`*9A`#E0`)i&`SD&ol`0g%col`$y&`&@,old`1,$`*;.==CLR`>8.`)^$`Rr*`#h.`(*&`#:-`(A,`#8,`ex5`)Z-`)N+`E4$`[u*)
 c`1.$80,'PLAYBACK SPEED',GOLD`#D)140`)=& done`e@)`Z;*`)<.t='<`f[)`ey%`Ob& a second >'`E*.sp`fV$`oc&*5,110,t`:(%`28)`*=,`*3*`CS1`CR+`*9-`D_2`D^+`/+*OK,CLR`/&%`;{&`&_,lot(titl`>U$opt`9}*sl`k_+,S_SLOTS+`n)$ inf=S_info(s`)E$opt`7S)'Slot`&J(l)+(':`G{(nf[0]`&Y%'if inf`c:&: empty'`sR$`#q,Cancel')
 c=choose`${%,opt`W+&c<0 or c==`$q&`@,* 0`/y)c+1`%l(rogress(k,`s~$`7$$60,1`m3$`m=$`(d(rbox`#>,16,6`?f)`#[%4,124,max(2,192*(k+1)//n),8`+,&`RC&o_sav`b6)`Me+sl=`(M,'SAVE TO`M2$`a=&l`BM,`,J-100`E{$ing...`,F)data`M++`97&f`s~$.F:
 `#E$`($(len(f)//256)`#>5%`#=,extend(f)
 tr`b{$S`%L&l,data`=]$s.F),`+E$,`(1*`:3%slot=sl`b|-`M?(`Ym)`N,-`-v*sav`Ho$to `id$`*u*'.']`j7&')
 except E`#*$ion as `.z$`Zv*Could`&z%ave:'`q.$e)[:24]],'Error'`)$+loa`0j&`(s0LOAD FROM`(u- or`#-$`-+*`),,`cw%`%r%`.v$`$e*Un`%X$ `#A%s will','be lost. `6w&l`KR%`6v&c`-+%]`Kl%?')!`5(&`*D:Load`*E/`)7&`)-$`(2%,fps=S`%p&l`)3.`(#Mload`(#9`$s*F`0z$p`Ue$`~V.`$Z%`&^$n=data[p]*256+`#/%+1]
  F`+o(bytes(`#>&2:p+2+n]`De$p+=2+`ag$reset(s,F,`T]%`+P*`)[%`#C.:`a($=F
`3U%=fp`Qv%`W^$`Q~.0`Yj)`YP2`ZN0`,^.`e0,`$Z(0`O$(tudio`S@$s=a_S`#2&`%;,[`]N*`$D.)],6`Zx%x=16`#,$y=12`#,$ol=`]6$pen`%<%`t4$`i()`q(0[255]*`q.;msel=0
`ss*
 held=0
 hc=0`>P2`85.he`J<&`m3$ hc`7[(`Ph%`#i& rep=k!`#Q%or(hc>3`#Y$hc%1==0)
 `$@%`<q&not`#v&`WZ%0.0`l^$`mq,`DT2,`XS(and re`CP%`_+/`:;3c`nB(`#/$`Yk&`:;4c`nL.`#5$`Z{&`@^*`#O(y`#z+y`#z/`[6+cy<`v1$`#y+y`#y&`}%(`#<%`f+$`rI.`?k%`t:*`*+$`#Z)==1`:-%`&x$ `{G$int`#M$a_wa`#.%`NN%`u8,`($1not`&h)`(?/==OK or`%E$EL`#E$want_pen=1`#E*`$Q$2`=j%`+n$`$q+`#S(`#H%`#1(`%su`|O%hown`tR$`%v+`$+%`*72`&01`Hs-`ax1`&41CLR`)L&`%7(`.b)`#q1`#b1`Kx%`&w&`Es(`#e+c=`Q6)m`Ec(if c>`g%&`/)%c`#Y%`q(%`:5(`#K$`gN(`Jz0`+])c`n#& `yd*`#?,2`%L&undo`lO0  u=`#=%`,/&`nh8`nj(u`#/&`n^-`$5)3`,x(`#l@`ig1`#y:4`*e&`:V$`oL,`)u)`x($`#@%`#p%`1t)`jf$`v0+`&r$`&5-5`/.(i`/V(`#u+`zq%`#O)6`#D(`#x>7`#J4Tru`#I.8`#I(`s>,`#D,9`)[)`n~%`)U-`)z.`KI(`&b&`wV-`#W*`1V)`6k%`>i$`#/%`#J-`kx&`D_,`#}>`)[&`@4,`#T>`)8-`:$%`(o&`#V0`@^)`@:)or`@9Rn`ic$`@81New?')`Q<)`pg%`:oF`%>+5`%>)`$udquit`$v4Quit`$w.`@>(`&L3`&q$`#6$`/f)`;S(`%((!`*l*`ne,RULES='Draw a picture, add`F{&,`-/$play them`Vs$. Saves stay on the calculator.'
a_KEYS=[`Wv)move `%f(pen','DEL: eraser`_1&menu','Menu:`XF$rs,`$P)play,','`,S$,`Gb$`$f$`Eg$]`bt(ain`@<$`>0.c=home('GHANIM','ANIMATION STUDIO',`%}&,`%+%,(`p^(B`YU$`>m&c<`.-%`(I)`AW*
`$G('''
GAMESRC['GHBLOCKS']=r'''import random
try:
 from time `#A&monotonic as b_now
except E`#*$ion:
`#<%=None
b_CW=10
b_CH=2`#+$=9
b_OUT=(50,20,70)
b_WELL=(35,30,9`#5$PANEL=(70,35,10`#7$X0=115
b_Y0=22
b_SHAPES=(((0,1),(1`#)$2`#)$3,1)),((0,0`#=$0),`#I+),(`#71`#^%`#W*`#=42`#=9`#s%`#C0`$L0`#W+)
b_COLS=((90,200,22`#h$3`#1%6`#S$70,90,210),(70,11`#J,140,50),(80,19`&S$,(2`&p$,70))
def b_cells(p):
 s,r,x,y=p
 out=[]
 for cx,cy in `&n([s]:
  rx,ry=(`#B$)
  if s!=1:
  `#[$i in range(r)`#9$`#V(2-ry,rx)
  out.append((x+rx,y+ry))
 return out`$u,_i`$w1if r%2==0`$_$`#Y$[(x+i,y+1)`$R/4)]`$#([(x+2,y+i`#G4`$<%get`$8%`$V&`$N,if p[0]==0 else`&c+`#b&ok(b,`#c$for x,`&Z&`#y) if x<0 or x>=b_CW or y`#.$H`&F$`$@&False`#S%y>=0 and b[y][x`(E$`#J/`#1&True`$S&bevel(todo,c):
 lo,hi=(dk(c,0.55),lt`#.$45))`$z%px,p`$|$todo`&q%ct(`#9$,b_C`#&$lo`#PF-1`#)&hi`#T?+1,py+`#R%2`#)&c)
class b_Well:
 def __init__(self`&g$self.s=[[0]*`&f$`);/b_CH)]`#L(las`,:%def show`#n$,b,p,full=`&f$`#}$new=[c`,d%`)&,if c[1]>=0]if p`)l$[]`(g%fu`$u$  `)z$=[(x,y`*t$`%h$`$Z+`*%$`#7-W`$p$else`#f+`%#)+new`%4-`#3%v=p[0]+1 `$T) 0
  ch={}
`.4%`%-$`#s$`#}$x,y=c
   w=v if`#B%new`,%&`*l%
 `.~%`&t$`#6%!=w`.s%`#8,=w`#6$ch[c`#/%run`4w%`$F%`%i0`/r)`%n/+1`/w&e=x<`)*$and ch.get(`&]$)==0`#E$if e`#A$run is Non`&I%`$G%x`#l%lif not`#N.not`#R-ect(b_X0+run*`,7%Y0+y`#.$(x-run)`#:&C,`6n%)`$3*`%W+w`%>*1,8`%;%todo=[`$)%x`$&/)for`%F$,u`([$h.items()if u==w`(>(`-%( `.u.`5X%[w-1]`0j(side(score,lines,nxt,old):`2k$old`&C,`(Y$,h in((26,64),(96,4`69$42,40)`%6%rbox(226,y,88,h,6,(15`6M%190),2,`9h&)
  text(234,44,'NEXT',(200,185,230)`#G-114,'SCORE`#I=60,'LINES`#I3old=(None,`#())`%a$nxt!=old[2`73%ect(2`8@$,40,2`%%-`&s([(244+x*9,54+y*9`.I%`4L,(nxt,0,0,0))]`(C(nxt]`$?%`(<$`$A%0`$A$`(6%[0]`+-0`%O*31,str(`#J%)`&f5`#G(`$)$)`$5%`)H$`$5%1`$5,1`$5;77`$5)1`$58`#G&`$)$`9]*`*f0`+&(game():
 b`3hBcls(`@D$`5@&`#F+`=5$,30`+$$`(l$0,i,320,15,(58,25,8`)W$`+A$b_X0-4`-N$`#*$CW*b_C+8,b_CH`#.&4,WHITE`+R$`._&well=`6(%(`#p(4,26,96,56,6,GOLD`,*-`&/$14,48,'STACK'`#G$`#=+68,'DROP`#<)`%K$,c`3=$enumerat`%w$OLS[:5]`%T*12+i*1`$H$11,11,cc`$b*150,`.7$`-s=`$P%2,167,'2nd key:`-(2`#J)84,'drop it`#I2`)I$=0
`*j%=0
 nxt=`FE%.randint(0,6)
 p`2>&t=0
 held`#+$c=0
 sd=`1(7`.E&`7@$`FW$`20$`#-$`7<)while`=.$`,.&p`4s-p=[`.*%3,-1`2h$`$o9 `$T;sd`#D$`5X&`?l,   message(['Score '+`.#*,'Lines`#7&`-%%],'Stacked to the top'`5_%`-?%`9>$ell.`<4$b,p)
  k=key(`D9&k==CLR`@4+
  speed=max(2,14-`$7$//5)
  q=list(`#m$`#c%held`7o$k`#j$hc+=1`;n,`([%`#P$!`#P%or k==DOWN or(k in(LEFT,RIGHT)and hc>4 and(hc`Dc$`5I&`$;%LEFT`&H%q[2]-`$8$`9G%k==`#i$`#A*`$V%`#A)UP`#>(1]=(q[1]+1)%4`:U(`(R+q`(R&`$.,`#G9`$5&2`$5,DOWN`#B%t=`&j$`#@,SECOND`#B%`+,%`#x&[q[0],q[1],q[2],q[3]+1`.e%`$2$3`%D(`#|+`,c$k`&~%`,/$`3j%n`,F(`=h$all=t>`#W% or tn-las`#5(*0.035`&~&fa`AR&`-3%tn`)5,t`$J&`#v-`$F%q!=p`Fu%`&8-p=q`+;5`$4,`.y$  q=[p[0],p[1],p[2],p`%t%`$f&`(8/`$#&`$$2`${*`IG8`#u%y>`KN%`=U$`Ab&`C,%`#a%ull=[y`AX5if 0`)u$in`#_$`$o$`E,-`B7+`#7+ del`#T$`$A(.insert(0,`7N(`@L&`-{$+=len(full`#9&`/_$+=(0,100,300,500,800)[`#M)`$%&`&/,`<p$True`#l(`1@@`3U) pause(0.02)
b_RULES="Shapes`)&$`VP&`0w%. Fit them together to fill whole rows, which then clear. Don't le`#c$ stack rea`#I%`$$$"
b_KEYS=['Left/Right: move','Up: turn','Down: `6O$faster'`7+$`#6&all`#x$way','CLEAR: quit'`PS(main`<%$`5N.c=home('GHBLOCKS'`9r& `9]%`&4&,`$q%,('Pl`$,$Back'`A@$if c<`+$%`3X)`=;(
`$A('''
GAMESRC['GHBREAK']=r'''import random
c_ROWS=5
c_COLS=10
c_BW=3`#+$H`#3&Y=34
c_RC=((220,60,60),(235,140,5`#0%0,21`#=&70,190,90),(170,9`#?$))
c_PW=46
c_BG=(30,70,170)
def c_brick(r,c,on):
 x=10+c*c_BW+1
 y=c_BY+r*c_BH+1
 if on:
  rect(x,y,c_BW-2,c_BH`#*$RC[r])`#E32,lt(`#C(`#D,+`#a$4`#K*dk`#K,else`$<=BG`%?-s():
 w=`&|%`%<$-2
 for r in range(`(H%):
 `%V2`$5%11,y,w`%J8`#A&`%F611`%G*w`%B1for c`$T*1,`$v%`$V$`#d%`(B(-1,`$g$1,`$K$OW`%@$`%i0wall`%h%`#c$0,24,4,186,(20`*1%230))`#C&316`#E@,24,1`#C%120,130,16`#g1`#E5c_PC=`+P$1`+o$`$q(paddle(x`$s)x,192,c_PW,8,c_PC`#M)uck(x,y`#M*-3,y-3,6,6,WHITE)
c_HUD=[None,None]`#a&hud(score,lives):`+h$`#Q$[0]is Non`*Z$text(6,17,'Score')`#8(214`#:$Balls',GOLD)`#k$`#}$!=`#r(:
 `$%/not`$*)`$+&`$,$str(`#J()`({&`#D1`$($)`$4%`%-$`$4(1`$4.1`$4627`%&$`$5*1`$50`#E+`&4%`%L(`$g(,`#](=`&[-`&t&game`*s$cls(`#~&`*~(2,320,2`(](`+G*
 b=[[1]*`,=%`.-7]
`.f+
 left=`,I)COLS
`(;%=0
`&3%=3
 px=137`%/*`&F)=None
`)t3
 while`#h%>0 and`$6$>0:
  bx,by=(px+c_PW/2,180.0)
  vx=`4P%.choice((-3.0,3.`,n$ vy=-3.0
 `,@*px)
  pause(0.5)
  st=Steer((LEFT,RIGHT`#d$`$_%Tru`)3%k=key()
 `)Y$k==CLR`#<$ return
   opx=px
   d=st.feed(k`#V(d==LEFT`#W%px=max(4,px-7`#E$ if px==4`#D% st.stop`$<%el`#f%`$j$`#g*in(316-`.T$px+`#n.`#=(`#u4obx,oby=(`&w$`#6$bx+=v`%-$by+=vy`%&&bx<7 or bx>312`#q%vx=-`#N% b`%9%7,`$V%2,bx`&U$`#_$y<26`#U&y=-`#x% by=26`#E&vy`)T&188<by<198 and(px-3<bx<`)Z&+3`3p$`#l%abs(v`%#% vx=(bx-`*)*))/5`%w(`#L$x)<1`%t&vx=1`$?$x>=0`7D$-1
   r=int((by-c_BY)//c_BH`$*$c`#=&x-10`#;%W`%M(0<=r<`,h%`%2$0<=c<`-N&and b[r][c`/s$ `#0(=0`#1$`:X,`+}$`&7-`,u$+=`.+&-r)*1`#Z%left-=`$~$`-E5`$d%`.L$=`-:$   break
   vacate(int(obx)-3,`#.%y`#.(`#8*`#7%6,6`1C)`<%$by<`7{$`7w++`+a&`03$`04+max(0`#q$(oby-3`&r-)`*7$`#k%`#G)+`#G.+1)`)W&`9j%`9k+`$%-x-3`(Y+`$#(COL`$#)x+`#E,`#}+`+T$[rr][cc]and`*;$r`<4&`%Z&BH/2-by)+abs(c`?;(0+c_BW/2-bx)`1?%`##$`)<)r,cc,1`&P)px!=px`+u&`(E%op`98%`#*&`9?)`(-->18`->&`1[/`/]%`#}4`#u&`$)(`:>-`#m%uck`)l$bx)`)R(`.V*>21`%@&`*b$`*{?`*j(`6K$`*O@`#H$4`$b$312`%_*`+g.message([`:x% '+`9U*],'All `6o% cleared!'`B:+`#c?Game over')
c_RULES='Bounce the ball off your `(1% to`%Y% every`$H%. You have 3`#Y$s.'
c_KEYS=['Left/Right:`#j(glides that way','ENTER: stop`$F$`#L%','CLEAR: quit'`>R(main`D;%`6s-c=home('GHBREAK','`#+$OUT',`%Q&,`$b%,('Pl`$B$Back'`)X$if c<`)T%`7F)`;p(
`$>('''
GAMESRC['GHCRYPT']=r'''import math
`#/&random
try:
 from time `#M(onotonic as d_now
except E`#*$ion:
`#<%=None
d_MAP=['#BBBB###SSS###','B....#.`##%`#4)`##(k','#####G`#E+`#Q$`#V,T....l`#4&j`#E0C`#i(###PF####']
d_VW=320
d_VH=172
d_COLS=3`#-$WID=d_VW//`#:%
d_FOV=1.0
d_WALL=(75,95,99)
d_DOOR=(110,75,45)
d_FL`#7$42,36,32)
d_CEIL=(16,16,18)
d_LINK1='petradavis.github.io/'`#C&2='Encrypted/?ysolde=1'
d_CIPHER='LI WKH OLJKWV GLH VKH LV LQ`#<$URRP. GRQW UXQ. KLGH`#?(FRDW FORVHW. LWV FRG`#a$HFKR'
d_TAPGRID=('ABCDE','FGHIK','LMNOP','QRSTU','VWXYZ')
d_KNOCKS=((4,1),(4,5),(2,4),(1`#/$4,4))
class d_St:
 pass
d_SPR={'couch':(1.3,((0,1,0,0.2,(150,40,45)),(0.08,0.92`#?$0.36,(120,30,3`#D%,0.1`#A(28`#d188,1`#A6)),'table':(0.9`$O$`#q%`#O&95,65,40`#n,`#>4`$+%8,0.33`$j%85,5`#Z&3,0.7`#>%0.37,(140,70,180`$M%phon`$M%6`$M(5`$2$3`$L15`$L&`#=0`$K$`$*$4`$J125,0.75`#@%0.42,(20,`#%$`$J%lamp`$I*.45,0.5`$L%55,(180,150,7`#u&15,`$T$`#H%.72,(235,220,17`#x&desk`)@$2`%C(`%B69`%AA5`%A2,0.`%?$`#($8,(200,19`$q$`$H%rack`%B$7`%B%6,0.54`$3$8,(80,55`*I(`%?%`%f$`#u$75,(6`(_%1`$:&`%W$`%c$4`%b&110,50`$[$)),'vas`)$%`$9%1,0.9`*5%5`%c0`$.$65`#?%`$B$(60,120,1`#F)`*<&`(F((9`#@$`(>$))}`-@%ITES=[(3.3,5.5,`-M&),(1.9,4.6`,3(),(4.4,6.4`*v(`#G$0,6.5`)a&),(2.6,1.5`(x&),(12.4,4.9`&e&),(6.5,1.4`%_&)]
d_ROOMS=(('Library',0,0,5,3),('Living Room',0,3,5,8),('Grand Foyer',5,0,14,8))
def d_tile(x,y):
 if 0<=y<len(`69$)and 0<=int(x)<14:
  return `#D$[int(y)]`#+$x)]
`#A('#'`$+&solid(g,`$.&t=`$>+`$=$t=='l'and g.l`%5$`$0+False`#{)t!='.`#~(room(g):
 for n,x0,y0,x1,y1 in `&F&:
  if x0<=g.x<x1 and y`#2$y<y1:
 `$7)n`%0*`&M,`$:&clock():`#H)`9]$()if`#-% else 0`%j(hade(c,k`#T*(min(255,int(c[0]*k)),`#8.1`#842`#8$`(s(light(g,i,d`(v&g.blackout:
  base=0.0
 el`#@$power`#=)max`,s%1.0-d/14)
`%+$`#_,6`#|&flash:
  off=abs(i-`:4%/2)/(`#.%*0.32)`($%off<`&l%base+=(1-off)*`$>$,1-d/12)*(1.1 if not`$j(`&T&.35)`&y)min`1n$base`%o(colour(t`%l&t in 'lkjCF'`+O-DOOR`*l)S`#?+`1z$90,60`+1*B`#C,`#?$,`$R,`<e%`(<(q(`)8+ int(k*5+0.5)/5`#G&put(sp,a,b,c`$u&b<=a`$m+sp
 out=[]`+s%y0,y1,cc in sp`+i&y0<`#W$ out.append((y0`*)$y1,a),cc))`#n$`#B)`$>%)`#{<1>b`#{1max(y0,b)`#T%)`%p*out`%G&diff(old,new`%G&old is Non`*K$`-H(ew`%O*i=j=0
 y=0
 while y<d_VH`*d$0,o1,oc=old[i]
  n0,n1,nc=new[j]
  e=min(o1,n1`*s(c!=nc`%4$if out`.|$out[-1][1]==y and(`#5(2]==n`(G$`%h%[-1]=`#A)0],e,nc)
  `,c)`(1/`#D%)
  y=e`$N&1==`#N%i+=1`#7%n`#7)j`#7$`&Y1column(g,t,u,top,h`/o%cl=(0,0,0)`.v-`,p%`C9%
 f`#H>`0g%`C{&,0.5`-d51)
 y0`/R%,top)
 y1`&{$d_VH,top+h)
 sp=[(`39$cl),(`*T%`$.*`.-),k)),(`#?$VH,fl)]`)~$y0==0:
  sp=sp[1:`#:&1==`)b(`#=%:-1]`$8%s`+f$s`+^% if s[1]>s[0]]
 def band(v0,v1`-U% a`6w$`$~$*(1-v1))&~1
  b`#</0`#<(if b-a>=2`5,,`.V)`&,%a`3h%`%A$b)`%g)c,k`)h$`.i+`0v3if u<0.12 or u>0.88`$5$sp=`%0$`>$&70,48,30`#w$`#?).8,1,`0c%`,C&0.7<u<0.85`#k..42,0.47,(21`C.$,9`#q%`$^)kC`9#$0.12`#g$3`/@%n=t=='`#?%g.closet`$#.`>C$,(4`EX%`#{%`#B,3,0.57`#D$20`>8$if on`*l$`@|$`#Z%`6V*`#=%3`G2%`$r*=='F`:p(ocked`.Z$0.15`$|$25`.W%`$D*6,0.64,`8B$3`$g(`7h$`4u*`;)$ in range(6`#i.n*0.14,`#*%+0.07`A6$7`H5%`(1(`&H%`(x/`AF%3`Im&`Cx$`&32`&S$`#F1`$o)`6D%`$o/4`$o%cc=(`#[$`C<%,(5`7*$1`#/$60,13`(*$,(17`BL%60))[(int(u*4)+n)%4]`%^025+0.05`%d$`#/$2,cc`$],T`+j(0.1`%i$9`%i/`EF%,(15,15,2`)=$`0I%tv`)>%6`$t%6`%].G`#~*28`$#$7`-w%`,e-5`,f%5`*#(`)S/75,(220,`,>&`#F%`#y$4`*1%5`,s%`(g,`J)3`#F$`%))not`4u&`)C1,(240,`#&$`$[%`%@)P`%@*3`$D$6`&@08,0.56,(13`(m%13`*a%`$|&`${%`$z044`>}%`=r-4`#p$`#=458`.@.`1(*`Cj&ender(g,full=`D8$`9|&full or`%v$hasattr(g,'cols')or g.cover!=COVER[0]:
 `#8(`#7)`#6&ls=[None]*`W$&  g.ysk`Y@% shown=`#L%
 new`;%$zb=[0`#U*ca=math.cos(g.a)
 s`#5&sin`#5&for i`-**`#_%`-/$cam=(i`?/%`B4&2-1
  rx=ca-sa*cam*`Xe$*0.5*1.15
  ry=sa+c`#A7mx`5p$g.x)
  my`#1&y)
  ddx`CU$1/rx)if rx`8|&0`##(.0`#J$y`#J(y`#J$y`#J5`#f$<`8L$ sx=`%+$ sdx=(g.x-mx)*ddx
`<U+sx`<*$`#G%mx+1-g.`#I)`$2$`#s(y`#s)y=(g.y-my)*ddy`#s-y`#s(y=(my`#s$`#I)side=0
  t='#'`1L30`1M%if sdx<sdy`,/&dx+=`$[%  mx+=s`#.%`#u)`>s+sdy+=`$9%  my+=s`#.%`#O$`$g$`LZ)mx,m`(A$`5n$`L3$`1|$ot(`Ln2)`@F&break
  d=sdx-ddx`$z$ide==0`(P%sdy-`$K%d`=|$d,0.05)
  zb[i]=d`&r%`#W&`#{$u=g.y+d*r`&f-u=g.x+d*rx
  u-`*A$u)
  h`#.$d_VH*1.35/d)&~7
  top=`#:$-h)//2
  k=`GH$`Kh.*(0.8`$M(`*R&.`1k%new`BK(`A]7)
 d_sprites(g,zb,ca,sa`E^$
 ys=d_ys_place`#B+`IP%`.u$ is`/|$None`9m$ys`F3( or ys[0]!=`#N$`(2$`.S/g.ysa,g.ysb`9U&hown[i]`/t&runs={}
 hit`1D%`/=<`He+`QO%`G}$`#x(,new[i]`$2%key=`B_&`Ex%r=runs.get(ke`*U)r`G#$r`F})i`*D%`#4)i+`+9$`57$`Od$  r`(2([i,i+1]`F}/runs[key]=[`#D&`9c$if ys`S6%s[1]<=i<ys[2`3I$ `%q$True
`&9+`%?%`&&%key`Ci$orted(runs,key=lambda q:q[2`%k%`%e&=key`&H&a,b`&f$`$c(`CI&ct(a*`iW%,y0,(b-a)`#3)1-y0`&O$`%&$`7y&`)Q, or hi`S)$ `*O$draw(g,ys)`,p,`#>$shimmer(g)`5X(`)x$`)~&=(`#}$,`&.$,`&+$`SK+`6.+`Ua&`,%6:
 ls`Op*sx,sy,kind`*4%`]X&:
  dx=sx-g.x
  dy=sy-g.`&C$wd=dx*ca+dy*sa`%f%fwd<0.`<z%contin`(d$ls`LH*fwd,-dx*s`#]$ca`$@$))`$Z$.sort(reverse`)F$`7S&fwd,side`$o)ls`&f$cx=side/fwd/(`6y.`Fo$col=(cx+1)/2`9H*half=`%V$[kind][0]/2`#i5`#W&`0e$h`Jk$`10%fwd`1.0`1-6nt(scol),fw`%V$`.U0`I}%`#J(-half`Yt&`$D%`#>)+`#>$+1`4;&if`3Z%<fwd`,o%`(.+ u`:a&-`#{,/(2*`#-$if`%u$>`4e&0.5`#w&u<0`Jh%`Y7%`#x-for u0,u1,`M%&`*6)`&]&1`.C&if u0<=u<=u`#l& y0`MM8   y1`MQ8`/U&1-y0>=2`_p(`O1(  `4d$`6S$`Mg$`#0%`Mk&y0`Ml+y1`Mm0`,y%bottom(g,promp`Zq(`#0%==g.`0Q$:`N?)
 `#6&=`#F%
`/h%0`Q;%3`Dq%-`#0$BLACK)
 text(4`#D$+15,`cb),GREY`5q(`^w)`#Q$25`#v%+15,'LIGHT',GOLD`#s/33`%&&[:31],WHITE)
d_YS=[]`%Q&_poly_slabs(pts`-?$,step,top`-c$,`%v%`-o%:`7j$[p[1]for p in pts]
 y`TU$`1J$n=len(pts)
 first`#3$d_YS)`YU*`Zl$s`3L%c=y+step`,~$xs`0l$`,c0n`,0%`f]$=pts`Z(% x2,y2`#3$(i+1)%n`5S)1<=yc<y`RM$y2`#0%`*}&xs`0d(x1+(yc-y1)*(x2-x1)/(y2-y1`N7(len(xs)`TD(d_YS`]}*i`#?$/256`*b$`#/(1-(`%A%)/640,1-y`#+$`1e( y+=step`9m&,on in((`&B$`X?$,(`&H)-1`(>&`/#%`R.%and i`kg&Y`:B%`-|-k=d_YS`&9&`#.&=(`#E,5`,:(_limb`)a$w`$l$=`B4$`(:/0,`)6(-2,2`$:$`(F$,`(<%(`(M%,`#*$+1`#,(2`#,(3`:K$n`@r$1`1K$abs`($&/8`27)k`)R1t0=k/n`#-$1=(k+1)`#1%xm=x1+`(q&*(t0+t1`3I% ya=y1+`$&&*t`Cw$yb`#7-`0.$hw=w*0.4+abs`)a(n/3`)I1(xm-hw`)=%(xm+`#/(1-`+v$a,yb`)K$-0.004,1-`,b$`#:)+`#:%`)b&`(2&oval(cx,cy,rx,r`9*%`-x%a=0.`(A$`KT,0.55`KU/`#6&pt`-.%`(q/1`VW%t=2*`#U$pi*i/16
  lx=cx+rx`#;%cos(t)`#/*a)-ry`#2%sin`#>)sin(a)
  ly=cy`#c5`#F%+`#c4`#~%
  pt`-z)(140+lx*ca-ly*sa,5`#2$sa+ly*ca`Df%`189`&c)build_ys`q>$`&JF`,M([128`x?%32,88`WY%6],11`$F1[(98,122`w8$8,11`#-$`y$$6)`YA%21`XH$46,26`#-$10`#-(06`#A$],0,8,`3;$`R]%
 hem=[(108,2`Y:$14`#-)62,330)]
 x=162`2|(x>9`vp$hem`&d)x-4.5,330+(1`Hr$`vx%%2`:6%6)`-d$x-=9`$<$`#[)94`$-$`%a1hem,0,6`$r%`$}$`&N-18`7M$112,4`{x&470,108,612,98,628],9`#X-40`#X%46,462,136,474`XN$610,162,630`#Y000,128,84,250,92,262,76,420],7`#N-58`#N$176,248,166`#P$184,41`#Q&for `x^%sg`3]$`#p%,-1),(`#M&,`>T&`A^$`-R*`br&`$:)`yK&0+sg*(f*4-6),y0+52+f%2*8`#=*5-4`#=$70+f*3],2.6)
 hair=[(-18,-6),(-27,30`#,$4,9`#5$6`a+%8,100),(2`a.$,(17`#U%10,-24),(-`#-&]`+k2`-g?for lx,l`II$hair],0,4`&p%`1?$0,0,17,25`#;&for ex,`I|$((137.2,41.`,j$49.1,48.55`&X%`3/.ex-2`3.&ex+`#.&1-(ey+2`8Q((ey-`#0&4)`<q$G=4
d_RIM=((215,`#&$25`d6(75,19`&4$50`*.$255`#]$INSIDE=(36,36,44`0$(`Pk4`@4%`aW%ys_vi`K+$`^H&`O~%dx=g.y`H~&dy=g.y`I#&`H~1`H}.`#k-cx=(`Hr,)`H-7`H,6`H+$0.45`G|B`U10fw`U3&`U21a`RR&b=0`5}1`GlW`Gk(>=`Gl(if a`x^,`qd$
 `qP$+1`&K$`#C-`&M-left`%@$`$P+`P$&)&~3`d4(((left`$^$`H]%`#G+`Vv&a,b)`#($`)t*`P3*`)m*d_Y`NX%`6<,`$R%,wid`#r*=`P6$
 lo=`Qp(
 hi=b`#0)row`VD%eye`9|*`?g-`O{)`$?%xa`>:$lo`%;$left+u0*wid))//d_YG
  xb`Dj$hi`#G+1`#G$+1+d_YG-1`#P*y`uk3
`>&$`J91`VQ$if `@k$=`6E$`%*$`={+a+xb)*d_YG//2,(ya+yb)//2`i]%`LA+if xb<=xa`Qa0for r`*s0ya`$}&,`DQ$`Jz%b)`%>.`NX)`#d%ow`.P$ `#-$[r]`8;*a,xb`$[%`XJ+`#H%=[`#B&]
 ou`TI%open_`(g$`$h/d_VH`$E%+1`hB%ur`#K$ segs=`XA(ow`ZX%r,(`9=%m`HY*`$7$`Xp$eg`${%if m`Eg$xa<=m`Zk&`O@)xb>`#7. `#2(=xb`%C.`:B)[`$/$`Dc$`$=-m`$:(xb-xa>=`x;% cur`#U$a+1,0]`eE%`#8&+1,xb-1,1`#:-b-1,xb`#O)`$L*`#o(`#?)`[S+list(`&t$`(x)key`-d$in cu`^C&ou`WW*key,`#U$.pop`_B$,r`Fj*`#|%`#](`#t.`#Y$`#v&pen_`^x%r
 g.ri`(M%for c in(0,`)2%for`)s%`EA%,r0,r1`#r$u`]&%`,f)c`Lk&,y,w,hh=(xa`,^$,r0`#+%(`&{$`,t%`Rr*r1`#4$)-`#J&`t$)hh>`gx%`_$&`#~(,`7>( if c`?{%`8*$[0`bP%`te)`$]& `%Q%`,T*`#n&`rm$`0>$2,wid//12)`0|((x,y`:u$x,`&k$eyes`Nl$o+r<=x<hi-`dM&<=y`U]$-r`&W&rr`W3$((r,(35,`vM%)),(r*2//3,(8`9i%245)),`/*$1,r//3),(23`9w+`>x)`$N+`/y%irc`%7$rr,c`49+`b.*`:(,ri`,=$`V3(`n^/3`N*%`&+%=random.choice(`#a$)`#a$`(?*,`#G.`(9$`KB)wrap(s,n=3`K,$`02(`Tr$ara`/2$.split('\n'`$F$line='`pF(w`U>$ara`#J( `#I%`S*(line)+len(w)+1>`X]$`,}-`#D$`#8$`#~$w`.5.`#7$`#G$+' '+w).strip()
`#j4`97&out`%Q&page(title,body,color=`X:%:
`$($s=`%z&body)
 per=9`%v&`RJ0`#S$),per`3#%l`8s$ c`Yo%0,`$4%`Yd& y=44`&>&l`)($`#d$[p:p+per`2N%`#^$10,y,ln`$j%`&#$y+=17
  more=`#R$`U+$`$J%`[,(10,204,'ENTER:`#O$'if`#+$`-j%`#=%/CLEAR: close'`[~(`Jd&Tru`()%k=wkey`%@$`/u$ in(OK,CLR`sw/if k==CLR`#:$`+Z&`(-%toast(g,`$s%:
 `|8(+=1
 rbox(10,50,300,30+18*`&p+8`]p( y=72`(A%`&P+`(0$`%k$y,ln`Xz&18`L{(`%/%`3$%`%*,pass`aW*`k=,ay(g,`$s$`%+*`,o)27`-%)keypad`*S&hint,`W)$abc='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
`*,(`*+6y=4`%U-`$D&`$*$`.6%`*).`(x(`*&&typed`./$sel=0`%y(`)5(`/Q$60,96,200,26`d$) s`.g*`_{2s+=(`$$$[i]if`]2&`#4$)`*a%_')+' '`(K)116,s`.=(`)&)`$(02`Vv% x=4+i%13*24`,A$y=140+i//13*28`2r$=GOLD`Qj$==sel`,#%`#}$`*~%`1y%y,22,24`%G*`*m%`#=+5`ur&`$r$x+6,yy+18,abc[i]`#?%`,N+`,0%LEFT`%z%el=(sel-1)%26`rV$`#E%RIGH`#F.+`#F. in(UP,DOWN`&l&`#K)3`#q/DEL`/S%`)1$`(5%:-1]`#F+`-j.`G1&`#A)OK`#e*+=abc[sel`e^(`(z*==`3c&`#k&`#9$`,7&objective`6g/powe`<^$t='It is pitch dark. Find the `#J$ sw`#?$by`#7$front door.'
`$x%`#y%not`+P$t='The`#E$ locked behind you. Look arou`$.&foye`#p0`1k$`=A$t="Decode Ivy'`}]$e. The coat`29%t `.n% wants four letters."`#}-living`$q&Unlock`$N$L`#;$ Room`$T/taphear`LK$`%J&TV in`#Z0`&=&ed itself on`&73book`%G.the knocks.`%S+book might expla`$:%m`%?%`8l%t='`#h3The hallway`&-/ive`&-)'`oY&awak`#r%+='\nShe is `#9$. Stay quiet. Hide whe`%j%`vN$s stutt`(|%`+.(`3i(hort`+%8`#O&'`*t5`$f%`*^.`#T(`*F5`#T,`*C*`#V&`*H2 (DEL)"`#X+`){*`$2(`*$6`$3,`)},`#Y(`*&&`)o2`%D0`)l(`$p(`%{$`)c."`&l)'H`)3-: 5`)+('`(+&journal`(-%body=`/F.`)Q&`&g(body+="\n\n`$>*: "+d_CIPHER+'\nMy nam`)u$`*l$ey`*@)`%n,`#q%'\n\nK`+4$: 4-1 4-5 2-4 1-5 4-4'
`?j('JOURNAL'`?n$`$f,`&,(d_gri`#Q&)`:S5`#C+:`9X2"IVY'S NOTEBOOK"`wQ-10,44,'For talking through walls.`>U)`#R(61,'`%K(row, then column`#Q*`PU/`c^%`8n&0,92+r*20,str(r+1)`AL)`Kp(`d;.if r==`JU&`#j%40+c*24,76`#j$c`#j,`#F/`$7(d_TAPGRID[r][c]`%D+`Aa$I`Ir$J share a box.  `A[$`%G)`?6C`(Q%facing`+4%`m:,g.a`m9/`#5%`I6/1,9`ce%=n*0.2`1z$d_tile(g.x+ca*d,g.y+sa*d`:G&t!='.'and(not(t=='l'and`.x)`K=%`13* best`_)(d=1.5`$P%sx,s`rx%`?c%SPRITE`[H%x=s`c#& dy=s`b~& dist`%B&qrt(dx*dx+dy*`,*$ if`#D$<bd and(`cM+)/max(dist,0.01)>0.8`$q$`$g$kind`#0$d=dist`/N)bes`3?(label(g,t`3A&t=='P'`0z,`Fy&`3:2t=='F`#N4`:G*`#L*G`#L4grandfather clock`#S*C`#S4hide`Tk$`4#$'`/7$`:&&`HW+`HQ&`:;(`#y*l`#y4`9B,`%#.k`$M5`3#-`#P*j`#P4dining r`$%2S`&&9 staircase`#Q*T`#Q4smart TV`#J*B`#J4bookshelf`#K*table`#O,"`#O&`5j1if `.K$'phone','desk','lamp','couch','rack','vase`QC%`$N/look`:K*'`6D(use`+.5`)>$`:U)`#Z(`Ji('P`#=$`=}$)
 `#N(=Tr`c>)`/W+`G9&g.blackout=n%2==0
`rs$rend`Ud$`#m$`#F)`v9$`5s$`$=&CLUNK. Years of dust rattl`+D$the wiring`$^(`BU%`$_(`$3.`Ls*['ASHGROVE SMART HOME:','Welcome home.','F`-T) LOCKED.','You did`;&$set that up.'])`A/&`.K*`%;("`$2+`#p(`@D&ndle doesn't move."`(H$`Dp&`-e%`E+)i`?j$ck. Swolle`(2$its frame`%z$`$M)`/L%`?t2`)@1Too`F}$ to make it`Vp$ G`%P$`A0)on first`(-(note`(+*`:C$`:/+",'Folded paper, tu`G5,`A9$endulum glass.\n\nDad never notices anything. Grandma taught me this on`C)&I was six. `=g3\n\n'`>1-\n- I.V.Y`%B(arm`*K)`&a)`2X%`2:+`&].hid`?X%`()E`$V%pad is dead`$E%a=`T+)'COAT CLOSET KEYPAD','A brass`#b&. F`I[,'`y[$ if a=='ECHO`%#$`$})`(e(`?A.`.31`$s.`4b&clicks`gZ$. On a hook: a`$[* tagged LIVING ROOM. You t`*Y%`%T%`&j$`oI%`&&4buzzes. Wrong cod`,(/`6%%`Fo3`&~1L`-;$. `&K+hole, polished from us`$,%`<2)`0-8`$x+`%f+urns. Stiff`AV&all at onc`#~)tv`#z*`#l&Somewher`1a)`88+, a`Gn+s`M^,`%~,`7~%`#w*`/Y&shu`lS$`/_7`8*%`#Y)Boarded, chaine`=T$ pad`0p%`1;%`#2& is engraved M.A`#}.`8-%`2.)Book`/|$radios,`)1$s`$($moths. Mildred's, mostly."`#u,`9K%`-NGTV`-J$ark`(2%d_tv`(y$`#t)`9K*`H:*`(T*`H>-`1d3`Gp%"She can hear vo`15&d scree`)p$he's bad at`R$* think it's too slow`8X$her`1-$- Ivy`%q-`:p%`(k-An old rotary `#D$. Silent. For now`(R.`;R$`(U-`(3) desk. Pag`%4&p`#-$of dot`#5%dashes`(T.`<D$`$b4`,o%fl`X,$amp`$S.`<v%`#[-`0R$ushions still hol`5I%shape of someon`+w/`=b$`%G-Coa`6y%hooks. On`Tf% child's raincoat`%>.`>I$`$a-Dried flower`V7%y crumbl`6;&you`i)$th`$a/`$]%`54R`]C$No`F0%`5>2`<m/LOCK`5?$stick`wl$`07$Ivy\'s writing: "t`,q%knows.`yE$en."',5`5Z+QUIE`-i% g.won`,k(`44V`QR3`.,$`QL&(10,14,30)`QV*4,`%Q0TV'`QY18,'HDMI 3:`rq%ho`;:$comes next`Q^26`$}$n `Aa$`)-$n`.6%`A0$`#R(y=100
 x=20`Qm&`wJ$ d_KNOCK`Lm$for grp in(r,c`C(%`C>/grp`o,&`w))4`i)*  x+=1`~I%pause(0.2`(E$`#<$0
`#+%4`(V%x>27`RI%`$b%`k^$24`%L*170,'4-1 `VO$`VP$`VQ$`VR$,(160,21`xz&`RB/Writt`A6%your `Xr&.`RE/`Wu*`)x&`okD`,S)`_u)`#.&`*c(g.ytimer=6`3K*'...'`*j&`(]& stops.\nEvery`3C&`8P(house flickers`99)\n`b)0`ax>,(200,14`#&$`q=)`@$&:
 g.hidde`,l(`YA-70`FH%squeeze into`$/$coat'`)])`#P%90,'`<l%. B`0+%`54$ly.`#N0150`vd)step ou`,2+0`q82k=`mx.`k{&`v?(`*y)`wp$0`uu$`Bq%ystate=='hunt`Uz$t0>25`/V&`#A&'dormant'`#9(_vis`K*)`)3*`~-&randint(35,5`,6%`pX$0,110,320,30`pZ+`%e&30,"The static fade`8q)gone."`+F*`(P&`$K&`vi4ight`Yf)g.`#3$`En)g.yx,g.yy=(9.5,1.0`Yg3`ui%`N1,<3`86$`N9)`%|)n>=3`#3%y=1.0+max(0,n-3)*0.08`AI1`(M,`&h0`O%2`#a-`3o)...it`Hx$a woman. Mad`8T%`&Z$. And she`#H$loo`-R$at`oa$'`,B(ys_update(g,d`Qz(`.f+ or`5G%`Rm*`df&`*F)`*)(`&G%`)r%-=dt`*q)`#5$<`b3&`*c*warn`*_(`*L%`wF$`Bv*`)q%hisses`:y$`C}-`/N$`BD%`.}0`9_(`$q+`$7$`$n3`(.+`+s+om()<0.35`%58`Sh1 spots=((2`*_$5),`*j&5),`#7$6.4),(11`#8)6`#8$`4*$  far=[p`+8$p in`#s%`9p$bs(p[0]-g.x)+`#1%1]-g.y)>5]or`:H$(`#R$`#n$`,6*`%@&choice(far`#C(`(>&`/@$`.{-`LH*`(O&28`&c2`#Z$`&c3dx=g.x-g.y`c9&g.`c:$`c;$`c8:sp=0.55*`*<(d>0.01`($$nx=g.yx+dx/d*sp`#6$`#|$y+dy`#6)`+e&d_solid(g,n`%s%)or `fB&`#5(in `Lk&`&@%=nx`#g5`&]$ny`:B&`&g$ny`*9.d`/]&`*A22`*A&d<0.6`>M&c`Se$`/L%`&j(`,r7`3U@`+-2`3k?`/7%`$L):`2.18`%Y$for y`#8*0,176,22`]X&v`$&060,230`4p,y`4n$22,(gv,`#%$`@@$`8],90,'S`u~$u`|c&',(220,1`#&%`@s*13`8.(`lvL g.`)P$,g.a=`-o%5.5,`+0$pi`3X&`(%0`3nB`&{)30`6M5ending`r_240,'enCRYPTed`<1&60,6`%Y+70`DM-fl`JO$ gree`QY%`&Q*End of`2?$demo`#A+125,'Full game at`D6)`#C&47,d_LINK1`<106`#=(2`#=/203,'CLEAR: leave`(G5!=CLR`(>)`&%%`7f$_menu`F=&=choose('PAUSED',['Resume','J`B(%','Quit`%J$`bv$`YE.if c==`/g$`yO,`gJ)c==2`$H(lay`(I$g=d_St`wV%`)}+9`3x%,-`)}&/`9Y%`g;%`ed)`ac&`[*)`Ws)`V|$`*#)`Cv)`Rh+`CC(`_,(`<F*`#Z)`)L$`<U)`*}2wo`=L+`=]0`+c0`,,5`+e%`+d$y`31$y`#0%`&o,`+a&`E$(`+^+'Ashgrove Manor. Bo`cD$at government auction. `k#$ off since`+V$accident`E6$It is pitch`Nj&F`d~)`r}+ by`#7$`rf*`,?$last=d_`rE$`$}$irty`&V&st=Steer((UP,DOWN),True`+Z)`=:%`=/&`D$*d=st.feed(k)if k`#K$in(LEFT,RIGHT)`i5$st.d`xH&`$I) dt=t-last`4z$_now`id%`54&`${$`8?$t=`@p$.02,min(dt,0`:m&mov`)x*`EZ&`-K&`#z%`-F0`R[)`60$`%t+  contin`#/$`#n%DEL`6W&`-,,`#ZASECOND`6p&`+V%`&V%`#/$`#:%`ea/`#v-`(0%`&|$`#r-`4-&`$0&LEFT`$.&a-=2.0*`yx$t,`O4)`&4%`SE,k==`(S$`#[(+`#[Bif d==UP or d==DOWN`#c$s=(1.6`#B*else-1.0)`<J%`<=%x+`~g-*s`<D*`#=%`~o(`#=%r=0.22 if s>0`#w%0.22
   ox,oy=(`0z&`$s$`<{3`$9/r`#O$`<F(`<q;x,n`$[0r`=$*`=#%`AP(g.x-o`AN&g.y-oy)<0.0`?)& st.stop`,;$`(A6`M1&f=d_fac`JF%`$*&f`#i%`w8(f`TX%`*+.`*,.`#r&`*),`2v& and(`+,%`2~&)and(d_room(g)=='`pT$ Foyer`x~%`H|$`Aq%atan2(1.0-g.y,9.5`D9$`+c%ff=(look-g.a`&O%pi)%(2*`#/(`5M(`&O+diff`FY%`%U(`M:+`&R2`%h.before=`4F(`J6%`5((`7S$`Jk/`%}%`(>$`+o$irty`#Y%`#g4 or`$-&`/?&`ou.`$T$`0Z(`(x0d_bottom(g,d_label`(z$if f`1m%d_short(g`1N$`+1&`$f$`$7$`NI(03`5~$`=u(
d_RULES="Explore `6+., solve`~c&`k$*hid`51$m Ysol`Vn;"
d_KEYS=['Up/Down: start walking','Pres`v.%other`vW$to`XW$','Left/Right:`on$ a`U{$'`V.)use  2nd:`?M%`$K$','DEL:`[$(  `>2&`%z$']`<F&main`<F$`VZ.c=home('GH`97$'`@}+ DEMO',`&N&,`%M%,('Start','Back'`(A(c<`F~%`5C)`=a(
`$E('''
GAMESRC['GHFLAP']=r'''import random
try:
 from time `#A&monotonic as e_now
except E`#*$ion:
`#<%=None
e_GAP=64
e_NP=15
e_TW=e_NP*2
e_TOP=22
e_GND=196
e_BX=60
e_BR=7
e_SKY=(110,195,240)
e_LEAF=(50,140,6`#6$INK=(20,`#%$)
e_BODY=(240,200,`#[%BEAK=(245`#]$3`#7$GRAV=900.0
e_FLAP=-265`#1%ALL=43`#>%SPEED=80.0
def e_column(gy):
 return[(`%C$,gy,`$q%),(gy,gy+`%z$,`%?$`#7$`#4)GND`#O(]`%a%COL=`#n(`#C(SKY)]`$B&bg(p,trees):
 for t in `#5$:
  if 0<=p-t[0]//2<e_NP:
  `$p& t[2]`$}( `$<(`$%&diff(old,new):
 cuts=sorted(set([a`$;$a,b,c in old]+[b`#84`#M/new`#M2new]))
 out=[]`%>%i in range(len(cuts)-1):
  a,b=`#4$[i],`#+%+1])`%g%b<=a`%X$continue
  m=(a+b)//2
  co=cn`+I% `$4$y0,y1`%#)`#a$if y0<=m<y1`#3$`#X$`#R2new`#R7n`#R$if cn is not None and co!=cn`#](out`#9$out[-1][1]==a and(`#5(2]==cn`%m$ `#J(=`#A)0],b,cn)
   else`#J).append((`(%$n))`)S)out`)N&spans(cols,out`+w$un={}`(B%p,sp in col`*a$keep`#@$`#A$s in sp`%9(`#2$run`%>$run[s`%=%`#D%`#a$[s]=(`#>&0],p+1`%&/`#H)p`#@(`$3)ru`&J)`&i%in`#R$ or`#Z([0]!=`$))`#w%e_`%U$(s,`#<%`%X$
 `%X$keep`%Z%`$,,`#U6`&G%`#=)`&F(`)t&=s
`)l$1>y0:
`(=.c,r[0]*2,y0,(r[1]-r[0])*2,y1-y0)`$%(clip(sp,a,b):`,h.`+%+`(/%y0=max(y0,a)
  y1=min(y1,b`,b&`$T)`$U-`#m&`)r5batch(todo):
 todo.sort()`$M%c,x,y,w,h`0Z$odo:
  rect(`#;&,c`%:(bird(`2R&ct(e_BX-7,y-6,14,12,`4%%`$N$`#B&+7,y-1,5,4,`4/%`#@-2,y-3,3,3,`4s$`$1(ground(`$2)0,196,320,5,(70,170,80`%^%`#B$201`#B$9,(120,8`5G$`%P&x`0f*0`#H$20`-t$`%S%+6,204,4,2,(95,6`5o$`(y)rashed(y`3z*if y+7>=`4I$`#l%`(-$True`-]&`$:*`&9%e_BR)//2,`%g%`#2(+`26%`)m/`560`0b%==`4X$`1N(`2B) dx=abs(p*2+1-e_BX`-z$if dx>e_BR`#U3y=int`$g$R*e_BR-dx*dx)**0.5`#c(y0<y+dy`/@$y-dy`2B)`%a-`#0&False`&J&new_tree(x):
 gy=`<6%.randint(20,55)*2`9#)x`8z%`9?*`82(game`)j$cls(`8M%
`*(+`)c+`);%`*O( text(6,17,'Score'`#=/`#>%0`#:+rees=[`%.+332),`#3.+172)]
 shown=[`9*(]*160
 y=1`<)$ v=`#*$score=0
 passed=[`&<$,`#)$]
 go`#J%o`(K%y`%K$`-_$oy)
 pause(0.4)
 last=`?,$()i`&|$ow`3B$ 0
 while`(L$`4V$=key(`/x&k==CL`)g%`()%`#:%`#e$`#9$`#{)`)}$t`0^$0.12,max(0.03,t-last)`#D$`$Q$t
`4f+dt=0.05`$8& in(UP,SECOND,OK`+q%v=`?/%
  v`$+$`?0%,v+`?T%*d`4D$y+=v*dt`2#&<`>0$+7`#g$y=`#1&.0`#v%`&P$ go+=`?q&`#]%step`&f$go/4)*4`#G$-=step
  lo,hi=(160,0`6[(`<O+2`$z%t=`)r$[i]
   a=`>x&`#>$[0]`#s) if`#4$+e_TW<`3y%`*R%[i]=`&r$`*F(max(332`.z%[1-i][0]`*X$`&p$`*,&[i]=`-G% `$h%p in(a,`$K&`;B&lo`&[$lo`(c%,p`#i&hi`5m$hi,min`%U$p+e_NP`#B%if`9($`$3)and`%.+`1>)`$-%`$Y*`/1%  `-6,str(`,4$)`Be&`#D$`#5$+=1`#Q=`-m% work`8)$ hit`%f)`2|/`(n$`%g%n=`2T-`%A(`?6(`.5$[p`;3&d=`C8&`#:(,`>R%`2S$`#F%`$K$`8d)p,d`&[&`,w%BX-8<=p*2<=`4<$12`#Y&`$z$`&*)`$)(=n
 `8_$`%C%`?1(work,`9B$
  n`/1*`%+$y!=oy`#{$`CD$oy-6,ny-6)`#@$>oy`-d$(ny+6,oy+6`>^%`$#&[(p,`;r(`%T(a,b))`6W58`6T+13)//2)]`$d)`;8-`$h, or hit`$o$`11&n`%/$oy=ny`0;(`8G3 `1T-  message(['You`*h& '+`)~*+'`-6%.'],'Crash!'`#^$`1M)`#v(01)
e_RULES="Flap to fly through the gaps between`#4$`$&% Don't hit`#8* or`#V%`6,$."
e_KEYS=['Up, 2nd or ENTER: flap','CLEAR: quit'`7)(main`7)$`3t.c=home('GHFLAP','WING IT',`%5&,`$9%,('Play','Back'`+>$if c`0H&`%y)`89(
`$<('''
GAMESRC['GHHANG']=r'''import random
f_WORDS='PLANET ROCKET GALAXY COMET ORBIT JUNGLE TIGER PARROT DOLPHIN OCTOPUS PENGUIN CASTLE DRAGON WIZARD KNIGHT PIRATE TREASURE ISLAND VOLCANO DESERT GLACIER THUNDER RAINBOW BLIZ`#s$TORNADO PUZZLE RIDDLE SECRET MYSTERY CIPHER LANTERN CANDLE MIRROR LADDER BAS`%e$UITAR TRUMPET VIOLIN PI`$_$RUM`%N$CIL ERASER NOTEBOOK BACKPACK LOCKER SCIENCE HISTORY ALGEBRA GEOMETRY CALCULUS PIZZA PANCAKE WAFFLE NOODLE BURRITO PRETZEL COOKIE MUFFIN BANANA AVOCADO'.split()
f_ABC='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
f_INK=(20,`#%$)
f_POST=(225,175`#7&USED=(190,`#&&)
def f_lxy(i):
 return(30+i%13*20,150+i//13*28`#R(nbox(x,y,w,h,c`#[%ct(x+2,y,w-4,2,c)`#8,+h-2`#<1,y+2,2,h-4`#Q,w-2`#<.`$n&etter_box(i,used,sel):
 x,y=`%2(
 c=GOLD if i==sel else `%m% if `&f$[i]in used`#B(INK
`%I,18,2`$b%text(x+4,y+18,`#d(`$d0s(`$X&for i in range(26):
 `$Y$!=sel:
  `$~/ `$B2`$Z$)`#r%r`#r+`#q$`$[$34,168+r*28,' '.join(`$i%r*13:r*13+13])`#q*`&Z,sel,''`&Z$`%8&word_line(w`&x%new=None`&}$0=310-len(w)*20
 if new is None`$c)x0,85`$[*[ch if ch `(.-'_'for`#:&w`$p+`+2&
 at=[i`&f0`$I%)if w[i]==new]`(0+at`$Q++i*2`$V%_',WHITE`&i&`#N;new`$T(`&,%figure(n):`%d%==0:
  r`+^$0,136,120,12,5,(110,180,90)`%;%`#G%40`#G$4,(8`-M$,7`#C+8,132,74,6,`.Y%`#=-6,74,2,dk(`#@%,0.75`#b*24,18,5,11`#c127`*V$`#>$`#d?2,5`#c14,21,52`$F6col`#7&)
 `&m$o`(d*4`+V$ draw`*Z%29+o,44,50+o,23`$.)72,23,3,13,(140,90,4`&1(`)k%`$2%`*$%`(<%1`(<$ing(73,46,10`(p%,2`)H)`*N*=((73,56,73,95),(73,65,60,82`#1)86`#1)95,62,118`#2)84`#2$)[n-2`*w&o in(0,1`%W$`%V*a[0]+o,a[1],a[2`#/%3]`*T(game():
 w=`9w%.choice(`9~&)
`,y$=''
 bad=0
 sel=0
 cls(`+s)`+C(0`.x+`0p%
`.k3)
 while Tru`.I$done=True`(w&`.&&`(q$`.M%not`.Q(`#9$`#V%False`1c%d`/;& message(['You got it: '+w],`#5$win!'`1{$`(O( if bad>=6`#f/The word was`#g&Out of guesses`#m/k=wkey()
  old=sel`$&%k==LEFT`$($sel=(sel-1)%26
  el`#E%RIGH`#F.+`#F0UP or k==DOWN`#N/3`#O/CLR`#E$`$i)`#<(OK and`6M&sel]`&u0used+=`#C*`(D&`#4*`(Z)`4.4`#J*`&4$els`(V% bad+=1`#Z&`*<&bad)`&;%old`6g$`%R&OK`#X$`5R-old`92*`#A1sel`#A+f_RULES='Guess the hidden`)6%one `#a% at a time. Six wrong`)E(`&A$the game is over.'
f_KEYS=['Arrows: pick a`#x&','ENTER:`#l% it','CLEAR: quit']`.$&main`.$%`,j-c=home('GHHANG','HANGMAN',`%G&,`$J%,('Play','Back'`1?$if c<`5C$`)a*`/5(
`$<('''
GAMESRC['GHPONG']=r'''import random
g_PH=36
g_TOP=24
g_TABLE=(30,85,165)
g_BALL=(250,150,40)
g_LINE=(150,190,235)
def g_net(box=None):
 if box is None or g_ring_hi`#L$):
  col(`#y%)
  draw_circle(160,117,28)
 for y in range(`%($+2,208,14`#n$`$81(box[1]<y+7 and y<`#4%+8 and`#A$0]<161)and(159`#C$0]+8)`#v$ rect(159,y,2,7,WHITE`%^(`%9*):
 x0,y0=b
 nx=min(max`%0$x0),x0+7)-160
 ny`#A*17,y0),y`#A%17
 fx=max(abs(x0-160),`#/%+7`#1$)
 fy`#F)y0-117`#F%y`#F$17))
 return nx*nx+ny*ny<=29*29`%w$fx*fx+fy*fy>=27*27`%A&court():
 cls(`)u&`#t$ct(0,207,320,3,`(m)`#=&`(I%1`#A$1`#A*`)v%`&F(paddle(x,y,c):`#a&x,y,6,g_PH,c`#L)uck(x,y`#H*-4,y-4,8,8,`+C%`#N(scores(a,`(A$`$X&0`$R$`$_$-2,`%8*text(110,18,str(a)`#8(20`#8)b),GOLD`%M/-2`#y$2`)h(`#q&4,18,'YOU'`%h*`#v%5`#v$'CALC`#?*`%$%game`(#$`(0)
 me=cpu=0
 py=cy=100
`%P*me,cpu)
 serve=1
 while me<`,1%cpu<7:
  bx,by=(160.0,110.0)
  vx=4.0*`#c$
  vy=`/Q%.choice((-2.5,-1.5,1.5,2.5))
 `(t*8,py`%m)`#:*306,cy`&G( pause(0.5)
  st=Steer((UP,DOWN`#w$`%(%True`-_$k=key()
 `.d$k==CLR`#<$`+w&
   opy,ocy=(py,cy`#O$d=st.feed(k`#a(d==UP`#_%p`,|%`+G%3,py-6`#I$ if py==`#<&`#P% st.stop`$O%el`#p%DOWN`#r*in(206-`+X$py+`#s.`#=(`#t4target=by`#E$/2`$x&vx>0`(w$bx>120`#^%cy+`%($-4,min(4,`#b%-cy`&Q$ cy=int`0-$`%K(`$e-cy)`#L%obx,oby=(`)s$`#6$bx+=vx`#-$y+=vy`$R&by<`#p%6 or by>202`$W%vy=-`#J% b`&h,6`$>&2,b`$c&if bx<1`39$ vx<`%J$(py-4<by<py+g_PH+`4/%`+<$min(9,-vx*1.0`&e&vy+=(by-(`#S&/2))/6`$I%x=18`$3)>302`$4&`&[%(c`$4&c`$43ax(-`$59`#T&`$5.30`(e$ob=(int(obx)-4,`#.%y)-4`#i$vacate(ob[0],ob[1]`#E$`#O*`#N$`1J&`0t(`%2$opy!=py`$n&`#l%8,opy,`-e$`2L&`#X0cy!=c`#X.306,ocy,`.*&`#]60<obx<24`#^%`.w7`,N%`$e6`$d$o`$e*`#X*if 126`$*$19`$+)net(ob`#D(29`#D%3`,=(`0.8`$M&`%X7`%W&o`%X*`#[)`5e&`(<&`(:(`+K+`-^(pu+=1`#.$`3,)   break`*j+`$t(me`#Q.-`#R.`5P$`)WC`8+( `4Z3message(['You '+str(me)+' -`#1&cpu)+' Calculator'],`#P$win!'if me>cpu else '`#J* wins')
g_RULES="Bounce the ball past`#1$c`$$*s `(Y%. First to 7 points`#u$."
g_KEYS=['Up/Down:`#V& glides that way','ENTER: stop`$3$`#L%','CLEAR: quit']`8;&main`8;$`5T.c=home('GHPONG','`#*%`%G&,`$X%,('Pl`$=$Back'`)b$if c`)_&`6#)`9H(
`$9('''
GAMESRC['GHRPG']=r'''import random
h_T=20
h_MAPS=(['T`##/','T.`##$T`#+(`#6$HH`#1%`#61C`#6,`##->`#6(~~~`#66TT`#]1`#63`$))`$w0],`%18`#c$`%2$T`#s(T.C`#6-<`#~&`#)&`#6&`$I$`#9&`$y&`%{&`#6,`#2&T`$y*`#[%`&#-`#p&`%1?#`##/','#::::`#($`##$`#6&C:#:##`#&&','<`#I%#`#O&`#6)::#:B`#6)#::`#|$`#O&`$))`$&)`#6&`#G$`#M%`#I.C`$O+`$w0])
h_NAMES=('Meadow','Whisper Woods','Hollow Cave')
h_FOES=((),(('Slime',12,4,1,6,(80,200,90)),('Bat',10,5,0,7,(120,90,160))`#d$Bone R`#H$8,7,2,12,(220,`#&$0`#j%Cave Eye',22,8,3,15,(200,60,`#o$)
h_BOSS=(`$x(King',70`$e%0,(110,80,180`#Q$GRASS=(40,110,50)
h_STONE=(60,55`#6&BASE={'.':`#V&,'>`#/+<`#/+ `#/+T`#/+H`#/+~':(4`%u%90),'#':(30,28,35),':':`$P&,'B`#/)}
h_LEAF=(25,85,35`$f%RK=(9`%w$3`$x$LINE=(45,40,38)
h_WOOD=`(3$7`#Z%def h_shapes(m,x,y,ch,out):
 px=x*h_T
 py=20+y`#0%if ch in '.>< ':
  h=(x*7+y*13)%5
  if h==2:
   out.append((0,(24`)2%90),0,(px+14,py+4,2,2)))
  el`#e%4`#e530,12`*@%`#f&`#e$15`#f)`#e$ch=='T`$k$`#g.`&C%`#_&8`#_$4,4,6`$F%`#O,1,`((%,1`$t%0,py+8,8`$//~`$/%=(x*5+y*3)%8`$?1`*~$160,235`%((o`#t%6,1`#v/H`%&3`,:$1`+v$`%k)2,py+9,16,1`#h%`%//(170,50,40),2,([px,`%8&x+20],[`#d$py`#l$]`#g22`&D43,4,7`#O4(250,`(^$4`(Y/1,3,3`#VH13`#W/`&0*C'or`#-%c`&:$if m`*u6`,X%`#w%,py,h_T`($&`+u%`#r$`*m460,40,`&}*`$W$6,14`&})`&~16`0*%`%h/7,12,9`#V32,GOLD`&8-`13$`,W)se`$e4100,7`/*$`#_2`+q%`&@*#`%L$for yy in(6,13)`#z450,47,58`#y&,py+y`&E,`#x*:`-K5`(#8`#[*B`#[M`&v1`47*`.--11`..&`&t4`,E%+3,px+6`,L*14`#)$7`,R%4,py-1,py`)H$`#-%4`,_33,RE`(n(5`.Y%`,&5`#K,1`.A$`#L)`3P%base(m,ch):`3/,C`,$%return `5R&`,4$<2`)t$ `5/&
`#G*BASE.get(ch,`#U&`$0(hero(x,y`4V?`%+,5`4%&0`3?&`(&,5,4`%]$`#S,6,`6)%`%_&6`(O$,8`&-&`#M.BLAC`05-5,1`)Q&`#L:1`(L$`#M8(6`59%2`,g*`$M$9,8`15&`#S24`-:,`$}%6,3`%M5`#R1`$X%`#S:210,215,22`4m)1`*6$4,2`+Y&`#U.`/N+`8(%`<]$`/N$`)*%paint(ops):
 ops.sort(key=lambda o:(o[0],o[1],o[2],o[3][1]if o[2]==0`*H%0`#<%0]))
 last=None
`/l$layer,c,kind,a in ops`3A&kind==0`0)$if`#^$ and`#,$[0]==(`#c&)and(`#9$2]==a[1]`#5*4`#5$3`#5+1]+`#+$3`#=$0]`11%`#{%3]+=a[2]`#5$continue`$J+`#N%rect`#q(,`$B&`#+%3`#+&4`#+&0][1]`3j$`%k$[`$~),a[0],a[1],a[2],a[3]`$@$`$?+`$>,`$=Y`(*%`&i*1`#t$circ(`$M/c`52-col(`#5$ fill_poly`#T*)`03$`$i(`$hQ`*p%cells(g,todo,wit`0.%):
 mp=g.maps[g.m]`+2$=[]
 rows={}`*G%x,y in todo`$O$ows.setdefault(y,[])`,K(x)`#W%`#U$row`*q$xs=sorted(rows[y`&M$i=0
  while i<len(x`,]$  c=`3*&g.m,mp[y][xs[i]`(+%j=i+1
 `#_(j`#_(and xs[j]==xs[j-1]+1 and(`#r4j]])==c`+E&j+=`#w$ops`.c)-1,c,0,(`$D$*h_T,`3:(,(j-i)`#-$h_T`:p&i=j`&E5`Dq)g.`Ds%`$M&],ops`)C%`(P)`#S%`4g$g.x,g.y`#H&`/u,`)9&draw_map(g,after_msg=False):
 r0,r1=(0,10`$.%`#G)`)&$0=max(0,(MSG[0]-20)//h_T)
  r1=min(1`#A)+MSG[1`#H*+1`:o$`+s%h_HUD[0]`,X&`*z*[(x,y)`)r*ange(`$c$`#8$x`#8*16)],r0<=g.y<r1`%b$hud(g)
`$($=[None]`7z(`#=$:
 t=(`NA&`+q$[:13],'HP'+str(g.hp)+'/`#1(mhp),'LV`#3(lv)+' `#P)pot)`&A%t==`%E(`:#*`#=$`#:(is Non`%q$`.8$0,0,3`N4$`7^%`;M$ld=('',`#%$`&G+old`$))`*<%i,x,c in((0,4`5g$),(1,140,WHITE),(2,2`#1)`+g$if t[i]!=old[i`$t$ text(x,15,`#8%`$V*`#>+t[i`0v%`(x)t
class h_Game:
 pass`=3)r`<$$w,v,mx,`-/$f`*G&min(w,int(w*v/mx)))if v>`6k(`&J$v>`63$`#W%2,f)
`&J%x,y,f,6`$T$`#4%+f,y,w-f,6,DARK`,@(foe_art(f):
 c=f[5]
 n=f`&V$if n==`SJ&:
`3V&`MK$5,30`3Q%`$)$19`#7$`OW$`#:$`Be$n==`Sj$`#_$`3q(`3p*[17`SO&`#+%],[80,10`BU%20`1+$`$=)10`EB$`$&.`TL(`$i-100,2`#M%`#8&4`QR$1`$~-7`G[%30,3`#z.`T~)`%e8`#7,14`*D&`#;/`??&`+M+`&@&5,`L}%6`#r060,18`#7&ol(`+]$`&G.200,205,212`&O%28,235,240],[4`$m$42,28,42`#/$5`&Z$`$C$208`V2$,5,RE`#~$`#:%27`#:.`)Y710,92,3`,N*`#:%3`#:/`(X<45,83,2`#O(`,](ttle(g,`+4$name,fhp,fat,fdf,xp=(f[0],f[1],f[2],f[3],f[4])
 mx=fhp
 cls()
 rbox(15`):$14`TE&0,f[5]`$B*`,O-
 c`.f$26,name+' appears!'`/{%
 opts=['Attack','Potion','Run']
 sel=0
 log=''
`/Z%12,56,'You'`*+)`#<(8`$5%[:1`%>$`(d$`1D$`4B*`M:%c=GOLD if i==sel`/G%`#t$
 `%^&0+i*102,154,96,24,`*O&`$8$58`#B%-len(opts[i])*5,172,`#2&`#Q$was`6>&`:o%Tru`+h$now=`4|$`(S$sel,log`Qo&was `4:& or was[0]!=now`4l&`1~&12,62`(I$`#n$`5c$,GREEN`#n:1`#n&1`#n/9`#n%fhp,mx`+}(`#h*not`#l%and`#m$2]!=sel`#j$`&}((`#<%,sel`<g&`(&>  edge`();`(+O`%f73]!=lo`;a$`%C3`$u%`*O%0,202,`#W%[:31`6j1`#E&log`#B%GREY)
 `)L$now
  k=wkey(`$X&k==LEFT`$.$sel=(sel-1)%3`Em2k==RIGH`#O.+`#O7!=OK`E&&`#;,sel`IM(d`7>$1,g.atk+`o<%.randint(0,3)-fdf`Eb%hp-=d`FX$og='You hit`);$`<+%d)+'.'`b.(`$.$`Fo%if `<G$`$>(`#f%No p`.s$s left`#^$`Ik.`#X$-`Bk%g.hp`?t$`+t%g.hp+25`H5%`$Y(feel better`$R*f is `hh%`$G$log="You can't run from him!"`#X(`%{+om()<0.6`I}&`Sy$Tr`$m$`H|)`#y$Couldn't get away."`(-%fhp<`%m&g.xp+=xp
   msg=[`%)$won. +`&^%xp)+' XP'`KP$`/]%g.xp>=g.lv*1`^i%`#6$-`#6(`#5&lv`F1& `&<$+=8`#0&atk+=`#I(dfn`#J*h`I_$h`$Z$ msg`Fj('Level up! LV`)E&`A]$`(0$message(msg`4F(defeated'`#D$`&?.`*r(fat`*p5`$_$)
`$Z%`*r%log=log+' It hits`*r0`*b$`&r*`$](`&j%fainted...'],'Game over`$h-`G<$`Sg(lay():
 g=`A/%()
 `Lm%=[[list(r`E{$r in mp]for mp in `x>%]`#R$=0
 `Hr&=(4,4`#j$`&|(=3`#A$atk=6
`(F%=1
`(w$`#+%xp`#e%pot=1
 steps=0`9.)`IQ,)
`%d+The `pv+ took',"the village's light.",'Bring it back!'],'TINY QUEST'`$1/,True)`6t0`1W1CLR`/6(`$b*ENTER: quit adventure','CLEAR: keep going'],'Quit?')=`1K(`H.) `$Z5`/w-dx,dy={`3*$(-1,0),`2f%(`#/$UP:(0,-1),DOWN:(0,1)}`_^$k,(0,0`hm(dx==0`7=$dy`1E(`$0+nx,ny=(g.x+d`)G$+dy)
 `S#1`?}$x>=16 or nx<`/G(m+=1`#@+else-`1x&x=0`#=/ 15`%o0`%j0ch=mp[ny][nx`$B&`ci&T~`hW%`5-/`oB+`/H/`Mk)`-J1rest by the fire.','HP`#:$ored`-b$Cottage`-_%`(oA`ls/`%4*='c`5:$`,[$`1>&`/$/ound a`5p&`+q$Chest`$DO`j7%`Nt%`CU)`5Y%`<W&`0R&`Kk%  `.*(`2i$`-z-`-W$`+b&s to','`-z+. You did it`-m%HE END`$|%`,>+`#-)ox,o`*t%,g.`*n$`0E)`+4$)`SU$`SF*`#S$)]`%b)`0*$`&T%`%P$FO`RZ&and`#@%>6`X9$`7h212`%p%`0o)`,$%ot`&>,`#Z&choice(`$*+`Q-%`.b8)
h_RULES='Walk`*[$meadow, woods`-{$cave. Rest at`#G$c`*i%, open chests`<9$`;Z&,`.X%`6Z$`#T$`2K+.'
h_KEYS=['Ar`]K$ walk','Fights: Left/R`))$+ `1M$`1=*quit'`VL(main`5X$`2M.c=home('GHRPG'`34-,`%d&,`$N%,('Play','Back'`uY)`/o&`&N)`6l(
`$>('''
GAMESRC['GHSIMON']=r'''import random
`#1&math
i_CX=160
i_CY=116
i_RO=84
i_RI=36
i_PADS=((UP,2,(30,130,50),(110,255,130)),(RIGHT,3,(150,30,30),(`#C$10,11`#G$DOWN,0`#l$60,1`#l%20,17`#p$)),(LEFT,1,(16`$5%2`#l(235,100)))
i_SHAPE=[]
def i_shapes():
 for q in range(4):
  xs=[]
  y`#+&for r,order in((i_RO,`#T%9)),(i_RI+3`#5&8,-1,-1))`#p$`#a$i in `#d$`#6$ a=math.pi/2*(q+i/8)`#;$dx=r*`#>$cos(a`#8&y`#8(sin`#8(xs.append(int(i_CX+(max(dx,4)if`%D$(0,3)else min(dx,-5)))`#e%y`#e0Y`#e&y`#e-1`#e+y`#e*`&k&`#h((xs,ys))`&x&gap`&v%d=(15,`#%$)
 rec`$v%-4,i_CY-i_RO-1,8,`#,$`&]$1,d`#M3+i_RI`#K=`#p&`#|$4`#K-8`#M.`#p%`#K9col(d)`)~%`)Q$`#R&`#F$`#*$2`)<$draw_circle`#|$`#w$,r`%u(pad(i,lit):
 k,q,dim,bright=`-#%[i]`$8%`#9% if lit `(-$dim)
 `&n$=`()&[q]
 fill_poly`(/&`$7&body`(.$if not`(](:`(i$`,E(
 circ`$x+i_RO+8,(6`-^$65)`#F75,`)**`&1&`,)$`-1,`%d(False)
`)k)
 ring`#w.I`#u+,3,(70,70,75`*K)score(n`%B(:
  text(66,17,str(n-1),BLACK)
`&J$`#G)204,17,'CLEAR quit',GREY)`#j)`#B$Score')
`#~1))`$?*s=`$6(`#b(`*y$len(s)*5`+M%7,s,(25,25,28)`$Y+`&e2I-6`#N.`$+&`$Q(`$(7WHITE`&4(flash(i,`*g$`(5(True)
 pause(t`(>$`(N.`#=%0.12`.K*me`*@$cl`(h$`*R(
 seq`28$while Tru`%?$`(U(`$k$eq`/T$seq`/P(`5f%.randint`0p$)
 `$B)5`&Z$=max(0.18,0.5`%Z%eq)*0.02)`3O&`*h$seq`2l$`%a,`#C&want`#F,k=wke`%($  if k==CLR`3N%return
   got=-1`3x-`+r,`#^$`.=)[0]==k`#;%`#^$i`$%&got<0`#;%`#v$2`#;*>=`#<&`$~(got,0.`29$`#G(!=want`$:)`#Y, pass`#-$message(['You got '+str`(5)-1)+' in a row.'],'Wrong color!'`4o%`%m&i_RULES='Watch the`#J%s l`0j$up, then repeat them in`#L$same`77%. Each round adds one more.'
i_KEYS=['Up: green   Right: red','Down: blue  Left: yellow'`.L&:`.M%`9o(main`+K$`+2.c=home('GHSIMON','`#+&`%U&,`$S%,('Play','Back'`71%f c`(y&`)z)`,Z(
`$;('''
GAMESRC['GHSOLI']=r'''j_CW=40
j_CHT=30
j_TOPY=4
j_TABY`#?%RANKS=('','A','2','3','4','5','6','7','8','9','10','J','Q','K')
j_CARD=(245,`#&%0)
j_BACK=(40,80,16`#6$FELT=(15,70,40)
def j_cx(c):
 return 6+c*44
j_SUITS=(((0,1,7,3),(2,1,3,5),(1,0,2`#-$4`#-)3,1,1,6)),(`#M-2,5`#c$3,`#o$),(0,3,7,1`#M$`#/%2`#M-2`#o$`$(%`#-(`#c%`#w%6,5`#c&`#y,2,2`#c$5`#-)2,0,3`$%&`#W%`$F%`#c$`%s(suit(x,y,s,k=1):
 c=RED if s<2 else BLACK
 for a,b,w,h in `&<&[s]:
  rect(x+a*k,y+b*k,w*k,h*k,c`$4(body`$4$h,`(1&`#U$1,y,j_CW-2,h,`$4$)`#?(,y+1`#?$,h-2`#?/+1`#A)-2`#C$`$3)card`$3$cd,h=`+3$):
 if cd is None:
  col((60,110,80))
  draw_`$G(`$&%`$.$HT-1)`%W$turn
 r,s,up=cd`#|$not up:
 `%W.`+:%)
  if h>=12:
 `&B)4,y+4`$-%8,h-8,lt(`#U%,0.15`$Y$`#O(6,y+6`$Y&2,h-12`$&+`$_(`$F/CARD)`$k$h>=14:
  text(x+3,y+14,`.$&[r],`)W5)`%A$`*-%+`$F%1`%$$s`#|)`&2$`%k%`#K&1`$&$5,s,2`)_)acks(x,ys,i,j):
 y0=ys[i]
 h=ys[j]-y0+4`)@,0`){:0`)|>`#B(`)}&`&?)for k in range(i+1`$V%`#_+s[k]`#a(1`$$(class j_G:
 pass`%F&new():
 g=j_G()
 deck=[[r,s,False]for s`$;*4)for r`#4*1,14)]
 shuffle(deck)
 g.tab=[]`$~%c`#S*7`$z$pile=[deck.pop(`#z$i`#H*c+1)]`#J&[-1][2]=True
 `#~%.append(pile`$7$stock=deck
 g.waste`$G$g.found=[[],`#%(]`2m)g`%y&layout`#s%:
 dn,fu=(5,15)
 while Tru`-q$ys`#}$ y=`58%
 `%R%d in`${$`,y$ys`$n(y`,[$y+=fu`.e%[2]`+P$dn`-S%not`#[$ or ys[-1]+`+C$<=208 or fu<=8`-v&`%&$ys
  fu-=1`#g%fu<`.<&dn=3`%D&`/R$col(g,c,drawn):
`(6%`&Z$[c]
 x=`5u&
 ys=`%{.
 n=len`#0(d=`#j$`#Z$start=0`-@$`1($not`1,$ and n:
  old=d[0]
 `&X&`#W$<min(len(old),n)and old[`#@$]==ys`#.&`%?$`#.$+`%W$`$<%min(`#-$,max(0,`#s/-1)`.}%`&m(`.}%`33&`(p%,None)
  bottom`)+&`(1%
`0,$:`#@*`(N,`(*%`%a3<len(d[0])and`$k%==n-`6f$`.?(,`#v%-`2A%,6,`:C%`3?$=`#V$`&@)i<`&X$ j=i
 `#8(j<n-1 and(`%L([j][2]`$.% j`&=% if j>i+1`#9&`1P0`#9$i=j`#+$contin`-T$`6L+s[i],`$*$i`0:$HT if i`%B$`3?%ys[i+1]-`#N$+4`#z$i`$J$`&7(`&3$or`&^&<d[1`9/+`%}&`%{%210-`#3)`&)&`*u(=(ys`#P&`3o(top_state(g,s`89&s==0`$(%`,x$len(`/^&)>0
 p=`/^&`#O&`%6&`/h&[s-3`/^*tuple(p[-1])if p`#N%None`-U,slot`$J(`-A&`6)&`$U(`+%,OPY,[1,0`38&if`1I(`$&*`8*,`${E`$*0`$~$`$}.`$[&>`*A+`*8$`7i,`#c%+8,s-3`7o*frame`9R&top`3c$):
 t=2 if to`$0&0
 r=[(x-2,y-t,2,h+t+2),`99&`#80,y+`:I$W,2)]`$i$to`<4$r`2o((x,y`7r$`#G$`8:$`(U$r`$e&marks(g,s,`1i$`:e$7`)b+`%,(`(Q&`&5(`>O%`&t%tab[s-7`$J%`&-$`#e9-7`#g$AB`#g*`2h-)
 i=`0~%`2k$)-n`%#*`#p2`-Z%`0F,`-B%,i==`En)fits_`)O$(cd,f`.0$`@W)[1]!=f`$|+`*_$`$=)cd[0]==`4@$`8a$0]+1 if`6;%`(s$1`$2-tab(cd`$.,`2|,`#{.13
 t=`$$(`-2*[2]and t`#H$`#O$+`+$%(t[1]<2)!=(`%+$<2`EQ)tak`.j$rc`).*rc==`1R$`#~%[`,a&[-1`:(,`)$%rc-7][-n:]`#v&remov`#x:`#q&`<0%`4v*`)w)`#u$
  del p`#}%`34$p`-<*`<K&`3X%`#1(`<Y%`%E&ry_`$O,,dst`G{$ards=`%g/`$l$3<=dst<=6:`;(&!=1 or`(C$`)q.ards[0],dst-3,`/Y(`#1$`$]&`)x.`&*2`%x$`#Z,`-v(`$%(`0z*`=W$`4]%st>=7`7k$dst!=src`#0$`*K,`$g(`&d%dst-7`$^%`$M6`#H*.ext`$K)`$H1`%A-`+h&aceup(g`J^%n=0`Ae&`?4$`=@(`&e&`>|$`&1$n`6y$`#t&n`#p&game`CM)`CY$
 cls(`6c)cur=7
 depth=1
 held=`5?$ cols=[None]*7
 tops=[-1`#0$shown`A($`A=.want`A?%if`#q$`$g$want+=[(r,WHITE`DV*`2-*held[0]`#+%1]`Cl$`#Z*GOLD`#Y4cur,`%,$`$9(`9i)`/T&]
  busy=want!=`%($`Bz&r,`EP$`#6$`$r$if(r,c)not in`$G$`<#%`:G$r[0],r[1],r[2],r[3]`=H+`G-(`SB$3,4,5,6`+e%st=`:G0`=-&st!=tops`Pb& `9H1`#8$`#E&=st`#2$`%=$`Fm&`Gc5`/;)c]`$2&cols[c]`<w+`#5&[2]!=[`;+%cd`&y$`F(&`$[.`DY(col`$a&`#f&=`#+&+(`#k6,`#Q%`%$,if`#2$`$*$`(D+`(,Cc`#r$`+,%want`#r%sum(`Cr$f`$D$f`-#%`/O$))==5`F{%message(['All 52`1I% are home.'],'You win!'`Q?&`<o% k=wkey()`F5&cur`$C%k==CLR`*E&`,E*`-B,`B+/if`$R+ENTER: quit this game','CLEAR: keep playing'],'Quit?')==OK`&?(`$l&`.y.`(Z%`._+`*N%`.b)`&Y(`.K$`$j,`%C%LEF`R<$`/h$cur-`9*$cu`4=%`,:$7)`-]$cur+6`*p(ur==`((%`#/$1
  el`#w%RIG`S6%`#x(`:#%`#x+6,13`#y)-`#y83`#y+DOWN`41$cur`>-%`1f%+`(]%`#J(UP`#H(>=`#I%if`2-%<`3O,ur-7`K-$`06,`$C%`#P$`Gf&`8{(`&4*7`$t&-7!=`VA&`%m,`$r,`6=&(`#v$>`Is&`#0$`N_%`#W(`)D&`1l/`$A%`&-(`Dy$`#3%`Da&`#4& cd=`#5&`:~(`#:&`Ru+  `;H*`8G(d`#M&`%T* `S.)`<i(::`>#$`##$`6o,`$K-`$5&`9s(`$6+`+$&`%Z%`%8$`>S$`#B(`#f&`->$(1,`]_$`#P*`9r(`1x&ur-7]and(`),1>=`&n$`Lc&`#t&`5^)`#z$`%U*`:($=held`.c3`=W3cur)`(l+SECOND`$d$`(m1src=cur`(t)`=_$`%:&else-`NG(src>=0`*($`@*%`&-, or(`#D$`%q,`@(%)`%T&`28)`Yd(`*)*`%311,3+f`#D( break`;h&ur!=o`1_&`;,)`#=&`>/)`+p$max(1,`(71`,++`Fx$`#F4
j_RULES='Build four`E*$s from Ace to King, one per suit. In the columns, stack`4V&down in alternating colors.'
j_KEYS=['Arrows: move   `3k&pick/put','Up/D`#o(`$3&: more`$1%',`4D% o`$U%deck:`Q9$','2nd: send`#O$ to`Ls$`%L$`4f*quit'`Ep(main`?U$`>U.c=home('GHSOLI','SOLITAIRE',`&V&,`%D%,('Play','Back'`fW$if c<`/o%`5W)`@i(
`$>('''
GAMESRC['GHSUDOKU']=r'''import random
k_S=20
k_X0`#+%Y0=15
k_INK=(20,`#%$)
k_PEN=(40,90,200)
def k_make(holes):
 base=3
 r=list(range(3))
 rows=[g*3+i for g in sample(r,3)for i`#7/]
 col`#ZTnums=`#6(`$O$1,10),9)
 sol=[nums[(base*(rr%base)+rr//base+cc)%9]for rr in`%.$`$I$cc in`$a$]
 puz=sol[:]
`#@$`$R-`$?$81),`&4) puz[i]=0
 return puz`&_&valid(b):`#o+`#h%9`#_$row=set(b[i*9:i*9+9])
  colm`#<(::`#7%bx=i%3*3+i//3*27
  box`#I$(b[bx+o`%K$o in(0,1,2,9,10,11,18,19,20)))
 `$S$s in(row,colm,box`$X$ if s!`#w$`&w+`#>%`%M(False`%[)True`%]&clash(b,i):
 v=b[i]
 if not v`%^$`#f.=i//9
 c=i%9`&6%j`&6*81`$@$if j!=i and b[j]==`#o$`#;$//9==r or j%9==c or(j//27==i//27`#X$j%9//3==c//3`%9.`%+$`$_.k_SHOWN={}`%D(ell(b,fixed,i,cur):
 x=k_X0+i%9*k_S
 y=k_Y0+i//`#4&bg=k_FIX if `#a$[i]else WHITE`&5*c=(`.8$`#K1RED i`&n.`#;$`.U$)if v `#3$None
 on=i==cur
 old=`%7&.get(i)`(B$old is`#R$ or old[0]!`&f%rect(x+1,y+1,k_S-2`#)&bg)
 `#w$`$1%`$A$and(`#s31]!=c`&z$text(x+5,y+16,str(v),c`$Q92]!=on:
  k=GOL`%j$on`%O%bg`$k62,k)`#=.k_S-3`#A93,`%D%6`#=-`#W%`#A0`&U&[i]=(v,c,on)
`)2$=(236,238,246`2k(first`*.)`*,&`0U$`/80c=0
  while c<9`+{(`)]%r*9+c]`+R%e=c`#+$`#N%e<9`+}$`#K*e`#K& e+=1`,+&ct(`+F$c*k_S,`+A$r`#.$(e-c)`#8&S,`%9$)`#W$c=e
  `(%$`#t%c`#s$k_grid()`%67row=''.join([(str(b`%-&)if `#/(`(}$' ')+' '`3H$`#m,`1j$if row.strip(`.@%`*E$`%7$5`%3++16,row.r`#N&,`-2$`$l&`39+`0%&`-[(`)-/`-je,`/t$`*.$`/g-cur`)_$`)y&`&W%`5&210`)n&`$T)i%3==0`$+$(150,`#&&)
  t=2`#E/ 1`&M%t==2`&F$`)Z*i*k_S-1`&L$-1`,&%*9+2`-x$`#L+`#F&`#S+`#J%`#L&`)r)col(`#_%draw_line`$3+`#i$,`#3/+`#q$`#W3`$<+`#W%`#L$`#9+`&O)am`<7,=`<I-
`(w%=[v!=0`&s$v in b]
 cls(`3@$)
 rbox(208,12,106,30,8,`)1$,2,(225,235,252))
`*}%222,33,'SUDOKU'`#P%`#@)14,70,'0-9 type',GREY`#A,90,'ENTER +1`#A2110,'DEL eras`#c3130,'CLEAR quit`#D)`4Q(clear()
 cur=0
`/b&`+v%cur`/V$cur`.b&`1&2`#U(Tru`)?$k=wkey(`4h(`5j$`,Y$==LEFT`0^$cur%`19%cur-`0V$el`#G%RIGH`#H+<8`#J(`1#%`#J(UP`#G(>`#E)-=9`#E+DOWN`#G(<7`,)%`#l$`#H,CLR`,B&turn`#<(not`%t/ v=-`2J$if k in NUMS`1q%v=NUMS[k]`2-%`#}%OK`#@(b`#i$%9+`#d$`$i)EL`#D(0`#|&v>=0`#7%`#V%=v`#0$`0y6`#V%`$t*i`4@(`;r6`#?$if 0`#V$in b`&2$`AD-    message(['Every row, column and','box is complete.'],'Solved!'`$1%`&f*`$U/ol`*>(`1|9k_RULES='Fill the grid so e`$Z4 3x3 box has`#Q$numbers 1 to 9 once. Red`#<)`3o$.'
k_KEYS=['Arrows: move'`..$:`./$ a`#W&'`.$&: count up  DEL:`-s(`-^%:`-_%]`Ht)in`41$`,x.c=home('GH`/Z(`/e+`%m$,`$e%,('Easy','Medium','Hard','Back'`Db$if c<`*?%`(1+`2%$(36,46,54)[c])
`$Z('''
GAMESRC['GHTTT']=r'''import random
l_LINES=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5`#;&4`#+$2,4,6))
l_X0=85
l_Y0=28
l_S=50
l_INK=(20,`#%$)
def l_winner(b):
 for a,c,d in `$[&:
  if b[a]and`#+$==b[c`#)$d]:
   return`#?$
 if 0 not in b:
`#A)3
`#-(0`$E&cpu`$B*who in(2,1):
 `$U9 v=[b[a],b[c],b[d]]
 `$n$v.count(who)==2 and`#7)0)==1`#d$`$N&(`$%$)[v.index(0)`%+%b[4]==0`%(+4
 free=[i`$_$i in(0,2,6,8)`#T$i]==0`#c%not`#P$`%2$`#X/ range(9`#X.`$/&`)l%.choice(free`(_(frame(i,c):
 x=l_X0+i%3*l_S+3
 y=l_Y0+i//`#6)w=l_S-6
 rect(x+3,y,w-6,3,c)`#8,+w-3`#<1,y+3,`#:%`#Q+w-3`#<.`)%&ell(b,i,cur,full=True`$u2`$s1
 m=b[i`&M+ull:
 `%c+GOLD if i==cur else WHITE)
 elif m`)8&col(`,6$)
  a,e=(12,l_S-12)
  fill_poly([x+a-1,x+a+2,x+e+1,x+e-2],[y+a,`#&%e,y+e]`#]1e-`#V*`#d%a-1`#]6`$i(2`*Q$ing(x+l_S//2,y`#,(15,`%#$,3,`%E&`&k%grid(`,n(`*y$1,2`,l$`(H$`&n%*`%N$,l_Y0,3,l_S*3`#s%)`#K,`#C$`#P+S*3`#Q$`#K$l_SHOWN=['']`$E&status(s):
 o=`#D&[`,3&s==o`,p*`#6$len(s)==len(o`$o$d=[k`%*$k`,I*`#I%)if s[k]!=o[k`.Y$`(i$d[0],d[-1]+1)
  x=160-`#V%*5+a*10
  text(x,203,o[a:e]`&K(`#>-s`#>%`%{(els`..$c`#F$`#a$`#Z*`#8*s`#T)`%d*=s`(L(ame(vs_cpu):
 b=[0]*9
 cls(`#q(`#Z+''
`)()
 cur=4
 turn=1
`,3)cur`,5$)
 while Tru`$u$w=`3x+`3_%w`1N$msg="It's a draw"if w==3`,o%'X wins!'`#9%1`#9&Calculator`#B$'if `%:%`#C&O`#Y&
  `)c*msg+' - ENTER')
  `$p&wkey()`4g%(OK,CLR`)W$  pass`5:*`%(%`$3&and`%q%`,f%`$1*'Thinking...`$0%pause(0.3`#1$m=`5S(
   b[m]=2`#f%`0h&m,cur`#@$`&x(  continue`0:$`$3&('X'if`$O&`&2(O')+' to move`$I$k=`%Q%
  old=cur`%9%k==LEFT`%:$cur%3>`5P$ cur-`$?$`/9$k==RIGH`#J+<`%c%cur+`#J-UP`#G(>`#E)-=3`#E+DOWN`#G(<6`#k*`#G,CLR`9H+`#<+OK`#_$b[cur`7J(`#1(`#N&`%~%3-`#2(`&l)cur`&n(if cur!=old`(x&`#G&old`#K$False`(=$`#d0`#>(l_RULES='Get three in a row (across, down or diagonal) before the other player. Play`#:$c`,1*or`+0$ to a friend.'
l_KEYS=['Arrows:`)K%,'`,-$: place your mark','CLEAR: quit`2N)main`3r$`.J.c=home('GHTTT','TIC-TAC-TOE',`%f&,`$K%,('vs Calc','2`%1$ers','Back')`(%(<`(e%`)0)`0k&c==0)
`$R('''
H_main()
