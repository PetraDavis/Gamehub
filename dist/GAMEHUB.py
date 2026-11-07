# GAMEHUB - game center for the TI-84 Evo. Run this file.
from GAMEHUBB import*
def rect(x,y,w,h,c):
 if w<1 or h<1:
  return
 col(c)
 fill_rect(x-1,y-1,w+1,h+1)
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
def halo(x,y,r,c,t=2):
 col(c)
 for i in range(t):
  draw_circle(x,y,r-i)
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
def I_blocks(x,y,c):
 s=8
 cells=((-2,1,(220,70,70)),(-1,1,(220,70,70)),(0,1,(70,110,220)),(1,1,(70,110,220)),(-2,0,(80,190,90)),(0,0,(70,110,220)),(1,0,(230,200,60)),(-2,-1,(80,190,90)),(1,-1,(230,200,60)),(-1,-3,(170,90,210)),(0,-3,(170,90,210)),(0,-2,(170,90,210)))
 for cx,cy,col in cells:
  I_bevel(x+cx*s,y+cy*s+2,s,col)
def I_sudoku(x,y,c):
 s=11
 x0=x-16
 y0=y-16
 I_box(x0+s+1,y0+1,s-1,s-1,(250,225,140))
 nums=('53 ',' 7 ','1 9')
 for r in range(3):
  for k in range(3):
   ch=nums[r][k]
   if ch!=' ':
    I_digit7(x0+k*s+3,y0+r*s+2,ch,I_INK if(r,k)!=(1,1)else(40,90,200))
 for i in(1,2):
  I_line(x0+i*s,y0,x0+i*s,y0+3*s,I_INK)
  I_hline(x0,x0+3*s,y0+i*s,I_INK)
 I_c_(I_INK)
 for o in(0,1):
  draw_rect(x0-o-1,y0-o-1,3*s+2*o+1,3*s+2*o+1)
def I_flap(x,y,c):
 I_box(x-14,y-16,10,4,I_WHITE)
 I_circ(x-12,y-15,3,I_WHITE)
 I_circ(x-7,y-17,4,I_WHITE)
 I_ground(x,y,15,(70,170,80))
 I_box(x+14,y+4,4,12,(120,80,40))
 I_circ(x+16,y+1,6,(50,140,60))
 I_circ(x-2,y-1,11,(170,120,20))
 I_circ(x-2,y-1,10,(250,215,50))
 I_poly([x-14,x-2,x-6],[y-1,y+1,y+8],(255,245,190))
 I_circ(x+3,y-5,4,I_WHITE)
 I_circ(x+4,y-5,2,I_BLACK)
 I_poly([x+7,x+17,x+7],[y-2,y+1,y+2],(245,140,30))
 I_poly([x+7,x+15,x+7],[y+2,y+3,y+5],(200,100,20))
def I_rpg(x,y,c):
 I_circ(x-5,y-8,6,(240,200,160))
 I_box(x-11,y-15,13,5,(110,70,30))
 I_box(x-11,y-11,3,5,(110,70,30))
 I_box(x-8,y-9,2,2,I_BLACK)
 I_box(x-3,y-9,2,2,I_BLACK)
 I_box(x-11,y-1,13,12,(60,120,230))
 I_box(x-11,y+5,13,2,(110,70,30))
 I_box(x-14,y,3,8,(240,200,160))
 I_box(x-10,y+11,4,6,(60,40,30))
 I_box(x-4,y+11,4,6,(60,40,30))
 I_box(x+2,y+1,4,3,(240,200,160))
 I_box(x+2,y-23,12,26,(15,45,70))
 I_box(x+4,y-22,8,24,(40,110,170))
 I_box(x+5,y-21,6,22,(100,200,245))
 I_box(x+7,y-21,2,21,(240,252,255))
 I_box(x+3,y+1,10,2,I_GOLD)
 I_box(x+7,y+3,2,5,(120,80,40))
 for sx,sy in((x+16,y-18),(x+1,y-14),(x+15,y-6)):
  I_box(sx,sy,2,2,(200,240,255))
def I_simon(x,y,c):
 r=18
 cols=((40,170,60),(200,40,40),(40,80,200),(220,180,30))
 for q in range(4):
  a0=-math.pi/2+q*math.pi/2
  xs=[x]
  ys=[y]
  for i in range(6):
   a=a0+math.pi/2*i/5
   xs.append(x+r*math.cos(a))
   ys.append(y+r*math.sin(a))
  I_poly(xs,ys,cols[q])
 I_circ(x,y,5,I_BLACK)
 I_box(x-1,y-r,2,2*r,I_BLACK)
 I_box(x-r,y-1,2*r,2,I_BLACK)
def I_hangman(x,y,c):
 I_box(x-19,y+15,24,3,I_INK)
 I_box(x-13,y-18,3,34,I_INK)
 I_box(x-13,y-18,24,3,I_INK)
 I_line(x-11,y-9,x-3,y-17,I_INK,2)
 I_box(x+8,y-16,2,6,(140,90,40))
 I_circ(x+9,y-6,4,I_INK)
 I_circ(x+9,y-6,2,I_WHITE)
 I_line(x+9,y-2,x+9,y+7,I_INK,2)
 I_line(x+9,y+1,x+4,y+5,I_INK)
 I_line(x+10,y+1,x+15,y+5,I_INK)
 I_line(x+9,y+7,x+5,y+13,I_INK)
 I_line(x+10,y+7,x+14,y+13,I_INK)
