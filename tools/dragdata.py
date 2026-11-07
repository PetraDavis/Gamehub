# Makes the packed picture data in calc/GHDRAGON.py: the dragon's base
# shape, each kind's special look, and the accessories. Edit the shapes here
# and run this file; it rewrites the block between the ART markers.
#
# Shapes use a grid where the dragon faces left, about 48 x 34 units.
# ('r', colour, x, y, w, h)        a rectangle
# ('c', colour, x, y, r)           a circle
# ('t', colour, x1, y1, x2, y2, x3, y3)  a triangle
# Colours are numbers into the palette in GHDRAGON.drag: 0-14 PAL; 15 = the dragon's wing colour
# (lighter), 16 = darker, 17 = the dragon's own colour; 18 purple, 19 silver, 20 cape blue,
# 21 night blue, 22 bright violet, 23 blood red; 24 = a little lighter, 25 = much darker.
import os, re

OX, OY = 8, 8   # added to every x, y so nothing is negative

def wing(c, rib=16):
    # the near wing: skin, two finger bones, the arm along the front, shoulder
    return [('t', c, 16, 18, 32, 2, 29, 20), ('t', rib, 32, 2, 20, 19, 22, 19), ('t', rib, 32, 2, 25, 20, 27, 20),
            ('t', 17, 15, 18, 32, 1, 18, 18), ('c', 17, 18, 19, 3), ('t', 1, 32, 1, 34, -1, 33, 3)]


# grouped by colour, because every colour change costs as much as a shape
BASE = ([('t', 16, 22, 17, 37, 0, 39, 17)] +                                    # far wing
        [('r', 25, 19, 26, 4, 7), ('r', 25, 17, 32, 5, 2), ('r', 25, 33, 26, 4, 7), ('r', 25, 31, 32, 5, 2)] +  # far legs
        [('t', 17, 33, 18, 49, 23, 33, 27), ('t', 17, 46, 19, 52, 23, 46, 27),  # tail and its spade
         ('c', 17, 18, 22, 5), ('c', 17, 33, 22, 5), ('r', 17, 18, 17, 15, 10),  # body
         ('t', 17, 10, 13, 20, 18, 14, 24), ('r', 17, 9, 12, 7, 10),           # neck
         ('r', 17, 2, 8, 12, 8), ('r', 17, 0, 11, 4, 5)] +                     # head, snout
        [('t', 16, 33, 24, 49, 23, 33, 27), ('r', 16, 0, 15, 11, 2)] +           # tail shadow, jaw
        [('r', 24, 18, 17, 14, 2), ('r', 24, 3, 8, 9, 1)] +                     # shine on back and head
        [('r', 15, 16, 24, 19, 3), ('r', 15, 9, 16, 2, 6), ('t', 15, 10, 8, 17, 2, 13, 10)] +  # belly, throat, horn
        [('r', 16, 21, 24, 1, 3), ('r', 16, 25, 24, 1, 3), ('r', 16, 29, 24, 1, 3),  # belly plates
         ('t', 16, 7, 9, 12, 2, 10, 9)] +                                       # back horn
        wing(15)[:1] + wing(15)[1:3] +
        [('t', 17, 15, 18, 32, 1, 18, 18), ('c', 17, 18, 19, 3),
         ('c', 17, 19, 26, 4), ('r', 17, 16, 26, 5, 7), ('r', 17, 14, 32, 7, 2),   # near legs
         ('c', 17, 32, 26, 4), ('r', 17, 29, 26, 5, 7), ('r', 17, 27, 32, 7, 2)] +
        [('r', 25, 4, 8, 5, 1)] +                                               # brow
        [('r', 1, 4, 10, 3, 2), ('r', 1, 2, 15, 1, 1), ('r', 1, 14, 33, 1, 1), ('r', 1, 27, 33, 1, 1),
         ('t', 1, 32, 1, 34, -1, 33, 3)] +                                     # eye, fang, claws, wing claw
        [('r', 0, 5, 10, 2, 2), ('r', 0, 1, 12, 1, 1)])                         # pupil, nostril

