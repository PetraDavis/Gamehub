# Dragon Tamer: explore three lands, find dragon eggs and hatch them, name
# your dragons, ride them over water, lava and mountains, and fight monsters.
# 20 kinds of dragon from Common to Legendary, a Dragon Book that fills in as
# you hatch them, and a very rare evil dragon with a secret egg. Saves your dragons, coins, accessories and the
# eggs in your backpack every time you visit the nest.
from GHLIB import *
import random

TEST = True       # the evil dragon shows up often, for testing
EVIL = 0.12 if TEST else 0.004

T = 20
# The calculator can't hold the whole game at once, so tools/bundle.py puts
# these functions in their own files. Each file is loaded when one of its
# functions is called and dropped from memory again when it returns.
SWAP = {"W": ("bar", "foe_art", "foe_screen", "battle", "evil"),
        "X": ("rest", "load", "new_quest", "board", "portrait", "pen", "lst", "dress", "shop", "nest",
              "menu", "win"),
        "Y": ("backpack", "book", "hatch", "oval", "egg")}
MAPS = (
    ["TTTTTTTTTTTTT~~~",
     'T.....""".....~~',
     'T.H...""""...~~~',
     'T.....""".T...~~',
     "T..........E.~~~",
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
     '..""".....^^....',
     "^^^^^^^^^^^^^^^^"],
)
LANDS = ("Green Valley", "Fire Mountain", "Frost Peaks")
GROUND = ((50, 130, 60), (85, 65, 55), (215, 225, 240))
TALL = ((35, 100, 45), (120, 90, 60), (170, 190, 220))
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
RARE = ("Common", "Uncommon", "Rare", "Epic", "Legendary", "Quantum")
def cl(b):
    # colours packed as bytes (r, g, b, r, g, b...): far fewer code words
    return [tuple(b[i:i + 3]) for i in range(0, len(b), 3)]


RCOL = cl(b'\xff\xff\xffx\xdcxZ\xa0\xff\xc8n\xf0\xe6\xb4(<\xe6\xe6')
# dragon kinds: name, element, rarity, colour. Each rarer level has fewer.
DT = list(zip(('Pyrrak', 'Smoldedrake', 'Aquawyrm', 'Gillwing', 'Fernling', 'Lichenwing', 'Stonewyrm', 'Volcanox', 'Ashveil', 'Glacius', 'Tempestra', 'Thornwyrm', 'Dawnwing', 'Pearlhorn', 'Jadewyrm', 'Petalwyrm', 'Blazequill', 'Abyssar', 'Rootwyrm', 'Lumora', 'Quantum'),
         b'\x00\x00\x01\x01\x02\x02\x02\x00\x00\x01\x01\x02\x00\x01\x02\x02\x00\x01\x02\x03\x03', b'\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x02\x02\x02\x02\x03\x03\x03\x04\x05', cl(b'\xdcF(\xeb\x8c(<\x82\xe6(\xaa\xaaF\xaaF\x82\x96<\x96\x8cx\xaa(\x1eKKU\xa0\xd2\xf5xd\xc8\x1en<\xf0\xbe(\xf0x\x96<\xc8\x96\xfa\xa0\xd2\xffZ<\x1e<\xa0nP(\x19\x19#\x19\x1eP')))
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
PAL3 = cl(b'F-\x14\xb4\x82\x14dix\xc8P\x96\x14\x8c\xa0\x14(x\xa0n<')

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
        b'\x00\x00"\x19\x07\n\x00\x00\x01\x00)\x1e\x05\x00\x00\x00\x02\x00)\x1a9\x1f)#\x02\x16\x12\x10\x19\n\x15\x12\x00\x16\x11\x18\x02\x06\x00\x00\x00\x16\x19\x1d\x08\x01\x00\x00\x00\x16 \x1d\x01\x03\x00\x00\x00\x16 \x1f\t\x01\x00\x00\x00\x16)\x1c\x01\x04\x00\x00\x00\x16.\x1d\x07\x01\x00\x00',
        b'\x02\x17\x1c\x19\x1e\x13 \x19\x02\x17+\x1b-\x150\x1c\x02\x171\x1d3\x186\x1e\x02\x17\x13\x14\x15\x0f\x18\x14\x00\x19\x18 \x13\x03\x00\x00\x00\x17\x11\x18\x02\x06\x00\x00')
