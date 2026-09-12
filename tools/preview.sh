#!/usr/bin/env zsh
# preview.sh — live-preview all themes. Run in zsh: zsh tools/preview.sh
# Press Enter to advance, Ctrl-C to stop

REPO="${0:A:h:h}"
THEMES_DIR="$REPO/themes"

themes=("$THEMES_DIR"/*.toml)
total=${#themes[@]}
i=0

for toml in "${themes[@]}"; do
  name="${toml:t:r}"
  i=$(( i + 1 ))

  export STARSHIP_CONFIG="$toml"
  clear
  print -P "%B%F{cyan}[$i/$total] Theme: $name%f%b\n"

  # print -P renders zsh %{...%} prompt escapes as actual ANSI colors
  print -P "$(STARSHIP_LOG=error starship prompt 2>/dev/null)"
  echo
  # Also show error-state prompt (red ❯)
  print -P "$(STARSHIP_LOG=error starship prompt --status=1 2>/dev/null)"
  echo

  print -P "%F{240}--- press Enter for next, Ctrl-C to stop ---%f "
  read -r || break
done

print -P "\n%B%F{green}All $total themes previewed.%f%b\n"
