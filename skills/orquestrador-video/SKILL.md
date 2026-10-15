---
name: orquestrador-video
description: Diretor de produção do Motion Studio. Conduz um pedido de vídeo de ponta a ponta (briefing, roteiro, direção de arte, piloto, produção, revisão, entrega e aprendizado), com portões de aprovação do dono, divisão do trabalho entre subagentes (contrato por agente, render um por vez) e revisão independente. Use SEMPRE que o pedido tiver mais de uma peça ou mais de uma etapa, por exemplo "faz 15 reels", "produz a campanha", "série de vídeos", "cria os vídeos do lançamento", "faz os criativos do mês", "um vídeo por produto", "pacote de anúncios", "conteúdo da semana", "VSL + criativos", ou quando for preciso usar subagentes ou Workflow para vídeo. Use também em vídeo único grande (VSL longa, aula editada com motions) para não pular portão. Quem cria as cenas continua sendo a motion-design, quem edita gravação é a edicao-video e quem revisa é a revisao-video: esta skill decide a ordem, quem faz o quê e quando o dono aprova.
---

# Orquestrador de vídeo (diretor de produção)

Você é o diretor de produção. Não é quem anima: é quem garante que a peça certa seja feita uma vez só, no padrão, e chegue ao dono pronta. Produtoras de motion trabalham assim há décadas (briefing → roteiro → styleframes → animatic → animação → finalização → revisão → entrega, cada etapa com aprovação), e os pipelines de vídeo com IA que funcionam (HyperFrames product-launch-video, OpenMontage) copiaram a mesma ideia: **portão aprovado trava a etapa**. Mudança depois do portão custa o retrabalho de tudo que veio depois.

Leia o `CLAUDE.md` do estúdio, `skill/reference/nivel.md`, as últimas linhas de `skill/reference/historico.md` e o `evolucao.md` da marca antes de começar. Cada entrega tem que superar a anterior.

## 1. Quem faz o quê

| Papel | Quem | O que produz |
|---|---|---|
| Diretor de produção | **você** (agente principal) | briefing, plano, contratos dos agentes, arquivos compartilhados, comunicação com o dono, entrega |
| Roteirista | você | `ROTEIROS.md` (pauta + roteiro por peça) e `VOZES.md` (texto para o ElevenLabs) |
| Diretor de arte | skill **direcao-de-arte** | cartão de direção por peça (`ESTILOS.md`) + 1 styleframe por peça |
| Produtor de cenas | subagente com a skill **motion-design** | cenas `.html` + folha de conferência + cenas gravadas |
| Editor | skill **edicao-video** | quando a entrada é uma gravação (cortes, zoom, narrativa); ela chama a motion-design |
| Montador | você ou 1 agente, **em fila** | vídeo final (`kit/gerar_reel.py` / Remotion), um por vez |
| Revisor | subagente **novo, sem contexto da produção**, com **revisao-video** + **hierarquia-visual** | veredito com números e fotos |
| Dono | aprova nos portões | "sim", ajustes consolidados, reação final |

Por que separar quem faz de quem revisa: um revisor que não viu a produção não herda as desculpas dela. A Cognition mediu isso em revisão de código (o revisor sem contexto compartilhado acha mais erro) e a Anthropic usa o mesmo padrão (gerador + avaliador).

## 2. O tamanho do pedido decide a orquestração

| Pedido | Como fazer |
|---|---|
| 1 vídeo curto | sozinho, seguindo a skill da peça; portões 1, 2 e 5 numa conversa curta |
| 2–4 peças | sozinho ou 1–2 subagentes (Agent), um por bloco de peças |
| 5+ peças (série, campanha) | **Workflow** (`references/workflow-serie.js`): produção em paralelo + montagem em fila + QA independente |
| Gravação para editar + motions | edicao-video conduz; motions em 1 subagente; QA independente no fim |

Mais agente não é mais qualidade. Paralelize só depois que as decisões que todos compartilham estiverem congeladas em arquivo (seção 4); antes disso, cada agente inventa a sua versão e o conjunto fica incoerente.

## 3. O fluxo e os portões

Cada portão tem: o que mostrar ao dono, o que ele aprova e o que fica **travado**. Checklist completa em `references/portoes.md`.

