"""Variant 1 -- Indian truck art x matchbox label.

Maximalist on purpose. The header is the painted rear panel of a truck; each
project is a matchbox label with its own three-colour brand palette, the way
real match brands worked. Flat enamel fills, heavy black outlines, halftone
shading, paper grain, and deliberate colour misregistration -- every vintage
label in the Datawala and Dotz collections is out of register, and a
perfectly registered one reads as a pastiche of the thing rather than the
thing.

Display type comes from src/pathfont.py, utility type from the same bitmap
face the other two variants use. Nothing here needs a font to exist.
"""
import glyphs as g
import pathfont as pf

VB_W = 830
M = 26                      # outer border inset
CW, CH = 3.0, 4.4           # utility type -> 14.1px cap at 380px
ADV = 6 * CW

LIGHT = {
    "paper": "#FDF6E3", "ink": "#111111", "green": "#0B6E4F",
    "marigold": "#F5A623", "vermilion": "#E23E30", "peacock": "#1B5EA8",
    "pink": "#E5187E", "turmeric": "#FFD100", "cream": "#FFF6D8",
    "night": False,
}
DARK = {
    "paper": "#101A3D", "ink": "#050914", "green": "#0A5C44",
    "marigold": "#FFB43D", "vermilion": "#FF5A3D", "peacock": "#2E7BD6",
    "pink": "#FF3D97", "turmeric": "#FFD46B", "cream": "#FFF3D0",
    "night": True,
}


def n(v):
    return g._n(v)


# --- primitives -------------------------------------------------------------

def scallop(x0, x1, y, r, up=True, fill="#000", stroke=None, sw=3):
    """A run of half-circles -- the meenakari edge that borders everything."""
    d = ["M%s %s" % (n(x0), n(y))]
    x = x0
    sweep = 1 if up else 0
    while x + r * 2 <= x1 + 0.01:
        d.append("A%s %s 0 0 %d %s %s" % (n(r), n(r), sweep, n(x + r * 2), n(y)))
        x += r * 2
    if x < x1:
        d.append("L%s %s" % (n(x1), n(y)))
    extra = ' stroke="%s" stroke-width="%s"' % (stroke, n(sw)) if stroke else ""
    return '<path d="%s" fill="%s"%s/>' % (" ".join(d), fill, extra)


def chevron_band(x0, y, w, h, a, b, ink, step=26):
    """Diagonal hazard banding, the strip painted along a truck's bumper."""
    out = ['<g clip-path="url(#cl_%s)">' % n(y).replace(".", "_"),
           '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>'
           % (n(x0), n(y), n(w), n(h), a)]
    x = x0 - h
    while x < x0 + w + h:
        out.append('<path d="M%s %s l%s 0 l%s %s l%s 0 z" fill="%s"/>'
                   % (n(x), n(y + h), n(step), n(h), n(-h), n(-step), b))
        x += step * 2
    out.append("</g>")
    clip = ('<clipPath id="cl_%s"><rect x="%s" y="%s" width="%s" height="%s"/>'
            "</clipPath>" % (n(y).replace(".", "_"), n(x0), n(y), n(w), n(h)))
    frame = ('<rect x="%s" y="%s" width="%s" height="%s" fill="none" '
             'stroke="%s" stroke-width="3"/>' % (n(x0), n(y), n(w), n(h), ink))
    return clip, "".join(out) + frame


def tassels(x0, x1, y, pal, count=22, drop=44):
    """Jhalar. Each strand swings on its own phase or it reads as a machine."""
    cols = [pal["vermilion"], pal["turmeric"], pal["green"], pal["pink"],
            pal["peacock"], pal["marigold"]]
    out = []
    step = (x1 - x0) / float(count)
    for i in range(count):
        x = x0 + step * (i + 0.5)
        c = cols[i % len(cols)]
        d = drop * (0.72 + 0.28 * ((i * 7) % 5) / 4.0)
        out.append(
            '<g transform="translate(%s %s)">'
            '<animateTransform attributeName="transform" type="rotate" '
            'values="-4;4;-4" dur="%ss" begin="%ss" repeatCount="indefinite" '
            'additive="sum"/>'
            '<path d="M0 0 L0 %s" stroke="%s" stroke-width="5" '
            'stroke-linecap="round"/>'
            '<circle cx="0" cy="%s" r="7" fill="%s" stroke="%s" '
            'stroke-width="2.5"/></g>'
            % (n(x), n(y), n(2.6 + (i % 5) * 0.34), n(i * -0.21), n(d), c,
               n(d + 4), c, pal["ink"])
        )
    return "".join(out)


