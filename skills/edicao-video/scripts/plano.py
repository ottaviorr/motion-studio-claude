"""Plano de edição de uma gravação: o que fica, o que sai, o que acelera.
uso: python plano.py fonte/edicao.json
Lê do edicao.json: bruto (vídeo), palavras (transcrição com tempo), atividade (tela, de atividade.py),
cortes manuais [[ini, fim, "motivo"(, "exato")], ...] e as regras de silêncio/aceleração.
Gera ao lado do edicao.json:
  edl.json            trechos [{in, out, vel, tipo}] na ordem (tempo do bruto)
  palavras-final.json palavras que sobraram, no tempo do vídeo editado (para motions e revisão)
  cortes.txt          relatório legível: cada corte/aceleração com o texto e o motivo
Regras:
  - silêncio longo → corta, deixando um respiro antes/depois (com a tela mexendo também: o resultado aparece logo depois
    e a fala segue; acelerar no meio de uma frase quebra o sentido — o dono reprovou). Aceleração só com "acelerar": {"ativo": true}
  - emenda em que a tela muda de verdade ganha "fusao" (o render funde 0,25 s em vez de pular)
  - cada borda de corte é puxada para o ponto mais baixo do áudio por perto (sem cortar sílaba nem dar estalo)."""
import sys, json, os, subprocess
import numpy as np

cfg_path = sys.argv[1]; base = os.path.dirname(os.path.abspath(cfg_path))
C = json.load(open(cfg_path))
P = lambda k, d=None: os.path.join(base, C.get(k, d))
S = {'db': -40, 'min': 0.45, 'antes': 0.15, 'depois': 0.10, **C.get('silencio', {})}
A = {'ativo': False, 'atividade': 0.01, 'fracao': 0.25, 'alvo': 4, 'max': 6, 'min_dur': 0.9, 'min_bruto': 2.5, **C.get('acelerar', {})}

# ---------- áudio: volume a cada 10 ms ----------
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', P('bruto'), '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                     capture_output=True, check=True).stdout
au = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
HOP = 160
rms = np.sqrt(np.add.reduceat(au ** 2, np.arange(0, len(au), HOP)) / HOP + 1e-12)
db = 20 * np.log10(rms + 1e-9)
DUR = len(au) / 16000

def vale(t, janela=0.12):
    """ponto mais quieto perto de t"""
    i0, i1 = max(0, int((t - janela) * 100)), min(len(db), int((t + janela) * 100) + 1)
    return (i0 + int(np.argmin(db[i0:i1]))) / 100

def quieto_antes(t, limite, recua=0.3, db_q=-62):
    """último ponto em silêncio em [t - recua, t] (o Whisper erra a borda da palavra em ~0,15 s);
    a borda do corte vai para lá, sem comer o começo da palavra seguinte nem deixar meia sílaba"""
    for i in range(int(t * 100), max(int(limite * 100), int((t - recua) * 100)) - 1, -1):
        if 0 <= i < len(db) and db[i] < db_q: return max(limite, i / 100 - .01)
    return None

def silencios():
    q = db < S['db']; out = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) / 100 >= S['min']: out.append((i / 100, j / 100))
            i = j
        else: i += 1
    return out

# ---------- tela: quanto mexe ----------
at = json.load(open(P('atividade'))); F = at['fps']; dif = np.array(at['diff'])
def mexe(a, b):
    seg = dif[int(a * F):max(int(a * F) + 1, int(b * F))]
    return len(seg) and (seg > A['atividade']).mean() >= A['fracao']

W = json.load(open(P('palavras')))
def texto(a, b): return ' '.join(w['w'] for w in W if w['t'] >= a - .05 and w['e'] <= b + .05)

# ---------- 1. cortes manuais (bordas no vale do áudio) ----------
fica = [[0.0, DUR]]; rel = []
for ini, fim, motivo, *op in sorted(C.get('cortes', [])):
    if 'exato' in op: a, b = ini, fim   # bordas medidas à mão (ex.: "é" arrastado colado na palavra seguinte)
    else:
        a = quieto_antes(ini, 0) or vale(ini, .05)
        b = quieto_antes(fim, a + .02) or vale(fim, .05)   # gaguejada no meio da fala (sem silêncio): ajuste fino no vale
    rel.append(f'CORTE   {a:7.2f}–{b:7.2f}  ({b-a:4.1f}s)  {motivo}: "{texto(a, b)}"')
    novo = []
    for x, y in fica:
        if b <= x or a >= y: novo.append([x, y]); continue
        if a > x: novo.append([x, a])
        if b < y: novo.append([b, y])
    fica = novo