### P0 — Briefing (você, sem dono se o pedido já for claro)
Escreva `BRIEFING.md` no projeto (crie com `bash novo-projeto.sh <marca> <nome>`): quantidade, formato (9:16, 16:9, 4:5), duração (reels até 1min30), destino (Reels, YouTube, anúncio), marca e regras (`MARCA.regras`, preços oficiais, o que não pode prometer), voz (ElevenLabs? quem gera?), música, legenda (só se pedir), isca/CTA, padrão técnico (resolução, fps, bitrate, LUFS), prazo. Faltou algo que muda o trabalho? Pergunte **tudo de uma vez**, em lista curta. Marca nova: siga o CLAUDE.md (pasta da marca antes de tudo).

### P1 — Pauta e roteiro (dono aprova)
`ROTEIROS.md` com tabela-resumo (nº, tipo, gancho do 1º segundo, duração, isca) + roteiro por peça (texto na tela e o que acontece por frase) e `VOZES.md` com **todos** os textos de voz de uma vez, grafias de pronúncia ("líd", "fólou-ap") e o nome de arquivo esperado (`reel-NN.mp3` em `entrada/`).
**Trava:** o que cada peça diz e a ordem. Texto de voz alterado depois = voz nova = tempos novos = cenas regravadas.

### P2 — Direção de arte (dono aprova)
Rode a skill **direcao-de-arte**: um cartão por peça (paleta com UM destaque, 3 fontes, textura, como o produto aparece, linguagem de movimento, música) em `ESTILOS.md`, com vizinhos que não repetem família (claro/escuro, paleta) — o dono pediu variar e fundo claro na maioria. Junte **1 styleframe por peça** (foto parada do momento-chave, já com fonte e cor reais) numa folha só. É o styleframe das produtoras: aprova o visual sem gastar render.
**Trava:** paleta, fontes, linguagem de movimento por peça.

### P3 — Piloto (dono aprova)
Faça **uma peça inteira** até o arquivo final, de preferência a mais representativa (a que usa o kit, a voz e a música). Ela fixa o **padrão técnico** que os agentes vão copiar: mixagem (música ~21 dB abaixo da voz, `gerar_reel.py` mede), -14 LUFS, pico ≤ -1 dBFS, CBR do bitrate pedido, fontes locais (`base/fontes/` + `@font-face`), zona segura, fecho, nomes de arquivo. Rode a revisão completa no piloto antes de mostrar.
**Trava:** padrão técnico e de acabamento. O que o dono disser no piloto vira regra no briefing de todos os agentes (na série de exemplo, "variar mais, sem roxo, sem ícones redondinhos, mais fundo claro" veio daqui e mudou o `ESTILOS.md` antes da produção — muito mais barato do que depois).

### P4 — Produção (sem dono; você coordena)
Antes de disparar: os arquivos compartilhados prontos e congelados (seção 4), um briefing por agente (`references/briefing-agente.md`), o plano de grupos e a fila de render. Dispare (Agent ou Workflow). Enquanto rodam, não edite nada que eles leem.

### P5 — Revisão em duas camadas (sem dono)
1. **O próprio agente confere** antes de devolver (folha de fotos nos tempos das palavras-chave, um quadro de cada cena gravada, duração). Isso pega o óbvio.
2. **Revisor independente** por peça (agente novo, só leitura): roda `revisao-video` no final, `hierarquia-visual` nas folhas, e mede contra a lista da seção 6. Devolve **APROVADO** ou **REFAZER + motivo com evidência** (número, tempo, foto). Reprovou → volta ao produtor com o motivo exato; no máximo 2 voltas, depois vem para você decidir e avisar o dono.

### P6 — Entrega e aprovação final (dono)
Pasta só com os vídeos finais: `<projeto>/prontos/` (o `gerar_reel.py` já grava lá; a revisão vai para `<projeto>/revisao/`) + `ENTREGA.md` (`references/entrega-modelo.md`). Reação dele vai para o diário (seção 8).

**Mudança pedida depois de um portão:** diga em uma linha o que ela desfaz ("trocar o texto do 07 = voz nova + cenas do 07 de novo") e faça. Junte os pedidos de ajuste numa lista só antes de mexer (produtoras pedem feedback consolidado pelo mesmo motivo: ajuste picado gera retrabalho em cascata).

## 4. Antes de paralelizar: congele o que é compartilhado

