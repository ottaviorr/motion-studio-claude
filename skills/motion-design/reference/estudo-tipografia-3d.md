# 04 · Tipografia cinética, hierarquia e 3D em vídeo educativo de alto nível

Pesquisa de 16/10/2026 para o Motion Studio. Régua: os motions Filme C site do portfólio (nível 30–50 do `nivel.md`) e a aula SLA v2 do cliente B (`projetos/<projeto>/v1/fonte/motions2/`).
Motor: cenas HTML com `frame(t)` gravadas pelo HyperFrames em 1080p30 + three.js r186 via `kit/objeto3d.js`.
Legenda de aplicabilidade: **[HTML]** dá para fazer só com CSS/DOM · **[3D]** precisa do three.js · **[ambos]**.

---

## 1. Resumo em 5 linhas

1. A aula SLA v2 acertou o principal: um conceito-objeto (o mostrador é a régua), três fontes com papel fixo, cor plena só no estado e composição assimétrica. Os melhores quadros são `20:00` sobre vermelho e `NO VÁCUO.`.
2. O que ainda denuncia "template/IA": o halo roxo em quase-preto em 5 das 6 cenas, o cartão branco com ícone, os chips em pílula com bolinha, o mono usado como enfeite e o fechamento em lista de slide.
3. Há um bug no kit: a luz-chave do `objeto3d.js` está dentro de um comentário (linha 62). O relógio é iluminado só pelo ambiente, sem luz-chave nem contraluz (rim), e por isso parece adesivo colado no fundo.
4. Para subir de nível sem perder o didático: cada pausa tem que valer como um pôster, o mesmo nível de texto sai sempre no mesmo tamanho, o fundo é plano (luz só de fonte visível), o objeto tem chão e três luzes, e entre os motions de uma aula entra costura (o objeto sai e entra no mesmo lugar).
5. Abaixo estão 24 regras com números e links e 5 receitas `frame(t)` prontas: profundidade de campo falsa com troca de foco, luz de estúdio com rim e sombra de contato, texto que vira sólido 3D, grade de 12 colunas e transição por máscara de tipo. A máscara de tipo foi testada no Chrome e funciona.

---

## 2. Crítica das cenas do último vídeo (aula SLA v2)

Base: código de `motions2/` e quadros tirados dos `.mp4` finais (30 %, 60 % e 90 % de cada cena).

**O que está no nível (não perder):**
- **O mostrador do relógio é a régua** (verde, laranja, vermelho), e o ponteiro para na palavra. É o tipo de ideia que um estúdio vende: o objeto é a explicação, não um enfeite. A cena 02 (`10:00` → `20:00` com o vermelho invadindo a tela) é o melhor quadro do vídeo.
- **`SLA.` encaixado em 1610 px** e **`NO VÁCUO.` em cor plena** passam no teste do pôster: parados, valem como peça impressa.
- Composição **ancorada à esquerda e assimétrica**. Nada flutua no centro sem motivo.
- Entrada em expo.out, saída curta, nenhum quique na palavra gigante.

**O que denuncia template, em ordem de gravidade:**

