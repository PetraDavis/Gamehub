# GHDRAGOP: the game part of GHDRAGON. Run GHDRAGON, not this.
from GHDRAGOB import*
G_NAMES=('Blaze','Splash','Fern','Spark','Misty','Clover','Ziggy','Nova','Pebble','Rocket','Biscuit','Luna','Comet','Pip','Maple','Echo','Sunny','Bolt','Willow','Ash','Ripple','Twig','Ember','Taro')
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
def G_foe_art(f):
 c=f[4]
 n=f[0]
 if n=='Shadow Wyrm':
  G_baby(225,105,c,3)
  rect(166,79,9,9,RED)
 elif n in('Goblin','Rock Troll','Snow Yeti'):
  s=1 if n=='Goblin'else 2
  rect(220-12*s,100-10*s,24*s,30*s,c)
  circ(220,92-14*s,10*s,c)
  rect(214-2*s,88-16*s,4,4,BLACK)
  rect(222+2*s,88-16*s,4,4,BLACK)
 elif n=='Bog Toad':
  circ(220,105,26,c)
  circ(206,82,8,c)
  circ(234,82,8,c)
  circ(206,82,3,BLACK)
  circ(234,82,3,BLACK)
 else:
  col(c)
  fill_poly([195,245,230,220,210],[80,80,130,115,130])
  circ(220,78,16,c)
  rect(212,74,4,4,BLACK)
  rect(224,74,4,4,BLACK)
