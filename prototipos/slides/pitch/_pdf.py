# -*- coding: utf-8 -*-
"""Gera os PDFs de distribuição do deck do vídeo pitch.

São arquivos para mandar, não para ensaiar dentro. O `deck.html` continua sendo
a ferramenta; estes PDFs existem para a Ana e o Hygor abrirem no celular e
saberem exatamente quais quadros cada um grava.

  · CRONOS-PITCH.pdf        — os 21 quadros, um por página, do jeito que projeta
  · CRONOS-PITCH-ANA.pdf    — só os quadros da Ana
  · CRONOS-PITCH-HYGOR.pdf  — só os quadros do Hygor

Sem roteiro de fala, de propósito: eles já sabem o que falar, e a fala da banca
era conversada em três vozes, que não é o que vai para o vídeo.

As imagens saem em PNG (para montar no Canva) e em JPEG (para os PDFs não
passarem de alguns MB).

Uso:
    .venv/Scripts/python.exe prototipos/slides/pitch/_pdf.py
    .venv/Scripts/python.exe prototipos/slides/pitch/_pdf.py --sem-foto
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from _montar import ORDEM  # noqa: E402

AQUI = Path(__file__).parent
DECK = AQUI / "deck.html"
ROTEIRO_BANCA = AQUI.parent / "ao-vivo" / "ROTEIRO.html"
PNGS = AQUI / "_png" / "quadros"
IMGS = AQUI / "_pdf" / "img"
SAIDA = AQUI / "_pdf"
CHROME = (r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
          r"\chromium-1217\chrome-win64\chrome.exe")

ASSENTA_MS = 4200          # o mesmo tempo do verificador da banca

EQUIPE = {
    "igor": ("Igor", "../../../brand/equipe/igor.png"),
    "ana": ("Ana", "../../../brand/equipe/ana-beatriz.png"),
    "hygor": ("Hygor", "../../../brand/equipe/hygor.png"),
}
FONTES = ("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700"
          "&family=Outfit:wght@400;500;600;700;800&display=swap")

# título dos quadros que não vêm da banca
TITULOS_PROPRIOS = {"objetivo": "Objetivo do projeto"}

# o quadro da demonstração não rende um áudio como os outros: ali a gravação é
# da tela, com a narração por cima. O nome do arquivo segue o mesmo padrão, para
# a ordem alfabética continuar sendo a ordem da linha do tempo.
DEMO = 31
ICONE_MIC = ('<rect x="9" y="2.6" width="6" height="11.4" rx="3"/>'
             '<path d="M5.4 11.4a6.6 6.6 0 0 0 13.2 0"/><path d="M12 18v3.4"/>')
ICONE_DEMO = ('<rect x="2.6" y="4.4" width="18.8" height="13" rx="2.2"/>'
              '<path d="M8.6 21h6.8"/><path d="M12 17.4V21"/>')


def titulos_da_banca() -> dict[int, str]:
    t = ROTEIRO_BANCA.read_text(encoding="utf-8")
    return {int(n): tit for n, tit in
            re.findall(r"^(\d+): \{\s*\n\s*titulo: \"([^\"]*)\"", t, re.M)}


def quadros() -> list[dict]:
    """Um registro por quadro: número no vídeo, título e de quem é a voz."""
    deck = DECK.read_text(encoding="utf-8")
    quem = dict(re.findall(r'data-slide="(\d+)"[^>]*data-quem="([a-z]+)"', deck))
    banca = titulos_da_banca()

    fora = []
    saida = []
    for novo, item in enumerate(ORDEM, start=1):
        titulo = (TITULOS_PROPRIOS.get(item, item) if isinstance(item, str)
                  else banca.get(item, f"Slide {item}"))
        dono = quem.get(str(novo))
        if dono not in EQUIPE:
            fora.append(novo)
            continue
        saida.append({"n": novo, "titulo": titulo, "quem": dono,
                      "origem": item if isinstance(item, int) else None})
    if fora:
        raise SystemExit(f"quadros sem data-quem reconhecido: {fora}")
    return saida


def captura(pw, numeros: list[int]) -> None:
    PNGS.mkdir(parents=True, exist_ok=True)
    IMGS.mkdir(parents=True, exist_ok=True)
    nav = pw.chromium.launch(executable_path=CHROME)
    pg = nav.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1.5)
    pg.goto(DECK.as_uri())
    pg.add_style_tag(content="#chrome{display:none!important}")
    pg.wait_for_timeout(900)
    for n in numeros:
        pg.evaluate(f"() => window.cronosIr({n}, 0)")
        pg.wait_for_timeout(ASSENTA_MS)
        pg.screenshot(path=str(PNGS / f"{n:02d}.png"))
        pg.screenshot(path=str(IMGS / f"{n:02d}.jpg"), type="jpeg", quality=88)
        print(f"  quadro {n:02d}")
    nav.close()


def nome_audio(q: dict) -> str:
    """O nome que o áudio daquele quadro tem que ter.

    O número do quadro vem na frente, com zero à esquerda, porque a ordem
    alfabética dos arquivos passa a ser a ordem da linha do tempo do vídeo: na
    montagem é só arrastar de cima para baixo. O primeiro nome no fim separa os
    arquivos das duas pessoas quando eles caem na mesma pasta.
    """
    return f"{q['n']:02d}-{q['quem']}"


def faixas(ns: list[int]) -> str:
    """01 02 07 08 09  ->  01–02 · 07–09, que é como se lê de relance."""
    L, ini, ant = [], ns[0], ns[0]
    for n in ns[1:] + [None]:
        if n != ant + 1:
            L.append(f"{ini:02d}" if ini == ant else f"{ini:02d}–{ant:02d}")
            ini = n
        ant = n
    return " · ".join(L)


def pagina_deck(qs: list[dict]) -> str:
    paginas = "\n".join(
        f'<div class="pg"><img src="_pdf/img/{q["n"]:02d}.jpg" alt=""></div>' for q in qs)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Cronos · deck do vídeo pitch</title><style>
@page{{size:1600px 900px;margin:0}}
html,body{{margin:0;padding:0;background:#fff}}
.pg{{width:1600px;height:900px;overflow:hidden;page-break-after:always}}
.pg:last-child{{page-break-after:auto}}
.pg img{{display:block;width:1600px;height:900px}}
</style></head><body>{paginas}</body></html>"""


