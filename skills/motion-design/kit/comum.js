// motion-design · base das cenas. Cada cena é uma função PURA do tempo: frame(t) desenha o segundo t
// (nada de transição/animação de CSS) — assim a gravação quadro a quadro sai idêntica e com desfoque de movimento.
// A marca vem do projeto: marca.css (variáveis --m-*) e marca.js (window.MARCA). Nada de marca fixa aqui.

// ---------- tempo e curvas ----------
const C=x=>Math.max(0,Math.min(1,x)), p=(t,a,b)=>C((t-a)/(b-a));
const eo=x=>1-Math.pow(1-C(x),3), eio=x=>{x=C(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;};
const back=(x,s=1.7)=>{x=C(x);const c3=s+1;return 1+c3*Math.pow(x-1,3)+s*Math.pow(x-1,2);};
const $=id=>document.getElementById(id);
const typed=(s,t,a,b)=>s.slice(0,Math.round(s.length*p(t,a,b)));
const M=window.MARCA||{};
// dinheiro no formato da marca (MARCA.moeda = 'BRL'|'USD'|..., MARCA.locale = 'pt-BR'|...)
const dinheiro=(n,casas=0)=>new Intl.NumberFormat(M.locale||'pt-BR',{style:'currency',currency:M.moeda||'BRL',minimumFractionDigits:casas,maximumFractionDigits:casas}).format(n);
// cor da marca pelo nome da variável (--m-cor → cor('cor'))
const cor=n=>getComputedStyle(document.documentElement).getPropertyValue('--m-'+n).trim();

// ---------- entrada/saída ----------
// entra em a (mola), sai em b; o: {x,y,s,d,od,r,k,base}; devolve o quanto está visível
function pop(el,t,a,b=1e9,o={}){
  const y=o.y??30,x=o.x??0,s=o.s??.9,d=o.d??.55,od=o.od??.35,r=o.r??0;
  const k=back(p(t,a,a+d),o.k??1.4), f=eo(p(t,a,a+d*.6)), z=1-eio(p(t,b,b+od)), v=Math.min(f,z);
  el.style.opacity=v.toFixed(3); el.style.visibility=v<=.001?'hidden':'visible';
  el.style.transform=(o.base||'')+` translate(${(x*(1-k)).toFixed(1)}px,${(y*(1-k)+(1-z)*-12).toFixed(1)}px) scale(${(s+(1-s)*k).toFixed(4)}) rotate(${(r*(1-k)).toFixed(2)}deg)`;
  return v;
}
function vis(el,v){el.style.opacity=v.toFixed(3);el.style.visibility=v<=.001?'hidden':'visible';}
// palavras que sobem uma a uma: <span class="w">…</span>; T = tempos (um por palavra) ou passo fixo
function palavras(root,t,T,b=1e9){root.querySelectorAll('.w').forEach((w,i)=>pop(w,t,Array.isArray(T)?T[i]:T+i*.09,b,{y:40,s:.96,d:.5}));}

// ---------- fundo, cor e máscara ----------
// degradê em malha que se mexe: cols = [[cor, x%, y%, raio%], ...]; base = cor de fundo
function mesh(el,t,cols,base,vel=1){el.style.background=cols.map(([c,x,y,r],i)=>{const dx=Math.sin(t*.35*vel+i*1.7)*9,dy=Math.cos(t*.3*vel+i*2.3)*9;return `radial-gradient(${r}% ${r}% at ${(x+dx).toFixed(1)}% ${(y+dy).toFixed(1)}%,${c},transparent 70%)`}).join(',')+','+base;}
// cor intermediária entre dois hex (#rrggbb)
function mix(a,b,k){const h=s=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16));const A=h(a),B=h(b);return '#'+A.map((v,i)=>Math.round(v+(B[i]-v)*C(k)).toString(16).padStart(2,'0')).join('');}
// revela num círculo a partir de (x,y) do elemento
function wipe(el,t,a,d=.6,x='50%',y='50%'){const k=eio(p(t,a,a+d));el.style.clipPath=k>=1?'none':`circle(${(k*150).toFixed(1)}% at ${x} ${y})`;el.style.visibility=k<=0?'hidden':'visible';}

