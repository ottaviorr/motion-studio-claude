"""Entrega para o YouTube: capítulos da descrição + legenda .srt (para enviar, não queimada).
uso: python capitulos.py fonte/edicao.json [--introducao "Introdução"]
  → <pasta do vídeo>/capitulos-youtube.txt  (começa em 00:00, ≥ 3 capítulos, cada um ≥ 10 s — regra do YouTube)
  → <pasta do vídeo>/legenda.srt            (de palavras-final.json: até 42 caracteres por linha, 2 linhas, 1–6 s por bloco)
Os nomes são os mesmos dos capítulos na tela ("capitulos" do edicao.json)."""
import sys, os, json
a = sys.argv[1:]; cfg = os.path.abspath(a[0]); base = os.path.dirname(cfg); C = json.load(open(cfg))
INTRO = a[a.index('--introducao') + 1] if '--introducao' in a else 'Introdução'
pasta = os.path.dirname(os.path.normpath(os.path.join(base, C.get('saida', '../editado.mp4'))))
mmss = lambda t: f'{int(t // 60):02d}:{int(t % 60):02d}'

caps = sorted([(float(t), txt) for t, _, txt in C.get('capitulos', [])])
if not caps or caps[0][0] > 0.5: caps = [(0.0, INTRO)] + caps
junto = [caps[0]]
for t, txt in caps[1:]:
    if t - junto[-1][0] < 10: junto[-1] = (junto[-1][0], junto[-1][1] + ' · ' + txt)   # capítulo < 10 s: junta com o anterior
    else: junto.append((t, txt))
if len(junto) < 3: print('aviso: o YouTube só mostra capítulos com ≥ 3 marcas')
open(os.path.join(pasta, 'capitulos-youtube.txt'), 'w').write('\n'.join(f'{mmss(t)} {txt}' for t, txt in junto) + '\n')

W = json.load(open(os.path.join(base, 'palavras-final.json')))
def ts(t): h, r = divmod(t, 3600); m, s = divmod(r, 60); return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}'
blocos, cur = [], []
for w in W:
    cur.append(w); txt = ' '.join(x['w'] for x in cur); d = w.get('e', w['t'] + .3) - cur[0]['t']
    fim_frase = w['w'][-1:] in '.?!'
    if len(txt) > 70 or d > 5.5 or (fim_frase and d > 1.0): blocos.append(cur); cur = []
if cur: blocos.append(cur)
linhas = []
for i, b in enumerate(blocos, 1):
    txt = ' '.join(x['w'] for x in b); t0 = b[0]['t']; t1 = max(t0 + 1.0, b[-1].get('e', b[-1]['t'] + .3))
    if len(txt) > 42:   # quebra em 2 linhas perto do meio
        ws = txt.split(); meio = len(txt) / 2; acc = 0
        for j, x in enumerate(ws):
            acc += len(x) + 1
            if acc >= meio: txt = ' '.join(ws[:j + 1]) + '\n' + ' '.join(ws[j + 1:]); break
    linhas.append(f'{i}\n{ts(t0)} --> {ts(t1)}\n{txt}\n')
open(os.path.join(pasta, 'legenda.srt'), 'w').write('\n'.join(linhas))
print(open(os.path.join(pasta, 'capitulos-youtube.txt')).read() + f'{len(linhas)} blocos de legenda → {pasta}/legenda.srt')
