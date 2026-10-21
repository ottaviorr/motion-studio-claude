#!/usr/bin/env node
// conferir_hierarquia.mjs — confere a HIERARQUIA VISUAL de uma cena HTML do estúdio (página com window.frame(t), window.DUR e #st).
// Abre a cena no Chrome do computador (sem janela, via CDP, mesmo padrão do kit/gravar.mjs), chama frame(t) e mede pelo DOM + pela imagem:
//   tamanho de fonte EFETIVO de cada texto visível (font-size × escala acumulada dos transforms), contraste texto × fundo
//   (WCAG 2.x e APCA Lc, com o fundo amostrado ATRÁS do texto: foto com texto × foto com o texto apagado), texto fora da zona segura,
//   palavras visíveis por tela, níveis de tamanho (razão título:apoio), cores de destaque no quadro e tempo de exposição de cada texto.
//
// uso: node conferir_hierarquia.mjs cena.html [--t 1.2,3.4] [--n 8] [--perfil auto|9x16|16x9|16x9-feed] [--zona auto|reels|reels-anuncio|tiktok|shorts|todas|titulo|nenhuma]
//                                  [--passo 0.1] [--fotos pasta] [--json saida.json] [--ui "seletor css"] [--sem-exposicao]
//   --t      tempos (s) para a conferência completa (com fotos). Sem --t: --n tempos espalhados (padrão 8) + os tempos em que mais texto aparece.
//   --perfil tabela de números a usar (auto: deitado → 16x9, em pé → 9x16). 16x9-feed = vídeo deitado assistido dentro do feed em pé (texto ×1,8).
//   --zona   zona segura (auto: reels no em pé, titulo no deitado).
//   --fotos  salva uma foto por tempo com as caixas pintadas (verde ok · amarelo aviso · vermelho falha) e a zona segura, e uma folha.
//   --ui     o que é réplica de interface (regras de rótulo de UI, não de título). Padrão: .lu-win,.lu-cel,.bw,.cel,.tela,[data-hv=ui]
//   Na cena: data-hv="ignorar" num elemento tira o texto dele da conferência (marca-d'água decorativa, textura de letras).
// Saída: relatório no terminal (código 1 se houver FALHA) e, com --json, tudo em JSON.
import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

// ---------------------------------------------------------------- TABELA DO ESTÚDIO (fonte: references/tabela-numeros.md)
// px = pixels do palco (1080×1920 ou 1920×1080), já com a escala dos transforms.
const PERFIS = {
  "9x16": {
    nome: "em pé 1080×1920 (celular)",
    rotuloMin: 30,      // nada abaixo disto: 11 pt (mínimo da Apple HIG) num celular de 393 pt de largura (1 pt ≈ 2,75 px do vídeo)
    apoioMin: 40,       // frase de apoio/legenda (≈ 14,5 pt; recomendado 44–60 = 16–22 pt); 30–39 só para etiqueta curta (≤ 3 palavras)
    tituloMin: 84,      // nível 1 (≈ 30 pt; Large Title da Apple = 34 pt = 93 px)
    grandeRegular: 66,  // "texto grande" da WCAG (24 px CSS ≈ 18 pt) convertido para o vídeo em pé: 24 / 0,364
    grandeNegrito: 51,  // 18,66 px CSS (14 pt negrito) / 0,364
    razaoNiveis: 1.5,   // nível 1 ÷ nível 2 mínimo
    palavrasTitulo: 6,  // aviso acima disto no nível 1
    palavrasTela: 15,   // aviso acima disto fora de UI; falha acima de palavrasTelaMax
    palavrasTelaMax: 25,
    zona: "reels",
  },
  "16x9": {
    nome: "deitado 1920×1080 (celular deitado em tela cheia / computador: 1 pt ≈ 2,25 px)",
    rotuloMin: 26, apoioMin: 36, tituloMin: 72, grandeRegular: 54, grandeNegrito: 42,
    razaoNiveis: 1.5, palavrasTitulo: 8, palavrasTela: 20, palavrasTelaMax: 35, zona: "titulo",
  },
  "16x9-feed": {
    nome: "deitado 1920×1080 visto dentro de página/feed com o celular em pé (1 pt ≈ 4,9 px)",
    rotuloMin: 54, apoioMin: 72, tituloMin: 150, grandeRegular: 118, grandeNegrito: 91,
    razaoNiveis: 1.5, palavrasTitulo: 6, palavrasTela: 15, palavrasTelaMax: 25, zona: "titulo",
  },
};
// zonas seguras em px do palco. proibido = retângulos onde texto importante não pode ficar (botões, legenda, perfil).
const ZONAS = {
  // Reels orgânico (kit/zona-segura.png do estúdio): livre y 220–1540; coluna de botões x > 930 a partir de y 700.
  // ideal = regra da Meta para anúncio (14% topo, 35% base, 6% laterais → x 65–1015, y 269–1248): fora dela vira AVISO
  reels: { w: 1080, h: 1920, seguro: [60, 220, 1020, 1540], proibido: [[930, 700, 1080, 1540]], ideal: [65, 220, 1015, 1248], nome: "Reels (zona-segura.png do kit; ideal: base do anúncio Meta)" },
  // anúncio Meta Reels/Stories: 14% / 35% / 6% (facebook.com/business/ads-guide … instagram-reels) — tudo fora é FALHA
  "reels-anuncio": { w: 1080, h: 1920, seguro: [65, 269, 1015, 1248], proibido: [], ideal: null, nome: "anúncio Meta (14% topo, 35% base, 6% lados)" },
  // TikTok orgânico (números de terceiros; o TikTok não publica em texto): topo 108, base 320, esq. 60, dir. 120
  tiktok: { w: 1080, h: 1920, seguro: [60, 108, 960, 1600], proibido: [], ideal: [65, 269, 960, 1248], nome: "TikTok (orgânico)" },
  // YouTube Shorts (lido da imagem do Google): topo 288, base 672, esq. 48, dir. 192
  shorts: { w: 1080, h: 1920, seguro: [48, 288, 888, 1248], proibido: [], ideal: null, nome: "YouTube Shorts" },
  // uma peça para as três plataformas: pior caso de cada lado
  todas: { w: 1080, h: 1920, seguro: [65, 288, 888, 1248], proibido: [], ideal: null, nome: "Reels+TikTok+Shorts (pior caso)" },
  // 16:9: área de grafismo da EBU R95 (5% de cada lado → 96 px / 54 px em 1920×1080)
  titulo: { w: 1920, h: 1080, seguro: [96, 54, 1824, 1026], proibido: [], ideal: null, nome: "grafismo 90% (EBU R95)" },
  nenhuma: null,
};
const APCA_MIN = { grande: 60, apoio: 75, enorme: 45 }; // Lc (APCA 0.0.98G, valor absoluto) — APCA in a Nutshell / Bronze Simple Mode

