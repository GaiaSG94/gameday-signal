#!/usr/bin/env python3
"""Planches V2 de la page Jeu — refs catégorie `narratif-jeu` (hub REFERENCES-DESIGN.md V2).

Usage : python3 G-DESIGN/_src/build_v2.py
Sortie : G-DESIGN/planches/v2/0X-*.html, autonomes (polices embarquées en base64, zéro réseau).
Données : vrai réseau du 2026-11-18 (src/shared/puzzle.ts).
"""
import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "planches" / "v2"


def font(family, file, weight=400, style="normal"):
    b = base64.b64encode((HERE / "fonts" / file).read_bytes()).decode()
    return (f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{b}) format('woff2');"
            f"font-weight:{weight};font-style:{style};font-display:block}}")


DATA_JS = r"""
const FREQ  = ["ABBAB","AABAA","ABBAB","BBBAA","BABAA"];          // A = mât, B = parabole
const CLUES = [[1,2,1,2,0],[1,0,1,1,1],[1,3,2,4,0],[1,4,1,1,1],[1,0,1,2,2]];
const PAT   = ["00100","01111","01001","10100","10000"];          // partie en cours (B3 en trop)
const FRESH = [1,3];
const N=5, on=(r,c)=>PAT[r][c]==="1";
function curOf(r,c){let n=0,f=FREQ[r][c];for(let dr=-1;dr<=1;dr++)for(let dc=-1;dc<=1;dc++){
  if(!dr&&!dc)continue;const R=r+dr,C=c+dc;if(R<0||C<0||R>=N||C>=N)continue;if(on(R,C)&&FREQ[R][C]===f)n++;}return n;}
const CELLS=[];for(let r=0;r<N;r++)for(let c=0;c<N;c++){const t=CLUES[r][c],cur=curOf(r,c);
  CELLS.push({r,c,kind:FREQ[r][c]==="A"?"mast":"dish",target:t,cur,on:on(r,c),fresh:r===FRESH[0]&&c===FRESH[1],
  status:cur===t?"met":(cur>t?"over":"under")});}
const TOWERS=CELLS.filter(x=>x.on).length, MET=CELLS.filter(x=>x.status==="met").length;
const LINKS=[];for(const a of CELLS)for(const b of CELLS){if(!a.on||!b.on||a.kind!==b.kind)continue;
  if(b.r*N+b.c<=a.r*N+a.c)continue;if(Math.abs(a.r-b.r)<=1&&Math.abs(a.c-b.c)<=1)LINKS.push([a,b]);}
const STATES=[
  [{kind:"mast",target:2,cur:1,on:false,status:"under"},"Mât éteint","chiffre pas atteint"],
  [{kind:"dish",target:2,cur:1,on:false,status:"under"},"Parabole éteinte",""],
  [{kind:"mast",target:1,cur:1,on:true,status:"met"},"Allumé","chiffre atteint"],
  [{kind:"dish",target:3,cur:3,on:true,fresh:true,status:"met"},"Vient d'être allumé","ondes, 900 ms"],
  [{kind:"mast",target:1,cur:2,on:false,status:"over"},"Trop","une voisine de trop"],
];
"""

