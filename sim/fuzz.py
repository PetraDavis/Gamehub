# Press random keys in every game to look for crashes.
import sys, random
sys.path[:0] = ['.', '../calc']
import simstate as S, ti_system
from ti_system import SimDone
import time; time.sleep = lambda s: None
mods = sys.argv[1:] or ['GHTTT', 'GHSIMON', 'GHHANG', 'GHMERGE', 'GHPONG', 'GHBREAK', 'GHFLAP', 'GHBLOCKS', 'GHSUDOKU', 'GHSOLI', 'GHRPG', 'GHSPACE']
pool = [25, 34, 24, 26, 105, 105, 21, 23, 92, 93, 0, 0]
for m in mods:
    for seed in range(25):
        random.seed(seed)
        S.keys = [105] + [random.choice(pool) for _ in range(600)]
        S.polls = 0
        sys.modules.pop(m, None)
        try:
            mod = __import__(m)
            mod.main()
        except SimDone:
            pass
        except Exception as e:
            print('CRASH', m, seed, repr(e)); import traceback; traceback.print_exc(); break
    print('ok', m)
