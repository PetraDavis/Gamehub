# GHDRAGOB: part of GHDRAGOP. Keep it next to GHDRAGOP.
from GHDRAGOC import*
from GHDRAGOC import _C
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
def cls(c=BLACK):
 COVER[0]+=1
 col(c)
 fill_rect(-1,-1,321,211)
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
G_MAPS=(['TTTTTTTTTTTTT~~~','T.....""".....~~','T.H...""""...~~~','T.....""".T...~~','T..........E.~~~','T....TT.......~~','T.""".TT......~~','T.""".........~~','TTTTTTTTTTTTTT~~'],['~^^^^^^^^^^^^^^^','~...""""..LLL..^','~..^"""..LLELL.^','~.....^...LLL...','~...............','~...^^...."""...','~..LL....."""..^','~.....^^.......^','~^^^^^^^^^^^^^^^'],['^^^^^^^^^^^^^^^^','...""".....^E^^^','...........^^^^^','......~~~~......','....~~~~B~~~....','.....~~~~~......','.."""...........','..""".....^^....','^^^^^^^^^^^^^^^^'])
G_GROUND=((50,130,60),(85,65,55),(215,225,240))
G_TALL=((35,100,45),(120,90,60),(170,190,220))
G_DT=list(zip(('Pyrrak','Smoldedrake','Aquawyrm','Gillwing','Fernling','Lichenwing','Stonewyrm','Volcanox','Ashveil','Glacius','Tempestra','Thornwyrm','Dawnwing','Pearlhorn','Jadewyrm','Petalwyrm','Blazequill','Abyssar','Rootwyrm','Lumora','Quantum'),b'\x00\x00\x01\x01\x02\x02\x02\x00\x00\x01\x01\x02\x00\x01\x02\x02\x00\x01\x02\x03\x03',b'\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x02\x02\x02\x02\x03\x03\x03\x04\x05',G_cl(b'\xdcF(\xeb\x8c(<\x82\xe6(\xaa\xaaF\xaaF\x82\x96<\x96\x8cx\xaa(\x1eKKU\xa0\xd2\xf5xd\xc8\x1en<\xf0\xbe(\xf0x\x96<\xc8\x96\xfa\xa0\xd2\xffZ<\x1e<\xa0nP(\x19\x19#\x19\x1eP')))
G_NAMES=('Blaze','Splash','Fern','Spark','Misty','Clover','Ziggy','Nova','Pebble','Rocket','Biscuit','Luna','Comet','Pip','Maple','Echo','Sunny','Bolt','Willow','Ash','Ripple','Twig','Ember','Taro')
G_BOSS=('Shadow Wyrm',110,12,0,(90,50,140),3)
def G_egg_type(m):
 r=random.randint(0,99)+m*6
 rar=4 if r>=99 else 3 if r>=92 else 2 if r>=78 else 1 if r>=52 else 0
 return random.choice([i for i in range(20)if G_DT[i][2]==rar])
def G_base(m,ch):
 if ch=='~':
  return G_WATER
 if ch=='L':
  return G_LAVA
 if ch=='"':
  return G_TALL[m]
 return G_GROUND[m]
def G_shapes(m,x,y,ch,out):
 px=x*G_T
 py=20+y*G_T
 if ch=='T':
  out.append((0,G_BARK,0,(px+8,py+14,4,6)))
  out.append((1,G_LEAF,1,(px+10,py+8,8)))
 elif ch=='~':
  out.append((0,(110,160,235),0,(px+(x*5+y*3)%8,py+8,6,1)))
 elif ch=='L':
  out.append((0,(250,200,60),0,(px+(x*7+y*5)%12,py+6,5,3)))
 elif ch=='"':
  c=G_GROUND[m]
  for o in(3,9,15):
   out.append((0,c,0,(px+o,py+6+o%4,2,8)))
 elif ch=='^':
  out.append((0,G_ROCK,2,([px,px+10,px+20],[py+20,py+1,py+20])))
  out.append((1,WHITE,2,([px+6,px+10,px+14],[py+8,py+1,py+8])))
 elif ch=='H':
  out.append((0,G_BARK,1,(px+10,py+12,9)))
  out.append((1,(60,40,20),1,(px+10,py+12,6)))
  out.append((2,(245,235,210),1,(px+7,py+12,3)))
  out.append((2,(245,235,210),1,(px+13,py+11,3)))
  out.append((3,(200,160,90),0,(px+1,py+15,18,2)))
 elif ch=='E':
  r=G_DT[G_EGGS.get((m,x,y),0)][2]
  sh=(25,25,35)if r==4 else G_CYAN if r==5 else(245,235,210)
  sp=G_MAG if r==5 else YELLOW if r==4 else G_RCOL[r]if r else(200,170,120)
  out.append((0,G_BARK,0,(px+3,py+15,14,4)))
  out.append((1,sh,1,(px+10,py+10,6)))
  out.append((2,sp,0,(px+7,py+8,3,3)))
  out.append((2,sp,0,(px+11,py+12,3,3)))
 elif ch=='B':
  out.append((0,(40,30,60),1,(px+10,py+10,9)))
  out.append((1,G_BOSS[4],1,(px+10,py+10,6)))
  out.append((2,(255,60,60),0,(px+6,py+8,3,3)))
  out.append((2,(255,60,60),0,(px+11,py+8,3,3)))
