"""Monta o vídeo editado: cortes (edl.json), zoom que segue a ação (zoom.json), câmera do apresentador fixa
por cima (nunca entra no zoom), cenas de motion intercaladas, camadas transparentes (capítulos) e áudio tratado.
Sai no PADRÃO DE ENTREGA (scripts/padrao.py): 1920×1080, 30 fps, H.264 High 18 Mb/s constante, AAC 320 k, -14 LUFS, BT.709.
uso:
  python render.py fonte/edicao.json                       → vídeo final ("saida" no edicao.json)
  python render.py fonte/edicao.json --quadros 12.5,40,88  → só fotos desses tempos (fonte/revisao/), para conferir rápido
  python render.py fonte/edicao.json --previa              → 960×540 no codificador de hardware do Mac, para assistir
  python render.py fonte/edicao.json --trecho 60,64 [--crf N | --sem-perda]  → só um pedaço, sem áudio (teste de qualidade)
  python render.py fonte/edicao.json --camada-tela         → só a tela (cortes+zoom, câmera tapada) + voz.wav, para montar no Remotion
edicao.json:
  bruto (o NORMALIZADO: scripts/normalizar.py → bruto-30p.mov), saida, fps (padrão 30)
  escala: sem ela a saída é 1920×1080 venha o bruto em 1080p ou 4K; "escala": 2 = 4K a partir de 1080p (só se o dono pedir)
  camera [x,y,w,h] px EXATOS do bruto, camera_raio, camera_recuo (px que o recorte entra, padrão 2)
  cameras [[s_ini, s_fim, x, y, w, h], ...] (s do bruto): câmera que muda de canto — um retângulo por trecho
  camera_fora [[ini, fim], ...] (s do bruto): a câmera mudou de lugar (cena do OBS trocada) → quadro original, sem colar câmera nem zoom
  borda (px de faixa preta nas laterais), nitidez (0–1, padrão .35: realce leve no que sofre zoom)
  motions [{arquivo, ini, fade}]  → tela cheia (a câmera vem por cima, a menos que "sem_camera": true)
  camadas [{arquivo, ini}]        → .mov ProRes 4444 com alfa, por cima de tudo (capítulos, selos)
  fusao (s, padrão .25): emenda marcada com "fusao" no edl (tela mudou no corte) entra fundindo o último quadro com o novo.
Sincronia por construção: o quadro k do editado mostra o quadro q_in + (k − q0) do bruto (inteiros do edl, sem arredondar
tempo) e o áudio é cortado nas mesmas amostras (1 quadro = 1600 amostras); o áudio fica em PCM até a única codificação AAC."""
import sys, os, json, subprocess, time
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import padrao as P

T_INI = time.time()
cfg = sys.argv[1]; base = os.path.dirname(os.path.abspath(cfg)); C = json.load(open(cfg))
arg = sys.argv[2:]
J = lambda p: os.path.join(base, p)
edl = json.load(open(J('edl.json'))); ZK = json.load(open(J('zoom.json'))) if os.path.exists(J('zoom.json')) else [{'t': 0, 'z': 1, 'cx': .5, 'cy': .5}]
BRUTO = J(C['bruto']); FPS = C.get('fps', P.FPS)
INFO = P.probe(BRUTO); VW, VH, SFPS = INFO['w'], INFO['h'], INFO['fps']
previa = '--previa' in arg
if not ('--quadros' in arg or '--trecho' in arg):
    ok, txt = P.taxa_constante(BRUTO)
    if not ok:
        sys.exit(f'bruto fora do ritmo ({txt}).\nA câmera ia escorregar em relação à voz. Rode antes:\n'
                 f'  python {os.path.dirname(os.path.abspath(__file__))}/normalizar.py {BRUTO}\ne ponha o bruto-30p.mov no edicao.json.')
    if abs(SFPS - FPS) > 1e-3: print(f'aviso: bruto a {SFPS:g} fps e saída a {FPS} fps (funciona, mas normalizar.py deixa tudo no mesmo quadro)')

# trechos com quadros inteiros (plano.py novo). edl antigo, sem q0/nq: calcula (e avisa)
if 'q0' not in edl['trechos'][0] or edl.get('fps', FPS) != FPS:
    print('aviso: edl.json sem quadros inteiros (ou com outro fps) — rode plano.py de novo para sincronia exata')
    q = 0
    for e in edl['trechos']:
        e['q_in'] = round(e['in'] * FPS); e['nq'] = max(1, round((e['out'] - e['in']) / e['vel'] * FPS)); e['q0'] = q; e['ini'] = q / FPS; q += e['nq']
