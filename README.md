# starship-theme

A collection of minimal [Starship](https://starship.rs) prompt themes with **rounded solid chips**.  
Each theme uses Nerd Font `\ue0b6` / `\ue0b4` caps and a cohesive palette.

> **Requires** a [Nerd Font](https://www.nerdfonts.com/) in your terminal.

---

## Themes

| # | Name | Palette Family | Base |
|---|------|---------------|------|
| 1 | `midnight-bloom` | Catppuccin Mocha + Dracula pink | `#1e1e2e` |
| 2 | `dracula-classic` | Pure Dracula | `#282a36` |
| 3 | `catppuccin-mocha` | Pure Catppuccin Mocha | `#1e1e2e` |
| 4 | `catppuccin-macchiato` | Pure Catppuccin Macchiato | `#24273a` |
| 5 | `cyber-tokyo` | Tokyo Night + neon magenta | `#1a1b26` |
| 6 | `tokyo-night` | Pure Tokyo Night | `#1a1b26` |
| 7 | `material-ocean` | Material Ocean | `#0f111a` |
| 8 | `nord-frost` | Pure Nord | `#2e3440` |
| 9 | `vaporwave` | Magenta/cyan/mint, loud | `#1a1b26` |
| 10 | `gruvbox-ember` | Gruvbox Dark warm | `#282828` |

---

## Prompt Layout

```
 ~/p/my-project  󰊢 main ✓   3.12.0   <dim time>
❯
```

**Segments:** `path` (last 3) → `git_branch` + `git_status` → `lang` (python/rust/go/node) → `cmd_duration` (dim, no chip) → `❯` on second line.

---

## Install

```bash
git clone https://github.com/Aviksaikat/starship-theme.git ~/starship-theme
cd ~/starship-theme
bash install.sh
```

`install.sh` symlinks every `themes/*.toml` into `~/.config/starship/`.

If your shell already uses:

```zsh
export STARSHIP_CONFIG=$(ls $HOME/.config/starship/*.toml | grep -v -e 'jetpack.toml' -e 'starship.toml.bak' | shuf -n1)
```

…the new themes are picked up automatically on every new shell session — no further config needed.

---

## Preview

Run the truecolor preview script (requires a 24-bit terminal):

```bash
python3 tools/preview_rounded.py
```

> Screenshots / previews coming soon.

---

## Structure

```
starship-theme/
  themes/           # 10 x .toml theme files
  tools/
    preview_rounded.py
    preview_blends.py
  install.sh
  README.md
  .gitignore
```
