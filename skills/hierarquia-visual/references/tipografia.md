# Tipografia para vídeo (referência)

Pesquisa de 08/10/2026. Números resumidos em `tabela-numeros.md`; aqui está o porquê e o como fazer no HTML das cenas.

## 1. Escala: poucos degraus, saltos grandes

- Escalas modulares (https://typescale.com/): 1,125 · 1,2 · 1,25 · 1,333 · 1,414 · 1,5 · 1,618. Em UI de leitura longa usam-se as pequenas (1,2–1,25). **Em vídeo vertical, de relance, use 1,333–1,618**: com só 3 níveis, o salto tem que ser visível sem comparar.
- Refactoring UI faz escala à mão (12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72) — o ponto é ter **um conjunto fechado** e não inventar tamanho por elemento. No estúdio: defina 3 tamanhos por reel no `rNN-estilo.css` (ex.: `--t1:108px; --t2:56px; --t3:32px`) e não use outro.
- A ferramenta conta os "níveis" (tamanhos que diferem > 15%) fora de UI: mais de 3 = aviso. Nos reels testados, as cenas tinham 4–7 tamanhos (ex.: 108/69/47/36/26 px), sinal de tamanhos inventados por elemento.

Escalas prontas para o reel (1080×1920):
| Razão | Rótulo | Apoio | Subtítulo | Título | Título enorme |
|---|---|---|---|---|---|
| 1,333 | 32 | 42 | 56 | 75 → use 84+ | 100 / 133 |
| 1,5 | 30 | 44 | 66 | 100 | 150 |
| 1,618 | 32 | 52 | 84 | 136 | 220 |

## 2. Hierarquia sem só aumentar

Ordem de força (o que o olho pega primeiro): **movimento que começa > contraste de luminância > tamanho > cor saturada > peso > posição (topo-esquerda)**. Fontes: Abrams & Christ 2003 (início de movimento captura atenção); Treisman (cor/forma "saltam"); NN/g (leitura em camadas pelos títulos: https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/).

- "Emphasize by de-emphasizing" (Refactoring UI): antes de aumentar o título, **apague o resto** — apoio em peso 500 e cor de tinta secundária, rótulos menores.
- Peso: use 2 pesos por fonte (ex.: 800 título, 500–600 apoio). Peso < 400 some no vídeo comprimido e no celular.
- Cor do texto secundário: mesmo matiz do fundo, não cinza neutro (ver `cor.md`), e ainda ≥ 4,5:1.
- Um elemento só no nível 1 por tela. Dois títulos do mesmo tamanho = o olho não sabe onde começar.

## 3. Altura-x, peso e família

- Legibilidade em tamanho pequeno depende da **altura-x** (altura da minúscula), não do tamanho nominal. Tamanho crítico de leitura = 0,2° de altura-x (Legge & Bigelow 2011); a 30–35 cm isso dá 17–20 px de altura-x no reel.
- Fontes de altura-x grande (Inter, Figtree, Work Sans, Manrope ≈ 0,53–0,55 do corpo) leem melhor pequenas que serifas display (DM Serif, Instrument Serif ≈ 0,45) e que manuscritas (Caveat ≈ 0,40). **Regra:** serif display e manuscrita só em ≥ 56 px; rótulo e UI sempre em sans de altura-x grande ou mono.
- Condensadas (Bebas, Big Shoulders, Barlow Condensed, Anton): ótimas em título, ruins em frase. Em condensada, título ≥ 96 px.
- Serif itálica em sigla curta lê errado ("IA" vira "/A" — `armadilhas.md`).
- Números: mono ou `font-variant-numeric: tabular-nums` para contador que muda (não "dança").

## 4. Entrelinha

- Quanto maior a letra, menor a entrelinha: título display 0,90–1,05; subtítulo 1,05–1,15; frase 1,2–1,35 (Butterick: 1,20–1,45 para texto corrido; Apple Large Title 1,21; Material Display L 1,12).
- Título com entrelinha < 0,9 encosta acentos (Á, Ç) na linha de cima — confira em português.

## 5. Espacejamento (tracking)

- Display grande: −0,02 a −0,045 em (o estúdio usa −0,04 a −0,045 nos títulos grotescos). Inter recomenda −0,022 em a partir de ~32 px (fórmula dinâmica de rsms).
- Caixa-alta pequena (rótulo, "AGENDADO", "LINK NA BIO"): **+0,05 a +0,10 em** (Bringhurst 5–10%; Butterick 5–12%). Caixa-alta sem tracking positivo embola no celular.
- Mono: 0 a −0,01 em.

## 6. Comprimento de linha e quebra

- Título no reel: 2–4 palavras por linha, até 3 linhas, quebra **pelo sentido** com `<br>` (Netflix: depois de pontuação, antes de conjunção/preposição; nunca separar artigo do substantivo, nome do sobrenome).
- `text-wrap: balance` equilibra a largura das linhas (até 6 linhas no Chromium), mas não o sentido: use como rede de segurança, não como regra.
- Nunca deixe uma palavra sozinha na última linha de um título (viúva). Reescreva ou mude a quebra.
- Legenda queimada: ≤ 42 caracteres por linha, ≤ 2 linhas (Netflix).

## 7. Caixa e alinhamento

- Alinhamento à esquerda para frase (o olho volta sempre ao mesmo x); centralizado só para 1–2 linhas de impacto.
- Título em CAIXA-ALTA perde a silhueta das palavras: ok para 1–4 palavras, ruim para frase.
- Uma margem esquerda única por reel (o estúdio usa x = 80 em 1080): título, apoio e rótulo começam no mesmo x.

## 8. No HTML das cenas

```css
:root{ --t1:108px; --t2:56px; --t3:32px; }           /* 3 níveis, razão ~1,9 e ~1,75 */
.t1{font:800 var(--t1)/.95 var(--m-titulo);letter-spacing:-.04em}
.t2{font:600 var(--t2)/1.15 var(--m-ui);letter-spacing:-.01em;color:var(--tinta-2)}
.t3{font:700 var(--t3)/1.1 var(--m-ui);letter-spacing:.08em;text-transform:uppercase}
.t1,.t2{text-wrap:balance}
```
E confira: `node scripts/conferir_hierarquia.mjs fonte/NN-cena.html --fotos /tmp/hv` (a ferramenta mede o tamanho EFETIVO, já com câmera/scale).
