# Do briefing ao conceito visual

O caminho dos estúdios de motion: **briefing → conceito → referências (moodboard) → quadros-chave (style frames) → storyboard → animação.** Cada etapa é mais barata de mudar que a seguinte. No nosso estúdio: briefing e conceito no cartão de direção, referências por escrito, quadros-chave com `fotos.sh`, storyboard = plano por frase da motion-design.

## 1. Conceito primeiro, estética depois

A equipe da Figma (identidade da Config 2025) começou **pelo conceito, não pelo moodboard**: "restringir o conceito, mas não a execução, é o que faz um sistema adaptável". Moodboard antes do conceito vira catálogo de coisas bonitas sem motivo; o conceito dá o critério para escolher.

Conceito visual = **uma regra que explica todas as escolhas.** Se alguém pergunta "por que essa fonte?", a resposta tem que sair do conceito.

| Conceito fraco | Conceito forte |
|---|---|
| "Moderno e clean, com as cores da marca" | "O pipeline é uma grade suíça: o card vermelho é o único que se move" |
| "Dark premium tech" | "Madrugada: o celular é a única luz do quarto, e quando o cliente agenda, amanhece" |
| "Divertido e colorido" | "O formulário é de papel: ele dobra, vira aviãozinho e pousa na agenda" |

## 2. Cinco geradores de conceito

1. **Objeto-personagem.** Uma coisa concreta atravessa o vídeo e se transforma; o olho segue objetos, não ideias. (Card que anda pelo funil; Poké Ball que vira cada componente; formulário que vira aviãozinho.) Pergunta: *qual objeto do mundo do cliente carrega essa história?*
2. **Regra formal única.** Uma lei vale para tudo. "Uma forma que nunca corta: cada estado é o mesmo elemento mudando de tamanho, raio e cor" (skillry `twoclipping-402193`). "As palavras têm papéis de arquitetura: ESPERAR é viga, VOZ é pilar, CHÃO é plataforma" (`gdgtify-929495`). Pergunta: *que regra, se valesse para o vídeo inteiro, deixaria ele inconfundível?*
3. **Mundo/cenário.** A peça acontece num lugar com luz e objetos próprios: quarto de madrugada, painel de aeroporto, sala de controle, prancheta de engenheiro. Pergunta: *onde essa dor acontece de verdade?*
4. **Material/meio.** O vídeo "é feito de" alguma coisa: papel, xerox, tinta de risografia, cupom térmico, caderno, planta técnica. O material traz textura, cor e até frame rate (xerox a 15 fps). Pergunta: *de que material seria feito esse assunto se fosse impresso?*
5. **A virada como mudança de estilo.** O antes num estilo, o depois em outro; a troca conta a história sem palavra (caos em xerox tremendo → sistema em papel limpo; noite → manhã). Pergunta: *como a tela muda quando o problema é resolvido?*

Combine no máximo dois (ex.: material + virada).

## 3. Teste do conceito (antes de escrever o cartão)

- [ ] Cabe numa frase sem "e" no meio.
- [ ] Dá para descrever o quadro de abertura como foto.
- [ ] Rende cenas pela duração toda (reel de 60–90 s precisa de 6–12 cenas diferentes dentro da mesma ideia).
- [ ] Serve à mensagem (pergunta 2 do briefing) — não é um estilo procurando assunto.
- [ ] O produto real cabe nele (tela real ou réplica fiel aparece em algum momento).
- [ ] Não é a mesma família da peça anterior da marca.
- [ ] Trocando o logo, NÃO vira um vídeo de qualquer marca.

## 4. Referências com função (moodboard em texto)

Não temos onde colar imagens, então o moodboard é escrito e preciso. Cada referência diz **o que se pega dela**:

```
Referências
- Cor e papel: risografia em duas tintas (repertório #9) — pegar o desalinhamento de 2–4 px, não os personagens.
- Movimento: skillry twoclipping-496100 — "cada cena feita da anterior; nada some, funde ou corta".
- Produto: nosso reel cliente A 07 — interface desmontada em camadas, cursor grande.
```

Fontes de referência, nesta ordem:
1. Os nossos exemplos aprovados (`~/.claude/skills/motion-design/examples/`, em especial o `ESTILOS.md` de uma série aprovada).
2. `references/repertorio-estilos.md`.
3. Prompts do skillry (`github.com/yihui-dev/awesome-opus5-5-videos`, `data/videos.json`; página `skillry.dev/ai-videos/opus-5-5/<slug>`). Bons para ler: `daniel-haida-636937` (filme de produto premium com regras), `twoclipping-402193` e `-496100` (forma única, keynote), `gdgtify-929495` (tipografia arquitetônica), `koldo2k-778767` (colagem/xerox), `techhalla-498547` (paleta estrita e sistema de 3 fontes), `stokebuilder-356793` ("escreva uma bíblia de estilo e um kit de componentes primeiro, para toda animação parecer o mesmo programa").
4. Escolas e autores (Müller-Brockmann, Bauhaus, Vignelli, Paula Scher, Memphis, risografia) — pegue a **lógica** (grade, forma primária, linha de metrô), não a superfície.

Regra: no máximo 3 referências. Mais que isso vira média, e média é o que a IA já faz sozinha.

## 5. Quadros-chave (style frames)

Um quadro-chave é um quadro final parado, no estilo definitivo — o contrato visual antes de animar (Buck, School of Motion, Boords). Para nós:

1. Escreva só o **estado final** de 3 cenas: abertura (quadro 0 = capa), virada, fecho.
2. Fotografe (`fotos.sh`) e monte a folha.
3. Critique com `critica.md` (itens 1–14). Passou? Só então escreva as animações.
4. Os 3 quadros ficam na pasta da peça (`fonte/quadros-chave/`) como referência para as outras cenas.

Por quê: problema de composição, cor ou tipo aparece no quadro parado. Animação bonita não salva quadro feio, e refazer animação custa 10× mais.

## 6. Perguntas que o diretor de arte responde (e escreve)

- O que o espectador sente no 1º segundo, na virada e no fecho?
- Qual é o elemento que o olho segue de cena em cena?
- Onde está o peso de cada quadro (canto, borda, centro)?
- O que é real (tela do produto) e o que é ilustração? (vai no guia de entrega)
- Que cor só aparece uma vez, e quando?
- Que fonte grita, qual explica, qual marca número?
- Qual é o único movimento que só esta peça tem?
- O que está proibido nesta peça (específico, não genérico)?
