#!/usr/bin/env python3
"""
Verify every blockquote excerpt in concepts/*.md (and readings) is real text
from its cited chapter of the Alexander source books, at the cited page.

Ported from wilber-wiki's verify_quotes.py. Differences: sources are the
per-chapter Markdown files in the sibling `sources` repo, checking is
chapter-level, and the cited printed page is sanity-checked.

Usage:
    python3 skills/add-concept-page/scripts/verify_quotes.py [file-or-glob ...] [--strict]

    No arguments: checks concepts/*.md. --strict turns WARNINGs into failures.
    Exit code 0 if every quote passes, 1 if any fails.

Sources: $ALEXANDER_SOURCES (default: ../sources/texts relative to this repo,
i.e. /Users/rgrp/src/natureoforder/sources/texts).

Attribution line (last line of the blockquote):
    > — *The Phenomenon of Life*, ch. 5, "Fifteen Fundamental Properties", p. 150
    > — *A Pattern Language*, pattern 12, "Community of 7000", p. 78
The italic title picks the book. `ch. N` picks markdown/NN-*.md; `pattern NNN`
picks markdown/patterns/NNN-*.md. With no chapter, the whole book is searched
and a WARNING is printed. `p. N` / `pp. N-M` is the printed page where the
quote starts.

Matching: a quote is split on "..." / "…" into segments; each segment of
12+ characters must appear in the chapter (frontmatter stripped) after the
same normalisation as Wilber's: curly quotes -> straight, dashes -> hyphen,
**bold** and [^footnote] markers stripped, whitespace collapsed. *Italics*
are kept; a match that only works with italics stripped is accepted. A
trailing "." may stand in for the source's different closing punctuation; a
trailing quotation mark may not.

Page check: the chapter frontmatter `page_starts` gives, for each printed
page, a `before` anchor (text just after the page boundary). The quote's
first segment must lie at or after the cited page's anchor and before the
next page's anchor. If the anchors cannot be located the check is a WARNING.

Scan check is NOT done by this script. OCR is a machine draft: a quote that
passes here matches the markdown, which may itself be wrong. Always also
compare with the page scan (see SKILL.md).
"""
import glob
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCES = Path(os.environ.get("ALEXANDER_SOURCES") or REPO_ROOT.parent / "sources" / "texts")

# book slug (as used in `works:` frontmatter) -> directory under SOURCES
WORK_SOURCES = {
    "timeless-way-of-building": "timeless-way-of-building",
    "pattern-language": "pattern-language",
    "nature-of-order-1": "nature-of-order-01-the-phenomenon-of-life",
    "nature-of-order-2": "nature-of-order-02-the-process-of-creating-life",
    "nature-of-order-3": "nature-of-order-03-a-vision-of-a-living-world",
    "nature-of-order-4": "nature-of-order-04-the-luminous-ground",
}

# italic title in an attribution line -> book slug
WORK_TITLES = {
    "The Timeless Way of Building": "timeless-way-of-building",
    "A Pattern Language": "pattern-language",
    "The Phenomenon of Life": "nature-of-order-1",
    "The Process of Creating Life": "nature-of-order-2",
    "A Vision of a Living World": "nature-of-order-3",
    "The Luminous Ground": "nature-of-order-4",
}

MIN_SEGMENT_LEN = 12


def normalize(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\[\^[^\]]+\]", "", s)
    s = re.sub(r"<sup>.*?</sup>", "", s)  # reading-page note markers
    s = re.sub(r"</?(?:span|em|i|cite)\b[^>]*>", "", s)
    s = (
        s.replace("‘", "'").replace("’", "'")
        .replace("“", '"').replace("”", '"')
        .replace("–", "-").replace("—", "-")
    )
    return re.sub(r"\s+", " ", s).strip()


def strip_italics(s: str) -> str:
    return re.sub(r"\*(.+?)\*", r"\1", s)


def split_frontmatter(text: str):
    """Return (frontmatter_text, body)."""
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def page_starts(fm: str) -> list[dict]:
    out = []
    for line in fm.split("\n"):
        m = re.match(r"^\s*-\s*(\{.*\})\s*$", line)
        if m:
            try:
                out.append(json.loads(m.group(1)))
            except ValueError:
                pass
    return out


