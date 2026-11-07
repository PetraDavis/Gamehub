# GHDETECT from GAMEHUB, on its own. Run it.
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
DARK=(40,40,40)
H=210
def shuffle(a):
 for i in range(len(a)-1,0,-1):
  j=random.randint(0,i)
  a[i],a[j]=(a[j],a[i])
def sample(seq,k):
 a=list(seq)
 shuffle(a)
 return a[:k]
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
def choose(title,opts,sel=0):
 cls()
 ctext(24,title,GOLD)
 n=len(opts)
 for i in range(n):
  y=40+i*30
  c=GOLD if i==sel else WHITE
  rbox(60,y,200,24,8,c,2,BLACK,False)
  ctext(y+18,opts[i],c)
 while True:
  k=wkey()
  old=sel
  if k==UP:
   sel=(sel-1)%n
  elif k==DOWN:
   sel=(sel+1)%n
  elif k==OK:
   return sel
  elif k==CLR:
   return-1
  if sel==old:
   continue
  for i in(old,sel):
   y=40+i*30
   c=GOLD if i==sel else WHITE
   edge(60,y,200,24,8,c)
   ctext(y+18,opts[i],c)
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
I_BG={'GHDETECT':(35,30,55)}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_circ(x,y,r,c):
 I_c_(c)
 fill_circle(int(x),int(y),int(r))
def I_poly(xs,ys,c):
 I_c_(c)
 fill_poly([int(v)for v in xs],[int(v)for v in ys])
def I_detect(x,y,c):
 I_box(x-14,y+4,6,9,(120,90,60))
 I_box(x-6,y+8,6,9,(120,90,60))
 I_circ(x+2,y-4,11,(230,180,40))
 I_circ(x+2,y-4,8,(190,220,245))
 I_poly([x+9,x+13,x+19,x+15],[y+5,y+1,y+13,y+17],(120,80,40))
I_ICONS={'GHDETECT':I_detect}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_BG=(35,30,55)
G_SKIN=((240,200,160),(200,150,110),(150,100,70),(250,215,185))
G_HAIR=((200,70,40),(30,30,30),(240,210,90),(170,170,175))
G_HAIRN=('red','black','blond','grey')
G_SHIRT=((60,120,230),(200,60,70),(70,170,90),(230,150,40),(150,90,200))
G_NAMES=('Rosa','Hugo','Basil','Lily','Rex','Ada','Tom','Mia','Otto','Ivy','Max','Nell','Finn','Zoe','Gus')
G_LOOT=('the golden cupcake','the museum diamond',"Grandma's recipe","the mayor's hat",'the prize pumpkin','the royal crown')
G_PLACE=('Maple Manor','the town museum','the bakery','the castle','the county fair')
G_ROOMS=('Kitchen','Library','Garden','Attic','Ballroom')
G_MOVES=6
class G_Case:
 pass
def G_new_case():
 c=G_Case()
 c.names=sample(G_NAMES,5)
 while True:
  c.t=[(random.randint(0,3),random.randint(0,1),random.randint(0,1))for i in range(5)]
  c.thief=random.randint(0,4)
  if c.t.count(c.t[c.thief])==1:
   break
 c.skin=[random.randint(0,3)for i in range(5)]
 c.shirt=sample(range(5),5)
 c.loot=random.choice(G_LOOT)
 c.place=random.choice(G_PLACE)
 rooms=sample(range(5),5)
 c.room=[None]*5
 for k in range(3):
  c.room[rooms[k]]=k
 c.searched=[False]*5
 c.asked=[False]*5
 c.notes=[]
 c.moves=G_MOVES
 return c
def G_clue(c,k,true=True):
 h,hat,gl=c.t[c.thief]
 if k==0:
  if not true:
   h=(h+random.randint(1,3))%4
  return G_HAIRN[h]+' hair'
 if k==1:
  return 'a hat'if hat==true else 'no hat'
 return 'glasses'if gl==true else 'no glasses'
def G_room_text(c,k):
 h,hat,gl=c.t[c.thief]
 if k==0:
  return['You find a '+G_HAIRN[h]+' hair','caught on the window.']
 if k==1:
  return['A hat left a ring in','the dust.']if hat else['Muddy hand prints on','a hat stand: no hat.']
 return['A glasses lens lies','under a chair.']if gl else['A note in tiny writing','read without glasses.']