// ---------- ícones (traço, 24x24) ----------
const ICON={
  check:'<path d="m5 12.5 4.5 4.5L19 7.5"/>',x:'<path d="M6 6l12 12M18 6 6 18"/>',
  bolt:'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',star:'<path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4 6.1 20.5l1.2-6.5L2.5 9.4l6.6-.9z"/>',
  lock:'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
  phone:'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
  chat:'<path d="M21 11.5a8.4 8.4 0 0 1-12.8 7.2L3 20.5l1.4-4.1A8.4 8.4 0 1 1 21 11.5z"/>',
  cal:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',user:'<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
  globe:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
  spark:'<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>',trend:'<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
  coin:'<circle cx="12" cy="12" r="9"/><path d="M14.8 9.2A3 3 0 0 0 12 8c-1.7 0-3 .9-3 2s1.3 1.7 3 2 3 .9 3 2-1.3 2-3 2a3 3 0 0 1-2.8-1.2M12 6v2m0 8v2"/>',
  palette:'<circle cx="12" cy="12" r="9"/><circle cx="8" cy="10" r="1.3"/><circle cx="12" cy="7.5" r="1.3"/><circle cx="16" cy="10" r="1.3"/><path d="M12 21a2.5 2.5 0 0 1 0-5h1.5a2 2 0 0 0 2-2"/>',
  play:'<path d="M7 4l13 8-13 8z"/>',heart:'<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/>',
};
const ic=(n,sz=28,c='currentColor',sw=2.4)=>`<svg width="${sz}" height="${sz}" viewBox="0 0 24 24" fill="none" stroke="${c}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${ICON[n]||''}</svg>`;

// ---------- marca ----------
// LOGO(h): usa MARCA.logo (SVG em texto ou caminho de imagem) + MARCA.nome; h = altura em px
function LOGO(h=90,o={}){const l=M.logo||'';const img=l.trim().startsWith('<svg')?l.replace('<svg',`<svg height="${h}" style="height:${h}px;width:auto;display:block"`):l?`<img src="${l}" style="height:${h}px;display:block" alt="">`:'';
  return `<span style="display:inline-flex;align-items:center;gap:${h*.24}px">${img}${o.semNome||!M.nome?'':`<b style="font:800 ${h*.62}px var(--m-titulo);letter-spacing:-.02em;color:${o.cor||'inherit'}">${M.nome}</b>`}</span>`;}

// ---------- telas reais (fotos de app/site) ----------
// barra de navegador; url pode ter HTML (ex.: <span id="u"></span> para digitar)
const NAV=(url,lock=true)=>`<div class="bar"><i style="background:#FF5F57"></i><i style="background:#FEBC2E"></i><i style="background:#28C840"></i><div class="url">${lock?'<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#1E8E3E" stroke-width="2.8"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>':''}<span class="u">${url}</span></div></div>`;
// navegador com fotos de telas/ (w×h = tamanho da foto em px CSS; fotos em 2x); várias fotos = troca com seq()
function TELA(id,fotos,url='',w=1600,h=900){return `<div class="bw tela" id="${id}" style="width:${w}px;height:${h+52}px">${NAV(url)}<div class="pg">${fotos.map((f,i)=>`<img src="telas/${f}.jpg" id="${id}-${i}" style="position:absolute;left:0;top:0;width:${w}px;height:${h}px;opacity:${i?0:1}">`).join('')}</div></div>`;}
// celular com foto de telas/ (430x932 em 3x)
function CEL(id,fotos,w=470){const h=w*932/430;return `<div class="cel" id="${id}" style="width:${w+32}px;height:${h+32}px"><div class="tela-cel"><div class="ilha"></div>${fotos.map((f,i)=>`<img src="telas/${f}.jpg" id="${id}-${i}" style="opacity:${i?0:1}">`).join('')}</div></div>`;}
// sequência de fotos: S = [[t, índice], ...]; cada troca entra por cima com fade de d s; devolve o índice atual
function seq(id,n,S,t,d=.25){let c=0;S.forEach(([a],k)=>{if(t>=a)c=k;});const cur=S[c][1],prev=c?S[c-1][1]:-1,a=S[c][0];
  for(let k=0;k<n;k++){const e=$(id+'-'+k);if(!e)continue;e.style.opacity=k===cur?(c?Math.min(1,p(t,a,a+d)):1):(k===prev?1:0);e.style.zIndex=k===cur?2:1;}return cur;}
