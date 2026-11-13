"""Independent integrity checks for the frozen official footprint subset (stdlib)."""
import json,math,pathlib,subprocess,hashlib,xml.etree.ElementTree as ET
root=pathlib.Path(__file__).resolve().parents[1]
p=root/'docs/data/federation-buildings.json';d=json.loads(p.read_text());svg=root/'docs/data/federation-figure-ground.svg'
assert len(d['features'])==907
assert d['records_returned']==1001
assert d['bbox']==[144.9605,-37.8245,144.9782,-37.8115]
polygons=holes=vertices=0
for f in d['features']:
 assert f['properties']['tier']==1 and f['properties']['footprint_type']=='Structure'
 g=f['geometry'];assert g['type'] in ['Polygon','MultiPolygon']
 for poly in ([g['coordinates']] if g['type']=='Polygon' else g['coordinates']):
  polygons+=1;holes+=len(poly)-1
  for ring in poly:
   assert ring[0]==ring[-1] and len(ring)>=4
   for lon,lat,*_ in ring:
    assert 144<lon<146 and -39<lat<-37 and math.isfinite(lon+lat)
    vertices+=1
before=svg.read_bytes();subprocess.run(['python',str(root/'scripts/update_federation_gis.py'),'--offline'],check=True)
assert svg.read_bytes()==before,'Non-deterministic offline rebuild'
s=ET.fromstring(before);ns={'s':'http://www.w3.org/2000/svg'}
paths=s.findall('.//s:g[@fill-rule="evenodd"]/s:path',ns);assert len(paths)==polygons
assert s.find('.//s:clipPath',ns) is not None
# Independently check the graphic bar against the frame aspect and 100 m.
R=6371008.8;w,so,e,n=d['bbox'];span_x=R*math.radians(e-w)*math.cos(math.radians((so+n)/2));span_y=R*math.radians(n-so)
scale=min(900/span_x,600/span_y)
bar=s.find('.//s:path[@stroke-width="5"]',ns).attrib['d'];assert abs(float(bar.split('h')[1])-100*scale)<.001
print(json.dumps(dict(features=len(d['features']),polygons=polygons,holes=holes,vertices=vertices,deterministic_rebuild=True,bar_100m_px=round(scale*100,3),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest())))
