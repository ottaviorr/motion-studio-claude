# 02 — Texto de ênfase por cima da gravação (o "textinho na tela")

Pesquisa de 16/10/2026. Pedido do dono: além do motion em tela cheia, às vezes "jogar um textinho na tela" por cima da gravação (tela + câmera de tutorial). **Não é legenda corrida** (essa só quando ele pedir). É uma palavra ou número que aparece quando é dito e some.

Ponto de partida: `skill/reference/tipografia-que-funciona.md`, `nivel.md` 30–60, `hierarquia-visual/SKILL.md`, `edicao-video/references/anotacoes.md` (holofote, lupa, seta, passos: **este estudo não repete isso**, cuida só do TEXTO) e a aula SLA v2 (`projetos/<projeto>/v1/`).

Legenda das fontes: **[medido]** = medi aqui (quadro real + `conferir_hierarquia.mjs`); **[doc]** = documentação ou artigo; **[observação]** = descrição de estilo de terceiros (guias de template, sem número oficial); **[casa]** = regra que já existe no estúdio; **[proposta]** = número para começar e ajustar vendo o vídeo.

---

## 1. Resumo em 5 linhas

1. O texto de ênfase só ajuda quando é **pouca palavra e a palavra-chave da fala**: na meta-análise de Adesope & Nesbit, o texto resumido em palavras-chave ganhou do texto que repete a fala inteira. 1 ou 2 palavras (no máximo 4), aparecendo entre 0,15 s antes e 0,1 s depois da palavra dita, e parado pelo menos máx(1 s; 0,5 + 0,33 s × palavras).
2. Sobre a UI clara do CRM, **testei 7 tratamentos em 4 quadros reais da aula**. Branco com sombra ficou em 1,3–1,7:1 (ilegível). Placa de tinta, papel osso com sombra dura e marca-texto ácido passaram em todos (15–16:1), no branco e no roxo do cabeçalho. Tinta sem placa só passa em área vazia medida. O véu desfocado passa raspando (4,7–6:1) e fica com cara de sujeira.
3. Catálogo com 12 estilos. Para tutorial servem 8: palavra em placa, grito + palavrinha serif, número que conta, pergunta retórica, marca-texto na UI, riscado ou sublinhado à mão, seta à mão com palavra e rótulo documental. Não servem para tutorial: o "text pop" do MrBeast (só 1 por vídeo, como carimbo), a legenda palavra por palavra do Hormozi e da Ali (só se pedir) e o texto atrás do apresentador (só com a câmera grande).
4. Frequência: **2 a 4 textos por minuto** nos trechos de tela, com pelo menos 8 s entre um e outro (o par pergunta → resposta conta como um só). Um texto por vez. Somado às anotações, um sinal novo a cada 8–10 s no máximo, revezando texto → anotação → zoom → motion, e o mesmo estilo no máximo 2 vezes seguidas.
5. Receita: `"textos"` no `edicao.json`, preso à palavra pelo `palavras-final.json` (um resolvedor acha o tempo e a posição livre). O componente Remotion `<TextoEnfase estilo=… palavra=… ini=…/>` tem 6 estilos com Archivo, Instrument Serif e JetBrains Mono. Proponho 8 entradas para a aula SLA (seção 5).

---

## 2. Catálogo: 12 estilos de texto de ênfase

**Números que valem para todos** (16:9, 1920×1080):
- Zona: 96 px dos lados e 54 px em cima/embaixo **[casa]**. Nunca a menos de 40 px da câmera do apresentador, do cartão de capítulo (acima da câmera) ou do selo (alto, centro).
- Lado: o texto fica na metade oposta à ação (cursor ou centro do zoom no `zoom.json`) e, de preferência, no terço de cima.
- Entrada: 0,28–0,5 s com desaceleração forte (expo/quint). Saída: 0,22–0,3 s acelerando (cúbica), terminando ≥ 0,2 s antes de qualquer corte para motion **[casa: nivel 35]**.
- Sem quique em palavra grande. Overshoot só em selo pequeno.
- Cor: um destaque por tela. Vermelho, laranja e verde só como **estado** do SLA (as mesmas cores do `SeloStatus`).

### 2.1 Palavra-chave em placa (keyword pop)
- **Função na fala:** o termo que o aluno precisa lembrar ("métrica real", "combinado"). É a "palavra-chave condensada" que a pesquisa mostra ajudar **[doc]**.
- **Tamanho:** Archivo 900, 96–140 px (9–13 % da altura). Largura ≤ 40 % da tela (≤ 770 px). Se não couber, use condensado (wdth 75–85) ou duas linhas. Nunca abaixo de 72 px **[casa]**.
- **Contraste:** placa de tinta `#16141f` com texto osso `#f4f1ea` = 16,1:1 em qualquer fundo **[medido]**. Folga da placa: .12em em cima, .28em dos lados, .16em embaixo. Canto reto ou 4 px (canto arredondado com ícone é sinal de IA, nivel 52).
- **Tempo:** máx(1 s; 0,5 + 0,33 × palavras). Fica até o fim da frase + 0,3 s, no máximo 4 s (depois disso vira papel de parede).
- **Entrada/saída:** a placa abre como uma cortina da esquerda (clip 0,28 s expo.out); as letras sobem de dentro dela (112 %, 0,026 s entre letras) e a largura vai de 62 → 100 em 0,5 s. Saída: a cortina fecha para a direita em 0,22 s.
- **Denuncia "template":** pílula colorida com gradiente, emoji, sombra suave borrada, Montserrat/Inter, entrar com "pop" elástico.

### 2.2 Grito + palavrinha (frase-tese, estilo keynote)
- **Função:** a frase que resume o porquê ("você para de **perder leads**"), a opinião do apresentador ("eu deixo **todos**").
- **Inspiração:** keynote da Apple, uma frase curta por tela sobre o produto **[observação]**. Aqui é o padrão Nomad do estúdio (nivel 32).
- **Tamanho:** grito Archivo 900 de 110–160 px. Voz em Instrument Serif itálica a 0,4–0,5× (56–72 px; nunca abaixo de 56 **[casa]**), acima e à esquerda do grito.
- **Contraste:** em área vazia medida pode ir sem placa (tinta 18,2:1 no branco **[medido]**). Se a área tiver texto da UI, use papel osso (seção 3).
- **Tempo:** o grito entra na palavra-chave e a voz junto ou 0,12 s depois, nunca antes (nivel 32). Total ≥ 0,5 + 0,33 × palavras.
- **Entrada/saída:** grito por máscara + largura (62 → 100), voz com opacidade + 24 px em 0,5 s quint.out. Saída: largura → 62 com ls +.3em e fade, power2.in, 0,3 s.
- **Denuncia:** duas palavras em itálico, frase inteira gigante, tudo centralizado na tela.

