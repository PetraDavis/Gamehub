# GHDRAGOP: the game part of GHDRAGON. Run GHDRAGON, not this.
from GHDRAGOB import*
def G_egg_type(m):
 r=random.randint(0,99)+m*6
 rar=4 if r>=99 else 3 if r>=92 else 2 if r>=78 else 1 if r>=52 else 0
 return random.choice([i for i in range(20)if G_DT[i][2]==rar])
def G_save(g):
 s=[1,g.coins,g.own]+(g.bag+[-1]*5)[:5]
 for d in g.pen:
  p=G_PAINT.index(d[6])+1 if d[6]in G_PAINT and d[6]!=G_DT[d[1]][3]else 0
  s+=[G_NAMES.index(d[0])*32+d[1],d[2],d[5],p*200+d[7]*20+d[8]]
 try:
  from ti_system import store_list
  store_list('DRG',s)
 except Exception:
  pass
def G_load(g):
 try:
  from ti_system import recall_list
  s=[int(v)for v in recall_list('DRG')]
 except Exception:
  return
 if len(s)<8 or s[0]!=1:
  return
 g.coins,g.own=(s[1],s[2])
 g.bag=[e for e in s[3:8]if e>=0]
 for i in range(8,len(s)-3,4):
  t=s[i]%32
  lv=s[i+1]
  mh=20+6*min(4,G_DT[t][2])+6*(lv-1)
  p=s[i+3]//200
  g.pen.append([G_NAMES[s[i]//32],t,lv,mh,mh,s[i+2],G_PAINT[p-1]if p else G_DT[t][3],s[i+3]//20%10,s[i+3]%20])
 if g.pen:
  g.pick=g.pen[0]
 g.warm=12
def G_pen(g):
 while g.pen:
  opts=[('> 'if d is g.pick else '')+d[0]+' L'+str(d[2])+' '+G_DT[d[1]][0][:6]for d in g.pen]
  c=choose('Dragon pen '+str(len(g.pen))+'/10',opts+['Back'])
  if c<0 or c>=len(g.pen):
   return
  d=g.pen[c]
  a=choose(d[0]+' the '+G_DT[d[1]][0],['Pick as partner','See '+d[0],'Let it go free','Back'])
  if a==0:
   g.pick=d
  elif a==1:
   t=G_DT[d[1]]
   G_portrait(d)
   message([t[0]+' ('+G_RARE[t[2]]+')','Element: '+G_ENAME[t[1]],'Level '+str(d[2])+'  HP '+str(d[4])],d[0])
  elif a==2 and len(g.pen)>1:
   g.pen.remove(d)
   if g.pick is d:
    g.pick=g.pen[0]
def G_dress(g,d,first):
 ids=[i for i in range(first,first+8)if g.own>>i&1]
 if not ids:
  message(['Buy one in the shop first.'],'Nothing to wear')
  return
 c=G_lst('Wear on '+('head'if first==1 else 'body'),[G_GEAR[i][0]for i in ids]+['Nothing'])
 if c<0:
  return
 v=ids[c]if c<len(ids)else 0
 if first==1:
  d[7]=v
 else:
  d[8]=v
 G_portrait(d)
 message([d[0]+' looks great!'],'Dressed up')
def G_shop(g):
 while True:
  d=g.pick
  c=choose(d[0]+': '+str(g.coins)+' coins',['Buy accessories','Head: '+(G_GEAR[d[7]][0]or 'nothing'),'Body: '+(G_GEAR[d[8]][0]or 'nothing'),'Paint it 20c','Back'])
  if c==0:
   f=choose('Buy for the',['Head','Body','Back'])
   if f not in(0,1):
    continue
   f=1+8*f
   opts=[G_GEAR[i][0]+(' (have)'if g.own>>i&1 else ' '+str(G_GEAR[i][1])+'c')for i in range(f,f+8)]
   i=G_lst(str(g.coins)+' coins',opts+['Back'])
   i=f+i if 0<=i<8 else 0
   if i and(not g.own>>i&1):
    if g.coins<G_GEAR[i][1]:
     message(['You need '+str(G_GEAR[i][1])+' coins.','Do quests to earn more.'],'Not enough')
    else:
     g.coins-=G_GEAR[i][1]
     g.own|=1<<i
     message([G_GEAR[i][0]+' is in your bag.'],'Bought!')
  elif c in(1,2):
   G_dress(g,d,1 if c==1 else 9)
  elif c==3:
   if g.coins<20:
    message(['You need 20 coins.'],'Not enough')
    continue
   p=choose('Pick a colour',list(G_PAINTN))
   if p>=0:
    g.coins-=20
    d[6]=G_PAINT[p]
    G_portrait(d)
    message([d[0]+' looks great!'],'Painted')
  else:
   return
def G_nest(g):
 G_rest(g)
 G_save(g)
 while True:
  c=choose('The Nest (saved)',['Dragon pen','Quest board','Shop','Backpack','Leave the nest'])
  if c==0:
   G_pen(g)
  elif c==1:
   G_board(g)
  elif c==2:
   if g.pick is None:
    message(['Hatch a dragon first!'])
   else:
    G_shop(g)
  elif c==3:
   G_backpack(g)
  else:
   G_save(g)
   return
def G_backpack(g):
 cls(G_NIGHT)
 ctext(22,'BACKPACK',GOLD)
 if not g.bag:
  ctext(100,'No eggs. Go and find some!')
 for i in range(len(g.bag)):
  G_egg(40+i*60,90,3,g.bag[i])
  text(16+i*60,150,G_RARE[G_DT[g.bag[i]][2]][:5],G_RCOL[G_DT[g.bag[i]][2]])
 if g.bag:
  text(6,186,'The first egg hatches in '+str(g.warm),WHITE)
 n=len([i for i in range(1,17)if g.own>>i&1])
 text(6,204,'Accessories: '+str(n)+' of 16',GREY)
 while wkey()not in(OK,CLR):
  pass
def G_hatch(g):
 e=g.bag.pop(0)
 g.warm=12
 t=G_DT[e]
 cls(G_NIGHT)
 ctext(24,'The egg is cracking!',GOLD)
 G_egg(160,110,5,e)
 pause(1.0)
 cls(G_NIGHT)
 G_drag(73,30,3,e,t[3])
 ctext(200,G_RARE[t[2]]+' '+t[0]+' dragon!',G_RCOL[t[2]])
 pause(1.2)
 names=sample(G_NAMES,4)
 i=choose('Name your '+t[0]+':',names)
 nm=names[max(0,i)]
 mh=20+6*min(4,t[2])
 d=[nm,e,1,mh,mh,0,t[3],0,0]
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
 c=choose(d[0]+' the '+G_DT[d[1]][0],[first,'Backpack','Keep exploring'])
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
  G_backpack(g)
 G_draw_map(g)
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
 g.hp=g.mhp=30
 g.pen=[]
 g.pick=None
 g.ride=None
 g.bag=[]
 g.warm=12
 g.coins=0
 g.own=0
 g.quest=None
 g.seen=0
 g.spawn=30
 G_load(g)
 steps=0
 G_draw_map(g)
 if g.pen or g.bag:
  message(['Welcome back! You have',str(len(g.pen))+' dragons, '+str(g.coins)+' coins.'],'DRAGON TAMER')
 else:
  message(['The Shadow Wyrm scared','the dragons away. Find','eggs and raise a team!'],'DRAGON TAMER')
 G_draw_map(g,True)
 while True:
  k=wkey()
  if k==CLR:
   if message(['ENTER: save and quit','CLEAR: keep going'],'Quit?')==OK:
    G_rest(g)
    G_save(g)
    return
   G_draw_map(g,True)
   continue
  if k in(OK,SECOND):
   if g.pick is not None:
    G_menu(g)
   else:
    G_backpack(g)
    G_draw_map(g)
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
    if g.pick:
     G_drag(73,30,3,g.pick[1],g.pick[6],g.pick[7],g.pick[8])
    message(['The Shadow Wyrm flies far','away. Dragons return to','every land. You did it!'],'THE END')
    G_rest(g)
    G_save(g)
    return
   if g.hp<=0:
    return
   G_draw_map(g)
   continue
  if ch=='E'and(len(g.bag)>=5 or len(g.pen)+len(g.bag)>=10):
   G_draw_map(g)
   message(['Your backpack is full.']if len(g.bag)>=5 else['No room in your pen.','Let a dragon go first.'],'Egg')
   G_draw_map(g,True)
   continue
  ox,oy=(g.x,g.y)
  g.x,g.y=(nx,ny)
  if ch=='E':
   mp[ny][nx]='.'
   G_cells(g,[(ox,oy),(nx,ny)],True)
   e=G_EGGS.pop((g.m,nx,ny),0)
   if not g.bag:
    g.warm=12
   g.bag.append(e)
   G_hud(g)
   message(['You found an egg with',G_RARE[G_DT[e][2]]+" spots! It's in",'your backpack.'],'An egg!')
   G_draw_map(g,True)
   continue
  if ch=='H':
   G_nest(g)
   G_draw_map(g)
   continue
  G_cells(g,[(ox,oy),(nx,ny)],True)
  if g.bag:
   g.warm-=1
   if g.warm<=0:
    G_hatch(g)
    continue
  g.spawn-=1
  if g.spawn<=0:
   g.spawn=random.randint(25,40)
   if sum((1 for q in G_EGGS if q[0]==g.m))<2:
    G_put_egg(g,G_egg_type(g.m),False)
  G_hud(g)
  steps+=1
  if steps>3 and random.random()<G_EVIL:
   steps=0
   if not G_evil(g):
    return
   continue
  if ch=='"'and steps>3 and(random.random()<0.2):
   steps=0
   if not G_battle(g,random.choice(G_FOES[g.m])):
    return
   G_draw_map(g)
def G_back():
 G_play()
