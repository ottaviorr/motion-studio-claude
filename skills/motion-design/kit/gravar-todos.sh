#!/bin/bash
# Grava as cenas da pasta fonte para a pasta de cima (copie este arquivo para a pasta fonte).
# Página com <div id="st" class="... alfa ..."> → .mov transparente; as outras → .mp4.
# Uso: bash fonte/gravar-todos.sh [01 05 ...]   (sem números = todos).
#   PADRÃO DO DONO: 1080p a 30 fps com taxa de bits alta (40 Mb/s) — sem FPS/ESCALA os dois motores já gravam assim. FPS=60 · ESCALA=2 (4K) só se o pedido disser.
#   MOTOR=hf (padrão) → HyperFrames (kit/hf.mjs): mesma imagem, 2–3,4× mais rápido, uma cena por vez (ele já usa vários Chromes e a fila global).
#   MOTOR=cdp → gravador próprio (kit/gravar.mjs) com desfoque de movimento (--blur 3), 3 cenas por vez. Para desfoque de verdade no hf: kit/desfoque.sh.
#   PREVIA=1 → prévia rápida (hf --previa: qualidade draft, 12 Mb/s) para o dono olhar; nunca entregue a prévia. X264=1 → codifica no x264 por CRF.
#   No hf, .mov com alfa sai em 1080 (o HyperFrames não faz 4K com alfa).
cd "$(dirname "$0")"
K="$HOME/.claude/skills/motion-design/kit"
G="${GRAVAR:-$K/gravar.mjs}"
MOTOR="${MOTOR:-hf}"
lista=("$@"); [ ${#lista[@]} = 0 ] && lista=($(ls [0-9][0-9]-*.html | cut -c1-2))
grava(){ f=$(ls $1-*.html); n=${f%.html}; if grep -q 'id="st" class="[^"]*alfa' "$f"; then e=mov; else e=mp4; fi
  if [ "$MOTOR" = hf ]; then node "$K/hf.mjs" "../$n.$e" --html "$f" ${FPS:+--fps $FPS} ${ESCALA:+--escala $ESCALA} ${PREVIA:+--previa} ${X264:+--x264} > /dev/null && echo "pronto: $n.$e (hyperframes)"
  else node "$G" "../$n.$e" --html "$f" --blur 3 ${FPS:+--fps $FPS} ${ESCALA:+--escala $ESCALA} ${PRORES:+--prores} > /dev/null && echo "pronto: $n.$e"; fi; }
if [ "$MOTOR" = hf ]; then for k in "${lista[@]}"; do grava $k; done
else i=0; for k in "${lista[@]}"; do grava $k & i=$((i+1)); [ $((i%3)) = 0 ] && wait; done; wait; fi
