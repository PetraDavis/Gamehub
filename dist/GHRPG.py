# GHRPG from GAMEHUB, on its own. Run it.
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
DARK=(40,40,40)
RED=(220,50,50)
GREEN=(50,190,80)
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
I_GOLD=(230,180,40)
I_BG={}
def I_c_(c):
 set_color(c[0],c[1],c[2])
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_circ(x,y,r,c):
 I_c_(c)
 fill_circle(int(x),int(y),int(r))
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
I_ICONS={'GHRPG':I_rpg}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_T=20
G_MAPS=(['TTTTTTTTTTTTTTTT','T......TT......T','T.HH...........T','T.HH....C......T','T..............>','T....~~~.......>','T....~~~...TT..T','T..........TT..T','T..............T','TTTTTTTTTTTTTTTT'],['TTTTTTTTTTTTTTTT','T..T....TT...T.T','T..T.C..TT...T.T','<......T.....T.T','<..TT..T..T....>','T..TT.....T....>','T.....T...TTT..T','T.TT..T.C......T','T.TT..T........T','TTTTTTTTTTTTTTTT'],['################','#::::#:::::::::#','#::C:#:###:###:#','<::::#:#:::#:::#','<::::::#:B:#:::#','#::#####:::#:#:#','#::::::::::::#:#','#:####:#####:#:#','#:::::::C::::::#','################'])
G_NAMES=('Meadow','Whisper Woods','Hollow Cave')
G_FOES=((),(('Slime',12,4,1,6,(80,200,90)),('Bat',10,5,0,7,(120,90,160))),(('Bone Rat',18,7,2,12,(220,220,200)),('Cave Eye',22,8,3,15,(200,60,60))))
G_BOSS=('Hollow King',70,12,4,0,(110,80,180))
G_GRASS=(40,110,50)
G_STONE=(60,55,50)
G_BASE={'.':G_GRASS,'>':G_GRASS,'<':G_GRASS,' ':G_GRASS,'T':G_GRASS,'H':G_GRASS,'~':(40,90,190),'#':(30,28,35),':':G_STONE,'B':G_STONE}
G_LEAF=(25,85,35)
G_BARK=(90,60,30)
G_LINE=(45,40,38)
G_WOOD=(120,75,35)
def G_shapes(m,x,y,ch,out):
 px=x*G_T
 py=20+y*G_T
 if ch in '.>< ':
  h=(x*7+y*13)%5
  if h==2:
   out.append((0,(240,220,90),0,(px+14,py+4,2,2)))
  elif h==4:
   out.append((0,(230,120,160),0,(px+4,py+15,2,2)))
 elif ch=='T':
  out.append((0,G_BARK,0,(px+8,py+14,4,6)))
  out.append((1,G_LEAF,1,(px+10,py+8,8)))
 elif ch=='~':
  o=(x*5+y*3)%8
  out.append((0,(110,160,235),0,(px+o,py+8,6,1)))
 elif ch=='H':
  out.append((0,(200,170,120),0,(px+2,py+9,16,11)))
  out.append((1,(170,50,40),2,([px,px+10,px+20],[py+9,py,py+9])))
  out.append((2,G_BARK,0,(px+8,py+13,4,7)))
  out.append((2,(250,230,140),0,(px+4,py+11,3,3)))
  out.append((2,(250,230,140),0,(px+13,py+11,3,3)))
 elif ch=='C'or ch=='c':
  if m==2:
   out.append((0,G_LINE,0,(px,py,G_T,1)))
  if ch=='C':
   out.append((0,(60,40,20),0,(px+3,py+6,14,11)))
   out.append((1,(160,110,40),0,(px+4,py+7,12,9)))
   out.append((2,GOLD,0,(px+4,py+10,12,2)))
  else:
   out.append((0,(100,70,30),0,(px+4,py+10,12,6)))
 elif ch=='#':
  for yy in(6,13):
   out.append((0,(50,47,58),0,(px,py+yy,G_T,1)))
 elif ch==':':
  out.append((0,G_LINE,0,(px,py,G_T,1)))
 elif ch=='B':
  out.append((0,G_LINE,0,(px,py,G_T,1)))
  out.append((1,(110,80,180),1,(px+10,py+11,8)))
  out.append((2,GOLD,2,([px+3,px+6,px+10,px+14,px+17],[py+4,py-1,py+3,py-1,py+4])))
  out.append((3,RED,0,(px+5,py+8,3,3)))
  out.append((3,RED,0,(px+12,py+8,3,3)))
def G_base(m,ch):
 if ch in 'Cc':
  return G_GRASS if m<2 else G_STONE
 return G_BASE.get(ch,G_GRASS)
