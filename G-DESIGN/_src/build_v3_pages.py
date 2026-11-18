#!/usr/bin/env python3
"""Étape C — planches V3 des pages Post, Carte de fin, Séries & classement (style « Socles de nuit », STYLE.md).

Usage : python3 G-DESIGN/_src/build_v3_pages.py   (après build_v3.py, qui produit la page Jeu)
Réutilise le moteur 3D de build_v3.py et le chrome hôte de build_v2.py. Fichiers autonomes, zéro réseau.
"""
from pathlib import Path
import build_v2 as v2
import build_v3 as v3

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "planches" / "v3"

EXTRA_CSS = r"""
.feed-card{width:800px;background:#fff;border-radius:14px;border:1px solid #e3e5e8;padding:14px 20px 12px;margin-bottom:16px}
.feed-img{height:150px;border-radius:12px;background:linear-gradient(135deg,#d9dee4,#c9d0d8)}
.cap{font:500 11px 'Lex';letter-spacing:.12em;text-transform:uppercase;color:#8b9ac0}
.cap.hot{color:#ffc46b}
.big{font:700 60px/.95 'Lex';letter-spacing:-.035em;font-variant-numeric:tabular-nums}
.h2{font:700 23px/1.1 'Lex';letter-spacing:-.02em}
.txt{font:400 14px/1.45 'Lex';color:#b8c3de}
.txt b{color:#fff;font-weight:500}
.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.btn2{height:46px;padding:0 18px;border-radius:23px;border:1px solid rgba(255,255,255,.14);cursor:pointer;color:#eef2fb;font:500 14px 'Lex';
  background:linear-gradient(180deg,rgba(255,255,255,.10),rgba(255,255,255,.03));box-shadow:inset 0 1px 0 rgba(255,255,255,.14)}
.card{border-radius:20px;background:linear-gradient(180deg,rgba(29,42,80,.92),rgba(16,23,48,.94));border:1px solid rgba(255,255,255,.10);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 30px 60px -30px rgba(0,0,0,.8);backdrop-filter:blur(12px)}
.plus{display:inline-block;font:600 12px 'Lex';color:#2a1700;background:#ffc46b;border-radius:8px;padding:2px 7px;vertical-align:middle}
.sock{position:relative;width:30px;height:30px;border-radius:9px;background:linear-gradient(180deg,#2a3c72,#1d2c5c);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 4px 0 #121c3d,0 8px 14px -6px rgba(0,0,0,.7)}
.sock.lit{background:linear-gradient(180deg,#34488a,#24366b)}
.sock.lit::after{content:"";position:absolute;left:50%;top:46%;width:9px;height:9px;margin:-4.5px;border-radius:50%;background:#ffe2b0;
  box-shadow:0 0 0 2px rgba(255,196,107,.25),0 0 16px 4px rgba(255,170,70,.55)}
.sock.miss{opacity:.55}
.sock.today{outline:2px solid #ffc46b;outline-offset:3px}
.sock.future{background:transparent;box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)}
.sock.sm{width:22px;height:22px;border-radius:6px;box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 3px 0 #121c3d}
.sock.sm.lit::after{width:6px;height:6px;margin:-3px}
.cal{display:grid;grid-template-columns:repeat(7,30px);gap:11px 9px}
.cal span{font:500 10px 'Lex';color:#6f7da3;text-align:center}
.lb{display:flex;flex-direction:column;gap:4px}
.lr{display:grid;grid-template-columns:50px 1fr auto;align-items:center;height:34px;padding:0 14px;border-radius:12px;font:400 14px 'Lex';color:#cdd6ec}
.lr .rk{font:600 13px 'Lex';color:#8b9ac0;font-variant-numeric:tabular-nums}
.lr .tm{font:500 14px 'Lex';color:#eef2fb;font-variant-numeric:tabular-nums}
.lr.me{background:linear-gradient(180deg,rgba(255,196,107,.16),rgba(255,196,107,.06));box-shadow:inset 0 0 0 1px rgba(255,196,107,.45)}
.lr.me .rk,.lr.me .tm{color:#ffc46b}
.lr .lamp{display:inline-block;width:7px;height:7px;border-radius:50%;background:#ffc46b;box-shadow:0 0 10px 2px rgba(255,170,70,.6);margin-right:9px;vertical-align:middle}
.gap{height:14px;display:flex;align-items:center;padding-left:22px;color:#4f5c82;letter-spacing:.3em}
.tabs{display:inline-flex;padding:4px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}
.tabs b{padding:7px 14px;border-radius:10px;font:500 13px 'Lex';color:#8b9ac0}
.tabs b.on{background:linear-gradient(180deg,rgba(255,255,255,.14),rgba(255,255,255,.05));color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.18)}
.stat{display:flex;flex-direction:column;gap:3px}
.stat b{font:600 18px 'Lex';color:#fff;font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.thumb{position:relative;width:300px;height:190px;border-radius:16px;overflow:hidden}
.thumb canvas{position:absolute;inset:0;width:100%;height:100%}
.thumb .s-ui{left:14px;right:14px;bottom:12px}
.toast{padding:10px 16px;border-radius:14px;font:500 13px 'Lex';color:#eef2fb;background:linear-gradient(180deg,#24335f,#18224a);border:1px solid rgba(255,255,255,.12)}
.compose{width:330px;border-radius:14px;background:#fff;border:1px solid #e3e5e8;padding:12px 14px;font:400 13px/1.45 system-ui;color:#1c1c1c}
.compose small{display:block;color:#6b7178;margin-bottom:6px;font-size:11.5px}
"""

