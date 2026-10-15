# Tabela de números do estúdio (com fontes)

Pesquisa de 2026-10-08. Os números marcados **(estúdio)** são decisão nossa, tirada da conta ao lado; o resto vem da fonte citada. A ferramenta `scripts/conferir_hierarquia.mjs` usa exatamente estes valores (objeto `PERFIS` e `ZONAS` no topo do arquivo).

## 0. A conversão que manda em tudo

| Como o vídeo é visto | 1 pt do celular = | 1 px do vídeo = | Fonte da conta |
|---|---|---|---|
| Reel 1080×1920 ocupando a largura de um celular de 393 pt (iPhone 15/16, 6,1") | 2,75 px | 0,364 pt | 1080 ÷ 393 (Apple: 393×852 pt) |
| Reel com o app preenchendo a altura (corta ~97 px de cada lado) | 2,25 px | 0,44 pt | 1920 ÷ 852 |
| VSL 1920×1080, celular deitado, tela cheia | 2,25 px | 0,44 pt | 1920 ÷ 852 |
| VSL 1920×1080 dentro de página/feed, celular em pé | 4,9 px | 0,20 pt | 1920 ÷ 393 |

Consequência: **uma VSL deitada vista no celular em pé precisa de letra ~1,8× maior que um reel** para ter o mesmo tamanho físico. E todo número de UI/web ("16 px", "11 pt") tem que ser multiplicado por 2,75 no reel.

## 1. Tamanho de texto (px do palco, já com a escala dos transforms)

| Nível | 1080×1920 (reel) | 1920×1080 (tela cheia) | 1920×1080 no feed em pé | Por quê |
|---|---|---|---|---|
| **Título** (nível 1) | mín. **84**, recomendado 96–160 | mín. 72, rec. 96–140 | mín. 150 | Large Title da Apple = 34 pt = 93 px no reel; 84 px já era a regra do estúdio (ESTILOS.md) |
| **Subtítulo** (nível 2) | 56–72 | 48–64 | 100–130 | razão ≥ 1,5 em relação ao título |
| **Apoio / frase** (≥ 4 palavras) | mín. **40**, rec. **44–60** | mín. 36, rec. 40–52 | mín. 72 | 16–22 pt no celular; corpo da Apple = 17 pt = 47 px |
| **Rótulo / etiqueta** (≤ 3 palavras) | mín. **30**, rec. 32–40 | mín. 26 | mín. 54 | 11 pt = mínimo da Apple HIG = 30 px no reel |
| **Texto de UI que a fala cita** | ≥ **30** efetivo (zoom 1,3–1,5 numa UI de 20–23 px) | ≥ 26 | ≥ 54 | idem; UI web de 14–16 px gravada a 100% vira 5–7 pt no celular |
| **Texto de UI de fundo** (textura, ninguém precisa ler) | sem mínimo | — | — | mas não pode competir com o título |

Fontes: Apple HIG Typography (iOS: corpo 17 pt, mínimo 11 pt, Large Title 34 pt) https://developer.apple.com/design/human-interface-guidelines/typography · Material 3 type scale (Display L 57, Headline L 32, Body L 16, Label S 11 sp) https://raw.githubusercontent.com/material-components/material-web/main/tokens/versions/v0_192/_md-sys-typescale.scss · Legge & Bigelow 2011, "Does print size matter for reading?" (tamanho crítico = 0,2° de altura-x; fluente de 0,2° a 2°) https://legge.dl8.umn.edu/sites/legge.psych.umn.edu/files/2020-08/Legge%20Bigelow%202011%20Does%20size%20matter%20for%20reading%3F%20A%20review%20of%20findings%20from%20vision%20science%20and%20typography.pdf

Conta do piso físico (Legge & Bigelow): a 30–35 cm, 0,2° de altura-x = 1,05–1,22 mm = 17–20 px de altura-x no reel → fonte com altura-x ~0,55 (Inter) ≈ **32–37 px**. É o piso para texto PARADO com tempo; para leitura de relance use 2–3× (≈ 65–110 px) **(estúdio, inferência)**. Por isso: rótulo 30 px só para 1–3 palavras; frase ≥ 44 px.

## 2. Hierarquia entre níveis

| Regra | Número | Fonte |
|---|---|---|
| Razão título ÷ apoio | **≥ 1,5** (falha da ferramenta); recomendado ≥ 2 | prática de escala modular (1,25 por degrau × 2 degraus ≈ 1,5; Perfect Fifth = 1,5) — https://typescale.com/ · **(estúdio)** ≥ 2 no celular sem som |
| Níveis de tamanho fora de UI na mesma tela | **≤ 3** | **(estúdio)**: título + apoio + rótulo |
| Blocos no nível 1 | **1** (no máx. 2 se formam uma frase) | Treisman (busca pop-out) — ver cor.md |
| Escala sugerida no reel | 1,5 a partir de 40: **40 / 60 / 90 / 135** (ou 1,333: 42 / 56 / 75 / 100 / 133) | https://typescale.com/ |

## 3. Peso, entrelinha, espacejamento

| Nível | Peso | Entrelinha (line-height) | Tracking (letter-spacing) |
|---|---|---|---|
| Título display (≥ 84 px) | 700–900 (grotesca) ou 400 (serif display) | **0,90–1,05** | **−0,02 a −0,045 em** |
| Subtítulo | 600–800 | 1,05–1,15 | −0,01 a −0,03 em |
| Apoio / frase | 500–600 (nunca < 400 em vídeo) | **1,2–1,35** | 0 a −0,01 em |
| Rótulo em CAIXA-ALTA | 600–700 | 1,0–1,2 | **+0,05 a +0,10 em** |
| Número/mono | 500–600, algarismos tabulares | 1,0 | 0 a −0,01 em |

Fontes: Butterick, entrelinha ótima de texto corrido 120–145% https://practicaltypography.com/line-spacing.html · Apple: Large Title 34/41 (1,21), Body 17/22 (1,29) · Material: Display L 57/64 (1,12) · caixa-alta 5–10% (Bringhurst via https://webtypography.net.clagnut.com/2.1.6; Butterick 5–12% https://practicaltypography.com/letterspacing.html) · Inter: tracking dinâmico −0,022 em a partir de ~32 px (https://d.rsms.me/inter-website/v3/dynmetrics/) · Refactoring UI: não usar peso < 400 em texto de interface.

## 4. Linha e quebra

| Regra | Número | Fonte |
|---|---|---|
| Título no reel | **2–4 palavras por linha, até 3 linhas** | **(estúdio)**, da largura útil de ~950 px |
| Palavras no nível 1 | **≤ 6** (ideal 3–4) | estúdio (`nivel.md` item 25) |
| Legenda | ≤ 42 caracteres por linha, ≤ 2 linhas | Netflix https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617 |
| Texto corrido (raro em vídeo) | 45–75 caracteres por linha (66 ideal) | Bringhurst https://webtypography.net/2.1.2 |
| Largura máxima de legenda em 16:9 | 68% da largura (~1300 px em 1920) | BBC (via https://clevercast.com/bbc-subtitling-guidelines; fonte primária bloqueada) |
| Quebra | depois de pontuação; antes de conjunção/preposição; nunca separar artigo+substantivo, nome+sobrenome, pronome+verbo | Netflix (regras gerais) |
| `text-wrap: balance` | vale até 6 linhas no Chromium | MDN https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap |

## 5. Contraste

| Texto | WCAG 2.2 (falha abaixo) | APCA Lc (aviso abaixo) |
|---|---|---|
| Normal (< 66 px no reel; < 51 px se negrito ≥ 600) | **4,5:1** | 75 se for frase (≥ 4 palavras); 60 se rótulo |
| Grande (≥ 66 px, ou ≥ 51 px negrito) | **3:1** | 60 |
| Enorme (≥ 99 px regular ou ≥ 66 px peso 700+) | 3:1 | 45 |
| Não texto (ícone, linha de gráfico, borda) | 3:1 | 15–30 |
| Recomendado para vídeo comprimido / tela ao sol **(estúdio)** | **7:1** em apoio | 90 em apoio |

16:9 tela cheia: grande = 54 px (42 negrito). 16:9 no feed: 118 px (91 negrito).
Fontes: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html · https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html · detalhes em `cor.md`.

## 6. Zona segura e margens

| Formato | Livre (x × y) em px | Fonte |
|---|---|---|
| Reels orgânico (estúdio) | y 220–1540; coluna de botões x > 930 a partir de y 700; margem lateral 60 | `kit/zona-segura.png` |
| Reels/Stories **anúncio** (Meta) | 14% topo, 35% base, 6% lados → **x 65–1015, y 269–1248** | https://www.facebook.com/business/ads-guide/update/video/instagram-reels |
| TikTok orgânico | topo 108, base 320, esq. 60, dir. 120 → x 60–960, y 108–1600 | terceiros (TikTok não publica em texto): https://www.upload-post.com/tools/safe-zone-checker/ |
| YouTube Shorts | topo 288, base 672, esq. 48, dir. 192 → x 48–888, y 288–1248 | imagem do Google https://support.google.com/google-ads/answer/9128498 (lida por terceiros) |
| **Uma peça para as três** | **x 65–888, y 288–1248** | pior caso de cada lado (inferência) |
| 16:9 (VSL, aula) | grafismo: 5% de cada lado = **96 px / 54 px** em 1080p (192/108 em 4K); ação 3,5% = 67/38 px | EBU R95 https://tech.ebu.ch/docs/r/r095.pdf · SMPTE ST 2046-1 (90%/93%) |

Na ferramenta: `--zona reels` (padrão no em pé), `reels-anuncio`, `tiktok`, `shorts`, `todas`, `titulo` (padrão no deitado), `nenhuma`.

## 7. Leitura e tempo

| Regra | Número | Fonte |
|---|---|---|
| Tempo mínimo de um texto na tela | **máx(1,0 s; 0,5 s + 0,33 s × palavras)** | **(estúdio)**: BBC 0,33 s/palavra + 0,5 s para achar o texto; nunca menos que 0,83 s (Netflix) |
| Texto legal / oferta em anúncio sem som | 0,2 s × palavras + 2 s (até 9 palavras); + 3 s (10+) | Clearcast https://help.clearcast.co.uk/en/article/legal-supers-our-helpful-tools |
| Velocidade de leitura PT-BR | ~180 palavras/min (~3 palavras/s); 17 caracteres/s em legenda | Messias et al. 2008 (IReST PT-BR) https://aboonline.org.br/details/1379/en-US · Netflix PT-BR https://partnerhelp.netflixstudios.com/hc/en-us/articles/215600497 |
| Duração máxima de uma legenda | 7 s | Netflix |
| Palavras fora de UI na tela ao mesmo tempo | ideal **≤ 15** (aviso), **> 25 = falha**; título ≤ 6 | **(estúdio)**: 2 linhas Netflix ≈ 14 palavras |
| Gancho | legível no quadro 0, em ≤ 1,5 s | `inspiracao.md` |

## 8. Espaço e grade

| Regra | Número | Fonte |
|---|---|---|
| Unidade de grade | 8 pt → **24 px no reel** (múltiplos: 24/48/72/96) ; 16:9: 8 px × 2,25 ≈ 18 → use 20/40/80 | Material 8 dp; conversão (estúdio) |
| Espaço dentro do grupo ÷ entre grupos | **≤ 1 : 2** | Gestalt de proximidade (NN/g https://www.nngroup.com/videos/proximity-gestalt/); razão = prática |
| Margem lateral no reel | ≥ 65 px (6%); título alinhado a 80 px é o padrão do estúdio | Meta |
| Espaço negativo | ≥ 40% do quadro sem elemento em cena de frase de impacto **(estúdio)** | contenção (`inspiracao.md`) |

## 9. Cor

| Regra | Número |
|---|---|
| Papéis | fundo ~60% · tinta ~30% · **1 destaque ≤ 10%** da área |
| Cores de destaque (matizes saturados que não são o fundo) por quadro | **1** (+ no máx. 1 semântica) — mais de 2 = aviso |
| Destaque × fundo | ≥ 3:1 (ou ≥ 4,5:1 se o destaque vira texto pequeno) |
| Vermelho × verde | só com diferença de luminância + ícone/palavra (8% dos homens são daltônicos) |
Detalhes e fontes: `cor.md`.

## 10. Movimento como nível de hierarquia

| Regra | Número | Fonte |
|---|---|---|
| O que puxa o olho é o **início** do movimento, não o movimento contínuo | 1 entrada por vez no ponto que importa | Abrams & Christ 2003 https://pubmed.ncbi.nlm.nih.gov/12930472/ |
| Entrada de texto | 300–600 ms com desaceleração (M3 emphasizedDecelerate `cubic-bezier(.05,.7,.1,1)`) | Material 3 https://m3.material.io/styles/motion/easing-and-duration/tokens-specs |
| Saída | 150–250 ms com aceleração (`cubic-bezier(.3,0,.8,.15)`) | Material 3 |
| Escalonamento palavra a palavra | 30–90 ms entre itens, ≤ 8 itens (o kit usa 90 ms) | prática; `comum.js palavras()` |
| Flashes | ≤ 3 por segundo | WCAG 2.3.1 |
