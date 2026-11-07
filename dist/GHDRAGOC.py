# GHDRAGOC: part of GHDRAGOP. Keep it next to GHDRAGOP.
from ti_draw import*
from ti_system import*
import time
import random
UP=25
DOWN=34
LEFT=24
RIGHT=26
OK=105
CLR=45
SECOND=21
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
GREY=(110,110,110)
DARK=(40,40,40)
RED=(220,50,50)
GREEN=(50,190,80)
YELLOW=(240,220,60)
H=210
def shuffle(a):
 for i in range(len(a)-1,0,-1):
  j=random.randint(0,i)
  a[i],a[j]=(a[j],a[i])
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
def _corners(x,y,w,h,r,t):
 return((x,y,w,t),(x,y+h-t,w,t),(x,y+t,t,h-2*t),(x+w-t,y+t,t,h-2*t))
def rbox(x,y,w,h,r,c,t=2,inner=BLACK,fill=True):
 edge(x,y,w,h,r,c,t)
 if fill:
  rect(x+t,y+t,w-2*t,h-2*t,inner)
def edge(x,y,w,h,r,c,t=2,inner=BLACK):
 col(c)
 for bx,by,bw,bh in _corners(x,y,w,h,r,t):
  if bw>0 and bh>0:
   fr(bx,by,bw,bh)
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
G_T=20
G_MAPS=(['TTTTTTTTTTTTT~~~','T.....""".....~~','T.H...""""...~~~','T.....""".T...~~','T..........E.~~~','T....TT.......~~','T.""".TT......~~','T.""".........~~','TTTTTTTTTTTTTT~~'],['~^^^^^^^^^^^^^^^','~...""""..LLL..^','~..^"""..LLELL.^','~.....^...LLL...','~...............','~...^^...."""...','~..LL....."""..^','~.....^^.......^','~^^^^^^^^^^^^^^^'],['^^^^^^^^^^^^^^^^','...""".....^E^^^','...........^^^^^','......~~~~......','....~~~~B~~~....','.....~~~~~......','.."""...........','..""".....^^....','^^^^^^^^^^^^^^^^'])
G_LANDS=('Green Valley','Fire Mountain','Frost Peaks')
G_GROUND=((50,130,60),(85,65,55),(215,225,240))
G_TALL=((35,100,45),(120,90,60),(170,190,220))
G_WATER=(40,90,190)
G_LAVA=(230,90,20)
G_ROCK=(110,105,115)
G_LEAF=(25,85,35)
G_BARK=(90,60,30)
G_ENAME=('fire','water','plant','star')
G_RARE=('Common','Uncommon','Rare','Epic','Legendary')
G_RCOL=(WHITE,(120,220,120),(90,160,255),(200,110,240),GOLD)
G_DT=(('Ember',0,0,(220,70,40)),('Cinder',0,0,(235,140,40)),('Puddle',1,0,(60,130,230)),('Brook',1,0,(40,170,170)),('Sprig',2,0,(70,170,70)),('Mossy',2,0,(130,150,60)),('Pebble',2,0,(150,140,120)),('Magma',0,1,(170,40,30)),('Frost',1,1,(160,210,245)),('Thorn',2,1,(30,110,60)),('Storm',1,1,(120,100,200)),('Smoky',0,1,(90,90,100)),('Sunscale',0,2,(240,190,40)),('Coral',1,2,(240,120,150)),('Jade',2,2,(60,200,150)),('Blossom',2,2,(250,160,210)),('Phoenix',0,3,(255,90,60)),('Leviathan',1,3,(30,60,160)),('Oakheart',2,3,(110,80,40)),('Starwing',3,4,(250,240,180)))
G_PAINT=((220,70,40),(60,130,230),(70,170,70),(240,190,40),(200,110,240),(240,120,150),(40,40,50),(240,240,245))
G_SHOP=(('Paint it',20,0),('Saddle',15,1),('Scarf',25,2),('Crown',60,4))
G_FOES=((('Goblin',14,4,6,(110,160,60),3),('Bog Toad',16,4,7,(60,120,160),1)),(('Lava Imp',26,7,12,(240,120,30),0),('Rock Troll',32,7,14,(120,110,90),2)),(('Ice Wraith',34,9,16,(150,200,240),1),('Snow Yeti',42,9,18,(235,235,245),3)))
G_BOSS=('Shadow Wyrm',110,12,0,(90,50,140),3)
def G_beats(a,b):
 return a==3 and b!=3 or(a<3 and b==(a+2)%3)
def G_egg_type(m):
 r=random.randint(0,99)+m*6
 rar=4 if r>=99 else 3 if r>=92 else 2 if r>=78 else 1 if r>=52 else 0
 return random.choice([i for i in range(len(G_DT))if G_DT[i][2]==rar])
G_EGGS={}
def G_el(d):
 return G_DT[d[1]][1]
G_HUD=[None]
class G_Game:
 pass
def G_go_home(g):
 g.m,g.x,g.y=(0,3,2)
 G_rest(g)
def G_rest(g):
 g.hp=g.mhp
 g.ride=None
 for d in g.pen:
  d[3]=d[4]
def G_new_quest(g):
 k=random.randint(0,2)
 if k==0:
  n=random.randint(2,4)
  land=random.randint(0,g.seen)
  nm=random.choice(G_FOES[land])[0]
  return[0,nm,n,0,8*n+6*land,'Beat '+str(n)+' '+nm+'s']
 if k==1:
  return[1,None,1,0,20,'Hatch an egg']
 land=random.randint(0,g.seen)
 n=random.randint(3,5)
 return[2,land,n,0,7*n+6*land,str(n)+' wins: '+G_LANDS[land]]
def G_stats(d):
 t=G_DT[d[1]]
 message([t[0]+' ('+G_RARE[t[2]]+')','Element: '+G_ENAME[t[1]],'Level '+str(d[2])+'  HP '+str(d[3])+'/'+str(d[4]),'Attack '+str(5+2*d[2]+2*t[2])],d[0])
