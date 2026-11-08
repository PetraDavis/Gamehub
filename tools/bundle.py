# Joins the calculator sources into the files the site sends:
#   dist/GAMEHUB.py         the menu, with the helpers, icons and saves built in
#   dist/<GAME>.py          one game with the helpers and its icon built in. It runs
#                           on its own, and GAMEHUB loads it only when it is picked,
#                           because the calculator can't hold every game at once.
# Each module's own top-level names get a prefix so they can't clash, and
# "import GHICONS" / "GHICONS.draw" become plain names. No exec, no imports.
# Run from the repo root: python3 tools/bundle.py
import ast, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lzpack import pack, unpack, minify
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALC = os.path.join(ROOT, 'calc')
DIST = os.path.join(ROOT, 'dist')
LIB = 'GHLIB'
OWN = {'GHLIB', 'GHICONS', 'GHSAVE', 'GAMEHUB'}
GAMES = sorted(f[:-3] for f in os.listdir(CALC) if f.endswith('.py') and f[:-3] not in OWN)
SHORT = {}


def short(mod):
    if mod not in SHORT:
        SHORT[mod] = mod[2:].lower()
    return SHORT[mod]


def parse(mod):
    return ast.parse(open(os.path.join(CALC, mod + '.py')).read())


def top_names(tree):
    out = set()
    for n in tree.body:
        for t in ast.walk(n) if not isinstance(n, (ast.FunctionDef, ast.ClassDef)) else [n]:
            if isinstance(t, (ast.FunctionDef, ast.ClassDef)):
                out.add(t.name)
            elif isinstance(t, ast.Name) and isinstance(t.ctx, ast.Store):
                out.add(t.id)
    return out


def local_names(fn):
    out = set()
    a = fn.args
    for x in a.posonlyargs + a.args + a.kwonlyargs + [a.vararg, a.kwarg]:
        if x:
            out.add(x.arg)
    body = fn.body if isinstance(fn.body, list) else [fn.body]
    stack = list(body)
    while stack:
        n = stack.pop()
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out.add(n.name)
            continue
        if isinstance(n, (ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            continue
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            out.add(n.id)
        if isinstance(n, ast.ExceptHandler) and n.name:
            out.add(n.name)
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for al in n.names:
                nm = (al.asname or al.name).split('.')[0]
                if not nm.startswith('GH'):
                    out.add(nm)
        stack.extend(ast.iter_child_nodes(n))
    return out


def comp_names(c):
    out = set()
    for g in c.generators:
        for t in ast.walk(g.target):
            if isinstance(t, ast.Name):
                out.add(t.id)
    return out


class Renamer(ast.NodeTransformer):
    # rename: {module-level name: new name}; mods: {module name: prefix} for X.attr
    def __init__(self, rename, mods):
        self.rename = rename
        self.mods = mods
        self.scopes = []

    def shadowed(self, name):
        return any(name in s for s in self.scopes)

    def visit_Name(self, n):
        if n.id in self.rename and not self.shadowed(n.id):
            n.id = self.rename[n.id]
        return n

    def visit_Attribute(self, n):
        if isinstance(n.value, ast.Name) and n.value.id in self.mods and not self.shadowed(n.value.id):
            return ast.copy_location(ast.Name(id=self.mods[n.value.id] + n.attr, ctx=n.ctx), n)
        self.generic_visit(n)
        return n

    def _fn(self, n):
        self.scopes.append(local_names(n))
        for d in getattr(n, 'decorator_list', []):
            self.visit(d)
        self.visit(n.args)
        if isinstance(n.body, list):
            n.body = [self.visit(b) for b in n.body]
        else:
            n.body = self.visit(n.body)
        self.scopes.pop()
        return n

    def visit_FunctionDef(self, n):
        if not self.scopes and n.name in self.rename:
            n.name = self.rename[n.name]
        return self._fn(n)

    def visit_ClassDef(self, n):
        if not self.scopes and n.name in self.rename:
            n.name = self.rename[n.name]
        self.generic_visit(n)
        return n

    def visit_Lambda(self, n):
        return self._fn(n)

    def _comp(self, n):
        self.scopes.append(comp_names(n))
        self.generic_visit(n)
        self.scopes.pop()
        return n

    visit_ListComp = visit_SetComp = visit_DictComp = visit_GeneratorExp = _comp

    def visit_Import(self, n):
        n.names = [a for a in n.names if a.name not in self.mods]
        return n if n.names else None

    def visit_ImportFrom(self, n):
        if n.module in self.mods:
            return None
        for a in n.names:
            b = a.asname or a.name
            if b in self.rename and not self.shadowed(b):
                a.asname = self.rename[b]
        return n


def strip_docs(tree):
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Module)) and n.body:
            b = n.body[0]
            if isinstance(b, ast.Expr) and isinstance(b.value, ast.Constant) and isinstance(b.value.value, str):
                n.body = n.body[1:] or [ast.Pass()]


