# Relatório: skill "hierarquia-visual"

Data: 08/10/2026. Pasta: `.ferramentas/pesquisa-skills/hierarquia-visual/` (nada fora dela foi editado; nada foi commitado).

## O que foi entregue

| Arquivo | O que é |
|---|---|
| `SKILL.md` (150 linhas) | a skill no formato do skill-creator: como montar a hierarquia de uma cena (10 passos), a TABELA DE NÚMEROS para 1080×1920 e 1920×1080, regras de cor, o uso da ferramenta e o checklist |
| `scripts/conferir_hierarquia.mjs` | ferramenta de conferência automática (Node 24 + Chrome do sistema via CDP, sem pacotes) |
| `references/tabela-numeros.md` | todos os números com fonte e a conta de conversão celular ↔ px do vídeo |
| `references/tipografia.md` | escala, altura-x, peso, entrelinha, tracking, quebra de linha, CSS pronto |
| `references/cor.md` | fundo · tinta · um destaque, como escolher o destaque, cor semântica, daltonismo, WCAG e APCA (fórmulas) |
| `references/leitura-em-video.md` | tempo de leitura, quantidade de texto, o que o olho lê primeiro, movimento como hierarquia, zoom de UI, grid |
| `teste/` | cópias das cenas e arquivos da base (r02, r03, r09, r10 do projeto cliente A e a cena deitada da padaria), uma cena sintética com valores conhecidos, os relatórios `.txt`/`.json` e as folhas de fotos `fotos-*/folha.jpg` |

Para instalar: copiar a pasta para `~/.claude/skills/hierarquia-visual/` (sem a pasta `teste/`).

## O que foi pesquisado (e as fontes principais)

