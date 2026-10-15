# Motores de render: qual usar (pesquisa e piloto de 07/10/2026)

As cenas continuam iguais: HTML com `cena(DUR, frame)` e `window.frame(t)`. O que muda é quem grava.

| Motor | Como chamar | Quando |
|---|---|---|
| **HyperFrames** (HeyGen, Apache-2.0, v0.8.140 fixa em `.ferramentas`) | `node kit/hf.mjs saida.mp4 --html cena.html --escala 2` · lote: `MOTOR=hf bash fonte/gravar-todos.sh` | **Padrão.** Mesma imagem, 2–3,4× mais rápido (vários Chromes em paralelo) |
| **gravar.mjs** (próprio, CDP) | `node kit/gravar.mjs saida.mp4 --html cena.html --blur 3 --escala 2` | Movimento muito rápido que pede **desfoque de movimento** (o HyperFrames ainda não tem na linha de comando) e **alfa em 4K** (`--prores --escala 2`; o HyperFrames só faz alfa em 1080) |

## Piloto (cena "03 uma tag", 9,1 s, Apple M4)
| | 1080p60 | 4K60 |
|---|---|---|
| gravar.mjs (sem desfoque) | 54 s | 90 s |
| HyperFrames | 16 s | 44 s |
| SSIM entre os dois | 0,996 | 0,996 |
Alfa: `hf.mjs saida.mov` → ProRes 4444 (yuva444p12le), alfa conferido (3 s em 8,8 s).

## Como a ponte funciona (kit/hf.mjs)
1. `gravar.mjs --dur` abre a cena e lê `window.DUR`, largura e altura.
2. Cria `.hf-<cena>.html` ao lado: o `#st` ganha `data-composition-id/start/duration/width/height` e entra uma "timeline" mínima em `window.__timelines.main` cujo `seek(t)` chama `frame(t)`.
3. `hyperframes render <pasta> -c .hf-<cena>.html --fps 60 --quality high --crf 16 [--resolution landscape-4k] [--format mov]` e apaga o temporário.
Por que assim: a API oficial de "frame source" dentro de iframe não ficava pronta (fontes do Google no iframe); a timeline-ponte na própria página funcionou de primeira e não exige mudar nenhuma cena.

## Remotion (adotado para a MONTAGEM final, não para gravar cenas)
- Desde a aula de exemplo v3: as cenas continuam em HTML (gravadas pelo HyperFrames) e o Remotion monta o vídeo (câmera, transições, capítulos, áudio). Ver skill edicao-video, `references/montagem-remotion.md`.
- Framework React (useCurrentFrame), também Chrome + ffmpeg por baixo. Licença: grátis para pessoa física / empresa de até 3 pessoas, **inclusive para trabalho de cliente** desde que o cliente receba só o vídeo, não o código (FAQ oficial). Acima: US$ 25/mês por pessoa.
- Vantagens reais: Studio com linha do tempo, transições prontas (@remotion/transitions), legendas (@remotion/captions, inclusive do ElevenLabs), `<Video>` de @remotion/media com quadro exato, skills oficiais (`npx skills add remotion-dev/skills`), plugin Claude Code (`claude plugin marketplace add remotion-dev/claude-code-plugin`).
- Por que não para as cenas: exigiria reescrever as cenas em React/TSX (o HyperFrames reaproveita tudo), build com node_modules de centenas de MB por projeto, `create-video --yes` falha dentro de repositório git, recursos mais bonitos (HtmlInCanvas, motion blur novo) são experimentais.
- Quando reconsiderar: se o estúdio quiser usar bibliotecas de componentes Remotion (remocn, snapcn, remotion-bits — MIT) ou o Player para prévia ao cliente num site.

## O que ainda dá para tirar do HyperFrames (próximos passos)
- **Catálogo** (~300–400 blocos: `npx hyperframes add <nome>`; ver `npx hyperframes catalog`): 14 transições com shader WebGL, ~17 estilos de legenda, lower thirds, texturas. Blocos são GSAP; para usar ao lado das nossas cenas, monte uma composição-mãe com sub-composições.
- **Áudio:** mixagem com "voiceover carve" (música abaixa sob a voz), EQ/compressor, `hyperframes beats` (batida da música para cortar no tempo).
- **lint / check / snapshot** (folha de contato com `--at`), `--batch` com `--variables` para várias versões de anúncio.
- **Plugins instalados (07/10/2026, com o ok do dono):** `hyperframes@hyperframes` e `remotion@remotion`. As skills deles ficam em `~/.claude/plugins/cache/{hyperframes,remotion}/…/skills/` — as mais úteis: `motion-doctrine`, `cut-the-curve`, `seam-craft`, `talking-head-recut`, `hyperframes-audio` (HyperFrames) e `remotion-best-practices` (Remotion).

## Fontes
remotion.dev/docs (license/faq, shared-memory-capture, transitions, captions, ai/skills) · github.com/remotion-dev/remotion/blob/main/LICENSE.md · github.com/heygen-com/hyperframes · hyperframes.heygen.com (concepts/determinism, guides/frame-sources, guides/4k-rendering, guides/rendering, packages/cli) · issue #4833 (motion blur fora da CLI) · #4584 (BeginFrame cai para screenshot com 6+ workers).

