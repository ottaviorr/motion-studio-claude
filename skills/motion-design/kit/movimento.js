// motion-design · movimento de animador (estudo 3, 16/10/2026: Ben Marriott, Ordinary Folk, Daniel Schiffer).
// Carregue DEPOIS do comum.js (usa C, p, eo, eio). Tudo é função pura de t: nada de Math.random sem semente.
// Regra-mãe: título NUNCA pisca. Toda troca de título/cena tem um movimento-guia e acontece no quadro
// mais rápido desse movimento (troca), ou é um corte honesto na batida. Fade A→B só em momento lento e emocional.

// ---------- curvas de verdade (cubic-bezier igual ao CSS, resolvido por Newton) ----------
function bz(x1, y1, x2, y2) {
  const A = (a, b) => 1 - 3 * b + 3 * a, B = (a, b) => 3 * b - 6 * a, Cc = (a) => 3 * a;
  const f = (t, a, b) => ((A(a, b) * t + B(a, b)) * t + Cc(a)) * t, d = (t, a, b) => 3 * A(a, b) * t * t + 2 * B(a, b) * t + Cc(a);
  return (x) => { x = C(x); let t = x; for (let i = 0; i < 8; i++) { const e = f(t, x1, x2) - x, s = d(t, x1, x2); if (Math.abs(s) < 1e-6) break; t -= e / s; } return f(C(t), y1, y2); };
}
// as 3 curvas da casa — use UMA curva-mestra por frase/cena e copie para todos os elementos dela
const sai = bz(0, .9, .25, 1);      // impacto: parte rápido, chega macio (entradas, carimbo, câmera)
const chega = bz(.6, 0, 1, .4);     // acelera até o corte (o que está SAINDO de cena)
const parte = bz(0, .6, .4, 1);     // sai do corte já em movimento (o que ENTRA depois do corte)
const forte = bz(.7, 0, .3, 1);     // in-out forte: o pico de velocidade fica no meio (para troca)

// ---------- antecipação: recua antes de disparar (devolve 0 → −r → 1; multiplique pela distância) ----------
function antes(t, a, d, r = .12, ra = .4) { return t < a ? -r * eio(p(t, a - d * ra, a)) : -r + (1 + r) * sai(p(t, a, a + d)); }

// ---------- troca no pico: A some e B aparece no MESMO quadro, no meio de um movimento forte ----------
// devolve {k (0→1 com curva forte), v (velocidade 0→1→0), fase: 0 = mostra A, 1 = mostra B}
// uso: const T=troca(t,2.0,.5); grupo.style.transform=`rotate(${T.k*180}deg) scale(${1-.15*T.v})`; A.style.opacity=1-T.fase; B.style.opacity=T.fase;
function troca(t, a, d = .5, curva = forte) { const k = curva(p(t, a, a + d)); return { k, v: Math.sin(Math.PI * k), fase: k < .5 ? 0 : 1 }; }

// ---------- match cut de escala (≤ 5%) atravessando o corte em tc ----------
function antesDoCorte(t, tc, amp = .05, d = .33) { return 1 + amp * chega(p(t, tc - d, tc)); }   // cena A
function depoisDoCorte(t, tc, amp = .05, d = .4) { return 1 + amp * (1 - parte(p(t, tc, tc + d))); } // cena B começa ampliada e assenta

// ---------- impacto: anel que sai do objeto e cena que reage ----------
// anel: elemento com border; vai de 1× a ~2,2× em 20 quadros, some com eo. Dois anéis: o 2º com atraso de 0,1 s.
function anel(el, t, tb, s1 = 2.2, d = .67) { const q = p(t, tb, tb + d); el.style.transform = `translate(-50%,-50%) scale(${(1 + (s1 - 1) * sai(q)).toFixed(4)})`; el.style.opacity = t < tb ? 0 : (1 - eo(q)).toFixed(3); }
// quique amortecido depois do impacto (objetos secundários): deslocamento em unidades (multiplique)
function reage(t, tb, f = 18, amort = 6) { const dt = t - tb; return dt < 0 ? 0 : Math.exp(-amort * dt) * Math.sin(f * dt); }
// tremor que cresce antes do impacto e para seco no quadro do carimbo (tensão)
function tensao(t, tb, amp = 12, d = .5) { const k = p(t, tb - d, tb); return t >= tb ? [0, 0] : [amp * k * vn(t * 30, 3), amp * k * vn(t * 30, 9)]; }

