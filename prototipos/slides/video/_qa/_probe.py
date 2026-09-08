"""Sondagens pontuais: pixel do fantasma no slide 1, coreografia fina do slide 2,
alinhamento do rodape dos dois cartoes e fonte do sinal de menos.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME = Path(
    r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
    r"\chromium-1217\chrome-win64\chrome.exe"
)
AQUI = Path(__file__).parent
DECK = Path(r"C:/Users/IGOR~1.VIG/AppData/Local/Temp/claude/C--Users-igor-vignola-Documents-Personal-FIAP-Challenge-LocaWeb/c74e1992-556b-4c8e-a196-16a1cfd7787a/scratchpad") / "deck.html"

EXTRA_S2 = [700, 1300, 2200, 2300, 2450, 2530, 2700, 2900, 3100, 4200, 6500]

DETALHE = r"""
() => {
  window.requestAnimationFrame = function(){ return 0; };
  document.getAnimations().forEach(a => { try{ a.pause(); }catch(e){} });
  const stage = document.getElementById('stage');
  const sr = stage.getBoundingClientRect();
  const rel = el => { const r = el.getBoundingClientRect();
    return { x:+(r.left-sr.left).toFixed(1), y:+(r.top-sr.top).toFixed(1),
             w:+r.width.toFixed(1), h:+r.height.toFixed(1) }; };
  const slide = document.querySelector('.slide.is-active');
  const o = { slide: slide.id, cols: [] };
  slide.querySelectorAll('.col').forEach((col, ci) => {
    const cost = col.querySelector('.cost');
    const b = cost.querySelector('b');
    const span = cost.querySelector('span');
    const cs = getComputedStyle(cost);
    const dado = { i:ci,
      costRect: rel(cost), borderTopY: rel(cost).y, borderTop: cs.borderTopWidth,
      bRect: rel(b), bTxt: b.textContent.trim(), bLineH: getComputedStyle(b).lineHeight,
      spanRect: rel(span), spanTxt: span.textContent.replace(/\s+/g,' ').trim(),
      barras: [], };
    col.querySelectorAll('.stp').forEach((stp,k) => {
      const bar = stp.querySelector('.bar');
      const cb = getComputedStyle(bar);
      dado.barras.push({ k, cls: stp.className, rot: bar.textContent.trim(),
        bg: cb.backgroundColor, fg: cb.color,
        scaleY: +(bar.getBoundingClientRect().height / bar.offsetHeight).toFixed(3) });
    });
    const pin = col.querySelector('.pin');
    if(pin){
      const rp = rel(pin);
      const centros = [].slice.call(col.querySelectorAll('.stp')).map(s => {
        const r = rel(s); return +(r.x + r.w/2).toFixed(1); });
      const c = rp.x + rp.w/2;
      let melhor=-1, dist=1e9;
      centros.forEach((cx,k)=>{ const dd=Math.abs(cx-c); if(dd<dist){dist=dd;melhor=k;} });
      const b1 = pin.querySelector('.b1'), b2 = pin.querySelector('.b2');
      dado.pin = { op: getComputedStyle(pin).opacity, centro:+c.toFixed(1),
        col: melhor, dist:+dist.toFixed(1), centros,
        pillRect: rel(pin.querySelector('b')),
        b1: b1 ? { op:getComputedStyle(b1).opacity, rect:rel(b1) } : null,
        b2: b2 ? { op:getComputedStyle(b2).opacity, rect:rel(b2) } : null };
    }
    o.cols.push(dado);
  });
  return o;
}
"""

FANTASMA = r"""
() => {
  window.requestAnimationFrame = function(){ return 0; };
  document.getAnimations().forEach(a => { try{ a.pause(); }catch(e){} });
  const t = document.querySelector('.cp .tag2');
  const cs = getComputedStyle(t);
  const r = t.getBoundingClientRect();
  const anims = t.getAnimations().map(a => ({ n:a.animationName, t:a.currentTime,
      fase: a.effect.getComputedTiming().progress, estado:a.playState,
      delay:a.effect.getComputedTiming().delay }));
  return { opacity: cs.opacity, transform: cs.transform, color: cs.color,
           willChange: cs.willChange, rect:{x:r.x,y:r.y,w:r.width,h:r.height},
           anims,
           wordScroll: document.querySelector('.cp .word').scrollWidth,
           wordClient: document.querySelector('.cp .word').clientWidth };
}
"""


def main() -> None:
    url = DECK.as_uri()
    saida = {}
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=str(CHROME))
        pg = nav.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
        pg.goto(url)
        pg.wait_for_timeout(2500)

        # 1) fantasma do tag2 no slide 1
        for t in (700, 900, 950):
            pg.reload(); pg.wait_for_timeout(900)
            pg.keyboard.press("h"); pg.keyboard.press("1"); pg.keyboard.press("r")
            pg.wait_for_timeout(t)
            saida[f"fantasma_{t}"] = pg.evaluate(FANTASMA)
            pg.screenshot(path=str(AQUI / f"probe_s1_{t:04d}ms.png"),
                          clip={"x": 430, "y": 500, "width": 740, "height": 140})

        # 2) coreografia fina do slide 2
        for t in EXTRA_S2:
            pg.reload(); pg.wait_for_timeout(900)
            pg.keyboard.press("h"); pg.keyboard.press("2"); pg.keyboard.press("r")
            pg.wait_for_timeout(t)
            saida[f"s2_{t}"] = pg.evaluate(DETALHE)
            pg.screenshot(path=str(AQUI / f"s2_{t:04d}ms.png"))
        nav.close()
    (AQUI / "probe.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
