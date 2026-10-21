# 04 — Sistema de variedade criativa (variar sempre, sem perder identidade nem qualidade)

Pedido do dono (out/2026): o editor (IA + skills) deve "sempre variar no que está usando e sempre ter essa criatividade" — não repetir o mesmo estilo de vídeo para vídeo nem dentro do vídeo — mantendo identidade e qualidade.

Lido antes: `CLAUDE.md`; `direcao-de-arte` (SKILL.md, repertorio-estilos, serie, rubrica, anti-ia); `motion-design/reference/nivel.md` e `historico.md`; `aprendizado/reacoes.md`; memórias `reels-variedade` e `motions-nivel-portfolio`; post-mortem da aula SLA; motions da SLA v2 (`projetos/<projeto>/v1/fonte/motions2/`).

---

## 1. Resumo em 5 linhas

1. Os canais que variam sem perder a cara fazem igual: um **núcleo fixo pequeno** (fontes, um destaque de cor, gancho/fecho, qualidade) e um **repertório organizado por função** que gira (Vox, Pentagram, Figma, pacotes de TV).
2. A IA tende a repetir sozinha (estudos de 2025 mostram que o modelo e os juízes preferem o "típico"): variedade **não acontece por boa vontade**, só com memória escrita, regra de não repetir e crítica que pune repetição.
3. Proposta: um **cardápio de recursos** (função, custo, receita no kit, frequência máxima), um **registro do que já usamos** (`aprendizado/repertorio-usado.md`) com janela de proibição, e um **orçamento por minuto**.
4. Antes de editar, a IA escreve um **plano de edição** com **3 opções** (conservadora, troca de 3 eixos, provocada por carta oblíqua/SCAMPER), dá a cada uma a chance de ser "a resposta típica" e escolhe a que mais ensina com distância ≥ 3 eixos da anterior; **1 estreia por vídeo**.
5. A rubrica ganha o critério 11 **Frescor** (10 %), com travas automáticas: repetir a assinatura ou o objeto-conceito do vídeo anterior do mesmo tipo = nota ≤ 2 = VOLTA; variar quebrando o núcleo também.

---

## 2. Princípios (com fontes)

