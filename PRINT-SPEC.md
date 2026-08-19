# Matsui DTF Tradeshow Banner — Print Specification

## Finished size

| | inches | feet |
|---|---|---|
| **Trim (finished)** | 240 × 120 | 20 × 10 |
| **With bleed** | 244 × 124 | — |
| **Bleed** | 2 in all sides | — |
| **Safe margin** | 4 in inside trim | — |

No printer spec was supplied, so these are standard vinyl-banner values:
2 in bleed clears the hem, and the 4 in safe margin keeps all type off the
hem and grommet line. **If your printer specifies different values, send them
and the files can be rebuilt — the bleed and safe margin are parameters in
`matsui-banner-20x10-build.py`, not baked into the artwork.**

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
