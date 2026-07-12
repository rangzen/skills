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
| [`youtube`](#youtube) | Composable toolkit for fetching YouTube metadata, transcripts, and transcript-backed summaries. |

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

### `youtube`

Composable toolkit for fetching YouTube metadata, transcripts, and
transcript-backed summaries.

Use it when you want to:
- fetch a YouTube video's metadata (title, duration, thumbnail, channel)
- download a video's transcript
- generate notes or a summary from a video

Typical prompts:
- `get metadata for this youtube video`
- `summarize this youtube video`
- `download the transcript of ...`
- `take notes on ...`

## External Skills

Omit `--skill <name>` to open an interactive multi-select picker for the whole repo:

```sh
npx skills add anthropics/skills
```

Skills from [anthropics/skills](https://github.com/anthropics/skills) worth installing:

| Skill | Description | Install |
| --- | --- | --- |
| [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Create, modify, and measure agent skills. | `npx skills add anthropics/skills --skill skill-creator` |
| [`pdf`](https://github.com/anthropics/skills/tree/main/skills/pdf) | Read, merge, split, fill, encrypt, and OCR PDF files. | `npx skills add anthropics/skills --skill pdf` |
| [`docx`](https://github.com/anthropics/skills/tree/main/skills/docx) | Create, read, and edit Word documents. | `npx skills add anthropics/skills --skill docx` |
| [`xlsx`](https://github.com/anthropics/skills/tree/main/skills/xlsx) | Open, read, edit, and create spreadsheets (.xlsx, .csv, .tsv). | `npx skills add anthropics/skills --skill xlsx` |
| [`pptx`](https://github.com/anthropics/skills/tree/main/skills/pptx) | Work with PowerPoint files as input or output. | `npx skills add anthropics/skills --skill pptx` |

Skills from [rangzen/knowledge-project-skills](https://github.com/rangzen/knowledge-project-skills):

| Skill | Description | Install |
| --- | --- | --- |
| [`kp-init`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-init) | Scaffold a new knowledge project: directory structure, `.knowledge-project` config, and stub files. | `npx skills add rangzen/knowledge-project-skills --skill kp-init` |
| [`kp-source`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-source) | Add and track sources (PDF, URL, CSV, database) with ingestion dates and hashes. | `npx skills add rangzen/knowledge-project-skills --skill kp-source` |
| [`kp-staging`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-staging) | Run LLM extractors over ingested sources and write structured JSON to `staging/`. | `npx skills add rangzen/knowledge-project-skills --skill kp-staging` |
| [`kp-query`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-query) | Query the knowledge base and save answers with provenance to `wiki/queries/`. | `npx skills add rangzen/knowledge-project-skills --skill kp-query` |
| [`kp-wiki`](https://github.com/rangzen/knowledge-project-skills/tree/main/skills/kp-wiki) | Build the navigable wiki: entity pages, glossary, wikilinks, and typed entry points. | `npx skills add rangzen/knowledge-project-skills --skill kp-wiki` |

Skills from [kunchenguid/lavish-axi](https://github.com/kunchenguid/lavish-axi) by [Kun Chen](https://github.com/kunchenguid):

| Skill | Description | Install |
| --- | --- | --- |
| [`lavish`](https://github.com/kunchenguid/lavish-axi) | Turn complex or visual agent responses into rich, reviewable HTML artifacts the user can annotate and send feedback on. | `npx skills add kunchenguid/lavish-axi --skill lavish` |

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
