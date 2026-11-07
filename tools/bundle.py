# Joins the calculator sources into the files the site sends:
#   dist/GAMEHUB.py         the menu, with the helpers, icons and saves built in
#   dist/<GAME>.py          one game with the helpers and its icon built in. It runs
#                           on its own, and GAMEHUB loads it only when it is picked,
#                           because the calculator can't hold every game at once.
# Each module's own top-level names get a prefix so they can't clash, and
# "import GHICONS" / "GHICONS.draw" become plain names. No exec, no imports.
# Run from the repo root: python3 tools/bundle.py
import ast, os, sys
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


def emit(parts, head):
    src = head + '\n'
    imports = set()
    body = []
    for t in parts:
        for n in t.body:
            if isinstance(n, (ast.Import, ast.ImportFrom)) and n.col_offset == 0 and not isinstance(n, ast.Try):
                s = ast.unparse(n)
                if s not in imports:
                    imports.add(s)
                    body.insert(len(imports) - 1, s)
                continue
            body.append(ast.unparse(n))
    out = []
    for ln in '\n'.join(body).split('\n'):
        # one space per indent level instead of four, to save calculator memory
        n = len(ln) - len(ln.lstrip(' '))
        out.append(' ' * (n // 4) + ln[n:])
    return src + '\n'.join(out) + '\n'


def mods_map(extra):
    m = {'GHLIB': '', 'GHICONS': 'icons_', 'GHSAVE': 'save_'}
    for g in extra:
        m[g] = short(g) + '_'
    return m


def build_hub():
    mods = mods_map([])
    parts = [convert(LIB, mods), convert('GHICONS', mods), convert('GHSAVE', mods), convert('GAMEHUB', mods)]
    shake(parts)
    return emit(parts, '# GAMEHUB - game center for the TI-84 Evo. Run this file.')


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
    keep_only(icons, 'icons_ICONS', g)
    keep_only(icons, 'icons_BG', g)
    parts = [convert(LIB, mods), icons]
    if 'GHSAVE' in open(os.path.join(CALC, g + '.py')).read():
        parts.append(convert('GHSAVE', mods))
    parts.append(convert(g, mods))
    parts.append(ast.parse(mods[g] + 'main()'))
    shake(parts)
    parts.append(ast.parse('RAN = True'))
    return emit(parts, '# %s from GAMEHUB, on its own. Run it.' % g)


def build_single():
    # GHONE: the whole game center in ONE file. The menu and helpers are code;
    # each game is kept as text and only turned into code when it is picked,
    # because text takes far less calculator memory than ready-to-run code.
    mods = mods_map(GAMES)
    hub = [convert(LIB, mods), convert('GHICONS', mods), convert('GHSAVE', mods), convert('GAMEHUB', mods)]
    games = [convert(g, mods) for g in GAMES]
    for g, t in zip(GAMES, games):
        t.body.append(ast.parse(mods[g] + 'main()').body[0])
    # keep every helper any game uses, then hand only the menu over as code
    shake(hub + games)
    src = emit(hub, '# GHONE - all of GAMEHUB in one file (test). Run this file.')
    # the menu's own main() call sits at the end; put the games before it
    lines = src.rstrip('\n').split('\n')
    call = lines.pop()
    out = ['GAMESRC = {}']
    for g, t in zip(GAMES, games):
        code = emit([t], '').strip('\n')
        assert "'''" not in code and not code.endswith('\\')
        out.append("GAMESRC[%r] = r'''%s'''" % (g, code))
    return '\n'.join(lines + out + [call]) + '\n'


if __name__ == '__main__':
    os.makedirs(DIST, exist_ok=True)
    out = {'GAMEHUB': build_hub(), 'GHONE': build_single()}
    for g in GAMES:
        out[g] = build_game(g)
    for name, src in out.items():
        compile(src, name, 'exec')
        open(os.path.join(DIST, name + '.py'), 'w').write(src)
    print(' '.join('%s=%d' % (k, len(v)) for k, v in out.items()))
