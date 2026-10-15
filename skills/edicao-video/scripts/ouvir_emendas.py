"""Ouve o vídeo editado ANTES de renderizar: monta só o áudio a partir do edl.json e transcreve.
uso: python ouvir_emendas.py fonte/edicao.json [--modelo medium] [--cortes]
Saída: o texto do vídeo editado em frases com o tempo (editado). Leia como espectador:
  - emenda de corte de fala tem que soar como uma frase só, sem meia sílaba ("e a automação", não "e a auto-automação")
  - com --cortes, imprime também 4 s em volta de cada corte manual (o que veio antes ‖ o que veio depois)
Rápido (~1 min para 3 min de vídeo): rode depois de cada mudança nos cortes, antes do render (que demora)."""
import sys, os, json, subprocess
import numpy as np
cfg = sys.argv[1]; base = os.path.dirname(os.path.abspath(cfg)); C = json.load(open(cfg))
modelo = sys.argv[sys.argv.index('--modelo') + 1] if '--modelo' in sys.argv else 'medium'
edl = json.load(open(os.path.join(base, 'edl.json')))['trechos']
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(base, C['bruto']), '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                     capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
au = np.concatenate([a[int(e['in'] * 16000):int(e['out'] * 16000)] for e in edl if e['tipo'] == 'fala'])
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'motion-design', 'scripts'))
from transcrever import transcrever_audio   # GPU NVIDIA quando houver, senão CPU
segs = transcrever_audio(au, modelo)
for s in segs: print(f'{s.start:7.1f}  {s.text.strip()}')
if '--cortes' in sys.argv:
    ws = [w for s in segs for w in s.words]
    def mapa(x):
        t = 0
        for e in edl:
            if e['tipo'] != 'fala': continue
            if e['in'] - .01 <= x <= e['out'] + .01: return t + x - e['in']
            t += e['out'] - e['in']
    print('\n== emendas dos cortes manuais')
    for ini, fim, motivo, *_ in sorted(C.get('cortes', [])):
        t = mapa(fim)
        if t is None: continue
        antes = ' '.join(w.word.strip() for w in ws if t - 2.5 <= w.start < t)
        depois = ' '.join(w.word.strip() for w in ws if t <= w.start < t + 2)
        print(f'{t:7.1f}  …{antes} ‖ {depois}…   ({motivo})')
