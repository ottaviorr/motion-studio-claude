# Leitura em vídeo: celular, sem som, de relance (referência)

Pesquisa de 2026-10-08.

## 1. O espectador do estúdio

- Celular em pé, a 30–40 cm, rolando o feed, **muitas vezes sem som**. Decide em ~1,5 s se fica (`inspiracao.md`).
- Não controla o tempo: o texto some quando a cena quer. Por isso tempo de exposição é regra, não detalhe.
- A tela do celular encolhe o vídeo: 1 px do reel ≈ 0,364 pt (ver `tabela-numeros.md` §0). O que parece grande no monitor de 27" é pequeno no celular. **Confira sempre no tamanho do celular** (folha de fotos em 360 px de largura ≈ tamanho real).

## 2. Quanto tempo um texto precisa ficar

| Base | Número | Fonte |
|---|---|---|
| Leitura silenciosa PT-BR | ~180 palavras/min ≈ 3 palavras/s (6,1 letras por palavra) | Messias et al. 2008, IReST PT-BR https://aboonline.org.br/details/1379/en-US |
| Inglês (meta-análise, 190 estudos) | 238 palavras/min não-ficção | Brysbaert 2019 https://www.bps.org.uk/research-digest/most-comprehensive-review-date-finds-average-persons-reading-speed-slower |
| Legenda PT-BR adulto | até 17 caracteres/s | Netflix PT-BR https://partnerhelp.netflixstudios.com/hc/en-us/articles/215600497 |
| Legenda: mínimo / máximo | 5/6 s (0,833 s) / 7 s por evento; ≤ 2 linhas; 42 caracteres/linha | Netflix regras gerais https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617 |
| BBC | 160–180 palavras/min; ~0,33 s por palavra | BBC Subtitle Guidelines (via https://clevercast.com/bbc-subtitling-guidelines) |
| Texto de anúncio (legal) | 0,2 s/palavra + 2 s de reconhecimento (≤ 9 palavras); + 3 s (10+) | Clearcast https://help.clearcast.co.uk/en/article/legal-supers-our-helpful-tools |
| "Deixe ler duas vezes" | prática de pós-produção | https://www.ssw.com.au/rules/post-production-do-you-give-enough-time-to-read-texts-in-your-videos |

**Regra do estúdio (a ferramenta usa):** tempo mínimo = **máx(1,0 s; 0,5 s + 0,33 s × palavras)**.
- 1 palavra: 1,0 s · 3 palavras: 1,5 s · 4: 1,8 s · 6: 2,5 s · 10: 3,8 s.
- O 0,5 s é o tempo de achar o texto na tela (o olho chega depois do corte). Com narração que diz a mesma frase, o mínimo cai na prática, mas o estúdio mira o espectador sem som.
- Texto de oferta/legal (preço, "14 dias grátis", condição): use a regra da Clearcast (≥ 2 s + 0,2 s/palavra).
- Palavra que entra palavra a palavra conta a partir da 1ª palavra; o texto inteiro precisa de pelo menos 0,5 s **completo** antes de sair.
- Contador/relógio que gira não precisa do mínimo em cada número — só o número final.

## 3. Quanto texto por tela

- Uma ideia por tela; título com **3–4 palavras** (máx. 6). Total fora de UI: ideal ≤ 15 palavras visíveis ao mesmo tempo (≈ 2 linhas de legenda), mais de 25 é falha.
- Legenda queimada + título ao mesmo tempo: a legenda já é o texto da fala; o título vira 1–3 palavras-chave, não repete a frase.
- UI de produto pode ter muitas palavras (é cenário), desde que o olho seja levado para UM ponto (zoom, holofote, destaque) e o resto fique visivelmente secundário.

## 4. O que o olho lê primeiro (e como usar)

1. **Movimento que começa.** Abrams & Christ (2003): o início do movimento captura a atenção; o movimento contínuo não (https://pubmed.ncbi.nlm.nih.gov/12930472/). Em vídeo, o olhar de várias pessoas converge onde há movimento ("sincronia atencional", Smith & Mital 2013, https://dx.doi.org/10.1167/12.13.3).
   → Faça **uma** coisa começar a se mexer onde você quer o olho; o resto fica parado. Loop decorativo (flutuar, girar) para de puxar e só cansa.
2. **Rosto.** Em gravação com pessoa, o olho vai ao rosto/boca; texto perto do rosto (sem cobrir) é lido mais rápido do que no canto oposto.
3. **Contraste de luminância e tamanho.** O maior e mais contrastado lê primeiro.
4. **Cor isolada** (um destaque único salta — Treisman).
5. **Posição.** Sem outros sinais, topo-esquerda primeiro (padrão F/camadas, NN/g). No reel, o topo (y 250–600) é onde o título mora.

Ordem de entrada = ordem de leitura: entre o título primeiro, o apoio 0,2–0,4 s depois, o detalhe por último. Nunca tudo ao mesmo tempo.

## 5. Movimento como nível de hierarquia

- Nível 1 entra com o movimento mais forte (escala + deslocamento, 400–600 ms, desaceleração). Nível 2 entra com movimento menor (só deslocamento/opacidade, 300–400 ms). Rótulos aparecem quase parados (opacidade 200 ms).
- **Destino comum (Gestalt):** itens que se movem juntos são lidos como um grupo (https://learninglink.oup.com/public/files/cdn/wolfe4e/wa04.01.html). Os itens de uma lista entram com a mesma direção e curva; o item que deve se destacar entra diferente (von Restorff).
- Câmera que aproxima = "olhe aqui" (holofote natural). A ferramenta trata texto em movimento como transição (não reprova tamanho no meio do zoom), mas o quadro **parado** depois do zoom tem que passar.
- Durações de vídeo podem ser 1,5–2× as de UI (o espectador não clicou em nada): entrada 400–800 ms, saída 200–300 ms (Material 3: emphasized 500 ms; entrada 400 ms; saída 200 ms — https://m3.material.io/styles/motion/easing-and-duration/tokens-specs).
- ≤ 3 flashes por segundo (WCAG 2.3.1).

## 6. UI de produto mostrada no vídeo

- UI web real tem texto de 12–16 px. Num reel de 1080, a janela de 1600 px inteira reduzida a ~1000 px deixa o texto com 8–10 px = **ilegível** (3–4 pt).
- Zoom mínimo para ler: **30 px ÷ tamanho do texto da UI**. UI de 20–23 px (kit de telas) → zoom **1,3–1,5×** (a regra que já estava no ESTILOS.md agora tem a conta). UI de 14 px → 2,1×.
- Janela inteira só por um instante (< 1 s, como "mapa"); depois a câmera vai ao ponto que a fala cita.
- Reconstrua em camadas e escale a região, em vez de print parado (`inspiracao.md`). Em 16:9 no feed em pé, UI ≥ 54 px efetivos (zoom 2,5–4×).
- A ferramenta avisa: "UI em 19 px < 30 px: se a fala cita este texto, aproxime 1,58× ou mais".

## 7. Grid, margens e espaço negativo

- Reel: margem esquerda única (80 px no estúdio), lateral ≥ 65 px; grade de 24 px (8 pt × 2,75 ≈ 22 → 24).
- 16:9: grafismo dentro de 96 px / 54 px das bordas (EBU R95, 5%). Legenda ≤ 68% da largura.
- Proximidade: espaço dentro do grupo ≤ metade do espaço entre grupos (título+apoio colados, distantes da UI).
- Região comum: um fundo/cartão compartilhado agrupa mais forte que a proximidade (https://www.nngroup.com/articles/common-region/).
- Espaço negativo é o que deixa o título ser o nível 1: em frase de impacto, ≥ 40% do quadro vazio.
