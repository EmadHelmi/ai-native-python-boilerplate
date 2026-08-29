#!/usr/bin/env python3

# Author: Emad Helmi <s.emad.helmi@gmail.com> (@emad.helmi)

"""Require explicit approval for selected high-impact shell commands.

This hook is a workflow safety net for Cursor's beforeShellExecution
event. It complements AGENTS.md; it does not replace the repository's
human-agent working agreement.

The policy is intentionally narrow:

- ordinary and read-only commands are allowed;
- known state-changing or high-impact commands require approval;
- no command is permanently denied by the baseline policy.

This is not intended to be a complete shell security sandbox.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class ApprovalRule:
    """A command pattern that requires explicit user approval."""

    pattern: re.Pattern[str]
    reason: str


def compile_pattern(pattern: str) -> re.Pattern[str]:
    """Compile a case-insensitive command-matching pattern."""

    return re.compile(pattern, re.IGNORECASE)


APPROVAL_RULES = (
    # -----------------------------------------------------------------
    # Git mutations
    # -----------------------------------------------------------------
    ApprovalRule(
        compile_pattern(
            r"\bgit\b[^\n;&|]*\b"
            r"(?:add|commit|push|pull|merge|rebase|reset|revert|"
            r"cherry-pick|tag|stash|switch|checkout|restore|clean|"
            r"rm|mv)\b"
        ),
        "This command changes Git or working-tree state.",
    ),
    ApprovalRule(
        compile_pattern(
            r"\bgit\s+branch\s+"
            r"(?:-[^\s]*[dDmM][^\s]*\b|--delete\b|--move\b)"
        ),
        "This command modifies or deletes a Git branch.",
    ),
    ApprovalRule(
        compile_pattern(
            r"\bgit\s+branch\s+(?!"
            r"--show-current\b|--list\b|-l\b|-a\b|-r\b|-v\b|-vv\b"
            r")[A-Za-z0-9._/-]+"
        ),
        "This command may create or modify a Git branch.",
    ),
    # -----------------------------------------------------------------
    # Python dependency / environment mutations
    # -----------------------------------------------------------------
    ApprovalRule(
        compile_pattern(r"\buv\s+(?:add|remove|sync|lock)\b"),
        "This command changes project dependencies, the lock file, "
        "or the managed environment.",
    ),
    ApprovalRule(
        compile_pattern(
            r"\b(?:python(?:3(?:\.\d+)*)?\s+-m\s+)?"
            r"pip\s+(?:install|uninstall)\b"
        ),
        "This command changes installed Python dependencies.",
    ),
    ApprovalRule(
        compile_pattern(r"\bpoetry\s+(?:add|remove|update|lock|install)\b"),
        "This command changes project dependencies, the lock file, "
        "or the managed environment.",
    ),
    # -----------------------------------------------------------------
    # High-impact filesystem / operating-system mutations
    # -----------------------------------------------------------------
    ApprovalRule(
        compile_pattern(
            r"(^|[;&|]\s*)"
            r"(?:sudo\s+)?rm\s+"
            r"(?:-[^\s]*r[^\s]*\s+|--recursive\b)"
        ),
        "This command recursively removes filesystem content.",
    ),
    ApprovalRule(
        compile_pattern(r"(^|[;&|]\s*)sudo(?:\s|$)"),
        "This command requests elevated operating-system privileges.",
    ),
    ApprovalRule(
        compile_pattern(
            r"\b(?:apt|apt-get)\s+"
            r"(?:install|remove|purge|upgrade|dist-upgrade|full-upgrade)\b"
        ),
        "This command changes operating-system packages.",
    ),
    # -----------------------------------------------------------------
    # High-impact Docker mutations
    # -----------------------------------------------------------------
    ApprovalRule(
        compile_pattern(r"\bdocker\s+system\s+prune\b"),
        "This command removes Docker resources.",
    ),
    ApprovalRule(
        compile_pattern(
            r"\bdocker\s+(?:volume|network)\s+"
            r"(?:rm|prune)\b"
        ),
        "This command removes Docker resources.",
    ),
    ApprovalRule(
        compile_pattern(r"\bdocker\s+(?:container\s+)?rm\b"),
        "This command removes Docker containers.",
    ),
    ApprovalRule(
        compile_pattern(r"\bdocker\s+rmi\b"),
        "This command removes Docker images.",
    ),
    ApprovalRule(
        compile_pattern(
            r"\bdocker(?:\s+compose|\-compose)\s+down\b"
            r"[^\n;&|]*(?:\s-v\b|\s--volumes\b)"
        ),
        "This command removes Docker Compose volumes and their data.",
    ),
    # -----------------------------------------------------------------
    # Explicit database-destructive commands
    # -----------------------------------------------------------------
    ApprovalRule(
        compile_pattern(r"\bdropdb(?:\s|$)"),
        "This command drops a PostgreSQL database.",
    ),
    ApprovalRule(
        compile_pattern(
            r"\bredis-cli\b[^\n;&|]*\b"
            r"(?:FLUSHALL|FLUSHDB)\b"
        ),
        "This command clears Redis data.",
    ),
)


def read_command() -> str:
    """Read the beforeShellExecution payload and return its command."""

    payload = json.load(sys.stdin)

    command = payload.get("command")

    if not isinstance(command, str):
        raise TypeError("Hook payload does not contain a valid command.")

    return command


def find_approval_reason(command: str) -> str | None:
    """Return the first approval reason matching the command."""

    for rule in APPROVAL_RULES:
        if rule.pattern.search(command):
            return rule.reason

    return None


def emit_permission(
    permission: str,
    *,
    user_message: str | None = None,
    agent_message: str | None = None,
) -> None:
    """Write a valid Cursor hook response to stdout."""

    response: dict[str, str] = {"permission": permission}

    if user_message is not None:
        response["user_message"] = user_message

    if agent_message is not None:
        response["agent_message"] = agent_message

    json.dump(response, sys.stdout)
    sys.stdout.write("\n")


def main() -> int:
    """Evaluate a shell command against the approval policy."""

    command = read_command()

    reason = find_approval_reason(command)

    if reason is None:
        emit_permission("allow")
        return 0

    emit_permission(
        "ask",
        user_message=(f"Explicit approval is required. {reason}"),
        agent_message=(
            "This shell command crossed an approval boundary defined "
            "by the repository workflow. Do not treat approval of this "
            "command as approval for additional work."
        ),
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        print(
            f"shell-guard: invalid hook input: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1) from None
