# Medir qualidade de imagem

"Ficou pixelado" pode ser três coisas diferentes, com consertos diferentes. Meça antes de mexer.

| Causa | Como aparece | Como medir | Conserto |
|---|---|---|---|
| **Compressão** (pouca taxa) | blocos em áreas lisas, texto "sujo" em volta | `scripts/qualidade.py comparar final.mkv sem-perda.mkv` (renderize o mesmo trecho com `--sem-perda`): SSIM < 0,99 | Conferir se saiu nos 18 Mb/s do padrão (a revisão mede); preset mais lento |
| **Aumento** (zoom sobre captura pequena) | texto mole, borda borrada, sem blocos | `qualidade.py recorte final.mp4 63 1100 150 800 400` e o mesmo recorte do bruto: o bruto também é mole no tamanho equivalente | Um único redimensionamento Lanczos + nitidez leve; zoom máx. 1,6×; captura maior (1440p/4K) na próxima gravação |
| **Plataforma** (YouTube/WhatsApp recomprimem) | o arquivo local está bom, o publicado não | comparar o arquivo local com o baixado | Enviar no padrão (1080p30, 18 Mb/s constante: arquivo rico recomprime melhor) |

Referência da 1ª aula editada: CRF 17 já era transparente (SSIM 0,9986, PSNR 51 dB contra sem perda) — o "pixelado" era aumento. A versão 4K resolveu com um único redimensionamento + motions nítidos. Desde 15/10/2026 a entrega é 1080p30 18 Mb/s (regra do dono): o redimensionamento único e a nitidez continuam.

Recorte 1:1 é a única forma honesta de olhar nitidez: folha de fotos reduzida esconde tudo.
