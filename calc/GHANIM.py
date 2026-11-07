# Animation Studio: draw frame by frame and play it back.
# Arrows move. ENTER = pen on/off. DEL = eraser on/off. 2nd = menu.
# Saves go to calculator lists (see GHSAVE), so they stay if GAMEHUB is deleted.
from GHLIB import *
import GHSAVE

CWD = 32
CHG = 24
N = CWD * CHG
P = 6
CX = 6
CY = 26
PAL = ((0, 0, 0), (255, 255, 255), (128, 128, 128), (200, 200, 200),
       (220, 40, 40), (245, 140, 30), (250, 220, 50), (60, 190, 70),
       (20, 100, 40), (80, 200, 230), (40, 80, 200), (20, 30, 90),
       (150, 60, 190), (245, 140, 190), (130, 80, 40), (245, 200, 160))
MAXB = 60000
KEYGAP = 15


# ---------- frame encoding ----------
def enc_key(fr):
    out = bytearray([1])
    i = 0
    while i < N:
        c = fr[i]
        n = 1
        while i + n < N and fr[i + n] == c and n < 255:
            n += 1
        out.append(n)
        out.append(c)
        i += n
    return bytes(out)


def enc_delta(prev, fr):
    out = bytearray([0])
    pos = 0
    i = 0
    while i < N:
        if fr[i] == prev[i]:
            i += 1
            continue
        j = i
        last = i
        while j < N and j - i < 254:
            if fr[j] != prev[j]:
                j += 1
                last = j
            elif j + 1 < N and fr[j + 1] != prev[j + 1]:
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


def apply(fr, d):
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
            fr[pos + t] = (b >> 4) if t % 2 == 0 else (b & 15)
        p += (n + 1) // 2
        pos += n


class Studio:
    pass


def dec(s, i):
    k = i
    while k > 0 and s.F[k][0] != 1:
        k -= 1
    fr = bytearray(N)
    for j in range(k, i + 1):
        apply(fr, s.F[j])
    return fr


def chain(s, i):
    n = 0
    k = i
    while k > 0 and s.F[k][0] != 1:
        k -= 1
        n += 1
    return n


def encode_at(s, i, fr, prev):
    if prev is None:
        return enc_key(fr)
    d = enc_delta(prev, fr)
    if i > 0 and chain(s, i - 1) + 1 >= KEYGAP:
        return enc_key(fr)
    return d


def commit(s):
    if not s.dirty:
        return
    i = s.ci
    nx = None
    if i + 1 < len(s.F) and s.F[i + 1][0] == 0:
        nx = dec(s, i + 1)
    s.F[i] = encode_at(s, i, s.cur, s.prv if i > 0 else None)
    if nx is not None:
        s.F[i + 1] = enc_delta(s.cur, nx)
    s.dirty = False


def used(s):
    t = 0
    for f in s.F:
        t += len(f) + 2
    return t


# ---------- drawing ----------
def want(s, i):
    v = s.cur[i]
    if v == 0 and s.onion and s.ci > 0 and s.prv[i]:
        return 16 + s.prv[i]
    return v


