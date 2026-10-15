"""Gera tempos.js e plano.json a partir da transcrição da voz (palavras.json).
uso (na pasta motion/vsl): python3 fonte/gerar-plano.py
Cada cena começa numa palavra (índice global em INICIO). O clipe da cena k vai de (início − X/2) até
(início da cena seguinte + X/2), para sobrar meia transição de cada lado. A última cena ganha CAUDA s
depois do fim da voz (chamada final). Nas cenas, use W('palavra') do marca.js para pegar o tempo de cada palavra."""
import json, pathlib, subprocess
F = pathlib.Path(__file__).parent
W = json.load(open(F / 'palavras.json'))
X = 0.5           # duração da transição entre cenas (xfade)
CAUDA = 4.6       # segundos de tela depois da última palavra (CTA)
FIM_VOZ = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(F.parent/'voz.mp3')],capture_output=True,text=True).stdout or 0)  # duração do voz.mp3
# índice da 1ª palavra de cada cena (ver palavras.txt)
INICIO = {'01': 0, '02': 18, '03': 33}   # TROQUE: cena → índice da 1ª palavra (veja palavras.txt)
ks = list(INICIO)
plano, tempos = {}, {}
for i, k in enumerate(ks):
    ini = W[INICIO[k]]['t']
    fim_pal = INICIO[ks[i + 1]] if i + 1 < len(ks) else len(W)
    a = 0.0 if i == 0 else round(ini - X / 2, 3)
    b = round(W[INICIO[ks[i + 1]]]['t'] + X / 2, 3) if i + 1 < len(ks) else round(FIM_VOZ + CAUDA, 3)
    plano[k] = {'in': a, 'out': b}
    # palavras da cena com o tempo relativo ao começo do clipe
    tempos[k] = [[w['w'], round(w['t'] - a, 3)] for w in W[INICIO[k]:fim_pal]]
(F / 'tempos.js').write_text('// Gerado por gerar-plano.py a partir da voz real. Não editar à mão.\n'
                             f'window.PLANO={json.dumps(plano)};\nwindow.PALAVRAS={json.dumps(tempos, ensure_ascii=False)};\n')
json.dump({'X': X, 'clips': [{'k': k, **plano[k]} for k in ks]}, open(F / 'plano.json', 'w'), indent=1)
(F / 'palavras.txt').write_text(' '.join(f"{i}:{w['w']}@{w['t']:.2f}" for i, w in enumerate(W)))
for k in ks:
    print(k, plano[k], round(plano[k]['out'] - plano[k]['in'], 2), 's')