class Chapter:
    def __init__(self, path: Path):
        self.path = path
        fm, body = split_frontmatter(path.read_text())
        self.starts = page_starts(fm)
        self.text = normalize(body)
        self.loose = strip_italics(self.text)

    def variant(self, loose: bool) -> str:
        return self.loose if loose else self.text


_chapter_cache: dict[Path, Chapter] = {}


def chapter(path: Path) -> Chapter:
    if path not in _chapter_cache:
        _chapter_cache[path] = Chapter(path)
    return _chapter_cache[path]


def find_chapter_file(work: str, ch: str | None, pattern: str | None):
    """Return list of chapter files for the citation, or None if no ch/pattern given."""
    d = SOURCES / WORK_SOURCES[work] / "markdown"
    if pattern is not None:
        return sorted((d / "patterns").glob(f"{int(pattern):03d}-*.md"))
    if ch is not None:
        return sorted(d.glob(f"{int(ch):02d}-*.md"))
    return None


def whole_book(work: str) -> list[Path]:
    d = SOURCES / WORK_SOURCES[work] / "markdown"
    return sorted(d.glob("*.md")) + sorted((d / "patterns").glob("*.md"))


ATTR_RE = re.compile(r"^(?:—|--)\s*(.*)$")


def extract_quotes(text: str):
    """Yield (line_no, body, attribution_or_None) for each quotation.
    A quotation ends at its attribution line; trailing text with no
    attribution is yielded with None."""
    lines = text.split("\n")
    i, n = 0, len(lines)
    while i < n:
        if not lines[i].startswith(">"):
            i += 1
            continue
        start = i
        body: list[str] = []
        while i < n and lines[i].startswith(">"):
            s = lines[i][1:].strip()
            m = ATTR_RE.match(s)
            if m:
                if body:
                    yield start + 1, " ".join(body), s
                body, start = [], i + 1
            elif s:
                body.append(s)
            i += 1
        if body:
            yield start + 1, " ".join(body), None


def parse_attribution(attr: str):
    title = None
    m = re.search(r"\*([^*]+)\*", attr)
    if m:
        title = m.group(1).strip()
    ch = re.search(r"\bch\.?\s*(\d+)", attr)
    pat = re.search(r"\bpattern\s+(\d+)", attr, re.I)
    pg = re.search(r"\bpp?\.\s*(\d+)", attr)
    return (
        title,
        ch.group(1) if ch else None,
        pat.group(1) if pat else None,
        pg.group(1) if pg else None,
    )


def frontmatter_works(text: str) -> list[str]:
    fm, _ = split_frontmatter(text)
    m = re.search(r"^works:\s*\[(.*?)\]", fm, re.M)
    if not m:
        return []
    return [w.strip().strip("'\"") for w in m.group(1).split(",") if w.strip()]


def find_variants(seg: str, chap: Chapter):
    """Return (loose_flag, seg_in_that_variant) or None if not found."""
    for loose in (False, True):
        s = strip_italics(seg) if loose else seg
        t = chap.variant(loose)
        if s in t:
            return loose, s
        if s.endswith(".") and s[:-1] in t:
            return loose, s[:-1]
    return None


def anchor_pos(chap: Chapter, printed: str, loose: bool):
    """Position of the `before` anchor for a printed page, or None."""
    for e in chap.starts:
        if str(e.get("printed")) == str(printed):
            a = e.get("before")
            if not a:
                return None
            a = normalize(a)
            if loose:
                a = strip_italics(a)
            p = chap.variant(loose).find(a)
            return p if p >= 0 else None
    return None


