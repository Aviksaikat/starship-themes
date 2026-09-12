# Starship Theme — Design Document

Date: 2026-09-12
Repo: https://github.com/Aviksaikat/starship-theme

---

## Goal

A collection of minimal Starship prompt themes with rounded solid chips.
Drops into the existing random-pick setup in `.zshrc` / `config.fish`.

---

## Terminal Context (backgrounds to render against)

| Terminal  | Theme                | Background |
|-----------|----------------------|------------|
| Ghostty   | Dracula              | `#282a36`  |
| WezTerm   | Dracula (Official)   | `#282a36`  |
| Alacritty | Catppuccin Mocha     | `#1e1e2e`  |
| Kitty     | Catppuccin Macchiato | `#24273a`  |
| Nord      | (available/planned)  | `#2e3440`  |

All backgrounds are near-black dark. Chip bg colors must be vivid enough to
pop against all five. Chip foreground text uses the matching dark base so the
text looks "native" to that palette family.

---

## Prompt Layout — Rounded Chips

Single line of rounded solid chips, dim time on right, `❯` on second line.

```
 <path>   <branch status>   <lang>   <dim time>
❯
```

Rounded caps: `\ue0b6` (left) and `\ue0b4` (right) — Nerd Font required.
These are already in use in the existing pl10k_like.toml.

### Segments

| Segment      | Content                         | Notes                         |
|--------------|---------------------------------|-------------------------------|
| path         | `$directory` truncated to 3     | chip bg = path_color          |
| git          | branch + all_status + ahead/behind | only shown inside git repos|
| lang         | python / rust / go / node etc   | only shown when detected      |
| time         | HH:MM, dimmed, no chip          | always shown                  |
| character    | `❯` green / red on error        | second line                   |

---

## Themes — 10 total

Chip `txt` (text inside the chip) always uses the matching dark base so text
contrast is correct and the chip feels "native" to each palette family.

| # | Name             | Palette family              | Chip text base |
|---|------------------|-----------------------------|----------------|
| 1 | midnight-bloom   | Catppuccin Mocha + Dracula pink | `#1e1e2e`  |
| 2 | dracula-classic  | Pure Dracula                | `#282a36`      |
| 3 | catppuccin-mocha | Pure Catppuccin Mocha       | `#1e1e2e`      |
| 4 | catppuccin-macchiato | Pure Catppuccin Macchiato | `#24273a`    |
| 5 | cyber-tokyo      | Tokyo Night + neon magenta  | `#1a1b26`      |
| 6 | tokyo-night      | Pure Tokyo Night            | `#1a1b26`      |
| 7 | material-ocean   | Material Ocean              | `#0f111a`      |
| 8 | nord-frost       | Pure Nord                   | `#2e3440`      |
| 9 | vaporwave        | Magenta/cyan/mint, loud     | `#1a1b26`      |
|10 | gruvbox-ember    | Gruvbox Dark warm           | `#282828`      |

---

## File Structure

```
starship-theme/
  themes/
    midnight-bloom.toml
    dracula-classic.toml
    catppuccin-mocha.toml
    catppuccin-macchiato.toml
    cyber-tokyo.toml
    tokyo-night.toml
    material-ocean.toml
    nord-frost.toml
    vaporwave.toml
    gruvbox-ember.toml
  tools/
    preview_rounded.py      (truecolor terminal preview)
    preview_blends.py
  README.md
  install.sh                (symlinks all themes into ~/.config/starship/)
```

---

## Install Script

`install.sh` symlinks every `themes/*.toml` into `~/.config/starship/`.
The existing `.zshrc` line already does `shuf -n1` over all `.toml` files
(excluding jetpack and .bak), so new themes are picked up automatically.

---

## TOML Conventions (per theme)

```toml
# rounded left cap: \ue0b6  right cap: \ue0b4
# Each segment uses: fg(BASE) bg(CHIP_COLOR) + caps in CHIP_COLOR fg on transparent

format = """
[](color_path)\
$directory\
[](fg:color_path bg:color_git)\
$git_branch\
$git_status\
[](fg:color_git bg:color_lang)\
...
[ ](fg:color_last)\
$cmd_duration\
$line_break\
$character"""

[directory]
truncation_length = 3
truncation_symbol = "…/"
style = "fg:BASE bg:color_path"
format = "[ $path ]($style)"
```

Each theme defines a `[palettes.NAME]` block with semantic names:
`color_path`, `color_git`, `color_lang`, `color_time`, `BASE` (text in chips).

---

## Implementation Plan (tasks)

**T1** — Scaffold repo structure + install.sh + .gitignore
**T2** — Write themes 1-5 (midnight-bloom, dracula-classic, catppuccin-mocha, catppuccin-macchiato, cyber-tokyo)
**T3** — Write themes 6-10 (tokyo-night, material-ocean, nord-frost, vaporwave, gruvbox-ember)
**T4** — Write README.md with screenshots section + install instructions
**T5** — Update tools/preview_rounded.py to match final themes
**T6** — Initial commit + push to GitHub
**T7** — Update ~/.zshrc STARSHIP_CONFIG line to include new themes dir; update fish config

---

## Integration — existing .zshrc

Current line (line 142):
```zsh
export STARSHIP_CONFIG=$(ls $HOME/.config/starship/*.toml | grep -v -e 'jetpack.toml' -e 'starship.toml.bak' | shuf -n1)
```

After install.sh symlinks the new themes into `~/.config/starship/`, they
are included in the pool automatically — no .zshrc change needed.
