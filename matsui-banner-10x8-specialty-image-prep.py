"""Crop each sample to the panel aspect without amputating the print.

A plain centre crop cut "MATSUI COLOR" down to "MATSU / COLO" -- on a banner
that reads as a mistake. So the printed design is located first and the crop is
built around it.

Where the crop runs past the edge of the photo, the frame is extended rather
than cutting into the print, and how it is extended is decided per side:

  * mirroring the fabric outwards keeps the weave and knit texture running, and
    disappears -- but only while it reflects plain cloth. Reflect further than
    the plain margin and the design folds back on itself, which showed up as a
    duplicated mandala petal on the Eco panel.
  * so a side with less plain cloth than it needs is filled flat with the
    garment's own colour instead. On the dark, even grounds where that happens
    the fill is invisible; a heather grey would show it, which is exactly the
    case mirroring covers.
"""
import numpy as np
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

ASPECT = 4 / 3
OUT = (1800, 1350)
MARGINS = (0.07, 0.05, 0.035, 0.02, 0.0)

# An all-over print has no discrete mark to protect, but it still has a
# subject. The Mona Lisa sample is centred on her face rather than on the
# middle of the garment, which had cropped through her forehead.
CENTER = {'vintage': (0.5, 0.20)}

PICKS = {
    'vintage':     'src/Vintage_Clear-White_02.JPG',
    'pearlescent': 'src/Pearlescent_Shimmer_04.JPG',
    'g600':        'src/Top_G600_05.JPG',
    'velvet':      'src/Velvet_Puff_01.JPG',
    'threed':      'src/3D_White_05.JPG',
    'eco':         'src/Eco_Discharge_Base_DNFM-White_DNFW_02.JPG',
}


def design_box(im):
    """Bounding box of the print (generous), and the garment colour behind it."""
    a = np.asarray(im.resize((im.width // 6, im.height // 6))).astype(float)
    H, W = a.shape[:2]
    corners = np.concatenate([a[:H//8, :W//8].reshape(-1, 3), a[:H//8, -W//8:].reshape(-1, 3),
                              a[-H//8:, :W//8].reshape(-1, 3), a[-H//8:, -W//8:].reshape(-1, 3)])
    garment = np.median(corners, axis=0)
    d = np.linalg.norm(a - garment, axis=2)
    m = d > max(55, np.percentile(d, 75))
    # Keep only rows/columns carrying a real run of design pixels, then take the
    # true extent. Percentiles clipped the mandala's outer ring; a 1% run let
    # folds and shadows count as design and swallowed the whole frame. 4% of the
    # span separates all six samples cleanly.
    colhit = m.sum(axis=0) > H * 0.04
    rowhit = m.sum(axis=1) > W * 0.04
    xs, ys = np.nonzero(colhit)[0], np.nonzero(rowhit)[0]
    return (xs.min()/W, ys.min()/H, xs.max()/W, ys.max()/H), tuple(int(v) for v in garment)


def crop_for(m, x0, y0, x1, y1, W, H):
    bx0, by0, bx1, by1 = (x0-m)*W, (y0-m)*H, (x1+m)*W, (y1+m)*H
    cw, ch = bx1-bx0, by1-by0
    if cw/ch < ASPECT:
        cw = ch*ASPECT
    else:
        ch = cw/ASPECT
    cx, cy = (bx0+bx1)/2, (by0+by1)/2
    return round(cx-cw/2), round(cy-ch/2), round(cx+cw/2), round(cy+ch/2)


for key, path in PICKS.items():
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    W, H = im.size
    (x0, y0, x1, y1), garment = design_box(im)

    if (x1-x0) > 0.90 and (y1-y0) > 0.90:          # all-over print, nothing to lose
        c = CENTER.get(key, (0.5, 0.5))
        ImageOps.fit(im, OUT, Image.LANCZOS, centering=c) \
                .save(f'{key}.jpg', quality=92, optimize=True)
        print(f'{key:12s} all-over print -> filled, centring {c}')
        continue

    # plain cloth available beyond the design, per side
    room = {'l': x0*W, 'r': (1-x1)*W, 't': y0*H, 'b': (1-y1)*H}
    for m in MARGINS:
        left, top, right, bottom = crop_for(m, x0, y0, x1, y1, W, H)
        need = {'l': max(0, -left), 'r': max(0, right-W),
                't': max(0, -top), 'b': max(0, bottom-H)}
        if all(need[s] <= room[s] for s in need):
            break

    region = np.asarray(im.crop((max(0, left), max(0, top), min(W, right), min(H, bottom))))
    notes = []
    for side, axis, before in (('t', 0, True), ('b', 0, False), ('l', 1, True), ('r', 1, False)):
        n = int(need[side])
        if not n:
            continue
        pads = [(0, 0)] * 3
        pads[axis] = (n, 0) if before else (0, n)
        if n <= room[side]:
            region = np.pad(region, pads, mode='symmetric')
            notes.append(f'{side}:mirror {n}px')
        else:
            region = np.pad(region, pads, mode='constant',
                            constant_values=0)      # per-channel fill below
            sl = [slice(None)] * 3
            sl[axis] = slice(0, n) if before else slice(region.shape[axis]-n, None)
            region[tuple(sl)] = np.array(garment, dtype=region.dtype)
            notes.append(f'{side}:fill {n}px')

    Image.fromarray(region).resize(OUT, Image.LANCZOS) \
         .save(f'{key}.jpg', quality=92, optimize=True)
    print(f'{key:12s} design {x0:.2f}-{x1:.2f} x {y0:.2f}-{y1:.2f}  margin {m:.3f}  '
          + ('; '.join(notes) if notes else 'no padding'))
