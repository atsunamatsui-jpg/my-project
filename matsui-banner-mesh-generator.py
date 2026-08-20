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
    'deep':   ('#12314F', '#1B5375', '#2A7E9B'),
    'ocean':  ('#123F63', '#1D6E8C', '#35A0B0'),
    'teal':   ('#12566E', '#1E8496', '#48B4BE'),
    'blue':   ('#1A386E', '#2B5595', '#3F82B8'),
    'indigo': ('#252B63', '#3A4A8E', '#5470B4'),
    'violet': ('#33296B', '#4F4098', '#7266BE'),
    'plum':   ('#4A2760', '#6B3A82', '#8E5C9E'),
    'slate':  ('#16263F', '#24405F', '#3A5C82'),
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
    (-150,  400, 1300,  860, 'teal',    25, 0.72,  110, 101),
    ( 620, 1250, 1050,  800, 'ocean',  200, 0.58, 190, 102),
    ( 250, 2850, 1200,  740, 'blue',    -8, 0.60, 165, 103),
    (1500,  250,  800,  560, 'deep',    70, 0.44, 175, 104),
    # middle zone -- MM2
    (2450, 1500, 1200,  940, 'indigo',  15, 0.64, 178, 201),
    (3150,  350, 1050,  720, 'violet', 150, 0.62, 150, 202),
    (2850, 2900, 1100,  700, 'plum',   -20, 0.52, 178, 203),
    (3750, 1750,  920,  740, 'indigo', 100, 0.46, 200, 204),
    # right zone -- consumables
    (5300, 1500, 1100,  760, 'plum',    35, 0.56, 165, 301),
    (5150,  280, 1200,  660, 'violet', 200, 0.44, 190, 305),
    (5750, 2350, 1020,  800, 'blue',   190, 0.52, 178, 302),
    (4750, 2850,  940,  640, 'slate',   10, 0.46, 190, 303),
    (6150, 1150,  740,  660, 'ocean',   60, 0.42, 178, 304),
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
            f'<rect width="{W}" height="{H}" fill="#0C1830"/>'
            f'{"".join(body)}</svg>')


if __name__ == '__main__':
    svg = build()
    with open('mesh.svg', 'w') as f:
        f.write(svg)
    print('mesh.svg', len(svg), 'chars,', len(BLOBS), 'blobs')
