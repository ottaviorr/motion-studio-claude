# motion-design · skill do Claude Code

Motion design feito em HTML, onde cada quadro é uma função do tempo (`frame(t)`), gravado quadro a quadro pelo Chrome com desfoque de movimento. Sai MP4 com fundo ou MOV com transparência.

Serve para motions por cima de vídeo gravado (talking head), anúncios curtos, explicadores narrados e VSLs mostrando um app em uso, com a voz feita depois no ElevenLabs.

## Instalar

```bash
git clone https://github.com/<seu-usuario>/<este-repositorio> ~/.claude/skills/motion-design
```

Depois, no Claude Code, peça um vídeo ("faz os motions do meu vídeo", "uma VSL mostrando meu sistema") ou rode `/motion-design`.

## Precisa ter no computador

- Google Chrome
- Node.js 18 ou mais novo
- ffmpeg (`brew install ffmpeg`)
- Python 3 (só para transcrever voz: `bash scripts/setup.sh ./motion` instala o faster-whisper localmente)

## Por onde começar

- `SKILL.md`: o que a skill faz e qual modo usar.
- `reference/nivel.md`: o acabamento mínimo de cada vídeo.
- `reference/vsl-produto.md`: o método da VSL de produto (roteiro, réplica do app, ressincronia com a voz, transições).
- `examples/`: começa vazia; cada vídeo que subir o nível vira um exemplo enxuto aqui (ciclo de aprendizado).
- `reference/historico.md`: todos os vídeos feitos com a skill e o que cada um trouxe. A skill se atualiza e faz commit a cada vídeo entregue ("Ciclo de aprendizado" no `SKILL.md`).

O motor narrado (`engine/`) é derivado do motion-broll de Bart, sob licença MIT (`LICENSE-motion-broll.txt`).
