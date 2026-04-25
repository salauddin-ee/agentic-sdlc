---
name: asdlc-brownfield-brainstorm
description: Use when understanding the business impact and user impact of a story or feature request in an existing system — before any technical planning or implementation.
version: 1.0.0
---

Understand the business and user impact of this story in isolation before planning how to implement it. Small stories have large blast radii. Understand the blast radius first.

## When to Use

- A story or feature request arrives for an existing system
- After `asdlc-context-harvest` has been completed (existing-system.md exists)
- Before `asdlc-brownfield-tech-plan` begins

## Checklist

1. **Read `docs/architecture/existing-system.md`** — understand the system context
2. **Ask clarifying questions** (one at a time):
   - What user job-to-be-done does this story serve?
   - What is the measurable business outcome? (conversion, retention, error rate reduction)
   - Who is affected — which user personas, which upstream/downstream systems?
   - Are there dependencies on other in-flight stories or parallel work?
   - Is there a deadline or regulatory driver?
3. **Research comparable implementations** — before writing acceptance criteria:
   - Search for how 1-3 similar products or open-source projects implement this feature (see Scale Guide)
   - Note: patterns that are industry standard vs. differentiators worth owning
   - Document findings in the `### Comparable implementations` subsection of the story BRD
4. **Write acceptance criteria** in Given/When/Then format
5. **Write definition of done** for this story specifically
6. **Identify scope risks** — what could expand this story's scope unintentionally?
7. **Check existing behavior** — does anything like this already exist? Can we extend it?
8. **Document in `docs/product/features/brd.md`** (append a story section) — using format below
9. **Transition** — invoke `asdlc-brownfield-design` (if UI changes) or `asdlc-brownfield-tech-plan`

## Questions Protocol

- One question at a time
- Focus: purpose, who is affected, how success is measured
- If the story has multiple independent sub-problems, flag decomposition before going deeper

## Story BRD Format

Append to `docs/product/features/brd.md` (or create if brownfield project):

```markdown
## Story: [STORY-ID] — [Title] — [Date]

### User job-to-be-done
[What is the user trying to accomplish? In their words, not system terms.]

### Business outcome
[Measurable: "reduce support tickets by X%", "increase conversion by Y%", "eliminate manual step Z"]

### User personas affected
[Which personas from the system context? New personas if this story introduces them?]

### Comparable implementations
[How do 1-3 similar products or open-source projects (per Scale Guide) solve this? What patterns are worth borrowing?]
- [Product/project]: [How they handle it] — [What to borrow / what to avoid]

### Acceptance criteria
- Given [context]
- When [action]
- Then [outcome]

### Definition of done (story level)
- [ ] Acceptance criteria verified with passing tests
- [ ] Regression tests still passing
- [ ] Coverage not decreased from baseline
- [ ] No new tech debt introduced (or explicitly logged)

### Dependencies
[Other in-flight stories? Shared systems? External APIs?]

### Scope risks
[What could creep into this story? What is explicitly out of scope?]

### Existing behavior check
[Does a similar capability already exist? URL / method / component name if so.]
```

## Red Flags

| Thought | Reality |
|---|---|
| "The story is self-explanatory" | Self-explanatory to the requester ≠ clear to the implementer. Write it down. |
| "Success metrics aren't needed for a small story" | If you can't measure success, you can't verify done. Define them. |
| "Scope risks are obvious" | Write them down. Unwritten risks become scope creep. |
| "We're extending existing behavior — no need to check" | Check first. Extending the wrong thing is worse than building new. |
| "I don't need to research how others do this" | Reinventing known patterns wastes time. Search first — borrow what works, reject what doesn't. |

## Scale Guide

| Story size | Expected research depth | Acceptance criteria count |
|---|---|---|
| Tiny (few hours) | 1 comparable example, or skip if obvious standard pattern | 1-2 |
| Small (1-2 days) | 2-3 comparable examples | 3-5 |
| Medium (3-5 days) | 3-5 comparable examples with notes | 5-8 |
| Large (>5 days) | Flag for decomposition before continuing | Decompose first |
