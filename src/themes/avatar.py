"""The profile avatar: truck art x matchbox label, one square.

Reuses truckart's palette and motif primitives so the avatar and the README
header are the same artwork, not two things that resemble each other.

The hard constraint is size. GitHub shows this at about 40px in comment
threads and 260px on the profile page, and crops it to a circle in most
places. So: everything that matters lives inside the inscribed circle, the
shapes are large and flat, and there is no type -- a monogram would be mud
at 40px. It has to read as "curly hair, dark glasses" at a glance or it does
not work at all.

Static on purpose. Avatars are uploaded as PNG; animation would be thrown
away by the rasteriser.
"""
import math

from . import truckart

VB = 1000
C = VB / 2.0

# The enamel set is truckart's, imported not copied -- if the panel palette
# changes the avatar follows. Plus the three tones a face needs that a truck
# rear panel never did.
PAL = dict(truckart.LIGHT)
PAL.update({"skin": "#DC9455", "skin_shade": "#B26F36", "hair": "#171009"})


def n(v):
    return ("%.2f" % v).rstrip("0").rstrip(".") or "0"


def _sunburst(cx, cy, r, count, a, b, rot=0.0):
    """Alternating wedges. The single most matchbox thing there is."""
    out = []
    step = 360.0 / count
    for i in range(count):
        a0 = math.radians(rot + i * step)
        a1 = math.radians(rot + i * step + step * 0.5)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        out.append('<path d="M%s %s L%s %s A%s %s 0 0 1 %s %s Z" fill="%s"/>'
                   % (n(cx), n(cy), n(x0), n(y0), n(r), n(r), n(x1), n(y1),
                      a if i % 2 == 0 else b))
    return "".join(out)


def _scallop_ring(cx, cy, r, count, cols, ink, rr):
    """Meenakari edge, wrapped into a circle. Polychrome: a bead ring that
    runs one colour all the way round is a border, not meenakari."""
    out = []
    for i in range(count):
        ang = math.radians(360.0 * i / count)
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" '
                   'stroke-width="5"/>'
                   % (n(x), n(y), n(rr), cols[i % len(cols)], ink))
    return "".join(out)


def _curls(cx, cy, rx, ry, ink, hair):
    """The hair reads as curly only if its silhouette is lumpy. Circles
    around an arc do that at 40px in a way that drawn ringlets do not."""
    out = []
    lumps = [
        (-1.06, 30), (-0.92, 40), (-0.76, 47), (-0.58, 52), (-0.40, 54),
        (-0.20, 50), (0.00, 55), (0.20, 50), (0.40, 54), (0.58, 51),
        (0.76, 46), (0.92, 38), (1.06, 29),
    ]
    for t, rr in lumps:
        ang = math.pi + (t + 1.0) * math.pi / 2.0
        x = cx + rx * math.cos(ang)
        y = cy + ry * math.sin(ang)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>'
                   % (n(x), n(y), n(rr), hair))
    return "".join(out)


