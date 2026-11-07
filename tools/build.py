# Builds the download page assets: app icons, files.json and gamehub.zip.
# Run from the repo root: python3 tools/build.py
import sys, os, json, zipfile
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

files = sorted(f for f in os.listdir(os.path.join(ROOT, 'calc')) if f.endswith('.py'))
first = ['GAMEHUB.py', 'GHLIB.py', 'GHICONS.py', 'GHSAVE.py']
files = [f for f in first if f in files] + [f for f in files if f not in first]
info = []
for f in files:
    p = os.path.join(ROOT, 'calc', f)
    name = f[:-3]
    assert name.isalpha() and name.isupper() and len(name) <= 8, f
    info.append({'file': f, 'name': name, 'bytes': os.path.getsize(p)})
json.dump(info, open(os.path.join(ROOT, 'site', 'files.json'), 'w'), indent=1)
with zipfile.ZipFile(os.path.join(ROOT, 'gamehub.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(os.path.join(ROOT, 'calc', f), 'GAMEHUB/' + f)
print(len(files), 'files,', sum(i['bytes'] for i in info), 'bytes')
