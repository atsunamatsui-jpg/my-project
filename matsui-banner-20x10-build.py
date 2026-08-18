"""Builds the 20ft x 10ft (2:1) tradeshow banner.

Runs in three layer modes so the background can be swapped downstream:
  bg  -> background artwork only
  fg  -> all content, transparent ground
  all -> flattened composite
"""
import base64
import pathlib
import sys

LAYER = sys.argv[1] if len(sys.argv) > 1 else 'all'
assert LAYER in ('bg', 'fg', 'all')

W, H = 6000, 3000

def b64(p):
    with open(p, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

FONT_DIR = pathlib.Path('/mnt/skills/examples/canvas-design/canvas-fonts')

def font_face(file, family, weight=400):
    data = base64.b64encode((FONT_DIR / f'{file}.ttf').read_bytes()).decode('ascii')
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:normal;"
            f"font-display:block;src:url(data:font/ttf;base64,{data}) format('truetype');}}")

FONT_FACES = ''.join([
    font_face('BricolageGrotesque-Bold', 'Display', 700),
    font_face('Outfit-Regular', 'Body', 400),
    font_face('Outfit-Bold', 'Body', 700),
])

mm4_hero = b64('mm4_hero.png')
mm2_hero = b64('mm2_hero.png')
matsui_logo = b64('../logo_full.png')
qr = b64('qr_clean.png')
PROD = {k: b64(f'prod_{k}.png') for k in
        ['cmykw','jetting','cleaner','powder','paper_film','pet_film']}

CMYK = ['#00B3D6', '#E6007E', '#FFD400', '#161616']

# ------------------------------------------------------------------ pieces

def icon(body):
    return f'<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">{body}</svg>'

ICONS = {
 'drop': '<path d="M24 4C24 4 10 22 10 31a14 14 0 0 0 28 0C38 22 24 4 24 4Z" fill="currentColor"/>',
 'glue-drop': ('<path d="M24 4C24 4 10 22 10 31a14 14 0 0 0 28 0C38 22 24 4 24 4Z" fill="currentColor"/>'
               '<circle cx="19" cy="30" r="2.6" fill="#fff" opacity="0.85"/>'),
 'gear': ('<path fill="currentColor" d="M27.4 4.5 28.6 9a15.9 15.9 0 0 1 4.6 2.7l4.4-1.6 3 5.2-3.5 3.1a16 16 0 0 1 0 5.3l3.5 3.1-3 5.2-4.4-1.6a15.9 15.9 0 0 1-4.6 2.7l-1.2 4.5h-6l-1.2-4.5a15.9 15.9 0 0 1-4.6-2.7l-4.4 1.6-3-5.2 3.5-3.1a16 16 0 0 1 0-5.3l-3.5-3.1 3-5.2 4.4 1.6a15.9 15.9 0 0 1 4.6-2.7l1.2-4.5Z"/>'
          '<circle cx="24" cy="24" r="7" fill="#0A0F14"/>'),
 'target': ('<circle cx="24" cy="24" r="18" stroke="currentColor" stroke-width="3.4" fill="none"/>'
            '<circle cx="24" cy="24" r="10.5" stroke="currentColor" stroke-width="3.4" fill="none"/>'
            '<circle cx="24" cy="24" r="3.4" fill="currentColor"/>'),
 'speed': ('<path d="M6 30a18 18 0 0 1 36 0" stroke="currentColor" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
           '<path d="M24 30 33 17" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"/>'
           '<circle cx="24" cy="30" r="3" fill="currentColor"/>'),
 'eco': ('<path d="M24 42C12 42 7 33 7 22 18 22 24 27 24 37 24 27 30 22 41 22c0 11-5 20-17 20Z" fill="currentColor"/>'
         '<path d="M24 42V17" stroke="#0A0F14" stroke-width="2.6" stroke-linecap="round"/>'),
}

def droplets(h=54):
    out = ''
    for i, c in enumerate(CMYK):
        out += (f'<svg style="width:{h}px;height:{h}px;margin-left:{-h*0.42 if i else 0}px;'
                f'position:relative;z-index:{10-i}" viewBox="0 0 48 48">'
                f'<path d="M24 4C24 4 8 24 8 33a16 16 0 0 0 32 0C40 24 24 4 24 4Z" fill="{c}"/></svg>')
    return f'<span class="droprow">{out}</span>'

MM4_FEATURES = [('drop', '#4FD8EE', 'WASH DURABLE', '60°C × 5 CYCLES'),
                ('glue-drop', '#FFAE4A', 'INKJET-PRINTABLE', 'GLUE + POWDER')]
