"""
Abre cada tela do protótipo e tira screenshots em formato 16:9
mantendo sidebar + topbar visíveis em todos os slides.

Estratégia: detecta o container scrollable (.content / .editorial), scrolla
em pedaços do tamanho do viewport e tira screenshot da viewport inteira a
cada passo. Modais são fechados antes da captura.

Uso:
    python prototipos/_screenshot_telas.py
"""
import asyncio
import shutil
import sys
from math import ceil
from pathlib import Path

from playwright.async_api import async_playwright

# Windows PowerShell usa cp1252 — forca UTF-8 no stdout
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

VIEWPORT_W = 1440
VIEWPORT_H = 810  # 16:9

BASE = Path(__file__).parent
TELAS_DIR = BASE / "telas"
OUT_DIR = BASE / "screenshots"

TELAS_ORDEM = [
    "dashboard.html",
    "previsao.html",
    "cascata.html",
    "saude-produto.html",
    "morning-brief.html",
]

# JS que fecha modais comuns sem afetar layout principal
JS_CLOSE_MODALS = """() => {
  document.querySelectorAll('.mb-backdrop, .modal-bd, .mb-modal, .modal').forEach(el => {
    el.classList.remove('on', 'open');
    el.style.display = 'none';
    el.style.pointerEvents = 'none';
  });
}"""

# detecta o container interno que rola (não o body)
JS_DETECT_SCROLLABLE = """() => {
  const candidates = ['.content', '.editorial', '.main'];
  for (const sel of candidates) {
    const el = document.querySelector(sel);
    if (el && el.scrollHeight > el.clientHeight + 5) return sel;
  }
  return null;
}"""


async def capture_one(page, html_path: Path) -> dict:
    url = html_path.as_uri()
    await page.goto(url, wait_until="networkidle")

    # fecha modais que abrem por default
    await page.evaluate(JS_CLOSE_MODALS)

    # espera animacoes fadeUp / cascade
    await page.wait_for_timeout(1500)

    # detecta container scrollable
    scrollable_sel = await page.evaluate(JS_DETECT_SCROLLABLE)

    if scrollable_sel:
        scroll_h = await page.evaluate(
            f"document.querySelector({scrollable_sel!r}).scrollHeight"
        )
        client_h = await page.evaluate(
            f"document.querySelector({scrollable_sel!r}).clientHeight"
        )
    else:
        scroll_h = await page.evaluate("document.documentElement.scrollHeight")
        client_h = VIEWPORT_H

    # cada slide = altura visivel do container
    num_prints = max(1, ceil(scroll_h / client_h))

    stem = html_path.stem
    out = OUT_DIR / stem
    out.mkdir(parents=True, exist_ok=True)

    pieces = []
    for i in range(num_prints):
        top = i * client_h
        if scrollable_sel:
            await page.evaluate(
                f"document.querySelector({scrollable_sel!r}).scrollTop = {top}"
            )
        else:
            await page.evaluate(f"window.scrollTo(0, {top})")

        # tempo curto pra render
        await page.wait_for_timeout(350)

        slide_path = out / f"{stem}-slide{i+1:02d}.png"
        await page.screenshot(path=str(slide_path), full_page=False)
        pieces.append(slide_path.name)

    return {
        "file": html_path.name,
        "scroll": scroll_h,
        "client": client_h,
        "scrollable": scrollable_sel or "(body)",
        "num_prints": num_prints,
        "pieces": pieces,
    }


async def main():
    # limpa screenshots anteriores
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Capturando em {VIEWPORT_W}x{VIEWPORT_H}\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            device_scale_factor=1.5,  # mais nítido pro PPT
        )
        page = await ctx.new_page()

        results = []
        for fname in TELAS_ORDEM:
            f = TELAS_DIR / fname
            if not f.exists():
                print(f"  [skip] {fname} nao existe")
                continue
            try:
                r = await capture_one(page, f)
                print(
                    f"  [OK] {r['file']:22s}  scroll {r['scroll']:5d}px / vp {r['client']:4d}px  "
                    f"({r['scrollable']:>10s})  ->  {r['num_prints']} slide(s)"
                )
                results.append(r)
            except Exception as e:
                print(f"  [ERR] {fname}: {e}")

        await browser.close()

    print("\n" + "=" * 76)
    print(f"{'Tela':<24} {'Scroll':>8} {'Viewport':>9} {'Slides':>7}")
    print("-" * 76)
    total = 0
    for r in results:
        print(f"{r['file']:<24} {r['scroll']:>6}px {r['client']:>7}px {r['num_prints']:>7}")
        total += r["num_prints"]
    print("-" * 76)
    print(f"{'TOTAL':<24} {' ':>8} {' ':>9} {total:>7}")
    print("=" * 76)
    print(f"\nScreenshots em: {OUT_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
