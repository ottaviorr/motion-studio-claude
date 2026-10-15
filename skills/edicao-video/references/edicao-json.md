# fonte/edicao.json (modelo comentado)

```json
{
  "bruto": "../bruto.mp4",
  "palavras": "palavras.json",
  "atividade": "atividade.json",
  "saida": "../aula-editada-4k.mp4",

  "camera": [55, 754, 491, 276],      // x, y, largura, altura EXATOS da câmera no bruto (px)
  "camera_recuo": 2, "camera_raio": 20,
  "borda": 10,                        // px de faixa preta nas laterais da gravação (0 se não houver)

  "escala": 1, "fps": 30, "crf": 14, "nitidez": 0.35,   // padrão do dono: 1080p30 (escala 2 = 4K, fps 60 só se pedirem)

  "cortes": [
    [31.32, 37.27, "frase recomeçada"],
    [191.00, 193.33, "repetição", "exato"],
    [196.10, 207.87, "EDITORIAL: caminho abandonado", "exato"]
  ],
  "silencio": {"db": -40, "min": 0.6, "antes": 0.2, "depois": 0.15},
  "acelerar": {"ativo": false},       // true só se o dono pedir (selo ▶▶ N×)
  "fusao": 0.25,

  "zoom": {"max": 1.6},
  "zoom_fixo": [],

  "motions": [ {"arquivo": "motions/01-abertura-4k.mp4", "ini": 0.0, "fade": 0.4},
               {"arquivo": "motions/05-fechamento-4k.mp4", "ini": 167.76, "fade": 0.4, "sem_camera": true} ],
  "camadas": [ {"arquivo": "motions/c1-exemplo.mov", "ini": 28.17} ],
  "camera_fora": [[192.2, 202.6]]     // s do BRUTO em que a câmera saiu do lugar (cena do OBS trocada)
}
```
- `motions`: tela cheia; a câmera vem por cima, a menos que `sem_camera`. A que começa em 0 entra sem fusão (gancho no quadro 0). Uma que começa no fim da fala estende o vídeo (o áudio ganha silêncio).
- `camadas`: `.mov` ProRes 4444 com alfa por cima de tudo (capítulos, selos).
- Tempos de `motions`/`camadas` são do vídeo **editado**: tire de `palavras-final.json` (campo `t`; `src` é o tempo no bruto). Mudou um corte antes delas → recalcule.
