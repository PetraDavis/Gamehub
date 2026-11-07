# GHANIM from GAMEHUB, on its own. Run it.
from ti_draw import *
from ti_system import *
import time
import random
import math
from ti_system import store_list, recall_list
UP = 25
DOWN = 34
LEFT = 24
RIGHT = 26
OK = 105
CLR = 45
DEL = 23
SECOND = 21
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (230, 180, 40)
GREY = (110, 110, 110)
DARK = (40, 40, 40)
RED = (220, 50, 50)
H = 210
def key():
    return get_key(0)
def wkey():
    return wait_key()
def col(c):
    set_color(c[0], c[1], c[2])
def rect(x, y, w, h, c):
    if w < 2 or h < 2:
        if w < 1 or h < 1:
            return
        col(c)
        draw_line(x, y, x + w - 1, y + h - 1)
        return
    col(c)
    fill_rect(x, y, w, h)
def cls(c=BLACK):
    col(c)
    fill_rect(-1, -1, 322, 212)
def text(x, y, s, c=WHITE):
    col(c)
    draw_text(x, y, s)
def ctext(y, s, c=WHITE, cx=160):
    col(c)
    draw_text(cx - len(s) * 5, y, s)
def circ(x, y, r, c):
    col(c)
    fill_circle(x, y, r)
def ring(x, y, r, c, t=2, inner=BLACK):
    col(c)
    fill_circle(x, y, r)
    col(inner)
    fill_circle(x, y, r - t)
def rrect(x, y, w, h, r, c):
    col(c)
    fill_rect(x + r, y, w - 2 * r, h)
    fill_rect(x, y + r, w, h - 2 * r)
    fill_circle(x + r, y + r, r)
    fill_circle(x + w - r - 1, y + r, r)
    fill_circle(x + r, y + h - r - 1, r)
    fill_circle(x + w - r - 1, y + h - r - 1, r)
def rbox(x, y, w, h, r, c, t=2, inner=BLACK):
    rrect(x, y, w, h, r, c)
    rrect(x + t, y + t, w - 2 * t, h - 2 * t, max(r - t, 2), inner)
def pause(s):
    time.sleep(s)
def message(lines, title=None):
    n = len(lines) + (1 if title else 0)
    h = n * 18 + 30
    y = (H - h) // 2
    rbox(20, y, 280, h, 8, WHITE)
    yy = y + 24
    if title:
        ctext(yy, title, GOLD)
        yy += 18
    for s in lines:
        ctext(yy, s)
        yy += 18
    while True:
        k = wkey()
        if k in (OK, CLR):
            return k
def choose(title, opts, sel=0):
    cls()
    ctext(24, title, GOLD)
    n = len(opts)
    while True:
        for i in range(n):
            y = 40 + i * 30
            c = GOLD if i == sel else WHITE
            rbox(60, y, 200, 24, 8, c)
            ctext(y + 18, opts[i], c)
        k = wkey()
        if k == UP:
            sel = (sel - 1) % n
        elif k == DOWN:
            sel = (sel + 1) % n
        elif k == OK:
            return sel
        elif k == CLR:
            return -1
def _wrap(s, n=30):
    out = []
    line = ''
    for w in s.split(' '):
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = (line + ' ' + w).strip()
    if line:
        out.append(line)
    return out
def how_to(title, rules, buttons):
    cls()
    ctext(20, 'HOW TO PLAY', GOLD)
    ctext(38, title, GREY)
    y = 60
    for ln in _wrap(rules):
        text(8, y, ln)
        y += 16
    y += 6
    text(8, y, 'BUTTONS', GOLD)
    y += 17
    for b in buttons:
        text(8, y, b)
        y += 16
    text(8, 206, 'ENTER: back', GREY)
    while wkey() not in (OK, CLR, UP, DOWN):
        pass
