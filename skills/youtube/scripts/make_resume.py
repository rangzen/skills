#!/usr/bin/env -S uv run
# /// script
# dependencies = ["requests", "python-dotenv"]
# ///
"""Create a resume (summary) of a YouTube transcript.

Reads the transcript from <dir>/transcript.txt, sends it to an
OpenRouter chat model, and writes the resume to
<dir>/resume-<timestamp>-<model>.md (with YAML frontmatter).

The target may be given as:
  - a directory path containing transcript.txt (e.g. db/dQw4w9WgXcQ-slug)
  - a bare video id (resolved against ./db, or --base-dir if given)
  - a full YouTube URL (id extracted, then resolved the same way)

Environment (see .env.example):
    OPENROUTER_API_KEY   - your OpenRouter API key
    OPENROUTER_MODEL     - model id to use, e.g. "openai/gpt-4o-mini"

These are read from the environment. python-dotenv also auto-loads a
.env from the current directory or any parent (so a project-level .env
works), and this script additionally checks for a .env next to itself as
a fallback for a personal, skill-local key.

Usage:
    make_resume.py db/dQw4w9WgXcQ-slug [--language xx]
    make_resume.py dQw4w9WgXcQ
    make_resume.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

Each run writes a new timestamped file, so old resumes are preserved.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import find_dotenv, load_dotenv

OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"

DEFAULT_LANGUAGE = "english"

SYSTEM_PROMPT = (
    "You are an expert content summarizer. Given the transcript of a "
    "YouTube video, write a clear, well-structured resume (summary) in "
    "Markdown. Include: a short overview, the main points as a bulleted "
    "list, and key takeaways. Be faithful to the content and concise."
)


def extract_video_id(value: str) -> str:
    """Accept a bare video id or a YouTube URL and return the 11-char id."""
    patterns = [
        r"(?:v=|/)([A-Za-z0-9_-]{11})(?:[&?].*)?$",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/embed/([A-Za-z0-9_-]{11})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value
    raise ValueError(f"Could not extract video id from: {value}")


def resolve_transcript(base_dir: Path, value: str) -> tuple[Path | None, Path]:
    """Find transcript.txt for the given argument.

    Accepts a directory path, a bare video id, or a YouTube URL. Returns
    (transcript_path, dir) or (None, dir).
    """
    candidate = Path(value)
    if candidate.is_dir():
        transcript = candidate / "transcript.txt"
        if transcript.exists():
            return transcript, candidate
        return None, candidate
    if candidate.is_file() and candidate.name == "transcript.txt":
        return candidate, candidate.parent

    try:
        video_id = extract_video_id(value)
    except ValueError:
        return None, candidate
    video_dir = base_dir / video_id
    if not video_dir.is_dir():
        matches = sorted(base_dir.glob(f"{video_id}-*"))
        if matches and matches[0].is_dir():
            video_dir = matches[0]
    transcript = video_dir / "transcript.txt"
    if transcript.exists():
        return transcript, video_dir
    return None, video_dir


def build_user_prompt(transcript: str, language: str) -> str:
    return (
        f"Below is the transcript of a YouTube video. Write a resume "
        f"(summary) of it in {language}.\n\n"
        f"Transcript:\n```\n{transcript}\n```\n\nResume:"
    )


def sanitize_for_filename(value: str) -> str:
    """Make a string safe to use in a filename."""
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")


def build_frontmatter(video_id: str, model: str, language: str, timestamp: datetime) -> str:
    lines = [
        "---",
        f"video_id: {video_id}",
        f"model: {model}",
        f"language: {language}",
        f"generated_at: {timestamp.isoformat()}",
        "---",
        "",
    ]
    return "\n".join(lines)


def call_openrouter(api_key: str, model: str, system_prompt: str, user_prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "youtube-skill",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
    }
    response = requests.post(OPENROUTER_CHAT_URL, headers=headers, json=payload, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(
            f"OpenRouter request failed ({response.status_code}): {response.text}"
        )
    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected OpenRouter response: {data}") from exc


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "video",
        help="path to a transcript directory, a bare video id, or a full YouTube URL",
    )
    parser.add_argument(
        "--language", default=DEFAULT_LANGUAGE,
        help=f"Language for the resume (default: {DEFAULT_LANGUAGE})",
    )
    parser.add_argument(
        "--base-dir", default=None,
        help="Directory to resolve bare video ids against (default: ./db)",
    )
    args = parser.parse_args(argv[1:])

    # Auto-loads the nearest .env by walking up from the current directory
    # (e.g. a project-level .env), then falls back to one next to this
    # script for a personal, skill-local key. load_dotenv never overrides
    # variables already set in the environment.
    load_dotenv(find_dotenv(usecwd=True))
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    api_key = os.environ.get("OPENROUTER_API_KEY")
    model = os.environ.get("OPENROUTER_MODEL")
    if not api_key:
        print("Error: OPENROUTER_API_KEY is not set. See .env.example.", file=sys.stderr)
        return 1
    if not model:
        print("Error: OPENROUTER_MODEL is not set. See .env.example.", file=sys.stderr)
        return 1

    base_dir = Path(args.base_dir) if args.base_dir else Path.cwd() / "db"
    transcript_file, video_dir = resolve_transcript(base_dir, args.video)
    if transcript_file is None:
        print(
            f"Error: transcript not found for {args.video!r}. "
            f"Pass a directory path, a video id, or a YouTube URL. "
            f"Run download_transcript.py first.",
            file=sys.stderr,
        )
        return 1
    label = video_dir.name
    id_match = re.match(r"([A-Za-z0-9_-]{11})", video_dir.name)
    video_id = id_match.group(1) if id_match else video_dir.name

    transcript = transcript_file.read_text(encoding="utf-8")
    user_prompt = build_user_prompt(transcript, args.language)

    print(f"Generating resume for {label} using {model} ...")
    resume = call_openrouter(api_key, model, SYSTEM_PROMPT, user_prompt)

    timestamp = datetime.now().astimezone()
    frontmatter = build_frontmatter(video_id, model, args.language, timestamp)
    content = f"{frontmatter}\n{resume}"

    stamp = timestamp.strftime("%Y%m%dT%H%M%S")
    model_slug = sanitize_for_filename(model)
    out_file = video_dir / f"resume-{stamp}-{model_slug}.md"
    out_file.write_text(content, encoding="utf-8")
    print(f"Saved: {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
