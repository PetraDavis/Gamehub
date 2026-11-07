# GAMEHUB - game center for the TI-84 Evo. Run this file.
from GHLIB import *
import sys
import gc

CATS = [
    ("Arcade", [("Wing It", "GHFLAP"), ("Pong", "GHPONG"), ("Breakout", "GHBREAK")]),
    ("Puzzle", [("Stack Drop", "GHBLOCKS"), ("2048", "GHMERGE"), ("Sudoku", "GHSUDOKU"), ("Simon", "GHSIMON")]),
    ("Classics", [("Solitaire", "GHSOLI"), ("Tic-Tac-Toe", "GHTTT"), ("Hangman", "GHHANG")]),
    ("Adventure", [("Tiny Quest", "GHRPG"), ("Encrypted Demo", "GHCRYPT")]),
    ("Create", [("Animation Studio", "GHANIM")]),
    ("Settings", [("Key Test", "*keys"), ("Delete All Saves", "*wipe"), ("About", "*about")]),
]

BAR_Y = 34
BAR_H = 22
BAR_GAP = 27


def header():
    cls()
    ctext(22, "GAMEHUB", WHITE)


def draw_bar(i, on):
    y = BAR_Y + i * BAR_GAP
    c = GOLD if on else WHITE
    rbox(50, y, 220, BAR_H, 9, c)
    ctext(y + 17, CATS[i][0], c)


def cat_screen(sel):
    header()
    for i in range(len(CATS)):
        draw_bar(i, i == sel)
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


def draw_app(app, i, on):
    x, y = app_pos(i)
    c = GOLD if on else WHITE
    try:
        import GHICONS
        ring(x, y, 27, c, 2, GHICONS.bg(app[1]))
        GHICONS.draw(app[1], x, y, WHITE)
    except Exception:
        ring(x, y, 27, c)
        ctext(y + 7, app[0][0], c, x)


def show_title(name):
    rect(0, 186, 320, 24, BLACK)
    ctext(203, name, GOLD)


def app_screen(ci, sel=0):
    cname, apps = CATS[ci]
    cls()
    rbox(90, 8, 140, 24, 9, WHITE)
    ctext(26, cname, WHITE)
    for i in range(len(apps)):
        draw_app(apps[i], i, i == sel)
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
            show_title(apps[sel][0])


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
        m.main()
    except Exception as e:
        cls()
        message([str(e)[:26], "Is " + mod + " on the", "calculator?"], "Could not run")
    try:
        del sys.modules[mod]
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


def main():
    ci = 0
    while True:
        ci = cat_screen(ci)
        if ci < 0:
            cls()
            return
        ai = 0
        while True:
            ai = app_screen(ci, ai)
            if ai < 0:
                break
            run_app(CATS[ci][1][ai][1])


main()
