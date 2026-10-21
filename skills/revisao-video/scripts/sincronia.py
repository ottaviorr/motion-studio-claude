"""Mede a sincronia voz × câmera de um vídeo editado (em ms), sem assistir.
uso:
  python sincronia.py final.mp4 --original bruto.mp4 --edl fonte/edl.json [--camera x,y,w,h] [--limite 40] [--json saida.json]
  python sincronia.py final.mp4 --camera x,y,w,h            → só "lábio × voz" (sem bruto: valor absoluto, menos preciso)
--camera: retângulo da câmera no BRUTO (px). Sem ele, lê "camera" do edicao.json ao lado do edl.json.

Duas medidas:
 1. POR EMENDA (com --original e --edl): para cada trecho do edl, em janelas de até 4 s:
    - áudio: correlação cruzada da voz do final com a voz do bruto → em que instante do bruto o som está (δA, precisão de 0,06 ms);
    - imagem: a região da câmera do final comparada quadro a quadro com a do bruto, deslocando de 1 em 1 ms → em que instante
      do bruto a imagem está (δV). Usa o tempo real de cada quadro (pts), então mede certo mesmo em gravação de taxa variável.
    atraso da imagem = δA − δV  (positivo = a boca vem DEPOIS da voz; negativo = a boca vem antes).
 2. LÁBIO × VOZ: energia do movimento na região da boca (achada sozinha: as células da câmera que mais acompanham a voz)
    × envelope da voz; o deslocamento que maximiza a correlação. Medido no final e no bruto; a diferença é o que a edição mudou
    (o valor absoluto tem viés natural de ~0–60 ms: a boca abre antes do som).
Sai: tabela por trecho, pior caso, veredito (APROVADO se |atraso| ≤ limite em todas as janelas confiáveis) e JSON opcional."""
import sys, os, json, re, subprocess
import numpy as np

SR = 16000; GW, GH = 64, 36   # áudio 16 kHz; câmera reduzida a 64×36 (só o movimento importa)


def probe(p):
    o = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,start_time:format=start_time',
                                   '-of', 'json', p], capture_output=True, text=True).stdout)
    fs = float(o['format'].get('start_time', 0) or 0)
    v = next((s for s in o['streams'] if s['codec_type'] == 'video'), None)
    au = next((s for s in o['streams'] if s['codec_type'] == 'audio'), None)
    return v, (float(au.get('start_time', 0) or 0) - fs) if au else None


def audio(p):
    """voz mono 16 kHz em float; t0 = instante (s) da 1ª amostra, já na linha do tempo que o player usa"""
    _, t0 = probe(p)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-map', '0:a:0', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy(), t0


def camera(p, rect):
    """região da câmera reduzida (64×36, cinza) de TODOS os quadros, com o tempo real (pts) de cada um"""
    x, y, w, h = [int(round(v)) for v in rect]
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-v', 'info', '-i', p, '-map', '0:v:0', '-fps_mode', 'passthrough',
                        '-vf', f'crop={w}:{h}:{x}:{y},scale={GW}:{GH}:flags=area,format=gray,showinfo', '-f', 'rawvideo', '-'],
                       capture_output=True)
    q = np.frombuffer(r.stdout, np.uint8).reshape(-1, GH, GW).astype(np.float32)
    ts = np.array([float(m) for m in re.findall(rb'pts_time:\s*(-?[\d.]+)', r.stderr)])
    n = min(len(q), len(ts)); return q[:n], ts[:n]


