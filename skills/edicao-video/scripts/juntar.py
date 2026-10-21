"""Gravação que chegou em partes (part1, part2, part3 de um vídeo só) → um bruto normalizado, sem a voz escorregar nas emendas.
uso: python juntar.py part1.mp4 part2.mp4 [...] -o v1/bruto-30p.mov [--fps 30]
Faz o mesmo que o normalizar.py (30 fps constante pelo tempo real, PCM 48 kHz desde 0, BT.709 8 bits), mas parte por parte:
cada parte vira exatamente N quadros e o áudio dela é completado/cortado para N/30 s antes de emendar.
Por quê: o áudio de cada parte costuma ser ~30 ms mais curto que o vídeo; juntar com `concat -c copy` deixa um buraco (ou um
deslocamento de edit list, já vimos 44 ms) em cada emenda, e tudo depois dela fica fora da boca. Também grava `partes.json`
(onde cada parte começa no bruto) ao lado da saída."""
import sys, os, json, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import padrao as P

a = sys.argv[1:]
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
FPS = int(op('--fps', P.FPS)); SAI = os.path.abspath(op('-o'))
ENTS = [os.path.abspath(x) for i, x in enumerate(a) if not x.startswith('-') and (i == 0 or a[i - 1] not in ('-o', '--fps'))]

ins, fil, partes, t = [], [], [], 0.0
for k, e in enumerate(ENTS):
    i = P.probe(e)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=duration',
                                '-of', 'csv=p=0', e], capture_output=True, text=True).stdout.strip())
    n = round(dur * FPS); faixa = 'pc' if i['faixa'] == 'pc' else 'tv'
    ins += [*P.HWDEC, '-i', e]
    fil.append(f'[{k}:v:0]fps={FPS}:start_time=0:round=near,trim=end_frame={n},setpts=PTS-STARTPTS,'
               f'scale=in_range={faixa}:out_range=tv:in_color_matrix=bt709:out_color_matrix=bt709:flags=lanczos,'
               f'format=yuv420p,setsar=1[v{k}]')
    fil.append(f'[{k}:a:0]aresample={P.SR}:async=1:first_pts=0,aformat=channel_layouts=stereo,apad,'
               f'atrim=end_sample={round(n / FPS * P.SR)},asetpts=PTS-STARTPTS[a{k}]')
    partes.append({'arquivo': os.path.basename(e), 'inicio': round(t, 4), 'quadros': n}); t += n / FPS
    print(f'{os.path.basename(e)}: {i["w"]}×{i["h"]} faixa={i["faixa"]} · {n} quadros ({n / FPS:.2f} s) · começa em {partes[-1]["inicio"]:.2f} s')
fil.append(''.join(f'[v{k}][a{k}]' for k in range(len(ENTS))) + f'concat=n={len(ENTS)}:v=1:a=1[v][a]')

P.fila(); t0 = time.time()
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fil), '-map', '[v]', '-map', '[a]',
                '-fps_mode', 'cfr', '-r', str(FPS), *P.V_INTER, '-c:a', 'pcm_s24le',
                '-video_track_timescale', str(FPS * 1000), SAI], check=True)
json.dump(partes, open(os.path.join(os.path.dirname(SAI), 'partes.json'), 'w'), indent=1, ensure_ascii=False)
ok, txt = P.taxa_constante(SAI, FPS)
print(f'juntado em {time.time() - t0:.0f}s → {SAI}\n  {txt}  {"OK" if ok else "FORA DO RITMO — investigue"}')
if not ok: sys.exit(1)
