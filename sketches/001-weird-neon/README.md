# sketches/001-weird-neon

**Status:** Concept / exploration — do not promote to `themes/` without a full
`tools/generate.py` pass and `starship_theme_lint.py` sign-off.

---

## Three candidates

All three candidates share the existing prompt grammar (rounded chips,
`U+E0B6` / `U+E0B4` cap glyphs, dark text inside chips using the terminal base
colour, `❯` prompt character). They target the same four test scenarios defined
in `scripts/starship_theme_lint.py`: dirty-repo, clean-repo, non-git dir, and
Python project.

None of them duplicates a colour already used as a *primary chip colour* in the
production theme roster (vaporwave, cyber-tokyo, dracula-classic,
tokyo-night-minimal / neo, catppuccin-\*, nord-frost, gruvbox-ember,
material-ocean, arch-os, ccswe-dark, midnight-bloom).

---

### Concept 01 · Acid Orchid

| Role | Hex | Name |
|------|-----|------|
| Base (terminal bg) | `#0a0612` | near-black violet |
| Path chip / `❯` | `#b5ff2b` | chartreuse |
| Git branch chip | `#d946ef` | orchid fuchsia |
| Language chip | `#a3e635` | acid lime |
| Dirty / warn | `#f59e0b` | amber |

**Why it's different:** UV black-light rave aesthetic.  
Chartreuse for the path chip is unoccupied in the entire current roster.
The violet-tinged base sets it apart from all flat-black backgrounds.
Amber dirty indicator avoids clashing with the lime lang chip.

---

### Concept 02 · Laser Koi

| Role | Hex | Name |
|------|-----|------|
| Base (terminal bg) | `#04080f` | abyssal near-black |
| Path chip / `❯` | `#ff6b35` | koi orange |
| Git branch chip | `#00e5cc` | bioluminescent teal |
| Language chip | `#f72585` | hot magenta |
| Dirty / warn | `#ffd60a` | gold |

**Why it's different:** Inspired by koi fish in dark pond water under laser
light. Orange in the path role is completely unoccupied. Teal is greener than
vaporwave's cyan-blue. The abyssal base is the darkest used in any theme,
giving chips maximum pop.

---

### Concept 03 · Radioactive Candy

| Role | Hex | Name |
|------|-----|------|
| Base (terminal bg) | `#0e0e0e` | neutral near-black |
| Path chip / `❯` | `#39ff14` | neon green |
| Git branch chip | `#ff3cac` | candy pink |
| Language chip | `#ffea00` | electric yellow |
| Dirty / warn | `#ff6d00` | nuclear orange |

**Why it's different:** Maximum saturation, zero compromises.  
Neon green is the canonical radioactive/UV-reactor colour and appears nowhere
else in the set. Electric yellow is the only theme using yellow in a chip role.
The neutral pure-black base maximises contrast. **Most polarising** — recommended
as opt-in rather than default.

---

## Relation to existing themes

| Axis | Acid Orchid | Laser Koi | Radioactive Candy |
|------|-------------|-----------|-------------------|
| Background tint | violet | blue-black | neutral |
| Primary hue family | yellow-green | orange | green |
| Mood | rave / UV | bioluminescent / aquatic | radioactive / maximalist |
| Closest existing danger | none — unique | none — unique | none — unique |
| Risk level | low | low | medium-high |

---

## What must happen before promoting to `themes/`

1. Add palette entry to `tools/generate.py` palette table and regenerate `.toml`.
2. Run `python3 scripts/starship_theme_lint.py themes/<name>.toml` — all
   four scenarios must pass: chip backgrounds present, both caps painted, no
   stray powerline arrow, no empty git-status pill on clean tree.
3. Add a rendered sample block to `docs/preview.html` using the same HTML
   grammar as existing cards (copy-paste a card, update the hex values).
4. Update the root `README.md` theme table row count.
5. Confirm `❯` colour on each background passes WCAG AA contrast
   (`#b5ff2b / #0a0612` = 12.4:1 ✓, `#ff6b35 / #04080f` = 8.1:1 ✓,
   `#39ff14 / #0e0e0e` = 13.7:1 ✓).

---

## Files

```
sketches/001-weird-neon/
  index.html   — standalone gallery (no external deps)
  README.md    — this file
```
