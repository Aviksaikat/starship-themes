#!/usr/bin/env python3
"""Verify generated variation themes actually render their palette colours.

starship exits 0 and silently strips styling when a palette key fails to
resolve, so exit codes prove nothing. This asserts the expected truecolor
escapes appear in the real prompt output, per theme.
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES = os.path.join(REPO, "themes")
SAMPLE_CWD = REPO  # a git repo, so path + git chips render


def rgb(h):
    h = h.lstrip("#")
    return "%d;%d;%d" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def render(name):
    env = dict(os.environ, STARSHIP_CONFIG=os.path.join(THEMES, name + ".toml"),
               STARSHIP_LOG="error")
    r = subprocess.run(["starship", "prompt"], capture_output=True, env=env,
                       cwd=SAMPLE_CWD)
    return r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


def expected_colors(path):
    """Pull the palette values the theme actually references.

    For inline-hex themes: every distinct hex in the file.
    For named-palette themes: the values in the last [palettes.*] block.
    """
    raw = open(path, encoding="utf-8").read()
    blocks = re.findall(r"\[palettes\.([\w-]+)\]\n(.*?)(?=\n\[|\Z)", raw, re.S)
    if blocks:
        used = re.search(r"^palette\s*=\s*['\"]([\w-]+)['\"]", raw, re.M)
        name = used.group(1) if used else blocks[-1][0]
        for bname, body in blocks:
            if bname == name:
                return sorted({v for v in re.findall(r'["\'](#[0-9A-Fa-f]{6})["\']', body)})
        return sorted({v for v in re.findall(r'["\'](#[0-9A-Fa-f]{6})["\']', blocks[-1][1])})
    return sorted({h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}", raw)})


def main():
    names = sys.argv[1:]
    if not names:
        names = sorted(
            f[:-5] for f in os.listdir(THEMES) if f.endswith(".toml")
        )

    bad = []
    for n in names:
        path = os.path.join(THEMES, n + ".toml")
        out, err = render(n)
        problems = []
        if err.strip():
            problems.append("STDERR:" + err.strip()[:60])
        if not out.strip():
            problems.append("EMPTY-OUTPUT")

        cols = expected_colors(path)
        present = [c for c in cols if rgb(c) in out]
        missing = [c for c in cols if rgb(c) not in out]

        # A theme whose palette never reaches the output is silently unstyled.
        if cols and not present:
            problems.append(f"NO-PALETTE-COLOURS-IN-OUTPUT ({len(cols)} expected)")

        if problems:
            bad.append((n, problems, len(present), len(cols)))
            print(f"  FAIL  {n:26s} {', '.join(problems)}")
        else:
            print(f"  ok    {n:26s} {len(present)}/{len(cols)} palette colours rendered")

    print()
    if bad:
        print(f"FAILURES: {len(bad)}/{len(names)}")
        return 1
    print(f"All {len(names)} themes render their palettes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