def convert(mod, mods):
    tree = parse(mod)
    names = top_names(tree)
    if mod == LIB:
        rename = {}
    else:
        rename = {k: mods.get(mod, short(mod) + '_') + k for k in names}
    tree = Renamer(rename, mods).visit(tree)
    strip_docs(tree)
    ast.fix_missing_locations(tree)
    return tree


def hub_loader(tree, games):
    # GAMEHUB: "m = __import__(mod)" becomes a lookup of the game's main()
    class Fix(ast.NodeTransformer):
        def visit_Call(self, n):
            self.generic_visit(n)
            if isinstance(n.func, ast.Name) and n.func.id == '__import__':
                return ast.parse('_GameMod(GAMES[x])').body[0].value.__class__(
                    func=ast.Name(id='_GameMod', ctx=ast.Load()),
                    args=[ast.Subscript(value=ast.Name(id='GAMES', ctx=ast.Load()), slice=n.args[0], ctx=ast.Load())],
                    keywords=[])
            return n
    tree = Fix().visit(tree)
    ast.fix_missing_locations(tree)
    return tree


def emit(parts, head, pre=()):
    src = head + '\n'
    imports = set()
    body = list(pre)
    for t in parts:
        for n in t.body:
            if isinstance(n, (ast.Import, ast.ImportFrom)) and n.col_offset == 0 and not isinstance(n, ast.Try):
                s = ast.unparse(n)
                if s not in imports:
                    imports.add(s)
                    body.insert(len(pre) + len(imports) - 1, s)
                continue
            body.append(ast.unparse(n))
    out = []
    for ln in '\n'.join(body).split('\n'):
        # one space per indent level instead of four, to save calculator memory
        n = len(ln) - len(ln.lstrip(' '))
        out.append(' ' * (n // 4) + ln[n:])
    # and no spaces that Python doesn't need
    return src + minify('\n'.join(out) + '\n')


def mods_map(extra):
    # short name prefixes: every name costs calculator memory
    m = {'GHLIB': '', 'GHICONS': 'I_', 'GHSAVE': 'S_', 'GAMEHUB': 'H_'}
    for g in extra:
        m[g] = 'G_'
    return m


# The Evo runs out of memory turning a file into code when the file holds
# too much code (it counts words, not bytes: "a=1" costs as much as
# "apple=100"). GAMEHUB 6800 words opened, 7900 didn't; Tiny Quest at 6100
# opens. So a file over LIMIT words is split in two: <NAME>B holds the
# helpers and everything they need, and <NAME> starts with
# "from <NAME>B import *" and keeps the rest.
SPLIT_OVER = 6200
LIMIT = 5000


def words(src):
    import tokenize, io
    skip = (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER)
    return sum(1 for t in tokenize.generate_tokens(io.StringIO(src).readline) if t.type not in skip)


def node_words(n):
    return words(ast.unparse(n) + '\n')


def defines(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return {n.name}
    out = set()
    stack = [n]
    while stack:
        x = stack.pop()
        if isinstance(x, (ast.FunctionDef, ast.ClassDef)) and x is not n:
            out.add(x.name)
            continue
        if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store):
            out.add(x.id)
        if isinstance(x, (ast.Import, ast.ImportFrom)):
            out |= {(a.asname or a.name).split('.')[0] for a in x.names}
        stack.extend(ast.iter_child_nodes(x))
    return out


def side_name(name, k=0):
    # GHANIM -> GHANIMB, then GHANIMC (calculator names: 8 letters at most)
    return name[:7] + 'BCDEF'[k]


def loads(nodes):
    return {x.id for n in nodes for x in ast.walk(n) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load)}


def split(parts, name, head, tail):
    # tail: statements that must stay last in the main file (main(), RAN)
    nodes = [n for t in parts for n in t.body]
    full = emit([ast.Module(body=nodes + tail, type_ignores=[])], head)
    if words(full) <= SPLIT_OVER:
        return {name: full}
    imports = [n for n in nodes if isinstance(n, (ast.Import, ast.ImportFrom))]
    rest = [n for n in nodes if n not in imports]
    out = {}
    cur, cur_head, cur_tail, k = name, head, tail, 0
    while True:
        bn = side_name(name, k)
        main_nodes, side_nodes = peel(rest, cur_tail)
        if not side_nodes:
            main_nodes, side_nodes = rest, []
        have = set()
        for n in side_nodes:
            have |= defines(n)
        under = sorted(u for u in loads(main_nodes + cur_tail) if u in have and u.startswith('_'))
        pre = []
        if side_nodes:
            pre = ['from %s import *' % bn] + (['from %s import %s' % (bn, ','.join(under))] if under else [])
        body = main_nodes + cur_tail if pre else imports + main_nodes + cur_tail
        out[cur] = emit([ast.Module(body=body, type_ignores=[])], cur_head, pre)
        if not side_nodes:
            return out
        rest = side_nodes
        last = emit([ast.Module(body=imports + rest, type_ignores=[])], '')
        cur, cur_head, cur_tail, k = bn, '# %s: part of %s. Keep it next to %s.' % (bn, name, name), [], k + 1
        if words(last) <= LIMIT:
            out[cur] = emit([ast.Module(body=imports + rest, type_ignores=[])], cur_head)
            return out


MOVABLE = (ast.FunctionDef, ast.ClassDef, ast.Assign, ast.Try)


def peel(rest, tail):
    # Split rest into (main, side): side holds definitions and everything
    # they need, main holds callers nothing in side needs, about LIMIT words
    owner = {}
    for n in rest:
        for d in defines(n):
            owner[d] = n
    deps = {}
    for n in rest:
        deps[id(n)] = {id(owner[u]) for u in loads([n]) if u in owner and owner[u] is not n}
    side = {id(n) for n in rest if isinstance(n, MOVABLE) and defines(n)}
    for n in rest:
        if not isinstance(n, MOVABLE):
            side -= {id(owner[d]) for d in defines(n) if d in owner}
    while True:
        bad = {i for i in side if not deps[i] <= side}
        if not bad:
            break
        side.difference_update(bad)
    size = {id(n): node_words(n) for n in rest}
    order = {id(n): k for k, n in enumerate(rest)}
    budget = LIMIT - sum(size[id(n)] for n in rest if id(n) not in side) - words(emit([ast.Module(body=tail, type_ignores=[])], ''))
    while True:
        needed = set()
        for i in side:
            needed |= deps[i]
        free = [i for i in side if i not in needed and size[i] <= budget]
        if not free:
            break
        # biggest first; ties go by place in the file so every build is the same
        i = max(free, key=lambda i: (size[i], -order[i]))
        side.discard(i)
        budget -= size[i]
    return [n for n in rest if id(n) not in side], [n for n in rest if id(n) in side]


# GAMEHUB itself is tiny: it loads the menu (GHMENU), and when a game is
# picked it drops the whole menu from memory before loading the game, so
# the calculator only ever holds one of them. GAMEHUB alone stayed in
# memory under every game and they ran out of room together.
LAUNCHER = """# GAMEHUB - game center for the TI-84 Evo. Run this file.
import sys
import gc
def drop(names):
 for k in names:
  try:
   del sys.modules[k]
  except Exception:
   pass
# a game that stopped with an error last time can leave its files in memory
# (and stale, even after new ones are sent): clear every GH file first
drop([k for k in sys.modules if k[:2]=="GH"])
st=[0,0,0,"",""]
while True:
 gc.collect()
 import GHMENU
 mod=GHMENU.H_pick(st)
 GHMENU=None
 drop(["GHMENU"]+["GHMENU"+c for c in "BCDEF"])
 gc.collect()
 if not mod:
  break
 try:
  m=__import__(mod)
  if not getattr(m,"RAN",False):
   m.main()
 except Exception as e:
  st[3]=str(e)[:26]
  st[4]=mod
 m=None
 drop([mod]+[mod[:7]+c for c in "ABCDEFHPQSTVWXYZ"])
"""


def build_hub():
    mods = mods_map([])
    parts = [convert(LIB, mods), convert('GHICONS', mods), convert('GHSAVE', mods), convert('GAMEHUB', mods)]
    # the menu file doesn't run main(); GAMEHUB calls its pick()
    hub = parts[-1]
    hub.body = [n for n in hub.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                                            and getattr(n.value.func, 'id', '') == 'H_main')]
    keep = ast.parse('H_pick')
    parts.append(keep)
    shake(parts)
    parts.pop()
    out = split(parts, 'GHMENU', '# GHMENU: the GAMEHUB menu. Run GAMEHUB, not this.', keep.body)
    out['GAMEHUB'] = LAUNCHER
    return out


