---
name: asdlc-context-harvest
description: Use when starting work on an existing codebase you are unfamiliar with — before proposing any change, writing any code, or making any technical recommendation.
version: 1.0.0
---

Build accurate understanding of the existing system before proposing any change. Assumptions about unfamiliar code cause regressions. Evidence first, proposals second.

<HARD-GATE>
Do NOT propose any changes, write any code, or invoke any implementation skill until existing-system.md is written and the gate below passes.
</HARD-GATE>

## Checklist

1. **Ingest available documentation**: README, existing ADRs, API specs, architecture diagrams, CHANGELOG
2. **Detect tech stack and versions**: languages, frameworks, major libraries, runtimes
3. **Run existing test suite**: record pass rate and coverage % as the baseline
4. **Identify existing patterns**: directory structure, naming conventions, error handling style, logging format
5. **Identify known tech debt**: TODO comments, suppressed lint warnings, flagged issues, known fragile areas
6. **Identify integration points**: external services, downstream consumers, event streams, shared databases
7. **Write `docs/architecture/existing-system.md`** — using format below
8. **Gate evaluation** — invoke `asdlc-stage-gates` skill
9. **Transition** — invoke `asdlc-brownfield-brainstorm` skill

## Codebase Fingerprinting Process

### Tech stack detection
Read project configuration files to detect the tech stack, library versions, and build tools. For each claimed or detected technology, classify its status: `present` (backed by a build/config file), `planned` (documented but no code yet), or `not found` (claimed in docs but missing).

```bash
# Check package files
cat package.json | grep -E "(dependencies|devDependencies)"
cat requirements.txt  # or Pipfile, pyproject.toml
cat Cargo.toml
cat build.gradle
cat pom.xml

# Check runtime versions
node --version
python --version
java --version

# Check CI/CD config for version pins
cat .github/workflows/*.yml
cat .circleci/config.yml
```

### Test baseline
Run the full test suite and record:
- Total tests
- Passing / failing
- Coverage % (from coverage report, not estimated)
- **Mandatory Evidence**: You must record the exact command used to run tests, the exit code, timestamp, and a snippet of the summary output.

This is the **immutable baseline**. Coverage must not decrease when you're done.

### Pattern identification
Read representative files from key directories. Identify:
- How errors are handled (throw vs. return, error types)
- How logging is done (library, format, log levels used)
- How requests are validated (middleware, decorators, manual)
- Directory organization philosophy (by layer vs. by feature)
- Test file location and naming convention

## existing-system.md Format

`docs/architecture/existing-system.md`:

```markdown
# Existing system analysis

> **Status:** Draft | Approved
> **Version:** 0.1.0

## Tech stack
| Component | Technology | Version | Status | Notes |
|---|---|---|---|---|
| Language | TypeScript | 5.2 | present | Strict mode enabled |
| Runtime | Node.js | 20 LTS | present | |
| Framework | Express | 4.18 | present | With zod validation middleware |
| Database | PostgreSQL | 15 | planned | Mentioned in docs, not in repo yet |
| Test runner | Vitest | 1.2 | present | |

## Test coverage baseline
- Total tests: [N]
- Passing: [N]
- Failing: [N] (list any pre-existing failures)
- Coverage: [N]% lines / [N]% branches
- Last run: [timestamp]
- **Evidence**:
  - Command: `[exact command]`
  - Exit code: `[0 or other]`
  - Output summary:
    ```text
    [paste final 5-10 lines of test output showing pass/fail counts]
    ```

**This baseline must not decrease. Any change that drops coverage requires HITL approval.**

## Existing patterns
- Error handling: [e.g., custom AppError class, thrown and caught in middleware]
- Logging: [e.g., Winston with JSON format, levels: info/warn/error]
- Input validation: [e.g., Zod schemas at controller boundary]
- Directory structure: [e.g., by feature, not by layer]
- Naming: [e.g., camelCase files, PascalCase classes, kebab-case routes]

## Known tech debt
- [File/area]: [Description of issue]
- [TODOs to be aware of but NOT touch in this story]

## Integration points
| Integration | Direction | Protocol | Notes |
|---|---|---|---|
| Stripe API | outbound | REST | Used for payments — rate limited |
| Redis | outbound | TCP | Used for session cache |
| Internal analytics service | outbound | gRPC | Fragile — see ADR-005 |

## Fragile / high-risk areas
[List files or subsystems that are particularly risky to touch — and why]

## Constraints
[Things we cannot change — API contracts with external consumers, data schema frozen, etc.]
```

## Gate

```
[ ] Tech stack and versions documented
[ ] Test coverage baseline recorded (exact numbers, not estimates)
[ ] Test execution evidence provided (command, exit code, timestamp, output snippet)
[ ] Existing patterns documented — error handling, logging, validation, directory structure
[ ] Tech stack entries classified as present/planned/not-found with file evidence
[ ] Architecture claims validated against repo reality
[ ] Integration points identified with direction and protocol
[ ] Fragile / high-risk areas flagged
[ ] Known tech debt inventoried (not to fix — just to be aware of)
[ ] existing-system.md physically exists at docs/architecture/existing-system.md
```

## Red Flags

| Thought | Reality |
|---|---|
| "I can infer the patterns from one file" | Pattern exceptions are everywhere. Read representative files from at least 3 areas. |
| "The tests probably pass" | Probably is not a baseline. Run the suite. Record the number. |
| "I know this framework — I know the patterns" | Framework knowledge ≠ this team's conventions. Read the actual code. |
| "The integration points are obvious" | Undocumented integrations are where changes cause silent production failures. |
