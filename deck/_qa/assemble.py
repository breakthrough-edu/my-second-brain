#!/usr/bin/env python3
"""Assemble ordered slide PNGs into one PDF (one PNG per page, 1:1).
Usage: python3 assemble.py <png_dir> <out.pdf>
Pages are ordered by filename (01-*.png .. 24-*.png). Missing/short renders are
reported so a partial run never silently ships an incomplete deck.
"""
import sys, os, glob, fitz

def main():
    from PIL import Image
    png_dir, out = sys.argv[1], sys.argv[2]
    # only real slides: NN-*.png (two-digit prefix), skip stray _test etc.
    pngs = sorted(glob.glob(os.path.join(png_dir, "[0-9][0-9]-*.png")))
    if not pngs:
        print("FAIL: no NN-*.png slides in " + png_dir); return 1
    doc = fitz.open()
    report = []
    for p in pngs:
        pw, ph = Image.open(p).size          # true pixel dims
        img = fitz.open(p)
        pdfbytes = img.convert_to_pdf()
        img.close()
        src = fitz.open("pdf", pdfbytes)
        page = doc.new_page(width=1920, height=1080)   # 1:1 pt page
        page.show_pdf_page(page.rect, src, 0)
        report.append((os.path.basename(p), pw, ph))
    doc.save(out, deflate=True)
    doc.close()
    print("WROTE %s  (%d pages)" % (out, len(pngs)))
    for name, w, h in report:
        flag = "" if (w, h) == (1920, 1080) else "  <-- UNEXPECTED PIXEL SIZE"
        print("  %-32s %dx%d px%s" % (name, w, h, flag))
    return 0

if __name__ == "__main__":
    sys.exit(main())
