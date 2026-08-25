"""Variant 3 -- contribution-square portrait.

Everything on the page is a contribution square: the face, the type, and the
live numbers. The joke only lands if the numbers are the same substance as
the portrait, so they are set in the square font at the largest size here.

Motion never hides anything. The load wave brightens each cell one level and
lets it fall back, sweeping diagonally the way the real graph populates --
it does not fade cells in from nothing, because a still of this file has to
be the finished picture.
"""
import random

import glyphs as g
import portrait

VB_W = 830
M = 30
CONTENT = VB_W - 2 * M          # 770

P_PITCH, P_SQ, P_RX = 17.0, 12.4, 2.3        # portrait
B_PITCH, B_SQ, B_RX = 4.4, 3.3, 0.7          # body type  -> 29 columns
H_PITCH, H_SQ, H_RX = 5.0, 3.7, 0.8          # section headings
N_PITCH = 6.8                                # the name
S_PITCH = 6.2                                # the live numbers
BLH = 46                                     # body line pitch
COLS = 29

SCALE_DARK = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
SCALE_LIGHT = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]

DARK = {"scale": SCALE_DARK, "canvas": "#0d1117",
        "head": 4, "body": 3, "muted": 2, "rule": 1}
# On light the scale runs the other way -- level 4 is the DARKEST green -- so
# body copy has to climb to 4 to stay legible on white. Size carries the
# hierarchy instead of colour.
LIGHT = {"scale": SCALE_LIGHT, "canvas": "#ffffff",
         "head": 4, "body": 4, "muted": 3, "rule": 1}


def n(v):
    return g._n(v)


ABOUT = [
    "i build agent systems, then",
    "i build the thing that",
    "grades them.",
]

PROJECTS = [
    ("lexgraph", [
        "graphrag over judgments of",
        "the indian supreme court.",
        "flat vector search against",
        "a knowledge graph. same",
        "corpus, same questions,",
        "same metrics.",
    ], "python networkx chromadb"),
    ("queryforge", [
        "agentic postgres index",
        "advisor. an llm proposes",
        "indexes, a real benchmark",
        "grades them. the planner",
        "on the workload, not a",
        "second model scoring it.",
    ], "langgraph mcp langfuse"),
    ("research", [
        "two papers under review",
        "with mait faculty. one",
        "benchmarks clustering",
        "protocols in a single",
        "framework. the other,",
        "hiecf, pairs type-2 fuzzy",
        "logic with q-learning.",
    ], "fuzzy logic  q-learning"),
]

WORK = [
    ("drdo sag", "research intern", [
        "sdr client-server in java.",
        "irss apis over tcp,",
        "aes-256, per-message iv.",
    ]),
    ("cantilever labs", "ai engineer intern", [
        "rag chatbot with grounded",
        "answers. captioning and",
        "nlp triage models.",
    ]),
    ("t&p cell, mait", "corporate relations", [
        "recruiter outreach,",
        "campus drives end to end.",
    ]),
]

STACK = [
    "python  java  sql  c++",
    "langchain  langgraph",
    "crewai  rag  graphrag",
    "mcp  ragas  langfuse",
    "fastapi  docker  vllm",
    "sglang  ollama  pytorch",
    "postgres  chromadb",
    "lancedb  networkx  numpy",
]

CONTACT = [
    "satvikrastogi.vercel.app",
    "github.com/satvikrastogii",
    "linkedin: satvikrastogii",
    "leetcode: blackmancodes",
    "satvikrastogi777@gmail.com",
]


class Page(object):
    def __init__(self, pal, seed):
        self.p = pal
        self.out = []
        self.body_chars = set()
        self.head_chars = set()
        self.y = 0
        self.rng = random.Random(seed)

    def cell(self, x, y, lvl, pitch, sq, rx, sweep=None):
        """One contribution square. sweep is the wave's begin time, or None."""
        sc = self.p["scale"]
        anim = ""
        if sweep is not None and lvl > 0:
            up = sc[min(lvl + 1, 4)]
            anim += (
                '<animate attributeName="fill" values="%s;%s;%s" dur="1.1s" '
                'begin="%ss" fill="remove"/>' % (sc[lvl], up, sc[lvl], n(sweep))
            )
            # ambient shimmer, kept under 10% of cells or it reads as static
            if self.rng.random() < 0.055:
                anim += (
                    '<animate attributeName="fill" values="%s;%s;%s" '
                    'dur="%ss" begin="%ss" repeatCount="indefinite"/>'
                    % (sc[lvl], up, sc[lvl], n(3.0 + self.rng.random() * 2.5),
                       n(4.0 + self.rng.random() * 9.0))
                )
        return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s">%s</rect>' % (
            n(x), n(y), n(sq), n(sq), n(rx), sc[lvl], anim
        ) if anim else (
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (
                n(x), n(y), n(sq), n(sq), n(rx), sc[lvl])
        )

    def body(self, s, x=M, lvl=None, pitch=B_PITCH):
        self.body_chars |= set(s)
        lv = self.p["body"] if lvl is None else lvl
        self.out.append(g.sq_run(s, x, self.y, pitch, g.BODY,
                                 ' fill="%s"' % self.p["scale"][lv]))
        self.y += BLH

    def head(self, s, pitch=H_PITCH, lvl=None, x=M):
        self.head_chars |= set(s)
        lv = self.p["head"] if lvl is None else lvl
        self.out.append(g.sq_run(s, x, self.y, pitch, g.HEAD,
                                 ' fill="%s"' % self.p["scale"][lv]))
        self.y += g.HEAD["h"] * pitch + 16

    def rule(self):
        """A section divider drawn as a row of empty days."""
        pitch = CONTENT / 53.0
        for i in range(53):
            self.out.append(self.cell(M + i * pitch, self.y,
                                      self.p["rule"], pitch, pitch * 0.72, 1.2))
        self.y += pitch + 26

    def gap(self, k=1.0):
        self.y += BLH * k


