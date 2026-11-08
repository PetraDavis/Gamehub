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
PAL = ((255, 255, 255), (0, 0, 0), (128, 128, 128), (200, 200, 200),
       (220, 40, 40), (245, 140, 30), (250, 220, 50), (60, 190, 70),
       (20, 100, 40), (80, 200, 230), (40, 80, 200), (20, 30, 90),
       (150, 60, 190), (245, 140, 190), (130, 80, 40), (245, 200, 160))
# the onion skin: each colour mixed with 4 parts white, a faint afterimage
COL = PAL + tuple(((r + 1020) // 5, (g + 1020) // 5, (b + 1020) // 5) for r, g, b in PAL)
INK = (20, 20, 20)
HI = (200, 120, 0)
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
# Nothing is cleared and drawn again: s.shown keeps what each canvas cell
# shows now, and only cells that differ are painted, joined into rows of one
# colour. Words are updated letter by letter. So the screen never flashes.
def want(s, i):
    v = s.cur[i]
    if v == 0 and s.onion and s.ci > 0 and s.prv[i]:
        return 16 + s.prv[i]
    return v


def paint(s, i, v):
    x = CX + (i % CWD) * P
    y = CY + (i // CWD) * P
    rect(x, y, P, P, COL[v])
    s.shown[i] = v


def refresh(s, src=None):
    # paint the cells that differ from s.shown; src is a frame (for playback),
    # or None for the frame being edited with its onion skin.
    # Every drawing call is slow on the calculator, so changed cells are joined
    # into rectangles as big as possible. A rectangle may also cover cells that
    # already show its colour (painting them again changes nothing), and all
    # rectangles of one colour are drawn together.
    t = src if src is not None else bytearray([want(s, i) for i in range(N)])
    sh = s.shown
    hb = s.hide if s.hide >= 0 and sh[s.hide] == t[s.hide] else -1
    todo = {}
    for i in range(N):
        v = t[i]
        if sh[i] == v:
            continue
        r = i // CWD
        c = i - r * CWD
        # the run of cells to the right that end up colour v
        e = 1
        while c + e < CWD and t[i + e] == v and i + e != hb:
            e += 1
        # or only up to the last of them that still needs painting
        n = e
        while n > 1 and sh[i + n - 1] == v:
            n -= 1
        best = None
        for w in ((e, n) if n < e else (e,)):
            h = 1
            while r + h < CHG:
                j = i + h * CWD
                k = 0
                while k < w and t[j + k] == v and j + k != hb:
                    k += 1
                if k < w:
                    break
                h += 1
            g = 0
            for q in range(h):
                j = i + q * CWD
                for k in range(w):
                    if sh[j + k] != v:
                        g += 1
            if best is None or g > best[0]:
                best = (g, w, h)
        g, w, h = best
        for q in range(h):
            j = i + q * CWD
            for k in range(w):
                sh[j + k] = v
        if v in todo:
            todo[v].append((c, r, w, h))
        else:
            todo[v] = [(c, r, w, h)]
    for v in todo:
        for c, r, w, h in todo[v]:
            rect(CX + c * P, CY + r * P, w * P, h * P, COL[v])


def cursor(s):
    x = CX + s.cx * P
    y = CY + s.cy * P
    v = s.cur[s.cy * CWD + s.cx]
    col(BLACK if v in (0, 3, 6, 15) else WHITE)
    draw_rect(x, y, P - 2, P - 2)
    s.hide = s.cy * CWD + s.cx


def uncursor(s):
    # painting the cell again in its own colour only removes the outline
    i = s.cy * CWD + s.cx
    s.hide = -1
    paint(s, i, want(s, i))


def label(s, key, x, y, t, c, bg=WHITE):
    # write t at x, y; if something was written there before, change only
    # the letters that differ. Neighbouring changed letters are erased with
    # one rectangle and written with one text call, because each call is slow.
    old = s.lab.get(key)
    s.lab[key] = (t, c)
    if old is None:
        text(x, y, t, c)
        return
    o, oc = old
    n = max(len(o), len(t))
    o = o + " " * (n - len(o))
    t2 = t + " " * (n - len(t))
    segs = []
    for k in range(n):
        if o[k] != t2[k] or (oc != c and t2[k] != " "):
            if segs and k - segs[-1][1] <= 2:
                segs[-1][1] = k + 1
            else:
                segs.append([k, k + 1])
    rub = [g for g in segs if o[g[0]:g[1]].strip()]
    for a, b in rub:
        rect(x + a * 10, y - 12, (b - a) * 10, 16, bg)
    for a, b in segs:
        w = t2[a:b]
        if w.strip():
            text(x + a * 10, y, w, c)


def swatch(s, c, sel=-1):
    # the outline around colour c: dark while choosing, gold for the pen colour
    x = 210 + (c % 4) * 26
    y = 30 + (c // 4) * 26
    e = INK if c == sel else (GOLD if c == s.col else WHITE)
    rect(x - 2, y - 2, 26, 2, e)
    rect(x - 2, y + 22, 26, 2, e)
    rect(x - 2, y, 2, 22, e)
    rect(x + 22, y, 2, 22, e)


def palette(s):
    for c in range(16):
        x = 210 + (c % 4) * 26
        y = 30 + (c // 4) * 26
        rect(x + 1, y + 1, 20, 20, PAL[c])
    # the panel behind is white, so only outlines of another colour are drawn
    col(GREY)
    draw_rect(210, 30, 20, 20)
    swatch(s, s.col)


def topbar(s):
    pct = used(s) * 100 // MAXB
    label(s, "fr", 4, 17, "Frame " + str(s.ci + 1) + "/" + str(len(s.F)), INK)
    label(s, "fps", 160, 17, str(s.fps) + "fps", GREY)
    label(s, "mem", 236, 17, "Mem " + str(pct) + "%", RED if pct > 90 else GREY)


def botbar(s, a=None, b=None):
    if a is None:
        a = ("Pen up", "PEN DOWN", "ERASER")[s.pen]
        ca = HI if s.pen else INK
    else:
        ca = HI
    label(s, "b1", 6, 190, a, ca)
    label(s, "b2", 6, 206, b or "ENTER pen DEL eraser 2nd menu", GREY)


def side(s):
    # the right-hand panel: colours, onion skin and save slot
    rect(MX, 22, 320 - MX, 154, WHITE)
    s.lab.pop("on", None)
    s.lab.pop("sv", None)
    palette(s)
    sidetext(s)


def sidetext(s):
    label(s, "on", 210, 150, "Onion " + ("on" if s.onion else "off"), GREY)
    label(s, "sv", 210, 168, "Saved " + (str(s.slot) if s.slot else "-"), GREY)


def full(s):
    cls(WHITE)
    rect(CX - 2, CY - 2, CWD * P + 4, 2, DARK)
    rect(CX - 2, CY + CHG * P, CWD * P + 4, 2, DARK)
    rect(CX - 2, CY, 2, CHG * P, DARK)
    rect(CX + CWD * P, CY, 2, CHG * P, DARK)
    s.shown = bytearray(N)
    s.hide = -1
    s.lab = {}
    refresh(s)
    side(s)
    topbar(s)
    botbar(s)
    cursor(s)


def update(s):
    # after an edit or a frame change: only what changed is painted
    uncursor(s)
    refresh(s)
    topbar(s)
    sidetext(s)
    botbar(s)
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
        s.broke = True
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
    uncursor(s)
    botbar(s, "Playing. Up/Down: speed", "Any other key stops")
    i = 0
    fr = bytearray(N)
    while True:
        if s.F[i][0] == 1 or i == 0:
            fr = bytearray(N)
        apply(fr, s.F[i])
        refresh(s, fr)
        label(s, "fr", 4, 17, "Frame " + str(i + 1) + "/" + str(len(s.F)), INK)
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
    s.cur = dec(s, s.ci)
    update(s)


# ---------- menus ----------
ITEMS = ("Color", "Fill area", "Undo", "Wipe frame",
         "Next frame", "Prev frame", "Add copy", "Add blank",
         "Del frame", "Play", "Speed", "Onion skin",
         "Save", "Load", "New", "Quit")
MX = 202
MY = 24
MH = 25
MV = 6
MW = 108           # menu box width; the scroll bar sits to its right
SBX = MX + MW + 4  # scroll bar track
SBH = MV * MH - 3
THH = SBH * MV // 16


def thumb_y(top):
    return MY + (SBH - THH) * top // (16 - MV)


def scrollbar(top, old=None):
    # a dark track with a white thumb; when the list scrolls only the strip
    # the thumb left is painted dark again
    if old is None:
        rect(SBX, MY, 5, SBH, DARK)
    elif old == top:
        return
    else:
        a, b = thumb_y(old), thumb_y(top)
        vacate(SBX, a, SBX, b, 5, THH, DARK)
        vacate(SBX, b, SBX, a, 5, THH, WHITE)
        return
    rect(SBX, thumb_y(top), 5, THH, WHITE)


def mbox(x, y, w, h, c):
    # an outline with notched corners: four rectangles, so it can be
    # recoloured without touching the inside
    rect(x + 2, y, w - 4, 2, c)
    rect(x + 2, y + h - 2, w - 4, 2, c)
    rect(x, y + 2, 2, h - 4, c)
    rect(x + w - 2, y + 2, 2, h - 4, c)


def mrows(s, top, sel):
    # bring the 6 visible rows up to date, drawing each colour in one go:
    # first the outlines, then black over words that change, then the words
    boxes = []
    rub = []
    words = []
    for r in range(MV):
        i = top + r
        y = MY + r * MH
        c = GOLD if i == sel else WHITE
        if s.lab.get(("mb", r)) != c:
            boxes.append((c, y))
            s.lab[("mb", r)] = c
        old = s.lab.get(("m", r))
        t = ITEMS[i]
        if old != (t, c):
            if old and old[0] != t:
                rub.append((y, len(old[0])))
            words.append((c, y, t))
            s.lab[("m", r)] = (t, c)
    boxes.sort()
    for c, y in boxes:
        mbox(MX + 1, y, MW, 22, c)
    for y, n in rub:
        rect(MX + 5, y + 4, n * 10, 16, BLACK)
    words.sort()
    for c, y, t in words:
        text(MX + 5, y + 16, t, c)


def menu(s, sel):
    # the menu opens over the colour panel, so the drawing stays on screen
    rect(MX, 22, 320 - MX, 154, BLACK)
    for r in range(MV):
        s.lab.pop(("mb", r), None)
        s.lab.pop(("m", r), None)
    botbar(s, "MENU  Up/Down: pick", "ENTER: do it  2nd: close")
    top = min(max(0, sel - 2), 16 - MV)
    mrows(s, top, sel)
    scrollbar(top)
    while True:
        k = wkey()
        old = sel
        if k == UP:
            sel = (sel - 1) % 16
        elif k == DOWN:
            sel = (sel + 1) % 16
        elif k in (LEFT, RIGHT):
            sel = (sel + 8) % 16
        elif k == OK:
            break
        elif k in (CLR, SECOND):
            sel = -1
            break
        nt = top
        if sel < top:
            nt = sel
        elif sel >= top + MV:
            nt = sel - MV + 1
        scrollbar(nt, top)
        top = nt
        mrows(s, top, sel)
    side(s)
    botbar(s)
    return sel


def pick_color(s):
    sel = s.col
    swatch(s, sel, sel)
    botbar(s, "Arrows: pick a colour", "ENTER: use it  CLEAR: back")
    while True:
        k = wkey()
        old = sel
        if k == LEFT:
            sel = (sel - 1) % 16
        elif k == RIGHT:
            sel = (sel + 1) % 16
        elif k == UP:
            sel = (sel - 4) % 16
        elif k == DOWN:
            sel = (sel + 4) % 16
        elif k == OK:
            old = s.col
            s.col = sel
            swatch(s, old)
            break
        elif k == CLR:
            break
        if sel != old:
            swatch(s, old, sel)
            swatch(s, sel, sel)
    swatch(s, sel)
    swatch(s, s.col)
    botbar(s)


def pick_speed(s):
    cls()
    ctext(80, "PLAYBACK SPEED", GOLD)
    ctext(140, "ENTER done", GREY)
    s.lab = {}
    while True:
        t = "< " + str(s.fps) + " frames a second >"
        label(s, "sp", 160 - len(t) * 5, 110, t, WHITE, BLACK)
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
    s.hide = -1
    s.lab = {}
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
                if s.shown[i] != want(s, i):
                    uncursor(s)
                    cursor(s)
            botbar(s)
            topbar(s)
            continue
        if k == CLR and s.pen:
            s.pen = 0
            botbar(s)
            continue
        if k == SECOND or k == CLR:
            s.pen = 0
            c = menu(s, msel)
            if c >= 0:
                msel = c
            s.broke = False
            if c == 0:
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
                play(s)
            elif c == 10:
                pick_speed(s)
                s.broke = True
            elif c == 11:
                s.onion = not s.onion
            elif c == 12:
                do_save(s)
                s.broke = True
            elif c == 13:
                do_load(s)
                s.broke = True
            elif c == 14:
                if s.changed:
                    s.broke = True
                if not s.changed or message(["Unsaved changes will", "be lost. ENTER: new", "CLEAR: cancel"], "New?") == OK:
                    reset(s, [enc_key(bytearray(N))], 6)
            elif c == 15:
                if not s.changed or message(["Unsaved changes will", "be lost. ENTER: quit", "CLEAR: cancel"], "Quit?") == OK:
                    return
                s.broke = True
            if s.broke:
                full(s)
            elif c != 9:
                update(s)


RULES = 'Draw a picture, add frames, and play them back. Saves stay on the calculator.'
KEYS = ['Arrows: move  ENTER: pen', 'DEL: eraser  2nd: menu', 'Menu: colors, frames, play,', 'speed, save and load']


def forget():
    # "Delete" on the home screen: wipe every saved animation, after asking
    if choose("Delete all saves?", ["No, keep them", "Yes, delete them"]) == 1:
        GHSAVE.wipe(1)
        message(["All your saved", "animations are gone."], "Saves deleted")


def main():
    while True:
        c = home("GHANIM", 'ANIMATION STUDIO', RULES, KEYS, ("Play", "Delete", "Back"), 0, forget)
        if c < 0:
            return
        studio()
