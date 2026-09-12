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

# SGR sequences only: ESC [ <params> m  (colours, bold, reset)
ESC = re.compile(r"\x1b\[([0-9;]*)m")

# Any other CSI sequence: ESC [ <params> <final-byte-that-is-not-m>
# These include ESC[J (erase display), ESC[H (cursor home), ESC[2J, etc.
# They must be stripped so they never leak as literal "[J" into the HTML.
#
# CSI final bytes are A-Z and a-z (plus some punctuation).  SGR ends in 'm'
# (lowercase).  Pattern: all uppercase A-Z + all lowercase except 'm'.
# [A-Za-ln-z] = A-Z (all uppercase) + a-l + n-z (all lowercase minus 'm').
_NON_SGR_CSI = re.compile(r"\x1b\[[0-9;]*[A-Za-ln-z@`]")


def hexof(r, g, b):
    return "#%02x%02x%02x" % (int(r), int(g), int(b))


def ansi_to_html(s):
    """Convert an ANSI string (starship output) to HTML spans.

    Non-SGR CSI sequences (ESC[J, ESC[2J, ESC[H, …) are stripped first so they
    never appear as literal control-sequence remnants in the output.
    SGR colour and reset sequences are faithfully converted to <span> elements.
    """
    # 1. Strip zsh prompt wrappers.
    s = s.replace("%{", "").replace("%}", "")
    # 2. Strip non-SGR CSI sequences BEFORE any further processing.
    s = _NON_SGR_CSI.sub("", s)

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


def _self_test():
    """Regression tests for ansi_to_html — run automatically at import time."""
    # Non-SGR CSI sequences must never appear as literal bracket-letter remnants.
    assert "[J" not in ansi_to_html("\x1b[J hello"), \
        "ESC[J leaked as literal '[J'"
    assert "[J" not in ansi_to_html("\x1b[2J hello"), \
        "ESC[2J leaked as literal '[J'"
    assert "[H" not in ansi_to_html("\x1b[H hello"), \
        "ESC[H leaked as literal '[H'"
    # ESC[K (erase line) must also be stripped.
    assert "[K" not in ansi_to_html("\x1b[K hello"), \
        "ESC[K leaked as literal '[K'"

    # SGR colour sequences must survive and produce correct hex values.
    result = ansi_to_html("\x1b[38;2;100;200;50m hello\x1b[0m")
    assert "color:#64c832" in result, \
        f"SGR fg colour lost; got: {result!r}"
    assert "hello" in result, "text content lost"

    bg_result = ansi_to_html("\x1b[48;2;30;40;50m bg\x1b[0m")
    assert "background:#1e2832" in bg_result, \
        f"SGR bg colour lost; got: {bg_result!r}"

    # Mixed: non-SGR before SGR — colour must survive, non-SGR must vanish.
    mixed = ansi_to_html("\x1b[J\x1b[38;2;255;0;0m red\x1b[0m")
    assert "[J" not in mixed, "ESC[J survived mixed input"
    assert "color:#ff0000" in mixed, "SGR colour lost in mixed input"

    print("render_html self-test: all assertions passed")


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


# Run self-test whenever this module is loaded (import or direct run).
_self_test()

if __name__ == "__main__":
    main()
