#!/usr/bin/env bash
# Fetch a real transcript for a YouTube video and generate a Markdown resume
# from it. Chains download_transcript.py and make_resume.py so the caller
# only needs one call per video. Both scripts are self-contained (PEP 723
# inline deps run via `uv run`), so this works from any directory as long
# as `uv` is installed and OPENROUTER_API_KEY / OPENROUTER_MODEL are set.
#
# Usage:
#   get_video_notes.sh <youtube-url-or-id> [language] [output_dir]
#
# output_dir defaults to ./db under the current working directory, so
# transcripts/resumes land next to wherever you're taking notes. Prints the
# path to the generated resume-*.md file on the last line of stdout.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <youtube-url-or-id> [language] [output_dir]" >&2
  exit 1
fi

VIDEO="$1"
LANGUAGE="${2:-english}"
OUTPUT_DIR="${3:-$(pwd)/db}"

uv run "$SCRIPT_DIR/download_transcript.py" "$VIDEO" "$OUTPUT_DIR" >&2

VIDEO_ID=$(python3 -c "
import re, sys
patterns = [
    r'(?:v=|/)([A-Za-z0-9_-]{11})(?:[&?].*)?\$',
    r'youtu\.be/([A-Za-z0-9_-]{11})',
    r'youtube\.com/embed/([A-Za-z0-9_-]{11})',
    r'youtube\.com/shorts/([A-Za-z0-9_-]{11})',
]
v = sys.argv[1]
for p in patterns:
    m = re.search(p, v)
    if m:
        print(m.group(1))
        sys.exit(0)
if re.fullmatch(r'[A-Za-z0-9_-]{11}', v):
    print(v)
    sys.exit(0)
sys.exit(1)
" "$VIDEO")

VIDEO_DIR=$(ls -d "$OUTPUT_DIR/${VIDEO_ID}"* 2>/dev/null | head -n1)
if [ -z "$VIDEO_DIR" ]; then
  echo "Error: could not find a downloaded transcript dir for video id $VIDEO_ID under $OUTPUT_DIR" >&2
  exit 1
fi

uv run "$SCRIPT_DIR/make_resume.py" "$VIDEO_DIR" --language "$LANGUAGE" >&2

RESUME_FILE=$(ls -t "$VIDEO_DIR"/resume-*.md | head -n1)
echo "$RESUME_FILE"
