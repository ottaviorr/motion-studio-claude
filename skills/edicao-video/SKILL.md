---
name: edicao-video
description: Editor de vídeo profissional para gravações já feitas (aula, tutorial de tela + câmera, vídeo de YouTube, talking head, live, reunião gravada). Lê o vídeo como roteiro (começo, meio e fim), corta silêncio, gaguejada, frase recomeçada, tomada repetida e trecho que confunde, faz zoom onde a ação acontece, mantém a câmera do apresentador limpa e sincronizada com a voz, intercala motions, trata o áudio e exporta no padrão do dono (1920×1080, 30 fps, bitrate alto). Use SEMPRE que alguém mandar um vídeo gravado e pedir para editar, cortar, limpar, "deixar profissional", tirar silêncios ou erros, melhorar o ritmo, preparar para YouTube/curso, ou mesmo só "dá um tapa nesse vídeo" — mesmo sem dizer "edição". Use também quando a voz e a boca/câmera parecerem fora de sincronia.
---

# Edição de vídeo gravado

O dono grava (tela + câmera, ou só câmera) e quer de volta o vídeo **como um editor profissional entregaria**: que se entende do começo ao fim, sem tempo morto, sem tropeço, com ritmo, zoom onde importa, motion onde ajuda, **voz colada na boca** e qualidade de imagem no máximo que a gravação permite.

Esta skill orquestra. Motions são da skill **motion-design** (gravadas pelo HyperFrames); a montagem final pode ser no **Remotion** (plugins oficiais do Remotion e do HyperFrames instalados: leia `motion-doctrine` e `cut-the-curve` do HyperFrames antes de desenhar transições); a conferência final é da skill **revisao-video**. Scripts em `scripts/` (Python com numpy, opencv-python-headless, pillow, faster-whisper; no Motion Studio: `.ferramentas/.venv/bin/python`, abreviado `PY` abaixo).

## Regras do dono (aprendidas)
- **Padrão de entrega (regra principal, 15/10/2026): 1920×1080 · 30 fps constante · H.264 High · 18 Mb/s · AAC 320 k 48 kHz · -14 LUFS · BT.709.** Motions intercalados também em 1080p30. 4K ou 60 fps só se ele pedir para uma peça. Números em `scripts/padrao.py`; detalhes em `references/imagem.md`.
- **Voz e câmera sincronizadas por construção** (ele notou câmera fora da voz). Bruto normalizado na entrada, cortes na grade de 30 fps, áudio em PCM até o fim; a revisão mede e reprova acima de 40 ms. Ver `references/sincronia.md`.
- **Legenda corrida não é padrão.** Só se ele pedir (VSL, anúncio). Texto dentro dos motions, sim.
- **Nem todo vídeo é de marca.** Vídeo de YouTube qualquer: só editar. Marca e motions só quando fazem sentido.
- **Erro de fala → cortar e ficar com a tomada certa.** Erro sem repetição, com o rosto aparecendo, não tem conserto por corte: deixe e avise.
- **Nada de acelerar 4× no meio da explicação.** Ele reprovou: quebra a frase e não ensina. Trecho calado em que ele só clica é cortado (o resultado aparece logo depois) com fusão curta se a tela mudar.
- **O vídeo tem que fazer sentido sozinho.** Repetição, caminho abandonado ("ou melhor, vou fazer de outro jeito") e explicação dada duas vezes saem. Isso é editar, não só limpar.

## Passo a passo

1. **Receber.** Projeto novo (no Motion Studio: `bash novo-projeto.sh <marca> <nome>`), bruto em `v1/bruto.mp4`. `ffprobe` + 6 quadros espalhados: o que é (tela + câmera? só rosto?), onde está a câmera, faixa preta nas bordas, resolução da captura. **Gravação em partes** (part1, part2…, um vídeo só): `PY scripts/juntar.py part1.mp4 part2.mp4 … -o v1/bruto-30p.mov` junta e normaliza parte por parte (pula o passo 2a). **Câmera que muda de lugar** (bolha do Screen Studio trocando de canto, abertura com a câmera grande): mapeie os lugares e use `cameras` no `edicao.json` (`references/edicao-json.md`).
2. **Normalizar e transcrever — EM PARALELO** (os dois leem o bruto; um usa o codificador, o outro o Whisper):
   - `PY scripts/normalizar.py v1/bruto.mp4` → `v1/bruto-30p.mov` (30 fps constante pelo tempo real de cada quadro, áudio PCM 48 kHz começando junto, cor 8 bits BT.709). Diz se o bruto era de taxa variável. **Todo o resto usa o `bruto-30p.mov`.**
   - `PY scripts/ouvir.py v1/bruto.mp4 --palavras fonte/palavras.json --modelo medium` (tempo por palavra; `medium` acha melhor os tropeços; cache: rodar de novo é instantâneo).