HOST_JS = r"""
function cv(cfg){return `<canvas data-view="${cfg.mob?"mob":"desk"}" data-cfg='${JSON.stringify(cfg)}'></canvas>`}
function deskPost(title,h,inner,below){return `<div class="host"><div class="h-top"><div class="a"></div><div class="s">Search</div><div class="a"></div></div>
 <div class="h-wrap"><div><div class="post"><div class="p-head"><i></i><b>r/SignalValley</b>· u/signal-ops · 2h</div>
 <div class="p-title">${title}</div><div class="slot" style="width:760px;height:${h}px">${inner}</div>
 <div class="p-act"><span>418 comments</span><span>Share</span></div></div>${below||""}</div>
 <div class="side"><b>r/SignalValley</b>One valley network to fix every day. Same puzzle for everyone, new one at midnight UTC.</div></div></div>`}
function mobPost(title,h,inner,below,bar){return `<div class="host"><div class="m-st"><span>9:41</span><span>●●●</span></div>
 <div class="m-bar">${bar||'<u></u>r/SignalValley'}</div>
 <div class="m-post"><div class="p-head"><i></i><b>${bar?"r/SignalValley":"u/signal-ops"}</b>· 2h</div><div class="p-title">${title}</div></div>
 <div class="slot" style="width:390px;height:${h}px;border-radius:0">${inner}</div>
 <div class="m-act"><span>418 comments</span><span>Share</span></div>${below||""}</div>`}
"""

