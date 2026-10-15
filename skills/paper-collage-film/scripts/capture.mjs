// Deterministic frame capture of a code-based motion composition (DOM/CSS/SVG/Canvas/WebGL) via headless Chrome/Brave (HFT_BROWSER overrides) + CDP.
// The page MUST expose:
//   window.__comp = { width, height, fps, duration }      (seconds)
//   window.__seek = async (t) => { ...render the frame at time t...; }   (pure function of t)
// usage:
//   node capture.mjs <page.html[?query]> <out_dir> [--query "style=luxury-serif&scheme=light"] [--stills 0.5,1.2,...] [--from s] [--to s] [--every n] [--jpg]
// (system/proof copy of motion/tools/capture.mjs: adds query-string support so one page renders any style)
// Frames are written as out_dir/f_00000.png (or stills as out_dir/still_<t>.png).
import { spawn } from 'node:child_process';
import { existsSync as __exists } from 'node:fs';
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const BRAVE = process.env.HFT_BROWSER || [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
].find((p) => __exists(p));
if (!BRAVE) { console.error('No Chromium-based browser found. Set HFT_BROWSER=/path/to/chrome'); process.exit(1); }
const args = process.argv.slice(2);
const [pagePath, inlineQuery] = args[0].split('?');
const page = resolve(pagePath);
const outDir = resolve(args[1]);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const stills = opt('--stills', null);
const from = parseFloat(opt('--from', '0'));
const toArg = opt('--to', null);
const every = parseInt(opt('--every', '1'));
const jpg = args.includes('--jpg');
const query = opt('--query', inlineQuery || '');
mkdirSync(outDir, { recursive: true });

const PORT = 9400 + (process.pid % 2500); // per-process port: parallel workers never collide
const proc = spawn(BRAVE, [
  '--headless=new', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
  '--use-mock-keychain', '--password-store=basic', '--disable-extensions', '--disable-component-update',
  '--force-color-profile=srgb', '--ignore-gpu-blocklist', '--enable-webgl', '--use-angle=metal',
  '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required', '--allow-file-access-from-files',
  `--remote-debugging-port=${PORT}`, `--user-data-dir=/tmp/lf-cap-${process.pid}`, 'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let wsUrl;
for (let i = 0; i < 160 && !wsUrl; i++) {
  try { const l = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); wsUrl = l.find((t) => t.type === 'page')?.webSocketDebuggerUrl; } catch {}
  if (!wsUrl) await sleep(250);
}
if (!wsUrl) { console.error('browser did not start'); proc.kill(); process.exit(1); }
const ws = new WebSocket(wsUrl);
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
let id = 0; const pending = new Map(); const listeners = [];
ws.addEventListener('message', (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } else listeners.forEach((l) => l(m)); });
const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (expr) => {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails).slice(0, 800));
  return r.result?.result?.value;
};
const consoleMsgs = [];
listeners.push((m) => { if (m.method === 'Runtime.consoleAPICalled') consoleMsgs.push(m.params.args.map((a) => a.value).join(' ')); if (m.method === 'Runtime.exceptionThrown') consoleMsgs.push('EXC ' + JSON.stringify(m.params.exceptionDetails).slice(0, 400)); });

await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
const loaded = new Promise((r) => { const t = setTimeout(r, 20000); listeners.push((m) => { if (m.method === 'Page.loadEventFired') { clearTimeout(t); r(); } }); });
await send('Page.navigate', { url: 'file://' + page + (query ? '?' + query.replace(/^\?/, '') : '') });
await loaded;
// wait for the composition to declare itself
let comp = null;
for (let i = 0; i < 120 && !comp; i++) { comp = await evaluate('window.__comp && window.__seek ? window.__comp : null').catch(() => null); if (!comp) await sleep(250); }
if (!comp) { console.error('page did not expose __comp/__seek. console:', consoleMsgs.slice(-10)); ws.close(); proc.kill(); process.exit(1); }
await send('Emulation.setDeviceMetricsOverride', { width: comp.width, height: comp.height, deviceScaleFactor: 1, mobile: false });
console.log('comp:', JSON.stringify(comp));
await evaluate('document.fonts.ready.then(()=>true)');
if (window_ready_wait()) await evaluate('window.__ready ? window.__ready : true');

function window_ready_wait() { return true; }

async function shot(t, file) {
  await evaluate(`(async()=>{await window.__seek(${t}); await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))); return true})()`);
  const s = await send('Page.captureScreenshot', { format: jpg ? 'jpeg' : 'png', quality: jpg ? 95 : undefined, clip: { x: 0, y: 0, width: comp.width, height: comp.height, scale: 1 }, captureBeyondViewport: false });
  writeFileSync(file, Buffer.from(s.result.data, 'base64'));
}

const t0 = Date.now();
if (stills) {
  for (const t of stills.split(',').map(Number)) { await shot(t, `${outDir}/still_${t.toFixed(2)}.png`); }
  console.log(`stills: ${stills} -> ${outDir}`);
} else {
  const fps = comp.fps, dur = toArg ? parseFloat(toArg) : comp.duration;
  const n0 = Math.round(from * fps), n1 = Math.round(dur * fps);
  for (let n = n0; n < n1; n += every) {
    await shot(n / fps, `${outDir}/f_${String(n).padStart(5, '0')}.${jpg ? 'jpg' : 'png'}`);
    if (n % (fps * 2) === 0) console.log(`frame ${n}/${n1} (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  }
  console.log(`done ${n1 - n0} frames @${fps}fps -> ${outDir}`);
}
if (consoleMsgs.length) console.log('console:', consoleMsgs.slice(-8).join(' | '));
ws.close(); proc.kill(); process.exit(0);
