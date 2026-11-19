# Turns the built homepage into the pre-launch waitlist page. Keeps the live flow as index-live.html.
import shutil
html=open('index.html').read()
font='''<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet"><style>
.sub,.try{display:none!important}.navlinks a:not(.pill){display:none!important}.copy{gap:26px!important}
h1{letter-spacing:-.035em!important;line-height:1.02!important;font-size:clamp(44px,6vw,92px)!important}
.ask{box-shadow:none!important;border-width:1.5px!important}.ask:focus-within{box-shadow:0 0 0 4px var(--soft)!important}
.navlinks .pill{border-width:1.5px!important;font-weight:500!important}
body,.ask input,.btn,nav a,.msg,.logo span,.scene text,.chips button,.callbtn,button,input{font-family:'Hanken Grotesk',sans-serif!important}
h1,h1 *{font-family:'Hanken Grotesk',sans-serif!important;font-weight:300!important}h1 .rot{font-weight:400!important}
.logo span{font-weight:400!important;letter-spacing:-.02em!important}.scene text{font-weight:500!important;letter-spacing:.14em!important}
</style>'''
# Re-measure the rotating word once Hanken Grotesk has actually arrived: until then the browser
# lays the headline out in a narrower fallback font, and a width measured then clips the word.
refit='''<script>(function(){var f=function(){dispatchEvent(new Event('resize'))};
if(document.fonts){document.fonts.addEventListener('loadingdone',f);document.fonts.load('300 64px "Hanken Grotesk"').then(f,f);document.fonts.load('400 64px "Hanken Grotesk"').then(f,f);}
addEventListener('load',f);})();</script>'''
html=html.replace('</head>',font+refit+'</head>',1)
open('index-live.html','w').write(html)

