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
# 21 night blue, 22 bright violet, 23 blood red; 24 = a little lighter, 25 = much darker;
# 26 dark brown, 27 dark gold, 28 steel, 29 deep pink, 30 teal, 31 deep blue, 32 light brown.
import os, re

OX, OY = 8, 8   # added to every x, y so nothing is negative

def wing(c, rib=16):
    # the near wing: skin, two finger bones, the arm along the front, shoulder, claw
    return [('t', c, 16, 18, 32, 2, 29, 20), ('t', rib, 32, 2, 20, 19, 22, 19), ('t', rib, 32, 2, 25, 20, 27, 20),
            ('t', 17, 15, 18, 32, 1, 18, 18), ('c', 17, 18, 19, 3), ('t', 1, 32, 1, 34, -1, 33, 3)]


# A dragon is drawn in this order, so patterns stay on the body and under the
# wing: BASE, the kind's "under" shapes, its wing, LEGS (near legs and face),
# then the kind's "over" shapes. Shapes are grouped by colour, because every
# colour change costs as much as a shape.
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
         ('t', 16, 7, 9, 12, 2, 10, 9)])                                        # back horn

LEGS = ([('c', 17, 19, 26, 4), ('r', 17, 16, 26, 5, 7), ('r', 17, 14, 32, 7, 2),   # near legs
         ('c', 17, 32, 26, 4), ('r', 17, 29, 26, 5, 7), ('r', 17, 27, 32, 7, 2)] +
        [('r', 25, 4, 8, 5, 1)] +                                               # brow
        [('r', 1, 4, 10, 3, 2), ('r', 1, 2, 15, 1, 1), ('r', 1, 14, 33, 1, 1), ('r', 1, 27, 33, 1, 1)] +  # eye, fang, claws
        [('r', 0, 5, 10, 2, 2), ('r', 0, 1, 12, 1, 1)])                         # pupil, nostril

