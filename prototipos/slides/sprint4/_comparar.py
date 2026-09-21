# -*- coding: utf-8 -*-
"""Duas comparações para decidir a forma do pptx da Sprint 4.

Usa slides REAIS do deck da banca como tela, com a animação congelada no estado
final, para a decisão ser tomada sobre o que vai ao arquivo e não sobre um
exemplo inventado. Mesmo molde do ao-vivo/_comparar_marcador.py.

  _comparar-blocos.html   como avisar em qual bloco do template cada slide está
      A  rótulo "Bloco 2 · Compreendendo o desafio" no rodapé, à direita,
         no lugar que o marcador de quem apresenta libera. Nenhum slide a mais.
      B  uma divisória escura nova abrindo o bloco, no desenho .dv2 da banca,
         e os slides seguem limpos.

  _comparar-telas.html    o slide de captura da aplicação, em dois visuais
      A  o layout da Sprint 3 que está no rascunho: moldura de navegador,
         coluna de texto à esquerda (PNG já renderizado)
      B  o mesmo conteúdo no visual da banca: cabeçalho e título da casa, o
         print num cartão plano, "quem usa" e "no dia a dia" à esquerda

Uso:
    .venv/Scripts/python.exe prototipos/slides/sprint4/_comparar.py
"""
from __future__ import annotations

import re
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
AO_VIVO = AQUI.parent / "ao-vivo"
PNG = AQUI / "_png" / "_comparar"
CHROME = (r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
          r"\chromium-1217\chrome-win64\chrome.exe")

FONTES = ('<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600'
          '&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')

LOGO_CLARO = ('<svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" '
              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" '
              'r="3" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg>')
LOGO_ESCURO = LOGO_CLARO.replace('stroke="#fff"', 'stroke="#0A0E17"').replace("#3B82F6", "#2563EB")

RE_STYLE = re.compile(r"<style>(.*?)</style>", re.S)
RE_SECTION = re.compile(r'(<section class="slide.*?</section>)', re.S)


# ── utilidades herdadas do comparador do marcador ────────────────────────────
def resolve_contadores(texto: str) -> str:
    """Escreve o valor final onde o contador espera o JS."""
    def valor(m: re.Match) -> str:
        alvo = m.group(2)
        dec = re.search(r'data-dec="(\d+)"', m.group(1))
        if dec and int(dec.group(1)) > 0:
            v = f"{float(alvo.replace(',', '.')):.{int(dec.group(1))}f}".replace(".", ",")
        else:
            v = f"{int(float(alvo.replace(',', '.'))):,}".replace(",", ".")
        return m.group(1) + v + m.group(3)
    return re.sub(r'(<span class="ct"[^>]*data-to="([^"]+)"[^>]*>)[^<]*(</span>)', valor, texto)


def bloco(nome: str) -> tuple[str, str]:
    """CSS e a primeira <section> (composição A) de um bloco da banca."""
    t = (AO_VIVO / "blocos" / nome).read_text(encoding="utf-8")
    css = "\n".join(c.strip() for c in RE_STYLE.findall(t))
    secao = RE_SECTION.findall(t)[0]
    secao = resolve_contadores(secao)
    # os blocos moram em ao-vivo/blocos/; esta página mora em sprint4/. Um ../
    # a menos leva ao mesmo lugar: ../figs -> ../ao-vivo/figs, ../../../../ -> ../../../
    secao = secao.replace('src="../../../../', 'src="../../../').replace('src="../figs/', 'src="../ao-vivo/figs/')
    css = css.replace("url(../figs/", "url(../ao-vivo/figs/")
    secao = secao.replace('class="slide', 'class="is-active slide', 1)
    return css, secao


def com_rotulo_no_rodape(secao: str, rotulo: str) -> str:
    """Forma A: o rótulo do bloco entra no rodapé, à direita, onde ficava o marcador."""
    numero, nome = rotulo.split(" · ", 1)
    span = f'<span class="rotb"><b>{numero}</b> · {nome}</span>'
    return re.sub(r'(<div class="ft">)(.*?)(</div>)', r"\1\2" + span + r"\3", secao, count=1, flags=re.S)