def chakra(cx, cy, r, pal, spokes=12, dur=26):
    """The wheel. Slow enough that you notice it only on the second look."""
    out = ['<g transform="translate(%s %s)">' % (n(cx), n(cy)),
           '<animateTransform attributeName="transform" type="rotate" '
           'from="0" to="360" dur="%ss" repeatCount="indefinite" '
           'additive="sum"/>' % n(dur),
           '<circle r="%s" fill="%s" stroke="%s" stroke-width="4"/>'
           % (n(r), pal["marigold"], pal["ink"]),
           '<circle r="%s" fill="none" stroke="%s" stroke-width="3"/>'
           % (n(r * 0.62), pal["ink"])]
    for i in range(spokes):
        out.append('<path d="M0 %s L0 %s" stroke="%s" stroke-width="4" '
                   'transform="rotate(%s)"/>'
                   % (n(-r * 0.62), n(-r * 0.96), pal["ink"],
                      n(360.0 * i / spokes)))
    out.append('<circle r="%s" fill="%s" stroke="%s" stroke-width="3"/>'
               % (n(r * 0.24), pal["vermilion"], pal["ink"]))
    out.append("</g>")
    return "".join(out)


def nazar(cx, cy, r, pal):
    """Nazar battu. It blinks, rarely, and never while you are reading."""
    return (
        '<g transform="translate(%s %s)">'
        '<circle r="%s" fill="%s" stroke="%s" stroke-width="4"/>'
        '<circle r="%s" fill="%s"/>'
        '<circle r="%s" fill="%s"/>'
        '<circle r="%s" fill="%s"/>'
        '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="0.85"/>'
        '<rect x="%s" y="%s" width="%s" height="%s" fill="%s">'
        '<animate attributeName="height" values="0;0;%s;0;0" dur="7s" '
        'begin="3s" repeatCount="indefinite" keyTimes="0;0.94;0.965;0.99;1"/>'
        "</rect></g>"
        % (n(cx), n(cy), n(r), pal["peacock"], pal["ink"],
           n(r * 0.72), pal["cream"], n(r * 0.46), pal["peacock"],
           n(r * 0.22), pal["ink"],
           n(-r * 0.16), n(-r * 0.2), n(r * 0.1), pal["cream"],
           n(-r), n(-r), n(r * 2), 0, pal["peacock"], n(r * 2))
    )


def feather(cx, cy, s, pal, i=0):
    """One peacock eye-feather. The fan shimmers by hue, not by moving."""
    return (
        '<g transform="translate(%s %s) scale(%s)">'
        '<path d="M0 0 C-6 -34 -22 -54 0 -78 C22 -54 6 -34 0 0 Z" fill="%s" '
        'stroke="%s" stroke-width="3"/>'
        '<ellipse cy="-54" rx="13" ry="17" fill="%s" stroke="%s" '
        'stroke-width="2.5"/>'
        '<ellipse cy="-54" rx="6" ry="8" fill="%s"/>'
        '<animate attributeName="opacity" values="1;0.72;1" dur="%ss" '
        'begin="%ss" repeatCount="indefinite"/>'
        "</g>"
        % (n(cx), n(cy), n(s), pal["green"], pal["ink"],
           pal["peacock"], pal["ink"], pal["marigold"],
           n(4.2 + i * 0.5), n(i * 0.6))
    )


def lotus(cx, cy, s, pal, petal=None, core=None):
    petal = petal or pal["pink"]
    core = core or pal["turmeric"]
    out = ['<g transform="translate(%s %s) scale(%s)">' % (n(cx), n(cy), n(s))]
    for a in (-72, -36, 0, 36, 72):
        out.append('<path d="M0 0 C-16 -22 -16 -44 0 -60 C16 -44 16 -22 0 0 Z" '
                   'fill="%s" stroke="%s" stroke-width="3" '
                   'transform="rotate(%d)"/>' % (petal, pal["ink"], a))
    out.append('<circle cy="-8" r="11" fill="%s" stroke="%s" stroke-width="3"/>'
               % (core, pal["ink"]))
    out.append("</g>")
    return "".join(out)


