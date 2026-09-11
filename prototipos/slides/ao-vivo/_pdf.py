# -*- coding: utf-8 -*-
"""Gera os dois PDFs que vão para a equipe: o deck e o roteiro de fala.

São arquivos para mandar, não para ensaiar dentro. O `deck.html` e o
`ROTEIRO.html` continuam sendo as ferramentas; estes dois PDFs existem para a
Ana e o Hygor abrirem no celular sem depender de nada.

  · CRONOS-DECK.pdf     — um slide por página, 1600x900, do jeito que projeta.
  · CRONOS-ROTEIRO.pdf  — uma página por slide, em A4 deitado: a imagem do
                          slide de um lado, a fala do outro. Sem palavras-chave
                          e sem nota de conferência: essas são ferramentas de
                          ensaio, e aqui o que importa é o texto corrido.

Os dois saem das MESMAS fotos, capturadas do `deck.html` já montado, para não
existir a chance de o PDF mostrar uma versão e a projeção outra.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_pdf.py
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_pdf.py --sem-foto
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
DECK = AQUI / "deck.html"
ROTEIRO = AQUI / "ROTEIRO.html"
FOTOS = AQUI / "_png" / "roteiro"
IMGS = AQUI / "_pdf" / "img"
SAIDA = AQUI / "_pdf"
CHROME = (r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
          r"\chromium-1217\chrome-win64\chrome.exe")

# o mesmo tempo do verificador: nada no deck pode terminar depois disso
ASSENTA_MS = 4200
PPM = 145  # o ritmo que o relógio do roteiro usa, para somar o tempo de cada um

EQUIPE = {
    "igor":  ("Igor",  "../../../brand/equipe/igor.png"),
    "ana":   ("Ana",   "../../../brand/equipe/ana-beatriz.png"),
    "hygor": ("Hygor", "../../../brand/equipe/hygor.png"),
}
FONTES = ("https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800"
          "&display=swap")


# ═══════════════════════════════════════════════════════════════════════════
# o que o roteiro guarda
# ═══════════════════════════════════════════════════════════════════════════
def le_falas() -> list[dict]:
    """Lê as entradas do ROTEIRO.html.

    Fatiar entre os inícios e não casar o fecho: várias entradas têm `},` no
    meio, nos objetos de `versoes`, e um casamento preguiçoso engole a seguinte.
    """
    t = ROTEIRO.read_text(encoding="utf-8")
    ini = [(int(m.group(1)), m.start()) for m in re.finditer(r"^(\d+): \{$", t, re.M)]
    if not ini:
        raise SystemExit("não achei nenhuma entrada no ROTEIRO.html")

    entradas = []
    for i, (n, pos) in enumerate(ini):
        corpo = t[pos:(ini[i + 1][1] if i + 1 < len(ini) else len(t))]
        fala = re.search(r"fala: \[(.*?)\]", corpo, re.S).group(1)
        entradas.append({
            "n": n,
            "titulo": re.search(r'titulo: "([^"]*)"', corpo).group(1),
            "quem": re.search(r'quem: "([a-z]+)"', corpo).group(1),
            "fala": json.loads("[" + fala + "]"),
        })
    return entradas


# ═══════════════════════════════════════════════════════════════════════════
# 1 · as fotos
# ═══════════════════════════════════════════════════════════════════════════
def captura(pw) -> list[int]:
    """Duas fotos por slide, do mesmo quadro assentado.

    O PNG é o que o ROTEIRO.html já referencia na miniatura. O JPEG existe só
    para os PDFs: em PNG os dois arquivos passavam de 30 MB cada, que não se
    manda para ninguém. Em JPEG de qualidade 86 ficam em torno de 5 MB e a
    diferença não aparece nem no papel nem na tela.
    """
    FOTOS.mkdir(parents=True, exist_ok=True)
    IMGS.mkdir(parents=True, exist_ok=True)
    nav = pw.chromium.launch(executable_path=CHROME)
    # escala 1,5: em 1 as letras finas do rodapé ficam com degrau, e em 2 o
    # arquivo dobra sem ganho visível
    pg = nav.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1.5)
    pg.goto(DECK.as_uri())
    # a barra do visualizador é ferramenta de ensaio e não entra na foto. O
    # marcador de quem apresenta, sim: ele agora faz parte do slide.
    pg.add_style_tag(content="#chrome{display:none!important}")
    pg.wait_for_timeout(900)

    numeros = pg.evaluate(
        "() => [...new Set([...document.querySelectorAll('.slide')]"
        ".map(s => +s.dataset.slide))].sort((a,b) => a-b)")
    for n in numeros:
        pg.evaluate(f"() => window.cronosIr({n}, 0)")
        pg.wait_for_timeout(ASSENTA_MS)
        pg.screenshot(path=str(FOTOS / f"{n:02d}.png"))
        pg.screenshot(path=str(IMGS / f"{n:02d}.jpg"), type="jpeg", quality=86)
        print(f"  slide {n:02d}")
    nav.close()
    return numeros


# ═══════════════════════════════════════════════════════════════════════════
# 2 · o PDF do deck
# ═══════════════════════════════════════════════════════════════════════════
def pagina_deck(numeros: list[int]) -> str:
    paginas = "\n".join(
        f'<div class="pg"><img src="_pdf/img/{n:02d}.jpg" alt=""></div>'
        for n in numeros)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Cronos · deck da banca</title><style>
@page{{size:1600px 900px;margin:0}}
html,body{{margin:0;padding:0;background:#fff}}
.pg{{width:1600px;height:900px;overflow:hidden;page-break-after:always}}
.pg:last-child{{page-break-after:auto}}
.pg img{{display:block;width:1600px;height:900px}}
</style></head><body>{paginas}</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════
# 3 · o PDF do roteiro
# ═══════════════════════════════════════════════════════════════════════════
def pagina_roteiro(entradas: list[dict], so: str | None = None) -> str:
    """O roteiro em A4 deitado. Com `so`, sai a versão de uma pessoa só.

    A versão individual não é um recorte cego: cada página diz de quem ela está
    pegando a vez, e a primeira é um índice dos slides dela. Sem isso, quem só
    tem as próprias páginas não sabe quando entra — que é o que se erra ao vivo.
    """
    por = {}
    for e in entradas:
        d = por.setdefault(e["quem"], {"slides": [], "pal": 0})
        d["slides"].append(e["n"])
        d["pal"] += len(re.sub(r"<[^>]+>", "", " ".join(e["fala"])).split())

    dono = {e["n"]: e["quem"] for e in entradas}

    def relogio(pal: int) -> str:
        m, s = divmod(round(pal / PPM * 60), 60)
        return f"{m}min{s:02d}" if m else f"{s}s"

    def faixas(ns: list[int]) -> str:
        """01 02 07 08 09  ->  01–02 · 07–09, que é como se lê de relance."""
        L, ini, ant = [], ns[0], ns[0]
        for n in ns[1:] + [None]:
            if n != ant + 1:
                L.append(f"{ini:02d}" if ini == ant else f"{ini:02d}–{ant:02d}")
                ini = n
            ant = n
        return " · ".join(L)

    def vez(n: int) -> str:
        """De quem esta página está pegando a vez."""
        d = dono[n]
        if n == min(dono):
            return "Abre a apresentação"
        ant = dono.get(n - 1)
        if ant and ant != d:
            return f"Entra depois de {EQUIPE[ant][0]}"
        return ""

    total = relogio(sum(d["pal"] for d in por.values()))

    if so:
        eu = por[so]
        capa = f"""<article class="pg cp q-{so}">
  <img class="cara" src="{EQUIPE[so][1]}" alt="">
  <h1>{EQUIPE[so][0]}</h1>
  <p class="dz">Roteiro da banca · 15 de setembro de 2026</p>
  <p class="qt">{len(eu['slides'])} slides · {relogio(eu['pal'])} de fala ·
     {faixas(eu['slides'])}</p>
