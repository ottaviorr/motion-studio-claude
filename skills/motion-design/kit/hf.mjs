// Renderiza uma cena do estúdio (página com window.frame(t) e window.DUR) pelo HyperFrames (HeyGen, Apache-2.0).
// Mesma imagem do gravar.mjs (SSIM 0,996 medido), 2–3,4× mais rápido: vários Chromes em paralelo + captura do HyperFrames.
// Uso: node hf.mjs saida.mp4|saida.mov --html cena.html [--fps 30] [--escala 1] [--taxa 40M] [--x264 --crf 16] [--previa] [--workers N]
// PADRÃO DO DONO: 1920×1080 (ou 1080×1920) a 30 fps, taxa de bits alta. --fps 60 / --escala 2 (4K) só se o pedido disser.
//   .mp4 sai pelo codificador de vídeo do Mac (h264_videotoolbox, --gpu do HyperFrames) a 40 Mb/s: encode 8,4 s → 1,8 s numa cena de 10 s,
//   SSIM 0,994 contra referência quase sem perda (x264 CRF 16 dá 0,993 com 15 Mb/s). --x264: volta para o x264 por CRF (CPU).
//   --previa: prévia rápida para o dono olhar (qualidade draft, 12 Mb/s). Nunca entregue a prévia.
//   Fontes do Google viram fontes locais embutidas (kit/fontes-locais.mjs, cache em ~/.cache/motion-studio-fontes): sem rede no render.
//   .mov = transparente (ProRes 4444). O HyperFrames não faz 4K com alfa: com .mov a escala volta para 1 (use gravar.mjs --prores --escala 2 se precisar de alfa em 4K).
//   Desfoque de movimento: o HyperFrames ainda não tem na linha de comando → para cena com movimento muito rápido, gravar.mjs --blur 3.
// Precisa do hyperframes instalado (no Motion Studio: .ferramentas, versão fixa) e do Chrome do sistema (só para ler a duração).
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath, pathToFileURL } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
// fontes locais: ao lado (kit) ou na skill (cópia do hf.mjs dentro de projetos/*/base); sem nenhum dos dois, segue com o link do Google
let localizarFontes = async (s) => s;
for (const p of [path.join(aqui, "fontes-locais.mjs"), path.join(os.homedir(), ".claude/skills/motion-design/kit/fontes-locais.mjs")])
  if (fs.existsSync(p)) { ({ localizarFontes } = await import(pathToFileURL(p).href)); break; }
const arg = (n, d) => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : d; };
const saida = path.resolve(process.argv[2] && !process.argv[2].startsWith("--") ? process.argv[2] : "saida.mp4");
const html = path.resolve(arg("--html", "cena.html"));
const fps = arg("--fps", "30"), crf = arg("--crf", "16");
const previa = process.argv.includes("--previa"), x264 = process.argv.includes("--x264") || process.argv.includes("--crf") || process.platform !== "darwin";
const taxa = arg("--taxa", previa ? "12M" : "40M");
// workers fixos pulam a calibração automática do HyperFrames (~1,4 s por cena). 8 era o mais rápido num M4 de 10 núcleos,
// mas travava o MacBook Air (sem ventoinha, 16 GB) com agentes em paralelo → padrão 4 (a imagem sai IDÊNTICA, só ~1,5× mais lento).
// Mais rápido quando a máquina estiver livre: --workers 8 ou HF_WORKERS=8.
const workers = arg("--workers", process.env.HF_WORKERS || String(Math.max(2, Math.min(4, os.cpus().length - 2))));
const alfa = saida.endsWith(".mov");
let escala = Number(arg("--escala", 1));
if (alfa && escala !== 1) { console.log("aviso: HyperFrames não faz 4K com transparência — saindo em escala 1"); escala = 1; }

