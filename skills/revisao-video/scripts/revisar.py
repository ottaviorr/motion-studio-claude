"""Revisão de um vídeo pronto, sem precisar assistir: ouve de novo, mede e fotografa.
uso: python revisar.py video.mp4 [--saida pasta] [--esperado palavras.json|roteiro.txt] [--edl edl.json]
                                  [--original bruto] [--camera x,y,w,h] [--padrao edicao|nenhum] [--modelo large-v3-turbo] [--fotos 12]
Gera na pasta de saída (padrão: <video>-revisao/):
  revisao.txt         0. RESULTADO: APROVADO ou REPROVADO, com o motivo de cada reprovação
                      1. técnico × padrão de entrega (1920×1080, 30 fps constante, H.264 High, 16–20 Mb/s, AAC 320 k 48 kHz,
                         -14 LUFS, pico ≤ -1 dBFS, BT.709). --padrao edicao é o padrão quando há --edl; "nenhum" só mede.
                      1b. sincronia voz × câmera por emenda (com --edl e --original): reprova acima de 40 ms (scripts/sincronia.py)
                      2. fala: diferenças entre o que devia ser dito (--esperado) e o que se ouve no final
                      3. repetições coladas ("eu vim cá eu vim cá"): gaguejada que sobrou
                      4. a fala do vídeo final em frases (para ler como espectador: começo, meio e fim)
  ouvido.json         transcrição do final com tempo por palavra (com cache: o mesmo áudio não é transcrito duas vezes)
  sincronia.json      atraso por trecho e por janela (com --edl e --original)
  folha-fotos.jpg     N quadros espalhados pelo vídeo
  folha-emendas.jpg   0,1 s antes/depois de cada emenda (só com --edl)
As etapas pesadas (transcrição, sincronia, fotos) rodam em paralelo."""
import sys, os, json, subprocess, re, difflib, unicodedata
from concurrent.futures import ThreadPoolExecutor
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ouvir import transcrever, carregar, PADRAO as MODELO_PADRAO
import sincronia

a = sys.argv[1:]; VID = os.path.abspath(a[0])
op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
_d = os.path.dirname(VID); _n = re.sub(r'\.\w+$', '', os.path.basename(VID))
# vídeo em prontos/ (pasta de entrega) → revisão em <projeto>/revisao/<nome>, para a pasta de entrega ficar só com vídeos
OUT = op('--saida', os.path.join(os.path.dirname(_d), 'revisao', _n) if os.path.basename(_d) == 'prontos' else re.sub(r'\.\w+$', '', VID) + '-revisao'); os.makedirs(OUT, exist_ok=True)
J = lambda p: os.path.join(OUT, p)
norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())
PADRAO = op('--padrao', 'edicao' if '--edl' in a else 'nenhum')
# padrão de entrega do vídeo editado (regra principal do dono, 15/10/2026) — os mesmos números de edicao-video/scripts/padrao.py
ALVO = {'w': 1920, 'h': 1080, 'fps': 30, 'mbps': (16, 20.5), 'abr': 300, 'sr': 48000, 'lufs': (-15, -13), 'tp': -1.0}
rel, reprova = [], []


def probe(p):
    o = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,bit_rate:stream=codec_type,codec_name,profile,width,height,'
                                   'r_frame_rate,avg_frame_rate,pix_fmt,color_space,color_primaries,color_transfer,bit_rate,sample_rate',
                                   '-of', 'json', p], capture_output=True, text=True).stdout)
    v = [s for s in o['streams'] if s['codec_type'] == 'video'][0]
    au = next((s for s in o['streams'] if s['codec_type'] == 'audio'), {})
    return v, au, float(o['format']['duration']), int(o['format']['bit_rate']) / 1e6


fr = lambda s: (lambda x, y: float(x) / float(y) if float(y) else 0)(*s.split('/'))


