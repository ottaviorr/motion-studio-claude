"""Transcrição em frases numeradas, para ler o vídeo como roteiro (decupagem narrativa).
uso: python frases.py fonte/palavras.json [--pausa 0.6] > fonte/frases.txt
Cada linha: nº · [início–fim do bruto] · texto. Pausa longa vira linha "~ pausa Xs".
Frase = termina em . ? ! ou numa pausa ≥ --pausa. Use os números para escrever a decupagem (narrativa.md)."""
import sys, json
a = sys.argv[1:]; W = json.load(open(a[0]))
PAUSA = float(a[a.index('--pausa') + 1]) if '--pausa' in a else .6
frases, cur = [], []
for i, w in enumerate(W):
    if cur and w['t'] - cur[-1]['e'] >= PAUSA:
        frases.append((cur, w['t'] - cur[-1]['e'])); cur = []
    cur.append(w)
    if w['w'][-1:] in '.?!': frases.append((cur, 0)); cur = []
if cur: frases.append((cur, 0))
for n, (f, p) in enumerate(frases, 1):
    print(f"{n:3d} [{f[0]['t']:7.2f}–{f[-1]['e']:7.2f}] {' '.join(w['w'] for w in f)}")
    if p >= 1.5: print(f"      ~ pausa {p:.1f}s")