def G_hero(x,y,out):
 px=x*G_T
 py=20+y*G_T
 out.append((5,(240,200,160),1,(px+10,py+5,4)))
 out.append((6,G_WOOD,0,(px+6,py+1,8,3)))
 out.append((6,BLACK,0,(px+8,py+5,1,1)))
 out.append((6,BLACK,0,(px+11,py+5,1,1)))
 out.append((6,(60,120,230),0,(px+6,py+9,8,7)))
 out.append((6,(60,40,30),0,(px+6,py+16,3,4)))
 out.append((6,(60,40,30),0,(px+11,py+16,3,4)))
 out.append((6,(210,215,225),0,(px+15,py+4,2,8)))
 out.append((6,GOLD,0,(px+14,py+12,4,2)))
def G_paint(ops):
 ops.sort(key=lambda o:(o[0],o[1],o[2],o[3][1]if o[2]==0 else 0,o[3][0]))
 last=None
 for layer,c,kind,a in ops:
  if kind==0:
   if last and last[0]==(layer,c)and(last[2]==a[1])and(last[4]==a[3])and(last[1]+last[3]==a[0]):
    last[3]+=a[2]
    continue
   if last:
    rect(last[1],last[2],last[3],last[4],last[0][1])
   last=[(layer,c),a[0],a[1],a[2],a[3]]
   continue
  if last:
   rect(last[1],last[2],last[3],last[4],last[0][1])
   last=None
  if kind==1:
   circ(a[0],a[1],a[2],c)
  else:
   col(c)
   fill_poly(a[0],a[1])
 if last:
  rect(last[1],last[2],last[3],last[4],last[0][1])
def G_cells(g,todo,with_hero):
 mp=g.maps[g.m]
 ops=[]
 rows={}
 for x,y in todo:
  rows.setdefault(y,[]).append(x)
 for y in rows:
  xs=sorted(rows[y])
  i=0
  while i<len(xs):
   c=G_base(g.m,mp[y][xs[i]])
   j=i+1
   while j<len(xs)and xs[j]==xs[j-1]+1 and(G_base(g.m,mp[y][xs[j]])==c):
    j+=1
   ops.append((-1,c,0,(xs[i]*G_T,20+y*G_T,(j-i)*G_T,G_T)))
   i=j
 for x,y in todo:
  G_shapes(g.m,x,y,mp[y][x],ops)
 if with_hero:
  G_hero(g.x,g.y,ops)
 G_paint(ops)
