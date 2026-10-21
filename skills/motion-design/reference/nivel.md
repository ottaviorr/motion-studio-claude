# Nível de acabamento (mínimo para entregar)

Construído ao longo de vários vídeos (anúncio → explicador → antes/depois → 3 vídeos de motions sobre gravação). Cada item veio de um vídeo que ficou melhor por causa dele ou de uma crítica do dono. Nunca entregue abaixo disto.

1. **Sincronia com a fala é o principal.** Uma cena = uma frase. Cada mudança cai numa palavra: `tempo da palavra − início do clipe`. Se a frase não tem nada visual, não force.
2. **Tela real sempre que existir** (app, painel, login, site). Fotografe com `scripts/fotos-telas.mjs`. Onde não houver acesso, réplica fiel feita a partir de prints, com **dados inventados**, e diga no guia o que é real e o que é ilustração.
3. **Fundo com significado, nunca fixo.** Cada cena tem um fundo que diz algo: a cor do cliente (identidade), cinza quando a identidade some, verde e amarelo para "Brasil", escuro e dourado para preço/oferta, claro para "o sistema de sempre". Degradê em malha que se mexe (`mesh`) + grão (`.grao`).
4. **Tipografia em camadas:** título pesado (`--m-titulo`) + **uma** palavra-chave em serif itálico (`--m-serif`) com cor + texto de interface (`--m-ui`). Títulos de uma linha.
5. **Movimento com intenção:** mola curta (`pop`), câmera que aproxima no ponto da fala (`cam`), holofote que escurece o resto (`spot`), revelação em círculo (`wipe`), 3D com `perspective` (camadas, notebooks, telas inclinadas), cursor que clica de verdade, adesivos (`.stk`) com a palavra-chave.
6. **Formato pela função:** deitado 1920×1080 (no Reels fica em cima do rosto) para explicar · em pé 1080×1920 tela cheia para revelação de marca, frase de impacto e oferta · transparente (`class="alfa"`, `.mov`) quando o rosto tem que continuar aparecendo — conteúdo só na lateral livre, conferido com `ROSTO=quadro.jpg`.
7. **Ler o texto como o espectador lê.** Sem duplo sentido (ex.: "IMPOSTO" num carimbo leu como "taxa"). Frase literal ganha de trocadilho.
8. **Números oficiais da marca** (`MARCA.regras`, site, tabela de preços). Nada de porcentagem ou promessa inventada.
9. **Dados reais nunca aparecem.** Prints e gravações de tela do cliente têm nomes e conversas reais → só referência.
10. **Conferência em duas etapas:** folha de fotos nos tempos das batidas (antes de gravar) e um quadro de CADA arquivo final + duração e tamanho (depois de gravar).
11. **Transição entre cenas com movimento, nunca fusão parada** (corrigido no estudo 3, 16/10/2026: fusão A→B com tela parada lê como "piscou"/IA; use zoom-through, match cut, máscara com objeto ou corte no movimento — nivel 69). [Antigo:] sobreponha ~0,5 s com `xfade` (deslize lateral entre telas do mesmo app; círculo/zoom em mudança de assunto). Cada clipe começa X/2 antes da frase e termina X/2 depois da seguinte.
12. **Tempo pela palavra, não pelo segundo.** Com voz pronta, cada animação usa `W('palavra')` (kit/marca-exemplo/marca.js) e o plano sai da transcrição (`kit/gerar-plano.py`). Trocar a voz = regerar o plano e regravar; o visual se ajusta sozinho.
13. **Ler a frase inteira antes de ilustrar a palavra.** A cena desenha o sentido da frase ("quem usa o sistema todo dia" é sobre quem atende, não suporte 7 dias). Nada na tela promete o que a fala não prometeu.
14. **O espectador se vê na tela.** Quando a promessa é "com a sua marca", mostre o produto padrão virando o dele: uma marca de exemplo neutra ("Sua Agência") com cor que contraste com a de quem vende, mudando item por item na fala.
15. **Quantidade sem número.** "Inúmeras aulas/clientes/modelos": muitos objetos reais + gerados no mesmo estilo, em movimento que acelera e câmera que se afasta, sem contador.
16. **Toda VSL sai com legenda .srt** gerada da transcrição (`kit/montar-final.py`): nomes corrigidos, palavras inventadas pelo Whisper fora, frases sem pedaço solto.
17. **Cena seguinte começa onde a anterior terminou** quando é o mesmo objeto (mesma janela, mesmo enquadramento): a transição vira continuidade (`fade`), não troca de assunto.
18. **Anúncio em pé = feito para quem assiste sem som.** Legenda palavra a palavra queimada no vídeo (a palavra falada acende; palavras-chave da oferta em cor), conteúdo só dentro da zona segura (y 230–1300 em 1080×1920, longe da coluna de botões da direita) e gancho visível no quadro 0, sem entrada a partir do preto. Confira cada cena com a legenda e a zona por cima (`kit/conferir.py`).
19. **Reaproveitar cena é bom, desde que retemporizada pela voz nova.** Troque `B(n)`/tempos fixos por `W('palavra')` e confira a frase: a cena antiga tem que desenhar o sentido da frase nova (troque o adesivo/título).
20. **Liga/desliga com palavras coladas:** quando duas batidas caem a menos de 1 s ("liga ou desliga"), a resposta de cada estado aparece até ~0,3 s depois da palavra, senão some antes de ser lida.
21. **Motion sai na resolução da entrega: 1920×1080 (ou 1080×1920) a 30 fps, taxa de bits alta** (regra do dono desde 13/10/2026; antes era 4K60). É o padrão do `hf.mjs` e do `gravar-todos.sh` (H.264 a 40 Mb/s). 60 fps ou 4K só quando o pedido disser (peça avulsa de portfólio ou anúncio). Texto pequeno de interface em réplica: SVG/HTML, nunca raster esticado.
22. **Capítulo e fechamento também são motion:** marcador discreto no começo de cada bloco (alfa, por cima, perto da câmera, com entrada e saída) e card de fechamento quando o vídeo termina "no ar".
23. **Câmera contínua e objeto que vira a próxima cena.** Em vez de trocar slide, a câmera segue ou um elemento da cena cresce e vira a cena seguinte; corte com velocidade casada (nada parado no ponto de corte). Ver `reference/inspiracao.md`.
24. **Tela de produto em camadas:** réplica dividida em regiões que animam com pequeno atraso (número resolve, gráfico desenha), nunca um print parado.
25. **Contenção:** um destaque de cor, no máximo 3–4 palavras por tela, um estilo de movimento por vídeo. Nada de partícula, glitch ou 3D girando "porque dá".
26. **Série de reels: uma direção de arte por peça.** Antes de produzir, um `ESTILOS.md` com paleta (fundo/tinta/UM destaque), 3 fontes, como o produto aparece e a linguagem de movimento de cada reel; vizinhos nunca repetem; a maioria em fundo CLARO (o dono achou escuro demais). O kit de telas é re-tematizado por CSS por reel (`rNN-estilo.css`). Ver `projetos/<projeto>/ESTILOS.md`.
27. **Reels narrados: a voz manda.** Cena principal = duração da voz + 0,3 s, cada troca numa palavra (`W`), fecho no estilo do reel depois da voz; música MEDIDA e posta 21 dB abaixo da voz (fala sempre clara — o dono reclamou de música alta), -14 LUFS, CBR 20 Mb/s (`kit/gerar_reel.py`).
28. **Vídeo sem voz anda na batida da música.** Meça a faixa (`kit/batidas.py`: BPM, grade, drops), escolha a trilha pela ESTRUTURA (intro → drop → cheio → pausa → drop 2) casada com o roteiro, escreva as cenas em batidas (`bt(n)`, compasso `BR`), corte só em início de compasso, ponha os drops nas viradas do roteiro e confira o bumbo do áudio final contra os cortes (±30 ms). Tempo da cena reescalado pelo BPM (`ritmo.js`) = trocar música sem reescrever cena.
29. **Talking head com motions de ênfase: a pessoa não vai e volta.** Serviços seguidos = um bloco só (a pessoa fica em cartão num canto e os motions trocam entre si); zoom lento contínuo nos trechos só de rosto; legenda presa embaixo da pessoa (cheia ou em cartão) para não cobrir o motion. (lição de um colaborador, out/2026)