// fila global: uma gravação por vez no computador inteiro (vários agentes em paralelo gravando juntos travavam a máquina)
const FILA = path.join(os.homedir(), ".cache", "motion-studio-fila-render");
fs.mkdirSync(path.dirname(FILA), { recursive: true });
for (let espera = 0; ; espera++) {
  try { fs.mkdirSync(FILA); break; } catch {
    try { if (Date.now() - fs.statSync(FILA).mtimeMs > 45 * 60e3) fs.rmSync(FILA, { recursive: true, force: true }); } catch {}   // trava esquecida (> 45 min)
    if (espera % 30 === 0) console.log("aguardando a vez na fila de render…");
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 2000);   // espera sem abrir processo (vale no Windows também)
  }
}
const solta = () => { try { fs.rmSync(FILA, { recursive: true, force: true }); } catch {} };
process.on("exit", solta); process.on("SIGINT", () => { solta(); process.exit(130); });
const tIni = Date.now();
// 0. Windows com 2 GPUs: garante que o Chrome do render usa a dedicada (no Mac não faz nada)
if (process.platform === "win32") spawnSync(process.execPath, [path.join(aqui, "gpu-windows.mjs")], { stdio: "inherit" });
// 1. cópia temporária ao lado da cena (nome único: duas gravações da mesma cena não apagam o temporário uma da outra), com as fontes locais
const pasta = path.dirname(html), nome = path.basename(html, ".html");
const comp = path.join(pasta, `.hf-${nome}-${process.pid}.html`);
process.on("exit", () => { try { fs.rmSync(comp, { force: true }); } catch {} });
let src = fs.readFileSync(html, "utf8");
if (!/id="st"/.test(src)) { console.error('a cena precisa de <div id="st">'); process.exit(1); }
src = await localizarFontes(src);
fs.writeFileSync(comp, src);
// 2. duração e tamanho da cena (o gravar.mjs abre a página e lê window.DUR) — já com as fontes locais: 3,4 s → 1,4 s
const nodePath = process.env.NODE_PATH || "";
const info = spawnSync("node", [path.join(aqui, "gravar.mjs"), "x.mp4", "--html", comp, "--dur"], { encoding: "utf8", env: { ...process.env, NODE_PATH: nodePath } });
const m = (info.stdout || "").match(/\{.*\}/);
if (!m) { console.error("não consegui ler a duração da cena:\n" + info.stdout + info.stderr); process.exit(1); }
const { dur, w, h, erros } = JSON.parse(m[0]);
if (erros?.length) console.log("erros na página:", erros);

// 3. composição: #st vira a composição, e uma "timeline" mínima repassa o tempo para frame(t)
// só depois do <body>: o modelo-cena cita <div id="st"> num comentário do CSS (era a causa do HF_DE_COMPOSITION_ROOT_MISSING — achado de um colaborador)
src = src.replace(/(<body[^>]*>[\s\S]*?)id="st"/i, `$1id="st" data-composition-id="main" data-start="0" data-duration="${dur}" data-width="${w}" data-height="${h}"`);
const ponte = `<script>(function(){let tt=0;const D=${dur};const tl={
seek(t){tt=+t||0;if(window.frame)window.frame(tt);return tl;},time(t){return t===undefined?tt:tl.seek(t);},totalTime(t){return tl.time(t);},
progress(p){return p===undefined?tt/D:tl.seek(p*D);},duration(){return D;},totalDuration(){return D;},pause(){return tl;},play(){return tl;},
paused(){return true;},isActive(){return false;},timeScale(){return 1;},getChildren(){return [];},eventCallback(){return tl;},kill(){},
invalidate(){return tl;},render(t){return tl.seek(t);}};window.__timelines=window.__timelines||{};window.__timelines.main=tl;})();</script>`;
src = src.replace(/<\/body>/i, ponte + "</body>");
fs.writeFileSync(comp, src);

// 4. render — chama o .mjs pelo node (o .bin/hyperframes é script de shell e não roda no Windows)
const bin = [path.resolve(nodePath, "hyperframes/bin/hyperframes.mjs"), path.resolve(aqui, "../../../.ferramentas/node_modules/hyperframes/bin/hyperframes.mjs"), path.resolve(aqui, "../../../../motion-studio/.ferramentas/node_modules/hyperframes/bin/hyperframes.mjs")].find((b) => fs.existsSync(b));
const cmd = bin ? [process.execPath, bin] : ["npx", "-y", "hyperframes@0.8.140"];
const cod = alfa ? [] : x264 ? ["--crf", crf] : ["--gpu", "--video-bitrate", taxa];
const a = ["render", pasta, "-c", path.basename(comp), "--fps", fps, "--quality", previa ? "draft" : "high", ...cod, "--workers", workers, "--output", saida,
  ...(process.env.HF_VERBOSE ? [] : ["--quiet"]), ...(alfa ? ["--format", "mov"] : []),
  ...(process.env.HF_SEM_CAPTURA_RAPIDA ? ["--experimental-fast-capture=false"] : []),   // a captura rápida desliga sozinha em cena com 3D CSS (perspective/preserve-3d)
  ...(escala === 2 ? ["--resolution", w >= h ? "landscape-4k" : "portrait-4k"] : [])];
const t0 = Date.now();
// prioridade baixa (nice 10): o render usa o processador que sobra e o computador continua respondendo — mesmo resultado quadro a quadro
const leve = process.platform !== "win32" && !process.env.HF_SEM_NICE;
const r = spawnSync(leve ? "nice" : cmd[0], leve ? ["-n", "10", ...cmd, ...a] : [...cmd.slice(1), ...a], { stdio: "inherit", env: { ...process.env, HYPERFRAMES_SKIP_SKILLS: "1" } });
fs.rmSync(comp, { force: true });
if (r.status !== 0) { console.error("HyperFrames falhou"); process.exit(r.status || 1); }
console.log(`pronto: ${saida} (${dur}s de cena em ${((Date.now() - t0) / 1000).toFixed(1)}s de render, ${((Date.now() - tIni) / 1000).toFixed(1)}s no total)`);
