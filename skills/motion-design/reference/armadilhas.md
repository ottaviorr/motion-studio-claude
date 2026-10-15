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
