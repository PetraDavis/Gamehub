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
 if g.pol and g.pol[0]is d:
  g.pol=None
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
 top=-1
 while True:
  t=sel//10*10
  if t!=top:
   top=t
   rect(0,32,320,178,BLACK)
   for i in range(top,min(n,top+10)):
    text(30,50+(i-top)*h,opts[i],GOLD if i==sel else WHITE)
   if n>10:
    text(6,206,'More: keep going ('+str(top//10+1)+'/'+str((n+9)//10)+')',GREY)
  elif sel!=old:
   for i in(old,sel):
    y=50+(i-top)*h
    if i==old:
     rect(14,y-10,8,6,BLACK)
    text(30,y,opts[i],GOLD if i==sel else WHITE)
  rect(14,50+(sel-top)*h-10,8,6,GOLD)
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
def G_pol_off(g):
 d=g.pol[0]
 d[9]=d[9]&8|g.pol[1]
 g.pol=None
 if d in g.pen:
  message([d[0]+"'s shine",'wore off...'],'Hm')
  G_draw_map(g,True)
def G_cop(g):
 cls(G_NIGHT)
 rect(125,105,70,72,(40,60,150))
 circ(160,80,26,(240,200,160))
 rect(130,50,60,16,(20,30,80))
 rect(124,64,72,5,(20,30,80))
 rect(150,120,10,12,YELLOW)
 rect(148,78,6,4,BLACK)
 rect(166,78,6,4,BLACK)
 ctext(24,'OFFICER BRICK',GOLD)
 ctext(196,'Excuse me, tamer!')
 while wkey()not in(OK,CLR):
  pass
 message(['Have you seen a shady','merchant? Hood, yellow','eyes, sells fake stuff?'],'Officer Brick')
 g.book|=1<<30
 if choose('Tell on Shen?',['Turn him in','Never seen him'])==0:
  g.book|=1<<31
  g.coins+=300
  t=random.choice([i for i in range(20)if G_DT[i][2]==3])
  if len(g.bag)<5 and G_kids(g)+4<=40:
   g.bag.append(t)
   m="It's in your backpack."
  else:
   G_put_egg(g,t,True)
   m="I'll leave it by you."
  message(["Got him! He'll be locked","up for a long time. Here's",'300 coins and an Epic egg.'],'Officer Brick')
  message([m],'Officer Brick')
 else:
  g.book|=1<<22
  message(['Hmm. Well, tell me','if you see him.'],'Officer Brick')
 G_shen_off(g)
 if g.book>>31&1:
  g.shn=5000
def G_shen(g,ch='M',x=0):
 m,x,y=g.shen
 if g.maps[m][y][x]=='O':
  return G_cop(g)
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
 mad=g.book>>31&1
 ctext(196,random.choice(('You! You told on me!|Prices went up. Wonder why.|I remember you, snitch.'if mad else "Psst... over here.|Rare goods. Very real.|Don't ask where I got these.|Best prices in all the lands.|You look like a smart tamer.|Nice dragon. Shame if it got sparkly.").split('|')))
 while wkey()not in(OK,CLR):
  pass
 if g.book>>32&1:
  g.book&=~(1<<32)
  message(['You opened my package!','Shen always knows. Heh.',"That'll cost you."],'Shady Shen')
  if g.book>>30&1 and(not mad)and(choose('Shen wants coins',['Pay him','Threaten him'])==1):
   message(['"Don\'t charge me unless','you want to be','arrested!"'],'You')
   message(['...Fine. FINE.',"We're even.",'This time.'],'Shady Shen')
  else:
   g.coins-=min(g.coins,random.randint(20,40))
 elif met and(not g.book>>24&1)and(random.random()<0.15):
  message(['Psst... got a job. Take','this package to the',"village. And DON'T peek."],'Shady Shen')
  if choose('Take the job?',['Sure','No thanks'])==0:
   g.book|=1<<24
   message(['Someone will be waiting','there for it. Heh.'],'Shady Shen')
 free=g.book>>22&1
 if free:
  message(["Psst... you didn't tell",'the officer about me.','Pick one thing. Free.'],'Shady Shen')
 while True:
  S=(('Glimmer Stone',60),('Power Fruit',40),('Mystery Egg',50),('Healing Tonic',20),('Lucky Charm',35),('Mystery Box',30),('Egg Swap',25),('Golden Coin',45),('Accessory Crate',40),('Treasure Map',35),('Dragon Insurance',20),('Speed Saddle',50),('Shiny Polish',25),('Moldy Egg',15),('Shiny Egg',70))+((('Glimmer Pack x5',250),)if g.buys>=10 else())
  S=[(n,p*(1+mad))for n,p in S]
  z=len(S)
  c=G_zl('Pick 1 thing for FREE!'if free else 'Shady Shen   '+str(g.coins)+' coins',[n+(' - sold out'if n=='Moldy Egg'and g.book>>29&1 else ' '+str(p)+'c')for n,p in S]+(['Use Glimmer Stones ('+str(g.glim)+')']if g.glim else[])+['Leave'])
  if c==z and g.glim:
   G_glim(g)
   continue
  if c<0 or c>=z:
   message([random.choice("No refunds. Ever.|You didn't see me.|Come back soon, friend.".split('|'))],'Shady Shen')
   return
  n,p=S[c]
  p*=1-free
  if g.coins<p:
   message(["That's "+str(p)+' coins, friend.','Come back richer.'],'Shady Shen')
   continue
  d=None
  if c==1:
   d=G_who(g,'Feed the Power Fruit to',False)
   if d is None:
    continue
  if c==13 and g.book>>29&1:
   message(['All gone. Heh.',"Should've bought more",'when you had the chance.'],'Shady Shen')
   continue
  if c in(2,13,14)and(len(g.bag)>=5 or G_kids(g)+4>40):
   message(['No room for an egg.'],'Shady Shen')
   continue
  if c==6:
   if not g.bag:
    message(['You have no eggs to swap.'],'Shady Shen')
    continue
   e=G_zl('Swap which egg?',['Egg '+str(i+1)for i in range(len(g.bag))]+['Back'])
   if not 0<=e<len(g.bag):
    continue
  if c==7 and g.curse or(c==11 and g.sad):
   message(['You already have one.','One is plenty. Heh.'],'Shady Shen')
   continue
  if c==12:
   d=G_who(g,'Polish which dragon?')
   if d is None:
    continue
  g.coins-=p
  if not free and c!=13 and g.book>>28&1 and(random.random()<0.1):
   message([random.choice(('It was just a painted rock!','The box was empty...','It crumbled into dust.','It melted in your hand.'))],'Huh?')
   continue
  g.book=g.book&~(1<<22)|1<<28
  free=0
  g.buys+=1
  if g.buys==10:
   message(["Psst... you're my best","customer. Next time I'll",'have something special.'],'Shady Shen')
  if n=='Glimmer Pack x5':
   c=0
   g.glim+=4
  box=c==5
  if box:
   c=random.choice((0,1,3,4,8,20,20,21))
   d=G_grown(g)if c==1 else None
   if c==1 and d is None:
    c=20
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
  elif c==8:
   i=random.randint(1,16)
   if g.own>>i&1:
    m=['A '+G_GEAR[i][0]+'... but you','already have one.','No refunds. Heh.']
   else:
    g.own|=1<<i
    m=['A '+G_GEAR[i][0]+'!','Put it on at the','village shop.']
  elif c==9:
   if G_put_egg(g,0,False,'X'):
    m=['X marks the spot!','Look for a chest','somewhere in this land.']
   else:
    m=['The map is all smudged.',"Can't read it. Oh well."]
  elif c==10:
   m=['Your dragons are now','fully insured. Trust me.',"I'll take care of it."]
  elif c==11:
   g.sad=1
   m=['A Speed Saddle! Your','dragon flies faster now.','Zoom zoom. Heh.']
  elif c==12:
   if g.pol:
    g.pol[0][9]=g.pol[0][9]&8|g.pol[1]
   g.pol=[d,d[9]&7,random.randint(80,140)]
   d[9]=d[9]&8|random.randint(1,4)
   m=[d[0]+' sparkles!','So shiny. Totally','real. Heh heh.']
  elif c==13:
   g.book|=1<<29
   g.bag.append(random.choice([i for i in range(20)if G_DT[i][2]>=3]))
   m=['A Moldy Egg. Ew.',"It's probably rotten.",'No refunds. Heh.']
  elif c==14:
   g.bag.append(23+32*random.randint(1,4))
   m=['A Shiny Egg! Super rare.','Totally worth it.','Heh heh heh.']
  elif c==20:
   m=['The box was empty.','Just air. Heh.']
  else:
   n=random.randint(10,60)
   g.coins+=n
   m=[str(n)+' coins inside!']
  message(m,'Mystery Box'if box else n)
def G_shen_off(g):
 if g.shen:
  m,x,y=g.shen
  if g.maps[m][y][x]in 'MO':
   g.maps[m][y][x]='.'
   if m==g.m:
    G_cells(g,[(x,y)],False)
  g.shen=None
  g.shn=random.randint(120,180)