### 2.3 Número que conta (count-up / contagem)
- **Função:** valor dito na fala que importa ("10 minutos", "20", "45 segundos", "2 gatilhos").
- **Tamanho:** número Archivo 800–900 com `tabular-nums` (para os dígitos não pularem), 160–240 px (15–22 %), lh .8, ls −.06em. Unidade em mono 36–48 px +.08em, ou em serif 56–64 px.
- **Tempo:** aparece 0,15 s antes do número dito e conta em 0,5–0,8 s (expo.out), **terminando no valor exato no fim da palavra**. Fica ≥ 1,5 s parado.
- **Regra:** o número tem que bater com o da tela do CRM. Contagem regressiva que atravessa um corte salta junto (`anotacoes.md` 2.8); se houver corte dentro da espera, não conte.
- **Denuncia:** número gigante + rotulinho "sem ser o conceito" (nivel 52), dígitos girando como caça-níquel, casas decimais inventadas.

### 2.4 Pergunta retórica na tela (com "?" visual)
- **Função:** marcar a virada "pergunta → resposta" ("quer dizer o quê?", "Por quê?"). Prende atenção para a resposta.
- **Tamanho:** a frase em Instrument Serif itálica, 72–96 px, palavra por palavra **no tempo de cada palavra dita**. O "?" em Archivo 900 wdth 125, 1,6–2× a frase (140–180 px), um pouco girado.
- **Tempo:** sai quando a resposta começa (+0,2 s). Ou vira a resposta: o "?" é trocado pela palavra-resposta no mesmo lugar (custo zero de olhar).
- **"!" visual:** o mesmo gesto com "!" serve para um aviso real ("não coloque este"). No máximo 1 "?" e 1 "!" por vídeo.
- **Denuncia:** emoji 🤔, "?" em 3D girando, ponto de interrogação em todas as perguntas.

### 2.5 Marca-texto sobre a UI (o highlighter da Vox)
- **Função:** a fala lê uma opção da tela ("contar apenas as mensagens dos fluxos selecionados"). Em vez de escrever de novo o que a UI já diz, **pinte a própria UI**. É a "cor que se espalha pelo próprio objeto", que guiou melhor que seta em Boucheix & Lowe **[doc, via anotacoes.md]**.
- **Como a Vox faz:** traço de cor animado pelo fim do traço (stroke end) e borda irregular com turbulent displace **[doc: aejuice, miracamp]**.
- **Tamanho:** altura = 1,25–1,35× a altura da linha da UI; folga de 6 px nas pontas; inclinação −1 a −2°; borda levemente irregular (semente fixa, nada de tremer por quadro).
- **Contraste:** cor ácida `#c8ff2e` com `mix-blend-mode: multiply` e α .65–.8. O texto preto da UI continua preto, com ~13–15:1 sobre o ácido **[medido no ácido sólido: 15,4:1]**.
- **Legibilidade:** só vale se o texto da UI estiver ≥ 20 px efetivos (zoom 1,6× no CRM). Na tela a 1× (UI de 12–14 px), use lupa (anotações) ou escreva a palavra em placa.
- **Tempo:** o traço anda **com a fala**: começa na primeira palavra marcada e termina na última. Mínimo 0,4 s; acima de 2 s, divida em 2 traços. Sai com fade de 0,3 s.
- **Denuncia:** retângulo perfeito, amarelo-limão a 100 % cobrindo o texto, marca-texto em linha que a fala não leu.

### 2.6 Sublinhado e círculo feitos à mão
- **Função:** pôr peso numa palavra que já está na tela (nossa ou da UI) sem trocar a cor dela.
- **Base:** Rough Notation tem os tipos underline, box, circle, highlight, strike-through, crossed-off e bracket, com padrão de 800 ms, 2 passadas e 5 px de folga **[doc]**. Para vídeo, 800 ms é lento: use 0,3–0,45 s.
- **Tamanho:** traço 0,06–0,08 em (6–9 px numa palavra de 110 px), 0,12 em abaixo da linha de base, passando 4 % de cada lado. Círculo: elipse que não fecha (sobra de 8–12°).
- **Cor:** a cor de estado quando a palavra é um estado ("atrasou" = vermelho do vencido). Senão, tinta.
- **Denuncia:** a mesma curva perfeita em todo sublinhado (varie a semente), sublinhado em palavra que já tem placa e marca-texto.

### 2.7 Riscado (correção / "não é isso")
- **Função:** negar ou mostrar que algo rompeu ("rompeu com o ~~combinado~~", "SLA ~~fica~~ de fora", o "RESPONDIDO?" riscado do motion pegadinha).
- **Tamanho:** linha de 0,08–0,1 em a 0,47 do corpo com lh .84 (nivel 50), medida com `Range` na largura real da palavra, passando 4 % de cada lado, girada −2 a −4°.
- **Tempo:** a palavra aparece primeiro (≥ 0,6 s legível) e o risco anda em 0,3 s (p4out) **na palavra da negação**. Depois a palavra cai para 55 % de opacidade.
- **Denuncia:** risco que não alcança a palavra toda, risco no meio de balão de conversa (nivel 50: o dono achou "bugado").

### 2.8 Seta desenhada à mão + palavra
- **Função:** dar nome a uma coisa da tela ("o gatilho"). Os números de seta e rótulo já estão em `anotacoes.md` 2.6.
- **O que este estudo acrescenta:** a variante "à mão" (estilo Johnny Harris, que usa caneta e papel de verdade **[doc: RNDR]**): traço 5–6 px com ponta aberta de 2 riscos, curva com 15–25 % de flecha, 120–260 px, desenhada em 0,35 s. A palavra fica na ponta de trás em serif itálica 56–64 px (não em mono).
- **Denuncia:** seta de banco de imagens, seta reta com triângulo cheio, seta atravessando a tela.

### 2.9 Rótulo documental (Vox / Johnny Harris: texto sobre imagem)
- **Função:** situar, sem gritar: nome do campo, de onde vem um dado, data ou fonte ("CONFIGURAÇÕES › SLA", "GATILHO · CONVERSATIONS SLA").
- **Base:** editores no estilo Vox/Harris descrevem fontes fixas: sans geométrica no título, serif na citação, mono no dado técnico; texturas de papel; deixar o vídeo respirar **[observação: pedidos de editor no Upwork e Fiverr]**.
- **Tamanho:** mono 500–700, 26–32 px, CAIXA-ALTA, +.08em (+.28em no estilo cinema), com um filete de 2 px de 60–120 px. Placa de tinta α .9 se o fundo for UI.
- **Tempo:** ≥ 1,5 s. Pode ficar enquanto a tela não mudar (é contexto, não ênfase).
- **Denuncia:** mono como enfeite (nivel 53). Use só para coisa de máquina: nome de campo, gatilho, tempo.

