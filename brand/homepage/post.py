import re, json
html=open('index.html').read()
# drop the four hovering pros from the hero
html=re.sub(r'<div class="pro p\d">.*?</svg></div></div>','',html,flags=re.S)

WINGS=('<g transform="translate(48 80) scale(1.45) translate(-48 -80)"><g class="wing wl"><path class="wingp" d="M48 76 C22 54 2 66 8 82 C14 80 16 88 24 88 C26 95 36 95 48 88 Z"/><path d="M14 80 q10 -2 18 2 M24 88 q8 -4 16 -2"/></g></g>'
       '<g transform="translate(72 80) scale(1.45) translate(-72 -80)"><g class="wing wr"><path class="wingp" d="M72 76 C98 54 118 66 112 82 C106 80 104 88 96 88 C94 95 84 95 72 88 Z"/><path d="M106 80 q-10 -2 -18 2 M96 88 q-8 -4 -16 -2"/></g></g>')
FACES={
 'smile':'<path class="eyes" d="M55 46 h.1 M65 46 h.1"/><path d="M56 52 q4 3 8 0"/>',
 'grin':'<path class="eyes" d="M55 46 h.1 M65 46 h.1"/><path class="mouth" d="M54 51 q6 7 12 0 Z"/>',
 'wink':'<path class="eyes" d="M55 46 h.1"/><path d="M63 46 h4"/><path d="M56 52 q4 3 8 0"/>',
 'shock':'<path class="eyes" d="M55 45 h.1 M65 45 h.1"/><circle cx="60" cy="54" r="2.6"/>',
 'serious':'<path class="eyes" d="M55 47 h.1 M65 47 h.1"/><path d="M51 42 l6 2 M69 42 l-6 2 M56 54 h8"/>',
 'cool':'<path class="shades" d="M51 43 h18 v3 q-4 4 -8 0 h-2 q-4 4 -8 0 Z"/><path d="M57 54 q4 2 7 -1"/>',
 'specs':'<circle cx="55" cy="46" r="3.6"/><circle cx="65" cy="46" r="3.6"/><path d="M58.6 46 h2.8"/><path d="M56 53 q4 2 8 0"/>',
}
def pro(name,label,front='',face='smile',wings=True,arms='down',back=''):
    arm={'down':'M46 72 L30 98 M74 72 L90 98','right':'M46 72 L30 98 M74 72 L92 40','both':'M46 72 L40 36 M74 72 L80 36'}[arms]
    svg=(f'{WINGS if wings else ""}{back}'
         '<path class="fillbg" d="M48 64 h24 a4 4 0 0 1 4 4 v42 h-32 v-42 a4 4 0 0 1 4 -4 Z"/>'
         '<path d="M52 110 l-2 30 M68 110 l2 30 M44 140 h8 M68 140 h8"/>'
         f'<path d="{arm}"/><circle class="fillbg" cx="60" cy="48" r="13"/>{FACES[face]}{front}')
    return {'name':name,'label':label,'wings':wings,'svg':f'<svg viewBox="-4 -30 140 180" role="img" aria-label="{label}">{svg}</svg>'}

