# GHCRYPTB: part of GHCRYPT. Keep it next to GHCRYPT.
from GHCRYPTC import*
from GHCRYPTC import _corners
WHITE=(255,255,255)
def rect(x,y,w,h,c):
 if w<1 or h<1:
  return
 col(c)
 fill_rect(x-1,y-1,w+1,h+1)
def cls(c=BLACK):
 COVER[0]+=1
 col(c)
 fill_rect(-1,-1,321,211)
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
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
G_MAP=['#BBBB###SSS###','B....#.......#','B............k','#####G.......#','#....#.......#','T....l.......j','#....#.......C','########PF####']
G_KNOCKS=((4,1),(4,5),(2,4),(1,5),(4,4))
G_SPR={'couch':(1.3,((0,1,0,0.2,(150,40,45)),(0.08,0.92,0.2,0.36,(120,30,35)),(0,0.12,0.2,0.28,(150,40,45)),(0.88,1,0.2,0.28,(150,40,45)))),'table':(0.9,((0,0.12,0,0.28,(95,65,40)),(0.88,1,0,0.28,(95,65,40)),(0,1,0.28,0.33,(120,85,50)),(0.3,0.7,0.33,0.37,(140,70,180)))),'phone':(0.6,((0,0.15,0,0.3,(95,65,40)),(0.85,1,0,0.3,(95,65,40)),(0,1,0.3,0.34,(120,85,50)),(0.25,0.75,0.34,0.42,(20,20,20)))),'lamp':(0.6,((0.45,0.55,0,0.55,(180,150,70)),(0.15,0.85,0.55,0.72,(235,220,170)))),'desk':(1.2,((0,0.1,0,0.3,(95,65,40)),(0.9,1,0,0.3,(95,65,40)),(0,1,0.3,0.35,(120,85,50)),(0.2,0.5,0.35,0.38,(200,190,150)))),'rack':(0.7,((0.46,0.54,0,0.8,(80,55,35)),(0.15,0.45,0.35,0.75,(60,70,110)),(0.55,0.85,0.4,0.72,(110,50,50)))),'vase':(0.7,((0.1,0.9,0,0.25,(95,65,40)),(0.35,0.65,0.25,0.45,(60,120,140)),(0.3,0.7,0.45,0.55,(90,140,70))))}
G_SPRITES=[(3.3,5.5,'couch'),(1.9,4.6,'table'),(4.4,6.4,'phone'),(1.0,6.5,'lamp'),(2.6,1.5,'desk'),(12.4,4.9,'rack'),(6.5,1.4,'vase')]
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
def G_shade(c,k):
 return(min(255,int(c[0]*k)),min(255,int(c[1]*k)),min(255,int(c[2]*k)))
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
def G_sprites(g,zb,ca,sa,new):
 lst=[]
 for sx,sy,kind in G_SPRITES:
  dx=sx-g.x
  dy=sy-g.y
  fwd=dx*ca+dy*sa
  if fwd<0.2:
   continue
  lst.append((fwd,-dx*sa+dy*ca,kind))
 lst.sort(reverse=True)
 for fwd,side,kind in lst:
  cx=side/fwd/(G_FOV*0.5*1.15)
  scol=(cx+1)/2*G_COLS
  half=G_SPR[kind][0]/2/fwd/(G_FOV*0.5*1.15)*G_COLS/2
  h=G_VH*1.35/fwd
  top=(G_VH-h)/2
  k=G_lq(G_light(g,int(scol),fwd))
  for i in range(max(0,int(scol-half)),min(G_COLS,int(scol+half)+1)):
   if zb[i]<fwd:
    continue
   u=(i+0.5-(scol-half))/(2*half)if half>0 else 0.5
   if u<0 or u>1:
    continue
   for u0,u1,v0,v1,c in G_SPR[kind][1]:
    if u0<=u<=u1:
     y0=int(top+h*(1-v1))&~1
     y1=int(top+h*(1-v0))&~1
     if y1-y0>=2 and y0<G_VH:
      new[i]=G_put(new[i],max(0,y0),min(G_VH,y1),G_shade(c,k))
def G_bottom(g,prompt):
 if prompt==g.shown:
  return
 g.shown=prompt
 rect(0,G_VH,320,210-G_VH,BLACK)
 text(4,G_VH+15,G_room(g),GREY)
 if g.flash:
  text(250,G_VH+15,'LIGHT',GOLD)
 text(4,G_VH+33,prompt[:31],WHITE)
def G__poly_slabs(pts,kind,step,top=True,bottom=True):
 ys=[p[1]for p in pts]
 y=min(ys)
 n=len(pts)
 first=len(G_YS)
 while y<max(ys):
  yc=y+step/2
  xs=[]
  for i in range(n):
   x1,y1=pts[i]
   x2,y2=pts[(i+1)%n]
   if y1<=yc<y2 or y2<=yc<y1:
    xs.append(x1+(yc-y1)*(x2-x1)/(y2-y1))
  if len(xs)>=2:
   G_YS.append((min(xs)/256,max(xs)/256,1-(y+step)/640,1-y/640,kind))
  y+=step
 for i,on in((first,top),(len(G_YS)-1,bottom)):
  if on and i<len(G_YS):
   u0,u1,v0,v1,k=G_YS[i]
   G_YS[i]=(u0,u1,v0,v1,5)
def G__limb(pts,w,kind=0):
 for i in range(0,len(pts)-2,2):
  x1,y1,x2,y2=(pts[i],pts[i+1],pts[i+2],pts[i+3])
  n=max(1,int(abs(y2-y1)/8))
  for k in range(n):
   t0=k/n
   t1=(k+1)/n
   xm=x1+(x2-x1)*(t0+t1)/2
   ya=y1+(y2-y1)*t0
   yb=y1+(y2-y1)*t1
   hw=w*0.4+abs(x2-x1)/n/3
   G_YS.append(((xm-hw)/256,(xm+hw)/256,1-max(ya,yb)/640-0.004,1-min(ya,yb)/640+0.004,kind))
