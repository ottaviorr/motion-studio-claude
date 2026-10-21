# 01 — Pop-ups, cards e overlays parciais por cima da gravação (sem trocar a tela)

Pedido do dono (16/10/2026): *"nem sempre eu quero que você faça edição colocando motion na tela inteira. Às vezes eu quero que você jogue um pop-up, alguma mensagem assim por cima da tela, que não troque a tela inteira."*

Complementa, sem repetir: `edicao-video/references/tela-em-cena.md` (a tela ENCOLHE e coisas acontecem em volta) e `references/anotacoes.md` (holofote, lupa, elemento que levanta, seta, passos: tudo APONTA para algo que está na tela). Aqui a tela **fica inteira, do mesmo tamanho**, e um objeto pequeno entra num canto, diz uma coisa e sai. Já existem no `componentes.tsx`: `Capitulo` (etiqueta acima da câmera) e `SeloStatus` (estado no alto, ao centro).

Legenda das fontes: **[medido]** constante lida no código de uma ferramenta aberta · **[doc]** documentação oficial · **[casa]** regra que já existe no estúdio (nivel.md, hierarquia-visual, anotacoes) · **[proposta]** número para começar e ajustar depois de ver no vídeo · **[obs.]** observação geral de estilo de canal/pacote (sem número medido).

---

## 1. Resumo em 5 linhas

1. **Pop-up é para o que NÃO está na tela**: a opinião do dono ("eu gosto de deixar para contar"), uma dica, um aviso, o nome de um termo, o caminho do menu para anotar, e o que acontece fora da tela (a mensagem chegando no celular do lead, a notificação chegando na equipe). O que ESTÁ na tela é anotação (holofote/seta), não pop-up.
2. Números que se repetem nas fontes: **entra em 0,35–0,45 s desacelerando** (`cubic-bezier(.05,.7,.1,1)`, Material 3) e **sai em 0,2–0,25 s acelerando** (`cubic-bezier(.3,0,.8,.15)`; Sonner usa 200 ms na saída e 400 ms na entrada); **viagem curta (24–40 px) vindo da borda mais perto**; vida de **4 s (padrão Sonner/Material), de 4 a 10 s no máximo**; tempo parado ≥ máx(1 s; 0,5 + 0,33 s × palavras) (casa, nível 36).
3. **Onde:** dentro da margem EBU (96 px dos lados, 54 px em cima/embaixo), no canto **oposto à câmera** e **longe de onde o cursor vai trabalhar no próximo segundo** (`atividade.json`); nunca em cima do capítulo, do selo nem da câmera. Tamanho: **22–32 % da largura** para card/toast, ≤ 40 % para lower third, ≤ 10 % da altura para selo/sticker.
4. **Um pop-up por vez**, um a cada 20–40 s no trecho de demonstração (somando com as anotações: ≤ 1 a cada 15 s), e nunca durante o clique que o aluno precisa copiar. Texto de 1 a 4 palavras no grito + no máximo uma linha de apoio; o texto ECOA a fala (mesmas palavras), não compete com ela.
5. No pipeline: **um componente `<PopUp tipo= lado= ini= dur= />`** com entrada/saída/posição comuns e 9 "miolos" (Toast, CardLateral, LowerThird, Selo, Balao, Checklist, Alerta, Caminho, Citacao), lidos da chave **`"popups"`** do `edicao.json` — só CSS por cima da tela, então a sincronia voz × câmera continua por construção. Visual da casa: Archivo + Instrument Serif + JetBrains Mono, retângulo de raio 10 px (não pílula), fio de estado à esquerda, fundo chapado sem vidro, sem halo, sem quique.

---

## 2. Catálogo (14 tipos)

Tamanhos em px da saída 1920×1080. Tamanho de letra pela hierarquia-visual, 16:9 tela cheia [casa]: **rótulo ≥ 26 px, apoio ≥ 36 px, grito 44–56 px; serif só a partir de 56 px**. Isso deixa os cards maiores do que os "toasts de app" (que são feitos para 1 m de distância do monitor, não para vídeo assistido no celular deitado).

Tempo: `T_min = máx(1 s; 0,5 + 0,33 s × palavras)` parado [casa, nível 36] **+ 0,4 s de entrada + 0,25 s de saída**. Quando o texto NÃO é dito pela voz (a voz fala outra coisa), multiplique o parado por 1,5 [proposta: a leitura disputa atenção com a escuta].