// ---------------------------------------------------------------- argumentos
const argv = process.argv.slice(2);
const arg = (n, d) => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : d; };
const tem = (n) => argv.includes(n);
const COM_VALOR = new Set(["--t", "--n", "--perfil", "--zona", "--passo", "--fotos", "--json", "--ui"]);
const htmlArg = argv.find((a, i) => !a.startsWith("--") && !(i > 0 && COM_VALOR.has(argv[i - 1])));
if (!htmlArg) { console.log("uso: node conferir_hierarquia.mjs cena.html [--t 1,2.5] [--n 8] [--perfil auto|9x16|16x9|16x9-feed] [--zona auto|reels|reels-anuncio|tiktok|shorts|todas|titulo|nenhuma] [--fotos pasta] [--json saida.json]"); process.exit(2); }
const html = path.resolve(htmlArg);
const UI_SEL = arg("--ui", ".lu-win,.lu-cel,.lu-vw,.bw,.cel,.tela,[data-hv=ui]");
const passo = Number(arg("--passo", 0.1));
const nTempos = Number(arg("--n", 8));
const fotosDir = arg("--fotos", null) ? path.resolve(arg("--fotos")) : null;
const jsonOut = arg("--json", null);

// ---------------------------------------------------------------- Chrome (padrão do kit/gravar.mjs: porta 0 + DevToolsActivePort)
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "hierarquia-"));
const ch = spawn(CHROME, ["--headless=new", "--remote-debugging-port=0", `--user-data-dir=${dir}/perfil`, "--hide-scrollbars", "--force-color-profile=srgb", "--window-size=1920,1920", "about:blank"], { stdio: "ignore" });
let alvo, porta;
for (let i = 0; i < 75 && !alvo; i++) { await new Promise((r) => setTimeout(r, 200)); try { porta ??= fs.readFileSync(`${dir}/perfil/DevToolsActivePort`, "utf8").split("\n")[0]; alvo = (await (await fetch(`http://127.0.0.1:${porta}/json`)).json()).find((t) => t.type === "page")?.webSocketDebuggerUrl; } catch {} }
if (!alvo) { console.error("Chrome não abriu"); ch.kill(); process.exit(2); }
const ws = new WebSocket(alvo); await new Promise((ok) => (ws.onopen = ok));
let id = 0; const esp = new Map(), erros = [];
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.method === "Runtime.exceptionThrown") erros.push(m.params.exceptionDetails.exception?.description?.split("\n")[0]); if (m.id && esp.has(m.id)) { esp.get(m.id)(m); esp.delete(m.id); } };
const cdp = (method, params = {}) => new Promise((ok) => { const i = ++id; esp.set(i, ok); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await cdp("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true }); if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description || "erro no evaluate"); return r.result?.result?.value; };
const fim = async (cod) => { try { ws.close(); } catch {} ch.kill(); await new Promise((r) => setTimeout(r, 600)); try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} process.exit(cod); };

await cdp("Page.enable"); await cdp("Runtime.enable");
await cdp("Page.navigate", { url: "file://" + html });
await new Promise((r) => setTimeout(r, 1500));
await ev("document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,800)))");
const W = await ev("(document.getElementById('st')||document.body).offsetWidth"), H = await ev("(document.getElementById('st')||document.body).offsetHeight");
const DUR = await ev("window.DUR");
if (typeof DUR !== "number" || !(await ev("typeof window.frame==='function'"))) { console.error("a página não tem window.frame(t) / window.DUR"); await fim(2); }
await cdp("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: false });

let perfilNome = arg("--perfil", "auto");
if (perfilNome === "auto") perfilNome = W > H ? "16x9" : "9x16";
const P = PERFIS[perfilNome]; if (!P) { console.error("perfil desconhecido: " + perfilNome); await fim(2); }
let zonaNome = arg("--zona", "auto"); if (zonaNome === "auto") zonaNome = W > H ? "titulo" : (H / W > 1.7 ? "reels" : "nenhuma");
const Z = ZONAS[zonaNome] === undefined ? (console.error("zona desconhecida: " + zonaNome), null) : ZONAS[zonaNome];

// ---------------------------------------------------------------- código que roda DENTRO da página (nomes com __hv para não colidir com a cena)
const NA_PAGINA = String.raw`
(()=>{
const ids=new WeakMap(); let prox=1;
const idDe=el=>{ if(!ids.has(el)) ids.set(el,prox++); return ids.get(el); };
const st=document.getElementById('st')||document.body;
const INLINE=new Set(['inline','inline-block','contents']);
function bloco(el){ // o "parágrafo" do texto: sobe enquanto for palavra/trecho em linha
  if(el instanceof SVGElement){ return el.closest('text')||el; }
  let x=el; while(x.parentElement && x!==st && INLINE.has(getComputedStyle(x).display) && x.parentElement!==st) x=x.parentElement; return x; }
function escala(el){ // escala acumulada dos transforms (raiz da área do determinante 2D), scale e zoom
  if(el instanceof SVGElement && el.getScreenCTM){ const m=el.getScreenCTM(); let s=m?Math.sqrt(Math.abs(m.a*m.d-m.b*m.c)):1;
    // getScreenCTM não inclui transforms CSS dos pais HTML: soma os deles
    let x=el.ownerSVGElement; while(x && x.ownerSVGElement) x=x.ownerSVGElement; return s*escalaHTML(x&&x.parentElement); }
  return escalaHTML(el); }
function escalaHTML(el){ let s=1; for(let x=el;x&&x.nodeType===1;x=x.parentElement){ const cs=getComputedStyle(x);
    if(cs.transform&&cs.transform!=='none'){ const m=new DOMMatrix(cs.transform); s*=Math.sqrt(Math.abs(m.a*m.d-m.b*m.c)); }
    if(cs.scale&&cs.scale!=='none'){ const v=cs.scale.split(' ').map(Number); s*=Math.sqrt(Math.abs(v[0]*(v.length>1?v[1]:v[0]))); }
    if(cs.zoom&&cs.zoom!=='1'&&cs.zoom!=='normal'){ s*=Number(cs.zoom)||1; } }
  return s; }
function visivel(el){ let op=1; for(let x=el;x&&x.nodeType===1;x=x.parentElement){ const cs=getComputedStyle(x); if(cs.display==='none') return 0; op*=Number(cs.opacity); if(op<=0.02) return 0; }
  if(getComputedStyle(el).visibility!=='visible') return 0; return op; }
function corte(el){ // retângulo visível depois dos overflow:hidden/clip dos pais (aproximação: ignora clip-path/máscara — a foto resolve)
  const sr=st.getBoundingClientRect(); let r=[sr.left,sr.top,sr.right,sr.bottom];
  for(let x=el.parentElement;x&&x!==document.body;x=x.parentElement){ const cs=getComputedStyle(x);
    if(/hidden|clip|scroll|auto/.test(cs.overflow+cs.overflowX+cs.overflowY) && !(x instanceof SVGElement)){ const b=x.getBoundingClientRect(); r=[Math.max(r[0],b.left),Math.max(r[1],b.top),Math.min(r[2],b.right),Math.min(r[3],b.bottom)]; } }
  return r; }
function corAlfa(c){ const m=c.match(/rgba?\(([^)]+)\)/); if(!m) return 1; const v=m[1].split(/[ ,\/]+/).filter(Boolean); return v.length>3?Number(v[3]):1; }
window.__hvColetar=function(uiSel,opMin){
  const sr=st.getBoundingClientRect(); const out=new Map();
  const tw=document.createTreeWalker(st,NodeFilter.SHOW_TEXT,{acceptNode:n=>/\S/.test(n.nodeValue)?1:2});
  for(let n;(n=tw.nextNode());){
    const el=n.parentElement; if(!el||el.closest('script,style,[data-hv="ignorar"],#__hv_cam')) continue;
    const op=visivel(el); if(op<opMin) continue;
    const cs=getComputedStyle(el);
    const fill = el instanceof SVGElement ? cs.fill : (cs.webkitTextFillColor||cs.color);
    if(corAlfa(fill)<0.05 && corAlfa(cs.color)<0.05 && !(cs.webkitTextStrokeWidth&&parseFloat(cs.webkitTextStrokeWidth)>0)) continue;
    const rg=document.createRange(); rg.selectNodeContents(n); const c=corte(el);
    const rects=[...rg.getClientRects()].map(q=>[Math.max(q.left,c[0]),Math.max(q.top,c[1]),Math.min(q.right,c[2]),Math.min(q.bottom,c[3])]).filter(q=>q[2]-q[0]>1&&q[3]-q[1]>1).map(q=>[q[0]-sr.left,q[1]-sr.top,q[2]-sr.left,q[3]-sr.top]);
    if(!rects.length) continue;
    const b=bloco(el); const k=idDe(b);
    const fs=parseFloat(cs.fontSize)*escala(el);
    let o=out.get(k); if(!o){ o={id:k,tag:b.tagName.toLowerCase()+(b.id?'#'+b.id:'')+(b.classList&&b.classList.length?'.'+[...b.classList].slice(0,2).join('.'):''),texto:'',rects:[],fs:fs,fsMax:fs,peso:Number(cs.fontWeight)||400,familia:cs.fontFamily.split(',')[0].replace(/["']/g,'').trim(),ui:!!el.closest(uiSel),op:op,ls:cs.letterSpacing,lh:cs.lineHeight,fsCss:parseFloat(cs.fontSize),cor:fill}; out.set(k,o); }
    o.texto+=(o.texto&&!/\s$/.test(o.texto)?' ':'')+n.nodeValue.replace(/\s+/g,' ').trim();
    if(!o.partes) o.partes=[]; o.partes.push([fs,(n.nodeValue.match(/[\p{L}\p{N}][\p{L}\p{N}'’.,%$-]*/gu)||[]).length]);
    o.rects.push(...rects); if(fs<o.fs){o.fs=fs;} if(fs>o.fsMax){o.fsMax=fs;o.peso=Number(cs.fontWeight)||400;o.familia=cs.fontFamily.split(',')[0].replace(/["']/g,'').trim();o.ls=cs.letterSpacing;o.lh=cs.lineHeight;o.fsCss=parseFloat(cs.fontSize);o.cor=fill;}
    o.op=Math.max(o.op,op);
  }
  return [...out.values()].map(o=>{ const xs=o.rects; const bb=[Math.min(...xs.map(r=>r[0])),Math.min(...xs.map(r=>r[1])),Math.max(...xs.map(r=>r[2])),Math.max(...xs.map(r=>r[3]))];
    const tops=[]; xs.forEach(r=>{ if(!tops.some(t=>Math.abs(t-r[1])<o.fs*0.5)) tops.push(r[1]); });
    o.bbox=bb.map(Math.round); o.linhas=tops.length; o.palavras=(o.texto.match(/[\p{L}\p{N}][\p{L}\p{N}'’.,%$-]*/gu)||[]).length; o.texto=o.texto.trim(); return o; });
};
// pixels: A = quadro normal, B = mesmo quadro com o texto apagado (cor transparente) → o que muda é a tinta; o fundo atrás é B.
const lin=c=>{c/=255;return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4);};
const LUT=new Float64Array(256).map((_,i)=>lin(i));
const Lrel=(r,g,b)=>0.2126*LUT[r]+0.7152*LUT[g]+0.0722*LUT[b];
const Yapca=(r,g,b)=>0.2126729*Math.pow(r/255,2.4)+0.7151522*Math.pow(g/255,2.4)+0.0721750*Math.pow(b/255,2.4);
function apca(txtY,bgY){ // APCA 0.0.98G-4g (apca-w3)
  const bt=0.022,bc=1.414; txtY=txtY>bt?txtY:txtY+Math.pow(bt-txtY,bc); bgY=bgY>bt?bgY:bgY+Math.pow(bt-bgY,bc);
  if(Math.abs(bgY-txtY)<0.0005) return 0; let s;
  if(bgY>txtY){ s=(Math.pow(bgY,0.56)-Math.pow(txtY,0.57))*1.14; return s<0.1?0:(s-0.027)*100; }
  s=(Math.pow(bgY,0.65)-Math.pow(txtY,0.62))*1.14; return s>-0.1?0:(s+0.027)*100; }
async function imgData(b64){ const im=new Image(); im.src='data:image/png;base64,'+b64; await im.decode(); const cv=document.createElement('canvas'); cv.width=im.width; cv.height=im.height; const cx=cv.getContext('2d',{willReadFrequently:true}); cx.drawImage(im,0,0); return cx.getImageData(0,0,im.width,im.height); }
window.__hvPixels=async function(blocos,a64,b64){
  const A=await imgData(a64), B=await imgData(b64), w=A.width, h=A.height, a=A.data, b=B.data;
  for(const o of blocos){
    const vis=new Uint8Array(w*h); const pix=[];
    for(const r of o.rects){ const x0=Math.max(0,Math.floor(r[0])),y0=Math.max(0,Math.floor(r[1])),x1=Math.min(w,Math.ceil(r[2])),y1=Math.min(h,Math.ceil(r[3]));
      for(let y=y0;y<y1;y++) for(let x=x0;x<x1;x++){ const i=y*w+x; if(vis[i]) continue; vis[i]=1; const j=i*4; const d=Math.abs(a[j]-b[j])+Math.abs(a[j+1]-b[j+1])+Math.abs(a[j+2]-b[j+2]); pix.push([d,j]); } }
    const tinta=pix.filter(p=>p[0]>30); o.pxTinta=tinta.length; o.pxArea=pix.length;
    // fundo da caixa inteira (B): média e desvio da luminância → "fundo agitado"
    let sL=0,sL2=0; for(const p of pix){ const j=p[1]; const L=Lrel(b[j],b[j+1],b[j+2]); sL+=L; sL2+=L*L; } const n=pix.length||1; o.fundoDesvio=Math.sqrt(Math.max(0,sL2/n-(sL/n)**2));
    if(tinta.length<12){ o.renderizado=false; continue; } o.renderizado=true;
    { let x0=1e9,y0=1e9,x1=-1,y1=-1; for(const [,j] of tinta){ const i=j/4, x=i%w, y=(i-x)/w; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } o.bboxDom=o.bbox; o.bbox=[x0,y0,x1+1,y1+1]; } // caixa pela tinta de verdade (resolve clip-path/máscara/texto cortado)
    tinta.sort((p,q)=>q[0]-p[0]); const nucleo=tinta.slice(0,Math.max(8,Math.round(tinta.length*0.35)));
    let ir=0,ig=0,ib=0,br=0,bg=0,bb=0; const rs=[];
    for(const [,j] of nucleo){ ir+=a[j];ig+=a[j+1];ib+=a[j+2];br+=b[j];bg+=b[j+1];bb+=b[j+2];
      const L1=Lrel(a[j],a[j+1],a[j+2]),L2=Lrel(b[j],b[j+1],b[j+2]); rs.push((Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05)); }
    const k=nucleo.length; const T=[ir/k,ig/k,ib/k].map(Math.round), F=[br/k,bg/k,bb/k].map(Math.round);
    o.tinta=T; o.fundo=F; const L1=Lrel(...T),L2=Lrel(...F); o.wcag=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    rs.sort((x,y)=>x-y); o.wcagP10=rs[Math.floor(rs.length*0.1)];
    o.lc=apca(Yapca(...T),Yapca(...F));
  }
  // cores de destaque no quadro inteiro (A): OKLab, croma > 0,07, agrupadas por matiz (24 faixas de 15°)
  const bins=new Array(0x18).fill(0), soma=Array.from({length:24},()=>[0,0,0]); let N=0; const cont=new Map();
  for(let y=0;y<h;y+=4) for(let x=0;x<w;x+=4){ const j=(y*w+x)*4; N++; const R=LUT[a[j]],G=LUT[a[j+1]],Bl=LUT[a[j+2]];
    const l=Math.cbrt(0.4122214708*R+0.5363325363*G+0.0514459929*Bl), m=Math.cbrt(0.2119034982*R+0.6806995451*G+0.1073969566*Bl), s=Math.cbrt(0.0883024619*R+0.2817188376*G+0.6299787005*Bl);
    const L=0.2104542553*l+0.7936177850*m-0.0040720468*s, A_=1.9779984951*l-2.4285922050*m+0.4505937099*s, B_=0.0259040371*l+0.7827717662*m-0.8086757660*s;
    const C=Math.hypot(A_,B_); if(C<0.07||L<0.2) continue; let hh=Math.atan2(B_,A_)*180/Math.PI; if(hh<0) hh+=360; const k=Math.floor(hh/15)%24; bins[k]++; soma[k][0]+=a[j];soma[k][1]+=a[j+1];soma[k][2]+=a[j+2]; }
  const lim=N*0.002; const grupos=[]; const usado=new Array(0x18).fill(false);
  for(let k=0;k<24;k++){ if(bins[k]<lim||usado[k]) continue; let ini=k; while(bins[(ini+23)%24]>=lim && !usado[(ini+23)%24] && (ini+23)%24!==k) ini=(ini+23)%24;
    let g={px:0,r:0,g:0,b:0}; let x=ini; do{ usado[x]=true; g.px+=bins[x]; g.r+=soma[x][0]; g.g+=soma[x][1]; g.b+=soma[x][2]; x=(x+1)%24; } while(bins[x]>=lim && !usado[x]);
    grupos.push({parte:g.px/N,cor:'#'+[g.r,g.g,g.b].map(v=>Math.round(v/g.px).toString(0x10).padStart(2,'0')).join('')}); }
  grupos.sort((x,y)=>y.parte-x.parte);
  return {blocos, cores:grupos.map(g=>({...g,fundo:g.parte>0.35}))};
};
window.__hvMarcas=function(lista,zona){ // desenha caixas e zona por cima (só para a foto de conferência)
  let d=document.getElementById('__hv_cam'); if(!d){ d=document.createElement('div'); d.id='__hv_cam'; d.style.cssText='position:absolute;left:0;top:0;width:100%;height:100%;z-index:2147483647;pointer-events:none'; st.appendChild(d); }
  const box=(x0,y0,x1,y1,css)=>'<div style="position:absolute;left:'+x0+'px;top:'+y0+'px;width:'+(x1-x0)+'px;height:'+(y1-y0)+'px;'+css+'"></div>';
  let s=''; if(zona){ s+=box(zona.seguro[0],zona.seguro[1],zona.seguro[2],zona.seguro[3],'outline:3px dashed rgba(255,0,90,.85)'); for(const p of zona.proibido) s+=box(p[0],p[1],p[2],p[3],'background:rgba(255,0,90,.22)'); }
  for(const o of lista){ const c=o.nivel==='FALHA'?'#ff2d2d':o.nivel==='AVISO'?'#ffb800':'#19d36b'; const [x0,y0,x1,y1]=o.bbox;
    s+=box(x0-4,y0-4,x1+4,y1+4,'border:4px solid '+c+';border-radius:6px');
    s+='<div style="position:absolute;left:'+Math.max(0,x0-4)+'px;top:'+Math.max(0,y0-34)+'px;background:'+c+';color:#000;font:700 22px/30px Menlo,monospace;padding:0 8px;white-space:nowrap">'+o.rot+'</div>'; }
  d.innerHTML=s; };
window.__hvLimpa=function(){ const d=document.getElementById('__hv_cam'); if(d) d.remove(); };
})();`;
await ev(NA_PAGINA);
// sem transição CSS (a cena é função do tempo; evita que a troca de cor da foto B "anime")
await ev(`(()=>{const s=document.createElement('style');s.id='__hv_fixo';s.textContent='*{transition:none!important}';document.head.appendChild(s)})()`);
const OCULTA = `*{color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important;-webkit-text-stroke-color:transparent!important;text-decoration-color:transparent!important;caret-color:transparent!important} svg text,svg tspan,svg textPath{fill:transparent!important;stroke:transparent!important}`;

const vaiPara = async (t) => ev(`frame(${t}); new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))`);
const foto = async () => (await cdp("Page.captureScreenshot", { format: "png", clip: { x: 0, y: 0, width: W, height: H, scale: 1 } })).result.data;

// ---------------------------------------------------------------- 1) varredura leve (só DOM) para o tempo de exposição
const tempoMinimo = (palavras) => Math.max(1.0, 0.5 + 0.33 * palavras); // s · 0,5 s para achar o texto + 0,33 s por palavra (BBC; ~180 palavras/min, leitura em PT-BR); nunca < 1 s (Netflix: 0,83 s)
const runs = []; const abertos = new Map(); const palavrasNoTempo = [];
const setPal = (s) => new Set((s.toLowerCase().match(/[\p{L}\p{N}]+/gu) || []));
const mesmoTexto = (a, b) => { const na = a.toLowerCase().replace(/\s+/g, " ").trim(), nb = b.toLowerCase().replace(/\s+/g, " ").trim(); if (na.startsWith(nb) || nb.startsWith(na)) return true; /* digitando letra a letra */ const A = setPal(a), B = setPal(b); if (!A.size || !B.size) return false; let ab = [...A].every((x) => B.has(x)), ba = [...B].every((x) => A.has(x)); return ab || ba; };
if (!tem("--sem-exposicao")) {
  const n = Math.floor(DUR / passo);
  for (let i = 0; i <= n; i++) {
    const t = +(i * passo).toFixed(3);
    const bl = await ev(`frame(${t}); __hvColetar(${JSON.stringify(UI_SEL)}, 0.5).map(o=>({id:o.id,texto:o.texto,ui:o.ui,palavras:o.palavras,fs:o.fsMax,bbox:o.bbox}))`);
    const dentro = bl.filter((o) => o.bbox[2] > 0 && o.bbox[0] < W && o.bbox[3] > 0 && o.bbox[1] < H);
    palavrasNoTempo.push([t, dentro.filter((o) => !o.ui).reduce((s, o) => s + o.palavras, 0)]);
    const vistos = new Set();
    for (const o of dentro) {
      if (o.ui) continue;
      const ab = abertos.get(o.id);
      if (ab && mesmoTexto(ab.texto, o.texto)) { ab.fimT = t; if (setPal(o.texto).size > setPal(ab.texto).size) { ab.texto = o.texto; ab.palavras = o.palavras; } ab.cheioT ??= null; vistos.add(o.id); continue; }
      if (ab) { const soNum = (x) => !/\p{L}{2,}/u.test(x.replace(/R\$|pessoas?|dias?|h|min/gi, "")); if (soNum(ab.texto) && soNum(o.texto)) { ab.contador = true; } runs.push(ab); }
      abertos.set(o.id, { id: o.id, texto: o.texto, palavras: o.palavras, iniT: t, fimT: t, fs: o.fs }); vistos.add(o.id);
    }
    for (const [k, ab] of abertos) if (!vistos.has(k)) { runs.push(ab); abertos.delete(k); }
  }
  for (const ab of abertos.values()) { ab.ateFim = true; runs.push(ab); }
}

// ---------------------------------------------------------------- 2) tempos da conferência completa
let tempos;
if (arg("--t")) tempos = arg("--t").split(",").map(Number).filter((x) => !isNaN(x));
else {
  tempos = Array.from({ length: nTempos }, (_, i) => +((DUR * (i + 0.5)) / nTempos).toFixed(2));
  // + os 2 momentos com mais palavras na tela (os mais carregados)
  const top = [...palavrasNoTempo].sort((a, b) => b[1] - a[1]).slice(0, 2).map((x) => x[0]);
  for (const t of top) if (!tempos.some((x) => Math.abs(x - t) < 0.5)) tempos.push(t);
  tempos.sort((a, b) => a - b);
}

// ---------------------------------------------------------------- 3) regras
const r1 = (x) => (Math.round(x * 10) / 10).toString().replace(".", ",");
const r2 = (x) => x.toFixed(2).replace(".", ",");
const hex = (c) => "#" + c.map((v) => v.toString(0x10).padStart(2, "0")).join("").toUpperCase();
const fora = (bb, r) => Math.max(r[0] - bb[0], bb[2] - r[2], r[1] - bb[1], bb[3] - r[3], 0);
const cruza = (bb, r) => bb[0] < r[2] && bb[2] > r[0] && bb[1] < r[3] && bb[3] > r[1];
function julgar(o, papel, P) {
  const p = [];
  const grande = o.fsMax >= P.grandeRegular || (o.fsMax >= P.grandeNegrito && o.peso >= 600);
  // tamanho
  if (o.fs < P.rotuloMin && o.ui) p.push(["AVISO", `UI em ${Math.round(o.fs)} px < ${P.rotuloMin} px: se a fala cita este texto, aproxime ${r2(P.rotuloMin / o.fs)}× ou mais`]);
  else if (o.fs < P.rotuloMin) p.push(["FALHA", `${Math.round(o.fs)} px < ${P.rotuloMin} px (mínimo absoluto)`]);
  const palPeq = (o.partes || []).filter((x) => x[0] < P.apoioMin).reduce((a, x) => a + x[1], 0);
  if (!o.ui && o.fs >= P.rotuloMin && o.fs < P.apoioMin && palPeq > 3) p.push(["FALHA", `frase de ${palPeq} palavras em ${Math.round(o.fs)} px (< ${P.apoioMin} px de apoio; rótulo só até 3 palavras)`]);
  // contraste
  if (o.renderizado) {
    const min = grande ? 3 : 4.5;
    if (o.wcag < min) p.push(["FALHA", `contraste ${r2(o.wcag)}:1 < ${min}:1 (WCAG ${grande ? "texto grande" : "texto normal"})`]);
    // APCA (px CSS ÷ 0,364 no em pé): Lc 45 só para ≥ 36 px/400 ou 24 px/700 CSS; Lc 60 para rótulo/título; Lc 75 para frase de leitura
    const enorme = o.fsMax >= P.grandeRegular * 1.5 || (o.fsMax >= P.grandeRegular && o.peso >= 700);
    const lcMin = enorme ? APCA_MIN.enorme : (o.ui || grande || o.palavras <= 3) ? APCA_MIN.grande : APCA_MIN.apoio;
    if (Math.abs(o.lc) < lcMin && o.wcag >= min) p.push(["AVISO", `APCA Lc ${Math.round(Math.abs(o.lc))} < ${lcMin}`]);
    if (o.fundoDesvio > 0.12 && o.wcagP10 < min) p.push(["AVISO", `fundo agitado atrás do texto (pior trecho ${r2(o.wcagP10)}:1)`]);
  }
  // zona segura
  if (Z && !o.ui) {
    const f = fora(o.bbox, Z.seguro); const pr = Z.proibido.some((r) => cruza(o.bbox, r));
    if (f > 4 || pr) p.push(["FALHA", f > 4 ? `fora da zona segura (${Math.round(f)} px)` : "em cima da coluna de botões"]);
    else if (Z.ideal && fora(o.bbox, Z.ideal) > 4) p.push(["AVISO", `fora da área ideal (y ${Z.ideal[1]}–${Z.ideal[3]}): legenda/CTA de anúncio cobre`]);
  } else if (Z && o.ui) {
    const f = fora(o.bbox, [0, Z.seguro[1], W, Z.seguro[3]]);
    if (f > 4 && o.bbox[1] < Z.seguro[3] && o.bbox[3] > Z.seguro[1]) p.push(["INFO", "UI cortada pela zona (ok se não precisa ser lida)"]);
  }
  if (o.surgindo) for (const x of p) if (x[0] !== "INFO") { x[0] = "INFO"; x[1] += " (entrando/saindo: opacidade parcial)"; }
  if (o.movendo) for (const x of p) if (x[0] !== "INFO" && !/contraste|APCA|fundo/.test(x[1])) { x[0] = "INFO"; x[1] += " (em movimento: confira no quadro parado)"; }
  if (papel === "título" && o.linhas > 3) p.push(["AVISO", `título em ${o.linhas} linhas (máx. 3)`]);
  if (papel === "título" && o.palavras > P.palavrasTitulo) p.push(["AVISO", `título com ${o.palavras} palavras (máx. ${P.palavrasTitulo})`]);
  return p;
}

const resultado = { cena: html, w: W, h: H, dur: DUR, perfil: perfilNome, zona: zonaNome, tempos: [], exposicao: [], erros };
if (fotosDir) fs.mkdirSync(fotosDir, { recursive: true });
let nF = 0, nA = 0;
const porProblema = new Map(); // tipo de problema → textos distintos (o resumo conta TEXTOS, não linhas repetidas em vários tempos)
const anotar = (nivel, tipo, quem) => { const k = nivel + " " + tipo; if (!porProblema.has(k)) porProblema.set(k, new Set()); porProblema.get(k).add(quem); };
const lin = [];
const say = (s = "") => lin.push(s);
say(`Cena: ${path.basename(html)}  ·  ${W}×${H}, ${r1(DUR)} s  ·  perfil ${perfilNome} (${P.nome})  ·  zona ${Z ? Z.nome : "nenhuma"}`);
say(`Tabela: rótulo ≥ ${P.rotuloMin} px · apoio ≥ ${P.apoioMin} px · título ≥ ${P.tituloMin} px · título:apoio ≥ ${P.razaoNiveis} · contraste ≥ 4,5:1 (≥ 3:1 se ≥ ${P.grandeRegular} px, ou ${P.grandeNegrito} px negrito)`);
for (const t of tempos) {
  // texto "em movimento" (câmera aproximando/afastando, cartão passando): mede de novo 0,15 s depois
  const depois = await ev(`frame(${Math.min(DUR, t + 0.15)}); __hvColetar(${JSON.stringify(UI_SEL)}, 0.02).map(o=>({id:o.id,fs:o.fsMax,bbox:o.bbox,op:o.op}))`);
  await vaiPara(t);
  const a64 = await foto();
  const blocos0 = await ev(`__hvColetar(${JSON.stringify(UI_SEL)}, 0.02)`);
  await ev(`(()=>{const s=document.createElement('style');s.id='__hv_oc';s.textContent=${JSON.stringify(OCULTA)};document.head.appendChild(s)})(); new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))`);
  const b64 = await foto();
  await ev(`document.getElementById('__hv_oc').remove(); new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))`);
  const px = await ev(`__hvPixels(${JSON.stringify(blocos0)}, ${JSON.stringify(a64)}, ${JSON.stringify(b64)})`);
  const dep = new Map(depois.map((o) => [o.id, o]));
  for (const o of px.blocos) { const d = dep.get(o.id); o.movendo = !!d && (Math.abs(d.fs / o.fsMax - 1) > 0.04 || Math.abs(d.bbox[0] - (o.bboxDom || o.bbox)[0]) + Math.abs(d.bbox[1] - (o.bboxDom || o.bbox)[1]) > 0.02 * W);
    o.surgindo = !d || Math.abs(d.op - o.op) > 0.05 || o.op < 0.9; } // entrando/saindo (opacidade mudando ou parcial)
  const blocos = px.blocos.filter((o) => o.renderizado && o.bbox[2] > 0 && o.bbox[0] < W && o.bbox[3] > 0 && o.bbox[1] < H);
  // níveis de tamanho (fora de UI): agrupa tamanhos a menos de 15% um do outro
  const tam = [...new Set(blocos.filter((o) => !o.ui).map((o) => Math.round(o.fsMax)))].sort((a, b) => b - a);
  const niveis = []; for (const s of tam) { if (!niveis.length || s < niveis[niveis.length - 1].ref / 1.15) niveis.push({ ref: s, min: s }); else niveis[niveis.length - 1].min = s; }
  const nivelDe = (o) => niveis.findIndex((n) => Math.round(o.fsMax) <= n.ref && Math.round(o.fsMax) >= n.min);
  const papelDe = (o) => (o.ui ? "UI" : (() => { const k = nivelDe(o); return k === 0 && niveis.length > 1 ? "título" : k === 0 ? "único" : k === 1 ? "apoio" : "detalhe"; })());
  const palavras = blocos.filter((o) => !o.ui).reduce((s, o) => s + o.palavras, 0);
  const palavrasUI = blocos.filter((o) => o.ui).reduce((s, o) => s + o.palavras, 0);
  const destaques = px.cores.filter((c) => !c.fundo);
  const corTexto = new Set(blocos.filter((o) => !o.ui).map((o) => { const [r, g, b] = o.tinta; const mx = Math.max(r, g, b), mn = Math.min(r, g, b); if (mx - mn < 40) return null; const hh = Math.round((Math.atan2(Math.sqrt(3) * (g - b), 2 * r - g - b) * 180) / Math.PI / 30); return hh; }).filter((x) => x !== null));
  const geral = [];
  if (niveis.length >= 2 && niveis[0].min / niveis[1].ref < P.razaoNiveis) geral.push(["AVISO", `título e apoio perto demais (${niveis[0].min} × ${niveis[1].ref} px = ${r2(niveis[0].min / niveis[1].ref)}; mín. ${P.razaoNiveis})`]);
  if (niveis.length && niveis[0].ref < P.tituloMin && palavras > 0) geral.push(["AVISO", `o maior texto da tela tem ${niveis[0].ref} px (título ≥ ${P.tituloMin} px): nada puxa o olho primeiro`]);
  if (niveis.length > 3) geral.push(["AVISO", `${niveis.length} tamanhos de texto fora de UI (máx. 3 níveis): ${niveis.map((n) => n.ref).join(" / ")} px`]);
  const n1 = blocos.filter((o) => !o.ui && nivelDe(o) === 0 && niveis.length > 1);
  if (n1.length > 2) geral.push(["AVISO", `${n1.length} blocos competindo no nível 1`]);
  if (palavras > P.palavrasTelaMax) geral.push(["FALHA", `${palavras} palavras fora de UI na tela (máx. ${P.palavrasTelaMax})`]);
  else if (palavras > P.palavrasTela) geral.push(["AVISO", `${palavras} palavras fora de UI na tela (ideal ≤ ${P.palavrasTela})`]);
  if (destaques.length > 2) geral.push(["AVISO", `${destaques.length} cores de destaque no quadro (1 destaque + no máx. 1 semântica)`]);
  if (corTexto.size > 2) geral.push(["AVISO", `texto em ${corTexto.size} matizes diferentes`]);
  const itens = blocos.map((o) => { const papel = papelDe(o); const prob = julgar(o, papel, P); const nivel = prob.some((x) => x[0] === "FALHA") ? "FALHA" : prob.some((x) => x[0] === "AVISO") ? "AVISO" : "OK"; return { ...o, papel, prob, nivel }; });
  itens.sort((a, b) => b.fsMax - a.fsMax);
  for (const g of geral) { g[0] === "FALHA" ? nF++ : nA++; anotar(g[0], g[1].replace(/\d+([,.]\d+)?/g, "N").replace(/(N( \/ N)+)/, "N / …"), `t=${r2(t)}`); }
  for (const o of itens) for (const x of o.prob) { if (x[0] === "INFO") continue; anotar(x[0], x[1].replace(/\d+([,.]\d+)?/g, "N"), o.texto.slice(0, 24)); }
  say(""); say(`== t = ${r2(t)} s ==  palavras: ${palavras} (+${palavrasUI} em UI)  ·  níveis: ${niveis.map((n) => n.ref + " px").join(" → ") || "—"}${niveis.length > 1 ? `  (razão ${r2(niveis[0].min / niveis[1].ref)})` : ""}  ·  destaques de cor: ${destaques.length ? destaques.map((c) => `${c.cor} ${r1(c.parte * 100)}%`).join(", ") : "nenhum"}${px.cores.some((c) => c.fundo) ? `  (fundo colorido ${px.cores.filter((c) => c.fundo).map((c) => c.cor).join(",")})` : ""}`);
  for (const g of geral) say(`  ${g[0].padEnd(5)} ${g[1]}`);
  // UI com tudo ok vira uma linha só (a interface tem muitos rótulos)
  const uiOk = itens.filter((o) => o.ui && o.nivel === "OK");
  // textos iguais em tamanho/peso/fonte/problema viram uma linha só ("×N")
  const grupos = new Map();
  for (const o of itens) {
    if (o.ui && o.nivel === "OK") continue;
    const k = [o.nivel, o.papel, Math.round(o.fsMax), o.peso, o.familia, hex(o.tinta), hex(o.fundo), o.prob.map((x) => x[1].replace(/\(\d+ px\)/, "")).join("|")].join("~");
    if (!grupos.has(k)) grupos.set(k, []); grupos.get(k).push(o);
  }
  for (const g of grupos.values()) {
    const o = g[0];
    const txt = g.length > 1 ? g.slice(0, 3).map((x) => `"${x.texto.slice(0, 16)}"`).join(", ") + (g.length > 3 ? "…" : "") : `"${o.texto.length > 34 ? o.texto.slice(0, 33) + "…" : o.texto}"`;
    say(`  ${o.nivel.padEnd(5)} ${o.papel.padEnd(7)} ${String(Math.round(o.fsMax)).padStart(3)} px ${o.peso} ${o.familia.slice(0, 0x10).padEnd(0x10)} ${g.length > 1 ? `×${g.length} ` : ""}${txt}  ${r2(o.wcag)}:1 Lc ${Math.round(Math.abs(o.lc))}  ${hex(o.tinta)}/${hex(o.fundo)}${o.prob.length ? "  → " + o.prob.map((x) => x[1]).join("; ") : ""}`);
  }
  if (uiOk.length) { const mn = Math.min(...uiOk.map((o) => o.fs)); const cmin = Math.min(...uiOk.map((o) => o.wcag)); say(`  OK    UI      ${uiOk.length} textos de interface ok (menor ${Math.round(mn)} px, pior contraste ${r2(cmin)}:1)`); }
  if (!itens.length) say("  (nenhum texto visível)");
  resultado.tempos.push({ t, palavras, palavrasUI, niveis: niveis.map((n) => n.ref), cores: px.cores, geral, textos: itens.map(({ rects, ...o }) => o) });
  if (fotosDir) {
    await ev(`__hvMarcas(${JSON.stringify(itens.map((o) => ({ bbox: o.bbox, nivel: o.nivel, rot: `${Math.round(o.fsMax)}px ${r1(o.wcag)}:1` })))}, ${JSON.stringify(Z)}); new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))`);
    const r = await cdp("Page.captureScreenshot", { format: "jpeg", quality: 85, clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
    fs.writeFileSync(path.join(fotosDir, `t${String(Math.round(t * 100)).padStart(5, "0")}.jpg`), Buffer.from(r.result.data, "base64"));
    await ev("__hvLimpa()");
  }
}

// ---------------------------------------------------------------- 4) exposição
if (runs.length) {
  say(""); say(`== Tempo de exposição (varredura a cada ${r1(passo)} s; mínimo = máx(1 s; 0,5 s + 0,33 s × palavras); FALHA abaixo de 70% do mínimo) ==`);
  let curtos = 0;
  const vistos = new Set();
  for (const r of runs.sort((a, b) => a.iniT - b.iniT)) {
    const dur = r.fimT - r.iniT + passo; const min = tempoMinimo(r.palavras);
    const chave = r.texto + "@" + r.iniT; if (vistos.has(chave)) continue; vistos.add(chave);
    if (!r.palavras || r.contador) continue;
    const soNumero = !/\p{L}{2,}/u.test(r.texto); // relógio/contador/preço: AVISO, não FALHA
    const st = dur >= min ? "OK" : r.ateFim ? "INFO" : dur >= 0.7 * min || soNumero ? "AVISO" : "FALHA";
    resultado.exposicao.push({ texto: r.texto, palavras: r.palavras, de: r.iniT, ate: +(r.fimT + passo).toFixed(2), dur: +dur.toFixed(2), min, status: st });
    if (st === "OK") continue;
    if (st === "FALHA") { nF++; curtos++; anotar("FALHA", "pouco tempo na tela para ler", r.texto.slice(0, 24)); } else if (st === "AVISO") { nA++; anotar("AVISO", "pouco tempo na tela para ler", r.texto.slice(0, 24)); }
    const txt = r.texto.length > 40 ? r.texto.slice(0, 39) + "…" : r.texto;
    say(`  ${st.padEnd(5)} "${txt}" ficou ${r1(dur)} s (${r1(r.iniT)}–${r1(r.fimT + passo)} s), precisa de ${r1(min)} s para ${r.palavras} palavra(s)${r.ateFim ? " — vai até o fim da cena: conte a próxima" : ""}`);
  }
  const ok = resultado.exposicao.filter((e) => e.status === "OK").length;
  say(`  ${ok} de ${resultado.exposicao.length} textos ficam tempo suficiente para ler.`);
}
say(""); say("== Resumo por problema (textos distintos) ==");
const ordem = [...porProblema.entries()].sort((a, b) => (a[0] < b[0] ? -1 : 1));
for (const [k, set] of ordem) say(`  ${k.padEnd(0x4e).slice(0, 0x4e)} ${String(set.size).padStart(3)}  ex.: ${[...set].slice(0, 3).map((x) => `"${x}"`).join(", ")}`);
const nFd = ordem.filter(([k]) => k.startsWith("FALHA")).reduce((s, [, v]) => s + v.size, 0), nAd = ordem.filter(([k]) => k.startsWith("AVISO")).reduce((s, [, v]) => s + v.size, 0);
resultado.resumo = ordem.map(([k, v]) => ({ problema: k, textos: [...v] }));
nF = nFd; nA = nAd;
say(""); say(`== Resumo: ${nF} falha(s), ${nA} aviso(s)${erros.length ? `  ·  erros de JS na cena: ${[...new Set(erros)].slice(0, 3).join(" | ")}` : ""} ==`);
console.log(lin.join("\n"));
resultado.falhas = nF; resultado.avisos = nA;
if (jsonOut) fs.writeFileSync(path.resolve(jsonOut), JSON.stringify(resultado, null, 1));
if (fotosDir) {
  const fotos = fs.readdirSync(fotosDir).filter((f) => /^t\d+\.jpg$/.test(f)).sort();
  const cols = Math.min(fotos.length, W > H ? 3 : 5), rows = Math.ceil(fotos.length / cols);
  const larg = W > H ? 640 : 360;
  const r = spawnSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", "1", "-pattern_type", "glob", "-i", path.join(fotosDir, "t*.jpg"), "-vf", `scale=${larg}:-2,tile=${cols}x${rows}:padding=6:color=0x141418`, "-frames:v", "1", "-update", "1", path.join(fotosDir, "folha.jpg")]);
  console.log(r.status === 0 ? `folha: ${path.join(fotosDir, "folha.jpg")}` : `fotos em ${fotosDir}`);
}
await fim(nF ? 1 : 0);
