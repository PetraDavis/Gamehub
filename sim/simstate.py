keys = []; gap = 0; gapleft = 0; polls = 0; maxpolls = 200000; ops = 0; t = 0
lists = {}; img = None; on_poll = None; outdir = '.'
def shot(name):
    img.resize((640, 420), 0).save(outdir + '/' + name + '.png')
