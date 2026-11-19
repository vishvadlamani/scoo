# Builds exchanges-start.html: the pitch and application for founding exchange operators (networks,
# brokers, trade groups, franchises). Pre-launch there are no live exchanges, so the page shows one
# clearly labelled example and reserves the applicant's exchange name.
import json, re
pros = json.load(open('_pros.json'))
mark = open('_mark.svg').read()
def place(svg, x, y, w, h):
    return re.sub(r'^<svg ', f'<svg x="{x}" y="{y}" width="{w}" height="{h}" ', svg.strip(), count=1)

# Calls flowing into a hub (the exchange) and out to its members.
HUB = f'''<svg viewBox="0 0 400 280" aria-hidden="true" class="ill">
<g class="links"><path id="l1" d="M200 140 C150 120 120 80 76 70"/><path id="l2" d="M200 140 C250 120 280 80 324 70"/>
<path id="l3" d="M200 140 C150 165 120 205 76 214"/><path id="l4" d="M200 140 C250 165 280 205 324 214"/></g>
<circle r="5" class="dot"><animateMotion dur="2.4s" repeatCount="indefinite" keyPoints="1;0" keyTimes="0;1" calcMode="linear"><mpath href="#l1"/></animateMotion></circle>
<circle r="5" class="dot"><animateMotion dur="2.4s" begin="-0.6s" repeatCount="indefinite" calcMode="linear"><mpath href="#l2"/></animateMotion></circle>
<circle r="5" class="dot"><animateMotion dur="2.4s" begin="-1.2s" repeatCount="indefinite" keyPoints="1;0" keyTimes="0;1" calcMode="linear"><mpath href="#l3"/></animateMotion></circle>
<circle r="5" class="dot"><animateMotion dur="2.4s" begin="-1.8s" repeatCount="indefinite" calcMode="linear"><mpath href="#l4"/></animateMotion></circle>
<rect x="130" y="108" width="140" height="64" rx="18" class="paper"/><text x="200" y="135" text-anchor="middle" class="h">YOUR EXCHANGE</text><text x="200" y="155" text-anchor="middle" class="s">your rules · your fee</text>
{place(pros['plumber'], 30, 16, 70, 90)}{place(pros['electrician'], 300, 16, 70, 90)}{place(pros['lawyer'], 30, 176, 70, 90)}{place(pros['insurance'], 300, 176, 70, 90)}
</svg>'''

TRADES = ['Plumbing', 'Electrical', 'HVAC', 'Roofing', 'Handyman', 'Cleaning', 'Moving', 'Locksmith', 'Pest control',
          'Landscaping', 'Auto repair', 'Legal', 'Insurance', 'Real estate', 'Health', 'Home services (mixed)', 'Other']
SIZES = ['Just starting', '1–10', '11–50', '51–200', '200+']
VOLUMES = ['None yet', 'Under 500', '500–5,000', '5,000–50,000', '50,000+']
CONSENT = ('I agree to Scoo\'s <a href="/terms" target="_blank" rel="noopener">terms</a>, and that Scoo may call, text or email me about this '
           'application. Reply STOP to opt out.')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Start an exchange on Scoo</title>
