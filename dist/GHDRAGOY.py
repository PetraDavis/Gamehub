# GHDRAGOY: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
def G_oval(x,y,s,c,k=0):
 circ(x,y+2*s,7*s-k,c)
 circ(x,y-2*s,6*s-k,c)
 circ(x,y-5*s,4*s-k,c)
def G_egg(x,y,s,t):
 q,t=(t//32,t%32)
 if t>=30:
  s=max(2,s*2//3)
  y+=2*s
  t=0
 r=max(0,G_DT[t][2])
 shell=((245,235,210),(225,240,205),(215,230,250),(235,215,250),(30,30,70),(20,20,45),(125,118,110))[r]
 if q:
  shell=G_SCH[q][2]
 G_oval(x,y,s,BLACK,-1)
 G_oval(x,y,s,dk(shell,0.7))
 G_oval(x-s,y-s,s,shell,2*s)
 if r==4:
  for dx,dy,n in((-3,-4,1),(3,3,1),(-2,5,0),(-1,-7,0),(-5,1,0),(4,-5,0)):
   rect(x+(dx-n)*s,y+dy*s,(2*n+1)*s,s,YELLOW)
   rect(x+dx*s,y+(dy-n)*s,s,(2*n+1)*s,YELLOW)
  circ(x+s,y-s,2*s,(250,230,140))
  circ(x+2*s,y-2*s,2*s,shell)
 elif r>4:
  m=(35,40,110)if r==5 else(90,84,78)
  circ(x+2*s,y+4*s,4*s,m)
  circ(x-3*s,y+1*s,2*s,m)
  Z=(-1,-8,2,-4,-2,-1,2,2,-1,5,1,8)
  for c,w in(((110,50,180),s+1),((210,150,255),max(1,s//2)))if r==5 else(((245,140,30),s+1),((250,220,60),max(1,s//2))):
   col(c)
   for i in range(0,10,2):
    ax,ay,bx,by=(x+Z[i]*s,y+Z[i+1]*s,x+Z[i+2]*s,y+Z[i+3]*s)
    fill_poly([ax-w,ax+w,bx+w,bx-w],[ay,ay,by,by])
  rect(x-5*s,y-3*s,s,s,c)
  rect(x+4*s,y-6*s,s,s,c)
 else:
  sp=G_SCH[q][3]if q else((190,150,100),(90,170,80),(60,120,230),(150,80,220))[r]
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
  v=g.bag[i]
  G_egg(40+i*60,90,3,v)
  r=G_DT[v%32%30][2]
  text(16+i*60,150,'Small'if v%32>=30 else 'Shiny'if v>31 else '???'if r>4 else G_RARE[r][:5],G_SCH[v//32][2]if v>31 else WHITE if v%32>=30 else G_RCOL[r])
 if g.glim:
  text(6,170,'Glimmer Stones: '+str(g.glim)+' (ENTER: use)',GOLD)
 if g.bag:
  text(6,188,'The first egg hatches in '+str(g.warm),WHITE)
 n=len([i for i in range(1,17)if g.own>>i&1])
 text(6,206,'Accessories: '+str(n)+' of 16',GREY)
 while True:
  k=wkey()
  if k==CLR or(k==OK and(not g.glim)):
   return False
  if k==OK:
   return True
def G_book(g):
 P=list(range(20))+[k for k in(20,21,23,24)if g.book>>k+12*(k==24)&1]
 n=len(P)
 i=0
 while True:
  cls(G_NIGHT)
  t=G_DT[P[i]]
  got=g.book>>P[i]+12*(P[i]==24)&1
  ctext(22,'DRAGON BOOK  '+str(i+1)+'/'+str(n),GOLD)
  if got:
   G_drag(102,30,2,P[i],t[3])
   ctext(150,t[0],WHITE)
   ctext(172,('Champion'if P[i]==24 else G_RARE[t[2]])+' '+G_ENAME[t[1]],G_RCOL[t[2]])
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
