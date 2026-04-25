# Multi-platform Installation Plan

> **Status:** Approved
> **Owner:** TBD
> **Last updated:** 2026-04-25
> **Audience:** End users who want to install Agentic SDLC into their own projects

## Execution update

As of 2026-04-25, the repository has already completed most of the install-doc cleanup described below:

- `docs/installation.md` is now the canonical install guide
- `.codex/INSTALL.md` has been rewritten to use clone + editable install + `asdlc init`
- `.opencode/INSTALL.md` now exists and mirrors the Codex fetch/bootstrap flow
- `docs/platforms/codex.md`, `docs/platforms/opencode.md`, and `docs/platforms/cursor.md` now point at the canonical install flow
- root entry-point docs (`CLAUDE.md`, `AMP.md`, `ANTIGRAVITY.md`, `GEMINI.md`) no longer present direct PyPI installation as the supported path
- the clone-based install flow has been verified in a fresh virtual environment
- package metadata has been hardened so `python -m build` and `python -m twine check dist/*` pass cleanly
- the unverified Claude plugin manifest has been removed from the supported repo surface; Claude now uses the same documented manual install path as the other supported agents

Chosen path from here:

1. Installation-plan cleanup inside the repo is complete
2. Keep marketplace work out of scope for this iteration
3. Move next into release prep for TestPyPI/PyPI, then update install docs once the publish path is real

Remaining in-repo gaps:

- none for the current pre-publish install-doc scope

## Goal

Provide first-class install instructions for Agentic SDLC across the four prioritized coding agents — **Claude Code, Codex, OpenCode, and Cursor** — using the Superpowers repository as inspiration for the multi-platform install experience.

Superpowers is the model for **how the install guide is organized**: one clear section per agent, marketplace paths where available, and fetch/manual fallbacks where needed.

Agent Skills is the standard for **what gets installed**: skills must end up in `.agents/skills/<skill-name>/SKILL.md` relative to the target project root, with valid `name` and `description` frontmatter.

This plan is about the **install and entry-point documentation layer**:
- how an end user gets the framework into a project
- which files each agent should read at startup
- which repo docs should be treated as the source of truth

It is **not** a runtime feature plan for the CLI or the skills themselves.

Every install path must work from a **local clone**. The package is not yet on PyPI, so `pip install agentic-sdlc` must not be presented as the primary install path.

---

## Confirmed answers (from product owner)

| # | Question | Answer |
|---|---|---|
| Q1 | Is `agentic-sdlc` published on PyPI? | **No.** Local clone only for now. All `pip install agentic-sdlc` references must be replaced or clearly marked as future-state only. |
| Q2 | Public GitHub URL? | `https://github.com/salauddin-ee/agentic-sdlc` |
| Q3 | What about `.claude-plugin/plugin.json`? | Treat it as optional platform packaging. Fix it only if we can verify the official Claude Code plugin spec; otherwise remove it from the core install path. |
| Q4 | Prioritized platforms? | **Claude Code, Codex, OpenCode, Cursor.** Amp / Antigravity / Gemini / Copilot are deprioritized for new platform work, but stale install instructions must still be cleaned up. |
| Q5 | Audience? | End users (not framework contributors) |
| Q6 | Verification? | Each install command must be verified in a fresh shell as part of Phase 1 |

---

## Audit: what we already support

| Platform | Existing artifact | Status |
|---|---|---|
| **Claude Code** ⭐ | `.claude-plugin/plugin.json` + `CLAUDE.md` | ⚠️ Manifest uses non-standard fields; not on marketplace |
| **OpenAI Codex** ⭐ | `.codex/INSTALL.md` | ⚠️ References deprecated install flow (`scripts/init-context.sh`) and points users to roadmap docs instead of canonical install docs |
| **OpenCode** ⭐ | None | ❌ Not supported |
| **Cursor** ⭐ | None | ❌ Not supported |
| Local clone (universal) | `pyproject.toml`, `asdlc init` command | ✅ Works (after `pip install -e .`) |
| Amp | `AMP.md` | ⚠️ Stale `pip install agentic-sdlc` instruction; deprioritized |
| Antigravity | `ANTIGRAVITY.md` | ⚠️ Stale `pip install agentic-sdlc` instruction; deprioritized |
| Gemini CLI | `GEMINI.md` | ⚠️ Stale `pip install agentic-sdlc` instruction; deprioritized |
| GitHub Copilot CLI | None | ❌ Not in scope |

