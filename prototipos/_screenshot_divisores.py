"""
Captura screenshot dos divisores HTML em 1440x810 (proporcao 16:9 = slide PPT).
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

W, H = 1440, 810
BASE = Path(__file__).parent
DIV_DIR = BASE / "divisores"
OUT_DIR = DIV_DIR / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)


async def main():
    files = sorted(DIV_DIR.glob("*.html"))
    if not files:
        print("Nenhum HTML encontrado.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": W, "height": H},
            device_scale_factor=2.0,
        )
        page = await ctx.new_page()

        for f in files:
            await page.goto(f.as_uri(), wait_until="networkidle")
            await page.wait_for_timeout(800)
            out = OUT_DIR / f"{f.stem}.png"
            await page.screenshot(path=str(out), full_page=False)
            print(f"  [OK] {f.name} -> {out.name}")

        await browser.close()

    print(f"\nScreenshots em: {OUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
