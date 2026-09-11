# -*- coding: utf-8 -*-
"""Captura um PNG por slide para o roteiro, na composição que vai ao ar.

O roteiro precisa da miniatura do slide ao lado da fala. Ela sai daqui, e não do
_verifica.py: aquele fotografa TODAS as composições, com nome por variação, e
serve para conferência. Este fotografa UMA por slide — a primeira, que é a
escolhida sempre que o slide já foi decidido — e grava com o número puro, que é
o que o ROTEIRO.html referencia.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_roteiro_png.py        (tudo)
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_roteiro_png.py 1 2    (só estes)
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
DECK = AQUI / "deck.html"
SAIDA = AQUI / "_png" / "roteiro"
CHROME = (
    r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
    r"\chromium-1217\chrome-win64\chrome.exe"
)
# o mesmo tempo do verificador: nada no deck pode terminar depois disso
ASSENTA_MS = 4200


def main() -> int:
    SAIDA.mkdir(parents=True, exist_ok=True)
    pedidos = [int(a) for a in sys.argv[1:]]

    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        # escala 1,5: o roteiro mostra a miniatura em ~520px e o dono do projeto
        # amplia para conferir texto. Em 1 fica borrado, em 2 o arquivo dobra.
        pg = nav.new_page(viewport={"width": 1600, "height": 900},
                          device_scale_factor=1.5)
        pg.goto(DECK.as_uri())
        # a barra do visualizador e o marcador de quem apresenta ficam fora da
        # foto: a primeira é ferramenta de ensaio, e o segundo ainda não está
        # decidido — o roteiro é sobre o que se fala, não sobre quem fala.
        pg.add_style_tag(content="#chrome,.apres{display:none!important}")
        pg.wait_for_timeout(900)

        numeros = pg.evaluate(
            "() => [...new Set([...document.querySelectorAll('.slide')]"
            ".map(s => +s.dataset.slide))].sort((a,b) => a-b)")
        alvos = [n for n in numeros if not pedidos or n in pedidos]

        for n in alvos:
            pg.evaluate(f"() => window.cronosIr({n}, 0)")
            pg.wait_for_timeout(ASSENTA_MS)
            pg.screenshot(path=str(SAIDA / f"{n:02d}.png"))
            print(f"  slide {n:02d}")

        nav.close()

    print(f"\n{len(alvos)} PNG em _png/roteiro/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
