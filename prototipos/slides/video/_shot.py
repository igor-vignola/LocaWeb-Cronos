"""Captura os slides do deck do vídeo, com a animação já assentada.

Uso:
    .venv/Scripts/python.exe prototipos/slides/video/_shot.py

O chromium que o playwright instalado espera (v1234) não baixou nesta máquina;
o 1217 já estava em disco, então aponta direto para ele.
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME = Path(
    r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
    r"\chromium-1217\chrome-win64\chrome.exe"
)
AQUI = Path(__file__).parent
SAIDA = AQUI / "_png"
ESPERA_MS = 5200  # cobre a cascata mais longa


def main() -> None:
    SAIDA.mkdir(exist_ok=True)
    url = (AQUI / "deck.html").as_uri()
    with sync_playwright() as p:
        navegador = p.chromium.launch(executable_path=str(CHROME))
        pagina = navegador.new_page(
            viewport={"width": 1600, "height": 900}, device_scale_factor=1
        )
        pagina.goto(url)
        pagina.wait_for_timeout(1800)
        pagina.keyboard.press("h")
        total = pagina.evaluate("document.querySelectorAll('.slide').length")
        for indice in range(total):
            if indice:
                pagina.keyboard.press("ArrowRight")
            pagina.wait_for_timeout(ESPERA_MS)
            destino = SAIDA / f"{indice + 1:02d}.png"
            pagina.screenshot(path=str(destino))
            print(f"slide {indice + 1} -> {destino.name}")
        navegador.close()


if __name__ == "__main__":
    main()
