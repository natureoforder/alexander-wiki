import os, sys
root = sys.argv[1]
def exists(slug): return os.path.exists(f"{root}/concepts/{slug}.md")
def title(name, slug, cls):
    if slug.startswith('/'): return f'<a href="{slug}" class="{cls}">{name}</a>'
    if exists(slug): return f'<a href="/concepts/{slug}" class="{cls}">{name}</a>'
    return f'<span class="{cls}">{name}</span>'
def branch(name, slug, note):
    live = slug.startswith('/') or exists(slug)
    tag, href = ('a', f' href="{slug if slug.startswith("/") else "/concepts/"+slug}"') if live else ('span', '')
    coming = '' if live else ' <span class="ar-coming">(coming)</span>'
    return f'<{tag}{href} class="ar-branch{"" if live else " is-coming"}"><span class="ar-branch__title">{name}{coming}</span><span class="ar-branch__note">{note}</span></{tag}>'

PROPS = [("Levels of scale","levels-of-scale"),("Strong centers","strong-centers"),("Boundaries","boundaries"),("Alternating repetition","alternating-repetition"),("Positive space","positive-space"),("Good shape","good-shape"),("Local symmetries","local-symmetries"),("Deep interlock and ambiguity","deep-interlock-and-ambiguity"),("Contrast","contrast"),("Gradients","gradients"),("Roughness","roughness"),("Echoes","echoes"),("The void","the-void"),("Simplicity and inner calm","simplicity-and-inner-calm"),("Not-separateness","not-separateness")]

ACTS = [
 ("I", "Is that feeling telling you something true?", "Everyone knows that some places feel more alive than others. Alexander’s first and largest claim is that this feeling is not just taste: it registers something real, in the place and in us.", [
  (1, True, "Life", "quality-without-a-name", "the quality without a name", "Start here. What the best places share: nothing in them is at war with itself. In 1979 he said it could not be named; by 2002 he called it simply life, and said that everything has more of it or less.", [("Being alive","being-alive","you know the quality first in yourself"),("Value is objective","value-is-objective","why statements about life can be true or false")]),
 ]),
 ("II", "What is it in a place that you are feeling?", "If the feeling is real, it must answer to something in the thing itself. <em>The Phenomenon of Life</em>, the first book of <em>The Nature of Order</em>, names that structure.", [
  (2, False, "Wholeness", "wholeness", None, "Before the parts, the whole: every coherent part of a place, nested and overlapping, taken together.", [("Semilattice","semilattice","“A City is Not a Tree”, 1965: real wholes overlap")]),
  (3, True, "Centers", "centers", None, "The units wholeness is made of. Each center is made of other centers, and grows stronger as its neighbors do.", []),
  (4, True, "The fifteen properties", "fifteen-properties", None, "Fifteen ways centers help each other come to life, found in good buildings, old carpets and nature alike.", "PROPS"),
  (5, False, "The mirror of the self", "mirror-of-the-self", None, "A test you can run yourself: of two things, which is the better picture of your whole self?", [("Deep feeling","deep-feeling","feeling, not opinion, as the instrument")]),
  (6, False, "Living structure", "living-structure", None, "What a thing is like when its centers help one another densely. Nature has it everywhere; only we can make things without it.", [("Ornament and function","ornament-and-function","not two things but one")]),
 ]),
 ("III", "How does such a thing get made?", "Living structure cannot be drawn up and assembled; it has to be grown. <em>The Process of Creating Life</em> asks how. <em>The Timeless Way of Building</em> (1979) and <em>A Pattern Language</em> (1977, with Sara Ishikawa, Murray Silverstein and others) come in here as the first answer.", [
  (7, True, "Structure-preserving transformations", "structure-preserving-transformations", "each step makes the whole more alive", "The single good step: strengthen something already latent in the whole. The fifteen properties return here as fifteen kinds of step.", []),
  (8, False, "Living process", "living-process", None, "One process, repeated thousands of times: look at the whole, strengthen one center, check, and look again.", [("Every part unique","every-part-unique","the same patterns repeat, the parts never do"),("Form language","form-language","a shared vocabulary of shapes, which he said he had not worked out")]),
  (9, False, "Pattern language", "pattern-language", None, "Shared knowledge of what works, linked from regions down to rooms, so that ordinary people can use it. Worked out with his colleagues at the Center for Environmental Structure in the 1970s, and still how most people meet the work.", [("Patterns","patterns","one pattern: a problem and the core of its solution"),("The gate","the-gate","learn the language, then let it go"),("Piecemeal growth","piecemeal-growth","towns grown by many small acts"),("All 253 patterns","/patterns","the index to <em>A Pattern Language</em>")]),
  (10, False, "Generative codes", "generative-codes", None, "Patterns put in order: pattern languages (from the late 1960s), then sequences (about 1990), then codes a community can follow step by step (about 2002).", [("Sequences","sequences","the order of the steps decides whether it works")]),
 ]),
 ("IV", "Who makes it, so that people belong there?", "A living world needs millions of people making it, not a few designers. <em>A Vision of a Living World</em> shows what that looks like; <em>The Process of Creating Life</em> says what stands in the way.", [
  (11, True, "Belonging", "belonging", None, "What it is all for: the sense that the world is ours and we have a right to be in it.", []),
  (12, False, "People shaping their own places", "people-shaping-their-own-places", None, "The people who will use a place lay it out themselves, on the ground, with a language they share.", [("The architect-builder","architect-builder","design and building done by the same hands"),("The Eishin campus","/practice/eishin-campus","a school laid out by Alexander and his colleagues with its teachers and students")]),
  (13, False, "The modern building process", "modern-building-process", None, "Why it is so hard now: drawings, loans, contracts and rules that stop anyone adjusting as they go, and how he thought that could change.", []),
 ]),
 ("V", "Is the life in things also a kind of self?", "In <em>The Luminous Ground</em> Alexander says what he thinks all this implies about matter itself. He offers it as a hypothesis, and says plainly that he has doubts.", [
  (14, True, "The “I”", "the-i", None, "One self-like ground beneath things, which every living center opens onto.", [("The mechanistic world-picture","mechanistic-world-picture","what he is arguing against"),("Color and inner light","color-and-inner-light","where unity can most nearly be seen"),("Pleasing yourself","pleasing-yourself","the most personal turns out the most objective")]),
 ]),
]

