"""Tests for the pull-request metadata policy."""

from __future__ import annotations

import importlib.util
import json
import os
import runpy
import sys
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest import CaptureFixture, MonkeyPatch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = PROJECT_ROOT / ".github" / "scripts" / "validate_pr.py"
VALID_BODY = """## Summary

Add the public contribution baseline.

## Motivation

Make incoming changes consistent and reviewable.

## Testing

Ran the complete local quality gate.

## Checklist

- [x] I ran the relevant checks.
- [X] I updated documentation or confirmed it is unnecessary.
"""


def load_validator() -> ModuleType:
    """Load the policy validator as an importable module."""

    spec = importlib.util.spec_from_file_location(
        "validate_pr", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the pull-request validator.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def validator() -> ModuleType:
    """Return a freshly loaded validator module."""

    return load_validator()


@pytest.mark.parametrize(
    "title",
    [
        "feat: add public contribution files",
        "fix(ci): preserve immutable action pins",
        "refactor!: simplify the baseline",
    ],
)
def test_validate_title_accepts_conventional_titles(
    validator: ModuleType,
    title: str,
) -> None:
    """Accept supported Conventional Commit title forms."""

    assert validator.validate_title(title) == []


def test_validate_title_rejects_invalid_and_long_titles(
    validator: ModuleType,
) -> None:
    """Reject malformed titles and report the length independently."""

    errors = validator.validate_title("Add files " + "x" * 100)

    assert len(errors) == 2


def test_validate_body_accepts_completed_template(
    validator: ModuleType,
) -> None:
    """Accept the required sections when they contain real content."""

    assert validator.validate_body(VALID_BODY) == []


@pytest.mark.parametrize(
    ("body", "expected_error"),
    [
        (
            VALID_BODY.replace("## Motivation", "## Context"),
            "Include exactly one '## Motivation' section.",
        ),
        (
            VALID_BODY.replace(
                "Make incoming changes consistent and reviewable.",
                "<!-- Explain why this is needed. -->",
            ),
            "Provide content in the 'Motivation' section.",
        ),
        (
            VALID_BODY.replace("- [x]", "- [ ]"),
            "Resolve every unchecked pull-request checklist item.",
        ),
        (
            VALID_BODY.replace("- [x]", "- done").replace("- [X]", "- done"),
            "Complete the pull-request checklist.",
        ),
    ],
)
def test_validate_body_rejects_incomplete_templates(
    validator: ModuleType,
    body: str,
    expected_error: str,
) -> None:
    """Reject missing, empty, or incomplete pull-request sections."""

    assert expected_error in validator.validate_body(body)


def test_validate_body_rejects_sections_out_of_order(
    validator: ModuleType,
) -> None:
    """Keep required sections in the order presented by the template."""

    body = (
        VALID_BODY.replace("## Summary", "## Temporary", 1)
        .replace("## Motivation", "## Summary", 1)
        .replace("## Temporary", "## Motivation", 1)
    )

    assert validator.validate_body(body) == [
        "Keep the required sections in template order."
    ]


def write_event(
    path: Path,
    *,
    title: object = "docs: improve contribution guidance",
    body: object = VALID_BODY,
    author: object = "contributor",
    sender: object = "contributor",
) -> None:
    """Write representative GitHub pull-request event data."""

    path.write_text(
        json.dumps(
            {
                "pull_request": {
                    "title": title,
                    "body": body,
                    "user": {"login": author},
                },
                "sender": {"login": sender},
            }
        ),
        encoding="utf-8",
    )


def test_read_event_rejects_missing_metadata(
    validator: ModuleType,
    tmp_path: Path,
) -> None:
    """Reject events that do not describe a pull request."""

    event_path = tmp_path / "event.json"
    event_path.write_text("{}", encoding="utf-8")

    with pytest.raises(TypeError, match="pull_request"):
        validator.read_event(event_path)


def test_read_event_rejects_missing_author(
    validator: ModuleType,
    tmp_path: Path,
) -> None:
    """Reject events without pull-request author metadata."""

    event_path = tmp_path / "event.json"
    event_path.write_text(
        json.dumps({"pull_request": {"title": "fix: valid", "body": ""}}),
        encoding="utf-8",
    )

    with pytest.raises(TypeError, match="author"):
        validator.read_event(event_path)


@pytest.mark.parametrize(
    ("field", "value", "expected_error"),
    [
        ("title", 42, "title"),
        ("body", 42, "body"),
        ("author", 42, "author"),
    ],
)
def test_read_event_rejects_invalid_field_types(
    validator: ModuleType,
    tmp_path: Path,
    field: str,
    value: object,
    expected_error: str,
) -> None:
    """Reject incorrectly typed pull-request event fields."""

    event_path = tmp_path / "event.json"
    values: dict[str, object] = {
        "title": "fix: valid",
        "body": "body",
        "author": "contributor",
    }
    values[field] = value
    write_event(event_path, **values)

    with pytest.raises(TypeError, match=expected_error):
        validator.read_event(event_path)


def test_main_accepts_valid_event(
    validator: ModuleType,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Return success for a valid human-authored pull request."""

    event_path = tmp_path / "event.json"
    write_event(event_path)
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))

    assert validator.main() == 0
    assert "satisfies" in capsys.readouterr().out


def test_main_allows_dependabot_generated_body(
    validator: ModuleType,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Exempt a Dependabot PR even when a maintainer triggers the event."""

    event_path = tmp_path / "event.json"
    write_event(
        event_path,
        title="build(deps): update development dependencies",
        body="Dependabot-generated update.",
        author="dependabot[bot]",
        sender="EmadHelmi",
    )
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))

    assert validator.main() == 0


def test_main_does_not_exempt_human_pr_updated_by_automation(
    validator: ModuleType,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Keep the body policy for human PRs regardless of the event sender."""

    event_path = tmp_path / "event.json"
    write_event(
        event_path,
        body="Missing the required sections.",
        author="contributor",
        sender="dependabot[bot]",
    )
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))

    assert validator.main() == 1


def test_main_rejects_invalid_event(
    validator: ModuleType,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Return failure and an actionable error for invalid metadata."""

    event_path = tmp_path / "event.json"
    write_event(event_path, title="Update things", body="")
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))

    assert validator.main() == 1
    assert "Conventional Commit" in capsys.readouterr().err


def test_main_rejects_missing_event_path(
    validator: ModuleType,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Return failure when GitHub does not provide an event path."""

    monkeypatch.delenv("GITHUB_EVENT_PATH", raising=False)

    assert validator.main() == 1
    assert "GITHUB_EVENT_PATH" in capsys.readouterr().err


def test_main_rejects_malformed_json(
    validator: ModuleType,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Return failure when the event file is not valid JSON."""

    event_path = tmp_path / "event.json"
    event_path.write_text("not-json", encoding="utf-8")
    monkeypatch.setenv("GITHUB_EVENT_PATH", os.fspath(event_path))

    assert validator.main() == 1
    assert "unable to read" in capsys.readouterr().err


def test_script_entrypoint(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Execute the validator through its workflow entry point."""

    event_path = tmp_path / "event.json"
    write_event(event_path)
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))

    with pytest.raises(SystemExit, match="0"):
        runpy.run_path(str(VALIDATOR_PATH), run_name="__main__")

    assert "satisfies" in capsys.readouterr().out
