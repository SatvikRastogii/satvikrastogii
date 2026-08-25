"""Hand-authored bitmap glyph table, rendered two ways.

Variant 2 (terminal) emits merged outline paths; variant 3 emits contribution
squares. One definition, two renderers -- so the terminal and the portrait are
provably the same typeface.

No font files, no @font-face, no metric guessing: every advance width is a
count of cells, so layout is exact in any renderer.
"""

# 5 wide x 8 tall. '#' is on. Row 0 is the cap line, row 6 the baseline row,
# row 7 the descender row. Glyphs written with 7 rows get a blank row 7 -- only
# g j p q y , ; _ reach below the baseline and they are defined with all 8.
# Without that 8th row those five sit a row high and read as capitals.
F5 = {}
CAPR = 7   # cap line to baseline inclusive -- the visual cap height in rows


def _d(spec, rows_expected=7):
    for chunk in spec.strip().split("\n\n"):
        lines = chunk.split("\n")
        ch = lines[0]
        ch = " " if ch == "SPACE" else ch
        rows = lines[1:]
        assert len(rows) == rows_expected, (ch, len(rows))
        assert all(len(r) == 5 for r in rows), ch
        F5[ch] = rows + ["....."] * (8 - rows_expected)


_d(r"""
SPACE
.....
.....
.....
.....
.....
.....
.....

A
.###.
#...#
#...#
#####
#...#
#...#
#...#

B
####.
#...#
#...#
####.
#...#
#...#
####.

C
.###.
#...#
#....
#....
#....
#...#
.###.

D
####.
#...#
#...#
#...#
#...#
#...#
####.

E
#####
#....
#....
####.
#....
#....
#####

F
#####
#....
#....
####.
#....
#....
#....

G
.###.
#...#
#....
#.###
#...#
#...#
.###.

H
#...#
#...#
#...#
#####
#...#
#...#
#...#

I
#####
..#..
..#..
..#..
..#..
..#..
#####

J
..###
...#.
...#.
...#.
...#.
#..#.
.##..

K
#...#
#..#.
#.#..
##...
#.#..
#..#.
#...#

L
#....
#....
#....
#....
#....
#....
#####

M
#...#
##.##
#.#.#
#...#
#...#
#...#
#...#

N
#...#
##..#
#.#.#
#..##
#...#
#...#
#...#

O
.###.
#...#
#...#
#...#
#...#
#...#
.###.

P
####.
#...#
#...#
####.
#....
#....
#....

Q
.###.
#...#
#...#
#...#
#.#.#
#..#.
.##.#

R
####.
#...#
#...#
####.
#.#..
#..#.
#...#

S
.####
#....
#....
.###.
....#
....#
####.

T
#####
..#..
..#..
..#..
..#..
..#..
..#..

U
#...#
#...#
#...#
#...#
#...#
#...#
.###.

V
#...#
#...#
#...#
#...#
#...#
.#.#.
..#..

W
#...#
#...#
#...#
#...#
#.#.#
##.##
#...#

X
#...#
#...#
.#.#.
..#..
.#.#.
#...#
#...#

Y
#...#
#...#
.#.#.
..#..
..#..
..#..
..#..

Z
#####
....#
...#.
..#..
.#...
#....
#####
""")

_d(r"""
a
.....
.....
.###.
....#
.####
#...#
.####

b
#....
#....
####.
#...#
#...#
#...#
####.

c
.....
.....
.###.
#....
#....
#....
.###.

d
....#
....#
.####
#...#
#...#
#...#
.####

e
.....
.....
.###.
#...#
#####
#....
.###.

f
..##.
.#..#
.#...
####.
.#...
.#...
.#...

g
.....
.###.
#...#
#...#
.####
....#
####.

h
#....
#....
####.
#...#
#...#
#...#
#...#

i
..#..
.....
.##..
..#..
..#..
..#..
.###.

j
...#.
.....
..##.
...#.
...#.
#..#.
.##..

k
#....
#....
#..#.
#.#..
##...
#.#..
#..#.

l
.##..
..#..
..#..
..#..
..#..
..#..
.###.

m
.....
.....
##.#.
#.#.#
#.#.#
#...#
#...#

n
.....
.....
####.
#...#
#...#
#...#
#...#

o
.....
.....
.###.
#...#
#...#
#...#
.###.

p
.....
####.
#...#
#...#
####.
#....
#....

q
.....
.####
#...#
#...#
.####
....#
....#

r
.....
.....
#.##.
##..#
#....
#....
#....

s
.....
.....
.####
#....
.###.
....#
####.

t
.#...
.#...
####.
.#...
.#...
.#..#
..##.

u
.....
.....
#...#
#...#
#...#
#..##
.##.#

v
.....
.....
#...#
#...#
#...#
.#.#.
..#..

w
.....
.....
#...#
#...#
#.#.#
#.#.#
.#.#.

x
.....
.....
#...#
.#.#.
..#..
.#.#.
#...#

y
.....
#...#
#...#
#...#
.####
....#
.###.

z
.....
.....
#####
...#.
..#..
.#...
#####
""")