pl_css='''<style>
.badge{display:inline-flex;align-items:center;gap:8px;border:1.5px solid var(--ink);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:500}
.badge i{width:8px;height:8px;border-radius:99px;background:var(--accent);animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{50%{opacity:.25}}
.ask .go{width:auto!important;padding:0 20px;font-weight:600;font-size:15px;gap:6px;display:inline-flex!important;align-items:center}
.ask .mic{display:none!important}
.note{margin:0;font-size:14px;color:var(--muted)}
.pl{width:min(560px,100%);display:none;flex-direction:column;gap:14px;text-align:left;border:1.5px solid var(--ink);border-radius:22px;padding:20px 22px;background:var(--bg);animation:pop .3s ease-out}
.pl.on{display:flex}.pl h2{margin:0;font-size:22px;font-weight:500;letter-spacing:-.01em}.pl p{margin:0;color:var(--muted);line-height:1.45}
.meter{height:8px;border-radius:99px;border:1.5px solid var(--ink);overflow:hidden}.meter i{display:block;height:100%;width:0;background:var(--accent);transition:width 1.4s cubic-bezier(.3,.8,.3,1)}
.row2{display:flex;gap:8px;flex-wrap:wrap}.row2 input{flex:1 1 220px;min-height:48px;border:1.5px solid var(--ink);border-radius:999px;padding:0 18px;font-size:16px;background:var(--bg);color:var(--ink)}
.row2 button,.share button{min-height:48px;border-radius:999px;border:1.5px solid var(--ink);background:var(--ink);color:var(--bg);padding:0 20px;font-size:15px;font-weight:600;cursor:pointer}
.share{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}.share button{background:var(--bg);color:var(--ink);min-height:42px!important;padding:0 6px!important;font-size:14px!important}
.link{display:flex;align-items:center;gap:8px;border:1.5px dashed var(--ink);border-radius:14px;padding:10px 14px;font-size:15px}
.link span{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.fine{font-size:12px!important}
.tabs{display:grid;grid-template-columns:1fr 1fr;border:1.5px solid var(--ink);border-radius:999px;padding:4px;gap:4px}
.tabs button{min-height:40px;border:0;border-radius:999px;background:transparent;color:var(--ink);font-size:15px;font-weight:500;cursor:pointer}
.tabs button[aria-selected=true]{background:var(--ink);color:var(--bg)}
.tab{display:flex;flex-direction:column;gap:12px}.tab[hidden]{display:none}
.link .copy{flex:0 0 auto;width:auto;min-height:40px;border-radius:999px;border:1.5px solid var(--ink);background:var(--bg);color:var(--ink);padding:0 14px;font-weight:600;cursor:pointer}
#trade{min-height:46px;border:1.5px solid var(--ink);border-radius:999px;padding:0 16px;font-size:15px;background:var(--bg);color:var(--ink)}
.earned{display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:2px 10px;border-top:1.5px solid var(--line,#ddd);padding-top:12px}
.earned span{color:var(--muted);font-size:14px}.earned b{font-size:24px;font-weight:500}.earned small{grid-column:1/-1;color:var(--muted);font-size:12px}
.prolink{color:var(--ink);font-weight:500}
.hero.joined .ask,.hero.joined .note{display:none}
.hero.joined h1{display:none}.hero.joined .copy{gap:16px!important}.pl{gap:12px}.pl p{font-size:15px}
@media (max-width:640px){.hero.joined h1{display:none}.pl{padding:16px}}
</style>'''
pl_html='''<p class="badge" id="badge"><i></i>Launching city by city</p>'''
form_new='''<form class="ask" role="search" id="zipform">
<label for="need" class="vh">Your ZIP code</label>
<input id="need" type="text" inputmode="numeric" autocomplete="postal-code" maxlength="5" placeholder="Enter your ZIP code">
<button type="submit" class="go">Join the waitlist</button>
</form>
<p class="note">Be first when Scoo arrives. Free to join. · <a class="prolink" href="#" id="knowpro">Know a great pro? Refer them</a></p>
<div class="pl" id="pl" aria-live="polite"></div>'''
import re
html=re.sub(r'<div class="thread" id="thread" aria-live="polite"></div>\s*<form class="ask".*?</form>',lambda m:'<div class="thread" id="thread" aria-live="polite"></div>\n'+form_new,html,flags=re.S)
html=html.replace('<div class="copy">','<div class="copy">\n'+pl_html,1)
pl_js=r'''<script>
(()=>{
// Pre-launch waitlist. Numbers below are placeholders; production reads them from the waitlist store.
const form=document.getElementById('zipform'),inp=document.getElementById('need'),pl=document.getElementById('pl'),hero=document.querySelector('.hero');
const CITY={'75':'Dallas','76':'Fort Worth','77':'Houston','78':'Austin','85':'Phoenix','30':'Atlanta','33':'Miami','80':'Denver','90':'Los Angeles','10':'New York'};
const GOAL=1000;
new ResizeObserver(()=>dispatchEvent(new Event('resize'))).observe(pl);
// the live page cycles example requests in this box; here it only ever asks for a ZIP
Object.defineProperty(inp,'placeholder',{configurable:true,get(){return this.getAttribute('placeholder')},set(){}});
const hash=s=>[...s].reduce((a,c)=>(a*31+c.charCodeAt(0))%9973,7);
form.addEventListener('submit',e=>{e.preventDefault();e.stopImmediatePropagation();
  const z=inp.value.trim();if(!/^\d{5}$/.test(z)){inp.focus();inp.setAttribute('placeholder','5-digit ZIP, e.g. 75201');inp.value='';return;}
  const city=CITY[z.slice(0,2)]||'your area', waiting=180+hash(z)%620, pct=Math.round(waiting/GOAL*100);
  hero.classList.add('joined');
  pl.innerHTML=`<h2>${waiting.toLocaleString()} neighbours in ${city} are waiting</h2>
   <p>Scoo opens in ${city} at ${GOAL.toLocaleString()} sign-ups. Add yours.</p>
   <div class="meter" role="progressbar" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100" aria-label="${city} progress to launch"><i></i></div>
   <form class="row2" id="contact"><label class="vh" for="em">Email or phone</label><input id="em" autocomplete="email" placeholder="Email or mobile number" required><button type="submit">Save my spot</button></form>
   <p class="fine">We'll only contact you about Scoo launching near you. No spam.</p>`;
  pl.classList.add('on');requestAnimationFrame(()=>requestAnimationFrame(()=>pl.querySelector('.meter i').style.width=pct+'%'));
  document.getElementById('badge').innerHTML=`<i></i>Coming soon to ${city}`;
  pl.querySelector('#contact').addEventListener('submit',ev=>{ev.preventDefault();
    const spot=waiting+1, code='scoo.app/r/'+(z+spot).slice(-6);
    pl.innerHTML=`<h2>You're #${spot.toLocaleString()} in ${city}</h2>
     <div class="tabs" role="tablist"><button role="tab" aria-selected="true" data-t="friend">Know a friend?</button><button role="tab" aria-selected="false" data-t="pro">Know a pro?</button></div>
     <div class="tab" data-p="friend">
       <p>Invite friends and neighbours. You each get <b>$10 Scoo credit</b> when they join, and ${city} opens sooner.</p>
       <div class="meter"><i style="width:${Math.round(spot/GOAL*100)}%"></i></div>
       <div class="link"><span>${code}</span><button type="button" class="copy">Copy</button></div>
       <div class="share"><button type="button">WhatsApp</button><button type="button">Text</button><button type="button">Facebook</button><button type="button">Email</button></div>
     </div>
     <div class="tab" data-p="pro" hidden>
       <p>Your plumber, electrician, lawyer, mechanic? Send them your pro invite. You get <b>$25 Scoo credit</b> when they join and take their first job. They get Scoo's AI receptionist free.</p>
       <label class="vh" for="trade">Their trade</label>
       <select id="trade"><option>Plumber</option><option>Electrician</option><option>HVAC</option><option>Lawyer</option><option>Insurance agent</option><option>Mechanic</option><option>Cleaner</option><option>Mover</option><option>Other</option></select>
       <div class="link"><span>${code.replace('/r/','/pro/')}</span><button type="button" class="copy">Copy</button></div>
       <div class="share"><button type="button">WhatsApp</button><button type="button">Text</button><button type="button">Email</button><button type="button">More</button></div>
       <p class="fine">You send the invite from your phone. Scoo never contacts a pro you mention unless they sign up.</p>
     </div>
     <div class="earned"><span>Your credit so far</span><b>$0</b><small>$10 per friend · $25 per pro · up to $100</small></div>
     <p class="fine">Credit is applied to your requests once Scoo launches in your city. Not redeemable for cash.</p>`;
    pl.querySelectorAll('.copy').forEach(b=>b.onclick=e2=>{const t=b.previousElementSibling.textContent;navigator.clipboard&&navigator.clipboard.writeText('https://'+t);b.textContent='Copied';});
    pl.querySelectorAll('[role=tab]').forEach(t=>t.onclick=()=>{pl.querySelectorAll('[role=tab]').forEach(x=>x.setAttribute('aria-selected',x===t));
      pl.querySelectorAll('.tab').forEach(p=>p.hidden=p.dataset.p!==t.dataset.t);});
  });
},true);
document.getElementById('knowpro').onclick=e=>{e.preventDefault();inp.focus();inp.setAttribute('placeholder','Your ZIP first, then refer your pro');};
if(/waitlist-demo/.test(location.search))(async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));await w(6500);
  for(const c of '75201'){inp.value+=c;await w(90);}await w(400);form.requestSubmit();await w(2200);
  const em=document.getElementById('em');for(const c of 'sam@example.com'){em.value+=c;await w(45);}await w(400);document.getElementById('contact').requestSubmit();await w(3200);const pt=document.querySelector('[data-t=pro]');pt&&pt.click();})();
})();
</script>'''
html=html.replace('</style></head>','</style>'+pl_css+'</head>',1) if False else html.replace('</head>',pl_css+'</head>',1)
html=html.replace('</body></html>',pl_js+'\n</body></html>')
open('index.html','w').write(html)
