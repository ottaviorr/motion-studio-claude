// motion-design · MISTURA de vídeo real + design desenhado/tipografia, com a animação guiada pela música (17/10/2026).
// Carregue DEPOIS de comum.js e movimento.js (usa C, p, eo, eio, sai, chega, forte, tq, hs, vn).
// Regra técnica (HyperFrames): tudo é função pura de t. Música, física, recorte e rastreio são PRÉ-CALCULADOS fora da cena
// (analisar_musica.py, simular_queda.mjs, recortar.py) e a cena só lê os dados (<script src="x.js"> com window.*_DADOS).
// O <video> é sempre o do HyperFrames (data-start/data-duration/data-media-start/data-track-index): ele injeta os quadros.
// Por isso nada aqui põe vídeo dentro de SVG/canvas: o efeito é (a) uma camada POR CIMA com furo (letra vazada, pincel),
// (b) clip-path/filter no próprio <video> (janelas, colagem, duotone) ou (c) canvas com PNGs pré-carregados (recorte do sujeito).
// (A demo de cada helper fica só no estúdio de trabalho.)

// ---------- utilidades ----------
const NS = 'http://www.w3.org/2000/svg';
const svgEl = (tag, at = {}, pai) => { const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); if (pai) pai.appendChild(e); return e; };
// gerador com semente (mulberry32): mesma semente = mesma borda rasgada / mesma pincelada em todo render
function semente(s) { s = s >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
// mede texto (caixa real da tinta) — font = '900 100px Archivo'
const _cv = document.createElement('canvas').getContext('2d');
function medeTexto(s, font) { _cv.font = font; const m = _cv.measureText(s); return { w: m.actualBoundingBoxLeft + m.actualBoundingBoxRight, l: m.actualBoundingBoxLeft, asc: m.actualBoundingBoxAscent, desc: m.actualBoundingBoxDescent, adv: m.width }; }
// tamanho de fonte para a palavra ocupar `largura` px (fonte = '900 {}px Archivo' — o {} vira o tamanho)
function encaixaFonte(s, fonte, largura) { const m = medeTexto(s, fonte.replace('{}', 100)); return largura / m.w * 100; }
// ponto normalizado (0–1) de um vídeo com object-fit:cover dentro da caixa [l,t,w,h] do palco → px do palco
function pontoNoVideo(u, v, caixa, fonte = [1080, 1920]) {
  const [l, t, w, h] = caixa, s = Math.max(w / fonte[0], h / fonte[1]), sw = fonte[0] * s, sh = fonte[1] * s;
  return [l + (w - sw) / 2 + u * sw, t + (h - sh) / 2 + v * sh];
}

// ---------- MÚSICA (dados do analisar_musica.py) ----------
// const MUSICA = musica(window.MUSICA_DADOS)  →  .batidas .compassos .onsets .secoes .drops .bpm .batida
//   .energia(t) / .grave(t)    0–1, interpolado por quadro, com ataque rápido e soltura lenta (não treme)
//   .perto(t, lista?)          batida (ou item da lista) mais perto de t   ·  .antes(t, lista?) última que já passou
//   .pulso(t, decai=.18, lista?) 1 no golpe → 0 (exponencial) · .secao(t) {ini,fim,tipo,nivel} · .indice(t) nº da batida
function musica(D) {
  if (!D) throw new Error('musica(): faltam os dados — <script src="x.musica.js"> antes da cena (analisar_musica.py)');
  const fps = D.fps || 30, E = D.energia || [], G = D.grave || [];
  const amostra = (A, t) => { const x = C(t * fps / Math.max(1, A.length - 1)) * (A.length - 1), i = Math.floor(x), f = x - i; return A.length ? A[i] * (1 - f) + (A[Math.min(i + 1, A.length - 1)]) * f : 0; };
  // envelope: sobe em ~1 quadro, desce em ~0,35 s (lido para trás: função pura de t, sem estado)
  const env = (A, t, sol = .35) => { let v = 0; for (let k = 0; k <= 12; k++) { const dt = k / fps; v = Math.max(v, amostra(A, t - dt) * Math.exp(-dt / sol)); } return v; };
  const lista = (l) => l || D.batidas;
  const antesDe = (t, l) => { l = lista(l); let r = null; for (const b of l) { const x = Array.isArray(b) ? b[0] : b; if (x <= t + 1e-6) r = x; else break; } return r; };
  return {
    ...D, onsetsT: (D.onsets || []).map((o) => o[0]),
    energia: (t, sol) => env(E, t, sol), grave: (t, sol) => env(G, t, sol), energiaCrua: (t) => amostra(E, t),
    perto: (t, l) => { l = lista(l); let m = l[0], d = 1e9; for (const b of l) { const x = Array.isArray(b) ? b[0] : b; if (Math.abs(x - t) < d) { d = Math.abs(x - t); m = x; } } return m; },
    antes: antesDe,
    indice: (t) => { let i = -1; D.batidas.forEach((b, k) => { if (b <= t + 1e-6) i = k; }); return i; },
    pulso: (t, decai = .18, l) => { const a = antesDe(t, l); return a == null ? 0 : Math.exp(-(t - a) / decai); },
    secao: (t) => (D.secoes || []).find((s) => t >= s.ini && t < s.fim) || (D.secoes || [])[D.secoes.length - 1] || { tipo: 'cheio', nivel: 1 },
  };
}

// naBatida(t, MUSICA, alvo, o) — entrada presa à batida/onset mais próximo de `alvo` (s). Devolve {k, a, v, pulso}:
//   k 0→1 (curva `sai`, com antecipação de o.antes s recuando o.recuo), a = instante do golpe, v = visível (0/1), pulso 1→0 depois do golpe.
//   o.em: 'batida' (padrão) | 'compasso' | 'onset' (só onsets com força ≥ o.forca, padrão .35) · o.d duração da entrada (.28)
//   Uso: const e = naBatida(t, MUSICA, 2.1); el.style.transform = `translateY(${(1-e.k)*120}px) scale(${1+.08*e.pulso})`;
function naBatida(t, M, alvo, o = {}) {
  const l = o.em === 'compasso' ? M.compassos : o.em === 'onset' ? M.onsets.filter((x) => x[1] >= (o.forca ?? .35)).map((x) => x[0]) : M.batidas;
  const a = M.perto(alvo, l), d = o.d ?? .28, pre = o.antes ?? .12;
  const k = t < a ? -(o.recuo ?? .06) * eio(p(t, a - pre, a)) : sai(p(t, a, a + d));
  return { k, a, v: t >= a - pre ? 1 : 0, pulso: t >= a ? Math.exp(-(t - a) / (o.decai ?? .16)) : 0 };
}
// palavras numa lista de elementos, uma por batida a partir de `desde` (pula `passo` batidas entre elas). Devolve os tempos.
function palavrasNaBatida(els, t, M, desde, passo = 1, o = {}) {
  const i0 = M.batidas.findIndex((b) => b >= desde - .05), T = [];
  els.forEach((el, i) => { const a = M.batidas[Math.min(M.batidas.length - 1, i0 + i * passo)] ?? desde + i * M.batida * passo; T.push(a);
    const e = naBatida(t, M, a, o); el.style.opacity = e.v ? 1 : 0;
    el.style.transform = `translateY(${((1 - e.k) * (o.y ?? 90)).toFixed(1)}px) scale(${(1 + (o.soco ?? .06) * e.pulso).toFixed(4)})`; });
  return T;
}

// respira(t, MUSICA, el?, o) — fonte variável/escala seguindo a energia. o: {wght:[300,900], wdth:[75,125], escala:[1,1.05], fonte:'energia'|'grave', sol}
//   Devolve a energia usada (0–1). Sem `el`, só devolve o número (para usar em qualquer coisa: brilho, grão, desfoque).
//   A fonte precisa ter os eixos (Archivo wdth 62–125 wght 100–900, Roboto Flex, Fraunces…): pedir no Google Fonts com a faixa.
function respira(t, M, el, o = {}) {
  const e = (o.fonte === 'grave' ? M.grave : M.energia)(t, o.sol ?? .35);
  if (el) {
    const ax = []; for (const k of ['wght', 'wdth', 'opsz', 'slnt']) if (o[k]) ax.push(`'${k}' ${(o[k][0] + (o[k][1] - o[k][0]) * e).toFixed(1)}`);
    if (ax.length) el.style.fontVariationSettings = ax.join(',');
    if (o.escala) el.style.transform = (o.base || '') + ` scale(${(o.escala[0] + (o.escala[1] - o.escala[0]) * e).toFixed(4)})`;
  }
  return e;
}

// ---------- 1 · letraComVideo: vídeo dentro de texto gigante (a camada de cor tem a palavra vazada; o vídeo fica EMBAIXO) ----------
// const L = letraComVideo(pai, {texto:'BRASA', fonte:"400 {}px Anton", familia:'Anton', cor:'#D7261E', largura:940, x:70, topo:440, esticaY:1})
// L.quadro(t, {escala, origem:[x,y]})  → mergulho: escala 1 → 60 com pico no corte (use p(t,a,b)**3.2, como a 11)
function letraComVideo(pai, o) {
  const id = 'lv' + Math.floor(semente(o.texto.length * 97 + (o.x | 0))() * 1e6);
  const sv = svgEl('svg', { width: 1080, height: 1920, style: 'position:absolute;left:0;top:0;overflow:visible;pointer-events:none' }, pai);
  const mk = svgEl('mask', { id, maskUnits: 'userSpaceOnUse', x: -5e4, y: -5e4, width: 1e5, height: 1e5 }, svgEl('defs', {}, sv));
  svgEl('rect', { x: -5e4, y: -5e4, width: 1e5, height: 1e5, fill: '#fff' }, mk);
  const tx = svgEl('text', { 'font-family': o.familia, fill: '#000', 'font-weight': o.peso || 400 }, mk); tx.textContent = o.texto;
  const capa = svgEl('rect', { x: -5e4, y: -5e4, width: 1e5, height: 1e5, fill: o.cor, mask: `url(#${id})` }, sv);
  let F = 0, M0 = null;
  const arruma = () => { F = encaixaFonte(o.texto, o.fonte, o.largura ?? 940); M0 = medeTexto(o.texto, o.fonte.replace('{}', F)); const sy = o.esticaY ?? 1;
    tx.setAttribute('font-size', F.toFixed(1)); tx.setAttribute('transform', `translate(${((o.x ?? 70) + M0.l).toFixed(1)},${((o.topo ?? 440) + M0.asc * sy).toFixed(1)}) scale(1,${sy})`); };
  return {
    svg: sv, texto: tx, capa,
    caixa: () => { if (!M0) arruma(); const sy = o.esticaY ?? 1; return [o.x ?? 70, o.topo ?? 440, M0.w, (M0.asc + M0.desc) * sy]; },
    quadro(t, q = {}) { if (!M0) arruma(); const s = q.escala ?? 1, [ox, oy] = q.origem || [540, 960];
      sv.style.transformOrigin = `${ox}px ${oy}px`; sv.style.transform = `scale(${s.toFixed(4)})`; sv.style.opacity = q.opacidade ?? 1; },
  };
}

// ---------- 2 · janelas: grade suíça de N células com vídeos que abrem/fecham ----------
// const J = janelas(['v1','v2','v3','v4'], {colunas:2, margem:96, calha:24, topo:420, base:1500})   (ids de <video> do HF)
// J.quadro(t, abre, fecha, {passo:.08, dir:'v'|'h'})  → cada célula abre do meio (clip-path inset) com `forte`, em escada
// J.celulas = [[l,t,w,h], ...] para alinhar texto à grade
function janelas(ids, o = {}) {
  const n = ids.length, col = o.colunas ?? 2, lin = Math.ceil(n / col), m = o.margem ?? 96, g = o.calha ?? 24;
  const L = o.largura ?? 1080, top = o.topo ?? 420, bot = o.base ?? 1500;
  const cw = (L - 2 * m - (col - 1) * g) / col, ch = (bot - top - (lin - 1) * g) / lin;
  const cel = ids.map((_, i) => [m + (i % col) * (cw + g), top + Math.floor(i / col) * (ch + g), cw, ch]);
  ids.forEach((id, i) => { const e = $(id), [l, t, w, h] = cel[i]; Object.assign(e.style, { position: 'absolute', left: l + 'px', top: t + 'px', width: w + 'px', height: h + 'px', objectFit: 'cover' }); });
  return {
    celulas: cel,
    quadro(t, abre, fecha = 1e9, q = {}) { const ps = q.passo ?? .08, d = q.d ?? .45;
      ids.forEach((id, i) => { const e = $(id), k = forte(p(t, abre + i * ps, abre + i * ps + d)) * (1 - forte(p(t, fecha + (n - 1 - i) * ps * .6, fecha + (n - 1 - i) * ps * .6 + d * .7)));
        const r = (1 - k) * 50; e.style.clipPath = q.dir === 'h' ? `inset(0 ${r.toFixed(2)}% 0 ${r.toFixed(2)}%)` : `inset(${r.toFixed(2)}% 0 ${r.toFixed(2)}% 0)`;
        e.style.transform = `scale(${(1.12 - .12 * k).toFixed(4)})`; e.style.opacity = k > .001 ? 1 : 0; });
    },
  };
}

// ---------- 3 · colagem: recorte com borda irregular de papel + sombra dura + rotação ----------
// const K = colagem('v3', {caixa:[120,520,840,760], semente:4, borda:18, papel:'#F4EEE2', sombra:[14,16,'#111'], rot:-3})
//   cria o papel atrás (div com o mesmo contorno, maior pela borda) e recorta o <video> com clip-path polygon (borda rasgada)
// K.quadro(t, a, sai?)  → "bate" na mesa: chega de 1,25× com rotação extra, a 12 fps (tq), e assenta; sai = some num rasgo para cima
function colagem(id, o) {
  const [l, t0, w, h] = o.caixa, R = semente(o.semente ?? 3), b = o.borda ?? 18, pts = [];
  const lado = (ax, ay, bx, by, n) => { for (let i = 0; i < n; i++) { const k = i / n, j = (R() - .5) * (o.rasgo ?? 14); pts.push([ax + (bx - ax) * k + (ay === by ? 0 : j), ay + (by - ay) * k + (ax === bx ? 0 : j)]); } };
  const N = o.dentes ?? 26; lado(0, 0, w, 0, N); lado(w, 0, w, h, N); lado(w, h, 0, h, N); lado(0, h, 0, 0, N);
  const poli = (pad) => 'polygon(' + pts.map(([x, y]) => `${(x + (x < w / 2 ? -pad : pad) * (1 + .5 * R())).toFixed(1)}px ${(y + (y < h / 2 ? -pad : pad) * (1 + .5 * R())).toFixed(1)}px`).join(',') + ')';
  const v = $(id), pai = v.parentNode, g = document.createElement('div'), papel = document.createElement('div');
  Object.assign(g.style, { position: 'absolute', left: l + 'px', top: t0 + 'px', width: w + 'px', height: h + 'px', transformOrigin: '50% 50%' });
  const [sx, sy, sc] = o.sombra || [14, 16, 'rgba(17,17,17,.9)'];
  g.style.filter = `drop-shadow(${sx}px ${sy}px 0 ${sc})`;
  Object.assign(papel.style, { position: 'absolute', inset: 0, background: o.papel ?? '#F4EEE2', clipPath: poli(b) });
  pai.insertBefore(g, v); g.appendChild(papel); g.appendChild(v);
  Object.assign(v.style, { position: 'absolute', left: 0, top: 0, width: w + 'px', height: h + 'px', objectFit: 'cover', clipPath: poli(0) });
  return {
    grupo: g, papel,
    quadro(t, a, z = 1e9) { const tt = tq(t, 12), k = sai(p(tt, a, a + .25)), ks = eio(p(t, z, z + .3)), rot = (o.rot ?? -3) + (1 - k) * 9 * (o.rot < 0 ? -1 : 1);
      g.style.opacity = t < a ? 0 : 1; g.style.visibility = t < a || ks >= 1 ? 'hidden' : 'visible';
      g.style.transform = `translateY(${(-1300 * ks).toFixed(1)}px) rotate(${(rot + 8 * ks).toFixed(2)}deg) scale(${(1.25 - .25 * k).toFixed(4)})`; },
  };
}

// ---------- 4 · pincelRevela: pinceladas com textura revelam o vídeo (camada de cor por cima com o furo das pinceladas), a 12 fps ----------
// const P = pincelRevela(pai, {cor:'#F2EEE6', semente:2, tracos:5, espessura:260})
// P.quadro(t, a, d=0.9) → os traços vão sendo pintados em zigue-zague (dasharray), bordas roídas por turbulência; d≈0,6–1,2 s
function pincelRevela(pai, o = {}) {
  const R = semente(o.semente ?? 2), id = 'pr' + Math.floor(R() * 1e6), L = o.largura ?? 1080, A = o.altura ?? 1920;
  const sv = svgEl('svg', { width: L, height: A, style: 'position:absolute;left:0;top:0;pointer-events:none' }, pai);
  const df = svgEl('defs', {}, sv);
  const fl = svgEl('filter', { id: id + 'f', x: '-20%', y: '-20%', width: '140%', height: '140%' }, df);
  svgEl('feTurbulence', { type: 'fractalNoise', baseFrequency: '.035 .09', numOctaves: 3, seed: o.semente ?? 2, result: 'n' }, fl);
  svgEl('feDisplacementMap', { in: 'SourceGraphic', in2: 'n', scale: o.roido ?? 70, xChannelSelector: 'R', yChannelSelector: 'G' }, fl);
  const mk = svgEl('mask', { id, maskUnits: 'userSpaceOnUse', x: 0, y: 0, width: L, height: A }, df);
  svgEl('rect', { width: L, height: A, fill: '#fff' }, mk);
  const gp = svgEl('g', { filter: `url(#${id}f)` }, mk), n = o.tracos ?? 5, esp = o.espessura ?? 260, tracos = [];
  for (let i = 0; i < n; i++) {   // zigue-zague de cima para baixo, cada traço levemente curvo
    const y = (i + .5) * A / n + (R() - .5) * 60, ida = i % 2 === 0, x0 = ida ? -120 : L + 120, x1 = ida ? L + 120 : -120, cy = y + (R() - .5) * 180;
    const pa = svgEl('path', { d: `M${x0},${y.toFixed(0)} Q${L / 2},${cy.toFixed(0)} ${x1},${(y + (R() - .5) * 90).toFixed(0)}`, fill: 'none', stroke: '#000', 'stroke-width': esp * (.85 + .3 * R()), 'stroke-linecap': 'round' }, gp);
    tracos.push(pa);
  }
  svgEl('rect', { width: L, height: A, fill: o.cor ?? '#F2EEE6', mask: `url(#${id})` }, sv);
  let comp = null;
  return {
    svg: sv,
    quadro(t, a, d = .9, q = {}) { if (!comp) comp = tracos.map((x) => x.getTotalLength()); const tt = tq(t, q.fps ?? 12), k = p(tt, a, a + d);
      tracos.forEach((x, i) => { const ki = C(k * n - i); x.setAttribute('stroke-dasharray', `${comp[i]} ${comp[i]}`); x.setAttribute('stroke-dashoffset', (comp[i] * (1 - eo(ki))).toFixed(1)); });
      sv.style.opacity = t < a - .001 ? (q.antesVisivel ? 1 : 0) : 1; },
  };
}

// ---------- 5 · linhaSegue: traço que segue pontos rastreados (recortar.py --ponto → sujeito.json "ponto", ou "topo"/"centro") ----------
// const S = linhaSegue(pai, DADOS, {caixa:[0,0,1080,1920], fonte:[w,h] do arquivo, campo:'ponto'|'topo'|'centro', cor, rastro:.6, inicio:tCena})
// S.quadro(t) → desenha o rastro dos últimos `rastro` s até o ponto atual + bolinha + rótulo (S.rotulo é um div para texto); devolve [x,y]
function linhaSegue(pai, D, o = {}) {
  const sv = svgEl('svg', { width: 1080, height: 1920, style: 'position:absolute;left:0;top:0;overflow:visible;pointer-events:none' }, pai);
  const pa = svgEl('path', { fill: 'none', stroke: o.cor ?? '#fff', 'stroke-width': o.espessura ?? 6, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, sv);
  const bo = svgEl('circle', { r: o.raio ?? 14, fill: o.cor ?? '#fff' }, sv);
  const ro = document.createElement('div'); Object.assign(ro.style, { position: 'absolute', left: 0, top: 0, whiteSpace: 'nowrap' }); pai.appendChild(ro);
  const campo = o.campo ?? (D.ponto && D.ponto.length ? 'ponto' : 'topo'), fps = D.fps || 30, fonte = o.fonte ?? [D.w, D.h];
  const pt = (i) => { i = Math.max(0, Math.min(D.n - 1, i)); const q = campo === 'ponto' ? D.ponto[i] : (D.quadros[i] || {})[campo]; return q ? pontoNoVideo(q[0], q[1], o.caixa ?? [0, 0, 1080, 1920], fonte) : null; };
  // suaviza (média de 5 quadros) para o traço não tremer com o ruído da máscara
  const ps = (i) => { let sx = 0, sy = 0, c = 0; for (let k = -2; k <= 2; k++) { const q = pt(i + k); if (q) { sx += q[0]; sy += q[1]; c++; } } return c ? [sx / c, sy / c] : null; };
  return {
    svg: sv, rotulo: ro,
    quadro(t, q = {}) { const t0 = o.inicio ?? 0, i = Math.round((t - t0) * fps), nr = Math.round((o.rastro ?? .6) * fps), cres = C(p(t, t0, t0 + (q.d ?? .5)));
      const P = []; for (let k = Math.max(0, i - nr); k <= i; k++) { const z = ps(k); if (z) P.push(z); }
      const vis = t >= t0 && P.length > 1 && i < D.n; sv.style.opacity = ro.style.opacity = vis ? (q.opacidade ?? 1) : 0;
      if (!vis) return null;
      pa.setAttribute('d', 'M' + P.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join('L'));
      const [x, y] = P[P.length - 1]; bo.setAttribute('cx', x.toFixed(1)); bo.setAttribute('cy', y.toFixed(1)); bo.setAttribute('r', ((o.raio ?? 14) * eo(cres)).toFixed(1));
      const [dx, dy] = o.desvio ?? [36, -70]; ro.style.transform = `translate(${(x + dx).toFixed(1)}px,${(y + dy).toFixed(1)}px)`;
      return [x, y]; },
  };
}

// ---------- 6 · atrasDoSujeito: texto ENTRE o fundo e a pessoa (recorte RGBA do recortar.py desenhado num canvas por cima do texto) ----------
// Ordem no HTML: <video> (HF) → texto → <canvas id="rc" width=1080 height=1920>. Chame atrasDoSujeito NO CARREGAMENTO do script
// (não dentro do frame): ele cria <img> escondidas que seguram o evento load, então o render só começa com tudo carregado.
// const A = atrasDoSujeito('rc', 'pasta-recorte', 90, {caixa:[0,0,1080,1920], fonte:[720,1280], inicio: tCena (= data-start do vídeo)})
// A.quadro(t, {transform}) → desenha o recorte do quadro certo (mesmo transform do vídeo, se ele tiver zoom); fora do trecho limpa
function atrasDoSujeito(idCanvas, pasta, n, o = {}) {
  const cv = $(idCanvas), cx = cv.getContext('2d'), imgs = [], box = document.createElement('div');
  box.style.cssText = 'position:absolute;width:1px;height:1px;overflow:hidden;opacity:0;pointer-events:none;left:-10px;top:-10px';
  for (let i = 0; i < n; i++) { const im = document.createElement('img'); im.src = `${pasta}/r_${String(i).padStart(4, '0')}.png`; box.appendChild(im); imgs.push(im); }
  (document.body || document.documentElement).appendChild(box);
  const fps = o.fps ?? 30;
  return {
    imagens: imgs,
    quadro(t, q = {}) { const i = Math.round((t - (o.inicio ?? 0)) * fps); cx.setTransform(1, 0, 0, 1, 0, 0); cx.clearRect(0, 0, cv.width, cv.height);
      if (i < 0 || i >= n) return false; const im = imgs[i]; if (!im.complete || !im.naturalWidth) return false;
      const [l, tp, w, h] = o.caixa ?? [0, 0, 1080, 1920], s = Math.max(w / im.naturalWidth, h / im.naturalHeight), sw = im.naturalWidth * s, sh = im.naturalHeight * s;
      cx.save(); cx.beginPath(); cx.rect(l, tp, w, h); cx.clip(); cx.drawImage(im, l + (w - sw) / 2, tp + (h - sh) / 2, sw, sh); cx.restore();
      cv.style.transform = q.transform || ''; cv.style.transformOrigin = q.origem || '50% 50%'; return true; },
  };
}

// ---------- 7 · duotone: o vídeo vira 2 cores da marca (sombra → escuro, luz → claro) por filtro SVG ----------
// duotone('dt1', '#1B1464', '#FFC23A', {contraste:1.15}); depois el.style.filter = 'url(#dt1)'  (pode somar: 'url(#dt1) contrast(1.1)')
// mistura(k) por quadro: duotone(...).quanto(k) → 0 = cor original, 1 = duotone pleno (troca na batida: k = naBatida(...).k)
function duotone(id, escuro, claro, o = {}) {
  const hex = (c) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16) / 255), [a, b] = [hex(escuro), hex(claro)];
  let sv = document.getElementById(id + '-svg');
  if (!sv) { sv = svgEl('svg', { id: id + '-svg', width: 0, height: 0, style: 'position:absolute' }, document.body); }
  sv.innerHTML = '';
  const f = svgEl('filter', { id, 'color-interpolation-filters': 'sRGB', x: 0, y: 0, width: '100%', height: '100%' }, sv);
  const c = o.contraste ?? 1.15, off = (1 - c) / 2;
  svgEl('feColorMatrix', { in: 'SourceGraphic', type: 'matrix', values: `.30 .59 .11 0 0  .30 .59 .11 0 0  .30 .59 .11 0 0  0 0 0 1 0`, result: 'cinza' }, f);
  const ct = svgEl('feComponentTransfer', { in: 'cinza', result: 'duo' }, f);
  ['R', 'G', 'B'].forEach((k, i) => svgEl('feFunc' + k, { type: 'table', tableValues: `${C(a[i] + off * 0).toFixed(3)} ${C(b[i]).toFixed(3)}` }, ct));
  svgEl('feComponentTransfer', { in: 'duo', result: 'duoC' }, f).append(...['R', 'G', 'B'].map((k) => svgEl('feFunc' + k, { type: 'linear', slope: c, intercept: off })));
  const mixC = svgEl('feComposite', { in: 'duoC', in2: 'SourceGraphic', operator: 'arithmetic', k1: 0, k2: 1, k3: 0, k4: 0 }, f);
  return { id, quanto(k) { mixC.setAttribute('k2', C(k).toFixed(3)); mixC.setAttribute('k3', (1 - C(k)).toFixed(3)); } };
}

// ---------- 8 · fisica: lê o fisica.json do simular_queda.mjs e posiciona os elementos (centro + rotação) ----------
// fisica(t, FISICA_DADOS['queda'], {p1: el, p2: el, ...}, {inicio}) → cada el (position:absolute; left/top 0; width/height = w/h do JSON)
//   aparece no t do corpo (antes disso, escondido); depois do último quadro fica parado na última posição.
function fisica(t, D, els, o = {}) {
  const i = Math.max(0, Math.min(D.n - 1, Math.round((t - (o.inicio ?? 0)) * D.fps)));
  for (const id in els) { const c = D.corpos[id], el = els[id]; if (!c || !el) continue;
    const [x, y, a] = c.q[i], vis = t - (o.inicio ?? 0) >= c.t;
    el.style.width = c.w + 'px'; el.style.height = c.h + 'px'; el.style.opacity = vis ? 1 : 0;
    el.style.transform = `translate(${(x - c.w / 2).toFixed(1)}px,${(y - c.h / 2).toFixed(1)}px) rotate(${a.toFixed(4)}rad)`; }
  return i;
}
