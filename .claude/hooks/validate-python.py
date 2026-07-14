#!/usr/bin/env python3
"""PostToolUse(Edit|Write) hook: format + lint edited Python files with ruff.

Non-blocking by design — always exits 0. When an edited file is a `.py` under the project,
runs `uvx ruff format` then `uvx ruff check --fix` so style stays consistent without a manual
step. ruff is run via `uvx` (ephemeral tool run) because it is NOT a project dependency; if
`uvx`/ruff isn't available it quietly no-ops, and it prints the "applied" line ONLY when ruff
actually ran — so a missing tool never reports a false success (the bug this replaced).

Note: `ruff check --fix` exits 1 when fixable-but-unfixed lint remains — a normal result, not a
hook failure — so only OTHER non-zero codes count as "ruff couldn't run". For non-Python
projects, remove this hook from settings.json.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    file_path = payload.get("tool_input", {}).get("file_path", "")
    if not file_path or not file_path.endswith(".py"):
        return 0

    path = Path(file_path)
    if not path.is_file():
        return 0

    project_dir = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or "."

    for cmd in (["format", str(path)], ["check", "--fix", str(path)]):
        try:
            proc = subprocess.run(
                ["uvx", "ruff", *cmd],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return 0  # uvx unavailable or slow — non-blocking no-op

        # `ruff check --fix` exits 1 when unfixable lint remains (a normal result); any other
        # non-zero means ruff never actually ran (uvx failed, bad config, …) — don't claim success.
        ran = proc.returncode == 0 or (cmd[0] == "check" and proc.returncode == 1)
        if not ran:
            sys.stderr.write(
                f"[validate-python] ruff {cmd[0]} could not run (exit {proc.returncode}); skipped\n"
            )
            return 0

    print(f"[validate-python] ruff format + check --fix applied to {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
