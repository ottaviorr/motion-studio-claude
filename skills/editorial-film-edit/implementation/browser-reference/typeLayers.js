// Emphasis type (DOM, above the graded picture). Time-driven only — a pure function of programme time t.
//   { id, style, text, t0, t1, x, y, size, align: 'left'|'center'|'right', color, w,
//     enter: 'soft'|'blur'|'rise'|'cut'|'type'|'wipe'|'slam'|'pop'|'blurpop'|'draw'|'flicker',
//     exit: 'cut'|'blur'|'fade'|'drift', exitDur (s, drift exit), caret, cps,
//     words: [{w, t, it}] (per-word reveal on the spoken word), wordMotion: 'soft'|'rise'|'decel'|<blur default>,
//     sub / qual / src (number style),
//     A_v15:
//     motion: { drift: [dx, dy] em/s, sway: em, swayHz, track: [from, to] em } — CONTINUOUS motion over the whole life of
//             the layer, independent of the shot grid: a layer that spans a cut keeps moving through it (no reset at cuts).
//     posterize: fps | {fps, from, to} | [{fps, from, to}, …] — stop-motion steps for THIS layer's animation only (absolute
//             reel time); the picture and the grain keep running at 25 fps underneath.
//     halo: true → soft readability halo instead of the hard drop shadow }
// The EDL may give meta.typeDefaults (merged under every layer) so the whole reel shares one motion language.
// `*word*` in text → italic serif accent. Fonts: three families only (src/fonts.js, css --f-sans / --f-serif / --f-mono).
import { clamp, ease, posterT } from './engine.js';

const STYLE_CLASS = {
  display_sans: 'ty7 ty7-sans', display_serif: 'ty7 ty7-serif', serif_ink: 'ty7 ty7-serif ty7-ink', sans_ink: 'ty7 ty7-sans ty7-ink',
  credit: 'ty7 ty7-credit', heavy: 'ty7 ty7-heavy', number: 'ty7 ty7-num', number_ink: 'ty7 ty7-num ty7-ink', label_box: 'ty7 ty7-box', typewriter: 'ty7 ty7-type', typewriter_ink: 'ty7 ty7-type ty7-ink',
  // legacy (A_v03–A_v06), kept so older timelines still load
  extended_caps: 'ty-ext', neon_script: 'ty-neon', hand_script: 'ty-hand', serif_display: 'ty-serif', mono_label: 'ty-mono', boxed_caps: 'ty-box',
  flash_word: 'ty-flash', condensed_caps: 'ty-cond', white_script: 'ty-wscript', serif_type: 'ty-serif', boxed_caps_ink: 'ty-box ty-box-ink',
};
const runs = s => String(s).split(/(\*[^*]+\*)/).filter(Boolean).map(p => p.startsWith('*') ? { text: p.slice(1, -1), it: true } : { text: p, it: false });
const expo = u => (u >= 1 ? 1 : 1 - Math.pow(2, -10 * u));
// soft arrival: a longer, gentler expo with a little blur and rise; settles without overshoot (A_v15 “more active, but softer”)
const SOFT_DUR = 0.32;
function softIn(u) { const e = expo(clamp(u)); return { y: (1 - e) * 0.32, blur: (1 - e) * 9, op: clamp(u * 4.5) }; }

export class TypeLayers {
  constructor(root, layers, size = [1080, 1920], defaults = {}) {
    this.root = root; this.size = size;
    this.items = layers.map(L0 => {
      const L = { ...defaults, ...L0, motion: L0.motion === null ? null : { ...(defaults.motion || {}), ...(L0.motion || {}) } };
      const el = document.createElement('div');
      el.className = `ty ${STYLE_CLASS[L.style] || 'ty-ext'}${L.halo ? ' soft-halo' : ''}`;
      if (L.referenceLine) el.classList.add('reference-line');
      el.dataset.id = L.id || ''; el.dataset.avoid = '1'; el.dataset.kind = 'type';
      const span = document.createElement('span');
      let wordSpans = null;
      if (L.words) {
        wordSpans = L.words.map((wd, k) => { const s = document.createElement('span'); s.className = `w${wd.it ? ' it' : ''}`; s.style.display = 'inline-block'; s.textContent = (k ? ' ' : '') + wd.w; span.appendChild(s); return [s, wd]; });
      } else if (L.style === 'typewriter' || L.style === 'typewriter_ink' || L.enter === 'type' || L.countTo != null) {
        span.textContent = L.text;
      } else {
        for (const r of runs(L.text)) { const s = document.createElement('span'); if (r.it) s.className = 'it'; s.textContent = r.text; span.appendChild(s); }
      }
      el.appendChild(span);
      if (L.style === 'number' || L.style === 'number_ink') {
        for (const [k, cls] of [['sub', 'ty7-sub'], ['qual', 'ty7-qual'], ['src', 'ty7-src']]) if (L[k]) { const d = document.createElement('div'); d.className = cls; d.textContent = L[k]; el.appendChild(d); }
      }
      let caret = null;
      if (L.caret) { caret = document.createElement('i'); caret.className = 'ty-caret'; el.appendChild(caret); }
      Object.assign(el.style, { left: `${L.x}px`, top: `${L.y}px`, fontSize: `${L.size || 120}px`, textAlign: L.align || 'center' });
      if (L.color) el.style.color = L.color;
      if (L.w) el.style.width = `${L.w}px`;
      if (L.shadow) span.style.textShadow = L.shadow;
      el.style.display = 'none';
      root.appendChild(el);
      return { L, el, span, caret, wordSpans, shown: false };
    });
  }

