# -*- coding: utf-8 -*-
"""Renderiza slides HTML em PNG 1600x900 para conferência visual.

Aceita caminhos de arquivo ou nomes soltos dentro de uma pasta base. Reporta se o conteúdo
transborda o quadro do slide, que é o defeito mais comum e o mais difícil de ver no HTML.

Uso:
    .venv/Scripts/python scripts/renderiza_slides.py prototipos/slides/mvp/deck/d03m-r5a.html
    .venv/Scripts/python scripts/renderiza_slides.py --saida _r5 prototipos/slides/mvp/deck/*.html
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
LARGURA, ALTURA = 1600, 900


def main() -> None:
    args = sys.argv[1:]
    saida_nome = "_png"
    if "--saida" in args:
        i = args.index("--saida")
        saida_nome = args[i + 1]
        args = args[:i] + args[i + 2 :]
    if not args:
        raise SystemExit("informe ao menos um arquivo .html")

    caminhos = [Path(a) if Path(a).is_absolute() else RAIZ / a for a in args]
    faltando = [c for c in caminhos if not c.exists()]
    if faltando:
        raise SystemExit("não existe: " + ", ".join(str(c) for c in faltando))

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        nav = pw.chromium.launch(channel="chrome")
        pg = nav.new_context(
            viewport={"width": LARGURA, "height": ALTURA}, device_scale_factor=1
        ).new_page()
        erros: list[str] = []
        pg.on("pageerror", lambda e: erros.append(str(e)))
        for origem in caminhos:
            destino = origem.parent / saida_nome
            destino.mkdir(exist_ok=True)
            pg.goto(origem.resolve().as_uri(), wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(1100)
            alvo = pg.locator(".slide").first
            alvo.screenshot(path=str(destino / f"{origem.stem}.png"))
            transbordo = pg.evaluate(
                "() => {const s=document.querySelector('.slide');"
                "return [s.scrollHeight - s.clientHeight, s.scrollWidth - s.clientWidth];}"
            )
            aviso = ""
            if transbordo[0] > 1 or transbordo[1] > 1:
                aviso = f"   <-- TRANSBORDA {transbordo[0]}px na vertical, {transbordo[1]}px na horizontal"
            print(f"  {saida_nome}/{origem.stem}.png{aviso}")
        nav.close()
        for e in erros:
            print(f"  ERRO DE JAVASCRIPT: {e}")


if __name__ == "__main__":
    main()
