---
title: Design session brief
date: 2026-11-26
beads: alex-88s.19.5
---

# Design session brief

**Goal.** Give the Alexander Wiki a distilled brand that feels like Alexander, and apply it to the front page, the titles and the navbar, using Rufus's design-skill approach.

**Done-check.** A brand doc with mood board (`docs/plans/2026-11-26-brand.md` plus images in `docs/plans/brand/`) showing 2–3 directions inside the brief, with Rufus's pick recorded. The chosen direction applied to the front page, pattern-title font, navbar and global CSS, and checked in a browser on desktop and phone. Committed, merged to `main`, pushed, Beads synced.

## Method

Load and follow the `designing-look-and-feel` skill (Rufus's design skill). Distil the brand first, then the mood board, then build. Show Rufus the directions before building. Use a subagent to critique the board before showing it.

## What is already decided (from the 25 Nov Codex session)

- **Accepted as shippable:** typesetting after the interior of *A Pattern Language* (EB Garamond, small-capital titles, oldstyle figures, generous spacing; see `about/design.md`). Also the plate-and-commentary spread for patterns (stacked on phones), and the *Nature of Order* emblem as logo ("logo is good"). Rufus wants "this approach on whole site (maybe not side by side but general look)".
- **Rejected:** the red jacket palette ("where is this weird red coming from"), the first landing pages ("this looks terrible"), and the Seeds of Renaissance theme. He asked for something "more tufte like or alexander like".
- **Still open:**
  - Pattern titles such as WINDOW PLACE "need a different font".
  - Navbar "needs some work… probably a different font".
  - Front page: a beautiful opening with images from the books.
  - Whether colour has a place. *A Pattern Language*'s yellow Oxford jacket is a reference, and *The Nature of Order*, especially Book 4 on colour and inner light, is full of colour. The current "no colour except in figures" rule is up for review.

## References

- *A Pattern Language* interior: the PDF is in the `natureoforder/sources` private release (see `~/src/natureoforder/sources/texts/pattern-language/README.md`); page images in `assets/design/`.
- Oxford jacket: `assets/pattern-language-jacket.jpg`. Emblem: `assets/nature-of-order-mark.png`.
- *Nature of Order* figures: `~/src/natureoforder/sources/texts/nature-of-order-0*/markdown/figures/`.
- Book covers being gathered now under `assets/covers/` by the works task.
- Current CSS: `custom.css`. Flowershow notes: `layout: plain` keeps the navbar and footer; `<script>` does not run in `.md`; use scoped CSS, not arbitrary Tailwind classes.

## Coordination

Other work touches the same repo: works pages (`works/`), Visionary, and concept pages. Keep CSS changes scoped and easy to merge, and rebase on `main` before merging.
