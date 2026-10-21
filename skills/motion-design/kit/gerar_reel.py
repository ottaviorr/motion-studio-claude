"""Monta reels/anúncios no Remotion a partir de reels/*.json (cenas do HyperFrames + música na batida + voz + efeitos).
uso:  python gerar_reel.py <pasta-do-projeto>            → (re)gera <projeto>/remotion/src (uma composição por reel)
      python gerar_reel.py <pasta-do-projeto> --render 01  → gera e renderiza o reel 01 em <projeto>/prontos/reel-01.mp4 (+ volume -14 LUFS); espera a vez na fila global de render
Cada <projeto>/reels/NN.json:
  {"cenas": [{"arquivo": "cenas/r01a.mp4", "entrada": "nenhuma", "saida": "curva"}, ...],    ← em sequência, emendadas
   "musica": {"arquivo": "musica/tech-01.mp3", "inicio": 3.914, "volume": 0.55, "fade": 1.2}, ← "inicio" = segundo da faixa
   "voz": {"arquivo": "vozes/reel-02.mp3", "inicio": 0.0},                                    ← opcional: com voz, a música é medida e fica
   "musica_abaixo_da_voz": 21,                                                                ←   21 dB abaixo dela (o "volume" da música é ignorado)
   "sfx": [[11.0, "whoosh", 0.25], [3.2, "mouse-click", 0.15]],                              ← [segundo, nome em public/sfx, volume]
   "w": 1080, "h": 1920, "fps": 60, "bitrate": "20M"}   ← bitrate fixo alto (o dono pediu); padrão 20M
Modelo de componentes: $K/remotion-reel/src/reel.tsx (copiado para o projeto). Mídias entram em public/ por hard link."""
import sys, os, json, glob, shutil, subprocess
P = os.path.abspath(sys.argv[1]); R = os.path.join(P, 'remotion'); K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pub = os.path.join(R, 'public'); os.makedirs(os.path.join(R, 'src'), exist_ok=True); os.makedirs(pub, exist_ok=True)
shutil.copy(os.path.join(K, 'remotion-reel', 'src', 'reel.tsx'), os.path.join(R, 'src', 'reel.tsx'))
if not os.path.exists(os.path.join(R, 'remotion.config.ts')): shutil.copy(os.path.join(K, 'remotion-reel', 'remotion.config.ts'), R)   # padrões de render por sistema
def lufs(p, ss=None, t=None):
    a = ['ffmpeg', '-v', 'info'] + (['-ss', str(ss)] if ss else []) + (['-t', str(t)] if t else []) + ['-i', p, '-af', 'ebur128', '-f', 'null', '-']
    import re; m = re.findall(r'I:\s+(-?[\d.]+) LUFS', subprocess.run(a, capture_output=True, text=True).stderr); return float(m[-1]) if m else -20.0
