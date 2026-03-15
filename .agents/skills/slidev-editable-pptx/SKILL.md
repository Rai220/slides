---
name: slidev-editable-pptx
description: Convert Slidev presentations into editable PowerPoint files with real text objects via Pandoc. Use when the user asks for a редактируемый PPTX, editable PowerPoint, или PPTX не картинками.
---

# Slidev Editable PPTX

Use this skill when a user wants an editable `pptx` from a `Slidev` deck.

## Important

Do not use `bunx slidev export --format pptx` for this goal. Slidev exports PPTX slides as images, so the text is not truly editable.

## Default Workflow

1. Read the source `slides.md`.
2. Keep the original Slidev file unchanged.
3. Create a sibling file such as `slides_pandoc.md`.
4. Convert Slidev-specific markup into Pandoc-friendly slide markdown.
5. Export with `pandoc` to a new `pptx`.
6. Verify that the resulting PPTX contains native text, not only media.

## Conversion Rules

- Preserve slide order, headings, lists, and images.
- Remove Slidev-only slide frontmatter like `layout:` and `class:`.
- Remove deck CSS such as `<style>...</style>`.
- Replace Slidev column syntax like `::right::` with Pandoc columns:

```md
:::::::::::::: {.columns}
::: {.column width="58%"}
Left content
:::
::: {.column width="42%"}
![](image.png){width=85%}
:::
::::::::::::::
```

- Convert HTML images to markdown images with local relative paths whenever possible.
- Keep captions as normal text under the image.
- If the first slide is a title slide, prefer Pandoc metadata in the file frontmatter:

```yaml
---
title: "Presentation title"
subtitle: "Optional subtitle"
author: "Author name"
lang: ru-RU
---
```

- Avoid duplicating the title slide in the body if the same content is already represented in metadata.

## Export Command

Run from the presentation directory:

```bash
pandoc "slides_pandoc.md" -t pptx -o "presentation_editable.pptx"
```

## Verification

After export, confirm the PPTX has native text objects. A quick check is to inspect the PPTX zip and verify slide XML contains `<a:t>` text nodes.

Example:

```bash
python3 - <<'PY'
import zipfile
from pathlib import Path

pptx = Path("presentation_editable.pptx")
with zipfile.ZipFile(pptx) as z:
    slides = [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
    text_slides = sum("<a:t>" in z.read(name).decode("utf-8", errors="ignore") for name in slides)
    print(f"slides={len(slides)}")
    print(f"slides_with_text_xml={text_slides}")
PY
```

## Notes

- Pandoc produces editable text and image objects, but not a pixel-perfect copy of the Slidev design.
- If the user wants closer visual fidelity, create or use a `reference-doc` PPTX template and export with `--reference-doc=template.pptx`.
- Save the adapted markdown and the exported PPTX next to the original deck unless the user asks for another location.
