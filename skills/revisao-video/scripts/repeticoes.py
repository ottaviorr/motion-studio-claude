"""Acha TOMADA REPETIDA (colada ou distante) no vídeo final: cada ilha de fala é transcrita sozinha (edicao-video/scripts/ilhas.py)
e comparada com as 3 seguintes. Qualquer par parecido = REPROVADO até alguém ouvir e decidir.
uso: python repeticoes.py final.mp4 [--ilhas ilhas.txt] [--db -45] [--limiar 0.7]
  (--ilhas: reaproveita uma saída do ilhas.py já feita; sem ele, roda o ilhas.py — ~2 min por minuto de vídeo)
Por quê: na aula SLA ficaram 8 tomadas erradas junto com as certas; a transcrição do vídeo inteiro "engolia" a repetição.
Com música por baixo, use --db -45 (a trilha ocupa os silêncios)."""
import sys, os, re, subprocess
from difflib import SequenceMatcher
a = sys.argv[1:]; FIN = a[0]
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
LIM = float(op('--limiar', .7))
if op('--ilhas'): txt = open(op('--ilhas')).read()
else:
    ilhas = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'edicao-video', 'scripts', 'ilhas.py')
    txt = subprocess.run([sys.executable, ilhas, FIN, '--db', op('--db', '-45')], capture_output=True, text=True).stdout
I = []
for l in txt.splitlines():
    m = re.match(r'^\S?\s*([\d.]+)–\s*([\d.]+)\s+(.*)$', l.strip())
    if m: I.append((float(m[1]), m[3]))
# frases dentro de cada ilha (ilha longa vira várias frases), com o tempo da ilha
F = [(t, f.strip()) for t, s in I for f in re.split(r'(?<=[.?!])\s+', s) if len(f.split()) >= 3]
norm = lambda s: re.sub(r'[^a-zà-ú0-9 ]', '', s.lower())
pares = []
for i, (t, f) in enumerate(F):
    for j in range(i + 1, min(len(F), i + 4)):
        r = SequenceMatcher(None, norm(f), norm(F[j][1])).ratio()
        A, B = norm(f).split(), norm(F[j][1]).split()
        # recomeço: um trecho de 4 palavras do COMEÇO de B (primeiras 6) já foi dito em A ("…do seu…" → "o tempo de resposta dos seus")
        reco = any(' '.join(B[k:k + 4]) in ' '.join(A) for k in range(0, max(0, min(3, len(B) - 3))))
        if r >= LIM or reco: pares.append((t, F[j][0], r, f, F[j][1]))
mm = lambda t: f'{int(t // 60)}:{int(t % 60):02d}'
for t1, t2, r, f1, f2 in pares: print(f'  {mm(t1)} ≈ {mm(t2)} ({r:.2f}): "{f1[:70]}" × "{f2[:70]}"')
print(f'{len(F)} frases · {len(pares)} pares parecidos → REPETIÇÕES:', 'REPROVADO (ouvir cada par)' if pares else 'APROVADO')