_d(r"""
0
.###.
#...#
#..##
#.#.#
##..#
#...#
.###.

1
..#..
.##..
..#..
..#..
..#..
..#..
.###.

2
.###.
#...#
....#
...#.
..#..
.#...
#####

3
#####
...#.
..#..
...#.
....#
#...#
.###.

4
...#.
..##.
.#.#.
#..#.
#####
...#.
...#.

5
#####
#....
####.
....#
....#
#...#
.###.

6
..##.
.#...
#....
####.
#...#
#...#
.###.

7
#####
....#
...#.
..#..
.#...
.#...
.#...

8
.###.
#...#
#...#
.###.
#...#
#...#
.###.

9
.###.
#...#
#...#
.####
....#
...#.
.##..
""")

_d(r"""
.
.....
.....
.....
.....
.....
.##..
.##..

,
.....
.....
.....
.....
.##..
.##..
.#...

:
.....
.##..
.##..
.....
.##..
.##..
.....

;
.....
.##..
.##..
.....
.##..
.##..
.#...

'
.##..
.##..
.#...
.....
.....
.....
.....

"
##.##
##.##
.....
.....
.....
.....
.....

-
.....
.....
.....
#####
.....
.....
.....

/
....#
....#
...#.
..#..
.#...
#....
#....

\
#....
#....
.#...
..#..
...#.
....#
....#

(
...#.
..#..
.#...
.#...
.#...
..#..
...#.

)
.#...
..#..
...#.
...#.
...#.
..#..
.#...

!
..#..
..#..
..#..
..#..
..#..
.....
..#..

?
.###.
#...#
....#
...#.
..#..
.....
..#..

$
..#..
.####
#.#..
.###.
..#.#
####.
..#..

_
.....
.....
.....
.....
.....
.....
#####

#
.#.#.
.#.#.
#####
.#.#.
#####
.#.#.
.#.#.

@
.###.
#...#
#.###
#.#.#
#.###
#....
.###.

[
.###.
.#...
.#...
.#...
.#...
.#...
.###.

]
.###.
...#.
...#.
...#.
...#.
...#.
.###.

{
..##.
.#...
.#...
##...
.#...
.#...
..##.

}
.##..
...#.
...#.
...##
...#.
...#.
.##..

<
...#.
..#..
.#...
#....
.#...
..#..
...#.

>
.#...
..#..
...#.
....#
...#.
..#..
.#...

|
..#..
..#..
..#..
..#..
..#..
..#..
..#..

*
.....
#.#.#
.###.
#####
.###.
#.#.#
.....

+
.....
..#..
..#..
#####
..#..
..#..
.....

=
.....
.....
#####
.....
#####
.....
.....

%
##..#
##.#.
..#..
.#...
#..##
.#.##
#....

&
.##..
#..#.
#.#..
.#...
#.#.#
#..#.
.##.#

~
.....
.....
.##.#
#..#.
.....
.....
.....

^
..#..
.#.#.
#...#
.....
.....
.....
.....

·
.....
.....
.....
..#..
.....
.....
.....

*S*
..#..
..#..
#####
.###.
.#.#.
#...#
.....
""")

_d(r"""
g
.....
.....
.####
#...#
#...#
.####
....#
.###.

j
...#.
.....
..##.
...#.
...#.
...#.
#..#.
.##..

p
.....
.....
####.
#...#
#...#
####.
#....
#....

q
.....
.....
.####
#...#
#...#
.####
....#
....#

y
.....
.....
#...#
#...#
#...#
.####
....#
.###.

,
.....
.....
.....
.....
.....
.##..
.##..
.#...

;
.....
.....
.##..
.##..
.....
.##..
.##..
.#...

:
.....
.....
.##..
.##..
.....
.##..
.##..
.....

_
.....
.....
.....
.....
.....
.....
.....
#####
""", rows_expected=8)

STAR = "*S*"  # named so it can't collide with a real character

GAP = 1  # cells of tracking between glyphs
W, H = 5, 8


def _rows(ch):
    return F5.get(ch, F5["?"])


def advance(cw):
    """Width of one character cell including tracking, in user units."""
    return (W + GAP) * cw


def text_width(s, cw):
    return len(s) * advance(cw) - GAP * cw if s else 0.0


