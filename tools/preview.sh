#!/usr/bin/env zsh
# preview.sh — render & test every theme in this repo, one at a time.
#
# Usage:
#   zsh tools/preview.sh              # step through all themes (Enter = next)
#   zsh tools/preview.sh saffron-grove  # render just one theme
#   zsh tools/preview.sh --all         # dump every theme, no paging
#
# Must run in zsh with a Nerd Font terminal (kitty/ghostty/wezterm).
# Uses `print -P` to expand the %{...%} escapes starship emits for zsh.

setopt no_nomatch 2>/dev/null

REPO="${0:A:h:h}"
THEMES_DIR="$REPO/themes"

if [[ $# -gt 0 && "$1" != "--all" ]]; then
  themes=("$THEMES_DIR/$1.toml")
else
  themes=("$THEMES_DIR"/*.toml)
fi

render() {
  local toml="$1" name="${1:t:r}" out
  printf '\n\033[1;36m── %s \033[0m\033[2m(%s)\033[0m\n' "$name" "$toml"
  out="$( cd "$REPO" && STARSHIP_CONFIG="$toml" STARSHIP_LOG=error starship prompt 2>/dev/null )"
  print -P -- "$out"
  printf '\n'
}

if [[ "$1" == "--all" ]]; then
  for toml in "${themes[@]}"; do render "$toml"; done
  exit 0
fi

if [[ $# -gt 0 ]]; then
  render "${themes[1]}"
  exit 0
fi

total=${#themes}
i=0
for toml in "${themes[@]}"; do
  i=$(( i + 1 ))
  clear
  printf '\033[1;33m[%d/%d]\033[0m ' "$i" "$total"
  render "$toml"
  printf '\033[2m── Enter = next · q = quit ──\033[0m '
  read -r ans || break
  [[ "$ans" == "q" ]] && break
done
printf '\n\033[1;32mDone — %d themes.\033[0m\n' "$total"