CSS_PAGINA = """
/* a página de comparação, não o slide */
body{background:#2A2F38;overflow:auto;padding:34px 0 60px}
.palco{width:1600px;height:900px;position:relative;overflow:hidden;margin:0 auto 46px;
  box-shadow:0 30px 90px -40px rgba(0,0,0,.7);background:#fff}
.palco .stage{position:absolute;inset:0}
.palco img.pronto{display:block;width:1600px;height:900px}
.rot{width:1600px;margin:0 auto 12px;color:#fff;font-family:var(--mono);font-size:14px;
  letter-spacing:.3px}
.sec{width:1600px;margin:70px auto 26px;color:#fff;font-family:var(--font);font-size:30px;
  font-weight:800;letter-spacing:-.8px;padding-top:26px;border-top:1px solid rgba(255,255,255,.18)}
.sec small{display:block;font-size:16px;font-weight:400;color:rgba(255,255,255,.62);margin-top:6px;
  letter-spacing:0;line-height:1.45;max-width:1100px}
.slide{animation:none !important}
/* o .mesh fica de fora do congelamento: travado no fim da deriva ele desenha um
   retângulo claro no meio do slide, que não existe na peça real */
.mesh{animation:none !important;transform:none !important}
.is-active *:not(.mesh){animation-duration:.01ms !important;animation-delay:0ms !important}

/* ══ forma A · o rótulo do bloco no rodapé ══ */
.rotb{margin-left:auto;order:9;display:inline-flex;align-items:center;gap:8px}
.rotb b{font-weight:800}
.light .rotb{color:#68737F} .light .rotb b{color:var(--accent)}
.dark .rotb{color:#A6B0BD} .dark .rotb b{color:#93C5FD}
"""


def pagina(titulo: str, css: str, partes: list[str], saida: Path) -> None:
    estilo = (AO_VIVO / "_estilo.css").read_text(encoding="utf-8")
    html = (f'<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">\n'
            f"<title>{titulo}</title>\n{FONTES}\n<style>\n{estilo}\n{css}\n{CSS_PAGINA}\n</style></head>"
            f"<body>\n{chr(10).join(partes)}\n</body></html>\n")
    saida.write_text(html, encoding="utf-8")
    print(f"{saida.name} escrito, {len(html) // 1024} KB")


def palco(ident: str, legenda: str, conteudo: str) -> str:
    return (f'<p class="rot">{legenda}</p>\n'
            f'<div class="palco" id="{ident}"><div class="stage">{conteudo}</div></div>')


# ── comparação 1 · os blocos do template ─────────────────────────────────────
ROTULO = "Bloco 2 · Compreendendo o desafio"

DIVISORIA_BLOCO = f"""
<section class="is-active slide dark dv3 dv2" data-slide="0" data-var="a">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="hd">
    <div class="bi">{LOGO_ESCURO}</div>
    <div class="bn">Cronos</div>
    <div class="tag">Bloco 2 &middot; Template FIAP</div>
  </div>
  <div class="body">
    <div class="lft">
      <div class="bl" style="--d:200ms"><b>Bloco 02</b> &middot; de sete</div>
      <h1 class="tt">
        <span class="mask" style="--d:420ms"><span>Compreendendo</span></span>
        <span class="mask" style="--d:520ms"><span>o desafio</span></span>
      </h1>
      <p class="lead rv" style="--d:860ms">O cenário em que o problema acontece, o problema nomeado, o efeito que ele produz no indicador e por que a hora de resolver é agora.</p>
    </div>
    <div class="pv rv3" style="--d:900ms">
      <div class="pvh"><span class="dot"></span>O que este bloco responde</div>
      <div class="pvgrid">
        <div class="pc rv" style="--d:1160ms">
          <div class="pl">Prazo de OLA</div>
          <div class="pn">4 h <span class="u">P2</span> &middot; 12 h <span class="u">P3</span></div>
          <div class="ps">tempo de resolução por prioridade</div>
        </div>
        <div class="pc rv" style="--d:1280ms">
          <div class="pl">Base do indicador</div>
          <div class="pn">25.600</div>
          <div class="ps">elegíveis ao KPI, 2023 a 2025</div>
        </div>
        <div class="pc wide rv" style="--d:1400ms">
          <div class="pl">Violações em 2025, contra o limite do ano</div>
          <div class="pn">42 <span class="u">de 39 no P2</span> &nbsp;&middot;&nbsp; 196 <span class="u">de 263 no P3</span></div>
          <div class="ps">o P2 passou o limite em novembro, e a leitura só chegou na apuração de dezembro</div>
        </div>
      </div>
    </div>
  </div>
  <div class="ft"></div>
</section>
"""