⭐ = Phase 3 focus

### Bugs found during audit

1. `.codex/INSTALL.md` references `scripts/init-context.sh` — **deprecated; use `asdlc init` instead**.
2. `.codex/INSTALL.md` sends users to `docs/future-platforms.md` — **wrong destination; use `docs/installation.md` for install guidance**.
3. `.claude-plugin/plugin.json` uses fields (`skills`, `entrypoint`) that need verification against the official Claude Code plugin spec before being treated as supported.
4. **All entry-point docs assume `pip install agentic-sdlc` works — it does not (not on PyPI).**

---

## Conceptual model

The framework is **two things**:
1. A **Python CLI** (`asdlc init/serve/update-agents`) that scaffolds project structure
2. A **skills library** (`src/agentic_sdlc/skills/*.md`) that agents read

Until PyPI publish, both are delivered together via **local clone + `pip install -e .`**. Plugin manifests (Claude/Cursor) only ship the skills.

The Agent Skills compatibility target is:

```text
<target-project>/.agents/skills/<skill-name>/SKILL.md
```

`asdlc init` must create that layout automatically. Manual installs must copy `src/agentic_sdlc/skills/` into that exact location.

### Two supported install flows

| Flow | When to use | Requires Python? |
|---|---|---|
| **A. Clone + pip install** (recommended) | 90% of users — single command, CLI auto-creates `docs/` and `.agents/skills/` in target project | Yes |
| **B. Clone + manual copy** (fallback) | Users without Python, on locked-down machines, or just trying skills quickly | No |

**Important:** Flow B is **documentation only** — no new scripts or code. We tell users which `cp` and `mkdir` commands to run themselves. The repo already has everything they need (`src/agentic_sdlc/skills/`, `AGENTS.md`).

---

## Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Users try `pip install agentic-sdlc` and it fails | **Certain** | High | Replace all references with clone-based install in Phase 1 |
| Claude Code plugin spec changes or differs from our assumptions | Medium | Medium | Keep plugin manifest optional until verified; document manual install as canonical |
| Cursor has no formal manifest format we control | Medium | Medium | Use `.cursorrules` or pip-style install; document as best-effort |
| OpenCode fetch URL hard-coded to `main` branch | Low | Low | Document this is acceptable until release tagging |
| Documentation drift across entry-point docs | High | Medium | Single source of truth: `docs/installation.md`. Other docs link to it. |
| Obsolete install files keep misleading users | High | Medium | Delete or redirect old install artifacts that are not part of the chosen install story |
| Future PyPI publish breaks docs | Low | Low | When PyPI ships, add pip install as Option A and demote clone install |

---

## Phased execution plan

### Phase 1 — Fix what's broken (and confirm reality)

**Effort:** ~1.5 hours

| # | File | Action |
|---|---|---|
| 1.1 | `.codex/INSTALL.md` and `docs/platforms/codex.md` | Create or update the files so they point at real repo paths and a local-clone install flow (`git clone` + `pip install -e .` + `asdlc init`) |
| 1.2 | `.claude-plugin/plugin.json` | Decide: **(a)** fix to match official Claude plugin spec after verification; **(b)** move to a more accurate path if Claude expects it elsewhere; **(c)** delete or ignore it if it cannot be made valid. Do not make it part of the core install path unless verified. |
| 1.3 | `AMP.md`, `CLAUDE.md`, `GEMINI.md`, `ANTIGRAVITY.md`, `docs/platforms/*.md`, and packaged bootstrap docs under `src/agentic_sdlc/core/` | Replace `pip install agentic-sdlc` with **clone + `pip install -e .`** flow in the repo docs and any packaged entry-point docs that are still part of the runtime surface. Add a TODO note: "switch to PyPI install once published." |
| 1.4 | All install commands | Verify each runs successfully in a fresh venv before marking phase complete |

**Done when:**
- No file references a path that does not exist (`rg` clean)
- `.claude-plugin/plugin.json` is either validated, moved, deleted, or explicitly excluded from the core install path — with rationale documented
- Every entry-point doc has a verified working install command
- Each install command has been run end-to-end in a fresh shell
- `asdlc init` and manual-copy flows both install skills to `.agents/skills/<skill-name>/SKILL.md`

