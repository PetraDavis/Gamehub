# GHSUDOKU from GAMEHUB, on its own. Run it.
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
NUMS={102:0,92:1,93:2,94:3,82:4,83:5,84:6,72:7,73:8,74:9}
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
GREY=(110,110,110)
RED=(220,50,50)
H=210
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
I_BG={'GHSUDOKU':I_WHITE}
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
I_ICONS={'GHSUDOKU':I_sudoku}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_S=20
G_X0=20
G_Y0=15
G_INK=(20,20,20)
G_PEN=(40,90,200)
def G_make(holes):
 base=3
 r=list(range(3))
 rows=[g*3+i for g in sample(r,3)for i in sample(r,3)]
 cols=[g*3+i for g in sample(r,3)for i in sample(r,3)]
 nums=sample(range(1,10),9)
 sol=[nums[(base*(rr%base)+rr//base+cc)%9]for rr in rows for cc in cols]
 puz=sol[:]
 for i in sample(range(81),holes):
  puz[i]=0
 return puz
def G_valid(b):
 for i in range(9):
  row=set(b[i*9:i*9+9])
  colm=set(b[i::9])
  bx=i%3*3+i//3*27
  box=set((b[bx+o]for o in(0,1,2,9,10,11,18,19,20)))
  for s in(row,colm,box):
   if s!=set(range(1,10)):
    return False
 return True
def G_clash(b,i):
 v=b[i]
 if not v:
  return False
 r=i//9
 c=i%9
 for j in range(81):
  if j!=i and b[j]==v:
   if j//9==r or j%9==c or(j//27==i//27 and j%9//3==c//3):
    return True
 return False
G_SHOWN={}
def G_cell(b,fixed,i,cur):
 x=G_X0+i%9*G_S
 y=G_Y0+i//9*G_S
 bg=G_FIX if fixed[i]else WHITE
 v=b[i]
 c=(G_INK if fixed[i]else RED if G_clash(b,i)else G_PEN)if v else None
 on=i==cur
 old=G_SHOWN.get(i)
 if old is None or old[0]!=v:
  rect(x+1,y+1,G_S-2,G_S-2,bg)
  old=None
 if v and(old is None or old[1]!=c):
  text(x+5,y+16,str(v),c)
 if old is None or old[2]!=on:
  k=GOLD if on else bg
  rect(x+1,y+1,G_S-2,2,k)
  rect(x+1,y+G_S-3,G_S-2,2,k)
  rect(x+1,y+3,2,G_S-6,k)
  rect(x+G_S-3,y+3,2,G_S-6,k)
 G_SHOWN[i]=(v,c,on)
G_FIX=(236,238,246)
def G_first(b,fixed,cur):
 for r in range(9):
  c=0
  while c<9:
   if fixed[r*9+c]:
    e=c
    while e<9 and fixed[r*9+e]:
     e+=1
    rect(G_X0+c*G_S,G_Y0+r*G_S,(e-c)*G_S,G_S,G_FIX)
    c=e
   else:
    c+=1
 G_grid()
 for r in range(9):
  row=''.join([(str(b[r*9+c])if b[r*9+c]else ' ')+' 'for c in range(9)])
  if row.strip():
   text(G_X0+5,G_Y0+r*G_S+16,row.rstrip(),G_INK)
 for i in range(81):
  v=b[i]
  G_SHOWN[i]=(v,(G_INK if fixed[i]else RED if G_clash(b,i)else G_PEN)if v else None,False)
 G_cell(b,fixed,cur,cur)
def G_grid():
 for i in range(10):
  c=G_INK if i%3==0 else(150,150,150)
  t=2 if i%3==0 else 1
  if t==2:
   rect(G_X0+i*G_S-1,G_Y0-1,2,G_S*9+2,c)
   rect(G_X0-1,G_Y0+i*G_S-1,G_S*9+2,2,c)
  else:
   col(c)
   draw_line(G_X0+i*G_S,G_Y0,G_X0+i*G_S,G_Y0+G_S*9)
   draw_line(G_X0,G_Y0+i*G_S,G_X0+G_S*9,G_Y0+i*G_S)
def G_game(holes):
 b=G_make(holes)
 fixed=[v!=0 for v in b]
 cls(WHITE)
 rbox(208,12,106,30,8,G_PEN,2,(225,235,252))
 text(222,33,'SUDOKU',G_PEN)
 text(214,70,'0-9 type',GREY)
 text(214,90,'ENTER +1',GREY)
 text(214,110,'DEL erase',GREY)
 text(214,130,'CLEAR quit',GREY)
 G_SHOWN.clear()
 cur=0
 while fixed[cur]:
  cur+=1
 G_first(b,fixed,cur)
 while True:
  k=wkey()
  old=cur
  if k==LEFT and cur%9:
   cur-=1
  elif k==RIGHT and cur%9<8:
   cur+=1
  elif k==UP and cur>8:
   cur-=9
  elif k==DOWN and cur<72:
   cur+=9
  elif k==CLR:
   return
  elif not fixed[cur]:
   v=-1
   if k in NUMS:
    v=NUMS[k]
   elif k==OK:
    v=b[cur]%9+1
   elif k==DEL:
    v=0
   if v>=0:
    b[cur]=v
    for i in range(81):
     if not fixed[i]:
      G_cell(b,fixed,i,cur)
    if 0 not in b and G_valid(b):
     message(['Every row, column and','box is complete.'],'Solved!')
     return
  G_cell(b,fixed,old,cur)
  G_cell(b,fixed,cur,cur)
G_RULES='Fill the grid so every row, column and 3x3 box has the numbers 1 to 9 once. Red numbers clash.'
G_KEYS=['Arrows: move','0-9: type a number','ENTER: count up  DEL: erase','CLEAR: quit']
def G_main():
 while True:
  c=home('GHSUDOKU','SUDOKU',G_RULES,G_KEYS,('Easy','Medium','Hard','Back'))
  if c<0:
   return
  G_game((36,46,54)[c])
G_main()
RAN=True
