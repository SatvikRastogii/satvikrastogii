"""Turn an SVG in this repo into a PNG, using the browser as the renderer.

GitHub will not take an SVG as a profile avatar, so the avatar has to ship as
a raster. There is no SVG rasteriser installed here and adding cairosvg would
break the stdlib-plus-requests rule, so this borrows the one renderer that is
already on the machine and is guaranteed to agree with what a viewer sees:
Chrome itself.

    python src/rasterize.py assets/avatar/avatar.svg 1024

Serves the repo, opens a page that draws the SVG into a canvas at the size
you asked for, and takes the PNG back over POST. The page has to be served
from the same origin as the SVG or the canvas is tainted and cannot be read.
"""
import base64
import http.server
import os
import posixpath
import socketserver
import sys
import threading
import time
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PORT = 8732

PAGE = """<!doctype html><meta charset="utf-8"><title>rasterize</title>
<body style="margin:0;background:#222;color:#ddd;font:13px ui-monospace,monospace">
<p id="s" style="padding:12px">rendering...</p>
<script>
const q = new URLSearchParams(location.search);
const src = q.get('f'), size = +(q.get('size') || 1024);
const img = new Image();
img.onload = async () => {
  const c = document.createElement('canvas');
  c.width = c.height = size;
  const x = c.getContext('2d');
  x.imageSmoothingEnabled = true;
  x.drawImage(img, 0, 0, size, size);
  let data;
  try { data = c.toDataURL('image/png'); }
  catch (e) { document.getElementById('s').textContent = 'TAINTED: ' + e; return; }
  const r = await fetch('/save?f=' + encodeURIComponent(src), {
    method: 'POST', body: data.split(',')[1] });
  document.getElementById('s').textContent = await r.text();
};
img.onerror = () => document.getElementById('s').textContent = 'LOAD FAILED';
img.src = '/' + src + '?c=' + Date.now();
</script>"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path.startswith("/raster"):
            body = PAGE.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        from urllib.parse import urlparse, parse_qs, unquote
        q = parse_qs(urlparse(self.path).query)
        rel = unquote(q.get("f", [""])[0])
        # keep the write inside the repo whatever the page asks for
        safe = posixpath.normpath(rel).lstrip("/")
        if not safe.endswith(".svg") or safe.startswith(".."):
            self.send_error(400, "bad target")
            return
        out = os.path.join(ROOT, safe[:-4] + ".png")
        raw = self.rfile.read(int(self.headers["Content-Length"]))
        png = base64.b64decode(raw)
        with open(out, "wb") as f:
            f.write(png)
        msg = "wrote %s  %.1f KB" % (os.path.relpath(out, ROOT),
                                     len(png) / 1024.0)
        print(msg)
        Handler.done = msg
        body = msg.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


Handler.done = None


def main():
    rel = sys.argv[1] if len(sys.argv) > 1 else "assets/avatar/avatar.svg"
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 1024
    url = "http://127.0.0.1:%d/raster?f=%s&size=%d" % (PORT, rel, size)

    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print("open: %s" % url)
    if "--no-open" not in sys.argv:
        webbrowser.open(url)

    deadline = time.time() + 60
    while Handler.done is None and time.time() < deadline:
        time.sleep(0.25)
    srv.shutdown()
    if Handler.done is None:
        print("timed out -- no PNG received")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
