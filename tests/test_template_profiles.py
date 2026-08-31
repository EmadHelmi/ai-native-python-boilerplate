"""Tests for deterministic boilerplate usage profiles."""

from __future__ import annotations

import importlib.util
import runpy
import shutil
import sys
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest import CaptureFixture, MonkeyPatch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SETUP_PATH = PROJECT_ROOT / "scripts" / "setup_profile.py"

PUBLIC_FILES = (
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "SECURITY.md",
    "SUPPORT.md",
    "tests/test_pr_policy.py",
    "tests/test_repository_publication.py",
    "tests/test_template_profiles.py",
    "docs/project/decisions/0001-template-usage-profiles.md",
)

MARKED_DOCUMENT = """# Shared Guide

Reusable guidance remains.

<!-- template-profile:collaborative:start -->
Collaborative-only publication guidance.
<!-- template-profile:collaborative:end -->
"""

PUBLIC_PROJECT_URLS = """[project.urls]
Documentation = "https://example.com/docs"
Issues = "https://example.com/issues"
Repository = "https://example.com"
"""

PYPROJECT = f"""[project]
name = "example"
license = "MIT"
license-files = ["LICENSE"]

{PUBLIC_PROJECT_URLS}
[tool.coverage.run]
source = [".cursor/hooks", ".github/scripts", "scripts"]
"""

README = """# Example

Solo setup remains documented.

<!-- template-profile:collaborative:start -->
Collaborative-only publication guidance.
<!-- template-profile:collaborative:end -->

Shared documentation remains.
"""


