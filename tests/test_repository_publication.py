"""Validate public repository identity and merge-protection metadata."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_SLUG = "EmadHelmi/ai-native-python-boilerplate"
REPOSITORY_URL = f"https://github.com/{REPOSITORY_SLUG}"
REQUIRED_CHECKS = {
    "Compatibility gate",
    "Quality gate",
    "Review dependency changes",
    "Validate metadata",
}
UV_VERSION_PATTERN = re.compile(
    r'^\s*UV_VERSION:\s*"(?P<version>[^\"]+)"$', re.MULTILINE
)
UV_HOOK_PATTERN = re.compile(
    r"repo: https://github\.com/astral-sh/uv-pre-commit\s+"
    r"rev: (?P<version>\S+)",
)


def load_ruleset() -> dict[str, Any]:
    """Return the versioned default-branch ruleset."""

    path = PROJECT_ROOT / ".github" / "rulesets" / "main.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _required_match(pattern: re.Pattern[str], content: str) -> str:
    match = pattern.search(content)
    assert match is not None
    return match.group("version")


def test_uv_runtime_and_lock_hook_versions_match() -> None:
    """Prevent the CI uv runtime from drifting behind the lock hook."""

    workflow = (PROJECT_ROOT / ".github/workflows/ci.yml").read_text(
        encoding="utf-8"
    )
    hooks = (PROJECT_ROOT / ".pre-commit-config.yaml").read_text(
        encoding="utf-8"
    )

    assert _required_match(UV_VERSION_PATTERN, workflow) == _required_match(
        UV_HOOK_PATTERN,
        hooks,
    )


def rules_by_type(ruleset: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index rules by their unique type."""

    rules = ruleset["rules"]
    assert isinstance(rules, list)
    return {rule["type"]: rule for rule in rules}


def test_packaging_metadata_uses_canonical_repository_urls() -> None:
    """Keep published package links aligned with the selected repository."""

    with (PROJECT_ROOT / "pyproject.toml").open("rb") as file:
        project = tomllib.load(file)["project"]

    assert project["urls"] == {
        "Documentation": f"{REPOSITORY_URL}/tree/main/docs",
        "Issues": f"{REPOSITORY_URL}/issues",
        "Repository": REPOSITORY_URL,
    }


def test_readme_public_actions_are_profile_scoped() -> None:
    """Keep publication badges inside the removable collaborative section."""

    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    start = readme.index("<!-- template-profile:collaborative:start -->")
    end = readme.index("<!-- template-profile:collaborative:end -->")
    public_section = readme[start:end]

    assert f"{REPOSITORY_URL}/generate" in public_section
    assert f"{REPOSITORY_URL}/actions/workflows/ci.yml" in public_section
    assert "Contribute" in public_section


def test_security_policy_uses_private_reporting() -> None:
    """Send vulnerability reports to GitHub's private advisory workflow."""

    policy = (PROJECT_ROOT / "SECURITY.md").read_text(encoding="utf-8")
    assert f"{REPOSITORY_URL}/security/advisories/new" in policy
    assert "mailto:s.emad.helmi@gmail.com" in policy


def test_ruleset_protects_default_branch() -> None:
    """Enforce the approved review, merge, and history policy."""

    ruleset = load_ruleset()
    assert ruleset["name"] == "Protect main"
    assert ruleset["target"] == "branch"
    assert ruleset["source_type"] == "Repository"
    assert ruleset["enforcement"] == "active"
    assert ruleset["conditions"]["ref_name"] == {
        "exclude": [],
        "include": ["~DEFAULT_BRANCH"],
    }
    assert ruleset["bypass_actors"] == [
        {
            "actor_id": 5,
            "actor_type": "RepositoryRole",
            "bypass_mode": "pull_request",
        }
    ]

    rules = rules_by_type(ruleset)
    assert {"deletion", "non_fast_forward", "required_linear_history"} <= (
        rules.keys()
    )

    pull_request = rules["pull_request"]["parameters"]
    assert pull_request == {
        "allowed_merge_methods": ["squash"],
        "dismiss_stale_reviews_on_push": True,
        "require_code_owner_review": True,
        "require_last_push_approval": False,
        "required_approving_review_count": 1,
        "required_review_thread_resolution": True,
    }

    status_checks = rules["required_status_checks"]["parameters"]
    assert status_checks["strict_required_status_checks_policy"] is True
    assert status_checks["do_not_enforce_on_create"] is False
    assert {
        check["context"] for check in status_checks["required_status_checks"]
    } == REQUIRED_CHECKS