ARTW = b'\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x05\x1c\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x0f\x10\x03\x02\x0f\x10\x0f\x10\x15\x00\x00\x12\x00\x17'
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
        b'\x00\x16\n\x15\x06\x01\x00\x00\x00\x16\r\x12\x02\x02\x00\x00',
        b'\x02\x00\x11\x11\x1c\x02\x16\x12\x02\x00\x0e\x10\x14\x04\x12\x11\x00\x17\x08\x17\x0b\x01\x00\x00\x00\x01\n\x17\x01\x02\x00\x00\x00\x01\r\x17\x01\x02\x00\x00\x00\x01\x10\x17\x01\x02\x00\x00\x00\x12\x0b\x11\x05\x04\x00\x00\x00\x16\x0c\x12\x03\x02\x00\x00\x00\x01\r\x12\x01\x01\x00\x00\x02\x00\x0b\x10\x11\x10\x11\x12')
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
        b'\x00\x00*T\x0e$\x00\x00\x00\x00dT\x0e$\x00\x00\x01\x001z\x08\x00\x00\x00\x01\x00kz\x08\x00\x00\x00\x00\x008P,,\x00\x00\x00\x018P&(\x00\x00\x00\x02<T\x0c\x14\x00\x00\x00\x03>|\x0c\x08\x00\x00\x00\x03R|\x0c\x08\x00\x00\x01\x00NB\x12\x00\x00\x00\x01\x01L@\x10\x00\x00\x00\x01\x02F:\x06\x00\x00\x00\x00\x03B;\x08\x02\x00\x00\x00\x03R;\x08\x02\x00\x00\x02\x04@48"F2\x02\x04\\4d"V2\x02\x05@4<(F2\x02\x05\\4`(V2\x01\x06NF\n\x00\x00\x00\x00\x07D>\x05\x05\x00\x00\x00\x07S>\x05\x05\x00\x00\x00\x08E?\x02\x02\x00\x00\x00\x08T?\x02\x02\x00\x00\x00\tFJ\x10\x04\x00\x00\x00\x08GJ\x02\x03\x00\x00\x00\x08SJ\x02\x03\x00\x00\x00\x06:t\x04\x06\x00\x00\x00\x06<X\x03\x06\x00\x00\x00\x06Bt\x04\x06\x00\x00\x00\x06DX\x03\x06\x00\x00\x00\x06Jt\x04\x06\x00\x00\x00\x06LX\x03\x06\x00\x00\x00\x06Rt\x04\x06\x00\x00\x00\x06TX\x03\x06\x00\x00\x00\x06Zt\x04\x06\x00\x00\x00\x06\\X\x03\x06\x00\x00')
MONP = (b'B`$\xe6\x8c\x96_<\x1e}U-<(\x14\xe6\xb4(n\xa0<\xa0\xc1\x80(<\x14\xfa\xdc<\x00\x00\x00<\x14\x14\xff\xff\xffP2\x19Z<\x1e',
        b'$H`<x\xa0\x8a\xae\xc6\xf0\xc8<\x00\x00\x00\xff\xff\xff\x180@\xa7\xc2\xd4',
        b'\xaa\x1e\x14\xf0n\x1e\xfa\xc8<\xfa\xdc<n\x14\x14\xfa\xb4P\xff\xf0x\x00\x00\x00Z\n\n\xff\xff\xff',
        b'HB6xnZ\xa7\xa0\x930,$\xfa\xaa(\xff\xff\xffP\x8c<',
        b'Z\x8c\xc8\x96\xc8\xf0\xe1\xf0\xff\xff\xff\xff\x14\x1eFx\xdc\xff',
        b'\x8d\x8d\x93\xeb\xeb\xf5\xf2\xf2\xf8^^b\x96\x96\xa5nn}\xbe\xd2\xeb<\x96\xe6\xff\xff\xff<\x1e2')
# END ART

# monster: name, hp, attack, xp, colour, element
FOES = ((("Goblin", 14, 4, 6, (110, 160, 60), 3), ("Bog Toad", 16, 4, 7, (60, 120, 160), 1)),
        (("Lava Imp", 26, 7, 12, (240, 120, 30), 0), ("Rock Troll", 32, 7, 14, (120, 110, 90), 2)),
        (("Ice Wraith", 34, 9, 16, (150, 200, 240), 1), ("Snow Yeti", 42, 9, 18, (235, 235, 245), 3)))
