# GHDRAGOP: the game part of GHDRAGON. Run GHDRAGON, not this.
from GHDRAGOB import*
GREY=(110,110,110)
def pause(s):
 time.sleep(s)
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
G_NIGHT=(45,50,80)
G_ENAME=('fire','water','plant','star')
G_NAMES=('Blaze','Splash','Fern','Spark','Misty','Clover','Ziggy','Nova','Pebble','Rocket','Biscuit','Luna','Comet','Pip','Maple','Echo','Sunny','Bolt','Willow','Ash','Ripple','Twig','Ember','Taro')
G_PAINT=G_cl(b'\xdcF(<\x82\xe6F\xaaF\xf0\xbe(\xc8n\xf0\xf0x\x96((2\xf0\xf0\xf5')
def G_egg_roll(g,t):
 if g.book&2097151 and random.random()<0.05:
  t=G_SMALL
 if random.random()<0.02:
  r=random.random()
  return t+32*(1 if r<0.4 else 2 if r<0.7 else 3 if r<0.9 else 4)
 return t
def G_grown(g):
 for d in g.pen:
  if not d[9]&8:
   return d
 return None
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
 G_CAVE[0]=not g.book>>26&1 and any((d[1]==20 and(not d[9]&8)for d in g.pen))
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
def G_save(g):
 s=[4,g.coins,g.own,g.book,g.dread]+(g.bag+[-1]*5)[:5]
 b=[2,g.glim+100*g.luck+200*g.curse+400*min(10,g.buys)]
 for d in g.pen:
  if d[9]&8:
   b+=[G_pack(d[0]),d[1]+32*(d[9]&7)]
   continue
  p=G_PAINT.index(d[6])+1 if d[6]in G_PAINT and d[6]!=G_DT[d[1]][3]else 0
  s+=[G_pack(d[0]),d[1],d[2],d[5],(d[9]&7)*4000+p*200+d[7]*20+d[8]]
 try:
  from ti_system import store_list
  store_list('DRG',s)
  store_list('DRB',b)
 except Exception:
  pass
def G_quest_step(g,kind,what):
 q=g.quest
 if q is None or q[0]!=kind or(q[1]is not None and q[1]!=what):
  return
 q[3]+=1
 if q[3]>=q[2]:
  g.coins+=q[4]
  g.quest=None
  message(['You finished:',q[5],'+'+str(q[4])+' coins!'],'Quest done!')
def G_put_egg(g,t,near,ch='E'):
 mp=g.maps[g.m]
 for n in range(30):
  if near:
   x=g.x+random.randint(-1,1)
   y=g.y+random.randint(-1,1)
  else:
   x=random.randint(1,14)
   y=random.randint(1,7)
  if 0<=x<16 and 0<=y<9 and(mp[y][x]in '."')and((x,y)!=(g.x,g.y))and(near or abs(x-g.x)+abs(y-g.y)>3):
   mp[y][x]=ch
   if ch=='E':
    G_EGGS[g.m,x,y]=t
   else:
    g.shen=(g.m,x,y)
   G_cells(g,[(x,y)],False)
   return True
 return False
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
 g.book=0
 g.quest=None
 g.seen=0
 g.face=0
 g.spawn=100
 g.dread=0
 g.glim=g.luck=g.curse=g.buys=0
 g.shen=None
 g.shn=random.randint(250,350)
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
   c=G_menu(g)
   if c:
    (G_backpack if c==1 else G_book)(g)
    G_draw_map(g)
   continue
  dx,dy={LEFT:(-1,0),RIGHT:(1,0),UP:(0,-1),DOWN:(0,1)}.get(k,(0,0))
  if dx==0 and dy==0:
   continue
  nx,ny=(g.x+dx,g.y+dy)
  if dx:
   g.face=dx>0
  if nx<0 or nx>15:
   m=(0 if nx>15 else-1)if g.m==3 else g.m+(1 if nx>15 else-1)
   if m<0 and g.m==0:
    m=3
   if 0<=m<=3:
    ch=g.maps[m][ny][15-g.x]
    if ch!='T'and(ch not in '~L^'or g.ride is not None):
     if g.shen:
      G_shen_off(g)
     g.m=m
     if m<3:
      g.seen=max(g.seen,m)
     g.x=15-g.x
     G_draw_map(g)
   continue
  if ny<0 or ny>8:
   continue
  mp=g.maps[g.m]
  ch=mp[ny][nx]
  if ch=='C'and G_CAVE[0]:
   if not G_titan(g):
    return
   continue
  if ch in 'TW'or(ch in '~L^C'and g.ride is None):
   continue
  if ch=='B':
   if G_battle(g,G_BOSS):
    G_win(g)
    return
   if g.hp<=0:
    return
   G_draw_map(g)
   continue
  if ch=='E'and(len(g.bag)>=5 or G_kids(g)+(1 if G_EGGS.get((g.m,nx,ny),0)%32==G_SMALL else 4)>40):
   G_draw_map(g)
   message(['Your backpack is full.']if len(g.bag)>=5 else['No room in your pen.','Let a dragon go first.'],'Egg')
   G_draw_map(g,True)
   continue
  if ch=='M':
   G_shen(g)
   G_draw_map(g)
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
   message(['You found a'+(' shiny'if e>31 else '')+' small egg!',"It's in your backpack."]if e%32==G_SMALL else['You found a'+(' shiny'if e>31 else 'n')+' egg with',G_RARE[G_DT[e%32][2]]+" spots! It's in",'your backpack.'],'An egg!')
   G_draw_map(g,True)
   continue
  if ch=='Q':
   G_board(g)
   G_draw_map(g)
   continue
  if ch=='S':
   G_draw_map(g)
   if g.pick is None:
    message(['Hatch a dragon first!'],'Shop')
    G_draw_map(g,True)
   else:
    G_shop(g)
    G_draw_map(g)
   continue
  if ch=='H':
   while True:
    c=G_nest(g)
    if not c:
     break
    (G_backpack if c==1 else G_book if c==2 else G_glim)(g)
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
   g.spawn=random.randint(100,200)
   if g.m<3 and(not any((q[0]==g.m for q in G_EGGS))):
    G_put_egg(g,G_egg_roll(g,G_egg_type(g.m,g.luck)),False)
    g.luck=0
  g.shn-=1
  if g.shen:
   if g.shn<0:
    G_shen_off(g)
  elif g.shn<=0 and g.m<3 and G_put_egg(g,0,False,'M'):
   g.shn=60
  if g.curse and random.random()<0.01:
   g.coins-=min(g.coins,random.randint(1,3))
  G_hud(g)
  steps+=1
  if g.dread>0:
   g.dread-=1
  if g.m<3 and(g.dread==1 or(not g.dread and steps>3 and(random.random()<G_EVIL)))and(not g.book>>25&1)and any((G_DT[d[1]][2]>=3 for d in g.pen)):
   steps=0
   if not G_evil(g):
    return
   continue
  if ch=='"'and steps>3 and(random.random()<0.2):
   steps=0
   lo,hi=G_LVL[g.m]
   if not G_battle(g,random.choice(G_FOES[g.m]),lo+min(hi-lo,int(random.random()**1.6*(hi-lo+1)))):
    return
   G_draw_map(g)
def G_back():
 G_play()
