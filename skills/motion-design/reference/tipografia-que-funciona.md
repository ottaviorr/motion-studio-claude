# Tipografia que funciona (Archivo + Instrument Serif + JetBrains Mono)

Tirado dos fontes dos trabalhos que o dono mais elogiou: os 3 motions do portfólio ("foda pra crlh") e o site do portfólio. Os números abaixo estão no código, não são chute. Use como ponto de partida e ajuste pela peça.

`$PORTF` = `~/motion-studio/projetos/<projeto>` · `$SITE` = `<site-do-portfólio>/app/src/secoes` (só leitura)

## 1. As 3 fontes (e só elas)

| Papel | Fonte | Eixo/peso usado | Nunca |
|---|---|---|---|
| **Grito** (nível 1) | Archivo variável | wght 800–900; **wdth 62–125** (`font-stretch`) | parágrafo, frase longa |
| **Voz** (nível 2, a palavrinha) | Instrument Serif itálica | 400 só | animar `font-stretch` (não tem eixo de largura: não muda nada e custa layout, `$SITE/01-marca.js:258`) |
| **Máquina** (nível 3, rótulo/número técnico) | JetBrains Mono | 500–700, CAIXA-ALTA | menos de 30 px no reel |

Arquivos `.woff2` locais (gravar sem internet, `font-display:block`):
- Jogo completo + `@font-face` pronto: `$PORTF/02-filme-c/fonte/fontes.css` + `fontes/` (Archivo latin/latin-ext, Instrument Serif normal/itálica, JetBrains Mono). Copie os dois para o `fonte/` da cena.
- Também em `$PORTF/base/fontes/` (Archivo + Space Mono) e `$PORTF/03-filme-b/fonte/fontes/` (os 3, um arquivo cada).
- O JetBrains Mono é um arquivo variável só (os "400/500/700" de `02-filme-c` têm o mesmo tamanho): declare uma vez com faixa de peso.

```css
@font-face{font-family:'Archivo';font-weight:100 900;font-stretch:62% 125%;font-display:block;
  src:url(fontes/Archivo-100-900-latin.woff2) format('woff2')}          /* + o latin-ext com unicode-range */
@font-face{font-family:'Instrument Serif';font-style:italic;font-weight:400;font-display:block;
  src:url(fontes/InstrumentSerif-italic-400-latin.woff2) format('woff2')}
@font-face{font-family:'JetBrains Mono';font-weight:100 800;font-display:block;
  src:url(fontes/JetBrainsMono-normal-400-latin.woff2) format('woff2')}
```
- Use `font-stretch:62%…125%` (CSS) em vez de `font-variation-settings:'wdth'`: anima com GSAP/estilo e não apaga o `font-weight`. Se precisar de `font-variation-settings`, ponha os dois eixos juntos (`'wdth' 125,'wght' 900`).
- Antes do quadro 0, carregue todos os pesos/larguras usados (`document.fonts.load('900 100px Archivo')`… e um `#pre` escondido com cada combinação, `$PORTF/01-filme-a/fonte/filme-a.html:126`). Medida de largura feita antes da fonte chegar = palavra errada no vídeo.
- Proporção medida (Chrome): a mesma palavra em wdth 125 fica **1,8–1,9× mais larga** que em 62. É a "sanfona" que dá para animar.

## 2. Escala de hierarquia em números

**9:16 (1080×1920)** — Filme A e Filme B:

| Nível | Fonte | Tamanho | % da altura | Ajuste |
|---|---|---|---|---|
| 1 palavra | Archivo 900, wdth 100 | **encaixada em 940 px de largura (87 %)**: 148 px (FRONTEIRA.) a 278 px (VIAJE.) | 7,7–14,5 % | lh .86, ls −.045em, `nowrap` |
| 1 número | Archivo 800, `tabular-nums` | 396 px (4,2), 520 px (1) · unidade 116 px | 20,6–27 % | lh .8, ls −.06em (unidade −.03em) |
| 2 voz | Instrument Serif itálica | 80–104 px (fecho: 150–170 px) | 4,2–5,4 % | lh 1, ls −.01em |
| 3 rótulo | JetBrains Mono 500/700 | 30 px | 1,6 % | ls +.08em, CAIXA-ALTA |
| Número de interface | JetBrains Mono 700 | 100 px (saldo), 52 px (chip) | 5,2 % | ls −.04em |

