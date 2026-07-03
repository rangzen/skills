---
name: init-docs
description: Scaffolds the OpenAI harness-style docs/ knowledge base for a project. Use this skill whenever the user types /init-docs, asks to "set up docs", "initialize the knowledge base", "scaffold the docs structure", "set up AGENTS.md", or starts a new project and wants documentation structure. Always use this skill proactively when a project has no docs/ directory, no AGENTS.md, and the user asks about documentation setup.
---

# init-docs

Scaffolds a structured `docs/` knowledge base following the progressive-disclosure model: a small stable AGENTS.md entry point that maps to deeper sources of truth.

## Step 1 — Read the project

Before writing anything, infer the project's identity. Read whatever exists:

- `CLAUDE.md`, `README.md`, `README` (project name, purpose, stack)
- `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod` (language, dependencies)
- `src/`, `app/`, `lib/` directory listings (architecture clues)
- Existing `AGENTS.md` or `docs/` (already partially set up?)

Extract: **project name**, **one-sentence purpose**, **primary language/stack**, **key domains or packages** (if inferable). You'll use these to fill in the templates below — don't leave placeholders where you have real information.

## Step 2 — Check what exists

For every file you're about to create, check if it already exists. **Never overwrite an existing file.** Skip it and note it in your final report.

Files to check:
```
AGENTS.md
ARCHITECTURE.md
docs/DESIGN.md
docs/FRONTEND.md
docs/PLANS.md
docs/PRODUCT_SENSE.md
docs/QUALITY_SCORE.md
docs/RELIABILITY.md
docs/SECURITY.md
docs/design-docs/index.md
docs/design-docs/core-beliefs.md
docs/exec-plans/tech-debt-tracker.md
docs/product-specs/index.md
```

## Step 3 — Create the files

Create each missing file using the templates below. Fill in project-specific details where you have them; leave guiding prompts where you don't.

---

### AGENTS.md (repo root)

Keep this under 100 lines. It is a MAP — no inline content, only pointers. Every section title should link somewhere.

```markdown
# AGENTS.md
> Entry point for AI agents. This file is a map — details live in docs/. Keep it under 100 lines.

## What is this project?
[One sentence: what it does and for whom.]

## Architecture
See [ARCHITECTURE.md](ARCHITECTURE.md) for the domain map and package layering.

## Documentation index

| Document | Purpose |
|---|---|
| [docs/DESIGN.md](docs/DESIGN.md) | Design system and UI conventions |
| [docs/FRONTEND.md](docs/FRONTEND.md) | Frontend patterns and component conventions |
| [docs/PLANS.md](docs/PLANS.md) | Overview of active plans and planning conventions |
| [docs/PRODUCT_SENSE.md](docs/PRODUCT_SENSE.md) | User goals and product context |
| [docs/QUALITY_SCORE.md](docs/QUALITY_SCORE.md) | Domain quality grades and gap tracking |
| [docs/RELIABILITY.md](docs/RELIABILITY.md) | SLOs, failure modes, on-call runbook |
| [docs/SECURITY.md](docs/SECURITY.md) | Security posture and known risks |

## Design docs
Catalogued in [docs/design-docs/index.md](docs/design-docs/index.md).
Core agent-first operating principles: [docs/design-docs/core-beliefs.md](docs/design-docs/core-beliefs.md).

## Plans
- Active: [docs/exec-plans/active/](docs/exec-plans/active/)
- Completed: [docs/exec-plans/completed/](docs/exec-plans/completed/)
- Tech debt: [docs/exec-plans/tech-debt-tracker.md](docs/exec-plans/tech-debt-tracker.md)

## Product specs
Catalogued in [docs/product-specs/index.md](docs/product-specs/index.md).

## External references
llms.txt files and external tool references: [docs/references/](docs/references/)

## Key conventions
<!-- List 3–5 project-specific conventions agents must know.
     Examples: "Use X for Y", "Run Z before committing", "Never do W" -->
- [Add convention 1]
- [Add convention 2]
```

---

### ARCHITECTURE.md (repo root)

```markdown
# Architecture

## Overview
[Describe the system in 2–3 sentences: what it does, how the major parts relate.]

## Domain map

| Domain | Package / path | Responsibility |
|---|---|---|
| [domain] | `src/[path]` | [what it owns] |

## Package layering
<!-- Describe dependency rules between layers.
     Example: "UI may import from core but not from infra." -->

## Key data flows
<!-- Describe 1–3 important request/data flows through the system. -->

## External dependencies
| Service | Purpose | Docs |
|---|---|---|
| [service] | [why] | [link] |

## Decision log
<!-- Link to design-docs that explain major architectural decisions. -->
See [docs/design-docs/index.md](docs/design-docs/index.md).
```

---

### docs/DESIGN.md

```markdown
# Design

## Design system
<!-- What design system or component library is used? Custom? Tailwind? shadcn? -->

## Visual language
<!-- Colors, typography, spacing tokens. Link to a reference if one exists. -->

## Component conventions
<!-- How are components structured? Where do they live? Naming rules? -->

## UX principles
<!-- 3–5 core UX principles that guide design decisions in this project. -->
```

---

### docs/FRONTEND.md

```markdown
# Frontend

## Stack
<!-- Framework, routing, state management, styling approach. -->

## Directory structure
<!-- Where do pages, components, hooks, utils live? -->

## Data fetching
<!-- How does the frontend talk to the backend? REST, GraphQL, tRPC, server components? -->

## Conventions
<!-- Naming, file co-location, import order, anything non-obvious. -->

## Testing
<!-- How is frontend code tested? What's the coverage expectation? -->
```

---

### docs/PLANS.md

