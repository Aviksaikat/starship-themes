#!/usr/bin/env python3
"""Generate the starship-theme TOML files from a single template.

Design: minimal rounded-chip prompt.
  <apple prefix> <path pill> <git branch pill> <git status text> <lang pills> <dim cmd_duration>
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
  * Apple glyph 󰀵 (U+F0035 Nerd Font) is embedded inside the directory pill
    content as `󰀵 $path` — it shares the chip's background colour so it
    reads as part of the path chip, not a standalone prefix. This is the
    correct visual appearance (logo inside the rounded chip on macOS).

Run:  python3 tools/generate.py
"""

import os

L = "\ue0b6"  #  rounded left cap
R = "\ue0b4"  #  rounded right cap
ARROW = "\u276f"  # ❯
ELLIPSIS = "\u2026"  # …
APPLE = "\U000f0035"  # 󰀵  Nerd Font Apple glyph (macOS)

THEMES = {
    # ── original 10 themes ────────────────────────────────────────────────
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
    "tokyo-night-minimal": dict(
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
    # ── 7 new themes ──────────────────────────────────────────────────────
    "arch-os": dict(
        desc="Arch OS — polar-night base (#2e3440), snow-storm path (#d8dee9), aurora-green git (#a3be8c), aurora-yellow lang (#ebcb8b), dim time (#4c566a)",
        path="#d8dee9", git="#a3be8c", lang="#ebcb8b", time="#4c566a", base="#2e3440",
    ),
    "tokyo-night-neo": dict(
        desc="Tokyo Night Neo — electric blue path, neon-magenta branch",
        path="#769ff0", git="#ff2a6d", lang="#7dcfff", time="#565f89", base="#0f111a",
    ),
    "ccswe-dark": dict(
        desc="CoryCharlton dark — indigo path, ember git, emerald lang",
        path="#769ff0", git="#eb4d28", lang="#5fa04e", time="#999999", base="#1d2230",
    ),
    "ninetailedstarship-latte": dict(
        desc="Ninetailed Catppuccin Latte — teal path, mauve git, green lang",
        path="#179299", git="#8839ef", lang="#3d9a29", time="#6c6f85", base="#eff1f5",
    ),
    "ninetailedstarship-frappe": dict(
        desc="Ninetailed Catppuccin Frappé — sky path, mauve git, teal lang",
        path="#99d1db", git="#ca9ee6", lang="#81c8be", time="#737994", base="#303446",
    ),
    "ninetailedstarship-macchiato": dict(
        desc="Ninetailed Catppuccin Macchiato — teal path, lavender git",
        path="#8bd5ca", git="#c6a0f6", lang="#91d7e3", time="#6e738d", base="#24273a",
    ),
    "ninetailedstarship-mocha": dict(
        desc="Ninetailed Catppuccin Mocha — pink path, mauve git, teal lang",
        path="#f38ba8", git="#cba6f7", lang="#94e2d5", time="#585b70", base="#1e1e2e",
    ),
}


# One pill builder: cap / content / cap, all lower-case palette refs.
def pill(color, content, prefix=" "):
    return f'{prefix}[{L}](fg:{color})[{content}](fg:base bg:{color})[{R}](fg:{color})'


def build_toml(name, path, git, lang, time, base, **_ignored):
    """Build a complete TOML config string for one theme.

    The Apple glyph 󰀵 is embedded inside the directory pill content, so it
    shares the chip's background colour and reads as part of the path chip.
    format = is a single TOML basic string (no multiline magic needed).
    """
    path_pill = pill("color_path", f"{APPLE} $path", prefix="")
    git_pill  = pill("color_git",  "$symbol$branch")
    lang_pill = pill("color_lang", "$symbol$version")

    # Single-line format value: module refs only (Apple is inside $directory pill).
    fmt = ("$directory"
           "$git_branch"
           "$git_status"
           "$c$rust$golang$nodejs$python"
           "$cmd_duration"
           "$line_break"
           "$character")

    return (
        f'"$schema" = "https://starship.rs/config-schema.json"\n'
        f'\n'
        f'add_newline = true\n'
        f'command_timeout = 20\n'
        f'\n'
        f'format = "{fmt}"\n'
        f'\n'
        f'palette = "{name}"\n'
        f'\n'
        f'# --- path -------------------------------------------------------------------\n'
        f'[directory]\n'
        f'format = "{path_pill}"\n'
        f'truncation_length = 3\n'
        f'truncation_symbol = "{ELLIPSIS}/"\n'
        f'truncate_to_repo = false\n'
        f'\n'
        f'# --- git --------------------------------------------------------------------\n'
        f'[git_branch]\n'
        f'format = "{git_pill}"\n'
        f'\n'
        f'# Renders only when the working tree is dirty; nothing at all when clean.\n'
        f'[git_status]\n'
        f'format = "([ $all_status$ahead_behind](fg:color_git))"\n'
        f'\n'
        f'# --- languages (each renders only when detected) ----------------------------\n'
        f'[c]\n'
        f'format = "{lang_pill}"\n'
        f'\n'
        f'[rust]\n'
        f'format = "{lang_pill}"\n'
        f'\n'
        f'[golang]\n'
        f'format = "{lang_pill}"\n'
        f'\n'
        f'[nodejs]\n'
        f'format = "{lang_pill}"\n'
        f'\n'
        f'[python]\n'
        f'format = "{lang_pill}"\n'
        f'\n'
        f'# --- command duration -------------------------------------------------------\n'
        f'[cmd_duration]\n'
        f'show_milliseconds = false\n'
        f'format = " [$duration](fg:color_time)"\n'
        f'min_time = 1000\n'
        f'\n'
        f'# --- character --------------------------------------------------------------\n'
        f'[character]\n'
        f'success_symbol = "[{ARROW}](bold fg:color_path)"\n'
        f'error_symbol = "[{ARROW}](bold red)"\n'
        f'\n'
        f'[palettes.{name}]\n'
        f'color_path = "{path}"\n'
        f'color_git = "{git}"\n'
        f'color_lang = "{lang}"\n'
        f'color_time = "{time}"\n'
        f'base = "{base}"\n'
    )


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outdir = os.path.join(root, "themes")
    os.makedirs(outdir, exist_ok=True)

    for name, p in THEMES.items():
        body = build_toml(name, **p)
        with open(os.path.join(outdir, name + ".toml"), "w", encoding="utf-8") as fh:
            fh.write(body)
        print("wrote themes/" + name + ".toml")


if __name__ == "__main__":
    main()