PROS=[
 pro('plumber','Plumber with a wrench','<path class="accent" d="M46 42 a14 13 0 0 1 28 0 Z"/><path d="M74 42 h10"/><path d="M52 64 v16 M68 64 v16"/><rect class="fillbg" x="50" y="80" width="20" height="30" rx="2"/><g transform="translate(88 96) rotate(30)"><path class="fillbg" d="M-3 0 h6 v22 h-6 Z M-8 -10 a8 8 0 1 0 16 0 l-4 4 h-8 Z"/></g>'),
 pro('lawyer','Lawyer with a briefcase','<path d="M48 39 q12 -14 24 0"/><path d="M54 64 l6 8 l6 -8"/><path class="accent" d="M60 72 l-3 4 l3 18 l3 -18 Z"/><rect class="fillbg" x="18" y="98" width="24" height="18" rx="3"/><path d="M26 98 v-4 h8 v4"/>',face='serious'),
 pro('insurance','Insurance agent under an umbrella','<path d="M48 40 q12 -12 24 0"/><path d="M92 40 V4"/><path class="soft" d="M52 6 Q92 -32 132 6 Q122 0 112 6 Q102 0 92 6 Q82 0 72 6 Q62 0 52 6 Z"/><path d="M92 40 q0 6 -5 6"/>',face='wink',wings=False,arms='right'),
 pro('doctor','Doctor with a stethoscope','<circle class="fillbg" cx="60" cy="36" r="4"/><path d="M47 38 q13 -8 26 0"/><path d="M52 64 q-2 22 8 22 q10 0 8 -22"/><circle cx="60" cy="88" r="3"/><path class="cross" d="M64 98 h8 M68 94 v8"/>'),
 pro('electrician','Electrician with a hard hat and a lightning bolt','<path class="yellow" d="M45 42 a15 13 0 0 1 30 0 h3 v4 h-36 v-4 Z"/><path d="M46 52 l-6 -1 M74 52 l6 -1 M47 57 l-5 2 M73 57 l5 2"/><path class="yellow" d="M92 88 l-7 12 h7 l-5 12 l12 -15 h-7 l5 -9 Z"/>',face='shock'),
 pro('mover','Mover carrying a box','<rect class="soft" x="36" y="2" width="48" height="34" rx="2"/><path d="M36 12 h48 M60 2 v10"/><path class="drop" d="M78 42 q3 5 0 8 q-3 -3 0 -8 Z"/>',wings=False,arms='both'),
 pro('cleaner','Cleaner with a mop','<path class="accent" d="M46 42 q14 -12 28 0 l6 4 l-6 2"/><path d="M88 96 L102 132"/><path class="fillbg" d="M92 132 h20 l3 10 h-26 Z"/><path d="M95 136 v6 M101 136 v6 M107 136 v6"/>',face='grin'),
 pro('realtor','Real estate agent holding a SOLD sign','<path d="M48 38 q6 -10 18 -6 q6 2 6 8"/><path d="M92 40 V8"/><rect class="fillbg" x="70" y="-14" width="44" height="22" rx="3"/><text x="92" y="2" text-anchor="middle" class="signtxt">SOLD</text>',face='grin',arms='right'),
 pro('trainer','Personal trainer with a dumbbell','<path class="band" d="M47 40 h26"/><path class="thick" d="M84 98 h16 M84 92 v12 M100 92 v12"/>',face='cool'),
 pro('handyman','Handyman with a hammer','<path d="M54 53 q3 -3 6 0 q3 -3 6 0"/><path d="M47 40 q13 -10 26 0"/><path d="M44 100 h32"/><path d="M90 98 l8 -22"/><path class="fillbg" d="M90 74 l14 7 l-3 5 l-14 -7 Z"/>',face='smile'),
 pro('tutor','Tutor with a book','<circle class="fillbg" cx="60" cy="31" r="6"/><path d="M47 44 q13 -14 26 0"/><rect class="soft" x="16" y="94" width="26" height="20" rx="2"/><path d="M29 94 v20"/>',face='specs'),
 pro('mechanic','Mechanic with a tyre','<path d="M46 42 a14 13 0 0 1 28 0 Z" class="blue"/><path d="M50 62 l2 -4"/><circle class="fillbg" cx="96" cy="104" r="13"/><circle cx="96" cy="104" r="5"/><path d="M62 82 q4 2 8 0"/>',face='grin'),
]

middle=''

