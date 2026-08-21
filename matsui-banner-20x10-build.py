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

# Trim (finished) size is 240x120in mapped to 6000x3000 css px -> 25 px/in.
# No printer spec was supplied, so this uses the common vinyl-banner setup:
# 2in bleed all round and a 4in safe margin inside trim, which clears the
# hem and grommet line on a banner this size.
TRIM_W, TRIM_H = 6000, 3000        # 240 x 120 in
PX_PER_IN = 25
BLEED_IN, SAFE_IN = 2, 4
BLEED = BLEED_IN * PX_PER_IN       # 50 px
SAFE  = SAFE_IN * PX_PER_IN        # 100 px
W, H = TRIM_W + BLEED*2, TRIM_H + BLEED*2   # 6100 x 3100 = 244 x 124 in

# On a booth the lower part of a 10ft-tall banner sits behind tables, below
# eye level and often blocked by people, so a strip along the bottom carries
# background only -- nothing there is load-bearing if it is never seen.
CLEAR_IN = 30                      # 2.5 ft of clear space at the foot
CONTENT_H = TRIM_H - CLEAR_IN * PX_PER_IN      # 2250 px = 90 in
# Bottom padding has to clear the deepest drop-shadow as well as the artwork,
# or the shadows feather down past the line into the zone that must stay clean.
BOT_PAD = 58                       # content no longer runs to the hem, so the
                                   # 4in safe margin is only needed up top

# Column widths are set to what each machine needs at full height, so the space
# between the three blocks is this one number rather than an accident of how
# percentages happened to divide. With the columns this wide the group nearly
# fills the sheet: outer margins land just under 5in, a little over the 4in
# safe line.
COL_GAP = 200

SHOW_GUIDES = '--guides' in sys.argv

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
# Official lockups. Each already contains the CMYK droplets, the wordmark and
# the "BY MATSUI INTERNATIONAL" line, so they replace the whole typeset block.
mm4_logo = b64('mm4_logo.png')
mm2_logo = b64('mm2_logo.png')
MESH = ('<div class="bg-mesh" style="background-image:url(data:image/png;base64,'
        + b64('mesh.png') + ')"></div>')

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

# Three bars sit side by side across the column, so each label breaks over two
# lines at the same weight -- it is one label, not a heading and a sub-line.
MM2_FEATURES = [('speed', 'HIGH-SPEED', 'PRODUCTION'),
                ('drop', 'VIBRANT', 'COLOR'),
                ('target', 'SHARP', 'DETAIL')]
MM4_FEATURE = ('glue-drop', 'ONE SYSTEM &mdash; POWDER + POWDERLESS')
CONS_SPAN = {'cmykw':'s6','jetting':'s2','cleaner':'s2','powder':'s2',
             'paper_film':'s3','pet_film':'s3'}
CONSUMABLES = [('cmykw','CMYKW'), ('jetting','JETTING GLUE'),
               ('cleaner','CLEANER ST'), ('powder','POWDER'),
               ('paper_film','PAPER FILMS'), ('pet_film','PET FILMS')]

def mm2_feats():
    return ''.join(
        f'<div class="feat"><span class="ic" style="color:#FFFFFF">{icon(ICONS[i])}</span>'
        f'<div class="ft"><b>{a}</b><b>{b}</b></div></div>'
        for i, a, b in MM2_FEATURES)

def mm4_feat():
    i, label = MM4_FEATURE
    return (f'<div class="feat feat-solo"><span class="ic" style="color:#FFFFFF">'
            f'{icon(ICONS[i])}</span><div class="ft"><b>{label}</b></div></div>')

def cons_cards():
    return ''.join(
        f'<div class="cons-card {CONS_SPAN[k]}">'
        f'<div class="shot"><img src="data:image/png;base64,{PROD[k]}" alt="{lab}"/></div>'
        f'<div class="clab">{lab}</div></div>'
        for k, lab in CONSUMABLES)

# ------------------------------------------------------------------- styles

# The background lives in its own absolutely-positioned layer so it can be
# rendered, swapped or suppressed independently of the content.
BG_HTML = f'''
  <div class="bg">
    <div class="bg-base"></div>
    {MESH}
    <div class="bg-vig"></div>
  </div>'''

