# Dragon Tamer: explore three lands, find dragon eggs and hatch them, name
# your dragons, ride them over water, lava and mountains, and fight monsters.
# 20 kinds of dragon from Common to Legendary, a Dragon Book that fills in as
# you hatch them, and a very rare evil dragon with a secret egg. Saves your dragons, coins, accessories and the
# eggs in your backpack every time you visit the nest.
from GHLIB import *
import random

TEST = False      # True: the evil dragon shows up often, for testing
EVIL = 0.12 if TEST else 0.004

T = 20
# The calculator can't hold the whole game at once, so tools/bundle.py puts
# these functions in their own files. Each file is loaded when one of its
# functions is called and dropped from memory again when it returns.
SWAP = {"W": ("bar", "foe_art", "foe_screen", "battle", "evil", "titan"),
        "X": ("rest", "load", "new_quest", "board", "portrait", "pen", "lst", "dress", "shop", "nest",
              "win"),
        # the merchant has a file of his own, with its own copy of the list, so the
        # pen and fights don't have to carry his code
        "Z": ("shen", "cop", "who", "glim", "zl", "shen_off", "pol_off"),
        "Y": ("backpack", "book", "hatch", "oval", "egg", "frame", "kbox", "typed", "menu")}
MAPS = (
    ["TTTTTTTTTTTTT~~~",
     'T.....""".....~~',
     'T.H...""""...~~~',
     'T.....""".T...~~',
     "...........E.~~~",
     "T....TT.......~~",
     'T.""".TT......~~',
     'T.""".........~~',
     "TTTTTTTTTTTTTT~~"],
    ["~^^^^^^^^^^^^^^^",
     '~...""""..LLL..^',
     '~..^"""..LLELL.^',
     "~.....^...LLL...",
     "~...............",
     '~...^^...."""...',
     '~..LL....."""..^',
     "~.....^^.......^",
     "~^^^^^^^^^^^^^^^"],
    ["^^^^^^^^^^^^^^^^",
     '...""".....^E^^^',
     "...........^^^^^",
     "......~~~~......",
     "....~~~~B~~~....",
     ".....~~~~~......",
     '.."""...........',
     '..""".....^C....',
     "^^^^^^^^^^^^^^^^"],
    # the village, left of Green Valley: Q quest hall, S shop, W well, = path
    ["TTTTTTTTTTTTTTTT",
     "T..............T",
     "T..Q.......S...T",
     "T..=.......=...T",
     "T..=============",
     "T.......W......T",
     "T..............T",
     "T..............T",
     "TTTTTTTTTTTTTTTT"],
)
LANDS = ("Green Valley", "Fire Mountain", "Frost Peaks", "Village")
GROUND = ((50, 130, 60), (85, 65, 55), (215, 225, 240), (75, 150, 70))
TALL = ((35, 100, 45), (120, 90, 60), (170, 190, 220), (75, 150, 70))
WATER = (40, 90, 190)
LAVA = (230, 90, 20)
ROCK = (110, 105, 115)
LEAF = (25, 85, 35)
BARK = (90, 60, 30)
CYAN = (60, 230, 230)
NIGHT = (45, 50, 80)   # behind monsters and dragon pictures
MAG = (230, 60, 220)

# elements: 0 fire, 1 water, 2 plant, 3 star. Fire burns plant, water puts
# out fire, plant drinks water, and star beats them all.
ENAME = ("fire", "water", "plant", "star")
RARE = ("Common", "Uncommon", "Rare", "Epic", "Legendary", "Quantum", "Ancient")
def cl(b):
    # colours packed as bytes (r, g, b, r, g, b...): far fewer code words
    return [tuple(b[i:i + 3]) for i in range(0, len(b), 3)]


RCOL = cl(b'\xff\xff\xffx\xdcxZ\xa0\xff\xc8n\xf0\xe6\xb4(<\xe6\xe6\xf5\xa0<')
# dragon kinds: name, element, rarity, colour. Each rarer level has fewer.
DT = list(zip(('Pyrrak', 'Smoldedrake', 'Aquawyrm', 'Gillwing', 'Fernling', 'Lichenwing', 'Stonewyrm', 'Volcanox', 'Ashveil', 'Glacius', 'Tempestra', 'Thornwyrm', 'Dawnwing', 'Pearlhorn', 'Jadewyrm', 'Petalwyrm', 'Blazequill', 'Abyssar', 'Rootwyrm', 'Lumora', 'Quantum', 'Petralith'),
         b'\x00\x00\x01\x01\x02\x02\x02\x00\x00\x01\x01\x02\x00\x01\x02\x02\x00\x01\x02\x03\x03\x03', b'\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x02\x02\x02\x02\x03\x03\x03\x04\x05\x06', cl(b'\xdcF(\xeb\x8c(<\x82\xe6(\xaa\xaaF\xaaF\x82\x96<\x96\x8cx\xaa(\x1eKKU\xa0\xd2\xf5xd\xc8\x1en<\xf0\xbe(\xf0x\x96<\xc8\x96\xfa\xa0\xd2\xffZ<\x1e<\xa0nP(\x19\x19#\x19\x1eP}vn')))
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NAMES = ("Blaze", "Splash", "Fern", "Spark", "Misty", "Clover", "Ziggy", "Nova",
         "Pebble", "Rocket", "Biscuit", "Luna", "Comet", "Pip", "Maple", "Echo",
         "Sunny", "Bolt", "Willow", "Ash", "Ripple", "Twig", "Ember", "Taro")
PAINT = cl(b'\xdcF(<\x82\xe6F\xaaF\xf0\xbe(\xc8n\xf0\xf0x\x96((2\xf0\xf0\xf5')
PAINTN = ("Red", "Blue", "Green", "Gold", "Purple", "Pink", "Black", "White")
# accessories 1-8 go on the head, 9-16 on the body: name, price
GEAR = (("", 0), ("Bow", 15), ("Goggles", 25), ("Wizard hat", 40), ("Crown", 80),
        ("Party hat", 20), ("Top hat", 35), ("Flower", 15), ("Viking helmet", 60),
        ("Scarf", 15), ("Saddle", 25), ("Cape", 40), ("Armor", 60),
        ("Bell collar", 20), ("Backpack", 30), ("Flag", 45), ("Necklace", 50))
GEARC = [None] + cl(b'\xfa\x96\xc8(((\x82<\xbe\xe6\xb4(<\xe6\xe6\x00\x00\x00\xfa\x96\xc8\xbe\xc3\xcd\xdc(\x1eZ<\x1e(P\xc8\xbe\xc3\xcd(P\xc8Z\xbeP\xdc(\x1e\xe6\xb4(')
# picture colours used by the art below; 15-17 are the dragon's own
PAL = cl(b'\x00\x00\x00\xff\xff\xff\xfa\xdc<\xf5\x8c\x1e\xdc(\x1exx}\xc8\xc8\xd2\x1eZ(Z\xbeP\xfa\x96\xc8nK(<\xe6\xe6\xe6<\xdc\xe6\xb4(\xaa\xd2\xfa')
PAL2 = cl(b'\x82<\xbe\xbe\xc3\xcd(P\xc8\x1e\x1eF\xc8\x82\xff\xaa\x14\x1e')
PAL3 = cl(b'F-\x14\xb4\x82\x14dix\xc8P\x96\x14\x8c\xa0\x14(x\xa0n<\xf0\xd7\xff')

# ART: made by tools/dragdata.py (edit the shapes there, then run it)
ARTB = b'\x02\x10\x1e\x19-\x08/\x19\x00\x19\x1b"\x04\x07\x00\x00\x00\x19\x19(\x05\x02\x00\x00\x00\x19)"\x04\x07\x00\x00\x00\x19\'(\x05\x02\x00\x00\x02\x11)\x1a9\x1f)#\x02\x116\x1b<\x1f6#\x01\x11\x1a\x1e\x05\x00\x00\x00\x01\x11)\x1e\x05\x00\x00\x00\x00\x11\x1a\x19\x0f\n\x00\x00\x02\x11\x12\x15\x1c\x1a\x16 \x00\x11\x11\x14\x07\n\x00\x00\x00\x11\n\x10\x0c\x08\x00\x00\x00\x11\x08\x13\x04\x05\x00\x00\x02\x10) 9\x1f)#\x00\x10\x08\x17\x0b\x02\x00\x00\x00\x18\x1a\x19\x0e\x02\x00\x00\x00\x18\x0b\x10\t\x01\x00\x00\x00\x0f\x18 \x13\x03\x00\x00\x00\x0f\x11\x18\x02\x06\x00\x00\x02\x0f\x12\x10\x19\n\x15\x12\x00\x10\x1d \x01\x03\x00\x00\x00\x10! \x01\x03\x00\x00\x00\x10% \x01\x03\x00\x00\x02\x10\x0f\x11\x14\n\x12\x11'
ARTL = b'\x01\x11\x1b"\x04\x00\x00\x00\x00\x11\x18"\x05\x07\x00\x00\x00\x11\x16(\x07\x02\x00\x00\x01\x11("\x04\x00\x00\x00\x00\x11%"\x05\x07\x00\x00\x00\x11#(\x07\x02\x00\x00\x00\x19\x0c\x10\x05\x01\x00\x00\x00\x01\x0c\x12\x03\x02\x00\x00\x00\x01\n\x17\x01\x01\x00\x00\x00\x01\x16)\x01\x01\x00\x00\x00\x01#)\x01\x01\x00\x00\x00\x00\r\x12\x02\x02\x00\x00\x00\x00\t\x14\x01\x01\x00\x00'
ARTF = (b'\x02\x036\x1e<\x10@\x1e\x02\x029\x1e<\x15>\x1e',
        b'\x00\x10\x1e\x1d\x02\x02\x00\x00\x00\x10$\x1e\x02\x02\x00\x00\x00\x10+\x1d\x02\x02\x00\x00',
        b'\x02\x0f.\x1c3\x156\x1d\x02\x100\x1c3\x175\x1d\x01\x0e\x1e\x1d\x01\x00\x00\x00\x01\x0e#\x1c\x01\x00\x00\x00\x01\x0e)\x1d\x01\x00\x00\x00',
        b'\x00\x01\x16\x1c\x07\x02\x00\x00\x00\x01\x1d\x1d\x07\x02\x00\x00\x00\x01$\x1c\x08\x02\x00\x00\x00\x01,\x1d\x04\x01\x00\x00',
        b'',
        b'\x00\x07\x1a\x1b\x05\x03\x00\x00\x00\x07#\x1e\x05\x02\x00\x00\x00\x07+\x1c\x03\x02\x00\x00\x00\x070\x1d\x03\x02\x00\x00',
        b'\x01\x05-\x1b\x02\x00\x00\x00\x01\x051\x1c\x02\x00\x00\x00\x01\x055\x1e\x01\x00\x00\x00\x01\x05\x1e\x1e\x02\x00\x00\x00\x01\x05&\x1f\x02\x00\x00\x00\x01\x06\x1e\x1d\x01\x00\x00\x00\x01\x06&\x1e\x01\x00\x00\x00',
        b'\x00\x03\x19\x1c\x06\x01\x00\x00\x00\x03\x1e\x1c\x01\x04\x00\x00\x00\x03#\x1b\x01\x05\x00\x00\x00\x03#\x1f\x06\x01\x00\x00\x00\x03,\x1d\x05\x01\x00\x00',
        b'',
        b'\x02\x01\x1d\x19\x1f\x13!\x19\x02\x01+\x1b-\x16/\x1c\x02\x010\x1d2\x184\x1e',
        b'',
        b'\x02\x10\x1d\x19\x1f\x14!\x19\x02\x10+\x1b-\x16/\x1c\x02\x100\x1d2\x184\x1e',
        b'',
        b'',
        b'\x00\x1e\x1c\x1d\x02\x01\x00\x00\x00\x1e"\x1e\x02\x01\x00\x00\x00\x1e(\x1d\x02\x01\x00\x00',
        b'',
        b'\x02\x035\x1e;\rA\x1e\x02\x028\x1e;\x13>\x1e',
        b'\x02\x0f)\x1a,\x14/\x1b\x02\x0f0\x1d4\x176\x1e\x01\x0b\x1d\x1d\x01\x00\x00\x00\x01\x0b#\x1e\x01\x00\x00\x00\x01\x0b*\x1d\x01\x00\x00\x00',
        b'\x00\x10\x1c\x1a\x01\x08\x00\x00\x00\x10!\x1a\x01\x08\x00\x00\x00\x10&\x1a\x01\x08\x00\x00\x00\x10-\x1c\x01\x04\x00\x00',
        b'',
        b'\x00\x00"\x19\x07\n\x00\x00\x01\x00)\x1e\x05\x00\x00\x00\x02\x00)\x1a9\x1f)#\x02\x12*\x1b-\x14/\x1c\x02\x120\x1d3\x175\x1e\x02\x16+\x1b-\x14.\x1b\x02\x161\x1d3\x174\x1d\x02\x16\x12\x10\x19\n\x15\x12\x00\x16\x11\x18\x02\x06\x00\x00\x00\x16\x19\x1d\x08\x01\x00\x00\x00\x16 \x1d\x01\x03\x00\x00\x00\x16 \x1f\t\x01\x00\x00\x00\x16)\x1c\x01\x04\x00\x00\x00\x16.\x1d\x07\x01\x00\x00',
        b"\x00\x10\x1b\x1a\x05\x03\x00\x00\x00\x10#\x1e\x05\x03\x00\x00\x00\x10,\x1c\x04\x02\x00\x00\x02\x10\x12\x16\x16\x15\x14\x1a\x02\x13\x13\x15\x15\r\x18\x15\x02\x13\x17\x17\x1a\x10\x1c\x18\x02\x13*\x1b-\x120\x1c\x02\x130\x1d3\x156\x1e\x02\x135\x1e7\x199\x1e\x02\x01\x14\x15\x15\r\x15\x15\x02\x01+\x1a-\x12-\x1a\x02\x011\x1c3\x153\x1c\x00\x03\x19\x1d\x07\x01\x00\x00\x00\x03\x1f\x1d\x01\x04\x00\x00\x00\x03\x1f \x08\x01\x00\x00\x00\x03'\x1c\x01\x05\x00\x00\x00\x03'\x1c\x07\x01\x00\x00\x00\x03.\x1d\x01\x02\x00\x00\x00\x03\x11\x17\x01\x05\x00\x00\x00\x03\x11\x17\x03\x01\x00\x00\x00\x02\x1a\x1d\x05\x01\x00\x00\x00\x02  \x06\x01\x00\x00\x00\x02(\x1c\x05\x01\x00\x00",
        b'\x02\x17\x1c\x19\x1e\x13 \x19\x02\x17+\x1b-\x150\x1c\x02\x171\x1d3\x186\x1e\x02\x17\x13\x14\x15\x0f\x18\x14\x00\x19\x18 \x13\x03\x00\x00\x00\x17\x11\x18\x02\x06\x00\x00')
