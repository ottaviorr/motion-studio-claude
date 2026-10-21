"""Última etapa: deixa um vídeo no PADRÃO DE ENTREGA (scripts/padrao.py) numa única codificação.
uso: python finalizar.py video.mp4 [audio.wav] saida.mp4 [--lufs -14] [--sem-loudnorm]
  - vídeo: 1920×1080 (Lanczos, só se vier de outro tamanho), 30 fps constante, H.264 High 18 Mb/s CBR, BT.709
  - áudio: do audio.wav (PCM do Remotion ou do render.py) ou do próprio vídeo; -14 LUFS em duas passadas; AAC 320 k 48 kHz
  - confere no fim: duração do vídeo × áudio (diferença ≤ 1 quadro) e taxa de bits.
Use depois do Remotion (montagem em camadas) ou para conformar qualquer peça intercalada (motion) ao padrão."""
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import padrao as P

a = sys.argv[1:]
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
livres = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--lufs',))]
VID, SAI = livres[0], livres[-1]; AUD = livres[1] if len(livres) == 3 else None
if op('--lufs'): P.LUFS = float(op('--lufs'))
t0 = time.time()
P.fila()
iv = P.probe(VID)
vf = f'fps={P.FPS}'
if (iv['w'], iv['h']) != (P.W, P.H): vf += f',scale={P.W}:{P.H}:flags=lanczos'
vf += f",scale=in_color_matrix=bt709:out_color_matrix=bt709:in_range={'pc' if iv['faixa'] == 'pc' else 'tv'}:out_range=tv,format=yuv420p"
ent = ['-i', VID] + (['-i', AUD] if AUD else [])
amap = '1:a:0' if AUD else '0:a:0'
af = '' if '--sem-loudnorm' in a else P.loudnorm(AUD or VID) + ','
subprocess.run(['ffmpeg', '-v', 'error', '-y', *P.HWDEC, *ent, '-map', '0:v:0', '-map', amap,
                '-vf', vf, *P.V_FINAL, '-af', f'{af}aresample={P.SR}', *P.A_FINAL, '-movflags', '+faststart', SAI], check=True)
f = P.probe(SAI)
print(f"pronto em {time.time() - t0:.0f}s: {SAI}\n  {f['w']}×{f['h']} {f['fps']:g} fps · vídeo {f['v_bps'] / 1e6:.1f} Mb/s · "
      f"áudio {f['acodec']} {f['a_bps'] / 1e3:.0f} k {f['sr']} Hz · {f['dur']:.2f}s ({f['quadros']} quadros)")
