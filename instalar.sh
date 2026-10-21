#!/bin/bash
# Instala o Motion Studio: liga as 8 skills em ~/.claude/skills, cria os atalhos da pasta e instala as ferramentas em .ferramentas/.
# uso: bash instalar.sh            (rode de dentro da pasta clonada)
set -e
cd "$(dirname "$0")"; E="$PWD"
for c in node npm ffmpeg python3; do command -v $c >/dev/null || { echo "Falta: $c (macOS: brew install $c)"; exit 1; }; done
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
(cd .ferramentas && npm install --silent)
[ -x .ferramentas/.venv/bin/python ] || python3 -m venv .ferramentas/.venv
.ferramentas/.venv/bin/pip install -q faster-whisper numpy opencv-python-headless
# GPU NVIDIA para a transcrição (faster-whisper/CTranslate2): sem elas, o transcrever.py/ouvir.py cai para CPU sozinho
nvidia-smi >/dev/null 2>&1 && .ferramentas/.venv/bin/pip install -q nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*" || true
echo "Pronto. Abra esta pasta no Claude Code e peça um vídeo. Marca nova: crie marcas/<marca>/ (modelo em marcas/exemplo/)."
