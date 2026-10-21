# 03 — A gramática do editor: qual recurso usar em cada frase

Pedido do dono (16/10/2026): *"um editor faria um vídeo para ele não ficar sempre usando o mesmo estilo de coisa, para sempre variar no que está usando. Ex.: 'nesse momento eu vou colocar um motion, nesse aqui um card, nesse aqui eu vou jogar um textinho na tela'."*

Este estudo responde **como o editor decide**, frase por frase, entre corte seco, zoom, tela em cena, anotação, card parcial, texto de ênfase, motion em tela cheia, câmera em destaque, B-roll/print, tela dividida e respiro. Ele complementa o estudo 1 (`pesquisa/<estudo>/`): lá estão o **como** de cada recurso (`tela-em-cena.md`, `anotacoes.md`, `oficio-youtube.md`). Aqui está o **quando**.

---

## 1. Resumo em 5 linhas

1. O editor bom não varia por sorteio. Ele **lê a função de cada frase** (definição, passo, número, aviso, comparação, opinião, prova…) e cada função tem 2–3 recursos certos. A variedade **nasce do roteiro**, porque as funções mudam a cada 5–20 s. O vídeo não fica bagunçado porque **a mesma função sempre recebe o mesmo recurso** (Ali Abdaal usa o mesmo cartão para as 10 dicas; Nate Herk traz a mesma pirâmide de volta 4 vezes).
2. Os recursos formam uma **escada de intensidade**: 0 nada / corte seco → 1 zoom → 2 anotação ou texto curto → 3 card parcial ou bolha da câmera crescendo → 4 tela em cena → 5 motion em tela cheia. O degrau é proporcional ao **peso da ideia no vídeo inteiro**. O topo é escasso (≤ 1 motion por minuto). Frase de ligação fica no degrau 0, e é isso que dá contraste.
3. Medimos 5 vídeos grandes nos primeiros 4 min, com uma amostra a cada 2 s e detecção de cortes. Algo muda a cada **5–8 s** nos vídeos de rosto (Nate: 42 cortes em 4 min) e a cada **~25 s** no tutorial puro de tela (Kevin Stratvert: só 3 cortes, com o ritmo vindo do zoom e dos destaques). Quem ensina software põe o rosto em destaque só no gancho e nas opiniões. O resto é tela com destaques puxados pela fala.
4. A aula SLA v2 usou **3 recursos**: motion em tela cheia, zoom e capítulo, mais o selo do teste. O plano de exemplo (seção 5) usa **10**, sem passar de 3 chamadas por minuto, com tela encolhida em 14% do tempo de tela e nenhum recurso que não seja a base repetido em duas frases seguidas.
5. Proposta: um **passo novo na edicao-video, "mapa de recursos"**, entre o zoom e os motions. Ele gera uma tabela `fonte/mapa-recursos.md` (frase → função → recurso → porquê) com 6 regras de orçamento conferíveis. O texto está pronto na seção 6.

---

## 2. Os vídeos analisados (logs)

**Método.** Com o `yt-dlp` (já instalado) baixei os primeiros 4 min de cada vídeo em 360p, só a imagem, na pasta de rascunho da sessão (nada ficou no projeto). Depois:
- tirei um quadro a cada 2 s (120 por vídeo) e montei folhas de contato com o tempo, que eu olhei quadro a quadro;
- li a legenda automática do YouTube com tempo (a do Kevin deu erro 429, então usei os capítulos e a descrição dele);
- contei os cortes com o ffmpeg (`select=gt(scene,0.25)`). Esse método conta pouco: zoom suave e fusão não aparecem.

As porcentagens de tempo vêm da contagem das 120 amostras e são **aproximadas** (±5 pontos). Os tempos dos logs têm precisão de 2 s.