def render(stats=None, dark=False):
    p = PAL
    ink, hair = p["ink"], p["hair"]
    o = []

    # ---- ground ---------------------------------------------------------
    o.append('<rect width="%d" height="%d" fill="%s"/>' % (VB, VB,
                                                           p["vermilion"]))
    o.append('<circle cx="%s" cy="%s" r="486" fill="%s"/>'
             % (n(C), n(C), p["marigold"]))
    o.append(_scallop_ring(
        C, C, 462, 36,
        [p["turmeric"], p["vermilion"], p["peacock"], p["turmeric"],
         p["green"], p["pink"]], ink, 27))
    o.append('<circle cx="%s" cy="%s" r="432" fill="%s" stroke="%s" '
             'stroke-width="14"/>' % (n(C), n(C), p["cream"], ink))

    # rays behind the head, clipped to the inner disc
    o.append('<g clip-path="url(#disc)">')
    o.append(_sunburst(C, 560, 470, 24, p["turmeric"], p["cream"], rot=7))
    o.append('<circle cx="%s" cy="%s" r="418" fill="url(#dots)" '
             'opacity="0.30"/>' % (n(C), n(C)))
    o.append("</g>")

    # ---- shoulders ------------------------------------------------------
    o.append('<g clip-path="url(#disc)">')
    o.append('<path d="M180 1000 Q210 806 500 792 Q790 806 820 1000 Z" '
             'fill="%s" stroke="%s" stroke-width="13"/>'
             % (p["peacock"], ink))
    o.append('<path d="M430 800 L500 900 L570 800 Z" fill="%s" stroke="%s" '
             'stroke-width="11" stroke-linejoin="round"/>' % (p["cream"], ink))
    o.append("</g>")

    # ---- neck -----------------------------------------------------------
    o.append('<path d="M432 690 L432 800 Q500 836 568 800 L568 690 Z" '
             'fill="%s" stroke="%s" stroke-width="13" '
             'stroke-linejoin="round"/>' % (p["skin_shade"], ink))

    # ---- ears -----------------------------------------------------------
    for sx in (-1, 1):
        o.append('<ellipse cx="%s" cy="486" rx="40" ry="52" fill="%s" '
                 'stroke="%s" stroke-width="13"/>'
                 % (n(C + sx * 214), p["skin"], ink))

    # ---- face -----------------------------------------------------------
    o.append('<path d="M304 380 Q304 268 500 268 Q696 268 696 380 L696 520 '
             'Q696 700 500 700 Q304 700 304 520 Z" fill="%s" stroke="%s" '
             'stroke-width="14"/>' % (p["skin"], ink))
    # cheek blocks -- flat enamel shading, no gradient
    for sx in (-1, 1):
        o.append('<ellipse cx="%s" cy="556" rx="46" ry="30" fill="%s" '
                 'opacity="0.55"/>' % (n(C + sx * 152), p["vermilion"]))

    # ---- hair -----------------------------------------------------------
    o.append('<path d="M292 424 Q288 250 500 250 Q712 250 708 424 '
             'Q676 344 500 344 Q324 344 292 424 Z" fill="%s"/>' % hair)
    o.append(_curls(C, 376, 232, 152, ink, hair))
    for cx_, cy_, rr in ((266, 306, 32), (740, 298, 28), (330, 246, 26),
                         (678, 240, 23)):
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>'
                 % (cx_, cy_, rr, hair))
    o.append('<path d="M292 424 Q288 250 500 250 Q712 250 708 424" '
             'fill="none" stroke="%s" stroke-width="14" '
             'stroke-linecap="round"/>' % ink)
    # two highlight curls so the mass is not a flat blob
    for cx_, cy_, rr in ((392, 300, 17), (600, 296, 14)):
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s" opacity="0.5"/>'
                 % (cx_, cy_, rr, p["marigold"]))

    # ---- sunglasses -----------------------------------------------------
    o.append('<path d="M318 452 L682 452" stroke="%s" stroke-width="16" '
             'stroke-linecap="round"/>' % ink)
    for sx in (-1, 1):
        x = C + sx * 108
        o.append('<rect x="%s" y="440" width="176" height="128" rx="30" '
                 'fill="%s" stroke="%s" stroke-width="15"/>'
                 % (n(x - 88), p["vermilion"], ink))
        o.append('<rect x="%s" y="452" width="152" height="104" rx="22" '
                 'fill="%s"/>' % (n(x - 76), ink))
        # the glint: one hard diagonal, the way enamel paint does a reflection
        o.append('<path d="M%s 548 L%s 462 L%s 462 L%s 548 Z" fill="%s" '
                 'opacity="0.85"/>'
                 % (n(x - 58), n(x - 20), n(x + 6), n(x - 32), p["turmeric"]))
    o.append('<path d="M472 492 Q500 474 528 492" fill="none" stroke="%s" '
             'stroke-width="15" stroke-linecap="round"/>' % ink)

    # ---- nose and mouth --------------------------------------------------
    o.append('<path d="M500 570 L500 616 Q500 632 478 634" fill="none" '
             'stroke="%s" stroke-width="13" stroke-linecap="round" '
             'stroke-linejoin="round"/>' % ink)
    o.append('<path d="M436 664 Q500 706 564 664" fill="none" stroke="%s" '
             'stroke-width="15" stroke-linecap="round"/>' % ink)

    defs = [
        "<defs>",
        '<clipPath id="disc"><circle cx="%s" cy="%s" r="425"/></clipPath>'
        % (n(C), n(C)),
        '<pattern id="dots" width="16" height="16" '
        'patternUnits="userSpaceOnUse">'
        '<circle cx="3" cy="3" r="2.4" fill="%s"/></pattern>' % ink,
        "</defs>",
    ]
    alt = ("Avatar: a curly-haired man in dark sunglasses, painted in Indian "
           "truck-art enamel colours inside a matchbox-label scalloped border")
    return "".join(
        ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'role="img" aria-label="%s">' % (VB, VB, alt)]
        + defs + o + ["</svg>"])