BOSS = ("Shadow Wyrm", 110, 12, 0, (90, 50, 140), 3)
DREAD = ("Dread Drake", 70, 11, 30, (40, 35, 45), 3)


def beats(a, b):
    return (a == 3 and b != 3) or (a < 3 and b == (a + 2) % 3)


def egg_type(m):
    # most eggs are common; the further you travel the luckier you get
    r = random.randint(0, 99) + m * 6
    rar = 4 if r >= 99 else 3 if r >= 92 else 2 if r >= 78 else 1 if r >= 52 else 0
    return random.choice([i for i in range(20) if DT[i][2] == rar])


# ---------- pictures ----------
def art(b, x, y, s, P):
    for i in range(0, len(b), 8):
        c = P[b[i + 1]]
        a1, a2, a3, a4, a5, a6 = b[i + 2], b[i + 3], b[i + 4], b[i + 5], b[i + 6], b[i + 7]
        if b[i] == 0:
            rect(x + a1 * s, y + a2 * s, a3 * s, a4 * s, c)
        elif b[i] == 1:
            circ(x + a1 * s, y + a2 * s, a3 * s, c)
        else:
            col(c)
            fill_poly([x + a1 * s, x + a3 * s, x + a5 * s], [y + a2 * s, y + a4 * s, y + a6 * s])


def drag(x, y, s, t, c, head=0, body=0):
    # a dragon facing left, about 58 x 50 times s pixels, top left at x, y
    P = PAL + [lt(c, 0.45), dk(c, 0.6), c] + PAL2 + [lt(c, 0.2), dk(c, 0.4)] + PAL3
    art(ARTB, x, y, s, P)
    art(ARTF[t], x, y, s, P)
    w, b = ARTW[2 * t], ARTW[2 * t + 1]
    art(bytes((2, w, 24, 26, 40, 10, 37, 28, 2, b, 40, 10, 28, 27, 30, 27, 2, b, 40, 10, 33, 28, 35, 28,
               2, 17, 23, 26, 40, 9, 26, 26, 1, 17, 26, 27, 3, 0, 0, 0, 2, 1, 40, 9, 42, 7, 41, 11)), x, y, s, P)
    art(ARTL, x, y, s, P)
    art(ARTO[t], x, y, s, P)
    if body:
        art(ARTG[body], x, y, s, P)
    if head:
        art(ARTG[head], x, y, s, P)


def oval(x, y, s, c, k=0):
    # an egg shape centred on x, y; k shrinks it (negative k grows it)
    circ(x, y + 2 * s, 7 * s - k, c)
    circ(x, y - 2 * s, 6 * s - k, c)
    circ(x, y - 5 * s, 4 * s - k, c)


