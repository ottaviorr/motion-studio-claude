// Reel engine — pure, DOM-free. Everything is a function of absolute time t (seconds),
// so playback, scrubbing and validation all evaluate the same code path.
// Authored by Claude Opus 5.5 for OPUS 5.5 talking-head reel A_v01.

export const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const lerp = (a, b, k) => a + (b - a) * k;

// ── Easing ───────────────────────────────────────────────────────────────────
const c1 = 1.70158, c3 = c1 + 1;
export const EASE = {
  linear: k => k,
  hold: k => (k < 1 ? 0 : 1),
  sineInOut: k => -(Math.cos(Math.PI * k) - 1) / 2,
  sineOut: k => Math.sin((k * Math.PI) / 2),
  cubicIn: k => k * k * k,
  cubicOut: k => 1 - Math.pow(1 - k, 3),
  cubicInOut: k => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2),
  quartOut: k => 1 - Math.pow(1 - k, 4),
  expoOut: k => (k === 1 ? 1 : 1 - Math.pow(2, -10 * k)),
  expoIn: k => (k === 0 ? 0 : Math.pow(2, 10 * k - 10)),
  expoInOut: k =>
    k === 0 ? 0 : k === 1 ? 1 : k < 0.5 ? Math.pow(2, 20 * k - 10) / 2 : (2 - Math.pow(2, -20 * k + 10)) / 2,
  backOut: k => 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2),
  // Damped spring that settles by k=1 (one overshoot, no wallpaper wobble).
  spring: k => 1 - Math.exp(-6 * k) * Math.cos(7.5 * k) * (1 - k),
};
export const easeNames = Object.keys(EASE);
export const ease = (name, k) => (EASE[name] || EASE.cubicInOut)(clamp(k));

// ── Keys ─────────────────────────────────────────────────────────────────────
// A key track is [[t, value, easeName?], ...] sorted by t. The ease on a key shapes
// the segment ARRIVING at that key. Values may be numbers or arrays of numbers.
export function sample(keys, t) {
  if (!keys || keys.length === 0) return undefined;
  if (t <= keys[0][0]) return keys[0][1];
  const last = keys[keys.length - 1];
  if (t >= last[0]) return last[1];
  let i = 1;
  while (i < keys.length && keys[i][0] < t) i++;
  const [t0, v0] = keys[i - 1];
  const [t1, v1, e] = keys[i];
  const k = t1 === t0 ? 1 : ease(e || 'cubicInOut', (t - t0) / (t1 - t0));
  if (Array.isArray(v0)) return v0.map((a, j) => lerp(a, v1[j], k));
  if (typeof v0 === 'number') return lerp(v0, v1, k);
  return k < 1 ? v0 : v1;
}

// Layer animation shorthand → explicit keys.
//   in:  { t, dur, from:{prop:v}, ease }   props travel from `from` to rest value
//   out: { t, dur, to:{prop:v}, ease }     props travel from rest value to `to`
//   keys:{ prop: [[t,v,ease],...] }        explicit tracks (merged, sorted)
export const REST = { opacity: 1, x: 0, y: 0, scale: 1, rot: 0, skewX: 0, blur: 0, tracking: 0, reveal: 1, typed: 1, count: 1, on: 1, progress: 1, press: 0, strike: 0, clip: 1 };

export function compileLayer(layer) {
  const tracks = {};
  const push = (p, k) => (tracks[p] = tracks[p] || []).push(k);
  const rest = p => (layer.rest && p in layer.rest ? layer.rest[p] : REST[p]);
  if (layer.in) {
    const { t, dur = 0.5, from = { opacity: 0 }, ease: e = 'expoOut' } = layer.in;
    for (const p in from) { push(p, [t, from[p]]); push(p, [t + dur, rest(p), e]); }
  }
  for (const p in layer.keys || {}) for (const k of layer.keys[p]) push(p, k);
  for (const p in tracks) tracks[p].sort((a, b) => a[0] - b[0]);
  if (layer.out) {
    // Exit starts from whatever the property is doing at out.t (not the rest value).
    const { t, dur = 0.35, to = { opacity: 0 }, ease: e = 'cubicIn' } = layer.out;
    for (const p in to) {
      const from = tracks[p] ? sample(tracks[p], t) : rest(p);
      tracks[p] = (tracks[p] || []).filter(k => k[0] < t);
      push(p, [t, from]); push(p, [t + dur, to[p], e]);
    }
  }
  const t0 = layer.in ? layer.in.t : (layer.t0 ?? 0);
  const t1 = layer.out ? layer.out.t + (layer.out.dur ?? 0.35) : (layer.t1 ?? Infinity);
  const children = (layer.children || []).map(compileLayer);
  return { ...layer, tracks, t0, t1, children };
}

export function propsAt(cl, t) {
  const out = {};
  for (const p in REST) out[p] = cl.rest && p in cl.rest ? cl.rest[p] : REST[p];
  for (const p in cl.tracks) out[p] = sample(cl.tracks[p], t);
  return out;
}

