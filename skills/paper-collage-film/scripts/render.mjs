// Render HTML files to PNG via headless Chrome/Brave (HFT_BROWSER overrides) + Chrome DevTools Protocol (no npm deps).
// usage: node render.mjs <out_dir> <file1.html> [file2.html ...]
// Frame size is read from <meta name="frame" content="1920x1080"> (default 1920x1080).
import { spawn } from 'node:child_process';
import { existsSync as __exists } from 'node:fs';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { basename, resolve } from 'node:path';

const BRAVE = process.env.HFT_BROWSER || [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
].find((p) => __exists(p));
if (!BRAVE) { console.error('No Chromium-based browser found. Set HFT_BROWSER=/path/to/chrome'); process.exit(1); }
const PORT = 9333 + Math.floor(Math.random() * 500);
const [outDir, ...files] = process.argv.slice(2);
mkdirSync(outDir, { recursive: true });

const proc = spawn(BRAVE, [
  '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
  '--no-default-browser-check', '--use-mock-keychain', '--password-store=basic',
  '--disable-extensions', '--disable-component-update', '--force-color-profile=srgb',
  `--remote-debugging-port=${PORT}`, `--user-data-dir=/tmp/brave-render-${PORT}`, 'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function getWs() {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/list`);
      const list = await r.json();
      const page = list.find((t) => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(250);
  }
  throw new Error('browser did not start');
}

const ws = new WebSocket(await getWs());
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
let id = 0;
const pending = new Map();
const listeners = [];
ws.addEventListener('message', (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  else listeners.forEach((l) => l(msg));
});
const send = (method, params = {}) => new Promise((res) => {
  const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params }));
});
const waitEvent = (name, timeout = 15000) => new Promise((res) => {
  const t = setTimeout(() => res(null), timeout);
  listeners.push((m) => { if (m.method === name) { clearTimeout(t); res(m); } });
});

await send('Page.enable');
await send('Runtime.enable');
for (const f of files) {
  const html = readFileSync(f, 'utf8');
  const m = html.match(/<meta name="frame" content="(\d+)x(\d+)"/);
  const [w, h] = m ? [+m[1], +m[2]] : [1920, 1080];
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  const loaded = waitEvent('Page.loadEventFired');
  await send('Page.navigate', { url: 'file://' + resolve(f) });
  await loaded;
  await send('Runtime.evaluate', { expression: 'document.fonts.ready.then(()=>true)', awaitPromise: true });
  await sleep(400);
  const shot = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: w, height: h, scale: 1 } });
  const out = `${outDir}/${basename(f).replace(/\.html$/, '')}.png`;
  writeFileSync(out, Buffer.from(shot.result.data, 'base64'));
  console.log('wrote', out, `${w}x${h}`);
}
ws.close();
proc.kill();
process.exit(0);