css='''
.how{max-width:1100px;margin:0 auto;padding:96px 24px 48px;font-family:Inter,system-ui,sans-serif;color:var(--ink)}
.how h2{font-family:'Space Grotesk',sans-serif;font-size:clamp(32px,4vw,48px);letter-spacing:-1px;margin:0 0 32px;text-align:center}
.how ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}
.how li{border:2px solid var(--ink);border-radius:20px;padding:24px}
.how li span{display:inline-grid;place-items:center;width:36px;height:36px;border-radius:99px;background:var(--accent);color:#fff;font-weight:700}
.how h3{font-family:'Space Grotesk',sans-serif;font-size:22px;margin:14px 0 6px}.how p{margin:0;color:var(--muted);line-height:1.5}
.foot{position:relative;font-family:Inter,system-ui,sans-serif;color:var(--ink)}
.pile{height:clamp(170px,22vh,220px);border-bottom:2px solid var(--ink)}
.footbar{display:flex;flex-wrap:wrap;gap:16px 32px;align-items:center;justify-content:space-between;padding:24px clamp(16px,4vw,48px) 40px}
.footbar nav{display:flex;flex-wrap:wrap;gap:20px}.footbar a{color:var(--ink);text-decoration:none}.footbar p{margin:0;color:var(--muted)}
.sky{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:2}
nav,.copy{z-index:3!important}
.hero{height:100vh;height:100dvh;min-height:560px;position:relative}
.copy{justify-content:center!important;padding:16px 20px!important}
.street{flex-shrink:0}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.ask{display:flex;align-items:center;gap:6px;width:min(640px,100%);background:var(--bg);border:2px solid var(--ink);border-radius:999px;padding:6px 6px 6px 22px;box-shadow:0 6px 0 var(--ink);margin-top:8px}
.ask input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:500 18px Inter,system-ui,sans-serif;color:var(--ink);min-height:48px}
.ask input::placeholder{color:var(--muted)}
.ask button{display:grid;place-items:center;width:48px;height:48px;border-radius:999px;border:0;cursor:pointer;background:transparent;color:var(--ink)}
.ask .go{background:var(--accent);color:#fff}
.ask svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.ask:focus-within{box-shadow:0 6px 0 var(--accent);border-color:var(--accent)}
.try{margin:6px 0 0;font-size:14px;color:var(--muted)}.try a{color:var(--ink)}
nav,.copy,.street,.how,.footbar{position:relative;z-index:1}.footbar{background:var(--bg)}
.faller{position:absolute;left:0;top:0;width:var(--pw);will-change:transform}
.faller svg{width:100%;height:auto;overflow:visible;display:block}
.faller svg *{fill:none;stroke:var(--ink);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.faller .fillbg{fill:var(--bg)}.faller .wingp,.faller .soft{fill:var(--soft)}.faller .accent{fill:var(--accent)}
.faller .yellow{fill:#FFC93D}.faller .blue{fill:#7FB2FF}.faller .drop{fill:#9EC9FF;stroke-width:1.5}
.faller .eyes{stroke-width:4}.faller .mouth{fill:var(--bg)}.faller .shades{fill:var(--ink)}
.faller .cross{stroke:var(--accent);stroke-width:3}.faller .band{stroke:var(--accent);stroke-width:5}.faller .thick{stroke-width:5}
.faller .signtxt{stroke:none;fill:var(--accent);font:700 12px 'Space Grotesk',sans-serif;letter-spacing:1px}
.faller .wing{transform-box:fill-box;animation:flap .3s ease-in-out infinite alternate}
.faller .wl{transform-origin:100% 50%}.faller .wr{transform-origin:0% 50%;animation-name:flapr}
.faller.landed .wing{animation:none;transform:rotate(-40deg) scale(.6)}.faller.landed .wr{transform:rotate(40deg) scale(.6)}
.faller.bounce svg{animation:squash .5s ease-out;transform-origin:50% 100%}
@keyframes squash{30%{transform:scale(1.08,.88)}60%{transform:scale(.97,1.04)}100%{transform:none}}
@keyframes flap{to{transform:rotate(-16deg) scaleY(.85)}}@keyframes flapr{to{transform:rotate(16deg) scaleY(.85)}}
'''
js='''<script>
(()=>{
const ALL=%s;
const sky=document.getElementById('sky');
const fast=/fast/.test(location.search)?8:1, reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const phone=innerWidth<640;
const pick=phone?['plumber','insurance','doctor','electrician']:['plumber','lawyer','insurance','doctor','electrician','mover'];
const cast=pick.map(n=>ALL.find(p=>p.name===n));
const pw=phone?64:100, H=pw*1.28;
// evenly spaced slots, shuffled so the order of arrival feels natural
let slots=cast.map((_,i)=>(i+.5)/cast.length);
const order=[...cast.keys()].sort(()=>Math.random()-.5).sort((a,b)=>(cast[a].name==='mover')-(cast[b].name==='mover'));
let floorY=0,fallers=[],last=0,t0=0;
function layout(){const sv=document.querySelector('.scene').getBoundingClientRect(),hr=document.querySelector('.hero').getBoundingClientRect();floorY=sv.top-hr.top+sv.height*(536/580);
  const pad=phone?14:Math.max(40,innerWidth*.06), span=innerWidth-2*pad-pw;
  fallers.forEach(f=>{f.tx=pad+f.slot*span; if(f.landed) place(f,f.tx,floorY-H+pw*.18,0);});}
function place(f,x,y,r){f.el.style.transform=`translate(${x}px,${y}px) rotate(${r}deg)`;}
function make(i,k){const p=cast[i],el=document.createElement('div');el.className='faller';el.style.setProperty('--pw',pw+'px');el.innerHTML=p.svg;sky.appendChild(el);
  return {el,p,slot:slots[i],start:k*2.6,y:-H*1.5,landed:false,drift:(Math.random()<.5?-1:1)*(40+Math.random()*60),ph:Math.random()*6};}
function land(f){f.landed=true;f.el.classList.add('landed','bounce');place(f,f.tx,floorY-H+pw*.18,0);}
function tick(t){if(!t0)t0=t;const dt=Math.min(.05,(t-(last||t))/1000)*fast;last=t;const el=(t-t0)/1000*fast;
  for(const f of fallers){if(f.landed||el<f.start)continue;
    const speed=f.p.name==='mover'?260:(f.p.name==='insurance'?70:95);
    f.y+=speed*dt; const end=floorY-H+pw*.18, rem=Math.max(0,end-f.y), k=Math.min(1,rem/600);
    const x=f.tx+f.drift*k+Math.sin(el*1.6+f.ph)*10*k, r=Math.sin(el*1.3+f.ph)*7*k;
    if(f.y>=end){land(f);continue;} place(f,x,f.y,r);}
  requestAnimationFrame(tick);}
addEventListener('load',()=>{fallers=order.map((i,k)=>make(i,k));window.scooFallers=fallers;layout();
  if(reduce){fallers.forEach(land);return;} requestAnimationFrame(tick);});
addEventListener('resize',layout);
const ex=['My AC just died…','Need a lawyer by Friday…','Cheaper car insurance…','Someone to move a sofa…','Help losing weight…','A plumber, now…'];
const inp=document.getElementById('need');let ei=0;if(!reduce)setInterval(()=>{if(document.activeElement!==inp&&!inp.value){ei=(ei+1)%%ex.length;inp.placeholder=ex[ei];}},2600);
})();
</script>'''%json.dumps([{k:p[k] for k in ('name','wings','svg')} for p in PROS])
html=html.replace('</section></body></html>','<div class="sky" id="sky" aria-hidden="true"></div></section>\n'+js+'\n</body></html>')
form='''<form class="ask" role="search" onsubmit="return false">
<label for="need" class="vh">What do you need?</label>
<input id="need" type="text" autocomplete="off" placeholder="My AC just died…">
<button type="button" class="mic" aria-label="Speak instead"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg></button>
<button type="submit" class="go" aria-label="Ask Scoo"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"/></svg></button>
</form>
<p class="try">Try: <a href="#">Leaky tap</a> · <a href="#">Car insurance</a> · <a href="#">Divorce lawyer</a> · <a href="#">Movers</a></p>'''
html=html.replace('<div class="ctas"><a class="btn primary" href="#">Tell Scoo what you need</a><a class="btn secondary" href="#">I\'m a pro</a></div>',form)
html=html.replace('<a class="pill" href="#">For pros</a>','<a class="pill" href="#">I\'m a pro</a>')
html=html.replace('</style>',css+'</style>',1)
html=html.replace('body{{','body{').replace('}}','}') if False else html
html=html.replace('.hero{min-height:100vh','.hero{min-height:100vh')

