# -*- coding: utf-8 -*-
"""Três abordagens para o slide de destaque de tela, todas sem fio puxado.

O Igor reprovou a versão com linhas ligando a anotação ao ponto da imagem: fica
poluído. Aqui estão três formas de dizer a mesma coisa usando ícone e proximidade,
aplicadas aos três destaques da aba Panorama para ele escolher uma.

    A · legendas alinhadas embaixo   imagem grande em cima; cada legenda fica na
                                     coluna do elemento que descreve, e o alinhamento
                                     faz o trabalho que a linha fazia
    B · balões com bico              balão de vidro encostado no próprio elemento,
                                     com um bico de 9px no lugar da linha
    C · passos ao lado               imagem à direita, coluna de passos à esquerda,
                                     na mesma ordem de leitura da tela

Uso:
    .venv/Scripts/python.exe prototipos/slides/sprint4/_comparar_telas.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
import monta_deck_sprint4 as mk  # noqa: E402

PNG = AQUI / "_png" / "_comparar"
SAIDA = AQUI / "_tela-{}.html"
PRINTS = "../../../sprints/sprint-3/prints"
PALCO_W = 1472

ICONES = {
    "curva": '<path d="M3 16.5c3.2 0 4.6-9 8.2-9 3.7 0 4.3 9 8.2 9"/><circle cx="19.4" cy="16.5" r="2.1"/>',
    "base": '<ellipse cx="12" cy="5.6" rx="7.4" ry="2.8"/><path d="M4.6 5.6v12.2c0 1.5 3.3 2.8 7.4 2.8s7.4-1.3 7.4-2.8V5.6"/><path d="M4.6 11.7c0 1.5 3.3 2.8 7.4 2.8s7.4-1.3 7.4-2.8"/>',
    "relogio": '<circle cx="12" cy="12" r="8.6"/><path d="M12 6.8V12l3.4 2"/>',
    "alvo": '<circle cx="12" cy="12" r="8.4"/><circle cx="12" cy="12" r="3.4"/><path d="M12 1.8v2.6M12 19.6v2.6M1.8 12h2.6M19.6 12h2.6"/>',
    "peso": '<path d="M4 20V9.5M10 20V4.5M16 20v-7M22 20V6.5"/>',
    "lista": '<path d="M4 6.5h4M4 12h4M4 17.5h4"/><path d="M11.5 6.5h8.5M11.5 12h8.5M11.5 17.5h8.5"/>',
}


def icone(nome: str, classe: str = "ic") -> str:
    return (f'<svg class="{classe}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONES[nome]}</svg>')


# ── os três destaques do Panorama ───────────────────────────────────────────
# região: recorte da imagem inteira. itens: caixa do elemento, ícone, título e fonte.
DESTAQUES = [
    dict(
        titulo="Previsto para hoje e o fechamento de ontem",
        fecho="A coordenação lê em cinco segundos se o dia é normal ou pede reforço.",
        x=.585, y=.070, w=.345, h=.210,
        itens=[
            dict(x=.660, y=.104, w=.134, h=.152, ic="curva",
                 t="Previsto para hoje, em P3 e P2", s="Prophet · faixa de 80%",
                 d="O número do dia e o intervalo em que ele deve cair."),
            dict(x=.822, y=.096, w=.104, h=.080, ic="base",
                 t="Como ontem fechou", s="Base elegível ao KPI",
                 d="Registrados no dia anterior e quantos violaram o prazo."),
            dict(x=.822, y=.184, w=.104, h=.072, ic="relogio",
                 t="Dias úteis seguidos sem violação", s="Base elegível ao KPI",
                 d="A sequência em pé até o corte do relógio do sistema."),
        ]),
    dict(
        titulo="O dia hora a hora, P3 e P2",
        fecho="Registrado abaixo da faixa é dia calmo; acima, é hora de olhar a fila.",
        x=.072, y=.295, w=.856, h=.380,
        itens=[
            dict(x=.243, y=.470, w=.164, h=.100, ic="base",
                 t="O que já entrou até as 15h", s="Registro da base",
                 d="A linha cheia é o realizado do dia, hora a hora."),
            dict(x=.348, y=.398, w=.128, h=.098, ic="curva",
                 t="O esperado para a hora, com a faixa", s="Prophet · curva por hora",
                 d="A tracejada e a faixa em volta dizem o que era esperado agora."),
            dict(x=.505, y=.345, w=.420, h=.318, ic="alvo",
                 t="O P2 ao lado, com meta própria", s="Prophet",
                 d="As duas prioridades entram no indicador, cada uma com a sua meta."),
        ]),
    dict(
        titulo="Onde agir agora",
        fecho="O topo da fila de risco sem sair do Panorama; a seta abre o detalhe do caso.",
        x=.072, y=.690, w=.856, h=.310,
        itens=[
            dict(x=.078, y=.788, w=.048, h=.040, ic="alvo",
                 t="Probabilidade de estourar o prazo", s="Regressão logística",
                 d="Cada caso aberto recebe a sua, e a lista ordena por ela."),
            dict(x=.232, y=.802, w=.114, h=.030, ic="peso",
                 t="O fator que mais pesa na pontuação", s="Explicabilidade do modelo",
                 d="Produto, equipe ou hora de abertura, com o peso de cada um."),
            dict(x=.816, y=.694, w=.098, h=.030, ic="lista",
                 t="A fila completa, 49 casos às 15h", s="Aba Fila de risco",
                 d="O mesmo modelo, com filtro por faixa de risco e por prioridade."),
        ]),
]

CABECA = """<section class="slide light {classe}" data-slide="0" data-var="a">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="hd"><div class="bi">{logo}</div><div class="bn">Cronos</div>
    <div class="tag">Aba Panorama &middot; destaque {i} de 3</div></div>
  <div class="body">"""
RODAPE = """  </div>
  <div class="ft"><span>Captura da aplicação &middot; relógio do sistema em 01/10/2025, 15h</span></div>
