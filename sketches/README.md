# sketches/

Disposable design explorations — **do not merge to `themes/`** without
`tools/generate.py` + `scripts/starship_theme_lint.py` sign-off.

## Unified comparison

**[sketches/index.html](./index.html)** — 9 candidates side-by-side, 3 columns,
four terminal-background toggles (Dracula, Catppuccin Mocha/Macchiato, Void),
click-to-shortlist, palette swatches with hex values, rationale, and prompt
samples (dirty repo · clean+Python).

### Chip grammar — contiguous separators (no rounded caps)

All nine themes use **contiguous solid segments** joined by distinct powerline
separator glyphs. Rounded caps U+E0B4 / U+E0B6 are explicitly excluded.

| Theme | Separator glyph | Codepoint |
|---|---|---|
| Cryogenic | `>>>` triple right-arrow | U+E0B0 ×3 |
| Circuit Glacier | flame | U+E0C6 |
| Event Horizon | lower-left triangle | U+E0B8 |
| Mossfire | honeycomb | U+E0C0 |
| Saffron Grove | upper-left triangle | U+E0BC |
| Copper Bloom | pixel blocks | U+E0CE |
| Acid Orchid | flame | U+E0C6 |
| Laser Koi | `>>>` triple right-arrow | U+E0B0 ×3 |
| Radioactive Candy | pixel blocks | U+E0CE |

**Segment anatomy:**
- Segment body: `bg=chipColour`, `color=terminalBg` (dark text)
- Inter-segment separator: `color=currentChipColour bg=nextChipColour GLYPH`
- Tail separator: `color=lastChipColour bg=terminalBg GLYPH` (bleeds to canvas)
- No leading cap; directory chip starts with solid segment + `󰀵` (U+F0035)
- No inter-module spacer spans

## Directories

| Directory | Direction | Candidates |
|-----------|-----------|------------|
| [001-cold-technical/](./001-cold-technical/) | Cold / Technical | Cryogenic, Circuit Glacier, Event Horizon |
| [001-warm-organic/](./001-warm-organic/) | Warm / Organic | Mossfire, Saffron Grove, Copper Bloom |
| [001-weird-neon/](./001-weird-neon/) | Weird / Neon | Acid Orchid, Laser Koi, Radioactive Candy |
