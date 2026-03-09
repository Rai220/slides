# YouTube Subtitles Extractor

Extract subtitles from YouTube videos and format them as meaningful phrases with timecodes.

## Usage

```bash
python3 .agents/skills/youtube-subtitles/extract_subtitles.py <YOUTUBE_URL> [--output <OUTPUT_PATH>] [--lang <LANG>]
```

### Arguments

- `YOUTUBE_URL` — YouTube video URL (any format: full, short, embed)
- `--output` — Output file path (default: `subtitles_<video_id>.md`)
- `--lang` — Preferred subtitle language (default: `ru`, falls back to `en`, then auto-generated)

### Output format

The script produces a Markdown file with:
- Video title and URL in the header
- Phrases grouped by meaning (not raw subtitle segments)
- Each phrase has a clickable timecode link

Example output:
```markdown
# Субтитры: Название видео

> Источник: https://youtu.be/VIDEO_ID

## Таймкоды

- [00:00:05](https://youtu.be/VIDEO_ID?t=5) Приветствую всех, сегодня мы поговорим о том, как устроен OpenClaw
- [00:00:23](https://youtu.be/VIDEO_ID?t=23) Начнём с архитектуры и разберём основной цикл работы агента
```

### How it works

1. Downloads subtitles via `yt-dlp` (prefers manual subs, falls back to auto-generated)
2. Parses VTT format, deduplicates overlapping segments
3. Merges short segments into coherent phrases (by punctuation and pause gaps)
4. Formats as Markdown with clickable YouTube timecode links

### Requirements

- `yt-dlp` (installed via homebrew)
- Python 3.10+
