# GAMEHUB - game center for the TI-84 Evo. Run this file.
from GHLIB import *
import sys
import gc

CATS = [
    ("Arcade", [("Wing It", "GHFLAP"), ("Pong", "GHPONG"), ("Breakout", "GHBREAK"), ("Star Patrol", "GHSTAR")]),
    ("Puzzle", [("Stack Drop", "GHBLOCKS"), ("2048", "GHMERGE"), ("Sudoku", "GHSUDOKU"), ("Simon", "GHSIMON")]),
    ("Classics", [("Solitaire", "GHSOLI"), ("Tic-Tac-Toe", "GHTTT"), ("Hangman", "GHHANG"), ("Memory Match", "GHMATCH")]),
    ("Adventure", [("Tiny Quest", "GHRPG"), ("Dragon Tamer", "GHDRAGON"), ("Detective Case", "GHDETECT"), ("Lost Orbit", "GHSPACE")]),
    ("Create", [("Animation Studio", "GHANIM"), ("Fortune Cards", "GHFORTUN"), ("Name Generator", "GHNAMES")]),
    ("Settings", [("Key Test", "*keys"), ("Delete All Saves", "*wipe"), ("About", "*about")]),
]

BAR_Y = 34
BAR_H = 22
BAR_GAP = 27


def header():
    cls()
    ctext(22, "GAMEHUB", WHITE)


def draw_bar(i, on, first=False):
    # after the first time only the outline and words change colour
    y = BAR_Y + i * BAR_GAP
    c = GOLD if on else WHITE
    if first:
        rbox(50, y, 220, BAR_H, 9, c, 2, BLACK, False)
    else:
        edge(50, y, 220, BAR_H, 9, c)
    ctext(y + 17, CATS[i][0], c)


def cat_screen(sel):
    header()
    for i in range(len(CATS)):
        draw_bar(i, i == sel, True)
    while True:
        k = wkey()
        old = sel
        if k == UP:
            sel = (sel - 1) % len(CATS)
        elif k == DOWN:
            sel = (sel + 1) % len(CATS)
        elif k == OK or k == RIGHT:
            return sel
        elif k == CLR:
            return -1
        if sel != old:
            draw_bar(old, False)
            draw_bar(sel, True)


def app_pos(i):
    return 50 + (i % 4) * 73, 82 + (i // 4) * 70


def draw_app(app, i, on, first=False):
    # after the first time only the ring changes colour, not the icon
    x, y = app_pos(i)
    c = GOLD if on else WHITE
    if first:
        try:
            import GHICONS
            circ(x, y, 26, GHICONS.bg(app[1]))
            GHICONS.draw(app[1], x, y, WHITE)
        except Exception:
            ctext(y + 7, app[0][0], WHITE, x)
    halo(x, y, 27, c, 3)


def show_title(name, old=None):
    if old:
        ctext(203, old, BLACK)
    ctext(203, name, GOLD)


def app_screen(ci, sel=0):
    cname, apps = CATS[ci]
    cls()
    rbox(90, 8, 140, 24, 9, WHITE, 2, BLACK, False)
    ctext(26, cname, WHITE)
    for i in range(len(apps)):
        draw_app(apps[i], i, i == sel, True)
    show_title(apps[sel][0])
    n = len(apps)
    while True:
        k = wkey()
        old = sel
        if k == LEFT:
            sel = (sel - 1) % n
        elif k == RIGHT:
            sel = (sel + 1) % n
        elif k == UP and sel >= 4:
            sel -= 4
        elif k == DOWN and sel + 4 < n:
            sel += 4
        elif k == OK:
            return sel
        elif k == CLR:
            return -1
        if sel != old:
            draw_app(apps[old], old, False)
            draw_app(apps[sel], sel, True)
            show_title(apps[sel][0], apps[old][0])


def run_app(mod):
    if mod == "*keys":
        return key_test()
    if mod == "*wipe":
        return wipe()
    if mod == "*about":
        cls()
        message(["Game center for the", "TI-84 Evo.", "CLEAR goes back."], "GAMEHUB")
        return
    gc.collect()
    try:
        m = __import__(mod)
        # a one-file game runs itself when loaded and sets RAN
        if not getattr(m, 'RAN', False):
            m.main()
    except Exception as e:
        cls()
        message([str(e)[:26], "Is " + mod + " on the", "calculator?"], "Could not run")
    # forget the game and its part files (like GHANIMB) to free memory
    for k in [mod] + [mod[:7] + c for c in "BCDEFHP"]:
        try:
            del sys.modules[k]
        except Exception:
            pass
    m = None
    gc.collect()


def key_test():
    cls()
    ctext(30, "KEY TEST", GOLD)
    ctext(60, "Press any key to see")
    ctext(80, "its code. CLEAR twice")
    ctext(100, "in a row to leave.")
    last = 0
    while True:
        k = wkey()
        rect(60, 120, 200, 40, BLACK)
        ctext(150, "Code: " + str(k), WHITE)
        if k == CLR and last == CLR:
            return
        last = k


def wipe():
    cls()
    ctext(40, "DELETE ALL SAVES", GOLD)
    ctext(70, "This erases every")
    ctext(90, "Animation Studio")
    ctext(110, "animation.")
    ctext(150, "ENTER: delete", RED)
    ctext(175, "CLEAR: keep them")
    if wkey() != OK:
        return
    n = 0
    try:
        import GHSAVE
        n = GHSAVE.wipe()
    except Exception:
        pass
    cls()
    message([str(n) + " save lists cleared."], "Done")


def pick(st):
    # The menu. Returns the game the player picked, or None to leave.
    # st remembers [category, app, inside a category, error, game] between
    # calls, because the menu is unloaded while a game runs (see main).
    if st[3]:
        cls()
        message([st[3], "Is " + st[4] + " on the", "calculator?"], "Could not run")
        st[3] = ""
    while True:
        if not st[2]:
            ci = cat_screen(st[0])
            if ci < 0:
                cls()
                return None
            st[0], st[1], st[2] = ci, 0, 1
        ai = app_screen(st[0], st[1])
        if ai < 0:
            st[2] = 0
            continue
        st[1] = ai
        mod = CATS[st[0]][1][ai][1]
        if mod[0] == "*":
            run_app(mod)
            continue
        return mod


def main():
    # on the calculator, dist/GAMEHUB.py does this same loop but drops the
    # whole menu from memory while a game runs (tools/bundle.py)
    st = [0, 0, 0, "", ""]
    while True:
        mod = pick(st)
        if not mod:
            return
        run_app(mod)


main()
