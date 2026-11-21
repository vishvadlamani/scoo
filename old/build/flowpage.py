# Builds request.html: the sign-up flow as its own page, one step per screen, each with a line-art
# illustration in the same style as the street. Pre-launch: it ends on the city waitlist and referrals.
import json, re
def place(svg,x,y,w,h):
    return re.sub(r'^<svg ', f'<svg x="{x}" y="{y}" width="{w}" height="{h}" ', svg.strip(), count=1)
pros = json.load(open('_pros.json'))
mark = open('_mark.svg').read().replace('class="mark"', 'class="mark" ')

# ---- illustrations (viewBox 0 0 320 220; ink lines, coral/soft accents) ----
ILL_NEED = '''<svg viewBox="0 0 320 220" aria-hidden="true" class="ill">
<rect x="112" y="18" width="96" height="184" rx="18"/><path d="M146 30 h28"/><circle cx="160" cy="188" r="5"/>
<g class="pop" style="--i:0"><path class="soft" d="M128 58 h64 a10 10 0 0 1 10 10 v18 a10 10 0 0 1 -10 10 h-40 l-12 10 v-10 h-12 a10 10 0 0 1 -10 -10 v-18 a10 10 0 0 1 10 -10 Z"/><path d="M134 74 h40 M134 84 h24"/></g>
<g class="pop" style="--i:1"><path d="M136 108 h56 a10 10 0 0 1 10 10 v14 a10 10 0 0 1 -10 10 h-10 v10 l-12 -10 h-34 a10 10 0 0 1 -10 -10 v-14 a10 10 0 0 1 10 -10 Z"/><circle class="dot" cx="150" cy="125" r="3"/><circle class="dot" cx="162" cy="125" r="3" style="--i:1"/><circle class="dot" cx="174" cy="125" r="3" style="--i:2"/></g>
<path class="spark" d="M236 52 l6 -10 M246 66 l12 -4 M232 40 l-2 -12"/><path class="spark" d="M84 150 l-10 6 M80 136 l-12 -2"/>
</svg>'''

ILL_ZIP = '''<svg viewBox="0 0 320 220" aria-hidden="true" class="ill">
<path d="M10 196 H310"/><path d="M10 206 H310" class="dash"/>
<rect x="34" y="132" width="62" height="64"/><path d="M28 132 L65 104 L102 132"/><rect x="56" y="160" width="18" height="36"/>
<rect x="118" y="118" width="84" height="78"/><path d="M114 118 h92"/><rect x="128" y="132" width="20" height="22"/><rect x="172" y="132" width="20" height="22" class="lit"/><rect x="150" y="164" width="20" height="32"/>
<rect x="224" y="138" width="62" height="58"/><path d="M218 138 L255 112 L292 138"/><rect x="246" y="164" width="18" height="32"/>
<g class="pin"><path class="accent" d="M160 14 c-20 0 -32 14 -32 30 c0 22 32 52 32 52 s32 -30 32 -52 c0 -16 -12 -30 -32 -30 Z"/><circle cx="160" cy="44" r="10" class="paper"/></g>
<ellipse class="shadow" cx="160" cy="112" rx="16" ry="4"/>
</svg>'''

PROPS = {
 'plumber': '<path d="M214 70 h40 v14 h-14 v10"/><path d="M214 64 v26"/><path class="drop" d="M240 100 q5 8 0 12 q-5 -4 0 -12 Z"/><path class="drop" style="--i:1" d="M240 100 q5 8 0 12 q-5 -4 0 -12 Z"/><path d="M222 150 h36 l-4 30 h-28 Z"/><path class="water" d="M226 156 h28"/>',
 'electrician': '<circle cx="242" cy="86" r="22" class="glow"/><path d="M234 108 h16 v12 h-16 Z M236 114 h12"/><path class="spark" d="M242 52 v-12 M268 62 l10 -8 M216 62 l-10 -8 M276 88 h12 M208 88 h-12"/>',
 'lawyer': '<rect x="214" y="66" width="56" height="74" rx="4" class="paper"/><path d="M224 82 h36 M224 94 h36 M224 106 h24"/><path class="accent-line" d="M226 124 q8 -10 14 0 q6 10 14 -2"/>',
 'insurance': '<path d="M206 152 h64 l-8 -20 h-44 Z"/><rect x="200" y="152" width="76" height="18" rx="6"/><circle cx="218" cy="172" r="8" class="paper"/><circle cx="258" cy="172" r="8" class="paper"/><path class="rain" d="M216 60 l-4 10 M240 50 l-4 10 M264 60 l-4 10"/>',
 'doctor': '<path class="accent" d="M242 132 s-30 -18 -30 -38 a16 16 0 0 1 30 -8 a16 16 0 0 1 30 8 c0 20 -30 38 -30 38 Z"/><path d="M220 100 h12 l6 -10 l8 20 l6 -10 h14" class="paper-line"/>',
 'mover': '<rect x="212" y="112" width="58" height="48" class="soft"/><path d="M212 126 h58 M241 112 v14"/><rect x="226" y="80" width="40" height="32" class="soft"/><path d="M226 92 h40"/>',
}
QUESTIONS = {
 'plumber': ('Is water leaking right now?', ["Yes, it's urgent", 'No, it can wait']),
 'electrician': ('Is anything sparking or smoking?', ['Yes', 'No']),
 'lawyer': ('What kind of help do you need?', ['Divorce or family', 'Injury', 'Business', 'Something else']),
 'insurance': ('What do you want to insure?', ['Car', 'Home', 'Life', 'Health']),
 'doctor': ('Is this a medical emergency?', ['Yes', 'No']),
 'mover': ('When do you need them?', ['Today', 'This week', 'Later']),
 'pro': ('How soon do you need help?', ['Right now', 'This week', 'Just planning ahead']),
}
ILL_Q = {k: f'<svg viewBox="0 0 320 220" aria-hidden="true" class="ill"><path d="M10 206 H310"/>{place(pros[k],40,40,132,170)}<g>{PROPS[k]}</g></svg>' for k in PROPS}