TQ = sum(e['nq'] for e in edl['trechos']); DUR = TQ / FPS

# --camada-tela: para montar no Remotion — sai <saida>-tela.mp4 (só a tela, câmera tapada, sem motions) + <saida>-voz.wav
CAMADA = '--camada-tela' in arg
if CAMADA: C['motions'] = []; C['camadas'] = []
if previa: OW, OH = 960, 540
elif 'escala' in C and C['escala'] != 1: OW, OH = int(VW * C['escala']), int(VH * C['escala'])
else: OW, OH = P.W, P.H
E = OW / VW
TR = C.get('zoom_transicao', .8)
BORDA = C.get('borda', 0); BW = (VW - 2 * BORDA) / VW; BX = BORDA / VW; BY = (1 - BW) / 2
NIT = C.get('nitidez', .35); FUS = C.get('fusao', .25)
COLOR = f"scale=in_color_matrix=bt709:in_range={'pc' if INFO['faixa'] == 'pc' else 'tv'}:out_color_matrix=bt709,format=bgr24"


def trecho_q(k):
    """quadro k do editado → (índice do quadro do bruto, trecho)"""
    lo, hi = 0, len(edl['trechos']) - 1
    while lo < hi:   # busca binária pelo último trecho com q0 ≤ k
        m = (lo + hi + 1) // 2
        if edl['trechos'][m]['q0'] <= k: lo = m
        else: hi = m - 1
    e = edl['trechos'][lo]; k = min(k, e['q0'] + e['nq'] - 1)
    return int(np.floor((e['q_in'] + (k - e['q0']) * e['vel']) * SFPS / FPS + 1e-4)), e


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
FORA = C.get('camera_fora', []); CAM_FORA = False
CX, CY, CW, CH = C.get('camera', [0, 0, 0, 0]); RE = C.get('camera_recuo', 2); RAIO = C.get('camera_raio', 20)
# câmera que muda de canto (Screen Studio/OBS movendo a bolha): "cameras": [[s_ini, s_fim, x, y, w, h], ...] em s do BRUTO.
# Cada trecho usa o seu retângulo (tapar e colar no mesmo lugar). Fora de todos os trechos vale "camera".
CAMS = C.get('cameras', [])
if CAMS and not CW: CX, CY, CW, CH = CAMS[0][2:6]   # 7º campo opcional ({"destino", "punch"}) é da montagem no Remotion
_PREP = {}


def preparar(cw, ch):
    """máscara de cantos arredondados + sombra para uma câmera de cw×ch (cache por tamanho)"""
    if (cw, ch) in _PREP: return _PREP[(cw, ch)]
    ow, oh = int(round(cw * E)), int(round(ch * E))
    r_in = int(RE * E); rr = int(RAIO * E)
    mask = np.zeros((oh, ow), np.uint8)
    x0, y0, x1, y1 = r_in, r_in, ow - 1 - r_in, oh - 1 - r_in
    cv2.rectangle(mask, (x0 + rr, y0), (x1 - rr, y1), 255, -1); cv2.rectangle(mask, (x0, y0 + rr), (x1, y1 - rr), 255, -1)
    for cx_, cy_ in [(x0 + rr, y0 + rr), (x1 - rr, y0 + rr), (x0 + rr, y1 - rr), (x1 - rr, y1 - rr)]:
        cv2.circle(mask, (cx_, cy_), rr, 255, -1, cv2.LINE_AA)
    mask = cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), .8 * E)[..., None]   # borda macia de ~1 px
    pad = int(40 * E)
    sombra = np.zeros((oh + 2 * pad, ow + 2 * pad), np.float32); sombra[pad:pad + oh, pad:pad + ow] = mask[..., 0]
    sombra = (cv2.GaussianBlur(sombra, (0, 0), 14 * E) * .45)[..., None]
    # prontos para as operações nativas do OpenCV (mistura em float no numpy custava ~16 ms por quadro em 4K)
    _PREP[(cw, ch)] = (ow, oh, pad, sombra, np.ascontiguousarray(mask[..., 0]), np.ascontiguousarray(1 - mask[..., 0]),
                       np.repeat(1 - sombra, 3, axis=2).astype(np.float32))
    return _PREP[(cw, ch)]