MM2_FEATURES = [('gear', 'AUTOMATED', 'MAINTENANCE'), ('target', 'PRECISION', 'PRINTING'),
                ('speed', 'HIGH-SPEED', 'PRODUCTION'), ('eco', 'SMART & ECO', 'OPERATION')]
CONS_SPAN = {'cmykw':'s6','jetting':'s2','cleaner':'s2','powder':'s2',
             'paper_film':'s3','pet_film':'s3'}
CONSUMABLES = [('cmykw','POWDERLESS CMYKW'), ('jetting','JETTING GLUE'),
               ('cleaner','CLEANER ST'), ('powder','HYBRID POWDER'),
               ('paper_film','POWDERLESS PAPER FILMS'), ('pet_film','POWDERLESS PET FILMS')]

def mm4_feats():
    return ''.join(
        f'<div class="feat"><span class="ic" style="color:{col}">{icon(ICONS[i])}</span>'
        f'<div class="ft"><b>{a}</b><span>{b}</span></div></div>'
        for i, col, a, b in MM4_FEATURES)

def mm2_feats():
    return ''.join(
        f'<div class="feat feat-c"><span class="ic" style="color:#FFFFFF">{icon(ICONS[i])}</span>'
        f'<div class="ft"><b>{a}</b><span>{b}</span></div></div>'
        for i, a, b in MM2_FEATURES)

def cons_cards():
    return ''.join(
        f'<div class="cons-card {CONS_SPAN[k]}">'
        f'<div class="shot"><img src="data:image/png;base64,{PROD[k]}" alt="{lab}"/></div>'
        f'<div class="clab">{lab}</div></div>'
        for k, lab in CONSUMABLES)

# ------------------------------------------------------------------- styles

# The background lives in its own absolutely-positioned layer so it can be
# rendered, swapped or suppressed independently of the content.
BG_HTML = '''
  <div class="bg">
    <div class="bg-base"></div>
    <div class="bg-p bg-p1"></div>
    <div class="bg-p bg-p2"></div>
    <div class="bg-p bg-p3"></div>
    <div class="bg-grain"></div>
    <div class="bg-vig"></div>
    <div class="bg-rule"></div>
  </div>'''

BG_CSS = f'''
.bg {{ position:absolute; inset:0; z-index:0; }}
.bg-base {{ position:absolute; inset:0; background:#07090D; }}

.bg-p {{ position:absolute; top:0; bottom:0; }}
/* MM4 — cool teal */
.bg-p1 {{
  left:0; width:38%;
  background:
    radial-gradient(ellipse 76% 58% at 44% 34%, rgba(0,190,214,0.34) 0%, rgba(0,190,214,0) 64%),
    radial-gradient(ellipse 60% 44% at 10% 94%, rgba(0,120,150,0.24) 0%, rgba(0,120,150,0) 62%),
    linear-gradient(168deg,#070C11 0%,#0A141B 48%,#07101A 100%);
  clip-path: polygon(0 0, 100% 0, 88% 100%, 0% 100%);
}}
/* MM2 — magenta / violet */
.bg-p2 {{
  left:32%; width:40%;
  background:
    radial-gradient(ellipse 74% 56% at 52% 32%, rgba(214,0,140,0.30) 0%, rgba(214,0,140,0) 64%),
    radial-gradient(ellipse 60% 44% at 88% 94%, rgba(110,40,190,0.26) 0%, rgba(110,40,190,0) 62%),
    linear-gradient(168deg,#0A0710 0%,#140A1C 48%,#0D0715 100%);
  clip-path: polygon(12% 0, 100% 0, 88% 100%, 0% 100%);
}}
/* consumables — warm gold */
.bg-p3 {{
  left:66%; right:0; width:34%;
  background:
    radial-gradient(ellipse 72% 56% at 56% 30%, rgba(201,162,39,0.24) 0%, rgba(201,162,39,0) 64%),
    linear-gradient(168deg,#0B0A07 0%,#14110A 48%,#0C0B07 100%);
  clip-path: polygon(12% 0, 100% 0, 100% 100%, 0% 100%);
}}

.bg-grain {{
  position:absolute; inset:0;
  background-image: radial-gradient(rgba(255,255,255,0.05) 2px, transparent 2.2px);
  background-size: 34px 34px;
}}
.bg-vig {{
  position:absolute; inset:0;
  background:radial-gradient(ellipse 76% 66% at 50% 46%, rgba(0,0,0,0) 56%, rgba(0,0,0,0.48) 100%);
}}
.bg-p2::before, .bg-p3::before {{
  content:""; position:absolute; top:0; bottom:0; left:0; width:3px;
  background:linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.42) 45%, rgba(255,255,255,0) 100%);
  transform:skewX(-6.8deg); transform-origin:top;
}}
.bg-rule {{
  position:absolute; top:0; left:0; right:0; height:14px;
  background:linear-gradient(90deg,#00BED6 0%,#5A6BE0 34%,#C9A227 62%,#FF2D8E 100%);
}}
'''

