# Name Generator: press ENTER for a new made-up name. Left/Right picks what the
# name is for (a hero, a monster, a pet, a wizard,
# a dragon or a planet), Up/Down picks
# a female or a male name.
from GHLIB import *
import random

BGC = (20, 60, 70)
PANEL = (10, 35, 45)

# kind: (word on screen, first parts, female endings, male endings, titles
# for anyone, female titles, male titles). A name is a first part plus an
# ending, and sometimes a title. Planets have no female or male.
KINDS = (
    ("HERO", ("Bra", "Kael", "Ari", "Thor", "Lyn", "Ro", "Zar", "Fen", "Mir", "Dax", "El", "Tam"),
     ("a", "wen", "dra", "ia", "ra", "elle", "ina", "issa"),
     ("dor", "ric", "ion", "mir", "lan", "vin", "eth", "an"),
     ("the Brave", "the Bold", "Swiftfoot", "of the North", "Lionheart", "the True", "Stormborn"),
     ("Queen of Blades", "the Shieldmaiden", "Lady of Light"),
     ("King of Blades", "the Shieldbearer", "Lord of Light")),
    ("MONSTER", ("Grak", "Zul", "Mog", "Skrel", "Vor", "Bog", "Kra", "Gul", "Thrax", "Urg", "Snarl", "Drog"),
     ("ra", "ixa", "mira", "ella", "gra", "ssa", "atha", "ina"),
     ("thor", "gash", "nok", "gor", "zak", "rot", "ug", "skar"),
     ("the Hungry", "of the Swamp", "Bonecrusher", "the Smelly", "the Endless", "of Doom", "the Grumpy"),
     ("Swamp Queen", "Mother of Bats", "the Witch"),
     ("Swamp King", "Father of Bats", "the Ogre")),
    ("PET", ("Mo", "Pip", "Bis", "Wig", "Noo", "Bun", "Fizz", "Lol", "Pud", "Snu", "Tib", "Zig"),
     ("bella", "kins", "lily", "cupcake", "ette", "sy", "pie", "boo"),
     ("chi", "ster", "bit", "pop", "muffin", "snoot", "beans", "gus"),
     ("the Fluffy", "the Sleepy", "the Zoomy", "of the Couch", "the Brave", "the Sneaky"),
     ("the Princess", "the Cuddly Queen", "the Cute"),
     ("the Prince", "the Cuddly King", "Jr.")),
    ("WIZARD", ("Ald", "Mer", "Zeph", "Quill", "Sol", "Orin", "Vex", "Ils", "Bram", "Nim", "Eld", "My"),
     ("yra", "andra", "iel", "ana", "elle", "ora", "ina", "essa"),
     ("bus", "ion", "dor", "wick", "oth", "aris", "ius", "on"),
     ("the Grey", "of the Stars", "Moonweaver", "the Wise", "Spellbinder", "of the Tower", "the Odd"),
     ("the Enchantress", "Witch of the Woods", "Lady of Spells"),
     ("the Enchanter", "Warlock of the Woods", "Lord of Spells")),
    ("DRAGON", ("Vyr", "Draz", "Ign", "Sca", "Fafn", "Ryn", "Zyth", "Kor", "Ember", "Sil", "Tal", "Aur"),
     ("ira", "essa", "yx", "andra", "eth", "ara", "ithra", "ona"),
     ("ax", "gorn", "ion", "rax", "oth", "ius", "drak", "on"),
     ("the Fierce", "Flamecaller", "of the Peaks", "Skyrender", "the Ancient", "Stormwing", "the Shiny"),
     ("Queen of Ashes", "Mother of Eggs", "the Sky Empress"),
     ("King of Ashes", "Father of Eggs", "the Sky Emperor")),
    ("PLANET", ("Zor", "Kep", "Vel", "Astra", "Nyx", "Oro", "Tal", "Xen", "Lumi", "Cyra", "Pol", "Rho"),
     ("ax", "lon", "ia", "us", "tara", "on", "is", "ix", "ara", "eon", "una", "os"),
     (),
     ("Prime", "IV", "Minor", "VII", "Major", "B", "X"), (), ()),
)
GENDERS = ("FEMALE", "MALE")


def one(t):
    return t[random.randint(0, len(t) - 1)]


def has_gender(k):
    return len(KINDS[k][3]) > 0


def make(k, g):
    w, first, fem, male, titles, ftit, mtit = KINDS[k]
    ends = male if g and male else fem
    a = one(first) + one(ends)
    if len(a) > 14:
        a = a[:14]
    t = ""
    if random.randint(0, 1):
        t = one(titles + ((mtit if g else ftit) if random.randint(0, 2) == 0 else ()))
    return a, t


def show_kind(k, old=None):
    # "< HERO >" at the top: cover the old word, then write the new one
    if old is not None:
        rect(60, 38, 200, 18, BGC)
    ctext(50, "< " + KINDS[k][0] + " >", GOLD)


def show_gender(k, g):
    # FEMALE  MALE under it, the chosen one gold (planets have neither)
    rect(40, 60, 240, 18, BGC)
    if has_gender(k):
        text(80, 72, GENDERS[0], GOLD if g == 0 else GREY)
        text(190, 72, GENDERS[1], GOLD if g == 1 else GREY)


def show_name(nm):
    # the panel's inside is painted over in one go, then the name on top
    rect(24, 92, 272, 70, PANEL)
    ctext(120 if nm[1] else 131, nm[0], WHITE)
    if nm[1]:
        ctext(146, nm[1], GOLD)


def game():
    k = 0
    g = 0
    cls(BGC)
    ctext(22, "NAME GENERATOR", GOLD)
    rbox(20, 88, 280, 78, 8, WHITE, 2, PANEL)
    ctext(182, "ENTER: new name", GREY)
    ctext(200, "Up/Down: female or male", GREY)
    show_kind(k)
    show_gender(k, g)
    show_name(make(k, g))
    while True:
        key_ = wkey()
        if key_ == CLR:
            return
        if key_ in (LEFT, RIGHT):
            old = k
            k = (k + (1 if key_ == RIGHT else -1)) % len(KINDS)
            show_kind(k, old)
            if has_gender(k) != has_gender(old):
                show_gender(k, g)
            show_name(make(k, g))
        elif key_ in (UP, DOWN) and has_gender(k):
            g = 1 - g
            show_gender(k, g)
            show_name(make(k, g))
        elif key_ in (OK, SECOND):
            show_name(make(k, g))


RULES = "Need a name for a story, a game or a drawing? Pick what it is for, female or male, and press ENTER for as many new names as you like."
KEYS = ["Left/Right: what it is for", "Up/Down: female or male", "ENTER: new name", "CLEAR: stop"]


def main():
    while True:
        c = home("GHNAMES", "NAME GENERATOR", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        game()
