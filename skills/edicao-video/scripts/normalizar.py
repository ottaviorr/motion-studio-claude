"""Normaliza o bruto ANTES de tudo: quadros em ritmo constante de 30 fps pelo tempo real de cada quadro, áudio PCM 48 kHz
começando junto com o vídeo, cor 8 bits BT.709. É o primeiro passo da sincronia por construção.
uso: python normalizar.py v1/bruto.mp4 [saida.mov] [--fps 30] [--rapido]
  → v1/bruto-30p.mov (ao lado do bruto). Ponha "bruto": "../bruto-30p.mov" no edicao.json.
  --rapido: codifica no hardware (Mac: h264_videotoolbox; NVIDIA: h264_nvenc; 60 Mb/s) em vez do x264 CRF 10 (um pouco maior, ~2× mais rápido).
Por quê: gravação de tela, OBS sobrecarregado e iPhone gravam com taxa VARIÁVEL (quadros fora do ritmo, quadros perdidos).
Quem conta quadros como se fossem tempo (render.py, trimBefore do Remotion) desliza um quadro a cada quadro perdido, e o
erro se acumula até o fim. Aqui o filtro fps escolhe, para cada instante k/30 s, o quadro que estava na tela naquele instante.
Resolução: mantém a do bruto (4K continua 4K: o zoom aproveita); a entrega em 1080p sai do render.
Faixa de cor: respeita a do arquivo (o bruto do cliente B é HEVC 10 bits em faixa completa: 0–1023)."""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import padrao as P

a = sys.argv[1:]
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
ENT = os.path.abspath(a[0])
FPS = int(op('--fps', P.FPS))
livres = [x for i, x in enumerate(a[1:], 1) if not x.startswith('--') and a[i - 1] not in ('--fps',)]
SAI = os.path.abspath(livres[0]) if livres else os.path.splitext(ENT)[0] + f'-{FPS}p.mov'

i = P.probe(ENT); ok, txt = P.taxa_constante(ENT)
print(f'bruto: {i["w"]}×{i["h"]} {i["vcodec"]} {i["pix"]} faixa={i["faixa"]} · {txt}')
if i['trc'] in ('arib-std-b67', 'smpte2084'):
    print('ATENÇÃO: bruto em HDR (iPhone?). Este ffmpeg não tem zscale para converter direito: grave em SDR '
          '(Ajustes > Câmera > Gravar vídeo > desligar HDR) ou aceite cor um pouco lavada.')
if not ok: print('→ ritmo NÃO constante (ou áudio desalinhado): sem normalizar, a câmera escorrega em relação à voz.')

faixa = 'pc' if i['faixa'] == 'pc' else 'tv'
vf = (f'fps={FPS}:start_time=0:round=near,'
      f'scale=in_range={faixa}:out_range=tv:in_color_matrix=bt709:out_color_matrix=bt709:flags=lanczos,format=yuv420p,setsar=1')
enc = ((['-c:v', 'h264_videotoolbox'] if P.MAC else ['-c:v', 'h264_nvenc', '-preset', 'p5']) + ['-b:v', '60M', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-g', str(FPS), *P.COR] if '--rapido' in a
       else P.V_INTER)
P.fila()   # é uma codificação pesada: entra na fila global de render
t0 = time.time()
subprocess.run(['ffmpeg', '-v', 'error', '-y', *P.HWDEC, '-i', ENT, '-map', '0:v:0', '-map', '0:a:0',
                '-vf', vf, '-fps_mode', 'cfr', '-r', str(FPS), *enc,
                '-af', f'aresample={P.SR}:async=1:first_pts=0', '-ac', '2', '-c:a', 'pcm_s24le',
                '-video_track_timescale', str(FPS * 1000), SAI], check=True)
ok2, txt2 = P.taxa_constante(SAI, FPS)
print(f'normalizado em {time.time() - t0:.0f}s → {SAI}\n  {txt2}  {"OK" if ok2 else "AINDA FORA DO RITMO — investigue"}')
if not ok2: sys.exit(1)
