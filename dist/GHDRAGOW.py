# GHDRAGOW: part of GHDRAGON, loaded only while it is needed.
from GHDRAGOP import*
G_SHINE={'Timmy':"WHOA! It's SILVER!/Is that normal?!/That's so cool!|It's GOLD! Like a/treasure! Can my/Pyrrak be gold too?|It GLOWS! Mom has/to see this! Wait,/do I still fight it?|PURPLE AND BLUE?!/Best. Day. EVER!/I'm telling everyone!"}
G_SPECIAL={19:{'Timmy':'Is that a LUMORA?!/Those are, like,/super legendary!','Lulu':"A Lumora?! Okay,/that is NOT tiny./That's amazing.",'Mira':"A Lumora... I've/only seen one in/a painting.",'Captain Vex':"A Lumora! Stars on/its wings, like a/sailor's night sky!",'Duchess Ivy':"A Lumora! Even I/don't own one./How dare you.",'Aurora':"A Lumora! I've/always wanted one./Lucky you."},20:{'Timmy':'WHAT is THAT?!/It looks like space!/Is it even real?!','Lulu':"What... IS that?/I'm scared. And/also jealous.",'Rocco':"That thing isn't/rock. I don't trust/it. At all.",'Mira':"I've never seen a/dragon like that./What IS it?",'Captain Vex':"Blimey! What beast/is THAT? It's like/the night itself!",'Duchess Ivy':"That dragon... it's/darker than my/castle dungeon!",'Grim':'......!#...Finally. A dragon/as dark as me.','Sheen':"Ooh, nice dragon./Wanna sell it? I'll/give you 20 coins.",'Aurora':"I've never seen/that dragon. Not/even in books."},21:{'Timmy':'A ROCK DRAGON?!/With GOLD cracks?!/Best rock EVER!','Lulu':'Is it... a statue?/Wait, it MOVED!/Ahh!','Rocco':'A dragon made of/ROCK! I TOLD you/rocks are the best!','Mira':'Gold cracks and/crystals? Is that/even a dragon?','Captain Vex':"That's no dragon,/it's a walking/treasure chest! Arr!",'Duchess Ivy':'Gold AND crystals!/The fanciest dragon/in all the land!','Grim':'...A stone dragon.#...It looks older/than the mountains.','Sheen':'Those crystals look/valuable. Wanna/trade? Heh heh.','Aurora':"A dragon of stone?/I didn't know they/existed. Amazing."}}
def G_arena(g,*a):
 import gc
 d=g.pick
 if d is None:
  message(['Come back when you','have a grown dragon!'],'Arena')
  return
 op=(1,g.book>>37&1 or g.book>>35&1,g.book>>38&1)
 s=choose('THE ARENA',['Section '+str(i+1)+(': '+str(10*i+10)+' tamers'if op[i]else ': locked')for i in range(3)]+['Leave'])
 if not 0<=s<3:
  return
 if not op[s]:
  message(['Win Section '+str(s),'first!'],'Arena')
  return
 fee=min(500,25+25*g.ar)
 if choose('SECTION '+str(s+1),['Enter: '+str(fee)+'c','Leave'])!=0:
  return
 if g.coins<fee:
  message(['The entry fee is',str(fee)+' coins. Come','back with more!'],'Arena')
  return
 g.coins-=fee
 g.ar+=1
 w=0
 N=10*s+10
 for i in range(N):
  T=G_tamer(s,i)
  n,k,lv,say=T[:4]
  n='???'if n[0]=='*'else n
  cls(G_NIGHT)
  ctext(24,'ROUND '+str(w+1)+' OF '+str(N),GOLD)
  for p in say.split('#'):
   message(p.split('/'),n)
  q=d[9]&7
  e=T[4].split('|')[d[1]-19]if s and 18<d[1]<22 else G_SPECIAL.get(d[1],{}).get(n,'')
  for p in e.split('#')if e else():
   message(p.split('/'),n)
  p=G_SHINE.get(n)if q else 0
  if p:
   message(p.split('|')[q-1].split('/'),n)
  if e and q and(not w):
   message((['People in the crowd','point at your dragon.'],['The crowd starts','whispering...'],['The whole crowd','goes silent...'],['The crowd ROARS!','Everyone jumps up','to see your dragon!'])[q-1],'Arena')
  d[3]=d[4]
  g.ride=d
  t=G_DT[k]
  r=4 if k==23 else t[2]
  f=(t[0],20+6*r+6*lv,4+lv+2*r,3*lv,t[3],t[1],k)
  if k==23:
   f=('Gold Dragon',)+f[1:4]+(GOLD,)+f[5:]+(2,)
  elif random.random()<0.17:
   f+=(random.randint(1,s+2),)
  gc.collect()
  if not G_battle(g,f,0,1):
   break
  w+=1
 d[3]=d[4]
 c=(0,15,30,50,75,100,130,165,200,250,300)[w]if not s else(25,30)[s-1]*w
 m=['You won '+str(w)+' of '+str(N)+' matches.','+'+str(c)+' coins!']
 if w>N*2//3:
  g.glim+=s+1
  m.append('And '+str(s+1)+' Glimmer Stone'+'s!'[s<1:])
 if w==N:
  if s<2:
   m=['SECTION '+str(s+1)+' WON!','+'+str(c)+' coins!','Section '+str(s+2)+' is open!'if not op[s+1]else 'Glimmer Stones too!']
   g.book|=1<<37+s
   if not g.book>>39+s&1:
    if len(g.bag)<5:
     g.book|=1<<39+s
     g.bag.append(random.choice([i for i in range(20)if G_DT[i][2]==s+2]))
     m.append(('And a Rare egg!','And an Epic egg!')[s])
    else:
     m.append('(No room for the egg!)')
  elif not g.book>>35&1 and len(g.bag)<5 and(G_kids(g)+4<=40):
   g.book|=1<<35
   g.bag.append(24)
   m=['GRAND CHAMPION!','+'+str(c)+' coins and a','Champion egg!']
  else:
   m=['GRAND CHAMPION!','+'+str(c)+' coins and','3 Glimmer Stones!'if g.book>>35&1 else '(no room for the egg!)']
 g.coins+=c
 message(m,'Arena')
