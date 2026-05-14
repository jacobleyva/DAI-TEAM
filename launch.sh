#!/bin/sh

set -eu

cd "$(dirname "$0")"

printf '%s\n' "Workspace: $(pwd)"
printf '%s\n' ""
printf '%s\n' "Start Codex from this directory, then read in this order:"
printf '%s\n' "1. LAUNCHER.md"
printf '%s\n' "2. WELCOME.md"
printf '%s\n' "3. START_HERE.md"
printf '%s\n' "4. dai-overview.md"
printf '%s\n' "5. active-work-map.md"
printf '%s\n' "6. core/constitution.md"
printf '%s\n' "7. memory/identity.md"
printf '%s\n' "8. memory/current-focus.md"