def G_draw_map(g,after_msg=False):
 r0,r1=(0,10)
 if after_msg:
  r0=max(0,(MSG[0]-20)//G_T)
  r1=min(10,(MSG[0]+MSG[1]-20)//G_T+1)
 else:
  G_HUD[0]=None
 G_cells(g,[(x,y)for y in range(r0,r1)for x in range(16)],r0<=g.y<r1)
 G_hud(g)
G_HUD=[None]
def G_hud(g):
 t=(G_NAMES[g.m][:13],'HP'+str(g.hp)+'/'+str(g.mhp),'LV'+str(g.lv)+' P'+str(g.pot))
 if t==G_HUD[0]:
  return
 if G_HUD[0]is None:
  rect(0,0,320,20,BLACK)
  old=('','','')
 else:
  old=G_HUD[0]
 for i,x,c in((0,4,GOLD),(1,140,WHITE),(2,240,WHITE)):
  if t[i]!=old[i]:
   text(x,15,old[i],BLACK)
   text(x,15,t[i],c)
 G_HUD[0]=t
class G_Game:
 pass
def G_bar(x,y,w,v,mx,c):
 f=max(0,min(w,int(w*v/mx)))if v>0 else 0
 if v>0:
  f=max(2,f)
 rect(x,y,f,6,c)
 rect(x+f,y,w-f,6,DARK)
def G_foe_art(f):
 c=f[5]
 n=f[0]
 if n=='Slime':
  circ(220,95,30,c)
  rect(190,95,60,30,c)
 elif n=='Bat':
  col(c)
  fill_poly([170,220,270,220],[80,100,80,120])
  circ(220,100,12,c)
 elif n=='Bone Rat':
  circ(220,100,22,c)
  circ(245,85,10,c)
  rect(170,110,30,3,c)
 elif n=='Cave Eye':
  circ(220,95,30,c)
  circ(220,95,14,WHITE)
  circ(220,95,6,BLACK)
 else:
  rect(195,70,50,60,c)
  circ(220,60,18,c)
  col(GOLD)
  fill_poly([200,205,212,220,228,235,240],[45,30,42,28,42,30,45])
  rect(208,55,5,5,RED)
  rect(227,55,5,5,RED)
 if n=='Slime':
  circ(210,92,3,BLACK)
  circ(230,92,3,BLACK)
 elif n=='Bone Rat':
  circ(245,83,2,BLACK)
def G_battle(g,f):
 name,fhp,fat,fdf,xp=(f[0],f[1],f[2],f[3],f[4])
 mx=fhp
 cls()
 rbox(150,30,140,120,10,f[5],2,BLACK)
 G_foe_art(f)
 ctext(26,name+' appears!',GOLD)
 opts=['Attack','Potion','Run']
 sel=0
 log=''
 text(12,56,'You',WHITE)
 text(12,86,name[:12],f[5])
 for i in range(3):
  c=GOLD if i==sel else WHITE
  rbox(10+i*102,154,96,24,8,c)
  text(58+i*102-len(opts[i])*5,172,opts[i],c)
 was=None
 while True:
  now=(g.hp,fhp,sel,log)
  if was is None or was[0]!=now[0]:
   G_bar(12,62,120,g.hp,g.mhp,GREEN)
  if was is None or was[1]!=now[1]:
   G_bar(12,92,120,fhp,mx,RED)
  if was is not None and was[2]!=sel:
   for i in(was[2],sel):
    c=GOLD if i==sel else WHITE
    edge(10+i*102,154,96,24,8,c)
    text(58+i*102-len(opts[i])*5,172,opts[i],c)
  if was is None or was[3]!=log:
   if was is not None:
    text(10,202,was[3][:31],BLACK)
   text(10,202,log[:31],GREY)
  was=now
  k=wkey()
  if k==LEFT:
   sel=(sel-1)%3
   continue
  if k==RIGHT:
   sel=(sel+1)%3
   continue
  if k!=OK:
   continue
  if sel==0:
   d=max(1,g.atk+random.randint(0,3)-fdf)
   fhp-=d
   log='You hit for '+str(d)+'.'
  elif sel==1:
   if g.pot==0:
    log='No potions left.'
    continue
   g.pot-=1
   g.hp=min(g.mhp,g.hp+25)
   log='You feel better.'
  elif f is G_BOSS:
   log="You can't run from him!"
  elif random.random()<0.6:
   return True
  else:
   log="Couldn't get away."
  if fhp<=0:
   g.xp+=xp
   msg=['You won. +'+str(xp)+' XP']
   while g.xp>=g.lv*12:
    g.xp-=g.lv*12
    g.lv+=1
    g.mhp+=8
    g.atk+=2
    g.dfn+=1
    g.hp=g.mhp
    msg.append('Level up! LV '+str(g.lv))
   message(msg,name+' defeated')
   return True
  d=max(1,fat+random.randint(0,3)-g.dfn)
  g.hp-=d
  log=log+' It hits '+str(d)+'.'
  if g.hp<=0:
   message(['You fainted...'],'Game over')
   return False
def G_play():
 g=G_Game()
 g.maps=[[list(r)for r in mp]for mp in G_MAPS]
 g.m=0
 g.x,g.y=(4,4)
 g.hp=g.mhp=30
 g.atk=6
 g.dfn=1
 g.lv=1
 g.xp=0
 g.pot=1
 steps=0
 cls()
 G_draw_map(g)
 message(['The Hollow King took',"the village's light.",'Bring it back!'],'TINY QUEST')
 G_draw_map(g,True)
 while True:
  k=wkey()
  if k==CLR:
   if message(['ENTER: quit adventure','CLEAR: keep going'],'Quit?')==OK:
    return
   G_draw_map(g,True)
   continue
  dx,dy={LEFT:(-1,0),RIGHT:(1,0),UP:(0,-1),DOWN:(0,1)}.get(k,(0,0))
  if dx==0 and dy==0:
   continue
  nx,ny=(g.x+dx,g.y+dy)
  mp=g.maps[g.m]
  if nx>=16 or nx<0:
   g.m+=1 if nx>=16 else-1
   g.x=0 if nx>=16 else 15
   G_draw_map(g)
   continue
  ch=mp[ny][nx]
  if ch in 'T~#':
   continue
  if ch=='H':
   g.hp=g.mhp
   G_hud(g)
   message(['You rest by the fire.','HP restored.'],'Cottage')
   G_draw_map(g,True)
   continue
  if ch=='C':
   mp[ny][nx]='c'
   g.pot+=1
   message(['You found a potion!'],'Chest')
   G_draw_map(g,True)
   continue
  if ch=='B':
   if G_battle(g,G_BOSS):
    if g.hp>0:
     cls()
     message(['The light returns to','the village. You did it!'],'THE END')
    return
   return
  ox,oy=(g.x,g.y)
  g.x,g.y=(nx,ny)
  G_cells(g,[(ox,oy)],True)
  steps+=1
  if G_FOES[g.m]and steps>6 and(random.random()<0.12):
   steps=0
   if not G_battle(g,random.choice(G_FOES[g.m])):
    return
   G_draw_map(g)
G_RULES='Walk the meadow, woods and cave. Rest at the cottage, open chests for potions, and defeat the Hollow King.'
G_KEYS=['Arrows: walk','Fights: Left/Right + ENTER','CLEAR: quit']
def G_main():
 while True:
  c=home('GHRPG','TINY QUEST',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_play()
G_main()
RAN=True
