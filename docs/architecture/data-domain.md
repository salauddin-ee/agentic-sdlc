# Interface contracts

> **Status:** Draft
> **Version:** 0.1.0

## CLI commands

### `asdlc validate-skills`
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
      "path": "src/agentic_sdlc/skills/using-agentic-sdlc/SKILL.md",
      "message": "Reference points to skills/<name>/SKILL.md but packaged source lives under src/agentic_sdlc/skills/."
    }
  ],
  "warnings": []
}
```

Exit behavior:
- `0` when no errors are found
- non-zero when one or more validation errors are found

### `asdlc eval-skills`
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