def load_setup_module() -> ModuleType:
    """Load the setup command as an importable module."""

    spec = importlib.util.spec_from_file_location("setup_profile", SETUP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the template-profile setup module.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def setup_profile() -> ModuleType:
    """Return a freshly loaded setup module."""

    return load_setup_module()


@pytest.fixture
def template_root(tmp_path: Path) -> Path:
    """Create a representative collaborative template repository."""

    root = tmp_path / "project"
    (root / ".agents").mkdir(parents=True)
    (root / ".cursor" / "rules").mkdir(parents=True)
    (root / ".github" / "scripts").mkdir(parents=True)
    (root / "docs" / "project" / "decisions").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "tests").mkdir()

    (root / "AGENTS.md").write_text("agent agreement\n", encoding="utf-8")
    (root / ".agents" / "skill.md").write_text(
        "agent skill\n", encoding="utf-8"
    )
    (root / ".cursor" / "rules" / "core.mdc").write_text(
        "engineering rule\n", encoding="utf-8"
    )
    (root / ".github" / "scripts" / "validate_pr.py").write_text(
        "# public automation\n", encoding="utf-8"
    )
    shutil.copy2(SETUP_PATH, root / "scripts" / "setup_profile.py")

    for relative_path in PUBLIC_FILES:
        (root / relative_path).write_text("public file\n", encoding="utf-8")

    for relative_path in (
        "docs/getting-started.md",
        "docs/customizing-the-template.md",
        "docs/development-tooling.md",
    ):
        (root / relative_path).write_text(
            MARKED_DOCUMENT,
            encoding="utf-8",
        )
    (root / "docs/project/decisions/README.md").write_text(
        "# Decisions\n\n"
        "| ADR | Decision | Status |\n"
        "| :-- | :------- | :----- |\n"
        "| [ADR-0001](0001-template-usage-profiles.md) "
        "| Template Usage Profiles | Accepted |\n",
        encoding="utf-8",
    )

    (root / "README.md").write_text(README, encoding="utf-8")
    (root / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
    (root / "LICENSE").write_text("MIT notice\n", encoding="utf-8")
    return root


def shared_snapshot(root: Path) -> dict[str, bytes]:
    """Capture all agent and rule content for preservation checks."""

    paths = [root / "AGENTS.md"]
    paths.extend(
        path for path in (root / ".agents").rglob("*") if path.is_file()
    )
    paths.extend(
        path for path in (root / ".cursor").rglob("*") if path.is_file()
    )
    return {
        path.relative_to(root).as_posix(): path.read_bytes() for path in paths
    }


def test_solo_preview_reports_exact_actions_without_mutation(
    setup_profile: ModuleType,
    template_root: Path,
) -> None:
    """Preview every solo mutation while leaving the repository untouched."""

    before = {
        path.relative_to(template_root).as_posix(): path.read_bytes()
        for path in template_root.rglob("*")
        if path.is_file()
    }

    actions = setup_profile.planned_actions(template_root, "solo")

    assert actions == (
        "remove .github",
        "remove CODE_OF_CONDUCT.md",
        "remove CONTRIBUTING.md",
        "remove GOVERNANCE.md",
        "remove SECURITY.md",
        "remove SUPPORT.md",
        "remove tests/test_pr_policy.py",
        "remove tests/test_repository_publication.py",
        "remove tests/test_template_profiles.py",
        "remove docs/project/decisions/0001-template-usage-profiles.md",
        "remove scripts/setup_profile.py",
        "rename LICENSE to THIRD_PARTY_NOTICES.md",
        "remove MIT and public project metadata from pyproject.toml",
        "remove collaborative coverage and documentation references",
    )
    after = {
        path.relative_to(template_root).as_posix(): path.read_bytes()
        for path in template_root.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_apply_solo_removes_only_public_layer(
    setup_profile: ModuleType,
    template_root: Path,
) -> None:
    """Produce a solo tree without changing any agent or rule content."""

    shared_before = shared_snapshot(template_root)
    license_content = (template_root / "LICENSE").read_bytes()

    setup_profile.apply_profile(template_root, "solo")

    assert not (template_root / ".github").exists()
    assert all(not (template_root / path).exists() for path in PUBLIC_FILES)
    assert not (template_root / "scripts/setup_profile.py").exists()
    assert not (template_root / "LICENSE").exists()
    assert (template_root / "THIRD_PARTY_NOTICES.md").read_bytes() == (
        license_content
    )
    assert shared_snapshot(template_root) == shared_before

    pyproject = (template_root / "pyproject.toml").read_text(encoding="utf-8")
    assert 'license = "MIT"' not in pyproject
    assert "license-files" not in pyproject
    assert "[project.urls]" not in pyproject
    assert "ai-native-python-boilerplate" not in pyproject
    assert 'source = [".cursor/hooks"]' in pyproject
    assert ".github/scripts" not in pyproject

    readme = (template_root / "README.md").read_text(encoding="utf-8")
    assert "Collaborative-only" not in readme
    assert "Shared documentation remains." in readme

    for relative_path in (
        "docs/getting-started.md",
        "docs/customizing-the-template.md",
        "docs/development-tooling.md",
    ):
        content = (template_root / relative_path).read_text(encoding="utf-8")
        assert "Collaborative-only" not in content
        assert "Reusable guidance remains." in content

    decision_register = (
        template_root / "docs/project/decisions/README.md"
    ).read_text(encoding="utf-8")
    assert "Template Usage Profiles" not in decision_register


def test_real_solo_output_has_no_public_collaboration_narrative(
    setup_profile: ModuleType,
    tmp_path: Path,
) -> None:
    """Verify the rendered project, not only a representative fixture."""

    target = tmp_path / "solo-project"
    shutil.copytree(
        PROJECT_ROOT,
        target,
        ignore=shutil.ignore_patterns(
            ".git",
            ".pytest_cache",
            ".ruff_cache",
            ".venv",
            "__pycache__",
        ),
    )
    shared_before = shared_snapshot(target)

    setup_profile.apply_profile(target, "solo")

    assert shared_snapshot(target) == shared_before
    assert not (target / ".github").exists()
    assert not (target / "scripts/setup_profile.py").exists()
    assert not (
        target / "docs/project/decisions/0001-template-usage-profiles.md"
    ).exists()

    rendered_paths = (
        Path("README.md"),
        Path("docs/getting-started.md"),
        Path("docs/customizing-the-template.md"),
        Path("docs/development-tooling.md"),
        Path("docs/project/decisions/README.md"),
    )
    forbidden_phrases = (
        "template-profile:collaborative",
        "collaborative profile",
        "public collaboration",
        "public contribution",
        "contribute improvements",
        "github's **use this template**",
        "profile and setup flow",
        "template usage profiles",
    )
    for relative_path in rendered_paths:
        content = (
            (target / relative_path).read_text(encoding="utf-8").casefold()
        )
        assert all(phrase not in content for phrase in forbidden_phrases)


def test_solo_application_removes_one_time_profile_tooling(
    setup_profile: ModuleType,
    template_root: Path,
) -> None:
    """Leave no boilerplate profile implementation in the derived project."""

    setup_profile.apply_profile(template_root, "solo")

    assert not (template_root / "scripts/setup_profile.py").exists()
    assert not (template_root / "tests/test_template_profiles.py").exists()


def test_collaborative_profile_is_a_validated_no_op(
    setup_profile: ModuleType,
    template_root: Path,
) -> None:
    """Keep a complete collaborative repository unchanged."""

    assert setup_profile.planned_actions(template_root, "collaborative") == ()


def test_collaborative_profile_rejects_missing_public_content(
    setup_profile: ModuleType,
    template_root: Path,
) -> None:
    """Reject a collaborative profile with incomplete public content."""

    (template_root / "SUPPORT.md").unlink()

    with pytest.raises(
        setup_profile.ProfileSetupError,
        match="Collaborative profile is incomplete",
    ):
        setup_profile.planned_actions(template_root, "collaborative")


@pytest.mark.parametrize(
    ("pyproject", "expected_error"),
    [
        (
            PYPROJECT.replace('license = "MIT"\n', ""),
            "Collaborative MIT metadata",
        ),
        (
            PYPROJECT.replace(PUBLIC_PROJECT_URLS, ""),
            "Collaborative public project URLs",
        ),
        (
            PYPROJECT.replace(
                'source = [".cursor/hooks", ".github/scripts", "scripts"]',
                'source = ["unknown"]',
            ),
            "Collaborative coverage sources",
        ),
    ],
)
def test_collaborative_profile_rejects_invalid_metadata(
    setup_profile: ModuleType,
    template_root: Path,
    pyproject: str,
    expected_error: str,
) -> None:
    """Reject collaborative metadata that does not match the public layer."""

    (template_root / "pyproject.toml").write_text(pyproject, encoding="utf-8")

    with pytest.raises(setup_profile.ProfileSetupError, match=expected_error):
        setup_profile.planned_actions(template_root, "collaborative")


def test_solo_output_is_no_longer_a_profile_source_repository(
    setup_profile: ModuleType,
    template_root: Path,
) -> None:
    """Require a fresh template for any later profile selection."""

    setup_profile.apply_profile(template_root, "solo")

    with pytest.raises(
        setup_profile.ProfileSetupError,
        match="Not a complete boilerplate root",
    ):
        setup_profile.planned_actions(template_root, "collaborative")


def test_setup_rejects_unrelated_directory(
    setup_profile: ModuleType,
    tmp_path: Path,
) -> None:
    """Refuse to operate outside a recognizable boilerplate root."""

    with pytest.raises(
        setup_profile.ProfileSetupError,
        match="Not a complete boilerplate root",
    ):
        setup_profile.planned_actions(tmp_path, "solo")


def test_setup_rejects_ambiguous_license_state(
    setup_profile: ModuleType,
    template_root: Path,
) -> None:
    """Refuse to overwrite an existing provenance notice."""

    (template_root / "THIRD_PARTY_NOTICES.md").write_text(
        "existing notice\n", encoding="utf-8"
    )

    with pytest.raises(
        setup_profile.ProfileSetupError,
        match="Expected exactly one",
    ):
        setup_profile.planned_actions(template_root, "solo")


def test_setup_rejects_incomplete_solo_profile(
    setup_profile: ModuleType,
    template_root: Path,
) -> None:
    """Reject a solo marker while public collaboration files remain."""

    (template_root / "LICENSE").replace(
        template_root / "THIRD_PARTY_NOTICES.md"
    )
    solo_pyproject = setup_profile._solo_pyproject_content(
        template_root / "pyproject.toml"
    )
    (template_root / "pyproject.toml").write_text(
        solo_pyproject, encoding="utf-8"
    )

    with pytest.raises(
        setup_profile.ProfileSetupError,
        match="still contains public files",
    ):
        setup_profile.planned_actions(template_root, "solo")


def test_filesystem_helpers_report_errors(
    setup_profile: ModuleType,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Translate filesystem failures into stable profile errors."""

    with pytest.raises(setup_profile.ProfileSetupError, match="Cannot read"):
        setup_profile._read_text(tmp_path / "missing.txt")

    with pytest.raises(setup_profile.ProfileSetupError, match="Cannot write"):
        setup_profile._write_text(tmp_path, "content")

    target = tmp_path / "target.txt"
    target.write_text("content", encoding="utf-8")

    def fail_unlink(_path: Path) -> None:
        raise OSError("denied")

    monkeypatch.setattr(Path, "unlink", fail_unlink)
    with pytest.raises(setup_profile.ProfileSetupError, match="Cannot remove"):
        setup_profile._remove_exact_path(target)


def test_remove_exact_path_ignores_absent_path(
    setup_profile: ModuleType,
    tmp_path: Path,
) -> None:
    """Allow an exact removal manifest to contain an already absent path."""

    setup_profile._remove_exact_path(tmp_path / "absent")


@pytest.mark.parametrize(
    ("pyproject", "expected_error"),
    [
        (
            PYPROJECT.replace('license-files = ["LICENSE"]\n', ""),
            "MIT project metadata",
        ),
        (
            PYPROJECT.replace(
                PUBLIC_PROJECT_URLS,
                PUBLIC_PROJECT_URLS
                + '[project.urls]\nRepository = "https://duplicate.example"\n',
            ),
            "Public project URLs",
        ),
        (
            PYPROJECT.replace(
                'source = [".cursor/hooks", ".github/scripts", "scripts"]',
                'source = ["unknown"]',
            ),
            "Coverage sources",
        ),
    ],
)
def test_setup_rejects_unsupported_pyproject_state_before_removal(
    setup_profile: ModuleType,
    template_root: Path,
    pyproject: str,
    expected_error: str,
) -> None:
    """Validate shared configuration before deleting public files."""

    (template_root / "pyproject.toml").write_text(pyproject, encoding="utf-8")

    with pytest.raises(setup_profile.ProfileSetupError, match=expected_error):
        setup_profile.apply_profile(template_root, "solo")

    assert (template_root / ".github").is_dir()
    assert (template_root / "LICENSE").is_file()


def test_setup_rejects_incomplete_readme_markers(
    setup_profile: ModuleType,
    template_root: Path,
) -> None:
    """Reject ambiguous documentation edits before deleting anything."""

    readme = (template_root / "README.md").read_text(encoding="utf-8")
    (template_root / "README.md").write_text(
        readme.replace("<!-- template-profile:collaborative:end -->", ""),
        encoding="utf-8",
    )

    with pytest.raises(
        setup_profile.ProfileSetupError,
        match="Collaborative markers",
    ):
        setup_profile.apply_profile(template_root, "solo")

    assert (template_root / ".github").is_dir()


def test_main_previews_and_applies_solo_profile(
    setup_profile: ModuleType,
    template_root: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Expose an explicit preview-before-apply command-line workflow."""

    monkeypatch.chdir(template_root)

    assert setup_profile.main(["solo"]) == 0
    assert "Planned changes:" in capsys.readouterr().out
    assert (template_root / ".github").is_dir()

    assert setup_profile.main(["solo", "--apply"]) == 0
    assert "Applied changes:" in capsys.readouterr().out
    assert not (template_root / ".github").exists()
    assert not (template_root / "scripts/setup_profile.py").exists()


def test_main_reports_profile_errors(
    setup_profile: ModuleType,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: CaptureFixture[str],
) -> None:
    """Return a stable non-zero result for unsafe CLI requests."""

    monkeypatch.chdir(tmp_path)

    assert setup_profile.main(["solo"]) == 2
    assert "profile setup failed" in capsys.readouterr().err


def test_script_entry_point_returns_success(
    template_root: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """Expose the module as a directly runnable command."""

    monkeypatch.chdir(template_root)
    monkeypatch.setattr(
        sys,
        "argv",
        [str(SETUP_PATH), "collaborative"],
    )

    with pytest.raises(SystemExit, match="0"):
        runpy.run_path(str(SETUP_PATH), run_name="__main__")
