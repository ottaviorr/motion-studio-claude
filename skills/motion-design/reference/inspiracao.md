# Inspiração: o que os melhores vídeos feitos com IA têm em comum

Fonte: galeria skillry.dev/ai-videos/opus-5-5 (475 vídeos virais feitos com Claude Opus 5.5; prompts públicos em github.com/yihui-dev/awesome-opus5-5-videos, `data/videos.json`) e os lançamentos da HeyGen com código aberto (github.com/heygen-com/hyperframes-launches). Pesquisa de 07/10/2026. Use como régua, não como cópia.

## Padrões que se repetem nos melhores
1. **Gancho em 1,5 s e uma ideia nova a cada 1,5–2 s.** Nada de intro de logo de 5 s. Final parado tempo suficiente para ler.
2. **Câmera contínua em vez de troca de slide.** Empurrões e pans de 1,5–3 s com ease-in-out, metade da velocidade "padrão". **Um objeto da cena vira a transição seguinte** (o ponto do gráfico cresce e vira o canto do próximo cartão). Cortes de "velocidade casada": a curva que sai de uma cena continua na outra, nada parado no ponto de corte.
3. **Tela de produto em camadas, não print parado.** A UI é reconstruída e cada região anima sozinha: o número principal resolve nítido, o gráfico desenha, as métricas chegam com pequeno atraso. Cursor de macOS grande que clica de verdade. Moldura de navegador/celular.
4. **Tipografia:** Inter/Geist para interface; mono (JetBrains) para número e código; uma fonte display pesada para impacto; manuscrita desenhada com `stroke-dashoffset` para anotação. Texto entra palavra a palavra. No máximo 3–4 palavras por tela.
5. **Paleta contida:** fundo escuro (preto, grafite, azul-marinho) + **um** destaque (dourado/laranja), ou papel creme com tinta. Verde só para estado positivo de verdade. Tudo dos tokens da marca.
6. **Acabamento:** vidro com moderação, brilho suave, grão leve, grade de fundo, halftone. Profundidade com parallax leve e desfoque de fundo.
7. **O que NÃO fazer:** excesso de partículas, glassmorphism em tudo, cartão girando em 3D, zoom constante, UI quicando, 20 estilos de animação no mesmo vídeo, glitch, parágrafo de marketing, dashboard falso. "Confiança visual vem da contenção."
8. **Som amarrado à imagem:** cortes na batida (120–129 BPM), um som curto por elemento que aparece e silêncio no resto; o vídeo também precisa funcionar sem som. Master -14 LUFS / -2 dBTP.
9. **Versões da mesma base:** 30/15/6 s em 16:9 e 9:16 como listas de cenas diferentes; o vertical é **recomposto**, não cortado.
10. **Autoverificação:** folha de contato com ~20 quadros antes do render final; estado inicial de tudo definido em t=0 (a cena pode ser "pulada" para qualquer tempo).

## Estrutura de briefing que funciona (modelo dos prompts mais fortes)
1. Fonte da verdade: site/app/marca reais (cores, fontes, telas) — `marca.css`, `MARCA.regras`.
2. Regras criativas centrais (3–5 frases) e a lista do que não fazer.
3. Formato: resolução, fps, duração.
4. Arco emocional (ex.: caos → controle → clareza → marca).
5. Storyboard com tempos (cena por cena, o que entra em qual palavra).
6. Transições, movimento, luz/material, tipografia, som e ritmo.
7. Só produto real; não inventar números nem clientes.
8. "Não pare na primeira versão": olhe a folha de contato e refaça o que estiver apressado, sobreposto ou cortado.
