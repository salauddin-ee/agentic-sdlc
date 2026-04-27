---
name: asdlc-ui-mockups
description: Use when a user-facing redesign, new landing page, or major visual contract change needs visual approval before implementation proceeds.
version: 1.1.0
---

Lock visual direction before production work hardens it. Major UI changes require researched, reviewable mockups — at multiple breakpoints — and explicit human approval before implementation planning or production implementation proceeds.

<HARD-GATE>
Do NOT begin production implementation, implementation-planning, or brownfield-tech-plan for the affected UI until a mockup has been reviewed and approved via HITL.
</HARD-GATE>

## When to Use

- A user-facing redesign changes the product's visual contract
- A new landing page or major marketing surface is being introduced
- A brownfield story changes layout, hierarchy, or interaction patterns in a way users will notice immediately
- The design-system stage produced tokens and components, but the team still needs to approve concrete screen direction

## Checklist

1. **Read design inputs**: `docs/product/design-system.md` and `docs/product/accessibility.md` (if present)

2. **Research comparable UIs** — before producing anything, search the web for 3-5 similar screens or products:
   - Screenshot or link 3-5 reference UIs relevant to this surface (competitors, design inspiration, Dribbble, Behance, Mobbin)
   - Identify: layout patterns, information hierarchy, navigation conventions, tone
   - Document references in `docs/product/mockups.md` under `## Design references`

3. **Ask the user explicitly** — one question at a time:
   - "Do you want me to create a mockup, or import existing mockups?"
   - If creating: "Should I use AI image generation or a coded HTML/CSS prototype?" (see Mockup Techniques below)
   - "Which breakpoints are required? (e.g., mobile 375px + desktop 1280px)"

4. **Produce the mockup artifact** using the chosen technique (see Mockup Techniques section):
   - Must cover at minimum **mobile and desktop** breakpoints
   - Must visibly apply design tokens from `docs/product/design-system.md`
   - Must be reviewable by the user without any technical setup

5. **Self-review the mockup** before presenting:
   - Does it match the BRD's functional requirements?
   - Are the accessibility requirements from `docs/product/accessibility.md` visible in the mockup?
   - Are all key user flows represented (at least the primary happy path)?

6. **Write `docs/product/mockups.md`** — using the `mockups-template.md` file in this skill's directory

7. **Share the artifact for review** — link screenshots, open the coded prototype, or embed images in the mockups doc

8. **HITL checkpoint** — invoke `asdlc-hitl-protocol` skill for explicit approval:
   - If changes requested: revise the mockup and re-present (see Iteration Protocol below)
   - If approved: proceed

9. **Record the decision** — update `docs/product/mockups.md` with the approved direction and any scope restrictions

10. **Transition**:
    - Greenfield: continue to `asdlc-tech-architecture` or `asdlc-implementation-planning` only after approval
    - Brownfield: continue to `asdlc-brownfield-tech-plan` only after approval

---

## Mockup Artifact Format

A reviewable mockup artifact must take one of these forms:

| Format | Description | When to use |
|---|---|---|
| **Screenshots** | AI-generated or exported images embedded in `docs/product/mockups.md` | Quick visual direction; no interactivity needed |
| **Coded prototype** | Static HTML/CSS file opened in browser; screenshots captured for the mockups doc | Interactive review; fine layout detail matters |
| **Imported screens** | Exported Figma, wireframe, or design-tool screens saved to `docs/product/mockup-assets/` | Existing design files already exist |

A text description alone is **not** a valid artifact. The user must be able to review the visual direction without technical setup.

---

## Mockup Techniques

Choose the technique that best fits the project context. Document the chosen technique in `docs/product/mockups.md`.

### Technique A — AI Image Generation
**When:** Quick visual direction approval needed; no coded prototype required.
```
1. Describe each screen in detail, referencing the design tokens
2. Use an image generation tool to produce high-fidelity screen mockups
3. Save generated images to docs/product/mockup-assets/
4. Embed images in docs/product/mockups.md
5. Produce at minimum: mobile (375px) and desktop (1280px) variants for each key screen
```

### Technique B — Coded HTML/CSS Prototype
**When:** Interactive review needed; agent has HTML/CSS capability; fine detail matters.
```
1. Build a static HTML page using the design tokens from design-system.md as CSS custom properties
2. Implement the primary user flow only — not full functionality
3. Use placeholder content (Lorem Ipsum, placeholder images)
4. Open the prototype in the browser and take screenshots for the mockups doc
5. Produce responsive layout: single file with CSS media queries for mobile + desktop
```

### Technique C — Import Existing Mockups
**When:** Figma screens, wireframes, or design files already exist.
```
1. Export or screenshot all relevant screens from the existing tool
2. Save to docs/product/mockup-assets/
3. Document: source tool, file location, what screens are covered, what is NOT covered
4. Explicitly note any gaps between the imported mockups and the current BRD requirements
```

---

## Responsive Matrix

Every mockup must address at minimum two breakpoints. Document in the mockups template:

| Screen | Mobile (375px) | Desktop (1280px) | Tablet (768px) |
|---|---|---|---|
| [Screen name] | ✅ Required | ✅ Required | Optional |

If tablet is skipped, document the decision explicitly.

---

## Iteration Protocol

If the user requests changes after the first HITL:

```
Round 1: Revise mockup → re-present → HITL
Round 2: Revise mockup → re-present → HITL
Round 3: If still not approved → HITL with escalation:
         "We have reached 3 iteration rounds. Should we: [A] Approve the current direction with noted reservations, [B] Pause and revisit requirements in brd.md, [C] Continue iterating?"
```

Never proceed to implementation without explicit approval regardless of iteration count.

---

## Gate

```
[ ] Trigger is confirmed: redesign, new landing page, or major visual contract change
[ ] Design references researched — at least 3 comparable UIs documented
[ ] User answered: create or import mockups, and which technique to use
[ ] Mockup covers minimum: mobile (375px) and desktop (1280px) breakpoints
[ ] Design tokens from design-system.md are visibly applied in the mockup
[ ] Primary user flow represented (at least happy path)
[ ] Accessibility requirements visible in mockup (e.g., focus states, contrast)
[ ] docs/product/mockups.md written with artifact references and design references
[ ] Visual direction presented to the user for review
[ ] Explicit approval recorded via HITL before implementation proceeds
[ ] No production implementation started before approval
```

## Red Flags

| Thought | Reality |
|---|---|
| "The redesign is obvious — I'll skip mockups" | Obvious to the agent is not approved by the user. Create or import the mockup first. |
| "A text description is enough" | Major visual changes require screenshots or a coded prototype the user can review. Text is not reviewable. |
| "We already have Figma screens, so I can proceed without documenting them" | Existing mockups still need to be imported, referenced, and explicitly approved in the project artifact. |
| "I'll start coding and refine the visuals later" | Violating the letter of the gate is violating the spirit. Do NOT begin production implementation before approval. |
| "The user hasn't answered but the direction is clear" | No response is not approval. Invoke `asdlc-hitl-protocol` and wait. |
| "I only need to mockup the desktop version" | Mobile is mandatory. Responsive behavior is a contract decision, not an implementation detail. |
| "I'll just pick a mockup technique without asking" | The user may have existing Figma screens or strong tool preferences. Ask first. |
| "Round 3 of revisions — I should just start coding" | No number of revision rounds substitutes for explicit approval. Follow the iteration protocol. |
| "I searched but couldn't find good references" | Search harder. Dribbble, Behance, Mobbin, and competitor sites always have relevant UI patterns. |
