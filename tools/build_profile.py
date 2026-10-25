"""Build the compact GitHub profile using only Python's standard library.

Run from the profile repository: python3 tools/build_profile.py
Pass --refresh-stats to update the public snapshot through authenticated gh.
No dependency installation, hosted widget or scheduled workflow required.
"""
from pathlib import Path
import argparse
import datetime as dt
import html
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parent
if ROOT.name=='tools': ROOT=ROOT.parent
ASSETS=ROOT/'assets'
PALETTES={
    'dark':{'bg':'#091426','ink':'#ECF2FF','muted':'#9AAED0','accent':'#6794FF','bright':'#79E6EF','line':'#263959','tile':'#112444'},
    'light':{'bg':'#F4F7FF','ink':'#132342','muted':'#526580','accent':'#2459D7','bright':'#087A89','line':'#D4DFF1','tile':'#E2EAF9'},
}
FONT="'Avenir Next','Trebuchet MS','Segoe UI',Arial,sans-serif"
MONO="'SFMono-Regular',Consolas,'Liberation Mono',monospace"

def refresh_stats():
    def get(endpoint):
        r=subprocess.run(['gh','api',endpoint],capture_output=True,text=True,check=True)
        return json.loads(r.stdout)
    user=get('users/M1Vj')
    repos=[]
    page=1
    while True:
        batch=get(f'users/M1Vj/repos?per_page=100&type=owner&page={page}')
        repos.extend(r for r in batch if not r['private'])
        if len(batch)<100:break
        page+=1
    languages=sorted({r['language'] for r in repos if not r['fork'] and r['language']})
    data={'login':user['login'],'retrieved_at':dt.datetime.now(dt.timezone.utc).date().isoformat(),
          'public_repositories':user['public_repos'],
          'stars_on_public_owned_repositories':sum(r['stargazers_count'] for r in repos),
          'primary_languages_in_original_public_repositories':languages,
          'sources':['https://api.github.com/users/M1Vj','https://api.github.com/users/M1Vj/repos?per_page=100&type=owner']}
    assert len(repos)==data['public_repositories'],'Incomplete public repository inventory'
    (ROOT/'sources-stats.json').write_text(json.dumps(data,indent=2)+'\n')

def hero(theme,mobile=False,still=False):
    c=PALETTES[theme]
    w,h=(600,300) if mobile else (1200,300)
    x=34 if mobile else 54
    name_size=57 if mobile else 91
    name_y=115 if mobile else 151
    role_y=160 if mobile else 201
    dots=[]
    gx,gy=(421,174) if mobile else (898,56)
    pitch=13 if mobile else 22
    for row in range(9):
        for col in range(10):
            level=(row*7+col*3)%11
            if (row+2*col)%5==0:continue
            fill=c['bright'] if level>7 else c['accent']
            dots.append(f'<circle cx="{gx+col*pitch}" cy="{gy+row*pitch}" r="{2 if mobile else 3.4}" fill="{fill}" opacity="{.18+level*.065:.2f}"/>')
    line_y=193 if mobile else 235
    motion='' if still else '<style>.signal{animation:signal 3.6s ease-out 1}@keyframes signal{from{stroke-dashoffset:110}to{stroke-dashoffset:0}}@media(prefers-reduced-motion:reduce){.signal{animation:none}}</style>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">Vj Mabansag — Applied AI and full-stack development</title><desc id="desc">A typographic header in blue with a decorative dot matrix. Embeddings, transformers and AI agents.</desc>{motion}
<rect width="{w}" height="{h}" rx="16" fill="{c['bg']}"/>
<path d="M{x} 40h25" stroke="{c['accent']}" stroke-width="3"/>
<text x="{x+37}" y="45" fill="{c['muted']}" font-family="{MONO}" font-size="14">M1Vj</text>
<text x="{x}" y="{name_y}" fill="{c['ink']}" font-family="{FONT}" font-size="{name_size}" font-weight="700" letter-spacing="{-3 if mobile else -5}">Vj Mabansag</text>
<text x="{x}" y="{role_y}" fill="{c['muted']}" font-family="{FONT}" font-size="{20 if mobile else 26}">Applied AI &amp; full-stack development</text>
<path d="M{x} {line_y}h{300 if mobile else 490}" fill="none" stroke="{c['line']}"/>
<path class="signal" d="M{x} {line_y}h110" fill="none" stroke="{c['accent']}" stroke-width="2" stroke-dasharray="110"/>
<text x="{x}" y="{234 if mobile else 272}" fill="{c['accent']}" font-family="{FONT}" font-size="{16 if mobile else 18}">Embeddings · Transformers · AI agents</text>
<g>{''.join(dots)}</g>
</svg>'''

def stats_svg(theme,stats,mobile=False):
    c=PALETTES[theme]
    values=[(stats['public_repositories'],'Public repos'),(stats['stars_on_public_owned_repositories'],'GitHub stars'),
            (len(stats['primary_languages_in_original_public_repositories']),'Languages')]
    groups=[]
    for i,(value,label) in enumerate(values):
        x=32+i*(200 if mobile else 400)
        if i:groups.append(f'<path d="M{x-25} 24v82" stroke="{c["line"]}"/>')
        groups.append(f'<text x="{x}" y="65" font-family="{FONT}" font-size="44" font-weight="700" fill="{c["ink"]}">{value}</text><text x="{x}" y="96" font-family="{FONT}" font-size="20" fill="{c["muted"]}">{label}</text>')
    desc=', '.join(f'{v} {l.lower()}' for v,l in values)
    w,h=(600,132) if mobile else (1200,132)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">Public GitHub snapshot: {desc}. Updated {stats["retrieved_at"]}.</title><rect width="{w}" height="{h}" rx="12" fill="{c["bg"]}"/>{"".join(groups)}</svg>'

BODY='''<details>
<summary><b>Projects</b> — AI tools &amp; full-stack builds</summary>

