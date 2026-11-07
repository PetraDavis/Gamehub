# GHDRAGOB: part of GHDRAGOP. Keep it next to GHDRAGOP.
from GHDRAGOC import*
UP=25
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
G_MAPS=(['TTTTTTTTTTTTT~~~','T.....""".....~~','T.H...""""...~~~','T.....""".T...~~','T..........E.~~~','T....TT.......~~','T.""".TT......~~','T.""".........~~','TTTTTTTTTTTTTT~~'],['~^^^^^^^^^^^^^^^','~...""""..LLL..^','~..^"""..LLELL.^','~.....^...LLL...','~...............','~...^^...."""...','~..LL....."""..^','~.....^^.......^','~^^^^^^^^^^^^^^^'],['^^^^^^^^^^^^^^^^','...""".....^E^^^','...........^^^^^','......~~~~......','....~~~~B~~~....','.....~~~~~......','.."""...........','..""".....^^....','^^^^^^^^^^^^^^^^'])
G_GEAR=(('',0),('Bow',15),('Goggles',25),('Wizard hat',40),('Crown',80),('Party hat',20),('Top hat',35),('Flower',15),('Viking helmet',60),('Scarf',15),('Saddle',25),('Cape',40),('Armor',60),('Bell collar',20),('Backpack',30),('Flag',45),('Necklace',50))
G_FOES=((('Goblin',14,4,6,(110,160,60),3),('Bog Toad',16,4,7,(60,120,160),1)),(('Lava Imp',26,7,12,(240,120,30),0),('Rock Troll',32,7,14,(120,110,90),2)),(('Ice Wraith',34,9,16,(150,200,240),1),('Snow Yeti',42,9,18,(235,235,245),3)))
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
def G_battle(g,f):
 name,fhp,fat,xp,fc,fe=f
 mx=fhp
 G_foe_screen(f,name+' appears!')
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
   text(12,56,now[0],d[6]if d and d[1]!=19 else WHITE)
   text(12,86,name[:12],RED if f is G_DREAD else fc)
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
    G_foe_screen(f,name)
    was=None
  else:
   g.hp-=dm
   if g.hp<=0:
    cls()
    ctext(60,'YOU DIED',RED)
    message(['The '+name+' won.','Back to your last save','at the nest.'],'Game over')
    return False
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
 message(['The Dread Drake flies','away... and leaves its','QUANTUM EGG behind!'],'Whoa!')
 G_draw_map(g,True)
 return True
