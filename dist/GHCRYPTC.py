# GHCRYPTC: part of GHCRYPTP. Keep it next to GHCRYPTP.
from ti_draw import*
from ti_system import*
import time
import random
import math
import gc
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
def _corners(x,y,w,h,r,t):
 return((x,y,w,t),(x,y+h-t,w,t),(x,y+t,t,h-2*t),(x+w-t,y+t,t,h-2*t))
def rbox(x,y,w,h,r,c,t=2,inner=BLACK,fill=True):
 edge(x,y,w,h,r,c,t)
 if fill:
  rect(x+t,y+t,w-2*t,h-2*t,inner)
def edge(x,y,w,h,r,c,t=2,inner=BLACK):
 col(c)
 for bx,by,bw,bh in _corners(x,y,w,h,r,t):
  if bw>0 and bh>0:
   fr(bx,by,bw,bh)
def pause(s):
 time.sleep(s)
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
try:
 from time import monotonic as G_now
except Exception:
 G_now=None
G_MAP=['#BBBB###SSS###','B....#.......#','B............k','#####G.......#','#....#.......#','T....l.......j','#....#.......C','########PF####']
G_VW=320
G_VH=172
G_COLS=32
G_CWID=G_VW//G_COLS
G_FOV=1.0
G_WALL=(75,95,99)
G_DOOR=(110,75,45)
G_FLOOR=(42,36,32)
G_CEIL=(16,16,18)
G_LINK1='petradavis.github.io/'
G_LINK2='Encrypted/?ysolde=1'
G_CIPHER='LI WKH OLJKWV GLH VKH LV LQ WKH URRP. GRQW UXQ. KLGH LQ WKH FRDW FORVHW. LWV FRGH LV HFKR'
G_TAPGRID=('ABCDE','FGHIK','LMNOP','QRSTU','VWXYZ')
G_KNOCKS=((4,1),(4,5),(2,4),(1,5),(4,4))
class G_St:
 pass
G_SPRD=b'\xa6\x04\x00\xff\x003\x96(-\x14\xeb3\\x\x1e#\x00\x1f3G\x96(-\xe0\xff3G\x96(-\x99\x04\x00\x1a\x00L_A(\xe6\xff\x00L_A(\x00\xffLYxU23\x80Ya\xc8\xbe\x96L\x02s\x8c\x00\x8c\xb4\x96F&\xd9\x8c\xb8\xeb\xdc\xaaL\x04\x00&\x00L_A(\xd9\xff\x00L_A(\x00\xffLWxU2@\xbfWk\x14\x14\x14Y\x03u\x8a\x00\xccP7#&sY\xbf<Fn\x8c\xd9f\xb8n22s\x04\x00\x1f\x00G_A(\xe0\xff\x00G_A(\x00\xffGTxU2L\xb2T^\x8cF\xb4Y\x03\x1a\xe6\x00@_A(Y\xa6@s<x\x8cL\xb2s\x8cZ\x8cF'
G_SPR={}
G_ROOMS=(('Library',0,0,5,3),('Living Room',0,3,5,8),('Grand Foyer',5,0,14,8))
def G_tile(x,y):
 if 0<=y<len(G_MAP)and 0<=int(x)<14:
  return G_MAP[int(y)][int(x)]
 return '#'
def G_solid(g,x,y):
 t=G_tile(x,y)
 if t=='l'and g.living:
  return False
 return t!='.'
def G_room(g):
 for n,x0,y0,x1,y1 in G_ROOMS:
  if x0<=g.x<x1 and y0<=g.y<y1:
   return n
 return 'Grand Foyer'
def G_clock():
 return G_now()if G_now else 0
def G_shade(c,k):
 return min(255,int(c[0]*k))<<16|min(255,int(c[1]*k))<<8|min(255,int(c[2]*k))
def G_light(g,i,d):
 if g.blackout:
  base=0.0
 elif g.power:
  base=max(0.35,1.0-d/14)
 else:
  base=0.06
 if g.flash:
  off=abs(i-G_COLS/2)/(G_COLS*0.32)
  if off<1:
   base+=(1-off)*max(0,1-d/12)*(1.1 if not g.power else 0.35)
 return min(1.2,base)
def G_colour(t):
 if t in 'lkjCF':
  return G_DOOR
 if t=='S':
  return(120,90,60)
 if t=='B':
  return(90,60,35)
 return G_WALL
def G_lq(k):
 return int(k*5+0.5)/5
def G_put(sp,a,b,c):
 if b<=a:
  return sp
 out=[]
 for y0,y1,cc in sp:
  if y0<a:
   out.append((y0,min(y1,a),cc))
 out.append((a,b,c))
 for y0,y1,cc in sp:
  if y1>b:
   out.append((max(y0,b),y1,cc))
 return out
