---
name: scoped-commits
description: 'Guide commit message writing using scope-first convention (anti-Conventional Commits). Use when writing or reviewing commit messages, setting up commit conventions, or asked about git commit style. Trigger on: "commit message", "git commit", "how to commit", "commit convention", "commit style".'
---

# scoped-commits

Write commit messages using the **scope-first** format — the same convention used by Linux, Git, Go, and FreeBSD. Do not use Conventional Commits (`feat:`, `fix:`, `chore:`, etc.).

## Format

```
scope: short description of what changed
```

**Blank line, then optional body** if the why isn't obvious from the subject.

## Rules

1. **Scope first, always.** The scope (which part of the codebase changed) is the most important piece of information. Reviewers, debuggers, and incident responders scan by scope.

2. **Pick scope from the project's structure.** Use whatever is self-evident: subsystem name, package path, service name, component name, directory. Examples:
   - Linux: `i2c: virtio: mark device ready before registering the adapter`
   - Go: `net/http/cookiejar: add godoc links`
   - Git: `gitlab-ci: update macOS image`

3. **Let the description carry the type.** "add", "remove", "fix", "update", "refactor" in the description is enough. No need for a separate type prefix — it wastes space and is often inaccurate.

4. **Scope is required; body is optional.** A commit without a scope is like a sentence without a subject.

5. **Keep subject under ~72 chars.** The scope eats some of that — be concise in the description.

6. **Avoid stuffing ticket numbers into the scope.** `JIRA-123: fix bug` hides what changed. Put ticket refs in the body instead.

7. **Separate the commit log from the changelog.** Commit messages are for developers tracing code changes — not for end-users. Don't write commit messages to double as release notes.

## Why not Conventional Commits?

- `feat(auth): add OAuth` — type before scope inverts priority. You have to parse past the type to reach what matters.
- Predefined types (`feat`, `fix`, `chore`, `refactor`…) don't fit all changes and create awkward commits that don't belong anywhere.
- Automated changelog generation from commit types produces results that serve neither developers nor end-users well.
- Automated semver bumping from commit types breaks on reverts, subtle breakages, and retroactive fixes.
- Type metadata in subjects enables security risks (build automation triggered by commit title can be spoofed).

## Good examples

```
auth: replace bcrypt with argon2 for password hashing
api/users: add pagination to list endpoint
ui/sidebar: fix collapse animation on mobile
infra: upgrade postgres to 16
parser: handle empty input without panicking
```

## Bad examples (avoid)

```
feat(auth): add OAuth          ← type before scope
fix: broken login              ← no scope
JIRA-456: update dependencies  ← ticket as scope
chore: misc cleanup            ← vague, no scope
```

## When writing a commit for the user

- Infer the scope from the files changed (directory, package, module, component).
- Write the description as an imperative verb phrase ("add", "fix", "remove", "update").
- Add a body only if the *why* isn't obvious from the diff or the subject line.
- Never add a type prefix.

## References

See **`references/sources.md`** for the origin article, the scopedcommits.com standard, and links to real commit logs from Linux, Git, Go, FreeBSD, and NixOS.