def egg(x, y, s, t):
    # a shaded egg; its pattern shows how rare it is
    r = DT[t][2]
    shell = ((245, 235, 210), (225, 240, 205), (215, 230, 250), (235, 215, 250), (30, 30, 70), (20, 20, 45))[r]
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
    elif r == 5:
        # Quantum: black and night blue with glowing violet cracks
        circ(x + 2 * s, y + 4 * s, 4 * s, (35, 40, 110))
        circ(x - 3 * s, y + 1 * s, 2 * s, (35, 40, 110))
        Z = (-1, -8, 2, -4, -2, -1, 2, 2, -1, 5, 1, 8)
        for c, w in (((110, 50, 180), s + 1), ((210, 150, 255), max(1, s // 2))):
            col(c)
            for i in range(0, 10, 2):
                ax, ay, bx, by = x + Z[i] * s, y + Z[i + 1] * s, x + Z[i + 2] * s, y + Z[i + 3] * s
                fill_poly([ax - w, ax + w, bx + w, bx - w], [ay, ay, by, by])
        rect(x - 5 * s, y - 3 * s, s, s, (210, 150, 255))
        rect(x + 4 * s, y - 6 * s, s, s, (210, 150, 255))
    else:
        sp = ((190, 150, 100), (90, 170, 80), (60, 120, 230), (150, 80, 220))[r]
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
    elif ch == "^":
        out.append((0, ROCK, 2, ([px, px + 10, px + 20], [py + 20, py + 1, py + 20])))
        out.append((1, WHITE, 2, ([px + 6, px + 10, px + 14], [py + 8, py + 1, py + 8])))
    elif ch == "H":
        out.append((0, BARK, 1, (px + 10, py + 12, 9)))
        out.append((1, (60, 40, 20), 1, (px + 10, py + 12, 6)))
        out.append((2, (245, 235, 210), 1, (px + 7, py + 12, 3)))
        out.append((2, (245, 235, 210), 1, (px + 13, py + 11, 3)))
        out.append((3, (200, 160, 90), 0, (px + 1, py + 15, 18, 2)))
    elif ch == "E":
        r = DT[EGGS.get((m, x, y), 0)][2]
        sh = (25, 25, 35) if r == 4 else CYAN if r == 5 else (245, 235, 210)
        sp = MAG if r == 5 else YELLOW if r == 4 else RCOL[r] if r else (200, 170, 120)
        out.append((0, BARK, 0, (px + 3, py + 15, 14, 4)))
        out.append((1, sh, 1, (px + 10, py + 10, 6)))
        out.append((2, sp, 0, (px + 7, py + 8, 3, 3)))
        out.append((2, sp, 0, (px + 11, py + 12, 3, 3)))
    elif ch == "B":
        out.append((0, (40, 30, 60), 1, (px + 10, py + 10, 9)))
        out.append((1, BOSS[4], 1, (px + 10, py + 10, 6)))
        out.append((2, (255, 60, 60), 0, (px + 6, py + 8, 3, 3)))
        out.append((2, (255, 60, 60), 0, (px + 11, py + 8, 3, 3)))


EGGS = {}  # (land, x, y): dragon kind of the egg lying there


def el(d):
    return DT[d[1]][1]


def hero(g, out):
    px = g.x * T
    py = 20 + g.y * T
    d = g.ride
    if d is not None:
        c = d[6]
        out.append((5, lt(c, 0.45), 2, ([px, px + 9, px + 4], [py + 2, py + 11, py + 14])))
        out.append((6, c, 0, (px + 2, py + 11, 13, 7)))
        out.append((6, c, 0, (px + 13, py + 6, 7, 7)))
        out.append((6, c, 0, (px, py + 15, 3, 3)))
        out.append((6, c, 0, (px + 4, py + 18, 3, 2)))
        out.append((6, c, 0, (px + 11, py + 18, 3, 2)))
        out.append((7, YELLOW if d[1] == 19 else BLACK, 0, (px + 17, py + 8, 2, 2)))
        if d[8]:
            out.append((7, GEARC[d[8]], 0, (px + 5, py + 11, 6, 3)))
        if d[7]:
            out.append((8, GEARC[d[7]], 0, (px + 14, py + 3, 5, 3)))
        out.append((8, (240, 200, 160), 1, (px + 8, py + 5, 3)))
        out.append((8, (60, 120, 230), 0, (px + 6, py + 8, 5, 4)))
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
        drag(162, 42, 2, 21 if f is DREAD else 8, f[4])
    else:
        k = [m[0] for l in FOES for m in l].index(n)
        art(MONA[k], 142, 12, 1, cl(MONP[k]))


def foe_screen(f, title):
    cls()
    rbox(150, 30, 140, 120, 10, RED if f is DREAD else f[4], 2, NIGHT)
    foe_art(f)
    ctext(24, title, GOLD)


def battle(g, f):
    # returns True when the monster is beaten, 2 when you got away, False
    # when you died
    name, fhp, fat, xp, fc, fe = f
    mx = fhp
    foe_screen(f, name + " appears!")
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
            at = 5 + 2 * d[2] + 2 * DT[d[1]][2]
            if o == "Claw":
                dm = at + random.randint(0, 2)
                log = "Claw hits for " + str(dm) + "."
            else:
                dm = at + random.randint(2, 5)
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
            message(msg[:3] or ["You won!"], name + " beaten")
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
                foe_screen(f, name)
                was = None
        else:
            g.hp -= dm
            if g.hp <= 0:
                cls()
                ctext(60, "YOU DIED", RED)
                message(["The " + name + " won.", "Back to your last save", "at the nest."], "Game over")
                return False


def rest(g):
    g.hp = g.mhp
    g.ride = None
    for d in g.pen:
        d[3] = d[4]


# ---------- saving: one list called DRG ----------
# [2, coins, accessories owned, species in the book, eggs in the bag (up to 5, -1 = none),
#  then 4 numbers a dragon: name*32+kind, level, xp, paint*200+head*20+body]
def save(g):
    s = [2, g.coins, g.own, g.book] + (g.bag + [-1] * 5)[:5]
    for d in g.pen:
        p = PAINT.index(d[6]) + 1 if d[6] in PAINT and d[6] != DT[d[1]][3] else 0
        s += [NAMES.index(d[0]) * 32 + d[1], d[2], d[5], p * 200 + d[7] * 20 + d[8]]
    try:
        from ti_system import store_list
        store_list("DRG", s)
    except Exception:
        pass


def load(g):
    try:
        from ti_system import recall_list
        s = [int(v) for v in recall_list("DRG")]
    except Exception:
        return
    if len(s) < 9 or s[0] != 2:
        return
    g.coins, g.own, g.book = s[1], s[2], s[3]
    g.bag = [e for e in s[4:9] if e >= 0]
    for i in range(9, len(s) - 3, 4):
        t = s[i] % 32
        lv = s[i + 1]
        mh = 20 + 6 * min(4, DT[t][2]) + 6 * (lv - 1)
        p = s[i + 3] // 200
        g.pen.append([NAMES[s[i] // 32], t, lv, mh, mh, s[i + 2], PAINT[p - 1] if p else DT[t][3], s[i + 3] // 20 % 10, s[i + 3] % 20])
    if g.pen:
        g.pick = g.pen[0]
    g.warm = 12


# ---------- quests ----------
def new_quest(g):
    k = random.randint(0, 2)
    if k == 0:
        n = random.randint(2, 4)
        land = random.randint(0, g.seen)
        nm = random.choice(FOES[land])[0]
        return [0, nm, n, 0, 8 * n + 6 * land, "Beat " + str(n) + " " + nm + "s"]
    if k == 1:
        return [1, None, 1, 0, 20, "Hatch an egg"]
    land = random.randint(0, g.seen)
    n = random.randint(3, 5)
    return [2, land, n, 0, 7 * n + 6 * land, str(n) + " wins: " + LANDS[land]]


def quest_step(g, kind, what):
    q = g.quest
    if q is None or q[0] != kind or (q[1] is not None and q[1] != what):
        return
    q[3] += 1
    if q[3] >= q[2]:
        g.coins += q[4]
        g.quest = None
        message(["You finished:", q[5], "+" + str(q[4]) + " coins!"], "Quest done!")


def board(g):
    if g.quest is not None:
        q = g.quest
        c = choose(q[5] + " " + str(q[3]) + "/" + str(q[2]), ["Keep going", "Give up quest"])
        if c == 1:
            g.quest = None
        return
    qs = [new_quest(g) for i in range(3)]
    c = choose("Quests: pick one", [q[5][:15] + " " + str(q[4]) + "c" for q in qs] + ["Not now"])
    if 0 <= c < 3:
        g.quest = qs[c]


# ---------- the nest ----------
def portrait(d):
    cls(NIGHT)
    drag(102, 10, 2, d[1], d[6], d[7], d[8])


def pen(g):
    while g.pen:
        opts = [("> " if d is g.pick else "") + d[0] + " L" + str(d[2]) + " " + DT[d[1]][0][:6] for d in g.pen]
        c = choose("Dragon pen " + str(len(g.pen)) + "/10", opts + ["Back"])
        if c < 0 or c >= len(g.pen):
            return
        d = g.pen[c]
        a = choose(d[0] + " the " + DT[d[1]][0], ["Pick as partner", "See " + d[0], "Let it go free", "Back"])
        if a == 0:
            g.pick = d
        elif a == 1:
            t = DT[d[1]]
            portrait(d)
            message([t[0] + " (" + RARE[t[2]] + ")", "Element: " + ENAME[t[1]], "Level " + str(d[2]) + "  HP " + str(d[4])], d[0])
        elif a == 2 and len(g.pen) > 1:
            g.pen.remove(d)
            if g.pick is d:
                g.pick = g.pen[0]


def lst(title, opts):
    # a list with small rows, for up to 10 choices; -1 for CLEAR
    cls()
    ctext(24, title, GOLD)
    n = len(opts)
    sel = old = 0
    for i in range(n):
        text(70, 50 + i * 17, opts[i], GOLD if i == 0 else WHITE)
    while True:
        if sel != old:
            for i in (old, sel):
                rect(0, 34 + i * 17, 320, 17, BLACK)
                text(70, 50 + i * 17, opts[i], GOLD if i == sel else WHITE)
        rect(54, 40 + sel * 17, 8, 6, GOLD)
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
        elif c == 3:
            if g.coins < 20:
                message(["You need 20 coins."], "Not enough")
                continue
            p = choose("Pick a colour", list(PAINTN))
            if p >= 0:
                g.coins -= 20
                d[6] = PAINT[p]
                portrait(d)
                message([d[0] + " looks great!"], "Painted")
        else:
            return


def nest(g):
    rest(g)
    save(g)
    while True:
        c = choose("The Nest (saved)", ["Dragon pen", "Quest board", "Shop", "Backpack and book", "Leave the nest"])
        if c == 0:
            pen(g)
        elif c == 1:
            board(g)
        elif c == 2:
            if g.pick is None:
                message(["Hatch a dragon first!"])
            else:
                shop(g)
        elif c == 3:
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
        egg(40 + i * 60, 90, 3, g.bag[i])
        r = DT[g.bag[i]][2]
        text(16 + i * 60, 150, "???" if r > 4 else RARE[r][:5], RCOL[r])
    if g.bag:
        text(6, 186, "The first egg hatches in " + str(g.warm), WHITE)
    n = len([i for i in range(1, 17) if g.own >> i & 1])
    text(6, 204, "Accessories: " + str(n) + " of 16", GREY)
    while wkey() not in (OK, CLR):
        pass


def book(g):
    # one page a species; a page fills in once you have hatched that kind.
    # The secret page only exists after you have hatched the secret dragon.
    n = 21 if g.book >> 20 & 1 else 20
    i = 0
    while True:
        cls(NIGHT)
        t = DT[i]
        got = g.book >> i & 1
        ctext(22, "DRAGON BOOK  " + str(i + 1) + "/" + str(n), GOLD)
        if got:
            drag(102, 30, 2, i, t[3])
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


def hatch(g):
    e = g.bag.pop(0)
    g.warm = 12
    t = DT[e]
    cls(NIGHT)
    ctext(24, "The egg is cracking!", GOLD)
    egg(160, 110, 5, e)
    pause(0.6)
    # cracks spread, then a flash, then the dragon
    col(WHITE if t[2] > 3 else (70, 45, 30))
    C = (160, 74, 152, 88, 152, 88, 162, 100, 162, 100, 154, 114, 170, 86, 176, 100, 176, 100, 168, 112)
    for i in range(0, 20, 4):
        a1, b1, a2, b2 = C[i:i + 4]
        fill_poly([a1 - 2, a1 + 2, a2 + 2, a2 - 2], [b1, b1, b2, b2])
        pause(0.25)
    cls((255, 248, 215))
    drag(73, 30, 3, e, t[3])
    rect(0, 182, 320, 28, NIGHT)
    ctext(200, ("" if t[2] > 4 else RARE[t[2]] + " ") + t[0] + " dragon!", RCOL[t[2]])
    pause(1.2)
    names = sample(NAMES, 4)
    i = choose("Name your " + t[0] + ":", names)
    nm = names[max(0, i)]
    mh = 20 + 6 * min(4, t[2])
    d = [nm, e, 1, mh, mh, 0, t[3], 0, 0]
    g.pen.append(d)
    msg = [nm + " joins your pen!"]
    if not g.book >> e & 1:
        g.book |= 1 << e
        msg.append("New page in your book!")
    if g.pick is None:
        g.pick = d
        msg += ["Press ENTER to ride.", "Dragons fly over water,", "lava and mountains."]
    draw_map(g)
    message(msg, t[0])
    quest_step(g, 1, None)
    draw_map(g, True)


def menu(g):
    # ENTER on the map: ride or get off your partner
    d = g.pick
    if g.ride is not None:
        first = "Get off " + d[0]
    else:
        first = "Ride " + d[0] + ("" if d[3] > 0 else " (tired)")
    c = choose(d[0] + " the " + DT[d[1]][0], [first, "Backpack", "Dragon book", "Keep exploring"])
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


def put_egg(g, t, near):
    # an egg turns up on an empty spot (next to you when near is set)
    mp = g.maps[g.m]
    for n in range(30):
        if near:
            x = g.x + random.randint(-1, 1)
            y = g.y + random.randint(-1, 1)
        else:
            x = random.randint(1, 14)
            y = random.randint(1, 7)
        if 0 <= x < 16 and 0 <= y < 9 and mp[y][x] in '."' and (x, y) != (g.x, g.y) and (near or abs(x - g.x) + abs(y - g.y) > 3):
            mp[y][x] = "E"
            EGGS[(g.m, x, y)] = t
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
        g.dread = random.randint(25, 50)
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


def win(g):
    cls()
    if g.pick:
        drag(73, 30, 3, g.pick[1], g.pick[6], g.pick[7], g.pick[8])
    message(["The Shadow Wyrm flies far", "away. Dragons return to", "every land. You did it!"], "THE END")
    rest(g)
    save(g)


def play():
    g = Game()
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
    g.pick = None
    g.ride = None
    g.bag = []
    g.warm = 12
    g.coins = 0
    g.own = 0
    g.book = 0
    g.quest = None
    g.seen = 0
    g.spawn = 30
    g.dread = 0
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
            c = menu(g) if g.pick is not None else 1
            if c:
                (backpack if c == 1 else book)(g)
                draw_map(g)
            continue
        dx, dy = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, -1), DOWN: (0, 1)}.get(k, (0, 0))
        if dx == 0 and dy == 0:
            continue
        nx, ny = g.x + dx, g.y + dy
        if nx < 0 or nx > 15:
            m = g.m + (1 if nx > 15 else -1)
            if 0 <= m < 3:
                ch = g.maps[m][ny][15 - g.x]
                if ch != "T" and (ch not in "~L^" or g.ride is not None):
                    g.m = m
                    g.seen = max(g.seen, m)
                    g.x = 15 - g.x
                    draw_map(g)
            continue
        if ny < 0 or ny > 8:
            continue
        mp = g.maps[g.m]
        ch = mp[ny][nx]
        if ch == "T" or (ch in "~L^" and g.ride is None):
            continue
        if ch == "B":
            if battle(g, BOSS):
                win(g)
                return
            if g.hp <= 0:
                return
            draw_map(g)
            continue
        if ch == "E" and (len(g.bag) >= 5 or len(g.pen) + len(g.bag) >= 10):
            draw_map(g)
            message(["Your backpack is full."] if len(g.bag) >= 5 else ["No room in your pen.", "Let a dragon go first."], "Egg")
            draw_map(g, True)
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
            message(["You found an egg with", RARE[DT[e][2]] + " spots! It's in", "your backpack."], "An egg!")
            draw_map(g, True)
            continue
        if ch == "H":
            while True:
                c = nest(g)
                if not c:
                    break
                (backpack if c == 1 else book)(g)
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
            g.spawn = random.randint(25, 40)
            if sum(1 for q in EGGS if q[0] == g.m) < 2:
                put_egg(g, egg_type(g.m), False)
        hud(g)
        steps += 1
        # the evil dragon only hunts tamers who own a Rare (or rarer) dragon
        if g.dread > 0:
            g.dread -= 1
        if (g.dread == 1 or steps > 3 and random.random() < EVIL) and not g.book >> 25 & 1 and \
                any(DT[d[1]][2] >= 2 for d in g.pen):
            steps = 0
            if not evil(g):
                return
            continue
        if ch == '"' and steps > 3 and random.random() < 0.2:
            steps = 0
            if not battle(g, random.choice(FOES[g.m])):
                return
            draw_map(g)


RULES = "Find eggs (new ones keep turning up), walk to hatch them and name your dragons. 20 kinds, Common to Legendary. Ride over water, lava and mountains. The nest saves your game and has your pen, quests for coins and a shop. If you lose all your HP, you die!"
KEYS = ["Arrows: walk or fly", "ENTER: ride, get off, backpack", "Fights: Left/Right + ENTER", "CLEAR: save and quit"]


def main():
    while True:
        c = home("GHDRAGON", "DRAGON TAMER", RULES, KEYS, ("Play", "Back"))
        if c < 0:
            return
        play()
