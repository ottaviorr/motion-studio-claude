// Fotos de telas REAIS (app local, login de sistema, site público) em 2x, seguindo um arquivo de passos.
// Abre o Chrome sem janela em 1600x900 (escala 2 → fotos 3200x1800) com porta livre (pode rodar vários em paralelo).
// Uso: node fotos-telas.mjs passos.mjs pasta-saida   · modelo de passos: reference/passos-exemplo.mjs
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
const [passosArq, saida] = process.argv.slice(2);
fs.mkdirSync(saida, { recursive: true });
const dir = fs.mkdtempSync(path.join(os.tmpdir(), "painel-"));
const ch = spawn(process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", ["--headless=new", "--remote-debugging-port=0", `--user-data-dir=${dir}/p`, "--hide-scrollbars", "--window-size=1600,900", "about:blank"], { stdio: "ignore" });
let alvo, porta;
for (let i = 0; i < 60 && !alvo; i++) { await new Promise((r) => setTimeout(r, 200)); try { porta ??= fs.readFileSync(`${dir}/p/DevToolsActivePort`, "utf8").split("\n")[0]; alvo = (await (await fetch(`http://127.0.0.1:${porta}/json`)).json()).find((t) => t.type === "page")?.webSocketDebuggerUrl; } catch {} }
const ws = new WebSocket(alvo); await new Promise((ok) => (ws.onopen = ok));
let id = 0; const esp = new Map(), erros = [];
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.method === "Runtime.exceptionThrown") erros.push(m.params.exceptionDetails.exception?.description); if (m.id && esp.has(m.id)) { esp.get(m.id)(m); esp.delete(m.id); } };
const cdp = (method, params = {}) => new Promise((ok) => { const i = ++id; esp.set(i, ok); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await cdp("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true }); return r.result?.result?.value ?? r.result?.exceptionDetails?.exception?.description; };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
await cdp("Page.enable"); await cdp("Runtime.enable");
await cdp("Emulation.setDeviceMetricsOverride", { width: 1600, height: 900, deviceScaleFactor: 2, mobile: false });
const go = async (url) => { await cdp("Page.navigate", { url }); await wait(1800); };
const shot = async (nome, clip) => { const r = await cdp("Page.captureScreenshot", { format: "png", ...(clip ? { clip: { ...clip, scale: 1 } } : {}) }); fs.writeFileSync(path.join(saida, nome + ".png"), Buffer.from(r.result.data, "base64")); console.log("foto", nome); };
const passos = (await import(path.resolve(passosArq))).default;
await passos({ go, ev, shot, wait, cdp });
console.log("erros:", JSON.stringify(erros));
ws.close(); ch.kill();