FEAT = [
    # 0 Ember: a flame on its tail
    [('t', 3, 46, 22, 52, 8, 56, 22), ('t', 2, 49, 22, 52, 13, 54, 22)],
    # 1 Cinder: smoke puffs from its nose
    [('c', 6, -3, 10, 2), ('c', 6, -6, 6, 3), ('c', 5, -8, 1, 2)],
    # 2 Puddle: round belly and a fin
    [('c', 15, 25, 23, 6), ('t', 16, 22, 16, 26, 9, 30, 16)],
    # 3 Brook: a wavy white stripe
    [('r', 1, 14, 20, 7, 2), ('r', 1, 21, 21, 7, 2), ('r', 1, 28, 20, 8, 2)],
    # 4 Sprig: a leaf on its head
    [('t', 8, 5, 8, 9, -1, 13, 8), ('r', 7, 8, 5, 1, 4)],
    # 5 Mossy: moss patches
    [('r', 7, 18, 17, 5, 3), ('r', 7, 27, 21, 6, 3), ('r', 7, 4, 9, 3, 2), ('r', 7, 36, 21, 4, 2)],
    # 6 Pebble: rocky bumps
    [('c', 5, 18, 16, 3), ('c', 5, 24, 15, 3), ('c', 5, 30, 16, 3), ('c', 5, 8, 9, 2)],
    # 7 Magma: glowing cracks
    [('r', 3, 18, 19, 6, 1), ('r', 3, 23, 20, 1, 5), ('r', 3, 28, 18, 1, 6), ('r', 3, 29, 23, 5, 1), ('r', 3, 5, 14, 4, 1)],
    # 8 Smoky: smoke-grey wings
    wing(5) + [('c', 6, -3, 12, 2)],
    # 9 Frost: icicle spikes
    [('t', 1, 16, 16, 18, 10, 20, 16), ('t', 1, 22, 16, 24, 10, 26, 16), ('t', 1, 30, 16, 32, 10, 34, 16), ('t', 1, 37, 20, 39, 15, 41, 20)],
    # 10 Storm: lightning on its wing
    [('r', 2, 23, 7, 2, 4), ('r', 2, 23, 10, 5, 2), ('r', 2, 26, 11, 2, 5)],
    # 11 Thorn: thorn spikes
    [('t', 16, 34, 20, 36, 15, 38, 20), ('t', 16, 39, 20, 41, 15, 43, 20), ('t', 16, 10, 12, 13, 6, 16, 12)],
    # 12 Sunscale: a sun on its chest
    [('c', 2, 18, 22, 4), ('c', 13, 18, 22, 2)],
    # 13 Coral: coral horns
    [('r', 9, 5, 1, 2, 7), ('r', 9, 3, 2, 2, 2), ('r', 9, 10, 0, 2, 8), ('r', 9, 12, 1, 2, 2)],
    # 14 Jade: a gem on its forehead
    [('r', 11, 6, 8, 3, 3), ('r', 1, 7, 8, 1, 1)],
    # 15 Blossom: petals on its wings
    [('c', 1, 24, 8, 2), ('c', 9, 28, 13, 2), ('c', 1, 22, 15, 2), ('c', 2, 25, 11, 1)],
    # 16 Phoenix: fire wings, a crest and a flaming tail
    wing(3, 2) + [('t', 2, 3, 8, 6, -1, 9, 8), 
     ('t', 3, 45, 22, 51, 5, 57, 22), ('t', 2, 48, 22, 51, 11, 54, 22)],
    # 17 Leviathan: a long body with fins
    [('r', 17, 30, 18, 14, 6), ('t', 15, 20, 16, 24, 10, 28, 16), ('t', 15, 33, 18, 36, 12, 39, 18)],
    # 18 Oakheart: branch antlers and bark
    [('r', 10, 6, 0, 2, 8), ('r', 10, 3, 1, 4, 2), ('r', 10, 10, 0, 2, 8), ('r', 10, 11, 0, 4, 2),
     ('r', 16, 19, 17, 1, 9), ('r', 16, 25, 17, 1, 9), ('r', 16, 31, 17, 1, 9)],
    # 19 Starwing: black, with yellow stars on its night-blue wings
    wing(21, 0) + [('r', 2, 24, 6, 2, 2), ('r', 2, 27, 11, 2, 2), ('r', 2, 21, 14, 2, 2),
     ('r', 2, 29, 4, 1, 1), ('r', 2, 25, 15, 1, 1), ('t', 2, 24, 17, 27, 23, 21, 23), ('r', 2, 5, 10, 2, 2)],
    # 20 Quantum: dark blue and black halves, violet glow, violet eyes
    [('r', 0, 25, 17, 9, 10), ('c', 0, 33, 22, 5), ('t', 0, 33, 18, 49, 23, 33, 27), ('t', 22, 10, 8, 17, 2, 13, 10), ('r', 22, 9, 16, 2, 6)] +
    wing(0, 18) +
    [('r', 22, 17, 21, 8, 1), ('r', 22, 24, 21, 1, 4), ('r', 22, 24, 24, 9, 1), ('r', 22, 33, 20, 1, 4),
     ('r', 22, 38, 21, 8, 1), ('r', 22, 2, 13, 6, 1), ('r', 22, 5, 10, 2, 2),
     ('r', 18, 40, 10, 2, 2), ('r', 22, 44, 14, 1, 1), ('r', 18, -4, 4, 2, 2), ('r', 22, -2, 1, 1, 1)],
    # 21 Dread Drake (the evil one, never hatched): spikes, big horns, red mouth, violet eyes
    [('t', 23, 18, 17, 20, 11, 23, 17), ('t', 23, 24, 17, 26, 10, 29, 17), ('t', 23, 30, 17, 32, 11, 35, 17),
     ('t', 23, 37, 19, 39, 14, 42, 20), ('t', 23, 43, 21, 45, 17, 47, 22), ('t', 23, 10, 12, 12, 7, 15, 12)] +
    wing(0, 23) +
    [('t', 0, 9, 9, 20, -6, 14, 10), ('t', 0, 6, 8, 12, -4, 10, 9),
     ('r', 23, 0, 15, 11, 1), ('r', 23, 9, 16, 2, 6), ('r', 25, 16, 24, 19, 3), ('r', 1, 2, 15, 1, 2), ('r', 1, 5, 15, 1, 2), ('r', 1, 8, 15, 1, 2),
     ('r', 18, 3, 9, 5, 4), ('r', 22, 4, 10, 3, 2), ('r', 1, 5, 10, 1, 1), ('t', 0, 3, 8, 9, 8, 9, 10)],
]

