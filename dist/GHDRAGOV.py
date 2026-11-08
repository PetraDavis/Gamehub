# GHDRAGOV: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
G_NETTLE=((('Black as night, it was!','Came when I was young','and ate my good dragons.'),("I'd have run, but it",'had an EGG. Hee hee!')),(('Purple eyes in the dark!','It only hunts tamers','with big strong dragons.'),),(('I beat the purple-eyed','beast once. It left me','something not in books!'),),(('The cold peaks remember','a name carved in stone.','My name? No... not mine.'),),(('A giant of rock with a','heart of gold. I heard','it snore once! Hee!'),),(('Only the darkest dragon','can wake the stone one.','Remember that, dearie.'),),(('Five letters on a door,','up where the snow is.','Or was it four? Hee!'),),(('The moon owes me three',"coins. I'll get 'em."),),(('My cat is a dragon.',"Don't tell him."),),(('Who are you? Go away!','...No, come back. Sit.'),),(('I ate a rock once.','Good rock. Crunchy.'),))
G_VILLAGER=(('Farmer Bo',('Eggs turn up every','hundred steps or so.','Keep walking!'),('Monsters hide in the','tall grass. Ride over','it if you can.'),('The farther lands have','rarer eggs. And meaner','monsters.'),('My cow got stepped on','by a dragon. Again.'),('Stay away from Old','Nettle. She talks','to rocks.')),('Baker Rose',('Walk into your nest','to heal your dragons.'),('I once saw a shiny egg.','It sparkled like sugar!'),('Small eggs hatch babies.',"So cute. Can't ride",'them, though.'),('Fresh bread! Oh, you','only have dragon food?'),('Old Nettle says a black','dragon ate her dragons.','Crazy old bat!')),('Little Pip',("When I grow up I'll",'tame a Legendary!'),('The quest hall pays','lots of coins!'),('Did you know dragons','can fly over lava?'),('Wanna see my rock?',"It's a good rock."),('Mom says Old Nettle is','cuckoo. Her hut is the','purple one.')))
def G_deliver(g):
 message(['A hooded stranger is',"waiting for Shen's",'package.'],'Village')
 c=choose('The package',['Hand it over','Peek inside'])
 g.book&=~(1<<24)
 if c==1:
  r=random.random()
  e=n=0
  if r<0.15:
   r=random.random()
   e=30+32*random.randint(1,4)if r<0.08 else 30 if r<0.4 else random.choice([i for i in range(20)if G_DT[i][2]>=2])+32*random.randint(1,4)
   m=["An egg! It's a"+(' small'if e%32==30 else ''),('shiny 'if e>31 else '')+'egg, wow.']
  elif r<0.6:
   n=random.randint(30,100)
   m=[str(n)+' coins!']
  else:
   m=None
  if m:
   message(['You peek inside...']+m,'Package')
   if e and(len(g.bag)>=5 or G_kids(g)+4>40):
    message(['No room for an egg.','You close the package.'],'Package')
   elif choose('Take it?',['Take it','Leave it'])==0:
    g.book|=1<<32
    g.coins+=n
    if e:
     g.bag.append(e)
    message(['You take it. The','stranger snatches the','package and runs off.'],'Package')
    return
  else:
   message(['You peek inside...','Just rocks!','You close it up again.'],'Package')
 n=random.randint(60,120)
 g.coins+=n
 message(['He nods and pays you',str(n)+' coins. Shen keeps','his word. This time.'],'Village')
def G_talk(g,x):
 n,*L=G_VILLAGER[x//5%3]
 message(list(random.choice(L)),n)
def G_nettle(g):
 cls(G_NIGHT)
 col((110,50,140))
 fill_poly([125,160,200],[200,80,200])
 circ(150,70,20,WHITE)
 circ(132,60,10,WHITE)
 circ(168,58,10,WHITE)
 circ(150,78,15,(225,190,160))
 rect(143,76,4,3,BLACK)
 rect(155,76,4,3,BLACK)
 rect(205,110,4,90,G_BARK)
 rect(196,106,13,4,G_BARK)
 ctext(24,'OLD NETTLE',GOLD)
 ctext(196,"Eh? Who's there?")
 while wkey()not in(OK,CLR):
  pass
 k=[d[1]for d in g.pen]
 if 20 in k and(not g.book>>33&1):
  g.book|=1<<33
  P=(('THE BLACK DRAGON!','I TOLD them! Nobody','believed old Nettle!'),('Take my old crown,','dearie. I kept it','for this day.'))
  if g.own>>4&1:
   g.coins+=150
  g.own|=1<<4
 elif 21 in k and(not g.book>>34&1):
  g.book|=1<<34
  P=(('The stone one... AWAKE!','Hee hee hee! I KNEW it!'),('Take these shiny',"stones. Five of 'em.",'No use to me.'))
  g.glim+=5
 else:
  P=random.choice(G_NETTLE)
 for p in P:
  message(list(p),'Old Nettle')
def G_found(g,ch,nx,ny=0,ox=0,oy=0):
 if ch=='V':
  return G_talk(g,nx)
 if ch=='N':
  return G_nettle(g)
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
