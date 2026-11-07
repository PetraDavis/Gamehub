# GHDRAGOX: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
G_GEAR=(('',0),('Bow',15),('Goggles',25),('Wizard hat',40),('Crown',80),('Party hat',20),('Top hat',35),('Flower',15),('Viking helmet',60),('Scarf',15),('Saddle',25),('Cape',40),('Armor',60),('Bell collar',20),('Backpack',30),('Flag',45),('Necklace',50))
G_PAINTN=('Red','Blue','Green','Gold','Purple','Pink','Black','White')
def G_rest(g):
 g.hp=g.mhp
 g.ride=None
 for d in g.pen:
  d[3]=d[4]
def G_load(g):
 try:
  from ti_system import recall_list
  s=[int(v)for v in recall_list('DRG')]
 except Exception:
  return
 if len(s)<9 or s[0]not in(2,3,4):
  return
 v=s[0]
 k=min(1,v-2)
 g.coins,g.own,g.book=(s[1],s[2],s[3])
 if k:
  g.dread=s[4]
 g.bag=[e for e in s[4+k:9+k]if e>=0]
 w=5 if v>3 else 4
 for i in range(9+k,len(s)-w+1,w):
  if v>3:
   n,nm=(s[i],'')
   while n:
    nm=G_ABC[n%27-1]+nm
    n//=27
   nm=nm[0]+nm[1:].lower()
   i+=1
   t=s[i]
  else:
   nm,t=(G_NAMES[s[i]//32],s[i]%32)
  lv=s[i+1]
  mh=20+6*min(4,G_DT[t][2])+6*(lv-1)
  p=s[i+3]//200
  g.pen.append([nm,t,lv,mh,mh,s[i+2],G_PAINT[p-1]if p else G_DT[t][3],s[i+3]//20%10,s[i+3]%20])
 if g.pen:
  g.pick=g.pen[0]
 g.warm=12
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
def G_portrait(d):
 cls(G_NIGHT)
 G_drag(102,10,2,d[1],d[6],d[7],d[8])
def G_pen(g):
 while g.pen:
  opts=[('> 'if d is g.pick else '')+d[0]+' L'+str(d[2])+' '+G_DT[d[1]][0][:6]for d in g.pen]
  c=G_lst('Dragon pen '+str(len(g.pen))+'/10',opts+['Back'])
  if c<0 or c>=len(g.pen):
   return
  d=g.pen[c]
  a=choose(d[0]+' the '+G_DT[d[1]][0],['Pick as partner','See '+d[0],'Let it go free','Back'])
  if a==0:
   g.pick=d
   if g.ride is not None:
    g.ride=d
   message([d[0]+' is your partner now!'],'Partner')
  elif a==1:
   t=G_DT[d[1]]
   G_portrait(d)
   message([t[0]+' ('+G_RARE[t[2]]+')','Element: '+G_ENAME[t[1]],'Level '+str(d[2])+'  HP '+str(d[4])],d[0])
  elif a==2 and len(g.pen)>1:
   g.pen.remove(d)
   if g.pick is d:
    g.pick=g.pen[0]
   if g.ride is d:
    g.ride=g.pick
def G_lst(title,opts):
 cls()
 ctext(24,title,GOLD)
 n=len(opts)
 h=15 if n>9 else 17
 sel=old=0
 for i in range(n):
  text(70,50+i*h,opts[i],GOLD if i==0 else WHITE)
 while True:
  if sel!=old:
   for i in(old,sel):
    rect(0,50+i*h-16,320,h,BLACK)
    text(70,50+i*h,opts[i],GOLD if i==sel else WHITE)
  rect(54,50+sel*h-10,8,6,GOLD)
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
  c=choose('The Nest (saved)',['Dragon pen','Quest board','Shop','Backpack and book','Leave the nest'])
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
   k=choose('Look at your',['Backpack','Dragon book'])
   if k>=0:
    return k+1
  else:
   G_save(g)
   return 0
def G_menu(g):
 d=g.pick
 if g.ride is not None:
  first='Get off '+d[0]
 else:
  first='Ride '+d[0]+(''if d[3]>0 else ' (tired)')
 c=choose(d[0]+' the '+G_DT[d[1]][0],[first,'Backpack','Dragon book','Keep exploring'])
 if c==0:
  if g.ride is not None:
   if g.maps[g.m][g.y][g.x]in '~L^':
    G_draw_map(g)
    message(["You can't get off here!"])
    G_draw_map(g,True)
    return 0
   g.ride=None
  elif d[3]==0:
   G_draw_map(g)
   message([d[0]+' is too tired.','Rest at the nest first.'])
   G_draw_map(g,True)
   return 0
  else:
   g.ride=d
 elif c in(1,2):
  return c
 G_draw_map(g)
 return 0
def G_win(g):
 cls()
 if g.pick:
  G_drag(73,30,3,g.pick[1],g.pick[6],g.pick[7],g.pick[8])
 message(['The Shadow Wyrm flies far','away. Dragons return to','every land. You did it!'],'THE END')
 G_rest(g)
 G_save(g)
