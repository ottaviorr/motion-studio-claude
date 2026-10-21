"""Gera a montagem final no Remotion a partir do plano de edição (modo "camadas": Python + HyperFrames + Remotion).
uso: python gerar_remotion.py fonte/edicao.json pasta-remotion [--tela v3/aula-tela.mp4 --voz v3/aula-voz.wav]
Antes: render.py --camada-tela (tela + voz.wav) e as cenas gravadas (kit/hf.mjs, 1080p30). O edicao.json usa:
  motions [{arquivo, ini}] (a primeira em 0 = abertura; uma com "sem_camera" no fim = fechamento),
  capitulos [[ini, n, "texto"]], camera, camera_recuo, camera_raio, escala.
Escreve: <pasta>/src/{index.ts, Root.tsx, componentes.tsx (do modelo da skill), Aula.tsx} e liga as mídias em <pasta>/public/.
Aula.tsx tem UM nó JSX por clipe (câmera, cena, capítulo, efeito): no Remotion Studio cada um pode ser movido/aparado à mão.
Escreve também <pasta>/renderizar.sh: Remotion (vídeo + áudio PCM, uma passada) na fila global → finalizar.py → padrão de entrega.
SINCRONIA: cada trecho da câmera usa os inteiros do edl (from = q0, durationInFrames = nq, trimBefore = q_in) — nada de
round(ini*fps) e round(in*fps) separados (davam até 21 ms de desvio e 1 quadro sem câmera entre trechos na v3 do cliente B)."""
import sys, os, json, shutil, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import padrao as P
a = sys.argv[1:]; cfg = os.path.abspath(a[0]); base = os.path.dirname(cfg); C = json.load(open(cfg)); R = os.path.abspath(a[1])
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
J = lambda p: os.path.normpath(os.path.join(base, p))
MODELO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'remotion')
edl = json.load(open(J('edl.json'))); ZK = json.load(open(J('zoom.json')))
at = json.load(open(J(C.get('atividade', 'atividade.json'))))
FPS = C.get('fps', P.FPS)
INFO = P.probe(J(C['bruto'])); VW, VH = INFO['w'], INFO['h']
OW, OH = (int(VW * C['escala']), int(VH * C['escala'])) if C.get('escala', 1) != 1 else (P.W, P.H)
E = OW / VW
if 'q0' not in edl['trechos'][0] or edl.get('fps') != FPS: sys.exit('edl.json sem quadros inteiros (ou de outro fps): rode plano.py de novo')
TQ = sum(e['nq'] for e in edl['trechos'])
dur_de = lambda p: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
saida = C.get('saida', '../v3/aula-v3.mp4'); b_ = J(saida)[:-4]
TELA = J(op('--tela', b_ + '-tela.mp4')) if '--tela' in a else b_ + '-tela.mp4'
VOZ = J(op('--voz', b_ + '-voz.wav')) if '--voz' in a else b_ + '-voz.wav'

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
liga(TELA, 'tela.mp4'); liga(VOZ, 'voz.wav')
for velho in ('bruto.mp4',):
    if os.path.lexists(os.path.join(pub, velho)): os.remove(os.path.join(pub, velho))
# câmera: recorte do bruto NORMALIZADO (30 fps constante: o quadro n do camera-k.mp4 é o quadro n do bruto), no tamanho da saída,
# H.264 BT.709 faixa limitada (o Remotion lê certo; HEVC 10 bits saía lavado). Já sai sem a borda do original (camera_recuo).
# Câmera que muda de canto ("cameras": [[s_ini, s_fim, x, y, w, h, {"destino": [x,y,w,h], "punch": true}?], ...] em s do bruto):
# um recorte por lugar; "destino" = onde ela aparece na saída (ex.: abertura com a câmera grande ao lado do texto).
if abs(INFO['fps'] - FPS) > 1e-3: sys.exit(f"bruto a {INFO['fps']:g} fps: normalize antes (scripts/normalizar.py) para a câmera casar quadro a quadro com a voz")
rec = C.get('camera_recuo', 2); raio = C.get('camera_raio', 20)
LUGARES = [{'de': l[0], 'ate': l[1], 'rect': l[2:6], **(l[6] if len(l) > 6 else {})} for l in C.get('cameras', [])] or \
          [{'de': 0, 'ate': 1e9, 'rect': C['camera']}]
