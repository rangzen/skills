#!/usr/bin/env bash
# link-context.sh - Symlink personal context files into HOME.
#
# Iterates over context/ and creates ~/FILE -> context/FILE for each file.
# Then adds ~/CLAUDE.md -> ~/AGENTS.md so Claude Code picks up the agent
# instructions without a separate copy.
#
# Safe to run multiple times: existing symlinks and real files are skipped.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTEXT_DIR="$SCRIPT_DIR/../context"

# Create a symlink from src to dst, skipping if dst already exists.
link() {
  local src="$1"
  local dst="$2"

  if [[ -L "$dst" ]]; then
    echo "skip (already linked): $dst"
    return
  fi

  # Leave real files alone - do not overwrite user data.
  if [[ -e "$dst" ]]; then
    echo "skip (file exists, not a symlink): $dst"
    return
  fi

  ln -s "$src" "$dst"
  echo "linked: $dst -> $src"
}

# Link every regular file in context/ to HOME.
for file in "$CONTEXT_DIR"/*; do
  [[ -f "$file" ]] || continue
  name="$(basename "$file")"
  link "$(realpath "$file")" "$HOME/$name"
done

# CLAUDE.md is the entry point Claude Code looks for in HOME.
# Point it at AGENTS.md so there is only one source of truth.
link "$HOME/AGENTS.md" "$HOME/CLAUDE.md"
