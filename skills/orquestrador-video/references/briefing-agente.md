# Briefing de agente (modelos)

O subagente não vê a conversa, nem a memória, nem o que os outros agentes fazem. O prompt e os arquivos no disco são o mundo inteiro dele. Por isso: objetivo, formato de saída, ferramentas, limites, tudo escrito (é a lição central do sistema de pesquisa multiagente da Anthropic: tarefa vaga = trabalho duplicado ou fora do alvo).

Preencha os `{campos}`. Não resuma os arquivos compartilhados no prompt: aponte o caminho (resumo perde decisão). Só cite a regra específica que a etapa precisa.

---

## A. Produtor de cenas (motion-design)

```
Você vai produzir as CENAS das peças {LISTA} de {PROJETO_NOME} ({FORMATO}: {W}×{H}, {FPS} fps, {narradas|só música}).
Projeto: {PROJ}. Outros {N_OUTROS} agentes fazem outras peças AO MESMO TEMPO na mesma pasta.

1. MISSÃO (uma frase por peça)
{NN}: {objetivo da peça — o que o espectador entende/sente no fim}
...

2. LEIA ANTES (nesta ordem)
- ~/.claude/skills/motion-design/SKILL.md, reference/nivel.md, reference/armadilhas.md, reference/inspiracao.md
- Doutrina de movimento: ~/.claude/plugins/cache/hyperframes/hyperframes/0.8.140/.claude/skills/motion-doctrine/SKILL.md e cut-the-curve/SKILL.md
- {PROJ}/BRIEFING.md (padrão técnico e regras do dono)
- {PROJ}/ESTILOS.md — SÓ as seções {LISTA} + "Regras que valem para todas" (+ "Ajuste do dono", se houver)
- {PROJ}/VOZES.md (texto falado) e {PROJ}/base/vozes-palavras.js (tempo de cada palavra)
- {PROJ}/base/LEIA-ME-KIT.md (kit de telas) e o piloto aprovado {PROJ}/base/{PILOTO}.html (padrão de código e de qualidade)
- Regras da marca: {MARCA_JS} ({REGRAS_CRITICAS_EM_UMA_LINHA})
- Skill hierarquia-visual (para conferir as suas folhas)

3. ARQUIVOS QUE VOCÊ CRIA (nomes EXATOS; nada além disto)
Por peça NN, em {PROJ}/base/:
- rNN-estilo.css
- rNNa-<nome-curto>.html (principal; se dividir: rNNa1-, rNNa2-…)
- rNNb-fecho.html
Em {PROJ}/cenas/: rNNa-<nome-curto>.mp4, rNNb-fecho.mp4
Em {PROJ}/reels/: NN.json (formato do cabeçalho de ~/.claude/skills/motion-design/kit/gerar_reel.py; "bitrate":"{BITRATE}")

4. NÃO TOQUE
kit e marca (comum.*, marca.*, produto-ui.*, fontes/), ESTILOS.md, VOZES.md, BRIEFING.md, vozes-palavras.js, arquivos de outras peças, remotion/, git.
Precisa mudar algo comum? Não mude: descreva no relatório ("PEDIDO AO DIRETOR: …").
Não rode gerar_reel.py nem o Remotion (a montagem é em fila, feita depois).

5. RASCUNHO
Só em {SCRATCH}/{PREFIXO}/ (ex.: fotos, folhas, scripts temporários). Nunca na raiz do scratchpad.

6. GRAVAÇÃO EM FILA (uma por vez no COMPUTADOR, não só sua)
Grave assim, sempre:
  L={PROJ}/.fila-render
  until mkdir "$L" 2>/dev/null; do sleep 5; done
  (cd {PROJ}/base && node ~/.claude/skills/motion-design/kit/hf.mjs ../cenas/<cena>.mp4 --html <cena>.html --crf 12); rc=$?
  rmdir "$L"; exit $rc
Rode com `bash -c '...'` (o zsh quebra laços). Se a trava ficar presa > 20 min sem processo do hyperframes/chrome rodando (`pgrep -fl hyperframes`), avise no relatório em vez de apagar.

7. PADRÃO TÉCNICO (do piloto)
{W}×{H}, {FPS} fps, crf 12 nas cenas; fontes LOCAIS (base/fontes/ + @font-face, elemento escondido com cada peso antes do quadro 0); zona segura {ZONA}; gancho visível no quadro 0; DUR da principal = voz + 0,3 s; toda troca numa palavra com W('palavra', k) — palavra curta/repetida: use a ocorrência certa (k) ou a palavra seguinte, mais rara.

8. CONFERÊNCIA ANTES DE DEVOLVER
- Antes de gravar: FOTOS_DIR={SCRATCH}/{PREFIXO}/fotos bash fotos.sh <cena>.html <≥12 tempos, incluindo CADA palavra-chave>; folha com grade (em pé: folha em pé com a zona segura). OLHE a folha: ilegível, sobreposto, fora da zona, fonte genérica, texto que contradiz a voz, marca proibida → corrija e fotografe de novo.
- Depois de gravar: ffprobe (duração, resolução, fps) e um quadro a ~75 % de cada MP4.

9. RESPOSTA (objeto do schema, ou texto nesta ordem)
Por peça: arquivos criados · duração de cada cena gravada · caminho da folha que você olhou · o que corrigiu depois de olhar · problemas abertos · PEDIDOS AO DIRETOR · lição nova (se houver).

10. PRONTO = existem no disco: cenas/rNNa-*.mp4, cenas/rNNb-fecho.mp4, reels/NN.json, e a folha em {SCRATCH}/{PREFIXO}/. Sem isso, não diga que terminou.
```

