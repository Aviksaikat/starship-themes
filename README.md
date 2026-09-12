# starship-theme

Minimal [Starship](https://starship.rs) prompt themes built from **rounded solid chips** —
no powerline arrows, no clutter. Path, git branch and language, and nothing else competing
for your attention.

> **Requires a [Nerd Font](https://www.nerdfonts.com/)** — the rounded caps use
> `U+E0B6` / `U+E0B4`. Tested with CaskaydiaCove Nerd Font.

---

## Themes

| # | Name | Palette | Chip text (base) |
|---|------|---------|------------------|
| 1 | `midnight-bloom` | Catppuccin Mocha + Dracula pink | `#1e1e2e` |
| 2 | `dracula-classic` | Pure Dracula | `#282a36` |
| 3 | `catppuccin-mocha` | Pure Catppuccin Mocha | `#1e1e2e` |
| 4 | `catppuccin-macchiato` | Pure Catppuccin Macchiato | `#24273a` |
| 5 | `cyber-tokyo` | Tokyo Night + neon magenta | `#1a1b26` |
| 6 | `tokyo-night` | Pure Tokyo Night | `#1a1b26` |
| 7 | `material-ocean` | Material Ocean | `#0f111a` |
| 8 | `nord-frost` | Pure Nord | `#2e3440` |
| 9 | `vaporwave` | Magenta / cyan / mint | `#1a1b26` |
| 10 | `gruvbox-ember` | Gruvbox Dark | `#282828` |

Every palette is tuned to sit correctly on dark terminal backgrounds — Dracula
(`#282a36`), Catppuccin Mocha (`#1e1e2e`) / Macchiato (`#24273a`) and Nord (`#2e3440`).
The text inside each chip uses that palette's own base colour so the chips read as native
to the theme rather than pasted on.

---

## Prompt layout

```
 …/github/starship-theme   main ?1   🐍 v3.12.1   1.2s
❯
```

* **path** — truncated to the last 3 components (`truncate_to_repo = false`, so it behaves
  the same inside and outside a repo)
* **git** — branch pill, plus plain-coloured status text that appears *only* when the tree
  is dirty
* **languages** — `c`, `rust`, `golang`, `nodejs`, `python`; each renders its own pill only
  when detected
* **cmd_duration** — dim text, shown after 1s
* **character** — `❯`, green normally, red on a failed command

Each pill carries both caps, so an absent segment never leaves a dangling half-chip behind.

---

## Install

```bash
git clone https://github.com/Aviksaikat/starship-theme.git
cd starship-theme
./install.sh
```

Symlinks every `themes/*.toml` into `~/.config/starship/`. Re-running is safe (existing
links are reported, real files are never overwritten). To undo:

```bash
./install.sh --uninstall     # removes only links pointing back into this repo
```

Use a different destination with `STARSHIP_DIR=/some/path ./install.sh`.

### Picking one up

Any of the usual ways works. For example, a specific theme:

```sh
export STARSHIP_CONFIG=~/.config/starship/midnight-bloom.toml
```

Or rotate randomly on every new shell:

```sh
export STARSHIP_CONFIG=$(ls $HOME/.config/starship/*.toml | shuf -n1)
```

Since `install.sh` drops the files into `~/.config/starship/`, a setup like the second one
picks the new themes up automatically — no further config needed.

---

## Preview

`tools/render_html.py` renders the **real** `starship prompt` output of every theme into a
single page (convert ANSI → HTML), so what you see is what Starship actually emits:

```bash
python3 tools/render_html.py     # -> docs/preview.html
open docs/preview.html
```

---

## Development

The `.toml` files are generated, not hand-edited:

```bash
python3 tools/generate.py    # regenerate themes/ from the template
python3 tools/verify.py      # assert every theme renders styled pills
```

`tools/verify.py` checks each theme across four scenarios (dirty repo, clean repo,
non-git directory, Python project) and asserts: no config parse errors, chip backgrounds
present, both caps painted in the right colour, no stray powerline arrows, and that a
clean repo produces no empty git-status pill.

### Gotchas worth knowing

Two Starship behaviours cost real debugging time and are baked into `generate.py`:

1. **Palette keys must be lowercase.** An uppercase key such as `BASE` does not resolve —
   and worse, the failed lookup silently strips the styling from the entire styled group
   it appears in, so your chip renders as unstyled text with no error message.
2. **The cap glyph must live inside the styled group.** `[<cap>](fg:color)` paints the cap;
   `<cap>[](fg:color)` leaves it in the terminal's default colour.

Also note that a segment wrapped in a plain string (not a conditional group) will still
render its literal spaces when empty — which is how you end up with a hollow pill. The
git status here is wrapped in `( ... )` so a clean tree emits nothing at all.

---

## Structure

```
starship-theme/
├── themes/                  # 10 generated .toml themes
├── tools/
│   ├── generate.py          # template -> themes/
│   ├── verify.py            # render assertions (4 scenarios x 10 themes)
│   └── render_html.py       # real output -> docs/preview.html
├── docs/
│   ├── preview.html         # generated visual preview
│   └── plans/               # design doc + implementation plan
├── install.sh
└── README.md
```
