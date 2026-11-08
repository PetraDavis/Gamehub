# GHDRAGOZ: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
def G_who(g,title,babies=True):
 L=[d for d in g.pen if babies or not d[9]&8]
 pg=0
 while L:
  sh=L[pg:pg+9]
  more=len(L)>9
  c=G_zl(title,[d[0]+' '+G_DT[d[1]][0]for d in sh]+(['More...']if more else[])+['Back'])
  if more and c==len(sh):
   pg=pg+9 if pg+9<len(L)else 0
   continue
  return sh[c]if 0<=c<len(sh)else None
 message(['You need a dragon first.'],'Hm')
 return None
def G_glim(g):
 d=G_who(g,'Make shiny ('+str(g.glim)+' stones)')
 if d is None:
  return
 q=0
 if g.glim>=5:
  c=choose('Glimmer Stones: '+str(g.glim),['Random (1 stone)','Pick colour (5)','Back'])
  if c==1:
   q=choose('Which shiny?',[G_SCH[i][0]for i in range(1,5)])+1
   if q<1:
    return
   g.glim-=5
  elif c!=0:
   return
 if not q:
  g.glim-=1
  q=random.randint(1,4)
 d[9]=d[9]&8|q
 d[6]=G_DT[d[1]][3]
 cls(G_NIGHT)
 G_drag(102,10,2,d[1],d[6],d[7],d[8],None,0,q)if not d[9]&8 else G_drag(131,45,1,d[1],d[6],0,0,None,0,q)
 message([d[0]+' sparkles!','Now a '+G_SCH[q][0]+' '+G_DT[d[1]][0]+'!'],'Shiny!')
 G_save(g)
def G_zl(title,opts):
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
def G_shen(g):
 met=g.book>>27&1
 g.book|=1<<27
 if met and random.random()<0.25+0.25*g.curse:
  g.coins-=min(g.coins,random.randint(2,6)*(1+g.curse))
 cls(G_NIGHT)
 col((70,45,95))
 fill_poly([110,160,210],[200,40,200])
 circ(160,95,22,(15,10,20))
 rect(148,90,6,4,YELLOW)
 rect(166,90,6,4,YELLOW)
 circ(222,170,20,(150,105,55))
 rect(214,150,16,4,(110,75,40))
 ctext(24,'SHADY SHEN',GOLD)
 ctext(196,random.choice(('Psst... over here.','Rare goods. Very real.',"Don't ask where I got these.",'Best prices in all the lands.','You look like a smart tamer.','Nice dragon. Shame if it got sparkly.')))
 while wkey()not in(OK,CLR):
  pass
 while True:
  S=(('Glimmer Stone',60),('Power Fruit',40),('Mystery Egg',50),('Healing Tonic',20),('Lucky Charm',35),('Mystery Box',30),('Egg Swap',25),('Golden Coin',45))+((('Glimmer Pack x5',250),)if g.buys>=10 else())
  z=len(S)
  c=G_zl('Shady Shen   '+str(g.coins)+' coins',[n+' '+str(p)+'c'for n,p in S]+(['Use Glimmer Stones ('+str(g.glim)+')']if g.glim else[])+['Leave'])
  if c==z and g.glim:
   G_glim(g)
   continue
  if c<0 or c>=z:
   message([random.choice(('No refunds. Ever.',"You didn't see me.",'Come back soon, friend.'))],'Shady Shen')
   return
  n,p=S[c]
  if g.coins<p:
   message(["That's "+str(p)+' coins, friend.','Come back richer.'],'Shady Shen')
   continue
  d=None
  if c==1:
   d=G_who(g,'Feed the Power Fruit to',False)
   if d is None:
    continue
  if c==2 and(len(g.bag)>=5 or G_kids(g)+4>40):
   message(['No room for an egg.'],'Shady Shen')
   continue
  if c==6:
   if not g.bag:
    message(['You have no eggs to swap.'],'Shady Shen')
    continue
   e=G_zl('Swap which egg?',['Egg '+str(i+1)for i in range(len(g.bag))]+['Back'])
   if not 0<=e<len(g.bag):
    continue
  if c==7 and g.curse:
   message(['You already have one.','One is plenty. Heh.'],'Shady Shen')
   continue
  g.coins-=p
  if g.book>>28&1 and random.random()<0.1:
   message([random.choice(('It was just a painted rock!','The box was empty...','It crumbled into dust.','It melted in your hand.'))],'Huh?')
   continue
  g.book|=1<<28
  g.buys+=1
  if g.buys==10:
   message(["Psst... you're my best","customer. Next time I'll",'have something special.'],'Shady Shen')
  if c==8:
   c=0
   g.glim+=4
  if c==5:
   c=random.choice((0,1,3,4,9,9,10))
   d=G_grown(g)if c==1 else None
   if c==1 and d is None:
    c=9
  if c==0:
   g.glim+=1
   m=['Glimmer Stones: '+str(g.glim),'Use 1 for a random shiny,','or 5 to pick the colour.']
  elif c==1:
   d[2]+=1
   d[4]+=6
   d[3]=d[4]
   m=[d[0]+' ate the Power Fruit.',d[0]+' is now level '+str(d[2])+'!']
  elif c==2:
   g.bag.append(G_egg_roll(g,random.randint(0,19)))
   m=['A Mystery Egg!',"It's in your backpack."]
  elif c==3:
   g.hp=g.mhp
   for dd in g.pen:
    dd[3]=dd[4]
   m=['Everyone feels great!']
  elif c==4:
   g.luck=1
   g.spawn=min(g.spawn,40)
   m=['You feel lucky.','Your next egg will','be a rare one!']
  elif c==6:
   g.bag[e]=G_egg_roll(g,G_egg_type(g.m))
   m=['Swapped! A brand new','egg is in your backpack.']
  elif c==7:
   g.curse=1
   m=['A Golden Coin! Double','coins from fights.','Lucky you. Heh heh.']
  elif c==9:
   m=['The box was empty.','Just air. Heh.']
  else:
   n=random.randint(10,60)
   g.coins+=n
   m=[str(n)+' coins inside!']
  message(m,n if c<9 else 'Mystery Box')
def G_shen_off(g):
 if g.shen:
  m,x,y=g.shen
  if g.maps[m][y][x]=='M':
   g.maps[m][y][x]='.'
   if m==g.m:
    G_cells(g,[(x,y)],False)
  g.shen=None
  g.shn=random.randint(120,180)
