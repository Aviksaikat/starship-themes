#!/usr/bin/env python3
"""Contrast-check every theme's foreground/background pairs.

The palette verifier (`verify_palette.py`) proves a colour *reaches* the output.
It cannot tell you the text is unreadable on it. This does that: it extracts
every `fg:X bg:Y` pair from a theme (in either order, with palette names or
literal hex), resolves them, and reports WCAG contrast below a threshold.

The failure mode it exists to catch, found by eye on gruvbox-mono:
`gruvbox_rainbow` drives ALL chip text from one `color_fg0`, used against BOTH
dark chip backgrounds (`color_bg1`, `color_bg3`) and the accent chips. Make fg0
dark to suit the accents and the dark-backed chips become dark-on-dark.

Usage:
  python3 tools/verify_contrast.py [theme ...]     # default: every theme
  python3 tools/verify_contrast.py --threshold 4.0
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
THEMES = os.path.join(ROOT, "themes")

# Separator glyphs are deliberately low-contrast on some themes (they only have
# to hint at a boundary), so pairs whose styled group contains nothing but a
# private-use glyph are exempt.
def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(hexstr):
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def palette_of(text):
    """name -> hex, for every [palettes.*] block in the file."""
    out = {}
    for m in re.finditer(r"\[palettes\.([^\]]+)\]\s*\n(.*?)(?=\n\[|\Z)", text, re.S):
        for k, v in re.findall(r"(\w+)\s*=\s*['\"](#[0-9a-fA-F]{6})['\"]", m.group(2)):
            out[k.lower()] = v
    return out


def resolve(token, pal):
    """`color_fg0` | `#aabbcc` | bare named ANSI -> hex, or None."""
    token = token.strip()
    if token.startswith("#"):
        return token
    if token.lower() in pal:
        return pal[token.lower()]
    return None


PAIR = re.compile(r"(fg|bg):([#\w]+)")


def is_glyph_only(body):
    """Separator/icon-only groups carry no text, so their contrast is moot.

    The powerline arrows are deliberately low-contrast shapes: the leading
    glyph of a segment is drawn in the PREVIOUS chip's colour against this
    chip's background, which is exactly what makes the ribbon look continuous.
    """
    stripped = body.strip()
    if not stripped:
        return True
    return all(
        0xE000 <= ord(c) <= 0xF8FF          # BMP private use (powerline, nerd)
        or 0xF0000 <= ord(c) <= 0xFFFFD     # supplementary private use
        or 0xF0035 == ord(c)                # Apple icon
        or c.isspace()
        for c in stripped
    )


def pairs_in(text):
    """Yield (fg_token, bg_token) for every styled group that sets both.

    Groups whose visible content is glyph-only are skipped -- see
    `is_glyph_only`.
    """
    for body, style in re.findall(r"\[([^\]]*)\]\(([^)]*)\)", text):
        if is_glyph_only(body):
            continue
        found = dict(PAIR.findall(style))
        if "fg" in found and "bg" in found:
            yield found["fg"], found["bg"], body


def main():
    argv = sys.argv[1:]
    threshold = 3.0
    if "--threshold" in argv:
        i = argv.index("--threshold")
        threshold = float(argv[i + 1])
        del argv[i:i + 2]

    names = argv or sorted(
        os.path.basename(p)[:-5] for p in glob.glob(os.path.join(THEMES, "*.toml"))
    )

    bad = 0
    for name in names:
        path = os.path.join(THEMES, name + ".toml")
        if not os.path.exists(path):
            print(f"  ??    {name:22s} no such theme")
            continue
        text = open(path, encoding="utf-8").read()
        pal = palette_of(text)
        worst = []
        for fg_t, bg_t, body in pairs_in(text):
            fg, bg = resolve(fg_t, pal), resolve(bg_t, pal)
            if not fg or not bg:
                continue
            r = contrast(fg, bg)
            if r < threshold:
                worst.append((r, fg_t, bg_t, body.strip()[:26]))
        if worst:
            bad += 1
            worst.sort()
            print(f"  LOW   {name:22s} {len(worst)} pair(s) under {threshold:g}")
            for r, fg_t, bg_t, body in worst[:3]:
                print(f"          {r:5.2f}:1  fg:{fg_t} on bg:{bg_t}   '{body}'")
        else:
            print(f"  ok    {name:22s} all pairs >= {threshold:g}")

    print()
    if bad:
        print(f"{bad} theme(s) have low-contrast chip text.")
        return 1
    print(f"All themes pass contrast >= {threshold:g}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