open('index.html','w').write(html)
print(len(PROS))

# ---------------- conversation after the arrow ----------------
chat_css = '''
h1 .rot{display:inline-block;position:relative;vertical-align:bottom;overflow:hidden;color:var(--accent);transition:width .45s cubic-bezier(.3,.8,.3,1);white-space:nowrap;padding-bottom:.08em;margin-bottom:-.08em}
h1 .rot .w{display:inline-block}
h1 .tail{color:var(--ink)}
h1{font-size:clamp(40px,5.4vw,80px)!important}
.scene{max-height:46vh!important}
h1 .rot .w.out{animation:wout .35s ease-in forwards}h1 .rot .w.in{animation:win .45s cubic-bezier(.3,.8,.3,1.2)}
@keyframes wout{to{transform:translateY(-100%);opacity:0}}@keyframes win{from{transform:translateY(100%);opacity:0}}
.faller.hop svg{animation:hop .6s ease-out;transform-origin:50% 100%}
@keyframes hop{30%{transform:translateY(-22%) rotate(-4deg)}55%{transform:translateY(0) scale(1.06,.92)}75%{transform:scale(.98,1.03)}}

.thread{display:none;width:min(640px,100%);flex-direction:column;gap:10px;overflow-y:auto;padding:4px 4px 8px;scroll-behavior:smooth}
.hero.chatting .thread{display:flex}
.hero.chatting h1{font-size:clamp(28px,3vw,40px);letter-spacing:-1px}
.hero.chatting .sub,.hero.chatting .try{display:none}
.hero.chatting .copy{justify-content:flex-end!important}
.msg{max-width:85%;padding:12px 16px;border:2px solid var(--ink);border-radius:20px;font-size:16px;line-height:1.45;text-align:left;animation:pop .25s ease-out}
.msg.me{align-self:flex-end;background:var(--soft);border-bottom-right-radius:6px}
.msg.bot{align-self:flex-start;background:var(--bg);border-bottom-left-radius:6px;display:flex;gap:10px;align-items:flex-start}
.msg.bot .av{flex-shrink:0;width:28px;height:28px;border-radius:99px;background:var(--accent);color:#fff;display:grid;place-items:center;font:700 12px 'Space Grotesk',sans-serif}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.chips button{min-height:40px;padding:0 14px;border-radius:999px;border:2px solid var(--ink);background:var(--bg);color:var(--ink);font:600 14px Inter,sans-serif;cursor:pointer}
.chips button:hover{background:var(--soft)}
.typing{display:inline-flex;gap:4px;padding:6px 2px}.typing i{width:7px;height:7px;border-radius:99px;background:var(--ink);opacity:.3;animation:dot 1s infinite}
.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}
.callcard{display:flex;flex-direction:column;gap:10px;margin-top:10px}
.callcard label{font-size:13px;color:var(--muted);display:flex;gap:8px;align-items:flex-start;line-height:1.4}
.callcard input[type=tel]{min-height:46px;border:2px solid var(--ink);border-radius:12px;padding:0 12px;font:500 17px Inter,sans-serif;background:var(--bg);color:var(--ink)}
.callcard input[type=checkbox]{width:18px;height:18px;margin-top:1px;accent-color:var(--accent)}
.callbtn{min-height:48px;border:0;border-radius:999px;background:var(--accent);color:#fff;font:700 16px Inter,sans-serif;cursor:pointer}
.callbtn:disabled{opacity:.45;cursor:not-allowed}
.msg.status{align-self:stretch;max-width:none;display:block;text-align:left}
@media (max-width:640px){.hero.chatting h1{display:none}}
.status b{font-family:'Space Grotesk',sans-serif;font-size:18px}
.bar{height:8px;border-radius:99px;border:2px solid var(--ink);margin-top:10px;overflow:hidden}.bar i{display:block;height:100%;width:0;background:var(--accent);transition:width 2.4s ease-in-out}
.ring{display:flex;align-items:center;gap:12px;margin-top:6px}
.ring .ph{width:44px;height:44px;border-radius:99px;background:var(--accent);display:grid;place-items:center;animation:ringing .5s ease-in-out infinite alternate}
.ring .ph svg{width:22px;height:22px;fill:none;stroke:#fff;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.faller.flyoff{transition:transform 1.6s cubic-bezier(.5,0,.8,.4)!important}
.faller.chosen{transition:transform 1.2s ease-in-out!important}
.faller .bubble{position:absolute;left:50%;bottom:100%;transform:translate(-50%,-6px);white-space:nowrap;background:var(--bg);border:2px solid var(--ink);border-radius:14px;padding:3px 8px;font:700 clamp(10px,1.1vw,13px) Inter,sans-serif;color:var(--ink);animation:pop .3s ease-out}
@keyframes pop{from{transform:scale(.92);opacity:0}}
@keyframes dot{50%{opacity:1}}
@keyframes ringing{from{transform:rotate(-12deg)}to{transform:rotate(12deg)}}
'''
chat_js = r'''<script>
(()=>{
// rotating expert in the headline, with the matching pro hopping on the street
(()=>{const rot=document.querySelector('h1 .rot');if(!rot||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const W=[['an expert',null],['a plumber','plumber'],['a lawyer','lawyer'],['an electrician','electrician'],['a doctor','doctor'],['an insurance agent','insurance'],['movers','mover']];
 let i=0;const meas=document.createElement('span');meas.style.cssText='position:absolute;visibility:hidden;white-space:nowrap';rot.parentNode.appendChild(meas);
 const fit=t=>{meas.textContent=t;rot.style.width=meas.getBoundingClientRect().width+'px';};fit(W[0][0]);addEventListener('resize',()=>fit(W[i][0]));
 setInterval(()=>{if(document.querySelector('.hero.chatting'))return;i=(i+1)%W.length;const [t,name]=W[i];
  const old=rot.querySelector('.w');old.classList.add('out');const nw=document.createElement('span');nw.className='w in';nw.textContent=t;
  setTimeout(()=>{old.remove();rot.appendChild(nw);fit(t);},300);
  const f=(window.scooFallers||[]).find(f=>f.p.name===name&&f.landed);if(f){f.el.classList.remove('hop');void f.el.offsetWidth;f.el.classList.add('hop');}
 },2200);})();
const hero=document.querySelector('.hero'),thread=document.getElementById('thread'),form=document.querySelector('.ask'),inp=document.getElementById('need');
const CATS=[
 {k:/plumb|leak|tap|pipe|toilet|drain|water heater/i,pro:'plumber',noun:'a plumber',q:'Is water leaking right now?',a:['Yes, it\'s urgent','No, it can wait']},
 {k:/lawyer|legal|divorce|attorney|custody|sue/i,pro:'lawyer',noun:'a lawyer',q:'What kind of help do you need?',a:['Divorce or family','Injury','Business','Something else']},
 {k:/insur/i,pro:'insurance',noun:'an insurance agent',q:'What do you want to insure?',a:['Car','Home','Life','Health']},
 {k:/electric|power|outlet|spark|breaker|wiring/i,pro:'electrician',noun:'an electrician',q:'Is anything sparking or smoking?',a:['Yes','No']},
 {k:/move|moving|sofa|couch|movers/i,pro:'mover',noun:'movers',q:'When do you need them?',a:['Today','This week','Later']},
 {k:/doctor|weight|health|glp|clinic|sick/i,pro:'doctor',noun:'a doctor',q:'Is this a medical emergency?',a:['Yes','No']},
];
let cat=null,step=0,zip='';
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const scroll=()=>{thread.scrollTop=thread.scrollHeight};
function sizeThread(){const copy=document.querySelector('.copy'),h1=document.querySelector('.copy h1');
  const h=copy.clientHeight-form.offsetHeight-(h1.offsetParent?h1.offsetHeight+18:0)-56;thread.style.maxHeight=Math.max(140,h)+'px';}
function me(t){const d=document.createElement('div');d.className='msg me';d.textContent=t;thread.appendChild(d);scroll();}
async function bot(html,delay=700){const d=document.createElement('div');d.className='msg bot';d.innerHTML='<span class="av">s</span><div class="body"><span class="typing"><i></i><i></i><i></i></span></div>';
  thread.appendChild(d);scroll();await wait(delay);d.querySelector('.body').innerHTML=html;scroll();return d;}
function chips(d,opts,fn){const c=document.createElement('div');c.className='chips';opts.forEach(o=>{const b=document.createElement('button');b.type='button';b.textContent=o;b.onclick=()=>{c.remove();fn(o)};c.appendChild(b)});(d.querySelector('.body')||d).appendChild(c);scroll();}
async function start(text){
  hero.classList.add('chatting');sizeThread();me(text);
  cat=CATS.find(c=>c.k.test(text))||CATS[0];
  await bot(`Got it. I'll find you ${cat.noun}. What's your ZIP code?`);
  step=1;inp.value='';inp.placeholder='ZIP code';inp.inputMode='numeric';inp.focus({preventScroll:true});
}
async function gotZip(z){
  zip=z;me(z);inp.value='';inp.placeholder='Type a message…';inp.removeAttribute('inputmode');step=2;
  if(cat.pro==='doctor'){}
  const d=await bot(cat.q);chips(d,cat.a,ans=>answered(ans));
}
async function answered(ans){
  me(ans);
  if(cat.pro==='doctor'&&ans==='Yes'){await bot('Please call 911 now. Scoo is not for emergencies.');return;}
  const d=await bot(`What number should ${cat.noun} call?<div class="callcard">
    <input type="tel" id="tel" autocomplete="tel" placeholder="(555) 555-0100" aria-label="Your phone number">
    <label><input type="checkbox" id="ok">I agree that Scoo and one matched pro may call me at this number about this request. Calls may be recorded.</label>
    <button class="callbtn" id="callme" type="button" disabled>Call me</button></div>`);
  const tel=d.querySelector('#tel'),ok=d.querySelector('#ok'),btn=d.querySelector('#callme');
  const check=()=>btn.disabled=!(ok.checked&&tel.value.replace(/\D/g,'').length>=10);tel.oninput=check;ok.onchange=check;
  btn.onclick=()=>{d.querySelector('.callcard').remove();me(tel.value);match();};
  step=3;
}
async function busy(s){
  // nobody free: say so plainly, offer a call back within the hour (the exchange sources a pro meanwhile)
  const all=window.scooFallers||[];
  all.forEach((f,i)=>setTimeout(()=>{const b=document.createElement('div');b.className='bubble';b.textContent='On a job';f.el.appendChild(b);},i*150));
  await wait(1400);
  const who=cat.noun.replace(/^an? /,'');
  s.innerHTML=`<b>All ${who}s near ${zip} are busy right now</b><div style="margin-top:6px">Want a call back within the hour? We'll keep looking and the first pro who's free will call you.</div>`;
  chips(s.tagName?s:s,['Yes, call me within the hour','Not now'],async ans=>{me(ans);
    all.forEach(f=>f.el.querySelectorAll('.bubble').forEach(b=>b.remove()));
    if(ans.startsWith('Yes')){const t=new Date(Date.now()+3600e3).toLocaleTimeString([], {hour:'numeric',minute:'2-digit'});
      await bot(`Done. A ${who} will call you by <b>${t}</b>. Keep your phone nearby. We'll text you if anything changes.`);}
    else await bot('No problem. Your request is saved. Just ask again whenever you\'re ready.');});
  if(!s.querySelector('.body')){const c=s.querySelector('.chips');}
  scroll();
}
async function match(){
  const s=document.createElement('div');s.className='msg bot status';s.innerHTML=`<b>Finding ${cat.noun} near ${zip}…</b><div class="bar"><i></i></div>`;thread.appendChild(s);scroll();
  requestAnimationFrame(()=>s.querySelector('.bar i').style.width='100%');
  if(/busy/.test(location.search)){await wait(2600);return busy(s);}
  const all=window.scooFallers||[];let chosen=all.find(f=>f.p.name===cat.pro)||all[0];
  await wait(900);
  all.forEach((f,i)=>{if(f===chosen)return;f.el.classList.remove('landed');f.el.classList.add('flyoff');
    const m=(f.el.style.transform.match(/translate\(([-\d.]+)px,\s*([-\d.]+)px\)/)||[0,0,0]);
    setTimeout(()=>{f.el.style.transform=`translate(${+m[1]+(Math.random()*200-100)}px,${-innerHeight}px) rotate(${Math.random()*40-20}deg)`;},i*120);});
  await wait(1600);
  if(chosen){const m=chosen.el.style.transform.match(/translate\(([-\d.]+)px,\s*([-\d.]+)px\)/);chosen.el.classList.add('chosen');
    chosen.el.style.transform=`translate(${innerWidth/2-chosen.el.offsetWidth/2}px,${m?m[2]:0}px) rotate(0deg) scale(1.15)`;
    await wait(1200);const b=document.createElement('div');b.className='bubble';b.textContent='Calling you!';chosen.el.appendChild(b);}
  s.innerHTML=`<b>Rivera Plumbing is calling you now</b><div class="ring"><span class="ph"><svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg></span><span>Licensed plumber · 2.1 miles away<br>Answer your phone. It's ringing from (214) 555-0199.</span></div>`;
  if(!/Plumb/.test(cat.noun)&&cat.pro!=='plumber'){s.querySelector('b').textContent=`Your ${cat.noun.replace(/^an? /,'')} is calling you now`;s.querySelector('.ring span:last-child').innerHTML='Matched near '+zip+'<br>Answer your phone. It\'s ringing now.';}
  scroll();
}
form.addEventListener('submit',e=>{e.preventDefault();const v=inp.value.trim();
  if(step===0&&v)start(v);else if(step===1&&/^\d{5}$/.test(v))gotZip(v);});
document.querySelector('.go').type='submit';
document.querySelectorAll('.try a').forEach(a=>a.onclick=e=>{e.preventDefault();if(step===0){inp.value=a.textContent;form.requestSubmit();}});
addEventListener('resize',()=>hero.classList.contains('chatting')&&sizeThread());
// scripted walk-through for recordings: ?demo
if(/demo/.test(location.search))(async()=>{
  const type=async(t)=>{inp.focus();for(const ch of t){inp.value+=ch;await wait(55);}};
  await wait(6500);await type('My water heater is leaking');await wait(400);form.requestSubmit();
  await wait(2000);await type('75201');await wait(300);form.requestSubmit();
  await wait(1800);thread.querySelector('.chips button').click();
  await wait(1700);const tel=document.getElementById('tel');for(const ch of '(214) 555-0142'){tel.value+=ch;await wait(40);}tel.oninput();
  await wait(400);document.getElementById('ok').click();await wait(500);document.getElementById('callme').click();
  if(/busy/.test(location.search)){await wait(5200);const c=[...thread.querySelectorAll('.chips button')].find(b=>b.textContent.startsWith('Yes'));c&&c.click();}
})();
})();
</script>'''
html=open('index.html').read()
html=html.replace('<form class="ask"','<div class="thread" id="thread" aria-live="polite"></div>\n<form class="ask"',1)
html=html.replace('</style>',chat_css+'</style>',1)
html=html.replace('</body></html>',chat_js+'\n</body></html>')
open('index.html','w').write(html)

