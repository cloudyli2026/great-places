"""Render the two documented figure excerpts, preserving geometry and original scale bars.
Usage: python scripts/render_siena_drawings.py /path/to/original-thesis.pdf
Requires PyMuPDF and Pillow. Obtain the original via docs/drawings/sources.json.
"""
from pathlib import Path
import sys,json,hashlib
import pymupdf
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/drawings'
metadata=json.loads((OUT/'sources.json').read_text());source=Path(sys.argv[1])
if metadata.get('pdf_sha256'):assert hashlib.sha256(source.read_bytes()).hexdigest()==metadata['pdf_sha256'],'Unexpected source PDF'
with pymupdf.open(source) as document:
 for item in metadata['figures']:
  page=document[item['physical_pdf_spread']-1]
  pix=page.get_pixmap(matrix=pymupdf.Matrix(2.4,2.4),clip=pymupdf.Rect(*item['clip_pdf_points']))
  Image.frombytes('RGB',(pix.width,pix.height),pix.samples).save(OUT/item['file'],'WEBP',quality=94)
  print(item['file'],pix.width,pix.height)