ILL_ASK = '''<svg viewBox="0 0 320 220" aria-hidden="true" class="ill">
<rect x="96" y="22" width="128" height="180" rx="12"/><rect x="134" y="12" width="52" height="22" rx="8" class="soft"/>
<g class="row" style="--i:0"><rect x="116" y="56" width="20" height="20" rx="5"/><path class="tick" d="M120 66 l5 5 l9 -11"/><path d="M148 62 h56 M148 72 h36"/></g>
<g class="row" style="--i:1"><rect x="116" y="96" width="20" height="20" rx="5"/><path class="tick" d="M120 106 l5 5 l9 -11"/><path d="M148 102 h56 M148 112 h28"/></g>
<g class="row" style="--i:2"><rect x="116" y="136" width="20" height="20" rx="5"/><path d="M148 142 h56 M148 152 h40"/></g>
<g class="pencil"><path class="soft" d="M236 168 l34 -60 l14 8 l-34 60 Z"/><path d="M236 168 l-4 18 l18 -10"/><path d="M266 116 l14 8"/></g>
<path class="spark" d="M70 70 l-12 -6 M66 92 h-14 M240 40 l8 -10"/>
</svg>'''
ILL_SEARCH = """<svg viewBox="0 0 320 220" aria-hidden="true" class="ill map">
<defs><clipPath id="mapclip"><rect x="20" y="10" width="280" height="200" rx="22"/></clipPath></defs>
<g clip-path="url(#mapclip)"><g class="zoom">
<path class="water" d="M-40 170 C40 140 90 200 160 186 S260 150 360 176"/>
<path class="road" d="M-40 60 H360 M-40 120 H360 M60 -40 V260 M140 -40 V260 M220 -40 V260 M-40 -10 L360 230"/>
<path class="lane" d="M-40 90 H360 M100 -40 V260 M180 -40 V260 M260 -40 V260 M-40 30 H360 M-40 150 H360"/>
<rect class="park" x="148" y="68" width="64" height="44" rx="6"/>
<path class="tree-dot" d="M162 82 h.1 M178 94 h.1 M196 80 h.1 M188 102 h.1"/>
<rect class="blk" x="68" y="68" width="64" height="44" rx="4"/><rect class="blk" x="228" y="68" width="64" height="44" rx="4"/>
<rect class="blk" x="68" y="8" width="64" height="44" rx="4"/><rect class="blk" x="148" y="8" width="64" height="44" rx="4"/>
<rect class="blk" x="228" y="128" width="64" height="30" rx="4"/><rect class="blk" x="-12" y="68" width="64" height="44" rx="4"/>
</g></g>
<rect x="20" y="10" width="280" height="200" rx="22" class="frame"/>
<g class="radar"><circle cx="180" cy="104" r="10" class="ring" style="--i:0"/><circle cx="180" cy="104" r="10" class="ring" style="--i:1"/><circle cx="180" cy="104" r="10" class="ring" style="--i:2"/></g>
<g class="sweep"><path d="M180 104 L180 28 A76 76 0 0 1 234 50 Z" class="beam"/></g>
<g class="pin"><path class="accent" d="M180 52 c-12 0 -20 9 -20 19 c0 14 20 33 20 33 s20 -19 20 -33 c0 -10 -8 -19 -20 -19 Z"/><circle cx="180" cy="71" r="6.5" class="paper"/></g>
</svg>"""
ILL_PHONE = f'''<svg viewBox="0 0 320 220" aria-hidden="true" class="ill">
<g class="ring"><rect x="116" y="20" width="88" height="170" rx="16"/><path d="M146 32 h28"/>
{place(mark.replace('class="mark" ',''),124,62,72,52)}
<rect x="134" y="140" width="52" height="22" rx="11" class="accent"/></g>
<path class="buzz" d="M96 70 q-10 20 0 40 M80 60 q-16 30 0 60 M224 70 q10 20 0 40 M240 60 q16 30 0 60"/>
</svg>'''

ILL_DONE = '''<svg viewBox="0 0 320 220" aria-hidden="true" class="ill">
<path d="M10 196 H310"/>
<rect x="10" y="96" width="66" height="100"/><path d="M4 96 h78"/><rect x="20" y="110" width="18" height="24"/><rect x="48" y="110" width="18" height="24" class="lit"/><path class="soft" d="M8 150 h70 l-8 14 h-54 Z"/><rect x="22" y="168" width="20" height="28"/>
<rect x="240" y="110" width="66" height="86"/><path d="M234 110 L273 84 L312 110"/><rect x="252" y="124" width="18" height="22"/><rect x="280" y="124" width="18" height="22"/><rect x="264" y="164" width="18" height="32"/>
<g class="wave">PRO</g>
<g class="bubble-s"><rect x="128" y="34" width="64" height="28" rx="14" class="paper"/><text x="160" y="53" text-anchor="middle">Soon!</text></g>
<path class="spark" d="M112 44 l-8 -8 M210 44 l8 -8"/>
</svg>'''

