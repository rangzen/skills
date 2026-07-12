---
name: youtube
description: Work with YouTube videos - fetch metadata (title, duration, thumbnail, channel), download a transcript, or generate a transcript-backed summary. Use for any YouTube URL when the user wants notes, a summary, metadata, key points, or the raw transcript. Also reach for this any time you're about to write about a video's content from its title alone: YouTube pages render client-side so a plain fetch only returns page boilerplate.
---

# YouTube skill

Composable toolkit for working with YouTube videos.
Each script is self-contained and can be used independently or chained.

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) installed (scripts declare inline PEP 723
  dependencies - `uv run` installs them on the fly, no project setup needed).
- An OpenRouter API key, only for `make_resume.py`.
  Set `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` as environment variables,
  in a `.env` in the working directory, or in a `.env` in this skill's own
  directory (copy `.env.example` there) for a personal default.

## Scripts

### Metadata only (no LLM, no API key)

```bash
uv run scripts/get_metadata.py <youtube-url-or-id> [output_dir]
```

Writes `metadata.json` into the video's output directory and prints a
human-readable summary with title, channel, duration, upload date, view
count, and thumbnail URL.
Works even when no transcript is available (live streams, etc.).

### Transcript only (no LLM, no API key)

```bash
uv run scripts/download_transcript.py <youtube-url-or-id> [output_dir]
```

Downloads the video's captions and saves them as `transcript.txt` and
`transcript.json` in the video's output directory.

### Summary from transcript (LLM via OpenRouter)

```bash
uv run scripts/make_resume.py <video-dir-or-url-or-id> [--language english] [--base-dir ./db]
```

Reads an existing `transcript.txt`, calls the configured OpenRouter model,
and writes a timestamped `resume-*.md` with YAML frontmatter and Markdown
content (overview, main points, key takeaways).
Run `download_transcript.py` first.

### Full pipeline - transcript + summary in one call

```bash
scripts/get_video_notes.sh <youtube-url-or-id> [language] [output_dir]
```

Chains `download_transcript.py` and `make_resume.py`.
`language` defaults to `english`; `output_dir` defaults to `./db` under the
current working directory.
Prints the path to the generated `resume-*.md` as its last line - read that
file.

## Output directory layout

All scripts use the same convention so they share a directory automatically:

```
<output_dir>/
  <video_id>-<slug>/
    metadata.json        # from get_metadata.py
    transcript.txt       # from download_transcript.py
    transcript.json      # from download_transcript.py
    resume-*.md          # from make_resume.py (timestamped, one per run)
```

`output_dir` defaults to `./db` relative to wherever you run the script,
so files land next to your notes rather than inside this skill's directory.

If a directory for the video already exists (e.g. from a prior script run),
subsequent scripts write into that same directory rather than creating a new
one.

## Using the notes

Once you have the resume, write the video's notes as bullets under its title
(linked to the video URL), pulling concrete points from the resume's "main
points" and "key takeaways" rather than copying the whole summary verbatim.
Match the structure the destination document already uses; don't impose a new
one.

Don't fabricate notes if the transcript fetch fails (no captions available) -
say so plainly rather than inventing plausible-sounding content from the
title alone.
