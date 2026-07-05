#!/usr/bin/env python3
"""Crop a 1920x1080 slide PNG into overlapping zoom regions for the vision QA pass.
The Read tool downsamples full images to ~512px wide, hiding fine SVG/text
collisions -- cropping restores the detail. Outputs 6 regions (2 rows x 3 cols,
overlapping) into crops/<name>__r{row}c{col}.png plus a full half-res overview.
Usage: python3 crop.py <slide.png>
"""
import sys, os
from PIL import Image

def main():
    png = sys.argv[1]
    im = Image.open(png).convert("RGB")
    W, H = im.size
    base = os.path.splitext(os.path.basename(png))[0]
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crops")
    os.makedirs(outdir, exist_ok=True)
    made = []
    # overview (half res) for layout gestalt
    ov = im.resize((W // 2, H // 2))
    ovp = os.path.join(outdir, base + "__overview.png"); ov.save(ovp); made.append(ovp)
    # 2 rows x 3 cols with 12% overlap, kept at full res
    cols, rows = 3, 2
    ovx, ovy = int(W * 0.06), int(H * 0.06)
    cw, ch = W // cols, H // rows
    for r in range(rows):
        for c in range(cols):
            x0 = max(0, c * cw - ovx); y0 = max(0, r * ch - ovy)
            x1 = min(W, (c + 1) * cw + ovx); y1 = min(H, (r + 1) * ch + ovy)
            crop = im.crop((x0, y0, x1, y1))
            p = os.path.join(outdir, f"{base}__r{r}c{c}.png"); crop.save(p); made.append(p)
    for p in made:
        print(p)

if __name__ == "__main__":
    main()