ARTW = b'\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x05\x1c\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x03\x02\x0f\x10\x0f\x10\x15\x00\x15\x16\x10\r\x00\x17'
ARTO = (b'',
        b'\x01\x06\x06\x12\x02\x00\x00\x00\x01\x06\x04\x0e\x02\x00\x00\x00\x01\x05\x03\n\x01\x00\x00\x00',
        b'\x02\x0f\x11\x13\x16\x10\x14\x16',
        b'\x00\x10\x13\x15\x01\x03\x00\x00\x00\x10\x15\x15\x01\x03\x00\x00',
        b'\x02\x08\x0c\x10\x0f\x08\x12\x10\x02\x07\x0f\x10\x0f\x08\x12\x10\x00\x07\x0f\x0c\x01\x04\x00\x00',
        b'\x00\x07\x11\x11\x03\x02\x00\x00',
        b'\x01\x05\x14\x14\x02\x00\x00\x00',
        b'\x00\x03\x11\x15\x03\x01\x00\x00',
        b'\x01\x06\x06\x14\x02\x00\x00\x00',
        b'\x00\x0e\x0b\x11\x02\x01\x00\x00',
        b'\x00\x02$\x0f\x02\x04\x00\x00\x00\x02"\x12\x04\x02\x00\x00\x00\x02"\x13\x02\x05\x00\x00',
        b'',
        b'\x01\x02!\x1f\x03\x00\x00\x00\x01\r!\x1f\x01\x00\x00\x00',
        b'\x00\t\r\t\x02\x07\x00\x00\x00\t\x0b\n\x02\x02\x00\x00\x00\t\x12\x08\x02\x08\x00\x00\x00\t\x14\t\x02\x02\x00\x00\x00\x1d\x0e\t\x01\x07\x00\x00\x00\x1d\x13\x08\x01\x08\x00\x00',
        b'\x00\x0b\x10\x10\x03\x02\x00\x00\x00\x01\x10\x10\x01\x01\x00\x00',
        b'\x01\t$\x12\x02\x00\x00\x00\x01\x01!\x16\x02\x00\x00\x00\x01\t\x1e\x18\x01\x00\x00\x00\x01\x02$\x18\x01\x00\x00\x00',
        b'\x02\x02\x0b\x10\x0e\x08\x11\x10',
        b'',
        b'\x00\n\x0e\x08\x02\x08\x00\x00\x00\n\x0b\t\x04\x02\x00\x00\x00\n\x12\x08\x02\x08\x00\x00\x00\n\x13\x08\x04\x02\x00\x00',
        b'\x02\x02!\x1c$!\x1e!\x00\x02#\x10\x02\x02\x00\x00\x00\x02!\x15\x02\x02\x00\x00\x00\x02\x1d\x18\x01\x01\x00\x00\x00\x02%\r\x01\x01\x00\x00\x00\x02#\x19\x01\x01\x00\x00\x00\x02\r\x12\x02\x02\x00\x00',
        b'\x00\x01 \x13\x01\x01\x00\x00\x00!#\x0f\x01\x01\x00\x00\x00\x01\x1d\x17\x01\x01\x00\x00\x00!$\x16\x01\x01\x00\x00\x00!!\x18\x01\x01\x00\x00\x00\x01%\x0c\x01\x03\x00\x00\x00\x01$\r\x03\x01\x00\x00\x02\x16\x13\x1c\x16\x18\x19\x1c\x02\x16\x13\x1c\x16 \x19\x1c\x00!\x15\x1b\x03\x02\x00\x00\x00\x01\x16\x1b\x01\x02\x00\x00\x02\x12\x0e\x11\x12\x05\x12\x11\x02\x16\x11\x11\x1b\x01\x16\x12\x02!\x13\x10\x1b\x01\x15\x10\x02\x166\x1b<\x1f6#\x01\x16=\x1f\x03\x00\x00\x00\x01!=\x1f\x02\x00\x00\x00\x00\x01=\x1e\x01\x01\x00\x00\x00\x16\n\x15\x06\x01\x00\x00\x00\x16\x0c\x12\x03\x02\x00\x00\x00\x01\r\x12\x01\x01\x00\x00',
        b'\x01\x10=\x1f\x04\x00\x00\x00\x01\x05<\x1e\x03\x00\x00\x00\x01\x06;\x1d\x01\x00\x00\x00\x00\x03<\x1e\x03\x01\x00\x00\x00\x02>\x1f\x01\x02\x00\x00\x02\x10\r\x11\x10\x07\x12\x11\x02\x13\x10\x11\x15\x00\x18\x11\x02\x01\x13\x0f\x15\x00\x15\x0f\x02\x02\x14\x03\x15\x00\x16\x03\x02\x02\x0f\n\x10\x07\x11\n\x00\x02\x0c\x12\x03\x02\x00\x00\x00\x01\r\x12\x01\x01\x00\x00\x00\x03\n\x15\x06\x01\x00\x00\x02\x03\x12\x1c\x15\x17\x18\x1c\x02\x03\x12\x1c\x15!\x18\x1c\x02\x02\x13\x1c\x15\x19\x17\x1c\x02\x02\x13\x1c\x15\x1f\x17\x1c\x00\x01\x14\x1a\x01\x02\x00\x00\x01\x05\x04\x0b\x02\x00\x00\x00\x00\x06\x03\n\x01\x01\x00\x00\x01\x05\x1f\x04\x02\x00\x00\x00\x00\x06\x1e\x03\x01\x01\x00\x00\x01\x05;\x11\x02\x00\x00\x00\x00\x06:\x10\x01\x01\x00\x00\x00\x02#\x06\x01\x01\x00\x00\x00\x02?\x12\x01\x01\x00\x00',
        b'\x02\x00\x11\x11\x1c\x02\x16\x12\x02\x00\x0e\x10\x14\x04\x12\x11\x00\x17\x08\x17\x0b\x01\x00\x00\x00\x01\n\x17\x01\x02\x00\x00\x00\x01\r\x17\x01\x02\x00\x00\x00\x01\x10\x17\x01\x02\x00\x00\x00\x12\x0b\x11\x05\x04\x00\x00\x00\x16\x0c\x12\x03\x02\x00\x00\x00\x01\r\x12\x01\x01\x00\x00\x02\x00\x0b\x10\x11\x10\x11\x12')
ARTU = (b'', b'\x02\x10\x14\x14\x16\x10\x18\x15\x02\x10\x17\x16\x19\x12\x1b\x18\x02\x10+\x1b-\x17/\x1c\x02\x100\x1c2\x194\x1d\x02\x104\x1d6\x1b7\x1e', b'\x02\x10\x14\x14\x16\x10\x18\x15\x02\x10\x17\x16\x19\x12\x1b\x18\x02\x10+\x1b-\x17/\x1c\x02\x100\x1c2\x194\x1d\x02\x104\x1d6\x1b7\x1e', b'\x02\x10\x14\x14\x16\x10\x18\x15\x02\x10\x17\x16\x19\x12\x1b\x18\x02\x10+\x1b-\x17/\x1c\x02\x100\x1c2\x194\x1d\x02\x104\x1d6\x1b7\x1e', b'\x02\x10\x14\x14\x16\x10\x18\x15\x02\x10\x17\x16\x19\x12\x1b\x18\x02\x10+\x1b-\x17/\x1c\x02\x100\x1c2\x194\x1d\x02\x104\x1d6\x1b7\x1e', b'', b'')
ARTT = (b'', b'', b'\x02\x0f\x13\x15\x19\x11\x16\x18\x02\x10\x14\x16\x19\x14\x16\x18\x00\x01\r\x12\x01\x01\x00\x00', b'\x02\x0f\x13\x15\x19\x11\x16\x18\x02\x10\x14\x16\x19\x14\x16\x18\x00\x01\r\x12\x01\x01\x00\x00\x02\x02\x17\x0c\x19\n\x18\r\x02\x02\x12\x0c\x14\n\x13\r\x02\x1b+\x1b-\x17/\x1c\x02\x1b0\x1c2\x194\x1d\x02\x1b4\x1d6\x1b7\x1e\x02\x02,\x1a-\x17.\x1a\x02\x021\x1b2\x193\x1b\x00\x02\x16)\x01\x01\x00\x00\x00\x02#)\x01\x01\x00\x00\x02\x1b\x13\x1c\x15\x19\x17\x1c\x02\x1b\x13\x1c\x15\x1f\x17\x1c\x00\x01\x15\x1b\x01\x02\x00\x00', b'\x02\x0f\x13\x15\x19\x11\x16\x18\x02\x10\x14\x16\x19\x14\x16\x18\x00\x01\r\x12\x01\x01\x00\x00\x02\x02\x17\x0c\x19\n\x18\r\x02\x02\x12\x0c\x14\n\x13\r\x02\x1b+\x1b-\x17/\x1c\x02\x1b0\x1c2\x194\x1d\x02\x1b4\x1d6\x1b7\x1e\x02\x02,\x1a-\x17.\x1a\x02\x021\x1b2\x193\x1b\x00\x02\x16)\x01\x01\x00\x00\x00\x02#)\x01\x01\x00\x00\x02\x1b\x13\x1c\x15\x19\x17\x1c\x02\x1b\x13\x1c\x15\x1f\x17\x1c\x00\x01\x15\x1b\x01\x02\x00\x00\x02\x0f\x11\x14\n\x0b\x15\x11\x02\x10\x11\x14\r\x0e\x14\x12\x00\x02\x05\x0b\x01\x05\x00\x00\x00\x02\x03\r\x05\x01\x00\x00\x00\x02\x1d\x06\x01\x05\x00\x00\x00\x02\x1b\x08\x05\x01\x00\x00\x00\x02:\x14\x01\x05\x00\x00\x00\x028\x16\x05\x01\x00\x00\x00\x01\x05\r\x01\x01\x00\x00\x00\x01\x1d\x08\x01\x01\x00\x00\x00\x01:\x16\x01\x01\x00\x00\x00\x02\x0c\t\x01\x01\x00\x00\x00\x022\x0c\x01\x01\x00\x00\x00\x02>$\x01\x01\x00\x00', b'\x02\x0f\x13\x15\x19\x11\x16\x18\x02\x10\x14\x16\x19\x14\x16\x18\x00\x01\r\x12\x01\x01\x00\x00\x02\x0f\x11\x14\n\x0b\x15\x11\x02\x10\x11\x14\r\x0e\x14\x12\x00!\x05\x0b\x01\x05\x00\x00\x00!\x03\r\x05\x01\x00\x00\x00!\x1d\x06\x01\x05\x00\x00\x00!\x1b\x08\x05\x01\x00\x00\x00!:\x14\x01\x05\x00\x00\x00!8\x16\x05\x01\x00\x00\x00\x01\x05\r\x01\x01\x00\x00\x00\x01\x1d\x08\x01\x01\x00\x00\x00\x01:\x16\x01\x01\x00\x00\x00!\x0c\t\x01\x01\x00\x00\x00!2\x0c\x01\x01\x00\x00\x00!>$\x01\x01\x00\x00', b'\x02\x0f\x13\x15\x19\x11\x16\x18\x02\x10\x14\x16\x19\x14\x16\x18\x00\x01\r\x12\x01\x01\x00\x00\x02\x0f\x11\x14\n\x0b\x15\x11\x02\x10\x11\x14\r\x0e\x14\x12')
ARTG = (b'',
        b'\x02\t\x14\x0e\x10\n\x10\x12\x02\t\x14\x0e\x18\n\x18\x12\x02\x1d\x14\x0e\x11\r\x11\x11\x02\x1d\x14\x0e\x17\r\x17\x11\x00\x0c\x13\r\x02\x02\x00\x00',
        b'\x00\x1a\x0b\x11\x0c\x02\x00\x00\x00\x1c\x0b\x10\x06\x05\x00\x00\x00\x0e\x0c\x11\x04\x03\x00\x00\x00\x01\x0c\x11\x01\x01\x00\x00',
        b'\x02\x12\x0b\x0f\x10\x01\x14\x0f\x02\x15\x10\x01\x14\x0f\x11\x0f\x00\x12\t\x0f\x0c\x02\x00\x00\x00\x15\t\x10\x0c\x01\x00\x00\x00\x16\x0c\x0c\x07\x01\x00\x00\x00\x02\x0e\x08\x02\x02\x00\x00\x00\x02\x11\x0b\x01\x01\x00\x00',
        b'\x00\r\x0b\r\t\x03\x00\x00\x02\r\x0b\r\x0b\t\x0e\r\x02\r\r\r\x0f\x08\x12\r\x02\r\x11\r\x14\t\x14\r\x00\x1b\x0b\x0f\t\x01\x00\x00\x00\x02\x0c\r\x01\x01\x00\x00\x00\x04\r\x0e\x01\x01\x00\x00\x00\x0b\x11\x0e\x01\x01\x00\x00',
        b'\x02\x0b\x0b\x10\x0f\x02\x13\x10\x02\x1e\x0f\x02\x13\x10\x10\x10\x00\x02\r\n\x04\x01\x00\x00\x00\x02\x0c\r\x06\x01\x00\x00\x01\x0c\x0f\x02\x02\x00\x00\x00',
        b'\x00\x00\t\x0f\r\x02\x00\x00\x00\x00\x0b\x05\t\n\x00\x00\x00\x04\x0b\x0c\t\x02\x00\x00\x00\x1c\x0c\x06\x01\x06\x00\x00',
        b'\x02\x08\x13\x0f\x18\x0c\x15\x10\x01\t\x11\x0b\x02\x00\x00\x00\x01\t\x14\x0e\x02\x00\x00\x00\x01\t\x0e\x0e\x02\x00\x00\x00\x01\x1d\x11\x10\x02\x00\x00\x00\x01\x02\x11\x0e\x02\x00\x00\x00\x00\x03\x11\x0e\x01\x01\x00\x00',
        b'\x02\x06\x0c\x0e\x07\x07\x0c\x0b\x02\x06\x14\x0e\x19\x07\x14\x0b\x01\x13\x10\r\x04\x00\x00\x00\x00\x13\x0b\r\n\x03\x00\x00\x00\x1c\x11\x0c\x04\x04\x00\x00\x00\r\n\x10\x0c\x01\x00\x00\x00\x01\x0e\x0b\x01\x02\x00\x00',
        b'\x00\x04\x10\x16\t\x03\x00\x00\x00\x04\x14\x19\x03\x06\x00\x00\x00\x17\x10\x18\t\x01\x00\x00\x00\x17\x16\x19\x01\x06\x00\x00\x00\x01\x12\x16\x01\x03\x00\x00\x00\x01\x14\x1c\x03\x01\x00\x00',
        b'\x00\n\x1b\x17\x0b\x04\x00\x00\x00 \x1c\x17\t\x01\x00\x00\x00\x1a\x1b\x1a\x0b\x01\x00\x00\x00\x1a\x1b\x14\x02\x04\x00\x00\x00\x1a \x1b\x01\x06\x00\x00\x00\r\x1f!\x03\x01\x00\x00',
        b"\x02\x14\x12\x16&\x170'\x02\x1f\x1c\x17&\x170'\x01\r\x13\x17\x02\x00\x00\x00\x00\x02\x12\x16\x01\x01\x00\x00",
        b'\x00\x13\x16\x1c\x16\x06\x00\x00\x00\x13\x11\x15\x06\x08\x00\x00\x00\x01\x17\x1c\x14\x01\x00\x00\x00\x1c\x16!\x16\x01\x00\x00\x00\x1c\x11\x19\x06\x01\x00\x00\x00\x1c \x1c\x01\x06\x00\x00\x00\r\x1a\x1e\x01\x01\x00\x00\x00\r&\x1e\x01\x01\x00\x00',
        b'\x00\x14\x10\x16\t\x02\x00\x00\x00\x1f\x10\x17\t\x01\x00\x00\x01\x1b\x14\x1a\x02\x00\x00\x00\x01\r\x14\x19\x01\x00\x00\x00\x00\x00\x13\x1b\x02\x01\x00\x00',
        b"\x00\x1a&\x17\x01\x05\x00\x00\x00\x08'\x13\x07\x07\x00\x00\x00\x07'\x13\x07\x02\x00\x00\x00\x07,\x15\x02\x05\x00\x00\x00\r*\x15\x01\x01\x00\x00\x00\x01(\x16\x01\x02\x00\x00",
        b'\x00\x1a*\x04\x01\x15\x00\x00\x00\x04+\x04\t\x06\x00\x00\x00\x17+\x08\t\x02\x00\x00\x00\x02.\x06\x02\x02\x00\x00\x00\r)\x03\x03\x01\x00\x00',
        b'\x00\r\x11\x19\x07\x01\x00\x00\x00\x1b\x13\x1a\x03\x01\x00\x00\x01\x0b\x14\x1c\x02\x00\x00\x00\x00\x1e\x14\x1d\x02\x01\x00\x00\x00\x01\x13\x1b\x01\x01\x00\x00')