# each kind: (under the wing, the wing's skin and bone colours, over everything)
FEAT = [
    # 0 Pyrrak: a flame on the tip of its tail
    ([('t', 3, 46, 22, 52, 8, 56, 22), ('t', 2, 49, 22, 52, 13, 54, 22)], (15, 16), []),
    # 1 Smoldedrake: smoke puffs from its nose, sooty spots
    ([('r', 16, 22, 21, 2, 2), ('r', 16, 28, 22, 2, 2), ('r', 16, 35, 21, 2, 2)], (15, 16),
     [('c', 6, -2, 10, 2), ('c', 6, -4, 6, 2), ('c', 5, -5, 2, 1)]),
    # 2 Aquawyrm: a tail fin, bubbly spots and a cheek fin
    ([('t', 15, 38, 20, 43, 13, 46, 21), ('t', 16, 40, 20, 43, 15, 45, 21),
      ('c', 14, 22, 21, 1), ('c', 14, 27, 20, 1), ('c', 14, 33, 21, 1)], (15, 16),
     [('t', 15, 9, 11, 14, 8, 12, 14)]),
    # 3 Gillwing: a wavy white stripe and gills
    ([('r', 1, 14, 20, 7, 2), ('r', 1, 21, 21, 7, 2), ('r', 1, 28, 20, 8, 2), ('r', 1, 36, 21, 4, 1)], (15, 16),
     [('r', 16, 11, 13, 1, 3), ('r', 16, 13, 13, 1, 3)]),
    # 4 Fernling: a leaf on its head
    ([], (15, 16), [('t', 8, 4, 8, 7, 0, 10, 8), ('t', 7, 7, 8, 7, 0, 10, 8), ('r', 7, 7, 4, 1, 4)]),
    # 5 Lichenwing: moss patches
    ([('r', 7, 18, 19, 5, 3), ('r', 7, 27, 22, 5, 2), ('r', 7, 35, 20, 3, 2), ('r', 7, 40, 21, 3, 2)], (15, 16),
     [('r', 7, 9, 9, 3, 2)]),
    # 6 Stonewyrm: rocky bumps on its tail, neck and sides
    ([('c', 5, 37, 19, 2), ('c', 5, 41, 20, 2), ('c', 5, 45, 22, 1), ('c', 5, 22, 22, 2), ('c', 5, 30, 23, 2),
      ('c', 6, 22, 21, 1), ('c', 6, 30, 22, 1)], (15, 16), [('c', 5, 12, 12, 2)]),
    # 7 Volcanox: glowing cracks
    ([('r', 3, 17, 20, 6, 1), ('r', 3, 22, 20, 1, 4), ('r', 3, 27, 19, 1, 5), ('r', 3, 27, 23, 6, 1),
      ('r', 3, 36, 21, 5, 1)], (15, 16), [('r', 3, 9, 13, 3, 1)]),
    # 8 Ashveil: smoke-grey wings and a puff of smoke
    ([], (5, 28), [('c', 6, -2, 12, 2)]),
    # 9 Glacius: icicle spikes on its back and tail
    ([('t', 1, 21, 17, 23, 11, 25, 17), ('t', 1, 35, 19, 37, 14, 39, 20), ('t', 1, 40, 21, 42, 16, 44, 22)], (15, 16),
     [('r', 14, 3, 9, 2, 1)]),
    # 10 Tempestra: lightning on its wing
    ([], (15, 16), [('r', 2, 28, 7, 2, 4), ('r', 2, 26, 10, 4, 2), ('r', 2, 26, 11, 2, 5)]),
    # 11 Thornwyrm: thorns on its tail and back
    ([('t', 16, 21, 17, 23, 12, 25, 17), ('t', 16, 35, 19, 37, 14, 39, 20), ('t', 16, 40, 21, 42, 16, 44, 22)], (15, 16), []),
    # 12 Dawnwing: a sun on its chest
    ([], (15, 16), [('c', 2, 25, 23, 3), ('c', 13, 25, 23, 1)]),
    # 13 Pearlhorn: coral horns
    ([], (15, 16), [('r', 9, 5, 1, 2, 7), ('r', 9, 3, 2, 2, 2), ('r', 9, 10, 0, 2, 8), ('r', 9, 12, 1, 2, 2),
                    ('r', 29, 6, 1, 1, 7), ('r', 29, 11, 0, 1, 8)]),
    # 14 Jadewyrm: a gem on its forehead and jade scales
    ([('r', 30, 20, 21, 2, 1), ('r', 30, 26, 22, 2, 1), ('r', 30, 32, 21, 2, 1)], (15, 16),
     [('r', 11, 8, 8, 3, 2), ('r', 1, 8, 8, 1, 1)]),
    # 15 Petalwyrm: petals on its wings
    ([], (15, 16), [('c', 9, 28, 10, 2), ('c', 1, 25, 14, 2), ('c', 9, 22, 16, 1), ('c', 2, 28, 16, 1)]),
    # 16 Blazequill: fire wings, a crest and a flaming tail
    ([('t', 3, 45, 22, 51, 5, 57, 22), ('t', 2, 48, 22, 51, 11, 54, 22)], (3, 2), [('t', 2, 3, 8, 6, 0, 9, 8)]),
    # 17 Abyssar: fins and glowing deep-sea spots
    ([('t', 15, 33, 18, 36, 12, 39, 19), ('t', 15, 40, 21, 44, 15, 46, 22),
      ('c', 11, 21, 21, 1), ('c', 11, 27, 22, 1), ('c', 11, 34, 21, 1)], (15, 16), []),
    # 18 Rootwyrm: branch antlers and bark
    ([('r', 16, 20, 18, 1, 8), ('r', 16, 25, 18, 1, 8), ('r', 16, 30, 18, 1, 8), ('r', 16, 37, 20, 1, 4)], (15, 16),
     [('r', 10, 6, 0, 2, 8), ('r', 10, 3, 1, 4, 2), ('r', 10, 10, 0, 2, 8), ('r', 10, 11, 0, 4, 2)]),
    # 19 Lumora: black, with yellow stars on its night-blue wings
    ([], (21, 0),
     [('t', 2, 25, 20, 28, 25, 22, 25), ('r', 2, 27, 8, 2, 2), ('r', 2, 25, 13, 2, 2), ('r', 2, 21, 16, 1, 1), ('r', 2, 29, 5, 1, 1),
      ('r', 2, 27, 17, 1, 1), ('r', 2, 5, 10, 2, 2)]),
    # 20 Quantum: dark blue and black halves, violet glow, violet eyes
    ([('r', 0, 26, 17, 7, 10), ('c', 0, 33, 22, 5), ('t', 0, 33, 18, 49, 23, 33, 27), ('t', 22, 10, 8, 17, 2, 13, 10),
      ('r', 22, 9, 16, 2, 6), ('r', 22, 17, 21, 8, 1), ('r', 22, 24, 21, 1, 3), ('r', 22, 24, 23, 9, 1),
      ('r', 22, 33, 20, 1, 4), ('r', 22, 38, 21, 7, 1)], (0, 18),
     [('r', 22, 2, 13, 6, 1), ('r', 22, 5, 10, 2, 2)]),
    # 21 Dread Drake (the evil one, never hatched): spikes, big horns, red mouth, violet eyes
    ([('t', 23, 20, 17, 22, 11, 24, 17), ('t', 23, 35, 19, 37, 13, 40, 20), ('t', 23, 41, 21, 43, 16, 46, 22),
      ('t', 23, 11, 12, 13, 7, 16, 12), ('r', 25, 16, 24, 19, 3), ('r', 23, 9, 16, 2, 6)], (0, 23),
     [('t', 0, 9, 9, 20, -6, 14, 10), ('t', 0, 6, 8, 12, -4, 10, 9),
      ('r', 23, 0, 15, 11, 1), ('r', 1, 2, 15, 1, 2), ('r', 1, 5, 15, 1, 2), ('r', 1, 8, 15, 1, 2),
      ('r', 18, 3, 9, 5, 4), ('r', 22, 4, 10, 3, 2), ('r', 1, 5, 10, 1, 1), ('t', 0, 3, 8, 9, 8, 9, 10)]),
]

