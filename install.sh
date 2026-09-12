#!/usr/bin/env bash
#
# install.sh — link the themes in this repo into your Starship config dir.
#
#   bash install.sh              # install
#   bash install.sh --uninstall  # remove only the links this repo created
#
# Override the destination with STARSHIP_DIR (default: ~/.config/starship).
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THEME_DIR="${REPO_DIR}/themes"
TARGET_DIR="${STARSHIP_DIR:-${HOME}/.config/starship}"

MODE="install"
[[ "${1:-}" == "--uninstall" ]] && MODE="uninstall"

if [[ ! -d "${THEME_DIR}" ]]; then
    echo "error: no themes/ directory next to install.sh" >&2
    exit 1
fi

mkdir -p "${TARGET_DIR}"

installed=0
skipped=0
removed=0

for src in "${THEME_DIR}"/*.toml; do
    name="$(basename "${src}")"
    dest="${TARGET_DIR}/${name}"

    if [[ "${MODE}" == "uninstall" ]]; then
        # Only remove links that point back into THIS repo.
        if [[ -L "${dest}" && "$(readlink "${dest}")" == "${src}" ]]; then
            rm "${dest}"
            echo "Removed:   ${name}"
            (( removed++ )) || true
        fi
        continue
    fi

    if [[ -L "${dest}" ]]; then
        target="$(readlink "${dest}")"
        if [[ "${target}" == "${src}" ]]; then
            echo "Linked:    ${name} (already present)"
        else
            echo "SKIPPED:   ${name} — already linked to ${target}" >&2
        fi
        (( skipped++ )) || true
        continue
    fi

    if [[ -e "${dest}" ]]; then
        echo "SKIPPED:   ${name} — a real file already exists at ${dest}" >&2
        (( skipped++ )) || true
        continue
    fi

    ln -s "${src}" "${dest}"
    echo "Installed: ${name}"
    (( installed++ )) || true
done

echo
if [[ "${MODE}" == "uninstall" ]]; then
    echo "Done — removed ${removed} link(s) from ${TARGET_DIR}"
else
    echo "Done — ${installed} installed, ${skipped} skipped, into ${TARGET_DIR}"
    echo
    echo "If your shell already does:"
    echo "  export STARSHIP_CONFIG=\$(ls \$HOME/.config/starship/*.toml | shuf -n1)"
    echo "these themes are picked up automatically in new shells."
fi
