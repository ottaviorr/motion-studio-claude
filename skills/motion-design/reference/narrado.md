# Modo explicador/anúncio narrado (vídeo inteiro, sem filmagem)

Motor de Bart (`engine/`, MIT — `LICENSE-motion-broll.txt`): uma forma só que se transforma, câmera, legendas palavra a palavra.

```bash
bash $K/scripts/setup.sh ./motion                     # uma vez por projeto: pastas, playwright-core, venv com faster-whisper
P=./motion/.venv/bin/python
$P $K/scripts/voz.py motion/inputs/roteiro.txt motion/work/voz.wav --voz "Luciana (Enhanced)" --taxa 178   # ou ElevenLabs (.env)
$P $K/scripts/transcrever.py motion/work/voz.wav motion/work/words.json --roteiro motion/inputs/roteiro.txt
python3 $K/engine/build.py motion/dist motion/clips/*.html --words motion/work/words.json
NODE_PATH=./motion/node_modules node $K/engine/checar.cjs motion/dist/*.html
NODE_PATH=./motion/node_modules node $K/engine/beats.cjs motion/dist/01-x.html motion/work/01.png 0.9 1.5 2.4
NODE_PATH=./motion/node_modules node $K/engine/render.cjs motion/dist/01-x.html motion/out/01-x_0m00s00.mp4 30
$P $K/scripts/montar.py motion/plano.json saida.mp4 --sfx
```

- Roteiro: 25–40 s, gancho na 1ª frase, oferta e endereço no fim. Pronúncia × grafia: `[[iPhone|ai fone]]` (a voz fala o segundo, a legenda mostra o primeiro e nunca separa).
- Em cada clipe: `const IN=…; window.CLIP_IN=IN;` antes de qualquer `M.w('palavra')` (senão pega a palavra de outra cena). Marca de duas palavras é UMA palavra no `words.json`.
- `M.scene({W,H,bg,T,offset:IN,center,captions:{max:3}, SH, SEQ, layers, cursor})`. Slots `data-slot="bg"` e `"front"`. Ajudas: `M.type`, `M.caret`, `M.vis`, `M.track` (molas), `M.FAST`/`M.SLOW`.
- `plano.json`: `{"W","H","fps","bg","audio","music","tail","clips":[{"file","in","out"}]}`. Conferir volume (≈ -15 LUFS) e quadros do MP4 final.
- Voz do macOS: confira o nome com `say -v '?'` (nome errado cai na voz padrão em silêncio). Vozes "Enhanced/Premium" se baixam em Acessibilidade → Conteúdo Falado.
