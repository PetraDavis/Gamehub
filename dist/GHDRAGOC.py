# GHDRAGOC: part of GHDRAGOP. Keep it next to GHDRAGOP.
from GHDRAGOD import*
from GHDRAGOD import _corners
def rbox(x,y,w,h,r,c,t=2,inner=BLACK,fill=True):
 edge(x,y,w,h,r,c,t)
 if fill:
  rect(x+t,y+t,w-2*t,h-2*t,inner)
def edge(x,y,w,h,r,c,t=2,inner=BLACK):
 col(c)
 for bx,by,bw,bh in _corners(x,y,w,h,r,t):
  if bw>0 and bh>0:
   fr(bx,by,bw,bh)
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
G_NAMES=('Blaze','Splash','Fern','Spark','Misty','Clover','Ziggy','Nova','Pebble','Rocket','Biscuit','Luna','Comet','Pip','Maple','Echo','Sunny','Bolt','Willow','Ash','Ripple','Twig','Ember','Taro')
G_PAINT=((220,70,40),(60,130,230),(70,170,70),(240,190,40),(200,110,240),(240,120,150),(40,40,50),(240,240,245))
G_PAINTN=('Red','Blue','Green','Gold','Purple','Pink','Black','White')
G_GEARC=(None,(250,150,200),(40,40,40),(130,60,190),GOLD,G_CYAN,BLACK,(250,150,200),(190,195,205),(220,40,30),G_BARK,(40,80,200),(190,195,205),(40,80,200),(90,190,80),(220,40,30),GOLD)
def G_oval(x,y,s,c,k=0):
 circ(x,y+2*s,7*s-k,c)
 circ(x,y-2*s,6*s-k,c)
 circ(x,y-5*s,4*s-k,c)
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
  G_hero(g,ops)
 G_paint(ops)
def G_draw_map(g,after_msg=False):
 r0,r1=(0,9)
 if after_msg:
  r0=max(0,(MSG[0]-20)//G_T)
  r1=min(9,(MSG[0]+MSG[1]-20)//G_T+1)
 else:
  cls()
  G_HUD[0]=None
 G_cells(g,[(x,y)for y in range(r0,r1)for x in range(16)],r0<=g.y<r1)
 G_hud(g)
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
def G_bar(x,y,w,v,mx,c):
 f=max(0,min(w,int(w*v/mx)))if v>0 else 0
 if v>0:
  f=max(2,f)
 rect(x,y,f,6,c)
 rect(x+f,y,w-f,6,DARK)
def G_foe_screen(f,title):
 cls()
 rbox(150,30,140,120,10,RED if f is G_DREAD else f[4],2,G_NIGHT)
 G_foe_art(f)
 ctext(24,title,GOLD)
def G_quest_step(g,kind,what):
 q=g.quest
 if q is None or q[0]!=kind or(q[1]is not None and q[1]!=what):
  return
 q[3]+=1
 if q[3]>=q[2]:
  g.coins+=q[4]
  g.quest=None
  message(['You finished:',q[5],'+'+str(q[4])+' coins!'],'Quest done!')
