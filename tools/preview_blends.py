#!/usr/bin/env python3
"""Blend preview for the starship-theme repo. Truecolor render.

Run:  python3 /tmp/starship-blends.py
"""

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"


def fg(h):
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return f"\x1b[38;2;{r};{g};{b}m"


def bg(h):
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return f"\x1b[48;2;{r};{g};{b}m"


# truncated-to-last-3 path
PATH_ = "\u2026/github/starship-theme"
BRANCH = "main"
STATUS = "\u271a1 \u21e11"
LANG = "\U0001f40d py 3.12.1"
TIME = "22:41"
CHAR = "\u276f"

BLENDS = [
    dict(name="Midnight Bloom", layout="B", tag="Catppuccin base, Dracula pink branch",
         path="#89b4fa", branch="#ff79c6", clean="#a6e3a1", dirty="#ff5555",
         lang="#94e2d5", time="#6c7086", char="#a6e3a1", chipfg="#1e1e2e"),
    dict(name="Neon Sangria", layout="A", tag="Dracula purple + Material red + Tokyo cyan",
         path="#bd93f9", branch="#cba6f7", clean="#50fa7b", dirty="#ff5370",
         lang="#7dcfff", time="#6272a4", char="#50fa7b", chipfg="#282a36"),
    dict(name="Terminal Frost", layout="C", tag="Tokyo blue + Dracula cyan, cool & quiet",
         path="#7aa2f7", branch="#8be9fd", clean="#c3e88d", dirty="#f7768e",
         lang="#b4befe", time="#565f89", char="#9ece6a", chipfg="#1a1b26"),
    dict(name="Gruvbox Ember", layout="A", tag="pure Gruvbox warm, retro terminal",
         path="#d65d0e", branch="#d79921", clean="#98971a", dirty="#cc241d",
         lang="#fab387", time="#665c54", char="#b8bb26", chipfg="#282828"),
    dict(name="Cyber Tokyo", layout="B", tag="Tokyo violet + neon magenta/green",
         path="#bb9af7", branch="#ff2a6d", clean="#05ffa1", dirty="#ff2a6d",
         lang="#7dcfff", time="#565f89", char="#05ffa1", chipfg="#1a1b26"),
    dict(name="Mocha Rose", layout="C", tag="Catppuccin pink-forward, soft",
         path="#f5c2e7", branch="#cba6f7", clean="#a6e3a1", dirty="#f38ba8",
         lang="#f2cdcd", time="#6c7086", char="#f5c2e7", chipfg="#1e1e2e"),
    dict(name="Vaporwave", layout="B", tag="magenta/cyan/mint, loud on purpose",
         path="#b967ff", branch="#ff71ce", clean="#05ffa1", dirty="#ff2a6d",
         lang="#01cdfe", time="#6c7086", char="#05ffa1", chipfg="#1a1b26"),
    dict(name="Slate Minimal", layout="C", tag="near-monochrome, one accent",
         path="#9aa5ce", branch="#c0caf5", clean="#9ece6a", dirty="#f7768e",
         lang="#737aa2", time="#565f89", char="#c0caf5", chipfg="#1a1b26"),
    dict(name="Amber CRT", layout="A", tag="amber phosphor, old-school terminal",
         path="#ffb000", branch="#ffcc00", clean="#ffb000", dirty="#ff5f00",
         lang="#ffd580", time="#8a6d3b", char="#ffb000", chipfg="#1c1c1c"),
    dict(name="Iceberg", layout="A", tag="cool desaturated blue/white",
         path="#8fbcbb", branch="#88c0d0", clean="#a3be8c", dirty="#bf616a",
         lang="#81a1c1", time="#4c566a", char="#88c0d0", chipfg="#2e3440"),
]

LAYOUT_NAME = {"A": "spaced", "B": "chips", "C": "divider"}


def render(b):
    p = b
    if p["layout"] == "A":
        line1 = (
            f"{fg(p['path'])}{PATH_}{RESET}"
            f"  {fg(p['branch'])}{BRANCH}{RESET}"
            f" {fg(p['dirty'])}{STATUS}{RESET}"
            f"  {fg(p['lang'])}{LANG}{RESET}"
            f"  {fg(p['time'])}{DIM}{TIME}{RESET}"
        )
    elif p["layout"] == "B":
        line1 = (
            f"{bg(p['path'])}{fg(p['chipfg'])} {PATH_} {RESET}"
            f" {bg(p['branch'])}{fg(p['chipfg'])} {BRANCH} {STATUS} {RESET}"
            f" {bg(p['lang'])}{fg(p['chipfg'])} {LANG} {RESET}"
            f" {fg(p['time'])}{DIM}{TIME}{RESET}"
        )
    else:
        line1 = (
            f"{fg(p['path'])}{PATH_}{RESET}"
            f" {fg(p['time'])}{DIM}\u2502{RESET}"
            f" {fg(p['branch'])}{BRANCH}{RESET}"
            f"{fg(p['dirty'])} {STATUS}{RESET}"
            f" {fg(p['time'])}{DIM}\u2502{RESET}"
            f" {fg(p['lang'])}{LANG}{RESET}"
        )
    return line1 + "\n" + f"{fg(p['char'])}{BOLD}{CHAR}{RESET} "


def main():
    print()
    print("=" * 74)
    print("  STARSHIP BLEND CANDIDATES \u2014 path truncated to last 3")
    print("=" * 74)
    for i, b in enumerate(BLENDS, 1):
        print()
        print(
            f"  {BOLD}{i:>2}. {b['name']}{RESET}"
            f"  {DIM}[{LAYOUT_NAME[b['layout']]}]{RESET}"
        )
        print(f"      {DIM}{b['tag']}{RESET}")
        for line in render(b).split("\n"):
            print(f"      {line}")
    print()
    print("=" * 74)
    print("  Reply with the numbers you want shipped.")
    print("=" * 74)
    print()


if __name__ == "__main__":
    main()
