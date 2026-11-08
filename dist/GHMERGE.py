# GHMERGE from GAMEHUB, on its own. Run it.
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
I_BG={'GHMERGE':(187,173,160)}
I_FONT={'0':'111101101101111','1':'010110010010111','2':'111001111100111','3':'111001111001111','4':'101101111001001','5':'111100111001111','6':'111100111101111','7':'111001001001001','8':'111101111101111','9':'111101111001111'}
def I_c_(c):
 col(c)
def I_rr(x,y,w,h,r,c):
 I_c_(c)
 fill_rect(x+r-1,y-1,w-2*r+1,h+1)
 fill_rect(x-1,y+r-1,w+1,h-2*r+1)
 for cx in(x+r,x+w-r-1):
  for cy in(y+r,y+h-r-1):
   fill_circle(cx,cy,r)
def I_digits(x,y,s,c,p=2):
 I_c_(c)
 for i,ch in enumerate(s):
  bits=I_FONT[ch]
  for n in range(15):
   if bits[n]=='1':
    fill_rect(x+i*4*p+n%3*p-1,y+n//3*p-1,p+1,p+1)
def I_g2048(x,y,c):
 I_rr(x-20,y-12,41,28,4,(200,160,30))
 I_rr(x-20,y-14,41,28,4,(237,194,46))
 I_digits(x-14,y-5,'2048',I_WHITE)
I_ICONS={'GHMERGE':I_g2048}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_X0=90
G_Y0=26
G_S=36
G_BOARD=(187,173,160)
G_TC={0:(205,193,180),2:(230,225,215),4:(235,220,190),8:(240,170,110),16:(245,140,90),32:(245,110,85),64:(245,80,50),128:(235,205,110),256:(235,200,90),512:(235,195,70),1024:(235,190,50),2048:(235,185,30)}
def G_add(b):
 e=[i for i in range(16)if b[i]==0]
 if e:
  b[random.choice(e)]=4 if random.random()<0.1 else 2
def G_slide(row):
 r=[v for v in row if v]
 out=[]
 pts=0
 i=0
 while i<len(r):
  if i+1<len(r)and r[i]==r[i+1]:
   out.append(r[i]*2)
   pts+=r[i]*2
   i+=2
  else:
   out.append(r[i])
   i+=1
 return(out+[0]*(4-len(out)),pts)
def G_move(b,d):
 pts=0
 nb=b[:]
 for j in range(4):
  if d<2:
   idx=[j*4+i for i in range(4)]
  else:
   idx=[i*4+j for i in range(4)]
  if d==1 or d==3:
   idx.reverse()
  row,p=G_slide([b[i]for i in idx])
  pts+=p
  for n in range(4):
   nb[idx[n]]=row[n]
 return(nb,pts)
def G_draw(b,score,old=None,oscore=-1):
 faces=[]
 nums=[]
 for i in range(16):
  v=b[i]
  if old and old[i]==v:
   continue
  x=G_X0+i%4*G_S
  y=G_Y0+i//4*G_S
  c=G_TC.get(v,(235,180,20))
  faces.append((c,x+2,y+2,G_S-4,G_S-6))
  faces.append((dk(c,0.8),x+2,y+G_S-4,G_S-4,2))
  if v:
   s=str(v)
   if len(s)>3:
    s=s[:2]+'k'if v>=10000 else s
   nums.append(((60,55,50)if v<8 else WHITE,x+G_S//2-len(s)*5,y+24,s))
 faces.sort()
 for c,x,y,w,h in faces:
  rect(x,y,w,h,c)
 nums.sort()
 for c,x,y,s in nums:
  text(x,y,s,c)
 if score!=oscore:
  if oscore>=0:
   text(165,200,str(oscore),G_BOARD)
  text(165,200,str(score),WHITE)
def G_frame():
 cls(WHITE)
 rrect(12,34,64,64,8,dk((235,185,30),0.8))
 rrect(12,32,64,64,8,(235,185,30))
 text(24,70,'2048',WHITE)
 text(12,128,'Join',(120,110,100))
 text(12,146,'same',(120,110,100))
 text(12,164,'tiles!',(120,110,100))
 text(250,60,'Arrows',(120,110,100))
 text(250,78,'slide',(120,110,100))
 rrect(G_X0-4,G_Y0-4,G_S*4+8,G_S*4+8,8,G_BOARD)
 rrect(95,182,130,24,6,G_BOARD)
 text(105,200,'Score',WHITE)
def G_game():
 b=[0]*16
 G_add(b)
 G_add(b)
 score=0
 G_frame()
 G_draw(b,score)
 won=False
 while True:
  k=wkey()
  d={LEFT:0,RIGHT:1,UP:2,DOWN:3}.get(k,-1)
  if k==CLR:
   return
  if d<0:
   continue
  nb,p=G_move(b,d)
  if nb!=b:
   ob,osc=(b,score)
   b=nb
   score+=p
   G_add(b)
   G_draw(b,score,ob,osc)
   if 2048 in b and(not won):
    won=True
    message(['You made 2048!','Keep going?'],'Amazing!')
    G_frame()
    G_draw(b,score)
  stuck=True
  for dd in range(4):
   if G_move(b,dd)[0]!=b:
    stuck=False
  if stuck:
   message(['Final score '+str(score)],'No moves left')
   return
G_RULES='Slide the tiles. Two tiles with the same number join into one. Try to make 2048!'
G_KEYS=['Arrows: slide all tiles','CLEAR: quit']
def G_main():
 while True:
  c=home('GHMERGE','2048',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
