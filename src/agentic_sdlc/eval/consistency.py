"""
Cross-file consistency checker — M3 implementation.

Checks for drift between skills, docs, templates, and CLI-generated paths.

Rules implemented:
  consistency.path.wrong_artifact_name     Skill references a file by a stale/wrong name
                                            (e.g. interface-contracts.md → data-domain.md)
  consistency.path.wrong_location          Skill references correct filename but wrong directory
                                            (e.g. implementation-plan in docs/sdlc/ vs docs/sdlc/epics/)
  consistency.template.missing             Skill instructs copying a template that doesn't exist
  consistency.cli.missing_stub             Skill references a doc path that CLI init does not create
  consistency.skill_path.old_style         Skill references skills using old repo-root style
                                           (.agents/skills/<name>/SKILL.md) instead of packaged path

All findings are ERRORS because path drift directly causes agent confusion.
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import ValidationIssue, ValidationReport
from .utils import rel as _rel


# ---------------------------------------------------------------------------
# Canonical file names — single source of truth
# Skills should use THESE names; flag anything else as drift.
# ---------------------------------------------------------------------------

# Maps stale/wrong filenames → canonical filenames
STALE_FILENAME_MAP: dict[str, str] = {
    "interface-contracts.md": "data-domain.md",
    "coding-constitution.md": "coding-standards.md",
}

# Maps stale paths → canonical paths (full relative path from repo root)
STALE_PATH_MAP: dict[str, str] = {
    "docs/sdlc/interface-contracts.md":    "docs/architecture/data-domain.md",
    "docs/sdlc/implementation-plan.md":    "docs/sdlc/epics/implementation-plan.md",
    "docs/sdlc/coding-constitution.md":    "docs/architecture/coding-standards.md",
}

# Files that CLI init creates as stubs (relative to repo root)
CLI_CREATED_STUBS: set[str] = {
    "docs/architecture/domain-model.md",
    "docs/product/features/brd.md",
    "docs/product/design-system.md",
    "docs/product/mockups.md",
    "docs/product/personas.md",
    "docs/architecture/tech-architecture.md",
    "docs/architecture/coding-standards.md",
    "docs/sdlc/epics/implementation-plan.md",
    "docs/architecture/data-domain.md",
    "docs/product/accessibility.md",
    "docs/architecture/existing-system.md",
}

# Files referenced in skills that CLI does NOT create as stubs
# These are created during the workflow itself (not by init)
WORKFLOW_CREATED_FILES: set[str] = {
    "docs/sdlc/epics/task-graph.md",
    "docs/sdlc/test-plans/test-plan.md",
    "docs/sdlc/retrospectives/retrospective.md",
    "docs/sdlc/retrospectives/critical-review.md",
}

# Pattern: old-style skill path references. Match:
#   - skills/<name>/SKILL.md
#   - ./skills/<name>/SKILL.md
# while excluding:
#   - .agents/skills/<name>/SKILL.md
#   - src/agentic_sdlc/skills/<name>/SKILL.md
OLD_SKILL_PATH_RE = re.compile(
    r"(?<!\.agents/)(?<!src/agentic_sdlc/)(?:\./)?skills/([\w<>.-]+)/SKILL\.md"
)


def _check_stale_filenames(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    """Flag any references to stale/renamed filenames."""
    issues = []
    for stale, canonical in STALE_FILENAME_MAP.items():
        # Match as a standalone word (not the canonical name itself)
        if stale in content:
            # Find line numbers
            for i, line in enumerate(content.splitlines(), 1):
                if stale in line:
                    issues.append(ValidationIssue(
                        rule_id="consistency.path.wrong_artifact_name",
                        severity="error",
                        path=_rel(path, repo_root),
                        message=(
                            f"References stale filename '{stale}'. "
                            f"The canonical name is '{canonical}'. Update all references."
                        ),
                        line=i,
                    ))
    return issues


def _check_stale_paths(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    """Flag references to stale full paths."""
    issues = []
    for stale_path, canonical_path in STALE_PATH_MAP.items():
        if stale_path in content:
            for i, line in enumerate(content.splitlines(), 1):
                if stale_path in line:
                    issues.append(ValidationIssue(
                        rule_id="consistency.path.wrong_location",
                        severity="error",
                        path=_rel(path, repo_root),
                        message=(
                            f"References stale path '{stale_path}'. "
                            f"The correct path is '{canonical_path}'."
                        ),
                        line=i,
                    ))
    return issues


def _check_template_refs(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    """Check that any template file referenced in a skill actually exists in that skill's directory."""
    issues = []
    
    # Find references like `foo-template.md`
    pattern = re.compile(r"([a-z-]+-template\.md)")
    for match in pattern.finditer(content):
        template_name = match.group(1)
        template_path = path.parent / template_name
        if not template_path.exists():
            line_num = content[:match.start()].count("\n") + 1
            issues.append(ValidationIssue(
                rule_id="consistency.template.missing",
                severity="error",
                path=_rel(path, repo_root),
                message=f"References template '{template_name}' which does not exist in the skill's directory.",
                line=line_num,
            ))
    return issues


