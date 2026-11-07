# GHDRAGOB: part of GHDRAGOP. Keep it next to GHDRAGOP.
from GHDRAGOC import*
UP=25
def message(lines,title=None):
 n=len(lines)+(1 if title else 0)
 h=n*18+30
 y=(H-h)//2
 rbox(20,y,280,h,8,WHITE)
 MSG[0],MSG[1]=(y,h)
 COVER[0]+=1
 yy=y+24
 if title:
  ctext(yy,title,GOLD)
  yy+=18
 for s in lines:
  ctext(yy,s)
  yy+=18
 while True:
  k=wkey()
  if k in(OK,CLR):
   return k
G_LANDS=('Green Valley','Fire Mountain','Frost Peaks','Village')
G_ARTF=(b'\x02\x036\x1e<\x10@\x1e\x02\x029\x1e<\x15>\x1e',b'\x00\x10\x1e\x1d\x02\x02\x00\x00\x00\x10$\x1e\x02\x02\x00\x00\x00\x10+\x1d\x02\x02\x00\x00',b'\x02\x0f.\x1c3\x156\x1d\x02\x100\x1c3\x175\x1d\x01\x0e\x1e\x1d\x01\x00\x00\x00\x01\x0e#\x1c\x01\x00\x00\x00\x01\x0e)\x1d\x01\x00\x00\x00',b'\x00\x01\x16\x1c\x07\x02\x00\x00\x00\x01\x1d\x1d\x07\x02\x00\x00\x00\x01$\x1c\x08\x02\x00\x00\x00\x01,\x1d\x04\x01\x00\x00',b'',b'\x00\x07\x1a\x1b\x05\x03\x00\x00\x00\x07#\x1e\x05\x02\x00\x00\x00\x07+\x1c\x03\x02\x00\x00\x00\x070\x1d\x03\x02\x00\x00',b'\x01\x05-\x1b\x02\x00\x00\x00\x01\x051\x1c\x02\x00\x00\x00\x01\x055\x1e\x01\x00\x00\x00\x01\x05\x1e\x1e\x02\x00\x00\x00\x01\x05&\x1f\x02\x00\x00\x00\x01\x06\x1e\x1d\x01\x00\x00\x00\x01\x06&\x1e\x01\x00\x00\x00',b'\x00\x03\x19\x1c\x06\x01\x00\x00\x00\x03\x1e\x1c\x01\x04\x00\x00\x00\x03#\x1b\x01\x05\x00\x00\x00\x03#\x1f\x06\x01\x00\x00\x00\x03,\x1d\x05\x01\x00\x00',b'',b'\x02\x01\x1d\x19\x1f\x13!\x19\x02\x01+\x1b-\x16/\x1c\x02\x010\x1d2\x184\x1e',b'',b'\x02\x10\x1d\x19\x1f\x14!\x19\x02\x10+\x1b-\x16/\x1c\x02\x100\x1d2\x184\x1e',b'',b'',b'\x00\x1e\x1c\x1d\x02\x01\x00\x00\x00\x1e"\x1e\x02\x01\x00\x00\x00\x1e(\x1d\x02\x01\x00\x00',b'',b'\x02\x035\x1e;\rA\x1e\x02\x028\x1e;\x13>\x1e',b'\x02\x0f)\x1a,\x14/\x1b\x02\x0f0\x1d4\x176\x1e\x01\x0b\x1d\x1d\x01\x00\x00\x00\x01\x0b#\x1e\x01\x00\x00\x00\x01\x0b*\x1d\x01\x00\x00\x00',b'\x00\x10\x1c\x1a\x01\x08\x00\x00\x00\x10!\x1a\x01\x08\x00\x00\x00\x10&\x1a\x01\x08\x00\x00\x00\x10-\x1c\x01\x04\x00\x00',b'',b'\x00\x00"\x19\x07\n\x00\x00\x01\x00)\x1e\x05\x00\x00\x00\x02\x00)\x1a9\x1f)#\x02\x12*\x1b-\x14/\x1c\x02\x120\x1d3\x175\x1e\x02\x16+\x1b-\x14.\x1b\x02\x161\x1d3\x174\x1d\x02\x16\x12\x10\x19\n\x15\x12\x00\x16\x11\x18\x02\x06\x00\x00\x00\x16\x19\x1d\x08\x01\x00\x00\x00\x16 \x1d\x01\x03\x00\x00\x00\x16 \x1f\t\x01\x00\x00\x00\x16)\x1c\x01\x04\x00\x00\x00\x16.\x1d\x07\x01\x00\x00',b"\x00\x10\x1b\x1a\x05\x03\x00\x00\x00\x10#\x1e\x05\x03\x00\x00\x00\x10,\x1c\x04\x02\x00\x00\x02\x10\x12\x16\x16\x15\x14\x1a\x02\x13\x13\x15\x15\r\x18\x15\x02\x13\x17\x17\x1a\x10\x1c\x18\x02\x13*\x1b-\x120\x1c\x02\x130\x1d3\x156\x1e\x02\x135\x1e7\x199\x1e\x02\x01\x14\x15\x15\r\x15\x15\x02\x01+\x1a-\x12-\x1a\x02\x011\x1c3\x153\x1c\x00\x03\x19\x1d\x07\x01\x00\x00\x00\x03\x1f\x1d\x01\x04\x00\x00\x00\x03\x1f \x08\x01\x00\x00\x00\x03'\x1c\x01\x05\x00\x00\x00\x03'\x1c\x07\x01\x00\x00\x00\x03.\x1d\x01\x02\x00\x00\x00\x03\x11\x17\x01\x05\x00\x00\x00\x03\x11\x17\x03\x01\x00\x00\x00\x02\x1a\x1d\x05\x01\x00\x00\x00\x02  \x06\x01\x00\x00\x00\x02(\x1c\x05\x01\x00\x00",b'\x02\x17\x1c\x19\x1e\x13 \x19\x02\x17+\x1b-\x150\x1c\x02\x171\x1d3\x186\x1e\x02\x17\x13\x14\x15\x0f\x18\x14\x00\x19\x18 \x13\x03\x00\x00\x00\x17\x11\x18\x02\x06\x00\x00')
G_FOES=((('Goblin',14,4,6,(110,160,60),3),('Bog Toad',16,4,7,(60,120,160),1)),(('Lava Imp',26,7,12,(240,120,30),0),('Rock Troll',32,7,14,(120,110,90),2)),(('Ice Wraith',34,9,16,(150,200,240),1),('Snow Yeti',42,9,18,(235,235,245),3)))
def G_drag(x,y,s,t,c,head=0,body=0,out=None,f=0,sp=0):
 P=G_PAL+[lt(c,0.45),dk(c,0.6),c]+G_PAL2+[lt(c,0.2),dk(c,0.4)]+G_PAL3
 if sp:
  bl=(c[0]*3+c[1]*6+c[2])//10
  n,c,l,k,a=G_SCH[sp]
  Q=[dk(k,0.5),P[1]]
  for q in P[2:]:
   v=(q[0]*3+q[1]*6+q[2])//10
   Q.append(l if v>200 else a if max(q)-min(q)>110 else l if v>165 else dk(k,0.5)if v<40 else l if v>bl else k)
  P=Q
  P[15],P[16],P[17],P[24],P[25]=(l,k,c,l,k)
  if t==21:
   P[2],P[5],P[6],P[19]=(l,c,l,a)
 w,b=(G_ARTW[2*t],G_ARTW[2*t+1])
 r=G_DT[t][2]if t<len(G_DT)else 0
 for a in(G_ARTB,G_ARTF[t],G_ARTU[r],bytes((2,w,24,26,40,10,37,28,2,b,40,10,28,27,30,27,2,b,40,10,33,28,35,28,2,17,23,26,40,9,26,26,1,17,26,27,3,0,0,0,2,1,40,9,42,7,41,11)),G_ARTL,G_ARTT[r],G_ARTO[t],G_ARTG[body]if body else b'',G_ARTG[head]if head else b'',bytes((0,1,17,31,5,1,0,0,0,1,19,29,1,5,0,0,0,1,34,14,5,1,0,0,0,1,36,12,1,5,0,0,0,1,41,32,5,1,0,0,0,1,43,30,1,5,0,0))if sp else b''):
  G_art(a,x,y,s,P,out,f)
