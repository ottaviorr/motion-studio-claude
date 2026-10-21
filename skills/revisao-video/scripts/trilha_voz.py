"""Mede a distância trilha × voz SÓ nas janelas com fala (LUFS de curto prazo, 3 s). Reprova abaixo de 20 dB.
uso: python trilha_voz.py voz.wav trilha.wav palavras-final.json [--alvo 30] [--minimo 28]
Por quê: o dono achou a trilha "muito alta" a 18 dB e aprovou 25 dB (aula SLA, 16/10/2026). O LUFS integrado do arquivo
inteiro esconde trecho em que a música sobe; aqui cada janela de 3 s com fala é medida (voz e trilha separadas, mesmo tempo).
Saída: mediana, pior janela (com o tempo), quantas abaixo do mínimo, e RESULTADO."""
import sys, json, subprocess
import numpy as np
a = sys.argv[1:]; VOZ, TRI, PAL = a[0], a[1], a[2]
op = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
ALVO, MIN = op('--alvo', 30), op('--minimo', 28)   # regra do dono (16/10/2026): música 30 dB abaixo da voz
SR = 48000
def carrega(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-af', 'highpass=f=60', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)
v, m = carrega(VOZ), carrega(TRI)
n = min(len(v), len(m)); v, m = v[:n], m[:n]
W = json.load(open(PAL))
fala = np.zeros(int(n / SR * 10) + 1, bool)   # máscara de fala a cada 0,1 s
for w in W: fala[int(w['t'] * 10):int(w.get('e', w['t'] + .3) * 10) + 1] = True
db = lambda x: 10 * np.log10(np.mean(x ** 2) + 1e-12)
res = []
for t in np.arange(0, n / SR - 3, 1.0):
    i0, i1 = int(t * SR), int((t + 3) * SR)
    if fala[int(t * 10):int((t + 3) * 10)].mean() < .6: continue   # janela com ≥ 60 % de fala
    res.append((t, db(v[i0:i1]) - db(m[i0:i1])))
if not res: sys.exit('nenhuma janela com fala')
d = np.array([r[1] for r in res]); pior = res[int(np.argmin(d))]
baixo = [r for r in res if r[1] < MIN]
print(f'trilha × voz em {len(res)} janelas com fala: mediana {np.median(d):.1f} dB abaixo · pior {pior[1]:.1f} dB em {int(pior[0]//60)}:{int(pior[0]%60):02d} · alvo {ALVO:g}')
for t, x in baixo[:10]: print(f'   {int(t//60)}:{int(t%60):02d}  {x:.1f} dB')
print('TRILHA:', 'REPROVADO (' + str(len(baixo)) + ' janelas abaixo de ' + f'{MIN:g} dB)' if baixo else 'APROVADO')