def home(mod, title, rules, buttons, opts=('Play', 'Back'), sel=0):
    n = len(opts)
    while True:
        cls()
        ring(160, 58, 36, GOLD, 3)
        try:
            circ(160, 58, 33, icons_bg(mod))
            icons_draw(mod, 160, 58, WHITE)
        except Exception:
            pass
        ctext(122, title, GOLD)
        ctext(146, 'Up/Down: how to play', GREY)
        bw = (300 - (n - 1) * 8) // n
        while True:
            for i in range(n):
                x = 10 + i * (bw + 8)
                c = GOLD if i == sel else WHITE
                rect(x, 166, bw, 28, BLACK)
                rbox(x, 166, bw, 28, 10, c)
                text(x + bw // 2 - len(opts[i]) * 5, 186, opts[i], c)
            k = wkey()
            if k == LEFT:
                sel = (sel - 1) % n
            elif k == RIGHT:
                sel = (sel + 1) % n
            elif k in (UP, DOWN):
                how_to(title, rules, buttons)
                break
            elif k == CLR:
                return -1
            elif k == OK:
                if opts[sel] == 'Back':
                    return -1
                return sel
icons_BLACK = (0, 0, 0)
icons_WHITE = (255, 255, 255)
icons_RED = (215, 40, 40)
icons_BG = {'GHANIM': icons_WHITE}
def icons_c_(c):
    set_color(c[0], c[1], c[2])
def icons_box(x, y, w, h, c):
    icons_c_(c)
    fill_rect(int(x), int(y), max(2, int(w)), max(2, int(h)))
def icons_circ(x, y, r, c):
    icons_c_(c)
    fill_circle(int(x), int(y), int(r))
def icons_anim(x, y, c):
    icons_box(x - 20, y - 13, 41, 27, (35, 35, 40))
    for i in range(5):
        icons_box(x - 18 + i * 8, y - 11, 4, 3, icons_WHITE)
        icons_box(x - 18 + i * 8, y + 9, 4, 3, icons_WHITE)
    for i, by in enumerate((4, -2, 2)):
        fx = x - 17 + i * 12
        icons_box(fx, y - 6, 11, 13, (120, 200, 240))
        icons_box(fx, y + 4, 11, 3, (70, 170, 80))
        icons_circ(fx + 5, y + by, 2, (240, 120, 40))
    icons_circ(x + 17, y - 9, 1, icons_RED)
icons_ICONS = {'GHANIM': icons_anim}
def icons_bg(mod):
    return icons_BG.get(mod, icons_BLACK)
def icons_draw(mod, x, y, c):
    f = icons_ICONS.get(mod)
    if f:
        f(x, y, c)
save_SLOTS = 3
save_PER = 100
save_B = 5
def save_hname(s):
    return 'A' + str(s) + 'H'
def save_dname(s, i):
    n = str(i)
    return 'A' + str(s) + '0' * (3 - len(n)) + n
def save_info(s):
    try:
        h = recall_list(save_hname(s))
        if len(h) >= 4 and int(h[0]) == 1:
            return (int(h[1]), int(h[2]))
    except Exception:
        pass
    return None
def save_save(s, data, frames, fps, show=None):
    nums = []
    n = len(data)
    i = 0
    while i < n:
        v = 0
        for j in range(save_B):
            v = v * 256 + (data[i + j] if i + j < n else 0)
        nums.append(v)
        i += save_B
    nl = (len(nums) + save_PER - 1) // save_PER
    for k in range(nl):
        if show:
            show(k, nl)
        store_list(save_dname(s, k), nums[k * save_PER:(k + 1) * save_PER])
    old = 0
    try:
        old = int(recall_list(save_hname(s))[3])
    except Exception:
        pass
    for k in range(nl, old):
        try:
            store_list(save_dname(s, k), [0])
        except Exception:
            pass
    store_list(save_hname(s), [1, frames, fps, nl, n])
    return nl
def save_load(s, show=None):
    h = recall_list(save_hname(s))
    frames, fps, nl, n = (int(h[1]), int(h[2]), int(h[3]), int(h[4]))
    data = bytearray(n)
    p = 0
    for k in range(nl):
        if show:
            show(k, nl)
        for v in recall_list(save_dname(s, k)):
            v = int(v)
            chunk = []
            for j in range(save_B):
                chunk.append(v % 256)
                v //= 256
            for j in range(save_B - 1, -1, -1):
                if p < n:
                    data[p] = chunk[j]
                    p += 1
    return (data, frames, fps)
anim_CWD = 32
anim_CHG = 24
anim_N = anim_CWD * anim_CHG
anim_P = 6
anim_CX = 6
anim_CY = 26
anim_PAL = ((255, 255, 255), (0, 0, 0), (128, 128, 128), (200, 200, 200), (220, 40, 40), (245, 140, 30), (250, 220, 50), (60, 190, 70), (20, 100, 40), (80, 200, 230), (40, 80, 200), (20, 30, 90), (150, 60, 190), (245, 140, 190), (130, 80, 40), (245, 200, 160))
anim_INK = (20, 20, 20)
anim_HI = (200, 120, 0)
anim_MAXB = 60000
anim_KEYGAP = 15
def anim_enc_key(fr):
    out = bytearray([1])
    i = 0
    while i < anim_N:
        c = fr[i]
        n = 1
        while i + n < anim_N and fr[i + n] == c and (n < 255):
            n += 1
        out.append(n)
        out.append(c)
        i += n
    return bytes(out)
def anim_enc_delta(prev, fr):
    out = bytearray([0])
    pos = 0
    i = 0
    while i < anim_N:
        if fr[i] == prev[i]:
            i += 1
            continue
        j = i
        last = i
        while j < anim_N and j - i < 254:
            if fr[j] != prev[j]:
                j += 1
                last = j
            elif j + 1 < anim_N and fr[j + 1] != prev[j + 1]:
                j += 1
            else:
                break
        j = last
        skip = i - pos
        while skip > 255:
            out.append(255)
            out.append(0)
            skip -= 255
        out.append(skip)
        out.append(j - i)
        t = i
        while t < j:
            hi = fr[t]
            lo = fr[t + 1] if t + 1 < j else 0
            out.append(hi * 16 + lo)
            t += 2
        pos = j
        i = j
    return bytes(out)
def anim_apply(fr, d):
    if d[0] == 1:
        p = 1
        i = 0
        while p < len(d):
            n = d[p]
            c = d[p + 1]
            for t in range(n):
                fr[i + t] = c
            i += n
            p += 2
        return
    p = 1
    pos = 0
    L = len(d)
    while p < L:
        pos += d[p]
        n = d[p + 1]
        p += 2
        for t in range(n):
            b = d[p + t // 2]
            fr[pos + t] = b >> 4 if t % 2 == 0 else b & 15
        p += (n + 1) // 2
        pos += n
class anim_Studio:
    pass
def anim_dec(s, i):
    k = i
    while k > 0 and s.F[k][0] != 1:
        k -= 1
    fr = bytearray(anim_N)
    for j in range(k, i + 1):
        anim_apply(fr, s.F[j])
    return fr
def anim_chain(s, i):
    n = 0
    k = i
    while k > 0 and s.F[k][0] != 1:
        k -= 1
        n += 1
    return n
def anim_encode_at(s, i, fr, prev):
    if prev is None:
        return anim_enc_key(fr)
    d = anim_enc_delta(prev, fr)
    if i > 0 and anim_chain(s, i - 1) + 1 >= anim_KEYGAP:
        return anim_enc_key(fr)
    return d
def anim_commit(s):
    if not s.dirty:
        return
    i = s.ci
    nx = None
    if i + 1 < len(s.F) and s.F[i + 1][0] == 0:
        nx = anim_dec(s, i + 1)
    s.F[i] = anim_encode_at(s, i, s.cur, s.prv if i > 0 else None)
    if nx is not None:
        s.F[i + 1] = anim_enc_delta(s.cur, nx)
    s.dirty = False
def anim_used(s):
    t = 0
    for f in s.F:
        t += len(f) + 2
    return t
def anim_want(s, i):
    v = s.cur[i]
    if v == 0 and s.onion and (s.ci > 0) and s.prv[i]:
        return 16 + s.prv[i]
    return v
def anim_paint(s, i, v):
    x = anim_CX + i % anim_CWD * anim_P
    y = anim_CY + i // anim_CWD * anim_P
    if v >= 16:
        c = anim_PAL[v - 16]
        rect(x, y, anim_P, anim_P, anim_PAL[0])
        rect(x + 1, y + 1, anim_P - 2, anim_P - 2, ((c[0] + 510) // 3, (c[1] + 510) // 3, (c[2] + 510) // 3))
    else:
        rect(x, y, anim_P, anim_P, anim_PAL[v])
    s.shown[i] = v
def anim_refresh(s):
    for i in range(anim_N):
        v = anim_want(s, i)
        if s.shown[i] != v:
            anim_paint(s, i, v)
def anim_cursor(s):
    x = anim_CX + s.cx * anim_P
    y = anim_CY + s.cy * anim_P
    v = s.cur[s.cy * anim_CWD + s.cx]
    col(BLACK if v in (0, 3, 6, 15) else WHITE)
    draw_rect(x + 1, y + 1, anim_P - 3, anim_P - 3)
def anim_uncursor(s):
    i = s.cy * anim_CWD + s.cx
    anim_paint(s, i, anim_want(s, i))
def anim_palette(s, sel=-1):
    for c in range(16):
        x = 210 + c % 4 * 26
        y = 30 + c // 4 * 26
        rect(x - 2, y - 2, 26, 26, WHITE)
        if c == s.col:
            rbox(x - 2, y - 2, 26, 26, 5, GOLD, 2, WHITE)
        if c == sel:
            rbox(x - 2, y - 2, 26, 26, 5, anim_INK, 2, WHITE)
        rect(x + 1, y + 1, 20, 20, anim_PAL[c])
        if c == 0:
            col(GREY)
            draw_rect(x + 1, y + 1, 19, 19)
def anim_topbar(s):
    rect(0, 0, 320, 22, WHITE)
    text(4, 17, 'Frame ' + str(s.ci + 1) + '/' + str(len(s.F)), anim_INK)
    text(160, 17, str(s.fps) + 'fps', GREY)
    pct = anim_used(s) * 100 // anim_MAXB
    text(236, 17, 'Mem ' + str(pct) + '%', RED if pct > 90 else GREY)
def anim_botbar(s):
    rect(0, 176, 320, 34, WHITE)
    m = ('Pen up', 'PEN DOWN', 'ERASER')[s.pen]
    text(6, 190, m, anim_HI if s.pen else anim_INK)
    text(6, 205, 'ENTER pen DEL eraser 2nd menu', GREY)
def anim_full(s):
    cls(WHITE)
    rect(anim_CX - 2, anim_CY - 2, anim_CWD * anim_P + 4, anim_CHG * anim_P + 4, DARK)
    s.shown = bytearray([255] * anim_N)
    anim_refresh(s)
    anim_palette(s)
    anim_topbar(s)
    anim_botbar(s)
    rect(208, 136, 104, 36, WHITE)
    text(210, 150, 'Onion ' + ('on' if s.onion else 'off'), GREY)
    text(210, 168, 'Saved ' + (str(s.slot) if s.slot else '-'), GREY)
    anim_cursor(s)
def anim_set_px(s, i, c):
    if s.cur[i] != c:
        if not s.dirty:
            s.undo = bytearray(s.cur)
        s.cur[i] = c
        s.dirty = True
        s.changed = True
def anim_fill(s):
    i0 = s.cy * anim_CWD + s.cx
    old = s.cur[i0]
    new = s.col
    if old == new:
        return
    s.undo = bytearray(s.cur)
    stack = [i0]
    while stack:
        i = stack.pop()
        if s.cur[i] != old:
            continue
        s.cur[i] = new
        x = i % anim_CWD
        if x > 0:
            stack.append(i - 1)
        if x < anim_CWD - 1:
            stack.append(i + 1)
        if i >= anim_CWD:
            stack.append(i - anim_CWD)
        if i < anim_N - anim_CWD:
            stack.append(i + anim_CWD)
    s.dirty = True
    s.changed = True
def anim_go(s, j):
    anim_commit(s)
    if j == s.ci + 1:
        s.prv = s.cur
        s.cur = bytearray(s.prv)
        anim_apply(s.cur, s.F[j])
    else:
        s.cur = anim_dec(s, j)
        s.prv = anim_dec(s, j - 1) if j > 0 else bytearray(anim_N)
    s.ci = j
    s.undo = None
def anim_add_frame(s, blank):
    if anim_used(s) > anim_MAXB:
        message(['Memory is full.', 'Save, or delete frames.'], "Can't add")
        return
    anim_commit(s)
    i = s.ci
    nx = anim_dec(s, i + 1) if i + 1 < len(s.F) else None
    new = bytearray(anim_N) if blank else bytearray(s.cur)
    s.F.insert(i + 1, anim_enc_delta(s.cur, new))
    if nx is not None and s.F[i + 2][0] == 0:
        s.F[i + 2] = anim_enc_delta(new, nx)
    s.prv = s.cur
    s.cur = new
    s.ci = i + 1
    s.changed = True
def anim_del_frame(s):
    if len(s.F) == 1:
        s.undo = bytearray(s.cur)
        s.cur = bytearray(anim_N)
        s.dirty = True
        return
    i = s.ci
    nx = anim_dec(s, i + 1) if i + 1 < len(s.F) else None
    p = anim_dec(s, i - 1) if i > 0 else None
    del s.F[i]
    if nx is not None:
        s.F[i] = anim_enc_key(nx) if p is None else anim_enc_delta(p, nx)
    if i >= len(s.F):
        i = len(s.F) - 1
    s.dirty = False
    s.ci = i
    s.cur = anim_dec(s, i)
    s.prv = anim_dec(s, i - 1) if i > 0 else bytearray(anim_N)
    s.changed = True
def anim_play(s):
    anim_commit(s)
    onion = s.onion
    s.onion = False
    rect(0, 176, 320, 34, WHITE)
    text(6, 190, 'Playing. Up/Down: speed', anim_HI)
    text(6, 205, 'Any other key stops', GREY)
    i = 0
    fr = bytearray(anim_N)
    while True:
        if s.F[i][0] == 1 or i == 0:
            fr = bytearray(anim_N)
        anim_apply(fr, s.F[i])
        for p in range(anim_N):
            if s.shown[p] != fr[p]:
                anim_paint(s, p, fr[p])
        rect(0, 0, 150, 22, WHITE)
        text(4, 17, 'Frame ' + str(i + 1) + '/' + str(len(s.F)), anim_INK)
        t = 0
        steps = max(1, 12 // s.fps)
        stop = False
        for q in range(steps):
            k = key()
            if k == UP and s.fps < 12:
                s.fps += 1
                anim_topbar(s)
            elif k == DOWN and s.fps > 1:
                s.fps -= 1
                anim_topbar(s)
            elif k and k not in (UP, DOWN):
                stop = True
                break
            pause(1 / 12)
        if stop:
            break
        i = (i + 1) % len(s.F)
    while key():
        pass
    s.onion = onion
    s.cur = anim_dec(s, s.ci)
    anim_full(s)
anim_ITEMS = ('Color', 'Fill area', 'Undo', 'Clear frame', 'Next frame', 'Prev frame', 'Add copy', 'Add blank', 'Delete frame', 'Play', 'Speed', 'Onion skin', 'Save', 'Load', 'New', 'Quit')
def anim_menu(sel):
    cls()
    ctext(18, 'STUDIO MENU', GOLD)
    while True:
        for i in range(16):
            x = 8 + i // 8 * 156
            y = 26 + i % 8 * 23
            c = GOLD if i == sel else WHITE
            rect(x, y, 150, 21, BLACK)
            rbox(x, y, 148, 21, 8, c)
            text(x + 74 - len(anim_ITEMS[i]) * 5, y + 16, anim_ITEMS[i], c)
        k = wkey()
        if k == UP:
            sel = (sel - 1) % 16
        elif k == DOWN:
            sel = (sel + 1) % 16
        elif k in (LEFT, RIGHT):
            sel = (sel + 8) % 16
        elif k == OK:
            return sel
        elif k in (CLR, SECOND):
            return -1
def anim_pick_color(s):
    sel = s.col
    while True:
        anim_palette(s, sel)
        k = wkey()
        if k == LEFT:
            sel = (sel - 1) % 16
        elif k == RIGHT:
            sel = (sel + 1) % 16
        elif k == UP:
            sel = (sel - 4) % 16
        elif k == DOWN:
            sel = (sel + 4) % 16
        elif k == OK:
            s.col = sel
            break
        elif k == CLR:
            break
    anim_palette(s)
def anim_pick_speed(s):
    cls()
    while True:
        rect(0, 60, 320, 80, BLACK)
        ctext(80, 'PLAYBACK SPEED', GOLD)
        ctext(110, '< ' + str(s.fps) + ' frames a second >')
        ctext(140, 'ENTER done', GREY)
        k = wkey()
        if k == LEFT and s.fps > 1:
            s.fps -= 1
        elif k == RIGHT and s.fps < 12:
            s.fps += 1
        elif k in (OK, CLR):
            return
def anim_pick_slot(title):
    opts = []
    for sl in range(1, save_SLOTS + 1):
        inf = save_info(sl)
        opts.append('Slot ' + str(sl) + (': ' + str(inf[0]) + ' fr' if inf else ': empty'))
    opts.append('Cancel')
    c = choose(title, opts)
    if c < 0 or c == save_SLOTS:
        return 0
    return c + 1
def anim_progress(k, n):
    rect(60, 120, 200, 30, BLACK)
    rbox(60, 120, 200, 16, 6, WHITE)
    rect(64, 124, max(2, 192 * (k + 1) // n), 8, GOLD)
def anim_do_save(s):
    anim_commit(s)
    sl = anim_pick_slot('SAVE TO')
    if not sl:
        return
    cls()
    ctext(100, 'Saving...', GOLD)
    data = bytearray()
    for f in s.F:
        data.append(len(f) // 256)
        data.append(len(f) % 256)
        data.extend(f)
    try:
        save_save(sl, data, len(s.F), s.fps, anim_progress)
        s.slot = sl
        s.changed = False
        message([str(len(s.F)) + ' frames saved', 'to slot ' + str(sl) + '.'], 'Saved')
    except Exception as e:
        message(['Could not save:', str(e)[:24]], 'Error')
def anim_do_load(s):
    sl = anim_pick_slot('LOAD FROM')
    if not sl or not save_info(sl):
        return
    if s.changed and message(['Unsaved changes will', 'be lost. ENTER: load', 'CLEAR: cancel'], 'Load?') != OK:
        return
    cls()
    ctext(100, 'Loading...', GOLD)
    try:
        data, frames, fps = save_load(sl, anim_progress)
    except Exception as e:
        message(['Could not load:', str(e)[:24]], 'Error')
        return
    F = []
    p = 0
    for k in range(frames):
        n = data[p] * 256 + data[p + 1]
        F.append(bytes(data[p + 2:p + 2 + n]))
        p += 2 + n
    anim_reset(s, F, fps)
    s.slot = sl
def anim_reset(s, F, fps):
    s.F = F
    s.fps = fps
    s.ci = 0
    s.cur = anim_dec(s, 0)
    s.prv = bytearray(anim_N)
    s.dirty = False
    s.changed = False
    s.undo = None
    s.slot = 0
def anim_studio():
    s = anim_Studio()
    anim_reset(s, [anim_enc_key(bytearray(anim_N))], 6)
    s.cx = 16
    s.cy = 12
    s.col = 1
    s.pen = 0
    s.onion = True
    s.shown = bytearray([255] * anim_N)
    msel = 0
    anim_full(s)
    held = 0
    hc = 0
    while True:
        k = key()
        if k == held and k:
            hc += 1
        else:
            hc = 0
        rep = k != held or (hc > 3 and hc % 1 == 0)
        held = k
        if not k:
            pause(0.01)
            continue
        if k in (LEFT, RIGHT, UP, DOWN) and rep:
            anim_uncursor(s)
            if k == LEFT and s.cx > 0:
                s.cx -= 1
            elif k == RIGHT and s.cx < anim_CWD - 1:
                s.cx += 1
            elif k == UP and s.cy > 0:
                s.cy -= 1
            elif k == DOWN and s.cy < anim_CHG - 1:
                s.cy += 1
            if s.pen:
                i = s.cy * anim_CWD + s.cx
                anim_set_px(s, i, s.col if s.pen == 1 else 0)
                anim_paint(s, i, anim_want(s, i))
            anim_cursor(s)
            continue
        if not rep:
            continue
        if k == OK or k == DEL:
            want_pen = 1 if k == OK else 2
            s.pen = 0 if s.pen == want_pen else want_pen
            if s.pen:
                i = s.cy * anim_CWD + s.cx
                anim_set_px(s, i, s.col if s.pen == 1 else 0)
                anim_paint(s, i, anim_want(s, i))
                anim_cursor(s)
            anim_botbar(s)
            anim_topbar(s)
            continue
        if k == CLR and s.pen:
            s.pen = 0
            anim_botbar(s)
            continue
        if k == SECOND or k == CLR:
            c = anim_menu(msel)
            if c >= 0:
                msel = c
            s.pen = 0
            if c == 0:
                anim_full(s)
                anim_pick_color(s)
            elif c == 1:
                anim_fill(s)
            elif c == 2 and s.undo is not None:
                u = s.undo
                s.undo = bytearray(s.cur)
                s.cur = u
                s.dirty = True
            elif c == 3:
                s.undo = bytearray(s.cur)
                s.cur = bytearray(anim_N)
                s.dirty = True
            elif c == 4:
                if s.ci + 1 < len(s.F):
                    anim_go(s, s.ci + 1)
                else:
                    anim_add_frame(s, False)
            elif c == 5 and s.ci > 0:
                anim_go(s, s.ci - 1)
            elif c == 6:
                anim_add_frame(s, False)
            elif c == 7:
                anim_add_frame(s, True)
            elif c == 8:
                anim_del_frame(s)
            elif c == 9:
                anim_full(s)
                anim_play(s)
            elif c == 10:
                anim_pick_speed(s)
            elif c == 11:
                s.onion = not s.onion
            elif c == 12:
                anim_do_save(s)
            elif c == 13:
                anim_do_load(s)
            elif c == 14:
                if not s.changed or message(['Unsaved changes will', 'be lost. ENTER: new', 'CLEAR: cancel'], 'New?') == OK:
                    anim_reset(s, [anim_enc_key(bytearray(anim_N))], 6)
            elif c == 15:
                if not s.changed or message(['Unsaved changes will', 'be lost. ENTER: quit', 'CLEAR: cancel'], 'Quit?') == OK:
                    return
            if c != 0:
                anim_full(s)
anim_RULES = 'Draw a picture, add frames, and play them back. Saves stay on the calculator.'
anim_KEYS = ['Arrows: move  ENTER: pen', 'DEL: eraser  2nd: menu', 'Menu: colors, frames, play,', 'speed, save and load']
def anim_main():
    while True:
        c = home('GHANIM', 'ANIMATION STUDIO', anim_RULES, anim_KEYS, ('Play', 'Back'))
        if c < 0:
            return
        anim_studio()
anim_main()
