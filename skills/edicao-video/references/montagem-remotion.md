# Montagem em camadas: Python + HyperFrames + Remotion (aula IA ON/OFF v3)

Cada ferramenta faz o que faz melhor; nenhuma faz o trabalho da outra.

| Camada | Quem | Comando | Por quê |
|---|---|---|---|
| Tela (cortes, pausas, zoom, fusão nas emendas) | `scripts/render.py --camada-tela` | sai `<saida>-tela.mp4` (câmera tapada, sem motions, CRF 10) + `<saida>-voz.wav` (PCM, -14 LUFS) | Um único redimensionamento Lanczos + nitidez |
| Cenas de motion | HyperFrames via `motion-design/kit/hf.mjs --fps 30` (1080p30) | `motions/hf/NN-*.mp4` | Mesma imagem do gravador próprio, 2–3× mais rápido |
| Montagem (câmera por cima, transições, capítulos, efeitos, áudio) | Remotion | `scripts/gerar_remotion.py fonte/edicao.json pasta-remotion` → `bash pasta-remotion/renderizar.sh` | Linha do tempo editável no Studio (`npm run dev`), animação por quadro, transições com mola/curva, `<Video>` com quadro exato |
| Entrega | `scripts/finalizar.py` (chamado pelo `renderizar.sh`) | padrão 1080p30 18 Mb/s, AAC 320 k, -14 LUFS | Uma única codificação final; o Remotion devolve vídeo CRF 10 + áudio PCM |

## Transições (da `motion-doctrine` / `cut-the-curve` do HyperFrames — plugin instalado)
- **Nunca fusão entre tela e cena.** Corte no meio do movimento, mesma direção e mesma velocidade dos dois lados, um lado visível por vez.
- **Tela → cena = empurrão (zoom-through):** a tela cresce 1→1,2 acelerando (0,2 s, desfoque até 18 px, apaga), corte, a cena entra crescendo 0,75→1 (0,5 s, expo.out). Origem do empurrão = onde a ação estava na tela (o "objeto" que a câmera atravessa).
- **Cena → tela = curva para a esquerda (a "corrente" do filme):** a cena sai acelerando 230 px (×escala) para a esquerda e some antes do corte; a tela entra da direita já em movimento e desacelera (0,3 s, power4).
- **Fechamento = zoom reverso (chegada):** a tela recua 1→0,8; o card chega grande (1,25→1). A câmera some junto.
- **Capítulos:** entrada em cascata palavra a palavra (waterfall), saída para a esquerda em ~75% do tempo da entrada.
- Orçamento: 2–3 tipos de transição por vídeo, repetidos.
- Efeito sonoro: um whoosh discreto (volume 0,16) em cada empurrão; nada mais (aula, não anúncio).

## Arquivos
- Modelo: `remotion/` desta skill (`package.json` com versões fixas 4.0.534, `tsconfig.json`, `remotion.config.ts`, `src/componentes.tsx`: Tela, Cena, Moldura, TrechoCamera, Capitulo).
- `renderizar.sh` (gerado): espera a vez na fila global, `npx remotion render Aula out/montagem.mkv --codec=h264 --crf=10 --x264-preset=veryfast --audio-codec=pcm-16` (uma passada; render separado só do áudio custava 4 min) e `finalizar.py` → arquivo de entrega.
- `gerar_remotion.py` escreve `src/Aula.tsx` com **um nó JSX por clipe** (cada trecho da câmera, cada cena, cada capítulo, cada whoosh): no Studio dá para mover/aparar cada um à mão, que é o que a skill oficial do Remotion pede.
- `edicao.json`: `motions` (tempos do vídeo editado; a de 0 = abertura, a com `sem_camera` = fechamento) e `capitulos [[ini, n, "texto"]]`.

