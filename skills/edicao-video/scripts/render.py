"""Monta o vídeo editado: cortes (edl.json), zoom que segue a ação (zoom.json), câmera do apresentador fixa
por cima (nunca entra no zoom), cenas de motion intercaladas, camadas transparentes (capítulos) e áudio tratado.
uso:
  python render.py fonte/edicao.json                       → vídeo final ("saida" no edicao.json)
  python render.py fonte/edicao.json --quadros 12.5,40,88  → só fotos desses tempos (fonte/revisao/), para conferir rápido
  python render.py fonte/edicao.json --previa              → 960×540 rápido para assistir
  python render.py fonte/edicao.json --partes 4             → o mesmo vídeo em 4 processos paralelos (decodifica na GPU se houver), junta no fim
  python render.py fonte/edicao.json --trecho 60,64 [--crf N | --sem-perda]  → só um pedaço, sem áudio (teste de qualidade)
  python render.py fonte/edicao.json --camada-tela [--crf 10] → só a tela (cortes+zoom, câmera tapada) + voz, para montar no Remotion
edicao.json:
  bruto, saida, crf (padrão 14), escala (1 = resolução do bruto; 2 = 4K a partir de 1080p — recomendado para YouTube)
  camera [x,y,w,h] px EXATOS (medir: primeiro/último pixel escuro), camera_raio, camera_recuo (px que o recorte entra, padrão 2)
  camera_fora [[ini, fim], ...] (s do bruto): a câmera mudou de lugar → quadro original, sem colar câmera nem zoom
  borda (px de faixa preta nas laterais), nitidez (0–1, padrão .35: realce leve no que sofre zoom)
  motions [{arquivo, ini, fade}]  → tela cheia (a câmera vem por cima, a menos que "sem_camera": true)
  camadas [{arquivo, ini}]        → .mov ProRes 4444 com alfa, por cima de tudo (capítulos, selos)
  fusao (s, padrão .25): emenda marcada com "fusao" no edl (tela mudou no corte) entra fundindo o último quadro com o novo."""
import sys, os, json, subprocess
import numpy as np, cv2

cfg = sys.argv[1]; base = os.path.dirname(os.path.abspath(cfg)); C = json.load(open(cfg))
arg = sys.argv[2:]
J = lambda p: os.path.join(base, p)
edl = json.load(open(J('edl.json'))); ZK = json.load(open(J('zoom.json'))) if os.path.exists(J('zoom.json')) else [{'t': 0, 'z': 1, 'cx': .5, 'cy': .5}]
BRUTO = J(C['bruto']); DUR = edl['dur']; FPS = C.get('fps', 30)   # padrão do dono desde 13/10/2026: 1080p30 (escala 1, fps 30)
def probe(p):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                        '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip().split(',')
    return int(o[0]), int(o[1]), (lambda a, b: int(a) / int(b))(*o[2].split('/'))
VW, VH, SFPS = probe(BRUTO)
previa = '--previa' in arg
# --camada-tela: para montar no Remotion — sai <saida>-tela.mp4 (só a tela, câmera tapada, sem motions) + <saida>-voz.m4a
CAMADA = '--camada-tela' in arg
if CAMADA: C['motions'] = []; C['camadas'] = []
E = 1 if previa else C.get('escala', 1)
OW, OH = int(VW * E), int(VH * E)
TR = C.get('zoom_transicao', .8)
BORDA = C.get('borda', 0); BW = (VW - 2 * BORDA) / VW; BX = BORDA / VW; BY = (1 - BW) / 2
NIT = C.get('nitidez', .35); FUS = C.get('fusao', .25)
COLOR = 'scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709,format=bgr24'

def fonte(t):
    for e in edl['trechos']:
        d = (e['out'] - e['in']) / e['vel']
        if e['ini'] - 1e-6 <= t < e['ini'] + d: return e['in'] + (t - e['ini']) * e['vel'], e
    e = edl['trechos'][-1]; return e['out'] - 1 / SFPS, e