### 2.10 Text pop do MrBeast → versão "carimbo"
- **Como é lá:** 3–4 palavras, fonte pesada, entra e sai com pancada e efeito sonoro, várias por minuto **[observação: guias da SendShort e da VidPros]**.
- **Para tutorial:** **não**. Briga com a UI e cansa. O que aproveitamos é 1 "carimbo" por vídeo, no momento da prova ("FUNCIONOU." quando a automação dispara): Archivo 900, 140–200 px, girado −4°, escala 1,15 → 1 em 0,12 s sem quique, tremida de 4 px na tela por 0,15 s e um clique de papel 20 dB abaixo da voz.
- **Denuncia:** carimbo a cada 10 s, amarelo + contorno preto + "BOOM".

### 2.11 Legenda de palavra-chave (Hormozi / Ali Abdaal / Iman Gadzhi)
- **Como é:** Hormozi usa Montserrat Black em caixa-alta, branco com contorno preto, 2–3 palavras por vez e a palavra-chave em amarelo, 2–4 pt maior, na parte de baixo do meio da tela **[observação: SendShort, Kapwing]**. Ali Abdaal escreve ao lado do rosto, frase por frase, com a palavra-chave em amarelo sobre P&B **[observação: Choppity, SendShort]**. Iman Gadzhi usa minúscula, uma cor só, sem palavra fluorescente: parece "premium" **[observação: Submagic]**.
- **Para tutorial:** **não, a menos que o dono peça legenda** (regra da casa). Em tela de software, a faixa de baixo bate na câmera e na UI. O que aproveitamos: (a) **uma** palavra destacada por frase; (b) a contenção do Iman (uma cor só) quando a legenda for pedida.
- **Teste:** o contorno no estilo Hormozi passa no contraste (13:1 medindo o contorno), mas embola na serif e no mono pequenos (seção 3).

### 2.12 Texto atrás do apresentador (text behind subject)
- **Como é:** a palavra gigante fica entre o fundo e a pessoa. O After Effects usa Roto Brush, duplica a camada e põe o texto no meio **[doc: Adobe, Motion Array]**.
- **Para nós:** só quando a câmera é **grande** (abertura de 0–29 s com a câmera em 1040×585, talking head, YouTube sem tela). No cartão de 485×270 do canto não aparece.
- **Como fazer:** máscara com Robust Video Matting (alfa por quadro, `downsample_ratio` 0,25 em HD, GPL-3.0) ou MediaPipe Selfie Segmentation (mais leve, máscara 0–1) **[doc]**. Saída em `camera-alfa.webm` (VP9 com alfa, o Remotion lê). Ordem das camadas: câmera inteira → texto → câmera recortada pela máscara.
- **Tamanho:** grito encaixado na largura, 300–420 px (28–39 % da altura), atrás da cabeça e dos ombros, com o topo das letras visível. Uma vez por vídeo.
- **Denuncia:** borda da máscara tremendo ou com halo (desfoque de 1–2 px na borda, mais erosão de 1 px), cabelo cortado, palavra que a fala não diz.

### O que a pesquisa diz (por que pouca palavra)
- **Redundância:** repetir na tela a fala inteira atrapalha (Mayer). Mas palavras-chave condensadas **ajudam**: no meta-estudo de Adesope & Nesbit (2012), os termos-chave extraídos da narração explicaram boa parte da vantagem de "fala + texto" sobre "só fala" **[doc]**. Texto levemente resumido também ajudou em Yue, Bjork & Bjork (2013) **[doc]**.
- **Contiguidade temporal:** d = 1,31 (`anotacoes.md`). Por isso o texto entra na palavra, nem antes nem depois.
- **Leitura:** a Netflix limita legenda em português do Brasil a 17 caracteres/s para adultos, com 42 por linha **[doc]**. O texto de ênfase fica bem abaixo disso: 1–4 palavras em ≥ 1 s.

---

## 3. Legibilidade sobre a UI clara do CRM (testado)

**Como testei:** montei uma página com 4 quadros reais da `aula-sla-v2.mp4` e o mesmo grupo de texto: rótulo mono 30 px "TEMPO MÁXIMO", grito Archivo 900 112 px "20 MIN." e voz serif 64 px "e nem um a mais". Rodei `hierarquia-visual/scripts/conferir_hierarquia.mjs`, que mede o contraste WCAG/APCA no pixel atrás de cada letra, com 7 tratamentos.

Os 4 quadros:
- 56 s: configurações do SLA, branco cheio de linhas de texto.
- 245 s: construtor de fluxo, branco com nós.
- 100 s: configurações com a barra lateral escura.
- 76 s: o texto cruzando a **faixa roxa do cabeçalho** e o branco da conversa.

Os arquivos ficaram na pasta de rascunho da sessão (`teste.html`, `teste2.html`, `fotos/`).

| Tratamento | UI branca com texto (56/245/100 s) | Roxo + branco (76 s) | Veredito |
|---|---|---|---|
| A. Tinta `#16141f` sem placa | grito 13–18:1 ✓, mas a serif **cruza as linhas da UI** (o medidor não pega a embolação) | rótulo 2,3:1 ✗ no roxo; grito com "fundo agitado" 1,56:1 | Só em **área vazia medida** (seção 3.2) |
| B. Osso + sombra suave (padrão YouTube) | 1,3–1,7:1 ✗ nos 3 textos | serif 1,4:1 ✗ | **Nunca** sobre UI clara |
| C. Osso + contorno de 12 px (Hormozi) | 13–15:1 (medindo o contorno) | grito 2,4:1 em parte ✗ | Lê, mas embola serif e mono e tem cara de CapCut. Não usar |
| D. Placa de tinta, texto osso | **16,1:1** ✓ em tudo | **16,1:1** ✓ | **Padrão** |
| E. Marca-texto ácido `#c8ff2e`, texto tinta | 15,4:1 ✓ | 15,4:1 ✓ | Só na palavra-chave (é o destaque da tela) |
| F. Papel osso `#f2eefa` + filete de 2 px + sombra dura de 10 px | 15,9:1 ✓ | 15,9:1 ✓ | **Padrão em fundo claro** (descola da UI branca pela sombra dura) |
| G. Véu escuro desfocado (42 px) + osso | 4,7–6,4:1, raspando | 4,8–15:1 | Passa, mas parece sujeira cinza na UI. Não usar |

