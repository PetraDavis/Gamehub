# Desktop stand-in for ti_system. Keys come from simstate.keys (a list of codes);
# get_key(0) returns 0 between scripted keys for `gap` polls.
import simstate as S
class SimDone(Exception): pass
def _next(block):
    S.polls += 1
    if S.on_poll: S.on_poll()
    if S.keys:
        if block or S.gapleft <= 0:
            S.gapleft = S.gap
            k = S.keys.pop(0)
            if block and k == 0: return _next(block)
            if isinstance(k, str):
                S.shot(k); return _next(block)
            return k
        S.gapleft -= 1
        return 0
    if block or S.polls > S.maxpolls: raise SimDone()
    return 0
def wait_key(): return _next(True)
def get_key(n=0): return _next(n != 0)
def escape(): return False
def disp_clr(*a): pass
def disp_at(*a): pass
def disp_wait(*a): pass
def sleep(s): S.t += s
def wait(s): S.t += s
_lists = S.lists
def store_list(name, lst):
    if len(lst) > 100: raise ValueError('list too long')
    for v in lst:
        if isinstance(v, bool) or not isinstance(v, (int, float)): raise TypeError('numbers only')
    _lists[name] = [float(v) for v in lst]
def recall_list(name):
    if name not in _lists: raise ValueError('no such list')
    return list(_lists[name])
