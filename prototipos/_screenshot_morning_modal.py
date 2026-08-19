"""
Captura o dashboard.html com o modal do Morning Brief ABERTO (overlay sobre o dash).
Salva em prototipos/screenshots/morning-brief/morning-brief-modal.png
"""
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE = Path(__file__).parent
DASH = BASE / "telas" / "dashboard.html"
OUT = BASE / "screenshots" / "morning-brief" / "morning-brief-modal.png"

W, H = 1440, 810

JS_OPEN_MODAL = """() => {
  const bd = document.getElementById('mbBackdrop');
  const md = document.getElementById('mbModal');
  if (bd) bd.classList.add('open');
  if (md) md.classList.add('open');
}"""


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": W, "height": H},
            device_scale_factor=2.0,
        )
        page = await ctx.new_page()
        await page.goto(DASH.as_uri(), wait_until="networkidle")
        await page.wait_for_timeout(1200)  # animações de entrada
        await page.evaluate(JS_OPEN_MODAL)
        await page.wait_for_timeout(500)   # animação do modal
        await page.screenshot(path=str(OUT), full_page=False)
        await browser.close()
    print(f"[OK] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
