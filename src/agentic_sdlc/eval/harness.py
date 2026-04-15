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

    Assertion types:
      must_include        List[str]  — each string must appear verbatim in skill text
      must_not_include    List[str]  — each string must NOT appear in skill text
      must_have_section   List[str]  — each '## Heading' must be present
      must_refuse_shortcut  bool     — skill must have a Red Flags / Common Rationalizations
                                       section AND it must contain language matching the
                                       shortcut described in the fixture prompt
      must_require_hitl     bool     — skill must explicitly reference the hitl-protocol skill

    Args:
        fixture:    The scenario fixture with assertions.
        skill_text: Full text content of the target SKILL.md file.

    Returns:
        ScenarioResult with ok=True if all assertions pass.
    """
    failures: list[str] = []
    skill_text_lower = skill_text.lower()

    # ------------------------------------------------------------------
    # must_include — verbatim string presence
    # ------------------------------------------------------------------
    for required in fixture.must_include:
        if required.lower() not in skill_text_lower:
            failures.append(
                f"must_include FAIL: skill text does not contain '{required}'. "
                f"The skill must explicitly mention this to handle the scenario: \"{fixture.prompt}\""
            )

    # ------------------------------------------------------------------
    # must_not_include — forbidden string absence
    # ------------------------------------------------------------------
    for forbidden in fixture.must_not_include:
        if forbidden.lower() in skill_text_lower:
            failures.append(
                f"must_not_include FAIL: skill text contains forbidden string '{forbidden}'. "
                f"This would permit incorrect behavior in scenario: \"{fixture.prompt}\""
            )

    # ------------------------------------------------------------------
    # must_have_section — ## Heading must be present
    # ------------------------------------------------------------------
    for section in fixture.must_have_section:
        heading = f"## {section}" if not section.startswith("##") else section
        if heading.lower() not in skill_text_lower:
            failures.append(
                f"must_have_section FAIL: skill is missing section '{heading}'. "
                f"This section is required to handle scenario: \"{fixture.prompt}\""
            )

    # ------------------------------------------------------------------
    # must_refuse_shortcut — skill must have anti-shortcut guardrails
    #
    # Pass condition:
    #   1. Skill contains a Red Flags OR Common Rationalizations section, AND
    #   2. That section contains at least one row that addresses the
    #      shortcut pattern described in the fixture's prompt keywords
    # ------------------------------------------------------------------
    if fixture.must_refuse_shortcut:
        has_guardrail_section = (
            "## red flags" in skill_text_lower
            or "## common rationalizations" in skill_text_lower
        )
        if not has_guardrail_section:
            failures.append(
                f"must_refuse_shortcut FAIL: skill has no '## Red Flags' or "
                f"'## Common Rationalizations' section. Cannot guard against: \"{fixture.prompt}\""
            )
        else:
            # Extract keywords from the prompt and check they are addressed
            # in the guardrail section. Use simple word overlap heuristic.
            prompt_keywords = set(
                w.lower() for w in fixture.prompt.split()
                if len(w) > 4 and w.isalpha()
            )
            # Find the guardrail section text
            section_start = max(
                skill_text_lower.find("## red flags"),
                skill_text_lower.find("## common rationalizations"),
            )
            guardrail_text = skill_text_lower[section_start:]
            matched = any(kw in guardrail_text for kw in prompt_keywords)
            if not matched:
                failures.append(
                    f"must_refuse_shortcut FAIL: '## Red Flags' section does not address "
                    f"the shortcut pattern in prompt \"{fixture.prompt}\". "
                    f"Add an explicit row covering this rationalization."
                )

    # ------------------------------------------------------------------
    # must_require_hitl — skill must reference hitl-protocol
    # ------------------------------------------------------------------
    if fixture.must_require_hitl:
        has_hitl_ref = (
            "hitl-protocol" in skill_text_lower
            or "hitl" in skill_text_lower
        )
        if not has_hitl_ref:
            failures.append(
                f"must_require_hitl FAIL: skill does not reference 'hitl-protocol'. "
                f"This scenario requires explicit human approval: \"{fixture.prompt}\""
            )

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

    if skill_filter and not fixtures:
        report.results.append(ScenarioResult(
            scenario_id="harness-load",
            skill=skill_filter,
            ok=False,
            failures=[f"Zero coverage: No scenarios found for skill '{skill_filter}'"],
        ))

    for fixture in fixtures:
        skill_path = repo_root / ".agents" / "skills" / fixture.skill / "SKILL.md"
        if not skill_path.exists():
            skill_path = repo_root / "skills" / fixture.skill / "SKILL.md"
        if not skill_path.exists():
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
