#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"

cd "$REPO_ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "error: not inside a git repository"
  exit 1
fi

branch="$(git branch --show-current)"
if [[ -z "$branch" ]]; then
  echo "error: could not determine current branch"
  exit 1
fi

echo "Repository: $REPO_ROOT"
echo "Branch: $branch"
echo
echo "Current status:"
git status --short
echo

read "commit_message?What commit name do you want for this push? "
if [[ -z "${commit_message// }" ]]; then
  echo "error: commit name cannot be blank"
  exit 1
fi

tracked_and_untracked=("${(@f)$(git ls-files -m -o --exclude-standard)}")
files_to_add=()

for path in "${tracked_and_untracked[@]}"; do
  [[ -z "$path" ]] && continue

  case "$path" in
    *.docx|*.pptx|*.xlsx)
      echo "Skipping binary office file: $path"
      continue
      ;;
  esac

  files_to_add+=("$path")
done

if (( ${#files_to_add[@]} > 0 )); then
  git add -- "${files_to_add[@]}"
fi

if git diff --cached --quiet; then
  echo "No staged changes to commit."
else
  git commit -m "$commit_message"
fi

git push origin "$branch"

echo
echo "Pushed $branch with commit message: $commit_message"
