# Motores de render: qual usar (pesquisa e piloto de 07/10/2026)

As cenas continuam iguais: HTML com `cena(DUR, frame)` e `window.frame(t)`. O que muda é quem grava.

| Motor | Como chamar | Quando |
|---|---|---|
| **HyperFrames** (HeyGen, Apache-2.0, v0.8.140 fixa em `.ferramentas`) | `node kit/hf.mjs saida.mp4 --html cena.html` (1080p30, 40 Mb/s) · lote: `bash fonte/gravar-todos.sh` | **Padrão.** Mesma imagem, 2–3,4× mais rápido (vários Chromes em paralelo) |
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
3. `hyperframes render <pasta> -c .hf-<cena>.html --fps 30 --quality high --gpu --video-bitrate 40M --workers 8 [--resolution landscape-4k] [--format mov]` e apaga o temporário. Antes, o `<link>` do Google Fonts vira fontes embutidas do cache local (`kit/fontes-locais.mjs`) e a duração é lida já dessa cópia.
Por que assim: a API oficial de "frame source" dentro de iframe não ficava pronta (fontes do Google no iframe); a timeline-ponte na própria página funcionou de primeira e não exige mudar nenhuma cena.

## Velocidade no Mac (M4, 10 núcleos) — medido em 15/10/2026
Tempo interno (depois de pegar a vez na fila), cena 16:9 de 9,74 s; "antes" = ler a duração + render do `hf.mjs` antigo.
| Cena | antes, padrão antigo (60 fps) | antes a 30 fps | **agora (1080p30, 40 Mb/s)** | `--previa` |
|---|---|---|---|---|
| 18-parede-aulas (3D CSS) | 48,6 s | 32,5 s | **15,2 s** (2,1× × 30 fps; 3,2× × antigo) | 12,0 s |
| 07-tem-tudo (2D) | 33,8 s | 19,9 s | **12,1 s** (1,6×; 2,8×) | 10,2 s |
De onde veio (fases do HyperFrames com `HF_VERBOSE=1`):
- **Codificação no VideoToolbox (`--gpu`)**: encode 8,4 s → 1,8 s. Qualidade contra referência quase sem perda (x264 CRF 4): x264 CRF 16 = SSIM 0,9929 a 15 Mb/s; VideoToolbox padrão 0,9865 a 10 Mb/s (fraco!); **30 Mb/s 0,9939; 50 Mb/s 0,9957** → padrão 40 Mb/s. `--x264` volta ao CRF.
- **Ler a duração**: 5,1 s → 1,4 s. 2,3 s eram o Google Fonts baixando (agora cache local embutido) e 2,8 s eram esperas fixas no `gravar.mjs`.
- **Workers fixos (8)**: pula a calibração automática (setup 1,6 s → 0,2 s). 3 workers: captura 7,5 s; 5 (auto): 5,6 s; 8: 5,3 s; 10: sem ganho.
- A captura rápida (drawElementImage) desliga sozinha em cena com 3D CSS — a parede de aulas usa a captura comum.
- O que NÃO adiantou: mais workers que 8; `--quality draft` ganha pouco (~2–3 s), só serve para prévia.

## Desempenho na GPU (Windows, RTX 3050 + Intel UHD, 12 threads — medido por um colaborador em 11–13/10/2026)
| Gargalo | Antes | Depois | O que mudou |
|---|---|---|---|
| Chrome do render na GPU integrada (Intel) | cena 6,4 s alfa: 170 s | 128 s | preferência "alto desempenho" para cada `chrome-headless-shell.exe` — `kit/gpu-windows.mjs` (o `hf.mjs` roda sozinho no Windows) |
| Shader de fundo dentro de cada cena | 95 s | 23 s de captura | fundo gravado UMA vez (960×540, 30 fps) e composto no ffmpeg: `kit/compor_fundo.py` (furo da câmera + fade). Mais workers NÃO ajuda |
| Transcrição (faster-whisper medium) | CPU ~0,7× tempo real | 2 min de áudio em 20 s | CUDA (`transcrever.py` cai para CPU sozinho; no Mac vai direto para CPU) |
| Montagem Remotion 4K60 | 10 s em 197 s | 141 s | `remotion.config.ts` (só no Windows): `angle` + 8 processos + x264 `veryfast`; 12 processos é PIOR |
- Captura rápida do HyperFrames: a falha antiga era o bug do `id="st"` no comentário (corrigido no `hf.mjs`). Desligar: `HF_SEM_CAPTURA_RAPIDA=1`.
- Medido por ele: cena de 10 s → 116 s em 4K60 e 28 s em 1080p30 (4×) — base da decisão do dono pelo 1080p30.

## Remotion (adotado para a MONTAGEM final, não para gravar cenas)
- Desde a aula IA ON/OFF v3: as cenas continuam em HTML (gravadas pelo HyperFrames) e o Remotion monta o vídeo (câmera, transições, capítulos, áudio). Ver skill edicao-video, `references/montagem-remotion.md`.
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
