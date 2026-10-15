---
name: hierarquia-visual
description: Regras em números de hierarquia visual para vídeo (reels 9:16 1080×1920 vistos no celular sem som, VSLs e aulas 16:9) — tamanho de título/apoio/rótulo em px, peso, entrelinha, tracking, contraste WCAG e APCA, um destaque de cor, zona segura do Reels/TikTok/Shorts, margens, tempo de leitura por palavra, máximo de palavras por tela e zoom mínimo de interface — mais uma ferramenta que mede tudo isso automaticamente numa cena HTML. Use SEMPRE que for criar ou revisar uma cena, reel, anúncio, VSL, capa, legenda ou motion com texto; quando alguém disser "não dá pra ler", "letra pequena", "tá poluído", "tá tudo do mesmo tamanho", "o olho não sabe onde olhar", "a cor não destaca", "fica embaixo dos botões do Instagram", "texto passa rápido demais", "qual tamanho de fonte usar", "qual cor de destaque", "contraste"; e antes de gravar qualquer cena da skill motion-design — mesmo que ninguém fale em "hierarquia".
---

# Hierarquia visual (números do estúdio)

Hierarquia é a ordem em que o olho lê a tela. Em vídeo vertical isso decide tudo: o espectador está no celular, a 30–40 cm, rolando o feed, muitas vezes sem som, e não pode pausar. Se o olho não acha o título em meio segundo, ele rola. Esta skill dá os números que garantem essa ordem e uma ferramenta que confere a cena pronta.

Use junto com a skill **motion-design** (que faz as cenas): esta decide tamanho, cor e espaço; aquela decide movimento e montagem.

## A conta que muda tudo

Um reel de 1080 px de largura aparece num celular de ~393 pt de largura: **1 pt do celular = 2,75 px do vídeo**. Todo número de interface precisa ser multiplicado:

- 11 pt (o mínimo da Apple) = **30 px** no reel. Corpo de texto (17 pt) = 47 px. Large Title (34 pt) = 93 px.
- VSL 1920×1080 vista no celular **em pé** (dentro de página/feed): 1 pt = 4,9 px, ou seja, letra ~1,8× maior que no reel.
- UI web de 14–16 px mostrada a 100% vira 5–7 pt no celular = ilegível.

Por isso o monitor engana: confira sempre no tamanho do celular (a folha de fotos a 360 px de largura ≈ tamanho real).

## Como montar a hierarquia de uma cena (nesta ordem)

1. **Escreva a frase da tela antes de desenhar.** Uma ideia por tela. Título com 3–4 palavras (máx. 6). Se precisa de mais, é a fala ou outra cena.
2. **Escolha o nível 1 — um só.** É o que o espectador tem que ler se ler só uma coisa. Todo o resto existe para apoiar.
3. **Defina 3 tamanhos para o vídeo inteiro** (título, apoio, rótulo) numa escala de razão 1,333–1,618. Ponha no `rNN-estilo.css` como `--t1/--t2/--t3` e não invente tamanho por elemento. Razão título ÷ apoio ≥ 1,5 (melhor ≥ 2).
4. **Rebaixe antes de aumentar.** Apoio em peso 500–600 e tinta secundária; rótulo pequeno em caixa-alta com tracking positivo. Só depois aumente o título, se ainda precisar.
5. **Pinte: fundo · tinta · UM destaque.** O destaque vai só na coisa do nível 1 (ou na palavra-chave dele). Cor semântica (verde = ok) só no elemento de estado.
6. **Posicione na zona segura** e numa margem esquerda única (80 px no reel). Título no terço de cima (y 250–600); nada importante abaixo de y 1248 em anúncio, nem sobre a coluna de botões.
7. **Dê espaço.** Título e apoio colados (mesmo grupo), longe do resto (espaço entre grupos ≥ 2× o de dentro). Em frase de impacto, ≥ 40% do quadro vazio.
8. **Ordene a entrada.** O que entra primeiro é lido primeiro: nível 1, depois apoio (0,2–0,4 s depois), depois detalhe. O início de um movimento puxa o olho; só uma coisa começa a se mexer por vez no ponto que importa.
9. **Segure o tempo de leitura.** Cada texto fica pelo menos máx(1 s; 0,5 s + 0,33 s × palavras).
10. **Rode a ferramenta** e corrija o que falhar antes de gravar.