def _check_doc_path_refs(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    """
    Check that referenced docs/ paths are either CLI-created stubs or known workflow-created files.
    Flag any docs/ path that is neither — it may be a typo or stale reference.
    """
    issues = []
    known_paths = CLI_CREATED_STUBS | WORKFLOW_CREATED_FILES

    # Match doc path references like docs/path/to/file.md
    doc_path_re = re.compile(r"`?(docs/[a-z-/]+\.md)`?")
    for match in doc_path_re.finditer(content):
        ref_path = match.group(1)
        if ref_path not in known_paths:
            # It could be a dynamically-named path like docs/architecture/adrs/ADR-001.md
            # Only flag if it doesn't have a wildcard/placeholder segment
            is_placeholder = re.search(r"(ADR-|STORY-|\[|\{|N\d\d\d)", ref_path)
            if not is_placeholder:
                line_num = content[:match.start()].count("\n") + 1
                issues.append(ValidationIssue(
                    rule_id="consistency.cli.missing_stub",
                    severity="error",
                    path=_rel(path, repo_root),
                    message=(
                        f"References '{ref_path}' which is neither a CLI-created stub nor a "
                        "known workflow-created file. Add it to the CLI init stubs or document it as workflow-created."
                    ),
                    line=line_num,
                ))
    return issues


def _check_old_style_skill_paths(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    """
    Flag old-style bare skill path references (skills/<name>/SKILL.md)
    which should now be .agents/skills/<name>/SKILL.md.
    We allow relative internal paths if resolving inside the package, but warn if we see
    the outdated skills/<name>/SKILL.md convention.

    Args:
        content: The text content to check.
        repo_root: The repo root path.
    Returns:
        List of CheckIssue containing any warnings.
    """
    issues = []
    
    for match in OLD_SKILL_PATH_RE.finditer(content):
        full_ref = match.group(0)
        line_num = content[:match.start()].count("\n") + 1
        issues.append(ValidationIssue(
            rule_id="consistency.skill_path.old_style",
            severity="error",
            path=_rel(path, repo_root),
            line=line_num,
            message=(
                f"References skill using old repo-root path '{full_ref}'. "
                "Update to use '.agents/skills/<name>/SKILL.md'."
            )
        ))
    
    return issues


# ---------------------------------------------------------------------------
# Rule registry
# ---------------------------------------------------------------------------

CONSISTENCY_RULES = [
    _check_stale_filenames,
    _check_stale_paths,
    _check_template_refs,
    _check_doc_path_refs,
    _check_old_style_skill_paths,
]


# ---------------------------------------------------------------------------
# Public entry point — called by the main validate() in validator.py
# ---------------------------------------------------------------------------

def check(repo_root: Path, report: ValidationReport) -> None:
    """
    Run all consistency checks against all SKILL.md files in repo_root.

    Findings are appended directly to the provided report.
    This is called from validator.validate() after static rules complete.

    Args:
        repo_root: Path to the repository root.
        report:    ValidationReport to append findings to.
    """
    skills_dir = repo_root / ".agents" / "skills"
    if not skills_dir.exists():
        skills_dir = repo_root / "skills"
    if not skills_dir.exists():
        skills_dir = repo_root / "src" / "agentic_sdlc" / "skills"
    if not skills_dir.exists():
        return  # already reported by static validator

    skill_files = sorted(skills_dir.glob("*/SKILL.md"))

    for skill_path in skill_files:
        skill_name = skill_path.parent.name
        content = skill_path.read_text(encoding="utf-8")

        for rule in CONSISTENCY_RULES:
            report.checks_run += 1
            issues = rule(skill_name, skill_path, content, repo_root)
            for issue in issues:
                if issue.severity == "error":
                    report.errors.append(issue)
                else:
                    report.warnings.append(issue)