def G_shapes(m,x,y,ch,out):
 px=x*G_T
 py=20+y*G_T
 if ch=='T':
  out.append((0,G_BARK,0,(px+8,py+14,4,6)))
  out.append((1,G_LEAF,1,(px+10,py+8,8)))
 elif ch=='~':
  out.append((0,(110,160,235),0,(px+(x*5+y*3)%8,py+8,6,1)))
 elif ch=='L':
  out.append((0,(250,200,60),0,(px+(x*7+y*5)%12,py+6,5,3)))
 elif ch=='"':
  c=G_GROUND[m]
  for o in(3,9,15):
   out.append((0,c,0,(px+o,py+6+o%4,2,8)))
 elif ch in '^C':
  out.append((0,G_ROCK,2,([px,px+10,px+20],[py+20,py+1,py+20])))
  out.append((1,WHITE,2,([px+6,px+10,px+14],[py+8,py+1,py+8])))
  if ch=='C'and G_CAVE[0]:
   out.append((2,(20,18,25),1,(px+10,py+17,5)))
   out.append((3,YELLOW,0,(px+8,py+9,5,1)))
 elif ch in 'QS':
  out.append((0,(235,215,170),0,(px+3,py+9,14,11)))
  out.append((1,(200,50,40)if ch=='Q'else(50,90,200),2,([px,px+10,px+20],[py+10,py,py+10])))
  out.append((2,G_BARK,0,(px+8,py+13,4,7)))
  if ch=='Q':
   out.append((3,YELLOW,0,(px+9,py+3,2,4)))
   out.append((3,YELLOW,0,(px+9,py+8,2,1)))
  else:
   out.append((3,YELLOW,1,(px+10,py+5,2)))
 elif ch=='M':
  out.append((0,(70,45,95),2,([px+3,px+10,px+17],[py+19,py+2,py+19])))
  out.append((1,(15,10,20),1,(px+10,py+8,3)))
  out.append((1,(150,105,55),1,(px+16,py+15,3)))
  out.append((2,YELLOW,0,(px+8,py+7,1,1)))
  out.append((2,YELLOW,0,(px+11,py+7,1,1)))
 elif ch=='W':
  out.append((0,G_ROCK,1,(px+10,py+11,8)))
  out.append((1,G_WATER,1,(px+10,py+11,5)))
 elif ch=='H':
  out.append((0,G_BARK,1,(px+10,py+12,9)))
  out.append((1,(60,40,20),1,(px+10,py+12,6)))
  out.append((2,(245,235,210),1,(px+7,py+12,3)))
  out.append((2,(245,235,210),1,(px+13,py+11,3)))
  out.append((3,(200,160,90),0,(px+1,py+15,18,2)))
 elif ch=='E':
  v=G_EGGS.get((m,x,y),0)
  q,k=(v//32,v%32)
  r=G_DT[k%G_SMALL][2]
  sh=G_SCH[q][2]if q else(25,25,35)if r==4 else G_CYAN if r==5 else G_ROCK if r==6 else(245,235,210)
  sp=G_SCH[q][3]if q else G_MAG if r==5 else YELLOW if r>=4 else G_RCOL[r]if r else(200,170,120)
  out.append((0,G_BARK,0,(px+3,py+15,14,4)))
  out.append((1,sh,1,(px+10,py+10,4 if k==G_SMALL else 6)))
  out.append((2,sp,0,(px+7,py+8,3,3)))
  out.append((2,sp,0,(px+11,py+12,3,3)))
 elif ch=='B':
  out.append((0,(40,30,60),1,(px+10,py+10,9)))
  out.append((1,G_BOSS[4],1,(px+10,py+10,6)))
  out.append((2,(255,60,60),0,(px+6,py+8,3,3)))
  out.append((2,(255,60,60),0,(px+11,py+8,3,3)))
G_SCH=(None,('Silver',(190,195,205),(240,242,248),(105,110,125),(80,170,255)),('Gold',(235,185,40),(255,235,130),(150,100,20),(255,110,30)),('Neon',(40,255,140),(240,255,60),(255,40,220),(40,230,255)),('Purple-blue',(130,60,210),(70,150,255),(40,30,120),(160,235,255)))
def G_hero(g,out):
 px=g.x*G_T
 py=20+g.y*G_T
 d=g.ride
 if d is not None:
  r=g.face
  out.append((8,(60,120,230),0,(px+(9 if r else 8),py+5,3,5)))
  out.append((9,(240,200,160),1,(px+(10 if r else 9),py+3,2)))
  G_drag(px,py+2,0.34,d[1],d[6],d[7],d[8],out,20 if r else 0,d[9]&7)
  return
 out.append((5,(240,200,160),1,(px+10,py+5,4)))
 out.append((6,G_BARK,0,(px+6,py+1,8,3)))
 out.append((6,(60,120,230),0,(px+6,py+9,8,7)))
 out.append((6,(60,40,30),0,(px+6,py+16,3,4)))
 out.append((6,(60,40,30),0,(px+11,py+16,3,4)))
def G_paint(ops):
 ops.sort(key=lambda o:(o[0],o[1],o[2],o[3][1]if o[2]==0 else 0,o[3][0]))
 last=None
 for layer,c,kind,a in ops:
  if kind==0:
   if last and last[0]==(layer,c)and(last[2]==a[1])and(last[4]==a[3])and(last[1]+last[3]==a[0]):
    last[3]+=a[2]
    continue
   if last:
    rect(last[1],last[2],last[3],last[4],last[0][1])
   last=[(layer,c),a[0],a[1],a[2],a[3]]
   continue
  if last:
   rect(last[1],last[2],last[3],last[4],last[0][1])
   last=None
  if kind==1:
   circ(a[0],a[1],a[2],c)
  else:
   col(c)
   fill_poly(a[0],a[1])
 if last:
  rect(last[1],last[2],last[3],last[4],last[0][1])
