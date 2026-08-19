"""Iridescent liquid-gradient background, in the idiom of the supplied
inspiration: vivid multi-hue blobs floating on a deep indigo ground.

Each blob is an organic closed curve filled with a 3-stop gradient, so colour
shifts *within* the shape rather than being a flat glow. Deterministic.
"""
import math
import random

W, H = 6100, 3100

# Palette read off the inspiration: aqua/mint on the left, violet/magenta
# through the middle, warm coral at the right, all on deep indigo.
GRADS = {
    'aqua':    ('#22D3EE', '#5EEAD4', '#A3E635'),
    'teal':    ('#0EA5E9', '#22D3EE', '#67E8F9'),
    'blue':    ('#2563EB', '#6366F1', '#22D3EE'),
    'violet':  ('#7C3AED', '#A855F7', '#38BDF8'),
    'magenta': ('#DB2777', '#C026D3', '#7C3AED'),
    'pink':    ('#F472B6', '#E879F9', '#818CF8'),
    'coral':   ('#FB7185', '#FB923C', '#FBBF24'),
    'amber':   ('#F59E0B', '#FB923C', '#F472B6'),
}


def blob_path(cx, cy, rx, ry, seed, points=9, jitter=0.30):
    """A smooth organic closed curve -- liquid, not circular."""
    r = random.Random(seed)
    pts = []
    for i in range(points):
        a = 2 * math.pi * i / points
        fx = 1 - jitter + r.random() * jitter * 2
        fy = 1 - jitter + r.random() * jitter * 2
        pts.append((cx + math.cos(a) * rx * fx, cy + math.sin(a) * ry * fy))
    # close the ring with quadratics hung off the midpoints -> no corners
    d = [f'M{(pts[-1][0]+pts[0][0])/2:.1f},{(pts[-1][1]+pts[0][1])/2:.1f}']
    for i in range(len(pts)):
        cur, nxt = pts[i], pts[(i + 1) % len(pts)]
        mid = ((cur[0] + nxt[0]) / 2, (cur[1] + nxt[1]) / 2)
        d.append(f'Q{cur[0]:.1f},{cur[1]:.1f} {mid[0]:.1f},{mid[1]:.1f}')
    d.append('Z')
    return ''.join(d)


# (cx, cy, rx, ry, palette, angle, opacity, blur, seed)
BLOBS = [
    # left zone -- MM4, cool
    (-150,  400, 1250,  820, 'teal',    25, 0.55,  90, 101),
    ( 620, 1250, 1000,  760, 'aqua',   200, 0.42, 175, 102),
    ( 250, 2850, 1150,  700, 'blue',    -8, 0.46, 148, 103),
    (1500,  250,  760,  520, 'aqua',    70, 0.32, 162, 104),
    # middle zone -- MM2, hot
    (2450, 1500, 1150,  900, 'violet',  15, 0.49, 162, 201),
    (3150,  350, 1000,  680, 'magenta',150, 0.49, 135, 202),
    (2850, 2900, 1050,  660, 'pink',   -20, 0.41, 162, 203),
    (3750, 1750,  880,  700, 'violet', 100, 0.36, 189, 204),
    # right zone -- consumables, warm
    (5250,  450, 1000,  700, 'coral',   35, 0.48, 135, 301),
    (5650, 1900,  950,  780, 'amber',  190, 0.39, 162, 302),
    (4750, 2850,  900,  600, 'magenta', 10, 0.35, 175, 303),
    (6150, 1150,  700,  620, 'pink',    60, 0.32, 162, 304),
]


def build():
    defs, body = [], []
    for i, (cx, cy, rx, ry, pal, ang, op, blur, seed) in enumerate(BLOBS):
        c1, c2, c3 = GRADS[pal]
        gid = f'g{i}'
        rad = math.radians(ang)
        x1, y1 = 50 - math.cos(rad) * 50, 50 - math.sin(rad) * 50
        x2, y2 = 50 + math.cos(rad) * 50, 50 + math.sin(rad) * 50
        defs.append(
            f'<linearGradient id="{gid}" x1="{x1:.1f}%" y1="{y1:.1f}%" '
            f'x2="{x2:.1f}%" y2="{y2:.1f}%">'
            f'<stop offset="0%" stop-color="{c1}"/>'
            f'<stop offset="52%" stop-color="{c2}"/>'
            f'<stop offset="100%" stop-color="{c3}"/></linearGradient>')
        defs.append(
            f'<filter id="f{i}" x="-40%" y="-40%" width="180%" height="180%">'
            f'<feGaussianBlur stdDeviation="{blur}"/></filter>')
        body.append(
            f'<path d="{blob_path(cx, cy, rx, ry, seed)}" fill="url(#{gid})" '
            f'opacity="{op}" filter="url(#f{i})"/>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">'
            f'<defs>{"".join(defs)}</defs>'
            f'<rect width="{W}" height="{H}" fill="#0A0E2A"/>'
            f'{"".join(body)}</svg>')


if __name__ == '__main__':
    svg = build()
    with open('mesh.svg', 'w') as f:
        f.write(svg)
    print('mesh.svg', len(svg), 'chars,', len(BLOBS), 'blobs')
