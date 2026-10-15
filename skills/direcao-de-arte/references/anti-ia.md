# Sinais de "feito por IA" e o antídoto de cada um

"Se você mostrasse e dissesse 'foi uma IA que fez', a pessoa acreditaria na hora? Se sim, esse é o problema." O vídeo bom faz perguntar "como fizeram isso?", não "qual IA fez?". Os sinais abaixo são os padrões para onde os modelos convergem sozinhos; quase sempre aparecem juntos. **Três ou mais na mesma peça = genérico.**

Fontes: lista de "lazy defaults" do HyperFrames (`hyperframes-creative/references/house-style.md` e `typography.md`), anti-padrões do Impeccable (pbakaus), regras do prompt Taxtello e dos "Banned" do skillry, e as críticas do dono.

## Cor
| Sinal | Antídoto |
|---|---|
| Gradiente roxo→azul, ciano/neon no escuro | Paleta do conceito, 1 destaque com regra de uso |
| Escuro "premium" como padrão, com brilho | Escolha claro/escuro pelo conceito; maioria clara (dono) |
| Texto em gradiente (`background-clip:text`) | Cor sólida; destaque por tamanho/peso/serif itálico |
| `#000` e `#fff` puros, cinza morto | Neutros puxados para a matiz do conceito (`#111` quente, `#F1EFE9`) |
| Muitas cores "equilibradas" | Uma dominante + um destaque forte |
| Gradiente linear de tela inteira no escuro | Fundo sólido + brilho radial localizado (evita faixas no H.264) |

## Tipografia
| Sinal | Antídoto |
|---|---|
| Inter, Roboto, Poppins, Montserrat, Open Sans em tudo | Fonte com caráter que sai do conceito (repertório) |
| A fonte "diferente" batida: **Syne**, Playfair, Cormorant, Cinzel, Outfit, Sora | Mesma lista de banidas do HyperFrames: só com motivo explícito |
| Duas sem-serifa parecidas (título e apoio) | Sistema de 3 papéis: grito / apoio / número, com contraste real (serif+sans, sans+mono, condensada+larga) |
| Mono usada só para "parecer técnico" | Mono só para número, hora, código, rótulo de metadado |
| Título pequeno de site no vídeo | Escala de vídeo (título 84–200 px em 9:16) |

## Layout e elementos
| Sinal | Antídoto |
|---|---|
| Grade de cards iguais (ícone + título + texto) | Um elemento protagonista; os outros recuam |
| **Ícone redondinho colorido acima de cada título** (pedido do dono) | Conjunto do estilo (traço 1,5–3 px, cantos do estilo) ou nenhum ícone |
| Tudo centralizado com peso igual | Peso ancorado em borda/canto/grade |
| Glassmorphism em tudo | Vidro em 0–3 momentos com motivo |
| Métrica gigante + rótulo + "+23 %" inventado | Só número oficial (`MARCA.regras`); quantidade sem número (nível 15) |
| Dashboard falso genérico | Tela real ou réplica fiel do produto com dados inventados plausíveis |
| Barra colorida na borda esquerda do card | Fio, numeração, rótulo mono |
| Sparkline decorativa sem dado | Gráfico só com dado que a fala cita |

## Movimento
| Sinal | Antídoto |
|---|---|
| Tudo entra de baixo com fade (`y:30, opacity:0`) | Entradas pela corrente da peça, ligadas à palavra |
| Elementos "respirando"/flutuando para encher tempo | Revelações em etapas, câmera com intenção, interface funcionando (motion-doctrine) |
| Quique, elástico | Mola curta com no máximo um pequeno passe |
| Partículas, glitch/RGB split, lens flare, tremor de câmera | Nada; efeito só com motivo de conceito (ex.: desalinhamento riso só no impacto) |
| Cartão girando em 3D, zoom constante | Profundidade com parallax leve e perspectiva fixa |
| Fusão (crossfade) entre cenas | Corte no meio do movimento, objeto que carrega o olho |
| 20 estilos de animação no mesmo vídeo | Um estilo de movimento + 2–3 transições repetidas |
| Logo de abertura de 5 s | Gancho no quadro 0; logo no fecho |

## Texto e conteúdo
| Sinal | Antídoto |
|---|---|
| Parágrafo de marketing na tela | 3–4 palavras por tela; a voz explica |
| Frase de efeito vazia ("Revolucione seu negócio") | A frase literal da fala |
| Trocadilho visual que confunde | Literal ganha (nível 7) |
| Pessoas/rostos gerados por IA | Sem rostos falsos; ilustração assumida ou retrato em pontinhos |

## Antídotos de nível alto (o que os melhores fazem)
1. **Imperfeição intencional:** 15 fps "em dois" no que é feito à mão (a Figma baixou de 60 para 15 fps para parecer "tátil, feito à mão, não tão liso"), tremor de plotter, desalinhamento de riso — sempre em quantidade controlada e com motivo.
2. **Material de verdade:** papel, retícula, cupom, tinta — vem com textura e lógica própria.
3. **Restrição declarada:** "nenhuma outra cor", "só estas 3 fontes", "o destaque só aparece no card que se move".
4. **Lista de proibidos específica da peça** no cartão de direção.
5. **Detalhe de produção:** rótulos mono de metadado, numeração, marcas de registro, carimbo — "o que faz parecer produzido, não gerado" (HyperFrames, video-composition).
