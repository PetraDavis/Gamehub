# GHANIM from GAMEHUB, on its own. Run it.
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
def vacate(ox,oy,nx,ny,w,h,c):
 if abs(nx-ox)>=w or abs(ny-oy)>=h:
  rect(ox,oy,w,h,c)
  return
 if ny>oy:
  rect(ox,oy,w,ny-oy,c)
 elif ny<oy:
  rect(ox,ny+h,w,oy-ny,c)
 y0=max(oy,ny)
 y1=min(oy,ny)+h
 if nx>ox:
  rect(ox,y0,nx-ox,y1-y0,c)
 elif nx<ox:
  rect(nx+w,y0,ox-nx,y1-y0,c)
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
I_RED=(215,40,40)
I_BG={'GHANIM':I_WHITE}
def I_c_(c):
 set_color(c[0],c[1],c[2])
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
def S_info(s):
 try:
  h=recall_list(S_hname(s))
  if len(h)>=4 and int(h[0])==1:
   return(int(h[1]),int(h[2]))
 except Exception:
  pass
 return None
def S_save(s,data,frames,fps,show=None):
 nums=[]
 n=len(data)
 i=0
 while i<n:
  v=0
  for j in range(S_B):
   v=v*256+(data[i+j]if i+j<n else 0)
  nums.append(v)
  i+=S_B
 nl=(len(nums)+S_PER-1)//S_PER
 for k in range(nl):
  if show:
   show(k,nl)
  store_list(S_dname(s,k),nums[k*S_PER:(k+1)*S_PER])
 old=0
 try:
  old=int(recall_list(S_hname(s))[3])
 except Exception:
  pass
 for k in range(nl,old):
  try:
   store_list(S_dname(s,k),[0])
  except Exception:
   pass
 store_list(S_hname(s),[1,frames,fps,nl,n])
 return nl
def S_load(s,show=None):
 h=recall_list(S_hname(s))
 frames,fps,nl,n=(int(h[1]),int(h[2]),int(h[3]),int(h[4]))
 data=bytearray(n)
 p=0
 for k in range(nl):
  if show:
   show(k,nl)
  for v in recall_list(S_dname(s,k)):
   v=int(v)
   chunk=[]
   for j in range(S_B):
    chunk.append(v%256)
    v//=256
   for j in range(S_B-1,-1,-1):
    if p<n:
     data[p]=chunk[j]
     p+=1
 return(data,frames,fps)
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
def G_enc_key(fr):
 out=bytearray([1])
 i=0
 while i<G_N:
  c=fr[i]
  n=1
  while i+n<G_N and fr[i+n]==c and(n<255):
   n+=1
  out.append(n)
  out.append(c)
  i+=n
 return bytes(out)
def G_enc_delta(prev,fr):
 out=bytearray([0])
 pos=0
 i=0
 while i<G_N:
  if fr[i]==prev[i]:
   i+=1
   continue
  j=i
  last=i
  while j<G_N and j-i<254:
   if fr[j]!=prev[j]:
    j+=1
    last=j
   elif j+1<G_N and fr[j+1]!=prev[j+1]:
    j+=1
   else:
    break
  j=last
  skip=i-pos
  while skip>255:
   out.append(255)
   out.append(0)
   skip-=255
  out.append(skip)
  out.append(j-i)
  t=i
  while t<j:
   hi=fr[t]
   lo=fr[t+1]if t+1<j else 0
   out.append(hi*16+lo)
   t+=2
  pos=j
  i=j
 return bytes(out)
