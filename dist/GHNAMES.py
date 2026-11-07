# GHNAMES from GAMEHUB, on its own. Run it.
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
SECOND=21
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
GREY=(110,110,110)
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
I_WHITE=(255,255,255)
I_INK=(20,20,20)
I_GOLD=(230,180,40)
I_BG={'GHNAMES':(20,60,70)}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_poly(xs,ys,c):
 I_c_(c)
 fill_poly([int(v)for v in xs],[int(v)for v in ys])
def I_names(x,y,c):
 I_box(x-14,y-9,28,18,I_WHITE)
 I_poly([x-14,x-21,x-14],[y-9,y,y+9],I_WHITE)
 I_box(x-17,y-1,3,3,(20,60,70))
 I_box(x-8,y-4,17,3,I_GOLD)
 I_box(x-8,y+2,11,3,I_INK)
I_ICONS={'GHNAMES':I_names}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_BGC=(20,60,70)
G_PANEL=(10,35,45)
G_KINDS=(('HERO',('Bra','Kael','Ari','Thor','Lyn','Ro','Zar','Fen','Mir','Dax','El','Tam'),('a','wen','dra','ia','ra','elle','ina','issa'),('dor','ric','ion','mir','lan','vin','eth','an'),('the Brave','the Bold','Swiftfoot','of the North','Lionheart','the True','Stormborn'),('Queen of Blades','the Shieldmaiden','Lady of Light'),('King of Blades','the Shieldbearer','Lord of Light')),('MONSTER',('Grak','Zul','Mog','Skrel','Vor','Bog','Kra','Gul','Thrax','Urg','Snarl','Drog'),('ra','ixa','mira','ella','gra','ssa','atha','ina'),('thor','gash','nok','gor','zak','rot','ug','skar'),('the Hungry','of the Swamp','Bonecrusher','the Smelly','the Endless','of Doom','the Grumpy'),('Swamp Queen','Mother of Bats','the Witch'),('Swamp King','Father of Bats','the Ogre')),('PET',('Mo','Pip','Bis','Wig','Noo','Bun','Fizz','Lol','Pud','Snu','Tib','Zig'),('bella','kins','lily','cupcake','ette','sy','pie','boo'),('chi','ster','bit','pop','muffin','snoot','beans','gus'),('the Fluffy','the Sleepy','the Zoomy','of the Couch','the Brave','the Sneaky'),('the Princess','the Cuddly Queen','the Cute'),('the Prince','the Cuddly King','Jr.')),('WIZARD',('Ald','Mer','Zeph','Quill','Sol','Orin','Vex','Ils','Bram','Nim','Eld','My'),('yra','andra','iel','ana','elle','ora','ina','essa'),('bus','ion','dor','wick','oth','aris','ius','on'),('the Grey','of the Stars','Moonweaver','the Wise','Spellbinder','of the Tower','the Odd'),('the Enchantress','Witch of the Woods','Lady of Spells'),('the Enchanter','Warlock of the Woods','Lord of Spells')),('DRAGON',('Vyr','Draz','Ign','Sca','Fafn','Ryn','Zyth','Kor','Ember','Sil','Tal','Aur'),('ira','essa','yx','andra','eth','ara','ithra','ona'),('ax','gorn','ion','rax','oth','ius','drak','on'),('the Fierce','Flamecaller','of the Peaks','Skyrender','the Ancient','Stormwing','the Shiny'),('Queen of Ashes','Mother of Eggs','the Sky Empress'),('King of Ashes','Father of Eggs','the Sky Emperor')),('PLANET',('Zor','Kep','Vel','Astra','Nyx','Oro','Tal','Xen','Lumi','Cyra','Pol','Rho'),('ax','lon','ia','us','tara','on','is','ix','ara','eon','una','os'),(),('Prime','IV','Minor','VII','Major','B','X'),(),()))
G_GENDERS=('FEMALE','MALE')
def G_one(t):
 return t[random.randint(0,len(t)-1)]
def G_has_gender(k):
 return len(G_KINDS[k][3])>0
def G_make(k,g):
 w,first,fem,male,titles,ftit,mtit=G_KINDS[k]
 ends=male if g and male else fem
 a=G_one(first)+G_one(ends)
 if len(a)>14:
  a=a[:14]
 t=''
 if random.randint(0,1):
  t=G_one(titles+((mtit if g else ftit)if random.randint(0,2)==0 else()))
 return(a,t)
def G_show_kind(k,old=None):
 if old is not None:
  rect(60,38,200,18,G_BGC)
 ctext(50,'< '+G_KINDS[k][0]+' >',GOLD)
def G_show_gender(k,g):
 rect(40,60,240,18,G_BGC)
 if G_has_gender(k):
  text(80,72,G_GENDERS[0],GOLD if g==0 else GREY)
  text(190,72,G_GENDERS[1],GOLD if g==1 else GREY)
def G_show_name(nm):
 rect(24,92,272,70,G_PANEL)
 ctext(120 if nm[1]else 131,nm[0],WHITE)
 if nm[1]:
  ctext(146,nm[1],GOLD)
def G_game():
 k=0
 g=0
 cls(G_BGC)
 ctext(22,'NAME GENERATOR',GOLD)
 rbox(20,88,280,78,8,WHITE,2,G_PANEL)
 ctext(182,'ENTER: new name',GREY)
 ctext(200,'Up/Down: female or male',GREY)
 G_show_kind(k)
 G_show_gender(k,g)
 G_show_name(G_make(k,g))
 while True:
  key_=wkey()
  if key_==CLR:
   return
  if key_ in(LEFT,RIGHT):
   old=k
   k=(k+(1 if key_==RIGHT else-1))%len(G_KINDS)
   G_show_kind(k,old)
   if G_has_gender(k)!=G_has_gender(old):
    G_show_gender(k,g)
   G_show_name(G_make(k,g))
  elif key_ in(UP,DOWN)and G_has_gender(k):
   g=1-g
   G_show_gender(k,g)
   G_show_name(G_make(k,g))
  elif key_ in(OK,SECOND):
   G_show_name(G_make(k,g))
G_RULES='Need a name for a story, a game or a drawing? Pick what it is for, female or male, and press ENTER for as many new names as you like.'
G_KEYS=['Left/Right: what it is for','Up/Down: female or male','ENTER: new name','CLEAR: stop']
def G_main():
 while True:
  c=home('GHNAMES','NAME GENERATOR',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_game()
G_main()
RAN=True
