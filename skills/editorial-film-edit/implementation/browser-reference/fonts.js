// A_v15: the ONLY three type families of the reel (user: “only 3 main font families”).
// Every DOM style (css/reel.css uses the same three stacks via --f-sans / --f-serif / --f-mono) and every canvas text
// (ghost words, inserts through kit.js F) must resolve to one of these. The first name of each stack is the family;
// the rest are fallbacks for machines without it (render on the user's Mac: Helvetica Neue / Didot / Menlo exist).
export const FONT = {
  sans: '"Helvetica Neue", Helvetica, Arial, sans-serif',      // grotesque: captions, heavy words, UI
  serif: '"Didot", "Bodoni 72", "Bodoni Moda", serif',          // display serif + italic accents, numerals
  mono: 'Menlo, "SF Mono", "DejaVu Sans Mono", monospace',        // credits, sources, typewriter, code
};
export const FAMILIES = Object.fromEntries(Object.entries(FONT).map(([k, v]) => [k, v.split(',')[0].replace(/"/g, '').trim()]));
// generic fallbacks are allowed in an audit (they only appear when the family itself is missing)
const FALLBACKS = new Set(Object.values(FONT).flatMap(v => v.split(',').slice(1).map(s => s.replace(/"/g, '').trim().toLowerCase())));
// family a CSS font-family string resolves to (its first name), or null if it is not one of the three
export function familyOf(cssFamily) {
  const first = String(cssFamily || '').split(',')[0].replace(/["']/g, '').trim().toLowerCase();
  const hit = Object.entries(FAMILIES).find(([, f]) => f.toLowerCase() === first);
  return hit ? hit[0] : FALLBACKS.has(first) ? 'fallback' : null;
}
// ONE source of truth for CSS and canvas: main.js writes these stacks into the CSS custom properties at boot, so the DOM
// type (css/reel.css: --f-sans / --f-serif / --f-mono) and the canvas type (ghost words, inserts via kit.js F) can never drift apart.
// Heavy words are a WEIGHT of the sans (800), not a fourth family.
export function applyFontTokens(el = document.documentElement) {
  el.style.setProperty('--f-sans', FONT.sans);
  el.style.setProperty('--f-serif', FONT.serif);
  el.style.setProperty('--f-mono', FONT.mono);
}
