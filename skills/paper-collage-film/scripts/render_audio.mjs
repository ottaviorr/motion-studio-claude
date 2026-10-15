// usage: node render_audio.mjs <score.html[?preset=pulse&bpm=128&dur=15&drop=2&vac=10.5&lift=11&end=13]> <out.wav>
// Renders an OfflineAudioContext page in headless Chrome/Brave and saves window.__wav (16-bit, 48 kHz, normalised to -1 dBFS).
import { spawn } from 'node:child_process'; import { existsSync, writeFileSync } from 'node:fs'; import { resolve } from 'node:path';
const B = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'].find(existsSync);
const [pageArg, outWav] = process.argv.slice(2); const [page, query] = pageArg.split('?'); const PORT = 9900 + Math.floor(Math.random() * 90);
const proc = spawn(B, ['--headless=new', '--no-first-run', '--disable-extensions', '--autoplay-policy=no-user-gesture-required', `--remote-debugging-port=${PORT}`, `--user-data-dir=/tmp/brave-aud-${PORT}-${Date.now()}`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms)); let ws;
for (let i = 0; i < 80 && !ws; i++) { try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); const u = l.find((t) => t.type === 'page')?.webSocketDebuggerUrl; if (u) ws = new WebSocket(u); } catch {} if (!ws) await sleep(250); }
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
let id = 0; const pend = new Map(); let pageErr = ''; ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } else if (m.method === 'Runtime.exceptionThrown') pageErr = JSON.stringify(m.params.exceptionDetails).slice(0, 600); });
const send = (method, params = {}) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
await send('Runtime.enable');
const ev = async (x) => (await send('Runtime.evaluate', { expression: x, returnByValue: true, awaitPromise: true })).result?.result?.value;
await send('Page.navigate', { url: 'file://' + resolve(page) + (query ? '?' + query : '') });
const t0 = Date.now(); let st;
while (true) { await sleep(300); if (pageErr) { st = 'PAGE ERROR: ' + pageErr; break; } st = await ev('window.__err ? "ERR:"+window.__err : (window.__done ? "done" : "")'); if (st) break; if (Date.now() - t0 > 240000) { st = 'timeout'; break; } }
if (st !== 'done') { console.error(st); proc.kill(); process.exit(1); }
const len = await ev('window.__wav.length'); const size = 1 << 20; const parts = [];
for (let i = 0; i * size < len; i++) parts.push(Buffer.from(await ev(`window.__chunk(${i},${size})`), 'base64'));
writeFileSync(outWav, Buffer.concat(parts)); console.log(`wrote ${outWav} ${len} bytes, raw peak ${await ev('window.__peak')}, ${((Date.now() - t0) / 1000).toFixed(1)}s`);
ws.close(); proc.kill(); process.exit(0);
