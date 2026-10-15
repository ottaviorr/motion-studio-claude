# Cortes de fala: bordas exatas

O Whisper erra a borda das palavras em 0,1–0,2 s. Cortar no tempo dele come o começo da palavra seguinte ou deixa meia sílaba. Por isso:

1. **Liste o corte com os tempos do Whisper** (`fonte/frases.txt` / `palavras.json`) e um motivo.
2. **O plano ajusta sozinho** quando há silêncio perto: a borda recua até o último ponto em silêncio (< -62 dB) antes da fala, até 0,3 s.
3. **Quando não há silêncio** (gaguejada colada: "a auto automação", "é" arrastado antes da palavra), olhe o volume: `scripts/perfil.py bruto.mp4 213.3 193.3`. Ache o vale mais fundo entre as duas palavras e escreva o corte com `"exato"`:
   `[191.00, 193.33, "repetição", "exato"]`.
4. **Gravação com noise gate** (OBS/plugin): aparece -120 dB colado na fala. É ótimo: é a borda exata. Corte nele.
5. **Ouça antes de renderizar:** `scripts/ouvir_emendas.py fonte/edicao.json --cortes` imprime "…antes ‖ depois…" em cada corte manual. Tem que soar como uma frase só.
6. **Pausas:** silêncio ≥ 0,6 s é encurtado (respiro de 0,2 s antes e 0,15 s depois). Pausa menor fica: cortar tudo deixa a fala atropelada e a câmera pulando.
7. **Fusão:** emenda em que a tela muda de verdade (o plano compara o quadro antes e depois) recebe `fusao` e o render funde 0,25 s. Sem fusão a tela "pisca".

## Antes de apontar um erro de fala
Confirme ouvindo o trecho (recorte e transcreva, ou leia a transcrição do vídeo final na revisão). Na aula de exemplo a primeira transcrição dizia "tirei a IA desativada"; ele tinha falado certo ("tirei essa tag de IA desativada").
