#!/bin/zsh
set -euo pipefail

ROOT_DIR="${1:-$PWD}"

echo "Codex DAI Phase 1 scaffold detected at: $ROOT_DIR"
echo
echo "Suggested next steps:"
echo "1. Fill in memory/identity.md and memory/preferences.md"
echo "2. Add your active repositories to memory/projects-index.md"
echo "3. Copy project-specific context into each repo under docs/ai/ if useful"
echo "4. Turn one automation spec into a Codex automation"
echo "5. Promote any repeated workflow into a new skill"
