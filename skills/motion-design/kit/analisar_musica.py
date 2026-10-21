"""Analisa uma trilha para a cena dançar com ela: batidas, compassos, onsets, energia por quadro e seções.
uso: .ferramentas/.venv/bin/python analisar_musica.py faixa.mp3 [--inicio 41.1] [--dur 14] [--bpm 105] [--fps 30] [-o saida.json]
  Sem -o, grava <faixa>.musica.json. Grava também <saida>.js (window.MUSICA_DADOS = {...}) para a cena carregar com <script src>,
  porque a página aberta por file:// não pode fazer fetch de JSON. A cena NUNCA analisa áudio ao vivo: só lê este arquivo.
  Tempos no JSON são TEMPO DA CENA (0 = --inicio na faixa). `inicio` guarda o corte para o montar.py/ffmpeg (-ss inicio -t dur).

O que sai (tudo pré-calculado, determinístico):
  bpm, batida (s), batidas[]            grade uniforme (faixa produzida tem tempo fixo) ajustada nos bumbos do trecho
  forca[]                               força de cada batida 0–1 (grave + fluxo), para saber qual batida "pesa"
  compassos[]                           batidas "1" (downbeat), escolhidas pela fase de 4 com mais grave e mais virada de energia
  onsets[] = [[t, forca], ...]          ataques (caixa, prato, nota) — para entrada de palavra fora da grade
  energia[] (1 por quadro, 0–1)         RMS em dB normalizado no trecho (p5→0, p95→1), suavizado ~100 ms; grave[] idem só < 150 Hz
  secoes[] = [{ini, fim, tipo, nivel}]  tipo: intro | sobe | drop | cheio | respiro | fim (energia por compasso, ver abaixo)
  drops[], respiros[]                   instantes (s) em que a música cai pesada / abre espaço
  lufs, energia_db_compasso[]           para conferência
Regra das seções (por compasso, dB RMS): cada compasso é alto ou baixo (meio entre p20 e p80, histerese 1 dB, compasso
isolado não conta); intro = baixo do começo; fim = baixo do final; respiro = baixo no meio; cheio = alto; drop = 1º compasso
alto que sobe ≥ 3 dB sobre os 2 anteriores (regra do batidas.py); sobe = fim de um trecho baixo crescendo ≥ 2 dB até o alto.
Faixa sem dinâmica (p90−p10 < 4 dB, lo-fi em loop) vira um "cheio" só. É energia, não harmonia: confira no ouvido.
--conferir: roda também o beat_this (rede neural, MIT, ~6 s) só para conferir o compasso; avisa se discordar.
"""
import sys, json, subprocess, re, os
import numpy as np
import librosa

a = sys.argv[1:]
if not a or a[0].startswith('-'): print(__doc__); sys.exit(1)
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
faixa = a[0]; ini = float(op('--inicio', 0)); dur = op('--dur'); FPS = int(op('--fps', 30)); bpm_forcado = op('--bpm')
saida = op('-o') or op('--saida') or os.path.splitext(faixa)[0] + '.musica.json'
SR = 22050; HOP = 512

y_all, _ = librosa.load(faixa, sr=SR, mono=True)
total = len(y_all) / SR
fim = min(total, ini + float(dur)) if dur else total
# a grade (período e fase) sai da FAIXA INTEIRA: música produzida tem tempo fixo, e o trecho sozinho engana — numa intro
# sem bumbo o baixo de contratempo puxa a fase meia batida (filme-a: trecho 5,7–19,7 s deu a grade no contratempo).
# Depois a fase e o período são polidos só no trecho (±40 ms, ±0,3 %). Tudo que sai é do trecho.
m0 = 0.; m1 = total
y = y_all[int(m0 * SR):int(m1 * SR)]

# ---------- envelopes ----------
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=HOP))
fq = librosa.fft_frequencies(sr=SR, n_fft=2048)
env = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S, ref=np.max), sr=SR, hop_length=HOP)
low = S[fq < 150].sum(0)
lowon = np.maximum(0, np.diff(np.log1p(low), prepend=np.log1p(low[0])))
tt = librosa.frames_to_time(np.arange(len(env)), sr=SR, hop_length=HOP) + m0     # tempo absoluto na faixa