BG_CSS = f'''
.bg {{ position:absolute; inset:0; z-index:0; }}
.bg-base {{ position:absolute; inset:0; background:#08060F; }}


/* MM4 — cool teal */

/* MM2 — magenta / violet */

/* consumables — warm gold */


/* woven cloth: warp and weft crossing, the substrate the ink prints on */
.bg-weave {{
  position:absolute; inset:0; mix-blend-mode:overlay; opacity:0.5;
  background-image:
    repeating-linear-gradient(90deg, rgba(255,255,255,0.10) 0 2px, rgba(0,0,0,0.07) 2px 5px),
    repeating-linear-gradient(0deg,  rgba(255,255,255,0.08) 0 2px, rgba(0,0,0,0.06) 2px 5px);
}}
/* halftone: the screen-print reference, fading in from the edges */
.bg-halftone {{
  position:absolute; inset:0; opacity:0.5;
  background-image: radial-gradient(rgba(255,255,255,0.16) 2.4px, transparent 2.6px);
  background-size: 30px 30px;
  -webkit-mask-image: radial-gradient(ellipse 66% 60% at 50% 50%, transparent 42%, #000 100%);
  mask-image: radial-gradient(ellipse 66% 60% at 50% 50%, transparent 42%, #000 100%);
}}
/* a slow diagonal sheen, like light across satin */
.bg-sheen {{
  position:absolute; inset:0; mix-blend-mode:screen; opacity:0.30;
  background:linear-gradient(104deg,
    rgba(255,255,255,0) 34%, rgba(255,255,255,0.16) 47%,
    rgba(255,255,255,0.04) 54%, rgba(255,255,255,0) 66%);
}}
.bg-mesh {{
  position:absolute; inset:0;
  background-size:100% 100%; background-repeat:no-repeat;
}}
/* Holds quiet ground under the headlines: heaviest at the top where type
   sits, lifting through the middle so the mesh stays vivid behind the
   machines. */
.bg-scrim {{
  position:absolute; inset:0;
  background:linear-gradient(180deg,
    rgba(4,3,10,0.40) 0%, rgba(4,3,10,0.22) 20%,
    rgba(4,3,10,0.04) 48%, rgba(4,3,10,0.00) 74%,
    rgba(4,3,10,0.16) 100%);
}}
.bg-vig {{
  position:absolute; inset:0;
  background:radial-gradient(ellipse 78% 66% at 50% 38%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.30) 100%);
}}
.bg-unused-seam {{
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

.unify {{
  position:absolute; inset:0; z-index:3; pointer-events:none;
  background:radial-gradient(ellipse 92% 82% at 50% 38%,
    rgba(150,140,210,0.06) 0%, rgba(60,40,110,0.10) 62%, rgba(10,6,24,0.22) 100%);
  mix-blend-mode:soft-light;
  /* This wash exists to tie the composited subjects to the ground. There are
     no subjects in the lower third, so it fades out before the clear zone --
     that leaves the artwork layer genuinely empty there, which is what makes
     the background swappable without a ghost tint riding along. */
  -webkit-mask-image:linear-gradient(180deg,#000 0%,#000 62%,transparent 74%);
  mask-image:linear-gradient(180deg,#000 0%,#000 62%,transparent 74%);
}}

.content {{
  position:absolute; z-index:2; display:flex;
  top:{BLEED}px; left:{BLEED}px; width:{TRIM_W}px; height:{CONTENT_H}px;
  justify-content:center; gap:{COL_GAP}px;
  /* hard guarantee that nothing -- including the tail of a blurred shadow --
     reaches the lower third. Padding already keeps the shadows clear, so the
     clip only ever catches a few per cent of alpha. */
  overflow:hidden;
}}

.col {{ position:relative; display:flex; flex-direction:column; align-items:center; }}
.col-mm4  {{ width:2072px; padding:{SAFE+6}px 0 0; }}
.col-mm2  {{ width:1798px; padding:{SAFE+6}px 0 0; }}
.col-cons {{ width:1510px; padding:{SAFE+6}px 0 0; }}

/* ---- brandmark ---- */
.droprow {{ display:inline-flex; align-items:center; }}
.brand {{ display:flex; flex-direction:column; align-items:center; }}
.brand .name {{
  font-family:'Display',sans-serif; font-weight:700; font-size:104px;
  color:#fff; letter-spacing:-1px; margin-top:12px; line-height:1;
}}
.brand .sub {{
  font-family:'Body',sans-serif; font-weight:600; font-size:38px; letter-spacing:8px;
  color:rgba(255,255,255,0.66); margin-top:18px; text-align:center;
}}
.brand .sub2 {{
  font-family:'Body',sans-serif; font-weight:400; font-size:30px; letter-spacing:6px;
  color:rgba(255,255,255,0.48); margin-top:8px;
}}
.brand::after {{
  content:""; display:block; width:170px; height:1px; margin:30px auto 0;
  background:linear-gradient(90deg,rgba(255,255,255,0) 0%,rgba(255,255,255,0.55) 50%,rgba(255,255,255,0) 100%);
}}

/* ---- headline ---- */
.lockup {{ display:block; height:auto; margin:0 auto;
  filter:drop-shadow(0 12px 28px rgba(0,0,0,0.55)); }}
.lockup-mm4 {{ width:100%; max-width:1440px; }}
.lockup-mm2 {{ width:100%; max-width:1411px; margin-top:12px; }}

.hl {{ text-align:center; margin-top:40px; }}
.hl .main {{
  display:block; font-family:'Display',sans-serif; font-weight:700;
  font-size:112px; letter-spacing:-2px; line-height:1;
  background:linear-gradient(180deg,#FFFFFF 0%,#C6D3DC 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
}}
.hl .sub {{
  display:block; font-family:'Body',sans-serif; font-weight:400; font-size:54px;
  letter-spacing:1.8px; color:rgba(255,255,255,0.86); margin-top:22px; line-height:1.4;
}}
.rainbow {{ text-align:center; margin-top:20px; }}
.rainbow span {{
  display:block; font-family:'Display',sans-serif; font-weight:700;
  font-size:68px; letter-spacing:0.5px; line-height:1.3;
}}
.rainbow .r1 {{ color:#A8F4FB; }}
.rainbow .r2 {{ color:#FFE28A; }}
.rainbow .r3 {{ color:#FFE3F4; }}

/* ---- feature chips ---- */
/* Wide full-width bars stacked down the column, rather than a wrapping row
   of near-square chips -- a long label reads faster across than stacked. */
.feats {{ display:flex; flex-direction:row; justify-content:center;
  align-items:stretch; gap:20px; width:100%; margin-top:32px; }}
.feat {{
  flex:1 1 0; min-width:0;
  display:flex; align-items:center; justify-content:center; gap:22px;
  background:rgba(6,12,18,0.34);
  border:1px solid rgba(255,255,255,0.34);
  border-radius:6px; padding:20px 30px;
}}
/* the lone MM4 bar hugs its label instead of stretching the full column */
.feat-solo {{ flex:0 0 auto; padding:20px 44px; }}
.col-mm2 .feats {{ margin-top:24px; }}
/* Lifting the icon out of the flow lets the label centre on the box itself.
   Left in the flow it centres as an icon+text pair, which sits the words a
   couple of inches right of centre. */
.col-mm2 .feat {{ position:relative; }}
.col-mm2 .feat .ic {{ position:absolute; left:32px; top:50%; transform:translateY(-50%); }}
.feat .ic {{ width:76px; height:76px; flex:none; display:block; }}
.feat .ic svg {{ width:100%; height:100%; display:block; }}
.ft {{ display:flex; flex-direction:column; line-height:1.24; text-align:center; }}
.ft b {{ font-family:'Body',sans-serif; font-weight:700; font-size:48px; letter-spacing:2px; color:#fff; }}
.ft span {{ font-family:'Body',sans-serif; font-weight:400; font-size:40px; letter-spacing:1.6px; color:rgba(255,255,255,0.88); }}

/* ---- hero ---- */
.hero {{ flex:1; min-height:0; width:100%; display:flex; align-items:flex-end; justify-content:center; padding-bottom:{BOT_PAD}px; }}
.hero img {{ width:100%; max-width:none; height:auto; max-height:100%; object-fit:contain; display:block;
             filter:drop-shadow(0 24px 30px rgba(0,0,0,0.62)); }}

/* ---- consumables column ---- */
.cons-top {{
  display:flex; align-items:center; justify-content:center; gap:46px;
}}
.cons-top img.logo {{ height:460px; display:block;
  filter:drop-shadow(0 10px 26px rgba(0,0,0,0.55)); }}
.cons-title {{
  font-family:'Display',sans-serif; font-weight:700; font-size:82px; letter-spacing:-0.5px;
  margin-top:30px; text-align:center; color:#fff;
}}
.cons-title span {{ color:#FFE28A; }}
.cons-rule {{
  width:210px; height:1px; margin:20px auto 28px;
  background:linear-gradient(90deg,rgba(255,226,138,0) 0%,#FFE28A 50%,rgba(255,226,138,0) 100%);
}}
.cons-grid {{
  flex:1; min-height:0; width:100%;
  display:grid; grid-template-columns:repeat(6,1fr);
  grid-auto-rows:1fr; gap:24px;
  padding-bottom:{BOT_PAD}px;
}}
.cons-card {{
  background:linear-gradient(180deg,rgba(6,12,18,0.40) 0%,rgba(6,12,18,0.26) 100%);
  border:1px solid rgba(255,255,255,0.28); border-radius:6px;
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
  font-size:44px; letter-spacing:2.4px; color:#F2F7FA; text-align:center; line-height:1.25;
}}
'''

