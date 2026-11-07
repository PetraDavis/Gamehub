# GHCRYPTB: part of GHCRYPTP. Keep it next to GHCRYPTP.
from GHCRYPTC import*
LEFT=24
def circ(x,y,r,c):
 col(c)
 fill_circle(x,y,r)
G_CWID=G_VW//G_COLS
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
def G_column(g,t,u,top,h,k):
 cl=(0,0,0)if g.blackout else G_CEIL
 fl=(0,0,0)if g.blackout else G_shade(G_FLOOR,0.5 if not g.power else 1)
 y0=max(0,top)
 y1=min(G_VH,top+h)
 sp=[(0,y0,cl),(y0,y1,G_shade(G_colour(t),k)),(y1,G_VH,fl)]
 if y0==0:
  sp=sp[1:]
 if y1==G_VH:
  sp=sp[:-1]
 sp=[s for s in sp if s[1]>s[0]]
 def band(v0,v1,c):
  a=int(top+h*(1-v1))&~1
  b=int(top+h*(1-v0))&~1
  if b-a>=2:
   return G_put(sp,max(0,a),min(G_VH,b),G_shade(c,k))
  return sp
 if t in 'lkjCF':
  if u<0.12 or u>0.88:
   sp=band(0,0.8,(70,48,30))
  sp=band(0.8,1,G_WALL)
  if 0.7<u<0.85:
   sp=band(0.42,0.47,(210,180,90))
  if t in 'kC'and 0.12<u<0.3:
   on=t=='C'and g.closet
   sp=band(0.5,0.6,(40,40,40))
   sp=band(0.53,0.57,(40,200,70)if on else(200,40,40)if g.power else(30,30,30))
  if t=='F'and g.locked and(0.15<u<0.25):
   sp=band(0.6,0.64,(255,30,40))
 elif t=='S':
  for n in range(6):
   sp=band(n*0.14,n*0.14+0.07,(95,70,45))
  if 0.2<u<0.8:
   sp=band(0.25,0.32,(150,120,80))
   sp=band(0.55,0.62,(150,120,80))
 elif t=='B':
  for n in range(4):
   cc=((150,50,50),(50,90,150),(60,130,70),(170,140,60))[(int(u*4)+n)%4]
   sp=band(n*0.25+0.05,n*0.25+0.2,cc)
 elif t=='T':
  if 0.1<u<0.9:
   sp=band(0.35,0.7,(15,15,20)if not g.tv else(60,90,160))
 elif t=='G':
  if 0.28<u<0.72:
   sp=band(0,0.85,(70,45,30))
   sp=band(0.6,0.75,(220,210,180))
   if 0.45<u<0.55:
    sp=band(0.2,0.55,(180,150,70))
    if not g.note:
     sp=band(0.25,0.3,(240,240,230))
 elif t=='P':
  if 0.3<u<0.6:
   sp=band(0.38,0.56,(130,130,135))
   if 0.4<u<0.5:
    sp=band(0.44 if g.power else 0.48,0.54 if g.power else 0.58,(40,40,40))
 return sp
def G_render(g,full=False):
 if full or not hasattr(g,'cols')or g.cover!=COVER[0]:
  g.cover=COVER[0]
  g.cols=[None]*G_COLS
  g.ysk=None
 shown=g.cols
 new=[]
 zb=[0]*G_COLS
 ca=math.cos(g.a)
 sa=math.sin(g.a)
 for i in range(G_COLS):
  cam=(i+0.5)/G_COLS*2-1
  rx=ca-sa*cam*G_FOV*0.5*1.15
  ry=sa+ca*cam*G_FOV*0.5*1.15
  mx=int(g.x)
  my=int(g.y)
  ddx=abs(1/rx)if rx else 1000000000.0
  ddy=abs(1/ry)if ry else 1000000000.0
  if rx<0:
   sx=-1
   sdx=(g.x-mx)*ddx
  else:
   sx=1
   sdx=(mx+1-g.x)*ddx
  if ry<0:
   sy=-1
   sdy=(g.y-my)*ddy
  else:
   sy=1
   sdy=(my+1-g.y)*ddy
  side=0
  t='#'
  for n in range(40):
   if sdx<sdy:
    sdx+=ddx
    mx+=sx
    side=0
   else:
    sdy+=ddy
    my+=sy
    side=1
   t=G_tile(mx,my)
   if t!='.'and(not(t=='l'and g.living)):
    break
  d=sdx-ddx if side==0 else sdy-ddy
  d=max(d,0.05)
  zb[i]=d
  if side==0:
   u=g.y+d*ry
  else:
   u=g.x+d*rx
  u-=int(u)
  h=int(G_VH*1.35/d)&~7
  top=(G_VH-h)//2
  k=G_lq(G_light(g,i,d)*(0.8 if side else 1.0))
  new.append(G_column(g,t,u,top,h,k))
 G_sprites(g,zb,ca,sa,new)
 ys=G_ys_place(g,zb,ca,sa)
 if g.ysk is not None and(ys is None or ys[0]!=g.ysk):
  for i in range(g.ysa,g.ysb):
   shown[i]=None
 runs={}
 hit=False
 for i in range(G_COLS):
  for y0,y1,c in G_diff(shown[i],new[i]):
   key=(y0,y1,c)
   r=runs.get(key)
   if r and r[-1][1]==i:
    r[-1][1]=i+1
   elif r:
    r.append([i,i+1])
   else:
    runs[key]=[[i,i+1]]
   if ys and ys[1]<=i<ys[2]:
    hit=True
  shown[i]=new[i]
 for key in sorted(runs,key=lambda q:q[2]):
  y0,y1,c=key
  for a,b in runs[key]:
   rect(a*G_CWID,y0,(b-a)*G_CWID,y1-y0,c)
 if ys:
  if ys[0]!=g.ysk or hit:
   G_ys_draw(g,ys)
  else:
   G_ys_shimmer(g)
  g.ysk,g.ysa,g.ysb=(ys[0],ys[1],ys[2])
 else:
  g.ysk=None
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
def G_ys_draw(g,ys):
 left,wid,top,h,a,b=ys[0]
 lo=a*G_CWID
 hi=b*G_CWID
 rows={}
 eyes=[]
 for i in range(0,len(G_YSD),5):
  u0,u1,v0,v1,kind=(G_YSD[i]/255,G_YSD[i+1]/255,G_YSD[i+2]/255,G_YSD[i+3]/255,G_YSD[i+4])
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
