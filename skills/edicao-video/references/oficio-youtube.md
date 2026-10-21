# 03 — O ofício de editar tutorial e aula para YouTube

Pesquisa de 16/10/2026 para as skills `edicao-video` e `revisao-video`. Foco: aula de tela + câmera (GoHighLevel, automações), como a aula SLA do cliente B.

Como ler a força de cada fonte:
- **[forte]**: estudo, documentação oficial ou norma.
- **[média]**: profissional conhecido falando do próprio trabalho.
- **[fraca]**: blog de ferramenta ou de marketing. Serve só como indício.

Cada regra diz se vale para TUTORIAL: **sim**, **adaptar** ou **não** (só para entretenimento).

---

## 1. Resumo em 5 linhas

1. Tutorial não é vlog. Estudos com 6,9 milhões de sessões mostram que o aluno de tutorial assiste só 2–3 min e depois **pula e volta**. Por isso capítulos, gancho que confirma o título e ritmo de **informação nova** pesam mais que corte rápido.
2. Música por baixo da voz: as referências dizem **no mínimo 15–20 dB abaixo** (WCAG: ≥ 20 dB). Para aprender, a pesquisa (Mayer) diz que música **atrapalha**. Os **25 dB** que o dono aprovou estão certos para aula: vira o nosso padrão (22–28 dB, nunca menos de 20), medido por script e reprovado na revisão.
3. Os primeiros 30 s são uma métrica oficial do YouTube ("Intro"). Nos primeiros 10–15 s o vídeo tem que provar o título (mostrar o resultado ou a dor) e dizer o que vem. O pipeline já faz a promessa, mas não mostra o resultado na abertura e ninguém confere isso.
4. O que mais falta: (a) **medir a trilha** e fazer o ducking por script; (b) a revisão achar **tomada repetida distante** e **motion com elementos sobrepostos**, que foram as duas reclamações; (c) entregar os **capítulos para a descrição** e a legenda .srt; (d) uma **checklist de retenção** com números.
5. Proposta: 9 melhorias em arquivos concretos (seção 4). As três primeiras atacam exatamente o que o dono pediu para mudar na aula SLA.

---

## 2. Regras com números e fontes

### 2.1 Estrutura e gancho