def tecnico():
    v, au, d, br = probe(VID)
    ld = subprocess.run(['ffmpeg', '-v', 'info', '-i', VID, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = re.findall(r'I:\s+(-?[\d.]+) LUFS', ld); TP = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', ld)
    vbr = int(v.get('bit_rate', 0) or 0) / 1e6 or br
    abr = int(au.get('bit_rate', 0) or 0) / 1e3
    L = ['## 1. Técnico' + (' × padrão de entrega (1920×1080 · 30 fps · H.264 High · 16–20 Mb/s · AAC 320 k 48 kHz · -14 LUFS · BT.709)' if PADRAO == 'edicao' else ''),
         f"{v['width']}×{v['height']} · {v['r_frame_rate']} fps (média {fr(v['avg_frame_rate']):.3f}) · {v['codec_name']} {v.get('profile', '')} {v['pix_fmt']} "
         f"{v.get('color_space', '?')} · {d:.1f}s · vídeo {vbr:.1f} Mb/s · áudio {au.get('codec_name', '—')} {abr:.0f} k {au.get('sample_rate', '—')} Hz"]
    if '--original' in a:
        vo, _, do, bo = probe(op('--original'))
        L.append(f"original: {vo['width']}×{vo['height']} · {vo['r_frame_rate']} fps · {do:.1f}s · {bo:.1f} Mb/s")
    L.append(f"Volume {I[-1] if I else '?'} LUFS · pico {TP[-1] if TP else '?'} dBFS")
    r = []
    if PADRAO == 'edicao':
        chk = [((v['width'], v['height']) == (ALVO['w'], ALVO['h']), f"resolução {v['width']}×{v['height']} (padrão 1920×1080)"),
               (abs(fr(v['r_frame_rate']) - ALVO['fps']) < .01 and abs(fr(v['avg_frame_rate']) - ALVO['fps']) < .05, f"fps {v['r_frame_rate']} / média {fr(v['avg_frame_rate']):.2f} (padrão 30 constante)"),
               (v['codec_name'] == 'h264' and v.get('profile') == 'High', f"codec {v['codec_name']} {v.get('profile')} (padrão H.264 High)"),
               (ALVO['mbps'][0] <= vbr <= ALVO['mbps'][1], f"taxa de vídeo {vbr:.1f} Mb/s (padrão 16–20)"),
               (au.get('codec_name') == 'aac' and abr >= ALVO['abr'] and int(au.get('sample_rate', 0) or 0) == ALVO['sr'], f"áudio {au.get('codec_name')} {abr:.0f} k {au.get('sample_rate')} Hz (padrão AAC 320 k 48 kHz)"),
               (bool(I) and ALVO['lufs'][0] <= float(I[-1]) <= ALVO['lufs'][1], f"volume {I[-1] if I else '?'} LUFS (padrão -14 ±1)"),
               (bool(TP) and float(TP[-1]) <= ALVO['tp'], f"pico {TP[-1] if TP else '?'} dBFS (padrão ≤ -1)"),
               (v.get('color_space') == 'bt709' or v.get('color_primaries') == 'bt709', f"cor {v.get('color_space')} (padrão BT.709 marcado)")]
        for ok, txt in chk:
            L.append(f"  {'ok  ' if ok else 'FORA'}  {txt}")
            if not ok: r.append(txt)
    return L + [''], r, d


def fala():
    au = carregar(VID)
    segs = transcrever(au, op("--modelo", MODELO_PADRAO))
    ouv = [{'w': x['w'], 't': round(x['t'], 2)} for s in segs for x in s['words']]
    json.dump(ouv, open(J('ouvido.json'), 'w'), ensure_ascii=False, indent=0)
    b = [norm(x['w']) for x in ouv]; L = []
    if '--esperado' in a:
        p = op('--esperado')
        esp = json.load(open(p)) if p.endswith('.json') else [{'w': w, 't': 0} for w in open(p).read().split()]
        ea = [norm(x['w']) for x in esp]
        L.append('## 2. Fala: esperado × ouvido no final (a maioria é o Whisper ouvindo diferente; olhe as que caem perto de emenda)')
        n = 0
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ea, b, autojunk=False).get_opcodes():
            if tag == 'equal': continue
            e = ' '.join(x['w'] for x in esp[i1:i2]); o = ' '.join(x['w'] for x in ouv[j1:j2])
            if norm(e) == norm(o): continue
            t = ouv[j1]['t'] if j1 < len(ouv) else ouv[-1]['t']
            L.append(f'  {t:7.2f}s  esperado: "{e}"  →  ouvido: "{o}"'); n += 1
        L += [f'  ({n} diferenças)', '']
    L.append('## 3. Repetições coladas (gaguejada que sobrou?)')
    for k in range(1, 4):
        for i in range(len(b) - 2 * k + 1):
            if b[i:i + k] == b[i + k:i + 2 * k] and all(len(x) > 1 for x in b[i:i + k]):
                L.append(f'  {ouv[i]["t"]:7.2f}s  "{" ".join(x["w"] for x in ouv[i:i + 2 * k])}"')
    L += ['', '## 4. A fala do vídeo final (leia como espectador: dá para entender? começa, desenvolve e fecha?)']
    return L + [f"  {s['start']:6.1f}  {s['text'].strip()}" for s in segs] + ['']


def sinc():
    if '--edl' not in a and '--camera' not in a: return [], []
    cam = [float(x) for x in op('--camera').split(',')] if '--camera' in a else None
    r, L = sincronia.medir(VID, op('--original'), op('--edl'), cam, 40.0, J('sincronia.json'))
    return L + [''], (['sincronia voz × câmera: pior emenda {:+.0f} ms (limite ±40 ms)'.format(r['pior_ms'])] if r.get('aprovado') is False else [])


# fotos
def foto(t, w=480):
    b_ = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0, t):.3f}', '-i', VID, '-frames:v', '1', '-vf', f'scale={w}:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                        capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(b_, np.uint8), cv2.IMREAD_COLOR) if b_ else None