// ---------- ruído com semente (determinístico) e gate weave de película ----------
const hs = (n) => { const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); };
const vn = (t, s = 0) => { const i = Math.floor(t), f = t - i, u = f * f * (3 - 2 * f); return (hs(i + s) * (1 - u) + hs(i + 1 + s) * u) * 2 - 1; };
// weave: a 12 Hz, até 3 px no 1080×1920, com escala 101% para não mostrar borda
function weave(t, amp = 3, hz = 12, s = 1) { return `translate(${(amp * vn(t * hz, s)).toFixed(2)}px,${(amp * vn(t * hz, s + 6)).toFixed(2)}px) scale(1.01)`; }

// ---------- 12 fps para a camada "feita à mão" (rabisco, seta, marca-texto, carimbo); vídeo e título ficam a 30 ----------
const tq = (t, fps = 12) => Math.floor(t * fps) / fps;

// ---------- morph de texto sem piscar ("goo": borra, cruza e endurece o alfa) ----------
// gooFiltro(id) cria o <filter> no documento; goo(id,t,a,d) anima. Palavras de tamanho parecido; d = 0,6–1,0 s em reel.
// Por baixo, cruze a opacidade das duas palavras com p(t,a+d*.35,a+d*.65).
function gooFiltro(id = 'goo') {
  if (document.getElementById(id)) return;
  const ns = 'http://www.w3.org/2000/svg', svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('width', 0); svg.setAttribute('height', 0); svg.style.position = 'absolute';
  svg.innerHTML = `<filter id="${id}" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence id="${id}-tb" type="fractalNoise" baseFrequency=".02" numOctaves="2" seed="1"/>`
    + `<feDisplacementMap id="${id}-dm" in="SourceGraphic" scale="0"/><feGaussianBlur id="${id}-gb" stdDeviation="0"/>`
    + `<feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 20 -8"/></filter>`;
  document.body.appendChild(svg);
}
function goo(id, t, a, d = .8) {
  const k = p(t, a, a + d), s = Math.sin(Math.PI * k);
  document.getElementById(id + '-gb').setAttribute('stdDeviation', (14 * s).toFixed(2));
  document.getElementById(id + '-dm').setAttribute('scale', (25 * s).toFixed(2));
  document.getElementById(id + '-tb').setAttribute('seed', Math.floor(t * 12));
  return k;
}

// ---------- wipe curto direcional (2–3 quadros) quando a palavra tem direção ("cai", "sobe") ----------
function wipeCurto(el, t, a, dir = 'baixo', d = .09) {
  const k = p(t, a, a + d) * 100;
  el.style.clipPath = { baixo: `inset(0 0 ${100 - k}% 0)`, cima: `inset(${100 - k}% 0 0 0)`, dir: `inset(0 ${100 - k}% 0 0)`, esq: `inset(0 0 0 ${100 - k}%)` }[dir];
}

// ---------- zoom-through: a troca de título padrão (cut-the-curve, HyperFrames) ----------
// A sai: escala 1→1,2 + desfoque 0→10 px em 0,2 s (power3.in), opacidade 1→0,15 LINEAR separada; corte num quadro em tc;
// B entra: 0,75→1 + desfoque 10→0 em 0,5 s (expo.out). Os dois nunca juntos. Desfoque no invólucro, nunca nos filhos.
const p3in = (x) => Math.pow(C(x), 3), expoOut = (x) => (x = C(x), x >= 1 ? 1 : 1 - Math.pow(2, -10 * x));
function zoomThrough(A, B, t, tc, saida = .2, entrada = .5) {
  if (t < tc) {
    const k = p(t, tc - saida, tc), e = p3in(k);
    A.style.transform = `scale(${(1 + .2 * e).toFixed(4)})`; A.style.filter = `blur(${(10 * e).toFixed(2)}px)`; A.style.opacity = (1 - .85 * k).toFixed(3);
    B.style.opacity = 0;
  } else {
    const e = expoOut(p(t, tc, tc + entrada));
    A.style.opacity = 0;
    B.style.transform = `scale(${(.75 + .25 * e).toFixed(4)})`; B.style.filter = `blur(${(10 * (1 - e)).toFixed(2)}px)`; B.style.opacity = 1;
  }
}
// escala grande (câmera que empurra, zoom longo) interpolada em log: parece constante, não freia no fim
const escalaLog = (a, b, k) => a * Math.pow(b / a, C(k));
