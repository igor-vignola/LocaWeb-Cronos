# -*- coding: utf-8 -*-
"""Compara as duas propostas de divisória de bloco com a divisória de seção da banca.

Três palcos: a divisória de seção 7 da banca (referência, para ver que não se
confundem), a proposta clara e a proposta escura, as duas renderizadas para o
bloco 2. Animação congelada no estado final.

Uso:
    .venv/Scripts/python.exe prototipos/slides/sprint4/_comparar_divisoria.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
import monta_deck_sprint4 as mk  # noqa: E402

PNG = AQUI / "_png" / "_comparar"
SAIDA = AQUI / "_comparar-divisoria.html"

CSS_PAGINA = """
body{background:#2A2F38;overflow:auto;padding:34px 0 60px}
.palco{width:1600px;height:900px;position:relative;overflow:hidden;margin:0 auto 46px;
  box-shadow:0 30px 90px -40px rgba(0,0,0,.7);background:#fff}
.rot{width:1600px;margin:0 auto 12px;color:#fff;font-family:var(--mono);font-size:14px}
"""


def palco(ident: str, legenda: str, secao: str) -> str:
    secao = secao.replace('class="slide', 'class="is-active slide', 1)
    return f'<p class="rot">{legenda}</p>\n<div class="palco" id="{ident}">{secao}</div>'


def main() -> int:
    estilo = (mk.AO_VIVO / "_estilo.css").read_text(encoding="utf-8")
    ref_secao, ref_css = mk.slide_banca(7)
    clara_secao, clara_css = mk.render_div(mk.BLOCOS / "00-div-bloco.html", 2)
    escura_secao, escura_css = mk.render_div(mk.BLOCOS / "_div-bloco-escura.html", 2)
    # o congelamento e a fonte vêm do builder; os palcos são divs, não o #palco dele
    css_builder = mk.CSS_BUILDER.replace("#palco{", ".palco-x{")
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{mk.FONTES}'
            f"<style>{estilo}\n{ref_css}\n{clara_css}\n{escura_css}\n{css_builder}\n{CSS_PAGINA}</style></head><body>"
            + palco("ref", "Referência · divisória de SEÇÃO da banca (slide 7), não muda", ref_secao)
            + palco("clara", "Proposta A · divisória de BLOCO clara, número atrás do título", clara_secao)
            + palco("escura", "Proposta B · divisória de BLOCO escura, centralizada, sem gradiente", escura_secao)
            + "</body></html>")
    SAIDA.write_text(html, encoding="utf-8")
    PNG.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=mk.CHROME)
        pg = nav.new_page(viewport={"width": 1700, "height": 1000})
        pg.goto(SAIDA.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(600)
        for el in pg.query_selector_all(".palco"):
            destino = PNG / f"divisoria-{el.get_attribute('id')}.png"
            el.scroll_into_view_if_needed()
            el.screenshot(path=str(destino))
            print(f"  {destino.name}")
        nav.close()
    print(f"{SAIDA.name} escrito")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
