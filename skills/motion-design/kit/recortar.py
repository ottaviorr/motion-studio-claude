"""Recorta o sujeito (pessoa, cabelo, roupa) de um vídeo quadro a quadro com o MediaPipe Image Segmenter (Apache-2.0).
Para "texto ATRÁS da pessoa": a cena desenha o vídeo, depois o texto, e por cima o recorte da pessoa (mistura.js → atrasDoSujeito).
uso: .ferramentas/.venv/bin/python recortar.py video.mp4 --saida pasta/ [--inicio 2.0] [--dur 3] [--fps 30] [--largura 720]
        [--modelo multiclasse|selfie] [--classes pessoa|cabelo|rosto|corpo|roupa|cabelo,rosto] [--ponto x,y] [--suave 0.5]
Sai em pasta/:
  r_0000.png …   recorte RGBA (pixels do vídeo onde é sujeito, transparente no resto) no tamanho --largura (altura proporcional)
  m_0000.png …   máscara em tons de cinza (branco = sujeito), mesma resolução — para CSS mask‑image ou cor só no cabelo
  sujeito.json   {fps, inicio, dur, w, h, n, quadros: [{caixa:[x,y,w,h], centro:[x,y], topo:[x,y], area}], ponto: [[x,y],...]}
                 coordenadas em fração 0–1 do quadro (multiplique pela caixa do vídeo na cena). Também sujeito.js (window.SUJEITO_DADOS).
  folha.jpg      3 quadros (começo, meio, fim): vídeo | máscara | recorte sobre xadrez — OLHE antes de usar.
--inicio/--dur: trecho do ARQUIVO (o mesmo data-media-start do <video> na cena). --fps: quadros da CENA, ex.: 30, não do arquivo:
  o quadro i é o instante inicio + i/fps do arquivo (lido por tempo, então 25 fps no arquivo também casa).
--modelo multiclasse (padrão, 256×256, tem cabelo/rosto/corpo/roupa) ou selfie (mais leve, só pessoa, borda mais dura).
--ponto x,y (fração 0–1 no 1º quadro): rastreia esse ponto com fluxo óptico (Lucas-Kanade do OpenCV) → "ponto" no JSON (linhaSegue).
--suave: mistura com a máscara do quadro anterior (0 = sem, 0,5 = padrão) para a borda não tremer.
Modelos em ~/motion-studio/.ferramentas/modelos/ (selfie_multiclass_256x256.tflite, selfie_segmenter.tflite).
"""
import sys, os, json
import numpy as np, cv2
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

a = sys.argv[1:]
if not a or a[0].startswith('-'): print(__doc__); sys.exit(1)
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
video = a[0]; pasta = op('--saida', os.path.splitext(video)[0] + '-recorte')
ini = float(op('--inicio', 0)); dur = op('--dur'); FPS = float(op('--fps', 30)); LARG = int(op('--largura', 720))
modelo = op('--modelo', 'multiclasse'); classes = op('--classes', 'pessoa'); suave = float(op('--suave', .5)); ponto = op('--ponto')
MOD = os.path.expanduser('~/motion-studio/.ferramentas/modelos/' + ('selfie_multiclass_256x256.tflite' if modelo == 'multiclasse' else 'selfie_segmenter.tflite'))
# multiclasse: 0 fundo, 1 cabelo, 2 pele do corpo, 3 pele do rosto, 4 roupa, 5 outros (acessórios)
CL = {'pessoa': [1, 2, 3, 4, 5], 'cabelo': [1], 'corpo': [2], 'rosto': [3], 'roupa': [4], 'outros': [5], 'pele': [2, 3]}
quero = sorted({c for n in classes.split(',') for c in CL[n.strip()]})
if modelo != 'multiclasse' and classes != 'pessoa': sys.exit('o modelo selfie só separa pessoa; use --modelo multiclasse para cabelo/rosto/roupa')

os.makedirs(pasta, exist_ok=True)
for f in os.listdir(pasta):
    if f[:2] in ('r_', 'm_') and f.endswith('.png'): os.remove(os.path.join(pasta, f))
cap = cv2.VideoCapture(video)
fps_arq = cap.get(cv2.CAP_PROP_FPS) or 30; tot = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps_arq
fim = min(tot, ini + float(dur)) if dur else tot
n = int(round((fim - ini) * FPS))
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=mpt.BaseOptions(model_asset_path=MOD), running_mode=vision.RunningMode.VIDEO,
    output_confidence_masks=True, output_category_mask=False))

def quadro(t):   # lê o quadro do arquivo mais perto do instante t (por índice, mais confiável que CAP_PROP_POS_MSEC)
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps_arq))); ok, im = cap.read(); return im if ok else None

