# Unidade × variedade numa série

O problema: 15 reels iguais cansam o feed (o dono pediu para variar); 15 reels sem nada em comum não constroem marca. A solução dos estúdios de identidade é um **sistema**: um núcleo pequeno que nunca muda e variáveis que mudam com regra.

- Pentagram (campanha do Channel 5): sistema modular "altamente flexível, que comporta conteúdos muito diferentes mantendo forte consistência visual em vários formatos", com modelos que a equipe aplica com confiança.
- Figma (Config): "restringir o conceito, não a execução"; paleta grande gerida por variáveis ("para nada parecer cansado"); o logo "você reconhece, mas ele se comporta um pouco diferente a cada ano".
- Prompt do skillry `stokebuilder-356793` (50 animações para um podcast): "escreva primeiro uma bíblia de estilo compartilhada e um kit de componentes, para toda animação parecer o mesmo programa".

## 1. O que fica fixo e o que muda

| Camada | Fixo na série | Muda por peça |
|---|---|---|
| Marca | Logo, nome, grafia, regras de texto (`MARCA.regras`), preços oficiais | Cor da marca vira papel diferente (destaque, tinta, virada, fecho) |
| Estrutura | Gancho no 1º segundo, uma frase por cena; fecho com CTA na mesma posição **só em série de uma marca** | O que acontece dentro de cada cena; em série-vitrine também a **linguagem** (`cardapio-linguagens.md`), o **fechamento e o CTA** (`fechamentos.md`) |
| Técnica | Formato, fps, CBR, -14 LUFS, zona segura, tamanho mínimo de letra | — |
| Voz e som | Narrador, nível da música (≈ 21 dB abaixo da voz) | A trilha |
| Visual | **Uma regra de série** (ex.: "sempre um único destaque de cor", "o produto sempre aparece real em algum momento") | Paleta, fontes, textura/material, ícones, como o produto aparece, movimento, corrente |

Quanto mais forte o núcleo fixo de estrutura (fecho, CTA, gancho), mais a parte visual pode variar sem a série se perder.

**Série-vitrine** (amostras de nichos diferentes, prospecção, portfólio): o objetivo é mostrar repertório, então o núcleo encolhe para a qualidade técnica e o rodapé (@, "imagens ilustrativas"). Linguagem, % de vídeo, fechamento e CTA viram variáveis com regra de vizinho (SKILL.md, Parte B). Foi o erro da v2 da prospecção: a série variou a fonte e repetiu a linguagem e o fecho nas 14.

## 2. Eixos de variação (gire pelo menos 3 entre vizinhos)

1. **Luz:** claro / escuro / colorido saturado (amarelo, azul de planta).
2. **Matiz do fundo:** quente (papel, kraft) / frio / neutro.
3. **Família tipográfica do título:** grotesca / serif / condensada / larga / mono / manuscrita.
4. **Material:** liso / papel / impresso (halftone, riso) / técnico (grade, blueprint) / tela (terminal, painel).
5. **Como o produto aparece:** tela real em camadas / objeto (celular, cupom) / metáfora (planta, mapa) / redesenhado (grade, caderno).
6. **Movimento:** corrente (esquerda / cima / Z) e assinatura (forma única, traço desenhado, flip, impressão, dobra).
7. **Ritmo:** 30 qps liso / 12–15 desenhos/s "em dois" / batida.

## 3. Regras de vizinhança

- Duas peças seguidas **nunca** repetem: família de luz+matiz do fundo, fonte de título, escola do repertório.
- Dois escuros seguidos: proibido (preferência do dono). Meta: **≥ 60 % claros**.
- A cor da marca como **fundo**: no máximo 1 a cada 5 peças.
- Mesmo conjunto de ícones: nunca em vizinhos; o ícone-app redondinho colorido não volta.
- Mesma assinatura de movimento: no máximo 2 vezes na série.

- Mesma linguagem do cardápio ou mesmo fechamento: nunca em vizinhos; 3 seguidas na mesma família (V · V+ · M · D · 3D · F): proibido.

Confira com `scripts/conferir-serie.py ESTILOS.md`.

## 4. Como produzir sem custo dobrado

- **Kit de telas re-tematizável:** as réplicas do produto num só arquivo (`cliente-a-ui.css/js`) com variáveis (`--lu-brand`, `--lu-paper`, `--lu-ink`, `--lu-line`…). Cada peça tem `estilo-NN.css` que sobrescreve variáveis, sombras, bordas e a fonte de interface. Variar estilo = trocar CSS, não refazer telas.
- **Funções puras de estado** (`luPipe`, `luChat`, `luAgenda`…): a mesma tela em qualquer estilo.
- **Fecho como componente** (`FECHO()`) que veste a paleta e as fontes da peça.
- **Bíblia antes, agentes depois:** com o `ESTILOS.md` pronto, cada agente produz um grupo de peças em paralelo sem conversar com os outros — a unidade está no documento.

## 5. Matriz da série cliente A (exemplo aprovado: "gostei demais")

| # | Luz | Fundo | Título | Material | Produto | Corrente |
|---|---|---|---|---|---|---|
| 02 | ◐ escuro→claro | azul-noite | Big Shoulders (condensada) | foto/filme | celular-objeto | Z frente |
| 03 | claro | papel neutro | Inter Tight (grotesca) | liso + grade | redesenhado (grade) | esquerda |
| 04 | azul saturado | azul planta | Plex Condensed | técnico | metáfora (planta) | esquerda |
| 05 | claro | jornal quente | Anton (condensada) | impresso (xerox) | colagem → real | cima |
| 06 | escuro | preto | Fraunces (serif) | liso | elementos soltos | esquerda |
| 07 | claro | off-white | Geist | liso | tela em camadas | Z frente |
| 08 | escuro | preto quente | Space Grotesk | tela (terminal) | log → ficha | cima |
| 09 | claro | kraft | DM Serif Display | papel | objeto (formulário) | esquerda |
| 10 | amarelo | amarelo | Archivo Black | impresso (cupom) | objeto (cupom) | baixo |
| 11 | escuro | grafite | Barlow Condensed | tela (painel) | redesenhado (painel) | vertical |
| 12 | claro | papel | Shantell Sans (manuscrita) | papel (caderno) | prints colados | baixo |
| 13 | escuro | azul-noite | Unbounded (larga) | técnico | fluxo → painel | baixo |
| 14 | claro | papel | Anybody (larga) | impresso (riso) | impresso | Z trás |
| 15 | escuro | índigo | Bebas Neue | tecido (jeans) | objeto (celular no bolso) | cima |

Leitura crítica (para a próxima série): 7 de 14 claros contando o amarelo e o kraft (50 %) — abaixo da meta de 60 % que o dono pediu depois; 11 e 13 são escuros separados só pelo 12. As correntes 12 e 13 repetem (para baixo) em vizinhos, e 03/04 também (esquerda) — passou porque o resto mudou muito, mas é o primeiro lugar para variar. Na próxima, trocar um dos escuros técnicos por um claro (ex.: Sinalização de metrô ou Explicador de dados do repertório).
