"""Analisa uma trilha: BPM, grade de batidas (fase do bumbo), energia por compasso e drops.
uso: python batidas.py faixa.mp3 [--json saida.json]"""
import sys, json, subprocess, numpy as np
f = sys.argv[1]; sr = 22050
a = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-f','s16le','-ac','1','-ar',str(sr),'-'],capture_output=True).stdout,np.int16).astype(np.float32)/32768
h = 256; fps = sr/h; n = len(a)//h
S = np.abs(np.fft.rfft(a[:n*h].reshape(n,h)*np.hanning(h),axis=1)); fq = np.fft.rfftfreq(h,1/sr)
low = S[:, fq<150].sum(1); flux = np.maximum(0, np.diff(np.log1p(S),axis=0)).sum(1); flux = np.r_[0, flux]
lowf = np.maximum(0, np.diff(np.log1p(low), prepend=0))
# BPM: autocorrelação do fluxo, 70–180 BPM, preferindo 100–160
x = flux - flux.mean(); ac = np.correlate(x, x, 'full')[len(x)-1:]
best = None
for bpm in np.arange(70, 180, .05):
    L = 60/bpm*fps; i0 = int(L); fr_ = L-i0
    v = ac[i0]*(1-fr_)+ac[i0+1]*fr_; v2 = ac[int(2*L)] if int(2*L)<len(ac) else 0
    sc = v + .5*v2 + (0.15*ac[0]*0 )
    if 95 <= bpm <= 165: sc *= 1.08
    if best is None or sc > best[0]: best = (sc, bpm)
bpm = best[1]
# refina o período por ajuste linear dos picos do bumbo e acha a fase
per = 60/bpm
def score(ph, per):
    k = np.arange(0, (len(a)/sr-ph)/per); idx = np.round((ph+k*per)*fps).astype(int); idx = idx[idx < len(lowf)]
    return lowf[idx].sum() + .5*flux[idx].sum()/flux.max()*lowf.max()
for _ in range(2):
    phs = np.arange(0, per, 1/fps); ph = phs[np.argmax([score(p, per) for p in phs])]
    pers = per*np.linspace(.995, 1.005, 81); per = pers[np.argmax([score(ph, q) for q in pers])]
bpm = 60/per
# energia por compasso (dB) e grave por compasso
bar = 4*per; nb = int((len(a)/sr-ph)//bar)
E = []; G = []
for b in range(nb):
    s0, s1 = int((ph+b*bar)*sr), int((ph+(b+1)*bar)*sr); seg = a[s0:s1]
    E.append(20*np.log10(np.sqrt((seg**2).mean())+1e-9)); i0, i1 = int((ph+b*bar)*fps), int((ph+(b+1)*bar)*fps); G.append(float(np.log10(low[i0:i1].mean()+1e-9)))
E = np.array(E); G = np.array(G)
# drops: compasso cuja energia sobe ≥ 3 dB em relação à média dos 2 anteriores
drops = [int(b) for b in range(2, nb) if E[b] - E[b-2:b].mean() >= 3 and G[b] - G[b-2:b].mean() >= .15]
punch = float(np.percentile(lowf, 99.5) / (np.median(lowf)+1e-9))
lu = subprocess.run(['ffmpeg','-v','info','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
import re; I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', lu)[-1])
r = {'arquivo': f, 'bpm': round(bpm, 3), 'batida0': round(float(ph), 4), 'compasso': round(bar, 4), 'lufs': I, 'punch': round(punch,1),
     'drops_compasso': drops, 'drops_s': [round(ph+b*bar, 3) for b in drops], 'energia_db': [round(float(e),1) for e in E],
     'faixa_dinamica_db': round(float(np.percentile(E,90)-np.percentile(E,10)),1)}
if '--json' in sys.argv: json.dump(r, open(sys.argv[sys.argv.index('--json')+1],'w'), indent=1)
print(f"{f}: {r['bpm']} BPM · batida0 {r['batida0']}s · {I} LUFS · punch {r['punch']} · dinâmica {r['faixa_dinamica_db']} dB · drops {r['drops_s']}")
print('   energia/compasso:', ' '.join(f'{e:.0f}' for e in E))
