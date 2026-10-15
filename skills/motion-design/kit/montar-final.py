"""Monta a VSL final: cenas com transição sobreposta (xfade) no ritmo da voz + narração + legenda .srt.
uso (na pasta motion/vsl): python3 fonte/montar-final.py
Lê fonte/plano.json (in/out de cada clipe, gerado por gerar-plano.py), fonte/palavras.json e voz.mp3.
Saídas: VSL-final.mp4 (1080p), VSL-web.mp4 (720p leve, para o site) e VSL-legenda.srt."""
import json, subprocess, pathlib, re
P = json.load(open('fonte/plano.json')); X = P['X']; clips = P['clips']
# transição na entrada de cada cena: dentro do mesmo app desliza para o lado (como navegar);
# nas viradas de assunto, círculo ou zoom. 04→05 é contínua (mesmo enquadramento), por isso fade.
TRANS = {}   # TROQUE: '05': 'smoothleft', '06': 'circleopen'… (sem entrada = 'fade')
arq = {c['k']: next(pathlib.Path('.').glob(f"{c['k']}-*.mp4")) for c in clips}

# ---------- legenda ----------
W = json.load(open('fonte/palavras.json'))
FORA = set()   # índices de palavras que o Whisper inventou (duração zero, tempos repetidos): ficam fora da legenda
CORR = {'Chat': 'ChatGPT', 'GPT': ''}   # TROQUE: como o Whisper escreveu → como deve sair na legenda ('' apaga)
pal = []
for i, w in enumerate(W):
    if i in FORA: continue
    s = w['w']
    if s in CORR: s = CORR[s]
    if s.startswith('.') and pal:            # app .suagência .com .br / 1 .000 / R $
        pal[-1][0] += s; pal[-1][2] = w['e']; continue
    if s == '$' and pal and pal[-1][0] == 'R':
        pal[-1][0] = 'R$'; pal[-1][2] = w['e']; continue
    if s in ('', ','):
        if s == ',' and pal: pal[-1][0] += ','
        continue
    if pal and pal[-1][0] == 'R$' and re.match(r'^\d', s):
        pal[-1][0] += ' ' + s; pal[-1][2] = w['e']; continue
    pal.append([s, w['t'], w['e']])
pal[0][0] = pal[0][0]
leg, cur = [], []
for k, (s, a, b) in enumerate(pal):
    cur.append((s, a, b)); txt = ' '.join(x[0] for x in cur)
    fim = s.endswith(('.', '?', ':')) or (s.endswith(',') and len(txt) > 22) or len(txt) > 40
    if fim or k == len(pal) - 1:
        leg.append([txt, cur[0][1], cur[-1][2]]); cur = []
# junta pedaço solto ("por trás.", "pra sempre.") à linha de cima quando cabe
jun = []
for l in leg:
    if jun and len(l[0].split()) <= 2 and not jun[-1][0].endswith(('.', '?', ':')) and len(jun[-1][0]) + len(l[0]) <= 54:
        jun[-1][0] += ' ' + l[0]; jun[-1][2] = l[2]
    else: jun.append(l)
leg = jun
for i in range(1, len(leg)):
    if leg[i - 1][0].endswith(('.', '?')): leg[i][0] = leg[i][0][0].upper() + leg[i][0][1:]
for i in range(len(leg) - 1):
    leg[i][2] = min(leg[i][2] + .35, leg[i + 1][1])
fmt = lambda s: f"{int(s // 3600):02}:{int(s % 3600 // 60):02}:{int(s % 60):02},{int(round(s % 1 * 1000)) % 1000:03}"
pathlib.Path('VSL-legenda.srt').write_text(''.join(f"{i + 1}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n" for i, (t, a, b) in enumerate(leg)), encoding='utf-8')

# ---------- vídeo ----------
cmd = ['ffmpeg', '-v', 'error', '-y']
for c in clips: cmd += ['-i', str(arq[c['k']])]
cmd += ['-i', 'voz.mp3']
fc = [f'[{i}:v]fps=30,settb=AVTB,format=yuv420p[c{i}]' for i in range(len(clips))]
ult = 'c0'
for i, c in enumerate(clips[1:], 1):
    fc.append(f"[{ult}][c{i}]xfade=transition={TRANS.get(c['k'], 'fade')}:duration={X}:offset={c['in']:.3f}[x{i}]"); ult = f'x{i}'
fim = clips[-1]['out']
fc.append(f'[{len(clips)}:a]aresample=48000,highpass=f=70,loudnorm=I=-15:TP=-1.5:LRA=7,apad,atrim=0:{fim:.3f},afade=t=out:st={fim - 1.0:.3f}:d=1.0[a]')
base = cmd + ['-filter_complex', ';'.join(fc), '-map', f'[{ult}]', '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart']
subprocess.run(base + ['-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', 'VSL-final.mp4'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'VSL-final.mp4', '-vf', 'scale=1280:720:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow', '-crf', '25',
                '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', 'VSL-web.mp4'], check=True)
print('pronto: VSL-final.mp4, VSL-web.mp4 e VSL-legenda.srt')
