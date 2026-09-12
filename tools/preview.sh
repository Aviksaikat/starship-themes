#!/usr/bin/env zsh
# preview.sh — render & test themes from this repo.
#
# Usage:
#   zsh tools/preview.sh                     # step through all themes (Enter = next, q = quit)
#   zsh tools/preview.sh --all               # dump every theme, no paging
#   zsh tools/preview.sh nord-frost          # render one theme
#   zsh tools/preview.sh pl10k-nord pastel-tokyo gruvbox-neon   # render several
#
# Must run in zsh with a Nerd Font terminal (kitty/ghostty/wezterm).
# Uses `print -P` to expand the %{...%} escapes starship emits for zsh.
# (Pipe the prompt into `print -P` and you get nothing — it takes arguments,
#  not stdin.)

setopt no_nomatch 2>/dev/null

REPO="${0:A:h:h}"
THEMES_DIR="$REPO/themes"

local -a themes
local mode

if [[ "$1" == "--all" ]]; then
  themes=("$THEMES_DIR"/*.toml)
  mode=all
elif (( $# > 0 )); then
  themes=()
  local n
  for n in "$@"; do themes+=("$THEMES_DIR/$n.toml"); done
  mode=given
else
  themes=("$THEMES_DIR"/*.toml)
  mode=step
fi

render() {
  local toml="$1" name="${1:t:r}" out
  printf '\n\033[1;36m── %s \033[0m\033[2m(%s)\033[0m\n' "$name" "$toml"
  if [[ ! -f "$toml" ]]; then
    printf '\033[1;31m   no such theme\033[0m\n'
    return
  fi
  out="$( cd "$REPO" && STARSHIP_CONFIG="$toml" STARSHIP_LOG=error starship prompt 2>/dev/null )"
  print -P -- "$out"
  printf '\n'
}

if [[ "$mode" == "all" || "$mode" == "given" ]]; then
  for toml in "${themes[@]}"; do render "$toml"; done
  exit 0
fi

local total=${#themes} i=0
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
