# GHMENUB: part of GHMENU. Keep it next to GHMENU.
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
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
RED=(220,50,50)
H=210
def wkey():
 return wait_key()
_C=[None]
def col(c):
 if c!=_C[0]:
  _C[0]=c
  set_color(c[0],c[1],c[2])
COVER=[0]
def cls(c=BLACK):
 COVER[0]+=1
 col(c)
 fill_rect(-1,-1,321,211)
TY=6
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
MSG=[0,0]
I_BLACK=(0,0,0)
I_WHITE=(255,255,255)
I_INK=(20,20,20)
I_RED=(215,40,40)
I_GOLD=(230,180,40)
I_BG={'GHSOLI':(25,110,55),'GHBLOCKS':(40,30,90),'GHSUDOKU':I_WHITE,'GHANIM':I_WHITE,'GHFLAP':(110,195,240),'GHTTT':I_WHITE,'GHMERGE':(187,173,160),'GHPONG':(30,85,165),'GHBREAK':(30,70,170),'GHHANG':I_WHITE,'GHSPACE':(15,20,50),'GHFORTUN':(55,25,85),'GHNAMES':(20,60,70),'GHSTAR':(8,10,32),'GHMATCH':(30,90,80),'GHDRAGON':(50,130,60),'GHDETECT':(35,30,55),'GHSUPER':I_WHITE}
I_FONT={'0':'111101101101111','1':'010110010010111','2':'111001111100111','3':'111001111001111','4':'101101111001001','5':'111100111001111','6':'111100111101111','7':'111001001001001','8':'111101111101111','9':'111101111001111'}
def I_c_(c):
 col(c)
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
def I_fortune(x,y,c):
 I_box(x-19,y-10,13,20,(120,40,140))
 I_box(x+6,y-10,13,20,(120,40,140))
 I_box(x-8,y-15,16,25,(250,240,215))
 I_poly([x,x+2,x+6,x+3,x+4,x,x-4,x-3,x-6,x-2],[y-9,y-4,y-4,y-1,y+4,y+1,y+4,y-1,y-4,y-4],I_GOLD)
def I_names(x,y,c):
 I_box(x-14,y-9,28,18,I_WHITE)
 I_poly([x-14,x-21,x-14],[y-9,y,y+9],I_WHITE)
 I_box(x-17,y-1,3,3,(20,60,70))
 I_box(x-8,y-4,17,3,I_GOLD)
 I_box(x-8,y+2,11,3,I_INK)
def I_dragon(x,y,c):
 I_poly([x-2,x+10,x+4],[y-2,y-17,y+2],(240,190,40))
 I_box(x-10,y-2,20,11,(220,70,40))
 I_box(x-18,y-9,11,9,(220,70,40))
 I_box(x+9,y+3,9,3,(220,70,40))
 I_box(x-7,y+9,4,5,(220,70,40))
 I_box(x+4,y+9,4,5,(220,70,40))
 I_box(x-15,y-7,3,3,I_BLACK)
def I_detect(x,y,c):
 I_box(x-14,y+4,6,9,(120,90,60))
 I_box(x-6,y+8,6,9,(120,90,60))
 I_circ(x+2,y-4,11,(230,180,40))
 I_circ(x+2,y-4,8,(190,220,245))
 I_poly([x+9,x+13,x+19,x+15],[y+5,y+1,y+13,y+17],(120,80,40))
def I_match(x,y,c):
 I_box(x-19,y-12,17,24,(200,70,90))
 I_box(x-15,y-8,9,16,(225,120,135))
 I_box(x+2,y-12,17,24,(250,245,230))
 I_circ(x+8,y-2,3,I_RED)
 I_circ(x+13,y-2,3,I_RED)
 I_poly([x+4,x+17,x+10],[y-1,y-1,y+6],I_RED)
def I_about(x,y,c):
 I_c_(c)
 fill_circle(x,y-10,3)
 fill_rect(x-3,y-5,6,19)
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
S_SLOTS=3
def S_hname(s):
 return 'A'+str(s)+'H'
H_BAR_Y=34
H_BAR_H=22
H_BAR_GAP=27
def H_header():
 cls()
 ctext(22,'GAMEHUB',WHITE)
def H_app_pos(i):
 return(50+i%4*73,82+i//4*70)
def H_show_title(name,old=None):
 if old:
  ctext(203,old,BLACK)
 ctext(203,name,GOLD)