### 3.1 Por que a placa ganha
- A UI do CRM troca de fundo a cada clique: branco `#fff`, cinza `#f2f4f4`, roxo `#2a2759`, barra lateral escura, nós coloridos. Texto que depende do fundo falha em algum quadro: o A falhou no roxo e o B no branco.
- A placa leva o próprio fundo, então o contraste é fixo (16:1).
- Sombra suave não ajuda no branco: ela é cinza claro em volta de letra clara.
- O contorno "resolve" o contraste, mas as letras pequenas viram borrão (6–8 px de contorno numa serif de 64 px enchem os vãos).
- **Placa por GRUPO, não por linha:** três placas soltas (D no teste) ficam com cara de bilhete de sequestro. Uma placa só para o grupo, ou placa só no grito com a voz fora dela sobre área vazia.

### 3.2 Quando dá para ir sem placa (tinta nua)
- Só sobre uma área que fica **vazia durante todo o texto** e com ≥ 40 px de folga de qualquer texto da UI.
- Como medir: no recorte da camada de tela, a densidade de bordas (Canny) < 1,5 % dos pixels e o desvio de luminância < 6 em todos os quadros do intervalo. Isso pega zoom ou rolagem que traga UI para baixo do texto **[proposta]**.
- Na aula SLA, a área de conversa à direita das mensagens (x 1000–1700, y 380–700 a 67–74 s) passa nessa regra.
- O medidor marcou o A como "OK" (18:1) em cima das linhas da UI: **contraste alto não basta**, precisa de vazio.

### 3.3 Regras de posição na aula (16:9)
- **Câmera:** canto inferior direito `[1393, 749, 485, 270]` de 29 a 130,7 s; canto inferior esquerdo `[58, 757, 485, 270]` depois. Texto ≥ 40 px fora disso.
- **Capítulo:** cartão logo acima da câmera (y ~650–740), 3 s. Nenhum texto de ênfase no mesmo lado por 3 s.
- **Selo do teste ao vivo:** alto, centro, de 219,5 a 240,4 s. Nesse intervalo, nada de texto em x 700–1220, y 60–200.
- **Ação:** o centro do zoom (`zoom.json` cx, cy) e o cursor. O texto vai para a metade oposta. Com zoom ≥ 1,4 o texto fica fixo na tela (não "anda" com o zoom). Só o marca-texto, o sublinhado e o riscado sobre a UI seguem a vista (`useAlvo` do `anotacoes.md` 4.2).
- **Terço de cima primeiro:** y 120–420 no lado oposto à câmera.

### 3.4 Cor
- Um destaque por tela: o ácido `#c8ff2e` do site **ou** a cor de estado do SLA (`#f59e0b` laranja, `#ef4444` vermelho, `#22c55e` verde), nunca os dois juntos. O teste com o ácido marcou "3 cores de destaque" porque o roxo do CRM já conta como uma.
- Placa de tinta e papel osso não contam como destaque.

---

## 4. Receita no pipeline

### 4.1 Onde mora: `edicao.json` → `"textos"`
Igual às `anotacoes`: tudo no **tempo editado**. Só que o tempo é achado pela **palavra**, não digitado.

```json
"textos": [
  { "estilo": "pergunta", "palavra": "quer dizer o quê?", "perto": 67, "pos": [1040, 420], "fundo": "nua" },
  { "estilo": "risca", "palavra": "rompeu", "texto": "COMBINADO.", "risca_em": "combinado", "perto": 72, "pos": [1040, 430], "cor": "#ef4444" },
  { "estilo": "numero", "palavra": "dois", "ate": 2, "voz": "que você vai usar", "perto": 151, "pos": [360, 300] },
  { "estilo": "marca-ui", "palavra": "apenas", "ate_palavra": "selecionados", "perto": 272, "alvo": [452, 311, 460, 29] }
]
```
- `palavra` = 1 ou mais palavras seguidas da fala (sem acento e sem pontuação na hora de comparar). `perto` = tempo aproximado, para escolher a ocorrência certa.
- `texto` = o que aparece. Se faltar, é a própria `palavra` em caixa-alta + ponto final.
- `pos` = canto superior esquerdo do grupo em px da saída. Se faltar, o resolvedor escolhe.
- `alvo` (marca-ui) = retângulo em px da saída no quadro da palavra. No pipeline completo, é `[x, y, w, h]` do bruto 0–1, convertido pelo `vista.json` (`anotacoes.md` 4.2).

### 4.2 Resolvedor: `scripts/textos.py` (proposta)
Lê `edicao.json` e `palavras-final.json` e escreve `fonte/textos-resolvidos.json` com `ini`, `fim` e os tempos relativos de cada palavra.

```python
import json, re, unicodedata
def norm(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode())

def achar(pal, frase, perto):
    alvo = [norm(w) for w in frase.split()]
    achados = [i for i in range(len(pal) - len(alvo) + 1)
               if [norm(pal[i + k]["w"]) for k in range(len(alvo))] == alvo]
    if not achados: raise SystemExit(f"palavra não achada: {frase}")
    i = min(achados, key=lambda i: abs(pal[i]["t"] - perto))
    return i, i + len(alvo) - 1

def leitura(n): return max(1.0, 0.5 + 0.33 * n)          # hierarquia-visual

def resolver(t, pal, ed):
    i, j = achar(pal, t["palavra"], t["perto"])
    ini = pal[i]["t"] - 0.10                               # entra 0,1 s antes da palavra (−0,15 a +0,1)
    k = j                                                  # fim da frase: próxima pontuação
    while k < len(pal) - 1 and not pal[k]["w"].endswith((".", "?", "!")): k += 1
    n = len((t.get("texto") or t["palavra"]).split()) + len((t.get("voz") or "").split())
    fim = min(max(ini + leitura(n), pal[k]["e"] + 0.30), ini + 4.0)
    # não atravessa motion: sai 0,2 s antes do próximo
    for m in ed["motions"]:
        if ini < m["ini"] < fim + 0.2: fim = m["ini"] - 0.2
    if fim - ini < leitura(n): print(f"AVISO: '{t['palavra']}' fica {fim-ini:.2f}s (< leitura {leitura(n):.2f}s)")
    # palavras com tempo relativo (pergunta revela no tempo de cada palavra; risca_em acha o tempo do risco)
    t["palavras"] = [{"w": p["w"], "t": round(p["t"] - ini, 3)} for p in pal[i:k + 1]]
    if "risca_em" in t: t["risca_t"] = round(pal[achar(pal, t["risca_em"], t["perto"] + 1)[0]]["t"] - ini, 3)
    if "ate_palavra" in t: t["ate_t"] = round(pal[achar(pal, t["ate_palavra"], t["perto"] + 1)[1]]["e"] - ini, 3)
    t["ini"], t["fim"] = round(ini, 3), round(fim, 3)
    return t
```