- **Tamanho legível no celular:** Apple HIG (corpo 17 pt, mínimo 11 pt, Large Title 34 pt), Material 3 type scale, Legge & Bigelow 2011 (tamanho crítico de leitura = 0,2° de altura-x). A conta 1080 px ÷ 393 pt dá **1 pt = 2,75 px** no reel, então 11 pt = 30 px, 17 pt = 47 px, 34 pt = 93 px. Uma VSL 16:9 vista com o celular em pé tem 1 pt = 4,9 px (letra ~1,8× maior que no reel).
- **Legenda e leitura:** Netflix (42 caracteres por linha, 2 linhas, 17 cps em PT-BR, mínimo 0,833 s, máximo 7 s, regras de quebra), BBC (0,33 s por palavra; fonte primária bloqueada, citada por terceiros), Clearcast (0,2 s por palavra + 2 s em texto de anúncio), leitura em PT-BR de ~180 palavras/min (Messias 2008, IReST), Brysbaert 2019.
- **Zonas seguras:** Meta Reels anúncio (14% topo, 35% base, 6% lados: x 65–1015, y 269–1248, fonte oficial), YouTube Shorts (imagem do Google), TikTok (sem número oficial em texto; números de terceiros), EBU R95 (grafismo 5% = 96/54 px em 1080p) e SMPTE ST 2046-1.
- **Contraste:** WCAG 2.2 (4,5:1 e 3:1; texto grande = 24 px ou 18,66 px negrito) e APCA 0.0.98G-4g (fórmula e constantes do apca-w3; Lc 90/75/60/45/30/15 por uso). A fórmula implementada bate com os valores de referência (preto/branco Lc 106,04; #888/branco 63,06).
- **Tipografia:** escalas modulares (typescale.com), Refactoring UI (peso e cor antes de tamanho; "apague o resto"), Bringhurst (45–75 caracteres por linha; caixa-alta +5–10%), Butterick (entrelinha 120–145%), tracking dinâmico da Inter (−0,022 em a partir de 32 px), MDN `text-wrap: balance`.
- **Cor e atenção:** 60-30-10 (regra prática), Treisman & Gelade 1980 (cor única "salta"), von Restorff, NEI/NIH (daltonismo em 8% dos homens), WCAG 1.4.1 (cor não pode ser o único sinal), Refactoring UI (texto secundário com o matiz do fundo).
- **Movimento e leitura:** Abrams & Christ 2003 (o INÍCIO do movimento captura a atenção, o movimento contínuo não), Smith & Mital 2013 (o olhar converge no movimento), NN/g (leitura em camadas, proximidade, região comum), Material 3 (durações e curvas), WCAG 2.3.1 (≤ 3 flashes por segundo).

Ficou sem fonte primária, e por isso está marcado como decisão do estúdio:
- razão título ÷ apoio ≥ 1,5 (falha) / ≥ 2 (recomendado);
- espaço de 1:2 entre os grupos;
- valores de stagger;
- números do TikTok e dos Shorts;
- os 8% de altura da BBC.

## As 10 regras mais valiosas

1. **Multiplique tudo por 2,75 no reel.** 1 pt do celular = 2,75 px do vídeo 1080×1920. O mínimo absoluto é 30 px (11 pt), uma frase pede ≥ 40 px (o recomendado é 44–60) e um título ≥ 84 px. Numa VSL 16:9 que vai rodar com o celular em pé, multiplique por 4,9: rótulo 54 px, apoio 72 px, título 150 px.
2. **Um nível 1 só, e três tamanhos no máximo.** Título, apoio e rótulo saem de uma escala de razão 1,333–1,618 e não muda o tamanho de um elemento por vez. A razão título ÷ apoio é ≥ 1,5 (melhor ≥ 2).
3. **Rebaixe antes de aumentar.** O apoio vai em peso 500–600 e tinta secundária; o rótulo vai pequeno, em caixa-alta e com +0,05–0,10 em de tracking. Peso < 400 nunca. Serif display e manuscrita só a partir de 56 px.
4. **Contraste medido no pixel, atrás de cada letra.** O texto normal precisa de ≥ 4,5:1 e o grande de ≥ 3:1. No reel, "grande" é ≥ 66 px, ou ≥ 51 px em negrito. Para o apoio, a meta do estúdio é 7:1. Exemplo achado no teste: o vermelho suíço #E3241B sobre o papel #F1EFE9 dá 4,0:1, então só serve para texto ≥ 51 px em negrito.
5. **Fundo · tinta · UM destaque (≤ 10% da área).** Um destaque só, porque a cor única salta sem o olho procurar. O verde fica só para o estado positivo, sempre com ícone ou palavra junto, porque 1 em cada 12 homens é daltônico.
6. **Zona segura do destino, em números.** Reels orgânico: y 220–1540, sem nada em x > 930 a partir de y 700. Anúncio Meta: x 65–1015, y 269–1248. Uma peça para as três plataformas: x 65–888, y 288–1248. 16:9: 96/54 px das bordas.
7. **Tempo de tela = máx(1 s; 0,5 s + 0,33 s × palavras).** Texto de oferta ou de condição pede ≥ 2 s + 0,2 s por palavra.
8. **Título com 3–4 palavras (máx. 6), 2–4 por linha, até 3 linhas, quebrado pelo sentido.** Não deixe palavra sozinha na última linha. Fora de UI, ≤ 15 palavras na tela ao mesmo tempo; acima de 25 é falha.
9. **UI precisa de zoom = 30 ÷ tamanho do texto da UI.** No kit cliente A (UI de 20–23 px), isso dá 1,3–1,5×. A janela inteira só aparece por menos de 1 s, como mapa.
10. **A ordem de entrada é a ordem de leitura.** O que puxa o olho é o início do movimento. Só uma coisa começa a se mexer por vez, no ponto que importa: o título primeiro, o apoio 0,2–0,4 s depois, o detalhe por último. Elementos do mesmo grupo entram iguais (destino comum).

## A ferramenta: `scripts/conferir_hierarquia.mjs`

**Como funciona**

Abre a cena no Chrome sem janela, no mesmo padrão do `kit/gravar.mjs` (porta 0 + DevToolsActivePort). Depois:
1. Varre a cena a cada 0,1 s e registra quando cada texto aparece e some, para calcular a exposição.
2. Em cada tempo de conferência (8 espalhados + os 2 momentos com mais texto), chama `frame(t)` e mede pelo DOM:
   - texto visível (por `visibility`, `display`, opacidade acumulada e `overflow` dos pais);
   - tamanho efetivo = font-size × escala acumulada de `transform`, `scale`, `zoom` e da CTM do SVG;
   - linhas, palavras e papel (UI ou não).
3. Fotografa o quadro duas vezes: normal e com todo o texto transparente. A diferença entre as duas é a tinta; a segunda foto é o fundo atrás de cada letra. Daí saem:
   - WCAG e APCA medidos no núcleo da letra;
   - o pior trecho e o desvio do fundo (fundo agitado);
   - a caixa do texto pela tinta de verdade, que resolve máscara e corte;
   - texto encoberto, que não é contado.
4. Mede as cores de destaque do quadro inteiro (OKLab, croma > 0,07, agrupadas por matiz; o que cobre mais de 35% conta como fundo).
5. Mede de novo 0,15 s depois. Texto que mudou de tamanho ou posição (câmera, passagem) ou que está com opacidade parcial (entrando ou saindo) vira INFO, não FALHA.
6. Gera o relatório por tempo, a seção de exposição e um resumo por tipo de problema que conta **textos distintos**. Com `--fotos`, salva fotos com as caixas pintadas e a zona segura, mais uma `folha.jpg`. Com `--json`, salva tudo em JSON. Sai com código 1 se houver FALHA.

Leva ~7 s por cena de 35–45 s.

### Resultado do teste

**Cena sintética** (`teste/cenas/zz-sintetica.html`, valores conhecidos): todos os valores esperados foram medidos exatamente.
- 100 px preto em branco: 21,00:1 e Lc 106, como na referência.
- Texto de 20 px dentro de `scale(2)`: medido como **40 px** efetivos.
- #777 em branco: **4,48:1**, FALHA por pouco, correto.
- 24 px: FALHA (< 30).
- Texto em y 1400: AVISO (fora da área do anúncio).
- Texto em x 950: FALHA (fora da zona).
- Texto que aparece de 0,6 s a 1,0 s: "ficou 0,4 s, precisa de 1,2 s", FALHA.

**4 cenas reais aprovadas da série cliente A** (cópias em `teste/cenas/`) e **1 cena 16:9** (`teste/deitada/`):

| Cena | Falhas (textos distintos) | Avisos | Textos com tempo suficiente | Principais achados |
|---|---|---|---|---|
| r03a funil (suíço P&B) | 73 | 50 | 83 de 105 | Rótulos mono de 20–26 px nos cartões (nº da etapa, "Instagram", "R$"). Quadro afastado do funil com textos de 9–19 px por vários segundos. Vermelho #E3241B em texto pequeno a 4,0–4,3:1. 5–7 tamanhos de texto por tela. "Pagou?" fica 0,5 s. |
| r10a cupom (amarelo brutalista) | 47 | 69 | 64 de 81 | Cabeçalho do cupom em 22–24 px. Texto sobre o amarelo com sombra/papel a 2,8–3,5:1. 36 textos de UI abaixo de 30 px (a fala cita alguns). |
| r09a aviãozinho (papelaria) | 24 | 31 | 56 de 66 | Rótulos do formulário em 22–24 px, cinza #6E768C sobre papel (4,16:1). Título serif 92 px no kraft com Lc 57 (aviso). Notificação de 5 palavras por 1,4 s. |
| r02a madrugada (celular no escuro) | 44 | 54 | 47 de 60 | Hora e status do celular em 14–18 px. Notificação em cinza (3,5:1). Frase "quando o cliente está pronto" em tamanho de rótulo. |
| 16:9 padaria | 2 | 3 | 3 de 7 | Pílula "fornada do dia" 20 px (< 26). URL "paodeouro.com.br" a 3,2:1. Os outros 4 textos não contam como falha: são relógio que gira (aviso) ou textos que vão até o fim da cena (info). |

Leitura honesta do resultado:
- Os títulos dos reels aprovados passam em tudo: 92–150 px, 6–18:1, na zona.
- As falhas se concentram em rótulos e detalhes de 9–26 px, em cinzas/vermelhos sobre papel e em textos que passam rápido.
- Isso bate com a percepção de "bonito mas cheio" e mostra onde a próxima série pode subir de nível sem mudar a direção de arte:
  - rótulos ≥ 30 px;
  - 3 tamanhos por tela;
  - vermelho/cinza só em texto grande;
  - segurar cada título ≥ 1,0–1,5 s.
- Muitos avisos de UI são aceitáveis, porque a interface é cenário. A ferramenta diz quanto aproximar se a fala citar o texto.

Exemplo de saída real (r03a, t = 26,1 s):
```
== t = 26,10 s ==  palavras: 3 (+63 em UI)  ·  níveis: 108 px  ·  destaques de cor: #e42f27 2,1%
  OK    único   108 px 800 Inter Tight      "Quanto dinheiro parado."  15,33:1 Lc 95  #181818/#F1EEE8
  FALHA UI       30 px 700 Azeret Mono      ×3 "2 pessoas", "5 pessoas", "2 pessoas"  4,27:1 Lc 65  #E3251C/#F7F6F2  → contraste 4,27:1 < 4.5:1 (WCAG texto normal)
  AVISO UI       19 px 600 Inter Tight      "WhatsApp"  9,68:1 Lc 77  #D4D4D4/#2A2A2A  → UI em 19 px < 30 px: se a fala cita este texto, aproxime 1,60× ou mais
```

### Limitações conhecidas

- Não sabe o que a narração cita: por isso, UI pequena é AVISO.
- Não mede texto em imagem nem texto com `background-clip:text`.
- A varredura de exposição usa opacidade ≥ 0,5 pelo DOM, sem foto.
- Contador ou relógio que troca no lugar vira AVISO, não FALHA.
- Precisa de internet para as Google Fonts da cena, igual à gravação.

## Próximos passos sugeridos

1. Copiar a skill para `~/.claude/skills/hierarquia-visual/` e citar em `motion-design/SKILL.md` no passo "Conferir antes de gravar".
2. Pôr os tokens `--t1/--t2/--t3` no `kit/modelo-cena.html`.
3. Acrescentar no `nivel.md`: "rótulo ≥ 30 px; 3 tamanhos por tela; texto ≥ máx(1 s; 0,5 + 0,33 × palavras)".
4. Calibrar com o dono se a falha de exposição em títulos narrados deve ser mais branda: quem ouve a voz lê mais rápido.
