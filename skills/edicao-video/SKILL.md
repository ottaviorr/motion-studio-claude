---
name: edicao-video
description: Editor de vídeo profissional para gravações já feitas (aula, tutorial de tela + câmera, vídeo de YouTube, talking head, live, reunião gravada). Lê o vídeo como roteiro (começo, meio e fim), corta silêncio, gaguejada, frase recomeçada, tomada repetida e trecho que confunde, faz zoom onde a ação acontece, mantém a câmera do apresentador limpa, intercala motions, trata o áudio e exporta em alta qualidade (1080p30, o padrão do dono). Use SEMPRE que alguém mandar um vídeo gravado e pedir para editar, cortar, limpar, "deixar profissional", tirar silêncios ou erros, melhorar o ritmo, preparar para YouTube/curso, ou mesmo só "dá um tapa nesse vídeo" — mesmo sem dizer "edição".
---

# Edição de vídeo gravado

O dono grava (tela + câmera, ou só câmera) e quer de volta o vídeo **como um editor profissional entregaria**: que se entende do começo ao fim, sem tempo morto, sem tropeço, com ritmo, zoom onde importa, motion onde ajuda e qualidade de imagem no máximo que a gravação permite.

Esta skill orquestra. Motions são da skill **motion-design** (gravadas pelo HyperFrames); a montagem final pode ser no **Remotion** (plugins oficiais do Remotion e do HyperFrames instalados: leia `motion-doctrine` e `cut-the-curve` do HyperFrames antes de desenhar transições); a conferência final é da skill **revisao-video**. Scripts em `scripts/` (Python com numpy, opencv-python-headless, pillow, faster-whisper; no Motion Studio: `.ferramentas/.venv/bin/python`).

## Regras do dono (aprendidas)
- **Legenda corrida não é padrão.** Só se ele pedir (VSL, anúncio). Texto dentro dos motions, sim.
- **Nem todo vídeo é de marca.** Vídeo de YouTube qualquer: só editar. Marca e motions só quando fazem sentido.
- **Erro de fala → cortar e ficar com a tomada certa.** Erro sem repetição, com o rosto aparecendo, não tem conserto por corte: deixe e avise.
- **Nada de acelerar 4× no meio da explicação.** Ele reprovou: quebra a frase e não ensina. Trecho calado em que ele só clica é cortado (o resultado aparece logo depois) com fusão curta se a tela mudar.
- **O vídeo tem que fazer sentido sozinho.** Repetição, caminho abandonado ("ou melhor, vou fazer de outro jeito") e explicação dada duas vezes saem. Isso é editar, não só limpar.
- **Entrega em 1080p a 30 fps** (decisão do dono, 13/10/2026; a regra antiga era 4K60 e deixava o render ~8× mais lento). Um único redimensionamento de alta qualidade quando há zoom; motions gravados em 1080p30. 4K/60 só se ele pedir.

## Passo a passo

1. **Receber.** Projeto novo (no Motion Studio: `bash novo-projeto.sh <marca> <nome>`), bruto em `v1/bruto.mp4`. `ffprobe` + 6 quadros espalhados: o que é (tela + câmera? só rosto?), onde está a câmera, faixa preta nas bordas, resolução da captura.
2. **Transcrever** com tempo por palavra (`--modelo medium`, acha melhor os tropeços): no Motion Studio `skill/scripts/transcrever.py bruto.mp4 fonte/palavras.json --modelo medium`.
3. **Frases:** `scripts/frases.py fonte/palavras.json > fonte/frases.txt` — a aula em frases numeradas com tempo.
4. **Decupagem narrativa** (o passo que separa editor de cortador): leia `references/narrativa.md` e escreva `fonte/narrativa.md` — blocos (abertura, conceito, demonstração, caso, fechamento), o papel de cada um e o que sai (repetição, caminho abandonado, tropeço). Aqui nascem os cortes editoriais e os capítulos.
5. **Atividade da tela e lugar da câmera:** `scripts/atividade.py bruto.mp4 fonte/atividade.json --camera x,y,w,h` e `scripts/camera_lugar.py fonte/edicao.json` (acha trechos em que a câmera saiu do lugar → `camera_fora`; 1 min para 18 min de vídeo). Rode ANTES do render: na aula IA de Fluxo isso custou um render perdido.
6. **Cortes** no `fonte/edicao.json` (modelo em `references/edicao-json.md`): tropeços + editoriais, cada um com motivo. Bordas exatas: `scripts/perfil.py bruto.mp4 <tempos>` e `references/cortes.md`.
7. **Plano:** `scripts/plano.py fonte/edicao.json` → `edl.json`, `palavras-final.json`, `cortes.txt`.
8. **Ouvir as emendas antes de renderizar:** `scripts/ouvir_emendas.py fonte/edicao.json --cortes`. Cada emenda tem que soar como uma frase só. Errou? Ajuste a borda e rode de novo (1 min, contra 15 do render).
9. **Zoom:** `scripts/zoom.py fonte/edicao.json` (segue a ação, segura ≥ 4 s, até 1,6×). Ajuste manual com `zoom_fixo`. Ver `references/imagem.md`.
10. **Motions e capítulos** (skill motion-design, com cartão da skill direcao-de-arte e números da hierarquia-visual): 2–5 frases que ficam mais claras desenhadas, marcadores de capítulo (do passo 4) e um fechamento se o vídeo termina "no ar". Tempos tirados de `palavras-final.json`. Grave em 1080p30 (padrão do kit).
11. **Fotos antes do render:** `scripts/render.py fonte/edicao.json --quadros 10,48,88 [--cheio]` — zoom legível, câmera limpa (sem borda clara), capítulos no lugar.
12. **Render** — dois caminhos:
    - **Montagem em camadas (padrão desde a v3):** `render.py --camada-tela` (tela + voz) → cenas pelo HyperFrames (`motion-design/kit/hf.mjs`) → `scripts/gerar_remotion.py` → `npx remotion render`. Transições da doutrina (empurrão / curva / zoom reverso), capítulos nativos, linha do tempo editável no Remotion Studio. Ver `references/montagem-remotion.md`.
    - **Tudo no Python:** `scripts/render.py fonte/edicao.json` (fusões simples; `--previa` para assistir rápido em 960×540).
13. **Revisão:** skill **revisao-video** (`revisar.py` com `--esperado palavras-final.json --edl edl.json --original bruto.mp4`). Leia a fala final como espectador.
14. **Entregar:** vídeo + `ENTREGA.txt` (o que foi feito, cada corte com motivo — em especial os editoriais, que mudam o conteúdo —, o que não deu para consertar, real × ilustração, dado de cliente que aparece na tela).
15. **Aprender:** reação do dono no diário da marca; lição geral em `references/` desta skill; script novo que serviu em `scripts/`.

## Referências (leia quando chegar no passo)
- `references/narrativa.md` — como ler o vídeo como roteiro e decidir o que sai (passo 4).
- `references/cortes.md` — borda exata de corte, noise gate, "exato", fusão (passos 6–8).
- `references/imagem.md` — qualidade 4K, nitidez, zoom, recorte da câmera (passos 9–12).
- `references/edicao-json.md` — todas as chaves do `edicao.json`.
- `references/montagem-remotion.md` — montagem final no Remotion com cenas do HyperFrames e as regras de transição.
- `references/armadilhas.md` — o que já deu errado.
