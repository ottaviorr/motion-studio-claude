---
name: direcao-de-arte
description: Diretor de arte do Motion Studio. Decide o CONCEITO VISUAL de cada peça antes de produzir (cartão de direção com conceito em 1 frase, referências, paleta com um destaque, 3 fontes, textura, como o produto aparece, linguagem de movimento e o que NÃO fazer) e, depois, critica a folha de fotos e manda ajustar ou refazer. Use SEMPRE antes de começar qualquer reel, série de reels, VSL, anúncio, explicador, lançamento de produto ou motion por cima de gravação — e sempre que pedirem "estilo", "cara", "visual", "direção de arte", "conceito", "paleta", "fonte", "moodboard", "referência", "variar o estilo", "tá com cara de IA", "tá genérico", "tá feio", "dá pra ficar mais bonito?", "o que você acha do visual?", ou quando for revisar o visual de cenas antes de gravar. Também quando o dono reclamar que os vídeos estão parecidos entre si.
---

# Direção de arte (antes e depois de produzir)

O diretor de arte não anima. Ele decide **o que a peça parece e por quê**, escreve isso de um jeito que quem anima não precisa adivinhar, e depois olha o resultado com olho frio e manda ajustar. A skill **motion-design** executa; a **revisao-video** mede o técnico; esta aqui cuida da ideia visual e do gosto.

Por que existe: os vídeos feitos com IA caem sozinhos no mesmo lugar (fundo escuro, gradiente roxo, Inter, cartão com ícone redondinho, brilho, tudo flutuando). Isso não é falta de técnica, é falta de **decisão**. A série de 15 reels de exemplo ("gostei demais") só ficou boa porque cada reel teve uma direção de arte escrita antes (um `ESTILOS.md`). Esta skill transforma aquilo em processo.

## Quando entra

| Momento | O que faz | Entrega |
|---|---|---|
| **Antes** (sempre) | Briefing → 3 rotas → escolhe 1 → cartão de direção → 3 quadros-chave parados | `fonte/DIRECAO.md` (uma por peça) ou `ESTILOS.md` (série) |
| **No meio** | Confere a folha de fotos ANTES de gravar (o mais barato de corrigir) | Ordens de ajuste |
| **Depois** | Crítica da folha de fotos do final, decide ajustar × refazer | Ordens de ajuste + linha no `evolucao.md` |

Leia antes: `skill/reference/nivel.md` (o mínimo do estúdio), `skill/reference/inspiracao.md` (o que os melhores têm em comum), o `evolucao.md` da marca e a memória do dono. **Cada vídeo tem que superar o anterior** — e "superar" em direção de arte é ter uma ideia visual mais clara, não mais efeitos.

## Preferências do dono (fixas)

- **Variar a direção de arte** entre peças de uma série; logo e nome da marca ficam, o resto pode mudar.
- **Maioria em fundo claro** (ele achou escuro demais). Escuro só quando o conceito pede (madrugada, silêncio, cinema).
- **Nada de ícones redondinhos coloridos repetidos** (o "ícone-app" do reel 01 não volta).
- Legenda corrida só quando ele pedir (VSL/anúncio). Texto dentro dos motions sim.
- Ele assiste sem som no VS Code: a imagem tem que contar a história sozinha.

---

## Parte A — Do briefing ao conceito visual

### A1. Responda o briefing visual (8 perguntas, por escrito)

1. **Para quem e onde?** (Reels no celular, VSL no YouTube, aula 4K, anúncio sem som.) Define formato, tamanho de letra e zona segura.
2. **Qual a UMA coisa que a pessoa tem que lembrar?** Se forem duas, são duas peças.
3. **O que ela deve SENTIR?** Três palavras (ex.: "calma, controle, alívio"). O estilo sai do sentimento, não do assunto.
4. **Qual a virada?** Todo bom vídeo tem um antes → depois (caos → ordem, noite → manhã, silêncio → resposta). A virada é onde a direção de arte pode mudar de propósito.
5. **Como o produto aparece?** Tela real, réplica, objeto (celular, cupom, painel), metáfora (planta técnica, aviãozinho de papel)? O produto é o herói ou o pano de fundo?
6. **O que a marca exige e o que proíbe?** `marcas/<marca>/marca.css` e `MARCA.regras` (preços, nomes, promessas). Cor e logo da marca são sagrados; a aplicação é sua.
7. **O que já fizemos para essa marca?** `evolucao.md` + estilos já usados. Não repita a família de estilo da peça anterior.
8. **Qual o risco de ficar genérico?** Diga em voz alta o clichê do tema (CRM → dashboard roxo com cards; finanças → gráfico subindo azul) para fugir dele.

### A2. Gere 3 rotas, escolha 1

Escreva três rotas bem diferentes, cada uma com nome, conceito em 1 frase e o quadro de abertura descrito. Escolha pelo critério: **qual serve melhor à pergunta 2 e 3 e qual o espectador nunca viu nesta marca**. A primeira ideia costuma ser a média do que a IA já viu — por isso três.

