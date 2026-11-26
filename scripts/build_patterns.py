#!/usr/bin/env python3
"""Build the A Pattern Language pages under /patterns from the reading edition.

Source: natureoforder/sources, texts/pattern-language/markdown (one file per
pattern, opening matter, section introductions, images). Run again whenever the
sources are corrected:

    python3 scripts/build_patterns.py [path/to/pattern-language/markdown]

Writes patterns/<slug>.md for all 253 patterns, the opening matter and section
pages, copies the images to assets/patterns/apl/ (lossless jpegtran pass), and
links every row of patterns/index.md. The hand-made pages listed in HAND keep
everything above the GENERATED marker; the full text is regenerated below it.

Needs Python 3.11+, pandoc and jpegtran.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "src/natureoforder/sources/texts/pattern-language/markdown"
OUT = ROOT / "patterns"
IMG_OUT = ROOT / "assets/patterns/apl"
IMG_URL = "/assets/patterns/apl/"
SOCIAL_OUT = ROOT / "assets/patterns/social"
SOCIAL_MIN = 400  # link-preview images: at least this many pixels on each side
HAND = {"window-place", "positive-outdoor-space"}
MARKER = "<!-- GENERATED: full text below is rebuilt by scripts/build_patterns.py; edit above this line -->"
CITATION = ("Christopher Alexander, Sara Ishikawa and Murray Silverstein, with Max Jacobson, Ingrid Fiksdahl-King and Shlomo Angel, "
            "<cite>A Pattern Language</cite> (Oxford University Press, 1977)")
STAR_WORDS = {1: "One star", 2: "Two stars"}
SECTIONS = [("Towns", 1, 94), ("Buildings", 95, 204), ("Construction", 205, 253)]

# --------------------------------------------------------------------------- sources


def read_source(path: Path) -> tuple[list[dict], str]:
    text = path.read_text()
    pages: list[dict] = []
    if text.startswith("---\n"):
        fm, text = text[4:].split("\n---\n", 1)
        for m in re.finditer(r"^\s*- (\{.*\})\s*$", fm, re.M):
            pages.append(json.loads(m.group(1)))
    return pages, text


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def load_patterns() -> dict[int, dict]:
    pats = {}
    for f in sorted((SRC / "patterns").glob("[0-9][0-9][0-9]-*.md")):
        num = int(f.name[:3])
        slug = f.stem[4:]
        pages, body = read_source(f)
        head = re.search(r"^# (\d+)\.\s*(.+?)\s*$", body, re.M)
        stars = head.group(2).count("★")
        pats[num] = dict(num=num, slug=slug, src=f, pages=pages, body=body, stars=stars,
                         heading=head.group(2).replace("★", "").strip())
    assert len(pats) == 253, len(pats)
    return pats


def site_titles() -> dict[int, str]:
    """Titles as already set in the index, so page titles match the index."""
    titles = {}
    for m in re.finditer(r"^\| (\d+) \| (?:\[)?(.+?)(?:\]\([^)]*\))? \| (\d+) \|$", (OUT / "index.md").read_text(), re.M):
        titles[int(m.group(1))] = m.group(2)
    return titles


# --------------------------------------------------------------------------- markdown passes

SRC_HREF = re.compile(r'href="(?:\.\./)?(?:patterns/)?(\d{3})-([a-z0-9-]+)\.md"')
REF = re.compile(r"([A-Z][A-Z0-9'’&,\-\. ]*[A-Z0-9'’])\s*\((\d{1,3})\)")


def map_links(h: str) -> str:
    return SRC_HREF.sub(lambda m: f'href="/patterns/{m.group(2)}"', h)


def match_title(name: str, num: int, pats: dict[int, dict]) -> tuple[int, int] | None:
    """Find the pattern a plain reference names. Returns (pattern, offset of the
    name within the matched text). Trims leading words ("Then ALCOVES"), accepts
    short forms ("LIGHT ON TWO SIDES" for 159) and, when the printed number is an
    OCR slip, a name that matches another title exactly."""
    words = name.split(" ")
    for i in range(len(words)):
        cand = norm(" ".join(words[i:]))
        if len(cand) < 4:
            break
        offset = len(" ".join(words[:i])) + (1 if i else 0)
        want = norm(pats[num]["heading"])
        if SequenceMatcher(None, cand, want).ratio() >= 0.75 or (len(cand) >= 8 and want.startswith(cand)):
            return num, offset
        exact = [n for n, q in pats.items() if norm(q["heading"]) in (cand, cand.rstrip("s"))]
        if len(exact) == 1:
            return exact[0], offset
    return None


def link_plain_refs(h: str, pats: dict[int, dict]) -> str:
    """Link references the source left as plain text, such as ALCOVES (179)."""
    parts = re.split(r"(<[^>]+>)", h)
    depth = 0
    for k, part in enumerate(parts):
        if part.startswith("<"):
            if re.match(r"<a\b", part):
                depth += 1
            elif part.startswith("</a"):
                depth -= 1
            continue
        if depth or not part:
            continue

        def sub(m: re.Match) -> str:
            num = int(m.group(2))
            if num not in pats:
                return m.group(0)
            hit = match_title(m.group(1), num, pats)
            if not hit:
                return m.group(0)
            n, off = hit
            return f'{m.group(0)[:off]}<a href="/patterns/{pats[n]["slug"]}">{m.group(0)[off:]}</a>'

        parts[k] = REF.sub(sub, part)
    return "".join(parts)


SOLUTION_LEAD = re.compile(r"^(Therefore|Namely|Seriously though)\s*[:;,.]\s*$")


def bold_solution(md: str) -> str:
    """The book sets the problem statement and the solution in bold. The source
    mostly does too; fill the gaps. The solution is the paragraph(s) after a
    standalone 'Therefore:' (or 'Therefore, ...' when there is none); the problem
    is the first paragraph after the first divider, or the italic opening."""
    blocks = md.split("\n\n")
    lead = next((i for i, b in enumerate(blocks) if SOLUTION_LEAD.match(b.strip())), None)
    if lead is not None:
        blocks[lead] = "Therefore:" if blocks[lead].strip().startswith("Therefore") else blocks[lead].strip()
        j = lead + 1
        while j < len(blocks) and not blocks[j].lstrip().startswith(("![", "⟦DIVIDER")):
            blocks[j] = embolden(blocks[j])
            j += 1
    else:
        for i, b in enumerate(blocks):
            m = re.match(r"^Therefore\s*[,;:]\s+(\S.*)$", b.strip(), re.S)
            if m:
                blocks[i] = "Therefore:\n\n" + embolden(m.group(1))
                lead = i
                break
    end = lead if lead is not None else len(blocks)
    is_bold = lambda b: split_mark(b)[1].startswith("**") and b.strip().endswith("**")
    if not any(is_bold(b) for b in blocks[:end]):
        div = next((i for i, b in enumerate(blocks[:end]) if b.strip() == "⟦DIVIDER⟧"), None)
        if div is not None and div + 1 < end:
            blocks[div + 1] = embolden(blocks[div + 1])
        else:
            for i, b in enumerate(blocks[:end]):
                mark, s = split_mark(b)
                if re.fullmatch(r"\*[^*].*[^*]\*", s, re.S):
                    blocks[i] = embolden(mark + s[1:-1])
                    break
    return "\n\n".join(blocks)


def embolden(p: str) -> str:
    mark, p = split_mark(p)
    if not p or p.startswith("**") or p.startswith("#"):
        return mark + p
    return mark + "**" + p.replace("**", "") + "**"


def split_mark(p: str) -> tuple[str, str]:
    """Separate a leading page sentinel from a paragraph."""
    m = re.match(r"((?:⟦P:[^⟧]+⟧)?)(.*)", p.strip(), re.S)
    return m.group(1), m.group(2).strip()


def insert_page_marks(md: str, pages: list[dict], skip_first: bool) -> str:
    """Put a sentinel where each printed page begins, from the boundary quotations."""
    pos = 0
    for k, pg in enumerate(pages):
        if pg.get("printed") is None or (skip_first and k == 0):
            continue
        before = re.sub(r"\s*\.\.\.\s*$", "", pg["before"]).strip()
        words = before.split()[:6]
        rx = r"\s+".join(re.escape(w) for w in words)
        m = re.compile(rx).search(md, pos)
        if not m:
            print(f"  page {pg['printed']}: boundary not found", file=sys.stderr)
            continue
        i = m.start()
        mark = f"⟦P:{pg['printed']}⟧"
        at_block = i == 0 or md[max(0, i - 2):i] == "\n\n"
        token = md[i:].split(None, 1)[0]
        if at_block and (token.startswith(("#", "![", "|", "-", "[")) or re.match(r"^(\d+\\?\.|[A-Z]\.)$", token)):
            md = md[:i] + mark + "\n\n" + md[i:]
            pos = i + len(mark) + 2
        else:
            md = md[:i] + mark + md[i:]
            pos = i + len(mark)
    return md


def staricon_to_divider(md: str) -> str:
    return re.sub(r"!\[[^\]]*\]\((?:\.\./)?media/img/staricon\.jpg\)", "⟦DIVIDER⟧", md)


# --------------------------------------------------------------------------- html


def img_name(src: str) -> str:
    return re.sub(r"[()]", "", Path(src).name)


def pandoc(md: str) -> str:
    r = subprocess.run(["pandoc", "-f", "markdown+smart-implicit_figures", "-t", "html5", "--wrap=none"],
                       input=md, capture_output=True, text=True, check=True)
    return r.stdout


SIZES: dict[str, tuple[int, int]] = {}


def img_size(name: str) -> tuple[int, int]:
    if name not in SIZES:
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(IMG_OUT / name)],
                             capture_output=True, text=True).stdout
        w = int(re.search(r"pixelWidth: (\d+)", out).group(1))
        h = int(re.search(r"pixelHeight: (\d+)", out).group(1))
        SIZES[name] = (w, h)
    return SIZES[name]


def img_tag(src: str, alt: str, lazy: bool = True) -> str:
    name = img_name(src)
    w, h = img_size(name)
    load = ' loading="lazy"' if lazy else ""
    return f'<img src="{IMG_URL}{name}" width="{w}" height="{h}" alt="{html.escape(alt, quote=True)}"{load} />'


def finish_html(h: str, title: str) -> str:
    # figures: an image alone in a paragraph, with a following one-line italic caption folded in
    def fig(m: re.Match) -> str:
        src = m.group(1)
        cap = m.group(2)
        page = m.group(3)
        if cap:
            alt = re.sub(r"<[^>]+>", "", cap).strip().rstrip(".")
            alt = alt[:1].upper() + alt[1:]
            capt = f"<figcaption>{cap}</figcaption>"
        else:
            alt, capt = f"Illustration for {title}", ""
        return f'<figure class="pl-figure">{img_tag(src, alt)}{capt}</figure>'

    h = re.sub(r'<p><img src="([^"]+)"[^>]*/?></p>\s*(?:<p>(<em>[^<]{1,220}</em>\.?)</p>)?()', fig, h)
    h = re.sub(r'<img src="([^"]+)"[^>]*/?>', lambda m: img_tag(m.group(1), f"Illustration for {title}"), h)
    h = h.replace("<p>⟦DIVIDER⟧</p>", '<p class="pl-divider" aria-hidden="true">◆ ◆ ◆</p>').replace("⟦DIVIDER⟧", "")
    h = re.sub(r"<p>⟦P:([^⟧]+)⟧</p>", r'<p class="pl-pagebreak"><span class="pl-page" title="Page \1 of the 1977 edition">\1</span></p>', h)
    h = re.sub(r"⟦P:([^⟧]+)⟧", r'<span class="pl-page" title="Page \1 of the 1977 edition">\1</span>', h)
    h = h.replace(' href="/patterns/', ' class="pl-ref" href="/patterns/')
    # one HTML block for Flowershow: no blank lines, no deep indentation
    return "\n".join(line.strip() for line in h.splitlines() if line.strip())


# --------------------------------------------------------------------------- pages


def stars_html(n: int) -> str:
    return f' · <span aria-label="{STAR_WORDS[n]}">{"*" * n}</span>' if n else ""


def section_of(num: int) -> str:
    return next(name for name, a, b in SECTIONS if a <= num <= b)


def pattern_body(p: dict, pats: dict, titles: dict) -> tuple[str, str | None, list[int], str]:
    md = p["body"]
    md = re.sub(r"^# \d+\..*\n", "", md, count=1, flags=re.M).lstrip()
    opening = None
    m = re.match(r"!\[[^\]]*\]\(([^)]+)\)\s*", md)
    if m:
        opening, md = m.group(1), md[m.end():]
    md = insert_page_marks(md, p["pages"], skip_first=True)
    md = staricon_to_divider(md)
    md = bold_solution(md)
    # first bold paragraph is the problem statement: use it for the description
    prob = re.search(r"^(?:⟦P:[^⟧]+⟧)?\*\*(.+?)\*\*\s*$", md, re.M)
    desc = re.sub(r"[*_⟦⟧]|P:\S+", "", prob.group(1)).strip() if prob else ""
    body = link_plain_refs(map_links(pandoc(md)), pats)
    slugs = {q["slug"]: n for n, q in pats.items()}
    refs = []
    for s in re.findall(r'href="/patterns/([a-z0-9-]+)"', body):
        n = slugs.get(s)
        if n and n != p["num"] and n not in refs:
            refs.append(n)
    refs.sort()
    return finish_html(body, titles[p["num"]]), opening, refs, desc


def ref_list(nums: list[int], pats: dict, titles: dict) -> str:
    return "<ul>" + "".join(f'<li><a href="/patterns/{pats[n]["slug"]}"><span class="pl-num">{n}</span> {html.escape(titles[n])}</a></li>' for n in nums) + "</ul>"


def connections(num: int, out: dict, inc: dict, pats: dict, titles: dict) -> str:
    parts = ['<nav class="pattern-links" aria-label="Connections">']
    if out[num]:
        parts.append(f"<h2>Links to</h2>{ref_list(out[num], pats, titles)}")
    if inc[num]:
        parts.append(f"<h2>Linked from</h2>{ref_list(sorted(inc[num]), pats, titles)}")
    parts.append("</nav>")
    return "".join(parts)


def neighbours(num: int, pats: dict, titles: dict) -> str:
    bits = []
    if num > 1:
        bits.append(f'<a href="/patterns/{pats[num-1]["slug"]}">← {num-1} {html.escape(titles[num-1])}</a>')
    bits.append('<a href="/patterns">All 253 patterns</a>')
    if num < 253:
        bits.append(f'<a href="/patterns/{pats[num+1]["slug"]}">{num+1} {html.escape(titles[num+1])} →</a>')
    return '<p class="pattern-nav">' + " · ".join(bits) + "</p>"


def page_range(p: dict) -> str:
    printed = [pg["printed"] for pg in p["pages"] if isinstance(pg.get("printed"), int)]
    return f"{printed[0]}–{printed[-1]}" if len(printed) > 1 else str(printed[0])


def social_image(slug: str, src: str | None) -> str | None:
    """Link-preview image for a page: the opening photograph, enlarged (only
    for the preview copy) so its short side is at least SOCIAL_MIN pixels."""
    if not src:
        return None
    name = img_name(src)
    w, h = img_size(name)
    if min(w, h) >= SOCIAL_MIN:
        return IMG_URL + name
    SOCIAL_OUT.mkdir(parents=True, exist_ok=True)
    dst = SOCIAL_OUT / f"{slug}.jpg"
    if not dst.exists() or dst.stat().st_mtime < (IMG_OUT / name).stat().st_mtime:
        width = -(-w * SOCIAL_MIN // min(w, h))
        subprocess.run(["sips", "--resampleWidth", str(width), str(IMG_OUT / name), "--out", str(dst)],
                       capture_output=True, check=True)
    return f"/assets/patterns/social/{slug}.jpg"


def write_pattern(p: dict, body: str, opening: str | None, desc: str, pats, titles, out, inc) -> None:
    num, slug, title = p["num"], p["slug"], titles[p["num"]]
    first = p["pages"][0]["printed"]
    source = (f'<div class="pattern-source"><p>{CITATION}, pattern {num}, pp. {page_range(p)}. '
              f'Text and illustrations from the <a href="https://github.com/natureoforder/sources">Nature of Order sources</a> reading edition, transcribed from the 1977 printing; '
              f'report errors on <a href="https://github.com/natureoforder/alexander-wiki/issues">GitHub</a>.</p>{neighbours(num, pats, titles)}</div>')
    conn = connections(num, out, inc, pats, titles)
    text = f'<article class="pattern-text" aria-label="The text of {html.escape(title)}">{body}</article>'
    path = OUT / f"{slug}.md"
    first_fig = re.search(r'<img src="%s([^"]+)"' % re.escape(IMG_URL), body)
    image = social_image(slug, opening or (first_fig and first_fig.group(1)))
    if slug in HAND:
        existing = path.read_text()
        if image and not re.search(r"^image:", existing.split("\n---\n", 1)[0], re.M):
            existing = existing.replace("\nlayout: plain\n", f"\nimage: {image}\nlayout: plain\n", 1)
        if MARKER in existing:
            head = existing.split(MARKER)[0].rstrip()
        else:  # first run: drop the closing source block and wrapper, keep frontmatter, plate and commentary
            head = existing.rstrip()
            head = re.sub(r"\n<(?:div|section) class=\"pattern-source\".*\Z", "", head, flags=re.S).rstrip()
        fig = (f'<figure class="pattern-figure pl-figure">{img_tag(opening, f"Opening photograph for {title}")}'
               f'<figcaption>Opening photograph, p. {first}.</figcaption></figure>') if opening and slug != "window-place" else ""
        page = (f"{head}\n{MARKER}\n"
                f'<div class="pattern-spread pattern-full">'
                f'<section class="pattern-plate"><p class="pattern-meta">The full pattern · p. {first}</p>{fig}{conn}</section>'
                f"{text}</div>\n{source}\n</div>\n")
    else:
        fig = (f'<figure class="pattern-figure pl-figure">{img_tag(opening, f"Opening photograph for {title}", lazy=False)}</figure>') if opening else ""
        fm = (f"---\ntitle: {json.dumps(title)}\n"
              f"description: {json.dumps(f'Pattern {num} of A Pattern Language (1977), in full. ' + desc)}\n"
              + (f"image: {image}\n" if image else "")
              + "layout: plain\n---\n\n")
        page = (fm + f'<div class="pattern-reading pattern-full">\n'
                f'<div class="pattern-spread">'
                f'<section class="pattern-plate" aria-labelledby="t-{slug}">'
                f'<p class="pattern-meta"><a href="/patterns">A Pattern Language</a> · <a href="/patterns#{section_of(num).lower()}">{section_of(num)}</a> · Pattern {num} · p. {first}{stars_html(p["stars"])}</p>'
                f'<h1 class="pattern-title" id="t-{slug}">{html.escape(title)}</h1>{fig}{conn}</section>'
                f"{text}</div>\n{source}\n</div>\n")
    path.write_text(page)


EXTRA = [
    # (out slug, title, source file, start heading, end heading or None, description)
    ("using-this-book", "Using This Book", "using-this-book.md", "# USING THIS BOOK", "## SUMMARY OF THE LANGUAGE",
     "The authors' guide to A Pattern Language: what a pattern is, how the patterns connect, and how to read them."),
    ("summary-of-the-language", "Summary of the Language", "using-this-book.md", "## SUMMARY OF THE LANGUAGE", "## CHOOSING A LANGUAGE FOR YOUR PROJECT",
     "All 253 patterns of A Pattern Language in sequence, with the sentences that connect each group to the next."),
    ("choosing-a-language", "Choosing a Language for Your Project", "using-this-book.md", "## CHOOSING A LANGUAGE FOR YOUR PROJECT", None,
     "How to choose patterns from A Pattern Language for your own project, and the poetry of the language."),
    ("towns", "Towns", "towns.md", "# TOWNS", None, "The introduction to the Towns section of A Pattern Language: patterns 1 to 94."),
    ("buildings", "Buildings", "buildings.md", "# **BUILDINGS**", None, "The introduction to the Buildings section of A Pattern Language: patterns 95 to 204."),
    ("construction", "Construction", "construction.md", "# CONSTRUCTION", None, "The introduction to the Construction section of A Pattern Language: patterns 205 to 253."),
    ("acknowledgments", "Acknowledgments", "acknowledgments.md", "# Acknowledgments", None,
     "The authors' acknowledgments and the photographers whose pictures appear in A Pattern Language."),
]
EXTRA_NAV = ["using-this-book", "summary-of-the-language", "choosing-a-language", "towns", "buildings", "construction", "acknowledgments"]


def write_extra(slug, title, fname, start, end, desc, pats, titles) -> None:
    pages, body = read_source(SRC / fname)
    md = insert_page_marks(body, pages, skip_first=False)
    a = md.index(start)
    # a page mark placed just before the start heading belongs to this part
    pre = re.search(r"⟦P:[^⟧]+⟧\n\n$", md[:a])
    a = pre.start() if pre else a
    b = md.index(end) if end else len(md)
    preb = re.search(r"⟦P:[^⟧]+⟧\n\n$", md[:b]) if end else None
    b = preb.start() if preb else b
    md = md[a:b].strip()
    md = re.sub(r"^=+\s*$", "", md, flags=re.M)
    md = re.sub(r"^#+ .*$", "", md, count=1, flags=re.M)  # the page prints its own title
    md = staricon_to_divider(md)
    body_html = finish_html(link_plain_refs(map_links(pandoc(md)), pats), title)
    i = EXTRA_NAV.index(slug)
    nav = []
    if i > 0:
        p = next(e for e in EXTRA if e[0] == EXTRA_NAV[i - 1])
        nav.append(f'<a href="/patterns/{p[0]}">← {p[1]}</a>')
    nav.append('<a href="/patterns">All 253 patterns</a>')
    if i < len(EXTRA_NAV) - 1:
        n = next(e for e in EXTRA if e[0] == EXTRA_NAV[i + 1])
        nav.append(f'<a href="/patterns/{n[0]}">{n[1]} →</a>')
    printed = [str(p["printed"]) for p in pages if p.get("printed")]
    fm = f"---\ntitle: {json.dumps(title)}\ndescription: {json.dumps(desc)}\nlayout: plain\n---\n\n"
    page = (fm + '<div class="pattern-reading pattern-full pattern-essay">\n'
            f'<p class="pattern-meta"><a href="/patterns">A Pattern Language</a></p>'
            f'<h1 class="pattern-title">{html.escape(title)}</h1>'
            f'<article class="pattern-text">{body_html}</article>\n'
            f'<div class="pattern-source"><p>{CITATION}.</p><p class="pattern-nav">{" · ".join(nav)}</p></div>\n</div>\n')
    (OUT / f"{slug}.md").write_text(page)


def link_index(pats, titles) -> None:
    idx = OUT / "index.md"
    t = idx.read_text()
    t = re.sub(r"^\| (\d+) \| (?:\[)?(.+?)(?:\]\([^)]*\))? \| (\d+) \|$",
               lambda m: f"| {m.group(1)} | [{m.group(2)}](/patterns/{pats[int(m.group(1))]['slug']}) | {m.group(3)} |", t, flags=re.M)
    idx.write_text(t)


def copy_images() -> None:
    IMG_OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted((SRC / "media/img").iterdir()):
        if f.name in {"staricon.jpg", "cover.jpg"} or f.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        dst = IMG_OUT / img_name(f.name)
        if dst.exists() and dst.stat().st_mtime >= f.stat().st_mtime:
            continue
        if f.suffix.lower() in {".jpg", ".jpeg"}:
            subprocess.run(["jpegtran", "-copy", "none", "-optimize", "-outfile", str(dst), str(f)], check=True)
        else:
            shutil.copy2(f, dst)


def main() -> None:
    copy_images()
    pats = load_patterns()
    titles = site_titles()
    assert len(titles) == 253, len(titles)
    built = {n: pattern_body(p, pats, titles) for n, p in pats.items()}
    out = {n: b[2] for n, b in built.items()}
    inc: dict[int, set] = {n: set() for n in pats}
    for n, refs in out.items():
        for r in refs:
            inc[r].add(n)
    for n, p in pats.items():
        body, opening, _, desc = built[n]
        write_pattern(p, body, opening, desc, pats, titles, out, inc)
    for e in EXTRA:
        write_extra(*e, pats, titles)
    link_index(pats, titles)
    links = sum(len(v) for v in out.values())
    print(f"253 patterns, {len(EXTRA)} other pages, {links} distinct pattern-to-pattern links")


if __name__ == "__main__":
    main()
