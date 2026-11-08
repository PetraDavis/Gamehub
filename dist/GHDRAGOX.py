# GHDRAGOX: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
def G_unpack(n):
 nm=''
 while n:
  nm=G_ABC[n%27-1]+nm
  n//=27
 return nm[0]+nm[1:].lower()
G_PAINTN=('Red','Blue','Green','Gold','Purple','Pink','Black','White')
G_MAPS=(['TTTTTTTTTTTTT~~~','T.....""".....~~','T.H...""""...~~~','T.....""".T...~~','...........E.~~~','T....TT.......~~','T.""".TT......~~','T.""".........~~','TTTTTTTTTTTTTT~~'],['~^^^^^^^^^^^^^^^','~...""""..LLL..^','~..^"""..LLELL.^','~.....^...LLL...','~...............','~...^^...."""...','~..LL....."""..^','~.....^^.......^','~^^^^^^^^^^^^^^^'],['^^^^^^^^^^^^^^^^','...""".....^E^^^','...........^^^^^','......~~~~......','....~~~~B~~~....','.....~~~~~......','.."""...........','..""".....^C....','^^^^^^^^^^^^^^^^'],['TTTTTTTTTTTTTTTT','T.....A......N.T','T..Q.......S...T','T..=.......=...T','T..=============','T.......W......T','T.....V......V.T','T.V............T','TTTTTTTTTTTTTTTT'])
def G_load(g):
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
 g.bag=[]
 g.warm=12
 g.spawn=100
 g.pick=g.ride=g.quest=g.pol=g.shen=None
 g.deck={}
 g.coins=g.own=g.book=g.seen=g.face=g.dread=g.glim=g.luck=g.curse=g.buys=g.done=g.cd=g.sad=g.ar=0
 g.shn=random.randint(120,180)
 try:
  from ti_system import recall_list
  s=[int(v)for v in recall_list('DRG')]
 except Exception:
  return
 if len(s)<9 or s[0]not in(2,3,4):
  return
 v=s[0]
 k=min(1,v-2)
 pk=0
 g.coins,g.own,g.book=(s[1],s[2],s[3])
 if k:
  g.dread=s[4]
 g.bag=[e for e in s[4+k:9+k]if e>=0]
 w=5 if v>3 else 4
 for i in range(9+k,len(s)-w+1,w):
  if v>3:
   nm=G_unpack(s[i])
   i+=1
   t=s[i]
  else:
   nm,t=(G_NAMES[s[i]//32],s[i]%32)
  lv=s[i+1]
  mh=20+6*min(4,G_DT[t][2])+6*(lv-1)+6*(t==20)+16*(t==21)+3*(t==24)
  x=s[i+3]%4000
  p=x//200
  g.pen.append([nm,t,lv,mh,mh,s[i+2],G_PAINT[p-1]if p else G_DT[t][3],x//20%10,x%20,s[i+3]//4000])
 try:
  b=[int(v)for v in recall_list('DRB')]
  if b[0]>2:
   g.ar=b.pop(2)
  if b[0]>1:
   pk=b[1]//500000%12
   g.cd=b[1]//6000000%16
   g.sad=b[1]//96000000%2
   g.shn=max(g.shn,b[1]//192000000*100)
   b[1]%=500000
   g.glim,g.luck,g.curse,g.buys,g.done=(b[1]%100,b[1]//100%2,b[1]//200%2,b[1]//400%11,b[1]//4400)
   b=b[1:]
  for i in range(1,len(b)-1,2):
   t=b[i+1]%32
   g.pen.append([G_unpack(b[i]),t,1,10,10,0,G_DT[t][3],0,0,8+b[i+1]//32])
 except Exception:
  pass
 big=[d for d in g.pen if not d[9]&8]
 g.pick=big[pk]if pk<len(big)else G_grown(g)
 g.warm=12
def G_new_quest(g):
 t=min(10,g.done)
 m=1+0.3*t
 k=random.randint(0,2)
 if k==0:
  n=random.randint(2,4)+t//2
  land=random.randint(min(g.seen,t//3),g.seen)
  nm=random.choice(G_FOES[land])[0]
  return[0,nm,n,0,int((8*n+6*land)*m),'Beat '+str(n)+' '+nm+'s']
 if k==1:
  n=1+t//3
  return[1,None,n,0,int(20*n*m),'Hatch '+(str(n)+' eggs'if n>1 else 'an egg')]
 land=random.randint(min(g.seen,t//3),g.seen)
 n=random.randint(3,5)+t//2
 return[2,land,n,0,int((7*n+6*land)*m),str(n)+' wins: '+G_LANDS[land]]
def G_board(g):
 if g.quest is not None:
  q=g.quest
  c=choose(q[5]+' '+str(q[3])+'/'+str(q[2]),['Keep going','Give up quest'])
  if c==1:
   g.quest=None
  return
 qs=[G_new_quest(g)for i in range(3)]
 c=G_lst('Quests (level '+str(min(10,g.done)+1)+')',[q[5]+'  '+str(q[4])+'c'for q in qs]+['Not now'])
 if 0<=c<3:
  g.quest=qs[c]
def G_portrait(d):
 cls(G_NIGHT)
 if d[9]&8:
  G_drag(131,45,1,d[1],d[6],d[7],d[8],None,0,d[9]&7)
 else:
  G_drag(102,10,2,d[1],d[6],d[7],d[8],None,0,d[9]&7)
def G_pen(g):
 pg=0
 while g.pen:
  k=G_kids(g)
  top=pg*9
  sh=g.pen[top:top+9]
  opts=[('> 'if d is g.pick else '')+d[0]+(' baby'if d[9]&8 else ' L'+str(d[2]))+' '+G_DT[d[1]][0]for d in sh]
  more=len(g.pen)>9
  c=G_lst('Pen '+str(k//4)+('','.25','.5','.75')[k%4]+'/10',opts+(['More...']if more else[])+['Back'])
  if more and c==len(sh):
   pg=pg+1 if(pg+1)*9<len(g.pen)else 0
   continue
  if c<0 or c>=len(sh):
   return
  d=sh[c]
  b=d[9]&8
  a=choose(d[0]+' the '+('baby 'if b else '')+G_DT[d[1]][0],['Pick as partner','See '+d[0],'Let it go free','Back'])
  if a==0 and b:
   message([d[0]+' is too little to','ride or fight. Babies','just live in your pen.'],'Baby')
  elif a==0:
   g.pick=d
   if g.ride is not None:
    g.ride=d
   message([d[0]+' is your partner now!'],'Partner')
  elif a==1:
   t=G_DT[d[1]]
   G_portrait(d)
   q=d[9]&7
   ctext(122,d[0],GOLD)
   ctext(142,(G_SCH[q][0]+' 'if q else '')+t[0])
   ctext(160,('Champion'if d[1]==24 else G_RARE[t[2]])+'  '+G_ENAME[t[1]]+' element')
   ctext(178,'A baby'if b else 'Level '+str(d[2])+'  HP '+str(d[4]))
   ctext(200,'ENTER: back',GREY)
   while wkey()not in(OK,CLR):
    pass
  elif a==2 and choose('Free '+d[0]+' forever?',['No, keep '+d[0],'Yes, let it go'])==1:
   g.pen.remove(d)
   if g.pick is d:
    g.pick=G_grown(g)
   if g.ride is d:
    g.ride=g.pick
   message([d[0]+' flies away. Bye!'],'Free')
def G_lst(title,opts):
 cls()
 ctext(24,title,GOLD)
 n=len(opts)
 h=15 if n>9 else 17
 sel=old=0
 for i in range(n):
  text(30,50+i*h,opts[i],GOLD if i==0 else WHITE)
 while True:
  if sel!=old:
   for i in(old,sel):
    rect(0,50+i*h-16,320,h,BLACK)
    text(30,50+i*h,opts[i],GOLD if i==sel else WHITE)
  rect(14,50+sel*h-10,8,6,GOLD)
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
  elif c==3 and d[9]&7:
   message(['Shiny dragons keep','their special colours.'],'Paint')
  elif c==3:
   if g.coins<20:
    message(['You need 20 coins.'],'Not enough')
    continue
   p=G_lst('Pick a colour',list(G_PAINTN))
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
  c=choose('The Nest (saved)',['Dragon pen','Backpack and book','Leave the nest']+(['Glimmer Stones: '+str(g.glim)]if g.glim else[]))
  if c==3:
   return 3
  elif c==0:
   G_pen(g)
  elif c==1:
   k=choose('Look at your',['Backpack','Dragon book'])
   if k>=0:
    return k+1
  else:
   G_save(g)
   return 0
def G_win(g):
 cls()
 if g.pick:
  G_drag(73,30,3,g.pick[1],g.pick[6],g.pick[7],g.pick[8],None,0,g.pick[9]&7)
 message(['The Shadow Wyrm flies far','away. Dragons return to','every land. You did it!'],'THE END')
 G_rest(g)
 G_save(g)
