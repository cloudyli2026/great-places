"""Render the three case footprints at one metric scale; pyproj required.
SVG originals: 300 mm wide, 600 m square map at 1:2500. Web uses graphic scale.
"""
import json,pathlib,hashlib
from xml.sax.saxutils import escape
from pyproj import CRS,Transformer
from shapely.geometry import Polygon,box
from shapely import make_valid,union_all
ROOT=pathlib.Path(__file__).resolve().parents[1];DATA=ROOT/'docs/data'
CASES=[('01','san-marco',45.4342,12.3387),('03','siena',43.31865,11.33165),('04','federation',-37.8178,144.969)]
SPAN=600;FRAME=800;PPM=FRAME/SPAN

def build():
 records=[]
 for number,slug,lat,lon in CASES:
  file=DATA/(slug+'-comparison-buildings.geojson') if slug!='federation' else DATA/'federation-buildings.json'
  raw=json.loads(file.read_text());features=raw['features']
  crs=CRS.from_proj4(f'+proj=aeqd +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=m +no_defs');t=Transformer.from_crs('EPSG:4326',crs,always_xy=True)
  paths=[];polygons=holes=0;shapes=[]
  for f in features:
   if f.get('properties',{}).get('is_underground') is True:continue
   g=f['geometry'];ps=[g['coordinates']] if g['type']=='Polygon' else g['coordinates'] if g['type']=='MultiPolygon' else []
   for poly in ps:
    projected=[[t.transform(*p[:2]) for p in ring] for ring in poly]
    flat=[p for ring in projected for p in ring]
    if not flat or max(p[0] for p in flat)<-SPAN/2 or min(p[0] for p in flat)>SPAN/2 or max(p[1] for p in flat)<-SPAN/2 or min(p[1] for p in flat)>SPAN/2:continue
    shapes.append(make_valid(Polygon(projected[0],projected[1:])))
    d=' '.join(' '.join(('M' if i==0 else 'L')+f'{100+(x+SPAN/2)*PPM:.3f},{80+(SPAN/2-y)*PPM:.3f}' for i,(x,y) in enumerate(ring))+'Z' for ring in projected)
    paths.append('<path d="'+d+'"/>');polygons+=1;holes+=len(poly)-1
  built=union_all(shapes).intersection(box(-300,-300,300,300)).area
  source='Overture Maps 2026-10-21 / TerraLab / ODbL 1.0' if slug!='federation' else 'City of Melbourne 2020 / tier 1 Structure / CC BY 4.0'
  name={'san-marco':'PIAZZA SAN MARCO','siena':'PIAZZA DEL CAMPO','federation':'FEDERATION SQUARE'}[slug]
  svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="300mm" height="300mm" viewBox="0 0 1000 1000" role="img" aria-labelledby="title desc" data-span-m="600" data-px-per-m="{PPM}" data-native-scale="2500"><title id="title">{number} {name} · 600 × 600 m</title><desc id="desc">North up. Identical 600 metre square and 100 metre bar for all three cases. Source: {escape(source)}. Black buildings, white unclassified space including water; not a walking map.</desc><defs><clipPath id="map"><rect x="100" y="80" width="800" height="800"/></clipPath></defs><rect width="1000" height="1000" fill="#fff"/><g fill="#282722" fill-rule="evenodd" clip-path="url(#map)">{''.join(paths)}</g><rect x="100" y="80" width="800" height="800" fill="none" stroke="#ddd6cb"/><g font-family="Arial,sans-serif" fill="#282722"><text x="100" y="39" font-size="19">{number} / {name}</text><text x="900" y="39" text-anchor="end" font-size="16">N ↑</text><text x="100" y="915" font-size="14">600 × 600 m · native SVG 1:2500 at 300 mm width</text><g id="graphic-scale" data-length-m="100"><path d="M100 944h{100*PPM:.6f}" stroke="#282722" stroke-width="5"/><path d="M100 937v14M{100+50*PPM:.6f} 937v14M{100+100*PPM:.6f} 937v14" stroke="#282722" stroke-width="2"/><text x="100" y="968" font-size="13">0</text><text x="{100+50*PPM}" y="968" text-anchor="middle" font-size="13">50</text><text x="{100+100*PPM}" y="968" text-anchor="middle" font-size="13">100 m</text></g><text x="310" y="953" font-size="12">{escape(source)}</text></g><circle cx="500" cy="480" r="9" stroke="#a34f38" stroke-width="2" fill="none"/></svg>'''
  output=slug+'-figure-ground-600m.svg';(DATA/output).write_text(svg+'\n')
  records.append(dict(case=number,slug=slug,center=[lon,lat],span_m=SPAN,frame_svg_units=FRAME,px_per_m=PPM,scale_bar_m=100,scale_bar_svg_units=100*PPM,native_width_mm=300,native_scale=2500,projection=crs.to_wkt(),built_area_in_frame_m2=round(built,3),built_coverage_percent=round(100*built/(SPAN*SPAN),2),source=source,source_file=file.name,source_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),polygons_in_frame=polygons,holes=holes,svg=output))
 (DATA/'comparison-figures.json').write_text(json.dumps({'note':'Identical metric drawing scale, not identical source epochs or guaranteed footprint semantics. White includes water and other non-building surfaces. Not for surveying or navigation.','figures':records},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps([{'case':r['case'],'polygons':r['polygons_in_frame'],'span_m':r['span_m'],'bar_svg_units':r['scale_bar_svg_units']} for r in records]))
if __name__=='__main__':build()