def G_face(c,i,x,y,big=1):
 h,hat,gl=c.t[i]
 r=14*big
 rect(x-r,y+r-2,2*r,r,G_SHIRT[c.shirt[i]])
 circ(x,y,r,G_SKIN[c.skin[i]])
 rect(x-r,y-r,2*r,r//2+1,G_HAIR[h])
 rect(x-r,y-r//2,3*big,r//2+2,G_HAIR[h])
 rect(x+r-3*big,y-r//2,3*big,r//2+2,G_HAIR[h])
 if hat:
  rect(x-r-3*big,y-r-1,2*r+6*big,3*big,DARK)
  rect(x-r+3*big,y-r-9*big,2*r-6*big,9*big,DARK)
 if gl:
  for dx in(-6*big,2*big):
   rect(x+dx,y-2*big,5*big,4*big,BLACK)
   rect(x+dx+big,y-big,3*big,2*big,(200,230,255))
  rect(x-big,y-big,3*big,big,BLACK)
 else:
  rect(x-5*big,y-big,2*big,2*big,BLACK)
  rect(x+3*big,y-big,2*big,2*big,BLACK)
 rect(x-3*big,y+6*big,6*big,big+1,(150,60,60))
def G_lineup(c,title,sel=None):
 cls(G_BG)
 ctext(22,title,GOLD)
 for i in range(5):
  x=32+i*64
  G_face(c,i,x,90)
  text(x-len(c.names[i])*5,140,c.names[i],WHITE)
  if c.asked[i]:
   text(x-15,160,'asked',GREY)
 text(6,186,'Moves left: '+str(c.moves),WHITE)
 if sel is None:
  text(6,204,'ENTER: back',GREY)
  while wkey()not in(OK,CLR):
   pass
  return-1
 text(6,204,'Left/Right, ENTER: pick',GREY)
 while True:
  x=32+sel*64
  rbox(x-30,52,60,96,6,GOLD,2,G_BG,False)
  k=wkey()
  if k==OK:
   return sel
  if k==CLR:
   return-1
  if k in(LEFT,RIGHT):
   rbox(x-30,52,60,96,6,G_BG,2,G_BG,False)
   sel=(sel+(1 if k==RIGHT else-1))%5
def G_notebook(c):
 lines=c.notes[-6:]or['No clues yet.']
 message(lines,'Notebook')
def G_search(c):
 opts=[G_ROOMS[i]+(' (done)'if c.searched[i]else '')for i in range(5)]
 i=choose('Search which room?',opts+['Back'])
 if i<0 or i>=5 or c.searched[i]:
  return
 c.searched[i]=True
 c.moves-=1
 k=c.room[i]
 cls(G_BG)
 if k is None:
  message(['You search everywhere,','but find nothing useful.'],G_ROOMS[i])
  c.notes.append(G_ROOMS[i]+': nothing')
  return
 message(G_room_text(c,k),G_ROOMS[i]+': a clue!')
 c.notes.append(G_ROOMS[i]+': '+G_clue(c,k))
def G_question(c):
 i=G_lineup(c,'Question who?',0)
 if i<0:
  return
 if c.asked[i]:
  cls(G_BG)
  message(['You already asked '+c.names[i]+'.'])
  return
 c.asked[i]=True
 c.moves-=1
 k=random.randint(0,2)
 s=G_clue(c,k,i!=c.thief)
 cls(G_BG)
 G_face(c,i,160,46,2)
 room=random.choice(G_ROOMS)
 message(['I was in the '+room+'.','I saw the thief! They','had '+s+'.'],c.names[i]+' says')
 c.notes.append(c.names[i]+' says: '+s)
def G_accuse(c):
 i=G_lineup(c,'Who is the thief?',0)
 if i<0:
  return False
 cls(G_BG)
 G_face(c,c.thief,160,70,2)
 t=c.names[c.thief]
 h,hat,gl=c.t[c.thief]
 why=[G_HAIRN[h]+' hair, '+('a hat,'if hat else 'no hat,'),'glasses.'if gl else 'no glasses.']
 if i==c.thief:
  message(['You caught '+t+'!']+why+['Case closed. Great work!'],'SOLVED')
 else:
  message([c.names[i]+' is innocent.','It was '+t+':']+why,'Wrong person!')
 return True
def G_play():
 c=G_new_case()
 cls(G_BG)
 message(['Someone stole',c.loot,'at '+c.place+'!','Room clues are true,','but the thief will lie.'],'NEW CASE')
 while True:
  if c.moves<=0:
   cls(G_BG)
   message(['Out of moves!','Time to name the thief.'],'Hurry')
   if G_accuse(c):
    return
   continue
  o=choose('Moves left: '+str(c.moves),['Search a room','Question someone','See suspects','Notebook','Name the thief!'])
  if o==0:
   G_search(c)
  elif o==1:
   G_question(c)
  elif o==2:
   G_lineup(c,'The suspects')
  elif o==3:
   G_notebook(c)
  elif o==4:
   if G_accuse(c):
    return
  else:
   cls(G_BG)
   if message(['ENTER: quit this case','CLEAR: keep going'],'Quit?')==OK:
    return
G_RULES='Something was stolen! Search rooms for clues and question the 5 suspects, then name the thief. Clues in rooms are always true, but the thief lies. You only have 6 moves. Every case is different.'
G_KEYS=['Up/Down + ENTER: choose','Left/Right: pick a suspect','CLEAR: back']
def G_main():
 while True:
  c=home('GHDETECT','DETECTIVE CASE',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_play()
G_main()
RAN=True
