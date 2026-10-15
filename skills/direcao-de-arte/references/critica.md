# Crítica de arte: como olhar, como julgar, como mandar ajustar

## 1. Crítica não é gosto

Há três tipos de retorno (Connor & Irizarry, *Discussing Design*):

| Tipo | Exemplo | Serve? |
|---|---|---|
| Reação | "Não gostei do verde." | Não: fala de quem olha, não da peça |
| Ordem sem motivo | "Troca pra azul." | Pouco: resolve uma vez, não ensina nada |
| **Crítica** | "O verde do fundo é a mesma cor do 'confirmado', então a virada não se destaca. Fundo neutro, verde só no confirmado." | **Sim**: elemento + objetivo + efeito |

Toda observação responde às 4 perguntas:
1. Qual o objetivo desta cena (do cartão de direção e da frase da voz)?
2. Que elementos servem a esse objetivo?
3. Eles funcionam?
4. Por quê / por que não?

Ordem de fala (a "escada"): **entender → valorizar → apontar → sugerir.** Diga primeiro o que funciona (para não ser destruído no ajuste), depois os problemas, depois as ordens.

## 2. Preparar o material

- Folha de fotos nas batidas (antes de gravar): `FOTOS_DIR=<pasta> bash fonte/fotos.sh cena.html t1 t2 ...` e `bash fonte/grade.sh folha.jpg <pasta>/*.jpg`. Em pé: folha em pé com a zona segura (skill revisao-video).
- Folha do vídeo final: ~1 quadro por segundo ou um por cena (75 % da duração).
- Teste do olho apertado: `bash scripts/apertar-olho.sh folha.jpg` → miniatura, borrada e em cinza lado a lado.
- O cartão de direção aberto ao lado. Sem cartão não há crítica objetiva, só opinião.

## 3. Checklist objetiva (o que olhar, com números)

Marque cada item: ✅ ok · ⚠️ deve ajustar · ⛔ bloqueia a entrega.

### Hierarquia e leitura
1. **Um ponto focal por quadro.** Na versão borrada sobra UMA mancha dominante e é a certa (título ou produto). Duas manchas iguais = ninguém sabe onde olhar.
2. **Valor (claro/escuro) separa as camadas.** Na versão em cinza, texto e fundo não viram a mesma massa. Contraste do texto ≥ 4,5:1 (letra pequena) e ≥ 3:1 (título grande).
3. **Tamanho no celular (1080×1920):** título ≥ 84 px, apoio ≥ 40 px, rótulo ≥ 28 px. Em 1920×1080 deitado que vai para o Reels: título ≥ 72 px.
4. **No máximo 3–4 palavras por tela** e uma linha de título (duas só se for a frase-gancho).
5. **Zona segura:** tudo que importa entre y 230 e 1300; nada importante em x > 930 a partir de y ≈ 700 (botões do Reels).

### Fidelidade ao cartão
6. **Nenhuma cor fora do cartão.** Conte: fundo, tinta, destaque, neutros derivados. Cor nova = ⚠️ (inventada no meio do caminho).
7. **O destaque aparece só onde a regra manda** e em no máximo 1 lugar por quadro.
8. **Fontes = as 3 do cartão**, nos papéis certos. Fonte de sistema aparecendo (fonte que não carregou) = ⛔.
9. **Ícones do mesmo conjunto** (mesmo traço, mesmos cantos, mesma cor). Ícone redondinho colorido de app = ⛔ (pedido do dono).
10. **Textura na intensidade do cartão** e visível depois da compressão (grão que some no H.264 não existe; textura que suja o texto, sim, atrapalha).

### Composição
11. **Peso ancorado.** Conteúdo preso a borda, canto ou grade; "tudo centralizado flutuando" só se o cartão pediu (fecho solene).
12. **Espaço vazio de propósito.** Nem tela vazia de slide (fundo liso + uma frase pequena) nem tudo cheio. Fundo claro precisa de estrutura (fios, grade, papel) para não parecer slide em branco.
13. **O produto se lê.** Tela do produto com zoom 1,3–1,5×, nunca a janela inteira pequena por mais de um instante.
14. **Escala de vídeo, não de site:** bordas 2–4 px, padding grande, nada de sombra de 1 px invisível.

### Sequência (folha inteira em ordem)
15. **A história aparece sem som.** Só olhando os quadros, dá para dizer o problema, a virada e a solução?
16. **Quadro 0 funciona como capa.** Gancho visível no primeiro quadro, nada entrando do preto/vazio.
17. **A virada é visível** (muda luz, cor, ritmo ou estilo de propósito).
18. **Fecho no idioma da peça** (mesma paleta e fontes), logo legível, parado ≥ 1 s.
19. **Os quadros parecem a mesma peça** (sem cena "de outro vídeo").

