# 02 — Anotações e destaques por cima da gravação de tela (tutoriais de software)

Pesquisa de 16/10/2026 para a skill **edicao-video** (aulas CRM/cliente B e YouTube). Ponto de partida: o que o estúdio já tem
(`zoom.py` até 1,6×, `atividade.json` a cada 1/4 s, `SeloStatus`/`Capitulo` no Remotion, `spot()`/`cam()`/`cursor()`/`wipe()` no
`kit/comum.js`) e o último vídeo (`projetos/<projeto>/v1/`, aula SLA v2).

Legenda das fontes dos números: **[medido]** = constante lida no código-fonte de uma ferramenta aberta; **[doc]** = documentação
oficial; **[pesquisa]** = artigo científico; **[casa]** = regra que já existe no estúdio; **[proposta]** = número que eu recomendo
começar usando (sem fonte externa, ajustar depois de ver no vídeo).

---

## 1. Resumo em 5 linhas

1. O que separa um tutorial "claro" de um "bonito" é **sinalização sincronizada com a fala**: um destaque por vez, aparecendo até 0,3 s da palavra, perto do alvo (Mayer: sinalização d = 0,69, contiguidade temporal d = 1,31, espacial d = 0,82; ajuda mais quem sabe pouco — o público do cliente B).
2. As ferramentas de mercado (Screen Studio, FocuSee, Cursorful, Tella, Recordly, OpenScreen, Screenize) convergiram para o mesmo pacote: zoom que segue o clique (1,5–2,5× para clique, 2,2–2,8× para campo digitado), entrada de zoom em ~1–1,5 s com curva `cubic-bezier(.16,1,.3,1)`, cursor suavizado e clique visível em 140–350 ms.
3. O que elas **não** fazem e nós podemos fazer (porque montamos no Remotion com a transcrição): anotação puxada pela palavra falada — holofote, lupa, elemento que levanta, seta + rótulo e passo numerado — com o retângulo do elemento achado pela `atividade.json` + OCR, guardado no **tempo editado** e convertido pela vista do zoom quadro a quadro.
4. Nosso gargalo técnico é a nitidez: zoom acima de 1,6× numa captura 1080p pixela; para lupa e elemento que levanta, recorte do **bruto** (não da camada de tela já ampliada), congelado em PNG quando o elemento não muda; e peça captura 1440p/4K.
5. Orçamento por aula: 1 anotação a cada ~15–25 s em média, no máximo 1 destaque ativo (exceto a sequência de passos numerados, até 4), cada um parado no mínimo `máx(1 s; 0,5 + 0,33 s × palavras)`; três receitas prontas para a aula SLA no fim.

---

## 2. Catálogo de técnicas [11]

### 2.1 Zoom que segue a ação (pan & zoom)
- **Como é:** a "câmera" aproxima onde o clique/digitação acontece e desliza entre alvos sem voltar ao 1× quando o próximo alvo está perto.
- **Ajuda:** UI com texto pequeno (CRM tem fonte de 12–13 px), campos sendo preenchidos, menus.
- **Atrapalha:** troca de página inteira, tela "pulando" a cada clique (enjoo), zoom em captura de baixa resolução (pixela), zoom que corta o contexto que a fala cita ("aqui do lado").
- **Números:**
  - Escala por atividade, Screenize **[medido]**: clique 1,5–2,5×; digitando em campo 2,2–2,8×; código 2,0–2,5×; navegando (cliques espalhados) 1,5–1,8×; rolando 1,3–1,5×; arrastando 1,3–1,6×; lendo 1,0–1,3×; troca de app/página 1,0×; teto global 2,8×; folga em volta da área de trabalho 8 %; alvo ocupa ~70 % do quadro.
  - Antecipação (a câmera começa a ir antes da ação), Screenize **[medido]**: clique 0,15 s; digitação 0,4 s; rolagem/arraste 0,25 s. Mola de posição: resposta 0,35 s, amortecimento 0,9; mola do zoom: resposta 0,55 s, amortecimento 0,9. Sessão de digitação termina após 1,5 s sem tecla; ocioso após 5 s → volta a 1×.
  - OpenScreen **[medido]**: presets 1,25 / 1,5 / **1,8 (padrão)** / 2,2 / 3,5 / 5,0×; entrada do zoom 1,52 s, saída 1,02 s, curva `cubic-bezier(0.16, 1, 0.3, 1)` (o código chama de `easeOutScreenStudio`); zooms a menos de 1,5 s um do outro viram **pan direto** em 1,0 s com `cubic-bezier(0.1, 0, 0.2, 1)`; sugestão automática onde o cursor para entre 0,45 e 2,6 s, com 1,8 s entre sugestões.
  - Recordly **[medido]**: preset "Focused" entra e sai em 0,2 s; "Smooth" 1,52/1,02 s (mesmo do OpenScreen). Tella **[doc]**: zoom automático dura até 5 s. FocuSee **[doc]**: 1,0–4,0×.
  - Nosso **[casa]**: até 1,6×, parado ≥ 4 s, troca só se o alvo novo dura 1,5 s, transição 0,8 s (`zoom.py`, `references/imagem.md`).
