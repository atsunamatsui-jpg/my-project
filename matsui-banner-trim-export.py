"""Cut the bleed off the composite and write a trim-only EPS.

The main deliverable carries 2in of bleed all round, so the *sheet* is 244x124
in -- 1.968:1, not 2:1. That is correct for print, but a 61x31 in file invites
a printer to fit it to a 20x10 ft frame and distort it.

This writes a second file at the exact finished size instead: bleed removed, so
the artwork is precisely 20 x 10 ft (2.000000:1) with nothing to trim.
"""
import os

from PIL import Image

from make_eps import write_eps

Image.MAX_IMAGE_PIXELS = None

DPI = 300
QUARTER = 4                      # files are supplied at quarter scale
BLEED_IN_FINAL = 2               # bleed at final size
BLEED_PX = round(BLEED_IN_FINAL / QUARTER * DPI)      # 150 px in file space
REPO = '/home/user/my-project'
STEM = 'matsui-banner-20x10'


def trim(src, out_eps):
    im = Image.open(src)
    w, h = im.size
    box = (BLEED_PX, BLEED_PX, w - BLEED_PX, h - BLEED_PX)
    cut = im.crop(box)
    tw, th = cut.size
    ratio = tw / th
    assert abs(ratio - 2.0) < 1e-9, f'trim is {ratio:.6f}:1, expected exactly 2:1'
    tmp = 'trim_tmp.png'
    cut.save(tmp, format='PNG', dpi=(DPI, DPI))
    cut.close()
    im.close()
    write_eps(tmp, out_eps, tw / DPI, th / DPI)
    os.remove(tmp)
    print(f'   trim {tw}x{th} px = {tw/DPI:.1f}x{th/DPI:.1f} in at quarter scale'
          f' -> {tw/DPI*QUARTER:.0f}x{th/DPI*QUARTER:.0f} in final'
          f' = {tw/DPI*QUARTER/12:.0f}x{th/DPI*QUARTER/12:.0f} ft, ratio {ratio:.6f}')


if __name__ == '__main__':
    trim('sheet300_all.png', f'{REPO}/{STEM}-300dpi-TRIM-no-bleed.eps')
