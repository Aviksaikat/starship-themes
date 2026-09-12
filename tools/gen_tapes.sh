#!/usr/bin/env bash
# gen_tapes.sh — generate one VHS tape per theme, record GIF, extract PNG
# Usage: ./tools/gen_tapes.sh [theme_name]  (no arg = all themes)
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
THEMES_DIR="$REPO/themes"
TAPES_DIR="$REPO/tapes"
MEDIA_DIR="$REPO/media"
PNG_DIR="$MEDIA_DIR/png"
mkdir -p "$TAPES_DIR" "$MEDIA_DIR" "$PNG_DIR"

make_tape() {
  local toml="$1"
  local name
  name="$(basename "$toml" .toml)"
  local tape="$TAPES_DIR/${name}.tape"
  local out_gif="$MEDIA_DIR/${name}.gif"
  local out_png="$PNG_DIR/${name}.png"

  cat > "$tape" <<TAPE
Output "$out_gif"

Set Shell "zsh"
Set FontFamily "JetBrainsMono Nerd Font Mono"
Set FontSize 16
Set Width 1200
Set Height 300
Set Theme "Dracula"
Set TypingSpeed 20ms
Set Padding 20

Type "export STARSHIP_CONFIG='$toml' STARSHIP_LOG=error"
Enter
Sleep 200ms

Type 'eval "\$(starship init zsh)"'
Enter
Sleep 500ms

Hide
Type "clear"
Enter
Sleep 300ms
Show

Type "echo '$name'"
Enter
Sleep 600ms
TAPE

  echo "  recording $name ..."
  vhs "$tape" 2>/dev/null
  local total
  total="$(ffprobe -v quiet -select_streams v:0 -count_packets \
    -show_entries stream=nb_read_packets -of csv=p=0 "$out_gif" 2>/dev/null || echo 50)"
  local frame=$(( total > 10 ? total - 10 : total - 1 ))
  ffmpeg -y -i "$out_gif" -vf "select=eq(n\\,$frame)" -frames:v 1 "$out_png" 2>/dev/null
  echo "  png: $out_png"
}

if [[ $# -eq 1 ]]; then
  toml="$THEMES_DIR/$1.toml"
  [[ -f "$toml" ]] || { echo "not found: $toml"; exit 1; }
  make_tape "$toml"
else
  for toml in "$THEMES_DIR"/*.toml; do
    make_tape "$toml"
  done
fi
