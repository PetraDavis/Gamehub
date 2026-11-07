# Desktop stand-in for the TI-84 Evo ti_draw module (for testing only).
from PIL import Image, ImageDraw, ImageFont
import simstate as S
W, H = 320, 210
img = Image.new('RGB', (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)
_c = [(0, 0, 0)]
try:
    _font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 16)
except Exception:
    _font = ImageFont.load_default()
S.img = img
class tidrawException(Exception): pass
def _chk(*v):
    S.ops += 1
def clear(): d.rectangle([0, 0, W, H], fill=(255, 255, 255)); _chk()
def set_color(r, g, b):
    for v in (r, g, b):
        if not (0 <= int(v) <= 255): raise tidrawException('color')
    _c[0] = (int(r), int(g), int(b))
def fill_rect(x, y, w, h):
    if w < 2 or h < 2: raise tidrawException('fill_rect w/h must be >1')
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=_c[0]); _chk()
def clear_rect(x, y, w, h, c=(255, 255, 255)):
    if w < 2 or h < 2: raise tidrawException('clear_rect w/h must be >1')
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=tuple(c)); _chk()
def draw_rect(x, y, w, h): d.rectangle([x - 1, y - 1, x + w, y + h], outline=_c[0]); _chk()
def fill_circle(x, y, r): d.ellipse([x - r, y - r, x + r, y + r], fill=_c[0]); _chk()
def draw_circle(x, y, r): d.ellipse([x - r, y - r, x + r, y + r], outline=_c[0]); _chk()
def draw_line(x1, y1, x2, y2): d.line([x1, y1, x2, y2], fill=_c[0]); _chk()
def draw_poly(xs, ys): d.line(list(zip(xs, ys)), fill=_c[0]); _chk()
def fill_poly(xs, ys): d.polygon(list(zip(xs, ys)), fill=_c[0]); _chk()
def draw_text(x, y, s):
    s = str(s)
    for i, ch in enumerate(s):
        d.text((x + i * 10, y - 14), ch, fill=_c[0], font=_font)
    _chk()
def plot_xy(x, y, shape): d.point((x, y), fill=_c[0])
def set_pen(size, style): pass
def set_window(*a): pass
def get_screen_dim(): return [319, 209]
def show_draw(): pass
