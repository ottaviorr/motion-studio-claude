# Armadilhas (cada uma já aconteceu)

| Sintoma | Causa | Como evitar |
|---|---|---|
| Textos aparecem todos juntos; uma tela fica deformada | ID de texto igual ao de tela (`#t1` título × `TELA('t1')`): o CSS de `#t1` pega os dois e `$('t1')` devolve o errado | Textos com `h1, h2…`; telas com `t…` |
| A cena inteira não anima | Variável com nome da base (`const C=…`, `M`, `p`, `eo`…) | Nomes próprios (`CL`, `LISTA`) |
| Arquivo da cena sai vazio ou cortado | Escrito por heredoc do shell com `${…}`/crases | Escrever com o editor de arquivos, não com `cat <<EOF` |
| Uma gravação sai com a página de OUTRA cena / foto "atrasada" | Vários Chrome na mesma porta sorteada | Sempre `--remote-debugging-port=0` + `DevToolsActivePort` (já no `kit/gravar.mjs`) |
| `.mov` "sem transparência" no ffmpeg | O ffmpeg não lê o alfa do HEVC | Conferir com `kit/alfa.swift` (AVFoundation) |
| Lista de arquivos vira um item só | zsh não divide `$L` / `set -- $x` | Rodar laços de arquivos com `bash -c '…'` |
| Clique no login não faz nada, página recarrega com `?` | O script do app ainda não carregou | Esperar 4–5 s depois de abrir |
| Texto em branco some no fundo claro (ex.: logo da marca) | Logo/nome pensados para fundo escuro | `LOGO(h,{cor})` e versão de logo para fundo claro |
| Câmera "erra o alvo" ao aproximar | Fórmula de translate somando posição duas vezes | Elemento em `left:0;top:0` e só `transform` (ou `cam()`) |
| Motion por cima do rosto cobre o rosto/mão | Conteúdo largo demais | Manter à esquerda (x < ~680 em 1920) e conferir com `ROSTO=quadro.jpg` |
| Palavra-chave com duplo sentido | Trocadilho visual | Frase literal |
| Preço "a partir de" quando o valor é médio | Arredondamento da fala | Usar a regra da marca (`MARCA.regras`) |
| Um elemento sai no lugar errado mesmo com `left/top` certos | Regra mais específica da cena vence (`#forno svg{…}` pega o `<svg id="pao">` dentro do forno) | Seletores por classe ou id direto; evite `#pai tag` genérico |
| Comando de terminal quebra com `echo ===` ou linha de `====` | No zsh, `=palavra` é expandido | Use `echo '---'` (entre aspas) ou rode com `bash -c` |
| Texto some dentro de um cartão branco (só aparece a linha de baixo) | O `#st` tem `color` claro e o texto sem cor própria herda o branco | Dê `color` ao cartão claro (ex.: notificação, réplica de app) |
| Cena inteira não anima ("Identifier 'CEL' has already been declared") | `CEL`, `TELA`, `NAV`, `LOGO`, `cursor` também são nomes da base | Nomes de tempo com sufixo próprio (`CELU`, `TEL_`) |
| Duração/tempos por cena não mudam (clipe sai com a duração antiga) | Script no `<head>` lê `document.title` antes do `<title>` existir | Ler o título dentro de uma função chamada no `frame`/`cena`, não no topo |
| Cena promete algo que a fala não prometeu (ex.: semana inteira acesa em "quem usa o sistema todo dia") | Desenhar a palavra solta, não o sentido da frase | Antes de ilustrar uma palavra, ler a frase inteira: de quem/de quê ela fala |
| Legenda com frase que ninguém falou | O Whisper inventa palavras com duração zero (várias com o mesmo tempo) | Antes da legenda, procurar palavras com `t == e` ou tempos repetidos e tirar |
| Endereço digitado sai com espaços ("app. suaagencia .com.br") | Barra de endereço é `display:flex` com `gap`: cada pedaço vira um item | Pôr o texto do endereço inteiro dentro de um único `<span>` |
| `afade ... d=.8` faz o ffmpeg falhar ("Unable to parse d") | Número sem o zero antes do ponto | Escreva `0.8` em filtros do ffmpeg |
| Legenda queimada não aparece / overlay ignora transparência | HEVC com alfa não é lido pelo ffmpeg | Grave a camada em ProRes 4444 (`gravar.mjs --prores`) e sobreponha com `overlay=format=auto` |
| Linha reta com brilho (`feGaussianBlur`) some do SVG | Filtro em `objectBoundingBox`: linha horizontal tem caixa de altura 0 | `filterUnits="userSpaceOnUse"` com x/y/width/height do desenho |
| Elemento sai com a cor/fonte de outro componente (ex.: `.ch`) | Classe genérica repetida entre CSS de réplicas (crm.css × vert.css) | Prefixe classes nas réplicas ou não carregue os dois CSS na mesma cena |
| Nas folhas de conferência, a página "vazia" em t=0 | Elemento entra com `pop` de 0 → gancho perde o 1º segundo | No anúncio, o que segura o gancho começa em `pop(...,-1,...)` (já visível) |
| Corte de fala come o começo da palavra seguinte ou deixa meia sílaba | O Whisper erra a borda da palavra em ~0,1–0,15 s (e gravação com noise gate tem −120 dB colado na fala) | Borda de corte no último silêncio antes da fala (skill edicao-video) e confira transcrevendo o trecho já cortado |
| "É" arrastado colado na palavra seguinte não sai no corte | Sem silêncio entre o "é" e a palavra, o ajuste automático recua para antes do "é" | Meça a borda no perfil de volume e marque o corte como `"exato"` |
| Transcrição diz que ele errou ("tirei a IA desativada") mas ele falou certo | Primeira passada do Whisper errou | Antes de apontar erro de fala, confirme na transcrição do vídeo final (skill revisao-video) ou num recorte |
| Folha de fotos sem texto / filtro `drawtext` não existe | O ffmpeg desta máquina não tem freetype | Escrever rótulos com OpenCV/Pillow |
| Vídeo sai a 30 fps quando a gravação é 60 | `gravar-todos.sh` usava o padrão do `gravar.mjs` | `FPS=60 bash fonte/gravar-todos.sh` |
| `fotos.sh` fotografa com o gravar.mjs da skill, não com a cópia da pasta | Caminho fixo | `GRAVAR=$PWD/gravar.mjs bash fotos.sh ...` |
| Elementos criados em laço (`.map`) ficam todos empilhados | Esqueceu `left:${x}px` no template | Só a folha de fotos mostra: sempre olhar |
| Troca com `sed` "funciona" mas não troca nada | Texto inserido com aspas escapadas (`\"`) | `grep -c` depois de cada troca |
| MP4 de cena muda de contraste em outro editor | O gravador saía em faixa completa BT.601 (`yuvj420p`) | Corrigido: `gravar.mjs` sai em BT.709 faixa limitada; quem lê MP4 antigo deixa o ffmpeg ler a cor marcada no arquivo |
| Gravar em 4K enche o disco | `--escala 2`: ~0,8 MB por foto, cena de 10 s com blur 3 ≈ 1,5 GB temporário, ~5 min | Grave 2–3 de cada vez e olhe o espaço livre antes |
| Espaço some em volta do "·" ("Exemplo·etapa") | Separador em `<i>`/`<span>` dentro de flex perde os espaços | Padding no separador; conferir com zoom na foto |
| "IA" em serif itálico lê como "/A" | Sigla curta na Instrument Serif itálica | Serif só em palavra comum |
| Peça por cima (capítulo) some no fim do vídeo de repente | Saída terminando no último quadro (a 60 fps o último é 2,983 s, não 3,0) | Termine a saída antes do último quadro; confira por cima de um quadro claro e de um escuro |
| HyperFrames: "Composition has zero duration" / "Runtime ready: false" | Cena em iframe com frame source: as fontes do Google no iframe não ficam prontas | Usar `kit/hf.mjs` (ponte de timeline na própria página da cena) |
| HyperFrames: "Unsupported ProRes rate control" | `--crf` com saída `.mov` | O `hf.mjs` já tira o `--crf` no .mov |
| HyperFrames em 4K com transparência não sai | O HyperFrames só faz 4K em MP4 | Alfa em 4K: `gravar.mjs --prores --escala 2` |
| `npx create-video --yes` (Remotion) falha | Roda dentro de um repositório git | Criar o projeto fora do repositório |
| Título cai no momento errado da fala | `W('palavra')` sem índice devolve a 1ª ocorrência; palavra curta repete muito ("se", "no", "e" também casa com "é") | Use a palavra seguinte, mais rara, ou o índice da ocorrência: `W('no',2)`; confira na folha de fotos |
| Folha de fotos em pé sai achatada | `grade.sh` força 960×540 | Para 9:16 use a folha da skill revisao-video (`revisar.py --fotos N`) ou uma folha própria em pé com a zona segura desenhada |
| Fonte do Google às vezes não carrega na foto (sai serif genérica) | `<link>` do Google Fonts sem tempo de carregar | Baixe as `.woff2` para `base/fontes/` + `@font-face` local, e um elemento escondido usando cada peso antes do quadro 0 |
| Agentes em paralelo sobrescrevem scripts de rascunho | Mesmo caminho no scratchpad | Cada agente com a sua pasta (`scratchpad/<prefixo>/`) |
| Render no HyperFrames muito mais lento | `drop-shadow`/`mix-blend-mode` desligam a captura rápida | Sombra com `box-shadow` em elemento opaco; grão como imagem, não blend |
| Reel "com bitrate alto" saiu com 7,7 Mb/s | `--video-bitrate` (média) gasta pouco em cena fácil; x264 só respeita mínimo em CBR | `gerar_reel.py` faz ProRes HQ intermediário → x264 CBR (`nal-hrd=cbr`, minrate=maxrate=bitrate) |
| Medida de largura errada (moldura maior que o texto) | Medida feita no carregamento, antes da fonte | Medir dentro do `frame(t)` e redesenhar só quando o tamanho mudar |
| Música alta demais, a fala fica difícil de entender (o dono reclamou) | Música abaixada por um fator fixo; as vozes do ElevenLabs saem com volumes muito diferentes (-19 a -26 LUFS) e as trilhas vêm altas (-7 a -15) — numa delas a música ficou MAIS alta que a voz | `gerar_reel.py` mede voz e trecho da música (LUFS) e põe a música 21 dB abaixo da voz; efeitos acompanham o nível da voz. Conferir no final: trecho com voz × fecho só com música (~20 dB de diferença) |
| Corte "atrasado" ~20 ms em relação ao bumbo no vídeo final | atraso do decodificador de MP3 (a faixa medida crua × a faixa tocada pelo Remotion) | meça o bumbo NO ARQUIVO FINAL e adiante a música (batida0 + ~0,02 s) |
| `$M:linear=true` virou "inear=true" no ffmpeg | no zsh, `$VAR:l` é modificador (minúsculas) | sempre `${VAR}` antes de `:` em linha de comando |
| Faixa marquee fica sem texto no fim | texto de comprimento fixo correndo por muitos segundos | repita o texto o bastante para vel × duração (e mais, se o BPM acelerar a cena) |
| `batidas.py` deu 113,3 BPM numa faixa de 85 | bumbo sincopado 3-3-2: a autocorrelação lê 4/3 do real (nenhum critério automático acertou) | conte os bumbos no trecho usado e rode `batidas.py faixa.mp3 --bpm 85` (ele sempre lembra o 3/4) |
| Cortes escorregam ~130 ms até o drop | BPM médio da faixa (120,215) × real (121,000): erro pequeno que acumula | `batidas.py faixa.mp3 --trecho INI FIM` (grade fina só no trecho usado) e confira o bumbo do arquivo final contra os cortes (±30 ms) |
| Vidro three.js clareia / sai cinza | fundo transparente + `transmission`; em r149, ColorManagement desligado | vidro escuro e fosco: `transmission: 0`, `clearcoat 1`, `clearcoatRoughness .045`; `kit/objeto3d.js` liga a cor certa em r149 e r152+. Fixe UMA versão do three por projeto (r149 sai ~7 % mais claro que o r186) |
| `HF_DE_COMPOSITION_ROOT_MISSING` no HyperFrames | o `id="st"` citado num comentário do CSS recebia os atributos da composição | corrigido no `hf.mjs`: só troca o `id="st"` depois do `<body>` (achado de um colaborador) |
| Cada cena levava 3–5 s antes de começar a gravar | o Chrome baixava o Google Fonts só para ler a duração (2,3 s) e esperava 1,5 + 0,8 s fixos | `hf.mjs` embute as fontes do cache local (`kit/fontes-locais.mjs`) e o `gravar.mjs --dur` espera o carregamento de verdade: 5,1 s → 1,4 s |
| `.mp4` do hf.mjs com menos de 40 Mb/s | no VideoToolbox a taxa é alvo, cena fácil gasta menos (deu 18 Mb/s numa cena simples) | normal: a qualidade medida (SSIM) é a que importa. Se precisar de CRF fixo, `--x264` |
| Desfoque com "degraus" (cópias do objeto) | poucas amostras: o objeto anda mais de 1/3 da própria largura entre duas | `desfoque.sh` com o padrão (16 subquadros a 30 fps); o HyperFrames grava no máximo 240 fps por passada |
| Captura rápida do HyperFrames não liga | cena com 3D CSS (`perspective`, `preserve-3d`, `backface-visibility`) | normal; a cena grava pela captura comum. Para medir: `HF_VERBOSE=1` mostra o motivo |
| Película/ruído diferente entre renders | `Math.random` ou hash com `Math.sin` (varia entre motores) | hash inteiro com semente por quadro de filme (`kit/pelicula.js`) |
| Cena escura sai BRANCA no vídeo, mas a foto do fotos.sh sai certa | fundo pintado direto no `#st` (`#st{background:#0b0a12}`): o HyperFrames grava o palco por cima de branco | ponha o fundo numa camada própria: `<div style="position:absolute;inset:0;background:…">` como 1º filho do `#st` (aconteceu na oferta do tour cliente A, 16/10/2026) |
| Volume final 1 dB acima do alvo depois do limitador | `alimiter` do ffmpeg tem `level=1` por padrão: sobe o ganho sozinho até o teto | `alimiter=limit=0.89:level=disabled` sempre que o LUFS foi calculado antes (prospecção, 16/10/2026) |
| Cor do texto some no HyperFrames (sai a cor padrão clara), mas a foto do fotos.sh sai certa | cor herdada do `#st` não vale no render do HF | cor hex direto nos blocos de texto; confira quadros do .mp4, não só as fotos (prospecção, 16/10/2026) |
| Vídeo real dentro da cena | — | `<video src muted playsinline data-start data-duration data-track-index>` dentro do `#st`: o HyperFrames extrai e injeta os quadros; transform/clip-path/filter animam no `frame(t)`. O fotos.sh não mostra o vídeo: confira com `--previa` |
| Dono: "só piscou a tela do nada" na troca de título | troca por corte seco do fundo inteiro ou flash branco, sem movimento-guia | `troca()` no pico de um movimento, match cut de escala, máscara com objeto do nicho ou `goo`; conferir a tira de emenda (±10 quadros) no .mp4 (prospecção, 16/10/2026) |
| Dono: "cara de IA" em bolo, mapa, cachorro, planta | coisa orgânica ou real desenhada com formas geométricas em código | vídeo real/foto/3D fotográfico como base; vetor só anota (nivel 68) |
| Tarja sobre vídeo não cobre o que devia (boca no dentista) | posição fixa sobre um vídeo em que a pessoa se mexe | rastrear ou cortar o trecho; conferir quadro a quadro no .mp4 |
| Borda clara aparece no canto do vídeo durante blur/deslize/zoom inverso | invólucro do vídeo do mesmo tamanho da tela | invólucro maior que a tela pelo deslize + desfoque (≥ 220 px de sobra; zoom inverso ≥ 1/0,8) — prospecção v2, 16/10/2026 |
| `<video>` de cena escondida reaparece por cima (HyperFrames) | o HF força o vídeo visível no `data-start`, ignorando `visibility:hidden` do contêiner | esconder cena com `opacity:0` no contêiner (e/ou janela `data-start`/`data-duration` só do trecho); fundo aparece 2–3 quadros no fim do `data-duration` → estender a duração |
| Texto some ou volta no meio do plano só no .mp4 | `frame(t)` dependia do estado do quadro anterior; o HF grava em vários processos fora de ordem | cada quadro escreve o estado COMPLETO (função pura de t) |
| Sublinhado "à mão" vira risco sobre a palavra | posição medida com `getBoundingClientRect` durante a animação/na caixa inline (baixa) | medir sem transform e somar ~0,3 em do corpo; conferir no .mp4 em tamanho real; sem espaço até a linha de baixo, não sublinhar |
| Clipe de banco com expressão forçada (careta) no close final | escolha pela descrição, não pelo quadro | folha de quadros de todo clipe antes de usar; rosto em close só com expressão natural |