def G_diff(old,new):
 if old is None:
  return new
 out=[]
 i=j=0
 y=0
 while y<G_VH:
  o0,o1,oc=old[i]
  n0,n1,nc=new[j]
  e=min(o1,n1)
  if oc!=nc:
   if out and out[-1][1]==y and(out[-1][2]==nc):
    out[-1]=(out[-1][0],e,nc)
   else:
    out.append((y,e,nc))
  y=e
  if o1==e:
   i+=1
  if n1==e:
   j+=1
 return out
G_YSD=b"{\x85\xce\xd3\x00|\x86\xd1\xd7\x00}\x87\xd5\xda\x00~\x88\xd8\xdd\x00\x80\x8b\xdb\xe1\x00\x84\x8f\xdf\xe6\x00t\x89\xcf\xd2\x05b\x9b\xcc\xcf\x00c\x9f\xc9\xcc\x00c\x9e\xc6\xc9\x00d\x9d\xc2\xc6\x00e\x9c\xbf\xc2\x00e\x9b\xbc\xbf\x00f\x9a\xb9\xbc\x00g\x99\xb6\xb9\x00h\x98\xb2\xb6\x00h\x97\xaf\xb2\x00i\x96\xac\xaf\x00j\x95\xa9\xac\x00j\x95\xa6\xa9\x00k\x94\xa3\xa6\x00l\x93\x9f\xa3\x00l\x93\x9c\x9f\x00m\x92\x99\x9c\x00k\x94\x99\x9b\x00j\x95\x97\x99\x00i\x96\x94\x97\x00h\x97\x92\x94\x00g\x98\x8f\x92\x00f\x99\x8d\x8f\x00e\x9a\x8b\x8d\x00d\x9b\x88\x8b\x00c\x9c\x86\x88\x00b\x9d\x83\x86\x00a\x9e\x81\x83\x00`\x9f\x7f\x81\x00_\xa0|\x7f\x00^\xa1z|\x00^\x9cxz\x00^\x98ux\x05ry{\x81\x00qyx}\x00qxuz\x00qxqw\x00pxns\x00pwkp\x00pwhm\x00owdj\x00ovaf\x00nv^c\x00nvZ`\x00nuW\\\x00muTY\x00mtQV\x00mtMS\x00ltJO\x00lsGL\x00mzCI\x00s{?E\x00sz<A\x00rz9>\x00qy5;\x00qx27\x00pw/4\x00ow+1\x00nv(-\x00nu%*\x00mu!'\x00lt\x1e#\x00ls\x1b \x00ks\x17\x1d\x00jr\x14\x19\x00jq\x11\x16\x00ip\r\x13\x00hp\n\x10\x00dn\x07\x0c\x00_i\x04\t\x00\x88\x8f{\x81\x00\x88\x90x}\x00\x89\x90tz\x00\x89\x90qw\x00\x89\x91ns\x00\x8a\x91kp\x00\x8a\x91gm\x00\x8a\x92di\x00\x8b\x92af\x00\x8b\x92]c\x00\x8b\x93Z_\x00\x8c\x93W\\\x00\x8c\x94SY\x00\x8c\x94PU\x00\x8d\x94MR\x00\x8d\x95IO\x00\x8e\x95FK\x00\x86\x93AH\x00\x84\x8c>C\x00\x85\x8d;@\x00\x86\x8d8=\x00\x86\x8e4:\x00\x87\x8f16\x00\x88\x90.3\x00\x89\x91+0\x00\x8a\x91(-\x00\x8b\x92$*\x00\x8b\x93!&\x00\x8c\x94\x1e#\x00\x8d\x95\x1b \x00\x8e\x96\x18\x1d\x00\x8f\x96\x14\x1a\x00\x90\x97\x11\x17\x00\x90\x98\x0e\x13\x00\x91\x99\x0b\x10\x00\x93\x9e\x07\r\x00\x99\xa4\x03\t\x00`f\xc8\xcd\x00_e\xc4\xca\x00^d\xc1\xc7\x00]c\xbe\xc3\x00\\b\xbb\xc0\x00[a\xb8\xbd\x00Z`\xb4\xba\x00X_\xb1\xb6\x00W^\xae\xb3\x00V]\xab\xb0\x00U\\\xa7\xad\x00T[\xa4\xa9\x00SY\xa1\xa6\x00RX\x9e\xa3\x00QW\x9a\xa0\x00R]\x96\x9c\x00X^\x92\x98\x00W]\x8f\x94\x00V]\x8c\x91\x00V\\\x88\x8e\x00U[\x85\x8a\x00TZ\x82\x87\x00SY~\x84\x00RX{\x80\x00QXx}\x00QWtz\x00PVqv\x00OUns\x00NTkp\x00MSgm\x00LSdi\x00LRaf\x00KQ]c\x00JPZ_\x00IOW\\\x00\x9b\xa1\xc8\xcd\x00\x9c\xa2\xc5\xca\x00\x9d\xa4\xc1\xc7\x00\x9e\xa5\xbe\xc3\x00\xa0\xa6\xbb\xc0\x00\xa1\xa7\xb8\xbd\x00\xa2\xa8\xb5\xba\x00\xa3\xaa\xb1\xb7\x00\xa4\xab\xae\xb4\x00\xa6\xac\xab\xb0\x00\xa7\xad\xa8\xad\x00\xa8\xae\xa5\xaa\x00\xa9\xb0\xa2\xa7\x00\xaa\xb1\x9e\xa4\x00\xac\xb2\x9b\xa0\x00\xa4\xb0\x96\x9d\x00\xa3\xa9\x92\x98\x00\xa4\xaa\x8f\x94\x00\xa5\xab\x8c\x91\x00\xa6\xac\x88\x8e\x00\xa7\xad\x85\x8b\x00\xa8\xae\x82\x87\x00\xa9\xaf\x7f\x84\x00\xaa\xb0{\x81\x00\xab\xb1x}\x00\xac\xb2uz\x00\xad\xb3rw\x00\xae\xb4nt\x00\xaf\xb5kp\x00\xb0\xb6hm\x00\xb1\xb7dj\x00\xb2\xb8af\x00\xb3\xb9^c\x00\xb4\xba[`\x00KNSY\x00LOPU\x00MPLR\x00NQIN\x00OREK\x00PSBG\x00PS>D\x00OR;@\x00KMSY\x00KMPU\x00KNLR\x00LNIN\x00LNFK\x00LNBH\x00LO?D\x00JN:A\x00JMSY\x00JLPU\x00JLLR\x00ILIN\x00IKEK\x00IKBG\x00HK?D\x00FI<A\x00EH8>\x00JMSY\x00ILPU\x00HKLR\x00GJIN\x00GIFK\x00FHBH\x00EG?D\x00CF;A\x00@D7=\x00ILSY\x00HKPU\x00FILR\x00DGIN\x00CFEK\x00ADBG\x00?B>D\x00=@:@\x00;>6<\x00\xb5\xb8W]\x00\xb4\xb7TY\x00\xb3\xb6PV\x00\xb2\xb5MR\x00\xb1\xb4IO\x00\xb0\xb3FK\x00\xb0\xb3BH\x00\xb1\xb4?D\x00\xb6\xb8W]\x00\xb6\xb8TY\x00\xb5\xb8PV\x00\xb5\xb7MR\x00\xb5\xb7JO\x00\xb5\xb7FL\x00\xb4\xb7CH\x00\xb5\xb9>E\x00\xb6\xb9W]\x00\xb7\xb9TY\x00\xb7\xb9PV\x00\xb7\xbaMR\x00\xb8\xbaIO\x00\xb8\xbaFK\x00\xb8\xbbCH\x00\xba\xbd@E\x00\xbb\xbe<B\x00\xb6\xb9W]\x00\xb7\xbaTY\x00\xb8\xbbPV\x00\xb9\xbcMR\x00\xba\xbcJO\x00\xbb\xbdFL\x00\xbc\xbeCH\x00\xbd\xc0?E\x00\xbf\xc3;A\x00\xb7\xbaW]\x00\xb8\xbbTY\x00\xba\xbdPV\x00\xbc\xbfMR\x00\xbd\xc0IO\x00\xbf\xc2FK\x00\xc1\xc4BH\x00\xc3\xc6>D\x00\xc5\xc8:@\x00\x8d\x93\xf4\xf5\x05\x87\x99\xf2\xf4\x00\x81\xa0\xf1\xf2\x00|\xa0\xef\xf1\x00x\x9f\xed\xef\x00t\x9e\xec\xed\x00p\x9e\xea\xec\x00l\x9d\xe9\xea\x00h\x9b\xe7\xe9\x00d\x98\xe5\xe7\x00b\x96\xe4\xe5\x00`\x94\xe2\xe4\x00^\x92\xe1\xe2\x00\\\x90\xdf\xe1\x00Y\x8d\xdd\xdf\x00W\x8b\xdc\xdd\x00U\x89\xda\xdc\x00S\x87\xd9\xda\x00Q\x85\xd7\xd9\x00N\x82\xd5\xd7\x00L\x80\xd4\xd5\x00J~\xd2\xd4\x00Hz\xd1\xd2\x00Fv\xcf\xd1\x00`q\xcd\xcf\x00`m\xcc\xcd\x00_h\xca\xcc\x00_d\xc9\xca\x00^_\xc7\xc9\x05\x8a\x99\xf3\xf4\x05\x84\x9c\xf1\xf3\x00\x80\x9e\xef\xf1\x00}\x9f\xee\xef\x00{\x9e\xec\xee\x00z\x9e\xeb\xec\x00y\x9d\xe9\xeb\x00x\x9b\xe8\xe9\x00y\x98\xe6\xe8\x00z\x95\xe4\xe6\x00|\x90\xe3\xe4\x00\x84\x86\xe1\xe3\x05\x87\x8b\xee\xef\x04\x93\x97\xeb\xec\x04"
G_YG=4
G_RIM=((215,215,225),(170,175,190),(250,250,255))
G_INSIDE=(36,36,44)
def G_ys_place(g,zb,ca,sa):
 if not g.ys_vis:
  return None
 dx=g.yx-g.x
 dy=g.yy-g.y
 fwd=dx*ca+dy*sa
 if fwd<0.2:
  return None
 cx=(-dx*sa+dy*ca)/fwd/(G_FOV*0.5*1.15)
 scol=(cx+1)/2*G_COLS
 half=0.45/2/fwd/(G_FOV*0.5*1.15)*G_COLS/2
 h=int(G_VH*1.35/fwd)&~7
 top=(G_VH-h)//2
 a=None
 b=0
 for i in range(max(0,int(scol-half)),min(G_COLS,int(scol+half)+1)):
  if zb[i]>=fwd:
   if a is None:
    a=i
   b=i+1
 if a is None:
  return None
 left=int((scol-half)*G_CWID)&~3
 return((left,int(2*half*G_CWID)&~3,top,h,a,b),a,b)