SHELL_CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#e9e7e2;color:#1a1a1a;font-family:'Lex',system-ui,sans-serif}
#fit{transform-origin:0 0}
.board{width:1930px;padding:36px 36px 44px}
.intro{display:flex;gap:56px;align-items:flex-end;margin-bottom:24px}
.intro h1{font:600 30px/1.05 'Lex',system-ui;letter-spacing:-.02em}
.intro .tag{font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.55;margin-bottom:8px}
.intro p{font-size:13.5px;line-height:1.5;max-width:62ch;opacity:.85}
.intro .refs{font-size:12px;line-height:1.5;max-width:46ch;opacity:.7}
.frames{display:flex;gap:44px;align-items:flex-start}
.flabel{font-size:11px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-bottom:8px}
.frame{position:relative;overflow:hidden;border-radius:12px;box-shadow:0 1px 0 rgba(0,0,0,.08),0 20px 50px -30px rgba(0,0,0,.4)}
.desk{width:1440px;height:900px}
.mob{width:390px;height:844px;border-radius:46px;box-shadow:0 0 0 10px #121212,0 30px 60px -30px rgba(0,0,0,.5)}
.states{margin-top:30px;display:flex;gap:40px;align-items:flex-start}
.states h2{font-size:11px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;font-weight:500;margin-bottom:10px}
.srow{display:flex;gap:14px;align-items:flex-end}
.sitem{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:12px}
.sitem small{opacity:.55;font-size:11px}

/* hôte neutre (aucune marque) */
.host{position:absolute;inset:0;background:#f3f4f5;color:#1c1c1c;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.h-top{height:52px;background:#fff;border-bottom:1px solid #e3e5e8;display:flex;align-items:center;padding:0 20px;gap:14px}
.h-top .s{margin:0 auto;width:460px;height:34px;border-radius:17px;background:#eef0f2;color:#8a9097;font-size:13px;display:flex;align-items:center;padding:0 16px}
.h-top .a{width:30px;height:30px;border-radius:50%;background:#dfe2e6}
.h-wrap{display:flex;gap:24px;justify-content:center;padding-top:20px}
.post{width:800px;background:#fff;border-radius:14px;padding:14px 20px 12px;border:1px solid #e3e5e8}
.p-head{display:flex;align-items:center;gap:8px;font-size:12px;color:#6b7178}
.p-head i{width:22px;height:22px;border-radius:50%;background:var(--accent)}
.p-head b{color:#1c1c1c}
.p-title{font-size:18px;font-weight:600;margin:6px 0 12px;letter-spacing:-.01em}
.slot{position:relative;overflow:hidden;border-radius:12px}
.p-act{display:flex;gap:8px;margin-top:10px}
.p-act span{font-size:12px;color:#4a5057;background:#eef0f2;border-radius:15px;padding:6px 13px}
.side{width:300px;background:#fff;border-radius:14px;border:1px solid #e3e5e8;padding:16px;font-size:13px;line-height:1.5;color:#4a5057;height:max-content}
.side b{display:block;color:#1c1c1c;font-size:14px;margin-bottom:4px}
.m-st{height:44px;display:flex;justify-content:space-between;align-items:center;padding:0 30px;font-size:14px;font-weight:600;background:#fff}
.m-bar{height:46px;display:flex;align-items:center;gap:10px;padding:0 16px;font-size:14px;font-weight:600;background:#fff}
.m-bar u{width:9px;height:9px;border-left:2px solid #222;border-bottom:2px solid #222;transform:rotate(45deg)}
.m-post{background:#fff;padding:2px 16px 10px}
.m-post .p-title{font-size:15px;margin:4px 0 0}
.m-act{height:46px;display:flex;align-items:center;gap:8px;padding:0 16px;background:#fff}
.m-act span{font-size:12px;color:#4a5057;background:#eef0f2;border-radius:15px;padding:5px 12px}
.game{position:absolute;inset:0;overflow:hidden}
.tap{cursor:pointer}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""

SHELL_JS = r"""
const DESK={w:760,h:640,mob:false}, MOB={w:390,h:646,mob:true};
function hostDesk(){return `<div class="host"><div class="h-top"><div class="a"></div><div class="s">Search</div><div class="a"></div></div>
 <div class="h-wrap"><div class="post"><div class="p-head"><i></i><b>r/SignalValley</b>· u/signal-ops · 2h</div>
 <div class="p-title">Daily network #12 · Nov 18</div>
 <div class="slot" style="width:760px;height:640px">${game(DESK)}</div>
 <div class="p-act"><span>418 comments</span><span>Share</span></div></div>
 <div class="side"><b>r/SignalValley</b>One valley network to fix every day. Same puzzle for everyone, new one at midnight UTC.</div></div></div>`}
function hostMob(){return `<div class="host"><div class="m-st"><span>9:41</span><span>●●●</span></div>
 <div class="m-bar"><u></u>r/SignalValley</div>
 <div class="m-post"><div class="p-head"><i></i><b>u/signal-ops</b>· 2h</div><div class="p-title">Daily network #12 · Nov 18</div></div>
 <div class="slot" style="width:390px;height:${MOB.h-(844-44-46-62-46)+0}px;height:646px">${game(MOB)}</div>
 <div class="m-act"><span>418 comments</span><span>Share</span></div></div>`}
function fit(){const el=document.getElementById("fit"),s=Math.min(1,innerWidth/1930);
  el.style.transform=`scale(${s})`;document.body.style.height=el.offsetHeight*s+"px";}
document.getElementById("desk").innerHTML=hostDesk();
document.getElementById("mob").innerHTML=hostMob();
document.getElementById("states").innerHTML=STATES.map(([x,a,b])=>`<div class="sitem">${stateCell(x)}${a}<small>${b}</small></div>`).join("");
document.getElementById("extras").innerHTML=extras();
addEventListener("resize",fit);fit();
"""


def page(d):
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Signal · {d.get('ver','V2')} · {d['name']}</title>
<style>
{font('Lex','lexend-latin-400-normal.woff2',400)}
{font('Lex','lexend-latin-500-normal.woff2',500)}
{font('Lex','lexend-latin-700-normal.woff2',700)}
{d['fonts']}
:root{{--accent:{d['accent']}}}
{SHELL_CSS}
/* ===== direction {d['name']} ===== */
{d['css']}
</style></head><body>
{d.get('svgdefs','')}
<div id="fit"><div class="board">
 <section class="intro">
  <div><div class="tag">Signal · page Jeu · planche {d.get('ver','V2')} · {d['num']}/{d.get('of',3)}</div><h1>{d['title']}</h1></div>
  <p>{d['pitch']}</p>
  <p class="refs">{d['refs']}</p>
 </section>
 <div class="frames">
  <div><div class="flabel">Desktop · 1440 × 900 · post ouvert</div><div class="frame desk" id="desk"></div></div>
  <div><div class="flabel">Mobile · 390 × 844</div><div class="frame mob" id="mob"></div></div>
 </div>
 <section class="states">
  <div><h2>États d'une antenne</h2><div class="srow" id="states"></div></div>
  <div><h2>États d'interface</h2><div class="srow" id="extras"></div></div>
 </section>
</div></div>
<script>
{DATA_JS}
{d['js']}
{SHELL_JS}
</script></body></html>"""


# =============================================================== 01 — CARNET
CARNET = dict(
    num=1, name="Carnet", title="01 — Carnet de veille",
    accent="#ff5b2e",
    refs="Refs : <b>Don't Look Up</b> (papier, trait d'encre, petites figures qui parlent en bulles, boutons pilule à ombre pleine) · "
         "<b>Gemeos</b> (autocollants à contour, note posée à côté de l'action) · <b>Gapsy</b> (l'éclat « WOW » griffonné).",
    pitch="La vallée dessinée à l'encre sur du papier. Il y a deux sortes d'antennes, les mâts et les paraboles, "
          "et chacune dit son chiffre dans une bulle. Quand le compte est bon, la bulle se remplit d'encre ; quand il y en a trop, elle crie "
          "dans un éclat. Une seule couleur, l'orange signal, pour ce qui émet. C'est la direction qui s'écarte du bleu nuit.",
    fonts=font('Fred', 'fredoka-latin-600-normal.woff2', 600) + font('Fred', 'fredoka-latin-700-normal.woff2', 700),
    svgdefs="""<svg width="0" height="0" style="position:absolute"><defs>
 <filter id="ink"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="2.2"/></filter>
 <filter id="inkT"><feTurbulence type="fractalNoise" baseFrequency="0.025" numOctaves="2" seed="2"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>
</defs></svg>""",
    css=r"""
.c-game{background:#f4f1e9;color:#151515;font-family:'Fred',system-ui;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/></filter><rect width='160' height='160' filter='url(%23n)' opacity='.07'/></svg>")}
.c-title{position:absolute;font:700 64px/0.9 'Fred';letter-spacing:-.01em;filter:url(#inkT);transform:rotate(-2.5deg);transform-origin:left}
.c-sub{position:absolute;font:600 13px 'Fred';letter-spacing:.06em;text-transform:uppercase;opacity:.6}
.stk{position:absolute;background:#fff;border:2.5px solid #151515;border-radius:14px;box-shadow:3px 3px 0 #151515;padding:6px 12px 5px;font:600 15px 'Fred';display:flex;gap:8px;align-items:baseline;white-space:nowrap}
.stk em{font-style:normal;font-size:11px;opacity:.55;text-transform:uppercase;letter-spacing:.06em}
.stk.or{background:var(--accent);color:#fff}
.stk.or em{opacity:.85}
.c-board{position:absolute}
.c-board svg{overflow:visible}
.ink{fill:none;stroke:#151515;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.c-side{position:absolute;display:flex;flex-direction:column;gap:14px}
.c-h{font:700 26px/1.05 'Fred'}
.c-p{font:500 15px/1.45 'Lex';color:#333}
.c-p b{font-weight:500;background:linear-gradient(transparent 60%,rgba(255,91,46,.35) 0)}
.kinds{display:flex;gap:10px}
.kind{display:flex;align-items:center;gap:6px;background:#fff;border:2px solid #151515;border-radius:12px;padding:4px 10px 4px 4px;font:600 13px 'Fred'}
.c-prog{font:600 14px 'Fred';display:flex;gap:14px}
.c-prog span{opacity:.55;font-weight:500}
.c-btn{height:56px;border-radius:28px;background:#151515;color:#fff;font:700 19px 'Fred';letter-spacing:.02em;border:0;box-shadow:4px 4px 0 var(--accent);cursor:pointer}
.c-foot{font:500 12px 'Lex';opacity:.55}
@keyframes wv{0%{opacity:0;transform:scale(.6)}30%{opacity:1}100%{opacity:0;transform:scale(1.5)}}
.waves path{animation:wv 1.8s ease-out infinite;transform-box:fill-box;transform-origin:center}
.waves path:nth-child(2n){animation-delay:.25s}
.sc{background:#f4f1e9;border:2px solid #151515;border-radius:14px;box-shadow:3px 3px 0 #151515}
""",
    js=r"""
const INK="#151515",ACC="#ff5b2e",PAPER="#f4f1e9";
function tower(x){ // origine = pied de l'antenne
  let g=`<ellipse cx="0" cy="2" rx="15" ry="4" fill="rgba(0,0,0,.13)"/>`;
  const st=x.on?`fill="${INK}"`:`fill="${PAPER}"`;
  if(x.kind==="mast"){
    g+=`<path d="M-12,0 L0,-46 L12,0 Z" ${st} stroke="${INK}" stroke-width="2.2" stroke-linejoin="round"/>
     <path class="ink" style="stroke:${x.on?PAPER:INK};stroke-width:1.6" d="M-8,-12 L8,-12 M-5,-24 L5,-24 M-8,-12 L5,-24 M8,-12 L-5,-24 M-5,-24 L2,-35 M5,-24 L-2,-35"/>
     <circle cx="0" cy="-49" r="${x.on?4.5:3}" fill="${x.on?ACC:PAPER}" stroke="${INK}" stroke-width="2"/>`;
  }else{
    g+=`<path class="ink" d="M-9,0 L0,-16 L9,0 M0,-16 L0,-24"/>
     <path d="M-17,-38 Q-6,-14 15,-26 Z" ${st} stroke="${INK}" stroke-width="2.2" stroke-linejoin="round"/>
     <path class="ink" d="M-1,-29 L7,-42"/><circle cx="7" cy="-44" r="${x.on?4.5:3}" fill="${x.on?ACC:PAPER}" stroke="${INK}" stroke-width="2"/>`;
  }
  const tx=x.kind==="mast"?0:7, ty=x.kind==="mast"?-49:-44;
  if(x.on){
    const w=`<path d="M${tx+8},${ty-6} q5,6 0,12 M${tx-8},${ty-6} q-5,6 0,12"/><path d="M${tx+13},${ty-10} q8,10 0,20 M${tx-13},${ty-10} q-8,10 0,20"/>`;
    g+=`<g class="${x.fresh?"waves":""}" fill="none" stroke="${ACC}" stroke-width="2.4" stroke-linecap="round">${w}${x.fresh?`<path d="M${tx+19},${ty-14} q11,14 0,28 M${tx-19},${ty-14} q-11,14 0,28"/>`:""}</g>`;
  }
  // bulle
  const by=-74; let b;
  if(x.status==="over"){
    let p="";for(let i=0;i<20;i++){const a=i/20*Math.PI*2,R=i%2?13:19;p+=`${(Math.cos(a)*R*1.15).toFixed(1)},${(by+Math.sin(a)*R).toFixed(1)} `;}
    b=`<polygon points="${p}" fill="#fff" stroke="${INK}" stroke-width="2.2" stroke-linejoin="round"/>
       <text x="0" y="${by+5.5}" text-anchor="middle" font-family="Fred" font-weight="700" font-size="16" fill="${INK}">${x.target}</text>`;
  }else{
    const met=x.status==="met";
    b=`<path d="M-14,${by-11} h28 a8,8 0 0 1 8,8 v6 a8,8 0 0 1 -8,8 h-10 l-5,6 l-1,-6 h-12 a8,8 0 0 1 -8,-8 v-6 a8,8 0 0 1 8,-8 z"
        fill="${met?INK:"#fff"}" stroke="${INK}" stroke-width="2.2" stroke-linejoin="round"/>
       <text x="0" y="${by+5.5}" text-anchor="middle" font-family="Fred" font-weight="700" font-size="16" fill="${met?"#fff":INK}">${x.target}</text>`;
  }
  return g+b;
}
function board(pw,ph){
  const W=pw*5,H=ph*5;
  const pos=x=>[x.c*pw+pw/2,x.r*ph+ph-8];
  let links=LINKS.map(([a,b])=>{const[p,q]=[pos(a),pos(b)];const ya=a.kind==="mast"?-49:-44;
    return `<path d="M${p[0]},${p[1]+ya} Q${(p[0]+q[0])/2},${(p[1]+q[1])/2+ya-14} ${q[0]},${q[1]+ya}" fill="none" stroke="${ACC}" stroke-width="2" stroke-dasharray="1 6" stroke-linecap="round"/>`}).join("");
  let ground="";for(let r=0;r<5;r++){const y=r*ph+ph-6;ground+=`<path class="ink" style="stroke-width:1.3;opacity:.25" d="M6,${y+6} q${W/4},-4 ${W/2},0 t${W/2-12},0"/>`;}
  const t=CELLS.map(x=>{const[p,q]=pos(x);return `<g class="tap" transform="translate(${p},${q})">${tower(x)}<rect x="${-pw/2}" y="-92" width="${pw}" height="${ph}" fill="transparent"/></g>`}).join("");
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><g filter="url(#ink)">${ground}${links}${t}</g></svg>`;
}
function game(L){
  if(!L.mob) return `<div class="game c-game">
    <div class="c-title" style="left:34px;top:30px">SIGNAL</div>
    <div class="c-sub" style="left:38px;top:96px">Network #12 · Tue Nov 18</div>
    <div class="stk" style="right:150px;top:34px;transform:rotate(-3deg)"><em>time</em>02:47</div>
    <div class="stk or" style="right:28px;top:30px;transform:rotate(4deg)"><em>streak</em>6 days</div>
    <div class="c-board" style="left:20px;top:136px">${board(88,96)}</div>
    <div class="c-side" style="left:500px;top:170px;width:230px">
      <div class="c-h">Turn the towers on.</div>
      <div class="c-p">Each bubble says how many towers <b>of its own kind</b> must be on around it, diagonals included.</div>
      <div class="kinds"><span class="kind">${mini("mast")}masts</span><span class="kind">${mini("dish")}dishes</span></div>
      <div class="c-prog">${TOWERS} on <span>·</span> ${MET}/25 settled</div>
      <button class="c-btn">Transmit</button>
      <div class="c-foot">1,284 people fixed today's valley</div>
    </div></div>`;
  return `<div class="game c-game">
    <div class="c-title" style="left:20px;top:22px;font-size:46px">SIGNAL</div>
    <div class="c-sub" style="left:22px;top:70px;font-size:11px">Network #12 · Nov 18</div>
    <div class="stk" style="right:104px;top:22px;transform:rotate(-3deg);font-size:13px;padding:4px 9px"><em>time</em>02:47</div>
    <div class="stk or" style="right:16px;top:20px;transform:rotate(4deg);font-size:13px;padding:4px 9px">6 days</div>
    <div class="c-board" style="left:15px;top:96px">${board(72,82)}</div>
    <div class="c-side" style="left:16px;right:16px;top:${96+82*5+6}px;gap:10px">
      <div class="c-p" style="font-size:13.5px">Turn towers on. Each bubble = towers <b>of its own kind</b> on around it.</div>
      <div class="c-prog" style="font-size:13px">${TOWERS} on <span>·</span> ${MET}/25 settled</div>
      <button class="c-btn" style="height:52px">Transmit</button>
    </div></div>`;
}
function mini(k){return `<svg width="26" height="26" viewBox="-14 -22 28 26"><g transform="scale(.42) translate(0,0)">${k==="mast"
  ?`<path d="M-12,0 L0,-46 L12,0 Z" fill="${PAPER}" stroke="${INK}" stroke-width="4"/>`
  :`<path d="M-9,0 L0,-16 L9,0 M0,-16 L0,-24" fill="none" stroke="${INK}" stroke-width="4"/><path d="M-17,-38 Q-6,-14 15,-26 Z" fill="${PAPER}" stroke="${INK}" stroke-width="4"/>`}</g></svg>`}
function stateCell(x){return `<div class="sc"><svg width="96" height="112" viewBox="-48 -100 96 112"><g filter="url(#ink)">${tower(x)}</g></svg></div>`}
function extras(){return `
 <div class="sitem"><button class="c-btn" style="width:190px">Transmit</button>Repos<small>ombre orange décalée</small></div>
 <div class="sitem"><button class="c-btn" style="width:190px;transform:translate(3px,3px);box-shadow:1px 1px 0 var(--accent)">Transmit</button>Pressé<small>l'ombre s'écrase</small></div>
 <div class="sitem"><div class="stk" style="position:static;transform:rotate(-1.5deg);font-size:14px;padding:9px 14px"><span style="font-family:Fred;font-weight:700">Static!</span>&nbsp;${25-MET} bubbles still disagree.</div>Échec<small>autocollant sous la grille</small></div>
 <div class="sitem"><div class="sc" style="width:200px;height:56px;display:grid;place-items:center;font:600 15px Fred">tuning in<span style="color:var(--accent)">&nbsp;)) )) ))</span></div>Chargement<small>les ondes s'écrivent</small></div>`}
""")

# =============================================================== 02 — ÎLOT
ILOT = dict(
    num=2, name="Ilot", title="02 — L'îlot de nuit",
    accent="#ffc46b",
    refs="Refs : <b>Dairy Food Bulgaria</b> (le monde du produit posé en maquette sur une île flottante, nuages dessous, vue de 3/4) · "
         "<b>Matchball</b> (titre noir ultra-condensé, objets avec ombre douce, bouton rectangle franc).",
    pitch="La vallée devient une petite île qui flotte dans la nuit, vue de trois quarts. L'herbe porte les mâts, la roche porte les "
          "paraboles. Allumer une antenne pose une flaque de lumière ambrée sur sa dalle, et un câble se tend entre les voisines qui se parlent. "
          "C'est la plus « objet de jeu » et celle qui garde le bleu nuit de l'idéation.",
    fonts=font('Cond', 'barlow-condensed-latin-800-normal.woff2', 800),
    css=r"""
.i-game{background:linear-gradient(#0a1430 0%,#16264d 62%,#2a3a66 100%);color:#eef2fa}
.i-title{position:absolute;font:800 112px/.8 'Cond';letter-spacing:-.01em;text-transform:uppercase;color:#f3f5fb}
.i-sub{position:absolute;font:400 14px/1.4 'Lex';color:#a9b6d3}
.i-meta{position:absolute;display:flex;gap:22px}
.i-meta div{display:flex;flex-direction:column}
.i-meta b{font:800 40px/.9 'Cond';color:#fff}
.i-meta span{font:500 10px 'Lex';letter-spacing:.14em;text-transform:uppercase;color:#8a99bd;margin-top:4px}
.i-side{position:absolute;display:flex;flex-direction:column;gap:14px}
.i-p{font:400 14.5px/1.5 'Lex';color:#c7d1e6}
.i-p b{color:#fff;font-weight:500}
.i-legend{display:flex;flex-direction:column;gap:6px;font:400 12.5px 'Lex';color:#a9b6d3}
.i-legend span{display:flex;gap:8px;align-items:center}
.i-legend i{width:18px;height:10px;transform:skewX(-30deg)}
.i-prog{font:500 12px 'Lex';letter-spacing:.06em;text-transform:uppercase;color:#8a99bd}
.i-prog b{color:#fff;font-weight:500}
.i-btn{height:54px;background:#f3f5fb;color:#0a1430;border:0;font:800 24px 'Cond';letter-spacing:.06em;text-transform:uppercase;cursor:pointer;box-shadow:0 12px 30px -12px rgba(0,0,0,.6)}
@keyframes pool{0%{opacity:.9;transform:scale(.4)}100%{opacity:0;transform:scale(1.6)}}
.ring{animation:pool 1.8s ease-out infinite;transform-box:fill-box;transform-origin:center}
.ring.b{animation-delay:.45s}
@keyframes tw{50%{opacity:.25}}
.star{animation:tw 3s ease-in-out infinite}
.sc{background:linear-gradient(#0a1430,#1c2c56);border-radius:12px}
""",
    js=r"""
const AMB="#ffc46b";
const TOP={mast:"#4d7356",dish:"#7d8799"}, TOPL={mast:"#5d8766",dish:"#8f99ab"};
function geo(tw,th,ox,oy){return (r,c)=>[ox+(c-r)*tw/2, oy+(c+r)*th/2]}
function tile(x,X,Y,tw,th,s=.93){
  const a=tw/2*s,b=th/2*s;
  let g=`<polygon points="${X},${Y-b} ${X+a},${Y} ${X},${Y+b} ${X-a},${Y}" fill="${x.on?TOPL[x.kind]:TOP[x.kind]}" stroke="rgba(0,0,0,.25)" stroke-width="1"/>`;
  if(x.on) g+=`<ellipse cx="${X}" cy="${Y}" rx="${a*.8}" ry="${b*.8}" fill="${AMB}" opacity=".32"/>`;
  if(x.fresh) g+=`<ellipse class="ring" cx="${X}" cy="${Y}" rx="${a*.7}" ry="${b*.7}" fill="none" stroke="${AMB}" stroke-width="2"/><ellipse class="ring b" cx="${X}" cy="${Y}" rx="${a*.7}" ry="${b*.7}" fill="none" stroke="${AMB}" stroke-width="2"/>`;
  return g;
}
function mastTop(x,X,Y,h){return x.kind==="mast"?[X,Y-h]:[X+5,Y-h*.78]}
function antenna(x,X,Y,h){
  const L="#e6ebf5";let g=`<ellipse cx="${X+6}" cy="${Y+2}" rx="9" ry="3" fill="rgba(0,0,0,.3)"/>`;
  if(x.kind==="mast"){
    g+=`<path d="M${X-5},${Y} L${X},${Y-h} L${X+5},${Y}" fill="none" stroke="${L}" stroke-width="2"/>
        <path d="M${X-3.5},${Y-h*.3} L${X+3.5},${Y-h*.3} M${X-2},${Y-h*.6} L${X+2},${Y-h*.6}" stroke="${L}" stroke-width="1.4"/>`;
  }else{
    g+=`<path d="M${X},${Y} L${X},${Y-h*.5}" stroke="${L}" stroke-width="2"/>
        <path d="M${X-9},${Y-h*.85} Q${X-4},${Y-h*.35} ${X+9},${Y-h*.62} Z" fill="${L}"/>
        <path d="M${X},${Y-h*.62} L${X+5},${Y-h*.78}" stroke="${L}" stroke-width="1.6"/>`;
  }
  const [tx,ty]=mastTop(x,X,Y,h);
  if(x.on) g+=`<circle cx="${tx}" cy="${ty}" r="13" fill="${AMB}" opacity=".22"/><circle cx="${tx}" cy="${ty}" r="4.5" fill="${AMB}"/>`;
  else g+=`<circle cx="${tx}" cy="${ty}" r="2.6" fill="#3a4a72" stroke="${L}" stroke-width="1.2"/>`;
  return g;
}
function plaque(x,X,Y,sz){
  const met=x.status==="met",over=x.status==="over";
  return `<circle cx="${X}" cy="${Y}" r="${sz}" fill="${met?"#f3f5fb":"rgba(8,16,40,.85)"}" stroke="${over?AMB:(met?"none":"rgba(230,235,245,.5)")}" stroke-width="${over?2:1.2}" ${over?'stroke-dasharray="3 2.5"':""}/>
   <text x="${X}" y="${Y+sz*.42}" text-anchor="middle" font-family="Lex" font-weight="700" font-size="${sz*1.2}" fill="${met?"#0a1430":"#f3f5fb"}">${x.target}</text>`;
}
let L_MOB=false;
function island(W,H,tw,th,ox,oy,mh){L_MOB=W<500;
  const P=geo(tw,th,ox,oy),d=th*.75;
  const c=(r,cc)=>P(r,cc), Nn=c(-.5,-.5),E=c(-.5,4.5),S=c(4.5,4.5),Wp=c(4.5,-.5);
  let g="";
  // étoiles + lune
  const st=[[.08,.1],[.2,.22],[.36,.06],[.62,.14],[.77,.07],[.9,.2],[.52,.27],[.13,.42],[.94,.44]];
  g+=st.map(([a,b],i)=>`<circle class="star" style="animation-delay:${i*.4}s" cx="${W*a}" cy="${H*b}" r="${i%3?1:1.6}" fill="#dfe6f6"/>`).join("");
  // nuages sous l'île
  g+=`<defs><filter id="cl"><feGaussianBlur stdDeviation="10"/></filter></defs><g opacity=".22" fill="#dfe6f6" filter="url(#cl)"><ellipse cx="${S[0]-tw*1.8}" cy="${S[1]+d*3.4}" rx="${tw*1.6}" ry="${th*.55}"/><ellipse cx="${S[0]+tw*1.4}" cy="${S[1]+d*3}" rx="${tw*1.9}" ry="${th*.6}"/><ellipse cx="${S[0]}" cy="${S[1]+d*4.2}" rx="${tw*2.6}" ry="${th*.7}"/></g>`;
  // socle : flancs + dessous rocheux
  const dn=(p,k)=>`${p[0]},${p[1]+k}`;
  g+=`<polygon points="${dn(Wp,0)} ${dn(S,0)} ${dn(S,d)} ${dn(Wp,d)}" fill="#4a3a33"/>
      <polygon points="${dn(S,0)} ${dn(E,0)} ${dn(E,d)} ${dn(S,d)}" fill="#3a2d29"/>
      <polygon points="${dn(Wp,d)} ${dn(S,d)} ${S[0]+tw*.4},${S[1]+d*2.6} ${S[0]-tw*.5},${S[1]+d*3.3} ${Wp[0]+tw*.9},${Wp[1]+d*1.9}" fill="#2c2330"/>
      <polygon points="${dn(S,d)} ${dn(E,d)} ${E[0]-tw*.8},${E[1]+d*2.1} ${S[0]+tw*.4},${S[1]+d*2.6}" fill="#231c2a"/>
      <path d="M${Wp[0]+tw*.4},${Wp[1]+d*1.2} q4,${d} -2,${d*1.6} M${S[0]+tw*.9},${S[1]+d*1.4} q-3,${d*.9} 2,${d*1.5}" stroke="#4a3a33" stroke-width="2" fill="none"/>
      <polygon points="${Nn[0]},${Nn[1]} ${E[0]},${E[1]} ${S[0]},${S[1]} ${Wp[0]},${Wp[1]}" fill="#1d2b2a"/>`;
  const order=[...CELLS].sort((a,b)=>(a.r+a.c)-(b.r+b.c)||a.c-b.c);
  g+=order.map(x=>{const[X,Y]=P(x.r,x.c);return tile(x,X,Y,tw,th)}).join("");
  // câbles entre lampes
  g+=LINKS.map(([a,b])=>{const[A1,A2]=P(a.r,a.c),[B1,B2]=P(b.r,b.c);const[p,q]=mastTop(a,A1,A2-th*.2,mh),[u,v]=mastTop(b,B1,B2-th*.2,mh);
    return `<path d="M${p},${q} Q${(p+u)/2},${(q+v)/2+12} ${u},${v}" fill="none" stroke="${AMB}" stroke-width="1.6" opacity=".75"/>`}).join("");
  g+=order.map(x=>{const[X,Y]=P(x.r,x.c);return `<g class="tap">${antenna(x,X,Y-th*.2,mh)}</g>`}).join("");
  g+=order.map(x=>{const[X,Y]=P(x.r,x.c);return plaque(x,X,Y+th*.14,Math.max(10,tw*.11))}).join("");
  // lune
  g+=`<circle cx="${W-(L_MOB?40:52)}" cy="${L_MOB?150:150}" r="${L_MOB?16:24}" fill="#f1ead8"/><circle cx="${W-(L_MOB?40:52)}" cy="150" r="${L_MOB?34:52}" fill="#f1ead8" opacity=".06"/>`;
  return `<svg width="${W}" height="${H}" style="position:absolute;inset:0">${g}</svg>`;
}
function game(L){
  if(!L.mob) return `<div class="game i-game">${island(760,640,104,52,290,228,40)}
    <div class="i-title" style="left:30px;top:30px">Signal</div>
    <div class="i-sub" style="left:32px;top:126px">Network 12 · fix tonight's valley</div>
    <div class="i-meta" style="right:110px;top:36px"><div><b>02:47</b><span>time</span></div><div><b>6</b><span>nights in a row</span></div></div>
    <div class="i-side" style="left:566px;top:330px;width:170px">
      <p class="i-p">Light the antennas. Each number = antennas <b>of its kind</b> lit on the 8 tiles around it.</p>
      <div class="i-legend"><span><i style="background:${TOP.mast}"></i>grass · masts</span><span><i style="background:${TOP.dish}"></i>rock · dishes</span></div>
      <div class="i-prog"><b>${TOWERS}</b> lit · <b>${MET}</b>/25 right</div>
      <button class="i-btn">Transmit</button>
    </div></div>`;
  return `<div class="game i-game">${island(390,646,74,37,195,196,30)}
    <div class="i-title" style="left:18px;top:20px;font-size:76px">Signal</div>
    <div class="i-meta" style="right:18px;top:24px;gap:14px"><div><b style="font-size:30px">02:47</b><span>time</span></div><div><b style="font-size:30px">6</b><span>nights</span></div></div>
    <div class="i-sub" style="left:20px;top:88px;font-size:12.5px">Network 12 · fix tonight's valley</div>
    <div class="i-side" style="left:18px;right:18px;bottom:18px;gap:10px">
      <p class="i-p" style="font-size:13px">Light the antennas. Each number = antennas <b>of its kind</b> lit around it.</p>
      <div class="i-prog"><b>${TOWERS}</b> lit · <b>${MET}</b>/25 right</div>
      <button class="i-btn" style="height:50px">Transmit</button>
    </div></div>`;
}
function stateCell(x){const tw=88,th=44,X=48,Y=78;
  return `<div class="sc"><svg width="96" height="112">
   <polygon points="${X-tw/2},${Y} ${X},${Y+th/2} ${X},${Y+th/2+12} ${X-tw/2},${Y+12}" fill="#4a3a33"/>
   <polygon points="${X},${Y+th/2} ${X+tw/2},${Y} ${X+tw/2},${Y+12} ${X},${Y+th/2+12}" fill="#3a2d29"/>
   ${tile(x,X,Y,tw,th,1)}${antenna(x,X,Y-2,40)}${plaque(x,X-18,Y+6,11)}</svg></div>`}
function extras(){return `
 <div class="sitem"><button class="i-btn" style="width:190px">Transmit</button>Repos<small>rectangle franc</small></div>
 <div class="sitem"><button class="i-btn" style="width:190px;background:#c9d2e6;box-shadow:none;transform:translateY(2px)">Transmit</button>Pressé<small>ombre retirée</small></div>
 <div class="sitem"><div style="background:#0a1430;color:#eef2fa;padding:12px 16px;width:300px;font:400 13px Lex;border-left:3px solid var(--accent)"><b style="font:800 20px Cond;text-transform:uppercase;letter-spacing:.04em">Static</b> · ${25-MET} numbers still wrong. The cables show who talks to whom.</div>Échec<small>bandeau sous l'île</small></div>
 <div class="sitem"><div style="background:linear-gradient(#0a1430,#1c2c56);color:#a9b6d3;width:200px;height:56px;display:grid;place-items:center;font:800 20px Cond;letter-spacing:.1em;text-transform:uppercase">Rising from the clouds…</div>Chargement<small>l'île monte des nuages</small></div>`}
""")

# =============================================================== 03 — FENÊTRE
FENETRE = dict(
    num=3, name="Fenetre", title="03 — La fenêtre sur la vallée",
    accent="#ffc46b",
    refs="Refs : <b>Raben Rifaie</b> (une seule teinte qui tient tout l'écran, une fenêtre lumineuse découpée dans un mur, sérif italique contre grotesque) · "
         "<b>MemoryQuest</b> (le jeu vit dans un objet : l'écran est encadré, l'action est un gros bouton physique).",
    pitch="On regarde la vallée depuis une fenêtre à petits carreaux : chaque carreau encadre une antenne, et la grille du jeu, ce sont les croisillons. "
          "Tout est dans un seul bleu, en valeurs ; la seule chaleur vient des carreaux où une antenne s'allume. "
          "C'est la plus calme et la plus narrative des trois, au plus près de « vallée la nuit, logique silencieuse ».",
    fonts=font('Serif', 'instrument-serif-latin-400-italic.woff2', 400, 'italic'),
    css=r"""
.f-game{background:#1a2442;color:#e9e3d6}
.f-light{position:absolute;pointer-events:none}
.f-title{position:absolute;font:italic 400 72px/.9 'Serif';letter-spacing:-.01em;color:#efe7d6}
.f-sub{position:absolute;font:400 13px 'Lex';color:#8f9bbd;letter-spacing:.02em}
.f-meta{position:absolute;display:flex;gap:26px;font:400 11px 'Lex';letter-spacing:.12em;text-transform:uppercase;color:#8f9bbd}
.f-meta b{display:block;font:italic 400 34px/1 'Serif';letter-spacing:0;text-transform:none;color:#efe7d6;margin-top:4px}
.f-side{position:absolute;display:flex;flex-direction:column;gap:16px}
.f-p{font:400 14.5px/1.55 'Lex';color:#b9c2db}
.f-p em{font:italic 400 19px 'Serif';color:#efe7d6}
.f-legend{display:flex;gap:16px;font:400 12px 'Lex';color:#8f9bbd}
.f-legend span{display:flex;align-items:center;gap:6px}
.f-prog{font:400 12px 'Lex';color:#8f9bbd}
.f-prog b{font:italic 400 18px 'Serif';color:#efe7d6}
.f-btn{height:52px;border-radius:26px;background:#efe7d6;color:#1a2442;border:0;font:500 15px 'Lex';display:flex;align-items:center;justify-content:center;gap:12px;cursor:pointer;box-shadow:0 14px 34px -14px rgba(255,196,107,.5)}
.f-btn i{font-style:normal;font-size:18px}
@keyframes rise{0%{opacity:.8;transform:scale(.5)}100%{opacity:0;transform:scale(2.2)}}
.ring{animation:rise 2s ease-out infinite;transform-box:fill-box;transform-origin:center}
.ring.b{animation-delay:.5s}
.sc{background:#1a2442;border-radius:12px;padding:8px}
""",
    js=r"""
const AMB="#ffc46b",SIL="#0b1226",CREAM="#efe7d6";
function sil(x,X,Y,s){ // silhouette d'antenne, pied en X,Y
  let g;
  if(x.kind==="mast") g=`<path d="M${X-7*s},${Y} L${X},${Y-30*s} L${X+7*s},${Y} Z" fill="${SIL}"/><rect x="${X-.8*s}" y="${Y-38*s}" width="${1.6*s}" height="${9*s}" fill="${SIL}"/>`;
  else g=`<path d="M${X-6*s},${Y} L${X},${Y-12*s} L${X+6*s},${Y} Z M${X-1*s},${Y-12*s} h${2*s} v${-6*s} h${-2*s} z" fill="${SIL}"/><path d="M${X-12*s},${Y-28*s} Q${X-4*s},${Y-10*s} ${X+11*s},${Y-20*s} Z" fill="${SIL}"/>`;
  const [tx,ty]=x.kind==="mast"?[X,Y-39*s]:[X+5*s,Y-29*s];
  if(x.on) g+=`<circle cx="${tx}" cy="${ty}" r="${3.4*s}" fill="${AMB}"/>`;
  if(x.fresh) g+=`<circle class="ring" cx="${tx}" cy="${ty}" r="${9*s}" fill="none" stroke="${AMB}" stroke-width="1.5"/><circle class="ring b" cx="${tx}" cy="${ty}" r="${9*s}" fill="none" stroke="${AMB}" stroke-width="1.5"/>`;
  return {g,tx,ty};
}
function pane(x,X0,Y0,p,s,id){
  const X=X0+p*.56,Y=Y0+p*.86;
  const {g,tx,ty}=sil(x,X,Y,s);
  let glow=x.on?`<rect x="${X0}" y="${Y0}" width="${p}" height="${p}" fill="url(#warm${id})"/>
     <defs><radialGradient id="warm${id}" cx="${(tx-X0)/p}" cy="${(ty-Y0)/p}" r=".75"><stop offset="0" stop-color="${AMB}" stop-opacity=".75"/><stop offset=".45" stop-color="${AMB}" stop-opacity=".18"/><stop offset="1" stop-color="${AMB}" stop-opacity="0"/></radialGradient></defs>`:"";
  const met=x.status==="met",over=x.status==="over",fs=Math.round(p*.3);
  const num=`<text x="${X0+p*.14}" y="${Y0+p*.34}" font-family="Serif" font-style="italic" font-size="${fs}" fill="${CREAM}" opacity="${met?1:.5}">${x.target}</text>
    ${met?`<path d="M${X0+p*.12},${Y0+p*.42} h${fs*.6}" stroke="${CREAM}" stroke-width="1.4"/>`:""}
    ${over?`<circle cx="${X0+p*.2}" cy="${Y0+p*.25}" r="${fs*.62}" fill="none" stroke="${AMB}" stroke-width="1.4" stroke-dasharray="3 3"/>`:""}`;
  return `<g class="tap">${glow}${g}${num}</g>`;
}
function landscape(x0,y0,S){
  return `<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1533"/><stop offset=".5" stop-color="#2b3f74"/><stop offset="1" stop-color="#5a74b0"/></linearGradient></defs>
   <rect x="${x0}" y="${y0}" width="${S}" height="${S}" fill="url(#sky)"/>
   <circle cx="${x0+S*.35}" cy="${y0+S*.055}" r="${S*.022}" fill="#efe7d6"/><circle cx="${x0+S*.35}" cy="${y0+S*.055}" r="${S*.05}" fill="#efe7d6" opacity=".08"/>
   <path d="M${x0},${y0+S*.5} C${x0+S*.25},${y0+S*.3} ${x0+S*.45},${y0+S*.5} ${x0+S*.7},${y0+S*.4} S${x0+S},${y0+S*.42} ${x0+S},${y0+S*.42} V${y0+S} H${x0}Z" fill="#30477d"/>
   <path d="M${x0},${y0+S*.72} C${x0+S*.3},${y0+S*.52} ${x0+S*.5},${y0+S*.7} ${x0+S*.75},${y0+S*.6} S${x0+S},${y0+S*.63} ${x0+S},${y0+S*.63} V${y0+S} H${x0}Z" fill="#22365f"/>
   <path d="M${x0},${y0+S*.86} C${x0+S*.25},${y0+S*.8} ${x0+S*.55},${y0+S*.9} ${x0+S},${y0+S*.82} V${y0+S} H${x0}Z" fill="#152242"/>`;
}
function windowSVG(W,H,x0,y0,S){
  const p=S/5,m=Math.max(3.5,S*.011),rev=S*.05;
  let g=`<rect x="${x0-rev}" y="${y0-rev}" width="${S+rev*2}" height="${S+rev*2}" fill="#26315a"/>
   <polygon points="${x0-rev},${y0-rev} ${x0},${y0} ${x0},${y0+S} ${x0-rev},${y0+S+rev}" fill="#33406e"/>
   <polygon points="${x0-rev},${y0+S+rev} ${x0},${y0+S} ${x0+S},${y0+S} ${x0+S+rev},${y0+S+rev}" fill="#3c4a7a"/>`;
  g+=landscape(x0,y0,S);
  g+=CELLS.map((x,i)=>pane(x,x0+x.c*p,y0+x.r*p,p,S/440,i)).join("");
  let mull="";for(let i=1;i<5;i++){mull+=`<rect x="${x0+i*p-m/2}" y="${y0}" width="${m}" height="${S}" fill="${SIL}"/><rect x="${x0}" y="${y0+i*p-m/2}" width="${S}" height="${m}" fill="${SIL}"/>`;}
  g+=mull+`<rect x="${x0}" y="${y0}" width="${S}" height="${S}" fill="none" stroke="${SIL}" stroke-width="${m*1.6}"/>`;
  // lumière portée sur le mur et au sol
  g=`<polygon points="${x0+S+rev},${y0-rev} ${W},${y0+S*.15} ${W},${H} ${x0+S*.4},${H}" fill="#efe7d6" opacity=".035"/>`+g;
  return `<svg width="${W}" height="${H}" style="position:absolute;inset:0">${g}</svg>`;
}
function glyph(k){return `<svg width="16" height="18" viewBox="0 0 16 18">${k==="mast"?`<path d="M3,17 L8,2 L13,17Z" fill="#8f9bbd"/>`:`<path d="M5,17 L8,11 L11,17Z" fill="#8f9bbd"/><path d="M1,6 Q5,15 15,9Z" fill="#8f9bbd"/>`}</svg>`}
function game(L){
  if(!L.mob) return `<div class="game f-game">${windowSVG(760,640,52,150,430)}
    <div class="f-title" style="left:44px;top:34px">Signal</div>
    <div class="f-sub" style="left:48px;top:108px">Network 12 · the valley, tonight</div>
    <div class="f-meta" style="right:40px;top:44px"><div>time<b>02:47</b></div><div>streak<b>6 nights</b></div></div>
    <div class="f-side" style="left:536px;top:200px;width:196px">
      <p class="f-p"><em>Wake the valley.</em><br>Each pane's number counts the lit antennas <i>of the same kind</i> in the 8 panes around it.</p>
      <div class="f-legend"><span>${glyph("mast")}masts</span><span>${glyph("dish")}dishes</span></div>
      <div class="f-prog"><b>${TOWERS}</b> lit &nbsp;·&nbsp; <b>${MET}</b> of 25 at peace</div>
      <button class="f-btn">Transmit <i>→</i></button>
    </div></div>`;
  return `<div class="game f-game">${windowSVG(390,646,26,110,338)}
    <div class="f-title" style="left:22px;top:22px;font-size:54px">Signal</div>
    <div class="f-meta" style="right:22px;top:26px;gap:16px"><div>time<b style="font-size:26px">02:47</b></div><div>streak<b style="font-size:26px">6</b></div></div>
    <div class="f-sub" style="left:24px;top:78px;font-size:12px">Network 12 · the valley, tonight</div>
    <div class="f-side" style="left:22px;right:22px;bottom:20px;gap:10px">
      <p class="f-p" style="font-size:13px">Each number counts lit antennas <i>of its kind</i> in the 8 panes around it.</p>
      <div class="f-prog"><b>${TOWERS}</b> lit &nbsp;·&nbsp; <b>${MET}</b> of 25 at peace</div>
      <button class="f-btn" style="height:50px">Transmit <i>→</i></button>
    </div></div>`;
}
let SID=100;
function stateCell(x){SID++;const p=92;return `<div class="sc"><svg width="${p}" height="${p}">${landscape(0,0,p).replace(/id="sky"/,`id="sky${SID}"`).replace(/url\(#sky\)/,`url(#sky${SID})`)}${pane(x,0,0,p,p/88,SID)}
  <rect x="0" y="0" width="${p}" height="${p}" fill="none" stroke="${SIL}" stroke-width="6"/></svg></div>`}
function extras(){return `
 <div class="sitem"><button class="f-btn" style="width:190px">Transmit <i>→</i></button>Repos<small>pilule crème</small></div>
 <div class="sitem"><button class="f-btn" style="width:190px;background:#d8cfbd;box-shadow:none">Transmit <i>→</i></button>Pressé<small>la lueur s'éteint</small></div>
 <div class="sitem"><div style="background:#1a2442;color:#b9c2db;padding:12px 18px;width:300px;font:400 13px/1.5 Lex;border-radius:14px"><em style="font:italic 20px Serif;color:#efe7d6">Only static.</em> ${25-MET} panes still disagree.</div>Échec<small>phrase sous la fenêtre</small></div>
 <div class="sitem"><div style="background:#1a2442;color:#8f9bbd;width:220px;height:56px;border-radius:14px;display:grid;place-items:center;font:italic 20px Serif">the valley is waking…</div>Chargement<small>les carreaux s'allument un à un</small></div>`}
""")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, d in [("01-carnet", CARNET), ("02-ilot", ILOT), ("03-fenetre", FENETRE)]:
        (OUT / f"{slug}.html").write_text(page(d), encoding="utf-8")
        print("écrit", (OUT / f"{slug}.html").relative_to(HERE.parent.parent))


if __name__ == "__main__":
    main()