def suave(x): x = min(1, max(0, x)); return x * x * x * (x * (x * 6 - 15) + 10)

def vista(t):
    """retângulo visível (x0, y0, w) em 0–1 do bruto, interpolado entre as mudanças de zoom"""
    rect = lambda k: (k['cx'] - .5 / k['z'], k['cy'] - .5 / k['z'], 1 / k['z'])
    cur = rect(ZK[0])
    for i, k in enumerate(ZK[1:], 1):
        if t < k['t']: break
        prox = ZK[i + 1]['t'] if i + 1 < len(ZK) else 1e9
        d = min(TR, max(.25, prox - k['t']))
        a = suave((t - k['t']) / d); alvo = rect(k)
        cur = tuple(c + (b - c) * a for c, b in zip(cur, alvo))
    if BORDA: x0, y0, w = cur; return (BX + x0 * BW, BY + y0 * BW, w * BW)
    return cur

# ---------- câmera: recorte exato, um pouco para dentro (a borda clara/suavizada do original não vaza) ----------
# camera_fora [[ini, fim], ...] em segundos do BRUTO: trechos em que a câmera saiu do lugar (cena do OBS trocada)
FORA = C.get('camera_fora', []); CAM_FORA = False
CX, CY, CW, CH = C.get('camera', [0, 0, 0, 0]); RE = C.get('camera_recuo', 2); RAIO = C.get('camera_raio', 20)
if CW:
    # retângulo de destino na saída (mesmo lugar, escalado)
    ox, oy, ow, oh = int(round(CX * E)), int(round(CY * E)), int(round(CW * E)), int(round(CH * E))
    r_in = int(RE * E); rr = int(RAIO * E)
    mask = np.zeros((oh, ow), np.uint8)
    x0, y0, x1, y1 = r_in, r_in, ow - 1 - r_in, oh - 1 - r_in
    cv2.rectangle(mask, (x0 + rr, y0), (x1 - rr, y1), 255, -1); cv2.rectangle(mask, (x0, y0 + rr), (x1, y1 - rr), 255, -1)
    for cx_, cy_ in [(x0 + rr, y0 + rr), (x1 - rr, y0 + rr), (x0 + rr, y1 - rr), (x1 - rr, y1 - rr)]:
        cv2.circle(mask, (cx_, cy_), rr, 255, -1, cv2.LINE_AA)
    mask = cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), .8 * E)[..., None]   # borda macia de ~1 px
    PAD = int(40 * E)
    sombra = np.zeros((oh + 2 * PAD, ow + 2 * PAD), np.float32); sombra[PAD:PAD + oh, PAD:PAD + ow] = mask[..., 0]
    sombra = (cv2.GaussianBlur(sombra, (0, 0), 14 * E) * .45)[..., None]
    # versões prontas para as operações nativas do OpenCV (mistura numpy em float custava ~16 ms por quadro em 4K)
    MASK2, MASK2I = np.ascontiguousarray(mask[..., 0]), np.ascontiguousarray(1 - mask[..., 0])
    SOMBRA3 = np.repeat(1 - sombra, 3, axis=2).astype(np.float32)