# ------------------------------------------------------------------ 00 POST
POST_JS = r"""
const STREAK=6;
function inlineDesk(){return `<div class="game s-game">${cv({board:"dark",fresh:12,fov:24,tilt:1.5,halfW:6.4,vk:.62,tx:-3.1,tz:.5})}
  <div class="s-ui" style="left:34px;top:34px;width:330px;display:flex;flex-direction:column;gap:14px">
    <div class="cap">Daily puzzle · Network 12 · Nov 18</div>
    <div class="big" style="font-size:64px">Signal</div>
    <div class="txt" style="font-size:15px">The valley went dark. <b>Light the right towers</b>: each number counts lit towers of its kind around it.</div>
    <div class="row"><div class="pill" style="font-size:14px"><em>today</em>1,284 solved</div><div class="pill hot" style="font-size:14px"><em>your streak</em><b>${STREAK}</b></div></div>
    <div class="row" style="margin-top:6px;gap:14px"><button class="tx" style="width:200px">Tune in</button><span class="hint">about 3 min</span></div>
  </div></div>`}
function inlineMob(){return `<div class="game s-game">${cv({mob:true,board:"dark",fresh:12,fov:30,tilt:1.7,halfW:4.3,vk:1.3,ty:0,tz:3.2})}
  <div class="s-ui" style="left:18px;right:18px;bottom:18px;display:flex;flex-direction:column;gap:11px">
    <div class="cap">Daily puzzle · Network 12</div>
    <div class="row" style="justify-content:space-between;align-items:flex-end"><div class="big" style="font-size:44px">Signal</div><div class="pill hot" style="font-size:13px;padding:6px 10px"><em>streak</em><b>${STREAK}</b></div></div>
    <div class="txt" style="font-size:13px">The valley went dark. <b>Light the right towers.</b> 1,284 solved today.</div>
    <button class="tx" style="height:50px">Tune in</button>
  </div></div>`}
const BELOW_D=`<div class="feed-card"><div class="p-head"><i style="background:#c9d0d8"></i><b>r/nightphotography</b>· 5h</div><div class="p-title">Long exposure over the reservoir</div><div class="feed-img"></div></div>`;
const BELOW_M=`<div style="background:#fff;margin-top:8px;padding:10px 16px"><div class="p-head"><i style="background:#c9d0d8"></i><b>r/nightphotography</b>· 5h</div><div class="p-title" style="font-size:15px;margin:4px 0 8px">Long exposure over the reservoir</div><div class="feed-img" style="height:120px"></div></div>`;
function DESK(){return deskPost("Daily network #12 · Nov 18",420,inlineDesk(),BELOW_D)}
function MOB(){return mobPost("Daily network #12 · Nov 18",470,inlineMob(),BELOW_M,'<span style="font-size:17px">Home</span>')}
function STATES_HTML(){return `
 <div><h2>Variantes du post (même post, selon le joueur)</h2><div class="srow">
  <div class="sitem"><div class="thumb s-game">${cv({board:"play",fov:26,tilt:1.6,halfW:5.6,vk:.7,tz:2.4,static:1})}<div class="s-ui row" style="justify-content:space-between"><div class="pill" style="font-size:13px"><em>in progress</em>02:47</div><button class="tx" style="height:40px;width:110px;font-size:14px">Resume</button></div></div>En cours<small>la partie reprend où elle était</small></div>
  <div class="sitem"><div class="thumb s-game">${cv({board:"solved",fov:26,tilt:1.6,halfW:5.6,vk:.7,tz:2.4})}<div class="s-ui row" style="justify-content:space-between"><div class="pill hot" style="font-size:13px"><em>solved</em><b>3:12</b></div><button class="btn2" style="height:40px">See result</button></div></div>Déjà résolu<small>la vallée reste allumée</small></div>
  <div class="sitem"><div class="thumb s-game">${cv({board:"dark",fov:26,tilt:1.6,halfW:5.6,vk:.7,tz:2.4})}<div class="s-ui row" style="justify-content:space-between"><span class="txt" style="font-size:12.5px">Streak ended at 6.</span><button class="tx" style="height:40px;width:150px;font-size:14px">Start a new one</button></div></div>Série cassée<small>ton neutre, pas de reproche</small></div>
 </div></div>`}
"""

