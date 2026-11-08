# GHDRAGOB: part of GHDRAGOP. Keep it next to GHDRAGOP.
from GHDRAGOC import*
UP=25
def G_egg_type(m,up=0):
 r=random.randint(0,999)
 rar=4 if r<4+2*m else 3 if r<30+10*m else 2 if r<110+25*m else 1 if r<330+40*m else 0
 rar=min(4,rar+up)
 return random.choice([i for i in range(20)if G_DT[i][2]==rar])
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
def G_hud(g):
 d=g.ride
 if d is not None:
  who=d[0]+' '+str(d[3])+'/'+str(d[4])
 else:
  who='You '+str(g.hp)+'/'+str(g.mhp)
 t=(G_LANDS[g.m],who,'Egg '+str(g.warm)if g.bag else str(g.coins)+'c')
 if t==G_HUD[0]:
  return
 old=G_HUD[0]or('','','')
 if G_HUD[0]is None:
  rect(0,0,320,20,BLACK)
 for i,x,c in((0,4,GOLD),(1,140,WHITE),(2,262,YELLOW)):
  if t[i]!=old[i]:
   text(x,15,old[i],BLACK)
   text(x,15,t[i],c)
 G_HUD[0]=t
