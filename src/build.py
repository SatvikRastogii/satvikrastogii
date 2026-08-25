"""Render every variant SVG from data/stats.json + the theme modules.

Usage: python src/build.py [variant ...]
No SVG library on purpose -- the markup is a string so nothing can quietly
insert something Camo will refuse to serve.
"""
import datetime
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from themes import terminal, truckart, contrib  # noqa: E402

VARIANTS = {
    "terminal": (terminal, "terminal"),
    "truckart": (truckart, "truckart"),
    "contrib": (contrib, "contrib"),
}

PLACEHOLDER = {
    "generated": "",
    "total_contributions": None,
    "commits_year": None,
    "current_streak": None,
    "longest_streak": None,
    "public_repos": None,
    "stars": None,
    "languages": [],
    "calendar": [],
    "active_variant": "truckart",
    "shimmer_seed": 20260825,
}


def load_stats():
    p = os.path.join(ROOT, "data", "stats.json")
    s = dict(PLACEHOLDER)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            s.update(json.load(f))
    return s


def num(v):
    """Live stat or a visible blank -- never a made-up number."""
    return "--" if v is None else "{:,}".format(v) if isinstance(v, int) else str(v)


# --- README generation ------------------------------------------------------
# The <picture> markup is generated rather than kept in the template because
# rotate.yml reorders it weekly. Everything else lives in README.template.md.

OWNER, REPO = "SatvikRastogii", "satvikrastogii"
RAW = ("https://raw.githubusercontent.com/%s/%s/main/assets/%%s/%%s-%%s.svg?v=%%s"
       % (OWNER, REPO))

META = {
    "truckart": {
        "name": "Truck art",
        "blurb": "An Indian truck rear panel, with each project as a "
                 "matchbox label",
        "alt": "Satvik Rastogi's profile painted as an Indian truck rear "
               "panel: a HORN OK PLEASE style ribbon reading PUSH OK PLEASE, "
               "his name in hand-painted display lettering, an ALL INDIA WORK "
               "PERMIT badge reading OPEN TO WORK, and matchbox-label cards "
               "for LexGraph, QueryForge and his wireless sensor network "
               "research, followed by experience, stack and contact details.",
    },
    "terminal": {
        "name": "Terminal",
        "blurb": "A shell session, in GitHub's own black and green",
        "alt": "Satvik Rastogi's profile as a terminal session: a boot "
               "sequence, a neofetch-style block with live GitHub statistics, "
               "then commands whose output is each section -- about, "
               "LexGraph, QueryForge, wireless sensor network research, "
               "internships, stack and contact details.",
    },
    "contrib": {
        "name": "Contribution squares",
        "blurb": "A portrait and every word of type built from contribution "
                 "squares",
        "alt": "Satvik Rastogi's profile drawn entirely in GitHub "
               "contribution squares: a portrait of a curly-haired man in "
               "glasses, live commit, streak, repository and star counts set "
               "in a square bitmap font, then about, LexGraph, QueryForge, "
               "research, work, stack and contact sections in the same "
               "squares.",
    },
}
ORDER = ["truckart", "terminal", "contrib"]


def picture(variant, sha, indent=""):
    m = META[variant]
    dark = RAW % (variant, variant, "dark", sha)
    light = RAW % (variant, variant, "light", sha)
    lines = [
        "<picture>",
        '  <source media="(prefers-color-scheme: dark)" srcset="%s">' % dark,
        '  <source media="(prefers-color-scheme: light)" srcset="%s">' % light,
        # the <img> fallback is required: some clients ignore <source>
        '  <img alt="%s" src="%s" width="830">' % (m["alt"], light),
        "</picture>",
    ]
    return "\n".join(indent + ln for ln in lines)


