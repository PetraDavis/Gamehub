# usage: python3 run.py MODULE outdir key key 'shot:name' ...
# key names: up down left right ok clr del 2nd, or numbers; 'wN' = N empty polls; 'name' with ':' = screenshot
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'calc'))
import simstate as S, random
random.seed(int(os.environ.get('SEED', '1')))
N = {'up': 25, 'down': 34, 'left': 24, 'right': 26, 'ok': 105, 'clr': 45, 'del': 23, '2nd': 21}
mod, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True); S.outdir = out
S.gap = int(os.environ.get('GAP', '0'))
for a in sys.argv[3:]:
    if a.startswith('shot:'): S.keys.append(a[5:])
    elif a.startswith('w') and a[1:].isdigit(): S.keys.extend([0] * int(a[1:]))
    elif a in N: S.keys.append(N[a])
    else: S.keys.append(int(a))
import ti_system
import time as _t
_t.sleep = lambda s: None
from ti_system import SimDone
try:
    m = __import__(mod)
    if hasattr(m, 'main'): m.main()
except SimDone:
    pass
S.shot('final')
print('polls', S.polls, 'ops', S.ops, 'lists', {k: len(v) for k, v in S.lists.items()})
