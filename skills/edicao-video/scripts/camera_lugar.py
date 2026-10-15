"""Acha os trechos em que a câmera do apresentador SAIU do lugar (cena do OBS trocada, câmera escondida) — rode ANTES do render.
uso: python camera_lugar.py fonte/edicao.json   → imprime "camera_fora": [[ini, fim], ...] (segundos do BRUTO) para colar no edicao.json
Como: a região da câmera tem sempre o mesmo "jeito" (a pessoa na frente do mesmo fundo). Compara o histograma de brilho dessa região,
2 vezes por segundo, com o histograma típico do vídeo inteiro; trecho que foge do padrão por ≥ 1 s = câmera fora do lugar.
Num projeto real isso só foi visto na folha de fotos, depois de um render perdido (câmera à direita por 10 s)."""
import sys, os, json, subprocess
import numpy as np
cfg = sys.argv[1]; base = os.path.dirname(os.path.abspath(cfg)); C = json.load(open(cfg, encoding='utf8'))
BRUTO = os.path.join(base, C['bruto']); CX, CY, CW, CH = C['camera']
FPS, W = 2, 384   # amostra 2 quadros/s em 384 px de largura (rápido: ~1 min para 10 min de vídeo)
o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', BRUTO], capture_output=True, text=True).stdout
VW, VH = [int(x) for x in o.split()[0].split(',') if x][:2]; H = W * VH // VW; k = W / VW
b = subprocess.run(['ffmpeg', '-v', 'error', '-i', BRUTO, '-vf', f'fps={FPS},scale={W}:{H},format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
F = np.frombuffer(b, np.uint8).reshape(-1, H, W)
x0, y0, x1, y1 = int(CX * k) + 2, int(CY * k) + 2, int((CX + CW) * k) - 2, int((CY + CH) * k) - 2
hist = np.array([np.histogram(f[y0:y1, x0:x1], bins=16, range=(0, 256))[0] for f in F], np.float32)
hist /= hist.sum(1, keepdims=True)
dist = np.abs(hist - np.median(hist, 0)).sum(1)          # 0 = igual ao padrão; 2 = totalmente diferente
fora = dist > max(.6, np.percentile(dist, 50) * 4)
# junta em trechos (tolera 1 amostra solta) e descarta os menores que 1 s
trechos, i = [], 0
while i < len(fora):
    if fora[i]:
        j = i
        while j + 1 < len(fora) and (fora[j + 1] or (j + 2 < len(fora) and fora[j + 2])): j += 1
        if (j - i + 1) / FPS >= 1: trechos.append([round(max(0, i / FPS - .5), 1), round((j + 1) / FPS + .5, 1)])
        i = j + 1
    else: i += 1
print(f'{len(F)} amostras · distância típica {np.median(dist):.2f}')
print('"camera_fora":', json.dumps(trechos), ' ← segundos do bruto; confira 1 quadro de cada e refine a borda (10 quadros/s) antes de usar')
