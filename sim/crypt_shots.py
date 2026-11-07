import sys, math, os
sys.path[:0] = ['.', '../calc']
import simstate as S
import ti_draw
import GHCRYPT as C
out = sys.argv[1]; os.makedirs(out, exist_ok=True); S.outdir = out
def mk():
    g = C.St()
    g.power = g.locked = g.note = g.closet = g.living = g.tv = False
    g.tapheard = g.notebook = g.awake = g.armed = g.sighted = False
    g.flash = True; g.blackout = False; g.won = False; g.hidden = False; g.ys_vis = False
    g.ystate = 'dormant'; g.ytimer = 0; g.yx = g.yy = 0; g.shown = None
    return g
def shot(g, name, x, y, a):
    g.x, g.y, g.a = x, y, a; g.shown = None
    C.render(g); f = C.facing(g); C.bottom(g, C.label(g, f) if f else C.objective(g).split('\n')[0]); S.shot(name)
g = mk()
shot(g, '1dark_north', 9.5, 6.4, -math.pi/2)
shot(g, '2dark_door', 9.0, 5.9, math.pi/2)
g.power = g.locked = True
shot(g, '3lit_stairs', 9.5, 6.4, -math.pi/2)
shot(g, '4clock', 7.2, 3.5, math.pi)
shot(g, '5closet', 11.6, 6.3, 0)
g.note = g.closet = g.living = g.tv = True
shot(g, '6living', 5.6, 5.5, math.pi)
shot(g, '7livingtv', 3.5, 4.4, math.pi*0.85)
shot(g, '8library', 6.5, 2.4, math.pi)
g.ys_vis = True; g.yx, g.yy = 9.5, 2.5
shot(g, '9ysolde', 9.5, 6.0, -math.pi/2)
shot(g, '10keypad', 12.3, 2.4, 0)
