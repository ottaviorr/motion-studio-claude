---
name: revisao-video
description: Revisor de vídeo pronto, antes de entregar ao cliente ou publicar. "Assiste" sem olhos — transcreve o vídeo final de novo e compara com o que devia ser dito, acha gaguejada e repetição que sobraram, mede volume (LUFS), resolução, taxa de bits e qualidade de imagem (SSIM/PSNR, recorte 1:1), fotografa as emendas e lê a fala como espectador (o vídeo começa, desenvolve e fecha?). Use SEMPRE no fim de qualquer edição, VSL, motion, anúncio ou aula antes de dizer que está pronto, e quando pedirem "revisa esse vídeo", "confere se está ok", "tá com qualidade boa?", "tem algum erro?", "ficou pixelado?".
---

# Revisão de vídeo pronto

Quem revisa não assiste: ouve de novo (transcrição do arquivo FINAL), mede e olha fotos. A revisão serve para pegar o que escapou e para **medir** em vez de achar ("ficou ótimo" não é revisão).

Scripts em `scripts/` (Python com numpy, opencv-python-headless, faster-whisper; no Motion Studio: `.ferramentas/.venv/bin/python`).

## Passo a passo
1. **Rodar a revisão:**
   `scripts/revisar.py final.mp4 --esperado fonte/palavras-final.json --edl fonte/edl.json --original bruto.mp4`
   (sem edição por trás: só `final.mp4`, ou `--esperado roteiro.txt` numa VSL). Sai `<final>-revisao/revisao.txt` + `folha-fotos.jpg` (+ `folha-emendas.jpg`).
2. **Ler o técnico:** resolução e fps iguais ou maiores que o original; volume -16 a -14 LUFS e pico ≤ -1 dBFS; taxa de bits coerente (4K60 de tela: 10–25 Mb/s em CRF 14).
3. **Fala (esperado × ouvido):** quase toda diferença é o Whisper ouvindo diferente ("com V6" = "conversation"). Importa a que cai **perto de uma emenda**: recorte 6 s em volta e transcreva de novo antes de concluir. Nunca aponte "erro do apresentador" sem confirmar.
4. **Repetições coladas:** gaguejada que sobrou → volta para a edição.
5. **Leitura como espectador** (`## 4` do relatório): leia a fala inteira de uma vez. Responda por escrito:
   - Começa dizendo o que vai entregar? Termina, ou só para?
   - Alguma ideia aparece duas vezes? Algum "ou melhor" sobrou? Alguma frase sem fim?
   - Algo depende de ver a tela e não está claro?
   Problema aqui é problema de edição (skill edicao-video, `references/narrativa.md`).
6. **Fotos:** olhe `folha-fotos.jpg` (abertura no quadro 0, sem tela preta, câmera inteira, motions no lugar) e `folha-emendas.jpg` (pulo feio, tela piscando sem fusão).
7. **Hierarquia e legibilidade:** rode `node ~/.claude/skills/hierarquia-visual/scripts/conferir_hierarquia.mjs <cena>.html` nas cenas-fonte (tamanho real do texto, contraste medido, zona segura, palavras por tela, tempo de leitura) e a crítica de arte da skill **direcao-de-arte** na folha de fotos. Revisor independente (skill orquestrador-video) não edita: devolve APROVADO ou REFAZER com evidência.
8. **Qualidade de imagem medida** (quando houver dúvida ou o dono reclamar): `references/qualidade.md`.
9. **Relatório para o dono:** o que foi conferido, os números, o que foi corrigido e o que ficou (com o porquê). Diga só o que foi verificado; o que não deu para verificar (o "feeling" do ritmo) é dele.

## Referências
- `references/qualidade.md` — como medir qualidade de imagem e achar a causa do "pixelado".