for k, L_ in enumerate(LUGARES):
    x_, y_, w_, h_ = L_['rect']; dx, dy, dw, dh = L_.get('destino', L_['rect'])
    L_['saida'] = [dx + rec, dy + rec, dw - 2 * rec, dh - 2 * rec] if 'destino' not in L_ else [dx, dy, dw, dh]
    L_['arq'] = f'camera-{k}.mp4'; CAMF = os.path.join(pub, L_['arq'])
    if not os.path.exists(CAMF) or os.path.getmtime(CAMF) < max(os.path.getmtime(J(C['bruto'])), os.path.getmtime(cfg)):
        ow_, oh_ = L_['saida'][2] * E, L_['saida'][3] * E
        fx = 'lanczos' if ow_ > w_ - 2 * rec else 'area'   # x264 pede lados pares: arredonda para cima (o navegador estica < 1 px)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', J(C['bruto']), '-an', '-vf',
                        f"crop={w_ - 2 * rec}:{h_ - 2 * rec}:{x_ + rec}:{y_ + rec},scale={2 * -(-round(ow_) // 2)}:{2 * -(-round(oh_) // 2)}:flags={fx}:in_color_matrix=bt709:out_color_matrix=bt709:"
                        f"in_range={'pc' if INFO['faixa'] == 'pc' else 'tv'}:out_range=tv,format=yuv420p",
                        '-fps_mode', 'passthrough', *P.V_INTER, '-movflags', '+faststart', CAMF], check=True)
def lugar_de(s):
    for k, L_ in enumerate(LUGARES):
        if L_['de'] <= s < L_['ate']: return k
    return 0
