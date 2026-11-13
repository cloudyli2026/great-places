const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
const {execFileSync}=require('child_process');
// Trust only this managed environment's known proxy CA in Chromium.
let proxyArgs=[];if(process.env.CODEX_PROXY_CERT){const pub=execFileSync('openssl',['x509','-in',process.env.CODEX_PROXY_CERT,'-pubkey','-noout']);const der=execFileSync('openssl',['pkey','-pubin','-outform','der'],{input:pub});const pin=require('crypto').createHash('sha256').update(der).digest('base64');proxyArgs=['--ignore-certificate-errors-spki-list='+pin];}
const out=path.resolve(process.env.TEST_OUTPUT||'work/browser-results');fs.mkdirSync(out,{recursive:true});
const base=process.env.TEST_BASE||'http://127.0.0.1:8000/cases/federation-square.html';
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox',...proxyArgs]});
 const results={url:base,checked:new Date().toISOString(),checks:[],errors:[],failedRequests:[]};
 const expect=(ok,detail)=>{results.checks.push({pass:!!ok,detail});if(!ok)console.error('FAIL',detail)};
 for(const [label,width,height] of [['desktop',1440,1000],['mobile',390,844],['small-mobile',320,740]]){
  const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1});
  const page=await context.newPage();page.on('pageerror',e=>results.errors.push({label,error:e.message}));
  page.on('requestfailed',r=>results.failedRequests.push({label,url:r.url(),error:r.failure()?.errorText}));
  await page.goto(base,{waitUntil:'networkidle'});
  const ids=['intro','scale','syntax','boundary','life','conclusion','factsheet'];
  for(const lang of ['zh','en']){
   await page.locator(`[data-lang="${lang}"]`).click();
   expect(await page.locator('html').getAttribute('lang')===lang,`${label}/${lang}: document language`);
   for(const id of ids){
    await page.evaluate(id=>location.hash=id,id);await page.waitForTimeout(150);
    expect(await page.locator('main>section:visible').count()===1&&await page.locator(`section#${id}`).isVisible(),`${label}/${lang}/${id}: one chapter visible`);
    expect(await page.locator('.chapter-nav a[aria-current="page"]').evaluate(a=>a.hash)==='#'+id,`${label}/${lang}/${id}: active nav`);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${label}/${lang}/${id}: no document overflow`);
    const images=page.locator(`section#${id} img`);
    for(let i=0;i<await images.count();i++){
     await images.nth(i).scrollIntoViewIfNeeded();await images.nth(i).evaluate(im=>im.loading='eager');
     try{await images.nth(i).evaluate(im=>im.decode());}catch(e){results.errors.push({label,lang,id,src:await images.nth(i).getAttribute('src'),error:'image decode failed'})}
     expect(await images.nth(i).evaluate(im=>im.complete&&im.naturalWidth>0),`${label}/${lang}/${id}: image ${i+1} decoded`);
    }
    const opposite=lang==='en'?'zh':'en';
    expect(await page.locator(`section#${id} [lang="${opposite}"]:visible`).count()===0,`${label}/${lang}/${id}: opposite-language text hidden`);
    await page.evaluate(()=>scrollTo(0,0));
    if(label!=='small-mobile'&&['intro','scale','boundary','life','factsheet'].includes(id)&&lang==='zh')await page.screenshot({path:path.join(out,`${label}-${id}.png`),fullPage:true});
   }
  }
  await page.evaluate(()=>location.hash='scale');await page.waitForTimeout(100);
  await page.locator('.chapter-nav a[href$="#syntax"]').click();await page.waitForTimeout(100);
  expect(await page.locator('#syntax').isVisible(),`${label}: chapter nav click`);
  await page.locator('#syntax .chapter-pagination a').first().click();await page.waitForTimeout(100);
  expect(await page.locator('#scale').isVisible(),`${label}: previous chapter click`);
  const opener=page.locator('#fed-gis .image-inspect');await opener.click();
  expect(await page.locator('dialog').evaluate(d=>d.open),`${label}: image dialog opens`);
  await page.keyboard.press('Escape');expect(!await page.locator('dialog').evaluate(d=>d.open),`${label}: Escape closes image dialog`);
  expect(await opener.evaluate(b=>b===document.activeElement),`${label}: image dialog restores focus`);
  await page.evaluate(()=>location.hash='syntax');await page.waitForTimeout(150);await page.goBack();await page.waitForTimeout(150);
  expect(await page.locator('#scale').isVisible(),`${label}: browser history restores chapter`);
  for(const [hash,id] of [['climate','life'],['sources','conclusion'],['fed-gis-figure-ground','scale']]){
   await page.evaluate(h=>location.hash=h,hash);await page.waitForTimeout(100);expect(await page.locator('#'+id).isVisible(),`${label}: legacy #${hash} route`);
  }
  await page.evaluate(()=>location.hash='factsheet');await page.waitForTimeout(100);await page.emulateMedia({media:'print'});
  expect(await page.locator('#factsheet').isVisible(),`${label}: factsheet print view`);
  if(label==='desktop')await page.pdf({path:path.join(out,'federation-square-factsheet.pdf'),preferCSSPageSize:true,printBackground:true});
  await context.close();
 }
 results.summary={passed:results.checks.filter(c=>c.pass).length,failed:results.checks.filter(c=>!c.pass).length,errors:results.errors.length};
 fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results.summary));
 await browser.close();if(results.summary.failed||results.errors.length)process.exitCode=1;
})();
