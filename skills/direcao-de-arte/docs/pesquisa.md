# Relatório · pesquisa do papel DIRETOR DE ARTE (08/10/2026)

## O que entreguei

```
direcao-de-arte/
  SKILL.md                         processo: briefing → conceito → cartão → quadros-chave; série; crítica; ajustar × refazer
  references/conceito.md           briefing visual, 5 geradores de conceito, teste do conceito, moodboard em texto, style frames
  references/repertorio-estilos.md 27 direções de arte prontas (paleta hex, fontes Google conferidas, textura, movimento, quando usar/não usar)
  references/serie.md              unidade × variedade, eixos de variação, regras de vizinhança, matriz da série de exemplo com leitura crítica
  references/critica.md            método (Connor & Irizarry), checklist de 26 itens com números, formato de ordem de ajuste, exemplos reais
  references/anti-ia.md            sinais de "feito por IA" por categoria (cor, tipo, layout, movimento, texto) e o antídoto de cada um
  assets/cartao-direcao.md         modelo do cartão de direção (com bloco ```cartao``` que o script lê)
  assets/estilos-serie-modelo.md   modelo da bíblia de uma série (núcleo fixo + tabela + seção por peça)
  scripts/conferir-serie.py        confere a série: % claros, escuros seguidos, vizinhos repetidos, fontes-padrão de IA, contraste
  scripts/apertar-olho.sh          folha em miniatura + borrada + cinza (teste do olho apertado), só ffmpeg
```

Testes feitos: `conferir-serie.py` rodou na série aprovada de exemplo (lê a tabela-resumo mesmo sem blocos `cartao`): 7/14 claros (50 %, abaixo da meta de 60 % que o dono pediu depois), nenhum vizinho repetido, avisa Syne/Inter/Outfit nos apoios e destaques de baixo contraste usados como superfície. Num arquivo de teste com erros de propósito, pegou escuros seguidos, mesma fonte de título, mesmo estilo e contraste ilegível (sai com código 1). `apertar-olho.sh` gerou a folha tripla (2880×540). Todas as 60 fontes citadas responderam 200 no Google Fonts.

Não editei nada fora desta pasta e não fiz commit.

## O que pesquisei

1. **O que o estúdio já sabe** (para não repetir): SKILL.md, `nivel.md`, `inspiracao.md`, `armadilhas.md` da motion-design; `ESTILOS.md` e `LEIA-ME.md` da série de exemplo; histórico e `evolucao.md` das marcas; memória do dono (variar, mais claro, sem ícone redondinho, legenda só se pedir, assiste sem som).
2. **Doutrina do HyperFrames 0.8.140:** `motion-doctrine` (lei do vetor, corrente, carregadores, nada de balançar parado, pausa antes do clímax), `hyperframes-creative` (house-style e "lazy defaults", video-composition, visual-styles com 8 estilos de escola, typography com fontes banidas, design-adherence) e `product-launch-video` (visual-design: plano de tomadas no tempo da voz, nunca adiantar tudo, "Video direction" escrito uma vez com lista negativa).
3. **Os 513 prompts do skillry** (`data/videos.json`): li os mais longos de motion/explainer e os trechos de "art direction", "palette", "banned". Padrões: paleta estrita com "nenhuma outra cor", sistema de 3 fontes com papéis, regra formal única ("uma forma que nunca corta", "palavras têm papéis de arquitetura"), lista de banidos, material/meio explícito (xerox, papel, pixel), "escreva primeiro uma bíblia de estilo e um kit de componentes" para séries, "a confiança visual vem da contenção".
4. **Como diretores de arte trabalham:** fluxo brief → moodboard → style frame → storyboard → animatic (Buck, Boords, Milanote); Figma Config (conceito antes do moodboard; 15 fps para parecer feito à mão; paleta grande gerida por variáveis); Pentagram/Channel 5 (sistema modular consistente com conteúdo variado); basement.studio/Vercel (tipografia como ativo central, precisão).
5. **Crítica:** *Discussing Design* (reação × ordem × crítica; as 4 perguntas), "escada de feedback" (entender, valorizar, apontar, sugerir), teste do olho apertado (squint) e de miniatura.
6. **Escolas e repertório:** Müller-Brockmann/suíço, Bauhaus, Memphis, Y2K, risografia (tabela de tintas com hex), Vignelli, editorial, pop art.
7. **Vídeo vertical:** zona segura do Reels, gancho em 1–2 s, quadro de capa legível parado.
8. **Sinais de IA:** Impeccable (anti-padrões), artigos sobre "AI slop", lista do HyperFrames.

