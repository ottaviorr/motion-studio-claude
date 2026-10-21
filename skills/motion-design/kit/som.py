"""Efeitos sonoros sintetizados por peça (técnica dos 3 motions do portfólio): whoosh, impacto, tique, riser… gerados por código,
sincronizados com a cena, num WAV 48 kHz estéreo 24 bits com limitador e pico máximo controlado — pronto para mixar com a trilha.
Só numpy (o venv do estúdio não tem scipy). Mesma entrada = mesmo som (semente fixa, cada evento com a sua).

uso: .ferramentas/.venv/bin/python som.py eventos.json saida.wav
     .ferramentas/.venv/bin/python som.py saida.wav --dur 4 whoosh@1.2 impacto@2:0.9 tique@3:.4:-.3 [--pico -1] [--trilha m.mp3 --inicio 5.7]
     .ferramentas/.venv/bin/python som.py --lista          (tipos e parâmetros)
  evento em argumento: tipo@tempo[:ganho[:pan]] · tempo em s, ou bN = batida N (precisa de --bpm, e --ancora se a batida 0 não for 0 s)
eventos.json:
  {"dur": 20, "bpm": 121, "ancora": 0, "semente": 1, "pico": -1, "ganho_fx": 1,
   "trilha": "musica.mp3", "inicio": 5.699, "ganho_trilha": 0.8, "saida_trilha": 1.2,
   "eventos": [{"t": 1.0, "tipo": "whoosh", "g": 0.3, "pan": -0.35, "dur": 0.48},
               {"b": 20, "tipo": "impacto", "g": 0.9}, ...]}
  t = segundos (ou b = batida); g = ganho (0..1, padrão .3); pan -1..1; os outros campos vão para o efeito (ver --lista).
  ALINHAMENTO: o tempo é o instante que CASA com a imagem — whoosh/sopro: o pico (o corte no meio do giro); riser e reverso:
  o fim (o drop); impacto, tique, clique etc.: o ataque.
Níveis que funcionaram nos do portfólio (ganho de cada efeito com a trilha a 1,0):
  whoosh de giro .22–.36 · tap .42 · bip .16 · tique de moeda .22 · subida .12 · pouso .32 · impacto .7–.95 · sub-drop .8
  (no Filme C os efeitos somados ainda entraram × .55; no Filme B a trilha a .55 e os efeitos × .42 — peça calma, trilha baixa).
  Depois de juntar com a trilha: -14 LUFS e pico real ≤ -1 dBTP (loudnorm em 2 passadas ou ganho + alimiter 0.8 a 192 kHz).
Sem --trilha sai só a faixa de efeitos (pico ≤ --pico, padrão -1 dBFS). Com --trilha sai a mistura (ainda sem normalizar em LUFS)."""
import sys, json, wave, subprocess, numpy as np

SR = 48000

# ---------- blocos ----------
def env(n, a, d):
    """ataque linear de a s + queda exponencial de d s"""
    t = np.arange(n) / SR; e = np.exp(-t / max(d, 1e-5)); na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na); return e
def lp(x, fc):
    """passa-baixa de 1 polo (fc pode variar no tempo)"""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape); a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); v = 0.0
    for i in range(len(x)): v = (1 - a[i]) * x[i] + a[i] * v; y[i] = v
    return y
def hp(x, fc): return x - lp(x, fc)
def bp_var(x, f0, f1, q=.7):
    """passa-faixa de estado variável com a frequência andando de f0 a f1 (o 'ar' do whoosh)"""
    n = len(x); fc = np.geomspace(f0, f1, n); f = 2 * np.sin(np.pi * np.minimum(fc, SR / 6) / SR); y = np.empty(n); lo = b = 0.0
    for i in range(n):
        h = x[i] - lo - q * b; b += f[i] * h; lo += f[i] * b; y[i] = b
    return y
def norm(x): return x / (np.abs(x).max() + 1e-9)
def reverb(x, seg=2.0, mix=.3, cor=2500, rng=None):
    """sala sintética: ruído com queda exponencial (RT60 = seg), convolução por FFT"""
    n = int(seg * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (seg / 6.9)); ir = lp(ir, cor); ir /= np.sqrt((ir ** 2).sum())
    L = len(x) + n; F = 1 << (L - 1).bit_length(); y = np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:L]
    z = np.zeros(L); z[:len(x)] = x * (1 - mix); return z + y * mix * 1.6
def seno_var(f): return np.sin(2 * np.pi * np.cumsum(f) / SR)

