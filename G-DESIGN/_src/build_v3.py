#!/usr/bin/env python3
"""Planche V3 de la page Jeu — 3D temps réel (Three.js 0.149, MIT, embarqué), lumière et matière.

Usage : python3 G-DESIGN/_src/build_v3.py
Sortie : G-DESIGN/planches/v3/01-socles.html — autonome, zéro réseau, jouable (clic = allumer / éteindre).
"""
from pathlib import Path
import build_v2 as v2

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "planches" / "v3"
THREE = (HERE / "vendor" / "three-0.149.0.min.js").read_text(encoding="utf-8")

CSS = r"""
.s-game{background:radial-gradient(90% 70% at 50% 38%,#1b2a52 0%,#0d1530 55%,#070b1b 100%);color:#eef2fb;font-family:'Lex',system-ui}
.s-game canvas{position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:manipulation}
.s-ui{position:absolute;pointer-events:none}
.s-ui *{pointer-events:auto}
.s-title{font:700 30px/1 'Lex';letter-spacing:-.03em}
.s-sub{font:400 12.5px 'Lex';color:#8b9ac0;margin-top:6px}
.pills{display:flex;gap:8px}
.pill{display:flex;align-items:baseline;gap:7px;padding:8px 13px;border-radius:14px;
  background:linear-gradient(180deg,rgba(255,255,255,.10),rgba(255,255,255,.03));
  border:1px solid rgba(255,255,255,.10);box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 8px 20px -10px rgba(0,0,0,.6);
  backdrop-filter:blur(10px);font:500 16px 'Lex';font-variant-numeric:tabular-nums}
.pill em{font-style:normal;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#8b9ac0}
.pill.hot b{color:#ffc46b;font-weight:600}
.rule{font:400 14px/1.45 'Lex';color:#b8c3de;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.rule b{color:#fff;font-weight:500}
.kind{display:inline-flex;align-items:center;gap:5px;padding:3px 9px 3px 6px;border-radius:10px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);font-size:12.5px;color:#dbe3f5}
.meter{display:flex;gap:3px}
.meter i{flex:1;height:6px;border-radius:3px;background:rgba(255,255,255,.12);transition:background .25s}
.meter i.met{background:#eef2fb}
.meter i.over{background:#ffc46b}
.mtxt{display:flex;justify-content:space-between;font:500 11.5px 'Lex';letter-spacing:.06em;text-transform:uppercase;color:#8b9ac0;margin-bottom:7px}
.mtxt b{color:#fff;font-weight:600}
.tx{height:54px;border:0;border-radius:27px;cursor:pointer;font:600 16px 'Lex';letter-spacing:.01em;color:#2a1700;
  background:linear-gradient(180deg,#ffd9a0 0%,#ffbf62 55%,#f2a443 100%);
  box-shadow:inset 0 1.5px 0 rgba(255,255,255,.7),inset 0 -2px 0 rgba(150,80,10,.25),0 4px 0 #b9721f,0 16px 30px -10px rgba(255,170,70,.65);
  transition:transform .08s,box-shadow .08s}
.tx:active,.tx.down{transform:translateY(3px);box-shadow:inset 0 1.5px 0 rgba(255,255,255,.6),0 1px 0 #b9721f,0 8px 18px -10px rgba(255,170,70,.6)}
.tx.idle{background:linear-gradient(180deg,#3a4466,#2a3253);color:#8b9ac0;box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 4px 0 #161b30}
.hint{font:400 11.5px 'Lex';color:#6f7da3;text-align:center}
.sc{width:124px;height:124px;border-radius:16px;overflow:hidden;position:relative;background:radial-gradient(80% 80% at 50% 40%,#1b2a52,#0a1024)}
.sc canvas{width:124px;height:124px;display:block}
.glass{padding:12px 16px;border-radius:16px;background:linear-gradient(180deg,#1d2a50,#141d3b);border:1px solid rgba(255,255,255,.1);box-shadow:inset 0 1px 0 rgba(255,255,255,.12);color:#b8c3de;font:400 13px/1.45 'Lex'}
.glass b{color:#fff;font-weight:600}
.srow{align-items:flex-start}
"""

