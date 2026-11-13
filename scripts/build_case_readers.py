"""Build all three aligned, paginated cases from one template and vocabulary."""
from pathlib import Path
from html import escape as e
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';CONTENT=ROOT/'cases/reader'
CHAPTERS=[('intro',['概况','Overview']),('scale',['尺度','Scale']),('syntax',['连接','Connectivity']),('boundary',['边界','Edges']),('life',['使用','Use']),('conclusion',['评价','Assessment']),('sources',['资料','Sources']),('factsheet',['档案','Factsheet'])]
CASES=[('01','index.html','San Marco'),('03','cases/piazza-del-campo.html','Siena'),('04','cases/federation-square.html','Federation Square')]
def bi(pair):return '<span lang="zh">'+e(str(pair[0]))+'</span><span lang="en">'+e(str(pair[1]))+'</span>'
def build_case(number):
 d=json.loads((CONTENT/(number+'.json')).read_text());prefix='' if number=='01' else '../'
 def url(u):return prefix+u[2:] if u.startswith('@/') else u
 def source_ref(s):return '<a href="'+e(url(s['url']),quote=True)+'" target="_blank" rel="noopener noreferrer">'+bi(s['label'])+'</a>'
 def figure(key):
  a=d['assets'][key];src=e(url(a['url']),quote=True);z,en=a['title'];caption=a.get('caption',a['title']);cl='drawing' if a.get('drawing') else 'photo';h=''
  if a.get('crop'):
   x,y,w,h0=a['crop'];iw,ih=a['original_size'];h=f'<svg class="crop-svg" viewBox="{x} {y} {w} {h0}" role="img" aria-label="{e(z,quote=True)}" data-alt-zh="{e(z,quote=True)}" data-alt-en="{e(en,quote=True)}"><image href="{src}" x="0" y="0" width="{iw}" height="{ih}"/></svg>'
  else:h=f'<img src="{src}" alt="{e(z,quote=True)}" data-alt-zh="{e(z,quote=True)}" data-alt-en="{e(en,quote=True)}" loading="lazy" decoding="async">'
  return f'<figure class="media {cl}"><button class="image-button" type="button" aria-label="Inspect image / 放大图像" data-image="{src}" data-alt-zh="{e(z,quote=True)}" data-alt-en="{e(en,quote=True)}" data-caption-zh="{e(caption[0],quote=True)}" data-caption-en="{e(caption[1],quote=True)}">'+h+'</button><figcaption><span class="caption-main">'+bi(caption)+'</span><details class="credit"><summary>'+bi(['图像出处','Image credit'])+'</summary><p>'+source_ref({'url':a['source'],'label':a['credit']})+'<br>'+bi(a.get('rights',['版权归原作者；按原出处核查使用范围。','Copyright retained; consult the original source for reuse.']))+'</p></details></figcaption></figure>'
 def facts():return '<dl class="facts">'+''.join('<div><dt>'+bi(row['label'])+'</dt><dd>'+bi(row['value'])+'</dd></div>' for row in d['facts'])+'</dl>'
 def render(b):
  typ=b['type']
  if typ=='p':return '<p class="prose">'+bi(b['text'])+'</p>'
  if typ=='takeaway':return '<div class="takeaway">'+bi(b['text'])+'</div>'
  if typ=='figure':return figure(b['asset'])
  if typ=='pair':return '<div class="image-pair">'+''.join(figure(x) for x in b['assets'])+'</div>'
  if typ=='hero':return '<div class="hero-layout">'+figure(b['asset'])+facts()+'</div>'
  if typ=='cards':return '<div class="reading-points">'+''.join('<article><h3>'+bi(x['title'])+'</h3><p>'+bi(x['text'])+'</p></article>' for x in b['items'])+'</div>'
  if typ=='map':
   lat,lon=d['coordinates'];google=f'https://www.google.com/maps?q={lat},{lon}&z=17&output=embed';return f'<iframe class="map-frame" src="{google}" title="{e(d["name"],quote=True)} 地理位置" data-title-zh="{e(d["name"],quote=True)} 地理位置" data-title-en="{e(d["name"],quote=True)} location map" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe><div class="map-links"><a href="https://www.google.com/maps/search/?api=1&query={lat},{lon}" target="_blank" rel="noopener">'+bi(['在Google Maps中打开','Open Google Maps'])+f'</a><a href="https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}" target="_blank" rel="noopener">OpenStreetMap ↗</a></div>'
  if typ=='metric':return '<div class="metric-figure">'+figure('figure-ground')+'</div><div class="downloads"><a href="'+url(d['assets']['figure-ground']['url'])+'" download>'+bi(['下载矢量图','Download SVG'])+'</a><a href="'+prefix+'comparison.html#figure-ground">'+bi(['并排比较01／03／04','Compare 01 / 03 / 04'])+'</a></div>'
  if typ=='strip':return '<div class="section-strip">'+''.join('<span>'+bi(x)+'</span>' for x in b['items'])+'</div>'
  if typ=='links':return '<div class="downloads">'+''.join(source_ref(x) for x in b['items'])+'</div>'
  if typ=='table':return '<div class="table-scroll" tabindex="0"><table><thead><tr>'+''.join('<th>'+bi(x)+'</th>' for x in b['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+bi(x)+'</td>' for x in row)+'</tr>' for row in b['rows'])+'</tbody></table></div>'
  if typ=='archive':return '<details class="archive"><summary>'+bi(b['title'])+'</summary>'+''.join(render(x) for x in b['blocks'])+'</details>'
  if typ=='assessment':
   return '<div class="dimension-grid">'+''.join('<article class="dimension"><div class="dimension-label">'+bi(x['label'])+'</div><h3>'+bi(x['verdict'])+'</h3><p>'+bi(x['text'])+'</p>'+(' <a class="dimension-source" href="'+e(url(x['source']),quote=True)+'" target="_blank" rel="noopener">'+bi(['出处','Source'])+'</a>' if x.get('source') else '')+'</article>' for x in d['assessment'][b.get('start',0):b.get('end',len(d['assessment']))])+'</div>'
  if typ=='metrics':return '<div class="metric-cards">'+''.join('<article><small>'+bi(x['label'])+'</small><strong>'+bi(x['display'])+'</strong><p>'+bi(x['scope'])+'</p><a href="'+e(url(x['source']),quote=True)+'" target="_blank" rel="noopener">'+bi(['出处与口径','Source and scope'])+'</a></article>' for x in d['metrics'])+'</div>'
  if typ=='factsheet':return '<button class="print-button" type="button">'+bi(['打印／保存PDF','Print / save PDF'])+'</button><div class="factsheet-layout">'+facts()+figure('figure-ground')+'</div>'
  raise ValueError(typ)
 views=[]
 for p in d['pages']:
  refs=''
  if p.get('sources'):refs='<details class="references"><summary>'+bi(['本页资料','Page references'])+'</summary><ol>'+''.join('<li>'+source_ref(s)+'</li>' for s in p['sources'])+'</ol></details>'
  views.append('<section class="case-view" id="'+p['id']+'" data-chapter="'+p['chapter']+'" data-title-zh="'+e(p['tab'][0],quote=True)+'" data-title-en="'+e(p['tab'][1],quote=True)+'" data-case-name="'+e(d['name'],quote=True)+'"'+(' hidden' if p['id']!='intro' else '')+'><div class="eyebrow">'+number+' / '+p['chapter'].upper()+'</div><h1 tabindex="-1">'+bi(p['title'])+'</h1><p class="lede">'+bi(p['lede'])+'</p>'+''.join(render(x) for x in p['blocks'])+refs+'</section>')
 tabs=[]
 for chapter,title in CHAPTERS:
  pages=[p for p in d['pages'] if p['chapter']==chapter]
  tabs.append('<nav class="page-tabs" aria-label="Chapter pages / 章内分页" data-chapter="'+chapter+'"'+(' hidden' if chapter!='intro' else '')+'>'+''.join('<a class="reader-link" href="#'+p['id']+'">'+bi(p['tab'])+'</a>' for p in pages)+'</nav>')
 index=''.join('<a href="'+prefix+path+'"'+(' aria-current="page"' if n==number else '')+'>'+n+' '+label+'</a>' for n,path,label in [('01','index.html','San Marco'),('02','cases/la-rambla.html','La Rambla'),('03','cases/piazza-del-campo.html','Siena'),('04','cases/federation-square.html','Federation Square'),('05','cases/schouwburgplein.html','Schouwburgplein'),('06','cases/place-de-la-republique.html','République')])
 nav=''.join('<a class="reader-link'+(' utility' if k in ['sources','factsheet'] else '')+'" data-chapter="'+k+'" href="#'+('scale' if k=='scale' else k)+'">'+bi(title)+'</a>' for k,title in CHAPTERS)
 css=(DOCS/'assets/case-reader.css').read_text();js=(DOCS/'assets/case-reader.js').read_text();version=hashlib.sha256((css+js).encode()).hexdigest()[:12]
 html='<!doctype html><html lang="zh" data-language="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="reader-version" content="'+version+'"><title>'+e(d['name'])+' | THE GREAT PLACES</title><style data-shared="case-reader">'+css+'</style></head><body data-case="'+number+'"><a class="skip reader-link" href="#intro">'+bi(['跳至正文','Skip to content'])+'</a><header class="site-header"><div class="shell"><div class="top-row"><a class="brand" href="'+prefix+'index.html">THE GREAT PLACES</a><div class="project-index" role="navigation" aria-label="Project index / 案例索引">'+index+'</div><div class="languages" role="group" aria-label="Language / 语言"><button data-lang="zh" aria-pressed="true">中文</button><button data-lang="en" aria-pressed="false">EN</button></div></div><nav class="chapter-nav" aria-label="Chapters / 章节">'+nav+'</nav></div></header><main class="shell"><div class="reader-heading"><div><strong>'+e(d['name'])+'</strong><p>'+bi(d['location'])+'</p></div><a href="'+prefix+'comparison.html" class="eyebrow">01 × 03 × 04 ↗</a></div>'+''.join(tabs)+''.join(views)+'</main><nav class="pager" aria-label="Page navigation / 分页"><div class="shell pager-inner"><a class="reader-link" data-step="-1" href="#intro"><small>'+bi(['← 上一页','← Previous'])+'</small><span class="pager-title"></span></a><span class="page-count" aria-live="polite"></span><a class="reader-link" data-step="1" href="#location"><small>'+bi(['下一页 →','Next →'])+'</small><span class="pager-title"></span></a></div></nav><footer class="shell site-footer">THE GREAT PLACES · '+number+' · '+bi(['图纸、数据与完整出处见资料页','Drawings, data and full references in Sources'])+'</footer><dialog class="image-dialog" aria-label="Image inspection / 放大图像"><button type="button">'+bi(['关闭 ×','Close ×'])+'</button><div class="dialog-inner"><img alt=""><div class="dialog-caption"></div></div></dialog><script data-shared="case-reader">'+js+'</script></body></html>\n'
 path=DOCS/next(path for n,path,_ in CASES if n==number);path.write_text(html.replace('><','>\n<'));print(number,version,len(d['pages']),'pages',len(html),'characters')
if __name__=='__main__':
 for n,_,_ in CASES:build_case(n)
 from build_case_comparison import build
 build()