1. **Bloqueia · fundo "IA" em 5 de 6 cenas.** `fundoSLA()` pinta um radial `#5b3fc4` a 35–42 % + uma mancha `#2a1d5a` sobre `#0c0a14`. É exatamente o sinal nº 1 dos catálogos de "AI slop": halo radial violeta em fundo quase preto ([impeccable.style/slop](https://www.impeccable.style/slop) cita "radial-gradient background halos", "soft spotlights" e "purple gradients"; [pixelslop](https://cdn.jsdelivr.net/npm/pixelslop@0.3.8/dist/skill/resources/ai-slop-patterns.md) classifica "dark mode + glowing accents" como de severidade alta). O portfólio que o dono amou usa **cor plena que troca no corte**, sem halo. Prova dentro do próprio vídeo: os quadros mais fortes são justamente os de vermelho plano. No fechamento, o verde + o roxo no canto deixam a tela lamacenta.
2. **Bloqueia · bug de luz no kit.** Em `kit/objeto3d.js:62` (e na cópia `motions2/objeto3d.js`), `chave.position.set(-3,6,4);cena.add(chave);` ficou **dentro do comentário** `// r155+ mudou...`. A luz-chave nunca entra na cena. O metal vive só do PMREM e da `PointLight` da zona, então falta modelado e contraluz, e o relógio "cola" no fundo plano vermelho sem sombra nenhuma.
3. **Deve · zonas do mostrador sujas.** As zonas apagadas são `MeshBasicMaterial` × 0,42: o laranja vira **mostarda/marrom**, e o vermelho e o verde perdem o croma (dá para ver no recorte do quadro `20:00`). Como o material é Basic (sem luz), o anel parece um vetor colado: não pega o brilho do vidro nem da luz. Apagar uma cor é misturá-la com a cor do mostrador, não escurecê-la (receita 2).
4. **Deve · cena 03 é o "kit de IA" inteiro.** Tem cartão branco arredondado com ícone de traço no canto (`#gat`, sinal "ícone acima do título" / "cards envolvendo tudo"), chips em pílula com `●` ("● em breve · 10 min") e balão de SMS genérico. Os trilhos de 6 px **não chegam nos destinos**: o laranja termina no chip, e o vermelho passa por baixo de `RESPONDE.`. E `AVISA.` a 40 % de opacidade parece desativado ou com bug, não "em segundo plano". É a cena que mais parece um template de Figma.
5. **Deve · mono como "vibe técnica".** O JetBrains Mono +.28em está em **todos** os rótulos ("cliente B PARTNERS · GOHIGHLEVEL", "O QUE É O SLA", "RESUMO DA AULA", "UM GATILHO, DUAS AUTOMAÇÕES"). O pixelslop lista "monospace for tech vibes (uso fora de código)" como sinal. No portfólio, o mono era **máquina**: relógio, código, cota. Aqui ele só se justifica em `10:00`, `20 MIN`, `SLA 14:00` e no gatilho. Rótulo de seção pode sair em Archivo 600 ou simplesmente não existir.
6. **Deve · "hero metric" repetido.** Número gigante com rotulinho mono embaixo (`10:00` / VENCIMENTO EM BREVE, `13:45` / ACIONA AUTOMAÇÕES) é outro padrão catalogado (pixelslop nº 3). Em 02 ele está certo, porque o número é o conceito. Em 00 (`13:45` em 64 px laranja + rótulo) é só decoração e briga com `CONTROLE.`.
7. **Deve · o mesmo gesto em todos os gritos.** As cerca de 12 palavras gigantes entram iguais: letras sobem da máscara e a largura vai de 62 para 112–118. Repetido 12 vezes, o gesto deixa de ser assinatura e vira preset. O repertório que já existe ficou de fora: letras viajando entre palavras (item 34, perfeito em `RESPONDIDO.` → `NO VÁCUO.`, que dividem `O`, `D`/`.`), onda de peso (item 33) e entrada de perto da câmera com desfoque.
8. **Deve · hierarquia quebrada no fechamento [05].** São quatro níveis (rótulo mono, `NO PRAZO.`, lista numerada em Archivo 800 50 px, logo de 70 px com pouco contraste), e a lista em frase ("Fluxo do SLA fora da contagem") é slide de resumo, não motion. O relógio parado em 6 min funciona. O resto pede **um grito + o objeto + a marca**.
9. **Pode · colisões pequenas.** Em 02, o número `20` (HTML preso ao mostrador) fica **debaixo do ponteiro** justamente em 20:00. `VENCIDO · ROMPEU O COMBINADO` e `MÁXIMO.` estão colados: o espaço entre grupos é menor que o de dentro do grupo. Em 00, `CONTROLE.` termina em x ≈ 1830 (margem de ~90 px, abaixo dos 96 da zona segura). Em 01, o quadro do meio tem só a frase serif de 8 palavras solta no vazio: a "voz" carregando frase em vez de palavrinha.
10. **Pode · sem costura entre os motions.** Cada motion começa do fundo vazio. O relógio aparece em 00, 02 e 05, mas nunca **sai de um e entra no outro** no mesmo lugar e tamanho. A costura (item 38) é o que faz uma aula parecer um filme só.

---

## 3. Regras novas ou refinadas [24]

### Tipografia

**1. Cada pausa é um pôster.** Todo quadro de platô tem que funcionar como tipografia estática: alinhado na grade, sem nada pela metade, sem texto a menos de 96 px da borda. Regra de Mat Voyce na releitura cinética do *Think Different*: "every pause point must hold as valid typography"; as transições são só física das letras, sem corte narrativo ([abduzeedo](https://www.abduzeedo.com/mat-voyces-think-different-kinetic-typography-mass)). Teste: folha de fotos no meio de cada platô; se um quadro não serve de capa, refaça. **[ambos]**

**2. Letra com massa, não com easing de UI.** Gritos assentam com inércia: entrada expo.out de 0,35–0,75 s e **overshoot ≤ 2 %** da altura. Quique ou elástico em texto é sinal catalogado ([impeccable](https://www.impeccable.style/slop): "bounce or elastic easing"; [pixelslop](https://cdn.jsdelivr.net/npm/pixelslop@0.3.8/dist/skill/resources/ai-slop-patterns.md) nº 11). Na palavra pesada, atrasar 0,02–0,03 s por letra dá o peso. **[HTML]**

**3. Três gestos de entrada no repertório, nunca o mesmo duas vezes seguidas.** (a) máscara + largura 62 → alvo; (b) letras viajando entre palavras (LCS, item 34); (c) chegada de perto da câmera, escala 6 → 1 com desfoque 26 → 0 px em 0,46 s. Numa aula com 10 gritos: no máximo 50 % do mesmo gesto. **[HTML]**

**4. Mesmo nível = mesmo tamanho.** Lista de gritos do mesmo nível (01/02/03) sai num `font-size` só, o **menor** dos encaixes, alinhada à esquerda. Encaixar cada uma pela largura dá tamanhos diferentes e cria uma hierarquia falsa. **[HTML]**

**5. Voz = 1 a 3 palavras.** A serif itálica é a palavrinha que conversa com o grito (0,2–0,6× o tamanho dele). Frase de 4 ou mais palavras vai para a fala; se tiver que aparecer, entra como apoio em Archivo 500, 40–52 px no 16:9, e nunca fica sozinha na tela por mais de 0,5 s. **[HTML]**

**6. Mono só para máquina.** JetBrains Mono apenas para tempo, contagem, código, gatilho e cota técnica, ou seja, coisa que um sistema escreveria. Rótulo de seção ou marca: Archivo 600, caixa-alta, +.06em, ou nada. O pixelslop lista "monospace for tech vibes" como sinal. **[HTML]**

**7. Tracking cai com o tamanho, entrelinha também.** Medidas da Apple: display de 56 px com peso 600, lh 1,07 e −0,28 px (≈ −.005em); 80 px com tracking negativo; corpo de 17 px com lh 1,47 e −0,374 px ([opendesigner · Apple](https://opendesigner.io/design-systems/apple); [Vercel](https://cdn.jsdelivr.net/npm/gridstamp@1.4.0/DESIGN.md): Geist display com −2,4 a −2,88 px). No vídeo: ≥ 200 px → −.045 a −.06em, lh .80–.86; 56–120 px → −.01 a −.02em, lh 1,0–1,07; rótulo 26–36 px → +.06 a +.10em. O +.28em fica reservado ao estilo cinema e a no máximo uma linha por tela. **[HTML]**

### Hierarquia e composição

**8. Grade de 12 colunas no 16:9.** Margem de 96 px (EBU R95), calha de 24 px, coluna de **122 px** ((1920 − 192 − 11×24) / 12). Toda borda esquerda de texto cai numa linha de coluna; topos em múltiplos de 8 px. A Vercel monta tudo sobre uma grade modular de 360 px em 1080, inspirada no estilo suíço ([rauno.me · Vercel](https://2023.rauno.me/craft/vercel); [Müller-Brockmann](https://en.wikipedia.org/wiki/Josef_M%C3%BCller-Brockmann)). Receita 4. **[HTML]**

**9. O objeto no terço, o texto no outro.** Centro óptico do objeto num ponto dos terços (x 640 ou 1280; y 360 ou 720), texto na coluna oposta e **≥ 40 % do quadro vazio** na frase de impacto. Mais de 70 % dos elementos centralizados é sinal de IA ([pixelslop](https://cdn.jsdelivr.net/npm/pixelslop@0.3.8/dist/skill/resources/ai-slop-patterns.md) nº 17). **[ambos]**

**10. Espaço entre grupos ≥ 2× o espaço de dentro.** Rótulo e grito do mesmo grupo ficam a ≤ 0,15em do grito; o grupo seguinte fica a ≥ 0,5em. Hoje há casos de grupos colados (02: `ROMPEU O COMBINADO` / `MÁXIMO.`). **[HTML]**

**11. Três níveis + o objeto, e o fecho é um grito.** Fechamento não é lista de resumo: um grito (o estado final, ex. `NO PRAZO.`), o objeto no estado final e a marca. A lista vai para a descrição do vídeo ou para a fala. **[ambos]**

**12. O objeto-conceito nunca é coberto pelo próprio texto.** Rótulo preso ao objeto (`O.proj`) se afasta do ponteiro ou da parte móvel quando a distância angular fica < 12°: desliza para fora no raio, sem sumir. **[3D]**

### Cor

**13. Fundo plano. Luz colorida só se vier de uma fonte visível.** Nada de halo radial roxo ou azul em quase-preto, gradiente roxo → azul, glow em `box-shadow` nem texto com gradiente ([impeccable](https://www.impeccable.style/slop); [pixelslop](https://cdn.jsdelivr.net/npm/pixelslop@0.3.8/dist/skill/resources/ai-slop-patterns.md) nº 1, 2, 5, 13, 22). O fundo é tinta ou osso, **plano**, mais grão. Luz de cor só como rebatimento do objeto (raio ≤ 35 % da tela, alfa ≤ 0,25, centrada nele). A cor de estado entra **plena** por um gesto, como já fazemos no vermelho. **[ambos]**

**14. Fundo claro também na aula.** O dono prefere claro (itens 26 e "preferências fixas"). Numa aula com 6 motions, **pelo menos 2 em osso** (`#f2eefa` com tinta `#0c0a14`). O metal no claro pede ambiente claro (`corEstudio` = cor do fundo). A alternância escuro/claro também marca os capítulos. **[ambos]**

**15. Apagar é misturar com o fundo, não multiplicar.** Para recuar um elemento colorido: `cor.lerp(corDoFundo, .6)`, que mantém o matiz e baixa o croma e o contraste. Multiplicar por 0,4 leva o laranja para o marrom e o vermelho para o vinho. Para texto que recua: no máximo 55 % de opacidade **e** sem cor de destaque, nunca 40 % (parece desativado). **[ambos]**

**16. Contraste APCA pelo tamanho real.** Lc 90 para texto corrido, Lc 75 no mínimo para corpo ≥ 18 px/400, Lc 60 para 24 px/400 ou 16 px/700, Lc 45 para 36 px/400 ou 24 px/700 ([tabela APCA](https://www.achecks.org/apca-accessible-colour-contrast-checker/); [WP/APCA](https://steve-frenzel.statichost.eu/posts/learning-about-perceptual-contrast)). Os nossos gritos (≥ 150 px) passam com Lc 45–60; o rótulo de 30 px tem que mirar Lc 75 (o `--suave #9a94ad` em `#0c0a14` fica perto do limite em vídeo comprimido). **[HTML]**

### 3D, materiais e luz

**17. Três luzes + ambiente com faixas, sempre.** Chave a 30–45° acima e de lado, preenchimento a ¼–½ da chave do lado oposto, **recorte (rim) atrás, do lado oposto à chave, a 1,5–3× a intensidade dela**. Por cima, ambiente PMREM com faixas de luz (*lightformers*, intensidade > 1) para desenhar os riscos no metal ([three.js · RoomEnvironment](https://threejs.org/docs/pages/RoomEnvironment.html); [drei Lightformers em three puro](https://discourse.threejs.org/t/r3f-lightformers-in-vanilla-three-js/48495); [setup de três pontos](https://tessl.io/registry/skills/github/CloudAI-X/threejs-skills/threejs-lighting)). O rim pode levar a **cor do estado**: é assim que a cor "invade" o objeto antes do fundo. Primeiro, conserte o bug (receita 2). **[3D]**

**18. Objeto nunca flutua sem chão.** Sombra de contato (elipse escura com desfoque, alfa 0,35–0,55, largura 1,1–1,3× o objeto) ou reflexo no chão. O drei usa `ContactShadows` com `blur`, `opacity` e `far` ([drei staging](https://tessl.io/registry/tessl/npm-react-three--drei/10.7.0/files/docs/staging.md)). Em vídeo, a versão em HTML presa por `O.proj` sai mais barata e igual. **[ambos]**

**19. Material com significado, e as partes gráficas iluminadas.** Metal = precisão e tempo; fosco/argila = didático e amigável; vidro só quando o conceito é transparência. O que é "impresso" no objeto (mostrador, zonas, marcas) usa `MeshStandardMaterial` (rugosidade 0,5–0,7, `emissive` 0,05–0,35), nunca `MeshBasic`: assim pega luz, sombra e o brilho do vidro e para de parecer adesivo. Vidro em tudo (glassmorphism) é sinal de IA. **[3D]**

**20. Profundidade de campo: um plano nítido, troca de foco na palavra.** Um plano em foco; o resto com desfoque proporcional à distância (2–12 px em 1080p) e escala de paralaxe de 0,3–0,6 %. A troca de foco (*rack focus*) dura 0,4–0,6 s e cai na palavra, como no Apple Motion: objetos espalhados em Z e foco animado de um para o outro ([Ripple Training](https://www.rippletraining.com/blog/motion/how-to-create-a-rack-focus-effect/)). O nível 1 nunca fica desfocado no platô. Receita 1. **[ambos]**

### Movimento e câmera

**21. Câmera com velocidade casada no corte.** Na transição por *tracking*, a câmera anda para frente ou para trás com a curva no **pico de velocidade exatamente no corte**, e um desfoque mais curto que o movimento, centrado no corte (técnica Vox, [PremiumBeat](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)). Para nós: 0,5–0,8 s de movimento em eio, desfoque de 0 → 10 → 0 px em 0,3 s centrado no corte. Vale também entre motions da mesma aula (costura, item 38). **[ambos]**

**22. Alternar novidade alta e baixa.** Depois de um gesto grande (cor invadindo, troca de foco, objeto girando), os 2–4 s seguintes só têm micro-movimento (respiro, ponteiro, contagem). A Vercel alterna animações de alta e de baixa novidade "para evitar fadiga" ([rauno.me](https://2023.rauno.me/craft/vercel)). Regra: dois gestos grandes nunca a menos de 1,5 s um do outro. **[ambos]**

**23. Textura em passo de 12 q/s, texto liso a 30.** O "liso de computador" sai com textura (grão, papel, retícula) trocando a 12 q/s (2–3 texturas por segundo, 5–6 no ciclo, como na Vox, [PremiumBeat](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)), enquanto texto e objeto seguem lisos a 30 q/s. É o "imperfeito de propósito" que a Canva aponta como tendência de 2026 contra a estética de IA ([Campaign Brief](https://campaignbrief.com/?p=305692)). Semente do ruído = `floor(t*12)`. **[HTML]**

### O que denuncia IA (lista de verificação com pontuação)

**24. Conte os sinais antes de gravar. 0–1 = limpo, 2–3 = corrigir, 4 ou mais = refazer** (escala do [pixelslop](https://cdn.jsdelivr.net/npm/pixelslop@0.3.8/dist/skill/resources/ai-slop-patterns.md)). Os sinais que mais aparecem em motion:
- halo radial ou gradiente roxo/azul/ciano em quase-preto; glow em volta das coisas;
- texto com gradiente (`background-clip:text`);
- cartão arredondado com sombra genérica e ícone de traço no canto; cartões idênticos em grade de 3;
- chip em pílula com bolinha "●" pulsando;
- número gigante + rotulinho embaixo, sem ser o conceito;
- mono como enfeite;
- glassmorphism (vidro fosco em mais de 1 elemento);
- quique ou elástico;
- tudo centralizado;
- Inter/Roboto/system-ui como voz da peça;
- `#000`/`#fff` puros;
- partículas e glitch "porque dá";
- ícone redondo colorido repetido.

A aula SLA v2 marca **4** (halo, cartão+ícone, pílula+bolinha, mono como enfeite) e por isso parece "quase lá". Zerando esses quatro, ela fica no nível do portfólio.

---

## 4. Cinco receitas prontas (padrão `frame(t)`)

Usam o que já existe em `comum.js` (`p`, `eio`, `eo`, `mix`, `$`) e `aula2.js` (`EXPO`, `lerp`, `encaixa`, `letras`). Tudo função pura de `t`.

### Receita 1 · Profundidade de campo falsa com troca de foco (*rack focus*) [ambos]

```js
// Cada camada tem um z (0 = plano do objeto). O desfoque cresce com a distância ao foco.
// abert ≈ "abertura": 6 px/un = f/1.4 (sonho), 3 = f/2.8, 1.5 = f/5.6. Teto 12 px (custa render no HyperFrames).
const CAM=[{el:$('fundoTxt'),z:-2.5},{el:$('gl'),z:0},{el:$('rotulo'),z:1}];
function foco(zf,abert=4){
  CAM.forEach(c=>{const d=c.z-zf,b=Math.min(12,Math.abs(d)*abert);
    c.el.style.filter=b<.25?'none':`blur(${b.toFixed(2)}px)`;
    c.el.style.transform=`scale(${(1+d*.004).toFixed(4)})`;          // paralaxe de "respiro de lente"
    c.el.style.opacity=(1-Math.min(.35,Math.abs(d)*.08)).toFixed(3);}); // longe = levemente mais apagado
}
// na cena: foco no relógio; em "vencido" o foco pula para o rótulo em 0,5 s; volta em "menos"
cena(dur(11.2),t=>{
  const zf=lerp(0,1,eio(p(t,W('vencido')-.1,W('vencido')+.4)))*(1-eio(p(t,W('menos')-.2,W('menos')+.3)));
  foco(zf,3.5);
});
```
- O canvas WebGL desfoca inteiro: ponha o fundo com texto em outra camada HTML (marca-d'água, `data-hv="ignorar"`) para ter três planos de verdade.
- Para desfoque real no three: `BokehPass` ([exemplo three.js](https://threejs.org/examples/#webgl_postprocessing_dof)). Mas o CSS em camadas é mais barato e já basta para motion didático.

### Receita 2 · Luz de estúdio com rim, sombra de contato e zonas corrigidas [3D]

```js
// 0) CONSERTO DO KIT (kit/objeto3d.js:62): tirar do comentário a linha da luz-chave:
//    const chave=new T.DirectionalLight(...);   // r155+ ...
//    chave.position.set(-3,6,4); cena.add(chave);
// 1) três pontos + rim na cor do estado
function luzEstudio(O,{chave=.9,fill=.3,rim=2.2}={}){
  const T=O.THREE;
  O.luz.intensity=chave;O.luz.position.set(-3,5,4);if(!O.luz.parent)O.cena.add(O.luz);
  const f=new T.DirectionalLight(0xc9ccff,fill);f.position.set(4,-1,3);O.cena.add(f);
  const r=new T.DirectionalLight(0xffffff,rim);r.position.set(3.5,2.5,-4.5);O.cena.add(r);   // atrás e oposto à chave
  return {fill:f,rim:r};
}
const L=luzEstudio(R.O);
// 2) zonas do mostrador que pegam luz, "apagadas" por mistura (não ×0,42)
//    no relogio3d.js: new T.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:.3,roughness:.6,metalness:0})
const FACE=new THREE.Color(0x0e0c16);
function acendeZona(m,ativa,brilho=1){m.color.copy(m.userData.cor).lerp(FACE,ativa?0:.6);m.emissive.copy(m.color);m.emissiveIntensity=ativa?.35*brilho:.04;}
// 3) sombra de contato em HTML, presa à base do objeto pela projeção
//    <div id="sombra" style="position:absolute;border-radius:50%;background:radial-gradient(closest-side,rgba(0,0,0,.55),transparent);filter:blur(8px)"></div>
function sombra(el,O,{raio=1.25,yBase=-1.32,alfa=.5}={}){
  const [x,y]=O.proj([0,yBase,0]),[x2]=O.proj([raio,yBase,0]),w=Math.abs(x2-x)*2.4;
  el.style.left=(x-w/2)+'px';el.style.top=(y-w*.06)+'px';el.style.width=w+'px';el.style.height=(w*.14)+'px';el.style.opacity=alfa;
}
// em frame(t): o rim pega a cor do estado UM pouco antes de o fundo virar (antecipa o gesto)
cena(D,t=>{
  const m=/* minutos */0,cor=corMin(m);
  L.rim.color.set(cor);L.rim.intensity=2.2+1.2*eio(p(t,W('vencido')-.4,W('vencido')));
  R.poe({min:m,cam:{az:-14,el:14,dist:9.6},xc:590,yc:600});
  sombra($('sombra'),R.O);
});
```
- Fundo claro: `corEstudio` igual ao fundo e rim branco a 1,2. No escuro, rim de 2–3, na cor do estado.
- Conferir no recorte: precisa aparecer uma borda clara contínua do lado oposto à chave. Se não aparece, o rim está fraco ou atrás demais.

### Receita 3 · Texto que vira objeto 3D (sólido em fatias, encaixe com o HTML) [3D]

Sem `TextGeometry` (exigiria converter a Archivo para typeface JSON): a palavra é desenhada num canvas com a fonte já carregada e empilhada em N fatias. De frente, ela é idêntica ao grito HTML; girando, tem espessura e lateral de metal. Assim o grito HTML pode **trocar** pelo sólido no quadro em que os dois coincidem (*match cut*).

```js
// precisa: fontesProntas() antes. ctx.fontStretch só aceita palavras: 62%→'extra-condensed', 100%→'normal', 125%→'expanded'.
function textoSolido(O,txt,{px=300,peso=900,largura='expanded',fatias=32,prof=.45,corFace=0xf2eefa,corLado=0x6f6a80,alturaUn=1}={}){
  const T=O.THREE,c=document.createElement('canvas'),g=c.getContext('2d');
  const fonte=`${peso} ${px}px Archivo`;g.font=fonte;g.fontStretch=largura;
  const w=Math.ceil(g.measureText(txt).width+px*.2),h=Math.ceil(px*1.1);
  c.width=w;c.height=h;g.font=fonte;g.fontStretch=largura;g.letterSpacing=(-.045*px)+'px';
  g.fillStyle='#fff';g.textBaseline='middle';g.fillText(txt,px*.1,h*.52);
  const tex=new T.CanvasTexture(c);tex.colorSpace=T.SRGBColorSpace;tex.anisotropy=8;
  const geo=new T.PlaneGeometry(alturaUn*w/h,alturaUn),grupo=new T.Group();
  for(let i=0;i<fatias;i++){const frente=i===0;
    const mat=new T.MeshStandardMaterial({alphaMap:tex,transparent:false,alphaTest:.5,side:T.DoubleSide,
      color:frente?corFace:corLado,metalness:frente?.1:.9,roughness:frente?.55:.3});
    const pl=new T.Mesh(geo,mat);pl.position.z=-i*prof/fatias;grupo.add(pl);}
  grupo.userData.larguraUn=alturaUn*w/h;return grupo;
}
// encaixe: a que distância o sólido fica com a MESMA largura em px que o grito HTML (fov vertical)
function distParaLargura(O,larguraUn,px,H=1080,fov=24){return larguraUn*H/(2*Math.tan(fov*Math.PI/360)*px);}
// uso: o HTML "NO PRAZO." entra; aos 2,0 s ele some e o sólido aparece no mesmo lugar; gira 0 → 35° mostrando a espessura
const S=textoSolido(R.O,'NO PRAZO.');R.O.objeto.add(S);
const larguraHTML=860, d0=distParaLargura(R.O,S.userData.larguraUn,larguraHTML);
cena(8,t=>{
  const k=eio(p(t,2.0,3.2)), troca=t>=2.0;
  $('np').style.visibility=troca?'hidden':'visible'; S.visible=troca;
  S.rotation.y=(-35*k)*Math.PI/180; S.rotation.x=(8*k)*Math.PI/180;
  R.O.poeCamera({az:0,el:0,dist:d0*(1+.12*k)});R.O.render();
});
```
- No quadro da troca, o sólido está de frente e tem o mesmo tamanho: o olho não vê a costura. Confira com duas fotos em `t = 1,99` e `2,0`.
- 32 fatias com prof .45 já parecem maciço até 40° de giro. Acima disso, use 64 fatias ou limite o giro.

### Receita 4 · Grade de composição 16:9 (12 colunas, terços, linha de base) [HTML]

```css
:root{--mg:96px;--gut:24px;--col:122px;--base:8px}       /* (1920-192-11*24)/12 = 122 */
#grade{position:absolute;inset:0;z-index:99;pointer-events:none;display:none;
  background:
   repeating-linear-gradient(90deg,transparent 0 96px,rgba(255,0,80,.10) 96px 218px,transparent 218px 242px) 0 0/146px 100% no-repeat,
   linear-gradient(90deg,transparent 639px,#0ff 639px 641px,transparent 641px 1279px,#0ff 1279px 1281px,transparent 1281px),
   linear-gradient(180deg,transparent 359px,#0ff 359px 361px,transparent 361px 719px,#0ff 719px 721px,transparent 721px)}
body.grade #grade{display:block}
```
```js
// x da borda esquerda da coluna n (0–11) e da direita da coluna n
const col=n=>96+n*(122+24), colFim=n=>col(n)+122;
// encaixa o grito na largura de N colunas, em vez de um número solto
const larguraCols=(a,b)=>colFim(b)-col(a);                    // ex.: colunas 6–11 = 852 px
encaixa($('np'),larguraCols(6,11)); $('np').style.left=col(6)+'px';
// conferência: lista quem não está numa linha de coluna (±2 px) nem num múltiplo de 8 no topo
function conferirGrade(){const linhas=[...Array(0xc)].flatMap((_,n)=>[col(n),colFim(n)]);
  document.querySelectorAll('.G,.V,.M,.N').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width)return;
    const ok=linhas.some(x=>Math.abs(x-r.left)<=2);if(!ok)console.warn('fora da grade:',e.id,Math.round(r.left));});}
// ?grade na URL → mostra a grade (prévia), nunca na gravação
if(location.search.includes('grade'))document.body.classList.add('grade');
```
- O grito encaixa em **colunas**, não em px soltos: 6 colunas = 852 px, 8 = 1144 px, 11 = 1582 px. Isso amarra todos os motions da aula na mesma estrutura sem que fiquem iguais.
- Objeto: centro num ponto dos terços (640/360, 1280/360, 640/720, 1280/720).

### Receita 5 · Transição por máscara de tipo (a cena seguinte nasce de dentro da letra) [HTML]

Testado no Chrome (16/10/2026): `clip-path:url(#id)` com `<text>` dentro de `<clipPath>` funciona em elemento HTML, usa as fontes da página e aceita `transform` no texto, então anima em `frame(t)`.

```html
<svg width="0" height="0" style="position:absolute"><clipPath id="mt" clipPathUnits="userSpaceOnUse">
  <text id="mtx" x="0" y="0" style="font:900 330px Archivo;font-stretch:118%;letter-spacing:-.045em">NO PRAZO.</text>
</clipPath></svg>
<div id="cenaA">…</div>                                   <!-- cena atual (ex.: vermelho, NO VÁCUO.) -->
<div id="cenaB" style="position:absolute;inset:0;clip-path:url(#mt)">…</div>   <!-- próxima (verde, relógio) -->
```
```js
// 1) a palavra aparece como "janela" para B, no mesmo lugar do grito; 2) dá zoom para dentro do miolo do "O" até B cobrir a tela
const X0=620,Y0=900;                                            // linha de base do texto (na grade)
$('mtx').setAttribute('x',X0);$('mtx').setAttribute('y',Y0);
let CX=0,CY=0;                                                  // centro do miolo do "O" (medido uma vez, com a fonte carregada)
function mede(){const b=$('mtx').getExtentOfChar(1);CX=b.x+b.width/2;CY=b.y+b.height*.52;}
cena(D,t=>{ if(!CX)mede();
  const a=W('prazo')-.2, ent=EXPO(p(t,a,a+.45)), zoom=Math.pow(p(t,a+.9,a+1.6),3);   // ease-in: velocidade máxima no fim (corte)
  const s=lerp(.92,1,ent)*Math.pow(60,zoom);                    // ×60 = o miolo do O passa a cobrir 1920×1080
  $('mtx').setAttribute('transform',`translate(${CX} ${CY}) scale(${s.toFixed(4)}) translate(${-CX} ${-CY})`);
  $('cenaB').style.visibility=ent>0?'visible':'hidden';
  if(zoom>=1)$('cenaB').style.clipPath='none';                  // terminou: B é a cena inteira
  $('cenaA').style.filter=`blur(${(8*zoom).toFixed(1)}px)`;     // A desfoca enquanto a câmera "atravessa" a letra
});
```
- Escolha a letra com miolo grande (O, D, Q, 0): o zoom passa **pelo buraco**, então B surge sem nenhuma borda de letra cortando a tela.
- O pico de velocidade fica no fim do zoom (ease-in): o corte para a próxima cena cai em movimento, como pede o item 37.
- Variante didática: em vez do miolo da letra, a palavra gigante vira a janela para a **tela real** do produto (B = print da plataforma). "SLA." mostrando por dentro o painel de configuração do SLA.

---

## Fontes consultadas

- Sinais de IA: [impeccable.style/slop](https://www.impeccable.style/slop) · [pixelslop, catálogo de padrões](https://cdn.jsdelivr.net/npm/pixelslop@0.3.8/dist/skill/resources/ai-slop-patterns.md) · [Canva 2026 "Imperfect by Design"](https://campaignbrief.com/?p=305692)
- Tipografia cinética: [Mat Voyce, *Think Different* (abduzeedo)](https://www.abduzeedo.com/mat-voyces-think-different-kinetic-typography-mass) · [Kyle Cooper, *Se7en* (The Fincher Analyst)](https://thefincheranalyst.com/2025/09/26/30-years-of-kyle-coopers-classic-title-sequence-for-se7en/): tipo feito à mão e passado pela câmera, a textura analógica como argumento
- Sistemas: [Apple (opendesigner)](https://opendesigner.io/design-systems/apple) · [Vercel DESIGN.md](https://cdn.jsdelivr.net/npm/gridstamp@1.4.0/DESIGN.md) · [Vercel Ship (crafter)](https://visual-reference.crafter.run/references/hunt-vercel-ship) · [Rauno, homepage da Vercel](https://2023.rauno.me/craft/vercel)
- Explicadores: [Vox, técnicas (PremiumBeat)](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/) · [Kurzgesagt (U. Michigan)](https://artsatmichigan.umich.edu/ink/?p=11220): forma simplificada e cor saturada a serviço do mecanismo explicado
- Estúdios: [ManvsMachine (Motion Array)](https://motionarray.com/learn/motion-design/studio-spotlight-manvsmachine/) · [Buck (Motion Array)](https://motionarray.com/learn/motion-design/industry-spotlight-buck/) · [Tendril (LBB)](https://lbbonline.com/companies/tendril/about): quadros de estilo iluminados antes de animar · [Gunner, *Mesh* (Motionographer)](https://motionographer.com/2016/12/12/gunner-their-new-film-mesh-and-the-importance-of-changing-things-up/) · [Igloo Inc, Site of the Year Awwwards 2024 (abeto)](https://awwwards.com/igloo-inc-case-study.html)
- 3D: [three.js RoomEnvironment](https://threejs.org/docs/pages/RoomEnvironment.html) · [Lightformers em three puro](https://discourse.threejs.org/t/r3f-lightformers-in-vanilla-three-js/48495) · [drei staging / ContactShadows](https://tessl.io/registry/tessl/npm-react-three--drei/10.7.0/files/docs/staging.md) · [luz de três pontos em three](https://tessl.io/registry/skills/github/CloudAI-X/threejs-skills/threejs-lighting) · [*rack focus* (Ripple Training)](https://www.rippletraining.com/blog/motion/how-to-create-a-rack-focus-effect/)
- Contraste: [APCA (achecks)](https://www.achecks.org/apca-accessible-colour-contrast-checker/) · [Washington Post e APCA](https://steve-frenzel.statichost.eu/posts/learning-about-perceptual-contrast)
- Composição: [Josef Müller-Brockmann](https://en.wikipedia.org/wiki/Josef_M%C3%BCller-Brockmann) · *match cut* ([morphic](https://morphic.com/ai-glossary/match-cut))

Observação: as páginas da Motion Array sobre ManvsMachine e Buck devolveram 403. Delas ficou só o que aparece na busca (ManvsMachine: Cinema 4D + Arnold/V-Ray, Houdini, composição em Nuke, "high-end 3D"; Tendril: quadros de estilo com luz e textura no Redshift antes de animar). Nenhum número desta pesquisa saiu dessas duas páginas.
