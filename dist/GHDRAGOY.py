# GHDRAGOY: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
def shuffle(a):
 for i in range(len(a)-1,0,-1):
  j=random.randint(0,i)
  a[i],a[j]=(a[j],a[i])
def sample(seq,k):
 a=list(seq)
 shuffle(a)
 return a[:k]
DEL=23
def G_oval(x,y,s,c,k=0):
 circ(x,y+2*s,7*s-k,c)
 circ(x,y-2*s,6*s-k,c)
 circ(x,y-5*s,4*s-k,c)
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
def G_backpack(g):
 cls(G_NIGHT)
 ctext(22,'BACKPACK',GOLD)
 if not g.bag:
  ctext(100,'No eggs. Go and find some!')
 for i in range(len(g.bag)):
  G_egg(40+i*60,90,3,g.bag[i])
  r=G_DT[g.bag[i]][2]
  text(16+i*60,150,'???'if r>4 else G_RARE[r][:5],G_RCOL[r])
 if g.bag:
  text(6,186,'The first egg hatches in '+str(g.warm),WHITE)
 n=len([i for i in range(1,17)if g.own>>i&1])
 text(6,204,'Accessories: '+str(n)+' of 16',GREY)
 while wkey()not in(OK,CLR):
  pass
def G_book(g):
 n=21 if g.book>>20&1 else 20
 i=0
 while True:
  cls(G_NIGHT)
  t=G_DT[i]
  got=g.book>>i&1
  ctext(22,'DRAGON BOOK  '+str(i+1)+'/'+str(n),GOLD)
  if got:
   G_drag(102,30,2,i,t[3])
   ctext(150,t[0],WHITE)
   ctext(172,G_RARE[t[2]]+' '+G_ENAME[t[1]],G_RCOL[t[2]])
  else:
   G_oval(160,90,4,(30,32,55))
   ctext(98,'?',GREY)
   ctext(150,'???',GREY)
   ctext(172,'Not found yet',GREY)
  f=len([k for k in range(20)if g.book>>k&1])
  text(6,204,'Found '+str(f)+' of 20   Left/Right',GREY)
  k=wkey()
  if k in(LEFT,RIGHT):
   i=(i+(1 if k==RIGHT else-1))%n
  elif k in(OK,CLR):
   return
def G_frame(x,y,w,h,c):
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
 G_frame(60,38,200,30,WHITE)
 for r in range(2):
  text(30,110+r*30,' '.join(G_ABC[r*13:r*13+13]),WHITE)
 text(62,179,'Delete',WHITE)
 text(208,179,'Done',WHITE)
 text(6,204,'ENTER: pick  DEL: erase',GREY)
 nm=''
 sel=old=0
 G_frame(*G_kbox(0),GOLD)
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
   G_frame(*G_kbox(old),BLACK)
   G_frame(*G_kbox(sel),GOLD)
def G_hatch(g):
 e=g.bag.pop(0)
 g.warm=12
 t=G_DT[e]
 cls(G_NIGHT)
 ctext(24,'The egg is cracking!',GOLD)
 G_egg(160,110,5,e)
 pause(0.6)
 col(WHITE if t[2]>3 else(70,45,30))
 C=(160,74,152,88,152,88,162,100,162,100,154,114,170,86,176,100,176,100,168,112)
 for i in range(0,20,4):
  a1,b1,a2,b2=C[i:i+4]
  fill_poly([a1-2,a1+2,a2+2,a2-2],[b1,b1,b2,b2])
  pause(0.25)
 cls((255,248,215))
 G_drag(73,30,3,e,t[3])
 rect(0,182,320,28,G_NIGHT)
 ctext(200,(''if t[2]>4 else G_RARE[t[2]]+' ')+t[0]+' dragon!',G_RCOL[t[2]])
 pause(1.2)
 names=sample(G_NAMES,4)
 i=choose('Name your '+t[0]+':',names+['Type a name'])
 nm=names[max(0,i)]if i<4 else G_typed(t[0])or names[0]
 mh=20+6*min(4,t[2])
 d=[nm,e,1,mh,mh,0,t[3],0,0]
 g.pen.append(d)
 msg=[nm+' joins your pen!']
 if not g.book>>e&1:
  g.book|=1<<e
  msg.append('New page in your book!')
 if g.pick is None:
  g.pick=d
  msg+=['Press ENTER to ride.','Dragons fly over water,','lava and mountains.']
 G_draw_map(g)
 message(msg,t[0])
 G_quest_step(g,1,None)
 G_draw_map(g,True)
