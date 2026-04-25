---
name: asdlc-design-system
description: Use when establishing visual and interaction language for a project that has UI — before any frontend code is written and before technical architecture locks in visual decisions.
version: 1.0.0
---

Define the visual and interaction language before any technical decisions lock it in. Stages 2 and 3 (design-system and tech-architecture) may run in either order depending on whether UI is the primary driver.

<HARD-GATE>
Do NOT write any frontend code or select UI frameworks until design tokens, component inventory, and accessibility requirements are documented and approved.
</HARD-GATE>

## When to Use

- Project has user-facing UI (web, mobile, desktop)
- Team needs a shared visual language before implementation
- Existing design system needs extending for new components

**Skip this stage** only if: the project is purely backend/API with no UI whatsoever. Document the skip decision in `docs/product/design-system.md` with a one-line rationale.

## Checklist

1. **Read `docs/product/features/brd.md`** — understand the user personas and functional requirements
2. **Search for design inspiration** (before touching tokens):
   - Search the web for UI designs in this domain (Dribbble, Behance, Mobbin, competitor sites)
   - Collect 3-5 reference screenshots or URLs — document in the `## Design references` section of `design-system.md`
   - Identify: color mood, typography style, spacing density, key interaction patterns
3. **Ask design context questions** (one at a time):
   - Is there an existing brand or design system to inherit from?
   - What devices and breakpoints must be supported?
   - Are there data density requirements (dashboards vs. consumer UI)?
   - Internationalization and RTL requirements?
   - Dark mode required?
4. **Reference [component.gallery](https://component.gallery)** for component patterns relevant to the domain
5. **Define design tokens** — color, typography, spacing, border radius, shadows, motion
6. **Generate a visual style tile** — produce a small HTML/CSS preview page (or describe one clearly) showing:
   - Color palette swatches with labels
   - Typography specimens (heading, body, caption examples)
   - Key UI elements (primary button, input field, card) rendered with the tokens
   - This confirms the tokens *look right together* before committing them
7. **Produce component inventory** — every UI component required, with state variants
8. **Write `docs/product/accessibility.md`** — WCAG 2.2 AA requirements
9. **Write `docs/product/design-system.md`** — using the `design-system-template.md` file in this skill's directory
10. **Self-review** — check for missing components, incomplete token definitions
11. **Present to user** — get approval section by section
12. **Gate evaluation** — invoke `asdlc-stage-gates` skill
13. **Transition** — if this is a user-facing redesign, new landing page, or major visual contract change, invoke `asdlc-ui-mockups` before implementation-planning begins

## Accessibility Requirements (`docs/product/accessibility.md`)

```markdown
# Accessibility requirements

> **Status:** Draft | Approved
> **Version:** 0.1.0

## Target
WCAG 2.2 AA minimum

## Color contrast
- Body text: 4.5:1 minimum
- Large text (18px+ bold or 24px+): 3:1 minimum
- UI components and focus indicators: 3:1 minimum

## Keyboard navigation
[List per component — tab order, keyboard shortcuts, focus trap rules]

## Screen reader semantics
[ARIA roles, labels, live regions required per component]

## Focus indicators
Visible on all interactive elements — minimum 3:1 contrast against adjacent colors

## Motion
Respect `prefers-reduced-motion` — all animations must have a static fallback
```

## Gate

```
[ ] Design inspiration researched — at least 3 reference URLs/screenshots documented
[ ] Visual style tile produced — tokens confirmed to look correct together before committing
[ ] Design tokens defined: color, typography, spacing, border radius, shadow, motion
[ ] Component inventory complete — covers all components implied by FR list in BRD
[ ] Accessibility requirements documented (WCAG 2.2 AA target confirmed)
[ ] Responsive breakpoints defined and documented
[ ] Dark mode decision made (required or explicitly out of scope)
[ ] design-system.md and accessibility.md written to docs/product/
[ ] User has reviewed and approved
```

## Red Flags

| Thought | Reality |
|---|---|
| "We'll figure out the design system as we go" | Inconsistent components created under time pressure become permanent tech debt. |
| "Accessibility can be added later" | Retrofitting accessibility is 3-5x more expensive than designing for it. |
| "The tokens don't need to be exact yet" | Approximate tokens lead to approximate implementations. Define them now. |
| "We only need a few components" | Component inventory always grows. Identify all of them upfront. |
| "I don't need to look at references — I'll invent the design" | Inventing without research produces generic or worse-than-existing solutions. Search first. |
| "The style tile is extra work" | Undefined tokens look fine on paper, wrong on screen. Generate the tile before committing. |

## Scale Guide

Adapt depth to project size. Both tiny and large projects go through this stage; the output just scales.

| Project size | Expected output depth | Examples |
|---|---|---|
| Tiny (1-day) | 5-10 tokens, 3-5 components, skip style tile | Single landing page, static site |
| Small (1-week) | Full token table, 10-15 components, simple style tile | Simple web app, internal tool |
| Medium (1-month) | Complete token system, 20+ components, full style tile | Full-stack web application |
| Large (multi-month) | Full design system with variants, dark mode, RTL, animated style tile | Enterprise platform, product suite |
