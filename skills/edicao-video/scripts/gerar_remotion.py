"""Gera a montagem final no Remotion a partir do plano de edição (modo "camadas": Python + HyperFrames + Remotion).
uso: python gerar_remotion.py fonte/edicao.json pasta-remotion [--tela v3/aula-tela.mp4 --voz v3/aula-voz.m4a]
Antes: render.py --camada-tela (tela + voz) e as cenas gravadas (kit/hf.mjs). O edicao.json usa:
  motions [{arquivo, ini}] (a primeira em 0 = abertura; uma com "sem_camera" no fim = fechamento),
  capitulos [[ini, n, "texto"]], camera, camera_recuo, camera_raio, escala.
Escreve: <pasta>/src/{index.ts, Root.tsx, componentes.tsx (do modelo da skill), Aula.tsx} e liga as mídias em <pasta>/public/.
Aula.tsx tem UM nó JSX por clipe (câmera, cena, capítulo, efeito): no Remotion Studio cada um pode ser movido/aparado à mão."""
import sys, os, json, shutil, subprocess
import numpy as np
a = sys.argv[1:]; cfg = os.path.abspath(a[0]); base = os.path.dirname(cfg); C = json.load(open(cfg)); R = os.path.abspath(a[1])
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
J = lambda p: os.path.normpath(os.path.join(base, p))
MODELO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'remotion')
edl = json.load(open(J('edl.json'))); ZK = json.load(open(J('zoom.json')))
at = json.load(open(J(C.get('atividade', 'atividade.json'))))
FPS = C.get('fps', 30); E = C.get('escala', 1)   # padrão 1080p30 (dono, 13/10/2026)
# NVENC (GPU NVIDIA) quando existir: 4K de 81 s em 39 s × ~5 min no x264, SSIM 0,997 entre os dois
NVENC = 'h264_nvenc' in subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], capture_output=True, text=True).stdout
ENC_INTER = (['-c:v', 'h264_nvenc', '-preset', 'p6', '-tune', 'hq', '-rc', 'vbr', '-cq', '14', '-b:v', '0'] if NVENC
             else ['-c:v', 'libx264', '-preset', 'medium', '-crf', '12'])
probe = lambda p, k: subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', k, '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip()
VW, VH = map(int, probe(J(C['bruto']), 'stream=width,height').split(','))
dur_de = lambda p: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
saida = C.get('saida', '../v3/aula-v3.mp4'); b_ = J(saida)[:-4]
TELA = J(op('--tela', b_ + '-tela.mp4')) if '--tela' in a else b_ + '-tela.mp4'
VOZ = J(op('--voz', b_ + '-voz.m4a')) if '--voz' in a else b_ + '-voz.m4a'

# ---------- origem do empurrão: onde a ação estava na tela logo antes da cena (o "objeto" que a câmera atravessa) ----------
BORDA = C.get('borda', 0); BW = (VW - 2 * BORDA) / VW; BX = BORDA / VW; BY = (1 - BW) / 2
def suave(x): x = min(1, max(0, x)); return x * x * x * (x * (x * 6 - 15) + 10)
def vista(t):
    rect = lambda k: (k['cx'] - .5 / k['z'], k['cy'] - .5 / k['z'], 1 / k['z']); cur = rect(ZK[0])
    for i, k in enumerate(ZK[1:], 1):
        if t < k['t']: break
        prox = ZK[i + 1]['t'] if i + 1 < len(ZK) else 1e9; d = min(.8, max(.25, prox - k['t']))
        cur = tuple(c + (b - c) * suave((t - k['t']) / d) for c, b in zip(cur, rect(k)))
    x0, y0, w = cur; return (BX + x0 * BW, BY + y0 * BW, w * BW)
def fonte(t):
    for e in edl['trechos']:
        d = (e['out'] - e['in']) / e['vel']
        if e['ini'] <= t < e['ini'] + d: return e['in'] + (t - e['ini']) * e['vel']
    return None
def origem(T):
    x0, y0, w = vista(max(0, T - .1)); cx, cy, n = 0, 0, 0
    for t in np.arange(max(0, T - 2.5), T, .25):
        s = fonte(t); i = int(s * at['fps']) if s is not None else -1
        if 0 <= i < len(at['diff']) and at['diff'][i] > .002 and at['caixa'][i]:
            b = at['caixa'][i]; cx += (b[0] + b[2]) / 2; cy += (b[1] + b[3]) / 2; n += 1
    if not n: return .5, .5
    return float(np.clip((cx / n - x0) / w, .15, .85)), float(np.clip((cy / n - y0) / w, .15, .85))

