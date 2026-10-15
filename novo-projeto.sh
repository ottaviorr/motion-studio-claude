#!/bin/bash
# Cria um projeto novo: bash novo-projeto.sh <marca> <nome-do-projeto>
# Ex.: bash novo-projeto.sh exemplo reels-outubro  →  projetos/AAAA-MM-exemplo-reels-outubro/
# Copia o kit da skill e o pacote da marca para base/; cada vídeo vai numa subpasta com fonte/.
set -e
cd "$(dirname "$0")"
M="$1"; N="$2"
[ -z "$M" ] || [ -z "$N" ] && { echo "uso: bash novo-projeto.sh <marca> <nome>"; ls marcas; exit 1; }
[ -d "marcas/$M" ] || { echo "Marca '$M' não existe em marcas/. Crie o pacote da marca primeiro."; ls marcas; exit 1; }
P="projetos/$(date +%Y-%m)-$M-$N"
[ -e "$P" ] && { echo "Já existe: $P"; exit 1; }
mkdir -p "$P/base"
K=skill/kit
cp "$K"/comum.js "$K"/comum.css "$K"/gravar.mjs "$K"/hf.mjs "$K"/fotos.sh "$K"/grade.sh "$K"/gravar-todos.sh "$K"/gerar-plano.py "$K"/montar-final.py "$P/base/"
for f in legenda.js legenda.css conferir.py zona-segura.png gpu-windows.mjs compor_fundo.py shader.js; do [ -f "$K/$f" ] && cp "$K/$f" "$P/base/"; done
cp -R "marcas/$M/." "$P/base/"
rm -f "$P/base/evolucao"*.md
cat > "$P/LEIA-ME.txt" <<EOF
Projeto: $N · marca: $M · criado em $(date +%d/%m/%Y)
Diário da marca: marcas/$M/evolucao.md
Estrutura: base/ (kit + marca) · uma pasta por vídeo com fonte/ (cenas .html, roteiro.txt, palavras.json) e os .mp4 finais.
EOF
echo "pronto: $P"
