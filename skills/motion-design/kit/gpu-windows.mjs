// Windows com duas GPUs (notebook: Intel + NVIDIA): marca os Chromes de render para usar a GPU dedicada.
// Sem isso o HyperFrames/Remotion caem na Intel (cena com shader: 170 s × 128 s na RTX 3050).
// Cada versão nova do Chrome (HyperFrames) e cada projeto Remotion novo trazem um .exe novo: rode de novo (o hf.mjs já roda sozinho).
// uso: node gpu-windows.mjs [pasta-do-estudio]   → marca o que faltar em HKCU\Software\Microsoft\DirectX\UserGpuPreferences
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

if (process.platform !== "win32") process.exit(0);
// raiz do estúdio: sobe as pastas até achar skills/ e projetos/ (o script roda do kit e das cópias nos projetos)
let estudio = path.resolve(process.argv[2] || path.dirname(fileURLToPath(import.meta.url)));
while (!(fs.existsSync(path.join(estudio, "skills")) && fs.existsSync(path.join(estudio, "projetos"))) && path.dirname(estudio) !== estudio) estudio = path.dirname(estudio);
const CHAVE = "HKCU\\Software\\Microsoft\\DirectX\\UserGpuPreferences";
const dirs = (p) => { try { return fs.readdirSync(p, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => path.join(p, d.name)); } catch { return []; } };
const existe = (p) => fs.existsSync(p) && p;

const exes = [];
// HyperFrames: ~/.cache/hyperframes/chrome/chrome-headless-shell/<versão>/chrome-headless-shell-win64/
for (const v of dirs(path.join(os.homedir(), ".cache", "hyperframes", "chrome", "chrome-headless-shell")))
  exes.push(existe(path.join(v, "chrome-headless-shell-win64", "chrome-headless-shell.exe")));
// Remotion: <pasta com remotion>/node_modules/.remotion/chrome-headless-shell/win64/… (projetos/*/*/remotion e skills/*/remotion*)
const rem = (p) => existe(path.join(p, "node_modules", ".remotion", "chrome-headless-shell", "win64", "chrome-headless-shell-win64", "chrome-headless-shell.exe"));
for (const pr of dirs(path.join(estudio, "projetos"))) for (const v of dirs(pr)) exes.push(rem(path.join(v, "remotion")));
for (const s of dirs(path.join(estudio, "skills"))) for (const r of dirs(s).filter((d) => path.basename(d).startsWith("remotion"))) exes.push(rem(r));
exes.push(existe(process.env.CHROME || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"));

const ja = spawnSync("reg", ["query", CHAVE], { encoding: "utf8" }).stdout || "";
let novos = 0;
for (const e of exes.filter(Boolean).map((x) => path.normalize(x))) {
  if (ja.toLowerCase().includes(e.toLowerCase())) continue;
  const r = spawnSync("reg", ["add", CHAVE, "/v", e, "/t", "REG_SZ", "/d", "GpuPreference=2;", "/f"], { encoding: "utf8" });
  if (r.status === 0) { novos++; console.log("GPU dedicada:", e); }
}
if (novos) console.log(`(${novos} Chrome(s) novo(s) marcados para a GPU dedicada)`);