**Verification:**
```bash
# 1. No broken file refs
rg "scripts/init-context.sh" . \
  --glob '!docs/sdlc/epics/installation-plan.md' \
  --glob '!task.md' \
  --glob '!.venv/**'

# 2. No remaining "pip install agentic-sdlc" (since not on PyPI)
rg "pip install agentic-sdlc\b" . \
  --glob '!docs/sdlc/epics/installation-plan.md' \
  --glob '!.venv/**'

# 3. Claude manifest decision is documented
rg ".claude-plugin/plugin.json" docs/installation.md docs/platforms README.md

# 4. Fresh-venv smoke test
python3 -m venv /tmp/asdlc-test
source /tmp/asdlc-test/bin/activate
pip install -e .
asdlc --help
asdlc init /tmp/asdlc-init-test
deactivate && rm -rf /tmp/asdlc-test /tmp/asdlc-init-test
```

### Phase 1.5 — Remove obsolete install artifacts

**Effort:** ~30 min

After Phase 1 identifies the canonical install paths, remove or reduce old installation artifacts that are no longer needed.

| Artifact | Decision |
|---|---|
| `.claude-plugin/plugin.json` | Keep only if verified against the official Claude Code plugin spec; otherwise delete it or move it out of the supported install path |
| `.codex/INSTALL.md` | Keep, because Codex/OpenCode-style fetch instructions are useful; rewrite it to use `asdlc init` |
| `docs/platforms/*.md` | Either rewrite as short pointers to `docs/installation.md` or keep only platform-specific behavior notes with no duplicated install commands |
| `docs/future-platforms.md` | Keep only if it remains a roadmap document; remove install instructions from it |
| Root `AMP.md`, `CLAUDE.md`, `GEMINI.md`, `ANTIGRAVITY.md` | Keep if these are copied by `asdlc init` or used by agents; otherwise reduce them to startup instructions and point install steps to `docs/installation.md` |
| `src/agentic_sdlc/core/AGENTS.md` | Keep, because this is the packaged bootstrap file copied by `asdlc init` |

**Do not edit or delete generated/local environment files** such as `.venv/`; they are not source install artifacts.

**Done when:**
- No obsolete install file presents a separate unsupported install path
- No root/platform/core doc tells users to run `pip install agentic-sdlc` while PyPI is unavailable
- Any removed file has either a replacement path or a documented rationale
- Git status shows only intentional source/doc changes, not virtualenv or generated package edits

**Verification:**
```bash
# No stale install commands in source docs
rg "pip install agentic-sdlc|scripts/init-context.sh" . \
  --glob '!docs/sdlc/epics/installation-plan.md' \
  --glob '!task.md' \
  --glob '!.venv/**'

# No duplicated install docs except the canonical install guide and approved fetch files
rg "## Installation|# Installation" README.md docs .codex \
  --glob '!docs/sdlc/epics/installation-plan.md' \
  --glob '!.venv/**'
```

### Phase 2 — Centralize install docs

**Effort:** ~1 hour

Rewrite `docs/installation.md` in the Superpowers style with one section per **prioritized** platform. Deprioritized platforms get a single "manual install" line each.

**Structure:**
```
# Installation

> Installation differs by platform. Pick your agent below.
> Note: agentic-sdlc is not yet on PyPI. All paths use a local clone.

## Flow A — Recommended (clone + pip + asdlc init)
git clone https://github.com/salauddin-ee/agentic-sdlc.git
cd agentic-sdlc
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
asdlc init /path/to/your/project

## Flow B — Without Python (manual copy)
> Use this if you don't have Python or just want skills quickly.
> No CLI; you run the copy commands yourself.

git clone https://github.com/salauddin-ee/agentic-sdlc.git
mkdir -p /path/to/your-project/.agents
cp -r agentic-sdlc/src/agentic_sdlc/skills /path/to/your-project/.agents/skills
cp agentic-sdlc/AGENTS.md /path/to/your-project/AGENTS.md
mkdir -p /path/to/your-project/docs/{architecture/adrs,product/features,sdlc/stories,sdlc/workspaces,sdlc/test-plans,sdlc/retrospectives}

## Claude Code           ← Phase 3 quick win
## OpenAI Codex CLI/App  ← Phase 3 quick win
## OpenCode              ← Phase 3 quick win
## Cursor                ← Phase 3 quick win

## Other agents (manual install via Flow A or Flow B above)
- Amp
- Antigravity
- Gemini CLI
- GitHub Copilot CLI

## Local development (contributors)
pip install -e ".[dev]"
```