## O nível dos motions do portfólio e do site do portfólio (10–15/10/2026, "foda pra crlh")
Fontes: `$PORTF` = `~/motion-studio/projetos/<projeto>`, `$SITE` = `<site-do-portfólio>` (seções em `app/src/secoes/`, `app/CONTRATO.md`). Receitas completas em `reference/tipografia-que-funciona.md` e `examples/motions-jr/`.

30. **Tipografia em 3 papéis fixos: Archivo variável (grito), Instrument Serif itálica (voz), JetBrains Mono (máquina).** Grito em wght 800–900, lh .8–.86, ls −.045 a −.06em. Voz em 400, lh 1, ls −.01em. Rótulo mono 500–700, CAIXA-ALTA, +.08em (+.28em no estilo cinema), nunca abaixo de 30 px. Fontes locais com `font-display:block`, carregadas antes do quadro 0. Nenhuma quarta fonte. (`$PORTF/02-filme-c/fonte/fontes.css`; `filme-a.html:126`)
31. **O grito é encaixado pela largura, não por tamanho fixo.** Meça com `Range` e encaixe em 87 % da largura no 9:16 (940 px → 148–278 px, 8–15 % da altura) e 84 % no 16:9 (1610 px → ~356 px, 33 % da altura); teto do site: min(90 % da largura, 44 % da altura). Número sozinho chega a 396–520 px (20–27 % da altura) com `tabular-nums`. (`filme-a.html:305–316`; `meia-noite.html:183–186`; `filme-b.html:29–31`; `$SITE/…/01-marca.js:205–214`)
32. **Palavra gigante + UMA palavrinha itálica.** A voz tem 0,2–0,6 do tamanho do grito (.2em presa acima e à esquerda, ou 80–104 px no reel), acima e à esquerda (Filme A: voz em y 540, grito em y 700) ou no lugar da palavra-chave com 1,12–1,16em. Entra junto ou depois do grito, nunca antes. (`$PORTF/styleframes/sf1.html`; `$SITE/…/01-marca.css .mc-k`)
33. **A largura da Archivo é gesto, não enfeite.** Condensado (wdth 62) = cinema, tensão, números; expandido (125) = marca e grito. Funcionaram: respiro 125 → 108 com escala 1 → 1,06 ao longo do ato; entrada 62 → 100 (0,5 s) ou 62 → 125 (0,8 s) em expo.out; saída para 62 com ls +.3em e fade em power2.in; onda letra a letra (fase −0,95 rad por letra) com o peso ao contrário (900 ↔ 320). Instrument Serif não tem eixo de largura: nunca anime `font-stretch` nela. (`$SITE/…/01-marca.js:230–267`; `05-corte.js:199–203`)
34. **Letras em comum viajam entre palavras seguidas** (quando B entra até 0,5 s depois de A começar a sair): pares pela maior subsequência comum (LCS); cada letra voa de A para B interpolando x, y, altura, wdth e cor, num arco de 5 % da altura para cima, power3.inOut no todo, power2.inOut por letra, 0,04 s entre letras; a original de A some na saída e a de B só aparece quando a viajante chega. (`$SITE/…/01-marca.js:298–347`)
35. **Entrada desacelera forte; saída é mais curta e acelera.** Entradas 0,32–0,75 s em expo.out/quint.out; saídas 0,25–0,4 s em ease-in cúbico, terminando ~0,2 s antes do corte. Letras sobem 112 % com 0,026 s entre elas; número sai de dentro de máscara (420 px em 0,75 s). Nada de quique na palavra gigante: overshoot (back 1,6–1,8) só em selo e chip pequeno. (`filme-b.html:314–319`; `filme-a.html:475, 493`)
36. **Platô de leitura medido, não sentido.** (Estudo 3: no platô, nada em loop "respirando" — chegou, parou; a referência medida de edição profissional tem zero microanimação. Peso do item 68–74 vence.) Cada ideia fica montada e PARADA no mínimo máx(1 s; 0,5 + 0,33 s × palavras). Referências: 1 palavra no reel a 121 BPM = 2 tempos = 0,99 s; especificação número + serif = 3,4 s (número parado ~2 s); título de abertura ~4,8 s; fecho 5 s. No platô só respiro (deriva lenta, luz), nada entrando ou saindo. Melhor cortar um ato do que acelerar todos. (`filme-b.html:76–78`; `$SITE/app/CONTRATO.md`)
37. **Corte na batida e no meio de um movimento.** Reel de lançamento: um plano a cada 2 tempos (~1 s a 120 BPM); keynote: a cada meio compasso ×3 (~3,4 s a 105 BPM); abertura de série: elementos por semicolcheia (0,176 s a 85 BPM) e título no drop. O corte cai no pico de velocidade (giro centrado no corte com ease-in-out de 1 tempo; objeto que "passa pela câmera" 1 tempo antes e 1 depois). Nunca corte com tudo parado. (`filme-a.html:168–171`; `filme-b.html:239–257`; `meia-noite.html:150–155`)
38. **Costura: o último quadro de A é o primeiro de B — nenhuma troca "do nada".** Vale: match cut de forma (o ponto do "Um." cresce até o tamanho do vidro do objeto); objeto que persiste; cor que invade por um gesto em 0,3–0,5 do ato (círculo que nasce da luz, lâmina inclinada 15 % na direção do movimento); saída de A sobreposta à entrada de B (recortes empurrados para a câmera, escala ×4,2 e desfoque 14 px em 0,6 s, enquanto o título chega). Corte seco: no máximo 1 por filme, e com intenção. (`filme-b.html:327–343`; `meia-noite.html:369–379`; `$SITE/…/01-marca.js:46–55, 271–296`)
39. **Câmera em trilho, não em saltos.** Poses viram pontos de controle de duas curvas CatmullRom centrípetas (posição e mira), no máximo 45° de azimute por trecho; o tempo entre poses segue o ease de cada trecho e o platô é parado de verdade (respiro de ±0,05 un.). Sem trilho, o mínimo é um empurrão contínuo por cena: +16 % em 4 s no escuro, +5–6 % no título. (`$SITE/…/01-marca.js:610–658`; `meia-noite.html:335–448`; `kit/objeto3d.js`)
40. **Desfoque de movimento de verdade em peça rápida** (`kit/desfoque.sh`): 2 passadas no HyperFrames (máximo 240 fps cada) defasadas meio subquadro → até 480 amostras/s. A 30 fps o padrão é 16 subquadros por quadro com obturador de 180°; o deslocamento por amostra fica em até ~1/3 da largura do objeto que corre (com 8 subquadros, 10 000 px/s mostrou "degraus"). Letra que vem de perto da câmera leva desfoque próprio de 26 → 0 px ao pousar (escala 6 → 1 em 0,46 s, expo.out). Peça calma (keynote) vai sem desfoque. (`$PORTF/01-filme-a/fonte/montar.sh`, que usou 60 fps e 270°; `meia-noite.html:397–413`)
41. **Objeto entre as letras.** Três camadas da mesma palavra: atrás inteira; na frente só as letras que o objeto não atravessa; e uma cópia de cor invertida recortada pelo contorno projetado do objeto (`clip-path: polygon` do fecho convexo, `O.proj` do `kit/objeto3d.js`). Letras perto do objeto pulam e voltam: −46 px × gaussiana de 230 px, amortecida em ~0,3 s. (`filme-a.html:87–91, 436–457`)
42. **Um destaque de cor, só no que conta**: limão só no saldo e no último quadro (Filme A); vermelho só no hífen-brasa, nos dois-pontos e no halo (MEIA-NOITE); laranja só no LED, nas cotas e no ponto do nome (Filme B). O resto é tinta + fundo; o fundo em cor plena pode trocar a cada corte (cobalto, laranja, creme, tinta). (`$PORTF/ESTILOS.md`)
43. **Styleframe aprovado antes de animar; cena escrita em batidas.** Um quadro-chave por peça em HTML (o dono aprova pela folha). A cena usa `kit/ritmo.js` com BPM medido na grade fina do trecho (`batidas.py --trecho`), batida 0 no tempo forte e drop numa batida conhecida: trocar a música = mudar BPM e início, sem reescrever a cena. (`$PORTF/styleframes/`; `$PORTF/musica/LICENCAS.md`)
44. **Som desenhado por peça, mixado por caráter** (`kit/som.py`): whoosh com o PICO (62–78 % da duração) no corte, riser e whoosh reverso TERMINAM no drop. Peça enérgica: trilha × 0,8 + efeitos 0,2–0,42 (impacto até 0,95); peça calma: trilha × 0,55 + efeitos × 0,42. Final em −14 LUFS, pico −1,5 dBTP. (`$PORTF/0*/fonte/som.py`, `montar.sh`)
45. **Película só onde o conceito pede** (`kit/pelicula.js`): semente pelo quadro de filme a 24 q/s, não pelo do vídeo. Referência MEIA-NOITE: grão α 0,42 em escala 1,5; riscos que vivem 0,6 s; até 4 partículas de poeira por quadro; flicker 0,025–0,095; oscilação ±2,2 px em x e ±1,6 px em y. Custa ~3× no render: grave o resto com ela desligada nas prévias.

