# Matsui DTF Tradeshow Banner — Print Specification

## Finished size

| | inches | feet |
|---|---|---|
| **Trim (finished)** | 240 × 120 | 20 × 10 |
| **With bleed** | 244 × 124 | — |
| **Bleed** | 2 in all sides | — |
| **Safe margin** | 4 in inside trim | — |
| **Content band** | top 80 in | top 6 ft 8 in |
| **Clear zone** | bottom 40 in | bottom 3 ft 4 in |

No printer spec was supplied, so these are standard vinyl-banner values:
2 in bleed clears the hem, and the 4 in safe margin keeps all type off the
hem and grommet line. **If your printer specifies different values, send them
and the files can be rebuilt — the bleed and safe margin are parameters in
`matsui-banner-20x10-build.py`, not baked into the artwork.**

## Clear zone — bottom third

All artwork is held in the **top two thirds** (top 80 in). The **bottom 40 in
carries background gradient only** — no logos, machines, product shots or
type — because on a booth that band sits behind tables, below eye level and
behind foot traffic.

This is enforced, not just laid out: the content box is clipped at the 80 in
line, so the artwork layer contains **zero** pixels below it, drop-shadow
tails included. The background gradient still runs the full height and full
bleed, so the banner reads as one piece.

The gradient was re-tuned for this: the blue → violet → pink → orange
progression is compressed into the content band so the luminous part of the
field sits behind the artwork, and the lower third resolves into deeper
indigo and plum. It holds the same saturation as the rest of the sheet
(0.56) at about 76% of the value, so it stays coloured ink rather than
turning into a dark margin.

The proof (`...-PROOF-guides.png`) marks the line in green.

The split is a constant — `CONTENT_H` in the build script. If the booth
setup changes and you want content lower, change that one value and rebuild.

## Column spacing

The three columns are sized to hug their own widest element and are separated
by a single constant, `COL_GAP` (240 px = 9.6 in), with the group centred.
Earlier the columns split the full width as percentages, which left 17–19 in
between blocks; the gap is now a number you can set rather than a leftover.

Because the machine photos are limited by the height of the content band, not
by width, their image boxes were heavily letterboxed — so the columns could
be brought in **without any artwork getting smaller**. Lockups, machines and
consumable cards are all identical in size to the previous version.

Outer margins land at about 13 in a side. Gaps and margins trade against each
other one-for-one: the artwork totals about 194 in of the 240 in width, so
tightening the gaps further widens the margins by the same amount.

## Files

Artwork is supplied at **quarter scale, 300 DPI** — a 61 × 31 in sheet.
**Print at 400%.** The files report 300 DPI in their metadata.

| File | Use |
|---|---|
| `matsui-banner-20x10-300dpi.eps` | **Send this to the printer.** Composite, with bleed. |
| `...-300dpi-BACKGROUND.eps` | Background layer only. |
| `...-300dpi-ARTWORK.eps` | Content layer only (ground baked in — EPS cannot hold alpha). |
| `...-300dpi-artwork.png` | Content layer on **true transparency** — use this one to drop the artwork over a different background. |
| `matsui-banner-20x10-PROOF-guides.png` | Proof only. Shows bleed / trim / safe lines. **Do not print.** |
| `matsui-banner-20x10.html` | Editable source. |
| `matsui-banner-20x10-build.py` | Build script — regenerates every file above. |

## Resolution — read before ordering

The sheet is 300 DPI **at quarter scale**, which is **75 DPI at the finished
20 × 10 ft size**. That is normal and correct for a banner viewed from several
feet, and it is the honest ceiling here for a specific reason:

- the MM4/MM2 machine cutouts are ~2600 px and span ~7 ft on the banner → **~31 DPI at final size**
- the consumable product shots come out of a 3840 px reference → **~56 DPI at final size**

Rendering a larger canvas would upscale those photos, not sharpen them. True
300 DPI at full size would be 72,000 × 36,000 px (2.6 gigapixels, ~7.8 GB) and
would still carry the same underlying photo detail.

**To genuinely increase sharpness, supply higher-resolution source art:**
original machine renders and original product photography. The layout will
take them without changes.

## Known gaps

- **MM2 lockup carries a generated white keyline.** The supplied MM4 art has
  a white keyline baked in and holds on the dark ground; the supplied MM2 art
  is black with no keyline and was effectively invisible there. A matching
  keyline was generated so the pair reads as one system. **If Matsui has an
  official reversed / knockout MM2 for dark backgrounds, use it instead** —
  drop it in as `mm2_logo.png` and rebuild.
- **"Shishine gloss"** in the G600 copy looks like a typo; left as supplied.

## Regenerating

`matsui-banner-20x10-build.py` rebuilds every output. It takes a layer mode
(`bg`, `fg`, `all`) and an optional `--guides` flag for the proof. Bleed and
safe margin are constants at the top of the file.

Full-size PNG copies of the composite and background layers are **not**
committed -- each is ~95 MB and duplicates its EPS counterpart. Rebuild them
from the script if a printer asks for PNG rather than EPS. The artwork PNG
*is* committed, because it is the only file carrying real transparency.