# ------------------------------------------------------------------ 02 FIN
FIN_JS = r"""
const week=[1,1,1,1,1,1,1].map((v,i)=>`<i class="sock sm lit${i===6?" today":""}"></i>`).join("");
function cardDesk(){return `<div class="s-ui card" style="left:28px;right:28px;bottom:26px;padding:22px 24px;display:grid;grid-template-columns:1fr 1.15fr 1fr;gap:24px;align-items:center">
   <div><div class="cap hot">Signal clear</div><div class="big" style="margin:8px 0 8px">3:12</div><div class="txt">Faster than <b>64%</b> of today's 1,284 operators. Rank <b>#312</b>.</div></div>
   <div style="border-left:1px solid rgba(255,255,255,.08);padding-left:24px"><div class="cap">Streak</div><div class="row" style="margin:8px 0 12px;gap:10px"><span class="big" style="font-size:52px">7</span><span class="plus">+1</span></div><div class="row" style="gap:7px">${week}</div></div>
   <div style="display:flex;flex-direction:column;gap:10px"><button class="tx">Share your time</button><button class="btn2">Copy result</button><div class="hint" style="text-align:left">Next network in <b style="color:#eef2fb;font-weight:500">06:41:12</b></div></div>
 </div>`}
function DESK(){return deskPost("Daily network #12 · Nov 18",640,`<div class="game s-game">${cv({board:"solved",wave:1,boost:1,fov:24,tilt:1.9,halfW:7.4,vk:.75,tz:2.6})}
   <div class="s-ui" style="left:28px;top:26px"><div class="s-title">Signal</div><div class="s-sub">Network 12 · Tue Nov 18</div></div>
   <div class="s-ui pills" style="right:26px;top:26px"><div class="pill"><em>lit</em>12</div><div class="pill hot"><em>25 / 25</em><b>right</b></div></div>
   ${cardDesk()}</div>`)}
function MOB(){return mobPost("Daily network #12 · Nov 18",646,`<div class="game s-game">${cv({mob:true,board:"solved",wave:1,boost:1,fov:30,tilt:2.0,halfW:4.6,vk:1.0,tz:4.4})}
   <div class="s-ui" style="left:18px;top:18px"><div class="s-title" style="font-size:26px">Signal</div><div class="s-sub">Network 12 · Nov 18</div></div>
   <div class="s-ui card" style="left:14px;right:14px;bottom:14px;padding:18px;display:flex;flex-direction:column;gap:14px">
     <div class="row" style="justify-content:space-between;align-items:flex-end">
       <div><div class="cap hot">Signal clear</div><div class="big" style="font-size:48px;margin-top:6px">3:12</div></div>
       <div style="text-align:right"><div class="cap">Streak</div><div class="row" style="justify-content:flex-end;gap:8px;margin-top:6px"><span class="big" style="font-size:40px">7</span><span class="plus">+1</span></div></div></div>
     <div class="txt" style="font-size:13px">Faster than <b>64%</b> of today's operators · rank <b>#312</b></div>
     <div class="row" style="gap:6px">${week}</div>
     <button class="tx" style="height:50px">Share your time</button>
     <div class="row" style="justify-content:space-between"><button class="btn2" style="height:40px">Copy result</button><span class="hint">Next in 06:41:12</span></div>
   </div></div>`)}
function STATES_HTML(){return `
 <div><h2>Interactions de la carte</h2><div class="srow">
  <div class="sitem"><div class="compose"><small>Comment as u/you</small>Signal #12 cleared in 3:12 · streak 7. The corner dish was the key.<br><span style="color:#6b7178">|</span></div>« Share your time »<small>ouvre le champ commentaire pré-rempli, sans spoiler</small></div>
  <div class="sitem"><div class="toast">Copied: Signal #12 · 3:12 · streak 7</div>« Copy result »<small>toast verre, 2 s</small></div>
  <div class="sitem"><div class="card" style="padding:14px 16px;width:250px"><div class="cap">Next network in</div><div class="big" style="font-size:34px;margin-top:6px">06:41:12</div></div>Compte à rebours<small>minuit UTC, même réseau pour tous</small></div>
  <div class="sitem"><div class="card" style="padding:14px 16px;width:230px"><div class="cap hot">Streak started</div><div class="row" style="margin-top:8px;gap:8px"><span class="big" style="font-size:40px">1</span><span class="txt" style="font-size:12.5px">Come back tomorrow to make it 2.</span></div></div>Première série<small>remplace le +1</small></div>
 </div></div>`}
"""