FG_CSS = f'''
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ background:#0A0A0A; }}
body {{ display:flex; justify-content:center; align-items:center; }}

.banner {{
  position:relative; width:{W}px; height:{H}px; overflow:hidden;
  font-family:'Body',sans-serif;
}}

.content {{ position:absolute; inset:0; z-index:2; display:flex; }}

.col {{ position:relative; display:flex; flex-direction:column; align-items:center; }}
.col-mm4  {{ width:38%; padding:78px 60px 0; }}
.col-mm2  {{ width:34%; padding:78px 50px 0; }}
.col-cons {{ width:28%; padding:78px 60px 0; }}

/* ---- brandmark ---- */
.droprow {{ display:inline-flex; align-items:center; }}
.brand {{ display:flex; flex-direction:column; align-items:center; }}
.brand .name {{
  font-family:'Display',sans-serif; font-weight:700; font-size:104px;
  color:#fff; letter-spacing:-1px; margin-top:12px; line-height:1;
}}
.brand .sub {{
  font-family:'Body',sans-serif; font-weight:600; font-size:26px; letter-spacing:7px;
  color:rgba(255,255,255,0.66); margin-top:18px; text-align:center;
}}
.brand .sub2 {{
  font-family:'Body',sans-serif; font-weight:400; font-size:20px; letter-spacing:5px;
  color:rgba(255,255,255,0.48); margin-top:8px;
}}
.brand::after {{
  content:""; display:block; width:170px; height:1px; margin:30px auto 0;
  background:linear-gradient(90deg,rgba(255,255,255,0) 0%,rgba(255,255,255,0.55) 50%,rgba(255,255,255,0) 100%);
}}

/* ---- headline ---- */
.hl {{ text-align:center; margin-top:26px; }}
.hl .main {{
  display:block; font-family:'Display',sans-serif; font-weight:700;
  font-size:112px; letter-spacing:-2px; line-height:1;
  background:linear-gradient(180deg,#FFFFFF 0%,#C6D3DC 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
}}
.hl .sub {{
  display:block; font-family:'Body',sans-serif; font-weight:400; font-size:27px;
  letter-spacing:1.6px; color:rgba(255,255,255,0.74); margin-top:22px; line-height:1.5;
}}
.rainbow {{ text-align:center; margin-top:26px; }}
.rainbow span {{
  display:block; font-family:'Display',sans-serif; font-weight:700;
  font-size:60px; letter-spacing:0.5px; line-height:1.3;
}}
.rainbow .r1 {{ color:#7FE9F3; }}
.rainbow .r2 {{ color:#F2D06B; }}
.rainbow .r3 {{ color:#FF8FD0; }}

/* ---- feature chips ---- */
.feats {{ display:flex; gap:24px; justify-content:center; flex-wrap:wrap; margin-top:34px; }}
.feat {{
  display:flex; align-items:center; gap:20px;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.17);
  border-radius:5px; padding:22px 30px;
}}
.feat .ic {{ width:64px; height:64px; flex:none; display:block; }}
.feat .ic svg {{ width:100%; height:100%; display:block; }}
.feat.feat-c {{ flex-direction:column; text-align:center; gap:14px; padding:26px 24px; }}
.feat.feat-c .ic {{ width:70px; height:70px; }}
.ft {{ display:flex; flex-direction:column; line-height:1.24; }}
.ft b {{ font-family:'Body',sans-serif; font-weight:700; font-size:25px; letter-spacing:1.8px; color:#fff; }}
.ft span {{ font-family:'Body',sans-serif; font-weight:400; font-size:20px; letter-spacing:1.5px; color:rgba(255,255,255,0.76); }}

/* ---- hero ---- */
.hero {{ flex:1; min-height:0; width:100%; display:flex; align-items:center; justify-content:center; padding-bottom:60px; }}
.hero img {{ width:104%; max-width:none; height:auto; max-height:100%; object-fit:contain; display:block;
             filter:drop-shadow(0 46px 54px rgba(0,0,0,0.62)); }}

/* ---- consumables column ---- */
.cons-top {{ display:flex; align-items:center; justify-content:center; gap:34px; }}
.cons-top img.logo {{ height:120px; filter:brightness(0) invert(1); }}
.cons-top img.qr {{ width:132px; height:132px; background:#fff; padding:9px; border-radius:6px; }}
.cons-title {{
  font-family:'Display',sans-serif; font-weight:700; font-size:76px; letter-spacing:-0.5px;
  margin-top:44px; text-align:center; color:#fff;
}}
.cons-title span {{ color:#C9A227; }}
.cons-rule {{
  width:210px; height:1px; margin:26px auto 40px;
  background:linear-gradient(90deg,rgba(201,162,39,0) 0%,#C9A227 50%,rgba(201,162,39,0) 100%);
}}
.cons-grid {{
  flex:1; min-height:0; width:100%;
  display:grid; grid-template-columns:repeat(6,1fr);
  grid-auto-rows:1fr; gap:24px;
  padding-bottom:70px;
}}
.cons-card {{
  background:linear-gradient(180deg,rgba(255,255,255,0.06) 0%,rgba(255,255,255,0.022) 100%);
  border:1px solid rgba(255,255,255,0.12); border-radius:6px;
  box-shadow:0 22px 46px -20px rgba(0,0,0,0.85);
  padding:30px 18px 22px;
  display:flex; flex-direction:column; align-items:center;
  min-height:0;
}}
.cons-card.s6 {{ grid-column:span 6; }}
.cons-card.s3 {{ grid-column:span 3; }}
.cons-card.s2 {{ grid-column:span 2; }}
.shot {{ flex:1; min-height:0; width:100%; display:flex; align-items:center; justify-content:center; }}
.shot img {{ width:100%; height:100%; object-fit:contain; display:block;
             filter:drop-shadow(0 20px 24px rgba(0,0,0,0.6)); }}
.clab {{
  margin-top:18px; font-family:'Body',sans-serif; font-weight:700;
  font-size:21px; letter-spacing:2.4px; color:#E4EBF0; text-align:center; line-height:1.3;
}}
'''

