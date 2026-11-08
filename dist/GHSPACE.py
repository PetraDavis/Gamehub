# GHSPACE from GAMEHUB, on its own. Run it.
from ti_draw import*
from ti_system import*
import time
import random
import math
UP=25
DOWN=34
LEFT=24
RIGHT=26
OK=105
CLR=45
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
GREY=(110,110,110)
RED=(220,50,50)
H=210
def wkey():
 return wait_key()
_C=[None]
def col(c):
 if c!=_C[0]:
  _C[0]=c
  set_color(c[0],c[1],c[2])
def fr(x,y,w,h):
 fill_rect(x-1,y-1,w+1,h+1)
def rect(x,y,w,h,c):
 if w<1 or h<1:
  return
 col(c)
 fill_rect(x-1,y-1,w+1,h+1)
COVER=[0]
def cls(c=BLACK):
 COVER[0]+=1
 col(c)
 fill_rect(-1,-1,321,211)
TY=6
def text(x,y,s,c=WHITE):
 col(c)
 draw_text(x,y+TY,s)
def ctext(y,s,c=WHITE,cx=160):
 col(c)
 draw_text(cx-len(s)*5,y+TY,s)
def circ(x,y,r,c):
 col(c)
 fill_circle(x,y,r)
def ring(x,y,r,c,t=2,inner=BLACK):
 col(c)
 fill_circle(x,y,r)
 col(inner)
 fill_circle(x,y,r-t)
