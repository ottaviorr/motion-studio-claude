# Cardápio de linguagens de vídeo curto [30]

Para que serve: **cada amostra de uma série mostra um TIPO de vídeo diferente**. O dono quer "mostrar bagagem independentemente do tema" (17/10/2026). Na v2 da prospecção a série tinha 14 fontes diferentes e uma linguagem só (vídeo em tela cheia + título no topo + "Chama no WhatsApp"). Por isso pareceu um molde trocando de cor.

**Linguagem ≠ estilo.** O **estilo** (`repertorio-estilos.md`, 32 estilos) define paleta, fontes e textura. A **linguagem** define outras coisas:
- a relação entre vídeo real e design (quem é palco, quem é recheio);
- o que a letra faz;
- a estrutura em segundos;
- o som.

Uma linguagem aceita vários estilos, e as fichas indicam quais combinam. O cartão de direção trava as duas: `linguagem: L07` + `estilo: 17`.

Origem: consolida os 20 tipos da internet (`pesquisa/<estudo>/07`), as 15 técnicas de mistura (`03`), os 12 tratamentos tipográficos (`02`), as 25 ideias do GitHub (`06`), a lente do gosto do dono (`05`) e os estilos já existentes. Onde dois desses eram a mesma coisa, viraram uma ficha só.

## Como usar

1. Leia a tabela-índice e risque o que a série já usou (`aprendizado/repertorio-usado.md`, tabela de linguagens).
2. Escolha pela **matéria do nicho**, não pelo efeito. A pergunta é: o que o cliente compra lá, e qual linguagem mostra isso melhor? A coluna "nichos" ajuda.
3. Copie para o cartão: código, % vídeo × design, assinatura sonora e o fechamento que combina (`fechamentos.md`).
4. **Regras de série:**
   - nenhum vizinho repete a linguagem;
   - nunca 3 peças seguidas na mesma família (V · V+ · M · D · 3D · F);
   - a % de vídeo cobre pelo menos de 0–20 % até 80–95 % na série;
   - cada família aparece pelo menos uma vez a cada 6 peças.

**Famílias** (o eixo que mais muda a cara da peça):
- **V** · vídeo manda (≥ 80 %), o design pontua.
- **V+** · vídeo dominante, com design desenhado em volta ou por cima e interagindo.
- **M** · mistura forte: o vídeo mora **dentro** do design (letra, janela, papel, página).
- **D** · design e tipografia mandam (≤ 25 % de vídeo, quase sempre dentro da letra ou da forma).
- **3D** · objeto 3D fotográfico é o herói.
- **F** · formato narrativo: a estrutura é a ideia (laboratório, processo, episódio).

**Ferramentas citadas nas fichas** (kit da motion-design, `~/.claude/skills/motion-design/kit/`):
- `movimento.js`: `troca`, `zoomThrough`, `anel`, `reage`, `tensao`, `weave`, `tq` (12 fps), `goo`, `wipeCurto` e as curvas `sai/chega/parte/forte`.
- `mistura.js` (em criação): letra-janela, janelas de grade, colagem com borda, lâmina, duotone.
- `analisar_musica.py`: gera `musica.json` com batidas, compassos, onsets, energia por quadro e seções (intro/sobe/drop/cheio/respiro/fim).
- `recortar.py`: alfa do sujeito (rembg/BiRefNet/MediaPipe) como PNG ou WebM.
- `objeto3d.js` (three.js r186, três luzes + chão).
- `pelicula.js`: grão, gate weave.
- matter.js: física 2D pré-simulada com passo fixo.
- `som.py` e o kit de sfx.

Tudo é determinístico (sem relógio, sem `Math.random()` solto).

**Som, regra geral** (vale para todas, `nivel.md` 80):
- efeito diegético só na ação visível, a ±1 quadro;
- whoosh 2–4 quadros antes do corte;
- riser termina no quadro do impacto;
- silêncio de 4–8 quadros antes do hit principal;
- música 30 dB abaixo da voz quando houver fala;
- a trilha tem curva: não fica a mesma faixa em loop com a mesma energia.

---

## Índice

| # | Linguagem | Família | Vídeo × design | Fechamentos que combinam |
|---|---|---|---|---|
| L01 | Palavra-janela (vídeo dentro da letra) | M | 45 / 55 | F06 carimbo, F12 letra abre a porta |
| L02 | Grade modular na batida | M | 50 / 50 | F13 pôster de células |
| L03 | Documento-palco (agenda, comanda, bula, calendário) | M | 35 / 65 | F01 caneta circula, F05 comanda, F09 bula |
| L04 | Página de revista física | M | 45 / 55 | F14 índice fecha |
| L05 | Colagem de papel e fita | M | 50 / 50 | F07 etiqueta pendurada, F06 carimbo |
| L06 | Flyer de xerox / lambe-lambe | D | 25 / 75 | F15 lambe colado no muro |
| L07 | Riso / duotone de 2 tintas | D | 20 / 80 | F13 pôster, F16 QR impresso |
| L08 | Rabisco vivo sobre vídeo | V+ | 70 / 30 | F11 notificação, F07 etiqueta |
| L09 | Prancheta técnica (cota que mede o real) | V+ | 65 / 35 | F08 trena |
| L10 | Texto atrás da pessoa | V+ | 80 / 20 | F17 nome no letreiro |
| L11 | Lâmina antes/depois | V+ | 75 / 25 | F18 reflexo vira logo |
| L12 | Rampa e congela | V | 90 / 10 | F18 o produto vira o logo |
| L13 | ASMR macro | V | 95 / 5 | F20 a palavra no vapor/na superfície |
| L14 | Filme de cinema (letterbox e créditos) | V+ | 80 / 20 | F04 créditos sobem |
| L15 | Legenda que sente | V+ | 30 / 70 (tipo protagonista) | F03 cartão de retorno, F09 bula |
| L16 | Tipografia com peso (física) | D | 20 / 80 | F02 ingresso destacável |
| L17 | O número é a imagem | D | 20 / 80 | F02 ingresso, F05 comanda |
| L18 | Corte seco tipográfico na batida | D | 30 / 70 | F06 carimbo |
| L19 | Letras-personagem (identidade cinética) | D | 15 / 85 | F12 letra abre a porta |
| L20 | Objeto 3D herói (branco de estúdio, cotas) | 3D | 0–20 / 80 | F18 objeto vira logo |
| L21 | Vista explodida | 3D | 20 / 80 | F19 remonta e acende |
| L22 | FOOH na fachada | 3D | 85 / 15 (3D dentro da rua) | F17 letreiro da loja |
| L23 | Lente de vidro / lupa | 3D | 50 / 50 | F17 o endereço entra em foco |
| L24 | Tela réplica: resolve em 3 toques | M | 55 / 45 | F11 notificação, F10 botão |
| L25 | Laboratório: verdade ou mito | F | 50 / 50 | F06 carimbo de veredito |
| L26 | Do material ao produto (process film) | F | 80 / 20 | F08 trena, F13 pôster |
| L27 | Stop-motion de bancada | F | 70 / 30 | F07 caixa fecha com etiqueta |
| L28 | Matéria digital (dither, ASCII, pixel sort que acende) | V+ | 70 / 30 | F19 remonta e acende |
| L29 | Matéria simulada (tecido, goo, tinta) | D | 20 / 80 | F20 a marca escrita na matéria |
| L30 | Humor de série (objeto fala / episódio absurdo) | F | 80 / 20 | F20 sem CTA, só a marca |

