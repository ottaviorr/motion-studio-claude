---
name: motion-design
description: Use quando pedirem vídeo, motion, motion design, animação, B-roll, Reels, Stories, anúncio em vídeo, explicador animado, cenas para pôr por cima de uma gravação (talking head) ou vídeo mostrando a tela de um produto — em qualquer projeto ou marca.
---

# Motion design (qualquer marca)

Cenas feitas em HTML onde **cada quadro é uma função do tempo** (`frame(t)`), gravadas quadro a quadro pelo Chrome (HyperFrames). Sai MP4 (fundo próprio) ou MOV com transparência (para pôr por cima de outro vídeo). `$K` = esta pasta.

**Padrão de entrega (regra do dono): 1920×1080 (ou 1080×1920) a 30 fps, taxa de bits alta.** É o que o `hf.mjs` e o `gravar-todos.sh` fazem sem nenhuma opção (H.264 a 40 Mb/s). Motion para vídeo editado também sai em 1080p30. 60 fps ou 4K (`FPS=60 ESCALA=2`) só em peça avulsa de portfólio ou anúncio, se o pedido disser.

**Antes de começar:** se a peça ainda não tem conceito visual, rode a skill **direcao-de-arte** (cartão de direção: conceito, paleta com um destaque, 3 fontes, o que NÃO fazer) — e, se for mais de uma peça, quem conduz é a **orquestrador-video**. Monte a hierarquia pela tabela da skill **hierarquia-visual** e confira cada cena com `node ~/.claude/skills/hierarquia-visual/scripts/conferir_hierarquia.mjs cena.html` antes de gravar (réplica feita à mão leva `data-hv="ui"`). Depois: leia `reference/nivel.md` (acabamento mínimo), `reference/inspiracao.md` (o que os melhores vídeos feitos com IA têm em comum), as últimas linhas de `reference/historico.md` (o nível atual: cada vídeo tem que superar o último) e o diário do projeto `motion/evolucao.md` (se não existir, crie a partir de `reference/evolucao-modelo.md`; alguns projetos têm um pacote de marca próprio que já traz o diário). **Depois de entregar:** acrescente uma linha no diário do projeto. Lição que vale para qualquer projeto: acrescente também em `reference/nivel.md` ou `reference/armadilhas.md` desta skill (se esta pasta não puder ser editada, registre no diário do projeto). Cada vídeo tem que superar o anterior.

Exemplos: a skill vem sem vídeos prontos. Os seus vão sendo salvos em `examples/` a cada vídeo que subir o nível (passo 5 do ciclo de aprendizado) e passam a ser a referência das próximas peças. Tipografia que funcionou: `reference/tipografia-que-funciona.md`.

## Qual modo

| Pedido | Modo |
|---|---|
| "Faz os motions do meu vídeo" (ele grava falando e edita) | **A — cenas sincronizadas com a gravação** (o mais usado) |
| Uma cena só para uma frase, sem a gravação em mãos | **A** com tempos estimados (≈ 0,35 s por palavra, ou os que ele disser) — avise que os tempos são estimados |
| Anúncio/vídeo curto sem narração, uma peça só | **B — vídeo inteiro em `frame(t)`**: uma página longa com `cena(DUR, …)`, mesmo kit |
| Explicador narrado (voz sintética ou do dono) com legendas | **C — motor narrado**: `reference/narrado.md` |
| VSL mostrando o sistema/app em uso, voz feita depois (ElevenLabs) | **B + roteiro + ressincronia com a voz**: `reference/vsl-produto.md` |
| "Edita esse vídeo" (gravação de aula/YouTube: cortar, ritmo, zoom, revisar) | **Outra skill: `edicao-video`** (ela chama esta para os motions). Motion para vídeo editado: tempos de `palavras-final.json`, gravar em 1080p30 (padrão) |
| Motion sem voz, na batida (portfólio, abertura, lançamento) | **B na batida**: `kit/batidas.py --trecho` → cena em batidas (`kit/ritmo.js`) → desfoque real (`kit/desfoque.sh`) se for rápido → som desenhado (`kit/som.py`) |
| VSL com a voz já pronta (o dono manda o MP3) | **B direto na voz**: transcrever → `kit/gerar-plano.py` → cenas com `W('palavra')` → `kit/montar-final.py` (vídeo + .srt) |

## Montar a pasta (A e B)

```
<projeto>/video N/fonte/   comum.js comum.css gravar-todos.sh fotos.sh grade.sh   ← de $K/kit/ (+ ritmo.js pelicula.js objeto3d.js shader.js som.py quando a peça usar)
                           marca.css marca.js                                     ← de $K/kit/marca-exemplo/, com a marca do projeto
                           gerar-plano.py montar-final.py                         ← de $K/kit/ (quando há voz: plano, transições e legenda .srt)
                           NN-nome.html (de $K/kit/modelo-cena.html)  telas/ (fotos reais)  palavras.json
<projeto>/video N/         NN-nome.mp4|.mov  ONDE-COLOCAR.txt
```
Sem marca definida: pergunte cores, fontes, logo e regras de texto (preços, nomes proibidos) — ou tire do site/projeto. Sem logo: desenhe um selo simples e avise no guia.
Fontes: as cenas podem usar `<link>` do Google Fonts — o `hf.mjs` troca por fontes locais embutidas (cache em `~/.cache/motion-studio-fontes`, `kit/fontes-locais.mjs`), então só a primeira vez precisa de internet. Troque no `<link>` da cena e no `marca.css`. Trio que funcionou: Archivo (wdth 62–125) + Instrument Serif itálica + JetBrains Mono. `engine/` e `engine/fonts` são só do modo C.