MONA = (b'\x02\x002:ADAN\x02\x00j:[D[N\x02\x018?AEAK\x02\x01d?[E[K\x00\x00:l\x08\x0e\x00\x00\x00\x00Z\\\x08\x12\x00\x00\x00\x02>X \x1e\x00\x00\x00\x03>X\x0e\x1e\x00\x00\x00\x04>h \x04\x00\x00\x00\x05Lh\x04\x04\x00\x00\x01\x00NJ\x0f\x00\x00\x00\x01\x06LH\r\x00\x00\x00\x01\x07HD\x05\x00\x00\x00\x00\x08BD\t\x02\x00\x00\x00\x08QD\t\x02\x00\x00\x00\tDG\x05\x04\x00\x00\x00\tSG\x05\x04\x00\x00\x00\nFH\x02\x02\x00\x00\x00\nUH\x02\x02\x00\x00\x00\x0bFQ\x10\x04\x00\x00\x00\x0cHQ\x02\x02\x00\x00\x00\x0cRQ\x02\x02\x00\x00\x00\r`P\x05"\x00\x00\x01\rbN\x08\x00\x00\x00\x01\x0e`L\x05\x00\x00\x00\x00\x00Av\t\n\x00\x00\x00\x06Rv\t\n\x00\x00',
        b'\x01\x00Nd\x1c\x00\x00\x00\x01\x01J`\x19\x00\x00\x00\x01\x02BV\x08\x00\x00\x00\x01\x00>H\n\x00\x00\x00\x01\x00^H\n\x00\x00\x00\x01\x01=G\x08\x00\x00\x00\x01\x01]G\x08\x00\x00\x00\x01\x03>H\x05\x00\x00\x00\x01\x03^H\x05\x00\x00\x00\x00\x04=E\x03\x06\x00\x00\x00\x04]E\x03\x06\x00\x00\x00\x05<E\x01\x01\x00\x00\x00\x05\\E\x01\x01\x00\x00\x00\x068`,\x03\x00\x00\x01\x07Nr\x0e\x00\x00\x00\x00\x07@r\x1c\x0c\x00\x00\x01\x00@V\x03\x00\x00\x00\x00\x02?T\x01\x01\x00\x00\x01\x00ZX\x03\x00\x00\x00\x00\x02YV\x01\x01\x00\x00\x01\x00PR\x03\x00\x00\x00\x00\x02OP\x01\x01\x00\x00\x01\x00bf\x03\x00\x00\x00\x00\x02ad\x01\x01\x00\x00\x00\x002x\x0e\x06\x00\x00\x00\x00\\x\x0e\x06\x00\x00',
        b'\x02\x003HiH\\~\x02\x003H\\~Nl\x02\x003HNl@~\x02\x019JcJXt\x02\x019JXtNf\x02\x019JNfDt\x02\x02BPZPNh\x02\x03`dpRfr\x02\x04?<G$E8\x02\x04]<U$W8\x01\x00ND\x11\x00\x00\x00\x01\x01LB\x0f\x00\x00\x00\x01\x05G<\x05\x00\x00\x00\x00\x04C>\x07\x03\x00\x00\x00\x04R>\x07\x03\x00\x00\x00\x06DA\x05\x05\x00\x00\x00\x06SA\x05\x05\x00\x00\x00\x07FB\x02\x03\x00\x00\x00\x07UB\x02\x03\x00\x00\x00\x08EL\x12\x03\x00\x00\x00\tGL\x02\x02\x00\x00\x00\tSL\x02\x02\x00\x00',
        b'\x00\x00*T\x0e$\x00\x00\x00\x00dT\x0e$\x00\x00\x01\x001z\x08\x00\x00\x00\x01\x00kz\x08\x00\x00\x00\x00\x008P,,\x00\x00\x00\x018P&(\x00\x00\x00\x02<T\x0c\x14\x00\x00\x00\x03>|\x0c\x08\x00\x00\x00\x03R|\x0c\x08\x00\x00\x01\x00NB\x12\x00\x00\x00\x01\x01L@\x10\x00\x00\x00\x01\x02F:\x06\x00\x00\x00\x00\x03B;\x08\x02\x00\x00\x00\x03R;\x08\x02\x00\x00\x00\x04D>\x05\x04\x00\x00\x00\x04S>\x05\x04\x00\x00\x00\x03EI\x12\x04\x00\x00\x00\x05FI\x03\x02\x00\x00\x00\x05SI\x03\x02\x00\x00\x00\x06B0\x0e\x05\x00\x00\x01\x03@\\\x04\x00\x00\x00\x00\x02>Y\x02\x01\x00\x00\x01\x03Vf\x04\x00\x00\x00\x00\x02Tc\x02\x01\x00\x00\x01\x03Hp\x04\x00\x00\x00\x00\x02Fm\x02\x01\x00\x00\x01\x03ZV\x04\x00\x00\x00\x00\x02XS\x02\x01\x00\x00\x00\x03PX\x01\n\x00\x00\x00\x03Pa\x07\x01\x00\x00',
        b'\x02\x003HiH\\~\x02\x003H\\~Nl\x02\x003HNl@~\x02\x019HaHVv\x02\x019HVvNh\x02\x019HNhDv\x02\x02>JPJHl\x02\x034r:\x82@r\x02\x03@rF\x82Lr\x02\x03LrR\x82Xr\x02\x03Xr^\x82dr\x01\x00ND\x11\x00\x00\x00\x01\x01LB\x0f\x00\x00\x00\x01\x02G<\x05\x00\x00\x00\x00\x04C>\x08\t\x00\x00\x00\x04Q>\x08\t\x00\x00\x00\x05EA\x04\x04\x00\x00\x00\x05SA\x04\x04\x00\x00\x00\x04HL\x0c\x06\x00\x00\x01\x02p:\x03\x00\x00\x00\x01\x02,X\x02\x00\x00\x00',
        b'\x00\x00*T\x0e$\x00\x00\x00\x00dT\x0e$\x00\x00\x01\x001z\x08\x00\x00\x00\x01\x00kz\x08\x00\x00\x00\x00\x008P,,\x00\x00\x00\x018P&(\x00\x00\x00\x02<T\x0c\x14\x00\x00\x00\x03>|\x0c\x08\x00\x00\x00\x03R|\x0c\x08\x00\x00\x01\x00NB\x12\x00\x00\x00\x01\x01L@\x10\x00\x00\x00\x01\x02F:\x06\x00\x00\x00\x00\x03B;\x08\x02\x00\x00\x00\x03R;\x08\x02\x00\x00\x02\x04@48"F2\x02\x04\\4d"V2\x02\x05@4<(F2\x02\x05\\4`(V2\x01\x06NF\n\x00\x00\x00\x00\x07D>\x05\x05\x00\x00\x00\x07S>\x05\x05\x00\x00\x00\x08E?\x02\x02\x00\x00\x00\x08T?\x02\x02\x00\x00\x00\tFJ\x10\x04\x00\x00\x00\x08GJ\x02\x03\x00\x00\x00\x08SJ\x02\x03\x00\x00\x00\x06:t\x04\x06\x00\x00\x00\x06<X\x03\x06\x00\x00\x00\x06Bt\x04\x06\x00\x00\x00\x06DX\x03\x06\x00\x00\x00\x06Jt\x04\x06\x00\x00\x00\x06LX\x03\x06\x00\x00\x00\x06Rt\x04\x06\x00\x00\x00\x06TX\x03\x06\x00\x00\x00\x06Zt\x04\x06\x00\x00\x00\x06\\X\x03\x06\x00\x00',
        b'\x00\x00:l\x0e\x16\x00\x00\x00\x00Tl\x0e\x16\x00\x00\x00\x01<l\n\x14\x00\x00\x00\x01Vl\n\x14\x00\x00\x01\x00,Z\n\x00\x00\x00\x00\x00&Z\x0c\x1e\x00\x00\x01\x00pZ\n\x00\x00\x00\x00\x00jZ\x0c\x1e\x00\x00\x01\x00,x\t\x00\x00\x00\x01\x00px\t\x00\x00\x00\x01\x01,X\x08\x00\x00\x00\x01\x01pX\x08\x00\x00\x00\x01\x01+v\x06\x00\x00\x00\x01\x01ov\x06\x00\x00\x00\x01\x00NZ\x1a\x00\x00\x00\x01\x01LX\x17\x00\x00\x00\x01\x02DP\x08\x00\x00\x00\x01\x00N8\x0f\x00\x00\x00\x01\x01M7\r\x00\x00\x00\x01\x02H2\x04\x00\x00\x00\x02\x074J86>H\x02\x07^Hd6hJ\x02\x066H86:H\x02\x06bHd6eH\x00\x08B2\x18\x04\x00\x00\x00\x03E7\x06\x04\x00\x00\x00\x03R7\x06\x04\x00\x00\x00\x04H@\x0c\x02\x00\x00\x00\x04DR\x02\x0c\x00\x00\x00\x04D\\\n\x02\x00\x00\x00\x04N\\\x02\n\x00\x00\x00\x04VN\x02\x08\x00\x00\x00\x04VN\x08\x02\x00\x00\x00\x03ES\x01\n\x00\x00\x00\x03O]\x01\x08\x00\x00\x01\x03NX\x04\x00\x00\x00\x01\x06NX\x02\x00\x00\x00\x01\x01$0\x04\x00\x00\x00\x01\x01x6\x03\x00\x00\x00\x01\x02#/\x01\x00\x00\x00')
MONP = (b'B`$\xe6\x8c\x96_<\x1e}U-<(\x14\xe6\xb4(n\xa0<\xa0\xc1\x80(<\x14\xfa\xdc<\x00\x00\x00<\x14\x14\xff\xff\xffP2\x19Z<\x1e',
        b'$H`<x\xa0\x8a\xae\xc6\xf0\xc8<\x00\x00\x00\xff\xff\xff\x180@\xa7\xc2\xd4',
        b'\xaa\x1e\x14\xf0n\x1e\xfa\xc8<\xfa\xdc<n\x14\x14\xfa\xb4P\xff\xf0x\x00\x00\x00Z\n\n\xff\xff\xff',
        b'HB6xnZ\xa7\xa0\x930,$\xfa\xaa(\xff\xff\xffP\x8c<',
        b'Z\x8c\xc8\x96\xc8\xf0\xe1\xf0\xff\xff\xff\xff\x14\x1eFx\xdc\xff',
        b'\x8d\x8d\x93\xeb\xeb\xf5\xf2\xf2\xf8^^b\x96\x96\xa5nn}\xbe\xd2\xeb<\x96\xe6\xff\xff\xff<\x1e2',
        b'PKF\x82zp\xaa\xa2\x96\xfa\xc8<\xf5\x8c\x1e\x00\x00\x00\xeb\xeb\xf0\xbe\xc3\xcd2.*')
# END ART

