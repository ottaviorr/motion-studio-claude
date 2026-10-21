#!/bin/bash
# Desfoque de movimento REAL no HyperFrames (técnica do Filme A): grava a cena 2 vezes em fps alto, a 2ª passada
# adiantada meio subquadro, e o ffmpeg tira a média dos subquadros de cada quadro final (como um obturador de câmera).
# Uso: bash desfoque.sh cena.html saida.mp4 [--fps 30] [--sub 16] [--obturador 0.5] [--escala 1] [--crf 14] [--manter pasta]
#   --fps        quadros por segundo do vídeo final (padrão 30; regra do estúdio: 1080p30)
#   --sub        subquadros por quadro final, somando as 2 passadas; cada passada grava a fps×sub/2.
#                Padrão = o máximo: 480/fps (16 a 30 fps, 8 a 60 fps). O HyperFrames grava no máximo 240 fps: por isso
#                2 passadas (240 + 240 defasadas = 480 amostras/s). Medido: a 30 fps, --sub 8 mostra "degraus" (cópias
#                separadas) em movimento de ~10 000 px/s; --sub 16 vira rastro liso. Regra: deslocamento por amostra ≤ ~1/3 da
#                largura do objeto que corre (px/s ÷ (fps × amostras usadas)).
#   --obturador  fração do quadro em que o "obturador" fica aberto (0.5 = 180°, cinema; o Filme A usou 0.75 = 270° a 60 fps)
#   --escala 2   4K (repassa para o hf.mjs) · --crf do vídeo final (as passadas saem com CRF 12)
#   --manter     guarda as passadas p1.mp4/p2.mp4 nessa pasta (senão vão para um temporário apagado no fim)
# Exemplo do Filme A: --fps 60 --sub 8 --obturador 0.75 → 2 passadas a 240 fps, média de 3+3 = 6 subquadros por quadro.
# Deslocamento da 2ª passada: este script cria uma cópia da cena com window.DESLOC = 1/(2 × fps da passada) no <head>.
#   - Cena que NÃO fala em DESLOC: o window.frame é embrulhado sozinho (frame(t) recebe t + DESLOC). Nada a fazer.
#   - Cena que já trata (como o Filme A: `t += window.DESLOC||0` no começo do frame): o script só define a variável.
# Tempo: o obturador abre no tempo do quadro (t … t + obturador/fps), então o último quadro nunca passa de DUR.
# Só .mp4 (fundo próprio). Transparência com desfoque: gravar.mjs --prores --blur 3.
# Fila de render: cada passada entra na fila global do hf.mjs (uma gravação por vez no computador). Não rode em paralelo.
set -e
[ $# -ge 2 ] || { sed -n 2,20p "$0"; exit 1; }
AQUI="$(cd "$(dirname "$0")" && pwd)"
# python: o do estúdio se houver (no Git Bash do Windows, "python3" costuma ser o atalho da Microsoft Store)
PY=python3; for p in "$AQUI/../../../.ferramentas/.venv/bin/python" "$HOME/.claude/skills/motion-design/../../.ferramentas/.venv/bin/python"; do [ -x "$p" ] && { PY="$p"; break; }; done
CENA="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; SAIDA="$2"; shift 2
FPS=30; SUB=""; OBT=0.5; ESCALA=1; CRF=14; MANTER=""
while [ $# -gt 0 ]; do case "$1" in
  --fps) FPS=$2; shift 2;; --sub) SUB=$2; shift 2;; --obturador) OBT=$2; shift 2;;
  --escala) ESCALA=$2; shift 2;; --crf) CRF=$2; shift 2;; --manter) MANTER=$2; shift 2;;
  *) echo "opção desconhecida: $1"; exit 1;; esac; done
[ -n "$SUB" ] || SUB=$(( 480 / FPS / 2 * 2 ))
export NODE_PATH="${NODE_PATH:-$HOME/motion-studio/.ferramentas/node_modules}"

# contas: fps de cada passada (S subquadros por quadro final em cada uma), quantos entram na média (N) e o deslocamento
read PF S N DES < <("$PY" -c "
f,s,o=$FPS,$SUB,$OBT
S=s//2; pf=f*S
assert s%2==0 and s>=2, '--sub precisa ser par'
assert pf<=240, f'cada passada ficaria a {pf} fps (máximo do HyperFrames: 240). Baixe --sub ou --fps'
N=max(1,min(S,round(S*o)))
print(pf,S,N,repr(1/(2*pf)))")
[ -n "$PF" ] || exit 1
echo "desfoque: 2 passadas a $PF fps, média de $N+$N subquadros por quadro (obturador $("$PY" -c "print(round($N/$S*360))")°), saída $FPS fps"

R="${MANTER:-$(mktemp -d)}"; mkdir -p "$R"
P2HTML="$(dirname "$CENA")/.desfoque-$(basename "$CENA" .html)-$$.html"   # ao lado da cena: caminhos relativos continuam valendo
trap 'rm -f "$P2HTML"; [ -z "$MANTER" ] && rm -rf "$R"' EXIT

# cópia da cena com o deslocamento (python para não depender de sed do macOS)
"$PY" - "$CENA" "$P2HTML" "$DES" <<'PY'
import sys, re
src, dst, d = sys.argv[1], sys.argv[2], sys.argv[3]
h = open(src, encoding='utf8').read()
cabeca = f'<script>window.DESLOC={d};</script>'
if 'DESLOC' not in h:
    # embrulha o frame quando a cena o define (cena(), window.frame=… ou function frame)
    cabeca = ('<script>window.DESLOC=%s;(function(){const D=window.DESLOC;const emb=f=>(typeof f!=="function"||f.__desloc)?f:Object.assign(function(t){return f.call(this,(+t||0)+D);},{__desloc:1});'
              'let g;Object.defineProperty(window,"frame",{configurable:true,get(){return g;},set(f){g=emb(f);}});'
              'addEventListener("load",()=>{if(window.frame&&!window.frame.__desloc)window.frame=emb(window.frame);});})();</script>') % d
    rabo = '<script>if(window.frame&&!window.frame.__desloc){const f=window.frame,D=window.DESLOC;window.frame=Object.assign(function(t){return f.call(this,(+t||0)+D);},{__desloc:1});}</script>'
    h = re.sub(r'</body>', lambda m: rabo + m.group(0), h, count=1, flags=re.I)
m = re.search(r'<head[^>]*>', h, re.I)
h = h[:m.end()] + cabeca + h[m.end():] if m else cabeca + h
open(dst, 'w', encoding='utf8').write(h)
PY

node "$AQUI/hf.mjs" "$R/p1.mp4" --html "$CENA" --fps "$PF" --crf 12 --escala "$ESCALA"
node "$AQUI/hf.mjs" "$R/p2.mp4" --html "$P2HTML" --fps "$PF" --crf 12 --escala "$ESCALA"

# média das 2 passadas → média de N subquadros seguidos → fica 1 a cada S (o que fecha o obturador) → fps final
ffmpeg -v error -y -i "$R/p1.mp4" -i "$R/p2.mp4" -filter_complex \
 "[0:v][1:v]blend=all_mode=average,tmix=frames=$N,select='eq(mod(n\,$S)\,$((N-1)))',setpts=N/($FPS*TB),fps=$FPS,format=yuv420p" \
 -c:v libx264 -preset slow -crf "$CRF" -profile:v high -pix_fmt yuv420p \
 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -movflags +faststart "$SAIDA"
echo "pronto: $SAIDA ($(ffprobe -v error -select_streams v -show_entries stream=width,height,r_frame_rate,nb_frames -of csv=p=0 "$SAIDA"))"