dur_de = lambda p: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
def liga(rel):
    orig = os.path.join(P, rel); dst = os.path.join(pub, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.lexists(dst): os.remove(dst)
    try: os.link(orig, dst)                     # o Remotion não serve symlink da public/
    except OSError: shutil.copy(orig, dst)
    return rel
reels = []
for jf in sorted(glob.glob(os.path.join(P, 'reels', '*.json'))):
    n = os.path.basename(jf)[:-5]; C = json.load(open(jf)); fps = C.get('fps', 60); W, H = C.get('w', 1080), C.get('h', 1920)
    L = [f'// GERADO por motion-design/kit/gerar_reel.py a partir de reels/{n}.json — um nó por clipe (editável no Studio).',
         'import React from "react";\nimport { AbsoluteFill, Sequence, staticFile, useVideoConfig } from "remotion";\nimport { Audio } from "@remotion/media";\nimport { Cena, Musica } from "./reel";',
         f'export const Reel{n}: React.FC = () => {{\n  const {{ fps }} = useVideoConfig();\n  return (\n    <AbsoluteFill style={{{{ background: "#0b0a12" }}}}>']
    t = 0.0
    for c in C['cenas']:
        d = dur_de(os.path.join(P, c['arquivo'])); f0, nf = int(round(t * fps)), int(round(d * fps))
        L.append(f'      <Sequence name="{os.path.basename(c["arquivo"])[:-4]}" from={{{f0}}} durationInFrames={{{nf}}} premountFor={{fps}}>'
                 f'<Cena src={{staticFile("{liga(c["arquivo"])}")}} dur={{{d:.3f}}} entrada="{c.get("entrada", "curva")}" saida="{c.get("saida", "curva")}" largura={{{W}}} /></Sequence>')
        t += d
    dur = t
    # mixagem pela medida, não pelo chute: a música fica ABAIXO_DA_VOZ dB abaixo da voz (padrão 21: fala clara por cima)
    # e os efeitos acompanham o nível da voz (foram pensados para uma voz a ~-19 LUFS). O dono reclamou de música alta.
    m, v = C.get('musica'), C.get('voz')
    Lv = lufs(os.path.join(P, v['arquivo'])) if v else None
    k_sfx = min(1.0, 10 ** ((Lv + 19) / 20)) if v else 1.0
    if m:
        if v:
            Lm = lufs(os.path.join(P, m['arquivo']), m.get('inicio', 0) or None, dur)
            vol = min(1.0, 10 ** ((Lv - C.get('musica_abaixo_da_voz', 21) - Lm) / 20))
        else:
            vol = m.get('volume', .55)
        L.append(f'      <Musica src={{staticFile("{liga(m["arquivo"])}")}} inicio={{{m.get("inicio", 0)}}} volume={{{vol:.4f}}} fade={{{m.get("fade", 1.2)}}} dur={{{dur:.3f}}} />')
    if v: L.append(f'      <Sequence name="voz" from={{{int(round(v.get("inicio", 0) * fps))}}}><Audio src={{staticFile("{liga(v["arquivo"])}")}} /></Sequence>')
    for ts, nome, vol in C.get('sfx', []):
        L.append(f'      <Sequence name="{nome} {ts:.2f}s" from={{{max(0, int(round(ts * fps)))}}} durationInFrames={{{fps * 2}}}><Audio src={{staticFile("sfx/{nome}.wav")}} volume={{{vol * k_sfx:.4f}}} /></Sequence>')
    L.append('    </AbsoluteFill>\n  );\n};\n')
    open(os.path.join(R, 'src', f'Reel{n}.tsx'), 'w').write('\n'.join(L))
    reels.append((n, int(round(dur * fps)), fps, W, H, C.get('bitrate', '20M')))
imp = '\n'.join(f'import {{ Reel{n} }} from "./Reel{n}";' for n, *_ in reels)
comps = '\n'.join(f'    <Composition id="Reel{n}" component={{Reel{n}}} width={{{W}}} height={{{H}}} fps={{{fps}}} durationInFrames={{{nf}}} />' for n, nf, fps, W, H, _ in reels)
open(os.path.join(R, 'src', 'Root.tsx'), 'w').write(f'import React from "react";\nimport {{ Composition }} from "remotion";\n{imp}\nexport const RemotionRoot: React.FC = () => (\n  <>\n{comps}\n  </>\n);\n')
open(os.path.join(R, 'src', 'index.ts'), 'w').write('import { registerRoot } from "remotion";\nimport { RemotionRoot } from "./Root";\nregisterRoot(RemotionRoot);\n')
print('reels:', ', '.join(f'{n} ({nf / fps:.1f}s)' for n, nf, fps, *_ in reels))

def fila():
    """uma montagem/gravação por vez no computador inteiro (mesma trava do hf.mjs)"""
    import time, atexit
    f = os.path.join(os.path.expanduser('~'), '.cache', 'motion-studio-fila-render'); os.makedirs(os.path.dirname(f), exist_ok=True)
    while True:
        try: os.mkdir(f); break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(f) > 45 * 60: os.rmdir(f)
            except OSError: pass
            time.sleep(2)
    atexit.register(lambda: os.path.isdir(f) and os.rmdir(f))
if '--render' in sys.argv:
    fila()
    n = sys.argv[sys.argv.index('--render') + 1]; br = next(r[5] for r in reels if r[0] == n)
    # vídeo final vai direto para prontos/ (pasta só com os vídeos que o dono recebe); reels/ guarda só as configurações
    os.makedirs(os.path.join(P, 'prontos'), exist_ok=True); bruto = os.path.join(R, 'out', f'reel-{n}-bruto.mov'); final = os.path.join(P, 'prontos', f'reel-{n}.mp4')
    # 1) Remotion → ProRes HQ (quase sem perda); 2) H.264 CBR (bitrate constante = br: o dono pediu bitrate alto; o x264 só respeita mínimo em CBR)
    #    — com só "--video-bitrate" o codificador gastava bem menos em cena fácil (saíram de 7,7 a 23 Mb/s).
    subprocess.run([shutil.which('npx') or 'npx', 'remotion', 'render', f'Reel{n}', bruto, '--codec=prores', '--prores-profile=hq', '--log=error'], cwd=R, check=True)
    med = subprocess.run(['ffmpeg', '-v', 'info', '-i', bruto, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    Lm = json.loads(med[med.rindex('{'):med.rindex('}') + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={Lm['input_i']}:measured_TP={Lm['input_tp']}:measured_LRA={Lm['input_lra']}"
          f":measured_thresh={Lm['input_thresh']}:offset={Lm['target_offset']}:linear=true")
    b = int(str(br).rstrip('Mm')) if str(br)[-1] in 'Mm' else 20
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', bruto,
                    '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high',
                    '-b:v', f'{b}M', '-minrate', f'{b}M', '-maxrate', f'{b}M', '-bufsize', f'{b}M', '-x264-params', 'nal-hrd=cbr',
                    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    '-af', ln + ',aresample=48000', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', final], check=True)
    os.remove(bruto); print('pronto:', final)