Contagem: M 6 · D 7 · V 2 · V+ 7 · 3D 4 · F 4. As que já foram aprovadas pelo dono: L01 (Hamburgueria (exemplo)), L20 + L23 (Ótica (exemplo)), L11 (Estética automotiva (exemplo)), L14 (barbearia v1, cinema).

---

## Fichas

### L01 · Palavra-janela (vídeo dentro da letra)
- **Assinatura:** uma palavra gigante em cor plena "fura" o fundo e o vídeo do nicho passa por dentro das letras. Depois a letra cresce até virar a tela inteira (a letra é a transição).
- **Vídeo × design:** 45 / 55. O vídeo é o recheio e a cor plena é o palco.
- **Tipografia:** grito pesado e largo (Anton, Archivo 800 wdth 125) encaixado em 940 px, até esticado 2× na altura. Uma palavra literal ("BRASA", "CAMADAS", "NAVALHA"). Tratamentos 1 e 4 de `02-tipografia`.
- **Som:** efeitos = o som do que está dentro da letra (chapa chiando, faca no bolo, navalha) + baque grave quando a letra cresce + carimbo no preço. Trilha: entra cheia no quadro 0, abre um respiro quando a letra vira tela, volta no drop do fecho.
- **Estrutura (12 s):** 0–1,5 palavra-janela · 1,5–5 a letra abre e vira plano · 5–9 janelas de borda áspera com 2–3 planos · 9–12 fecho.
- **Nichos:** ✓ hamburgueria, confeitaria · ✗ dentista (não pode mostrar procedimento, e boca dentro da letra fica estranho).
- **Kit:** `mistura.js` (letra-janela, `<mask>` com `<text>`), `troca`/`zoomThrough`, `analisar_musica.py` (crescimento no compasso).
- **Referência:** nossa 11 Hamburgueria (exemplo) (`<pasta-da-série>/moldes/entrega/11-hamburgueria.mp4`, nota 8,5) · Spotify Wrapped 2024, "type as form" ([D&AD](https://dandad.org/awards/professional/2024/238334/wrapped-design)).
- **Estilos:** 5, 30, 11.
- **Risco de IA:** médio. Fonte fina ou palavra longa vira textura sem leitura. Evitar: palavra de ≤ 7 letras, peso ≥ 800, vídeo com movimento forte e contraste dentro da letra; borda áspera (turbulência) nas janelas, nunca cartão arredondado.

### L02 · Grade modular na batida
- **Assinatura:** a tela é uma grade suíça (2×3 → 3×4 → 1). Cada célula é um vídeo ou um bloco de tipo, e a grade se reorganiza no compasso como página de revista viva.
- **Vídeo × design:** 50 / 50. A grade é o desenho.
- **Tipografia:** grotesca em coluna, números de célula em mono ≥ 30 px, uma célula vira palavra gigante. Tratamento 2: cada letra de "LOOKS" é uma janela com um look diferente.
- **Som:** efeitos = caixa (snare) a cada reorganização, clique seco de régua nos fios, tecido/cabide na troca de look. Trilha: funk ou breakbeat que muda de padrão a cada 4 compassos, e a grade muda junto. Corte para o bumbo sozinho no respiro.
- **Estrutura (14 s):** 0–1 grade cheia já mexendo · 1–6 duas reorganizações · 6–10 uma célula cresce até a tela (match de escala) · 10–14 pôster final.
- **Nichos:** ✓ loja de roupa, academia (modalidades) · ✗ farmácia (vira catálogo frio).
- **Kit:** `mistura.js` (janelas `clip-path: inset()` em stagger de 3–6 quadros), `analisar_musica.py` (compassos e seções), `wipeCurto`.
- **Referência:** Videobolt "modular layouts" ([blog](https://blog.videobolt.net/post/top-motion-graphics-trends-2026)) · grade de 12 colunas do nível 54.
- **Estilos:** 1, 2, 26.
- **Risco de IA:** alto se as células tiverem cantos arredondados e sombra (vira dashboard). Evitar: fio reto de 2 px, calha fixa de 24 px, sem raio, sem sombra.

### L03 · Documento-palco (agenda, comanda, bula, calendário, recibo)
- **Assinatura:** o documento do nicho ocupa a tela inteira e é o layout. Cada linha riscada ou dobra aberta mostra um vídeo no vão. O único espaço livre cresce e vira a mensagem.
- **Vídeo × design:** 35 / 65. O vídeo mora nos vãos e nas linhas.
- **Tipografia:** o próprio documento: horários em mono 64–80 px, nomes em serif ou manuscrita, o horário livre encaixado em 940 px com vídeo dentro. Tratamentos 3 e 12.
- **Som:** efeitos = caneta riscando (um risco por batida), papel dobrando/desdobrando, impressora térmica, grampeador. Trilha: pulso leve que acelera conforme a agenda enche, para seco no último horário livre (2 batidas de silêncio) e volta macia no fecho.
- **Estrutura (15 s):** 0–2 documento cheio, primeiro risco · 2–9 cada linha abre um vídeo do serviço · 9–12 só sobra uma linha · 12–15 caneta circula (fecho).
- **Nichos:** ✓ salão (agenda do dia), farmácia (bula que se desdobra, sem nome de remédio) · ✗ automotivo (o documento não é o que o cliente compra).
- **Kit:** `movimento.js` (`tq` 12 fps no risco), `mistura.js` (janelas nos vãos), `getBoundingClientRect` das linhas para posicionar os vídeos.
- **Referência:** v1 do salão (agenda que enche, que o dono elogiou o conceito) + v2 da farmácia (etiqueta de bula) · Spotify Wrapped 2025, flyer DIY ([Creative Review](https://www.creativereview.co.uk/spotify-wrapped-2025-film-lewis-capaldi-jade-pinkpanthress/)).
- **Estilos:** 16, 17, 23.
- **Risco de IA:** alto se o papel for branco liso com sombra suave (vira card de UI). Evitar: fibra do papel em multiply 15–25 %, curvatura, sombra dura, traço a 12 fps com *boil*.

### L04 · Página de revista física
- **Assinatura:** uma revista de papel com luz e lombada. As "fotos" são vídeos e a página vira no gesto filmado (a modelo girando, a mão passando).
- **Vídeo × design:** 45 / 55.
- **Tipografia:** editorial: Didot ou Fraunces itálica **dentro** do grito (tratamento 11), fólio, "p. 12", sumário cujas linhas abrem vídeos (tratamento 3).
- **Som:** efeitos = folha virando (papel encorpado, não whoosh), caneta tinteiro no sumário, clique de câmera no "flash" da foto. Trilha: house elegante a 118–124 bpm que abaixa um filtro (passa-baixa) quando a página vira e abre na nova.
- **Estrutura (16 s, lenta):** 0–2 capa com vídeo na foto · 2–8 duas viradas · 8–13 sumário com janelas · 13–16 índice fecha.
- **Nichos:** ✓ estética (protocolo como matéria de revista), moda (lookbook) · ✗ academia (energia errada).
- **Kit:** `mistura.js` (página com vídeo), CSS 3D `rotateY` com sombra que corre na dobra (12–15 quadros), `pelicula.js` só se o estilo pedir grão.
- **Referência:** v1 da estética (sumário) e da moda (revista virando) · Buck, Pinterest "It's Possible" ([Buck](https://BUCK.co/work/pinterest-it-s-possible)).
- **Estilos:** 3, 24.
- **Risco de IA:** médio. Na v1 o papel era liso e as fotos eram selos pequenos. Evitar: foto ocupando a página, papel com luz, curva e textura; nada de serif itálica como "sobrescrito pequeno" (tique da v2).

### L05 · Colagem de papel e fita
- **Assinatura:** o sujeito real recortado com borda branca fibrosa, sombra dura e rotação de ±3°, preso com fita crepe numa superfície de cor ou kraft. Tudo entra a 12 fps com um tranco de 2 quadros.
- **Vídeo × design:** 50 / 50.
- **Tipografia:** recortada de revista (letras de fontes diferentes só no título), apoio em grotesca limpa para contrastar, preço escrito à mão.
- **Som:** efeitos = fita sendo puxada e colada, tesoura cortando papel, papel amassando na saída. Trilha: indie/ukulele seco com palmas, um corte a cada colagem, e a trilha para enquanto a fita "estala" no fecho.
- **Estrutura (13 s):** 0–1 primeiro recorte colado · 1–8 3–4 recortes em camadas, cada um com um vídeo · 8–13 etiqueta pendurada (fecho).
- **Nichos:** ✓ pet (bicho recortado entrando na conversa), salão (polaroids da agenda) · ✗ odonto (fica infantil para clínica).
- **Kit:** `recortar.py` (alfa do sujeito), `mistura.js` (borda fibrosa `feMorphology` + `feTurbulence`), `tq`. Para vinheta de 5–30 s em 16:9, a skill **paper-collage-film**.
- **Referência:** Graphic Design Junction 2026, colagem mixed media ([GDJ](https://graphicdesignjunction.com/2026/01/video-and-motion-creative-trends-2026/)) · Buck/Pinterest.
- **Estilos:** 17, 29, 10.
- **Risco de IA:** alto quando o recorte é liso e a sombra difusa (sticker de IA). Evitar: borda com fibra, sombra dura e deslocada, 12 fps, nada de bicho desenhado (D1).

### L06 · Flyer de xerox / lambe-lambe
- **Assinatura:** um cartaz de rua fotocopiado em P&B + uma cor, com retícula grossa e fita. O vídeo real é "impresso" (filtro de xerox) e preso no papel. A data e o preço aparecem em letreiro de lambe.
- **Vídeo × design:** 25 / 75.
- **Tipografia:** condensada pesada carimbada (Anton, Bebas), tinta falhada, letras desalinhadas por registro. Uma palavra por cartaz.
- **Som:** efeitos = luz da xerox passando (zumbido + clique), grampeador, rolo de cola no muro. Trilha: boom-bap com chiado de vinil e um scratch como transição.
- **Estrutura (12 s):** 0–1 a xerox "imprime" o primeiro quadro · 1–8 três cartazes empilhando · 8–12 o lambe é colado no muro real (fecho).
- **Nichos:** ✓ barbearia, hamburgueria (smash night) · ✗ estética (a sujeira contradiz o cuidado).
- **Kit:** `mistura.js` (duotone/retícula), shader de retícula por canvas, `tq`, `weave`.
- **Referência:** Spotify Wrapped 2025 ([Creative Review](https://www.creativereview.co.uk/spotify-wrapped-2025-film-lewis-capaldi-jade-pinkpanthress/)) · GDJ "grunge street opener".
- **Estilos:** 10, 6.
- **Risco de IA:** médio. O grunge "preset" (manchas iguais, texturas de banco aplicadas por cima de tudo) denuncia. Evitar: textura só no papel, não no vídeo inteiro; retícula com pontos de 6–10 px coerentes com a escala.

### L07 · Riso / duotone de 2 tintas
- **Assinatura:** tudo impresso em duas tintas fluorescentes (rosa + azul, laranja + verde), com registro desalinhado e grão. O vídeo vira duotone e as tintas se sobrepõem formando a terceira cor.
- **Vídeo × design:** 20 / 80 (o vídeo é matéria impressa, não cena).
- **Tipografia:** grotesca larga ou serif de cartaz em uma tinta, a sombra da outra tinta deslocada de 3–6 px.
- **Som:** efeitos = rolo da duplicadora riso, papel saindo da bandeja, um "tum" de tinta a cada camada. Trilha: lo-fi com bateria seca; a segunda tinta entra quando a trilha dobra de instrumentos.
- **Estrutura (14 s):** 0–2 só a primeira tinta · 2–6 a segunda entra e forma a imagem · 6–11 três "páginas" · 11–14 pôster com QR impresso.
- **Nichos:** ✓ café/padaria (cardápio), academia (grade de horários) · ✗ farmácia (cor fluorescente em saúde soa promoção).
- **Kit:** `mistura.js` (duotone `feColorMatrix` + `feComponentTransfer`), grão de riso (shader MIT), `analisar_musica.py` (camadas na seção "sobe").
- **Referência:** [sevenevesai/riso-windowseat](https://github.com/sevenevesai/riso-windowseat) (filmes inteiros em riso, MIT) · [Robpayot/risograph-grain-shader](https://github.com/Robpayot/risograph-grain-shader).
- **Estilos:** 9.
- **Risco de IA:** médio. Duotone em tudo vira filtro de app. Evitar: o registro desalinhado é a assinatura; a paleta tem só 2 tintas de verdade (sem gradiente); nada de pastel.

### L08 · Rabisco vivo sobre vídeo
- **Assinatura:** um vídeo real e, por cima, um traço tremido feito à mão que segue o sujeito (coroa no cachorro, bolhas, setas, "cheiroso!"). A linha "ferve" a 12 fps.
- **Vídeo × design:** 70 / 30 (o traço ocupa ≥ 25 % da área em metade do tempo).
- **Tipografia:** manuscrita só nas palavras do rabisco; um grito em grotesca no início e no fim. Nada de manuscrita no corpo.
- **Som:** efeitos = giz ou caneta a cada traço, "plop" de bolha com altura variando, borracha no apagar. Trilha: assobio ou ukulele alegre que dá um "respiro" (só percussão) quando o traço desenha a palavra principal.
- **Estrutura (12 s):** 0–1 primeiro traço já aparecendo sobre o vídeo · 1–9 três ações, cada uma com seu rabisco · 9–12 o traço escreve a marca.
- **Nichos:** ✓ pet, confeitaria (chamadas da fatia real em glacê) · ✗ farmácia (rabisco sobre medicamento pode parecer indicação).
- **Kit:** `tq`, `feTurbulence` com semente `floor(t*12)`, keyframes do sujeito a cada 6 quadros (Catmull-Rom) ou trilha do OpenCV, [rough-notation](https://github.com/rough-stuff/rough-notation) como referência.
- **Referência:** Ben Marriott, frame a frame sobre o motion-base ([Motion Design School](https://motiondesign.school/courses/motion-practice-with-ben-marriott)).
- **Estilos:** 16, 25.
- **Risco de IA:** alto quando a linha é perfeita, parada ou desgruda do objeto. Evitar: rastreio de verdade (ou plano parado), ponta de seta desenhada, *boil* de 2 px, coraçõezinhos no máximo 1.

### L09 · Prancheta técnica (cota que mede o real)
- **Assinatura:** linhas de cota de arquiteto se estendem sobre o objeto filmado e o número sai de dentro do fio. A palavra tem a largura exata do que mede.
- **Vídeo × design:** 65 / 35.
- **Tipografia:** mono só nos números (é máquina), grotesca condensada no grito, a "palavra que mede" (tratamento 8): "2,10 m" de ponta a ponta do sofá.
- **Som:** efeitos = trena estendendo e travando, clique de lapiseira, "tic" no traço de ponta da cota. Trilha: minimal eletrônica com tique de metrônomo, que sobe um semitom a cada medida e para seca na cota final.
- **Estrutura (14 s):** 0–1,5 o objeto real e a primeira cota nascendo · 1,5–9 três medidas · 9–11 a planta desenhada por cima a 12 fps se ergue (variação "mapinha": planta → sala real por match cut) · 11–14 trena recolhe.
- **Nichos:** ✓ móveis, ótica (ponte e haste) · ✗ hamburgueria (medir comida tira o apetite).
- **Kit:** `anel` nos traços de ponta, `troca`, `encaixa()` com a largura medida no quadro, `objeto3d.js` se a planta subir em 3D com material fotográfico.
- **Referência:** Filme B (cotas que viram número, ★★★) · Stash 2025, "do material ao produto" ([Stash](https://www.stashmedia.tv/best-of-stash-2025-brand-films/)).
- **Estilos:** 13, 32.
- **Risco de IA:** alto se a cota flutuar sem objeto ou se a planta for vetor chapado de cartilha (reprovado). Evitar: a cota sempre medindo algo filmado; planta só como traço sobre foto real.

### L10 · Texto atrás da pessoa
- **Assinatura:** a palavra gigante passa entre o fundo e o sujeito filmado, cortada pelo corpo. Troca uma vez por look ou por passo.
- **Vídeo × design:** 80 / 20 (o design está dentro da cena).
- **Tipografia:** grito de largura total (Archivo Black, Big Shoulders), uma palavra, no terço de cima por trás da cabeça. Pode ser em toro 3D girando atrás (variação academia).
- **Som:** efeitos = whoosh de tecido na troca de palavra, salto alto ou passo no tempo, secador/tesoura (salão). Trilha: house de passarela a 124 bpm, corte a cada 2 compassos, filtro abre quando a pessoa chega perto da câmera.
- **Estrutura (12 s):** 0–1 a pessoa já andando, a palavra atrás · 1–9 três trocas · 9–12 a última palavra é o nome da loja.
- **Nichos:** ✓ moda, salão (cor nova só no cabelo, pela máscara de cabelo) · ✗ odonto (rosto de paciente + promessa).
- **Kit:** `recortar.py` (MediaPipe selfie/multiclasse ou SAM2, WebM com alfa), três camadas (vídeo → título → sujeito), `troca`.
- **Referência:** [Adobe, roto do sujeito](https://www.adobe.com/learn/after-effects/web/rotoscope-subject) · [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) · [codrops-kinetic-typo](https://github.com/marioecg/codrops-kinetic-typo) (toro).
- **Estilos:** 5, 30, 31.
- **Risco de IA:** médio. Fosco ruim no cabelo denuncia na hora. Evitar: plano com fundo limpo e contorno firme; conferir a máscara quadro a quadro no .mp4.

### L11 · Lâmina antes/depois
- **Assinatura:** uma lâmina reta ou inclinada (15°) divide a tela: cor chapada da marca + título de um lado, vídeo do outro. A lâmina anda com um movimento filmado (o pano, a porta) e troca o ANTES pelo DEPOIS.
- **Vídeo × design:** 75 / 25.
- **Tipografia:** grotesca pesada itálica, ANTES/DEPOIS ganhando cor quando a lâmina passa; contador mono subindo com o resultado.
- **Som:** efeitos = pano ou rodo passando (o som da lâmina é o do objeto que limpa), contador digital clicando, "brilho" curto no fim. Trilha: synth com pulso que segura um riser durante a lâmina e cai no drop no DEPOIS.
- **Estrutura (13 s):** 0–1 metade suja, metade limpa · 1–8 duas passadas da lâmina · 8–10 contador trava · 10–13 o reflexo vira logo.
- **Nichos:** ✓ estética automotiva, limpeza/lavanderia · ✗ estética facial (antes/depois de rosto = promessa de resultado).
- **Kit:** `mistura.js` (lâmina `clip-path: polygon()`), `troca` no pico de velocidade, `analisar_musica.py` (drop).
- **Referência:** nossa 10 Estética automotiva (exemplo) (aprovada, 7,5).
- **Estilos:** 30, 19.
- **Risco de IA:** médio. Bloco diagonal varrendo em todo corte é preset. Evitar: no máximo 2 lâminas por peça, sempre motivadas por um gesto filmado.

### L12 · Rampa e congela
- **Assinatura:** um plano real em câmera lenta acelera, **trava num quadro**, e o texto entra no vazio do congelamento. Repete 3 vezes e solta.
- **Vídeo × design:** 90 / 10. O tipo só vive nos congelamentos.
- **Tipografia:** uma palavra curta por congelamento, encaixada no espaço negativo do quadro (não no topo fixo), entrando no hit.
- **Som:** efeitos = riser na aceleração, tape stop no congelamento, a palavra cai num hit seco; o som do objeto (espuma, água) volta quando solta. Trilha: trap cinematográfica com um drop por congelamento e silêncio de 6 quadros antes do último.
- **Estrutura (12 s):** 0–1 o plano em movimento · 1–4, 4–7, 7–10 três rampas + congelamento · 10–12 solta e fecha.
- **Nichos:** ✓ automotivo, academia · ✗ farmácia (velocidade e trap não combinam com cuidado).
- **Kit:** curva de tempo em `video.currentTime` (rampa com `forte`), `analisar_musica.py` (drops), `troca`.
- **Referência:** Daniel Schiffer, speed ramp + freeze ([LensVid](https://lensvid.com/technique/shooting-a-professional-looking-product-commercial-at-home/)).
- **Estilos:** 19, 31.
- **Risco de IA:** baixo de "cara de IA", alto de "molde". O "congela + painel sobe" da v2 foi o vício da série. Aqui o congelamento é ritmo, não fecho: **nunca** fechar com congela + painel.

### L13 · ASMR macro
- **Assinatura:** close extremo e lento do serviço (máscara espalhando, gota caindo, fatia abrindo). Quase sem texto: uma palavra pequena e elegante por vez.
- **Vídeo × design:** 95 / 5.
- **Tipografia:** serif fina ou grotesca leve pequena (o oposto do grito), rótulo mono ≥ 30 px. A marca no fim, grande.
- **Som:** efeitos = o som é o produto, de perto e com reverb seco (creme, borrifo, tecido, faca no bolo). Trilha: pad muito baixo ou nenhuma; a única "batida" é o som do objeto.
- **Estrutura (15 s, lenta):** 0–1,5 o macro já em ação · 1,5–12 três texturas, 4 s cada · 12–15 a palavra pousa na superfície.
- **Nichos:** ✓ estética/spa, confeitaria · ✗ pet (macro de bicho é aflitivo).
- **Kit:** só vídeo + `pelicula.js` leve; `som.py` para mixar o close-mic.
- **Referência:** ASMR de comida ([The Grocer](https://www.thegrocer.co.uk/analysis-and-features/asmr-how-brands-are-selling-the-sound-of-food/595431.article)).
- **Estilos:** 25, 18.
- **Risco de IA:** baixo de IA, mas é a linguagem que mais "tira a essência de desenhar" (crítica de 17/10). Use no máximo 1 a cada 6 peças, e leve pelo menos 1 gesto tipográfico que toque o vídeo (a palavra escrita no vapor, na espuma).

### L14 · Filme de cinema (letterbox e créditos)
- **Assinatura:** letterbox 2,39:1 dentro do 9:16, moldura de película (timecode, "CENA 03", 35 MM) e créditos de filme que sobem no fim ("elenco: corte · barba · navalha").
- **Vídeo × design:** 80 / 20.
- **Tipografia:** título de cinema (serif condensada ou grotesca espaçada), créditos em duas colunas, rótulos de película em mono. Variação apresentador: Didot itálico na palavra-chave (editorial de arquivo).
- **Som:** efeitos = projetor rodando, a ponta de filme, clique de claquete, a navalha/tesoura em close. Trilha: tema de cinema (cordas ou sintetizador de suspense) que cresce até o título e fica só no pad sob os créditos.
- **Estrutura (16 s):** 0–2 contagem ou claquete · 2–11 três "cenas" numeradas · 11–16 créditos sobem e o último é a marca.
- **Nichos:** ✓ barbearia, hamburgueria premium · ✗ farmácia.
- **Kit:** `pelicula.js` (grão, weave), `movimento.js` (`weave`), skill **editorial-film-edit** quando houver apresentador.
- **Referência:** barbearia v1 (o dono sentiu falta da "cara de filme" na v2) · Filme C MEIA-NOITE (estilo 31, ★★★).
- **Estilos:** 28, 31, 4.
- **Risco de IA:** médio. Barras pretas + LUT laranja-azulado é o "cinematic" de preset. Evitar: cor do filme própria da marca, créditos com texto real do serviço, timecode que corre de verdade.

### L15 · Legenda que sente
- **Assinatura:** o vídeo é calmo (o dono falando, mãos trabalhando) e a legenda é a imagem: a palavra forte engorda e cresce, a palavra baixa encolhe, e cada voz tem uma cor.
- **Vídeo × design:** 30 / 70 de atenção. O vídeo ocupa a tela, mas o tipo é o protagonista.
- **Tipografia:** fonte variável (Roboto Flex, Recursive) com `wght` 300→900 guiado pelo volume de cada palavra; 2–4 palavras por vez, no centro, nunca na faixa de baixo.
- **Som:** efeitos = um tique suave sob cada palavra-chave, respiração mantida (não cortar), um "papel" baixinho na troca de frase. Trilha: pad baixo com ducking pesado (30 dB sob a voz) e um único respiro antes da frase final.
- **Estrutura (15–20 s):** 0–2 a frase-gancho na voz · 2–15 a história curta · últimos 3 s fecho falado e escrito.
- **Nichos:** ✓ dentista (o paciente que tinha medo, sem procedimento), farmácia (orientação do farmacêutico) · ✗ hamburgueria sem voz.
- **Kit:** `palavras.json` (transcrever.py) + RMS por palavra → `font-variation-settings`; `legenda.js` como base; `analisar_musica.py` não precisa.
- **Referência:** Caption with Intention, Grand Prix Cannes 2025 ([LBB](https://lbbonline.com/news/behind-the-oscar-winning-caption-revolution)). O oposto (mecânico): Hormozi ([análise](https://www.choppity.com/tools/recreate-video-editing-style/alex-hormozi/)).
- **Estilos:** 3, 22.
- **Risco de IA:** alto se virar legenda "karaoke" amarela de 2 palavras (o padrão de todo app). Evitar: o peso e o tamanho seguem a voz de verdade, não toda palavra; legenda corrida só se o dono pedir.

### L16 · Tipografia com peso (física)
- **Assinatura:** as palavras caem do alto como objetos (anilhas, produtos na cesta), quicam pouco, empilham, e a última amassa as anteriores.
- **Vídeo × design:** 20 / 80. O fundo é um vídeo escurecido ou cor plena.
- **Tipografia:** grotesca pesada e condensada (Anton, Archivo 900), cada palavra é um corpo rígido com massa; números entram como placas.
- **Som:** efeitos = o som do objeto que a letra imita (anilha batendo no chão = metal + grave; produto na cesta = plástico), rangido quando a pilha cede. Trilha: phonk/trap pesada, cada queda num kick, silêncio de 6 quadros antes da última palavra.
- **Estrutura (10 s, rápida):** 0–1 primeira palavra cai · 1–7 pilha de 4–6 palavras · 7–8 a pesada amassa · 8–10 o ingresso é destacado.
- **Nichos:** ✓ academia, mercado/hortifruti · ✗ estética (peso e queda = agressivo).
- **Kit:** matter.js pré-simulado (`Engine.update(e, 1000/60)` fixo, semente fixa, `pos[frame]`), `reage`, `analisar_musica.py` (kicks).
- **Referência:** Mat Voyce, "Think Different" ([Abduzeedo](https://www.abduzeedo.com/mat-voyces-think-different-kinetic-typography-mass)) · [liabru/matter-js](https://github.com/liabru/matter-js).
- **Estilos:** 5, 6.
- **Risco de IA:** médio. Quique elástico de "bounce" é o vício número um (a motion-doctrine proíbe). Evitar: restituição ≤ 0,3, a queda pesa (cai rápido, para seco).

### L17 · O número é a imagem
- **Assinatura:** cor chapada inteira e um número de 600–900 px que vira forma (o 0 vira o farol, o 1 vira a régua), extrudado em camadas, com o vídeo real visto pelo vão.
- **Vídeo × design:** 20 / 80.
- **Tipografia:** Archivo 900 wdth 62 no número, dígitos rolando como placar, centavos em itálica a 0,3×. Tratamento 5.
- **Som:** efeitos = contador de slot travando com "thunk" em cada número, moeda ou ticket saindo, catraca. Trilha: synth-pop com corte seco a cada número, no compasso.
- **Estrutura (11 s):** 0–1 o primeiro número já rolando · 1–8 três números ("6h" → "22h" → "1ª aula") · 8–11 o último trava e vira fecho.
- **Nichos:** ✓ academia (horário, aulas), automotivo ("1 tarde") · ✗ odonto (número sugere preço, e preço é proibido).
- **Kit:** CSS 3D com 12 cópias `translateZ` (extrusão), máscara de placar, `mistura.js` (vídeo dentro do número), `anel`.
- **Referência:** Spotify Wrapped 2024 ([análise](https://alexjimenezdesign.substack.com/p/three-design-elements-that-made-spotify)) · nossa 03 Academia (exemplo) (o placar foi o melhor da peça; cuidado com dígito que parece bug).
- **Estilos:** 30, 6, 22.
- **Risco de IA:** alto: "número gigante + rotulinho sem ser o conceito" está na lista de sinais de IA (nível 52). Evitar: o número É o assunto (horário, medida, quantidade real), nunca métrica decorativa; preço fictício leva "de exemplo".

### L18 · Corte seco tipográfico na batida
- **Assinatura:** uma palavra por batida, encaixada pela largura e **fatiada ao meio** no corte (metade de cima de A + metade de baixo de B), com o vídeo trocando no mesmo quadro. É o "CORTA." que o dono curtiu.
- **Vídeo × design:** 30 / 70.
- **Tipografia:** grito encaixado em 940 px, uma palavra, cor plena atrás ou vídeo dentro. Tratamento 9.
- **Som:** efeitos = o golpe do objeto do nicho em cada corte (tesoura, faca na tábua, carimbo). Trilha: na batida o tempo todo, com um compasso de silêncio antes da palavra final.
- **Estrutura (10 s):** 0–0,5 primeira palavra · 0,5–8 uma palavra por batida (≈ 12–16 palavras), com platôs de 1 s a cada 4 · 8–10 carimbo.
- **Nichos:** ✓ barbearia, hamburgueria · ✗ dentista (ritmo agressivo).
- **Kit:** `analisar_musica.py` (batidas e compassos), `clip-path inset` duplo, `troca`.
- **Referência:** site do dono ("tipografia gigante e corte seco, CORTA. no ácido", 10/10) · DIA Studio ([It's Nice That](https://www.itsnicethat.com/features/dia-mitch-paone-meg-donohoe-graphic-design-animation-typography-180918)).
- **Estilos:** 5, 30, 1.
- **Risco de IA:** médio: corte sem gesto "pisca" (reprovado). Evitar: o corte é a letra fatiada, nunca flash; platô de leitura a cada 4 palavras (regra 18 do gosto do dono).

### L19 · Letras-personagem (identidade cinética)
- **Assinatura:** o nome da loja em letras grossas que "vivem" a ação do nicho: se penteiam, se esticam como cabelo molhado, giram como bobe. O vídeo real passa por dentro delas em 2 s.
- **Vídeo × design:** 15 / 85.
- **Tipografia:** uma display variável com eixos (`wdth`, `wght`, `slnt`) e regras fixas de movimento; letras em comum viajando entre palavras (tratamento 10: "PRONTA" → "PONTAS").
- **Som:** efeitos = o som da ação que a letra faz (secador quando estica, tesoura quando corta, spray quando brilha). Trilha: house com vocal picado; cada sílaba do vocal mexe uma letra.
- **Estrutura (13 s):** 0–1 a palavra já se mexendo · 1–9 três ações · 9–11 vídeo dentro das letras · 11–13 a letra abre a porta para o logo.
- **Nichos:** ✓ salão, moda · ✗ farmácia.
- **Kit:** fontes variáveis OFL, `opentype.js` (contorno do glifo), `movimento.js` (`reage`, `tensao`), receita de letras viajando (nível 34).
- **Referência:** DIA, kinetic identity ([Creative Review](https://www.creativereview.co.uk/dia-agency-typography-motion-design/)) · DEMO Festival 2025 ([Studio Dumbar](https://studiodumbar.com/work/demo-2025)).
- **Estilos:** 5, 8, 12.
- **Risco de IA:** alto se a letra ganhar olhos/boca ou virar mascote. Evitar: a letra age, não tem rosto; o movimento é mecânico da tipografia (eixos), não "fofo".

### L20 · Objeto 3D herói (branco de estúdio, cotas)
- **Assinatura:** um único objeto 3D fotográfico (três luzes, sombra de contato) gira no branco de estúdio, as cotas nascem das bordas e a palavra muda de peso com o objeto.
- **Vídeo × design:** 0–20 / 80 (a foto ou o vídeo entram como fundo desfocado ou num plano final).
- **Tipografia:** grito encaixado que muda `wdth`/peso por variante do produto, itálica que fala, mono nas cotas.
- **Som:** efeitos = clique de encaixe, "tink" de vidro ou metal no pouso, obturador quando a variante troca. Trilha: keynote limpa (piano + pulso) que respira antes da última variante.
- **Estrutura (13 s):** 0–1,5 o objeto chega de perto com desfoque · 1,5–9 três variantes ou especificações · 9–13 o objeto pousa e vira o logo.
- **Nichos:** ✓ ótica, relojoaria · ✗ comida (3D de comida = reprovado).
- **Kit:** `objeto3d.js` (GLB real, HDRI Poly Haven), `troca`, `anel` nas cotas.
- **Referência:** nossa 01 Ótica (exemplo) (aprovada, 8,0) · Filme B (estilo 32, ★★★).
- **Estilos:** 32, 18, 19.
- **Risco de IA:** alto se o objeto for feito de primitivas. Evitar: só GLB real ou modelo já aprovado; material Standard/Physical, nunca Basic; nunca objeto orgânico.

### L21 · Vista explodida
- **Assinatura:** o aparelho se separa em camadas (vidro, tela, bateria, placa) com rótulos finos de engenharia. A peça trocada acende e tudo se fecha de novo.
- **Vídeo × design:** 20 / 80 (abre num plano real da bancada e corta para o 3D).
- **Tipografia:** rótulos mono ≥ 30 px com fio até a peça, grito curto no fecho ("tela nova.").
- **Som:** efeitos = um "clack" metálico de altura diferente a cada camada (escala que sobe), parafusadeira, o reverso com whoosh na remontagem. Trilha: eletrônica de pulso constante; o drop vem quando tudo encaixa.
- **Estrutura (12 s):** 0–1,5 mão real com o aparelho trincado · 1,5–7 explode em 4–5 camadas · 7–10 a peça trocada acende · 10–12 remonta e liga.
- **Nichos:** ✓ assistência de celular, estética automotiva (camadas do verniz) · ✗ salão.
- **Kit:** `objeto3d.js` com GLB real (ou caixas e planos de textura fotográfica), `troca`, OutlinePass do three.js se o estilo for HQ.
- **Referência:** Form Films, UNTLD MOTO; Millarc, Huawei Mate XT ([Stash 3D 2025](https://www.stashmedia.tv/best-of-stash-2025-3d-style/)).
- **Estilos:** 13, 19, 32.
- **Risco de IA:** alto: celular modelado em CSS foi reprovado. Evitar: abrir e fechar com filmagem real da mão; o 3D só no meio, com textura fotográfica.

### L22 · FOOH na fachada
- **Assinatura:** um plano real da rua e da fachada; um objeto gigante (hambúrguer de 4 m, poltrona na praça) desce e "senta" na frente da loja com sombra de contato. Parece notícia.
- **Vídeo × design:** 85 / 15 (o 3D dentro da rua).
- **Tipografia:** quase nada: um letreiro curto que aparece como placa da loja ou faixa no prédio, rastreado no plano.
- **Som:** efeitos = som de rua real, assobio de queda, impacto grave com alarme de carro distante (humor), murmúrio de gente. Trilha: só entra depois do impacto.
- **Estrutura (11 s):** 0–2 rua normal, som ambiente · 2–4 a queda · 4–8 as pessoas olham, o objeto "respira" · 8–11 o letreiro.
- **Nichos:** ✓ hamburgueria, loja de móveis · ✗ dentista ou farmácia (objeto gigante de saúde soa propaganda irresponsável).
- **Kit:** three.js com câmera travada no plano estático do Pexels, plano de sombra em `multiply`, `objeto3d.js`.
- **Referência:** Maybelline/Ian Padgham ([Creative Review](https://www.creativereview.co.uk/faux-ooh-fake-advertising/)) · Jacquemus ([FOOH 2025](https://www.fooh.com/blog/fooh-trends-in-2025)).
- **Estilos:** 30 (no letreiro).
- **Risco de IA:** alto: luz que não bate com o plano denuncia tudo. Depende de plano com câmera parada. Teste 1 quadro antes de prometer; luz-chave copiada da direção do sol no vídeo.

### L23 · Lente de vidro / lupa
- **Assinatura:** um disco de vidro 3D (refração, dispersão) passa pela tela; atrás dele o mundo embaçado fica nítido e as letras se distorcem e se ajeitam.
- **Vídeo × design:** 50 / 50. O vídeo embaçado é o fundo e a lente é o personagem.
- **Tipografia:** tabela de Snellen como tipografia (linhas de tamanhos decrescentes), a última linha vira o endereço.
- **Som:** efeitos = "shimmer" cristalino quando a lente passa, ar, um tom que afina (pitch subindo até a nota certa) quando o foco entra. Trilha: ambient com sino; a nota afinada é a tônica da trilha.
- **Estrutura (13 s):** 0–1 tudo borrado, a lente entra · 1–8 a lente foca rua, rosto, cardápio · 8–13 foca a linha do endereço.
- **Nichos:** ✓ ótica, joalheria · ✗ hamburgueria.
- **Kit:** three.js `MeshPhysicalMaterial` (`transmission`, `ior`, `dispersion`), máscara de foco (dentro nítido, fora 12 px de desfoque), `objeto3d.js`.
- **Referência:** nossa 01 Ótica (exemplo) (a lente como máscara de foco) · Videobolt "glass and dispersion" ([blog](https://blog.videobolt.net/post/top-motion-graphics-trends-2026)).
- **Estilos:** 32, 18.
- **Risco de IA:** médio: vidro com arco-íris exagerado é o "glassmorphism" proibido. Evitar: dispersão sutil, a lente sempre mostrando um mundo filmado, nunca card de vidro.

### L24 · Tela réplica: resolve em 3 toques
- **Assinatura:** a mão real segura o celular e a tela composta em perspectiva mostra a réplica do agendamento ou do pedido (dados inventados). O dedo toca 3 vezes e chega a notificação.
- **Vídeo × design:** 55 / 45.
- **Tipografia:** a interface com a tipografia da marca (não a do sistema), um grito fora do celular a cada toque.
- **Som:** efeitos = toque de vidro, tique de rolagem, pop de notificação, "ding" de confirmação. Trilha: lo-fi leve que só cresce na confirmação.
- **Estrutura (12 s):** 0–1,5 a mão já tocando · 1,5–8 três toques (serviço, horário, confirmar) · 8–12 notificação e o serviço real feito.
- **Nichos:** ✓ barbearia, pet (banho e tosa) · ✗ ótica (agendamento não é o que vende).
- **Kit:** vídeo de mão real + tela composta por homografia (OpenCV ou 4 cantos chaveados), réplica em HTML com `movimento.js`.
- **Referência:** ManvsMachine, Squarespace ([Creative Review](https://www.creativereview.co.uk/squarespace-make-the-next-motion-graphics/)) · estudo advids 2026, tela real > UI desenhada ([advids](https://advids.co/blog/ui-animation-motion-design-trends)) · nossa 02 Loja de celular (exemplo) (tela rastreada no celular real).
- **Estilos:** 7, 18.
- **Risco de IA:** alto: celular em código e ícone-app colorido já foram reprovados. Evitar: o aparelho é sempre filmado; a UI sem ícones redondinhos; é a linguagem natural para um dos 2–3 WhatsApp da série (F10/F11).

### L25 · Laboratório: verdade ou mito
- **Assinatura:** uma bancada branca com régua e cronômetro. Três mitos do nicho em 15 s, cada um testado no macro real e julgado por um carimbo VERDADE / MITO.
- **Vídeo × design:** 50 / 50. O macro real é a prova e a camada de medição é o desenho.
- **Tipografia:** o mito em serif entre aspas, o veredito em carimbo condensado com tinta falhada a 6° de rotação, dados em mono com "de exemplo".
- **Som:** efeitos = clique de cronômetro, bipe de medição, carimbo seco (low thump + papel) em cada veredito. Trilha: groove mínimo que **para** antes de cada carimbo.
- **Estrutura (15 s):** 0–1,5 o primeiro mito escrito · 1,5–5, 5–9, 9–12 três testes · 12–15 o carimbo final é a marca.
- **Nichos:** ✓ farmácia (protetor solar, hidratação; nunca medicamento), ótica (luz azul) · ✗ dentista (mito/verdade sobre tratamento esbarra na publicidade do conselho).
- **Kit:** carimbo SVG (escala 1,4 → 1 em 4 quadros, `anel`, `reage`), `tq` nas setas, `analisar_musica.py` para as paradas.
- **Referência:** Vaseline Verified, Grand Prix Cannes 2025 ([Ogilvy](https://www.ogilvy.com/work/vaseline-verified)).
- **Estilos:** 22, 23, 1.
- **Risco de IA:** médio: gráfico inventado de "estudo" é desinformação. Evitar: só mito que o cliente pode provar; nada de "clinicamente comprovado"; o carimbo é o personagem.

### L26 · Do material ao produto (process film)
- **Assinatura:** cinco passos de 2 s, do material bruto ao produto pronto (tora → serra → lixa → tecido → sala). Cada passo tem um número grande e uma palavra, e a costura é por match cut de forma.
- **Vídeo × design:** 80 / 20.
- **Tipografia:** numeração editorial gigante (1 → 5) em serif ou mono, uma palavra por passo, a régua que liga um plano ao outro.
- **Som:** efeitos = foley de oficina (serra, lixa, grampo, tesoura no tecido). Trilha: percussão orgânica que ganha um instrumento a cada passo (build aditivo) e chega cheia no produto pronto.
- **Estrutura (13 s):** 0–1 material bruto · 1–11 cinco passos de 2 s · 11–13 produto pronto + ficha técnica.
- **Nichos:** ✓ móveis, confeitaria (da farinha à fatia) · ✗ farmácia (processo de remédio não se mostra).
- **Kit:** `troca` com match de escala ±5 %, `analisar_musica.py` (seções "sobe"), régua SVG com `stroke-dashoffset`.
- **Referência:** Loop, Bella+Canvas "Heavyweight" ([Stash 2025](https://www.stashmedia.tv/best-of-stash-2025-brand-films/)).
- **Estilos:** 3, 26, 13.
- **Risco de IA:** baixo de IA, alto de "vídeo de banco". Evitar: o match cut por forma precisa ser certeiro (círculo da tora = círculo do botão do sofá); o número é o fio que costura.

### L27 · Stop-motion de bancada
- **Assinatura:** vista de cima, os objetos reais do nicho andam sozinhos a 12 fps com tremidinha. O produto se monta peça por peça e o nome é escrito com o próprio material (confeito, parafuso, mecha).
- **Vídeo × design:** 70 / 30 (fotos reais recortadas movidas quadro a quadro).
- **Tipografia:** o nome escrito com o material (letras de objeto) + uma grotesca pequena e limpa no apoio.
- **Som:** foley de toque a cada quadro-chave (colher, papel manteiga, açúcar caindo, parafuso na mesa). Trilha: pizzicato ou ukulele a 100–110 bpm, um passo por batida.
- **Estrutura (12 s):** 0–1 bancada vazia, o primeiro objeto entra · 1–9 montagem em 8–10 passos · 9–12 a caixa fecha com etiqueta.
- **Nichos:** ✓ confeitaria, papelaria/presentes · ✗ academia.
- **Kit:** `tq` no tempo (`floor(t*12)/12`), jitter de ±1 px por quadro com semente, `recortar.py` (recortes das fotos), matter.js opcional para o "cair".
- **Referência:** Blinkink, Bake Off ([It's Nice That](https://www.itsnicethat.com/articles/isabel-garrett-great-british-bake-off-advert-blinkink-animation-advertising-project-170925)) · Just Eat ([shots](https://shots.net/news/view/just-eats-stop-motion-stunner)) · Zombie Studio "47" ([Stash](https://www.stashmedia.tv/zombie-adds-character-to-cafe-joyeuxs-inclusive-mission)).
- **Estilos:** 17, 25.
- **Risco de IA:** alto se os objetos forem desenhados (o bolo vetorial foi reprovado "por muito"). Evitar: só foto real recortada; sombra dura de luz de cima; tremida de verdade a 12 fps.

### L28 · Matéria digital (dither, ASCII, pixel sort que acende)
- **Assinatura:** o vídeo real começa degradado em código (dither 1-bit verde, rosto em ASCII, pixel sort derretendo) e "acende" em cor no momento em que o produto aparece.
- **Vídeo × design:** 70 / 30 (o vídeo é a matéria, o pós-processo é o desenho).
- **Tipografia:** mono pixelada ou bitmap de verdade (Silkscreen, VT323) só nos rótulos de máquina, grito em grotesca no "acende".
- **Som:** efeitos = bitcrush e chiado de modem no degradado, um "power on" grave quando acende, teclado mecânico. Trilha: chiptune ou eletrônica com filtro fechado que abre de uma vez no "acende".
- **Estrutura (11 s):** 0–1 dither já mexendo · 1–6 dois planos degradados · 6–7 o "acende" (o drop) · 7–11 cor plena e marca.
- **Nichos:** ✓ loja de games/eletrônicos, escola de TI ou coworking · ✗ estética (degradar rosto é ofensivo).
- **Kit:** [dithering-shader](https://github.com/niccolofanton/dithering-shader), [play.core](https://github.com/ertdfgcvb/play.core) (ASCII), [satyarth/pixelsort](https://github.com/satyarth/pixelsort) offline, `shader.js`.
- **Referência:** as fontes do `06-github-creative` §B · Nutter Butter "deep-fried" como parente ([The Drum](https://www.thedrum.com/awards-case-study/how-nutter-butter-revived-its-brand-with-a-surreal-nutterverse-campaign)).
- **Estilos:** 14, 27.
- **Risco de IA:** alto: glitch e partícula estão na lista de sinais de IA. Evitar: o degradado tem sentido narrativo (antes = mundo sem o produto); um efeito só por peça; o "acende" é o conceito.

### L29 · Matéria simulada (tecido, goo, tinta)
- **Assinatura:** uma matéria física simulada carrega a mensagem: tecido pendurado que a tesoura corta e cai revelando o preço; gotas de espuma gooey que se juntam e formam a palavra; duas tintas que se misturam de verdade.
- **Vídeo × design:** 20 / 80.
- **Tipografia:** a palavra é revelada ou formada pela matéria; grotesca de cartaz em cima.
- **Som:** efeitos = o som da matéria (tecido rasgando ou caindo, bolha estourando, tinta escorrendo). Trilha: entra fraca e ganha corpo conforme a matéria se forma; corte seco quando a palavra fica legível.
- **Estrutura (12 s):** 0–1 a matéria já em movimento · 1–8 a transformação · 8–12 a matéria forma o logo.
- **Nichos:** ✓ loja de tecidos/costura (tecido), lava-rápido (espuma gooey) · ✗ odonto.
- **Kit:** [verlet-js](https://github.com/subprotocol/verlet-js) (tecido, pré-simulado), `goo`/`gooFiltro` do `movimento.js`, [spectral.js](https://github.com/rvanwijnen/spectral.js) (tinta), passo fixo + semente.
- **Referência:** `06-github-creative`, ideias 10, 17 e 18.
- **Estilos:** 8, 9, 2.
- **Risco de IA:** alto: metaball colorido liso é "blob de IA". Evitar: cor e textura da matéria tiradas da filmagem real do nicho; abrir com 1 s de vídeo real da matéria verdadeira.

### L30 · Humor de série (objeto que fala / episódio absurdo)
- **Assinatura:** duas variantes. **(a) Objeto fala:** o produto real na bancada ganha olhos e boca 2D e reclama ("Você me toma em jejum?"), em < 10 s. **(b) Episódio absurdo:** lo-fi "deep-fried", zoom brusco, legenda enigmática ("Episódio 3"), o produto num lugar impossível, sem explicar.
- **Vídeo × design:** 80 / 20.
- **Tipografia:** (a) legenda de personagem com cor própria; (b) texto de VHS e legenda de meme.
- **Som:** (a) a voz do personagem com pitch alterado, "boing" nas sobrancelhas, sem música; (b) bitcrush, drone grave, corte para silêncio total e um grito distorcido de 4 quadros.
- **Estrutura (8–10 s):** 0–1 o absurdo já no quadro 0 · 1–7 a piada · 7–10 só a marca, sem CTA (o mistério é o CTA).
- **Nichos:** ✓ hamburgueria (público jovem), pet · ✗ dentista, farmácia (humor com remédio = automedicação) e qualquer marca que não aceite humor estranho.
- **Kit:** vídeo estático do Pexels + rosto 2D em SVG com `tq` (a); `shader.js`, bitcrush no `som.py` (b).
- **Referência:** Ryanair no TikTok ([Socialinsider](https://socialinsider.io/blog/ryanair-social-media-strategy)) · Duolingo ([Shorty](https://shortyawards.com/14th/duolingo-tiktok-2)) · Nutter Butter ([The Drum](https://www.thedrum.com/awards-case-study/how-nutter-butter-revived-its-brand-with-a-surreal-nutterverse-campaign)).
- **Estilos:** 27, 10.
- **Risco de IA:** **o maior do cardápio**. O dono reprovou personagem em código e "rosto desenhado". Só como a amostra ousada da série (no máximo 1), só com o rosto mínimo (dois pontos e um traço) sobre produto filmado, e só depois de mostrar 1 quadro para ele.

---

## Combinações que já sabemos que funcionam
- **L01 + L18** (Hamburgueria (exemplo)): palavra-janela + corte na batida.
- **L20 + L23** (Ótica (exemplo)): objeto 3D + lente que foca.
- **L11 + L17** (Estética automotiva (exemplo)): lâmina + contador.

Uma peça tem **uma** linguagem principal e no máximo **uma** de apoio. Três linguagens na mesma peça viram colcha de retalhos.

## Linguagem nova (31+)
Vale quando muda pelo menos 2 das 3 colunas em relação a todas as linguagens existentes:
- a relação vídeo × design;
- o que a letra faz;
- a estrutura.

Escreva a ficha no mesmo formato, com a reação do dono quando houver.