### Movimento (assistindo, não na folha)
20. **Uma corrente**; mudanças de direção têm causa visível.
21. **Assinatura presente** (o movimento que só esta peça tem).
22. **Nada balançando parado** (respirar, flutuar, brilho pulsando para "encher").
23. **Sem quique/elástico, sem partícula, sem glitch, sem giro 3D gratuito.**
24. **Pausa antes do clímax** (0,3–0,75 s) e final parado o bastante para ler.

### Sinais de IA
25. Passe a lista de `anti-ia.md`. Três sinais ou mais = a peça parece genérica, mesmo com tudo acima certo.

### Série
26. A peça não repete a família, a fonte de título nem a escola da peça vizinha (`scripts/conferir-serie.py`).

## 4. Ordens de ajuste (formato fixo)

**Onde · O que está · Por que atrapalha · O que fazer · Como conferir.**

Exemplos:

| Ruim | Bom |
|---|---|
| "Tá muito poluído." | "Cena 05, 3,1 s · 7 elementos com o mesmo peso (4 cards, 2 ícones, título) · o olho não acha o título, e a frase é 'uma caixa só' · deixar 1 caixa grande no centro-esquerda, os 4 cards encolhem para 30 % e saem de foco · na folha borrada, a caixa é a única mancha." |
| "Muda essa cor." | "Fundo do fecho `#7B5CF0` · cor fora do cartão (o reel é suíço P&B + vermelho) · o fecho parece outro vídeo · fundo `#F1EFE9`, logo na tinta, vermelho só no 'Comente CRM' · conferir que não há hex fora do cartão (`grep -o '#[0-9A-Fa-f]\{6\}' cena.html \| sort -u`)." |
| "Coloca mais movimento." | "Cena 04, 2–6 s · tudo entra até 1,2 s e fica parado 4 s · parece slide · segurar os 3 itens e revelar cada um na palavra (`W('lembrete')`, `W('confirma')`, `W('avalia')`) · pausar em qualquer segundo: algo está chegando." |
| "Tá com cara de IA." | "Cenas 02–06 · gradiente roxo→azul + cards com ícone redondo + brilho · 3 sinais da lista anti-IA · trocar o fundo pelo papel do cartão, ícones por traço 2 px quadrado, tirar o brilho · rever na folha: nenhum dos 3 sinais." |

Regras:
- **Problema antes de solução.** Se a solução não for óbvia, descreva bem o problema e deixe quem anima propor.
- **Uma ordem por problema.** Nada de "e também..." na mesma linha.
- **Sempre o "como conferir".** Ordem sem conferência volta errada.
- **Gravidade:** ⛔ bloqueia (não entrega) · ⚠️ deve (entrega pior sem) · 💡 pode (polimento, se der tempo).

## 5. Ajustar, refazer ou voltar ao conceito

- **Ajustar:** problema local, cartão respeitado, ideia funciona.
- **Refazer a cena:** a cena não desenha a frase, ou o quadro parado continua feio depois de 2 rodadas de ajuste.
- **Voltar ao conceito:** mais de 1/3 das cenas com o mesmo problema; a peça parece a anterior; trocando o logo, vira "qualquer marca"; três ou mais sinais de IA mesmo com o cartão cumprido (o cartão era genérico).
- **Voltar ao briefing:** bonito, mas sem som ninguém entende a mensagem.

Limite: **duas rodadas** de ajuste na mesma cena. Na terceira, refaça a composição.

## 6. Exemplos reais do estúdio

- **Reel 01 da série de exemplo (piloto):** reação do dono "gostei do estilo", mas "nem sempre roxo, nada de ícones redondinhos". Crítica que faltou antes: item 9 (conjunto de ícones) e a regra da série (a cor da marca não é o fundo de todas).
- **Série 02–15:** escrita a bíblia inteira antes, cada reel com conceito próprio → "gostei demais dos resultados". Crítica que funcionou: conferir vizinhos e contar claro × escuro na tabela.
- **Carimbo "IMPOSTO"** (VSL anterior) leu como "taxa": item 15 (ler como o espectador) — frase literal ganha de trocadilho.
- **Música alta sob a voz:** não é direção de arte, mas a mesma lógica: medir em vez de achar (motion-design, `gerar_reel.py`).