def G_battle(g,f):
 name,fhp,fat,xp,fc,fe=f
 mx=fhp
 cls()
 rbox(150,30,140,120,10,fc,2,BLACK)
 G_foe_art(f)
 ctext(24,name+' appears!',GOLD)
 log=''
 sel=0
 was=None
 while True:
  d=g.ride
  opts=('Claw','Breath','Run')if d is not None else('Sword','Run')
  n=len(opts)
  w=300//n
  sel=min(sel,n-1)
  now=(d[0]if d else 'You',d[3]if d else g.hp,fhp,sel,log,n)
  if was is None or was[0]!=now[0]:
   rect(0,40,148,60,BLACK)
   rect(0,150,320,34,BLACK)
   text(12,56,now[0],d[6]if d else WHITE)
   text(12,86,name[:12],fc)
   for i in range(n):
    cc=GOLD if i==sel else WHITE
    rbox(10+i*w,154,w-6,24,8,cc)
    text(10+i*w+(w-6)//2-len(opts[i])*5,172,opts[i],cc)
   was=None
  if was is None or was[1]!=now[1]:
   G_bar(12,62,120,now[1],d[4]if d else g.mhp,GREEN)
  if was is None or was[2]!=fhp:
   G_bar(12,92,120,fhp,mx,RED)
  if was is not None and was[3]!=sel:
   for i in(was[3],sel):
    cc=GOLD if i==sel else WHITE
    edge(10+i*w,154,w-6,24,8,cc)
    text(10+i*w+(w-6)//2-len(opts[i])*5,172,opts[i],cc)
  if was is None or was[4]!=log:
   rect(0,186,320,24,BLACK)
   text(6,202,log[:31],GREY)
  was=now
  k=wkey()
  if k in(LEFT,RIGHT):
   sel=(sel+(1 if k==RIGHT else-1))%n
   continue
  if k!=OK:
   continue
  o=opts[sel]
  if o=='Run':
   if f is G_BOSS:
    log='The Wyrm blocks your way!'
    continue
   if random.random()<0.6:
    return True
   log="Couldn't get away."
  elif o=='Sword':
   dm=random.randint(3,5)
   fhp-=dm
   log='Sword hits for '+str(dm)+'.'
  else:
   at=5+2*d[2]+2*G_DT[d[1]][2]
   if o=='Claw':
    dm=at+random.randint(0,2)
    log='Claw hits for '+str(dm)+'.'
   else:
    dm=at+random.randint(2,5)
    if G_beats(G_el(d),fe):
     dm*=2
     log='Super breath! '+str(dm)+'.'
    elif G_beats(fe,G_el(d)):
     dm//=2
     log='Weak breath... '+str(dm)+'.'
    else:
     log='Breath hits for '+str(dm)+'.'
   fhp-=dm
  if fhp<=0:
   msg=[]
   for dd in g.pen:
    if dd[3]>0 and(dd is d or dd is g.pick):
     dd[5]+=xp
     while dd[5]>=dd[2]*10:
      dd[5]-=dd[2]*10
      dd[2]+=1
      dd[4]+=6
      dd[3]=dd[4]
      msg.append(dd[0]+' is now level '+str(dd[2])+'!')
   message(msg[:3]or['You won!'],name+' beaten')
   if f is not G_BOSS:
    G_quest_step(g,0,name)
    G_quest_step(g,2,g.m)
   return True
  dm=max(1,fat+random.randint(0,3)-(d[2]if d else 0))
  log+=' It hits '+str(dm)+'.'
  if d is not None:
   d[3]=max(0,d[3]-dm)
   if d[3]==0:
    g.ride=None
    message([d[0]+' is too tired to fly.','You fight on foot!'],'Oh no')
    cls()
    rbox(150,30,140,120,10,fc,2,BLACK)
    G_foe_art(f)
    ctext(24,name,GOLD)
    was=None
  else:
   g.hp-=dm
   if g.hp<=0:
    message(['You fainted...','Your dragons carry you','home to the nest.'],'Ouch')
    G_go_home(g)
    return False
def G_quest_step(g,kind,what):
 q=g.quest
 if q is None or q[0]!=kind or(q[1]is not None and q[1]!=what):
  return
 q[3]+=1
 if q[3]>=q[2]:
  g.coins+=q[4]
  g.quest=None
  message(['You finished:',q[5],'+'+str(q[4])+' coins!'],'Quest done!')
def G_hatch(g):
 e=g.egg
 g.egg=None
 t=G_DT[e]
 cls()
 ctext(30,'The egg is cracking!',GOLD)
 circ(160,110,30,(245,235,210))
 pause(0.8)
 rect(120,70,80,80,BLACK)
 G_baby(160,115,t[3],2)
 ctext(190,G_RARE[t[2]]+' '+t[0]+' dragon!',G_RCOL[t[2]])
 pause(1.0)
 names=sample(G_NAMES,4)
 i=choose('Name your '+t[0]+':',names)
 nm=names[max(0,i)]
 d=[nm,e,1,20+6*t[2],20+6*t[2],0,t[3],0]
 g.pen.append(d)
 msg=[nm+' joins your pen!']
 if g.pick is None:
  g.pick=d
  msg+=['Press ENTER to ride.','Dragons fly over water,','lava and mountains.']
 G_draw_map(g)
 message(msg,G_RARE[t[2]]+' '+t[0])
 G_quest_step(g,1,None)
 G_draw_map(g,True)
def G_menu(g):
 d=g.pick
 if g.ride is not None:
  first='Get off '+d[0]
 else:
  first='Ride '+d[0]+(''if d[3]>0 else ' (tired)')
 c=choose(d[0]+' the '+G_DT[d[1]][0],[first,'Fly home to the nest','Keep exploring'])
 if c==0:
  if g.ride is not None:
   if g.maps[g.m][g.y][g.x]in '~L^':
    G_draw_map(g)
    message(["You can't get off here!"])
    G_draw_map(g,True)
    return
   g.ride=None
  elif d[3]==0:
   G_draw_map(g)
   message([d[0]+' is too tired.','Rest at the nest first.'])
   G_draw_map(g,True)
   return
  else:
   g.ride=d
 elif c==1:
  G_go_home(g)
 G_draw_map(g)
def G_spawn(g):
 g.spawn=random.randint(25,40)
 mp=g.maps[g.m]
 if sum((1 for k in G_EGGS if k[0]==g.m))>=2:
  return
 for n in range(20):
  x=random.randint(1,14)
  y=random.randint(1,7)
  if mp[y][x]in '."'and abs(x-g.x)+abs(y-g.y)>3:
   mp[y][x]='E'
   G_EGGS[g.m,x,y]=G_egg_type(g.m)
   G_cells(g,[(x,y)],False)
   return
def G_play():
 g=G_Game()
 g.maps=[[list(r)for r in mp]for mp in G_MAPS]
 G_EGGS.clear()
 for m in range(3):
  for y in range(9):
   for x in range(16):
    if G_MAPS[m][y][x]=='E':
     G_EGGS[m,x,y]=random.randint(0,6)if m==0 else G_egg_type(m)
 g.m,g.x,g.y=(0,3,2)
 g.hp=g.mhp=20
 g.pen=[]
 g.pick=None
 g.ride=None
 g.egg=None
 g.warm=0
 g.coins=0
 g.quest=None
 g.seen=0
 g.spawn=30
 steps=0
 G_draw_map(g)
 message(['The Shadow Wyrm scared','the dragons away. Find','eggs and raise a team!'],'DRAGON TAMER')
 G_draw_map(g,True)
 while True:
  k=wkey()
  if k==CLR:
   if message(['ENTER: quit adventure','CLEAR: keep going'],'Quit?')==OK:
    return
   G_draw_map(g,True)
   continue
  if k in(OK,SECOND):
   if g.pick is not None:
    G_menu(g)
   continue
  dx,dy={LEFT:(-1,0),RIGHT:(1,0),UP:(0,-1),DOWN:(0,1)}.get(k,(0,0))
  if dx==0 and dy==0:
   continue
  nx,ny=(g.x+dx,g.y+dy)
  if nx<0 or nx>15:
   m=g.m+(1 if nx>15 else-1)
   if 0<=m<3:
    ch=g.maps[m][ny][15-g.x]
    if ch!='T'and(ch not in '~L^'or g.ride is not None):
     g.m=m
     g.seen=max(g.seen,m)
     g.x=15-g.x
     G_draw_map(g)
   continue
  if ny<0 or ny>8:
   continue
  mp=g.maps[g.m]
  ch=mp[ny][nx]
  if ch=='T'or(ch in '~L^'and g.ride is None):
   continue
  if ch=='B':
   if G_battle(g,G_BOSS):
    cls()
    G_baby(160,120,g.ride[6]if g.ride else GOLD,2)
    message(['The Shadow Wyrm flies far','away. Dragons return to','every land. You did it!'],'THE END')
    return
   G_draw_map(g)
   continue
  if ch=='E'and(g.egg is not None or len(g.pen)>=7):
   G_draw_map(g)
   message(["You're already keeping",'an egg warm.']if g.egg is not None else['Your pen is full (7).','Let a dragon go first.'],'Egg')
   G_draw_map(g,True)
   continue
  ox,oy=(g.x,g.y)
  g.x,g.y=(nx,ny)
  if ch=='E':
   mp[ny][nx]='.'
   G_cells(g,[(ox,oy),(nx,ny)],True)
   g.egg=G_EGGS.pop((g.m,nx,ny),0)
   g.warm=12
   G_hud(g)
   message(['You found an egg with',G_RARE[G_DT[g.egg][2]]+' spots! Keep','walking and it will hatch.'],'An egg!')
   G_draw_map(g,True)
   continue
  if ch=='H':
   G_nest(g)
   G_draw_map(g)
   continue
  G_cells(g,[(ox,oy),(nx,ny)],True)
  if g.egg is not None:
   g.warm-=1
   if g.warm<=0:
    G_hatch(g)
    continue
  g.spawn-=1
  if g.spawn<=0:
   G_spawn(g)
  G_hud(g)
  steps+=1
  if ch=='"'and steps>3 and(random.random()<0.2):
   steps=0
   G_battle(g,random.choice(G_FOES[g.m]))
   G_draw_map(g)
def G_back():
 G_play()
