# GHDRAGOB: part of GHDRAGOP. Keep it next to GHDRAGOP.
from GHDRAGOC import*
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
G_NAMES=('Blaze','Splash','Fern','Spark','Misty','Clover','Ziggy','Nova','Pebble','Rocket','Biscuit','Luna','Comet','Pip','Maple','Echo','Sunny','Bolt','Willow','Ash','Ripple','Twig','Ember','Taro')
G_GEAR=(('',0),('Bow',15),('Goggles',25),('Wizard hat',40),('Crown',80),('Party hat',20),('Top hat',35),('Flower',15),('Viking helmet',60),('Scarf',15),('Saddle',25),('Cape',40),('Armor',60),('Bell collar',20),('Backpack',30),('Flag',45),('Necklace',50))
G_FOES=((('Goblin',14,4,6,(110,160,60),3),('Bog Toad',16,4,7,(60,120,160),1)),(('Lava Imp',26,7,12,(240,120,30),0),('Rock Troll',32,7,14,(120,110,90),2)),(('Ice Wraith',34,9,16,(150,200,240),1),('Snow Yeti',42,9,18,(235,235,245),3)))
def G_egg_type(m):
 r=random.randint(0,99)+m*6
 rar=4 if r>=99 else 3 if r>=92 else 2 if r>=78 else 1 if r>=52 else 0
 return random.choice([i for i in range(20)if G_DT[i][2]==rar])
def G_egg(x,y,s,t):
 r=G_DT[t][2]
 shell=((245,235,210),(225,240,205),(215,230,250),(235,215,250),(30,30,70),(20,20,45))[r]
 G_oval(x,y,s,BLACK,-1)
 G_oval(x,y,s,dk(shell,0.7))
 G_oval(x-s,y-s,s,shell,2*s)
 if r==4:
  for dx,dy,n in((-3,-4,1),(3,3,1),(-2,5,0),(-1,-7,0),(-5,1,0),(4,-5,0)):
   rect(x+(dx-n)*s,y+dy*s,(2*n+1)*s,s,YELLOW)
   rect(x+dx*s,y+(dy-n)*s,s,(2*n+1)*s,YELLOW)
  circ(x+s,y-s,2*s,(250,230,140))
  circ(x+2*s,y-2*s,2*s,shell)
 elif r==5:
  circ(x+2*s,y+4*s,4*s,(35,40,110))
  circ(x-3*s,y+1*s,2*s,(35,40,110))
  Z=(-1,-8,2,-4,-2,-1,2,2,-1,5,1,8)
  for c,w in(((110,50,180),s+1),((210,150,255),max(1,s//2))):
   col(c)
   for i in range(0,10,2):
    ax,ay,bx,by=(x+Z[i]*s,y+Z[i+1]*s,x+Z[i+2]*s,y+Z[i+3]*s)
    fill_poly([ax-w,ax+w,bx+w,bx-w],[ay,ay,by,by])
  rect(x-5*s,y-3*s,s,s,(210,150,255))
  rect(x+4*s,y-6*s,s,s,(210,150,255))
 else:
  sp=((190,150,100),(90,170,80),(60,120,230),(150,80,220))[r]
  if r>=2:
   for i in range(-5,5,2):
    rect(x+i*s,y+(i%4==1)*s,2*s,2*s,sp)
  for dx,dy in((-3,-5),(2,-3),(-2,5),(3,5),(-5,2))[:3+r]:
   rect(x+dx*s,y+dy*s,2*s,2*s,sp)
 circ(x-3*s,y-5*s,s+1,WHITE)
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
def G_save(g):
 s=[2,g.coins,g.own,g.book]+(g.bag+[-1]*5)[:5]
 for d in g.pen:
  p=G_PAINT.index(d[6])+1 if d[6]in G_PAINT and d[6]!=G_DT[d[1]][3]else 0
  s+=[G_NAMES.index(d[0])*32+d[1],d[2],d[5],p*200+d[7]*20+d[8]]
 try:
  from ti_system import store_list
  store_list('DRG',s)
 except Exception:
  pass
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
def G_board(g):
 if g.quest is not None:
  q=g.quest
  c=choose(q[5]+' '+str(q[3])+'/'+str(q[2]),['Keep going','Give up quest'])
  if c==1:
   g.quest=None
  return
 qs=[G_new_quest(g)for i in range(3)]
 c=choose('Quests: pick one',[q[5][:15]+' '+str(q[4])+'c'for q in qs]+['Not now'])
 if 0<=c<3:
  g.quest=qs[c]
def G_lst(title,opts):
 cls()
 ctext(24,title,GOLD)
 n=len(opts)
 sel=old=0
 for i in range(n):
  text(70,50+i*17,opts[i],GOLD if i==0 else WHITE)
 while True:
  if sel!=old:
   for i in(old,sel):
    rect(0,34+i*17,320,17,BLACK)
    text(70,50+i*17,opts[i],GOLD if i==sel else WHITE)
  rect(54,40+sel*17,8,6,GOLD)
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
def G_put_egg(g,t,near):
 mp=g.maps[g.m]
 for n in range(30):
  if near:
   x=g.x+random.randint(-1,1)
   y=g.y+random.randint(-1,1)
  else:
   x=random.randint(1,14)
   y=random.randint(1,7)
  if 0<=x<16 and 0<=y<9 and(mp[y][x]in '."')and((x,y)!=(g.x,g.y))and(near or abs(x-g.x)+abs(y-g.y)>3):
   mp[y][x]='E'
   G_EGGS[g.m,x,y]=t
   G_cells(g,[(x,y)],False)
   return True
 return False
def G_evil(g):
 cls()
 ctext(90,'The sky goes dark...',RED)
 pause(0.8)
 if not G_battle(g,G_DREAD):
  return False
 G_draw_map(g)
 if not G_put_egg(g,20,True)and len(g.bag)<5:
  g.bag.append(20)
 message(['The Dread Drake flies','away... and leaves a','strange egg behind!'],'Whoa!')
 G_draw_map(g,True)
 return True