def cells(s):
    """Yield (col, row) for every lit pixel, in glyph-grid coordinates."""
    for i, ch in enumerate(s):
        ox = i * (W + GAP)
        for r, row in enumerate(_rows(ch)):
            for c, px in enumerate(row):
                if px == "#":
                    yield ox + c, r


def path(s, x, y, cw, ch):
    """One merged <path> d for a string. Horizontal runs collapse into single
    rects, which keeps the file small without touching the shapes."""
    out = []
    for i, c in enumerate(s):
        ox = x + i * (W + GAP) * cw
        for r, row in enumerate(_rows(c)):
            run = 0
            for col in range(W + 1):
                on = col < W and row[col] == "#"
                if on:
                    run += 1
                elif run:
                    px = ox + (col - run) * cw
                    py = y + r * ch
                    out.append(
                        "M%s %sh%sv%sh-%sz"
                        % (_n(px), _n(py), _n(run * cw), _n(ch), _n(run * cw))
                    )
                    run = 0
    return "".join(out)


def _n(v):
    return ("%.2f" % v).rstrip("0").rstrip(".") or "0"


def squares(s, x, y, pitch, size, rx=2):
    """Yield <rect> tuples (px, py, size) on a square grid -- variant 3."""
    for col, row in cells(s):
        yield x + col * pitch, y + row * pitch, size, rx


# --- <use>/<defs> renderer -------------------------------------------------
# Emitting a merged path per character puts a full README well over 400KB.
# Defining each glyph once at unit scale and referencing it with <use> costs
# ~30 bytes per character instead of ~220. <use> renders fine in <img> context.

def gid(ch):
    return "g%x" % ord(ch)


def defs_for(chars):
    """<path> defs at unit cell scale (1x1 per pixel) for the glyphs given."""
    out = []
    for ch in sorted(set(chars)):
        if ch not in F5:
            ch = "?"
        d = path(ch, 0, 0, 1, 1)
        if d:
            out.append('<path id="%s" d="%s"/>' % (gid(ch), d))
    return "".join(out)


def run(s, x, y, cw, ch, extra=""):
    """A <g> holding one <use> per non-blank character.

    x, y are user units; the group scales the unit glyphs, so <use> offsets
    stay in whole cells and the character grid can never drift.
    """
    uses = []
    for i, c in enumerate(s):
        if c == " " or (c not in F5 and c != " "):
            if c == " ":
                continue
        cc = c if c in F5 else "?"
        uses.append('<use href="#%s" x="%d"/>' % (gid(cc), i * (W + GAP)))
    if not uses:
        return ""
    return '<g transform="translate(%s %s) scale(%s %s)"%s>%s</g>' % (
        _n(x), _n(y), _n(cw), _n(ch), extra, "".join(uses)
    )


# --- contribution-square renderer (variant 3) ------------------------------
# Same glyph tables, drawn as rounded squares on a pitch grid. Text blocks use
# <use> for the same reason the terminal does: a full page of per-cell rects
# would be about a megabyte.

from glyphs7 import F7, W7, H7, CAPR7  # noqa: E402

BODY = {"t": F5, "w": W, "h": H, "cap": CAPR, "gap": 1, "id": "b"}
HEAD = {"t": F7, "w": W7, "h": H7, "cap": CAPR7, "gap": 1, "id": "h"}


def face_rows(face, ch):
    return face["t"].get(ch, face["t"].get("?", face["t"][" "]))


def face_adv(face):
    return face["w"] + face["gap"]


def face_width(s, face, pitch):
    if not s:
        return 0.0
    return (len(s) * face_adv(face) - face["gap"]) * pitch


def sq_gid(face, ch):
    return "%s%x" % (face["id"], ord(ch))


def sq_defs(chars, face, size, rx):
    """One <g> of unit-pitch rects per glyph, referenced by <use>."""
    out = []
    for ch in sorted(set(chars)):
        rows = face_rows(face, ch)
        cells = []
        for r, row in enumerate(rows):
            for c, px in enumerate(row):
                if px == "#":
                    cells.append(
                        '<rect x="%s" y="%s" width="%s" height="%s" rx="%s"/>'
                        % (c, r, _n(size), _n(size), _n(rx))
                    )
        if cells:
            out.append('<g id="%s">%s</g>' % (sq_gid(face, ch), "".join(cells)))
    return "".join(out)


def sq_run(s, x, y, pitch, face, extra=""):
    uses = []
    adv = face_adv(face)
    for i, c in enumerate(s):
        if c == " ":
            continue
        if c not in face["t"]:
            c = "?"
        uses.append('<use href="#%s" x="%d"/>' % (sq_gid(face, c), i * adv))
    if not uses:
        return ""
    return '<g transform="translate(%s %s) scale(%s)"%s>%s</g>' % (
        _n(x), _n(y), _n(pitch), extra, "".join(uses))