Margem lateral 72–80 px; cabeçalho mono em y = 236 (zona segura); fecho centrado em y ≈ 1066–1335.

**16:9 (1920×1080)** — MEIA-NOITE e site:

| Nível | Fonte | Tamanho | % da altura | Ajuste |
|---|---|---|---|---|
| 1 título | Archivo 900, **wdth 62** | encaixado em 1610 px (84 %) → ~356 px | 33 % | lh .82, ls +.005em |
| 1 palavra do site | Archivo 900, wdth 125→108 | `min(90 % da largura, 44 % da altura)` | até 44 % | lh .9, ls −.04em |
| 1 relógio/timecode | JetBrains Mono 700 | 250 px (150 px no recorte) | 23 % | ls +.01em |
| 2 crédito | Instrument Serif | nome 112 px / linha de cima itálica 58 px; assinatura 84 px | 10 % / 5,4 % | ls −.01em |
| 3 rótulo de cinema | JetBrains Mono 500 | 36–50 px | 3,3–4,6 % | ls **+.28em**, CAIXA-ALTA |

Cantos a 96 px da borda, 56–64 px de cima/baixo.

Razões entre níveis que funcionaram: voz = **0,2× a 0,6×** o grito (site `.mc-k` = .2em; Filme A 104/173 px); rótulo ≈ 0,3× a voz. Três níveis na tela, nunca quatro (ver skill hierarquia-visual).

## 3. Palavra gigante + palavrinha itálica

O padrão Nomad: a palavra em caixa-alta enche a largura e uma palavrinha minúscula em serif itálica "fala" com ela ("seu / DINHEIRO.", "e o que sobra, / INVISTA.", "sem / FRONTEIRA.", "uma / IDEIA.", "vira / CÓDIGO.").

```css
.grito{position:absolute;left:0;width:1080px;text-align:center;font-family:Archivo;font-weight:900;
  font-stretch:100%;line-height:.86;letter-spacing:-.045em;white-space:nowrap}
.grito span{display:inline-block}                     /* uma letra por span: anima e deixa o objeto passar entre elas */
.voz{position:absolute;left:72px;font-family:'Instrument Serif';font-style:italic;font-size:104px;line-height:1;letter-spacing:-.01em}
/* site (palavrinha presa na palavra): */
.k{position:absolute;left:.05em;top:-.4em;font-size:.2em;font-family:'Instrument Serif';font-style:italic;letter-spacing:0}
```
```js
// encaixa a palavra na largura (medir com Range, não com offsetWidth; refazer quando a fonte chegar)
function encaixa(el, alvo){ el.style.fontSize='200px'; const r=document.createRange(); r.selectNodeContents(el);
  el.style.fontSize=(200*alvo/r.getBoundingClientRect().width).toFixed(2)+'px'; }
encaixa(grito, 940);                                   // 9:16 → 940 px · 16:9 → 1610 px · site → min(.9·W, .44·H)
```
- A palavrinha fica **em cima e à esquerda** da palavra (Filme A: voz em y 540 com grito em y 700; site: −.4em, a .05em da borda) ou **dentro da frase, no lugar da palavra-chave** (`em` com 1,12–1,16em, `$SITE/01-marca.css`, `02-filme.css`).
- Uma palavrinha por tela. Ela entra **depois** do grito ou junto (site: +0,1 do ato; Filme B: 2–3,5 tempos depois do número).
- **Objeto entre as letras** (Filme A, `filme-a.html:87–91, 436–457`; site `.mc-tras`/`.mc-frente`): três cópias da palavra — atrás (inteira), canvas do objeto, frente (com as letras de `tras:[i]` escondidas) e uma cópia de cor invertida recortada pelo contorno do objeto (`clip-path: polygon(...)` do fecho convexo projetado). A letra que o objeto atravessa fica atrás; as outras, na frente.
- As letras perto do objeto "se refazem": `dy = −46·e^(−d²)·e^(−3,2l)·cos(15l)` px, com `d = (x_letra − x_objeto)/230` e `l` em batidas.