JS = r"""
// ---------- état jouable (partagé desktop / mobile) ----------
const ST={on:PAT.map(r=>[...r].map(c=>c==="1")),fresh:FRESH[0]*5+FRESH[1],freshT:0};
const SOL=["00100","01111","00001","10111","10100"];
const GRIDS={dark:SOL.map(r=>[...r].map(()=>false)),solved:SOL.map(r=>[...r].map(c=>c==="1"))};
function cells(G=ST.on){const out=[];for(let r=0;r<5;r++)for(let c=0;c<5;c++){const f=FREQ[r][c];let n=0;
  for(let dr=-1;dr<=1;dr++)for(let dc=-1;dc<=1;dc++){if(!dr&&!dc)continue;const R=r+dr,C=c+dc;
    if(R<0||C<0||R>4||C>4)continue;if(G[R][C]&&FREQ[R][C]===f)n++;}
  const t=CLUES[r][c];out.push({i:r*5+c,r,c,kind:f==="A"?"mast":"dish",target:t,cur:n,on:G[r][c],
    status:n===t?"met":(n>t?"over":"under")});}return out;}
const KIND_ICON={mast:`<svg width="12" height="16" viewBox="0 0 12 16"><path d="M6 1 L9 15 H3Z" fill="#dbe3f5"/><circle cx="6" cy="2" r="1.8" fill="#ffc46b"/></svg>`,
  dish:`<svg width="16" height="16" viewBox="0 0 16 16"><path d="M2 5 Q5 13 14 8Z" fill="#dbe3f5"/><path d="M7 11 L8 15" stroke="#dbe3f5" stroke-width="1.6"/><circle cx="11" cy="4" r="1.8" fill="#ffc46b"/></svg>`};

function ui(L){
  const meter=`<div class="mtxt"><span><b class="js-on">${TOWERS}</b> lit</span><span><b class="js-met">${MET}</b> / 25 numbers right</span></div><div class="meter js-meter">${"<i></i>".repeat(25)}</div>`;
  if(!L.mob) return `
   <div class="s-ui" style="left:28px;top:26px"><div class="s-title">Signal</div><div class="s-sub">Network 12 · Tue Nov 18</div></div>
   <div class="s-ui pills" style="right:26px;top:26px"><div class="pill"><em>time</em>02:47</div><div class="pill hot"><em>streak</em><b>6</b></div></div>
   <div class="s-ui" style="left:28px;right:28px;bottom:24px;display:grid;grid-template-columns:1fr 210px;gap:28px;align-items:end">
     <div><div class="rule" style="margin-bottom:14px"><b>Each number = lit towers of the same kind around it.</b><span class="kind">${KIND_ICON.mast}round · masts</span><span class="kind">${KIND_ICON.dish}square · dishes</span></div>${meter}</div>
     <button class="tx">Transmit</button>
   </div>`;
  return `
   <div class="s-ui" style="left:18px;top:18px"><div class="s-title" style="font-size:26px">Signal</div><div class="s-sub">Network 12 · Nov 18</div></div>
   <div class="s-ui pills" style="right:16px;top:18px"><div class="pill" style="padding:7px 10px;font-size:14px">02:47</div><div class="pill hot" style="padding:7px 10px;font-size:14px"><em>streak</em><b>6</b></div></div>
   <div class="s-ui" style="left:18px;right:18px;bottom:18px;display:flex;flex-direction:column;gap:12px">
     <div class="rule" style="font-size:13px"><b>Each number = lit towers of the same kind around it.</b><span class="kind">${KIND_ICON.mast}round</span><span class="kind">${KIND_ICON.dish}square</span></div>
     <div>${meter}</div>
     <button class="tx" style="height:52px">Transmit</button>
   </div>`;
}
function game(L){return `<div class="game s-game"><canvas data-view="${L.mob?"mob":"desk"}"></canvas>${ui(L)}</div>`}
function stateCell(x){return `<div class="sc"><canvas data-state='${JSON.stringify(x)}' width="248" height="248"></canvas></div>`}
function extras(){return `
 <div class="sitem"><button class="tx" style="width:180px">Transmit</button>Prêt<small>touche physique, 4 px d'épaisseur</small></div>
 <div class="sitem"><button class="tx down" style="width:180px">Transmit</button>Pressé<small>la touche s'enfonce</small></div>
 <div class="sitem"><div class="glass" style="width:270px"><b>Static.</b> 8 numbers are still off. The lit lines show who talks to whom.</div>Échec<small>carte verre, 4 s</small></div>
 <div class="sitem"><div class="glass" style="width:220px"><div class="mtxt" style="margin-bottom:8px"><span>Powering the valley</span></div><div class="meter">${'<i class="met"></i>'.repeat(9)}${"<i></i>".repeat(16)}</div></div>Chargement<small>les socles s'allument un à un</small></div>`}

// ---------- 3D ----------
THREE.ColorManagement.legacyMode=false;
const AMBER=0xffb85c, PITCH=1.18;
function roundedBox(w,h,d,r,b){
  const s=new THREE.Shape(),x=-(w/2-b),y=-(d/2-b),W=w-2*b,D=d-2*b,R=Math.min(r,W/2,D/2);
  s.moveTo(x+R,y);s.lineTo(x+W-R,y);s.quadraticCurveTo(x+W,y,x+W,y+R);s.lineTo(x+W,y+D-R);s.quadraticCurveTo(x+W,y+D,x+W-R,y+D);
  s.lineTo(x+R,y+D);s.quadraticCurveTo(x,y+D,x,y+D-R);s.lineTo(x,y+R);s.quadraticCurveTo(x,y,x+R,y);
  const g=new THREE.ExtrudeGeometry(s,{depth:h-2*b,bevelEnabled:true,bevelSize:b,bevelThickness:b,bevelSegments:5,curveSegments:10});
  g.rotateX(-Math.PI/2);g.translate(0,b,0);g.computeVertexNormals();return g;
}
function glowTex(){const c=document.createElement("canvas");c.width=c.height=128;const x=c.getContext("2d");
  const g=x.createRadialGradient(64,64,0,64,64,64);g.addColorStop(0,"rgba(255,214,150,1)");g.addColorStop(.25,"rgba(255,184,92,.55)");g.addColorStop(1,"rgba(255,184,92,0)");
  x.fillStyle=g;x.fillRect(0,0,128,128);return new THREE.CanvasTexture(c);}
let GLOW=null;
function numTex(cell){
  const c=document.createElement("canvas");c.width=256;c.height=192;const x=c.getContext("2d");
  const lit=cell.on;const col=cell.status==="met"?(lit?"#101a40":"#ffffff"):cell.status==="over"?(lit?"#b0600c":"#ffc46b"):(lit?"rgba(16,26,64,.45)":"rgba(150,168,210,.75)");
  x.font="700 128px Lex";x.textAlign="center";x.textBaseline="middle";
  x.shadowColor=cell.status==="met"&&!lit?"rgba(255,255,255,.45)":"transparent";x.shadowBlur=12;
  x.fillStyle=col;x.fillText(String(cell.target),128,104);
  if(cell.status==="over"){x.shadowBlur=0;x.strokeStyle=col;x.lineWidth=7;x.setLineDash([14,10]);x.beginPath();x.arc(128,100,84,0,Math.PI*2);x.stroke();}
  if(cell.status==="met"){x.shadowBlur=0;x.fillStyle=col;x.fillRect(98,176,60,7);}
  const t=new THREE.CanvasTexture(c);t.anisotropy=8;t.encoding=THREE.sRGBEncoding;return t;
}
const MAT={
  ped:()=>new THREE.MeshStandardMaterial({color:0x1d2c5c,roughness:.5,metalness:.06}),
  plinth:new THREE.MeshStandardMaterial({color:0x111a36,roughness:.72,metalness:.1}),
  ceramic:new THREE.MeshStandardMaterial({color:0xe9edf6,roughness:.32,metalness:.02}),
  bulbOff:new THREE.MeshStandardMaterial({color:0x5d6c92,roughness:.25,metalness:.2}),
  bulbOn:new THREE.MeshStandardMaterial({color:0xffe2b0,emissive:0xffa63d,emissiveIntensity:2.4,roughness:.2}),
  link:new THREE.MeshBasicMaterial({color:0xffc46b,transparent:true,opacity:.9,toneMapped:false}),
};
function antenna(kind){
  const g=new THREE.Group();let bulbY,bulbZ=0;
  if(kind==="mast"){
    const base=new THREE.Mesh(new THREE.CylinderGeometry(.1,.12,.06,24),MAT.ceramic);base.position.y=.03;
    const sp=new THREE.Mesh(new THREE.CylinderGeometry(.022,.085,.62,4),MAT.ceramic);sp.position.y=.37;sp.rotation.y=Math.PI/4;
    const ring=new THREE.Mesh(new THREE.TorusGeometry(.07,.012,8,24),MAT.ceramic);ring.rotation.x=Math.PI/2;ring.position.y=.28;
    g.add(base,sp,ring);bulbY=.73;
  }else{
    const st=new THREE.Mesh(new THREE.CylinderGeometry(.03,.07,.26,16),MAT.ceramic);st.position.y=.13;
    const bowl=new THREE.Mesh(new THREE.SphereGeometry(.27,40,14,0,Math.PI*2,0,1.0),MAT.ceramic);
    bowl.material=MAT.ceramic.clone();bowl.material.side=THREE.DoubleSide;
    bowl.scale.set(1,.55,1);bowl.rotation.x=Math.PI-0.85;bowl.position.set(0,.36,0);
    const arm=new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,.3,8),MAT.ceramic);arm.position.set(0,.47,.1);arm.rotation.x=.85;
    g.add(st,bowl,arm);bulbY=.6;bulbZ=.2;
  }
  g.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}});
  const bulb=new THREE.Mesh(new THREE.SphereGeometry(kind==="mast"?.075:.06,24,16),MAT.bulbOff);bulb.position.set(0,bulbY,bulbZ);
  g.add(bulb);g.userData={bulb,bulbY,bulbZ};return g;
}
function makeScene(canvas,opts){
  const R=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:"high-performance"});
  R.setPixelRatio(Math.min(devicePixelRatio,2));R.shadowMap.enabled=true;R.shadowMap.type=THREE.PCFSoftShadowMap;
  R.outputEncoding=THREE.sRGBEncoding;R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.0;
  const S=new THREE.Scene();
  S.add(new THREE.HemisphereLight(0x6f8fe0,0x0a1022,.7));
  const moon=new THREE.DirectionalLight(0xc4d3ff,1.6);moon.position.set(-5,9,4);moon.castShadow=true;
  moon.shadow.mapSize.set(2048,2048);Object.assign(moon.shadow.camera,{left:-5,right:5,top:5,bottom:-5,near:1,far:25});moon.shadow.bias=-.0004;moon.shadow.normalBias=.02;
  S.add(moon);
  const rim=new THREE.DirectionalLight(0x7f9cff,.55);rim.position.set(3,4,-7);S.add(rim);
  const cam=new THREE.PerspectiveCamera(opts.fov||26,1,.1,100);
  const root=new THREE.Group();S.add(root);
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(40,40),new THREE.ShadowMaterial({opacity:.38}));ground.rotation.x=-Math.PI/2;ground.position.y=-.9;ground.receiveShadow=true;S.add(ground);
  const inst={R,S,cam,root,canvas,opts,peds:[],cellObjs:[],links:new THREE.Group(),rings:[],hover:-1};
  root.add(inst.links);
  if(!opts.single){
    const pl=new THREE.Mesh(roundedBox(6.35,.42,6.35,.55,.12),MAT.plinth);pl.position.y=-.46;pl.receiveShadow=true;pl.castShadow=true;root.add(pl);
  }
  const n=opts.single?1:25;
  for(let i=0;i<n;i++){
    const r=Math.floor(i/5),c=i%5, kind=opts.single?opts.single.kind:(FREQ[r][c]==="A"?"mast":"dish");
    const grp=new THREE.Group();
    if(!opts.single)grp.position.set((c-2)*PITCH,0,(r-2)*PITCH);
    const ped=new THREE.Mesh(roundedBox(1,.42,1,kind==="mast"?.47:.14,.06),MAT.ped());ped.castShadow=true;ped.receiveShadow=true;ped.userData.i=i;
    const ant=antenna(kind);ant.scale.setScalar(.8);ant.position.set(0,.42,-.24);
    const num=new THREE.Mesh(new THREE.PlaneGeometry(.6,.45),new THREE.MeshBasicMaterial({transparent:true,toneMapped:false}));
    num.rotation.x=-Math.PI/2;num.position.set(0,.423,.2);
    const light=new THREE.PointLight(AMBER,0,3.4,2);light.position.set(0,.42+ant.userData.bulbY*.8+.3,-.24+ant.userData.bulbZ*.8);
    const glow=new THREE.Sprite(new THREE.SpriteMaterial({map:GLOW,color:0xffc46b,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false,opacity:0}));
    glow.scale.setScalar(opts.boost?1.7:1.1);glow.position.copy(light.position);
    const ringMats=[0,1].map(()=>new THREE.MeshBasicMaterial({color:0xffc46b,transparent:true,opacity:0,toneMapped:false,depthWrite:false}));
    const rings=ringMats.map(m=>{const ri=new THREE.Mesh(new THREE.RingGeometry(.44,.47,64),m);ri.rotation.x=-Math.PI/2;ri.position.y=.44;return ri});
    grp.add(ped,ant,num,light,glow,...rings);root.add(grp);
    inst.peds.push(ped);inst.cellObjs.push({grp,ped,ant,num,light,glow,rings,kind,key:""});
  }
  // interaction
  const ray=new THREE.Raycaster(),m=new THREE.Vector2();
  const pick=e=>{const b=canvas.getBoundingClientRect();m.x=((e.clientX-b.left)/b.width)*2-1;m.y=-((e.clientY-b.top)/b.height)*2+1;
    ray.setFromCamera(m,cam);const h=ray.intersectObjects(inst.peds,false)[0];return h?h.object.userData.i:-1;};
  if(opts.board==="play"){
    canvas.addEventListener("pointermove",e=>{inst.hover=pick(e);canvas.style.cursor=inst.hover>=0?"pointer":"default";});
    canvas.addEventListener("pointerleave",()=>{inst.hover=-1});
    canvas.addEventListener("pointerdown",e=>{const i=pick(e);if(i<0)return;const r=Math.floor(i/5),c=i%5;
      ST.on[r][c]=!ST.on[r][c];ST.fresh=ST.on[r][c]?i:-1;ST.freshT=performance.now();refreshAll();});
  }
  return inst;
}
function sizeCam(inst){
  const {canvas,cam,R,opts}=inst;const w=canvas.clientWidth,h=canvas.clientHeight;if(!w||!h)return;
  R.setSize(w,h,false);cam.aspect=w/h;
  const dir=new THREE.Vector3(0,opts.tilt||1.15,1).normalize();
  const vf=THREE.MathUtils.degToRad(cam.fov)/2,hf=Math.atan(Math.tan(vf)*cam.aspect);
  const half=opts.single?.95:(opts.halfW||3.6);
  const d=Math.max(half/Math.tan(hf),half*(opts.vk||.95)/Math.tan(vf));
  const t=new THREE.Vector3(opts.tx||0,opts.ty||0,opts.tz||0);cam.position.copy(t).addScaledVector(dir,d);cam.lookAt(t);cam.updateProjectionMatrix();
}
function apply(inst,list){
  list.forEach((cell,k)=>{const o=inst.cellObjs[k];
    const key=cell.on+cell.status;
    if(o.key!==key){o.key=key;
      if(o.num.material.map)o.num.material.map.dispose();o.num.material.map=numTex(cell);o.num.material.needsUpdate=true;
      o.ant.userData.bulb.material=cell.on?MAT.bulbOn:MAT.bulbOff;
      o.light.intensity=cell.on?(inst.opts.single?3.2:2.6):0;o.glow.material.opacity=cell.on?.75:0;
      o.ped.material.color.set(cell.on?0x2a3c72:0x1d2c5c);
      o.targetY=cell.on?-.07:0;}
    o.fresh=inst.opts.single?!!cell.fresh:(inst.opts.board==="play"?cell.i===ST.fresh:cell.i===(inst.opts.fresh??-1));
    o.lit=cell.on;o.waveDelay=(cell.r+cell.c)*140+cell.c*20;
  });
  if(inst.opts.single)return;
  inst.links.children.forEach(ch=>ch.geometry.dispose());inst.links.clear();
  for(const a of list)for(const b of list){
    if(!a.on||!b.on||a.kind!==b.kind||b.i<=a.i)continue;if(Math.abs(a.r-b.r)>1||Math.abs(a.c-b.c)>1)continue;
    const pa=inst.cellObjs[a.i].glow.position.clone().add(inst.cellObjs[a.i].grp.position).add(new THREE.Vector3(0,-.07,0));
    const pb=inst.cellObjs[b.i].glow.position.clone().add(inst.cellObjs[b.i].grp.position).add(new THREE.Vector3(0,-.07,0));
    const mid=pa.clone().add(pb).multiplyScalar(.5).add(new THREE.Vector3(0,.32,0));
    inst.links.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(pa,mid,pb),28,.013,6),MAT.link));
  }
}
const INST=[];
function refreshAll(){
  const list=cells();INST.forEach(i=>{if(i.opts.board==="play")apply(i,list)});
  const on=list.filter(x=>x.on).length,met=list.filter(x=>x.status==="met").length;
  document.querySelectorAll(".js-on").forEach(e=>e.textContent=on);
  document.querySelectorAll(".js-met").forEach(e=>e.textContent=met);
  document.querySelectorAll(".js-meter").forEach(m=>[...m.children].forEach((el,k)=>el.className=list[k].status==="under"?"":list[k].status));
  document.querySelectorAll(".s-game .tx").forEach(b=>b.classList.toggle("idle",on===0));
}
function tick(t){
  const reduce=matchMedia("(prefers-reduced-motion:reduce)").matches;
  for(const inst of INST){
    inst.cellObjs.forEach((o,k)=>{
      o.grp.position.y+=((o.targetY||0)-o.grp.position.y)*.25;
      const hov=inst.hover===k;o.ped.material.emissive.set(hov?0x18264d:0x000000);
      const ph=reduce?0:((t-(inst.opts.board==="play"?ST.freshT:0))%1800)/1800;
      o.rings.forEach((ri,j)=>{if(!o.fresh||reduce){ri.material.opacity=0;return;}
        const p=(ph+j*.5)%1;ri.scale.setScalar(1+p*1.7);ri.material.opacity=(1-p)*.85;});
      let w=1;if(inst.opts.wave&&o.lit){w=reduce?1:Math.min(1,Math.max(0,(t-inst.t0-600-o.waveDelay)/380));
        o.light.intensity=(inst.opts.boost?3.6:2.6)*w;o.ant.userData.bulb.material=w>.25?MAT.bulbOn:MAT.bulbOff;o.targetY=w>.25?-.07:0;
        inst.links.visible=(t-inst.t0)>600+8*140+400;}
      if(o.lit&&!reduce)o.glow.material.opacity=(inst.opts.boost?.95:(.68+Math.sin(t*.004+k)*.06))*w;
    });
    inst.R.render(inst.S,inst.cam);
  }
  requestAnimationFrame(tick);
}
async function boot(){
  try{await document.fonts.load("700 100px Lex");}catch(e){}
  GLOW=glowTex();
  document.querySelectorAll("canvas[data-view]").forEach(cv=>{
    const mob=cv.dataset.view==="mob";
    const cfg=Object.assign({board:"play"},mob?{fov:30,tilt:2.1,halfW:3.4,vk:1.0,ty:0,tz:.9}:{fov:24,tilt:1.75,halfW:5.4,vk:.7,ty:0,tz:.75},cv.dataset.cfg?JSON.parse(cv.dataset.cfg):{});
    const inst=makeScene(cv,cfg);inst.t0=performance.now();if(cfg.board!=="play")apply(inst,cells(GRIDS[cfg.board]));INST.push(inst);});
  document.querySelectorAll("canvas[data-state]").forEach(cv=>{
    const x=JSON.parse(cv.dataset.state);const inst=makeScene(cv,{single:x,fov:30,tilt:1.0});inst.root.position.y=-.35;
    apply(inst,[Object.assign({i:0,r:0,c:0},x)]);INST.push(inst);});
  if(typeof EXTRA_BOOT==="function")EXTRA_BOOT();
  const ro=new ResizeObserver(()=>INST.forEach(sizeCam));INST.forEach(i=>{sizeCam(i);ro.observe(i.canvas)});
  refreshAll();requestAnimationFrame(tick);
}
setTimeout(boot,0);
"""