Formas de chegar num conceito (detalhe em `references/conceito.md`):
- **Objeto-personagem:** uma coisa atravessa o vídeo e se transforma (o card que anda pelo funil; o formulário que vira aviãozinho).
- **Regra formal única:** uma lei que vale para o vídeo inteiro ("uma forma que nunca corta"; "as palavras têm papéis de arquitetura").
- **Mundo/cenário:** a peça acontece num lugar (quarto de madrugada, painel de aeroporto, sala de controle).
- **Material/meio:** papel, xerox, risografia, planta técnica, cupom térmico, caderno.
- **A virada como troca de estilo:** o antes num estilo, o depois em outro (xerox tremendo a 15 fps → papel limpo a 60 fps).

O conceito bom cabe numa frase, dá para desenhar o quadro de abertura na cabeça, e se sustenta pela duração toda (reel de 1min30 precisa de uma ideia que renda várias cenas).

### A3. Escreva o cartão de direção

Use o modelo `assets/cartao-direcao.md`. Campos obrigatórios:

- **Conceito em 1 frase** + o sentimento (3 palavras).
- **Referências (2–3), cada uma com a função:** "a cor vem de X, o movimento de Y". Use o catálogo `references/repertorio-estilos.md`, slugs do skillry (prompts em `github.com/yihui-dev/awesome-opus5-5-videos/data/videos.json`) e os nossos exemplos. Referência sem função vira cópia.
- **Paleta:** fundo · tinta · **UM** destaque, com hex, e a **regra de uso do destaque** (onde ele pode aparecer). Neutros puxados para a cor do conceito; nunca `#000`/`#fff` puros sem motivo.
- **Tipografia em 3 papéis:** título (grito) / apoio / número-rótulo. Fontes do Google com o nome exato. Não juntar duas sem-serifa parecidas; evitar as fontes-padrão de IA (lista em `references/anti-ia.md`) a não ser com motivo.
- **Textura:** grão, halftone, papel, grade, nenhuma — e a intensidade. "Nenhuma" também é escolha (suíço, keynote).
- **Como o produto aparece** e **quais ícones** (traço, espessura, cantos) — ou "nenhum ícone".
- **Linguagem de movimento:** a corrente (uma direção dominante), a assinatura (1 movimento que só esta peça tem), 2–3 transições no máximo, e o ritmo (com a voz `W()` ou na batida). Segue a motion-doctrine do HyperFrames: corte no meio do movimento, objeto que carrega o olho, nada de balançar parado, pausa de 0,3–0,75 s antes do clímax, sem quique.
- **O que NÃO fazer** (5–8 itens, específicos desta peça). A lista de banidos é tão importante quanto o resto.
- **3 quadros-chave** (abertura, virada, fecho) descritos como fotografia: o que está onde, qual cor domina, qual palavra está na tela.

### A4. Prove com quadros parados antes de animar

Quadro-chave (style frame) é o contrato visual: estúdios como a Buck fazem quadros finais parados antes de animar porque mudar uma imagem custa minutos e mudar uma animação custa horas. No nosso fluxo: escreva só o estado final das 3 cenas-chave, fotografe com `FOTOS_DIR=... bash fonte/fotos.sh cena.html <t>` e critique (Parte C) **antes** de escrever as animações. Se o quadro parado não é bonito, a animação não salva.

Depois, passe o cartão para a **motion-design** (cada cena cita o cartão no topo do HTML como comentário) e siga.

---

## Parte B — Unidade × variedade numa série

Uma série tem que parecer **a mesma marca** e **peças diferentes**. A Figma resume: *restrinja o conceito, não a execução*. Detalhe e matriz em `references/serie.md`.

**Núcleo fixo (nunca muda):** logo e nome, estrutura do fecho (CTA, "link na bio"), regras de texto da marca, voz/narrador, qualidade técnica (4K/60 fps, CBR, -14 LUFS), zona segura, dados inventados, tamanho mínimo de letra.

**Variáveis (mudam por peça):** paleta, família tipográfica, textura/material, como o produto aparece, conjunto de ícones, linguagem de movimento e corrente, música.

**Regras da série:**
1. Escreva a bíblia (`ESTILOS.md`) **inteira antes** de produzir a primeira peça, com tabela-resumo. Assim dá para ver repetição de longe.
2. **Vizinhos nunca repetem** a mesma família (claro/escuro + matiz do fundo), a mesma fonte de título nem a mesma escola.
3. **Pelo menos 60% em fundo claro** (preferência do dono). Conte na tabela.
4. A cor da marca vira **um** momento (destaque, virada ou fecho), não o fundo de todas.
5. **Kit re-tematizável:** telas do produto num kit único com variáveis CSS; cada peça sobrescreve com `estilo-NN.css`. Variar estilo não pode custar refazer o produto.
6. Rode `python3 scripts/conferir-serie.py ESTILOS.md` (lê os blocos `cartao` e aponta vizinhos repetidos, % claro, fontes banidas e contraste ruim).

