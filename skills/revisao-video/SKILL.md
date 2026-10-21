---
name: revisao-video
description: Revisor de vídeo pronto, antes de entregar ao cliente ou publicar. "Assiste" sem olhos — transcreve o vídeo final de novo e compara com o que devia ser dito, acha gaguejada e repetição que sobraram, mede o padrão de entrega (1080p30, 16–20 Mb/s, AAC 320 k, -14 LUFS), a sincronia voz × câmera em cada emenda (reprova acima de 40 ms), a qualidade de imagem (SSIM/PSNR, recorte 1:1), fotografa as emendas e lê a fala como espectador (o vídeo começa, desenvolve e fecha?). Use SEMPRE no fim de qualquer edição, VSL, motion, anúncio ou aula antes de dizer que está pronto, e quando pedirem "revisa esse vídeo", "confere se está ok", "tá com qualidade boa?", "tem algum erro?", "ficou pixelado?", "a voz tá fora da boca?", "tá dessincronizado?".
---

# Revisão de vídeo pronto

Quem revisa não assiste: ouve de novo (transcrição do arquivo FINAL), mede e olha fotos. A revisão serve para pegar o que escapou e para **medir** em vez de achar ("ficou ótimo" não é revisão).

Scripts em `scripts/` (Python com numpy, opencv-python-headless, faster-whisper; no Motion Studio: `.ferramentas/.venv/bin/python`).

## Passo a passo
1. **Rodar a revisão:**
   `scripts/revisar.py final.mp4 --esperado fonte/palavras-final.json --edl fonte/edl.json --original bruto.mp4`
   (sem edição por trás: só `final.mp4`, ou `--esperado roteiro.txt` numa VSL; `--padrao nenhum` para peça que não segue o padrão de edição, ex.: reel 9:16). Sai `<final>-revisao/revisao.txt` (começa com **RESULTADO: APROVADO/REPROVADO** e o motivo) + `sincronia.json` + `folha-fotos.jpg` (+ `folha-emendas.jpg`). Transcrição, sincronia e fotos rodam em paralelo; a transcrição tem cache (~1 min para 3 min de vídeo).
2. **Ler o técnico × padrão de entrega** (vídeo editado, regra do dono): 1920×1080 · 30 fps constante · H.264 High · 16–20 Mb/s · AAC 320 k 48 kHz · -14 ±1 LUFS · pico ≤ -1 dBFS · BT.709. Qualquer "FORA" reprova: volta para a edição (`finalizar.py` da edicao-video conserta o formato numa codificação).
2b. **Sincronia voz × câmera** (com `--edl` e `--original`; `scripts/sincronia.py`): atraso por emenda em ms, pior caso. **Reprova acima de ±40 ms**; pipeline certo dá ~0 ms. Fora → a causa e o conserto estão em `edicao-video/references/sincronia.md` (bruto de taxa variável sem normalizar, edl antigo sem quadros inteiros, concat de pedaços). Sem bruto/edl: `sincronia.py final.mp4 --camera x,y,w,h` dá só o "lábio × voz" (indício).
2c. **Trilha × voz** (vídeo com música): `PY scripts/trilha_voz.py <saida>-voz.wav musica/trilha.wav fonte/palavras-final.json` — LUFS de curto prazo (3 s) só nas janelas com fala. **Regra do dono: 30 dB** (mediana ≥ 30; reprova qualquer janela abaixo de 28). Padrão do script: `--alvo 30 --minimo 28`. Histórico: 18 alta → 25 ok → 30 regra (16/10/2026).
3. **Fala (esperado × ouvido):** quase toda diferença é o Whisper ouvindo diferente ("com V6" = "conversation"). Importa a que cai **perto de uma emenda**: recorte 6 s em volta e transcreva de novo antes de concluir. Nunca aponte "erro do apresentador" sem confirmar.
4. **Repetições:** (a) coladas (`revisar.py`, item 3 do relatório); (b) **tomada repetida distante**: `PY scripts/repeticoes.py final.mp4 --db -45` (roda o `edicao-video/scripts/ilhas.py` e compara cada frase com as 3 seguintes: muito parecidas ou recomeço com 4 palavras já ditas). Qualquer par = REPROVADO até alguém ouvir e decidir. No bruto da aula SLA ele acha 7 das 8 tomadas que o dono apontou; no final corrigido, 0.
5. **Leitura como espectador** (`## 4` do relatório): leia a fala inteira de uma vez. Responda por escrito:
   - Começa dizendo o que vai entregar? Termina, ou só para?
   - Alguma ideia aparece duas vezes? Algum "ou melhor" sobrou? Alguma frase sem fim?
   - Algo depende de ver a tela e não está claro?
   Problema aqui é problema de edição (skill edicao-video, `references/narrativa.md`).