def _corners(x,y,w,h,r,t):
 if r<=t:
  return((x,y,w,t),(x,y+h-t,w,t),(x,y+t,t,h-2*t),(x+w-t,y+t,t,h-2*t))
 a=min(r//2,2*t)
 return((x+r,y,w-2*r,t),(x+r,y+h-t,w-2*r,t),(x,y+r,t,h-2*r),(x+w-t,y+r,t,h-2*r),(x+a,y+t,r-a,t),(x+w-r,y+t,r-a,t),(x+a,y+h-2*t,r-a,t),(x+w-r,y+h-2*t,r-a,t),(x+t,y+a,t,r-a),(x+w-2*t,y+a,t,r-a),(x+t,y+h-r,t,r-a),(x+w-2*t,y+h-r,t,r-a))
def rbox(x,y,w,h,r,c,t=2,inner=BLACK,fill=True):
 edge(x,y,w,h,r,c,t)
 if not fill:
  return
 col(inner)
 if r<=t:
  fr(x+t,y+t,w-2*t,h-2*t)
  return
 a=min(r//2,2*t)
 fr(x+t,y+r,w-2*t,h-2*r)
 fr(x+r,y+t,w-2*r,t)
 fr(x+r,y+h-2*t,w-2*r,t)
 if r>2*t:
  fr(x+a,y+2*t,w-2*a,r-2*t)
  fr(x+a,y+h-r,w-2*a,r-2*t)
def edge(x,y,w,h,r,c,t=2,inner=BLACK):
 col(c)
 for bx,by,bw,bh in _corners(x,y,w,h,r,t):
  if bw>0 and bh>0:
   fr(bx,by,bw,bh)
MSG=[0,0]
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
def _wrap(s,n=30):
 out=[]
 line=''
 for w in s.split(' '):
  if len(line)+len(w)+1>n:
   out.append(line)
   line=w
  else:
   line=(line+' '+w).strip()
 if line:
  out.append(line)
 return out
def how_to(title,rules,buttons):
 cls()
 ctext(20,'HOW TO PLAY',GOLD)
 ctext(38,title,GREY)
 y=60
 for ln in _wrap(rules):
  text(8,y,ln)
  y+=16
 y+=6
 text(8,y,'BUTTONS',GOLD)
 y+=17
 for b in buttons:
  text(8,y,b)
  y+=16
 text(8,206,'ENTER: back',GREY)
 while wkey()not in(OK,CLR,UP,DOWN):
  pass
def home(mod,title,rules,buttons,opts=('Play','Back'),sel=0):
 n=len(opts)
 while True:
  cls()
  ring(160,58,36,GOLD,3)
  try:
   circ(160,58,33,I_bg(mod))
   I_draw(mod,160,58,WHITE)
  except Exception:
   pass
  ctext(122,title,GOLD)
  ctext(146,'Up/Down: how to play',GREY)
  bw=(300-(n-1)*8)//n
  first=True
  old=-1
  while True:
   for i in range(n):
    if not first and i!=sel and(i!=old):
     continue
    x=10+i*(bw+8)
    c=GOLD if i==sel else WHITE
    if first:
     rbox(x,166,bw,28,10,c,2,BLACK,False)
    else:
     edge(x,166,bw,28,10,c)
    text(x+bw//2-len(opts[i])*5,186,opts[i],c)
   first=False
   old=sel
   k=wkey()
   if k==LEFT:
    sel=(sel-1)%n
   elif k==RIGHT:
    sel=(sel+1)%n
   elif k in(UP,DOWN):
    how_to(title,rules,buttons)
    break
   elif k==CLR:
    return-1
   elif k==OK:
    if opts[sel]=='Back':
     return-1
    return sel
I_BLACK=(0,0,0)
I_BG={'GHSPACE':(15,20,50)}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_poly(xs,ys,c):
 I_c_(c)
 fill_poly([int(v)for v in xs],[int(v)for v in ys])
def I_space(x,y,c):
 for sx,sy in((-15,-12),(12,-16),(16,8),(-17,10),(2,17)):
  I_box(x+sx,y+sy,2,2,(255,240,180))
 I_poly([x-4,x+4,x+8,x-8],[y-14,y-14,y+6,y+6],(220,225,235))
 I_box(x-3,y-7,6,5,(90,170,230))
 I_poly([x-8,x-13,x-8],[y-2,y+8,y+6],(215,40,40))
 I_poly([x+8,x+13,x+8],[y-2,y+8,y+6],(215,40,40))
 I_poly([x-5,x+5,x],[y+7,y+7,y+15],(250,170,40))
I_ICONS={'GHSPACE':I_space}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_AIR=30
G_TANK=10
G_S={'wake':('You wake in a sleep pod on Station Kestrel. Red lights blink. A calm voice says: Hull breach. Air failing. Please go to the escape pods. The room is empty.',(('Climb out of the pod','rooms','',''),)),'rooms':('Crew quarters. Every bed is empty and unmade. A locker hangs open. A tablet glows on the floor.',(('Read the tablet','log','','c'),('Search the locker','locker','','kh'),('Go out to the corridor','hall','',''))),'log':("Captain's log: Something got in through the cargo bay. Everyone to the pods. The pod code starts 4-7. I hid the last number on the bridge. The rest is static.",(('Put the tablet down','rooms','',''),)),'locker':('Inside you find a space helmet and a keycard marked CARGO. You take them both.',(('Close the locker','rooms','',''),)),'hall':('Corridor. Doors to the cargo bay, pod bay and med bay. A ladder goes up. A vent is open.',(('Open the cargo bay','cargo','k',''),('Try the pod bay door','blast','',''),('Go into the med bay','med','',''),('Climb the ladder','bridge','',''),('Crawl into the vent','vent','',''),('Back to the quarters','rooms','',''))),'blast':('A heavy blast door guards the pod bay. The screen beside it says: OPENS ONLY WITH MAIN POWER. SEE ENGINE ROOM.',(('Step back','hall','',''),('The power is on. Go in','pods','p',''))),'vent':('You crawl into the dark vent. Something else is moving in here too, just ahead of you. It stops when you stop.',(('Back out, fast','hall','',''),('Keep crawling','ventend','',''))),'med':('The med bay. Broken glass covers the floor. An oxygen tank sits on a shelf, and a red box on the wall says EMERGENCY FLARE. A soft bed looks very comfy.',(('Take the oxygen tank','tank','','t'),('Open the red box','flarebox','','f'),('Lie down for a moment','nap','',''),('Back to the corridor','hall','',''))),'tank':("You strap on the oxygen tank and take a deep breath. That's better. You have more air now.",(('Look around the med bay','med','',''),)),'flarebox':('Inside is a flare gun with one shot. Bright light might scare off things that like the dark.',(('Take it and look around','med','',''),)),'bridge':("The bridge. Stars shine through cracked glass. The captain's chair is turned away from you. A big red button glows on the main desk.",(('Turn the chair around','chair','','d'),('Press the red button','button','',''),('Climb back down','hall','',''))),'chair':('Nobody is in the chair, but a note is taped to it: Last number of the pod code is 1. Good luck.',(('Put the note away','bridge','',''),)),'cargo':('Crates lie torn open. Something has been living in here. Across the bay a hatch leads to the engine room. A soft clicking comes from behind the crates.',(('Sneak to the engine room','engine','',''),('Fire the flare at the crates','flare','fS','s'),('Look behind the crates','eyes','S',''),('Leave the cargo bay','hall','',''))),'flare':('The flare bursts into blinding light. Dozens of shining eyes squeeze shut, and the creatures scramble away into the vents, shrieking.',(('Go on','cargo','',''),)),'engine':('The engine room. The air here is so thin it hurts to breathe. A big lever on the wall says MAIN POWER: OFF.',(('Wear helmet, pull lever','power','hP','p'),('Pull the lever','faint','P','x'),('Try the lever again','gasp','xP',''),('Go back to the cargo bay','cargo','',''))),'faint':("You pull, but there isn't enough air. The room spins and you have to stumble back out. You need something to breathe with. Trying that again would be a bad idea.",(('Back to the cargo bay','cargo','',''),)),'power':('Lights flicker on all over the station. Far away, a blast door groans open. Behind you, something is clicking.',(('Run for the pod bay','pods','s',''),('Run for the pod bay','swarm','S',''))),'swarm':('Creatures pour out of the cargo bay and fill the corridor, clicking and hissing. They are between you and the pod bay!',(('Fire the flare gun','scare','f','s'),('Push through them','caught','',''),('Hide in the med bay','hide','',''))),'scare':('Blinding light fills the corridor. The creatures shriek and scatter. The way to the pod bay is clear!',(('Run!','pods','',''),)),'hide':('You hold your breath behind the med bay door. Claws scrape past outside... and fade away. That took a lot of air.',(('Sneak to the pod bay','pods','',''),)),'pods':('The pod bay. One escape pod is left. Its keypad blinks: ENTER CODE. A sign says: 2 WRONG TRIES LOCK THE PAD.',(('Type 4-7-1','home','cd',''),('Guess a code','wrong','','w'),('Guess one more time','lockout','w',''),('Go look for the code','hall','',''))),'wrong':('WRONG CODE. One more wrong try will lock the keypad. Did anyone leave the code somewhere?',(('Think it over','pods','',''),)),'home':('The hatch seals. The pod launches into the stars just as something slams against the window... and falls away. Behind you, Station Kestrel goes dark. You made it!',()),'ventend':('You keep going. The thing ahead turns around. Its eyes shine in the dark, and it is much bigger than you.',()),'nap':('You close your eyes for just a moment. The air keeps leaking out while you sleep... and you never wake up.',()),'button':('A voice says: SELF DESTRUCT. TEN SECONDS. There is no off button. Never press the big red button.',()),'eyes':('Dozens of shining eyes look back at you. You run, but they are much faster than you.',()),'gasp':('You pull and pull, but there is no air left to breathe. The room goes black.',()),'caught':('You try to push past, but there are far too many of them. The clicking closes in around you.',()),'lockout':('WRONG CODE. KEYPAD LOCKED. The pod will not open now, and the clicking is right behind you.',())}
G_DEAD=('ventend','nap','button','eyes','gasp','caught','lockout')
def G_fits(c,have):
 for f in c[2]:
  if(f.lower()in have)==f.isupper():
   return False
 return not(c[3]and all((f in have for f in c[3])))
def G_page(s,air):
 cls()
 text(4,14,'LOST ORBIT',GOLD)
 text(236,14,'Air '+str(air),RED if air<=5 else GREY)
 y=36
 for ln in G_wrap(s):
  text(6,y,ln)
  y+=17
 return y
def G_wrap(s,n=31):
 out=[]
 line=''
 for w in s.split(' '):
  if line and len(line)+len(w)+1>n:
   out.append(line)
   line=w
  else:
   line=(line+' '+w).strip()
 if line:
  out.append(line)
 return out
def G_pick(opts,y0):
 sel=0
 y0=max(y0+6,206-20*len(opts))
 for i in range(len(opts)):
  text(20,y0+i*20,opts[i],GOLD if i==sel else WHITE)
 text(6,y0,'>',GOLD)
 while True:
  k=wkey()
  old=sel
  if k==UP:
   sel=(sel-1)%len(opts)
  elif k==DOWN:
   sel=(sel+1)%len(opts)
  elif k==OK:
   return sel
  elif k==CLR:
   return-1
  if sel!=old:
   rect(6,y0+old*20-12,10,16,BLACK)
   text(20,y0+old*20,opts[old],WHITE)
   text(6,y0+sel*20,'>',GOLD)
   text(20,y0+sel*20,opts[sel],GOLD)
def G_game():
 have=''
 air=G_AIR
 at='wake'
 while True:
  words,choices=G_S[at]
  if not choices:
   y=G_page(words,air)
   ctext(max(y+10,186),'GAME OVER'if at in G_DEAD else 'THE END',RED if at in G_DEAD else GOLD)
   ctext(206,'ENTER',GREY)
   while wkey()not in(OK,CLR):
    pass
   return
  show=[c for c in choices if G_fits(c,have)]
  y=G_page(words,air)
  i=G_pick([c[0]for c in show],y)
  if i<0:
   if message(['ENTER: quit the story','CLEAR: keep playing'],'Quit?')==OK:
    return
   continue
  c=show[i]
  for f in c[3]:
   if f not in have:
    have+=f
    if f=='t':
     air+=G_TANK
  at=c[1]
  air-=3 if at=='hide'else 1
  if air<=0:
   cls()
   message(['The air runs out.','Station Kestrel goes','quiet. Try again!'],'Out of air')
   return
G_RULES='You wake alone on a failing space station. Pick what to do in each scene. Find the pod code and escape before the air runs out. Choose carefully!'
G_KEYS=['Up/Down: pick a choice','ENTER: do it','CLEAR: quit']
def G_main():
 while True:
  c=home('GHSPACE','LOST ORBIT',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