3. **Frases:** `scripts/frases.py fonte/palavras.json > fonte/frases.txt` — a aula em frases numeradas com tempo.
   **E as ilhas:** `PY scripts/ilhas.py v1/bruto-30p.mov > fonte/ilhas.txt` — cada trecho de fala transcrito SOZINHO. A transcrição inteira engole tomada repetida (na aula SLA ficaram 8 tomadas erradas junto com as certas e o dono reclamou); leia as ilhas vizinhas procurando a mesma frase duas vezes. Depois do render, rode de novo no final (`--db -45`) para confirmar que nenhuma sobrou.
4. **Decupagem narrativa** (o passo que separa editor de cortador): leia `references/narrativa.md` e escreva `fonte/narrativa.md` — blocos (abertura, conceito, demonstração, caso, fechamento), o papel de cada um e o que sai (repetição, caminho abandonado, tropeço). Aqui nascem os cortes editoriais e os capítulos.
4b. **Plano de variedade (antes de qualquer motion)** — o dono pediu "sempre variar e ter criatividade", sem perder identidade.
   Leia as últimas 5 linhas do mesmo tipo em `~/motion-studio/aprendizado/repertorio-usado.md` e escreva a lista do proibido
   (janela por eixo: objeto 5 vídeos, assinatura 3, estilo de diagrama 3, abertura 2, fundo base 1, fechamento 1, trilha 5).
   Escreva 3 opções em `fonte/PLANO-EDICAO.md` — A conservadora, B troca ≥ 3 eixos, C provocada (1 carta oblíqua + 1 operador
   SCAMPER) — cada uma com conceito, objeto, fundo base, abertura, assinatura, restrição declarada, estreia e a chance de ser a
   resposta típica. Escolha pela ordem: ensina sem som > cabe no núcleo > distância ≥ 3 eixos > menos típica > custo.
   Monte a tabela tempo a tempo com os recursos do cardápio (`references/variedade.md` §3a) dentro
   do orçamento: ≤ 3 destaques/min, 4–6 motions em 5 min, 1 estreia, nenhum gesto > 50 %, vizinhos diferentes, ≥ 2 de 6 claros,
   nada > 40 s sem mudança visual. Núcleo fixo (não varia): qualidade de entrega, 3 papéis de fonte, um destaque, grito encaixado,
   costura, marca. Depois de entregar: linha no `repertorio-usado.md`.
