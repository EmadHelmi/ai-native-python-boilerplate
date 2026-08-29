"""Validate pull-request metadata against the public contribution policy."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

MAX_TITLE_LENGTH = 100
TITLE_PATTERN = re.compile(
    r"^(?:build|chore|ci|docs|feat|fix|perf|refactor|revert|test)"
    r"(?:\([a-z0-9][a-z0-9._/-]*\))?!?: [^\s].*$"
)
REQUIRED_SECTIONS = ("Summary", "Motivation", "Testing", "Checklist")
AUTOMATED_ACTORS = frozenset({"dependabot[bot]"})
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
UNCHECKED_ITEM_PATTERN = re.compile(r"^\s*-\s*\[\s\]", re.MULTILINE)
CHECKED_ITEM_PATTERN = re.compile(r"^\s*-\s*\[[xX]\]", re.MULTILINE)


def validate_title(title: str) -> list[str]:
    """Return policy errors for a pull-request title."""

    errors: list[str] = []

    if len(title) > MAX_TITLE_LENGTH:
        errors.append(
            f"The title must not exceed {MAX_TITLE_LENGTH} characters."
        )

    if TITLE_PATTERN.fullmatch(title) is None:
        errors.append(
            "Use a Conventional Commit title such as "
            "'feat(scope): describe the change'."
        )

    return errors


def visible_content(lines: list[str]) -> str:
    """Return section content after removing template comments."""

    return HTML_COMMENT_PATTERN.sub("", "\n".join(lines)).strip()


def section_ranges(body: str) -> tuple[dict[str, tuple[int, int]], list[str]]:
    """Locate required second-level sections and report structural errors."""

    lines = body.splitlines()
    locations: list[tuple[str, int]] = []
    errors: list[str] = []

    for section in REQUIRED_SECTIONS:
        marker = f"## {section}"
        matches = [
            index for index, line in enumerate(lines) if line.strip() == marker
        ]

        if len(matches) != 1:
            errors.append(f"Include exactly one '{marker}' section.")
            continue

        locations.append((section, matches[0]))

    if errors:
        return {}, errors

    indexes = [index for _, index in locations]
    if indexes != sorted(indexes):
        return {}, ["Keep the required sections in template order."]

    ranges: dict[str, tuple[int, int]] = {}
    for position, (section, start) in enumerate(locations):
        if position + 1 < len(locations):
            end = locations[position + 1][1]
        else:
            end = len(lines)
        ranges[section] = (start + 1, end)

    return ranges, []


def validate_body(body: str) -> list[str]:
    """Return policy errors for a pull-request body."""

    ranges, errors = section_ranges(body)
    if errors:
        return errors

    lines = body.splitlines()

    for section in REQUIRED_SECTIONS[:-1]:
        start, end = ranges[section]
        if not visible_content(lines[start:end]):
            errors.append(f"Provide content in the '{section}' section.")

    checklist_start, checklist_end = ranges["Checklist"]
    checklist = visible_content(lines[checklist_start:checklist_end])

    if CHECKED_ITEM_PATTERN.search(checklist) is None:
        errors.append("Complete the pull-request checklist.")
    if UNCHECKED_ITEM_PATTERN.search(checklist) is not None:
        errors.append("Resolve every unchecked pull-request checklist item.")

    return errors


def read_event(event_path: Path) -> tuple[str, str, str]:
    """Read title, body, and actor from a GitHub pull-request event."""

    event: dict[str, Any] = json.loads(event_path.read_text(encoding="utf-8"))
    pull_request = event.get("pull_request")
    sender = event.get("sender")

    if not isinstance(pull_request, dict):
        raise TypeError("The event does not contain pull_request metadata.")
    if not isinstance(sender, dict):
        raise TypeError("The event does not contain sender metadata.")

    title = pull_request.get("title")
    body = pull_request.get("body") or ""
    actor = sender.get("login")

    if not isinstance(title, str):
        raise TypeError("The pull-request title must be a string.")
    if not isinstance(body, str):
        raise TypeError("The pull-request body must be a string.")
    if not isinstance(actor, str):
        raise TypeError("The pull-request actor must be a string.")

    return title, body, actor


def main() -> int:
    """Validate the GitHub event selected by GITHUB_EVENT_PATH."""

    event_path_value = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path_value:
        print("PR policy: GITHUB_EVENT_PATH is not set.", file=sys.stderr)
        return 1

    try:
        title, body, actor = read_event(Path(event_path_value))
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        print(f"PR policy: unable to read the event: {exc}", file=sys.stderr)
        return 1

    errors = validate_title(title)
    if actor not in AUTOMATED_ACTORS:
        errors.extend(validate_body(body))

    if errors:
        for error in errors:
            print(f"PR policy: {error}", file=sys.stderr)
        return 1

    print("Pull-request metadata satisfies the contribution policy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
