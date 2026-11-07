# Counts drawing calls per frame (between two key reads) and estimates the
# time on a real Evo, using the GHBENCH numbers from Petra's calculator.
# python3 calls.py [GAMES...]
import sys, random
sys.path[:0] = ['.', '../calc']
import simstate as S, ti_draw
from ti_system import SimDone
import time; time.sleep = lambda s: None
MS = {'set_color': 5.5, 'fill_rect': 6.8, 'clear_rect': 6.8, 'draw_rect': 7.9, 'fill_circle': 9.0,
      'draw_circle': 9.0, 'draw_line': 7.9, 'draw_text': 5.5, 'fill_poly': 12.1, 'draw_poly': 12.1, 'clear': 7.0}
cur = {}
def wrap(f):
    o = getattr(ti_draw, f)
    def w(*a):
        cur[f] = cur.get(f, 0) + 1
        return o(*a)
    return w
for f in MS:
    if hasattr(ti_draw, f):
        setattr(ti_draw, f, wrap(f))
frames = []
def poll():
    if cur:
        frames.append(dict(cur))
        cur.clear()
S.on_poll = poll
def ms(d):
    return sum(MS[k] * v for k, v in d.items())
mods = sys.argv[1:] or ['GHTTT', 'GHSIMON', 'GHHANG', 'GHMERGE', 'GHPONG', 'GHBREAK', 'GHFLAP', 'GHBLOCKS', 'GHSUDOKU', 'GHSOLI', 'GHRPG', 'GHSPACE', 'GHFORTUN', 'GHANIM']
pool = [25, 34, 24, 26, 105, 105, 21, 23, 92, 93, 0, 0]
for mod in mods:
    frames.clear(); cur.clear()
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
        g = m.play if mod in ('GHRPG',) else (m.studio if mod == 'GHANIM' else m.game)
        n = g.__code__.co_argcount
        g(*([True, 40][:n] if mod == 'GHTTT' else [40][:n]))
    except SimDone:
        pass
    if not frames:
        print(mod, 'no frames'); continue
    first = frames[0]
    rest = sorted(ms(f) for f in frames[1:]) or [0]
    worst = max(frames[1:] or [first], key=ms)
    print('%-9s first %4d calls %5.0f ms | later: median %4.0f ms, 90%% %4.0f ms, worst %4.0f ms %s' % (
        mod, sum(first.values()), ms(first), rest[len(rest) // 2], rest[len(rest) * 9 // 10], rest[-1],
        ' '.join('%s=%d' % (k.replace('fill_', 'f').replace('draw_', 'd'), v) for k, v in sorted(worst.items()))))