## Cuidados (aconteceram)
- **Câmera lavada** (pretos claros, menos contraste) quando o Remotion lê o bruto HEVC 10 bits direto. O gerador cria `public/camera.mp4`: só o recorte da câmera, ampliado com Lanczos, H.264 BT.709 faixa limitada — os 37 trechos usam esse arquivo com o mesmo `trimBefore`. Conferir sempre: recorte da câmera v2 × v3 e o percentil 5 (preto) igual.
- O Remotion **não serve symlink** da pasta `public/` (404): o gerador usa hard link (não gasta disco).
- Fechamento tem que começar **antes** do fim da camada de tela, senão aparece quadro preto: o gerador limita `ini ≤ dur − 0,02`.
- `npx create-video --yes` falha dentro de repositório git: o projeto é montado à mão pelo gerador (package.json do modelo + `npm i`).
- Fotos antes do render: `npx remotion still Aula out/x.jpg --frame=N --scale=0.5`, nos pontos de costura (0,1 s antes e depois de cada uma).

## Render rápido (medido no Mac M4, 30 s da aula em 1080p30)
- `remotion.config.ts` do modelo: **GL "angle"** (composição e blur na GPU) 25 s × 82 s no "swangle" padrão do Remotion — 3,3× mais rápido; **concorrência 6** (4 = 26 s, 6 = 25 s, 8 = 27 s, 10 = 36 s: satura).
- Aula inteira (2min53): Remotion 219 s + finalizar 84 s = 303 s (antes, com áudio renderizado à parte, 593 s).
- Sincronia: a câmera de cada trecho usa os inteiros do edl (`from = q0`, `durationInFrames = nq`, `trimBefore = q_in`) — ver `sincronia.md`. Cenas e capítulos: fim = `round((ini + dur)·fps)` (sem buraco de 1 quadro).

## Câmera que muda de lugar (aula SLA do cliente B, 15/10/2026)
- Gravação do Screen Studio: câmera grande no centro na abertura, depois canto direito, depois canto esquerdo. Mapeie com quadros a cada 0,1 s (a troca é um corte ou uma fusão de ~0,25 s) e meça cada retângulo no pixel.
- `cameras` no `edicao.json` → `MolduraMovel` (um bloco por lugar; nos últimos 0,55 s voa até o próximo) + `TrechoCam` (recorte sem borda, `objectFit: cover`, `zoom` opcional). A troca de canto cai dentro de um corte: a câmera nunca mostra os quadros da fusão do original.
- Abertura com a câmera em `destino` (grande ao lado do texto da cena 00): o slot da cena some junto com o voo. Jump cuts do rosto disfarçados com `punch` (1 / 1,1 alternado).
- Sincronia da abertura não sai no `revisar.py` (a câmera está fora do lugar do bruto): meça a energia de movimento do miolo da câmera no final × bruto, quadro a quadro, por número de quadro (`select=between(n,…)`), nunca com `-ss` (dá ±1 quadro falso). Deu 0 quadro nos 7 trechos.
- `SeloStatus`: estado ao vivo por cima (ex.: SLA laranja → vermelho → verde durante o teste), troca na palavra.
- Render: aula de 5min17 com 6 cenas, 64 trechos e 3 lugares de câmera = 408 s (Remotion + finalizar).

## Camada Extras do projeto (aula SLA v3, 16/10/2026)
Se existir `remotion/src/Extras.tsx`, o `gerar_remotion.py` importa `Extras`, `PalcoTela` e `PalcoCamera`: a tela entra dentro de `PalcoTela` (poses de tela em cena: cartão 0,62–0,66 com raio e sombra), a câmera dentro de `PalcoCamera` (anda junto com o cartão — esconde o remendo da câmera tapada — e cresce 1,5× ancorada no canto nas falas de opinião) e `<Extras/>` vai por cima de tudo (abertura-relâmpago, holofotes, rótulos, passos, texto, card, sons). Modelo completo: `remotion/exemplos/Extras-aula-sla.tsx`.
- Coordenadas dos alvos: medidas no BRUTO com grade; nos trechos com anotação, `zoom_fixo` em 1× (começando ~0,5 s antes) para a tela = bruto.
- Página que rola no clique (ex.: "Salvo"): o destaque some junto com o clique (aconteceu: o anel ficou num espaço vazio 0,2 s depois).
- A sincronia medida pelo `revisar.py` fica "inconclusiva" nos trechos em que a câmera anda ou cresce; os trechos são os mesmos do edl — confira os medidos (0–1 ms) e diga isso na entrega.
