#!/usr/bin/env python3
"""Makes site/assets/img/beam.webp: a dithered elliptical pool of light.

White dots on black. The page uses it as an SVG mask over a solid bright-blue fill, so the only
saturated colour in an illustration reads as grain, not as a soft gradient. Dither is seeded, so
the output is repeatable. Run: python3 tools/make_stipple.py
"""
import os, random
from PIL import Image

W, H, CELL = 640, 320, 2
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site', 'assets', 'img', 'beam.webp')

random.seed(7)
im = Image.new('L', (W, H), 0)
px = im.load()
cw, ch = W // CELL, H // CELL
for j in range(ch):
    for i in range(cw):
        dx = (i + .5) / cw * 2 - 1
        dy = (j + .5) / ch * 2 - 1
        r = (dx * dx + dy * dy) ** .5
        p = max(0.0, 1 - r) ** 1.35          # density falls off toward the rim
        if random.random() < p:
            for a in range(CELL):
                for b in range(CELL):
                    px[i * CELL + a, j * CELL + b] = 255
im.save(OUT, 'WEBP', quality=60, method=6)
print(OUT, os.path.getsize(OUT), 'bytes')
