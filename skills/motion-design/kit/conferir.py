"""Folha de conferência: fotos de uma cena em vários segundos, lado a lado, com a zona segura do Reels por cima (em pé).
uso: python3 base/conferir.py <vídeo>/fonte/NN-nome.html t1 t2 ... [--leg]   → .shots/conf-NN.jpg
--leg: põe também a camada de legenda no tempo global certo (só criativos em pé)."""
import sys, subprocess, pathlib, json, tempfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
B = pathlib.Path(__file__).parent; G = B / 'gravar.mjs'
html = pathlib.Path(sys.argv[1]).resolve(); args = sys.argv[2:]; leg = '--leg' in args
ts = [float(a) for a in args if not a.startswith('--')]
tmp = pathlib.Path(tempfile.mkdtemp(prefix='conf-'))
def foto(arq, t, out):
    subprocess.run(['node', str(G), str(out), '--html', str(arq), '--so', str(t)], capture_output=True, cwd=arq.parent)
k = html.name[:2]; plano = json.load(open(html.parent / 'plano.json'))
ini = next(c['in'] for c in plano['clips'] if c['k'] == k)
with ThreadPoolExecutor(4) as ex:
    for i, t in enumerate(ts):
        ex.submit(foto, html, t, tmp / f'c{i}.mp4')
        if leg: ex.submit(foto, html.parent / 'legenda.html', round(ini + t, 3), tmp / f'l{i}.mov')
ims = []
for i, t in enumerate(ts):
    im = Image.open(tmp / f'c{i}.jpg').convert('RGBA')
    if leg and (tmp / f'l{i}.png').exists(): im.alpha_composite(Image.open(tmp / f'l{i}.png').convert('RGBA'))
    if im.height > im.width: im.alpha_composite(Image.open(B / 'zona-segura.png'))
    ims.append(im.convert('RGB'))
w = 420 if ims[0].height > ims[0].width else 640; h = round(w * ims[0].height / ims[0].width)
cols = min(len(ims), 5 if w == 420 else 3); rows = (len(ims) + cols - 1) // cols
folha = Image.new('RGB', (w * cols, h * rows), (20, 20, 24))
for i, im in enumerate(ims): folha.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
out = B.parent.parent.parent / '.shots' / f'conf-{html.parent.parent.name[:3]}-{k}.jpg'
folha.save(out, quality=85); print(out)
