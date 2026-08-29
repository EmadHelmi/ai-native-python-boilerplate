"""Tests for the Cursor shell-command approval guard."""

from __future__ import annotations

import importlib.util
import io
import json
import runpy
import sys
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest import CaptureFixture, MonkeyPatch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = PROJECT_ROOT / ".cursor" / "hooks" / "shell-guard.py"


def load_shell_guard() -> ModuleType:
    """Load the hook file as an importable module."""

    spec = importlib.util.spec_from_file_location("shell_guard", HOOK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the shell guard module.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def shell_guard() -> ModuleType:
    """Return a freshly loaded shell guard module."""

    return load_shell_guard()


@pytest.mark.parametrize(
    ("command", "requires_approval"),
    [
        ("git status --short", False),
        ("python -m pytest", False),
        ("git push origin main", True),
        ("uv sync --locked", True),
        ("rm -rf build", True),
        ("docker system prune", True),
        ("redis-cli FLUSHALL", True),
    ],
)
def test_find_approval_reason(
    shell_guard: ModuleType,
    command: str,
    *,
    requires_approval: bool,
) -> None:
    """Classify representative safe and high-impact commands."""

    reason = shell_guard.find_approval_reason(command)

    assert (reason is not None) is requires_approval


def test_read_command_returns_string(
    shell_guard: ModuleType,
    monkeypatch: MonkeyPatch,
) -> None:
    """Read a valid command from the Cursor hook payload."""

    monkeypatch.setattr(sys, "stdin", io.StringIO('{"command": "git status"}'))

    assert shell_guard.read_command() == "git status"


def test_read_command_rejects_non_string(
    shell_guard: ModuleType,
    monkeypatch: MonkeyPatch,
) -> None:
    """Reject a payload whose command has the wrong type."""

    monkeypatch.setattr(sys, "stdin", io.StringIO('{"command": 42}'))

    with pytest.raises(TypeError, match="valid command"):
        shell_guard.read_command()


def test_emit_permission(
    shell_guard: ModuleType,
    capsys: CaptureFixture[str],
) -> None:
    """Emit the response fields supported by Cursor hooks."""

    shell_guard.emit_permission(
        "ask",
        user_message="Approve this command.",
        agent_message="Wait for approval.",
    )

    assert json.loads(capsys.readouterr().out) == {
        "permission": "ask",
        "user_message": "Approve this command.",
        "agent_message": "Wait for approval.",
    }


@pytest.mark.parametrize(
    ("command", "expected_permission"),
    [("git status", "allow"), ("git commit -m test", "ask")],
)
def test_main_emits_expected_permission(
    shell_guard: ModuleType,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
    command: str,
    expected_permission: str,
) -> None:
    """Return the appropriate Cursor permission for a command."""

    monkeypatch.setattr(
        sys, "stdin", io.StringIO(json.dumps({"command": command}))
    )

    assert shell_guard.main() == 0
    assert (
        json.loads(capsys.readouterr().out)["permission"]
        == expected_permission
    )


def test_script_rejects_invalid_json(
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Exit unsuccessfully when Cursor sends malformed JSON."""

    monkeypatch.setattr(sys, "stdin", io.StringIO("not-json"))

    with pytest.raises(SystemExit, match="1"):
        runpy.run_path(str(HOOK_PATH), run_name="__main__")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "invalid hook input" in captured.err