## TABELA DE NÚMEROS

Px = pixels do palco, já com a escala dos transforms (câmera, `scale`). Fontes e contas em `references/tabela-numeros.md`.

### Tamanho, peso, entrelinha e tracking

| Nível | Reel 1080×1920 | 16:9 tela cheia 1920×1080 | 16:9 no feed em pé | Peso | Entrelinha | Tracking |
|---|---|---|---|---|---|---|
| Título (nível 1) | mín. **84**, rec. 96–160 | mín. 72, rec. 96–140 | mín. 150 | 700–900 (serif display: 400) | 0,90–1,05 | −0,02 a −0,045 em |
| Subtítulo | 56–72 | 48–64 | 100–130 | 600–800 | 1,05–1,15 | −0,01 a −0,03 em |
| Apoio / frase (4+ palavras) | mín. **40**, rec. **44–60** | mín. 36, rec. 40–52 | mín. 72 | 500–600 | 1,2–1,35 | 0 a −0,01 em |
| Rótulo (≤ 3 palavras) | mín. **30**, rec. 32–40 | mín. 26 | mín. 54 | 600–700 | 1,0–1,2 | caixa-alta: +0,05 a +0,10 em |
| UI que a fala cita | ≥ **30** efetivo | ≥ 26 | ≥ 54 | — | — | — |

- Serif display e manuscrita só a partir de 56 px (altura-x pequena). Condensada só em título ≥ 96 px. Nunca peso < 400.
- Título: 2–4 palavras por linha, até 3 linhas, quebra pelo sentido (`<br>`), sem palavra sozinha na última linha. `text-wrap: balance` como rede.
- No máximo **3 tamanhos** de texto fora de UI na mesma tela.

### Contraste (medido no pixel, atrás de cada letra)

| Texto | WCAG 2.2 mínimo | APCA Lc mínimo |
|---|---|---|
| Normal (reel < 66 px; < 51 px se peso ≥ 600) | **4,5:1** | 75 frase · 60 rótulo |
| Grande (reel ≥ 66 px, ou ≥ 51 px negrito) | **3:1** | 60 |
| Enorme (reel ≥ 99 px, ou ≥ 66 px peso 700+) | 3:1 | 45 |
| Ícone, linha de gráfico, borda de botão | 3:1 | 15–30 |
| Meta do estúdio para apoio (vídeo comprimido, sol na tela) | 7:1 | 90 |

16:9 tela cheia: "grande" = 54 px (42 negrito). 16:9 no feed: 118 px (91 negrito). Branco puro gigante em preto puro "estoura" (APCA: teto Lc 90 em texto grande): use tinta #F2–#F5.

### Espaço, zona segura e margens

| Formato | Área livre para texto importante |
|---|---|
| Reels orgânico (`kit/zona-segura.png`) | y 220–1540, x 60–1020; nada em x > 930 a partir de y 700 (botões) |
| Reels/Stories anúncio (Meta: 14% topo, 35% base, 6% lados) | **x 65–1015, y 269–1248** |
| TikTok orgânico | x 60–960, y 108–1600 |
| YouTube Shorts | x 48–888, y 288–1248 |
| Uma peça para as três | **x 65–888, y 288–1248** |
| 16:9 (EBU R95, grafismo 5%) | 96 px dos lados, 54 px em cima/embaixo (4K: 192/108) |

Grade: 24 px no reel (8 pt × 2,75). Margem esquerda única. Dentro do grupo ≤ ½ do espaço entre grupos.

### Leitura e quantidade