Conferências do resolvedor (avisos, não erro):
- Menos de 8 s do texto anterior, exceto pares marcados com `"par": true`.
- Dentro de motion, de capítulo (±3 s, mesmo lado) ou de selo.
- `pos` dentro da câmera (+40 px).
- Mais de 2 iguais seguidos ou mais de 40 % do mesmo estilo.
- Área sem vazio (seção 3.2) com `fundo: "nua"`: troca sozinho para `"papel"`.

O `gerar_remotion.py` cria um `<Sequence from={round(ini·fps)} durationInFrames={round((fim−ini)·fps)}>` por texto, igual aos capítulos. Ordem das camadas: Tela → anotações que escurecem → **marca-ui / risca sobre a UI** → anotações que flutuam → **TextoEnfase (placa, grito, número, pergunta)** → Câmera → Capítulo/Selo → Cenas.

### 4.3 Componente Remotion (esboço; encaixa no `componentes.tsx`)
Usa as fontes locais do portfólio (a Archivo do Google Fonts no Remotion não garante o eixo de largura). Copie `fontes/` de `projetos/<projeto>/02-filme-c/fonte/` para `remotion/public/fontes/`.

```tsx
// ---------- TEXTO DE ÊNFASE (esboço) ----------
import React, { useMemo } from "react";
import { AbsoluteFill, continueRender, delayRender, Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const expoOut = Easing.out(Easing.exp), quintOut = Easing.out(Easing.poly(5)), p3in = Easing.in(Easing.poly(3)), p4out = Easing.out(Easing.poly(4));
const TINTA = "#16141f", OSSO = "#f4f1ea", PAPEL = "#f2eefa", ACIDO = "#c8ff2e";

// fontes locais, carregadas antes do quadro 0 (font-display:block do estúdio)
const fontesProntas = (() => {
  if (typeof document === "undefined") return;
  const h = delayRender("fontes do TextoEnfase");
  const ff = [
    new FontFace("Archivo", `url(${staticFile("fontes/Archivo-100-900-latin.woff2")})`, { weight: "100 900", stretch: "62% 125%" }),
    new FontFace("Archivo", `url(${staticFile("fontes/Archivo-100-900-latin-ext.woff2")})`, { weight: "100 900", stretch: "62% 125%", unicodeRange: "U+0100-024F" }),
    new FontFace("Instrument Serif", `url(${staticFile("fontes/InstrumentSerif-italic-400-latin.woff2")})`, { style: "italic", weight: "400" }),
    new FontFace("JetBrains Mono", `url(${staticFile("fontes/JetBrainsMono-normal-700-latin.woff2")})`, { weight: "700" }),
  ];
  Promise.all(ff.map((f) => f.load())).then((ok) => { ok.forEach((f) => document.fonts.add(f)); continueRender(h); });
})();

// encaixa a palavra numa largura, medindo com a largura FINAL (nivel 48)
const useEncaixe = (texto: string, largura: number, stretch: number, peso = 900) => useMemo(() => {
  if (typeof document === "undefined") return 120;
  const s = document.createElement("span");
  s.style.cssText = `position:absolute;visibility:hidden;white-space:nowrap;font:${peso} 200px Archivo;font-stretch:${stretch}%;letter-spacing:-.045em`;
  s.textContent = texto; document.body.appendChild(s);
  const w = s.getBoundingClientRect().width; s.remove();
  return Math.min(160, (200 * largura) / w);              // teto de 160 px: ênfase, não pôster
}, [texto, largura, stretch, peso]);

type Pal = { w: string; t: number };
export type TextoProps = {
  estilo: "placa" | "grito-voz" | "numero" | "pergunta" | "marca-ui" | "risca";
  palavra: string;           // texto principal (já em caixa-alta quando é grito)
  ini?: number;              // só documentação: quem posiciona no tempo é a <Sequence>
  dur: number;               // fim − ini (s)
  pos?: [number, number];    // canto superior esquerdo do grupo (px da saída 1920×1080)
  voz?: string;              // palavrinha serif (grito-voz, numero)
  rotulo?: string;           // mono (placa, numero)
  largura?: number;          // largura máxima do grito (px), padrão 640
  fundo?: "placa" | "papel" | "nua";
  cor?: string;              // estado (risca/sublinha) ou ACIDO (marca-ui)
  palavras?: Pal[];          // tempos relativos (pergunta)
  risca_t?: number;          // quando o risco anda (risca)
  ate?: number; de?: number; // número que conta
  alvo?: [number, number, number, number]; // marca-ui: retângulo da linha da UI no quadro (px da saída)
  ate_t?: number;            // marca-ui: quando o traço chega ao fim (fim da última palavra marcada)
  escala: number;            // E = saída/1920
};

const saida = (t: number, dur: number, d = 0.25) => 1 - interpolate(t, [dur - d, dur], [0, 1], { ...clamp, easing: p3in });

// fundo do grupo: placa de tinta (padrão sobre UI), papel osso com sombra dura, ou nada (área vazia medida)
const caixa = (fundo: TextoProps["fundo"], E: number): React.CSSProperties =>
  fundo === "placa" ? { background: TINTA, color: OSSO, padding: `${14 * E}px ${30 * E}px ${18 * E}px` }
  : fundo === "papel" ? { background: PAPEL, color: TINTA, padding: `${14 * E}px ${30 * E}px ${18 * E}px`, boxShadow: `0 0 0 ${2 * E}px ${TINTA}, ${10 * E}px ${10 * E}px 0 ${TINTA}` }
  : { color: TINTA };

// grito: letras sobem de dentro da máscara (112 %, 0,026 s entre letras) e a largura abre 62 → alvo
const Grito: React.FC<{ txt: string; px: number; t: number; E: number; wdth?: number; cor?: string }> = ({ txt, px, t, E, wdth = 100, cor }) => (
  <div style={{ font: `900 ${px * E}px Archivo`, lineHeight: 0.86, letterSpacing: "-.045em", whiteSpace: "nowrap", overflow: "hidden", color: cor, paddingBottom: ".04em",
    fontStretch: `${interpolate(t, [0, 0.5], [62, wdth], { ...clamp, easing: expoOut })}%` }}>
    {[...txt].map((c, i) => (
      <span key={i} style={{ display: "inline-block", whiteSpace: "pre",
        transform: `translateY(${112 * (1 - interpolate(t - i * 0.026, [0, 0.32], [0, 1], { ...clamp, easing: expoOut }))}%)` }}>{c}</span>
    ))}
  </div>
);
const Voz: React.FC<{ txt: string; px: number; t: number; E: number; atraso?: number }> = ({ txt, px, t, E, atraso = 0.12 }) => {
  const k = interpolate(t - atraso, [0, 0.5], [0, 1], { ...clamp, easing: quintOut });
  return <div style={{ font: `italic 400 ${px * E}px "Instrument Serif"`, lineHeight: 1, letterSpacing: "-.01em", opacity: k, transform: `translateY(${(1 - k) * 24 * E}px)` }}>{txt}</div>;
};
const Rotulo: React.FC<{ txt: string; E: number; t: number }> = ({ txt, E, t }) => (
  <div style={{ font: `700 ${30 * E}px "JetBrains Mono"`, letterSpacing: ".08em", textTransform: "uppercase", opacity: interpolate(t, [0.15, 0.4], [0, 1], clamp) }}>{txt}</div>
);

export const TextoEnfase: React.FC<TextoProps> = (p) => {
  const { fps } = useVideoConfig(); const t = useCurrentFrame() / fps; const E = p.escala;
  const [x, y] = p.pos ?? [1040, 160];
  const fundo = p.fundo ?? "placa";
  const out = saida(t, p.dur);
  const px = useEncaixe(p.palavra, p.largura ?? 640, p.estilo === "numero" ? 75 : 100);
  const base: React.CSSProperties = { position: "absolute", left: x * E, top: y * E, display: "flex", flexDirection: "column", alignItems: "flex-start", gap: 10 * E };

  // 1) PLACA: palavra-chave; a placa abre como cortina (0,28 s) e fecha para a direita na saída
  if (p.estilo === "placa") {
    const abre = interpolate(t, [0, 0.28], [100, 0], { ...clamp, easing: expoOut });
    const fecha = interpolate(t, [p.dur - 0.22, p.dur], [0, 100], { ...clamp, easing: p3in });
    return (<AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ ...base, ...caixa(fundo, E), clipPath: `inset(0 ${abre}% 0 ${fecha}%)` }}>
        {p.rotulo && <Rotulo txt={p.rotulo} E={E} t={t} />}
        <Grito txt={p.palavra} px={px} t={t - 0.06} E={E} />
      </div></AbsoluteFill>);
  }

  // 2) GRITO + VOZ: a palavrinha serif acima e à esquerda, entra junto/depois (nunca antes)
  if (p.estilo === "grito-voz") {
    const larg = interpolate(t, [p.dur - 0.3, p.dur], [100, 62], { ...clamp, easing: Easing.in(Easing.quad) });
    return (<AbsoluteFill style={{ pointerEvents: "none", opacity: out }}>
      <div style={{ ...base, ...caixa(fundo, E), gap: 4 * E }}>
        {p.voz && <Voz txt={p.voz} px={Math.max(56, px * 0.45)} t={t} E={E} />}
        <Grito txt={p.palavra} px={px} t={t} E={E} wdth={t > p.dur - 0.3 ? larg : 100} />
      </div></AbsoluteFill>);
  }

  // 3) NÚMERO: conta em 0,6 s (expo.out) e para no valor exato; dígitos tabulares; unidade/voz ao lado
  if (p.estilo === "numero") {
    const de = p.de ?? 0, ate = p.ate ?? Number(p.palavra);
    const v = Math.round(interpolate(t, [0, 0.6], [de, ate], { ...clamp, easing: expoOut }));
    const k = interpolate(t, [0, 0.35], [0, 1], { ...clamp, easing: expoOut });
    return (<AbsoluteFill style={{ pointerEvents: "none", opacity: out }}>
      <div style={{ ...base, ...caixa(fundo, E), flexDirection: "row", alignItems: "flex-end", gap: 22 * E }}>
        <div style={{ font: `800 ${200 * E}px Archivo`, fontStretch: "75%", fontVariantNumeric: "tabular-nums", lineHeight: 0.8, letterSpacing: "-.06em",
          clipPath: "inset(-10% -5% 0 -5%)", transform: `translateY(${(1 - k) * 60 * E}px)` }}>{v}</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 * E, paddingBottom: 8 * E }}>
          {p.rotulo && <Rotulo txt={p.rotulo} E={E} t={t} />}
          {p.voz && <Voz txt={p.voz} px={60} t={t} E={E} atraso={0.25} />}
        </div>
      </div></AbsoluteFill>);
  }

  // 4) PERGUNTA: frase serif revelada no tempo de cada palavra dita + "?" gigante em Archivo largo
  if (p.estilo === "pergunta") {
    const ws = p.palavras ?? p.palavra.split(" ").map((w, i) => ({ w, t: i * 0.2 }));
    const ultimo = ws[ws.length - 1].t;
    const q = interpolate(t - ultimo, [0, 0.45], [0, 1], { ...clamp, easing: expoOut });
    return (<AbsoluteFill style={{ pointerEvents: "none", opacity: out }}>
      <div style={{ ...base, ...caixa(fundo, E), flexDirection: "row", alignItems: "flex-end", gap: 18 * E }}>
        <div style={{ font: `italic 400 ${84 * E}px "Instrument Serif"`, lineHeight: 1, maxWidth: 620 * E }}>
          {ws.map((w, i) => { const k = interpolate(t - w.t, [-0.05, 0.3], [0, 1], { ...clamp, easing: quintOut });
            return <span key={i} style={{ display: "inline-block", marginRight: ".22em", opacity: k, transform: `translateY(${(1 - k) * 18 * E}px)` }}>{w.w.replace(/[?]$/, "")}</span>; })}
        </div>
        <div style={{ font: `900 ${170 * E}px Archivo`, fontStretch: "125%", lineHeight: 0.8, color: p.cor,
          transform: `scale(${0.6 + 0.4 * q}) rotate(${-8 * (1 - q)}deg)`, opacity: q, transformOrigin: "30% 90%" }}>?</div>
      </div></AbsoluteFill>);
  }

  // 5) MARCA-UI: traço ácido em multiply sobre a linha da UI, andando com a fala (início da 1ª → fim da última palavra)
  if (p.estilo === "marca-ui" && p.alvo) {
    const [ax, ay, aw, ah] = p.alvo;
    const k = interpolate(t, [0, Math.max(0.4, p.ate_t ?? 0.6)], [0, 1], { ...clamp, easing: Easing.inOut(Easing.quad) });
    const h = ah * 1.3, y0 = ay - (h - ah) / 2, L = aw + 12;
    // borda irregular com semente fixa (nada de tremer por quadro)
    const onda = (i: number) => Math.sin(i * 12.9898) * 2.2;
    const topo = Array.from({ length: 9 }, (_, i) => `${(i / 8) * L},${onda(i)}`).join(" ");
    const base_ = Array.from({ length: 9 }, (_, i) => `${L - (i / 8) * L},${h + onda(i + 20)}`).join(" ");
    return (<AbsoluteFill style={{ pointerEvents: "none", opacity: saida(t, p.dur, 0.3) }}>
      <svg width="100%" height="100%" style={{ position: "absolute", mixBlendMode: "multiply" }}>
        <defs><clipPath id="anda"><rect x={0} y={-10} width={L * k} height={h + 20} /></clipPath></defs>
        <g transform={`translate(${(ax - 6) * E} ${y0 * E}) scale(${E}) rotate(-1.2)`} clipPath="url(#anda)">
          <polygon points={`${topo} ${base_}`} fill={p.cor ?? ACIDO} opacity={0.75} />
        </g>
      </svg></AbsoluteFill>);
  }

  // 6) RISCA: palavra (placa/papel/nua) e o risco andando na palavra da negação; depois a palavra apaga para 55 %
  if (p.estilo === "risca") {
    const rt = p.risca_t ?? 0.6;
    const k = interpolate(t - rt, [0, 0.3], [0, 1], { ...clamp, easing: p4out });
    const apaga = interpolate(t - rt, [0.3, 0.6], [1, 0.55], clamp);
    return (<AbsoluteFill style={{ pointerEvents: "none", opacity: out }}>
      <div style={{ ...base, ...caixa(fundo, E) }}>
        <div style={{ position: "relative" }}>
          <div style={{ opacity: apaga }}><Grito txt={p.palavra} px={px} t={t} E={E} /></div>
          {/* risco a .47 do corpo (lh .86), 4 % além de cada lado, girado −3°; medido na largura do bloco */}
          <div style={{ position: "absolute", left: "-4%", top: `${0.47 * 0.86 * px * E - 0.045 * px * E}px`, height: 0.09 * px * E, width: `${108 * k}%`,
            background: p.cor ?? "#ef4444", transform: "rotate(-3deg)", transformOrigin: "0 50%", borderRadius: 2 * E }} />
        </div>
      </div></AbsoluteFill>);
  }
  return null;
};
```