def render_readme(stats, sha):
    tpl_path = os.path.join(ROOT, "README.template.md")
    with open(tpl_path, encoding="utf-8") as f:
        tpl = f.read()

    active = stats.get("active_variant") or "truckart"
    if active not in META:
        active = "truckart"
    others = [v for v in ORDER if v != active]

    alts = ["### The other two themes\n",
            "This profile changes personality every Monday. The other two "
            "are always here.\n"]
    for v in others:
        m = META[v]
        alts.append("<details>")
        alts.append("<summary><b>%s</b> — %s</summary>\n" % (m["name"],
                                                             m["blurb"]))
        alts.append(picture(v, sha))
        alts.append("\n</details>\n")

    stamp = "Active theme: %s. Last regenerated %s." % (
        META[active]["name"], stats.get("generated") or "not yet")

    out = (tpl
           .replace("{{HERO}}", picture(active, sha))
           .replace("{{ALTERNATES}}", "\n".join(alts))
           .replace("{{STAMP}}", stamp))
    # strip the template's own instructions from the generated file
    out = re.sub(r"^<!--.*?-->\n", "", out, count=1, flags=re.S)
    out = ("<!-- Generated from README.template.md. Do not edit by hand; "
           "run `python src/build.py --readme`. -->\n" + out)

    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8",
              newline="\n") as f:
        f.write(out)
    print("README.md          active=%s  v=%s" % (active, sha))


def asset_version():
    """Cache-buster: a hash of the SVG bytes, not the commit SHA.

    The brief called for the short SHA. It cannot work, for two reasons this
    repo hit immediately:

      1. The value has to be written *into* the commit, so it can never equal
         that commit's own SHA. CI regenerates the README, gets a different
         value, and the "committed output is stale" check fails every time.
      2. It changes on every run whether or not the images did, so README.md
         is always dirty and the skip-the-commit-when-nothing-changed step
         never fires. You would get a commit a day forever.

    Hashing the assets serves the actual purpose -- telling Camo the bytes
    changed -- and changes exactly when they do.
    """
    h = hashlib.sha1()
    for variant in ORDER:
        for theme in ("dark", "light"):
            p = os.path.join(ROOT, "assets", variant,
                             "%s-%s.svg" % (variant, theme))
            if os.path.exists(p):
                with open(p, "rb") as f:
                    h.update(f.read())
    return h.hexdigest()[:8]


def save_stats(stats):
    p = os.path.join(ROOT, "data", "stats.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(stats, f, indent=1, sort_keys=True)
        f.write("\n")


def reseed(stats):
    """New shimmer seed so variant 3 twinkles differently day to day."""
    stats["shimmer_seed"] = int(datetime.date.today().strftime("%Y%m%d"))
    save_stats(stats)
    print("shimmer_seed       %s" % stats["shimmer_seed"])
    return stats


def rotate(stats):
    """Advance the active variant. Stored in stats.json so the daily stats
    job reads it back rather than resetting it."""
    cur = stats.get("active_variant") or ORDER[0]
    nxt = ORDER[(ORDER.index(cur) + 1) % len(ORDER)] if cur in ORDER else ORDER[0]
    stats["active_variant"] = nxt
    save_stats(stats)
    print("active_variant     %s -> %s" % (cur, nxt))
    return stats


def main(argv):
    stats = load_stats()
    if "--reseed" in argv:
        stats = reseed(stats)
        argv = [a for a in argv if a != "--reseed"]
    if "--rotate" in argv:
        stats = rotate(stats)
        argv = [a for a in argv if a != "--rotate"]
    readme = "--readme" in argv
    argv = [a for a in argv if a != "--readme"]

    # Build before rendering the README: the cache-buster hashes the SVGs, so
    # it has to be computed after they are written.
    want = argv or (list(VARIANTS) if not readme else [])
    for name in want:
        mod, folder = VARIANTS[name]
        outdir = os.path.join(ROOT, "assets", folder)
        os.makedirs(outdir, exist_ok=True)
        for dark in (True, False):
            svg = mod.render(stats, dark)
            fn = "%s-%s.svg" % (name, "dark" if dark else "light")
            with open(os.path.join(outdir, fn), "w", encoding="utf-8",
                      newline="\n") as f:
                f.write(svg)
            print("%-34s %6.1f KB" % (
                "assets/%s/%s" % (folder, fn), len(svg.encode()) / 1024.0))

    if readme:
        render_readme(stats, asset_version())


if __name__ == "__main__":
    main(sys.argv[1:])