def janela_audio(fa, fa0, ba, ba0, t0, t1, s0, L=.3):   # ±0,3 s: mais que isso acha a MESMA frase repetida no bruto (o corte de repetição)
    """δA: deslocamento (s) entre o som do final em [t0, t1] e o bruto a partir de s0 (esperado), busca ±L"""
    i0, i1 = int((t0 - fa0) * SR), int((t1 - fa0) * SR)
    j0 = int((s0 - L - ba0) * SR)
    if i0 < 0 or i1 > len(fa) or j0 < 0: return None, 0
    f = fa[i0:i1]; b = ba[j0:j0 + (i1 - i0) + int(2 * L * SR)]
    if len(b) < (i1 - i0) + int(2 * L * SR) or f.std() < 1e-4: return None, 0
    n = 1 << int(np.ceil(np.log2(len(b) + len(f))))
    cc = np.fft.irfft(np.fft.rfft(b, n) * np.conj(np.fft.rfft(f, n)), n)[:len(b) - len(f) + 1]
    e = np.sqrt(np.convolve(b * b, np.ones(len(f)), 'valid') * (f * f).sum()) + 1e-9
    cc = cc / e; k = int(np.argmax(cc))
    if 0 < k < len(cc) - 1:   # refino parabólico (sub-amostra)
        y0, y1, y2 = cc[k - 1], cc[k], cc[k + 1]; k = k + .5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
    return k / SR - L, float(cc.max())


def janela_video(F, tf, B, tb, t0, t1, s_de, L=1.0, passo=.001):
    """δV: em que instante do bruto está a imagem do final em [t0, t1]. s_de(t) = instante esperado no bruto.
    Compara a DIFERENÇA entre quadros seguidos (o movimento, que é único em cada instante; o quadro parado quase não muda
    e deixaria o pico largo) e varre δ de 1 em 1 ms. O máximo é um platô (vários δ dão os mesmos quadros) → pega o centro."""
    k = np.where((tf >= t0) & (tf < t1))[0]; k = k[k > 0]
    k = k[tf[k - 1] >= t0]                  # par de quadros dentro da janela (sem atravessar a emenda)
    if len(k) < 8: return None, 0
    f = F[k] - F[k - 1]; fn = np.sqrt((f * f).sum())
    if fn < .3 * np.sqrt(f.size): return None, 0   # câmera parada demais (ou sem câmera): não dá para medir
    s1, s0 = s_de(tf[k]), s_de(tf[k - 1]); ds = np.arange(-L, L + passo / 2, passo); cor = np.empty(len(ds))
    ix = lambda s: np.clip(np.searchsorted(tb, s + 1e-6, 'right') - 1, 0, len(tb) - 1)
    cache = {}
    for i, d in enumerate(ds):
        i1, i0 = ix(s1 + d), ix(s0 + d); key = i1.tobytes() + i0.tobytes()
        if key not in cache:
            g = B[i1] - B[i0]; cache[key] = float((f * g).sum() / (fn * np.sqrt((g * g).sum()) + 1e-9))
        cor[i] = cache[key]
    m = cor.max(); j0 = int(np.argmax(cor)); j1 = j0
    while j1 + 1 < len(cor) and cor[j1 + 1] >= m - 1e-9: j1 += 1
    longe = (ds < ds[j0] - .012) | (ds > ds[j1] + .012)       # o segundo melhor fora do platô (ambiguidade)
    seg = cor[longe].max() if longe.any() else 0
    # δ = INÍCIO do platô: o quadro do final é cópia de um quadro do bruto, e o platô vai do instante em que aquele quadro
    # entra até o próximo entrar (com a webcam a 30 fps dentro de 60, o centro dava -8 ms falsos em tudo)
    return float(ds[j0]), float(m - max(0, seg) * .5)


