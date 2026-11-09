# GHMENU: the GAMEHUB menu. Run GAMEHUB, not this.
from GHMENUB import*
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
def I_digit7(x,y,ch,c):
 I_c_(c)
 bits=I_FONT7[ch]
 for r in range(7):
  row=bits[r*5:r*5+5]
  k=0
  while k<5:
   if row[k]=='1':
    e=k
    while e+1<5 and row[e+1]=='1':
     e+=1
    draw_line(x+k,y+r,x+e,y+r)
    k=e+1
   else:
    k+=1
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
def I_superttt(x,y,c):
 for i in(-1,1):
  I_box(x+i*7-1,y-20,3,41,I_INK)
  I_box(x-20,y+i*7-1,41,3,I_INK)
 for i in(-1,1):
  I_box(x+i*2,y-5,1,11,(150,150,160))
  I_box(x-5,y+i*2,11,1,(150,150,160))
 I_line(x-17,y-17,x-11,y-11,I_RED,2)
 I_line(x-11,y-17,x-17,y-11,I_RED,2)
 I_c_((40,90,210))
 fill_circle(x+13,y+13,4)
 I_c_(I_WHITE)
 fill_circle(x+13,y+13,2)
def I_breakout(x,y,c):
 cols=((220,60,60),(235,140,50),(230,210,60),(70,190,90))
 for r in range(3):
  for i in range(4):
   bx=x-19+i*10
   I_box(bx,y-15+r*6,9,5,cols[(i+r)%4])
   I_hline(bx,bx+8,y-15+r*6,tuple((min(255,v+60)for v in cols[(i+r)%4])))
 for i,(dx,dy)in enumerate(((-8,12),(-5,8))):
  I_box(x+dx,y+dy,2,2,(120,150,230))
 I_circ(x-1,y+5,2,I_WHITE)
 I_rr(x-11,y+13,22,4,1,I_WHITE)
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
def I_space(x,y,c):
 for sx,sy in((-15,-12),(12,-16),(16,8),(-17,10),(2,17)):
  I_box(x+sx,y+sy,2,2,(255,240,180))
 I_poly([x-4,x+4,x+8,x-8],[y-14,y-14,y+6,y+6],(220,225,235))
 I_box(x-3,y-7,6,5,(90,170,230))
 I_poly([x-8,x-13,x-8],[y-2,y+8,y+6],(215,40,40))
 I_poly([x+8,x+13,x+8],[y-2,y+8,y+6],(215,40,40))
 I_poly([x-5,x+5,x],[y+7,y+7,y+15],(250,170,40))
def I_star(x,y,c):
 I_box(x-7,y-15,14,9,(120,230,90))
 I_box(x-7,y-15,3,3,(8,10,32))
 I_box(x+4,y-15,3,3,(8,10,32))
 I_box(x-4,y-11,8,2,(8,10,32))
 I_box(x-1,y-3,2,6,(255,230,90))
 I_box(x-10,y+7,20,10,(90,200,255))
 I_box(x-10,y+7,7,4,(8,10,32))
 I_box(x+3,y+7,7,4,(8,10,32))
I_ICONS={'GHSOLI':I_solitaire,'GHBLOCKS':I_blocks,'GHSUDOKU':I_sudoku,'GHANIM':I_anim,'GHFLAP':I_flap,'GHTTT':I_ttt,'GHMERGE':I_g2048,'GHPONG':I_pong,'GHBREAK':I_breakout,'GHRPG':I_rpg,'GHSIMON':I_simon,'GHHANG':I_hangman,'GHSPACE':I_space,'GHFORTUN':I_fortune,'GHNAMES':I_names,'GHSTAR':I_star,'GHMATCH':I_match,'GHDRAGON':I_dragon,'GHDETECT':I_detect,'GHSUPER':I_superttt,'*keys':I_keys,'*wipe':I_wipe,'*about':I_about}
def I_draw(mod,x,y,c):
 f=I_ICONS.get(mod)
 if f:
  f(x,y,c)
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
H_CATS=[('Arcade',[('Wing It','GHFLAP'),('Pong','GHPONG'),('Breakout','GHBREAK'),('Star Patrol','GHSTAR')]),('Puzzle',[('Stack Drop','GHBLOCKS'),('2048','GHMERGE'),('Sudoku','GHSUDOKU'),('Simon','GHSIMON'),('Super Tic-Tac-Toe','GHSUPER')]),('Classics',[('Solitaire','GHSOLI'),('Tic-Tac-Toe','GHTTT'),('Hangman','GHHANG'),('Memory Match','GHMATCH')]),('Adventure',[('Tiny Quest','GHRPG'),('Detective Case','GHDETECT'),('Lost Orbit','GHSPACE')]),('Create',[('Animation Studio','GHANIM'),('Fortune Cards','GHFORTUN'),('Name Generator','GHNAMES')]),('Settings',[('Key Test','*keys'),('Delete Saves','*wipe'),('About','*about')])]
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
 for k in[mod]+[mod[:7]+c for c in 'BCDEFHP']:
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
 ctext(40,'DELETE SAVES',GOLD)
 ctext(80,'This erases')
 ctext(100,'all your animations')
 ctext(160,'ENTER: delete',RED)
 ctext(185,'CLEAR: keep them')
 if wkey()!=OK:
  return
 n=0
 try:
  n=S_wipe(3)
 except Exception:
  pass
 cls()
 message([str(n)+' save lists cleared.'],'Done')
def H_pick(st):
 if st[3]:
  cls()
  message([st[3],'Is '+st[4]+' on the','calculator?'],'Could not run')
  st[3]=''
 while True:
  if not st[2]:
   ci=H_cat_screen(st[0])
   if ci<0:
    cls()
    return None
   st[0],st[1],st[2]=(ci,0,1)
  ai=H_app_screen(st[0],st[1])
  if ai<0:
   st[2]=0
   continue
  st[1]=ai
  mod=H_CATS[st[0]][1][ai][1]
  if mod[0]=='*':
   H_run_app(mod)
   continue
  return mod
H_pick
