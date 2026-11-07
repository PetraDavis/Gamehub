# Press random keys in the one-file builds (dist/) to look for crashes.
import sys, random, os
sys.path[:0] = ['.']
import simstate as S, ti_system
from ti_system import SimDone
import time; time.sleep = lambda s: None
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dist')
names = sys.argv[1:] or sorted(f[:-3] for f in os.listdir(D) if f.endswith('.py'))
pool = [25, 34, 24, 26, 105, 105, 21, 23, 92, 93, 45, 0, 0]
bad = 0
for m in names:
    src = compile(open(os.path.join(D, m + '.py')).read(), m, 'exec')
    for seed in range(25 if m != 'GAMEHUB' else 80):
        random.seed(seed)
        S.keys = [105] + [random.choice(pool) for _ in range(800)]
        S.polls = 0
        try:
            exec(src, {'__name__': '__main__'})
        except SimDone:
            pass
        except Exception as e:
            bad += 1
            print('CRASH', m, seed, repr(e)); import traceback; traceback.print_exc(); break
    print('ok' if not bad else 'checked', m)