def keep_only(tree, var, key):
    # trim a module-level dict literal (ICONS / BG) to the one entry a game needs
    for n in tree.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == var and isinstance(n.value, ast.Dict):
            pairs = [(k, v) for k, v in zip(n.value.keys, n.value.values) if isinstance(k, ast.Constant) and k.value == key]
            n.value.keys = [k for k, _ in pairs]
            n.value.values = [v for _, v in pairs]


def shake(parts):
    # drop top-level functions, classes and plain constants nothing uses
    while True:
        used = set()
        for t in parts:
            for n in t.body:
                for x in ast.walk(n):
                    if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load):
                        used.add(x.id)
        gone = 0
        for t in parts:
            keep = []
            for n in t.body:
                name = None
                if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                    name = n.name
                elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                    name = n.targets[0].id
                if name and name not in used:
                    gone += 1
                    continue
                keep.append(n)
            t.body = keep
        if not gone:
            return parts


def build_game(g):
    mods = mods_map([g])
    icons = convert('GHICONS', mods)
    keep_only(icons, mods['GHICONS'] + 'ICONS', g)
    keep_only(icons, mods['GHICONS'] + 'BG', g)
    parts = [convert(LIB, mods), icons]
    if 'GHSAVE' in open(os.path.join(CALC, g + '.py')).read():
        parts.append(convert('GHSAVE', mods))
    parts.append(convert(g, mods))
    call = ast.parse(mods[g] + 'main()')
    parts.append(call)
    shake(parts)
    parts.pop()
    if sum(words(ast.unparse(t)) for t in parts) > STAGE_OVER:
        return build_staged(g)
    tail = call.body + ast.parse('RAN = True').body
    return split(parts, g, '# %s from GAMEHUB, on its own. Run it.' % g, tail)