# blocos: trechos seguidos no mesmo lugar (um trecho não pode atravessar a troca de lugar: corte nela)
blocos = []
for e in edl['trechos']:
    k = lugar_de(e['in'])
    if lugar_de(max(e['in'], e['out'] - 1e-3)) != k: sys.exit(f"trecho {e['in']:.2f}–{e['out']:.2f} atravessa a troca de lugar da câmera: ponha um corte nela")
    if blocos and blocos[-1]['k'] == k: blocos[-1]['tr'].append(e)
    else: blocos.append({'k': k, 'tr': [e]})
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
  <Composition id="Aula" component={{Aula}} width={{{OW}}} height={{{OH}}} fps={{{FPS}}} durationInFrames={{{max(TQ, int(round(fim * FPS)))}}} />
);
''')
cam = LUGARES[0]['rect']
TEMA = f' tema="{C["tema"]}"' if C.get('tema') else ''
L = []
L.append('// GERADO por skill edicao-video/scripts/gerar_remotion.py — um nó por clipe; pode editar no Remotion Studio.')
L.append('import React from "react";\nimport { AbsoluteFill, Sequence, staticFile, useVideoConfig } from "remotion";\nimport { Audio } from "@remotion/media";')
L.append('import { Tela, Cena, MolduraMovel, TrechoCam, Capitulo, SeloStatus, type Costura } from "./componentes";')
EXTRAS = os.path.exists(os.path.join(R, 'src', 'Extras.tsx'))   # camada do projeto: tela em cena, anotações, pop-ups, texto (escrita à mão; o gerador não sobrescreve)
if EXTRAS: L.append('import { Extras, PalcoTela, PalcoCamera } from "./Extras";')
L.append(f'const E = {E};\nconst CAM: [number, number, number, number] = {json.dumps(cam)};')
L.append('const COSTURAS: Costura[] = ' + json.dumps(costuras) + ';')
L.append('export const Aula: React.FC = () => {\n  const { fps } = useVideoConfig();\n  return (\n    <AbsoluteFill style={{ background: "#0d0c14" }}>')
L.append('      {/* camada de tela (cortes + zoom, vinda do render.py --camada-tela) */}')
L.append(f'      '+('<PalcoTela>' if EXTRAS else '')+f'<Sequence name="Tela" from={{0}} durationInFrames={{{TQ}}} premountFor={{fps}}><Tela src={{staticFile("tela.mp4")}} costuras={{COSTURAS}} escala={{E}} /></Sequence>'+('</PalcoTela>' if EXTRAS else ''))
L.append('      {/* cenas de motion (gravadas pelo HyperFrames) */}')
for c in cenas:
    ent = {'abertura': 'nenhuma', 'meio': 'empurrao', 'fechamento': 'reverso'}[c['tipo']]; sai = 'nenhuma' if c['tipo'] == 'fechamento' else 'curva'
    q_a, q_b = int(round(c['ini'] * FPS)), int(round((c['ini'] + c['dur']) * FPS))   # fim arredondado (não a duração): sem buraco de 1 quadro
    L.append(f'      <Sequence name="{c["nome"]}" from={{{q_a}}} durationInFrames={{{q_b - q_a}}} premountFor={{fps}}>'
             f'<Cena src={{staticFile("cenas/{c["nome"]}.mp4")}} entrada="{ent}" saida="{sai}" dur={{{c["dur"]:.3f}}} escala={{E}} /></Sequence>')
L.append('      {/* câmera do apresentador: um bloco por lugar (voa até o próximo); cada trecho do bruto, na ordem dos cortes */}')
if EXTRAS: L.append('      <PalcoCamera>')
for bi, bl in enumerate(blocos):
    Lg = LUGARES[bl['k']]; q_a = bl['tr'][0]['q0']; q_b = bl['tr'][-1]['q0'] + bl['tr'][-1]['nq']
    prox = LUGARES[blocos[bi + 1]['k']]['saida'] if bi + 1 < len(blocos) else None
    some = f" someEm={{{fecha - q_a / FPS:.3f}}}" if fecha and q_a / FPS <= fecha < q_b / FPS + 1 else ''
    L.append(f'      <Sequence name="câmera · lugar {bl["k"]}" from={{{q_a}}} durationInFrames={{{q_b - q_a}}} premountFor={{fps}}>')
    L.append(f'        <MolduraMovel rect={{{json.dumps(Lg["saida"])}}}{f" vai={{{json.dumps(prox)}}}" if prox else ""} dur={{{(q_b - q_a) / FPS:.3f}}} escala={{E}} raio={{{raio}}}{some}>')
    for i, e in enumerate(bl['tr']):   # inteiros do plano: os trechos encostam (q0 + nq = próximo q0) e casam com a voz
        vel = f' velocidade={{{e["vel"]}}}' if e['vel'] != 1 else ''
        zm = f' zoom={{{1.1 if i % 2 else 1}}}' if Lg.get('punch') else ''
        L.append(f'          <Sequence name="câmera {edl["trechos"].index(e) + 1:02d}" from={{{e["q0"] - q_a}}} durationInFrames={{{e["nq"]}}} premountFor={{fps}}>'
                 f'<TrechoCam src={{staticFile("{Lg["arq"]}")}} trimBefore={{{e["q_in"]}}}{vel}{zm} /></Sequence>')
    L.append('        </MolduraMovel>\n      </Sequence>')
if EXTRAS: L.append('      </PalcoCamera>')
L.append('      {/* capítulos */}')
def bloco_em(t):
    q = int(round(t * FPS))
    for bl in blocos:
        if bl['tr'][0]['q0'] <= q < bl['tr'][-1]['q0'] + bl['tr'][-1]['nq']: return LUGARES[bl['k']]
    return LUGARES[-1]
for ini, n, txt in C.get('capitulos', []):
    sx, sy, sw, sh = bloco_em(ini)['saida']; direita = sx + sw / 2 > OW / E / 2   # câmera à direita: etiqueta cresce para a esquerda
    L.append(f'      <Sequence name="capítulo {n}" from={{{int(round(ini * FPS))}}} durationInFrames={{{3 * FPS}}} premountFor={{fps}}><Capitulo n={{{n}}} texto={json.dumps(txt, ensure_ascii=False)} x={{{sx + sw if direita else sx}}} base={{{sy - 18}}} escala={{E}}{" direita" if direita else ""}{TEMA} /></Sequence>')
L.append('      {/* selos de status por cima (ex.: estado do SLA durante o teste ao vivo) */}')
for s_ in C.get('selos', []):
    q_a, q_b = int(round(s_['ini'] * FPS)), int(round(s_['fim'] * FPS))
    est = [[round(t_ - s_['ini'], 3), c_, x_] for t_, c_, x_ in s_['estados']]
    L.append(f'      <Sequence name="selo {s_["rotulo"]}" from={{{q_a}}} durationInFrames={{{q_b - q_a}}} premountFor={{fps}}><SeloStatus rotulo={json.dumps(s_["rotulo"], ensure_ascii=False)} estados={{{json.dumps(est, ensure_ascii=False)}}} dur={{{(q_b - q_a) / FPS:.3f}}} escala={{E}}{TEMA} /></Sequence>')
if EXTRAS: L.append('      <Extras />')
L.append('      {/* áudio: voz tratada + um whoosh discreto em cada empurrão */}')
L.append('      <Audio src={staticFile("voz.wav")} />')
if C.get('trilha'):   # música de fundo já mixada no nível certo (ex.: ~18 dB abaixo da voz, sobe no fechamento)
    liga(J(C['trilha']), 'trilha.wav'); L.append('      <Audio src={staticFile("trilha.wav")} />')
if tem_whoosh:
    for c in costuras:
        if c['tipo'] in ('entra-cena', 'fechamento') and c['t'] > .05:
            L.append(f'      <Sequence name="whoosh {c["t"]:.1f}s" from={{{max(0, int(round((c["t"] - .28) * FPS)))}}} durationInFrames={{{FPS}}}><Audio src={{staticFile("sfx/whoosh.wav")}} volume={{0.16}} /></Sequence>')
L.append('    </AbsoluteFill>\n  );\n};\n')
open(os.path.join(R, 'src', 'Aula.tsx'), 'w').write('\n'.join(L))
print(f'Remotion: {len(cenas)} cenas, {len(edl["trechos"])} trechos de câmera em {len(blocos)} lugar(es), {len(C.get("capitulos", []))} capítulos, {fim:.1f}s → {R}/src/Aula.tsx')

# ---------- render: Remotion (vídeo quase sem perda + som PCM, numa passada) na fila global → finalizar.py (padrão de entrega) ----------
shutil.copy(os.path.join(MODELO, 'remotion.config.ts'), os.path.join(R, 'remotion.config.ts'))
final = J(saida)
sh = f"""#!/bin/bash
# GERADO por gerar_remotion.py — render na fila global (um por vez no computador) + finalização no padrão de entrega.
set -e; cd "$(dirname "$0")"; mkdir -p out
F=$HOME/.cache/motion-studio-fila-render; mkdir -p $HOME/.cache
until mkdir "$F" 2>/dev/null; do sleep 2; done; trap 'rmdir "$F" 2>/dev/null' EXIT; export MOTION_FILA=1
t0=$(date +%s)
# uma passada: vídeo quase sem perda + áudio PCM (sem AAC no meio). Render só do áudio (--codec=wav) custava 4 min a mais.
npx remotion render Aula out/montagem.mkv --codec=h264 --crf=10 --x264-preset=veryfast --audio-codec=pcm-16 --log=error "$@"
"{sys.executable.replace(os.sep, '/')}" "{os.path.abspath(os.path.join(os.path.dirname(__file__), 'finalizar.py')).replace(os.sep, '/')}" out/montagem.mkv "{final}"
echo "montagem + finalização em $(( $(date +%s) - t0 ))s"
"""
open(os.path.join(R, 'renderizar.sh'), 'w', newline='\n').write(sh)   # LF: com CRLF (Windows) o bash quebra na 1ª linha
os.chmod(os.path.join(R, 'renderizar.sh'), 0o755)
print(f'render: bash {R}/renderizar.sh  → {final}')
