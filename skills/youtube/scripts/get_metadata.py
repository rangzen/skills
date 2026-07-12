#!/usr/bin/env -S uv run
# /// script
# dependencies = ["yt-dlp"]
# ///
"""Fetch metadata for a YouTube video (title, duration, thumbnail, channel).

No LLM or API key required. Writes metadata.json into the video's output
directory and prints a human-readable summary. Works even when no transcript
is available (live streams, age-restricted videos, etc.).

The output directory follows the same convention as download_transcript.py:
  <output_dir>/<video_id>-<slug>/metadata.json

If a directory for this video already exists under output_dir (e.g. from a
prior download_transcript.py run), metadata.json is written there instead
of creating a new directory.

Usage:
    get_metadata.py <youtube-url-or-id> [output_dir]

output_dir defaults to ./db relative to the current directory.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yt_dlp


def extract_video_id(url: str) -> str:
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
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if len(value) > 80:
        value = value[:80].rstrip("-")
    return value


def format_duration(seconds: int | None) -> str:
    if not seconds:
        return "unknown"
    h, remainder = divmod(int(seconds), 3600)
    m, s = divmod(remainder, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def fetch_info(url: str) -> dict:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


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

    print(f"Fetching metadata for {video_id} ...")
    try:
        info = fetch_info(url)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: yt-dlp failed: {exc}", file=sys.stderr)
        return 1

    title = info.get("title") or ""
    duration_secs = info.get("duration")
    channel = info.get("uploader") or info.get("channel") or ""
    channel_url = info.get("uploader_url") or info.get("channel_url") or ""
    thumbnail = info.get("thumbnail") or ""
    upload_date = info.get("upload_date") or ""
    view_count = info.get("view_count")
    description = info.get("description") or ""

    metadata = {
        "video_id": video_id,
        "title": title,
        "duration_seconds": duration_secs,
        "duration": format_duration(duration_secs),
        "channel": channel,
        "channel_url": channel_url,
        "thumbnail": thumbnail,
        "upload_date": upload_date,
        "view_count": view_count,
        "description": description,
        "url": f"https://www.youtube.com/watch?v={video_id}",
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    existing = sorted(output_dir.glob(f"{video_id}-*"))
    if existing and existing[0].is_dir():
        out_dir = existing[0]
    else:
        slug = slugify(title)
        dir_name = f"{video_id}-{slug}" if slug else video_id
        out_dir = output_dir / dir_name
        out_dir.mkdir(exist_ok=True)

    out_file = out_dir / "metadata.json"
    out_file.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Title:    {title}")
    print(f"Channel:  {channel}")
    print(f"Duration: {format_duration(duration_secs)}")
    if upload_date:
        print(f"Uploaded: {upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}")
    if view_count is not None:
        print(f"Views:    {view_count:,}")
    if thumbnail:
        print(f"Thumb:    {thumbnail}")
    print(f"Saved:    {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
