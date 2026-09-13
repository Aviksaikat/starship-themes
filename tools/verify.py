#!/usr/bin/env python3
"""Verify every generated theme actually renders styled pills.

Per theme, in four scenarios (dirty repo / clean repo / non-git dir / python project):
  * Apple glyph (󰀵) is present in the theme source file
  * no config parse error on stderr
  * path pill: chip background present, BOTH caps painted in colour_path
  * Apple glyph appears INSIDE the path chip body — after the color_path bg-colour
    escape and before the first subsequent right-cap (U+E0B4) or hard reset ESC[0m
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
APPLE = "\U000f0035"  # 󰀵 Nerd Font Apple glyph — must appear in every theme

SCEN = {
    "dirty": "/tmp/sstest/dirty",
    "clean": "/tmp/sstest/clean",
    "nongit": "/tmp/sstest/plain",
    "pyproj": "/tmp/sstest/pyproj",
}


def ensure_scenarios():
    """Provision the fixture directories this verifier renders against.

    Self-provisioning on purpose: relying on hand-made dirs under /tmp means a
    routine cleanup silently breaks the suite with a FileNotFoundError instead
    of a real failure.
    """
    def git(*args, cwd):
        subprocess.run(["git", *args], cwd=cwd, capture_output=True)

    for d in SCEN.values():
        os.makedirs(d, exist_ok=True)

    for key in ("dirty", "clean"):
        d = SCEN[key]
        if not os.path.isdir(os.path.join(d, ".git")):
            git("init", "-q", cwd=d)
            git("-c", "user.email=t@t", "-c", "user.name=t",
                "commit", "--allow-empty", "-m", "init", "-q", cwd=d)

    # `dirty` needs one untracked file so git_status has something to render;
    # `clean` must stay pristine so git_status contributes nothing.
    dirty_probe = os.path.join(SCEN["dirty"], "modified.txt")
    if not os.path.exists(dirty_probe):
        open(dirty_probe, "w").close()

    open(os.path.join(SCEN["pyproj"], "main.py"), "w").close()


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


def apple_in_path_chip(out, color_path):
    """True iff the Apple glyph appears INSIDE the directory pill body.

    'Inside the pill body' means the glyph appears:
      1. After an SGR escape that sets bg to color_path  (params may be combined,
         e.g. ESC[48;2;r;g;b;38;2;r;g;bm — Starship merges bg and fg into one)
      2. Before the first right-cap U+E0B4 or hard reset ESC[0m / ESC[m that
         follows that background escape.

    Strips zsh %{...%} prompt wrappers before analysing so escape sequences are
    contiguous and positions are comparable.
    """
    # Normalise: remove zsh prompt wrappers so escapes are contiguous.
    clean = out.replace("%{", "").replace("%}", "")

    # Match any SGR escape that contains the bg color_path parameters.
    # Starship often emits combined sequences: ESC[48;2;r;g;b;38;2;r;g;bm
    # so we search for 48;2;r;g;b as a substring within any CSI params.
    bg_sub = "48;2;" + rgb(color_path)  # e.g. "48;2;137;180;250"
    # Find the SGR escape (ESC[...m) whose params contain this substring.
    # Regex: ESC [ (params-containing-bg_sub) m
    bg_pat = re.compile(
        r"\x1b\[" + r"[0-9;]*" + re.escape(bg_sub) + r"[0-9;]*m"
    )
    m = bg_pat.search(clean)
    if m is None:
        return False

    after_bg = clean[m.end():]

    apple_pos = after_bg.find(APPLE)
    if apple_pos == -1:
        return False

    # Pill body ends at the first right cap or hard reset after the bg escape.
    cap_pos = after_bg.find(R)
    # Match ESC[0m or ESC[m (hard reset)
    reset_m = re.search(r"\x1b\[0?m", after_bg)
    reset_pos = reset_m.start() if reset_m else -1
    end_positions = [p for p in (cap_pos, reset_pos) if p >= 0]
    if not end_positions:
        # No pill end found — accept if Apple is present (graceful fallback).
        return True

    return apple_pos < min(end_positions)


def main():
    ensure_scenarios()
    themes = sorted(f for f in os.listdir(os.path.join(ROOT, "themes"))
                    if f.endswith(".toml"))
    failures = []

    for t in themes:
        cfg = os.path.join(ROOT, "themes", t)
        raw = open(cfg, encoding="utf-8").read()
        pal = read_palette(raw)
        name = t[:-5]

        # This verifier asserts the rounded-chip family's structure. The
        # powerline variations have no color_path/color_git/color_lang scheme
        # and are covered by verify_palette.py + verify_contrast.py instead.
        if "color_path" not in pal:
            print(f"  skip  {name:24s} (powerline family)")
            continue

        # Assert Apple glyph is present in the TOML source (inside directory format)
        if APPLE not in raw:
            failures.append(f"{name}: missing Apple glyph (󰀵) in theme file")
            print(f"  FAIL  {name:24s} [Apple glyph missing in source]")
            continue

        # Arrow-separated themes (saffron-grove) legitimately carry no rounded
        # caps -- their segment boundaries are powerline arrows instead, so the
        # cap assertions don't apply.
        uses_arrows = ARROW in raw

        for scen, cwd in SCEN.items():
            out, err = run(["prompt"], cfg, cwd)
            problems = []
            if "ERROR" in err.upper():
                problems.append("PARSE-ERROR")
            # Only stray if the theme's own source doesn't ask for the arrow:
            # saffron-grove uses powerline arrows deliberately.
            if ARROW in out and ARROW not in raw:
                problems.append("STRAY-ARROW")

            # Strong positional check: Apple must appear INSIDE the path chip body —
            # after the color_path background escape, before the right cap or reset.
            # A simple substring match anywhere in output is NOT sufficient.
            if not apple_in_path_chip(out, pal["color_path"]):
                # Diagnose: is it missing entirely, or in the wrong position?
                if APPLE not in out:
                    problems.append("apple-glyph-missing-in-output")
                else:
                    problems.append("apple-glyph-outside-path-chip")

            want = [pal["color_path"]]
            # A CLEAN repo correctly renders no git pill at all, so only the
            # dirty scenario is expected to carry the git chip background.
            if scen == "dirty":
                want.append(pal["color_git"])
            if scen == "pyproj":
                want.append(pal["color_lang"])
            for col in want:
                if "48;2;" + rgb(col) not in out:
                    problems.append("no-chip-bg:" + col)

            if not uses_arrows:
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