def rotulo(im, txt):
    if im is None: return None
    cv2.rectangle(im, (0, 0), (8 + 11 * len(txt), 28), (0, 0, 0), -1)
    cv2.putText(im, txt, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .55, (255, 255, 255), 1, cv2.LINE_AA); return im
def folha(ims, arq, por_linha):
    ims = [i for i in ims if i is not None]
    if not ims: return
    h, w = ims[0].shape[:2]; ims = [cv2.resize(i, (w, h)) for i in ims]
    ims += [np.zeros_like(ims[0])] * (-len(ims) % por_linha)
    cv2.imwrite(arq, np.vstack([np.hstack(ims[i:i + por_linha]) for i in range(0, len(ims), por_linha)]), [cv2.IMWRITE_JPEG_QUALITY, 82])
def fotos(d):
    N = int(op('--fotos', 12))
    with ThreadPoolExecutor(6) as ex:
        ts = list(np.linspace(.05, d - .1, N)); folha([rotulo(i, f'{t:.1f}s') for t, i in zip(ts, ex.map(foto, ts))], J('folha-fotos.jpg'), 4)
        if '--edl' not in a: return []
        emendas = [e['ini'] for e in json.load(open(op('--edl')))['trechos'][1:]]
        ts = [x for t in emendas for x in (t - .1, t + .1)]
        ims = [rotulo(i, f"{ts[k] + (.1 if k % 2 == 0 else -.1):.1f} {'antes' if k % 2 == 0 else 'depois'}") for k, i in enumerate(ex.map(foto, ts))]
    folha(ims, J('folha-emendas.jpg'), 8)
    return [f'## 5. Emendas: {len(emendas)} → folha-emendas.jpg (pulo feio de rosto/tela, quadro preto, câmera fora do lugar)']


L1, r1, dur = tecnico()
with ThreadPoolExecutor(3) as ex:   # transcrição, sincronia e fotos ao mesmo tempo (cada uma usa um recurso diferente)
    fF = ex.submit(fala); fS = ex.submit(sinc); fP = ex.submit(fotos, dur)
    L2 = fF.result(); L1b, r1b = fS.result(); L5 = fP.result()
reprova = r1 + r1b
res = ['## 0. RESULTADO: ' + ('REPROVADO' if reprova else 'APROVADO (técnico e sincronia; fala e fotos: leia abaixo)')] + [f'  - {x}' for x in reprova] + ['']
rel = res + L1 + L1b + L2 + L5
open(J('revisao.txt'), 'w').write('\n'.join(rel) + '\n')
print('\n'.join(rel)); print('→', OUT)
sys.exit(1 if reprova else 0)