Limites: os sites de Linear, Apple e Stripe não têm bastidores públicos de direção de arte (a busca da Stripe só trouxe vagas); usei o que aparece nos próprios filmes e nos prompts que os imitam (Taxtello, keynote). O README do `hyperframes-launches` não traz paletas/fontes (só STORYBOARD.md por projeto). A página do skillry é uma galeria; o conteúdo útil está no JSON.

## Fontes

- Galeria: https://skillry.dev/ai-videos/opus-5-5 · prompts: https://github.com/yihui-dev/awesome-opus5-5-videos (`data/videos.json`) — slugs citados: daniel-haida-636937, twoclipping-402193, twoclipping-496100, annacher-433425, gdgtify-929495, koldo2k-778767, leowenai-125931, techhalla-498547, stokebuilder-356793, jake11moran-414633, astrothewizard-618782, majidmanzarpour-927543
- Lançamentos HeyGen/HyperFrames: https://github.com/heygen-com/hyperframes-launches
- Skills locais HyperFrames 0.8.140: `~/.claude/plugins/cache/hyperframes/hyperframes/0.8.140/.claude/skills/motion-doctrine/`, `skills/hyperframes-creative/`, `skills/product-launch-video/`
- Figma, identidade da Config 2025: https://www.figma.com/blog/how-we-shaped-the-visual-identity-for-config-2025/
- It's Nice That, Config 2024: https://itsnicethat.com/features/figma-config-2024-identity-graphic-design-spotlight-090724
- Pentagram, Channel 5: https://www.pentagram.com/work/channel-5/story
- basement.studio, Vercel: https://basement.studio/post/scaling-vercel-years-of-building-refining-and-elevating
- Buck, Apple "Power to the Pro": https://buck.co/work/apple-power-to-the-pro
- Style frames: https://boords.com/blog/what-are-style-frames-definition-and-examples · https://www.milanote.com/guide/motion-design-style-frames
- Lançamento estilo Apple: https://motion.so/learn/apple-style-product-launch-video
- Crítica: https://andrewclark.super.site/all-media/discussing-design · https://blog.pageproof.com/giving-feedback-design/ · https://uxplanet.org/design-critique-framework-bab9692ac996
- Teste do olho apertado: https://polypane.app/blog/debug-your-visual-hierarchy-with-the-squint-test/
- Anti-padrões de IA: https://mintlify.wiki/pbakaus/impeccable/concepts/anti-patterns · https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website
- Müller-Brockmann: https://www.blinkist.com/en/books/grid-systems-in-graphic-design-en
- Memphis: https://www.masterclass.com/articles/memphis-design-guide · Y2K: https://webflow.com/blog/y2k-aesthetic
- Tintas Riso: https://sites.saic.edu/servicebureau/wp-content/uploads/sites/20/2025/03/EverythingRiso_2024.pdf · https://www.npmjs.org/package/riso-colors
- Zona segura do Reels: https://influencermarketinghub.com/resources/instagram-video-sizes-safe-zones-and-crop-guide-for-2026/

## As 10 lições mais valiosas

