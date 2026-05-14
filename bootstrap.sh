#!/bin/sh
# bootstrap.sh — one-command setup for a freshly cloned/extracted DAI v1.0
#
# Run from the repo root, once, after cloning or extracting:
#   ./bootstrap.sh
#
# What it does:
#   1. Verifies prerequisites (python3, git; optionally pdftotext for PDF ingest)
#   2. Generates memory/session-context.md (the file Codex reads at session start)
#   3. Generates memory/skills-catalog.md (one-line-per-skill index)
#   4. If this is a git repo, installs the pre-commit hooks; if not, offers to init
#   5. Prints the exact ~/.codex/config.toml block to paste, with the absolute
#      workspace path already substituted
#   6. Prints the recommended FIRST PROMPT to send Codex to verify wiring works
#
# Idempotent: safe to run multiple times. Won't overwrite an existing git history.

set -eu

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# Sanity check we're at the workspace root
if [ ! -f "LAUNCHER.md" ] || [ ! -d "core" ] || [ ! -d "memory" ]; then
    echo "ERROR: bootstrap.sh must run from the workspace root" >&2
    echo "(expected LAUNCHER.md, core/, memory/ in the current directory)" >&2
    exit 1
fi

cat <<HEADER
==========================================
  DAI v1.0 — Bootstrap
  Workspace: $ROOT
==========================================

HEADER

# ----- 1/5 Prerequisites -----
echo "[1/5] Checking prerequisites..."
MISSING=""
for tool in python3 git; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        MISSING="$MISSING $tool"
    fi
done
if [ -n "$MISSING" ]; then
    echo "  MISSING required tools:$MISSING" >&2
    echo "  Install them and re-run." >&2
    exit 1
fi
echo "  python3: $(command -v python3)"
echo "  git:     $(command -v git)"
if command -v pdftotext >/dev/null 2>&1; then
    echo "  pdftotext: $(command -v pdftotext)  (PDF ingest enabled)"
else
    echo "  pdftotext: not installed  (bin/dai-knowledge will skip PDFs; install poppler-utils to enable)"
fi
echo ""

# ----- 2/5 Synthesized session context -----
echo "[2/5] Generating memory/session-context.md..."
if [ -x "tools/scripts/build_session_context.sh" ]; then
    tools/scripts/build_session_context.sh
else
    echo "  ERROR: tools/scripts/build_session_context.sh missing or not executable" >&2
    exit 1
fi
echo ""

# ----- 3/5 Skills catalog -----
echo "[3/5] Generating memory/skills-catalog.md..."
if [ -x "tools/scripts/skills_index.sh" ]; then
    tools/scripts/skills_index.sh
else
    echo "  (skills_index.sh not present; skipping)"
fi
echo ""

# ----- 4/5 Git + pre-commit hooks -----
echo "[4/5] Git state + pre-commit hooks..."
IS_GIT_REPO=0
if [ -d ".git" ] || git rev-parse --git-dir >/dev/null 2>&1; then
    IS_GIT_REPO=1
fi

if [ "$IS_GIT_REPO" -eq 1 ]; then
    echo "  Repo is a git repository. Installing hooks..."
    tools/scripts/install_git_hooks.sh
else
    echo "  Not a git repository yet."
    printf "  Initialize git here and make an initial commit? [y/N] "
    if [ ! -t 0 ]; then
        # No interactive stdin (e.g., piped install). Skip rather than hang.
        echo ""
        echo "  Non-interactive stdin detected — skipping git init."
        echo "  Run 'git init && tools/scripts/install_git_hooks.sh' manually when ready."
    else
        read -r answer
        case "$answer" in
            y|Y|yes|YES)
                git init -q -b main
                git add .
                # Use simple commit msg; user can amend later
                git -c user.name="DAI v1.0" -c user.email="bootstrap@local" \
                    commit -q -m "Initial commit — DAI v1.0 bootstrap" \
                    || echo "  (commit may have failed; check git status)"
                git tag v1.0.0 2>/dev/null || true
                tools/scripts/install_git_hooks.sh
                ;;
            *)
                echo "  Skipping. To enable hooks later: 'git init && tools/scripts/install_git_hooks.sh'"
                ;;
        esac
    fi
fi
echo ""

# ----- 5/5 Print Codex wiring + first prompt -----
echo "[5/5] Codex wiring."
echo ""
echo "RECOMMENDED — run the safe wiring helper (TOML-aware, makes a backup):"
echo ""
echo "    tools/scripts/install-codex-config.py"
echo ""
echo "    Flags: --dry-run | --force | --workspace PATH | --config PATH"
echo "    See core/CODEX_INTEGRATION.md Step 2 + Step 2.5 for why this matters."
echo ""
echo "------------------------------------------------------"
echo ""
echo "MANUAL PATH (only if Python 3.11+ is unavailable) —"
echo "Paste the block below into ~/.codex/config.toml"
echo "AT THE TOP OF THE FILE, BEFORE ANY [section] HEADER."
echo ""
echo "Use nano/vim/VS Code — NOT TextEdit (smart-quote corruption is a known footgun)."
echo "See core/CODEX_INTEGRATION.md Step 2.5 for the four pitfalls + recovery path."
echo ""
echo "----------------- BEGIN config.toml -----------------"
cat <<TOML
developer_instructions = """
This workspace is at $ROOT.

At the start of every session, read $ROOT/memory/session-context.md.
That file is the synthesized startup context: constitution, algorithm, ISC
doctrine, identity, current focus, decision rules, and the skills catalog.

For any non-trivial work (multi-file, ambiguous, or touching core/, memory/,
or projects/{name}/), follow core/ALGORITHM.md — create a WORK note at
memory/work/{slug}.md and run the six phases (Observe, Think, Plan,
Execute, Verify, Learn).

For acceptance criteria, follow core/ISC.md — every criterion is one binary
tool probe; tool-verified evidence required before marking [x].

If asked about an available skill, check skills/skills-map.md.

Keep higher-priority system instructions in force. Use this workspace as
added scaffolding, not as a replacement for Codex behavior.
"""

[projects."$ROOT"]
trust_level = "trusted"
TOML
echo "------------------ END config.toml ------------------"
echo ""
echo "Step B — Start Codex from this directory, then paste this as your FIRST prompt:"
echo ""
echo "  > What's in memory/session-context.md? Summarize what this workspace"
echo "    is and what rules I'm operating under."
echo ""
echo "If Codex describes the constitution + Algorithm + ISC + verification doctrine"
echo "+ tiering + identity, the wiring works. If Codex says 'I don't see that file',"
echo "the path in config.toml is wrong — re-check the block above."
echo ""
echo "=========================================="
echo "  Bootstrap complete."
echo "=========================================="