Observações do esboço:
- **Sublinhado à mão** é o `risca` com `top` = 0,98 do corpo e `height` 0,07 em. Vale fazer um `modo: "sublinha"` em vez de um sétimo estilo.
- O `marca-ui` recebe o `alvo` em px **do quadro da palavra**. Se o zoom anda durante o traço, troque por `useAlvo(alvoBruto, fps, ini)` do `anotacoes.md` 4.5.
- Toda medição (`useEncaixe`) roda depois das fontes (`delayRender`). Medir antes da fonte chegar = palavra errada no vídeo.
- Conferir com `conferir_hierarquia.mjs` não funciona direto no Remotion. Grave 1 quadro por texto (`npx remotion still … --frame=N`) e rode a seção 3.2 nesses quadros. Ou faça uma página HTML com `frame(t)`, como no teste deste estudo.

### 4.4 Frequência e alternância (para o resolvedor e para a revisão)
| Regra | Número |
|---|---|
| Textos por minuto nos trechos de tela | **2–4** **[proposta]** (anúncio e reel: até 1 a cada 3–5 s; tutorial é mais calmo) |
| Distância mínima entre textos | 8 s (par pergunta → resposta conta como 1) |
| Textos ao mesmo tempo | 1 |
| Sinais somados (texto + anotação + selo + capítulo) | ≤ 1 novo a cada 8–10 s; nada novo por 2–4 s depois de um gesto grande (nivel 55) |
| Mesmo estilo seguido | ≤ 2; nenhum estilo > 40 % dos textos do vídeo |
| Trechos sem texto | abertura e fechamento (já são motion), dentro de motion, ±3 s de capítulo no mesmo lado, 1,5 s em volta de corte para motion |
| Carimbo, "!" e texto atrás da pessoa | 1 de cada por vídeo, no máximo |
| Texto que repete o que a UI já mostra grande | não escreva: use marca-texto ou sublinhado na própria UI |

