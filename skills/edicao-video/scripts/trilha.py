"""Ajusta a trilha para ficar SEMPRE pelo menos N dB abaixo da voz nos trechos com fala (só abaixa, nunca sobe).
uso: python trilha.py voz.wav trilha.wav palavras-final.json saida.wav [--alvo 30] [--folga 1]
Regra do dono (16/10/2026): música 30 dB abaixo da voz. Uma trilha de volume fixo fica a 30 dB na média, mas onde a voz é mais
baixa a distância cai para 27–28 dB. Aqui, a cada 0,25 s, mede voz e trilha em janelas de 3 s com fala e, onde a distância
ficaria menor que alvo − folga, abaixa a trilha só ali (curva suavizada em ~1,5 s, sem "bombear"). Fora da fala (fechamento,
pausas) não mexe. Confira depois com revisao-video/scripts/trilha_voz.py."""
import sys, json, subprocess
import numpy as np
a = sys.argv[1:]; VOZ, TRI, PAL, SAI = a[0], a[1], a[2], a[3]
op = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
ALVO, FOLGA = op('--alvo', 30), op('--folga', 1)
SR = 48000
def le(p, ch):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch)
v = le(VOZ, 1)[:, 0]; m = le(TRI, 2).copy(); n = len(m)
v = np.pad(v, (0, max(0, n - len(v))))[:n]   # a trilha manda no tamanho (fechamento sem fala continua)
mm = m.mean(1)
fala = np.zeros(int(n / SR * 10) + 2, bool)
for w in json.load(open(PAL)): fala[int(w['t'] * 10):int(w.get('e', w['t'] + .3) * 10) + 1] = True
db = lambda x: 10 * np.log10(np.mean(x ** 2) + 1e-12)
passo = .25; T = np.arange(0, n / SR, passo); g = np.zeros(len(T))   # ganho extra (dB, ≤ 0) por passo
for i, t in enumerate(T):
    a0, a1 = max(0, t - 1.5), min(n / SR, t + 1.5)
    if fala[int(a0 * 10):int(a1 * 10)].mean() < .4: continue
    i0, i1 = int(a0 * SR), int(a1 * SR)
    dist = db(v[i0:i1]) - db(mm[i0:i1])
    if dist < ALVO + FOLGA: g[i] = max(-8.0, dist - (ALVO + FOLGA))   # no máximo 8 dB: evita buraco onde a voz some (fim da fala)
# suaviza: mínimo numa janela de ±0,75 s, depois média de ±0,75 s (desce antes, sobe devagar)
k = int(.75 / passo)
gm = np.array([g[max(0, i - k):i + k + 1].min() for i in range(len(g))])
gs = np.convolve(gm, np.ones(2 * k + 1) / (2 * k + 1), mode='same')
gan = 10 ** (np.interp(np.arange(n) / SR, T, gs) / 20)
m *= gan[:, None]
import wave
with wave.open(SAI, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(m, -1, 1) * 32767).astype('<i2').tobytes())
print(f'trilha ajustada: {int((gs < -.1).sum() * passo)} s abaixados (até {gs.min():.1f} dB) → {SAI}')