# ---------- efeitos: cada um devolve (sinal mono, deslocamento em s do ponto de alinhamento) ----------
def whoosh(r, dur=.48, f0=500, f1=4200, pico=.62):
    """ar passando (giro, corte): ruído com filtro subindo; o PICO cai no tempo do evento"""
    n = int(dur * SR); u = np.linspace(0, 1, n)
    e = np.where(u < pico, (u / pico) ** 2.2, ((1 - u) / (1 - pico)) ** 1.6)
    return norm(bp_var(r.standard_normal(n), f0, f1) * e), -pico * dur
def sopro(r, dur=.55, f0=500, f1=4200, pico=.78):
    """ar que cresce até o corte e some rápido depois (Filme B)"""
    n = int(dur * SR); u = np.linspace(0, 1, n); x = lp(r.standard_normal(n), np.linspace(f0, f1, n)); x = x - lp(x, 150)
    e = np.where(u < pico, (u / pico) ** 2.2, np.exp(-(u - pico) * dur / .05))
    return norm(x * e), -pico * dur
def reverso(r, dur=.6, fim=6500):
    """whoosh invertido: cresce e TERMINA no tempo (clarão, corte seco)"""
    n = int(dur * SR); u = np.linspace(0, 1, n)
    return norm(lp(r.standard_normal(n), 1500 + (fim - 1500) * u ** 3) * u ** 3), -dur
def riser(r, dur=2.0, f0=45, f1=115):
    """subida até o drop: ruído que abre + seno que sobe; para seco no tempo do evento"""
    n = int(dur * SR); u = np.linspace(0, 1, n)
    x = lp(r.standard_normal(n), 400 + 7000 * u ** 2.5) * u ** 2.2 * .5 + seno_var(f0 + (f1 - f0) * u ** 2) * u ** 2 * .35
    return norm(x), -dur
def impacto(r, dur=2.2, sala=.3):
    """hit de título: sub que cai 110 → 38 Hz + estalo + metal grave, com cauda de sala"""
    n = int(dur * SR); t = np.arange(n) / SR
    sub = seno_var(38 + 72 * np.exp(-t / .07)) * env(n, .001, .55)
    crack = lp(r.standard_normal(n), 6000) * env(n, .0005, .025)
    metal = sum(np.sin(2 * np.pi * fr * t + ph) * env(n, .002, dc) for fr, ph, dc in ((92, 0, .7), (143, 1, .5), (211, 2, .35), (317, .5, .25))) * .25
    return norm(reverb(sub + crack * .6 + metal, 2.6, sala, 2500, r)), 0
def subdrop(r, dur=1.2):
    """grave que cai 60 → 30 Hz (fim, corte para o preto)"""
    n = int(dur * SR); t = np.arange(n) / SR
    x = seno_var(30 + 30 * np.exp(-t / .06)) * env(n, .002, .45) + lp(r.standard_normal(n), 300) * env(n, .002, .25) * .2
    return norm(reverb(x, 1.3, .3, 1200, r)), 0
def baque(r, f=52):
    """batida surda (projetor, crédito que entra)"""
    n = int(.5 * SR); x = np.sin(2 * np.pi * f * np.arange(n) / SR) * env(n, .002, .12) + lp(r.standard_normal(n), 1200) * env(n, .001, .03) * .3
    return norm(reverb(x, 1.6, .3, 1800, r)), 0
def acento(r, f=1318.5):
    """número/nome que aparece: pulso grave que cai de tom + sino suave (f, quinta e oitava)"""
    n = int(1.6 * SR); t = np.arange(n) / SR
    x = .9 * seno_var(62 + 40 * np.exp(-t / .05)) * env(n, .003, .32)
    for k, g, d in ((1, .10, .55), (1.5, .05, .4), (2, .025, .25)): x += g * np.sin(2 * np.pi * f * k * t) * env(n, .004, d)
    return norm(x), 0
def tick(r, f=3200):
    """tique seco e agudo (moeda, contador, cota que trava)"""
    n = int(.04 * SR); t = np.arange(n) / SR
    return norm(np.sin(2 * np.pi * f * t) * np.exp(-t / .004) + .5 * np.sin(2 * np.pi * f * 1.7 * t) * np.exp(-t / .002) + np.diff(r.standard_normal(n), prepend=0) * np.exp(-t / .0015) * .2), 0