- **O que muda para nós [proposta]:** (a) encadear zooms próximos em pan (como o OpenScreen) em vez de voltar a 1×; (b) teto por tipo — 1,6× clique, 2,0× campo digitado **só se a captura for 1440p+**; (c) antecipar 0,15–0,4 s.
- **Links:** [Screenize](https://github.com/syi0808/screenize) (`Screenize/Generators/GenerationSettings.swift`), [OpenScreen](https://github.com/siddharthvaddem/openscreen) (`src/components/video-editor/videoPlayback/constants.ts`, `zoomRegionUtils.ts`, `types.ts`), [Recordly](https://github.com/webadderall/Recordly) (`cursorMotionPresets.ts`), [Tella — zoom](https://www.tella.com/docs/help/editing/add-a-zoom.md), [Screen Studio — auto zoom](https://screen.studio/guide/auto-zoom), [FocuSee (review)](https://hongkiat.com/blog/screen-recorder-focusee-review).

### 2.2 Holofote (spotlight): escurece o resto
- **Como é:** retângulo arredondado em volta do alvo, resto da tela escurecido (não preto), borda fina na cor de destaque.
- **Ajuda:** tela cheia de opções iguais (a página de configurações do SLA tem 8 rádios parecidos); quando a fala diz "esse aqui" sem nome.
- **Atrapalha:** escuro demais (perde o contexto: "onde fica isso?"), holofote que se mexe junto com o zoom (parece tremido), dois holofotes ao mesmo tempo, holofote que fica depois que a fala mudou de assunto.
- **Números [proposta, partindo do `spot()` = 0,6]:** escurecimento 0,55–0,65 de preto (ou 0,45 + desfoque de 2–4 px se o fundo for poluído); folga 10–16 px em volta do alvo; raio 10–14 px; borda 3–5 px; borda externa suave (feather) 20–30 px; entra em 0,35–0,45 s (ease-out), sai em 0,3 s (ease-in); um leve encolher 1,06 → 1 na entrada (já no `spot()`). Duração: até a fala trocar de alvo, mínimo 1,2 s.
- **Base:** "spotlight" e "dimming" são cues clássicos de seleção (de Koning et al.: selecionar, organizar, integrar); EMME (Jarodzka, van Gog) mostra que um holofote/ponto que segue o olhar do especialista guia a atenção e melhora tarefas de classificação. Ferramentas: FocuSee "Spotlight", Arcade "Spotlight".
- **Links:** [de Koning et al. — framework de cueing](https://learntechlib.org/p/72972), [EMME (Springer, revisão 2023)](https://link.springer.com/doi/10.1007/s10648-023-09731-7), [Tutorial com cueing visual](https://www.academia.edu/28764222/Enhancing_interactive_tutorial_effectiveness_through_visual_cueing), [Arcade — hotspots, callouts e spotlights](https://docs.arcade.software/kb/build/interactive-demo/edit/hotspots-callouts-and-spotlights).

### 2.3 Lupa (recorte ampliado por cima)
- **Como é:** círculo ou cartão com o detalhe ampliado 2–2,5×, ligado ao lugar original por uma linha fina ou por um "cone"; a tela continua inteira atrás.
- **Ajuda:** quando é preciso **contexto e detalhe ao mesmo tempo** (o cronômetro "43s" do lead + a conversa inteira). Alternativa ao zoom de câmera quando o zoom cortaria o resto.
- **Atrapalha:** cobrir justamente a área que a fala cita depois; ampliar conteúdo que se mexe rápido; ampliar a camada já ampliada (pixel duplo).
- **Números [proposta]:** ampliação 2,0–2,5× sobre o **bruto**; diâmetro 260–380 px em 1080p (círculo) ou cartão de até 520×300; anel 4 px + sombra `0 18px 44px rgba(0,0,0,.45)`; distância da origem 120–300 px, nunca em cima da câmera do apresentador; entra crescendo 0,6 → 1 a partir do ponto de origem em 0,45 s (expo.out), sai encolhendo de volta em 0,3 s.
- **Referência visual:** o recurso "Magnifier" do Camtasia e os callouts de lupa dos templates de "SaaS explainer" do After Effects; Mayer contiguidade espacial (detalhe perto do original).

### 2.4 Cursor realçado e clique visível
- **Como é:** cursor maior e suavizado; no clique ele "afunda" e solta um anel.
- **Ajuda:** sempre que a ação é um clique e o cursor é pequeno (Retina em 1080p = cursor de ~12 px). Dá ritmo e prova "foi aqui que ele clicou".
- **Atrapalha:** anel em clique irrelevante (rolar a página, clique para focar janela), cursor gigante cobrindo o texto do botão, rastro.
- **Números:** OpenScreen **[medido]**: ponto de realce raio 28 px em referência 1920 px, opacidade 0,95; animação de clique 140 ms; anel some em 240 ms; suavização 0,18. Screenize **[medido]**: aperta para 0,75–0,8 em 0,08 s, solta em 0,15 s com mola leve. Recordly **[medido]**: cursor 2,5× maior, "quique" do clique 350 ms. Nosso `cursor()` **[casa]**: aperta 0,82, anel 0,55 s, curva com arco de 8 %.
- **Nosso limite:** o cursor já vem queimado na gravação (OBS/Screen Studio). Sem telemetria do mouse, dá para **achar** o cursor (casar o desenho da seta do macOS com `cv2.matchTemplate` no bruto) e **achar o clique** (surto de mudança pequeno em volta do cursor nos 0,1–0,3 s seguintes, já visível na `atividade.json`), e desenhar só o anel por cima. Trocar o cursor exige gravar sem cursor + log do mouse (Screen Studio faz isso internamente).
- **Links:** [OpenScreen cursorRenderer.ts](https://github.com/siddharthvaddem/openscreen), [Screen Studio (review do cursor)](https://daveswift.com/screen-studio/), [Cursorful](https://cursorful.com/install).

### 2.5 Elemento da UI que "levanta" (recorte vira card 3D)
- **Como é:** o botão/campo é recortado do quadro, sobe na direção da câmera (escala + sombra + leve giro 3D), o resto escurece; depois pousa de volta no mesmo lugar (ou vira a cena seguinte, item 23 do `nivel.md`).
- **Ajuda:** **o** campo da aula (o "5 min" da meta, o filtro "SLA status", o botão "Salvar acionador"); quando o elemento é pequeno e o nome dele é a palavra-chave.
- **Atrapalha:** usar em todo clique (perde o peso); levantar um painel inteiro (vira slide); recorte com borda torta (mostra "colagem"); levantar e o zoom de fundo continuar andando.
- **Números [proposta]:** escala 1 → 1,10–1,18; sobe 10–16 px; `rotateX` 10° → 0 e `rotateY` −6° → 0 com `perspective: 1200px`; sombra cresce de `0 2px 6px` para `0 28px 60px rgba(0,0,0,.45)`; fundo escurece até 0,5; entrada 0,45–0,55 s (expo.out, sem quique — `nivel.md` 35), platô ≥ tempo de leitura do rótulo, pouso 0,3 s (ease-in). Folga do recorte 6–10 px, raio igual ao do elemento (CRM: 6–8 px na tela, ×escala do zoom). No máximo 1 a cada ~30 s.
- **Links:** [3D pop-up card transition (template AE)](https://autoae.online/hooks/3d-pop-up-card-transition-k34llxw9), [SaaS explainer em AE (Vane Motion)](https://learn-python.programiz.com/w/EVZ59GZ04URrJVa/🔥how-to-create-a-saas-explainer-ad-in-after-effects-|-full-tutorial-from-scratch/pages/), Rotato (mockups 3D de tela) [rotato.app](https://rotato.app).

### 2.6 Seta / linha que liga elemento a rótulo (callout)
- **Como é:** linha curva que se desenha da etiqueta até o alvo, ponta ou ponto no final; etiqueta curta (1–4 palavras).
- **Ajuda:** dar **nome** a algo da tela que a fala chama de "esse aqui" ("SLA status = o gatilho"); ligar duas coisas ("laranja = vencimento em breve").
- **Atrapalha:** seta comprida atravessando a tela (o olho perde a origem), seta cruzando texto, várias setas ao mesmo tempo. Boucheix & Lowe (2010): **setas** guiaram pior do que cor que se espalha pelo próprio objeto, e qualquer cue só funcionou **sincronizado** com o evento — preferir destacar o próprio elemento e usar a seta só para ligar um rótulo.
- **Números [proposta]:** traço 4–5 px em 1080p (Recordly usa 4 **[medido]**); curva com flecha de 15–25 % do comprimento; comprimento 80–300 px (≤ 1/4 da largura); desenha em 0,3–0,45 s (`stroke-dashoffset`, ease-out), ponta aparece nos últimos 20 %; etiqueta entra 0,1 s depois da linha chegar; a ponta para 8–12 px antes do alvo (não encosta). Texto do rótulo: Recordly usa 30–32 px **[medido]**; nosso mínimo em 1080p: 26–30 px no rótulo mono e 36–48 px na palavra (conferir com a skill hierarquia-visual).
- **Links:** [Boucheix & Lowe 2010 (PDF)](https://lead.ube.fr/wp-content/uploads/2023/09/000191-an-eye-tracking-comparison-of-external-pointing-cues-and-internal-continuous-cues-in-learning-with-complex-animations.pdf), [Recordly AnnotationOverlay/ArrowSvgs](https://github.com/webadderall/Recordly).

### 2.7 Rótulos numerados de passo (1, 2, 3)
- **Como é:** bolinha numerada que cai no lugar de cada clique da sequência; as anteriores ficam, mais apagadas; some tudo quando a tela muda.
- **Ajuda:** sequência que o aluno vai repetir sozinho (configurar, salvar). Vira "mapa" da tela — o aluno pausa e confere. É a lógica do Arcade/Supademo (cada clique = um passo).
- **Atrapalha:** numerar coisa que não é sequência; números que mudam de lugar com o zoom; mais de 5 na mesma tela.
- **Números [proposta]:** bolinha 44–52 px, número 24–28 px pesado (Archivo 800 ou JetBrains Mono 700, `tabular-nums`); entra com overshoot curto (back 1,6, 0,35 s — selo pequeno pode quicar, `nivel.md` 35) **na palavra ou no clique** (o que vier primeiro, até 0,2 s antes); passo anterior cai para 55 % de opacidade; no máximo 4–5 visíveis; ancorado no canto superior esquerdo do alvo, deslocado 12 px para fora.
- **Base:** Mayer, segmentação (d = 0,67) e pré-treino (d = 0,78). Arcade: cada clique vira um passo **[doc]**.
- **Links:** [Arcade — hotspots e callouts](https://docs.arcade.software/kb/build/interactive-demo/edit/hotspots-and-callouts), [Supademo — hotspots](https://docs.supademo.com/editing/hotspots).

### 2.8 Contador / chip de estado ao vivo
- **Como é:** número que corre junto com a tela (cronômetro do SLA, contagem regressiva "romper daqui 45 s") ou chip de estado que troca de cor.
- **Ajuda:** espera real na gravação (o teste de 45 s) — vira suspense em vez de tempo morto; prova de que o sistema funcionou.
- **Atrapalha:** contador inventado que não bate com o da tela; dois relógios diferentes ao mesmo tempo.
- **Números [casa + proposta]:** `SeloStatus` já existe (troca na palavra, overshoot 0,35 s). Número com `tabular-nums`, troca de dígito em "rolagem" de 0,18 s; contador **sempre derivado do tempo editado** (se houver corte dentro da espera, ele salta junto — melhor: não cortar dentro da contagem, ou mostrar "…" no salto).

### 2.9 Antes / depois
- **Como é:** o mesmo enquadramento em dois estados (5 min → 10 min; "contar todas" → "contar só as selecionadas"), por cortina (wipe) ou troca no lugar.
- **Ajuda:** mudança de configuração cujo efeito não se vê na hora.
- **Atrapalha:** enquadramentos diferentes (o olho procura onde está a diferença); antes/depois rápido demais.
- **Números [proposta]:** mesmo quadro, mesma escala; cada estado ≥ 1,5 s; cortina 0,5–0,6 s (`wipe()`), linha da cortina 3 px na cor de destaque; diferença marcada com holofote leve só no que mudou.

### 2.10 Texto digitado sobreposto (keystroke / campo ampliado)
- **Como é:** o que foi digitado aparece grande num chip perto do campo (ou atalhos de teclado num "pill" embaixo).
- **Ajuda:** nome de campo, valor ou expressão que o aluno vai copiar ("Conversations SLA", "Estamos verificando?").
- **Atrapalha:** repetir em texto tudo o que a voz diz (redundância); dados de cliente (regra do estúdio).
- **Números:** Screenize **[medido]**: chip de tecla fica 1,5 s, entra em 0,15 s, sai em 0,3 s. Nosso **[proposta]**: digitação reproduzida com `typed()` na velocidade real ou 25–35 caracteres/s, cursor de texto piscando 1 Hz, chip fica até 1 s depois do último caractere.

### 2.11 Transições entre telas (match cut de UI, morph, pan contínuo)
- **Como é:** em vez de corte seco entre duas páginas do CRM, o elemento clicado "vira" a tela seguinte (cresce até ocupar o quadro), ou a câmera desliza da área do clique para a área nova; tela de carregamento sai.
- **Ajuda:** navegação entre menus (Conversas → Automações → Fluxo) — o aluno não perde onde está.
- **Atrapalha:** transição de efeito em toda troca (aula, não anúncio); fusão longa (dois textos sobrepostos ilegíveis).
- **Números:** OpenScreen **[medido]**: pan conectado 1,0 s quando o próximo zoom vem em até 1,5 s. Nosso **[casa]**: fusão 0,25 s nas emendas; doutrina "nunca fusão entre tela e cena; 2–3 tipos de transição por vídeo". **[proposta]** match cut de UI: o recorte do item de menu cresce 1 → 1,2 em 0,2 s (ease-in, desfoque até 12 px) no clique; a tela nova entra 1,08 → 1 em 0,35 s a partir do mesmo ponto. Spinner/carregamento > 0,5 s: corta (já acontece na aula SLA aos ~244 s, tela branca com spinner).

### Bônus — desfoque de dado sensível
Supademo "Smart Blur" detecta e-mail, telefone, valores e nomes durante a gravação **[doc]**. Para nós: `desfoque` como mais um tipo de anotação (retângulo no tempo editado, desfoque 12–18 px + véu 0,2), obrigatório onde aparecer cliente real (regra do estúdio). [Supademo Smart Blur](https://docs.supademo.com/article/158-smart-blur-and-auto-redaction).

---

## 3. Regras de clareza — checklist para a revisão (revisao-video)

Números de Mayer (2021, tamanho de efeito mediano, d de Cohen): coerência 0,86 · sinalização 0,69 · contiguidade espacial 0,82 · contiguidade temporal 1,31 · segmentação 0,67 · pré-treino 0,78 · modalidade 1,00 · personalização 1,00 ([tabela em "The Future of Multimedia Learning"](https://edtechbooks.org/docx/10349)). Meta-análises: sinalização r = 0,17, efeito maior para quem tem **pouco conhecimento prévio** ([Richter, Scheiter & Eitel](https://psycharchives.org/handle/20.500.12034/2019)); cueing g = 0,53 em retenção e 0,36 em transferência ([meta-análise do Acta Psychologica Sinica, 2016](https://journal.psych.ac.cn/xlxb/CN/Y2016/V48/I5/540)). Para vídeo: sinalizar, segmentar, enxugar e casar modalidade com conteúdo ([Brame 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/)); vídeos curtos e informais prendem mais ([Guo, Kim & Rubin 2014](https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf)).

Cada item vira **pergunta de revisão** (sim/não), e os marcados com ⏱ podem ser medidos por script a partir de `anotacoes.json` + `palavras-final.json`:

**Sinalização (o olho sabe onde olhar)**
- [ ] ⏱ No máximo **1 destaque ativo** por vez (holofote, lupa, elemento que levanta). Exceção: passos numerados da mesma sequência, até 4–5.
- [ ] Cada destaque marca o que a **fala** está nomeando naquele instante — nunca algo que a fala não citou.
- [ ] O destaque é **no próprio elemento** (borda, cor, levantar); seta só para ligar rótulo (Boucheix & Lowe).
- [ ] Momento-chave da aula tem destaque (configuração que o aluno precisa repetir, valor numérico, botão de salvar).

**Contiguidade temporal (junto da palavra)**
- [ ] ⏱ Entrada da anotação entre **−0,3 s e +0,2 s** da palavra-gatilho (`palavras-final.json`). Mais cedo que −0,3 s "adivinha"; mais tarde que +0,3 s parece atrasado.
- [ ] ⏱ Saída quando a fala troca de alvo (≤ 0,5 s depois da última palavra relacionada), nunca no meio de uma frase sobre o alvo.
- [ ] ⏱ Platô de leitura ≥ `máx(1 s; 0,5 + 0,33 s × palavras do rótulo)` (`nivel.md` 36).

**Contiguidade espacial (perto do alvo)**
- [ ] ⏱ Rótulo a ≤ 300 px do alvo em 1080p; seta ≤ 1/4 da largura e sem cruzar texto.
- [ ] ⏱ Nenhuma anotação sobre a **câmera do apresentador**, o selo de status, o capítulo ou a borda de 48 px.
- [ ] O rótulo usa o **mesmo nome que a tela** ("SLA status", não "status do SLA") — o aluno vai procurar esse texto.

**Coerência (tirar o que não ensina)**
- [ ] Nenhuma anotação decorativa (brilho, partícula, seta "só porque sim").
- [ ] Tempo morto da tela (carregamento, procura do menu) cortado ou coberto — nunca enfeitado.
- [ ] ⏱ Média ≤ 1 anotação a cada 15 s no trecho de demonstração; em trecho conceitual (sem tela), zero.

**Redundância e modalidade (voz explica, texto nomeia)**
- [ ] Texto na tela tem 1–4 palavras (nome, valor, estado). Nunca a frase falada inteira (isso é legenda, e só se o dono pedir).
- [ ] Número dito = número escrito = número na tela do CRM (20 minutos, 45 s).

**Segmentação e pré-treino**
- [ ] Cada bloco de demonstração começa com o "mapa" (onde estamos: capítulo + holofote no menu) e termina com o resultado visível.
- [ ] Sequência de passos ≥ 3 cliques ganha números; o último passo ("Salvar") é o mais forte.

**Legibilidade e nitidez**
- [ ] ⏱ Zoom de fundo ≤ 1,6× em captura 1080p (≤ 2,0× em 1440p, ≤ 2,5× em 4K); lupa e elemento que levanta recortados do **bruto**.
- [ ] Contraste do rótulo ≥ 4,5:1 (WCAG) contra o fundo real (conferir com `conferir_hierarquia.mjs` num quadro exportado).
- [ ] Destaque usa **uma** cor (a do tema; no SLA, as cores do estado: laranja/vermelho/verde só para estado).

**Dados**
- [ ] Nenhum nome/telefone/conversa de cliente real visível em lupa ou elemento ampliado (ampliar torna legível o que antes não era).

---

## 4. Receitas de implementação no nosso pipeline

### 4.1 Onde a anotação mora: `edicao.json` → `"anotacoes"`
Tudo no **tempo editado** (o mesmo de `motions`, `capitulos`, `selos`), e o retângulo do alvo em **coordenadas do bruto normalizadas 0–1** (a verdade não muda quando o zoom muda). O gerador converte para pixels da saída quadro a quadro.

```json
"anotacoes": [
  { "tipo": "holofote", "ini": 55.6, "fim": 59.4, "alvo": [0.188, 0.437, 0.276, 0.071], "palavra": "metas" },
  { "tipo": "levanta",  "ini": 56.9, "fim": 59.4, "alvo": [0.188, 0.469, 0.115, 0.035], "rotulo": "VENCE EM BREVE · 5 MIN", "congelar": true },
  { "tipo": "lupa",     "ini": 221.0, "fim": 229.6, "alvo": [0.82, 0.20, 0.08, 0.04], "amp": 2.2, "onde": [1560, 420] },
  { "tipo": "passo",    "ini": 273.6, "fim": 294.5, "n": 1, "alvo": [0.30, 0.37, 0.30, 0.03] },
  { "tipo": "seta",     "ini": 136.4, "fim": 140.0, "alvo": [0.64, 0.52, 0.33, 0.045], "rotulo": "O GATILHO", "de": [980, 470] }
]
```
- `alvo` = `[x, y, w, h]` no bruto (0–1). `onde`/`de` = posição do rótulo/lupa em px da saída 1920×1080 (escolhida longe da câmera).
- `ini` sai da palavra: `ini = t_palavra − 0,15` (ou −0,3 para holofote, que precisa chegar antes do olho).

### 4.2 A ponte entre bruto e camada de tela: `vista.json` (uma fonte da verdade)
A camada de tela (`render.py --camada-tela`) já tem o zoom aplicado; a função `vista(t)` do `render.py` dá o retângulo visível do bruto `(x0, y0, w)` em cada instante (16:9 nos dois lados, então `h = w`). **Proposta:** o `render.py --camada-tela` grava também `vista.json` = `[[x0, y0, w], …]` **por quadro editado** (9 028 quadros na aula SLA ≈ 250 KB). O Remotion lê esse arquivo — não reimplementa a curva do zoom (evita escorregar 1 quadro).

Conversão bruto → saída no quadro `f`:
```
X = (u − x0[f]) / w[f] × 1920      Y = (v − y0[f]) / w[f] × 1080      escala_do_zoom = 1 / w[f]
```
- Se a anotação dura e o zoom anda por baixo, o retângulo acompanha (holofote "grudado").
- **Melhor ainda para lupa e elemento que levanta:** segurar o zoom parado durante a anotação (`zoom_fixo` com o valor atual) — o `anotar.py` pode escrever isso sozinho.
- Câmera fora do lugar (`camera_fora`) e trechos de motion: anotação não entra (a camada de tela está escondida).

### 4.3 Recortar o elemento da UI com nitidez
1. **Achar o quadro do bruto:** tempo editado → quadro do bruto com os inteiros do `edl.json` (`q_in + (k − q0)·vel`, igual a `trecho_q()` do `render.py`).
2. **Recortar do `bruto-30p.mov`, não da camada de tela** (a de tela já está ampliada 1,6×; ampliar de novo dá pixel duplo). Folga de 8 px, escala Lanczos direto para o tamanho final (tamanho na tela × escala do zoom × escala do "levantar"), saída H.264/PNG BT.709 faixa limitada (o mesmo cuidado do `camera.mp4`, que evitou a cor lavada):
   - elemento parado (campo, botão): **PNG congelado** do quadro da palavra → `public/anot/NN.png` (mais nítido, nada treme);
   - elemento que muda (cronômetro "43s"): **mp4 recortado** → `public/anot/NN.mp4` com o mesmo `trimBefore` do trecho (mesma regra de sincronia da câmera).
3. **Buraco embaixo:** enquanto o card está levantado, o lugar original fica com o próprio quadro (não precisa tapar), porque o véu escuro cobre tudo menos o card; ao pousar, o card volta exatamente para `X, Y` do quadro atual.

### 4.4 Achar o alvo sozinho: `scripts/anotar.py` (proposta)
Entrada: `edicao.json`, `edl.json`, `atividade.json`, `palavras-final.json`, `bruto-30p.mov`. Saída: `fonte/anotacoes-sugeridas.json` + folha de fotos com cada sugestão desenhada (aprovar antes de renderizar).

1. **Palavras-gatilho** na transcrição (tempo editado):
   - dêiticos: "aqui", "esse/essa", "isso", "olha", "dá uma olhada" → holofote (o alvo vem da tela, passo 2);
   - verbos de ação: "clico", "seleciono", "marco", "mudo para", "coloco", "salvo", "abro" → passo numerado / clique;
   - nomes que existem na tela: OCR (`tesseract` está instalado em `/opt/homebrew/bin`) no quadro do bruto, comparar com 1–3 palavras da fala (sem acento, minúsculas, distância de edição ≤ 1) → seta + rótulo ou elemento que levanta;
   - números ditos ("5 minutos", "45 segundos", "20") → antes/depois ou contador se o mesmo número aparece no OCR.
2. **Caixa onde a tela mexe:** `atividade.json` (`caixa` em 0–1 a cada 0,25 s do bruto) na janela `[t − 0,5; t + 1,0]`. É grossa (384×216, percentis 5–95) → refinar em resolução cheia: diferença entre os quadros `t − 0,25` e `t + 0,5`, limiar 12, dilatar 6 px, componentes conectados, maior componente dentro da caixa grossa.
3. **Cursor e clique (sem telemetria):** procurar a seta do macOS no quadro (`cv2.matchTemplate`, 2 tamanhos, limiar 0,8); clique = surto de diferença em raio de 60 px do cursor nos 0,1–0,3 s seguintes (anel de foco do CRM, rádio marcado, menu abrindo).
4. **Encaixar na borda do componente:** em volta do ponto (cursor/OCR), Canny + `findContours` + `approxPolyDP` → o menor retângulo de 4 lados que contém o ponto e tem altura 24–80 px (campo/botão do CRM) ou largura até 60 % da tela (bloco). Folga 8 px.
5. **Escolher o tipo:** (dêitico + bloco grande) → holofote; (nome dito + elemento pequeno) → levanta ou seta+rótulo; (verbo de ação em sequência ≥ 3 na mesma tela) → passos; (número + chip que muda) → lupa/contador.
6. **Orçamento e conflitos:** remove sugestões a < 8 s da anterior (exceto passos), dentro de motions/capítulos (±0,5 s), e as que cairiam sobre a câmera (`cameras` do `edicao.json` convertido para a saída). Confiança = OCR bate + componente bem fechado + clique detectado; abaixo de 0,6 vai só para a folha, não para o JSON.
7. **Saída também escreve `zoom_fixo`** durante lupa/levanta (segurar o zoom atual).

### 4.5 Componentes Remotion (esboço, não roda — encaixa no `componentes.tsx`)
Convenções iguais às do arquivo atual: `escala` (E) = saída/1920, `fontes(tema)`, `clamp`, curvas `p4out`/`p4in`/`expoOut`. Todos recebem o alvo já em px da saída por um hook que lê `vista.json`.

```tsx
// ---------- ANOTAÇÕES POR CIMA DA TELA (esboço) ----------
// alvo no bruto (0–1) → px da saída no quadro atual, pela vista gravada pelo render.py (--camada-tela → vista.json)
import vistaJson from "../public/vista.json"; // [[x0, y0, w], ...] por quadro EDITADO
type R = { x: number; y: number; w: number; h: number };
const W = 1920, H = 1080;
export const useAlvo = (alvo: [number, number, number, number], fps: number, desde: number): R => {
  const f = useCurrentFrame() + Math.round(desde * fps);            // quadro absoluto do vídeo editado
  const [x0, y0, w] = (vistaJson as number[][])[Math.min(f, vistaJson.length - 1)];
  const [u, v, uw, vh] = alvo;
  return { x: ((u - x0) / w) * W, y: ((v - y0) / w) * H, w: (uw / w) * W, h: (vh / w) * H };
};
const entraSai = (t: number, dur: number, ent = 0.4, sai = 0.3) =>
  Math.min(interpolate(t, [0, ent], [0, 1], { ...clamp, easing: expoOut }), 1 - interpolate(t, [dur - sai, dur], [0, 1], { ...clamp, easing: p4in }));

// HOLOFOTE: véu escuro com um buraco arredondado + borda de destaque
export const Holofote: React.FC<{ r: R; dur: number; escala: number; cor?: string; veu?: number; folga?: number; raio?: number }> =
  ({ r, dur, escala: E, cor = "#e8b867", veu = 0.6, folga = 12, raio = 12 }) => {
  const t = useCurrentFrame() / useVideoConfig().fps; const v = entraSai(t, dur, 0.4, 0.3);
  const s = 1.06 - 0.06 * interpolate(t, [0, 0.5], [0, 1], { ...clamp, easing: expoOut });
  const x = (r.x - folga) * E, y = (r.y - folga) * E, w = (r.w + 2 * folga) * E, h = (r.h + 2 * folga) * E;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {/* box-shadow gigante = véu; feather pelo blur da sombra */}
      <div style={{ position: "absolute", left: x, top: y, width: w, height: h, borderRadius: raio * E, transform: `scale(${s})`,
        boxShadow: `0 0 0 ${4 * E * v}px ${cor}, 0 0 ${24 * E}px ${6000 * E}px rgba(10,10,14,${(veu * v).toFixed(3)})` }} />
    </AbsoluteFill>
  );
};

// LUPA: recorte do BRUTO (png/mp4 em public/anot) ampliado, ligado à origem por uma linha
export const Lupa: React.FC<{ r: R; src: string; video?: boolean; trimBefore?: number; onde: [number, number]; diam?: number; amp?: number; dur: number; escala: number; cor?: string }> =
  ({ r, src, video, trimBefore = 0, onde, diam = 320, amp = 2.2, dur, escala: E, cor = "#e8b867" }) => {
  const t = useCurrentFrame() / useVideoConfig().fps; const v = entraSai(t, dur, 0.45, 0.3);
  const ox = r.x + r.w / 2, oy = r.y + r.h / 2;                      // origem (o detalhe na tela)
  const cx = ox + (onde[0] - ox) * v, cy = oy + (onde[1] - oy) * v;   // a lupa sai da origem e vai para o lugar livre
  const d = diam * (0.6 + 0.4 * v);
  const lado = Math.max(r.w, r.h) * amp;                              // tamanho do recorte ampliado dentro do círculo
  return (
    <AbsoluteFill style={{ pointerEvents: "none", opacity: Math.min(1, v * 1.5) }}>
      <svg width="100%" height="100%" style={{ position: "absolute" }}>
        <line x1={ox * E} y1={oy * E} x2={cx * E} y2={cy * E} stroke={cor} strokeWidth={3 * E} strokeDasharray={`${6 * E} ${6 * E}`} opacity={0.8} />
        <rect x={(r.x - 6) * E} y={(r.y - 6) * E} width={(r.w + 12) * E} height={(r.h + 12) * E} rx={8 * E} fill="none" stroke={cor} strokeWidth={3 * E} />
      </svg>
      <div style={{ position: "absolute", left: (cx - d / 2) * E, top: (cy - d / 2) * E, width: d * E, height: d * E, borderRadius: "50%", overflow: "hidden",
        background: "#fff", boxShadow: `0 0 0 ${4 * E}px ${cor}, 0 ${18 * E}px ${44 * E}px rgba(0,0,0,.45)` }}>
        {video
          ? <Video src={src} trimBefore={trimBefore} muted style={{ position: "absolute", left: "50%", top: "50%", width: lado * E, transform: "translate(-50%,-50%)" }} />
          : <Img src={src} style={{ position: "absolute", left: "50%", top: "50%", width: lado * E, transform: "translate(-50%,-50%)" }} />}
      </div>
    </AbsoluteFill>
  );
};

// ELEMENTO QUE LEVANTA: recorte congelado do bruto vira card 3D; véu escurece o resto; pousa no mesmo lugar
export const ElementoQueLevanta: React.FC<{ r: R; src: string; dur: number; escala: number; sobe?: number; raio?: number; rotulo?: string; tema?: string; cor?: string }> =
  ({ r, src, dur, escala: E, sobe = 1.14, raio = 8, rotulo, tema, cor = "#e8b867" }) => {
  const F = fontes(tema);
  const t = useCurrentFrame() / useVideoConfig().fps;
  const k = interpolate(t, [0, 0.5], [0, 1], { ...clamp, easing: expoOut });            // sobe sem quique
  const p = interpolate(t, [dur - 0.3, dur], [0, 1], { ...clamp, easing: p4in });        // pousa
  const a = k * (1 - p);
  const folga = 8;
  return (
    <AbsoluteFill style={{ pointerEvents: "none", perspective: 1200 * E }}>
      <AbsoluteFill style={{ background: `rgba(10,10,14,${(0.5 * a).toFixed(3)})` }} />
      <div style={{ position: "absolute", left: (r.x - folga) * E, top: (r.y - folga) * E, width: (r.w + 2 * folga) * E, height: (r.h + 2 * folga) * E,
        borderRadius: raio * E, overflow: "hidden", transformOrigin: "50% 60%",
        transform: `translateY(${-14 * a * E}px) scale(${1 + (sobe - 1) * a}) rotateX(${10 * (1 - k)}deg) rotateY(${-6 * (1 - k)}deg)`,
        boxShadow: `0 ${(2 + 26 * a) * E}px ${(6 + 54 * a) * E}px rgba(0,0,0,${0.15 + 0.3 * a}), 0 0 0 ${2 * a * E}px ${cor}` }}>
        <Img src={src} style={{ width: "100%", height: "100%" }} />
      </div>
      {rotulo && (
        <div style={{ position: "absolute", left: r.x * E, top: (r.y + r.h + 22) * E, opacity: interpolate(t, [0.25, 0.5], [0, 1], clamp) * (1 - p),
          transform: `translateY(${(1 - k) * 12 * E}px)`, font: `700 ${28 * E}px ${F.ui}`, letterSpacing: F.ls, color: "#f4f3f8",
          background: "rgba(13,12,20,.86)", padding: `${8 * E}px ${16 * E}px`, borderRadius: 6 * E, borderLeft: `${4 * E}px solid ${cor}` }}>{rotulo}</div>
      )}
    </AbsoluteFill>
  );
};

// SETA + RÓTULO: linha curva que se desenha do rótulo até o alvo (para 10 px antes), rótulo entra depois
export const Seta: React.FC<{ r: R; de: [number, number]; rotulo: string; dur: number; escala: number; cor?: string; tema?: string; curva?: number }> =
  ({ r, de, rotulo, dur, escala: E, cor = "#e8b867", tema, curva = 0.2 }) => {
  const F = fontes(tema);
  const t = useCurrentFrame() / useVideoConfig().fps; const sai = 1 - interpolate(t, [dur - 0.3, dur], [0, 1], { ...clamp, easing: p4in });
  const tx = r.x + r.w / 2, ty = r.y + r.h / 2;
  const ang = Math.atan2(ty - de[1], tx - de[0]); const dist = Math.hypot(tx - de[0], ty - de[1]);
  const fim: [number, number] = [tx - Math.cos(ang) * (Math.max(r.w, r.h) / 2 + 10), ty - Math.sin(ang) * (Math.max(r.w, r.h) / 2 + 10)];
  const mx = (de[0] + fim[0]) / 2 - Math.sin(ang) * dist * curva, my = (de[1] + fim[1]) / 2 + Math.cos(ang) * dist * curva;
  const d = `M ${de[0] * E} ${de[1] * E} Q ${mx * E} ${my * E} ${fim[0] * E} ${fim[1] * E}`;
  const k = interpolate(t, [0, 0.4], [0, 1], { ...clamp, easing: p4out });                 // desenha
  const L = dist * 1.15 * E;
  return (
    <AbsoluteFill style={{ pointerEvents: "none", opacity: sai }}>
      <svg width="100%" height="100%" style={{ position: "absolute" }}>
        <path d={d} fill="none" stroke={cor} strokeWidth={4.5 * E} strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - k)} />
        <circle cx={fim[0] * E} cy={fim[1] * E} r={7 * E * interpolate(t, [0.32, 0.45], [0, 1], clamp)} fill={cor} />
      </svg>
      <div style={{ position: "absolute", left: de[0] * E, top: de[1] * E, transform: `translate(-50%, -110%) translateY(${(1 - interpolate(t, [0.1, 0.45], [0, 1], { ...clamp, easing: p4out })) * 14 * E}px)`,
        opacity: interpolate(t, [0.1, 0.4], [0, 1], clamp), font: `700 ${28 * E}px ${F.ui}`, letterSpacing: F.ls, color: "#16141f",
        background: cor, padding: `${8 * E}px ${16 * E}px`, borderRadius: 6 * E, whiteSpace: "nowrap" }}>{rotulo}</div>
    </AbsoluteFill>
  );
};

// RÓTULO DE PASSO: bolinha numerada no canto do alvo; passos anteriores apagam para 55 %
export const RotuloPasso: React.FC<{ r: R; n: number; dur: number; proximoEm?: number; escala: number; cor?: string; tema?: string }> =
  ({ r, n, dur, proximoEm, escala: E, cor = "#e8b867", tema }) => {
  const F = fontes(tema);
  const t = useCurrentFrame() / useVideoConfig().fps;
  const k = interpolate(t, [0, 0.35], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.6)) });
  const apaga = proximoEm === undefined ? 1 : interpolate(t, [proximoEm, proximoEm + 0.3], [1, 0.55], clamp);
  const sai = 1 - interpolate(t, [dur - 0.25, dur], [0, 1], clamp);
  const D = 48;
  return (
    <div style={{ position: "absolute", left: (r.x - D * 0.6) * E, top: (r.y - D * 0.6) * E, width: D * E, height: D * E, borderRadius: "50%",
      background: cor, color: "#16141f", display: "grid", placeItems: "center", font: `800 ${26 * E}px ${F.ui}`, fontVariantNumeric: "tabular-nums",
      transform: `scale(${k})`, opacity: apaga * sai, boxShadow: `0 ${8 * E}px ${20 * E}px rgba(0,0,0,.35), 0 0 0 ${3 * E}px rgba(255,255,255,.9)` }}>{n}</div>
  );
};

// CLIQUE: anel no ponto do clique detectado (o cursor já está na gravação)
export const AnelClique: React.FC<{ x: number; y: number; escala: number; cor?: string }> = ({ x, y, escala: E, cor = "#ffffff" }) => {
  const t = useCurrentFrame() / useVideoConfig().fps; const k = interpolate(t, [0, 0.35], [0, 1], { ...clamp, easing: expoOut });
  return <div style={{ position: "absolute", left: x * E, top: y * E, width: 56 * E, height: 56 * E, borderRadius: "50%", border: `${3 * E}px solid ${cor}`,
    transform: `translate(-50%,-50%) scale(${0.3 + 0.9 * k})`, opacity: 1 - interpolate(t, [0.1, 0.35], [0, 1], clamp), boxShadow: `0 0 ${12 * E}px rgba(0,0,0,.35)` }} />;
};
```
O `gerar_remotion.py` passa cada item de `anotacoes` para um `<Sequence from={round(ini·fps)} durationInFrames={round((fim−ini)·fps)}>` com o componente certo — um nó JSX por anotação, editável no Studio, como já é feito com capítulos e selos. (Faltam `Img` em `import { Img } from "remotion"` e o `vista.json` no `public/`.)

### 4.6 Ordem das camadas no Remotion
`Tela` → **anotações que escurecem** (Holofote, véu do ElementoQueLevanta) → **anotações que flutuam** (card levantado, Lupa, Seta, RotuloPasso, AnelClique) → Câmera (`MolduraMovel`) → `SeloStatus` / `Capitulo` → Cenas. A câmera fica por cima do véu (o rosto nunca escurece).

---

## 5. Três exemplos aplicados à aula SLA (v2)
Tempos no vídeo editado (`fonte/palavras-final.json`); posições medidas nos quadros da `aula-sla-v2-tela.mp4`. Zoom no momento vem do `zoom.json`; câmera do apresentador: canto inferior direito até ~2:02 (quadros 1390,746 → 1881,1022 do bruto), canto inferior esquerdo depois (55,754 → 546,1030).

### Exemplo 1 — "A meta está definida como vencimento em breve para 5 minutos" (55,6–62,5 s)
- **Situação:** página "Configurações de SLA" inteira em 1× (zoom de 57,0 a 61,0 s = 1,0), com 8 grupos de opções parecidos; a fala diz "as metas", "dá uma olhada aqui", "5 minutos", "símbolo laranja". Hoje o aluno precisa caçar o "5" entre dezenas de campos.
- **Anotações:**
  1. `holofote` no bloco "Definir metas de SLA" (saída ≈ x 352–900, y 410–550) em **55,6 s** ("Dá uma olhada aqui"), véu 0,55.
  2. `levanta` do campo "5 | Mins" (saída ≈ x 362–580, y 506–544) em **56,9 s** (palavra "5" em 57,04), PNG congelado do bruto, sobe 1,16×, rótulo mono embaixo **"VENCE EM BREVE · 5 MIN"**.
  3. Em **58,8 s** ("símbolo **laranja**"): o rótulo troca o filete para laranja (#f59e0b) e um ponto laranja pulsa sobre a bolinha "SLA com vencimento em breve" (saída ≈ x 362–378, y 478–494) — cor do **estado**, a mesma do `SeloStatus`.
  4. Pousa em **60,7 s**, antes do zoom de 61,0 s para a conversa ("esse lead já está laranja" em 60,98) — o laranja do rótulo "passa" para o lead (continuidade de cor).
- **Por quê:** sinalização + contiguidade temporal na palavra; o elemento é pequeno e o nome dele é a palavra-chave.

### Exemplo 2 — Teste ao vivo: "vai romper daqui 45 segundos" (220,4–236,5 s)
- **Situação:** conversa aberta com zoom 1,47–1,6×; o cronômetro do SLA é um chip minúsculo "43s" no cabeçalho da conversa (saída ≈ x 1594–1732, y 224–264, com zoom 1,6) — a prova do teste inteira está ali. O `SeloStatus` já narra os estados no alto, ao centro (y 96–166).
- **Anotações:**
  1. `lupa` no chip em **220,3 s** ("se o meu SLA aqui **romper**" 220,43), mp4 recortado do bruto (o número corre), ampliação 2,2×, círculo de 300 px em **(1560, 470)** — área vazia da conversa, longe da câmera (canto inferior esquerdo) e abaixo do selo; linha tracejada até o chip.
  2. Em **223,1 s** ("daqui **45** segundos"): anel de destaque no número dentro da lupa (a fala e o número da tela batem: o aluno vê o mesmo 45 contando).
  3. Em **228,7 s** ("oficialmente **vencida**"): o anel da lupa vira vermelho no mesmo quadro em que o chip do CRM fica vermelho e o selo troca para "vencido · automação disparou" (tudo na mesma palavra, uma cor só).
  4. Lupa sai em **230,0 s**; em **235,1 s** ("Igual **mandou**") `holofote` na mensagem automática "Estamos verificando?" chegando na conversa, até 238,0 s (quando o zoom volta a 1×).
- **Cuidado:** a espera tem cortes (311,5–316,9 s do bruto saíram) — o contador não pode ser desenhado por nós; a lupa mostra o número **real** da gravação. Nada de cliente real: o lead é o de teste do dono.

### Exemplo 3 — O ajuste final: "contar apenas as mensagens dos fluxos selecionados" (267,4–294,5 s)
- **Situação:** de volta às configurações, zoom 1,6× (273,5 s em 0,312/0,477; 277,5 s em 0,312/0,338), um rádio, um menu de seleção múltipla e um "não coloque este". É a sequência que o aluno vai repetir — a parte mais "copiável" da aula, logo depois do capítulo 5 (266,7–269,7 s) e do motion "A pegadinha" (258,5–266,5 s).
- **Anotações (passos numerados, câmera no canto inferior esquerdo → rótulos à direita do alvo):**
  1. **267,3 s** ("venho aqui em **configurações**"): `holofote` curto no grupo "Como as mensagens de automação… devem influenciar o SLA?" até 270,0 s.
  2. **273,5 s** ("**selecionados**" 273,72): `passo` **1** no rádio "Contar apenas as mensagens de fluxos de trabalho selecionados".
  3. **274,6 s** ("eu **seleciono**" 274,73): `passo` **2** no campo de seleção (com tags AGENDAMENTOS, LEAD GANHO, META…); o 1 apaga para 55 %.
  4. **279,8 s** ("esse aqui em específico **SLA** eu não vou colocar"): `seta` + rótulo vermelho **"SLA FICA DE FORA"** apontando para a lista aberta (não existe um item "SLA" marcado — a seta mostra a ausência); fica até 287,5 s, cobrindo o "Por quê? Porque ele não é uma automação que responde o lead".
  5. **293,2 s** ("**Salvo** e prontinho" 293,32): `passo` **3** + `AnelClique` no botão Salvar; tudo some junto em 294,5 s.
- **Por quê:** segmentação (3 passos visíveis = o mapa do que repetir), pré-treino do lugar ("configurações") e o único "não faça" da aula com a cor de erro — sem competir com o motion anterior.

### O que eu não faria na aula SLA
- Seta ou lupa durante os motions, capítulos e o selo (já há sinalização ali).
- Destaque no trecho conceitual sem tela (abertura até ~30 s, "o que seria o SLA").
- Zoom acima de 1,6× nesta gravação (captura 1080p): para o próximo tutorial, pedir ao dono **captura 1440p ou 4K** e escala do sistema em 100 % — aí a lupa e o "levantar" ficam nítidos a 2–2,5×.

---

## Fontes
- Screen Studio: [guia de zoom](https://www.screen.studio/guide/adding-editing-zooms), [auto zoom](https://screen.studio/guide/auto-zoom), [pedido de ajuste do zoom automático](https://hub.screen.studio/p/custom-settings-for-default-automatic-zoom-range), [review (cursor)](https://daveswift.com/screen-studio/)
- FocuSee: [review Hongkiat](https://hongkiat.com/blog/screen-recorder-focusee-review), [UX Planet](https://uxplanet.org/create-eye-catching-videos-with-focusee-38f22adabe53)
- Cursorful: [cursorful.com](https://cursorful.com/install) · Tella: [zoom](https://www.tella.com/docs/help/editing/add-a-zoom.md) · Arcade: [hotspots/callouts/spotlights](https://docs.arcade.software/kb/build/interactive-demo/edit/hotspots-callouts-and-spotlights), [pan & zoom](https://docs.arcade.software/kb/build/interactive-demo/edit/pan-and-zoom) (as páginas do Arcade mudaram de endereço em 16/10; se der 404, buscar no [índice](https://docs.arcade.software/kb/sitemap.md)) · Supademo: [blur & annotate](https://docs.supademo.com/customize/blur-and-annotate), [smart blur](https://docs.supademo.com/article/158-smart-blur-and-auto-redaction), [hotspots](https://docs.supademo.com/editing/hotspots) · Rotato: [rotato.app](https://rotato.app)
- Código aberto (constantes lidas no código, clonado em 16/10/2026): [OpenScreen](https://github.com/siddharthvaddem/openscreen), [Recordly](https://github.com/webadderall/Recordly), [Screenize](https://github.com/syi0808/screenize); componente Remotion de cursor: [21st.dev Zoom Follows the Click](https://21st.dev/@21st/components/zoom-follow.md)
- After Effects: [3D pop-up card transition](https://autoae.online/hooks/3d-pop-up-card-transition-k34llxw9), [SaaS explainer do zero (Vane Motion)](https://learn-python.programiz.com/w/EVZ59GZ04URrJVa/🔥how-to-create-a-saas-explainer-ad-in-after-effects-|-full-tutorial-from-scratch/pages/)
- Aprendizagem: [Mayer — tabela de efeitos (The Future of Multimedia Learning)](https://edtechbooks.org/docx/10349), [Cambridge Handbook — coerência, sinalização, redundância, contiguidade](https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/C98AB3A6CE760DD63C048936EA0B3B44), [meta-análise de sinalização (dados)](https://psycharchives.org/handle/20.500.12034/2019), [meta-análise de cueing](https://journal.psych.ac.cn/xlxb/CN/Y2016/V48/I5/540), [Boucheix & Lowe 2010](https://lead.ube.fr/wp-content/uploads/2023/09/000191-an-eye-tracking-comparison-of-external-pointing-cues-and-internal-continuous-cues-in-learning-with-complex-animations.pdf), [de Koning et al.](https://learntechlib.org/p/72972), [EMME](https://link.springer.com/doi/10.1007/s10648-023-09731-7), [Brame 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/), [Guo, Kim & Rubin 2014](https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf)
- Canais (Fireship, Theo, Kevin Powell, Ali Abdaal): não achei documentação escrita dos números de edição deles; o que vale deles (zoom em código, corte seco no resultado, destaque de uma linha por vez) já está coberto pelas técnicas 2.1, 2.2 e 2.11 — conferir assistindo antes de citar número.