CONTENT_HTML = f'''
  <div class="content">

    <div class="col col-mm4">
      <img class="lockup lockup-mm4" src="data:image/png;base64,{mm4_logo}"
           alt="MM4 DIGITAL — DTF Hybrid Powder / Powderless by Matsui International"/>
      <div class="hl">
        <span class="main">HYBRID</span>
      </div>
      <div class="feats">{mm4_feat()}</div>
      <div class="hero"><img src="data:image/png;base64,{mm4_hero}" alt="MM4 Digital DTF printer"/></div>
    </div>

    <div class="col col-mm2">
      <img class="lockup lockup-mm2" src="data:image/png;base64,{mm2_logo}"
           alt="MM2 DIGITAL by Matsui International"/>
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
      </div>
      <div class="cons-title">DTF <span>CONSUMABLES</span></div>
      <div class="cons-rule"></div>
      <div class="cons-grid">{cons_cards()}</div>
    </div>

  </div>'''

GUIDE_HTML = f'''
  <div class="guides">
    <div class="g-trim"></div><div class="g-safe"></div>
    <div class="g-tag g-tag-trim">TRIM 240 x 120 in</div>
    <div class="g-tag g-tag-bleed">BLEED {BLEED_IN}in — 244 x 124 in</div>
    <div class="g-tag g-tag-safe">SAFE {SAFE_IN}in</div>
    <div class="g-clear"></div>
    <div class="g-tag g-tag-clear">CLEAR ZONE — bottom {CLEAR_IN} in (2.5 ft) background only</div>
  </div>'''

