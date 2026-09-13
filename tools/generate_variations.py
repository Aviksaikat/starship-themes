#!/usr/bin/env python3
"""Generate powerline-style variations of Avik's original dotfiles starship themes.

Sources (read-only, dotfiles-managed — never overwritten):
  ~/git_projects/gitlab/dotfiles_with_stow/starship/.config/starship/
    pl10k_like.toml         inline-hex palette -> hex substitution
    pastel-powerline.toml   inline-hex palette -> hex substitution
    catppuccin.toml         named palette      -> override palette keys
    gruvbox_rainbow.toml    named palette      -> override palette keys

Output: themes/<name>.toml in this repo (6 variations per original).
"""
import os
import re
import sys

SRC = os.path.expanduser(
    "~/git_projects/gitlab/dotfiles_with_stow/starship/.config/starship"
)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "themes")


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(name, text):
    path = os.path.join(OUT, name + ".toml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def sub_hex(text, mapping):
    """Single-pass hex substitution — keyed case-insensitively."""
    lut = {k.lower(): v for k, v in mapping.items()}

    def repl(m):
        return lut.get(m.group(0).lower(), m.group(0))

    return re.sub(r"#[0-9A-Fa-f]{6}", repl, text)


def inject_dark_fg(text, fg):
    """Pin a dark foreground onto module `style*` lines that set only a bg.

    Only matches lines whose quoted value starts with `bg:` -- the separator
    segments inside `format` already set fg (that IS the powerline arrow
    colour) and must be left alone.
    """
    return re.sub(
        r'^(\s*style(?:_user|_root)?\s*=\s*)"(bg:[^"]*)"',
        lambda m: f'{m.group(1)}"fg:{fg} {m.group(2)}"',
        text,
        flags=re.M,
    )


# ---------------------------------------------------------------------------
# 1. pl10k_like — slots in order of first appearance
#    A os/time/shell bg · B teal transition · C user/status bg · D path
#    E git · F langs · G package/aws
# ---------------------------------------------------------------------------
PL10K_SLOTS = ["#33658A", "#06969A", "#86BBD8", "#D8BB86", "#FCA17D", "#FCF392", "#7DF9AA"]

PL10K_VARIATIONS = {
    "pl10k-nord":      ["#2E3440", "#5E81AC", "#81A1C1", "#88C0D0", "#BF616A", "#EBCB8B", "#A3BE8C"],
    "pl10k-dracula":   ["#44475A", "#6272A4", "#8BE9FD", "#BD93F9", "#FF79C6", "#F1FA8C", "#50FA7B"],
    "pl10k-tokyo":     ["#1A1B26", "#7AA2F7", "#BB9AF7", "#7DCFFF", "#F7768E", "#E0AF68", "#9ECE6A"],
    "pl10k-catppuccin":["#313244", "#89B4FA", "#CBA6F7", "#F9E2AF", "#F38BA8", "#A6E3A1", "#94E2D5"],
    "pl10k-gruvbox":   ["#3C3836", "#458588", "#83A598", "#D79921", "#FB4934", "#FABD2F", "#B8BB26"],
    "pl10k-rosepine":  ["#26233A", "#31748F", "#9CCFD8", "#F6C177", "#EB6F92", "#EBBBCB", "#C4A7E7"],
}

# ---------------------------------------------------------------------------
# 2. pastel-powerline — slots
#    A os/user · B path · C git · D langs · E docker · F time
# ---------------------------------------------------------------------------
PASTEL_SLOTS = ["#9A348E", "#DA627D", "#FCA17D", "#86BBD8", "#06969A", "#33658A"]

PASTEL_VARIATIONS = {
    "pastel-nord":       ["#3B4252", "#5E81AC", "#81A1C1", "#88C0D0", "#8FBCBB", "#4C566A"],
    "pastel-dracula":    ["#44475A", "#BD93F9", "#FF79C6", "#8BE9FD", "#6272A4", "#282A36"],
    "pastel-tokyo":      ["#1A1B26", "#7AA2F7", "#F7768E", "#BB9AF7", "#7DCFFF", "#16161E"],
    "pastel-catppuccin": ["#A6ADC8", "#CBA6F7", "#F38BA8", "#89B4FA", "#94E2D5", "#F9E2AF"],
    "pastel-gruvbox":    ["#3C3836", "#D79921", "#FB4934", "#83A598", "#458588", "#282828"],
    "pastel-everforest": ["#D3C6AA", "#A7C080", "#E67E80", "#7FBBB3", "#83C092", "#DBBC7F"],
}

# Themes whose chips are light enough that the terminal's default (light)
# foreground is unreadable on them -> pin a dark fg on the module styles.
# Applied ONLY to `style*` lines that carry a bg; the format's separator
# segments already set fg (that's what colours the powerline arrow) and must
# not be touched.
PASTEL_DARK_FG = {
    "pastel-catppuccin": "#1E1E2E",
    "pastel-everforest": "#2B3339",
}

# pl10k_like hardcodes `fg:green` / `fg:red` for the ✓ / ✘ character glyphs on
# the character chip. Where that chip is light, the glyph is near-invisible.
# These variants get a dark glyph instead (fg = the variant's dark os/time hue,
# errors a legible dark red).
PL10K_DARK_CHAR = {
    "pl10k-rosepine",
}

# ---------------------------------------------------------------------------
# 3. catppuccin — keep the Catppuccin accent names, override their values.
#    Only the keys the config actually references are overridden; everything
#    else is inherited from the mocha block so nothing resolves to a missing key.
# ---------------------------------------------------------------------------
CAT_OVERRIDES = {
    "catppuccin-nord": {
        "base": "#2E3440", "mantle": "#292E39", "crust": "#232831",
        "red": "#BF616A", "peach": "#D08770", "yellow": "#EBCB8B",
        "green": "#A3BE8C", "sapphire": "#5E81AC", "lavender": "#B48EAD",
        "mauve": "#B48EAD", "blue": "#81A1C1", "teal": "#8FBCBB", "sky": "#88C0D0",
    },
    "catppuccin-tokyo": {
        "base": "#1A1B26", "mantle": "#16161E", "crust": "#13131A",
        "red": "#F7768E", "peach": "#FF9E64", "yellow": "#E0AF68",
        "green": "#9ECE6A", "sapphire": "#2AC3DE", "lavender": "#BB9AF7",
        "mauve": "#BB9AF7", "blue": "#7AA2F7", "teal": "#73DACA", "sky": "#7DCFFF",
    },
    "catppuccin-rosepine": {
        "base": "#191724", "mantle": "#1F1D2E", "crust": "#16141F",
        "red": "#EB6F92", "peach": "#F6C177", "yellow": "#F6C177",
        "green": "#31748F", "sapphire": "#31748F", "lavender": "#C4A7E7",
        "mauve": "#C4A7E7", "blue": "#31748F", "teal": "#9CCFD8", "sky": "#9CCFD8",
    },
    "catppuccin-everforest": {
        "base": "#2B3339", "mantle": "#272E33", "crust": "#232A2E",
        "red": "#E67E80", "peach": "#E69875", "yellow": "#DBBC7F",
        "green": "#A7C080", "sapphire": "#7FBBB3", "lavender": "#D699B6",
        "mauve": "#D699B6", "blue": "#7FBBB3", "teal": "#83C092", "sky": "#83C092",
    },
    "catppuccin-ocean": {
        "base": "#0B1929", "mantle": "#08131F", "crust": "#060E17",
        "red": "#E06C75", "peach": "#D19A66", "yellow": "#E5C07B",
        "green": "#98C379", "sapphire": "#61AFEF", "lavender": "#C678DD",
        "mauve": "#C678DD", "blue": "#61AFEF", "teal": "#56B6C2", "sky": "#56B6C2",
    },
    "catppuccin-lavender": {
        "base": "#1E1B2E", "mantle": "#181527", "crust": "#131020",
        "red": "#F38BA8", "peach": "#FAB387", "yellow": "#F9E2AF",
        "green": "#A6E3A1", "sapphire": "#89B4FA", "lavender": "#B4BEFE",
        "mauve": "#CBA6F7", "blue": "#89B4FA", "teal": "#94E2D5", "sky": "#89DCEB",
    },
}

# ---------------------------------------------------------------------------
# 4. gruvbox_rainbow — palette keys: fg0 bg1 bg3 blue aqua green orange purple red yellow
# ---------------------------------------------------------------------------
GRUVBOX_OVERRIDES = {
    "gruvbox-material": {
        "color_fg0": "#ddc7a1", "color_bg1": "#32302f", "color_bg3": "#5a524c",
        "color_blue": "#7daea3", "color_aqua": "#89b482", "color_green": "#a9b665",
        "color_orange": "#e78a4e", "color_purple": "#d3869b", "color_red": "#ea6962",
        "color_yellow": "#d8a657",
    },
    "gruvbox-light": {
        # Light chips + dark text, so the accents must be gruvbox's BRIGHT set.
        # Using the dark accents here and letting ensure_contrast lift them
        # produces muddy mid-tones (and a murky olive prompt glyph), because it
        # starts from the wrong palette.
        "color_fg0": "#3c3836", "color_bg1": "#ebdbb2", "color_bg3": "#d5c4a1",
        "color_blue": "#83a598", "color_aqua": "#8ec07c", "color_green": "#b8bb26",
        "color_orange": "#fe8019", "color_purple": "#d3869b", "color_red": "#fb4934",
        "color_yellow": "#fabd2f",
    },
    "gruvbox-ocean": {
        "color_fg0": "#fbf1c7", "color_bg1": "#1d2021", "color_bg3": "#3c3836",
        "color_blue": "#83a598", "color_aqua": "#8ec07c", "color_green": "#b8bb26",
        "color_orange": "#fe8019", "color_purple": "#d3869b", "color_red": "#fb4934",
        "color_yellow": "#fabd2f",
    },
    "gruvbox-forest": {
        "color_fg0": "#fbf1c7", "color_bg1": "#2b3328", "color_bg3": "#4a5440",
        "color_blue": "#6f9b8a", "color_aqua": "#8ec07c", "color_green": "#b8bb26",
        "color_orange": "#e0a44a", "color_purple": "#b16286", "color_red": "#cc5f4a",
        "color_yellow": "#d7c05a",
    },
    "gruvbox-mono": {
        # A single color_fg0 serves BOTH the dark bg1/bg3 chips (time, docker)
        # AND the accent chips (path/git/langs). So fg0 must stay light and the
        # accents must be medium-dark greys -- making fg0 dark would fix the
        # accents but leave the time chip dark-on-dark.
        "color_fg0": "#fbf1c7", "color_bg1": "#3c3836", "color_bg3": "#665c54",
        "color_blue": "#665c54", "color_aqua": "#7c6f64", "color_green": "#665c54",
        "color_orange": "#7c6f64", "color_purple": "#504945", "color_red": "#cc241d",
        "color_yellow": "#928374",
    },
}


def darken_character(text, dark_fg, dark_red):
    """Make the ✓ / ✘ character glyphs legible on a light character chip.

    pl10k_like hardcodes `fg:green` and `fg:red` against the character
    background. Only the `fg:...( bg:` forms are rewritten -- the frame's
    `(bold green)` styling has no background and is left alone.
    """
    text = text.replace("fg:green bg:", f"fg:{dark_fg} bg:")
    text = text.replace("fg:red bg:", f"fg:{dark_red} bg:")
    return text


# ---------------------------------------------------------------------------
# contrast safety
# ---------------------------------------------------------------------------

# gruvbox_rainbow derives every chip's text from one `color_fg0` and uses it
# against BOTH the dark bg1/bg3 chips and the accent chips. A variant that
# lightens the accents -- or darkens fg0 to suit them -- silently produces
# unreadable chips (found by eye on gruvbox-mono: a dark time pill). Enforce a
# minimum contrast instead of hand-tuning 7 accents x 6 variants.
CHIP_BG_KEYS = ("color_bg1", "color_bg3")
CHIP_FG_KEYS = ("color_blue", "color_aqua", "color_green", "color_orange",
                "color_purple", "color_red", "color_yellow")


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(hexstr):
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _shift(hexstr, toward_white, amount):
    h = hexstr.lstrip("#")
    parts = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    if toward_white:
        parts = [p + (255 - p) * amount for p in parts]
    else:
        parts = [p * (1 - amount) for p in parts]
    return "#%02x%02x%02x" % tuple(round(p) for p in parts)


def ensure_contrast(color, against, target=3.1):
    """Nudge `color` (hue preserved) until it contrasts >= `target` with `against`."""
    if contrast(color, against) >= target:
        return color
    toward_white = lum(against) < 0.5
    cur = color
    for _ in range(200):
        cur = _shift(cur, toward_white, 0.04)
        if contrast(cur, against) >= target:
            return cur
    return cur


def parse_palette(text, block_name):
    """Return dict of key->value inside [palettes.<block_name>]."""
    m = re.search(
        r"\[palettes\." + re.escape(block_name) + r"\]\n(.*?)(?=\n\[|\Z)", text, re.S
    )
    if not m:
        raise SystemExit(f"palette block {block_name} not found")
    out = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"(\w+)\s*=\s*'([^']*)'", line.strip()) or re.match(
            r'(\w+)\s*=\s*"([^"]*)"', line.strip()
        )
        if mm:
            out[mm.group(1)] = mm.group(2)
    return out


