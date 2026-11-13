/* Integration test of the shared reader, real media, maps and print output. */
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {execFileSync}=require('child_process');
const base=process.env.TEST_BASE||'http://127.0.0.1:8017/';
const out=path.resolve(process.env.TEST_OUTPUT||'work/reader-tests');fs.mkdirSync(out,{recursive:true});
let args=['--no-sandbox'];
if(process.env.CODEX_PROXY_CERT){const pub=execFileSync('openssl',['x509','-in',process.env.CODEX_PROXY_CERT,'-pubkey','-noout']);const pin=crypto.createHash('sha256').update(execFileSync('openssl',['pkey','-pubin','-outform','der'],{input:pub})).digest('base64');args.push('--ignore-certificate-errors-spki-list='+pin);}
const result={base,checked:new Date().toISOString(),checks:[],errors:[],media:[],maps:[]};
function check(ok,label){result.checks.push({pass:!!ok,label});if(!ok)console.error('FAIL',label);}
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROMIUM||'/usr/bin/chromium',args});
await Promise.all([['01','index.html'],['03','cases/piazza-del-campo.html'],['04','cases/federation-square.html']].map(async([n,url])=>{
 for(const [device,width,height] of [['desktop',1440,1000],['mobile',390,844],['small-mobile',320,740]]){
 const ctx=await browser.newContext({viewport:{width,height}}),p=await ctx.newPage();p.on('pageerror',e=>result.errors.push({n,device,error:e.message}));
 await p.goto(base+url,{waitUntil:'domcontentloaded'});await p.locator('.page-count').waitFor();
 const ids=await p.locator('.case-view').evaluateAll(v=>v.map(x=>x.id));
 check(ids.length>=20,`${n}/${device}: restored history and programme pages available`);
 for(const lang of ['zh','en']){
  await p.locator(`[data-lang=${lang}]`).click();
  check(await p.locator('html').getAttribute('lang')===lang,`${n}/${device}/${lang}: language`);
  for(const id of ids){
   await p.evaluate(id=>location.hash=id,id);await p.waitForFunction(id=>document.querySelector('.case-view:not([hidden])')?.id===id,id);
   const view=p.locator('#'+id);
   check(await p.locator('.case-view:visible').count()===1,`${n}/${device}/${lang}/${id}: only current page shown`);
   check(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${n}/${device}/${lang}/${id}: no document overflow`);
   check(await view.locator(`[lang=${lang==='en'?'zh':'en'}]:visible`).count()===0,`${n}/${device}/${lang}/${id}: translated text only`);
   check(await p.locator('.chapter-nav [aria-current]').getAttribute('data-chapter')===await view.getAttribute('data-chapter'),`${n}/${device}/${lang}/${id}: correct chapter`);
   if(lang==='zh'&&device==='desktop'){
    // Validate every ordinary image and SVG image, including originals inside disclosures.
    const urls=await view.locator('img,svg image').evaluateAll(xs=>xs.map(x=>x.tagName.toLowerCase()==='img'?x.src:x.href.baseVal));
    for(const src of [...new Set(urls)]){
     const resolved=await p.evaluate(src=>new URL(src,document.baseURI).href,src);
     const ok=await p.evaluate(async src=>{const im=new Image();im.src=src;try{await Promise.race([im.decode(),new Promise((_,r)=>setTimeout(()=>r(Error('timeout')),30000))]);return im.naturalWidth>0}catch{return false}},resolved);
     result.media.push({n,id,url:resolved,decoded:ok});check(ok,`${n}/${id}: media decoded ${resolved}`);
    }
    if(['intro','history','history-elevation','figure-ground','section','syntax','milestones','public-programme','celebrations','metrics','assessment','conclusion'].includes(id)){await p.evaluate(()=>scrollTo(0,0));await p.screenshot({path:path.join(out,`${n}-${device}-${id}.png`),fullPage:true});}
   }
   if(lang==='zh'&&device==='mobile'&&['intro','history','history-elevation','figure-ground','section','syntax','events','public-programme','celebrations','conclusion'].includes(id)){await p.evaluate(()=>scrollTo(0,0));await p.screenshot({path:path.join(out,`${n}-${device}-${id}.png`),fullPage:true});}
  }
 }
 await p.reload({waitUntil:'domcontentloaded'});check(await p.locator('html').getAttribute('lang')==='en',`${n}/${device}: language persists on reload`);
 await p.locator('[data-lang=zh]').click();await p.evaluate(()=>location.hash='intro');await p.waitForTimeout(60);
 for(const id of ids.slice(1)){await p.locator('[data-step="1"]').click();await p.waitForFunction(id=>document.querySelector('.case-view:not([hidden])')?.id===id,id);check(await p.locator('#'+id).isVisible(),`${n}/${device}: next-page click to ${id}`);}
 await p.locator('[data-step="-1"]').click();await p.waitForFunction(()=>document.querySelector('#sources:not([hidden])'));check(await p.locator('#sources').isVisible(),`${n}/${device}: previous page click`);
 await p.evaluate(()=>location.hash='figure-ground');await p.waitForTimeout(80);const opener=p.locator('#figure-ground .image-button');await opener.click();check(await p.locator('dialog').evaluate(x=>x.open),`${n}/${device}: image enlarges`);await p.keyboard.press('Escape');check(await opener.evaluate(x=>x===document.activeElement),`${n}/${device}: Escape restores focus`);
 await p.evaluate(()=>location.hash='plan');await p.waitForTimeout(70);await p.goBack();await p.waitForTimeout(70);check(await p.locator('#figure-ground').isVisible(),`${n}/${device}: browser back restores page`);
 await p.evaluate(()=>location.hash='scale');await p.waitForTimeout(70);check(await p.locator('#figure-ground').isVisible(),`${n}/${device}: legacy scale link`);
 await p.evaluate(()=>location.hash='location');await p.locator('iframe').scrollIntoViewIfNeeded();await p.waitForTimeout(4000);
 const map=await p.locator('iframe').getAttribute('src');check(map.includes('google.com/maps')&&map.includes('output=embed'),`${n}/${device}: identical interactive map type`);
 const mf=p.frames().find(f=>f.url().includes('google.com/maps'));const text=mf?await mf.locator('body').innerText().catch(()=> ''):'';check(/Map data|Map Data|Google/i.test(text),`${n}/${device}: live map rendered with attribution`);result.maps.push({n,device,url:map,frameUrl:mf?.url(),bodySample:text.slice(0,300)});
 if(device!=='small-mobile')await p.screenshot({path:path.join(out,`${n}-${device}-map.png`),fullPage:true});
 if(device==='desktop'){await p.evaluate(()=>location.hash='factsheet');await p.waitForTimeout(100);await p.locator('#factsheet img').evaluateAll(xs=>xs.forEach(x=>x.loading='eager'));await p.locator('#factsheet img').evaluate(im=>im.decode());await p.emulateMedia({media:'print'});check(await p.locator('#factsheet').isVisible(),`${n}: print factsheet visible`);await p.pdf({path:path.join(out,`${n}-factsheet.pdf`),preferCSSPageSize:true,printBackground:true});}
 await ctx.close();console.log('done',n,device);
 }
}));
for(const [device,width,height] of [['desktop',1440,1000],['mobile',390,844]]){
 const p=await browser.newPage({viewport:{width,height}});await p.goto(base+'comparison.html',{waitUntil:'domcontentloaded'});await p.locator('.page-count').waitFor();await p.waitForFunction(()=>document.querySelectorAll('.case-view:not([hidden])').length===1);for(const im of await p.locator('.comparison-grid img').all())await im.evaluate(x=>x.decode());
 const sizes=await p.locator('.comparison-grid img').evaluateAll(xs=>xs.map(x=>x.getBoundingClientRect().width));check(sizes.length===3&&Math.max(...sizes)-Math.min(...sizes)<.1,`comparison/${device}: all three diagrams at identical display scale`);
 for(const id of ['figure-ground','metrics','assessment','use']){await p.evaluate(id=>location.hash=id,id);await p.waitForTimeout(80);check(await p.locator('.case-view:visible').count()===1,`comparison/${device}/${id}: pagination`);check(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`comparison/${device}/${id}: no document overflow`);await p.screenshot({path:path.join(out,`comparison-${device}-${id}.png`),fullPage:true});}await p.close();
}
await browser.close();result.summary={passed:result.checks.filter(x=>x.pass).length,failed:result.checks.filter(x=>!x.pass).length,errors:result.errors.length,decoded:result.media.filter(x=>x.decoded).length,media:result.media.length};fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result.summary));if(result.summary.failed||result.summary.errors)process.exitCode=1;
})().catch(e=>{console.error(e);fs.writeFileSync(path.join(out,'browser-incomplete.json'),JSON.stringify(result,null,2));process.exitCode=1;});
