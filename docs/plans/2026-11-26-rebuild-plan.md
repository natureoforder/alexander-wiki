---
title: Alexander Wiki — state of the nation and rebuild plan
date: 2026-11-26
status: draft for Rufus
---

# Alexander Wiki — state of the nation and rebuild plan

## Goal

A site that feels like Alexander and lets readers meet him in his own words: a way in (roadmap), the ideas (concepts with generous excerpts), the books (works), why he matters beyond architecture (visionary), and Rufus's own notes. Modelled on the Wilber Wiki structure, with a brand distilled from *A Pattern Language* (interior and yellow Oxford jacket) and the *Nature of Order* volumes.

**Done-check for this round (a vertical slice Rufus can judge in one sitting):** roadmap page live; three pilot concept pages in the new excerpt-led shape (the quality without a name, centers, one fifteen-property page with Alexander's images); works hub plus two book pages; brand board with a chosen direction applied to the front page; credits, positioning note and a Visionary landing page with Rufus's two talks; Notes and Changelog sections visible. Approval of this slice gates the volume work (remaining concepts, properties, works, patterns, Living Neighborhoods). Committed, pushed, Beads synced.

## State of the nation

**What exists.** 29 concept pages, 3 Living Neighborhoods pages, Eishin practice guide and reading, a 253-pattern index with 2 pattern readings, a design-comparison page. EB Garamond typesetting after *A Pattern Language* pp. 833–834; calm and bookish. Preview on Flowershow; production at alexander.wiki.

**What's good.**

- Citations are accurate: every page reference spot-checked against the sources was right (one off-by-one in generative codes).
- `practice/eishin-campus-reading.md` — 19 quoted passages, page numbers, images, light editorial headings. Best page on the site and the model for the rest.
- Typesetting and the plate-and-commentary spread for patterns.
- The patterns index as scaffolding.

**What's wrong.**

- **No Alexander on the concept pages.** Not one block quotation across 29 concept pages. All paraphrase, in a formulaic shape (invented scene → gloss → "try it at a doorway" → see also). Sometimes softens him: the mirror-of-the-self page hedges where he claims the result is "independent of culture or personality" (Book 1, p. 317); the quality-without-a-name page invents a scene where his own "Now make yourself comfortable…" (TWB p. 32) is far stronger.
- **The fifteen property pages are stubs** (~110 words, no images), though each property gets 4–8 illustrated pages in Book 1, ch. 5.
- **Selection is lopsided.** Mostly Book 1 plus process odds and ends. Missing: being alive, the gate, patterns of events, pattern language *as a language*, unfolding wholeness, the fifteen transformations, every part unique, form language, living structure and degrees of life, the "I", colour, ornament, and almost all of Book 3. Two pages are essays answering GitHub issues, not concepts. Wholeness is split across three overlapping pages.
- **Living Neighborhoods section has no content of its own**: link lists into livingneighborhoods.org, duplicating the separate `natureoforder/livingneighborhoods` project.
- **No works section, no "who was Alexander", no roadmap, no credits.**
- **Hardly any images**, though the books argue through photographs and the sources repo has thousands of extracted figures.

**Sources available** (`natureoforder/sources/texts/`):

| Book | State | Excerpt safety |
|---|---|---|
| A Pattern Language | 253 pattern files, figures, page metadata; partly hand-corrected | Good; spot-check |
| The Timeless Way of Building | 27 chapters, machine draft, 126 figure crops | Good prose; check pull-quote order and italics |
| NoO 1 Phenomenon of Life | Full; prologue and ch. 7 reviewed | Rest machine draft; visible OCR errors ("theretore") |
| NoO 2 Process of Creating Life | Full, machine draft | Noticeable OCR damage in places |
| NoO 3 Vision of a Living World | Full, machine draft; pp. 529–530 missing | Noisiest, especially captions |
| NoO 4 Luminous Ground | Full, machine draft | Mostly clean |

Not available: *Notes on the Synthesis of Form*, *The Oregon Experiment*, *The Production of Houses*, *A New Theory of Urban Design*, *Battle for the Life and Beauty of the Earth*. Works pages for these can still be written from secondary information and covers.

**Wilber Wiki pattern to copy** (`life-itself/wilber-wiki`): a roadmap page of acts with a dependency-ordered spine, a starred essential route and side branches, rendered with scoped CSS loaded through `config.json` `head`; concept pages with a short synthesis then 3–8 verbatim block-quoted excerpts; a mandatory quote-verification script; a works hub; `docs/plans/` for plans and Beads for tasks.

## Positioning

The wiki is about Alexander's vision, ideas and the pragmatics of building with them, not a catalogue of his work. The footer and About link out to the [CES Archive](https://christopher-alexander-ces-archive.org/) and [PatternLanguage.com](https://www.patternlanguage.com/).

## Decisions taken (small, reversible)

- **Excerpts liberally**, as Rufus asked. Every excerpt is copied from the source markdown, checked against the page scan (OCR is unreliable), and fixed upstream in the sources repo when wrong.
- **`docs/` excluded from the site** (`contentExclude`).
- **Living Neighborhoods: replace the link hub with the real collection.** Per Rufus's 25 Nov brief, the whole tidied collection is published here as a sub-directory, sourced from the `natureoforder/livingneighborhoods` conversion (about 48 of 209 pages converted so far). Until then, the three thin pages become one short entry page.
- **Concept-page shape**: `## Alexander's view` (short synthesis, our words) → `## In *<Book>*` (verbatim excerpts with book, chapter and printed page; figures where the book has them) → `## See also`. No invented exercises; editorial examples labelled as ours.
- **Fifteen properties**: one rich page per property with Alexander's examples and images, built from the existing page references.
- **Port Wilber's `verify_quotes.py`** with chapter-level source files, so a quote cited to the wrong chapter fails.
- **Design builds on what was accepted on 25 Nov**, not a restart: the *Pattern Language* interior typesetting and the Nature of Order emblem stay. Open items from that session: pattern-title font (WINDOW PLACE), navbar font and design, the site-wide look, and the front page. Rejected then: the red jacket palette and the Seeds of Renaissance theme. Follows Rufus's `designing-look-and-feel` skill: brand distilled first, then mood board, then front page.

## Site structure (target)

| Section | Contents |
|---|---|
| Home | Opening, ways in, credits at the foot (Christopher Alexander; David Gasquez and other helpers) |
| Roadmap | The way into Alexander's ideas (sketch below) |
| Concepts | Excerpt-led pages; index with ★ for core terms |
| Works | Hub plus one page per book: cover, summary, contents, key concepts, links to sources and readings |
| Patterns | The 253-pattern index, built out over time with problem, "Therefore" and connections |
| Build with Alexander | The pragmatics: how to make a room, a house, a hamlet with his ideas (patterns, sequences, on-site decisions, the architect-builder). Eishin and Mexicali as worked cases; cross-link to Living Neighborhoods. An aside on our own hamlet project (Petit Bois Martin), since learning to do this ourselves is part of why the wiki exists |
| Readings | Long excerpts in the Eishin style |
| Visionary | Why Alexander matters beyond architecture: a new view of matter, value and the self. Rufus's talks: "Pioneer of the Second Renaissance" (2024, youtube.com/watch?v=W5VMwrXA3H0) and "Second Renaissance Visionary" (Building Beauty group, 2026, youtube.com/watch?v=h_3cfdUR_l4) |
| Notes | Rufus's own notes and materials (Timeless Way notes, talks, Harvard debate) |
| Changelog, About | As now; About gains the design comparison |

## Roadmap sketch (to refine in its own design doc)

Acts, each titled with a plain claim, spine stops in dependency order, ★ for an essential route of six:

1. **Some places are more alive than others — and you can feel it.** ★ The quality without a name → being alive → the mirror of the self as the test. Visionary hook: Alexander treats this feeling as objective, a challenge to the mechanistic picture. Branch: early work (*Notes on the Synthesis of Form*, "A City is Not a Tree").
2. **Shared knowledge of what works.** Patterns of events and space → ★ a pattern language as a living language → the gate (the language is the gate) → the breakdown of language → *A Pattern Language* (branches: favourite patterns).
3. **Life is a structure of centers.** Patterns were his first answer; centers the deeper one. ★ Wholeness and centers → degrees of life → ★ the fifteen properties (branches: each property) → the properties in nature → living structure.
4. **Life is grown, not designed.** ★ Unfolding wholeness → structure-preserving transformations → sequences → generative codes → every part unique → deep feeling.
5. **The people who use a place must shape it.** The architect-builder and decisions made on site → *The Oregon Experiment*, *The Production of Houses* → money, contracts and the process system (Book 2 part 3) → Book 3's world: belonging, public space, neighborhoods, rooms → worked cases: Eishin, Mexicali. Links to Build with Alexander.
6. **The ground of it all.** ★ The "I" and the luminous ground → colour and inner light → ornament → making wholeness heals the maker. Payoff for the Visionary section.

Side rail: where Alexander is contested (the Eisenman debate, modernist critics, Book 1's empirical claims).

## Rights stance

Rufus has said to use excerpts liberally. Every excerpt and figure carries book, chapter and printed page, and the site credits Alexander and the Center for Environmental Structure on every page footer and in About, with a contact for takedown requests. Figures are Alexander's own drawings and photographs from the books; third-party photographs are credited as the book credits them.

## Work plan and order (revised with Rufus, 26 Nov)

The Nature of Order is the biggest and most mature structure, so it leads and *A Pattern Language* and *The Timeless Way* are brought in around it. Steps:

1. **Works listing.** The works hub and one page per work (cover, summary, contents, materials). Short texts we hold are stored in full beside their work entry: *A City is Not a Tree* (1965) and the 1982 Harvard debate with Peter Eisenman.
2. **In-depth analysis of the sources.** One compact digest per book in `docs/research/`: the argument chapter by chapter, the key concepts with their defining passages and pages, important figures, and links to the other books. NoO 1–4 first, then TWB and APL. The books are too big to read whole in one pass, so each digest is built chapter by chapter.
3. **Concept list.** Drawn from the digests. Rufus reviews the first 5–10 names, not the content.
4. **Roadmap(s)**, in a separate session. There are several ways in: the story of what Alexander was doing, the books in order, the ideas in dependency order. The sketch above is one candidate.
5. **Concept pages.** Pilots first (the quality without a name, centers, one property with images), then batches.
6. **Build with Alexander**, organised around Living Neighborhoods: room, house, hamlet, with our hamlet as an aside.

Running alongside: brand board and front page; Visionary page with the two talks; Notes and Changelog made visible. Done already: footer links to the CES Archive and PatternLanguage.com, About page, front-page credits.

## Open questions for Rufus

- Front-page design reference: the design mentioned in the brief was not found in the repo or Downloads.
