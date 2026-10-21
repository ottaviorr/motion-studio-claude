# Relatório de pesquisa — skill orquestrador-video

Data: 08/10/2026. Papel: diretor de produção (orquestrador) do Motion Studio.

## O que foi lido no estúdio
- `CLAUDE.md` do estúdio, memórias do dono (`edicao-de-video.md`, `reels-variedade.md`).
- Skills: motion-design (SKILL.md, `nivel.md`, `armadilhas.md`, `historico.md`, `motores.md`, `kit/gerar_reel.py`), edicao-video, revisao-video (`revisar.py`).
- Projeto `projetos/<projeto>/`: ROTEIROS.md, ESTILOS.md, VOZES.md, ENTREGA.md, `reels/*.json`, `base/` (nomes das cenas por agente), pastas `reels/` e `reels-prontos/`.
- Script de Workflow real: `<pasta-de-workflows>` (5 grupos, `parallel`, uma fase, sem montagem nem QA dentro do fluxo).
- Plugin HyperFrames 0.8.140: `product-launch-video/SKILL.md`, `hyperframes/references/{brief-contract,review-loop,production-loop,subagent-dispatch}.md`.
- skill-creator (formato, descrição "insistente", corpo imperativo explicando o porquê) e workflow-authoring (API `agent/pipeline/parallel/phase/log`, `schema`, sem `Date.now`, `pipeline` como padrão, retomada por cache).
- Rascunhos paralelos: só a pasta `hierarquia-visual/` existia (vazia de SKILL.md); `direcao-de-arte` ainda não. A skill conta com as duas pelo nome e diz o que cada uma entrega.

## O que aconteceu na série de 15 reels (diagnóstico)
| Problema | Causa de orquestração |
|---|---|
| Música alta sob a voz | padrão técnico não estava fixado antes de paralelizar; ninguém media voz − música |
| Bitrate abaixo do pedido | "bitrate alto" virou alvo médio; o QA não comparava o medido com o pedido |
| Títulos fora de hora | `W()` pegou a 1ª ocorrência; a conferência do agente não cruzava troca × palavra |
| Scratchpad sobrescrito | rascunho num caminho comum |
| Fontes que não carregavam | Google Fonts em vez de fontes locais na `base/` antes do disparo |
| Renders simultâneos | a regra "uma gravação por vez" valia por agente; 5 agentes = 5 juntas |
| Nomes inconsistentes | `r08-a-terminal` × `r08a-…` (contrato sem nome exato) |
| Dono sem ouvir | VS Code sem áudio; o ENTREGA.md resolveu com a coluna "Som" |
| Duas pastas de finais | `reels/` (gerador) e `reels-prontos/` (entrega) sem regra escrita |

