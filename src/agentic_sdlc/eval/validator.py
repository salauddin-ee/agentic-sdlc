"""
Static skill validator — skeleton for M2.

Checks every SKILL.md in the skills directory for:
- Valid YAML frontmatter
- Required frontmatter fields: name, description, version
- Description starts with 'Use when'
- No placeholder content (TODO, TBD, fill in later)
- Required sections present (## Red Flags for discipline skills, etc.)

This module is intentionally empty of rule implementations for now (M1).
The structure, entry-point, and report-building wiring are all in place.
Actual rule implementations land in M2.
"""

from __future__ import annotations

from pathlib import Path

from .models import ValidationIssue, ValidationReport


def validate(repo_root: Path) -> ValidationReport:
    """
    Run all static validation checks against skills in repo_root.

    Args:
        repo_root: Path to the repository root. Skills are expected at
                   src/agentic_sdlc/skills/<name>/SKILL.md relative to this root.

    Returns:
        ValidationReport with all issues found.
    """
    report = ValidationReport()
    skills_dir = repo_root / "src" / "agentic_sdlc" / "skills"

    if not skills_dir.exists():
        report.errors.append(ValidationIssue(
            rule_id="validator.skills_dir.missing",
            severity="error",
            path=str(skills_dir.relative_to(repo_root)),
            message=f"Skills directory not found: {skills_dir}",
        ))
        return report

    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    report.checks_run += len(skill_files)

    # M2: rule implementations go here
    # Each rule will be a function that accepts (skill_path, content, frontmatter)
    # and returns a list[ValidationIssue].

    return report
