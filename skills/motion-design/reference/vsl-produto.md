# VSL de produto (telas do app em uso, voz gerada depois)

Feito na VSL do curso GoHighLevel Avançado (cliente B, out/2026). O dono adorou o resultado: "ficou foda".

## Quando usar
Pedido do tipo "um vídeo mostrando o sistema funcionando, sem voz agora, eu faço a voz no ElevenLabs depois". É o modo B (vídeo inteiro em `frame(t)`) com a ordem de trabalho abaixo.

## Ordem de trabalho
1. **Roteiro primeiro.** Uma frase por cena, 12 a 14 cenas, cerca de 70 a 80 s. A estrutura que converteu:
   gancho na dor de quem já paga → dor concreta (cena do dia a dia) → virada ("agora imagina") → uma funcionalidade por frase, mostrada em uso → promessa (montar do zero e vender como serviço) → bônus → preço com garantia → CTA curto.
   Entregue o roteiro num arquivo próprio, com a grafia para a voz pronunciar certo (ex.: "Gôu Rái Lével", "Clód", "cê-erre-eme", "fólou-ap") e uma tabela com o texto normal.
2. **Réplica da interface em vez de print.** Prints de cliente quase sempre têm dados reais. Monte uma "casca" do app em HTML (`crm.js`/`crm.css`: menu lateral, barra superior e ícones) e escreva cada tela por cima, com dados inventados e coerentes entre as cenas (mesma clínica, mesmo paciente, mesma IA). Ícones oficiais podem ser recortados dos prints (só o ícone, sem dados).
3. **Tempos por palavra desde o início.** Use `B(n)` (n = índice da palavra na frase) em vez de segundos soltos. Sem voz, `B(n)` estima cerca de 2,6 palavras por segundo. Com voz, lê o tempo real.
4. **Grave sem voz e entregue** o MP4 de cada cena e o vídeo inteiro (concat), para o dono aprovar o visual.
5. **Quando a voz chegar:** transcreva com `scripts/transcrever.py`, monte a tabela palavra → índice de cada cena e gere `tempos.js` (`window.TEMPOS` com os tempos relativos a cada clipe, `window.DURS` com a duração de cada clipe) e `plano.json` (in/out de cada clipe). Grave de novo: só o tempo muda, o visual fica igual.
6. **Monte com transição** (`montar-final.py`): cada clipe começa X/2 antes da frase e termina X/2 depois do início da seguinte (X ≈ 0,5 s), e `xfade` faz a passagem. Use deslize lateral (`smoothleft`) entre telas do mesmo app, como quem navega, e `circleopen` ou `zoomin` nas viradas de assunto. Narração com `loudnorm` em cerca de -15 LUFS e uma versão web 720p (cerca de 6 MB) para landing page.

## Quando a voz já vem pronta (VSL do programa cliente B, out/2026)
- Dá para pular a etapa "sem voz": transcreva, defina a palavra inicial de cada cena (índice global) num `gerar-plano.py` e use `W('palavra')` no `marca.js` (procura a palavra exata, depois o prefixo, dentro da cena). Mais robusto que contar índices `B(n)`.
- Exemplo do produto do cliente em branco/cinza → com a "sua marca" na palavra: o espectador se vê. Use uma marca de exemplo neutra ("Sua Agência") com cor que contraste com a da marca que vende.
- Quantidade ("inúmeras aulas") sem número: parede 3D de capas reais + capas geradas no mesmo estilo, filas duplicadas para correr sem emenda, câmera se afastando e velocidade crescendo.

## Armadilhas que aconteceram
- O dono reclamou de corte seco ("só piscou e mudou"). Nunca entregue cenas em sequência sem transição.
- A voz real saiu cerca de 20 % mais rápida que a estimativa. Sempre ressincronize, nunca estique o áudio.
- `marca.js` carrega antes do `<title>`: o número da cena tem de ser lido na hora do uso, não no topo do arquivo.
- Ao trocar a tela inteira de lugar (`wipe`) entre duas réplicas, confira que a de baixo some depois (senão a passagem fica dupla).

## Na landing page
Player com dois modos: prévia muda em loop com o botão "Assistir com som", que volta ao início e liga o áudio, ou capa parada com play. Carregue o vídeo só quando ele estiver perto da tela e mostre a capa para quem pediu menos movimento. Para escolher o hero, publique 5 variações em rotas separadas (`/v1` a `/v5`) e compare.