def G__oval(cx,cy,rx,ry,kind,step,a=0.0):
 ca=math.cos(0.55)
 sa=math.sin(0.55)
 pts=[]
 for i in range(16):
  t=2*math.pi*i/16
  lx=cx+rx*math.cos(t)*math.cos(a)-ry*math.sin(t)*math.sin(a)
  ly=cy+rx*math.cos(t)*math.sin(a)+ry*math.sin(t)*math.cos(a)
  pts.append((140+lx*ca-ly*sa,50+lx*sa+ly*ca))
 G__poly_slabs(pts,kind,step)
def G__build_ys():
 ca=math.cos(0.55)
 sa=math.sin(0.55)
 G__limb([128,120,132,88,140,66],11)
 G__poly_slabs([(98,122),(128,112),(160,126),(150,210),(146,260),(110,260),(106,210)],0,8,True,False)
 hem=[(108,250),(148,250),(162,330)]
 x=162
 while x>94:
  hem.append((x-4.5,330+(18 if int(x)%2 else 6)))
  x-=9
 hem.append((94,330))
 G__poly_slabs(hem,0,6,False,True)
 G__limb([118,320,112,460,120,470,108,612,98,628],9)
 G__limb([140,320,146,462,136,474,150,610,162,630],9)
 G__limb([100,128,84,250,92,262,76,420],7)
 G__limb([158,128,176,248,166,262,184,410],7)
 for x0,y0,sg in((76,420,-1),(184,410,1)):
  for f in range(5):
   G__limb([x0,y0,x0+sg*(f*4-6),y0+52+f%2*8,x0+sg*(f*5-4),y0+70+f*3],2.6)
 hair=[(-18,-6),(-27,30),(-24,96),(-6,70),(8,100),(20,60),(17,-6),(10,-24),(-10,-24)]
 G__poly_slabs([(140+lx*ca-ly*sa,50+lx*sa+ly*ca)for lx,ly in hair],0,4)
 G__oval(0,0,17,25,0,4)
 for ex,ey in((137.2,41.2),(149.1,48.55)):
  G_YS.append(((ex-2)/256,(ex+2)/256,1-(ey+2)/640,1-(ey-2)/640,4))
G_RIM=((215,215,225),(170,175,190),(250,250,255))
def G_ys_draw(g,ys):
 if not G_YS:
  G__build_ys()
 left,wid,top,h,a,b=ys[0]
 lo=a*G_CWID
 hi=b*G_CWID
 rows={}
 eyes=[]
 for u0,u1,v0,v1,kind in G_YS:
  xa=max(lo,int(left+u0*wid))//G_YG
  xb=min(hi,int(left+u1*wid)+1+G_YG-1)//G_YG
  ya=int(top+h*(1-v1))
  yb=int(top+h*(1-v0))+1
  if kind==4:
   eyes.append(((xa+xb)*G_YG//2,(ya+yb)//2))
   continue
  if xb<=xa:
   continue
  for r in range(max(0,ya)//G_YG,(min(G_VH,yb)+G_YG-1)//G_YG):
   if r in rows:
    rows[r].append((xa,xb))
   else:
    rows[r]=[(xa,xb)]
 out=[]
 open_={}
 for r in range(G_VH//G_YG+1):
  cur={}
  segs=sorted(rows.get(r,()))
  m=[]
  for xa,xb in segs:
   if m and xa<=m[-1][1]:
    if xb>m[-1][1]:
     m[-1][1]=xb
   else:
    m.append([xa,xb])
  for xa,xb in m:
   if xb-xa>=3:
    cur[xa,xa+1,0]=1
    cur[xa+1,xb-1,1]=1
    cur[xb-1,xb,0]=1
   else:
    cur[xa,xb,0]=1
  for key in list(open_):
   if key not in cur:
    out.append((key,open_.pop(key),r))
  for key in cur:
   if key not in open_:
    open_[key]=r
 g.rim=[]
 for c in(0,1):
  for(xa,xb,kind),r0,r1 in out:
   if kind==c:
    x,y,w,hh=(xa*G_YG,r0*G_YG,(xb-xa)*G_YG,min(G_VH,r1*G_YG)-r0*G_YG)
    if hh>0:
     rect(x,y,w,hh,G_INSIDE if c else G_RIM[0])
     if not c:
      g.rim.append((x,y,w,hh))
 r=max(2,wid//12)
 eyes=[(x,y)for x,y in eyes if lo+r<=x<hi-r and r<=y<G_VH-r]
 for rr,c in((r,(35,80,150)),(r*2//3,(80,175,245)),(max(1,r//3),(230,250,255))):
  for x,y in eyes:
   circ(x,y,rr,c)
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
def G_say(g,s):
 G_toast(g,G_wrap(s,27))
def G_objective(g):
 if not g.power:
  t='It is pitch dark. Find the power switch by the front door.'
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
def G_ending():
 cls()
 ctext(40,'enCRYPTed',(200,60,60))
 ctext(70,'The keypad flashes green.')
 ctext(90,'End of the demo.')
 ctext(125,'Full game at',GOLD)
 ctext(147,G_LINK1,WHITE)
 ctext(167,G_LINK2,WHITE)
 ctext(203,'CLEAR: leave',GREY)
 while wkey()!=CLR:
  pass
def G_pause_menu(g):
 c=choose('PAUSED',['Resume','Journal','Quit demo'])
 g.shown=None
 if c==1:
  G_journal(g)
 return c==2