def pagina_pessoa(qs: list[dict], so: str) -> str:
    """Os quadros de uma pessoa. Uma página por quadro, sem fala.

    Cada página diz o número do quadro no deck inteiro e a posição dele na
    sequência da pessoa, porque na hora de gravar o áudio o que se procura é
    "qual é o próximo meu", e não "qual é o próximo".
    """
    nome, foto = EQUIPE[so]
    meus = [q for q in qs if q["quem"] == so]
    total = len(qs)

    lista = "".join(
        f'<li><code>{nome_audio(q)}</code><span>{html.escape(q["titulo"])}</span></li>'
        for q in meus)
    corpo = [f"""<article class="pg cp q-{so}">
  <img class="cara" src="{foto}" alt="">
  <h1>{nome}</h1>
  <p class="dz">Slides do vídeo pitch · Cronos</p>
  <p class="qt"><b>{len(meus)} quadros</b> para gravar &middot; {faixas([q['n'] for q in meus])}</p>
  <div class="arq">
    <p class="ct">Grave um áudio por quadro e salve com este nome:</p>
    <ul>{lista}</ul>
    <p class="ob">A extensão pode ser a que o seu gravador gerar, não precisa converter.
      Se regravar algum, mande só o novo.</p>
  </div>
</article>"""]

    for i, q in enumerate(meus, start=1):
        corpo.append(f"""<article class="pg">
  <header>
    <span class="n">Quadro {q['n']:02d} de {total}</span>
    <h2>{html.escape(q['titulo'])}</h2>
    <span class="seq">{i}º de {len(meus)} seus</span>
  </header>
  <div class="salvar">
    <svg viewBox="0 0 24 24" aria-hidden="true">{ICONE_DEMO if q['origem'] == DEMO else ICONE_MIC}</svg>
    <span class="lb">{'Grave a tela com a narração e salve como'
                      if q['origem'] == DEMO else 'Salve o áudio como'}</span>
    <code>{nome_audio(q)}</code>
  </div>
  <img class="sl" src="_pdf/img/{q['n']:02d}.jpg" alt="">
</article>""")

    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Cronos · vídeo pitch · {nome}</title>
