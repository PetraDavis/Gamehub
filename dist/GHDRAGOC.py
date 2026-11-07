# GHDRAGOC: part of GHDRAGOP. Keep it next to GHDRAGOP.
from GHDRAGOD import*
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
G_GEARC=(None,(250,150,200),(40,40,40),(130,60,190),GOLD,G_CYAN,BLACK,(250,150,200),(190,195,205),(220,40,30),G_BARK,(40,80,200),(190,195,205),(40,80,200),(90,190,80),(220,40,30),GOLD)
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
  r=G_DT[G_EGGS.get((m,x,y),0)][2]
  sh=(25,25,35)if r==4 else G_CYAN if r==5 else(245,235,210)
  sp=G_MAG if r==5 else YELLOW if r==4 else G_RCOL[r]if r else(200,170,120)
  out.append((0,G_BARK,0,(px+3,py+15,14,4)))
  out.append((1,sh,1,(px+10,py+10,6)))
  out.append((2,sp,0,(px+7,py+8,3,3)))
  out.append((2,sp,0,(px+11,py+12,3,3)))
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
  out.append((7,YELLOW if d[1]==19 else BLACK,0,(px+17,py+8,2,2)))
  if d[8]:
   out.append((7,G_GEARC[d[8]],0,(px+5,py+11,6,3)))
  if d[7]:
   out.append((8,G_GEARC[d[7]],0,(px+14,py+3,5,3)))
  out.append((8,(240,200,160),1,(px+8,py+5,3)))
  out.append((8,(60,120,230),0,(px+6,py+8,5,4)))
  return
 out.append((5,(240,200,160),1,(px+10,py+5,4)))
 out.append((6,G_BARK,0,(px+6,py+1,8,3)))
 out.append((6,(60,120,230),0,(px+6,py+9,8,7)))
 out.append((6,(60,40,30),0,(px+6,py+16,3,4)))
 out.append((6,(60,40,30),0,(px+11,py+16,3,4)))
G_HUD=[None]
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
def G_bar(x,y,w,v,mx,c):
 f=max(0,min(w,int(w*v/mx)))if v>0 else 0
 if v>0:
  f=max(2,f)
 rect(x,y,f,6,c)
 rect(x+f,y,w-f,6,DARK)
def G_foe_screen(f,title):
 cls()
 rbox(150,30,140,120,10,RED if f is G_DREAD else f[4],2,G_NIGHT)
 G_foe_art(f)
 ctext(24,title,GOLD)
def G_battle(g,f):
 name,fhp,fat,xp,fc,fe=f
 mx=fhp
 G_foe_screen(f,name+' appears!')
 log=''
 sel=0
 was=None
 while True:
  d=g.ride
  opts=('Claw','Breath','Run')if d is not None else('Sword','Run')
  n=len(opts)
  w=300//n
  sel=min(sel,n-1)
  now=(d[0]if d else 'You',d[3]if d else g.hp,fhp,sel,log,n)
  if was is None or was[0]!=now[0]:
   rect(0,40,148,60,BLACK)
   rect(0,150,320,34,BLACK)
   text(12,56,now[0],d[6]if d and d[1]!=19 else WHITE)
   text(12,86,name[:12],RED if f is G_DREAD else fc)
   for i in range(n):
    cc=GOLD if i==sel else WHITE
    rbox(10+i*w,154,w-6,24,8,cc)
    text(10+i*w+(w-6)//2-len(opts[i])*5,172,opts[i],cc)
   was=None
  if was is None or was[1]!=now[1]:
   G_bar(12,62,120,now[1],d[4]if d else g.mhp,GREEN)
  if was is None or was[2]!=fhp:
   G_bar(12,92,120,fhp,mx,RED)
  if was is not None and was[3]!=sel:
   for i in(was[3],sel):
    cc=GOLD if i==sel else WHITE
    edge(10+i*w,154,w-6,24,8,cc)
    text(10+i*w+(w-6)//2-len(opts[i])*5,172,opts[i],cc)
  if was is None or was[4]!=log:
   rect(0,186,320,24,BLACK)
   text(6,202,log[:31],GREY)
  was=now
  k=wkey()
  if k in(LEFT,RIGHT):
   sel=(sel+(1 if k==RIGHT else-1))%n
   continue
  if k!=OK:
   continue
  o=opts[sel]
  if o=='Run':
   if f is G_BOSS:
    log='The Wyrm blocks your way!'
    continue
   if random.random()<0.6:
    return True
   log="Couldn't get away."
  elif o=='Sword':
   dm=random.randint(3,5)
   fhp-=dm
   log='Sword hits for '+str(dm)+'.'
  else:
   at=5+2*d[2]+2*G_DT[d[1]][2]
   if o=='Claw':
    dm=at+random.randint(0,2)
    log='Claw hits for '+str(dm)+'.'
   else:
    dm=at+random.randint(2,5)
    if G_beats(G_el(d),fe):
     dm*=2
     log='Super breath! '+str(dm)+'.'
    elif G_beats(fe,G_el(d)):
     dm//=2
     log='Weak breath... '+str(dm)+'.'
    else:
     log='Breath hits for '+str(dm)+'.'
   fhp-=dm
  if fhp<=0:
   msg=[]
   for dd in g.pen:
    if dd[3]>0 and(dd is d or dd is g.pick):
     dd[5]+=xp
     while dd[5]>=dd[2]*10:
      dd[5]-=dd[2]*10
      dd[2]+=1
      dd[4]+=6
      dd[3]=dd[4]
      msg.append(dd[0]+' is now level '+str(dd[2])+'!')
   message(msg[:3]or['You won!'],name+' beaten')
   if f is not G_BOSS:
    G_quest_step(g,0,name)
    G_quest_step(g,2,g.m)
   return True
  dm=max(1,fat+random.randint(0,3)-(d[2]if d else 0))
  log+=' It hits '+str(dm)+'.'
  if d is not None:
   d[3]=max(0,d[3]-dm)
   if d[3]==0:
    g.ride=None
    message([d[0]+' is too tired to fly.','You fight on foot!'],'Oh no')
    G_foe_screen(f,name)
    was=None
  else:
   g.hp-=dm
   if g.hp<=0:
    cls()
    ctext(60,'YOU DIED',RED)
    message(['The '+name+' won.','Back to your last save','at the nest.'],'Game over')
    return False
def G_quest_step(g,kind,what):
 q=g.quest
 if q is None or q[0]!=kind or(q[1]is not None and q[1]!=what):
  return
 q[3]+=1
 if q[3]>=q[2]:
  g.coins+=q[4]
  g.quest=None
  message(['You finished:',q[5],'+'+str(q[4])+' coins!'],'Quest done!')
