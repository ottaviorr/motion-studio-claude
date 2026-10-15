"""Onde a tela mexe, a cada 1/4 s (para acelerar trechos sem fala e para o zoom seguir a ação).
uso: python atividade.py bruto.mp4 atividade.json [--camera x,y,w,h]
Saída: {fps, diff:[fração de pixels que mudaram], caixa:[[x0,y0,x1,y1] em 0–1 ou null]}
A câmera do apresentador (retângulo em pixels do vídeo) fica de fora da conta."""
import sys, subprocess, json
import numpy as np
a = sys.argv[1:]; arq, saida = a[0], a[1]
W, H, F = 384, 216, 4
info = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', arq],
                      capture_output=True, text=True).stdout.strip().split(',')
VW, VH = int(info[0]), int(info[1])
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', arq, '-vf', f'fps={F},scale={W}:{H},format=gray', '-f', 'rawvideo', '-'],
                     capture_output=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)
m = np.ones((H, W), bool)
if '--camera' in a:
    x, y, w, h = map(int, a[a.index('--camera') + 1].split(','))
    m[int(y / VH * H) - 2:int((y + h) / VH * H) + 2, max(0, int(x / VW * W) - 2):int((x + w) / VW * W) + 2] = False
diff, caixa = [0.0], [None]
for i in range(1, len(v)):
    ch = (np.abs(v[i] - v[i - 1]) > 12) & m
    diff.append(round(float(ch.mean()), 4))
    ys, xs = np.nonzero(ch)
    caixa.append([round(float(np.percentile(xs, 5)) / W, 3), round(float(np.percentile(ys, 5)) / H, 3),
                  round(float(np.percentile(xs, 95)) / W, 3), round(float(np.percentile(ys, 95)) / H, 3)] if len(xs) > 3 else None)
json.dump({'fps': F, 'diff': diff, 'caixa': caixa}, open(saida, 'w'))
print(len(v), 'quadros')
