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

## Usage

These skills are trigger-based. After installation, invoke them by naming the
skill directly or by asking for the underlying task in natural language.

Examples:

```text
/init-docs
initialize a knowledge directory in this folder
write a scoped commit message for the current diff
```