### P1. Núcleo fixo pequeno + execução que varia
- **Vox**: os gráficos são reconhecíveis porque repetem os mesmos motivos (fontes, cores, animações, temas), mas cada vídeo aplica de um jeito próprio ao assunto; um dos motivos fixos é animar gráficos a 12 qps dentro de edição a 24 ("stutter") — a assinatura é técnica, não de layout. ([Kapwing](https://www.kapwing.com/resources/how-to-make-informational-videos-like-vox/), [PremiumBeat](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/))
- **Pentagram / MIT Media Lab**: uma grade 7×7 fixa gera um glifo diferente para cada um dos 23 grupos — "uma identidade fixa que celebra a diversidade". Regra fixa, saída variável. ([Pentagram](https://www.pentagram.com/news/mit-media-lab), [designboom](https://www.designboom.com/design/the-new-mit-media-lab-identity-by-pentagram/))
- **Figma (Config)**, já no nosso `serie.md`: "restringir o conceito, não a execução".
- **Kurzgesagt**: o traço (formas arredondadas, cores vivas, personagens simpáticos) é fixo, mas a técnica é "o que for preciso" (vetor, pixel, infográfico, 2D com 3D) e **cada vídeo ganha trilha própria** (Epic Mountain). ([Kurzgesagt — processo](https://kurzgesagt.org/youtube/), [UMich](https://artsatmichigan.umich.edu/ink/2019/09/27/simple-bright-beautiful-the-work-of-kurzgesagt))
- **Johnny Harris**: caixa de ferramentas fixa (mapas animados, papel/vegetal, grão, grade fina, sons de papel) e cada vídeo escolhe e combina dentro dela. ([aescripts](https://aescripts.com/learn/how-johnny-harris-makes-maps/))
- **Ali Abdaal** (shorts): núcleo fixo de grade P&B + 1 cor de destaque, legenda manuscrita à esquerda, ritmo de 2–5 s por plano. ([SendShort](https://sendshort.ai/guides/ali-abdaal-style/))
- **MKBHD**: o próprio time mostra como corta (masterclass de Final Cut); a identidade é luz, enquadramento e grade constantes. ([FCP Cafe](https://fcp.cafe/news/20241014.md))

**Para nós:** o núcleo é o que o dono já aprovou como "o topo" (nível do portfólio: 3 papéis de fonte, um destaque, grito encaixado, costura, qualidade 1080p30). O resto gira.

### P2. Organizar o repertório por FUNÇÃO (como um pacote de TV)
Pacotes de grafismo de TV vêm organizados por função: abertura, vinheta de entrada/saída (bumper), tarja (lower third, em 3 variações), transição, tela dividida, créditos. ([Videohive](https://www.videohive.net/item/upup-broadcast-package/5697347), [NewscastStudio — ABC](https://www.newscaststudio.com/2023/10/02/abc-owned-graphics-package-2023/2/))
**Para nós:** a variedade vira "qual variante entra em cada função", não "inventar tudo de novo". Assim dá para medir e não repetir.

### P3. A IA cai na resposta típica (colapso de modo) — e o juiz também
- **Verbalized Sampling** (2025): o colapso vem do "viés de tipicidade" dos dados de preferência (anotadores preferem o familiar). Pedir **várias respostas com a probabilidade de cada uma** aumenta a diversidade 1,6–2,1× em escrita criativa, sem perder qualidade; modelos mais capazes ganham mais. ([arXiv 2510.01171](https://arxiv.org/html/2510.01171v1))
- **Artificial Hivemind** (NeurIPS 2025, melhor artigo): repetição dentro do mesmo modelo e entre modelos; **modelos-juízes ficam mal calibrados** justamente onde o gosto humano varia. ([arXiv 2510.22954](https://arxiv.org/abs/2510.22954), [NeurIPS](https://neurips.cc/virtual/2025/poster/121421))
**Para nós:** (a) gerar 3 opções e marcar a "chance de ser a típica"; (b) o revisor (também IA) não pode só "gostar" — precisa de regra escrita que conte repetição.

### P4. Restrição gera criatividade
Haught-Tromp ("hipótese Green Eggs and Ham"): estudantes escreveram textos mais criativos com regras arbitrárias, e continuaram melhores depois que a regra saiu. O livro nasceu de uma aposta: 50 palavras no máximo. ([Big Think](https://bigthink.com/mind-brain/why-imposing-restrictions-can-actually-boost-creativity/), [Pacific Standard](https://psmag.com/?p=22040), [James Clear](https://jamesclear.com/dr-seuss))
**Para nós:** cada vídeo leva **uma restrição declarada** no plano ("só fundo claro", "nenhum card", "toda ênfase é por largura da fonte", "o diagrama é uma linha de metrô").

### P5. Perturbar o hábito de propósito
- **Oblique Strategies** (Eno e Schmidt, 1975): cartas sorteadas para quebrar o hábito no estúdio quando o tempo é caro — "Abandone os instrumentos normais", "Que erros você cometeu da última vez?", "Honre o erro como intenção escondida". ([Eye](https://eyemagazine.com/feature/article/oblique-strategies), [Wikipedia](https://en.wikipedia.org/wiki/Oblique_Strategies), [MusicRadar](https://www.musicradar.com/news/what-brian-enos-oblique-strategies-actually-are-and-how-you-can-use-them-in-your-music-production))
- **SCAMPER** (Eberle, 1971, a partir da lista de Osborn): Substituir, Combinar, Adaptar, Modificar/ampliar, Pôr em outro uso, Eliminar, Inverter. ([Wikipedia](https://en.wikipedia.org/wiki/SCAMPER))
**Para nós:** a opção C do plano sempre nasce de uma carta + um operador SCAMPER aplicado à "solução padrão" do momento.

### P6. Variar ≠ mudar tudo: estreia controlada
Mudar tudo de uma vez impede de saber o que deu certo e arrisca a qualidade. **Regra:** entre vídeos vizinhos giram ≥ 3 eixos visuais (`serie.md`), mas **só 1 recurso estreia** por vídeo (nunca usado, ainda sem componente testado). O resto é repertório já provado em combinação nova. Assim a reação do dono ensina algo.

### P7. Memória com penalidade por recência (como sistemas de recomendação)
Recomendadores equilibram "relevante" × "novo": o MMR escolhe item a item pela relevância **menos** a semelhança com o que já foi escolhido; há também diversidade temporal (o que mudou desde a última vez). ([Shaped](https://shaped.ai/blog/the-anatomy-of-a-modern-ranking-architectures-part-4), [RecSys ML](https://recsysml.substack.com/p/diversity-of-recommendations))
**Para nós:** registro do que usamos + peso que cai com o uso recente + bônus para o que o dono amou (mas com retorno modificado).

### P8. Plano no papel antes de cortar, crítica do problema
- **Paper edit**: no documentário, o corte é feito primeiro na transcrição e só depois no programa — economiza tempo e alinha a visão. ([Scribe](https://scribe.org/node/1048), [Chicago Media Works](https://www.chicagomediaworks.com/2instructworks/3editing_doc/3docedit_scriptmpl/3editing_docpaperwordedit.html))
- **Pixar / Braintrust**: ideias começam como "bebês feios"; a crítica franca é sobre o problema, não a pessoa, e não manda — sugere. ([Braden Kelley](https://bradenkelley.com/2015/11/the-little-known-secret-to-pixars-creative-success/), [Stanford eCorner](https://stvp.stanford.edu/clips/the-hungry-beast-and-the-ugly-baby))
**Para nós:** já temos `narrativa.md` (o paper edit da fala). Falta o **plano visual** junto dele, com as 3 opções como "bebês feios" baratos (texto, não render).

### P9. Orçamento por minuto (o que já sabemos)
- Teto de ~3 chamadas/destaques por minuto (alunos acharam 4/min demais); alarme se > 40 s sem mudança visual (`edicao-video/references/oficio-youtube.md`, M7).
- 1 anotação a cada 15–25 s; tela encolhida ≤ 30 % do tempo de tela (`edicao-video` passo 10b).
- ≤ 50 % do mesmo gesto de entrada; depois de gesto grande, 2–4 s de micro-movimento (`nivel.md` 55); um estilo de movimento por vídeo + 2–3 transições (`nivel.md` 25, `anti-ia.md`).
- ≥ 2 de cada 6 motions em fundo claro (`nivel.md` 59).

---

## 3. Proposta concreta

### O que é núcleo e o que gira (decisão)

| Camada | Fixo (identidade) | Gira (variedade) |
|---|---|---|
| Estúdio (todo vídeo) | Qualidade (1080p30, 16–20 Mb/s, -14 LUFS, ≤ 40 ms), 3 PAPÉIS de fonte (grito/voz/máquina), UM destaque de cor, grito encaixado pela largura, costura (nada "do nada"), sem sinais de IA, didático antes de bonito | Todo o resto |
| Marca/curso (ex.: aulas cliente B) | Logo, cores da marca, regras de texto, **trio Archivo / Instrument Serif / JetBrains Mono** (o dono aprovou como "o topo"; numa série de aulas vira a cara do curso, como as fontes da Vox), posição da câmera do professor, formato do capítulo-base | Objeto-conceito, luz/fundo base, estilo do repertório nos diagramas, gesto-assinatura, costura, tipo de tela em cena, anotações, abertura, fechamento, trilha |
| Outras marcas / YouTube sem marca | Só o núcleo do estúdio | Também o trio tipográfico (pool do `repertorio-estilos.md`) |

Observação: a memória `motions-nivel-portfolio` e o `nivel.md` 30 fixam o trio Archivo/Serif/Mono. Isso fica como **identidade** — a variedade mora nos outros eixos. Se o dono quiser trocar fontes também nas aulas, vira uma estreia declarada.

### (a) Cardápio de recursos do estúdio

Custo: **P** = até 15 min (componente pronto) · **M** = 30–90 min (receita existe, adaptar) · **G** = 2 h+ (novo ou 3D pesado) · **E** = estreia (componente em esboço, testar antes de usar em série).
Frequência: por vídeo de ~5 min, e janela entre vídeos do mesmo tipo ("não nos últimos N").

| # | Recurso | Função | Custo | Receita no kit | Frequência máxima |
|---|---|---|---|---|---|
| **Abrir / gancho** |||||
| 1 | Câmera do professor dentro da cena (slot + texto na fala ao lado, câmera voa para o canto) | gancho com rosto | M | `motions2/00-abertura.html` + `MolduraMovel` (`edicao-video/remotion/src/componentes.tsx`) | 1/vídeo · não nos últimos 2 |
| 2 | Resultado primeiro (mostrar o fim funcionando em ≤ 15 s, depois "como chegar") | gancho por prova | P–M | `edicao-video/references/oficio-youtube.md` (gancho); trecho do próprio bruto | 1/vídeo · não nos últimos 2 |
| 3 | Palavra gigante tela cheia na 1ª frase (grito encaixado + voz itálica) | gancho de frase | P | `aula2.js` `grito()`/`voz()`/`encaixa()`; `tipografia-que-funciona.md` §3 | 1/vídeo como abertura · não nos últimos 2 |
| 4 | Objeto-personagem entrando de perto da câmera com desfoque | gancho de objeto | M–G | `nivel.md` 40; `kit/desfoque.sh`; `kit/objeto3d.js` | 1/vídeo · não nos últimos 3 |
| **Conceito (a ideia que atravessa)** |||||
| 5 | Objeto 3D que É o conceito (three.js, 3 luzes + chão) | ensinar com metáfora física | G | `kit/objeto3d.js`; `motions2/relogio3d.js`; `nivel.md` 56 | 1 objeto/vídeo · o MESMO objeto não nos últimos 5 |
| 6 | Mundo CSS 3D (chão em grade, câmera em trilho) | diagrama com profundidade | M | `motions2/03-duas-automacoes.html`; `nivel.md` 39, 49 | 1–2/vídeo · não nos últimos 2 |
| 7 | Diagrama num estilo do repertório (metrô Vignelli, planta técnica, painel de aeroporto, caderno, cupom) | processo/etapas com material próprio | M | `direcao-de-arte/references/repertorio-estilos.md` (13, 15, 16, 6, 26) | 1 estilo/vídeo · o mesmo estilo não nos últimos 3 |
| 8 | Cor do estado invadindo a tela por um gesto (círculo que nasce do objeto) | virada/alerta | P–M | `aula2.js` `fundoSLA()`; `nivel.md` 51 | ≤ 3/vídeo · como linguagem principal, não nos últimos 2 |
| 9 | Palavra que vira outra (letras viajando, LCS) | antes → depois de conceito | M | `nivel.md` 34; `$SITE/app/src/secoes/01-marca.js` | ≤ 2/vídeo · não nos últimos 2 |
| 10 | Palavra riscada → substituta no mesmo lugar (RESPONDIDO. → NO VÁCUO.) | desfazer ideia errada | P | `motions2/04-pegadinha.html`; `nivel.md` 50 | 1/vídeo · não nos últimos 3 |
| 11 | Antes/depois (divisória que corre, ou troca de estilo na virada) | comparação | M | `edicao-video/references/anotacoes.md` 2.9; `direcao-de-arte` A2 "virada como troca de estilo" | 1/vídeo |
| 12 | Quantidade sem número (muitos objetos, câmera afasta) | "inúmeros" | M | `nivel.md` 15 | 1/vídeo · não nos últimos 3 |
| 13 | Número gigante com máscara + rótulo mono | tempo, prazo, contagem que a fala cita | P | `tipografia-que-funciona.md` §2, §7; `nivel.md` 31, 35 | ≤ 2/vídeo (só número dito na fala) |
| **Tela gravada** |||||
| 14 | Zoom que segue a ação | ler a interface | P | `edicao-video/scripts/zoom.py` | sempre que precisar (segura ≥ 4 s, ≤ 1,6×) |
| 15 | Tela em cena: cartão 0,75–0,84 + elemento que salta (pop-out 3D) | o "After Effects em volta" | E→M | `edicao-video/references/tela-em-cena.md` 2.1–2.10 (`TelaEmCena`, esboço) | 2–3 momentos/vídeo · ≤ 30 % do tempo de tela · variante diferente a cada vez |
| 16 | Holofote (escurece o resto) | "esse campo aqui" | E→P | `anotacoes.md` 2.2 | ≤ 3/vídeo |
| 17 | Lupa / elemento que levanta | detalhe pequeno | E→P | `anotacoes.md` 2.3, 2.5 | ≤ 2/vídeo |
| 18 | Seta + rótulo / passos 1-2-3 | sequência de cliques | E→P | `anotacoes.md` 2.6, 2.7 | 1 sequência/vídeo |
| 19 | Selo de status ao vivo | teste ao vivo, estado | P | `SeloStatus` (`componentes.tsx`) | 1/vídeo · não nos últimos 2 |
| 20 | Texto digitado ampliado | valor que o aluno copia | P–M | `anotacoes.md` 2.10 | ≤ 2/vídeo |
| **Costura e capítulos** |||||
| 21 | Match cut de forma (forma de A vira objeto de B) | costura | M | `nivel.md` 38 | ≥ 1/vídeo · o mesmo par não repete |
| 22 | Objeto-conceito que sai de um motion e entra no próximo | costura de aula | P (com objeto) | `nivel.md` 58 | todo vídeo com objeto |
| 23 | Lâmina/círculo de cor que invade | costura com virada | P | `nivel.md` 38 | ≤ 2/vídeo |
| 24 | Marcador de capítulo (alfa perto da câmera) | capítulo | P | `Capitulo` (`componentes.tsx`); `edicao-video/scripts/capitulos.py` | 1 por bloco · **forma do marcador gira por vídeo** (barra, estação, carimbo, número gigante) |
| **Ênfase e movimento (gestos)** |||||
| 25 | Entrada por máscara + largura (wdth 62 → 125) | grito | P | `nivel.md` 33, 35 | ≤ 50 % das entradas |
| 26 | Letras viajando entre palavras | grito em sequência | M | `nivel.md` 34 | ≤ 30 % |
| 27 | Chegada de perto da câmera com desfoque | impacto | M | `nivel.md` 40 | ≤ 2/vídeo |
| 28 | Onda letra a letra com peso ao contrário | fecho, respiro | P | `nivel.md` 33 | ≤ 1/vídeo |
| **Fechar** |||||
| 29 | Objeto no estado final + um grito + marca | fechamento | P–M | `nivel.md` 57; `motions2/05-fechamento.html` | 1/vídeo · a composição não repete a do anterior |
| 30 | Card "fim no ar" / próximo passo | fechamento sem fala | P | `edicao-video` passo 10 | 1/vídeo |
| **Material e som** |||||
| 31 | Película/grão | textura de arquivo | M (render 3×) | `kit/pelicula.js`; skill `editorial-film-edit` | só se o conceito pede · não nos últimos 2 |
| 32 | Colagem de papel (vinheta) | vinheta artesanal | G | skill `paper-collage-film` | 1 vinheta · não nos últimos 5 |
| 33 | Trilha sob a voz (-25 dB) | clima | P | `edicao-video/references/som.md`; `trilha_voz.py` | 1 trilha/vídeo · **a mesma faixa não nos últimos 5** |
| 34 | Efeitos desenhados (whoosh com pico no corte, riser no drop) | costura sonora | P–M | `kit/som.py`; `nivel.md` 44 | pouco; o mesmo pacote de sons não nos últimos 2 |
| **Luz / fundo base** |||||
| 35 | Família de fundo base (osso claro, tinta, cor plena, papel quente, azul planta) | clima do vídeo | P | `direcao-de-arte/references/serie.md` §2; `nivel.md` 51, 59 | a família BASE não repete o vídeo anterior do mesmo tipo; ≥ 2 de 6 motions claros |

### (b) Registro "o que já usamos"

Arquivo: `~/motion-studio/aprendizado/repertorio-usado.md` (criar ao adotar a proposta; não criei aqui porque fica fora desta pasta).

Formato: uma linha por vídeo entregue, uma coluna por **eixo de variedade** (os números são os do cardápio acima). Quem planeja lê as últimas 5 linhas do mesmo tipo de peça; quem entrega preenche a linha.

```markdown
# Repertório usado (o que já entrou em cada vídeo)

Tipos: aula · youtube · vsl · reel · anuncio · portfolio
Ler as últimas 5 linhas do MESMO tipo antes de planejar. Preencher depois de entregar (junto com historico.md).
Números = linhas do cardápio (pesquisa/<estudo>/04-variedade-criativa.md §3a).

| Data | Tipo | Projeto · vídeo | Fundo base | Estilo do repertório | Objeto-conceito | Abertura | Assinatura de movimento | Gestos de entrada (%) | Costura | Tela em cena / anotações | Capítulo (forma) | Fechamento | Trilha | Restrição declarada | Estreia | Reação |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 07/10/2026 | aula | cliente B IA ON/OFF v3 | escuro | — | — | — | corte no meio do movimento | fade+sobe (padrão) | xfade/corte | — | barra alfa | card fim | — | — | HyperFrames + Remotion | aguardando |
| 15/10/2026 | aula | cliente B SLA v1 | tinta | — | anel do tempo | 1 câmera dentro da cena | anel girando | cards padrão | anel atravessa | 19 selo status | barra alfa | anel + resumo | nenhuma | — | câmera dentro da cena | ★★ "ficou muito bom" |
| 16/10/2026 | aula | cliente B SLA v2/v2.1 | tinta + cor do estado | — (mundo CSS 3D) | 5 cronômetro 3D (mostrador = régua) | 1 câmera dentro da cena + 3 grito por palavra | 8 cor do estado invade a partir do relógio | 25 máscara+largura (~70 %), 13 número | 22 relógio atravessa | 6 mundo CSS 3D trilhos; 10 RESPONDIDO→NO VÁCUO; 19 selo | barra alfa | 29 relógio NO PRAZO + resumo 3 linhas mono | Mixkit -25 dB | "nível portfólio" | 5 objeto 3D em aula | ★★ "melhorou pra caralho" (3 pedidos) |
| 10/10/2026 | portfolio | Filme A / MEIA-NOITE / Filme B | cor plena / cinema escuro / branco estúdio | 30 / 31 / 32 | cartão / fósforo / objeto vidro | 3 palavra gigante | objeto entre letras / película / cotas→números | 25, 26, 27 | 21 match cut | — | — | logo | trilhas próprias | 1 destaque por peça | desfoque real | ★★★ "o topo" |
```

**Regra de não repetir (janela por eixo, só entre vídeos do mesmo tipo e mesma marca):**

| Eixo | Janela de proibição | Exceção |
|---|---|---|
| Objeto-conceito (o mesmo objeto) | últimos 5 | série que pede o mesmo objeto (ex.: curso com mascote) — declarar no núcleo |
| Assinatura de movimento | últimos 3 | — |
| Abertura (forma) | últimos 2 | — |
| Estilo do repertório nos diagramas | últimos 3 | — |
| Família de fundo base | último (vizinho) | — |
| Composição do fechamento | último | — |
| Forma do marcador de capítulo | último | se virou identidade do curso (declarar) |
| Trilha (a mesma faixa) | últimos 5 | trilha-tema do canal (declarar) |
| Gesto de entrada dominante (> 50 %) | último | — |

**Reprise do que o dono amou (★★★):** pode voltar depois da janela, **sempre modificado por um operador SCAMPER** (ex.: o "objeto entre as letras" volta como objeto 2D de papel, não 3D). Escrever no plano: "reprise de X, modificada por Y".

**Sorteio com peso (quando houver empate entre opções boas):**
`peso = base × 0,5^(usos nos últimos 5 do mesmo tipo) × bônus`, com `bônus` = 1,5 para ★★★, 1,2 para ★★, 0,5 para ✗; peso 0 dentro da janela de proibição. Sortear entre as 3 opções do plano pelo peso **só** quando a nota de "ensina" empatar — a função vem antes da novidade. (Um `aprendizado/sortear.py` de 30 linhas pode ler a tabela; opcional.)

**Dentro do vídeo (não repetir de motion para motion):**
- Vizinhos não repetem gesto de entrada nem a mesma variante de tela em cena.
- Nenhum gesto > 50 % das entradas; cada motion usa ≤ 2 gestos.
- Pelo menos 2 de cada 6 motions em fundo claro; nunca 3 motions seguidos na mesma família de fundo.
- Anotações: tipos alternados (holofote → seta → lupa), nunca o mesmo tipo duas vezes seguidas.

### (c) Procedimento: a IA planeja a variedade de um vídeo (7 passos)

1. **Ler a memória.** As últimas 5 linhas do mesmo tipo em `aprendizado/repertorio-usado.md`, as reações ✗/★ do mesmo tipo em `aprendizado/reacoes.md` e o "uma coisa para tentar no próximo" do último `POSTMORTEM.md`. Escrever a **lista do proibido** (o que está dentro da janela) e a **solução padrão** (o que a IA faria no piloto automático).
2. **Mapa de momentos.** Do `fonte/narrativa.md` (paper edit), listar os momentos com função: gancho, conceito, passo de tela, prova/teste, virada, capítulo, fechamento. Marcar quais ficam mais claros desenhados (os candidatos a motion) e onde a fala aponta a tela (candidatos a anotação).
3. **Orçamento.** Pela duração do editado (tabela abaixo), fixar quantos de cada recurso cabem.
4. **Três opções completas.** Cada uma com: nome, conceito em 1 frase, objeto-conceito, fundo base, estilo do repertório, abertura, assinatura, restrição declarada, estreia, e a **chance de ser a resposta típica** (0–1):
   - **A — conservadora:** o que funcionou por último, trocando só o proibido.
   - **B — troca de 3 eixos:** gira pelo menos 3 eixos do `serie.md` §2 em relação ao vídeo anterior.
   - **C — provocada:** sorteie 1 carta oblíqua (lista abaixo) e 1 operador SCAMPER e aplique à solução padrão.
   As opções são "bebês feios": texto e, no máximo, um quadro parado por opção. Nada de render.
5. **Escolher.** Critérios em ordem: (1) ensina melhor sem som; (2) cabe no núcleo (identidade intacta); (3) distância ≥ 3 eixos do vídeo anterior do mesmo tipo; (4) menor chance de ser a típica; (5) custo cabe no prazo. Pode juntar (ex.: B com a abertura de C). Escrever em 2 linhas por que ganhou e por que as outras perderam.
6. **Escrever o `fonte/PLANO-EDICAO.md`.** Tabela tempo a tempo: momento · função · recurso (nº do cardápio) · gesto · fundo · costura para o próximo. Depois o **teste de repetição**: nada da lista do proibido; ≤ 50 % do mesmo gesto; vizinhos diferentes; ≥ 2 de 6 claros; 1 estreia só; teto de destaques por minuto; nenhum trecho > 40 s sem mudança visual. Se falhar, ajustar antes de abrir a primeira cena.
7. **Depois de entregar.** Linha no `repertorio-usado.md` (todos os eixos) + reação do dono quando vier. Estreia que funcionou vira componente pronto (custo P/M no cardápio); estreia que falhou vai para `armadilhas.md`.

**Orçamento por minuto de vídeo editado (aula/tutorial com tela):**

| Recurso | Por minuto | Vídeo de 5 min | Observação |
|---|---|---|---|
| Destaques no total (motions + anotações + tela em cena) | ≤ 3 | ≤ 15 (alvo 10–12) | teto, não meta |
| Motions de ideia (cena cheia ou por cima) | ~1 | 4–6 | cada um desenha UMA ideia da fala |
| Anotações na tela | 1 a cada 15–25 s de tela | 5–8 | nunca no clique que o aluno copia |
| Tela em cena | — | 2–3 momentos, ≤ 30 % do tempo de tela | variante diferente a cada vez |
| Capítulos | — | 3–4 | forma do marcador nova a cada vídeo |
| Objeto-conceito | — | 1 (atravessa abertura → meio → fecho) | |
| Gestos de entrada distintos | — | ≥ 3, nenhum > 50 % | |
| Cortes secos com intenção | — | ≤ 1 | `nivel.md` 38 |
| Maior trecho sem mudança visual | — | ≤ 40 s | alarme do M7 |
| Estreia | — | 1 | |

**Cartas oblíquas do estúdio (adaptadas para vídeo; sortear 1):**
1. Comece pelo fim.
2. Tire o card: o que sobra se não houver nenhuma caixa?
3. Use só uma cor além do fundo.
4. O diagrama é um lugar (uma estação, uma mesa, um mapa).
5. O que um designer de jornal faria aqui?
6. A tela gravada é o objeto: tire-a do retângulo.
7. Troque o 3D pelo papel (ou o papel pelo 3D).
8. Que erro você cometeu da última vez? Faça o contrário.
9. Mostre a quantidade, não o número.
10. Inverta claro e escuro na virada.
11. Uma palavra só por tela, o vídeo inteiro.
12. Honre o erro: o tropeço da gravação vira o "jeito errado" antes do certo.

#### Texto pronto para colar — `edicao-video/SKILL.md` (novo passo 4b, depois da decupagem narrativa)

```markdown
4b. **Plano de variedade (antes de qualquer motion)** — o dono pediu "sempre variar e ter criatividade", sem perder identidade.
   Leia as últimas 5 linhas do mesmo tipo em `~/motion-studio/aprendizado/repertorio-usado.md` e escreva a lista do proibido
   (janela por eixo: objeto 5 vídeos, assinatura 3, estilo de diagrama 3, abertura 2, fundo base 1, fechamento 1, trilha 5).
   Escreva 3 opções em `fonte/PLANO-EDICAO.md` — A conservadora, B troca ≥ 3 eixos, C provocada (1 carta oblíqua + 1 operador
   SCAMPER) — cada uma com conceito, objeto, fundo base, abertura, assinatura, restrição declarada, estreia e a chance de ser a
   resposta típica. Escolha pela ordem: ensina sem som > cabe no núcleo > distância ≥ 3 eixos > menos típica > custo.
   Monte a tabela tempo a tempo com os recursos do cardápio (`pesquisa/<estudo>/04-variedade-criativa.md` §3a) dentro
   do orçamento: ≤ 3 destaques/min, 4–6 motions em 5 min, 1 estreia, nenhum gesto > 50 %, vizinhos diferentes, ≥ 2 de 6 claros,
   nada > 40 s sem mudança visual. Núcleo fixo (não varia): qualidade de entrega, 3 papéis de fonte, um destaque, grito encaixado,
   costura, marca. Depois de entregar: linha no `repertorio-usado.md`.
```

E no passo 10 (Motions), acrescentar no fim: "Siga o `fonte/PLANO-EDICAO.md` do passo 4b; mudar o plano no meio = atualizar o arquivo e refazer o teste de repetição."

#### Texto pronto para colar — `direcao-de-arte/SKILL.md`

Na A1, trocar a pergunta 7 por:

```markdown
7. **O que já fizemos?** Leia as últimas 5 linhas do mesmo tipo em `~/motion-studio/aprendizado/repertorio-usado.md`
   e o `evolucao.md` da marca. Escreva a lista do proibido (objeto 5 vídeos, assinatura 3, estilo 3, abertura 2,
   fundo base 1) e a "solução padrão" — o que você faria no piloto automático. As 3 rotas não podem ser ela.
```

Na A2, acrescentar depois do primeiro parágrafo:

```markdown
**As 3 rotas têm papéis fixos:** A conservadora (o que funcionou, trocando o proibido), B troca ≥ 3 eixos de `serie.md` §2,
C provocada (sorteie 1 carta oblíqua e 1 operador SCAMPER — Substituir, Combinar, Adaptar, Modificar, Pôr em outro uso,
Eliminar, Inverter — e aplique à solução padrão). Dê a cada rota a chance de 0 a 1 de ser "a resposta típica de IA".
Modelos e juízes de IA preferem o típico (Verbalized Sampling; Artificial Hivemind, 2025): sem essa etapa as rotas saem
parecidas. Cada peça declara **uma restrição** ("nenhum card", "só fundo claro", "o diagrama é uma linha de metrô")
e **uma estreia** (um recurso nunca usado); o resto vem do repertório provado.
```

Na Parte B, acrescentar a regra 7:

```markdown
7. **Vale também dentro de um vídeo longo (aula, VSL):** os motions de um mesmo vídeo são vizinhos — não repetem gesto de
   entrada, nem variante de tela em cena, nem a família de fundo três vezes seguidas; nenhum gesto > 50 % das entradas.
```

### (d) Como a rubrica pune repetição

Proposta para `direcao-de-arte/references/rubrica.md`:

**Novo critério 11 — Frescor (10 %).** Pesos rebalanceados: Ideia visual 15 → 12 · Hierarquia 10 → 8 · Tipografia 10 → 8 · Movimento 10 → 8 · Costura 10 → 9 · Frescor 10 (os outros ficam iguais; soma 100).

| # | Critério | Peso | 1 (ruim) | 3 (ok) | 5 (topo do estúdio) |
|---|---|---|---|---|---|
| 11 | **Frescor** (é diferente do anterior e varia por dentro, sem perder a cara?) | 10 % | Repete o objeto-conceito, a assinatura ou a abertura do vídeo anterior do mesmo tipo; ou um gesto > 70 % das entradas; ou varia tanto que quebra o núcleo (outra fonte, outro destaque, sem costura) | Muda 1–2 eixos; dentro do vídeo há vizinhos repetidos | Muda ≥ 3 eixos em relação ao anterior, 1 estreia que funcionou, vizinhos todos diferentes, e trocando o logo ainda parece o nosso estúdio |

**Travas automáticas (o avaliador confere no `repertorio-usado.md` e no `PLANO-EDICAO.md`):**
- Algo dentro da janela de proibição sem exceção declarada → Frescor ≤ 2 → **VOLTA** (a rubrica já reprova qualquer critério ≤ 2).
- Gesto de entrada > 50 % → Movimento no máximo 3. Três motions seguidos na mesma família de fundo → Costura no máximo 3.
- Mais de 1 estreia → Acabamento no máximo 3 (risco de qualidade sem teste).
- Variedade que quebra o núcleo (4ª fonte, segundo destaque, troca "do nada") → Frescor ≤ 2 **e** Tipografia/Costura perdem 1.
- "Ganhou do anterior em:" passa a ter que citar **pelo menos 1 eixo novo**; se o vídeo só ganhou em acabamento, nota de Frescor ≤ 3.
- Nota de Frescor exige evidência como as outras: "eixos trocados: fundo (tinta → osso), estilo (CSS 3D → metrô), assinatura (cor invade → ponto que corre)".

Calibração: se o dono disser "tá parecido com o outro" com Frescor ≥ 4 → reescrever as âncoras. Se disser "estranho, não parece vocês" → a trava do núcleo estava frouxa.

---

## 4. Exemplo preenchido — próxima aula do dono (GoHighLevel genérica, ~5 min)

Tema ainda não definido; uso como exemplo **"Workflow de boas-vindas: lead preenche o formulário → recebe WhatsApp → entra no pipeline → equipe ganha tarefa"** (trocar pelo tema real quando a gravação chegar em `entrada/`; o procedimento é o mesmo). Marca suposta: cliente B (curso). Se for YouTube sem marca, o trio de fontes também pode girar.

### Passo 1 — memória
- Últimas aulas: SLA v2 (tinta + cor do estado; cronômetro 3D; mundo CSS 3D com trilhos; abertura com câmera dentro da cena; RESPONDIDO → NO VÁCUO; fechamento relógio + resumo mono; Mixkit), SLA v1 (anel, câmera dentro da cena), IA ON/OFF v3.
- Reações: ★ SLA v2 — música alta, borda cortada, "uma palavra gigante por vez". Post-mortem: "tentar tela em cena em 1–2 momentos calmos + 2 anotações; abrir mostrando o resultado em ≤ 15 s".
- **Proibido:** objeto relógio/anel; assinatura "cor do estado invade a partir do objeto"; abertura com câmera no slot; mundo CSS 3D com trilhos (janela 2); fundo base tinta; fechamento "objeto + resumo 3 linhas mono"; Mixkit da SLA; palavra riscada → substituta (janela 3).
- **Solução padrão (o piloto automático):** fundo escuro, fluxo do workflow como blocos ligados por linhas em 3D, um ícone por etapa, ponto correndo pela linha, contagem "3 s". → as rotas não podem ser isso.

### Passo 2 — mapa de momentos (ilustrativo)
| Tempo | Momento | Função |
|---|---|---|
| 0:00–0:15 | "quando alguém preenche seu formulário, recebe isso aqui na hora" | gancho |
| 0:15–0:40 | o que vamos montar (4 etapas) | promessa + mapa da aula |
| 0:40–1:40 | criar o gatilho "formulário enviado" | passo de tela |
| 1:40–2:50 | ação de WhatsApp com o nome do lead | passo de tela + porquê |
| 2:50–3:40 | mover no pipeline + criar tarefa | passo de tela |
| 3:40–4:30 | teste ao vivo: preenche e a mensagem chega | prova |
| 4:30–5:00 | recapitula e fecha | fechamento |

### Passo 3 — orçamento (5 min)
≤ 15 destaques (alvo 11) · 5 motions · 6 anotações · 2 telas em cena · 4 capítulos · 1 objeto-conceito · 3 gestos (nenhum > 50 %) · 1 estreia · nada > 40 s parado.

### Passo 4 — três opções
| | A — conservadora | B — troca de eixos | C — provocada |
|---|---|---|---|
| Nome | "A caixa de correio" | "Linha de metrô" | "De trás para a frente" |
| Conceito | Um envelope 3D de metal atravessa a aula e é entregue no fim | O workflow é uma linha de metrô: o lead é um passageiro que embarca no formulário e desce em cada estação | Começa com o celular do lead vibrando com a mensagem; a aula volta etapa por etapa até o formulário |
| Objeto | envelope 3D (three.js) | cartão de embarque do lead (papel, 2D, dados inventados: "Ana Ribeiro") | celular-objeto (réplica) |
| Fundo base | tinta | **osso claro**, linha na cor do destaque cliente B | branco de estúdio → tinta na virada |
| Estilo | 3D objeto | 26 Sinalização de metrô (Vignelli) | 18 Keynote claro + 22 explicador |
| Abertura | envelope chega de perto da câmera | mapa da linha desenhando (4 estações = 4 capítulos) | resultado primeiro (rec. 2) |
| Assinatura | envelope que se abre | o ponto que corre pela linha e "acende" a estação na palavra | rebobinar: cada etapa se desmonta em ordem inversa |
| Restrição | só 3D, sem card | nenhuma caixa: tudo é linha, ponto e rótulo | uma palavra por tela |
| Estreia | — | tela em cena com elemento que salta (rec. 15) | rebobinar |
| Chance de ser a típica | 0,55 (é o "objeto 3D da aula", virou nosso padrão) | 0,25 | 0,15 |
| Carta / SCAMPER | — | carta 4 "o diagrama é um lugar" + Substituir (bloco → estação) | carta 1 "comece pelo fim" + Inverter |

### Passo 5 — escolha
**B com a abertura de C.** B ensina melhor (workflow = sequência de etapas = linha com estações; o aluno vê onde está em cada capítulo), troca 4 eixos da SLA (fundo tinta → osso; 3D → plano Vignelli; assinatura cor-invade → ponto que corre; objeto metal → papel) e cumpre o "tentar no próximo" do post-mortem. A abertura de C (resultado primeiro) resolve o gancho em ≤ 15 s. A perdeu: repete o "objeto 3D que atravessa" pela 2ª vez seguida (tipicidade 0,55). C inteira perdeu: o "rebobinar" é estreia arriscada junto com a tela em cena (2 estreias).

### Passo 6 — `fonte/PLANO-EDICAO.md` (resumo)
Núcleo: Archivo/Instrument Serif/JetBrains Mono; destaque = cor do cliente B só na linha do metrô e no ponto; logo cliente B no fecho; 1080p30, -14 LUFS.
Restrição declarada: **nenhuma caixa/card em motion** — tudo é linha, ponto, rótulo e grito.

| Tempo | Momento | Recurso (nº) | Gesto | Fundo | Costura para o próximo |
|---|---|---|---|---|---|
| 0:00–0:12 | gancho: celular vibra com "Oi, Ana! Recebemos seu cadastro" | 2 resultado primeiro + 3 grito "NA HORA." (voz: "em segundos") | 27 chegada de perto da câmera | osso | o ponto verde da notificação vira o ponto da linha |
| 0:12–0:38 | mapa da aula | 7 metrô: linha desenha, 4 estações (FORMULÁRIO · WHATSAPP · PIPELINE · TAREFA) | 25 máscara + largura nos nomes | osso | câmera aproxima a estação 1 → vira o marcador de capítulo |
| 0:38 | capítulo 1 | 24 marcador = **estação acesa** (forma nova) | — | alfa | — |
| 0:50 | "aqui em Gatilho, escolha Formulário enviado" | 16 holofote | — | tela | — |
| 1:15 | "esse campo é o formulário certo" | 18 seta + rótulo | — | tela | — |
| 1:40 | capítulo 2 + porquê do nome na mensagem | 15 **estreia**: tela em cena 0,8 com o campo {{contact.first_name}} saltando da tela e virando "Ana" | 26 letras viajando ({{nome}} → Ana) | tela + osso | — |
| 2:20 | "a mensagem que ele recebe" | 20 texto digitado ampliado | — | tela | — |
| 2:50 | capítulo 3 | 24 estação acesa | — | alfa | — |
| 3:05 | "move para Novo lead e cria uma tarefa" | 18 passos 1-2-3 | — | tela | — |
| 3:25 | por que a tarefa importa (quem atende) | motion: linha bifurca (lead segue / equipe recebe tarefa), grito "NINGUÉM ESQUECE." | 25 máscara + largura | **tinta** (único escuro, marca a virada) | o ponto da bifurcação vira o cursor do teste |
| 3:40 | capítulo 4 — teste ao vivo | 15 tela em cena variante 2.8 (tela de lado + selo "ENVIADO · 3 s") — mas sem o `SeloStatus` da SLA: o selo é um bilhete de metrô carimbado | — | tela + osso | — |
| 4:10 | a mensagem chega no celular | 17 lupa no celular gravado | — | tela | — |
| 4:30–5:00 | fechamento | 29 nova composição: a linha inteira com as 4 estações acesas, o cartão de embarque "CHEGOU." e o logo cliente B; resumo vai para a descrição (nivel 57) | 28 onda letra a letra | osso | — |

Trilha: outra faixa (não Mixkit da SLA), -25 dB sob a voz, sobe só nos 30 s finais.

**Teste de repetição:**
- Proibido: nenhum item usado (sem relógio, sem slot de câmera, sem cor-invade como assinatura, sem CSS 3D, sem resumo mono). ✔
- Gestos: 5 entradas de motion — 25 em 2 (40 %), 26, 27 e 28 em 1 cada. ✔
- Fundos dos 5 motions: osso, osso, osso (tela em cena), tinta, osso → 4 de 5 claros; o único escuro marca a virada. ✔
- Destaques: 5 motions + 6 anotações + 2 telas em cena = 13 em 5 min (2,6/min). ✔
- Maior trecho sem mudança: 2:20–2:50 (30 s). ✔
- Estreia: só a tela em cena (rec. 15). As anotações 16–18 também estão em esboço — **testar o componente antes** num trecho curto; se não ficar pronto, cair para zoom (rec. 14) + rótulo no motion, sem segunda estreia.
- Distância do anterior: fundo base, estilo, assinatura, objeto, abertura, capítulo, fechamento, trilha = 8 eixos. Núcleo intacto (mesmas 3 fontes, um destaque, costura). ✔

### Passo 7 — linha para o registro (depois de entregar)
`| AAAA-MM-DD | aula | cliente B workflow boas-vindas | osso | 26 metrô | cartão de embarque (papel) | 2 resultado primeiro | ponto que corre e acende a estação | 25 50 %, 26, 27, 28 | ponto da notificação → linha; bifurcação → cursor | 15 ×2 (estreia), 16, 17, 18, 20 | estação acesa | linha inteira acesa + CHEGOU. | <faixa> -25 dB | nenhuma caixa | tela em cena | <reação> |`

---

## Fontes

- Vox: [Kapwing — How to make informational videos like Vox](https://www.kapwing.com/resources/how-to-make-informational-videos-like-vox/) · [PremiumBeat — replicating a Vox motion graphic](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)
- Pentagram / MIT Media Lab: [Pentagram](https://www.pentagram.com/news/mit-media-lab) · [designboom](https://www.designboom.com/design/the-new-mit-media-lab-identity-by-pentagram/)
- Kurzgesagt: [Our video process](https://kurzgesagt.org/youtube/) · [Arts at Michigan](https://artsatmichigan.umich.edu/ink/2019/09/27/simple-bright-beautiful-the-work-of-kurzgesagt)
- Johnny Harris: [aescripts — how Johnny Harris makes maps](https://aescripts.com/learn/how-johnny-harris-makes-maps/)
- Ali Abdaal: [SendShort — Ali Abdaal style](https://sendshort.ai/guides/ali-abdaal-style/)
- MKBHD: [FCP Cafe — masterclass do time MKBHD](https://fcp.cafe/news/20241014.md)
- Pacotes de TV por função: [Videohive — broadcast package](https://www.videohive.net/item/upup-broadcast-package/5697347) · [NewscastStudio — ABC 2023](https://www.newscaststudio.com/2023/10/02/abc-owned-graphics-package-2023/2/)
- Colapso de modo: [Verbalized Sampling (arXiv 2510.01171)](https://arxiv.org/html/2510.01171v1) · [Artificial Hivemind (arXiv 2510.22954)](https://arxiv.org/abs/2510.22954) · [NeurIPS 2025](https://neurips.cc/virtual/2025/poster/121421)
- Restrições: [Big Think](https://bigthink.com/mind-brain/why-imposing-restrictions-can-actually-boost-creativity/) · [Pacific Standard](https://psmag.com/?p=22040) · [James Clear — Dr. Seuss](https://jamesclear.com/dr-seuss)
- Oblique Strategies: [Eye Magazine (1997)](https://eyemagazine.com/feature/article/oblique-strategies) · [Wikipedia](https://en.wikipedia.org/wiki/Oblique_Strategies) · [MusicRadar](https://www.musicradar.com/news/what-brian-enos-oblique-strategies-actually-are-and-how-you-can-use-them-in-your-music-production)
- SCAMPER: [Wikipedia](https://en.wikipedia.org/wiki/SCAMPER)
- Diversidade em recomendação: [Shaped — ranking parte 4 (MMR)](https://shaped.ai/blog/the-anatomy-of-a-modern-ranking-architectures-part-4) · [RecSys ML — diversity](https://recsysml.substack.com/p/diversity-of-recommendations)
- Paper edit: [Scribe — Paper Cuts](https://scribe.org/node/1048) · [Chicago Media Works](https://www.chicagomediaworks.com/2instructworks/3editing_doc/3docedit_scriptmpl/3editing_docpaperwordedit.html)
- Pixar: [Braden Kelley — Braintrust](https://bradenkelley.com/2015/11/the-little-known-secret-to-pixars-creative-success/) · [Stanford eCorner — ugly baby](https://stvp.stanford.edu/clips/the-hungry-beast-and-the-ugly-baby)
- Nossas: `direcao-de-arte/references/serie.md`, `rubrica.md`, `anti-ia.md`; `motion-design/reference/nivel.md` (25, 30–60); `edicao-video/references/oficio-youtube.md` (M7), `tela-em-cena.md`, `anotacoes.md`; `projetos/<projeto>/v1/POSTMORTEM.md`.