def comparar_blocos() -> None:
    css_todos, partes = [], []
    secoes = {}
    for nome in ("04-medida.html", "05-quebras.html", "06-antecipar.html"):
        css, secao = bloco(nome)
        css_todos.append(css)
        secoes[nome] = secao

    partes.append('<div class="sec">Forma A · o rótulo do bloco no rodapé'
                  "<small>Nenhum slide a mais. No canto inferior direito, onde ficava a foto de quem "
                  "apresenta, entra o número e o nome do bloco do template. As sete divisórias da banca "
                  "continuam como estão.</small></div>")
    for i, nome in enumerate(secoes, 4):
        partes.append(palco(f"a{i}", f"A · slide {i} da banca, com o rótulo no rodapé",
                            com_rotulo_no_rodape(secoes[nome], ROTULO)))

    partes.append('<div class="sec">Forma B · uma divisória escura por bloco do template'
                  "<small>Sete slides novos no desenho das divisórias da banca, um antes de cada bloco. "
                  "Os slides seguem sem rótulo nenhum. Somadas às sete divisórias que a banca já tem, "
                  "ficam catorze em cerca de 55 slides.</small></div>")
    partes.append(palco("b0", "B · divisória nova, abre o bloco 2", DIVISORIA_BLOCO))
    for i, nome in enumerate(secoes, 4):
        partes.append(palco(f"b{i}", f"B · slide {i} da banca, limpo", secoes[nome]))

    pagina("Sprint 4 · como marcar os blocos do template", "\n".join(css_todos), partes,
           AQUI / "_comparar-blocos.html")


# ── comparação 2 · o slide de captura da aplicação ───────────────────────────
CSS_TELA_B = """
/* ══ forma B · captura da aplicação no visual da banca ══ */
.tlb .body{padding-top:14px}
.tlb .tt{font-size:52px;letter-spacing:-1.9px}
.tlb .cena{flex:1;display:flex;align-items:stretch;gap:44px;margin-top:18px;min-height:0}
.tlb .lado{width:392px;flex-shrink:0;display:flex;flex-direction:column}
.tlb .lado .leg{font-size:17px;line-height:1.5;color:var(--tx)}
.tlb .lado .leg b{color:var(--head);font-weight:700}
.tlb .itens{margin-top:22px}
.tlb .it{display:flex;gap:16px;padding:20px 0}
.tlb .it + .it{border-top:1px solid #DCE4EF}
.tlb .it .n{font-family:var(--mono);font-size:12.5px;color:var(--accent);padding-top:4px;flex-shrink:0}
.tlb .it b{display:block;font-size:12.5px;font-weight:700;letter-spacing:2.2px;text-transform:uppercase;
  color:var(--accent)}
.tlb .it span{display:block;font-size:15.5px;line-height:1.45;color:var(--tx);margin-top:8px}
.tlb .it span em{font-style:normal;color:var(--head);font-weight:700}
.tlb .pos{margin-top:auto;display:inline-flex;align-self:flex-start;font-size:12.5px;font-weight:600;
  color:var(--accent);background:#fff;border:1px solid var(--line);border-radius:999px;padding:7px 15px;
  box-shadow:0 4px 14px -8px rgba(37,99,235,.3)}
/* o print, plano, num cartão da casa. Teto em px: a imagem é 3200x2000 e a
   altura do corpo não é conhecida por ela. */
.tlb .palco2{flex:1;min-width:0;display:flex;align-items:center;justify-content:flex-end}
.tlb .tela{border-radius:14px;overflow:hidden;border:1px solid #D6DEE9;background:#fff;
  box-shadow:0 40px 90px -44px rgba(15,23,42,.5),0 0 0 1px rgba(15,23,42,.03)}
.tlb .tela img{display:block;height:612px;width:auto}
"""

