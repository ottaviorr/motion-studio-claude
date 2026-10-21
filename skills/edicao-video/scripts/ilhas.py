"""Transcreve cada "ilha" de fala SOZINHA (trecho entre dois silêncios) — acha tomada repetida que a transcrição inteira engoliu.
uso: python ilhas.py bruto-30p.mov [--edl fonte/edl.json] [--silencio 0.25] [--db -60] > fonte/ilhas.txt
Por quê: o Whisper, transcrevendo o vídeo de uma vez, "deduplica" frase repetida (na aula SLA: "eu vou usar esse gatilho," [8 s]
"eu vou usar esse gatilho aqui…" saiu como uma frase só, com uma palavra de 8 s; e outras tomadas erradas ficaram no vídeo).
Sozinha, cada ilha não tem contexto para ser engolida. Com --edl, marca o que ficou no vídeo (█ inteira, ▒ em parte, · cortada).
Leia a lista procurando a mesma ideia dita duas vezes em ilhas vizinhas: a errada sai com um corte "exato" nas bordas da ilha."""
import sys, os, json, subprocess
import numpy as np
a = sys.argv[1:]; arq = a[0]
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
SIL, DB = float(op('--silencio', .25)), float(op('--db', -60))
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', arq, '-map', '0:a:0', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True, check=True).stdout
au = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
H = 160; n = len(au) // H
db = 20 * np.log10(np.sqrt((au[:n * H].reshape(n, H) ** 2).mean(1)) + 1e-9)
fala = db > DB
# ilhas: fala separada por silêncio ≥ SIL; ilha < 0,12 s (estalo, respiro) fica de fora
ilhas, i = [], 0
while i < n:
    if not fala[i]: i += 1; continue
    j = i
    while True:
        k = j + 1
        while k < n and not fala[k]: k += 1
        if k < n and (k - j - 1) * .01 < SIL: j = k
        else: break
    if (j - i) * .01 >= .12: ilhas.append([round(i * .01, 2), round((j + 1) * .01, 2)])
    i = j + 1
edl = json.load(open(op('--edl')))['trechos'] if '--edl' in a else None
def ficou(t0, t1):
    if not edl: return ''
    tot = sum(max(0, min(t1, e['out']) - max(t0, e['in'])) for e in edl if e['tipo'] == 'fala')
    f = tot / max(.01, t1 - t0); return '█' if f > .9 else ('▒' if f > .1 else '·')
from faster_whisper import WhisperModel
m = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8')
for t0, t1 in ilhas:
    s0, s1 = max(0, int((t0 - .15) * 16000)), int((t1 + .15) * 16000)
    segs, _ = m.transcribe(au[s0:s1], language='pt', vad_filter=False, condition_on_previous_text=False, beam_size=5)
    txt = ' '.join(s.text.strip() for s in segs)
    print(f'{ficou(t0, t1)} {t0:7.2f}–{t1:7.2f}  {txt}', flush=True)
