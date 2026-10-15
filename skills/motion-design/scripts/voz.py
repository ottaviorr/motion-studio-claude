"""Narração a partir de um roteiro (pt-BR).
usage: python3 voz.py roteiro.txt saida.wav [--voz "Luciana"] [--taxa 180]
Roteiro: uma frase por linha (linha em branco = pausa maior). Para a pronúncia, escreva [[exibido|falado]]:
  "Abra o [[iPhone|ai fone]] e veja."  → a legenda mostra "iPhone", a voz diz "ai fone".
Motores: macOS `say` (padrão; instale a voz "Luciana (Premium)" em Ajustes → Acessibilidade → Conteúdo Falado → Gerenciar vozes)
         ElevenLabs, se ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID estiverem no ambiente ou no .env do projeto."""
import os, re, sys, json, subprocess, tempfile, pathlib, urllib.request
falado = lambda s: re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', r'\2', s)
def env(k):
    if os.environ.get(k): return os.environ[k]
    for f in ('.env', '../.env'):
        if os.path.exists(f):
            for l in open(f):
                if l.startswith(k + '='): return l.split('=', 1)[1].strip().strip('"')
def main():
    a = sys.argv[1:]; roteiro, saida = a[0], a[1]
    voz = a[a.index('--voz') + 1] if '--voz' in a else 'Luciana'; taxa = a[a.index('--taxa') + 1] if '--taxa' in a else '180'
    linhas = open(roteiro, encoding='utf-8').read().strip().split('\n')
    key, vid = env('ELEVENLABS_API_KEY'), env('ELEVENLABS_VOICE_ID')
    tmp = pathlib.Path(tempfile.mkdtemp())
    if key and vid:
        texto = '\n'.join(falado(l) for l in linhas)
        req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}', data=json.dumps({'text': texto, 'model_id': 'eleven_multilingual_v2'}).encode(), headers={'xi-api-key': key, 'content-type': 'application/json', 'accept': 'audio/mpeg'})
        (tmp / 'v.mp3').write_bytes(urllib.request.urlopen(req).read()); src = tmp / 'v.mp3'
    else:
        # say: pausa curta entre frases e maior em linha vazia
        partes = [('[[slnc 450]]' if not l.strip() else falado(l) + ' [[slnc 180]]') for l in linhas]
        (tmp / 'r.txt').write_text(' '.join(partes), encoding='utf-8')
        subprocess.run(['say', '-v', voz, '-r', str(taxa), '-f', str(tmp / 'r.txt'), '-o', str(tmp / 'v.aiff')], check=True); src = tmp / 'v.aiff'
    # 48 kHz, mono, leve compressão e normalização de volume (soa "de anúncio")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-af', 'highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,loudnorm=I=-15:TP=-1.5:LRA=7', '-ar', '48000', '-ac', '1', saida], check=True)
    print('voz:', saida)
if __name__ == '__main__': main()
