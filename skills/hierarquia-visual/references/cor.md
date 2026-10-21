# Cor e contraste em vídeo (referência)

Pesquisa de 08/10/2026. Números com fonte; o que é decisão do estúdio está marcado como **(estúdio)**.

## 1. Papéis de cor: fundo · tinta · UM destaque

Toda cena tem três papéis e só três:

| Papel | Área do quadro | Para quê |
|---|---|---|
| Fundo | ~60% | clima e significado (claro = "o sistema de sempre", escuro = noite/silêncio/oferta) |
| Tinta (texto e traço) | ~30% | ler; quase sempre neutra, do mesmo matiz do fundo puxado para o extremo |
| Destaque | ≤ 10% (no quadro inteiro, medido: 1–10%) | a UMA coisa que o olho tem que achar primeiro |

- A regra 60-30-10 vem da decoração de interiores e é regra prática, não ciência (https://paigebrunton.com/blog/60-30-10-color-rule-for-web-designers/). Use como teto do destaque, não como fórmula.
- **Por que um destaque só:** Treisman & Gelade (1980, Feature Integration Theory): alvo que difere por UM traço (cor) "salta" e o tempo de busca não depende do número de distratores; quando o alvo é conjunção de traços, a busca vira serial (https://en.wikipedia.org/wiki/Feature_integration_theory). Dois destaques = o olho tem que escolher = busca serial.
- **Efeito von Restorff (isolamento):** "o item que difere dos demais é o mais lembrado" (https://lawsofux.com/von-restorff-effect/). O destaque só funciona se for raro.
- **(estúdio)** O `conferir_hierarquia.mjs` mede as cores saturadas do quadro (OKLab, croma > 0,07, agrupadas por matiz): mais de 2 grupos que não são fundo = AVISO.

## 2. Como escolher o destaque

1. Comece pela marca (`--m-destaque`/`--m-cor`). Se a marca não tem, escolha o matiz **oposto** ao fundo no círculo (fundo frio → destaque quente), com croma alto.
2. O destaque precisa passar contraste com o fundo **como texto** (o destaque quase sempre vira palavra-chave): ≥ 3:1 se for palavra de título grande, ≥ 4,5:1 se for texto menor.
3. Destaque com a mesma luminância do fundo não "salta" para quem é daltônico: garanta diferença de **luminância** (Lc ≥ 30 entre destaque e fundo), não só de matiz.
4. Fundo colorido (amarelo, roxo) já é a cor forte da cena: aí o destaque é preto/branco ou um único segundo matiz em momento de virada (ex.: reel 10, amarelo → roxo só na virada).
5. Uma cor reservada por série tem um só significado (ex.: dourado = oferta; só no fecho).

## 3. Cor semântica

| Cor | Significa | Regra |
|---|---|---|
| Verde | ok / feito / positivo de verdade | só quando o estado é positivo (confirmado, pago); nunca como enfeite |
| Vermelho | erro / perda / alerta | não usar vermelho como destaque genérico ao lado de verde |
| Amarelo/âmbar | atenção / "olha aqui" | marca-texto, holofote |

- É convenção, não norma (não há fonte primária); por isso nunca dependa só da cor: **WCAG 1.4.1** — a cor não pode ser o único meio de passar a informação (https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). Some ✓/✕, palavra ou forma.
- A cor semântica **não conta** como segundo destaque, desde que apareça só no elemento de estado.

## 4. Daltonismo

- 1 em 12 homens (8%) e 1 em 200 mulheres (0,5%) têm deficiência de visão de cor; a mais comum dificulta separar vermelho de verde (NEI/NIH: https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness). Num anúncio para homens, ~1 em cada 12 espectadores.
- Regra: par vermelho × verde só com diferença de luminância visível (um claro, um escuro) **e** ícone/palavra junto. Teste rápido: dessature o quadro (preto e branco) — a hierarquia tem que continuar clara.

## 5. Texto secundário e cinzas (Refactoring UI)

- Hierarquia se faz com **peso e cor** antes de tamanho: "use weight and color instead of size" (Wathan & Schoger, https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886).
- Texto secundário em fundo **colorido**: não use cinza (fica "lavado"); use o mesmo matiz do fundo, mais claro ou mais escuro. Opacidade branca só em fundo liso; em foto/padrão falha.
- Em vídeo comprimido e tela de celular ao sol, o cinza "elegante" some: texto secundário ≥ 4,5:1 e Lc ≥ 60 (ver tabela).

## 6. Contraste: WCAG 2.2 e APCA

### WCAG 2.2 (norma em vigor)
| Critério | Exigência |
|---|---|
| 1.4.3 AA texto normal | ≥ 4,5:1 |
| 1.4.3 AA texto grande (≥ 24 px CSS, ou ≥ 18,66 px negrito) | ≥ 3:1 |
| 1.4.6 AAA | 7:1 normal / 4,5:1 grande |
| 1.4.11 não texto (ícone, borda de botão, linha de gráfico) | ≥ 3:1 contra a cor vizinha |

Fonte: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — "14pt and 18pt are equivalent to approximately 18.5px and 24px". O 4,5 vem de compensar acuidade 20/40 (3 × 1,5).

Fórmula: canal/255 → `c ≤ 0,04045 ? c/12,92 : ((c+0,055)/1,055)^2,4`; L = 0,2126 R + 0,7152 G + 0,0722 B; razão = (L1+0,05)/(L2+0,05).

**Conversão para o vídeo em pé (estúdio):** 1080 px de vídeo ocupam ~393 pt de largura num celular comum → 1 px do vídeo ≈ 0,364 pt. "Texto grande" da WCAG (24 px CSS) = **66 px** no quadro 1080×1920; negrito 18,66 px = **51 px**.

### APCA (rascunho do WCAG 3; versão 0.0.98G-4g, código apca-w3)
Mede contraste **perceptual** (leva em conta polaridade e o tamanho/peso da fonte). Resultado Lc de 0 a ~106 (positivo = texto escuro em fundo claro; negativo = claro no escuro; use o valor absoluto).

| Lc | Uso (APCA in a Nutshell) | Em px CSS | No reel 1080 (÷ 0,364) |
|---|---|---|---|
| 90 | preferido para corpo de texto | ≥ 14 px/400 | — |
| 75 | mínimo para texto corrido (frase) | 18 px/400 · 16/500 · 14/700 | 50 px/400 · 44/500 · 39/700 |
| 60 | texto que não é corrido (rótulo, título médio) | 24 px/400 · 21/500 · 18/600 · 16/700 | 66 px/400 · 58/500 · 49/600 · 44/700 |
| 45 | títulos grandes | 36 px/400 · 24 px/700 | 99 px/400 · 66 px/700 |
| 30 | mínimo absoluto para texto "de relance" | — | — |
| 15 | mínimo para não texto (forma) | — | — |

Fontes: https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html · código e constantes: https://github.com/Myndex/apca-w3 (src/apca-w3.js) · Bronze Simple Mode: https://readtech.org/ARC/tests/bronze-simple-mode/?tn=criterion (teto: Lc 90 para texto grande muito claro em fundo escuro — branco puro gigante em preto puro "estoura"; use #F2–F5 no texto).

Fórmula (implementada em `scripts/conferir_hierarquia.mjs`, conferida com os valores de referência: preto/branco = 106,04; branco/preto = −107,88; #888/branco = 63,06):
```
Y = 0.2126729·(R/255)^2.4 + 0.7151522·(G/255)^2.4 + 0.0721750·(B/255)^2.4   (sem linearização por partes)
Y < 0.022 → Y += (0.022 − Y)^1.414
fundo mais claro: S = (Yf^0.56 − Yt^0.57)·1.14 ; Lc = S < 0.1 ? 0 : (S − 0.027)·100
fundo mais escuro: S = (Yf^0.65 − Yt^0.62)·1.14 ; Lc = S > −0.1 ? 0 : (S + 0.027)·100
```

### Por que medir pelos pixels (e não pelo CSS)
Em vídeo o texto passa por cima de degradê em malha, foto, grão, vidro e brilho. A cor "de fundo" do CSS mente. A ferramenta fotografa o quadro duas vezes (com o texto e com o texto apagado) e compara a tinta com o fundo **atrás de cada letra**; também mede o desvio do fundo (fundo agitado = AVISO, mostra o pior trecho).

## 7. Texto sobre imagem/vídeo
- Meça contra o trecho mais claro do fundo (texto claro) ou o mais escuro (texto escuro), não a média.
- Soluções em ordem de preferência: mover o texto para área lisa → escurecer/clarear a região com degradê (scrim) de 40–60% → caixa sólida atrás (pílula/tarja) → sombra suave grande (não contorno duro).