def G_el(d):
 return G_DT[d[1]][1]
def G_beats(a,b):
 return a==3 and b!=3 or(a<3 and b==(a+2)%3)
G_TITAN=('Stone Titan',100,13,45,(230,180,60),3)
G_DREAD=('Dread Drake',70,11,30,(40,35,45),3)
G_MONP=(b'B`$\xe6\x8c\x96_<\x1e}U-<(\x14\xe6\xb4(n\xa0<\xa0\xc1\x80(<\x14\xfa\xdc<\x00\x00\x00<\x14\x14\xff\xff\xffP2\x19Z<\x1e',b'$H`<x\xa0\x8a\xae\xc6\xf0\xc8<\x00\x00\x00\xff\xff\xff\x180@\xa7\xc2\xd4',b'\xaa\x1e\x14\xf0n\x1e\xfa\xc8<\xfa\xdc<n\x14\x14\xfa\xb4P\xff\xf0x\x00\x00\x00Z\n\n\xff\xff\xff',b'HB6xnZ\xa7\xa0\x930,$\xfa\xaa(\xff\xff\xffP\x8c<',b'Z\x8c\xc8\x96\xc8\xf0\xe1\xf0\xff\xff\xff\xff\x14\x1eFx\xdc\xff',b'\x8d\x8d\x93\xeb\xeb\xf5\xf2\xf2\xf8^^b\x96\x96\xa5nn}\xbe\xd2\xeb<\x96\xe6\xff\xff\xff<\x1e2',b'PKF\x82zp\xaa\xa2\x96\xfa\xc8<\xf5\x8c\x1e\x00\x00\x00\xeb\xeb\xf0\xbe\xc3\xcd2.*')
G_MONA=(b'\x02\x002:ADAN\x02\x00j:[D[N\x02\x018?AEAK\x02\x01d?[E[K\x00\x00:l\x08\x0e\x00\x00\x00\x00Z\\\x08\x12\x00\x00\x00\x02>X \x1e\x00\x00\x00\x03>X\x0e\x1e\x00\x00\x00\x04>h \x04\x00\x00\x00\x05Lh\x04\x04\x00\x00\x01\x00NJ\x0f\x00\x00\x00\x01\x06LH\r\x00\x00\x00\x01\x07HD\x05\x00\x00\x00\x00\x08BD\t\x02\x00\x00\x00\x08QD\t\x02\x00\x00\x00\tDG\x05\x04\x00\x00\x00\tSG\x05\x04\x00\x00\x00\nFH\x02\x02\x00\x00\x00\nUH\x02\x02\x00\x00\x00\x0bFQ\x10\x04\x00\x00\x00\x0cHQ\x02\x02\x00\x00\x00\x0cRQ\x02\x02\x00\x00\x00\r`P\x05"\x00\x00\x01\rbN\x08\x00\x00\x00\x01\x0e`L\x05\x00\x00\x00\x00\x00Av\t\n\x00\x00\x00\x06Rv\t\n\x00\x00',b'\x01\x00Nd\x1c\x00\x00\x00\x01\x01J`\x19\x00\x00\x00\x01\x02BV\x08\x00\x00\x00\x01\x00>H\n\x00\x00\x00\x01\x00^H\n\x00\x00\x00\x01\x01=G\x08\x00\x00\x00\x01\x01]G\x08\x00\x00\x00\x01\x03>H\x05\x00\x00\x00\x01\x03^H\x05\x00\x00\x00\x00\x04=E\x03\x06\x00\x00\x00\x04]E\x03\x06\x00\x00\x00\x05<E\x01\x01\x00\x00\x00\x05\\E\x01\x01\x00\x00\x00\x068`,\x03\x00\x00\x01\x07Nr\x0e\x00\x00\x00\x00\x07@r\x1c\x0c\x00\x00\x01\x00@V\x03\x00\x00\x00\x00\x02?T\x01\x01\x00\x00\x01\x00ZX\x03\x00\x00\x00\x00\x02YV\x01\x01\x00\x00\x01\x00PR\x03\x00\x00\x00\x00\x02OP\x01\x01\x00\x00\x01\x00bf\x03\x00\x00\x00\x00\x02ad\x01\x01\x00\x00\x00\x002x\x0e\x06\x00\x00\x00\x00\\x\x0e\x06\x00\x00',b'\x02\x003HiH\\~\x02\x003H\\~Nl\x02\x003HNl@~\x02\x019JcJXt\x02\x019JXtNf\x02\x019JNfDt\x02\x02BPZPNh\x02\x03`dpRfr\x02\x04?<G$E8\x02\x04]<U$W8\x01\x00ND\x11\x00\x00\x00\x01\x01LB\x0f\x00\x00\x00\x01\x05G<\x05\x00\x00\x00\x00\x04C>\x07\x03\x00\x00\x00\x04R>\x07\x03\x00\x00\x00\x06DA\x05\x05\x00\x00\x00\x06SA\x05\x05\x00\x00\x00\x07FB\x02\x03\x00\x00\x00\x07UB\x02\x03\x00\x00\x00\x08EL\x12\x03\x00\x00\x00\tGL\x02\x02\x00\x00\x00\tSL\x02\x02\x00\x00',b'\x00\x00*T\x0e$\x00\x00\x00\x00dT\x0e$\x00\x00\x01\x001z\x08\x00\x00\x00\x01\x00kz\x08\x00\x00\x00\x00\x008P,,\x00\x00\x00\x018P&(\x00\x00\x00\x02<T\x0c\x14\x00\x00\x00\x03>|\x0c\x08\x00\x00\x00\x03R|\x0c\x08\x00\x00\x01\x00NB\x12\x00\x00\x00\x01\x01L@\x10\x00\x00\x00\x01\x02F:\x06\x00\x00\x00\x00\x03B;\x08\x02\x00\x00\x00\x03R;\x08\x02\x00\x00\x00\x04D>\x05\x04\x00\x00\x00\x04S>\x05\x04\x00\x00\x00\x03EI\x12\x04\x00\x00\x00\x05FI\x03\x02\x00\x00\x00\x05SI\x03\x02\x00\x00\x00\x06B0\x0e\x05\x00\x00\x01\x03@\\\x04\x00\x00\x00\x00\x02>Y\x02\x01\x00\x00\x01\x03Vf\x04\x00\x00\x00\x00\x02Tc\x02\x01\x00\x00\x01\x03Hp\x04\x00\x00\x00\x00\x02Fm\x02\x01\x00\x00\x01\x03ZV\x04\x00\x00\x00\x00\x02XS\x02\x01\x00\x00\x00\x03PX\x01\n\x00\x00\x00\x03Pa\x07\x01\x00\x00',b'\x02\x003HiH\\~\x02\x003H\\~Nl\x02\x003HNl@~\x02\x019HaHVv\x02\x019HVvNh\x02\x019HNhDv\x02\x02>JPJHl\x02\x034r:\x82@r\x02\x03@rF\x82Lr\x02\x03LrR\x82Xr\x02\x03Xr^\x82dr\x01\x00ND\x11\x00\x00\x00\x01\x01LB\x0f\x00\x00\x00\x01\x02G<\x05\x00\x00\x00\x00\x04C>\x08\t\x00\x00\x00\x04Q>\x08\t\x00\x00\x00\x05EA\x04\x04\x00\x00\x00\x05SA\x04\x04\x00\x00\x00\x04HL\x0c\x06\x00\x00\x01\x02p:\x03\x00\x00\x00\x01\x02,X\x02\x00\x00\x00',b'\x00\x00*T\x0e$\x00\x00\x00\x00dT\x0e$\x00\x00\x01\x001z\x08\x00\x00\x00\x01\x00kz\x08\x00\x00\x00\x00\x008P,,\x00\x00\x00\x018P&(\x00\x00\x00\x02<T\x0c\x14\x00\x00\x00\x03>|\x0c\x08\x00\x00\x00\x03R|\x0c\x08\x00\x00\x01\x00NB\x12\x00\x00\x00\x01\x01L@\x10\x00\x00\x00\x01\x02F:\x06\x00\x00\x00\x00\x03B;\x08\x02\x00\x00\x00\x03R;\x08\x02\x00\x00\x02\x04@48"F2\x02\x04\\4d"V2\x02\x05@4<(F2\x02\x05\\4`(V2\x01\x06NF\n\x00\x00\x00\x00\x07D>\x05\x05\x00\x00\x00\x07S>\x05\x05\x00\x00\x00\x08E?\x02\x02\x00\x00\x00\x08T?\x02\x02\x00\x00\x00\tFJ\x10\x04\x00\x00\x00\x08GJ\x02\x03\x00\x00\x00\x08SJ\x02\x03\x00\x00\x00\x06:t\x04\x06\x00\x00\x00\x06<X\x03\x06\x00\x00\x00\x06Bt\x04\x06\x00\x00\x00\x06DX\x03\x06\x00\x00\x00\x06Jt\x04\x06\x00\x00\x00\x06LX\x03\x06\x00\x00\x00\x06Rt\x04\x06\x00\x00\x00\x06TX\x03\x06\x00\x00\x00\x06Zt\x04\x06\x00\x00\x00\x06\\X\x03\x06\x00\x00',b'\x00\x00:l\x0e\x16\x00\x00\x00\x00Tl\x0e\x16\x00\x00\x00\x01<l\n\x14\x00\x00\x00\x01Vl\n\x14\x00\x00\x01\x00,Z\n\x00\x00\x00\x00\x00&Z\x0c\x1e\x00\x00\x01\x00pZ\n\x00\x00\x00\x00\x00jZ\x0c\x1e\x00\x00\x01\x00,x\t\x00\x00\x00\x01\x00px\t\x00\x00\x00\x01\x01,X\x08\x00\x00\x00\x01\x01pX\x08\x00\x00\x00\x01\x01+v\x06\x00\x00\x00\x01\x01ov\x06\x00\x00\x00\x01\x00NZ\x1a\x00\x00\x00\x01\x01LX\x17\x00\x00\x00\x01\x02DP\x08\x00\x00\x00\x01\x00N8\x0f\x00\x00\x00\x01\x01M7\r\x00\x00\x00\x01\x02H2\x04\x00\x00\x00\x02\x074J86>H\x02\x07^Hd6hJ\x02\x066H86:H\x02\x06bHd6eH\x00\x08B2\x18\x04\x00\x00\x00\x03E7\x06\x04\x00\x00\x00\x03R7\x06\x04\x00\x00\x00\x04H@\x0c\x02\x00\x00\x00\x04DR\x02\x0c\x00\x00\x00\x04D\\\n\x02\x00\x00\x00\x04N\\\x02\n\x00\x00\x00\x04VN\x02\x08\x00\x00\x00\x04VN\x08\x02\x00\x00\x00\x03ES\x01\n\x00\x00\x00\x03O]\x01\x08\x00\x00\x01\x03NX\x04\x00\x00\x00\x01\x06NX\x02\x00\x00\x00\x01\x01$0\x04\x00\x00\x00\x01\x01x6\x03\x00\x00\x00\x01\x02#/\x01\x00\x00\x00')
GREEN=(50,190,80)
DARK=(40,40,40)
def G_bar(x,y,w,v,mx,c):
 f=max(0,min(w,int(w*v/mx)))if v>0 else 0
 if v>0:
  f=max(2,f)
 rect(x,y,f,6,c)
 rect(x+f,y,w-f,6,DARK)