## 4. Largura e peso como função do tempo

| Gesto | Números | Fonte |
|---|---|---|
| Palavra "respira" o ato todo | wdth 125 → 108 % + escala 1 → 1,06, linear do começo ao fim do ato | `$SITE/01-marca.js:235–237` |
| Entrada esticando | wdth 62 → 100 % em 0,5 do ato, expo.out (junto com as letras subindo) | `01-marca.js:230` |
| Assinatura abrindo | wdth 62 → 125 % em 0,8, expo.out | `01-marca.js:267` |
| Saída "estica" | wdth → 62 %, letter-spacing → +.3em, opacidade → 0, power2.in | `01-marca.js:244` |
| Título nascendo | por letra: wdth 62 → 125 e wght 260 → 800 juntos, power3.out | `$SITE/02-filme.js:312` |
| Onda letra a letra (ANIMA.) | `w = ½+½·sin(fase − 0,95·i)`; wdth = 62→125 por `w`, wght = 900→320 ao contrário; no fim todas espremem para 62/300 | `$SITE/05-corte.js:199–203` |
| Título condensado no escuro | wdth 62 fixo, letras chegando de escala 6 → 1 | `$PORTF/02-filme-c/fonte/meia-noite.html:398–413` |

```js
// em frame(t): largura e peso por letra (uma onda que atravessa a palavra)
letras.forEach((l,i)=>{ const w=.5+.5*Math.sin(t*6 - i*.95);
  l.style.fontStretch=(62+63*w).toFixed(1)+'%'; l.style.fontWeight=Math.round(900-580*w*.85); });
```
- Na gravação (frame(t)) pode animar `font-stretch` à vontade. No site/celular custa layout por quadro: lá o site troca por `scaleX` (`01-marca.js:233`).
- Largura é contraste: **condensado [62] para cinema, tensão e números; expandido (125) para marca e grito**. Um mesmo vídeo pode passar de um para o outro como gesto, não como mistura aleatória.

## 5. Letras em comum viajando entre palavras

`$SITE/01-marca.js:298–347`. Quando a palavra A sai e B entra (com menos de 0,5 de intervalo), as letras em comum voam de uma para a outra; as outras saem/entram normalmente.

1. **Pares** = maior subsequência comum (LCS) das letras de A e B (CÓDIGO. → PORTFÓLIO.: `Ó I O .`; MOVIMENTO. → NÚMERO.: `M E O .`; NÚMERO. → PRODUÇÃO.: `R O .`). Só viaja quando B entra até 0,5 depois de A começar a sair.
2. **Medir** a posição/altura de cada letra no quadro final de A (`t0` = início da saída de A) e no quadro montado de B (`t1` = entrada de B + 0,5), com a linha do tempo posta nesses tempos (`tl.time(...)` e `getBoundingClientRect`). Guardar também o wdth de A e de B.
3. **Viajar** com cópias soltas (`.mc-v`, mesma fonte, `transform-origin:0 0`); esconder a letra original de A ao sair e a de B até chegar:
```js
const k=EIO(prog(t,t0,t1)), arco=Math.sin(Math.PI*k)*H*.05;           // arco para cima de 5 % da altura
pares.forEach(({a,b},n)=>{ const kk=EIO2(clamp(k*1.15 - n*.04));          // 0,04 de atraso por letra
  el[n].style.transform=`translate(${lerp(a.x,b.x,kk)}px,${lerp(a.y,b.y,kk)-arco}px) scale(${lerp(a.h,b.h,kk)/90})`;
  el[n].style.fontStretch=lerp(sA,sB,kk)+'%'; el[n].style.color=mistura(corA,corB,kk); });
```
- Curva geral power3.inOut; por letra power2.inOut. Interpolar **posição, altura, largura (wdth) e cor**.
- Em vídeo (frame(t)): o mesmo, com `t0` = início da saída e `t1` = entrada + ~0,4 s.

