"""Builds the 10ft x 8ft Specialty Inks tradeshow banner.

Companion to the 20x10 DTF banner: same palette, same mesh background, same
bleed and safe-margin conventions, same clear strip at the foot.

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

# Trim (finished) size is 120x96in mapped to 3000x2400 css px -> 25 px/in,
# the same scale as the wide banner so type sizes carry across directly.
TRIM_W, TRIM_H = 3000, 2400        # 120 x 96 in = 10 x 8 ft
PX_PER_IN = 25
BLEED_IN, SAFE_IN = 2, 4
BLEED = BLEED_IN * PX_PER_IN       # 50 px
SAFE = SAFE_IN * PX_PER_IN         # 100 px
W, H = TRIM_W + BLEED*2, TRIM_H + BLEED*2      # 3100 x 2500 = 124 x 100 in

# Matches the wide banner: the foot of a booth banner sits behind tables and
# below eye level, so it carries background only.
CLEAR_IN = 30                      # 2.5 ft
CONTENT_H = TRIM_H - CLEAR_IN * PX_PER_IN      # 1650 px = 66 in
BOT_PAD = 26

# ---- header lockup geometry -------------------------------------------------
# "MATSUI" is one line inside logo_full.png, not the whole file, so matching it
# to the headline means solving for the logo's overall height. Measured off the
# artwork and the rendered face:
#   MATSUI cap height  = 20.18% of the logo file's height
#   MATSUI cap top     = 65.08% down the logo file
#   Bricolage Bold cap = 69.08% of font-size, ink starting 15.13% down the box
# Sizing the logo from those puts the two words at the same cap height, and
# offsetting the headline by the difference sits them on one line.
HEAD_FS = 118                                   # headline font-size
MATSUI_CAP_FRAC, MATSUI_TOP_FRAC = 0.2018, 0.6508
CAP_RATIO, INK_TOP_RATIO = 0.6908, 0.1513

HEAD_CAP = HEAD_FS * CAP_RATIO                  # cap height of SPECIALTY INKS
LOGO_H = round(HEAD_CAP / MATSUI_CAP_FRAC)      # logo height that matches it
HEAD_OFFSET = round(LOGO_H * MATSUI_TOP_FRAC - HEAD_FS * INK_TOP_RATIO)

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

matsui_logo = b64('../logo_full.png')
MESH = ('<div class="bg-mesh" style="background-image:url(data:image/png;base64,'
        + b64('mesh.png') + ')"></div>')

# Photographs ride as JPEG -- PNG would triple the page weight for no gain.
SHOTS = {k: b64(f'{k}.jpg') for k in
         ['vintage', 'pearlescent', 'g600', 'velvet', 'threed', 'eco']}

# Copy exactly as supplied, with trailing full stops levelled out so the three
# description lines sit as a consistent set. The one substantive change is
# "PU High Deccity" -> "PU High Density", flagged separately.
PRODUCTS = [
    ('vintage', 'Vintage White &amp; Base',
     ['High Mesh printing', 'Strong elasticity', 'Max 350 mesh'],
     'PU High Mesh White &amp; Base', 'Mesh 180~305', 'Cure 320℉ × 2min'),
    ('pearlescent', 'Pearlescent Shimmer',
     ['Pigmented any colors', 'Soft Hand', 'Strong Color Value'],
     'Acrylic Silver &amp; Gold', 'Mesh 100~135', 'Cure 320℉ × 2min'),
    ('g600', 'TOP G600 / TOP COAT',
     ['Super Gel Top Coat', 'Shine gloss', 'Using 0.5% Top Fixer (Catalyst)'],
     'PU Gel Top Coat', 'Mesh 80~135', 'Cure 270℉ × 2min'),
    ('velvet', 'Velvet PUFF',
     ['Feeling like Flock', 'Soft Hand', 'Strong Color Value'],
     'PU Puff', 'Mesh 100~135', 'Cure 280℉ × 2min'),
    ('threed', '3D White &amp; Clear',
     ['Waterbase High density', 'Use 100μ to 200μ', 'Soft Hand'],
     'PU High Density', 'Mesh 80~135', 'Cure 280℉ × 2min'),
    ('eco', 'ECO Discharge White DNFW &amp; Clear DNFM',
     ['Non-Formaldehyde Type', 'Great Color Value', 'Soft Hand'],
     'Acrylic White &amp; Clear', 'Mesh 80~155', 'Cure 320℉ × 2min'),
]


def panels():
    out = ''
    for key, title, bullets, base, mesh, cure in PRODUCTS:
        lines = ''.join(f'<li>{b}</li>' for b in bullets)
        out += f'''
      <div class="card">
        <div class="shot"><img src="data:image/jpeg;base64,{SHOTS[key]}" alt="{title} print sample"/></div>
        <div class="info">
          <h3>{title}</h3>
          <div class="cols">
            <ul>{lines}</ul>
            <div class="spec">
              <span class="base">{base}</span>
              <span class="nums"><b>{mesh}</b><i>·</i><b>{cure}</b></span>
            </div>
          </div>
        </div>
      </div>'''
    return out


BG_HTML = f'''
  <div class="bg">
    <div class="bg-base"></div>
    {MESH}
    <div class="bg-vig"></div>
  </div>'''

BG_CSS = '''
.bg { position:absolute; inset:0; z-index:0; }
.bg-base { position:absolute; inset:0; background:#08060F; }
.bg-mesh { position:absolute; inset:0; background-size:100% 100%; background-repeat:no-repeat; }
.bg-vig {
  position:absolute; inset:0;
  background:radial-gradient(ellipse 80% 66% at 50% 38%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.30) 100%);
}
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
  -webkit-mask-image:linear-gradient(180deg,#000 0%,#000 62%,transparent 74%);
  mask-image:linear-gradient(180deg,#000 0%,#000 62%,transparent 74%);
}}

/* Content is held above the clear strip, exactly as on the wide banner.
   Clipped rather than merely laid out, so no shadow tail can creep below. */
.content {{
  position:absolute; z-index:2; overflow:hidden;
  top:{BLEED}px; left:{BLEED}px; width:{TRIM_W}px; height:{CONTENT_H}px;
  padding:{SAFE}px {SAFE}px {BOT_PAD}px;
  display:flex; flex-direction:column; align-items:center;
}}

/* ---- header ----
   Logo and headline form one lockup, sized and offset so MATSUI and SPECIALTY
   INKS share a cap height and a baseline. Aligning tops rather than baselines
   is equivalent once the cap heights match, and it keeps the offset positive
   so the logo alone sets the header's height. */
.head {{ display:flex; flex-direction:column; align-items:center; }}
.lock {{ display:flex; flex-direction:row; align-items:flex-start; gap:40px; }}
.lock img {{ height:{LOGO_H}px; display:block; filter:drop-shadow(0 12px 30px rgba(0,0,0,0.55)); }}
.lock h1 {{
  font-family:'Display',sans-serif; font-weight:700; font-size:{HEAD_FS}px;
  letter-spacing:-2px; line-height:1; color:#fff; margin-top:{HEAD_OFFSET}px;
  text-shadow:0 8px 26px rgba(0,0,0,0.45);
}}
.lock h1 span {{ color:#FFE28A; }}
.head .rule {{
  width:100%; height:3px; margin-top:16px;
  background:linear-gradient(90deg,rgba(255,226,138,0) 0%,#FFE28A 50%,rgba(255,226,138,0) 100%);
}}

/* ---- product grid ---- */
.grid {{
  flex:1; min-height:0; width:100%; margin-top:22px;
  display:grid; grid-template-columns:repeat(2,1fr); grid-auto-rows:1fr; gap:22px 30px;
}}
.card {{
  display:flex; align-items:stretch; min-height:0; overflow:hidden;
  background:linear-gradient(180deg,rgba(6,12,18,0.42) 0%,rgba(6,12,18,0.26) 100%);
  border:1px solid rgba(255,255,255,0.30); border-radius:8px;
  box-shadow:0 20px 40px -22px rgba(0,0,0,0.85);
}}
.shot {{ flex:none; height:100%; aspect-ratio:4/3; background:#0B0B10; }}
.shot img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.info {{ flex:1; min-width:0; padding:14px 28px; display:flex; flex-direction:column; justify-content:center; }}
.info h3 {{
  font-family:'Display',sans-serif; font-weight:700; font-size:54px;
  line-height:1.06; letter-spacing:-0.5px; color:#fff;
}}
.cols {{ display:flex; flex-direction:row; align-items:flex-start; gap:30px; margin-top:14px; }}
.info ul {{ list-style:none; flex:1 1 auto; min-width:0; }}
.info li {{
  font-family:'Body',sans-serif; font-weight:400; font-size:32px; line-height:1.34;
  color:rgba(255,255,255,0.90); padding-left:28px; position:relative;
}}
.info li::before {{
  content:""; position:absolute; left:4px; top:0.55em;
  width:11px; height:11px; border-radius:50%; background:#FFE28A;
}}
.spec {{
  flex:0 0 330px; padding-left:26px; border-left:1px solid rgba(255,255,255,0.26);
  display:flex; flex-direction:column;
}}
.spec .base {{
  font-family:'Body',sans-serif; font-weight:700; font-size:35px; letter-spacing:0.5px;
  color:#FFE28A; line-height:1.26;
}}
.spec .nums {{
  display:flex; flex-direction:column; row-gap:2px;
  font-family:'Body',sans-serif; font-weight:400; font-size:32px; letter-spacing:0.5px;
  color:rgba(255,255,255,0.82); line-height:1.3;
}}
.spec .nums b {{ font-weight:400; white-space:nowrap; }}
.spec .nums i {{ display:none; }}
'''

CONTENT_HTML = f'''
  <div class="content">
    <div class="head">
      <div class="lock">
        <img src="data:image/png;base64,{matsui_logo}" alt="Matsui International"/>
        <h1>SPECIALTY <span>INKS</span></h1>
      </div>
      <div class="rule"></div>
    </div>
    <div class="grid">{panels()}</div>
  </div>'''

GUIDE_HTML = f'''
  <div class="guides">
    <div class="g-trim"></div><div class="g-safe"></div>
    <div class="g-tag g-tag-trim">TRIM 120 x 96 in</div>
    <div class="g-tag g-tag-bleed">BLEED {BLEED_IN}in — 124 x 100 in</div>
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
.g-clear {{ position:absolute; left:{BLEED}px; width:{TRIM_W}px;
  top:{BLEED+CONTENT_H}px; height:0; outline:4px dashed #7CFF6B; }}
.g-tag {{ position:absolute; font-family:'Body',sans-serif; font-weight:700;
  font-size:34px; letter-spacing:2px; padding:10px 18px; border-radius:4px; }}
.g-tag-bleed {{ top:8px; left:12px; background:#FF2D8E; color:#fff; }}
.g-tag-trim  {{ top:{BLEED+14}px; left:{BLEED+14}px; background:#00E5FF; color:#00232B; }}
.g-tag-safe  {{ top:{BLEED+SAFE+14}px; left:{BLEED+SAFE+14}px; background:#FFD400; color:#2B2200; }}
.g-tag-clear {{ top:{BLEED+CONTENT_H+16}px; left:{BLEED+14}px; background:#7CFF6B; color:#0B2400; }}
'''

body_parts = []
if LAYER in ('bg', 'all'):
    body_parts.append(BG_HTML)
if LAYER in ('fg', 'all'):
    body_parts.append(CONTENT_HTML)
    body_parts.append('<div class="unify"></div>')
if SHOW_GUIDES:
    body_parts.append(GUIDE_HTML)

page_bg = 'transparent' if LAYER == 'fg' else '#0A0A0A'

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>Matsui Specialty Inks Tradeshow Banner 10x8</title>
<meta name="hz:slide-selector" content=".banner"/>
<meta name="hz:canvas-width" content="{W}"/>
<meta name="hz:canvas-height" content="{H}"/>
<style>
{FONT_FACES}
{FG_CSS}
{BG_CSS}
{GUIDE_CSS if SHOW_GUIDES else ''}
html,body {{ background:{page_bg}; }}
.banner {{ background:{'transparent' if LAYER == 'fg' else '#07090D'}; }}
</style>
</head>
<body>
  <div class="banner" data-canvas-width="{W}" data-canvas-height="{H}">
{''.join(body_parts)}
  </div>
</body>
</html>
'''

out = f'sq_{LAYER}{"_guides" if SHOW_GUIDES else ""}.html'
with open(out, 'w') as f:
    f.write(HTML)
print('wrote', out, len(HTML))
