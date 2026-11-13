"""Freeze official 2020 tier-1 footprints and render a metric SVG. Python stdlib only."""
import json, math, urllib.request, urllib.parse, pathlib, hashlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/data'
BBOX = (144.9605, -37.8245, 144.9782, -37.8115)
SOURCE = 'https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/2020-building-footprints/records'
def fetch():
    w,s,e,n=BBOX
    where=f"intersects(geo_shape, geom'POLYGON(({w} {s},{e} {s},{e} {n},{w} {n},{w} {s}))') AND tier=1"
    rows=[]
    for offset in range(0,10000,100):
        url=SOURCE+'?'+urllib.parse.urlencode({'where':where,'limit':100,'offset':offset,'order_by':'structure_id, property_id'})
        with urllib.request.urlopen(url,timeout=60) as f: data=json.load(f)
        rows.extend(data['results'])
        if len(rows)>=data['total_count']: break
    assert len(rows)==data['total_count'], 'Incomplete pagination'
    features=[]
    for r in rows:
        if r['tier']!=1 or r['footprint_type']!='Structure': continue
        features.append({'type':'Feature','geometry':r['geo_shape']['geometry'],'properties':{k:v for k,v in r.items() if k not in ('geo_shape','geo_point_2d')}})
    return {'type':'FeatureCollection','source':SOURCE,'bbox':list(BBOX),'capture_date':'2020-05','retrieved':'2026-11-13','license':'CC BY 4.0','selection':'tier=1 AND footprint_type=Structure; bridges excluded','records_returned':len(rows),'features':features}
def render(data):
    # Local equirectangular metric projection; same scale on both axes.
    w,s,e,n=BBOX; lat0=math.radians((s+n)/2); R=6371008.8
    width=R*math.radians(e-w)*math.cos(lat0); height=R*math.radians(n-s)
    scale=min(900/width,600/height)
    ox=(1000-width*scale)/2; oy=65
    def xy(p):return ox+R*math.radians(p[0]-w)*math.cos(lat0)*scale,oy+R*math.radians(n-p[1])*scale
    paths=[]
    for f in data['features']:
        g=f['geometry']; polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
        for poly in polys:
            rings=[]
            for ring in poly:
                assert len(ring)>=4 and ring[0]==ring[-1]
                rings.append(' '.join(('M' if i==0 else 'L')+f'{xy(p)[0]:.3f},{xy(p)[1]:.3f}' for i,p in enumerate(ring))+'Z')
            paths.append('<path d="'+' '.join(rings)+'"/>')
    bar=100*scale; cx,cy=xy([144.969,-37.8178])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 780" role="img" aria-labelledby="title desc"><title id="title">Federation Square · official 2020 building footprints</title><desc id="desc">{len(data['features'])} ground or podium footprint records. Structures black; bridges excluded. White includes water, rail and unclassified space, not necessarily walkable public space.</desc><defs><clipPath id="frame"><rect x="{ox}" y="{oy}" width="{width*scale}" height="{height*scale}"/></clipPath></defs><rect width="1000" height="780" fill="white"/><g fill="#282722" fill-rule="evenodd" clip-path="url(#frame)">{''.join(paths)}</g><g font-family="Arial" fill="#282722"><text x="35" y="30" font-size="18">FEDERATION SQUARE · FIGURE GROUND · 2020</text><text x="950" y="30" text-anchor="end">N ↑</text><text x="35" y="735" font-size="13">City of Melbourne · CC BY 4.0 · tier 1 structures · bridges excluded</text><text x="35" y="757" font-size="12">White = unclassified non-building space (includes river and railway). Not a walkability map.</text><path d="M35 695h{bar:.3f}" stroke="#282722" stroke-width="5"/><text x="35" y="681" font-size="13">100 m · local metric projection</text></g><circle cx="{cx}" cy="{cy}" r="12" fill="none" stroke="#a34f38" stroke-width="3"/></svg>'''
if __name__=='__main__':
    import sys
    path=OUT/'federation-buildings.json'
    data=json.loads(path.read_text()) if '--offline' in sys.argv else fetch()
    OUT.mkdir(exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    (OUT/'federation-figure-ground.svg').write_text(render(data))
    print(json.dumps({'features':len(data['features']),'records_returned':data['records_returned'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