def G_apply(fr,d):
 if d[0]==1:
  p=1
  i=0
  while p<len(d):
   n=d[p]
   c=d[p+1]
   for t in range(n):
    fr[i+t]=c
   i+=n
   p+=2
  return
 p=1
 pos=0
 L=len(d)
 while p<L:
  pos+=d[p]
  n=d[p+1]
  p+=2
  for t in range(n):
   b=d[p+t//2]
   fr[pos+t]=b>>4 if t%2==0 else b&15
  p+=(n+1)//2
  pos+=n
class G_Studio:
 pass
def G_dec(s,i):
 k=i
 while k>0 and s.F[k][0]!=1:
  k-=1
 fr=bytearray(G_N)
 for j in range(k,i+1):
  G_apply(fr,s.F[j])
 return fr
def G_chain(s,i):
 n=0
 k=i
 while k>0 and s.F[k][0]!=1:
  k-=1
  n+=1
 return n
def G_encode_at(s,i,fr,prev):
 if prev is None:
  return G_enc_key(fr)
 d=G_enc_delta(prev,fr)
 if i>0 and G_chain(s,i-1)+1>=G_KEYGAP:
  return G_enc_key(fr)
 return d
def G_commit(s):
 if not s.dirty:
  return
 i=s.ci
 nx=None
 if i+1<len(s.F)and s.F[i+1][0]==0:
  nx=G_dec(s,i+1)
 s.F[i]=G_encode_at(s,i,s.cur,s.prv if i>0 else None)
 if nx is not None:
  s.F[i+1]=G_enc_delta(s.cur,nx)
 s.dirty=False
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
def G_full(s):
 cls(WHITE)
 rect(G_CX-2,G_CY-2,G_CWD*G_P+4,2,DARK)
 rect(G_CX-2,G_CY+G_CHG*G_P,G_CWD*G_P+4,2,DARK)
 rect(G_CX-2,G_CY,2,G_CHG*G_P,DARK)
 rect(G_CX+G_CWD*G_P,G_CY,2,G_CHG*G_P,DARK)
 s.shown=bytearray(G_N)
 s.hide=-1
 s.lab={}
 G_refresh(s)
 G_side(s)
 G_topbar(s)
 G_botbar(s)
 G_cursor(s)
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
def G_fill(s):
 i0=s.cy*G_CWD+s.cx
 old=s.cur[i0]
 new=s.col
 if old==new:
  return
 s.undo=bytearray(s.cur)
 stack=[i0]
 while stack:
  i=stack.pop()
  if s.cur[i]!=old:
   continue
  s.cur[i]=new
  x=i%G_CWD
  if x>0:
   stack.append(i-1)
  if x<G_CWD-1:
   stack.append(i+1)
  if i>=G_CWD:
   stack.append(i-G_CWD)
  if i<G_N-G_CWD:
   stack.append(i+G_CWD)
 s.dirty=True
 s.changed=True
def G_go(s,j):
 G_commit(s)
 if j==s.ci+1:
  s.prv=s.cur
  s.cur=bytearray(s.prv)
  G_apply(s.cur,s.F[j])
 else:
  s.cur=G_dec(s,j)
  s.prv=G_dec(s,j-1)if j>0 else bytearray(G_N)
 s.ci=j
 s.undo=None
def G_add_frame(s,blank):
 if G_used(s)>G_MAXB:
  message(['Memory is full.','Save, or delete frames.'],"Can't add")
  s.broke=True
  return
 G_commit(s)
 i=s.ci
 nx=G_dec(s,i+1)if i+1<len(s.F)else None
 new=bytearray(G_N)if blank else bytearray(s.cur)
 s.F.insert(i+1,G_enc_delta(s.cur,new))
 if nx is not None and s.F[i+2][0]==0:
  s.F[i+2]=G_enc_delta(new,nx)
 s.prv=s.cur
 s.cur=new
 s.ci=i+1
 s.changed=True
def G_del_frame(s):
 if len(s.F)==1:
  s.undo=bytearray(s.cur)
  s.cur=bytearray(G_N)
  s.dirty=True
  return
 i=s.ci
 nx=G_dec(s,i+1)if i+1<len(s.F)else None
 p=G_dec(s,i-1)if i>0 else None
 del s.F[i]
 if nx is not None:
  s.F[i]=G_enc_key(nx)if p is None else G_enc_delta(p,nx)
 if i>=len(s.F):
  i=len(s.F)-1
 s.dirty=False
 s.ci=i
 s.cur=G_dec(s,i)
 s.prv=G_dec(s,i-1)if i>0 else bytearray(G_N)
 s.changed=True
def G_play(s):
 G_commit(s)
 G_uncursor(s)
 G_botbar(s,'Playing. Up/Down: speed','Any other key stops')
 i=0
 fr=bytearray(G_N)
 while True:
  if s.F[i][0]==1 or i==0:
   fr=bytearray(G_N)
  G_apply(fr,s.F[i])
  G_refresh(s,fr)
  G_label(s,'fr',4,17,'Frame '+str(i+1)+'/'+str(len(s.F)),G_INK)
  steps=max(1,12//s.fps)
  stop=False
  for q in range(steps):
   k=key()
   if k==UP and s.fps<12:
    s.fps+=1
    G_topbar(s)
   elif k==DOWN and s.fps>1:
    s.fps-=1
    G_topbar(s)
   elif k and k not in(UP,DOWN):
    stop=True
    break
   pause(1/12)
  if stop:
   break
  i=(i+1)%len(s.F)
 while key():
  pass
 s.cur=G_dec(s,s.ci)
 G_update(s)
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
def G_scrollbar(top,old=None):
 if old is None:
  rect(G_SBX,G_MY,5,G_SBH,DARK)
 elif old==top:
  return
 else:
  a,b=(G_thumb_y(old),G_thumb_y(top))
  vacate(G_SBX,a,G_SBX,b,5,G_THH,DARK)
  vacate(G_SBX,b,G_SBX,a,5,G_THH,WHITE)
  return
 rect(G_SBX,G_thumb_y(top),5,G_THH,WHITE)
def G_mbox(x,y,w,h,c):
 rect(x+2,y,w-4,2,c)
 rect(x+2,y+h-2,w-4,2,c)
 rect(x,y+2,2,h-4,c)
 rect(x+w-2,y+2,2,h-4,c)
def G_mrows(s,top,sel):
 boxes=[]
 rub=[]
 words=[]
 for r in range(G_MV):
  i=top+r
  y=G_MY+r*G_MH
  c=GOLD if i==sel else WHITE
  if s.lab.get(('mb',r))!=c:
   boxes.append((c,y))
   s.lab['mb',r]=c
  old=s.lab.get(('m',r))
  t=G_ITEMS[i]
  if old!=(t,c):
   if old and old[0]!=t:
    rub.append((y,len(old[0])))
   words.append((c,y,t))
   s.lab['m',r]=(t,c)
 boxes.sort()
 for c,y in boxes:
  G_mbox(G_MX+1,y,G_MW,22,c)
 for y,n in rub:
  rect(G_MX+5,y+4,n*10,16,BLACK)
 words.sort()
 for c,y,t in words:
  text(G_MX+5,y+16,t,c)
def G_menu(s,sel):
 rect(G_MX,22,320-G_MX,154,BLACK)
 for r in range(G_MV):
  s.lab.pop(('mb',r),None)
  s.lab.pop(('m',r),None)
 G_botbar(s,'MENU  Up/Down: pick','ENTER: do it  2nd: close')
 top=min(max(0,sel-2),16-G_MV)
 G_mrows(s,top,sel)
 G_scrollbar(top)
 while True:
  k=wkey()
  old=sel
  if k==UP:
   sel=(sel-1)%16
  elif k==DOWN:
   sel=(sel+1)%16
  elif k in(LEFT,RIGHT):
   sel=(sel+8)%16
  elif k==OK:
   break
  elif k in(CLR,SECOND):
   sel=-1
   break
  nt=top
  if sel<top:
   nt=sel
  elif sel>=top+G_MV:
   nt=sel-G_MV+1
  G_scrollbar(nt,top)
  top=nt
  G_mrows(s,top,sel)
 G_side(s)
 G_botbar(s)
 return sel
def G_pick_color(s):
 sel=s.col
 G_swatch(s,sel,sel)
 G_botbar(s,'Arrows: pick a colour','ENTER: use it  CLEAR: back')
 while True:
  k=wkey()
  old=sel
  if k==LEFT:
   sel=(sel-1)%16
  elif k==RIGHT:
   sel=(sel+1)%16
  elif k==UP:
   sel=(sel-4)%16
  elif k==DOWN:
   sel=(sel+4)%16
  elif k==OK:
   old=s.col
   s.col=sel
   G_swatch(s,old)
   break
  elif k==CLR:
   break
  if sel!=old:
   G_swatch(s,old,sel)
   G_swatch(s,sel,sel)
 G_swatch(s,sel)
 G_swatch(s,s.col)
 G_botbar(s)
def G_pick_speed(s):
 cls()
 ctext(80,'PLAYBACK SPEED',GOLD)
 ctext(140,'ENTER done',GREY)
 s.lab={}
 while True:
  t='< '+str(s.fps)+' frames a second >'
  G_label(s,'sp',160-len(t)*5,110,t,WHITE,BLACK)
  k=wkey()
  if k==LEFT and s.fps>1:
   s.fps-=1
  elif k==RIGHT and s.fps<12:
   s.fps+=1
  elif k in(OK,CLR):
   return
def G_pick_slot(title):
 opts=[]
 for sl in range(1,S_SLOTS+1):
  inf=S_info(sl)
  opts.append('Slot '+str(sl)+(': '+str(inf[0])+' fr'if inf else ': empty'))
 opts.append('Cancel')
 c=choose(title,opts)
 if c<0 or c==S_SLOTS:
  return 0
 return c+1
def G_progress(k,n):
 rect(60,120,200,30,BLACK)
 rbox(60,120,200,16,6,WHITE)
 rect(64,124,max(2,192*(k+1)//n),8,GOLD)
def G_do_save(s):
 G_commit(s)
 sl=G_pick_slot('SAVE TO')
 if not sl:
  return
 cls()
 ctext(100,'Saving...',GOLD)
 data=bytearray()
 for f in s.F:
  data.append(len(f)//256)
  data.append(len(f)%256)
  data.extend(f)
 try:
  S_save(sl,data,len(s.F),s.fps,G_progress)
  s.slot=sl
  s.changed=False
  message([str(len(s.F))+' frames saved','to slot '+str(sl)+'.'],'Saved')
 except Exception as e:
  message(['Could not save:',str(e)[:24]],'Error')
def G_do_load(s):
 sl=G_pick_slot('LOAD FROM')
 if not sl or not S_info(sl):
  return
 if s.changed and message(['Unsaved changes will','be lost. ENTER: load','CLEAR: cancel'],'Load?')!=OK:
  return
 cls()
 ctext(100,'Loading...',GOLD)
 try:
  data,frames,fps=S_load(sl,G_progress)
 except Exception as e:
  message(['Could not load:',str(e)[:24]],'Error')
  return
 F=[]
 p=0
 for k in range(frames):
  n=data[p]*256+data[p+1]
  F.append(bytes(data[p+2:p+2+n]))
  p+=2+n
 G_reset(s,F,fps)
 s.slot=sl
def G_reset(s,F,fps):
 s.F=F
 s.fps=fps
 s.ci=0
 s.cur=G_dec(s,0)
 s.prv=bytearray(G_N)
 s.dirty=False
 s.changed=False
 s.undo=None
 s.slot=0
def G_studio():
 s=G_Studio()
 G_reset(s,[G_enc_key(bytearray(G_N))],6)
 s.cx=16
 s.cy=12
 s.col=1
 s.pen=0
 s.onion=True
 s.shown=bytearray([255]*G_N)
 s.hide=-1
 s.lab={}
 msel=0
 G_full(s)
 held=0
 hc=0
 while True:
  k=key()
  if k==held and k:
   hc+=1
  else:
   hc=0
  rep=k!=held or(hc>3 and hc%1==0)
  held=k
  if not k:
   pause(0.01)
   continue
  if k in(LEFT,RIGHT,UP,DOWN)and rep:
   G_uncursor(s)
   if k==LEFT and s.cx>0:
    s.cx-=1
   elif k==RIGHT and s.cx<G_CWD-1:
    s.cx+=1
   elif k==UP and s.cy>0:
    s.cy-=1
   elif k==DOWN and s.cy<G_CHG-1:
    s.cy+=1
   if s.pen:
    i=s.cy*G_CWD+s.cx
    G_set_px(s,i,s.col if s.pen==1 else 0)
    G_paint(s,i,G_want(s,i))
   G_cursor(s)
   continue
  if not rep:
   continue
  if k==OK or k==DEL:
   want_pen=1 if k==OK else 2
   s.pen=0 if s.pen==want_pen else want_pen
   if s.pen:
    i=s.cy*G_CWD+s.cx
    G_set_px(s,i,s.col if s.pen==1 else 0)
    if s.shown[i]!=G_want(s,i):
     G_uncursor(s)
     G_cursor(s)
   G_botbar(s)
   G_topbar(s)
   continue
  if k==CLR and s.pen:
   s.pen=0
   G_botbar(s)
   continue
  if k==SECOND or k==CLR:
   s.pen=0
   c=G_menu(s,msel)
   if c>=0:
    msel=c
   s.broke=False
   if c==0:
    G_pick_color(s)
   elif c==1:
    G_fill(s)
   elif c==2 and s.undo is not None:
    u=s.undo
    s.undo=bytearray(s.cur)
    s.cur=u
    s.dirty=True
   elif c==3:
    s.undo=bytearray(s.cur)
    s.cur=bytearray(G_N)
    s.dirty=True
   elif c==4:
    if s.ci+1<len(s.F):
     G_go(s,s.ci+1)
    else:
     G_add_frame(s,False)
   elif c==5 and s.ci>0:
    G_go(s,s.ci-1)
   elif c==6:
    G_add_frame(s,False)
   elif c==7:
    G_add_frame(s,True)
   elif c==8:
    G_del_frame(s)
   elif c==9:
    G_play(s)
   elif c==10:
    G_pick_speed(s)
    s.broke=True
   elif c==11:
    s.onion=not s.onion
   elif c==12:
    G_do_save(s)
    s.broke=True
   elif c==13:
    G_do_load(s)
    s.broke=True
   elif c==14:
    if s.changed:
     s.broke=True
    if not s.changed or message(['Unsaved changes will','be lost. ENTER: new','CLEAR: cancel'],'New?')==OK:
     G_reset(s,[G_enc_key(bytearray(G_N))],6)
   elif c==15:
    if not s.changed or message(['Unsaved changes will','be lost. ENTER: quit','CLEAR: cancel'],'Quit?')==OK:
     return
    s.broke=True
   if s.broke:
    G_full(s)
   elif c!=9:
    G_update(s)
G_RULES='Draw a picture, add frames, and play them back. Saves stay on the calculator.'
G_KEYS=['Arrows: move  ENTER: pen','DEL: eraser  2nd: menu','Menu: colors, frames, play,','speed, save and load']
def G_main():
 while True:
  c=home('GHANIM','ANIMATION STUDIO',G_RULES,G_KEYS,('Play','Back'))
  if c<0:
   return
  G_studio()
G_main()
RAN=True