---

## B. Revisor independente (uma peça)

Agente novo, sem ter visto a produção. Só leitura.

```
Você é o REVISOR INDEPENDENTE da peça {NN} de {PROJETO_NOME}. Você não fez a peça e não deve corrigi-la: leia, meça e dê o veredito com evidência.
Arquivo final: {PROJ}/{PASTA_FINAIS}/{ARQUIVO}. Relatório técnico já gerado (se houver): {PROJ}/{PASTA_FINAIS}/{BASE}-revisao/revisao.txt.

Leia: skill revisao-video (~/.claude/skills/revisao-video/SKILL.md), skill hierarquia-visual, {PROJ}/BRIEFING.md, a seção {NN} de ESTILOS.md e de VOZES.md, regras da marca {MARCA_JS}.
Se o relatório técnico não existir, rode: .ferramentas/.venv/bin/python ~/.claude/skills/revisao-video/scripts/revisar.py <final> --esperado {SCRATCH}/qa-{NN}/voz.txt --saida {SCRATCH}/qa-{NN} --fotos 12 (copie antes o texto da voz da peça, do VOZES.md, para voz.txt). Nada no projeto: rascunho só em {SCRATCH}/qa-{NN}/.

Meça e responda cada item com número/tempo/foto:
1. Fala: transcrição × VOZES.md (voz inteira? diferença perto de emenda? recorte e confirme antes de acusar).
2. Mixagem: LUFS integrado (alvo {LUFS} ±1), pico (≤ -1 dBFS), voz − música (trecho com voz × fecho só música; esperado ~18–21 dB).
3. Imagem: resolução, fps, bitrate MEDIDO no arquivo (≥ {BITRATE}), quadro 0 não preto.
4. Sincronia: para cada título/troca do roteiro, o tempo na tela × o tempo da palavra (tolerância 0,3 s).
5. Fontes: as do cartão aparecem? (serif genérica = reprovado)
6. Hierarquia e legibilidade (hierarquia-visual) na folha de 12 fotos: uma leitura por tela, tamanhos mínimos, contraste.
7. Zona segura, gancho no quadro 0, fecho com a isca certa.
8. Marca: regras, dados inventados, nada proibido.
9. Direção de arte: bate com o cartão; não repete a peça vizinha ({VIZINHAS}).

Veredito: APROVADO só se nada falhar. Senão REFAZER, com a lista de falhas (item, evidência, o que corrigir, em que arquivo). Não edite nenhum arquivo do projeto.
```

---

## C. Correção (volta ao produtor)

```
A peça {NN} foi REPROVADA pelo revisor independente. Corrija SÓ isto:
{lista de falhas com evidência}
Mesmos limites do briefing original (arquivos, rascunho em {SCRATCH}/{PREFIXO}/, gravação em fila). Regrave só as cenas afetadas. Devolva o mesmo formato de resposta e diga, para cada falha, o que mudou e como conferiu.
```

> **Sempre incluir no briefing de produção:** "Réplica de interface feita à mão na cena (formulário, ficha, painel) leva `data-hv=\"ui\"` no contêiner; texto decorativo leva `data-hv=\"ignorar\"`. Antes de gravar, rode `node ~/.claude/skills/hierarquia-visual/scripts/conferir_hierarquia.mjs <cena>.html` e corrija toda FALHA que sobrar."