def tique(r, f=2350):
    """tique mecânico de relógio: clique + ressonância + corpo grave"""
    n = int(.25 * SR); t = np.arange(n) / SR
    return norm(hp(r.standard_normal(n), 3000) * env(n, .0003, .004) + np.sin(2 * np.pi * f * t) * env(n, .0005, .03) * .35 + np.sin(2 * np.pi * 180 * t) * env(n, .001, .02) * .5), 0
def clique(r, solta=.16):
    """botão: aperto (grave + estalo) e soltura mais leve `solta` s depois (0 = só o aperto)"""
    n = int((solta + .14) * SR); t = np.arange(n) / SR
    x = .9 * np.sin(2 * np.pi * 140 * t) * env(n, .001, .018) + .8 * np.sin(2 * np.pi * 2300 * t) * env(n, .0003, .005) + .4 * r.standard_normal(n) * env(n, .0001, .002)
    if solta > 0:
        k = int(solta * SR); m = n - k; t2 = np.arange(m) / SR
        x[k:] += .45 * np.sin(2 * np.pi * 2900 * t2) * env(m, .0003, .004) + .25 * np.sin(2 * np.pi * 180 * t2) * env(m, .001, .012)
    return norm(x), 0
def tap(r):
    """toque de cartão/dedo: 'tuc' grave curto + clique de plástico"""
    n = int(.09 * SR); t = np.arange(n) / SR
    return norm(np.sin(2 * np.pi * (180 - 60 * t / .09) * t) * np.exp(-t / .018) + np.diff(r.standard_normal(n), prepend=0) * np.exp(-t / .0025) * .35), 0
def bip(r, f=1760, dur=.11):
    """bip de confirmação (dois seguidos = aprovado: f e f × 4/3)"""
    n = int(dur * SR); t = np.arange(n) / SR; a = np.minimum(1, t / .004) * np.minimum(1, (dur - t) / .03)
    return norm((np.sin(2 * np.pi * f * t) * .6 + np.sin(4 * np.pi * f * t) * .12) * a), 0
def pouso(r):
    """objeto de metal pousando: 'tum' grave + brilho metálico curto"""
    n = int(.5 * SR); t = np.arange(n) / SR
    g = np.sin(2 * np.pi * (95 - 30 * t) * t) * np.exp(-t / .08)
    m = sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, d in ((2350, .09), (3710, .06), (5230, .04))) * .07
    return norm(g + m), 0
def papel(r):
    """papel/recorte batendo"""
    n = int(.08 * SR); return norm(lp(hp(r.standard_normal(n), 500), 5000) * env(n, .001, .018)), 0
def estalo(r):
    """estalo curto e agudo (faísca, chama)"""
    n = int(.012 * SR); return norm(hp(r.standard_normal(n), 2500) * env(n, .0005, .002)), 0

TIPOS = dict(whoosh=whoosh, sopro=sopro, reverso=reverso, riser=riser, impacto=impacto, hit=impacto, subdrop=subdrop,
             baque=baque, acento=acento, tick=tick, tique=tique, clique=clique, tap=tap, bip=bip, pouso=pouso, papel=papel, estalo=estalo)

def lista():
    import inspect
    for k, f in TIPOS.items():
        if k == 'hit': continue
        ps = [f'{p.name}={p.default}' for p in list(inspect.signature(f).parameters.values())[1:]]
        print(f'  {k:8} {f.__doc__.strip()}' + (f'  [{", ".join(ps)}]' if ps else ''))
    print('  hit      = impacto')

