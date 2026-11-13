"""Check all reachable media, citations, local assets and fragment targets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
import concurrent.futures,json,urllib.request,urllib.error,time,os,re
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  for key in ('href','src'):
   if key in a:self.links.append((tag,key,a[key]))
pages=['index.html','cases/piazza-del-campo.html','cases/federation-square.html','comparison.html'];urls={};local=[]
for page in pages:
 p=Parse();p.feed((DOCS/page).read_text())
 for tag,key,url in p.links:
  if url.startswith(('http://','https://')):urls.setdefault(url,[]).append({'page':page,'tag':tag,'attribute':key});continue
  target=urljoin('https://local/'+page,url);s=urlsplit(target);f=DOCS/unquote(s.path.lstrip('/'));valid=f.exists();detail='file'
  if valid and s.fragment and f.suffix=='.html':
   q=Parse();q.feed(f.read_text());valid=s.fragment in q.ids or s.fragment in ['scale','climate'];detail='fragment'
  local.append({'page':page,'url':url,'valid':valid,'type':detail})
def fetch(item):
 url,refs=item
 for attempt in range(2):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; GreatPlacesResearch/1.0)'})
   with urllib.request.urlopen(req,timeout=35) as r:
    data=r.read(1024);ctype=r.headers.get('Content-Type','');status=r.status;final=r.url
   expected_image=any(x['tag'] in ['img','image'] for x in refs)
   expected_pdf=urlsplit(url).path.lower().endswith('.pdf')
   challenge=b'_Incapsula_Resource' in data or b'cf-chl-' in data
   ok=status==200 and (not expected_image or ctype.startswith('image/')) and (not expected_pdf or data.startswith(b'%PDF-'))
   return {'url':url,'status':status,'type':ctype,'final':final,'valid':ok,'content_verified':not challenge,'warning':'Access challenge; HTTP 200 alone does not verify page content' if challenge else None,'references':refs}
  except Exception as ex:
   err=str(ex)
 return {'url':url,'status':getattr(ex,'code',None) if False else None,'error':err,'valid':False,'references':refs}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:external=list(pool.map(fetch,urls.items()))
result={'checked':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'local':local,'external':external};result['summary']={'local_total':len(local),'local_failed':sum(not x['valid'] for x in local),'external_total':len(external),'external_failed':sum(not x['valid'] for x in external),'access_challenges':sum(x.get('content_verified') is False for x in external)}
out=ROOT/'work/reader-tests';out.mkdir(exist_ok=True,parents=True);(out/'link-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False));print(json.dumps(result['summary']));print(json.dumps([x for x in external if not x['valid']],indent=2,ensure_ascii=False))

if result['summary']['local_failed'] or result['summary']['external_failed']:raise SystemExit(1)
