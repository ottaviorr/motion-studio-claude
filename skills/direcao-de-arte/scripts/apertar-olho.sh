#!/usr/bin/env bash
# Teste do "olho apertado": miniatura, borrada e em cinza, lado a lado.
# O que sobra na versão borrada é a hierarquia real; na cinza, se texto e fundo
# viram a mesma massa, falta contraste de valor.
#
# Uso: bash apertar-olho.sh folha.jpg [saida.jpg]
# Saída padrão: <folha>-olho.jpg ao lado da original. Precisa de ffmpeg.
set -euo pipefail
ENT="${1:?uso: bash apertar-olho.sh folha.jpg [saida.jpg]}"
SAI="${2:-${ENT%.*}-olho.jpg}"
# altura fixa de 540 px para as três versões (miniatura de verdade)
ffmpeg -loglevel error -y -i "$ENT" -filter_complex \
  "[0:v]scale=-2:540,split=3[a][b][c];[b]gblur=sigma=9[b2];[c]hue=s=0,gblur=sigma=3[c2];[a][b2][c2]hstack=inputs=3" \
  -frames:v 1 -q:v 3 "$SAI"
echo "$SAI  (esquerda: miniatura · meio: borrada · direita: cinza)"