**Done when:**
- Every prioritized platform has a section with at least one verified command
- Every deprioritized platform is listed with a pointer to the universal section
- README and `docs/getting-started.md` link to this doc instead of duplicating install steps
- Existing `docs/platforms/*.md` pages either link to `docs/installation.md` or are updated to match it

**Verification:**
```bash
rg "docs/installation.md" README.md docs/getting-started.md
```

### Phase 3 — Add quick wins for prioritized platforms

**Effort:** ~2 hours

| Platform | Required artifact | Notes |
|---|---|---|
| **Claude Code** | Documented manual flow in `docs/installation.md`; optional `.claude-plugin/plugin.json` only if verified against the official spec | Do not block manual install on plugin packaging |
| **Codex** | Updated `.codex/INSTALL.md` referencing real files; section in `docs/installation.md` | Already has structure, just needs Phase 1 fixes wired up |
| **OpenCode** | New `.opencode/INSTALL.md` with clone + install steps; Superpowers-style fetch URL using `https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.opencode/INSTALL.md` | Modeled after `.codex/INSTALL.md` |
| **Cursor** | Cursor section in `docs/installation.md` using `.cursorrules` or pip install workaround | No formal manifest format; document the best available path |

**Done when:**
- Each prioritized platform has a working install command in `docs/installation.md`
- OpenCode fetch URL returns valid markdown after merge
- Each command verified in the appropriate agent (or pip path verified for Cursor)

**Verification:**
```bash
# OpenCode (after merge to main)
curl -sf https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.opencode/INSTALL.md | head

# Codex install path
python3 -m venv /tmp/asdlc-codex-test
source /tmp/asdlc-codex-test/bin/activate
pip install -e .
asdlc init /tmp/asdlc-codex-project
test -f /tmp/asdlc-codex-project/AGENTS.md
test -f /tmp/asdlc-codex-project/.agents/skills/asdlc-using-agentic-sdlc/SKILL.md
```

### Phase 4 — Marketplace publishing (out of scope for this iteration)

**Effort:** Per-platform 1-3 days each, mostly waiting on external review.

| Marketplace | Submission process | Blockers |
|---|---|---|
| Claude Code official | Anthropic plugin marketplace PR | Need Anthropic contact + spec compliance + PyPI publish |
| Codex plugin store | OpenAI plugin submission | Need OpenAI developer account |
| Cursor marketplace | Cursor PR or in-app submission | Need Cursor publisher account |

For each, document a placeholder in `docs/installation.md`: *"Marketplace install coming soon — use the manual install above for now."*

### Phase 5 — Update README

**Effort:** ~15 min

Replace the README install section with:
- A 3-line quick-start using the universal clone+install path
- A link to `docs/installation.md` for per-platform options

**Done when:**
- README install section is no more than ~10 lines
- The quick-start command is the universal `git clone … && pip install -e . && asdlc init`
- All deeper install paths live in `docs/installation.md`

---

## Recommended scope for this iteration

**Phase 1 + Phase 1.5 + Phase 2 + Phase 3 + Phase 5** — fix bugs, remove obsolete install artifacts, centralize docs, add Claude/Codex/OpenCode/Cursor quick wins, polish README.

**Total effort:** ~4.5 hours

**Skip Phase 4** until PyPI publish + marketplace submissions are scheduled as separate work.

---

## Global success criteria

- A user on **Claude Code, Codex, OpenCode, or Cursor** finds a single command in `docs/installation.md` that installs Agentic SDLC.
- Both **Flow A (pip)** and **Flow B (manual copy)** are documented and work against a local clone (no PyPI dependency).
- Installed skills conform to Agent Skills layout: `.agents/skills/<skill-name>/SKILL.md`.
- All referenced files, scripts, and URLs exist and resolve.
- Obsolete install artifacts are removed or reduced to pointers to `docs/installation.md`.
- The Claude plugin manifest is either verified, relocated, removed, or explicitly documented as optional packaging — with rationale.
- README and `getting-started.md` direct users to the central install doc.
- Deprioritized platforms (Amp, Antigravity, Gemini, Copilot) still have a working install path via Flow A or Flow B.
- Each install command was verified in a fresh shell or fresh agent session before sign-off.
