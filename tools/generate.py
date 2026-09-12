#!/usr/bin/env python3
"""Generate the starship-theme TOML files from a single template.

Design: minimal rounded-chip prompt.
  <path pill> <git branch pill> <git status text> <lang pills> <dim cmd_duration>
  ❯

Rules learned the hard way (starship 1.26):
  * Palette keys MUST be lowercase. An uppercase key (e.g. BASE) does not
    resolve, and the failed lookup silently strips the styling from the whole
    styled group it appears in.
  * The rounded cap glyph must live INSIDE the styled group:
        [<cap>](fg:color)  -> cap painted in that colour
    Putting it outside the brackets leaves the glyph unstyled.
  * git_status is wrapped in a conditional group `( ... )` so a clean working
    tree renders nothing at all (no empty pill, no stray cap).
  * Each pill carries BOTH caps, so a segment that is absent never leaves a
    dangling cap behind.
  * truncate_to_repo = false so the path is always the last 3 components.

Run:  python3 tools/generate.py
"""

import os

L = "\ue0b6"  #  rounded left cap
R = "\ue0b4"  #  rounded right cap
ARROW = "\u276f"  # ❯
ELLIPSIS = "\u2026"  # …

THEMES = {
    "midnight-bloom": dict(
        desc="Catppuccin Mocha base with a Dracula-pink git branch",
        path="#89b4fa", git="#ff79c6", lang="#94e2d5", time="#6c7086", base="#1e1e2e",
    ),
    "dracula-classic": dict(
        desc="The canonical Dracula palette",
        path="#bd93f9", git="#ff79c6", lang="#8be9fd", time="#6272a4", base="#282a36",
    ),
    "catppuccin-mocha": dict(
        desc="Catppuccin Mocha — blue path, mauve branch, green lang",
        path="#89b4fa", git="#cba6f7", lang="#a6e3a1", time="#6c7086", base="#1e1e2e",
    ),
    "catppuccin-macchiato": dict(
        desc="Catppuccin Macchiato — the middle-dark Catppuccin flavour",
        path="#8aadf4", git="#c6a0f6", lang="#8bd5ca", time="#6e738d", base="#24273a",
    ),
    "cyber-tokyo": dict(
        desc="Tokyo Night violets with a neon-magenta branch",
        path="#bb9af7", git="#ff2a6d", lang="#7dcfff", time="#565f89", base="#1a1b26",
    ),
    "tokyo-night": dict(
        desc="Pure Tokyo Night — cool blue and violet",
        path="#7aa2f7", git="#bb9af7", lang="#73daca", time="#565f89", base="#1a1b26",
    ),
    "material-ocean": dict(
        desc="Material Ocean — deep navy with pastel accents",
        path="#82aaff", git="#c792ea", lang="#80cbc4", time="#546e7a", base="#0f111a",
    ),
    "nord-frost": dict(
        desc="Pure Nord — frost blues on polar night",
        path="#88c0d0", git="#81a1c1", lang="#a3be8c", time="#4c566a", base="#2e3440",
    ),
    "vaporwave": dict(
        desc="Vaporwave — magenta, cyan and mint, loud on purpose",
        path="#b967ff", git="#ff71ce", lang="#01cdfe", time="#6c7086", base="#1a1b26",
    ),
    "gruvbox-ember": dict(
        desc="Gruvbox Dark — warm embers and retro yellow",
        path="#d79921", git="#fe8019", lang="#8ec07c", time="#665c54", base="#282828",
    ),
}

# One pill builder: cap / content / cap, all lower-case palette refs.
def pill(color, content, prefix=" "):
    return (f'{prefix}[{L}](fg:{color})[{content}](fg:base bg:{color})[{R}](fg:{color})')


TEMPLATE = '''"$schema" = "https://starship.rs/config-schema.json"

add_newline = true
command_timeout = 20

format = """
$directory\\
$git_branch\\
$git_status\\
$c$rust$golang$nodejs$python\\
$cmd_duration\\
$line_break\\
$character"""

palette = "{name}"

# --- path -------------------------------------------------------------------
[directory]
format = "{path_pill}"
truncation_length = 3
truncation_symbol = "{ELLIPSIS}/"
truncate_to_repo = false

# --- git --------------------------------------------------------------------
[git_branch]
format = "{git_pill}"

# Renders only when the working tree is dirty; nothing at all when clean.
[git_status]
format = "([ $all_status$ahead_behind](fg:color_git))"

# --- languages (each renders only when detected) ----------------------------
[c]
format = "{lang_pill}"

[rust]
format = "{lang_pill}"

[golang]
format = "{lang_pill}"

[nodejs]
format = "{lang_pill}"

[python]
format = "{lang_pill}"

# --- command duration -------------------------------------------------------
[cmd_duration]
show_milliseconds = false
format = " [$duration](fg:color_time)"
min_time = 1000

# --- character --------------------------------------------------------------
[character]
success_symbol = "[{ARROW}](bold fg:color_path)"
error_symbol = "[{ARROW}](bold red)"

[palettes.{name}]
color_path = "{path}"
color_git = "{git}"
color_lang = "{lang}"
color_time = "{time}"
base = "{base}"
'''


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outdir = os.path.join(root, "themes")
    os.makedirs(outdir, exist_ok=True)

    pills = dict(
        path_pill=pill("color_path", "$path", prefix=""),
        git_pill=pill("color_git", "$symbol$branch"),
        lang_pill=pill("color_lang", "$symbol$version"),
    )

    for name, p in THEMES.items():
        body = TEMPLATE.format(name=name, ARROW=ARROW, ELLIPSIS=ELLIPSIS, **pills, **p)
        with open(os.path.join(outdir, name + ".toml"), "w", encoding="utf-8") as fh:
            fh.write(body)
        print("wrote themes/" + name + ".toml")


if __name__ == "__main__":
    main()