// câmera sobre uma tela: K = [[t, x, y, zoom], ...] (x,y em px da foto); centro = ponto do palco que recebe (x,y)
function cam(el,t,K,d=.9,centro=[960,540]){let x=K[0][1],y=K[0][2],s=K[0][3];
  for(let i=1;i<K.length;i++){const k=eio(p(t,K[i][0],K[i][0]+d));x+=(K[i][1]-x)*k;y+=(K[i][2]-y)*k;s+=(K[i][3]-s)*k;}
  el.style.transform=`translate(${(centro[0]-x*s).toFixed(1)}px,${(centro[1]-(y+52)*s).toFixed(1)}px) scale(${s.toFixed(4)})`;return s;}
// holofote num retângulo [x,y,w,h] da foto: borda de destaque e o resto escurecido
function spot(el,t,a,b,r,pad=10){const v=Math.min(eo(p(t,a,a+.45)),1-eio(p(t,b,b+.35)));const dc=cor('destaque')||'#e8b867';
  el.style.left=(r[0]-pad)+'px';el.style.top=(r[1]+52-pad)+'px';el.style.width=(r[2]+2*pad)+'px';el.style.height=(r[3]+2*pad)+'px';
  el.style.boxShadow=`0 0 0 ${(5*v).toFixed(1)}px ${dc},0 0 0 4000px rgba(10,10,14,${(.6*v).toFixed(3)})`;el.style.opacity=v>0?1:0;el.style.transform=`scale(${(1.08-.08*eo(p(t,a,a+.5))).toFixed(4)})`;}
// cursor: K = [[t,x,y],...] em px do palco; cl = tempos de clique; vis = [aparece, some]. Precisa de CURSOR no HTML.
const CURSOR='<svg id="cur" viewBox="0 0 24 24"><path d="M4 2l15 11-6.5 1.2 3.8 7.2-3 1.6-3.8-7.3L4 20z" fill="#fff" stroke="#11121A" stroke-width="1.4" stroke-linejoin="round"/></svg><div class="rip" id="rip"></div>';
function cursor(t,K,cl=[],v=[0,1e9]){const c=$('cur'),r=$('rip');let x=K[0][1],y=K[0][2];
  for(let i=1;i<K.length;i++){const [a,X,Y]=K[i],[b]=K[i-1];const k=eio(p(t,b,a));if(t>=b){const arc=Math.sin(Math.PI*k)*.08;const px=x,py=y;x=px+(X-px)*k-(Y-py)*arc;y=py+(Y-py)*k+(X-px)*arc;}}
  const on=t>=v[0]&&t<=v[1], dn=cl.some(a=>t>a-.06&&t<a+.1);
  c.style.opacity=on?Math.min(eo(p(t,v[0],v[0]+.25)),1-eio(p(t,v[1]-.25,v[1]))):0;
  c.style.transform=`translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${dn?.82:1})`;
  const a=cl.find(a=>t>=a&&t<a+.55);if(a!=null){const k=p(t,a,a+.55);r.style.opacity=(1-k).toFixed(3);r.style.transform=`translate(${(x+6).toFixed(1)}px,${(y+6).toFixed(1)}px) scale(${(.3+1.1*eo(k)).toFixed(3)})`;}else r.style.opacity=0;}

// ---------- cena ----------
// cena(DURAÇÃO, frame): registra a cena. ?play no endereço = assistir em loop no navegador.
function cena(DUR,fn){
  window.DUR=DUR; window.frame=fn;
  if(/[?&]play/.test(location.search)){const st=$('st');const W=st.offsetWidth,H=st.offsetHeight;const fit=()=>{const s=Math.min(innerWidth/W,innerHeight/H);st.style.transformOrigin='0 0';st.style.transform=`scale(${s})`;document.body.style.background='#333';};addEventListener('resize',fit);fit();
    document.fonts.ready.then(()=>{const t0=performance.now();(function loop(){fn(((performance.now()-t0)/1000)%(DUR+.6));requestAnimationFrame(loop)})()});}
  else document.fonts.ready.then(()=>fn(0));
}
