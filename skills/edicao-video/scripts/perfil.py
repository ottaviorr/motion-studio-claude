"""Volume do áudio a cada 20 ms em volta de um ponto — para achar a borda exata de um corte.
uso: python perfil.py bruto.mp4 70.6 84.1 [--janela 0.4]
Mostra, para cada tempo pedido, linhas "tempo  dB  ####". Silêncio ≈ abaixo de -60 dB; -120 = noise gate fechado (silêncio digital).
Regra: o corte começa no silêncio depois da última palavra que fica e termina no silêncio antes da próxima palavra que fica.
Quando não há silêncio (ex.: "é" arrastado colado na palavra), use o vale mais fundo e marque o corte como "exato"."""
import sys, subprocess
import numpy as np
a = sys.argv[1:]; arq = a[0]
jan = float(a[a.index('--janela') + 1]) if '--janela' in a else .4
ts = [float(x) for x in a[1:] if not x.startswith('--') and x != str(jan)]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', arq, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
au = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
for t0 in ts:
    print(f'== {t0}')
    for t in np.arange(max(0, t0 - jan), t0 + jan, .02):
        i = int(t * 16000); d = 20 * np.log10(np.sqrt((au[i:i + 320] ** 2).mean() + 1e-12))
        print(f'{t:8.2f} {d:6.0f} ' + '#' * int(max(0, d + 60) / 2) + ('   ◀' if abs(t - t0) < .01 else ''))