anterior = None; Q = []; pts = []; lk_prev = None; lk_pt = None; folha_ids = [0, n // 2, max(0, n - 1)]; folha = []
for i in range(n):
    t = ini + i / FPS; bgr = quadro(t)
    if bgr is None: break
    H0, W0 = bgr.shape[:2]; W = LARG; H = int(round(H0 * W / W0)); bgr = cv2.resize(bgr, (W, H), interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    # o modelo é quadrado (256×256): o 9:16 esticado deforma a pessoa e piora muito a máscara → completa com borda até quadrado
    L = max(W, H); px0, py0 = (L - W) // 2, (L - H) // 2
    sq = cv2.copyMakeBorder(rgb, py0, L - H - py0, px0, L - W - px0, cv2.BORDER_REPLICATE)
    r = seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(sq)), int(round(i * 1000 / FPS)) + 1)
    cm = [cv2.resize(m.numpy_view().astype(np.float32), (L, L))[py0:py0 + H, px0:px0 + W] for m in r.confidence_masks]
    if modelo == 'multiclasse': conf = np.clip(sum(cm[c] for c in quero), 0, 1)
    else: conf = cm[0] if len(cm) == 1 else cm[-1]
    conf = cv2.resize(conf.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
    if anterior is not None and suave > 0: conf = (1 - suave) * conf + suave * anterior
    anterior = conf
    # borda: curva em S (tira o halo cinza) + 1 px de desfoque
    alfa = np.clip((conf - .35) / .3, 0, 1); alfa = cv2.GaussianBlur(alfa, (0, 0), .8)
    a8 = (alfa * 255).astype(np.uint8)
    cv2.imwrite(os.path.join(pasta, f'm_{i:04d}.png'), a8)
    cv2.imwrite(os.path.join(pasta, f'r_{i:04d}.png'), np.dstack([bgr, a8]), [cv2.IMWRITE_PNG_COMPRESSION, 6])
    ys, xs = np.nonzero(a8 > 127)
    if len(xs):
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max(); top = ys.min(); xt = xs[ys <= top + 3].mean()
        Q.append({'caixa': [round(x0 / W, 4), round(y0 / H, 4), round((x1 - x0) / W, 4), round((y1 - y0) / H, 4)],
                  'centro': [round(xs.mean() / W, 4), round(ys.mean() / H, 4)], 'topo': [round(xt / W, 4), round(top / H, 4)], 'area': round(len(xs) / (W * H), 4)})
    else: Q.append(None)
    if ponto:   # Lucas-Kanade, quadro a quadro
        g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        if lk_prev is None: px, py = map(float, ponto.split(',')); lk_pt = np.array([[[px * W, py * H]]], np.float32)
        else:
            nv, st, _ = cv2.calcOpticalFlowPyrLK(lk_prev, g, lk_pt, None, winSize=(31, 31), maxLevel=3)
            if st[0][0]: lk_pt = nv
        lk_prev = g; pts.append([round(float(lk_pt[0][0][0]) / W, 4), round(float(lk_pt[0][0][1]) / H, 4)])
    if i in folha_ids:
        xadrez = ((np.indices((H, W)).sum(0) // 24) % 2 * 60 + 150).astype(np.uint8)[..., None].repeat(3, 2)
        rec = (bgr * alfa[..., None] + xadrez * (1 - alfa[..., None])).astype(np.uint8)
        folha.append(np.hstack([bgr, cv2.cvtColor(a8, cv2.COLOR_GRAY2BGR), rec]))
    if i % 30 == 0: print(f'  quadro {i}/{n}', end='\r')
nq = len(Q)
D = {'video': os.path.basename(video), 'inicio': ini, 'dur': round(nq / FPS, 3), 'fps': FPS, 'w': W, 'h': H, 'n': nq,
     'modelo': modelo, 'classes': classes, 'quadros': Q, 'ponto': pts}
json.dump(D, open(os.path.join(pasta, 'sujeito.json'), 'w'), separators=(',', ':'))
open(os.path.join(pasta, 'sujeito.js'), 'w').write('window.SUJEITO_DADOS=window.SUJEITO_DADOS||{};window.SUJEITO_DADOS[' + json.dumps(os.path.basename(os.path.normpath(pasta))) + ']=' + json.dumps(D, separators=(',', ':')) + ';\n')
if folha:
    fl = np.vstack(folha); s = min(1, 1800 / fl.shape[1]); cv2.imwrite(os.path.join(pasta, 'folha.jpg'), cv2.resize(fl, None, fx=s, fy=s), [cv2.IMWRITE_JPEG_QUALITY, 85])
areas = [q['area'] for q in Q if q]
print(f'{nq} quadros {W}×{H} → {pasta}  · sujeito em {len(areas)}/{nq} quadros, área média {np.mean(areas) if areas else 0:.2f}  · folha: {os.path.join(pasta, "folha.jpg")}')
