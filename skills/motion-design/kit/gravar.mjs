// Grava uma cena (página com window.frame(t) e window.DUR) quadro a quadro: Chrome do computador sem janela + ffmpeg.
// Uso: node gravar.mjs saida.mp4|saida.mov --html cena.html [--fps 30] [--blur 3] [--so 12.5] [--escala 2] [--crf 17]
// --dur: só imprime {dur, w, h} da cena e sai (usado pelo hf.mjs)
// --escala 2: mesma cena, o dobro de pixels (1920×1080 vira 3840×2160 nítido, para entrega em 4K)
// --so: só uma foto naquele segundo · --blur N: N subquadros por quadro misturados (desfoque de movimento) · o tamanho vem do #st da página
// Saída .mov = fundo transparente (HEVC com alfa, abre no CapCut/Final Cut/Premiere do Mac; a página deixa html/body/#st sem fundo) — para pôr por cima de outro vídeo
import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const arg = (n, d) => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : d; };
const saida = path.resolve(process.argv[2] && !process.argv[2].startsWith("--") ? process.argv[2] : "saida.mp4");
const fps = Number(arg("--fps", 30)), so = arg("--so", null), blur = Number(arg("--blur", 1));
const escala = Number(arg("--escala", 1)), crf = String(arg("--crf", 17));
// --prores: .mov transparente em ProRes 4444 (o ffmpeg lê o alfa e consegue sobrepor; o HEVC com alfa ele não lê)
const prores = process.argv.includes("--prores") || process.platform !== "darwin";   // alfa sem ProRes usa hevc_videotoolbox, que só existe no Mac
const alfa = saida.endsWith(".mov");
const html = path.resolve(arg("--html", "cena.html"));
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "cena-"));
const ch = spawn(CHROME, ["--headless=new", "--remote-debugging-port=0", `--user-data-dir=${dir}/perfil`, "--hide-scrollbars", "--window-size=1920,1920", "about:blank"], { stdio: "ignore" });
// porta 0: o Chrome escolhe uma livre e anota no DevToolsActivePort (com porta sorteada, dois gravadores ao mesmo tempo podiam cair no mesmo Chrome)
let alvo, porta;
for (let i = 0; i < 240 && !alvo; i++) { await new Promise((r) => setTimeout(r, 50)); try { porta ??= fs.readFileSync(`${dir}/perfil/DevToolsActivePort`, "utf8").split("\n")[0]; alvo = (await (await fetch(`http://127.0.0.1:${porta}/json`)).json()).find((t) => t.type === "page")?.webSocketDebuggerUrl; } catch {} }
const ws = new WebSocket(alvo); await new Promise((ok) => (ws.onopen = ok));
let id = 0; const esp = new Map(), erros = [];
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.method === "Runtime.exceptionThrown") erros.push(m.params.exceptionDetails.exception?.description); if (m.id && esp.has(m.id)) { esp.get(m.id)(m); esp.delete(m.id); } };
const cdp = (method, params = {}) => new Promise((ok) => { const i = ++id; esp.set(i, ok); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => (await cdp("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;
await cdp("Page.enable"); await cdp("Runtime.enable");
await cdp("Page.navigate", { url: "file://" + html });
// espera a página carregar de verdade (antes: 1,5 s fixos) e as fontes; só lendo a duração não precisa da folga de 0,8 s
for (let i = 0; i < 100 && !(await ev("location.protocol==='file:'&&document.readyState==='complete'")); i++) await new Promise((r) => setTimeout(r, 50));
const soDur = process.argv.includes("--dur");
await ev(`document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,${soDur ? 50 : 800})))`);
const W = await ev("document.getElementById('st').offsetWidth"), H = await ev("document.getElementById('st').offsetHeight");
if (soDur) { console.log(JSON.stringify({ dur: await ev("window.DUR"), w: W, h: H, erros })); ws.close(); ch.kill(); await new Promise((r) => setTimeout(r, 100)); try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} process.exit(0); }
await cdp("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: escala, mobile: false });
if (alfa) await cdp("Emulation.setDefaultBackgroundColorOverride", { color: { r: 0, g: 0, b: 0, a: 0 } });
const ext = alfa ? "png" : "jpg";
const foto = async (t, arq) => {
  await ev(`frame(${t}); new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))`);
  const r = await cdp("Page.captureScreenshot", { ...(alfa ? { format: "png" } : { format: "jpeg", quality: 95 }), clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
  fs.writeFileSync(arq, Buffer.from(r.result.data, "base64"));
};
if (so != null) { await foto(Number(so), saida.replace(/\.(mp4|mov)$/, "") + "." + ext); console.log("foto", so); }
else {
  const dur = await ev("window.DUR"), n = Math.round(dur * fps);
  fs.mkdirSync(`${dir}/q`);
  let k = 0;
  for (let i = 0; i < n; i++) { for (let b = 0; b < blur; b++) await foto(Math.max(0, (i + (b - (blur - 1) / 2) / (blur * 2)) / fps), `${dir}/q/${String(k++).padStart(6, "0")}.${ext}`); if (i % 60 === 0) process.stdout.write(`${i}/${n} `); }
  console.log("\ncodificando…");
  const r = spawnSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(fps * blur), "-i", `${dir}/q/%06d.${ext}`, ...(() => { // desfoque (blur) + MP4 em BT.709 faixa limitada (o padrão de vídeo; as fotos do Chrome são faixa completa BT.601)
    const vf = [blur > 1 ? `tmix=frames=${blur},select=eq(mod(n\\,${blur})\\,${blur - 1}),setpts=N/(${fps}*TB)` : null, alfa ? null : "scale=out_color_matrix=bt709:out_range=tv"].filter(Boolean);
    return [...(vf.length ? ["-vf", vf.join(",")] : []), ...(blur > 1 ? ["-r", String(fps)] : []), ...(alfa ? [] : ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"])]; })(), ...(alfa && prores ? ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-alpha_bits", "16", "-vendor", "apl0"] : alfa ? ["-c:v", "hevc_videotoolbox", "-allow_sw", "1", "-alpha_quality", "0.9", "-b:v", "24M", "-pix_fmt", "bgra", "-tag:v", "hvc1"] : ["-c:v", "libx264", "-preset", "slow", "-crf", crf, "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart"]), saida], { stdio: "inherit" });
  if (r.status !== 0) console.log("ffmpeg falhou");
}
console.log("erros:", JSON.stringify(erros));
ws.close(); ch.kill(); await new Promise((r) => setTimeout(r, 800)); try { fs.rmSync(dir, { recursive: true, force: true }); } catch {}
