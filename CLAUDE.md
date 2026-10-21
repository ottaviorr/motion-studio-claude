# Motion Studio

Estúdio de motion design e edição de vídeo para qualquer marca, ou sem marca (vídeo de YouTube). Oito skills especialistas:
- **orquestrador-video** — diretor de produção para pedidos com mais de uma peça ou etapa (séries, campanhas, VSL + criativos). Conduz os portões de aprovação do dono (roteiro → direção de arte → piloto → entrega), os agentes em paralelo com contrato e a revisão independente. Atalho: `skill-orquestrador/`.
- **direcao-de-arte** — conceito visual antes de produzir (cartão de direção, 27 estilos, unidade × variedade numa série) e crítica de arte depois. Atalho: `skill-arte/`.
- **hierarquia-visual** — regras em números (tamanho, contraste, cor, zona segura, tempo de leitura) mais o `conferir_hierarquia.mjs`, que mede a cena. Atalho: `skill-hierarquia/`.
- **motion-design** — cenas animadas em HTML (cada quadro é uma função do tempo), gravadas pelo Chrome ou pelo HyperFrames: anúncios, VSLs, explicadores, motions por cima de gravação, vídeos na batida da música. Atalho: `skill/`.
- **edicao-video** — editar uma gravação: leitura narrativa (começo, meio e fim), cortes de erro e de repetição, zoom na ação, câmera limpa, capítulos, pop-ups e texto de ênfase, entrega em 1080p30 com bitrate alto. Chama a motion-design para os motions. Atalho: `skill-edicao/`.
- **revisao-video** — revisar qualquer vídeo pronto antes de entregar (transcreve o final, mede volume e qualidade, fotografa as emendas). Atalho: `skill-revisao/`.
- **editorial-film-edit** — edição em estilo editorial de arquivo (grão, bloom, P&B, texto cinético, máscaras, tela dividida). Os módulos de referência ficam em `skills/editorial-film-edit/implementation/`.
- **paper-collage-film** — filme de colagem de papel rasgado de 5 a 30 s (intro, trailer, promo). Alguns scripts (extract, encode, mux, greenkey) são em Swift e só rodam no macOS; no Windows, use o ffmpeg no lugar deles.

Instalação: `bash instalar.sh` (liga as skills em `~/.claude/skills` e instala as ferramentas em `.ferramentas/`).

## Antes de qualquer vídeo
1. **Carregue a skill do pedido** e siga o SKILL.md dela:
   - mais de uma peça → orquestrador-video;
   - uma cena ou um vídeo → direcao-de-arte (conceito) + motion-design (cenas) + hierarquia-visual (números);
   - gravação para editar → edicao-video.

   Antes de entregar, rode a revisao-video.
2. **Leia o nível atual:** `skill/reference/nivel.md`, as últimas linhas de `skill/reference/historico.md` e o `evolucao.md` da marca em `marcas/<marca>/`. **Cada vídeo tem que superar o anterior.**
3. **Marca nova sem pasta:** pergunte cores, fontes, logo e regras de texto (preços oficiais, o que não pode prometer). Depois crie `marcas/<marca>/` a partir de `marcas/exemplo/`, com:
   - `marca.css`;
   - `marca.js`, com `MARCA.regras`;
   - o logo;
   - `evolucao.md`.

## Estrutura
- `marcas/<marca>/` — pacote da marca: `marca.css`, `marca.js` (com `MARCA.regras`), logos, imagens próprias e o `evolucao.md` (diário: o que já foi feito, regras fixas, reação do dono).
- `projetos/AAAA-MM-marca-nome/` — um projeto por entrega. Crie com `bash novo-projeto.sh <marca> <nome>`. Dentro ficam:
  - `base/`, com o kit e a marca copiados;
  - uma pasta por vídeo, com `fonte/` (cenas .html, roteiro, palavras.json);
  - os .mp4 finais.
- `entrada/` — onde o dono solta áudios (ElevenLabs), gravações, prints e logos. Mova para o projeto certo ao começar e deixe a pasta limpa.
- `.ferramentas/` — Node (playwright-core, puppeteer-core, HyperFrames 0.8.140, matter-js), Python (faster-whisper, numpy, opencv, librosa, mediapipe, pillow) e `modelos/` (recorte de sujeito), instalados pelo `instalar.sh`:
  - **transcrever:** `.ferramentas/.venv/bin/python skill/scripts/transcrever.py voz.mp3 fonte/palavras.json --roteiro fonte/roteiro.txt --modelo small`
  - **scripts de Node que precisam de pacote:** `NODE_PATH=$PWD/.ferramentas/node_modules node ...`
  - **gravar cenas mais rápido:** `node skill/kit/hf.mjs saida.mp4 --html cena.html` (1080p30 por padrão) ou `MOTOR=hf bash fonte/gravar-todos.sh` (ver `skill/reference/motores.md`)
  - **música (BPM, grade de batidas, drops):** `.ferramentas/.venv/bin/python skill/kit/batidas.py faixa.mp3`

## Regras do estúdio
- Dados reais de clientes (nomes, conversas, prints de conta) nunca aparecem no vídeo. Use réplica com dados inventados e diga no guia o que é real e o que é ilustração.
- Prints originais com dados de clientes ficam fora do git (`.gitignore` já ignora `print_*`).
- Vídeos, áudios e .mov ficam só na máquina; o git guarda as fontes (cenas, roteiros, marcas).
- Commits pequenos, um por assunto.
- Legenda corrida só quando o dono pedir (VSL/anúncio).
- **Padrão de entrega: vídeo editado sai em 1920×1080, 30 fps, bitrate alto (~16–20 Mb/s), AAC 320 k, -14 LUFS.** Motions que entram no vídeo editado também em 1080p30. Voz e câmera sincronizadas por construção (a revisão mede e reprova acima de 40 ms).
- Antes de entregar: nota pela rubrica (`skills/direcao-de-arte/references/rubrica.md`), comparando com o vídeo anterior do mesmo tipo. Quando o dono reagir: linha em `aprendizado/reacoes.md` (com as palavras dele e a regra que gerou) e `POSTMORTEM.md` no projeto (modelo em `skill/reference/postmortem-modelo.md`).
- Música só com licença de uso (ex.: Mixkit, com a licença anotada em `musica/LICENCAS.md` do projeto).
- Depois de entregar:
  - acrescente uma linha no `evolucao.md` da marca;
  - rode o ciclo de aprendizado da skill usada: histórico, nível/armadilhas/referências, kit/scripts e commit.
- **Repositórios separados:**
  - o seu estúdio de trabalho (com marcas, projetos e histórico) fica num repositório **privado**;
  - esta versão é só o sistema.