</article>"""
    else:
        cartoes = "".join(
            f'<div class="p"><img src="{EQUIPE[k][1]}" alt="">'
            f'<div><b>{EQUIPE[k][0]}</b>'
            f'<span>{faixas(por[k]["slides"])}</span>'
            f'<i>{len(por[k]["slides"])} slides · {relogio(por[k]["pal"])}</i></div></div>'
            for k in ("igor", "ana", "hygor") if k in por)
        capa = f"""<article class="pg capa">
  <h1>Cronos<span>Roteiro da banca · 15/09/2026</span></h1>
  <div class="quadro">{cartoes}</div>
  <p class="obs">Cada página traz um slide e a fala dele. O tempo é estimado a
     {PPM} palavras por minuto e soma <b>{total}</b> — a demonstração ao vivo,
     no slide 31, corre por fora dessa conta.</p>
</article>"""

    corpo = [capa]
    for e in entradas:
        if so and e["quem"] != so:
            continue
        nome, foto = EQUIPE[e["quem"]]
        paras = "".join(f"<p>{p}</p>" for p in e["fala"])
        troca = vez(e["n"])
        corpo.append(f"""<article class="pg">
  <header>
    <span class="n">Slide {e['n']:02d}</span>
    <h2>{html.escape(e['titulo'])}</h2>
    {f'<span class="vez">{troca}</span>' if troca else ''}
    <span class="quem"><img src="{foto}" alt=""><b>{nome}</b></span>
  </header>
  <div class="corpo">
    <img class="sl" src="_pdf/img/{e['n']:02d}.jpg" alt="">
    <div class="fala">{paras}</div>
  </div>
