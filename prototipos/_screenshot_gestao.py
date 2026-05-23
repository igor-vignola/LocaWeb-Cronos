"""Captura prints dos 3 HTMLs da secao Gestao em 1440x810 (16:9 do slide)."""
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
BASE = Path(__file__).parent / "gestao"
OUT = BASE / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)


async def main():
    files = ["intro.html", "board.html", "card.html"]
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": W, "height": H},
            device_scale_factor=2.0,
        )
        page = await ctx.new_page()
        for fname in files:
            f = BASE / fname
            await page.goto(f.as_uri(), wait_until="networkidle")
            await page.wait_for_timeout(800)
            out = OUT / f"{f.stem}.png"
            await page.screenshot(path=str(out), full_page=False)
            print(f"  [OK] {fname} -> {out.name}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
