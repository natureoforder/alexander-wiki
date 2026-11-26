---
title: Alexander Wiki design brief
date: 2026-11-26
beads: alex-88s.19.5
---

# Alexander Wiki design brief

The pieces of design work, each judged against the [brand](2026-11-26-brand.md). Method: the `designing-look-and-feel` skill. Session brief: [2026-11-26-design-session-brief.md](2026-11-26-design-session-brief.md).

## Pieces

1. **Global type and colour.** The base CSS every page inherits. Check the type and spacing against the best reading sites, not only against the book. Settle whether there is an accent colour and what it is used for.
2. **Navbar.** Rufus: "needs some work… probably a different font". It is generic today. Restyle the markup Flowershow already outputs: emblem, name, links, one rule, and a working menu on phones.
3. **Pattern titles.** Rufus: WINDOW PLACE "need a different font". On p. 833 the title is set in full capitals, widely spaced, flush left, with oldstyle figures. Ours mixes Caslon with small capitals and is centred.
4. **Works index.** Rufus: "design of works index page is important - could be by time but in a grid too and beautiful". There are 15 covers (`assets/covers/`; the filenames stay stable through the high-res pass), plus essays and talks, grouped into six periods, with a chronology table. Index pages work at two levels, the overview and each work's page, and the design should serve both. Keep its classes `works-*`.
5. **Front page.** Rufus doesn't want it reworked much. Only light changes that follow from 1–3, and better use of the books' pictures where that helps.

## Constraints

- Flowershow: scoped CSS in `custom.css`, raw HTML in `layout: plain` pages, no scripts in `.md`.
- Phone and desktop are equal. Check at 390 and 1440 px.
- Light mode only. Reading pages should print cleanly.
- Book pictures carry a credit line (book, page).
- Other sessions edit this repo, so keep changes scoped and rebase on `main` before merging.

## Method

1. A small mood board: pages from the books, a few websites that do type, spacing and hypertext really well, and 1–2 anti-references.
2. Two directions on the same page, each shown as navbar, pattern title, a reading paragraph and the Works index, with one recommended.
3. Rufus picks. Build the pick and check it in a browser on desktop and phone.

**Done when:** the brand, board, directions and Rufus's pick are recorded. Pieces 1–4 are built, plus any light front-page changes. `about/design.md` is updated, everything has been checked on desktop and phone, merged to `main` and pushed, and Beads is synced.
