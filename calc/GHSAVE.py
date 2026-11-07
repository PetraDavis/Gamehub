# GAMEHUB save helper. Only the Animation Studio and Dragon Tamer save.
# An animation in slot s is stored in calculator lists named A<s>H (header)
# and A<s>000, A<s>001, ... (data). Each number holds 5 bytes.
from ti_system import store_list, recall_list

SLOTS = 3
PER = 100
B = 5


def hname(s):
    return "A" + str(s) + "H"


def dname(s, i):
    n = str(i)
    return "A" + str(s) + "0" * (3 - len(n)) + n


def info(s):
    # returns (frames, fps) or None
    try:
        h = recall_list(hname(s))
        if len(h) >= 4 and int(h[0]) == 1:
            return int(h[1]), int(h[2])
    except Exception:
        pass
    return None


def save(s, data, frames, fps, show=None):
    # data: bytearray. Returns number of lists used.
    nums = []
    n = len(data)
    i = 0
    while i < n:
        v = 0
        for j in range(B):
            v = v * 256 + (data[i + j] if i + j < n else 0)
        nums.append(v)
        i += B
    nl = (len(nums) + PER - 1) // PER
    for k in range(nl):
        if show:
            show(k, nl)
        store_list(dname(s, k), nums[k * PER:(k + 1) * PER])
    old = 0
    try:
        old = int(recall_list(hname(s))[3])
    except Exception:
        pass
    for k in range(nl, old):
        try:
            store_list(dname(s, k), [0])
        except Exception:
            pass
    store_list(hname(s), [1, frames, fps, nl, n])
    return nl


def load(s, show=None):
    h = recall_list(hname(s))
    frames, fps, nl, n = int(h[1]), int(h[2]), int(h[3]), int(h[4])
    data = bytearray(n)
    p = 0
    for k in range(nl):
        if show:
            show(k, nl)
        for v in recall_list(dname(s, k)):
            v = int(v)
            chunk = []
            for j in range(B):
                chunk.append(v % 256)
                v //= 256
            for j in range(B - 1, -1, -1):
                if p < n:
                    data[p] = chunk[j]
                    p += 1
    return data, frames, fps


def wipe():
    n = 0
    for s in range(1, SLOTS + 1):
        try:
            h = recall_list(hname(s))
            nl = int(h[3])
        except Exception:
            continue
        for k in range(nl):
            try:
                store_list(dname(s, k), [0])
                n += 1
            except Exception:
                pass
        store_list(hname(s), [0])
        n += 1
    # Dragon Tamer keeps its dragons in one list too
    try:
        recall_list("DRG")
        store_list("DRG", [0])
        n += 1
    except Exception:
        pass
    return n