def tiger(cx, cy, s, pal, coat=None):
    """A brand mark, not a portrait -- match labels drew animals flat."""
    coat = coat or pal["marigold"]
    o, cream = pal["ink"], pal["cream"]
    out = ['<g transform="translate(%s %s) scale(%s)">' % (n(cx), n(cy), n(s))]
    for sx in (-1, 1):
        out.append('<path d="M%d -34 L%d -76 L%d -44 Z" fill="%s" stroke="%s" '
                   'stroke-width="3.5" stroke-linejoin="round"/>'
                   % (sx * 52, sx * 40, sx * 16, coat, o))
        out.append('<path d="M%d -40 L%d -66 L%d -44 Z" fill="%s"/>'
                   % (sx * 44, sx * 39, sx * 24, pal["vermilion"]))
    out.append('<path d="M-50 -22 Q-56 22 -30 42 Q0 58 30 42 Q56 22 50 -22 '
               'Q40 -46 0 -46 Q-40 -46 -50 -22 Z" fill="%s" stroke="%s" '
               'stroke-width="4"/>' % (coat, o))
    for sx in (-1, 1):
        for k in range(3):
            out.append('<path d="M%d %d Q%d %d %d %d" stroke="%s" '
                       'stroke-width="6" fill="none" stroke-linecap="round"/>'
                       % (sx * (20 + k * 11), -38 + k * 3,
                          sx * (26 + k * 11), -22 + k * 4,
                          sx * (22 + k * 11), -6 + k * 6, o))
    out.append('<path d="M-38 -18 L-12 -10 M38 -18 L12 -10" stroke="%s" '
               'stroke-width="6" stroke-linecap="round"/>' % o)
    for sx in (-1, 1):
        out.append('<path d="M%d -6 L%d 2 L%d 8 Z" fill="%s" stroke="%s" '
                   'stroke-width="2.5" stroke-linejoin="round"/>'
                   % (sx * 34, sx * 12, sx * 34, cream, o))
        out.append('<circle cx="%d" cy="1" r="5" fill="%s"/>' % (sx * 23, o))
    out.append('<ellipse cy="26" rx="30" ry="20" fill="%s" stroke="%s" '
               'stroke-width="3"/>' % (cream, o))
    out.append('<path d="M-11 18 L11 18 L0 28 Z" fill="%s"/>' % o)
    out.append('<path d="M0 28 L0 34 M0 34 Q-11 44 -20 36 M0 34 Q11 44 20 36" '
               'stroke="%s" stroke-width="3.5" fill="none" '
               'stroke-linecap="round"/>' % o)
    for sx in (-1, 1):
        for k in range(3):
            out.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="2.5" '
                       'stroke-linecap="round"/>'
                       % (n(sx * 24), n(20 + k * 6), n(sx * 56), n(12 + k * 11), o))
    out.append("</g>")
    return "".join(out)


def anvil(cx, cy, s, pal, body=None):
    body = body or pal["peacock"]
    o = pal["ink"]
    return (
        '<g transform="translate(%s %s) scale(%s)">'
        '<path d="M-44 -14 L40 -14 L46 2 L18 2 L14 22 L22 38 L-22 38 L-14 22 '
        'L-18 2 L-46 2 Z" fill="%s" stroke="%s" stroke-width="3.5"/>'
        '<path d="M-44 -14 L-56 -6 L-44 0 Z" fill="%s" stroke="%s" '
        'stroke-width="3"/>'
        '<g><path d="M0 -22 C-12 -40 8 -46 0 -66 C16 -48 12 -34 0 -22 Z" '
        'fill="%s" stroke="%s" stroke-width="3">'
        '<animate attributeName="opacity" values="1;0.55;1;0.8;1" dur="1.7s" '
        'repeatCount="indefinite"/></path>'
        '<path d="M0 -26 C-6 -38 4 -42 0 -54 C8 -42 6 -34 0 -26 Z" fill="%s">'
        '<animate attributeName="opacity" values="0.9;0.4;1;0.6;0.9" '
        'dur="1.1s" repeatCount="indefinite"/></path></g>'
        "</g>"
        % (n(cx), n(cy), n(s), body, o, body, o,
           pal["vermilion"], o, pal["turmeric"])
    )


