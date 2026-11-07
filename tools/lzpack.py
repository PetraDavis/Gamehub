# Text squeezing for the one-file build (GHONE), plus a minifier.
# pack() is a small LZ77: a back-reference is "`" + 2 letters of distance + 1
# of length, all from ALPH, so the result stays plain text that can sit in a
# raw string. GAMEHUB.unpack() is the calculator side and must match.
ALPH = ''.join(chr(c) for c in range(35, 127) if c not in (39, 92, 96))
B = len(ALPH)
MARK = '`'
def pack(s, minm=5):
    assert MARK not in s
    maxoff = B * B
    maxlen = B + 3  # length codes 4..B+3
    out = []; i = 0; n = len(s); tab = {}
    lit = []
    while i < n:
        best = 0; bo = 0
        if i + minm <= n:
            k = s[i:i+4]
            for p in reversed(tab.get(k, [])[-48:]):
                if i - p > maxoff: break
                l = 0
                while i + l < n and l < maxlen and s[p + l] == s[i + l]:
                    l += 1
                if l > best: best, bo = l, i - p
        if best >= minm:
            out.append(''.join(lit)); lit = []
            o = bo - 1
            out.append(MARK + ALPH[o // B] + ALPH[o % B] + ALPH[best - 4])
            for j in range(i, i + best):
                tab.setdefault(s[j:j+4], []).append(j)
            i += best
        else:
            lit.append(s[i]); tab.setdefault(s[i:i+4], []).append(i); i += 1
    out.append(''.join(lit))
    return ''.join(out)
def unpack(s):
    A = ALPH
    out = bytearray(); i = 0; n = len(s)
    while i < n:
        j = s.find('`', i)
        if j < 0: j = n
        out.extend(s[i:j].encode()); i = j
        if i < n:
            o = A.find(s[i+1]) * B + A.find(s[i+2]) + 1
            l = A.find(s[i+3]) + 4
            st = len(out) - o
            for k in range(l):
                out.append(out[st + k])
            i += 4
    return bytes(out).decode()

import tokenize, io, keyword
def minify(src):
    out = []; line = []; level = 0; prev = None
    toks = tokenize.generate_tokens(io.StringIO(src).readline)
    for t in toks:
        tp, s = t.type, t.string
        if tp in (tokenize.NEWLINE, tokenize.NL):
            if line:
                out.append(' ' * level + ''.join(line))
            line = []; prev = None; continue
        if tp == tokenize.INDENT: level += 1; continue
        if tp == tokenize.DEDENT: level -= 1; continue
        if tp in (tokenize.COMMENT, tokenize.ENDMARKER): continue
        if prev and (prev[-1].isalnum() or prev[-1] == '_') and (s[0].isalnum() or s[0] in '_"\''):
            line.append(' ')
        line.append(s); prev = s
    if line: out.append(' ' * level + ''.join(line))
    return '\n'.join(out) + '\n'
