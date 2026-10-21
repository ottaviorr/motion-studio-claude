"""Transcrição local (faster-whisper) com CACHE: o mesmo áudio + mesmo modelo nunca é transcrito duas vezes.
uso como módulo:  from ouvir import transcrever;  segs = transcrever(audio_16k_float32)
uso direto:       python ouvir.py bruto.mov [--modelo medium]                     → imprime as frases
                  python ouvir.py bruto.mov --palavras fonte/palavras.json [--modelo medium]  → passo 2 da edição
                  (mesmo formato do transcrever.py da motion-design: [{"w","t","e"}] + .txt "t:palavra")
Cada segmento: {'start', 'end', 'text', 'words': [{'w', 't', 'e'}]}. Nada sai do computador.
Cache em ~/.cache/motion-studio-whisper/<hash do áudio + modelo>.json (ouvir_emendas e a revisão rodam de novo sem custo
quando só a imagem mudou).
Modelo padrão: large-v3-turbo em lotes (BatchedInferencePipeline, lote 8). Medido no M4 com 173 s de fala:
  medium 109 s · turbo 89 s · turbo em lotes 57 s (acerta mais termos: "Conversation", "etapa", "lead"; mantém hesitações
  como "pré... foi"). Mais threads PIORA (10 threads: medium 149 s — os núcleos de eficiência atrasam): fica o padrão (4).
--modelo medium continua disponível (era o padrão antigo)."""
import os, sys, json, hashlib, subprocess
import numpy as np

CACHE = os.path.join(os.path.expanduser('~'), '.cache', 'motion-studio-whisper')
_modelos = {}


def carregar(arq, sr=16000):
    # async + first_pts=0: buraco no áudio vira silêncio no lugar certo (mesma linha do tempo do normalizar.py)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', arq, '-map', '0:a:0', '-af', f'aresample={sr}:async=1:first_pts=0', '-f', 's16le', '-ac', '1', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


PADRAO = 'large-v3-turbo'


def transcrever(audio, modelo=PADRAO, palavras=True, idioma='pt', lote=8):
    audio = np.ascontiguousarray(audio, np.float32)
    h = hashlib.sha1(audio.tobytes() + f'|{modelo}|{palavras}|{idioma}|{lote}|v1'.encode()).hexdigest()[:20]
    arq = os.path.join(CACHE, h + '.json')
    if os.path.exists(arq): return json.load(open(arq))
    from faster_whisper import WhisperModel, BatchedInferencePipeline
    if os.name == 'nt':   # Windows: DLLs do CUDA instaladas pelo pip (nvidia-cublas-cu12, nvidia-cudnn-cu12) — ver instalar.sh
        import glob
        for d in glob.glob(os.path.join(sys.prefix, 'Lib', 'site-packages', 'nvidia', '*', 'bin')):
            os.add_dll_directory(d); os.environ['PATH'] = d + os.pathsep + os.environ['PATH']
    # GPU NVIDIA primeiro (2 min de áudio em ~20 s numa RTX 3050); no Mac, ou se o CUDA falhar, CPU int8
    for disp, tipo in ((('cpu', 'int8'),) if sys.platform == 'darwin' else (('cuda', 'float16'), ('cpu', 'int8'))):
        try:
            if (modelo, disp) not in _modelos: _modelos[(modelo, disp)] = WhisperModel(modelo, device=disp, compute_type=tipo)
            m = _modelos[(modelo, disp)]
            if lote: segs, _ = BatchedInferencePipeline(m).transcribe(audio, language=idioma, vad_filter=True, word_timestamps=palavras, batch_size=lote)
            else: segs, _ = m.transcribe(audio, language=idioma, vad_filter=True, word_timestamps=palavras)
            out = [{'start': round(s.start, 3), 'end': round(s.end, 3), 'text': s.text,
                    'words': [{'w': w.word.strip(), 't': round(w.start, 3), 'e': round(w.end, 3)} for w in (s.words or []) if w.word.strip()]}
                   for s in segs]   # a GPU só falha de verdade aqui (DLL carregada sob demanda)
            break
        except Exception as e:
            if disp == 'cpu': raise
            print(f'(GPU indisponível: {str(e)[:80]} — usando CPU)', file=sys.stderr)
    os.makedirs(CACHE, exist_ok=True); json.dump(out, open(arq, 'w'), ensure_ascii=False)
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    m = a[a.index('--modelo') + 1] if '--modelo' in a else PADRAO
    segs = transcrever(carregar(a[0]), m)
    if '--palavras' in a:
        p = a[a.index('--palavras') + 1]; W = [w for s in segs for w in s['words']]
        json.dump(W, open(p, 'w'), ensure_ascii=False, indent=0)
        open(os.path.splitext(p)[0] + '.txt', 'w').write(' '.join(f"{w['t']:.2f}:{w['w']}" for w in W) + '\n')
        print(len(W), 'palavras →', p)
    else:
        for s in segs: print(f"{s['start']:7.1f}  {s['text'].strip()}")
