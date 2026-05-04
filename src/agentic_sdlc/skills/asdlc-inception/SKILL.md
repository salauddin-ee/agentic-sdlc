---
name: asdlc-inception
description: Use when starting a new project from scratch with unclear or partially-formed requirements — before any design, architecture, or code is written.
version: 1.1.0
---

Establish shared understanding of what is being built, for whom, and why — grounded in research about the real world — before anything else is done.

<HARD-GATE>
Do NOT invoke asdlc-design-system, asdlc-tech-architecture, or any implementation skill until you have produced a BRD and the user has approved it. This applies to every project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple to Need a BRD"

Every project goes through inception. A todo app, a CLI tool, a config change — all of them. The BRD can be short (a few sentences for trivial projects), but you MUST produce it and get user approval before moving on.

## Checklist

Complete in order:

1. **Load domain context** — check for any existing files, docs, or prior context in `docs/sdlc/`
2. **Identify the domain** — what industry, regulatory context, key entities, glossary terms apply?
3. **Research comparable products** — search the web for 1-5 products that solve a similar problem (see Scale Guide):
   - What do they do well? What are their known weaknesses or gaps?
   - What UX patterns, naming conventions, or feature sets are standard in this domain?
   - Document findings in the `## Prior art` section of the BRD
4. **Ask clarifying questions** — one at a time, across these axes:
   - Business objective and measurable success criteria
   - User personas and their jobs-to-be-done
   - Constraints (timeline, budget, compliance, existing systems)
   - Out-of-scope items (explicit)
   - Non-functional requirements (latency, availability, scale, geography)
5. **Write `docs/architecture/domain-model.md`** — domain knowledge, industry context, glossary
6. **Write `docs/product/features/brd.md`** — using the `brd-template.md` file in this skill's directory
7. **Self-review the BRD** — check for placeholders, contradictions, missing metrics
8. **Set artifact status** — update `docs/product/features/brd.md` status to `Ready for HITL`
9. **HITL checkpoint** — required before moving to Stage 2 (invoke `asdlc-hitl-protocol` skill)
10. **Record HITL evidence** — once the user responds, record `hitl_prompt`, `hitl_response`, `hitl_decision`, `hitl_approved_by`, and `hitl_approved_at` in the BRD metadata.
11. **Update Artifact Status** — only after an explicit approval response, update `docs/product/features/brd.md` status to `Approved`.
12. **Transition** — invoke `asdlc-design-system` or `asdlc-tech-architecture` skill (ask user which order)

## Clarifying Questions Protocol

- Ask **one question at a time** — never more
- Prefer **multiple-choice** when options are clear
- Focus on: purpose, constraints, success criteria, who is affected
- If the project scope is very large (multiple independent subsystems), flag it and help decompose into sub-projects before continuing

## Gate

Evaluate before triggering HITL:

```
[ ] Business objective is stated and measurable
[ ] At least 2 user personas defined — OR fewer per Scale Guide (tiny projects / explicitly N/A for internal tools)
[ ] Success metrics are quantified — no vague statements
[ ] NFRs captured (latency, availability, security baseline)
[ ] Out-of-scope is explicit — not empty
[ ] No open questions remain (or HITL scheduled to resolve them)
[ ] Prior art section completed — at least 1 comparable product researched (3+ for small/medium/large per Scale Guide)
[ ] BRD status is 'Ready for HITL' before HITL is triggered
[ ] BRD status is 'Approved' after HITL evidence is recorded
[ ] domain-model.md physically exists at docs/architecture/domain-model.md
[ ] brd.md physically exists at docs/product/features/brd.md
[ ] HITL completed and sign-off recorded in docs/sdlc/retrospectives/
```

If any item fails, loop within this stage — do not proceed.

## HITL Checkpoint

After the gate passes, trigger HITL using this format (or invoke `asdlc-hitl-protocol` skill):

```
HITL REQUIRED
Stage: asdlc-inception
Question: Does this BRD accurately capture your requirements before we move to design/architecture?
Context: BRD written to docs/product/features/brd.md
Options: [A] Approved — proceed to next stage
         [B] Changes needed — specify what to revise
Default if no response: Wait for explicit approval
```

## Red Flags

| Thought | Reality |
|---|---|
| "The requirements are obvious" | Obvious to you ≠ agreed with the user. Write the BRD. |
| "We'll figure out personas later" | Personas drive every design decision. Define them now. |
| "Success metrics can be vague" | Vague metrics cannot be verified. Make them quantifiable. |
| "Out-of-scope is implicit" | Implicit scope causes scope creep. Write it down explicitly. |
| "This is too small for a full BRD" | A BRD for a small project is 5 lines. Write them. |
| "I don't need to research competitors" | Research takes 10 minutes. It prevents you from reinventing known bad solutions. |
| "I already know what the competition does" | What you remember ≠ what a fresh search surfaces. Search now, write it down. |

## Scale Guide

Every project goes through inception. The output depth scales; the process doesn't.

| Project size | BRD depth | Prior art research | Example |
|---|---|---|---|
| Tiny (1-day) | 5-10 lines: 1-sentence objective, 1-2 FRs, basic NFRs | 1-2 comparable products | Single landing page, one-off script |
| Small (1-week) | 1 page: full FR list, 2 personas, quantified metrics | 3 comparable products | Simple web app, CLI tool, internal dashboard |
| Medium (1-month) | 2-3 pages: all sections complete | 3-5 with notes | Full-stack web application |
| Large (multi-month) | Full document: all sections, stakeholder sign-offs, compliance | 5+ with deep analysis | Enterprise platform, regulated product |
