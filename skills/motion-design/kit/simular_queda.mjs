// Física 2D PRÉ-SIMULADA (matter.js 0.20, MIT): palavras/objetos caem, quicam e empilham. A cena só lê as posições por quadro.
// Regra do gravador: nada de física ao vivo (o HyperFrames pula quadros e grava em paralelo) — passo fixo + semente fixa = mesmo resultado sempre.
// uso: node simular_queda.mjs queda.json [-o fisica.json]
//   queda.json: { "largura":1080, "altura":1920, "fps":30, "dur":4, "semente":7, "gravidade":1.6, "subpassos":4,
//                 "chao":1640, "paredes":true, "quique":0.25, "atrito":0.6,
//                 "fonte":"900 150px Archivo",            ← opcional: mede "texto" no Chrome (letra precisa estar instalada/na página)
//                 "estaticos":[{"x":540,"y":1400,"w":600,"h":20,"ang":0}],   ← prateleiras, rampa
//                 "corpos":[{"id":"p1","texto":"PÃO","w":420,"h":150,"x":520,"y":-200,"ang":0.08,"t":0.0,"quique":0.3,"forma":"caixa|circulo"}] }
//   x/ang ausentes = sorteados com a semente; t = quando o corpo entra no mundo (use MUSICA.batidas[i] para cair na batida).
// Saída: { fps, n, dur, largura, altura, corpos: { id: { w, h, t, texto, q: [[x, y, ang], ...] } } } (centro do corpo, px do palco; ang em rad)
//   + fisica.js (window.FISICA_DADOS = ...). Na cena: mistura.js → fisica(t, FISICA_DADOS, elementos).
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createRequire } from "node:module";

const req = createRequire(import.meta.url);
const tentar = [process.env.NODE_PATH, path.join(os.homedir(), "motion-studio/.ferramentas/node_modules")].filter(Boolean);
let Matter;
for (const p of [null, ...tentar]) { try { Matter = p ? req(path.join(p, "matter-js")) : req("matter-js"); break; } catch {} }
if (!Matter) { console.error("matter-js não encontrado (instale em ~/motion-studio/.ferramentas: npm i matter-js@0.20.0)"); process.exit(1); }

const arq = process.argv[2];
if (!arq) { console.error("uso: node simular_queda.mjs queda.json [-o fisica.json]"); process.exit(1); }
const io = process.argv.indexOf("-o");
const saida = io > 0 ? process.argv[io + 1] : arq.replace(/\.json$/, "") + ".fisica.json";
const C = JSON.parse(fs.readFileSync(arq, "utf8"));
const W = C.largura ?? 1080, H = C.altura ?? 1920, FPS = C.fps ?? 30, DUR = C.dur ?? 4, SUB = C.subpassos ?? 4;

// semente: mulberry32 (o Common.random do matter também é trocado, para ids e desempates)
let s = (C.semente ?? 7) >>> 0;
const rnd = () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
Matter.Common.random = (a = 0, b = 1) => a + rnd() * (b - a);

