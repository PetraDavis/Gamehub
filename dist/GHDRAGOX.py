# GHDRAGOX: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
def G_unpack(n):
 nm=''
 while n:
  nm=G_ABC[n%27-1]+nm
  n//=27
 return nm[0]+nm[1:].lower()
G_MAPS=(['TTTTTTTTTTTTT~~~','T.....""".....~~','T.H...""""...~~~','T.....""".T...~~','...........E.~~~','T....TT.......~~','T.""".TT......~~','T.""".........~~','TTTTTTTTTTTTTT~~'],['~^^^^^^^^^^^^^^^','~...""""..LLL..^','~..^"""..LLELL.^','~.....^...LLL...','~...............','~...^^...."""...','~..LL....."""..^','~.....^^.......^','~^^^^^^^^^^^^^^^'],['^^^^^^^^^^^^^^^^','...""".....^E^^^','...........^^^^^','......~~~~......','....~~~~B~~~....','.....~~~~~......','.."""...........','..""".....^C....','^^^^^^^^^^^^^^^^'],['TTTTTTTTTTTTTTTT','T.....A......N.T','T..Q.......S...T','T..=.......=...T','T..=============','T.......W......T','T.....V......V.T','T.V............T','TTTTTTTTTTTTTTTT'])
def G_load(g):
 g.maps=[[list(r)for r in mp]for mp in G_MAPS]
 G_EGGS.clear()
 for m in range(3):
  for y in range(9):
   for x in range(16):
    if G_MAPS[m][y][x]=='E':
     G_EGGS[m,x,y]=random.randint(0,6)if m==0 else G_egg_type(m)
 g.m,g.x,g.y=(0,3,2)
 g.hp=g.mhp=30
 g.pen=[]
 g.bag=[]
 g.warm=12
 g.spawn=100
 g.pick=g.ride=g.quest=g.pol=g.shen=None
 g.deck={}
 g.coins=g.own=g.book=g.seen=g.face=g.dread=g.glim=g.luck=g.curse=g.buys=g.done=g.cd=g.sad=g.ar=0
 g.shn=random.randint(120,180)
 try:
  from ti_system import recall_list
  s=[int(v)for v in recall_list('DRG')]
 except Exception:
  return
 if len(s)<9 or s[0]not in(2,3,4):
  return
 v=s[0]
 k=min(1,v-2)
 pk=0
 g.coins,g.own,g.book=(s[1],s[2],s[3])
 if k:
  g.dread=s[4]
 g.bag=[e for e in s[4+k:9+k]if e>=0]
 w=5 if v>3 else 4
 for i in range(9+k,len(s)-w+1,w):
  if v>3:
   nm=G_unpack(s[i])
   i+=1
   t=s[i]
  else:
   nm,t=(G_NAMES[s[i]//32],s[i]%32)
  lv=s[i+1]
  mh=20+6*min(4,G_DT[t][2])+6*(lv-1)+6*(t==20)+16*(t==21)+3*(t==24)
  x=s[i+3]%4000
  p=x//200
  g.pen.append([nm,t,lv,mh,mh,s[i+2],G_PAINT[p-1]if p else G_DT[t][3],x//20%10,x%20,s[i+3]//4000])
 try:
  b=[int(v)for v in recall_list('DRB')]
  if b[0]>2:
   g.ar=b.pop(2)
  if b[0]>1:
   pk=b[1]//500000%12
   g.cd=b[1]//6000000%16
   g.sad=b[1]//96000000%2
   g.shn=max(g.shn,b[1]//192000000*100)
   b[1]%=500000
   g.glim,g.luck,g.curse,g.buys,g.done=(b[1]%100,b[1]//100%2,b[1]//200%2,b[1]//400%11,b[1]//4400)
   b=b[1:]
  for i in range(1,len(b)-1,2):
   t=b[i+1]%32
   g.pen.append([G_unpack(b[i]),t,1,10,10,0,G_DT[t][3],0,0,8+b[i+1]//32])
 except Exception:
  pass
 big=[d for d in g.pen if not d[9]&8]
 g.pick=big[pk]if pk<len(big)else G_grown(g)
 g.warm=12
def G_win(g):
 cls()
 if g.pick:
  G_drag(73,30,3,g.pick[1],g.pick[6],g.pick[7],g.pick[8],None,0,g.pick[9]&7)
 message(['The Shadow Wyrm flies far','away. Dragons return to','every land. You did it!'],'THE END')
 G_rest(g)
 G_save(g)
