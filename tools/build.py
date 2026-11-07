# Builds the download page assets: app icons and the one-file builds in dist/.
# Run from the repo root: python3 tools/build.py
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'sim'), os.path.join(ROOT, 'calc')]
import simstate as S, ti_draw
from PIL import Image
import GHLIB as L, GHICONS as I

os.makedirs(os.path.join(ROOT, 'site', 'icons'), exist_ok=True)
for mod in I.ICONS:
    if mod.startswith('*'):
        continue
    L.cls()
    L.circ(160, 105, 26, I.bg(mod))
    I.draw(mod, 160, 105, L.WHITE)
    im = S.img.crop((160 - 26, 105 - 26, 160 + 26, 105 + 26)).resize((104, 104), Image.NEAREST)
    im.save(os.path.join(ROOT, 'site', 'icons', mod + '.png'))

# the one-file builds the site sends: dist/GAMEHUB.py and one file per game
import runpy
runpy.run_path(os.path.join(ROOT, 'tools', 'bundle.py'), run_name='__main__')
