#!/usr/bin/env python3
"""Reproducible build for the Vj Mabansag GitHub profile hero artwork.

Generates self-contained SVG illustrations (no external fonts, images, scripts
or trackers) for four reader contexts: light/dark x desktop/mobile, each as a
finite-motion file and an inert still file. Also writes the README and the
text-only profile from the same copy constants so the three never drift.
"""
from __future__ import annotations
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
if ROOT.name == 'tools':
    ROOT = ROOT.parent
ASSETS = ROOT / "assets"

SANS = "ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', 'Times New Roman', serif"

PALETTES = {
    "light": dict(
        bg="#EFE7D8", bg2="#E4D9C5", ink="#17211F", soft="#4C5C57",
        teal="#0E6F63", teal_hi="#149183", amber="#B96E28", amber_hi="#E8A24E",
        plum="#6B4C75", island="#DCCDB2", island_edge="#C4B292", island_deep="#A99574",
        wood="#B8834F", wood_l="#94653A", wood_r="#7B5230",
        paper="#FBF5E8", paper_edge="#D9CBB0", screen="#132A2A", screen_ink="#7FE3CE",
        leaf="#3F7A55", leaf_l="#5C9A6C", pot="#B4643F", metal="#8C9290",
        thread="#0E8A78", glow="#F6C177", shadow="#6B5A44",
    ),
    "dark": dict(
        bg="#0B1415", bg2="#0F1D1E", ink="#EAF2EC", soft="#9DB2AB",
        teal="#5EEAD4", teal_hi="#8FF5E3", amber="#F0B26B", amber_hi="#FFD39B",
        plum="#C2A3CE", island="#233B39", island_edge="#1A2C2B", island_deep="#12201F",
        wood="#8A5F3C", wood_l="#6C472C", wood_r="#553522",
        paper="#E9F0E6", paper_edge="#A9BDB4", screen="#0A1F1F", screen_ink="#8CF2DC",
        leaf="#5E9E74", leaf_l="#83BE90", pot="#C97B52", metal="#A7B2AE",
        thread="#6EF0D8", glow="#FFC98A", shadow="#000000",
    ),
}

def esc(s: str) -> str:
    return html.escape(s, quote=True)

class Iso:
    def __init__(self, ox: float, oy: float, s: float):
        self.ox, self.oy, self.s = ox, oy, s
    def p(self, x, y, z=0.0):
        return (self.ox + (x - y) * 0.8660254 * self.s,
                self.oy + (x + y) * 0.5 * self.s - z * self.s)
    def poly(self, pts, fill, stroke="none", sw=0.0, extra=""):
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in (self.p(*q) for q in pts))
        st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if sw else ""
        return f'<polygon points="{d}" fill="{fill}"{st}{(" " + extra) if extra else ""}/>'
    def slab(self, x0, y0, x1, y1, z0, z1, top, left, right, extra=""):
        """Axis-aligned box with three lit faces (light from upper left)."""
        return "".join([
            self.poly([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)], top, extra=extra),
            self.poly([(x0,y1,z1),(x1,y1,z1),(x1,y1,z0),(x0,y1,z0)], right),
            self.poly([(x1,y0,z1),(x1,y1,z1),(x1,y1,z0),(x1,y0,z0)], left),
        ])

def grad(gid, stops, x1=0, y1=0, x2=0, y2=1):
    body = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return (f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            f'{body}</linearGradient>')

def rgrad(gid, stops, cx="50%", cy="50%", r="50%"):
    body = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}">{body}</radialGradient>'

def face_matrix(g, x0, y0, x1, y1, z_top, z_bot, w=100.0, h=100.0):
    """Affine matrix mapping a 100x100 design space onto a constant-y world face."""
    ax, ay = g.p(x0, y0, z_top)
    bx, by = g.p(x1, y0, z_top)
    cx, cy = g.p(x0, y0, z_bot)
    a, b = (bx - ax) / w, (by - ay) / w
    c, d = (cx - ax) / h, (cy - ay) / h
    return f"matrix({a:.4f} {b:.4f} {c:.4f} {d:.4f} {ax:.2f} {ay:.2f})"

