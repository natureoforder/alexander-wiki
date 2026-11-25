# Working on Alexander Wiki

Keep each Markdown paragraph on one line. Write concept entries in original prose, cite specific works and passages, and distinguish editorial examples from Alexander's own. Keep collection pages traceable to the authors and original URLs.

Track work in Beads and order dependencies with bd dep. At session close fetch, push Git and verify Beads sync. The pre-push hook runs bd dolt push, which is also the manual fallback.
## Changelog

At session end, only log new features or significant reader-facing changes
(behaviour, fixes to materially broken functionality, or public content).
Skip polish, tidying, and small fixes as standalone entries; include them only
as supporting detail in a larger feature or release announcement that qualifies
on its own. Planning/research/design must itself be a significant public
deliverable. When unsure, skip.

Use `changelog/YYYY-MM-DD-slug.md` with `date`/`title`/`promote` frontmatter:
a plain-text title, one or two reader-facing sentences, a live link where
available, and consider a screenshot for visual work. Substantial announcements
can use paragraphs or bullets. Omit internal implementation detail. For the
first entry or when the format is unclear, fetch and follow
https://raw.githubusercontent.com/life-itself/changelog/main/CONVENTION.md
