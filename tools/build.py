# Builds the download page assets: app icons, the calculator files in dist/ and gamehub.zip.
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
import runpy, zipfile
runpy.run_path(os.path.join(ROOT, 'tools', 'bundle.py'), run_name='__main__')
D = os.path.join(ROOT, 'dist')
with zipfile.ZipFile(os.path.join(ROOT, 'gamehub.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(D)):
        if f.endswith('.py'):
            z.write(os.path.join(D, f), 'GAMEHUB/' + f)


# The calculator's Python rejects f(*a, x): no plain argument may follow *a.
import ast as _ast, glob as _glob
for _f in sorted(_glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dist', '*.py'))):
    for _n in _ast.walk(_ast.parse(open(_f).read())):
        if isinstance(_n, _ast.Call):
            _star = False
            for _a in _n.args:
                if isinstance(_a, _ast.Starred):
                    _star = True
                elif _star:
                    sys.exit('%s line %d: plain argument after *args (calculator SyntaxError)' % (_f, _n.lineno))
