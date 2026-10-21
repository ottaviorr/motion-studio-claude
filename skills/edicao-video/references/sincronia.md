# Sincronia voz × câmera

O dono notou "câmera desincronizada com a voz" em vídeos editados com motion por cima. A câmera é recortada da MESMA gravação (tela + câmera) e colada por cima; a voz vem da mesma gravação. Se as duas saem do mesmo instante do bruto, não tem como desencontrar — o desencontro vem do caminho. Aqui está cada causa, medida, e o que o pipeline faz para que a sincronia seja exata **por construção**.

## Como medir (sempre, na revisão)
`revisao-video/scripts/sincronia.py final.mp4 --original bruto.mp4 --edl fonte/edl.json` (o `revisar.py` já roda e reprova acima de **±40 ms**).
- **Por emenda:** em cada trecho do edl, janelas de até 4 s. Som: correlação cruzada da voz do final com a do bruto (busca ±0,3 s; mais que isso acha a mesma frase repetida que foi cortada). Imagem: a diferença entre quadros seguidos da região da câmera do final comparada com a do bruto, deslocando de 1 em 1 ms, usando o tempo real (pts) de cada quadro (busca ±1 s). **Atraso = δsom − δimagem** (+ = boca depois da voz).
- **Lábio × voz:** movimento das células da câmera que mais acompanham a voz × envelope da voz. Na aula do cliente B (rosto pequeno, pouco movimento de boca) deu correlação baixa e fica "inconclusivo": é só conferência grosseira. Vale a medida por emenda.
- Precisão: a webcam grava a 30 fps dentro de uma gravação de 60 (quadros repetidos aos pares), então ±1 quadro da webcam é o limite físico de qualquer medida; o resultado de um pipeline certo é ~0 ms.

## Causas encontradas e medidas (aula do cliente B, 37 emendas)
| Causa | Onde | Medido antes | Depois |
|---|---|---|---|
| **Gravação de taxa variável** (OBS perdendo quadro, gravação de tela, iPhone). O render escolhia o quadro do bruto por `int(s × fps)`, como se quadro fosse tempo. O ffmpeg tapa parte dos buracos repetindo quadro, mas não onde devia | `render.py` | teste com 27 quadros perdidos (1 a cada 10 s, como OBS sobrecarregado): pior **+53 ms**, média +19,6 ms → reprovado | `normalizar.py`: **-1,0 ms** pior, -0,1 média |
| **Vídeo e áudio arredondados cada um para um lado** — Remotion: `from = round(ini·60)` e `trimBefore = round(in·60)` independentes; `durationInFrames = round(dur·60)` deixava 1 quadro sem câmera entre trechos | `gerar_remotion.py` (v3) | v3 entregue: pior **-14 ms**, emendas variando de -14 a +2 ms; buraco de 1 quadro (ex.: trecho 6→7) | inteiros do edl: **-1,0 ms**, trechos encostam |
| **Quadro escolhido com `floor` + erro de vírgula flutuante** (`int(s·fps + 1e-6)`), escolhendo o quadro anterior | `render.py` (v1, v2) | v1 pior **+15,5 ms** (média +7,6); v2 pior **+13,1 ms** (média +6,1) | **-1,0 ms** |
| **AAC: atraso inicial (priming) a cada codificação** | voz.m4a → Remotion → AAC de novo | medido **0,0–0,1 ms** em todas as versões: ffmpeg grava a lista de edição e os players respeitam. Não era causa | áudio em PCM (wav) até a única codificação AAC, no fim |
| **Concat de pedaços com `-c copy`** (`render.py --partes` de um colaborador) | concat demuxer de mp4 | **+33 ms** constante (1 quadro) | retirado: sem ganho de tempo no Mac (o x264 já usa todos os núcleos) |
| **Motion de 60 fps numa saída de 30** lido quadro a quadro | `render.py` | o motion andaria na metade da velocidade e a fala dele perderia o tempo | `fps=30` no filtro de leitura |
| `-ss` antes do `-i` em keyframe, `-async/-vsync` ausentes | — | não usados no caminho da edição; o `normalizar.py` usa `fps` pelo tempo + `aresample=async=1:first_pts=0` | — |
| Motion por cima mudando a duração dos trechos | — | não acontece: motion é camada por cima; os trechos da tela/câmera/voz continuam com os mesmos quadros | regra no SKILL.md |
| Trecho acelerado | `gerar_remotion.py` | a câmera andava a 1× enquanto a tela ia a N× | `playbackRate` = velocidade do trecho |

## A construção (o que garante ≤ 1 ms)
1. **`normalizar.py` na entrada:** `fps=30:start_time=0` escolhe, para cada instante k/30 s, o quadro que estava na tela naquele instante (pelo pts, não pela contagem); áudio `aresample=48000:async=1:first_pts=0` (buraco vira silêncio no lugar certo), PCM 24 bits, começando junto com o vídeo. O `render.py` recusa bruto fora do ritmo.
2. **`plano.py` na grade:** toda borda de corte vai para o quadro de 30 fps mais próximo (≤ 16,7 ms de diferença na borda, imperceptível: a borda já é escolhida no silêncio). Cada trecho tem `q_in`, `q0`, `nq` inteiros.
3. **Mesmos instantes para imagem e som:** o quadro k do editado é o quadro `q_in + (k − q0)` do bruto; o áudio é cortado com `atrim=start_sample/end_sample` (1 quadro = 1600 amostras a 48 kHz, inteiro). Nada é arredondado duas vezes.
4. **Áudio em PCM até o fim:** `render.py` grava `voz.wav`; o Remotion recebe wav e devolve PCM (`--audio-codec=pcm-16`); só o `finalizar.py` (ou a junção final do `render.py`) codifica AAC, uma vez.
5. **Remotion com os inteiros do edl:** `from = q0`, `durationInFrames = nq`, `trimBefore = q_in` na `camera.mp4` (recortada do bruto normalizado, mesmo ritmo).
6. **Revisão mede** e reprova > 40 ms.

## Tempos da edição (aula do cliente B, bruto 4min25 → 2min53, Mac M4)
| Etapa | Antes (4K60, scripts antigos) | Depois (1080p30) |
|---|---|---|
| Normalizar bruto | — | 38 s (em paralelo com a transcrição) |
| Transcrição do bruto | 216 s (medium) | 80 s (large-v3-turbo em lotes) |
| Atividade + plano + zoom | 14 s (+ atividade não medida) | 21 s |
| Ouvir emendas | 160 s | 75 s |
| Render no Python (com motions) | **1179 s** | **179 s** |
| Revisão (agora com sincronia) | 219 s | 73 s |
| **Total** | **~1790 s (30 min)** | **~430 s (7 min)** |
| Montagem no Remotion (camadas) + finalização | v3 4K60 não cronometrada | camada de tela 123 s + Remotion 219 s + finalizar 84 s |