5b. **Checklist de retenção (aula/tutorial de YouTube)** — responder no relatório, cada item com o tempo:
   | # | Item | Passa quando |
   |---|---|---|
   | 1 | Título provado | o resultado ou a dor do título aparece em ≤ 10–15 s |
   | 2 | Assunto dito | o nome do assunto/ferramenta é dito em ≤ 30 s |
   | 3 | Roteiro | uma frase diz o que vem (2–4 partes) antes de 45 s |
   | 4 | Abertura em movimento | quadro 0 não é tela parada nem preta |
   | 5 | 1ª mudança forte | motion ou troca de plano entre 25–35 s |
   | 6 | Sem trecho morto | nenhum trecho > 40 s sem mudança visual (mapa do M7) |
   | 7 | Re-gancho | cada capítulo abre dizendo o que está em jogo; nenhum bloco > 6 min |
   | 8 | Sem repetição | nenhuma tomada repetida (colada ou distante, item 4) |
   | 9 | Ideia errada tratada | se há uma armadilha comum, ela aparece antes da solução |
   | 10 | Trilha | ≥ 20 dB abaixo da voz em toda janela de fala (alvo 25) |
   | 11 | Capítulos | `capitulos-youtube.txt` com 00:00, ≥ 3, cada ≥ 10 s |
   | 12 | Fechamento | resumo + próximo passo ≤ 20 s; área da tela final livre nos últimos 5–20 s |
   | 13 | Ritmo de fala | ppm do final (≥ 165 está ótimo; se < 140, procurar pausas que sobraram) |
   Itens 1–3, 7 e 9 dependem de leitura (o revisor escreve o tempo e a frase). 6, 8, 10, 11 e 13 são medidos.
   Item 10 ou 8 falhando = REPROVADO. Os outros = aviso ao dono com a sugestão.
5c. **Mapa de recursos e variedade:** o `fonte/mapa-recursos.md`/`PLANO-EDICAO.md` existe e o final cumpre (foto em cada linha com recurso); degrau 5 (motion cheio) ≤ 1/min; chamadas (anotação, texto, card, pop-up, tela em cena) ≤ 3/min; tela encolhida ≤ 30 %; nada > 40 s sem mudança; vizinhos não repetem gesto; nada dentro da janela de proibição do `aprendizado/repertorio-usado.md` (critério Frescor da rubrica).
6. **Fotos:** olhe `folha-fotos.jpg` (abertura no quadro 0, sem tela preta, câmera inteira, motions no lugar) e `folha-emendas.jpg` (pulo feio, tela piscando sem fusão).
7. **Hierarquia e legibilidade:** Inclui **sobreposição** no tempo: dois textos/elementos ocupando o mesmo lugar ao mesmo tempo reprova (motion "bugado" da aula SLA). E a **rubrica** (`direcao-de-arte/references/rubrica.md`): nota 1–5 por critério, com evidência, comparando com o vídeo anterior do mesmo tipo; passa com média ≥ 4,0 e nada ≤ 2. rode `node ~/.claude/skills/hierarquia-visual/scripts/conferir_hierarquia.mjs <cena>.html` nas cenas-fonte (tamanho real do texto, contraste medido, zona segura, palavras por tela, tempo de leitura) e a crítica de arte da skill **direcao-de-arte** na folha de fotos. Revisor independente (skill orquestrador-video) não edita: devolve APROVADO ou REFAZER com evidência.
8. **Qualidade de imagem medida** (quando houver dúvida ou o dono reclamar): `references/qualidade.md`.
9. **Relatório para o dono:** o que foi conferido, os números, o que foi corrigido e o que ficou (com o porquê). Diga só o que foi verificado; o que não deu para verificar (o "feeling" do ritmo) é dele.

## Referências
- `references/qualidade.md` — como medir qualidade de imagem e achar a causa do "pixelado".
- `scripts/sincronia.py` — como a sincronia é medida (docstring) e `edicao-video/references/sincronia.md` — causas e números.
