// Troca o <link> do Google Fonts de uma cena por um <style> com as fontes embutidas (data: woff2), guardadas num cache local.
// Por quê: cada Chrome do render baixava as fontes de novo (2,3 s só para ler a duração da cena) e, sem internet, a cena saía com a fonte errada.
// Cache: ~/.cache/motion-studio-fontes/ (um .css pronto por endereço + os .woff2). Só ficam os blocos latin e latin-ext (português).
// Uso no código: import { localizarFontes } from "./fontes-locais.mjs"; const html2 = await localizarFontes(html);
// Uso solto (aquece o cache ou gera uma cópia offline): node fontes-locais.mjs cena.html [saida.html]
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";

const CACHE = path.join(os.homedir(), ".cache", "motion-studio-fontes");
const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"; // sem UA moderno o Google devolve TTF
const hash = (s) => crypto.createHash("sha1").update(s).digest("hex").slice(0, 16);
const SUBCONJ = /^(latin|latin-ext)$/;

async function cssDe(url) {
  fs.mkdirSync(CACHE, { recursive: true });
  const arq = path.join(CACHE, hash(url) + ".css");
  if (fs.existsSync(arq)) return fs.readFileSync(arq, "utf8");
  const r = await fetch(url, { headers: { "user-agent": UA } });
  if (!r.ok) throw new Error(`Google Fonts respondeu ${r.status}`);
  const css = await r.text();
  // o CSS vem em blocos "/* latin */ @font-face{...}": fica só o que o português usa
  const blocos = [...css.matchAll(/(?:\/\*\s*([\w-]+)\s*\*\/\s*)?(@font-face\s*\{[^}]*\})/g)].filter((m) => !m[1] || SUBCONJ.test(m[1]));
  // fonte variável: o Google repete o mesmo arquivo num bloco por peso → junta num bloco só com a faixa de pesos (senão o base64 se repete 6×)
  const grupos = new Map();
  for (const [, sub, bloco] of blocos) {
    const k = bloco.replace(/font-weight:\s*\d+;/, ""), p = +(bloco.match(/font-weight:\s*(\d+)/)?.[1] || 400);
    const g = grupos.get(k) || { sub, bloco, min: p, max: p }; g.min = Math.min(g.min, p); g.max = Math.max(g.max, p); grupos.set(k, g);
  }
  let saida = "";
  for (const { sub, bloco, min, max } of grupos.values()) {
    let b = bloco.replace(/font-weight:\s*\d+;/, `font-weight: ${min === max ? min : min + " " + max};`);
    for (const [, u] of bloco.matchAll(/url\((https:[^)]+)\)/g)) {
      const fa = path.join(CACHE, hash(u) + ".woff2");
      if (!fs.existsSync(fa)) { const f = await fetch(u); if (!f.ok) throw new Error(`fonte ${f.status}: ${u}`); fs.writeFileSync(fa, Buffer.from(await f.arrayBuffer())); }
      b = b.replace(u, "data:font/woff2;base64," + fs.readFileSync(fa).toString("base64"));
    }
    saida += `/* ${sub || "?"} */ ${b.replace("font-display: swap", "font-display: block")}\n`;   // block: nada de quadro com fonte reserva
  }
  fs.writeFileSync(arq, saida);
  return saida;
}

export async function localizarFontes(src, avisar = console.log) {
  const links = [...src.matchAll(/<link\b[^>]*href="(https:\/\/fonts\.googleapis\.com\/[^"]+)"[^>]*>/gi)];
  for (const [tag, href] of links) {
    try { src = src.replace(tag, `<style data-fontes-locais>${await cssDe(href.replace(/&amp;/g, "&"))}</style>`); }
    catch (e) { avisar(`fontes: mantive o link do Google (${e.message})`); }
  }
  // o preconnect não serve mais para nada
  return src.replace(/<link\b[^>]*rel="preconnect"[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>/gi, "");
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) {
  const [ent, sai] = process.argv.slice(2);
  if (!ent) { console.log("uso: node fontes-locais.mjs cena.html [saida.html]"); process.exit(1); }
  const out = await localizarFontes(fs.readFileSync(ent, "utf8"));
  if (sai) fs.writeFileSync(sai, out); else console.log(`cache pronto em ${CACHE}`);
}