def main():
    d = dict(num=1, of=1, ver="V3", name="Socles", title="V3 — Socles de nuit (3D)", accent="#ffc46b",
             refs="Refs (catégorie <b>narratif-jeu</b>, principes) : <b>Raben Rifaie</b> (une teinte, une seule lumière chaude, matière douce) · "
                  "<b>MemoryQuest</b> (vraie 3D, objets qu'on a envie de presser, lumière qui sort des boutons) · "
                  "<b>Dairy Food Bulgaria</b> (le monde posé en maquette sur un socle qui flotte).",
             pitch="La grille est une console de 25 socles en céramique bleu nuit, posée sur une dalle qui flotte. Chaque socle porte un mât ou une parabole, "
                   "et son chiffre est gravé sur le dessus. Toucher un socle l'enfonce et allume une vraie lampe, qui éclaire ses voisins ; un fil de lumière relie "
                   "les antennes de même sorte. Seules les lampes et la touche « Transmit » sont chaudes. <b>Jouable : cliquez les socles.</b>",
             fonts="", css=CSS, js=JS)
    html = v2.page(d)
    html = html.replace("<script>\n", "<script>" + THREE + "</script>\n<script>\n", 1)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "01-socles.html").write_text(html, encoding="utf-8")
    print("écrit", (OUT / "01-socles.html").relative_to(HERE.parent.parent), f"{len(html)//1024} Ko")


if __name__ == "__main__":
    main()
