---
name: asdlc-ui-mockups
description: Use when a user-facing redesign, new landing page, or major visual contract change needs visual approval before implementation proceeds.
version: 1.0.0
---

Lock visual direction before production work hardens it. Major UI changes require a reviewable mockup and explicit human approval before implementation planning or production implementation proceeds.

<HARD-GATE>
Do NOT begin production implementation, implementation-planning, or brownfield-tech-plan for the affected UI until a mockup has been reviewed and approved.
</HARD-GATE>

## When to Use

- A user-facing redesign changes the product's visual contract
- A new landing page or major marketing surface is being introduced
- A brownfield story changes layout, hierarchy, or interaction patterns in a way users will notice immediately
- The design-system stage produced tokens and components, but the team still needs to approve concrete screen direction

## Checklist

1. **Read design inputs**: `docs/product/design-system.md` and `docs/product/accessibility.md` (if present)
2. **Ask the user explicitly**: "Do you want me to create a mockup, or import existing mockups?"
3. **Produce or import a reviewable artifact**:
   - If creating: create a mockup as screenshots or a coded prototype
   - If importing: record where the existing mockups came from and summarize what they cover
4. **Write `docs/product/mockups.md`** — using the `mockups-template.md` file in this skill's directory
5. **Share the artifact for review** — screenshots or coded prototype must be reviewable by the user
6. **HITL checkpoint** — invoke `asdlc-hitl-protocol` skill for explicit approval of the visual direction
7. **Record the decision** — update `docs/product/mockups.md` with the selected direction and any requested revisions
8. **Transition**:
   - Greenfield: continue to `asdlc-tech-architecture` or `asdlc-implementation-planning` only after approval
   - Brownfield: continue to `asdlc-brownfield-tech-plan` only after approval


## Mockup Artifact Format

Write `docs/product/mockups.md` using the `mockups-template.md` file located in this skill's directory.

## Gate

```
[ ] Trigger is confirmed: redesign, new landing page, or major visual contract change
[ ] User answered whether to create a mockup or import existing mockups
[ ] Reviewable artifact exists as screenshots or a coded prototype
[ ] docs/product/mockups.md written with artifact references
[ ] Visual direction presented to the user for review
[ ] Explicit approval recorded via HITL before implementation proceeds
[ ] No production implementation started before approval
```

## Red Flags

| Thought | Reality |
|---|---|
| "The redesign is obvious — I'll skip mockups" | Obvious to the agent is not approved by the user. Create or import the mockup first. |
| "A text description is enough" | Major visual changes require screenshots or a coded prototype that the user can review. |
| "We already have Figma screens, so I can proceed without documenting them" | Existing mockups still need to be imported, referenced, and explicitly approved in the project artifact. |
| "I'll start coding and refine the visuals later" | Violating the letter of the gate is violating the spirit. Do NOT begin production implementation before approval. |
| "The user hasn't answered but the direction is clear" | No response is not approval. Invoke `asdlc-hitl-protocol` and wait. |
