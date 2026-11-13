"""Catch duplicate Siena photographs, including different URLs serving the same image."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request,urlopen
from urllib.parse import urlsplit,unquote
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import io,json,hashlib
ROOT=Path(__file__).resolve().parents[1];page=ROOT/'docs/cases/piazza-del-campo.html';out=ROOT/'work/restoration';out.mkdir(parents=True,exist_ok=True)
class Photos(HTMLParser):
 def __init__(self):super().__init__();self.photo=False;self.urls=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='figure':self.photo='photo' in a.get('class','').split()
  if tag=='img' and self.photo:self.urls.append(a['src'])
 def handle_endtag(self,tag):
  if tag=='figure':self.photo=False
p=Photos();p.feed(page.read_text());assert len(p.urls)==len(set(p.urls)),'Repeated photo URL in the Siena body'
def read(u):
 if u.startswith('https://'):
  with urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as r:b=r.read()
 else:b=(page.parent/unquote(urlsplit(u).path)).read_bytes()
 im=Image.open(io.BytesIO(b)).convert('RGB');small=im.convert('L').resize((9,8));v=list(small.tobytes());bits=''.join('1' if v[y*9+x]>v[y*9+x+1] else '0' for y in range(8) for x in range(8));return {'url':u,'dimensions':list(im.size),'normalized_rgb_sha256':hashlib.sha256(im.resize((64,64)).tobytes()).hexdigest(),'difference_hash':hex(int(bits,2))}
with ThreadPoolExecutor(max_workers=6) as pool:images=list(pool.map(read,p.urls))
pairs=[]
for i,a in enumerate(images):
 for b in images[i+1:]:
  distance=(int(a['difference_hash'],16)^int(b['difference_hash'],16)).bit_count()
  if distance<=1 or a['normalized_rgb_sha256']==b['normalized_rgb_sha256']:pairs.append({'first':a['url'],'second':b['url'],'hash_distance':distance})
result={'case':'03','photo_count':len(images),'distinct_urls':len(set(p.urls)),'duplicates_or_near_duplicates':pairs,'images':images};(out/'siena-photo-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='images'},ensure_ascii=False));assert not pairs,'Duplicate or near-duplicate requires editorial review'
