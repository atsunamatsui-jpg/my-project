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
    'sunset': ('#4E63D8', '#E0609F', '#FF8A3C'),
    'ember':  ('#7B5CD6', '#F0568F', '#FF9A4A'),
    'orchid': ('#5A6FD8', '#B06FD0', '#F07AA8'),
    'coral':  ('#E0609F', '#FF7A5C', '#FFB877'),
    'violet': ('#3F4FC8', '#8B5FE0', '#D678C8'),
    'blush':  ('#9A6FE0', '#E39CC8', '#FFC7A8'),
    'flame':  ('#8B5FE0', '#F0568F', '#FFA455'),
    'azure':  ('#3A4AC0', '#6B7FE0', '#C489D8'),
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
    # left zone -- MM4
    (-280, 1500, 1180,  760, 'azure',   22, 0.96, 120, 101),
    ( 780, 2350, 1020,  680, 'violet', 198, 0.92, 150, 102),
    ( 180, 2950,  980,  560, 'orchid',  -8, 0.90, 140, 103),
    (1560, 1150,  820,  540, 'ember',   66, 0.80, 155, 104),
    # middle zone -- MM2
    (2560, 2100, 1150,  760, 'ember',   16, 0.94, 155, 201),
    (3320, 1250,  980,  620, 'violet', 148, 0.86, 145, 202),
    (2980, 3000, 1050,  600, 'orchid', -18, 0.88, 160, 203),
    (3980, 2350,  920,  660, 'flame',   96, 0.84, 170, 204),
    # right zone -- consumables
    (5320, 1950, 1080,  700, 'sunset',  34, 0.94, 150, 301),
    (6080, 1150,  820,  560, 'violet', 198, 0.80, 160, 305),
    (5720, 2900, 1020,  640, 'coral',  188, 0.90, 155, 302),
    (4820, 3020,  900,  560, 'blush',    8, 0.84, 165, 303),
    (6350, 2600,  760,  620, 'ember',   58, 0.82, 160, 304),
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
            f'<rect width="{W}" height="{H}" fill="#08060F"/>'
            f'{"".join(body)}</svg>')


if __name__ == '__main__':
    svg = build()
    with open('mesh.svg', 'w') as f:
        f.write(svg)
    print('mesh.svg', len(svg), 'chars,', len(BLOBS), 'blobs')