# ---------- tempo e grade ----------
if bpm_forcado: bpm0 = float(bpm_forcado)
else:
    bpm0 = float(np.atleast_1d(librosa.feature.tempo(onset_envelope=env, sr=SR, hop_length=HOP, start_bpm=120, prior=None))[0])
    while bpm0 < 75: bpm0 *= 2           # metade/dobro: preferimos 75–160 (o batidas.py prefere 95–165)
    while bpm0 > 165: bpm0 /= 2
_, bt = librosa.beat.beat_track(onset_envelope=env, sr=SR, hop_length=HOP, bpm=bpm0, tightness=400, units='time')
bt = bt + m0
# alvo de ajuste: bumbo (grave) + fluxo geral, interpolado em tempo contínuo
alvo = lowon / (lowon.max() + 1e-9) + .5 * env / (env.max() + 1e-9)
amostra = lambda ts: np.interp(ts, tt, alvo)
per = 60 / bpm0
if len(bt) >= 4 and not bpm_forcado:      # regressão linear das batidas do librosa = período médio sem deriva
    k = np.round((bt - bt[0]) / per); A = np.vstack([k, np.ones_like(k)]).T; per = float(np.linalg.lstsq(A, bt, rcond=None)[0][0])
ph = float(bt[0]) if len(bt) else ini
# refino: ataque do grave em resolução fina (janela 1024, passo 64 amostras ≈ 2,9 ms, como o batidas.py) + fluxo geral.
# Busca conjunta período × fase na faixa inteira (±4 % em volta do tempo do librosa, que erra 2–3 % às vezes).
hf_ = 64; w_ = 1024
fr_ = np.lib.stride_tricks.sliding_window_view(y, w_)[::hf_]
F_ = np.abs(np.fft.rfft(fr_ * np.hanning(w_), axis=1)); fqw = np.fft.rfftfreq(w_, 1 / SR)
lg = np.log1p(F_[:, fqw < 150].sum(1)); on_lo = np.maximum(0, np.diff(lg, prepend=lg[0]))
lf = np.log1p(F_); on_all = np.r_[0, np.maximum(0, np.diff(lf, axis=0)).sum(1)]
fino = on_lo / (np.percentile(on_lo, 99.5) + 1e-9) + .35 * on_all / (np.percentile(on_all, 99.5) + 1e-9)
t_fino = m0 + (np.arange(len(fino)) * hf_ + w_ / 2) / SR      # centro da janela
r0, r1 = m0, m1
def notas(phs, per_):   # phs: vetor de fases → soma do alvo fino na grade dentro de [r0, r1]
    k = np.arange(np.floor((r0 - phs.max()) / per_), np.ceil((r1 - phs.min()) / per_) + 1)
    T = phs[:, None] + k[None, :] * per_; v = np.interp(T, t_fino, fino); v[(T < r0) | (T > r1)] = 0
    return v.sum(1)
pers = [per] if bpm_forcado else 60 / np.arange(bpm0 * .96, bpm0 * 1.04, .02)
best = (-1, ph, per)
for q in pers:
    phs = np.arange(0, q, .003); sc = notas(phs, q); i = int(np.argmax(sc))
    if sc[i] > best[0]: best = (float(sc[i]), float(phs[i]), float(q))
_, ph, per = best
ph_g, per_g = ph, per                             # grade da faixa inteira (para achar o compasso)
r0, r1 = max(m0, ini - 2), min(m1, fim + 2)   # polimento no trecho usado (+2 s de cada lado)
ph = ph + per * np.round((ini - ph) / per)        # âncora da fase perto do trecho (o período polido não arrasta a grade)
for _ in range(2):   # polimento: fase em 1 ms (±40 ms), período em ±0,3 %
    phs = ph + np.arange(-.04, .04, .001); ph = float(phs[np.argmax(notas(phs, per))])
    if not bpm_forcado:
        qs = per * np.linspace(.997, 1.003, 121); per = float(qs[np.argmax([notas(np.array([ph]), q)[0] for q in qs])])