| Regra | Número |
|---|---|
| Tempo mínimo de cada texto | **máx(1,0 s; 0,5 s + 0,33 s × palavras)** — 1 palavra 1,0 s · 3 → 1,5 s · 6 → 2,5 s |
| Texto de oferta/condição em anúncio | ≥ 2 s + 0,2 s × palavras (Clearcast) |
| Palavras no título | 3–4 (máx. 6) |
| Palavras fora de UI na tela ao mesmo tempo | ideal ≤ 15; > 25 = falha |
| Legenda queimada | ≤ 42 caracteres/linha, ≤ 2 linhas, ≥ 0,83 s, ≤ 7 s |
| Zoom mínimo de UI | **30 px ÷ tamanho do texto da UI** (UI de 20–23 px → 1,3–1,5×; 14 px → 2,1×). Janela inteira só por < 1 s |

## Regras de cor

**Três papéis, só três:** fundo (~60% do quadro, dá o clima) · tinta (~30%, para ler) · **um destaque** (≤ 10% da área). Por quê: um alvo que difere por uma só cor "salta" sem o olho procurar (Treisman); dois destaques viram busca, e o item diferente só é lembrado se for raro (von Restorff).

**Como escolher o destaque:**
1. Da marca, se existir (`--m-destaque`). Se não: matiz oposto à temperatura do fundo (fundo frio → destaque quente), croma alto.
2. Precisa passar contraste **como texto** sobre o fundo (≥ 3:1 em palavra de título; ≥ 4,5:1 se vira texto menor).
3. Diferença de **luminância**, não só de matiz, para quem é daltônico (1 em 12 homens). Teste: veja o quadro em preto e branco — a hierarquia continua?
4. Fundo já saturado (amarelo, roxo): o destaque vira preto/branco, ou um segundo matiz só no momento de virada.
5. Cor reservada tem um significado só por série (ex.: dourado = oferta, só no fecho).

**Cores semânticas:** verde = ok/positivo de verdade · vermelho = erro/perda · amarelo = atenção. Não contam como segundo destaque se ficam só no elemento de estado. Nunca só a cor: some ✓/✕ ou a palavra (WCAG 1.4.1). Vermelho × verde lado a lado só com diferença de luminância + ícone.

**Texto secundário:** mesmo matiz do fundo (mais claro/escuro), não cinza neutro em fundo colorido; e ainda ≥ 4,5:1. Texto sobre foto/vídeo: mova para área lisa → degradê (scrim) 40–60% → tarja sólida → sombra suave grande.

Detalhes: `references/cor.md`.

## Ferramenta: `scripts/conferir_hierarquia.mjs`

