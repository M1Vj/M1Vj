"""Build original, dependency-free artwork for the M1Vj profile."""
from pathlib import Path
from html import escape
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
if ROOT.name == 'tools':
    ROOT = ROOT.parent
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

THEMES = {
    'light': dict(bg='#F4F7FC', ink='#16243D', muted='#516582', line='#D4DFF0', panel='#FFFFFF', blue='#5369E8', teal='#168B83', amber='#AB6A17', wash='#E6ECFF'),
    'dark': dict(bg='#111E33', ink='#EAF1FF', muted='#A5B8D5', line='#314564', panel='#192B46', blue='#9AABFF', teal='#6BD9C9', amber='#F1C17D', wash='#233559'),
}

def txt(x, y, text, size=24, weight=400, color='ink', **attrs):
    extra=' '.join(f'{k.replace("_", "-")}="{escape(str(v))}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" class="{color}" font-size="{size}" font-weight="{weight}" {extra}>{escape(text)}</text>'

def path(d, cls='line', width=2, extra=''):
    return f'<path d="{d}" fill="none" class="{cls}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def circle(x,y,r=5,cls='blue',extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" class="{cls}" {extra}/>'

def doc(x,y,w=36,h=48):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" class="panel"/>'+path(f'M{x+9} {y+14}h{w-18}m-{w-18} 9h{w-18}m-{w-18} 9h{w-25}', 'muted',2)

def svg(body,w,h,theme,title,desc,animated=True):
    c=THEMES[theme]
    css=''.join(f'.{k}'+'{'+('stroke:'+v+';fill:none;' if k=='line' else 'fill:'+v+';')+'}' for k,v in c.items())
    css+=' .line{stroke:'+c['line']+'}path.muted{stroke:'+c['muted']+';fill:none}.muted-stroke{stroke:'+c['muted']+';fill:none}.blue-stroke{stroke:'+c['blue']+';fill:none}.teal-stroke{stroke:'+c['teal']+';fill:none}.panel{stroke:'+c['line']+'} text{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif} .signal{stroke:'+c['blue']+';fill:none;stroke-dasharray:7 35;stroke-width:3;opacity:.65} .soft{opacity:.65}'
    if animated:
        css+=' @keyframes travel{to{stroke-dashoffset:-168}}.signal{animation:travel 4.8s linear 1 forwards}@keyframes breathe{0%,100%{opacity:.45}50%{opacity:.95}}.breathe{animation:breathe 4.8s ease-in-out 1 forwards}@media(prefers-reduced-motion:reduce){.signal,.breathe{animation:none}}'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><style>{css}</style>{body}</svg>\n'

def hero(theme,mobile=False,animated=True):
    if mobile:
        w,h=600,630
        b='<rect width="600" height="630" rx="24" class="bg"/>'
        b+=txt(36,75,'Vj Mabansag',58,700)
        b+=txt(38,117,'Applied AI & full-stack development',25,color='muted')
        b+=path('M38 148H562')
        b+=txt(38,200,'From context',44,650)+txt(38,252,'to working systems.',44,650)
        # A conceptual representation space: input points converge into layers.
        points=[(67,333),(101,349),(57,374),(122,390),(79,413),(140,324),(148,358)]
        for i,(x,y) in enumerate(points):
            b+=circle(x,y,5,'teal' if i%2 else 'blue')
            b+=path(f'M{x} {y}C180 {y} 182 368 230 368',width=1)
        for i in range(3):
            b+=f'<rect x="{230+i*15}" y="{320+i*12}" width="56" height="90" rx="7" class="panel"/>'
            for j in range(4):b+=path(f'M{240+i*15} {338+i*12+j*14}h32','blue-stroke',2)
        b+=path('M316 378H360M360 378C390 378 390 338 430 338M360 378H430M360 378C390 378 390 418 430 418')
        b+=path('M163 368H224','signal',3)
        b+=circle(360,378,7,'blue',extra='class="blue breathe"')
        for y,label in [(338,'HydraLab'),(378,'SmartMap'),(418,'MathWiz')]:
            b+=circle(430,y,4,'teal')+txt(444,y+7,label,23,550)
        b+=txt(38,482,'Embeddings. Transformers. Human review.',23,color='muted')
        b+=path('M38 513H562')
        b+=txt(38,559,'Python + TypeScript',26,550)
        b+=txt(38,599,'Philippines · BSCS at VSU',22,color='muted')
    else:
        w,h=1200,470
        b='<rect width="1200" height="470" rx="24" class="bg"/>'
        b+=txt(48,84,'Vj Mabansag',64,700)
        b+=txt(50,128,'Applied AI & full-stack development',27,color='muted')
        b+=path('M50 160H1150')
        b+=txt(50,232,'From context',47,650)+txt(50,291,'to working systems.',47,650)
        b+=txt(50,341,'Embeddings. Transformers. Human review.',24,color='muted')
        # Representation space, transformer-like layers and product branches.
        points=[(648,220),(680,246),(628,272),(696,306),(651,322),(721,211),(724,263)]
        for i,(x,y) in enumerate(points):
            b+=circle(x,y,5,'teal' if i%2 else 'blue')+path(f'M{x} {y}C755 {y} 753 270 791 270',width=1)
        for i in range(3):
            b+=f'<rect x="{793+i*16}" y="{212+i*11}" width="53" height="91" rx="7" class="panel"/>'
            for j in range(4):b+=path(f'M{803+i*16} {232+i*11+j*14}h31','blue-stroke',2)
        b+=path('M895 281H947M947 281C969 281 965 228 998 228M947 281H998M947 281C969 281 965 334 998 334')
        b+=path('M740 270H783','signal',3)+circle(947,281,7,'blue',extra='class="blue breathe"')
        for y,label in [(228,'HydraLab'),(281,'SmartMap'),(334,'MathWiz')]:
            b+=circle(998,y,4,'teal')+txt(1012,y+7,label,23,550)
        b+=path('M50 390H1150')
        b+=txt(50,434,'Python + TypeScript',25,550)+txt(820,434,'Philippines · BSCS at VSU',23,color='muted')
    # Duplicate attributes are prohibited; circle's class is constructed above.
    b=b.replace('class="blue" class="blue breathe"','class="blue breathe"')
    return svg(b,w,h,theme,'Vj Mabansag — applied AI and full-stack development','Conceptual illustration: context points form representations, pass through model layers and branch toward HydraLab, SmartMap and MathWiz. Essential profile information is also provided as text.',animated)

def hydra(theme,mobile=False):
    if mobile:
        b='<rect width="600" height="330" rx="20" class="bg"/>'
        b+=txt(30,54,'A visible evidence trail',32,650)
        for x,y,label in [(30,90,'Sources'),(330,90,'Citations'),(30,215,'Review'),(330,215,'Agents')]:
            b+=f'<rect x="{x}" y="{y}" width="240" height="68" rx="12" class="panel"/>'+txt(x+120,y+43,label,28,550,text_anchor='middle')
        b+=path('M270 124H330M450 158V215M330 249H270','blue-stroke',3)
        b+=txt(30,307,'Documents, citations, agents and human review.',22,color='muted')
        return svg(b,600,330,theme,'HydraLab evidence trail','Source documents connect to citations, agent workflows and human review.',False)
    w,h=1200,280
    b='<rect width="1200" height="280" rx="20" class="bg"/>'
    b+=txt(38,57,'HydraLab',34,700)+txt(38,94,'A research workbench with a visible evidence trail.',25,color='muted')
    # Source cards become a cited note, an agent path and an approval gate.
    for x in [42,88,134]:b+=doc(x,149,35,51)
    b+=path('M182 175H248M369 175H433M575 175H657M787 175H854M1009 175H1146')
    for x,width,label in [(248,121,'Sources'),(433,142,'Citations'),(657,130,'Agents'),(854,155,'Review')]:
        b+=f'<rect x="{x}" y="146" width="{width}" height="59" rx="12" class="panel"/>'+txt(x+width/2,183,label,25,550,text_anchor='middle')
    b+=path('M186 175H238M379 175H423M585 175H647M797 175H844','signal',3)
    b+=txt(38,250,'Python / FastAPI',22,color='muted')+txt(435,250,'React / TypeScript',22,color='muted')+txt(855,250,'SQLite / MCP',22,color='muted')
    return svg(b,w,h,theme,'HydraLab research workflow','Source documents connect to citations, agent workflows and human review. Python, FastAPI, React, TypeScript, SQLite and MCP.',False)

def seal(theme,mobile=False):
    if mobile:
        b='<rect width="600" height="172" rx="18" class="bg"/>'+path('M30 51l12 12 26-32','teal-stroke',4)
        b+=txt(92,57,'Build with AI.',32,650)+txt(92,99,'Check the evidence.',32,650)
        b+=txt(30,146,'Source review · tests · human judgment',23,color='muted')
        return svg(b,600,172,theme,'Build with AI. Check the evidence.','Source review, tests, browser checks and human judgment.',False)
    w,h=1200,124
    b='<rect width="1200" height="124" rx="18" class="bg"/>'
    b+=path('M42 67l13 13 26-32','teal-stroke',4)
    b+=txt(108,58,'Build with AI. Check the evidence.',30,650)
    b+=txt(108,94,'Source review · tests · browser checks · human judgment',23,color='muted')
    return svg(b,w,h,theme,'Build with AI. Check the evidence.','My workflow includes source review, tests, browser checks and human judgment.',False)

def write():
    for theme in THEMES:
        for mobile in [False,True]:
            for animated in [True,False]:
                name='workbench-'+theme+('-mobile' if mobile else '')+('' if animated else '-still')+'.svg'
                (ASSETS/name).write_text(hero(theme,mobile,animated))
        (ASSETS/f'hydralab-{theme}.svg').write_text(hydra(theme))
        (ASSETS/f'workflow-{theme}.svg').write_text(seal(theme))
        (ASSETS/f'hydralab-{theme}-mobile.svg').write_text(hydra(theme,True))
        (ASSETS/f'workflow-{theme}-mobile.svg').write_text(seal(theme,True))
    for f in ASSETS.glob('*.svg'):ET.fromstring(f.read_text())
    print(json.dumps({'assets':len(list(ASSETS.glob('*.svg'))),'bytes':sum(f.stat().st_size for f in ASSETS.glob('*.svg')),'xml':'valid'}))

if __name__=='__main__':write()