def usar_camera(s):
    """escolhe o retângulo da câmera para o instante s do bruto (só muda algo com "cameras")"""
    global CX, CY, CW, CH, ox, oy, ow, oh, PAD, sombra, MASK2, MASK2I, SOMBRA3
    if CAMS:
        for a_, b_, *r_ in CAMS:
            if a_ <= s < b_: CX, CY, CW, CH = r_[:4]; break
    if CW:
        ow, oh, PAD, sombra, MASK2, MASK2I, SOMBRA3 = preparar(CW, CH)
        ox, oy = int(round(CX * E)), int(round(CY * E))


usar_camera(0)


def tapar_camera(img):
    """no fundo que vai sofrer zoom, a câmera some e o lugar dela é reconstruído com a vizinhança (inpainting).
    Com zoom, esse retângulo cresce para fora da câmera colada por cima: cor chapada aparecia como bloco.
    Calculado em 1/4 da resolução e ampliado: o que aparece é só a borda, desfocada como a tela em volta."""
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
    s3 = SOMBRA3[y0c - y0:y0c - y0 + reg.shape[0], x0c - x0:x0c - x0 + reg.shape[1]]
    out[y0c:y0c + reg.shape[0], x0c:x0c + reg.shape[1]] = cv2.multiply(reg, s3, dtype=cv2.CV_8U)
    cam = src[CY:CY + CH, CX:CX + CW]
    if (ow, oh) != (CW, CH): cam = cv2.resize(cam, (ow, oh), interpolation=cv2.INTER_LANCZOS4 if E > 1 else cv2.INTER_AREA)
    dst = out[oy:oy + oh, ox:ox + ow]
    out[oy:oy + oh, ox:ox + ow] = cv2.blendLinear(np.ascontiguousarray(cam), np.ascontiguousarray(dst), MASK2, MASK2I)
    return out


# ---------- selo de aceleração (só se o plano ainda acelerar algum trecho) ----------
def selo(texto):
    from PIL import Image, ImageDraw, ImageFont
    # fonte do sistema: Mac (SF Rounded), Windows (Segoe UI negrito), Linux (DejaVu); sem nenhuma, a padrão do Pillow
    for arq in ('/System/Library/Fonts/SFNSRounded.ttf', 'C:/Windows/Fonts/segoeuib.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
        if os.path.exists(arq): f = ImageFont.truetype(arq, int(30 * E)); break
    else: f = ImageFont.load_default(int(30 * E))
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
    ap = suave((t - e['ini']) / .25) * suave((e['ini'] + e['nq'] / FPS - t) / .25)
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
# motions: deixa o ffmpeg ler a cor marcada no arquivo (o gravador do Chrome sai em faixa completa BT.601; forçar "tv/bt709"
# como no bruto muda o contraste). fps=FPS: motion gravado a 60 (ou 24) entra no ritmo certo, pelo tempo de cada quadro
# (sem isso, um motion de 60 fps lido quadro a quadro numa saída de 30 andaria na metade da velocidade)
def _vf(m): return f"fps={FPS},scale={OW}:{OH}:flags=lanczos,format=" + ('bgra' if m['alfa'] else 'bgr24')
def quadro_seq(m, t):
    """lê a peça em sequência (o vídeo editado anda para a frente)"""
    alvo = int(round((t - m['ini']) * FPS)); nb = OW * OH * (4 if m['alfa'] else 3)
    if m['proc'] is None:
        ss = max(0, alvo - 1) / FPS   # parte do vídeo que começa no meio de uma peça: pula até lá
        m['proc'] = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', m['p'], '-vf', _vf(m), '-ss', f'{ss:.4f}', '-f', 'rawvideo', '-'],
                                     stdout=subprocess.PIPE, bufsize=nb * 2)
        m['lidos'] = int(round(ss * FPS))
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
def compor(src, t, s, e, motion=None, a_mot=0, camada=None):
    """src = quadro do bruto (instante s do bruto); t = tempo no editado"""
    global CAM_FORA
    CAM_FORA = any(a <= s <= b for a, b in FORA); usar_camera(s)
    m = ativo(MOT, t)
    sem_cam = bool(m and m.get('sem_camera'))
    if motion is not None and a_mot >= 1:
        out = motion.copy() if sem_cam else por_camera(motion.copy(), src)
    else:
        fundo = tapar_camera(src.copy())
        x0, y0, w = (0, 0, 1) if CAM_FORA else vista(t)
        z = E / w   # um único redimensionamento: bruto → saída (zoom + escala juntos)
        if NIT > 0 and z > 1.05 and not previa:   # realce leve antes de ampliar (mesmo efeito, 4× menos pixels)
            fundo = cv2.addWeighted(fundo, 1 + NIT, cv2.GaussianBlur(fundo, (0, 0), .9), -NIT, 0)
        parado = CAM_FORA or vista(t - 1 / FPS) == (x0, y0, w)
        if parado and not previa:
            # enquadramento parado: recorte + resize (4× mais rápido que o warpAffine, mesma imagem)
            X0, Y0 = int(round(x0 * VW)), int(round(y0 * VH)); X1, Y1 = int(round((x0 + w) * VW)), int(round((y0 + w) * VH))
            X0, Y0 = max(0, X0), max(0, Y0); X1, Y1 = min(VW, X1), min(VH, Y1)
            rec = fundo[Y0:Y1, X0:X1]
            tela = rec.copy() if rec.shape[1] == OW and rec.shape[0] == OH else cv2.resize(
                rec, (OW, OH), interpolation=cv2.INTER_LANCZOS4 if rec.shape[1] < OW else cv2.INTER_AREA)
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
        i, e = trecho_q(min(TQ - 1, int(np.floor(t * FPS + 1e-6))))
        b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0, i - .25) / SFPS:.4f}', '-i', BRUTO, '-frames:v', '1', '-vf', COLOR, '-f', 'rawvideo', '-'],
                           capture_output=True).stdout
        src = np.frombuffer(b, np.uint8).reshape(VH, VW, 3)
        m = ativo(MOT, t); c = ativo(CAM_, t)
        out = compor(src, t, i / SFPS, e, quadro_solto(m, t) if m else None, peso_motion(m, t) if m else 0, quadro_solto(c, t) if c else None)
        cv2.imwrite(os.path.join(pasta, f'q{t:07.2f}.jpg'), cv2.resize(out, (960, 540), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 90])
        if '--cheio' in arg: cv2.imwrite(os.path.join(pasta, f'q{t:07.2f}-cheio.png'), out)
    print('fotos em', pasta); sys.exit()

