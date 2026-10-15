"""Revisão de um vídeo pronto, sem precisar assistir: ouve de novo, mede e fotografa.
uso: python revisar.py video.mp4 [--saida pasta] [--esperado palavras.json|roteiro.txt] [--edl edl.json]
                                  [--original bruto.mp4] [--modelo medium] [--fotos 12]
Gera na pasta de saída (padrão: <video>-revisao/):
  revisao.txt         1. técnico (resolução, fps, duração, Mb/s, volume LUFS e pico)
                      2. fala: diferenças entre o que devia ser dito (--esperado) e o que se ouve no final
                      3. repetições coladas ("eu vim cá eu vim cá"): gaguejada que sobrou
                      4. a fala do vídeo final em frases (para ler como espectador: começo, meio e fim)
  ouvido.json         transcrição do final com tempo por palavra
  folha-fotos.jpg     N quadros espalhados pelo vídeo
  folha-emendas.jpg   0,1 s antes/depois de cada emenda (só com --edl)"""
import sys, os, json, subprocess, re, difflib, unicodedata
import numpy as np, cv2
a = sys.argv[1:]; VID = os.path.abspath(a[0])
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
_d = os.path.dirname(VID); _n = re.sub(r'\.\w+$', '', os.path.basename(VID))
# vídeo em prontos/ (pasta de entrega) → revisão em <projeto>/revisao/<nome>, para a pasta de entrega ficar só com vídeos
OUT = op('--saida', os.path.join(os.path.dirname(_d), 'revisao', _n) if os.path.basename(_d) == 'prontos' else re.sub(r'\.\w+$', '', VID) + '-revisao'); os.makedirs(OUT, exist_ok=True)
J = lambda p: os.path.join(OUT, p)
norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())
rel = []

# 1. técnico
def probe(p):
    o = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,bit_rate:stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt',
                                   '-of', 'json', p], capture_output=True, text=True).stdout)
    v = [s for s in o['streams'] if s['codec_type'] == 'video'][0]
    return v, float(o['format']['duration']), int(o['format']['bit_rate']) / 1e6
v, d, br = probe(VID)
ld = subprocess.run(['ffmpeg', '-v', 'info', '-i', VID, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = re.findall(r'I:\s+(-?[\d.]+) LUFS', ld); TP = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', ld)
rel += ['## 1. Técnico', f"{v['width']}×{v['height']} · {v['r_frame_rate']} fps · {v['codec_name']} {v['pix_fmt']} · {d:.1f}s · {br:.1f} Mb/s"]
if '--original' in a:
    vo, do, bo = probe(op('--original'))
    rel.append(f"original: {vo['width']}×{vo['height']} · {vo['r_frame_rate']} fps · {do:.1f}s · {bo:.1f} Mb/s")
rel += [f"Volume {I[-1] if I else '?'} LUFS (YouTube/aula: -16 a -14) · pico {TP[-1] if TP else '?'} dBFS (≤ -1)", '']

# 2–4. fala
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'motion-design', 'scripts'))
from transcrever import transcrever_audio   # GPU NVIDIA quando houver, senão CPU
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', VID, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
au = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
segs = transcrever_audio(au, op('--modelo', 'medium'))
ouv = [{'w': x.word.strip(), 't': round(x.start, 2)} for s in segs for x in s.words if x.word.strip()]
json.dump(ouv, open(J('ouvido.json'), 'w'), ensure_ascii=False, indent=0)
b = [norm(x['w']) for x in ouv]
if '--esperado' in a:
    p = op('--esperado')
    esp = json.load(open(p)) if p.endswith('.json') else [{'w': w, 't': 0} for w in open(p).read().split()]
    ea = [norm(x['w']) for x in esp]
    rel.append('## 2. Fala: esperado × ouvido no final (a maioria é o Whisper ouvindo diferente; olhe as que caem perto de emenda)')
    n = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ea, b, autojunk=False).get_opcodes():
        if tag == 'equal': continue
        e = ' '.join(x['w'] for x in esp[i1:i2]); o = ' '.join(x['w'] for x in ouv[j1:j2])
        if norm(e) == norm(o): continue
        t = ouv[j1]['t'] if j1 < len(ouv) else ouv[-1]['t']
        rel.append(f'  {t:7.2f}s  esperado: "{e}"  →  ouvido: "{o}"'); n += 1
    rel += [f'  ({n} diferenças)', '']
rel.append('## 3. Repetições coladas (gaguejada que sobrou?)')
for k in range(1, 4):
    for i in range(len(b) - 2 * k + 1):
        if b[i:i + k] == b[i + k:i + 2 * k] and all(len(x) > 1 for x in b[i:i + k]):
            rel.append(f'  {ouv[i]["t"]:7.2f}s  "{" ".join(x["w"] for x in ouv[i:i + 2 * k])}"')
rel += ['', '## 4. A fala do vídeo final (leia como espectador: dá para entender? começa, desenvolve e fecha?)']
rel += [f'  {s.start:6.1f}  {s.text.strip()}' for s in segs] + ['']

# fotos
def foto(t, w=480):
    b_ = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0, t):.3f}', '-i', VID, '-frames:v', '1', '-vf', f'scale={w}:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                        capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(b_, np.uint8), cv2.IMREAD_COLOR) if b_ else None
def rotulo(im, txt):
    if im is None: return None
    cv2.rectangle(im, (0, 0), (8 + 11 * len(txt), 28), (0, 0, 0), -1)
    cv2.putText(im, txt, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .55, (255, 255, 255), 1, cv2.LINE_AA); return im
def folha(ims, arq, por_linha):
    ims = [i for i in ims if i is not None]
    if not ims: return
    h, w = ims[0].shape[:2]; ims = [cv2.resize(i, (w, h)) for i in ims]
    ims += [np.zeros_like(ims[0])] * (-len(ims) % por_linha)
    cv2.imwrite(arq, np.vstack([np.hstack(ims[i:i + por_linha]) for i in range(0, len(ims), por_linha)]), [cv2.IMWRITE_JPEG_QUALITY, 82])
N = int(op('--fotos', 12))
folha([rotulo(foto(t), f'{t:.1f}s') for t in np.linspace(.05, d - .1, N)], J('folha-fotos.jpg'), 4)
if '--edl' in a:
    emendas = [e['ini'] for e in json.load(open(op('--edl')))['trechos'][1:]]
    ims = []
    for t in emendas:
        ims += [rotulo(foto(t - .1), f'{t:.1f} antes'), rotulo(foto(t + .1), f'{t:.1f} depois')]
    folha(ims, J('folha-emendas.jpg'), 8)
    rel.append(f'## 5. Emendas: {len(emendas)} → folha-emendas.jpg (pulo feio de rosto/tela, quadro preto, câmera fora do lugar)')
open(J('revisao.txt'), 'w').write('\n'.join(rel) + '\n')
print('\n'.join(rel)); print('→', OUT)
