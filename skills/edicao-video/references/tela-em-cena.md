# 01 — Tela encolhida com motion em volta ("a tela diminui e o After Effects acontece ao redor")

Pedido do dono: *"seguir mostrando a tela, mas a tela diminui para uma tela menor e, em volta dessa tela, ter um motion como se fosse realmente um After Effects. Aparece alguma coisa em volta: pequenos motions, cards e tal aparecem na frente da tela."*

Hoje (aula SLA v2) a tela aparece sempre em tela cheia (com zoom) e os motions entram **em tela cheia, tapando a tela** (costura empurrão → cena → curva). Este estudo é o meio-termo: **a gravação continua rodando, menor, num cartão, e o motion mora na margem que sobra e na frente do cartão**.

Complementa (sem repetir) o `02-anotacoes-na-tela.md`: lá estão holofote, lupa, seta, passo e o `vista.json`/recorte do bruto. Aqui é o **palco**: o que acontece com a tela inteira (escala, posição, 3D, fundo) e como cards saem dela.

---

## 1. Resumo em 5 linhas

1. A técnica não tem um nome só: no mercado aparece como **"floating screen / inset screen"** (Screen Studio, Cap, Remotion Recorder), **"UI breakdown" / "SaaS UI animation"** (After Effects) e **"3D screen tilt" / "UI pop-out"**. O efeito central é **a tela virar objeto**: um cartão com borda arredondada e sombra em cima de um fundo da marca.
2. Os números se repetem nas fontes: **escala 0,75–0,84** com coisas em volta (Remotion Recorder 0,77; ElevenLabs ~0,75; Linear ~0,84), **0,90** quando é só um "respiro" para um card passar na frente, **0,55–0,65** quando um texto ou diagrama ocupa um lado; **transição de 0,3–0,6 s** desacelerando (spring damping 200 ou expo.out), **raio de 18–30 px**, **margem ≥ 5 % do lado menor** e **inclinação 3D sutil (3–8°) para ler, forte (14–28°) só de passagem**.
3. **O que a pessoa precisa ler não pode ficar na tela encolhida:** a UI do GoHighLevel (13–14 px na captura) passa a 9–13 px com a tela a 0,66. A tela encolhida é **contexto** ("onde estamos"). A informação vai para o **card que salta** (recorte nítido do bruto ou réplica em ≥ 30 px).
4. **Quando usar:** a fala explica o porquê enquanto a tela está parada, um nome na tela vale ser isolado, ou dá para resumir uma lista ao lado. **Quando NÃO usar:** durante o clique que o aluno precisa copiar (campo, menu, valor). Nesse caso, tela cheia com zoom. Também não serve com a tela rolando ou mudando de página, e não deve passar de ~30 % do tempo de tela.
5. No nosso pipeline isso é **só transformação**: um componente Remotion `TelaEmCena` envolve a `<Tela>` que já existe e muda escala, posição, 3D, raio e sombra pelo tempo. Ele não mexe em `trimBefore`, velocidade nem duração, então **a sincronia voz × câmera continua por construção**. Os cards são componentes Remotion ou HTML `frame(t)` gravados com alfa (`hf.mjs saida.mov` → `<OffthreadVideo transparent>`).

---

## 2. Catálogo de variações [10]

Coordenadas em px da saída 1920×1080. "Medido" = medi quadro a quadro no vídeo de referência; "código" = número tirado do código-fonte aberto da ferramenta; "estúdio" = inferência nossa.

