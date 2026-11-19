import math, random
random.seed(4)
G=520  # ground line y
els=[]  # (x_for_delay, svg)
layer=[0]
def add(x,s): els.append((x,s,layer[0]))
def R(x,y,w,h,extra=''): add(x,f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {extra}/>')
def L(x1,y1,x2,y2): add(min(x1,x2),f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
def P(x,d,cls=''): add(x,f'<path d="{d}" {cls}/>')
def C(x,y,r): add(x-r,f'<circle cx="{x}" cy="{y}" r="{r}"/>')
def win(x,y,w,h,lit=False,cross=False):
    R(x,y,w,h,'class="win'+(' lit' if lit else '')+'"')
    if cross: L(x+w/2,y,x+w/2,y+h); L(x,y+h/2,x+w,y+h/2)
lit_i=[0]
def litnext():
    return random.random()<0.16

def house(x):  # gabled house
    w=170;h=150;top=G-h
    R(x,top,w,h); P(x,f'M{x-12} {top} L{x+w/2} {top-80} L{x+w+12} {top} Z')
    R(x+120,top-62,18,40)  # chimney
    P(x,f'M{x+w/2-14} {top-36} a14 14 0 1 1 28 0 a14 14 0 1 1 -28 0')  # round attic window
    R(x+65,G-80,40,80); C(x+98,G-40,2.5)
    win(x+18,G-110,36,44,litnext()); win(x+w-54,G-110,36,44,litnext())
    L(x+10,G-60,x+60,G-60); L(x+110,G-60,x+160,G-60)  # window boxes
def brownstone(x):
    w=150;h=300;top=G-h
    R(x,top,w,h); R(x-6,top-14,w+12,14); L(x-6,top+8,x+w+6,top+8)
    for f in range(3):
        y=top+30+f*72
        for i in range(3): win(x+18+i*42,y,28,50,litnext())
        L(x+12,y+58,x+w-12,y+58)
    P(x,f'M{x+55} {G-30} L{x+55} {G-78} A20 20 0 0 1 {x+95} {G-78} L{x+95} {G-30}')
    for s in range(3): R(x+40-s*8,G-30+s*10,70+s*16,10)
def shop(x):
    w=200;h=230;top=G-h
    R(x,top,w,h); R(x-6,top-10,w+12,10)
    R(x+20,top+22,w-40,30,'class="sign"')
    for i in range(3): win(x+22+i*58,top+66,40,44,litnext())
    # awning scallops
    aw=G-120
    L(x+8,aw,x+w-8,aw)
    d=f'M{x+8} {aw} L{x+8} {aw+26} '
    n=8;sw=(w-16)/n
    for i in range(n): d+=f'q{sw/2} 14 {sw} 0 '
    d+=f'L{x+w-8} {aw}'
    P(x,d,'class="awn"')
    for i in range(1,n): L(x+8+i*sw,aw,x+8+i*sw,aw+26)
    R(x+20,G-88,100,88,'class="win"'); L(x+70,G-88,x+70,G)
    R(x+140,G-88,40,88); C(x+148,G-44,2.5)
def tower(x):
    w=190;h=420;top=G-h
    R(x,top,w,h); R(x+30,top-30,w-60,30); L(x+w/2,top-30,x+w/2,top-70); C(x+w/2,top-74,4)
    for f in range(8):
        y=top+20+f*40
        for i in range(5): R(x+16+i*34,y,22,26,'class="win'+(' lit' if litnext() else '')+'"')
    R(x+65,G-60,60,60); L(x+95,G-60,x+95,G)
def apartment(x):
    w=170;h=340;top=G-h
    R(x,top,w,h); R(x-6,top-12,w+12,12)
    # water tower
    tx=x+100
    P(tx,f'M{tx} {top-12} L{tx+6} {top-40} M{tx+44} {top-12} L{tx+38} {top-40}')
    R(tx-2,top-80,48,40); P(tx,f'M{tx-6} {top-80} L{tx+22} {top-100} L{tx+50} {top-80}')
    for f in range(5):
        y=top+24+f*48
        for i in range(3):
            win(x+20+i*48,y,32,34,litnext())
        if f%2==1: R(x+14,y+34,w-28,8)  # balcony ledge
    R(x+62,G-56,46,56)
def cafe(x):
    w=150;h=200;top=G-h
    R(x,top,w,h); P(x,f'M{x} {top} L{x} {top-20} L{x+w} {top-20} L{x+w} {top}')
    C(x+w/2,top+26,16)
    for i in range(2): win(x+20+i*70,top+50,40,36,litnext())
    aw=G-100;n=6;sw=w/n
    P(x,f'M{x-6} {aw} L{x+w+6} {aw} L{x+w-6} {aw+30} L{x+6} {aw+30} Z','class="awn"')
    for i in range(1,n): L(x-6+i*(w+12)/n,aw,x+6+i*(w-12)/n,aw+30)
    R(x+16,G-66,70,66,'class="win"'); R(x+100,G-66,34,66)
    # tables
def tree(x,s=1):
    layer[0]=1
    L(x,G,x,G-60*s)
    P(x,f'M{x} {G-60*s} c-46 0 -50 -50 -20 -64 c-6 -36 46 -40 50 -10 c34 -6 40 40 10 54 c4 20 -26 24 -40 20 Z'.replace('-60*s',''))
    layer[0]=0
def lamp(x):
    L(x,G,x,G-120); P(x,f'M{x} {G-120} q0 -16 18 -16'); R(x+12,G-140,14,10)
def clouds():
    for cx,cy,sc in ((260,120,1),(980,80,1.3),(1480,95,.9)):
        add(cx,f'<path class="cloud" style="--s:{sc}" d="M{cx} {cy} c0 -18 26 -22 32 -8 c6 -20 44 -18 46 4 c18 0 22 24 0 26 l-78 0 c-18 0 -18 -22 0 -22 Z"/>')

x=40
for fn,gap in ((house,30),(tree,0),(brownstone,30),(shop,20),(lamp,0),(tower,30),(cafe,30),(tree,0),(apartment,30),(house,0)):
    if fn is tree: tree(x+30); x+=80; continue
    if fn is lamp: lamp(x+10); x+=50; continue
    fn(x); x+={'house':170,'brownstone':150,'shop':200,'tower':190,'cafe':150,'apartment':170}[fn.__name__]+gap
W=x+40
clouds()
L(0,G,W,G); L(0,G+24,W,G+24)
for i in range(0,W,60): L(i,G+44,i+30,G+44)

# ---------- character (kept minimal) ----------
layer[0]=1
def T(x,y,txt,size=14,cls='txt'): add(x,f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" text-anchor="middle">{txt}</text>')
add(170,'<path class="smoke" d="M169 300 c-10 -12 10 -20 0 -32 c-10 -12 10 -20 0 -32"/>')
T(600,333,'HARDWARE &amp; CO',13)
add(865,'<circle class="blink" cx="865" cy="26" r="4"/>')
T(1065,315,'CAFÉ LUNA',11)
add(1058,'<path d="M1058 341 h14 v5 a7 7 0 0 1 -14 0 Z M1072 343 q5 0 3 5 q-2 2 -3 2"/>')
layer[0]=0

els.sort(key=lambda e:(e[2],e[0]))
out=[]
for k,(xx,s,_) in enumerate(els):
    delay=min(xx,W)/W*2.4+ (k%7)*0.02
    if xx==9999: delay=3.0
    s=(s.replace('<text ',f'<text style="--d:{delay:.2f}s" ',1) if s.startswith('<text') else s.replace('/>',f' pathLength="1"/>').replace('<g class="walker"',f'<g class="walker" style="--d:{delay:.2f}s"') if s.startswith('<g') else s.replace(' style="--k',' pathLength="1" style="--d:%.2fs;--k'%delay,1) if 'style="--k' in s else s.replace('/>',f' pathLength="1" style="--d:{delay:.2f}s"/>',1)) if 'style="--s' not in s else s.replace('style="--s',f'pathLength="1" style="--d:{delay:.2f}s;--s',1)
    out.append(s)
svg=f'<svg class="scene" viewBox="0 0 {W} {G+60}" role="img" aria-label="Line drawing of a city street: houses, shops, a cafe, apartments and an office tower">'+'\n'.join(out)+'</svg>'

def body(extra_back='',extra_front='',wings=True,arm_up=False):
    wing=('<g transform="translate(48 80) scale(1.45) translate(-48 -80)"><g class="wing wl"><path class="wingp" d="M48 76 C22 54 2 66 8 82 C14 80 16 88 24 88 C26 95 36 95 48 88 Z"/><path d="M14 80 q10 -2 18 2 M24 88 q8 -4 16 -2"/></g></g>'
          '<g transform="translate(72 80) scale(1.45) translate(-72 -80)"><g class="wing wr"><path class="wingp" d="M72 76 C98 54 118 66 112 82 C106 80 104 88 96 88 C94 95 84 95 72 88 Z"/><path d="M106 80 q-10 -2 -18 2 M96 88 q-8 -4 -16 -2"/></g></g>') if wings else ''
    rarm='M74 72 L92 40' if arm_up else 'M74 72 L90 98'
    return (f'{wing}{extra_back}'
      '<path class="skin" d="M48 64 h24 a4 4 0 0 1 4 4 v42 h-32 v-42 a4 4 0 0 1 4 -4 Z"/>'
      '<path d="M52 110 l-2 30 M68 110 l2 30 M44 140 h8 M68 140 h8"/>'
      f'<path d="M46 72 L30 98 {rarm}"/>'
      '<circle class="skin" cx="60" cy="48" r="13"/><path d="M55 50 h0.1 M65 50 h0.1" class="eyes"/><path d="M56 55 q4 3 8 0"/>'
      f'{extra_front}')
plumber=body('',
  '<path class="hat" d="M46 44 a14 13 0 0 1 28 0 Z"/><path d="M74 44 h10"/>'
  '<path d="M52 64 v16 M68 64 v16"/><rect class="bib" x="50" y="80" width="20" height="30" rx="2"/>'
  '<g transform="translate(88 96) rotate(30)"><path class="tool" d="M-3 0 h6 v22 h-6 Z M-8 -10 a8 8 0 1 0 16 0 l-4 4 h-8 Z"/></g>')
lawyer=body('',
  '<path d="M48 40 q12 -14 24 0"/>'
  '<path d="M54 64 l6 8 l6 -8"/><path class="tie" d="M60 72 l-3 4 l3 18 l3 -18 Z"/>'
  '<rect class="case" x="18" y="98" width="24" height="18" rx="3"/><path d="M26 98 v-4 h8 v4"/>')
doctor=body('',
  '<path d="M52 64 q-2 22 8 22 q10 0 8 -22"/><circle cx="60" cy="88" r="3"/>'
  '<path class="cross" d="M64 96 h8 M68 92 v8"/><path d="M46 44 q14 -12 28 0"/>')
umbrella=body('',
  '<path d="M48 42 q12 -12 24 0"/><path d="M92 40 V6"/>'
  '<path class="umb" d="M52 8 Q92 -30 132 8 Q122 2 112 8 Q102 2 92 8 Q82 2 72 8 Q62 2 52 8 Z"/>'
  '<path d="M92 40 q0 6 -5 6"/>',wings=False,arm_up=True)
def charsvg(cls,inner,label): return f'<div class="pro {cls}"><div class="bob"><svg viewBox="-4 -28 140 176" role="img" aria-label="{label}">{inner}</svg></div></div>'
pros=(charsvg('p1',plumber,'A plumber with wings flying in')+charsvg('p2',lawyer,'A lawyer with wings and a briefcase')
     +charsvg('p3',umbrella,'An insurance agent floating down under an umbrella')+charsvg('p4',doctor,'A doctor with wings and a stethoscope'))
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Scoo street</title>
<style>
:root{{--bg:#FFFFFF;--ink:#111111;--glow:#FFE7A3;--accent:#FF6B4A;--soft:#FFD9CF;--leaf:#9ED3A8;--muted:#555555}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0E0E10;--ink:#EDEDED;--glow:#5A4A1C;--accent:#FF7A5C;--soft:#4A2620;--leaf:#2F5A3A;--muted:#B5B5B5}}}}
:root[data-theme="dark"]{{--bg:#0E0E10;--ink:#EDEDED;--glow:#5A4A1C;--accent:#FF7A5C;--soft:#4A2620;--leaf:#2F5A3A;--muted:#B5B5B5}}
html,body{{margin:0;height:100%;background:var(--bg)}}
.hero{{min-height:100vh;display:flex;flex-direction:column;overflow:hidden;font-family:Inter,system-ui,sans-serif;color:var(--ink)}}
nav{{display:flex;justify-content:space-between;align-items:center;padding:20px clamp(16px,4vw,48px)}}
.logo{{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:28px;letter-spacing:-.5px;color:var(--ink);text-decoration:none}}
.navlinks{{display:flex;gap:24px;align-items:center;font-size:15px}}.navlinks a{{color:var(--ink);text-decoration:none}}
.navlinks .pill{{border:2px solid var(--ink);border-radius:999px;padding:9px 18px;font-weight:600}}
.copy{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;text-align:center;gap:18px;padding:24px 16px clamp(28px,5vh,56px);opacity:0;animation:fade .8s ease-out forwards .2s}}
h1{{margin:0;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:clamp(48px,7.5vw,104px);line-height:.95;letter-spacing:-2.5px}}
h1 span{{color:var(--accent)}}
.sub{{margin:0;font-size:clamp(17px,1.5vw,20px);line-height:1.5;color:var(--muted);max-width:520px}}
.ctas{{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:6px}}
.btn{{display:inline-flex;align-items:center;min-height:54px;padding:0 26px;border-radius:999px;font-size:16px;font-weight:600;text-decoration:none}}
.primary{{background:var(--ink);color:var(--bg)}}.secondary{{border:2px solid var(--ink);color:var(--ink)}}
.street{{display:flex;justify-content:center}}
.hero{{position:relative}}
.pro{{position:absolute;width:clamp(92px,9.5vw,140px);z-index:2;animation:drop 2.2s cubic-bezier(.22,.9,.3,1.15) both;animation-delay:var(--dl)}}
.pro svg{{width:100%;height:auto;overflow:visible}}
.pro svg *{{fill:none;stroke:var(--ink);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}}
.pro .skin,.pro .wingp,.pro .bib,.pro .case,.pro .hat{{fill:var(--bg)}}
.pro .wingp{{fill:var(--soft)}}.pro .hat,.pro .tie,.pro .umb{{fill:var(--accent)}}.pro .umb{{fill:var(--soft)}}
.pro .eyes{{stroke-width:4}}.pro .cross{{stroke:var(--accent);stroke-width:3}}.pro .tool{{fill:var(--bg)}}
.bob{{animation:bob 2.6s ease-in-out infinite alternate;animation-delay:calc(var(--dl) + 2.2s)}}
.wing{{transform-box:fill-box;animation:flap .35s ease-in-out infinite alternate}}
.wl{{transform-origin:100% 50%}}.wr{{transform-origin:0% 50%}}
.p3 .bob{{animation:sway 3s ease-in-out infinite alternate}}
.p1{{left:7%;top:20%;--dl:.9s}}.p2{{right:7%;top:15%;--dl:1.5s}}.p3{{left:19%;top:33%;--dl:2.1s}}.p4{{right:19%;top:31%;--dl:2.7s}}
@keyframes drop{{from{{transform:translateY(-110vh) rotate(-10deg)}}to{{transform:none}}}}
@keyframes bob{{to{{transform:translateY(-12px)}}}}
@keyframes flap{{from{{transform:rotate(0)}}to{{transform:rotate(-14deg) scaleY(.85)}}}}
.wr{{animation-name:flapr}}@keyframes flapr{{to{{transform:rotate(14deg) scaleY(.85)}}}}
@keyframes sway{{from{{transform:rotate(-6deg)}}to{{transform:rotate(6deg) translateY(-8px)}}}}
@media (max-width:900px){{.p2,.p4{{display:none}}.pro{{width:84px}}.p1{{left:5%;top:10%}}.p3{{left:auto;right:30%;top:8%}}}}
@media (prefers-reduced-motion:reduce){{.pro,.bob,.wing{{animation:none}}}}
@media (max-width:640px){{.navlinks a:not(.pill){{display:none}}}}
.scene{{flex-shrink:0;width:max(100%,900px);height:auto;max-height:55vh;display:block}}
.scene *{{fill:var(--bg);stroke:var(--ink);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;
 stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.1s ease-out forwards;animation-delay:var(--d)}}
.scene line{{fill:none}}
.win.lit{{animation:draw 1.1s ease-out forwards var(--d),glow .8s ease-out forwards calc(var(--d) + 2.6s)}}
.cloud{{animation:draw 1.1s ease-out forwards var(--d),drift 18s ease-in-out infinite alternate calc(var(--d) + 1s)}}
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600&display=swap');
.scene text{{stroke:none;fill:var(--ink);font-family:'Space Grotesk',sans-serif;font-weight:600;letter-spacing:1.5px;opacity:0;animation:fade .6s forwards;animation-delay:calc(var(--d) + .8s)}}
.flower{{fill:var(--accent)}}.leaf{{fill:var(--leaf)}}.awn{{fill:var(--soft)}}
.blink{{fill:var(--accent);stroke:none;animation:blink 1.6s steps(1) infinite}}
.bulb{{animation:draw .6s forwards var(--d),glow .5s forwards calc(var(--d) + 2.4s),twinkle 2s ease-in-out infinite calc(var(--d) + 3s + var(--k)*.3s)}}
.smoke,.steam{{fill:none;animation:draw 1s forwards var(--d),rise 3s ease-in-out infinite calc(var(--d) + 1s)}}
.tail{{fill:none;transform-origin:1543px 288px;animation:draw 1s forwards var(--d),wag 1.4s ease-in-out infinite alternate 3s}}
.walker{{stroke-dashoffset:0;opacity:0;animation:fade .5s forwards var(--d),walk 28s linear infinite var(--d)}}
.walker *{{animation:none;stroke-dashoffset:0;fill:none}}.walker circle{{fill:var(--bg)}}
@media (prefers-reduced-motion:reduce){{.walker{{animation:none;opacity:1;transform:translateX(600px)}}}}
.bird{{fill:none;transform-origin:720px 140px;animation:draw 1s forwards var(--d),flap .5s ease-in-out infinite alternate 2s,fly 40s linear infinite 2s}}
@keyframes fade{{to{{opacity:1}}}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:.15}}}}
@keyframes twinkle{{50%{{opacity:.45}}}}
@keyframes rise{{0%{{transform:translateY(0);opacity:1}}100%{{transform:translateY(-14px);opacity:0}}}}
@keyframes wag{{to{{transform:rotate(12deg)}}}}
@keyframes walk{{from{{transform:translateX(-120px)}}to{{transform:translateX(1780px)}}}}
@keyframes flap{{to{{transform:scaleY(.5)}}}}
@keyframes fly{{to{{translate:-900px -40px}}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes glow{{to{{fill:var(--glow)}}}}
@keyframes drift{{to{{transform:translateX(60px)}}}}
@media (prefers-reduced-motion:reduce){{.scene *{{animation:none;stroke-dashoffset:0}}.win.lit{{fill:var(--glow)}}}}
</style>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
</head><body><section class="hero">
{pros}
<nav aria-label="Main"><a class="logo" href="#">scoo</a><div class="navlinks"><a href="#">How it works</a><a href="#">Live exchange</a><a class="pill" href="#">For pros</a></div></nav>
<div class="copy">
<h1 aria-label="Get an expert in 60 seconds">Get <span class="rot" aria-hidden="true"><span class="w">an expert</span></span><br aria-hidden="true"><span class="tail" aria-hidden="true">in 60 seconds.</span></h1>
<p class="sub">Plumbers, lawyers, insurance, health and more. Tell Scoo what you need and the right pro calls you back.</p>
<div class="ctas"><a class="btn primary" href="#">Tell Scoo what you need</a><a class="btn secondary" href="#">I'm a pro</a></div>
</div>
<div class="street">{svg}</div>
</section></body></html>'''
open(__import__('os').path.join(__import__('os').path.dirname(__file__) or '.','index.html'),'w').write(html)
print(W,len(els))
