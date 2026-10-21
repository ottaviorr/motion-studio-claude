#!/bin/bash
# fotos.sh arquivo.html t1 t2 ... → fotos de conferência numa pasta temporária nova (ou em $FOTOS_DIR).
# Motions transparentes (class "alfa" no #st) saem em PNG; com ROSTO=quadro.jpg (um quadro da gravação) saem também por cima dele.
set -e
G="${GRAVAR:-$HOME/.claude/skills/motion-design/kit/gravar.mjs}"
S="${FOTOS_DIR:-$(mktemp -d "${TMPDIR:-/tmp}/fotos.XXXXXX")}"
mkdir -p "$S"; f=$1; shift; n=$(basename "$f" .html)
if grep -q 'id="st" class="[^"]*alfa' "$f"; then ext=mov; else ext=mp4; fi
# no máximo FOTOS_P Chromes ao mesmo tempo (padrão 3; antes abria um por tempo e travava o computador), com prioridade baixa
P="${FOTOS_P:-3}"
for t in "$@"; do while [ "$(jobs -rp | wc -l)" -ge "$P" ]; do sleep 0.2; done; (nice -n 10 node "$G" "$S/$n-$t.$ext" --html "$f" --so "$t" 2>&1 | grep -v "^foto" | grep -v 'erros: \[\]' || true
  if [ $ext = mov ] && [ -n "$ROSTO" ]; then ffmpeg -v error -y -i "$ROSTO" -i "$S/$n-$t.png" -filter_complex overlay "$S/$n-$t.jpg"; fi) & done; wait
echo "fotos em $S"