def mesh(cx, cy, s, pal, node=None):
    """The WSN label's mark: a sensor mesh electing a cluster head."""
    node = node or pal["green"]
    o = pal["ink"]
    pts = [(0, -34), (-38, -12), (38, -12), (-24, 30), (24, 30), (0, 4)]
    out = ['<g transform="translate(%s %s) scale(%s)">' % (n(cx), n(cy), n(s))]
    for a, b in ((5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (0, 1), (0, 2),
                 (3, 4)):
        out.append('<path d="M%d %d L%d %d" stroke="%s" stroke-width="3"/>'
                   % (pts[a][0], pts[a][1], pts[b][0], pts[b][1], o))
    for i, (x, y) in enumerate(pts):
        r, c = (15, pal["marigold"]) if i == 5 else (10, node)
        out.append('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" '
                   'stroke-width="3">'
                   '<animate attributeName="r" values="%d;%s;%d" dur="%ss" '
                   'begin="%ss" repeatCount="indefinite"/></circle>'
                   % (x, y, r, c, o, r, n(r * 1.18), r, n(3.0 + i * 0.4),
                      n(i * 0.5)))
    out.append("</g>")
    return "".join(out)


def ribbon(x, y, w, h, pal, fill=None):
    """A banner with swallow-tail ends, for lettering panels."""
    fill = fill or pal["vermilion"]
    t = h * 0.42
    return (
        '<path d="M%s %s L%s %s L%s %s L%s %s L%s %s L%s %s L%s %s L%s %s Z" '
        'fill="%s" stroke="%s" stroke-width="3.5" stroke-linejoin="round"/>'
        % (n(x), n(y), n(x + w), n(y), n(x + w + t), n(y + h / 2),
           n(x + w), n(y + h), n(x), n(y + h), n(x - t), n(y + h / 2),
           n(x), n(y), n(x), n(y), fill, pal["ink"])
    )


# --- composition ------------------------------------------------------------

ABOUT = [
    "I BUILD AGENT SYSTEMS, THEN I BUILD",
    "THE THING THAT GRADES THEM. A BENCHMARK",
    "THAT ONLY REPORTS ITS WINS IS NOT",
    "MEASURING ANYTHING.",
]

LABELS = [
    {
        "brand": "LEX GRAPH", "strip": "GRAPHRAG SAFETY MATCHES",
        "regd": "REGD. LG   MADE IN DELHI",
        "body": ["GRAPHRAG OVER JUDGMENTS OF",
                 "THE INDIAN SUPREME COURT.",
                 "FLAT VECTOR SEARCH AGAINST",
                 "A KNOWLEDGE GRAPH. SAME",
                 "CORPUS, SAME QUESTIONS,",
                 "SAME METRICS."],
        "tags": "PYTHON  NETWORKX  CHROMADB",
        "motif": "tiger", "keys": ("vermilion", "turmeric", "cream"),
        "fine": "PRODUCT OF INDIA",
    },
    {
        "brand": "QUERY FORGE", "strip": "AGENTIC INDEX WORKS",
        "regd": "REGD. QF   MADE IN DELHI",
        "body": ["AN LLM PROPOSES POSTGRES",
                 "INDEXES. A REAL BENCHMARK",
                 "GRADES THEM -- THE ACTUAL",
                 "PLANNER ON THE ACTUAL",
                 "WORKLOAD, NOT A SECOND",
                 "MODEL SCORING THE FIRST."],
        "tags": "LANGGRAPH  MCP  LANGFUSE",
        "motif": "anvil", "keys": ("peacock", "pink", "cream"),
        "fine": "STRIKE ON BOX ONLY",
    },
    {
        "brand": "H I E C F", "strip": "WIRELESS SENSOR RESEARCH",
        "regd": "TWO PAPERS   UNDER REVIEW",
        "body": ["CLUSTERING PROTOCOLS ALL",
                 "BENCHMARKED IN ONE SINGLE",
                 "FRAMEWORK, WITH MAIT",
                 "FACULTY. HIECF PAIRS TYPE-2",
                 "FUZZY LOGIC WITH Q-LEARNING",
                 "FOR CLUSTER HEAD SELECTION."],
        "tags": "FUZZY LOGIC  REINFORCEMENT LEARNING",
        "motif": "mesh", "keys": ("green", "marigold", "cream"),
        "fine": "SIX AUTHORS",
    },
]

ROAD = [
    ("DRDO", "RESEARCH INTERN", [
        "SCIENTIFIC ANALYSIS GROUP. A CLIENT-",
        "SERVER SYSTEM FOR SOFTWARE DEFINED",
        "RADIOS IN JAVA. IRSS APIS OVER TCP,",
        "AES-256 WITH A FRESH IV PER MESSAGE."]),
    ("CANTILEVER LABS", "AI ENGINEER INTERN", [
        "RAG CHATBOT WITH SOURCE-GROUNDED",
        "ANSWERS. IMAGE CAPTIONING AND NLP",
        "TRIAGE MODELS."]),
    ("TRAINING & PLACEMENT CELL", "CORPORATE RELATIONS", [
        "MAIT DELHI. RECRUITER OUTREACH AND",
        "ON-CAMPUS DRIVES RUN END TO END."]),
]

PLATES = [
    ("LANGUAGES", "PYTHON  JAVA  SQL  C++"),
    ("AGENTS", "LANGCHAIN  LANGGRAPH  CREWAI"),
    ("RETRIEVAL", "RAG  GRAPHRAG  RAGAS  CHROMADB"),
    ("SERVING", "FASTAPI  DOCKER  VLLM  SGLANG"),
    ("RUNTIMES", "OLLAMA  MCP  PYTORCH"),
    ("TRACING", "LANGFUSE  LANGSMITH"),
    ("DATA", "POSTGRES  LANCEDB  NETWORKX"),
    ("NUMERICS", "NUMPY  PANDAS  HUGGING FACE"),
]

CONTACT = [
    ("PORTFOLIO", "SATVIKRASTOGI.VERCEL.APP"),
    ("GITHUB", "GITHUB.COM/SATVIKRASTOGII"),
    ("LINKEDIN", "LINKEDIN.COM/IN/SATVIKRASTOGII"),
    ("LEETCODE", "LEETCODE.COM/U/BLACKMANCODES"),
    ("EMAIL", "SATVIKRASTOGI777@GMAIL.COM"),
]


class Panel(object):
    def __init__(self, pal):
        self.p = pal
        self.defs = []
        self.out = []
        self.chars = set()
        self.words = {}
        self.y = 0

    def small(self, s, x, y, colour, cw=CW, ch=CH, anchor="start",
              opacity=None):
        # glyph box is g.H rows, not the 7-row cap; leading has to clear it
        if not s.strip():
            return ""
        self.chars |= set(s)
        w = g.text_width(s, cw)
        if anchor == "middle":
            x -= w / 2.0
        elif anchor == "end":
            x -= w
        extra = ' fill="%s"' % colour
        if opacity is not None:
            extra += ' opacity="%s"' % opacity
        return g.run(s, x, y, cw, ch, extra)

    def word(self, s, tracking=22):
        """Register a display word once; returns its id and width."""
        key = (s, tracking)
        if key not in self.words:
            gid = "w%d" % len(self.words)
            self.words[key] = (gid, pf.width(s, tracking))
            self.defs.append(pf.group(s, gid, tracking))
        return self.words[key]


def _misregistered(inner, dx, dy, colour, opacity=0.5):
    """A second impression, off-register. The press was cheap; that is why
    these labels look the way they do."""
    return ('<g transform="translate(%s %s)" opacity="%s" '
            'style="mix-blend-mode:multiply" fill="%s">%s</g>'
            % (n(dx), n(dy), n(opacity), colour, inner))

def _label(p, y, spec):
    """One matchbox label. Three colours plus the black, like a real brand."""
    pal = p.p
    k1, k2, k3 = spec["keys"]
    c1, c2, c3 = pal[k1], pal[k2], pal[k3]
    ink = pal["ink"]
    x0, x1 = M + 14, VB_W - M - 14
    w = x1 - x0
    h = 474
    o = []
    # plate: outer keyline, colour ground, inner keyline, scalloped inner edge
    o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s" '
             'stroke="%s" stroke-width="5"/>' % (n(x0), n(y), n(w), n(h), c1, ink))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="%s" '
             'stroke="%s" stroke-width="3"/>'
             % (n(x0 + 13), n(y + 13), n(w - 26), n(h - 26), c3, ink))
    o.append(scallop(x0 + 13, x1 - 13, y + 13, 9, True, c1))
    o.append(scallop(x0 + 13, x1 - 13, y + h - 13, 9, False, c1))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#dots)" '
             'opacity="0.45"/>' % (n(x0 + 14), n(y + 14), n(w - 28), n(h - 28)))

    mx, my = x0 + 106, y + 186
    motif = {"tiger": tiger, "anvil": anvil, "mesh": mesh}[spec["motif"]]
    o.append(motif(mx, my, 1.02, pal, c1))

    tx = x0 + 196
    gid, gw = p.word(spec["brand"], 20)
    bs = min(0.40, (x1 - 36 - tx) / gw)
    o.append(pf.painted(gid, tx, y + 38, bs, c1, ink, c2,
                        highlight=pal["cream"]))
    hy = y + 38 + pf.CAP * bs + 16
    o.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="3"/>'
             % (n(tx), n(hy), n(x1 - 36), n(hy), ink))
    o.append(p.small(spec["strip"], tx, hy + 12, ink, 2.6, 3.9))
    ty = hy + 54
    for ln in spec["body"]:
        o.append(p.small(ln, tx, ty, ink))
        ty += 36
    o.append(p.small(spec["tags"], tx, ty + 6, c1, 2.6, 3.9))

    o.append('<path d="M%s %s L%s %s" stroke="%s" stroke-width="3"/>'
             % (n(x0 + 26), n(y + h - 48), n(x1 - 26), n(y + h - 48), ink))
    o.append(p.small(spec["regd"], x0 + 26, y + h - 40, ink, 2.4, 3.6))
    o.append(p.small(spec["fine"], x1 - 26, y + h - 40, ink, 2.4, 3.6,
                     anchor="end"))
    return "".join(o), h


