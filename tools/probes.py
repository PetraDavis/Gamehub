# Writes dist/GHSZA.py .. GHSZD.py (40, 48, 56, 64 KB): size test files.
# Calculator file names can only use letters, so the size is a letter. Each one is mostly a
# single long text, like the one-file GHONE, and shows "OK" if the calculator
# could open it. The biggest one that opens tells us the Evo's file limit.
import os, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALPH = "".join(chr(c) for c in range(35, 127) if c not in (39, 92, 96))
SIZES = (('A', 40), ('B', 48), ('C', 56), ('D', 64))
for L, kb in SIZES:
    r = random.Random(kb)
    head = ("# GHSZ%s - size test. If you can read OK on the screen, a %d KB file fits.\n"
            "from ti_draw import *\nfrom ti_system import *\nD = '''" % (L, kb))
    tail = ("'''\nset_color(0, 0, 0)\nfill_rect(-1, -1, 321, 211)\nset_color(255, 255, 255)\n"
            "draw_text(20, 60, 'Size test %d KB: OK')\ndraw_text(20, 90, 'Text length ' + str(len(D)))\n"
            "draw_text(20, 140, 'Press any key')\nwait_key()\n" % kb)
    n = kb * 1024 - len(head) - len(tail)
    body = ''.join(r.choice(ALPH) for _ in range(n))
    src = head + body + tail
    compile(src, 'p', 'exec')
    open(os.path.join(ROOT, 'dist', 'GHSZ%s.py' % L), 'w').write(src)
