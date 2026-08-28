"""Variant 2 -- terminal.

Restrained where variant 1 is loud. Every character is a <use> of a glyph
defined once at unit scale, so the character grid is exact and nothing
depends on a font the reader might not have.

The terminal is 42 columns wide. That is what 380px allows at 14px cap
height, and it is the constraint that wrote the copy.
"""
import glyphs as g

VB_W = 830
CW, CH = 3.0, 4.4          # glyph cell -- 7 rows => 30.8u cap => 14.1px at 380
ADV = (g.W + g.GAP) * CW   # 18u per column
CAP = g.CAPR * CH   # visual cap height; row 7 is the descender row
LH = 46                    # line pitch
X0 = 34                    # left text edge
COLS = 42

DARK = {
    "canvas": "#0d1117", "inset": "#010409", "edge": "#30363d",
    "green": "#3fb950", "bright": "#39d353", "hi": "#7ee787",
    "muted": "#8b949e", "text": "#f0f6fc", "link": "#58a6ff",
    "bar": ["#39d353", "#3fb950", "#2ea043", "#238636", "#1a7f37"],
    "crt": True,
}
LIGHT = {
    "canvas": "#ffffff", "inset": "#f6f8fa", "edge": "#d1d9e0",
    "green": "#1a7f37", "bright": "#1f883d", "hi": "#116329",
    "muted": "#59636e", "text": "#1f2328", "link": "#0969da",
    "bar": ["#1f883d", "#2da44e", "#3fb950", "#57ab5a", "#7ee787"],
    "crt": False,
}


def n(v):
    return g._n(v)


class Screen(object):
    def __init__(self, pal):
        self.p = pal
        self.bg = []
        self.fg = []
        self.defs = []
        self.chars = set()
        self.y = 0
        self.walk = []   # block-cursor path, one stop per character

    def use(self, s, x, y, key, opacity=None, glow=False):
        if not s.strip():
            return ""
        self.chars |= set(s)
        extra = ' fill="%s"' % self.p[key]
        if opacity is not None:
            extra += ' opacity="%s"' % opacity
        if glow and self.p["crt"]:
            # phosphor bleed is grime on a white page -- light theme skips it
            extra += ' filter="url(#bleed)"'
        return g.run(s, x, y, CW, CH, extra)

    def line(self, segs, indent=0, glow=False, typed=False):
        """segs: list of (text, palette-key). Laid out on the column grid."""
        col = indent
        parts = []
        for text, key in segs:
            parts.append(self.use(text, X0 + col * ADV, self.y, key, glow=glow))
            col += len(text)
        if typed and col > indent:
            # The cursor walks over text that is already on screen. A clipPath
            # reveal would look identical to a human, but any renderer that
            # samples the SMIL clock at t=0 -- and every rasteriser I could
            # test does -- would show an empty terminal forever. Nothing here
            # is allowed to depend on the animation having run.
            for c in range(indent, col + 1):
                self.walk.append((X0 + c * ADV, self.y))
            self.walk.extend([(X0 + col * ADV, self.y)] * 6)   # beat
        self.fg.append("".join(parts))
        self.y += LH
        return self

    def gap(self, k=1):
        self.y += int(LH * k)
        return self

    def inset(self, y0, y1, x0=X0 - 12, x1=VB_W - 26):
        self.bg.append(
            '<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="%s" '
            'stroke="%s" stroke-width="1"/>'
            % (n(x0), n(y0), n(x1 - x0), n(y1 - y0), self.p["inset"],
               self.p["edge"])
        )


# --- content ---------------------------------------------------------------

BOOT = [
    "booting satvik.profile",
    "[ ok ] mounted /projects",
    "[ ok ] loaded stack.d",
    "[ ok ] gh api: contributions",
]

ABOUT = [
    "i build rag and agent systems",
    "(sometimes websites)",
]