  update(t, splitMotion = null) {
    for (const it of this.items) {
      const { L, el, span, caret } = it;
      const on = t >= L.t0 && t < L.t1;
      if (on !== it.shown) { el.style.display = on ? '' : 'none'; it.shown = on; }
      // Keep the panel's words attached during the A_v16 presenter-split entrance.
      // Their individual animations, clocks and final CSS remain exactly as authored.
      const inPanel = splitMotion && L.t0 >= splitMotion.t0 && L.t1 <= splitMotion.t1 &&
        (splitMotion.side === 'right' ? L.x >= splitMotion.edge : L.x < splitMotion.edge);
      if (on && inPanel) {
        if (!it.panel) {
          const panel = document.createElement('div');
          Object.assign(panel.style, { position: 'absolute', inset: '0', width: `${this.size[0]}px`, height: `${this.size[1]}px`, pointerEvents: 'none' });
          this.root.insertBefore(panel, el); panel.appendChild(el); it.panel = panel;
        }
        it.panel.style.transform = `translateX(${splitMotion.offset.toFixed(4)}px)`;
        it.panel.style.clipPath = splitMotion.side === 'right'
          ? `inset(0 0 0 ${splitMotion.edge}px)`
          : `inset(0 ${this.size[0] - splitMotion.edge}px 0 0)`;
      } else if (it.panel) { it.panel.style.transform = ''; it.panel.style.clipPath = ''; }
      if (!on) continue;
      // A_v15: the animation clock of this layer (stepped inside posterize windows; visibility above uses the real t)
      const ta = posterT(t, L.posterize);
      const lt = ta - L.t0;
      let tx = 0, ty = 0, sc = 1, op = 1, clip = '', blur = 0, track = null;
      switch (L.enter || 'blur') {
        case 'soft': { const s = softIn(lt / (L.enterDur || Math.min(SOFT_DUR, Math.max(0.16, (L.t1 - L.t0) * 0.35)))); ty = s.y; blur = s.blur; op = s.op; break; }
        case 'rise': { const k = expo(clamp(lt / 0.22)); op = clamp(lt / 0.06); ty = (1 - k) * 0.45; break; }
        case 'blur': { const k = ease('cubicOut', clamp(lt / 0.22)); op = clamp(lt / 0.12); blur = (1 - k) * 14; ty = (1 - k) * 0.08; break; }
        case 'wipe': { const k = ease('cubicOut', clamp(lt / 0.16)); clip = `inset(-10% ${((1 - k) * 100).toFixed(1)}% -10% -2%)`; break; }
        case 'cut': break;
        case 'type': { const n = Math.min(L.text.length, Math.floor(lt * (L.cps || 22))); span.textContent = L.text.slice(0, Math.max(0, n)); if (caret) caret.style.opacity = n < L.text.length || Math.floor(lt * 2.2) % 2 === 0 ? 1 : 0; break; }
        case 'slam': { const k = ease('expoOut', clamp(lt / 0.14)); sc = 1.55 - 0.55 * k; blur = (1 - k) * 10; op = clamp(lt / 0.05); break; }
        case 'pop': { const k = ease('backOut', clamp(lt / 0.18)); sc = 0.82 + 0.18 * k; op = clamp(lt / 0.08); break; }
        case 'blurpop': { const k = ease('expoOut', clamp(lt / 0.12)); sc = 1.3 - 0.3 * k; blur = (1 - k) * 8; op = clamp(lt / 0.04); break; }
        case 'draw': { const k = ease('cubicOut', clamp(lt / 0.55)); clip = `inset(-20% ${(1 - k) * 100}% -20% -5%)`; break; }
        case 'flicker': { const f = [1, 0.15, 1, 0.3, 1, 1]; op = lt < 0.3 ? f[Math.floor(lt / 0.05)] : 1; break; }
      }
      // A_v15 continuous motion: a slow drift (+ optional sway / tracking) over the WHOLE life of the layer. It never resets at a
      // picture cut, so type that spans a cut carries the eye across it. Measured in em → scales with the type size.
      const M = L.motion;
      if (M) {
        const life = Math.max(0, lt);
        if (M.drift) { tx += M.drift[0] * life; ty += M.drift[1] * life; }
        if (M.sway) { const w = 2 * Math.PI * (M.swayHz || 0.35); tx += M.sway * Math.sin(w * life); ty += M.sway * 0.5 * Math.sin(w * life * 0.83 + 1.1); }
        if (M.track) { const k = ease('sineInOut', clamp(life / Math.max(0.01, L.t1 - L.t0))); track = M.track[0] + (M.track[1] - M.track[0]) * k; }
      }
      if (it.wordSpans) for (const [s, wd] of it.wordSpans) {
        const wt = posterT(t, L.posterize) - wd.t;      // each word on its own spoken time, stepped like the layer
        if (L.wordMotion === 'fade') {
          s.style.transform = ''; s.style.opacity = clamp((wt + 0.01) / 0.08).toFixed(3); s.style.filter = '';
        } else if (L.wordMotion === 'soft') {
          const st = softIn((wt + 0.03) / SOFT_DUR);
          s.style.transform = `translateY(${st.y.toFixed(3)}em)`; s.style.opacity = st.op.toFixed(3); s.style.filter = st.blur > 0.3 ? `blur(${st.blur.toFixed(1)}px)` : '';
        } else if (L.wordMotion === 'rise') {
          const u = clamp((wt + 0.03) / 0.22), e = expo(u);
          s.style.transform = `translateY(${((1 - e) * 0.45).toFixed(3)}em)`; s.style.opacity = clamp(u * 4).toFixed(3); s.style.filter = '';
        } else if (L.wordMotion === 'decel') {
          const u = clamp((wt + 0.03) / 0.55), e = expo(u), x = (1 - e) * 2.4;
          s.style.transform = `translateX(${x.toFixed(3)}em)`; s.style.opacity = clamp(u * 6).toFixed(3); s.style.filter = x > 0.02 ? `blur(${Math.min(14, x * 9).toFixed(1)}px)` : '';
        } else { const k = clamp((wt + 0.02) / 0.12); s.style.opacity = k.toFixed(3); s.style.filter = k < 0.98 ? `blur(${((1 - k) * 10).toFixed(1)}px)` : ''; }
      }
      if (L.countTo != null) { const u = clamp(lt / (L.countDur || 0.6)), e = expo(u); span.textContent = `${Math.round(L.countTo * (u >= 1 ? 1 : e))}${L.countSuffix ?? '%'}`; }
      // exits: hard cut by default; 'blur' = defocus out, 'fade' = 0.12 s, 'drift' = 0.28 s soft fade + blur while the drift goes on
      const left = L.t1 - ta;
      if (L.exit === 'blur' && left < 0.12) { const e = 1 - left / 0.12; blur = Math.max(blur, e * 10); op *= 1 - 0.7 * e; }
      if (L.exit === 'fade' && left < 0.12) op *= left / 0.12;
      const xd = L.exitDur || 0.28;   // 'drift' exit length (the EDL shortens it when a title cannot run past its cut)
      if (L.exit === 'drift' && left < xd) { const e = ease('cubicIn', 1 - left / xd); blur = Math.max(blur, e * 8); op *= 1 - e; ty -= e * 0.12; }
      const anchor = L.align === 'left' ? '' : L.align === 'right' ? 'translateX(-100%) ' : 'translateX(-50%) ';
      el.style.transform = `${anchor}translate(${tx.toFixed(4)}em, ${ty.toFixed(4)}em)${sc !== 1 ? ` scale(${sc.toFixed(4)})` : ''}`;
      el.style.opacity = op;
      el.style.clipPath = clip;
      el.style.filter = blur > 0.2 ? `blur(${blur.toFixed(1)}px)` : '';
      if (track != null) el.style.letterSpacing = `${track.toFixed(4)}em`;
    }
  }

  active() { return this.items.filter(i => i.shown).map(i => ({ id: i.L.id, kind: 'type', el: i.el, p: { opacity: 1, x: 0 }, avoid: true, depth: 0 })); }
}
