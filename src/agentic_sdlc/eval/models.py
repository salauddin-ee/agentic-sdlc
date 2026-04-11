"""
Shared data models for the eval package.

These are the canonical types used by both the static validator
and the scenario eval harness. Defined here to avoid circular imports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Validation models  (used by: asdlc validate-skills)
# ---------------------------------------------------------------------------

@dataclass
class ValidationIssue:
    """A single validation finding from the static validator or consistency checker."""

    rule_id: str
    """Dot-separated identifier, e.g. 'skill.frontmatter.missing_field'."""

    severity: str
    """'error' or 'warning'. Errors cause a non-zero exit; warnings are informational."""

    path: str
    """Repo-relative path to the file that triggered this issue."""

    message: str
    """Human-readable explanation of the problem."""

    line: Optional[int] = None
    """1-indexed line number within the file, if known."""

    def as_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
            "line": self.line,
        }


@dataclass
class ValidationReport:
    """Aggregated result of a full validate-skills run."""

    checks_run: int = 0
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def as_dict(self) -> dict:
        return {
            "ok": self.ok,
            "checks_run": self.checks_run,
            "errors": [e.as_dict() for e in self.errors],
            "warnings": [w.as_dict() for w in self.warnings],
        }


# ---------------------------------------------------------------------------
# Scenario eval models  (used by: asdlc eval-skills)
# ---------------------------------------------------------------------------

@dataclass
class ScenarioFixture:
    """
    A single scenario fixture loaded from a YAML file.

    Fixtures define the prompt, target skill, and rule-based assertions
    that determine whether the skill text is adequate to handle the scenario.

    Assertion semantics (all rule-based — no LLM required):
      must_include      : strings that MUST appear in the skill text
      must_not_include  : strings that MUST NOT appear in the skill text
      must_have_section : markdown section headings (## Foo) that must exist
      must_refuse_shortcut : skill must contain a Red Flags table or explicit
                             refusal language for the shortcut described in prompt
    """

    id: str
    skill: str
    prompt: str
    context: dict = field(default_factory=dict)
    assertions: dict = field(default_factory=dict)
    expected_result: str = "pass"

    # Convenience accessors for typed assertion fields
    @property
    def must_include(self) -> list[str]:
        return self.assertions.get("must_include", [])

    @property
    def must_not_include(self) -> list[str]:
        return self.assertions.get("must_not_include", [])

    @property
    def must_have_section(self) -> list[str]:
        return self.assertions.get("must_have_section", [])

    @property
    def must_refuse_shortcut(self) -> bool:
        return bool(self.assertions.get("must_refuse_shortcut", False))

    @property
    def must_require_hitl(self) -> bool:
        return bool(self.assertions.get("must_require_hitl", False))


@dataclass
class ScenarioResult:
    """Result of evaluating a single scenario fixture."""

    scenario_id: str
    skill: str
    ok: bool
    failures: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "scenario_id": self.scenario_id,
            "skill": self.skill,
            "ok": self.ok,
            "failures": self.failures,
        }


@dataclass
class EvalReport:
    """Aggregated result of a full eval-skills run."""

    results: list[ScenarioResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(r.ok for r in self.results)

    @property
    def scenarios_run(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.ok)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.ok)

    def as_dict(self) -> dict:
        return {
            "ok": self.ok,
            "scenarios_run": self.scenarios_run,
            "passed": self.passed,
            "failed": self.failed,
            "results": [r.as_dict() for r in self.results if not r.ok],
        }
