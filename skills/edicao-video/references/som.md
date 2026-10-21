# Som: voz, trilha e efeitos

## Trilha por baixo da voz (aula, tutorial, YouTube)
- **REGRA DO DONO (16/10/2026): música 30 dB abaixo da voz durante a fala** (mediana ≥ 30; nenhuma janela de 3 s abaixo de 28).
  Histórico: reprovou 18 dB ("alta"), aprovou 25 dB e depois pediu 30 como regra (aula SLA v3).
  Como: trilha base ~-44 LUFS sob voz de -14 + `scripts/trilha.py voz.wav trilha-base.wav palavras-final.json trilha.wav --alvo 30` (abaixa só onde a voz é mais baixa, até 8 dB) e conferir com `revisao-video/scripts/trilha_voz.py … --alvo 30 --minimo 28`.
- Medir em **LUFS de curto prazo (3 s) só nas janelas com fala** (tirar de `palavras-final.json`),
  não no integrado do arquivo inteiro: o integrado esconde trecho em que a música sobe.
- **Ducking por script** (`scripts/trilha.py`): a trilha desce com a fala e sobe só em buraco ≥ 2 s
  sem fala (até ~12–15 dB abaixo do nível da voz), com fade de 300–800 ms. Nada de "bombear" a cada palavra.
- **Explicação densa** (passo técnico, configuração campo a campo): a trilha pode cair mais (30 dB) ou
  sair. Pesquisa (Moreno & Mayer 2000; coerência de Mayer): música atrapalha o aprendizado.
- Fechamento sem fala: sobe (~-22 LUFS) e termina em fade.
- Trilha sem direitos, com licença em `musica/LICENCAS.md`.

## Voz
- Cadeia atual: highpass 70 Hz + compressor 2,5:1. Respiração alta: reduzir ~6 dB, não apagar.
- -14 LUFS integrado, pico verdadeiro ≤ -1 dBTP (o YouTube só abaixa, nunca aumenta).

## Efeitos (opcional, pouco)
- Só na entrada de motion de tela cheia e no capítulo. Whoosh com **a duração da transição**,
  pico no instante do corte, ~15–20 dB abaixo da voz. Nunca durante a fala explicando passo.
- Nada de efeito em clique comum de tela.
