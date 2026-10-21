# Imagem: padrão de entrega, qualidade, zoom e câmera

## Padrão de entrega (regra principal do dono, 15/10/2026)
**1920×1080 · 30 fps constante · H.264 High · 18 Mb/s constante (CBR) · AAC 320 k 48 kHz · -14 LUFS · BT.709.**
Os números moram em `scripts/padrao.py` (render.py, finalizar.py e gerar_remotion.py importam de lá). A revisão (`revisar.py`, skill revisao-video) reprova fora disso: resolução, fps, codec/perfil, 16–20 Mb/s, áudio, -14 ±1 LUFS, pico ≤ -1, BT.709.
- **Por que CBR:** o x264 em taxa média gasta pouco em tela parada (já saiu 7,7 Mb/s pedindo 20). Com `nal-hrd=cbr` a taxa fica no alvo; o dono pediu "bitrate alto" e o YouTube recomprime melhor a partir de um arquivo rico.
- **Antes era 4K60.** Saiu da regra: o render ficava muitas vezes mais lento (4× pixels × 2× quadros; ver `references/sincronia.md`, tempos) e não era o que o dono pede. 4K (`"escala": 2`) ou 60 fps (`"fps": 60`) só se ele pedir para uma peça.
- **Motions intercalados também em 1080p30:** `node skill/kit/hf.mjs cena.mp4 --html cena.html --fps 30` (escala 1). O render lê qualquer motion pelo tempo de cada quadro (`fps=30` no filtro), então um motion antigo de 60 fps entra na velocidade certa; mesmo assim, grave em 30.
- Peça que não saiu do render.py nem do Remotion (motion solto, vídeo de outro lugar): `scripts/finalizar.py video.mp4 saida.mp4` deixa no padrão numa única codificação.

## Qualidade (o dono achou a 1ª entrega "pixelada")
- O que "pixela" num vídeo de tela é quase sempre o **aumento**, não a compressão. Zoom de 1,6× sobre captura 1080p estica cada pixel. Medido: em CRF 17 a compressão já era invisível (SSIM 0,9986 contra render sem perda).
- **Um único redimensionamento** do bruto direto para a saída (zoom + escala juntos, Lanczos), com realce leve só no que sofre zoom (`"nitidez": .35`, aplicado antes de ampliar).
- **Bruto em 4K continua em 4K** no `normalizar.py` (só o ritmo e a cor mudam): o zoom de 1,6× numa captura 4K entregue em 1080p sai mais nítido que o original. **O que mais melhora é a captura:** peça ao dono para gravar a tela em 1440p ou 4K (canvas do OBS), escala do sistema em 100%.
- **Faixa de cor:** respeite a marcada no arquivo. O bruto do cliente B é HEVC 10 bits em **faixa completa** (0–1023) marcado como tal; os scripts antigos liam como faixa limitada (pretos esmagados, brancos estourados). O `normalizar.py` converte certo para 8 bits BT.709 limitado e daí em diante tudo é "tv".
- Para medir em vez de achar: skill revisao-video, `qualidade.py` (comparar com render sem perda; recorte 1:1 de texto).

## Zoom
- Segue a caixa onde a tela mexe (cliques, painéis), até 1,6×, parado ≥ 4 s, só muda se o alvo novo se mantém 1,5 s. Transição suave de 0,8 s.
- Zoom é para **ler**: painel lateral, campo sendo preenchido. Tela inteira mudando (troca de página) → volta para 1×.
- Ajuste manual: `"zoom_fixo": [[t_ini, t_fim, z, cx, cy]]` no tempo editado.

## Câmera do apresentador
- Fica **fixa por cima** e nunca entra no zoom. No fundo que sofre zoom, o lugar dela é reconstruído com a vizinhança (inpainting em 1/4 da resolução); a cor chapada antiga aparecia como bloco em volta da câmera quando o zoom crescia.
- **Meça o retângulo exato** (primeiro e último pixel escuro em cada lado, num quadro em que o fundo em volta é claro). Um pixel a mais pega a borda clara do recorte original e aparece um **anel branco** (aconteceu). O render ainda recorta 2 px para dentro (`camera_recuo`) e suaviza a borda, com raio próximo ao do original (`camera_raio`).
- **Câmera que muda de lugar** (cena do OBS trocada no meio): `scripts/camera_lugar.py fonte/edicao.json` acha os trechos e imprime `"camera_fora"`; nesses trechos sai o quadro original, sem colar câmera nem zoom, e a fusão não mistura quadros com a câmera em lugares diferentes.
- Sombra suave embaixo para descolar da tela.
- **Sincronia da câmera com a voz:** ver `references/sincronia.md`.

## Mudança visual (tutorial)
- Conta como mudança: motion, troca de zoom, capítulo, troca de página com fusão, câmera em tela cheia.
- **Alarme (não meta): trecho > 40 s sem nenhuma mudança** → avaliar zoom num detalhe, um motion curto
  de reforço ou corte. Em trecho de rosto: punch-in 1,1× a cada 2–3 cortes, não em todos.
- Teto: no máximo ~3 chamadas/destaques por minuto (alunos acharam 4/min demais).
- Motion que só enfeita sai (coerência de Mayer). Cada motion explica uma ideia da fala.