</section>"""


def _crop(d: dict, largura: float, classe: str = "crop", extra: str = "") -> tuple[str, float]:
    """A caixa com o recorte da imagem, em `largura` px, e a altura que ela ocupa."""
    razao = (d["h"] * 2000) / (d["w"] * 3200)
    altura = largura * razao
    bx = d["x"] / (1 - d["w"]) * 100
    by = d["y"] / (1 - d["h"]) * 100
    est = (f'width:{largura:.0f}px;height:{altura:.0f}px;'
           f'background-image:url({PRINTS}/01-panorama.png);'
           f'background-size:{100 / d["w"]:.3f}% {100 / d["h"]:.3f}%;'
           f'background-position:{bx:.3f}% {by:.3f}%')
    return f'<div class="{classe}" style="{est};{extra}"></div>', altura


# ── A · legendas alinhadas embaixo ──────────────────────────────────────────
CSS_A = """
.va .body{padding-top:14px}
.va .tt{font-size:42px;letter-spacing:-1.6px;line-height:1.06}
.va .cena{margin-top:22px;position:relative;margin-left:auto;margin-right:auto}
.va .crop{border-radius:14px;border:1px solid #D6DEE9;background-repeat:no-repeat;
  background-color:#fff;box-shadow:0 34px 80px -46px rgba(15,23,42,.5)}
.va .faixa{display:flex;margin-top:26px;border-top:1px solid #DCE4EF}
.va .lg{padding:18px 26px 0;border-right:1px solid #DCE4EF;display:flex;gap:14px;align-items:flex-start}
.va .lg:first-child{padding-left:0}
.va .lg:last-child{border-right:none;padding-right:0}
.va .lg .ic{width:22px;height:22px;color:var(--accent);flex-shrink:0;margin-top:2px}
.va .lg b{display:block;font-size:16px;font-weight:700;color:var(--head);letter-spacing:-.25px;
  line-height:1.3}
.va .lg p{font-size:13.5px;line-height:1.45;color:var(--tx);margin-top:6px}
.va .lg i{display:block;font-style:normal;font-family:var(--mono);font-size:11.5px;
  color:var(--accent);margin-top:8px}
.va .marca{position:absolute;border:2px solid var(--accent);border-radius:8px;
  background:rgba(37,99,235,.08);box-shadow:0 0 0 3px rgba(255,255,255,.45)}
"""


ALT_MAX_A = 440


def variante_a(d: dict, i: int) -> str:
    """Imagem grande em cima; cada legenda na coluna do que ela descreve."""
    largura = PALCO_W
    razao = (d["h"] * 2000) / (d["w"] * 3200)
    if largura * razao > ALT_MAX_A:
        largura = ALT_MAX_A / razao
    crop, alt = _crop(d, largura, extra="position:relative")
    marcas = "".join(
        f'<div class="marca" style="left:{(it["x"] - d["x"]) / d["w"] * 100:.2f}%;'
        f'top:{(it["y"] - d["y"]) / d["h"] * 100:.2f}%;width:{it["w"] / d["w"] * 100:.2f}%;'
        f'height:{it["h"] / d["h"] * 100:.2f}%"></div>' for it in d["itens"])
    legendas = "".join(
        f'<div class="lg" style="flex:1">{icone(it["ic"])}'
        f'<div><b>{it["t"]}</b><p>{it["d"]}</p><i>{it["s"]}</i></div></div>' for it in d["itens"])
    return (CABECA.format(classe="va", logo=mk.LOGO_CLARO, i=i)
            + f'<span class="eb">Aba Panorama &middot; destaque {i} de 3</span>'
            f'<h1 class="tt">{d["titulo"]}</h1>'
            f'<div class="cena" style="width:{largura:.0f}px;height:{alt:.0f}px">{crop[:-6]}{marcas}</div></div>'
            f'<div class="faixa">{legendas}</div>' + RODAPE)


# ── B · balões com bico, encostados no elemento ─────────────────────────────
CSS_B = """
.vb .body{padding-top:14px}
.vb .tt{font-size:42px;letter-spacing:-1.6px;line-height:1.06}
.vb .cena{margin:22px auto 0;position:relative}
.vb .crop{border-radius:14px;border:1px solid #D6DEE9;background-repeat:no-repeat;
  background-color:#fff;box-shadow:0 34px 80px -46px rgba(15,23,42,.5)}
.vb .marca{position:absolute;border:2px solid var(--accent);border-radius:8px;
  background:rgba(37,99,235,.10);box-shadow:0 0 0 3px rgba(255,255,255,.5)}
.vb .balao{position:absolute;background:rgba(255,255,255,.94);backdrop-filter:blur(10px);
  border:1px solid rgba(37,99,235,.22);border-radius:12px;padding:11px 15px;
  box-shadow:0 22px 44px -24px rgba(15,23,42,.55);display:flex;gap:11px;align-items:flex-start}
.vb .balao .ic{width:19px;height:19px;color:var(--accent);flex-shrink:0;margin-top:1px}
.vb .balao b{display:block;font-size:14.5px;font-weight:700;color:var(--head);line-height:1.3;
  letter-spacing:-.2px}
.vb .balao i{display:block;font-style:normal;font-family:var(--mono);font-size:11px;
  color:var(--accent);margin-top:5px}
.vb .balao::after{content:"";position:absolute;width:12px;height:12px;background:inherit;
  border-left:1px solid rgba(37,99,235,.22);border-top:1px solid rgba(37,99,235,.22);
  left:var(--bx,24px)}
.vb .balao.baixo::after{top:-7px;transform:rotate(45deg)}
.vb .balao.alto::after{bottom:-7px;transform:rotate(225deg)}
.vb .fecho{display:flex;align-items:flex-start;gap:12px;margin-top:auto;padding-top:16px;
  border-top:1px solid #DCE4EF;font-size:16.5px;line-height:1.45;color:var(--tx)}
.vb .fecho .ic{width:20px;height:20px;color:var(--accent);margin-top:2px;flex-shrink:0}
"""
BALAO_W = 340


ALT_MAX_B = 470
BALAO_H = 66


def _cabe(r: tuple, obstaculos: list[tuple], limite: tuple) -> bool:
    """O retângulo cabe no limite e não encosta em nenhum obstáculo?"""
    x, y, w, h = r
    if x < 8 or y < 8 or x + w > limite[0] - 8 or y + h > limite[1] - 8:
        return False
    return all(not (x < ox + ow + 10 and x + w + 10 > ox and y < oy + oh + 10 and y + h + 10 > oy)
               for ox, oy, ow, oh in obstaculos)


def variante_b(d: dict, i: int) -> str:
    """Balão de vidro encostado no elemento, com bico de 12px no lugar da linha."""
    largura = PALCO_W
    razao = (d["h"] * 2000) / (d["w"] * 3200)
    if largura * razao > ALT_MAX_B:
        largura = ALT_MAX_B / razao
    crop, alt = _crop(d, largura, extra="position:absolute;left:0;top:0")
    caixas = [((it["x"] - d["x"]) / d["w"] * largura, (it["y"] - d["y"]) / d["h"] * alt,
               it["w"] / d["w"] * largura, it["h"] / d["h"] * alt) for it in d["itens"]]
    partes = [f'<div class="marca" style="left:{bl:.0f}px;top:{bt:.0f}px;'
              f'width:{bw:.0f}px;height:{bh:.0f}px"></div>' for bl, bt, bw, bh in caixas]
    postos: list[tuple] = []
    for it, (bl, bt, bw, bh) in zip(d["itens"], caixas):
        cx = bl + bw / 2
        # tenta embaixo, em cima, à direita e à esquerda, nessa ordem
        tentativas = [
            ("baixo", cx - BALAO_W / 2, bt + bh + 14),
            ("alto", cx - BALAO_W / 2, bt - BALAO_H - 14),
            ("baixo", bl + bw + 14, bt + bh / 2 - BALAO_H / 2),
            ("baixo", bl - BALAO_W - 14, bt + bh / 2 - BALAO_H / 2),
        ]
        escolha = next((t for t in tentativas
                        if _cabe((t[1], t[2], BALAO_W, BALAO_H), caixas + postos, (largura, alt))),
                       None)
        if escolha is None:
            escolha = ("baixo", min(max(cx - BALAO_W / 2, 8), largura - BALAO_W - 8), bt + bh + 14)
        lado, bx, by = escolha
        postos.append((bx, by, BALAO_W, BALAO_H))
        bico = min(max(cx - bx - 6, 18), BALAO_W - 30)
        partes.append(
            f'<div class="balao {lado}" '
            f'style="left:{bx:.0f}px;top:{by:.0f}px;width:{BALAO_W}px;--bx:{bico:.0f}px">'
            f'{icone(it["ic"])}<div><b>{it["t"]}</b><i>{it["s"]}</i></div></div>')
    return (CABECA.format(classe="vb", logo=mk.LOGO_CLARO, i=i)
            + f'<span class="eb">Aba Panorama &middot; destaque {i} de 3</span>'
            f'<h1 class="tt">{d["titulo"]}</h1>'
            f'<div class="cena" style="width:{largura:.0f}px;height:{alt:.0f}px">{crop}{"".join(partes)}</div>'
            f'<div class="fecho">{icone("alvo")}<span>{d["fecho"]}</span></div>' + RODAPE)


# ── C · passos ao lado ──────────────────────────────────────────────────────
CSS_C = """
.vc .body{padding-top:14px}
.vc .cena{flex:1;min-height:0;display:flex;gap:46px;align-items:center}
.vc .lado{width:454px;flex-shrink:0}
.vc .tt{font-size:40px;letter-spacing:-1.5px;line-height:1.08}
.vc .passos{margin-top:24px}
.vc .ps{display:flex;gap:16px;padding:17px 0;align-items:flex-start}
.vc .ps + .ps{border-top:1px solid #DCE4EF}
.vc .ps .chip{width:42px;height:42px;border-radius:12px;background:var(--accent-l);
  border:1px solid #BFDBFE;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.vc .ps .chip .ic{width:21px;height:21px;color:var(--accent)}
.vc .ps b{display:block;font-size:16.5px;font-weight:700;color:var(--head);letter-spacing:-.25px;
  line-height:1.3}
.vc .ps p{font-size:14px;line-height:1.45;color:var(--tx);margin-top:5px}
.vc .ps i{display:block;font-style:normal;font-family:var(--mono);font-size:11.5px;
  color:var(--accent);margin-top:7px}
.vc .palco4{flex:1;min-width:0;display:flex;justify-content:flex-end}
.vc .crop{position:relative;border-radius:14px;border:1px solid #D6DEE9;background-repeat:no-repeat;
  background-color:#fff;box-shadow:0 40px 90px -46px rgba(15,23,42,.55)}
.vc .marca{position:absolute;border:2px solid var(--accent);border-radius:8px;
  background:rgba(37,99,235,.09);box-shadow:0 0 0 3px rgba(255,255,255,.45)}
.vc .fecho{display:flex;align-items:flex-start;gap:12px;margin-top:16px;padding-top:16px;
  border-top:1px solid #DCE4EF;font-size:16px;line-height:1.45;color:var(--tx)}
.vc .fecho .ic{width:20px;height:20px;color:var(--accent);margin-top:2px;flex-shrink:0}
"""


def variante_c(d: dict, i: int) -> str:
    """Imagem à direita; coluna de passos à esquerda, na ordem de leitura da tela."""
    largura = PALCO_W - 454 - 46
    crop, alt = _crop(d, largura, extra="position:relative")
    if alt > 520:
        largura, alt = largura * 520 / alt, 520
        crop, alt = _crop(d, largura, extra="position:relative")
    marcas = "".join(
        f'<div class="marca" style="left:{(it["x"] - d["x"]) / d["w"] * 100:.2f}%;'
        f'top:{(it["y"] - d["y"]) / d["h"] * 100:.2f}%;width:{it["w"] / d["w"] * 100:.2f}%;'
        f'height:{it["h"] / d["h"] * 100:.2f}%"></div>' for it in d["itens"])
    passos = "".join(
        f'<div class="ps"><span class="chip">{icone(it["ic"])}</span>'
        f'<div><b>{it["t"]}</b><p>{it["d"]}</p><i>{it["s"]}</i></div></div>' for it in d["itens"])
    return (CABECA.format(classe="vc", logo=mk.LOGO_CLARO, i=i)
            + f'<div class="cena"><div class="lado">'
            f'<span class="eb">Aba Panorama &middot; destaque {i} de 3</span>'
            f'<h1 class="tt">{d["titulo"]}</h1><div class="passos">{passos}</div>'
            f'<div class="fecho">{icone("alvo")}<span>{d["fecho"]}</span></div></div>'
            f'<div class="palco4">{crop[:-6]}{marcas}</div></div></div>' + RODAPE)


CSS_PAGINA = """
body{background:#2A2F38;overflow:auto;padding:34px 0 60px}
.palco{width:1600px;height:900px;position:relative;overflow:hidden;margin:0 auto 34px;
  box-shadow:0 30px 90px -40px rgba(0,0,0,.7);background:#fff}
.rot{width:1600px;margin:0 auto 10px;color:rgba(255,255,255,.62);font-family:var(--mono);font-size:13px}
.sec{width:1600px;margin:56px auto 22px;color:#fff;font-family:var(--font);font-size:30px;
  font-weight:800;letter-spacing:-.8px;padding-top:24px;border-top:1px solid rgba(255,255,255,.18)}
.sec small{display:block;font-size:16px;font-weight:400;color:rgba(255,255,255,.62);margin-top:6px;
  letter-spacing:0;line-height:1.45;max-width:1100px}
"""

VARIANTES = [
    ("A", "Legendas alinhadas embaixo",
     "A imagem ocupa a largura toda e as legendas ficam numa faixa abaixo dela, cada uma na "
     "coluna do elemento que descreve. O alinhamento faz o trabalho que a linha fazia.",
     variante_a, CSS_A),
    ("B", "Balões com bico, encostados no elemento",
     "O balão fica junto do que explica, com um bico de 12px no lugar da linha. Nada atravessa "
     "a imagem, e a ligação continua sem dúvida.", variante_b, CSS_B),
    ("C", "Passos ao lado da imagem",
     "A imagem vai para a direita e os passos ficam numa coluna à esquerda, na mesma ordem de "
     "leitura da tela. Cada passo tem ícone, título, uma linha e a fonte.", variante_c, CSS_C),
]


def main() -> int:
    """Um HTML por abordagem, para as três não se misturarem na mesma página."""
    estilo = (mk.AO_VIVO / "_estilo.css").read_text(encoding="utf-8")
    congela = mk.CSS_BUILDER.replace("#palco{", ".palco-x{")
    PNG.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=mk.CHROME)
        pg = nav.new_page(viewport={"width": 1700, "height": 1000})
        for letra, nome, desc, fn, css in VARIANTES:
            partes = [f'<div class="sec">Abordagem {letra} &middot; {nome}'
                      f"<small>{desc}</small></div>"]
            for i, d in enumerate(DESTAQUES, 1):
                partes.append(f'<p class="rot">Destaque {i} de 3 &middot; {d["titulo"]}</p>'
                              f'<div class="palco" id="{letra.lower()}{i}">'
                              + fn(d, i).replace('class="slide', 'class="is-active slide', 1)
                              + "</div>")
            html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
                    f'<title>Panorama · abordagem {letra} · {nome}</title>{mk.FONTES}'
                    f"<style>{estilo}\n{css}\n{congela}\n{CSS_PAGINA}</style></head>"
                    f"<body>{''.join(partes)}</body></html>")
            destino = AQUI / f"_tela-{letra}.html"
            destino.write_text(html, encoding="utf-8")
            pg.goto(destino.as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(700)
            for el in pg.query_selector_all(".palco"):
                png = PNG / f"tela-{el.get_attribute('id')}.png"
                el.scroll_into_view_if_needed()
                el.screenshot(path=str(png))
            print(f"{destino.name}  ·  {len(DESTAQUES)} slides")
        nav.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