# o grave do bumbo sobe ~10–20 ms depois do clique do ataque; a janela de 1024 centrada já compensa quase tudo
k0 = np.ceil((ini - .035 - ph) / per); b0 = ph + k0 * per   # batida até ~1 quadro antes do corte conta como a 1ª (vira 0)
batidas_abs = b0 + per * np.arange(0, int(np.floor((fim - b0) / per)) + 1)
batidas_abs = batidas_abs[batidas_abs < fim]
bpm = 60 / per

# força de cada batida: grave + fluxo na janela de ±40 ms
def pico(ts, w=.04):
    out = []
    for x in ts:
        m = (tt >= x - w) & (tt <= x + w); out.append(float(alvo[m].max()) if m.any() else 0.)
    return np.array(out)
forca = pico(batidas_abs); forca = forca / (forca.max() + 1e-9)

# ---------- compasso (qual das 4 fases é o "1") ----------
# grave médio por fase + virada de energia (RMS do compasso que começa ali contra o anterior): o "1" ganha nas duas
rms_all = librosa.feature.rms(y=y, frame_length=2048, hop_length=HOP)[0]
db_all = 20 * np.log10(rms_all + 1e-9)
def db_entre(t0, t1):
    m = (tt >= t0) & (tt < t1); return float(db_all[m].mean()) if m.any() else -90.
# fase do compasso: usa as batidas da janela de análise inteira (com folga) para ter mais compassos
grade_ext = ph_g + per_g * np.arange(np.ceil((m0 - ph_g) / per_g), np.floor((m1 - ph_g) / per_g) + 1)
# a grade local (polida) e a global diferem poucos ms no trecho: casa o "1" pela batida global mais próxima
lw = pico(grade_ext, .05)
# o "1" do compasso: onde o acorde muda (croma da batida contra a anterior) + onde o grave pesa (z-scores, grave vale meio).
# Testado: filme-a (3 da grade, confere com as notas do 01-filme-a), filme-b (0, confere), cine-02 (confere com o beat_this).
Cr = librosa.feature.chroma_stft(S=S ** 2, sr=SR)
frg = np.clip(np.searchsorted(tt, grade_ext), 0, Cr.shape[1] - 1)
Cb = np.array([Cr[:, frg[i]:max(frg[i] + 1, frg[i + 1])].mean(1) for i in range(len(grade_ext) - 1)])
Cb /= np.linalg.norm(Cb, axis=1, keepdims=True) + 1e-9
mud = np.r_[0, 1 - (Cb[1:] * Cb[:-1]).sum(1)]
zz = lambda v: (np.array(v) - np.mean(v)) / (np.std(v) + 1e-9)
g4 = [lw[f::4].mean() for f in range(4)]; c4 = [mud[f::4][1:].mean() for f in range(4)]
sc4 = zz(c4) + .5 * zz(g4)
melhor = (float(sc4.max()), int(np.argmax(sc4)))
fase = melhor[1]
uno = grade_ext[fase::4]
compassos_abs = np.array([b for b in batidas_abs if np.min(np.abs(uno - b)) < per / 2])

# ---------- onsets ----------
on_f = librosa.onset.onset_detect(onset_envelope=env, sr=SR, hop_length=HOP, backtrack=False, delta=.12, wait=4)
on_t = librosa.frames_to_time(on_f, sr=SR, hop_length=HOP) + m0
on_s = env[on_f] / (np.percentile(env, 99.5) + 1e-9)
sel = (on_t >= ini) & (on_t < fim)
onsets = [[round(float(t - ini), 3), round(float(min(1, s)), 2)] for t, s in zip(on_t[sel], on_s[sel])]