# ---------- vídeo ----------
saida = J(C.get('saida', 'editado.mp4'))
if previa: saida = saida.replace('.mp4', '-previa.mp4')
TRECHO = [float(x) for x in arg[arg.index('--trecho') + 1].split(',')] if '--trecho' in arg else None
if TRECHO:
    rot = 'sem-perda' if '--sem-perda' in arg else ('crf' + arg[arg.index('--crf') + 1]) if '--crf' in arg else 'padrao'
    saida = saida.replace('.mp4', f'-trecho-{rot}.mkv')
tmpv, tmpa = saida + '.video.mp4', saida + '.voz.wav'
fim_total = max([m['ini'] + m['dur'] for m in MOT] + [DUR])
total = max(TQ, int(round(fim_total * FPS)))

if not TRECHO:
    P.fila()
    # áudio: trechos de fala cortados nas MESMAS amostras dos quadros, micro-fades; acelerados viram silêncio;
    # voz tratada e -14 LUFS (duas passadas). Fica em PCM (wav) até a única codificação AAC no fim.
    SRC_SR = INFO['sr'] or P.SR; spq = SRC_SR / FPS   # amostras por quadro (48 kHz / 30 = 1600)
    fc, n = [], 0
    for e in edl['trechos']:
        d = e['nq'] / FPS
        if e['tipo'] == 'fala':
            a0 = int(round(e['q_in'] * spq)); a1 = a0 + int(round(e['nq'] * spq))
            fc.append(f"[0:a]atrim=start_sample={a0}:end_sample={a1},asetpts=N/SR/TB,aresample={P.SR},"
                      f"afade=t=in:d=0.008,afade=t=out:st={max(0, d - .008):.4f}:d=0.008[a{n}]")
        else:
            fc.append(f"anullsrc=r={P.SR}:cl=stereo,atrim=end_sample={int(round(e['nq'] * P.SR / FPS))}[a{n}]")
        n += 1
    if total > TQ:   # fim com cena sem fala (ex.: fechamento): silêncio até o fim do último motion
        fc.append(f"anullsrc=r={P.SR}:cl=stereo,atrim=end_sample={int(round((total - TQ) * P.SR / FPS))}[a{n}]"); n += 1
    VOZ = C.get('voz', 'highpass=f=70,acompressor=threshold=-21dB:ratio=2.5:attack=8:release=120:makeup=2')
    fc.append(''.join(f'[a{i}]aformat=sample_rates={P.SR}:channel_layouts=stereo[b{i}];' for i in range(n))
              + ''.join(f'[b{i}]' for i in range(n)) + f'concat=n={n}:v=0:a=1,{VOZ}[m]')
    fcs = ';'.join(fc)
    ln = P.loudnorm(BRUTO, fcs)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', BRUTO, '-filter_complex', fcs + f';[m]{ln},aresample={P.SR}[o]', '-map', '[o]',
                    '-c:a', 'pcm_s16le', tmpa], check=True)
    print(f'áudio pronto ({time.time() - T_INI:.0f}s)', flush=True)

