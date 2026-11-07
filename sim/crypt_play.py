import sys, math, os
sys.path[:0] = ['.', '../calc']
import simstate as S, ti_system
import time; time.sleep = lambda s: None
import GHCRYPT as C
from ti_system import SimDone
out = sys.argv[1]; os.makedirs(out, exist_ok=True); S.outdir = out
def word_keys(w):
    ks=[]; sel=0
    for ch in w:
        t=ord(ch)-65
        # move by rights (simple)
        while sel!=t:
            ks.append(26); sel=(sel+1)%26
        ks.append(105)
    return ks
def go(x,y,a):
    g.x,g.y,g.a=x,y,a
    f=C.facing(g); print('facing',f); return f
g=C.St()
g.power=g.locked=g.note=g.closet=g.living=g.tv=False
g.tapheard=g.notebook=g.awake=g.armed=g.sighted=False
g.flash=True;g.blackout=False;g.won=False;g.hidden=False;g.ys_vis=False
g.ystate='dormant';g.ytimer=0;g.yx=g.yy=0;g.shown=None
S.keys=[105]*3; C.use(g, go(8.5,6.5,math.pi/2)); print('power',g.power,g.locked)
S.keys=[105]; C.use(g, go(6.4,3.5,math.pi)); print('note',g.note,g.armed)
S.keys=['ys1']+[105]; C.sighting(g)
S.keys=word_keys('ECHO')+['closetok',105]; C.use(g, go(12.4,6.5,0)); print('closet',g.closet)
S.keys=[105,105]; C.use(g, go(6.3,5.5,math.pi)); print('living',g.living, C.solid(g,5.5,5.5))
S.keys=['tv',105,105]; C.use(g, go(1.0,5.5,math.pi)); print('tap',g.tapheard,g.awake)
S.keys=[105,105]; f=go(2.9,4.6,math.pi); C.use(g,f); print('notebook',g.notebook)
# Ysolde hunt sim
g.x,g.y,g.a=9.5,4.5,-math.pi/2
S.keys=[105]*5
for i in range(80):
    C.ys_update(g,0.5)
    if g.ystate=='hunt' and i%10==0: C.render(g)
print('ystate',g.ystate,'pos',round(g.x,1),round(g.y,1))
S.keys=word_keys('QUIET'); C.use(g, go(12.4,2.5,0)); print('won',g.won)
S.keys=['end',45]; C.ending()