# ---------------- logo in the top bar ----------------
MARK='''<svg class="mark" viewBox="38 26 276 192" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="9">
<circle cx="92" cy="94" r="48" stroke="currentColor"/><circle cx="260" cy="94" r="48" stroke="currentColor"/>
<path stroke="currentColor" d="M140 94 L212 94"/>
<path stroke="currentColor" d="M212 52 C202 38 170 38 162 56 C154 74 170 84 178 96 C186 108 196 122 194 140"/>
<path class="mouth" d="M194 140 C192 180 168 208 134 208 C106 208 84 194 76 174"/></g></svg>'''
html=open('index.html').read()
html=html.replace('<a class="logo" href="#">scoo</a>','<a class="logo" href="#" aria-label="Scoo home">'+MARK+'<span>scoo</span></a>',1)
html=html.replace('</style>','''
.logo{display:inline-flex;align-items:center;gap:10px;font-weight:500!important;letter-spacing:-.5px!important}
.logo .mark{height:42px;width:auto;color:var(--ink)}.logo .mouth{stroke:var(--accent)}
@media (max-width:640px){.logo .mark{height:36px}}
</style>''',1)
fav="data:image/svg+xml,"+__import__('urllib.parse').parse.quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="38 26 276 192"><g fill="none" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"><circle cx="92" cy="94" r="48" stroke="#111"/><circle cx="260" cy="94" r="48" stroke="#111"/><path d="M140 94 L212 94" stroke="#111"/><path d="M212 52 C202 38 170 38 162 56 C154 74 170 84 178 96 C186 108 196 122 194 140" stroke="#111"/><path d="M194 140 C192 180 168 208 134 208 C106 208 84 194 76 174" stroke="#FF6B4A"/></g></svg>')
html=html.replace('<title>',f'<link rel="icon" type="image/svg+xml" href="{fav}"><title>',1)
html=html.replace('family=Space+Grotesk:wght@600;700','family=Space+Grotesk:wght@500;600;700')
open('index.html','w').write(html)
