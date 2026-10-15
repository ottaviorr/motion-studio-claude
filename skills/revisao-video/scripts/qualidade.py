"""Qualidade de imagem medida, não achada.
uso:
  python qualidade.py comparar final.mp4 referencia.mkv [--ss 60 --t 4]
      SSIM e PSNR entre dois vídeos do MESMO conteúdo (ex.: render normal × render sem perda do mesmo trecho).
      Referência: SSIM ≥ 0,995 e PSNR ≥ 45 dB = compressão invisível. Abaixo de 0,98 dá para ver.
  python qualidade.py recorte video.mp4 63.0 x y w h [--saida recorte.png]
      Recorte 1:1 (sem reduzir) de uma região num tempo: é assim que se vê texto mole, serrilhado ou borda vazando.
      Compare com o mesmo recorte do bruto: se o bruto já é mole, a perda veio da gravação (resolução de captura), não do render."""
import sys, subprocess, re
a = sys.argv[1:]
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
if a[0] == 'comparar':
    x, y = a[1], a[2]
    ss = ['-ss', op('--ss')] if '--ss' in a else []; tt = ['-t', op('--t')] if '--t' in a else []
    for f in ('ssim', 'psnr'):
        r = subprocess.run(['ffmpeg', '-v', 'info', *ss, *tt, '-i', x, *ss, *tt, '-i', y, '-lavfi', f'[0:v]format=yuv420p[a];[1:v]format=yuv420p[b];[a][b]{f}', '-f', 'null', '-'],
                           capture_output=True, text=True).stderr
        m = re.findall(r'(SSIM.*|PSNR.*)', r); print(m[-1] if m else r[-400:])
elif a[0] == 'recorte':
    v, t, x, y, w, h = a[1], a[2], *a[3:7]
    out = op('--saida', f'recorte-{t}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', t, '-i', v, '-frames:v', '1', '-vf', f'crop={w}:{h}:{x}:{y}', out], check=True)
    print(out)
