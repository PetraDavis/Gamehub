# Name Generator: press ENTER for a new made-up name. Left/Right picks what the
# name is for: a hero, a monster, a pet, a wizard or a planet.
from GHLIB import *
import random

BGC = (20, 60, 70)
PANEL = (10, 35, 45)

# kind: (word on screen, first parts, last parts, titles). A name is a first
# part plus a last part, and sometimes a title.
KINDS = (
    ("HERO", ("Bra", "Kael", "Ari", "Thor", "Lyn", "Ro", "Zara", "Fen", "Mira", "Dax", "Elo", "Tam"),
     ("dor", "wen", "ric", "a", "ion", "dra", "mir", "ia", "lan", "ra", "vin", "eth"),
     ("the Brave", "the Bold", "Swiftfoot", "of the North", "Lionheart", "the True", "Stormborn")),
    ("MONSTER", ("Grak", "Zul", "Mog", "Skrel", "Vor", "Bog", "Kra", "Gul", "Thrax", "Urg", "Snarl", "Drog"),
     ("thor", "gash", "nok", "lix", "gor", "mire", "zak", "rot", "oom", "ug", "fang", "skar"),
     ("the Hungry", "of the Swamp", "Bonecrusher", "the Smelly", "the Endless", "of Doom", "the Grumpy")),
    ("PET", ("Mo", "Pip", "Bis", "Wig", "Noo", "Bun", "Fizz", "Lolly", "Pud", "Snu", "Tib", "Ziggy"),
     ("chi", "kins", "bles", "gy", "dle", "ster", "bit", "pop", "muffin", "snoot", "beans", "boo"),
     ("the Fluffy", "Sir Wiggles", "the Sleepy", "Jr.", "the Zoomy", "of the Couch", "the Brave")),
    ("WIZARD", ("Alda", "Mer", "Zeph", "Quill", "Sol", "Orin", "Vex", "Ilsa", "Bram", "Nim", "Eld", "Myra"),
     ("bus", "ion", "yra", "dor", "wick", "andra", "oth", "iel", "aris", "ius", "on", "ana"),
     ("the Grey", "of the Stars", "Moonweaver", "the Wise", "Spellbinder", "of the Tower", "the Odd")),
    ("PLANET", ("Zor", "Kep", "Vel", "Astra", "Nyx", "Oro", "Tal", "Xen", "Lumi", "Cyra", "Pol", "Rho"),
     ("ax", "lon", "ia", "us", "tara", "on", "is", "ix", "ara", "eon", "una", "os"),
     ("Prime", "IV", "Minor", "VII", "Major", "B", "X")),
)


def one(t):
    return t[random.randint(0, len(t) - 1)]


def make(k):
    w, first, last, titles = KINDS[k]
    a = one(first) + one(last)
    if random.randint(0, 3) == 0:
        a = a + one(last)
    if len(a) > 14:
        a = a[:14]
    return a, (one(titles) if random.randint(0, 1) else "")


def show_kind(k, old=None):
    # "< HERO >" at the top: cover the old word, then write the new one
    if old is not None:
        rect(60, 44, 200, 18, BGC)
    ctext(56, "< " + KINDS[k][0] + " >", GOLD)


def show_name(nm):
    # the panel's inside is painted over in one go, then the name on top
    rect(24, 86, 272, 74, PANEL)
    ctext(116 if nm[1] else 128, nm[0], WHITE)
    if nm[1]:
        ctext(142, nm[1], GOLD)


def game():
    k = 0
    cls(BGC)
    ctext(22, "NAME GENERATOR", GOLD)
    rbox(20, 82, 280, 82, 8, WHITE, 2, PANEL)
    ctext(180, "ENTER: new name", GREY)
    ctext(199, "Left/Right: kind  CLEAR: stop", GREY)
    show_kind(k)
    show_name(make(k))
    while True:
        key_ = wkey()
        if key_ == CLR:
            return
        if key_ in (LEFT, RIGHT):
            old = k
            k = (k + (1 if key_ == RIGHT else -1)) % len(KINDS)
            show_kind(k, old)
            show_name(make(k))
        elif key_ in (OK, UP, DOWN, SECOND):
            show_name(make(k))


RULES = "Need a name for a story, a game or a drawing? Pick what it is for and press ENTER for as many new names as you like."
KEYS = ["Left/Right: what it is for", "ENTER: new name", "CLEAR: stop"]


def main():
    while True:
        c = home("GHNAMES", "NAME GENERATOR", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