def render(stats, dark=True):
    pal = DARK if dark else LIGHT
    p = Panel(pal)
    ink, cream = pal["ink"], pal["cream"]
    x0, x1 = M, VB_W - M
    inner = x1 - x0
    cx = VB_W / 2.0

    # ---------------- header: the painted rear panel ----------------------
    y = M + 18
    clip, band = chevron_band(x0 + 10, y, inner - 20, 30,
                              pal["marigold"], ink, ink)
    p.defs.append(clip)
    p.out.append(band)
    y += 30

    px0, px1 = x0 + 10, x1 - 10
    panel_top = y + 12
    panel_h = 716
    p.out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="12" '
                 'fill="%s" stroke="%s" stroke-width="5"/>'
                 % (n(px0), n(panel_top), n(px1 - px0), n(panel_h),
                    pal["green"], ink))
    p.out.append(scallop(px0 + 8, px1 - 8, panel_top + 8, 11, True,
                         pal["marigold"]))
    p.out.append(scallop(px0 + 8, px1 - 8, panel_top + panel_h - 8, 11, False,
                         pal["marigold"]))
    if pal["night"]:
        # the reader is the vehicle behind; this is their headlights on the
        # panel. it has to be painted over the enamel, not under it.
        p.out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" '
                     'fill="url(#beam)"/>'
                     % (n(cx), n(panel_top + panel_h * 0.44),
                        n((px1 - px0) * 0.60), n(panel_h * 0.56)))

    ry = panel_top + 34
    # Narrow letters -- L, E, I, T -- have side bearings smaller than the
    # outline's half-width, so at the panel weight the black welds shut and
    # PLEASE reads as one blob. Lighter stroke and wider tracking, checked
    # against four alternatives before picking these numbers.
    gid, gw = p.word("STAR OK PLEASE", 38)
    rs = min(0.42, 568.0 / gw)
    rw = gw * rs
    p.out.append(ribbon(cx - rw / 2 - 28, ry, rw + 56, 64, pal))
    p.out.append(pf.painted(gid, cx - rw / 2, ry + 9, rs, pal["turmeric"], ink,
                            pal["ink"], out_w=36, weight=26, shadow_dx=5,
                            shadow_dy=6))

    ny = ry + 104
    fan_x, fan_y = px0 + 80, ny + 300
    for i, a in enumerate((-34, -17, 0, 17, 34)):
        p.out.append('<g transform="rotate(%s %s %s)">%s</g>'
                     % (n(a), n(fan_x), n(fan_y),
                        feather(fan_x, fan_y, 1.35, pal, i)))
    p.out.append(nazar(px1 - 88, ny + 128, 50, pal))

    for word, dy, colour in (("SATVIK", 0, pal["turmeric"]),
                             ("RASTOGI", 154, pal["marigold"])):
        gid, gw = p.word(word, 20)
        s = min(0.80, 430.0 / gw)
        w = gw * s
        # The one deliberate misprint. The colour plate sits three units off
        # the black plate, the way every label in the reference does.
        p.out.append(pf.painted(gid, cx - w / 2, ny + dy, s, colour, ink,
                                pal["vermilion"], highlight=cream))
        p.out.append('<use href="#%s" transform="translate(%s %s) scale(%s)" '
                     'fill="none" stroke="%s" stroke-width="%s" opacity="0.3" '
                     'style="mix-blend-mode:multiply" stroke-linecap="round" '
                     'stroke-linejoin="round"/>'
                     % (gid, n(cx - w / 2 - 2.5), n(ny + dy - 3), n(s),
                        pal["pink"], n(36 / s)))

    sy = ny + 336
    p.out.append(p.small("AI / AGENTIC ENGINEER", cx, sy, cream, 3.4, 5.0,
                         anchor="middle"))
    p.out.append(p.small("DELHI, INDIA   .   GRADUATING 2027", cx, sy + 42,
                         pal["marigold"], 2.8, 4.2, anchor="middle"))

    by = sy + 86
    bw, bh = 452, 104
    p.out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="8" fill="%s" '
                 'stroke="%s" stroke-width="5"/>'
                 % (n(cx - bw / 2), n(by), n(bw), n(bh), cream, ink))
    p.out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" '
                 'fill="none" stroke="%s" stroke-width="2.5"/>'
                 % (n(cx - bw / 2 + 8), n(by + 8), n(bw - 16), n(bh - 16),
                    pal["vermilion"]))
    p.out.append(p.small("ALL INDIA WORK PERMIT", cx, by + 20, pal["vermilion"],
                         3.0, 4.6, anchor="middle"))
    p.out.append(p.small("OPEN TO WORK", cx, by + 54, ink, 3.6, 5.4,
                         anchor="middle"))
    p.out.append(chakra(px0 + 76, by + bh / 2, 42, pal))
    p.out.append(chakra(px1 - 76, by + bh / 2, 42, pal, dur=31))

    y = panel_top + panel_h
    p.out.append(tassels(px0 + 16, px1 - 16, y, pal))
    y += 100

    # ---------------- about -----------------------------------------------
    ah = 236
    p.out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s" '
                 'stroke="%s" stroke-width="5"/>'
                 % (n(x0 + 14), n(y), n(inner - 28), n(ah), pal["vermilion"],
                    ink))
    p.out.append(scallop(x0 + 22, x1 - 22, y + 8, 9, True, pal["turmeric"]))
    ay = y + 54
    for ln in ABOUT:
        p.out.append(p.small(ln, cx, ay, cream, 3.0, 4.6, anchor="middle"))
        ay += 40
    y += ah + 44

    # ---------------- the labels -------------------------------------------
    gid, gw = p.word("THE LABELS", 18)
    s = 0.32
    p.out.append(pf.painted(gid, cx - gw * s / 2, y, s, pal["turmeric"], ink,
                            pal["vermilion"], highlight=cream))
    y += pf.CAP * s + 28
    for spec in LABELS:
        chunk, h = _label(p, y, spec)
        p.out.append(chunk)
        y += h + 26

    # ---------------- the road so far --------------------------------------
    y += 18
    gid, gw = p.word("THE ROAD SO FAR", 18)
    s = 0.28
    p.out.append(pf.painted(gid, cx - gw * s / 2, y, s, pal["marigold"], ink,
                            pal["vermilion"], highlight=cream))
    y += pf.CAP * s + 26
    accents = [pal["vermilion"], pal["peacock"], pal["green"]]
    for i, (org, role, lines) in enumerate(ROAD):
        # height follows the copy: fixed cards clipped the longest entry
        rh = 108 + len(lines) * 34 + 16
        p.out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="8" '
                     'fill="%s" stroke="%s" stroke-width="4"/>'
                     % (n(x0 + 14), n(y), n(inner - 28), n(rh),
                        "#16224E" if pal["night"] else cream, ink))
        p.out.append('<rect x="%s" y="%s" width="12" height="%s" fill="%s"/>'
                     % (n(x0 + 14), n(y), n(rh), accents[i]))
        p.out.append(lotus(x0 + 82, y + rh - 36, 0.56, pal, accents[i],
                           pal["turmeric"]))
        tx = x0 + 140
        p.out.append(p.small(org, tx, y + 24, cream if pal["night"] else ink,
                             3.2, 4.8))
        p.out.append(p.small(role, tx, y + 66, accents[i], 2.6, 3.9))
        ly = y + 108
        for ln in lines:
            p.out.append(p.small(ln, tx, ly, cream if pal["night"] else ink,
                                 2.7, 4.1))
            ly += 34
        y += rh + 16

    # ---------------- toolkit plates ---------------------------------------
    y += 26
    gid, gw = p.word("TOOLKIT", 18)
    s = 0.28
    p.out.append(pf.painted(gid, cx - gw * s / 2, y, s, pal["turmeric"], ink,
                            pal["vermilion"], highlight=cream))
    y += pf.CAP * s + 24
    plate_cols = [pal["green"], pal["vermilion"], pal["peacock"],
                  pal["marigold"], pal["pink"], pal["peacock"],
                  pal["green"], pal["vermilion"]]
    for i, (k, v) in enumerate(PLATES):
        ph = 54
        p.out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="7" '
                     'fill="%s" stroke="%s" stroke-width="4"/>'
                     % (n(x0 + 14), n(y), n(inner - 28), n(ph), cream, ink))
        p.out.append('<path d="M%s %s h186 v%s h-179 a7 7 0 0 1 -7 -7 z" '
                     'fill="%s"/>'
                     % (n(x0 + 21), n(y + 2), n(ph - 4), plate_cols[i]))
        p.out.append(p.small(k, x0 + 32, y + 18, cream, 2.8, 4.2))
        p.out.append(p.small(v, x0 + 224, y + 18, ink, 2.8, 4.2))
        y += ph + 10

    # ---------------- mudflap ----------------------------------------------
    y += 30
    mh = 316
    p.out.append('<path d="M%s %s h%s v%s q0 26 -26 26 h%s q-26 0 -26 -26 z" '
                 'fill="%s" stroke="%s" stroke-width="5"/>'
                 % (n(x0 + 14), n(y), n(inner - 28), n(mh - 26),
                    n(-(inner - 28 - 52)), pal["ink"], pal["marigold"]))
    p.out.append(scallop(x0 + 30, x1 - 30, y + 14, 9, True, pal["marigold"]))
    p.out.append(p.small("BURI NAZAR WAALE,", cx, y + 46, pal["turmeric"],
                         3.2, 4.8, anchor="middle"))
    p.out.append(p.small("TERA FORK BHI NA CHALE", cx, y + 82, pal["turmeric"],
                         3.2, 4.8, anchor="middle"))
    p.out.append(p.small("USE DIPPER AT NIGHT  .  DARK MODE IS THE SAME TRUCK", cx, y + 120, pal["marigold"], 2.4, 3.6,
                         anchor="middle"))

    # The number plate. The only digits on this panel, and a plate is the one
    # thing on a truck that has to be true.
    def num(v):
        return "--" if v is None else "{:,}".format(v)

    plate_w, plate_h = 560, 116
    py = y + 146
    p.out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="8" '
                 'fill="%s" stroke="%s" stroke-width="4"/>'
                 % (n(cx - plate_w / 2), n(py), n(plate_w), n(plate_h),
                    cream, ink))
    p.out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" '
                 'fill="none" stroke="%s" stroke-width="2"/>'
                 % (n(cx - plate_w / 2 + 7), n(py + 7), n(plate_w - 14),
                    n(plate_h - 14), pal["vermilion"]))
    p.out.append(p.small("%s COMMITS  .  %s STARS"
                         % (num(stats.get("commits_year")),
                            num(stats.get("stars"))),
                         cx, py + 22, ink, 3.0, 4.6, anchor="middle"))
    p.out.append(p.small("%s REPOS  .  %s DAY STREAK"
                         % (num(stats.get("public_repos")),
                            num(stats.get("current_streak"))),
                         cx, py + 66, ink, 3.0, 4.6, anchor="middle"))
    p.out.append(p.small("PULLED FROM THE GITHUB API THIS MORNING",
                         cx, py + plate_h + 12, pal["marigold"], 2.4, 3.6,
                         anchor="middle"))
    y += mh + 30

    for k, v in CONTACT:
        p.out.append(p.small(k, x0 + 22, y, pal["vermilion"], 2.8, 4.2))
        p.out.append(p.small(v, x0 + 200, y, cream if pal["night"] else ink,
                             2.8, 4.2))
        y += 34
    y += 12

    H = int(y + M + 30)

    # ---------------- frame, texture, assembly ------------------------------
    frame = [
        '<rect width="%d" height="%d" fill="%s"/>' % (VB_W, H, pal["paper"]),
        '<rect x="8" y="8" width="%s" height="%s" fill="none" stroke="%s" '
        'stroke-width="6"/>' % (VB_W - 16, H - 16, ink),
        '<rect x="17" y="17" width="%s" height="%s" fill="none" stroke="%s" '
        'stroke-width="3"/>' % (VB_W - 34, H - 34, pal["vermilion"]),
        scallop(21, VB_W - 21, 21, 10, True, pal["marigold"]),
        scallop(21, VB_W - 21, H - 21, 10, False, pal["marigold"]),
    ]

    defs = ["<defs>"]
    if pal["night"]:
        defs.append('<radialGradient id="beam">'
                    '<stop offset="0" stop-color="#FFC773" stop-opacity="0.34"/>'
                    '<stop offset="0.55" stop-color="#FF9B3D" '
                    'stop-opacity="0.13"/>'
                    '<stop offset="1" stop-color="#FF9B3D" stop-opacity="0"/>'
                    "</radialGradient>")
    defs.append('<pattern id="dots" width="9" height="9" '
                'patternUnits="userSpaceOnUse">'
                '<circle cx="2" cy="2" r="1.5" fill="%s" opacity="0.5"/>'
                "</pattern>" % ink)
    defs.append('<filter id="grain" x="0" y="0" width="100%" height="100%">'
                '<feTurbulence type="fractalNoise" baseFrequency="0.85" '
                'numOctaves="3" stitchTiles="stitch"/>'
                '<feColorMatrix type="saturate" values="0"/></filter>')
    defs.append(g.defs_for(p.chars))
    defs.append("".join(p.defs))
    defs.append("</defs>")

    grain = ('<rect width="%d" height="%d" filter="url(#grain)" '
             'opacity="%s" style="mix-blend-mode:multiply"/>'
             % (VB_W, H, "0.06" if not pal["night"] else "0.12"))

    alt = ("Satvik Rastogi, a profile painted as an Indian truck rear panel "
           "with matchbox-label project cards")
    return "".join(
        ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'role="img" aria-label="%s">' % (VB_W, H, alt)]
        + defs + frame + p.out + [grain, "</svg>"])