TELA_B = f"""
<section class="is-active slide light tlb" data-slide="0" data-var="a">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="hd">
    <div class="bi">{LOGO_CLARO}</div>
    <div class="bn">Cronos</div>
    <div class="tag">Aba Panorama &middot; captura 1 de 10</div>
  </div>
  <div class="body">
    <span class="eb"><span class="rv" style="--d:240ms">A aplicação</span></span>
    <h1 class="tt"><span class="mask" style="--d:340ms"><span>O dia em uma tela</span></span></h1>
    <div class="cena">
      <div class="lado">
        <p class="leg rv" style="--d:700ms">O previsto para a hora contra o registrado, em <b>P3 e P2</b>. Abaixo, os casos de maior risco agora e as duas metas do ano.</p>
        <div class="itens">
          <div class="it rv" style="--d:1000ms">
            <span class="n">01</span>
            <div><b>Quem usa</b><span>A coordenação de operações, na primeira meia hora do dia.</span></div>
          </div>
          <div class="it rv" style="--d:1140ms">
            <span class="n">02</span>
            <div><b>No dia a dia</b><span>Compara o que já entrou com o que o modelo esperava para a hora e decide se o dia pede reforço. <em>É a única tela que responde as duas perguntas juntas.</em></span></div>
          </div>
        </div>
        <span class="pos rv" style="--d:1300ms">igor-vignola.github.io/LocaWeb-Cronos</span>
      </div>
      <div class="palco2">
        <div class="tela rv3" style="--d:800ms"><img src="../../../sprints/sprint-3/prints/01-panorama.png" alt="Aba Panorama do painel operacional do Cronos"></div>
      </div>
    </div>
  </div>
  <div class="ft"><span>Captura da aplicação &middot; relógio do sistema em 01/10/2025, 15h</span></div>
</section>
"""


def comparar_telas() -> None:
    partes = [
        '<div class="sec">Forma A · o layout da Sprint 3, como está no rascunho'
        "<small>Coluna de texto à esquerda, o print dentro de uma janela de navegador desenhada, "
        "com abas e barra de endereço. Dez slides assim já existem, um por tela e um por folha de "
        "detalhe.</small></div>",
        palco("ta", "A · slide 26 do rascunho, sem mudança",
              '<img class="pronto" src="_png/26-tela-01-01-panorama.png" alt="">'),
        '<div class="sec">Forma B · o mesmo conteúdo no visual da banca'
        "<small>Cabeçalho, olho e título da casa. O print entra plano, num cartão, sem a janela de "
        "navegador. Quem usa e no dia a dia ficam à esquerda, e o endereço da aplicação vira uma "
        "pílula. Dez slides para desenhar neste molde.</small></div>",
        palco("tb", "B · o Panorama no visual da banca", TELA_B),
    ]
    pagina("Sprint 4 · o slide de captura em dois visuais", CSS_TELA_B, partes,
           AQUI / "_comparar-telas.html")


# ── fotografa cada palco, para conferir antes de mostrar ─────────────────────
def fotografa() -> None:
    PNG.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=CHROME)
        pg = nav.new_page(viewport={"width": 1700, "height": 1000}, device_scale_factor=1)
        for arquivo in ("_comparar-blocos.html", "_comparar-telas.html"):
            pg.goto((AQUI / arquivo).as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(700)
            for el in pg.query_selector_all(".palco"):
                ident = el.get_attribute("id")
                destino = PNG / f"{arquivo.split('-')[1].split('.')[0]}-{ident}.png"
                el.scroll_into_view_if_needed()
                el.screenshot(path=str(destino))
                print(f"  {destino.name}")
        nav.close()


def main() -> int:
    comparar_blocos()
    comparar_telas()
    fotografa()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
