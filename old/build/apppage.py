# Builds app.html: the signed-in home screen. A full-screen line-art map of their area, the request
# bar floating on top, and their launch area filling up toward the goal. Every number comes from
# /api/me (real, counted by area). Updates by polling for now; Durable Objects push later.
mark = open('_mark.svg').read()

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Scoo · Your area</title><link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet">
<link href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" rel="stylesheet">
<style>
:root{{--bg:#FFFFFF;--ink:#111111;--muted:#55595f;--accent:#FF6B4A;--soft:#FFD9CF;--line:#e7e5e0;--card:#FFFFFF}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0E0E10;--ink:#EDEDED;--muted:#a7abb3;--accent:#FF7A5C;--soft:#4A2620;--line:#2a2a2e;--card:#141417}}}}
:root[data-theme="dark"]{{--bg:#0E0E10;--ink:#EDEDED;--muted:#a7abb3;--accent:#FF7A5C;--soft:#4A2620;--line:#2a2a2e;--card:#141417}}
*{{box-sizing:border-box}}html,body{{margin:0;height:100%;background:var(--bg);color:var(--ink);font-family:'Hanken Grotesk',system-ui,sans-serif;overflow:hidden}}
#map{{position:fixed;inset:0}}
.top{{position:fixed;top:0;left:0;right:0;display:flex;gap:10px;align-items:center;padding:max(14px,env(safe-area-inset-top)) 14px 0;pointer-events:none;z-index:2}}
.top>*{{pointer-events:auto}}
.logo{{display:grid;place-items:center;width:50px;height:50px;border-radius:999px;background:var(--card);border:1.5px solid var(--ink);flex:0 0 auto}}
.logo svg{{height:22px;width:auto;color:var(--ink)}}.logo .mouth{{stroke:var(--accent)}}
.ask{{flex:1;display:flex;align-items:center;gap:6px;min-width:0;max-width:560px;height:50px;border:1.5px solid var(--ink);border-radius:999px;background:var(--card);padding:0 5px 0 18px;box-shadow:0 6px 24px rgba(0,0,0,.08)}}
.ask input{{flex:1;min-width:0;border:0;outline:0;background:transparent;color:var(--ink);font:400 17px 'Hanken Grotesk',sans-serif}}
.ask button{{display:grid;place-items:center;width:40px;height:40px;border:0;border-radius:999px;background:var(--accent);color:#fff;cursor:pointer}}
.ask svg{{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
.sheet{{position:fixed;left:12px;right:12px;bottom:max(12px,env(safe-area-inset-bottom));z-index:2;background:var(--card);border:1.5px solid var(--ink);border-radius:24px;padding:18px 18px 16px;
  box-shadow:0 10px 40px rgba(0,0,0,.12);display:flex;flex-direction:column;gap:12px;max-width:440px;transform:translateY(130%);transition:transform .7s cubic-bezier(.3,.8,.3,1)}}
.sheet.on{{transform:none}}
@media (min-width:880px){{.sheet{{left:24px;right:auto;bottom:24px;width:400px}}.top{{padding:24px 24px 0}}}}
.chip{{align-self:flex-start;display:inline-flex;align-items:center;gap:6px;padding:5px 11px;border:1.5px solid var(--ink);border-radius:999px;font-size:13px;font-weight:500}}
.chip svg{{width:14px;height:14px;fill:var(--accent);stroke:var(--ink);stroke-width:1.6}}.chip circle{{fill:var(--bg)}}
.sheet h1{{margin:0;font-weight:400;font-size:26px;letter-spacing:-.02em;line-height:1.15}}
.prog{{display:flex;flex-direction:column;gap:6px}}
.bar{{height:10px;border-radius:99px;border:1.5px solid var(--ink);overflow:hidden}}.bar i{{display:block;height:100%;width:0;background:var(--accent);transition:width 1.4s cubic-bezier(.3,.8,.3,1)}}
.prog small{{display:flex;justify-content:space-between;color:var(--muted);font-size:13px}}
.rows{{display:grid;gap:8px;font-size:15px}}
.row{{display:flex;gap:10px;align-items:flex-start;line-height:1.35}}.row b{{font-weight:600}}
.row .ic{{flex:0 0 auto;width:28px;height:28px;border-radius:99px;display:grid;place-items:center;background:var(--soft)}}
.row .ic svg{{width:16px;height:16px;fill:none;stroke:var(--ink);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.row small{{display:block;color:var(--muted);font-size:13px}}
.handle{{align-self:center;margin:-8px 0 -4px;width:60px;height:22px;border:0;background:none;cursor:pointer;display:grid;place-items:center}}.handle i{{width:40px;height:5px;border-radius:99px;background:var(--line)}}
.more{{display:grid;gap:12px;overflow:hidden;max-height:260px;transition:max-height .45s cubic-bezier(.3,.8,.3,1),opacity .3s}}
.sheet.min .more{{max-height:0;opacity:0;margin-top:-12px}}
@media (min-width:880px){{.handle{{display:none}}}}
.acts{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.acts button{{min-height:46px;border-radius:999px;border:1.5px solid var(--ink);background:var(--bg);color:var(--ink);font:600 15px 'Hanken Grotesk',sans-serif;cursor:pointer}}
.acts .p{{background:var(--accent);border-color:var(--accent);color:#fff}}
.toast{{position:fixed;left:50%;top:84px;transform:translate(-50%,-20px);opacity:0;z-index:3;background:var(--ink);color:var(--bg);padding:10px 16px;border-radius:999px;font-size:14px;font-weight:500;transition:all .4s ease;white-space:nowrap}}
.toast.on{{opacity:1;transform:translate(-50%,0)}}
.me{{width:22px;height:22px;border-radius:99px;background:var(--accent);border:3px solid var(--bg);box-shadow:0 0 0 1.5px var(--ink)}}
.me::after{{content:"";position:absolute;inset:-14px;border-radius:99px;border:2px solid var(--accent);animation:pulse 2.2s ease-out infinite}}
@keyframes pulse{{from{{transform:scale(.4);opacity:.9}}to{{transform:scale(1.6);opacity:0}}}}
.lbl{{font:500 12px 'Hanken Grotesk',sans-serif;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:3px 9px;white-space:nowrap}}
.lbl b{{color:var(--accent);font-weight:600}}
.gate{{position:fixed;inset:0;display:none;place-items:center;z-index:5;background:var(--bg);text-align:center;padding:24px}}
.gate.on{{display:grid}}.gate a{{display:inline-block;margin-top:14px;padding:14px 22px;border-radius:999px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600}}
.maplibregl-ctrl-attrib{{font-size:10px}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
</style></head><body>
<div id="map" role="img" aria-label="Map of your area"></div>
<div class="top">
  <a class="logo" href="/" aria-label="Scoo home">{mark}</a>
  <form class="ask" id="ask" role="search"><label for="q" class="vh" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">What do you need?</label>
    <input id="q" placeholder="What do you need?" autocomplete="off"><button aria-label="Ask Scoo"><svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6"/></svg></button></form>
</div>
<div class="toast" id="toast" role="status"></div>
<section class="sheet" id="sheet" aria-live="polite">
  <button class="handle" id="handle" aria-label="Show less" aria-expanded="true"><i></i></button>
  <span class="chip"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.3-7-11.5A7 7 0 0 1 19 9.5C19 14.7 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg><span id="place"></span></span>
  <h1 id="title"></h1>
  <div class="prog"><div class="bar"><i id="fill"></i></div><small><span id="count"></span><span id="goal"></span></small></div>
  <div class="more" id="more">
  <div class="rows">
    <div class="row"><span class="ic"><svg viewBox="0 0 24 24"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></svg></span><span id="pros"></span></div>
    <div class="row"><span class="ic"><svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3"/><path d="M3 20c0-3 3-5 6-5s6 2 6 5M16 11a3 3 0 1 0 0-6M21 20c0-2.4-1.7-4.3-4-4.8"/></svg></span><span id="inv"></span></div>
  </div>
  </div>
  <div class="acts"><button class="p" id="share">Invite friends</button><button id="pro">Know a pro?</button></div>
</section>
<div class="gate" id="gate"><div><h2 style="font-weight:400;margin:0">Join to see your area</h2><p style="color:var(--muted)">Tell Scoo what you need and save your spot.</p><a href="/request">Get started</a></div></div>
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
<script>
(()=>{{
const $=s=>document.querySelector(s);
const dark=matchMedia('(prefers-color-scheme: dark)').matches&&document.documentElement.dataset.theme!=='light';
const C=dark?{{bg:'#0E0E10',water:'#16233a',park:'#14241a',road:'#3a3a40',minor:'#26262b',build:'#1b1b1f',text:'#c9cbd1',halo:'#0E0E10',accent:'#FF7A5C'}}
            :{{bg:'#FFFFFF',water:'#D6E8FA',park:'#E4F2E1',road:'#C9C6BD',minor:'#E6E3DC',build:'#F2F0EA',text:'#55595f',halo:'#FFFFFF',accent:'#FF6B4A'}};
// A line-art style on OpenFreeMap's vector tiles: white ground, thin streets, quiet labels.
const style={{version:8,glyphs:'https://tiles.openfreemap.org/fonts/{{fontstack}}/{{range}}.pbf',
  sources:{{omt:{{type:'vector',url:'https://tiles.openfreemap.org/planet',attribution:'<a href="https://openfreemap.org">OpenFreeMap</a> © <a href="https://www.openmaptiles.org/">OpenMapTiles</a> © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}}}},
  layers:[
   {{id:'bg',type:'background',paint:{{'background-color':C.bg}}}},
   {{id:'park',type:'fill',source:'omt','source-layer':'park',paint:{{'fill-color':C.park}}}},
   {{id:'green',type:'fill',source:'omt','source-layer':'landcover',filter:['in','class','grass','wood'],paint:{{'fill-color':C.park,'fill-opacity':.6}}}},
   {{id:'water',type:'fill',source:'omt','source-layer':'water',paint:{{'fill-color':C.water}}}},
   {{id:'river',type:'line',source:'omt','source-layer':'waterway',paint:{{'line-color':C.water,'line-width':1.5}}}},
   {{id:'build',type:'fill',source:'omt','source-layer':'building',minzoom:14,paint:{{'fill-color':C.build,'fill-outline-color':C.minor}}}},
   {{id:'minor',type:'line',source:'omt','source-layer':'transportation',filter:['in','class','minor','service','track'],minzoom:12,paint:{{'line-color':C.minor,'line-width':['interpolate',['linear'],['zoom'],12,.5,16,3]}}}},
   {{id:'road',type:'line',source:'omt','source-layer':'transportation',filter:['in','class','primary','secondary','tertiary','trunk'],paint:{{'line-color':C.road,'line-width':['interpolate',['linear'],['zoom'],8,.5,12,1.2,16,5]}}}},
   {{id:'motorway',type:'line',source:'omt','source-layer':'transportation',filter:['==','class','motorway'],paint:{{'line-color':C.road,'line-width':['interpolate',['linear'],['zoom'],6,.8,12,2,16,7]}}}},
   {{id:'place',type:'symbol',source:'omt','source-layer':'place',filter:['in','class','city','town','suburb','neighbourhood'],
     layout:{{'text-field':['coalesce',['get','name:en'],['get','name']],'text-font':['Noto Sans Regular'],'text-size':['match',['get','class'],'city',14,'town',12,11]}},
     paint:{{'text-color':C.text,'text-halo-color':C.halo,'text-halo-width':1.5}}}}
  ]}};
const map=new maplibregl.Map({{container:'map',style,center:[-96.8,32.9],zoom:8.5,attributionControl:{{compact:true}},pitchWithRotate:false,dragRotate:false}});
map.touchZoomRotate.disableRotation();

// Fill the area like a glass: clip its outline below a horizontal line at `p` of its height.
function fillTo(poly,p){{
  const ys=poly.map(q=>q[1]),y0=Math.min(...ys),y1=Math.max(...ys),cut=y0+(y1-y0)*p,out=[];
  for(let i=0;i<poly.length;i++){{const a=poly[i],b=poly[(i+1)%poly.length],ia=a[1]<=cut,ib=b[1]<=cut;
    if(ia)out.push(a);if(ia!==ib){{const t=(cut-a[1])/(b[1]-a[1]);out.push([a[0]+(b[0]-a[0])*t,cut]);}}}}
  return out.length>2?out:null;}}
const ring=p=>[...p,p[0]];
let data=null,shown=0,anim=null;
// The whole area deepens in colour as it fills toward the launch goal.
function setFill(p){{if(!map.getLayer('fill')||!data.outline)return;
  map.getSource('fill').setData({{type:'Feature',geometry:{{type:'Polygon',coordinates:[ring(data.outline)]}}}});
  map.setPaintProperty('fill','fill-opacity',.06+.38*Math.max(0,Math.min(1,p)));}}
function animateFill(to){{cancelAnimationFrame(anim);const from=shown,t0=performance.now(),d=matchMedia('(prefers-reduced-motion: reduce)').matches?1:1600;
  const step=t=>{{const k=Math.min(1,(t-t0)/d),e=1-Math.pow(1-k,3);shown=from+(to-from)*e;setFill(shown);if(k<1)anim=requestAnimationFrame(step);}};anim=requestAnimationFrame(step);}}
const fmt=n=>n.toLocaleString();
const tradeName=(t,n)=>{{const special={{'HVAC':['HVAC pro','HVAC pros'],'Pest control':['pest control pro','pest control pros'],'Doctor or clinic':['clinic','clinics'],'Other':['pro','pros']}};
  if(special[t])return special[t][n>1?1:0];const w=t.toLowerCase();return n>1?(w.endsWith('s')?w+'es':w+'s'):w;}};
function render(d,first){{
  $('#place').textContent=`${{d.place||'Your area'}} · ${{d.zip}}`;
  $('#title').textContent=d.town?`Scoo is coming to ${{d.town}}`:'Scoo is coming to your area';
  $('#count').textContent=`${{fmt(d.waiting)}} ${{d.waiting===1?'neighbour':'neighbours'}} waiting · you're #${{fmt(d.position)}}`;
  $('#goal').textContent=`${{fmt(d.goal)}} to open`;
  $('#fill').style.width=Math.max(2,Math.min(100,d.waiting/d.goal*100))+'%';
  $('#pros').innerHTML=d.pros.length?`<span><b>${{d.pros.map(p=>`${{p.n}} ${{tradeName(p.trade,p.n)}}`).slice(0,3).join(' · ')}}</b> joined in ${{d.areaLabel}}<small>More pros means a faster launch.</small></span>`
    :`<span><b>Pros are joining soon</b><small>Know a great one? Invite them to claim a free AI receptionist.</small></span>`;
  $('#inv').innerHTML=d.invited?`<span><b>${{d.invited}} ${{d.invited===1?'person':'people'}}</b> joined through you<small>Every invite moves ${{d.area}} closer.</small></span>`
    :`<span><b>Invite neighbours to open ${{d.area}} sooner</b><small>You each get $10 credit.</small></span>`;
  if(map.getSource('area')){{
    map.getSource('area').setData(d.outline?{{type:'Feature',geometry:{{type:'Polygon',coordinates:[ring(d.outline)]}}}}:{{type:'FeatureCollection',features:[]}});
    map.getSource('near').setData({{type:'FeatureCollection',features:d.nearby.filter(n=>n.waiting>0).map(n=>({{type:'Feature',properties:{{w:n.waiting}},geometry:{{type:'Polygon',coordinates:[ring(n.outline)]}}}}))}});
    animateFill(d.waiting/d.goal);
  }}
  if(first){{
    const el=document.createElement('div');el.className='me';el.setAttribute('aria-label','You');
    if(d.pin)new maplibregl.Marker({{element:el}}).setLngLat([d.pin[1],d.pin[0]]).addTo(map);
    labels.forEach(m=>m.remove());labels=[];
    d.nearby.filter(n=>n.waiting>0).forEach(n=>{{const e=document.createElement('div');e.className='lbl';e.innerHTML=`${{n.name}} · <b>${{fmt(n.waiting)}}</b> waiting`;labels.push(new maplibregl.Marker({{element:e}}).setLngLat(n.center).addTo(map));}});
    const pts=(d.outline||[]).concat(d.pin?[[d.pin[1],d.pin[0]]]:[]);
    if(pts.length){{const b=new maplibregl.LngLatBounds(pts[0],pts[0]);pts.forEach(p=>b.extend(p));
      const wide=innerWidth>=880;map.fitBounds(b,{{padding:wide?{{top:90,bottom:60,left:460,right:60}}:{{top:90,bottom:Math.min(380,innerHeight*.48),left:24,right:24}},duration:first==='fly'?2200:0,maxZoom:12}});}}
  }}
}}
let labels=[];
const toast=m=>{{const t=$('#toast');t.textContent=m;t.classList.add('on');clearTimeout(t._h);t._h=setTimeout(()=>t.classList.remove('on'),3200);}};
async function load(){{const r=await fetch('/api/me',{{credentials:'same-origin'}});if(r.status===401){{$('#gate').classList.add('on');return null;}}return r.json();}}
map.on('load',async()=>{{
  map.addSource('near',{{type:'geojson',data:{{type:'FeatureCollection',features:[]}}}});
  map.addLayer({{id:'near-fill',type:'fill',source:'near',paint:{{'fill-color':C.accent,'fill-opacity':['interpolate',['linear'],['get','w'],1,.04,1000,.22]}}}});
  map.addSource('area',{{type:'geojson',data:{{type:'FeatureCollection',features:[]}}}});
  map.addSource('fill',{{type:'geojson',data:{{type:'FeatureCollection',features:[]}}}});
    map.addLayer({{id:'fill',type:'fill',source:'fill',paint:{{'fill-color':C.accent,'fill-opacity':.06,'fill-opacity-transition':{{duration:0}}}}}});
  map.addLayer({{id:'area-line',type:'line',source:'area',paint:{{'line-color':C.accent,'line-width':2.5}}}});
  data=await load();if(!data)return;render(data,'fly');setTimeout(()=>$('#sheet').classList.add('on'),400);
  // Live: poll for now (a Durable Object will push these later). Only real changes are announced.
  setInterval(async()=>{{const d=await load().catch(()=>null);if(!d)return;
    if(d.waiting>data.waiting)toast(`+${{d.waiting-data.waiting}} ${{d.waiting-data.waiting===1?'neighbour':'neighbours'}} just joined in ${{d.areaLabel}}`);
    else if(d.invited>data.invited)toast('Someone joined through your invite');
    const prosNow=d.pros.reduce((a,p)=>a+p.n,0),prosWas=data.pros.reduce((a,p)=>a+p.n,0);if(prosNow>prosWas)toast(`A new pro joined in ${{d.areaLabel}}`);
    data=d;render(d,false);}},(+new URLSearchParams(location.search).get('poll')||20)*1000);
}});
$('#handle').onclick=()=>{{const m=$('#sheet').classList.toggle('min');$('#handle').setAttribute('aria-expanded',String(!m));$('#handle').setAttribute('aria-label',m?'Show more':'Show less');}};
$('#ask').onsubmit=e=>{{e.preventDefault();const v=$('#q').value.trim();location.href='/request'+(v?'?q='+encodeURIComponent(v):'');}};
const share=async(url,text)=>{{if(navigator.share){{try{{await navigator.share({{text,url}});}}catch(_){{}}}}else{{await navigator.clipboard.writeText(url);toast('Link copied');}}}};
$('#share').onclick=()=>data&&share(`https://scoo.app/r/${{data.code}}`,`I'm on the Scoo early list: a pro calls you back in 60 seconds. Join with my link and we both get $10.`);
$('#pro').onclick=()=>data&&share(`https://scoo.app/pro/${{data.code}}`,`Thought of you: Scoo gives pros a free AI receptionist that answers the calls you miss and books the job. Claim yours here.`);
}})();
</script></body></html>'''
open('app.html', 'w').write(page)
print('ok')
