# -*- coding: utf-8 -*-
"""Verifica o deck da banca: captura, mede e monta a folha de contato.

O laço padrão de conferência. Roda depois de cada lote de slides.

O que ele mede, e o motivo de cada medida:

  vão morto        A distância entre o fim do conteúdo e o pé do corpo do
                   slide. É o defeito mais comum deste deck e o mais difícil
                   de ver em miniatura. Acima de 70px vira aviso.
  fora do palco    Elemento com parte fora de 1600x900. O .mesh e o .grid-bg
                   ficam de fora da conta: eles são a textura de fundo e
                   escalam 1,06 por desenho.
  invisível        Elemento que terminou a cascata com opacity 0, ou seja,
                   nunca apareceu. Costuma ser animação que não disparou.
  dimensão zero    Largura ou altura zero em elemento que deveria ter tamanho.
                   Barra com altura em porcentagem cai aqui.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_verifica.py          (tudo)
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_verifica.py 1 2 3    (só estes)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
DECK = AQUI / "deck.html"
PNG = AQUI / "_png"
CHROME = (
    r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
    r"\chromium-1217\chrome-win64\chrome.exe"
)
ASSENTA_MS = 4200
VAO_LIMITE = 70

MEDIDA = r"""() => {
  const a = document.querySelector('.slide.is-active');
  const corpo = a.querySelector('.body');
  const cr = corpo.getBoundingClientRect();
  const achados = [];
  let baixo = -Infinity, alto = Infinity;
  const bandas = [];

  /* mede a TINTA, nao a caixa: contêiner com flex:1 estica para o corpo inteiro
     e faria todo slide parecer perfeitamente preenchido. Tinta e elemento com
     texto proprio, imagem, ou caixa pintada pequena o bastante para nao ser
     contêiner (barra, quadradinho, fio). */
  const temTextoProprio = el => [...el.childNodes].some(
    n => n.nodeType === 3 && n.textContent.trim().length > 0);

  a.querySelectorAll('*').forEach(el => {
    const c = el.className.toString();
    if (/\b(mesh|grid-bg)\b/.test(c)) return;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const tag = el.tagName.toLowerCase();

    if (r.width > 0 && r.height > 0) {
      if (r.left < -1 || r.right > 1601 || r.top < -1 || r.bottom > 901)
        achados.push('FORA ' + tag + '.' + c.slice(0, 24));
    }
    if (parseFloat(cs.opacity) === 0 && r.width > 2)
      achados.push('INVISIVEL ' + tag + '.' + c.slice(0, 24));
    if (el.children.length === 0 && el.textContent.trim() &&
        (r.width < 1 || r.height < 1))
      achados.push('ZERO ' + tag + '.' + c.slice(0, 24));

    if (!corpo.contains(el) || r.width < 1 || r.height < 1) return;
    const pintado = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' ||
                    cs.borderTopWidth !== '0px';
    const eTinta = temTextoProprio(el) || tag === 'img' || tag === 'svg' ||
                   (pintado && r.height < cr.height * 0.85);
    if (eTinta) {
      baixo = Math.max(baixo, r.bottom);
      alto = Math.min(alto, r.top);
      bandas.push([r.top, r.bottom]);
    }
  });

  /* o vao INTERNO: junta as faixas de tinta em bandas e mede o maior buraco
     entre elas. Medir so o pe deixava passar slide com 300px de branco no meio,
     que foi exatamente o defeito que o dono do projeto viu antes da medicao. */
  bandas.sort((x, y) => x[0] - y[0]);
  const juntas = [];
  for (const [t0, t1] of bandas) {
    if (juntas.length && t0 <= juntas[juntas.length - 1][1] + 1)
      juntas[juntas.length - 1][1] = Math.max(juntas[juntas.length - 1][1], t1);
    else juntas.push([t0, t1]);
  }
  let maiorVao = 0, ondeVao = 0;
  for (let i = 1; i < juntas.length; i++) {
    const g = juntas[i][0] - juntas[i - 1][1];
    if (g > maiorVao) { maiorVao = g; ondeVao = Math.round(juntas[i - 1][1]); }
  }

  return {
    achados: achados.slice(0, 6),
    vaoTopo: Math.round(alto - cr.top),
    vaoPe: Math.round(cr.bottom - baixo),
    vaoMeio: Math.round(maiorVao),
    ondeVao: ondeVao,
    corpo: Math.round(cr.height),
    conteudo: Math.round(baixo - alto),
  };
}"""


def main() -> int:
    quais = [int(a) for a in sys.argv[1:] if a.isdigit()]
    html = DECK.read_text(encoding="utf-8")
    mapa: dict[int, list[str]] = {}
    for s, v in re.findall(r'data-slide="(\d+)" data-var="([^"]+)"', html):
        mapa.setdefault(int(s), []).append(v)
    alvos = sorted(n for n in mapa if not quais or n in quais)
    if not alvos:
        print("nenhum slide para verificar")
        return 1

    PNG.mkdir(exist_ok=True)
    tags: list[str] = []
    problemas: list[str] = []
    falhas: list[str] = []

    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": 1600, "height": 900})
        pg.on("requestfailed", lambda r: falhas.append(r.url.split("/")[-1]))
        pg.goto(DECK.resolve().as_uri())
        pg.wait_for_timeout(1200)
        pg.keyboard.press("h")

        for n in alvos:
            pg.keyboard.press(str(n))
            pg.wait_for_timeout(220)
            for i, _ in enumerate(sorted(mapa[n])):
                if i:
                    pg.keyboard.press("ArrowDown")
                pg.wait_for_timeout(ASSENTA_MS)
                tag = pg.evaluate(
                    "() => { const a = document.querySelector('.slide.is-active');"
                    " return a.getAttribute('data-slide') + a.getAttribute('data-var'); }"
                )
                pg.screenshot(path=str(PNG / f"{tag}.png"))
                tags.append(tag)
                m = pg.evaluate(MEDIDA)
                aviso = ""
                if m["vaoMeio"] > VAO_LIMITE and n != 1:
                    aviso += f"  << VAO INTERNO DE {m['vaoMeio']}px em y={m['ondeVao']}"
                    problemas.append(
                        f"{tag}: vão interno de {m['vaoMeio']}px em y={m['ondeVao']}")
                if m["vaoPe"] > VAO_LIMITE and n != 1:
                    aviso += f"  << VAO DE {m['vaoPe']}px NO PE"
                    problemas.append(f"{tag}: vão de {m['vaoPe']}px no pé do corpo")
                for x in m["achados"]:
                    problemas.append(f"{tag}: {x}")
                print(
                    f"  {tag}  corpo {m['corpo']}px  conteudo {m['conteudo']}px  "
                    f"topo {m['vaoTopo']}px  meio {m['vaoMeio']}px  "
                    f"pe {m['vaoPe']}px{aviso}"
                )
                for x in m["achados"]:
                    print(f"        {x}")
        nav.close()

    print(f"\nrecursos faltando: {sorted(set(falhas)) or 'nenhum'}")
    print(f"problemas: {len(problemas)}")

    largura, altura, rotulo, colunas = 700, 394, 24, 2
    linhas = (len(tags) + colunas - 1) // colunas
    folha = Image.new("RGB", (colunas * largura, linhas * (altura + rotulo)), "#1B1F26")
    d = ImageDraw.Draw(folha)
    for i, tag in enumerate(tags):
        im = Image.open(PNG / f"{tag}.png").convert("RGB")
        im = im.resize((largura - 8, altura - 8), Image.LANCZOS)
        x, y = (i % colunas) * largura, (i // colunas) * (altura + rotulo)
        folha.paste(im, (x + 4, y + rotulo + 4))
        d.text((x + 8, y + 6), f"slide {tag}", fill="#8FE3B0")
    nome = f"lote-{'-'.join(map(str, alvos))}.png" if quais else "folha-completa.png"
    folha.save(PNG / nome)
    print(f"folha: _png/{nome}  {folha.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