def apply_palette(text, old_name, new_name, overrides):
    """Rename palette, switch the palette= line, append an overridden block."""
    base = parse_palette(text, old_name)
    merged = dict(base)
    merged.update(overrides)
    missing = set(base) - set(merged)
    assert not missing, missing

    text = text.replace(f"palette = '{old_name}'", f"palette = '{new_name}'")
    text = text.replace(f'palette = "{old_name}"', f'palette = "{new_name}"')

    block = "\n[palettes." + new_name + "]\n"
    for k, v in merged.items():
        block += f'{k} = "{v}"\n'
    return text.rstrip("\n") + "\n" + block


def main():
    generated = []

    # --- pl10k_like: rename nothing, pure hex swap ---
    base = read(os.path.join(SRC, "pl10k_like.toml"))
    for name, colors in PL10K_VARIATIONS.items():
        text = sub_hex(base, dict(zip(PL10K_SLOTS, colors)))
        if name in PL10K_DARK_CHAR:
            text = darken_character(text, colors[0], "#8B1A1A")
        generated.append(write(name, text))

    # --- pastel-powerline ---
    base = read(os.path.join(SRC, "pastel-powerline.toml"))
    for name, colors in PASTEL_VARIATIONS.items():
        text = sub_hex(base, dict(zip(PASTEL_SLOTS, colors)))
        if name in PASTEL_DARK_FG:
            text = inject_dark_fg(text, PASTEL_DARK_FG[name])
        generated.append(write(name, text))

    # --- catppuccin ---
    base = read(os.path.join(SRC, "catppuccin.toml"))
    for name, ov in CAT_OVERRIDES.items():
        text = apply_palette(base, "catppuccin_mocha", name, ov)
        generated.append(write(name, text))

    # --- gruvbox_rainbow ---
    base = read(os.path.join(SRC, "gruvbox_rainbow.toml"))
    # The template hardcodes #83a598 as the docker/conda text colour on
    # color_bg3, while [pixi] uses color_fg0 for the same chip. Normalise so
    # every bg3 chip tracks the variant's fg0.
    base = base.replace("fg:#83a598 bg:", "fg:color_fg0 bg:")
    for name, ov in GRUVBOX_OVERRIDES.items():
        ov = dict(ov)
        fg0 = ov["color_fg0"]
        for key in CHIP_BG_KEYS + CHIP_FG_KEYS:
            if key in ov:
                ov[key] = ensure_contrast(ov[key], fg0)
        text = apply_palette(base, "gruvbox_dark", name, ov)
        generated.append(write(name, text))

    for p in generated:
        print(os.path.basename(p))
    print(f"\n{len(generated)} themes generated into {OUT}")


if __name__ == "__main__":
    main()