## Fontes externas
- Processo de produtoras de motion: [Motion Media — workflow do briefing ao render](https://www.motionmedia.com/mm-blog/motion-graphics-workflow-from-brief-to-final-render/); [Mechanism Digital — trust the process](https://www.mechanismdigital.com/post/trust-the-process); [Yans Media — guia de revisões em animação](https://www.yansmedia.com/blog/animation-revisions-guide); [Pixune — custos escondidos](https://pixune.com/Insights/hidden-costs-in-animation-production-budgets/); [Motion The Agency — revisão menor × maior](https://www.motiontheagency.com/blog/revisions-in-3d-animation).
- Versionamento/naming em pós: [Netflix Backlot — nomes de shot e versão](https://backlothelp.netflix.com/hc/en-us/articles/360057627473-VFX-Shot-and-Version-Naming-Recommendations); [fast.io — VFX pipeline](https://fast.io/resources/vfx-pipeline/).
- Pipelines de vídeo com IA: [OpenMontage (calesthio)](https://github.com/calesthio/OpenMontage) — research → proposal → script → scene plan → assets → edit → compose, portões humanos obrigatórios, checkpoints JSON retomáveis, auto-revisão pós-render (ffprobe, 4 quadros, áudio); HyperFrames `product-launch-video` (local) — gates por etapa, um worker por frame com pacote fechado, `handoff_in/out` numérico entre frames vizinhos, blocos instalados antes do paralelo, "o artefato no disco é a prova", render só depois da prévia aprovada; [/brag](https://cdn.jsdelivr.net/gh/latent-spaces/brag@main/README.md) — a skill dona da história entrega um brief de composição ao motor; [video-shotcraft](https://gittrend.io/repo/Vincentwei1021/video-shotcraft) — cartões de plano (152 receitas) como vocabulário fechado; [Claude Code Video Toolkit](https://github.com/wilwaldon/Claude-Code-Video-Toolkit) — perfis de marca e ciclo de projeto multi-sessão; [hyperframes-student-kit](https://www.skills.sh/nateherkai/hyperframes-student-kit) — skills separadas por etapa (história, estilo, cortes, batidas).
- Orquestração multiagente: [Anthropic — sistema de pesquisa multiagente](https://www.anthropic.com/engineering/multi-agent-research-system) (tarefa com objetivo/formato/ferramentas/limites; esforço proporcional; artefatos no sistema de arquivos; retomar em vez de recomeçar); [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (orquestrador-trabalhadores, portões entre etapas, avaliador-otimizador); [Cognition — Don't build multi-agents](https://cognition.ai/blog/dont-build-multi-agents) (decisões implícitas conflitantes entre agentes paralelos) e [Multi-agents: what's actually working](https://cognition.com/blog/multi-agents-working) (escritas em fio único; revisor sem contexto compartilhado acha mais erro).

## As 10 lições mais valiosas
1. **Portão aprovado trava a etapa.** Roteiro → direção de arte → piloto → produção. Mudança depois do portão desfaz tudo o que veio depois (produtoras cobram por isso; nós pagamos em render). Diga ao dono o custo em uma linha e junte os ajustes numa lista só.
2. **Styleframe antes de animar.** Uma foto parada por peça com fonte e cor reais aprova o visual sem gastar gravação (é o "sketch pass" do HyperFrames e o styleframe das produtoras).
3. **Piloto completo antes de paralelizar.** Ele fixa o padrão técnico (mixagem medida, CBR, LUFS, fontes locais, nomes) e traz a reação do dono quando ainda é barato mudar. No cliente A, "variar mais e fundo claro" veio do piloto.
4. **Congele o que é compartilhado antes do disparo.** Agentes paralelos não se veem; o que não estiver escrito eles decidem cada um de um jeito (Cognition). `ESTILOS.md`, kit, fontes, tempos das vozes e o piloto são a "memória comum".
5. **Uma escrita por arquivo.** Arquivo compartilhado só o diretor edita; cada agente só toca o que tem o prefixo dele; o revisor só lê. Pedido de mudança comum vem no relatório.
6. **Contrato com nomes exatos e critério de pronto no disco.** Objetivo, leituras, arquivos permitidos (nomes literais), proibidos, rascunho, fila, padrão técnico, conferência, formato de resposta e "pronto = estes arquivos existem". Confira o disco, não a mensagem.
7. **Recurso pesado tem fila global, não por agente.** Gravação, montagem e medição passam por uma trava única (`mkdir` atômico). Scratchpad por prefixo. Disco conferido antes do 4K.
8. **Divida por peça, serialize por recurso.** Cada agente leva 2–3 peças do HTML à cena gravada (dono da coerência da peça); montagem e medição em fila; revisão em agente separado. `pipeline` em vez de barreira: um grupo revisa enquanto outro produz.
9. **QA em duas camadas, a segunda independente e medida.** O agente confere a própria folha; um revisor novo, sem contexto da produção e sem permissão de editar, mede contra números (LUFS, pico, voz − música, bitrate medido ≥ pedido, troca × palavra, fontes, zona segura, hierarquia) e devolve APROVADO/REFAZER com evidência. Máximo 2 voltas, depois decisão humana.
10. **Mostre ao dono o que ele consegue avaliar.** Uma mensagem por portão com pergunta fechada; todos os textos de voz de uma vez; folha de styleframes; e o som descrito em texto em toda entrega (ele não ouve no VS Code). Real × ilustração sempre. Depois: diário, histórico, armadilhas, commit/push — a próxima série começa do nível desta.

## Como a skill amarra as outras
| Etapa | Skill | O que a orquestradora exige dela |
|---|---|---|
| P0–P1 briefing e roteiro | (a própria) | `BRIEFING.md`, `ROTEIROS.md`, `VOZES.md` |
| P2 direção de arte | **direcao-de-arte** | cartão por peça em `ESTILOS.md` + styleframe por peça; vizinhos sem repetir |
| P3–P4 cenas | **motion-design** | cenas no kit, `W()` na voz, folha de fotos, gravação pelo HyperFrames na fila, `reels/NN.json` |
| gravação para editar | **edicao-video** | narrativa, cortes, zoom; chama a motion-design para motions; render 4K |
| montagem | motion-design `kit/gerar_reel.py` / Remotion | um por vez, mixagem medida, CBR |
| P5 revisão | **revisao-video** + **hierarquia-visual** | relatório medido + leitura de hierarquia nas folhas, por um revisor independente |
| P6 e depois | (a própria) + ciclo de aprendizado de cada skill | `ENTREGA.md`, diário da marca, histórico/armadilhas/nível, commit/push |

## Arquivos entregues
- `SKILL.md` — fluxo, portões, papéis, divisão do trabalho, contrato, QA, comunicação, entrega, armadilhas.
- `references/portoes.md` — checklist por portão.
- `references/briefing-agente.md` — prompts-modelo: produtor, revisor independente, correção.
- `references/workflow-serie.js` — Workflow (produção → montagem em fila → revisão independente → correção, até 2 voltas), sintaxe conferida com `node --check`. Não foi executado.
- `references/entrega-modelo.md` — modelo de `ENTREGA.md`.

## Pendências
- Ajustar os nomes das skills `direcao-de-arte` e `hierarquia-visual` se mudarem, e apontar para o formato real do cartão de direção e da checagem de hierarquia quando existirem.
- A trava `.fila-render` é uma convenção: vale a pena virar um script no `kit/` (`fila.sh <comando>`) e entrar no `.gitignore`.
- Decidir uma única pasta de finais (o gerador escreve em `reels/`; o dono recebeu `reels-prontos/`).
