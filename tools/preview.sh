#!/usr/bin/env bash
# preview.sh — live-preview all themes in the current shell one by one
# Usage: ./tools/preview.sh
# Press Enter to advance, Ctrl-C to stop
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
THEMES_DIR="$REPO/themes"

themes=()
for f in "$THEMES_DIR"/*.toml; do
  themes+=("$f")
done

total=${#themes[@]}
i=0
for toml in "${themes[@]}"; do
  name="$(basename "$toml" .toml)"
  i=$(( i + 1 ))
  export STARSHIP_CONFIG="$toml"
  clear
  printf "\033[1;36m[%d/%d] Theme: %s\033[0m\n" "$i" "$total" "$name"
  printf "STARSHIP_CONFIG=%s\n\n" "$toml"
  # Force a starship eval so the prompt renders immediately
  eval "$(starship init bash 2>/dev/null)" 2>/dev/null || true
  PS1="$(starship prompt 2>/dev/null)" bash --norc --noprofile -i <<'INNER' 2>/dev/null || true
exit
INNER
  # Print a sample prompt line
  STARSHIP_CONFIG="$toml" starship prompt 2>/dev/null
  printf "\n\033[2m--- press Enter for next, Ctrl-C to stop ---\033[0m "
  read -r || break
done

printf "\n\033[1;32mAll %d themes previewed.\033[0m\n" "$total"
