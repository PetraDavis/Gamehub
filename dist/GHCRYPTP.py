# GHCRYPTP: the game part of GHCRYPT. Run GHCRYPT, not this.
from GHCRYPTB import*
class Steer:
 def __init__(self,keys,stop_on_back=False):
  self.keys=keys
  self.back=stop_on_back
  self.d=0
 def feed(self,k):
  if k in self.keys:
   if self.back and self.d and(k!=self.d)and(self.keys.index(k)//2==self.keys.index(self.d)//2):
    self.d=0
   else:
    self.d=k
  elif k:
   self.d=0
  return self.d
 def stop(self):
  self.d=0
G_SPRN=('couch','desk','lamp','phone','rack','table','vase')
def G__unpack_spr():
 i=0
 for name in G_SPRN:
  w,n=(G_SPRD[i]/255*2,G_SPRD[i+1])
  i+=2
  parts=[]
  for k in range(n):
   d=G_SPRD[i:i+7]
   parts.append((d[0]/255,d[1]/255,d[2]/255,d[3]/255,(d[4],d[5],d[6])))
   i+=7
  G_SPR[name]=(w,parts)
G__unpack_spr()
def G_bottom(g,prompt):
 if prompt==g.shown:
  return
 g.shown=prompt
 rect(0,G_VH,320,210-G_VH,BLACK)
 text(4,G_VH+15,G_room(g),GREY)
 if g.flash:
  text(250,G_VH+15,'LIGHT',GOLD)
 text(4,G_VH+33,prompt[:31],WHITE)
def G_keypad(title,hint,n):
 abc='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
 cls()
 ctext(20,title,GOLD)
 y=42
 for ln in G_wrap(hint,30):
  text(10,y,ln,GREY)
  y+=17
 typed=''
 sel=0
 while True:
  rect(60,96,200,26,BLACK)
  s=''
  for i in range(n):
   s+=(typed[i]if i<len(typed)else '_')+' '
  ctext(116,s.strip(),WHITE)
  for i in range(26):
   x=4+i%13*24
   yy=140+i//13*28
   c=GOLD if i==sel else WHITE
   rect(x,yy,22,24,BLACK)
   rbox(x,yy,22,24,5,c)
   text(x+6,yy+18,abc[i],c)
  k=wkey()
  if k==LEFT:
   sel=(sel-1)%26
  elif k==RIGHT:
   sel=(sel+1)%26
  elif k in(UP,DOWN):
   sel=(sel+13)%26
  elif k==DEL:
   typed=typed[:-1]
  elif k==CLR:
   return None
  elif k==OK:
   typed+=abc[sel]
   if len(typed)==n:
    return typed
def G_short(g):
 if not g.power:
  return 'Find the power switch'
 if not g.note:
  return 'Look around the foyer'
 if not g.closet:
  return "Decode Ivy's note (DEL)"
 if not g.living:
  return 'Unlock the Living Room'
 if not g.tapheard:
  return 'The TV switched itself on'
 if not g.notebook:
  return "Find Ivy's notebook"
 return 'Hallway keypad: 5 letters'
def G_facing(g):
 ca=math.cos(g.a)
 sa=math.sin(g.a)
 for n in range(1,9):
  d=n*0.2
  t=G_tile(g.x+ca*d,g.y+sa*d)
  if t!='.'and(not(t=='l'and g.living)):
   return t
 best=None
 bd=1.5
 for sx,sy,kind in G_SPRITES:
  dx=sx-g.x
  dy=sy-g.y
  dist=math.sqrt(dx*dx+dy*dy)
  if dist<bd and(dx*ca+dy*sa)/max(dist,0.01)>0.8:
   best=kind
   bd=dist
 return best
def G_label(g,t):
 if t=='P':
  return 'ENTER: power switch'
 if t=='F':
  return 'ENTER: front door'
 if t=='G':
  return 'ENTER: grandfather clock'
 if t=='C':
  return 'ENTER: hide in closet'if g.closet else 'ENTER: closet keypad'
 if t=='l':
  return 'ENTER: Living Room door'
 if t=='k':
  return 'ENTER: hallway keypad'
 if t=='j':
  return 'ENTER: dining room door'
 if t=='S':
  return 'ENTER: grand staircase'
 if t=='T':
  return 'ENTER: smart TV'
 if t=='B':
  return 'ENTER: bookshelf'
 if t=='table':
  return "ENTER: Ivy's notebook"
 if t in('phone','desk','lamp','couch','rack','vase'):
  return 'ENTER: look'
 return ''
def G_use(g,t):
 if t=='P':
  if g.power:
   return G_say(g,'Power: on.')
  g.power=True
  for n in range(6):
   g.blackout=n%2==0
   G_render(g)
  g.blackout=False
  G_say(g,'CLUNK. Years of dust rattle in the wiring.')
  g.locked=True
  G_render(g)
  G_toast(g,['ASHGROVE SMART HOME:','Welcome home.','Front door LOCKED.','You did not set that up.'])
 elif t=='F':
  G_say(g,"SMART HOME: LOCKED. The handle doesn't move."if g.locked else 'The door is stuck. Swollen in its frame.')
 elif t=='G':
  if not g.power:
   return G_say(g,'Too dark to make it out. Get the lights on first.')
  g.note=True
  G_page("IVY'S NOTE",'Folded paper, tucked behind the pendulum glass.\n\nDad never notices anything. Grandma taught me this one when I was six. My name is the key.\n\n'+G_CIPHER+'\n\n- I.V.Y.')
  g.armed=True
 elif t=='C':
  if g.closet:
   return G_hide(g)
  if not g.power:
   return G_say(g,'The keypad is dead.')
  a=G_keypad('COAT CLOSET KEYPAD','A brass keypad. Four letters.',4)
  if a=='ECHO':
   g.closet=True
   g.shown=None
   G_render(g)
   G_say(g,'The closet clicks open. On a hook: a brass key tagged LIVING ROOM. You take it.')
  elif a:
   G_say(g,'The keypad buzzes. Wrong code.')
 elif t=='l':
  if not g.closet:
   return G_say(g,'Locked. A brass keyhole, polished from use.')
  g.living=True
  G_render(g)
  G_say(g,'The brass key turns. Stiff, then all at once.')
  g.tv=True
  G_say(g,'Somewhere in the Living Room, a TV switches itself on.')
 elif t=='j':
  G_say(g,'Swollen shut in its frame.')
 elif t=='S':
  G_say(g,'Boarded, chained and padlocked. The padlock is engraved M.A.')
 elif t=='B':
  G_say(g,"Books on radios, codes and moths. Mildred's, mostly.")
 elif t=='T':
  if not g.power:
   return G_say(g,'The TV is dark.')
  G_tv(g)
 elif t=='table':
  g.notebook=True
  G_grid_page()
  G_page("IVY'S NOTEBOOK","She can hear voices and screens. She's bad at knocks. I think it's too slow for her.\n\n- Ivy")
 elif t=='phone':
  G_say(g,'An old rotary phone. Silent. For now.')
 elif t=='desk':
  G_say(g,"Mildred's desk. Pages and pages of dots and dashes.")
 elif t=='lamp':
  G_say(g,'An old brass floor lamp.')
 elif t=='couch':
  G_say(g,'The cushions still hold the shape of someone.')
 elif t=='rack':
  G_say(g,"Coats on hooks. One is a child's raincoat.")
 elif t=='vase':
  G_say(g,'Dried flowers. They crumble when you breathe.')
 elif t=='k':
  if not g.power:
   return G_say(g,'The keypad is dark. No power.')
  a=G_keypad('ASHGROVE SMART LOCK','A sticky note in Ivy\'s writing: "the TV knows. listen."',5)
  if a=='QUIET':
   g.won=True
  elif a:
   G_say(g,'The keypad buzzes. Wrong code.')
 g.shown=None
def G_tv(g):
 cls((10,14,30))
 ctext(24,'ASHGROVE SMART TV',GOLD)
 text(10,48,'HDMI 3: for whoever comes next',GREY)
 text(10,66,'Then black. Then knocking.',GREY)
 y=100
 x=20
 for r,c in G_KNOCKS:
  for grp in(r,c):
   for n in range(grp):
    circ(x,y,4,WHITE)
    x+=11
    pause(0.25)
   x+=10
  x+=14
  if x>270:
   x=20
   y+=24
 text(10,170,'4-1  4-5  2-4  1-5  4-4',(160,210,255))
 text(10,204,'Written in your journal. ENTER',GREY)
 g.tapheard=True
 while wkey()not in(OK,CLR):
  pass
 if not g.awake:
  g.awake=True
  g.ytimer=6
  G_page('...','The knocking stops.\nEvery screen in the house flickers at once.\n\nShe is awake. Hide when the lights stutter.',(200,140,140))
def G_hide(g):
 g.hidden=True
 cls()
 ctext(70,'You squeeze into the coat',WHITE)
 ctext(90,'closet. Breathe slowly.',WHITE)
 ctext(150,'ENTER: step out',GREY)
 t0=0
 while True:
  k=key()
  if k==OK:
   break
  pause(0.2)
  t0+=1
  if g.ystate=='hunt'and t0>25:
   g.ystate='dormant'
   g.ys_vis=False
   g.ytimer=random.randint(35,55)
   rect(0,110,320,30,BLACK)
   ctext(130,"The static fades. She's gone.",GREY)
 g.hidden=False
 g.shown=None
def G_sighting(g):
 g.sighted=True
 g.yx,g.yy=(9.5,1.0)
 for n in range(10):
  g.blackout=n<3 and n%2==0
  g.ys_vis=n>=3
  g.yy=1.0+max(0,n-3)*0.08
  G_render(g)
  pause(0.2)
 g.ys_vis=False
 g.blackout=False
 G_render(g)
 G_say(g,'...it was a woman. Made of static. And she was looking at you.')
def G_ys_update(g,dt):
 if not g.awake or g.won:
  return
 if g.ystate=='dormant':
  g.ytimer-=dt
  if g.ytimer<=0:
   g.ystate='warn'
   g.ytimer=4
   G_say(g,'Static hisses somewhere in the house. The lights stutter.')
 elif g.ystate=='warn':
  g.ytimer-=dt
  g.blackout=random.random()<0.35
  if g.ytimer<=0:
   g.blackout=False
   spots=((2.5,1.5),(9.5,1.5),(2.5,6.4),(11.5,1.5),(6.5,6.5))
   far=[p for p in spots if abs(p[0]-g.x)+abs(p[1]-g.y)>5]or list(spots)
   g.yx,g.yy=random.choice(far)
   g.ystate='hunt'
   g.ys_vis=True
   g.ytimer=28
 elif g.ystate=='hunt':
  g.ytimer-=dt
  dx=g.x-g.yx
  dy=g.y-g.yy
  d=math.sqrt(dx*dx+dy*dy)
  sp=0.55*dt
  if d>0.01:
   nx=g.yx+dx/d*sp
   ny=g.yy+dy/d*sp
   if not G_solid(g,nx,g.yy)or G_tile(nx,g.yy)in 'l':
    g.yx=nx
   if not G_solid(g,g.yx,ny):
    g.yy=ny
  g.blackout=d<3 and random.random()<0.25
  if d<0.6:
   G_caught(g)
  elif g.ytimer<=0:
   g.ystate='dormant'
   g.ys_vis=False
   g.blackout=False
   g.ytimer=random.randint(35,55)
def G_caught(g):
 for n in range(8):
  for y in range(0,176,22):
   gv=random.randint(60,230)
   rect(0,y,320,22,(gv,gv,gv))
 cls()
 ctext(90,'She found you.',(220,120,120))
 ctext(130,'ENTER',GREY)
 while wkey()not in(OK,CLR):
  pass
 g.x,g.y,g.a=(11.5,5.5,math.pi)
 g.ystate='dormant'
 g.ys_vis=False
 g.blackout=False
 g.ytimer=30
 g.shown=None
def G_play():
 g=G_St()
 g.x,g.y,g.a=(9.5,6.4,-math.pi/2)
 g.power=g.locked=g.note=g.closet=g.living=g.tv=False
 g.tapheard=g.notebook=g.awake=g.armed=g.sighted=False
 g.flash=True
 g.blackout=False
 g.won=False
 g.hidden=False
 g.ys_vis=False
 g.ystate='dormant'
 g.ytimer=0
 g.yx=g.yy=0
 g.shown=None
 cls()
 G_page('enCRYPTed','Ashgrove Manor. Bought at government auction. Power off since the accident.\n\nIt is pitch dark. Find the power switch by the front door.')
 last=G_clock()
 dirty=True
 st=Steer((UP,DOWN),True)
 while not g.won:
  k=key()
  d=st.feed(k)if k not in(LEFT,RIGHT)else st.d
  t=G_clock()
  dt=t-last if G_now else 0.25
  last=t
  dt=max(0.02,min(dt,0.5))
  moved=False
  if k==CLR:
   if G_pause_menu(g):
    return
   dirty=True
   continue
  if k==DEL:
   G_journal(g)
   dirty=True
   continue
  if k==SECOND:
   g.flash=not g.flash
   g.shown=None
   dirty=True
   while key()==SECOND:
    pass
  if k==LEFT:
   g.a-=2.0*max(dt,0.25)
   moved=True
  elif k==RIGHT:
   g.a+=2.0*max(dt,0.25)
   moved=True
  if d==UP or d==DOWN:
   s=(1.6 if d==UP else-1.0)*dt
   nx=g.x+math.cos(g.a)*s
   ny=g.y+math.sin(g.a)*s
   r=0.22 if s>0 else-0.22
   ox,oy=(g.x,g.y)
   if not G_solid(g,nx+math.cos(g.a)*r,g.y):
    g.x=nx
   if not G_solid(g,g.x,ny+math.sin(g.a)*r):
    g.y=ny
   if abs(g.x-ox)+abs(g.y-oy)<0.001:
    st.stop()
   moved=True
  elif k==OK:
   f=G_facing(g)
   if f:
    G_use(g,f)
    dirty=True
    while key()==OK:
     pass
  if g.armed and(not g.sighted)and(G_room(g)=='Grand Foyer'):
   look=math.atan2(1.0-g.y,9.5-g.x)
   diff=(look-g.a+math.pi)%(2*math.pi)-math.pi
   if abs(diff)<0.35:
    G_sighting(g)
    st.stop()
    dirty=True
  before=g.ys_vis or g.blackout
  G_ys_update(g,dt)
  if moved or dirty or g.ys_vis or g.blackout or before:
   G_render(g)
   dirty=False
  f=G_facing(g)
  G_bottom(g,G_label(g,f)if f else G_short(g))
  if not moved:
   pause(0.03)
 G_ending()
def G_back():
 G_play()
