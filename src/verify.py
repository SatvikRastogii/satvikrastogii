"""Constraint linter. Fails the build on anything that breaks on a profile.

These are the failures you cannot see until they are already live: GitHub
serves README images through the Camo proxy in <img> context, so a <script>,
a webfont, or any off-repo reference silently does nothing. Every check here
exists because the failure is invisible locally.

Usage:
    python src/verify.py            # everything, including link checks
    python src/verify.py --offline  # skip the network checks
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MAX_BYTES = 400 * 1024
SVG_DIRS = ("assets",)

# href="#id" is a <use> reference inside the same file and is fine. Anything
# with a scheme or a slash is reaching off-repo, which Camo will not fetch.
OFF_REPO = re.compile(r'\b(?:xlink:)?href\s*=\s*"(?!#)([^"]*)"')
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
PICTURE = re.compile(r"<picture\b.*?</picture>", re.I | re.S)
MD_LINK = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")
HTML_URL = re.compile(r'(?:src|srcset|href)\s*=\s*"(https?://[^"]+)"')

failures = []
checked = []


def fail(where, msg):
    failures.append("%s: %s" % (where, msg))


def ok(msg):
    checked.append(msg)


def svg_files():
    for d in SVG_DIRS:
        base = os.path.join(ROOT, d)
        for dirpath, _, names in os.walk(base):
            for nm in sorted(names):
                if nm.endswith(".svg"):
                    yield os.path.join(dirpath, nm)


def check_svgs():
    found = 0
    for path in svg_files():
        found += 1
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        raw = open(path, "rb").read()
        text = raw.decode("utf-8", "replace")

        if len(raw) > MAX_BYTES:
            fail(rel, "%.1f KB is over the %d KB budget"
                 % (len(raw) / 1024.0, MAX_BYTES // 1024))
        if re.search(r"<script\b", text, re.I):
            fail(rel, "<script> never executes in <img> context")
        if "@font-face" in text:
            fail(rel, "@font-face cannot load through Camo")
        if re.search(r"<foreignObject\b", text, re.I):
            fail(rel, "<foreignObject> does not render in <img> context")
        if re.search(r'viewBox\s*=\s*"', text) is None:
            fail(rel, "no viewBox, so the image will not scale")
        if re.search(r'<svg\b[^>]*\swidth\s*=\s*"', text):
            fail(rel, "fixed width on <svg> stops it scaling to the column")
        if "prefers-color-scheme" in text:
            fail(rel, "prefers-color-scheme is unreliable in <img> context; "
                      "theme switching belongs in the Markdown")
        if not re.search(r'aria-label\s*=\s*"[^"]+"', text):
            fail(rel, "no aria-label on the root <svg>")

        for ref in OFF_REPO.findall(text):
            if ref.startswith("data:"):
                fail(rel, "data: URI %r -- inline the shape instead"
                          % ref[:40])
            elif "://" in ref or ref.startswith("//"):
                fail(rel, "off-repo reference %r will not load" % ref[:60])

        for m in re.finditer(r'url\((#?[^)]*)\)', text):
            ref = m.group(1)
            if not ref.startswith("#"):
                fail(rel, "external url(%s) in a paint reference" % ref[:40])
                continue
            if ('id="%s"' % ref[1:]) not in text:
                fail(rel, "url(%s) points at an id that is not in the file"
                     % ref)

        for m in re.finditer(r'href="#([^"]+)"', text):
            if ('id="%s"' % m.group(1)) not in text:
                fail(rel, "<use href=#%s> has no target" % m.group(1))

        ok("%s  %.1f KB" % (rel, len(raw) / 1024.0))

    if not found:
        fail("assets", "no SVGs found -- did the build run?")


def check_readme():
    path = os.path.join(ROOT, "README.md")
    if not os.path.exists(path):
        fail("README.md", "missing -- generate it from README.template.md")
        return ""
    text = open(path, encoding="utf-8").read()

    for tag in IMG_TAG.findall(text):
        if not re.search(r'\salt\s*=\s*"[^"]+"', tag):
            fail("README.md", "<img> without real alt text: %s" % tag[:90])

    blocks = PICTURE.findall(text)
    if not blocks:
        fail("README.md", "no <picture> block, so dark mode will not switch")
    for b in blocks:
        if "<source" not in b:
            fail("README.md", "<picture> with no <source>")
        if "<img" not in b:
            fail("README.md", "<picture> with no <img> fallback -- some "
                              "clients ignore <source>")
        if 'media="(prefers-color-scheme: dark)"' not in b:
            fail("README.md", "<picture> has no dark <source>")

    for m in re.finditer(r'src(?:set)?="([^"]*raw\.githubusercontent[^"]*)"',
                         text):
        if "?v=" not in m.group(1):
            fail("README.md", "asset URL with no ?v= cache-buster: %s"
                 % m.group(1)[-70:])

    if "{{" in text:
        fail("README.md", "unsubstituted template placeholder left in output")
    ok("README.md structure")
    return text


RAW_SELF = re.compile(
    r"^https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/(.+?)(?:\?.*)?$")

# A 403 from LinkedIn is a bot block, not a broken link. Treating it as a
# failure would train us to ignore this check, which defeats the point.
BLOCKED = {401, 403, 405, 429, 999}


def check_links(text, offline):
    urls = sorted(set(MD_LINK.findall(text)) | set(HTML_URL.findall(text)))

    # Asset URLs point at this repo. Resolve them against the working tree --
    # before a push they always 404 on the network, which says nothing.
    remote, network = [], 0
    for url in urls:
        m = RAW_SELF.match(url)
        if m:
            local = os.path.join(ROOT, m.group(1).replace("/", os.sep))
            if os.path.exists(local):
                ok("asset %s resolves in the working tree" % m.group(1))
            else:
                fail("README.md", "asset URL has no file behind it: %s"
                     % m.group(1))
        else:
            remote.append(url)
            network += 1

    if not remote:
        return
    if offline:
        ok("skipped %d external link checks (--offline)" % network)
        return
    try:
        import requests
    except ImportError:
        ok("skipped %d external link checks (requests missing)" % network)
        return

    session = requests.Session()
    session.headers["User-Agent"] = (
        "Mozilla/5.0 (compatible; profile-verify/1.0)")
    for url in remote:
        try:
            r = session.head(url, allow_redirects=True, timeout=15)
            if r.status_code in BLOCKED or r.status_code >= 400:
                r = session.get(url, allow_redirects=True, timeout=20,
                                stream=True)
            code = r.status_code
            if code in BLOCKED:
                ok("link %s -> %d (bot-blocked, not verified)" % (url, code))
            elif code >= 400:
                fail("link", "%s -> HTTP %d" % (url, code))
            else:
                ok("link %s -> %d" % (url, code))
        except Exception as exc:
            fail("link", "%s -> %s" % (url, exc.__class__.__name__))


def main():
    offline = "--offline" in sys.argv
    check_svgs()
    text = check_readme()
    check_links(text, offline)

    for line in checked:
        print("  ok    %s" % line)
    if failures:
        print("\n%d problem(s):\n" % len(failures))
        for f in failures:
            print("  FAIL  %s" % f)
        return 1
    print("\nall %d checks passed" % len(checked))
    return 0


if __name__ == "__main__":
    sys.exit(main())