// ── Footage camera ───────────────────────────────────────────────────────────
// Camera keys: { t, to: presetName | {overrides}, dur, ease }. A move starts at t
// from the state at t and lands on `to` at t+dur. Holds are implicit.
const CAM_FIELDS = ['x', 'y', 'w', 'h', 'r', 'zoom', 'fy', 'ax'];

export function compileCamera(cameraKeys, presets) {
  const resolve = to => (typeof to === 'string' ? { ...presets[to] } : { ...to });
  const tracks = Object.fromEntries(CAM_FIELDS.map(f => [f, []]));
  let state = null;
  for (const k of cameraKeys) {
    const target = { ...(state || {}), ...(k.preset ? presets[k.preset] : {}), ...resolve(k.to) };
    if (!state) {
      for (const f of CAM_FIELDS) tracks[f].push([k.t, target[f]]);
    } else {
      for (const f of CAM_FIELDS) {
        tracks[f].push([k.t, state[f]]);
        tracks[f].push([k.t + (k.dur ?? 0.6), target[f], k.ease || 'expoInOut']);
      }
    }
    state = target;
  }
  return tracks;
}

export function cameraAt(camTracks, t) {
  const c = {};
  for (const f of CAM_FIELDS) c[f] = sample(camTracks[f], t);
  return c;
}

// Crop track rows: [t, cx, cy, top, gx0, gx1] normalised to source.
export function subjectAt(track, t) {
  const rows = track.rows;
  if (t <= rows[0][0]) return rows[0];
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] >= t) {
      const a = rows[i - 1], b = rows[i], k = (t - a[0]) / (b[0] - a[0]);
      return a.map((v, j) => lerp(v, b[j], k));
    }
  }
  return rows[rows.length - 1];
}

// Source rectangle for a card. Never stretches: crop aspect === card aspect.
//   zoom 1 = the smallest crop that still covers the card ("cover").
//   fy   = where the subject's face centre should sit inside the card (0..1 of height).
//   ax   = horizontal blend: 1 follows the tracked subject, 0 locks to source centre.
export function cropFor(cam, subject, SW, SH) {
  const cover = Math.max(cam.w / SW, cam.h / SH);
  const s = cover * Math.max(1, cam.zoom);
  const sw = cam.w / s, sh = cam.h / s;
  const cx = lerp(0.5, subject[1], cam.ax ?? 1) * SW;
  const cy = subject[2] * SH;
  let sx = cx - sw / 2;
  let sy = cy - cam.fy * sh;
  sx = clamp(sx, 0, SW - sw);
  sy = clamp(sy, 0, SH - sh);
  return { sx, sy, sw, sh, s };
}

// Map a normalised source rect into stage coordinates through the current crop.
export function sourceRectToStage(cam, crop, nx0, ny0, nx1, ny1, SW, SH) {
  const X = v => cam.x + (v * SW - crop.sx) * crop.s;
  const Y = v => cam.y + (v * SH - crop.sy) * crop.s;
  const x0 = Math.max(cam.x, X(nx0)), x1 = Math.min(cam.x + cam.w, X(nx1));
  const y0 = Math.max(cam.y, Y(ny0)), y1 = Math.min(cam.y + cam.h, Y(ny1));
  return x1 > x0 && y1 > y0 ? { x: x0, y: y0, w: x1 - x0, h: y1 - y0 } : null;
}

// ── Palettes ─────────────────────────────────────────────────────────────────
export const hexToRgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
export const rgbToCss = c => `rgb(${c.map(v => Math.round(v)).join(',')})`;

export function paletteAt(skyKeys, palettes, t) {
  let i = 0;
  while (i < skyKeys.length - 1 && skyKeys[i + 1][0] <= t) i++;
  const a = skyKeys[i], b = skyKeys[Math.min(i + 1, skyKeys.length - 1)];
  const k = b[0] === a[0] ? 0 : ease(b[2] || 'sineInOut', (t - a[0]) / (b[0] - a[0]));
  const pa = palettes[a[1]], pb = palettes[b[1]];
  return pa.map((hex, j) => rgbToCss(hexToRgb(hex).map((v, n) => lerp(v, hexToRgb(pb[j])[n], k))));
}

export const beatAt = (beats, t) => beats.find(b => t >= b.t0 && t < b.t1) || beats[beats.length - 1];
export const captionAt = (chunks, t) => chunks.find(c => t >= c.t0 && t < c.t1) || null;

// ── A_v15: posterize-time (stop-motion) for TYPE only ───────────────────────
// P = { fps: 8, from?: t, to?: t } or a number (fps over the whole life) or [{fps, from, to}, …] windows (absolute reel time).
// Inside a window the time used by a type animation is held on a coarser grid (8 fps = every 3rd frame at 25 fps),
// so the letters move in steps while the picture and the film grain keep running at 25 fps.
export function posterT(t, P) {
  if (!P) return t;
  const list = Array.isArray(P) ? P : [typeof P === 'number' ? { fps: P } : P];
  for (const w of list) {
    if (!w || !(w.fps > 0)) continue;
    if (t < (w.from ?? -Infinity) || t >= (w.to ?? Infinity)) continue;
    const base = w.from ?? 0;                       // grid anchored at the window start → the first step lands on the window
    return base + Math.floor((t - base) * w.fps + 1e-6) / w.fps;
  }
  return t;
}
