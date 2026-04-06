---
name: brownfield-design
description: Use when a brownfield story introduces new UI components or changes visual contracts visible to end users — before any frontend code is written for that story.
---

Resolve design for this story only. Inherit from the existing design system wherever possible. Introduce new design decisions only when the story genuinely requires them.

## When to Use

- Story introduces a new UI component that doesn't exist in the system
- Story changes an existing visual contract visible to users (layout, color, interaction)
- Story adds a new form, modal, table, or page-level element

**Skip this stage** if: the story is purely backend/API with no UI impact. Document the skip in a one-line note.

## Principle: Inherit First, Extend Minimally

Before proposing any new design:
1. Read the existing design system (in `/.agentic-sdlc/design-system.md` or the project's design tokens)
2. Check if any existing component can be reused or composed
3. Only introduce new tokens or components if nothing existing fits

New tokens or components introduced by this story must conform to the existing system's patterns — not start a parallel system.

## Checklist

1. **Read `/.agentic-sdlc/existing-system.md`** — identify existing UI framework and component library
2. **Read existing `/.agentic-sdlc/design-system.md`** (if present) or inspect existing components
3. **Answer design questions** (one at a time):
   - Does this story introduce any new UI components? If so, can they be composed from existing ones?
   - Are there accessibility implications? (new form fields, modals, dynamic content, focus management)
   - Does this story change any existing visual contract visible to users?
   - Are there responsive or device-specific concerns?
4. **Document delta** — only new tokens, only new components
5. **Update `/.agentic-sdlc/design-system.md`** — append delta section (do not overwrite)
6. **Update `/.agentic-sdlc/accessibility.md`** — append story-specific requirements
7. **Transition** — invoke `brownfield-tech-plan`

## Delta Design Format

Append to `/.agentic-sdlc/design-system.md`:

```markdown
## Story delta — [STORY-ID]: [Title] — [Date]

### New components introduced
| Component | States | Reuses existing | Notes |
|---|---|---|---|
| FileUploadDropzone | idle, dragging, uploading, error | Button, ProgressBar | Drag-and-drop not in existing system |

### New design tokens
| Token | Value | Rationale |
|---|---|---|
| color-upload-overlay | rgba(0,0,0,0.3) | Needed for drag overlay — no existing semi-transparent token |

### Accessibility additions
- FileUploadDropzone: `role="button"`, keyboard-activatable with Enter/Space, `aria-live` region for upload progress
- Error state: `aria-describedby` pointing to error message element
```

## Red Flags

| Thought | Reality |
|---|---|
| "I'll create a new design token for this one case" | New tokens fragment the system. Reuse or compose first. |
| "Accessibility can be handled in implementation" | Accessibility decisions are design decisions. Make them now. |
| "The existing components don't quite fit — I'll fork one" | Forking creates two maintenance burdens. Extend the existing one. |
| "This is a small UI change — no design needed" | Small changes to visible contracts still need to be consistent. Document them. |