# accessories: 1-8 go on the head, 9-16 on the body
GEAR = [
    [],
    # 1 Bow
    [('t', 9, 9, 6, 5, 2, 5, 10), ('t', 9, 9, 6, 13, 2, 13, 10), ('r', 4, 8, 5, 2, 2)],
    # 2 Goggles
    [('r', 10, 2, 9, 12, 2), ('r', 0, 3, 8, 5, 4), ('r', 14, 4, 9, 3, 2)],
    # 3 Wizard hat
    [('t', 18, 2, 8, 8, -7, 14, 8), ('r', 2, 7, 0, 2, 2)],
    # 4 Crown
    [('r', 13, 3, 5, 10, 3), ('t', 13, 3, 5, 4, 1, 6, 5), ('t', 13, 6, 5, 8, 0, 10, 5), ('t', 13, 10, 5, 12, 1, 13, 5), ('r', 4, 7, 6, 2, 1)],
    # 5 Party hat
    [('t', 11, 4, 8, 8, -6, 12, 8), ('r', 2, 6, 2, 4, 2), ('c', 12, 8, -6, 2)],
    # 6 Top hat
    [('r', 0, 2, 7, 12, 2), ('r', 0, 4, -3, 8, 10), ('r', 4, 4, 4, 8, 2)],
    # 7 Flower
    [('c', 9, 11, 3, 2), ('c', 9, 14, 6, 2), ('c', 9, 8, 6, 2), ('c', 9, 11, 9, 2), ('c', 2, 11, 6, 2)],
    # 8 Viking helmet
    [('r', 19, 3, 4, 10, 5), ('r', 13, 2, 8, 12, 1), ('t', 1, 3, 5, -1, -1, 5, 3), ('t', 1, 13, 5, 17, -1, 11, 3)],
    # 9 Scarf
    [('r', 4, 10, 13, 8, 3), ('r', 4, 13, 16, 3, 7)],
    # 10 Saddle
    [('r', 10, 20, 13, 10, 4), ('r', 13, 22, 17, 2, 6)],
    # 11 Cape
    [('t', 20, 12, 13, 32, 14, 40, 32), ('r', 2, 12, 13, 3, 3)],
    # 12 Armor
    [('r', 19, 15, 17, 20, 7), ('r', 6, 15, 20, 20, 1), ('r', 19, 10, 13, 6, 6)],
    # 13 Bell collar
    [('r', 20, 10, 14, 8, 2), ('c', 2, 14, 18, 2), ('r', 0, 13, 19, 2, 1)],
    # 14 Backpack
    [('r', 8, 28, 10, 8, 7), ('r', 7, 28, 10, 8, 2), ('r', 2, 31, 12, 2, 1)],
    # 15 Flag
    [('r', 10, 30, -2, 1, 18), ('r', 4, 31, -2, 8, 5), ('r', 2, 34, 0, 2, 1)],
    # 16 Necklace
    [('r', 13, 10, 15, 8, 1), ('r', 13, 13, 16, 2, 2), ('c', 11, 14, 19, 2)],
]


def pack(ops):
    out = []
    for o in ops:
        k, c = o[0], o[1]
        a = list(o[2:])
        if k == 'r':
            a = [a[0] + OX, a[1] + OY, a[2], a[3], 0, 0]
            kk = 0
        elif k == 'c':
            a = [a[0] + OX, a[1] + OY, a[2], 0, 0, 0]
            kk = 1
        else:
            a = [a[0] + OX, a[1] + OY, a[2] + OX, a[3] + OY, a[4] + OX, a[5] + OY]
            kk = 2
        for v in a:
            assert 0 <= v < 256, o
        out += [kk, c] + a
    return bytes(out)


def lit(b):
    return repr(b)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(root, 'calc', 'GHDRAGON.py')
    s = open(p).read()
    block = ["# ART: made by tools/dragdata.py (edit the shapes there, then run it)",
             "ARTB = " + lit(pack(BASE)),
             "ARTF = (" + ",\n        ".join(lit(pack(f)) for f in FEAT) + ")",
             "ARTG = (" + ",\n        ".join(lit(pack(g)) for g in GEAR) + ")",
             "# END ART"]
    s = re.sub(r"# ART: made by.*?# END ART", "\n".join(block).replace("\\", "\\\\"), s, flags=re.S)
    open(p, 'w').write(s)
    print('ok', len(FEAT), 'kinds', len(GEAR) - 1, 'accessories')


if __name__ == '__main__':
    main()
