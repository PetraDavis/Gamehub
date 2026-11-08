# GHTTT from GAMEHUB, on its own. Run it.
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
I_INK=(20,20,20)
I_BG={'GHTTT':I_WHITE}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_line(x1,y1,x2,y2,c,t=1):
 I_c_(c)
 for o in range(t):
  draw_line(int(x1)+o,int(y1),int(x2)+o,int(y2))
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
I_ICONS={'GHTTT':I_ttt}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_LINES=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
G_X0=85
G_Y0=28
G_S=50
G_INK=(20,20,20)
def G_winner(b):
 for a,c,d in G_LINES:
  if b[a]and b[a]==b[c]==b[d]:
   return b[a]
 if 0 not in b:
  return 3
 return 0
def G_cpu(b):
 for who in(2,1):
  for a,c,d in G_LINES:
   v=[b[a],b[c],b[d]]
   if v.count(who)==2 and v.count(0)==1:
    return(a,c,d)[v.index(0)]
 if b[4]==0:
  return 4
 free=[i for i in(0,2,6,8)if b[i]==0]
 if not free:
  free=[i for i in range(9)if b[i]==0]
 return random.choice(free)
def G_frame(i,c):
 x=G_X0+i%3*G_S+3
 y=G_Y0+i//3*G_S+3
 w=G_S-6
 rect(x+3,y,w-6,3,c)
 rect(x+3,y+w-3,w-6,3,c)
 rect(x,y+3,3,w-6,c)
 rect(x+w-3,y+3,3,w-6,c)
def G_cell(b,i,cur,full=True):
 x=G_X0+i%3*G_S
 y=G_Y0+i//3*G_S
 m=b[i]
 if not full:
  G_frame(i,GOLD if i==cur else WHITE)
 elif m==1:
  col(G_INK)
  a,e=(12,G_S-12)
  fill_poly([x+a-1,x+a+2,x+e+1,x+e-2],[y+a,y+a,y+e,y+e])
  fill_poly([x+e-2,x+e+1,x+a+2,x+a-1],[y+a,y+a,y+e,y+e])
 elif m==2:
  ring(x+G_S//2,y+G_S//2,15,G_INK,3,WHITE)
def G_grid():
 for i in(1,2):
  rect(G_X0+i*G_S-1,G_Y0,3,G_S*3,G_INK)
  rect(G_X0,G_Y0+i*G_S-1,G_S*3,3,G_INK)
G_SHOWN=['']
def G_status(s):
 o=G_SHOWN[0]
 if s==o:
  return
 if len(s)==len(o):
  d=[k for k in range(len(s))if s[k]!=o[k]]
  a,e=(d[0],d[-1]+1)
  x=160-len(s)*5+a*10
  text(x,203,o[a:e],WHITE)
  text(x,203,s[a:e],G_INK)
 else:
  ctext(203,o,WHITE)
  ctext(203,s,G_INK)
 G_SHOWN[0]=s
def G_game(vs_cpu):
 b=[0]*9
 cls(WHITE)
 G_SHOWN[0]=''
 G_grid()
 cur=4
 turn=1
 G_frame(cur,GOLD)
 while True:
  w=G_winner(b)
  if w:
   msg="It's a draw"if w==3 else 'X wins!'if w==1 else 'Calculator wins'if vs_cpu else 'O wins!'
   G_status(msg+' - ENTER')
   while wkey()not in(OK,CLR):
    pass
   return
  if vs_cpu and turn==2:
   G_status('Thinking...')
   pause(0.3)
   m=G_cpu(b)
   b[m]=2
   G_cell(b,m,cur)
   turn=1
   continue
  G_status(('X'if turn==1 else 'O')+' to move')
  k=wkey()
  old=cur
  if k==LEFT and cur%3>0:
   cur-=1
  elif k==RIGHT and cur%3<2:
   cur+=1
  elif k==UP and cur>2:
   cur-=3
  elif k==DOWN and cur<6:
   cur+=3
  elif k==CLR:
   return
  elif k==OK and b[cur]==0:
   b[cur]=turn
   turn=3-turn
   G_cell(b,cur,cur)
  if cur!=old:
   G_cell(b,old,cur,False)
   G_cell(b,cur,cur,False)
G_RULES='Get three in a row (across, down or diagonal) before the other player. Play the calculator or pass to a friend.'
G_KEYS=['Arrows: move','ENTER: place your mark','CLEAR: quit']
def G_main():
 while True:
  c=home('GHTTT','TIC-TAC-TOE',G_RULES,G_KEYS,('vs Calc','2 Players','Back'))
  if c<0:
   return
  G_game(c==0)
G_main()
RAN=True