steps_html = f'''
<section class="step" data-step="need">
  <div class="art">{ILL_NEED}</div>
  <h1>What do you need?</h1>
  <p class="lead">Describe it in your own words. A leaking pipe, a car insurance quote, a lawyer by Friday.</p>
  <form class="field" id="f-need"><label class="vh" for="need">What do you need?</label>
    <input id="need" autocomplete="off" placeholder="My water heater is leaking…" required>
    <button class="go" aria-label="Continue">{'<svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6"/></svg>'}</button></form>
</section>
<section class="step" data-step="zip" hidden>
  <div class="art">{ILL_ZIP}</div>
  <h1>Where are you?</h1>
  <p class="lead" id="zip-lead">We'll find a pro near you.</p>
  <form class="field" id="f-zip"><label class="vh" for="zip">ZIP code</label>
    <input id="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5" placeholder="ZIP code" required pattern="[0-9]{{5}}">
    <button class="go" aria-label="Continue"><svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6"/></svg></button></form>
</section>
<section class="step" data-step="q" hidden>
  <div class="art" id="q-art">{ILL_ASK}</div>
  <h1 id="q-title"></h1>
  <p class="lead">A quick question so the right pro calls you.</p>
  <div class="choices" id="q-choices"></div>
</section>
<section class="step" data-step="phone" hidden>
  <div class="art">{ILL_SEARCH}</div>
  <p class="placechip" id="placechip" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.3-7-11.5A7 7 0 0 1 19 9.5C19 14.7 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg><span id="pc-text"></span></p>
  <div class="searchbox" id="searchbox">
  <h1 id="s-title">Looking up your area…</h1>
  <ul class="checks" id="s-checks" aria-live="polite">
    <li data-k="area"><i></i><span>Finding <b id="s-zip"></b> on the map</span></li>
    <li data-k="pros"><i></i><span id="s-pros">Checking Scoo coverage</span></li>
    <li data-k="launch"><i></i><span id="s-launch">Checking when Scoo opens near you</span></li>
  </ul>
  </div>
  <div class="callwrap" id="callwrap" hidden>
    <h2 id="n-title">Scoo is coming to your area</h2>
    <p class="lead" id="n-lead">Get on the early list and be first to get a pro when we open.</p>
    <form class="stack" id="f-phone">
      <label class="vh" for="tel">Mobile number or email</label><input id="tel" type="text" autocomplete="on" autocapitalize="off" spellcheck="false" placeholder="Mobile number or email" required>
      <label class="consent"><input type="checkbox" id="ok" required><span>I agree to Scoo's <a href="/terms" target="_blank" rel="noopener">terms</a>. No spam. Unsubscribe anytime.</span></label>
      <div id="ts"></div>
      <button class="primary" id="save" disabled>Save my spot</button></form>
  </div>
</section>
<section class="step" data-step="done" hidden>
  <div class="art" id="done-art"></div>
  <h1 id="done-title"></h1>
  <p class="lead" id="done-lead"></p>
  <a class="primary letmein" href="/app" id="letmein">Let me in <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"/></svg></a>
  <div class="meter" aria-label="Progress to launch"><i></i></div>
  <div class="tabs" role="tablist"><button role="tab" aria-selected="true" data-t="f">Know a friend?</button><button role="tab" aria-selected="false" data-t="p">Know a pro?</button></div>
  <div class="tab" data-p="f"><p>You each get <b>$10 Scoo credit</b> when they join, and <span class="cityname"></span> opens sooner.</p>
    <div class="link"><span id="flink"></span><button type="button" class="cp">Copy</button></div>
    <div class="share"><button type="button">WhatsApp</button><button type="button">Text</button><button type="button">Facebook</button><button type="button">Email</button></div></div>
  <div class="tab" data-p="p" hidden><p>Know a great pro? Send them your link: they get Scoo's AI receptionist free, so they never miss a call. You get <b>$25 credit</b> when they join and take their first job.</p>
    <div class="link"><span id="plink"></span><button type="button" class="cp">Copy</button></div>
    <div class="share"><button type="button">WhatsApp</button><button type="button">Text</button><button type="button">Email</button><button type="button">More</button></div>
    <p class="fine">You send the invite yourself. Scoo never contacts a pro you mention unless they sign up.</p></div>
  <p class="fine">$10 per friend · $25 per pro · up to $100. Credit applies to requests after launch. Not redeemable for cash.</p>
</section>'''

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tell Scoo what you need</title>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#FFFFFF;--ink:#111111;--muted:#55595f;--accent:#FF6B4A;--soft:#FFD9CF;--glow:#FFE7A3;--line:#e7e5e0}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0E0E10;--ink:#EDEDED;--muted:#a7abb3;--accent:#FF7A5C;--soft:#4A2620;--glow:#5A4A1C;--line:#2a2a2e}}}}
:root[data-theme="dark"]{{--bg:#0E0E10;--ink:#EDEDED;--muted:#a7abb3;--accent:#FF7A5C;--soft:#4A2620;--glow:#5A4A1C;--line:#2a2a2e}}
*{{box-sizing:border-box}}html,body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Hanken Grotesk',system-ui,sans-serif}}
.vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
header{{display:flex;align-items:center;justify-content:space-between;padding:20px clamp(16px,4vw,48px);max-width:1200px;margin:0 auto}}
.logo{{display:inline-flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-size:26px;letter-spacing:-.02em}}
.logo .mark{{height:36px;width:auto;color:var(--ink)}}.logo .mouth{{stroke:var(--accent)}}
.back{{min-height:44px;padding:0 16px;border:1.5px solid var(--ink);border-radius:999px;background:var(--bg);color:var(--ink);font:500 15px inherit;cursor:pointer;font-family:inherit}}
.back[disabled]{{visibility:hidden}}
.dots{{display:flex;gap:8px;justify-content:center;margin:4px 0 0}}.dots i{{width:28px;height:4px;border-radius:99px;background:var(--line);transition:background .3s}}.dots i.on{{background:var(--accent)}}
main{{max-width:560px;margin:0 auto;padding:12px 20px 48px}}
.step{{display:flex;flex-direction:column;align-items:center;text-align:center;gap:16px;animation:in .45s cubic-bezier(.3,.8,.3,1)}}
.step[hidden]{{display:none}}
@keyframes in{{from{{opacity:0;transform:translateY(14px)}}}}
.art{{width:min(340px,86vw)}}
.ill{{width:100%;height:auto;overflow:visible}}.ill *{{fill:none;stroke:var(--ink);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
.ill .soft,.ill .wingp{{fill:var(--soft)}}.ill .accent{{fill:var(--accent);stroke:var(--ink)}}.ill .paper,.ill .fillbg,.ill .skin,.ill .mouth{{fill:var(--bg)}}.ill .lit{{fill:var(--glow)}}
.ill .yellow{{fill:#FFC93D}}.ill .blue{{fill:#7FB2FF}}.ill .shades{{fill:var(--ink)}}.ill .eyes{{stroke-width:4}}.ill .cross{{stroke:var(--accent);stroke-width:3}}.ill .band{{stroke:var(--accent);stroke-width:5}}.ill .thick{{stroke-width:5}}
.ill .dash{{stroke-dasharray:14 14}}.ill .shadow{{fill:var(--line);stroke:none}}.ill .glow{{fill:var(--glow)}}.ill .accent-line{{stroke:var(--accent)}}.ill .paper-line{{stroke:var(--accent)}}
.ill .spark,.ill .rain{{stroke:var(--accent)}}.ill .water{{stroke:#7FB2FF;stroke-width:3}}.ill .drop{{fill:#9EC9FF;animation:drip 1.4s ease-in infinite;animation-delay:calc(var(--i,0)*.7s)}}
.ill text{{stroke:none;fill:var(--ink);font:600 14px 'Hanken Grotesk',sans-serif}}
.ill .signtxt{{stroke:none;fill:var(--accent);font:700 12px 'Hanken Grotesk',sans-serif}}
.ill .wing{{transform-box:fill-box;animation:flap .3s ease-in-out infinite alternate}}.ill .wl{{transform-origin:100% 50%}}.ill .wr{{transform-origin:0% 50%;animation-name:flapr}}
.ill .pop{{animation:pop .5s cubic-bezier(.3,.8,.3,1.3) both;animation-delay:calc(.25s + var(--i)*.45s)}}
.ill .dot{{fill:var(--ink);stroke:none;animation:blink 1s infinite;animation-delay:calc(var(--i,0)*.15s)}}
.ill .pin{{animation:pin .9s cubic-bezier(.3,.8,.3,1.4) both}}.ill .shadow{{animation:shadow .9s ease-out both}}
.ill .ring{{transform-box:fill-box;transform-origin:50% 50%;animation:ring 1.2s ease-in-out infinite}}.ill .buzz{{stroke:var(--accent);animation:buzz 1.2s ease-in-out infinite}}

.ill .row{{animation:pop .4s cubic-bezier(.3,.8,.3,1.3) both;animation-delay:calc(.2s + var(--i)*.35s)}}
.ill .tick{{stroke:var(--accent);stroke-width:3;stroke-dasharray:24;stroke-dashoffset:24;animation:tick .4s ease-out forwards;animation-delay:calc(1.2s + var(--i,0)*.5s)}}
.ill .row:nth-of-type(2) .tick{{animation-delay:1.7s}}
.ill .pencil{{animation:write 1.6s ease-in-out infinite;transform-box:fill-box;transform-origin:0 100%}}
@keyframes tick{{to{{stroke-dashoffset:0}}}}@keyframes write{{50%{{transform:translate(-6px,4px) rotate(-4deg)}}}}
.ill .wave{{animation:hop 1.6s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}}.ill .bubble-s{{animation:pop .5s .5s cubic-bezier(.3,.8,.3,1.3) both}}
@keyframes flap{{to{{transform:rotate(-16deg) scaleY(.85)}}}}@keyframes flapr{{to{{transform:rotate(16deg) scaleY(.85)}}}}
@keyframes pop{{from{{opacity:0;transform:scale(.6)}}}}@keyframes blink{{50%{{opacity:.2}}}}
@keyframes pin{{from{{transform:translateY(-60px);opacity:0}}}}@keyframes shadow{{from{{opacity:0;transform:scale(.3)}}}}
@keyframes drip{{0%{{transform:translateY(0);opacity:0}}20%{{opacity:1}}100%{{transform:translateY(46px);opacity:0}}}}
@keyframes ring{{0%,60%,100%{{transform:rotate(0)}}10%,30%,50%{{transform:rotate(-5deg)}}20%,40%{{transform:rotate(5deg)}}}}
@keyframes buzz{{0%,60%,100%{{opacity:0}}10%,50%{{opacity:1}}}}@keyframes hop{{50%{{transform:translateY(-8px)}}}}
h1{{margin:4px 0 0;font-weight:300;font-size:clamp(32px,5vw,46px);letter-spacing:-.03em;line-height:1.05}}
.lead{{margin:0;color:var(--muted);font-size:17px;line-height:1.5;max-width:440px}}
.field{{display:flex;align-items:center;gap:6px;width:100%;border:1.5px solid var(--ink);border-radius:999px;padding:6px 6px 6px 20px;margin-top:6px}}
.field:focus-within{{box-shadow:0 0 0 4px var(--soft)}}
.field input{{flex:1;min-width:0;border:0;outline:0;background:transparent;color:var(--ink);font:400 18px 'Hanken Grotesk',sans-serif;min-height:48px}}
.go{{display:grid;place-items:center;width:48px;height:48px;border-radius:999px;border:0;background:var(--accent);color:#fff;cursor:pointer}}
.go svg{{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
.choices{{display:grid;grid-template-columns:1fr;gap:10px;width:100%}}
.choices button{{min-height:54px;border:1.5px solid var(--ink);border-radius:16px;background:var(--bg);color:var(--ink);font:500 17px 'Hanken Grotesk',sans-serif;cursor:pointer;text-align:left;padding:0 18px}}
.choices button:hover{{background:var(--soft)}}
.stack{{display:flex;flex-direction:column;gap:12px;width:100%;text-align:left}}
.stack #tel{{min-height:54px;border:1.5px solid var(--ink);border-radius:999px;padding:0 20px;font:400 18px 'Hanken Grotesk',sans-serif;background:var(--bg);color:var(--ink)}}
.consent a{{color:inherit}}.consent{{display:flex;gap:10px;font-size:14px;color:var(--muted);line-height:1.45}}.consent input{{width:20px;height:20px;margin-top:1px;accent-color:var(--accent);flex:0 0 auto}}
.primary{{min-height:54px;border:0;border-radius:999px;background:var(--accent);color:#fff;font:600 17px 'Hanken Grotesk',sans-serif;cursor:pointer}}.primary:disabled{{opacity:.4;cursor:not-allowed}}
.meter{{width:100%;height:8px;border-radius:99px;border:1.5px solid var(--ink);overflow:hidden}}.meter i{{display:block;height:100%;width:0;background:var(--accent);transition:width 1.4s cubic-bezier(.3,.8,.3,1)}}
.tabs{{display:grid;grid-template-columns:1fr 1fr;width:100%;border:1.5px solid var(--ink);border-radius:999px;padding:3px;gap:3px}}
.tabs button{{min-height:42px;border:0;border-radius:999px;background:transparent;color:var(--ink);font:500 15px 'Hanken Grotesk',sans-serif;cursor:pointer}}.tabs button[aria-selected=true]{{background:var(--ink);color:var(--bg)}}
.tab{{display:flex;flex-direction:column;gap:12px;width:100%;text-align:left}}.tab[hidden]{{display:none}}.tab p{{margin:0;line-height:1.45}}
.link{{display:flex;align-items:center;gap:8px;border:1.5px dashed var(--ink);border-radius:14px;padding:8px 12px}}.link span{{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.link button{{flex:0 0 auto;min-height:38px;border-radius:999px;border:1.5px solid var(--ink);background:var(--bg);color:var(--ink);padding:0 14px;font:600 14px 'Hanken Grotesk',sans-serif;cursor:pointer}}
.share{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}}.share button{{min-height:42px;border-radius:999px;border:1.5px solid var(--ink);background:var(--bg);color:var(--ink);font:500 14px 'Hanken Grotesk',sans-serif;cursor:pointer;padding:0 4px}}
@media (max-width:420px){{.share{{grid-template-columns:1fr 1fr}}}}
.err{{margin:0;color:#c0392b;font-size:14px}}

.map .road{{stroke:var(--ink);stroke-width:7;opacity:.14}}.map .lane{{stroke:var(--ink);stroke-width:2;opacity:.12}}
.map .water{{stroke:#9EC9FF;stroke-width:12;opacity:.55}}.map .park{{fill:#DCEFD9;stroke:none}}.map .tree-dot{{stroke:#7BB37A;stroke-width:9}}
.map .blk{{fill:var(--bg);stroke:var(--ink);stroke-width:1.5;opacity:.55}}.map .frame{{fill:none;stroke:var(--ink);stroke-width:2.2}}
.map .zoom{{transform-box:view-box;transform-origin:180px 90px;animation:zoomin 2.6s cubic-bezier(.3,.7,.2,1) both}}
@keyframes zoomin{{from{{transform:scale(.55) translate(-40px,30px)}}to{{transform:scale(1.15)}}}}
.map .pin{{animation:pin .7s 1.6s cubic-bezier(.3,.8,.3,1.4) both}}
.map .ring{{stroke:var(--accent);stroke-width:2;vector-effect:non-scaling-stroke;transform-box:fill-box;transform-origin:center;animation:ring 2.4s ease-out infinite;animation-delay:calc(1.9s + var(--i)*.8s);opacity:0}}
@keyframes ring{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(8);opacity:0}}}}
.map .sweep{{transform-box:view-box;transform-origin:180px 104px;animation:sweep 2.2s linear infinite;animation-delay:.3s}}
.map .beam{{fill:var(--accent);stroke:none;opacity:.12}}
@keyframes sweep{{to{{transform:rotate(360deg)}}}}
.checks{{list-style:none;margin:4px 0 0;padding:0;display:flex;flex-direction:column;gap:12px;width:100%;max-width:360px;text-align:left}}
.checks li{{display:flex;align-items:center;gap:12px;font-size:16px;color:var(--muted);opacity:.35;transition:opacity .3s}}
.checks li.run,.checks li.ok{{opacity:1;color:var(--ink)}}
.checks i{{flex:0 0 auto;width:22px;height:22px;border-radius:99px;border:2px solid var(--line);position:relative}}
.checks li.run i{{border-color:var(--line);border-top-color:var(--accent);animation:spin .7s linear infinite}}
.checks li.ok i{{border-color:var(--accent);background:var(--accent)}}
.checks li.ok i::after{{content:"";position:absolute;left:6px;top:3px;width:5px;height:9px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.callwrap{{width:100%;display:flex;flex-direction:column;align-items:center;gap:12px;animation:rise .55s cubic-bezier(.3,.8,.3,1) both}}
.step[data-step=phone] .art{{transition:width .75s cubic-bezier(.3,.8,.3,1)}}
.step[data-step=phone].notify .art{{width:132px}}
.searchbox{{display:flex;flex-direction:column;align-items:center;gap:16px;width:100%;max-height:420px;overflow:hidden;transition:max-height .6s cubic-bezier(.5,0,.3,1),opacity .3s ease}}
.notify .searchbox{{max-height:0;opacity:0;margin-top:-16px}}
.placechip{{display:inline-flex;align-items:center;gap:6px;margin:-4px 0 0;padding:6px 12px;border:1.5px solid var(--ink);border-radius:999px;font-size:14px;font-weight:500;animation:pop .45s cubic-bezier(.3,.8,.3,1.3) both}}
.placechip[hidden]{{display:none}}.placechip svg{{width:16px;height:16px;fill:var(--accent);stroke:var(--ink);stroke-width:1.6}}.placechip circle{{fill:var(--bg)}}
@keyframes inR{{from{{opacity:0;transform:translateX(32px)}}}}@keyframes inL{{from{{opacity:0;transform:translateX(-32px)}}}}
@keyframes outL{{to{{opacity:0;transform:translateX(-32px)}}}}@keyframes outR{{to{{opacity:0;transform:translateX(32px)}}}}
.callwrap[hidden]{{display:none}}.callwrap h2{{margin:0;font-weight:400;font-size:clamp(24px,3.4vw,30px);letter-spacing:-.02em}}
@keyframes rise{{from{{opacity:0;transform:translateY(18px)}}}}
.step[data-step=phone] .art{{width:min(300px,80vw)}}.step[data-step=phone] h1{{font-size:clamp(28px,4vw,38px)}}
.fine.center{{text-align:center}}
.step[data-step=phone] h2#n-title{{font-size:clamp(30px,5vw,40px);font-weight:400;letter-spacing:-.03em}}
.credit{{text-align:center;font-size:11px;color:var(--muted);margin:0 0 20px}}.credit a{{color:inherit}}
.letmein{{display:inline-flex;align-items:center;justify-content:center;gap:8px;width:100%;text-decoration:none;animation:pop .5s .6s cubic-bezier(.3,.8,.3,1.3) both}}.letmein svg{{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
.fine{{margin:0;font-size:12px;color:var(--muted);text-align:left;width:100%}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
</style></head><body>
<header><a class="logo" href="/" aria-label="Scoo home">{mark}<span>scoo</span></a><button class="back" id="back" type="button" disabled>Back</button></header>
<div class="dots" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
<main aria-live="polite">{steps_html}</main>
<script>
(()=>{{
const ILL_Q={json.dumps(ILL_Q)}, QS={json.dumps(QUESTIONS)}, PROSVG={json.dumps({k:pros[k] for k in QUESTIONS if k in pros})};
const DONE_ART={json.dumps(ILL_DONE)};
const CATS=[[/plumb|leak|tap|pipe|toilet|drain|water heater/i,'plumber','a plumber'],[/lawyer|legal|divorce|attorney|custody|sue/i,'lawyer','a lawyer'],
 [/insur/i,'insurance','an insurance agent'],[/electric|power|outlet|spark|breaker|wiring/i,'electrician','an electrician'],
 [/move|moving|sofa|couch|movers/i,'mover','movers'],[/doctor|weight|health|glp|clinic|sick/i,'doctor','a doctor']];
const GOAL=1000;
const order=['need','zip','q','phone','done'];let cur=0;const st={{}};
const $=s=>document.querySelector(s);
const reduceMotion=matchMedia('(prefers-reduced-motion: reduce)').matches;
function show(i){{
  const fwd=i>=cur,steps=[...document.querySelectorAll('.step')],prev=steps.find(s=>!s.hidden),next=steps.find(s=>s.dataset.step===order[i]);cur=i;
  document.querySelectorAll('.dots i').forEach((d,k)=>d.classList.toggle('on',k<=i));$('#back').disabled=i===0||i===order.length-1;
  const enter=()=>{{steps.forEach(s=>{{s.hidden=s!==next;s.style.animation='';}});if(!reduceMotion)next.style.animation=`${{fwd?'inR':'inL'}} .42s cubic-bezier(.3,.8,.3,1)`;scrollTo(0,0);
    const f=next.querySelector('input:not([hidden])');if(f&&f.offsetParent)setTimeout(()=>f.focus({{preventScroll:true}}),380);}};
  if(prev&&prev!==next&&!reduceMotion){{prev.style.animation=`${{fwd?'outL':'outR'}} .2s ease-in forwards`;setTimeout(enter,190);}}else enter();}}
$('#back').onclick=()=>show(Math.max(0,cur-1));
// The "searching" screen between the ZIP and the next question. It runs while the real lookup
// does, and every line it shows is true: the area comes from the API, and while Scoo is not live
// it says so rather than pretending to have found pros.
const wait=ms=>new Promise(r=>setTimeout(r,ms));
async function searching(zip){{
  const lis=[...document.querySelectorAll('#s-checks li')];lis.forEach(l=>l.className='');
  $('#s-zip').textContent=zip;$('#s-title').textContent='Looking up your area…';
  $('#s-pros').textContent=`Checking Scoo coverage in ${{zip}}`;
  $('#s-launch').textContent='Checking when Scoo opens near you';
  const lookup=(location.protocol==='file:'?Promise.resolve({{city:'Dallas',place:'Plano, TX',town:'Plano',areaLabel:'the Dallas area',waiting:0,goal:1000}}):fetch('/api/city?zip='+zip).then(r=>r.json())).catch(()=>null);
  const step=async(i,ms)=>{{lis[i].className='run';await wait(ms);lis[i].className='ok';}};
  await step(0,1100);const c=await lookup;
  st.city=c&&c.city||'your area';st.place=c&&c.place||null;st.town=c&&c.town||null;st.areaLabel=c&&c.areaLabel||'your area';st.waiting=c&&c.waiting||0;
  if(st.place)lis[0].querySelector('span').innerHTML=`Found <b>${{zip}}</b> · ${{st.place}}`;
  $('#s-title').textContent=st.place?`Found you in ${{st.place}}`:'Found your area';
  await step(1,1200);
  $('#s-launch').textContent=st.waiting>=25?`${{st.waiting.toLocaleString()}} neighbours already waiting in ${{st.areaLabel}}`:(st.town?`Scoo is coming to ${{st.town}}`:'Scoo is coming to your area');
  await step(2,1000);await wait(650);
}}
// The search runs once per ZIP; coming back to this screen shows its result straight away.
async function callScreen(){{
  show(3);const sec=document.querySelector('[data-step=phone]'),cw=$('#callwrap'),chip=$('#placechip');
  const settle=()=>{{
    $('#pc-text').textContent=st.place?`${{st.place}} · ${{st.zip}}`:st.zip;
    $('#n-title').textContent=st.town?`Scoo is coming to ${{st.town}}`:'Scoo is coming to your area';
    $('#n-lead').textContent='Get on the early list and be first to get a pro when we open.'+(st.waiting>=25?` Join ${{st.waiting.toLocaleString()}} neighbours already waiting.`:'');
    sec.classList.add('notify');chip.hidden=false;}};
  if(st.searchedZip!==st.zip&&!st.skipSearch){{
    sec.classList.remove('notify');chip.hidden=true;cw.hidden=true;$('#back').disabled=true;
    await wait(220);await searching(st.zip);st.searchedZip=st.zip;$('#back').disabled=false;
    settle();await wait(reduceMotion?0:520);
  }}else{{
    if(st.searchedZip!==st.zip){{st.city=st.city||'Dallas';st.place=st.place||'Plano, TX';st.town=st.town||'Plano';st.areaLabel=st.areaLabel||'the Dallas area';st.searchedZip=st.zip;}}
    settle();
  }}
  cw.hidden=false;setTimeout(()=>$('#tel').focus({{preventScroll:true}}),450);
}}

$('#f-need').onsubmit=e=>{{e.preventDefault();st.need=$('#need').value.trim();if(!st.need)return;
  const c=CATS.find(c=>c[0].test(st.need))||[null,'pro','a pro'];st.cat=c[1];st.noun=c[2];
  $('#zip-lead').textContent=`We'll find ${{st.noun}} near you.`;show(1);}};
$('#f-zip').onsubmit=async e=>{{e.preventDefault();const z=$('#zip').value.trim();if(!/^\\d{{5}}$/.test(z))return;st.zip=z;
  const [q,a]=QS[st.cat];$('#q-title').textContent=q;
  $('#q-choices').innerHTML=a.map(x=>`<button type="button">${{x}}</button>`).join('');
  $('#q-choices').querySelectorAll('button').forEach(b=>b.onclick=()=>{{st.answer=b.textContent;
    if(st.cat==='doctor'&&st.answer==='Yes'){{$('#q-title').textContent='Please call 911 now.';$('#q-choices').innerHTML='<p class="lead">Scoo is not for emergencies.</p>';return;}}
    callScreen();}});show(2);}};
const tel=$('#tel'),ok=$('#ok'),save=$('#save');
// Turnstile, when the site has it switched on: the button waits for the check as well.
let tsNeeded=false,tsToken=null;
const validContact=v=>v.includes('@')?/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(v.trim()):v.replace(/\\D/g,'').length>=10;
const chk=()=>save.disabled=!(ok.checked&&validContact(tel.value)&&(!tsNeeded||tsToken));tel.oninput=chk;ok.onchange=chk;
if(location.protocol!=='file:')fetch('/api/config').then(r=>r.json()).then(c=>{{if(!c.turnstileSiteKey)return;tsNeeded=true;chk();
  window.onTs=()=>turnstile.render('#ts',{{sitekey:c.turnstileSiteKey,theme:'auto',callback:t=>{{tsToken=t;chk();}},'expired-callback':()=>{{tsToken=null;chk();}}}});
  const sc=document.createElement('script');sc.src='https://challenges.cloudflare.com/turnstile/v0/api.js?onload=onTs&render=explicit';sc.async=true;document.head.appendChild(sc);}}).catch(()=>{{}});
const GOALN=GOAL;
function done(r){{
  const who=st.noun.replace(/^an? /,'');
  $('#done-art').innerHTML=DONE_ART.replace('PRO',['insurance','plumber','mover'].map((k,i)=>PROSVG[k].replace(/^<svg /,`<svg x="${{[72,118,170][i]}}" y="${{[86,82,86][i]}}" width="${{[78,84,78][i]}}" height="${{[100,108,100][i]}}" `)).join(''));
  $('#done-title').textContent=`You're on the list!`;
  $('#done-lead').textContent=`You're #${{r.position.toLocaleString()}} in ${{r.areaLabel||'your area'}}. We'll ${{r.via==='email'?'email':'text'}} you the moment Scoo opens in ${{r.town||'your area'}}.`;
  document.querySelectorAll('.cityname').forEach(n=>n.textContent=r.town||r.city);
  const f='scoo.app/r/'+r.code,p='scoo.app/pro/'+r.code;$('#flink').textContent=f;$('#plink').textContent=p;
  const msgF=`I just joined Scoo, get a pro to call you back in 60 seconds. Join with my link and we both get $10: https://${{f}}`;
  const msgP=`Thought of you: Scoo gives pros a free AI receptionist that answers the calls you miss and books the job. Claim yours: https://${{p}}`;
  const go=(btns,msg,url)=>{{const [wa,tx,third,fourth]=btns;
    wa.onclick=()=>open('https://wa.me/?text='+encodeURIComponent(msg));tx.onclick=()=>location.href='sms:?&body='+encodeURIComponent(msg);
    third.onclick=third.textContent==='Facebook'?()=>open('https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent('https://'+url)):()=>location.href='mailto:?subject=Scoo&body='+encodeURIComponent(msg);
    fourth.onclick=fourth.textContent==='Email'?()=>location.href='mailto:?subject=Scoo&body='+encodeURIComponent(msg):()=>navigator.share?navigator.share({{text:msg}}).catch(()=>{{}}):navigator.clipboard.writeText(msg);}};
  go(document.querySelectorAll('[data-p=f] .share button'),msgF,f);go(document.querySelectorAll('[data-p=p] .share button'),msgP,p);
  show(4);requestAnimationFrame(()=>requestAnimationFrame(()=>$('.meter i').style.width=Math.max(3,Math.min(100,Math.round(r.waiting/r.goal*100)))+'%'));}}
$('#f-phone').onsubmit=async e=>{{e.preventDefault();if(save.disabled)return;save.disabled=true;save.textContent='Saving…';
  let ref=null;try{{ref=localStorage.getItem('scoo_ref');}}catch(_){{}}
  const body={{need:st.need,category:st.cat,answer:st.answer||null,zip:st.zip,contact:tel.value.trim(),consent:ok.checked,consentText:$('.consent span').textContent,ref,turnstile:tsToken}};
  try{{
    if(location.protocol==='file:')return done({{position:1,waiting:1,goal:GOALN,city:'Dallas',town:'Plano',areaLabel:'the Dallas area',code:'demo01',via:tel.value.includes('@')?'email':'text'}});
    const res=await fetch('/api/requests',{{method:'POST',headers:{{'content-type':'application/json'}},body:JSON.stringify(body)}});
    const r=await res.json();if(!res.ok)throw new Error(r.error||'Something went wrong');done(r);
  }}catch(err){{save.textContent='Save my spot';if(window.turnstile&&tsNeeded){{turnstile.reset('#ts');tsToken=null;}}chk();
    let m=$('#f-phone .err');if(!m){{m=document.createElement('p');m.className='err';m.setAttribute('role','alert');$('#f-phone').appendChild(m);}}
    m.textContent=err.message+'. Please try again.';}}}};
document.querySelectorAll('.cp').forEach(b=>b.onclick=()=>{{navigator.clipboard&&navigator.clipboard.writeText('https://'+b.previousElementSibling.textContent);b.textContent='Copied';}});
document.querySelectorAll('[role=tab]').forEach(t=>t.onclick=()=>{{document.querySelectorAll('[role=tab]').forEach(x=>x.setAttribute('aria-selected',x===t));
  document.querySelectorAll('.tab').forEach(p=>p.hidden=p.dataset.p!==t.dataset.t);}});
try{{const rf=new URLSearchParams(location.search).get('ref');if(rf)localStorage.setItem('scoo_ref',rf);}}catch(_){{}}
const q=new URLSearchParams(location.search).get('q');if(q){{$('#need').value=q;$('#f-need').requestSubmit();}}else show(0);
// ?step=N jumps for screenshots; ?demo plays the flow
const step=new URLSearchParams(location.search).get('step');
if(step){{st.skipSearch=true;st.need=st.need||'My water heater is leaking';if(!st.cat){{st.cat='plumber';st.noun='a plumber';}}$('#zip').value='75201';
  if(+step===1)show(1);if(+step>=2)$('#f-zip').requestSubmit();if(+step>=3)callScreen();if(+step>=4){{tel.value='(214) 555-0142';ok.checked=true;chk();$('#f-phone').requestSubmit();}}}}
}})();
</script></body></html>'''
open('request.html', 'w').write(page)

# homepage: the input hands what was typed to the request page
home = open('index-live.html').read()
home = home.replace('<a class="pill" href="#">I\'m a pro</a>', '<a class="pill" href="/pros">I\'m a pro</a>')
home = home.replace('<div class="copy">', '<div class="copy">\n<p class="badge"><i></i>Launching city by city</p>', 1)
home = home.replace('</head>', '''<style>.badge{display:inline-flex;align-items:center;gap:8px;border:1.5px solid var(--ink);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:500}
.badge i{width:8px;height:8px;border-radius:99px;background:var(--accent);animation:pulse 1.6s ease-in-out infinite}@keyframes pulse{50%{opacity:.25}}</style></head>''', 1)
home = home.replace('</body></html>', '''<script>
try{const rf=new URLSearchParams(location.search).get('ref');if(rf)localStorage.setItem('scoo_ref',rf);}catch(_){}
document.querySelector('.ask').addEventListener('submit',e=>{e.preventDefault();e.stopImmediatePropagation();
  const v=document.getElementById('need').value.trim();location.href='/request'+(v?'?q='+encodeURIComponent(v):'');},true);
</script></body></html>''')
open('index.html', 'w').write(home)
print('ok')
