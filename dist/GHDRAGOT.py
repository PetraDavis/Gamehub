# GHDRAGOT: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
def G_who(g,title,babies=True):
 L=[d for d in g.pen if babies or not d[9]&8]
 pg=0
 while L:
  sh=L[pg:pg+9]
  more=len(L)>9
  c=G_zl(title,[d[0]+' '+G_DT[d[1]][0]for d in sh]+(['More...']if more else[])+['Back'])
  if more and c==len(sh):
   pg=pg+9 if pg+9<len(L)else 0
   continue
  return sh[c]if 0<=c<len(sh)else None
 message(['You need a dragon first.'],'Hm')
 return None
def G_glim(g):
 d=G_who(g,'Make shiny ('+str(g.glim)+' stones)')
 if d is None:
  return
 q=0
 if g.glim>=5:
  c=choose('Glimmer Stones: '+str(g.glim),['Random (1 stone)','Pick colour (5)','Back'])
  if c==1:
   q=choose('Which shiny?',[G_SCH[i][0]for i in range(1,5)])+1
   if q<1:
    return
   g.glim-=5
  elif c!=0:
   return
 if not q:
  g.glim-=1
  q=random.randint(1,4)
 if g.pol and g.pol[0]is d:
  g.pol=None
 d[9]=d[9]&8|q
 d[6]=G_DT[d[1]][3]
 cls(G_NIGHT)
 G_drag(102,10,2,d[1],d[6],d[7],d[8],None,0,q)if not d[9]&8 else G_drag(131,45,1,d[1],d[6],0,0,None,0,q)
 message([d[0]+' sparkles!','Now a '+G_SCH[q][0]+' '+G_DT[d[1]][0]+'!'],'Shiny!')
 G_save(g)
def G_zl(title,opts):
 cls()
 ctext(24,title,GOLD)
 n=len(opts)
 h=15 if n>9 else 17
 sel=old=0
 top=-1
 while True:
  t=sel//10*10
  if t!=top:
   top=t
   rect(0,32,320,178,BLACK)
   for i in range(top,min(n,top+10)):
    text(30,50+(i-top)*h,opts[i],GOLD if i==sel else WHITE)
   if n>10:
    text(6,206,'More: keep going ('+str(top//10+1)+'/'+str((n+9)//10)+')',GREY)
  elif sel!=old:
   for i in(old,sel):
    y=50+(i-top)*h
    if i==old:
     rect(14,y-10,8,6,BLACK)
    text(30,y,opts[i],GOLD if i==sel else WHITE)
  rect(14,50+(sel-top)*h-10,8,6,GOLD)
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
def G_pol_off(g):
 d=g.pol[0]
 d[9]=d[9]&8|g.pol[1]
 g.pol=None
 if d in g.pen:
  message([d[0]+"'s shine",'wore off...'],'Hm')
  G_draw_map(g,True)
