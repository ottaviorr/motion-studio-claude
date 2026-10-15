// A_v07 captions — the reference-4 system (_campstudios, 4:3): bold white grotesque, words appear ONE BY ONE in
// their final place as they are spoken, lines JUSTIFIED across a shared width, key words in italic Didot.
// Data: data/captions.A_v07.json { font, accentFont, size, chunks:[{ t0, t1, y, lines:[[wordIndex…]], words:[{w,t0,t1,accent}] }] }
// Pure function of t (DOM rebuilt only when the chunk changes; per-word opacity/blur set every frame).
import { clamp, posterT } from './engine.js';
import { FONT } from './fonts.js';
// A_v15: (1) the fonts are the reel's sans + serif families (src/fonts.js), whatever the caption JSON says;
// (2) a chunk keeps ONE position for its whole life — chosen at its first frame — so a caption that runs across a picture
//     cut no longer jumps to the next shot's capY (it continues through the cut, like the type layers);
// (3) words arrive softly (expo-out 0.24 s, small rise + light blur) and the block drifts up very slowly while it is on;
// (4) data.posterize / chunk.posterize: stop-motion steps for the caption animation only.

const REVEAL = 0.24;   // s — A_v15: softer arrival (A_v14 0.16)
const DRIFT = 0.025;  // em/s — A_v15: the block rises very slowly while it is on screen

export class Captions {
  constructor(root, data, W, H) {
    this.data = data; this.W = W; this.H = H; this.cur = null; this.spans = []; this.on = true;
    this.el = document.createElement('div'); this.el.className = 'cap7'; root.appendChild(this.el);
    this.size = data.size || 46;
    data = { ...data, font: FONT.sans, accentFont: FONT.serif }; this.data = data;
    this.el.style.fontSize = `${this.size}px`;
    // measure once per word with the real fonts (canvas) → justified line widths that do not depend on DOM timing
    const m = document.createElement('canvas').getContext('2d');
    const width = w => { m.font = w.accent ? `italic 400 ${this.size * 1.2}px ${data.accentFont}` : `700 ${this.size}px ${data.font}`; return m.measureText(w.w).width + (w.box ? this.size * 0.6 : 0); };
    this.yAt = () => H * 0.68;   // set by the player: caption centre of the shot on screen (EDL capY)
    for (const c of data.chunks) {
      c._w = c.words.map(width);
      const nat = c.lines.map(L => L.reduce((s, i) => s + c._w[i], 0));
      const gap = this.size * 0.42;                       // A_v12: compact block (was ref-4 wide justified gaps)
      const want = c.lines.map((L, k) => nat[k] + gap * Math.max(0, L.length - 1));
      const n = Math.max(...c.lines.map(L => L.length));   // ref 4: lines of 4+ words are spread across a wide, fixed measure
      c._lineW = Math.min(c.maxW || W * 0.84, Math.max(...want));
    }
  }

  chunkAt(t) { return this.on ? this.data.chunks.find(c => t >= c.t0 && t < c.t1) || null : null; }

  update(t) {
    const c = this.chunkAt(t);
    if (c !== this.cur) {
      this.cur = c; this.el.replaceChildren(); this.spans = [];
      if (c && !c.suppressed) {
        for (const L of c.lines) {
          const row = document.createElement('div'); row.className = 'cap7-line';
          row.style.width = `${c._lineW}px`;
          row.style.justifyContent = L.length === 1 ? 'center' : 'space-between';
          for (const i of L) {
            const w = c.words[i], sp = document.createElement('span');
            sp.textContent = w.w; if (w.accent) sp.className = 'acc'; if (w.box) sp.className = 'box';
            row.appendChild(sp); this.spans.push([sp, w]);
          }
          this.el.appendChild(row);
        }
      }
      this.el.style.display = c && !c.suppressed ? '' : 'none';
      this.el.classList.toggle('ink', !!(c && c.ink));   // A_v10: ink captions over light inserts (paper / light 3D)
    }
    if (!c || c.suppressed) return;
    if (c._y == null) c._y = c.y ?? this.yAt(c.t0 + 1e-4);     // A_v15: position fixed at the chunk's first frame
    const ta = posterT(t, c.posterize ?? this.data.posterize);
    this.el.style.top = `${c._y}px`;
    this.el.style.left = `${c.x ?? this.W / 2}px`;
    this.el.style.transform = `translate(-50%, calc(-50% - ${(Math.max(0, ta - c.t0) * DRIFT).toFixed(4)}em))`;
    for (const [sp, w] of this.spans) {
      const k = clamp((ta - w.t0 + 0.02) / REVEAL);
      const e = 1 - Math.pow(2, -10 * k);
      sp.style.opacity = Math.min(1, k * 2.6).toFixed(3); sp.style.display = 'inline-block';
      sp.style.transform = `translateY(${((1 - e) * 0.3).toFixed(3)}em)`;
      sp.style.filter = k < 0.6 ? `blur(${((1 - k / 0.6) * 4).toFixed(1)}px)` : '';
    }
  }

  // bounding boxes of the visible words (stage px) for the layout validator
  boxes(stage, scale) {
    const sr = stage.getBoundingClientRect();
    return this.spans.filter(([sp]) => +sp.style.opacity > 0.05).map(([sp, w]) => { const r = sp.getBoundingClientRect(); return { w: w.w, x: (r.left - sr.left) / scale, y: (r.top - sr.top) / scale, w2: r.width / scale, h: r.height / scale }; });
  }
}