def tapar_camera(img):
    """no fundo que vai sofrer zoom, a câmera some e o lugar dela é reconstruído com a vizinhança (inpainting).
    Com zoom, esse retângulo cresce para fora da câmera colada por cima: cor chapada aparecia como bloco (achado do revisor).
    Calculado em 1/4 da resolução (rápido) e ampliado: o que aparece é só a borda, desfocada como a tela em volta."""
    if not CW or CAM_FORA: return img
    M_ = 24; x0, y0 = max(0, CX - 3 - M_), max(0, CY - 3 - M_); x1, y1 = min(VW, CX + CW + 3 + M_), min(VH, CY + CH + 3 + M_)
    reg = img[y0:y1, x0:x1]; h, w = reg.shape[:2]
    pq = cv2.resize(reg, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
    mk = np.zeros(pq.shape[:2], np.uint8)
    mk[(CY - 3 - y0) // 4:(CY + CH + 3 - y0) // 4 + 1, (max(0, CX - 3) - x0) // 4:(CX + CW + 3 - x0) // 4 + 1] = 255
    rec = cv2.resize(cv2.inpaint(pq, mk, 5, cv2.INPAINT_TELEA), (w, h), interpolation=cv2.INTER_CUBIC)
    img[CY - 3:CY + CH + 3, max(0, CX - 3):CX + CW + 3] = rec[CY - 3 - y0:CY + CH + 3 - y0, max(0, CX - 3) - x0:CX + CW + 3 - x0]
    return img

def por_camera(out, src):
    if not CW or CAMADA or CAM_FORA: return out
    y0, x0 = oy + int(10 * E) - PAD, ox - PAD
    y0c, x0c = max(0, y0), max(0, x0)
    reg = out[y0c:y0 + sombra.shape[0], x0c:x0 + sombra.shape[1]]
    s = sombra[y0c - y0:y0c - y0 + reg.shape[0], x0c - x0:x0c - x0 + reg.shape[1]]
    s3 = SOMBRA3[y0c - y0:y0c - y0 + reg.shape[0], x0c - x0:x0c - x0 + reg.shape[1]]
    out[y0c:y0c + reg.shape[0], x0c:x0c + reg.shape[1]] = cv2.multiply(reg, s3, dtype=cv2.CV_8U)
    cam = src[CY:CY + CH, CX:CX + CW]
    if E != 1: cam = cv2.resize(cam, (ow, oh), interpolation=cv2.INTER_LANCZOS4)
    dst = out[oy:oy + oh, ox:ox + ow]
    out[oy:oy + oh, ox:ox + ow] = cv2.blendLinear(np.ascontiguousarray(cam), np.ascontiguousarray(dst), MASK2, MASK2I)
    return out

# ---------- selo de aceleração (só se o plano ainda acelerar algum trecho) ----------
def selo(texto):
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype('/System/Library/Fonts/SFNSRounded.ttf', int(30 * E))
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    w = int(f.getlength(texto)) + int(46 * E); h = int(54 * E)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(13, 12, 20, 215))
    d.text((int(23 * E), h // 2), texto, font=f, fill=(244, 243, 248, 255), anchor='lm')
    a = np.array(im).astype(np.float32); return a[..., [2, 1, 0]], a[..., 3:] / 255
SELOS = {}
def por_selo(out, e, t):
    if e['tipo'] != 'acelerado': return out
    k = f"▶▶  {e['vel']:g}×"
    if k not in SELOS: SELOS[k] = selo(k)
    rgb, al = SELOS[k]
    ap = suave((t - e['ini']) / .25) * suave((e['ini'] + (e['out'] - e['in']) / e['vel'] - t) / .25)
    x, y = (ox + int(18 * E), oy - al.shape[0] - int(18 * E)) if CW else (int(60 * E), int(60 * E))
    reg = out[y:y + al.shape[0], x:x + al.shape[1]].astype(np.float32); a = al * ap
    out[y:y + al.shape[0], x:x + al.shape[1]] = (rgb * a + reg * (1 - a)).astype(np.uint8)
    return out

# ---------- motions (tela cheia) e camadas (alfa) ----------
def carregar(lista, alfa):
    out = []
    for m in lista:
        p = J(m['arquivo'])
        if not os.path.exists(p): print('  (sem o arquivo ainda)', m['arquivo']); continue
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
        out.append({**m, 'p': p, 'dur': d, 'proc': None, 'lidos': 0, 'quadro': None, 'alfa': alfa})
    return out
MOT = carregar(C.get('motions', []), False); CAM_ = carregar(C.get('camadas', []), True)
def ativo(lista, t):
    for m in lista:
        if m['ini'] <= t < m['ini'] + m['dur']: return m
    return None
def peso_motion(m, t):
    f = m.get('fade', .4)
    a = 1.0 if m['ini'] == 0 else suave((t - m['ini']) / f)
    return a * (suave((m['ini'] + m['dur'] - t) / f) if m['ini'] + m['dur'] < DUR - .05 else 1)
# motions: deixa o ffmpeg ler a cor marcada no arquivo (o gravador do Chrome sai em faixa completa BT.601;
# forçar "tv/bt709" como no bruto muda o contraste)
def _vf(m): return f"scale={OW}:{OH}:flags=lanczos,format=" + ('bgra' if m['alfa'] else 'bgr24')
def quadro_seq(m, t):
    """lê a peça em sequência (o vídeo editado anda para a frente)"""
    alvo = int(round((t - m['ini']) * FPS)); nb = OW * OH * (4 if m['alfa'] else 3)
    if m['proc'] is None:
        m['proc'] = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', m['p'], '-vf', _vf(m), '-f', 'rawvideo', '-'], stdout=subprocess.PIPE, bufsize=nb * 2)
    while m['lidos'] <= alvo:
        b = m['proc'].stdout.read(nb)
        if len(b) < nb: break
        m['quadro'] = np.frombuffer(b, np.uint8).reshape(OH, OW, -1); m['lidos'] += 1
    return m['quadro']
def quadro_solto(m, t):
    nb = OW * OH * (4 if m['alfa'] else 3)
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t - m["ini"]:.3f}', '-i', m['p'], '-frames:v', '1', '-vf', _vf(m), '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(OH, OW, -1) if len(b) == nb else None
def por_alfa(out, q):
    if q is None: return out
    a = q[..., 3]
    pts = cv2.findNonZero(a)
    if pts is None: return out
    x, y, w, h = cv2.boundingRect(pts)
    al = a[y:y + h, x:x + w, None].astype(np.float32) / 255
    out[y:y + h, x:x + w] = (q[y:y + h, x:x + w, :3] * al + out[y:y + h, x:x + w] * (1 - al)).astype(np.uint8)
    return out

# ---------- composição de um quadro ----------
def compor(src, t, e, motion=None, a_mot=0, camada=None):
    global CAM_FORA
    CAM_FORA = any(a <= fonte(t)[0] <= b for a, b in FORA)   # câmera fora do lugar nesse trecho do bruto
    m = ativo(MOT, t)
    sem_cam = bool(m and m.get('sem_camera'))
    if motion is not None and a_mot >= 1:
        out = motion.copy() if sem_cam else por_camera(motion.copy(), src)
    else:
        fundo = tapar_camera(src.copy())
        x0, y0, w = (0, 0, 1) if CAM_FORA else vista(t)   # câmera mudou de lugar: quadro original, sem zoom
        z = E / w   # um único redimensionamento: bruto → saída (zoom + escala juntos)
        if NIT > 0 and z > 1.05 and not previa:   # realce leve (compensa a moleza do aumento), feito ANTES de ampliar:
            # mesmo efeito do realce no 4K com sigma .9·z, com 4× menos pixels (25 ms → ~6 ms por quadro)
            fundo = cv2.addWeighted(fundo, 1 + NIT, cv2.GaussianBlur(fundo, (0, 0), .9), -NIT, 0)
        parado = vista(t - 1 / FPS) == (x0, y0, w) if not CAM_FORA else True
        if parado and not previa:
            # enquadramento parado: recorte + resize Lanczos, 4× mais rápido que o warpAffine e mesma imagem (desvio de sub-pixel constante)
            X0, Y0 = int(round(x0 * VW)), int(round(y0 * VH)); X1, Y1 = int(round((x0 + w) * VW)), int(round((y0 + w) * VH))
            X0, Y0 = max(0, X0), max(0, Y0); X1, Y1 = min(VW, X1), min(VH, Y1)
            rec = fundo[Y0:Y1, X0:X1]
            # 1080p sem zoom: o recorte já é o quadro de saída (nada a redimensionar)
            tela = rec.copy() if rec.shape[1] == OW and rec.shape[0] == OH else cv2.resize(rec, (OW, OH), interpolation=cv2.INTER_LANCZOS4)
        else:
            M = np.float32([[z, 0, -x0 * VW * z], [0, z, -y0 * VH * z]])
            tela = cv2.warpAffine(fundo, M, (OW, OH), flags=cv2.INTER_LANCZOS4 if not previa else cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        if motion is not None and a_mot > 0:
            if sem_cam:   # cena sem câmera (fechamento): a câmera some junto com a fusão
                out = cv2.addWeighted(motion, a_mot, por_camera(tela, src), 1 - a_mot, 0)
            else:
                out = por_camera(cv2.addWeighted(motion, a_mot, tela, 1 - a_mot, 0), src)
        else:
            out = por_camera(tela, src)
    out = por_selo(out, e, t)
    return por_alfa(out, camada)

# ---------- modo fotos ----------
if '--quadros' in arg:
    pasta = J('revisao'); os.makedirs(pasta, exist_ok=True)
    for t in [float(x) for x in arg[arg.index('--quadros') + 1].split(',')]:
        s, e = fonte(t)
        b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{s:.3f}', '-i', BRUTO, '-frames:v', '1', '-vf', COLOR, '-f', 'rawvideo', '-'], capture_output=True).stdout
        src = np.frombuffer(b, np.uint8).reshape(VH, VW, 3)
        m = ativo(MOT, t); c = ativo(CAM_, t)
        out = compor(src, t, e, quadro_solto(m, t) if m else None, peso_motion(m, t) if m else 0, quadro_solto(c, t) if c else None)
        cv2.imwrite(os.path.join(pasta, f'q{t:07.2f}.jpg'), cv2.resize(out, (960, 540), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 90])
        if '--cheio' in arg: cv2.imwrite(os.path.join(pasta, f'q{t:07.2f}-cheio.png'), out)
    print('fotos em', pasta); sys.exit()

# ---------- vídeo ----------
saida = J(C.get('saida', 'editado.mp4'))
if previa: saida = saida.replace('.mp4', '-previa.mp4')
TRECHO = [float(x) for x in arg[arg.index('--trecho') + 1].split(',')] if '--trecho' in arg else None
# --parte i/N: este processo grava só a faixa i de N (lançado pelo --partes N); --partes N: grava N faixas em paralelo e junta
PARTE = tuple(map(int, arg[arg.index('--parte') + 1].split('/'))) if '--parte' in arg else None
PARTES = int(arg[arg.index('--partes') + 1]) if '--partes' in arg else 1
# processos em paralelo dividem os núcleos: sem isso cada um pede todos os threads do OpenCV e eles brigam (3 partes ficaram MAIS lentas que 1)
_thr = int(os.environ.get('RENDER_THREADS', 0)) or (max(1, (os.cpu_count() or 4) // PARTE[1]) if PARTE else 0)
if _thr: cv2.setNumThreads(_thr)
if '--crf' in arg: C['crf'] = int(arg[arg.index('--crf') + 1])
if TRECHO: saida = saida.replace('.mp4', f"-trecho-{'sem-perda' if '--sem-perda' in arg else 'crf' + str(C.get('crf', 14))}.mkv")
tmpv, tmpa = saida + '.video.mp4', saida + '.audio.m4a'
PARTE_ARQ = f'{saida}.parte{PARTE[0]:02d}.mp4' if PARTE else None

if not TRECHO and not PARTE:
    # áudio: trechos de fala colados com micro-fades; acelerados viram silêncio; voz tratada e -16 LUFS (duas passadas)
    fc, n = [], 0
    for e in edl['trechos']:
        d = (e['out'] - e['in']) / e['vel']
        if e['tipo'] == 'fala':
            fc.append(f"[0:a]atrim={e['in']:.4f}:{e['out']:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={max(0, d - .008):.4f}:d=0.008[a{n}]")
        else:
            fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{d:.4f}[a{n}]")
        n += 1
    # fim com cena sem fala (ex.: fechamento): silêncio até o fim do último motion
    fim_mot = max([m['ini'] + m['dur'] for m in MOT] + [DUR])
    if fim_mot > DUR + .01:
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{fim_mot - DUR:.4f}[a{n}]"); n += 1
    VOZ = C.get('voz', 'highpass=f=70,acompressor=threshold=-21dB:ratio=2.5:attack=8:release=120:makeup=2')
    fc.append(''.join(f'[a{i}]' for i in range(n)) + f'concat=n={n}:v=0:a=1,{VOZ}[m]')
    fcs = ';'.join(fc)
    med = subprocess.run(['ffmpeg', '-v', 'info', '-i', BRUTO, '-filter_complex', fcs + ';[m]loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json[o]',
                          '-map', '[o]', '-f', 'null', '-'], capture_output=True, text=True).stderr
    L = json.loads(med[med.rindex('{'):med.rindex('}') + 1])
    ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={L['input_i']}:measured_TP={L['input_tp']}:measured_LRA={L['input_lra']}"
          f":measured_thresh={L['input_thresh']}:offset={L['target_offset']}:linear=true")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', BRUTO, '-filter_complex', fcs + f';[m]{ln},aresample=48000[o]', '-map', '[o]',
                    '-c:a', 'aac', '-b:a', '256k', tmpa], check=True)
    print('áudio pronto', flush=True)
    if PARTES > 1:
        # cada parte é um processo próprio (o Python monta 1 quadro por vez; a máquina tem núcleos sobrando)
        procs = [subprocess.Popen([sys.executable, os.path.abspath(__file__), cfg, '--parte', f'{i}/{PARTES}', *[x for x in arg if x not in ('--partes', str(PARTES))]])
                 for i in range(1, PARTES + 1)]
        if any(p.wait() for p in procs): sys.exit('uma parte falhou')
        lista = saida + '.partes.txt'
        open(lista, 'w').write(''.join(f"file '{os.path.basename(saida)}.parte{i:02d}.mp4'\n" for i in range(1, PARTES + 1)))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lista, '-i', tmpa, '-map', '0:v', '-map', '1:a', '-c', 'copy',
                        '-movflags', '+faststart', saida], check=True, cwd=os.path.dirname(saida))
        for i in range(1, PARTES + 1): os.remove(f'{saida}.parte{i:02d}.mp4')
        os.remove(lista); os.remove(tmpa); print('pronto:', saida); sys.exit()

