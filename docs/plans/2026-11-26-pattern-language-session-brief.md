---
title: Pattern Language session brief
date: 2026-11-26
beads: alex-88s.20.2, alex-88s.19.15
---

# Pattern Language session brief

**Goal.** Put the whole of *A Pattern Language* (Alexander, Ishikawa, Silverstein, with Jacobson, Fiksdahl-King and Angel, 1977) on alexander.wiki: all 253 patterns, in full, as printed, with their images. Rufus decided this on 26 Nov: "literally a copy of his thing… including with the images". No summaries, no commentary in place of the text.

**Done-check.**

- One page per pattern at `/patterns/<slug>` for all 253, with the full text, the stars, the opening photograph and every figure in place, and the printed page numbers.
- Every pattern reference in the text, such as "WINDOW PLACE (180)", links to that pattern's page. Each page also lists the patterns it links to and the patterns that link to it.
- The opening matter ("Using this book", the summary of the language) and the three section introductions (Towns, Buildings, Construction) are on the site too.
- The patterns index links every row and has a title search box at the top (Beads `alex-88s.19.15`).
- Images at full size, no shrinking. A lossless `jpegtran -optimize` pass is fine.
- The two existing hand-made pages (`window-place.md`, `positive-outdoor-space.md`) keep their commentary and "try it" sections, set alongside the full text.
- Committed, merged to `main`, pushed, Beads synced. Add a changelog entry with a screenshot.

## Source

- `~/src/natureoforder/sources/texts/pattern-language/`: `markdown/patterns/NNN-*.md` are already cross-linked as `[NAME (NNN)](NNN-slug.md)`, with `page_starts` frontmatter. Images are in `markdown/media/img/` (823 files, 54 MB). Read `README.md` and `quality.md` there first for known OCR limits.
- Pattern slugs on the site drop the number (`/patterns/window-place`). Keep that, and map the links.

## Design

- Follow the existing pattern-page look (`patterns/window-place.md`, the `pattern-` classes in `custom.css`) and the *Pattern Language* interior typesetting already chosen by the design session. The problem statement and the "Therefore" solution should stand out in bold, as in the book.
- Generate the pages with a script kept in the repo (e.g. `scripts/build_patterns.py`) so they can be rebuilt when the sources are corrected.

## Search box

Scripts do not run inside `.md` pages, but there are two ways: a script injected site-wide through `config.json` `head` that only acts on `/patterns`, or a standalone `.html` widget. Check the Flowershow docs (https://flowershow.app/docs/agents/html.md and the premium features) for the cleanest route, and pick one.

## Later (not this session)

- A graph view of how the patterns connect (`alex-88s.20.3`).

## Conventions

Read `AGENTS.md` and `docs/voice.md`. One line per Markdown paragraph. Tasks in Beads. Commit and push at the end of each chunk; pushing `main` publishes the live site, and Rufus has approved this work.