# A game this big doesn't fit in memory all at once even in parts (none right now;
# the old Encrypted demo was one). So its home screen and the game itself become separate
# files that are never loaded together: <NAME>H shows the home screen,
# <NAME>P (plus its parts) is the game, and <NAME> loads one, drops it,
# then loads the other.
STAGE_OVER = 9000
# the game part loads while nothing else is in memory, but each of its files
# is turned into code while the earlier ones are already held, so smaller
# files keep that peak down
STAGE_LIMIT = 3040
LITE_BOXES = """
def _corners(x, y, w, h, r, t):
    return ((x, y, w, t), (x, y + h - t, w, t), (x, y + t, t, h - 2 * t), (x + w - t, y + t, t, h - 2 * t))


def rbox(x, y, w, h, r, c, t=2, inner=BLACK, fill=True):
    edge(x, y, w, h, r, c, t)
    if fill:
        rect(x + t, y + t, w - 2 * t, h - 2 * t, inner)
"""
STAGED = """# {g} from GAMEHUB, on its own. Run it.
import sys
import gc
def drop(names):
 for k in names:
  try:
   del sys.modules[k]
  except Exception:
   pass
# memory meter: prints how much memory is free at each step, so if this
# stops with a memory error the last lines say where
def free(step):
 gc.collect()
 try:
  print(step,gc.mem_free())
 except Exception:
  print(step)
# a run that stopped with an error can leave the game's files in memory
# (and stale, even after new ones are sent): clear every GH file first
drop([k for k in sys.modules if k[:2]=="GH" and k!=__name__])
while True:
 free("start")
 import {h}
 free("home loaded")
 c={h}.G_front()
 {h}=None
 drop(["{h}"])
 free("home dropped")
 if c<0:
  break
 try:
  import {p}
  free("game loaded")
  {p}.G_back()
 finally:
  {p}=None
  drop([k for k in sys.modules if k[:2]=="GH" and k!=__name__])
RAN=True
"""