# ---------- cenas e costuras ----------
cenas, costuras = [], []
for m in sorted(C.get('motions', []), key=lambda m: m['ini']):
    p = J(m['arquivo']); d = dur_de(p); ini = m['ini']
    tipo = 'abertura' if ini < .05 else ('fechamento' if m.get('sem_camera') else 'meio')
    if tipo == 'fechamento': ini = min(ini, edl['dur'] - .02)   # sem buraco preto entre o fim da tela e o fechamento
    ox, oy = origem(ini)
    if tipo == 'abertura': costuras.append({'t': 0.0, 'tipo': 'entra-cena', 'ox': .5, 'oy': .5})
    elif tipo == 'fechamento': costuras.append({'t': round(ini, 3), 'tipo': 'fechamento', 'ox': ox, 'oy': oy})
    else: costuras.append({'t': round(ini, 3), 'tipo': 'entra-cena', 'ox': round(ox, 3), 'oy': round(oy, 3)})
    if tipo != 'fechamento': costuras.append({'t': round(ini + d, 3), 'tipo': 'volta-tela', 'ox': .5, 'oy': .5})
    cenas.append({'nome': os.path.basename(p)[:-4], 'arq': p, 'ini': ini, 'dur': d, 'tipo': tipo})
fim = max([c['ini'] + c['dur'] for c in cenas] + [edl['dur']])
fecha = next((c['ini'] for c in cenas if c['tipo'] == 'fechamento'), None)

# ---------- pasta do projeto ----------
os.makedirs(os.path.join(R, 'src'), exist_ok=True); pub = os.path.join(R, 'public'); os.makedirs(os.path.join(pub, 'cenas'), exist_ok=True); os.makedirs(os.path.join(pub, 'sfx'), exist_ok=True)
for f in ('componentes.tsx',): shutil.copy(os.path.join(MODELO, 'src', f), os.path.join(R, 'src', f))
def liga(orig, nome):
    dst = os.path.join(pub, nome)
    if os.path.lexists(dst): os.remove(dst)
    try: os.link(orig, dst)          # hard link: o Remotion não serve symlink da pasta public/ (dá 404); hard link não gasta disco
    except OSError: shutil.copy(orig, dst)
liga(TELA, 'tela.mp4'); liga(VOZ, 'voz.m4a')
for velho in ('bruto.mp4',):
    if os.path.lexists(os.path.join(pub, velho)): os.remove(os.path.join(pub, velho))
# câmera: recorte do bruto, ampliado com Lanczos, H.264 BT.709 faixa limitada (o Remotion lê certo; HEVC 10 bits saía lavado)
cx_, cy_, cw_, ch_ = C['camera']; CAMF = os.path.join(pub, 'camera.mp4')
if not os.path.exists(CAMF) or os.path.getmtime(CAMF) < os.path.getmtime(J(C['bruto'])):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', J(C['bruto']), '-an', '-vf',
                    f'crop={cw_}:{ch_}:{cx_}:{cy_},scale={cw_ * E}:{ch_ * E}:flags=lanczos:in_color_matrix=bt709:out_color_matrix=bt709:in_range=tv:out_range=tv,format=yuv420p',
                    *ENC_INTER, '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
                    '-movflags', '+faststart', CAMF], check=True)
for c in cenas: liga(c['arq'], f"cenas/{c['nome']}.mp4")
for s in ('whoosh',):
    dst = os.path.join(pub, 'sfx', s + '.wav')
    if not os.path.exists(dst): subprocess.run(['curl', '-sfL', '-o', dst, f'https://remotion.media/{s}.wav'])
tem_whoosh = os.path.exists(os.path.join(pub, 'sfx', 'whoosh.wav'))