**Antes de rodar, marque o que é réplica de interface.** Telas do kit (`.lu-win`, `.lu-cel`…) já contam como UI. Qualquer réplica feita à mão na cena (formulário, ficha de contato, cupom, painel) leva `data-hv="ui"` no contêiner — senão cada rótulo de 20 px de dentro dela vira FALHA de "texto de leitura" e o relatório vira ruído (no reel 09 aprovado: 35 falhas, quase todas rótulos do formulário de mentira). Texto decorativo (marca-d'água, textura de letras): `data-hv="ignorar"`. FALHA que sobra depois disso é para corrigir.

Abre a cena no Chrome do computador (mesmo padrão do `kit/gravar.mjs`), chama `frame(t)` e mede pelo DOM e pela imagem:
- tamanho **efetivo** de cada texto (font-size × escala acumulada de `transform`, `scale`, `zoom` e SVG);
- contraste WCAG e APCA com o fundo **atrás de cada letra** (fotografa com o texto e com o texto apagado; acusa fundo agitado);
- texto fora da zona segura ou em cima dos botões; níveis de tamanho e razão título:apoio; palavras na tela; cores de destaque no quadro;
- **tempo de exposição** de cada texto (varre a cena a cada 0,1 s);
- texto em movimento (zoom/passagem) ou com opacidade parcial (entrando/saindo) vira INFO, não falha: o quadro parado é que tem que passar.

```bash
node ~/.claude/skills/hierarquia-visual/scripts/conferir_hierarquia.mjs fonte/NN-cena.html            # 8 tempos + os mais carregados
node .../conferir_hierarquia.mjs fonte/NN-cena.html --t 1.2,3.5,7 --fotos /tmp/hv-NN                  # tempos das batidas + fotos com caixas
node .../conferir_hierarquia.mjs cena.html --zona reels-anuncio      # anúncio pago: zona da Meta vira falha
node .../conferir_hierarquia.mjs vsl.html --perfil 16x9-feed         # VSL que vai rodar dentro de página/feed em pé
```
Opções: `--perfil auto|9x16|16x9|16x9-feed` · `--zona auto|reels|reels-anuncio|tiktok|shorts|todas|titulo|nenhuma` · `--n 8` · `--passo 0.1` · `--json saida.json` · `--ui "seletor"` (o que é réplica de interface; padrão `.lu-win,.lu-cel,.lu-vw,.bw,.cel,.tela,[data-hv=ui]`) · `--sem-exposicao`.
Na cena: `data-hv="ignorar"` tira um texto decorativo da conta (marca-d'água, textura de letras); `data-hv="ui"` marca uma réplica de interface.
Saída: relatório por tempo (OK / AVISO / FALHA com o motivo), seção de exposição, **resumo por problema contando textos distintos**, e com `--fotos` uma foto por tempo com as caixas pintadas (verde ok, amarelo aviso, vermelho falha) + a zona segura, e `folha.jpg`. Sai com código 1 se houver FALHA.

Como ler o resultado:
- **FALHA** = corrija antes de gravar (texto ilegível, contraste baixo, fora da zona, some antes de dar tempo).
- **AVISO** = decida conscientemente (UI pequena que a fala não cita pode ficar; 4 tamanhos numa tela de dados pode ser necessário).
- Limitações: não sabe o que a narração cita (UI pequena é aviso, não falha); texto feito com `background-clip:text` ou em imagem não é medido; `clip-path`/máscara é resolvido pela foto (texto encoberto não conta).

## Checklist (antes de gravar)

- [ ] Uma ideia por tela; título ≤ 6 palavras (ideal 3–4), quebra pelo sentido, sem viúva.
- [ ] Um nível 1 só; razão título ÷ apoio ≥ 1,5; no máximo 3 tamanhos fora de UI.
- [ ] Título ≥ 84 px · apoio ≥ 40 (rec. 44–60) · rótulo ≥ 30 · UI citada ≥ 30 efetivo (reel). 16:9: 72/36/26; no feed: 150/72/54.
- [ ] Peso ≥ 400; serif/manuscrita só ≥ 56 px; caixa-alta pequena com +0,05–0,10 em.
- [ ] Contraste ≥ 4,5:1 (≥ 3:1 se grande) medido no pixel; apoio mira 7:1.
- [ ] Fundo · tinta · UM destaque (≤ 10% da área); verde/vermelho só como estado e com ícone/palavra.
- [ ] Tudo que importa na zona segura do destino (orgânico, anúncio, TikTok, Shorts ou 16:9).
- [ ] Margem esquerda única; grupos com espaço interno ≤ ½ do externo; espaço negativo na frase de impacto.
- [ ] Ordem de entrada = ordem de leitura; só uma coisa começa a se mexer por vez.
- [ ] Cada texto fica ≥ máx(1 s; 0,5 + 0,33 × palavras); oferta ≥ 2 s + 0,2 s/palavra.
- [ ] UI: zoom ≥ 30 ÷ tamanho do texto; janela inteira só por < 1 s.
- [ ] Rodou `conferir_hierarquia.mjs` sem FALHA (ou com cada falha justificada no guia) e olhou a folha de fotos.

## Referências

- `references/tabela-numeros.md` — todos os números com fonte e conta.
- `references/tipografia.md` — escala, altura-x, peso, entrelinha, tracking, quebra; CSS pronto.
- `references/cor.md` — papéis de cor, destaque, semântica, daltonismo, WCAG/APCA (fórmulas).
- `references/leitura-em-video.md` — tempo de leitura, quantidade de texto, o que o olho lê primeiro, movimento como hierarquia, UI em vídeo, grid.
