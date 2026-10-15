// Componentes da montagem final no Remotion (skill edicao-video).
// Papéis: a camada de TELA (cortes + zoom) vem pronta do render.py --camada-tela; as CENAS vêm do HyperFrames (kit/hf.mjs);
// aqui entram câmera, transições, capítulos, áudio e efeitos — e tudo fica editável na linha do tempo do Remotion Studio.
// Transições seguem a motion-doctrine / cut-the-curve do HyperFrames: corte no meio do movimento, mesma direção e velocidade
// dos dois lados, nunca fusão. Tela → cena = empurrão para a frente (zoom-through); cena → tela = curva para a esquerda;
// fechamento = zoom reverso (chegada).
import React from "react";
import { AbsoluteFill, Easing, interpolate, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { Video } from "@remotion/media";
import { loadFont as loadBricolage } from "@remotion/google-fonts/BricolageGrotesque";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";

const { fontFamily: TITULO } = loadBricolage("normal", { weights: ["700", "800"], subsets: ["latin"] });
const { fontFamily: UI } = loadInter("normal", { weights: ["600", "700"], subsets: ["latin"] });

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const p3in = Easing.in(Easing.poly(3)), p4in = Easing.in(Easing.poly(4)), p4out = Easing.out(Easing.poly(4)), expoOut = Easing.out(Easing.exp);

export type Costura = { t: number; tipo: "entra-cena" | "volta-tela" | "fechamento"; ox: number; oy: number };

// ---------- TELA: a camada de tela, sai e volta pelas costuras ----------
export const Tela: React.FC<{ src: string; costuras: Costura[]; escala: number; children?: React.ReactNode }> = ({ src, costuras, escala }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  let s = 1, blur = 0, op = 1, x = 0, ox = 0.5, oy = 0.5;
  for (const c of costuras) {
    if (c.tipo === "entra-cena" && t >= c.t - 0.2 && t < c.t) {            // empurrão: cresce acelerando, desfoca, apaga
      const k = (t - (c.t - 0.2)) / 0.2;
      s = interpolate(k, [0, 1], [1, 1.2], { ...clamp, easing: p3in }); blur = 18 * k; op = 1 - 0.85 * k; ox = c.ox; oy = c.oy;
    }
    if (c.tipo === "fechamento" && t >= c.t - 0.2 && t < c.t) {           // zoom reverso: encolhe acelerando
      const k = (t - (c.t - 0.2)) / 0.2;
      s = interpolate(k, [0, 1], [1, 0.8], { ...clamp, easing: p3in }); blur = 18 * k; op = 1 - 0.85 * k; ox = c.ox; oy = c.oy;
    }
    if (c.tipo === "volta-tela" && t >= c.t && t < c.t + 0.3) {           // curva: entra da direita já em movimento, desacelera
      const k = (t - c.t) / 0.3;
      x = interpolate(k, [0, 1], [230 * escala, 0], { ...clamp, easing: p4out }); op = interpolate(k, [0, 0.5], [0.35, 1], clamp);
    }
  }
  // um lado visível por vez: depois que a cena entra, a tela fica escondida até a costura de volta
  const ultima = [...costuras].filter((c) => c.t <= t).sort((a, b) => a.t - b.t).pop();
  if (ultima && ultima.tipo !== "volta-tela") op = 0;
  return (
    <AbsoluteFill style={{ transform: `translateX(${x}px) scale(${s})`, transformOrigin: `${ox * 100}% ${oy * 100}%`,
      filter: blur > 0.05 ? `blur(${blur * escala}px)` : undefined, opacity: op }}>
      <Video src={src} muted style={{ width: "100%", height: "100%" }} />
    </AbsoluteFill>
  );
};

// ---------- CENA: um motion em tela cheia, com entrada e saída da doutrina ----------
export const Cena: React.FC<{ src: string; entrada: "empurrao" | "reverso" | "nenhuma"; saida: "curva" | "nenhuma"; dur: number; escala: number }> = ({ src, entrada, saida, dur, escala }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  let s = 1, blur = 0, op = 1, x = 0;
  if (entrada !== "nenhuma" && t < 0.5) {                                  // entra ainda em movimento (nunca do repouso)
    const k = t / 0.5;
    s = interpolate(k, [0, 1], entrada === "empurrao" ? [0.75, 1] : [1.25, 1], { ...clamp, easing: expoOut });
    blur = 18 * (1 - interpolate(k, [0, 1], [0, 1], { ...clamp, easing: expoOut })); op = interpolate(k, [0, 1], [0.15, 1], { ...clamp, easing: expoOut });
  }
  if (saida === "curva" && t > dur - 0.3) {                                // sai acelerando para a esquerda, apaga antes do corte
    const k = (t - (dur - 0.3)) / 0.3;
    x = interpolate(k, [0, 1], [0, -230 * escala], { ...clamp, easing: p4in }); op = interpolate(k, [0, 0.7], [1, 0], clamp);
  }
  return (
    <AbsoluteFill style={{ transform: `translateX(${x}px) scale(${s})`, filter: blur > 0.05 ? `blur(${blur * escala}px)` : undefined, opacity: op }}>
      <Video src={src} muted style={{ width: "100%", height: "100%" }} />
    </AbsoluteFill>
  );
};

// ---------- CÂMERA: moldura fixa por cima; cada trecho do bruto é um clipe filho ----------
export const Moldura: React.FC<{ rect: [number, number, number, number]; escala: number; recuo: number; raio: number; someEm?: number; children: React.ReactNode }> = ({ rect, escala, recuo, raio, someEm, children }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  const [x, y, w, h] = rect;
  const op = someEm === undefined ? 1 : interpolate(t, [someEm - 0.2, someEm + 0.3], [1, 0], clamp);
  return (
    <div style={{ position: "absolute", left: (x + recuo) * escala, top: (y + recuo) * escala, width: (w - 2 * recuo) * escala, height: (h - 2 * recuo) * escala,
      borderRadius: raio * escala, overflow: "hidden", opacity: op, boxShadow: `0 ${10 * escala}px ${30 * escala}px rgba(0,0,0,.35)` }}>
      {children}
    </div>
  );
};
// um trecho da câmera. src = camera.mp4 (só a câmera, já recortada e ampliada pelo gerador, H.264 BT.709):
// o bruto HEVC 10 bits lido direto pelo Remotion saía com a cor lavada (pretos claros).
export const TrechoCamera: React.FC<{ src: string; trimBefore: number; escala: number; recuo: number; largura: number; altura: number }> = ({ src, trimBefore, escala, recuo, largura, altura }) => (
  <Video src={src} trimBefore={trimBefore} muted style={{ position: "absolute", left: -recuo * escala, top: -recuo * escala, width: largura * escala, height: altura * escala, maxWidth: "none" }} />
);

// ---------- CAPÍTULO: etiqueta acima da câmera, entrada em cascata palavra a palavra, saída para a esquerda ----------
export const Capitulo: React.FC<{ n: number; texto: string; x: number; base: number; escala: number; cor?: string }> = ({ n, texto, x, base, escala, cor = "#e8b867" }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  const E = escala, dur = 3;
  const caixa = interpolate(t, [0, 0.45], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.5)) });
  const sai = interpolate(t, [dur - 0.45, dur - 0.1], [0, 1], { ...clamp, easing: p4in });
  const palavras = texto.split(" ");
  return (
    <div style={{ position: "absolute", left: x * E, top: base * E, transform: `translate(${-sai * 160 * E}px, -100%) scale(${0.85 + 0.15 * caixa})`, transformOrigin: "0% 100%",
      opacity: Math.min(caixa * 1.4, 1) * (1 - sai), display: "flex", alignItems: "center", gap: 16 * E, padding: `${12 * E}px ${26 * E}px ${12 * E}px ${12 * E}px`,
      borderRadius: 999, background: "rgba(13,12,20,.78)", border: `${1 * E}px solid rgba(255,255,255,.10)`, boxShadow: `0 ${14 * E}px ${36 * E}px rgba(0,0,0,.35)` }}>
      <div style={{ width: 46 * E, height: 46 * E, borderRadius: "50%", background: cor, color: "#16141f", display: "grid", placeItems: "center", font: `800 ${22 * E}px ${UI}` }}>{String(n).padStart(2, "0")}</div>
      <div>
        <div style={{ font: `700 ${12 * E}px ${UI}`, letterSpacing: ".16em", color: cor, opacity: interpolate(t, [0.15, 0.4], [0, 1], clamp) }}>CAPÍTULO {n}</div>
        <div style={{ display: "flex", gap: 9 * E, font: `800 ${27 * E}px ${TITULO}`, color: "#f4f3f8", letterSpacing: "-.02em", whiteSpace: "nowrap" }}>
          {palavras.map((p, i) => {                                         // waterfall: cada palavra sobe com atraso decrescente
            const t0 = 0.18 + 0.05 * (1 - Math.pow(0.84, i)) / (1 - 0.84);
            const k = interpolate(t, [t0, t0 + 0.3], [0, 1], { ...clamp, easing: p4out });
            return <span key={i} style={{ display: "inline-block", transform: `translateY(${(1 - k) * 22 * E}px)`, opacity: 0.35 + 0.65 * k * (k > 0 ? 1 : 0) * (t >= t0 ? 1 : 0) }}>{p}</span>;
          })}
        </div>
      </div>
    </div>
  );
};

export { AbsoluteFill, Sequence };
