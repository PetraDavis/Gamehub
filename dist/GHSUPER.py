# GHSUPER from GAMEHUB, on its own. Run it.
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
I_RED=(215,40,40)
I_BG={'GHSUPER':I_WHITE}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_line(x1,y1,x2,y2,c,t=1):
 I_c_(c)
 for o in range(t):
  draw_line(int(x1)+o,int(y1),int(x2)+o,int(y2))
def I_superttt(x,y,c):
 for i in(-1,1):
  I_box(x+i*7-1,y-20,3,41,I_INK)
  I_box(x-20,y+i*7-1,41,3,I_INK)
 for i in(-1,1):
  I_box(x+i*2,y-5,1,11,(150,150,160))
  I_box(x-5,y+i*2,11,1,(150,150,160))
 I_line(x-17,y-17,x-11,y-11,I_RED,2)
 I_line(x-11,y-17,x-17,y-11,I_RED,2)
 I_c_((40,90,210))
 fill_circle(x+13,y+13,4)
 I_c_(I_WHITE)
 fill_circle(x+13,y+13,2)
I_ICONS={'GHSUPER':I_superttt}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_LINES=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
G_X0=74
G_Y0=10
G_C=19
G_B=G_C*3
G_INK=(20,20,20)
G_LINE=(190,190,200)
G_XC=(215,40,40)
G_OC=(40,90,210)
G_TINT=((235,235,235),(250,215,215),(215,225,250))
def G_winner(b):
 for a,c,d in G_LINES:
  if b[a]in(1,2)and b[a]==b[c]==b[d]:
   return b[a]
 if 0 not in b:
  return 3
 return 0
def G_pos(g,s):
 return(G_X0+g%3*G_B+s%3*G_C,G_Y0+g//3*G_B+s//3*G_C)
def G_grid():
 for k in range(1,9):
  if k%3:
   rect(G_X0+k*G_C,G_Y0,1,G_B*3,G_LINE)
   rect(G_X0,G_Y0+k*G_C,G_B*3,1,G_LINE)
 for k in range(4):
  rect(G_X0+k*G_B-1,G_Y0-1,3,G_B*3+3,G_INK)
  rect(G_X0-1,G_Y0+k*G_B-1,G_B*3+3,3,G_INK)
def G_box_frame(g,c):
 if g<0:
  x,y,w=(G_X0,G_Y0,G_B*3)
 else:
  x,y,w=(G_X0+g%3*G_B,G_Y0+g//3*G_B,G_B)
 rect(x-1,y-1,w+3,3,c)
 rect(x-1,y+w-1,w+3,3,c)
 rect(x-1,y+2,3,w-3,c)
 rect(x+w-1,y+2,3,w-3,c)
def G_cursor(g,s,c):
 x,y=G_pos(g,s)
 rect(x+2,y+2,16,2,c)
 rect(x+2,y+16,16,2,c)
 rect(x+2,y+4,2,12,c)
 rect(x+16,y+4,2,12,c)
def G_mark(x,y,w,p):
 a=w//4+(w==G_C)
 e=w-a
 t=max(1,w//12)
 if p==1:
  col(G_XC)
  fill_poly([x+a-t,x+a+t,x+e+t,x+e-t],[y+a,y+a,y+e,y+e])
  fill_poly([x+e-t,x+e+t,x+a+t,x+a-t],[y+a,y+a,y+e,y+e])
 else:
  ring(x+w//2,y+w//2,w*3//10,G_OC,t+1,WHITE if w==G_C else G_TINT[2])
def G_take(g,p):
 x,y=(G_X0+g%3*G_B,G_Y0+g//3*G_B)
 rect(x+2,y+2,G_B-3,G_B-3,G_TINT[0 if p==3 else p])
 if p<3:
  G_mark(x+2,y+2,G_B-3,p)
G_SHOWN=['']
def G_status(s):
 o=G_SHOWN[0]
 if s==o:
  return
 ctext(196,o,WHITE)
 ctext(196,s,G_INK)
 G_SHOWN[0]=s
def G_game():
 cells=[[0]*9 for _ in range(9)]
 big=[0]*9
 cls(WHITE)
 G_SHOWN[0]=''
 G_grid()
 turn=1
 need=-1
 g,s=(4,4)
 G_box_frame(need,GOLD)
 G_cursor(g,s,GOLD)
 while True:
  w=G_winner(big)
  if w==3 or(not w and all((big[k]or 0 not in cells[k]for k in range(9)))):
   w=3
  if w:
   G_box_frame(need,G_INK)
   if not big[g]:
    G_cursor(g,s,WHITE)
   G_status(("It's a draw"if w==3 else('X'if w==1 else 'O')+' wins!')+' - ENTER')
   while wkey()not in(OK,CLR):
    pass
   return
  who='X'if turn==1 else 'O'
  G_status(who+(': go anywhere'if need<0 else ': play in the gold box'))
  k=wkey()
  og,os_=(g,s)
  gx,gy=(g%3*3+s%3,g//3*3+s//3)
  if k==CLR:
   return
  if k in(LEFT,RIGHT,UP,DOWN):
   dx=(k==RIGHT)-(k==LEFT)
   dy=(k==DOWN)-(k==UP)
   nx,ny=(gx+dx,gy+dy)
   if need>=0:
    lo_x,lo_y=(need%3*3,need//3*3)
    ok=lo_x<=nx<lo_x+3 and lo_y<=ny<lo_y+3
   else:
    while 0<=nx<9 and 0<=ny<9 and big[ny//3*3+nx//3]:
     nx,ny=(nx+3*dx,ny+3*dy)
    ok=0<=nx<9 and 0<=ny<9
   if ok:
    g,s=(ny//3*3+nx//3,ny%3*3+nx%3)
  elif k==OK and(not big[g])and(cells[g][s]==0):
   cells[g][s]=turn
   G_cursor(g,s,WHITE)
   x,y=G_pos(g,s)
   G_mark(x,y,G_C,turn)
   r=G_winner(cells[g])
   if r:
    big[g]=r
    G_take(g,r)
   old=need
   need=-1 if big[s]else s
   turn=3-turn
   if need!=old:
    G_box_frame(old,G_INK)
    G_box_frame(need,GOLD)
   if need>=0:
    g=need
   elif big[g]:
    g=[k for k in range(9)if not big[k]][0]if 0 in big else g
   if cells[g][s]:
    s=[k for k in range(9)if cells[g][k]==0][0]if 0 in cells[g]else s
   G_cursor(g,s,GOLD)
   continue
  if(g,s)!=(og,os_):
   G_cursor(og,os_,WHITE)
   G_cursor(g,s,GOLD)
G_RULES='Where you play in a small board sends your friend to that big box. Win small boards to take boxes. Get 3 in a row!'
G_KEYS=['Arrows: move  ENTER: place','CLEAR: quit']
def G_main():
 while True:
  c=home('GHSUPER','SUPER TIC-TAC-TOE',G_RULES,G_KEYS,('2 Players','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
