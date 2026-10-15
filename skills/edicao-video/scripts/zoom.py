"""Zoom que acompanha a ação na tela (estilo Screen Studio), no tempo do vídeo editado.
uso: python zoom.py fonte/edicao.json
Lê edl.json + atividade.json; grava zoom.json: [{t, z, cx, cy}] = a partir de t, ir para o zoom z centrado em (cx, cy) (0–1).
Ajustes manuais: "zoom_fixo" no edicao.json, [[t_ini, t_fim, z, cx, cy], ...] no tempo editado, vence o automático."""
import sys, json, os
import numpy as np
cfg = sys.argv[1]; base = os.path.dirname(os.path.abspath(cfg)); C = json.load(open(cfg))
Z = {'max': 1.6, 'min': 1.25, 'margem': .14, 'janela': 2.5, 'antes': .5, 'segura': 4.0, 'estavel': 1.5, 'limiar': .002, **C.get('zoom', {})}
edl = json.load(open(os.path.join(base, 'edl.json')))
at = json.load(open(os.path.join(base, C.get('atividade', 'atividade.json'))))
F = at['fps']; DUR = edl['dur']

def fonte(t):   # tempo editado → (tempo bruto, trecho)
    for e in edl['trechos']:
        d = (e['out'] - e['in']) / e['vel']
        if e['ini'] <= t < e['ini'] + d: return e['in'] + (t - e['ini']) * e['vel'], e
    return None, None

def caixas(t0, t1):
    out = []
    for t in np.arange(max(0, t0), min(DUR, t1), .25):
        s, e = fonte(t)
        if s is None or e['tipo'] != 'fala': continue
        i = int(s * F)
        if i < len(at['diff']) and at['diff'][i] > Z['limiar'] and at['caixa'][i]: out.append(at['caixa'][i])
    return out

def alvo(t):
    cx = caixas(t - Z['antes'], t + Z['janela'])
    if not cx: return None
    b = np.array(cx); x0, y0 = np.percentile(b[:, 0], 10), np.percentile(b[:, 1], 10)
    x1, y1 = np.percentile(b[:, 2], 90), np.percentile(b[:, 3], 90)
    z = min(Z['max'], 1 / (max(x1 - x0, y1 - y0) + Z['margem']))
    if z < Z['min']: return (1.0, .5, .5)
    h = .5 / z
    return (round(z, 2), round(float(np.clip((x0 + x1) / 2, h, 1 - h)), 3), round(float(np.clip((y0 + y1) / 2, h, 1 - h)), 3))

kf = [{'t': 0.0, 'z': 1.0, 'cx': .5, 'cy': .5}]; desde = 0.0
for t in np.arange(0, DUR, .5):
    s, e = fonte(t)
    a = (1.0, .5, .5) if (e and e['tipo'] != 'fala') else alvo(t)
    if a is None: continue
    u = kf[-1]
    perto = lambda p, q: abs(p[0] - q[0]) <= .2 and (p[0] == 1 or (abs(p[1] - q[1]) <= .1 and abs(p[2] - q[2]) <= .1))
    muda = not perto(a, (u['z'], u['cx'], u['cy']))
    if muda and not (e and e['tipo'] != 'fala'):   # só muda se o alvo novo se mantém (sem pular para lá e voltar)
        seg = [alvo(t + d) for d in np.arange(.5, Z['estavel'] + .01, .5)]
        muda = all(x is None or perto(x, a) for x in seg)
    forcado = e and e['tipo'] != 'fala' and u['z'] != 1.0
    if muda and (t - desde >= Z['segura'] or forcado):
        kf.append({'t': round(float(t), 2), 'z': float(a[0]), 'cx': float(a[1]), 'cy': float(a[2])}); desde = t
for t0, t1, z, cx, cy in C.get('zoom_fixo', []):   # manual: corta o automático no intervalo
    fim = [k for k in kf if k['t'] < t1][-1]
    kf = [k for k in kf if not (t0 <= k['t'] < t1)] + [{'t': t0, 'z': z, 'cx': cx, 'cy': cy}, {**fim, 't': t1}]
    kf.sort(key=lambda k: k['t'])
json.dump(kf, open(os.path.join(base, 'zoom.json'), 'w'), indent=0)
print(len(kf), 'mudanças de zoom'); [print(k) for k in kf]
