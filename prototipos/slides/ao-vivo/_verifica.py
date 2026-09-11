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
# A capa e o slide das quebras respiram de propósito: neles o branco é a
# composição, não defeito. Dez segundos num slide limpo valem mais que um
# minuto num amontoado, e esses dois valem dez segundos.
# Slides em que o branco é a composição, e não defeito. As sete divisórias
# entraram em 10/09/2026, quando o rodapé delas saiu: um divisor é uma pausa, e
# medir vão no pé de uma pausa é medir a pausa. Junto vieram os que ficaram
# esparsos ao perder texto no mesmo dia (5, 13, 26, 27).
SEM_AVISO_DE_VAO = (1, 2, 3, 5, 6, 7, 11, 12, 13, 15, 16, 19, 21, 22, 24, 25, 26, 27)

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
    const dentroDoCorpo = corpo.contains(el);

    if (r.width > 0 && r.height > 0) {
      if (r.left < -1 || r.right > 1601 || r.top < -1 || r.bottom > 901)
        achados.push('FORA DO PALCO ' + tag + '.' + c.slice(0, 24));
      /* conteudo empurrado para fora do CORPO do slide: acontece quando um flex
         em coluna nao cabe e o overflow do palco esconde o excedente. Um bloco
         inteiro desaparece da tela sem sair dos 1600x900, e a checagem de palco
         nao pega. Foi assim que a faixa de fatos de um slide sumiu. */
      if (dentroDoCorpo && (r.bottom > cr.bottom + 2 || r.top < cr.top - 2))
        achados.push('FORA DO CORPO ' + tag + '.' + c.slice(0, 24) +
          ' (passa ' + Math.round(Math.max(r.bottom - cr.bottom, cr.top - r.top)) + 'px)');
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
    problemas: list[str] = []

    # ── conferência estática antes de abrir o navegador ──
    # tag desbalanceada o navegador tolera calado, e o print sai quase certo:
    # é o defeito que passa pela revisão visual. Um <span> a mais já custou um
    # bug nesta sessão.
    for sec in re.findall(r'<section class="slide.*?</section>', html, re.S):
        m = re.search(r'data-slide="(\d+)" data-var="([^"]+)"', sec)
        tag_id = f"{m.group(1)}{m.group(2)}" if m else "?"
        for tag in ("span", "div", "p"):
            abre = len(re.findall(r"<" + tag + r"[\s>]", sec))
            fecha = len(re.findall(rf"</{tag}>", sec))
            if abre != fecha:
                problemas.append(
                    f"{tag_id}: <{tag}> desbalanceado, {abre} abre e {fecha} fecha")
                print(f"  {tag_id}: <{tag}> DESBALANCEADO, {abre} abre / {fecha} fecha")

    PNG.mkdir(exist_ok=True)
    tags: list[str] = []
    falhas: list[str] = []

    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": 1600, "height": 900})
        pg.on("requestfailed", lambda r: falhas.append(r.url.split("/")[-1]))
        pg.goto(DECK.resolve().as_uri())
        pg.wait_for_timeout(1200)
        pg.keyboard.press("h")

        for n in alvos:
            for i, _ in enumerate(sorted(mapa[n])):
                # pelo gancho, e não por tecla: a navegação por número do
                # visualizador cobre só 1 a 9 e o deck passou de nove slides
                pg.evaluate(f"() => window.cronosIr({n}, {i})")
                pg.wait_for_timeout(ASSENTA_MS)
                tag = pg.evaluate(
                    "() => { const a = document.querySelector('.slide.is-active');"
                    " return a.getAttribute('data-slide') + a.getAttribute('data-var'); }"
                )
                pg.screenshot(path=str(PNG / f"{tag}.png"))
                tags.append(tag)
                m = pg.evaluate(MEDIDA)
                aviso = ""
                if m["vaoMeio"] > VAO_LIMITE and n not in SEM_AVISO_DE_VAO:
                    aviso += f"  << VAO INTERNO DE {m['vaoMeio']}px em y={m['ondeVao']}"
                    problemas.append(
                        f"{tag}: vão interno de {m['vaoMeio']}px em y={m['ondeVao']}")
                if m["vaoPe"] > VAO_LIMITE and n not in SEM_AVISO_DE_VAO:
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
    for x in problemas:
        print(f"    - {x}")

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