# ------------------------------------------------------------------ 03 SÉRIES
SER_JS = r"""
// Novembre 2026 commence un dimanche. Résolu : 14 jours sur 18 ; série en cours 7 (12 → 18).
const MISSED=[4,9,10,11],TODAY=18;
function dayTex(d,st){const c=document.createElement("canvas");c.width=c.height=128;const x=c.getContext("2d");
  x.font="600 64px Lex";x.textAlign="center";x.textBaseline="middle";
  x.fillStyle=st==="lit"?"#eef2fb":st==="miss"?"rgba(150,168,210,.55)":"rgba(150,168,210,.28)";x.fillText(String(d),64,68);
  const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;t.anisotropy=8;return t;}
function makeCal(canvas,cfg){
  const R=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
  R.setPixelRatio(Math.min(devicePixelRatio,2));R.shadowMap.enabled=true;R.shadowMap.type=THREE.PCFSoftShadowMap;
  R.outputEncoding=THREE.sRGBEncoding;R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.0;
  const S=new THREE.Scene();S.add(new THREE.HemisphereLight(0x6f8fe0,0x0a1022,.7));
  const moon=new THREE.DirectionalLight(0xc4d3ff,1.6);moon.position.set(-5,9,4);moon.castShadow=true;moon.shadow.mapSize.set(2048,2048);
  Object.assign(moon.shadow.camera,{left:-6,right:6,top:6,bottom:-6,near:1,far:25});moon.shadow.bias=-.0004;moon.shadow.normalBias=.02;S.add(moon);
  const rim=new THREE.DirectionalLight(0x7f9cff,.55);rim.position.set(3,4,-7);S.add(rim);
  const cam=new THREE.PerspectiveCamera(cfg.fov||24,1,.1,100);const root=new THREE.Group();S.add(root);
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(40,40),new THREE.ShadowMaterial({opacity:.38}));ground.rotation.x=-Math.PI/2;ground.position.y=-.8;ground.receiveShadow=true;S.add(ground);
  const P=.98,inst={R,S,cam,root,canvas,opts:cfg,peds:[],cellObjs:[],links:new THREE.Group(),hover:-1,t0:performance.now()};
  const pl=new THREE.Mesh(roundedBox(7*P+.45,.3,5*P+.45,.45,.08),MAT.plinth);pl.position.y=-.34;pl.receiveShadow=pl.castShadow=true;root.add(pl);
  for(let d=1;d<=30;d++){
    const i=d-1,col=i%7,row=Math.floor(i/7),st=d>TODAY?"future":(MISSED.includes(d)?"miss":"lit");
    const grp=new THREE.Group();grp.position.set((col-3)*P,0,(row-2)*P);
    const h=st==="future"?.12:.32;
    const mat=new THREE.MeshStandardMaterial({color:st==="lit"?0x2a3c72:st==="miss"?0x18234d:0x2a3c72,roughness:.5,metalness:.06,transparent:st==="future",opacity:st==="future"?.22:1});
    const ped=new THREE.Mesh(roundedBox(.82,h,.82,.18,.04),mat);ped.castShadow=st!=="future";ped.receiveShadow=true;
    const num=new THREE.Mesh(new THREE.PlaneGeometry(.46,.46),new THREE.MeshBasicMaterial({map:dayTex(d,st),transparent:true,toneMapped:false}));
    num.rotation.x=-Math.PI/2;num.position.set(-.14,h+.003,.14);
    grp.add(ped,num);
    const bulb=new THREE.Mesh(new THREE.SphereGeometry(.085,24,16),st==="lit"?MAT.bulbOn:MAT.bulbOff);bulb.position.set(.12,h+.08,-.12);
    if(st!=="future")grp.add(bulb);
    const light=new THREE.PointLight(AMBER,st==="lit"?1.5:0,2.2,2);light.position.set(.12,h+.4,-.12);
    const glow=new THREE.Sprite(new THREE.SpriteMaterial({map:GLOW,color:0xffc46b,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false,opacity:st==="lit"?.7:0}));
    glow.scale.setScalar(.8);glow.position.set(.12,h+.1,-.12);
    const rings=[0,1].map(()=>{const m=new THREE.Mesh(new THREE.RingGeometry(.4,.43,64),new THREE.MeshBasicMaterial({color:0xffc46b,transparent:true,opacity:0,toneMapped:false,depthWrite:false}));m.rotation.x=-Math.PI/2;m.position.y=h+.02;return m});
    grp.add(light,glow,...rings);root.add(grp);
    inst.cellObjs.push({grp,ped,num,light,glow,rings,lit:st==="lit",fresh:d===TODAY,targetY:st==="miss"?-.06:0,ant:{userData:{bulb}}});
  }
  return inst;
}
function EXTRA_BOOT(){document.querySelectorAll("canvas[data-cal]").forEach(c=>INST.push(makeCal(c,JSON.parse(c.dataset.cal))));}
function calCv(cfg){return `<canvas data-cal='${JSON.stringify(cfg)}'></canvas>`}
const LB=[[1,"u/ridgewalker","1:04",1],[2,"u/quietnode","1:19",1],[3,"u/lumen_k","1:27",1]];
const ME=[312,"u/you","3:12","me"];
function lb(){const r=x=>`<div class="lr ${x[3]==="me"?"me":""}"><span class="rk">#${x[0]}</span><span>${x[3]===1?'<i class="lamp"></i>':""}${x[1]}</span><span class="tm">${x[2]}</span></div>`;
  return `<div class="lb">${LB.map(r).join("")}<div class="gap">···</div>${r(ME)}</div>`}
function DESK(){return deskPost("Daily network #12 · Nov 18",640,`<div class="game s-game">${calCv({fov:24,tilt:1.75,halfW:6.6,vk:.75,tz:2.6})}
   <div class="s-ui" style="left:28px;top:26px"><div class="s-title">Signal</div><div class="s-sub">November · 14 of 18 lit</div></div>
   <div class="s-ui" style="right:26px;top:26px"><div class="tabs"><b>Puzzle</b><b class="on">Streaks & board</b></div></div>
   <div class="s-ui card" style="left:28px;right:28px;bottom:26px;padding:20px 22px;display:grid;grid-template-columns:.8fr 1.25fr .85fr;gap:24px;align-items:stretch">
     <div><div class="cap hot">Current streak</div><div class="row" style="gap:8px;margin:8px 0 10px"><span class="big">7</span><span class="txt">days</span></div><div class="txt" style="font-size:13px">Best <b>12</b> · missed Nov 4, 9–11</div></div>
     <div style="border-left:1px solid rgba(255,255,255,.08);padding-left:22px"><div class="row" style="justify-content:space-between;margin-bottom:6px"><span class="cap">Today's fastest</span><span class="cap">1,284 solved</span></div>${lb()}</div>
     <div style="display:flex;flex-direction:column;justify-content:space-between;gap:12px"><div class="stat"><span class="cap">Median time</span><b>3:41</b></div><div class="stat"><span class="cap">First transmit</span><b>61%</b></div><button class="tx" style="height:46px;font-size:14px">Post your time</button></div>
   </div></div>`)}
function MOB(){return mobPost("Daily network #12 · Nov 18",646,`<div class="game s-game">${calCv({fov:30,tilt:1.9,halfW:4.6,vk:1.0,tz:5.0})}
   <div class="s-ui" style="left:16px;right:16px;top:16px;display:flex;justify-content:space-between;align-items:center"><div><div class="s-title" style="font-size:24px">Signal</div><div class="s-sub">November · 14 of 18 lit</div></div><div class="tabs"><b style="padding:6px 10px">Puzzle</b><b class="on" style="padding:6px 10px">Streaks</b></div></div>
   <div class="s-ui card" style="left:14px;right:14px;bottom:14px;padding:16px 12px 14px;display:flex;flex-direction:column;gap:10px">
     <div class="row" style="justify-content:space-between;align-items:flex-end;padding:0 6px">
       <div><div class="cap hot">Current streak</div><div class="row" style="gap:8px;margin-top:4px"><span class="big" style="font-size:44px">7</span><span class="txt">days</span></div></div>
       <div style="text-align:right"><div class="cap">Best</div><div class="h2" style="margin-top:4px">12</div></div></div>
     <div class="row" style="justify-content:space-between;padding:4px 6px 0;border-top:1px solid rgba(255,255,255,.08)"><span class="cap" style="margin-top:8px">Today's fastest</span><span class="cap" style="margin-top:8px">1,284 solved</span></div>
     ${lb()}
     <button class="tx" style="height:48px;font-size:15px">Post your time</button>
   </div></div>`)}
function STATES_HTML(){return `
 <div><h2>Jours du calendrier (socles 3D)</h2><div class="srow" style="gap:22px">
  <div class="sitem"><i class="sock lit"></i>Résolu<small>lampe allumée</small></div>
  <div class="sitem"><i class="sock miss"></i>Manqué<small>socle éteint, enfoncé</small></div>
  <div class="sitem"><i class="sock lit today"></i>Aujourd'hui<small>anneaux ambrés</small></div>
  <div class="sitem"><i class="sock future"></i>À venir<small>socle de verre</small></div>
 </div></div>
 <div><h2>Lignes du classement</h2><div class="srow" style="flex-direction:column;align-items:stretch;width:330px;background:#141d3b;padding:10px;border-radius:16px">
  <div class="lr"><span class="rk">#1</span><span><i class="lamp"></i>u/ridgewalker</span><span class="tm">1:04</span></div>
  <div class="lr me"><span class="rk">#312</span><span>u/you</span><span class="tm">3:12</span></div>
  <div class="lr" style="opacity:.55"><span class="rk">—</span><span>Not solved yet</span><span class="tm">—</span></div>
 </div></div>`}
"""

