const {chromium}=require('playwright');
const f='file://'+process.argv[2];
(async()=>{const b=await chromium.launch();
 for (const [n,w,h,s,sc] of [['desktop',1440,900,2,'light'],['phone',390,844,3,'light'],['desktop-dark',1440,900,2,'dark']]){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:s,colorScheme:sc});
 await p.goto(f+'?fast');await p.waitForTimeout(5000);
 const sh=await p.evaluate(()=>document.documentElement.scrollHeight);console.log(n,'scrollHeight',sh,'viewport',h);
 await p.screenshot({path:`single-${n}.png`});}
 const ctx=await b.newContext({viewport:{width:1280,height:720},recordVideo:{dir:'vid3',size:{width:1280,height:720}}});
 const p=await ctx.newPage();await p.goto(f);await p.waitForTimeout(20000);await ctx.close();await b.close();
})();