PROJECTS = [
    ("cat projects/lexgraph.md", [
        "graphrag legal knowledge navigator over",
        "indian supreme court judgments. two",
        "retrieval pipelines: flat vector search",
        "and a knowledge graph -- read the same",
        "corpus, answer the same questions, get",
        "judged on the same metrics. hybrid",
        "semantic router, contradiction detection",
        "for overruled precedent. runs local.",
    ], "python networkx chromadb llama 3.1"),
    ("cat projects/queryforge.md", [
        "agentic postgres index advisor. an llm",
        "proposes index configurations; a real",
        "database benchmark grades them -- the",
        "actual query planner on the actual",
        "workload, not a second model scoring it.",
        "propose, benchmark, archive, repeat.",
        "read-only allowlist, least-privilege",
        "role, hard storage budget.",
    ], "langgraph mcp langfuse postgres"),
    ("cat research/wsn.md", [
        "two papers under review, six authors,",
        "with mait faculty. one benchmarks",
        "classical, threshold-based and ai-driven",
        "clustering protocols under a single",
        "simulation framework. the other, hiecf,",
        "pairs type-2 fuzzy logic with q-learning",
        "for cluster head selection.",
    ], "fuzzy logic  reinforcement learning"),
]

ROLES = [
    ("drdo, scientific analysis group", "research intern", [
        "distributed client-server system for",
        "software defined radios. java 17, irss",
        "apis over tcp sockets, aes-256 channels",
        "with a fresh iv per message. without it",
        "the channel leaks its own structure.",
    ]),
    ("cantilever labs", "ai engineer intern", [
        "rag chatbot over a document corpus with",
        "source-grounded answers. plus image",
        "captioning and nlp triage models.",
    ]),
    ("training & placement cell, mait", "corporate relations", [
        "recruiter outreach, on-campus drives run",
        "end to end.",
    ]),
]

STACK = [
    ("languages", ["python  java  sql  c++"]),
    ("agents", ["langchain  langgraph  mcp",
                "rag  graphrag  ragas",
                "guardrails  litellm"]),
    ("serving", ["fastapi  docker  ollama",
                 "langfuse  langsmith  git"]),
    ("data", ["postgres  chromadb  networkx",
              "numpy  pandas  matplotlib",
              "seaborn  beautifulsoup"]),
    ("models", ["pytorch  tensorflow",
                "scikit-learn  hugging face"]),
]

CONTACT = [
    ("portfolio", "satvikrastogi.vercel.app"),
    ("github", "github.com/satvikrastogii"),
    ("linkedin", "linkedin.com/in/satvikrastogii"),
    ("leetcode", "leetcode.com/u/blackmancodes"),
    ("email", "satvikrastogi777@gmail.com"),
]


def _fmt(v):
    return "--" if v is None else "{:,}".format(v)


def _logo(pal, x, y):
    """Knowledge-graph mark: the neofetch slot, drawn not borrowed."""
    nodes = [(52, 52), (52, 0), (104, 52), (52, 104), (0, 52)]
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1)]
    out = ['<g transform="translate(%s %s)">' % (n(x), n(y))]
    for i, (a, b) in enumerate(edges):
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        out.append(
            '<path id="edge%d" d="M%d %dL%d %d" stroke="%s" stroke-width="2.5" '
            'opacity="0.5"/>' % (i, x1 + 8, y1 + 8, x2 + 8, y2 + 8,
                                  pal["green"])
        )
    for i, (nx, ny) in enumerate(nodes):
        out.append(
            '<rect x="%d" y="%d" width="17" height="17" rx="4" fill="%s">'
            '<animate attributeName="opacity" values="1;0.45;1" dur="%ss" '
            'begin="%ss" repeatCount="indefinite"/></rect>'
            % (nx, ny, pal["bright"] if i == 2 else pal["green"],
               n(3.4 + i * 0.37), n(i * 0.6))
        )
    out.append(
        '<circle r="4.5" fill="%s"><animateMotion dur="4.6s" '
        'repeatCount="indefinite"><mpath href="#edge0"/></animateMotion>'
        "</circle>" % pal["hi"]
    )
    out.append("</g>")
    return "".join(out)