def paint(s, i, v):
    x = CX + (i % CWD) * P
    y = CY + (i // CWD) * P
    if v >= 16:
        c = PAL[v - 16]
        rect(x, y, P, P, BLACK)
        rect(x + 2, y + 2, P - 4, P - 4, (c[0] // 2, c[1] // 2, c[2] // 2))
    else:
        rect(x, y, P, P, PAL[v])
    s.shown[i] = v


def refresh(s):
    for i in range(N):
        v = want(s, i)
        if s.shown[i] != v:
            paint(s, i, v)


def cursor(s):
    x = CX + s.cx * P
    y = CY + s.cy * P
    v = s.cur[s.cy * CWD + s.cx]
    col(BLACK if v in (1, 3, 6, 15) else WHITE)
    draw_rect(x + 1, y + 1, P - 3, P - 3)


def uncursor(s):
    i = s.cy * CWD + s.cx
    paint(s, i, want(s, i))


def palette(s, sel=-1):
    for c in range(16):
        x = 210 + (c % 4) * 26
        y = 30 + (c // 4) * 26
        rect(x - 2, y - 2, 26, 26, BLACK)
        if c == s.col:
            rbox(x - 2, y - 2, 26, 26, 5, GOLD)
        if c == sel:
            rbox(x - 2, y - 2, 26, 26, 5, WHITE)
        rect(x + 1, y + 1, 20, 20, PAL[c])
        if c == 0:
            col(GREY)
            draw_rect(x + 1, y + 1, 19, 19)


def topbar(s):
    rect(0, 0, 320, 22, BLACK)
    text(4, 17, "Frame " + str(s.ci + 1) + "/" + str(len(s.F)))
    text(160, 17, str(s.fps) + "fps", GREY)
    pct = used(s) * 100 // MAXB
    text(236, 17, "Mem " + str(pct) + "%", RED if pct > 90 else GREY)


def botbar(s):
    rect(0, 176, 320, 34, BLACK)
    m = ("Pen up", "PEN DOWN", "ERASER")[s.pen]
    text(6, 190, m, GOLD if s.pen else WHITE)
    text(6, 205, "ENTER pen DEL eraser 2nd menu", GREY)


def full(s):
    cls()
    rect(CX - 2, CY - 2, CWD * P + 4, CHG * P + 4, DARK)
    s.shown = bytearray([255] * N)
    refresh(s)
    palette(s)
    topbar(s)
    botbar(s)
    rect(208, 136, 104, 36, BLACK)
    text(210, 150, "Onion " + ("on" if s.onion else "off"), GREY)
    text(210, 168, "Saved " + (str(s.slot) if s.slot else "-"), GREY)
    cursor(s)


# ---------- editing ----------
def set_px(s, i, c):
    if s.cur[i] != c:
        if not s.dirty:
            s.undo = bytearray(s.cur)
        s.cur[i] = c
        s.dirty = True
        s.changed = True


def fill(s):
    i0 = s.cy * CWD + s.cx
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
        x = i % CWD
        if x > 0:
            stack.append(i - 1)
        if x < CWD - 1:
            stack.append(i + 1)
        if i >= CWD:
            stack.append(i - CWD)
        if i < N - CWD:
            stack.append(i + CWD)
    s.dirty = True
    s.changed = True


def go(s, j):
    commit(s)
    if j == s.ci + 1:
        s.prv = s.cur
        s.cur = bytearray(s.prv)
        apply(s.cur, s.F[j])
    else:
        s.cur = dec(s, j)
        s.prv = dec(s, j - 1) if j > 0 else bytearray(N)
    s.ci = j
    s.undo = None


def add_frame(s, blank):
    if used(s) > MAXB:
        message(["Memory is full.", "Save, or delete frames."], "Can't add")
        return
    commit(s)
    i = s.ci
    nx = dec(s, i + 1) if i + 1 < len(s.F) else None
    new = bytearray(N) if blank else bytearray(s.cur)
    s.F.insert(i + 1, enc_delta(s.cur, new))
    if nx is not None and s.F[i + 2][0] == 0:
        s.F[i + 2] = enc_delta(new, nx)
    s.prv = s.cur
    s.cur = new
    s.ci = i + 1
    s.changed = True


def del_frame(s):
    if len(s.F) == 1:
        s.undo = bytearray(s.cur)
        s.cur = bytearray(N)
        s.dirty = True
        return
    i = s.ci
    nx = dec(s, i + 1) if i + 1 < len(s.F) else None
    p = dec(s, i - 1) if i > 0 else None
    del s.F[i]
    if nx is not None:
        s.F[i] = enc_key(nx) if p is None else enc_delta(p, nx)
    if i >= len(s.F):
        i = len(s.F) - 1
    s.dirty = False
    s.ci = i
    s.cur = dec(s, i)
    s.prv = dec(s, i - 1) if i > 0 else bytearray(N)
    s.changed = True


# ---------- play ----------
def play(s):
    commit(s)
    onion = s.onion
    s.onion = False
    rect(0, 176, 320, 34, BLACK)
    text(6, 190, "Playing. Up/Down: speed", GOLD)
    text(6, 205, "Any other key stops", GREY)
    i = 0
    fr = bytearray(N)
    while True:
        if s.F[i][0] == 1 or i == 0:
            fr = bytearray(N)
        apply(fr, s.F[i])
        for p in range(N):
            if s.shown[p] != fr[p]:
                paint(s, p, fr[p])
        rect(0, 0, 150, 22, BLACK)
        text(4, 17, "Frame " + str(i + 1) + "/" + str(len(s.F)))
        t = 0
        steps = max(1, 12 // s.fps)
        stop = False
        for q in range(steps):
            k = key()
            if k == UP and s.fps < 12:
                s.fps += 1
                topbar(s)
            elif k == DOWN and s.fps > 1:
                s.fps -= 1
                topbar(s)
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
    s.cur = dec(s, s.ci)
    full(s)


# ---------- menus ----------
ITEMS = ("Color", "Fill area", "Undo", "Clear frame",
         "Next frame", "Prev frame", "Add copy", "Add blank",
         "Delete frame", "Play", "Speed", "Onion skin",
         "Save", "Load", "New", "Quit")


def menu(sel):
    cls()
    ctext(18, "STUDIO MENU", GOLD)
    while True:
        for i in range(16):
            x = 8 + (i // 8) * 156
            y = 26 + (i % 8) * 23
            c = GOLD if i == sel else WHITE
            rect(x, y, 150, 21, BLACK)
            rbox(x, y, 148, 21, 8, c)
            text(x + 74 - len(ITEMS[i]) * 5, y + 16, ITEMS[i], c)
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


def pick_color(s):
    sel = s.col
    while True:
        palette(s, sel)
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
    palette(s)


def pick_speed(s):
    cls()
    while True:
        rect(0, 60, 320, 80, BLACK)
        ctext(80, "PLAYBACK SPEED", GOLD)
        ctext(110, "< " + str(s.fps) + " frames a second >")
        ctext(140, "ENTER done", GREY)
        k = wkey()
        if k == LEFT and s.fps > 1:
            s.fps -= 1
        elif k == RIGHT and s.fps < 12:
            s.fps += 1
        elif k in (OK, CLR):
            return


def pick_slot(title):
    opts = []
    for sl in range(1, GHSAVE.SLOTS + 1):
        inf = GHSAVE.info(sl)
        opts.append("Slot " + str(sl) + (": " + str(inf[0]) + " fr" if inf else ": empty"))
    opts.append("Cancel")
    c = choose(title, opts)
    if c < 0 or c == GHSAVE.SLOTS:
        return 0
    return c + 1


def progress(k, n):
    rect(60, 120, 200, 30, BLACK)
    rbox(60, 120, 200, 16, 6, WHITE)
    rect(64, 124, max(2, 192 * (k + 1) // n), 8, GOLD)


def do_save(s):
    commit(s)
    sl = pick_slot("SAVE TO")
    if not sl:
        return
    cls()
    ctext(100, "Saving...", GOLD)
    data = bytearray()
    for f in s.F:
        data.append(len(f) // 256)
        data.append(len(f) % 256)
        data.extend(f)
    try:
        GHSAVE.save(sl, data, len(s.F), s.fps, progress)
        s.slot = sl
        s.changed = False
        message([str(len(s.F)) + " frames saved", "to slot " + str(sl) + "."], "Saved")
    except Exception as e:
        message(["Could not save:", str(e)[:24]], "Error")


def do_load(s):
    sl = pick_slot("LOAD FROM")
    if not sl or not GHSAVE.info(sl):
        return
    if s.changed and message(["Unsaved changes will", "be lost. ENTER: load", "CLEAR: cancel"], "Load?") != OK:
        return
    cls()
    ctext(100, "Loading...", GOLD)
    try:
        data, frames, fps = GHSAVE.load(sl, progress)
    except Exception as e:
        message(["Could not load:", str(e)[:24]], "Error")
        return
    F = []
    p = 0
    for k in range(frames):
        n = data[p] * 256 + data[p + 1]
        F.append(bytes(data[p + 2:p + 2 + n]))
        p += 2 + n
    reset(s, F, fps)
    s.slot = sl


def reset(s, F, fps):
    s.F = F
    s.fps = fps
    s.ci = 0
    s.cur = dec(s, 0)
    s.prv = bytearray(N)
    s.dirty = False
    s.changed = False
    s.undo = None
    s.slot = 0


def studio():
    s = Studio()
    reset(s, [enc_key(bytearray(N))], 6)
    s.cx = 16
    s.cy = 12
    s.col = 1
    s.pen = 0
    s.onion = True
    s.shown = bytearray([255] * N)
    msel = 0
    full(s)
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
            uncursor(s)
            if k == LEFT and s.cx > 0:
                s.cx -= 1
            elif k == RIGHT and s.cx < CWD - 1:
                s.cx += 1
            elif k == UP and s.cy > 0:
                s.cy -= 1
            elif k == DOWN and s.cy < CHG - 1:
                s.cy += 1
            if s.pen:
                i = s.cy * CWD + s.cx
                set_px(s, i, s.col if s.pen == 1 else 0)
                paint(s, i, want(s, i))
            cursor(s)
            continue
        if not rep:
            continue
        if k == OK or k == DEL:
            want_pen = 1 if k == OK else 2
            s.pen = 0 if s.pen == want_pen else want_pen
            if s.pen:
                i = s.cy * CWD + s.cx
                set_px(s, i, s.col if s.pen == 1 else 0)
                paint(s, i, want(s, i))
                cursor(s)
            botbar(s)
            topbar(s)
            continue
        if k == CLR and s.pen:
            s.pen = 0
            botbar(s)
            continue
        if k == SECOND or k == CLR:
            c = menu(msel)
            if c >= 0:
                msel = c
            s.pen = 0
            if c == 0:
                full(s)
                pick_color(s)
            elif c == 1:
                fill(s)
            elif c == 2 and s.undo is not None:
                u = s.undo
                s.undo = bytearray(s.cur)
                s.cur = u
                s.dirty = True
            elif c == 3:
                s.undo = bytearray(s.cur)
                s.cur = bytearray(N)
                s.dirty = True
            elif c == 4:
                if s.ci + 1 < len(s.F):
                    go(s, s.ci + 1)
                else:
                    add_frame(s, False)
            elif c == 5 and s.ci > 0:
                go(s, s.ci - 1)
            elif c == 6:
                add_frame(s, False)
            elif c == 7:
                add_frame(s, True)
            elif c == 8:
                del_frame(s)
            elif c == 9:
                full(s)
                play(s)
            elif c == 10:
                pick_speed(s)
            elif c == 11:
                s.onion = not s.onion
            elif c == 12:
                do_save(s)
            elif c == 13:
                do_load(s)
            elif c == 14:
                if not s.changed or message(["Unsaved changes will", "be lost. ENTER: new", "CLEAR: cancel"], "New?") == OK:
                    reset(s, [enc_key(bytearray(N))], 6)
            elif c == 15:
                if not s.changed or message(["Unsaved changes will", "be lost. ENTER: quit", "CLEAR: cancel"], "Quit?") == OK:
                    return
            if c != 0:
                full(s)

RULES = 'Draw a picture, add frames, and play them back. Saves stay on the calculator.'
KEYS = ['Arrows: move  ENTER: pen', 'DEL: eraser  2nd: menu', 'Menu: colors, frames, play,', 'speed, save and load']


def main():
    while True:
        c = home("GHANIM", 'ANIMATION STUDIO', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        studio()