def scene(theme, g, compact=False):
    c = PALETTES[theme]
    s = g.s
    o = []
    A = o.append

    # floating island shadow
    sx, sy = g.p(210, 150, -70)
    A(f'<ellipse cx="{sx:.1f}" cy="{sy+26*s:.1f}" rx="{250*s:.1f}" ry="{38*s:.1f}" fill="{c["shadow"]}" opacity="0.20" filter="url(#soft12)"/>')

    # underside strata: tapered, hand-cut rocks
    for inset, ztop, zbot, fill, op in ((20, -4, -26, c["island_deep"], ".72"),
                                        (52, -24, -52, c["island_deep"], ".52"),
                                        (92, -50, -76, c["island_deep"], ".34")):
        A(g.poly([(inset,inset,zbot),(420-inset,inset+6,zbot),(420-inset-6,300-inset,zbot),(inset+6,300-inset,zbot)],
                 fill, extra=f'opacity="{op}"'))
        A(g.poly([(inset,inset,ztop),(inset,300-inset,ztop),(inset+6,300-inset,zbot),(inset,inset+6,zbot)],
                 fill, extra=f'opacity="{op}"'))
    # island top
    A(g.poly([(0,0,0),(420,0,0),(420,300,0),(0,300,0)], c["island"]))
    A(g.poly([(0,300,0),(420,300,0),(420,300,-16),(0,300,-16)], c["island_edge"]))
    A(g.poly([(420,0,0),(420,300,0),(420,300,-16),(420,0,-16)], c["island_edge"]))
    # faint site grid + rim light
    for t in range(1, 6):
        x = t * 70
        A(g.poly([(x,0,0.2),(x,300,0.2)], "none", c["soft"], max(0.6, 0.75*s), 'opacity="0.16"'))
    for t in range(1, 5):
        y = t * 60
        A(g.poly([(0,y,0.2),(420,y,0.2)], "none", c["soft"], max(0.6, 0.75*s), 'opacity="0.16"'))
    A(g.poly([(0,0,0),(420,0,0),(420,300,0),(0,300,0)], "none", c["teal"], max(0.8, 1.0*s), 'opacity="0.35"'))

    # rug under the desk
    A(g.slab(58, 148, 338, 288, 0, 2.4, c["plum"], c["plum"], c["plum"], extra='opacity="0.16"'))

    # ---- wall map board (back right) ----
    bx0, bx1, by, bz0, bz1 = 278, 402, 24, 44, 176
    A(g.slab(286, 20, 296, 28, 0, 54, c["wood_l"], c["wood_r"], c["wood_l"]))
    A(g.slab(386, 20, 396, 28, 0, 54, c["wood_l"], c["wood_r"], c["wood_l"]))
    A(g.poly([(bx0,by,bz1),(bx1,by,bz1),(bx1,by,bz0),(bx0,by,bz0)], c["paper"]))
    A(g.poly([(bx0,by,bz1),(bx1,by,bz1),(bx1,by,bz1-4),(bx0,by,bz1-4)], c["paper_edge"]))
    A(g.poly([(bx0-6,by+2,bz1+6),(bx1+6,by+2,bz1+6),(bx1+6,by+2,bz1-2),(bx0-6,by+2,bz1-2)], c["wood"], extra='opacity="0.95"'))
    m = face_matrix(g, bx0, by, bx1, by, bz1, bz0)
    A(f'<g transform="{m}">')
    A(f'<rect x="0" y="0" width="100" height="100" fill="{c["paper"]}"/>')
    A(f'<path d="M8 64 C24 58 34 70 50 60 S76 44 92 50" fill="none" stroke="{c["teal"]}" stroke-width="1.4" stroke-dasharray="3 2.4" opacity="0.85"/>')
    A(f'<circle cx="50" cy="60" r="2.6" fill="{c["amber"]}"/>')
    A(f'<circle cx="50" cy="60" r="6" fill="none" stroke="{c["amber"]}" stroke-width="0.8" opacity="0.55"/>')
    A(f'<rect x="8" y="12" width="26" height="3" rx="1.2" fill="{c["ink"]}" opacity="0.55"/>')
    A(f'<rect x="8" y="19" width="16" height="2" rx="1" fill="{c["ink"]}" opacity="0.3"/>')
    for i, (rx, ry, rw, rh) in enumerate(((66,14,16,12),(84,30,10,9),(20,36,12,9),(62,74,18,10),(30,80,14,8))):
        A(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="1" fill="{c["plum"]}" opacity="{0.18+i*0.03:.2f}"/>')
    A(f'<path d="M4 96 H96" stroke="{c["ink"]}" stroke-width="0.5" opacity="0.18"/>')
    A('</g>')
    A(g.poly([(bx0,by,bz1),(bx0,by,bz0)], "none", c["paper_edge"], 0.8))

    # ---- desk ----
    dx0, dx1, dy0, dy1 = 74, 308, 168, 276
    A(g.slab(dx0, dy0, dx1, dy1, 66, 78, c["wood"], c["wood_l"], c["wood_r"]))
    A(g.poly([(dx0,dy1,78),(dx1,dy1,78),(dx1,dy1,74),(dx0,dy1,74)], c["amber_hi"], extra='opacity="0.28"'))
    # legs
    for lx, ly in ((dx0+12, dy0+10), (dx1-14, dy0+10), (dx0+12, dy1-12), (dx1-14, dy1-12)):
        A(g.slab(lx, ly, lx+7, ly+7, 0, 66, c["wood_r"], c["wood_r"], c["wood_r"]))
    # drawer, front face only
    A(g.poly([(dx0+34,dy1,66),(dx0+150,dy1,66),(dx0+150,dy1,26),(dx0+34,dy1,26)], c["wood_l"], extra='opacity="0.9"'))
    A(g.poly([(dx0+46,dy1,56),(dx0+138,dy1,56),(dx0+138,dy1,48),(dx0+46,dy1,48)], c["wood_r"]))
    A(f'<circle cx="{g.p(dx0+92,dy1,52)[0]:.1f}" cy="{g.p(dx0+92,dy1,52)[1]:.1f}" r="{2.4*s:.1f}" fill="{c["amber_hi"]}"/>')
    # wood grain
    for i in range(3):
        y = dy0 + 30 + i*22
        p0, p1 = g.p(dx0+18, y, 78.4), g.p(dx1-24, y+12, 78.4)
        A(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} Q{(p0[0]+p1[0])/2:.1f} {p0[1]-3*s:.1f} {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{c["wood_r"]}" stroke-width="{max(0.6,0.9*s):.1f}" opacity="0.35"/>')
    return o, c

def studio(theme, g, animated=True):
    o,c=scene(theme,g)
    A=o.append
    # Laptop, keyboard and a small constellation on the screen.
    A(g.slab(138,185,241,248,79,83,c['metal'],c['soft'],c['soft']))
    A(g.poly([(138,185,83),(241,185,83),(241,185,164),(138,185,164)],c['ink']))
    m=face_matrix(g,143,185,236,185,159,88)
    A(f'<g transform="{m}"><rect width="100" height="100" rx="3" fill="{c["screen"]}"/>')
    A(f'<path d="M14 30 28 44 14 58 M43 26 34 63" fill="none" stroke="{c["screen_ink"]}" stroke-width="3"/>')
    for x,y in [(68,25),(85,40),(62,52),(79,72),(50,78)]:
        A(f'<path d="M68 25 85 40 62 52 79 72 50 78 68 25 62 52" fill="none" stroke="{c["screen_ink"]}" stroke-width=".6" opacity=".4"/><circle cx="{x}" cy="{y}" r="2.5" fill="{c["screen_ink"]}"/>')
    A('</g>')
    for row in range(4):
        for col in range(10):
            x,y=148+col*8,195+row*8
            A(g.poly([(x,y,83.3),(x+5,y,83.3),(x+5,y+5,83.3),(x,y+5,83.3)],c['screen'],extra='opacity=".7"'))
    # Open research notebook on the desk.
    A(g.poly([(252,204,81),(290,199,81),(290,249,81),(252,254,81)],c['paper']))
    A(g.poly([(290,199,81),(320,210,81),(320,258,81),(290,249,81)],c['paper_edge']))
    for i in range(5):
        A(g.poly([(257,214+i*7,81.5),(284,210+i*7,81.5)],'none',c['teal'],.9,'opacity=".6"'))
    # Floor stack, warm mug, and plants give the workbench a lived-in scale.
    for z,fill in [(0,c['plum']),(9,c['teal']),(18,c['paper'])]:
        A(g.slab(328,220,384,265,z,z+8,fill,fill,c['paper_edge']))
    px,py=g.p(106,210,92)
    A(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="10" ry="5" fill="{c["paper"]}"/><path d="M{px-10:.1f} {py:.1f}v16q10 9 20 0v-16" fill="{c["paper_edge"]}"/><ellipse cx="{px:.1f}" cy="{py:.1f}" rx="8" ry="3" fill="{c["wood_r"]}"/><path d="M{px+9:.1f} {py+4:.1f}q13 -1 9 10q-4 5-10 1" fill="none" stroke="{c["paper_edge"]}" stroke-width="3"/>')
    for x,y in [(38,90),(360,140)]:
        A(g.slab(x-12,y-12,x+12,y+12,0,30,c['pot'],c['wood_l'],c['pot']))
        for dx,dz in [(-20,58),(17,72),(-8,86),(27,49)]:
            x1,y1=g.p(x,y,25);x2,y2=g.p(x+dx,y, dz)
            A(f'<path d="M{x1:.1f} {y1:.1f} Q{x2-12:.1f} {y2+8:.1f} {x2:.1f} {y2:.1f}" fill="none" stroke="{c["leaf"]}" stroke-width="3"/><ellipse cx="{x2:.1f}" cy="{y2:.1f}" rx="7" ry="16" transform="rotate({-30 if dx<0 else 35} {x2:.1f} {y2:.1f})" fill="{c["leaf_l"]}"/>')
    # A drawn trail crosses the miniature campus without turning it into a flowchart.
    pts=[g.p(*q) for q in [(34,44,2),(110,80,3),(184,106,3),(246,92,3),(332,70,3)]]
    d='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    A(f'<path class="trace" d="{d}" fill="none" stroke="{c["thread"]}" stroke-width="2.6" stroke-linecap="round" stroke-dasharray="5 6"/>')
    for x,y in [pts[0],pts[-1]]:
        A(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{c["amber_hi"]}" stroke="{c["ink"]}" stroke-width="1"/>')
    if animated:
        A(f'<circle r="4" fill="{c["amber_hi"]}" stroke="{c["ink"]}" stroke-width="1"><animateMotion dur="4.6s" repeatCount="1" fill="freeze" path="{d}"/></circle>')
    return ''.join(o)

def hero(theme, mobile=False, animated=True):
    c=PALETTES[theme]
    w,h=(640,700) if mobile else (1200,500)
    g=Iso(288,317,.74) if mobile else Iso(831,102,.91)
    x=32 if mobile else 56
    y=61 if mobile else 77
    title_size=66 if mobile else 84
    motion='''<style>.studio{animation:arrive 1s ease-out both}.trace{animation:trail 4.6s ease-out both}@keyframes arrive{from{opacity:.9;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}@keyframes trail{from{stroke-dashoffset:65;opacity:.7}to{stroke-dashoffset:0;opacity:1}}@media(prefers-reduced-motion:reduce){.studio,.trace{animation:none}animateMotion{display:none}}</style>''' if animated else ''
    defs=grad('back',[(0,c['bg'],1),(1,c['bg2'],1)],0,0,1,1)+rgrad('light',[(0,c['glow'],.15),(1,c['glow'],0)])
    label_y=253 if mobile else 313
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">Vj Mabansag — Applied AI and full-stack development</title><desc id="desc">An original miniature studio: code on a laptop, an open research notebook, plants and a campus map. Embeddings and transformers meet practical software.</desc><defs>{defs}<filter id="soft12"><feGaussianBlur stdDeviation="12"/></filter></defs>{motion}<rect width="{w}" height="{h}" rx="18" fill="url(#back)"/><ellipse cx="{w*.72}" cy="{h*.5}" rx="{w*.4}" ry="{h*.55}" fill="url(#light)"/><path d="M{x} {y+12}h28" stroke="{c['teal']}" stroke-width="3"/><text x="{x+40}" y="{y+17}" font-family="{SANS}" font-size="13" letter-spacing="2" fill="{c['soft']}">THE APPLIED AI STUDIO</text><text x="{x}" y="{y+101}" font-family="{SERIF}" font-size="{title_size}" letter-spacing="-3" fill="{c['ink']}">Vj Mabansag<tspan fill="{c['teal']}">.</tspan></text><text x="{x}" y="{y+143}" font-family="{SANS}" font-size="{20 if mobile else 23}" fill="{c['soft']}">From a curious idea</text><text x="{x}" y="{y+175}" font-family="{SANS}" font-size="{20 if mobile else 23}" fill="{c['soft']}">to something people can use.</text><text x="{x}" y="{label_y+30}" font-family="{SANS}" font-size="{14 if mobile else 16}" fill="{c['teal']}">Embeddings · Transformers · Full-stack</text><g class="studio">{studio(theme,g,animated)}</g><text x="{x}" y="{h-26}" font-family="{SANS}" font-size="12" letter-spacing="1.3" fill="{c['soft']}">PYTHON / TYPESCRIPT / PHILIPPINES</text></svg>'''

COPY='''I build AI tools and the software around them. I'm **Vj**, a Computer Science student at **Visayas State University**, Philippines, graduating in **2027**. My focus is applied AI, with research into model behavior and an interest in how AI should be used.

**[Explore my work](#selected-work)** · **[Research notes](#what-im-investigating)** · **[Connect on LinkedIn](https://www.linkedin.com/in/m1vj/)**

## Selected work

### [HydraLab ↗](https://github.com/M1Vj/HydraLab)
**A local research workbench.** Reading, citations, writing and research agents in one place. I built it around a simple need: keep the source close to the claim. Python, TypeScript and a desktop interface; currently pre-release.

### [VSU SmartMap ↗](https://github.com/M1Vj/VSU-SmartMap) · [Try the map](https://vsumap.vercel.app/)
**Campus navigation with AI assistance.** An interactive map, searchable directory, offline access and Gemini-powered location chat. It began as a Software Engineering group project; I now maintain it solo.

### [MathWiz Arena / centipede ↗](https://github.com/M1Vj/centipede)
**Math competitions, from registration to results.** Lead developer on a collaborative platform with problem banks, team contests, scoring, answer review and disputes. Next.js, TypeScript and Supabase.

**Also building:** [Dormy](https://github.com/M1Vj/Dormy), my solo dormitory operations app; [CodexSwap](https://github.com/M1Vj/CodexSwap), a native macOS tool; and [VSUEE agent tooling](https://github.com/M1Vj/vsuee-skill). **UniDorm is a separate group project.**

## What I'm investigating

How does watermarking change passive AI-text detector scores? My undergraduate research compares paired watermarked and unwatermarked Gemma responses, using Python analysis and reproducibility checks. A detector score needs careful interpretation.

**Working interests:** embeddings, transformers, NLP, AI agents and evaluation. **Tools I use:** Python, TypeScript, React / Next.js, FastAPI, PostgreSQL / Supabase and Git.

## AI with human judgment

During my **AI4GOV internship**, I contributed with Pod B to **SangkAI**, a civic-feedback prototype. My work included AI workflows, prompts, fallback behavior, safety checks, testing and documentation. Staff review AI suggestions before decisions.

I'm open to **early-career applied AI and software development opportunities**. [Let's talk →](https://www.linkedin.com/in/m1vj/)
'''

def picture():
    sources=[]
    for reduced in [True,False]:
        for mobile,theme in [(True,'dark'),(True,'light'),(False,'dark'),(False,'light')]:
            terms=[]
            if reduced:terms.append('(prefers-reduced-motion: reduce)')
            if mobile:terms.append('(max-width: 600px)')
            if theme=='dark':terms.append('(prefers-color-scheme: dark)')
            name='studio-'+theme+('-mobile' if mobile else '')+('-still' if reduced else '')+'.svg'
            if terms:sources.append(f'  <source media="{" and ".join(terms)}" srcset="./assets/{name}">')
    return '<picture>\n'+'\n'.join(sources)+'\n  <img src="./assets/studio-light.svg" width="1200" alt="Vj Mabansag — applied AI and full-stack development. An illustrated studio with a laptop, research notebook and campus map.">\n</picture>\n\n'

def main():
    ASSETS.mkdir(parents=True,exist_ok=True)
    for theme in PALETTES:
        for mobile in [False,True]:
            for animated in [False,True]:
                name='studio-'+theme+('-mobile' if mobile else '')+('' if animated else '-still')+'.svg'
                (ASSETS/name).write_text(hero(theme,mobile,animated))
    (ROOT/'README.md').write_text(picture()+COPY+'\n<sub>[Text-only profile](./PROFILE-STILL.md) · Original artwork, drawn for this profile.</sub>\n')
    (ROOT/'PROFILE-STILL.md').write_text('# Vj Mabansag\n\nApplied AI & full-stack development\n\n'+COPY+'\n[Back to the illustrated profile](./README.md)\n')
    print('Built 8 original SVG variants and both profile readers.')

if __name__=='__main__':main()