## Desempenho na GPU (Windows, RTX 3050 + Intel UHD, 12 threads — medido em 11/10/2026)
| Gargalo | Antes | Depois | O que mudou |
|---|---|---|---|
| Chrome do render na GPU integrada (Intel) | cena 6,4 s alfa: 170 s | 128 s | Preferência de GPU do Windows "alto desempenho" para cada `chrome-headless-shell.exe` (HKCU\Software\Microsoft\DirectX\UserGpuPreferences, `GpuPreference=2;`) — o log do HyperFrames mostra o `renderer=` |
| Shader de fundo dentro de cada cena | 95 s | 23 s de captura | Fundo gravado UMA vez (960×540, 30 fps) e composto no ffmpeg: `kit/compor_fundo.py` (furo da câmera + fade). Mais workers NÃO ajuda (4, 8, 11 = mesmo tempo) |
| Transcrição (faster-whisper medium) | CPU int8 ~0,7× tempo real | 2 min de áudio em 20 s | CUDA: `pip install nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"` + `os.add_dll_directory` (transcrever.py `transcrever_audio`, cai para CPU sozinho) |
| Intermediário 4K (x264 medium CRF 12) | ~5 min (81 s de vídeo) | 39 s | `h264_nvenc -preset p6 -tune hq -cq 14` (SSIM 0,997 contra o x264). Também no `render.py` e no `gerar_remotion.py` |
| Montagem Remotion 4K60 | 10 s em 197 s | 141 s | `remotion.config.ts`: `angle` + 8 processos + x264 `veryfast`. 12 processos é PIOR (158 s). Render em 1080p + ampliar não compensa (126 s): o gargalo é decodificar as fontes 4K |
- O Remotion não usa NVENC no Windows; o limite que sobra é a decodificação de vídeo por quadro (`OffthreadVideo`).
- Prévia rápida de shader: uma flag da marca (ex.: `window.FUNDO_NA_CENA = true`) desenha o fundo dentro da página.
- **Captura rápida do HyperFrames ligada de novo** (12/10/2026): a falha antiga no Windows era o bug do `id="st"` no comentário, não a GPU. Cena 4K opaca 39 s → 29 s, SSIM 0,9997; alfa igual. Desligar: `HF_SEM_CAPTURA_RAPIDA=1`.
- **GPU automática:** `kit/gpu-windows.mjs` marca na GPU dedicada todo Chrome de render que achar (HyperFrames + Remotion de cada projeto); o `hf.mjs` roda sozinho a cada render.
- **Remotion, o que NÃO adiantou** (trecho de 10 s 4K60, base 141 s): `<Video>` do @remotion/media (WebCodecs) 215 s · `--offthreadvideo-threads=8` 135 s · `toneMapped={false}` 142 s · 2 renders em paralelo 181 s · `--sequence` JPEG + NVENC 139 s. Conclusão: o Remotion está no limite da máquina (~4,5 quadros 4K/s). O próximo salto só trocando a montagem de talking head por ffmpeg + NVENC (filtros de recorte/escala por tempo, legenda em ASS) — ainda não feito.
- **render.py (edição tela+câmera, 4K60) — medido em 13/10/2026:** 10 s levavam 120 s. Gargalos: `warpAffine` Lanczos 4K (81–102 ms/quadro, já usa todos os threads), nitidez no 4K (25 ms), mistura da câmera em float (16 ms). Agora: enquadramento parado = recorte + `resize` Lanczos (22 ms, mesma imagem: 0,03/255), `warpAffine` só quando o zoom anda; nitidez antes de ampliar (6 ms); `blendLinear`/`multiply` nativos; NVDEC + NVENC. **10 s → 81 s.** Paralelo (`--partes N`, threads divididos) ficou PIOR (3 trechos: 315–330 s): o limite é compartilhado (memória/decodificação), não CPU — não usar até medir de novo.

## Padrão 1080p30 (decisão do dono, 13/10/2026)
- Todos os padrões do kit agora são 1920×1080 a 30 fps: `hf.mjs` (--fps 30, escala 1), `render.py` (`fps` 30, `escala` 1 no edicao.json), `gerar_remotion.py`, `compor_fundo.py`. 4K/60 só se o dono pedir (`--escala 2 --fps 60`, `"escala": 2, "fps": 60`).
- Medido: cena de motion de 10 s → 116 s em 4K60, **28 s em 1080p30** (4×). Montagem do render.py: ~31 ms/quadro × 60 em 4K → **~12 ms/quadro × 30 em 1080p** (~5× menos CPU por segundo de vídeo; a aula de 8:29 que levou ~90 min deve cair para ~20 min — estimativa, ainda não medida num vídeo inteiro).
- `scripts/camera_lugar.py` (edição): acha a câmera fora do lugar ANTES do render (histograma da região da câmera × padrão do vídeo; 1 min para 18 min). Testado: achou os 3 trechos reais de um bruto de 18 min, sem alarme falso.
