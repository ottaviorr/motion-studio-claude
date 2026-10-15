# Armadilhas da edição (cada uma aconteceu)

| Sintoma | Causa | Como evitar |
|---|---|---|
| Corte come o começo da palavra seguinte / sobra meia sílaba | Tempo do Whisper erra a borda em ~0,15 s | Borda no silêncio (o plano faz) ou medida com `perfil.py` e `"exato"`; ouça com `ouvir_emendas.py` |
| "É" arrastado continua depois do corte | Sem silêncio entre ele e a palavra, o ajuste recua para antes dele | Medir o vale e marcar `"exato"` |
| Aceleração 4× "não fez sentido" | Caiu no meio de uma frase ("para [4×] um estágio") | Aceleração desligada por padrão; corte + fusão |
| Anel branco em volta da câmera | Retângulo 1 px maior que a câmera pegou a borda clara do original | Medir o retângulo exato; `camera_recuo` 2 px |
| Vídeo "pixelado" | Zoom de 1,6× sobre captura 1080p, entregue em 1080p | Entrega 4K, um único redimensionamento Lanczos, nitidez leve, motions em 4K; pedir captura maior |
| Tela "pisca" na emenda | Corte entre duas telas diferentes | `fusao` (o plano marca quando a tela muda) |
| Vários decodificadores em paralelo não geram nada | Disputa do decodificador de vídeo do Mac (videotoolbox) | Renders de teste um de cada vez |
| `rm $P/...` bloqueado | Variável vazia viraria `/` | `"${P:?}"/arquivo` |
| zsh não divide lista de arquivos / `set -- $v` | Diferença zsh × bash | Rodar laços com `bash -c '…'` |
| ffmpeg sem `drawtext` | Compilado sem freetype | Texto em foto com OpenCV/Pillow |
| Motion fora de sincronia depois de mudar um corte | `ini` das cenas é do tempo editado | Recalcular pela palavra (`src` → `t` em `palavras-final.json`) |
| Câmera "lavada" na montagem do Remotion | `<Video>` lendo HEVC 10 bits do bruto com a faixa de cor errada | `camera.mp4` intermediário (recorte + Lanczos, H.264 BT.709 tv) — o gerador faz |
| Quadro preto antes do fechamento | Card de fechamento começando depois do fim da camada de tela | O gerador limita o início do fechamento ao fim da tela |
| 404 em arquivo da pasta public/ do Remotion | Symlink | Hard link (o gerador faz) |
| "Telinha branca" de 1 quadro em alguns cortes (Remotion) | `from=round(ini*fps)` + `durationInFrames=round(dur*fps)`: a soma dos arredondamentos deixa 1 quadro sem nenhum trecho, aparece o fundo | Fim de cada clipe = `round((ini+dur)*fps)` e duração = fim − início; conferir varrendo o vídeo final atrás de quadros só de fundo |
| Dono: "cortou demais" | Pausas cortadas a partir de 0,38 s com 0,08–0,12 s de margem: fala sem respiro, 21 cortes em 74 s | Talking head de anúncio: cortar só pausa ≥ 0,5 s, margem 0,2 s antes / 0,15 s depois |
| Câmera colada no lugar errado + câmera real com zoom em outro canto | O apresentador trocou a cena do OBS e a câmera foi para o outro canto por ~10 s; o render usa um retângulo fixo | Varrer o bruto (canto esquerdo × direito, região escura da cortina, 0,5 fps) antes de renderizar; trechos fora do lugar vão em `camera_fora` (s do bruto) e saem no quadro original, sem zoom |
| Bloco chapado em volta da câmera durante o zoom | O lugar da câmera no fundo era pintado com a cor da linha de cima; com zoom esse retângulo cresce para fora da câmera colada e aparece (revisor independente) | `tapar_camera` agora reconstrói por inpainting (1/4 da resolução); conferir quadros com zoom perto da câmera |
| Câmera dobrada por ~0,2 s | Fusão (dissolve) numa emenda em que a câmera muda de canto (`camera_fora`) | O render não funde quadros com a câmera em lugares diferentes: corte seco |