```markdown
# Plans

Plans are first-class artifacts. Small changes use ephemeral conversation context. Complex work uses exec-plans checked into the repo.

## How to create a plan
1. For small changes (< 1 day): plan in conversation, no file needed.
2. For complex work: create `docs/exec-plans/active/<name>.md` using the template below.
3. On completion: move to `docs/exec-plans/completed/`.

## Exec-plan template
\`\`\`markdown
# Plan: [title]
**Status**: active | completed | blocked
**Started**: YYYY-MM-DD

## Goal
[What done looks like.]

## Steps
- [ ] Step 1
- [ ] Step 2

## Decision log
| Date | Decision | Rationale |
|---|---|---|

## Progress log
| Date | Update |
|---|---|
\`\`\`

## Active plans
See [exec-plans/active/](exec-plans/active/).

## Completed plans
See [exec-plans/completed/](exec-plans/completed/).

## Tech debt
See [exec-plans/tech-debt-tracker.md](exec-plans/tech-debt-tracker.md).
```

---

### docs/PRODUCT_SENSE.md

```markdown
# Product sense

## Who is this for?
<!-- Describe the primary user. Their job, context, pain points. -->

## What problem does it solve?
<!-- The core problem in one paragraph. -->

## Success looks like
<!-- How do we know the product is working? What do users do differently? -->

## Non-goals
<!-- What are we explicitly not building? -->

## Open questions
<!-- Product-level questions that are unresolved. -->
```

---

### docs/QUALITY_SCORE.md

```markdown
# Quality score

Tracks quality grades per domain. Updated when a domain improves or regresses.

## Grading scale
- **A** — Excellent coverage, no known gaps
- **B** — Good, minor gaps
- **C** — Adequate, known gaps being tracked
- **D** — Significant gaps, active work needed
- **F** — Broken or untested

## Scores

| Domain | Grade | Notes | Last reviewed |
|---|---|---|---|
| [domain] | ? | Not yet graded | — |

## Gap tracker
<!-- List specific known gaps not covered by the grade above. -->
```

---

### docs/RELIABILITY.md

```markdown
# Reliability

## SLOs
<!-- Service level objectives. Uptime, latency, error rate targets. -->

## Failure modes
<!-- Known ways the system can fail and how each is handled. -->

## On-call runbook
<!-- What to do when something breaks. Key dashboards, alerts, escalation path. -->

## Dependencies and risks
<!-- External services we depend on and what happens if they go down. -->
```

---

### docs/SECURITY.md

```markdown
# Security

## Threat model
<!-- Who might attack this? What are they after? What's the blast radius? -->

## Auth and authorization
<!-- How are users authenticated? What are the authorization rules? -->

## Data classification
<!-- What sensitive data does the system handle? How is it protected? -->

## Known risks
<!-- Security risks that are accepted, deferred, or being mitigated. -->

## Security checklist
<!-- Link to or embed a checklist for common security reviews. -->
```

---

### docs/design-docs/index.md

```markdown
# Design docs index

All significant technical decisions are catalogued here with verification status.

| Doc | Status | Verified against code? | Summary |
|---|---|---|---|
| [core-beliefs.md](core-beliefs.md) | active | — | Agent-first operating principles |

## Verification status key
- **verified** — doc matches current code behavior
- **stale** — doc may not reflect current code, needs review
- **draft** — not yet verified
```

---

### docs/design-docs/core-beliefs.md

```markdown
# Core beliefs

These are the operating principles that guide agent behavior in this project. They are non-negotiable defaults — override only with explicit justification in a design doc.

## Agent-first
<!-- Agents operate without external context. Everything they need is in the repo. -->
1. The docs/ directory is the system of record. Code is truth; docs explain why.
2. AGENTS.md is the entry point. It maps; it does not explain.
3. Plans are artifacts. Complex work is captured in exec-plans, not conversation history.

## [Add project-specific beliefs]
<!-- Examples: "Prefer explicit over implicit", "Fail loudly", "No magic defaults" -->
```

---

### docs/exec-plans/tech-debt-tracker.md

```markdown
# Tech debt tracker

Known debt that is accepted and deferred. Each entry has a cost and a trigger for when to pay it down.

| Item | Area | Cost | Trigger to fix | Added |
|---|---|---|---|---|
| [example] | [domain] | [low/med/high] | [when X happens] | YYYY-MM-DD |
```

---

### docs/product-specs/index.md

```markdown
# Product specs index

| Spec | Status | Summary |
|---|---|---|
| [example.md](example.md) | draft | [what it covers] |

## Status key
- **draft** — being written, not approved
- **approved** — agreed on, implementation may be in progress
- **shipped** — implemented and verified
- **deprecated** — no longer relevant
```

---

## Step 4 — Create empty-directory placeholders

Create `.gitkeep` files in directories that must exist but start empty:
- `docs/exec-plans/active/.gitkeep`
- `docs/exec-plans/completed/.gitkeep`
- `docs/generated/.gitkeep`
- `docs/references/.gitkeep`

## Step 5 — Report

Print a summary:

```
✓ Created: AGENTS.md
✓ Created: ARCHITECTURE.md
✓ Created: docs/DESIGN.md
  ... (all created files)
⊘ Skipped: docs/SECURITY.md (already exists)
  ... (all skipped files)

Done. Start by filling in AGENTS.md — everything else can be discovered from there.
```

## Guiding principles (don't forget)

- **Never overwrite.** If a file exists, skip it. Don't merge, don't append.
- **Fill in what you know.** Don't leave `[project name]` when you read it from `package.json`.
- **AGENTS.md is a map.** If you find yourself writing content into AGENTS.md instead of a pointer, stop and put the content in the right doc instead.
- **Stubs guide, not lorem ipsum.** Every placeholder should tell the author what belongs there.