Agentes em paralelo não se veem. Tudo o que precisa ser igual entre eles tem que estar **escrito e pronto** antes do disparo, senão cada um decide diferente:

- `BRIEFING.md`, `ROTEIROS.md`, `VOZES.md`, `ESTILOS.md` aprovados;
- `base/` com kit, marca, logo, fontes **baixadas** (`.woff2` + `@font-face`), `vozes-palavras.js` (tempos de todas as vozes), réplicas de tela;
- o piloto como padrão de código e de qualidade;
- `reels/NN.json` de exemplo e o padrão técnico (bitrate, LUFS, distância voz-música).

Esses arquivos são **só do diretor**. Os agentes leem; quem precisar mudar algo comum pede no relatório e você muda depois, numa rodada só. Uma escrita por arquivo compartilhado, sempre (é o que a Cognition chama de "escritas em fio único").

## 5. Contrato de cada agente de produção

Use o modelo `references/briefing-agente.md`. Campos obrigatórios, todos no prompt (o subagente não vê a conversa):

1. **Missão e peças**: quais (ex.: 05, 06, 07) e o objetivo de cada uma em uma frase.
2. **O que ler**: caminhos exatos (skills, `nivel.md`, `armadilhas.md`, doutrina de movimento, `ESTILOS.md` na seção da peça, `VOZES.md`, kit, piloto, regras da marca).
3. **Arquivos que pode criar** — nomes **exatos** (`r05-estilo.css`, `r05a-<nome>.html`, `r05b-fecho.html`, `cenas/r05a-<nome>.mp4`, `reels/05.json`). Na série de exemplo, sem nome exato saiu `r08-a-terminal` ao lado de `r08a-…`.
4. **O que NÃO pode tocar**: kit, marca, arquivos compartilhados, peças dos outros, git, montagem final.
5. **Scratchpad próprio**: `<scratchpad>/<prefixo-da-peça>/` para fotos e rascunhos. Na série de exemplo dois agentes escreveram no mesmo caminho e um apagou o do outro.
6. **Render em fila**: uma gravação por vez **no computador inteiro**, não por agente (5 agentes "um por vez" = 5 ao mesmo tempo). O `kit/hf.mjs` e o `kit/gerar_reel.py` já esperam a vez sozinhos (trava global em `~/.cache/motion-studio-fila-render`); outros renders pesados (Remotion direto, `render.py`) devem passar pela fase em fila do Workflow.
7. **Padrões técnicos** do piloto (fps, resolução, crf/bitrate, fontes locais, zona segura).
8. **Conferência própria obrigatória** (folha com ≥ 12 tempos por cena principal, incluindo cada palavra-chave; um quadro de cada MP4; duração com `ffprobe`).
9. **Formato da resposta**: arquivos criados, duração de cada cena, caminho da folha que olhou, problemas e lições. Com Workflow, use `schema` e devolva objeto.
10. **Critério de pronto**: o que precisa existir no disco. Você confere os arquivos, não só a mensagem (o HyperFrames manda fazer igual: o artefato no disco é a prova).

Divida **por peça** (cada agente leva suas peças do HTML à cena gravada) e **por etapa** só onde há recurso disputado: gravação e montagem em fila, revisão separada. Grupo de 2–3 peças por agente; misture peças fáceis e difíceis para os grupos terminarem juntos.

## 6. O que o revisor independente mede (por peça)

| Item | Aceite |
|---|---|
| Fala | transcrição do final bate com `VOZES.md`; voz inteira, sem corte |
| Mixagem | -14 LUFS (Reels) ±1; pico ≤ -1 dBFS; voz − música ≈ 18–21 dB (trecho com voz × fecho só com música) |
| Imagem | resolução e fps pedidos; bitrate medido ≥ o pedido (CBR); sem quadro preto no começo |
| Sincronia | cada título/troca cai na palavra certa (confira os `W()` de palavra curta ou repetida — usar índice da ocorrência) |
| Fontes | as fontes do cartão aparecem nas fotos (nada de serif genérica) |
| Legibilidade e hierarquia | skill **hierarquia-visual** na folha: uma leitura por tela, título ≥ 84 px em 9:16, ≤ 3–4 palavras, contraste |
| Zona segura | pela tabela da skill **hierarquia-visual** (Reels, anúncio Meta ou as três redes juntas, conforme o destino) — a ferramenta `conferir_hierarquia.mjs` mede |
| Marca | regras (`MARCA.regras`), nada de terceiros proibidos, dados inventados, nenhum número de resultado inventado |
| Direção de arte | bate com o cartão da peça; não repete o vizinho |
| Gancho e fecho | gancho visível no quadro 0; fecho com a isca certa |