POW, POH = (960, 540) if previa else (OW, OH)
HW = (['-hwaccel', 'videotoolbox'] if sys.platform == 'darwin' else
      ['-hwaccel', 'cuda'] if 'cuda' in subprocess.run(['ffmpeg', '-hide_banner', '-hwaccels'], capture_output=True, text=True).stdout else [])
fim_total = max([m['ini'] + m['dur'] for m in MOT] + [DUR])
total = int(round(fim_total * FPS))
if PARTE: k0, k1 = total * (PARTE[0] - 1) // PARTE[1], total * PARTE[0] // PARTE[1]
elif TRECHO: k0, k1 = int(TRECHO[0] * FPS), int(TRECHO[1] * FPS)
else: k0, k1 = 0, total
# começa a decodificar perto do 1º quadro da faixa (seek exato: o bruto começa em 0 e tem quadros constantes)
ini_q = max(0, int(fonte(min(k0 / FPS, DUR - 1e-3))[0] * SFPS) - 2) if (PARTE or TRECHO) else 0
SS = ['-ss', f'{(ini_q - .5) / SFPS:.6f}'] if ini_q else []   # medido: -0,5 quadro entrega exatamente o quadro ini_q (+0,5 entrega o seguinte)
dec = subprocess.Popen(['ffmpeg', '-v', 'error', *HW, *SS, '-i', BRUTO, '-an', '-vf', COLOR, '-f', 'rawvideo', '-'], stdout=subprocess.PIPE, bufsize=VW * VH * 3 * 4)
crf = str(C.get('crf', 14))
# NVENC (GPU NVIDIA) quando existir: tira a codificação 4K do CPU, que já está ocupado montando os quadros
NVENC = 'h264_nvenc' in subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], capture_output=True, text=True).stdout
enc_v = (['-c:v', 'ffv1'] if '--sem-perda' in arg else ['-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23'] if previa
         else ['-c:v', 'h264_nvenc', '-preset', 'p6', '-tune', 'hq', '-rc', 'vbr', '-cq', crf, '-b:v', '0', '-profile:v', 'high'] if NVENC
         else ['-c:v', 'libx264', '-preset', 'slow' if E == 1 else 'medium', '-crf', crf, '-profile:v', 'high', '-x264-params', 'aq-mode=3'])
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{POW}x{POH}', '-r', str(FPS), '-i', '-',
                        '-vf', 'scale=in_color_matrix=bt709:out_color_matrix=bt709:out_range=tv,format=yuv420p', *enc_v,
                        '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', *([] if TRECHO else ['-movflags', '+faststart']),
                        saida if TRECHO else PARTE_ARQ if PARTE else tmpv], stdin=subprocess.PIPE)