# accessories: 1-8 go on the head, 9-16 on the body
GEAR = [
    [],
    # 1 Bow
    [('t', 9, 12, 6, 8, 2, 8, 10), ('t', 9, 12, 6, 16, 2, 16, 10), ('t', 29, 12, 6, 9, 5, 9, 9),
     ('t', 29, 12, 6, 15, 5, 15, 9), ('r', 12, 11, 5, 2, 2)],
    # 2 Goggles
    [('r', 26, 3, 9, 12, 2), ('r', 28, 3, 8, 6, 5), ('r', 14, 4, 9, 4, 3), ('r', 1, 4, 9, 1, 1)],
    # 3 Wizard hat
    [('t', 18, 3, 7, 8, -7, 12, 7), ('t', 21, 8, -7, 12, 7, 9, 7), ('r', 18, 1, 7, 12, 2), ('r', 21, 1, 8, 12, 1),
     ('r', 22, 4, 4, 7, 1), ('r', 2, 6, 0, 2, 2), ('r', 2, 9, 3, 1, 1)],
    # 4 Crown
    [('r', 13, 3, 5, 9, 3), ('t', 13, 3, 5, 3, 1, 6, 5), ('t', 13, 5, 5, 7, 0, 10, 5), ('t', 13, 9, 5, 12, 1, 12, 5),
     ('r', 27, 3, 7, 9, 1), ('r', 2, 4, 5, 1, 1), ('r', 4, 5, 6, 1, 1), ('r', 11, 9, 6, 1, 1)],
    # 5 Party hat
    [('t', 11, 3, 8, 7, -6, 11, 8), ('t', 30, 7, -6, 11, 8, 8, 8), ('r', 2, 5, 2, 4, 1), ('r', 2, 4, 5, 6, 1),
     ('c', 12, 7, -6, 2)],
    # 6 Top hat
    [('r', 0, 1, 7, 13, 2), ('r', 0, 3, -3, 9, 10), ('r', 4, 3, 4, 9, 2), ('r', 28, 4, -2, 1, 6)],
    # 7 Flower
    [('t', 8, 11, 7, 16, 4, 13, 8), ('c', 9, 9, 3, 2), ('c', 9, 12, 6, 2), ('c', 9, 6, 6, 2), ('c', 29, 9, 8, 2),
     ('c', 2, 9, 6, 2), ('r', 3, 9, 6, 1, 1)],
    # 8 Viking helmet
    [('t', 6, 4, 6, -1, -1, 4, 3), ('t', 6, 12, 6, 17, -1, 12, 3), ('c', 19, 8, 5, 4), ('r', 19, 3, 5, 10, 3),
     ('r', 28, 9, 4, 4, 4), ('r', 13, 2, 8, 12, 1), ('r', 1, 6, 3, 1, 2)],
    # 9 Scarf
    [('r', 4, 8, 14, 9, 3), ('r', 4, 12, 17, 3, 6), ('r', 23, 8, 16, 9, 1), ('r', 23, 14, 17, 1, 6),
     ('r', 1, 10, 14, 1, 3), ('r', 1, 12, 20, 3, 1)],
    # 10 Saddle
    [('r', 10, 19, 15, 11, 4), ('r', 32, 20, 15, 9, 1), ('r', 26, 19, 18, 11, 1), ('r', 26, 19, 12, 2, 4),
     ('r', 26, 24, 19, 1, 6), ('r', 13, 23, 25, 3, 1)],
    # 11 Cape
    [('t', 20, 10, 14, 30, 15, 40, 31), ('t', 31, 20, 15, 30, 15, 40, 31), ('c', 13, 11, 15, 2), ('r', 2, 10, 14, 1, 1)],
    # 12 Armor
    [('r', 19, 14, 20, 22, 6), ('r', 19, 9, 13, 6, 8), ('r', 1, 15, 20, 20, 1), ('r', 28, 14, 25, 22, 1),
     ('r', 28, 9, 17, 6, 1), ('r', 28, 24, 20, 1, 6), ('r', 13, 18, 22, 1, 1), ('r', 13, 30, 22, 1, 1)],
    # 13 Bell collar
    [('r', 20, 8, 14, 9, 2), ('r', 31, 8, 15, 9, 1), ('c', 27, 12, 18, 2), ('c', 13, 12, 17, 1), ('r', 0, 11, 19, 2, 1)],
    # 14 Backpack
    [('r', 26, 30, 15, 1, 5), ('r', 8, 31, 11, 7, 7), ('r', 7, 31, 11, 7, 2), ('r', 7, 36, 13, 2, 5),
     ('r', 13, 34, 13, 1, 1), ('r', 1, 32, 14, 1, 2)],
    # 15 Flag
    [('r', 26, 34, -4, 1, 21), ('r', 4, 35, -4, 9, 6), ('r', 23, 35, 0, 9, 2), ('r', 2, 38, -2, 2, 2),
     ('r', 13, 33, -5, 3, 1)],
    # 16 Necklace
    [('r', 13, 9, 17, 7, 1), ('r', 27, 11, 18, 3, 1), ('c', 11, 12, 20, 2), ('r', 30, 12, 21, 2, 1), ('r', 1, 11, 19, 1, 1)],
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
             "ARTL = " + lit(pack(LEGS)),
             "ARTF = (" + ",\n        ".join(lit(pack(f[0])) for f in FEAT) + ")",
             "ARTW = " + lit(bytes(c for f in FEAT for c in f[1])),
             "ARTO = (" + ",\n        ".join(lit(pack(f[2])) for f in FEAT) + ")",
             "ARTG = (" + ",\n        ".join(lit(pack(g)) for g in GEAR) + ")",
             "# END ART"]
    s = re.sub(r"# ART: made by.*?# END ART", "\n".join(block).replace("\\", "\\\\"), s, flags=re.S)
    open(p, 'w').write(s)
    print('ok', len(FEAT), 'kinds', len(GEAR) - 1, 'accessories')


if __name__ == '__main__':
    main()
