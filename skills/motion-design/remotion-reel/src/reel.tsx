// Montagem de reels/anúncios no Remotion (skill motion-design): cenas gravadas pelo HyperFrames (kit/hf.mjs) +
// música cortada na batida + voz + efeitos. Transições da motion-doctrine do HyperFrames: corte NO MEIO do movimento,
// mesma direção e velocidade dos dois lados, uma direção por vídeo (esquerda), nunca fusão.
//   curva      → sai acelerando para a esquerda / entra da direita desacelerando (padrão entre cenas)
//   empurrao   → sai crescendo e desfocando / entra crescendo (aprofundar o mesmo assunto)
//   reverso    → sai encolhendo / entra grande e assenta (chegada: fecho, oferta)
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { Video, Audio } from "@remotion/media";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const p3in = Easing.in(Easing.poly(3)), p4in = Easing.in(Easing.poly(4)), p4out = Easing.out(Easing.poly(4)), expoOut = Easing.out(Easing.exp);
export type Ent = "nenhuma" | "curva" | "empurrao" | "reverso";
export type Sai = "nenhuma" | "curva" | "empurrao" | "reverso";

export const Cena: React.FC<{ src: string; dur: number; entrada: Ent; saida: Sai; largura: number }> = ({ src, dur, entrada, saida, largura }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  const D = largura * 0.12;                                  // "partial travel": ~12% do quadro, nunca a tela inteira
  let x = 0, s = 1, blur = 0, op = 1;
  if (entrada === "curva" && t < 0.3) { const k = t / 0.3; x = interpolate(k, [0, 1], [D, 0], { ...clamp, easing: p4out }); op = interpolate(k, [0, 0.5], [0.35, 1], clamp); }
  if ((entrada === "empurrao" || entrada === "reverso") && t < 0.5) {
    const k = interpolate(t / 0.5, [0, 1], [0, 1], { ...clamp, easing: expoOut });
    s = entrada === "empurrao" ? 0.75 + 0.25 * k : 1.25 - 0.25 * k; blur = 14 * (1 - k); op = 0.15 + 0.85 * k;
  }
  const r = dur - t;
  if (saida === "curva" && r < 0.3) { const k = 1 - r / 0.3; x = interpolate(k, [0, 1], [0, -D], { ...clamp, easing: p4in }); op = interpolate(k, [0, 0.7], [1, 0], clamp); }
  if ((saida === "empurrao" || saida === "reverso") && r < 0.2) {
    const k = interpolate(1 - r / 0.2, [0, 1], [0, 1], { ...clamp, easing: p3in });
    s = saida === "empurrao" ? 1 + 0.2 * k : 1 - 0.2 * k; blur = 14 * k; op = 1 - 0.85 * k;
  }
  return (
    <AbsoluteFill style={{ transform: `translateX(${x}px) scale(${s})`, filter: blur > 0.05 ? `blur(${blur}px)` : undefined, opacity: op }}>
      <Video src={src} muted style={{ width: "100%", height: "100%" }} />
    </AbsoluteFill>
  );
};

// música: começa no ponto "inicio" da faixa (alinhado à batida), entra rápido e sai com fade no fim do vídeo
export const Musica: React.FC<{ src: string; inicio: number; volume: number; fade: number; dur: number }> = ({ src, inicio, volume, fade, dur }) => {
  const { fps } = useVideoConfig();
  return <Audio src={src} trimBefore={Math.round(inicio * fps)}
    volume={(f) => volume * interpolate(f / fps, [0, 0.08, dur - fade, dur], [0, 1, 1, 0], clamp)} />;
};