lidos, src = ini_q, None
ant, congelado, seg_ant, fora_ant, fora_cong = None, None, None, False, False
for k in range(k0 if (PARTE or TRECHO) else 0, k1):
    t = k / FPS; s, e = fonte(min(t, DUR - 1e-3))
    alvo = int(s * SFPS + 1e-6)
    while lidos <= alvo:
        b = dec.stdout.read(VW * VH * 3)
        if len(b) < VW * VH * 3: break
        src = np.frombuffer(b, np.uint8).reshape(VH, VW, 3); lidos += 1
    if e is not seg_ant: congelado, seg_ant, fora_cong = ant, e, fora_ant   # fora_cong: a câmera estava fora do lugar no quadro congelado?
    if k < k0: continue
    m = ativo(MOT, t); c = ativo(CAM_, t)
    out = compor(src, t, e, quadro_seq(m, t) if m else None, peso_motion(m, t) if m else 0, quadro_seq(c, t) if c else None)
    if e.get('fusao') and congelado is not None and t - e['ini'] < FUS and not (m and peso_motion(m, t) > .99) and CAM_FORA == fora_cong:
        out = cv2.addWeighted(congelado, 1 - suave((t - e['ini']) / FUS), out, suave((t - e['ini']) / FUS), 0)
    ant, fora_ant = out, CAM_FORA
    if previa: out = cv2.resize(out, (POW, POH), interpolation=cv2.INTER_AREA)
    enc.stdin.write(np.ascontiguousarray(out).tobytes())
    if k % 600 == 0: print(f'  {t:6.1f}s / {fim_total:.1f}s', flush=True)
enc.stdin.close(); enc.wait(); dec.kill()
for m in MOT + CAM_:
    if m['proc']: m['proc'].kill()
if TRECHO: print('pronto:', saida); sys.exit()
if PARTE: print('parte pronta:', PARTE_ARQ); sys.exit()
if CAMADA:
    base_ = saida[:-4]; os.replace(tmpv, base_ + '-tela.mp4'); os.replace(tmpa, base_ + '-voz.m4a')
    print('pronto:', base_ + '-tela.mp4', base_ + '-voz.m4a'); sys.exit()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmpv, '-i', tmpa, '-map', '0:v', '-map', '1:a', '-c', 'copy', '-movflags', '+faststart', saida], check=True)
os.remove(tmpv); os.remove(tmpa)
print('pronto:', saida)
