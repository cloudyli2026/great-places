"""Reproduce the three published Procuratie PDF figures without redrawing geometry.
Usage: python scripts/render_published_drawings.py [--download] [--source-dir PATH]
Requires PyMuPDF and Pillow. Original rights and hashes are in the figure manifest.
"""
from pathlib import Path
import argparse,json,hashlib,urllib.request,urllib.parse
import pymupdf
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--download',action='store_true');p.add_argument('--source-dir',type=Path,default=ROOT/'work/published-drawings');args=p.parse_args();args.source_dir.mkdir(parents=True,exist_ok=True)
for item in json.loads((ROOT/'docs/drawings/san-marco-sources.json').read_text())['drawings']:
 source=args.source_dir/Path(urllib.parse.urlsplit(item['source_url']).path).name
 if args.download:
  req=urllib.request.Request(item['source_url'],headers={'User-Agent':'Mozilla/5.0 (GreatPlacesResearch)'})
  with urllib.request.urlopen(req,timeout=40) as r:source.write_bytes(r.read())
 assert hashlib.sha256(source.read_bytes()).hexdigest()==item['pdf_sha256'],'Unexpected source PDF'
 with pymupdf.open(source) as document:
  page=document[item['physical_pdf_page']-1];scale=item['render_width_px']/page.rect.width
  pix=page.get_pixmap(matrix=pymupdf.Matrix(scale,scale))
  Image.frombytes('RGB',(pix.width,pix.height),pix.samples).save(ROOT/'docs/drawings'/item['file'],'WEBP',quality=94)
 print(item['file'])