- **[HydraLab](https://github.com/M1Vj/HydraLab)** — My local research workbench for reading, citations, writing and research agents. Pre-release.
- **[VSU SmartMap](https://github.com/M1Vj/VSU-SmartMap)** — Campus navigation with Gemini-powered location chat. Started as a group project; now maintained solo. [Open map](https://vsumap.vercel.app/).
- **[MathWiz Arena / centipede](https://github.com/M1Vj/centipede)** — Lead developer on a collaborative math competition platform.
- **[Dormy](https://github.com/M1Vj/Dormy)** — My solo-built dormitory operations app. **UniDorm is a separate group project.**
- **[CodexSwap](https://github.com/M1Vj/CodexSwap)** — Native macOS tooling. **[VSUEE skill](https://github.com/M1Vj/vsuee-skill)** — E-learning automation for AI agents.

</details>

<details>
<summary><b>Research</b> — embeddings, transformers &amp; evaluation</summary>

My undergraduate research compares passive AI-text detector scores on paired watermarked and unwatermarked Gemma responses, using Python analysis and reproducibility checks.

I focus on **embeddings, transformers, NLP, AI agents and evaluation**. Detector scores require careful interpretation.

</details>

<details>
<summary><b>Toolbox</b> — Python, TypeScript &amp; beyond</summary>

**Python · TypeScript · React / Next.js · FastAPI · PostgreSQL / Supabase · Git**

</details>

<details>
<summary><b>About</b> — background &amp; opportunities</summary>

I'm a **BS Computer Science student at Visayas State University**, Philippines, with expected completion in **July 2027**. My direction is **applied AI**, followed by **AI research** and **AI governance**.

During my **AI4GOV internship**, I contributed with Pod B to **SangkAI**, a civic-feedback prototype. My work included AI workflows, prompts, fallback behavior, safety checks, testing and documentation. Staff review AI suggestions before decisions.

Open to **early-career applied AI and software development opportunities**. [Connect on LinkedIn](https://www.linkedin.com/in/m1vj/).

</details>
'''

def picture(kind,still=False):
    sources=[]
    if kind=='hero':
        for reduced in ([True] if still else [True,False]):
            for mobile,theme in [(True,'dark'),(True,'light'),(False,'dark'),(False,'light')]:
                media=[]
                if reduced and not still:media.append('(prefers-reduced-motion: reduce)')
                if mobile:media.append('(max-width: 600px)')
                if theme=='dark':media.append('(prefers-color-scheme: dark)')
                name=f'hero-{theme}'+('-mobile' if mobile else '')+('-still' if reduced else '')+'.svg'
                if media:sources.append(f'  <source media="{" and ".join(media)}" srcset="./assets/{name}">')
        default='hero-light'+('-still' if still else '')+'.svg'
        alt='Vj Mabansag — Applied AI and full-stack development. Embeddings, transformers and AI agents.'
    else:
        sources=['  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/stats-dark-mobile.svg">',
                 '  <source media="(max-width: 600px)" srcset="./assets/stats-light-mobile.svg">',
                 '  <source media="(prefers-color-scheme: dark)" srcset="./assets/stats-dark.svg">']
        default='stats-light.svg'
        data=json.loads((ROOT/'sources-stats.json').read_text())
        payload=''.join(stats_svg(theme,data,mobile) for theme in PALETTES for mobile in [False,True])
        version=hashlib.sha256(payload.encode()).hexdigest()[:12]
        sources=[source.replace('.svg"',f'.svg?v={version}"') for source in sources]
        default+=f'?v={version}'
        alt=f'Public GitHub stats: {data["public_repositories"]} repositories, {data["stars_on_public_owned_repositories"]} stars, {len(data["primary_languages_in_original_public_repositories"])} languages.'
    return '<picture>\n'+'\n'.join(sources)+f'\n  <img src="./assets/{default}" width="1200" alt="{html.escape(alt)}">\n</picture>\n\n'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--refresh-stats',action='store_true')
    args=parser.parse_args()
    if args.refresh_stats:refresh_stats()
    data=json.loads((ROOT/'sources-stats.json').read_text())
    assert data['login']=='M1Vj'
    ASSETS.mkdir(parents=True,exist_ok=True)
    for theme in PALETTES:
        for mobile in [False,True]:
            for still in [False,True]:
                name=f'hero-{theme}'+('-mobile' if mobile else '')+('-still' if still else '')+'.svg'
                (ASSETS/name).write_text(hero(theme,mobile,still))
        for mobile in [False,True]:
            (ASSETS/(f'stats-{theme}'+('-mobile' if mobile else '')+'.svg')).write_text(stats_svg(theme,data,mobile))
    for still,name in [(False,'README.md'),(True,'PROFILE-STILL.md')]:
        intro='**Building useful AI tools.**\n\n'
        date=f'<sub>Public GitHub snapshot · {data["retrieved_at"]}</sub>\n\n'
        footer='\n[LinkedIn](https://www.linkedin.com/in/m1vj/) · [Repositories](https://github.com/M1Vj?tab=repositories)'
        if not still:footer+=' · [Still version](./PROFILE-STILL.md)'
        else:footer+=' · [Animated version](./README.md)'
        (ROOT/name).write_text(picture('hero',still)+intro+picture('stats')+date+BODY+footer+'\n')
    print(json.dumps({'assets':12,'details':4,'stats':data}))

if __name__=='__main__':main()
