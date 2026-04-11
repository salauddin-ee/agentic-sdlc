"""
Scenario eval harness — skeleton for M4.

Loads YAML fixture files and runs rule-based assertions against skill text.

Execution model: RULE-BASED ONLY — no LLM calls.
  - must_include      → check skill text contains each string
  - must_not_include  → check skill text does not contain each string
  - must_have_section → check skill text contains '## <heading>'
  - must_refuse_shortcut → check skill text contains a Red Flags section
                           with anti-rationalization language
  - must_require_hitl → check skill text references the hitl-protocol skill

This module is intentionally empty of assertion implementations (M1).
The fixture loading, path resolution, and report-building are all in place.
Actual assertion logic lands in M4.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from .models import EvalReport, ScenarioFixture, ScenarioResult


def load_fixture(fixture_path: Path) -> ScenarioFixture:
    """Load a single YAML fixture file into a ScenarioFixture."""
    with open(fixture_path) as f:
        data = yaml.safe_load(f)
    return ScenarioFixture(
        id=data["id"],
        skill=data["skill"],
        prompt=data["prompt"],
        context=data.get("context", {}),
        assertions=data.get("assertions", {}),
        expected_result=data.get("expected_result", "pass"),
    )


def load_fixtures(fixtures_root: Path, skill_filter: Optional[str] = None) -> list[ScenarioFixture]:
    """
    Load all fixture files from fixtures_root.

    Directory layout expected:
        fixtures/<skill-name>/<scenario-id>.yaml

    Args:
        fixtures_root: Path to the fixtures directory.
        skill_filter:  If provided, only load fixtures for this skill name.

    Returns:
        List of ScenarioFixture objects.
    """
    pattern = f"{skill_filter}/*.yaml" if skill_filter else "**/*.yaml"
    fixture_paths = sorted(fixtures_root.glob(pattern))
    return [load_fixture(p) for p in fixture_paths]


def evaluate_fixture(fixture: ScenarioFixture, skill_text: str) -> ScenarioResult:
    """
    Evaluate a single fixture against the text of its target skill.

    All assertions are rule-based checks against the skill markdown text.
    No LLM calls are made.

    Args:
        fixture:    The scenario fixture with assertions.
        skill_text: Full text content of the target SKILL.md file.

    Returns:
        ScenarioResult with ok=True if all assertions pass.
    """
    failures: list[str] = []

    # M4: assertion implementations go here.
    # Each assertion type will add to `failures` if it does not hold.

    ok = len(failures) == 0
    return ScenarioResult(scenario_id=fixture.id, skill=fixture.skill, ok=ok, failures=failures)


def run(repo_root: Path, fixtures_root: Path, skill_filter: Optional[str] = None) -> EvalReport:
    """
    Run all scenario evals and return an EvalReport.

    Args:
        repo_root:     Path to the repository root (to locate SKILL.md files).
        fixtures_root: Path to the fixtures directory.
        skill_filter:  If provided, only evaluate fixtures for this skill.

    Returns:
        EvalReport with pass/fail results per scenario.
    """
    report = EvalReport()
    fixtures = load_fixtures(fixtures_root, skill_filter=skill_filter)

    for fixture in fixtures:
        skill_path = repo_root / "src" / "agentic_sdlc" / "skills" / fixture.skill / "SKILL.md"

        if not skill_path.exists():
            report.results.append(ScenarioResult(
                scenario_id=fixture.id,
                skill=fixture.skill,
                ok=False,
                failures=[f"SKILL.md not found for skill '{fixture.skill}' at {skill_path}"],
            ))
            continue

        skill_text = skill_path.read_text(encoding="utf-8")
        result = evaluate_fixture(fixture, skill_text)
        report.results.append(result)

    return report
