# Hangman: guess the word one letter at a time.
from GHLIB import *
import random

WORDS = ("PLANET ROCKET GALAXY COMET ORBIT JUNGLE TIGER PARROT DOLPHIN OCTOPUS "
         "PENGUIN CASTLE DRAGON WIZARD KNIGHT PIRATE TREASURE ISLAND VOLCANO DESERT "
         "GLACIER THUNDER RAINBOW BLIZZARD TORNADO PUZZLE RIDDLE SECRET MYSTERY CIPHER "
         "LANTERN CANDLE MIRROR LADDER BASKET GUITAR TRUMPET VIOLIN PIANO DRUMS "
         "PENCIL ERASER NOTEBOOK BACKPACK LOCKER SCIENCE HISTORY ALGEBRA GEOMETRY CALCULUS "
         "PIZZA PANCAKE WAFFLE NOODLE BURRITO PRETZEL COOKIE MUFFIN BANANA AVOCADO").split()
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
INK = (20, 20, 20)
POST = (225, 175, 20)
USED = (190, 190, 190)


# Each drawing call is slow on the calculator, so a letter box is four
# rectangles (an outline with notched corners) and the letters of a row are
# written with one call: they sit 20 px apart, two characters of text.
def lxy(i):
    return 30 + (i % 13) * 20, 150 + (i // 13) * 28


def nbox(x, y, w, h, c):
    rect(x + 2, y, w - 4, 2, c)
    rect(x + 2, y + h - 2, w - 4, 2, c)
    rect(x, y + 2, 2, h - 4, c)
    rect(x + w - 2, y + 2, 2, h - 4, c)


def letter_box(i, used, sel):
    x, y = lxy(i)
    c = GOLD if i == sel else (USED if ABC[i] in used else INK)
    nbox(x, y, 18, 24, c)
    text(x + 4, y + 18, ABC[i], c)


def letters(sel):
    for i in range(26):
        if i != sel:
            x, y = lxy(i)
            nbox(x, y, 18, 24, INK)
    for r in range(2):
        text(34, 168 + r * 28, " ".join(ABC[r * 13:r * 13 + 13]), INK)
    letter_box(sel, "", sel)


def word_line(w, used, new=None):
    # first time: blanks and letters. Later only the guessed letter appears,
    # writing over its blanks, so the rest of the word stays still
    x0 = 310 - len(w) * 20
    if new is None:
        text(x0, 85, " ".join([ch if ch in used else "_" for ch in w]), INK)
        return
    at = [i for i in range(len(w)) if w[i] == new]
    for i in at:
        text(x0 + i * 20, 85, "_", WHITE)
    for i in at:
        text(x0 + i * 20, 85, new, INK)


def figure(n):
    if n == 0:
        rrect(0, 136, 120, 12, 5, (110, 180, 90))
        rect(0, 140, 120, 4, (80, 150, 70))
        rect(8, 132, 74, 6, POST)
        rect(8, 136, 74, 2, dk(POST, 0.75))
        rect(24, 18, 5, 116, POST)
        rect(27, 18, 2, 116, dk(POST, 0.75))
        rect(24, 18, 52, 5, POST)
        rect(24, 21, 52, 2, dk(POST, 0.75))
        col(POST)
        for o in range(4):
            draw_line(29 + o, 44, 50 + o, 23)
        rect(72, 23, 3, 13, (140, 90, 40))
        return
    col(INK)
    if n == 1:
        ring(73, 46, 10, INK, 2, WHITE)
        return
    a = ((73, 56, 73, 95), (73, 65, 60, 82), (73, 65, 86, 82), (73, 95, 62, 118), (73, 95, 84, 118))[n - 2]
    for o in (0, 1):
        draw_line(a[0] + o, a[1], a[2] + o, a[3])


def game():
    w = random.choice(WORDS)
    used = ""
    bad = 0
    sel = 0
    cls(WHITE)
    figure(0)
    letters(sel)
    word_line(w, used)
    while True:
        done = True
        for ch in w:
            if ch not in used:
                done = False
        if done:
            message(["You got it: " + w], "You win!")
            return
        if bad >= 6:
            message(["The word was " + w], "Out of guesses")
            return
        k = wkey()
        old = sel
        if k == LEFT:
            sel = (sel - 1) % 26
        elif k == RIGHT:
            sel = (sel + 1) % 26
        elif k == UP or k == DOWN:
            sel = (sel + 13) % 26
        elif k == CLR:
            return
        elif k == OK and ABC[sel] not in used:
            used += ABC[sel]
            if ABC[sel] in w:
                word_line(w, used, ABC[sel])
            else:
                bad += 1
                figure(bad)
        if old != sel or k == OK:
            letter_box(old, used, sel)
            letter_box(sel, used, sel)


RULES = 'Guess the hidden word one letter at a time. Six wrong guesses and the game is over.'
KEYS = ['Arrows: pick a letter', 'ENTER: guess it', 'CLEAR: quit']


def main():
    while True:
        c = home("GHHANG", 'HANGMAN', RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