| Vídeo | Canal | Tipo | Rosto em tela cheia | Tela gravada | Motion/cartão | B-roll/print | Cortes em 4 min | Chamadas por cima/min |
|---|---|---|---|---|---|---|---|---|
| [n8n will change your life as a developer](https://www.youtube.com/watch?v=bS9R6aCVEzw) | Fireship | explicador + demo | 0% | ~62% (sempre um cartão sobre fundo escuro) | ~13% | ~25% (meme, stock) | 35 | ~3 |
| [ChatGPT Work Tutorial for Beginners](https://www.youtube.com/watch?v=mqDn-h0PJnA) | Kevin Stratvert (apresentador: David DeWinter) | tutorial puro de tela | ~7% (só no gancho) | ~93% (15% com bolha) | logo + 2 rodapés | planilhas de exemplo | **3** | ~2,3 |
| [Notion Fundamentals: What are Blocks?](https://www.youtube.com/watch?v=11AJCbZ5Xew) | Thomas Frank Explains | aula de curso | ~33% | ~63% (35% com bolha) | vinheta 3% | — | 29 | ~1 |
| [How I'd Learn n8n if I had to Start Over in 2026](https://www.youtube.com/watch?v=Fqeo8q8-nJg) | Nate Herk | explicador de rosto (no-code) | ~42% (1/3 com chips por cima) | ~6% | **~37%** | ~10% (artigo, filme, imagem) | **42** | ~6 |
| [How I Manage My Time – 10 Time Management Tips](https://www.youtube.com/watch?v=iONDebHX9qk) | Ali Abdaal | lista de dicas de rosto | ~80% | — | ~5% (cartão de capítulo) | ~10% | 28 | ~1,5 |

### 2.1 Fireship · n8n (0:00–4:00)
| Tempo | Fala (resumo) | Função | Recurso |
|---|---|---|---|
| [0:00](https://www.youtube.com/watch?v=bS9R6aCVEzw&t=0s) | "Benjamin Franklin once said: lost time is never found again" | gancho (citação) | retrato + citação em texto (cartão) |
| 0:04 | (a citação continua) | piada | o retrato vira meme (mesmo layout) |
| 0:06–0:16 | "your Gen Z boss in a mini tells you…" | exemplo/piada | B-roll de stock literal (cronômetro, escritório) |
| 0:18 | "workflows that look like this" | dêixis ("isso") | diagrama do n8n |
| 0:22 | "why spend 1 hour… when you can spend 10 hours failing to automate it" | piada | cartão de texto, com a segunda linha em vermelho |
| 0:24–0:28 | "some people pay $500/month for Zapier" | número + piada | meme (HELL, Bob Esponja com "$500") |
| 0:30–0:34 | "this guy… 'I'm building my own Zapier'" | personagem | foto + nome em caixa alta + citação |
| 0:36–0:42 | "open-source… not the sponsor" | definição + aparte | print do repositório + **carimbo "NOT SPONSORED"** |
| 0:50 | "crazy ways you can use it" | roteiro | cartão "n8n · crazy use cases" |
| 0:56 | (marca do programa) | transição | vinheta "The Code Report" + data |
| [1:00](https://www.youtube.com/watch?v=bS9R6aCVEzw&t=60s) | "what is n8n?" | pergunta/definição | logo + "?" |
| 1:02–1:06 | "like Zapier… free and open source" | definição por comparação | logo Zapier → "but free && open source" |
| 1:10–1:20 | "input trigger… pipeline of steps" | termo técnico | diagrama + **rótulo "TRIGGER" com seta à mão**, depois "AUTOMATION →" |
| 1:26–1:32 | "GitHub PR → Docker → Discord" | exemplo | diagrama de 3 nós, com o último trocando de ícone |
| 1:34–1:48 | "YouTuber… IoT… gambler" | 3 exemplos | B-roll de stock + diagrama por cima de cada um |
| 1:58 | "without writing a single line of code" | afirmação forte | carimbo "CODE NOT REQUIRED" |
| 2:06 | "even more crazy" | emoção | meme de rosto sobre o diagrama |
| 2:10–2:14 | "npx n8n" | passo | terminal em tela cheia |
| 2:20 | "built with Vue.js, by the way" | aparte | logo do Vue por cima da UI |
| 2:24 | "this is a serious channel" | piada | meme (monges) |
| 2:30–3:12 | patrocinador: escolher VPS, região, plano, cupom | passos | tela da Hostinger + **setas à mão** + rótulo "LINUX VPS" + "FIRESHIP" com seta no campo do cupom |
| 3:44 | "the first node… some type of trigger" | termo | rótulo "TRIGGER" no centro da tela |
| 3:56 | "trigger anytime my wife sends me a message" | exemplo/piada | rótulo "TRIGGER ON WIFE MESSAGE" |

**O que se aprende**
- **Todo substantivo vira imagem:** citação, pessoa, ferramenta, número. Termo técnico vira **rótulo grande em caixa alta com seta à mão sobre a própria tela** ("TRIGGER"), nunca uma cena separada.
- **Aparte vira carimbo**, como "NOT SPONSORED" e "CODE NOT REQUIRED".
- **A tela nunca ocupa o quadro inteiro.** É sempre um cartão sobre fundo escuro, ou seja, "tela em cena" permanente e discreta.
- A densidade de meme é do tom do canal. Para a cliente B não serve, mas **rótulo de termo e carimbo de aparte servem**.

### 2.2 Kevin Stratvert · ChatGPT Work (0:00–4:00)
| Tempo | Fala (pelos capítulos e pela imagem) | Função | Recurso |
|---|---|---|---|
| [0:00](https://www.youtube.com/watch?v=mqDn-h0PJnA&t=0s) | o que o ChatGPT Work faz | gancho | rosto em tela cheia, gesto |
| 0:02–0:04 | nome do produto | assunto | logo "ChatGPT Work" sobre o rosto |
| 0:06–0:12 | "hand it a whole task" | promessa mostrada | tela + bolha do rosto, com o prompt escrito |
| 0:14–0:16 | apresentação | credencial | rosto + rodapé com o nome (faixa azul) |
| 0:18–0:28 | o que você vai fazer (planilha, Drive, agendado, site) | **trailer do vídeo** | 4 resultados prontos, ~2,5 s cada, com bolha |
| 0:30–0:36 | ponte | — | rosto em tela cheia, depois transição em chicote azul |
| 0:38–0:44 | baixar o app | passo | site + rodapé "chatgpt.com/work" |
| [1:14](https://www.youtube.com/watch?v=mqDn-h0PJnA&t=74s) | aba Work | dêixis | **holofote**: escurece o resto, o seletor fica claro |
| 1:20–1:28 | "where should this chat run?" | opção/definição | **zoom de ~2,5×** no menu (texto vira título) |
| 1:36–1:44 | a pasta com 4 planilhas | exemplo/material | explorador de arquivos + Excel (B-roll da própria tela) |
| 2:04–2:10 | permissões | opção | zoom no menu |
| [2:26–2:54](https://www.youtube.com/watch?v=mqDn-h0PJnA&t=146s) | as 3 partes de um bom prompt | **enumeração** | rótulos **"Outcome", "Context", "Standard"** entrando um por um à esquerda de cada linha do prompt |
| 3:10–3:20 | o resultado | prova | planilha gerada em tela cheia |
| [3:22–3:32](https://www.youtube.com/watch?v=mqDn-h0PJnA&t=202s) | o produto que mais perde dinheiro | achado/número | zoom + **a linha "Maple Bacon −$1,267" levanta**, com o resto desfocado |
| 3:44–3:52 | conferir o período | verificação | holofote na linha do cabeçalho |

**O que se aprende**
- Num tutorial puro de tela, **o rosto só trabalha no gancho**. Depois, zero.
- **O ritmo vem do zoom e dos destaques, não de corte:** só 3 cortes em 4 min, e mesmo assim nada fica parado mais de ~20 s.
- Um destaque a cada ~25 s, **sempre um por vez**.
- A enumeração é feita **com rótulos ao lado das linhas que já estão na tela**, não com cena nova. É o modelo para "o que o gatilho faz" na aula SLA.
- **O "trailer" de 10 s com os resultados prontos** é o roteiro de uma linha feito em imagem.

### 2.3 Thomas Frank · Notion Blocks (0:00–4:00)
| Tempo | Fala | Função | Recurso |
|---|---|---|---|
| [0:00](https://www.youtube.com/watch?v=11AJCbZ5Xew&t=0s) | "we are talking about the basics of blocks" | promessa | rosto + @ das redes |
| 0:06–0:10 | "how to create them… manipulate them" | lista de ações | tela (menu "/") como B-roll sob a fala |
| 0:14–0:26 | "blocks are pretty much everything you see" | definição | panorâmica lenta pelo painel pronto |
| 0:32–0:52 | "a blob of text… an image… a page is a block" | 3 exemplos | um corte da tela para **cada substantivo** (B-roll literal da própria tela) |
| 0:54–1:14 | promessa do curso | promessa | rosto em tela cheia (20 s) |
| 1:24–1:36 | "thomasjfrank.com/fundamentals" | chamada | site + **rodapé com a URL** |
| 2:00–2:16 | "link in description" | chamada | rosto + rodapé com a URL |
| 2:18–2:22 | "let's roll that intro" | transição | vinheta da marca (3 s) |
| 2:24–3:46 | criar blocos com "/" | passos | tela + bolha, com o cursor em círculo azul |
| 3:10, 3:18 | atalho de teclado | atalho | **cartãozinho preto** com o atalho, junto do menu |
| [3:48–3:50](https://www.youtube.com/watch?v=11AJCbZ5Xew&t=228s) | "I just want you to know that you can basically do whatever…" | ênfase pessoal | **a bolha do rosto cresce ~2×** e volta |
| 3:52 | referência dos blocos | recurso extra | página + rodapé com a URL |

**O que se aprende**
- Na abertura falada, **a tela entra como B-roll de cada coisa nomeada**, e o rosto volta entre uma e outra.
- No corpo da aula, a bolha da câmera é a base, e **a bolha cresce na frase que é conselho pessoal**. É barato e muito humano.
- Atalho de teclado vira card pequeno junto do elemento.
- **A mesma informação recorrente (a URL) sempre no mesmo rodapé.**

### 2.4 Nate Herk · como aprender n8n (0:00–4:00)
| Tempo | Fala | Função | Recurso |
|---|---|---|---|
| [0:00–0:08](https://www.youtube.com/watch?v=Fqeo8q8-nJg&t=0s) | "When I first started learning n8n…" | gancho (história) | B-roll/motion: mesa com n8n, janelas do YouTube, calendário "January 2026" |
| 0:12 | "build AI agents as quick as possible" | termo | chip "AI AGENTS" ao lado do rosto |
| 0:14–0:16 | "you can't build good agents until you understand workflows" | **tese** | frase em tela cheia, com as palavras-chave em verde |
| 0:20–0:24 | "in this video I'll walk you through…" | roteiro | janela do vídeo + "1. n8n · 2. AI automations?" |
| 0:26–0:32 | "Do not start with AI. Start with workflows." | regra principal | régua de $0–$50 000 + a frase escrita |
| 0:36 | "because they're cool" | piada | trecho de filme (Jim Carrey digitando) |
| 0:42–0:46 | "trying to run before you can walk" | metáfora | legenda-chave colorida sobre o rosto |
| [0:48–0:50](https://www.youtube.com/watch?v=Fqeo8q8-nJg&t=48s) | "the three layers" | **mapa** | pirâmide 3D com #1 workflows, #2 AI automations, #3 agents |
| 0:52–0:58 | "you know the inputs… outputs" | conceito | chips INPUT → OUTPUT junto do rosto, depois palavras "MAP THOSE", "RUNS THE…" |
| 1:04–1:06 | "one of the strongest ways to produce ROI" | tese | legenda-chave colorida |
| [1:08–1:14](https://www.youtube.com/watch?v=Fqeo8q8-nJg&t=68s) | "McKinsey found… 30% to 200% ROI" | **número com fonte** | print do artigo com marca-texto amarelo |
| 1:22–1:30 | "position yourself as an automation agency" | consequência | card "YOU · efficiency agency" com ramos |
| 1:32–1:36 | "AI automations are the next step up" | volta ao mapa | **a mesma pirâmide** com #2 aceso + 2 chips |
| 1:38–1:46 | "AI to personalize the email… score tickets" | 2 exemplos | ícones (e-mail, IA, prioridade alta/baixa) ao lado do rosto |
| 1:50–1:54 | "50% of work can be automated without AI" | número com fonte | artigo com sublinhado |
| 1:58–2:00 | "AI agents, the top layer" | volta ao mapa | pirâmide com #3 aceso |
| 2:02–2:06 | "make decisions, reference memory, use tools, adjust" | **enumeração** | 4 chips entrando um a um ao lado do rosto |
| 2:24–2:28 | "workflows are deterministic… agents non-deterministic" | **comparação** | dois rótulos lado a lado embaixo do rosto |
| 2:30–2:32 | "more AI, more possibility for errors" | causa → efeito | tela dividida "MORE AI → MORE ERRORS" (vermelho) |
| 2:42 | "core building blocks" | transição | **o rosto encolhe para um cartão** com nós em volta |
| 2:56–3:52 | "the transition curve… 5 phases" | modelo/conceito | curva desenhada aos poucos, **alternando com o rosto** (6 idas e voltas) |
| 3:08–3:10 | "JSON… HTTP request… prompt your agent" | lista de jargão | palavras soltas sobre a tela desfocada |
| 3:46–3:48 | "you're going to feel overwhelmed" | emoção | imagem de pessoa estressada |

**O que se aprende**
- É o mais variado, e mesmo assim tem ordem: **cada função sempre com o mesmo recurso**.
  - tese → legenda-chave colorida;
  - número → print da fonte com marca-texto;
  - enumeração → chips entrando um a um;
  - comparação → dois rótulos lado a lado;
  - emoção → imagem;
  - mapa → a mesma pirâmide.
- **O diagrama é construído aos poucos, intercalado com o rosto**, em vez de despejado de uma vez.
- O rosto é a base (~42%), e algo muda a cada ~5,7 s.

### 2.5 Ali Abdaal · 10 dicas de tempo (0:00–4:00)
| Tempo | Fala | Função | Recurso |
|---|---|---|---|
| [0:00–0:06](https://www.youtube.com/watch?v=iONDebHX9qk&t=0s) | "I have read basically all of the books…" | gancho | rosto + objeto na mão (suco), @ |
| 0:08–0:12 | "10 things that I still use" | **roteiro** | barra com 10 ícones no pé do quadro |
| 0:14–0:16 | "tip number one: we own all of our time" | capítulo | **cartão branco: título + ícone** (o mesmo modelo nas 10 dicas) |
| 0:20–0:26 | explicação | — | rosto, alternando enquadramento normal e punch-in |
| [0:28](https://www.youtube.com/watch?v=iONDebHX9qk&t=28s) | "I don't have time to do stuff" | crença errada | texto grande sobre o rosto |
| 0:36–0:38 | "at any given moment you are doing what you most want…" | citação | legenda-chave no pé |
| 0:50 | "six hours playing World of Warcraft" | exemplo/piada | B-roll do jogo em janela |
| 1:02–1:04 | "we are always in control of our own time" | tese | legenda-chave no pé |
| 1:18 | "hell yeah or no" | capítulo | o mesmo cartão branco + ícone |
| 1:22–1:26, 1:42 | "the title of this book by Derek Sivers" | fonte | livro físico na mão |
| 1:48 | "if I get an email saying…" | exemplo | print de e-mail |
| 2:04–2:10 | "my calendar is full of…" | exemplo | painel lateral com o calendário (o rosto continua) |
| 2:16 / 3:00 | "the daily highlight" / "use a to-do list" | capítulo | o mesmo cartão |
| 2:52–2:58, 3:22–3:28 | rotina de escrever a lista | exemplo | B-roll de mão escrevendo, cartão em macro |
| 3:44 | "I use Roam" | ferramenta citada | ícone pequeno no canto |

**O que se aprende**
- O rosto domina, e os recursos são **poucos e fixos por função**:
  - capítulo → o mesmo cartão;
  - tese → legenda-chave;
  - exemplo pessoal → B-roll;
  - fonte → objeto na mão;
  - ferramenta → ícone.
- **A barra de 10 ícones da abertura** funciona como "mapa".
- **Texto sobre o rosto só em tese e citação**: 3 vezes em 4 min.

### 2.6 O que os cinco têm em comum
1. **Função → recurso fixo.** Ninguém escolhe o recurso pela frase isolada. A escolha vem do papel da frase, e o mesmo papel recebe o mesmo tratamento. Isso é o que faz parecer "editado por alguém" e não "efeito aleatório".
2. **Dêixis manda destacar.** Quando a fala diz "esse aqui", "olha aqui" ou "this", o elemento recebe destaque no mesmo instante (Kevin 1:14 e 3:44; Fireship 0:18).
3. **Mapa recorrente:** pirâmide (Nate), barra de ícones (Ali), "trailer" de resultados (Kevin). O vídeo mostra o caminho e volta a ele na troca de bloco.
4. **Tela não fica 30 s igual.** Mesmo o tutorial mais seco (Kevin) muda algo a cada ~20–25 s.
5. **Contraste:** depois do recurso forte vem trecho limpo. Nate alterna diagrama ↔ rosto; Kevin faz um destaque e depois tela pura.
6. **Rosto = pessoa falando com você:** gancho, opinião, conselho, emoção. Instrução de clique é tela.

---

## 3. Princípios de escolha (com fonte)

- **O corte serve primeiro à emoção e à história.** A regra dos 6 de Walter Murch, em ordem: emoção 51%, história 23%, ritmo 10%. Num tutorial, "emoção" é **clareza** (já em `oficio-youtube.md` R1). O recurso que não serve à clareza da frase sai, por mais bonito que seja.
- **Corte motivado:** troca-se de imagem quando a fala traz informação nova que pede imagem nova, ou por um gesto ou som ([IU C229, aula 9](https://jkmedia.sitehost.iu.edu/C229/Lecture9_sp25.docx); [SSW, use cutaways](https://www.ssw.com.au/rules-legacy/use-cutaways)).
- **B-roll literal e B-roll conceitual.** O literal mostra o que foi nomeado: é seguro e se lê na hora, mas cansa se for só ele. O conceitual é para a frase sem objeto, como "minha equipe demora" ([Async, b-roll matching](https://async.com/blog/match-b-roll-to-your-video/)). Na aula de software, o "literal" é a própria tela ou um recorte dela, e o "conceitual" é o motion.
- **Texto na tela = só palavra-chave.** Texto que repete a narração piora retenção e transferência (redundância, Mayer, Heiser & Lonn 2001, [PDF](https://www.csus.edu/indiv/e/eppersonm/hist107/documents/mayer,%20heiser,%20&%20lonn%20(2001).pdf)). A exceção é texto **curto, que destaca a ação ou o termo e fica junto do que descreve** ([resumo dos princípios](https://www.digitallearninginstitute.com/blog/mayers-principles-multimedia-learning)). Daí a regra de 1–4 palavras.
- **Sinalização e contiguidade** (Mayer, já em `anotacoes.md`): destaque no elemento, na palavra (−0,3 a +0,2 s), um por vez. Ajuda mais quem sabe pouco, que é o público do cliente B.
- **Interrupção de padrão:** os blogs de retenção falam em "algo muda a cada 15–30 s", "B-roll a cada 30–60 s" e até "a cada 3–7 s" ([faceless.so](https://faceless.so/blog/retention-first-editing-12-cuts-that-hook-viewers); [Autonolab](https://blog.autonolab.com/blog/2025-10-01-pattern-interrupts-resetting-attention-every-30-seconds/); [Subscribr](https://subscribr.ai/youtube-strategy/editing-talking-head-videos-engaging)). São números **sem estudo publicado** e servem como **alarme**, não como meta. A nossa medição confirma a faixa: 5–8 s em vídeo de rosto e ~20–25 s em tutorial de tela.
- **Gráfico conta como profissionalismo:** 42% dos espectadores põem "gráficos profissionais (texto, sobreposição, rodapé)" entre as 3 coisas mais importantes num vídeo instrucional, e 87% preferem uma pessoa real a um avatar ([TechSmith Video Viewer Study 2024](https://assets.techsmith.com/docs/TechSmith-Video-Viewer-Study-2024.pdf)).
- **Fireship:** "se o quadro não entretém, ensina ou faz a transição, corta" ([guia de estilo Fireship](https://skills.sh/jarmen423/skills/fireship-video-style), fonte secundária). Para nós: **se o recurso não ensina, sai** (coerência de Mayer, d = 0,86).
- **Ali Abdaal:** 2–5 s por plano no trecho de rosto, cortes na troca natural de ideia ([Choppity](https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/), fonte secundária). Confere com o que medimos (28 cortes em 4 min, a maioria punch-in).

### 3.1 A escada de intensidade (a "hierarquia visual das edições")
| Degrau | Recurso | Custo de atenção | Quando |
|---|---|---|---|
| 0 | nada / corte seco / tela 1× | zero | frase de ligação, repetição de padrão já entendido, depois de um recurso forte (contraste) |
| 1 | zoom que segue a ação | baixo | passo, leitura de campo, clique a copiar |
| 2 | anotação (holofote, lupa, seta, passo numerado) ou texto curto (1–4 palavras) | médio | "esse aqui", valor, termo, estado, condição |
| 3 | card parcial (pop-up) · bolha da câmera cresce · rótulos ao lado da tela | médio-alto | benefício, dica extra, opinião, enumeração curta |
| 4 | tela em cena (encolhida, com coisas em volta) · tela dividida | alto | definição dentro da demo, menu com 3 opções, comparação com a tela viva |
| 5 | motion em tela cheia | máximo | ideia central do vídeo, número que vira régua, pegadinha, abertura, fechamento |

**Regras da escada**
1. **O degrau é proporcional ao peso da ideia no vídeo inteiro.** Pergunte: "se o aluno lembrar só 5 coisas, esta é uma?". Se for, merece o degrau 4–5.
2. **Não suba dois degraus em frases seguidas sem descer.** Depois de um 4 ou 5, a próxima frase fica em 0–1.
3. **O topo é escasso:** degrau 5 no máximo ~1 por minuto. Degraus 2–4 somados: no máximo 3 por minuto (TechSmith: 4 por minuto já cansa).
4. **Mesma função = mesmo recurso** no vídeo inteiro. A variedade vem das funções mudando, não do sorteio.
5. **Nenhum recurso que não seja a base em duas frases seguidas.** O zoom é a base e pode repetir; holofote → holofote não.
6. **Rosto = pessoa.** Câmera em destaque só em gancho, opinião, conselho, emoção e celebração. Nunca em instrução de clique.

---

## 4. A matriz: função da frase × recurso

Leitura: **1º** é o padrão. **2º** quando o 1º não cabe (tela mexendo, já usado na frase anterior, sem material). **3º** é a alternativa barata ou de variação. A última coluna diz o que **não** fazer.

| # | Função da frase (como reconhecer) | 1º | 2º | 3º | Por quê | Não fazer |
|---|---|---|---|---|---|---|
| 1 | **Gancho / promessa** (0–10 s; "essa automação mudou…") | B-roll real do resultado (cold open, 3–5 s do meio do vídeo, voz por cima) | motion tipográfico com a palavra do título | câmera em destaque, olho no olho | provar o título em ≤ 10 s (E1/E5); Kevin mostra o resultado em 0:18, Nate abre com história em B-roll | logo/vinheta antes da fala; "oi, pessoal" |
| 2 | **Dor / contexto** ("você já teve dificuldade de…") | motion tipográfico enumerando as dores | câmera em destaque (empatia) | B-roll conceitual (só se o tom permitir) | sem tela para mostrar, a dor é abstrata e vira palavra | mostrar a tela da ferramenta antes de dizer para que serve |
| 3 | **Definição do conceito central** ("o que seria o SLA?") | motion em tela cheia: palavra gigante + definição em 1 linha | tela em cena + coluna com o termo | cartão de termo (Fireship: logo + "but free && open source") | é a ideia que o aluno tem que levar; merece o degrau 5 uma vez | texto da definição inteira (redundância) |
| 4 | **Termo de interface / definição secundária** ("as metas", "o gatilho") | rótulo do termo junto do elemento (Fireship "TRIGGER" com seta) | tela em cena + coluna | card parcial | o aluno vai procurar esse nome na tela; o rótulo usa o mesmo nome que a UI | motion em tela cheia (gasta o topo à toa) |
| 5 | **Passo / clique a copiar** ("eu venho aqui em configurações") | tela cheia + zoom que segue | passos numerados (≥ 3 cliques seguidos) | anel de clique no botão | o aluno precisa ver o clique; contiguidade | encolher a tela, motion, texto grande por cima |
| 6 | **Valor / número da configuração** ("5 minutos", "20") | anotação: o campo levanta ou lupa (recorte do bruto) | zoom no campo | texto de ênfase com o número = o da tela | número dito = escrito = na tela; elemento pequeno | número diferente do da tela; ampliar a camada já ampliada |
| 7 | **Dêixis** ("esse aqui", "olha aqui", "dá uma olhada") | holofote no elemento, na palavra | seta + rótulo | zoom | a fala apontou; o olho tem que achar em < 0,3 s (Kevin 1:14) | destacar algo que a fala não citou |
| 8 | **Estado / indicador** (cor, selo, "está laranja") | ponto ou contorno na cor do estado sobre o elemento | selo de estado fixo (teste) | lupa, se for pequeno e mudar ao vivo | cor do estado = cor do destaque (uma cor só) | cor de destaque diferente da cor do estado |
| 9 | **Enumeração de itens que estão na tela** (3 opções de menu, 3 ações) | cards que saltam do menu (tela em cena) | rótulos ao lado de cada linha (Kevin: Outcome/Context/Standard) | holofote que anda item por item | a tela continua mostrando **onde** mora cada item; segmentação | lista em tela cheia longe da tela |
| 10 | **Enumeração abstrata** (sem tela: "resposta, velocidade, tempo médio") | motion tipográfico (um item por vez) | chips entrando um a um ao lado do rosto (Nate 2:02) | barra-mapa de ícones (Ali 0:08) | nada para apontar; o desenho organiza | os 3 itens de uma vez |
| 11 | **Comparação / contraste** (A × B, interno × lead, antes × depois) | tela dividida ou motion lado a lado | dois cards lado a lado (Nate 2:24) | errado riscado → certo no mesmo lugar (nível 50) | o olho compara o que está lado a lado | mostrar A e B em momentos separados sem ligação |
| 12 | **Aviso / erro comum / pegadinha** ("lembrando que…", "não coloque") | motion em tela cheia na cor de alerta (para o vídeo) | seta + rótulo vermelho no elemento ("SLA FICA DE FORA") | câmera em destaque ("atenção") | ideia errada antes da certa dobra o aprendizado (E7); merece o topo | aviso no mesmo tom visual do resto |
| 13 | **Opinião / recomendação pessoal** ("eu gosto de deixar", "recomendo") | bolha da câmera cresce 1,4–1,6× (Thomas Frank 3:48) | punch-in na câmera (se for grande) | texto curto "recomendo: ≤ 15 min" | é a pessoa falando, não a interface | anotação técnica (mistura opinião com regra) |
| 14 | **Benefício / consequência** ("já pega estatísticas", "para de perder lead") | card parcial (pop-up no pé, lado oposto da câmera) | bolha cresce | texto de ênfase de 1–3 palavras | resume o "para quê" sem tirar a tela | motion em tela cheia (o benefício não é conceito novo) |
| 15 | **Exemplo / caso** ("por exemplo, eu mando 'estamos verificando'") | recorte do exemplo real na tela (levanta/lupa) | B-roll ou print (real ou réplica marcada como ilustração) | tela em cena com recorte | exemplo é concreto: mostre o objeto (B-roll literal) | inventar visual genérico (stock) numa aula de software |
| 16 | **Prova / resultado ao vivo** ("mandou oficialmente agora") | tela cheia + lupa no número/mensagem real | selo de estado ao lado | o elemento que chegou salta como card | a prova é a tela; o recurso só aponta | desenhar por cima o que a tela já mostra |
| 17 | **Espera / tempo morto** (cliques calados, carregando) | corte (com fusão se a tela muda) | contador/selo ao lado | — | regra do dono: nada de 4× | acelerar; enfeitar o tempo morto |
| 18 | **Transição de capítulo / re-gancho** ("agora nas automações") | marcador de capítulo + fusão de página | mapa recorrente voltando com o item aceso (Nate) | câmera em destaque dizendo o que está em jogo | o aluno pula e volta (Guo); o mapa diz onde ele está | capítulo sem frase que relembre o que está em jogo |
| 19 | **Piada / aparte / emoção / celebração** ("tudo certinho, funcionou") | bolha cresce / punch-in | nada (deixar a tela mostrar) | carimbo (Fireship "NOT SPONSORED"), se o tom da marca deixar | emoção é do rosto | meme numa aula de marca séria |
| 20 | **Resumo / fechamento** | motion com 3 linhas + marca | card + área livre para a tela final | câmera em destaque | fecha o arco (≤ 20 s), tela final livre | sinalizar o fim e enrolar |
| 21 | **Frase de ligação** ("então", "beleza", "tá?", pergunta curta) | **nada** (degrau 0) | — | — | contraste; guarda força para a próxima | pôr recurso em toda frase |

**Desempate quando duas funções caem na mesma frase:** vale a de **maior peso no vídeo** (aviso > definição > valor > enumeração > benefício > opinião). A outra fica para a frase seguinte, se couber.

---

## 5. Plano de edição de exemplo: aula SLA inteira

Base: `projetos/<projeto>/v1/aula-sla-v2.mp4` (5:08). Os tempos são do **vídeo editado v2** e vêm de `fonte/palavras-final.json`. Gerei `frases.py` de novo, porque o `frases-final.txt` da pasta ainda está na v1 e tem tempos diferentes.

O que a tela mostra em cada trecho saiu de uma folha de contato da v2 (um quadro a cada 4 s). Os motions, capítulos e o selo atuais **ficam**: o dono aprovou com ★★. O plano só preenche os vãos com variedade.

Legenda dos recursos: **M** motion em tela cheia · **Z** zoom · **TC** tela em cena · **AN** anotação · **TX** texto de ênfase · **CP** card parcial · **CAM** câmera em destaque (punch-in ou bolha cresce) · **BR** B-roll/print · **CAP** capítulo · **0** nada.

| Tempo (editado) | Frase | Função | Recurso | Por quê |
|---|---|---|---|---|
| 0:00–0:03 | "Essa automação mudou completamente o atendimento da minha agência." | gancho | **BR** cold open: 3 s do teste ao vivo (3:48–3:56: chip vermelho + "Estamos verificando" chegando), com a voz de f1 por cima; o "MUDOU." do motion entra em 0:03 | provar o título antes de explicar (matriz 1); hoje a abertura só promete |
| 0:03–0:29 | dores: tempo de resposta, velocidade, tempo médio → "vem para resolver" → "controle… acionando automações" | dor + promessa | **M** 00 abertura (atual: RESPOSTA. VELOCIDADE. TEMPO MÉDIO. riscados → CONTROLE. + cronômetro) | enumeração abstrata, sem tela para mostrar (matriz 2/10) |
| 0:29–0:31 | "a automação que eu vou estar mostrando aqui hoje é SLA." | nome do assunto | **CAM** punch-in 1,15× na câmera grande | primeiro olho no olho; só dá aqui, porque até 0:37 a câmera do bruto é grande (1225 px). Conferir a nitidez na foto |
| 0:31–0:37 | "O que seria o SLA? SLA define o tempo que a sua equipe tem que atender…" | definição central | **M** 01 (SLA. gigante → definição) | a ideia nº 1 do vídeo leva o degrau 5 (matriz 3) |
| 0:37–0:47 | "diversos campos aqui para preencher… canal específico… ou em todos os canais" | tour / passo | **Z** no campo de canal | depois de 37 s de motion, degrau 1 (contraste) |
| 0:47 | — | transição | **CAP** 1 "Metas do SLA" (atual) | o aluno sabe onde está |
| 0:47–0:53 | "As metas de SLA, o que seriam essas metas? … o tempo que eu estou demorando para responder" | definição secundária | **TC** pose `direita` + coluna "META. = tempo até responder" | definição dentro da demo: não repete o motion; a tela calma continua visível (matriz 4) |
| 0:53–0:58 | "Dá uma olhada aqui. A meta está definida… para 5 minutos." | dêixis + valor | **AN** holofote no bloco "Definir metas" → o campo "5 Mins" levanta (`anotacoes.md`, Ex. 1) | "olha aqui" + número pequeno (matriz 6/7) |
| 0:58–1:05 | "símbolo laranja… Esse lead aqui já está laranja… vencimento em breve" | estado | **Z** no lead (zoom.json 61 s) + ponto laranja no chip, continuação da mesma anotação | a cor do estado liga a regra ao lead (matriz 8) |
| 1:05–1:14 | "E quando bater aqui 10 minutos, quer dizer o quê? Que… já rompeu com o combinado." | pergunta + resposta | **0** na pergunta (pausa de 0,3 s mantida) → **TX** "ROMPEU." vermelho, ao lado da bolha, na palavra "rompeu" | a resposta é a palavra que fica; 1 palavra só (Mayer) |
| 1:14–1:22 | "posso colocar aqui, caso seja o atendimento interno, para cancelar… ou se for realmente um lead, deixo rodando" | passo com condição | **Z** (74,5 s) + **AN** seta + rótulo "INTERNO → cancelar" no "Cancelar SLA" | o aluno precisa lembrar a **condição** (matriz 11, versão barata); 21 s depois da anotação anterior |
| 1:22–1:26 | "quando der o vermelho, ele vai ficar… em sinal vermelho" | estado já visto | **Z** (85,5 s), nada novo | padrão já entendido: degrau baixo |
| 1:26 | — | transição | **CAP** 2 "O que conta no SLA" (atual) | — |
| 1:26–1:30 | "posso colocar para automações contarem ou não para o SLA" | opção | **Z** no grupo "Como as mensagens de automação…" | configuração = zoom (matriz 5) |
| 1:30–1:31 | "Eu gosto de deixar para contar." | opinião | **CAM** a bolha cresce 1,0 → 1,5× em 0,4 s e volta | primeira opinião: é a pessoa, não a UI (matriz 13; Thomas Frank 3:48) |
| 1:31–1:40 | "O Conversation AI é a mesma coisa… quem pode desativar… deixo todos… você pode escolher" | mesma lógica repetida | **Z** (zoom.json) | sem recurso novo: o aluno já entendeu o padrão |
| 1:40–1:50 | "com isso aqui ativado já é muito bom… muitas estatísticas… métricas do tempo que a sua equipe demora" | benefício (e **buraco**: a página Estatísticas está vazia) | **CP** card no pé, à esquerda: mini-gráfico "tempo médio de resposta" (réplica, **ilustração**, dados inventados) + "✓ métricas da equipe" | a tela vazia não prova o benefício; o card mostra como fica (matriz 14/15). Marcar no guia como ilustração |
| 1:50–1:57 | "ainda tem outra funcionalidade… uma automação para… mandar para os seus atendentes que está demorando" | re-gancho falado | **0** (tela 1×) | a fala já carrega; o motion vem a seguir (contraste antes do degrau 5) |
| 1:57–2:09 | "vencimento em breve como 10 minutos e o vencido como 20… máximo… recomendo até menos" | números-limiar | **M** 02 régua (cronômetro 3D, atual) | os números que o vídeo inteiro usa depois viram régua (o "mapa recorrente") |
| 2:09–2:11 | "Aqui agora nas automações, eu…" | transição | **CAP** 3 "A automação do SLA" + fusão de página | — |
| 2:12–2:22 | "em específico, Conversations SLA… o SLA Status… o vencimento em breve… o laranja" | termo de UI (gatilho) | **TC** pose `3d-direita` + palavra "SLA STATUS" na coluna (`tela-em-cena.md`, Ideia 1) | nome que o aluno vai procurar; tela calma no painel do gatilho |
| 2:22–2:32 | "O vencido, que é o vermelho… quando é ignorado… quase nunca você vai usar… os que mais vai usar são esses dois" | enumeração na tela + hierarquia | **TC** (mesma pose) + 3 cards saltam do menu (Due soon/Overdue/SLA dismissed, traduzidos), "ignorado" riscado em "quase nunca" | menu em inglês de 13 px; os cards traduzem e dão a cor (matriz 9) |
| 2:32–2:45 | "se eu usar esse gatilho… notificar internamente a minha equipe, mandar uma mensagem para o meu lead. Colocar uma tag…" | enumeração de ações (ele está escolhendo) | tela volta cheia + **Z** (160,5 s) + **AN** holofote que anda: "Enviar notificação interna" → "Enviar SMS" → "tag" | ele está clicando, então tela cheia (matriz 5). Os itens já estão no menu "Ações recentes": o holofote anda, um por vez |
| 2:45–2:52 | "E assim eu vou tendo métricas. Se… essa automação está sendo muitas das vezes ativa, … métrica real que minha equipe está demorando" | insight pessoal | **CAM** a bolha cresce | conclusão de quem usa (matriz 13); 75 s depois da 1ª vez |
| 2:52–3:13 | "posso criar duas automações… uma… para notificar a equipe… uma… quando bate no vermelho… mando a mensagem para o lead" | comparação A × B | **M** 03 duas automações (atual: AVISA. × RESPONDE.) | comparação = lado a lado (matriz 11) |
| 3:13–3:16 | "…de fechar com esse lead." | fecho de frase | **0** | respiro depois de 21 s de motion |
| 3:16–3:26 | "além de notificar o lead com a mensagem básica, por exemplo, estamos verificando, também envio… uma notificação interna" | exemplo concreto | **AN** o campo "Mensagem" da ação SMS levanta com "estamos verificando" (recorte do bruto) | o texto exato que o aluno vai digitar (matriz 15) |
| 3:26–3:35 | "O atendimento ideal… já foi vencido, já rompeu os 20 minutos. Isso vai entrar para a estatística…" | consequência | **Z** no formulário da notificação interna, depois 1× | já há destaque 10 s antes: degrau baixo |
| 3:35 | — | transição | **CAP** 4 "Teste ao vivo" (atual) + fusão para a conversa | — |
| 3:35–3:39 | "Ok, pronta a minha automação… mandando para esse lead… Estamos verificando?" | início da prova | **0** / corte seco para a conversa | a tela já diz tudo |
| 3:39–3:46 | "se o meu SLA… romper… daqui 45 segundos, ele vai mandar uma mensagem" | número ao vivo | **AN** lupa no chip "45s" + selo do SLA (atual) (`anotacoes.md`, Ex. 2) | o número real conta na tela (matriz 16) |
| 3:46–3:54 | "A conversa foi oficialmente vencida… a automação já vai enviar…" | mudança de estado | selo fica vermelho na palavra "vencida" (atual) + o anel da lupa fica vermelho | a mesma palavra muda tudo, numa cor só |
| 3:54–4:00 | "Igual mandou oficialmente agora. Pode ver aqui… estamos verificando, foi enviada para uma automação." | prova | **TC** pose `direita` com recorte da conversa + a mensagem salta como card "ENVIADA POR AUTOMAÇÃO" (Ideia 3) | fecha "recebeu porque venceu" num quadro (matriz 16, 3º) |
| 4:01–4:08 | "se eu abrir aqui as automações… o fluxo… foi realmente o do SLA" | passo de verificação | **Z** (`zoom_fixo` 1,5×) no painel "Fluxos de trabalho ativos" | clique a copiar (onde conferir); anotação seria 3ª em 25 s |
| 4:08–4:13 | "Tudo certinho, já funcionou certinho…" | celebração | **0** | a tela mostra o resultado; não precisa de nada (matriz 19, 2º) |
| 4:13–4:18 | "aí você para de perder os seus leads por não atender." | benefício dito "para você" | **CAM** a bolha cresce | fala direta para a pessoa; última vez antes do aviso |
| 4:18–4:26 | "como essa automação envia mensagem… o SLA saiu daqui, sendo que esse lead segue no vácuo" | pegadinha | **M** 04 (RESPONDIDO? → NO VÁCUO., atual) | aviso = degrau 5 com cor de alerta (matriz 12) |
| 4:26 | — | transição | **CAP** 5 "O ajuste final" (atual) | — |
| 4:26–4:34 | "Então o que eu vou fazer? … configurações… contar apenas as mensagens dos fluxos… selecionados" | passo 1 | **AN** holofote curto no grupo → **passo 1** no rádio (`anotacoes.md`, Ex. 3) | sequência que o aluno vai repetir (matriz 5, 2º) |
| 4:34–4:38 | "E eu seleciono todos os fluxos…" | passo 2 | **AN** passo 2 no campo de seleção (o 1 esmaece) | mesma sequência (conta como uma chamada) |
| 4:38–4:49 | "esse aqui em específico SLA eu não vou colocar. Por quê? … não é… uma automação que responde o lead… passagem para que o lead não se sinta no vácuo. Entendeu?" | aviso no elemento | **AN** seta + rótulo vermelho "SLA FICA DE FORA", até "Entendeu?" | o único "não faça" da aula, com a cor de erro (matriz 12, 2º) |
| 4:49–4:53 | "leio e ignoro. Coloco o resto tudo aqui…" | passo | **Z** | degrau baixo entre dois destaques |
| 4:53–4:54 | "Salvo e prontinho." | passo final | **AN** passo 3 + anel de clique no Salvar; tudo some junto | o último passo é o mais forte |
| 4:54–5:00 | "notifico também o gerente… os atendentes que estão demorando" | complemento | **0** | orçamento do minuto cheio (3 chamadas); o fechamento resume |
| 5:00–5:08 | (sem fala) | fechamento | **M** 05 (NO PRAZO. + 3 linhas + logo, atual); a música sobe | resumo + respiro (matriz 20) |

### 5.1 Conferência do plano (as 6 regras da seção 3.1)
| Regra | Conta | OK? |
|---|---|---|
| Variedade | v2: 3 recursos (M, Z, CAP) + selo → plano: **10** (BR, M, CAM, Z, CAP, TC, AN, TX, CP, 0) | ✔ |
| Mesma função = mesmo recurso | opinião/insight/benefício para você → sempre CAM (1:30, 2:45, 4:13); passo → Z; aviso → M ou seta vermelha; termo de UI → TC; número ao vivo → lupa | ✔ |
| Degrau 5 ≤ 1 por minuto (fora a abertura) | motions em 0:31, 1:57, 2:52, 4:18, 5:00. O intervalo 2:52–4:18 tem 1 | ✔ |
| Chamadas (degraus 2–4) ≤ 3 por minuto | o minuto mais cheio (4:00–5:00) tem: bolha 4:13 · passos 1-2-3 (uma sequência) · seta 4:38 = 3. O card em 4:55 foi **cortado** por causa disso | ✔ |
| Tela encolhida ≤ 30% do tempo de tela | 0:47–0:53 (6 s) + 2:12–2:32 (20 s) + 3:54–4:00 (6 s) = 32 s de ~224 s de tela = **14%** | ✔ |
| Nenhum recurso não-base em 2 frases seguidas | AN → Z → AN… ; os dois TC seguidos em 2:12–2:32 são **um** trecho com duas poses | ✔ |
| Nunca encolher no clique a copiar | 2:32 (escolhe a ação) e 4:01 (abre o fluxo) ficam em tela cheia | ✔ |
| Anotação a cada 15–25 s em média | 7 anotações em ~3,7 min de demonstração ≈ 1 a cada 32 s (abaixo da média, de propósito: aula densa) | ✔ (conservador) |

**Material que falta para o plano:**
- trecho do cold open (já existe na gravação);
- réplica do gráfico de estatísticas (ilustração);
- recortes do bruto: campo "5 Mins", chip "45s", campo da mensagem SMS, menu SLA Status.

---

## 6. Proposta: passo novo na skill edicao-video, "mapa de recursos"

**Onde entra:** entre o passo 9 (zoom) e o 10 (motions), como **9b**. Hoje o passo 10 escolhe "2–5 frases que ficam mais claras desenhadas", e o 10b põe tela em cena e anotações. Isso decide **onde há motion**, mas não decide **o que cada frase recebe**. Por isso a v2 acabou com 3 recursos só.

### 6.1 Texto pronto para o SKILL.md (substitui o começo do passo 10 e cria o 9b)

```markdown
9b. **Mapa de recursos** (pedido do dono, 16/10/2026: "nesse momento um motion, nesse um card, nesse um textinho"). Antes de produzir qualquer motion, escreva `fonte/mapa-recursos.md`: uma linha por frase de `palavras-final.json` (ou por grupo de frases da mesma ideia) com **tempo · frase · função · recurso · por quê**. Funções e recursos em `references/gramatica.md` (matriz função × recurso, 1º/2º/3º, e a escada de intensidade 0–5).
   - Leia a **função** da frase antes de pensar no visual: definição, termo de UI, passo, valor, "esse aqui", estado, enumeração, comparação, aviso, opinião, benefício, exemplo, prova, espera, capítulo, emoção, fechamento, ligação.
   - **Mesma função = mesmo recurso** no vídeo inteiro. A variedade vem das funções mudando.
   - Degrau proporcional ao peso da ideia; **motion em tela cheia ≤ ~1/min**; **chamadas (anotação, texto, card, bolha, tela em cena) ≤ 3/min**; depois de um degrau 4–5, a frase seguinte fica em 0–1.
   - Nenhum recurso que não seja a base em duas frases seguidas (zoom é base).
   - Câmera em destaque (punch-in ou bolha crescendo) só em gancho, opinião, conselho, emoção. Instrução de clique é tela cheia com zoom.
   - Frase de ligação ("então", "tá?", pergunta curta) = **nada**. É o contraste que faz o resto aparecer.
   - Confira as 6 regras com a tabela (ou `scripts/mapa_recursos.py fonte/mapa-recursos.md`, que conta degrau/min, chamadas/min, % de tela encolhida e repetição seguida) e mostre o mapa ao dono **junto com o roteiro de cortes**, antes de gravar os motions. É barato mudar aqui e caro depois do render.
10. **Motions e capítulos** (skill motion-design, com cartão da direcao-de-arte e números da hierarquia-visual): produza o que o mapa marcou com M (motion em tela cheia), CP (card parcial) e TX (texto de ênfase)…
```

### 6.2 Conteúdo do `references/gramatica.md` novo
- A **escada de intensidade** (seção 3.1 deste estudo, com as 6 regras).
- A **matriz função × recurso** (seção 4, as 21 linhas, com "não fazer").
- **Como reconhecer a função pela fala** (gatilhos em português):
  - "o que seria / o que é" → definição;
  - "esse aqui / olha aqui / dá uma olhada" → dêixis;
  - número + unidade → valor;
  - "eu gosto / recomendo / eu, particularmente" → opinião;
  - "lembrando que / cuidado / não coloque" → aviso;
  - "por exemplo" → exemplo;
  - "primeiro… depois…" ou 3 itens → enumeração;
  - "ou… ou…" / "um… outro…" → comparação;
  - "agora / aqui agora nas…" → transição;
  - "tá? / entendeu? / então" → ligação.

  Isso permite um **pré-mapa automático** a partir de `palavras-final.json` (proposta: `mapa_recursos.py --sugerir`, que marca a função provável e deixa o recurso para decidir).
- Os **5 logs** deste estudo resumidos em 1 linha cada, como referência de "como os grandes fazem".
- O exemplo da aula SLA (seção 5) como modelo de `mapa-recursos.md`.

### 6.3 O que a revisão (revisao-video) passa a conferir
- O `mapa-recursos.md` existe e o vídeo final cumpre o que ele marca (foto em cada linha com recurso ≠ 0).
- Na contagem (conta-se pelo mapa e pelo `edicao.json`):
  - degrau 5 ≤ 1/min;
  - chamadas ≤ 3/min;
  - tela encolhida ≤ 30%;
  - nenhum trecho de tela > 40 s sem mudança.
- Rubrica: o item "variedade" da direção de arte ganha **nota pela quantidade de recursos diferentes usados com função clara**. É o oposto de "efeito por efeito".

### 6.4 Linha para `aprendizado/reacoes.md` (quando o dono reagir ao 1º vídeo com o mapa)
`| AAAA-MM-DD | <aula> | ? | "<palavras dele>" | variedade por função | edicao-video 9b + references/gramatica.md |`

---

## Fontes
- Vídeos analisados (amostra a cada 2 s dos primeiros 4 min + legenda automática + descrição/capítulos):
  - [Fireship · n8n will change your life as a developer](https://www.youtube.com/watch?v=bS9R6aCVEzw)
  - [Kevin Stratvert · ChatGPT Work Tutorial for Beginners](https://www.youtube.com/watch?v=mqDn-h0PJnA)
  - [Thomas Frank Explains · Notion Fundamentals: What are Blocks?](https://www.youtube.com/watch?v=11AJCbZ5Xew)
  - [Nate Herk · How I'd Learn n8n if I had to Start Over in 2026](https://www.youtube.com/watch?v=Fqeo8q8-nJg)
  - [Ali Abdaal · How I Manage My Time – 10 Time Management Tips](https://www.youtube.com/watch?v=iONDebHX9qk)
- Murch, *In the Blink of an Eye* (regra dos 6), via `oficio-youtube.md`.
- [Mayer, Heiser & Lonn 2001: redundância](https://www.csus.edu/indiv/e/eppersonm/hist107/documents/mayer,%20heiser,%20&%20lonn%20(2001).pdf) · [resumo dos princípios de Mayer (exceção de palavra-chave)](https://www.digitallearninginstitute.com/blog/mayers-principles-multimedia-learning)
- [TechSmith Video Viewer Study 2024](https://assets.techsmith.com/docs/TechSmith-Video-Viewer-Study-2024.pdf)
- [IU C229, corte motivado](https://jkmedia.sitehost.iu.edu/C229/Lecture9_sp25.docx) · [SSW, cutaways](https://www.ssw.com.au/rules-legacy/use-cutaways) · [Async, B-roll literal × conceitual](https://async.com/blog/match-b-roll-to-your-video/)
- Retenção, números sem estudo (usar como alarme): [faceless.so](https://faceless.so/blog/retention-first-editing-12-cuts-that-hook-viewers) · [Autonolab, interrupção de padrão](https://blog.autonolab.com/blog/2025-10-01-pattern-interrupts-resetting-attention-every-30-seconds/) · [Subscribr, talking head](https://subscribr.ai/youtube-strategy/editing-talking-head-videos-engaging)
- Estilos, fonte secundária: [guia de estilo Fireship](https://skills.sh/jarmen423/skills/fireship-video-style) · [Choppity, estilo Ali Abdaal](https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/)
- Internos: `~/.claude/skills/edicao-video/references/{narrativa,imagem,tela-em-cena,anotacoes,oficio-youtube}.md`; `projetos/<projeto>/v1/{ENTREGA.txt,fonte/palavras-final.json,fonte/edicao.json,fonte/zoom.json}`.
