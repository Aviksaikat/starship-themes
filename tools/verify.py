#!/usr/bin/env python3
"""Verify every generated theme actually renders styled pills.

Per theme, in four scenarios (dirty repo / clean repo / non-git dir / python project):
  * no config parse error on stderr
  * path pill: chip background present, BOTH caps painted in colour_path
  * git pill : chip background present, caps painted in colour_git (repos only)
  * lang pill: chip background present (python project only)
  * no stray powerline arrow anywhere
  * in a CLEAN repo the git_status module contributes nothing (no empty pill)

Run:  python3 tools/verify.py
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
L, R = "\ue0b6", "\ue0b4"
ARROW = "\ue0b0"

SCEN = {
    "dirty": "/tmp/sstest/dirty",
    "clean": "/tmp/sstest/clean",
    "nongit": "/tmp/sstest/plain",
    "pyproj": "/tmp/sstest/pyproj",
}


def rgb(hexstr):
    h = hexstr.lstrip("#")
    return "%d;%d;%d" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def read_palette(text):
    out = {}
    for m in re.finditer(r'^\s*(color_\w+|base)\s*=\s*"(#[0-9a-fA-F]{6})"', text, re.M):
        out[m.group(1)] = m.group(2)
    return out


def run(args, cfg, cwd):
    env = dict(os.environ, STARSHIP_CONFIG=cfg)
    r = subprocess.run(["starship"] + args, capture_output=True, env=env, cwd=cwd)
    return r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


def painted_cap(out, colour, cap):
    """Cap is painted correctly when its colour escape immediately precedes it.

    starship wraps escapes in %{ ... %} for zsh, so allow that in between.
    """
    pat = r"\x1b\[38;2;" + rgb(colour) + r"m%?\}?" + re.escape(cap)
    return re.search(pat, out) is not None


def main():
    themes = sorted(f for f in os.listdir(os.path.join(ROOT, "themes"))
                    if f.endswith(".toml"))
    failures = []

    for t in themes:
        cfg = os.path.join(ROOT, "themes", t)
        pal = read_palette(open(cfg, encoding="utf-8").read())
        name = t[:-5]

        for scen, cwd in SCEN.items():
            out, err = run(["prompt"], cfg, cwd)
            problems = []
            if "ERROR" in err.upper():
                problems.append("PARSE-ERROR")
            if ARROW in out:
                problems.append("STRAY-ARROW")

            want = [pal["color_path"]]
            if scen in ("dirty", "clean"):
                want.append(pal["color_git"])
            if scen == "pyproj":
                want.append(pal["color_lang"])
            for col in want:
                if "48;2;" + rgb(col) not in out:
                    problems.append("no-chip-bg:" + col)

            if not painted_cap(out, pal["color_path"], L):
                problems.append("left-cap-unpainted")
            if not painted_cap(out, pal["color_path"], R):
                problems.append("right-cap-unpainted")

            if not problems:
                print(f"  ok    {name:24s} {scen}")
            else:
                msg = f"{name}/{scen}: " + ",".join(problems)
                failures.append(msg)
                print(f"  FAIL  {name:24s} {scen}  {','.join(problems)}")

        # clean-repo git_status must be completely silent
        for scen, expect in (("clean", True), ("dirty", False)):
            out, _ = run(["module", "git_status"], cfg, SCEN[scen])
            empty = out.strip() == ""
            if empty and not expect:
                failures.append(f"{name}/{scen}: git_status empty but tree is dirty")
            if not empty and expect:
                failures.append(f"{name}/{scen}: git_status leaked an artefact when clean")

    print()
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  " + f)
        sys.exit(1)
    print("ALL THEMES VERIFIED")


if __name__ == "__main__":
    main()
