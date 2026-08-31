"""Apply a supported usage profile to a fresh boilerplate repository."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Final, Literal

Profile = Literal["collaborative", "solo"]

COLLABORATIVE_MARKER_START: Final = (
    "<!-- template-profile:collaborative:start -->"
)
COLLABORATIVE_MARKER_END: Final = "<!-- template-profile:collaborative:end -->"

LICENSE_FIELD: Final = 'license = "MIT"\n'
LICENSE_FILES_FIELD: Final = 'license-files = ["LICENSE"]\n'
PROJECT_URLS_HEADER: Final = "[project.urls]"
COLLABORATIVE_COVERAGE_SOURCE: Final = (
    'source = [".cursor/hooks", ".github/scripts", "scripts"]'
)
SOLO_COVERAGE_SOURCE: Final = 'source = [".cursor/hooks"]'

SOLO_TRANSFORM_PATHS: Final = (
    Path("README.md"),
    Path("docs/getting-started.md"),
    Path("docs/customizing-the-template.md"),
    Path("docs/development-tooling.md"),
)
DECISION_REGISTER_PATH: Final = Path("docs/project/decisions/README.md")
TEMPLATE_PROFILE_ADR_ENTRY: Final = (
    "| [ADR-0001](0001-template-usage-profiles.md) "
    "| Template Usage Profiles | Accepted |\n"
)

CORE_PATHS: Final = (
    Path("AGENTS.md"),
    Path(".agents"),
    Path(".cursor"),
    Path("README.md"),
    Path("pyproject.toml"),
    Path("scripts/setup_profile.py"),
    *SOLO_TRANSFORM_PATHS[1:],
    DECISION_REGISTER_PATH,
)

SOLO_REMOVE_PATHS: Final = (
    Path(".github"),
    Path("CODE_OF_CONDUCT.md"),
    Path("CONTRIBUTING.md"),
    Path("GOVERNANCE.md"),
    Path("SECURITY.md"),
    Path("SUPPORT.md"),
    Path("tests/test_pr_policy.py"),
    Path("tests/test_repository_publication.py"),
    Path("tests/test_template_profiles.py"),
    Path("docs/project/decisions/0001-template-usage-profiles.md"),
    Path("scripts/setup_profile.py"),
)

LICENSE_PATH: Final = Path("LICENSE")
NOTICE_PATH: Final = Path("THIRD_PARTY_NOTICES.md")


class ProfileSetupError(RuntimeError):
    """Report an unsafe or inconsistent template-profile operation."""


def validate_root(root: Path) -> Path:
    """Return a resolved boilerplate root or reject an unrelated directory."""

    resolved_root = root.resolve()
    missing = [
        path for path in CORE_PATHS if not (resolved_root / path).exists()
    ]
    if missing:
        formatted = ", ".join(path.as_posix() for path in missing)
        raise ProfileSetupError(
            f"Not a complete boilerplate root; missing: {formatted}."
        )
    return resolved_root


def detect_current_profile(root: Path) -> Profile:
    """Infer the current profile from mutually exclusive license artifacts."""

    has_license = (root / LICENSE_PATH).is_file()
    has_notice = (root / NOTICE_PATH).is_file()

    if has_license == has_notice:
        raise ProfileSetupError(
            "Expected exactly one of LICENSE or THIRD_PARTY_NOTICES.md."
        )
    return "collaborative" if has_license else "solo"


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise ProfileSetupError(f"Cannot read {path}.") from error


def _project_urls_bounds(lines: list[str]) -> tuple[int, int] | None:
    headers = [
        index
        for index, line in enumerate(lines)
        if line.strip() == PROJECT_URLS_HEADER
    ]
    if not headers:
        return None
    if len(headers) != 1:
        raise ProfileSetupError(
            "Public project URLs in pyproject.toml are incomplete or "
            "ambiguous."
        )

    start = headers[0]
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if lines[index].lstrip().startswith("[")
        ),
        len(lines),
    )
    entries = [
        line
        for line in lines[start + 1 : end]
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not entries:
        raise ProfileSetupError(
            "Public project URLs in pyproject.toml are incomplete or "
            "ambiguous."
        )
    return start, end


def _without_project_urls(content: str) -> str:
    lines = content.splitlines(keepends=True)
    bounds = _project_urls_bounds(lines)
    if bounds is None:
        return content

    start, end = bounds
    del lines[start:end]
    return "".join(lines)


def _solo_pyproject_content(path: Path) -> str:
    content = _read_text(path)
    license_count = content.count(LICENSE_FIELD)
    license_files_count = content.count(LICENSE_FILES_FIELD)

    if (license_count, license_files_count) == (1, 1):
        content = content.replace(LICENSE_FIELD, "", 1)
        content = content.replace(LICENSE_FILES_FIELD, "", 1)
    elif (license_count, license_files_count) != (0, 0):
        raise ProfileSetupError(
            "MIT project metadata in pyproject.toml is incomplete or "
            "ambiguous."
        )

    content = _without_project_urls(content)

    collaborative_count = content.count(COLLABORATIVE_COVERAGE_SOURCE)
    solo_count = content.count(SOLO_COVERAGE_SOURCE)
    if (collaborative_count, solo_count) == (1, 0):
        content = content.replace(
            COLLABORATIVE_COVERAGE_SOURCE,
            SOLO_COVERAGE_SOURCE,
            1,
        )
    elif (collaborative_count, solo_count) != (0, 1):
        raise ProfileSetupError(
            "Coverage sources in pyproject.toml do not match a supported "
            "profile."
        )

    return content


def _without_collaborative_sections(path: Path) -> str:
    """Remove every explicitly marked collaborative-only text section."""

    content = _read_text(path)
    start_count = content.count(COLLABORATIVE_MARKER_START)
    end_count = content.count(COLLABORATIVE_MARKER_END)

    if start_count == 0 or start_count != end_count:
        raise ProfileSetupError(
            f"Collaborative markers in {path} are incomplete or ambiguous."
        )

    for _ in range(start_count):
        before, marked_and_after = content.split(
            COLLABORATIVE_MARKER_START,
            1,
        )
        _, after = marked_and_after.split(COLLABORATIVE_MARKER_END, 1)
        content = f"{before.rstrip()}\n\n{after.lstrip()}"
    return content


def _solo_decision_register_content(path: Path) -> str:
    content = _read_text(path)
    if content.count(TEMPLATE_PROFILE_ADR_ENTRY) != 1:
        raise ProfileSetupError(
            "Template-profile ADR register entry is missing or ambiguous."
        )
    return content.replace(TEMPLATE_PROFILE_ADR_ENTRY, "", 1)


def _validate_collaborative(root: Path) -> None:
    missing = [
        path for path in SOLO_REMOVE_PATHS if not (root / path).exists()
    ]
    if missing:
        formatted = ", ".join(path.as_posix() for path in missing)
        raise ProfileSetupError(
            f"Collaborative profile is incomplete; missing: {formatted}."
        )

    pyproject = _read_text(root / "pyproject.toml")
    if (
        pyproject.count(LICENSE_FIELD) != 1
        or pyproject.count(LICENSE_FILES_FIELD) != 1
    ):
        raise ProfileSetupError(
            "Collaborative MIT metadata is missing from pyproject.toml."
        )
    if pyproject.count(COLLABORATIVE_COVERAGE_SOURCE) != 1:
        raise ProfileSetupError(
            "Collaborative coverage sources are not configured as expected."
        )
    if _project_urls_bounds(pyproject.splitlines(keepends=True)) is None:
        raise ProfileSetupError(
            "Collaborative public project URLs are missing from "
            "pyproject.toml."
        )
    for relative_path in SOLO_TRANSFORM_PATHS:
        _without_collaborative_sections(root / relative_path)
    _solo_decision_register_content(root / DECISION_REGISTER_PATH)


def planned_actions(root: Path, profile: Profile) -> tuple[str, ...]:
    """Return the exact mutations required for a requested profile."""

    resolved_root = validate_root(root)
    current_profile = detect_current_profile(resolved_root)

    if profile == "collaborative":
        if current_profile == "solo":
            raise ProfileSetupError(
                "The solo profile cannot be restored in place; create a fresh "
                "repository from the template."
            )
        _validate_collaborative(resolved_root)
        return ()

    pyproject = resolved_root / "pyproject.toml"
    _solo_pyproject_content(pyproject)
    for relative_path in SOLO_TRANSFORM_PATHS:
        _without_collaborative_sections(resolved_root / relative_path)
    _solo_decision_register_content(resolved_root / DECISION_REGISTER_PATH)

    if current_profile == "solo":
        unexpected = [
            path
            for path in SOLO_REMOVE_PATHS
            if (resolved_root / path).exists()
        ]
        if unexpected:
            formatted = ", ".join(path.as_posix() for path in unexpected)
            raise ProfileSetupError(
                f"Solo profile still contains public files: {formatted}."
            )
        return ()

    actions = [
        f"remove {path.as_posix()}"
        for path in SOLO_REMOVE_PATHS
        if (resolved_root / path).exists()
    ]
    actions.extend(
        (
            "rename LICENSE to THIRD_PARTY_NOTICES.md",
            "remove MIT and public project metadata from pyproject.toml",
            "remove collaborative coverage and documentation references",
        )
    )
    return tuple(actions)


def _write_text(path: Path, content: str) -> None:
    try:
        path.write_text(content, encoding="utf-8")
    except OSError as error:
        raise ProfileSetupError(f"Cannot write {path}.") from error


def _remove_exact_path(path: Path) -> None:
    try:
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    except OSError as error:
        raise ProfileSetupError(f"Cannot remove {path}.") from error


def apply_profile(root: Path, profile: Profile) -> tuple[str, ...]:
    """Apply a profile after validating its complete mutation plan."""

    actions = planned_actions(root, profile)
    if not actions:
        return actions

    resolved_root = root.resolve()
    pyproject_path = resolved_root / "pyproject.toml"
    pyproject_content = _solo_pyproject_content(pyproject_path)
    transformed_content = {
        relative_path: _without_collaborative_sections(
            resolved_root / relative_path
        )
        for relative_path in SOLO_TRANSFORM_PATHS
    }
    transformed_content[DECISION_REGISTER_PATH] = (
        _solo_decision_register_content(resolved_root / DECISION_REGISTER_PATH)
    )

    _write_text(pyproject_path, pyproject_content)
    for relative_path, content in transformed_content.items():
        _write_text(resolved_root / relative_path, content)
    for relative_path in SOLO_REMOVE_PATHS:
        _remove_exact_path(resolved_root / relative_path)

    try:
        (resolved_root / LICENSE_PATH).replace(resolved_root / NOTICE_PATH)
    except OSError as error:
        raise ProfileSetupError(
            "Cannot rename LICENSE to THIRD_PARTY_NOTICES.md."
        ) from error

    return actions


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preview or apply a boilerplate usage profile."
    )
    parser.add_argument("profile", choices=("collaborative", "solo"))
    parser.add_argument(
        "--apply",
        action="store_true",
        help="apply the displayed changes; otherwise only preview them",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the profile setup command from the repository root."""

    arguments = _parser().parse_args(argv)
    profile: Profile = arguments.profile

    try:
        actions = (
            apply_profile(Path.cwd(), profile)
            if arguments.apply
            else planned_actions(Path.cwd(), profile)
        )
    except ProfileSetupError as error:
        print(f"profile setup failed: {error}", file=sys.stderr)
        return 2

    if not actions:
        print(f"Profile '{profile}' is already complete; no changes needed.")
        return 0

    heading = "Applied changes:" if arguments.apply else "Planned changes:"
    print(heading)
    for action in actions:
        print(f"- {action}")
    if not arguments.apply:
        print("Re-run with --apply to perform these changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
