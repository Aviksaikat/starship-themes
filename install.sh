#!/usr/bin/env bash
# install.sh — symlink all themes into ~/.config/starship/
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.config/starship"

mkdir -p "${TARGET_DIR}"

count=0
for src in "${REPO_DIR}/themes/"*.toml; do
    name="$(basename "${src}")"
    dest="${TARGET_DIR}/${name}"

    if [[ -L "${dest}" ]]; then
        echo "Skipped (already linked): ${name}"
        continue
    fi

    ln -s "${src}" "${dest}"
    echo "Installed: ${name}"
    (( count++ )) || true
done

echo ""
echo "Done — ${count} theme(s) installed to ${TARGET_DIR}"