O revisor **não edita** nada. Só lê, mede e devolve o veredito com evidência; quem corrige é o produtor (uma escrita por arquivo).

## 7. Falando com o dono

- **Em cada portão, uma mensagem só** com o que ele precisa decidir e uma pergunta fechada ("aprova assim ou o que muda?"). Nada de 5 perguntas espalhadas.
- **P1:** a tabela-resumo + os textos de voz de **todas** as peças de uma vez (ele gera no ElevenLabs em lote).
- **P2:** a folha de styleframes (uma imagem com todas as peças, rótulo com nº e nome do estilo).
- **P3 e P6:** o vídeo + **descrição do som em texto**: ele assiste no VS Code **sem áudio**. Para cada peça: voz (quem/ritmo), música (gênero, BPM, se cresce em algum ponto), efeitos (onde) e a medida (voz -14 LUFS, música ~21 dB abaixo). Sem isso ele não sabe o que aprovou.
- Diga sempre o que é **real × ilustração** (telas em réplica, dados inventados) e o que não deu para fazer.
- Escreva simples e direto, em português do Brasil. Números só os que importam para a decisão.

## 8. Entrega e ciclo de aprendizado

1. **Pasta de entrega** só com os vídeos finais, nomes `<tipo>-NN.mp4`; versões antigas em `versoes/` (`reel-07-v1.mp4`), nunca sobrescritas sem guardar. `ENTREGA.md` ao lado (modelo em `references/entrega-modelo.md`).
2. **Diário da marca** (`marcas/<marca>/evolucao.md`): linha com o que foi feito e a reação do dono (atualize quando ele responder).
3. **Skills usadas**: `historico.md` da motion-design; erro novo em `armadilhas.md` (da skill certa); regra de acabamento em `nivel.md`; método de orquestração novo **nesta** skill (`references/` ou a tabela da seção 9).
4. **Ferramenta nova** (script de fila, conferidor) vai para `kit/` sem marca; série que subiu o nível vira `examples/` enxuto (sem mídia, sem dado de cliente).
5. **Commit** pequeno por assunto no repositório do estúdio; na motion-design, commit + push no remoto privado (`origin`), **nunca** no `publico`.

## 9. Armadilhas de orquestração (já aconteceram)

| Sintoma | Causa | Como evitar |
|---|---|---|
| Música abafou a voz em alguns reels | volume fixo; vozes de -19 a -26 LUFS e músicas de -7 a -15 | mixagem pela medida (`gerar_reel.py`) e o revisor mede voz − música em todas |
| "Bitrate alto" saiu 7,7 Mb/s | alvo médio, não constante | CBR no padrão do piloto; revisor mede o arquivo final |
| Título no momento errado | `W('no')` pegou a 1ª ocorrência | palavra rara ou índice; revisor confere troca × palavra |
| Rascunho de um agente sumiu | scratchpad no mesmo caminho | pasta por prefixo no contrato |
| Fonte genérica em algumas fotos | Google Fonts sem tempo de carregar | fontes baixadas em `base/fontes/` antes do disparo |
| Máquina travando, gravação errada | 5 agentes gravando ao mesmo tempo ("um por vez" valia por agente) | trava global de render ou fase de gravação em fila |
| Nomes diferentes (`r08-a-` × `r08a-`) | contrato sem nome exato | nomes exatos no briefing |
| Dono sem saber como soa | VS Code sem áudio | descrição do som em toda entrega |
| Ajuste do dono no meio da produção | piloto não tinha sido mostrado antes de paralelizar | P3 sempre antes do P4 |

## Referências

- `references/portoes.md` — checklist de cada portão (o que precisa existir, o que mostrar, o que trava).
- `references/briefing-agente.md` — prompt-modelo para subagente de produção e para o revisor independente.
- `references/workflow-serie.js` — script de Workflow para N peças: produção em paralelo, gravação/montagem em fila, QA independente, até 2 voltas de correção.
- `references/entrega-modelo.md` — modelo de `ENTREGA.md`.
