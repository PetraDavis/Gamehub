keys = []; gap = 0; gapleft = 0; polls = 0; maxpolls = 200000; ops = 0; t = 0
lists = {}; img = None; on_poll = None; outdir = '.'
def shot(name):
    img.resize((640, 420), 0).save(outdir + '/' + name + '.png')

# Match the calculator's smaller random and math modules, so missing functions
# fail here too (it has no random.shuffle, random.sample or math.hypot).
import random as _r, math as _m
for _n in ('shuffle', 'sample', 'choices'):
    if hasattr(_r, _n):
        delattr(_r, _n)
if hasattr(_m, 'hypot'):
    delattr(_m, 'hypot')
