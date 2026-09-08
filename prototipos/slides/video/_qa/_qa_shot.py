"""QA visual do deck do video: captura cada slide em varios instantes e mede o DOM.

Uso:
    .venv/Scripts/python.exe prototipos/slides/video/_qa/_qa_shot.py

Para cada par (slide, instante) recarrega a pagina, esconde a barra de ajuda,
salta para o slide, reinicia a animacao com `r`, espera o instante, congela
todas as animacoes (Web Animations + rAF dos contadores) e so entao mede e
tira o print. Assim o PNG e a medicao descrevem o mesmo frame.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME = Path(
    r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
    r"\chromium-1217\chrome-win64\chrome.exe"
)
AQUI = Path(__file__).parent
DECK = AQUI.parent / "deck.html"
INSTANTES = [300, 900, 1600, 2600, 3400, 5000, 6500]

MEDIR = r"""
() => {
  // congela tudo antes de medir
  window.requestAnimationFrame = function(){ return 0; };
  const anims = document.getAnimations();
  const timeline = anims.map(a => ({
    nome: a.animationName || (a.effect && a.effect.getKeyframes && 'css') || '?',
    alvo: sel(a.effect && a.effect.target),
    t: a.currentTime === null ? null : Math.round(a.currentTime),
    estado: a.playState,
  }));
  anims.forEach(a => { try { a.pause(); } catch(e){} });

  function sel(el){
    if(!el) return null;
    if(el.pseudoElement) el = el.element || el;
    let s = el.tagName ? el.tagName.toLowerCase() : '?';
    if(el.id) s += '#' + el.id;
    if(el.className && typeof el.className === 'string' && el.className.trim())
      s += '.' + el.className.trim().split(/\s+/).join('.');
    return s;
  }
  function parseRGB(c){
    const m = String(c).match(/-?[\d.]+/g);
    if(!m) return null;
    return [ +m[0], +m[1], +m[2], m.length > 3 ? +m[3] : 1 ];
  }
  function lin(v){ v/=255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); }
  function lum(rgb){ return 0.2126*lin(rgb[0]) + 0.7152*lin(rgb[1]) + 0.0722*lin(rgb[2]); }
  function mistura(fg, bg){
    const a = fg[3];
    return [ fg[0]*a + bg[0]*(1-a), fg[1]*a + bg[1]*(1-a), fg[2]*a + bg[2]*(1-a), 1 ];
  }
  function fundoEfetivo(el){
    let bg = [255,255,255,1];
    const pilha = [];
    let n = el;
    while(n && n.nodeType === 1){ pilha.push(n); n = n.parentElement; }
    pilha.reverse();
    for(const x of pilha){
      const c = parseRGB(getComputedStyle(x).backgroundColor);
      if(c && c[3] > 0) bg = mistura(c, bg);
    }
    return bg;
  }
  function contraste(el){
    const cs = getComputedStyle(el);
    const fg = parseRGB(cs.color);
    if(!fg) return null;
    const bg = fundoEfetivo(el);
    const f = mistura(fg, bg);
    const L1 = lum(f), L2 = lum(bg);
    const r = (Math.max(L1,L2) + 0.05) / (Math.min(L1,L2) + 0.05);
    return { ratio: +r.toFixed(2), cor: cs.color, fundo: 'rgb(' + bg.slice(0,3).map(Math.round).join(',') + ')',
             px: parseFloat(cs.fontSize), peso: cs.fontWeight, txt: (el.textContent||'').trim().slice(0,42) };
  }

  const stage = document.getElementById('stage');
  const sr = stage.getBoundingClientRect();
  const slide = document.querySelector('.slide.is-active');
  const rel = el => { const r = el.getBoundingClientRect();
    return { x:+(r.left-sr.left).toFixed(1), y:+(r.top-sr.top).toFixed(1),
             w:+r.width.toFixed(1), h:+r.height.toFixed(1) }; };

  const out = { slide: slide.id, stage: {w:sr.width, h:sr.height}, timeline: timeline,
                zero: [], invisivel: [], fora: [], overflow: [], contraste: [], colunas: [], contadores: [] };

  const todos = [].slice.call(slide.querySelectorAll('*'));
  for(const el of todos){
    const cs = getComputedStyle(el);
    if(cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = rel(el);
    const temTexto = (el.textContent||'').trim().length > 0;
    const s = sel(el);
    // tamanho zero em elemento que deveria medir
    if((r.w < 0.5 || r.h < 0.5) && (el.offsetWidth > 0 || el.offsetHeight > 0))
      out.zero.push({ sel:s, rect:r, offw:el.offsetWidth, offh:el.offsetHeight,
                      transform:cs.transform, op:cs.opacity });
    // nunca apareceu
    if(parseFloat(cs.opacity) < 0.02 && (temTexto || el.offsetHeight > 4))
      out.invisivel.push({ sel:s, op:cs.opacity, rect:r, txt:(el.textContent||'').trim().slice(0,40) });
    // fora dos limites
    if(r.w > 0.5 && r.h > 0.5 && (r.x < -0.5 || r.y < -0.5 || r.x + r.w > 1600.5 || r.y + r.h > 900.5))
      out.fora.push({ sel:s, rect:r, txt:(el.textContent||'').trim().slice(0,40) });
    // texto transbordando
    if(el.scrollWidth - el.clientWidth > 1 && cs.overflowX !== 'visible')
      out.overflow.push({ sel:s, scrollW:el.scrollWidth, clientW:el.clientWidth,
                          txt:(el.textContent||'').trim().slice(0,40) });
  }

  // contraste dos textos relevantes
  const alvos = slide.querySelectorAll('.eb>span,.tt span span,.ch,.cs,.rng,.bar,.pin b,.cost span,.cost b,.qt,.qt small,.ft span,.hd .bt,.hd .tag,.bn,.cap,.lg span,.kt,.fk,.fv,.fs,.plabel,.ck,.cn,.big');
  const vistos = new Set();
  for(const el of alvos){
    const s = sel(el);
    if(vistos.has(s + (el.textContent||'').slice(0,10))) continue;
    vistos.add(s + (el.textContent||'').slice(0,10));
    const c = contraste(el);
    if(c) out.contraste.push(Object.assign({ sel:s }, c));
  }

  // escada: colunas, barras e chip
  slide.querySelectorAll('.col').forEach((col, ci) => {
    const dados = { i:ci, titulo: (col.querySelector('.ch')||{}).textContent,
                    qt: (col.querySelector('.qt .ct')||{}).textContent, barras: [] };
    const steps = col.querySelector('.steps');
    dados.stepsRect = rel(steps);
    dados.stepsShadow = getComputedStyle(steps).boxShadow;
    dados.stepsTransform = getComputedStyle(steps).transform;
    const stps = [].slice.call(col.querySelectorAll('.stp'));
    stps.forEach((stp, k) => {
      const bar = stp.querySelector('.bar');
      const cb = getComputedStyle(bar);
      const rb = rel(bar), rs = rel(stp);
      dados.barras.push({ k:k, cls: stp.className, rot: bar.textContent.trim(),
        faixa: (stp.querySelector('.rng')||{}).textContent,
        cssHeight: bar.style.height, offh: bar.offsetHeight,
        rectH: rb.h, rectY: rb.y, scaleY: cb.transform,
        bg: cb.backgroundColor, fg: cb.color,
        centroX: +(rs.x + rs.w/2).toFixed(1), stpW: rs.w });
    });
    const pin = col.querySelector('.pin');
    if(pin){
      const rp = rel(pin);
      const b = pin.querySelector('b');
      const rbb = rel(b);
      const centro = rp.x + rp.w/2;
      let melhor = -1, dist = 1e9;
      dados.barras.forEach((bb, k) => {
        const d = Math.abs(bb.centroX - centro);
        if(d < dist){ dist = d; melhor = k; }
      });
      const b1 = pin.querySelector('.b1'), b2 = pin.querySelector('.b2');
      dados.pin = { cls: pin.className, rect: rp, op: getComputedStyle(pin).opacity,
        transform: getComputedStyle(pin).transform,
        centro: +centro.toFixed(1), colunaMaisProxima: melhor, distanciaAoCentro: +dist.toFixed(1),
        chipRect: rbb, chipTxt: b.textContent.trim(),
        b1: b1 ? { op: getComputedStyle(b1).opacity, rect: rel(b1), txt: b1.textContent } : null,
        b2: b2 ? { op: getComputedStyle(b2).opacity, rect: rel(b2), txt: b2.textContent } : null };
      // o chip cobre a barra abaixo?
      const alvoBar = dados.barras[melhor];
      dados.pin.sobreBarraTopo = alvoBar ? +(alvoBar.rectY - (rp.y + rp.h)).toFixed(1) : null;
    }
    const cost = col.querySelector('.cost');
    if(cost) dados.cost = { rect: rel(cost), op: getComputedStyle(cost).opacity,
                            txt: cost.textContent.replace(/\s+/g,' ').trim() };
    out.colunas.push(dados);
  });

  slide.querySelectorAll('.ct,#ct3').forEach(el => {
    out.contadores.push({ sel: sel(el), txt: el.textContent, to: el.getAttribute('data-to'),
                          delay: el.getAttribute('data-delay') });
  });

  const fill = slide.querySelector('.fill');
  if(fill){
    const cf = getComputedStyle(fill);
    out.meter = { fillRect: rel(fill), trackRect: rel(slide.querySelector('.track')),
                  cssWidth: cf.width, transform: cf.transform, offw: fill.offsetWidth };
  }
  const big = slide.querySelector('.big');
  if(big){
    const sup = big.querySelector('sup'), mask = big.querySelector('.mask');
    out.big = { bigRect: rel(big), maskRect: rel(mask), supRect: rel(sup),
                supOverflowTop: +(rel(mask).y - rel(sup).y).toFixed(1),
                txt: big.textContent.trim() };
  }
  out.fontes = { outfit: document.fonts.check('800 40px Outfit'),
                 mono: document.fonts.check('400 13px "JetBrains Mono"') };
  return out;
}
"""


def main() -> None:
    AQUI.mkdir(exist_ok=True)
    url = DECK.as_uri()
    relatorio = {}
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=str(CHROME))
        pg = nav.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
        pg.goto(url)
        pg.wait_for_timeout(2500)  # fontes
        for slide in (1, 2, 3):
            for t in INSTANTES:
                pg.reload()
                pg.wait_for_timeout(900)
                pg.keyboard.press("h")
                pg.keyboard.press(str(slide))
                pg.keyboard.press("r")
                pg.wait_for_timeout(t)
                dados = pg.evaluate(MEDIR)
                nome = f"s{slide}_{t:04d}ms"
                pg.screenshot(path=str(AQUI / f"{nome}.png"))
                relatorio[nome] = dados
                print(f"{nome}: zero={len(dados['zero'])} invis={len(dados['invisivel'])} "
                      f"fora={len(dados['fora'])} overflow={len(dados['overflow'])}")
        nav.close()
    (AQUI / "medicoes.json").write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print("json ->", AQUI / "medicoes.json")


if __name__ == "__main__":
    main()
