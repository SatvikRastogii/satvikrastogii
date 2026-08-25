"""The display face for variant 1, hand-authored.

Every glyph is a skeleton -- the centreline a sign painter would chalk before
loading a brush -- drawn in a box 140 units tall with the skeleton inset to
y 18..122. The theme strokes that same skeleton four times at four widths:
black outline, coloured drop shadow, enamel fill, and a thin highlight
offset up and left. Stroking one path rather than filling four outlines is
what keeps the layers in perfect register, which is the whole trick behind
painted lettering.

No font file, no conversion tool, no @font-face. Uppercase and figures only,
because truck panels are set in caps.
"""

CAP = 140          # cap height including the stroke
TOP, BOT = 18, 122  # skeleton extents

# glyph -> (advance, skeleton path data)
G = {
    " ": (46, ""),
    "A": (92, "M20 122 L46 20 L72 122 M29 86 L63 86"),
    "B": (90, "M22 18 L22 122 M22 18 L52 18 Q74 18 74 42 Q74 66 52 66 L22 66"
               " M52 66 Q78 66 78 94 Q78 122 52 122 L22 122"),
    "C": (88, "M70 42 Q62 18 42 18 Q18 18 18 50 L18 90 Q18 122 42 122"
               " Q62 122 70 98"),
    "D": (90, "M22 18 L22 122 M22 18 L48 18 Q76 18 76 48 L76 92"
               " Q76 122 48 122 L22 122"),
    "E": (78, "M66 18 L20 18 L20 122 L66 122 M20 70 L58 70"),
    "F": (74, "M66 18 L20 18 L20 122 M20 70 L58 70"),
    "G": (94, "M72 42 Q64 18 44 18 Q18 18 18 50 L18 90 Q18 122 44 122"
               " Q72 122 72 96 L72 78 L50 78"),
    "H": (92, "M20 18 L20 122 M72 18 L72 122 M20 70 L72 70"),
    "I": (46, "M23 18 L23 122"),
    "J": (76, "M56 18 L56 96 Q56 122 36 122 Q16 122 14 98"),
    "K": (90, "M20 18 L20 122 M72 18 L26 70 M42 54 L74 122"),
    "L": (76, "M20 18 L20 122 L66 122"),
    "M": (112, "M20 122 L20 18 L56 78 L92 18 L92 122"),
    "N": (96, "M20 122 L20 18 L76 122 L76 18"),
    "O": (94, "M18 48 Q18 18 47 18 Q76 18 76 48 L76 92 Q76 122 47 122"
               " Q18 122 18 92 Z"),
    "P": (86, "M22 122 L22 18 L52 18 Q76 18 76 46 Q76 74 52 74 L22 74"),
    "Q": (98, "M18 48 Q18 18 47 18 Q76 18 76 48 L76 92 Q76 122 47 122"
               " Q18 122 18 92 Z M56 98 L82 130"),
    "R": (90, "M22 122 L22 18 L52 18 Q76 18 76 44 Q76 68 52 68 L22 68"
               " M50 68 L76 122"),
    "S": (84, "M68 42 Q62 18 41 18 Q18 18 18 42 Q18 62 43 68 Q70 74 70 96"
               " Q70 122 43 122 Q20 122 14 98"),
    "T": (84, "M14 18 L70 18 M42 18 L42 122"),
    "U": (92, "M20 18 L20 92 Q20 122 46 122 Q72 122 72 92 L72 18"),
    "V": (94, "M20 18 L47 122 L74 18"),
    "W": (120, "M18 18 L39 122 L60 42 L81 122 L102 18"),
    "X": (92, "M20 18 L72 122 M72 18 L20 122"),
    "Y": (90, "M20 18 L45 70 L70 18 M45 70 L45 122"),
    "Z": (86, "M18 18 L68 18 L18 122 L68 122"),
    "0": (90, "M18 48 Q18 18 45 18 Q72 18 72 48 L72 92 Q72 122 45 122"
               " Q18 122 18 92 Z"),
    "1": (58, "M12 42 L31 18 L31 122"),
    "2": (84, "M16 42 Q18 18 43 18 Q68 18 68 44 Q68 64 45 82 L16 122 L70 122"),
    "3": (84, "M16 36 Q22 18 43 18 Q68 18 68 42 Q68 62 45 65 Q70 68 70 94"
               " Q70 122 43 122 Q20 122 15 100"),
    "4": (90, "M57 122 L57 18 L14 88 L76 88"),
    "5": (84, "M68 18 L23 18 L18 64 Q31 56 45 56 Q70 56 70 89 Q70 122 43 122"
               " Q20 122 15 100"),
    "6": (86, "M64 30 Q55 18 41 18 Q18 18 18 52 L18 92 Q18 122 42 122"
               " Q67 122 67 96 Q67 70 42 70 Q18 70 18 92"),
    "7": (80, "M14 18 L66 18 L33 122"),
    "8": (88, "M45 18 Q20 18 20 40 Q20 62 45 66 Q70 70 70 94 Q70 122 45 122"
               " Q20 122 20 94 Q20 70 45 66 Q70 62 70 40 Q70 18 45 18 Z"),
    "9": (86, "M22 110 Q31 122 45 122 Q68 122 68 88 L68 48 Q68 18 44 18"
               " Q19 18 19 44 Q19 70 44 70 Q68 70 68 48"),
    ".": (46, "M23 116 L23 122"),
    ",": (46, "M25 114 L17 138"),
    ":": (44, "M22 44 L22 50 M22 92 L22 98"),
    "!": (46, "M23 18 L23 90 M23 116 L23 122"),
    "?": (80, "M16 42 Q18 18 42 18 Q68 18 68 44 Q68 64 42 76 L42 92"
               " M42 116 L42 122"),
    "&": (100, "M86 122 L34 64 Q18 48 18 34 Q18 18 38 18 Q57 18 57 34"
                " Q57 50 34 66 Q14 82 14 100 Q14 122 39 122 Q64 122 76 98"),
    "-": (64, "M14 70 L50 70"),
    "/": (64, "M12 122 L52 18"),
    "'": (38, "M19 18 L19 46"),
    "(": (52, "M38 14 Q18 42 18 70 Q18 98 38 126"),
    ")": (52, "M16 14 Q36 42 36 70 Q36 98 16 126"),
}