GUIDE_CSS = f'''
.guides {{ position:absolute; inset:0; z-index:50; pointer-events:none; }}
.g-trim {{ position:absolute; top:{BLEED}px; left:{BLEED}px;
  width:{TRIM_W}px; height:{TRIM_H}px; outline:4px dashed #00E5FF; }}
.g-safe {{ position:absolute; top:{BLEED+SAFE}px; left:{BLEED+SAFE}px;
  width:{TRIM_W-SAFE*2}px; height:{TRIM_H-SAFE*2}px; outline:4px dashed #FFD400; }}
.g-tag {{ position:absolute; font-family:'Body',sans-serif; font-weight:700;
  font-size:34px; letter-spacing:2px; padding:10px 18px; border-radius:4px; }}
/* the line content is held above -- everything below is background only */
.g-clear {{ position:absolute; left:{BLEED}px; width:{TRIM_W}px;
  top:{BLEED+CONTENT_H}px; height:0; outline:4px dashed #7CFF6B; }}
.g-tag-clear {{ top:{BLEED+CONTENT_H+16}px; left:{BLEED+14}px;
  background:#7CFF6B; color:#0B2400; }}
.g-tag-bleed {{ top:8px; left:12px; background:#FF2D8E; color:#fff; }}
.g-tag-trim  {{ top:{BLEED+14}px; left:{BLEED+14}px; background:#00E5FF; color:#00232B; }}
.g-tag-safe  {{ top:{BLEED+SAFE+14}px; left:{BLEED+SAFE+14}px; background:#FFD400; color:#2B2200; }}
'''

body_parts = []
if LAYER in ('bg', 'all'):
    body_parts.append(BG_HTML)
if LAYER in ('fg', 'all'):
    body_parts.append(CONTENT_HTML)
if LAYER in ('fg', 'all'):
    body_parts.append('<div class="unify"></div>')
if SHOW_GUIDES:
    body_parts.append(GUIDE_HTML)

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
{GUIDE_CSS if SHOW_GUIDES else ''}
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

out = f'wide_{LAYER}{"_guides" if SHOW_GUIDES else ""}.html'
with open(out, 'w') as f:
    f.write(HTML)
print('wrote', out, len(HTML))