<link rel="stylesheet" href="{FONTES}">
<style>
@page{{size:A4 landscape;margin:0}}
:root{{--tt:#0B0F16;--tx:#3C4654;--tx2:#6B7785;--ln:#E3E8EF;--az:#2563EB}}
html,body{{margin:0;padding:0;background:#fff;color:var(--tx);
  font-family:"Outfit",system-ui,sans-serif;-webkit-print-color-adjust:exact;
  print-color-adjust:exact}}
.pg{{width:297mm;height:210mm;box-sizing:border-box;padding:12mm 14mm;
  display:flex;flex-direction:column;page-break-after:always;overflow:hidden}}
.pg:last-child{{page-break-after:auto}}

header{{display:flex;align-items:center;gap:12px;padding-bottom:5mm;
  border-bottom:1px solid var(--ln);margin-bottom:6mm}}
header .n{{font-size:10.5pt;font-weight:800;letter-spacing:.14em;text-transform:uppercase;
  color:var(--az);white-space:nowrap}}
header h2{{margin:0;font-size:17pt;font-weight:700;color:var(--tt);letter-spacing:-.3px;
  flex:1;min-width:0;line-height:1.2}}
header .seq{{font-size:9.5pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:var(--tx2);background:#F2F5F9;border-radius:999px;padding:2mm 4mm;white-space:nowrap}}

/* o nome do arquivo é a informação operacional da página: fica antes do slide,
   no caminho do olho, e não num rodapé que ninguém lê */
.salvar{{display:flex;align-items:center;gap:4mm;margin-bottom:5mm}}
.salvar svg{{width:6mm;height:6mm;fill:none;stroke:var(--az);stroke-width:1.6;
  stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}}
.salvar .lb{{font-size:10pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
  color:var(--tx2)}}
.salvar code{{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:15pt;
  font-weight:700;color:var(--az);background:#EFF4FF;border:1px solid #D6E2FB;
  border-radius:2.5mm;padding:1.6mm 4mm;letter-spacing:.02em}}
.sl{{width:100%;height:auto;display:block;border-radius:3mm;box-shadow:0 0 0 1px var(--ln)}}

/* a capa: de quem é o caderno e o que fazer com ele */
.q-igor{{--qc:#DC2626}} .q-hygor{{--qc:#2563EB}} .q-ana{{--qc:#CA8A04}}
.cp{{align-items:center;justify-content:center;text-align:center}}
.cp .cara{{width:40mm;height:40mm;border-radius:50%;object-fit:cover;
  box-shadow:0 0 0 2mm color-mix(in srgb, var(--qc) 16%, #fff)}}
.cp h1{{margin:6mm 0 0;font-size:34pt;font-weight:800;color:var(--tt);letter-spacing:-1.4px;
  line-height:1}}
.cp .dz{{margin:3mm 0 0;font-size:12.5pt;color:var(--tx2)}}
.cp .qt{{margin:5mm 0 0;padding-top:4mm;border-top:1px solid var(--ln);font-size:12pt;
  color:var(--tx2)}}
.cp .qt b{{color:var(--tt);font-weight:700}}

/* a lista dos nomes de arquivo, na capa: a pessoa vê de uma vez o que tem que
   entregar, e o padrão fica explicado uma vez só */
.cp .arq{{margin:7mm 0 0;text-align:left;border:1px solid var(--ln);border-radius:4mm;
  padding:6mm 8mm}}
.cp .arq .ct{{margin:0;font-size:11.5pt;font-weight:600;color:var(--tt)}}
.cp .arq ul{{list-style:none;margin:4mm 0 0;padding:0;display:grid;
  grid-template-columns:1fr 1fr;gap:2.5mm 8mm}}
.cp .arq li{{display:flex;align-items:baseline;gap:3mm;font-size:10.5pt;color:var(--tx2)}}
.cp .arq code{{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11pt;
  font-weight:700;color:var(--az);white-space:nowrap}}
.cp .arq .ob{{margin:5mm 0 0;padding-top:4mm;border-top:1px solid var(--ln);
  font-size:10.5pt;line-height:1.5;color:var(--tx2)}}
</style></head><body>{''.join(corpo)}</body></html>"""


def imprime(pw, html_txt: str, nome: str, **opts) -> Path:
    """Grava o HTML ao lado do deck, para os caminhos relativos valerem."""
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
    qs = quadros()
    numeros = [q["n"] for q in qs]

    with sync_playwright() as pw:
        if "--sem-foto" in sys.argv:
            print(f"reaproveitando as fotos de {IMGS}")
        else:
            print("fotografando o deck…")
            captura(pw, numeros)

        d = imprime(pw, pagina_deck(qs), "CRONOS-PITCH.pdf",
                    width="1600px", height="900px")
        print(f"\n{d.name}  ·  {d.stat().st_size / 1e6:.1f} MB  ·  {len(qs)} páginas")

        for k in ("igor", "ana", "hygor"):
            meus = [q for q in qs if q["quem"] == k]
            if not meus:
                continue
            u = imprime(pw, pagina_pessoa(qs, k), f"CRONOS-PITCH-{k.upper()}.pdf",
                        format="A4", landscape=True)
            print(f"{u.name}  ·  {u.stat().st_size / 1e6:.1f} MB  ·  "
                  f"{len(meus)} quadros  ·  {faixas([q['n'] for q in meus])}")

    print(f"\nPNGs para montar no Canva: {PNGS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
