# 08 · A receita do portfólio: por que Filme A, Filme C MEIA-NOITE e Filme B são o padrão-ouro

Estudo de leitura (17/10/2026). Fontes: `projetos/<projeto>/` (BRIEFING, ESTILOS, `*/fonte/*.html`, `som.py`, `montar.sh`, `musica/LICENCAS.md`), `aprendizado/reacoes.md` (linha de 17/10), `marcas/<marca>/evolucao.md` (linha 8), folhas de 12 quadros dos 3 finais e de 4 amostras da prospecção (11-hamburgueria e 01-otica, aprovadas; 03-academia e 12-confeitaria, reprovadas).
Frase do dono que guia tudo: *"desenhar bem, juntar com os vídeos quando necessário, uma música boa de fundo e sons que deixam o vídeo didático."*

---

## 1 · As três peças por dentro

### 01 · Filme A ("o do cartão"), 9:16, 60 fps, 19,83 s = 40 batidas
- **Herói:** um cartão de metal preto fosco com chip dourado e "MARCA" gravado, em three.js r186 (`vendor/three-r186.js`).
  - Materiais: `MeshPhysicalMaterial`, com frente e verso `metalness 1 · roughness 1 · clearcoat 1 · clearcoatRoughness .07`. A textura escovada é gerada em canvas (`escovado()`, com mapas de cor, rugosidade, metal e bump). A borda é metal polido (`roughness .2`).
  - Luz: não há lâmpadas. Há um **ambiente PMREM por cor de fundo** (`ambiente(nome)`, l. 265): 7 painéis brancos (faixa em cima, faixa larga atrás da câmera, duas verticais de contorno, softbox, contra-luz) mais um "chão" da cor do fundo. Por isso o metal rebate o cobalto, o laranja ou o creme do plano em que está.
  - Câmera: perspectiva calibrada para 1 unidade = 1 px (`DIST=1900`, fov = 2·atan(960/1900)), o que permite pôr o cartão numa coordenada de tela (`poeCartao({x,y,z,rx,ry,rz,anc})`).
  - Tom: ACES, exposição 1,05.
  - Profundidade: o **grito é montado em 3 camadas** (`gT/gF/gI`: trás, frente e invertida), e o cartão passa **entre as letras**. O `casco()` projeta o contorno do cartão na tela para recortar a camada da frente.
- **Roteiro visual** (planos de 2 batidas, ~1 s cada; `PLANOS`, l. 145):
  - 0–2 s: fundo tinta, *seu* **DINHEIRO.**, com o cartão entrando girando entre as letras. Depois vem o macro do chip.
  - 2–4 s: cobalto, **PAGUE.**, com o tap no terminal e um ✓.
  - 4–7 s: laranja, **VIAJE.**, e um mapa de pontos com o arco GRU→LIS→TYO (o cartão é o avião).
  - 7–9 s: tinta, uma carteira com 2 chips de moeda (BRL e EUR).
  - 9–10 s: creme, *e o que sobra,*, com um "$" desfocado gigante atrás (é a pausa da música).
  - 10–13 s: **INVISTA.** no drop, com o saldo em mono contando até R$ 12.480,00 sobre o fundo limão.
  - 13–15 s: **FRONTEIRA.**, e depois R$ / € / ¥ em cortes de meia batida.
  - 15–19,8 s: o cartão pousa em "Filme A", o fundo fica limão com *peça o seu.* e a assinatura "motion · o dono".
- **Tipografia:**
  - Grito: Archivo 900, ajustado por medição para ocupar **940 de 1080 px** (`montaGrito`: fs = 200·940/largura), com tracking −.045em e entrelinha .86.
  - Voz: Instrument Serif itálica 104 px, minúscula, por cima do grito.
  - Dados: JetBrains Mono 700, de 30 a 100 px.
  - Por tela: **1 palavra gigante + 1 palavrinha**, e no máximo 1 número.
  - Um HUD fixo no topo ("Filme A" + 01/05) dá o "capítulo".
