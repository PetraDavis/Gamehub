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


def letter_box(i, used, sel):
    x = 4 + (i % 13) * 24
    y = 150 + (i // 13) * 28
    c = GOLD if i == sel else (USED if ABC[i] in used else INK)
    rect(x, y, 22, 24, WHITE)
    rbox(x, y, 22, 24, 5, c, 2, WHITE)
    text(x + 6, y + 18, ABC[i], c)


def word_line(w, used):
    rect(120, 60, 200, 30, WHITE)
    s = ""
    for ch in w:
        s += (ch if ch in used else "_") + " "
    text(310 - len(s) * 10, 85, s.strip(), INK)


def figure(n):
    if n == 0:
        rect(8, 134, 74, 5, POST)
        rect(24, 18, 5, 116, POST)
        rect(24, 18, 52, 5, POST)
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
    for i in range(26):
        letter_box(i, used, sel)
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
                word_line(w, used)
            else:
                bad += 1
                figure(bad)
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