1. **Conceito antes de estética.** "Restringir o conceito, não a execução" (Figma). Um conceito numa frase explica todas as escolhas; moodboard sem conceito é catálogo.
2. **Uma regra visual central por peça.** Os melhores prompts têm uma lei que vale para o vídeo inteiro ("uma forma que nunca corta", "as palavras são a arquitetura"). É isso que os torna inconfundíveis, não os efeitos.
3. **Três rotas, depois escolher.** A primeira ideia de uma IA é a média do que ela já viu. Escrever três rotas bem diferentes e escolher pelo briefing tira o vídeo do lugar comum.
4. **Quadro parado antes de animar.** Style frames são o contrato visual dos estúdios (Buck): se o quadro parado é feio, a animação não salva. No nosso fluxo, `fotos.sh` nas 3 cenas-chave antes de escrever as animações.
5. **Paleta estrita com um destaque e regra de uso.** "Nenhuma outra cor"; o destaque só onde a regra manda; neutros puxados para a matiz do conceito; cor da marca como um momento, não como fundo de tudo.
6. **Tipografia em 3 papéis com contraste real** (grito / apoio / número) e fuga das fontes-padrão de IA (Inter, Poppins, Syne, Playfair…) a não ser com motivo.
7. **A lista do que NÃO fazer é metade da direção.** Todo bom prompt tem "Banned:". Ela deve ser específica da peça, não genérica.
8. **Série = núcleo fixo pequeno + bíblia de estilos.** Logo, fecho, regras, voz e técnica fixos; paleta, tipo, material, produto e movimento variam com regra de vizinhança (nunca repetir família, ≥ 60 % claros). Kit de telas re-tematizável por CSS faz a variedade sair barata.
9. **Crítica objetiva liga elemento a objetivo e diz como conferir.** As 4 perguntas de Connor & Irizarry + ordem no formato onde · o que · por que · o que fazer · como conferir. O teste do olho apertado mostra a hierarquia real em segundos.
10. **A confiança visual vem da contenção, e o antídoto da "cara de IA" é decisão com motivo:** material de verdade, imperfeição intencional (15 fps, desalinhamento de riso só no impacto), escala de vídeo, nada de gradiente roxo, brilho, cards iguais, ícone redondinho ou balançar parado.

## Como a skill se conecta com as outras

- **motion-design** (executa): a direção de arte roda ANTES, entrega `fonte/DIRECAO.md` (peça) ou `ESTILOS.md` (série) e os 3 quadros-chave aprovados; a motion-design cita o cartão no topo de cada cena e segue a folha de fotos dela (passo 5) — que volta para a crítica desta skill antes de gravar. Sugestão para a motion-design: no "Antes de começar", acrescentar "rode a direcao-de-arte e tenha o cartão de direção"; no `nivel.md` item 26, apontar para `serie.md` e `conferir-serie.py`.
- **edicao-video** (edita gravação): aqui a direção de arte é leve — um cartão para o pacote de motions da aula (capítulos, fecho, zoom), em geral sem marca, que respeita a câmera e a tela do apresentador. A pergunta principal é "como os motions conversam com a gravação" (cor, fonte e posição dos marcadores de capítulo).
- **revisao-video** (mede o técnico): roda depois; ela mede volume, resolução, emendas e transcrição. A crítica de arte desta skill usa as mesmas folhas de fotos (a folha em pé da revisao-video serve para 9:16) e se concentra no visual. Ordem sugerida no fim: revisao-video (técnico) → direcao-de-arte Parte C (visual) → entrega.
- **Ciclo de aprendizado:** reação do dono a um estilo vai para o repertório (campo de reação), crítica que se repete vira item do checklist ou do `nivel.md`.

## Para instalar (quando o dono aprovar)

Copiar a pasta para `~/.claude/skills/direcao-de-arte/`, criar o atalho no repositório como as outras (`skill-direcao/`) e citar no CLAUDE.md do estúdio em "Antes de qualquer vídeo".
