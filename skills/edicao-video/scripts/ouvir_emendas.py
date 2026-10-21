"""Ouve o vídeo editado ANTES de renderizar: monta só o áudio a partir do edl.json e transcreve.
uso: python ouvir_emendas.py fonte/edicao.json [--modelo large-v3-turbo] [--cortes]
Saída: o texto do vídeo editado em frases com o tempo (editado). Leia como espectador:
  - emenda de corte de fala tem que soar como uma frase só, sem meia sílaba ("e a automação", não "e a auto-automação")
  - com --cortes, imprime também 4 s em volta de cada corte manual (o que veio antes ‖ o que veio depois)
Rápido (só o áudio) e com cache (scripts/ouvir.py): rodar de novo o mesmo plano sai na hora."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ouvir import transcrever, carregar, PADRAO
cfg = sys.argv[1]; base = os.path.dirname(os.path.abspath(cfg)); C = json.load(open(cfg))
modelo = sys.argv[sys.argv.index('--modelo') + 1] if '--modelo' in sys.argv else PADRAO
edl = json.load(open(os.path.join(base, 'edl.json')))['trechos']
a = carregar(os.path.join(base, C['bruto']))
au = np.concatenate([a[int(round(e['in'] * 16000)):int(round(e['out'] * 16000))] for e in edl if e['tipo'] == 'fala'])
segs = transcrever(au, modelo, palavras='--cortes' in sys.argv)
for s in segs: print(f"{s['start']:7.1f}  {s['text'].strip()}")
if '--cortes' in sys.argv:
    ws = [w for s in segs for w in s['words']]
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
        antes = ' '.join(w['w'] for w in ws if t - 2.5 <= w['t'] < t)
        depois = ' '.join(w['w'] for w in ws if t <= w['t'] < t + 2)
        print(f'{t:7.1f}  …{antes} ‖ {depois}…   ({motivo})')
