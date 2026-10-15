#!/usr/bin/env python3
"""Confere a direção de arte de uma série (unidade × variedade).

Uso:
  python3 conferir-serie.py ESTILOS.md [outro.md ...]

Lê os blocos ```cartao``` (modelo em assets/cartao-direcao.md). Se não houver
nenhum, tenta a tabela-resumo do ESTILOS.md (colunas com 3 hex "fundo · tinta ·
destaque" e "título / apoio / número"), como no modelo assets/estilos-serie-modelo.md.

Aponta:
  - % de fundos claros (meta >= 60 %, preferência do dono) e dois escuros seguidos
  - vizinhos com a mesma família de fundo (luz + matiz), mesma fonte de título,
    mesmo estilo, mesma corrente, destaque de matiz parecida
  - fontes da lista de "padrão de IA" (HyperFrames typography.md) — só aviso
  - contraste tinta/fundo (< 4,5 bloqueia, < 7 avisa) e destaque/fundo < 3 (WCAG)
Saída 0 = nada bloqueante; 1 = há problema bloqueante (escuros seguidos, contraste ruim).
Só biblioteca padrão.
"""
import colorsys
import re
import sys

BANIDAS = {
    "inter", "roboto", "open sans", "noto sans", "arimo", "lato", "source sans",
    "source sans 3", "pt sans", "nunito", "poppins", "outfit", "sora",
    "playfair display", "cormorant garamond", "bodoni moda", "eb garamond",
    "cinzel", "prata", "syne", "montserrat",
}


def hex_rgb(h):
    h = h.strip().strip('"').strip("'").lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lum(rgb):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def familia(rgb):
    """claro/escuro + matiz grosseira (neutro quando pouca saturação)."""
    h, l, s = colorsys.rgb_to_hls(*rgb)
    luz = "claro" if lum(rgb) > 0.35 else "escuro"
    if s < 0.18 or l < 0.08 or l > 0.94:
        return luz, "neutro", None
    return luz, "cor", h * 360


def dist_matiz(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def ler_cartoes(texto):
    cards = []
    for bloco in re.findall(r"```cartao\s*\n(.*?)```", texto, re.S):
        c = {}
        for linha in bloco.splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                c[k.strip().lower()] = v.strip().strip('"').strip("'")
        if c.get("fundo", "").startswith("#") and len(c.get("fundo", "")) >= 4:
            cards.append(c)
    return cards


def ler_tabela(texto):
    cards = []
    for linha in texto.splitlines():
        if not linha.startswith("|"):
            continue
        cols = [c.strip() for c in linha.strip("|").split("|")]
        hexes = None
        fontes = None
        for c in cols:
            hx = re.findall(r"#[0-9A-Fa-f]{6}", c)
            if hexes is None and len(hx) >= 3:
                hexes = hx
            elif hexes is not None and fontes is None and c.count("/") >= 2:
                fontes = [f.strip() for f in re.sub(r"\(.*?\)", "", c).split("/")]
        if hexes and fontes:
            nome = re.sub(r"\*", "", cols[2]) if len(cols) > 2 else ""
            cards.append({
                "peca": cols[0], "estilo": nome, "fundo": hexes[0],
                "tinta": hexes[1], "destaque": hexes[2],
                "titulo": fontes[0], "apoio": fontes[1] if len(fontes) > 1 else "",
                "numero": fontes[2] if len(fontes) > 2 else "", "corrente": "",
            })
    return cards


def base_fonte(nome):
    nome = re.sub(r"\b(\d{3}|bold|black|regular|medium|italic|itálico)\b", "", nome, flags=re.I)
    return re.sub(r"\s+", " ", nome).strip().lower()


def main(arquivos):
    texto = "\n".join(open(a, encoding="utf-8").read() for a in arquivos)
    cards = ler_cartoes(texto) or ler_tabela(texto)
    if not cards:
        print("Nenhum bloco ```cartao``` nem tabela-resumo encontrada.")
        return 1
    bloqueia = False
    print(f"{len(cards)} peças\n")
    print(f"{'peça':>5}  {'fundo':8} {'família':16} {'tinta/fundo':>11} {'dest/fundo':>10}  título")
    fams = []
    for c in cards:
        f, t, d = hex_rgb(c["fundo"]), hex_rgb(c["tinta"]), hex_rgb(c["destaque"])
        fam = familia(f)
        fams.append(fam)
        ct, cd = contraste(f, t), contraste(f, d)
        rot = f"{fam[0]}/{fam[1] if fam[2] is None else int(fam[2])}"
        print(f"{c.get('peca',''):>5}  {c['fundo']:8} {rot:16} {ct:11.1f} {cd:10.1f}  {c.get('titulo','')}")
        if ct < 4.5:
            print(f"       ⛔ tinta sobre fundo com contraste {ct:.1f} (< 4,5): texto ilegível no celular")
            bloqueia = True
        elif ct < 7:
            print(f"       ⚠️ tinta sobre fundo {ct:.1f} (< 7): ok para título grande, ruim para texto pequeno")
        if cd < 3:
            print(f"       ⚠️ destaque quase some no fundo ({cd:.1f} < 3): só serve para superfície, não texto")
        for papel in ("titulo", "apoio", "numero"):
            if base_fonte(c.get(papel, "")) in BANIDAS:
                print(f"       ⚠️ {papel} '{c[papel]}' está na lista de fontes-padrão de IA: tem motivo?")

    claros = sum(1 for f in fams if f[0] == "claro")
    pct = 100 * claros / len(fams)
    print(f"\nFundos claros: {claros}/{len(fams)} ({pct:.0f} %) {'✅' if pct >= 60 else '⚠️ abaixo da meta de 60 %'}")

    print("\nVizinhos:")
    achou = False
    for i in range(1, len(cards)):
        a, b = cards[i - 1], cards[i]
        fa, fb = fams[i - 1], fams[i]
        par = f"{a.get('peca','')}→{b.get('peca','')}"
        if fa[0] == "escuro" and fb[0] == "escuro":
            print(f"  ⛔ {par}: dois fundos escuros seguidos")
            bloqueia = achou = True
        elif (fa[0] == fb[0] and fa[1] == fb[1]
              and (fa[2] is None or dist_matiz(fa[2], fb[2]) < 30)
              and abs(lum(hex_rgb(a["fundo"])) - lum(hex_rgb(b["fundo"]))) < 0.2):
            print(f"  ⚠️ {par}: mesma família de fundo ({fa[0]}, {fa[1]})")
            achou = True
        if base_fonte(a.get("titulo", "")) and base_fonte(a.get("titulo", "")) == base_fonte(b.get("titulo", "")):
            print(f"  ⚠️ {par}: mesma fonte de título ({b['titulo']})")
            achou = True
        if a.get("estilo") and a.get("estilo", "").lower() == b.get("estilo", "").lower():
            print(f"  ⚠️ {par}: mesmo estilo ({b['estilo']})")
            achou = True
        if a.get("corrente") and a.get("corrente", "").lower() == b.get("corrente", "").lower():
            print(f"  💡 {par}: mesma corrente ({b['corrente']}) — ok se o resto muda bastante")
            achou = True
        da, db = familia(hex_rgb(a["destaque"])), familia(hex_rgb(b["destaque"]))
        if da[2] is not None and db[2] is not None and dist_matiz(da[2], db[2]) < 20:
            print(f"  💡 {par}: destaques de matiz parecida")
            achou = True
    if not achou:
        print("  ✅ nenhum vizinho repetido")
    return 1 if bloqueia else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
