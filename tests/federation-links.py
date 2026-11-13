"""Audit the case's local references and remote URLs using real GETs (stdlib)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote,urldefrag
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'docs/cases/federation-square.html'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if a.get('href'):self.refs.append((tag,a['href']))
  if tag=='img' and a.get('src'):self.refs.append((tag,a['src']))
p=Links();p.feed(PAGE.read_text());assert len(p.ids)==len(set(p.ids)),'Duplicate DOM IDs'
urls={u for _,u in p.refs if u.startswith('https://')}
assets=json.loads((ROOT/'cases/federation-square/sources.json').read_text())
urls.update(a['image_url'] for a in assets['assets'] if a['image_url'].startswith('https://'))
local=[]
for tag,ref in p.refs:
 if ref.startswith('https://'):continue
 path,hash=urldefrag(ref)
 if not path:
  ok=not hash or unquote(hash) in p.ids
 else:ok=(PAGE.parent/unquote(path)).is_file()
 local.append({'url':ref,'pass':ok})
def get(url):
 for attempt in range(2):
  try:
   with urlopen(Request(url,headers={'User-Agent':'THE-GREAT-PLACES-source-audit/1.0'}),timeout=45) as r:
    payload=r.read();mime=r.headers.get('Content-Type','');status=r.status
    kind='image' if '/images/' in url or '/mediadata/' in url or 'site_media/' in url or '/wp-content/uploads/' in url else 'pdf' if urlparse(url).path.lower().endswith('.pdf') else 'html'
    valid=(payload.startswith(b'%PDF-') and 'pdf' in mime) if kind=='pdf' else mime.startswith('image/') if kind=='image' else 'html' in mime
    return dict(url=url,status=status,type=mime,bytes=len(payload),kind=kind,pass_check=status==200 and valid,sha256=hashlib.sha256(payload).hexdigest(),final_url=r.url)
  except Exception as e:
   if attempt: return dict(url=url,pass_check=False,error=str(e))
   time.sleep(.5)
remote=list(ThreadPoolExecutor(6).map(get,sorted(urls)))
report={'checked':'2026-11-13','scope':'All image src and href URLs in Federation Square page, plus the asset register. HTTP GET and MIME/PDF-signature validation. Browser independently decodes visible images.','local':local,'remote':remote,'summary':{'local_refs':len(local),'remote_urls':len(remote),'failed':sum(not x['pass'] for x in local)+sum(not x['pass_check'] for x in remote)}}
out=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'docs/research/federation-square/link-results.json'
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['summary']))
for x in remote:
 if not x['pass_check']:print(x)
if report['summary']['failed']:sys.exit(1)