def check_page(chap: Chapter, seg: str, loose: bool, page: str):
    """Return (ok, message). ok None means could not decide (warn)."""
    printed = {str(e.get("printed")): e for e in chap.starts}
    if str(page) not in printed:
        return None, f"printed page {page} not in {chap.path.name} page_starts"
    lo = anchor_pos(chap, page, loose)
    if lo is None:
        return None, f"cannot locate start anchor of p. {page} in {chap.path.name}"
    text = chap.variant(loose)
    hi = anchor_pos(chap, str(int(page) + 1), loose)
    if hi is None:
        hi = len(text)
    positions = [m.start() for m in re.finditer(re.escape(seg), text)]
    if any(lo <= p < hi for p in positions):
        return True, ""
    where = ", ".join(str(p) for p in positions[:3])
    return False, (
        f"quote starts outside printed p. {page} of {chap.path.name} "
        f"(chars {lo}-{hi}; found at {where})"
    )


def check_file(path: Path):
    """Return (failures, warnings)."""
    text = path.read_text()
    page_works = frontmatter_works(text)
    fails, warns = [], []
    nquotes = 0
    for lineno, body, attr in extract_quotes(text):
        nquotes += 1
        where = f"{path}:{lineno}"
        title = ch = pat = pg = None
        if attr:
            title, ch, pat, pg = parse_attribution(attr)
        else:
            warns.append(f"{where}: quote has no attribution line")
        work = WORK_TITLES.get(title) if title else None
        if title and not work:
            fails.append(f"{where}: UNKNOWN BOOK TITLE in attribution: *{title}*")
            continue
        if not work:
            cands = page_works
        else:
            cands = [work]
        cands = [w for w in cands if w in WORK_SOURCES]
        if not cands:
            fails.append(f"{where}: cannot tell which book this quote is from (add *Title* to the attribution or `works:`)")
            continue

        # Resolve files to search.
        files: list[Path] = []
        scoped = False
        for w in cands:
            sel = find_chapter_file(w, ch, pat) if (ch or pat) else None
            if sel:
                files += sel
                scoped = True
            elif sel == []:
                fails.append(f"{where}: no chapter file for {title or w} ch. {ch} / pattern {pat}")
        if (ch or pat) and not files:
            continue
        if not files:
            for w in cands:
                files += whole_book(w)
            warns.append(f"{where}: no chapter/pattern cited; searched whole book (cite `ch. N`)")
        if not any(f.exists() for f in files):
            fails.append(f"{where}: source files not found under {SOURCES} (set ALEXANDER_SOURCES)")
            continue

        norm = normalize(body)
        segs = [s.strip() for s in re.split(r"\.\.\.|…", norm)]
        segs = [s for s in segs if len(s) >= MIN_SEGMENT_LEN]
        first_hit = None
        for k, seg in enumerate(segs):
            hit = None
            for f in files:
                c = chapter(f)
                r = find_variants(seg, c)
                if r:
                    hit = (c, r)
                    break
            if not hit:
                snippet = seg if len(seg) < 100 else seg[:97] + "..."
                loc = f" (searched {files[0].name})" if scoped and len(files) == 1 else ""
                fails.append(f'{where}: NOT FOUND IN SOURCE{loc}: "{snippet}"')
            elif k == 0:
                first_hit = hit
        if first_hit and pg and scoped:
            c, (loose, s) = first_hit
            ok, msg = check_page(c, s, loose, pg)
            if ok is False:
                fails.append(f"{where}: WRONG PAGE: {msg}")
            elif ok is None:
                warns.append(f"{where}: page not checked: {msg}")
        elif first_hit and not pg:
            warns.append(f"{where}: no page cited")
    return fails, warns, nquotes


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    argv = [a for a in argv if a != "--strict"]
    if argv:
        files = [Path(p) for pat in argv for p in glob.glob(pat)]
    else:
        files = [Path(p) for p in glob.glob("concepts/*.md") if not p.endswith("index.md")]
    all_f, all_w, total = [], [], 0
    for f in sorted(files):
        fl, wl, n = check_file(f)
        all_f += fl
        all_w += wl
        total += n
    for w in all_w:
        print("WARNING:", w, file=sys.stderr)
    if strict:
        all_f += [f"(strict) {w}" for w in all_w]
    if all_f:
        print(f"FAIL: {len(all_f)} problem(s):\n")
        for f in all_f:
            print(" -", f)
        return 1
    print(f"PASS: {total} quote(s) in {len(files)} file(s) verified against {SOURCES} ({len(all_w)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
