"""Run me: python src/test_glyphs.py -- prints the font so you can read it."""
import string
import glyphs as g

PANGRAM = "Pack my box with five dozen liquor jugs. (0123456789)"
PUNCT = ".,:;'\"-/\()!?$_#@[]{}<>|*+=%&~^"


def render(s):
    grid = [[" "] * (len(s) * (g.W + g.GAP)) for _ in range(g.H)]
    for col, row in g.cells(s):
        grid[row][col] = "#"
    return "\n".join("".join(r).rstrip() for r in grid)


def main():
    required = string.ascii_letters + string.digits + " " + PUNCT
    missing = [c for c in required if c not in g.F5]
    assert not missing, "undefined glyphs: %r" % missing

    for row in g.F5.values():
        assert len(row) == g.H and all(len(r) == g.W for r in row)

    # advances are exact multiples of the cell -- the whole point of the font
    assert g.text_width("abc", 3.0) == 3 * 6 * 3.0 - 3.0

    # merged path emits at least one subpath per lit row-run
    assert g.path('A', 0, 0, 3, 4).count('M') == 12
    # descenders must reach row 7 or they read as capitals
    for ch in 'gjpqy_,;':
        assert '#' in g.F5[ch][7], 'no descender: %r' % ch
    for ch in 'PQYGJ':
        assert '#' not in g.F5[ch][7]

    print(render(PANGRAM))
    print()
    print(render(PUNCT))
    print()
    print(render("SATVIK RASTOGI"))
    print("\nok: %d glyphs, %d required, none missing" % (len(g.F5), len(required)))


if __name__ == "__main__":
    main()
