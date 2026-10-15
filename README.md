# Motion Studio

Um estúdio de motion design e edição de vídeo que roda dentro do **Claude Code**. Você pede o vídeo em português. O Claude conduz briefing, roteiro, direção de arte, cenas, gravação, montagem e revisão, e aprende a cada entrega.

Cada cena é uma página HTML em que **cada quadro é uma função do tempo** (`frame(t)`). O Chrome ou o [HyperFrames](https://github.com/heygen-com/hyperframes) grava quadro a quadro até 4K60, e o [Remotion](https://www.remotion.dev) monta o vídeo final com transições, música e efeitos.

## O que vem aqui

| Skill | O que faz |
|---|---|
| `orquestrador-video` | Diretor de produção: portões de aprovação, agentes em paralelo com contrato, revisão independente, entrega |
| `direcao-de-arte` | Conceito visual antes de produzir (cartão de direção, 27 estilos, séries sem repetição) e crítica depois |
| `hierarquia-visual` | Tamanho de letra, contraste, cor, zona segura e tempo de leitura em números, mais um conferidor automático de cenas |
| `motion-design` | Cenas em HTML (anúncio, VSL, explicador, motion por cima de gravação, vídeo na batida da música), kit de animação, gravadores, montagem |
| `edicao-video` | Edita gravações: narrativa, cortes de erro, zoom na ação, câmera limpa, capítulos, 4K |
| `revisao-video` | Revisa o vídeo final sem assistir: transcreve de novo, mede volume e qualidade, fotografa as emendas |
| `editorial-film-edit` | Edição em estilo editorial de arquivo: texto cinético, grão de filme, bloom, máscaras e tela dividida com o apresentador (em inglês; os módulos de navegador vêm em `implementation/`) |
| `paper-collage-film` | Filme de colagem de papel rasgado, de 5 a 30 s (intro, trailer, promo 16:9), em stop-motion feito em código, com motor em canvas, trilha sintetizada e exemplos (em inglês; alguns scripts usam Swift e só rodam no macOS) |

Também vêm:
- `novo-projeto.sh`, que cria um projeto;
- `marcas/exemplo/`, um pacote de marca neutro para copiar;
- o `CLAUDE.md` com as regras do estúdio.

**Não vêm:** vídeos ou exemplos prontos, áudios, marcas reais, projetos, histórico de clientes. Você parte das skills e cria os seus. A pasta `skills/motion-design/reference/historico.md` começa vazia e vai sendo preenchida pelos seus vídeos.

## Instalar (macOS)

Precisa de Google Chrome, Node.js 18+, ffmpeg e Python 3 (`brew install node ffmpeg python`).

```bash
git clone <url-deste-repositório> ~/motion-studio
cd ~/motion-studio && bash instalar.sh
```

O `instalar.sh` faz três coisas:
- liga as 8 skills em `~/.claude/skills`, por link simbólico, para que o que elas aprendem fique neste repositório;
- cria os atalhos `skill/`, `skill-edicao/` etc.;
- instala as ferramentas em `.ferramentas/` (HyperFrames 0.8.140, playwright-core, faster-whisper, opencv).

Plugins opcionais do Claude Code, que a montagem e as transições usam como referência:

```bash
claude plugin marketplace add remotion-dev/claude-code-plugin
claude plugin marketplace add heygen-com/hyperframes
```

## Usar

Abra a pasta no Claude Code (`cd ~/motion-studio && claude`) e peça, por exemplo:
- "faz um motion de 30 s apresentando minha marca, na batida da música";
- "faz 10 reels sobre o meu produto, cada um com uma cara";
- "edita essa gravação da aula e deixa em 4K";
- "revisa esse vídeo antes de eu postar".

Marca nova: o Claude pergunta cores, fontes, logo e regras de texto e cria `marcas/<marca>/` a partir de `marcas/exemplo/`.

## Como ele aprende
Depois de cada entrega, a skill usada registra:
- o vídeo em `reference/historico.md`;
- as regras novas de acabamento em `reference/nivel.md`;
- os erros em `reference/armadilhas.md`;
- as ferramentas novas em `kit/`.

Depois ela faz commit. Guarde o seu estúdio de trabalho num repositório **privado**, porque o histórico e os exemplos passam a ter dados das suas marcas.

## Licenças
O motor narrado (`skills/motion-design/engine/`) é derivado do motion-broll de Bart, sob licença MIT (`skills/motion-design/LICENSE-motion-broll.txt`). Fontes em `skills/motion-design/engine/fonts` sob as licenças de origem (Google Fonts). HyperFrames (Apache-2.0) e Remotion (licença própria: grátis para pessoa física e empresas de até 3 pessoas) são instalados à parte.
