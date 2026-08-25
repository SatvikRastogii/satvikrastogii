"""Render every variant SVG from data/stats.json + the theme modules.

Usage: python src/build.py [variant ...]
No SVG library on purpose -- the markup is a string so nothing can quietly
insert something Camo will refuse to serve.
"""
import json
import os
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


def main(argv):
    stats = load_stats()
    want = argv or list(VARIANTS)
    for name in want:
        mod, folder = VARIANTS[name]
        outdir = os.path.join(ROOT, "assets", folder)
        os.makedirs(outdir, exist_ok=True)
        for dark in (True, False):
            svg = mod.render(stats, dark)
            fn = "%s-%s.svg" % (name, "dark" if dark else "light")
            with open(os.path.join(outdir, fn), "w", encoding="utf-8") as f:
                f.write(svg)
            print("%-34s %6.1f KB" % (
                "assets/%s/%s" % (folder, fn), len(svg.encode()) / 1024.0))


if __name__ == "__main__":
    main(sys.argv[1:])
