# Decupagem narrativa: ler o vídeo como roteiro

Quem grava explicando ao vivo pensa em voz alta: começa uma frase, desiste, mostra o mesmo passo duas vezes, monta um caminho e troca por outro no meio ("ou melhor…"). Ao vivo isso passa. Gravado, confunde: o espectador não sabe qual das duas versões vale. O editor bom entrega **a versão que o apresentador queria ter gravado**, sem mudar o que ele quis dizer.

## Como fazer
1. Gere `fonte/frases.txt` (`scripts/frases.py`) e leia **inteiro** antes de cortar qualquer coisa. Olhe também uns quadros de cada trecho: o que se vê na tela importa tanto quanto o que se fala.
2. Divida em **blocos** e dê a cada um uma função: abertura (promessa: o que você vai aprender), conceito (o que é / para que serve), demonstração (como se faz), caso (exemplo real), fechamento (resumo / próximo passo).
3. Em cada bloco, marque:
   - **Repetição:** a mesma explicação ou o mesmo passo mostrado duas vezes. Fica a versão mais completa ou mais clara (geralmente a segunda: o apresentador já "ensaiou" na primeira). Sai a outra.
   - **Caminho abandonado:** ele monta/explica A, depois diz "ou melhor" e **desfaz A na tela** para fazer B. Sai A **e** a frase de troca ("ou melhor, eu até tiro isso aqui"). Fica B, dito de forma direta.
     Não confunda com **evolução**: "dá para tirar a tag à mão… ou melhor, dá para automatizar" apresenta duas opções válidas, a segunda melhor. Nada é desfeito; o espectador ganha as duas. Fica. O teste é a tela: se A some/é apagado, foi abandonado; se A continua valendo, é evolução.
   - **Frase sem fim / recomeço:** "eu coloquei aqui para… eu posso colocar aqui para…" → fica a última tentativa.
   - **Desvio:** comentário que não ajuda o objetivo do vídeo. Antes de cortar um "desvio", veja se o que ele descreve **continua na tela** (um nó, um campo, uma etapa): se continua, a fala é a legenda daquilo e cortar deixa um elemento sem explicação ("duas horas antes eu mando uma mensagem" explica o nó "2 horas antes" que fica visível no fluxo).
   - **Buraco:** algo que o espectador precisa saber e não foi dito/mostrado. Não dá para gravar de novo: resolva com um motion ou um texto na tela, ou avise.
4. Confira o **arco**: a abertura promete o que o vídeo entrega? O vídeo termina ou só para? Sem fechamento → card de fechamento curto (resumo em 2–3 linhas + marca), sem fala nova inventada.
5. **Capítulos** (aulas e tutoriais acima de ~2 min): um marcador discreto no começo de cada bloco ("Exemplo · etapa do funil", "Como criar a ação", "Caso real · agendamento"). Ajuda a pessoa a saber onde está.
6. Escreva `fonte/narrativa.md`: tabela bloco × frases × função × diagnóstico, a lista de cortes editoriais (com o texto que sai e o porquê) e os capítulos.

## Cuidados
- **Na dúvida, fica.** Corte editorial que tira informação é pior que um pouco de redundância. O objetivo é que o espectador entenda — não o menor vídeo possível.
- **Corte editorial muda conteúdo.** Liste cada um no `ENTREGA.txt` com o texto que saiu, para o dono poder pedir de volta.
- **Continuidade da tela:** antes de cortar um bloco, olhe o quadro antes e depois do corte. Se a tela muda muito, a emenda leva fusão (o plano marca sozinho). Se o que sai era o lugar onde algo foi criado e depois aparece pronto, tudo bem (o espectador aceita "já está pronto"); se a fala seguinte diz "isso aqui" apontando para o que sumiu, não corte ali.
- **A frase depois da emenda tem que se sustentar sozinha.** Prefira cortar em fim de frase. Se cortar no meio, ouça (`scripts/ouvir_emendas.py --cortes`): "…duas horas depois dele ter acontecido, e coloco assim: remover tag" funciona; "…quando alguém mover o lead para essa etapa ‖ é bem simples de criar" não (frase sem fim).
- **Não reescreva o apresentador.** Cortar é escolher entre o que ele disse; nada de juntar palavras soltas de lugares diferentes para formar frase nova (a boca na câmera denuncia).

## Exemplo real (aula de exemplo, 4min25 → 2min48)
| Bloco | Frases | Diagnóstico | Decisão |
|---|---|---|---|
| Abertura + o que a ação faz | 1–6 | ok | fica (motions de abertura e da ação) |
| Exemplo: etapa do funil | 7–12 | recomeço; 20 s calado configurando; metade final da 12 mostra a configuração que é refeita no bloco seguinte | corta o recomeço, o silêncio e a 2ª metade da 12 |
| Como criar a ação | 13–18 | gaguejada | fica (é a versão completa) |
| Uma tag, duas automações | 19–22 | coração da aula | fica (motion "uma tag só") |
| Caso real: agendamento | 23–33 | monta "update → ativa", explica e troca por "remover tag" | corta o caminho abandonado e o "ou melhor, eu até tiro isso aqui" |
| Fim | — | termina em "…minha empresa, etc." | card de fechamento com o resumo |