if TRECHO: k0, k1 = int(TRECHO[0] * FPS), int(TRECHO[1] * FPS)
else: k0, k1 = 0, total
kp = max(0, k0 - 1) if TRECHO else 0   # 1 quadro antes: a fusão da 1ª emenda da faixa precisa dele
# começa a decodificar perto do 1º quadro da faixa (bruto em ritmo constante: -0,5 quadro entrega exatamente o quadro ini_q)
ini_q = max(0, min(trecho_q(min(kp, TQ - 1))[0], trecho_q(min(k0, TQ - 1))[0]) - 2) if TRECHO else 0
SS = ['-ss', f'{(ini_q - .5) / SFPS:.6f}'] if ini_q else []
dec = subprocess.Popen(['ffmpeg', '-v', 'error', *P.HWDEC, *SS, '-i', BRUTO, '-an', '-vf', COLOR, '-f', 'rawvideo', '-'],
                       stdout=subprocess.PIPE, bufsize=VW * VH * 3 * 4)
enc_v = (['-c:v', 'ffv1'] if '--sem-perda' in arg else ['-c:v', 'libx264', '-preset', 'medium', '-crf', arg[arg.index('--crf') + 1]] if '--crf' in arg
         else P.V_PREVIA if previa else P.V_INTER if CAMADA else P.V_FINAL)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{OW}x{OH}', '-r', str(FPS), '-i', '-',
                        '-vf', 'scale=in_color_matrix=bt709:out_color_matrix=bt709:out_range=tv,format=yuv420p', *enc_v,
                        *([] if TRECHO else ['-movflags', '+faststart']), saida if TRECHO else tmpv], stdin=subprocess.PIPE)
lidos, src = ini_q, None
ant, congelado, seg_ant, fora_ant, fora_cong = None, None, None, False, False
for k in range(kp, k1):
    t = k / FPS; alvo, e = trecho_q(min(k, TQ - 1))
    while lidos <= alvo:
        b = dec.stdout.read(VW * VH * 3)
        if len(b) < VW * VH * 3: break
        src = np.frombuffer(b, np.uint8).reshape(VH, VW, 3); lidos += 1
    if e is not seg_ant: congelado, seg_ant, fora_cong = ant, e, fora_ant
    m = ativo(MOT, t); c = ativo(CAM_, t)
    out = compor(src, t, alvo / SFPS, e, quadro_seq(m, t) if m else None, peso_motion(m, t) if m else 0, quadro_seq(c, t) if c else None)
    if e.get('fusao') and congelado is not None and t - e['ini'] < FUS and not (m and peso_motion(m, t) > .99) and CAM_FORA == fora_cong:
        out = cv2.addWeighted(congelado, 1 - suave((t - e['ini']) / FUS), out, suave((t - e['ini']) / FUS), 0)
    ant, fora_ant = out, CAM_FORA
    if k < k0: continue
    enc.stdin.write(np.ascontiguousarray(out).tobytes())
    if k % 900 == 0: print(f'  {t:6.1f}s / {fim_total:.1f}s ({time.time() - T_INI:.0f}s)', flush=True)
enc.stdin.close(); enc.wait(); dec.kill()
for m in MOT + CAM_:
    if m['proc']: m['proc'].kill()
if TRECHO: print('pronto:', saida); sys.exit()
if CAMADA:
    base_ = saida[:-4]; os.replace(tmpv, base_ + '-tela.mp4'); os.replace(tmpa, base_ + '-voz.wav')
    print(f'pronto em {time.time() - T_INI:.0f}s:', base_ + '-tela.mp4', base_ + '-voz.wav'); sys.exit()
# junta: vídeo copiado, voz codificada em AAC uma única vez
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmpv, '-i', tmpa, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', *P.A_FINAL,
                '-movflags', '+faststart', saida], check=True)
os.remove(tmpv); os.remove(tmpa)
print(f'pronto em {time.time() - T_INI:.0f}s:', saida)
