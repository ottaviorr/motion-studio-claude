// A_v15 picture pipeline (A_v03 base, A_v14 film look, A_v15 rewrite of grain / bloom / B&W / archive age).
//   1. compose(): the shot runtime draws the current shot into a 2D "comp" canvas.
//   2. post(): WebGL passes over the comp. Everything is a pure function of the frame index — scrubbing is exact.
//      a) bright-pass + 4× downsample   b) separable Gaussian (H, V) at quarter resolution  → bloom texture
//      c) main pass: gate weave → softness → BLOOM / halation → grade (doc | light neutral B&W | film) → print + archive age
//         → vignette → FILM GRAIN (in film coordinates, new every frame) → dust / scratches → flash.
// A_v15 diagnosis of the A_v14 grain (“a static grain image overlaid on top”). The A_v14 grain DID change every frame (an independent
// check measured ~0.035 correlation of neighbouring high-pass residuals); the sticker feeling came from its LOOK:
//   • coarse 2.4 px value-noise clumps (blotchy), std 0.05, 60 % of it left in the deep shadows / highlights, + dust;
//   • its clump layer was ONE noise field translated by ≈(32, 18) px per frame: after that shift consecutive frames correlate
//     0.52–0.54 (tools/grain_lab.py, GPU look-lab frames) → a pattern that slides over the picture;
//   • grain was in SCREEN coordinates while the gate weave moved the picture under it → grain detached from the image.
//   • a second, sine-hash 1 px grain (0.06–0.075) sat on EVERY shot incl. the speaker; sin() of large arguments loses
//     precision on GPUs → patterned, and the grain changed character at every cut.
//   • frame index was taken modulo 997 → the grain sequence repeated at 39.9 s.
// A_v15 grain: jittered-blob (sparse convolution) noise — Gaussian blobs at random points, one per cell, 3×3 neighbourhood,
// kernel tight enough (e^-4.5 at one cell) that the neighbourhood cut leaves no seams; two octaves (fine 1.15 px cells,
// coarse 2.6 px cells at the current default, with only ≈10% of the variance), hashed with (cell, frame) → independent
// every frame; sampled at the weaved film position and weighted by luminance, smaller in shadows / highlights.
const VS = `attribute vec2 p; varying vec2 uv; void main(){ uv = vec2(p.x*.5+.5, .5-p.y*.5); gl_Position = vec4(p,0.,1.); }`;
// FBO passes render with GL's bottom-up rows; the comp texture is uploaded top-down. Keep one convention: all passes
// address textures with the same uv, so FBO outputs are written and read in the same orientation.
const VS_FBO = `attribute vec2 p; varying vec2 uv; void main(){ uv = vec2(p.x*.5+.5, p.y*.5+.5); gl_Position = vec4(p,0.,1.); }`;
const LUM = 'vec3(0.2126, 0.7152, 0.0722)';
const FS_BRIGHT = `precision highp float;
varying vec2 uv; uniform sampler2D tex; uniform vec2 srcRes; uniform float thr; uniform float exposure;
// uv here runs bottom-up; the comp texture is top-down → flip y when reading the comp
void main(){
  vec2 st = vec2(uv.x, 1.0 - uv.y), q = 1.0 / srcRes;
  vec3 acc = vec3(0.);
  for (int y = 0; y < 4; y++) for (int x = 0; x < 4; x++) acc += texture2D(tex, st + (vec2(float(x), float(y)) - 1.5) * q).rgb;
  vec3 c = acc / 16.0 * exposure;
  float l = dot(c, ${LUM});
  // soft-knee bright pass: only the top of the range blooms
  float w = smoothstep(thr, min(1.0, thr + 0.35), l);
  gl_FragColor = vec4(c * w, 1.);
}`;
const FS_BLUR = `precision highp float;
varying vec2 uv; uniform sampler2D tex; uniform vec2 dir;  // dir = one texel step along the blur axis
void main(){
  // 13-tap Gaussian, sigma ≈ 3.2 texels (quarter resolution → ≈ 13 px at full resolution per pass)
  vec3 c = texture2D(tex, uv).rgb * 0.1324;
  float w[6]; w[0] = 0.1253; w[1] = 0.1063; w[2] = 0.0806; w[3] = 0.0547; w[4] = 0.0332; w[5] = 0.0180;
  for (int i = 0; i < 6; i++) { float o = float(i + 1); c += (texture2D(tex, uv + dir * o).rgb + texture2D(tex, uv - dir * o).rgb) * w[i]; }
  gl_FragColor = vec4(c / 0.9686, 1.);
}`;
const FS = `precision highp float;
varying vec2 uv;
uniform sampler2D tex;
uniform sampler2D bloomTex;
uniform float grade;     // 0 clean, 1 film (teal-orange), 2 B&W (A_v15: light, soft, neutral), 3 doc, 4 B&W hard (A_v14 legacy)
uniform float grainIns;  // film grain std at mid-grey inside grainRect (0 = off)
uniform float grainOut;  // film grain std outside grainRect (A_v15: the speaker; 0 = clean)
uniform float grainSize; // fine grain cell size in output px (coarse = 2.25×)
uniform float grainColor;// 0 mono … 1 full per-dye-layer colour grain (B&W forces mono)
uniform vec4 grainRect;  // uv rect (x0, y0, x1, y1) of the insert (split: the B-roll half only)
uniform float film;      // film look inside grainRect, 0..1
uniform float age;       // A_v15 archive age inside grainRect, 0..1 (fade, softness, flicker, density breathing, dust, scratches)
uniform float bloom;     // A_v15 highlight bloom inside grainRect, 0..1 (added before the grade and before the grain)
uniform float halation;  // per-shot halation strength; 1 preserves the normal film look, 0 disables only halation
uniform float dust;      // A_v15 dust + scratches amount, 0..1 (default 0: optional, the user did not ask for it)
uniform float frame;     // integer frame index of the programme (NOT wrapped)
uniform float vignette;  // 0..1
uniform float blurX;     // whip / push blur in uv units
uniform float rgb;       // RGB split in uv units
uniform float flash;     // 0..1 white flash
uniform float exposure;  // multiplier
uniform float treat;     // 0 photo, 1 dot-matrix, 2 thermal
uniform float sweep;
uniform float cell;
uniform vec2 res;        // output size in px
const vec3 LUMA = ${LUM};
// sine-free hashes (Dave Hoskins) — stable for the coordinate / frame ranges used here
float hash13(vec3 p3){ p3 = fract(p3 * .1031); p3 += dot(p3, p3.zyx + 31.32); return fract((p3.x + p3.y) * p3.z); }
vec3 hash33(vec3 p3){ p3 = fract(p3 * vec3(.1031, .1030, .0973)); p3 += dot(p3, p3.yxz + 33.33); return fract((p3.xxy + p3.yxx) * p3.zyx); }
// jittered-blob noise in cell units; zero mean, normalised to std 1 (5.885 measured with tools/grain_lab.py)
float blobs(vec2 p, float seed){
  vec2 i = floor(p), f = fract(p); float g = 0.;
  for (int y = -1; y <= 1; y++) for (int x = -1; x <= 1; x++) {
    vec2 o = vec2(float(x), float(y));
    vec3 r = hash33(vec3(i + o, seed));
    vec2 d = o + r.xy - f;
    g += (r.z - 0.5) * exp(-dot(d, d) * 4.5);
  }
  return g * 5.885;
}
// smooth low-frequency field (density breathing of an old print) — value noise on a 3-cell lattice across the frame
float lowField(vec2 p, float seed){
  vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f);
  float a = hash13(vec3(i, seed)), b = hash13(vec3(i + vec2(1., 0.), seed)), c = hash13(vec3(i + vec2(0., 1.), seed)), d = hash13(vec3(i + vec2(1., 1.), seed));
  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y) * 2. - 1.;
}
vec3 sampleBlur(vec2 st){
  if (blurX < 0.0005 && rgb < 0.0005) return texture2D(tex, st).rgb;
  vec3 acc = vec3(0.);
  for (int i = -4; i <= 4; i++) {
    float o = float(i) / 4.0 * blurX;
    acc.r += texture2D(tex, st + vec2(o + rgb, 0.)).r;
    acc.g += texture2D(tex, st + vec2(o, 0.)).g;
    acc.b += texture2D(tex, st + vec2(o - rgb, 0.)).b;
  }
  return acc / 9.0;
}
vec3 thermalRamp(float v){
  vec3 a = vec3(0.04,0.02,0.10), b = vec3(0.20,0.10,0.62), cc = vec3(0.88,0.12,0.28), d = vec3(1.0,0.35,0.12), e = vec3(1.0,0.86,0.40), f = vec3(1.0,1.0,0.92);
  if (v < 0.2) return mix(a, b, v / 0.2); if (v < 0.45) return mix(b, cc, (v - 0.2) / 0.25);
  if (v < 0.65) return mix(cc, d, (v - 0.45) / 0.2); if (v < 0.85) return mix(d, e, (v - 0.65) / 0.2); return mix(e, f, (v - 0.85) / 0.15);
}
void main(){
  bool ins = uv.x >= grainRect.x && uv.x <= grainRect.z && uv.y >= grainRect.y && uv.y <= grainRect.w;
  float fm = ins ? film : 0.0, ag = ins ? age : 0.0, bl = ins ? bloom : 0.0;
  bool mono = grade > 1.5 && grade < 2.5 || grade > 3.5;
  vec2 st = uv;
  // gate weave: the picture wanders ≈1 px (slow drift + per-frame jitter); an older print weaves a little more
  vec2 weave = vec2(0.);
  if (fm > 0.0) weave = (vec2(sin(frame * 0.37) + 0.5 * sin(frame * 1.31 + 1.7), cos(frame * 0.29 + 0.4) + 0.5 * sin(frame * 1.07 + 2.3)) * 0.45
                       + (vec2(hash13(vec3(frame, 3.1, 0.)), hash13(vec3(7.7, frame, 0.))) - 0.5) * 0.7) * fm * (1.0 + 0.8 * ag);
  st += weave / res;
  vec3 c = sampleBlur(st) * exposure;
  if (fm > 0.0) {
    // lens + emulsion softness (0.8 px; up to 1.4 px for an old print)
    vec2 q = (0.8 + 0.6 * ag) / res;
    vec3 nb = texture2D(tex, st + vec2(q.x, 0.)).rgb + texture2D(tex, st - vec2(q.x, 0.)).rgb + texture2D(tex, st + vec2(0., q.y)).rgb + texture2D(tex, st - vec2(0., q.y)).rgb;
    c = mix(c, (c + nb * exposure) / 5.0, (0.6 + 0.3 * ag) * fm);
  }
  // A_v15 bloom (before grade and grain): soft glow of the highlights, blurred bright pass from the quarter-res chain.
  // Bloom texture rows are bottom-up → flip y.
  vec3 bt = texture2D(bloomTex, vec2(st.x, 1.0 - st.y)).rgb;
  if (bl > 0.0) c += bt * 0.8 * bl;
  float l = dot(c, LUMA);
  bool inSweep = uv.y <= sweep;
  if (treat > 0.5 && inSweep) {
    if (treat < 1.5) {
      vec2 px = uv * res; vec2 cid = floor(px / cell), cc0 = (cid + 0.5) * cell;
      vec3 s = texture2D(tex, cc0 / res).rgb; float lv = dot(s, LUMA);
      float r = cell * 0.5 * clamp(0.16 + pow(lv, 0.5) * 1.5, 0.0, 1.0);
      float ink = smoothstep(r, r - 1.2, length(px - cc0));
      vec3 bg = vec3(0.04, 0.04, 0.05), fg = mix(vec3(0.95, 0.93, 0.88), vec3(1.0, 0.35, 0.12), step(0.82, lv));
      c = mix(bg, fg, ink); l = dot(c, LUMA);
    } else { c = thermalRamp(clamp(l * 1.1, 0.0, 1.0)); l = dot(c, LUMA); }
  }
  if (treat > 0.5 && abs(uv.y - sweep) < 0.0018 && sweep < 0.999) c = vec3(1.0, 0.35, 0.12);
  if (grade > 3.5) {
    float k = smoothstep(0.02, 0.92, l); c = vec3(mix(k, k * k * (3.0 - 2.0 * k), 0.6));        // A_v14 hard B&W (legacy)
  } else if (grade > 2.5) {
    c = mix(c, c * c * (3.0 - 2.0 * c), 0.16);
    c = mix(vec3(l), c, 0.9) + vec3(0.010, 0.004, -0.008);
  } else if (grade > 1.5) {
    // A_v15 B&W: light, soft, fresh, neutral grey (no tint). Milky but not muddy blacks, open bright mids, gentle snap,
    // highlights roll off below paper white. The old-film character comes from grain / weave / flicker / halation.
    float k = 0.055 + 0.93 * clamp(l, 0., 1.2);
    k = pow(k, 0.86);
    k = mix(k, k * k * (3.0 - 2.0 * k), 0.18);
    c = vec3(k);
  } else if (grade > 0.5) {
    c = mix(c, c * c * (3.0 - 2.0 * c), 0.35);
    vec3 teal = vec3(-0.03, 0.025, 0.05), warm = vec3(0.05, 0.015, -0.04);
    c += teal * (1.0 - smoothstep(0.0, 0.5, l)) + warm * smoothstep(0.45, 1.0, l);
    c = mix(vec3(l), c, 0.92);
  }
  vec2 d = uv - 0.5; d.x *= res.x / res.y;
  if (fm > 0.0) {
    float lf = dot(c, LUMA);
    vec3 f = c;
    if (!mono) {
      // colour print: less saturation (more for an old print), teal shadows / warm highlights, lifted milky blacks
      f = mix(vec3(lf), c, 0.9 - 0.3 * ag);
      f += vec3(-0.010, 0.004, 0.012) * (1.0 - smoothstep(0.0, 0.45, lf)) + vec3(0.025, 0.010, -0.018) * smoothstep(0.5, 1.0, lf);
      f += vec3(0.018, 0.010, -0.012) * ag * smoothstep(0.35, 1.0, lf);                         // faded dye: warm, slightly yellow highlights
      f = 0.04 + 0.945 * f;
    }
    // archive fade: blacks a touch higher, whites a touch lower (B&W already has its own lifted toe)
    f = mix(f, 0.03 + 0.94 * f, ag * (mono ? 0.4 : 1.0));
    f = mix(f, 0.85 + (f - 0.85) / (1.0 + (f - 0.85) / 0.15), step(0.85, f));                 // highlight shoulder → 1.0 (lamps stay bright)
    // halation: wide glow of highlights shows AROUND them (on darker neighbours); colour stock red-orange, B&W grey
    float hl = dot(bt, vec3(0.3333)) * (1.0 - smoothstep(0.3, 0.8, lf)) * halation;
    f += mono ? vec3(hl) * 0.55 : vec3(1.0, 0.24, 0.05) * hl * 1.25;
    f *= 1.0 + (hash13(vec3(frame * 1.7, 9.2, 0.)) - 0.5) * (0.03 + 0.03 * ag);              // exposure flicker ±1.5 % (±3 % fully aged)
    f *= 1.0 + 0.035 * ag * lowField(uv * vec2(2.2, 1.7) + vec2(frame * 0.013, 0.), floor(frame / 3.0)); // uneven print density, changes every 3 frames
    f *= 1.0 - (0.12 + 0.06 * ag) * smoothstep(0.3, 0.8, length(d));                             // lens fall-off
    c = mix(c, f, fm);
  }
  c *= 1.0 - vignette * smoothstep(0.18, 0.62, length(d));
  // A_v15 FILM GRAIN — in film coordinates (moves with the weave), new and independent every frame, no lattice
  float gAmt = ins ? grainIns : grainOut;
  if (gAmt > 0.0) {
    vec2 fp = uv * res + weave;
    vec2 jo = vec2(hash13(vec3(frame, 1.3, 7.1)), hash13(vec3(frame, 5.9, 2.7))) * 97.0;      // per-frame random placement
    float an = hash13(vec3(frame, 3.3, 9.9)) * 6.2832;                                         // per-frame random lattice angle:
    mat2 rot = mat2(cos(an), -sin(an), sin(an), cos(an));                                      // no residual cell axis survives in time
    vec2 rp = rot * fp;
    float fine = blobs((rp + jo) / grainSize, frame * 2.0);
    float coarse = blobs((rp - jo) / (grainSize * 2.25), frame * 2.0 + 1.0);
    float gm = 0.95 * fine + 0.31 * coarse;                                                    // std ≈ 1; coarse contributes ≈9.6% of variance
    vec3 gc = vec3(gm);
    if (!mono && grainColor > 0.0) {
      vec3 dye = vec3(blobs((rp + jo.yx) / (grainSize * 2.25), frame * 2.0 + 4101.0),
                      blobs((rp - jo.yx) / (grainSize * 2.25), frame * 2.0 + 4207.0),
                      blobs((rp + jo * 0.5) / (grainSize * 2.25), frame * 2.0 + 4313.0));
      gc = mix(gc, gc * 0.8 + dye * 0.6, grainColor);
    }
    float lg = dot(clamp(c, 0., 1.), LUMA);
    // film: grain strongest in the midtones, clearly smaller in the toe and the shoulder (0.25 → 1.0 → 0.25)
    float wl = 0.25 + 3.0 * lg * (1.0 - lg);
    c += gc * gAmt * wl;                                                                     // age does not silently increase the selected grain strength
  }
  if (fm > 0.0 && dust > 0.0) {
    // dust on the print (~1 speck/frame, up to 3 when aged), moving with the film
    vec2 px = uv * res + weave, cid = floor(px / 90.0); vec3 r = hash33(vec3(cid, frame * 3.0 + 17.0));
    if (r.x > 0.9965 - 0.007 * ag) {
      vec2 ctr = (cid + 0.2 + 0.6 * r.yz) * 90.0, dv = px - ctr; float an = r.y * 6.2832;
      dv = mat2(cos(an), -sin(an), sin(an), cos(an)) * dv * vec2(1.0, 0.35 + 0.65 * r.z);
      float rad = 1.2 + 3.2 * fract(r.x * 977.0), m = 1.0 - smoothstep(rad * 0.55, rad, length(dv));
      c = mix(c, fract(r.y * 531.0) > 0.7 ? c + 0.32 : c * 0.2, m * 0.85 * fm * dust);
    }
    // aged print: occasionally a thin vertical scratch that lives 3–6 frames and wanders a little
    if (ag > 0.0) {
      float ep = floor(frame / 5.0); vec3 sr = hash33(vec3(ep, 41.0, 13.0));
      if (sr.x > 0.62) {
        float sx = (0.08 + 0.84 * sr.y) * res.x + sin(frame * 0.9 + sr.z * 6.0) * 1.5;
        float w = 1.0 - smoothstep(0.4, 1.3, abs(uv.x * res.x + weave.x - sx));
        float along = 0.55 + 0.45 * lowField(vec2(uv.y * 6.0, ep), 77.0);
        c += vec3(0.10) * w * along * ag * fm * dust;
      }
    }
  }
  c = mix(c, vec3(1.0), flash);
  gl_FragColor = vec4(clamp(c, 0., 1.), 1.);
}`;