# ---------- energia por quadro (fps da cena) ----------
nq = int(np.ceil((fim - ini) * FPS))
seg = y_all[int(ini * SR):int(fim * SR)]
hq = SR / FPS
def curva(sinal):
    v = np.array([np.sqrt(np.mean(sinal[int(i * hq):int((i + 1) * hq)] ** 2) + 1e-12) if int(i * hq) < len(sinal) else 1e-6 for i in range(nq)])
    d = 20 * np.log10(v + 1e-9)
    d = np.convolve(np.pad(d, 1, mode='edge'), np.ones(3) / 3, 'valid')   # ~100 ms
    lo, hi = np.percentile(d, 5), np.percentile(d, 95)
    return np.clip((d - lo) / (hi - lo + 1e-9), 0, 1), d
energia, energia_db = curva(seg)
# grave: passa-baixa simples por FFT
Fseg = np.fft.rfft(seg); fr = np.fft.rfftfreq(len(seg), 1 / SR); Fseg[fr > 150] = 0
grave, _ = curva(np.fft.irfft(Fseg, len(seg)))

# ---------- seções por compasso ----------
# compassos que cobrem o trecho (inclui o pedaço antes do 1º "1")
bordas = list(compassos_abs)
if not bordas or bordas[0] > ini + .05: bordas = [ini] + bordas
bordas = bordas + [fim]
if len(bordas) > 2 and bordas[1] - bordas[0] < per * .9: del bordas[1]   # pedacinho antes do 1º "1" entra no 1º compasso
if len(bordas) > 2 and bordas[-1] - bordas[-2] < per * .9: del bordas[-2]
E = np.array([db_entre(bordas[i], bordas[i + 1]) for i in range(len(bordas) - 1)])
nb = len(E)
# nível por compasso: alto/baixo com histerese de 1 dB em volta do meio entre p20 e p80; compasso isolado (1 só) não muda o nível
lim = (np.percentile(E, 20) + np.percentile(E, 80)) / 2 if nb else 0
faixa_din = float(np.percentile(E, 90) - np.percentile(E, 10)) if nb else 0
L = np.zeros(nb, int); est = int(E[0] >= lim + .5) if nb else 0
for i in range(nb):
    if est == 0 and E[i] >= lim + .5: est = 1
    elif est == 1 and E[i] <= lim - .5: est = 0
    L[i] = est
for i in range(1, nb - 1):
    if L[i - 1] == L[i + 1] != L[i]: L[i] = L[i - 1]
if faixa_din < 4: L[:] = 1                      # música sem dinâmica (lo-fi em loop): tudo "cheio", sem drop inventado
tipo = ['cheio' if v else 'respiro' for v in L]
# intro: o começo baixo; fim: o último trecho baixo
i = 0
while i < nb and L[i] == 0: tipo[i] = 'intro'; i += 1
j = nb - 1
while j > i and L[j] == 0: tipo[j] = 'fim'; j -= 1
if i == nb and nb: tipo = ['intro'] * nb      # trecho todo baixo
# drop: 1º compasso de um trecho alto que subiu ≥ 3 dB sobre os 2 anteriores (mesma regra do batidas.py)
for k in range(1, nb):
    if L[k] == 1 and L[k - 1] == 0 and E[k] - E[max(0, k - 2):k].mean() >= 3: tipo[k] = 'drop'
# sobe: fim de um trecho baixo que vem crescendo (cada compasso ≥ o anterior − 0,5 dB, total ≥ 2 dB) até um trecho alto
for k in range(1, nb):
    if L[k] == 1 and L[k - 1] == 0:
        j = k - 1
        while j >= 1 and L[j - 1] == 0 and E[j - 1] <= E[j] + .5: j -= 1
        if E[k - 1] - E[j] >= 2:
            for q in range(max(j, 1 if tipo[0] == 'intro' else 0), k): tipo[q] = 'sobe'
# junta compassos vizinhos do mesmo tipo (drop fica de 1 compasso: é o impacto; o platô depois dele é "cheio")
secoes = []
for i in range(nb):
    t0, t1 = bordas[i] - ini, bordas[i + 1] - ini
    if secoes and secoes[-1]['tipo'] == tipo[i] and tipo[i] != 'drop':
        secoes[-1]['fim'] = round(t1, 3); secoes[-1]['_e'].append(E[i])
    else: secoes.append({'ini': round(max(0, t0), 3), 'fim': round(t1, 3), 'tipo': tipo[i], '_e': [E[i]]})
