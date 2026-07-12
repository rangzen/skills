#!/usr/bin/env -S uv run
# /// script
# dependencies = ["youtube-transcript-api", "requests"]
# ///
"""Download a YouTube transcript for a given video URL or id.

Usage:
    download_transcript.py <youtube-url-or-id> [output_dir]

Creates <output_dir> (default: ./db, relative to the current directory) if
missing, then <output_dir>/<video_id>-<slug>/ and writes the transcript into
that directory. The slug is derived from the video title, e.g.
db/P3KDebPTUrw-openai-codex-lead-new-shape-product-andrew-ambrosino.

Self-contained: run with `uv run download_transcript.py ...` and uv installs
the two dependencies on the fly, no project setup required.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import requests
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Extract the 11-char video id from various YouTube URL forms."""
    patterns = [
        r"(?:v=|/)([A-Za-z0-9_-]{11})(?:[&?].*)?$",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/embed/([A-Za-z0-9_-]{11})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url
    raise ValueError(f"Could not extract video id from: {url}")


def slugify(value: str) -> str:
    """Turn a title into a url-style slug, e.g. for directory names."""
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if len(value) > 80:
        value = value[:80].rstrip("-")
    return value


def fetch_video_title(video_id: str) -> str:
    """Fetch the video title via YouTube's oEmbed endpoint."""
    url = (
        "https://www.youtube.com/oembed"
        f"?url=https://www.youtube.com/watch?v={video_id}&format=json"
    )
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "youtube-skill"})
        resp.raise_for_status()
        return resp.json().get("title", "")
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: could not fetch video title: {exc}", file=sys.stderr)
        return ""


def format_transcript(transcript) -> str:
    """Render the fetched transcript as 'start --> text' lines."""
    lines = []
    for snippet in transcript:
        start = getattr(snippet, "start", 0.0)
        text = getattr(snippet, "text", "").strip()
        lines.append(f"{start:07.2f} --> {text}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print(__doc__)
        return 1

    url = argv[1]
    output_dir = Path(argv[2]) if len(argv) == 3 else Path.cwd() / "db"

    try:
        video_id = extract_video_id(url)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    existing = sorted(output_dir.glob(f"{video_id}*"))
    if existing and existing[0].is_dir():
        out_dir = existing[0]
        title = ""
    else:
        title = fetch_video_title(video_id)
        slug = slugify(title)
        dir_name = f"{video_id}-{slug}" if slug else video_id
        out_dir = output_dir / dir_name
        out_dir.mkdir(exist_ok=True)

    print(f"Fetching transcript for video {video_id} ({title or 'unknown title'}) ...")
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: could not fetch transcript: {exc}", file=sys.stderr)
        return 1
    content = format_transcript(transcript)

    out_file = out_dir / "transcript.txt"
    out_file.write_text(content, encoding="utf-8")

    raw_file = out_dir / "transcript.json"
    raw_file.write_text(
        json.dumps(
            [{"text": s.text, "start": s.start, "duration": s.duration}
             for s in transcript],
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved: {out_file}")
    print(f"Saved: {raw_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
