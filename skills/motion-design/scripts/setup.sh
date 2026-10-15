#!/usr/bin/env bash
# Preparação (uma vez por projeto): pastas, motor de render (playwright-core + Chrome do computador) e transcrição local.
set -e
D="${1:-./motion}"
mkdir -p "$D"/{clips,dist,out,work,inputs}
for c in node ffmpeg python3; do command -v $c >/dev/null || { echo "Falta: $c (macOS: brew install $c)"; exit 1; }; done
[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ] || echo "Aviso: Google Chrome não encontrado; defina CHROME=/caminho/do/chrome"
[ -f "$D/package.json" ] || echo '{"private":true}' > "$D/package.json"
[ -d "$D/node_modules/playwright-core" ] || (cd "$D" && npm install --silent playwright-core)
[ -x "$D/.venv/bin/python" ] || python3 -m venv "$D/.venv"
"$D/.venv/bin/python" -c "import faster_whisper" 2>/dev/null || "$D/.venv/bin/pip" install -q faster-whisper numpy
echo "Pronto. Rode os scripts de Node com NODE_PATH=$D/node_modules e os de Python com $D/.venv/bin/python."
