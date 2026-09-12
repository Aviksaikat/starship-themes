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
    "pastel-catppuccin": ["#45475A", "#CBA6F7", "#F38BA8", "#89B4FA", "#94E2D5", "#313244"],
    "pastel-gruvbox":    ["#3C3836", "#D79921", "#FB4934", "#83A598", "#458588", "#282828"],
    "pastel-everforest": ["#374145", "#A7C080", "#E67E80", "#7FBBB3", "#83C092", "#2B3339"],
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
        "color_fg0": "#3c3836", "color_bg1": "#ebdbb2", "color_bg3": "#bdae93",
        "color_blue": "#458588", "color_aqua": "#689d6a", "color_green": "#79740e",
        "color_orange": "#d65d0e", "color_purple": "#b16286", "color_red": "#9d0006",
        "color_yellow": "#b57614",
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
        "color_fg0": "#fbf1c7", "color_bg1": "#32302f", "color_bg3": "#504945",
        "color_blue": "#a89984", "color_aqua": "#d5c4a1", "color_green": "#bdae93",
        "color_orange": "#ebdbb2", "color_purple": "#d5c4a1", "color_red": "#fb4934",
        "color_yellow": "#ddc7a1",
    },
    "gruvbox-neon": {
        "color_fg0": "#fbf1c7", "color_bg1": "#161616", "color_bg3": "#2e2e2e",
        "color_blue": "#00d4ff", "color_aqua": "#00ff88", "color_green": "#a6ff00",
        "color_orange": "#ff8c00", "color_purple": "#d97bff", "color_red": "#ff2e5b",
        "color_yellow": "#ffe600",
    },
}


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
        generated.append(write(name, text))

    # --- pastel-powerline ---
    base = read(os.path.join(SRC, "pastel-powerline.toml"))
    for name, colors in PASTEL_VARIATIONS.items():
        text = sub_hex(base, dict(zip(PASTEL_SLOTS, colors)))
        generated.append(write(name, text))

    # --- catppuccin ---
    base = read(os.path.join(SRC, "catppuccin.toml"))
    for name, ov in CAT_OVERRIDES.items():
        text = apply_palette(base, "catppuccin_mocha", name, ov)
        generated.append(write(name, text))

    # --- gruvbox_rainbow ---
    base = read(os.path.join(SRC, "gruvbox_rainbow.toml"))
    for name, ov in GRUVBOX_OVERRIDES.items():
        text = apply_palette(base, "gruvbox_dark", name, ov)
        generated.append(write(name, text))

    for p in generated:
        print(os.path.basename(p))
    print(f"\n{len(generated)} themes generated into {OUT}")


if __name__ == "__main__":
    main()
