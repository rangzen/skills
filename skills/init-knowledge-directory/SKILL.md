---
name: init-knowledge-directory
description: >
  Initialize a knowledge-management workspace in the current directory. Use
  when the user wants a fixed knowledge-directory structure, empty .gitkeep
  files in each folder, a reusable `scripts/` directory, and an AGENTS.md file
  that defines how AI agents must treat sources, staging data, the wiki, root-
  level output documents, and generated scripts.
---

# Init Knowledge Directory

Create this structure at the project root:

- `sources/`
- `staging/`
- `wiki/`
- `scripts/`

Add an empty `.gitkeep` file inside each of those directories.

Create `AGENTS.md` at the project root with the exact English content below.

## Workflow

1. Work in the current directory.
2. Create the four directories if they do not already exist.
3. Create or overwrite these empty files:
   - `sources/.gitkeep`
   - `staging/.gitkeep`
   - `wiki/.gitkeep`
   - `scripts/.gitkeep`
4. Create or overwrite `AGENTS.md` with exactly this content:

```md
# AI Agent Directives for This Knowledge Directory

Follow the roles below strictly to preserve data integrity:

### sources/ (Read-Only)
- **Contents:** Raw documents, original PDFs, images, URL lists.
- **Golden rule:** NEVER MODIFY, DELETE, or WRITE into this directory. Only read from it during ingestion tasks.

### staging/ (Read / Write)
- **Contents:** Extracted text (raw Markdown), cleaned data, chunks for RAG.
- **Golden rule:** This directory is volatile and transitional. Clean formatting and remove noise so the text is easier to use. Keep an explicit trace of the original source filename.

### wiki/ (Read / Append / Update)
- **Contents:** The knowledge wiki (key concepts, entities, people).
- **Golden rule:** Act as an "Archivist." Every file should be highly connected with wiki links like `[[file_name]]`. Information must always be sourced back to `staging` or `sources`.

### Project root (Read / Write)
- **Contents:** Final documents created from the knowledge work.
- **Golden rule:** Final deliverables are created at the project root. Read `wiki` for concepts and `staging` for raw context before writing them.

### scripts/ (Read / Write)
- **Contents:** Reusable generated scripts and automation helpers.
- **Golden rule:** Store reusable scripts here only. All generated scripts must be Python scripts executed with `uv` so they do not pollute the rest of the environment.
```

## Output Rules

- Perform the file operations silently using file-manipulation tools.
- If write access is unavailable, generate one Bash script that performs the full setup.
- After completion, reply with exactly:

`✅ Knowledge directory initialized successfully`