---

## Parte C — Crítica de arte (depois)

Crítica não é gosto. Cada observação liga **um elemento** a **um objetivo** do cartão ou do briefing e diz o **efeito**. Método completo, checklist com números e exemplos em `references/critica.md`.

### C1. Como olhar a folha de fotos (nesta ordem)

1. **Miniatura e olho apertado.** Veja a folha pequena, depois borrada e em cinza (`bash scripts/apertar-olho.sh folha.jpg`). O que sobra é a hierarquia real. Tem UM ponto que puxa o olho em cada quadro?
2. **Quadro 0 = capa.** O primeiro quadro funciona parado, sozinho, no feed?
3. **Fidelidade ao cartão.** Paleta (alguma cor fora?), fontes (alguma trocada?), textura, ícones, como o produto aparece. Tudo que não está no cartão é suspeito.
4. **Hierarquia e leitura.** No máximo 3–4 palavras por tela, título ≥ 84 px em 9:16, contraste suficiente, nada importante fora da zona segura (y 230–1300 em 1080×1920).
5. **Composição.** Peso ancorado (canto, borda, grade), não tudo centralizado flutuando; espaço vazio de propósito; o produto grande o bastante para ler.
6. **Sequência.** Lendo os quadros em ordem, a história aparece sem som? A virada é visível? Os quadros vizinhos parecem a mesma peça?
7. **Movimento** (no vídeo, não na folha): a corrente é respeitada, a assinatura aparece, nada balançando parado, final parado tempo suficiente para ler.
8. **Sinais de IA** (`references/anti-ia.md`).

### C2. Escreva ordens de ajuste, não opiniões

Formato fixo: **onde (cena + tempo) · o que está · por que atrapalha (ligado ao objetivo) · o que fazer · como conferir.**

- Ruim: "o título tá meio fraco".
- Bom: "Cena 03, 2,4 s · título 'Seu funil anda sozinho' em 64 px, mesma cor dos cards · some na miniatura, e é a frase que o reel tem que deixar · subir para 110 px, tinta `#111` sobre o papel, cards recuam para 40 % de opacidade · conferir na folha apertada: o título é a primeira coisa que aparece."

Comece pelo que funciona (para não perder no ajuste), depois as ordens por gravidade: **bloqueia** (não entrega), **deve** (entrega pior sem), **pode** (polimento).

## Parte D — Ajustar ou refazer?

| Sintoma | Decisão |
|---|---|
| Problema local (tamanho, cor de um elemento, tempo de entrada, um ícone fora do conjunto) | **Ajuste** na cena, regrave só ela |
| A cena não comunica a frase, ou o quadro parado é feio mesmo arrumando detalhes | **Refaça a cena** (mesmo cartão, outra composição) |
| Mais de 1/3 das cenas com o mesmo problema, ou a peça parece a anterior, ou dá para trocar o logo e ela vira "qualquer marca" | **Volte ao conceito** (Parte A), escolha outra rota |
| Bonito mas o espectador não entende a mensagem sem som | **Volte ao briefing**: o conceito está servindo ao estilo, não à mensagem |
| Fica com cara de IA mesmo com o cartão cumprido | O cartão estava genérico: reescreva o conceito com objeto/material mais específico |

Refazer cedo é barato. Na dúvida, refaça a partir dos quadros parados, não do vídeo gravado.

## Depois de entregar (ciclo de aprendizado)

- Linha no `marcas/<marca>/evolucao.md`: estilo usado (nome do catálogo), reação do dono.
- Estilo novo que funcionou → acrescente no `references/repertorio-estilos.md` com o exemplo nosso.
- Crítica que se repetiu → vira item do checklist em `references/critica.md` ou do `nivel.md` da motion-design.
- Reação do dono a um estilo ("achei escuro", "gostei demais") → anote no catálogo (campo "reação do dono").

## Arquivos

- `references/conceito.md` — briefing visual, geradores de conceito, moodboard em texto, quadros-chave.
- `references/repertorio-estilos.md` — 27 direções de arte prontas (paleta, fontes Google exatas, textura, movimento, quando usar e quando não).
- `references/serie.md` — unidade × variedade, matriz de rotação, exemplo.
- `references/critica.md` — método de crítica, checklist com números, modelos de ordem de ajuste.
- `references/anti-ia.md` — sinais de "feito por IA" e o antídoto de cada um.
- `assets/cartao-direcao.md` — modelo do cartão (copie para `fonte/DIRECAO.md`).
- `assets/estilos-serie-modelo.md` — modelo da bíblia de uma série.
- `scripts/conferir-serie.py` — confere a série (vizinhos, % claro, fontes, contraste).
- `scripts/apertar-olho.sh` — folha em miniatura, borrada e em cinza (teste do olho apertado).