</article>""")

    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Cronos · roteiro da banca</title>
<link rel="stylesheet" href="{FONTES}">
<style>
@page{{size:A4 landscape;margin:0}}
:root{{--tt:#0B0F16;--tx:#3C4654;--tx2:#6B7785;--tx3:#9AA3B0;
  --ln:#E3E8EF;--az:#2563EB}}
html,body{{margin:0;padding:0;background:#fff;color:var(--tx);
  font-family:"Outfit",system-ui,sans-serif;-webkit-print-color-adjust:exact;
  print-color-adjust:exact}}
.pg{{width:297mm;height:210mm;box-sizing:border-box;padding:13mm 14mm;
  display:flex;flex-direction:column;page-break-after:always;overflow:hidden}}
.pg:last-child{{page-break-after:auto}}

/* ── cabeçalho: número, título e de quem é a vez ─────────────────────────── */
header{{display:flex;align-items:center;gap:12px;padding-bottom:7mm;
  border-bottom:1px solid var(--ln);margin-bottom:8mm}}
header .n{{font-size:10.5pt;font-weight:800;letter-spacing:.14em;
  text-transform:uppercase;color:var(--az);white-space:nowrap}}
header h2{{margin:0;font-size:17pt;font-weight:700;color:var(--tt);
  letter-spacing:-.3px;flex:1;min-width:0;line-height:1.2}}
header .quem{{display:inline-flex;align-items:center;gap:8px;white-space:nowrap;
  flex-shrink:0}}
header .quem img{{width:26px;height:26px;border-radius:50%;object-fit:cover;
  box-shadow:0 0 0 1px var(--ln)}}
header .quem b{{font-size:12pt;font-weight:700;color:var(--tt)}}

/* ── o slide de um lado, a fala do outro ─────────────────────────────────── */
.corpo{{display:grid;grid-template-columns:148mm 1fr;gap:9mm;flex:1;min-height:0}}
.corpo .sl{{width:148mm;height:83.25mm;display:block;border-radius:3mm;
  box-shadow:0 0 0 1px var(--ln)}}
.fala p{{margin:0 0 4.5mm;font-size:12.5pt;line-height:1.62;color:var(--tt)}}
.fala p:last-child{{margin-bottom:0}}
.fala em{{font-style:normal;font-weight:700;color:var(--az)}}
.fala b{{font-weight:700}}

/* ── a capa: quem pega o quê ─────────────────────────────────────────────── */
.capa{{justify-content:center}}
.capa h1{{margin:0 0 12mm;font-size:34pt;font-weight:800;color:var(--tt);
  letter-spacing:-1.2px;line-height:1}}
.capa h1 span{{display:block;font-size:13pt;font-weight:500;color:var(--tx2);
  letter-spacing:0;margin-top:4mm}}
.quadro{{display:flex;gap:8mm}}
.quadro .p{{flex:1;display:flex;align-items:center;gap:10px;padding:6mm 7mm;
  border:1px solid var(--ln);border-radius:4mm}}
.quadro .p img{{width:44px;height:44px;border-radius:50%;object-fit:cover;
  box-shadow:0 0 0 1px var(--ln)}}
.quadro .p b{{display:block;font-size:14pt;font-weight:700;color:var(--tt)}}
.quadro .p span{{display:block;font-size:11pt;color:var(--tx);margin-top:1mm}}
.quadro .p i{{display:block;font-style:normal;font-size:9.5pt;color:var(--tx2);
  margin-top:1.5mm}}
.obs{{margin:10mm 0 0;font-size:11pt;line-height:1.6;color:var(--tx2);max-width:75%}}
.obs b{{color:var(--tt)}}

/* ── a troca de voz, no cabeçalho da página ──────────────────────────────── */
header .vez{{font-size:9.5pt;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;color:var(--tx2);background:#F2F5F9;
  border-radius:999px;padding:2mm 4mm;white-space:nowrap;flex-shrink:0}}

/* ── a primeira página de uma pessoa só ──────────────────────────────────── */
/* Rosto, nome e três linhas. Duas tentativas antes desta puseram um resumo de
   todos os slides aqui — um tabuleiro de fichas, depois um índice — e as duas
   transformaram a abertura num relatório. O que ela precisa dizer é de quem é
   este caderno; o resto está nas páginas. */
.q-igor{{--qc:#DC2626}} .q-hygor{{--qc:#2563EB}} .q-ana{{--qc:#CA8A04}}
.cp{{align-items:center;justify-content:center;text-align:center}}
.cp .cara{{width:62mm;height:62mm;border-radius:50%;object-fit:cover;
  box-shadow:0 0 0 2mm color-mix(in srgb, var(--qc) 16%, #fff)}}
.cp h1{{margin:11mm 0 0;font-size:46pt;font-weight:800;color:var(--tt);
  letter-spacing:-1.8px;line-height:1}}
.cp .dz{{margin:5mm 0 0;font-size:13pt;color:var(--tx2)}}
.cp .qt{{margin:9mm 0 0;padding-top:6mm;border-top:1px solid var(--ln);
  font-size:12pt;color:var(--tx2)}}
</style></head><body>{''.join(corpo)}</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════
def imprime(pw, html_txt: str, nome: str, **opts) -> Path:
    """Grava o HTML ao lado do deck (para os caminhos relativos valerem) e imprime."""
    tmp = AQUI / f"_tmp_{nome}.html"
    tmp.write_text(html_txt, encoding="utf-8")
    nav = pw.chromium.launch(executable_path=CHROME)
    pg = nav.new_page()
    pg.goto(tmp.as_uri())
    pg.wait_for_load_state("networkidle")
    pg.wait_for_timeout(600)
    destino = SAIDA / nome
    pg.pdf(path=str(destino), print_background=True,
           margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, **opts)
    nav.close()
    tmp.unlink()
    return destino


def main() -> int:
    SAIDA.mkdir(parents=True, exist_ok=True)
    entradas = le_falas()

    with sync_playwright() as pw:
        if "--sem-foto" in sys.argv:
            numeros = sorted(int(p.stem) for p in IMGS.glob("[0-9][0-9].jpg"))
            print(f"reaproveitando {len(numeros)} fotos de _pdf/img/")
        else:
            print("fotografando o deck…")
            numeros = captura(pw)

        faltando = [e["n"] for e in entradas if e["n"] not in numeros]
        if faltando:
            raise SystemExit(f"sem foto para os slides {faltando}")

        d = imprime(pw, pagina_deck(numeros), "CRONOS-DECK.pdf",
                    width="1600px", height="900px")
        print(f"\n{d.name}  ·  {d.stat().st_size / 1e6:.1f} MB  ·  {len(numeros)} páginas")

        r = imprime(pw, pagina_roteiro(entradas), "CRONOS-ROTEIRO.pdf",
                    format="A4", landscape=True)
        print(f"{r.name}  ·  {r.stat().st_size / 1e6:.1f} MB  ·  {len(entradas) + 1} páginas")

        # um por pessoa: quem apresenta não devia folhear as páginas dos outros
        for k in ("igor", "ana", "hygor"):
            quantos = sum(1 for e in entradas if e["quem"] == k)
            u = imprime(pw, pagina_roteiro(entradas, so=k),
                        f"CRONOS-ROTEIRO-{k.upper()}.pdf", format="A4", landscape=True)
            print(f"{u.name}  ·  {u.stat().st_size / 1e6:.1f} MB  ·  {quantos + 1} páginas")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
