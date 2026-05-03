---
name: asdlc-stage-gates
description: Use when evaluating whether a stage's exit criteria are met before proceeding to the next stage. Mandatory at every stage boundary.
version: 1.0.0
---

Every stage ends with a self-evaluated gate. If the gate fails, loop within the stage. Do not proceed.

## The Rule

```
Gate fails → loop within the current stage → fix → re-evaluate → repeat
Gate passes → proceed to next stage
```

There is no partial pass. Every criterion must be checked. Unchecked items are failed items.

## Gate Evaluation Protocol

1. Read the gate checklist for the current stage from its SKILL.md
2. For each criterion: evaluate against actual output, not intent
3. Determine whether this stage has a mandatory HITL checkpoint:
   - Mandatory HITL stages: `asdlc-inception`, `asdlc-tech-architecture`, `asdlc-ui-mockups`, `asdlc-story-breakdown`
   - Mandatory HITL also applies when the stage checklist explicitly requires HITL
4. Validate artifact status:
   - Before HITL: primary artifact must have `Status: Ready for HITL`
   - After HITL approval: primary artifact must have `Status: Approved`
   - Status: Approved is invalid unless HITL evidence is recorded in artifact frontmatter
5. If HITL is mandatory, verify the primary artifact frontmatter or metadata block:
   - Before HITL (`Status: Ready for HITL`): `hitl_prompt` is populated with the exact prompt or a stable reference; `hitl_response`, `hitl_decision`, `hitl_approved_by`, and `hitl_approved_at` may be blank
   - After HITL (`Status: Approved`): all evidence fields must be populated:
     - `hitl_prompt`: exact HITL prompt presented to the user, or a stable reference to the prompt in the artifact
     - `hitl_response`: exact user response or a concise quote/reference from the user response
     - `hitl_decision`: `approved`, `changes_requested`, or `rejected`
     - `hitl_approved_by`: human identifier, name, or `user`
     - `hitl_approved_at`: timestamp/date
6. Mark each criterion `[x]` (pass) or `[ ]` (fail - with reason)
7. If the stage gate criteria pass but HITL has not yet been invoked:
   - Commit current stage artifacts to the current `docs/{stage-name}` branch
   - Invoke `asdlc-hitl-protocol`
   - Stop and wait for explicit user response
   - Do not mark the artifact `Approved`
   - Do not proceed to the next stage
8. If all criteria pass and HITL evidence is complete:
   - Commit all stage artifacts to the current `docs/{stage-name}` branch
     (this branch must have been created at the start of this stage — see `asdlc-git-discipline` skill, Stage Artifact Protocol, step 1):
     ```
     git add docs/
     git commit -m "docs({stage-name}): stage complete — gate passed"
     ```
   - Then proceed to the next stage
9. If any fail: do not proceed. Return to the stage, fix the gap, re-evaluate the full gate

> **Important:** If no `docs/{stage-name}` branch exists, create it now before committing: `git checkout -b docs/{stage-name}`. See `asdlc-git-discipline` skill for full branch and commit conventions.

<HARD-GATE>
Mandatory HITL is not satisfied by intent, conversation memory, or an agent-written "Approved" status. The gate only passes after the prompt and human response are recorded in artifact frontmatter or metadata block.
</HARD-GATE>

## Gate Format

```
GATE [stage name] — [date]
[x] Criterion 1 — verified: [how you verified it]
[x] Criterion 2 — verified: [how you verified it]
[ ] Criterion 3 — FAIL: [specific reason it fails]
[ ] Criterion 4 — FAIL: [specific reason it fails]
RESULT: FAIL — must fix criterion 3 and 4 before proceeding
```

Or on pass:

```
GATE [stage name] — [date]
[x] Criterion 1 — verified: business objective measurable, tied to FR-001
[x] Criterion 2 — verified: 3 personas defined in brd.md
[x] Criterion 3 — verified: success metrics quantified (P95 < 200ms)
[x] Criterion 4 — verified: NFRs listed in brd.md
[x] Criterion 5 — verified: out-of-scope section has 3 explicit items
[x] HITL checkpoint invoked — verified: hitl_prompt, hitl_response, hitl_decision, hitl_approved_by, hitl_approved_at present in brd.md metadata
RESULT: PASS — proceed to asdlc-design-system
```

## Gate Criteria Interpretation

**"Written to `docs/sdlc/`"** — File must physically exist at the specified path. Not drafted in conversation memory.

**"User has reviewed and approved"** — HITL checkpoint completed (invoke `asdlc-hitl-protocol` skill). Not assumed.

**"HITL checkpoint invoked"** — The artifact must reference the actual HITL prompt and user response in frontmatter or the artifact metadata block. The agent cannot infer, summarize from memory, or self-approve this item.

**"Status: Approved"** — Valid only after HITL evidence exists. Before HITL, use `Status: Ready for HITL`.

**"No open questions"** — Every question in `docs/product/features/brd.md > Open questions` is resolved. Not merely noted.

**"All tests passing"** — Run the test suite. Zero failures. Not "probably passing." The artifact must contain explicit test execution evidence (the exact command run, exit code, timestamp, and a summary output snippet).

**"Interface contracts locked"** — The contracts in `docs/architecture/data-domain.md` are stable and approved. Not "mostly defined."

## Common Gate Failures

| Failure | What it means |
|---|---|
| Artifact not written to disk | Complete the output, write the file, re-evaluate |
| Success metrics are vague | Rewrite with quantifiable targets, re-evaluate |
| HITL not completed | Trigger HITL, wait for response, re-evaluate |
| Missing HITL evidence | Add `hitl_prompt`, `hitl_response`, `hitl_decision`, `hitl_approved_by`, and `hitl_approved_at` to artifact frontmatter |
| Tests not run or missing evidence | Run the suite, record results and output snippet, re-evaluate |
| Open questions remain | Resolve them (or explicitly schedule HITL for them), re-evaluate |

## Red Flags

| Thought | Reality |
|---|---|
| "Most criteria pass — close enough" | There is no "close enough." Every criterion must pass. |
| "I'll fix the failing criterion in the next stage" | That's not how gates work. Fix it now. |
| "The criterion is technically met" | If you're arguing technicalities, it's not met. |
| "The user will notice later" | Gates exist so users don't discover gaps in production. |
| "The artifact says Approved, so HITL happened" | Status alone proves nothing. Require recorded prompt and user response. |
| "I asked in chat but did not record it" | Unrecorded HITL fails the gate. Write the evidence to artifact frontmatter. |
