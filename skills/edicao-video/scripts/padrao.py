"""Padrão de entrega do vídeo editado (regra principal do dono, 15/10/2026) e peças comuns dos scripts.
  1920×1080 · 30 fps constante · H.264 High · 18 Mb/s constante (CBR, nunca abaixo de 16) · AAC 320 k 48 kHz · -14 LUFS · BT.709
Sincronia por construção: bruto normalizado (normalizar.py) → cortes no quadro de 30 fps (plano.py) → áudio em PCM até o fim
(uma única codificação AAC, no final). Importe daqui; não copie os números para outro lugar."""
import os, sys, json, shutil, subprocess, time, atexit

FPS = 30
W, H = 1920, 1080
SR = 48000
VBR = '18M'            # alvo; a revisão reprova fora de 16–20 Mb/s
ABR = '320k'
LUFS, TP, LRA = -14, -1.5, 11
COR = ['-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']
# taxa constante: o x264 em ABR gasta pouco em tela parada (já saiu 7,7 Mb/s pedindo 20); com nal-hrd=cbr ele mantém o alvo
V_FINAL = ['-c:v', 'libx264', '-preset', 'medium', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-g', str(2 * FPS),
           '-b:v', VBR, '-minrate', VBR, '-maxrate', VBR, '-bufsize', '36M', '-x264-params', 'nal-hrd=cbr:aq-mode=3', *COR]
# hardware de vídeo da máquina: Mac = VideoToolbox; Windows/Linux com NVIDIA = CUDA (decodifica) + NVENC (codifica); sem nada, CPU
MAC = sys.platform == 'darwin'
_ff = lambda *a: subprocess.run(['ffmpeg', '-hide_banner', *a], capture_output=True, text=True).stdout
NVIDIA = not MAC and shutil.which('nvidia-smi') is not None   # o ffmpeg lista nvenc/cuda mesmo sem a placa: confere a placa
NVENC = NVIDIA and 'h264_nvenc' in _ff('-encoders')
HWDEC = ['-hwaccel', 'videotoolbox'] if MAC else ['-hwaccel', 'cuda'] if NVIDIA and 'cuda' in _ff('-hwaccels') else []
# prévia para assistir: codificador de hardware (segundos, não minutos)
V_PREVIA = (['-c:v', 'h264_videotoolbox', '-b:v', '8M'] if MAC else ['-c:v', 'h264_nvenc', '-preset', 'p4', '-b:v', '8M'] if NVENC
            else ['-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23']) + ['-profile:v', 'high', '-pix_fmt', 'yuv420p', *COR]
# intermediário que ainda vai ser lido (camada de tela, câmera do Remotion, bruto normalizado): quase sem perda, rápido
V_INTER = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '10', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-g', str(FPS), *COR]
# AAC do sistema (AudioToolbox) em taxa constante: o aac nativo do ffmpeg pedindo 320 k entregava ~248 k em voz
_AAC_AT = 'aac_at' in subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], capture_output=True, text=True).stdout
A_FINAL = (['-c:a', 'aac_at', '-aac_at_mode', 'cbr', '-aac_at_quality', '0', '-b:a', ABR, '-ar', str(SR)] if _AAC_AT
           else ['-c:a', 'aac', '-b:a', ABR, '-ar', str(SR)])


def probe(p):
    """dict com largura, altura, fps nominal e médio, nº de quadros, duração, codec, perfil, faixa de cor e o áudio"""
    o = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                                   'format=duration,bit_rate,start_time:stream=index,codec_type,codec_name,profile,width,height,r_frame_rate,'
                                   'avg_frame_rate,nb_frames,pix_fmt,color_range,color_transfer,color_space,sample_rate,bit_rate,start_time,channels',
                                   '-of', 'json', p], capture_output=True, text=True).stdout)
    fr = lambda s: (lambda a, b: float(a) / float(b) if float(b) else 0)(*s.split('/'))
    v = next((s for s in o['streams'] if s['codec_type'] == 'video'), {}); au = next((s for s in o['streams'] if s['codec_type'] == 'audio'), {})
    return {'w': int(v.get('width', 0)), 'h': int(v.get('height', 0)), 'fps': fr(v.get('r_frame_rate', '0/1')), 'fps_medio': fr(v.get('avg_frame_rate', '0/1')),
            'quadros': int(v.get('nb_frames', 0) or 0), 'dur': float(o['format'].get('duration', 0)), 'vcodec': v.get('codec_name'), 'perfil': v.get('profile'),
            'pix': v.get('pix_fmt'), 'faixa': v.get('color_range'), 'trc': v.get('color_transfer'), 'v_bps': int(v.get('bit_rate', 0) or 0),
            'v_ini': float(v.get('start_time', 0) or 0), 'acodec': au.get('codec_name'), 'sr': int(au.get('sample_rate', 0) or 0),
            'a_bps': int(au.get('bit_rate', 0) or 0), 'a_ini': float(au.get('start_time', 0) or 0), 'total_bps': int(o['format'].get('bit_rate', 0) or 0)}