def _fmt(v):
    return "--" if v is None else "{:,}".format(v)


def render(stats, dark=True):
    pal = DARK if dark else LIGHT
    seed = stats.get("shimmer_seed") or 20260825
    p = Page(pal, seed)
    sc = pal["scale"]

    # --- portrait ---------------------------------------------------------
    pw, ph = portrait.size()
    px = (VB_W - pw * P_PITCH) / 2.0
    py = M
    for cx, cy, lvl in portrait.levels():
        sweep = 0.25 + cx * 0.022 + cy * 0.032
        p.out.append(p.cell(px + cx * P_PITCH, py + cy * P_PITCH, lvl,
                            P_PITCH, P_SQ, P_RX, sweep))
    p.y = py + ph * P_PITCH + 44

    # --- the live numbers, set in the same squares as the face ------------
    rows = [
        ("commits", _fmt(stats.get("commits_year"))),
        ("streak", _fmt(stats.get("current_streak"))),
        ("repos", _fmt(stats.get("public_repos"))),
        ("stars", _fmt(stats.get("stars"))),
    ]
    # two by two, not four across: at four across the labels collide, and
    # shrinking them would put the type under the 14px floor at 380px.
    colw = CONTENT / 2.0
    rowh = 42 + g.HEAD["h"] * S_PITCH + 30
    for i, (label, value) in enumerate(rows):
        cx = M + (i % 2) * colw
        cy = p.y + (i // 2) * rowh
        p.body_chars |= set(label)
        p.head_chars |= set(value)
        p.out.append(g.sq_run(label, cx, cy, B_PITCH, g.BODY,
                              ' fill="%s"' % sc[pal["muted"]]))
        p.out.append(g.sq_run(value, cx, cy + 42, S_PITCH, g.HEAD,
                              ' fill="%s"' % sc[4]))
    p.y += 2 * rowh + 18

    # --- name -------------------------------------------------------------
    p.head("SATVIK RASTOGI", pitch=N_PITCH)
    p.body("ai / agentic engineer")
    p.body("b.tech cs, mait delhi.", lvl=pal["muted"])
    p.body("graduating 2027. delhi, india.", lvl=pal["muted"])
    p.gap(0.4)

    # --- the real calendar, used as a rule --------------------------------
    cal = stats.get("calendar") or []
    if cal:
        pitch = CONTENT / float(max(len(cal), 1))
        sq = pitch * 0.72
        for wi, week in enumerate(cal):
            for di, lvl in enumerate(week):
                p.out.append(p.cell(M + wi * pitch, p.y + di * pitch,
                                    int(lvl), pitch, sq, sq * 0.18,
                                    0.25 + wi * 0.03))
        p.y += 7 * pitch + 14
        p.body("the last fifty-two weeks", lvl=pal["muted"])
        p.gap(0.3)
    else:
        p.rule()

    # --- sections ---------------------------------------------------------
    p.head("about")
    for ln in ABOUT:
        p.body(ln)
    p.gap(0.5)

    for title, lines, tags in PROJECTS:
        p.head(title)
        for ln in lines:
            p.body(ln)
        p.body(tags, lvl=pal["muted"])
        p.gap(0.5)

    p.head("work")
    for org, role, lines in WORK:
        p.body(org, lvl=4)
        p.body(role, lvl=pal["muted"])
        for ln in lines:
            p.body(ln)
        p.gap(0.35)
    p.gap(0.3)

    p.head("stack")
    for ln in STACK:
        p.body(ln)
    p.gap(0.5)

    p.head("contact")
    for ln in CONTACT:
        p.body(ln)

    stamp = stats.get("generated") or ""
    if stamp:
        p.gap(0.5)
        p.body("last sync " + stamp, lvl=pal["rule"])

    H = int(p.y + 20)

    defs = [
        "<defs>",
        g.sq_defs(p.body_chars, g.BODY, B_SQ / B_PITCH, B_RX / B_PITCH),
        g.sq_defs(p.head_chars, g.HEAD, H_SQ / H_PITCH, H_RX / H_PITCH),
        "</defs>",
    ]
    return "".join(
        ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
         'role="img" aria-label="Satvik Rastogi, a portrait and profile drawn '
         'entirely in GitHub contribution squares">' % (VB_W, H)]
        + defs
        + ['<rect width="%d" height="%d" fill="%s"/>' % (VB_W, H, pal["canvas"])]
        + p.out + ["</svg>"]
    )