# ---------- 2. silêncios dentro do que ficou ----------
segs = []   # (in, out, vel, tipo)
sil = silencios()
for x, y in fica:
    cur = x
    for s0, s1 in sil:
        a, b = max(s0, x), min(s1, y)
        if b - a < S['min']: continue
        ini_silencio = a if a > x + .01 else None   # silêncio colado no início do trecho: sem respiro antes
        a2 = a + (S['antes'] if ini_silencio is not None else 0)
        b2 = b - (S['depois'] if b < y - .01 else 0)
        if b2 - a2 < .15: continue
        if A['ativo'] and mexe(a, b) and b2 - a2 >= A['min_bruto']:
            vel = min(A['max'], max(2.0, (b2 - a2) / max(A['min_dur'], (b2 - a2) / A['alvo'])))
            segs.append((cur, a2, 1.0, 'fala')); segs.append((a2, b2, round(vel, 2), 'acelerado'))
            rel.append(f'ACELERA {a2:7.2f}–{b2:7.2f}  ({b2-a2:4.1f}s → {(b2-a2)/vel:3.1f}s, {vel:.1f}×)  tela mexendo sem fala')
        else:
            segs.append((cur, a2, 1.0, 'fala'))
            rel.append(f'PAUSA   {a2:7.2f}–{b2:7.2f}  ({b2-a2:4.1f}s)' + ('  (tela mexendo: corta e funde)' if mexe(a, b) else ''))
        cur = b2
    segs.append((cur, y, 1.0, 'fala'))
segs = [s for s in segs if s[1] - s[0] > 0.02]

# ---------- 3. mapa bruto → editado ----------
cam = C.get('camera')
def mini(tt):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{tt:.3f}', '-i', P('bruto'), '-frames:v', '1', '-vf', 'scale=192:108,format=gray',
                        '-f', 'rawvideo', '-'], capture_output=True).stdout
    g = np.frombuffer(b, np.uint8).reshape(108, 192).astype(np.int16)
    if cam: g = g.copy(); x, y, w, h = cam; g[int(y / 10) - 1:int((y + h) / 10) + 2, int(x / 10) - 1:int((x + w) / 10) + 2] = 0
    return g
edl = []; t = 0.0
for i, (a, b, v, tipo) in enumerate(segs):
    e = {'in': round(a, 3), 'out': round(b, 3), 'vel': v, 'tipo': tipo, 'ini': round(t, 3)}
    if i and a - segs[i - 1][1] > .05:   # houve corte antes deste trecho
        muda = float((np.abs(mini(segs[i - 1][1] - .03) - mini(a + .02)) > 18).mean())
        if muda > C.get('fusao_limiar', .02): e['fusao'] = round(muda, 3)
    edl.append(e)
    t += (b - a) / v
def mapa(s, folga=0.0):
    """tempo bruto → editado; com folga, um ponto que caiu num corte vai para a borda mais próxima (até 'folga' s)"""
    for e in edl:
        if e['in'] - 1e-3 <= s <= e['out'] + 1e-3: return e['ini'] + (s - e['in']) / e['vel']
    if folga:
        perto = min(edl, key=lambda e: min(abs(s - e['in']), abs(s - e['out'])))
        if min(abs(s - perto['in']), abs(s - perto['out'])) <= folga: return mapa(min(max(s, perto['in']), perto['out']))
    return None
final = []
for w in W:
    # palavra some só se o MEIO dela foi cortado (o Whisper erra as bordas em ~0,2 s)
    if mapa((w['t'] + w['e']) / 2) is None and mapa(w['t']) is None: continue
    m0 = mapa(w['t'], .4); m1 = mapa(max(w['t'], w['e'] - .02), .4)
    if m0 is None: continue
    if m1 is None: m1 = m0 + .2
    final.append({'w': w['w'], 't': round(m0, 3), 'e': round(max(m0, m1), 3), 'src': w['t']})

json.dump({'dur': round(t, 3), 'bruto_dur': round(DUR, 3), 'trechos': edl}, open(os.path.join(base, 'edl.json'), 'w'), indent=1)
json.dump(final, open(os.path.join(base, 'palavras-final.json'), 'w'), ensure_ascii=False, indent=0)
open(os.path.join(base, 'palavras-final.txt'), 'w').write(' '.join(f"{w['t']:.2f}:{w['w']}" for w in final) + '\n')
open(os.path.join(base, 'cortes.txt'), 'w').write(
    f'Bruto {DUR:.1f}s → editado {t:.1f}s ({DUR - t:.1f}s a menos)\n\n' + '\n'.join(sorted(rel, key=lambda r: float(r.split()[1].split('–')[0]))) + '\n')
print(f'{len(edl)} trechos · bruto {DUR:.1f}s → editado {t:.1f}s · {sum(1 for e in edl if e.get("fusao"))} emendas com fusão')
