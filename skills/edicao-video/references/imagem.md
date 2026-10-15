# Imagem: qualidade, zoom e câmera

## Qualidade (o dono achou a 1ª entrega "pixelada")
- O que "pixela" num vídeo de tela é quase sempre o **aumento**, não a compressão. Uma gravação 1080p com zoom de 1,6× estica cada pixel. Medido: em CRF 17 a compressão já era invisível (SSIM 0,9986 contra render sem perda).
- **Entrega em 4K** (`"escala": 2`): o render faz **um único redimensionamento** do bruto direto para 3840×2160 (zoom + escala juntos, Lanczos), com realce leve só no que sofre zoom (`"nitidez": .35`). No YouTube, vídeo enviado em 4K recebe muito mais taxa de bits; mesmo quem assiste em 1080p vê melhor.
- **Motions em 4K de verdade:** grave as cenas com `--escala 2` (a página continua 1920×1080, a saída sai 3840×2160 nítida). Imagem raster dentro da cena fica mole em 2×: prefira SVG.
- **CRF 14** (x264, preset medium em 4K), cores BT.709 explícitas na entrada e na saída.
- **O que mais melhora é a captura.** Peça ao dono para gravar a tela em 1440p ou 4K (canvas do OBS) e com a escala do sistema em 100%: texto pequeno numa captura 1080p de uma tela grande já nasce mole.
- Para medir em vez de achar: skill revisao-video, `qualidade.py` (comparar com render sem perda; recorte 1:1 de texto).

## Zoom
- Segue a caixa onde a tela mexe (cliques, painéis), até 1,6×, parado ≥ 4 s, só muda se o alvo novo se mantém 1,5 s. Transição suave de 0,8 s.
- Zoom é para **ler**: painel lateral, campo sendo preenchido. Tela inteira mudando (troca de página) → volta para 1×.
- Ajuste manual: `"zoom_fixo": [[t_ini, t_fim, z, cx, cy]]` no tempo editado.

## Câmera do apresentador
- Fica **fixa por cima** e nunca entra no zoom. No fundo que sofre zoom, o lugar dela é pintado com a cor da tela logo acima (senão aparece uma câmera gigante atrás).
- **Meça o retângulo exato** (primeiro e último pixel escuro em cada lado, num quadro em que o fundo em volta é claro). Um pixel a mais pega a borda clara do recorte original e aparece um **anel branco** (aconteceu). O render ainda recorta 2 px para dentro (`camera_recuo`) e suaviza a borda, com raio próximo ao do original (`camera_raio`).
- Sombra suave embaixo para descolar da tela.