### 2.1 Notificação (toast) — "chegou um aviso"
- **Função na fala:** algo que o SISTEMA faz sozinho e manda para alguém: "envio uma notificação interna para a equipe", "o gerente recebe", "o lead recebe um SMS". É a prova de que a automação age fora da tela.
- **Onde:** canto superior do lado oposto à câmera (é onde o macOS mostra os banners [doc]); se o topo tem a ação (botão Salvar do CRM), canto superior do canvas vazio. Pilha de 2–3 cresce para baixo com **14 px** entre eles [medido: Sonner `GAP = 14`, `VISIBLE_TOASTS_AMOUNT = 3`].
- **Tamanho:** 560–620 px de largura (29–32 %), ~170–200 px de altura (3 linhas: app/hora em mono 26, título Archivo 800 44, corpo 36). Sonner usa 356 px de largura em app [medido] — em vídeo precisa quase o dobro.
- **Tempo:** padrão 4 s de vida [medido: Sonner `TOAST_LIFETIME = 4000`; doc: Material snackbar 4–10 s; macOS banner ~5 s]. Toast com número que muda ("20:00") fica até a fala dizer o número + 0,5 s.
- **Entrada/saída:** desce 32 px de cima + opacidade 0→1 em 0,4 s [medido: Sonner `translateY(-100%)` → 0, 400 ms; aqui só 32 px para não varrer a tela]; sai subindo 0,2 s [medido: Sonner `TIME_BEFORE_UNMOUNT = 200`]. Sem overshoot. Toast novo empurra o anterior para baixo em 0,4 s (mesma curva).
- **Não parecer template:** nada de cópia do iOS (ícone redondo de app, vidro fosco, cantos de 20 px). Linha de cima em mono como "carimbo de máquina" (`NOTIFICAÇÃO INTERNA · agora`), título em Archivo 800, fio de estado (laranja/vermelho/verde do SLA) à esquerda. Dado do lead sempre inventado.
- **Exemplos:** [Sonner (código, toasts empilhados)](https://github.com/emilkowalski/sonner) · [Jitter — notificação iOS (modelo)](https://jitter.video/template/simple-notification-ios/) · [Envato — Notifications pack](https://elements.envato.com/notifications-A78P23K) · [Envato — Animated notification pack](https://elements.envato.com/animated-notification-pack-SNXZNYW) · [Motion.dev — notifications stack (280×60, gap 8)](https://motion.dev/tutorials/js-notifications-stack).

### 2.2 Card lateral (dica / opinião / "eu faço assim")
- **Função:** a opinião ou dica do apresentador que não é um passo da tela: "eu gosto de deixar para contar", "recomendo que coloque até menos", "conversa interna: cancela o SLA". Transforma um "tá?" em algo que o aluno guarda.
- **Onde:** encostado numa borda lateral (esquerda ou direita), na metade de cima ou no meio, do lado sem câmera e sem cursor. Nunca no centro.
- **Tamanho:** 520–640 px (27–33 %), até 4 linhas. Rótulo (`DICA`, `EU FAÇO ASSIM`) Archivo 600 caixa-alta 26 px +.06em; grito Archivo 800 caixa-alta 48–52 px com ponto final (o estilo `AVISA.` da aula); apoio Archivo 500 36 px.
- **Tempo:** 3–6 s. Sai quando a fala troca de assunto (≤ 0,5 s depois da última palavra da dica) [casa, anotacoes §3].
- **Entrada/saída:** vem da própria borda, 64 px de viagem, com máscara (o card "sai de dentro" da borda, não flutua do nada) em 0,42 s; o grito sobe 18 px 0,08 s depois do card. Sai voltando para a borda em 0,22 s.
- **Não parecer template:** sem ícone de lâmpada/traço no canto (sinal de IA nº "cartão arredondado + ícone de traço", nível 52); o rótulo já diz o que é. Grito encaixado, alinhado à esquerda.
- **Exemplos:** [Ali Abdaal — texto ao lado do apresentador, frase a frase (análise)](https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/) · [Arcade — callout é para dica/contexto, não para clique; título ≤ 5 palavras](https://docs.arcade.software/kb/build/interactive-demo/edit/hotspots-and-callouts) · [Tella — text overlays para callout e CTA](https://www.tella.com/alternatives/screen-studio.md).

### 2.3 Lower third (nome, termo, ferramenta)
- **Função:** apresentar um NOME na primeira vez que aparece: o apresentador ("Nome do Apresentador · Empresa"), um termo ("SLA · Service Level Agreement"), uma ferramenta ("Conversation AI").
- **Onde:** terço de baixo, no canto oposto à câmera; linha de base a 54 px + altura da legenda do YouTube livre no centro (a legenda CC do player aparece embaixo, no meio [obs.]). Dentro do title-safe [doc: EBU R95 grafismo 5 %; title-safe clássico 80–90 %].
- **Tamanho:** ≤ 40 % da largura (≤ 760 px), 9–12 % da altura (100–130 px). Grito Archivo 900 caixa-alta 56 px + segunda linha Instrument Serif itálico 56 px (serif só ≥ 56) ou mono 26 px.
- **Tempo:** 3,5–5 s; uma vez por termo no vídeo.
- **Entrada/saída:** faixa de tinta abre da esquerda para a direita (`clip-path`) em 0,45 s; palavras sobem 18 px com 0,06–0,08 s entre elas (o "waterfall" do `Capitulo`); sai fechando a faixa no sentido contrário em 0,25 s.
- **Não parecer template:** sem barrinha colorida + caixinha + gradiente de "pacote de lower thirds". Só faixa chapada, tipo grande e uma cor.
- **Exemplos:** [Mister Horse — Editors Bundle (lower thirds/títulos do Animation Composer)](https://aescripts.com/editors-bundle/) · [Envato — call-outs](https://elements.envato.com/call-outs-2FN4ATZ) · [EBU R95 (zonas seguras)](https://tech.ebu.ch/docs/r/r095.pdf) · [Safe area (Wikipedia)](https://en.wikipedia.org/wiki/Safe_area_(television)).

### 2.4 Selo / carimbo (estado curto)
- **Função:** marcar um estado em 1–2 palavras: `TESTE AO VIVO`, `NOVO`, `OPCIONAL`, `PLANO PRO`, `RECOMENDADO`. Diferente do `SeloStatus` (que narra estados que trocam): o selo é um carimbo fixo.
- **Onde:** encostado num canto superior (o oposto da câmera) ou colado a um card/lower third. Não no centro do topo quando o `SeloStatus` estiver ativo.
- **Tamanho:** ≤ 10 % da altura (~64–80 px), 160–360 px de largura. Archivo 800 caixa-alta 30–34 px, +.04em.
- **Tempo:** pode ficar o trecho inteiro (até 30 s) se for estado ("TESTE AO VIVO" durante o teste) — aí é o único pop-up permitido junto com outro.
- **Entrada/saída:** "carimbo": escala 1,12 → 1 e rotação −5° → −2° em 0,22 s, curva de desaceleração forte, sem rebote [proposta]; sai com opacidade em 0,2 s.
- **Não parecer template:** NÃO é a pílula com bolinha pulsando (sinal de IA, nível 52 — o próprio `SeloStatus` atual tem isso e deveria perder a bolinha). Retângulo de raio 4 px, contorno de 2 px na cor do estado, texto na cor do estado.
- **Exemplos:** [Envato — UI notification widgets](https://elements.envato.com/notifications-RTFSCN6) · `SeloStatus` em `componentes.tsx` (a referência do que trocar).

### 2.5 Balão de chat (a mensagem do outro lado)
- **Função:** mostrar o que o LEAD vê/recebe, ou uma pergunta que o aluno faria ("e se o lead responder?"). Na aula SLA: a mensagem "estamos verificando" que a automação manda.
- **Onde:** área vazia da tela (canvas do construtor, lista de conversas), do lado da câmera só se a câmera estiver embaixo e o balão em cima.
- **Tamanho:** máximo 30 % da largura (≤ 560 px), 1–2 linhas de Archivo 500 36 px; rótulo mono 26 px em cima (`SMS · PARA O LEAD`).
- **Tempo:** 2,5–4 s. Pode ter 0,5 s de "digitando" (três pontos) antes do texto, só se a fala tiver uma pausa ali.
- **Entrada/saída:** cresce do "rabo" do balão (transform-origin no canto do rabo), escala 0,92 → 1 + subida de 16 px em 0,35 s; sai com opacidade + 8 px para cima em 0,2 s.
- **Não parecer template:** sem imitar marca (verde do WhatsApp, azul do iMessage, logotipo). Balão osso (#f2eefa) com texto tinta quando o fundo é escuro; tinta com texto osso quando o fundo é claro (a tela do CRM é clara). Diga no ENTREGA: ilustração.
- **Exemplos:** [Envato — reels mobile notification](https://elements.envato.com/reels-mobile-notification-HRYPGJN) · [Envato — online calls](https://elements.envato.com/online-calls-FPRP89X).

### 2.6 Callout com seta (rótulo solto ligado a um ponto)
- **Função:** nomear um elemento da tela SEM escurecer nada. Já está em `anotacoes.md` §2.6 (seta + rótulo) e `tela-em-cena.md` §2.6 (linha até a margem). Aqui só a regra de convivência: **se aponta para a tela, é anotação** e segue as regras de lá (rótulo ≤ 300 px do alvo, seta ≤ 1/4 da largura). Não implementar de novo como pop-up.
- **Exemplos:** [Envato — engineered call-outs](https://elements.envato.com/engineered-call-outs-VQ7AFHU) · [Envato — callout titles and informational pointers](https://elements.envato.com/callout-VKX8TVS).

### 2.7 Mini-gráfico / contador
- **Função:** um número que a fala cita e a tela não mostra bem (tempo, %, quantidade): "você já pega estatísticas", "20 minutos", "3 automações". Só com número REAL ou explicitamente ilustrativo.
- **Onde:** canto superior oposto à câmera ou colado ao card que fala dele.
- **Tamanho:** 260–420 px; número Archivo 900 `tabular-nums` 72–96 px (é o grito), rótulo mono 26 px embaixo. Mini-barra/sparkline ≤ 360 × 80 px.
- **Tempo:** 2,5–5 s; o número "corre" até o valor em 0,6–0,9 s (expo.out) e fica parado ≥ 1,5 s.
- **Entrada/saída:** card entra como 2.2; dígitos rolam 0,18 s cada troca [casa, anotacoes §2.8].
- **Não parecer template:** número gigante + rotulinho só quando o número É o conceito (nível 52). Contador nunca inventado sobre uma espera real que teve corte (anotacoes §2.8).
- **Exemplos:** [Envato — modern call-out titles and data displays](https://elements.envato.com/call-outs-R7UGB5B) · nível 31 (encaixe pela largura).

### 2.8 Citação / frase-chave
- **Função:** a frase que resume o porquê da aula ("você para de perder lead por não atender"). Uma por vídeo, no fim de um bloco, quando a tela está parada.
- **Onde:** faixa de tinta chapada ocupando um lado (40–50 % da largura) ou o terço de baixo, sem cobrir a câmera.
- **Tamanho:** Instrument Serif itálico 64–80 px, até 2 linhas de 3–4 palavras; uma palavra em Archivo 900 na cor de estado.
- **Tempo:** 3–5 s (até 8 palavras: 0,5 + 0,33 × 8 = 3,1 s parado).
- **Entrada/saída:** faixa abre em 0,45 s (como o lower third), palavras entram uma a uma na fala (0,06 s de cascata); sai fechando.
- **Não parecer template:** sem aspas gigantes decorativas, sem fundo desfocado. Ver também "voz em serif" do nível 46.
- **Exemplos:** [Ali Abdaal (frase a frase, palavra-chave na cor)](https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/) · [canal Ali Abdaal](https://www.youtube.com/@aliabdaal).

### 2.9 Checklist que vai marcando
- **Função:** a fala lista 3–5 configurações/decisões em sequência ("automações contam, Conversation AI conta, todos podem desativar"). O aluno sai com o "como eu deixo" no olho.
- **Onde:** coluna lateral (esquerda ou direita) acima da câmera ou do lado oposto, longe do campo que está sendo clicado.
- **Tamanho:** 520–600 px de largura; cada item 64–72 px de altura (caixa 30 px + texto 34 px); máximo 5 itens (≤ 45 % da altura).
- **Tempo:** cada item marca NA palavra (−0,15 s); a lista fica até a última palavra do último item + 1,2 s. Total típico 6–12 s.
- **Entrada/saída:** card entra como 2.2, itens já estão escritos a 45 % de opacidade (o "mapa", segmentação); na palavra o traço do ✓ desenha em 0,25 s (stroke-dashoffset) e o item vai a 100 %. Sai inteiro em 0,25 s.
- **Não parecer template:** caixa quadrada de raio 3 px, ✓ desenhado à mão em traço de 4 px (não emoji ✅); nome da opção em mono quando é o texto exato da tela (é "máquina", nível 53).
- **Exemplos:** [Arcade — callouts descritivos, poucos por passo](https://docs.arcade.software/kb/build/interactive-demo/edit/hotspots-and-callouts) · anotacoes §2.7 (passos numerados, quando é para APONTAR).

### 2.10 Alerta ("cuidado" / "não faça")
- **Função:** o erro comum que custa caro: "esse do SLA eu NÃO coloco", "não marque essa opção", "se fizer isso o lead fica no vácuo". Só 1–2 por vídeo, senão perde a força.
- **Onde:** lado oposto à câmera, metade de cima; perto (≤ 300 px) do elemento se ele estiver visível.
- **Tamanho:** 560–640 px; rótulo `CUIDADO` Archivo 800 caixa-alta 26 px na cor de erro; grito tinta 48 px; apoio 36 px.
- **Tempo:** até o fim da justificativa da fala ("Por quê? Porque…") — 4–8 s.
- **Entrada/saída:** entra como 2.2; 0,45 s depois o fio vermelho do topo enche da esquerda para a direita em 0,3 s (o gesto da cor de estado, nível 51). Nada de tremer (quique/sacudida = sinal de IA).
- **Não parecer template:** sem triângulo amarelo de ⚠ genérico. Card OSSO (claro) para contrastar com os cards tinta — o alerta é o único claro do vídeo.
- **Exemplos:** [Arcade — o que o callout não deve fazer: cobrir a UI que explica](https://docs.arcade.software/kb/build/interactive-demo/edit/hotspots-and-callouts) · [Material — snackbar 4–10 s](https://m3.material.io/components/snackbar/guidelines).

### 2.11 Card de link / recurso
- **Função:** "o template está na descrição", "aula anterior sobre gatilhos", "doc oficial". No YouTube é o que segura o clique fora do vídeo.
- **Onde:** canto inferior oposto à câmera, ou superior esquerdo — **não no canto superior direito quando o vídeo usar os "cards" do YouTube** (o "i" e o teaser do player aparecem ali [obs.]). Nunca nos últimos 20 s (tela final do YouTube [doc]).
- **Tamanho:** 480–560 px; miniatura opcional 160×90 (frame do vídeo citado) + título Archivo 700 34 px + mono 26 px (`↓ DESCRIÇÃO` ou o endereço curto).
- **Tempo:** 4–6 s.
- **Entrada/saída:** como 2.2.
- **Exemplos:** [YouTube end screen (regras de tempo)](https://www.collabpals.com/tools/youtube-end-screen-previewer) · [Tella — CTAs](https://www.tella.com/alternatives/screen-studio.md).

### 2.12 Sticker / reação
- **Função:** humor ou ênfase emocional (Fireship, Linus [obs.]): um "pronto." quando funciona, um "👀" quando algo vai dar errado. No nosso caso: **raramente** (aula de cliente); YouTube próprio do dono pode usar 1–2.
- **Onde:** perto do rosto (fora da moldura da câmera, encostado nela) ou no ponto do resultado.
- **Tamanho:** ≤ 10 % da altura (≤ 110 px).
- **Tempo:** 0,8–1,5 s (é batida, não leitura).
- **Entrada/saída:** carimbo (2.4) em 0,18 s; sai em 0,15 s. Um "pop" de som só se combinar com a trilha.
- **Não parecer template:** nada de emoji 3D genérico, glitch ou partícula (nível 52). Palavra em Archivo 900 com contorno (ex.: `FUNCIONOU.`) é mais "nossa" do que emoji.
- **Exemplos:** [Fireship — densidade de memes e "punch" visual (análise)](https://skills.sh/jarmen423/skills/fireship-video-style) · [canal Fireship](https://www.youtube.com/@Fireship) · [canal Linus Tech Tips](https://www.youtube.com/@LinusTechTips).

### 2.13 Mini-janela flutuante (picture-in-picture de um detalhe)
- **Função:** mostrar DUAS coisas ao mesmo tempo sem trocar a tela: o celular do lead recebendo enquanto o fluxo roda; o histórico de execução enquanto a conversa está aberta; um trecho de outra parte da gravação (recorte do bruto em outro tempo).
- **Onde:** canto oposto à câmera; nunca encostada na câmera (as duas janelas viram "duas câmeras").
- **Tamanho:** 25–33 % da largura (480–640 px), 16:9 ou 9:16 (celular 260×520). Raio 18 px (o mesmo da câmera), sombra igual à da `MolduraMovel`.
- **Tempo:** 3–8 s; se tiver vídeo dentro, o trecho inteiro do que mostra.
- **Entrada/saída:** escala 0,9 → 1 + 24 px vindo do canto em 0,45 s; sai voltando ao canto em 0,25 s. Se a janela "vem de" um ponto da tela, use `CardSalto` (tela-em-cena §2.5).
- **Não parecer template:** sem moldura de iPhone realista de pacote; retângulo com raio e fio de 1 px.
- **Exemplos:** [Remotion Recorder — b-roll por cima da cena (from/durationInFrames)](https://www.remotion.dev/docs/recorder/editing/b-roll) · [canal MKBHD (inserts de detalhe em janela) ](https://www.youtube.com/@mkbhd).

### 2.14 Caminho / atalho (breadcrumb para anotar)
- **Função:** o caminho de menus que o aluno precisa repetir depois ("Automações › Fluxos › + Gatilho › Conversations SLA") ou o atalho de teclado. É a "receita" do trecho.
- **Onde:** canto superior oposto à câmera, alinhado à esquerda.
- **Tamanho:** até 45 % da largura em uma linha; itens em JetBrains Mono 26–28 px (é texto de máquina, o mesmo da tela), o último em Archivo 800 40 px na cor de destaque. Teclas: caixas de 56 px com borda de 2 px.
- **Tempo:** 3–5 s; aparece quando a fala chega no último item (ou logo depois do clique) — nunca antes de ele chegar lá (estragaria o "mapa" da tela).
- **Entrada/saída:** itens entram da esquerda com 0,07 s de cascata, 16 px de viagem; o `›` aparece junto do item seguinte. Sai inteiro em 0,22 s.
- **Exemplos:** [Arcade — callouts de contexto](https://docs.arcade.software/kb/build/interactive-demo/edit/hotspots-and-callouts) · [canal Thomas Frank (atalhos/menus de Notion por cima da tela)](https://www.youtube.com/@Thomasfrank).

---

## 3. Regras de posição, tempo e entrada

### 3.1 Pop-up, anotação, tela em cena ou motion cheio?
| A fala está… | Use |
|---|---|
| apontando um elemento que está na tela ("esse campo aqui") | **anotação** (`anotacoes.md`) |
| explicando um porquê com a tela parada ≥ 4 s, com 2–3 coisas para mostrar | **tela em cena** (`tela-em-cena.md`) |
| dando 1 informação que não está na tela (dica, opinião, nome, caminho, consequência fora da tela) | **pop-up** (este arquivo) |
| explicando um conceito sem tela (abertura, "o que é", fechamento) | **motion em tela cheia** |

### 3.2 Posição
- **Grade de 7 lugares** (`lado`): `sup-esq`, `sup-dir`, `sup-centro`, `esq`, `dir`, `inf-esq`, `inf-dir`. Margem [casa, EBU R95]: **96 px dos lados, 54 px em cima/embaixo**.
- **Zonas proibidas** (o gerador confere quadro a quadro): moldura da câmera + 24 px; etiqueta do `Capitulo` (acima da câmera, 3 s); `SeloStatus` (centro do topo, y 96–170); retângulo da ação = onde o cursor clica/digita de `ini − 0,5 s` até `fim + 0,5 s` (`atividade.json`) + 80 px; as últimas 20 s do vídeo no canto que a tela final do YouTube usa.
- **Regra do lado:** primeiro o canto oposto à câmera (diagonal); depois o lado oposto à ação; empate → em cima (o olho lê de cima e a legenda CC do YouTube fica embaixo no centro [obs.]).
- **Perto do que fala:** se o pop-up fala de um elemento visível, ≤ 300 px dele [casa]. Se não fala de nada visível, o mais longe possível da ação.
- **Contraste:** fundo do pop-up decide pela luz da área (média do recorte do quadro): área clara (CRM, Notion) → card **tinta**; área escura → card **osso**. Contraste do texto ≥ 4,5:1 [casa].

### 3.3 Tempo
- **Entra na palavra:** `ini = t_palavra − 0,15 s` (entre −0,3 e +0,2 s da palavra-gatilho) [casa, Mayer contiguidade temporal].
- **Parado:** `máx(1 s; 0,5 + 0,33 s × palavras)`; ×1,5 se a voz não está dizendo o texto [casa + proposta].
- **Vida total:** 2,5–6 s para quase tudo; checklist e selo de estado podem durar o trecho (≤ 12 s / ≤ 30 s). Nunca > 10 s parado sem mudar nada [doc: Material snackbar 4–10 s].
- **Sai:** ≤ 0,5 s depois da última palavra relacionada; nunca no meio da frase sobre ele; ≥ 0,3 s antes de um motion de tela cheia, de uma costura ou de um `TelaEmCena`.
- **Orçamento:** 1 pop-up visível por vez (exceção: selo de estado + 1; pilha de 2 toasts). No trecho de demonstração, **1 pop-up a cada 20–40 s** e, somado com anotações, ≤ 1 a cada 15 s. No trecho conceitual, 0 (o motion já faz).

### 3.4 Entrada e saída
- **Entrada:** 0,35–0,45 s, `cubic-bezier(.05,.7,.1,1)` (Material 3 "emphasized decelerate" [doc]) — começa rápido e pousa macio. Viagem curta: **24–40 px** para card/toast, 64 px com máscara para card lateral, nunca atravessando a tela. Opacidade chega a 1 em 60 % da entrada. Escala 0,985 → 1 (quase nada).
- **Saída:** 0,2–0,25 s, `cubic-bezier(.3,0,.8,.15)` (Material 3 "emphasized accelerate" [doc]; Sonner 200 ms [medido]) — sempre mais curta que a entrada; volta pela mesma borda.
- **Overshoot:** não para cards, toasts e lower thirds (quique/elástico é sinal de IA, nível 52). Só o carimbo (selo, sticker) pode ter um "assentar" de ≤ 3 % sem voltar.
- **Filhos em cascata:** 0,06–0,1 s entre rótulo → grito → apoio (o card chega primeiro).
- **Som:** nenhum por padrão (som.md: efeito só em motion de tela cheia e capítulo). Toast pode ter um "tic" curto 22–28 dB abaixo da voz se o dono pedir.
- **Repetição de sistema:** o mesmo tipo entra sempre do mesmo jeito no vídeo inteiro (o aluno aprende a "ler" o toast); variedade fica nos motions.

### 3.5 Convivência com a câmera e o cursor
- A câmera é sagrada: nada por cima, nada encostado (≥ 24 px). Pop-up no mesmo lado da câmera só em cima, com ≥ 1/3 da altura de distância.
- Se a câmera muda de canto (`cameras` no `edicao.json`, aula SLA: direita até 182 s, esquerda depois), o `lado: "auto"` muda junto.
- O cursor não pode entrar no pop-up no próximo 1 s (ele "some" atrás do card e o aluno perde o clique). Se não há lugar livre, **não use pop-up**: espere a tela acalmar ou use anotação.
- Zoom ativo (`zoom.json`): o pop-up é desenhado na saída (não acompanha o zoom). Se o zoom anda durante o pop-up, confira o retângulo da ação no fim do trecho também.

---

## 4. Receita no nosso pipeline

### 4.1 `edicao.json` → `"popups"`
No tempo editado (como `motions`, `capitulos`, `selos`). Posição pelo `lado` (o gerador resolve `"auto"`) ou `xy` em px da saída.

```json
"popups": [
  { "tipo": "card",     "ini": 75.80,  "dur": 3.8,  "lado": "inf-esq", "rotulo": "DICA", "grito": "INTERNO? CANCELA.", "apoio": "conversa da equipe não conta no SLA" },
  { "tipo": "checklist","ini": 89.80,  "dur": 10.7, "lado": "dir", "rotulo": "COMO EU DEIXO",
    "itens": [["Automações", "contam", 90.80], ["Conversation AI", "conta", 93.15], ["Quem desativa", "todos", 98.27]] },
  { "tipo": "caminho",  "ini": 134.0,  "dur": 3.0,  "lado": "sup-esq", "itens": ["Automações", "+ Gatilho", "Conversations SLA"] },
  { "tipo": "balao",    "ini": 199.70, "dur": 3.0,  "lado": "sup-esq", "xy": [420, 200], "rotulo": "SMS · PARA O LEAD", "texto": "estamos verificando" },
  { "tipo": "toast",    "ini": 202.60, "dur": 8.9,  "lado": "sup-esq", "app": "NOTIFICAÇÃO INTERNA", "titulo": "Atendimento demorando",
    "texto": "Marina Souza · sem resposta", "cor": "laranja", "trocas": [[209.06, "vermelho", "SLA vencido", "Marina Souza · 20:00 sem resposta"]] },
  { "tipo": "toast",    "ini": 296.20, "dur": 4.25, "lado": "sup-dir", "app": "PARA O GERENTE", "titulo": "Atendimento demorando", "cor": "vermelho", "empurrado": 298.75 },
  { "tipo": "toast",    "ini": 298.75, "dur": 1.70, "lado": "sup-dir", "app": "PARA OS ATENDENTES", "titulo": "Conversa vencida", "cor": "vermelho" }
]
```
- `tipo`: `toast | card | lowerthird | selo | balao | checklist | alerta | caminho | citacao` (contador e mini-janela entram depois).
- `lado`: um dos 7 lugares ou `"auto"`; `xy` sobrescreve. `cor`: nome de estado (`laranja`, `vermelho`, `verde`, `dica`) — uma cor por pop-up.
- `itens[i][2]`, `trocas[i][0]`, `empurrado`: tempos ABSOLUTOS do vídeo editado (o gerador converte para tempo do componente).
- `palavra` (opcional): em vez de `ini`, o gerador acha a palavra em `palavras-final.json` e faz `ini = t − 0,15`.

**Gerador (`gerar_remotion.py`, proposta):** para cada pop-up → `<Sequence from={round(ini·fps)} durationInFrames={round(dur·fps)}>` com o componente; resolve `"auto"` com a câmera do momento (`cameras`), capítulos, selos e `atividade.json`; mede a luz da área num quadro da `aula-sla-vN-tela.mp4` para escolher `tema` tinta/osso; **recusa** (aviso no console) pop-up que cai em zona proibida, que dura menos que `T_min` ou que encosta (< 0,3 s) num motion/costura. Camada: depois das anotações e da câmera, junto do `Capitulo`/`SeloStatus` (anotacoes §4.6), antes das cenas.

**Conferência:** `npx remotion still` em `ini + 0,45`, meio e `fim − 0,3` de cada pop-up; `conferir_hierarquia.mjs` num quadro exportado; contar sinais de IA (nível 52) — meta 0–1.

### 4.2 Componentes (esboço TSX; encaixa no `componentes.tsx`, não foi rodado)

```tsx
// ---------- POP-UPS: overlays parciais por cima da tela (não trocam a tela, não mexem em tempo) ----------
import React from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont as loadArchivo } from "@remotion/google-fonts/Archivo";
import { loadFont as loadSerif } from "@remotion/google-fonts/InstrumentSerif";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";
const { fontFamily: ARC } = loadArchivo("normal", { weights: ["500", "600", "700", "800", "900"], subsets: ["latin", "latin-ext"] });
const { fontFamily: SERIF } = loadSerif("italic", { weights: ["400"], subsets: ["latin", "latin-ext"] });
const { fontFamily: MONO } = loadMono("normal", { weights: ["500", "700"], subsets: ["latin", "latin-ext"] });

const ENTRA = Easing.bezier(0.05, 0.7, 0.1, 1);   // M3 emphasized decelerate: 0,35–0,45 s
const SAI = Easing.bezier(0.3, 0, 0.8, 0.15);     // M3 emphasized accelerate: 0,2–0,25 s
const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const useT = () => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); return f / fps; };

export const COR: Record<string, string> = { laranja: "#f59e0b", vermelho: "#ef4444", verde: "#22c55e", dica: "#e8b867" };
const TINTA = "#15131b", OSSO = "#f2eefa", CLARO = "#f3f1f7";
export type Lado = "sup-esq" | "sup-dir" | "sup-centro" | "esq" | "dir" | "inf-esq" | "inf-dir";
export type Tema = "tinta" | "osso";

// âncora (px da saída 1920×1080, margem EBU 96/54) + direção de onde vem (a borda mais perto)
const ANC: Record<Lado, { x: number; y: number; ax: number; ay: number; vx: number; vy: number }> = {
  "sup-esq": { x: 96, y: 54, ax: 0, ay: 0, vx: 0, vy: -1 },   "sup-dir": { x: 1824, y: 54, ax: 1, ay: 0, vx: 0, vy: -1 },
  "sup-centro": { x: 960, y: 54, ax: 0.5, ay: 0, vx: 0, vy: -1 },
  "esq": { x: 96, y: 300, ax: 0, ay: 0, vx: -1, vy: 0 },      "dir": { x: 1824, y: 300, ax: 1, ay: 0, vx: 1, vy: 0 },
  "inf-esq": { x: 96, y: 1026, ax: 0, ay: 1, vx: -1, vy: 0 },  "inf-dir": { x: 1824, y: 1026, ax: 1, ay: 1, vx: 1, vy: 0 },
};

type Comum = { lado: Lado; dur: number; escala: number; xy?: [number, number]; largura?: number; tema?: Tema; cor?: string };

// ---------- moldura comum: posição, entrada, saída; os miolos só desenham ----------
export const PopUp: React.FC<Comum & { viagem?: number; entra?: number; sai?: number; caixa?: boolean; children: React.ReactNode }> =
({ lado, dur, escala: E, xy, largura = 580, tema = "tinta", cor = COR.dica, viagem = 32, entra = 0.42, sai = 0.22, caixa = true, children }) => {
  const t = useT(); const a = ANC[lado]; const [x, y] = xy ?? [a.x, a.y];
  const e = interpolate(t, [0, entra], [0, 1], { ...cl, easing: ENTRA });
  const s = interpolate(t, [dur - sai, dur], [0, 1], { ...cl, easing: SAI });
  const d = viagem * ((1 - e) + 0.6 * s);                          // entra da borda e volta para ela
  return (
    <div style={{ position: "absolute", left: x * E, top: y * E, width: largura * E,
      transform: `translate(${-a.ax * 100}%, ${-a.ay * 100}%) translate(${a.vx * d * E}px, ${a.vy * d * E}px) scale(${0.985 + 0.015 * e})`,
      transformOrigin: `${a.ax * 100}% ${a.ay * 100}%`, opacity: Math.min(1, e / 0.6) * (1 - s),
      ...(caixa ? { background: tema === "tinta" ? TINTA : OSSO, color: tema === "tinta" ? CLARO : TINTA, borderRadius: 10 * E,
        boxShadow: `0 ${18 * E}px ${48 * E}px rgba(10,8,16,.30), 0 0 0 ${1 * E}px ${tema === "tinta" ? "rgba(255,255,255,.07)" : "rgba(21,19,27,.10)"}`,
        borderLeft: `${6 * E}px solid ${cor}`, padding: `${22 * E}px ${28 * E}px ${24 * E}px` } : {}) }}>
      {children}
    </div>
  );
};

// filho em cascata: sobe 18 px e acende depois do card (atraso em s)
const Sobe: React.FC<{ atraso: number; E: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ atraso, E, children, style }) => {
  const t = useT(); const k = interpolate(t, [atraso, atraso + 0.36], [0, 1], { ...cl, easing: ENTRA });
  return <div style={{ ...style, transform: `translateY(${(1 - k) * 18 * E}px)`, opacity: k }}>{children}</div>;
};
const rot = (E: number, cor: string) => ({ font: `600 ${26 * E}px ${ARC}`, letterSpacing: ".06em", textTransform: "uppercase" as const, color: cor });
const grito = (E: number, px = 50) => ({ font: `800 ${px * E}px ${ARC}`, letterSpacing: "-.025em", lineHeight: 0.95, textTransform: "uppercase" as const });
const apoio = (E: number) => ({ font: `500 ${36 * E}px ${ARC}`, lineHeight: 1.22, opacity: 0.86 });

// ---------- TOAST: carimbo de máquina + título + corpo; troca de estado na palavra; empurrado por um toast novo ----------
export const Toast: React.FC<Comum & { app: string; titulo: string; texto?: string; trocas?: [number, string, string, string?][]; empurrado?: number; alturaPilha?: number }> =
(p) => {
  const t = useT(); const E = p.escala;
  let cor = COR[p.cor ?? "laranja"] ?? p.cor!, titulo = p.titulo, texto = p.texto, k = 1;
  for (const [a, c, ti, tx] of p.trocas ?? []) if (t >= a) { cor = COR[c] ?? c; titulo = ti; texto = tx ?? texto; k = interpolate(t, [a, a + 0.3], [0, 1], { ...cl, easing: ENTRA }); }
  const desce = p.empurrado === undefined ? 0 : interpolate(t, [p.empurrado, p.empurrado + 0.4], [0, 1], { ...cl, easing: ENTRA });
  const a = ANC[p.lado]; const xy = p.xy ?? [a.x, a.y];
  return (
    <PopUp {...p} cor={cor} viagem={32} xy={[xy[0], xy[1] + desce * ((p.alturaPilha ?? 190) + 14)]}>
      <div style={{ display: "flex", justifyContent: "space-between", font: `500 ${26 * E}px ${MONO}`, letterSpacing: ".04em", opacity: 0.62 }}>
        <span>{p.app}</span><span>agora</span>
      </div>
      <div style={{ font: `800 ${44 * E}px ${ARC}`, letterSpacing: "-.02em", marginTop: 8 * E, transform: `translateY(${(1 - k) * 10 * E}px)` }}>{titulo}</div>
      {texto && <div style={{ ...apoio(E), marginTop: 4 * E }}>{texto}</div>}
    </PopUp>
  );
};

// ---------- CARD LATERAL: rótulo + grito + apoio, sai de dentro da borda ----------
export const CardLateral: React.FC<Comum & { rotulo: string; grito: string; apoio?: string }> = (p) => {
  const E = p.escala; const cor = COR[p.cor ?? "dica"] ?? p.cor!;
  return (
    <PopUp {...p} cor={cor} viagem={64}>
      <Sobe atraso={0.06} E={E} style={rot(E, cor)}>{p.rotulo}</Sobe>
      <Sobe atraso={0.14} E={E} style={{ ...grito(E), marginTop: 10 * E }}>{p.grito}</Sobe>
      {p.apoio && <Sobe atraso={0.22} E={E} style={{ ...apoio(E), marginTop: 12 * E }}>{p.apoio}</Sobe>}
    </PopUp>
  );
};

// ---------- LOWER THIRD: faixa chapada que abre da esquerda; grito + segunda linha em serif (≥ 56 px) ou mono ----------
export const LowerThird: React.FC<Comum & { grito: string; linha2?: string; mono?: boolean }> = (p) => {
  const t = useT(); const E = p.escala; const cor = COR[p.cor ?? "dica"] ?? p.cor!;
  const abre = interpolate(t, [0, 0.45], [0, 1], { ...cl, easing: ENTRA }) - interpolate(t, [p.dur - 0.25, p.dur], [0, 1], { ...cl, easing: SAI });
  return (
    <PopUp {...p} caixa={false} viagem={0} largura={p.largura ?? 760}>
      <div style={{ background: TINTA, color: CLARO, padding: `${18 * E}px ${30 * E}px`, clipPath: `inset(0 ${(1 - abre) * 100}% 0 0)`, borderBottom: `${4 * E}px solid ${cor}` }}>
        <div style={{ display: "flex", gap: 14 * E, flexWrap: "wrap" }}>
          {p.grito.split(" ").map((w, i) => <Sobe key={i} atraso={0.12 + 0.07 * i} E={E} style={grito(E, 56)}>{w}</Sobe>)}
        </div>
        {p.linha2 && <Sobe atraso={0.3} E={E} style={p.mono ? { font: `500 ${26 * E}px ${MONO}`, marginTop: 10 * E, opacity: 0.7 }
          : { font: `400 ${56 * E}px ${SERIF}`, lineHeight: 1, marginTop: 4 * E }}>{p.linha2}</Sobe>}
      </div>
    </PopUp>
  );
};

// ---------- SELO: carimbo retangular (sem pílula, sem bolinha), assenta de −5° para −2° ----------
export const Selo: React.FC<Comum & { texto: string }> = (p) => {
  const t = useT(); const E = p.escala; const cor = COR[p.cor ?? "vermelho"] ?? p.cor!;
  const k = interpolate(t, [0, 0.22], [0, 1], { ...cl, easing: Easing.out(Easing.poly(4)) });
  return (
    <PopUp {...p} caixa={false} viagem={0} entra={0.12} largura={p.largura ?? 360}>
      <div style={{ display: "inline-block", padding: `${10 * E}px ${18 * E}px`, border: `${2 * E}px solid ${cor}`, borderRadius: 4 * E,
        background: "rgba(21,19,27,.92)", color: cor, font: `800 ${32 * E}px ${ARC}`, letterSpacing: ".04em", textTransform: "uppercase",
        transform: `scale(${1.12 - 0.12 * k}) rotate(${-5 + 3 * k}deg)` }}>{p.texto}</div>
    </PopUp>
  );
};

// ---------- BALÃO: a mensagem do outro lado (ilustração); cresce do rabo ----------
export const Balao: React.FC<Comum & { rotulo: string; texto: string; digitando?: number }> = (p) => {
  const t = useT(); const E = p.escala; const dig = p.digitando ?? 0;
  const claro = (p.tema ?? "tinta") === "osso";
  return (
    <PopUp {...p} caixa={false} viagem={16} largura={p.largura ?? 560}>
      <div style={{ font: `500 ${26 * E}px ${MONO}`, opacity: 0.7, color: claro ? CLARO : TINTA, marginBottom: 8 * E }}>{p.rotulo}</div>
      <div style={{ display: "inline-block", background: claro ? OSSO : TINTA, color: claro ? TINTA : CLARO, borderRadius: `${22 * E}px ${22 * E}px ${22 * E}px ${4 * E}px`,
        padding: `${18 * E}px ${26 * E}px`, font: `500 ${36 * E}px ${ARC}`, boxShadow: `0 ${14 * E}px ${40 * E}px rgba(10,8,16,.28)` }}>
        {t < dig ? "···" : p.texto}
      </div>
    </PopUp>
  );
};

// ---------- CHECKLIST: itens já escritos a 45 % (o mapa); na palavra o ✓ desenha e o item acende ----------
export const Checklist: React.FC<Comum & { rotulo: string; itens: [string, string, number][] }> = (p) => {
  const t = useT(); const E = p.escala; const cor = COR[p.cor ?? "verde"] ?? p.cor!;
  return (
    <PopUp {...p} cor={cor} largura={p.largura ?? 580}>
      <div style={rot(E, cor)}>{p.rotulo}</div>
      {p.itens.map(([nome, valor, tm], i) => {
        const k = interpolate(t, [tm, tm + 0.25], [0, 1], { ...cl, easing: ENTRA });
        return (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 18 * E, marginTop: 18 * E, opacity: 0.45 + 0.55 * k }}>
            <svg width={30 * E} height={30 * E} viewBox="0 0 30 30">
              <rect x="1.5" y="1.5" width="27" height="27" rx="3" fill="none" stroke="currentColor" strokeWidth="2.5" opacity=".6" />
              <path d="M7 15.5 L13 21 L23.5 8.5" fill="none" stroke={cor} strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"
                strokeDasharray="30" strokeDashoffset={30 * (1 - k)} />
            </svg>
            <span style={{ font: `500 ${28 * E}px ${MONO}` }}>{nome}</span>
            <span style={{ font: `800 ${34 * E}px ${ARC}`, textTransform: "uppercase", marginLeft: "auto", color: k > 0.5 ? cor : "inherit" }}>{valor}</span>
          </div>
        );
      })}
    </PopUp>
  );
};

// ---------- ALERTA: o único card OSSO do vídeo; o fio de erro enche do topo 0,45 s depois ----------
export const Alerta: React.FC<Comum & { grito: string; apoio?: string; rotulo?: string }> = (p) => {
  const t = useT(); const E = p.escala; const cor = COR[p.cor ?? "vermelho"] ?? p.cor!;
  const fio = interpolate(t, [0.45, 0.75], [0, 1], { ...cl, easing: ENTRA });
  return (
    <PopUp {...p} tema="osso" cor="transparent">
      <div style={{ position: "absolute", left: 0, top: 0, height: 8 * E, width: `${fio * 100}%`, background: cor, borderRadius: `${10 * E}px ${10 * E}px 0 0` }} />
      <Sobe atraso={0.06} E={E} style={{ ...rot(E, cor), fontWeight: 800 }}>{p.rotulo ?? "Cuidado"}</Sobe>
      <Sobe atraso={0.14} E={E} style={{ ...grito(E, 48), marginTop: 10 * E }}>{p.grito}</Sobe>
      {p.apoio && <Sobe atraso={0.22} E={E} style={{ ...apoio(E), marginTop: 12 * E }}>{p.apoio}</Sobe>}
    </PopUp>
  );
};

// ---------- CAMINHO: breadcrumb em mono; o último item é o grito na cor ----------
export const Caminho: React.FC<Comum & { itens: string[] }> = (p) => {
  const E = p.escala; const cor = COR[p.cor ?? "dica"] ?? p.cor!; const n = p.itens.length;
  return (
    <PopUp {...p} cor={cor} largura={p.largura ?? 860}>
      <div style={{ display: "flex", alignItems: "baseline", flexWrap: "wrap", gap: 14 * E }}>
        {p.itens.map((it, i) => (
          <Sobe key={i} atraso={0.1 + 0.07 * i} E={E} style={i === n - 1 ? { font: `800 ${40 * E}px ${ARC}`, color: cor, letterSpacing: "-.02em" }
            : { font: `500 ${28 * E}px ${MONO}`, opacity: 0.8 }}>{it}{i < n - 1 ? "  ›" : ""}</Sobe>
        ))}
      </div>
    </PopUp>
  );
};

// ---------- CITAÇÃO: faixa chapada + serif; uma palavra em Archivo na cor ----------
export const Citacao: React.FC<Comum & { frase: string; forte: string }> = (p) => {
  const E = p.escala; const cor = COR[p.cor ?? "dica"] ?? p.cor!;
  return (
    <PopUp {...p} cor={cor} largura={p.largura ?? 860}>
      <div style={{ display: "flex", flexWrap: "wrap", gap: `${4 * E}px ${16 * E}px`, alignItems: "baseline" }}>
        {p.frase.split(" ").map((w, i) => (
          <Sobe key={i} atraso={0.1 + 0.06 * i} E={E} style={w.replace(/[.,]/g, "") === p.forte
            ? { font: `900 ${64 * E}px ${ARC}`, color: cor, textTransform: "uppercase", letterSpacing: "-.03em" }
            : { font: `400 ${68 * E}px ${SERIF}`, lineHeight: 1 }}>{w}</Sobe>
        ))}
      </div>
    </PopUp>
  );
};

// ---------- despachante: o gerador escreve <PopUpDe p={…} escala={E}/> dentro de cada <Sequence> ----------
export const PopUpDe: React.FC<{ p: any; escala: number }> = ({ p, escala }) => {
  const P = { ...p, escala };
  switch (p.tipo) {
    case "toast": return <Toast {...P} />;          case "card": return <CardLateral {...P} />;
    case "lowerthird": return <LowerThird {...P} />; case "selo": return <Selo {...P} />;
    case "balao": return <Balao {...P} />;           case "checklist": return <Checklist {...P} />;
    case "alerta": return <Alerta {...P} />;         case "caminho": return <Caminho {...P} />;
    case "citacao": return <Citacao {...P} />;      default: return null;
  }
};
```
Notas do esboço:
- O gerador converte os tempos absolutos (`itens[i][2]`, `trocas`, `empurrado`) para tempo da `Sequence` (`− ini`) antes de passar.
- `PopUp` usa `left/top` + `translate(-ax%, -ay%)`, então `inf-*` e `*-dir` crescem para dentro da tela sem conta de altura.
- Nada de `backdrop-filter` (vidro), gradiente, `border-radius: 999` ou bolinha pulsando — os quatro sinais de IA que o `Capitulo`/`SeloStatus` atuais ainda têm (vale trocar quando implementar estes).
- Tema "osso" para área escura e para o Alerta; "tinta" no resto (o CRM é claro).

---

## 5. Seis exemplos aplicados à aula SLA (v2)

Tempos no vídeo editado (`v1/fonte/palavras-final.json`; atenção: o `frases-final.txt` é da v1 e está ~3 s adiantado). Trechos de tela livres de motion cheio: 37,4–117,7 · 128,9–172,5 · 193,3–258,5 · 266,5–300,7 s. Câmera: canto inferior **direito** até 182 s, **esquerdo** depois. Já ocupados por outras propostas (não pôr pop-up junto): anotações 54–62 s, 220–238 s e 267–294 s (`anotacoes.md` §5); tela em cena 137–172 s e 242–247 s (`tela-em-cena.md` §5); `SeloStatus` 219,5–240,4 s; capítulos (3 s cada) em 47,4 · 86,3 · 131,0 · 215,1 · 266,7 s.

### Ex. 1 — Dica: conversa interna cancela o SLA (75,80–79,60 s) · `card`
- **Fala:** "caso seja o **atendimento interno** (75,98), para cancelar esse SLA. Eu só cancelo aqui. / **Ou** se for realmente um lead (79,63)…"
- **Tela:** conversa com zoom 1,6× no cabeçalho (chip "4m" e menu de cancelar, no centro-alto). Câmera inferior direita. Livre: lado esquerdo de baixo (mensagens de teste).
- **Pop-up:** `CardLateral`, `lado: "inf-esq"` (x 96, base 1026), 580 px, tinta, fio `dica` (#e8b867). Rótulo `DICA` · grito `INTERNO? CANCELA.` · apoio `conversa da equipe não entra no SLA`. 7 palavras → parado ≥ 2,8 s; vida 3,8 s; sai na palavra "Ou".
- **Por quê:** é uma regra de uso que a tela não diz (o menu só mostra "cancelar"); um "tá" que vira lembrança.

### Ex. 2 — Checklist "como eu deixo" (89,80–100,50 s) · `checklist`
- **Fala:** "Eu gosto de deixar para **contar** (90,95). O Conversation AI é a mesma coisa, **conta** (93,30) ou não… quem pode desativar… Eu, particularmente, deixo **todos** (98,42) os usuários."
- **Tela:** página de configurações do SLA com zoom 1,48× no centro-esquerda (os rádios). Câmera inferior direita; capítulo 2 sai em 89,3 s.
- **Pop-up:** `Checklist`, `lado: "dir"` (x 1824, y 300 → coluna 1244–1824 × 300–620, acima da câmera, que começa em 722), 580 px, fio verde. Rótulo `COMO EU DEIXO`. Itens (mono = texto da tela; grito = escolha): `Automações · CONTAM` ✓ 90,80 · `Conversation AI · CONTA` ✓ 93,15 · `Quem desativa · TODOS` ✓ 98,27. Sai em 100,5 s ("Só que" 100,07 + 0,4).
- **Por quê:** três decisões seguidas que o aluno precisa copiar; a lista inteira aparece a 45 % logo no início (mapa) e cada ✓ marca na palavra. O lado direito da tela, nesse zoom, só tem o fim das frases em inglês, que ninguém está lendo.

### Ex. 3 — O caminho do gatilho (134,00–137,00 s) · `caminho`
- **Fala:** "Aqui agora nas **automações** (129,79), eu… em específico, **Conversations SLA** (132,80). / E nele (134,54)…"
- **Tela:** construtor de fluxo vazio (canvas livre em cima à esquerda); câmera inferior direita com o capítulo 3 acima dela até 134,0 s; às 137,4 s começa a tela em cena (Ideia 1).
- **Pop-up:** `Caminho`, `lado: "sup-esq"`, 860 px, tinta, fio `dica`: `Automações  ›  + Gatilho  ›` **`Conversations SLA`**. Entra em 134,0 (logo que o capítulo sai: um por vez) e sai em 137,0 (0,4 s antes da tela encolher). 5 palavras → parado 2,2 s; cabe.
- **Por quê:** é o único lugar da aula em que o aluno precisa ACHAR um nome em inglês numa lista grande; o caminho fica como receita. Atraso de 1,2 s depois da palavra é aceito aqui porque é resumo (recapitula o que acabou de acontecer), não sinalização.

### Ex. 4 — O que o lead recebe (199,70–202,70 s) · `balao`
- **Fala:** "além de notificar o lead com a mensagem básica, por exemplo, **estamos verificando** (199,87)…"
- **Tela:** construtor do fluxo: no painel da direita ele digita "estamos ve…" na ação SMS (a ação está ali, x > 1150). Câmera inferior esquerda (55,754). Livre: canvas em cima, entre x 400 e 1000.
- **Pop-up:** `Balao`, `xy: [420, 200]`, 560 px, tinta (tela clara), rótulo mono `SMS · PARA O LEAD`, texto `estamos verificando` (o mesmo que ele está digitando), `digitando: 0,4`. Sai em 202,7 s, quando o toast do Ex. 5 entra.
- **Por quê:** mostra o OUTRO lado (o celular do lead) que não existe na tela; o aluno entende que a mensagem do painel vai chegar para alguém. Real × ilustração: o balão é ilustração.

### Ex. 5 — A notificação que chega na equipe (202,60–211,50 s) · `toast`
- **Fala:** "também envio para ele uma **notificação** (202,75) interna para a minha própria equipe, notificando que… o atendimento ideal desse lead já foi **vencido** (209,21), já rompeu os **20 minutos** (210,73)."
- **Tela:** a ação "Notificação interna" aberta no painel da direita (escolhendo tipo de usuário, y ~ 600). Câmera inferior esquerda.
- **Pop-up:** `Toast`, `lado: "sup-esq"` com `xy: [420, 96]` (mesmo lugar do balão, que acabou de sair: o olho já está ali), 600 px, tinta. Linha mono `NOTIFICAÇÃO INTERNA · agora`; título `Atendimento demorando`; corpo `Marina Souza · sem resposta` (lead inventado, o mesmo dos motions); fio laranja. **Troca** em 209,06 ("vencido"): fio vermelho, título `SLA vencido`, corpo `Marina Souza · 20:00 sem resposta`. Sai em 211,5 ("Isso" 211,53).
- **Por quê:** é a prova de que a automação age fora da tela, na palavra; a troca de cor é a mesma régua do SLA dos motions (laranja → vermelho), então ensina sem frase nova.

### Ex. 6 — Fechamento da demo: gerente e atendentes avisados (296,20–300,45 s) · `toast` × 2 (pilha)
- **Fala:** "Inclusive notifico também o **gerente** (296,39) que o atendimento está demorando. E os **atendentes** (298,91) que estão demorando também."
- **Tela:** caixa de conversas (cursor no centro-direita, y ~ 680); câmera inferior esquerda; motion de fechamento em 300,73 s.
- **Pop-up:** dois `Toast`, `lado: "sup-dir"` (x 1824, y 54 → cobre o cabeçalho da conversa por 4 s, onde ninguém está clicando), 560 px, fio vermelho. 1º: `PARA O GERENTE` / `Atendimento demorando` em 296,20. 2º: `PARA OS ATENDENTES` / `Conversa vencida` em 298,75, entrando no topo e **empurrando** o 1º 204 px para baixo (190 + 14) em 0,4 s. Os dois saem juntos em 300,20–300,45 (0,28 s antes do motion).
- **Por quê:** repete o sistema do Ex. 5 (o aluno já sabe ler o toast) e fecha a demo com o "quem recebe" à vista; a pilha mostra que são duas pessoas sem precisar de motion.

### O que eu NÃO faria na aula SLA
- Pop-up de 215 a 240 s (teste ao vivo): já tem `SeloStatus` + lupa; um terceiro elemento vira ruído. Se quiser algo ali, só um `Selo` `TESTE AO VIVO` no `sup-esq` e tirar a bolinha do `SeloStatus`.
- `Alerta` "SLA FICA DE FORA" em 278,4 s **só se** a seta do `anotacoes.md` Ex. 3 não for usada (as duas juntas = dois destaques). Se for usar: `lado: "dir"`, x 1824, y 300, rótulo `CUIDADO`, grito `NÃO MARQUE O SLA.`, apoio `ele não responde o lead`, até 288,5 s (fim do "Por quê?").
- `Citacao` em 253,5–258,3 s ("você para de perder os seus leads por não **atender**"): ficaria bonita, mas cola no motion "A pegadinha" (258,48 s) com 0,2 s de folga — abaixo dos 0,3 s mínimos. Só se o motion andar 0,5 s.
- Sticker/emoji: aula de cliente (cliente B) — não.

---

## Fontes
- [Sonner — código (constantes `TOAST_LIFETIME = 4000`, `GAP = 14`, `TOAST_WIDTH = 356`, `VISIBLE_TOASTS_AMOUNT = 3`, `TIME_BEFORE_UNMOUNT = 200`)](https://github.com/emilkowalski/sonner/blob/main/src/index.tsx) · [estilos (transform/opacity 400 ms; entrada `translateY(-100%)`; pilha com escala de 5 % por posição)](https://github.com/emilkowalski/sonner/blob/main/src/styles.css)
- [Material 3 — snackbar (4–10 s)](https://m3.material.io/components/snackbar/guidelines) · [Flutter — SnackBar.duration (padrão 4 s)](https://api.flutter.dev/flutter/material/SnackBar/duration.html) · [Material 3 — emphasizedDecelerate `Cubic(0.05, 0.7, 0.1, 1.0)`](https://api.flutter.dev/flutter/material/Easing/emphasizedDecelerate-constant.html) · [emphasizedAccelerate `(0.3, 0, 0.8, 0.15)`](https://api.flutter.dev/flutter/material/Easing/emphasizedAccelerate-constant.html) · [Material Components Android — Motion.md](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md)
- [Apple — UNAlertStyle.banner](https://developer.apple.com/documentation/usernotifications/unalertstyle/banner) · [Apple HIG — Notifications](https://developer.apple.com/design/human-interface-guidelines/notifications) · [macOS: banner ~5 s (addictivetips)](https://www.addictivetips.com/mac-os/change-banner-notification-dismiss-time-on-macos)
- [EBU R95 — zonas seguras (grafismo 5 %, ação 3,5 %)](https://tech.ebu.ch/docs/r/r095.pdf) · [Safe area (Wikipedia)](https://en.wikipedia.org/wiki/Safe_area_(television)) · [title/action safe (DEV)](https://dev.to/utilitylab/how-to-calculate-title-safe-and-action-safe-margins-for-video-1ifj)
- [Arcade — hotspots e callouts (título ≤ 5 palavras; callout para dica/contexto; não cobrir a UI que explica)](https://docs.arcade.software/kb/build/interactive-demo/edit/hotspots-and-callouts) · [Supademo — hotspots](https://supademo.com/academy/edit-and-refine/hotspots)
- [Remotion Recorder — b-roll por cima da cena](https://www.remotion.dev/docs/recorder/editing/b-roll) · [Remotion Recorder](https://www.remotion.dev/docs/recorder) · [Tella × Screen Studio (text overlays, callouts, CTAs)](https://www.tella.com/alternatives/screen-studio.md)
- Pacotes AE: [Mister Horse — Editors Bundle](https://aescripts.com/editors-bundle/) · [Motion Designers Bundle](https://aescripts.com/motion-designers-bundle/) · Envato: [call-outs](https://elements.envato.com/call-outs-2FN4ATZ), [engineered call-outs](https://elements.envato.com/engineered-call-outs-VQ7AFHU), [callout titles/pointers](https://elements.envato.com/callout-VKX8TVS), [call-outs + data displays](https://elements.envato.com/call-outs-R7UGB5B), [notifications](https://elements.envato.com/notifications-A78P23K), [UI notification widgets](https://elements.envato.com/notifications-RTFSCN6), [animated notification pack](https://elements.envato.com/animated-notification-pack-SNXZNYW), [notification dynamic island](https://elements.envato.com/notification-dynamic-island-WHHR4XS), [reels mobile notification](https://elements.envato.com/reels-mobile-notification-HRYPGJN) · [Jitter — notificação iOS](https://jitter.video/template/simple-notification-ios/) · [Motion.dev — notifications stack](https://motion.dev/tutorials/js-notifications-stack) · [Ben Marriott — Motion Practice](https://motiondesign.school/courses/motion-practice-with-ben-marriott)
- Estilo de canais [obs.]: [Ali Abdaal (análise do estilo)](https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/) · [Fireship (análise do estilo)](https://skills.sh/jarmen423/skills/fireship-video-style) · [@aliabdaal](https://www.youtube.com/@aliabdaal) · [@Fireship](https://www.youtube.com/@Fireship) · [@LinusTechTips](https://www.youtube.com/@LinusTechTips) · [@mkbhd](https://www.youtube.com/@mkbhd) · [@Thomasfrank](https://www.youtube.com/@Thomasfrank)
- [YouTube — tela final (últimos 5–20 s)](https://www.collabpals.com/tools/youtube-end-screen-previewer)
- Casa: `motion-design/reference/nivel.md` (36, 46, 51–55) · `hierarquia-visual/SKILL.md` (tamanhos 16:9, margem EBU) · `edicao-video/references/anotacoes.md` (§3 clareza, §4.6 camadas) · `tela-em-cena.md` (§2.5 CardSalto, §4 regras) · `som.md` (efeitos).
