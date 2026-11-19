const {chromium}=require('playwright');
const f='file://'+process.argv[2]+'?demo&fast';
(async()=>{const b=await chromium.launch();
 // phone stills at key moments
 const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:3});
 p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto(f);
 const at=[[10200,'flow-1-question'],[13000,'flow-2-callcard'],[17000,'flow-3-finding'],[21000,'flow-4-calling']];
 let t=0;for(const [ms,n] of at){await p.waitForTimeout(ms-t);t=ms;await p.screenshot({path:n+'.png'});}
 for (const [n,w,h] of [['desktop',1280,720],['phone',390,844]]){
  const ctx=await b.newContext({viewport:{width:w,height:h},recordVideo:{dir:'vid-'+n,size:{width:w,height:h}}});
  const q=await ctx.newPage();await q.goto(f);await q.waitForTimeout(24000);await ctx.close();}
 await b.close();})();
