// Fotos em alta resolução de uma página com window.frame(t) (ex.: uma réplica de sistema feita em HTML), para usar como "tela" em outra cena.
// Uso: node fotografar-cena.mjs pagina.html pasta-saida '[["nome",segundo,{"--var":"valor"}],...]' [x,y,w,h] [escala=2]
//   - cada item: nome do arquivo, segundo do frame(t) e (opcional) variáveis CSS para aplicar no <html> (trocar tema/cores)
//   - recorte x,y,w,h em px da página (padrão: a página toda)
import { spawn } from "node:child_process"; import fs from "node:fs"; import os from "node:os"; import path from "node:path";
const [html, saida, lista, recorte, esc] = process.argv.slice(2);
fs.mkdirSync(saida, { recursive: true });
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "foto-cena-"));
const ch = spawn(process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", ["--headless=new", "--remote-debugging-port=0", `--user-data-dir=${dir}/p`, "--hide-scrollbars", "--window-size=1920,1920", "about:blank"], { stdio: "ignore" });
let alvo, porta; for (let i = 0; i < 60 && !alvo; i++) { await new Promise((r) => setTimeout(r, 200)); try { porta ??= fs.readFileSync(`${dir}/p/DevToolsActivePort`, "utf8").split("\n")[0]; alvo = (await (await fetch(`http://127.0.0.1:${porta}/json`)).json()).find((t) => t.type === "page")?.webSocketDebuggerUrl; } catch {} }
const ws = new WebSocket(alvo); await new Promise((ok) => (ws.onopen = ok)); let id = 0; const esp = new Map();
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && esp.has(m.id)) { esp.get(m.id)(m); esp.delete(m.id); } };
const cdp = (method, params = {}) => new Promise((ok) => { const i = ++id; esp.set(i, ok); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (e) => (await cdp("Runtime.evaluate", { expression: e, awaitPromise: true, returnByValue: true })).result?.result?.value;
await cdp("Page.enable"); await cdp("Page.navigate", { url: "file://" + path.resolve(html) }); await new Promise((r) => setTimeout(r, 2500));
await ev("document.fonts.ready.then(()=>1)");
const W = await ev("(document.getElementById('st')||document.body).offsetWidth"), H = await ev("(document.getElementById('st')||document.body).offsetHeight");
await cdp("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: Number(esc || 2), mobile: false });
const [x, y, w, h] = recorte ? recorte.split(",").map(Number) : [0, 0, W, H];
for (const [nome, t, vars] of JSON.parse(lista)) {
  await ev(`(()=>{const r=document.documentElement;${vars ? `Object.entries(${JSON.stringify(vars)}).forEach(([k,v])=>r.style.setProperty(k,v));` : ""}window.frame&&frame(${t});return 1})()`);
  await new Promise((r) => setTimeout(r, 400));
  const r = await cdp("Page.captureScreenshot", { format: "jpeg", quality: 90, clip: { x, y, width: w, height: h, scale: 1 } });
  fs.writeFileSync(path.join(saida, nome + ".jpg"), Buffer.from(r.result.data, "base64")); console.log("foto", nome);
}
ws.close(); ch.kill();
