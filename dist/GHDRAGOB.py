# GHDRAGOB: part of GHDRAGOP. Keep it next to GHDRAGOP.
from GHDRAGOC import*
def sample(seq,k):
 a=list(seq)
 shuffle(a)
 return a[:k]
def G_base(m,ch):
 if ch=='~':
  return G_WATER
 if ch=='L':
  return G_LAVA
 if ch=='"':
  return G_TALL[m]
 return G_GROUND[m]
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
 elif ch=='^':
  out.append((0,G_ROCK,2,([px,px+10,px+20],[py+20,py+1,py+20])))
  out.append((1,WHITE,2,([px+6,px+10,px+14],[py+8,py+1,py+8])))
 elif ch=='H':
  out.append((0,G_BARK,1,(px+10,py+12,9)))
  out.append((1,(60,40,20),1,(px+10,py+12,6)))
  out.append((2,(245,235,210),1,(px+7,py+12,3)))
  out.append((2,(245,235,210),1,(px+13,py+11,3)))
  out.append((3,(200,160,90),0,(px+1,py+15,18,2)))
 elif ch=='E':
  c=G_RCOL[G_DT[G_EGGS.get((m,x,y),0)][2]]
  out.append((0,G_BARK,0,(px+3,py+15,14,4)))
  out.append((1,(245,235,210),1,(px+10,py+10,6)))
  out.append((2,c,0,(px+7,py+8,3,3)))
  out.append((2,c,0,(px+11,py+12,3,3)))
 elif ch=='B':
  out.append((0,(40,30,60),1,(px+10,py+10,9)))
  out.append((1,G_BOSS[4],1,(px+10,py+10,6)))
  out.append((2,(255,60,60),0,(px+6,py+8,3,3)))
  out.append((2,(255,60,60),0,(px+11,py+8,3,3)))
def G_hero(g,out):
 px=g.x*G_T
 py=20+g.y*G_T
 d=g.ride
 if d is not None:
  c=d[6]
  out.append((5,lt(c,0.45),2,([px,px+9,px+4],[py+2,py+11,py+14])))
  out.append((6,c,0,(px+2,py+11,13,7)))
  out.append((6,c,0,(px+13,py+6,7,7)))
  out.append((6,c,0,(px,py+15,3,3)))
  out.append((6,c,0,(px+4,py+18,3,2)))
  out.append((6,c,0,(px+11,py+18,3,2)))
  out.append((7,BLACK,0,(px+17,py+8,2,2)))
  if d[7]&1:
   out.append((7,G_BARK,0,(px+5,py+11,6,3)))
  if d[7]&2:
   out.append((7,RED,0,(px+12,py+11,3,5)))
  if d[7]&4:
   out.append((8,GOLD,0,(px+14,py+3,5,3)))
  out.append((8,(240,200,160),1,(px+8,py+5,3)))
  out.append((8,(60,120,230),0,(px+6,py+8,5,4)))
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
def G_cells(g,todo,with_hero):
 mp=g.maps[g.m]
 ops=[]
 rows={}
 for x,y in todo:
  rows.setdefault(y,[]).append(x)
 for y in rows:
  xs=sorted(rows[y])
  i=0
  while i<len(xs):
   c=G_base(g.m,mp[y][xs[i]])
   j=i+1
   while j<len(xs)and xs[j]==xs[j-1]+1 and(G_base(g.m,mp[y][xs[j]])==c):
    j+=1
   ops.append((-1,c,0,(xs[i]*G_T,20+y*G_T,(j-i)*G_T,G_T)))
   i=j
 for x,y in todo:
  G_shapes(g.m,x,y,mp[y][x],ops)
 if with_hero:
  G_hero(g,ops)
 G_paint(ops)
def G_hud(g):
 d=g.ride
 if d is not None:
  who=d[0]+' '+str(d[3])+'/'+str(d[4])
 else:
  who='You '+str(g.hp)+'/'+str(g.mhp)
 t=(G_LANDS[g.m],who,'Egg '+str(g.warm)if g.egg is not None else str(g.coins)+'c')
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
def G_bar(x,y,w,v,mx,c):
 f=max(0,min(w,int(w*v/mx)))if v>0 else 0
 if v>0:
  f=max(2,f)
 rect(x,y,f,6,c)
 rect(x+f,y,w-f,6,DARK)
def G_baby(x,y,c,big=1):
 col(lt(c,0.4))
 fill_poly([x-4*big,x+10*big,x+4*big],[y-6*big,y-22*big,y])
 rect(x-10*big,y-4*big,26*big,14*big,c)
 rect(x-22*big,y-12*big,14*big,11*big,c)
 rect(x+14*big,y+2*big,12*big,4*big,c)
 rect(x-18*big,y-9*big,3*big,3*big,BLACK)
def G_board(g):
 if g.quest is not None:
  q=g.quest
  c=choose(q[5]+' '+str(q[3])+'/'+str(q[2]),['Keep going','Give up quest'])
  if c==1:
   g.quest=None
  return
 qs=[G_new_quest(g)for i in range(3)]
 c=choose('Quests: pick one',[q[5][:15]+' '+str(q[4])+'c'for q in qs]+['Not now'])
 if 0<=c<3:
  g.quest=qs[c]
def G_pen(g):
 while g.pen:
  opts=[('> 'if d is g.pick else '')+d[0]+' L'+str(d[2])+' '+G_DT[d[1]][0][:6]for d in g.pen]
  c=choose('Dragon pen '+str(len(g.pen))+'/7',opts+['Back'])
  if c<0 or c>=len(g.pen):
   return
  d=g.pen[c]
  a=choose(d[0]+' the '+G_DT[d[1]][0],['Pick as partner','See stats','Let it go free','Back'])
  if a==0:
   g.pick=d
  elif a==1:
   cls()
   G_baby(160,60,d[6],1)
   G_stats(d)
  elif a==2 and len(g.pen)>1:
   g.pen.remove(d)
   if g.pick is d:
    g.pick=g.pen[0]
def G_shop(g):
 while True:
  d=g.pick
  opts=[]
  for nm,pr,bit in G_SHOP:
   opts.append(nm+(' (have)'if bit and d[7]&bit else ' '+str(pr)+'c'))
  c=choose(d[0]+': '+str(g.coins)+' coins',opts+['Back'])
  if c<0 or c>=len(G_SHOP):
   return
  nm,pr,bit=G_SHOP[c]
  if bit and d[7]&bit:
   continue
  if g.coins<pr:
   message(['You need '+str(pr)+' coins.','Do quests to earn more.'],'Not enough')
   continue
  if bit==0:
   p=choose('Pick a colour',['Red','Blue','Green','Gold','Purple','Pink','Black','White'])
   if p<0:
    continue
   d[6]=G_PAINT[p]
  else:
   d[7]|=bit
  g.coins-=pr
  cls()
  G_baby(160,120,d[6],2)
  message([d[0]+' looks great!'],nm)
def G_nest(g):
 G_rest(g)
 while True:
  opts=['Dragon pen','Quest board','Shop','Leave the nest']
  c=choose('The Nest (all rested)',opts)
  if c==0:
   G_pen(g)
  elif c==1:
   G_board(g)
  elif c==2:
   if g.pick is None:
    message(['Hatch a dragon first!'])
   else:
    G_shop(g)
  else:
   return
