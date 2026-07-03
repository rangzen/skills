# Personal Skills

This repository contains personal [Agent Skills](https://agentskills.io)
bundles for Codex and other compatible agents. Each skill lives under
`skills/<skill-name>/` and provides a `SKILL.md` entry point.

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

### `init-knowledge-directory`

Creates a fixed knowledge-workspace layout with:
- `sources/`
- `staging/`
- `wiki/`
- `scripts/`
- `AGENTS.md`

Use it when you want a non-code knowledge directory with strict rules around
raw sources, staging data, wiki content, and reusable scripts.

Typical prompts:
- `initialize a knowledge directory here`
- `set up sources, staging, wiki, and scripts`

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

## Usage

These skills are trigger-based. After installation, invoke them by naming the
skill directly or by asking for the underlying task in natural language.

Examples:

```text
/init-docs
initialize a knowledge directory in this folder
write a scoped commit message for the current diff
```
