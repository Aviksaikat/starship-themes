#!/usr/bin/env python3
"""Rounded-chip blend preview (Powerline rounded caps + solid bg).

Run:  python3 /tmp/starship-rounded.py
"""

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
LEFT = "\ue0b6"     #  rounded left cap
RIGHT = "\ue0b4"    #  rounded right cap


def fg(h):
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return f"\x1b[38;2;{r};{g};{b}m"


def bg(h):
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return f"\x1b[48;2;{r};{g};{b}m"


PATH_ = "\u2026/github/starship-theme"
BRANCH = "main"
STATUS = "\u271a1 \u21e11"
LANG = "\U0001f40d py 3.12.1"
TIME = "22:41"
CHAR = "\u276f"

THEMES = [
    dict(name="Midnight Bloom", tag="Catppuccin base, Dracula pink branch",
         path="#89b4fa", branch="#ff79c6", lang="#94e2d5",
         clean="#a6e3a1", dirty="#ff5555", time="#6c7086",
         txt="#1e1e2e", chipfg="#1e1e2e"),
    dict(name="Dracula Classic", tag="the canonical Dracula palette",
         path="#bd93f9", branch="#ff79c6", lang="#8be9fd",
         clean="#50fa7b", dirty="#ff5555", time="#6272a4",
         txt="#282a36", chipfg="#282a36"),
    dict(name="Catppuccin Mocha", tag="mauve / blue / teal, soft",
         path="#89b4fa", branch="#cba6f7", lang="#94e2d5",
         clean="#a6e3a1", dirty="#f38ba8", time="#6c7086",
         txt="#1e1e2e", chipfg="#1e1e2e"),
    dict(name="Cyber Tokyo", tag="Tokyo violet + neon magenta",
         path="#bb9af7", branch="#ff2a6d", lang="#7dcfff",
         clean="#05ffa1", dirty="#ff2a6d", time="#565f89",
         txt="#1a1b26", chipfg="#1a1b26"),
    dict(name="Vaporwave", tag="magenta / cyan / mint, loud",
         path="#b967ff", branch="#ff71ce", lang="#01cdfe",
         clean="#05ffa1", dirty="#ff2a6d", time="#6c7086",
         txt="#1a1b26", chipfg="#1a1b26"),
    dict(name="Tokyo Night", tag="cool blue-violet, calm",
         path="#7aa2f7", branch="#bb9af7", lang="#7dcfff",
         clean="#9ece6a", dirty="#f7768e", time="#565f89",
         txt="#1a1b26", chipfg="#1a1b26"),
    dict(name="Material", tag="Material Design blues + teal",
         path="#82aaff", branch="#c792ea", lang="#80cbc4",
         clean="#c3e88d", dirty="#ff5370", time="#546e7a",
         txt="#263238", chipfg="#263238"),
    dict(name="Gruvbox Ember", tag="warm retro, orange / yellow",
         path="#d65d0e", branch="#d79921", lang="#8ec07c",
         clean="#b8bb26", dirty="#cc241d", time="#665c54",
         txt="#282828", chipfg="#282828"),
    dict(name="Iceberg", tag="cold desaturated blue/white",
         path="#8fbcbb", branch="#88c0d0", lang="#81a1c1",
         clean="#a3be8c", dirty="#bf616a", time="#4c566a",
         txt="#2e3440", chipfg="#2e3440"),
    dict(name="Amber CRT", tag="amber phosphor terminal",
         path="#ffb000", branch="#ffcc00", lang="#ffd580",
         clean="#ffb000", dirty="#ff5f00", time="#8a6d3b",
         txt="#1c1c1c", chipfg="#1c1c1c"),
]


def chip(p, color, text):
    """One rounded solid chip."""
    return (
        f"{fg(color)}{LEFT}"
        f"{bg(color)}{fg(p['txt'])} {text} "
        f"{RESET}{fg(color)}{RIGHT}{RESET}"
    )


def render(t):
    p = t
    status_color = p["dirty"]
    git_txt = f"{BRANCH} {STATUS}"
    parts = [
        chip(p, p["path"], PATH_),
        chip(p, p["branch"], git_txt),
        chip(p, p["lang"], LANG),
    ]
    line1 = " ".join(parts) + f"  {fg(p['time'])}{DIM}{TIME}{RESET}"
    return line1 + "\n" + f"{fg(p['clean'])}{BOLD}{CHAR}{RESET} "


def main():
    print()
    print("=" * 76)
    print("  STARSHIP \u2014 ROUNDED SOLID CHIPS  (path \u2192 last 3)")
    print("=" * 76)
    for i, t in enumerate(THEMES, 1):
        print()
        print(f"  {BOLD}{i:>2}. {t['name']}{RESET}  {DIM}{t['tag']}{RESET}")
        for line in render(t).split("\n"):
            print(f"      {line}")
    print()
    print("=" * 76)
    print("  The \ue0b6 \ue0b4 caps need a Nerd Font (you already have one).")
    print("=" * 76)
    print()


if __name__ == "__main__":
    main()