lo, hi = (E.min(), E.max()) if nb else (0, 1)
for s in secoes: s['nivel'] = round(float((np.mean(s.pop('_e')) - lo) / (hi - lo + 1e-9)), 2)

# conferência opcional do compasso com o beat_this (rede neural, MIT): --conferir. Só avisa; a grade continua a nossa.
confere = None
if '--conferir' in a:
    try:
        from beat_this.inference import Audio2Beats
        bt_b, bt_d = Audio2Beats(checkpoint_path='final0', device='cpu', dbn=False)(y, SR)
        bt_b = bt_b + m0; bt_d = bt_d + m0
        G = grade_ext; offs = [x - G[np.argmin(abs(G - x))] for x in bt_b]; off = float(np.median(offs)) if offs else 0
        votos = np.bincount([int(np.argmin(abs(G - (x - off)))) % 4 for x in bt_d], minlength=4)
        fase_bt = int(np.argmax(votos)); confere = {'fase_beat_this': fase_bt, 'fase_nossa': fase, 'votos': votos.tolist(), 'desvio_batida_ms': round(off * 1000)}
        print(f"  beat_this: compasso {'CONFERE' if fase_bt == fase else 'DIFERENTE (ouça e, se for o caso, troque os compassos)'} · votos {votos.tolist()} · batidas dele {off*1000:+.0f} ms da nossa grade")
    except Exception as e: print('  beat_this indisponível:', e)

lu = subprocess.run(['ffmpeg', '-v', 'info', '-ss', str(ini), '-t', str(fim - ini), '-i', faixa, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = re.findall(r'I:\s+(-?[\d.]+) LUFS', lu); I = float(I[-1]) if I else None

r3 = lambda v: [round(float(x), 3) for x in v]
R = {'arquivo': os.path.basename(faixa), 'inicio': round(ini, 3), 'dur': round(fim - ini, 3), 'fps': FPS,
     'bpm': round(bpm, 3), 'batida': round(per, 5), 'batida0_abs': round(float(batidas_abs[0]), 4) if len(batidas_abs) else None,
     'batidas': r3(np.maximum(0, batidas_abs - ini)), 'forca': [round(float(x), 2) for x in forca],
     'compassos': r3(np.maximum(0, compassos_abs - ini)), 'fase_compasso': int(np.argmin(np.abs(batidas_abs - compassos_abs[0]))) if len(compassos_abs) and len(batidas_abs) else 0,
     'onsets': onsets, 'energia': [round(float(x), 3) for x in energia], 'grave': [round(float(x), 3) for x in grave],
     'secoes': secoes, 'drops': [s['ini'] for s in secoes if s['tipo'] == 'drop'], 'respiros': [s['ini'] for s in secoes if s['tipo'] == 'respiro'],
     'faixa_dinamica_db': round(faixa_din, 1), 'compasso_beat_this': confere, 'lufs': I, 'energia_db_compasso': [round(float(e), 1) for e in E]}
os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
json.dump(R, open(saida, 'w'), separators=(',', ':'))
js = os.path.splitext(saida)[0] + '.js'
open(js, 'w').write('window.MUSICA_DADOS=' + json.dumps(R, separators=(',', ':')) + ';\n')
print(f"{os.path.basename(faixa)} [{ini:.2f}–{fim:.2f}s]: {bpm:.2f} BPM · 1ª batida {R['batida0_abs']}s (abs) · {len(R['batidas'])} batidas · "
      f"{len(R['compassos'])} compassos · {len(onsets)} onsets · {I} LUFS")
print('  seções:', ' | '.join(f"{s['tipo']} {s['ini']:.1f}–{s['fim']:.1f} ({s['nivel']:.2f})" for s in secoes))
print('  dB/compasso:', ' '.join(f'{e:.0f}' for e in E))
if not bpm_forcado: print(f'  confira o bumbo: em batida sincopada (3-3-2) o tempo real costuma ser 3/4 = {bpm*.75:.1f} BPM (aí rode com --bpm)')
print('  →', saida, '+', js)
