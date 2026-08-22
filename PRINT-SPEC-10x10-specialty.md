# Matsui Specialty Inks Banner (10 × 10 ft) — Print Specification

Companion piece to the 20 × 10 DTF banner. Same palette, same mesh background,
same bleed and safe-margin conventions, same 2.5 ft clear strip at the foot.

## Aspect ratio

The finished banner is **10 × 10 ft — exactly 1.000000 : 1**.

The main file measures **31 × 31 in**. That is square too, but it is *not* the
finished proportion in inches — it carries 2 in of bleed all round:

```
31 × 31 in  (file, quarter scale)
  × 400%      → 124 × 124 in
  − 2 in bleed each edge → 120 × 120 in = 10 × 10 ft
```

**Print at 400%.** Do not let a printer scale 31 × 31 to fit a 10 × 10 frame —
that throws away the bleed. Two files are supplied so it cannot be ambiguous:

| If the printer wants… | Send |
|---|---|
| artwork **with bleed** (most vinyl shops, for the hem) | `...-300dpi.eps` — 31 × 31 in |
| artwork at **exact finished size** | `...-300dpi-TRIM-no-bleed.eps` — 30 × 30 in |

`matsui-banner-10x10-specialty-trim-export.py` builds the trim file and
**asserts** the 1:1 ratio, so a build that drifted off square fails rather than
shipping quietly.

## Finished size

| | inches | feet |
|---|---|---|
| **Trim (finished)** | 120 × 120 | 10 × 10 |
| **With bleed** | 124 × 124 | — |
| **Bleed** | 2 in all sides | — |
| **Safe margin** | 4 in inside trim | — |
| **Content band** | top 90 in | top 7 ft 6 in |
| **Clear zone** | bottom 30 in | bottom 2 ft 6 in |

## Clear zone

All artwork sits in the **top 90 in**; the **bottom 30 in carries background
gradient only**. Enforced by clipping the content box, so the artwork layer
holds **zero** pixels below the line, drop-shadow tails included. Measured on
the full-resolution artwork layer, ink spans x 150–2948 px against a
150–2950 px safe box.

`CLEAR_IN` in the build script is the single constant controlling this.

## Files

Artwork is supplied at **quarter scale, 300 DPI** — a 31 × 31 in sheet.

| File | Use |
|---|---|
| `...-300dpi.eps` | **Send this to the printer.** Composite, with bleed. |
| `...-300dpi-TRIM-no-bleed.eps` | Composite at exact finished size, 30 × 30 in. |
| `...-300dpi.png` | Same composite as PNG, 9300 × 9300 px (82 MB). |
| `...-300dpi-TRIM-no-bleed.png` | Trim composite as PNG, 9000 × 9000 px. |
| `...-300dpi-BACKGROUND.eps` | Background layer only — swap the ground. |
| `...-300dpi-ARTWORK.eps` | Content layer (ground baked in — EPS has no alpha). |
| `...-300dpi-artwork.png` | Content layer on **true transparency**. |
| `...-PROOF-guides.png` | Proof. Shows bleed / trim / safe / clear-zone lines. **Do not print.** |
| `matsui-banner-10x10-specialty.html` | Editable source. |
| `...-build.py` | Rebuilds every output. |
| `...-prep-images.py` | Crops the garment photos (see below). |
| `...-mesh-generator.py` | Regenerates the background gradient. |

## Header lockup

"MATSUI" and "SPECIALTY INKS" are matched in cap height and sit on one
baseline. That is derived, not eyeballed: "MATSUI" is a single line *inside*
the logo file, so the build solves for the logo's overall height from three
measured ratios (`MATSUI_CAP_FRAC`, `MATSUI_TOP_FRAC`, `CAP_RATIO`). Measured
on the rendered pixels, the two baselines land **0 px** apart.

Change the headline size and the logo follows automatically.

## Image prep — why the crops are not centred

A plain centre crop cut "MATSUI COLOR" down to "MATSU / COLO". The prep script
now locates each printed design first and builds the crop around it:

- **All-over prints** (the Mona Lisa, the floral) have no discrete mark to
  lose, so they are cropped to fill — but on a focal point, not the middle of
  the garment. The Mona Lisa is centred on her face.
- **Discrete designs** are guaranteed to survive whole. Where the crop runs
  past the photo edge, the frame is extended rather than cutting the print:
  mirroring the fabric carries the knit texture on and disappears, but only
  while it reflects plain cloth — reflecting further folded the Eco mandala
  back on itself and duplicated a petal. A side without enough plain cloth is
  filled with the garment's own colour instead, which is invisible on the dark
  even grounds where that happens.

## Resolution

300 DPI at quarter scale = **75 DPI at the finished 10 × 10 ft size**, matching
the wide banner. The garment photographs are 10–18 MP originals, which at panel
size work out to **130–260 DPI at final size** — comfortably beyond the sheet,
so the samples are not the limiting factor here.

## Source images

Nine photographs were supplied; six are used, one per product. Unused
alternates, easy to swap in `...-prep-images.py`:

- **Pearlescent** — metallic "TRA" close-up, and multi-colour "I'M TRAINING"
  (the floral on denim is in use)
- **3D White** — dark teal on a white tee (teal on charcoal is in use)

Three panels show the same MATSUI COLOR artwork, because that is the only
sample supplied for G600, Velvet and 3D. It reads as a deliberate comparison:
one design in gloss black, coral puff and raised teal.

## Copy

Set as supplied, with trailing full stops levelled across the description lines
so each set of three reads consistently. **One substantive change:** the 3D
spec base is set as **"PU High Density"**; the supplied copy read "PU High
Deccity", which appears to be a typo given the line above it says "Waterbase
Highdensity". Revert it in `PRODUCTS` if it is correct as supplied.