# monster: name, hp, attack, xp, colour, element
FOES = ((("Goblin", 14, 4, 6, (110, 160, 60), 3), ("Bog Toad", 16, 4, 7, (60, 120, 160), 1)),
        (("Lava Imp", 26, 7, 12, (240, 120, 30), 0), ("Rock Troll", 32, 7, 14, (120, 110, 90), 2)),
        (("Ice Wraith", 34, 9, 16, (150, 200, 240), 1), ("Snow Yeti", 42, 9, 18, (235, 235, 245), 3)))
LVL = ((1, 3), (3, 6), (6, 10), (1, 1))  # monster levels in each land
BOSS = ("Shadow Wyrm", 110, 12, 0, (90, 50, 140), 3)
DREAD = ("Dread Drake", 70, 11, 30, (40, 35, 45), 3)
TITAN = ("Stone Titan", 100, 13, 45, (230, 180, 60), 3)
CAVE = [0]  # 1 while the hidden cave is open (you own a Quantum and the Titan is not beaten)


def beats(a, b):
    return (a == 3 and b != 3) or (a < 3 and b == (a + 2) % 3)


def egg_type(m, up=0):
    # most eggs are common; rare ones are very rare. Further lands are much luckier.
    # Green Valley: legendary 0.4%, epic 2.6%, rare 8%, uncommon 22%, common 67%
    # Fire Mountain: 1%, 4%, 13%, 27%, 55%. Frost Peaks: 1.5%, 6.5%, 18%, 31%, 43%
    r = random.randint(0, 999)
    c = ((4, 30, 110, 330), (10, 50, 180, 450), (15, 80, 260, 570))[min(m, 2)]
    rar = 4 if r < c[0] else 3 if r < c[1] else 2 if r < c[2] else 1 if r < c[3] else 0
    rar = min(4, rar + up)
    return random.choice([i for i in range(20) if DT[i][2] == rar])


# ---------- pictures ----------
def art(b, x, y, s, P, out=None, f=0):
    for i in range(0, len(b), 8):
        c = P[b[i + 1]]
        a1, a2, a3, a4, a5, a6 = b[i + 2], b[i + 3], b[i + 4], b[i + 5], b[i + 6], b[i + 7]
        if out is not None:
            # small map picture: keep the shapes in order, round them, skip specks
            # f: mirror it (f is the picture width) so the dragon faces right
            k = b[i]
            if k == 0:
                if a3 * s < 0.8 or a4 * s < 0.8:
                    continue
                w = int(a3 * s + 0.5)
                a = (int(x + a1 * s + 0.5), int(y + a2 * s + 0.5), w, int(a4 * s + 0.5))
                if f:
                    a = (2 * x + f - a[0] - w,) + a[1:]
            elif k == 1:
                if a3 * s < 0.8:
                    continue
                a = (int(x + a1 * s + 0.5), int(y + a2 * s + 0.5), int(a3 * s + 0.5))
                if f:
                    a = (2 * x + f - a[0],) + a[1:]
            else:
                a = ([int(x + v * s + 0.5) for v in (a1, a3, a5)], [int(y + v * s + 0.5) for v in (a2, a4, a6)])
                if f:
                    a = ([2 * x + f - v for v in a[0]], a[1])
            out.append((10 + len(out), c, min(k, 2), a))
        elif b[i] == 0:
            rect(x + a1 * s, y + a2 * s, a3 * s, a4 * s, c)
        elif b[i] == 1:
            circ(x + a1 * s, y + a2 * s, a3 * s, c)
        else:
            col(c)
            fill_poly([x + a1 * s, x + a3 * s, x + a5 * s], [y + a2 * s, y + a4 * s, y + a6 * s])


def drag(x, y, s, t, c, head=0, body=0, out=None, f=0, sp=0):
    # a dragon facing left, about 58 x 50 times s pixels, top left at x, y
    # (with out, the shapes go into that list for the map instead of being drawn; sp: shiny scheme)
    P = PAL + [lt(c, 0.45), dk(c, 0.6), c] + PAL2 + [lt(c, 0.2), dk(c, 0.4)] + PAL3
    if sp:
        # shiny: every marking turns into a scheme colour that stands out from the body:
        # very bright -> light; colourful bits (flames, glows, gems) -> accent; whitish -> light;
        # near black -> very dark; the rest light or dark by whether it was lighter or darker
        # than the dragon's own colour. So each kind keeps its own pattern in the new colours.
        bl = (c[0] * 3 + c[1] * 6 + c[2]) // 10
        n, c, l, k, a = SCH[sp]
        Q = [dk(k, 0.5), P[1]]
        for q in P[2:]:
            v = (q[0] * 3 + q[1] * 6 + q[2]) // 10
            Q.append(l if v > 200 else a if max(q) - min(q) > 110 else l if v > 165 else dk(k, 0.5) if v < 40 else l if v > bl else k)
        P = Q
        # the body itself is always the main colour, light on top and dark underneath
        P[15], P[16], P[17], P[24], P[25] = l, k, c, l, k
        if t == 21:
            # Petralith: pebbles in the main colour with light tops, crystals in the accent
            P[2], P[5], P[6], P[19] = l, c, l, a
    w, b = ARTW[2 * t], ARTW[2 * t + 1]
    r = DT[t][2] if t < len(DT) else 0
    for a in (ARTB, ARTF[t], ARTU[r], bytes((2, w, 24, 26, 40, 10, 37, 28, 2, b, 40, 10, 28, 27, 30, 27, 2, b, 40, 10, 33, 28, 35, 28,
              2, 17, 23, 26, 40, 9, 26, 26, 1, 17, 26, 27, 3, 0, 0, 0, 2, 1, 40, 9, 42, 7, 41, 11)), ARTL, ARTT[r], ARTO[t],
              ARTG[body] if body else b"", ARTG[head] if head else b"",
              # shiny sparkles: three little white stars on the body and wing
              bytes((0, 1, 17, 31, 5, 1, 0, 0, 0, 1, 19, 29, 1, 5, 0, 0, 0, 1, 34, 14, 5, 1, 0, 0,
                     0, 1, 36, 12, 1, 5, 0, 0, 0, 1, 41, 32, 5, 1, 0, 0, 0, 1, 43, 30, 1, 5, 0, 0)) if sp else b""):
        art(a, x, y, s, P, out, f)


def oval(x, y, s, c, k=0):
    # an egg shape centred on x, y; k shrinks it (negative k grows it)
    circ(x, y + 2 * s, 7 * s - k, c)
    circ(x, y - 2 * s, 6 * s - k, c)
    circ(x, y - 5 * s, 4 * s - k, c)