## Motions de aula e de YouTube no nível do portfólio (aula SLA v2, 16/10/2026; pedido do dono)
46. **Vídeo editado também leva o nível do portfólio** (itens 30–45). Cards genéricos (chip arredondado, Inter, gradiente) pareceram "IA" ao lado do portfólio. Use a tipografia do portfólio: grito Archivo encaixado pela largura, voz em serif e rótulo em mono +.28em. Fundo em tinta, com a cor do ESTADO invadindo por um gesto (um círculo que nasce do objeto). Um objeto 3D que É o conceito da aula: na aula SLA, o cronômetro de metal cujo mostrador é a própria régua do SLA (verde, laranja, vermelho), com o ponteiro andando na palavra. O mesmo objeto atravessa a aula (abertura → régua → fechamento). Referência: `projetos/<projeto>/v1/fonte/motions2/` (`relogio3d.js`, `aula2.css`/`aula2.js` com `grito()`, `voz()`, `encaixa()`, `fundoSLA()`).
47. **Didático antes de bonito:** cada motion desenha UMA ideia da fala, de um jeito que se entenda sem som. Exemplos: "o tempo máximo é 20 minutos" vira o ponteiro parando no vermelho + 20:00 + MÁXIMO.; "duas automações" vira um gatilho com dois trilhos coloridos; "o lead segue no vácuo" vira um RESPONDIDO? fantasma riscado e NO VÁCUO.
48. **Encaixe pela largura na largura FINAL:** ponha o `font-stretch` final (ex.: 118 %) antes do `encaixa()`; medir em 100 e animar até 118 estoura a borda (aconteceu em todas as palavras da 1ª passada).
49. **Ambiente 3D sem three.js quando é diagrama:** um mundo em CSS 3D (`perspective`, `preserve-3d`, chão em grade com máscara) com câmera em trilho deixa o texto nítido e foi rápido de gravar. three.js fica para o objeto que precisa de metal e luz.
50. **Uma palavra gigante por vez e longe dos balões:** palavra fantasma atrás de conversa + risco atravessando a mensagem pareceu "bugado" ao dono. Zonas separadas (conversa em cima, grito embaixo) e o risco medido no tamanho da palavra (Range), na altura do meio das maiúsculas (~.47 do corpo com lh .84).

