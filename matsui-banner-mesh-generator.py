"""Continuous mesh gradient for the banner background.

Earlier versions stacked separate blurred blobs at differing opacities, which
reads as blotchy: every overlap is a visible lump and every blob edge is a
seam, no matter how much blur is applied.

This instead solves one smooth colour field. Control points are placed across
the canvas and every pixel is a normalised inverse-distance blend of all of
them, so the result is continuous by construction -- there are no shapes, no
edges and nothing to overlap. Computed small and resampled up, which
guarantees smoothness, then dithered to keep large-format print from banding.
"""
import numpy as np
from PIL import Image, ImageFilter

W, H = 6100, 3100
CALC_W, CALC_H = 260, 132       # solved small; upsampling is what makes it smooth


def hexrgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float)


# (x, y, colour) in normalised canvas space. Deep and cool at the top where
# the headlines sit, warming and brightening down and to the right, following
# the blue -> violet -> pink -> orange progression of the reference.
POINTS = [
    (0.00, 0.00, '#0B0A22'), (0.30, 0.00, '#141038'), (0.62, 0.00, '#171043'),
    (0.86, 0.00, '#1B1147'), (1.00, 0.06, '#241456'),

    (0.00, 0.34, '#2C3A9E'), (0.16, 0.52, '#4E63D8'), (0.03, 0.78, '#5E5BD6'),
    (0.22, 0.95, '#7B5CD6'), (0.38, 0.66, '#7A5AD8'),

    (0.44, 0.30, '#3B3A96'), (0.52, 0.86, '#B06FD0'), (0.62, 0.52, '#9A5FD8'),
    (0.70, 0.95, '#E0609F'), (0.74, 0.28, '#4A3C9E'),

    (0.84, 0.60, '#E86FA0'), (0.92, 0.92, '#FF8A5C'), (1.00, 0.44, '#C86FB8'),
    (1.00, 0.74, '#FF9A6A'), (0.96, 0.16, '#3E2E86'),
]

POWER = 2.15          # falloff sharpness: higher starts showing cells around points


def solve():
    px = np.array([p[0] for p in POINTS])
    py = np.array([p[1] for p in POINTS])
    cols = np.array([hexrgb(p[2]) for p in POINTS])

    gx, gy = np.meshgrid(np.linspace(0, 1, CALC_W), np.linspace(0, 1, CALC_H))
    # aspect-correct the distance metric or the field stretches horizontally
    ar = W / H
    dx = (gx[..., None] - px) * ar
    dy = gy[..., None] - py
    d2 = dx*dx + dy*dy + 1e-6

    w = 1.0 / np.power(d2, POWER / 2.0)
    w /= w.sum(axis=-1, keepdims=True)
    field = np.einsum('hwp,pc->hwc', w, cols)
    return np.clip(field, 0, 255)


def build():
    small = solve()
    im = Image.fromarray(small.astype(np.uint8), 'RGB')
    # Inverse-distance weighting leaves a faint halo around each control
    # point. Blurring at solve resolution erases that local structure while
    # leaving the large-scale colour flow untouched.
    im = im.filter(ImageFilter.GaussianBlur(radius=7))
    # bicubic up from a small solve leaves no structure to read as blotches
    im = im.resize((W // 2, H // 2), Image.BICUBIC).resize((W, H), Image.BICUBIC)

    # A smooth gradient this large will band on press. A little noise below
    # the visible threshold breaks the steps up.
    a = np.asarray(im).astype(np.float32)
    rng = np.random.default_rng(7)
    a += rng.normal(0.0, 1.7, a.shape)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB')


if __name__ == '__main__':
    build().save('mesh.png')
    print('mesh.png', W, 'x', H, '-', len(POINTS), 'control points, power', POWER)
