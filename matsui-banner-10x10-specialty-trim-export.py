"""Cut the bleed off the composite and write a trim-only EPS + PNG.

The main deliverable carries 2in of bleed all round, so the sheet is 124x124 in
-- still 1:1 here, but 31x31 in on the supplied file rather than the 30x30 in
that corresponds to the finished 10x10 ft. Removing the bleed gives a file at
exactly the finished size, so there is nothing for a printer to misread.
"""
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'banner'))
from make_eps import write_eps

Image.MAX_IMAGE_PIXELS = None
DPI, QUARTER, BLEED_IN_FINAL = 300, 4, 2
BLEED_PX = round(BLEED_IN_FINAL / QUARTER * DPI)        # 150 px
REPO = '/home/user/my-project'
STEM = 'matsui-banner-10x10-specialty'

im = Image.open('sheet300_all.png')
w, h = im.size
cut = im.crop((BLEED_PX, BLEED_PX, w-BLEED_PX, h-BLEED_PX))
tw, th = cut.size
assert tw == th, f'trim is {tw}x{th}, expected square'
assert abs(tw/th - 1.0) < 1e-9, f'trim ratio {tw/th:.6f}, expected exactly 1:1'
cut.save(f'{REPO}/{STEM}-300dpi-TRIM-no-bleed.png', format='PNG', dpi=(DPI, DPI), optimize=True)
tmp = 'trim_tmp.png'; cut.save(tmp, format='PNG', dpi=(DPI, DPI))
cut.close(); im.close()
write_eps(tmp, f'{REPO}/{STEM}-300dpi-TRIM-no-bleed.eps', tw/DPI, th/DPI)
os.remove(tmp)
print(f'   trim {tw}x{th} px = {tw/DPI:.0f}x{th/DPI:.0f} in at quarter scale'
      f' -> {tw/DPI*QUARTER:.0f}x{th/DPI*QUARTER:.0f} in final'
      f' = {tw/DPI*QUARTER/12:.0f}x{th/DPI*QUARTER/12:.0f} ft, ratio {tw/th:.6f}')