<meta name="description" content="Turn your network into an exchange. Your own page, rules in plain English, and you earn on every match. Apply to be a founding operator.">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#FFFFFF;--ink:#111111;--muted:#55595f;--accent:#FF6B4A;--soft:#FFD9CF;--line:#e7e5e0;--tint:#FFF6F3}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0E0E10;--ink:#EDEDED;--muted:#a7abb3;--accent:#FF7A5C;--soft:#4A2620;--line:#2a2a2e;--tint:#1a1412}}}}
:root[data-theme="dark"]{{--bg:#0E0E10;--ink:#EDEDED;--muted:#a7abb3;--accent:#FF7A5C;--soft:#4A2620;--line:#2a2a2e;--tint:#1a1412}}
*{{box-sizing:border-box}}html,body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Hanken Grotesk',system-ui,sans-serif}}
header{{display:flex;align-items:center;justify-content:space-between;padding:20px clamp(16px,4vw,48px);max-width:1200px;margin:0 auto}}
.logo{{display:inline-flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-size:26px;letter-spacing:-.02em}}
.logo .mark{{height:36px;width:auto;color:var(--ink)}}.logo .mouth{{stroke:var(--accent)}}
.pill{{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border:1.5px solid var(--ink);border-radius:999px;color:var(--ink);text-decoration:none;font-weight:500}}
main{{max-width:1120px;margin:0 auto;padding:8px clamp(16px,4vw,48px) 64px}}
.top{{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);grid-template-areas:"intro card" "art card";column-gap:clamp(24px,5vw,64px);align-items:start}}
.top>.intro{{grid-area:intro}}.top>.art{{grid-area:art}}.top>.card{{grid-area:card}}
@media (max-width:880px){{.top{{grid-template-columns:1fr;grid-template-areas:"intro" "card" "art";row-gap:28px}}}}
.badge{{display:inline-flex;align-items:center;gap:8px;border:1.5px solid var(--ink);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:500;margin:0}}
.badge i{{width:8px;height:8px;border-radius:99px;background:var(--accent)}}
h1{{margin:16px 0 0;font-weight:300;font-size:clamp(40px,5.4vw,70px);line-height:1.02;letter-spacing:-.035em}}h1 span{{color:var(--accent)}}
.lead{{margin:16px 0 0;font-size:19px;line-height:1.5;color:var(--muted);max-width:540px}}
.perks{{list-style:none;margin:22px 0 0;padding:0;display:grid;gap:12px}}
.perks li{{display:flex;gap:12px;align-items:flex-start;font-size:17px;line-height:1.4}}
.perks li::before{{content:"";flex:0 0 auto;width:22px;height:22px;margin-top:1px;border-radius:99px;background:var(--accent) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 12.5l4 4 8-9' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/16px no-repeat}}
.perks small{{display:block;color:var(--muted);font-size:14px}}.perks code{{font:inherit;color:var(--ink);background:var(--tint);padding:1px 6px;border-radius:6px}}
.art{{width:min(460px,100%);margin:24px auto 0}}
.ill{{width:100%;height:auto;overflow:visible}}.ill *{{fill:none;stroke:var(--ink);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
.ill .soft,.ill .wingp{{fill:var(--soft)}}.ill .accent,.ill .hat,.ill .tie{{fill:var(--accent)}}.ill .paper,.ill .fillbg,.ill .skin,.ill .bib,.ill .tool,.ill .case{{fill:var(--bg)}}
.ill .yellow{{fill:#FFC93D}}.ill .eyes{{stroke-width:4}}.ill .cross{{stroke:var(--accent);stroke-width:3}}.ill .umb{{fill:var(--soft)}}.ill .shades{{fill:var(--ink)}}
.ill .links path{{stroke:var(--accent);stroke-dasharray:6 7;stroke-width:2}}.ill .dot{{fill:var(--accent);stroke:none}}
.ill text{{stroke:none;fill:var(--ink)}}.ill .h{{font:600 13px 'Hanken Grotesk',sans-serif;letter-spacing:2px}}.ill .s{{font:400 12px 'Hanken Grotesk',sans-serif;fill:var(--muted)}}
.ill .wing{{transform-box:fill-box;animation:flap .3s ease-in-out infinite alternate}}.ill .wl{{transform-origin:100% 50%}}.ill .wr{{transform-origin:0% 50%;animation-name:flapr}}
@keyframes flap{{to{{transform:rotate(-16deg) scaleY(.85)}}}}@keyframes flapr{{to{{transform:rotate(16deg) scaleY(.85)}}}}
.card{{border:1.5px solid var(--ink);border-radius:24px;padding:clamp(18px,3vw,28px);background:var(--bg)}}
.card h2{{margin:0;font-size:24px;font-weight:500;letter-spacing:-.01em}}.card .sub{{margin:6px 0 0;color:var(--muted)}}
form{{display:grid;gap:12px;margin-top:18px}}
label.f{{display:grid;gap:6px;font-size:14px;font-weight:500}}
.f input,.f select{{min-height:50px;border:1.5px solid var(--ink);border-radius:14px;padding:0 14px;font:400 17px 'Hanken Grotesk',sans-serif;background:var(--bg);color:var(--ink);width:100%}}
.f input:focus,.f select:focus{{outline:none;box-shadow:0 0 0 4px var(--soft)}}
.slug{{display:flex;align-items:center;border:1.5px solid var(--ink);border-radius:14px;overflow:hidden;min-height:50px}}
.slug span{{padding:0 2px 0 14px;color:var(--muted);font-size:16px;white-space:nowrap}}.slug input{{border:0;min-height:48px;padding:0 14px 0 0;border-radius:0}}
.slug:focus-within{{box-shadow:0 0 0 4px var(--soft)}}.slug input:focus{{box-shadow:none}}
.hint{{font-size:13px;font-weight:400;color:var(--muted);min-height:18px}}.hint.ok{{color:#2E9E62}}.hint.bad{{color:#c0392b}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}@media (max-width:420px){{.row{{grid-template-columns:1fr}}}}
fieldset{{border:0;padding:0;margin:0;display:grid;gap:8px}}legend{{font-size:14px;font-weight:500;margin-bottom:6px}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}.chips label{{position:relative}}
.chips input{{position:absolute;opacity:0;pointer-events:none}}
.chips span{{display:inline-flex;align-items:center;min-height:38px;padding:0 13px;border:1.5px solid var(--line);border-radius:999px;font-size:14px;cursor:pointer;user-select:none}}
.chips input:checked+span{{border-color:var(--ink);background:var(--ink);color:var(--bg)}}.chips input:focus-visible+span{{box-shadow:0 0 0 4px var(--soft)}}
.consent{{display:flex;gap:10px;font-size:13px;color:var(--muted);line-height:1.45}}.consent input{{width:20px;height:20px;margin-top:1px;accent-color:var(--accent);flex:0 0 auto}}.consent a{{color:inherit}}
.primary{{min-height:54px;border:0;border-radius:999px;background:var(--accent);color:#fff;font:600 17px 'Hanken Grotesk',sans-serif;cursor:pointer}}.primary:disabled{{opacity:.4;cursor:not-allowed}}
.err{{margin:0;color:#c0392b;font-size:14px}}.fine{{margin:0;font-size:12px;color:var(--muted)}}
.done{{display:none;flex-direction:column;gap:14px}}.done.on{{display:flex}}.done h2{{font-size:28px;font-weight:400}}
.reserved{{border:1.5px dashed var(--ink);border-radius:14px;padding:12px 14px;font-size:17px}}.reserved b{{color:var(--accent)}}
section.band{{margin-top:clamp(48px,8vw,88px)}}section.band>h2{{font-weight:300;font-size:clamp(30px,3.6vw,44px);letter-spacing:-.03em;margin:0 0 8px}}
section.band>p{{margin:0 0 22px;color:var(--muted);font-size:17px;max-width:620px}}
.steps{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}}
.steps li{{border:1.5px solid var(--ink);border-radius:20px;padding:22px}}.steps b{{display:inline-grid;place-items:center;width:32px;height:32px;border-radius:99px;background:var(--accent);color:#fff;font-weight:600}}
.steps h3{{margin:12px 0 6px;font-size:20px;font-weight:500}}.steps p{{margin:0;color:var(--muted);line-height:1.5}}
.ex{{position:relative;border:1.5px solid var(--ink);border-radius:24px;overflow:hidden}}
.ex .tag{{position:absolute;top:14px;right:14px;background:var(--ink);color:var(--bg);font-size:12px;font-weight:600;letter-spacing:1.5px;padding:5px 10px;border-radius:999px}}
.ex .cover{{height:110px;background:var(--tint);border-bottom:1.5px solid var(--ink);background-image:radial-gradient(var(--soft) 1.5px,transparent 1.5px);background-size:16px 16px}}
.ex .head{{display:flex;gap:16px;align-items:flex-end;padding:0 22px;margin-top:-34px;flex-wrap:wrap}}
.ex .av{{width:72px;height:72px;border-radius:20px;border:1.5px solid var(--ink);background:var(--bg);display:grid;place-items:center;font:600 24px 'Hanken Grotesk';color:var(--accent)}}
.ex h3{{margin:0;font-size:26px;font-weight:500;letter-spacing:-.02em}}.ex .url{{color:var(--muted);font-size:14px}}
.ex .btns{{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap;padding-bottom:4px}}
.ex .btns span{{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border-radius:999px;border:1.5px solid var(--ink);font-weight:600;font-size:14px}}.ex .btns span.p{{background:var(--accent);border-color:var(--accent);color:#fff}}
.ex .body{{display:grid;grid-template-columns:1.2fr 1fr;gap:22px;padding:20px 22px 24px}}@media (max-width:760px){{.ex .body{{grid-template-columns:1fr}}}}
.ex h4{{margin:0 0 8px;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);font-weight:600}}
.ex .rules{{margin:0;padding:0;list-style:none;display:grid;gap:8px}}.ex .rules li{{background:var(--tint);border-radius:12px;padding:10px 12px;font-size:15px;line-height:1.4}}
.ex .stats{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.ex .stats div{{border:1.5px solid var(--line);border-radius:14px;padding:10px 12px}}.ex .stats b{{display:block;font-size:20px;font-weight:500}}.ex .stats small{{color:var(--muted);font-size:13px}}
.faq{{max-width:760px}}.faq details{{border-top:1.5px solid var(--line);padding:16px 0}}.faq summary{{cursor:pointer;font-size:18px;font-weight:500;list-style:none}}.faq summary::-webkit-details-marker{{display:none}}
.faq summary::after{{content:"+";float:right;color:var(--accent);font-size:22px;line-height:1}}.faq details[open] summary::after{{content:"–"}}.faq p{{margin:10px 0 0;color:var(--muted);line-height:1.55}}
.foot{{max-width:1120px;margin:0 auto;padding:0 clamp(16px,4vw,48px) 40px;font-size:14px}}.foot a{{color:var(--muted);margin-right:16px}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style></head><body>
<header><a class="logo" href="/" aria-label="Scoo home">{mark}<span>scoo</span></a><a class="pill" href="/pros">I'm a pro</a></header>
<main>
<div class="top">
  <section class="intro">
    <p class="badge"><i></i>For networks, brokers and trade groups</p>
    <h1>Turn your network into <span>an exchange.</span></h1>
    <p class="lead">Give your pros and lead sources their own home on Scoo. You set the rules, Scoo runs the matching, calls and payouts, and you earn on every match.</p>
    <ul class="perks">
      <li><span>Your own page and link<small>A home for your members at <code>scoo.app/x/yourname</code>, under your name.</small></span></li>
      <li><span>Rules in plain English<small>"Emergency plumbing in Dallas goes to members who answer fastest." Scoo turns it into a rule and tests it.</small></span></li>
      <li><span>Earn on every match<small>You set your fee. Scoo runs the money, so you never chase an invoice.</small></span></li>
      <li><span>Free tools for your members<small>Every pro gets Scoo's AI receptionist, so your network misses fewer calls.</small></span></li>
    </ul>
  </section>
  <div class="art">{HUB}</div>
  <section class="card" aria-labelledby="apply-title">
    <div id="apply">
      <h2 id="apply-title">Apply to be a founding operator</h2>
      <p class="sub">We're opening exchanges city by city. Founding operators go first.</p>
      <form id="f" novalidate>
        <label class="f">Exchange name<div class="slug"><span>scoo.app/x/</span><input id="slug" autocomplete="off" autocapitalize="off" spellcheck="false" maxlength="32" placeholder="dfw-home-pros" required></div><span class="hint" id="slughint">Lowercase letters, numbers and dashes.</span></label>
        <div class="row">
          <label class="f">Your name<input id="name" autocomplete="name" maxlength="80" required placeholder="Alex Rivera"></label>
          <label class="f">Company or network<input id="org" autocomplete="organization" maxlength="120" required placeholder="DFW Home Pros"></label>
        </div>
        <fieldset><legend>What does your network cover?</legend><div class="chips" id="trades">{''.join(f'<label><input type="checkbox" value="{t}"><span>{t}</span></label>' for t in TRADES)}</div></fieldset>
        <div class="row">
          <label class="f">Main ZIP you serve<input id="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5" required placeholder="75201"></label>
          <label class="f">Pros or members today<select id="size">{''.join(f'<option>{s}</option>' for s in SIZES)}</select></label>
        </div>
        <div class="row">
          <label class="f">Calls or leads a month<select id="volume">{''.join(f'<option>{v}</option>' for v in VOLUMES)}</select></label>
          <label class="f">Mobile or email<input id="contact" autocomplete="on" autocapitalize="off" spellcheck="false" maxlength="160" required placeholder="you@network.com"></label>
        </div>
        <label class="consent"><input type="checkbox" id="ok" required><span>{CONSENT}</span></label>
        <div id="ts"></div>
        <button class="primary" id="go" disabled>Apply and reserve my name</button>
        <p class="fine">Free to apply. We'll walk you through pricing before anything goes live.</p>
      </form>
    </div>
    <div class="done" id="done" aria-live="polite">
      <h2 id="d-title"></h2>
      <div class="reserved">Your exchange: <b id="d-url"></b></div>
      <p class="sub" id="d-lead"></p>
      <p class="sub">While you wait, tell your pros: they can claim Scoo's free AI receptionist today at <a href="/pros">scoo.app/pros</a>.</p>
    </div>
  </section>
</div>

<section class="band" aria-labelledby="ex-title">
  <h2 id="ex-title">What your exchange looks like</h2>
  <p>Your page, your rules, your members. This is an example, not a real exchange.</p>
  <div class="ex" aria-label="Example exchange page">
    <span class="tag">EXAMPLE</span>
    <div class="cover"></div>
    <div class="head"><div class="av">DH</div><div><h3>DFW Home Pros</h3><div class="url">scoo.app/x/dfw-home-pros · Plumbing, HVAC, Electrical · Dallas–Fort Worth</div></div>
      <div class="btns"><span class="p">Join as a pro</span><span>Sell calls here</span></div></div>
    <div class="body">
      <div><h4>House rules</h4><ul class="rules">
        <li>Emergency calls go first to members who answered 9 in 10 calls this month.</li>
        <li>Members take up to 8 calls a day, 7am to 9pm.</li>
        <li>New members get one call a day for their first week.</li>
        <li>Calls under 60 seconds are free for the member.</li></ul></div>
      <div><h4>This exchange</h4><div class="stats">
        <div><b>Members</b><small>pros who take calls</small></div><div><b>Sources</b><small>who send calls in</small></div>
        <div><b>Answer time</b><small>average, today</small></div><div><b>Jobs</b><small>matched this week</small></div></div>
        <p class="fine" style="margin-top:10px">Live numbers appear here once the exchange opens.</p></div>
    </div>
  </div>
</section>

<section class="band" aria-labelledby="how-title">
  <h2 id="how-title">How it works</h2>
  <ol class="steps">
    <li><b>1</b><h3>Apply</h3><p>Reserve your exchange name and tell us about your network.</p></li>
    <li><b>2</b><h3>Set your rules</h3><p>Who gets which calls, when, and for how much. In plain English, and we test them before you go live.</p></li>
    <li><b>3</b><h3>Bring your network</h3><p>Invite your pros and sources with your link. They get the free receptionist; you get a home for them.</p></li>
    <li><b>4</b><h3>Earn on every match</h3><p>Scoo runs the calls and the payouts. You see every match and every dollar, live.</p></li>
  </ol>
</section>

<section class="band faq" aria-labelledby="faq-title">
  <h2 id="faq-title">Questions</h2>
  <details><summary>Who is this for?</summary><p>Anyone who already connects customers with pros: pay-per-call and lead networks, brokers, agencies, trade associations, franchise owners and referral groups.</p></details>
  <details><summary>What does it cost?</summary><p>Applying is free. Once your exchange is live, you set your own fee on each match and Scoo takes a platform fee. We'll agree pricing with you before anything goes live.</p></details>
  <details><summary>Can I bring my existing buyers and sources?</summary><p>Yes. That's the point: your exchange runs on your relationships. Scoo handles the routing, calls, consent records and payouts.</p></details>
  <details><summary>Can my members belong to other exchanges too?</summary><p>Yes. A pro has one Scoo account and can join any exchange that accepts them, so good members build a reputation across Scoo.</p></details>
</section>
</main>
<footer class="foot"><a href="/terms">Terms</a><a href="/privacy">Privacy</a></footer>
<script>
(()=>{{
const $=s=>document.querySelector(s);
const slug=$('#slug'),hint=$('#slughint'),go=$('#go'),ok=$('#ok'),f=$('#f');
let slugOk=false,slugTimer=null,tsNeeded=false,tsToken=null;
const clean=v=>v.toLowerCase().replace(/[^a-z0-9-]+/g,'-').replace(/-+/g,'-').replace(/^-/,'').slice(0,32);
const contactOk=v=>v.includes('@')?/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(v.trim()):v.replace(/\\D/g,'').length>=10;
const chk=()=>go.disabled=!(slugOk&&$('#name').value.trim()&&$('#org').value.trim()&&/^\\d{{5}}$/.test($('#zip').value.trim())&&contactOk($('#contact').value)&&ok.checked&&(!tsNeeded||tsToken));
['#name','#org','#zip','#contact'].forEach(s=>$(s).addEventListener('input',chk));ok.addEventListener('change',chk);
// suggest a name from the company until they type their own
let typed=false;$('#org').addEventListener('input',()=>{{if(!typed){{slug.value=clean($('#org').value).replace(/-$/,'');checkSlug();}}}});
slug.addEventListener('input',()=>{{typed=true;const c=clean(slug.value);if(c!==slug.value)slug.value=c;checkSlug();}});
function checkSlug(){{slugOk=false;chk();clearTimeout(slugTimer);const v=slug.value.replace(/-$/,'');
  if(v.length<3){{hint.className='hint';hint.textContent='At least 3 characters.';return;}}
  hint.className='hint';hint.textContent='Checking…';
  slugTimer=setTimeout(async()=>{{
    try{{const r=location.protocol==='file:'?{{available:true}}:await (await fetch('/api/exchange-name?s='+encodeURIComponent(v))).json();
      if(slug.value.replace(/-$/,'')!==v)return;
      slugOk=!!r.available;hint.className='hint '+(slugOk?'ok':'bad');hint.textContent=slugOk?`scoo.app/x/${{v}} is available`:(r.reason||'That name is taken. Try another.');}}
    catch(_){{hint.className='hint bad';hint.textContent='Could not check right now.';}}chk();}},350);}}
if(location.protocol!=='file:')fetch('/api/config').then(r=>r.json()).then(c=>{{if(!c.turnstileSiteKey)return;tsNeeded=true;chk();
  window.onTs=()=>turnstile.render('#ts',{{sitekey:c.turnstileSiteKey,theme:'auto',callback:t=>{{tsToken=t;chk();}},'expired-callback':()=>{{tsToken=null;chk();}}}});
  const sc=document.createElement('script');sc.src='https://challenges.cloudflare.com/turnstile/v0/api.js?onload=onTs&render=explicit';sc.async=true;document.head.appendChild(sc);}}).catch(()=>{{}});
let ref=null;try{{const q=new URLSearchParams(location.search).get('ref');if(q)localStorage.setItem('scoo_op_ref',q);ref=localStorage.getItem('scoo_op_ref');}}catch(_){{}}
f.onsubmit=async e=>{{e.preventDefault();if(go.disabled)return;go.disabled=true;go.textContent='Sending…';
  const body={{slug:slug.value.replace(/-$/,''),name:$('#name').value.trim(),org:$('#org').value.trim(),trades:[...document.querySelectorAll('#trades input:checked')].map(i=>i.value),
    zip:$('#zip').value.trim(),size:$('#size').value,volume:$('#volume').value,contact:$('#contact').value.trim(),consent:ok.checked,consentText:$('.consent span').textContent,ref,turnstile:tsToken}};
  try{{
    const r=location.protocol==='file:'?{{slug:body.slug,place:'Dallas, TX',areaLabel:'the Dallas area'}}:await (async()=>{{const res=await fetch('/api/operators',{{method:'POST',headers:{{'content-type':'application/json'}},body:JSON.stringify(body)}});const j=await res.json();if(!res.ok)throw new Error(j.error||'Something went wrong');return j;}})();
    $('#d-title').textContent=`Thanks, ${{body.name.split(' ')[0]}}. You're in the founding round.`;
    $('#d-url').textContent='scoo.app/x/'+r.slug;
    $('#d-lead').textContent=`Your name is reserved. We're onboarding founding operators city by city, starting with ${{r.areaLabel||'your area'}}, and we'll be in touch to set up your rules.`;
    $('#apply').hidden=true;$('#done').classList.add('on');
  }}catch(err){{go.textContent='Apply and reserve my name';if(window.turnstile&&tsNeeded){{turnstile.reset('#ts');tsToken=null;}}chk();
    let m=f.querySelector('.err');if(!m){{m=document.createElement('p');m.className='err';m.setAttribute('role','alert');f.insertBefore(m,go);}}m.textContent=err.message+'. Please try again.';}}}};
}})();
</script></body></html>'''
open('exchanges-start.html', 'w').write(page)
print('ok')
