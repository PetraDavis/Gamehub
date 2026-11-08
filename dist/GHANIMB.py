# GHANIMB: part of GHANIM. Keep it next to GHANIM.
from ti_draw import*
from ti_system import*
import time
import random
import math
from ti_system import store_list,recall_list
UP=25
DOWN=34
LEFT=24
RIGHT=26
OK=105
CLR=45
DEL=23
SECOND=21
BLACK=(0,0,0)
WHITE=(255,255,255)
GOLD=(230,180,40)
GREY=(110,110,110)
DARK=(40,40,40)
RED=(220,50,50)
H=210
def key():
 return get_key(0)
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
def pause(s):
 time.sleep(s)
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
I_BLACK=(0,0,0)
I_WHITE=(255,255,255)
I_RED=(215,40,40)
I_BG={'GHANIM':I_WHITE}
def I_c_(c):
 col(c)
def I_box(x,y,w,h,c):
 I_c_(c)
 fill_rect(int(x)-1,int(y)-1,max(1,int(w))+1,max(1,int(h))+1)
def I_circ(x,y,r,c):
 I_c_(c)
 fill_circle(int(x),int(y),int(r))
def I_anim(x,y,c):
 I_box(x-20,y-13,41,27,(35,35,40))
 for i in range(5):
  I_box(x-18+i*8,y-11,4,3,I_WHITE)
  I_box(x-18+i*8,y+9,4,3,I_WHITE)
 for i,by in enumerate((4,-2,2)):
  fx=x-17+i*12
  I_box(fx,y-6,11,13,(120,200,240))
  I_box(fx,y+4,11,3,(70,170,80))
  I_circ(fx+5,y+by,2,(240,120,40))
 I_circ(x+17,y-9,1,I_RED)
I_ICONS={'GHANIM':I_anim}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
S_SLOTS=3
S_PER=100
S_B=5
def S_hname(s):
 return 'A'+str(s)+'H'
def S_dname(s,i):
 n=str(i)
 return 'A'+str(s)+'0'*(3-len(n))+n
def S_wipe(what=3):
 n=0
 for s in range(1,S_SLOTS+1 if what&1 else 1):
  try:
   h=recall_list(S_hname(s))
   nl=int(h[3])
  except Exception:
   continue
  for k in range(nl):
   try:
    store_list(S_dname(s,k),[0])
    n+=1
   except Exception:
    pass
  store_list(S_hname(s),[0])
  n+=1
 for nm in('DRG','DRB')if what&2 else():
  try:
   recall_list(nm)
   store_list(nm,[0])
   n+=1
  except Exception:
   pass
 return n
