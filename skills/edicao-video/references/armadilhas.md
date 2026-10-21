# Armadilhas da edição (cada uma aconteceu)

| Sintoma | Causa | Como evitar |
|---|---|---|
| Corte come o começo da palavra seguinte / sobra meia sílaba | Tempo do Whisper erra a borda em ~0,15 s | Borda no silêncio (o plano faz) ou medida com `perfil.py` e `"exato"`; ouça com `ouvir_emendas.py` |
| "É" arrastado continua depois do corte | Sem silêncio entre ele e a palavra, o ajuste recua para antes dele | Medir o vale e marcar `"exato"` |
| Aceleração 4× "não fez sentido" | Caiu no meio de uma frase ("para [4×] um estágio") | Aceleração desligada por padrão; corte + fusão |
| Anel branco em volta da câmera | Retângulo 1 px maior que a câmera pegou a borda clara do original | Medir o retângulo exato; `camera_recuo` 2 px |
| Vídeo "pixelado" | Zoom de 1,6× sobre captura 1080p | Um único redimensionamento Lanczos, nitidez leve antes de ampliar, zoom máx. 1,6×; pedir captura maior (1440p/4K — o `normalizar.py` mantém a resolução do bruto). Entrega continua 1080p30 (regra do dono) |
| Tela "pisca" na emenda | Corte entre duas telas diferentes | `fusao` (o plano marca quando a tela muda) |
| Vários decodificadores em paralelo não geram nada | Disputa do decodificador de vídeo do Mac (videotoolbox) | Renders de teste um de cada vez |
| `rm $P/...` bloqueado | Variável vazia viraria `/` | `"${P:?}"/arquivo` |
| zsh não divide lista de arquivos / `set -- $v` | Diferença zsh × bash | Rodar laços com `bash -c '…'` |
| ffmpeg sem `drawtext` | Compilado sem freetype | Texto em foto com OpenCV/Pillow |
| Motion fora de sincronia depois de mudar um corte | `ini` das cenas é do tempo editado | Recalcular pela palavra (`src` → `t` em `palavras-final.json`) |
| Câmera "lavada" na montagem do Remotion | `<Video>` lendo HEVC 10 bits do bruto com a faixa de cor errada | `camera.mp4` intermediário (recorte do bruto normalizado, H.264 BT.709 tv) — o gerador faz |
| Pretos esmagados / brancos estourados | Bruto HEVC 10 bits em faixa COMPLETA (0–1023) lido como faixa limitada | `normalizar.py` respeita a faixa marcada no arquivo e converte uma vez para 8 bits BT.709 limitado |
| Quadro preto antes do fechamento | Card de fechamento começando depois do fim da camada de tela | O gerador limita o início do fechamento ao fim da tela |
| 404 em arquivo da pasta public/ do Remotion | Symlink | Hard link (o gerador faz) |
| Câmera desencontrada da voz, piorando ao longo do vídeo | Bruto com taxa VARIÁVEL (OBS perdendo quadro, gravação de tela, iPhone); o render contava quadros como se fossem tempo | `normalizar.py` antes de tudo (30 fps constante pelo tempo real de cada quadro); `render.py` recusa bruto fora do ritmo; `revisar.py` mede (ver `sincronia.md`) |
| Câmera até 21 ms fora da voz e 1 quadro sem câmera entre trechos (Remotion, v3 do cliente B) | `from = round(ini·fps)` e `trimBefore = round(in·fps)` arredondados cada um para um lado; `durationInFrames = round(dur·fps)` deixava buraco | Cortes na grade de 30 fps desde o `plano.py` (`q_in`, `q0`, `nq` inteiros); o gerador usa os inteiros: trechos encostam por construção |
| Motion de 60 fps andando em câmera lenta numa saída de 30 | Leitura quadro a quadro sem olhar o tempo | `fps=30` no filtro de leitura dos motions (render.py faz) |
| "Telinha branca" de 1 quadro em alguns cortes (Remotion) | Soma dos arredondamentos de início + duração deixava 1 quadro sem clipe | Fim de cada clipe = `round((ini+dur)·fps)`; trechos da câmera com os inteiros do edl |
| Dono: "cortou demais" | Pausas cortadas a partir de 0,38 s com 0,08–0,12 s de margem: fala sem respiro | Talking head de anúncio: cortar só pausa ≥ 0,5 s, margem 0,2 s antes / 0,15 s depois |
| Câmera colada no lugar errado + câmera real com zoom em outro canto | O apresentador trocou a cena do OBS; o render usa um retângulo fixo | `camera_lugar.py` antes do render; trechos em `camera_fora` (s do bruto) saem no quadro original, sem zoom |
| Bloco chapado em volta da câmera durante o zoom | O lugar da câmera no fundo era pintado com uma cor; com zoom esse retângulo cresce para fora da câmera colada | `tapar_camera` reconstrói por inpainting (1/4 da resolução) |
| Câmera dobrada por ~0,2 s | Fusão numa emenda em que a câmera muda de canto (`camera_fora`) | O render não funde quadros com a câmera em lugares diferentes: corte seco |
| Voz escorregando depois de cada emenda de uma gravação em partes | `concat -c copy`: o áudio de cada parte é ~30 ms mais curto que o vídeo e o vídeo ganhou 44 ms de deslocamento | `scripts/juntar.py`: normaliza parte por parte e corta o áudio no número exato de quadros de cada uma |
| Câmera colada no lugar errado em metade do vídeo | A bolha da câmera muda de canto (Screen Studio) | Mapear os lugares (quadros a cada 0,1 s) e usar `cameras`; troca dentro de um corte |
| Whisper juntou uma frase repetida ("eu vou usar esse gatilho, [8 s] eu vou usar esse gatilho") como uma só, com tempos esticados | Palavra com duração de vários segundos na transcrição | Transcrever de novo só o trecho e ler o perfil de volume (`-120 dB` = gate fechado entre as tomadas) |
| Foto do Remotion verde | 17 `remotion still` em paralelo disputando o decodificador | Fotos em série (ou poucas por vez); o arquivo estava íntegro |
| Dono: "falei errado, cortou, falei certo, mas a vez errada ainda pegou" (8 casos na aula SLA) | A transcrição do vídeo inteiro deduplica frase repetida: a tomada errada nem aparece no `frases.txt` | `scripts/ilhas.py` (cada ilha de fala transcrita sozinha) antes de decidir os cortes, e de novo no final |
| Zoom fora do lugar depois de mudar cortes | `zoom.json` está no tempo do editado; corte novo desloca tudo | Mudou corte → `plano.py` → **`zoom.py`** → render (e motions/capítulos retemporizados) |
