"""Write three front-page mockups (preview only) into the given directory."""
import sys, os
out = sys.argv[1]
os.makedirs(out, exist_ok=True)

INTRO = 'Christopher Alexander (1936–2022) was the architect and thinker behind <cite>A Pattern Language</cite> and <cite>The Nature of Order</cite>. This is a field guide to the ideas, buildings and places he made with his collaborators.'
Q = 'Why does one window become everyone’s favorite place to sit? How do families laying out a neighborhood decide where a path should go?'
Q2 = 'Alexander and his collaborators spent decades studying questions like these in buildings, on drawing boards, and out on the land.'
ROUTES = [
    ('Roadmap', '/roadmap', 'Start here: Alexander’s ideas in the order they depend on each other.'),
    ('Concepts', '/concepts', 'What gives one place more life than another? Begin with <a href="/concepts/wholeness-and-centers">wholeness and centers</a>.'),
    ('Patterns', '/patterns', 'All 253 patterns by number and printed page. For something to try indoors, open <a href="/patterns/window-place">Window Place</a>.'),
    ('Works', '/works', 'Fifty years of books, from <cite>Notes on the Synthesis of Form</cite> to <cite>The Nature of Order</cite>.'),
    ('Guides', '/practice', 'Follow the making of the <a href="/practice/eishin-campus">Eishin campus</a>, where a school decided how it would sit on the land.'),
    ('Neighborhoods', '/living-neighborhoods', '<a href="/living-neighborhoods/first-walk">Take a walk with a neighbor</a> and compare the places each of you would keep.'),
]
CREDITS = '''<footer class="wiki-credits">
<p>The ideas, words and pictures here are the work of Christopher Alexander and his collaborators, among them Sara Ishikawa, Murray Silverstein, Max Jacobson, Ingrid Fiksdahl-King, Shlomo Angel, Howard Davis, Hajo Neis, Artemis Anninou and Maggie Moore Alexander, and the Center for Environmental Structure. Where we write “Alexander”, read “Alexander and his collaborators”. This wiki is made by Rufus Pollock with help from David Gasquez. <a href="/about">About this wiki</a>.</p>
</footer>'''
FM = '---\ntitle: "{t}"\nlayout: plain\nshowToc: false\nshowSidebar: false\n---\n\n'


def contents(cls):
    rows = ''.join(f'<li><a class="fp-label" href="{h}">{n}</a><p>{d}</p></li>\n' for n, h, d in ROUTES)
    return f'<ol class="{cls}">\n{rows}</ol>'


# A: Contents page. A plain title, the plate beside the questions, routes as a contents list.
a = FM.format(t='Front page mockup A: Contents') + f'''<div class="fp fp-a">
<header class="fp-a-head">
<p class="fp-mono">A field guide · 1936–2022</p>
<h1>Christopher Alexander Wiki</h1>
<p class="fp-intro">{INTRO}</p>
</header>
<div class="fp-a-body">
<div class="fp-a-main">
<p class="fp-q">{Q}</p>
<p>{Q2}</p>
<p class="fp-mono fp-contents-title">Where to begin</p>
{contents('fp-contents')}
</div>
<figure class="fp-plate"><a href="/patterns/window-place"><img src="/assets/patterns/window-place.jpg" alt="Two benches face one another in a deep recess, with a window between them." /></a><figcaption>Window Place · pattern 180 · p. 833</figcaption></figure>
</div>
{CREDITS}
</div>
'''

# B: Plates. A full-width row of pictures from the books opens the page.
plates = [
    ('/assets/patterns/window-place.jpg', 'A window seat in a deep recess.', 'Window Place · p. 833', '/patterns/window-place'),
    ('/assets/figures/nature-of-order-1/levels-of-scale-isfahan-porch.jpg', 'A columned porch in Isfahan, light falling across the floor.', 'Levels of scale · Isfahan', '/concepts'),
    ('/assets/figures/eishin-flags.jpg', 'White flags on poles across a green field, marking where buildings will stand.', 'Laying out Eishin', '/practice/eishin-campus'),
    ('/assets/figures/nature-of-order-1/levels-of-scale-mud-cracks.jpg', 'Dried mud cracked into cells of many sizes.', 'Levels of scale · mud', '/concepts'),
]
pl = ''.join(f'<figure><a href="{h}"><img src="{s}" alt="{al}" /></a><figcaption>{c}</figcaption></figure>\n' for s, al, c, h in plates)
b = FM.format(t='Front page mockup B: Plates') + f'''<div class="fp fp-b">
<section class="fp-b-plates" aria-label="Pictures from the books">
{pl}</section>
<header class="fp-b-head">
<h1>Christopher Alexander Wiki</h1>
<p class="fp-intro">{INTRO}</p>
</header>
<div class="fp-b-routes">
{contents('fp-contents')}
</div>
{CREDITS}
</div>
'''

# C: The question. Alexander's kind of question, large, beside the plate.
c = FM.format(t='Front page mockup C: The question') + f'''<div class="fp fp-c">
<section class="fp-c-hero">
<div class="fp-c-text">
<p class="fp-mono">Christopher Alexander Wiki</p>
<h1>Why does one window become everyone’s favorite place to sit?</h1>
<p class="fp-intro">{INTRO}</p>
<p class="fp-c-start"><a class="fp-mono" href="/roadmap">Start with the roadmap →</a></p>
</div>
<figure class="fp-plate"><a href="/patterns/window-place"><img src="/assets/patterns/window-place.jpg" alt="Two benches face one another in a deep recess, with a window between them." /></a><figcaption>Window Place · pattern 180 · p. 833</figcaption></figure>
</section>
<div class="fp-c-routes">
{contents('fp-contents')}
</div>
{CREDITS}
</div>
'''
for n, t in [('front-a', a), ('front-b', b), ('front-c', c)]:
    open(os.path.join(out, n + '.md'), 'w').write(t)
print('ok')
