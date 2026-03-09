#!/usr/bin/env python3
"""Extract YouTube subtitles and format them as meaningful phrases with timecodes.

Handles YouTube auto-generated VTT format where each cue has two lines:
line 1 = repeat of previous text (context), line 2 = new text with <c> word timing tags.
"""

import argparse
import os
import re
import subprocess
import tempfile


def get_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def download_subtitles(url: str, lang: str, tmpdir: str) -> str:
    """Download subtitles using yt-dlp, return path to VTT file."""
    base = os.path.join(tmpdir, "subs")

    # Try manual subtitles first, then auto-generated
    for auto_flag in [False, True]:
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--sub-format", "vtt",
            "--convert-subs", "vtt",
            "-o", base,
        ]
        if auto_flag:
            cmd += ["--write-auto-sub"]
        else:
            cmd += ["--write-sub"]

        cmd += ["--sub-lang", f"{lang},en", url]

        subprocess.run(cmd, capture_output=True, text=True)

        # Find the downloaded VTT file
        for f in sorted(os.listdir(tmpdir)):
            if f.endswith(".vtt"):
                return os.path.join(tmpdir, f)

    raise RuntimeError(
        f"Could not download subtitles for {url}. "
        "The video may not have subtitles available."
    )


def get_video_title(url: str) -> str:
    """Get video title via yt-dlp."""
    result = subprocess.run(
        ["yt-dlp", "--get-title", url],
        capture_output=True, text=True
    )
    return result.stdout.strip() or "Untitled"


def parse_timestamp(ts: str) -> float:
    """Parse VTT timestamp (HH:MM:SS.mmm) to seconds."""
    parts = ts.strip().split(":")
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return float(parts[0])


def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def strip_tags(text: str) -> str:
    """Remove VTT inline tags like <c>, </c>, <00:00:01.234>."""
    return re.sub(r'<[^>]+>', '', text).strip()


