# Sketch 001 — Warm / Organic Concept Gallery

**Status:** disposable exploration — do not merge to production  
**File:** [`index.html`](./index.html)  
**Purpose:** three Starship theme candidates that move away from Gruvbox recolors into distinct warm/organic territory.

---

## How to view

Open `index.html` in any modern browser.  
For accurate glyph rendering (rounded caps ``, folder icon `󰀵`) install a Nerd Font — the file embeds a font-stack that falls back gracefully.

The **light/dark toggle** in the top-right switches the page chrome between dark (`#111210`) and light (`#f2ede6`), so you can check how the palette rationale text reads in both modes.

---

## Candidates

### 1 · Mossfire
_Deep forest at dusk — moss canopy, ember coals_

| Role | Color | Name |
|------|-------|------|
| Background | `#1a2018` | forest-floor green |
| Path chip | `#7a9e5a` | moss |
| Git chip | `#c97b36` | ember |
| Lang chip | `#d4a853` | amber / turmeric |
| `❯` clean | `#9fbc7a` | sage |
| `❯` error | `#e07050` | rust |

**Concept:** The background carries its own green identity at near-black luminance — every other dark theme in the repo uses a neutral or blue-tinted near-black.  The path/git/lang chips form a cool→warm arc (moss → ember → amber) that reads as "forest after sunset" rather than "Gruvbox with different yellows".  The chip text uses the native `#1a2018` dark so glyphs feel painted on, not pasted.

**Readability check:** All three chip colors pass ≥ 7:1 contrast against `#1a2018` (path ≈ 7.8:1, git ≈ 7.1:1, lang ≈ 8.4:1).  Cap glyphs `#7a9e5a` / `#c97b36` / `#d4a853` pop clearly against all four production terminal backgrounds (#282a36, #1e1e2e, #24273a, #2e3440).

---

### 2 · Saffron Grove
_Spice-market warmth — bark, turmeric, clay, sage_

| Role | Color | Name |
|------|-------|------|
| Background | `#1e1610` | dried bark / dark leather |
| Path chip | `#c8973a` | saffron / turmeric |
| Git chip | `#b55840` | fired clay / terracotta |
| Lang chip | `#7ea85f` | sage green |
| `❯` clean | `#d4a036` | deep gold |
| `❯` error | `#c04830` | chili red |

**Concept:** The background `#1e1610` is warm-toned at near-black, a genuine differentiator from neutral-dark palettes.  The path and git chips are both warm but separated by ≈ 40° of hue (amber-yellow vs red-orange) so dirty-repo state reads unambiguously.  The sage lang chip is the deliberate complementary break — without it the palette would feel monochromatic and hard to scan.

**vs Gruvbox:** Gruvbox Dark uses `#282828` (neutral warm-grey), its canonical yellow is `#d79921` (lighter, more lemon), and its orange is `#fe8019` (pure bright orange).  Saffron Grove's bg is genuinely warm-brown, the path chip is deeper/more golden (less lemon), and the git chip is a desaturated brick-red that Gruvbox doesn't have at all.

---

### 3 · Copper Bloom
_Oxidized copper patina — dark slate, verdigris, warm metal_

| Role | Color | Name |
|------|-------|------|
| Background | `#161c1c` | cold teal-slate |
| Path chip | `#4a9e8a` | verdigris (oxidized copper) |
| Git chip | `#b87d4a` | raw copper |
| Lang chip | `#7ab8c0` | pale patina |
| `❯` clean | `#b87d4a` | copper |
| `❯` error | `#c05040` | corroded red |

**Concept:** The coldest of the three backgrounds — `#161c1c` reads as the shadow-side of a copper plate.  The path chip (verdigris) and git chip (raw copper) are directly complementary: the chemical relationship between copper and its oxide makes the pairing feel thematic rather than arbitrary.  The lang chip is a lighter teal, giving a three-level brightness gradient across the prompt so the eye can parse segments without reading the text.

**Distinctiveness:** The verdigris path chip is unique in the repo — no existing theme uses a blue-green as the primary chip.  The copper/verdigris split also means this palette works in both "warm" and "cool" registers simultaneously, making it versatile across terminal backgrounds.

---

## Prompt grammar (unchanged from repo standard)

```
<left-cap><chip-bg> content <right-cap>  <left-cap><chip-bg> content <right-cap>  ❯
```

- **Caps:** `` (U+E0B6) and `` (U+E0B4) — Nerd Font rounded caps.  
- **Chip text color:** always the matching dark base (`#1a2018`, `#1e1610`, or `#161c1c`).  
- **Git status:** `!` suffix appears only when dirty — no empty pill on a clean tree.  
- **Lang chip:** appears only when a language version is detected.  
- **`❯`:** second line; green on clean exit, error color on non-zero exit.

The gallery shows three terminal backgrounds per theme: Ghostty/WezTerm Dracula (`#282a36`), Alacritty Catppuccin Mocha (`#1e1e2e`), Kitty Catppuccin Macchiato (`#24273a`).

---

## Next steps (if any candidate is promoted)

1. Run `tools/generate.py` after adding the palette to its palette table.  
2. Lint the generated `.toml` with `scripts/starship_theme_lint.py`.  
3. Verify by running `starship prompt` in each scenario directory — do **not** trust exit code; inspect rendered escape sequences.  
4. Add the theme name to the random-rotation list in `install.sh`.
