# Montagem em camadas: Python + HyperFrames + Remotion (aula de exemplo v3)

Cada ferramenta faz o que faz melhor; nenhuma faz o trabalho da outra.

| Camada | Quem | Comando | Por quê |
|---|---|---|---|
| Tela (cortes, pausas, zoom, fusão nas emendas) | `scripts/render.py --camada-tela --crf 10` | sai `<saida>-tela.mp4` (câmera tapada, sem motions) + `<saida>-voz.m4a` | Um único redimensionamento Lanczos + nitidez: o melhor 4K a partir de captura 1080p |
| Cenas de motion | HyperFrames via `motion-design/kit/hf.mjs --escala 2` | `motions/hf/NN-*.mp4` | Mesma imagem do gravador próprio, 2–3× mais rápido |
| Montagem (câmera por cima, transições, capítulos, efeitos, áudio) | Remotion | `scripts/gerar_remotion.py fonte/edicao.json pasta-remotion` → `npx remotion render Aula saida.mp4 --codec=h264 --crf=14 --color-space=bt709` | Linha do tempo editável no Studio (`npm run dev`), animação por quadro, transições com mola/curva, `<Video>` com quadro exato |

## Transições (da `motion-doctrine` / `cut-the-curve` do HyperFrames — plugin instalado)
- **Nunca fusão entre tela e cena.** Corte no meio do movimento, mesma direção e mesma velocidade dos dois lados, um lado visível por vez.
- **Tela → cena = empurrão (zoom-through):** a tela cresce 1→1,2 acelerando (0,2 s, desfoque até 18 px, apaga), corte, a cena entra crescendo 0,75→1 (0,5 s, expo.out). Origem do empurrão = onde a ação estava na tela (o "objeto" que a câmera atravessa).
- **Cena → tela = curva para a esquerda (a "corrente" do filme):** a cena sai acelerando 230 px (×escala) para a esquerda e some antes do corte; a tela entra da direita já em movimento e desacelera (0,3 s, power4).
- **Fechamento = zoom reverso (chegada):** a tela recua 1→0,8; o card chega grande (1,25→1). A câmera some junto.
- **Capítulos:** entrada em cascata palavra a palavra (waterfall), saída para a esquerda em ~75% do tempo da entrada.
- Orçamento: 2–3 tipos de transição por vídeo, repetidos.
- Efeito sonoro: um whoosh discreto (volume 0,16) em cada empurrão; nada mais (aula, não anúncio).

## Arquivos
- Modelo: `remotion/` desta skill (`package.json` com versões fixas 4.0.534, `tsconfig.json`, `src/componentes.tsx`: Tela, Cena, Moldura, TrechoCamera, Capitulo).
- `gerar_remotion.py` escreve `src/Aula.tsx` com **um nó JSX por clipe** (cada trecho da câmera, cada cena, cada capítulo, cada whoosh): no Studio dá para mover/aparar cada um à mão, que é o que a skill oficial do Remotion pede.
- `edicao.json`: `motions` (tempos do vídeo editado; a de 0 = abertura, a com `sem_camera` = fechamento) e `capitulos [[ini, n, "texto"]]`.

## Cuidados (aconteceram)
- **Câmera lavada** (pretos claros, menos contraste) quando o Remotion lê o bruto HEVC 10 bits direto. O gerador cria `public/camera.mp4`: só o recorte da câmera, ampliado com Lanczos, H.264 BT.709 faixa limitada — os 37 trechos usam esse arquivo com o mesmo `trimBefore`. Conferir sempre: recorte da câmera v2 × v3 e o percentil 5 (preto) igual.
- O Remotion **não serve symlink** da pasta `public/` (404): o gerador usa hard link (não gasta disco).
- Fechamento tem que começar **antes** do fim da camada de tela, senão aparece quadro preto: o gerador limita `ini ≤ dur − 0,02`.
- `npx create-video --yes` falha dentro de repositório git: o projeto é montado à mão pelo gerador (package.json do modelo + `npm i`).
- Fotos antes do render: `npx remotion still Aula out/x.jpg --frame=N --scale=0.5`, nos pontos de costura (0,1 s antes e depois de cada uma).