def G_foe_art(f):
 n=f[0]
 if len(f)>6:
  G_drag(162,42,2,f[6],f[4],sp=f[7]if len(f)>7 else 0)
 elif f is G_BOSS or f is G_DREAD:
  G_drag(162,42,2,22 if f is G_DREAD else 8,f[4])
 else:
  k=([m[0]for l in G_FOES for m in l]+[G_TITAN[0]]).index(n)
  G_art(G_MONA[k],142,12,1,G_cl(G_MONP[k]))
def G_foe_screen(f,title):
 cls()
 rbox(150,30,140,120,10,RED if f is G_DREAD else f[4],2,G_NIGHT)
 G_foe_art(f)
 ctext(24,title,GOLD)
def G_battle(g,f,lv=0,ar=0):
 name,fhp,fat,xp,fc,fe=f[:6]
 up=lv-G_LVL[g.m][0]if lv else 0
 fhp,fat,xp=(fhp+4*up,fat+up,xp+3*up)
 who=('Lv '+str(lv)+' 'if lv else '')+name
 mx=fhp
 G_foe_screen(f,who+' appears!')
 log=''
 sel=0
 was=None
 while True:
  d=g.ride
  opts=('Claw','Breath','Run')if d is not None else('Sword','Run')
  n=len(opts)
  w=300//n
  sel=min(sel,n-1)
  now=(d[0]if d else 'You',d[3]if d else g.hp,fhp,sel,log,n)
  if was is None or was[0]!=now[0]:
   rect(0,40,148,60,BLACK)
   rect(0,150,320,34,BLACK)
   text(12,56,now[0],d[6]if d and d[1]!=19 else WHITE)
   text(12,86,name[:12],RED if f is G_DREAD else fc)
   for i in range(n):
    cc=GOLD if i==sel else WHITE
    rbox(10+i*w,154,w-6,24,8,cc)
    text(10+i*w+(w-6)//2-len(opts[i])*5,172,opts[i],cc)
   was=None
  if was is None or was[1]!=now[1]:
   G_bar(12,62,120,now[1],d[4]if d else g.mhp,GREEN)
  if was is None or was[2]!=fhp:
   G_bar(12,92,120,fhp,mx,RED)
  if was is not None and was[3]!=sel:
   for i in(was[3],sel):
    cc=GOLD if i==sel else WHITE
    edge(10+i*w,154,w-6,24,8,cc)
    text(10+i*w+(w-6)//2-len(opts[i])*5,172,opts[i],cc)
  if was is None or was[4]!=log:
   rect(0,186,320,24,BLACK)
   text(6,202,log[:31],GREY)
  was=now
  k=wkey()
  if k in(LEFT,RIGHT):
   sel=(sel+(1 if k==RIGHT else-1))%n
   continue
  if k!=OK:
   continue
  o=opts[sel]
  if o=='Run':
   if f is G_BOSS:
    log='The Wyrm blocks your way!'
    continue
   if ar:
    return 0
   if random.random()<0.6:
    return 2
   log="Couldn't get away."
  elif o=='Sword':
   dm=random.randint(3,5)
   fhp-=dm
   log='Sword hits for '+str(dm)+'.'
  else:
   q=(d[1]==20)+2*(d[1]==21)+(d[1]==24)
   at=5+2*d[2]+2*G_DT[d[1]][2]+q
   if o=='Claw':
    dm=at+random.randint(0,2+q)
    log='Claw hits for '+str(dm)+'.'
   else:
    dm=at+random.randint(2+q,5+2*q)
    if G_beats(G_el(d),fe):
     dm*=2
     log='Super breath! '+str(dm)+'.'
    elif G_beats(fe,G_el(d)):
     dm//=2
     log='Weak breath... '+str(dm)+'.'
    else:
     log='Breath hits for '+str(dm)+'.'
   fhp-=dm
  if len(f)>7 and f[6]==23 and(0<fhp<=mx//2):
   f=(G_DT[23][0],)+f[1:4]+(G_DT[23][3],)+f[5:7]
   name=who=f[0]
   message(['The shine is flaking',"off... It's just a",'DUSTMITE!'],'Huh?')
   message(['Uh... a very rare','Dustmite! Still','counts! Heh...'],'Sheen')
   G_foe_screen(f,who)
   was=None
  if fhp<=0:
   msg=[]
   for dd in g.pen:
    if dd[3]>0 and(dd is d or dd is g.pick)and(not ar):
     dd[5]+=xp
     while dd[5]>=dd[2]*10:
      dd[5]-=dd[2]*10
      dd[2]+=1
      dd[4]+=6
      dd[3]=dd[4]
      msg.append(dd[0]+' is now level '+str(dd[2])+'!')
   if lv>=5:
    k=g.curse and g.cd<15
    g.cd+=k
    c=lv*(1+k)
    g.coins+=c
    msg=['+'+str(c)+' coins!']+msg
   message(msg[:3]or['You won!'],who+' beaten')
   if f is not G_BOSS and(not ar):
    G_quest_step(g,0,name)
    G_quest_step(g,2,g.m)
   return True
  dm=max(1,fat+random.randint(0,3)-(d[2]if d else 0))
  log+=' It hits '+str(dm)+'.'
  if d is not None:
   d[3]=max(0,d[3]-dm)
   if d[3]==0:
    if ar:
     message([d[0]+' is knocked out!'],'Arena')
     return 0
    g.ride=None
    message([d[0]+' is too tired to fly.','You fight on foot!'],'Oh no')
    G_foe_screen(f,who)
    was=None
  else:
   g.hp-=dm
   if g.hp<=0:
    cls()
    ctext(60,'YOU DIED',RED)
    message(['The '+name+' won.','Back to your last save.'],'Game over')
    return False
def G_evil(g):
 cls()
 ctext(90,'The sky goes dark...',RED)
 pause(0.8)
 r=G_battle(g,G_DREAD)
 if not r:
  return False
 G_draw_map(g)
 if r==2:
  g.dread=random.randint(900,1100)
  message(['You got away...','but the Dread Drake','will be back!'],'Escaped')
  G_draw_map(g,True)
  return True
 g.dread=0
 g.book|=1<<25
 if not G_put_egg(g,20,True)and len(g.bag)<5:
  g.bag.append(20)
 message(['The Dread Drake flies','away... and leaves a','strange egg behind!'],'Whoa!')
 G_draw_map(g,True)
 return True
def G_titan(g,a=0):
 if a:
  return G_arena(g)
 G_draw_map(g)
 message(['A cave! Letters are','carved over the door:','P E T R A'],'Hidden cave')
 cls()
 ctext(90,'The ground shakes...',GOLD)
 pause(0.8)
 r=G_battle(g,G_TITAN)
 if not r:
  return False
 if r==2:
  G_draw_map(g)
  message(['You ran out of the cave.','The Stone Titan waits...'],'Escaped')
  G_draw_map(g,True)
  return True
 g.book|=1<<26
 G_draw_map(g)
 if not G_put_egg(g,21,True)and len(g.bag)<5:
  g.bag.append(21)
 message(['The Stone Titan crumbles','... and an egg of stone','rolls out!'],'Whoa!')
 G_draw_map(g,True)
 return True