TEMPLATE = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Signal · V3 · {name}</title>
<style>
{fonts}
:root{{--accent:#ffc46b}}
{shell}
{css}
{extra}
.states{{flex-wrap:wrap}}
.srow{{align-items:flex-start}}
</style></head><body>
<div id="fit"><div class="board">
 <section class="intro">
  <div><div class="tag">Signal · page {page} · planche V3 · étape C</div><h1>{title}</h1></div>
  <p>{pitch}</p>
  <p class="refs">Style : <b>STYLE.md</b> (« Socles de nuit », validé sur la page Jeu). Données cohérentes : réseau 12 du 18/11, série 6 avant, 7 après, 3:12, rang 312 sur 1,284.</p>
 </section>
 <div class="frames">
  <div><div class="flabel">Desktop · 1440 × 900</div><div class="frame desk" id="desk"></div></div>
  <div><div class="flabel">Mobile · 390 × 844</div><div class="frame mob" id="mob"></div></div>
 </div>
 <section class="states" id="states"></section>
</div></div>
<script>{three}</script>
<script>
{data}
{engine}
{host}
{page_js}
document.getElementById("desk").innerHTML=DESK();
document.getElementById("mob").innerHTML=MOB();
document.getElementById("states").innerHTML=STATES_HTML();
function fit(){{const el=document.getElementById("fit"),s=Math.min(1,innerWidth/1930);el.style.transform=`scale(${{s}})`;document.body.style.height=el.offsetHeight*s+"px";}}
addEventListener("resize",fit);fit();
</script></body></html>"""

PAGES = [
    ("00-post", "Post", "Post", "Post — la vallée éteinte dans le feed",
     "Vue inline du post : la console est là, éteinte, avec une seule onde qui appelle au centre. À gauche, le nom du jeu, la règle en une phrase, "
     "la preuve sociale du jour et la série du joueur, puis une seule touche chaude : « Tune in ». Trois variantes selon le joueur : en cours, déjà résolu, série cassée.",
     POST_JS),
    ("02-fin", "Fin", "Carte de fin", "Carte de fin — la vallée s'allume",
     "À la victoire, les 12 lampes s'allument en vague, de l'avant vers l'arrière, puis les fils de lumière se tendent. La carte verre en bas donne le temps, "
     "le rang, la série avec son +1 et la semaine en socles allumés. L'action chaude invite à poster son temps en commentaire ; le compte à rebours ramène demain.",
     FIN_JS),
    ("03-series", "Series", "Séries & classement", "Séries & classement",
     "Refaite dans le style verrouillé : le mois de novembre devient une console de 30 socles 3D. Jour réparé = lampe allumée, jour manqué = socle éteint et enfoncé, "
     "aujourd'hui = anneaux ambrés, jours à venir = socles de verre. La carte verre en bas porte la série, les plus rapides du jour (podium avec lampe, ligne du joueur) et les chiffres de la communauté.",
     SER_JS),
]


def main():
    engine = v3.JS.split("function ui(L){")[0] + "function game(){return ''}\n" + "\n// ---------- 3D ----------" + v3.JS.split("// ---------- 3D ----------")[1]
    fonts = "\n".join([v2.font('Lex', 'lexend-latin-400-normal.woff2', 400), v2.font('Lex', 'lexend-latin-500-normal.woff2', 500),
                       v2.font('Lex', 'lexend-latin-700-normal.woff2', 700)])
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, name, page, title, pitch, js in PAGES:
        html = TEMPLATE.format(name=name, page=page, title=title, pitch=pitch, fonts=fonts, shell=v2.SHELL_CSS, css=v3.CSS,
                               extra=EXTRA_CSS, three=v3.THREE, data=v2.DATA_JS, engine=engine, host=HOST_JS, page_js=js)
        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        print("écrit", (OUT / f"{slug}.html").relative_to(HERE.parent.parent), f"{len(html)//1024} Ko")


if __name__ == "__main__":
    main()