const GRADES = { clean: 0, film: 1, bw: 2, doc: 3, bw_hard: 4 };

export class Picture {
  constructor(outCanvas) {
    this.out = outCanvas;
    this.comp = document.createElement('canvas');
    this.comp.width = outCanvas.width; this.comp.height = outCanvas.height;
    this.ctx = this.comp.getContext('2d');
    const gl = outCanvas.getContext('webgl', { premultipliedAlpha: false, preserveDrawingBuffer: false });
    this.gl = gl;
    const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; };
    const program = (vs, fs, names) => {
      const prog = gl.createProgram();
      gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs));
      gl.bindAttribLocation(prog, 0, 'p');
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
      return { prog, u: Object.fromEntries(names.map(n => [n, gl.getUniformLocation(prog, n)])) };
    };
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    const mkTex = () => {
      const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      return t;
    };
    this.tex = mkTex();
    // quarter-resolution bloom chain (two ping-pong targets)
    this.bw = Math.max(1, Math.round(outCanvas.width / 4)); this.bh = Math.max(1, Math.round(outCanvas.height / 4));
    this.fb = [0, 1].map(() => {
      const t = mkTex(); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, this.bw, this.bh, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
      const f = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, f);
      gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0);
      return { t, f };
    });
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    this.pBright = program(VS_FBO, FS_BRIGHT, ['tex', 'srcRes', 'thr', 'exposure']);
    this.pBlur = program(VS_FBO, FS_BLUR, ['tex', 'dir']);
    this.pMain = program(VS, FS, ['tex', 'bloomTex', 'grade', 'grainIns', 'grainOut', 'grainSize', 'grainColor', 'grainRect', 'film', 'age', 'bloom', 'halation', 'dust', 'frame',
      'vignette', 'blurX', 'rgb', 'flash', 'exposure', 'treat', 'sweep', 'cell', 'res']);
  }

  // fx: { grade: 'clean'|'film'|'bw'|'doc'|'bw_hard', grainIns, grainOut, grainSize, grainColor, grainRect, film, age, bloom, bloomThr, dust,
  //       vignette, blurX, rgb, flash, exposure, treat, sweep, cell }
  post(t, fx, fps = 25) {
    const { gl } = this;
    gl.bindTexture(gl.TEXTURE_2D, this.tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, this.comp);
    // bloom chain (also feeds the halation), always computed so the main pass has a defined texture
    gl.viewport(0, 0, this.bw, this.bh);
    gl.useProgram(this.pBright.prog); let u = this.pBright.u;
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb[0].f);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, this.tex); gl.uniform1i(u.tex, 0);
    gl.uniform2f(u.srcRes, this.out.width, this.out.height); gl.uniform1f(u.thr, fx.bloomThr ?? 0.62); gl.uniform1f(u.exposure, fx.exposure ?? 1);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    gl.useProgram(this.pBlur.prog); u = this.pBlur.u; gl.uniform1i(u.tex, 0);
    for (let pass = 0; pass < 2; pass++) {          // H then V, twice → σ ≈ 4.5 quarter px ≈ 18 px at full res
      gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb[1].f); gl.bindTexture(gl.TEXTURE_2D, this.fb[0].t); gl.uniform2f(u.dir, 1 / this.bw, 0); gl.drawArrays(gl.TRIANGLES, 0, 3);
      gl.bindFramebuffer(gl.FRAMEBUFFER, this.fb[0].f); gl.bindTexture(gl.TEXTURE_2D, this.fb[1].t); gl.uniform2f(u.dir, 0, 1 / this.bh); gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    gl.viewport(0, 0, this.out.width, this.out.height);
    gl.useProgram(this.pMain.prog); u = this.pMain.u;
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, this.tex); gl.uniform1i(u.tex, 0);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, this.fb[0].t); gl.uniform1i(u.bloomTex, 1);
    gl.activeTexture(gl.TEXTURE0);
    gl.uniform1f(u.grade, GRADES[fx.grade] ?? 0);
    const gr = fx.grainRect || [0, 0, 1, 1];
    gl.uniform1f(u.grainIns, fx.grainIns || 0); gl.uniform1f(u.grainOut, fx.grainOut || 0);
    gl.uniform1f(u.grainSize, fx.grainSize || 1.15); gl.uniform1f(u.grainColor, fx.grainColor ?? 0.06);
    gl.uniform4f(u.grainRect, gr[0], gr[1], gr[2], gr[3]);
    gl.uniform1f(u.film, fx.film || 0); gl.uniform1f(u.age, fx.age || 0); gl.uniform1f(u.bloom, fx.bloom || 0); gl.uniform1f(u.dust, fx.dust || 0);
    gl.uniform1f(u.halation, fx.halation ?? 1);
    gl.uniform1f(u.frame, Math.round(t * fps));      // A_v15: no modulo — the grain never repeats inside a reel
    gl.uniform1f(u.vignette, fx.vignette ?? 0.35);
    gl.uniform1f(u.blurX, fx.blurX || 0); gl.uniform1f(u.rgb, fx.rgb || 0); gl.uniform1f(u.flash, fx.flash || 0);
    gl.uniform1f(u.exposure, fx.exposure ?? 1);
    gl.uniform1f(u.treat, fx.treat === 'dots' ? 1 : fx.treat === 'thermal' ? 2 : 0);
    gl.uniform1f(u.sweep, fx.sweep ?? 1); gl.uniform1f(u.cell, fx.cell || 14);
    gl.uniform2f(u.res, this.out.width, this.out.height);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
}