| # | Regra | Número | Tutorial? | Fonte |
|---|---|---|---|---|
| E1 | O YouTube mede a "Intro": quanto da audiência continua depois dos primeiros 30 s. Se cai, a causa é título/thumb desalinhados com a abertura ou a abertura em si. | **30 s** | sim | [forte] [YouTube Help, key moments](https://support.google.com/youtube/answer/9314415) |
| E2 | Primeiro minuto é o mais crítico. Num vídeo de 60 M de views, 21 M saíram no 1º minuto. A abertura tem que bater com o que o título e a thumb prometeram e já começar a entregar. | **1 min** | sim | [média] [MrBeast, "How to succeed in MrBeast production"](https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/) |
| E3 | Fórmula de gancho: provar o título nos primeiros ~10 s, dizer por que importa nos ~10 s seguintes e dar um roteiro de uma linha ("vou te mostrar X, Y e Z"). | **10 + 10 + 1 linha** | sim | [fraca] [OutlierKit](https://outlierkit.com/resources/youtube-hooks-and-retention/) |
| E4 | Proposta de valor clara nos primeiros 15 s. O número citado (+18% de retenção em 1 min) não tem estudo publicado. | **15 s** | sim | [fraca] [Vidpros sobre Mario Joos](https://vidpros.com/retention-editing-what-you-can-learn-from-mario-joos/) |
| E5 | Cold open: começar no momento mais curioso, sem "oi pessoal". No tutorial isso é **mostrar o resultado funcionando** (a automação disparando, o lead recebendo) antes de explicar. | 1º quadro já em movimento | adaptar | [fraca] [Clueso, cold open](https://www.clueso.io/glossary/cold-open) · [OutlierKit](https://outlierkit.com/resources/youtube-hooks-and-retention/) ("never open on a static frame") |
| E6 | Re-engajar em 3 min e em 6 min: um trecho forte que renova o interesse. No tutorial isso é o **início de capítulo** que relembra o que está em jogo ("agora a parte que evita o lead no vácuo"). | **a cada ~3 min** | adaptar | [média] [MrBeast doc](https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/) |
| E7 | Começar pelo **erro comum** (a ideia errada que o aluno tem) e depois desmontar. Na tese de Derek Muller (Veritasium), a nota no pós-teste praticamente dobrou com vídeos que tratam a ideia errada. Já o vídeo "claro e polido" reforçava o erro. | nota ~2× | sim | [forte] [The Journal sobre a tese](https://thejournal.com/articles/2015/05/05/watching-videos-does-not-necessarily-lead-to-learning.aspx) · [Scientific American](https://www.scientificamerican.com/article/how-youtube-star-derek-muller-of-veritasium-is-challenging-scientific/) |
| E8 | No entretenimento, "nunca sinalize que o vídeo está acabando". No tutorial o fechamento é obrigatório (resumo + próximo passo), mas curto. | — | **não** (a parte do "não sinalizar") | [média] MrBeast doc |
| E9 | Tela final do YouTube: só nos **últimos 5–20 s**, vídeo de **≥ 25 s**, até **4 elementos** em 16:9. O card de fechamento tem que deixar espaço livre para eles. | 5–20 s | sim | [forte] [YouTube Help, end screens](https://support.google.com/youtube/answer/6388789) |
| E10 | Planejar antes melhora o engajamento. Aula regravada pensando no formato online prende mais que aula antiga recortada. | — | sim | [forte] [Guo, Kim & Rubin 2014, edX](https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf) |
| E11 | Empacotamento (título + thumb) é parte da edição. Criadores grandes gastam ~30% do esforço em ideia e empacotamento, os pequenos ~5%. | 30% × 5% | sim | [média] [Colin and Samir, regras de Paddy Galloway](https://www.colinandsamir.com/resources/the-new-rules-of-youtube-from-paddy-galloway) |
| E12 | O teste A/B do YouTube aceita até 3 títulos/thumbs e decide pela **fatia de tempo assistido**, não pelo CTR. Thumb que engana perde. | até **3** opções | sim | [forte] [YouTube Help, A/B test](https://support.google.com/youtube/answer/16391400) |

### 2.2 Ritmo e cortes

| # | Regra | Número | Tutorial? | Fonte |
|---|---|---|---|---|
| R1 | Regra dos 6 de Walter Murch: um corte serve, em ordem, a **emoção 51%**, **história 23%**, **ritmo 10%**, trajetória do olho 7%, plano 2D 5%, espaço 3D 4%. Se algo tiver que ceder, cede o de baixo. Num tutorial, "emoção" vira **clareza**: o aluno entende e sente que está avançando. | 51/23/10/7/5/4 | adaptar | [forte] Murch, *In the Blink of an Eye* · [No Film School](https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch) |
| R2 | Cortar onde o pensamento termina. Para Murch, o piscar é a pontuação natural ("encerro esta ideia, começo outra"). No nosso caso: cortar no fim da frase ou da ideia, nunca no meio. | — | sim | [forte] [Big Think sobre Murch](https://bigthink.com/?p=60362) |
| R3 | "Não é a velocidade do corte, é a velocidade com que você traz **informação nova que avança**." Piada e enfeite atrapalham quando se acumulam. No máximo um momento leve por bloco. | — | sim | [média] Mario Joos (ex-MrBeast), via [Vidpros](https://vidpros.com/retention-editing-what-you-can-learn-from-mario-joos/) |
| R4 | Tutorial: o aluno não assiste tudo. Engajamento mediano de **2–3 min, seja qual for a duração**. Recomendação: dar suporte a **pular e rever**. | 2–3 min | sim | [forte] Guo et al. 2014, fig. 7 e tabela 1 |
| R5 | Aula: engajamento mediano de **até 6 min** em qualquer duração. Recomendação: blocos de < 6 min (no YouTube, isso vira capítulos). | < 6 min por bloco | sim | [forte] Guo et al. 2014 |
| R6 | Falar rápido está ok. Engajamento até 2× maior nos vídeos mais rápidos (até 254 palavras/min). A faixa de 145–165 ppm era a menos animada. Não desacelerar o apresentador. **A aula SLA editada ficou em ~190 ppm**, que está bom. | ≥ 165 ppm | sim | [forte] Guo et al. 2014, fig. 6 |
| R7 | Jump cut com punch-in: alternar entre o enquadramento normal e **110–120%** a cada 2º ou 3º corte faz o corte parecer intencional. Nós usamos 1,1× na câmera de rosto, dentro da faixa. Não aplicar punch-in em toda emenda, porque cansa. | 110–120%, a cada 2–3 cortes | adaptar (só em trecho de rosto) | [fraca] [Vizard](https://agent.vizard.ai/how-to/stop-the-punch-ins-cycling-too-fast-in-a-talking-head-edit.html) · [1of10](https://1of10.com/blog/what-is-a-jump-cut/) |
| R8 | J-cut e L-cut: a voz entra antes da imagem (J) ou continua depois (L). Cerca de **0,5 s** de sobreposição deixa demo e tutorial mais naturais. No nosso caso, usar quando entra ou sai um motion de tela cheia e na troca de capítulo, nunca nas emendas de fala dentro do mesmo plano. | ~0,5 s | adaptar | [fraca] [CapCut](https://www.capcut.com/create/j-cuts-and-l-cuts-dialogue-edits) · [Epidemic Sound](https://www.epidemicsound.com/blog/j-cuts-and-l-cuts/) |
| R9 | Respiração: reduzir a respiração alta (~ **-6 dB**) em vez de cortar. Voz sem nenhuma respiração soa editada e robótica. O nosso respiro de 0,2 s / 0,15 s está certo. | -6 dB | sim | [fraca/média] [iZotope RX Breath Control](https://s3.amazonaws.com/izotopedownloads/docs/rx9/en/breath-control/index.html) · [Such a Voice](https://suchavoice.com/?p=16018) |
| R10 | Primeiro passo de qualquer demo: um passe **impiedoso** tirando recomeço, deslize de mouse, muleta, silêncio longo e tempo morto, **antes** de pôr efeito. | — | sim | [média] [TechSmith](https://www.techsmith.com/blog/edit-demo-recording/) |

### 2.3 Visual e mudança de plano

| # | Regra | Número | Tutorial? | Fonte |
|---|---|---|---|---|
| V1 | Sinalização (Mayer): seta, destaque, zoom e cor no que importa melhoram o aprendizado. É o nosso zoom que segue a ação. | — | sim | [forte] [Learning Scientists](https://www.learningscientists.org/blog/2021/7/1-1) · [Cambridge Handbook](https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/C98AB3A6CE760DD63C048936EA0B3B44) |
| V2 | Zoom, cursor destacado e anotação **só quando ajudam a entender**. O objetivo é diminuir o tempo que o olho gasta procurando, não pôr movimento por pôr. "O espectador nunca deve adivinhar para onde olhar." | — | sim | [média] [TechSmith](https://www.techsmith.com/blog/edit-demo-recording/) |
| V3 | Excesso de chamadas cansa: alunos acharam **4 chamadas por minuto** demais. | < 4 por min | sim | [média] TechSmith (pesquisa com alunos, mesmo link) |
| V4 | Rosto do professor em momentos certos prende mais. Gravação "pessoal" prende mais que estúdio caro. Tablet desenhando (estilo Khan) prende 1,5–2× mais que slide ou tela de código. Se tiver que mostrar tela, **desenhe ou marque por cima dela**. | 1,5–2× | sim | [forte] Guo et al. 2014 ("introduce motion and continuous visual flow into tutorials") |
| V5 | Mudança visual (zoom, B-roll, corte de ângulo, texto) a cada **15–30 s** no corpo do vídeo, e nenhum quadro parado por mais de **30 s**. Números de blog, sem estudo publicado. Para tutorial use como **alarme** (trecho longo sem nada mudando), não como meta. | 15–30 s | adaptar | [fraca] [Choppity](https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/) · [AIR Media-Tech](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8) |
| V6 | Ali Abdaal: ritmo moderado, **2–5 s por plano** no trecho de rosto, cortes na transição natural das ideias. | 2–5 s | adaptar (trecho de rosto, não tela) | [fraca] Choppity (mesmo link) |
| V7 | Coerência (Mayer): tirar o que é bonito mas não ensina. Vale para motion decorativo, chip, ícone e enfeite. **23 de 23 experimentos** confirmaram, efeito mediano d = 0,86. | d = 0,86 | sim | [forte] [Mayer, coherence principle](https://www.cambridge.org/core/books/multimedia-learning/coherence-principle/4C1367F7716D91DE196CA8D319DF5FAD) |
| V8 | Pausa depois de uma revelação: o aluno precisa de tempo para ler antes da próxima mudança ("sem espera, o espectador está sempre atrás de você"). Os números que circulam (~2–3 s de pausa depois de uma fórmula) são de guias de terceiros sobre o estilo 3Blue1Brown, não do Grant. | 2–3 s depois do texto-chave | sim | [fraca] guia de terceiros sobre Manim · cruzar com o tempo de leitura da skill hierarquia-visual |

### 2.4 Som e música

| # | Regra | Número | Tutorial? | Fonte |
|---|---|---|---|---|
| S1 | Entrega em **-14 LUFS integrado**, pico verdadeiro ≤ **-1 dBTP**. O YouTube só **abaixa** o que passa de -14, nunca aumenta o que está baixo. O "Stats for nerds" mostra a "content loudness". | -14 LUFS / -1 dBTP | sim | [média] [IRPR Sound](https://sounddesign.irpr.agency/guides/how-to-mix-audio-for-youtube/) · [Youlean](https://youlean.co/?p=30813) |
| S2 | Música por baixo da fala: **15–20 dB abaixo** da voz, subindo só nos buracos sem fala. | 15–20 dB | sim | [média] IRPR Sound (mesmo link) |
| S3 | Norma de acessibilidade: fundo **≥ 20 dB abaixo** da fala ("cerca de 4× mais baixo"). Exceção para sons de 1–2 s. | ≥ 20 dB | sim | [forte] [WCAG 2.2, 1.4.7](https://www.w3.org/WAI/WCAG22/Understanding/low-or-no-background-audio.html) |
| S4 | Música e efeitos **pioram** a retenção e a transferência numa explicação narrada (Moreno & Mayer 2000, 2 experimentos). Efeito mediano de som irrelevante: **d = 1,11**. Para aula, a música tem que ser fundo de verdade e **sumir ou quase sumir na explicação densa**. | d = 1,11 | sim (é o ponto central) | [forte] [Moreno & Mayer 2000](https://tecfa.unige.ch/tecfa/teaching/methodo/Moreno_Mayer00.pdf) |
| S5 | Ducking: o ataque curto (1–10 ms) tira a música do caminho na hora; o longo (50–200 ms) desce suave. Release a partir de ~100 ms (padrão do Reaper), ratio 4:1 para "música sob fala". O auto-ducking do Premiere trabalha com redução de -12 a -18 dB e fades de centenas de ms. Para nós (música já baixa): **fade de 300–800 ms**, sem "bombear" a cada palavra. | ataque 50–200 ms · release ≥ 300 ms | sim | [fraca/média] [Vindral docs](https://composer-docs.vindral.com/operators/operators-sidechain-ducking.html) · [Adobe, auto ducking](https://www.adobe.com/learn/premiere-pro/web/automatic-audio-ducking) |
| S6 | Efeito sonoro com parcimônia: muitos efeitos "ficam pouco profissionais". O whoosh tem que ter **a mesma duração da transição**: começa e termina com o movimento e chega ao pico no instante do corte. Clique de mouse sintético só para chamar atenção num clique importante. | duração = transição | sim (pouco) | [média] [Storyblocks](https://www.storyblocks.com/resources/?p=435) · [TechSmith](https://www.techsmith.com/learn/tutorials/camtasia/sound-effects/) · [Krotos](https://krotos.studio/guide/4-whoosh-sound-effects-tips) |
| S7 | Música alta piora a **legenda automática** do YouTube, que já acerta só ~60–90%. Mais um motivo para 25 dB. | — | sim | [fraca] [Riverside](https://riverside.com/blog/youtubes-automatic-subtitles) · [Swarthmore](https://kb.swarthmore.edu/wiki/Auto-Captioning_Video_in_YouTube) |

**Conclusão sobre o nível da música (18 × 25 dB).** As referências de YouTube em geral pedem 15–20 dB, e a norma de acessibilidade pede ≥ 20 dB. A pesquisa de aprendizagem diz que, em explicação, quanto menos música melhor. Os **18 dB** ficaram abaixo da norma, e o dono estava certo em achar alto. Os **25 dB** estão acima do mínimo e combinam com aula.

Padrão proposto: **25 dB abaixo da voz durante a fala (faixa 22–28; reprovar abaixo de 20)**, medido em LUFS de curto prazo nas janelas com fala. Sobe para ~12–15 dB abaixo do nível da voz só em buraco de **≥ 2 s** sem fala, e no fechamento.

### 2.5 Retenção (gráfico do YouTube Studio)

| # | O que o gráfico mostra | Causa típica | O que a edição faz | Fonte |
|---|---|---|---|---|
| T1 | **Intro** baixa (% depois de 30 s) | A abertura não confirma o título/thumb, ou demora para começar | Provar o título em ≤ 10–15 s, cold open com o resultado | [forte] [YouTube Help](https://support.google.com/youtube/answer/9314415) |
| T2 | **Queda (dip)** num ponto | Gente pulando ou saindo: trecho morto, repetição, conteúdo fora do prometido | Cortar, encurtar ou mover. É lá que a próxima edição aprende | [forte] YouTube Help |
| T3 | **Pico (spike)** | Rever ou compartilhar. Pode ser ótimo **ou trecho confuso que o aluno reviu** | Num tutorial, pico em passo técnico = passo rápido demais. Pôr zoom ou motion ali | [forte] YouTube Help |
| T4 | **Top moments** | Ninguém sai | Puxar esse tipo de trecho mais para o começo nos próximos vídeos | [forte] YouTube Help |
| T5 | "Typical retention" | Compara com os **seus últimos 10 vídeos de duração parecida** | Medir "cada vídeo melhor que o anterior" por aqui, não por um % absoluto | [forte] [YouTube Help](https://support.google.com/youtube/answer/1715160?hl=en-GB) |
| T6 | "Não existe vídeo com 70% de retenção" | Mito do % mágico | Comparar com o próprio nicho | [média] Mario Joos, via Vidpros |
| T7 | Queda forte nos últimos 20 s | As pessoas saem antes da tela final: problema de ritmo do fim | Fechamento curto, tela final dentro dos 5–20 s | [fraca] [TubeMilestone](https://tubemilestone.com/blog/youtube-end-screen-ctr) |
| T8 | Primeira queda grande entre 25–35 s | Atenção cai depois da promessa | Primeira mudança visual forte (motion, troca de plano) por volta dos 25–35 s | [fraca] [AIR Media-Tech](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8) |

Os key moments só aparecem em vídeo com ≥ 60 s e ≥ 100 views ([YouTube Help](https://support.google.com/youtube/answer/9314415)).

### 2.6 Capítulos e legendas

| # | Regra | Número | Tutorial? | Fonte |
|---|---|---|---|---|
| C1 | Capítulos na descrição: o primeiro em **00:00**, no mínimo **3**, em ordem crescente, cada um com **≥ 10 s**. | 00:00 · ≥ 3 · ≥ 10 s | sim | [forte] [YouTube Help, capítulos](https://support.google.com/youtube/answer/9884579) |
| C2 | Tutorial é usado para pular e rever (R4). Capítulos transformam "não achei, vou embora" em "pulo para a parte". Os números de "+X% de retenção" que circulam (8–64%) são de blogs e não confiáveis; a lógica do Guo basta. | — | sim | [forte] Guo 2014 · [fraca] [TimeSkip](https://timeskip.io/blog/how-to-increase-youtube-watch-time) |
| C3 | Capítulo na tela + capítulo na descrição com **o mesmo nome**. A gente já faz o da tela. | — | sim | — |
| C4 | Legenda longa: em vídeo longo, o espectador prefere legenda **que se liga e desliga** (.srt enviado ao YouTube). Legenda queimada fixa numa aula irrita. Isso bate com a regra do dono (legenda corrida só se pedir). | — | sim | [fraca] [OpenClip](https://openclip.app/learn/burned-in-captions.md) |
| C5 | A legenda automática erra muito (60–90%). Enviar .srt próprio (temos `palavras-final.json` com tempo por palavra) melhora acessibilidade e busca. | — | sim | [fraca/média] [Swarthmore](https://kb.swarthmore.edu/wiki/Auto-Captioning_Video_in_YouTube) · [UConn](https://accessibility.its.uconn.edu/youtube) |

---

## 3. O que o pipeline JÁ faz bem e o que FALTA

### Já faz bem (manter)
- **Limpeza impiedosa antes de efeito** (R10): silêncio, gaguejada, recomeço e caminho abandonado, com motivo por corte (`narrativa.md`, `cortes.md`).
- **Corte no fim da ideia** (R2): "prefira cortar em fim de frase", e o `ouvir_emendas.py` confere.
- **Respiro natural** (R9): pausa ≥ 0,6 s encurtada, mantendo 0,2 s / 0,15 s, sem cortar toda respiração.
- **Ritmo de fala sem acelerar** (R6): ~190 ppm na aula SLA, e nada de 4×.
- **Sinalização** (V1, V2): zoom que segue a ação, até 1,6×, parado ≥ 4 s.
- **Ideia errada antes da certa** (E7): o motion "A pegadinha" (RESPONDIDO? → NO VÁCUO) é exatamente isso.
- **Capítulos na tela** (C3) e **fechamento com resumo** (E8).
- **Loudness** (S1): -14 LUFS em duas passadas, pico verdadeiro -1,5, medido e reprovado na revisão.
- **Sincronia e qualidade técnica**: acima do padrão de mercado (0–1 ms medido).

### Falta (por prioridade)

| Prioridade | Lacuna | Evidência no nosso último vídeo | Regra |
|---|---|---|---|
| **P1** | **Trilha sem medida nem ducking.** O nível é ajustado à mão por LUFS integrado (voz -14 × trilha ~-32 → "~18 dB"). Nenhum script mede a diferença **durante a fala**, a música não desce sozinha na fala nem sobe nos buracos, e a revisão não confere nada disso. | "música alta" (v1 a 18 dB → v2 a 25 dB, ajustada à mão) | S2–S5 |
| **P1** | **Tomada repetida distante passa pela revisão.** O `revisar.py` só acha repetição **colada** ("eu vim cá eu vim cá"). A tomada errada a 2–8 s da certa (o caso das 8 da aula SLA) só é pega se alguém rodar `ilhas.py` à mão. | "falei errado, cortou, falei certo, mas a vez errada ainda pegou" | R10, T2 |
| **P1** | **Motion "bugado" (sobreposição) não é medido.** O `conferir_hierarquia.mjs` mede tamanho, contraste, zona segura e tempo de leitura, mas **não acha dois elementos ocupando o mesmo lugar ao mesmo tempo**. | "A pegadinha" com elementos sobrepostos, refeito em 16/10 | V7, V8 |
| **P2** | **Gancho dos 30 s não é conferido.** A aula SLA abre bem (dor + promessa), mas com o resultado só dito, não mostrado, e o nome do assunto ("é SLA") só aos ~30 s. Ninguém mede "em quantos segundos o título é provado". | abertura de 0–32 s | E1–E5, T1 |
| **P2** | **Capítulos não saem para a descrição.** Há 5 capítulos na tela (47 s, 86 s, 131 s, 215 s, 267 s), mas não há arquivo com `00:00 Introdução …` para colar no YouTube. Sem o 00:00, o YouTube nem mostra os capítulos. | `edicao.json` → `capitulos` | C1, C2, R4 |
| **P2** | **Trechos longos sem mudança visual não são medidos.** Na aula SLA há ~87 s entre o motion 01 (30,8 s) e o 02 (117,7 s) e ~86 s entre o 03 e o 04. Zoom e capítulo cobrem parte disso, mas ninguém mede o maior trecho sem nada mudando. | intervalos dos motions | V5, T8 |
| **P3** | **Sem .srt.** Temos tempo por palavra, mas não entregamos legenda para enviar ao YouTube (que não é a legenda queimada que o dono não quer). | — | C4, C5 |
| **P3** | **Fechamento sem espaço para a tela final.** O card de fechamento não reserva lugar para os 4 elementos nos últimos 5–20 s. | `05-fechamento` | E9 |
| **P3** | **Sem candidatos de thumb e título.** A edição sabe qual é o quadro mais forte (motion-herói), mas não entrega 3 opções para o A/B test do YouTube. | — | E11, E12 |
| **P3** | **Sem ciclo com o gráfico de retenção.** "Cada vídeo melhor que o anterior" não usa a retenção real (Intro %, dips) do vídeo publicado. | — | T1–T5 |
| P4 | **Sem J/L-cut** na entrada e saída de motion de tela cheia e na troca de capítulo (hoje tudo entra seco com a voz). Ganho pequeno; só vale fazer se o render permitir sem mexer na sincronia. | — | R8 |
| P4 | **Efeito sonoro** (whoosh na entrada de motion, toque no capítulo) não existe. A pesquisa diz para usar pouco, então é baixa prioridade e opcional. | — | S4, S6 |

---

## 4. Proposta: 9 melhorias concretas

Nada disto foi aplicado. É proposta para o dono aprovar. Os textos sugeridos estão prontos para colar.

### M1 (P1): nova referência de som e trilha medida
**Criar** `~/.claude/skills/edicao-video/references/som.md`:

```markdown
# Som: voz, trilha e efeitos

## Trilha por baixo da voz (aula, tutorial, YouTube)
- **Nível: 25 dB abaixo da voz durante a fala** (faixa 22–28). Nunca menos de 20 dB (WCAG 1.4.7).
  O dono reprovou 18 dB ("alta") e aprovou 25 dB (aula SLA, 16/10/2026).
- Medir em **LUFS de curto prazo (3 s) só nas janelas com fala** (tirar de `palavras-final.json`),
  não no integrado do arquivo inteiro: o integrado esconde trecho em que a música sobe.
- **Ducking por script** (`scripts/trilha.py`): a trilha desce com a fala e sobe só em buraco ≥ 2 s
  sem fala (até ~12–15 dB abaixo do nível da voz), com fade de 300–800 ms. Nada de "bombear" a cada palavra.
- **Explicação densa** (passo técnico, configuração campo a campo): a trilha pode cair mais (30 dB) ou
  sair. Pesquisa (Moreno & Mayer 2000; coerência de Mayer): música atrapalha o aprendizado.
- Fechamento sem fala: sobe (~-22 LUFS) e termina em fade.
- Trilha sem direitos, com licença em `musica/LICENCAS.md`.

## Voz
- Cadeia atual: highpass 70 Hz + compressor 2,5:1. Respiração alta: reduzir ~6 dB, não apagar.
- -14 LUFS integrado, pico verdadeiro ≤ -1 dBTP (o YouTube só abaixa, nunca aumenta).

## Efeitos (opcional, pouco)
- Só na entrada de motion de tela cheia e no capítulo. Whoosh com **a duração da transição**,
  pico no instante do corte, ~15–20 dB abaixo da voz. Nunca durante a fala explicando passo.
- Nada de efeito em clique comum de tela.
```

**Criar** `scripts/trilha.py`. Ele recebe `voz.wav`, as trilhas e `palavras-final.json`, gera a curva de volume (janelas de fala + buracos ≥ 2 s), monta `trilha.wav` e imprime: "durante a fala: trilha X dB abaixo da voz (mediana / pior janela)". O `gerar_remotion.py` e o `render.py` passam a usar a trilha que sai dele.

No `SKILL.md`, **passo 12**, acrescentar: "Trilha (vídeo de YouTube): `PY scripts/trilha.py …` (ver `references/som.md`). Alvo: 25 dB abaixo da voz na fala."

### M2 (P1): a revisão mede a trilha
**Em** `~/.claude/skills/revisao-video/SKILL.md`, depois do item 2b:

```markdown
2c. **Trilha × voz** (vídeo com música; com `--voz voz.wav --trilha trilha.wav` ou separando pelo
   final): LUFS de curto prazo nas janelas com fala. **Reprova se a trilha ficar a menos de 20 dB da voz
   em qualquer janela de fala**; alvo 25 dB (22–28). Relatório: mediana, pior janela e o tempo dela.
   Sem as faixas separadas: diga que não mediu e peça o `voz.wav`/`trilha.wav` à edição.
```

**Em** `revisar.py`, nova seção `## 1c. Trilha × voz`. Como os dois wav já existem no projeto (`aula-sla-v2-voz.wav`, `musica/trilha.wav`), a medida é direta com `ebur128` do ffmpeg em cada faixa, cruzada com as janelas de fala.

### M3 (P1): a revisão acha tomada repetida distante
**Em** `revisao-video/SKILL.md`, item 4, trocar por:

```markdown
4. **Repetições:** (a) coladas, gaguejada que sobrou; (b) **tomada repetida distante**: o `revisar.py`
   roda `edicao-video/scripts/ilhas.py` no FINAL (`--db -45`) e compara cada ilha com as 3 seguintes
   (mesmas 4+ palavras em sequência, ou semelhança ≥ 0,6). Qualquer par = REPROVADO até alguém ouvir e
   decidir. Foi o problema da aula SLA (8 tomadas erradas).
```

**Em** `revisar.py`: chamar `ilhas.py` no final (já existe) e comparar com `difflib.SequenceMatcher` entre ilhas vizinhas. Sai uma lista "ilha 23 (2:41) ≈ ilha 24 (2:47): '…'".

### M4 (P1): motion sem sobreposição
**Em** `~/.claude/skills/hierarquia-visual/scripts/conferir_hierarquia.mjs` (ou um verificador novo que a revisão chama): amostrar a cena a cada 0,25 s, pegar o retângulo de cada elemento de texto/forma visível (opacidade > 0,1) e **reprovar quando dois textos se cruzam** (interseção > 4% da área do menor) fora de uma lista `permitir-sobrepor`.

**Em** `revisao-video/SKILL.md`, item 7, acrescentar: "inclui **sobreposição** de elementos no tempo (motion 'bugado' da aula SLA: dois textos no mesmo lugar)".

**Em** `edicao-video/references/armadilhas.md`, nova linha:
`| Dono: motion "bugado" (A pegadinha, aula SLA) | Palavra gigante e conversa ocupando o mesmo espaço ao mesmo tempo | Uma palavra gigante por vez, em área própria; verificador de sobreposição antes de gravar |`

### M5 (P2): gancho e re-gancho na decupagem
**Em** `~/.claude/skills/edicao-video/references/narrativa.md`, nova seção depois de "Como fazer":

```markdown
## Gancho (0–30 s) — o YouTube mede ("Intro": % que continua depois de 30 s)
- **0–10 s: provar o título.** De preferência MOSTRAR o resultado funcionando (cold open: a automação
  disparando, o lead recebendo, o painel com o número) — um trecho real de 3–8 s tirado do meio da
  gravação, antes da fala de abertura. Sem "oi, pessoal" antes disso.
- **10–20 s: por que importa** (a dor: "você já teve dificuldade de…").
- **até 30 s: o roteiro em uma linha** ("vou te mostrar a régua, a automação e um teste ao vivo")
  e o nome do assunto dito.
- Primeira mudança visual forte (motion ou troca de plano) entre 25–35 s.
- Se o assunto aparece pela 1ª vez depois de 30 s, puxe a frase para antes ou abra com um motion que o diga.

## Re-gancho a cada ~2–3 min
- Cada capítulo abre com uma frase (falada ou no motion) que lembra o que está em jogo
  ("agora a parte que impede o lead de ficar no vácuo"). Aluno de tutorial assiste 2–3 min e pula (Guo 2014).

## Ideia errada antes da certa
- Quando der, mostre o erro comum antes da solução (Veritasium/Muller: aprendizado ~2×). "A pegadinha"
  da aula SLA é o modelo.

## Fechamento
- Resumo + próximo passo em ≤ 20 s. O card de fechamento deixa **livre** a área da tela final do
  YouTube (até 4 elementos, nos últimos 5–20 s; vídeo ≥ 25 s).
```

### M6 (P2): capítulos para a descrição e .srt
**Em** `edicao-video/SKILL.md`, **passo 14 (Entregar)**, acrescentar:

```markdown
    + `capitulos-youtube.txt` (`scripts/capitulos.py fonte/edicao.json`): começa em `00:00 Introdução`,
      ≥ 3 capítulos, cada um ≥ 10 s, mesmos nomes dos capítulos na tela — pronto para colar na descrição.
    + `legenda.srt` (do `palavras-final.json`, linhas de até 42 caracteres e 2 linhas, 1–6 s cada) para
      ENVIAR ao YouTube como legenda que se liga/desliga. Não é legenda queimada (essa só se ele pedir).
```

`scripts/capitulos.py` é curto: lê `capitulos` do `edicao.json`, insere 00:00 se faltar, junta capítulos com menos de 10 s e escreve `M:SS Nome`. Na aula SLA sairia:
`00:00 Introdução · 00:47 Metas do SLA · 01:26 O que conta no SLA · 02:11 A automação do SLA · 03:35 Teste ao vivo · 04:26 O ajuste final`.

### M7 (P2): mapa de mudança visual
**Em** `edicao-video/references/imagem.md`, nova seção:

```markdown
## Mudança visual (tutorial)
- Conta como mudança: motion, troca de zoom, capítulo, troca de página com fusão, câmera em tela cheia.
- **Alarme (não meta): trecho > 40 s sem nenhuma mudança** → avaliar zoom num detalhe, um motion curto
  de reforço ou corte. Em trecho de rosto: punch-in 1,1× a cada 2–3 cortes, não em todos.
- Teto: no máximo ~3 chamadas/destaques por minuto (alunos acharam 4/min demais).
- Motion que só enfeita sai (coerência de Mayer). Cada motion explica uma ideia da fala.
```

**Em** `plano.py` (ou `render.py --fotos`): imprimir "maior trecho sem mudança visual: 0:31–1:57 (86 s)", juntando `motions`, `zoom.json`, `capitulos` e as emendas com `fusao`.

### M8 (P2): checklist de retenção na revisão
**Em** `revisao-video/SKILL.md`, novo item depois do 5 (leitura como espectador):

```markdown
5b. **Checklist de retenção (aula/tutorial de YouTube)** — responder no relatório, cada item com o tempo:
   | # | Item | Passa quando |
   |---|---|---|
   | 1 | Título provado | o resultado ou a dor do título aparece em ≤ 10–15 s |
   | 2 | Assunto dito | o nome do assunto/ferramenta é dito em ≤ 30 s |
   | 3 | Roteiro | uma frase diz o que vem (2–4 partes) antes de 45 s |
   | 4 | Abertura em movimento | quadro 0 não é tela parada nem preta |
   | 5 | 1ª mudança forte | motion ou troca de plano entre 25–35 s |
   | 6 | Sem trecho morto | nenhum trecho > 40 s sem mudança visual (mapa do M7) |
   | 7 | Re-gancho | cada capítulo abre dizendo o que está em jogo; nenhum bloco > 6 min |
   | 8 | Sem repetição | nenhuma tomada repetida (colada ou distante, item 4) |
   | 9 | Ideia errada tratada | se há uma armadilha comum, ela aparece antes da solução |
   | 10 | Trilha | ≥ 20 dB abaixo da voz em toda janela de fala (alvo 25) |
   | 11 | Capítulos | `capitulos-youtube.txt` com 00:00, ≥ 3, cada ≥ 10 s |
   | 12 | Fechamento | resumo + próximo passo ≤ 20 s; área da tela final livre nos últimos 5–20 s |
   | 13 | Ritmo de fala | ppm do final (≥ 165 está ótimo; se < 140, procurar pausas que sobraram) |
   Itens 1–3, 7 e 9 dependem de leitura (o revisor escreve o tempo e a frase). 6, 8, 10, 11 e 13 são medidos.
   Item 10 ou 8 falhando = REPROVADO. Os outros = aviso ao dono com a sugestão.
```

### M9 (P3): empacotamento e aprender com o gráfico
**Em** `edicao-video/SKILL.md`, **passo 14**, acrescentar: "3 quadros candidatos a thumb (o quadro-herói do motion mais forte, o resultado na tela, o rosto no momento de maior expressão) em `thumbs/` + 3 títulos sugeridos. O YouTube testa até 3 e escolhe pelo tempo assistido, então nada de thumb que promete o que o vídeo não entrega."

**Em** `edicao-video/SKILL.md`, **passo 15 (Aprender)**, acrescentar: "Quando o vídeo tiver ≥ 100 views, pedir ao dono um print da aba Retenção (Intro %, quedas, picos) e anotar no `evolucao.md` da marca: Intro % × retenção típica e o que acontecia em cada queda e em cada pico. Pico em passo técnico = passo rápido demais (pôr zoom ou motion na próxima)."

### Fora das 9 (só se sobrar tempo): J-cut na entrada de motion
No `gerar_remotion.py`, permitir `"jcut": 0.3` por motion: a imagem do motion entra 0,3 s **depois** da palavra que o chama, e na saída a voz continua 0,3–0,5 s sobre a tela antes do corte. Não mexe nos tempos da câmera (o motion já fica por cima), então a sincronia continua por construção.

---

## Fontes (todas as citadas)
- Guo, Kim & Rubin (2014), *How Video Production Affects Student Engagement* (edX, 6,9 M sessões): https://pg.ucsd.edu/publications/edX-MOOC-video-production-and-engagement_LAS-2014.pdf
- Moreno & Mayer (2000), *A Coherence Effect in Multimedia Learning*: https://tecfa.unige.ch/tecfa/teaching/methodo/Moreno_Mayer00.pdf
- Mayer, coherence principle: https://www.cambridge.org/core/books/multimedia-learning/coherence-principle/4C1367F7716D91DE196CA8D319DF5FAD
- Learning Scientists, vídeos instrucionais: https://www.learningscientists.org/blog/2021/7/1-1
- WCAG 2.2, 1.4.7: https://www.w3.org/WAI/WCAG22/Understanding/low-or-no-background-audio.html
- YouTube Help, key moments: https://support.google.com/youtube/answer/9314415 · retenção: https://support.google.com/youtube/answer/1715160 · capítulos: https://support.google.com/youtube/answer/9884579 · tela final: https://support.google.com/youtube/answer/6388789 · A/B test: https://support.google.com/youtube/answer/16391400
- MrBeast, *How to succeed in MrBeast production*: https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/
- Colin and Samir, regras do Paddy Galloway: https://www.colinandsamir.com/resources/the-new-rules-of-youtube-from-paddy-galloway
- Mario Joos (retenção), via Vidpros: https://vidpros.com/retention-editing-what-you-can-learn-from-mario-joos/
- Walter Murch, regra dos 6: https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch · piscar: https://bigthink.com/?p=60362
- Derek Muller (Veritasium), tese: https://thejournal.com/articles/2015/05/05/watching-videos-does-not-necessarily-lead-to-learning.aspx · https://www.scientificamerican.com/article/how-youtube-star-derek-muller-of-veritasium-is-challenging-scientific/
- IRPR Sound, mixagem para YouTube: https://sounddesign.irpr.agency/guides/how-to-mix-audio-for-youtube/
- Youlean, normalização do YouTube: https://youlean.co/?p=30813
- Ducking: https://composer-docs.vindral.com/operators/operators-sidechain-ducking.html · https://www.adobe.com/learn/premiere-pro/web/automatic-audio-ducking
- Efeitos: https://www.storyblocks.com/resources/?p=435 · https://www.techsmith.com/learn/tutorials/camtasia/sound-effects/ · https://krotos.studio/guide/4-whoosh-sound-effects-tips
- TechSmith, editar demo: https://www.techsmith.com/blog/edit-demo-recording/
- Respiração: https://s3.amazonaws.com/izotopedownloads/docs/rx9/en/breath-control/index.html · https://suchavoice.com/?p=16018
- J/L-cut: https://www.capcut.com/create/j-cuts-and-l-cuts-dialogue-edits · https://www.epidemicsound.com/blog/j-cuts-and-l-cuts/
- Punch-in: https://agent.vizard.ai/how-to/stop-the-punch-ins-cycling-too-fast-in-a-talking-head-edit.html · https://1of10.com/blog/what-is-a-jump-cut/
- Ritmo (blogs, fraca): https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/ · https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8 · https://outlierkit.com/resources/youtube-hooks-and-retention/ · https://www.clueso.io/glossary/cold-open
- Legendas: https://kb.swarthmore.edu/wiki/Auto-Captioning_Video_in_YouTube · https://riverside.com/blog/youtubes-automatic-subtitles · https://openclip.app/learn/burned-in-captions.md · https://accessibility.its.uconn.edu/youtube
- Capítulos (fraca): https://timeskip.io/blog/how-to-increase-youtube-watch-time · tela final (fraca): https://tubemilestone.com/blog/youtube-end-screen-ctr

**O que não achei:** nenhuma fonte primária de Paddy Galloway, Ali Abdaal, Fireship, Kurzgesagt ou 3Blue1Brown com números de edição. O que circula sobre eles são blogs de terceiros, marcados como [fraca] quando usados. Não há estudo publicado para "mudança visual a cada X s" em tutorial. Por isso o relatório usa esse número como alarme, não como meta.