# ---------- limitador (vetorizado: blocos de 1 ms, olha 3 ms à frente, solta em `rel` s) ----------
def limita(x, teto, rel=.08):
    B = 48; nb = -(-len(x) // B); pad = np.zeros((nb * B, x.shape[1])); pad[:len(x)] = np.abs(x)
    pk = pad.reshape(nb, B, -1).max(axis=(1, 2))
    pk = np.maximum.reduce([np.r_[pk[k:], np.zeros(k)] for k in range(4)])          # antecipa 3 blocos
    alvo = np.minimum(1, teto / np.maximum(pk, 1e-9)); g = np.empty(nb); v = 1.0; kr = np.exp(-1 / (rel * 1000))
    for i in range(nb): v = alvo[i] if alvo[i] < v else min(alvo[i], 1 - (1 - v) * kr); g[i] = v
    gs = np.interp(np.arange(len(x)), np.arange(nb) * B, g)
    return x * gs[:, None]

def escreve(saida, x):
    s = np.clip(np.round(x * 8388607), -8388608, 8388607).astype('<i4').tobytes()
    b = np.frombuffer(s, np.uint8).reshape(-1, 4)[:, :3].tobytes()      # 24 bits
    with wave.open(saida, 'wb') as w: w.setnchannels(2); w.setsampwidth(3); w.setframerate(SR); w.writeframes(b)

def gera(cfg, saida):
    bpm, anc = cfg.get('bpm'), cfg.get('ancora', 0)
    tempo = lambda e: e['t'] if 't' in e else anc + e['b'] * 60 / bpm
    evs = cfg['eventos']; dur = cfg.get('dur') or max(tempo(e) for e in evs) + 2.5
    N = int(dur * SR); fx = np.zeros((N, 2)); sem = cfg.get('semente', 1)
    for i, e in enumerate(evs):
        tp = e['tipo']
        if tp not in TIPOS: sys.exit(f'tipo desconhecido: {tp} (veja --lista)')
        extra = {k: v for k, v in e.items() if k not in ('t', 'b', 'tipo', 'g', 'pan')}
        y, des = TIPOS[tp](np.random.default_rng([sem, i]), **extra)
        g, pan = e.get('g', .3), e.get('pan', 0)
        L, R = np.cos((pan + 1) * np.pi / 4) * 1.41, np.sin((pan + 1) * np.pi / 4) * 1.41   # pan de potência constante
        j = int(round((tempo(e) + des) * SR))
        if j < 0: y = y[-j:]; j = 0
        y = y[:max(0, N - j)] * g; fx[j:j + len(y), 0] += y * L; fx[j:j + len(y), 1] += y * R
    fx *= cfg.get('ganho_fx', 1)
    print(f'efeitos: {len(evs)} · pico antes do limitador {20 * np.log10(np.abs(fx).max() + 1e-9):.1f} dBFS')
    mix = fx
    if cfg.get('trilha'):
        a = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f"{cfg.get('inicio', 0):.4f}", '-i', cfg['trilha'], '-t', f'{dur:.4f}',
                            '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
        m = np.frombuffer(a, np.float32).reshape(-1, 2).astype(float); m = np.pad(m, ((0, max(0, N - len(m))), (0, 0)))[:N]
        t = np.arange(N) / SR; so = cfg.get('saida_trilha', 1.0)
        m *= (np.minimum(1, t / .01) * np.clip((dur - t) / so, 0, 1) ** 1.5)[:, None]   # entra em 10 ms, sai em `saida_trilha` s
        mix = m * cfg.get('ganho_trilha', .8) + fx
    teto = 10 ** (cfg.get('pico', -1) / 20)
    mix = limita(mix, teto * .98)
    pk = np.abs(mix).max()
    if pk > teto: mix *= teto / pk          # garantia final
    escreve(saida, mix)
    print(f'ok {saida} · {dur:.3f} s · 48 kHz estéreo 24 bits · pico {20 * np.log10(np.abs(mix).max() + 1e-9):.2f} dBFS')

def main(a):
    if '--lista' in a or not a: lista(); return
    if a[0].endswith('.json'):
        cfg = json.load(open(a[0])); saida = a[1]; a = a[2:]
    else:
        saida = a[0]; a = a[1:]; cfg = {'eventos': []}
    op = lambda n: a[a.index(n) + 1] if n in a else None
    for n, k, f in (('--dur', 'dur', float), ('--pico', 'pico', float), ('--bpm', 'bpm', float), ('--ancora', 'ancora', float), ('--semente', 'semente', int),
                    ('--trilha', 'trilha', str), ('--inicio', 'inicio', float), ('--ganho-trilha', 'ganho_trilha', float), ('--ganho-fx', 'ganho_fx', float)):
        if op(n) is not None: cfg[k] = f(op(n))
    skip = {i + 1 for i, x in enumerate(a) if x.startswith('--')}
    for i, x in enumerate(a):
        if i in skip or x.startswith('--') or '@' not in x: continue
        tp, resto = x.split('@', 1); p = resto.split(':'); e = {'tipo': tp}
        if p[0].startswith('b'): e['b'] = float(p[0][1:])
        else: e['t'] = float(p[0])
        if len(p) > 1 and p[1]: e['g'] = float(p[1])
        if len(p) > 2 and p[2]: e['pan'] = float(p[2])
        cfg['eventos'].append(e)
    if not cfg['eventos']: sys.exit('nenhum evento (ex.: whoosh@1.2 impacto@2:0.9)')
    if any('b' in e for e in cfg['eventos']) and not cfg.get('bpm'): sys.exit('evento em batidas precisa de --bpm')
    gera(cfg, saida)

if __name__ == '__main__':
    main(sys.argv[1:])
