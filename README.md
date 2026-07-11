# Personal Skills

This repository contains personal [Agent Skills](https://agentskills.io)
compatible with any harness that supports the [spec](https://agentskills.io) (Claude Code, Pi, and others).
Each skill lives under `skills/<skill-name>/` and provides a `SKILL.md` entry point.

## Installation

Install this repository with `npx skills`:

```bash
npx skills add https://github.com/rangzen/skills
```

To update installed skills later:

```bash
npx skills update
```

For local development, you can also install from a checkout:

```bash
npx skills add /path/to/skills
```

## Skills

| Skill | Description |
| --- | --- |
| [`init-docs`](#init-docs) | Scaffolds a progressive-disclosure documentation base for a software project (`docs/`, `AGENTS.md`). |
| [`scoped-commits`](#scoped-commits) | Guides commit messages using a scope-first format instead of Conventional Commits. |

> `init-knowledge-directory` was merged into the `kp-init` skill in [rangzen/knowledge-project-skills](https://github.com/rangzen/knowledge-project-skills).

### `init-docs`

Scaffolds a progressive-disclosure documentation base for a software project.

Use it when you want to:
- initialize `docs/` for a repo
- create `AGENTS.md` and architecture/design/product docs
- set up a documentation structure without overwriting existing files

Typical prompts:
- `/init-docs`
- `set up docs for this project`
- `initialize the knowledge base for this repo`

### `scoped-commits`

Guides commit messages using a scope-first format instead of Conventional
Commits.

Format:

```text
scope: short description
```

Use it when you want help:
- writing a commit message
- defining commit conventions
- reviewing whether a commit title is well scoped

Typical prompts:
- `write a commit message for these changes`
- `what commit style should we use?`

## External Skills

Skills from [anthropics/skills](https://github.com/anthropics/skills) worth installing:

| Skill | Description |
| --- | --- |
| [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Create, modify, and measure agent skills. |
| [`pdf`](https://github.com/anthropics/skills/tree/main/skills/pdf) | Read, merge, split, fill, encrypt, and OCR PDF files. |
| [`docx`](https://github.com/anthropics/skills/tree/main/skills/docx) | Create, read, and edit Word documents. |
| [`xlsx`](https://github.com/anthropics/skills/tree/main/skills/xlsx) | Open, read, edit, and create spreadsheets (.xlsx, .csv, .tsv). |
| [`pptx`](https://github.com/anthropics/skills/tree/main/skills/pptx) | Work with PowerPoint files as input or output. |

Skills from [rangzen/knowledge-project-skills](https://github.com/rangzen/knowledge-project-skills):

| Skill | Description |
| --- | --- |
| [`kp-init`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-init) | Scaffold a new knowledge project: directory structure, `.knowledge-project` config, and stub files. |
| [`kp-source`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-source) | Add and track sources (PDF, URL, CSV, database) with ingestion dates and hashes. |
| [`kp-staging`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-staging) | Run LLM extractors over ingested sources and write structured JSON to `staging/`. |
| [`kp-query`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-query) | Query the knowledge base and save answers with provenance to `wiki/queries/`. |
| [`kp-wiki`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-wiki) | Build the navigable wiki: entity pages, glossary, wikilinks, and typed entry points. |

## Context

The `context/` directory contains personal context files that agents can load to understand who they are working with and how to act on behalf of Cédric.

| File | Purpose |
| --- | --- |
| [`context/AGENTS.md`](context/AGENTS.md) | General agent instructions following the [agents.md](https://agents.md) standard. Loaded by compatible agents automatically. |
| [`context/OPINIONS.md`](context/OPINIONS.md) | Cédric's engineering and product opinions. Agents read this when making technical decisions that benefit from his viewpoint. |
| [`context/VOICES.md`](context/VOICES.md) | Cédric's writing voice profile. Agents read this when writing or posting on his behalf. |

Run `scripts/link-context.sh` to symlink all context files into `~` and create `~/CLAUDE.md -> ~/AGENTS.md`.

Inspired by [Kun Chen](https://github.com/kunchenguid)'s approach to agent ergonomics and personal context design.

## Usage

These skills are trigger-based. After installation, invoke them by naming the
skill directly or by asking for the underlying task in natural language.

Examples:

```text
/init-docs
initialize a knowledge directory in this folder
write a scoped commit message for the current diff
```