// medir textos sem w/h no Chrome do sistema (opcional)
const semMedida = C.corpos.filter((c) => c.texto && (c.w == null || c.h == null));
if (semMedida.length) {
  if (!C.fonte) { console.error('corpos com "texto" e sem w/h precisam de "fonte" (ex.: "900 150px Archivo")'); process.exit(1); }
  let pw; for (const p of [null, ...tentar]) { try { pw = p ? req(path.join(p, "playwright-core")) : req("playwright-core"); break; } catch {} }
  const chrome = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome"].find((x) => fs.existsSync(x));
  const nav = await pw.chromium.launch({ executablePath: chrome, headless: true });
  const pg = await nav.newPage();
  const fam = (C.fonte.match(/\d+px\s+(.+)$/) || [])[1]?.replace(/['"]/g, "");
  await pg.setContent(`<link href="https://fonts.googleapis.com/css2?family=${encodeURIComponent(fam || "Archivo")}:wght@400;700;900&display=block" rel="stylesheet"><body>`);
  await pg.waitForTimeout(400);
  const med = await pg.evaluate(async ([f, ts]) => { await document.fonts.load(f); const cv = document.createElement("canvas").getContext("2d"); cv.font = f;
    return ts.map((t) => { const m = cv.measureText(t); return [Math.ceil(m.actualBoundingBoxLeft + m.actualBoundingBoxRight), Math.ceil(m.actualBoundingBoxAscent + m.actualBoundingBoxDescent)]; }); },
    [C.fonte, semMedida.map((c) => c.texto)]);
  await nav.close();
  semMedida.forEach((c, i) => { c.w ??= med[i][0] + 24; c.h ??= med[i][1] + 16; });
}

const { Engine, Bodies, Composite, Body } = Matter;
const eng = Engine.create({ gravity: { x: 0, y: C.gravidade ?? 1.6 } });
eng.positionIterations = 10; eng.velocityIterations = 8;
const est = [];
if ((C.chao ?? H) < 1e6) est.push(Bodies.rectangle(W / 2, (C.chao ?? H - 120) + 200, W * 3, 400, { isStatic: true }));
if (C.paredes !== false) est.push(Bodies.rectangle(-200, H / 2, 400, H * 4, { isStatic: true }), Bodies.rectangle(W + 200, H / 2, 400, H * 4, { isStatic: true }));
for (const e of C.estaticos || []) est.push(Bodies.rectangle(e.x, e.y, e.w, e.h, { isStatic: true, angle: e.ang || 0 }));
Composite.add(eng.world, est);

const corpos = C.corpos.map((c, i) => {
  const x = c.x ?? W * (.25 + .5 * rnd()), y = c.y ?? -c.h - 40 * i, ang = c.ang ?? (rnd() - .5) * .5;
  const op = { restitution: c.quique ?? C.quique ?? .25, friction: c.atrito ?? C.atrito ?? .6, frictionAir: c.ar ?? .012, angle: ang, density: c.densidade ?? .002, chamfer: c.forma === "circulo" ? undefined : { radius: Math.min(c.w, c.h) * .08 } };
  const b = c.forma === "circulo" ? Bodies.circle(x, y, c.w / 2, op) : Bodies.rectangle(x, y, c.w, c.h, op);
  if (c.vx || c.vy) Body.setVelocity(b, { x: c.vx || 0, y: c.vy || 0 });
  if (c.giro) Body.setAngularVelocity(b, c.giro);
  return { c, b, x, y, ang, dentro: false, q: [] };
});

const n = Math.round(DUR * FPS), dt = 1000 / FPS / SUB;
for (let f = 0; f < n; f++) {
  const t = f / FPS;
  for (const k of corpos) if (!k.dentro && t >= (k.c.t ?? 0)) { Composite.add(eng.world, k.b); k.dentro = true; }
  for (const k of corpos) k.q.push(k.dentro ? [+k.b.position.x.toFixed(1), +k.b.position.y.toFixed(1), +k.b.angle.toFixed(4)] : [+k.x.toFixed(1), +k.y.toFixed(1), +k.ang.toFixed(4)]);
  for (let i = 0; i < SUB; i++) Engine.update(eng, dt);
}
const R = { fps: FPS, n, dur: DUR, largura: W, altura: H, semente: C.semente ?? 7, corpos: {} };
for (const k of corpos) R.corpos[k.c.id] = { w: k.c.w, h: k.c.h, t: k.c.t ?? 0, texto: k.c.texto, forma: k.c.forma || "caixa", q: k.q };
fs.writeFileSync(saida, JSON.stringify(R));
const nome = path.basename(saida).replace(/\.(fisica\.)?json$/, "");
fs.writeFileSync(saida.replace(/\.json$/, "") + ".js", `window.FISICA_DADOS=window.FISICA_DADOS||{};window.FISICA_DADOS[${JSON.stringify(nome)}]=${JSON.stringify(R)};\n`);
const parados = corpos.filter((k) => { const a = k.q[n - 1], b = k.q[n - 2]; return Math.hypot(a[0] - b[0], a[1] - b[1]) < .5; }).length;
console.log(`${corpos.length} corpos · ${n} quadros a ${FPS} fps · ${parados}/${corpos.length} parados no fim → ${saida} (+ .js, chave "${nome}")`);
