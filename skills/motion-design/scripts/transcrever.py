"""Tempo de cada palavra, local (faster-whisper; nada sai do computador).
usage: python3 transcrever.py audio_ou_video saida.json [--roteiro roteiro.txt] [--modelo small]
Com --roteiro, as PALAVRAS vêm do roteiro (grafia certa, marcas, [[exibido|falado]]) e os TEMPOS vêm do áudio.
Saída: [{"w":"domínio","t":6.52,"e":6.98}, ...] e um .txt "t:palavra" ao lado."""
import sys, re, json, subprocess, difflib, unicodedata
import numpy as np
def norm(s): return re.sub(r'[^a-z0-9%]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())
def transcrever_audio(audio, modelo):
    """GPU NVIDIA (CUDA, float16) quando houver; senão CPU int8. No Windows as DLLs do CUDA vêm dos pacotes
    pip nvidia-cublas-cu12 / nvidia-cudnn-cu12 (instalar.sh) e precisam ser registradas antes de carregar o modelo."""
    import os, glob
    from faster_whisper import WhisperModel
    if os.name == 'nt':
        for d in glob.glob(os.path.join(sys.prefix, 'Lib', 'site-packages', 'nvidia', '*', 'bin')):
            os.add_dll_directory(d); os.environ['PATH'] = d + os.pathsep + os.environ['PATH']
    # no Mac não há CUDA: vai direto para a CPU (sem a mensagem de erro a cada transcrição)
    for disp, tipo in ((('cpu', 'int8'),) if sys.platform == 'darwin' else (('cuda', 'float16'), ('cpu', 'int8'))):
        try:
            segs, _ = WhisperModel(modelo, device=disp, compute_type=tipo).transcribe(audio, language='pt', word_timestamps=True, vad_filter=True)
            segs = list(segs)   # a GPU só falha de verdade aqui (DLL carregada sob demanda)
            print('whisper em', disp, file=sys.stderr); return segs
        except Exception as e:
            if disp == 'cpu': raise
            print('GPU indisponível, usando CPU:', str(e)[:120], file=sys.stderr)
def ouvir(arq, modelo):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', arq, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    segs = transcrever_audio(audio, modelo)
    return [{'w': w.word.strip(), 't': round(w.start, 3), 'e': round(w.end, 3)} for s in segs for w in s.words if w.word.strip()]
def tokens(roteiro):
    # cada item: (exibido, [palavras faladas])
    out = []
    for m in re.finditer(r'\[\[([^|\]]+)\|([^\]]+)\]\]|(\S+)', roteiro):
        if m.group(3): out.append((m.group(3), [m.group(3)]))
        else:
            ex, fa = m.group(1).split(), m.group(2).split()
            # pontuação logo depois do [[...]] fica grudada na última palavra exibida
            out.append((' '.join(ex), fa))
    # junta pontuação solta (ex.: "]]," vira token ",")
    res = []
    for ex, fa in out:
        if res and re.fullmatch(r'[.,!?;:]+', ex): res[-1] = (res[-1][0] + ex, res[-1][1])
        else: res.append((ex, fa))
    return res
def alinhar(ouvidas, roteiro):
    toks = tokens(roteiro); flat = [(i, norm(f)) for i, (_, fs) in enumerate(toks) for f in fs]
    a = [norm(w['w']) for w in ouvidas]; b = [f for _, f in flat]
    tempo = [None] * len(flat)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
            for k in range(j2 - j1): tempo[j1 + k] = (ouvidas[i1 + k]['t'], ouvidas[i1 + k]['e'])
        elif tag == 'replace':   # trecho com contagem diferente: espalha o tempo do trecho ouvido
            t0, t1 = ouvidas[i1]['t'], ouvidas[i2 - 1]['e']
            for k in range(j2 - j1): tempo[j1 + k] = (t0 + (t1 - t0) * k / (j2 - j1), t0 + (t1 - t0) * (k + 1) / (j2 - j1))
    # buracos (palavra do roteiro que o Whisper não ouviu): interpola entre vizinhos
    for j in range(len(tempo)):
        if tempo[j] is None:
            ant = next((tempo[k][1] for k in range(j - 1, -1, -1) if tempo[k]), 0.0)
            prox = next((tempo[k][0] for k in range(j + 1, len(tempo)) if tempo[k]), ant + 0.3)
            tempo[j] = (ant, max(ant + 0.05, prox))
    out = []
    for i, (ex, _) in enumerate(toks):
        js = [j for j, (ti, _) in enumerate(flat) if ti == i]
        # "Marca X" exibida fica UMA palavra (a legenda nunca separa a marca) com o tempo de todo o trecho falado
        out.append({'w': ex, 't': round(tempo[js[0]][0], 3), 'e': round(tempo[js[-1]][1], 3)})
    return out
def main():
    a = sys.argv[1:]; arq, saida = a[0], a[1]
    modelo = a[a.index('--modelo') + 1] if '--modelo' in a else 'small'
    ouvidas = ouvir(arq, modelo)
    words = alinhar(ouvidas, open(a[a.index('--roteiro') + 1], encoding='utf-8').read()) if '--roteiro' in a else ouvidas
    json.dump(words, open(saida, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    open(re.sub(r'\.json$', '', saida) + '.txt', 'w', encoding='utf-8').write(' '.join(f"{w['t']:.2f}:{w['w']}" for w in words) + '\n')
    print(len(words), 'palavras →', saida)
if __name__ == '__main__': main()
