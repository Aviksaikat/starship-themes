# sketches/001-cold-technical

**Design exploration only.** Disposable mockup — no TOML generated.
Do not merge into `themes/`. See `sketches/001-cold-technical/index.html` to preview.

---

## Three candidate concepts

### 1 · Cryogenic

| Role    | Colour    |
|---------|-----------|
| path    | `#9dcfea` |
| git     | `#6db3ce` |
| lang    | `#c5e8f6` |
| warn    | `#f5c842` |
| cursor  | `#5ab0d0` |

**Separator:** `U+E0B0` `` — the standard Powerline right-pointing chevron.
Acts as a gradient/taper tail: each chevron carries the previous chip's
background as its foreground, reading as a descending temperature ramp that
flows cooler with every step.

**Rationale:** Descending blue luminance from near-white frost to deep slate.
Each chip is temperature-mapped from 0 K upward — evoking superconductor readouts
and laboratory cryostats. Deliberately stays in a single blue-teal family, so
chips read as a unified cold system rather than a palette grab-bag.

**Distinguishes from existing themes:** Nord (warm blue/arctic green mix),
Catppuccin (lavender + teal), Tokyo Night (purple + cyan) all break into two or
more hue families. Cryogenic commits to one descending hue ramp.

---

### 2 · Circuit Glacier

| Role    | Colour    |
|---------|-----------|
| path    | `#00cf9a` |
| git     | `#0097c6` |
| lang    | `#00a87e` |
| warn    | `#ffa020` |
| cursor  | `#00cf9a` |

**Separator:** `U+E0C6` `` — the Powerline Extra pixel/columnar fade.
Its columnar, bit-level dissolve mirrors the precision of PCB copper traces
dissolving into the next conductor layer.

**Rationale:** PCB-trace mint-green and electric blue on near-void canvas.
Clean-room aesthetics of silicon wafers and solder pads — without the neon chaos
of cyberpunk. The amber warning channel is the single thermal anomaly in an
otherwise isothermal circuit-board colour scheme.

**Distinguishes from existing themes:** Tokyo Night Neo/Cyber Tokyo both
rely on neon-magenta or hot-pink accents; Circuit Glacier's accent is amber, and
the primary palette is strictly mint ↔ teal-blue rather than purple ↔ cyan.

---

### 3 · Event Horizon

| Role    | Colour    |
|---------|-----------|
| path    | `#d0d0d0` |
| git     | `#c22222` |
| lang    | `#787878` |
| warn    | `#ff5555` |
| cursor  | `#e8e8e8` |

**Separator:** `U+E0B8` `` — the Powerline Extra angled diagonal cut
(bottom-left fill). The hard geometric slice evokes the boundary discontinuity
at an event horizon, where space-time geometry is severed abruptly rather than
tapered.

**Rationale:** Near-monochrome — cold neutral grey and near-white — with a single
crimson warning channel. Inspired by physics-lab telemetry displays where signal
isolation demands maximum density and zero chromatic noise. The git chip alone
carries colour, so any branch-state deviation is instantly salient.

**Distinguishes from existing themes:** All current themes use at least two
distinct accent hues. Event Horizon is effectively grayscale + red only, which
no existing entry approaches.

---

## Segment grammar used in the mockup

All three themes use **contiguous solid-colour Powerline segments** — no rounded
caps, no inter-chip whitespace.

### Powerline Extra Symbols roles

| Glyph | Code point | Role in grammar |
|-------|-----------|-----------------|
| `` | `U+E0B0` | Standard right chevron — taper/gradient tail (Cryogenic) |
| `` | `U+E0C6` | Pixel / columnar fade (Circuit Glacier) |
| `` | `U+E0B8` | Angled diagonal cut — bottom-left fill (Event Horizon) |

> **Rejected:** `U+E0B4` `` and `U+E0B6` `` (rounded right/left caps) are
> never used — they break the contiguous segment flow.

### Separator rule

```
BODY_n   =  <span fg=chipText  bg=chipBg_n>  content  </span>
SEP_n→m  =  <span fg=chipBg_n bg=chipBg_m>  GLYPH    </span>
TAIL_sep =  <span fg=chipBg_last bg=termBg>  GLYPH    </span>
```

- **Separator fg** = current (left) segment's background — the glyph's left
  face blends seamlessly with the segment body it exits.
- **Separator bg** = next (right) segment's background — the glyph's right
  face starts the incoming segment colour.
- **Terminal tail** = separator with fg=last chip bg, bg=terminal canvas — the
  final glyph transitions from the prompt back to the raw terminal background.
- **No leading cap.** The first segment starts as a rectangular solid block
  flush with the left edge.
- **No HTML whitespace text nodes** between segment `<span>` elements.

### Apple glyph

The macOS  glyph `󰀵` (U+F0035, `nf-md-apple`) is always rendered **inside**
the body background span, never detached. The directory chip is
` 󰀵 …/git_projects/github/starship-theme `.

In JavaScript the code point must be written as `"\u{F0035}"` (ES2015 brace
notation for code points above U+FFFF) — the four-digit form `"\uF0035"` is a
syntax error for supplementary plane characters.

---

## Files

| File         | Purpose |
|--------------|---------|
| `index.html` | Standalone gallery — three themes × three prompt scenarios × three background toggles |
| `README.md`  | This file |