5. **Atividade da tela e lugar da câmera:** `scripts/atividade.py v1/bruto-30p.mov fonte/atividade.json --camera x,y,w,h` e `scripts/camera_lugar.py fonte/edicao.json` (trechos em que a câmera saiu do lugar → `camera_fora`). Rode ANTES do render: câmera trocada de canto custou um render perdido.
6. **Cortes** no `fonte/edicao.json` (modelo em `references/edicao-json.md`; `"bruto": "../bruto-30p.mov"`): tropeços + editoriais, cada um com motivo. Bordas exatas: `scripts/perfil.py v1/bruto-30p.mov <tempos>` e `references/cortes.md`.
7. **Plano:** `scripts/plano.py fonte/edicao.json` → `edl.json` (bordas na grade de 30 fps, com `q_in`/`q0`/`nq` inteiros), `palavras-final.json`, `cortes.txt`.
8. **Ouvir as emendas antes de renderizar:** `scripts/ouvir_emendas.py fonte/edicao.json --cortes`. Cada emenda tem que soar como uma frase só. Errou? Ajuste a borda e rode de novo.
9. **Zoom:** `scripts/zoom.py fonte/edicao.json` (segue a ação, segura ≥ 4 s, até 1,6×). Ajuste manual com `zoom_fixo`. Ver `references/imagem.md`.
9b. **Mapa de recursos** (pedido do dono, 16/10/2026: "nesse momento um motion, nesse um card, nesse um textinho"). Antes de produzir qualquer motion, escreva `fonte/mapa-recursos.md`: uma linha por frase de `palavras-final.json` (ou por grupo de frases da mesma ideia) com **tempo · frase · função · recurso · por quê**. Funções e recursos em `references/gramatica.md` (matriz função × recurso, 1º/2º/3º, e a escada de intensidade 0–5).
   - Leia a **função** da frase antes de pensar no visual: definição, termo de UI, passo, valor, "esse aqui", estado, enumeração, comparação, aviso, opinião, benefício, exemplo, prova, espera, capítulo, emoção, fechamento, ligação.
   - **Mesma função = mesmo recurso** no vídeo inteiro. A variedade vem das funções mudando.
   - Degrau proporcional ao peso da ideia; **motion em tela cheia ≤ ~1/min**; **chamadas (anotação, texto, card, bolha, tela em cena) ≤ 3/min**; depois de um degrau 4–5, a frase seguinte fica em 0–1.
   - Nenhum recurso que não seja a base em duas frases seguidas (zoom é base).
   - Câmera em destaque (punch-in ou bolha crescendo) só em gancho, opinião, conselho, emoção. Instrução de clique é tela cheia com zoom.
   - Frase de ligação ("então", "tá?", pergunta curta) = **nada**. É o contraste que faz o resto aparecer.
   - Confira as 6 regras com a tabela (ou `scripts/mapa_recursos.py fonte/mapa-recursos.md`, que conta degrau/min, chamadas/min, % de tela encolhida e repetição seguida) e mostre o mapa ao dono **junto com o roteiro de cortes**, antes de gravar os motions. É barato mudar aqui e caro depois do render.
10. **Motions e capítulos** (skill motion-design, com cartão da skill direcao-de-arte e números da hierarquia-visual): 2–5 frases que ficam mais claras desenhadas, marcadores de capítulo (do passo 4) e um fechamento se o vídeo termina "no ar". Tempos tirados de `palavras-final.json`. Grave em **1080p30** (`hf.mjs … --fps 30`). Motion fica POR CIMA: não muda a duração de nenhum trecho (é isso que mantém a câmera na voz).
10a. **Pop-ups, cards e texto de ênfase** (pedido do dono: "nem sempre motion na tela inteira; às vezes um pop-up, uma mensagem por cima da tela"): pop-up/card para o que NÃO está na tela (dica, termo, caminho de menu, o SMS chegando no lead) — `references/popups.md` (14 tipos; entra 0,35–0,45 s, sai 0,2–0,25 s, fica ~4 s, canto oposto à câmera, 1 a cada 20–40 s); texto de ênfase de 1–4 palavras na palavra falada — `references/texto-enfase.md` (sobre a UI clara do CRM: placa de tinta, papel osso com sombra dura ou marca-texto; texto claro com sombra é ilegível). Som de UI 12–18 dB abaixo da voz, só na entrada, ≤ 4/min, nunca em explicação técnica — `references/overlays-kit.md`. Biblioteca de overlays (`remotion/src/overlays/`) ainda em esboço: implementar e testar no próximo vídeo.
10b. **Tela em cena e anotações** (o "After Effects em volta da tela"; pedido do dono, 16/10/2026): onde a tela está CALMA e a fala explica um porquê, a tela encolhe para um cartão (0,75–0,84) e cards/elementos que saltam da tela aparecem em volta — `references/tela-em-cena.md`. Onde a fala aponta um elemento ("esse campo aqui"), anotação puxada pela palavra (holofote, lupa, elemento que levanta, seta + rótulo, passos 1-2-3) — `references/anotacoes.md`. Orçamento: 1 anotação a cada ~15–25 s, um destaque por vez, tela encolhida ≤ ~30 % do tempo de tela, nunca durante o clique que o aluno precisa copiar. Componentes ainda em esboço (TSX nos dois arquivos): implementar e testar no próximo vídeo antes de usar em série.
11. **Fotos antes do render:** `scripts/render.py fonte/edicao.json --quadros 10,48,88 [--cheio]` — zoom legível, câmera limpa (sem borda clara), capítulos no lugar. Para assistir: `--previa` (960×540 no codificador de hardware do Mac, segundos).
11b. **Trilha (vídeo de YouTube):** ver `references/som.md` — **30 dB abaixo da voz na fala** (regra do dono, 16/10/2026; nenhuma janela abaixo de 28 — `scripts/trilha.py --alvo 30`), sobe só no fechamento sem fala (~-22 LUFS). `edicao.json` → `"trilha": "../musica/trilha.wav"` (o Remotion toca por cima da voz).
12. **Render** (os dois esperam a vez na fila global de render) — dois caminhos:
    - **Tudo no Python (mais rápido):** `scripts/render.py fonte/edicao.json` → sai direto no padrão de entrega (fusões simples; `--partes 3` divide em processos paralelos).
    - **Montagem em camadas (transições da doutrina, capítulos nativos, linha do tempo editável no Remotion Studio):** `render.py --camada-tela` (tela + `voz.wav`) → cenas pelo HyperFrames → `scripts/gerar_remotion.py fonte/edicao.json pasta-remotion` → `bash pasta-remotion/renderizar.sh` (Remotion + `finalizar.py` no padrão). Ver `references/montagem-remotion.md`.
