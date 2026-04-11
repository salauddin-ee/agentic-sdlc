"""
Static skill validator — M2 implementation.

Rules implemented:
  skill.inventory.missing_skill_md        Skills directory exists under a skill folder but has no SKILL.md
  skill.frontmatter.invalid_yaml          SKILL.md has no valid YAML frontmatter block
  skill.frontmatter.missing_field         Required frontmatter field missing: name | description | version
  skill.frontmatter.description_prefix    description must start with 'Use when'
  skill.frontmatter.name_mismatch         frontmatter 'name' does not match the directory name
  skill.version.invalid_semver            version does not follow X.Y.Z semver format
  skill.placeholder.found                 Placeholder content detected (TBD / fill in later)
  skill.section.missing_red_flags         Discipline skill missing '## Red Flags' section
  skill.section.missing_gate             Workflow skill missing '## Gate' section
  skill.ref.broken_skill               Skill references another skill by name that does not exist

Severity:
  error   - structural violations that break the skill contract
  warning - editorial issues that should be fixed but do not break the skill
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import yaml

from .models import ValidationIssue, ValidationReport
from . import consistency as _consistency
from .utils import rel as _rel

# ---------------------------------------------------------------------------
# Skills that MUST have a ## Red Flags section (discipline / guardrail skills)
# ---------------------------------------------------------------------------
DISCIPLINE_SKILLS = {
    "implementation",
    "git-discipline",
    "hitl-protocol",
    "stage-gates",
    "critical-review",
    "code-review",
    "coding-constitution",
    "writing-skills",
}

# Skills that MUST have a ## Gate section (have explicit exit criteria)
GATED_SKILLS = {
    "inception",
    "design-system",
    "tech-architecture",
    "implementation-planning",
    "story-breakdown",
    "implementation",
    "critical-review",
    "testing",
    "code-review",
    "retrospective",
    "context-harvest",
    "brownfield-tech-plan",
    "git-discipline",
    "stage-gates",
}

# Placeholder patterns that should never appear in a published skill
# We only flag these if they appear as standalone content, NOT inside
# checklist items that are *instructing* the user to check for them.
PLACEHOLDER_PATTERNS = [
    re.compile(r"^\s*TBD\s*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^\s*fill in later\s*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^\s*\[TBD\]\s*$", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^\s*\[TODO:.*?\]\s*$", re.MULTILINE | re.IGNORECASE),
]

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

# Pattern to find references like `skill-name` skill or invoke `skill-name` skill
SKILL_REF_RE = re.compile(r"`([a-z][a-z0-9-]+)`\s+skill", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> tuple[Optional[dict], str]:
    """
    Extract YAML frontmatter from a markdown file.

    Returns (frontmatter_dict, body_text).
    If no valid frontmatter is found, returns (None, full_text).
    """
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    yaml_block = text[3:end].strip()
    body = text[end + 4:].strip()
    try:
        data = yaml.safe_load(yaml_block)
        if not isinstance(data, dict):
            return None, text
        return data, body
    except yaml.YAMLError:
        return None, text


# ---------------------------------------------------------------------------
# Individual rule functions
# Each accepts (skill_name, skill_path, content, frontmatter, repo_root)
# and returns a list[ValidationIssue].
# ---------------------------------------------------------------------------

def _rule_frontmatter_present(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    fm, _ = _parse_frontmatter(content)
    if fm is None:
        return [ValidationIssue(
            rule_id="skill.frontmatter.invalid_yaml",
            severity="error",
            path=_rel(path, repo_root),
            message="No valid YAML frontmatter block found. Add --- delimited frontmatter with name, description, version.",
        )]
    return []


def _rule_required_fields(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    fm, _ = _parse_frontmatter(content)
    if fm is None:
        return []  # already reported by _rule_frontmatter_present
    issues = []
    for field in ("name", "description", "version"):
        if not fm.get(field):
            issues.append(ValidationIssue(
                rule_id="skill.frontmatter.missing_field",
                severity="error",
                path=_rel(path, repo_root),
                message=f"Frontmatter missing required field: '{field}'.",
            ))
    return issues


def _rule_description_prefix(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    fm, _ = _parse_frontmatter(content)
    if not fm or not fm.get("description"):
        return []
    desc = str(fm["description"]).strip()
    if not desc.lower().startswith("use when"):
        return [ValidationIssue(
            rule_id="skill.frontmatter.description_prefix",
            severity="warning",
            path=_rel(path, repo_root),
            message=f"description should start with 'Use when'. Got: '{desc[:60]}...'",
        )]
    return []


def _rule_name_matches_directory(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    fm, _ = _parse_frontmatter(content)
    if not fm or not fm.get("name"):
        return []
    declared = str(fm["name"]).strip()
    if declared != skill_name:
        return [ValidationIssue(
            rule_id="skill.frontmatter.name_mismatch",
            severity="error",
            path=_rel(path, repo_root),
            message=f"Frontmatter 'name' is '{declared}' but directory name is '{skill_name}'. They must match.",
        )]
    return []


def _rule_semver(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    fm, _ = _parse_frontmatter(content)
    if not fm or not fm.get("version"):
        return []
    version = str(fm["version"]).strip()
    if not SEMVER_RE.match(version):
        return [ValidationIssue(
            rule_id="skill.version.invalid_semver",
            severity="warning",
            path=_rel(path, repo_root),
            message=f"version '{version}' does not follow X.Y.Z semver format.",
        )]
    return []


def _rule_no_placeholders(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    issues = []
    for pattern in PLACEHOLDER_PATTERNS:
        for match in pattern.finditer(content):
            line_num = content[:match.start()].count("\n") + 1
            issues.append(ValidationIssue(
                rule_id="skill.placeholder.found",
                severity="error",
                path=_rel(path, repo_root),
                message=f"Placeholder content found: '{match.group().strip()}'. Remove or replace before publishing.",
                line=line_num,
            ))
    return issues


def _rule_red_flags_section(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    if skill_name not in DISCIPLINE_SKILLS:
        return []
    # Accept either ## Red Flags or ## Common Rationalizations (implementation uses the latter)
    has_section = bool(
        re.search(r"^## Red Flags", content, re.MULTILINE) or
        re.search(r"^## Common Rationalizations", content, re.MULTILINE)
    )
    if not has_section:
        return [ValidationIssue(
            rule_id="skill.section.missing_red_flags",
            severity="error",
            path=_rel(path, repo_root),
            message=(
                f"Discipline skill '{skill_name}' must have a '## Red Flags' (or '## Common Rationalizations') "
                "section listing anti-patterns and rationalizations to refuse."
            ),
        )]
    return []


def _rule_gate_section(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    if skill_name not in GATED_SKILLS:
        return []
    has_gate = bool(re.search(r"^## Gate", content, re.MULTILINE))
    if not has_gate:
        return [ValidationIssue(
            rule_id="skill.section.missing_gate",
            severity="error",
            path=_rel(path, repo_root),
            message=(
                f"Workflow skill '{skill_name}' must have a '## Gate' section "
                "defining exit criteria before the next stage begins."
            ),
        )]
    return []


def _rule_broken_skill_refs(skill_name: str, path: Path, content: str, repo_root: Path) -> list[ValidationIssue]:
    """Check that any referenced skill names actually exist as directories."""
    skills_dir = repo_root / "src" / "agentic_sdlc" / "skills"
    existing_skills = {d.name for d in skills_dir.iterdir() if d.is_dir()}
    issues = []
    for match in SKILL_REF_RE.finditer(content):
        ref_name = match.group(1)
        # Skip self-references and generic words that aren't skill names
        if ref_name == skill_name:
            continue
        if ref_name not in existing_skills:
            line_num = content[:match.start()].count("\n") + 1
            issues.append(ValidationIssue(
                rule_id="skill.ref.broken_skill",
                severity="error",
                path=_rel(path, repo_root),
                message=f"References skill '{ref_name}' which does not exist in skills directory.",
                line=line_num,
            ))
    return issues


# ---------------------------------------------------------------------------
# Rule registry — order matters for readability of output
# ---------------------------------------------------------------------------

RULES = [
    _rule_frontmatter_present,
    _rule_required_fields,
    _rule_description_prefix,
    _rule_name_matches_directory,
    _rule_semver,
    _rule_no_placeholders,
    _rule_red_flags_section,
    _rule_gate_section,
    _rule_broken_skill_refs,
]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def validate(repo_root: Path) -> ValidationReport:
    """
    Run all static validation rules against all SKILL.md files in repo_root.

    Args:
        repo_root: Path to the repository root.

    Returns:
        ValidationReport with all issues found.
    """
    report = ValidationReport()
    skills_dir = repo_root / "src" / "agentic_sdlc" / "skills"

    if not skills_dir.exists():
        report.errors.append(ValidationIssue(
            rule_id="validator.skills_dir.missing",
            severity="error",
            path=str(skills_dir),
            message=f"Skills directory not found: {skills_dir}",
        ))
        return report

    skill_dirs = sorted([d for d in skills_dir.iterdir() if d.is_dir()])

    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        skill_path = skill_dir / "SKILL.md"

        # Rule: every skill directory must have a SKILL.md
        if not skill_path.exists():
            report.checks_run += 1
            report.errors.append(ValidationIssue(
                rule_id="skill.inventory.missing_skill_md",
                severity="error",
                path=_rel(skill_dir, repo_root),
                message=f"Skill directory '{skill_name}' has no SKILL.md file.",
            ))
            continue

        content = skill_path.read_text(encoding="utf-8")

        for rule in RULES:
            report.checks_run += 1
            issues = rule(skill_name, skill_path, content, repo_root)
            for issue in issues:
                if issue.severity == "error":
                    report.errors.append(issue)
                else:
                    report.warnings.append(issue)

    # M3: run cross-file consistency checks
    _consistency.check(repo_root, report)

    return report
