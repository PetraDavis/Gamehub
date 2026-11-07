# Finds visible redrawing: pixels that change colour more than once between
# two key reads (one frame), so the player sees them flash.
# python3 flicker.py [GAMES...]
import sys, random
sys.path[:0] = ['.', '../calc']
import numpy as np
import simstate as S, ti_draw
from ti_system import SimDone
import time; time.sleep = lambda s: None
st = {'prev': None, 'n': None, 'start': None, 'worst': 0, 'tot': 0, 'frames': 0}
def snap():
    return np.asarray(S.img, dtype=np.int16)
def wrap(f):
    o = getattr(ti_draw, f)
    def w(*a):
        r = o(*a)
        cur = snap()
        if st['prev'] is not None and st['n'] is not None:
            ch = (cur != st['prev']).any(axis=2)
            st['n'] += ch
        st['prev'] = cur
        return r
    return w
for f in ('fill_rect', 'fill_circle', 'draw_line', 'draw_circle', 'fill_poly', 'draw_text', 'draw_poly', 'draw_rect', 'clear_rect', 'clear'):
    setattr(ti_draw, f, wrap(f))
def frame():
    cur = snap()
    if st['n'] is not None:
        # flashed: painted 2+ times in the frame (an in-between colour was visible)
        same = (cur == st['start']).all(axis=2)
        fl = int(((st['n'] >= 1) & same).sum())
        st['frames'] += 1
        st['tot'] += fl
        if fl > st['worst']:
            st['worst'] = fl
            S.img.save('/tmp/flick_%s.png' % mod)
    st['n'] = np.zeros(cur.shape[:2], dtype=np.int32)
    st['prev'] = cur
    st['start'] = cur
S.on_poll = frame
mods = sys.argv[1:] or ['GHTTT', 'GHSIMON', 'GHHANG', 'GHMERGE', 'GHPONG', 'GHBREAK', 'GHFLAP', 'GHBLOCKS', 'GHSUDOKU', 'GHSOLI', 'GHRPG', 'GHSPACE', 'GHFORTUN']
pool = [25, 34, 24, 26, 105, 105, 21, 23, 92, 93, 0, 0]
for mod in mods:
    st.update(prev=None, n=None, worst=0, tot=0, frames=0)
    random.seed(1)
    S.keys = [random.choice(pool) for _ in range(300)]
    S.polls = 0; S.maxpolls = 3000
    sys.modules.pop(mod, None)
    m = __import__(mod)
    if hasattr(m, 'now'):
        c = [0.0]
        def fake(c=c): c[0] += 0.05; return c[0]
        m.now = fake
    try:
        g = m.play if mod in ('GHRPG', 'GHCRYPT') else m.game
        n = g.__code__.co_argcount
        g(*([True, 40][:n] if mod == 'GHTTT' else [40][:n]))
    except SimDone:
        pass
    print('%-9s frames %5d  flashing px/frame avg %7.0f  worst %6d' % (mod, st['frames'], st['tot'] / max(1, st['frames']), st['worst']))