G_CWD=32
G_CHG=24
G_N=G_CWD*G_CHG
G_P=6
G_CX=6
G_CY=26
G_PAL=((255,255,255),(0,0,0),(128,128,128),(200,200,200),(220,40,40),(245,140,30),(250,220,50),(60,190,70),(20,100,40),(80,200,230),(40,80,200),(20,30,90),(150,60,190),(245,140,190),(130,80,40),(245,200,160))
G_COL=G_PAL+tuple((((r+1020)//5,(g+1020)//5,(b+1020)//5)for r,g,b in G_PAL))
G_INK=(20,20,20)
G_HI=(200,120,0)
G_MAXB=60000
G_KEYGAP=15
class G_Studio:
 pass
def G_chain(s,i):
 n=0
 k=i
 while k>0 and s.F[k][0]!=1:
  k-=1
  n+=1
 return n
def G_used(s):
 t=0
 for f in s.F:
  t+=len(f)+2
 return t
def G_want(s,i):
 v=s.cur[i]
 if v==0 and s.onion and(s.ci>0)and s.prv[i]:
  return 16+s.prv[i]
 return v
def G_paint(s,i,v):
 x=G_CX+i%G_CWD*G_P
 y=G_CY+i//G_CWD*G_P
 rect(x,y,G_P,G_P,G_COL[v])
 s.shown[i]=v
def G_refresh(s,src=None):
 t=src if src is not None else bytearray([G_want(s,i)for i in range(G_N)])
 sh=s.shown
 hb=s.hide if s.hide>=0 and sh[s.hide]==t[s.hide]else-1
 todo={}
 for i in range(G_N):
  v=t[i]
  if sh[i]==v:
   continue
  r=i//G_CWD
  c=i-r*G_CWD
  e=1
  while c+e<G_CWD and t[i+e]==v and(i+e!=hb):
   e+=1
  n=e
  while n>1 and sh[i+n-1]==v:
   n-=1
  best=None
  for w in(e,n)if n<e else(e,):
   h=1
   while r+h<G_CHG:
    j=i+h*G_CWD
    k=0
    while k<w and t[j+k]==v and(j+k!=hb):
     k+=1
    if k<w:
     break
    h+=1
   g=0
   for q in range(h):
    j=i+q*G_CWD
    for k in range(w):
     if sh[j+k]!=v:
      g+=1
   if best is None or g>best[0]:
    best=(g,w,h)
  g,w,h=best
  for q in range(h):
   j=i+q*G_CWD
   for k in range(w):
    sh[j+k]=v
  if v in todo:
   todo[v].append((c,r,w,h))
  else:
   todo[v]=[(c,r,w,h)]
 for v in todo:
  for c,r,w,h in todo[v]:
   rect(G_CX+c*G_P,G_CY+r*G_P,w*G_P,h*G_P,G_COL[v])
def G_cursor(s):
 x=G_CX+s.cx*G_P
 y=G_CY+s.cy*G_P
 v=s.cur[s.cy*G_CWD+s.cx]
 col(BLACK if v in(0,3,6,15)else WHITE)
 draw_rect(x,y,G_P-2,G_P-2)
 s.hide=s.cy*G_CWD+s.cx
def G_uncursor(s):
 i=s.cy*G_CWD+s.cx
 s.hide=-1
 G_paint(s,i,G_want(s,i))
def G_label(s,key,x,y,t,c,bg=WHITE):
 old=s.lab.get(key)
 s.lab[key]=(t,c)
 if old is None:
  text(x,y,t,c)
  return
 o,oc=old
 n=max(len(o),len(t))
 o=o+' '*(n-len(o))
 t2=t+' '*(n-len(t))
 segs=[]
 for k in range(n):
  if o[k]!=t2[k]or(oc!=c and t2[k]!=' '):
   if segs and k-segs[-1][1]<=2:
    segs[-1][1]=k+1
   else:
    segs.append([k,k+1])
 rub=[g for g in segs if o[g[0]:g[1]].strip()]
 for a,b in rub:
  rect(x+a*10,y-12,(b-a)*10,16,bg)
 for a,b in segs:
  w=t2[a:b]
  if w.strip():
   text(x+a*10,y,w,c)
def G_swatch(s,c,sel=-1):
 x=210+c%4*26
 y=30+c//4*26
 e=G_INK if c==sel else GOLD if c==s.col else WHITE
 rect(x-2,y-2,26,2,e)
 rect(x-2,y+22,26,2,e)
 rect(x-2,y,2,22,e)
 rect(x+22,y,2,22,e)
def G_palette(s):
 for c in range(16):
  x=210+c%4*26
  y=30+c//4*26
  rect(x+1,y+1,20,20,G_PAL[c])
 col(GREY)
 draw_rect(210,30,20,20)
 G_swatch(s,s.col)
def G_topbar(s):
 pct=G_used(s)*100//G_MAXB
 G_label(s,'fr',4,17,'Frame '+str(s.ci+1)+'/'+str(len(s.F)),G_INK)
 G_label(s,'fps',160,17,str(s.fps)+'fps',GREY)
 G_label(s,'mem',236,17,'Mem '+str(pct)+'%',RED if pct>90 else GREY)
def G_botbar(s,a=None,b=None):
 if a is None:
  a=('Pen up','PEN DOWN','ERASER')[s.pen]
  ca=G_HI if s.pen else G_INK
 else:
  ca=G_HI
 G_label(s,'b1',6,190,a,ca)
 G_label(s,'b2',6,206,b or 'ENTER pen DEL eraser 2nd menu',GREY)
def G_side(s):
 rect(G_MX,22,320-G_MX,154,WHITE)
 s.lab.pop('on',None)
 s.lab.pop('sv',None)
 G_palette(s)
 G_sidetext(s)
def G_sidetext(s):
 G_label(s,'on',210,150,'Onion '+('on'if s.onion else 'off'),GREY)
 G_label(s,'sv',210,168,'Saved '+(str(s.slot)if s.slot else '-'),GREY)
def G_update(s):
 G_uncursor(s)
 G_refresh(s)
 G_topbar(s)
 G_sidetext(s)
 G_botbar(s)
 G_cursor(s)
def G_set_px(s,i,c):
 if s.cur[i]!=c:
  if not s.dirty:
   s.undo=bytearray(s.cur)
  s.cur[i]=c
  s.dirty=True
  s.changed=True
G_ITEMS=('Color','Fill area','Undo','Wipe frame','Next frame','Prev frame','Add copy','Add blank','Del frame','Play','Speed','Onion skin','Save','Load','New','Quit')
G_MX=202
G_MY=24
G_MH=25
G_MV=6
G_MW=108
G_SBX=G_MX+G_MW+4
G_SBH=G_MV*G_MH-3
G_THH=G_SBH*G_MV//16
def G_thumb_y(top):
 return G_MY+(G_SBH-G_THH)*top//(16-G_MV)
G_RULES='Draw a picture, add frames, and play them back. Saves stay on the calculator.'
G_KEYS=['Arrows: move  ENTER: pen','DEL: eraser  2nd: menu','Menu: colors, frames, play,','speed, save and load']
def G_forget():
 if choose('Delete all saves?',['No, keep them','Yes, delete them'])==1:
  S_wipe(1)
  message(['All your saved','animations are gone.'],'Saves deleted')
