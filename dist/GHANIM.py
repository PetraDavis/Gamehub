# GHANIM from GAMEHUB, on its own. Run it.
from GHANIMB import*
def circ(x,y,r,c):
 col(c)
 fill_circle(x,y,r)
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
def home(mod,title,rules,buttons,opts=('Play','Back'),sel=0,wipe=None):
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
    if opts[sel]=='Delete':
     wipe()
     break
    return sel
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
def G_dec(s,i):
 k=i
 while k>0 and s.F[k][0]!=1:
  k-=1
 fr=bytearray(G_N)
 for j in range(k,i+1):
  G_apply(fr,s.F[j])
 return fr
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
def G_main():
 while True:
  c=home('GHANIM','ANIMATION STUDIO',G_RULES,G_KEYS,('Play','Delete','Back'),0,G_forget)
  if c<0:
   return
  G_studio()
G_main()
RAN=True
