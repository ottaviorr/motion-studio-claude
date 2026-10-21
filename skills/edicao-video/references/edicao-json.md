# fonte/edicao.json (modelo comentado)

```json
{
  "bruto": "../bruto-30p.mov",        // o NORMALIZADO (scripts/normalizar.py ../bruto.mp4), nunca o original
  "palavras": "palavras.json",
  "atividade": "atividade.json",
  "saida": "../aula-editada.mp4",

  "camera": [55, 754, 491, 276],      // x, y, largura, altura EXATOS da câmera no bruto (px)
  "camera_recuo": 2, "camera_raio": 20,
  "borda": 10,                        // px de faixa preta nas laterais da gravação (0 se não houver)

  "fps": 30, "nitidez": 0.35,         // padrão de entrega: 1080p30 18 Mb/s (scripts/padrao.py). "escala": 2 = 4K, só se o dono pedir

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

  "motions": [ {"arquivo": "motions/01-abertura.mp4", "ini": 0.0, "fade": 0.4},
               {"arquivo": "motions/05-fechamento.mp4", "ini": 167.76, "fade": 0.4, "sem_camera": true} ],
  "camadas": [ {"arquivo": "motions/c1-exemplo.mov", "ini": 28.17} ],
  "camera_fora": [[192.2, 202.6]],    // s do BRUTO em que a câmera saiu do lugar (camera_lugar.py acha)
  // câmera que MUDA de lugar (s do bruto); 7º campo opcional só para a montagem no Remotion:
  //   destino = onde ela aparece na saída (abertura com a câmera grande ao lado do texto), punch = zoom 1/1,1 alternado entre cortes
  "cameras": [[0, 37.367, 347, 195, 1225, 689, {"destino": [96, 250, 1040, 585], "punch": true}],
              [37.367, 182.0, 1390, 746, 491, 276], [182.0, 9999, 55, 754, 491, 276]],
  // selo de status por cima (Remotion): estados [t do editado, cor, texto]
  "selos": [{"ini": 225.9, "fim": 246.6, "rotulo": "SLA DA CONVERSA", "estados": [[225.9, "#f59e0b", "vencimento em breve"], [234.15, "#ef4444", "vencido"]]}],
  "capitulos": [[28.17, 1, "Exemplo · etapa do funil"]]   // montagem no Remotion
}
```
- `motions`: tela cheia; a câmera vem por cima, a menos que `sem_camera`. A que começa em 0 entra sem fusão (gancho no quadro 0). Uma que começa no fim da fala estende o vídeo (o áudio ganha silêncio).
- `cameras`: o render tapa/cola a câmera no retângulo do lugar daquele instante; no Remotion cada lugar vira um recorte (`camera-k.mp4`) e um bloco de moldura que VOA até o lugar seguinte nos últimos 0,55 s. Um trecho do edl não pode atravessar a troca de lugar: ponha a troca dentro de um corte ou pausa (o gerador avisa). Capítulos ficam do lado livre da câmera daquele momento.
 com alfa por cima de tudo (capítulos, selos).
- Tempos de `motions`/`camadas` são do vídeo **editado**: tire de `palavras-final.json` (campo `t`; `src` é o tempo no bruto). Mudou um corte antes delas → recalcule.
- `edl.json` (gerado pelo `plano.py`): cada trecho tem `in`/`out` (s do bruto, na grade de 1/30 s), `ini` (s do editado), e os inteiros que garantem a sincronia — `q_in` (quadro do bruto), `q0` (quadro do editado), `nq` (quantos quadros). Não edite o edl à mão: mude o `edicao.json` e rode o plano.
