# GHDRAGOS: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
def sample(seq,k):
 a=list(seq)
 shuffle(a)
 return a[:k]
DEL=23
def G_frame(b,c):
 x,y,w,h=b
 rect(x,y,w,2,c)
 rect(x,y+h-2,w,2,c)
 rect(x,y,2,h,c)
 rect(x+w-2,y,2,h,c)
def G_kbox(i):
 if i<26:
  return(26+i%13*20,92+i//13*30,18,24)
 return(52,160,80,26)if i==26 else(188,160,80,26)
def G_typed(kind):
 cls()
 ctext(24,'Name your '+kind,GOLD)
 G_frame((60,38,200,30),WHITE)
 for r in range(2):
  text(30,110+r*30,' '.join(G_ABC[r*13:r*13+13]),WHITE)
 text(62,179,'Delete',WHITE)
 text(208,179,'Done',WHITE)
 text(6,204,'ENTER: pick  DEL: erase',GREY)
 nm=''
 sel=old=0
 G_frame(G_kbox(0),GOLD)
 while True:
  k=wkey()
  old=sel
  if k==LEFT:
   sel=(sel-1)%28
  elif k==RIGHT:
   sel=(sel+1)%28
  elif k==UP:
   sel=sel-13 if 13<=sel<26 else(13 if sel==26 else 20)if sel>25 else sel+13
  elif k==DOWN:
   sel=sel+13 if sel<13 else(26 if sel<19 else 27)if sel<26 else sel-13
  elif k==CLR:
   return ''
  elif k==DEL or(k==OK and sel==26):
   nm=nm[:-1]
  elif k==OK and sel==27:
   if nm:
    return nm
  elif k==OK and len(nm)<8:
   nm+=G_ABC[sel]if not nm else G_ABC[sel].lower()
  if k in(OK,DEL):
   rect(64,42,192,22,BLACK)
   text(70,62,nm+('_'if len(nm)<8 else ''),WHITE)
  if sel!=old:
   G_frame(G_kbox(old),BLACK)
   G_frame(G_kbox(sel),GOLD)
def G_hatch(g):
 v=g.bag.pop(0)
 g.warm=12
 q,e=(v//32,v%32)
 q*=e!=23
 b=e>=30
 if b:
  e=random.choice([i for i in range(20)if G_DT[i][2]>=2]if e==30 else[i for i in range(22)if g.book>>i&1]or[0])
 t=G_DT[e]
 cls(G_NIGHT)
 ctext(24,'The egg is cracking!',GOLD)
 G_egg(160,110,5,v)
 pause(0.6)
 col(WHITE if t[2]>3 else(70,45,30))
 C=(160,74,152,88,152,88,162,100,162,100,154,114,170,86,176,100,176,100,168,112)
 for i in range(0,20,4):
  a1,b1,a2,b2=C[i:i+4]
  fill_poly([a1-2,a1+2,a2+2,a2-2],[b1,b1,b2,b2])
  pause(0.25)
 cls((255,248,215))
 if b:
  G_drag(102,55,2,e,t[3],0,0,None,0,q)
 else:
  G_drag(73,30,3,e,t[3],0,0,None,0,q)
 rect(0,182,320,28,G_NIGHT)
 ctext(200,'A baby '+(G_SCH[q][0]+' 'if q else '')+t[0]+'!'if b else(G_SCH[q][0]+' 'if q else ''if t[2]>4 else('Champion'if e==24 else G_RARE[t[2]])+' ')+t[0]+' dragon!',G_SCH[q][2]if q else G_RCOL[t[2]])
 pause(1.2)
 names=sample(G_NAMES,4)
 i=choose('Name your '+t[0]+':',names+['Type a name'])
 nm=names[max(0,i)]if i<4 else G_typed(t[0])or names[0]
 mh=20+6*min(4,t[2])+6*(e==20)+16*(e==21)+3*(e==24)
 d=[nm,e,1,mh,mh,0,t[3],0,0,q+8*b]
 g.pen.append(d)
 msg=[nm+' joins your pen!']
 e+=12*(e==24)
 if not g.book>>e&1:
  g.book|=1<<e
  msg.append('New page in your book!')
 if g.pick is None and(not b):
  g.pick=d
  msg+=['Press ENTER to ride.','Dragons fly over water,','lava and mountains.']
 G_draw_map(g)
 message(msg,t[0])
 G_quest_step(g,1,None)
 G_draw_map(g,True)
def G_menu(g):
 d=g.pick
 opts=['Backpack','Dragon book','My quest','Save game','Keep exploring']
 if d is None:
  c=choose('Dragon Tamer',opts)
  c=c+1 if c>=0 else 5
 else:
  if g.ride is not None:
   first='Get off '+d[0]
  else:
   first='Ride '+d[0]+(''if d[3]>0 else ' (tired)')
  c=choose(d[0]+' the '+G_DT[d[1]][0],[first]+opts)
 if c==3:
  q=g.quest
  G_draw_map(g)
  if q is None:
   message(['You have no quest.','Visit the quest hall','in the village.'],'My quest')
  else:
   message([q[5],'Done: '+str(q[3])+' of '+str(q[2]),'Reward: '+str(q[4])+' coins'],'My quest')
  G_draw_map(g,True)
  return 0
 if c==4:
  G_save(g)
  G_draw_map(g)
  message(['Your dragons, coins and','eggs are saved.'],'Saved!')
  G_draw_map(g,True)
  return 0
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
