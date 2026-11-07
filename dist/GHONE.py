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
YELLOW=(240,220,60)
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
def block(x,y,w,h,c,e=2):
 rect(x,y,w,h,c)
 rect(x,y,w,e,lt(c))
 rect(x,y,e,h,lt(c))
 rect(x,y+h-e,w,e,dk(c))
 rect(x+w-e,y+e,e,h-e,dk(c))
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
def rbox(x,y,w,h,r,c,t=2,inner=BLACK):
 rrect(x,y,w,h,r,c)
 rrect(x+t,y+t,w-2*t,h-2*t,max(r-t,2),inner)
def edge(x,y,w,h,r,c,t=2,inner=BLACK):
 col(c)
 fr(x+r,y,w-2*r,t)
 fr(x+r,y+h-t,w-2*r,t)
 fr(x,y+r,t,h-2*r)
 fr(x+w-t,y+r,t,h-2*r)
 for cx,cy,sx,sy in((x+r,y+r,1,1),(x+w-r-1,y+r,-1,1),(x+r,y+h-r-1,1,-1),(x+w-r-1,y+h-r-1,-1,-1)):
  col(c)
  fill_circle(cx,cy,r)
  col(inner)
  fill_circle(cx,cy,max(r-t,2))
  ax=cx+1 if sx>0 else cx-r
  ay=y+t if sy>0 else cy-r
  fr(ax,ay,r,cy+r+1-ay if sy>0 else y+h-t-ay)
  ax=x+t if sx>0 else cx-r
  ay=cy+1 if sy>0 else cy-r
  fr(ax,ay,cx+r+1-ax if sx>0 else x+w-t-ax,r)
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
  rbox(60,y,200,24,8,c)
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
  while True:
   for i in range(n):
    x=10+i*(bw+8)
    c=GOLD if i==sel else WHITE
    if first:
     rbox(x,166,bw,28,10,c)
    else:
     edge(x,166,bw,28,10,c)
    text(x+bw//2-len(opts[i])*5,186,opts[i],c)
   first=False
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
I_BG={'GHSOLI':(25,110,55),'GHBLOCKS':(40,30,90),'GHSUDOKU':I_WHITE,'GHANIM':I_WHITE,'GHFLAP':(110,195,240),'GHTTT':I_WHITE,'GHMERGE':(187,173,160),'GHPONG':(30,85,165),'GHBREAK':(30,70,170),'GHHANG':I_WHITE}
I_FONT={'0':'111101101101111','1':'010110010010111','2':'111001111100111','3':'111001111001111','4':'101101111001001','5':'111100111001111','6':'111100111101111','7':'111001001001001','8':'111101111101111','9':'111101111001111'}
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
def I_digits(x,y,s,c,p=2):
 I_c_(c)
 for i,ch in enumerate(s):
  bits=I_FONT[ch]
  for n in range(15):
   if bits[n]=='1':
    fill_rect(x+i*4*p+n%3*p-1,y+n//3*p-1,p+1,p+1)
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
def I_g2048(x,y,c):
 I_rr(x-20,y-12,41,28,4,(200,160,30))
 I_rr(x-20,y-14,41,28,4,(237,194,46))
 I_digits(x-14,y-5,'2048',I_WHITE)
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
I_ICONS={'GHSOLI':I_solitaire,'GHBLOCKS':I_blocks,'GHSUDOKU':I_sudoku,'GHANIM':I_anim,'GHFLAP':I_flap,'GHTTT':I_ttt,'GHMERGE':I_g2048,'GHPONG':I_pong,'GHBREAK':I_breakout,'GHRPG':I_rpg,'GHSIMON':I_simon,'GHHANG':I_hangman,'GHCRYPT':I_crypt,'*keys':I_keys,'*wipe':I_wipe,'*about':I_about}
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
H_CATS=[('Arcade',[('Wing It','GHFLAP'),('Pong','GHPONG'),('Breakout','GHBREAK')]),('Puzzle',[('Stack Drop','GHBLOCKS'),('2048','GHMERGE'),('Sudoku','GHSUDOKU'),('Simon','GHSIMON')]),('Classics',[('Solitaire','GHSOLI'),('Tic-Tac-Toe','GHTTT'),('Hangman','GHHANG')]),('Adventure',[('Tiny Quest','GHRPG'),('Encrypted Demo','GHCRYPT')]),('Create',[('Animation Studio','GHANIM')]),('Settings',[('Key Test','*keys'),('Delete All Saves','*wipe'),('About','*about')])]
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
  rbox(50,y,220,H_BAR_H,9,c)
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
 rbox(90,8,140,24,9,WHITE)
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
a_INK=(20,`#%$)
a_HI=`%-$120,`#4$MAXB=60000
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
 v=`$2$`6c$if v==`*,(onion`6Q$s.ci>0`&0&pr`4s(`#{&16+`#9(`$4)v`$4&pai`$5%,`*<$x=a_CX+i%`<&(P
 y=a_CY+i//`#8+if v>=16`8N%`<4$[v-16]
  w`#3&0]`$N$ct(x,y,a_P,1,w)`#7++a_P-1`#=51,`#;$-2`#;,`#S&`#A8`#=%`#;%`#)%((c[0]+510)//3,(c[1`#1-2`#1)))
`6T)`%#-`#&&AL[v]`)O$shown[i]=`&[(refresh(s,src`+g$):
 runs={}
 `(g$=[]
 hide=s.hide`)w%r`07*`@-$`07$base=r*`(+$`&w$`4j*c<`#9$`9Q%=base+`49$v=src[i]if src`+r,`,5%`*_+`:3&`(}$ or(i==hide`*a&`%M)=`)v$`#O%`#:*!=v`#9%`%F%`7[((i,v)`$#$ c`:y(`;v+ e`6-%`-#, `%D(e`%D+ j`%E%`#B$ w`%F$j`%FBj`$E%if w!=v or(j`%F3j`%F+`;y)`%Q-j`%Q+`$x%Tr`%2% `#k,v`#5$e`%Z&if`#O%`&F)v`):$uns`#o&runs[v]`&D)c,r,e-c`&H&`=X*`#L(=[`#F)`:/&`*:&`#~-for c,r,n`#8([v`>Y%`+r$`.o$c*`+q%CY+r`#.$n`#4&`,+-for i,`$%$`):$`7J%`/h,`4M(ursor`1p%`/x&s.cx`/u-s.cy`#4%`1S(`#5&CWD`#Q$]
 col(BLACK`&E((0,3,6,15)`)=$WHITE)
 draw_`.3,`/$(`..$`-M&`$&-`3e(n`$w,`6,$`#I-`#c(-1
`%[-`-&+`%g(label(s,key,x,y,t,c,bg=`$o%:
 old=s.lab.get(key`$h$lab[key]=(t,c`62%old`9X,tex`%H%`#D%`8&)o,oc=old`(V%k`/p*max(len(o),len(t))`<6%=o[k]if k`8J$o`&Z%' '
  b=t`#?,t`#?,if a!=b`Eo(a!=' '`+;%`37&k*10,y-12,10,16,bg`01(b`#P+`%9%`#P&,b`%>%`F;$oc!`IQ%`#S,`#R3`(&%swatch(s,c,sel=-`>d$x=210+c%4*26
 y=30+c//`#1%e=`LE$ if c==sel`/e%GOLD`#7(.co`#9&`(p$
`%K&-2,y-2,26,2,e`<m$`#9(+2`#:5,2,2`#7,+2`#8,`8v(lette`+%%`.D$`(|*16`(l$`%?.`%@/`7I.`Ni%`.M%c]`LX$`%D$`=W$`-B$GREY`(O$`-&.`OD& `&l-`$p(topba`,r&pct=`<m)*100//`Oj%
`,P+'fr',4,17,'Frame '+str`<6$+1)+'/`#3%`?T(),`(R$)`#h.ps',160,17,`#b%fps)+`#;%`%7&`#R+mem',236`$?$Mem`$=&pct)+'%',RE`)E$pct>9`?w&`#j%`%T%bot`%T$,a`9]$,b`9e)if a`.*,a=('Pen up','PEN DOWN','ERASER')[s.pen]
  ca=a_HI`5d%pen`6^(INK`;U*`#H&`%=-b1',6`U9$a,ca`%Y.b2',6,206,b or 'ENTER pen DEL eraser 2nd menu`&A(`--&id`*w&`5#&MX,22,320-`#/$154,`3/(`19%pop('on',`C<&`#9+sv`#9)`+{,
`$2&`.Y$s`$D,`#5&:`%?-on',210,150,'O`BI$'+`$=$`&M$`B[%`0w%off')`)a3sv`#h&68,'Saved '+(`*?%slot)`:#%lot`#n&-`#l)`$i%full`$e%cls(`%t(`8<)`5x$CY`#*%`Bz%+4,2,DARK`#K3+`?N$`8q(`#SB,`#*$`#U&`#G0+`#h)`#O9`<)&`MF1`72+`(w$`A_$`B%+`(k)`#.&`/4)
`,k+`#0$`8B)`8T(pda`1O(`8d-`$*2`#z-`*#,`$.@set_px`92$c`..&`Hk(!=c`YI&`L=/ s.undo`%}+`#V$)`Jr$`#a%`A[$`J^(`?d&s.changed`#4%`)|&i`)|(i0`;*2`:9%`#x$0]
 new`5p%`:-(==new`My,`$f9stack=`#l%`YD&tack`%R$=`#.$`-r$`4]&`%v*old`4g&`D.)`%U)new`5q$`Jx&`#_%x>`5=%`#y%`Aa&i-1`$#&x`DN%-`RR$`#H/`O@$`Ny%`eu%`#n4`#<$`#K(<a_N`#5%`#t4`#N(`(G.`(F5go`EN$`*x$`R#)`($$j`:#$i+`$}$`N+$`(Q%`%|(`(+-prv`7e%`Uz%`QC(`U}&`3x(`#[%`R,(`Fm$`#~%`#6)-1)if j`Qu(`-w2c`]1$`)T&`SK$`]+&dd_frame(s,blank`6:(`8z(>`8u%:
  message(['Memory is full.'`2#%, or delete `#y$s.'],"Can't add"`%*%broke`,?(`+<(`&_.`UD*`Tq,`UJ/`TR)`,C%`%g.if `%@$`&(0`,:).F.insert(i`P6$`Tv1ew)`UR4`Y})i+2`Vj+`#5(`Ug-new`Ue(`)o+`)4%`,i$`(W$i+`2O$`*t3del`(](`(V&`%o(`bk&`0O?`3i1`0Y0`YQ3`(0Fp`#K*`+/%`Y%-
 del`Ya&`Y1<`&F(key(nx)if p`=B(`<^(`]j+`&e%`/>%`$^(`1-%`#1(`64%`Pk-`&|%`(4(`bq*`(S(`%88`-D3`(a2play`6O(`+u+`6]1`@*)'Playing. Up/Down: speed','Any other key stops'`o}(`d>3`4%%Tru`&h$`3p$F[i`+E%1 or i`D_(`#b3`de0i`E:$`W],`b-$`D:B`D7? steps=max(1,12//`D-%`#<$op`UO)for q`GT*`#X$`TG%k=key`6E$ if k==UP`.)&fps<12`KE%`#1$`Vf(`:X-`KL&k==DOW`of%`#P$>`6/%`#0%`ff%`#^7`#W$k`+q$in(UP,DOWN`V2&`%6$`Uj)`V?)pause(1/12`8L(top`#U$`#F(i=`&R$%`&J(`hU)ey(`$%$`jX$`+j/s.ci`*l%`=X(
a_ITEMS=('Color','Fill area','Undo','Clear`3~%','Next`#0)Prev`#0)Add copy`#.&`3*$','Del`#S*lay','S`+i&`Ct%skin`5;&','Load`$1$w','Quit'`xa$X=202
a_MY`|#%MH=25
a_MV=6`-O&mbox`L,$w,h`>v%`L}&4,y,w-8,2`Pc$`#8*+h-2`#<1,y`C/$h-8`#Q,w`O;$`#<3`OR$,2`$%.w-4`#:42`$=$4`#Q6`#<+`%@&row(s,r,i,o`pt$y=a_M`Yn%MH
 c=`QV(`G@(`QP&`.w$`V?(('mb',r))`Al&`&?&a_MX+1,y,116,2`$Y%`Vg&`#T%`A_$`.j*('m',r),`#[$5,y+16,`*J&[i],c,`Yt$`%,)enu(s,sel`K%>`#X&`e12MV`+|$`K(*`%8(`K,(`#>.`#=,`2t,MENU `2q*pick',`M9%: do it  2nd: close')
 top=min`Xk$0,sel-2),16-`$^$`$u:`(o+top+`#)&`VD$`3W1k=w`12(`Dr$el`/5%`1;$`Ae%el=(sel-1)%16`XK(`0}&`#E-+`#E. in(LEFT,RIGHT`0]%`#N)8`#r/OK`0J-`#g*CLR,SECOND`#g*-`2&$`#O(nt=top`1:&el<`1=(nt`%@&`#r$sel>=top+a_MV`#C+`&g$+1
 `(-$nt`4T&`&r4`&s?`K|-`Jd+`p6&sel`9>(ick_col`bF(sel`Hx(`X#+sel`+j$`*R.Arrows`*K% a colour`*T*use`*U$CLEAR: back'`)ZLLEFT`)]>`)3$`)^<`*F24`*FA`#E0`)v&`L:&ol`MW%col`$y&`&@,old`7k$`*H.==CLR`7..`)l$`Kh*`#h.`(*&`#:-`(A,`#8,`#4/.co`(g.`_m)ick_`>*$`Tk*)
 c`Pu$80,'PLAYBACK SPEED',GOLD`#D)140`)=& done`]6)`S1*`)<.t='<`^Q)`]o%`HV& a second >'`={.sp`^L$-`fb%*5,110,t`YR%`2U)`*=,`*3*`<I1`<H+`*9-`=T2`=S+`/8*OK,CLR`-l%`Et&`&_,lot(titl`^~$opts`uY$for sl`d^+,S_SLOTS+`g($ inf=S_info(s`)E$opts`OQ('Slot`&J(l)+(':`@q(nf[0]`&Y%'if inf`Z0&: empty'))`$P%`#q)Cancel')
 c=choose`${%,opt`O|&c<0 or c==`$q&`T,* 0`/y)c+1`%l(rogress(k,`9H$`7B$60,1`f%$0,30`(d)rbox`#>,16,6`_[)`#[%4,124,max(2,192*(k+1)//n),8`+,&`K9&o_sav`Y,)`FY+sl=`(M,'SAVE TO`F($`X3&l`VM,`,J-100`>p$ing...`,F)data`E|+`7^&f in s.F:
 `#E$`($(len(f)//256)`#>5%`#=,extend(f)
 tr`Yq$S`%L&l,data`oj$s.F),`+E$,`(1*`:P%slot=sl`Yr-`F5(`Rc)`F}-`-v*sav`Ad$to `bX$`*u*'.']`c-&')
 except E`#*$ion as `.z$`Sl*Could`&z%ave:'`j#$e)[:24]],'Error'`)$+loa`0j&`(s0LOAD FROM`(u- or`#-$`-+*`),,`Zm%`%r%`.v$`$e*Un`%X$ `#A%s will','be lost. `6w&l`DG%`6v&c`-+%]`Da%?')!`5(&`*D:Load`*E/`)7&`)-$`(2%,fps=S`%p&l`)3.`(#Mload`(#9`$s*F`0z$p`NY$`v[.`$Z%`&^$n=data[p]*256+`#/%+1]
  F`+o(bytes(`#>&2:p+2+n]`}^$p+=2+`X[$reset(s,F,`MR%`+P*`)[%`#C.:`Wy$=F
`3U%=fp`Jl%`PS$`Jt.0`R_)`RF2`SD0`,^.`]%,`$Z(0`f7(tudio`L6$s=a_S`#2&`%;,[`UD*`$D.)],6`Sn%x=16`#,$y=12`#,$ol=`U,$pen`%<%`m*$`ay)`iy0[255]*`j#;msel=0
`li*
 held=0
 hc=0`>P2`85.hel`,o%`f)$ hc`7[(`b-%`#i& rep=k!`#Q%or(hc>3`#Y$hc%1==`v_$`$@$`<q&not`#v&`PP%0.0`eS$`fg,`Dc2,`QI(and re`C^%`V|/`:;3c`g8(`#/$`Ra&`:;4c`gB.`#5$`Sq&`@^*`#O(y`#z+y`#z/`T,+cy<`o&$`#y+y`#y&`uw(`#<%`]|$`k?.`?k%`m0*`}.%`#Z(==1`:-%`&x$ `t=$int`#M$a_wa`#.%`-i$`n.-`($1not`&h)`(?/==OK or`%E$EL`#E$want_pen=1`#E*`$Q$2`=j%`+n$`$q+`#S(`#H%`#1(`%su`uE%hown`mH$`%v+`$+%`*72`&01`Hs-`Xn1`&41CLR`)L&`%7(`.b)`#q1`#b1`L*%`&w&`Es(`#e+c=`QS)m`Ec(if c>`^w&`/)%c`#Y%`iy%`:5(`#K$`_D(`Jz0`+])c`fu& `rX*`#?,2`%L&undo`eE0  u=`#=%`,/&`g]8`g_(u`#/&`gS-`$5)3`,x(`#l@`b[1`#y:4`*e&`:V$`hB,`)u)`py$`#@%`#p%`1t)`cZ$`o%+`&r$`&5-5`/.(i`/V(`#u+`sg%`#O)6`#D(`#x>7`#J4Tru`#I.8`#I(`l4,`#D,9`)[)`gt%`)U-`)z.`KI(`&b&`pL-`#W*`1V)`6k%`yp%`#/$`#J-`dn&`D_,`#}>`)[&`@4,`#T>`)8-`:$%`(o&`#V0`{f*`@:(or`@9Rn`bV$`@81New?')`Q<)`i[%`:oF`%>+5`%>)`$udquit`$v4Quit`$w.`@>(`&L3`&q$`#6$`/f)`;S(`%((!`*l*`gY,RULES='Draw a picture, add`F{&,`-/$play them`Vs$. Saves stay on the calculator.'
a_KEYS=[`Wv)move `%f(pen','DEL: eraser`_N&menu','Menu:`XF$rs,`$P)play,','`,S$,`Gb$`$f$`Eg$]`c6(ain`@<$`>0.c=home('GHANIM','ANIMATION STUDIO',`%}&,`%+%,(`iR(B`YU$`>m&c<`.-%`(I)`AW*
`$G('''
GAMESRC['GHBLOCKS']=r'''import random
b_CW=10
b_CH=2`#+$=9
b_OUT=(50,20,70)
b_WELL=(35,30,9`#5$DOT=(60,55,125)
b_PANEL=(70,35,10`#I$X0=115
b_Y0=22
b_SHAPES=(((0,1),(1`#)$2`#)$3,1)),((0,0`#=$0),`#I+),(`#71`#^%`#W*`#=42`#=9`#s%`#C0`$L0`#W+)
b_COLS=((90,200,22`#h$3`#1%6`#S$70,90,210),(70,11`#J,140,50),(80,19`&g$,(2`(&$,70))
def b_cells(p):
 s,r,x,y=p
 out=[]
 for cx,cy in `&n([s]:
  rx,ry=(`#B$)
  if s!=1:
  `#[$i in range(r)`#9$`#V(2-ry,rx)
  out.append((x+rx,y+ry))
 return out`$u,_i`$w1if r%2==0`$_$`#Y$[(x+i,y+1)`$R/4)]`$#([(x+2,y+i`#G4`$<%get`$8%`$V&`$N,if p[0]==0 else`&c+`#b&ok(b,`#c$for x,`&Z&`#y) if x<0 or x>=b_CW or y`#.$H`&F$`$@&False`#S%y>=0 and b[y][x`(E$`#J/`#1&True`$S&sq(x,y,c):`&D$y<`&A+
 px=b_X0+x*b_C
 py=b_Y0+y`#2%if c==`.>%`#Y%ct(px,py,b_C`#&&WELL)`#@*+4,py+4,2,2,`.h$)
`&;$`#e7dk(c,0.55)`#i+`#D&-1`#)&c`#?52,lt`#b$4`#b12`#F&`#D5+3,py+3`$n$`#D&7))
class b_Well:
 def __init__(self`(w$self.s=[[-1]*`(w$`*L/b_CH)]`#M(las`-K%def put`#n$,x,y,v`)m(0<=y`);$`$$%`)@%!=v`)C$`#7,=v
  `)7*`/s%[v-1]if v`+;(`(M&def show`$;%b,p,full=`*3$`$D$new=[c`/1%`+O,if c[1]>=0]if p`#|$[]`$w%fu`&2$  `,G$=[(x,y`-A$`,8$`%s+`,N$`#7-W`&,$`)p(`#f&`&;)+new`&K-`#3%v=p[0]+1 `$T) 0
  want=[(v`+S$ in new`%r&[c[1]][c[0]],c`$R$`#E$`$:$]`#a&.sort()
`1E%w,`#E$want`(2*put(c[0],c[1],w`/$(side(score,lines,nxt,old`-_&old is Non`%W$`&2$,h in((26,64),(96,4`4O$42,40)`2^%rbox(226,y,88,h,6,(15`4e%190)`,)$`7~$)
  text(234,44,'NEXT',(200,185,230`,D$`#G)114,'SCORE`#I=60,'LINES`#I3old=(None,`#())`%a$nxt!=old[2`5I%ect(2`6V$,40,2`%%-`2I1(nxt,0,0,`%w(c=`,,&nxt]`1x%`#u$4+x*9,54+y*9,9,9`0(/`#J58,8`0*%`#A(5`#A%5`#A$`/G/`7@$core`%>%0`%>$`)3%[0]is not`)9)`&L+31,str(`#J%)`(c5`#G(`$)$`$5&`*E$`$5%1`$5,1`$5;77`$5)1`$58`#G&`$)$`8q*`+c0`,#(game():
 b=[[0`1j>cls(`?k$)`7T%`#F+`<H$,30`))$`(+$0,i,320,15,(58,25,8`*T$`,>$b_X0-4,b_Y`#*%CW*b_C+8,b_CH`#.&4,WHITE`,O$`1l&well=`4+%(`#2&.`1|$b`+G%True`$-(4,26,96,56,6,GOLD`-?-`&G$14,48,'STACK'`#G$`#=+68,'DROP`#<)`%e$,c`/v$enumerat`&4$OLS[:5]`%n*12+i*1`$H$12,12`+_$`7f0`#H,1,11,cc`%,*150,`/s$`/R=`$w%2,167,'2nd key:`.d2`#J)84,'drop it`#I2`*-$=0
`+L%=0
 nxt=`Ea%.randint(0,6)
 p=None
 t=0
 held`#+$c=0
 sd=`2d7`0%&while`<c$`,N&p`2p, p=[`/b%3,-1`/N$`$P9 `$7;sd`#D$if`-K$`?D,   message(['Score '+`.D*,'Lines`#7&`-F%],'Stacked to the top'`$+$`>W) `+A-p)
  k=key`6>$if k==CLR`?i+
  speed=max(2,14-`$7$//5)
  q=list(`#m$`#c%held`;A$k`#j$hc+=1`8y,`(>%`#P$!`#P%or k==DOWN or(k in(LEFT,RIGHT)and hc>4 and(hc`D;$`3o&`$;%LEFT`&H%q[2]-`$8$ el`#@%`#i$`#A*`$V%`#A)UP`#>(1]=(q[1]+1)%4`#7$`(R.q`(R&`$.,`#G9`$5&2`$5,DOWN`#B%t=`&j$`#@,SECOND`#B%`+,%`#x&[q[0],q[1],q[2],q[3]+1`.m%`$2$3`%D(`#|+`,D$k
  t`#?%fall=t>`#C)if q!=p`EA%`%,-p=q`*/5if`#j$`4y%`)$$ q=[p[0],p[1],p[2],p`$h%`(X&`&,/`$#&`$$2`*%*`Gp8`#u%y>`Iw%   `GD(`?+&`#a%ull=[y`=3%`5K/if 0`(i$in`#_$`$o$`A+-`=m& in`#7, del`#T$`$A(.insert(0,`6d(`-_%`1(%+=len(full`#9&`.R$+=(0,100,300,500,800)[`#M)`$%&`5[8`#l$`04@`2,) pause(0.02)
b_RULES="Shapes`)&$ from`/k(. Fit them together to fill whole rows, which then clear. Don't le`#c$ stack rea`#I%`$$$"
b_KEYS=['Left/Right: move','Up: turn','Down: `5%$faster'`5[$`#6&all`#x$way','CLEAR: quit'`N|(main`;:$`4B.c=home('GHBLOCKS'`8n& `8X%`&4&,`$q%,('Pl`$,$Back'`8)$if c`MY%`2L*`<O(
`$A('''
GAMESRC['GHBREAK']=r'''import random
c_ROWS=5
c_COLS=10
c_BW=3`#+$H`#3&Y=34
c_RC=((220,60,60),(235,140,5`#0%0,21`#=&70,190,90),(170,9`#?$))
c_PW=46
c_BG=(30,70,170)
def c_brick(r,c,on):
 if on:
  block(10+c*c_BW+1,c_BY+r*c_BH`#1%W-2,c_BH`#*$RC[r],2)
 else:
  rect`#fKBG`$_(walls():
`#h%0,24,4,186,(20`%g%230))`#C&316`#E@,24,1`#C%120,130,16`#g1`#E5c_PC=`(+$1`(H$`#5$L=(255,200,15`&f)paddle(x`%+)x+1,192,c_PW-2,1,c_PC`$?(x,193,4,`#B$`#9*+4`#;$`#V$8`#@%L`#@*`#:$`#E%`#^1,195`#[$,4`#x/1,199`$P1for cx,cy in(`#d$2),`$.(`%*$),`#:$9`#:.9))`)E)`#e$,1`#z$`)&*puck(x,y`%|*-3,y-3,6,6,WHITE`$h)-2,y-2,2,2`(|&20,255`(8$HUD=[None,None]`$&&hud(score,lives):
 a='Score '+str`#A%)
 b='Balls`#:&`#R%`,>$a!=`$)$[0]:
  if `#2, text(6,17,`#:(`%P&`#>,a`#p%b`#p(1`#p.`#2%`#S%214`#r*1`#r/`#@&b,GOLD)
`$T)`#R)=(a,b`&u(game`,x$cls(`#m&`-((2,320,2`&|)`-L)
 b=[[1]*`0n%`)b$r in range(`12%)]`){%`#<2:
 `*:%`#=,COL`#=%`0<-1)
 left=`#_%`$;&
 `(R$=0
 `(D$=3
 px=137`%b*`&_)=None
`)O3
 while`#h%>0 and`$6$>0`1N$x,by=(p`+^%/2,180.0)
  vx=`3k%.choice((-3.0,3.`/Q$ vy=-3.0
 `.m*px)
  pause(0.5)
  st=Steer((LEFT,RIGHT`#d$`$_%Tru`29$ k=key()
 `)s$k==CLR`#<$ return
   opx=px
   d=st.feed(k`#V(d==LEFT`#W%px=max(4,px-7`#E$ if px==4`#D% st.stop`$<%el`#f%`$j$`#g*in(316-`/m$px+`#n.`#=(`#u4obx,oby=(`&w$`#6$bx+=v`%-$by+=vy`%&&bx<7 or bx>312`#q%vx=-`#N% b`%9%7,`$V%2,bx`&U$`#_$y<26`#U&y=-`#x% by=26`#E&vy`)T&188<by<198 and(px-3<bx<`)Z&+3`+D%`#l$abs(v`%#% vx=(bx-`*)*))/5`%w(`#L$x)<1`%t&vx=1`$?$x>=0`7T$-1
   r=int((by-c_BY)//c_BH`$*$c`#=&x-10`#;%W`%M(0<=r<`,h%`%2$0<=c<`..&and b[r][c`/|%`#0(=0`#1$`-X,`+}$`&7-`,u$+=`.K&-r)*1`#Z%left-=`$~$`-E5`$d%`.L$=`-:$   break
   vacate(int(obx)-3,`#.%y`#.(`#8*`#7%6,6`1m)`;a$by<`:e$`/O)BH+`+a&`0S$`0T+max(0`#q$(oby-3`&r-)`*7$`#k%`#G)+`#G.+1`6l%`$%&c`1=+`$%-x-3`(Y+`$#(COL`$#)x+`#E,`#}+`+T$[rr][cc]and`*;$r`=5&`%Z&BH/2-by)+abs(c`=a(0+c_BW/2-bx)`1?%`##$`)<)r,c`2u%`&P%px!=px`+u&`(E%op`9k$,`#*&`.i$8`(-.`#Y% or oby>18`-I&`1h/`9i(`)&&`)$(`.)*>21`$n&`*3$`*L?`*;(`6W$`)}@`#H$4`%2$312`%1*`+8.message([`:D3],'All `&O$s cleared!'`Ax+`#c?Game over')
c_RULES='Bounce the ball off your `&R% to`%Y% every`$H%. You have 3`#Y$s.'
c_KEYS=['Left/Right:`#j(glides that way','ENTER: stop`$F$`#L%','CLEAR: quit'`=[(main`:j$`6D.c=home('GHBREAK','`#+$OUT',`%Q&,`$b%,('Pl`$B$Back'`)X$if c<`)T%`6t)`;|(
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
d_COLS=40
d_CWID=d_VW//`#:%
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
  off=abs(i-`:4%/2)/(`#.%*0.32)`($%off<`&l%base+=(1-off)*`$>$,1-d/12)*(1.1 if not`$j(`&T&.35)`&y)min`1n$base`%o(wall_detail(g,t,u,top,h,x`(&%def band(v0,v1,c):
  y0`+v$top+h*(1-v1))
  y1`#:/0`#:$if y1-y0>=2`*(&ct(x,`%3%y0),`=7%`(c$d_VH,y1)-`#A,`)a*`,:& in 'lkjCF'`+A&u<0.12 or u>0.88`&J&nd`4K$8,(70,48,3`$]%`#<%.8,1,`><%`$s&0.7<u<0.85`#e+.42,0.47,(21`7z$,9`%I)`$T%kC`-p$0.12`#d$3`#c$on=t=='`#?%g.closet or`.*(`$*)`3:$,(4`:O%`$%%`#?)3,0.57`#A$20`3,$if on`)D$`5p$`#W%`+J*`#=%3`<%%`$u*=='F`/d(ocked `$+%15`%#$25`)?$`$A(6,0.64,`-3$3`$a(`,W$t=='S`(5$`/u$ in range(6`#f+n*0.14,`#*%+0.07`6#$7`<~%`(+(`&E%`(l,`61%3`>V&`8c$`&&/`&D$`#C1`$f)B`$f44`$f/25+0.02`$k$`#/%5`*-%5,2`$k% cc=(`$.$`8P%,(50,`9t&`7v%3`(J$,(17`7b%60))[(int(u*7)+n)%4]`$?35`$?*2,cc`%,,T`,%(0.1`&1$9`&1,`:T%,(15,15,2`)W$`/=%tv`)X%6`$n%6`&).G`#{*28`#|$7`..%`,y*`%p)`*;&`)l,75,(220,`,U&`#C%`#s$4`*E%5`-,%`)%)`?.3`#C$`${)not`2^$`)Z0,(240,`#&$`$R%`%4)P`%4*3`$>$6`&1-8,0.56,(13`(V%13`)*&`$s%`$r%`$q-44`3y%`2n-4`#m$`#=458`.E-`7B&olour(t`5k&`100`7W)DOOR`9k)`-:%`7B&12`(r$60`:0*`+t%`#C&`#?$,`4Q,`1I%`:((ender(g,full=`0J$`$V&full or`(/$hasattr(g,'cols')or g.cover!=COVER[0]:
 `#8(`#7)`#6&ls=[None]*`M>&  g.spr=[`$<$`#:*shown=`#V%
 spr=`#K$
 zb=[0`#K*ca=math.cos(g.a)
 s`#5&sin`#5&for i`.j*`#_%`.o$cam=(i+0.5)`Nx&*2-1
  rx=ca-sa*cam*`O0$*0.5*1.15
  ry=sa+c`#A7mx`7>$g.x)
  my`#1&y)
  ddx`9}$1/rx)if rx`)~%10`##(.0`#J$y`#J(y`#J$y`#J5`#f$<0`+A$sx=`%+$ sdx=(g.x-mx)*ddx
 `;b) sx=`#G*mx+1-g.`#I)`$2$`#s(y`#s)y=(g.y-my)*ddy`#s-y`#s(y=(my`#s$`#I)side=0
  t='#'`3130`32%if sdx<sdy`-V%sdx+=`$[%  mx+=s`#.%`#u)`$J* sdy+=`$9%  my+=s`#.%`#O$`$g$`C&)mx,m`(A$`,y$`BY$`36$ot(`C92)`$g% break
  d=sdx-ddx`$z$ide==0`(P%sdy-`$K%d`?x$d,0.05)
  zb[i]=d`&r%`#W&`#{$u=g.y+d*r`&f-u=g.x+d*rx
  u-`*A$u)
  h`#.$d_VH*1.35/d)
  top=`#7$-h)//2
  x=i*`=k%
  k=`B8.*(0.8`$R(`*W&.0)
  key=(`?b%t`C%$u*32)`#-$k*64`92(key==`.<$[i]`&P& spr[i]`&C%continue
 `.e%[i]=key`;P&op>`%o%m=top//2`#9(=4`E<(`@.*0`@%(top-m`?p)`XR%`@L$k,0.3)`4(%`#X&`#O(`@a%`#X:*0.8`#]%fy=`Ah$`#j%st=`&i$f`*N$if m`Am(`$,(fy`$)4`ZG$`$*)25)*0.7`5l&`#l&`6?%  ly=fy+m+m`(r%`$#,+`%,)ly-fy`%i-`$,1`$&&`#c(l`$d)1`$d?8`$d(`#_*+1`#b(`%q$ly-`#j=`#e&`.**`%44rest`%3D`#k*`&|1rest`#fA`FG-top`FH2`)F$`FK(`#E&`#y(`9F)`FV%`HW?
 used=d_sprites(g,zb,ca,s`6A>`-$%=`#@$used`M[(`#k2:`$-&{}
 lst=[]`#}%sx,sy,kind`Oc%`TY&:
  lst.append((`#J*`Ht&g.ys_vis`#L0g.yx,g.yy,'ys'))
 order`$:7ls`N8$dx=sx-g.x
  dy=sy-g.y
  fwd=dx*ca+dy*sa`/>%fwd<0.`-?%`/i,ide=-dx*s`#Q$ca
 `$E%`$g)fwd,side`%8)`#B%sort(reverse=True`(1&`#R- in`#R%`:S$x=side/fwd/(`9w.)
  scol=(cx+1)/2`<S*w=0.45`23$ind=='ys'`1;$`(4$[kind]`=;%half=w/2`$+5`#v&`/4$h`0L$`4K%fwd`4L02
  c`O*%scol-half)
  c`O&%scol+`#7$+1`4j$1.0`$k5`5$)`#X&),fw`5c$`+M/`,f%c0`T/%`$t%,c1`7x&if`7<%<fwd`.A%`)#+`+Q$[i]`9,%u`>N&-`%)+)/(2*`#-$if`&:$>`8R&0.5`$)&u<0`P(%`SL%`$*-`7H-`%W.`#P%d_ys_column(x,`$C+`#Z&,`$H%`#1(`.g$`1M%`$1,for u0,u1,`SK&`-X)`)G&1`Bu$`${%0<=u<=u`$z&`Ss8 `Sv9`#l%`Sy(`Z2(d_VH`#w&`T-a`Es&`0P+bottom(g,promp`GE(`#0%==g.`9t$`Fg*
 `#6&=`#F%
`$[%0`5H$,3`K<%-`#0$BLACK)
 text(4`#D$+15,`^5),GREY`0t(`YJ)`#Q$25`#v%+15,'LIGHT',GOLD`#s/33`%&&[:31],WHITE)
d_YS=[]`%Q&_poly_slabs(pts`/K$,step,top`/o$,`%v%`/{%:
 ys=[p[1]for p in pts]
 y=min(ys)
 n=len(pts)
 first`#3$d_YS)
 while y<max(ys`Yd%c=y+step`?8%s`3&$`-o0n`-V%`b1$=pts[i`Q<$x2,y2`#3$(i+1)%n`#9$`*2$<=yc<y`Y($y2`#0%`+-&xs`2j(x1+(yc-y1)*(x2-x1)/(y2-y`+=%if len(xs)`=.(d_YS`3K)mi`#?$/256`+$$`#/(1-(`%A%)/640,1-y`#+$`3s( y+=step`7q&,on in((`&B$`9+%(`&H)-1`(>&`0J%`Xj%and i`g:&Y`8F%`.,-k=d_YS`&9&`#.&=(`#E,5`OU(_limb`)a$w`$l$=`G<$`(:/0,`)6(-2,2`$:$`(F$,`(<%(`(M%,`#*$+1`#,(2`#,(3])
  n`Ez$1`3?$abs`($&/`AJ%for k`)R1t0=k/n`#-$1=(k+1)`#1%xm=x1+`(q&*(t0+t1`56% ya=y1+`$&&*t`Cd$yb`#7-`3]$hw=w*0.4+abs`)a(n/3`)I1(xm-hw`)=%(xm+`#/(1`0;$ya,yb`)K$-0.004,1-`,b$`#:)+`#:%`)b&`(2&oval(cx,cy,rx,r`;@%`-x%a=0.`(A$`P],0.55`P^/`#6&pt`-.%`(q/1`^;%t=2*`#U$pi*i/16
  lx=cx+rx`#;%cos(t)`#/*a)-ry`#2%sin`#>)sin(a)
`Du$cy`#c5`#F%+`#c4`#~%
  pt`-z)(140+lx*ca-ly*sa,5`#2$sa+ly*ca))
`18<`&c)build_ys`ln$`&JF`,M([128`so%32,88`^u%6],11`$F1[(98,122`rh$8,11`#-$`tS$6)`b.%21`_d$46,26`#-$10`#-(06`#A$],0,8,`3;$`Ws%
 hem=[(108,2`aT$14`#-)62,330)]
 x=162`2|(x>9`rC$hem`&d)x-4.5,330+(1`Mu$`rK%%2`;O%6`F+%x-=9`$<$`#[)94`$-$`%a1hem,0,6`$r%`$}$`&N-18`7M$112,4`wK&470,108,612,98,628],9`#X-40`#X%46,462,136,474`_y$610,162,630`#Y000,128,84,250,92,262,76,420],7`#N-58`#N$176,248,166`#P$184,41`#Q&for `t2%sg`3]$`#p%,-1),(`#M&,`?|&`Ck$`-R*`iQ&`$:)`t{&0+sg*(f*4-6),y0+52+f%2*8`#=*5-4`#=$70+f*3],2.6)
 hair=[(-18,-6),(-27,30`#,$4,9`#5$6`gE%8,100),(2`a$$,(17`#U%10,-24),(-`#-&]`+k2`-g?for lx,ly in`$]$],0,4`&p%`1?$0,0,17,25`#;&for ex,ey`&U$137.2,41.`,j$49.1,48.55`&X%`3/.ex-2`3.&ex+`#.&1-(ey+2`8Q((ey-`#0&4`2q)`BT,left,wid`B<&`?G%not`$6$`$>%`/b+
 x1=x+`C[(rim`6a+wid*0.01`Q;$eye`30*p in(0,1`)m)`9,-`Lo)`$;% pa`BY$left+u0*wi`Fu$ pb`#:+1`#:$`Gh$`E-*`.p$`#3$p`Y{( `$S$`&L)pa,pb`$B%`CT&`Dx,`#]%`=>&`#{)`hu&`#M- pa+=rim`#/%b-`#/(a`&&$x,p`4-$ b`?~$x1,pb`]~(b-a`xx&`#v-y0`z:%`&c$`Ed-`#]$y1`#o$`C<$`El1+1`$&(`Em$`$)4`&+-g=random.randint(190,2`4Z$   c=(g,g*19//20,g*9//1`],$`T|+`#g128,6`{M$`#e(,g+8`ZS*a,y0,b-a,`$m$,c`99/`(U+ in`(s$`OM$`fu%`%^)(v0+v1)/2`AR(2<=cy<`Zn%`)d%`8;,(pa+pb)//2,cy)`Pd(`J5$((0.03,(35,`or%)),(0.016,(80,175,245`#8&06,(230`2u$255)`.4%r`,T%`Rn$>0.01`M$&`,g)f`?A)`<_$`E}&`$r$e`*4(cx-r`&u%`*7)cx+r`)7*eb-e`*=5for dx`37*ea-cx,eb-cx`eN&h`d#%(r*r-dx*dx)**0.`)K&`(U$cx+d`Kh(cy-hh),1,2*hh+1,c`/~(wrap(s,n=3`>Y$ou`WY*para in s.split('\n'`$G$line='`h}(w`%n$ara`#J( `#I%`FW(line)+len(w)+1>`L0$  ou`Wt)`#D$`#8$`#~$w`+@.`#7$`#G$+' '+w).strip()
`#j4`Mm&out`%Q&page(title,body,color=`Ki%:
`$($s=`%z&body)
 per=9`1y*`Ey-`#S$),per`oz%l`2|$ c`MA%0,`$4%`M6& y=44`&>&l`l>$`#d$[p:p+per`Q_%`#^$10,y,ln`$j%`/d%+=17
  more=`#R$`HX$`$J%`NY(10,204,'ENTER:`#O$'if`#+$`+e%`#=%/CLEAR: close'`OP(`>6&Tru`()%k=wkey`%@$`2d$ in(OK,CLR`lQ/if k==CLR`#:$`Q>&`(-%toast(g,`$s%:
 `t|(+=1
 rbox(1`}_$300,30+18*`&p+8`PB( y=72`(A%`&P+`(0$`%k$y,ln`LL&18`@M(`%/%not`%*/pass`S+*None`bC(ay(g,`$s$`%+*`,o)27`9%)keypad`*S&hint,`JV$abc='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
`*,(`*+6y=4`%U-`$D&`$*$`.6%`*).`(x(`*&&typed`./$sel=0`%y(`)5(`/R$60,96,200,26`UR) s`.g*`RM2s+=(`$$$[i]if`Oa&`#4$)`*a%_')+' '`(K)116,s`.=(`)&)`$(02`JH% x=4+i%13*24`,A$y=140+i//13*28
`6A$GOLD`E<$==sel`,#%`#}$`6Q)x,yy,22,24`%G*`*m%`#=+5`6k$`&^&x+6,yy+18,abc[i]`#?%`,N+`,0%LEFT`%z%el=(sel-1)%26`t#$`#E%RIGH`#F.+`#F. in(UP,DOWN`&l&`#K)3`#q/DEL`/S%`)1$`(5%:-1]`#F+`-j. `+t$`#A*OK`#e*+=abc[sel`W1(`(z*==`3c&`#k&`#9$`,7&objective(g`A++g.pow`gM%t='It is pitch dark. Find the `#J$ sw`#?$by`#7$front door.'
`$x%`#y%not`+P$t='The`#E$ locked behind you. Look arou`$.&foye`#p0`1k$`k8$t="Decode Ivy's note. The coat`29%t `.n% wants four letters."`#}-`zg%`$q&Unlock`$N$L`#;$ Room`$T/taphear`g3$`%J&TV in`#Z0`&=&ed itself on`&73book`%G.the knocks.`%S+book might expla`$:%m`%?%`8l%t='`#h3The hallway`&-/ive`&-)'`c-&awak`#r%+='\nShe is `#9$. Stay quiet. Hide whe`%j%`k-$s stutt`(|%`+.(`3i(hort`+%8`#O&'`*t5`$f%`*^.`#T(`*F5`#T,`*C*`#V&`*H2 (DEL)"`#X+`){*`$2(`*$6`$3,`)},`#Y(`*&&`)o2`%D0`)l(`$p(`%{$`)c."`&l)'H`)3-: 5`)+('`(+&journal`(-%body=`/F.`)Q&`&g(body+="\n\n`$>*: "+d_CIPHER+'\nMy nam`)u$`*l$ey`*@)`%n,`#q%'\n\nK`+4$: 4-1 4-5 2-4 1-5 4-4'
`?j('JOURNAL'`?n$`$f,`&,(d_gri`#Q&)`:S5`#C+:`9X2"IVY'S NOTEBOOK"`k$-10,44,'For talking through walls.`>U)`#R(61,'`%K(row, then `PT%`#Q*for r`U10`8n&0,92+r*20,str(r+1)`AL)`GT$`Uj1if r`L%)`#j%40+c*24,76`#j$c`#j,`#F/`$7(d_TAPGRID[r][c]`%D+`Aa$I`h^$J share a box.  `A[$`%G)`?6C`(Q%facing`+4%`_i,g.a`_h/`#5%for `>+$`d+&,9`U7%=n*0.2`1z$d_tile(g.x+ca*d,g.y+sa*`Rp$if t!='.'and(not(t=='l'and`.x)`wd&`13) best`*R% bd=1.5`}i4`uI$ITE`UQ%`}o7dist`%B&qrt(`K.$+dy*`,*$ if`#D$<bd and(`~=+)/max(dist,0.01)>0.8`$q$`$g$kind`#0$d=dis`s~$`%,$bes`3?(label(g,`tr(t=='P`xS$`/|(`Fy&`3:2t=='F`#N4`:G*`#L*G`#L4grandfather clock`#S*C`#S4hide in`9v&'`/7$`:&&`HW+`HQ&`:;(`#y*l`#y4`9B,`%#.k`$M5`3#-`#P*j`#P4dining r`$%2S`&&9 staircase`#Q*T`#Q4smart TV`#J*B`#J4bookshelf`#K*table`#O,"`#O&`5j1if `.K$'phone','desk','lamp','couch','rack','vase`QC%`$N/look`:K*'`6D(use`+.5`)>$`:U)`#Z(`Ji('P`#=$`=}$)
 `#N(`y{$`2D&`/W+`G9&g.blackout=n%2==`rc$d_render`7V$`#F,`ih$`5s$`$=&CLUNK. Years of dust rattl`+D$the wiring`$^(`BU%`$_(`$3.`Ls*['ASHGROVE SMART HOME:','Welcome home.','F`-T) LOCKED.','You did`;&$set that up.'])`A/&`.K*`%;("`$2+`#p(`@D&ndle doesn't move."`(H$`Dp&`-e%`E+)i`?j$ck. Swolle`(2$its frame`%z$`$M)`/L%`?t2`)@1Too`F}$ to make it`Vp$ G`%P$`A0)on`~v%`(-(note`(+*`:C$`:/+",'Folded paper, tu`G5,`A9$endulum glass.\n\nDad never notices anything. Grandma taught me this on`C)&I was six. `=g3\n\n'`>1-\n- I.V.Y`%B(arm`*K)`&a)`2X%`2:+`&].hid`?X%`()E`$V%pad is dead`$E%a=`T+)'COAT CLOSET KEYPAD','A brass`#b&. F`I[,'`m/$ if a=='ECHO`%#$`$})`(e(`?A.`.31`$s.`4b&clicks open. On a hook: a`$[* tagged LIVING ROOM. You t`*Y%`%T%`&j$a`$d$`&&4buzzes. Wrong cod`,(/`6%%`Fo3`&~1L`-;$. `&K+hole, polished from us`$,%`<2)`0-8`$x+`%f+urns. Stiff`AV&all at onc`#~)tv`#z*`#l&Somewher`1a)`88+, a`Gn+s`M^,`%~,`7~%`#w*`/Y&shut`/_;`8*%`#Y)Boarded, chaine`=T$ pad`0p%`1;%`#2& is engraved M.A`#}.`8-%`2.)Book`/|$radios,`)1$s`$($moths. Mildred's, mostly."`#u,`9K%`-NGTV`-J$ark`(2%d_tv`(y$`#t)`9K*`H:*`(T*`H>-`1d3`Gp%"She can hear vo`15&d scree`)p$he's bad at`R$* think it's too slow`8X$her`1-$- Ivy`%q-`:p%`(k-An old rotary `#D$. Silent. For now`(R.`;R$`(U-`(3) desk. Pag`%4&p`#-$of dot`#5%dashes`(T.`<D$`$b4`,o%fl`X,$amp`$S.`<v%`#[-`0R$ushions still hol`5I%shape of someon`+w/`=b$`%G-Coa`6y%hooks. On`Tf% child's raincoat`%>.`>I$`$a-Dried flower`V7%y crumbl`6;&you`i)$th`$a/`$]%`54R`]C$No`F0%`5>2`<m/LOCK`5?$sticky`Tp%in Ivy\'s writing: "t`,q%knows. listen."',`q{$`5Z&QUIE`-i% g.won`,k(`44V`QR3`.,$`QL&(10,14,30)`QV*4,`%Q0TV'`QY18,'HDMI 3:`rq%ho`;:$comes next`Q^26`$}$n `Aa$`)-$n`.6%`A0$`#R(y=100
 x=20`Qm&`x&$ d_KNOCK`Lm$for grp in(r,c`C(%`C>/grp`o,&circ(x,y,4`i)*  x+=11`#-$pause(0.2`vB%x+=10
`#+%4`(V%x>27`RI%`$b%`k^$24`%L*170,'4-1 `VO$`VP$`VQ$`VR$,(160,21`yY&`RB/Writt`A6%your `Xr&.`RE/`Wu*`)x&`okD`,S)`_u)`#.&`*c(g.ytimer=6`3K*'...'`*j&`(]& stops.\nEvery`3C&`8P(house flickers`99)\n`b)0`ax>,(200,14`#&$`q=)`@$&:
 g.hidde`,l(`YA-70`FH%squeeze into`$/$coat'`)])`#P%90,'`<l%. B`0+%`54$ly.`#N0150`vd)step ou`,2+0`q82k=`mx.`k{&`v?(`*y)`wp$0`uu$`Bq%ystate=='hunt`Uz$t0>25`/V&`#A&'dormant'`#9(_vis`K*)`)3*random.randint(35,5`,6%`pX$0,110,320,30`pZ+`%e&30,"The static fade`8q)gone."`+F*`(P&`$K&`vi4ight`Yf)g.`#3$`En)g.yx,g.yy=(9.5,1.0`Yg3`ui%`N1,<3`86$`N9)`%|)n>=3`#3%y=1.0+max(0,n-3)*0.08`AI1`(M,`&h0`O%2`#a-`3o)...it`Hx$a woman. Mad`8T%`&Z$. And she`#H$loo`-R$at`oa$'`,B(ys_update(g,d`Qz(`.f+ or`5G%`Rm*`df&`*F)`*)(`&G%`)r%-=dt`*q)`#5$<`b3&`*c*warn`*_(`*L%`wF$`Bv*`)q%hisses`:y$`C}-`/N$`BD%`.}0`9_(`$q+`$7$`$n3`(.+`+s+om()<0.35`%58`Sh1 spots=((2`*_$5),`*j&5),`#7$6.4),(11`#8)6`#8$`4*$  far=[p`+8$p in`#s%`9p$bs(p[0]-g.x)+`#1%1]-g.y)>5]or`:H$(`#R$`#n$`,6*`%@&choice(far`#C(`(>&`/@$`.{-`LH*`(O&28`&c2`#Z$`&c3dx=g.x-g.y`c9&g.`c:$`c;$`c8:sp=0.55*`*<(d>0.01`($$nx=g.yx+dx/d*sp`#6$`#|$y+dy`#6)`+e&d_solid(g,n`%s%)or `fB&`#5(in `Lk&`&@%=nx`#g5`&]$ny`:B&`&g$ny`*9.d`/]&`*A22`*A&d<0.6`>M&c`Se$`/L%`&j(`,r7`3U@`+-2`3k?`/7%`$L):`2.18`%Y$for y`#8*0,176,22`]X&v`$&060,230`4p,y`4n$22,(gv,`#%$`@@$`8],90,'S`u~$u`|c&',(220,1`#&%`@s*13`8.(`lvL g.`)P$,g.a=`-o%5.5,`+0$pi`3X&`(%0`3nB`&{)30`6M5ending`r_240,'enCRYPTed`<1&60,6`%Y+70`DM-fl`JO$ gree`QY%`&Q*End of`2?$demo`#A+125,'Full game at`D6)`#C&47,d_LINK1`<106`#=(2`#=/203,'CLEAR: leave`(G5!=CLR`(>)`&%%`7f$_menu`F=&=choose('PAUSED',['Resume','J`B(%','Quit`%J$`bv$`YE.if c==`/g$`yO,`gJ)c==2`$H(lay`(I$g=d_St`wV%`)}+9`3x%,-`)}&/`9Y%`g;%`ed)`ac&`[*)`Ws)`V|$`*#)`Cv)`Rh+`CC(`_,(`<F*`#Z)`)L$`<U)`*}2wo`=L+`=]0`+c0`,,5`+e%`+d$y`31$y`#0%`&o,`+a&`E$(`+^+'Ashgrove Manor. Bo`cD$at government auction. `k#$ off since`+V$accident`E6$It is pitch`Nj&F`d~)`r}+ by`#7$`rf*`,?$last=d_`rE$`$}$irty`&V&st=Steer((UP,DOWN),True`+Z)`=:%`=/&`D$*d=st.feed(k)if k`#K$in(LEFT,RIGHT)`i5$st.d`xH&`$I) dt=t-last`4z$_now`id%`54&`${$`8?$t=`@p$.02,min(dt,0`:m&mov`)x*`EZ&`-K&`#z%`-F0`R[)`60$`%t+  contin`#/$`#n%DEL`6W&`-,,`#ZASECOND`6p&`+V%`&V%`#/$`#:%`ea/`#v-`(0%`&|$`#r-`4-&`$0&LEFT`$.&a-=2.0*`yx$t,`O4)`&4%`SE,k==`(S$`#[(+`#[Bif d==UP or d==DOWN`#c$s=(1.6`#B*else-1.0)`<J%`<=%x+`~g-*s`<D*`#=%`~o(`#=%r=0.22 if s>0`#w%0.22
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
e_LEAF=(50,140,6`#6)2=(44,126,54`#7(HI=(90,175,95`#8(LO=(30,95,`#u%TRUNK`$0%7`#7(INK=(20,`#%$)
e_ROUND=(6,2)
e_GRAV=900.0
e_FLAP=-265`#1%ALL=43`#>%SPEED=80.0
def e_column(j,gy):
 k=min(j,e_NP-1-j)
 yt=gy+`&Q$
 yc`#D$`&9$,yt+26)
 if k<2:
  sh=`$f&[k]
  c=`%S(`#H$==0 else `#9%
  out=[(`(8$,gy-sh,c),(`#-%yt+sh,`(2$),(`#1%yc`#G(`#-%`$S%`#G%]
`$&$:
  leaf`$E& if j%2`$E/2`$F24,leaf`$H%4,gy,`%,(`#6$,yt`$U+,yt+4`#D&HI`$j%4,yc`#h%]
  if 6<=j<=8:
 `$6$.append((yc`%()`)P$`$n$<8`$k%dk(`#:&)))
 `%C)`#g8SKY))
 return out`+X%COL`%M)`&<.`)^%bg(p,trees):
 for t in `#5$:
  j=p-t[0]//2`%>%0<=j<e_NP`$W$`$9&`*L+t[1]`$R*`$N(`$8&diff(old,new):
 cuts=sorted(set([a`$M$a,b,c in old]+[b`#84`#M/new`#M2new]))
`)G%]`%P%i in range(len(cuts)-1):
  a,b=`#4$[i],`#+%+`%>$ if b<=a`%f$continue
  m=(a+b)`&4%co=cn`0T% `$4$y0,y1`%#)`#a$if y0<=m<y1`#3$`#X$`#R2new`#R7n`#R$if cn is not None and co!=cn`#](out`#9$out[-1][1]==a and(`#5(2]==cn`%m$`*e$[-1]=`#A)0],b,cn)
 `+0+`+1-`(%$n`+)/`)N%paint(col`*e$run={}`(>%p,spans in col`*r$keep`#C$`#D$sp in `#H$`%<(`#6%run`%B$run[sp`%B%p`$b%keep[sp]=(`#@(0],p+1`%./`#J*p`#A(`$<*ru`&S)sp`&s$in`#U$ or`#^)[0]!=`$.*`#|%e__span(sp,`#>&)
 `%h$keep`%j%`$.-`#T4`&P%`#;*):
`)z(=sp`3G$y1>y0:
  rect(r[0]*2,y0,(r[1]-r[0])*2,max(2,y1-y0),c`#~(clip(`&o$,a,b):`,q.`+/+`(8)y0=max(y0,a)
  y1`5*$y1,b`,n&`$Y)`10.`#p%`)~5bird(y,wing,tilt):
 x=e_BX
 circ(x,y,8,(170,1`7j%)`#=+7,YELLOW`$$$ct(x-7,y-2+`#u$7,3,(255,245,19`#^++3,y-3,3,WHITE`#:*4,y-3+(1 if tilt>`5R&0),1,BLACK`$3)+7,y-1+tilt,5`$3$45`:c$30)`&|(ground(`,K$ect(0,196,320,5,(70,170,8`$c$`#B&201`#B$9,(120,80,4`#B$for x`1C*0`#H$16`.Q$`$Y&4,197,3,2,`;@$200,11`#b$`#E(`<e$8,2,2,(4`&h%5`#D-7,204`#h%95,6`%<&`#e*,207`#d%150,105,6`%^*score_bar(`#-$`%g+`$z%20`6G&
 text(6,17,'Score '+st`#[(,`=A$`+X)rashed(y`6s*if y+8>=`7B$`%t%`*c$True`0G&`&B*(e_BX-e_BR)//2,`#2$+`#2(+`4x%`,I/`8/0`3G%==`%/$`45(`5)) dx=abs(p*2+1-e_BX`0X$if dx>e_BR`#U3y=int`$g$R*e_BR-dx*dx)**0.5`#c(y0<y+dy`1~$y-dy`5))`%a-`#0&False`+((ame`+%$cls(`(1(`+?*`*z+`(V%`(/(`))-0)
`:n%=[[332,`Dn%.randint(20,55)*2],[332+17`#E:]
 shown=[`:v(]*160
 y=1`BG$ v=`#*$`$G$=0
 passed=[`%F$,`#)$]
 wing=0
 go`#R%o`&^%y`%*$`0<$oy,0,0)
 pause(0.4)
 last=`F4$()if`F>%`.~&
 while`&d$`6T$=key(`1i&k==CL`(}%`&~%`#:%`#e$`#9$`#{)`)8$t`2N$0.1`3X%0.03,t-last`-C$`$Q%t`?t,dt=0.05`$8& in(UP,SECOND,OK`+,%v=`EY%
  `%s%3
  v`Di&FALL,v+`F/%*dt`4#$+=v*dt`3z&<`@I$+9`#q$y=`#1&.0`$$%`&_$ go+=`FJ&`#]%step`&t$go/4)*4`#G$-=step
  lo,hi=(16`()%`>V02`%)%t=`*I$[i]
   a=`A:* t[0]`#s)`3R$[0]+e_TW<`5t%`#4$`6G$332`..%[1-i][0]+172`&h$ t[1]=`+%7`#D$`*Q%[i]=`,x% `$w%p in(a,`$Z&`=X&lo`&l$lo`(|%,p`(t% hi`$Q$hi,min`%f$p+e_NP`#B%if`;4$`$3)and`%=+`0o)`$-%`$Y*`.b%  `,J%+=1`;R&`3*0
  work`9f$`1t0`(D$`%.%n=`1L-`$e(`@p(`-~$[p`$i$n!=`#2(`$a%d=`E%&`#:(,`@@%`1Z$`#F%`$N$`:D)p,d`%o%`#T(=n`=+$`@@%work)
  n`.B* a=(min(oy,ny)-10)//2`(c$b=(max`#<&+11`#<)`#s([(p,`<o(`$k(a,b))`4u59`4r+13)//2)`?0$`-7$`)<%wing-`@F$`0%&n`<@&`:k$v>15`:j%-`#3%<-10`:{)
  oy=ny`/T(`6x3 `0o-  message(['You`)h&`7q-+'`3M%.'],'Crash!'`#^$`0h)`#v(01`QP$ULES="Flap to fly through the gaps between`#4$`$&% Don't hit`#8* or`#V%`5L$."
e_KEYS=['Up, 2nd or ENTER: flap','CLEAR: quit'`Lb(main`6I$`32.c=home('GHFLAP','WING IT',`%5&,`$9%,('Play','Back'`*h$if c`/W&`%y)`7Y(
`$<('''
GAMESRC['GHHANG']=r'''import random
f_WORDS='PLANET ROCKET GALAXY COMET ORBIT JUNGLE TIGER PARROT DOLPHIN OCTOPUS PENGUIN CASTLE DRAGON WIZARD KNIGHT PIRATE TREASURE ISLAND VOLCANO DESERT GLACIER THUNDER RAINBOW BLIZ`#s$TORNADO PUZZLE RIDDLE SECRET MYSTERY CIPHER LANTERN CANDLE MIRROR LADDER BAS`%e$UITAR TRUMPET VIOLIN PI`$_$RUM`%N$CIL ERASER NOTEBOOK BACKPACK LOCKER SCIENCE HISTORY ALGEBRA GEOMETRY CALCULUS PIZZA PANCAKE WAFFLE NOODLE BURRITO PRETZEL COOKIE MUFFIN BANANA AVOCADO'.split()
f_ABC='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
f_INK=(20,`#%$)
f_POST=(225,175`#7&USED=(190,`#&&)
def f_letter_box(i,used,sel,full=False):
 x=4+i%13*24
 y=150+i//13*28
 c=GOLD if i==sel else `$<% if `%5$[i]in used`#B(INK
`#B$ull:
  rbox(x,y,22,24,3,c,2,WHITE)
`#W$:
  edge`#H9text(x+6,y+18,`$A(,c`%[(word_line(w`%Z%new=Non`%T%0=310-len(w)*20
 for i in range(`#=%):
  ch=w[i]
  if new is Non`$n$`$P&0+i*20,85,ch if ch `%s-'_',`%w$)
  el`#E$==new`#i5'_'`%W)`$,4`#p(`%Y%figure(n):`&{$n==0`&{$rect(0,136,120,12,5,(110,180,90))
  `#G(40`#G$4,(80,150,7`#C+8,132,74,6,`*|%`#=-6,74,2,dk(`#@%,0.75`#b*24,18,5,11`#c127,18,2`#>$`#d?2,5`#c14,21,52`$F6col`#7&)
 `)B$o`)B*4`)=$ draw`*.%29+o,44,50+o,23`$.)72,23,3,13,(140,90,4`&1(turn
`$2&`)?%`(<%1`(<$ing(73,46,10`(p%`+p+`#c)a=((73,56,73,95),(73,65,60,82`#1)86`#1)95,62,118`#2)84`#2$)[n-2]`+|%o in(0,1`%W$`%V*a[0]+o,a[1],a[2`#/%3]`*T(game():
 w=`6=%.choice(`6D&)
`,+$=''
 bad=0
 sel=0
 cls(`%L(`+C)0)`-U126`$]$`0}8True`#g$`.d0)
 while Tru`-y$done=True`)A&`-r%`-N%`.%%not`.*(`#9$`#V%`2%$`.r%d`.k(message(['You got it: '+w],`#5$win!'`.1$`(v( if bad>=6`#f/The word was`#g&Out of guesses`#m/k=wkey()
  old=sel`$&%k==LEFT`$($sel=(sel-1)%26`04(k==RIGH`#F.+`#F0UP or k==DOWN`#N/3`#O/CLR`#E$`$i)`#<(OK and`4k&sel]`&u0used+=`#C*`(D&`#4*`(Z)`4&4`#J*`&4$`53(  bad+=1`#Z&`*c&bad)`&;%old!`6_$`%R%OK`#X$`*i-old`*k)`$%$`#A-sel`#A+f_RULES='Guess the hidden`)6%one `#a% at a time. Six wrong`)E(`&A$the game is over.'
f_KEYS=['Arrows: pick a`#x&','ENTER:`#l% it','CLEAR: quit']`.J&main`.J%`,j-c=home('GHHANG','HANGMAN',`%G&,`$J%,('Play','Back'`1f$if c<`5j$`)a*`/Z(
`$<('''
GAMESRC['GHMERGE']=r'''import random
g_X0=90
g_Y0=26
g_S=36
g_BOARD=(187,173,160)
g_TC={0:(205,193,180),2:(230,225,215),4:(235,220,190),8:(240,170,110),16:(245,140,90),32`#3&10,85),64`#3%80,50),128`#v&0`#G$),256`#5(`#g%51`$N$5,195,70),102`$P&19`#k%204`#l&185,30)}
def g_add(b):
 e=[i for i in range(16)if b[i]==0]
 if e:
  b[`&W%.choice(e)]=4 if`&p&.`#*%()<0.1 else 2`$9&slide(row):
 r=[v`$=$v`$=$ow if v]
 out=[]
 pts=0
 i=0
 while i<len(r):
  if i+1`#4&and r`$u$r[i+1]:
   out.append(r[i]*2)
   pts+=`#3%
   i+=2
 `$s$`#X4`#V$i+=1
 return(out+[0]*(4-le`#2$)),pts)`%U&move(b,d):`%3)nb=b[:]
`%a$j`&{*4`%:(d<2`$G$idx=[j*4+`(K14)]`$r,`#L$i*4+j`#L6if d==1 or d==3`#W(.reverse()
  row,p=`(T([b[i]`#q)idx`%n$`&E$p
 `$0$n`%+0 nb[idx[n]]=row[n]`&>)nb`&,,draw(b,score,old=None,o`#3$=-1):`&3%`+0.:
  v=b[i`%B&old and old`)P$v`$M$continue
  x=g_X0+i%4*g_S
  y=g_Y0+i//`#5(c=g_TC.get(v,`,n&0,20)`&)$rect(x+2,y+4,g_S-`#)%5,5,dk(c,0.8`#L12`#L/c)`$z%`$j%`#L&7`#w)14,2,lt`#r$4`#r$`#O)s=str(v`+%%f len(s)>`(}% s=s[:2]+'k'if v>=10000`-b%s
   tc=(60,55,50)if v<8`#A%WHITE`#E$ext(x+g_S//2`+r$s)*5,y+25,s,tc)`/2$`(S$!=`([%:`%_)95,182,130,24,6,`2j&)
  c`#~$200,'Score '+str(`#f$),`$I$`)p(frame():
 cls(`#>&`$,&12,34,6`#%$8,dk(`1N,`(:(`#N*2`#N)`#K,)
`%X%24,70,'2048'`$M(`#=%12,128,'Join',(12`4+$,10`#b*12,146,'same`#F;64,'tiles!`#H7250,60,'Arrows`#H;78,'`./$`#G2`%d%g_X0`*s$Y`#*%S*4+8`#+)8`(M*`(%%g`($(b=[0]*16
`5$)`#-,`.(%0
`(X*
`.U/)
 won=False`3r(Tru`*$$k=wkey`0A$d={LEFT:0,RIGHT:1,UP:2,DOWN:3}`-r$k,-1`,I&k==CLR`,|&turn`2I(0`.|0nb`1?$`3>)`#L%nb!=b`4?%b,osc=`$z+  b=nb`-P$core`1Z%`%f+ `1+1`#h$`-x(2048 in b and(not won`20%`%|$Tr`$d$  message(['You made`#a$!','Keep going?'],'Amazing!'`$.$`(*,`$W1)
  stuck`$2(for dd`3d1i`6H,d)[0]`&)(`#d&`(q&`.z$tuck`#?$`%#*Final`&9%`.U-],'No moves left`%#%`(e&g_RULES='Slide the `,X$. Two`#.% with`#=$same number join into one. Try to mak`&K(
g_KEYS=[`-+&: `,i$ all`#}%','CLEAR: quit']`9?(ain`,A$`+L.c=home('GHMERGE'`/V(`%2&,`$8%,('Play','Back'`3x(c`+9&`+M)`-O(
`$:('''
GAMESRC['GHPONG']=r'''import random
h_PH=36
h_TOP=24
h_TABLE=(30,85,165)
h_BALL=(250,150,40)
h_LINE=(150,190,235)
def h_net():
 col(`#J%)
 draw_circle(160,117,28)
 for y in range(`$S$+2,208,14):
  rect(159,y,2,7,WHITE`$6(cour`$8&ls(`%.&)
`#W%0,207,320,3,`$S)`#=&`$2%1`#A$1`#A*`%/&`$(&paddle(x,y,c):`#a&x,y`#U$PH,lt(c)`#y(x+1`#=*c`#9*2`%)$4`#6/+4,2`#N$-8`#l$,0.5`#p+2,y+`#A$4`#a04`$/55`#9*dk`$a$`%3&uck(x,y`%/*-4,y-4,8,8,`)>%`#j)-2,y-2,2,2,lt(`#@%,0.6`#r)scores(a,b`#t)0,0`&[$`&i$-2,`(A*text(110,18,str(a)`#8(20`#8)b),GOLD`(V/-2`#y$2`)Q(`#q&4,18,'YOU'`(q*`#v%5`#v$'CALC`#?*`%$%game`*-$`*9)
 me=cpu=0
 py=cy=100
`%P*me,cpu)
 serve=1
 while me<7 and cpu<7:
  bx,by=(160.0,110.0)
  vx=4.0*`#c$
  vy=`-p%.choice((-2.5,-1.5,1.5,2`)_%`*}*8,py`%m)`#:*306,cy`&G( pause(0.5)
  st=Steer((UP,DOWN`#w$`%(%True:
   k=key()
   if k==CLR`#<$ return
   opy,ocy=(py,cy`#O$d=st.feed(k`#a(d==UP`#_%py=max`.a&3,py-6`#I$ if py==`#<&`#P% st.stop`$O%el`#p%DOWN`#r*in(206-`,$$py+`#s.`#=(`#t4target=by`#E$/2`$x&vx>0`(w$bx>120`#^%cy+`%($-4,min(4,`#b%-cy`&Q$ cy=int(`%K,`$e-cy)`#L%obx,oby=(`)s$`#6$bx+=vx`#-$y+=vy`$R&by<`#p%6 or by>202`$W%vy=-`#J% b`&h,6`$>&2,b`$c&if bx<18`%A$vx<`%J$(py-4<by<p`0)%+`2|%`+<$min(9,-vx*1.0`&e&vy+=(by-(`#S&/2))/6`$I%x=18`$3)>302`$4&`&[%(c`$4&c`$43ax(-`$59`#T&`$5.30`(e$vacate(int(obx)-4,`#.%y`#.(`#8*`#7%`1X%`0_(`$y$opy!=py`$X&`#v%8,opy,`-O$6`2_%`#X0cy!=c`#X.306,ocy,`-q&`#]6126<obx<194`#b%`5q(`$W- or 0`#K$2`#J)`/25`$V+ or 29`$(%3`+c(`/R8`4s(`&<&`&:(`*7+`,I(pu+=1`#.$`1s)   break`)T+`$:(me`#Q.-`#R.`4<$`(WC`&-*`3F2message(['You '+str(me)+' -`#1&cpu)+' Calculator'],`#P$win!'if me>cpu else '`#J* wins')
h_RULES="Bounce the ball past`#1$c`$$*s `&|%. First to 7 points`#u$."
h_KEYS=['Up/Down:`#V& glides that way','ENTER: stop`$3$`#L%','CLEAR: quit']`7&&main`7&$`4@.c=home('GHPONG','`#*%`%G&,`$X%,('Pl`$=$Back'`)b$if c`)_&`4k)`84(
`$9('''
GAMESRC['GHRPG']=r'''import random
i_T=20
i_MAPS=(['T`##/','T.`##$T`#+(`#6$HH`#1%`#61C`#6,`##->`#6(~~~`#66TT`#]1`#63`$))`$w0],`%18`#c$`%2$T`#s(T.C`#6-<`#~&`#)&`#6&`$I$`#9&`$y&`%{&`#6,`#2&T`$y*`#[%`&#-`#p&`%1?#`##/','#::::`#($`##$`#6&C:#:##`#&&','<`#I%#`#O&`#6)::#:B`#6)#::`#|$`#O&`$))`$&)`#6&`#G$`#M%`#I.C`$O+`$w0])
i_NAMES=('Meadow','Whisper Woods','Hollow Cave')
i_FOES=((),(('Slime',12,4,1,6,(80,200,90)),('Bat',10,5,0,7,(120,90,160))`#d$Bone R`#H$8,7,2,12,(220,`#&$0`#j%Cave Eye',22,8,3,15,(200,60,`#o$)
i_BOSS=(`$x(King',70`$e%0,(110,80,180`#Q$GRASS=(40,110,50)
i_STONE=(60,55`#6$def i_grass(px,py,x,y):
 rect`#5&i_T`#&&`#x$)
 h=(x*7+y*13)%5`#P)+3+h*2,py+5+h,1,3,(70,150,70))`#J*5`#J(6`#J$2`#J713-h,py+14-`#s&3`&u$4`#I$if h==2:
 `#T*4,py+4,2,2,(24`&|%9`#Q$el`#S%4`#S,`#R$15`#S&30,12`(z&`&0&floor`&0C`&q$)
 o=0 if y%2 else 10`#T11,(45,40,38`%^,o,py,1`#E$`#C5`&G$2,6,1,(75,70,64`$s)tile(m,x,y,ch):
 px=x*i_T
 py=20+y`#0%if ch in '.>< ':
 `)d3`&D&ch=='T`#G9`$e)8`&]$2,4,7,(9`+f$3`(1$`(U*0`#F&2,7,(65,42,22`#F$circ`#F*8,8,(20,7`#h)`#C(9,py+7,6,(35,100,45`$--6`)_%3`*X1`%<*~`%<$`)#3(4`.Y%`*5% o=(x*5+y*3)%8`$-+o`+f$`(@%11`*4$,23`$Q.(o+9)%`+:%14,5`#O3`$[*H`&vB`)[$8,16`0*%00,1`/?$`&z.`#I$1`#J$2,(160,1`-*$`&Z%ol((170,5`-:( fill_poly([px,`(=&x+20],[py`(+$,py+9]`#e*20,35`(T(draw_line`({)`#d%`#X$`*(23`*(;`&B%1,3,3,(250,`..$`$t&`/W*`#I;`&j*C`&j%f m<`/g$`&u6else`#A&`/-0`$=+`$<$6,14,11,(60,40,`(5/`%,$7,12,9`(4&1`&|)`#G22,(19`%%$`4c$`%v1`4X$2,GOLD`#@,`,S$11,2,3`#?(`%d*c`%dm`$P+6,(10`..,`#G31,(`*s$5`.2&`$a*#`-k930,28,`-4&`2p05
  for yy in(0,7,14)`%($`#p*+y`3.)50,47,5`2i$`#[$xx in(o,o+10`#[-+x`$P$`:4$`#Y-`._*xx+5)%i_T`(o&`#N0`%N*:`.]&`&c2`#G*B`#G9`23/11,8`;q$55`,N)`#E/0,8`:S/`.:%`*4(`.u-+3,`2O%`.|(14`#)$7`/&%4,py-1,py`,8$`#-%4`/3$`9n)`0g%3,3,RE`+;-1`1&&`#>3`3h$14,8`7c$0,25`3h%`6|%hero(`8j&`6w7`$H-18,10`9e$5`0$*`&-.5,4`:Y&0`:)(`$W/`>X$`1R$`+z)`10-5,1,1,BLACK`<8,`&*$`#?6`#}$9,8`7H$`;J%2`#~.`$D%3`%z%12`(s$`):%`#E.6,3,4`0I(`#h.`$K%`#E=`&<$4,2`14$210,215,22`-U$`=x.`9i$`0G(`(K%`4J$map(g,after_msg=False):
 m=g.m
 r0,r1=(0,10`>~%`#N)`/&$0=max(0,(MSG[0]-20)//i_T`)z$1=min(1`#A)+MSG[1`#H*+1`-+$`1-%i_HUD[0]=None
`/L% in range(`$Q$`.s$`/-$`#<*16`/.%`=h-g.maps[m][y][x]`%*%r0<=g.y<r1`$9%`+?$g.x,g.y)
 i_hud(g)
`$S$=[None]`+l(`#=$:
 t=(`G3&[g.m][:13],'HP'+str(g.hp)+'/`#1(mhp),'LV`#3(lv)+' `#P)pot`Bn&t==`%r(`2t%turn`#=$`#:(is Non`&A$`)>$0,0,3`G%$`+P) old=('',`#%$`&t+old`$))`&s%i,x,c in((0,4`)|%,(1`6p$WHITE),(2,2`#1)`&|$if t[i]!=old[i`$t$ text(x,15,`#8%`$V*`#>+t[i],c`&|$`)H&t
class i_Game:
 pass`(*&bar(x,y,w,v,mx,c):
 f`*t&min(w,int(w*v/mx)))if v>0`5o%0`&J$v>0`*4$`#W$2,f`,g(x,y,f,6`$T$`#4%+f,y,w-f,6,DARK`F4)oe_art(f):
 c=f[5]
 n=f`&V$if n==`L<&:`44(`GN$5,30`$($`$)%19`#7$`1S$`#:$`5L$n==`LZ$`#_$ol(`#S$`4I+17`LA&`#+%],[80`C<$8`0^$`?B%`$=(10`9R$`$&.`M>(`$i-100,2`#M%`#8&45,85,1`$~-7`=%%30,3`#z.`Mp)`%e8`#7,14`*D&`#;/6`*+)`+M(`&@&`H]$5`@w$`#r.60,18`#7&`7o6200,205,212`&O%28,235,240],[4`$m$42,28,42`#/$5`7k*208`O#$,5`7K-227`#:.`)Y710,92,3`,N*`#:%3`#:/`(X<45,83,2`#O(`,](ttle(g,`+4$name,fhp,fat,fdf,xp=(f[0],f[1],f[2],f[3],f[`:9$mx=fhp
 cls()
 rbox(15`):$14`NX&0,f[5]`$B*`,O-
 c`.f$26,name+' appears!'`B%(opts=['Attack','Potion','Run']
 sel=0
 log=''
`/Z%12,56,'You'`*+)`#<(8`$5%[:1`%>$`(d$`1D$`4{*3`0|$c=GOLD`2]$==sel`/G%`#t$
 `%^&0+i*102,154,96,24,`*O&`$8$58`#B%-len(opts[i])*5,172,`#2&`#Q$was`6k&while Tru`+h$now=`4|$`(S$sel,log)`2e%was `4:& or was[0]!=now`4l&`1~&12,62`(I$`#n$`5c$,GREEN`#n:1`#n&1`#n/9`#n%fhp,mx`+}(`#h*not`#l%and`#m$2]!=sel`#j$`&}((`#<%,sel`8|%`(&?  edge`();`(+O`%f73]!=lo`<1$`%C3`$u%`*O%0,202,`#W%[:31`6j1`#E&log`#B%GREY)
 `)L$now
  k=wkey(`$X&k==LEFT`$.$sel=(sel-1)%3
   continue`#N)RIGH`#O.+`#O7!=OK`#L$`#;.sel==`7=$ d`7>$1,g.atk+`h.%.randint(0,3)-fdf`%J$fhp-=d
  `-l%You hit`);$`<+%d)+'.'`L+$`$.(`=m$ if `<G$`$>(`#f%No p`.s$s left`#^$`$u-`#X%-=1`#/%hp`@D$`+t%g.hp+25`$e$`$Y)feel better`$R*f is `aX%`$G$log="You can't run from him!"`#X(`%{+om()<0.6`Kh&turn`.F$`Nc,`#y$Couldn't get away."`(-%fhp<`%m&g.xp+=xp
   msg=[`%)$won. +`&^%xp)+' XP']
  `/]&g.xp>=g.lv*1`P>%`#6$-`#6(`#5&lv+`&D% `&<$+=8`#0&atk+=`#I(dfn`#J*hp=`#O$`#2$msg.append('Level up! LV`)E&`A]$`(0$message(msg`4F(defeated'`Nc&`&?,`*r(fat`*p5`$_$)
`$Z%`*r%log=log+' It hits`*r0`*b$`&r*`$](`&j%fainted...'],'Game over`$h-`Gp$`80&play():
 g=`A/%()
 `E~%=[[list(r)for r in mp]for mp in `q0%]`#R$=0
 `F/&=(4,4`#j$`&|(=3`#A$atk=6
`(F%=1
`(w$`#+%xp`#e%pot=1
 steps=0`9.)`J*,)
`%d+The `ih+ took',"the village's light.",'Bring it back!'],'TINY QUEST'`$1/,True)`6t0`1W1CLR`/6(`$b*ENTER: quit adventure','CLEAR: keep going'],'Quit?')=`1K(`H.) `$Z5`/w-dx,dy={`3*$(-1,0),`2f%(`#/$UP:(0,-1),DOWN:(0,1)}.get(k,(0,`TC%if dx==0`7=$dy`1E(`$0+nx,ny=(g.x+d`)G$+d`Uk$m`)D$aps`K1$`#p%nx>=16 or nx<`/G(m+=1`#@+else-`1x&x`Y>%`#=+ 15`%o0`%j0ch=mp[ny][nx`$B&`i/&T~`Z^%`5-/`e,+`/H/`Mk)`-J1rest by the fire.','HP`#:$ored`-b$Cottage`-_%`(oA`br. `%4*='c`5:$`,[$`1>&`/$/ound a`5p&`+q$Chest`$DO`Z{%`Nt%`CU)`5Y%`<W&`0R&`Kk%  `.*(`2i$`-z-`-W$`+b&s to','`-z+. You did it`-m%HE END`$|%`,>+`#-)ox,o`*t%`RF&`0E*`+4$`+a$`SA%g.m,`#R$,mp[oy][o`S@$`S02`0?%`&k%`%g$FO`Rq&and`#@%>6 and(`7}212`&*%`1))`,:%ot`&S,`#Z&choice(`$*+`QB%`.w8)
i_RULES='Walk`*r$m`yc$, woods`.5$cave. Rest at`#G$c`*~%, open chests`<N$`;q&,`.o%`6q$`#T$`2b+.'
i_KEYS=['Arrows: walk','Fights: Left/R`)>$+ `1d$`1R*quit'`Vc(main`5o$`2d.c=home('GHRPG'`3I-,`%d&,`$N%,('Play','Back'`1%(c`0)&`&N)`7%(
`$>('''
GAMESRC['GHSIMON']=r'''import random
`#1&math
j_CX=160
j_CY=116
j_RO=84
j_RI=36
j_PADS=((UP,2,(30,130,50),(110,255,130)),(RIGHT,3,(150,30,30),(`#C$10,11`#G$DOWN,0`#l$60,1`#l%20,17`#p$)),(LEFT,1,(16`$5%2`#l(235,100)))
j_SHAPE=[]
def j_shapes():
 for q in range(4):
  xs=[]
  y`#+&for i`#H*9`#H$ a=math.pi/2*(q+i/8)
   xs.append(int(j_CX+j_RO*`#P$cos(a))`#L$y`#L0Y`#L+sin`#L(`$H/8,-1,-1`$NSI`$NH`#L&`$N+`&[&`#P((xs,ys))`&j&gap`&h%d=(15,`#%$)
 rec`$G%-4,j_CY-j_RO-1,8,`#,$j_RI+1,d`#M3`$O$`#K=`#p&`#|$4`#K-8`#M.`#p%`#K9col(d)`)p%r in(`#R&`#F$`#*$2`()$draw_circle`#|$`#w$,r`%u(pad(i,lit):
 k,q,dim,bright=`,q%[i]`$8%`#9% if lit else dim)
 `&n$=`()&[q]
 fill_poly`(/&
`(+)`$A&body`(8$if not`(h(:`(s$`,A(
 circ`%&+j_RO+8,(6`-Y$65)`#F75,`)4*`&;&`+<+`--%`%n(False)
 ring`#m.I`#k+,3,(70,70,75`*K)score(n`%8(:
  text(6,17,'Score '+str(n-1),BLACK)
`&R$`#O)204`#Q$CLEAR quit',GREY)
`#q9))`$:*s=`$)(`#v(`*t$len(s)*5`+H%7,s,(25,25,28)`$L+`&T2I-6`#N.`$+&`$Y(`$(7WHITE`&/(flash(i,`*b$`(%(True)
 pause(t`)y$`(?.`#=%0.12`.F*me`*1$cl`)u$`*C(
 seq`2$$while Tru`%?$`(P(`$k$eq`/O$seq`/K(`5Q%.randint(0,3`#E$`$B(5`&Z$=max(0.18,0.5`%Z%eq)*0.02`1r-seq`1g$`%a,`#C&want`#F,k=wke`%($  if k==CLR`#=$ return
   got=-1
 `2|1`+c%`#^$`.8)[0]==k`#;%`#^$i`$%&got<0`#;%`#v$2`#;*>=`#<&`$~(got,0.`24$`#G(!=want`$:)`#Y, pass`#-$message(['You got`+K&`&D(-1)+' in a row.'],'Wrong color!'`$:$`%m(j_RULES='Watch the`#J%s l`0e$up, then repeat them in`#L$same order. Each round adds one more.'
j_KEYS=['Up: green   Right: red','Down: blue  Left: yellow'`.?&:`.@%`9Z(main`+K$`+2.c=home('GHSIMON','`#+&`%U&,`$S%,('Play','Back'`+7$if c`(y&`)z)`,Z(
`$;('''
GAMESRC['GHSOLI']=r'''k_CW=40
k_CHT=30
k_TOPY=4
k_TABY`#?%RANKS=('','A','2','3','4','5','6','7','8','9','10','J','Q','K')
k_CARD=(245,`#&%0)
k_BACK=(40,80,16`#6$FELT=(15,70,40)
def k_cx(c):
 return 6+c*44
k_PICS=(('.##.##.','#`##%`#-7.`#,$.','..###.`#-%.#...'),(`#/)`#C-`#W)`#mt`#w+.#.`#K.`#m%`$(*`#-(##.#.`%S1`#7(`$D+`#m(`&^(_runs(pi`&d$out=[]
 for r in range(7):
  row=pic[r]
  c=0
  while c<7:
   if row[c]=='#'`#6$ e=c`#+$`#M%e<7 and`#J$e`#J, e+=1`#-$for k`$E*len(out)`$L$   a=out[k]`#1%if a[0]==c`#|$a[2]==e-`#1$(a[1]+a[3]==r`#d( `#c%=(a[0],a[1],a[2],a[3]+1)`#H&break`%0%lse`#_&out.append((c,r,e-c,1)`#V%c=e
`#Q-c`%@$`+M&out
k_SUITS=[`(1))for p in `+h%]`(P&suit(x,y,s,k=1):
 c=RED if s<2`$.$ BLACK`(h%a,b,w,h`#m%`$.$[s]`(p$ect(x+a*k,y+b*k,w*k,h*k,c`-B)ard`$4$cd,h=`/<$):
 if cd is Non`%@$rbox`#K$k_CW,`#K$,4,(60,110,80),1,`.M%)`$B$turn
 r,s,up=cd
 r`$V%`#g(h,4,`%3$)`$7$not up`$3$`%$&1,y+1`#O$-2,h-2,3,`/i%)
`)Z$h>=12`(($`#T&4,y+4`#T%8,h-8,lt(`#U%,0.15`(g%for i`*i*x+7,x+`#W$6,6`*.&`#u$i,y+6,2,h-12`$C+`%J)`$r<CARD`%H%h>=14:
  text(x+3,y+14,`2~&[r],`)<5)
 `)m)`$j%11`%O$s`#|)`(A$:`#K,1`$&$5,s,2)
class k_G:
 pass`)T&new():
 g=k_G()
 deck=[[r,s,False]for s`&9*4`+V$`/W+1,14)]
 shuffle(deck)
 g.tab`0.)c`0.0pile=[deck.pop(`#z$`(F+c+1)]`#J&[-1][2]=True
 `#~%`-x(pile`$7$stock=deck
 g.waste`$G$g.found=[[],`#%(]`.-)g`%y&layout`#s%:
 dn,fu=(5,15)
`1C&Tru`,R$ys`#}$ y=`8#%
`*P%cd in`${$`*@$ys`$n(y`*u$y+=fu`-F%[2]`)>$dn`+m%not`#[$ or ys[-1]+`)1$<=208 or fu<=8`,3&`%&$ys
  fu-`2c$if fu<`,T&dn=3`%D&draw_col(g,c,drawn):
`(6%`&Z$[c]
 x=`8a&
 ys=`%{.
 n=len`#0(d=`#j$`#Z$start=0`+.$`/f$not`/j$`3]$n:
  old=d[0]`5I)`#W$<min`4P%ld),n)and old[`#@$]==ys`#.&`%?$`#.$`5<%`$<%min(`#-$,max(0,`#s/-`3g$`&m+`,k%`1q&`(p%,None)
  bottom`)+&`(1%
`4>)`#@&`(N,`(*%`%a3<len(d[0])and`$k%==n-`47$`1)(,`#v%-6`20%6`2_+`,T/`%P%`(m$`%-+ys[i],`,j$i]`3X% if i`$3$`/y%ys[i+1]-`#N$+4`%|%`4D) or`%F&<d[1`5D+`$f&`$d%210-`#3)`$m&`)](=(ys`#P&`5f(top_state(g,s`5_&s==0`$(%`+a$len(`.F&)>0
 p=`.F&`#O&`%.&`.O&[s-3`.F*tuple(p[-1])if p`#N%None`,>,slot`$J(`,*&`2Y&`$U(`)j,OPY,[1,0`1|&if`02(`$&*`4j,`${E`$*0`$~$`$}.`$[&>1`<N$`+S$`)H$`4>,`#c%+8,s-3,2`&~(frame`8T$h,top`2J$):
 t=2 if to`$0&0
 r=[(x-2,y-t,2,h+t+2),`5k&`#80,y+h`)Z&)]`$i$to`9C%`=@)x,y-2`#G()`(U)r`$e&marks(g,s`+c%`7:$`@X$`#K&`%,(`(Q&`&5(`;v%`&t%tab[s-7`$J%`&-$`#e9-7`#g$AB`#g*`1O-)
 i=`/g%`1R$)-n`%#*`#p2`-R%`//,`-:%,i==`GA)fits_`)O$(cd,f`.($`=~)[1]!=f`$|+`*_$`$=)cd`B6$`3)$`7H$0]+1 if`5#%`(s$1`$2-tab(cd`$.,`1e,`#{.13
 t=`$$(`-2*[2]and t`CX%d`$>%and((t[1]<2)!=(`%+$<2`F:)tak`.j$rc`).*rc==1`$A*[`,a&[-1`8l,`)$%rc-7][-n:`B_(remov`#x:`#q&`:t%`3^*`)w)`#u$
  del p`#}%`3g$p`-<*`;4&`2j%`#1(`;B%`%E&ry_`$O,,dst`D5$ards=`%g/`$l$3<=dst<=6:`9l&!=1 or`(C$`)q.ards[0],dst-3,`/Y(`#1$`$]&`)x.`&*2`%x$`#Z,`-v(`$%(`0z*`<@$`4]%st>=`In%dst!=sr`H}%`*K,`$g(`&d%dst-7`$^%`$M6`#H*.ext`$K)`$H1`%A-`+h&aceup(g,`LZ$n=0`@L&`=x$`<)(`&e&`=e$`&1$n`ID,n`#p&game`B6)`BB$
 cls(`6c)cur=7
 depth=1
 held=`5?$ cols=[None]*7
 tops=[-1`#0$shown`?l$`@%.wan`NV%`D9$eld`$g$want+=[(r,WHITE`C?*`2-*held[0]`#+%1]`BS$`#Z*GOLD`#Y4cur,`%,$`$9(`9i)`/T&]
  busy=want!=`%($`;:&r,`D9$`#6$`O|&(r,c)not in`$G$`H>+r[0],r[1],r[2],r[3]`<1/s in(0,1,3,4,5`H~(st=`:G0`Q4&st!=tops`Lw& `9H1`#8$`#E&=st`#2$`%=$`ET&`FJ5`/;)c`Q,$if`)-$[c]`<w+`#5&[2]!=[`;+%cd`&y$`Dl&`$[.`CB(col`$a&`#f&=`#+&+(`#k6,`#Q%`%$,if`#2$`$*$`(D+`(,Cc`#r$`+,%want`#r%sum(`BY$f`$D$f`-#%`/O$))==5`Ed%message(['All 52`1I% are home.'],'You win!'`$2$`<o( k=wkey()`Dy&cur`$C%k==CLR`*E&`,E*`-B,`&A$ntin`%m$ if`$R+ENTER: quit this game','CLEAR: keep playing'],'Quit?')==OK`&?(`$l&`.y.`(Z%`._+`*N%`.b)`&Y(`.K$`$j,`%C%LEF`Nn$`/h$cur-`9*$cu`4=%`,:$7)`-]$cur+6`*p(ur==`((%`#/$1
  el`#w%RIG`Oh%`#x(`:#%`#x+6,13`#y)-`#y83`#y+DOWN`41$cur`Zd&`1f$+`(]%`#J(UP`#H(>=`[/)`0#$<`3O,ur-7`Iq$`06,`$C%`#P$`[&&`Xw+`&4&7`$t&-7!=`Rs&`%m,`$r,`6=&(`#v$>`HZ&`#0$`MG%`#W(`)D&`1l/`$A%`&-(`Dy$`#3%`Da&`#4& cd=`#5&`:~(`#:&`Q]+  `;H*`8G(d`#M&`[}+`Qr)`<i(::`>#$`##$`6o,`$K-`$5&`9s(`$6+`+$&`%Z%`%8$`>S$`#B(`#f&`->$(1,`^g&`#P(`9r(`1x&ur-7]and(`),1>=`&n$`_r(`#t%`5^)`#z$`%U*`:($=held`.c3`=W3cur)`(l+SECOND`$d$`(m1src=cur`(t)`=_$`%:&else-`*a$`?z%>=0`*($`@*%`&-, or(`#D$`%q,`@(%`d.(`28)`XK(`*)*`%311,3+f`d&)`c[(`$o%!=o`1_&`;,)`#=&`>/)`+p$max(1,`(71`,++`Fx$`#F4
k_RULES='Build four`E*$s from Ace to King, one per suit. In the columns, stack`4V&down in alternating colors.'
k_KEYS=['Arrows: move   `3k&pick/put','Up/D`#o(`$3&: more`$1%',`4D% o`$U%deck:`Q9$','2nd: send`#O$ to`Ls$`%L$`4f*quit'`Ep(main`?U$`>U.c=home('GHSOLI','SOLITAIRE',`&V&,`%D%,('Play','Back'`cX$if c<`/o%`7E*`@i&
`$>('''
GAMESRC['GHSUDOKU']=r'''import random
l_S=20
l_X0`#+%Y0=15
l_INK=(20,`#%$)
l_PEN=(40,90,200)
def l_make(holes):
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
 c=i%9`&6%j`&6*81`$@$if j!=i and b[j]==`#o$`#;$//9==r or j%9==c or(j//27==i//27`#X$j%9//3==c//3`%9.`%+$`$_.l_SHOWN={}`%D(ell(b,fixed,i,cur):
 x=l_X0+i%9*l_S
 y=l_Y0+i//`#4&bg=(236,238,246)if `#h$[i]else WHITE`&<*c=(`.?$ `#K0RED i`&u.`#;$`.]$)if v `#3$None
 on=i==cur
 old=`%>&.get(i)`(I$old is`#R$ or old[0]!`&m%rect(x+1,y+1,l_S-2`#)&bg)
 `#w$`$1%`$A$and(`#s31]!=c`(%$text(x+5,y+16,str(v),c`$Q92]!=on:
  k=GOL`%j$on`%O%bg`$k62,k)`#=.l_S-3`#A93,`%D%6`#=-`#W%`#A0`&U&[i]=(v,c,on`2](grid(`.z310`%k$c=`)1)i%3==0`%5$(150,`#&&)
  t=2`#E/ 1`,I%t==2`+[$`$k$`*w%*l_S-1,l_Y0-1`$s%*9+2`&i$`#L+`#F&`#S+`#J%`#L&else`$#$col(`#_%draw_line`$3+`#i$,`#3/+`#q$`#W3`$<+`#W%`#L$`#9+`&O)am`6/,=`6A-
`,R%=[v!=0`&s$v in b]
 cls(`-1$`(T$`(<%
 rbox(208,12,106,30,8,`,s$,2,(225,235,252))
`+?%222,33,'SUDOKU'`#P%`#@)14,70,'0-9 type',GREY`#A,90,'ENTER +1`#A2110,'DEL eras`#c3130,'CLEAR quit`#D)`.L(clear()
 cur=0
 while`/[&cur]`*h$ur+=1`++1`2o&`1I5`#n(Tru`)b$k=wkey(`.z(`/|$ if k==LEFT`2w$cur%9`*4%ur-=1`*F$`#G%RIGH`#H+<8`#J(`$d$`#J)UP`#G(>`#E)-=9`#E+DOWN`#G(<7`,J%`#l$`#H,CLR`,e&turn`#<(not`&0/ v=-1`5M&k in NUMS`4~%v=NUMS[k]
 `#}*OK`#@(b`#i$%9+`#d$`$i)EL`#D(0`#|&v>=0`#7%`#V%=v`#0$`(I6`#V%`$t*i`$r% `(e9`#T%0`#V$in b`&2$`;^-    message(['Every row, column and','box is complete.'],'Solved!'`$1%`&f*`$U/old`$W(`#=/cur`#=%l_RULES='Fill the grid so e`$Z4 3x3 box has`#Q$numbers 1 to 9 once. Red`#<)`7m$.'
l_KEYS=['Arrows: move'`.E$:`.F$ a`#W&'`.<&: count up  DEL:`./(`-v%:`-w%]`C2)in`4R$`,x.c=home('GH`/s(`/|+`%m$,`$e%,('Easy','Medium','Hard','Back'`>{$if c<`*?%`(1+`2G$(36,46,54)[c])
`$Z('''
GAMESRC['GHTTT']=r'''import random
m_LINES=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5`#;&4`#+$2,4,6))
m_X0=85
m_Y0=28
m_S=50
m_INK=(20,`#%$)
def m_winner(b):
 for a,c,d in `$[&:
  if b[a]and`#+$==b[c`#)$d]:
   return`#?$
 if 0 not in b:
`#A)3
`#-(0`$E&cpu`$B*who in(2,1):
 `$U9 v=[b[a],b[c],b[d]]
 `$n$v.count(who)==2 and`#7)0)==1`#d$`$N&(`$%$)[v.index(0)`%+%b[4]==0`%(+4
 free=[i`$_$i in(0,2,6,8)`#T$i]==0`#c%not`#P$`%2$`#X/ range(9`#X.`$/&`)l%.choice(free`(_(cell(b,i,cur,full=True):
 x=m_X0+i%3*m_S
 y=m_Y0+i//`#4&if full`%=%ct(x+3,y+3,m_S-6`#)&WHITE)
 edge`#D54,GOLD if i==cur else `#Z$,3`#d)m=b[i`%w%m`()&col(`+&$)`)4&`)E$-1,0`)H& draw_line(x+12+o,y+12,x+m_S-`#3&`#.%)`#Q0`#E+`#U$`#Q0el`$S%2`%o$ing`#W%//2`#I%//2,15,`$k$`%7*`(0%grid(`+I(`)T$1,2`$}$`&^$`(3%*`$5$,m_Y0,`&H$*3`#s%)`#K,`#C$`#P+S*3`#Q$`#K$m_SHOWN=['']`$E&status(s):`&d$s!=`#H&[0`-l$ctext(20`$<$`#;&`(B)`#A+s`$V*`#L*=s`%R(ame(vs_cpu):
 b=[0]*9
 cls(`)6)`#Z*''
`&.)
 cur=4
 turn=1`&<*`,8):`$>$`+k,)
 while Tru`,v$w=`0n+`0T%w`)x$msg="It's a`)T$"if w==3`+&%'X wins!'`#9%1`#9&Calculator`#B$'if `%M%`#C&O`#Y&`$+$`&|(msg+' - ENTER'`*n$`$p%wkey()`1[%(OK,CLR`+b% pass`20*`%(%`$3&and`&)%`+#%`$1*'Thinking...`$0%pause(0.3`#1$m=`2I(
   b[m]=2`#f%`&Y&m`&Y& `(0)  continue`(($`$3&('X'if`$O&`&2(O')+' to move`$I$k=`%Q%
  old=cur`%9%k==LEFT`%:$cur%3>`2F$ cur-`$?$`-R$k==RIGH`#J+<`%c%cur+`#J-UP`#G(>`#E)-=3`#E+DOWN`#G(<6`#k*`#G,CLR`6>+`#<+OK`#_$b[cur`4@(`#1(`#N&`%~%3-`#2(`&l)cur`&n(if cur!=old`(x&`#G&old`#K$False`(j%`#d/`#>(m_RULES='Get three in a row (across, down or diagonal) before the other player. Play`#:$c`,1*or`+0$ to a friend.'
m_KEYS=['Arrows:`)K%,'`,-$: place your mark','CLEAR: quit`0i)main`20$`.J.c=home('GHTTT','TIC-TAC-TOE',`%f&,`$K%,('vs Calc','2`%1$ers','Back')`(%(<`(e%`)0)`0~&c==0)
`$R('''
H_main()