def egg(x, y, s, t):
    # a shaded egg; its pattern shows how rare it is. Small eggs are smaller, shiny ones shine.
    q, t = t // 32, t % 32
    if t == SMALL:
        s = max(2, s * 2 // 3)
        y += 2 * s
        t = 0
    r = DT[t][2]
    shell = ((245, 235, 210), (225, 240, 205), (215, 230, 250), (235, 215, 250), (30, 30, 70), (20, 20, 45), (125, 118, 110))[r]
    if q:
        shell = SCH[q][2]
    oval(x, y, s, BLACK, -1)
    oval(x, y, s, dk(shell, 0.7))
    oval(x - s, y - s, s, shell, 2 * s)
    if r == 4:
        # Lumora: a night sky with yellow stars and a moon
        for dx, dy, n in ((-3, -4, 1), (3, 3, 1), (-2, 5, 0), (-1, -7, 0), (-5, 1, 0), (4, -5, 0)):
            rect(x + (dx - n) * s, y + dy * s, (2 * n + 1) * s, s, YELLOW)
            rect(x + dx * s, y + (dy - n) * s, s, (2 * n + 1) * s, YELLOW)
        circ(x + s, y - s, 2 * s, (250, 230, 140))
        circ(x + 2 * s, y - 2 * s, 2 * s, shell)
    elif r > 4:
        # Quantum: black and night blue with glowing violet cracks; Petralith: stone with gold cracks
        m = (35, 40, 110) if r == 5 else (90, 84, 78)
        circ(x + 2 * s, y + 4 * s, 4 * s, m)
        circ(x - 3 * s, y + 1 * s, 2 * s, m)
        Z = (-1, -8, 2, -4, -2, -1, 2, 2, -1, 5, 1, 8)
        for c, w in (((110, 50, 180), s + 1), ((210, 150, 255), max(1, s // 2))) if r == 5 else (((245, 140, 30), s + 1), ((250, 220, 60), max(1, s // 2))):
            col(c)
            for i in range(0, 10, 2):
                ax, ay, bx, by = x + Z[i] * s, y + Z[i + 1] * s, x + Z[i + 2] * s, y + Z[i + 3] * s
                fill_poly([ax - w, ax + w, bx + w, bx - w], [ay, ay, by, by])
        rect(x - 5 * s, y - 3 * s, s, s, c)
        rect(x + 4 * s, y - 6 * s, s, s, c)
    else:
        sp = SCH[q][3] if q else ((190, 150, 100), (90, 170, 80), (60, 120, 230), (150, 80, 220))[r]
        if r >= 2:
            # a zig-zag band
            for i in range(-5, 5, 2):
                rect(x + i * s, y + (i % 4 == 1) * s, 2 * s, 2 * s, sp)
        for dx, dy in ((-3, -5), (2, -3), (-2, 5), (3, 5), (-5, 2))[:3 + r]:
            rect(x + dx * s, y + dy * s, 2 * s, 2 * s, sp)
    circ(x - 3 * s, y - 5 * s, s + 1, WHITE)


def base(m, ch):
    if ch == "~":
        return WATER
    if ch == "L":
        return LAVA
    if ch == '"':
        return TALL[m]
    if ch == "=":
        return (190, 160, 110)
    return GROUND[m]


def shapes(m, x, y, ch, out):
    px = x * T
    py = 20 + y * T
    if ch == "T":
        out.append((0, BARK, 0, (px + 8, py + 14, 4, 6)))
        out.append((1, LEAF, 1, (px + 10, py + 8, 8)))
    elif ch == "~":
        out.append((0, (110, 160, 235), 0, (px + (x * 5 + y * 3) % 8, py + 8, 6, 1)))
    elif ch == "L":
        out.append((0, (250, 200, 60), 0, (px + (x * 7 + y * 5) % 12, py + 6, 5, 3)))
    elif ch == '"':
        c = GROUND[m]
        for o in (3, 9, 15):
            out.append((0, c, 0, (px + o, py + 6 + o % 4, 2, 8)))
    elif ch in "^C":
        out.append((0, ROCK, 2, ([px, px + 10, px + 20], [py + 20, py + 1, py + 20])))
        out.append((1, WHITE, 2, ([px + 6, px + 10, px + 14], [py + 8, py + 1, py + 8])))
        if ch == "C" and CAVE[0]:
            out.append((2, (20, 18, 25), 1, (px + 10, py + 17, 5)))
            out.append((3, YELLOW, 0, (px + 8, py + 9, 5, 1)))
    elif ch in "QS":
        # a little house: walls, roof, door and a sign (! for quests, a coin for the shop)
        out.append((0, (235, 215, 170), 0, (px + 3, py + 9, 14, 11)))
        out.append((1, (200, 50, 40) if ch == "Q" else (50, 90, 200), 2, ([px, px + 10, px + 20], [py + 10, py, py + 10])))
        out.append((2, BARK, 0, (px + 8, py + 13, 4, 7)))
        if ch == "Q":
            out.append((3, YELLOW, 0, (px + 9, py + 3, 2, 4)))
            out.append((3, YELLOW, 0, (px + 9, py + 8, 2, 1)))
        else:
            out.append((3, YELLOW, 1, (px + 10, py + 5, 2)))
    elif ch == "M":
        out.append((0, (70, 45, 95), 2, ([px + 3, px + 10, px + 17], [py + 19, py + 2, py + 19])))
        out.append((1, (15, 10, 20), 1, (px + 10, py + 8, 3)))
        out.append((1, (150, 105, 55), 1, (px + 16, py + 15, 3)))
        out.append((2, YELLOW, 0, (px + 8, py + 7, 1, 1)))
        out.append((2, YELLOW, 0, (px + 11, py + 7, 1, 1)))
    elif ch == "O":
        # Officer Brick: blue coat, cap and a gold badge
        out.append((0, (40, 60, 150), 0, (px + 5, py + 9, 10, 10)))
        out.append((1, (240, 200, 160), 1, (px + 10, py + 6, 3)))
        out.append((2, (20, 30, 80), 0, (px + 6, py + 1, 8, 3)))
        out.append((2, YELLOW, 0, (px + 7, py + 11, 2, 2)))
    elif ch == "X":
        # a treasure chest from Shen's map
        out.append((0, BARK, 0, (px + 3, py + 8, 14, 10)))
        out.append((1, YELLOW, 0, (px + 3, py + 11, 14, 2)))
        out.append((1, YELLOW, 0, (px + 9, py + 10, 2, 4)))
    elif ch == "W":
        out.append((0, ROCK, 1, (px + 10, py + 11, 8)))
        out.append((1, WATER, 1, (px + 10, py + 11, 5)))
    elif ch == "H":
        out.append((0, BARK, 1, (px + 10, py + 12, 9)))
        out.append((1, (60, 40, 20), 1, (px + 10, py + 12, 6)))
        out.append((2, (245, 235, 210), 1, (px + 7, py + 12, 3)))
        out.append((2, (245, 235, 210), 1, (px + 13, py + 11, 3)))
        out.append((3, (200, 160, 90), 0, (px + 1, py + 15, 18, 2)))
    elif ch == "E":
        v = EGGS.get((m, x, y), 0)
        q, k = v // 32, v % 32
        r = DT[k % SMALL][2]
        sh = SCH[q][2] if q else (25, 25, 35) if r == 4 else CYAN if r == 5 else ROCK if r == 6 else (245, 235, 210)
        sp = SCH[q][3] if q else MAG if r == 5 else YELLOW if r >= 4 else RCOL[r] if r else (200, 170, 120)
        out.append((0, BARK, 0, (px + 3, py + 15, 14, 4)))
        out.append((1, sh, 1, (px + 10, py + 10, 4 if k == SMALL else 6)))
        out.append((2, sp, 0, (px + 7, py + 8, 3, 3)))
        out.append((2, sp, 0, (px + 11, py + 12, 3, 3)))
    elif ch == "B":
        out.append((0, (40, 30, 60), 1, (px + 10, py + 10, 9)))
        out.append((1, BOSS[4], 1, (px + 10, py + 10, 6)))
        out.append((2, (255, 60, 60), 0, (px + 6, py + 8, 3, 3)))
        out.append((2, (255, 60, 60), 0, (px + 11, py + 8, 3, 3)))


EGGS = {}  # (land, x, y): the egg lying there (see egg_roll)
# Shiny colour schemes: (name, main, light, dark, accent). An egg number is kind + 32 * scheme;
# kind 31 is a small egg, which hatches a baby of a kind you have discovered.
SCH = (None, ("Silver", (190, 195, 205), (240, 242, 248), (105, 110, 125), (80, 170, 255)),
       ("Gold", (235, 185, 40), (255, 235, 130), (150, 100, 20), (255, 110, 30)),
       ("Neon", (40, 255, 140), (240, 255, 60), (255, 40, 220), (40, 230, 255)),
       ("Purple-blue", (130, 60, 210), (70, 150, 255), (40, 30, 120), (160, 235, 255)))
SMALL = 31


def egg_roll(g, t):
    # 1 in 20 eggs is small (once you have a dragon kind in your book). Any egg, small too,
    # is shiny 1 time in 50: silver 40%, gold 30%, neon 20%, purple-blue 10%
    if g.book & 0x1FFFFF and random.random() < 0.05:
        t = SMALL
    if random.random() < 0.02:
        r = random.random()
        return t + 32 * (1 if r < 0.4 else 2 if r < 0.7 else 3 if r < 0.9 else 4)
    return t


def kids(g):
    # how full the pen is, in quarters: a dragon or a big egg takes 4, a baby or a small egg 1
    return sum(1 if d[9] & 8 else 4 for d in g.pen) + sum(1 if e % 32 == SMALL else 4 for e in g.bag)


def grown(g):
    # the first grown-up dragon (babies can't be partners)
    for d in g.pen:
        if not d[9] & 8:
            return d
    return None


def el(d):
    return DT[d[1]][1]


def hero(g, out):
    px = g.x * T
    py = 20 + g.y * T
    d = g.ride
    if d is not None:
        # the dragon's own detailed picture, small, with you on its back
        # g.face: 1 when you last flew right, so the dragon turns that way
        r = g.face
        out.append((8, (60, 120, 230), 0, (px + (9 if r else 8), py + 5, 3, 5)))
        out.append((9, (240, 200, 160), 1, (px + (10 if r else 9), py + 3, 2)))
        drag(px, py + 2, 0.34, d[1], d[6], d[7], d[8], out, 20 if r else 0, d[9] & 7)
        return
    out.append((5, (240, 200, 160), 1, (px + 10, py + 5, 4)))
    out.append((6, BARK, 0, (px + 6, py + 1, 8, 3)))
    out.append((6, (60, 120, 230), 0, (px + 6, py + 9, 8, 7)))
    out.append((6, (60, 40, 30), 0, (px + 6, py + 16, 3, 4)))
    out.append((6, (60, 40, 30), 0, (px + 11, py + 16, 3, 4)))


def paint(ops):
    # rectangles of one colour that touch side by side become one
    ops.sort(key=lambda o: (o[0], o[1], o[2], o[3][1] if o[2] == 0 else 0, o[3][0]))
    last = None
    for layer, c, kind, a in ops:
        if kind == 0:
            if last and last[0] == (layer, c) and last[2] == a[1] and last[4] == a[3] and last[1] + last[3] == a[0]:
                last[3] += a[2]
                continue
            if last:
                rect(last[1], last[2], last[3], last[4], last[0][1])
            last = [(layer, c), a[0], a[1], a[2], a[3]]
            continue
        if last:
            rect(last[1], last[2], last[3], last[4], last[0][1])
            last = None
        if kind == 1:
            circ(a[0], a[1], a[2], c)
        else:
            col(c)
            fill_poly(a[0], a[1])
    if last:
        rect(last[1], last[2], last[3], last[4], last[0][1])


def cells(g, todo, with_hero):
    mp = g.maps[g.m]
    ops = []
    rows = {}
    for x, y in todo:
        rows.setdefault(y, []).append(x)
    for y in rows:
        xs = sorted(rows[y])
        i = 0
        while i < len(xs):
            c = base(g.m, mp[y][xs[i]])
            j = i + 1
            while j < len(xs) and xs[j] == xs[j - 1] + 1 and base(g.m, mp[y][xs[j]]) == c:
                j += 1
            ops.append((-1, c, 0, (xs[i] * T, 20 + y * T, (j - i) * T, T)))
            i = j
    for x, y in todo:
        shapes(g.m, x, y, mp[y][x], ops)
    if with_hero:
        hero(g, ops)
    paint(ops)


def draw_map(g, after_msg=False):
    # after a message box, only the rows it covered are drawn again
    r0, r1 = 0, 9
    if after_msg:
        r0 = max(0, (MSG[0] - 20) // T)
        r1 = min(9, (MSG[0] + MSG[1] - 20) // T + 1)
    else:
        cls()
        HUD[0] = None
    CAVE[0] = not g.book >> 26 & 1 and any(d[1] == 20 and not d[9] & 8 for d in g.pen)
    cells(g, [(x, y) for y in range(r0, r1) for x in range(16)], r0 <= g.y < r1)
    hud(g)


HUD = [None]


def hud(g):
    d = g.ride
    if d is not None:
        who = d[0] + " " + str(d[3]) + "/" + str(d[4])
    else:
        who = "You " + str(g.hp) + "/" + str(g.mhp)
    t = (LANDS[g.m], who, ("Egg " + str(g.warm)) if g.bag else str(g.coins) + "c")
    if t == HUD[0]:
        return
    old = HUD[0] or ("", "", "")
    if HUD[0] is None:
        rect(0, 0, 320, 20, BLACK)
    for i, x, c in ((0, 4, GOLD), (1, 140, WHITE), (2, 262, YELLOW)):
        if t[i] != old[i]:
            text(x, 15, old[i], BLACK)
            text(x, 15, t[i], c)
    HUD[0] = t


class Game:
    pass


def bar(x, y, w, v, mx, c):
    f = max(0, min(w, int(w * v / mx))) if v > 0 else 0
    if v > 0:
        f = max(2, f)
    rect(x, y, f, 6, c)
    rect(x + f, y, w - f, 6, DARK)


def foe_art(f):
    n = f[0]
    if f is BOSS or f is DREAD:
        drag(162, 42, 2, 22 if f is DREAD else 8, f[4])
    else:
        k = ([m[0] for l in FOES for m in l] + [TITAN[0]]).index(n)
        art(MONA[k], 142, 12, 1, cl(MONP[k]))


def foe_screen(f, title):
    cls()
    rbox(150, 30, 140, 120, 10, RED if f is DREAD else f[4], 2, NIGHT)
    foe_art(f)
    ctext(24, title, GOLD)


def battle(g, f, lv=0):
    # returns True when the monster is beaten, 2 when you got away, False
    # when you died. lv: the monster's level (each level past its land's lowest adds
    # 4 HP, 1 attack and 3 XP); bosses have no level.
    name, fhp, fat, xp, fc, fe = f
    up = lv - LVL[g.m][0] if lv else 0
    fhp, fat, xp = fhp + 4 * up, fat + up, xp + 3 * up
    who = ("Lv " + str(lv) + " " if lv else "") + name
    mx = fhp
    foe_screen(f, who + " appears!")
    log = ""
    sel = 0
    was = None
    while True:
        d = g.ride
        opts = ("Claw", "Breath", "Run") if d is not None else ("Sword", "Run")
        n = len(opts)
        w = 300 // n
        sel = min(sel, n - 1)
        now = (d[0] if d else "You", d[3] if d else g.hp, fhp, sel, log, n)
        if was is None or was[0] != now[0]:
            rect(0, 40, 148, 60, BLACK)
            rect(0, 150, 320, 34, BLACK)
            text(12, 56, now[0], d[6] if d and d[1] != 19 else WHITE)
            text(12, 86, name[:12], RED if f is DREAD else fc)
            for i in range(n):
                cc = GOLD if i == sel else WHITE
                rbox(10 + i * w, 154, w - 6, 24, 8, cc)
                text(10 + i * w + (w - 6) // 2 - len(opts[i]) * 5, 172, opts[i], cc)
            was = None
        if was is None or was[1] != now[1]:
            bar(12, 62, 120, now[1], d[4] if d else g.mhp, GREEN)
        if was is None or was[2] != fhp:
            bar(12, 92, 120, fhp, mx, RED)
        if was is not None and was[3] != sel:
            for i in (was[3], sel):
                cc = GOLD if i == sel else WHITE
                edge(10 + i * w, 154, w - 6, 24, 8, cc)
                text(10 + i * w + (w - 6) // 2 - len(opts[i]) * 5, 172, opts[i], cc)
        if was is None or was[4] != log:
            rect(0, 186, 320, 24, BLACK)
            text(6, 202, log[:31], GREY)
        was = now
        k = wkey()
        if k in (LEFT, RIGHT):
            sel = (sel + (1 if k == RIGHT else -1)) % n
            continue
        if k != OK:
            continue
        o = opts[sel]
        if o == "Run":
            if f is BOSS:
                log = "The Wyrm blocks your way!"
                continue
            if random.random() < 0.6:
                return 2
            log = "Couldn't get away."
        elif o == "Sword":
            dm = random.randint(3, 5)
            fhp -= dm
            log = "Sword hits for " + str(dm) + "."
        else:
            # the secret dragons hit harder: Quantum claw 18-21, breath 21-25 at level 1;
            # Petralith claw 21-25, breath 25-30
            q = (d[1] == 20) + 2 * (d[1] == 21)
            at = 5 + 2 * d[2] + 2 * DT[d[1]][2] + q
            if o == "Claw":
                dm = at + random.randint(0, 2 + q)
                log = "Claw hits for " + str(dm) + "."
            else:
                dm = at + random.randint(2 + q, 5 + 2 * q)
                if beats(el(d), fe):
                    dm *= 2
                    log = "Super breath! " + str(dm) + "."
                elif beats(fe, el(d)):
                    dm //= 2
                    log = "Weak breath... " + str(dm) + "."
                else:
                    log = "Breath hits for " + str(dm) + "."
            fhp -= dm
        if fhp <= 0:
            msg = []
            for dd in g.pen:
                if dd[3] > 0 and (dd is d or dd is g.pick):
                    dd[5] += xp
                    while dd[5] >= dd[2] * 10:
                        dd[5] -= dd[2] * 10
                        dd[2] += 1
                        dd[4] += 6
                        dd[3] = dd[4]
                        msg.append(dd[0] + " is now level " + str(dd[2]) + "!")
            if lv >= 5:
                # strong monsters drop coins (twice as many with the Golden Coin,
                # but only for its first 15 wins; its bad side never wears off)
                k = g.curse and g.cd < 15
                g.cd += k
                c = lv * (1 + k)
                g.coins += c
                msg = ["+" + str(c) + " coins!"] + msg
            message(msg[:3] or ["You won!"], who + " beaten")
            if f is not BOSS:
                quest_step(g, 0, name)
                quest_step(g, 2, g.m)
            return True
        dm = max(1, fat + random.randint(0, 3) - (d[2] if d else 0))
        log += " It hits " + str(dm) + "."
        if d is not None:
            d[3] = max(0, d[3] - dm)
            if d[3] == 0:
                g.ride = None
                message([d[0] + " is too tired to fly.", "You fight on foot!"], "Oh no")
                foe_screen(f, who)
                was = None
        else:
            g.hp -= dm
            if g.hp <= 0:
                cls()
                ctext(60, "YOU DIED", RED)
                message(["The " + name + " won.", "Back to your last save."], "Game over")
                return False


def rest(g):
    g.hp = g.mhp
    g.ride = None
    for d in g.pen:
        d[3] = d[4]


# ---------- saving: lists DRG (grown dragons) and DRB (babies) ----------
# DRG: [4, coins, accessories owned, species in the book, steps until the Dread Drake returns,
#  eggs in the bag (up to 5, -1 = none), then 5 numbers a dragon: name (letters 1-26 in base 27),
#  kind, level, xp, shiny*4000+paint*200+head*20+body]
# DRB: [2, things from the merchant (Glimmer Stones + 100 * Lucky Charm + 200 * Golden Coin
#  + 400 * things bought from him, up to 10, + 4400 * quests finished, up to 99,
#  + 500000 * which grown dragon is your partner + 6000000 * Golden Coin wins used, up to 15),
#  then 2 numbers a baby: name, kind + 32 * shiny]  (version 1 had no second number)
def pack(nm):
    n = 0
    for ch in nm.upper():
        n = n * 27 + ABC.index(ch) + 1
    return n


def unpack(n):
    nm = ""
    while n:
        nm = ABC[n % 27 - 1] + nm
        n //= 27
    return nm[0] + nm[1:].lower()


def save(g):
    q = g.pol
    if q:
        x = q[0][9]
        q[0][9] = x & 8 | q[1]
    s = [4, g.coins, g.own, g.book, g.dread] + (g.bag + [-1] * 5)[:5]
    big = [d for d in g.pen if not d[9] & 8]
    pk = ([i for i in range(len(big)) if big[i] is g.pick] + [0])[0]
    b = [2, g.glim + 100 * g.luck + 200 * g.curse + 400 * min(10, g.buys) + 4400 * min(99, g.done) + 500000 * pk + 6000000 * min(15, g.cd) + 96000000 * g.sad + 192000000 * (g.book >> 31 & 1) * min(100, max(0, g.shn) // 100)]
    for d in g.pen:
        if d[9] & 8:
            b += [pack(d[0]), d[1] + 32 * (d[9] & 7)]
            continue
        p = PAINT.index(d[6]) + 1 if d[6] in PAINT and d[6] != DT[d[1]][3] else 0
        s += [pack(d[0]), d[1], d[2], d[5], (d[9] & 7) * 4000 + p * 200 + d[7] * 20 + d[8]]
    if q:
        q[0][9] = x
    try:
        from ti_system import store_list
        store_list("DRG", s)
        store_list("DRB", b)
    except Exception:
        pass


def load(g):
    # a new game first (this lives here, in a swap file, to keep the main file small)
    g.maps = [[list(r) for r in mp] for mp in MAPS]
    EGGS.clear()
    for m in range(3):
        for y in range(9):
            for x in range(16):
                if MAPS[m][y][x] == "E":
                    EGGS[(m, x, y)] = random.randint(0, 6) if m == 0 else egg_type(m)
    g.m, g.x, g.y = 0, 3, 2
    g.hp = g.mhp = 30
    g.pen = []
    g.bag = []
    g.warm = 12
    g.spawn = 100
    g.pick = g.ride = g.quest = g.pol = g.shen = None
    g.coins = g.own = g.book = g.seen = g.face = g.dread = g.glim = g.luck = g.curse = g.buys = g.done = g.cd = g.sad = 0
    g.shn = random.randint(120, 180)
    try:
        from ti_system import recall_list
        s = [int(v) for v in recall_list("DRG")]
    except Exception:
        return
    if len(s) < 9 or s[0] not in (2, 3, 4):
        return
    v = s[0]
    k = min(1, v - 2)
    pk = 0
    g.coins, g.own, g.book = s[1], s[2], s[3]
    if k:
        g.dread = s[4]
    g.bag = [e for e in s[4 + k:9 + k] if e >= 0]
    w = 5 if v > 3 else 4
    for i in range(9 + k, len(s) - w + 1, w):
        if v > 3:
            # the name is packed as letters 1-26 in base 27
            nm = unpack(s[i])
            i += 1
            t = s[i]
        else:
            nm, t = NAMES[s[i] // 32], s[i] % 32
        lv = s[i + 1]
        mh = 20 + 6 * min(4, DT[t][2]) + 6 * (lv - 1) + 6 * (t == 20) + 16 * (t == 21)
        x = s[i + 3] % 4000
        p = x // 200
        g.pen.append([nm, t, lv, mh, mh, s[i + 2], PAINT[p - 1] if p else DT[t][3], x // 20 % 10, x % 20, s[i + 3] // 4000])
    try:
        b = [int(v) for v in recall_list("DRB")]
        if b[0] > 1:
            pk = b[1] // 500000 % 12
            g.cd = b[1] // 6000000 % 16
            g.sad = b[1] // 96000000 % 2
            g.shn = max(g.shn, b[1] // 192000000 * 100)
            b[1] %= 500000
            g.glim, g.luck, g.curse, g.buys, g.done = b[1] % 100, b[1] // 100 % 2, b[1] // 200 % 2, b[1] // 400 % 11, b[1] // 4400
            b = b[1:]
        for i in range(1, len(b) - 1, 2):
            t = b[i + 1] % 32
            g.pen.append([unpack(b[i]), t, 1, 10, 10, 0, DT[t][3], 0, 0, 8 + b[i + 1] // 32])
    except Exception:
        pass
    big = [d for d in g.pen if not d[9] & 8]
    g.pick = big[pk] if pk < len(big) else grown(g)
    g.warm = 12


# ---------- quests ----------
def new_quest(g):
    # quests get harder the more you finish (up to level 10), and harder ones pay more
    t = min(10, g.done)
    m = 1 + 0.3 * t
    k = random.randint(0, 2)
    if k == 0:
        n = random.randint(2, 4) + t // 2
        land = random.randint(min(g.seen, t // 3), g.seen)
        nm = random.choice(FOES[land])[0]
        return [0, nm, n, 0, int((8 * n + 6 * land) * m), "Beat " + str(n) + " " + nm + "s"]
    if k == 1:
        n = 1 + t // 3
        return [1, None, n, 0, int(20 * n * m), "Hatch " + (str(n) + " eggs" if n > 1 else "an egg")]
    land = random.randint(min(g.seen, t // 3), g.seen)
    n = random.randint(3, 5) + t // 2
    return [2, land, n, 0, int((7 * n + 6 * land) * m), str(n) + " wins: " + LANDS[land]]


def quest_step(g, kind, what):
    q = g.quest
    if q is None or q[0] != kind or (q[1] is not None and q[1] != what):
        return
    q[3] += 1
    if q[3] >= q[2]:
        g.coins += q[4]
        g.quest = None
        g.done += 1
        message(["You finished:", q[5], "+" + str(q[4]) + " coins!"], "Quest done!")


def board(g):
    if g.quest is not None:
        q = g.quest
        c = choose(q[5] + " " + str(q[3]) + "/" + str(q[2]), ["Keep going", "Give up quest"])
        if c == 1:
            g.quest = None
        return
    qs = [new_quest(g) for i in range(3)]
    c = lst("Quests (level " + str(min(10, g.done) + 1) + ")", [q[5] + "  " + str(q[4]) + "c" for q in qs] + ["Not now"])
    if 0 <= c < 3:
        g.quest = qs[c]


# ---------- the nest ----------
def portrait(d):
    cls(NIGHT)
    if d[9] & 8:
        drag(131, 45, 1, d[1], d[6], d[7], d[8], None, 0, d[9] & 7)
    else:
        drag(102, 10, 2, d[1], d[6], d[7], d[8], None, 0, d[9] & 7)


def pen(g):
    # 9 dragons a page; babies take a quarter of a space each
    pg = 0
    while g.pen:
        k = kids(g)
        top = pg * 9
        sh = g.pen[top:top + 9]
        opts = [("> " if d is g.pick else "") + d[0] + (" baby" if d[9] & 8 else " L" + str(d[2])) + " " + DT[d[1]][0] for d in sh]
        more = len(g.pen) > 9
        c = lst("Pen " + str(k // 4) + ("", ".25", ".5", ".75")[k % 4] + "/10", opts + (["More..."] if more else []) + ["Back"])
        if more and c == len(sh):
            pg = pg + 1 if (pg + 1) * 9 < len(g.pen) else 0
            continue
        if c < 0 or c >= len(sh):
            return
        d = sh[c]
        b = d[9] & 8
        a = choose(d[0] + " the " + ("baby " if b else "") + DT[d[1]][0], ["Pick as partner", "See " + d[0], "Let it go free", "Back"])
        if a == 0 and b:
            message([d[0] + " is too little to", "ride or fight. Babies", "just live in your pen."], "Baby")
        elif a == 0:
            g.pick = d
            if g.ride is not None:
                g.ride = d
            message([d[0] + " is your partner now!"], "Partner")
        elif a == 1:
            t = DT[d[1]]
            portrait(d)
            q = d[9] & 7
            # the facts go under the picture, so nothing covers the dragon
            ctext(122, d[0], GOLD)
            ctext(142, (SCH[q][0] + " " if q else "") + t[0])
            ctext(160, RARE[t[2]] + "  " + ENAME[t[1]] + " element")
            ctext(178, "A baby" if b else "Level " + str(d[2]) + "  HP " + str(d[4]))
            ctext(200, "ENTER: back", GREY)
            while wkey() not in (OK, CLR):
                pass
        elif a == 2 and choose("Free " + d[0] + " forever?", ["No, keep " + d[0], "Yes, let it go"]) == 1:
            g.pen.remove(d)
            if g.pick is d:
                g.pick = grown(g)
            if g.ride is d:
                g.ride = g.pick
            message([d[0] + " flies away. Bye!"], "Free")


def lst(title, opts):
    # a list with small rows, for up to 11 choices; -1 for CLEAR
    cls()
    ctext(24, title, GOLD)
    n = len(opts)
    h = 15 if n > 9 else 17
    sel = old = 0
    for i in range(n):
        text(30, 50 + i * h, opts[i], GOLD if i == 0 else WHITE)
    while True:
        if sel != old:
            for i in (old, sel):
                rect(0, 50 + i * h - 16, 320, h, BLACK)
                text(30, 50 + i * h, opts[i], GOLD if i == sel else WHITE)
        rect(14, 50 + sel * h - 10, 8, 6, GOLD)
        k = wkey()
        old = sel
        if k == UP:
            sel = (sel - 1) % n
        elif k == DOWN:
            sel = (sel + 1) % n
        elif k == OK:
            return sel
        elif k == CLR:
            return -1


def dress(g, d, first):
    # pick one of the accessories you own for the head (1-8) or body (9-16)
    ids = [i for i in range(first, first + 8) if g.own >> i & 1]
    if not ids:
        message(["Buy one in the shop first."], "Nothing to wear")
        return
    c = lst("Wear on " + ("head" if first == 1 else "body"), [GEAR[i][0] for i in ids] + ["Nothing"])
    if c < 0:
        return
    v = ids[c] if c < len(ids) else 0
    if first == 1:
        d[7] = v
    else:
        d[8] = v
    portrait(d)
    message([d[0] + " looks great!"], "Dressed up")


def shop(g):
    while True:
        d = g.pick
        c = choose(d[0] + ": " + str(g.coins) + " coins", ["Buy accessories", "Head: " + (GEAR[d[7]][0] or "nothing"),
                                                           "Body: " + (GEAR[d[8]][0] or "nothing"), "Paint it 20c", "Back"])
        if c == 0:
            f = choose("Buy for the", ["Head", "Body", "Back"])
            if f not in (0, 1):
                continue
            f = 1 + 8 * f
            opts = [GEAR[i][0] + (" (have)" if g.own >> i & 1 else " " + str(GEAR[i][1]) + "c") for i in range(f, f + 8)]
            i = lst(str(g.coins) + " coins", opts + ["Back"])
            i = f + i if 0 <= i < 8 else 0
            if i and not g.own >> i & 1:
                if g.coins < GEAR[i][1]:
                    message(["You need " + str(GEAR[i][1]) + " coins.", "Do quests to earn more."], "Not enough")
                else:
                    g.coins -= GEAR[i][1]
                    g.own |= 1 << i
                    message([GEAR[i][0] + " is in your bag."], "Bought!")
        elif c in (1, 2):
            dress(g, d, 1 if c == 1 else 9)
        elif c == 3 and d[9] & 7:
            message(["Shiny dragons keep", "their special colours."], "Paint")
        elif c == 3:
            if g.coins < 20:
                message(["You need 20 coins."], "Not enough")
                continue
            p = lst("Pick a colour", list(PAINTN))
            if p >= 0:
                g.coins -= 20
                d[6] = PAINT[p]
                portrait(d)
                message([d[0] + " looks great!"], "Painted")
        else:
            return


def who(g, title, babies=True):
    # pick one of your dragons (10 to a page); None for Back
    L = [d for d in g.pen if babies or not d[9] & 8]
    pg = 0
    while L:
        sh = L[pg:pg + 9]
        more = len(L) > 9
        c = zl(title, [d[0] + " " + DT[d[1]][0] for d in sh] + (["More..."] if more else []) + ["Back"])
        if more and c == len(sh):
            pg = pg + 9 if pg + 9 < len(L) else 0
            continue
        return sh[c] if 0 <= c < len(sh) else None
    message(["You need a dragon first."], "Hm")
    return None


def glim(g):
    # 1 stone: a random shiny; 5 stones: you pick the colour
    d = who(g, "Make shiny (" + str(g.glim) + " stones)")
    if d is None:
        return
    q = 0
    if g.glim >= 5:
        c = choose("Glimmer Stones: " + str(g.glim), ["Random (1 stone)", "Pick colour (5)", "Back"])
        if c == 1:
            q = choose("Which shiny?", [SCH[i][0] for i in range(1, 5)]) + 1
            if q < 1:
                return
            g.glim -= 5
        elif c != 0:
            return
    if not q:
        g.glim -= 1
        q = random.randint(1, 4)
    if g.pol and g.pol[0] is d:
        g.pol = None
    d[9] = d[9] & 8 | q
    d[6] = DT[d[1]][3]
    cls(NIGHT)
    drag(102, 10, 2, d[1], d[6], d[7], d[8], None, 0, q) if not d[9] & 8 else drag(131, 45, 1, d[1], d[6], 0, 0, None, 0, q)
    message([d[0] + " sparkles!", "Now a " + SCH[q][0] + " " + DT[d[1]][0] + "!"], "Shiny!")
    save(g)


def zl(title, opts):
    # a list like lst(), kept in the merchant's own file. Long lists show
    # 10 rows a page and turn the page when you move past the end.
    cls()
    ctext(24, title, GOLD)
    n = len(opts)
    h = 15 if n > 9 else 17
    sel = old = 0
    top = -1
    while True:
        t = sel // 10 * 10
        if t != top:
            top = t
            rect(0, 32, 320, 178, BLACK)
            for i in range(top, min(n, top + 10)):
                text(30, 50 + (i - top) * h, opts[i], GOLD if i == sel else WHITE)
            if n > 10:
                text(6, 206, "More: keep going (" + str(top // 10 + 1) + "/" + str((n + 9) // 10) + ")", GREY)
        elif sel != old:
            for i in (old, sel):
                # same words in a new colour, so no clearing (it would clip the rows next to it)
                y = 50 + (i - top) * h
                if i == old:
                    rect(14, y - 10, 8, 6, BLACK)
                text(30, y, opts[i], GOLD if i == sel else WHITE)
        rect(14, 50 + (sel - top) * h - 10, 8, 6, GOLD)
        k = wkey()
        old = sel
        if k == UP:
            sel = (sel - 1) % n
        elif k == DOWN:
            sel = (sel + 1) % n
        elif k == OK:
            return sel
        elif k == CLR:
            return -1


def pol_off(g):
    # the Shiny Polish wears off
    d = g.pol[0]
    d[9] = d[9] & 8 | g.pol[1]
    g.pol = None
    if d in g.pen:
        message([d[0] + "'s shine", "wore off..."], "Hm")
        draw_map(g, True)


def cop(g):
    # Officer Brick comes once: turn Shen in (an Epic egg and 300 coins, but Shen is gone
    # for good) or keep quiet (Shen gives you one free thing next time)
    cls(NIGHT)
    rect(125, 105, 70, 72, (40, 60, 150))
    circ(160, 80, 26, (240, 200, 160))
    rect(130, 50, 60, 16, (20, 30, 80))
    rect(124, 64, 72, 5, (20, 30, 80))
    rect(150, 120, 10, 12, YELLOW)
    rect(148, 78, 6, 4, BLACK)
    rect(166, 78, 6, 4, BLACK)
    ctext(24, "OFFICER BRICK", GOLD)
    ctext(196, "Excuse me, tamer!")
    while wkey() not in (OK, CLR):
        pass
    message(["Have you seen a shady", "merchant? Hood, yellow", "eyes, sells fake stuff?"], "Officer Brick")
    g.book |= 1 << 30
    if choose("Tell on Shen?", ["Turn him in", "Never seen him"]) == 0:
        g.book |= 1 << 31
        g.coins += 300
        t = random.choice([i for i in range(20) if DT[i][2] == 3])
        if len(g.bag) < 5 and kids(g) + 4 <= 40:
            g.bag.append(t)
            m = "It's in your backpack."
        else:
            put_egg(g, t, True)
            m = "I'll leave it by you."
        message(["Got him! He'll be locked", "up for a long time. Here's", "300 coins and an Epic egg."], "Officer Brick")
        message([m], "Officer Brick")
    else:
        g.book |= 1 << 22
        message(["Hmm. Well, tell me", "if you see him."], "Officer Brick")
    shen_off(g)
    # if you told, Shen sits in jail for about 10000 steps, then comes back with double prices forever
    if g.book >> 31 & 1:
        g.shn = 10000


def shen(g):
    # Shady Shen. The game never tells you, but: after your first visit he sometimes
    # picks your pocket, after your first buy 1 thing in 10 is a fake, and the
    # Golden Coin makes coins go missing more often (book bit 27 = met, 28 = bought)
    m, x, y = g.shen
    if g.maps[m][y][x] == "O":
        return cop(g)
    met = g.book >> 27 & 1
    g.book |= 1 << 27
    if met and random.random() < 0.25 + 0.25 * g.curse:
        g.coins -= min(g.coins, random.randint(2, 6) * (1 + g.curse))
    cls(NIGHT)
    col((70, 45, 95))
    fill_poly([110, 160, 210], [200, 40, 200])
    circ(160, 95, 22, (15, 10, 20))
    rect(148, 90, 6, 4, YELLOW)
    rect(166, 90, 6, 4, YELLOW)
    circ(222, 170, 20, (150, 105, 55))
    rect(214, 150, 16, 4, (110, 75, 40))
    ctext(24, "SHADY SHEN", GOLD)
    mad = g.book >> 31 & 1
    ctext(196, random.choice(("You! You told on me!", "Prices went up. Wonder why.", "I remember you, snitch.")) if mad else random.choice(("Psst... over here.", "Rare goods. Very real.", "Don't ask where I got these.",
                              "Best prices in all the lands.", "You look like a smart tamer.",
                              "Nice dragon. Shame if it got sparkly.")))
    while wkey() not in (OK, CLR):
        pass
    # you didn't tell Officer Brick about him (book bit 22): one thing for free
    free = g.book >> 22 & 1
    if free:
        message(["Psst... you didn't tell", "the officer about me.", "Pick one thing. Free."], "Shady Shen")
    while True:
        # his best customers (10 things bought) see one more item
        S = (("Glimmer Stone", 60), ("Power Fruit", 40), ("Mystery Egg", 50), ("Healing Tonic", 20), ("Lucky Charm", 35),
             ("Mystery Box", 30), ("Egg Swap", 25), ("Golden Coin", 45), ("Accessory Crate", 40), ("Treasure Map", 35),
             ("Dragon Insurance", 20), ("Speed Saddle", 50), ("Shiny Polish", 25), ("Moldy Egg", 15)) + ((("Glimmer Pack x5", 250),) if g.buys >= 10 else ())
        # since you told on him, everything costs double
        S = [(n, p * (1 + mad)) for n, p in S]
        z = len(S)
        c = zl("Pick 1 thing for FREE!" if free else "Shady Shen   " + str(g.coins) + " coins", [n + (" - sold out" if n == "Moldy Egg" and g.book >> 29 & 1 else " " + str(p) + "c") for n, p in S] +
                (["Use Glimmer Stones (" + str(g.glim) + ")"] if g.glim else []) + ["Leave"])
        if c == z and g.glim:
            glim(g)
            continue
        if c < 0 or c >= z:
            message([random.choice(("No refunds. Ever.", "You didn't see me.", "Come back soon, friend."))], "Shady Shen")
            return
        n, p = S[c]
        p *= 1 - free
        if g.coins < p:
            message(["That's " + str(p) + " coins, friend.", "Come back richer."], "Shady Shen")
            continue
        d = None
        if c == 1:
            d = who(g, "Feed the Power Fruit to", False)
            if d is None:
                continue
        if c == 13 and g.book >> 29 & 1:
            message(["All gone. Heh.", "Should've bought more", "when you had the chance."], "Shady Shen")
            continue
        if c in (2, 13) and (len(g.bag) >= 5 or kids(g) + 4 > 40):
            message(["No room for an egg."], "Shady Shen")
            continue
        if c == 6:
            if not g.bag:
                message(["You have no eggs to swap."], "Shady Shen")
                continue
            e = zl("Swap which egg?", ["Egg " + str(i + 1) for i in range(len(g.bag))] + ["Back"])
            if not 0 <= e < len(g.bag):
                continue
        if c == 7 and g.curse or c == 11 and g.sad:
            message(["You already have one.", "One is plenty. Heh."], "Shady Shen")
            continue
        if c == 12:
            d = who(g, "Polish which dragon?")
            if d is None:
                continue
        g.coins -= p
        # (the Moldy Egg, his secret good deal, is never a fake)
        if not free and c != 13 and g.book >> 28 & 1 and random.random() < 0.1:
            message([random.choice(("It was just a painted rock!", "The box was empty...", "It crumbled into dust.",
                                    "It melted in your hand."))], "Huh?")
            continue
        g.book = g.book & ~(1 << 22) | 1 << 28
        free = 0
        g.buys += 1
        if g.buys == 10:
            message(["Psst... you're my best", "customer. Next time I'll", "have something special."], "Shady Shen")
        if n == "Glimmer Pack x5":
            c = 0
            g.glim += 4
        box = c == 5
        if box:
            # the Mystery Box: something from his bag, or nothing at all
            c = random.choice((0, 1, 3, 4, 8, 20, 20, 21))
            d = grown(g) if c == 1 else None
            if c == 1 and d is None:
                c = 20
        if c == 0:
            g.glim += 1
            m = ["Glimmer Stones: " + str(g.glim), "Use 1 for a random shiny,", "or 5 to pick the colour."]
        elif c == 1:
            d[2] += 1
            d[4] += 6
            d[3] = d[4]
            m = [d[0] + " ate the Power Fruit.", d[0] + " is now level " + str(d[2]) + "!"]
        elif c == 2:
            g.bag.append(egg_roll(g, random.randint(0, 19)))
            m = ["A Mystery Egg!", "It's in your backpack."]
        elif c == 3:
            g.hp = g.mhp
            for dd in g.pen:
                dd[3] = dd[4]
            m = ["Everyone feels great!"]
        elif c == 4:
            g.luck = 1
            g.spawn = min(g.spawn, 40)
            m = ["You feel lucky.", "Your next egg will", "be a rare one!"]
        elif c == 6:
            g.bag[e] = egg_roll(g, egg_type(g.m))
            m = ["Swapped! A brand new", "egg is in your backpack."]
        elif c == 7:
            g.curse = 1
            m = ["A Golden Coin! Double", "coins from fights.", "Lucky you. Heh heh."]
        elif c == 8:
            # the Accessory Crate: any of the 16, even one you already have
            i = random.randint(1, 16)
            if g.own >> i & 1:
                m = ["A " + GEAR[i][0] + "... but you", "already have one.", "No refunds. Heh."]
            else:
                g.own |= 1 << i
                m = ["A " + GEAR[i][0] + "!", "Put it on at the", "village shop."]
        elif c == 9:
            # the Treasure Map: a chest turns up in this land; 1 in 3 is empty
            if put_egg(g, 0, False, "X"):
                m = ["X marks the spot!", "Look for a chest", "somewhere in this land."]
            else:
                m = ["The map is all smudged.", "Can't read it. Oh well."]
        elif c == 10:
            # Dragon Insurance does absolutely nothing
            m = ["Your dragons are now", "fully insured. Trust me.", "I'll take care of it."]
        elif c == 11:
            # the Speed Saddle: no faster at all, but monsters find a riding tamer more often
            g.sad = 1
            m = ["A Speed Saddle! Your", "dragon flies faster now.", "Zoom zoom. Heh."]
        elif c == 12:
            # Shiny Polish: looks shiny for a while, then it wears off (it never saves)
            if g.pol:
                g.pol[0][9] = g.pol[0][9] & 8 | g.pol[1]
            g.pol = [d, d[9] & 7, random.randint(80, 140)]
            d[9] = d[9] & 8 | random.randint(1, 4)
            m = [d[0] + " sparkles!", "So shiny. Totally", "real. Heh heh."]
        elif c == 13:
            # looks rotten, but it's always an Epic or Legendary egg. Only one, ever.
            g.book |= 1 << 29
            g.bag.append(random.choice([i for i in range(20) if DT[i][2] >= 3]))
            m = ["A Moldy Egg. Ew.", "It's probably rotten.", "No refunds. Heh."]
        elif c == 20:
            m = ["The box was empty.", "Just air. Heh."]
        else:
            n = random.randint(10, 60)
            g.coins += n
            m = [str(n) + " coins inside!"]
        message(m, "Mystery Box" if box else n)


def nest(g):
    rest(g)
    save(g)
    while True:
        c = choose("The Nest (saved)", ["Dragon pen", "Backpack and book", "Leave the nest"] + (["Glimmer Stones: " + str(g.glim)] if g.glim else []))
        if c == 3:
            return 3
        elif c == 0:
            pen(g)
        elif c == 1:
            # play() shows these, so the nest's code can leave memory first
            k = choose("Look at your", ["Backpack", "Dragon book"])
            if k >= 0:
                return k + 1
        else:
            save(g)
            return 0


def backpack(g):
    cls(NIGHT)
    ctext(22, "BACKPACK", GOLD)
    if not g.bag:
        ctext(100, "No eggs. Go and find some!")
    for i in range(len(g.bag)):
        v = g.bag[i]
        egg(40 + i * 60, 90, 3, v)
        r = DT[v % 32 % SMALL][2]
        text(16 + i * 60, 150, "Small" if v % 32 == SMALL else "Shiny" if v > 31 else "???" if r > 4 else RARE[r][:5],
             SCH[v // 32][2] if v > 31 else WHITE if v % 32 == SMALL else RCOL[r])
    if g.glim:
        text(6, 170, "Glimmer Stones: " + str(g.glim) + " (ENTER: use)", GOLD)
    if g.bag:
        text(6, 188, "The first egg hatches in " + str(g.warm), WHITE)
    n = len([i for i in range(1, 17) if g.own >> i & 1])
    text(6, 206, "Accessories: " + str(n) + " of 16", GREY)
    # True: use the Glimmer Stones (play() does it, after this file leaves memory)
    while True:
        k = wkey()
        if k == CLR or k == OK and not g.glim:
            return False
        if k == OK:
            return True


def book(g):
    # one page a species; a page fills in once you have hatched that kind.
    # The secret page only exists after you have hatched the secret dragon.
    P = list(range(20)) + [k for k in (20, 21) if g.book >> k & 1]
    n = len(P)
    i = 0
    while True:
        cls(NIGHT)
        t = DT[P[i]]
        got = g.book >> P[i] & 1
        ctext(22, "DRAGON BOOK  " + str(i + 1) + "/" + str(n), GOLD)
        if got:
            drag(102, 30, 2, P[i], t[3])
            ctext(150, t[0], WHITE)
            ctext(172, RARE[t[2]] + " " + ENAME[t[1]], RCOL[t[2]])
        else:
            oval(160, 90, 4, (30, 32, 55))
            ctext(98, "?", GREY)
            ctext(150, "???", GREY)
            ctext(172, "Not found yet", GREY)
        f = len([k for k in range(20) if g.book >> k & 1])
        text(6, 204, "Found " + str(f) + " of 20   Left/Right", GREY)
        k = wkey()
        if k in (LEFT, RIGHT):
            i = (i + (1 if k == RIGHT else -1)) % n
        elif k in (OK, CLR):
            return


def frame(b, c):
    x, y, w, h = b
    rect(x, y, w, 2, c)
    rect(x, y + h - 2, w, 2, c)
    rect(x, y, 2, h, c)
    rect(x + w - 2, y, 2, h, c)


def kbox(i):
    # where item i of the letter keyboard sits: 26 letters, Delete, Done
    if i < 26:
        return 26 + (i % 13) * 20, 92 + (i // 13) * 30, 18, 24
    return (52, 160, 80, 26) if i == 26 else (188, 160, 80, 26)


def typed(kind):
    # type a name (up to 8 letters) with the arrows and ENTER
    cls()
    ctext(24, "Name your " + kind, GOLD)
    frame((60, 38, 200, 30), WHITE)
    for r in range(2):
        text(30, 110 + r * 30, " ".join(ABC[r * 13:r * 13 + 13]), WHITE)
    text(62, 179, "Delete", WHITE)
    text(208, 179, "Done", WHITE)
    text(6, 204, "ENTER: pick  DEL: erase", GREY)
    nm = ""
    sel = old = 0
    frame(kbox(0), GOLD)
    while True:
        k = wkey()
        old = sel
        if k == LEFT:
            sel = (sel - 1) % 28
        elif k == RIGHT:
            sel = (sel + 1) % 28
        elif k == UP:
            sel = sel - 13 if 13 <= sel < 26 else (13 if sel == 26 else 20) if sel > 25 else sel + 13
        elif k == DOWN:
            sel = sel + 13 if sel < 13 else (26 if sel < 19 else 27) if sel < 26 else sel - 13
        elif k == CLR:
            return ""
        elif k == DEL or (k == OK and sel == 26):
            nm = nm[:-1]
        elif k == OK and sel == 27:
            if nm:
                return nm
        elif k == OK and len(nm) < 8:
            nm += ABC[sel] if not nm else ABC[sel].lower()
        if k in (OK, DEL):
            rect(64, 42, 192, 22, BLACK)
            text(70, 62, nm + ("_" if len(nm) < 8 else ""), WHITE)
        if sel != old:
            frame(kbox(old), BLACK)
            frame(kbox(sel), GOLD)


def hatch(g):
    v = g.bag.pop(0)
    g.warm = 12
    q, e = v // 32, v % 32
    b = e == SMALL
    if b:
        # a baby of a kind you have discovered
        e = random.choice([i for i in range(22) if g.book >> i & 1] or [0])
    t = DT[e]
    cls(NIGHT)
    ctext(24, "The egg is cracking!", GOLD)
    egg(160, 110, 5, v)
    pause(0.6)
    # cracks spread, then a flash, then the dragon
    col(WHITE if t[2] > 3 else (70, 45, 30))
    C = (160, 74, 152, 88, 152, 88, 162, 100, 162, 100, 154, 114, 170, 86, 176, 100, 176, 100, 168, 112)
    for i in range(0, 20, 4):
        a1, b1, a2, b2 = C[i:i + 4]
        fill_poly([a1 - 2, a1 + 2, a2 + 2, a2 - 2], [b1, b1, b2, b2])
        pause(0.25)
    cls((255, 248, 215))
    if b:
        drag(102, 55, 2, e, t[3], 0, 0, None, 0, q)
    else:
        drag(73, 30, 3, e, t[3], 0, 0, None, 0, q)
    rect(0, 182, 320, 28, NIGHT)
    ctext(200, "A baby " + (SCH[q][0] + " " if q else "") + t[0] + "!" if b else (SCH[q][0] + " " if q else "" if t[2] > 4 else RARE[t[2]] + " ") + t[0] + " dragon!",
          SCH[q][2] if q else RCOL[t[2]])
    pause(1.2)
    names = sample(NAMES, 4)
    i = choose("Name your " + t[0] + ":", names + ["Type a name"])
    nm = names[max(0, i)] if i < 4 else typed(t[0]) or names[0]
    mh = 20 + 6 * min(4, t[2]) + 6 * (e == 20) + 16 * (e == 21)
    d = [nm, e, 1, mh, mh, 0, t[3], 0, 0, q + 8 * b]
    g.pen.append(d)
    msg = [nm + " joins your pen!"]
    if not g.book >> e & 1:
        g.book |= 1 << e
        msg.append("New page in your book!")
    if g.pick is None and not b:
        g.pick = d
        msg += ["Press ENTER to ride.", "Dragons fly over water,", "lava and mountains."]
    draw_map(g)
    message(msg, t[0])
    quest_step(g, 1, None)
    draw_map(g, True)


def menu(g):
    # ENTER on the map: ride or get off your partner, look in your things, or save
    d = g.pick
    opts = ["Backpack", "Dragon book", "My quest", "Save game", "Keep exploring"]
    if d is None:
        c = choose("Dragon Tamer", opts)
        c = c + 1 if c >= 0 else 5
    else:
        if g.ride is not None:
            first = "Get off " + d[0]
        else:
            first = "Ride " + d[0] + ("" if d[3] > 0 else " (tired)")
        c = choose(d[0] + " the " + DT[d[1]][0], [first] + opts)
    if c == 3:
        q = g.quest
        draw_map(g)
        if q is None:
            message(["You have no quest.", "Visit the quest hall", "in the village."], "My quest")
        else:
            message([q[5], "Done: " + str(q[3]) + " of " + str(q[2]), "Reward: " + str(q[4]) + " coins"], "My quest")
        draw_map(g, True)
        return 0
    if c == 4:
        save(g)
        draw_map(g)
        message(["Your dragons, coins and", "eggs are saved."], "Saved!")
        draw_map(g, True)
        return 0
    if c == 0:
        if g.ride is not None:
            if g.maps[g.m][g.y][g.x] in "~L^":
                draw_map(g)
                message(["You can't get off here!"])
                draw_map(g, True)
                return 0
            g.ride = None
        elif d[3] == 0:
            draw_map(g)
            message([d[0] + " is too tired.", "Rest at the nest first."])
            draw_map(g, True)
            return 0
        else:
            g.ride = d
    elif c in (1, 2):
        return c
    draw_map(g)
    return 0


def shen_off(g):
    # the merchant leaves (when you leave the land or his time is up)
    if g.shen:
        m, x, y = g.shen
        if g.maps[m][y][x] in "MO":
            g.maps[m][y][x] = "."
            if m == g.m:
                cells(g, [(x, y)], False)
        g.shen = None
        g.shn = random.randint(120, 180)


def put_egg(g, t, near, ch="E"):
    # an egg turns up on an empty spot (next to you when near is set); ch "M" puts the merchant there
    mp = g.maps[g.m]
    for n in range(30):
        if near:
            x = g.x + random.randint(-1, 1)
            y = g.y + random.randint(-1, 1)
        else:
            x = random.randint(1, 14)
            y = random.randint(1, 7)
        if 0 <= x < 16 and 0 <= y < 9 and mp[y][x] in '."' and (x, y) != (g.x, g.y) and (near or abs(x - g.x) + abs(y - g.y) > 3):
            mp[y][x] = ch
            if ch == "E":
                EGGS[(g.m, x, y)] = t
            elif ch in "MO":
                g.shen = (g.m, x, y)
            cells(g, [(x, y)], False)
            return True
    return False


def evil(g):
    # the evil dragon swoops in; beat it and it leaves a strange egg (the
    # game never says what is inside)
    cls()
    ctext(90, "The sky goes dark...", RED)
    pause(0.8)
    r = battle(g, DREAD)
    if not r:
        return False
    draw_map(g)
    if r == 2:
        # you got away, so no egg, and it hunts you again soon
        g.dread = random.randint(900, 1100)
        message(["You got away...", "but the Dread Drake", "will be back!"], "Escaped")
        draw_map(g, True)
        return True
    # beaten: it never comes back (remembered in the book's spare bit 25)
    g.dread = 0
    g.book |= 1 << 25
    if not put_egg(g, 20, True) and len(g.bag) < 5:
        g.bag.append(20)
    message(["The Dread Drake flies", "away... and leaves a", "strange egg behind!"], "Whoa!")
    draw_map(g, True)
    return True


def titan(g):
    # the hidden cave: a giant of living rock guards a stone egg. Running away is fine,
    # it waits in its cave; beat it once (book bit 26) and it leaves the egg
    draw_map(g)
    message(["A cave! Letters are", "carved over the door:", "P E T R A"], "Hidden cave")
    cls()
    ctext(90, "The ground shakes...", GOLD)
    pause(0.8)
    r = battle(g, TITAN)
    if not r:
        return False
    if r == 2:
        draw_map(g)
        message(["You ran out of the cave.", "The Stone Titan waits..."], "Escaped")
        draw_map(g, True)
        return True
    g.book |= 1 << 26
    draw_map(g)
    if not put_egg(g, 21, True) and len(g.bag) < 5:
        g.bag.append(21)
    message(["The Stone Titan crumbles", "... and an egg of stone", "rolls out!"], "Whoa!")
    draw_map(g, True)
    return True


def win(g):
    cls()
    if g.pick:
        drag(73, 30, 3, g.pick[1], g.pick[6], g.pick[7], g.pick[8], None, 0, g.pick[9] & 7)
    message(["The Shadow Wyrm flies far", "away. Dragons return to", "every land. You did it!"], "THE END")
    rest(g)
    save(g)


def play():
    g = Game()
    load(g)
    steps = 0
    draw_map(g)
    if g.pen or g.bag:
        message(["Welcome back! You have", str(len(g.pen)) + " dragons, " + str(g.coins) + " coins."], "DRAGON TAMER")
    else:
        message(["The Shadow Wyrm scared", "the dragons away. Find", "eggs and raise a team!"], "DRAGON TAMER")
    draw_map(g, True)
    while True:
        k = wkey()
        if k == CLR:
            if message(["ENTER: save and quit", "CLEAR: keep going"], "Quit?") == OK:
                rest(g)
                save(g)
                return
            draw_map(g, True)
            continue
        if k in (OK, SECOND):
            c = menu(g)
            if c:
                if (backpack if c == 1 else book)(g) and c == 1:
                    glim(g)
                draw_map(g)
            continue
        dx, dy = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, -1), DOWN: (0, 1)}.get(k, (0, 0))
        if dx == 0 and dy == 0:
            continue
        nx, ny = g.x + dx, g.y + dy
        if dx:
            g.face = dx > 0
        if nx < 0 or nx > 15:
            # the village (land 3) sits left of Green Valley
            m = (0 if nx > 15 else -1) if g.m == 3 else g.m + (1 if nx > 15 else -1)
            if m < 0 and g.m == 0:
                m = 3
            if 0 <= m <= 3:
                ch = g.maps[m][ny][15 - g.x]
                if ch != "T" and (ch not in "~L^" or g.ride is not None):
                    if g.shen:
                        shen_off(g)
                    g.m = m
                    if m < 3:
                        g.seen = max(g.seen, m)
                    g.x = 15 - g.x
                    draw_map(g)
            continue
        if ny < 0 or ny > 8:
            continue
        mp = g.maps[g.m]
        ch = mp[ny][nx]
        if ch == "C" and CAVE[0]:
            if not titan(g):
                return
            continue
        if ch in "TW" or (ch in "~L^C" and g.ride is None):
            continue
        if ch == "B":
            if battle(g, BOSS):
                win(g)
                return
            if g.hp <= 0:
                return
            draw_map(g)
            continue
        if ch == "E" and (len(g.bag) >= 5 or kids(g) + (1 if EGGS.get((g.m, nx, ny), 0) % 32 == SMALL else 4) > 40):
            draw_map(g)
            message(["Your backpack is full."] if len(g.bag) >= 5 else ["No room in your pen.", "Let a dragon go first."], "Egg")
            draw_map(g, True)
            continue
        if ch in "MO":
            # talk to the merchant (or the officer) without stepping on him
            shen(g)
            # what you bought is saved right away
            save(g)
            draw_map(g)
            continue
        ox, oy = g.x, g.y
        g.x, g.y = nx, ny
        if ch == "E":
            mp[ny][nx] = "."
            cells(g, [(ox, oy), (nx, ny)], True)
            e = EGGS.pop((g.m, nx, ny), 0)
            if not g.bag:
                g.warm = 12
            g.bag.append(e)
            hud(g)
            message(["You found a" + (" shiny" if e > 31 else "") + " small egg!", "It's in your backpack."] if e % 32 == SMALL else
                    ["You found a" + (" shiny" if e > 31 else "n") + " egg with", RARE[DT[e % 32][2]] + " spots! It's in", "your backpack."], "An egg!")
            draw_map(g, True)
            continue
        if ch == "X":
            mp[ny][nx] = "."
            cells(g, [(ox, oy), (nx, ny)], True)
            if random.random() < 0.33:
                message(["You dig it open...", "It's empty! Just dirt."], "Treasure")
            else:
                n = random.randint(30, 80) + 20 * g.m
                g.coins += n
                hud(g)
                message(["You dig it open...", str(n) + " coins inside!"], "Treasure")
            draw_map(g, True)
            continue
        if ch == "Q":
            board(g)
            draw_map(g)
            continue
        if ch == "S":
            draw_map(g)
            if g.pick is None:
                message(["Hatch a dragon first!"], "Shop")
                draw_map(g, True)
            else:
                shop(g)
                draw_map(g)
            continue
        if ch == "H":
            while True:
                c = nest(g)
                if not c:
                    break
                if (backpack if c == 1 else book if c == 2 else glim)(g) and c == 1:
                    glim(g)
            draw_map(g)
            continue
        cells(g, [(ox, oy), (nx, ny)], True)
        if g.bag:
            g.warm -= 1
            if g.warm <= 0:
                hatch(g)
                continue
        g.spawn -= 1
        if g.spawn <= 0:
            g.spawn = random.randint(100, 200)
            # up to 2 eggs can wait in one land
            if g.m < 3 and sum(1 for q in EGGS if q[0] == g.m) < 2:
                put_egg(g, egg_roll(g, egg_type(g.m, g.luck)), False)
                g.luck = 0
        # the merchant turns up every 150 steps or so and stays for about 60
        g.shn -= 1
        if g.shen:
            if g.shn < 0:
                shen_off(g)
        # once you've met Shen, Officer Brick comes looking for him (book bit 30 = asked, 31 = told on Shen)
        elif g.shn <= 0 and g.m < 3 and put_egg(g, 0, False, "O" if g.book >> 27 & 1 and not g.book >> 30 & 1 and random.random() < 0.3 else "M"):
            g.shn = 60
        if g.curse and random.random() < 0.01:
            g.coins -= min(g.coins, random.randint(1, 3))
        if g.pol:
            g.pol[2] -= 1
            if g.pol[2] <= 0:
                pol_off(g)
        hud(g)
        steps += 1
        # the evil dragon only hunts tamers who own an Epic (or rarer) dragon
        if g.dread > 0:
            g.dread -= 1
        if g.m < 3 and (g.dread == 1 or not g.dread and steps > 3 and random.random() < EVIL) and not g.book >> 25 & 1 and \
                any(DT[d[1]][2] >= 3 for d in g.pen):
            steps = 0
            if not evil(g):
                return
            continue
        # monsters hide in the tall grass, and further lands have more of them
        sd = g.sad and g.ride is not None and g.m < 3
        if (ch == '"' or sd and random.random() < 0.3) and steps > 3 and random.random() < 0.2 + 0.08 * min(g.m, 2) + 0.1 * sd:
            steps = 0
            # a level in this land's range; higher levels are rarer
            lo, hi = LVL[g.m]
            if not battle(g, random.choice(FOES[g.m]), lo + min(hi - lo, int(random.random() ** 1.6 * (hi - lo + 1)))):
                return
            draw_map(g)


RULES = "Find eggs (new ones keep turning up), walk to hatch them and name your dragons. 20 kinds, Common to Legendary. Ride over water, lava and mountains. Save any time from the ENTER menu. The nest has your dragon pen. Walk left from Green Valley to the village for quests and the shop. If you lose all your HP, you die!"
KEYS = ["Arrows: walk or fly", "ENTER: ride, backpack, save", "Fights: Left/Right + ENTER", "CLEAR: save and quit"]


def main():
    while True:
        c = home("GHDRAGON", "DRAGON TAMER", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        play()