def tempos_quadros(p):
    """tempo real (pts) de cada quadro de vídeo, sem decodificar (lê só os pacotes)"""
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'packet=pts_time', '-of', 'csv=p=0', p],
                       capture_output=True, text=True).stdout
    import numpy as np
    return np.sort(np.array([float(x) for x in o.split() if x.replace('.', '', 1).replace('-', '', 1).isdigit()]))


def taxa_constante(p, fps=None):
    """(ok, texto): o vídeo tem quadros em ritmo constante, começando em 0 e com áudio alinhado?"""
    import numpy as np
    i = probe(p); t = tempos_quadros(p)
    if len(t) < 2: return False, 'sem quadros'
    f = fps or round(1 / np.median(np.diff(t)))
    desvio = np.abs(t - t[0] - np.arange(len(t)) / f).max()
    ok = desvio < .25 / f and abs(i['v_ini'] - i['a_ini']) < 1e-3 and (fps is None or abs(i['fps'] - fps) < 1e-3)
    return ok, (f"{len(t)} quadros, {f:g} fps nominal, maior desvio do ritmo {desvio * 1000:.1f} ms, "
                f"vídeo começa em {i['v_ini']:.3f}s e áudio em {i['a_ini']:.3f}s")


def fila():
    """uma gravação/montagem por vez no computador inteiro (mesma trava do motion-design/kit/hf.mjs e gerar_reel.py)"""
    if os.environ.get('MOTION_FILA') == '1': return   # quem chamou já está com a vez (ex.: renderizar.sh do Remotion)
    f = os.path.join(os.path.expanduser('~'), '.cache', 'motion-studio-fila-render'); os.makedirs(os.path.dirname(f), exist_ok=True)
    avisou = False
    while True:
        try: os.mkdir(f); break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(f) > 45 * 60: os.rmdir(f); continue   # trava esquecida
            except OSError: pass
            if not avisou: print('aguardando a vez na fila de render…', flush=True); avisou = True
            time.sleep(2)
    atexit.register(lambda: os.path.isdir(f) and os.rmdir(f))
    os.environ['MOTION_FILA'] = '1'   # processos filhos (render.py --partes) não esperam a si mesmos


def loudnorm(entrada, filtro_antes='', mapa='0:a:0', extra_in=()):
    """filtro de 2ª passada do loudnorm (-14 LUFS), medido de verdade na 1ª passada. filtro_antes termina em [m] se usar filter_complex."""
    alvo = f'loudnorm=I={LUFS}:TP={TP}:LRA={LRA}'
    if filtro_antes:
        cmd = ['ffmpeg', '-v', 'info', *extra_in, '-i', entrada, '-filter_complex', filtro_antes + f';[m]{alvo}:print_format=json[o]', '-map', '[o]', '-f', 'null', '-']
    else:
        cmd = ['ffmpeg', '-v', 'info', *extra_in, '-i', entrada, '-map', mapa, '-af', alvo + ':print_format=json', '-f', 'null', '-']
    e = subprocess.run(cmd, capture_output=True, text=True).stderr
    L = json.loads(e[e.rindex('{'):e.rindex('}') + 1])
    return (f"{alvo}:measured_I={L['input_i']}:measured_TP={L['input_tp']}:measured_LRA={L['input_lra']}"
            f":measured_thresh={L['input_thresh']}:offset={L['target_offset']}:linear=true")