def labio(V, tv, au, a0, celulas=None):
    """lábio × voz: retorna (atraso da imagem em s, pico da correlação, células usadas).
    Movimento por célula (grade 16×12 da câmera) × envelope da voz, a 100 Hz, busca ±0,3 s. Quadros repetidos
    (webcam a 30 fps dentro de gravação a 60) saem antes, senão metade das diferenças é zero."""
    d = np.abs(np.diff(V, axis=0)).mean((1, 2)); manter = np.r_[True, d > .05]; V, tv = V[manter], tv[manter]
    gy, gx = 12, 16; H, W = V.shape[1:]
    if len(V) < 100: return None, 0, celulas
    blocos = V[:, :H // gy * gy, :W // gx * gx].reshape(len(V), gy, H // gy, gx, W // gx).mean((2, 4))
    mov = np.abs(np.diff(blocos, axis=0)).reshape(len(V) - 1, -1); tm = (tv[1:] + tv[:-1]) / 2
    grade = np.arange(max(tm[0], a0) + .5, min(tm[-1], a0 + len(au) / SR) - .5, .01)
    if len(grade) < 1000: return None, 0, celulas
    hop = SR // 100; n = len(au) // hop
    env = np.sqrt((au[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-10); te = a0 + (np.arange(n) + .5) / 100
    norm = lambda x: (x - x.mean(0)) / (x.std(0) + 1e-9)
    voz = norm(np.interp(grade, te, env))
    M = norm(np.stack([np.interp(grade, tm, mov[:, c]) for c in range(mov.shape[1])], 1))
    lags = np.arange(-30, 31)   # ±0,3 s em passos de 10 ms
    def xc(sig):
        return np.array([np.mean(sig[max(0, l):len(sig) + min(0, l)] * voz[max(0, -l):len(voz) - max(0, l)]) for l in lags])
    if celulas is None:
        pico = np.array([xc(M[:, c]).max() for c in range(M.shape[1])])
        celulas = list(np.argsort(pico)[-8:])   # as 8 células que mais acompanham a voz = boca/queixo
    cc = xc(M[:, celulas].mean(1)); k = int(np.argmax(cc)); kk = float(k)
    if 0 < k < len(cc) - 1:
        y0, y1, y2 = cc[k - 1], cc[k], cc[k + 1]; kk = k + .5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
    # lag > 0 = o movimento (imagem) vem depois da voz
    return (kk - 30) / 100, float(cc.max()), celulas


def medir(FINAL, ORIG=None, EDL=None, rect=None, LIM=40.0, saida_json=None):
    """mede e devolve (resultado, linhas do relatório). Usado pela linha de comando e pelo revisar.py."""
    FINAL = os.path.abspath(FINAL)
    vf, _ = probe(FINAL)
    if rect is None and EDL:
        ed = os.path.join(os.path.dirname(os.path.abspath(EDL)), 'edicao.json')
        if os.path.exists(ed): rect = json.load(open(ed)).get('camera')
    if not rect: return {'aprovado': None}, ['## Sincronia: sem --camera (x,y,w,h no bruto) e sem edicao.json com "camera" — não medida']
    E = 1.0
    if ORIG:
        vo, _ = probe(ORIG); E = vf['width'] / vo['width']
    # miolo da câmera (15% para dentro): longe da borda arredondada, da sombra e da moldura
    x, y, w, h = rect; ix, iy = w * .15, h * .15
    dentro = [x + ix, y + iy, w - 2 * ix, h - 2 * iy]
    fa, fa0 = audio(FINAL); F, tf = camera(FINAL, [v * E for v in dentro])
    res = {'final': FINAL, 'limite_ms': LIM, 'janelas': [], 'trechos': []}
    linhas = [f'## Sincronia voz × câmera (limite ±{LIM:g} ms)']
    if ORIG and EDL:
        ba, ba0 = audio(ORIG); B, tb = camera(ORIG, dentro)
        edl = json.load(open(EDL)); fps = edl.get('fps')
        linhas.append(f"{'trecho':>6} {'final(s)':>9} {'bruto(s)':>9} {'δsom':>8} {'δimagem':>8} {'ATRASO':>8}  (ms; ATRASO + = boca depois da voz)")
        for n, e in enumerate(edl['trechos'], 1):
            d = e['nq'] / fps if fps and 'nq' in e else (e['out'] - e['in']) / e['vel']
            if e.get('tipo', 'fala') != 'fala' or e['vel'] != 1 or d < .5: continue
            a0_, a1_ = e['ini'] + .06, e['ini'] + d - .06
            nj = max(1, int(np.ceil((a1_ - a0_) / 4))); cortes = np.linspace(a0_, a1_, nj + 1)
            s_de = lambda t, e=e: e['in'] + (t - e['ini'])
            pior = None
            for t0, t1 in zip(cortes[:-1], cortes[1:]):
                dA, cA = janela_audio(fa, fa0, ba, ba0, t0, t1, s_de(t0))
                dV, cV = janela_video(F, tf, B, tb, t0, t1, s_de)
                ok = dA is not None and dV is not None and cA > .5 and cV > .2
                j = {'trecho': n, 't0': round(t0, 3), 't1': round(t1, 3), 'som_ms': None if dA is None else round(dA * 1000, 1),
                     'imagem_ms': None if dV is None else round(dV * 1000, 1), 'conf_som': round(cA, 3), 'conf_imagem': round(cV, 3),
                     'atraso_ms': round((dA - dV) * 1000, 1) if ok else None}
                res['janelas'].append(j)
                if j['atraso_ms'] is not None and (pior is None or abs(j['atraso_ms']) > abs(pior['atraso_ms'])): pior = j
            if pior:
                res['trechos'].append({'trecho': n, 'ini': e['ini'], 'in': e['in'], **{k: pior[k] for k in ('som_ms', 'imagem_ms', 'atraso_ms')}})
                linhas.append(f"{n:>6} {e['ini']:9.2f} {e['in']:9.2f} {pior['som_ms']:8.1f} {pior['imagem_ms']:8.1f} {pior['atraso_ms']:8.1f}"
                              + ('   ← FORA' if abs(pior['atraso_ms']) > LIM else ''))
            else:
                linhas.append(f"{n:>6} {e['ini']:9.2f} {e['in']:9.2f}   (câmera coberta, parada demais ou trecho curto: não medido)")
        at = [t['atraso_ms'] for t in res['trechos']]
        falas = sum(1 for e in edl['trechos'] if e.get('tipo', 'fala') == 'fala')
        if len(at) >= max(1, falas // 2):
            res['pior_ms'] = max(at, key=abs); res['media_ms'] = round(float(np.mean(at)), 1); res['medidos'] = len(at)
            res['aprovado'] = bool(abs(res['pior_ms']) <= LIM)
            linhas += [f"pior caso {res['pior_ms']:+.1f} ms · média {res['media_ms']:+.1f} ms · {len(at)} de {falas} trechos de fala medidos",
                       f"SINCRONIA: {'APROVADO' if res['aprovado'] else 'REPROVADO'}"]
        else:
            res['aprovado'] = None
            linhas.append(f'SINCRONIA: INCONCLUSIVO — só {len(at)} de {falas} trechos medidos (a câmera está no lugar do edicao.json?)')
        lb, cb, cel = labio(B, tb, ba, ba0)
        lf, cf, _ = labio(F, tf, fa, fa0, cel)
        if lb is not None and lf is not None and min(cb, cf) >= .12:
            res['labio'] = {'bruto_ms': round(lb * 1000), 'final_ms': round(lf * 1000), 'diferenca_ms': round((lf - lb) * 1000), 'pico': round(cf, 3)}
            linhas.append(f"lábio × voz (conferência grosseira, ±30 ms): bruto {lb * 1000:+.0f} ms · final {lf * 1000:+.0f} ms → "
                          f"a edição mudou {1000 * (lf - lb):+.0f} ms")
        else:
            linhas.append('lábio × voz: inconclusivo (pouco movimento de boca visível); vale a medida por emenda acima')
    else:
        lf, cf, _ = labio(F, tf, fa, fa0)
        if lf is not None and cf >= .12:
            res['labio'] = {'final_ms': round(lf * 1000), 'pico': round(cf, 3)}
            linhas.append(f"lábio × voz: boca {lf * 1000:+.0f} ms em relação à voz (correlação {cf:.2f}). Sem o bruto é só indício: "
                          'normal fica entre -60 e +40 ms. Para medir de verdade: --original bruto --edl edl.json')
        else:
            linhas.append('lábio × voz: inconclusivo (pouco movimento de boca visível). Para medir: --original bruto --edl edl.json')
    if saida_json: json.dump(res, open(saida_json, 'w'), ensure_ascii=False, indent=1)
    return res, linhas


if __name__ == '__main__':
    a = sys.argv[1:]
    op = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    r, L = medir(a[0], op('--original'), op('--edl'), [float(x) for x in op('--camera').split(',')] if op('--camera') else None,
                 float(op('--limite', 40)), op('--json'))
    print('\n'.join(L))
    sys.exit(1 if r.get('aprovado') is False else 0)