CONTENT_HTML = f'''
  <div class="content">

    <div class="col col-mm4">
      <div class="brand">
        {droplets()}
        <div class="name">MM4 DIGITAL</div>
        <div class="sub">DTF HYBRID POWDER / POWDERLESS</div>
        <div class="sub2">BY MATSUI INTERNATIONAL</div>
      </div>
      <div class="hl">
        <span class="main">HYBRID</span>
        <span class="sub">Printable by Conventional Methods!<br/>OEKO-TEX Application Pending</span>
      </div>
      <div class="feats">{mm4_feats()}</div>
      <div class="hero"><img src="data:image/png;base64,{mm4_hero}" alt="MM4 Digital DTF printer"/></div>
    </div>

    <div class="col col-mm2">
      <div class="brand">
        {droplets()}
        <div class="name">MM2 DIGITAL</div>
        <div class="sub2">BY MATSUI INTERNATIONAL</div>
      </div>
      <div class="rainbow">
        <span class="r1">VIBRANT COLORS</span>
        <span class="r2">SHARP REPRODUCTION</span>
        <span class="r3">VIVID EXPRESSION</span>
      </div>
      <div class="feats">{mm2_feats()}</div>
      <div class="hero"><img src="data:image/png;base64,{mm2_hero}" alt="MM2 Digital DTF printer"/></div>
    </div>

    <div class="col col-cons">
      <div class="cons-top">
        <img class="logo" src="data:image/png;base64,{matsui_logo}" alt="Matsui International"/>
        <img class="qr" src="data:image/png;base64,{qr}" alt="matsui-color.com"/>
      </div>
      <div class="cons-title">DTF <span>CONSUMABLES</span></div>
      <div class="cons-rule"></div>
      <div class="cons-grid">{cons_cards()}</div>
    </div>

  </div>'''

body_parts = []
if LAYER in ('bg', 'all'):
    body_parts.append(BG_HTML)
if LAYER in ('fg', 'all'):
    body_parts.append(CONTENT_HTML)

# a transparent page for the foreground layer so it can sit over any ground
page_bg = 'transparent' if LAYER == 'fg' else '#0A0A0A'

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>Matsui DTF Tradeshow Banner 20x10</title>
<meta name="hz:slide-selector" content=".banner"/>
<meta name="hz:canvas-width" content="{W}"/>
<meta name="hz:canvas-height" content="{H}"/>
<style>
{FONT_FACES}
{FG_CSS}
{BG_CSS}
html,body {{ background:{page_bg}; }}
.banner {{ background:{'transparent' if LAYER=='fg' else '#07090D'}; }}
</style>
</head>
<body>
  <div class="banner" data-canvas-width="{W}" data-canvas-height="{H}">
{''.join(body_parts)}
  </div>
</body>
</html>
'''

out = f'wide_{LAYER}.html'
with open(out, 'w') as f:
    f.write(HTML)
print('wrote', out, len(HTML))
