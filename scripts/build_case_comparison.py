"""Build the common three-case comparison and transparent quantitative export."""
from pathlib import Path
from html import escape as e
import json,csv,hashlib
from build_case_readers import bi
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
def build():
 ds=[json.loads((ROOT/f'cases/reader/{n}.json').read_text()) for n in ['01','03','04']]
 columns=['municipal_population','plaza_area','event_capacity','annual_visits','building_coverage']
 def src(u):return u[2:] if u.startswith('@/') else u
 def link(u):return '<a href="'+e(src(u),quote=True)+'" target="_blank" rel="noopener">'+bi(['出处','Source'])+'</a>'
 def cell(m):return '<strong>'+bi(m['display'])+'</strong><p>'+bi(m['scope'])+'</p>'+link(m['source'])
 def table(headers,rows):return '<div class="table-scroll" tabindex="0"><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in r)+'</tr>' for r in rows)+'</tbody></table></div>'
 views=[]
 def section(id,title,lede,body):
  views.append('<section class="case-view" id="'+id+'" data-chapter="'+id+'" data-title-zh="'+e(title[0],quote=True)+'" data-title-en="'+e(title[1],quote=True)+'" data-case-name="01 × 03 × 04"'+(' hidden' if views else '')+'><div class="eyebrow">01 × 03 × 04</div><h1 tabindex="-1">'+bi(title)+'</h1><p class="lede">'+bi(lede)+'</p>'+body+'</section>')
 figure_body='<div class="comparison-overflow"><div class="comparison-grid">'
 for d in ds:
  a=d['assets']['figure-ground'];figure_body+='<figure><h2>'+d['number']+' · '+e(d['name'])+'</h2><a href="'+src(a['url'])+'" target="_blank"><img src="'+src(a['url'])+'" alt="'+e(a['title'][0],quote=True)+'"></a><figcaption>'+bi(['600 × 600米 · 100米比例尺','600 × 600 m · 100 m graphic bar'])+'<p class="source-note">'+e('Overture 2026 / ODbL' if d['number']!='04' else 'City of Melbourne 2020 / CC BY 4.0')+'</p></figcaption></figure>'
 figure_body+='</div></div><div class="takeaway">'+bi(['三张图使用同一600米方框、同一米制比例、同一北向与100米尺。手机版可横向浏览，三张图保持等宽。白色含水面与铁路，不等于公共开放地面。','All frames use the same 600 m square, metric scale, north and 100 m bar. Swipe horizontally on mobile; all maps remain equal width. White includes water and railway, not just public open ground.'])+'</div><div class="downloads"><a href="data/comparison-figures.json">'+bi(['图纸参数与覆盖率计算','Drawing parameters and coverage measures'])+'</a><a href="data/case-comparison.csv" download>'+bi(['下载定量对照CSV','Download quantitative CSV'])+'</a></div>'
 section('figure-ground',['同一比例，比较三座广场','One scale, three squares'],['01以连续边界组织空间，03以坡地和街墙聚拢，04以公共平台连接基础设施与文化。','01 is organised by continuous edges, 03 by slope and fronts, and 04 by civic ground connecting infrastructure and culture.'],figure_body)
 rows=[]
 keys=['population','plaza_area','event_capacity','annual_visits','building_coverage']
 for key in keys:
  ms=[next(m for m in d['metrics'] if m['key']==key) for d in ds];rows.append([bi(ms[0]['label'])]+[cell(m) for m in ms])
 section('metrics',['关键数字与统计范围','Key numbers and statistical boundaries'],['同名指标同表呈现；不同年份、边界与统计方法保留在每一格里。未取得的年量留空，不用全市游客量补齐。','Named metrics share one table, with dates, boundaries and methods retained in every cell. Missing annual counts are not filled with city-wide tourism.'],table([bi(['指标','Metric'])]+[e(d['name']) for d in ds],rows)+'<div class="takeaway">'+bi(['容量不能直接排名：01为2018特定活动限额，03为2026中央站立区，04为现行Main Square场地口径。覆盖率是实际GIS计算，不是公共性评分。','Capacity is not a ranking: 01 is a 2018 event cap, 03 a 2026 central standing area, and 04 the current Main Square venue listing. GIS coverage is a computed measure, not a publicness score.'])+'</div><div class="downloads"><a href="data/case-comparison.csv" download>CSV ↓</a><a href="data/case-comparison.json">JSON ↗</a></div>')
 rows=[]
 for i in range(10):
  r=[bi(ds[0]['assessment'][i]['label'])]
  for d in ds:
   a=d['assessment'][i];r.append('<strong>'+bi(a['verdict'])+'</strong><p>'+bi(a['text'])+'</p>'+link(a['source']))
  rows.append(r)
 section('assessment',['十个共同维度，同一组用词','Ten shared dimensions, one vocabulary'],['用空间、交通、景观、商业、气候、功能、时段、规模、科技与服务对象对齐三案；没有缺乏证据的总分。','Align form, transit, landscape, commerce, climate, programme, calendar, scale, technology and users, without an unsupported total score.'],table([bi(['共同维度','Shared dimension'])]+[e(d['name']) for d in ds],rows))
 rows=[]
 for d in ds:
  pg=next(p for p in d['pages'] if p['id']=='events');t=next(b for b in pg['blocks'] if b['type']=='table');rows.append(['<strong>'+e(d['name'])+'</strong>']+[bi(x) for x in t['rows'][0][1:]])
 body=table([bi(['案例','Case']),bi(['平日','Ordinary weekday']),bi(['普通周末／节假日','Ordinary weekend / holiday']),bi(['大型活动日','Major event day'])],rows)
 body+='<div class="takeaway">'+bi(['这里比较的是已记录的功能与布置变化。三案都未有同口径平日／节假日连续人流数据，因此不计算“节假日增长倍数”；年度访客量也不平均分摊为每日人数。','This compares documented programme and layout changes. No matched continuous ordinary/holiday flow series exists for all three, so no holiday multiplier or annual-to-daily average is inferred.'])+'</div>'
 for d in ds:
  body+='<details class="archive"><summary>'+e(d['name'])+' · '+bi(['三个突出特点','Three defining qualities'])+'</summary><div class="reading-points">'+''.join('<article><h3>'+bi(x['title'])+'</h3><p>'+bi(x['text'])+'</p></article>' for x in d['highlights'])+'</div></details>'
 section('use',['平日、节假日与三个特点','Ordinary days, holidays and three qualities'],['社区和游客可共享同一场地；BOTH不代表相同比例，而是有两类服务证据。','Communities and visitors may share a place; BOTH records evidence of both roles, not an equal split.'],body)
 css=(DOCS/'assets/case-reader.css').read_text();js=(DOCS/'assets/case-reader.js').read_text();nav=''.join('<a class="reader-link" href="#'+i+'" data-chapter="'+i+'">'+bi(t)+'</a>' for i,t in [('figure-ground',['同尺度图底','Figure-ground']),('metrics',['关键数字','Key numbers']),('assessment',['统一评价','Assessment']),('use',['平日与节假日','Ordinary / holidays'])])
 version=hashlib.sha256((css+js).encode()).hexdigest()[:12]
 html='<!doctype html><html lang="zh" data-language="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="reader-version" content="'+version+'"><title>01 × 03 × 04 | THE GREAT PLACES</title><style>'+css+'</style></head><body class="comparison-page" data-case="comparison"><header class="site-header"><div class="shell"><div class="top-row"><a class="brand" href="index.html">THE GREAT PLACES</a><div class="project-index"><a href="index.html">01 San Marco</a><a href="cases/piazza-del-campo.html">03 Siena</a><a href="cases/federation-square.html">04 Federation Square</a></div><div class="languages"><button data-lang="zh">中文</button><button data-lang="en">EN</button></div></div><nav class="chapter-nav">'+nav+'</nav></div></header><main class="shell">'+''.join(views)+'</main><nav class="pager"><div class="shell pager-inner"><a class="reader-link" data-step="-1" href="#figure-ground"><small>'+bi(['← 上一页','← Previous'])+'</small><span class="pager-title"></span></a><span class="page-count" aria-live="polite"></span><a class="reader-link" data-step="1" href="#metrics"><small>'+bi(['下一页 →','Next →'])+'</small><span class="pager-title"></span></a></div></nav><footer class="shell site-footer">'+bi(['图底统一绘图比例；资料年代与建筑轮廓定义不同。数据不是导航、法律边界或现场测绘依据。','Drawing scale is shared; source epochs and footprint definitions differ. Data is not for navigation, legal boundaries or surveying.'])+'</footer><dialog class="image-dialog"><button type="button">'+bi(['关闭 ×','Close ×'])+'</button><div class="dialog-inner"><img alt=""><div class="dialog-caption"></div></div></dialog><script>'+js+'</script></body></html>\n'
 (DOCS/'comparison.html').write_text(html.replace('><','>\n<'))
 export={'checked':'2026-11-13','vocabulary':json.loads((ROOT/'cases/reader/vocabulary.json').read_text()),'cases':[{k:d[k] for k in ['number','name','coordinates','metrics','assessment','highlights']} for d in ds]};(DOCS/'data/case-comparison.json').write_text(json.dumps(export,ensure_ascii=False,indent=2)+'\n')
 with (DOCS/'data/case-comparison.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['case','metric','value','unit','year','scope_zh','scope_en','source','measurement','status'])
  for d in ds:
   for m in d['metrics']:w.writerow([d['number'],m['key'],'' if m['value'] is None else m['value'],m['unit'] or '',m['year'] or '',*m['scope'],m['source'],m['measurement'] or '', 'unavailable' if m['value'] is None else 'available'])
 print('Comparison built: 3 cases, 10 aligned dimensions, source-scoped numerical export')
if __name__=='__main__':build()
