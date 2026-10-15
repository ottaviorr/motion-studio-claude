"""Monta o vídeo final de um EXPLICADOR/ANÚNCIO (sem filmagem): clipes em sequência + narração (+ música) (+ efeitos).
usage: python3 montar.py plano.json saida.mp4 [--sfx]
plano.json: {"W":1080,"H":1920,"fps":30,"bg":"#0B0C14","audio":"work/voz.wav","music":"inputs/musica.mp3"(opcional),
             "tail":1.2, "clips":[{"file":"out/01.mp4","in":0.0,"out":7.4}, ...]}
- cada clipe entra no seu "in" (corte seco) e segura o último quadro até o "out";
- música opcional fica baixa e abaixa ainda mais quando a voz fala (ducking);
- --sfx: um "whoosh" sintetizado (sem arquivo de terceiros) em cada troca de clipe."""
import json, sys, subprocess, pathlib
P = json.load(open(sys.argv[1])); base = pathlib.Path(sys.argv[1]).parent; out = sys.argv[2]; sfx = '--sfx' in sys.argv
rel = lambda f: str((base / f).resolve())
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', rel(P['audio'])], capture_output=True, text=True).stdout)
T = max(dur + P.get('tail', 1.2), max(c['out'] for c in P['clips']))
W, H, fps, bg = P['W'], P['H'], P.get('fps', 30), P.get('bg', '#0B0C14').lstrip('#')
cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=0x{bg}:s={W}x{H}:r={fps}:d={T:.3f}', '-i', rel(P['audio'])]
fc, last, n = [], '0:v', 2
for k, c in enumerate(P['clips']):
    cmd += ['-i', rel(c['file'])]
    fc.append(f"[{n}:v]tpad=stop_mode=clone:stop_duration=30,setpts=PTS-STARTPTS+{c['in']}/TB[c{k}]")
    fc.append(f"[{last}][c{k}]overlay=enable='between(t,{c['in']},{c['out']})':eof_action=pass[v{k}]"); last = f'v{k}'; n += 1
fc.append(f'[{last}]format=yuv420p[v]')
a = ['[1:a]aresample=48000,apad,atrim=0:%.3f[voz]' % T]
mix = ['[voz]']
if P.get('music'):
    cmd += ['-stream_loop', '-1', '-i', rel(P['music'])]
    a += [f'[{n}:a]aresample=48000,volume=0.22,atrim=0:{T:.3f},afade=t=out:st={T-1.5:.3f}:d=1.5[mus0]', '[voz]asplit[voz][vk]', '[mus0][vk]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=300[mus]']
    mix.append('[mus]'); n += 1
if sfx:
    for k, c in enumerate(P['clips'][1:], 1):
        t = max(0, c['in'] - 0.18)
        a.append(f"anoisesrc=d=0.5:c=pink:a=0.5,highpass=f=300,lowpass=f=5000,afade=t=in:d=0.25,afade=t=out:st=0.25:d=0.25,volume=0.25,adelay={int(t*1000)}|{int(t*1000)},apad,atrim=0:{T:.3f}[s{k}]")
        mix.append(f'[s{k}]')
a.append(''.join(mix) + f'amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.95[a]')
cmd += ['-filter_complex', ';'.join(fc + a), '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-c:a', 'aac', '-b:a', '192k', '-t', f'{T:.3f}', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True); print('vídeo:', out, f'{T:.1f}s')
