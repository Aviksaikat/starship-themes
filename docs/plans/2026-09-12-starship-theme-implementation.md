# Implementation Plan — starship-theme

Date: 2026-09-12
Design: [2026-09-12-starship-theme-design.md](./2026-09-12-starship-theme-design.md)

---

## Phase 1 — Scaffold

- [x] T1 `git clone` to `~/git_projects/github/starship-theme`
- [x] T2 `themes/`, `tools/`, `docs/plans/` directories
- [x] T3 `.gitignore` (macOS, editor, Python noise)

## Phase 2 — Theme template

- [x] T4 Decide layout: single line of rounded pills + dim `cmd_duration` + `❯`
- [x] T5 Confirm terminal backgrounds to render against (Dracula, Catppuccin
      Mocha/Macchiato, Nord) so chip colours are tuned to real environments
- [x] T6 Pick 10 palettes, 6 pure and 4 cross-family blends
- [x] T7 Fix `truncate_to_repo = false` so "last 3 components" is consistent

## Phase 3 — Generation & verification

- [x] T8 Write `tools/generate.py` — one template, 10 palettes
- [x] T9 Write `tools/verify.py` — 10 themes x 4 scenarios

Verification matrix per theme:

| Scenario      | Asserts                                                        |
|---------------|----------------------------------------------------------------|
| dirty repo    | path pill + git pill backgrounds, caps painted, status shown    |
| clean repo    | no empty git-status pill, no stray cap                          |
| non-git dir   | path pill only, correct path, no dangling caps                  |
| python project| language pill background present                                |

Global assertions: no config parse error on stderr, no powerline arrow (`U+E0B0`)
anywhere, palette keys all lowercase.

- [x] T10 All 40 scenario checks pass
- [x] T11 Visual confirmation via `tools/render_html.py` + screenshot

## Phase 4 — Packaging

- [x] T12 `install.sh` with `--uninstall` and `STARSHIP_DIR` override
- [x] T13 Smoke-test installer in a sandbox `HOME` (install, idempotent re-run,
      uninstall)
- [x] T14 `README.md`

## Phase 5 — Ship

- [x] T15 Commit and push to `github.com/Aviksaikat/starship-theme`
- [x] T16 Run `install.sh` against the real `~/.config/starship/` so the themes
      join the existing random rotation

---

## Defects found and fixed during implementation

| # | Defect | Cause | Fix |
|---|--------|-------|-----|
| 1 | All 10 themes rejected; Starship silently fell back to its default prompt | `'...\\($virtualenv\\)...'` written into a TOML **basic** string — `\(` is not a legal escape | Dropped the virtualenv fragment; format uses only valid escapes |
| 2 | Chips rendered with no background at all | Palette key `BASE` is uppercase — Starship does not resolve it, and the failed lookup strips the styling from the whole group it appears in | All palette keys lowercased (`base`) |
| 3 | Caps drawn in the terminal's default colour | Cap glyph placed outside the styled group: `<cap>[](fg:...)` | Glyph moved inside: `[<cap>](fg:...)` |
| 4 | Empty pink pill in a clean repo | Literal spaces inside a styled group still render when the variables are empty | git status wrapped in a conditional group `( ... )` |
| 5 | Path changed depending on repo membership | Default `truncate_to_repo = true` | Set `truncate_to_repo = false` |
| 6 | Pills appeared unstyled in the preview page only | Bug in the preview tool's ANSI→HTML converter: it merged differently-styled runs into one `<span>` | Converter closes and reopens a span at every escape |

Defects 1–5 were in the shipped themes (found by `tools/verify.py` and by inspecting
raw escape sequences). Defect 6 was in `tools/render_html.py`, caught by looking at the
rendered page.
