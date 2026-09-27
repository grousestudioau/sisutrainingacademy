"""SISU black-and-white treatment. Usage: python3 bw.py in.jpg [more.jpg ...] -> ../assets/img/bw/<name>.jpg  (colour originals live in ../_archive/img/)
Highlights pushed, shadows lifted, midtone detail kept. The grit comes from local contrast (clarity), not a hard global curve.
ponytail: one setting for every photo; per-photo tuning if a shot looks wrong."""
import sys, os
from PIL import Image, ImageFilter, ImageOps

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'bw')

def curve(v, lo, hi):
    x = min(1.0, max(0.0, (v - lo) / (hi - lo)))   # levels from the photo's own range, clipping only 0.3% each end
    x = 1 - (1 - x) ** 1.35                          # lifts shadows, pushes highlights toward white
    return round(255 * x)

def pct(hist, p):
    total, acc = sum(hist), 0
    for i, n in enumerate(hist):
        acc += n
        if acc >= total * p: return i
    return 255

def treat(path, width=1800):
    im = ImageOps.grayscale(Image.open(path))
    im.thumbnail((width, width))
    h = im.histogram()
    lo, hi = pct(h, .003), max(pct(h, .997), pct(h, .003) + 64)
    im = im.point([curve(v, lo, hi) for v in range(256)])
    im = im.filter(ImageFilter.UnsharpMask(radius=40, percent=45, threshold=0))   # clarity: local contrast, the grit
    im = im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2))  # fine detail
    noise = Image.effect_noise(im.size, 18).filter(ImageFilter.GaussianBlur(0.4))
    im = Image.blend(im, noise, 0.05)                                             # fine grain
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, os.path.splitext(os.path.basename(path))[0] + '.jpg')
    im.save(out, quality=84, optimize=True, progressive=True)
    return out

def _check():
    assert curve(255, 10, 245) == 255 and curve(10, 10, 245) == 0
    assert curve(128, 0, 255) > 128                   # mids lifted, not crushed
    assert curve(40, 0, 255) > 40                     # shadows opened

if __name__ == '__main__':
    _check()
    for p in sys.argv[1:]: print(treat(p))