## 6. O destaque de cor

Um destaque só, e só no que conta:
- Filme A: amarelo-limão `#E6FF00` só no saldo que conta e no último quadro; fundos em cor plena que trocam no corte (cobalto/laranja/creme/tinta).
- MEIA-NOITE: vermelho `#E50914` no hífen-brasa do título, no "+", nos dois-pontos do relógio e no halo.
- Filme B: laranja `#FF5A1F` só no LED, nas marcas de cota e no ponto do "Filme B." do fecho.
- Site: ácido `#c8ff2e` é o único destaque; verde só para estado.
Tinta e fundo fazem o resto (creme `#FFF4E0`/tinta `#0D0D0D`, osso `#E8E2D0`/preto `#050505`, gelo `#F4F5F7`/grafite `#16181D`).

## 7. Entrada, platô e saída (tempos medidos)

| Peça | Entrada | Platô legível | Saída |
|---|---|---|---|
| Filme A (121 BPM, 1 tempo = 0,496 s) | grito com soco de escala 1,06 → 1 em 0,32 tempo (no drop 1,14 → 1 em 0,5); voz 0,5 tempo, 24 px | plano de 2 tempos = 0,99 s; fecho 10 tempos (~5 s) | corte no meio do giro do cartão |
| MEIA-NOITE (85 BPM, semicolcheia 0,176 s) | letras de escala 6 → 1 em 0,46 s (expo.out), desfoque 26 → 0 px, uma por semicolcheia (9 letras = 1,6 s); créditos piscando em 4 quadros de película (0,17 s) | título montado ~4,8 s | recortes empurrados para a câmera: escala 1 → 4,2 e desfoque 14 px em 0,6 s |
| Filme B (105 BPM, meio compasso = 1,143 s) | número sai de dentro da linha (máscara) descendo 420 px em 0,75 s expo.out; serif 0,6 s quint.out, 26 px | cada especificação = 3 meios compassos = 3,43 s; número parado ~2 s, tela completa ~1,35 s | ease-in cúbico 0,28 s, 60 px, termina 0,2 s antes do corte |
| Site (1 T = 40vh) | letras sobem 112 % em 0,32 T, expo.out, 0,026 por letra | ato ≥ 45vh, platô ~20vh | 0,4 T power3.in, 0,03 por letra; a próxima entra durante a saída |

Regra que sai disso: **entrada com desaceleração forte (expo/quint), saída mais curta com aceleração (cúbica)**, e nada de quique nas palavras grandes (o overshoot `BACKE 1,6–1,8` só nos selos e chips pequenos do Filme A).

## 8. O que NÃO fazer
- Quarta fonte, ou segunda palavra em itálico na mesma tela.
- Grito em frase: 1 palavra (no máximo 2) + ponto final.
- `font-stretch` na Instrument Serif (não tem o eixo) ou wdth fora de 62–125 (trava no limite).
- Medir a palavra antes de a fonte carregar.
- Texto abaixo de 30 px (rótulo) ou serif abaixo de 56 px.
- Entrar a palavra seguinte com tela vazia entre as duas: sobreponha a saída de A com a entrada de B (ou faça as letras viajarem).
- Quique/elástico na palavra gigante; partícula/glitch no texto.
- Destaque de cor em mais de um elemento por tela.
- `mix-blend-mode` em texto por cima de WebGL (no site custava 30–45 ms por quadro).