# Shorter trails, each on its own page at /roadmap/<slug>, drawn from the same stops.
TRAILS = [
 ("make-a-place", "To make a place", "For anyone shaping a house, a garden, a school or a street.",
  "For anyone shaping a house, a garden, a school or a street. It starts with who does the making, then the tools: patterns, centers, the fifteen properties, and the step-by-step process that ties them together.",
  [12,9,3,4,7,8]),
 ("thesis", "The thesis", "His central claim, in five steps.",
  "Alexander’s central claim in five steps: that the life we feel in some places is real, that you can test for it, what it is made of, how it is made, and what he came to think it says about the world.",
  [1,5,6,7,14]),
 ("from-patterns", "From patterns or software", "From the patterns you know to what came after.",
  "Many people meet Alexander through pattern languages, in architecture or in software, where they inspired design patterns and the first wiki. This trail starts there and follows the work on: why he came to think patterns were not enough, and what he did next.",
  [9,3,10,8]),
]
names = {s[0]: s[2] for a in ACTS for s in a[3]}
stops_by_n = {s[0]: s for a in ACTS for s in a[3]}

def node(stop, href_note=None):
    n, star, name, slug, gloss, body, branches = stop
    live = exists(slug)
    cls = 'ar-node' + (' ar-node--star' if star else '') + ('' if live else ' is-coming')
    head = title(name, slug, 'ar-node__title') + ('&nbsp;<img src="/assets/nature-of-order-mark.png" class="ar-mark" alt="on the short route" />' if star else '') + ('' if live else ' <span class="ar-coming">(coming)</span>')
    g = f'<div class="ar-node__gloss">{gloss}</div>' if gloss else ''
    extra = f'<p class="ar-node__more">{href_note}</p>' if href_note else ''
    return head, g, cls, body, extra

out = []
w = out.append
w('''---
title: "The work of Alexander and colleagues: a roadmap"
description: An introduction to Alexander’s ideas and approach, in the order they depend on each other.
layout: plain
showSidebar: false
showToc: false
---

<div class="ar-root">
<div class="ar-wrap">
<h1 class="ar-title"><span class="ar-title__over">The work of Alexander and colleagues</span>A Roadmap</h1>
<p class="ar-lede">Christopher Alexander (1936–2022) was the architect and thinker behind <em>The Nature of Order</em> and, with his colleagues at the Center for Environmental Structure, <em>A Pattern Language</em>. Why do some places make you feel more alive? He spent fifty years on that question. This is a way into his answer, one question at a time, each opening the next.</p>
<div class="ar-ways"><div class="ar-ways__head ar-sc">Or take a shorter trail</div><div class="ar-ways__list">''')
for slug, t, short, intro, stops in TRAILS:
    w(f'<a class="ar-way" href="/roadmap/{slug}"><span class="ar-way__title">{t}</span><span class="ar-way__note">{short}</span></a>')