13. **Revisão:** skill **revisao-video** (`revisar.py final.mp4 --esperado fonte/palavras-final.json --edl fonte/edl.json --original v1/bruto.mp4`). Mede o padrão de entrega e a **sincronia por emenda** (reprova > 40 ms) junto com a fala e as fotos. Leia a fala final como espectador.
14. **Entregar:** vídeo + `ENTREGA.txt` (o que foi feito, cada corte com motivo — em especial os editoriais, que mudam o conteúdo —, o que não deu para consertar, real × ilustração, dado de cliente que aparece na tela, e a linha da sincronia medida).
14b. **Para o YouTube:** `PY scripts/capitulos.py fonte/edicao.json` → `capitulos-youtube.txt` (00:00 + capítulos, para a descrição) e `legenda.srt` (para ENVIAR ao YouTube; não queimada). 3 quadros candidatos a thumb + 3 títulos que o vídeo cumpre.
15. **Aprender:** Quando o vídeo tiver ≥ 100 views, pedir ao dono o print da aba Retenção e anotar no diário da marca o que acontecia em cada queda/pico. Reação do dono → `~/motion-studio/aprendizado/reacoes.md`; post-mortem (`motion-design/reference/postmortem-modelo.md`) quando ele reage. reação do dono no diário da marca; lição geral em `references/` desta skill; script novo que serviu em `scripts/`.

## Referências (leia quando chegar no passo)
- `references/sincronia.md` — por que a câmera escorrega da voz, como o pipeline evita por construção e como medir (passos 2, 7, 12, 13).
- `references/narrativa.md` — como ler o vídeo como roteiro e decidir o que sai (passo 4).
- `references/cortes.md` — borda exata de corte, noise gate, "exato", fusão (passos 6–8).
- `references/imagem.md` — padrão de entrega, nitidez, zoom, recorte da câmera (passos 9–12).
- `references/edicao-json.md` — todas as chaves do `edicao.json` e do `edl.json`.
- `references/montagem-remotion.md` — montagem final no Remotion com cenas do HyperFrames, as regras de transição e o render rápido.
- `references/armadilhas.md` — o que já deu errado.
- `references/tela-em-cena.md` — tela encolhida com motion em volta: 10 variações com números, componente `TelaEmCena` (esboço), regras (estudo out/2026).
- `references/anotacoes.md` — holofote, lupa, elemento que levanta, seta, passos; princípios de Mayer; `vista.json`/`anotar.py` (propostas).
- `references/gramatica.md` — função da frase × recurso (21 funções, escada de intensidade 0–5, logs de 5 tutoriais grandes, plano da aula SLA).
- `references/variedade.md` — cardápio de 35 recursos, janela de não repetir, 3 opções (A/B/C), cartas oblíquas, orçamento por minuto.
- `references/popups.md` · `references/texto-enfase.md` · `references/overlays-kit.md` — pop-ups/cards, texto de ênfase (contraste testado no CRM), som de UI e biblioteca de overlays.
- `references/som.md` — trilha 25 dB abaixo da voz, ducking, efeitos.
- `references/oficio-youtube.md` — gancho, ritmo, retenção, capítulos, com números e fontes (estudo out/2026).