## Estudo de tipografia, hierarquia e 3D (out/2026 · `reference/estudo-tipografia-3d.md`, com links e 5 receitas)
51. **Fundo plano, sem halo.** Nada de brilho radial roxo/azul em quase-preto (sinal nº 1 de "visual de IA"; estava em 5 de 6 cenas da aula SLA v2). Fundo tinta ou osso PLANO + grão; luz colorida só como rebatimento de um objeto visível (raio ≤ 35 % da tela, alfa ≤ 0,25). A cor de estado entra PLENA por um gesto (o vermelho da régua = o melhor quadro).
52. **Conte os sinais de IA antes de gravar** (0–1 limpo · 2–3 corrigir · 4+ refazer): halo/gradiente roxo, texto com gradiente, cartão arredondado + ícone de traço no canto, pílula com "●", número gigante + rotulinho sem ser o conceito, mono como enfeite, glassmorphism, quique/elástico, tudo centralizado, Inter como voz, #000/#fff puros, partícula/glitch, ícone redondo repetido. Aula SLA v2 marcou 4.
53. **Mono só para máquina** (tempo, contagem, código, gatilho). Rótulo de seção: Archivo 600 caixa-alta +.06em, ou nada. **Voz = 1 a 3 palavras**; frase vai para a fala.
54. **Mesmo nível = mesmo tamanho** (lista de gritos no menor encaixe, alinhada à esquerda). **Espaço entre grupos ≥ 2× o de dentro.** **Cada pausa é um pôster** (folha no meio de cada platô; ≥ 96 px da borda; grade de 12 colunas: margem 96, calha 24, coluna 122).
55. **Três gestos de entrada no repertório** (máscara + largura; letras viajando entre palavras; chegada de perto da câmera com desfoque) — nunca o mesmo duas vezes seguidas, ≤ 50 % do mesmo gesto na peça. Depois de um gesto grande, 2–4 s só de micro-movimento.
56. **3D com três luzes + chão:** chave 30–45°, preenchimento ¼–½, contraluz (rim) 1,5–3× do lado oposto (pode levar a cor do estado), ambiente com faixas; sombra de contato (elipse desfocada, alfa .35–.55). Partes "impressas" do objeto em `MeshStandardMaterial`, nunca Basic. **Apagar = misturar com a cor do fundo** (lerp .6), nunca multiplicar (o laranja vira marrom). Bug da luz-chave do `kit/objeto3d.js` corrigido em 16/10/2026.
57. **Fechamento = um grito + o objeto no estado final + a marca.** Lista de resumo vai para a descrição/fala.
58. **Costura entre os motions de uma aula:** o objeto-conceito sai de um motion e entra no próximo no mesmo lugar e tamanho; velocidade casada no corte (pico no corte, desfoque 0→10→0 px em 0,3 s).
59. **Pelo menos 2 de cada 6 motions em fundo claro** (osso #f2eefa) — o dono prefere claro; a alternância também marca capítulo.
60. **Tela em cena e anotações** (pedido do dono, 16/10/2026): em aula/tutorial, a tela pode encolher para um cartão (0,75–0,84) com cards e elementos que saltam em volta, e anotações puxadas pela palavra (holofote, lupa, elemento que levanta, seta, passos). Regras e componentes em `edicao-video/references/tela-em-cena.md` e `anotacoes.md`.

## Segunda pesquisa: pop-ups, texto, gramática do editor, variedade (16/10/2026 · `edicao-video/references/{popups,texto-enfase,gramatica,variedade,overlays-kit}.md`)
61. **Nem tudo é motion em tela cheia.** Escada de intensidade: 0 nada/corte · 1 zoom · 2 anotação ou texto curto · 3 card/pop-up parcial ou câmera crescendo · 4 tela em cena ou dividida · 5 motion em tela cheia. O degrau acompanha o peso da ideia; degrau 5 ≤ ~1/min; depois de um degrau 4–5, a frase seguinte fica em 0–1. A aula SLA v2 usou só 3 recursos; o plano ideal da mesma aula usa 10.
62. **Escolha pela FUNÇÃO da frase** (definição, passo, valor, "esse aqui", aviso, comparação, opinião, prova, espera, capítulo…): mesma função = mesmo recurso no vídeo inteiro; a variedade vem das funções. Frase de ligação ("tá?", "então") = nada. Mapa em `fonte/mapa-recursos.md` antes dos motions.
63. **Pop-up é para o que NÃO está na tela** (dica, termo, caminho de menu, o que acontece fora: SMS chegando). O que está na tela = anotação. Entra 0,35–0,45 s (cubic-bezier(.05,.7,.1,1), 24–40 px), sai 0,2–0,25 s, ~4 s parado, 22–32 % da largura, canto oposto à câmera, 1 a cada 20–40 s, nunca dois ao mesmo tempo. Sem pílula com bolinha (o Capítulo e o SeloStatus atuais ainda têm — trocar).
64. **Texto de ênfase: 1–4 palavras, na palavra falada** (−0,15 a +0,1 s). Sobre a UI clara do CRM, texto claro com sombra é ilegível (1,3–1,7:1 medido); funcionam placa de tinta, papel osso com sombra dura ou marca-texto (15–16:1). 2–4 por minuto, ≥ 8 s entre eles; "text pop" estilo MrBeast no máximo 1 por vídeo.
65. **Variedade com memória:** ler `~/motion-studio/aprendizado/repertorio-usado.md` (janela: objeto 5 vídeos, assinatura 3, abertura 2, fundo 1…), 3 rotas A conservadora / B troca ≥ 3 eixos / C provocada (carta oblíqua + SCAMPER), 1 estreia por vídeo, critério Frescor na rubrica. A IA e o juiz de IA preferem o típico: sem essa etapa, tudo sai parecido.
66. **Som de UI = tempero:** pop/tick/notificação 12–18 dB abaixo da voz, 30–300 ms, só na entrada, ≤ 4/min, nunca em explicação técnica. Sintetizar (`kit/som.py`, funções novas propostas) ou CC0/Pixabay; do `@remotion/sfx` só os CC0 (whoosh, mouse-click, ui-switch, page-turn, whip, shutter-modern).

67. **Música de fundo em vídeo com fala: 30 dB abaixo da voz** (regra do dono, 16/10/2026; antes 25). `edicao-video/scripts/trilha.py --alvo 30` + `trilha_voz.py`. Em motion sem fala, a trilha manda (ver memória "música na batida").

## Estudo 3 (16/10/2026): o que separa motion de animador de "cara de IA"
Origem: o dono reprovou 8 das 14 amostras da prospecção. As 3 aprovadas tinham matéria real (fogo e chapa filmados, óculos 3D fotográfico, carro real) com corte na batida. Pesquisa em `~/motion-studio/pesquisa/<estudo>/` (GitHub, skills, fóruns, Ben Marriott, Daniel Schiffer, nichos). Kit novo: `kit/movimento.js`.

68. **Matéria real é obrigatória.** Cada peça tem vídeo real (Pexels), foto recortada ou 3D fotográfico como base. O vetor só anota por cima da matéria (cota, seta, marca-texto). Nunca vira o cenário inteiro. Proibido fazer em código algo orgânico ou que existe de verdade: bicho, rosto, comida, bolo, celular, planta baixa "de cartilha". Celular = vídeo de mão real com a tela composta por cima em perspectiva.
69. **Título nunca pisca.** Toda troca de título ou cena tem um movimento-guia e a troca cai no quadro mais rápido dele (`troca()`, ~15 quadros com `forte`). Outras formas aceitas:
    - match cut de escala ≤ 5% (`antesDoCorte`/`depoisDoCorte`);
    - objeto do nicho passando como máscara (tesoura, espátula, cabide);
    - morph `goo` entre palavras de tamanho parecido;
    - corte seco honesto na batida.

    Proibido: flash branco de tela inteira, fade A→B com a tela parada, trocar o fundo inteiro sem movimento. Fade só em momento lento e emocional. Cortar sempre no movimento, nunca no repouso.
70. **Curvas assimétricas da casa** (`sai`, `chega`, `parte`, `forte`, via `bz()`). Use uma curva-mestra por frase, copiada para todos os elementos dela. `eio` simétrico em título está proibido.
    - **Antecipação** (`antes()`) antes de todo movimento grande.
    - **Nada nasce de `scale(0)`.**
    - **Impacto:** `anel()` + `reage()` nos objetos secundários + `tensao()` antes do carimbo.
71. **Estrutura de anúncio de produto (Schiffer, 15 s):**
    - 0–1,5 s: plano forte já em movimento, com o nicho reconhecível sem texto (≥ 2 objetos do nicho);
    - 1,5–5 s: mãos usando o produto ou serviço;
    - 5–10 s: detalhe em câmera lenta;
    - 10–13 s: produto em destaque;
    - 13–15 s: congela, marca e chamada.

    Final segurado de 0,6 a 1,4 s. No máximo 3 transições com efeito por peça; o resto é corte no movimento.
72. **Acabamento único sobre footage + código:** o mesmo tratamento de cor em todos os clipes (filtro igual no contêiner), grão de 4–6% que muda a cada quadro, vinheta leve e `weave()` (≤ 3 px, 12 Hz, escala 101%). O que é "feito à mão" (rabisco, seta, carimbo) anda a 12 fps (`tq`), e o vídeo e o título a 30.
73. **Processo:** antes do código, escreva no NOTAS.md:
    - a matéria real da peça;
    - 3 alternativas para cada transição, com a escolhida;
    - os planos na estrutura do item 71.

    Faça o blocking de tudo antes de polir a primeira cena. Na conferência, monte a **tira de emenda**: ±10 quadros em volta de cada corte, olhando o .mp4, nunca só as fotos. É ali que aparece o "piscou". Máscara ou tarja sobre vídeo conferida quadro a quadro no .mp4: tem que cobrir o que promete cobrir.
74. **Nicho mostra o que o cliente compra lá** (ver `pesquisa/<estudo>/06-nichos.md`): farmácia = balcão, farmacêutico, prateleira, serviço (pressão); confeitaria = faca entrando e a fatia abrindo; salão = o depois revelado. Respeitar as regras legais: farmácia sem automedicação nem promoção de remédio; dentista sem procedimento sendo feito, sem preço e sem "grátis"; estética sem promessa de resultado. Com modelo de banco, a peça leva "imagens ilustrativas".
75. **Doutrinas do HyperFrames já instaladas (internas, não aparecem na lista):** `~/.claude/plugins/cache/hyperframes/hyperframes/0.8.140/.claude/skills/motion-doctrine/` e `cut-the-curve/`, além de `seam-craft/`. Ler antes de peça com muitas transições. Regras-chave:
    - troca de título = zoom-through (`kit/movimento.js zoomThrough`);
    - frase → frase = waterfall, palavra por palavra (opacidade de entrada começa em 0,35 no meio do caminho);
    - mesmo objeto mudando de estado = rack-focus, com o corte no pico do desfoque (8–12 px);
    - pausa de 0,3–0,75 s antes do clímax;
    - ~3 objetos na tela, uma peça nova a cada ~1 s;
    - recorte nunca seco (pluma + sombra);
    - vídeo dentro de card sempre andando e com a cor do filme.

    Resumo das 20 regras em `pesquisa/<estudo>/02-skills-motion.md`.

## Avaliação v2 (17/10/2026): matéria real sem virar receita
76. **Separar objeto de sistema gráfico.** Peça reprovada por "cara de IA": o OBJETO desenhado (bolo, bicho, celular, mapa de cartilha) sai e vira filmagem. O SISTEMA gráfico (letra, cota, carimbo, grade, cortina, agenda, sumário, calendário) FICA e passa a abraçar a filmagem. Jogar os dois fora foi o erro da v2 da prospecção: viraram "vídeo com legenda".
77. **Vídeo dentro do design, não design em cima do vídeo.** Ferramentas:
    - letra vazada com vídeo dentro;
    - janelas de uma grade;
    - colagem com sombra dura;
    - pincelada que revela;
    - célula de pôster;
    - título atrás do sujeito;
    - duotone ou retícula na cor da marca.

    Conferências:
    - o design ocupa ≥ 35% da área em pelo menos metade dos quadros;
    - vídeo em tela cheia com texto por cima em ≤ 40% da duração;
    - nada de vídeo em cartão arredondado com sombra suave.
78. **Série = vitrine de repertório.** Cada peça trava, no cartão, quatro coisas: a linguagem (3D · vídeo dentro do design · vídeo dominante com desenho em volta · só design e tipografia), a % de vídeo, o fechamento e o CTA. Nenhum vizinho repete linguagem nem fechamento. A % de vídeo varia (0–85%). O título não fica no mesmo lugar em mais de 2 planos seguidos nem em mais de 1/3 da série. A série inteira não usa "congela + painel sobe". O WhatsApp escrito aparece em no máximo 2–3 peças, e de formas diferentes.
79. **A letra atua:** ≥ 2 planos por peça em que letra e vídeo se tocam, e uma tela com a letra em ≥ 50% do quadro. A serif itálica vai dentro do grito. No máximo 3 níveis de texto, rótulo ≥ 30 px. Os 12 tratamentos estão em `pesquisa/<estudo>/02-tipografia.md`.
80. **Som didático e música viva:**
    - efeito sonoro diegético só na ação visível, sincronizado ±1 quadro (faca, tesoura, clique, carimbo);
    - whoosh 2–4 quadros antes do corte;
    - a trilha sobe no gancho, abaixa sob a voz (30 dB) e corta seco antes do drop;
    - a tipografia entra na batida.

    Kit em `<pasta-da-série>/moldes/base/sfx/` + `montar2.py`.

## Aprovado de verdade (17/10/2026): a receita do portfólio, com o piloto "Por dentro."
O dono reprovou v1, v2 e v3 da prospecção ("cara de IA", "só vídeo com texto", "muito propaganda"). Ele aprovou a peça feita pela receita dos motions do portfólio. Fonte: `reference/receita-jr.md`, `reference/licoes-refs-reels.md` e a régua em `<pasta-da-série>/moldes/02-celular/`.

81. **Partir da receita do portfólio, não de cardápio de anúncio:**
    - um objeto-herói desenhado com realismo fotográfico (PBR, ambiente feito em código, texturas ricas em canvas: placa com centenas de componentes, etiqueta impressa, metal escovado);
    - uma palavra ou número gigante por tela, uma linha em itálico e um rótulo mono;
    - fecho calmo, sem preço nem WhatsApp.

    Pedido dele: "deixa o celular ainda mais real e esses desenhos também".
82. **Som sintetizado gesto a gesto** (`midia/som.py` por peça) e **música nova escolhida a dedo**, com o ponto alto num momento da imagem. Efeito de biblioteca "não soa real", e música genérica ele "odeia". Nunca reaproveitar a trilha de outra peça.
83. **Lições das referências dele:**
    - a cena troca pelo movimento;
    - a câmera atua (inclina, empurra, mergulha);
    - número rola nítido e trava com tique; desfoque forte no número "parece bug";
    - frase entra palavra por palavra;
    - halo e profundidade.

    Disco girando: anéis de desfoque, nunca estroboscópio.
84. **Vídeo "top":** tipografia gigante com vídeo real dentro das letras, mais motion desenhado no HyperFrames, mais montagem no Remotion (transições, cortes na batida, texto que atravessa os cortes). Exemplos: academia "Só mais uma." e moda "lookbook de revista".
85. **Processo que funcionou:**
    - piloto de UMA peça;
    - o dono aprova;
    - a série segue em ondas de no máximo 2 agentes;
    - cada piloto é corrigido pelo próprio agente, com o contexto aberto;
    - comida, bicho e rosto entram sempre como vídeo real.
86. **Vídeo longo de YouTube com personagem (série de exemplo (canal), 18/10/2026).** O dono aprovou o ato 1 e pediu o resto assim. O que funcionou:
    - rig SVG do anfitrião, reutilizável (`projetos/<projeto>/base/personagem.js`: poses e expressões que se misturam, traço a 12 fps);
    - um mundo contínuo, com câmera virtual, balão que vira cena e morph; nada de slides;
    - cada pose e expressão presa à palavra da fala;
    - ≥ 4 elementos didáticos por ato além do personagem, e algo novo a cada 5–8 s;
    - produção em atos de ~1 min, cada um sem áudio, com a faixa de efeitos à parte;
    - um quadro neutro combinado nas emendas;
    - uma montagem só, com a voz inteira e a música contínua 30 dB abaixo.

    Conferir a tira das emendas: texto que já começa visível no quadro 0 do ato "aparece do nada".
87. **Efeito sonoro em vídeo narrado (YouTube): ~24 dB abaixo da voz e mais −6 dB enquanto a voz fala (ducking).** Em 15 dB, o dono reclamou que atrapalha a fala (série de exemplo (canal), 18/10/2026). O efeito volta no respiro sem fala. Isto vale para efeitos; a música continua a 30 dB.