Alternância sugerida num bloco de 1 min de tela: anotação (holofote/passo) → texto (palavra ou número) → zoom → texto (pergunta/frase-tese) → motion. Assim cada recurso tem uma função: **anotação = onde olhar, texto = o que lembrar, motion = a ideia sem tela**.

---

## 5. Oito exemplos na aula SLA (tempo editado da `aula-sla-v2.mp4`)

Tempos das palavras em `fonte/palavras-final.json`. Posições medidas nos quadros reais. Nenhum cai dentro de motion (0–29,0; 30,9–37,4; 117,8–129,0; 172,5–193,3; 258,5–266,6; 300,7–) nem no selo.

| # | Fala (palavra âncora) | Tempo (ini → fim) | Texto na tela | Estilo | Onde (px) e fundo |
|---|---|---|---|---|---|
| 1 | "E quando bater aqui 10 minutos, **quer dizer o quê?**" (quer 67,35 · quê? 67,81) | **67,25 → 69,10** (4 palavras pedem 1,8 s de leitura; a palavra-resposta só vem em 72,29, então a pergunta pode ficar por cima do começo da resposta) | *quer dizer o* **?** | pergunta (palavras no tempo da fala; "?" 170 px) | x 1040, y 400: área de conversa vazia (x 1000–1700, y 380–700); **sem placa** (passa na regra 3.2) |
| 2 | "…já **rompeu** com o **combinado**." (rompeu 72,29 · combinado 73,72) | **72,19 → 74,40** (sai antes do zoom de 74,5) | **COMBINADO.** riscado em vermelho do vencido, o risco anda em 73,72 | risca (par com o #1) | mesmo lugar do #1 (o "?" vira a resposta); papel osso |
| 3 | "Eu, particularmente, **deixo todos** os usuários." (deixo 98,24 · todos 98,42) | **98,32 → 100,0** | *eu deixo* / **TODOS.** | grito-voz | x 1240, y 150 (alto à direita; câmera embaixo à direita); **placa de tinta** (linhas da UI atrás) |
| 4 | "Os que você mais vai usar vão ser **esses dois** aqui." (dois 151,55) | **151,40 → 153,40** | **2** (conta 0 → 2) + *que você vai usar* | numero | x 360, y 280: canvas vazio à esquerda (zoom no painel da direita, cx .655); sem placa |
| 5 | "…eu tenho **uma métrica real** que minha equipe está demorando" (métrica 170,27) | **170,17 → 172,30** (0,2 s antes do motion 03) | **MÉTRICA REAL.** em 2 linhas, wdth 80 | placa (cortina) | x 96, y 200: faixa branca à esquerda do painel Ações; acima da câmera (canto esquerdo) |
| 6 | "…eu vou saber **que atrasou**." (atrasou 214,45) | **214,35 → 215,40** | **ATRASOU.** + sublinhado à mão vermelho, que anda 214,45–214,80 | risca, modo sublinha | x 1150, y 130 (alto à direita); placa. O capítulo 4 entra em 215,1 do outro lado. Se ficar cheio, atrasar o capítulo para 215,6 |
| 7 | "aí você **para de perder** os seus leads…" (para 254,14 · perder 255,28) | **255,18 → 258,25** | *você para de* / **PERDER LEADS.** | grito-voz (frase-tese antes da pegadinha) | x 700, y 330: centro da conversa; papel osso (a bolha "estamos verificando" fica abaixo, y ~790) |
| 8 | "eu mudo para contar **apenas** as mensagens dos trabalhos **selecionados**." (apenas 271,82 → selecionados 273,72 + 0,5) | **271,72 → 274,50** | marca-texto ácido sobre a linha "Contar apenas as mensagens de fluxos de trabalho selecionados…" (x 452–912, y 311–340 no quadro de 272,0 s) | marca-ui (o traço chega ao fim em "selecionados") | sobre a UI, em multiply. Segue a vista quando o zoom de 273,5 começa (`useAlvo`) |

Notas:
- **Ritmo:** 8 textos em 300 s, ou 6 "batidas" (o 1+2 é um par). Nos ~216 s de tela dá ~2,2 por minuto, dentro da faixa. Somados às anotações do `anotacoes.md` (exemplos 1–3), dá ~1 sinal a cada 10 s.
- **Estilos:** pergunta, risca, grito-voz, número, placa, risca (sublinha), grito-voz, marca-ui. Nenhum estilo 3 vezes, nenhum par igual seguido. Grito-voz e risca aparecem 2 vezes cada (25 %).
- **Conflito com `anotacoes.md` exemplo 3:** o #8 **substitui** o holofote de 267,3 s e o passo 1 de 273,5 s (o marca-texto já diz onde olhar e o que é). Os passos 2 e 3 continuam. O exemplo 1 de lá (5 min, 55–61 s) fica como está, pois o #1 daqui começa só em 67,25.
- **O que eu não faria:**
  - texto em 219,5–240,4 s (o selo já narra o teste ao vivo);
  - "20 MIN." em 123–127 s (dentro do motion da régua);
  - carimbo "FUNCIONOU." em 248,7 s. Seria o único carimbo, mas fica a 6 s do #7 e a 10 s do motion pegadinha. Se o dono quiser mais "energia", ele entra no lugar do #7.
- **Texto atrás do apresentador:** na aula SLA só caberia na abertura (câmera grande, 0–29 s), mas ali já é motion. Fica para o próximo talking head ou YouTube sem tela.

---

## Fontes
- Editores de YouTube (descrições de estilo por ferramentas de legenda e templates, não pelos próprios criadores):
  - Ali Abdaal: [Choppity](https://www.choppity.com/tools/recreate-video-editing-style/ali-abdaal/), [SendShort](https://sendshort.ai/guides/ali-abdaal-captions/), [Submagic](https://www.submagic.co/blog/make-captions-like-ali-abdaal)
  - Hormozi: [SendShort](https://sendshort.ai/guides/hormozi-captions/), [Kapwing](https://www.kapwing.com/explore/hormozi-style-captions-template), [Submagic](https://www.submagic.co/pl/blog/how-to-make-alex-hormozi-captions)
  - Iman Gadzhi: [Submagic](https://submagic.co/blog/how-to-make-captions-like-iman-gadzhi), [SendShort](https://sendshort.ai/guides/iman-gadzhi-style/)
  - MrBeast: [SendShort](https://sendshort.ai/guides/mrbeast-style/), [VidPros](https://vidpros.com/mrbeast-thumb-and-video-editing-style/)
- Documentário:
  - Vox / Johnny Harris (descrição de estilo em pedido de editor): [Upwork](https://www.upwork.com/freelance-jobs/apply/Long-Term-Video-Editor-Premium-Documentary-Visual-Journalism-Vox-Johnny-Harris-Aesthetic_~022071695908697374205/)
  - Johnny Harris e objetos físicos: [RNDR](https://rndr.beehiiv.com/p/5-visuals-next-video-ead0)
  - Marca-texto estilo Vox: [AEJuice](https://aejuice.com/blog/how-to-highlight-text-in-after-effects), [Miracamp](https://www.miracamp.com/learn/after-effects/highlight-effects), [Text-Highlighter (GitHub)](https://github.com/pravbk100/Text-Highlighter)
- Anotação à mão: [Rough Notation](https://github.com/rough-stuff/rough-notation) (tipos e padrões)
- Texto atrás da pessoa:
  - Rotoscopia: [Adobe: rotoscopiar o sujeito](https://www.adobe.com/learn/after-effects/web/rotoscope-subject), [Motion Array: rotoscopia no After Effects](https://blog.motionarray.com/learn/after-effects/how-to-rotoscope-in-after-effects-the-basics-after-effects-tutorial/), [Motion Array: DaVinci Resolve](https://motionarray.com/learn/davinci-resolve/davinci-resolve-rotoscoping/)
  - Máscara automática: [Robust Video Matting](https://github.com/PeterL1n/RobustVideoMatting), [MediaPipe Selfie Segmentation](https://cdn.jsdelivr.net/npm/@subhajit-gorai/react-native-mediapipe-llm@1.0.3/mediapipe/docs/solutions/selfie_segmentation.md)
- Aprendizagem e leitura:
  - [Adesope & Nesbit 2012, redundância verbal (meta-análise)](https://rex.libraries.wsu.edu/esploro/outputs/journalArticle/Verbal-Redundancy-in-Multimedia-Learning-Environments/99900601157101842)
  - [Yue, Bjork & Bjork 2013 (PDF)](https://sites.lifesci.ucla.edu/psych-bjorklab/wp-content/uploads/sites/13/2016/07/YueBjorkBjork2013_redundancy.pdf)
  - [Netflix: guia de legenda em português do Brasil](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215600497-Brazilian-Portuguese-Timed-Text-Style-Guide)
  - Mayer, sinalização e contiguidade: ver fontes em `edicao-video/references/anotacoes.md`
- Apple keynote: não achei texto com números sobre a tipografia dos eventos. O que está em 2.2 é observação de estilo e precisa ser conferido assistindo antes de virar regra.
- Teste de contraste deste estudo: `hierarquia-visual/scripts/conferir_hierarquia.mjs` sobre quadros de 56, 76, 100 e 245 s da `aula-sla-v2.mp4` (página de teste e fotos na pasta de rascunho da sessão, fora do repositório).