w('''</div></div>
<div class="ar-legend">
<div><span class="ar-swatch"></span><span>Spine: read in order</span></div>
<div><span class="ar-swatch ar-swatch--star"></span><img src="/assets/nature-of-order-mark.png" class="ar-mark" alt="on the short route" /><span>The short route: six stops</span></div>
<div><span class="ar-swatch ar-swatch--branch"></span><span>Branch: optional depth</span></div>
<div><span class="ar-swatch ar-swatch--coming"></span><span>Page still to be written</span></div>
</div>''')
side = 0
for num, atitle, sub, stops in ACTS:
    w(f'<div class="ar-act" id="act-{num.lower()}"><div class="ar-act__num ar-sc">Act {num}</div><h2 class="ar-act__title">{atitle}</h2><p class="ar-act__sub">{sub}</p><hr class="ar-act__rule" /></div>')
    w('<div class="ar-spine">')
    for n, star, name, slug, gloss, body, branches in stops:
        live = exists(slug)
        cls = 'ar-node' + (' ar-node--star' if star else '') + ('' if live else ' is-coming')
        w(f'<div class="ar-stop" id="stop-{n}">')
        head = title(name, slug, 'ar-node__title') + ('&nbsp;<img src="/assets/nature-of-order-mark.png" class="ar-mark" alt="on the short route" />' if star else '') + ('' if live else ' <span class="ar-coming">(coming)</span>')
        g = f'<div class="ar-node__gloss">{gloss}</div>' if gloss else ''
        w(f'<div class="{cls}"><div class="ar-num">{n}</div><div class="ar-node__head">{head}</div>{g}<p class="ar-node__body">{body}</p></div>')
        if branches:
            sidecls = 'ar-branches--right' if side % 2 == 0 else 'ar-branches--left'
            side += 1
            if branches == "PROPS":
                items = ''.join(f'<a href="/concepts/{s}">{p}</a>' for p, s in PROPS)
                w(f'<div class="ar-branches ar-branches--wide"><div class="ar-props"><span class="ar-props__head ar-sc">One page each</span>{items}</div></div>')
            else:
                w(f'<div class="ar-branches {sidecls}">' + ''.join(branch(*b) for b in branches) + '</div>')
        w('</div>')
    w('</div>')
w('''<div class="ar-outro">
<div class="ar-outro__title">Why it matters beyond buildings</div>
<p class="ar-outro__body">If Alexander is right, value is something we can perceive and test, not just opinion, and that reaches well past architecture. See <a href="/visionary">Alexander as visionary</a>, or browse <a href="/concepts">all the concepts</a> and <a href="/works">the works</a>.</p>
</div>
</div>
</div>
''')
open(f"{root}/roadmap.md", "w").write("\n".join(out))

os.makedirs(f"{root}/roadmap", exist_ok=True)
for slug, t, short, intro, stops in TRAILS:
    o = [f'''---
title: "{t}: a trail through Christopher Alexander"
description: {short}
layout: plain
showSidebar: false
showToc: false
---

<div class="ar-root">
<div class="ar-wrap">
<div class="ar-kicker ar-sc"><a href="/roadmap">Roadmap</a> · a shorter trail</div>
<h1 class="ar-title">{t}</h1>
<p class="ar-lede">{intro}</p>
<div class="ar-spine ar-spine--trail">''']
    for i, n in enumerate(stops, 1):
        head, g, cls, body, extra = node(stops_by_n[n], f'<a href="/roadmap#stop-{n}">Stop {n} on the full roadmap</a>')
        o.append(f'<div class="ar-stop"><div class="{cls}"><div class="ar-num">{i}</div><div class="ar-node__head">{head}</div>{g}<p class="ar-node__body">{body}</p>{extra}</div></div>')
    others = ' · '.join(f'<a href="/roadmap/{s2}">{t2}</a>' for s2, t2, *_ in TRAILS if s2 != slug)
    o.append(f'''</div>
<div class="ar-outro">
<p class="ar-outro__body">For the whole picture, follow <a href="/roadmap">the full roadmap</a>. Other trails: {others}.</p>
</div>
</div>
</div>
''')
    open(f"{root}/roadmap/{slug}.md", "w").write("\n".join(o))