- **Transição:** corte seco **no pico de velocidade do giro** (a tabela `GIROS` põe o pico de cada giro de 360° na batida do corte). A cor do fundo troca no corte. Não há dissolve.
- **Ritmo × música:** *What About Action?* (Diego Nava, Mixkit #474), dance-pop a 121,0 BPM (fino, medido com fluxo espectral; o `batidas.py` leu 120,2 e escorregava 130 ms).
  - O vídeo entra na batida 11 da faixa, para que o quadro 0 seja tempo forte.
  - A pausa de 2 tempos da faixa cai em *"e o que sobra,"*, e a volta cai no INVISTA.
  - Cenas e efeitos são escritos **em batidas** (`ritmo.js`), então trocar a música só pede reescalar.
- **Som** (`som.py`, 95 linhas, tudo sintetizado em numpy a 48 kHz):
  - `whoosh` (ruído com passa-faixa variando de 500 a 4200 Hz, pico em 62 % da duração): **o pico cai no corte**. São 10 giros, com ganho de .22 a .36 e pan −.35.
  - `tap` + `bip` 1760/2350 Hz no contato do NFC.
  - `tick` por moeda que aparece.
  - `subida` (ruído que abre de 300 a 6000 Hz) na pausa, antes do drop.
  - `pouso` (tum de 95 Hz + 3 parciais metálicos) quando o cartão pousa.
  - Mix: música ×0,8 + efeitos. Depois, limitador e loudnorm em 2 passadas a −14 LUFS e −1,5 dBTP (`montar.sh`).
  - Imagem: 2 passadas a 240 fps com meio subquadro de deslocamento, depois `tmix` → **desfoque de movimento real** a 60 fps.

### 02 · Filme C "MEIA-NOITE" ("o filme da meia-noite"), 16:9, 20 s
- **Herói:** não há objeto. **A luz e a película são o herói.**
  - Um fósforo desenhado em canvas (`#luz`).
  - Película em canvas (`#pel`): 6 telhas de grão de 640² semeadas, que trocam a 24 q/s, mais poeira, riscos, flicker e gate weave.
  - Halation vermelha em 3 camadas de texto (`.titulo`, `.halo` com stroke de 6 px e blur de 10, `.halo2` com blur de 42), `#bloom` radial e um `#feixe` de luz que varre o título uma vez.
- **Roteiro visual** (85 BPM, B(n) = 13,058 + n·0,706 s):
  - 0,35 s: o fósforo acende → "Filme C apresenta" em mono.
  - 4,6 s: créditos em Instrument Serif 112 px sobrepostos e tremidos, com "00" gigante desfocado ao fundo (Archivo 62 % de largura, 1500 px, blur 24).
  - 8,1 s: recortes *a cidade* / **NÃO** / *dorme.* e o timecode 00:00 em caixa vermelha.
  - 10,2 s: as letras de MEIA-NOITE pousam uma a cada semicolcheia.
  - **12,0 s:** drop, com o título inteiro e o hífen em brasa.
  - 16,6 s: relógio 23:59:59 em mono 250 px; o tique "vira".
  - 18,35 s: corte seco para o preto e "motion · o dono".
- **Tipografia:** são 3 vozes, sempre: Archivo condensado 900 (grito), Instrument Serif (créditos) e JetBrains Mono (máquina). Só um vermelho, `#E50914`.
- **Transições:** fade para o preto, entrada de projetor piscando (0 → .55 → .2 → 1 em ~4 quadros de filme) e clarão.
- **Música:** *No Turning Back* (A. M., Mixkit #118), electronica sombria a 85 BPM com bumbo 3-3-2.
  - Entra em 11,362 s da faixa, para que **o bumbo do drop caia no título** (12,000 s).
  - Entra com fade de 0,9 s sob o fósforo e para seco (30 ms) no preto.
- **Som** (`som.py`, 102 linhas): o mais rico dos três. Cada efeito é **foley desenhado** do gesto da tela:
  - risco do fósforo (ruído granulado com 35 % de densidade, passa-alta de 1800 Hz) → "fwump" (filtro que abre de 3800 a 300 Hz) + baque de 75 Hz com reverb;
  - chiado da chama + 26 estalos sorteados, e um sopro quando apaga;
  - batida surda de projetor (52 Hz) a cada crédito;
  - "papel batendo" em cada recorte;
  - tique mecânico (clique + 2350 Hz + 180 Hz) no timecode;
  - subida até o drop, e um sopro em cada letra que pousa;
  - `impacto()` (sub que cai de 110 para 38 Hz + crack + 4 parciais de metal grave + reverb de 2,6 s) no título;
  - claque + impacto no "vira", e sub de 30 Hz no preto.
  - Mix: música 1,0 + efeitos ×0,55, normalizado a −14 LUFS e pico ≤ −1.

### 03 · Filme B ("o do produto que ia lançar"), 9:16, 18,69 s
- **Herói:** um seixo de alumínio e vidro de 54 mm, **modelado de verdade** em three.js.
  - Corpo em `LatheGeometry` (256 segmentos) de alumínio jateado (`metalness 1 · roughness .34` + mapa de rugosidade circular).
  - Chanfro diamantado polido (`roughness .05`), que pega o risco de luz.
  - Aro com 60 marcas gravadas (canvas).
  - Vidro fosco escuro com sulcos concêntricos (`roughness .46`, bump .0012, `clearcoat 1 / .045`; a transmissão foi desligada de propósito).
  - Anel de luz laranja que "enche", LED com brilho aditivo, botão polido em rebaixo.
  - Sala-caixa cinza + faixas de luz (PMREM) + 1 luz direcional de .55.
  - **Sombra de contato** em 2 planos (opacidades .5 e .12) que não gira com o objeto.
  - Câmera de 20° de fov em órbita (`estado(t)`: elevação, azimute, distância, altura na tela), com keyframes `K(t, …)` e curvas eio, eo3 e eioExpo.
- **Roteiro visual** (meio compasso HB = 1,143 s):
  - 0–2,3 s: "Um." em Archivo 800 de 76 px, sozinho no branco `#F4F5F7` (a música está baixa: a 55 %, subindo).
  - 2,3 s: corte para um macro do vidro de cima (elevação 88°); a câmera abre até o objeto inteiro.
  - 4,6 s: a cota do diâmetro (Ø 54,0) e a da espessura se desenham em SVG e **a cota vira o número** "4,2 mm" (396 px), com *e nada mais.* em serif de 80 px e "VIDRO + ALUMÍNIO" em mono.
  - 8,0 s: o objeto tomba para a câmera (o corte acontece no meio do giro); vem a vista de cima e o anel laranja enche de 0 a 38, com um mostrador de 38 traços em volta.
  - 11,4 s: chicote de câmera para a lateral; o botão é apertado (pressão em 50 ms, soltura em 160 ms) e o LED acende.
  - Em seguida, a câmera mergulha no vidro: "1 botão" e *simplesmente.*
  - 14,9 s: fecho com **Filme B.** (o ponto é o laranja) + *chega dia 23.* + assinatura.
- **Tipografia:** os números são gigantes (396–520 px), a unidade fica a 116 px e a frase em serif itálico a 80–96 px. Rótulos técnicos em mono de 30 px, cinza. HUD discreto: "do portfólio ONE · ESPEC. 01/03".
- **Música:** *Slow Rain* (A. M., Mixkit #122), electronica calma a 104,95 BPM.
  - Entra no compasso 10 da faixa.
  - **Os chimbais entram exatamente no "4,2 mm"** (compasso 12 = 4,574 s).
- **Som** (`som.py`, 94 linhas):
  - `tick` seco (3100 + 5400 Hz) quando cada cota **trava**;
  - catraca: **37 tiques, um por hora**, seguindo a mesma curva eo3 do anel na cena (o som é calculado com a fórmula da imagem), e ficando mais fortes no fim;
  - `clique` duplo do botão (aperta e solta 0,16 s depois);
  - `acento` em cada número (pulso de 62 a 102 Hz + sino em quinta: 1318/1975/2637 Hz);
  - `sopro` com o pico **no corte**.
  - Mix: música ×0,55 + efeitos ×0,42 (a música fica embaixo; o som didático fica claro).

---

## 2 · O denominador comum: 14 regras (com a evidência)

1. **Um herói, desenhado com ofício.** Cada peça tem um único objeto principal: o cartão, o fósforo e a película, ou o seixo. Ele é construído (geometria, material PBR, textura gerada, luz de estúdio PMREM, sombra de contato) e não é uma foto colada.
2. **O herói conta a história; o texto só nomeia.** É sempre 1 palavra gigante ou 1 número por plano, mais 1 linha em serif minúsculo e um rótulo mono. O máximo é 3 elementos de texto vivos ao mesmo tempo (folhas: nenhum quadro do portfólio tem mais).
3. **Três vozes tipográficas fixas:** grotesca pesada (Archivo 800/900), serif itálico (Instrument Serif) e mono (JetBrains Mono). O grito é medido para ocupar ~87 % da largura, e os números chegam a 400–520 px.
4. **Um destaque de cor só:** limão no Filme A (só no saldo e no fecho), vermelho no Filme C, laranja no Filme B (LED, anel e o ponto do nome). O resto é neutro ou chapado.
5. **Tudo é função do tempo, escrito em batidas** (`BT`, `HB`, `B(n)`). Cenas e som leem a mesma grade.
6. **O corte acontece no meio do movimento** (pico do giro, tombo, chicote de câmera), nunca com o objeto parado e nunca em dissolve.
7. **A música é medida e posicionada, não "colocada":** o ponto de entrada na faixa é escolhido para que o tempo forte, a pausa e o drop caiam em momentos da imagem (INVISTA; MEIA-NOITE a 12,000 s; chimbais no 4,2 mm).
8. **Uma faixa por peça, com caráter do gênero:** dance-pop para fintech, electronica sombria para suspense, minimal calma para keynote. A música combina com o *sentimento* do produto.
9. **Efeito sonoro = gesto da tela, sintetizado sob medida.** Não há nenhum arquivo de biblioteca. Cada som é calculado para o material do objeto: metal pousando, tap de plástico, catraca de mecanismo, fósforo, papel. Ele fica alinhado ao quadro (tick quando a cota trava; catraca com a mesma curva do anel). É isso que soa "real" e "didático".
10. **Poucos sons, com hierarquia:** os efeitos ficam de 6 a 10 dB abaixo do pico da música, salvo os 1–2 acentos-chave (impacto do título, pouso). Silêncio e respiro existem: no "Um." a música fica a 55 %, e no fósforo há fade de 0,9 s.
11. **Abre num gancho minimalista e fecha em calma:** "Um." sozinho, um fósforo no escuro, uma palavra com o cartão. O fecho é o objeto pousado, o nome, uma frase serif e a assinatura pequena. **Não há CTA de anúncio** (nem WhatsApp, nem preço, nem "promoção").
12. **Um "capítulo" visível** (01/05, ESPEC. 01/03, timecode) dá estrutura de filme, não de panfleto.
13. **Acabamento técnico:** 60 fps com desfoque de movimento real (2 passadas a 240 fps e tmix), ACES, −14 LUFS e pico de −1 dBFS, styleframes aprovados antes de animar.
14. **Duração de 18–20 s com 5–6 ideias**, cada ideia com pelo menos 1 meio-compasso (~1–2 s) para ler.

### Por contraste: o que as reprovadas fazem diferente
- **Propaganda:** a academia termina num cartaz "VALE 1ª AULA · apresenta na recepção · endereço · @ · dados de exemplo · R$ 89,90". A confeitaria termina numa etiqueta com calendário e "encomende com 5 dias / link da bio". O texto vira **copy de anúncio**, enquanto no do portfólio o texto é **legenda de filme**.
- **Poluição:** a academia empilha 6H / OU / 22H / TREINO / com / PROFESSOR / 89,90 numa pilha física, com textura de concreto e borracha, foto dentro das letras e placas. Isso dá de 6 a 9 elementos de texto vivos ao mesmo tempo, e o número "fica bugado" (quadros 6–7 da folha). A confeitaria mistura 4 linguagens (vídeo de bolo, letras de comida, mármore, mãos com fita).
- **Som falso:** os `som.json` de 03-academia, 12-confeitaria, 06-salao e outros chamam **12 a 15 arquivos de `base/sfx/`** (Mixkit, Freesound, Pixabay), como `anilha-pesada.wav` e `fita-laco.wav`. É som de biblioteca encaixado num gesto desenhado que não tem aquele peso ou material, e por isso "não tá real". Nos do portfólio, nenhum efeito é arquivo.
- **Música errada:** a academia **reusou a trilha do Filme A** (dance-pop) e a confeitaria **reusou a do Filme B** (Slow Rain), fora do sentimento do produto. Barbearia e salão usaram `cine-01` e `lofi-01` genéricas ("odiei a música"). No do portfólio, a música foi escolhida para *aquele* produto e posicionada pelo drop.
- **As aprovadas confirmam a regra:**
  - A **ótica** é a mais do portfólio do lote: um herói 3D (os óculos) com sombra de contato, branco de estúdio, 1 palavra gigante + serif, e a tabela de Snellen como contexto desfocado.
  - A **hamburgueria** é aprovada por ser ousada e limpa (vermelho chapado, 1 palavra por plano, vídeo **dentro** de uma moldura ou de letra).
  - As duas têm o fecho de anúncio que o dono tolerou, mas o pedido dele é afastar disso.

---

## 3 · Receita do portfólio aplicada a negócio local, sem cara de anúncio

Regra de tradução: **o negócio é o "produto fictício" e o serviço é o objeto-herói.** O vídeo é o "keynote do ofício", não a promoção. O texto mostra *o que é feito e com que precisão*, nunca oferta ou preço. O fecho é o nome, uma frase serif e o @ pequeno (como a assinatura do portfólio). O vídeo real entra só onde o desenho não convence (textura de comida, mão de artesão): 1 plano, dentro de uma moldura, de uma letra ou de uma máscara, nunca como fundo de tudo.

### Piloto A · Assistência técnica de celular (nicho 02-celular): "Por dentro." ★ recomendado
- **Ideia:** o celular é desmontado em camadas como numa keynote, e cada camada vira um número do serviço.
- **Herói:** um smartphone **genérico** (sem câmera ou recorte de marca real), com `RoundedBox` de alumínio jateado e vidro fosco. É o Filme B reaproveitado: corpo `aluJ`, chanfro polido, vidro com clearcoat e sombra de contato. Ele **explode em 4 camadas** na vertical (vidro, tela OLED com quadriculado de pixels, bateria, placa com conectores), com as cotas em SVG desenhando-se em volta.
- **Roteiro (~18 s, 6 ideias):**
  1. "Por dentro." minúsculo no branco.
  2. O aparelho gira e o vidro levanta (a cota vira **0,4 mm**, *de vidro novo.*).
  3. A bateria desliza para fora e um anel enche (**100 %**, *de novo.*).
  4. A placa com uma lupa sobre o conector mostra **1** *conector, limpo.*
  5. As camadas voltam e encaixam com clique.
  6. Fecho: o nome da loja, *seu celular, como novo.* e o @ pequeno.
  - Os números são do serviço ilustrativo, e o guia diz isso.
- **Vídeo real:** opcional, só 1 plano de 1,5 s de mãos com pinça ou chave pentalobe recortadas numa janela redonda (a "lupa"). Sem ele, o vídeo funciona igual.
- **Som sob medida (som.py):**
  - micro-parafuso = `tick` a 4–5 kHz com catraca (a mesma da bateria do Filme B);
  - ventosa no vidro = sopro grave curto + estalo;
  - conector flat = `clique()` duplo;
  - bateria saindo = deslize de ruído com passa-faixa de 800 a 2500 Hz;
  - `acento` em cada número e `pouso` metálico no encaixe final.
- **Música:** electronica minimal ou ambient de 100–112 BPM, nova (não pode ser Slow Rain), limpa e com um elemento que entra no 1º número.
- **Por que primeiro:**
  - É o nicho mais próximo de "produto" e do Filme B. Herói, câmera, material, cotas e som já existem e foram aprovados.
  - É didático por natureza ("mostra o que tem dentro"), não tem preço nem promoção, e não depende de filmagem.
  - Tem risco baixo de poluição: um objeto só e um número por plano.

### Piloto B · Marcenaria / loja de móveis (nicho 13-moveis): "A junta."
- **Ideia:** uma cadeira montada peça a peça no ar, em vista explodida, onde cada encaixe é uma especificação.
- **Herói:** uma cadeira em three.js com madeira (textura de veio gerada em canvas, `roughness .6`, verniz `clearcoat .3`), a junta de **espiga e encaixe** em close e as cotas em mm.
- **Vídeo real:** 1 plano de plaina ou lixa na madeira (textura que o 3D não dá), dentro de uma faixa.
- **Som:** batida de madeira (seno de 180–260 Hz + ruído curto passa-banda), encaixe (clique grave), lixa (ruído rosa com passa-faixa e envelope de vai e vem) e pouso no chão.
- **Música:** acústica ou indie calma, com violão ou piano de 90–100 BPM.

### Piloto C · Barbearia (nicho 05-barbearia, reprovado na música): "Meia-noite, só que às 9h."
- **Ideia:** a linguagem do Filme C, uma abertura de série para a barbearia: luz baixa, película, título que se monta no drop.
- **Herói:** a navalha como luz. Um fio de luz desenhado (canvas e halation) "corta" o escuro e revela o nome, letra por letra.
- **Vídeo real:** 2 planos curtos em P&B com grão (`kit/pelicula.js`) da tesoura e do degradê, sob a película.
- **Som:** foley sintetizado da tesoura (dois cliques metálicos de 3–5 kHz espaçados 40 ms + ressonância curta), da navalha (chiado agudo de ruído com passa-alta de 4 kHz e envelope de 120 ms) e do borrifador (ruído com ataque e queda rápida). Impacto no título.
- **Música:** soul ou funk lento, ou boom-bap instrumental a 85–92 BPM. **Não** cine genérico.

**Recomendação: fazer o A primeiro.** Ele tem o maior reaproveitamento (o Filme B é quase o esqueleto), o menor risco de "propaganda" e de "poluição", e o "didático" vem do próprio objeto. O C entra como 2º piloto para provar que a receita vale também para serviço de gente (com vídeo real dosado).

---

## 4 · O que reaproveitar direto

| O quê | Caminho | Uso |
|---|---|---|
| Objeto 3D por tempo (renderer, estúdio PMREM, câmera em órbita, chaves `[t,{…},curva]`, `O.proj`) | `~/motion-studio/skill/kit/objeto3d.js` (cópia em `<pasta-da-série>/moldes/base/objeto3d.js`) | Base do herói do Piloto A/B. As regras dos materiais do portfólio estão no cabeçalho (l. 20–32) |
| Materiais do Filme B (alumínio jateado, chanfro, vidro fosco sulcado, anel/LED aditivo, sombra de contato em 2 planos) | `projetos/<projeto>/03-filme-b/fonte/filme-b.html` l. 93–216 | Copiar os materiais e a sombra; trocar a `LatheGeometry` pelo corpo do celular |
| Câmera `estado(t)` + `K(t, ks)` + cotas SVG que viram número | o mesmo arquivo, l. 219–300 (câmera) e l. 305–430 (cotas, mostrador de 38 traços, chamada do botão) | Assinatura "cota → número" |
| Cartão entre as letras (3 camadas, `casco()`, `montaGrito` a 940 px, ambiente por cor) | `01-filme-a/fonte/filme-a.html` l. 179–320 | Herói chapado em cor plena (hamburgueria, moda) |
| Giros com pico no corte | `filme-a.html` l. 168–170 (`GIROS`, `giroY`) | Corte no meio do movimento |
| Ritmo em batidas | `01-filme-a/fonte/ritmo.js`, `skill/kit/ritmo.js` | Grade comum de cena e som |
| Película (grão em telhas, riscos, flicker, gate weave) + halation | `02-filme-c/fonte/meia-noite.html` l. 206–243 e CSS l. 46–51; `skill/kit/pelicula.js` | Piloto C |
| Efeitos sintetizados do portfólio já reunidos (whoosh, sopro, reverso, riser, impacto, subdrop, baque, acento, tick, tique, clique, tap, bip, pouso, papel, estalo, limitador, `gera(cfg)`) | `~/.claude/skills/motion-design/kit/som.py` (= `skill/kit/som.py`) | Partir daqui. Escrever o foley novo do nicho (parafuso, ventosa, madeira, tesoura) como função nova, no mesmo estilo, alinhada à curva da cena |
| `som.py` originais (para copiar a lógica de casar som com curva: catraca eo3; pico do whoosh no corte) | `01-filme-a/fonte/som.py`, `02-filme-c/fonte/som.py`, `03-filme-b/fonte/som.py` | Molde por peça |
| Medir BPM e achar o drop | `skill/kit/batidas.py`, `skill/kit/analisar_musica.py` | Escolher o ponto de entrada da faixa (regra 7) |
| Montagem (2 passadas a 240 fps → desfoque de movimento; loudnorm em 2 passadas a −14 LUFS; web CRF 22 com faststart; pôster) | `01-filme-a/fonte/montar.sh`, `02-filme-c/fonte/montar.sh` | Entrega (para a prospecção, 1080×1920 a 30 ou 60 fps) |
| Fontes (Archivo variável, Instrument Serif itálico, JetBrains Mono) | `03-filme-b/fonte/fontes/`, `base/fontes/` | As 3 vozes |

**Não reaproveitar:** `<pasta-da-série>/moldes/base/sfx/` (efeitos de biblioteca, o som "não real") nem as 3 trilhas do portfólio em outros nichos (já viraram marca dos motions do portfólio e soaram erradas na academia e na confeitaria). Cada piloto precisa de uma música nova, medida e posicionada pelo drop.