def parse_vtt_auto(vtt_path: str) -> list[dict]:
    """Parse YouTube auto-generated VTT into clean segments.

    YouTube auto-subs use a two-line cue format:
      Line 1: previous context (plain text, no tags) — SKIP
      Line 2: new words with <c> timing tags — EXTRACT

    Also handles "flash" cues (duration < 20ms) which are just clean snapshots — SKIP.
    """
    with open(vtt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into cue blocks
    # Each block: timestamp line + text lines, separated by blank lines
    blocks = re.split(r'\n\n+', content)

    segments = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Find timestamp line
        ts_match = re.search(
            r'(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)',
            block
        )
        if not ts_match:
            continue

        start = parse_timestamp(ts_match.group(1).replace(",", "."))
        end = parse_timestamp(ts_match.group(2).replace(",", "."))

        # Skip flash cues (< 20ms duration) — they're just clean-text snapshots
        if (end - start) < 0.02:
            continue

        # Get text after the timestamp line
        ts_line_end = ts_match.end()
        # Find end of the timestamp line (past any align/position attributes)
        rest = block[ts_line_end:]
        # Skip to next line
        newline_pos = rest.find('\n')
        if newline_pos == -1:
            continue
        text_part = rest[newline_pos + 1:]

        # In auto-subs, the cue has two lines:
        # Line 1: context repeat of previous text (no <c> tags)
        # Line 2: new text with <c> word-timing tags
        lines = text_part.split('\n')

        # Find the line with <c> tags — that's the new content
        new_line = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if '<c>' in line or re.search(r'<\d{2}:\d{2}', line):
                new_line = line
                break

        if new_line:
            text = strip_tags(new_line)
        else:
            # Manual subtitles or simple format — take all non-empty lines
            all_text = ' '.join(strip_tags(l) for l in lines if l.strip())
            if not all_text:
                continue
            text = all_text

        # Clean up HTML entities
        text = text.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
        text = re.sub(r'\s+', ' ', text).strip()

        if text and len(text) > 1:
            segments.append({"start": start, "end": end, "text": text})

    return segments


def merge_into_phrases(
    segments: list[dict],
    max_pause: float = 1.5,
    max_phrase_duration: float = 25.0,
) -> list[dict]:
    """Merge short segments into coherent phrases based on punctuation and pauses."""
    if not segments:
        return []

    phrases = []
    current = {
        "start": segments[0]["start"],
        "end": segments[0]["end"],
        "text": segments[0]["text"],
    }

    sentence_end = re.compile(r'[.!?…]\s*$')

    for seg in segments[1:]:
        pause = seg["start"] - current["end"]
        combined_duration = seg["end"] - current["start"]
        ends_sentence = sentence_end.search(current["text"])

        # Start new phrase if: big pause, sentence ended, or phrase too long
        if pause > max_pause or (ends_sentence and pause > 0.3) or combined_duration > max_phrase_duration:
            phrases.append(current)
            current = {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
            }
        else:
            current["end"] = seg["end"]
            current["text"] += " " + seg["text"]

    phrases.append(current)

    # Clean up merged text and remove stutter duplicates at boundaries
    for p in phrases:
        p["text"] = _remove_stutter(re.sub(r'\s+', ' ', p["text"]).strip())

    return phrases


def _remove_stutter(text: str) -> str:
    """Remove repeated phrases caused by auto-subtitle overlap.

    E.g. 'работать с памятью. Аа сам проект работать с памятью. Аа сам проект выпущен'
    becomes 'работать с памятью. Аа сам проект выпущен'
    """
    words = text.split()
    n = len(words)
    if n < 6:
        return text

    # Try to find a repeated subsequence (3-15 words) starting from inside the text
    for repeat_len in range(min(15, n // 2), 2, -1):
        for start in range(0, n - 2 * repeat_len + 1):
            chunk = words[start:start + repeat_len]
            next_chunk = words[start + repeat_len:start + 2 * repeat_len]
            if chunk == next_chunk:
                # Remove the duplicate
                cleaned = words[:start + repeat_len] + words[start + 2 * repeat_len:]
                return _remove_stutter(' '.join(cleaned))

    return text


def format_output(
    phrases: list[dict],
    video_id: str,
    title: str,
) -> str:
    """Format phrases as Markdown with clickable timecodes."""
    lines = [
        f"# Субтитры: {title}",
        "",
        f"> Источник: https://youtu.be/{video_id}",
        "",
        "## Таймкоды",
        "",
    ]

    for p in phrases:
        ts = format_timestamp(p["start"])
        t_sec = int(p["start"])
        link = f"https://youtu.be/{video_id}?t={t_sec}"
        lines.append(f"- [{ts}]({link}) {p['text']}")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract YouTube subtitles as phrases with timecodes"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--lang", "-l", default="ru", help="Preferred language (default: ru)")
    args = parser.parse_args()

    video_id = get_video_id(args.url)
    print(f"Video ID: {video_id}")

    print("Fetching video title...")
    title = get_video_title(args.url)
    print(f"Title: {title}")

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Downloading subtitles (lang={args.lang})...")
        vtt_path = download_subtitles(args.url, args.lang, tmpdir)
        print(f"Downloaded: {os.path.basename(vtt_path)}")

        print("Parsing subtitles...")
        segments = parse_vtt_auto(vtt_path)
        print(f"Clean segments: {len(segments)}")

        phrases = merge_into_phrases(segments)
        print(f"Merged phrases: {len(phrases)}")

    output = format_output(phrases, video_id, title)

    out_path = args.output or f"subtitles_{video_id}.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\nSaved to: {out_path}")
    print(f"Total phrases: {len(phrases)}")
    if phrases:
        total_duration = phrases[-1]["end"] - phrases[0]["start"]
        print(f"Duration: {format_timestamp(total_duration)}")


if __name__ == "__main__":
    main()