def G_ys_shimmer(g):
 if not g.rim:
  return
 for n in range(3):
  x,y,w,h=random.choice(g.rim)
  rect(x,y,w,h,random.choice(G_RIM))
def G_wrap(s,n=30):
 out=[]
 for para in s.split('\n'):
  line=''
  for w in para.split(' '):
   if len(line)+len(w)+1>n:
    out.append(line)
    line=w
   else:
    line=(line+' '+w).strip()
  out.append(line)
 return out
def G_page(title,body,color=WHITE):
 lines=G_wrap(body)
 per=9
 for p in range(0,len(lines),per):
  cls()
  ctext(20,title,GOLD)
  y=44
  for ln in lines[p:p+per]:
   text(10,y,ln,color)
   y+=17
  more=p+per<len(lines)
  text(10,204,'ENTER: more'if more else 'ENTER/CLEAR: close',GREY)
  while True:
   k=wkey()
   if k in(OK,CLR):
    break
  if k==CLR:
   return
def G_toast(g,lines):
 COVER[0]+=1
 rbox(10,50,300,30+18*len(lines),8,WHITE)
 y=72
 for ln in lines:
  ctext(y,ln)
  y+=18
 while wkey()not in(OK,CLR):
  pass
 g.shown=None
def G_objective(g):
 if not g.power:
  t='Find the red light by the door.'
 elif not g.note:
  t='The door locked behind you. Look around the foyer.'
 elif not g.closet:
  t="Decode Ivy's note. The coat closet keypad wants four letters."
 elif not g.living:
  t='Unlock the Living Room.'
 elif not g.tapheard:
  t='The TV in the Living Room switched itself on.'
 elif not g.notebook:
  t="Decode the knocks. Ivy's notebook might explain them."
 else:
  t='Decode the knocks. The hallway keypad wants five letters.'
 if g.awake:
  t+='\nShe is awake. Stay quiet. Hide when the lights stutter.'
 return t
def G_journal(g):
 body=G_objective(g)
 if g.note:
  body+="\n\nIvy's note: "+G_CIPHER+'\nMy name is the key.'
 if g.tapheard:
  body+='\n\nKnocks: 4-1 4-5 2-4 1-5 4-4'
 G_page('JOURNAL',body)
 if g.notebook:
  G_grid_page()
 g.shown=None
def G_grid_page():
 cls()
 ctext(20,"IVY'S NOTEBOOK",GOLD)
 text(10,44,'For talking through walls.',GREY)
 text(10,61,'Knocks: row, then column.',GREY)
 for r in range(5):
  text(110,92+r*20,str(r+1),GOLD)
  for c in range(5):
   if r==0:
    text(140+c*24,76,str(c+1),GOLD)
   text(140+c*24,92+r*20,G_TAPGRID[r][c])
 text(10,204,'I and J share a box.  ENTER',GREY)
 while wkey()not in(OK,CLR):
  pass
def G_pause_menu(g):
 c=choose('PAUSED',['Resume','Journal','Quit demo'])
 g.shown=None
 if c==1:
  G_journal(g)
 return c==2
