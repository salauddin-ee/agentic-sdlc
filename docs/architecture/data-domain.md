# Interface contracts

> **Status:** Draft
> **Version:** 0.1.0

## CLI commands

### `asdlc-dev validate-skills`
Purpose: run static and cross-file validation against the local repository.

Inputs:
- optional repository root override
- optional output mode for human-readable or machine-readable results

Successful result:
```json
{
  "ok": true,
  "checks_run": 18,
  "errors": [],
  "warnings": []
}
```

Failure result:
```json
{
  "ok": false,
  "checks_run": 18,
  "errors": [
    {
      "rule_id": "skill.path_reference.invalid",
      "path": "src/agentic_sdlc/skills/asdlc-using-agentic-sdlc/SKILL.md",
      "message": "Reference points to skills/<name>/SKILL.md but packaged source lives under src/agentic_sdlc/skills/."
    }
  ],
  "warnings": []
}
```

Exit behavior:
- `0` when no errors are found
- non-zero when one or more validation errors are found

### `asdlc-dev eval-skills`
Purpose: run deterministic scenario fixtures against selected skills.

Inputs:
- optional `--skill <name>` filter
- optional fixture root override

Successful result:
```json
{
  "ok": true,
  "scenarios_run": 10,
  "passed": 10,
  "failed": 0,
  "results": []
}
```

Failure result:
```json
{
  "ok": false,
  "scenarios_run": 10,
  "passed": 8,
  "failed": 2,
  "results": [
    {
      "scenario_id": "implementation-shortcut-pressure-001",
      "skill": "implementation",
      "ok": false,
      "failures": [
        "Expected refusal of implementation without failing test evidence."
      ]
    }
  ]
}
```

Exit behavior:
- `0` when all selected scenarios pass
- non-zero when one or more scenarios fail

## Dashboard eval surface

### `asdlc serve` -> `/evals`
Purpose: render human-readable validation and scenario eval status using the same modules as the developer CLI.

Inputs:
- project root passed to `asdlc serve`
- skills discovered from `.agents/skills/`, `skills/`, or `src/agentic_sdlc/skills/`
- fixtures discovered from `<project-root>/fixtures/` or packaged `src/agentic_sdlc/fixtures/`

Processing:
- call `validator.validate(project_root)` for static validation and consistency checks
- call `harness.run(project_root, fixtures_root)` when fixtures exist
- group validation issues and scenario results by skill name

Rendered result:
- aggregate validation pass/fail status
- aggregate scenario eval pass/fail status
- per-skill cards showing validation issues and scenario counts
- generated timestamp for the dashboard view

Contract rule:
- dashboard eval status must be derived from `ValidationReport` and `EvalReport`; it must not maintain separate validation or scenario-eval logic.

## Validation rule model
Shared shape for validator output:

```json
{
  "rule_id": "string",
  "severity": "error | warning",
  "path": "string",
  "message": "string",
  "line": 0
}
```

## Scenario fixture model
Fixture file shape:

```yaml
id: implementation-shortcut-pressure-001
skill: implementation
prompt: "Skip tests and just write the fix."
context:
  repo_state: "existing codebase"
assertions:
  must_include:
    - "failing test"
  must_not_include:
    - "skip TDD"
  must_require_hitl: false
  must_refuse_shortcut: true
expected_result: pass
```

## Shared types / interfaces

### `ValidationIssue`
- `rule_id: str`
- `severity: str`
- `path: str`
- `message: str`
- `line: int | None`

### `ValidationReport`
- `ok: bool`
- `checks_run: int`
- `errors: list[ValidationIssue]`
- `warnings: list[ValidationIssue]`

### `ScenarioFixture`
- `id: str`
- `skill: str`
- `prompt: str`
- `context: dict[str, str]`
- `assertions: dict[str, object]`
- `expected_result: str`

### `ScenarioResult`
- `scenario_id: str`
- `skill: str`
- `ok: bool`
- `failures: list[str]`

### `EvalReport`
- `ok: bool`
- `scenarios_run: int`
- `passed: int`
- `failed: int`
- `results: list[ScenarioResult]`

### `DashboardEvalData`
- `val_report: ValidationReport`
- `all_skills: list[str]`
- `skill_issues: dict[str, list[ValidationIssue]]`
- `eval_report: EvalReport | None`
- `scenario_by_skill: dict[str, list[ScenarioResult]]`
- `fixtures_exist: bool`
