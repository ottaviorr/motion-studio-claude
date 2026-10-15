"""Junta um fundo gravado UMA vez com o conteúdo de uma cena (gravado sem fundo), no ffmpeg — em segundos.
Por quê: shader de fundo dentro de cada cena deixa a captura do navegador ~4× mais lenta (medido no Windows:
95 s × 23 s numa cena de 6,4 s). O fundo é gravado pequeno (ex.: 960×540 a 30 fps) e ampliado aqui.

uso: python compor_fundo.py conteudo.mov fundo.mp4 saida.mov [--fade 0.4] [--furo x,y,w,h,r] [--fps 60] [--inicio 0]
  conteudo.mov  cena gravada com alfa (hf.mjs saida.mov) — só textos/cartões, fundo transparente
  fundo.mp4     fundo opaco (loop): ampliado para o tamanho do conteúdo
  --furo        retângulo arredondado que fica TRANSPARENTE no resultado (janela da câmera do apresentador)
  --fade        entrada e saída da peça inteira (alfa), em segundos
  --inicio      de que segundo do fundo começar (varia o fundo entre cenas)
  saída .mov = ProRes 4444 com alfa; saída .mp4 = H.264 opaco (NVENC se existir)."""
import sys, os, subprocess, tempfile
import numpy as np, cv2

a = sys.argv[1:]
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
CONT, FUNDO, SAIDA = a[0], a[1], a[2]
FADE = float(op('--fade', .4)); FPS = op('--fps', '30'); INI = float(op('--inicio', 0))
probe = lambda p, k: subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', k, '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip()
W, H = map(int, probe(CONT, 'stream=width,height').split(','))
D = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', CONT], capture_output=True, text=True).stdout)

# máscara: branco = mostra; furo preto com cantos arredondados (anti-serrilhado)
masc = np.full((H, W), 255, np.uint8)
if op('--furo'):
    x, y, w, h, r = map(int, op('--furo').split(','))
    S = 4; m = np.full((H * S, W * S), 255, np.uint8)   # desenha 4× maior e reduz: borda lisa
    X, Y, X2, Y2, R = x * S, y * S, (x + w) * S, (y + h) * S, r * S
    cv2.rectangle(m, (X + R, Y), (X2 - R, Y2), 0, -1); cv2.rectangle(m, (X, Y + R), (X2, Y2 - R), 0, -1)
    for cx, cy in [(X + R, Y + R), (X2 - R, Y + R), (X + R, Y2 - R), (X2 - R, Y2 - R)]: cv2.circle(m, (cx, cy), R, 0, -1)
    masc = cv2.resize(m, (W, H), interpolation=cv2.INTER_AREA)
mp = os.path.join(tempfile.mkdtemp(), 'mascara.png'); cv2.imwrite(mp, masc)

alfa = SAIDA.lower().endswith('.mov')
fo = max(0, D - FADE)
fc = (f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},trim=duration={D:.3f},setpts=PTS-STARTPTS,format=rgba[bg];"
      f"[bg][0:v]overlay=format=auto:shortest=1,format=rgba[c];"
      f"[2:v]format=gray,loop=-1:1,fps={FPS},trim=duration={D:.3f},setpts=PTS-STARTPTS,"
      f"fade=t=in:st=0:d={FADE},fade=t=out:st={fo:.3f}:d={FADE}[m];"
      f"[c][m]alphamerge[o]")
enc = (['-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0'] if alfa else
       ['-c:v', 'h264_nvenc', '-preset', 'p5', '-cq', '18', '-pix_fmt', 'yuv420p'])
cmd = ['ffmpeg', '-v', 'error', '-y', '-i', CONT, '-stream_loop', '-1', '-ss', f'{INI:.3f}', '-i', FUNDO, '-i', mp,
       '-filter_complex', fc, '-map', '[o]', '-an', *enc, SAIDA]
r = subprocess.run(cmd)
if r.returncode and not alfa:   # sem NVENC: x264
    cmd[cmd.index('h264_nvenc'):cmd.index('h264_nvenc') + 5] = ['libx264', '-preset', 'medium', '-crf', '18']
    r = subprocess.run(cmd)
sys.exit(r.returncode or print('pronto:', SAIDA, f'({D:.1f}s)'))
