# Checklist dos portões

Marque cada item antes de passar. Item que não se aplica: escreva "n/a" e o porquê. Portão com ★ precisa do "sim" do dono; os outros são seus.

## P0 — Briefing
- [ ] Projeto criado (`bash novo-projeto.sh <marca> <nome>`) e `entrada/` movida para ele (pasta `entrada/` limpa)
- [ ] `BRIEFING.md` com: quantidade · formato · duração · destino · marca e `MARCA.regras` · voz (quem gera, qual voz) · música · legenda (só se pedida) · isca/CTA · padrão técnico (resolução, fps, bitrate CBR, -14 LUFS / -16 em YouTube) · prazo
- [ ] Lidos: `nivel.md`, fim do `historico.md`, `evolucao.md` da marca, memórias do dono
- [ ] Dúvidas que mudam o trabalho perguntadas **numa mensagem só**

## P1 ★ — Pauta e roteiro
- [ ] `ROTEIROS.md`: tabela-resumo (nº, tipo, gancho do 1º segundo, duração, isca) + roteiro por peça
- [ ] `VOZES.md`: todos os textos de voz, grafias de pronúncia, nome de arquivo esperado, duração estimada (~2,5 palavras/s)
- [ ] Nenhuma promessa fora das regras da marca; nenhum número de resultado inventado
- [ ] Mostrado ao dono com uma pergunta fechada
- **Trava:** texto falado e ordem das peças

## P2 ★ — Direção de arte
- [ ] Skill **direcao-de-arte** rodada: cartão por peça em `ESTILOS.md` (paleta com 1 destaque, 3 fontes, textura, como o produto aparece, movimento, música)
- [ ] Vizinhos não repetem família (claro/escuro, paleta); a maioria em fundo claro se o dono pediu
- [ ] 1 styleframe por peça, folha única com rótulos
- [ ] Fontes de todos os cartões baixadas para `base/fontes/` (+ `@font-face`)
- **Trava:** visual de cada peça

## P3 ★ — Piloto
- [ ] Uma peça inteira até o arquivo final, pelo caminho que a série vai usar (kit, voz, música, montagem)
- [ ] Revisão completa no piloto (revisao-video + hierarquia-visual + tabela da seção 6 do SKILL.md)
- [ ] Entregue com descrição do som
- [ ] Ajustes do dono incorporados em `ESTILOS.md` / `BRIEFING.md` **antes** do P4
- **Trava:** padrão técnico e de acabamento (o piloto é o modelo de código para os agentes)

## P4 — Disparo da produção
- [ ] Arquivos compartilhados prontos e congelados (`base/`, `vozes-palavras.js` com todas as vozes, réplicas de tela, `ESTILOS.md`, `VOZES.md`)
- [ ] Todas as vozes recebidas, com duração medida (`ffprobe`) e transcritas
- [ ] Grupos de 2–3 peças, misturando fáceis e difíceis
- [ ] Um briefing por agente com os 10 campos (`briefing-agente.md`)
- [ ] Trava de render definida (caminho do `.fila-render`) e espaço em disco conferido (`df -h`; 4K enche rápido)
- [ ] Scratchpad por prefixo
- [ ] Nada que os agentes leem será editado enquanto rodam

## P5 — Revisão
- [ ] Cada agente devolveu: arquivos, durações, folha que olhou, problemas
- [ ] Os arquivos prometidos existem no disco (conferido por você, não pela mensagem)
- [ ] Montagem em fila, uma peça por vez, com `revisar.py` de cada final
- [ ] Revisor independente por peça: veredito com evidência
- [ ] Reprovadas voltaram ao produtor com o motivo exato (máx. 2 voltas; depois decisão sua + aviso ao dono)

## P6 ★ — Entrega
- [ ] Pasta de entrega só com os finais; versões antigas em `versoes/`
- [ ] `ENTREGA.md` (modelo) com descrição do som por peça e real × ilustração
- [ ] Mensagem ao dono: onde estão, o que mudou desde o piloto, o que não deu, uma pergunta fechada

## Depois — Aprendizado
- [ ] Linha no `evolucao.md` da marca (e reação quando chegar)
- [ ] Linha no `historico.md` da motion-design; erro novo em `armadilhas.md`; regra nova em `nivel.md`
- [ ] Lição de orquestração nesta skill
- [ ] Ferramenta nova no `kit/`; exemplo enxuto se subiu o nível
- [ ] Commits pequenos por assunto; motion-design: push no privado (nunca `publico`)


## Avaliador com nota (desde 16/10/2026 — estudo de aprimoramento)
Nos portões de styleframe (P2) e de entrega (P5/P6), além do revisor técnico: um avaliador SEM contexto da produção dá nota pela rubrica (`direcao-de-arte/references/rubrica.md`, 10 critérios, 1–5, com evidência) à peça E ao vídeo anterior do mesmo tipo.
Passa: média ≥ 4,0, nada ≤ 2, sem ⛔ técnico, e ganha do anterior em ≥ 2 critérios sem perder em nenhum. No máximo 3 voltas; na 3ª, vai ao dono com as notas.
Depois que o dono reage: linha em `~/motion-studio/aprendizado/reacoes.md` e `POSTMORTEM.md` (modelo em `motion-design/reference/postmortem-modelo.md`). Nota alta + dono pedindo refazer = corrigir a rubrica.