### 2.1 Respiro (scale-down sob um card)
- **Como é:** a tela recua um pouco (1 → 0,90), sem sair do centro, e um card, imagem ou B-roll entra **na frente** dela. Quando o card sai, ela volta a 1.
- **Quando:** um aparte curto (uma imagem, um número, uma frase) que não justifica tirar a tela. É a versão mais barata e a que menos atrapalha.
- **Números (código):** o Remotion Recorder usa `SCALE_DOWN = 0.1` (tela a 90 %), `B_ROLL_TRANSITION_DURATION = 10` quadros (0,33 s a 30 fps), `spring({ damping: 200 })` (sem quique), card com raio de 20 px e sombra `0 0 50px rgba(0,0,0,.2)`. Vários cards seguidos somam o recuo (`1 − 0,1 × n`).
- **Referência:** [remotion-dev/recorder · ScaleDownWithBRoll.tsx](https://github.com/remotion-dev/recorder/blob/main/remotion/scenes/BRoll/ScaleDownWithBRoll.tsx) e [config/transitions.ts](https://github.com/remotion-dev/recorder/blob/main/config/transitions.ts).

### 2.2 Cartão flutuante centrado (a "janela no palco")
- **Como é:** a tela vira um cartão centrado a 0,75–0,84, com raio, sombra e fundo de cor ou gradiente da marca em volta. A câmera do apresentador fica numa bolha que pode **morder o canto do cartão**.
- **Quando:** é o "modo padrão bonito" de tutorial SaaS. Serve para trechos de explicação longa em que a tela é pano de fundo, e como pose de partida para as outras variações.
- **Números:**
  - Linear Initiatives (medido): janela ~84 % da largura, margem lateral ~8 %, topo ~5,5 %, fundo cinza-claro liso, bolha redonda da câmera com diâmetro ~25 % da altura, sobreposta ao canto inferior direito da janela.
  - ElevenLabs Studio 3.0 (medido): janela ~75 % da largura sobre fundo quase preto com **brilho rosa difuso atrás** (glow na cor da marca).
  - Cap (código): layout "Floating" com margem e vão = **5 % do lado menor** (54 px), raio = **2,8 % do lado menor** (30 px), câmera com 30 % da largura útil.
  - Remotion Recorder (código): tela no máximo **77 % da largura** (`LANDSCAPE_DISPLAY_MAX_WIDTH_OF_CANVAS = 0.77`), margem segura de 30 px.
- **Referência:** [Introducing Linear Initiatives](https://www.youtube.com/watch?v=FlDVDvzCmn0) · [ElevenLabs Studio 3.0](https://www.youtube.com/watch?v=ZZSROGCVg9M) · [Cap · crates/rendering/src/lib.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/lib.rs) · [Screen Studio · Look & Feel (padding, inset, shadow)](https://screen.studio/guide/background).

### 2.3 Tela de lado + coluna de texto ou lista de passos
- **Como é:** a tela desliza para um lado (0,60–0,68) e a outra coluna recebe uma lista. Os itens acendem um por um na fala, e o item ativo fica em peso e cor cheios enquanto os outros esmaecem.
- **Quando:** quando a fala enumera ("canal, metas, automações, quem desativa") ou faz um resumo. A tela continua viva, mostrando onde aquilo mora.
- **Números:**
  - ElevenLabs (medido em 0:09–0:12): lista de 7 recursos à esquerda, tela à direita cortada pela borda. O item ativo vai a 100 % e os outros a ~50 %, trocando a cada ~0,3 s. Na saída, a lista some e **a tela desliza até o centro em ~0,6 s**, depois deriva devagar (~2 % de escala em 2 s).
  - Pose sugerida (estúdio): tela 0,64 com centro em x 1252 deixa livre de 54 a 637 px; com vão de 54 px, a coluna de texto vai de 54 a 583 px (≈ 530 px) para texto ≥ 44 px.
- **Referência:** [ElevenLabs Studio 3.0, 0:08–0:12](https://www.youtube.com/watch?v=ZZSROGCVg9M&t=8s).

### 2.4 Tela inclinada em 3D (perspectiva)
- **Como é:** o cartão gira em Y (e um pouco em X) como uma tela física ou uma página de livro aberto, e os cards ocupam o lado que "abriu". Tem dois níveis de inclinação:
  - **sutil**, para continuar legível: rotateY −3,5°, rotateX 1,6°;
  - **forte**, só como movimento de passagem: 14–28°.
- **Quando:** a sutil serve para dar sensação de "objeto" num trecho parado. A forte entra na transição para um card ou diagrama, ou numa abertura de capítulo, e não fica parada enquanto se lê.
- **Números:**
  - HyperFrames `yt-screen-warp` (código): `perspective(1400px) rotateY(-3.5deg) rotateX(1.6deg)`, entrada com escala 0,96 → 1 em 0,5 s (power2.out) e saída de 0,35 s (power2.in).
  - `split-tilt-cards` (código): livro aberto com ±18°, sendo o cartão da esquerda `rotateY(+18)` e o da direita `rotateY(−18)`. **Tela à direita usa rotateY negativo** (a borda de dentro afasta).
  - `tilt-card` (código): rotateX −7°, rotateY 10° em 0,72 s.
  - Cap (código, testes do modo 3D): tilt −28° / 26°, fov 45°. A transição de pose é **cortada direto por padrão** (`transition_in = 0`), e a suavização opcional usa bezier (0,65, 0, 0,35, 1).
  - Tutoriais AE "3D SaaS dashboards": câmera 3D com profundidade entre camadas (sem números publicados).
- **Referência:** `~/.claude/plugins/cache/hyperframes/hyperframes/0.8.140/registry/components/yt-screen-warp/`, `split-tilt-cards/`, `tilt-card/` · [3 Modern Ways to Animate 3D SaaS Dashboards (Editing Snapped)](https://www.youtube.com/watch?v=STJLumt-yww) · [3D Floating UI Animation (Motion Nations)](https://www.youtube.com/watch?v=ErdO0edE1Ig) · [Cap · configuration.rs (Camera3DProperties)](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs).

### 2.5 Elemento que salta da tela (pop-out em 3D) — a estrela do pedido
- **Como é:** a tela encolhe e **um pedaço dela** (o nó do gatilho, o campo, o chip "5m") se descola:
  1. nasce no lugar exato onde está na tela;
  2. sobe em direção à câmera, crescendo de 1,6 a 2,2×, com sombra aumentando e leve rotação;
  3. para numa área livre e fica legível;
  4. volta ao lugar ou sai.

  O lugar de origem pode ficar marcado por um contorno na cor do estado (o "encaixe" vazio).
- **Quando:** a fala dá nome a uma coisa da tela ("Conversations SLA", "SLA Status", "vencimento em breve"). É o jeito de mostrar **qual** elemento sem obrigar a pessoa a caçar.
- **Números:**
  - ElevenLabs (medido em 0:14): o painel "Edit Speech" aparece sozinho, ~1,6× maior que na janela, centralizado, com a mesma sombra e glow.
  - Duração do voo (estúdio, a partir do nível 35): 0,45–0,6 s em expo.out na ida e 0,3–0,4 s em ease-in na volta.
  - Nitidez: recorte **do bruto**, nunca da camada de tela, que já foi ampliada (ver 02, §4.3). Acima de 1,6× sobre captura 1080p, use réplica HTML.
- **Referência:** [ElevenLabs Studio 3.0, 0:13–0:16](https://www.youtube.com/watch?v=ZZSROGCVg9M&t=13s) · [I Recreated a Viral SaaS Animation (Mhd Labs)](https://www.youtube.com/watch?v=HpksVzegElQ), que mistura 2D e 3D com movimento espacial "pulado" · [3D Product Pop Animation (Motion Nations)](https://www.youtube.com/watch?v=VOjo9HmjAa8) · 02-anotacoes §2.5.

### 2.6 Anotação ligada por linha (callout fora da tela)
- **Como é:** com a tela encolhida, o rótulo fica **na margem, fora do cartão**, ligado ao ponto da tela por uma linha fina. A linha nasce do ponto e desenha até o rótulo. Encolher abre espaço para o rótulo sem tapar a UI.
- **Quando:** quando há 2–3 nomes para apontar na mesma tela (laranja = vencimento em breve, vermelho = vencido).
- **Números:**
  - Até **3 rótulos por tela** (Hera, guia de UI animation), entrando com 50–100 ms entre um e outro.
  - Texto de 5–8 palavras no máximo (TechSmith).
  - Rótulo mono ≥ 30 px (nosso nível 30).
  - Linha de 2 px desenhada em 0,3 s; o rótulo chega 0,1 s depois.
- **Referência:** [Hera · UI animation video for software marketing](https://hera.video/blog/ui-animation-video-for-software-marketing) · [TechSmith · annotate recordings](https://www.techsmith.com/blog/annotate-recorded-calls/) · HyperFrames `hw-callout-circle` (registro local).

### 2.7 Tela no canto + diagrama ocupando o resto
- **Como é:** a tela vai para um canto (0,40–0,50) e um diagrama ou cena ocupa ~2/3 do quadro. A tela continua rodando para não "perder o fio".
- **Quando:** o conceito precisa de desenho grande (as duas automações, a régua) e a tela só mostra que a demonstração continua. É o meio-termo exato entre "motion em tela cheia" (hoje) e a tela cheia.
- **Números:**
  - Cap (código): no modo lado a lado, o cartão menor leva 30 % da largura útil, com margem e vão de 5 % do lado menor.
  - Pose sugerida (estúdio): s 0,42, centro (1463, 281), no canto superior direito. Fica longe da câmera, que na aula SLA está embaixo à esquerda.
- **Referência:** [Cap · FLOATING_* em lib.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/lib.rs).

### 2.8 Contador ou selo de estado ao lado da tela
- **Como é:** um número grande (cronômetro, contagem, %) ou um selo de estado vive **na margem ao lado** do cartão, sincronizado com o que acontece na tela.
- **Quando:** teste ao vivo, espera ou estado que muda.
- **Números:** contador em Archivo `tabular-nums` encaixado pela largura da coluna (nível 31). O nosso `SeloStatus` já faz o estado; aqui ele desce do topo para a coluna lateral.
- **Referência:** [Warp 2.0, descrito em moonb.io](https://www.moonb.io/blog/product-launch-video) (rótulos e tempos ao lado do apresentador) · `SeloStatus` em `componentes.tsx` · 02-anotacoes §2.8.

### 2.9 Moldura de janela ou navegador (chrome)
- **Como é:** o cartão ganha uma barra de título (três bolinhas ou URL) e vira "uma janela". Isso ajuda a ler a tela como **objeto**, sobretudo quando a gravação não tem borda própria.
- **Quando:** combina com 2.2 e 2.4. Fica dispensável se a UI já tem cabeçalho forte, como o CRM.
- **Números:**
  - Cap (código): `FrameStyle` = None, MacOS, Windows, Browser ou Macbook; o vídeo entra **dentro** da moldura e o conjunto segue padding, posição e zoom.
  - HyperFrames `browser-device-stage` (código): cartão de 82 % da largura, entrada com escala 0,965 → 1 e subida de 4,5 % da altura em power3.out, sombra `0 3cqh 9cqh` a 45 %, deriva de −0,5 % da altura no platô.
- **Referência:** [Cap · FrameStyle em configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs) · `registry/components/browser-device-stage/`.

### 2.10 Mergulho (o card vira a cena)
- **Como é:** a tela encolhe, um card salta dela e **o próprio card cresce até ocupar o quadro**, virando a cena de motion em tela cheia. Na volta acontece o contrário: a cena encolhe para o tamanho do card e pousa na tela.
- **Quando:** é a ponte entre o modo novo e as cenas que já fazemos. Troca o empurrão genérico por um "objeto que persiste" (nível 38).
- **Números:**
  - `parallax-device-dive` (código): sobe com escala 0,86 → 1,02, empurra para 1,035 e atravessa em 1,09 (power4.in). Depois a UI se abre em camadas, em power4.out.
  - Desfoque no pico da costura: 18–20 px em superfície grande (`cut-catalog`).
- **Referência:** `registry/components/parallax-device-dive/` · `product-launch-video/references/cut-catalog.md` do HyperFrames.

---

## 3. Receita de implementação no nosso pipeline

### 3.1 O que muda (e o que NÃO muda)

| Camada | Hoje | Com TelaEmCena |
|---|---|---|
| Tela (`render.py --camada-tela` → `tela.mp4` + `voz.wav`) | cortes + zoom + câmera tapada | **igual**. Nada é renderizado de novo |
| Remotion `<Tela>` | tela cheia, costuras empurrão/curva | a mesma `<Tela>`, **embrulhada** em `<TelaEmCena>`, que só transforma (escala, posição, 3D, raio, sombra, recorte) |
| Câmera (`MolduraMovel` + `TrechoCam`) | fixa no lugar do bruto | mesmos trechos e mesmos `trimBefore`; opcionalmente embrulhada em `<SegueTela>` (só posição e escala, o rosto nunca inclina) |
| Motions | cena em tela cheia (`Cena`) | + cards e linhas em volta (Remotion) e/ou HTML `frame(t)` com alfa (`hf.mjs x.mov` → `<OffthreadVideo transparent>`) |
| Áudio | `voz.wav` + música | igual (+ um whoosh discreto a 0,12–0,16 na saída do card, se quiser) |

**Sincronia:** `TelaEmCena` e `SegueTela` só mudam CSS `transform`. A `<Video>` da tela continua numa `<Sequence from={0}>` com o vídeo inteiro, e os `TrechoCam` continuam com `from = q0`, `durationInFrames = nq` e `trimBefore = q_in`. Nada muda de tempo, então a revisão continua medindo 0–1 ms. **Regras:** nunca pausar ou congelar a tela dentro do `TelaEmCena` (para congelar, use um card PNG por cima) e nunca mexer em `playbackRate`.

### 3.2 Onde mora no `edicao.json`
Tempos no tempo editado, como `motions`, `capitulos` e `selos`:

```json
"tela_em_cena": [
  { "ini": 137.4, "fim": 155.3, "pose": "3d-direita", "entra": 0.6, "sai": 0.45, "camera": "segue" },
  { "ini": 155.3, "fim": 171.9, "pose": "esquerda" },
  { "ini": 242.3, "fim": 246.9, "pose": "direita", "recorte": [0, 120, 1440, 810] }
],
"cards": [
  { "ini": 146.2, "dur": 7.0, "alvo": [0.64, 0.50, 0.17, 0.12], "para": [470, 330, 620], "src": "anot/sla-status.png", "ry": 10 },
  { "ini": 137.8, "dur": 9.0, "html": "motions3/gatilho-cards.html" }
]
```
- `pose` = nome de `POSES` (abaixo) ou um objeto `{s, cx, cy, rx, ry, raio, sombra, recorte}`. Trechos colados (`fim` = `ini` do próximo) **voam de uma pose para a outra** sem voltar à tela cheia.
- `alvo` no bruto (0–1), a mesma convenção do 02. O `gerar_remotion.py` converte com `vista.json` e depois com `mapeia()` daqui.
- A pose é a **fonte da verdade** também para o HTML: o gerador escreve `tempos.js` com `TELA = {pose, ini, fim}` para a cena HTML desenhar em volta do cartão sem invadir.
- Escolha do momento: use `atividade.json`. Encolha só com tela calma por ≥ 2 s e nunca a menos de 0,5 s de um clique.

### 3.3 Esboço do componente (TSX, encaixa no `componentes.tsx`; não precisa rodar)

```tsx
// ---------- TELA EM CENA: a tela encolhe para um cartão e o motion acontece em volta ----------
// Só transforma a camada de tela (que já vem pronta do render.py --camada-tela). Não muda tempo nenhum:
// a <Video> da tela segue na mesma Sequence from={0}; a sincronia voz × câmera fica intacta.
// Uso: <TelaEmCena trechos={TELA_EM_CENA} escala={E}><Tela src=... costuras=... escala={E} /></TelaEmCena>
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

const W = 1920, H = 1080;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
const expoOut = Easing.out(Easing.exp), cubicIn = Easing.in(Easing.cubic);

export type Pose = {
  s: number;                                   // escala do cartão (1 = tela cheia)
  cx: number; cy: number;                      // centro do cartão na saída (px de 1920×1080)
  rx?: number; ry?: number; rz?: number;       // graus (CSS: rotateX, rotateY, rotateZ)
  recorte?: [number, number, number, number];  // pedaço da camada de tela que aparece [x, y, w, h] (px da tela); padrão = inteira
  raio?: number;                               // px na saída
  sombra?: number;                             // 0..1
};
type PoseCheia = Required<Pose>;
export const CHEIA: PoseCheia = { s: 1, cx: W / 2, cy: H / 2, rx: 0, ry: 0, rz: 0, recorte: [0, 0, W, H], raio: 0, sombra: 0 };

// poses de partida (números da seção 2). Margem mínima = 54 px (5 % do lado menor).
export const POSES: Record<string, Pose> = {
  respiro:      { s: 0.90, cx: 960,  cy: 540, raio: 18, sombra: 0.6 },            // 2.1 Remotion Recorder
  centro:       { s: 0.78, cx: 960,  cy: 520, raio: 20, sombra: 1 },              // 2.2 (sobra embaixo p/ legenda de card)
  direita:      { s: 0.64, cx: 1252, cy: 540, raio: 20, sombra: 1 },              // 2.3 cartão 637–1866; texto em 54–583 px
  esquerda:     { s: 0.64, cx: 668,  cy: 540, raio: 20, sombra: 1 },
  "3d-direita": { s: 0.66, cx: 1220, cy: 540, rx: 3, ry: -12, raio: 22, sombra: 1 }, // 2.4 livro aberto: borda de dentro afasta
  "3d-sutil":   { s: 0.80, cx: 960,  cy: 540, rx: 1.6, ry: -3.5, raio: 18, sombra: 1 }, // yt-screen-warp
  canto:        { s: 0.42, cx: 1463, cy: 281, raio: 16, sombra: 0.8 },            // 2.7 canto sup. direito (câmera embaixo à esq.)
};

export type TrechoTela = { ini: number; fim: number; pose: Pose; entra?: number; sai?: number; deriva?: number };

const completa = (p: Pose): PoseCheia => ({ ...CHEIA, ...p, recorte: p.recorte ?? CHEIA.recorte });
const mistura = (a: PoseCheia, b: PoseCheia, k: number): PoseCheia => ({
  s: lerp(a.s, b.s, k), cx: lerp(a.cx, b.cx, k), cy: lerp(a.cy, b.cy, k),
  rx: lerp(a.rx, b.rx, k), ry: lerp(a.ry, b.ry, k), rz: lerp(a.rz, b.rz, k),
  recorte: a.recorte.map((v, i) => lerp(v, b.recorte[i], k)) as PoseCheia["recorte"],
  raio: lerp(a.raio, b.raio, k), sombra: lerp(a.sombra, b.sombra, k),
});

// pose da tela no instante t (s do vídeo editado). Entrada desacelera (expo.out), saída acelera e é mais curta (nível 35).
// Trechos colados voam direto de uma pose para a outra. No platô: deriva lenta de +2 % (nível 39), 0 = parado de verdade.
export function poseNoTempo(trechos: TrechoTela[], t: number): PoseCheia {
  const ord = [...trechos].sort((a, b) => a.ini - b.ini);
  for (let i = 0; i < ord.length; i++) {
    const tr = ord[i];
    if (t < tr.ini || t >= tr.fim) continue;
    const entra = tr.entra ?? 0.6, sai = tr.sai ?? 0.45, deriva = tr.deriva ?? 0.02;
    const ant = ord[i - 1], prox = ord[i + 1];
    const coladoAnt = !!ant && Math.abs(ant.fim - tr.ini) < 0.05;
    const coladoProx = !!prox && Math.abs(prox.ini - tr.fim) < 0.05;
    const de = coladoAnt ? completa(ant.pose) : CHEIA;
    const kIn = interpolate(t, [tr.ini, tr.ini + entra], [0, 1], { ...clamp, easing: expoOut });
    const kOut = coladoProx ? 0 : interpolate(t, [tr.fim - sai, tr.fim], [0, 1], { ...clamp, easing: cubicIn });
    let p = mistura(de, completa(tr.pose), kIn);
    p = { ...p, s: p.s * (1 + deriva * interpolate(t, [tr.ini + entra, tr.fim - sai], [0, 1], clamp)) };
    if (kOut > 0) p = mistura(p, CHEIA, kOut);
    return p;
  }
  return CHEIA;
}

// ponto da camada de tela (px 1920×1080, já com o zoom da camada) → ponto na saída, com a perspectiva do cartão.
// Serve para ancorar card, linha e câmera num elemento da tela. Ordem CSS: rotateX(a) rotateY(b) rotateZ(c) → aplica Z, depois Y, depois X.
export function mapeia(p: PoseCheia, x: number, y: number, perspectiva = 1600): [number, number] {
  const [x0, y0, w, h] = p.recorte;
  const X = (x - x0 - w / 2) * p.s, Y = (y - y0 - h / 2) * p.s;          // relativo ao centro do cartão
  const a = (p.rx * Math.PI) / 180, b = (p.ry * Math.PI) / 180, c = (p.rz * Math.PI) / 180;
  const Xz = X * Math.cos(c) - Y * Math.sin(c), Yz = X * Math.sin(c) + Y * Math.cos(c);
  const Xy = Xz * Math.cos(b), Zy = -Xz * Math.sin(b);                    // rotateY
  const Yx = Yz * Math.cos(a) - Zy * Math.sin(a), Zx = Yz * Math.sin(a) + Zy * Math.cos(a); // rotateX
  const f = perspectiva / (perspectiva - Zx);                             // perspective-origin = centro do quadro
  return [W / 2 + (p.cx - W / 2 + Xy) * f, H / 2 + (p.cy - H / 2 + Yx) * f];
}
// (conferir com uma foto: npx remotion still Aula out/x.jpg --frame=N — se o ponto cair 2–3 px fora, é o sinal de rotateX)

// fundo do palco: tinta + brilho na cor do ESTADO (ElevenLabs) + chão em grade opcional (nível 49). Fica atrás; com s = 1 a tela cobre tudo.
export const FundoPalco: React.FC<{ escala: number; cor?: string; grade?: boolean }> = ({ escala: E, cor = "#e8b867", grade = false }) => (
  <AbsoluteFill style={{ background: `radial-gradient(60% 55% at 55% 50%, ${cor}2e 0%, transparent 70%), #0d0c14` }}>
    {grade && <div style={{ position: "absolute", inset: 0, transform: `perspective(${1200 * E}px) rotateX(62deg) translateY(${220 * E}px)`,
      backgroundImage: `linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px)`,
      backgroundSize: `${80 * E}px ${80 * E}px`, maskImage: "linear-gradient(to top, #000 10%, transparent 75%)" }} />}
  </AbsoluteFill>
);

export const TelaEmCena: React.FC<{ trechos: TrechoTela[]; escala: number; perspectiva?: number; fundo?: React.ReactNode; children: React.ReactNode }> =
  ({ trechos, escala: E, perspectiva = 1600, fundo, children }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  const p = poseNoTempo(trechos, t);
  const [x0, y0, rw, rh] = p.recorte;
  const w = rw * p.s, h = rh * p.s;                                      // tamanho do cartão na saída
  const cheia = p.s > 0.999 && Math.abs(p.rx) + Math.abs(p.ry) + Math.abs(p.rz) < 0.01 && rw === W && rh === H;
  if (cheia) return <AbsoluteFill>{children}</AbsoluteFill>;              // custo zero fora dos trechos
  return (
    <AbsoluteFill style={{ perspective: perspectiva * E }}>
      {fundo ?? <FundoPalco escala={E} />}
      <div style={{
        position: "absolute", left: (p.cx - w / 2) * E, top: (p.cy - h / 2) * E, width: w * E, height: h * E,
        transform: `rotateX(${p.rx}deg) rotateY(${p.ry}deg) rotateZ(${p.rz}deg)`, transformOrigin: "50% 50%",
        borderRadius: p.raio * E, overflow: "hidden", background: "#000",
        boxShadow: `0 ${30 * E}px ${90 * E}px rgba(0,0,0,${0.5 * p.sombra}), 0 0 0 ${1 * E}px rgba(255,255,255,${0.1 * p.sombra})`,
      }}>
        {/* a camada de tela inteira, reduzida e deslocada para o recorte aparecer no cartão */}
        <div style={{ position: "absolute", left: -x0 * p.s * E, top: -y0 * p.s * E, width: W * E, height: H * E,
          transform: `scale(${p.s})`, transformOrigin: "0 0" }}>
          {children}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// câmera que acompanha a tela (estilo Linear: a bolha morde o canto do cartão).
// rect = lugar da câmera na saída (o mesmo retângulo tapado na camada de tela). Só posição + escala: o rosto nunca inclina.
// Use quando o recorte NÃO tira o canto da câmera; senão deixe a câmera no lugar (ou voando com MolduraMovel.vai).
export const SegueTela: React.FC<{ trechos: TrechoTela[]; rect: [number, number, number, number]; escala: number; minimo?: number; children: React.ReactNode }> =
  ({ trechos, rect, escala: E, minimo = 0.75, children }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig();
  const p = poseNoTempo(trechos, frame / fps);
  const [x, y, w, h] = rect; const rcx = x + w / 2, rcy = y + h / 2;
  const [mx, my] = mapeia(p, rcx, rcy);
  const s = Math.max(p.s, minimo);                                         // câmera não fica menor que 75 % (rosto legível)
  return <AbsoluteFill style={{ transform: `translate(${(mx - s * rcx) * E}px, ${(my - s * rcy) * E}px) scale(${s})`, transformOrigin: "0 0" }}>{children}</AbsoluteFill>;
};

// card que SALTA da tela: nasce no lugar exato do elemento (de = retângulo na camada de tela), voa até "para" crescendo,
// gira um pouco em Y e ganha sombra; nos últimos 0,35 s volta para o lugar (pouso). inicio = s do vídeo editado (para ler a pose).
// children = recorte nítido do BRUTO (PNG congelado, ver 02 §4.3) ou réplica HTML em ≥ 30 px.
export const CardSalto: React.FC<{ trechos: TrechoTela[]; inicio: number; dur: number; de: [number, number, number, number];
  para: [number, number, number]; ry?: number; cor?: string; escala: number; children: React.ReactNode }> =
  ({ trechos, inicio, dur, de, para, ry = 10, cor = "#e8b867", escala: E, children }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  const p = poseNoTempo(trechos, inicio + t);
  const [dx, dy, dw, dh] = de; const [cx, cy, largura] = para;
  const [ox, oy] = mapeia(p, dx + dw / 2, dy + dh / 2);                   // onde o elemento está agora, na saída
  const s0 = (dw * p.s) / largura;                                        // tamanho de origem relativo ao final
  const ida = interpolate(t, [0, 0.55], [0, 1], { ...clamp, easing: expoOut });
  const volta = interpolate(t, [dur - 0.35, dur], [0, 1], { ...clamp, easing: cubicIn });
  const k = ida * (1 - volta);
  const x = lerp(ox, cx, k), y = lerp(oy, cy, k), s = lerp(s0, 1, k);
  const altura = (largura * dh) / dw;
  return (
    <>
      {/* encaixe vazio: contorno na cor do estado no lugar de onde o card saiu */}
      <div style={{ position: "absolute", left: (ox - (dw * p.s) / 2) * E, top: (oy - (dh * p.s) / 2) * E, width: dw * p.s * E, height: dh * p.s * E,
        borderRadius: 8 * E, border: `${2 * E}px solid ${cor}`, opacity: 0.9 * k, boxShadow: `0 0 ${18 * E}px ${cor}66` }} />
      <div style={{ position: "absolute", left: (x - largura / 2) * E, top: (y - altura / 2) * E, width: largura * E, height: altura * E,
        transform: `perspective(${1400 * E}px) rotateY(${ry * k}deg) scale(${s})`, transformOrigin: "50% 50%",
        borderRadius: 14 * E, overflow: "hidden", background: "#fff",
        boxShadow: `0 ${40 * k * E}px ${120 * k * E}px rgba(0,0,0,${0.55 * k}), 0 0 0 ${1 * E}px rgba(0,0,0,.08)` }}>
        {children}
      </div>
    </>
  );
};

// linha-guia do ponto da tela até o card/rótulo na margem: desenha em 0,3 s; o rótulo chega 0,1 s depois (fora deste componente)
export const LinhaGuia: React.FC<{ trechos: TrechoTela[]; inicio: number; ponto: [number, number]; ate: [number, number]; dur: number; escala: number; cor?: string }> =
  ({ trechos, inicio, ponto, ate, dur, escala: E, cor = "#e8b867" }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;
  const [ax, ay] = mapeia(poseNoTempo(trechos, inicio + t), ponto[0], ponto[1]);
  const [bx, by] = ate;
  const comp = Math.hypot(bx - ax, by - ay);
  const desenha = interpolate(t, [0, 0.3], [0, 1], { ...clamp, easing: expoOut });
  const some = interpolate(t, [dur - 0.25, dur], [1, 0], clamp);
  return (
    <svg style={{ position: "absolute", inset: 0, width: "100%", height: "100%", opacity: some }} viewBox={`0 0 ${W} ${H}`}>
      <circle cx={ax} cy={ay} r={6} fill={cor} />
      <line x1={ax} y1={ay} x2={bx} y2={by} stroke={cor} strokeWidth={2} strokeDasharray={comp} strokeDashoffset={comp * (1 - desenha)} />
    </svg>
  );
};
```

### 3.4 Ordem das camadas no `Aula.tsx` (de trás para a frente)

```tsx
<AbsoluteFill style={{ background: "#0d0c14" }}>
  {/* 1. palco + tela (o fundo só aparece quando a tela encolhe) */}
  <Sequence name="Tela" from={0} durationInFrames={N}>
    <TelaEmCena trechos={TELA_EM_CENA} escala={E}><Tela src={staticFile("tela.mp4")} costuras={COSTURAS} escala={E} /></TelaEmCena>
  </Sequence>
  {/* 2. linhas e cards que saltam (Remotion) */}
  <Sequence name="card · SLA status" from={Math.round(146.2 * fps)} durationInFrames={Math.round(7 * fps)}>
    <CardSalto trechos={TELA_EM_CENA} inicio={146.2} dur={7} de={[1240, 520, 330, 130]} para={[470, 330, 620]} escala={E}>
      <Img src={staticFile("anot/sla-status.png")} style={{ width: "100%", height: "100%" }} />
    </CardSalto>
  </Sequence>
  {/* 3. motion HTML frame(t) com alfa: hf.mjs motions3/gatilho-cards.html → .mov (ProRes 4444) */}
  <Sequence name="motion · gatilho (alfa)" from={Math.round(137.8 * fps)} durationInFrames={Math.round(9 * fps)}>
    <OffthreadVideo src={staticFile("cenas/gatilho-cards.mov")} transparent muted />
  </Sequence>
  {/* 4. cenas em tela cheia que continuam existindo (empurrão/curva) */}
  {/* 5. câmera (por cima de tudo, menos capítulos) — opcionalmente embrulhada em SegueTela */}
  <SegueTela trechos={TELA_EM_CENA} rect={[58, 757, 485, 270]} escala={E}>{/* Sequences da câmera, iguais */}</SegueTela>
  {/* 6. capítulos e selo */}
</AbsoluteFill>
```

Notas práticas:
- **Alfa:**
  - `hf.mjs saida.mov` grava ProRes 4444 com alfa (`motores.md`). O `<Video>` do `@remotion/media` que usamos não lê ProRes; use `<OffthreadVideo transparent>` do pacote `remotion`, que aceita VP8, VP9 e ProRes com alfa e extrai PNG, por isso é mais lento.
  - Mantenha os clipes de alfa curtos (≤ 10 s cada).
  - Se o render pesar, converta para WebM: `ffmpeg -i x.mov -c:v libvpx-vp9 -pix_fmt yuva420p -crf 18 -b:v 0 -auto-alt-ref 0 x.webm`.
- **HTML ou Remotion?** Card que **sai da tela** (precisa de `mapeia()` quadro a quadro) e linha-guia ficam no Remotion. Tipografia do portfólio (grito Archivo encaixado, voz serif, objeto 3D three.js) fica no HTML `frame(t)` com alfa, desenhado **em volta** do retângulo do cartão que o `tempos.js` informa.
- **Desfoque:** no voo forte (pose 3D de passagem, mergulho 2.10), desfoque de 18–20 px no wrapper do cartão no pico. No encolher normal, nada de desfoque.
- **Fotos antes do render:** `npx remotion still Aula out/x.jpg --frame=N --scale=0.5` em ini + 0,1 s, no meio e em fim − 0,1 s de cada trecho. Confira três coisas: a borda do cartão não pode cair na zona da câmera, o "encaixe" do card tem que estar sobre o elemento certo, e o remendo da câmera tapada não pode aparecer.
- **Remendo da câmera tapada:** a camada de tela tem o lugar da câmera reconstruído pela vizinhança. Em tela cheia a câmera tapa o remendo, mas com a tela encolhida ele **aparece no canto do cartão**. Há três saídas:
  1. `SegueTela`, em que a câmera vai junto e cobre o remendo;
  2. `recorte` que exclui aquele canto;
  3. pose em que o canto do remendo fica atrás da câmera parada.

  A revisão deve fotografar isso.

---

## 4. Regras

**Fazer**
- Encolher só quando a tela está **calma** (≥ 2 s sem clique pelo `atividade.json`). A transição termina **na palavra**: comece 0,3–0,6 s antes dela.
- Entrar em 0,5–0,6 s desacelerando (expo.out ou spring damping 200, sem quique) e voltar em 0,35–0,45 s acelerando, terminando antes do próximo clique.
- Um trecho de tela encolhida dura **4–15 s**. Abaixo de 3 s, a ida e a volta (~1 s) comem o trecho.
- **Uma ideia por trecho, até 3 elementos em volta**, entrando com 0,08–0,12 s entre um e outro. Cada um fica parado o mínimo de máx(1 s; 0,5 + 0,33 s × palavras) (nível 36).
- O que é para LER vai no card (recorte do bruto ou réplica ≥ 30 px), e a tela encolhida é contexto. Confira a conta: texto da UI × zoom da camada × escala do cartão ≥ 30 px, senão não é para ler ali.
- Margem ≥ 54 px; cartão com raio de 18–22 px (o mesmo da câmera, 18), sombra `0 30px 90px` a 50 % e fio de 1 px branco a 10 %.
- Fundo do palco em tinta com o **brilho na cor do estado** (laranja, vermelho ou verde do SLA). Uma cor de destaque só (nível 42).
- Manter a câmera visível e sem girar. Se a tela vai para o lado da câmera, a câmera voa (`MolduraMovel.vai`) ou segue a tela.
- Variar entre 2–3 poses no vídeo inteiro e repeti-las (o mesmo orçamento das transições).

**Não fazer**
- Encolher durante o clique, a digitação ou a escolha num menu que o aluno precisa copiar. Ali vale tela cheia com zoom.
- Encolher com a tela rolando ou trocando de página: os cards perdem a âncora.
- Deixar a tela inclinada > 8° enquanto se lê. Inclinação forte é só passagem.
- Pôr card em cima do ponto da ação ou da câmera.
- Usar fusão entre tela encolhida e cena: o cartão **persiste** ou vira a cena (mergulho).
- Passar de ~30 % do tempo de tela no modo encolhido (estúdio). Aula é para ver o clique.
- Ampliar a camada de tela para fazer card (ela já tem o zoom e pixela). Recorte do bruto.
- Deixar a tela flutuando, balançando ou "respirando" o tempo todo. No platô, no máximo +2 % de deriva ou parado de verdade.

---

## 5. Três ideias aplicadas à aula SLA (tempos do vídeo editado v2)

Hoje existem cenas cheias em 0–29 s, 30,9–37,4, 117,8–129, 172,5–193,3, 258,5–266,6 e 300,7–fim. As ideias abaixo ficam **entre** elas e não brigam com os exemplos do 02 (metas aos 55 s, contador do teste aos 220 s e ajuste final aos 267 s). A câmera, de 130,7 s em diante, está embaixo à esquerda `[58, 757, 485, 270]`.

### Ideia 1 — "Conversations SLA": a tela vira o painel e os três estados saltam como cards (137,4–155,3 s)
- **Na tela:** o painel do gatilho "Conversations SLA" e, aos ~146 s, o menu SLA Status aberto com Due soon, Overdue e SLA dismissed.
- **Pose:** `3d-direita` (s 0,66, ry −12°, rx 3°) entra em 137,4 s e chega em "Conversations SLA" (137,7). A câmera não se mexe: o cartão fica à direita, e o cartão vai de ~586 a 1854 px em x, e a coluna de texto à esquerda vai de 54 a ~530 px em x e de 54 a 720 px em y, acima da câmera.
- **Motion:**
  - 137,7 s: rótulo mono "O GATILHO" na coluna, com a palavra gigante **SLA STATUS** (Archivo encaixado em ~540 px).
  - 145,9 s ("vencido, que é o vermelho"): do menu aberto saltam **três cards** pela `CardSalto` (recorte do bruto em ~146 s, cada linha do menu), empilhados na coluna com 0,1 s entre eles:
    - `VENCIMENTO EM BREVE · Due soon`, com borda laranja;
    - `VENCIDO · Overdue`, com borda vermelha;
    - `IGNORADO · SLA dismissed`, com borda cinza.
  - 152,0 s ("quase nunca você vai usar"): o card cinza é riscado (risco medido no tamanho da palavra, nível 50) e cai para 35 %.
  - 153,5 s ("os que você mais vai usar"): laranja e vermelho crescem 1,06× com brilho na cor.
  - 155,3 s: os cards voltam para o menu (pouso de 0,35 s) e a tela volta inteira, porque ele começa a escolher a ação.
- **Por que ajuda:** o menu tem texto de ~13 px em inglês. O card traduz e dá a cor do estado, e a pessoa continua vendo que é **aquele** menu.

### Ideia 2 — "o que o gatilho faz": tela à esquerda, três ações acendem ao lado e o card vira a cena "duas automações" (155,3–172,5 s)
- **Na tela:** o painel "Actions" (Enviar notificação interna, Enviar SMS, tag…). A cena "03 duas automações" já existe aos 172,5 s.
- **Pose:** voa de `3d-direita` para `esquerda` (trechos colados, sem voltar à tela cheia) e depois deriva +2 %. Para não colidir com a câmera (embaixo à esquerda), use `SegueTela`: a bolha vai junto e morde o canto inferior esquerdo do cartão, no estilo Linear, cobrindo o remendo da câmera.
- **Motion na coluna da direita** (cartão de 54 a 1283 px; coluna de x 1336 a 1866), lista de 3 linhas no tipo do portfólio:
  - 155,3 s "notificar internamente a minha equipe" → `AVISA. a equipe`;
  - 165,9 s "colocar uma tag" → `MARCA. com tag`;
  - 168,2 s "vou tendo métricas" → `MEDE. quantas vezes venceu`.

  Cada linha acende na palavra e a anterior esmaece para 50 %, como a lista do ElevenLabs. Uma linha-guia sai do item "Enviar notificação interna" na tela até `AVISA.`.
- **Saída (mergulho, 2.10):** em 172,2 s a coluna recua, o cartão da tela encolhe para 0,4 e o bloco `AVISA.` cresce até virar o primeiro trilho da cena "duas automações". O corte acontece no pico do crescimento (desfoque de 18 px), no lugar do empurrão genérico.

### Ideia 3 — a prova: a mensagem "Estamos verificando?" salta da conversa e mostra de onde veio (242,3–246,9 s, depois tela cheia para o clique)
- **Na tela:** a conversa do lead com a mensagem automática "Estamos verificando" recém-chegada. Logo depois (247 s) ele abre as automações. Esse clique fica em tela cheia.
- **Pose:** `direita` (s 0,64) com `recorte` só da área da conversa, sem a barra lateral do CRM. Assim o texto da conversa fica a ~0,64 × zoom da camada, a bolha da câmera continua no lugar (embaixo à esquerda, fora do cartão) e o remendo some no recorte.
- **Motion:**
  - 242,6 s ("aqui a conversa estamos verificando"): a bolha da mensagem salta como card (recorte do bruto, 1,8×) para a coluna da esquerda, com o selo mono `ENVIADA POR AUTOMAÇÃO`.
  - 244,5 s ("foi enviada para uma automação"): embaixo do card escreve-se o "recibo" em mono: `FLUXO · SLA` / `GATILHO · Overdue` / `20:00 VENCIDO`, com o 20:00 em vermelho (a única cor do quadro).
  - 246,5 s: o card pousa de volta na conversa (0,35 s) e o cartão volta à tela cheia **0,4 s antes** do clique em "automações" (247 s).
- **Por que ajuda:** fecha o raciocínio "o lead recebeu porque o SLA venceu" num quadro só, sem tirar a conversa real da frente. Também prepara a "pegadinha" (258 s), porque a mesma mensagem é a que "tira o SLA" e deixa o lead no vácuo.

---

## Fontes

**Código aberto (números exatos)**
- Remotion Recorder:
  - [ScaleDownWithBRoll.tsx](https://github.com/remotion-dev/recorder/blob/main/remotion/scenes/BRoll/ScaleDownWithBRoll.tsx): escala 0,9 com spring damping 200;
  - [config/transitions.ts](https://github.com/remotion-dev/recorder/blob/main/config/transitions.ts): 10 e 15 quadros;
  - [config/layout.ts](https://github.com/remotion-dev/recorder/blob/main/config/layout.ts): tela ≤ 77 % e margem de 30 px;
  - [get-layout.ts](https://github.com/remotion-dev/recorder/blob/main/remotion/layout/get-layout.ts): raio de 20 px.
- Cap (gravador aberto, alternativa ao Screen Studio):
  - [crates/rendering/src/lib.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/lib.rs): layout flutuante com margem de 5 %, câmera 30 % e raio de 2,8 %; padding até 40 %;
  - [crates/rendering/src/scene.rs](https://github.com/CapSoftware/Cap/blob/main/crates/rendering/src/scene.rs): troca de cena com ease-in-out (0,42, 0, 0,58, 1);
  - [crates/project/src/configuration.rs](https://github.com/CapSoftware/Cap/blob/main/crates/project/src/configuration.rs): transição de cena de 0,3 s, câmera 3D com fov 45 e tilt −28/26, molduras de janela e navegador, spring da tela com rigidez 200, amortecimento 40 e massa 2,25.
- HyperFrames 0.8.140 (registro local `~/.claude/plugins/cache/hyperframes/hyperframes/0.8.140/registry/components/`): `yt-screen-warp`, `split-tilt-cards`, `tilt-card`, `browser-device-stage`, `parallax-device-dive`, `device-frame-stage`, `hw-callout-circle`. Também `skills/product-launch-video/references/cut-catalog.md` e `motion-language.md`.

**Vídeos (medidos quadro a quadro aqui)**
- [ElevenLabs · Introducing Studio 3.0](https://www.youtube.com/watch?v=ZZSROGCVg9M): janela ~75 % com glow rosa, lista lateral, painel isolado ~1,6× e deslize de ~0,6 s.
- [Linear · Introducing Linear Initiatives](https://www.youtube.com/watch?v=FlDVDvzCmn0): janela ~84 % sobre cinza-claro e bolha redonda da câmera mordendo o canto.

**Tutoriais de After Effects (técnica de referência, sem números publicados)**
- [3 Modern Ways to Animate 3D SaaS Dashboards (Editing Snapped)](https://www.youtube.com/watch?v=STJLumt-yww)
- [3D Floating UI Animation (Motion Nations)](https://www.youtube.com/watch?v=ErdO0edE1Ig)
- [3D Product Pop Animation (Motion Nations)](https://www.youtube.com/watch?v=VOjo9HmjAa8)
- [SaaS Animation Tutorial (Motion Nations)](https://www.youtube.com/watch?v=T9l2o583sEU)
- [Master SaaS Motion Graphics in 30 Minutes (TomsProject)](https://www.youtube.com/watch?v=Jccbzpicst8)
- [I Recreated a Viral SaaS Animation (Mhd Labs)](https://www.youtube.com/watch?v=HpksVzegElQ)
- [The Full SaaS Animation Masterclass (Trim Studio)](https://www.youtube.com/watch?v=rCm0nyOOxh4)
- [SaaS Motion Graphics Full Tutorial – Appgen (Motion with Nas)](https://www.youtube.com/watch?v=vye0_xIG5HY)

**Guias e artigos**
- [Screen Studio · Look & Feel](https://screen.studio/guide/background): padding, inset, sombra, cantos.
- [Material Design · Duration & easing](https://m1.material.io/motion/duration-easing.html): transições grandes > 375 ms; emphasized de 400–500 ms.
- [Hera · UI animation video for software marketing](https://hera.video/blog/ui-animation-video-for-software-marketing): 3 rótulos por sequência; zoom em vez de interface inteira.
- [Clueso · tasteful screen recording videos](https://www.clueso.io/cluebooks/making-tasteful-screen-recording-videos--visual-framing-engagement): transições ≤ 0,3 s; margem de 10–12 % para texto.
- [TechSmith · annotate recordings](https://www.techsmith.com/blog/annotate-recorded-calls/): 5–8 palavras por anotação.
- [moonb.io · 12 product launch videos](https://www.moonb.io/blog/product-launch-video): formatos Linear, Warp, Raycast.
- [Hound Studio · 22 best product launch videos](https://hound-studio.com/blog/22-best-product-launch-videos-2026-examples-formulas): ElevenLabs e Google Workspace com rotações 3D de UI e glow.
- [Remotion · OffthreadVideo `transparent`](https://www.remotion.dev/docs/offthreadvideo): alfa em VP8, VP9 e ProRes.

**Estúdio (lido para não repetir)**
- `~/.claude/skills/edicao-video/SKILL.md`, `references/montagem-remotion.md`, `remotion/src/componentes.tsx`
- `~/.claude/skills/motion-design/reference/nivel.md` (itens 30–50), `tipografia-que-funciona.md`
- `~/.claude/skills/hierarquia-visual/SKILL.md`: zoom mínimo de UI = 30 px ÷ texto da UI.
- `projetos/<projeto>/v1/` (`ENTREGA.txt`, `remotion/src/Aula.tsx`, `fonte/frases-final.txt` e quadros de `aula-sla-v2.mp4` em 63, 136–160, 228–288 s)
