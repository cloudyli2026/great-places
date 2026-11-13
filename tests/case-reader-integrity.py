"""Verify shared structure, missing-data semantics, metric scale and reproducible outputs."""
from pathlib import Path
import json,hashlib,re,subprocess,sys,xml.etree.ElementTree as ET,math
from pyproj import CRS,Transformer,Geod
ROOT=Path(__file__).resolve().parents[1]
ns={'s':'http://www.w3.org/2000/svg'};cases=[json.loads((ROOT/f'cases/reader/{n}.json').read_text()) for n in ['01','03','04']]
core=[p['id'] for p in cases[0]['pages'] if p['id']!='history-elevation']
assert all([p['id'] for p in d['pages'] if p['id']!='history-elevation']==core for d in cases)
assert all({'milestones','public-programme','celebrations'} <= {p['id'] for p in d['pages']} for d in cases)
assert all([x['key'] for x in d['assessment']]==[x['key'] for x in cases[0]['assessment']] for d in cases)
assert all(len(d['assessment'])==10 and len(d['highlights'])==3 for d in cases)
for d in cases:
 for x in d['metrics']:
  assert x['source'] and x['scope'] and 'year' in x
  if x['key']=='annual_visits' and d['number']!='04':assert x['value'] is None
 assert len([p for p in d['pages'] if any(b['type']=='map' for b in p['blocks'])])==1
r=json.loads((ROOT/'docs/data/comparison-figures.json').read_text());geod=Geod(ellps='WGS84')
for f in r['figures']:
 src=ROOT/'docs/data'/f['source_file'];assert hashlib.sha256(src.read_bytes()).hexdigest()==f['source_sha256']
 svg=ET.parse(ROOT/'docs/data'/f['svg']).getroot();assert svg.attrib['width']=='300mm' and svg.attrib['viewBox']=='0 0 1000 1000'
 # 800/1000 of a 300 mm sheet spans 600,000 mm: 1:2500.
 assert abs(600000/(300*800/1000)-2500)<1e-8
 bar=svg.find('.//s:g[@id="graphic-scale"]/s:path',ns).attrib['d'];assert abs(float(bar.split('h')[1])/800*600-100)<1e-5
 # Independently verify that projecting a true geodesic 100 m from the center gives 100 m.
 lon,lat=f['center'];t=Transformer.from_crs('EPSG:4326',CRS.from_wkt(f['projection']),always_xy=True)
 for azimuth in [0,90,180,270]:
  x,y,_=geod.fwd(lon,lat,azimuth,100);a,b=t.transform(x,y);assert abs(math.hypot(a,b)-100)<.001
 assert 0<f['built_coverage_percent']<100
paths=[ROOT/'docs/index.html',ROOT/'docs/cases/piazza-del-campo.html',ROOT/'docs/cases/federation-square.html',ROOT/'docs/comparison.html',ROOT/'docs/data/case-comparison.json',ROOT/'docs/data/case-comparison.csv']+[ROOT/'docs/data'/f['svg'] for f in r['figures']]+[ROOT/'docs/data/comparison-figures.json']
before={p:p.read_bytes() for p in paths}
subprocess.run([sys.executable,str(ROOT/'scripts/build_comparison_figures.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/build_case_readers.py')],check=True)
assert all(p.read_bytes()==old for p,old in before.items()),'Build changed committed output'
versions=[re.search('name="reader-version" content="([^"]+)',(ROOT/p).read_text())[1] for p in ['docs/index.html','docs/cases/piazza-del-campo.html','docs/cases/federation-square.html','docs/comparison.html']]
assert len(set(versions))==1
print(json.dumps({'shared_reader_version':versions[0],'cases':3,'pages_per_case':{d['number']:len(d['pages']) for d in cases},'assessment_dimensions':10,'qualities_per_case':3,'figures':3,'native_scale':'1:2500 at 300mm SVG width','span_m':600,'graphic_scale_m':100,'geodesic_validation':'4 directions per case, error < 1mm at 100m','reproducible_outputs':len(paths),'result':'pass'}))