## Modo A, passo a passo

1. **Transcrever** a gravação com tempo por palavra (local): `bash $K/scripts/setup.sh ./motion` (uma vez) e `./motion/.venv/bin/python $K/scripts/transcrever.py video.mp4 "video N/fonte/palavras.json" --modelo small`. Listar `palavra@tempo` e corrigir nomes que o Whisper erra.
2. **Plano por frase:** início = 1ª palavra − 0,1 s; duração até o fim da frase; batidas = palavra-chave − início. Pule trechos que o dono mandou cortar; com tomadas repetidas, escolha uma e avise.
3. **Formato por cena:** deitado (padrão) · em pé tela cheia (`class="v"`: revelação, impacto, oferta) · transparente (`class="alfa"`: por cima do rosto, conteúdo na lateral livre).
4. **Escrever as cenas** a partir de `kit/modelo-cena.html` (ferramentas de `kit/comum.js` listadas no topo do arquivo: `pop`, `mesh`, `mix`, `wipe`, `TELA`, `CEL`, `seq`, `cam`, `spot`, `cursor`, `LOGO`, `dinheiro`, `ic`). Telas reais: `reference/telas-reais.md`.
5. **Conferir antes de gravar:** `conferir_hierarquia.mjs` (skill hierarquia-visual) + `FOTOS_DIR=<pasta de rascunho> bash fonte/fotos.sh NN-x.html 1.2 3.4` (com `ROSTO=quadro.jpg` para os transparentes) e `bash fonte/grade.sh folha.jpg <pasta>/*.jpg`. Olhe todas as fotos. Sem `FOTOS_DIR`, cada chamada cria uma pasta nova no temporário do sistema (apague no fim).
6. **Gravar:** `bash "video N/fonte/gravar-todos.sh"` — HyperFrames, 1080p30 a 40 Mb/s (o padrão). Para o dono olhar antes: `PREVIA=1` (rascunho rápido, nunca entregue). Movimento muito rápido: `bash $K/kit/desfoque.sh NN-x.html ../NN-x.mp4` (desfoque real, 2 passadas). Alfa em 4K: `MOTOR=cdp ESCALA=2 PRORES=1`. Fundo pesado (shader) em várias cenas: grave o fundo uma vez e junte com `kit/compor_fundo.py`. Ver `reference/motores.md`.
7. **Conferir os finais:** um quadro de cada arquivo (~75 % da duração) + duração e tamanho (`ffprobe`).
8. **Entregar:** `ONDE-COLOCAR.txt` (nº, arquivo, formato, início na gravação, duração, frase; o que é real × ilustração) e atualizar o diário.

## Ciclo de aprendizado (obrigatório depois de cada entrega)

A skill aprende com cada vídeo. Ao entregar, sem o dono precisar pedir:
1. **Diário do projeto** (`motion/evolucao.md`): uma linha com o que entrou de novo e a reação do dono (atualize quando ele responder).
2. **Histórico da skill** (`reference/historico.md`): uma linha (data, projeto, vídeo, o que trouxe de novo, reação).
3. **Lições gerais**: regra de acabamento em `reference/nivel.md`; erro que aconteceu em `reference/armadilhas.md`; método novo no `reference/` do modo (ex.: `vsl-produto.md`).
4. **Ferramenta nova que serve para outros projetos** (função, script, réplica de app) vai para `kit/` em versão sem marca.
5. **Vídeo que subiu o nível** (técnica nova ou o dono elogiou muito): salve um exemplo enxuto em `examples/<nome>/` com `LEIA-ME.md` (o que cada arquivo ensina). Sem dados de cliente, sem prints reais, sem mídia pesada (vídeos, áudios e capas do cliente ficam fora).
6. **Salvar a skill no git**: `git -C ~/.claude/skills/motion-design add -A && git -C ~/.claude/skills/motion-design commit -m "aprendizado: <vídeo> (<projeto>)"` e, se a skill tiver remoto, `push` para o seu repositório **privado** (ela guarda histórico e exemplos dos seus clientes). Uma versão aberta, se existir, só recebe conhecimento sem dados de cliente e só quando o dono pedir.

## Antes de entregar
Rode a skill **revisao-video** no arquivo final (transcrição de novo, volume, fotos, qualidade medida).

## Erros comuns
Ver `reference/armadilhas.md` (IDs que colidem, nomes reservados da base, Chrome em paralelo, alfa do HEVC, zsh, apps que precisam de espera, duplo sentido).
