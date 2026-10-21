# Modelo de ENTREGA.md

Fica ao lado da pasta de finais. Escrito para o dono, que vai ler no VS Code **sem som**: o som precisa estar descrito em texto. Baseado no `ENTREGA.md` dos 15 reels do cliente A (aprovado).

```markdown
# {Marca} · {N} {tipo de peça} (entrega de {DD/MM/AAAA})

Pasta: `{pasta-de-finais}/{tipo}-01.mp4` … `{tipo}-NN.mp4` · {W}×{H} · {fps} fps · H.264 **{bitrate} constante** · áudio AAC 256k a **{LUFS} LUFS** ({por quê: padrão do Instagram / YouTube}).
Versão: v{n} ({o que mudou desde a anterior, ou "primeira entrega"}). Versões antigas em `versoes/`.
Marca: {regras que valeram: nome, o que nunca aparece}. Telas: **{reais | réplicas com dados inventados}** ({exemplos de nomes inventados}). Números dentro das telas são exemplo, não resultado prometido.

## O que tem em cada um (e como soa)

| # | Duração | Estilo | Isca | Som |
|---|---|---|---|---|
| 01 | 22 s | {direção de arte em poucas palavras} | {CTA} | {voz: quem/ritmo} + {música: gênero, BPM, onde cresce}; {efeitos: onde}; música ~21 dB abaixo da voz |

## Revisão feita em todos
- Fala transcrita de novo no arquivo final: {resultado}.
- Volume {LUFS} LUFS, pico ≤ -1 dBFS; voz − música medido: {faixa} dB.
- Bitrate medido: {faixa} Mb/s (pedido: {bitrate}).
- {N} quadros de cada um conferidos: legibilidade/hierarquia, zona segura, fontes, regras da marca.
- Revisor independente: {N aprovados de primeira, N corrigidos (o quê)}.

## Real × ilustração
- {o que é tela real, o que é réplica, o que é ilustração}

## O que não deu / ficou de fora
- {item e por quê — ou "nada"}

## Para postar
- {passos práticos: link na bio, automação de comentário, capa, legenda do post}

## Onde mexer, se quiser ajustar
- Cenas: `base/rNN-*.html` (estilo em `base/rNN-estilo.css`). Gravar de novo: `node ~/.claude/skills/motion-design/kit/hf.mjs ../cenas/<cena>.mp4 --html <cena>.html --crf 12` (dentro de `base/`).
- Montagem: `reels/NN.json` → `python ~/.claude/skills/motion-design/kit/gerar_reel.py <projeto> --render NN`.
- Linha do tempo: `cd remotion && npm run dev`.

Músicas/licenças: {origem e licença, ex.: Mixkit, `musica/LICENCAS.md`}.
```

Na mensagem ao dono (curta): onde estão, quantos, o que mudou desde o piloto, o que não deu, e uma pergunta fechada ("aprova assim ou quer ajuste em algum? diga o número e o quê").