def main_calls(tree, mods, g):
    # main() is "while True: c = home(...); if c < 0: return; play()":
    # pull out the home(...) call and the name of the game function
    fn = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == mods[g] + 'main'][0]
    home_call = play = None
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'home':
            home_call = n
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and getattr(n.value.func, 'id', '') != 'home':
            play = n.value.func.id
    return home_call, play


def build_staged(g):
    mods = mods_map([g])
    h, p, g7 = g[:7] + 'H', g[:7] + 'P', g[:7]
    out = {}
    # the home screen file: the helpers, the icon and the game's words
    icons = convert('GHICONS', mods)
    keep_only(icons, mods['GHICONS'] + 'ICONS', g)
    keep_only(icons, mods['GHICONS'] + 'BG', g)
    game = convert(g, mods)
    home_call, play = main_calls(game, mods, g)
    front = ast.parse('def G_front():\n return 0')
    front.body[0].body[0].value = home_call
    keep = ast.parse('G_front')
    parts = [convert(LIB, mods), icons, game, front, keep]
    shake(parts)
    parts.pop()
    out.update(split(parts, h, '# %s: home screen of %s. Run %s, not this.' % (h, g, g), []))
    # the game file: no icon and no home screen, and plain square boxes
    # instead of the rounded ones, which take a lot of code
    game = convert(g, mods)
    lib = convert(LIB, mods)
    lite = {n.name: n for n in ast.parse(LITE_BOXES).body}
    lib.body = [lite.get(getattr(n, 'name', None), n) for n in lib.body]
    parts = [lib]
    if 'GHSAVE' in open(os.path.join(CALC, g + '.py')).read():
        parts.append(convert('GHSAVE', mods))
    parts.append(game)
    back = ast.parse('def G_back():\n %s()' % play)
    parts.append(back)
    keep = ast.parse('G_back')
    parts.append(keep)
    swaps = take_swaps(game, mods[g], g7, p)
    # the swap files use the game's helpers too, so shake with them in view
    held = [ast.Module(body=nodes, type_ignores=[]) for nodes in swaps.values()]
    shake(parts + held)
    pull_helpers(parts, swaps)
    parts.pop()
    global LIMIT
    keep_limit, LIMIT = LIMIT, STAGE_LIMIT
    out.update(split(parts, p, '# %s: the game part of %s. Run %s, not this.' % (p, g, g), []))
    LIMIT = keep_limit
    for name, nodes in swaps.items():
        have = set()
        for n in nodes:
            have |= defines(n)
        under = sorted(u for u in loads(nodes) if u.startswith('_') and u not in have)
        pre = ['from %s import *' % p] + (['from %s import %s' % (p, ','.join(under))] if under else [])
        out[name] = emit([ast.Module(body=nodes, type_ignores=[])],
                         '# %s: part of %s, loaded only while it is needed.' % (name, g), pre)
    out[g] = STAGED.format(g=g, h=h, p=p, g7=g7)
    return out


SWAP_STUB = """
def {f}(*a):
    import {m}
    r = {m}.{f}(*a)
    {m} = None
    G__drop("{m}")
    return r
"""
SWAP_DROP = """
def G__drop(m):
    import sys, gc
    try:
        del sys.modules[m]
    except Exception:
        pass
    gc.collect()
"""


def take_swaps(game, pre, g7, p):
    # SWAP = {"W": (names...)} in a game: move those functions into <g7>W
    # etc. (pull_helpers then moves what only they use), and leave small
    # stubs that load the file, call it and drop it again
    node = [n for n in game.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == pre + 'SWAP']
    if not node:
        return {}
    game.body.remove(node[0])
    spec = ast.literal_eval(node[0].value)
    out = {}
    for letter, names in sorted(spec.items()):
        want = {pre + n for n in names}
        moved = [n for n in game.body if isinstance(n, ast.FunctionDef) and n.name in want]
        rest = [n for n in game.body if n not in moved]
        m = g7 + letter
        stubs = [ast.parse(SWAP_STUB.format(f=n.name, m=m)).body[0] for n in moved if isinstance(n, ast.FunctionDef)]
        game.body = rest + stubs
        out[m] = moved
    game.body += ast.parse(SWAP_DROP).body
    return out