def _langbar(s, pal, x, y, langs):
    w = 232.0
    if not langs:
        return s.use("--", x, y, "muted")
    out = []
    cx = x
    for i, L in enumerate(langs[:5]):
        seg = w * (L.get("pct", 0) / 100.0)
        if seg < 1:
            continue
        out.append(
            '<rect x="%s" y="%s" width="%s" height="10" rx="2" fill="%s"/>'
            % (n(cx), n(y + 5), n(max(seg - 2, 1)), pal["bar"][i % 5])
        )
        cx += seg
    names = "  ".join(L["name"].lower() for L in langs[:3])
    out.append(s.use(names, x, y + 22, "muted"))
    return "".join(out)


def render(stats, dark=True):
    pal = DARK if dark else LIGHT
    s = Screen(pal)

    bar_h = 44
    win_y = 8
    s.y = win_y + bar_h + 34

    for b in BOOT:
        if b.startswith("[ ok ]"):
            s.line([("[ ok ]", "green"), (b[6:], "muted")], typed=True)
        else:
            s.line([(b, "muted")], typed=True)
    s.gap(0.6)

    # --- neofetch ---------------------------------------------------------
    nf_top = s.y - 16
    logo_y = s.y
    rx = 176
    vx = rx + 8 * ADV
    rows = [
        ("role", "ai / agentic engineer"),
        ("school", "b.tech cs, mait delhi"),
        ("grad", "2027"),
        ("where", "delhi, india"),
        ("repos", _fmt(stats.get("public_repos"))),
        ("commits", _fmt(stats.get("commits_year"))),
        ("streak", _fmt(stats.get("current_streak")) + " d"),
        ("stars", _fmt(stats.get("stars"))),
    ]
    s.fg.append(s.use("satvik@github", rx, s.y, "bright", glow=True))
    s.y += int(LH * 0.8)
    s.fg.append(
        '<rect x="%s" y="%s" width="%s" height="2" fill="%s" opacity="0.5"/>'
        % (n(rx), n(s.y), n(VB_W - 26 - rx), pal["green"])
    )
    s.y += int(LH * 0.5)
    for k, v in rows:
        s.fg.append(s.use(k, rx, s.y, "green"))
        s.fg.append(s.use(v, vx, s.y, "text"))
        s.y += LH
    s.fg.append(s.use("langs", rx, s.y, "green"))
    s.fg.append(_langbar(s, pal, vx, s.y, stats.get("languages") or []))
    s.y += LH + 18
    s.fg.append(_logo(pal, X0 + 8, logo_y + 6))
    s.inset(nf_top, s.y - 20, X0 - 12, VB_W - 26)
    s.gap(0.5)

    # --- about ------------------------------------------------------------
    s.line([("$ ", "green"), ("cat about.txt", "text")], typed=True)
    for ln in ABOUT:
        s.line([(ln, "muted")], indent=1)
    s.gap(0.5)

    # --- projects ---------------------------------------------------------
    for cmd, body, tags in PROJECTS:
        s.line([("$ ", "green"), (cmd, "text")], typed=True)
        y0 = s.y - 12
        for ln in body:
            s.line([(ln, "text")], indent=1)
        s.line([(tags, "link")], indent=1)
        s.inset(y0, s.y - 8)
        s.gap(0.5)

    # --- roles ------------------------------------------------------------
    s.line([("$ ", "green"), ("history | grep -i intern", "text")], typed=True)
    for org, title, body in ROLES:
        s.line([(org, "bright")], indent=1)
        s.line([(title, "muted")], indent=1)
        for ln in body:
            s.line([(ln, "text")], indent=2)
        s.gap(0.3)
    s.gap(0.2)

    # --- stack ------------------------------------------------------------
    s.line([("$ ", "green"), ("ls stack.d/", "text")], typed=True)
    y0 = s.y - 12
    for k, vals in STACK:
        s.fg.append(s.use(k, X0 + ADV, s.y, "green"))
        for j, v in enumerate(vals):
            s.fg.append(s.use(v, X0 + 11 * ADV, s.y + j * LH, "text"))
        s.y += LH * len(vals)
    s.inset(y0, s.y - 8)
    s.gap(0.5)

    # --- contact ----------------------------------------------------------
    s.line([("$ ", "green"), ("cat contact.txt", "text")], typed=True)
    for k, v in CONTACT:
        s.fg.append(s.use(k, X0 + ADV, s.y, "green"))
        s.fg.append(s.use(v, X0 + 11 * ADV, s.y, "link"))
        s.y += LH
    s.gap(0.4)

    s.fg.append(s.use("$", X0, s.y, "green", glow=True))
    s.walk.insert(0, (X0 + ADV, s.y))
    s.walk.extend([(X0 + ADV, s.y)] * 3)
    s.y += LH

    # one cursor for the whole session: it walks every command, then parks on
    # the final prompt and blinks. transform and opacity animate independently.
    steps = s.walk[::2] if len(s.walk) > 460 else s.walk
    dur = min(9.0, max(2.0, len(steps) * 0.022))
    s.fg.append(
        '<rect width="%s" height="%s" fill="%s" opacity="0.5" '
        'transform="translate(%s %s)">'
        '<animateTransform attributeName="transform" type="translate" '
        'values="%s" dur="%ss" calcMode="discrete" fill="freeze"/>'
        '<animate attributeName="opacity" values="0.5;0.5;0.12;0.12" '
        'dur="1.06s" calcMode="discrete" repeatCount="indefinite"/>'
        "</rect>"
        % (n(CW * g.W), n(CAP), pal["hi"], n(steps[0][0]), n(steps[0][1]),
           ";".join("%s %s" % (n(x), n(y)) for x, y in steps), n(dur))
    )

    stamp = stats.get("generated") or ""
    if stamp:
        s.fg.append(s.use("last sync " + stamp, X0, s.y, "muted",
                          opacity="0.65"))
        s.y += LH

    H = int(s.y + 26)
    win_h = H - win_y - 14

    title = "satvik@mait: ~"
    s.chars |= set(title) | set("$ ")

    body = [
        '<rect width="%d" height="%d" fill="%s"/>' % (VB_W, H, pal["canvas"]),
        '<rect x="8" y="%d" width="%d" height="%d" rx="12" fill="%s" '
        'stroke="%s" stroke-width="1.5"/>'
        % (win_y, VB_W - 16, win_h, pal["canvas"], pal["edge"]),
        '<path d="M9.5 %d v-%d a11 11 0 0 1 11 -11 h%d a11 11 0 0 1 11 11 v%d z" '
        'fill="%s"/>'
        % (win_y + bar_h, bar_h - 11, VB_W - 16 - 22, bar_h - 11, pal["inset"]),
        '<line x1="9" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.5"/>'
        % (win_y + bar_h, VB_W - 9, win_y + bar_h, pal["edge"]),
    ]
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        body.append('<circle cx="%d" cy="%d" r="7" fill="%s"/>'
                    % (32 + i * 24, win_y + bar_h // 2, c))
    body.append(g.run(title, 300, win_y + bar_h / 2.0 - CAP / 2.0, CW, CH,
                      ' fill="%s"' % pal["muted"]))

    defs = ["<defs>", g.defs_for(s.chars), "".join(s.defs)]
    defs.append(
        '<filter id="bleed" x="-30%" y="-40%" width="160%" height="180%">'
        '<feGaussianBlur stdDeviation="1.5" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
        "</feMerge></filter>"
    )
    if pal["crt"]:
        defs.append(
            '<pattern id="scan" width="4" height="4" '
            'patternUnits="userSpaceOnUse">'
            '<rect width="4" height="1.6" fill="#000" opacity="0.30"/>'
            "</pattern>"
        )
    defs.append("</defs>")

    tail = []
    if pal["crt"]:
        tail.append(
            '<rect x="8" y="%d" width="%d" height="%d" rx="12" '
            'fill="url(#scan)" opacity="0.5"/>' % (win_y, VB_W - 16, win_h)
        )

    head = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'role="img" aria-label="Satvik Rastogi, terminal-style profile">'
        % (VB_W, H)
    ]
    return "".join(head + defs + body + s.bg + s.fg + tail + ["</svg>"])