def G_hero(g,out):
 px=g.x*G_T
 py=20+g.y*G_T
 d=g.ride
 if d is not None:
  c=d[6]
  out.append((5,lt(c,0.45),2,([px,px+9,px+4],[py+2,py+11,py+14])))
  out.append((6,c,0,(px+2,py+11,13,7)))
  out.append((6,c,0,(px+13,py+6,7,7)))
  out.append((6,c,0,(px,py+15,3,3)))
  out.append((6,c,0,(px+4,py+18,3,2)))
  out.append((6,c,0,(px+11,py+18,3,2)))
  out.append((7,YELLOW if d[1]==19 else BLACK,0,(px+17,py+8,2,2)))
  if d[8]:
   out.append((7,G_GEARC[d[8]],0,(px+5,py+11,6,3)))
  if d[7]:
   out.append((8,G_GEARC[d[7]],0,(px+14,py+3,5,3)))
  out.append((8,(240,200,160),1,(px+8,py+5,3)))
  out.append((8,(60,120,230),0,(px+6,py+8,5,4)))
  return
 out.append((5,(240,200,160),1,(px+10,py+5,4)))
 out.append((6,G_BARK,0,(px+6,py+1,8,3)))
 out.append((6,(60,120,230),0,(px+6,py+9,8,7)))
 out.append((6,(60,40,30),0,(px+6,py+16,3,4)))
 out.append((6,(60,40,30),0,(px+11,py+16,3,4)))
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
def G_hud(g):
 d=g.ride
 if d is not None:
  who=d[0]+' '+str(d[3])+'/'+str(d[4])
 else:
  who='You '+str(g.hp)+'/'+str(g.mhp)
 t=(G_LANDS[g.m],who,'Egg '+str(g.warm)if g.bag else str(g.coins)+'c')
 if t==G_HUD[0]:
  return
 old=G_HUD[0]or('','','')
 if G_HUD[0]is None:
  rect(0,0,320,20,BLACK)
 for i,x,c in((0,4,GOLD),(1,140,WHITE),(2,262,YELLOW)):
  if t[i]!=old[i]:
   text(x,15,old[i],BLACK)
   text(x,15,t[i],c)
 G_HUD[0]=t
def G_evil(*a):
 import GHDRAGOW
 r=GHDRAGOW.G_evil(*a)
 GHDRAGOW=None
 G__drop('GHDRAGOW')
 return r
def G_rest(*a):
 import GHDRAGOX
 r=GHDRAGOX.G_rest(*a)
 GHDRAGOX=None
 G__drop('GHDRAGOX')
 return r
def G_load(*a):
 import GHDRAGOX
 r=GHDRAGOX.G_load(*a)
 GHDRAGOX=None
 G__drop('GHDRAGOX')
 return r
def G_nest(*a):
 import GHDRAGOX
 r=GHDRAGOX.G_nest(*a)
 GHDRAGOX=None
 G__drop('GHDRAGOX')
 return r
def G_menu(*a):
 import GHDRAGOX
 r=GHDRAGOX.G_menu(*a)
 GHDRAGOX=None
 G__drop('GHDRAGOX')
 return r
def G_win(*a):
 import GHDRAGOX
 r=GHDRAGOX.G_win(*a)
 GHDRAGOX=None
 G__drop('GHDRAGOX')
 return r
def G_backpack(*a):
 import GHDRAGOY
 r=GHDRAGOY.G_backpack(*a)
 GHDRAGOY=None
 G__drop('GHDRAGOY')
 return r
def G_book(*a):
 import GHDRAGOY
 r=GHDRAGOY.G_book(*a)
 GHDRAGOY=None
 G__drop('GHDRAGOY')
 return r
def G_hatch(*a):
 import GHDRAGOY
 r=GHDRAGOY.G_hatch(*a)
 GHDRAGOY=None
 G__drop('GHDRAGOY')
 return r
def G__drop(m):
 import sys,gc
 try:
  del sys.modules[m]
 except Exception:
  pass
 gc.collect()
