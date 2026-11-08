# GHDRAGOV: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
G_VILLAGER=(('Farmer Bo',('Eggs turn up every','hundred steps or so.','Keep walking!'),('Monsters hide in the','tall grass. Ride over','it if you can.'),('The farther lands have','rarer eggs. And meaner','monsters.'),('My cow got stepped on','by a dragon. Again.')),('Baker Rose',('Walk into your nest','to heal your dragons.'),('I once saw a shiny egg.','It sparkled like sugar!'),('Small eggs hatch babies.',"So cute. Can't ride",'them, though.'),('Fresh bread! Oh, you','only have dragon food?')),('Little Pip',("When I grow up I'll",'tame a Legendary!'),('The quest hall pays','lots of coins!'),('Did you know dragons','can fly over lava?'),('Wanna see my rock?',"It's a good rock.")))
def G_deliver(g):
 message(['A hooded stranger is',"waiting for Shen's",'package.'],'Village')
 c=choose('The package',['Hand it over','Peek inside'])
 g.book&=~(1<<24)
 if c!=1:
  n=random.randint(60,120)
  g.coins+=n
  message(['He nods and pays you',str(n)+' coins. Shen keeps','his word. This time.'],'Village')
  return
 g.book|=1<<32
 r=random.random()
 if r<0.15 and len(g.bag)<5 and(G_kids(g)+4<=40):
  r=random.random()
  g.bag.append(30+32*random.randint(1,4)if r<0.08 else 30 if r<0.4 else random.choice([i for i in range(20)if G_DT[i][2]>=2])+32*random.randint(1,4))
  m=['An egg was inside! You','keep it. The stranger','runs off.']
 elif r<0.6:
  n=random.randint(30,100)
  g.coins+=n
  m=[str(n)+' coins inside!','You pocket them. The','stranger runs off.']
 else:
  m=['Just rocks!','The stranger laughs','and runs off.']
 message(m,'Package')
def G_talk(g,x):
 n,*L=G_VILLAGER[x//5%3]
 message(list(random.choice(L)),n)
def G_found(g,ch,nx,ny=0,ox=0,oy=0):
 if ch=='V':
  return G_talk(g,nx)
 if ch=='D':
  return G_deliver(g)
 mp=g.maps[g.m]
 mp[ny][nx]='.'
 G_cells(g,[(ox,oy),(nx,ny)],True)
 if ch=='E':
  e=G_EGGS.pop((g.m,nx,ny),0)
  if not g.bag:
   g.warm=12
  g.bag.append(e)
  G_hud(g)
  message(['You found a'+(' shiny'if e>31 else '')+' small egg!',"It's in your backpack."]if e%32==G_SMALL else['You found a'+(' shiny'if e>31 else 'n')+' egg with',G_RARE[G_DT[e%32][2]]+" spots! It's in",'your backpack.'],'An egg!')
 elif random.random()<0.33:
  message(['You dig it open...',"It's empty! Just dirt."],'Treasure')
 else:
  n=random.randint(30,80)+20*g.m
  g.coins+=n
  G_hud(g)
  message(['You dig it open...',str(n)+' coins inside!'],'Treasure')