open(os.path.join(R, 'src', 'index.ts'), 'w').write('import { registerRoot } from "remotion";\nimport { RemotionRoot } from "./Root";\nregisterRoot(RemotionRoot);\n')
open(os.path.join(R, 'src', 'Root.tsx'), 'w').write(f'''import React from "react";
import {{ Composition }} from "remotion";
import {{ Aula }} from "./Aula";
export const RemotionRoot: React.FC = () => (
  <Composition id="Aula" component={{Aula}} width={{{VW * E}}} height={{{VH * E}}} fps={{{FPS}}} durationInFrames={{{int(round(fim * FPS))}}} />
);
''')
cam = C['camera']; rec = C.get('camera_recuo', 2); raio = C.get('camera_raio', 20)
L = []
L.append('// GERADO por skill edicao-video/scripts/gerar_remotion.py — um nó por clipe; pode editar no Remotion Studio.')
L.append('import React from "react";\nimport { AbsoluteFill, Sequence, staticFile, useVideoConfig } from "remotion";\nimport { Audio } from "@remotion/media";')
L.append('import { Tela, Cena, Moldura, TrechoCamera, Capitulo, type Costura } from "./componentes";')
L.append(f'const E = {E};\nconst CAM: [number, number, number, number] = {json.dumps(cam)};')
L.append('const COSTURAS: Costura[] = ' + json.dumps(costuras) + ';')
L.append('export const Aula: React.FC = () => {\n  const { fps } = useVideoConfig();\n  return (\n    <AbsoluteFill style={{ background: "#0d0c14" }}>')
L.append('      {/* camada de tela (cortes + zoom, vinda do render.py --camada-tela) */}')
L.append(f'      <Sequence name="Tela" from={{0}} durationInFrames={{{int(round(edl["dur"] * FPS))}}} premountFor={{fps}}><Tela src={{staticFile("tela.mp4")}} costuras={{COSTURAS}} escala={{E}} /></Sequence>')
L.append('      {/* cenas de motion (gravadas pelo HyperFrames) */}')
for c in cenas:
    ent = {'abertura': 'nenhuma', 'meio': 'empurrao', 'fechamento': 'reverso'}[c['tipo']]; sai = 'nenhuma' if c['tipo'] == 'fechamento' else 'curva'
    L.append(f'      <Sequence name="{c["nome"]}" from={{{int(round(c["ini"] * FPS))}}} durationInFrames={{{int(round(c["dur"] * FPS))}}} premountFor={{fps}}>'
             f'<Cena src={{staticFile("cenas/{c["nome"]}.mp4")}} entrada="{ent}" saida="{sai}" dur={{{c["dur"]:.3f}}} escala={{E}} /></Sequence>')
L.append('      {/* câmera do apresentador: cada trecho do bruto, na mesma ordem dos cortes */}')
L.append(f'      <Moldura rect={{CAM}} escala={{E}} recuo={{{rec}}} raio={{{raio}}}{f" someEm={{{fecha:.3f}}}" if fecha else ""}>')
for i, e in enumerate(edl['trechos'], 1):
    d = (e['out'] - e['in']) / e['vel']
    L.append(f'        <Sequence name="câmera {i:02d}" from={{{int(round(e["ini"] * FPS))}}} durationInFrames={{{max(1, int(round(d * FPS)))}}} premountFor={{fps}}>'
             f'<TrechoCamera src={{staticFile("camera.mp4")}} trimBefore={{{int(round(e["in"] * FPS))}}} escala={{E}} recuo={{{rec}}} largura={{{cam[2]}}} altura={{{cam[3]}}} /></Sequence>')
L.append('      </Moldura>')
L.append('      {/* capítulos */}')
for ini, n, txt in C.get('capitulos', []):
    L.append(f'      <Sequence name="capítulo {n}" from={{{int(round(ini * FPS))}}} durationInFrames={{{3 * FPS}}} premountFor={{fps}}><Capitulo n={{{n}}} texto={json.dumps(txt, ensure_ascii=False)} x={{{cam[0]}}} base={{{cam[1] - 18}}} escala={{E}} /></Sequence>')
L.append('      {/* áudio: voz tratada + um whoosh discreto em cada empurrão */}')
L.append('      <Audio src={staticFile("voz.m4a")} />')
if tem_whoosh:
    for c in costuras:
        if c['tipo'] in ('entra-cena', 'fechamento') and c['t'] > .05:
            L.append(f'      <Sequence name="whoosh {c["t"]:.1f}s" from={{{max(0, int(round((c["t"] - .28) * FPS)))}}} durationInFrames={{{FPS}}}><Audio src={{staticFile("sfx/whoosh.wav")}} volume={{0.16}} /></Sequence>')
L.append('    </AbsoluteFill>\n  );\n};\n')
open(os.path.join(R, 'src', 'Aula.tsx'), 'w').write('\n'.join(L))
print(f'Remotion: {len(cenas)} cenas, {len(edl["trechos"])} trechos de câmera, {len(C.get("capitulos", []))} capítulos, {fim:.1f}s → {R}/src/Aula.tsx')