def advance(ch, tracking=0):
    return G.get(ch, G["?"])[0] + tracking


def width(s, tracking=22):
    return sum(advance(c, tracking) for c in s)


def _xs(d):
    """Every x coordinate in a skeleton path. The faces use only absolute
    M/L/Q, so x values are the even entries of each command's number list."""
    import re
    out = []
    for _cmd, body in re.findall(r"([MLQ])([^MLQZz]*)", d):
        nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", body)]
        out += nums[0::2]
    return out


def ink_span(s, tracking=22):
    """Left and right edge of the actual marks, not of the advance box.

    width() counts the tracking that follows the final letter and knows
    nothing about side bearings, so centring on it puts a word visibly off to
    one side -- 18 units for STAR OK PLEASE. Centre on this instead. Stroke
    weight is ignored on purpose: it grows both edges equally and cancels.
    """
    xs, x = [], 0
    for ch in s:
        adv, d = G.get(ch, G["?"])
        if d:
            xs += [x + v for v in _xs(d)]
        x += adv + tracking
    return (min(xs), max(xs)) if xs else (0.0, 0.0)


def centre_x(s, tracking, scale, cx):
    """Where to place a word so its ink is centred on cx."""
    lo, hi = ink_span(s, tracking)
    return cx - (lo + hi) / 2.0 * scale


def group(s, gid, tracking=22, jitter=True):
    """A <g> of translated skeleton paths, for <use> to stroke repeatedly.

    Each letter gets a small deterministic rotation and vertical offset. A
    truck panel is chalked and brushed by hand; letters sitting on a perfect
    baseline at identical angles is the one thing that would give this away
    as typeset. The wobble is derived from the character and its position, so
    it is stable across rebuilds -- the same word always wobbles the same way.
    """
    parts = []
    x = 0
    for i, ch in enumerate(s):
        adv, d = G.get(ch, G["?"])
        if d:
            if jitter:
                h = (ord(ch) * 37 + i * 101) % 100
                rot = (h % 7 - 3) * 0.5          # -1.5 to +1.5 degrees
                dy = ((h // 7) % 7 - 3) * 1.1    # -3.3 to +3.3 units
                t = ('translate(%s %s) rotate(%s %s 70)'
                     % (_n(x), _n(dy), _n(rot), _n(adv / 2.0)))
            else:
                t = "translate(%s 0)" % _n(x)
            parts.append('<path d="%s" transform="%s"/>' % (d, t))
        x += adv + tracking
    return '<g id="%s" fill="none">%s</g>' % (gid, "".join(parts))


def _n(v):
    return ("%.1f" % v).rstrip("0").rstrip(".") or "0"


def painted(gid, x, y, scale, fill, outline, shadow, highlight=None,
            weight=36.0, out_w=44.0, shadow_dx=8.0, shadow_dy=9.0):
    """Stroke one skeleton into a painted letter.

    Five passes: the drop shadow gets its own outline and fill so it reads as
    a second letter behind the first, which is what a painter actually does,
    rather than a blur. The layers cannot drift out of register because they
    are the same path.
    """
    def use(dx, dy, colour, w, extra=""):
        return ('<use href="#%s" transform="translate(%s %s) scale(%s)" '
                'stroke="%s" stroke-width="%s"%s/>'
                % (gid, _n(x + dx), _n(y + dy), _n(scale), colour,
                   _n(w / scale), extra))

    layers = [
        use(shadow_dx, shadow_dy, outline, out_w),
        use(shadow_dx, shadow_dy, shadow, weight),
        use(0, 0, outline, out_w),
        use(0, 0, fill, weight),
    ]
    if highlight:
        layers.append(use(-3.0, -4.0, highlight, weight * 0.17,
                          ' opacity="0.7"'))
    return ('<g stroke-linecap="round" stroke-linejoin="round">%s</g>'
            % "".join(layers))