def pull_helpers(parts, swaps):
    # a helper (or constant) only one swap file uses moves into that file;
    # a stub nothing outside its own swap file calls goes away
    real = {n.name for nodes in swaps.values() for n in nodes if isinstance(n, ast.FunctionDef)}
    for t in parts:
        for n in list(t.body):
            if isinstance(n, ast.FunctionDef) and n.name in real:
                own = [k for k, nodes in swaps.items() if any(getattr(m, 'name', '') == n.name for m in nodes)][0]
                if not any(n.name in loads([m]) for u in parts for m in u.body if m is not n) and \
                        not any(n.name in loads(nodes) for k, nodes in swaps.items() if k != own):
                    t.body.remove(n)
    while True:
        moved = 0
        for t in parts:
            for n in list(t.body):
                if not isinstance(n, (ast.FunctionDef, ast.Assign)) or getattr(n, 'name', '') in real:
                    continue
                d = defines(n)
                if not d or any(d & loads([m]) for u in parts for m in u.body if m is not n):
                    continue
                users = [k for k, nodes in swaps.items() if d & loads(nodes)]
                if len(users) == 1:
                    t.body.remove(n)
                    swaps[users[0]].insert(0, n)
                    moved += 1
        if not moved:
            return


def build_single():
    # GHONE: the whole game center in ONE file. The menu and helpers are code;
    # each game is kept as squeezed text (tools/lzpack.py) and only unpacked
    # and turned into code when it is picked, because the calculator can't
    # load a file holding every game as code.
    # short name prefixes, since every letter counts here
    mods = {'GHLIB': '', 'GHICONS': 'I_', 'GHSAVE': 'S_', 'GAMEHUB': 'H_'}
    for i, g in enumerate(GAMES):
        mods[g] = chr(97 + i) + '_'
    hub = [convert(LIB, mods), convert('GHICONS', mods), convert('GHSAVE', mods), convert('GAMEHUB', mods)]
    games = [convert(g, mods) for g in GAMES]
    for g, t in zip(GAMES, games):
        t.body.append(ast.parse(mods[g] + 'main()').body[0])
    # keep every helper any game uses, then hand only the menu over as code
    shake(hub + games)
    src = '# GHONE - all of GAMEHUB in one file (test). Run this file.\n' + minify(emit(hub, ''))
    # the menu's own main() call sits at the end; put the games before it
    lines = src.rstrip('\n').split('\n')
    call = lines.pop()
    out = ['GAMESRC={}']
    for g, t in zip(GAMES, games):
        code = minify(emit([t], '')).strip('\n')
        z = pack(code)
        assert unpack(z) == code
        assert Q3 not in z and not z.endswith('\\') and '\r' not in z
        out.append('GAMESRC[%r]=r%s%s%s' % (g, Q3, z, Q3))
    return '\n'.join(lines + out + [call]) + '\n'


Q3 = "'" * 3


if __name__ == '__main__':
    os.makedirs(DIST, exist_ok=True)
    # build_single() (the one-file GHONE) is kept but not built: the Evo
    # can't open a file over about 36-40 KB, so one file can't hold every game
    out = dict(build_hub())
    parts = {}
    for g in GAMES:
        files = build_game(g)
        out.update(files)
        parts[g] = sorted(files)[::-1]
    for f in os.listdir(DIST):
        if f.endswith('.py') and f[:-3] not in out:
            os.remove(os.path.join(DIST, f))
    # the site sends every file a game needs
    parts['GAMEHUB'] = sorted(f for f in out if f.startswith('GHMENU'))[::-1] + ['GAMEHUB']
    import json
    open(os.path.join(DIST, 'parts.js'), 'w').write('window.PARTS = ' + json.dumps(parts, sort_keys=True) + ';\n')
    for name, src in out.items():
        compile(src, name, 'exec')
        open(os.path.join(DIST, name + '.py'), 'w').write(src)
    print(' '.join('%s=%d/%dw' % (k, len(v), words(v)) for k, v in out.items()))
