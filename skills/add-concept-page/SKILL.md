---
name: add-concept-page
description: Use when adding or editing a concepts/*.md page (or a long reading) in alexander-wiki, or when asked to verify or audit excerpts there. Covers page shape, sourcing from the sources repo, the mandatory quote-verification script, and the scan check for OCR errors.
---

# Adding a concept page

## Overview

A concept page pairs a short synthesis in our own words with verbatim excerpts from Alexander's books, each with book, chapter and printed page, plus his figures where the book argues by image. Adapted from wilber-wiki's `add-excerpt-page`.

**The one rule that matters most: every quote must be real, checked text, not a paraphrase and not a reconstruction from memory.** And because the Nature of Order and Timeless Way texts are OCR machine drafts, a quote that matches the markdown can still be wrong. Every excerpt is checked twice: against the source markdown (script) and against the page scan (you).

## When to use

- Adding `concepts/<slug>.md`, or editing a page's excerpts or figures.
- Auditing existing excerpts.
- Not for pattern pages or the Eishin-style long readings, except that the verifier and scan check apply to them too.

## Sourcing

Sources live in the sibling repo `/Users/rgrp/src/natureoforder/sources/texts/` (override with `ALEXANDER_SOURCES`). Read its `AGENTS.md` and the book's `README.md` first. Never quote from memory or from our own earlier pages: open the chapter file and copy from it.

| Book slug (`works:`) | Directory | Chapter files | Notes |
|---|---|---|---|
| `timeless-way-of-building` | `timeless-way-of-building` | `markdown/NN-*.md` (ch. 1-27) | machine draft |
| `pattern-language` | `pattern-language` | `markdown/patterns/NNN-*.md` (cite `pattern NNN`) | partly hand-corrected |
| `nature-of-order-1` | `nature-of-order-01-the-phenomenon-of-life` | `markdown/NN-*.md` (00 = prologue) | machine draft; prologue and ch. 7 reviewed |
| `nature-of-order-2` | `nature-of-order-02-the-process-of-creating-life` | `markdown/NN-*.md` | machine draft, noticeable damage |
| `nature-of-order-3` | `nature-of-order-03-a-vision-of-a-living-world` | `markdown/NN-*.md` | noisiest; pp. 529-530 missing |
| `nature-of-order-4` | `nature-of-order-04-the-luminous-ground` | `markdown/NN-*.md` | mostly clean |

Page numbers: each chapter's YAML frontmatter has `page_starts` with `pdf`, `printed`, a short `after` (text just before the boundary) and a unique `before` (text just after it). Cite the printed page where the quote starts, never the PDF page. Book title in the attribution is the italic title: *The Timeless Way of Building*, *A Pattern Language*, *The Phenomenon of Life*, *The Process of Creating Life*, *A Vision of a Living World*, *The Luminous Ground* (the verifier maps these to the books).

## Page shape

Frontmatter:

```yaml
---
title: <display title>
description: <one sentence>
slug: <matches filename>
aliases: [<lowercase alternate names>]
status: draft
works: [<book slugs from the table>]
---
```

Sections, in order:

1. `## Alexander's view`: a short synthesis in our words. No invented exercises ("try it at a doorway"). Any editorial example is labelled as ours ("An example of ours, not Alexander's: ..."). Say where he is strong and where he is contested; do not soften claims he makes plainly.
2. One `## In *<Book>*` section per book, containing verbatim blockquotes, each ending with an attribution line:

   ```markdown
   > Now make yourself comfortable. Not in some way which you can show to other people...
   >
   > — *The Timeless Way of Building*, ch. 2, "The quality without a name", p. 32
   ```

   For *A Pattern Language* use `pattern 12, "Community of 7000", p. 78`. Figures from the sources repo, where the book argues by image, go in the same section (see Figures).
3. `## See also`: wikilinks or relative links, each with a one-line reason.

## Excerpts

- Copy from the source markdown open in front of you (grep or Read in this session), never from memory.
- `...` marks every elision, including a quote that starts mid-sentence (keep the source's lowercase) or joins non-adjacent passages. Do not silently end a sentence with a period the source does not have; cut to the last full clause or use `...`. A trailing `.` may stand for different closing punctuation (the one tolerance). A trailing quotation mark may not.
- Cite the actual chapter number and title and the printed page where the quote starts (`pp. 175-176` is fine: the first page is checked). Cite `(footnote)` if the text is from a note.
- Show quotes directly: plain blockquote, no accordion syntax, no per-excerpt heading. Typically 3-8 quotes; more if the material supports it, per Rufus's "excerpts liberally".
- Bold within a quote sparingly and only editorially; the verifier strips it. Keep source italics.
- One paragraph per line, never hard-wrapped.

## Figures

Where the book argues by image (the fifteen properties, Timeless Way plates), include the figure. Sources: `<book>/markdown/figures/` (Nature of Order: `figures/bulk/pdf-NNNN-NN.jpg`, `figures/chapter-07/`; Timeless Way: `figures/pdf-NNNN-N.jpg`) and `pattern-language/markdown/media/`. Copy the file into `assets/figures/<book-slug>/` with a meaningful name, then:

```markdown
![Alt text describing what is shown.](../assets/figures/nature-of-order-1/levels-of-scale-door.jpg)

*Caption in our words or the book's, labelled. From p. 147.*
```

The crops are automatic and can split, omit or merge pictures: open the crop and the page scan before using it, and check the book's own caption wording (captions are the noisiest text).

## Verifying quotes (mandatory, every time)

```bash
python3 skills/add-concept-page/scripts/verify_quotes.py concepts/<slug>.md
```

With no arguments it checks `concepts/*.md`. It checks every blockquote segment against the cited chapter file (frontmatter stripped; `...` elisions, dropped italics and a substituted final `.` tolerated), and checks that the quote starts on the cited printed page using the chapter's `page_starts` anchors. A quote with no chapter is searched book-wide with a WARNING; fix the citation. `--strict` makes warnings fail. Exit 1 on failure. **A failure means fix the quote or the citation, not argue with the script.**

## Scan check (mandatory, every excerpt)

Passing the script only proves the quote equals our markdown, which is an OCR draft. For each excerpt:

1. Open the page record `<book>/raw/pages/pdf-NNNN.json` (Timeless Way: the line with `"pdf": NNNN` in `raw/pages.jsonl`), NNNN being the `pdf` value of the cited page in `page_starts`. This is the raw OCR with word geometry: it catches reading-order and paragraph-join problems but it is the same OCR engine, so it cannot catch a misread letter by itself.
2. For the true check, look at the scan. The page images are not stored in the repos. The source PDFs are in the private release `source-pdfs` of `natureoforder/sources` (and `searchable-editions`); `page_starts[].scan` gives the URL with `#page=N` where present. Download once with `gh release download source-pdfs -R natureoforder/sources -p '<book>.pdf' -D <scratch dir>` (verify the SHA-256 in the book README), then render a page: `pdftoppm -f N -l N -r 110 -jpeg book.pdf out`, and read the image. Do not commit PDFs.
3. Compare every word of the excerpt with the image. Typical OCR damage: `I` for `1`, `thar` for `that`, `theretore`, `?` for footnote markers, italics lost or added, dropped hyphenation, wrong small-capital case (`sTRoNg CENTErs`).
4. If the markdown is wrong, fix it upstream in the sources repo: edit the chapter file, commit there with its own commit ("Correct OCR in NoO1 ch. 5 p. 151 against scan"), and update the chapter's `page_starts` `before`/`after` annotation if the corrected passage is one of them. Then record the correction in the book's `quality/verified-readings.json` so regeneration keeps it, in that file's existing format: Nature of Order books map the PDF page number to a list of `{"lines": [<OCR line as extracted>], "replacement": "<corrected text>"}` (add `"standalone": true` for replacement paragraphs); the Timeless Way file maps the PDF page to `[<wrong>, <right>]`. Match the neighbouring entries.
5. Only after the scan agrees, quote the corrected text. Never quote our own correction that the scan does not show.

## Rationalisations to watch for (yours, mid-task)

| Thought | Reality |
|---|---|
| "I'm confident this is roughly what he said" | Confidence is not verification. Grep the source, then the scan. |
| "It's basically what Alexander means" | A paraphrase-as-quote is the failure this skill exists to prevent. Find the real sentence or write it as prose in the synthesis. |
| "I'll end it with a period, cleaner" | If the source does not end there, that is a silent edit. Use `...` or stop one clause earlier. |
| "The script passed, so it is right" | The script compares against an OCR draft. `thar` for `that` passes if the draft has it too. Do the scan check. |
| "The OCR JSON agrees, so the scan does" | Same OCR engine, same errors. Look at the page image. |
| "Fixing the OCR can wait, I'll quote it corrected here" | Fix upstream in the sources repo first, or the next quote of that passage repeats the error. |
| "A little scene or exercise makes the idea land" | Invented exercises are what the rebuild removes. Quote him; label any example of ours. |
| "The page number is close enough" | The script checks it and readers use it. Use the printed page where the quote starts. |
| "Verification is for the reviewer" | You wrote the quote; you verify it before calling the page done. |
| "Alexander is hedging here, I'll soften" | Keep his claim at his strength (for example Book 1, p. 317, independent of culture or personality) and note where critics contest it in the synthesis. |

## After adding a page

Update `concepts/index.md` (keep its order, star core terms), link the page from and to genuinely related concepts, and read `docs/plans/2026-11-26-rebuild-plan.md` for where the concept sits in the roadmap. Commit the sources-repo fixes and this repo's page separately.

## Lessons from the pilot pages (26 Nov)

The three pilots (`concepts/quality-without-a-name.md`, `concepts/centers.md`, `concepts/levels-of-scale.md`) are the reference pages. Match their shape and voice.

- **Quotation share.** Aim for roughly two thirds of the words to be Alexander's.
- **Every quote reads on its own** or follows a one-line lead-in that sets it up. Elide only whole sentences.
- **Figures: re-crop from the PDF.** The automatic crops in `figures/bulk/` are low-resolution and sometimes split. Render the page with `pdftoppm`, crop, and check each image against the page. Save to `assets/figures/<book>/` with caption and page.
- **Verified readings.** Record each OCR fix in the book's `quality/verified-readings.json`. NoO books use `{"lines": [...], "replacement": "..."}`; TWB uses `["wrong", "right"]` pairs, and a page may now carry several. Copy an existing entry as the template.
- **Small capitals** use the `.sc` class, not inline styles. His italics inside a quote show upright, because quotes are set in italic.
- **Co-authored books.** Name the authors on first mention (see `docs/voice.md`).
- **Before handing off:** `verify_quotes.py --strict` passes, and every internal link resolves.