def I_crypt(x,y,c):
 rs=[7]
 def rnd(a,b):
  rs[0]=(rs[0]*1103515245+12345)%2147483648
  return a+rs[0]%(b-a+1)
 k=0.21
 ox=x+3
 oy=y-17
 ca=math.cos(0.55)
 sa=math.sin(0.55)
 def m(cx,cy):
  return(ox+(cx-140)*k,oy+(cy-50)*k)
 def head(lx,ly):
  return m(140+lx*ca-ly*sa,50+lx*sa+ly*ca)
 def band(pts,w):
  left=[]
  right=[]
  for i in range(len(pts)-1):
   (x1,y1),(x2,y2)=(pts[i],pts[i+1])
   d=math.sqrt((x2-x1)**2+(y2-y1)**2)or 1
   nx=-(y2-y1)/d*w/2
   ny=(x2-x1)/d*w/2
   left+=[(x1+nx,y1+ny),(x2+nx,y2+ny)]
   right+=[(x1-nx,y1-ny),(x2-nx,y2-ny)]
  return[m(px,py)for px,py in left+right[::-1]]
 shapes=[[head(17*math.cos(t*math.pi/8),25*math.sin(t*math.pi/8))for t in range(16)],[head(px,py)for px,py in((-18,-6),(-27,30),(-24,96),(-6,70),(8,100),(20,60),(17,-6),(10,-24),(-10,-24))],band(((128,125),(132,88),(140,66)),11),[m(px,py)for px,py in((98,122),(128,112),(160,126),(150,210),(148,250),(108,250),(106,210))],band(((100,128),(84,250),(90,260)),7),band(((158,128),(176,248),(170,258)),7)]
 def spans(pts):
  out=[]
  ys=[p[1]for p in pts]
  n=len(pts)
  for row in range(int(min(ys)),int(max(ys))+1):
   yc=row+0.5
   xs=[]
   for i in range(n):
    (x1,y1),(x2,y2)=(pts[i],pts[(i+1)%n])
    if y1<=yc<y2 or y2<=yc<y1:
     xs.append(x1+(yc-y1)*(x2-x1)/(y2-y1))
   if len(xs)>=2:
    out.append((row,int(min(xs)+0.5),int(max(xs)+0.5)))
  return out
 all_spans=[spans(sh)for sh in shapes]
 for sp in all_spans:
  for row,a,b in sp:
   g=rnd(190,255)
   I_hline(a,max(a,b-1),row,(g,g*19//20,g*9//10))
 for sp in all_spans:
  for row,a,b in sp[1:-1]:
   if b-a>2:
    g=rnd(28,62)
    I_hline(a+1,b-2,row,(g,g,g+8))
 pts=[]
 for ex,ey in((137.2,41.2),(149.1,48.55)):
  a,b=m(ex,ey)
  pts.append((int(a),int(b)))
 for a,b in pts:
  I_hline(a-1,a+1,b-1,(35,80,150))
  I_hline(a-2,a+2,b,(35,80,150))
  I_hline(a-1,a+1,b+1,(35,80,150))
 for a,b in pts:
  I_hline(a-1,a+1,b,(80,175,245))
  I_line(a,b-1,a,b+1,(80,175,245))
 for a,b in pts:
  I_hline(a,a,b,(230,250,255))
def I_space(x,y,c):
 for sx,sy in((-15,-12),(12,-16),(16,8),(-17,10),(2,17)):
  I_box(x+sx,y+sy,2,2,(255,240,180))
 I_poly([x-4,x+4,x+8,x-8],[y-14,y-14,y+6,y+6],(220,225,235))
 I_box(x-3,y-7,6,5,(90,170,230))
 I_poly([x-8,x-13,x-8],[y-2,y+8,y+6],(215,40,40))
 I_poly([x+8,x+13,x+8],[y-2,y+8,y+6],(215,40,40))
 I_poly([x-5,x+5,x],[y+7,y+7,y+15],(250,170,40))
I_ICONS={'GHSOLI':I_solitaire,'GHBLOCKS':I_blocks,'GHSUDOKU':I_sudoku,'GHANIM':I_anim,'GHFLAP':I_flap,'GHTTT':I_ttt,'GHMERGE':I_g2048,'GHPONG':I_pong,'GHBREAK':I_breakout,'GHRPG':I_rpg,'GHSIMON':I_simon,'GHHANG':I_hangman,'GHCRYPT':I_crypt,'GHSPACE':I_space,'GHFORTUN':I_fortune,'GHNAMES':I_names,'*keys':I_keys,'*wipe':I_wipe,'*about':I_about}
def I_bg(mod):
 return I_BG.get(mod,I_BLACK)
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
def S_dname(s,i):
 n=str(i)
 return 'A'+str(s)+'0'*(3-len(n))+n
def S_wipe():
 n=0
 for s in range(1,S_SLOTS+1):
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
 return n
H_CATS=[('Arcade',[('Wing It','GHFLAP'),('Pong','GHPONG'),('Breakout','GHBREAK')]),('Puzzle',[('Stack Drop','GHBLOCKS'),('2048','GHMERGE'),('Sudoku','GHSUDOKU'),('Simon','GHSIMON')]),('Classics',[('Solitaire','GHSOLI'),('Tic-Tac-Toe','GHTTT'),('Hangman','GHHANG')]),('Adventure',[('Tiny Quest','GHRPG'),('Encrypted Demo','GHCRYPT'),('Lost Orbit','GHSPACE')]),('Create',[('Animation Studio','GHANIM'),('Fortune Cards','GHFORTUN'),('Name Generator','GHNAMES')]),('Settings',[('Key Test','*keys'),('Delete All Saves','*wipe'),('About','*about')])]
def H_draw_bar(i,on,first=False):
 y=H_BAR_Y+i*H_BAR_GAP
 c=GOLD if on else WHITE
 if first:
  rbox(50,y,220,H_BAR_H,9,c,2,BLACK,False)
 else:
  edge(50,y,220,H_BAR_H,9,c)
 ctext(y+17,H_CATS[i][0],c)
def H_cat_screen(sel):
 H_header()
 for i in range(len(H_CATS)):
  H_draw_bar(i,i==sel,True)
 while True:
  k=wkey()
  old=sel
  if k==UP:
   sel=(sel-1)%len(H_CATS)
  elif k==DOWN:
   sel=(sel+1)%len(H_CATS)
  elif k==OK or k==RIGHT:
   return sel
  elif k==CLR:
   return-1
  if sel!=old:
   H_draw_bar(old,False)
   H_draw_bar(sel,True)
def H_draw_app(app,i,on,first=False):
 x,y=H_app_pos(i)
 c=GOLD if on else WHITE
 if first:
  try:
   circ(x,y,26,I_bg(app[1]))
   I_draw(app[1],x,y,WHITE)
  except Exception:
   ctext(y+7,app[0][0],WHITE,x)
 halo(x,y,27,c,3)
def H_app_screen(ci,sel=0):
 cname,apps=H_CATS[ci]
 cls()
 rbox(90,8,140,24,9,WHITE,2,BLACK,False)
 ctext(26,cname,WHITE)
 for i in range(len(apps)):
  H_draw_app(apps[i],i,i==sel,True)
 H_show_title(apps[sel][0])
 n=len(apps)
 while True:
  k=wkey()
  old=sel
  if k==LEFT:
   sel=(sel-1)%n
  elif k==RIGHT:
   sel=(sel+1)%n
  elif k==UP and sel>=4:
   sel-=4
  elif k==DOWN and sel+4<n:
   sel+=4
  elif k==OK:
   return sel
  elif k==CLR:
   return-1
  if sel!=old:
   H_draw_app(apps[old],old,False)
   H_draw_app(apps[sel],sel,True)
   H_show_title(apps[sel][0],apps[old][0])
def H_run_app(mod):
 if mod=='*keys':
  return H_key_test()
 if mod=='*wipe':
  return H_wipe()
 if mod=='*about':
  cls()
  message(['Game center for the','TI-84 Evo.','CLEAR goes back.'],'GAMEHUB')
  return
 gc.collect()
 try:
  m=__import__(mod)
  if not getattr(m,'RAN',False):
   m.main()
 except Exception as e:
  cls()
  message([str(e)[:26],'Is '+mod+' on the','calculator?'],'Could not run')
 for k in[mod]+[mod[:7]+c for c in 'BCDEF']:
  try:
   del sys.modules[k]
  except Exception:
   pass
 m=None
 gc.collect()
def H_key_test():
 cls()
 ctext(30,'KEY TEST',GOLD)
 ctext(60,'Press any key to see')
 ctext(80,'its code. CLEAR twice')
 ctext(100,'in a row to leave.')
 last=0
 while True:
  k=wkey()
  rect(60,120,200,40,BLACK)
  ctext(150,'Code: '+str(k),WHITE)
  if k==CLR and last==CLR:
   return
  last=k
def H_wipe():
 cls()
 ctext(40,'DELETE ALL SAVES',GOLD)
 ctext(70,'This erases every')
 ctext(90,'Animation Studio')
 ctext(110,'animation.')
 ctext(150,'ENTER: delete',RED)
 ctext(175,'CLEAR: keep them')
 if wkey()!=OK:
  return
 n=0
 try:
  n=S_wipe()
 except Exception:
  pass
 cls()
 message([str(n)+' save lists cleared.'],'Done')
def H_main():
 ci=0
 while True:
  ci=H_cat_screen(ci)
  if ci<0:
   cls()
   return
  ai=0
  while True:
   ai=H_app_screen(ci,ai)
   if ai<0:
    break
   H_run_app(H_CATS[ci][1][ai][1])
H_main()
