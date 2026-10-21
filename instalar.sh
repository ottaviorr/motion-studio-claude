#!/bin/bash
# Instala o Motion Studio: liga as 8 skills em ~/.claude/skills, cria os atalhos da pasta e instala as ferramentas em .ferramentas/.
# uso: bash instalar.sh            (rode de dentro da pasta clonada)
set -e
cd "$(dirname "$0")"; E="$PWD"
for c in node npm ffmpeg; do command -v $c >/dev/null || { echo "Falta: $c (macOS: brew install $c)"; exit 1; }; done
# python: no Git Bash do Windows "python3" costuma ser só o atalho da Microsoft Store — testa se roda de verdade
PY=; for c in python3 python; do $c -c "import sys" 2>/dev/null && { PY=$c; break; }; done
[ -n "$PY" ] || { echo "Falta: python 3 (macOS: brew install python · Windows: winget install Python.Python.3.12)"; exit 1; }
[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ] || echo "Aviso: Google Chrome não encontrado; defina CHROME=/caminho/do/chrome"
# 1) skills → ~/.claude/skills (link simbólico: o que a skill aprende fica neste repositório)
mkdir -p ~/.claude/skills
for s in motion-design edicao-video revisao-video orquestrador-video direcao-de-arte hierarquia-visual editorial-film-edit paper-collage-film; do
  if [ -e ~/.claude/skills/$s ] && [ ! -L ~/.claude/skills/$s ]; then echo "Já existe ~/.claude/skills/$s (pasta); pulei"; else ln -sfn "$E/skills/$s" ~/.claude/skills/$s; fi
done
# 2) atalhos usados no CLAUDE.md e no novo-projeto.sh
ln -sfn skills/motion-design skill; ln -sfn skills/edicao-video skill-edicao; ln -sfn skills/revisao-video skill-revisao
ln -sfn skills/orquestrador-video skill-orquestrador; ln -sfn skills/direcao-de-arte skill-arte; ln -sfn skills/hierarquia-visual skill-hierarquia
# 3) ferramentas: Node (gravação, HyperFrames na versão fixa) e Python (transcrição, revisão)
mkdir -p .ferramentas
[ -f .ferramentas/package.json ] || echo '{"private":true,"dependencies":{"hyperframes":"0.8.140","playwright-core":"^1.63.0","puppeteer-core":"^23.11.1"}}' > .ferramentas/package.json
(cd .ferramentas && npm install --silent && npm install --silent matter-js@0.20.0)   # matter-js: kit/simular_queda.mjs
if [ ! -x .ferramentas/.venv/bin/python ]; then
  $PY -m venv .ferramentas/.venv
  # Windows: o venv cria Scripts/; o CLAUDE.md e os scripts usam .venv/bin/python
  [ -d .ferramentas/.venv/Scripts ] && [ ! -e .ferramentas/.venv/bin ] && cmd //c mklink /J "$(cygpath -w "$E/.ferramentas/.venv/bin")" "$(cygpath -w "$E/.ferramentas/.venv/Scripts")" >/dev/null
fi
# librosa: kit/analisar_musica.py · mediapipe: kit/recortar.py · pillow: selos do render.py
.ferramentas/.venv/bin/pip install -q faster-whisper numpy opencv-python-headless librosa mediapipe pillow
# modelos do recorte de sujeito (MediaPipe, Apache-2.0)
mkdir -p .ferramentas/modelos; U=https://storage.googleapis.com/mediapipe-models/image_segmenter
[ -f .ferramentas/modelos/selfie_multiclass_256x256.tflite ] || curl -fsSL -o .ferramentas/modelos/selfie_multiclass_256x256.tflite "$U/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite" || echo "Aviso: não baixei o modelo multiclasse"
[ -f .ferramentas/modelos/selfie_segmenter.tflite ] || curl -fsSL -o .ferramentas/modelos/selfie_segmenter.tflite "$U/selfie_segmenter/float16/latest/selfie_segmenter.tflite" || echo "Aviso: não baixei o modelo selfie"
# Windows: Python lendo/gravando arquivos em UTF-8 (sem isso, acento em .json/.txt sai trocado: o padrão lá é cp1252)
case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) setx PYTHONUTF8 1 >/dev/null && echo "PYTHONUTF8=1 ligado (vale nos terminais novos)";; esac
# GPU NVIDIA para a transcrição (faster-whisper/CTranslate2): sem elas, o transcrever.py/ouvir.py cai para CPU sozinho
nvidia-smi >/dev/null 2>&1 && .ferramentas/.venv/bin/pip install -q nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*" || true
echo "Pronto. Abra esta pasta no Claude Code e peça um vídeo. Marca nova: crie marcas/<marca>/ (modelo em marcas/exemplo/)."
