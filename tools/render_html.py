#!/usr/bin/env python3
"""Render the real `starship prompt` output of every theme into a single HTML page.

Useful as (a) a faithful visual preview for the README and (b) a way to eyeball
the rounded caps without installing anything.

Run:  python3 tools/render_html.py   ->  docs/preview.html
"""
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "preview.html")

ESC = re.compile(r"\x1b\[([0-9;]*)m")


def hexof(r, g, b):
    return "#%02x%02x%02x" % (int(r), int(g), int(b))


def ansi_to_html(s):
    """Convert an ANSI string (starship output) to HTML spans."""
    s = s.replace("%{", "").replace("%}", "")
    out, pos = [], 0
    state = {"fg": None, "bg": None, "bold": False, "open": False}

    def esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def close():
        if state["open"]:
            out.append("</span>")
            state["open"] = False

    def emit(text):
        if not text:
            return
        if not state["open"]:
            style = []
            if state["fg"]:
                style.append("color:" + state["fg"])
            if state["bg"]:
                style.append("background:" + state["bg"])
            if state["bold"]:
                style.append("font-weight:600")
            out.append('<span style="%s">' % ";".join(style))
            state["open"] = True
        out.append(esc(text))

    for m in ESC.finditer(s):
        emit(s[pos:m.start()])
        close()  # each escape starts a fresh run
        pos = m.end()
        params = [p for p in m.group(1).split(";") if p != ""]
        i = 0
        while i < len(params):
            p = params[i]
            if p == "0":
                state["fg"] = state["bg"] = None
                state["bold"] = False
            elif p == "1":
                state["bold"] = True
            elif p == "38" and i + 4 < len(params) and params[i + 1] == "2":
                state["fg"] = hexof(params[i + 2], params[i + 3], params[i + 4])
                i += 4
            elif p == "48" and i + 4 < len(params) and params[i + 1] == "2":
                state["bg"] = hexof(params[i + 2], params[i + 3], params[i + 4])
                i += 4
            i += 1
    emit(s[pos:])
    close()
    return "".join(out)


def palette_of(text):
    return dict(re.findall(r'^\s*(\w+)\s*=\s*"(#[0-9a-fA-F]{6})"', text, re.M))


def render(cfg, cwd):
    env = dict(os.environ, STARSHIP_CONFIG=cfg)
    r = subprocess.run(["starship", "prompt"], capture_output=True, env=env, cwd=cwd)
    return r.stdout.decode("utf-8", "replace").replace("\n", "")


def main():
    themes = sorted(f for f in os.listdir(os.path.join(ROOT, "themes"))
                    if f.endswith(".toml"))
    cards = []
    for t in themes:
        cfg = os.path.join(ROOT, "themes", t)
        pal = palette_of(open(cfg, encoding="utf-8").read())
        name = t[:-5]
        repo = render(cfg, "/tmp/sstest/dirty")
        proj = render(cfg, "/tmp/sstest/pyproj")
        cards.append(
            '<section class="card" style="background:%s">'
            '<h2>%s</h2>'
            '<pre class="p">%s</pre>'
            '<pre class="p">%s</pre>'
            '<div class="meta">path %s &middot; git %s &middot; lang %s'
            "</div></section>"
            % (pal["base"], name,
               ansi_to_html(repo) or "&nbsp;",
               ansi_to_html(proj) or "&nbsp;",
               pal["color_path"], pal["color_git"], pal["color_lang"])
        )

    html = """<!doctype html>
<html><head><meta charset="utf-8"><title>starship-theme preview</title>
<style>
  body { background:#111; color:#ddd; font-family:"CaskaydiaCove Nerd Font",monospace;
         padding:24px; }
  .grid { display:grid; grid-template-columns:1fr 1fr; gap:18px; }
  .card { border-radius:10px; padding:14px 18px; }
  .card h2 { font-size:13px; margin:0 0 10px; color:#bbb; font-weight:600;
             letter-spacing:.4px; }
  pre.p { margin:0; font-size:17px; line-height:1.5; white-space:pre;
          font-family:"CaskaydiaCove Nerd Font",monospace; }
  .meta { margin-top:10px; font-size:11px; color:#888; }
</style></head><body>
<h1 style="font-size:16px">starship-theme &mdash; rounded chip preview</h1>
<div class="grid">
%s
</div></body></html>""" % "\n".join(cards)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
