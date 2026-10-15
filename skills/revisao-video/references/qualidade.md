# Medir qualidade de imagem

"Ficou pixelado" pode ser três coisas diferentes, com consertos diferentes. Meça antes de mexer.

| Causa | Como aparece | Como medir | Conserto |
|---|---|---|---|
| **Compressão** (pouca taxa) | blocos em áreas lisas, texto "sujo" em volta | `scripts/qualidade.py comparar final.mkv sem-perda.mkv` (renderize o mesmo trecho com `--sem-perda`): SSIM < 0,99 | CRF menor (14 → 12), preset mais lento |
| **Aumento** (zoom sobre captura pequena) | texto mole, borda borrada, sem blocos | `qualidade.py recorte final.mp4 63 1100 150 800 400` e o mesmo recorte do bruto: o bruto também é mole no tamanho equivalente | Entrega 4K com um único redimensionamento Lanczos + nitidez leve; zoom máx. 1,6×; captura maior na próxima gravação |
| **Plataforma** (YouTube/WhatsApp recomprimem) | o arquivo local está bom, o publicado não | comparar o arquivo local com o baixado | Enviar 4K (YouTube dá mais taxa), CRF 12–14 |

Referência da 1ª aula editada: CRF 17 já era transparente (SSIM 0,9986, PSNR 51 dB contra sem perda) — o "pixelado" era aumento. A versão 4K resolveu com um único redimensionamento + motions gravados em 4K.

Recorte 1:1 é a única forma honesta de olhar nitidez: folha de fotos reduzida esconde tudo.
