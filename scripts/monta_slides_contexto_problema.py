# -*- coding: utf-8 -*-
"""Gera os slides 03 (contextualização) e 04 (problema) da abertura do deck.

Estes dois voltaram para a mesa três vezes. O que reprovou as versões anteriores:

* **03** montava o Ishikawa como seis cartões iguais em volta de uma espinha decorativa, e
  as "causas" eram métricas do nosso próprio modelo, não causas do problema do cliente.
  Aqui a espinha é desenhada de verdade, o texto fica sobre o osso sem moldura, e cada
  causa é uma frase de causa com a evidência numérica embaixo. Duas causas ficam em azul:
  são as que o Cronos ataca, o que prepara o slide seguinte.
* **04** desenhava doze células verdes iguais por prioridade, o que comunica "está tudo
  bem" e esconde a única coisa que importa, que é a travessia de faixa. Aqui a régua vira
  fundo do gráfico, o acumulado sobe contra ela, e o mês que decidiu a nota é anotado.

A geometria sai de cálculo, não de número digitado no CSS: altura de barra, corte de faixa
e coordenada de osso são funções dos valores da folha de fatos.

Uso:
    .venv/Scripts/python scripts/monta_slides_contexto_problema.py          # HTML
    .venv/Scripts/python scripts/monta_slides_contexto_problema.py --png    # HTML + PNG
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "prototipos" / "slides" / "mvp" / "abertura"

LARGURA, ALTURA = 1600, 900

CABECA = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>{titulo}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="base.css">
<style>{css}</style>
</head><body>
<section class="slide light {classe}">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="hd"><div class="bi"><svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" r="3" fill="none" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg></div><div class="bn">Cronos</div><span class="bt">· Veja antes · Aja antes</span><div class="tag">Template · slide {n}</div></div>
  <div class="body">{corpo}</div>
  <div class="ft"><span>Cronos · Super Data Bros · 2TSCOA</span><span>Challenge FIAP 2026 com Locaweb</span></div>
</section>
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# Slide 03 · contextualização
# ═══════════════════════════════════════════════════════════════════════════════
# Cada causa é (categoria, frase de causa, evidência em HTML, se é atacada pelo Cronos).
# A frase diz o que causa o estouro; a evidência é o número que sustenta a frase. Sem a
# frase o slide vira painel de indicadores, que foi o defeito das versões anteriores.
CAUSAS_TOPO = [
    (
        "Método",
        "A fila é atendida por ordem de prioridade, que não separa quem vai estourar.",
        'ROC AUC de <b class="ac">0,4693</b>, abaixo dos <b>0,5063</b> de uma fila sorteada',
        True,
    ),
    (
        "Medição",
        "A faixa de nota do ano só é conhecida na apuração de dezembro.",
        'O P2 vai de <b>35</b> em outubro a <b class="ac">41</b> em novembro',
        True,
    ),
    (
        "Máquina",
        "Quase todo registro nasce do monitoramento automático.",
        '<b>85,1%</b> vêm de Monitoramento e <b>65,6%</b> fecham sem intervenção',
        False,
    ),
]
CAUSAS_BASE = [
    (
        "Mão de obra",
        "O risco se concentra numa equipe pequena.",
        'Team11 responde por <b>8%</b> do volume e <b>46%</b> das violações',
        False,
    ),
    (
        "Material",
        "O caso inédito estoura mais que a rotina conhecida.",
        'Incidentes únicos: <b>38%</b> do volume e <b>59%</b> das violações',
        False,
    ),
    (
        "Meio ambiente",
        "O tamanho da fila não diz onde a violação vai acontecer.",
        'O volume diário explica <b>2,5%</b> da variação',
        False,
    ),
]

# Geometria do Ishikawa, em px do próprio bloco. A espinha corta o bloco na metade; os
# ossos de cima e de baixo são simétricos, e o texto de cada um ocupa a faixa livre acima
# ou abaixo da ponta do osso.
ISH_W, ISH_H = 1472, 520
ESPINHA_Y = ISH_H // 2
OSSO_DX, OSSO_DY = 170, 120
# O espaçamento das âncoras é o que impede um bloco de texto de encostar no vizinho: cada
# bloco ocupa de `âncora - OSSO_DX - 6` até `+ TXT_W`, então a distância entre âncoras
# precisa passar de TXT_W com folga.
ANCORAS_TOPO = [300, 640, 980]
ANCORAS_BASE = [360, 700, 1040]
TXT_W = 300
CABECA_X, CABECA_W, CABECA_H = 1148, 312, 152


def _ossos_svg() -> str:
    """Espinha, seta e os seis ossos. Osso atacado pelo Cronos sai em azul."""
    p = [
        f'<line x1="24" y1="{ESPINHA_Y}" x2="{CABECA_X - 14}" y2="{ESPINHA_Y}" '
        f'stroke="#0B1220" stroke-width="2.4"/>',
        f'<path d="M{CABECA_X - 30} {ESPINHA_Y - 9} L{CABECA_X - 8} {ESPINHA_Y} '
        f'L{CABECA_X - 30} {ESPINHA_Y + 9} Z" fill="#0B1220"/>',
    ]
    for ancoras, sinal, causas in (
        (ANCORAS_TOPO, -1, CAUSAS_TOPO),
        (ANCORAS_BASE, +1, CAUSAS_BASE),
    ):
        for x, (_, _, _, foco) in zip(ancoras, causas):
            cor = "#2563EB" if foco else "#AEBACB"
            larg = "2.4" if foco else "1.8"
            p.append(
                f'<line x1="{x}" y1="{ESPINHA_Y}" x2="{x - OSSO_DX}" '
                f'y2="{ESPINHA_Y + sinal * OSSO_DY}" stroke="{cor}" stroke-width="{larg}"/>'
            )
            p.append(
                f'<circle cx="{x}" cy="{ESPINHA_Y}" r="4" fill="#fff" stroke="{cor}" '
                f'stroke-width="2"/>'
            )
    return f'<svg class="ossos" width="{ISH_W}" height="{ISH_H}">{"".join(p)}</svg>'


def _textos_ossos() -> str:
    """Blocos de texto nas pontas dos ossos, sem moldura: o osso já delimita."""
    saida = []
    for ancoras, topo, causas in (
        (ANCORAS_TOPO, True, CAUSAS_TOPO),
        (ANCORAS_BASE, False, CAUSAS_BASE),
    ):
        for x, (cat, frase, evid, foco) in zip(ancoras, causas):
            esq = x - OSSO_DX - 6
            pos = (
                f"top:2px;height:{ESPINHA_Y - OSSO_DY - 12}px;justify-content:flex-end"
                if topo
                else f"top:{ESPINHA_Y + OSSO_DY + 10}px;height:{ESPINHA_Y - OSSO_DY - 12}px"
            )
            saida.append(
                f'<div class="osso{" foco" if foco else ""}" '
                f'style="left:{esq}px;width:{TXT_W}px;{pos}">'
                f'<span class="cat">{cat}</span>'
                f'<p class="cau">{frase}</p>'
                f'<p class="evi">{evid}</p></div>'
            )
    return "".join(saida)


def slide_03() -> str:
    css = """
.ish .body{padding:20px 64px 40px}
.ish .tt{font-size:38px}
.ish .lead{font-size:17px;margin-top:11px;max-width:1180px}

/* faixa de contexto: uma linha só, dividida, em vez de quatro cartões repetidos */
.ctx{display:flex;align-items:stretch;background:#fff;border:1px solid var(--line);
  border-radius:14px;margin-top:16px;box-shadow:0 14px 34px -30px rgba(15,23,42,.28)}
.ctx .c{padding:13px 22px;border-left:1px solid var(--line);min-width:0}
.ctx .c:first-child{border-left:none}
.ctx .c .k{font-size:11px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;
  color:var(--tx2)}
.ctx .c .v{font-size:22px;font-weight:800;letter-spacing:-.7px;color:var(--head);
  margin-top:4px;font-variant-numeric:tabular-nums}
.ctx .c .v em{font-style:normal;font-size:14px;font-weight:600;color:var(--tx);
  letter-spacing:0}
.ctx .hist{flex:1;background:linear-gradient(90deg,#F7FAFF,#fff);border-radius:0 13px 13px 0}
.ctx .hist .v{font-size:15.5px;font-weight:500;color:var(--tx);letter-spacing:0;
  line-height:1.45;margin-top:5px}
.ctx .hist .v b{color:var(--head);font-weight:700}

/* Ishikawa */
.ish .diag{position:relative;width:1472px;height:520px;margin-top:10px}
.ish .ossos{position:absolute;inset:0}
.ish .osso{position:absolute;display:flex;flex-direction:column;gap:3px}
.ish .osso .cat{font-size:11.5px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
  color:var(--tx2)}
.ish .osso.foco .cat{color:var(--accent)}
.ish .osso .cau{font-size:15.5px;line-height:1.32;font-weight:600;color:var(--head)}
.ish .osso .evi{font-size:13.5px;line-height:1.35;color:var(--tx);
  font-variant-numeric:tabular-nums}
.ish .osso .evi b{font-weight:700;color:var(--head)}
.ish .osso .evi b.ac{color:var(--accent)}

/* cabeça: o efeito, com as duas prioridades lado a lado */
.ish .cab{position:absolute;background:var(--ink);border-radius:16px;padding:18px 22px;
  display:flex;flex-direction:column;box-shadow:0 22px 48px -26px rgba(11,18,32,.55)}
.ish .cab .k{font-size:11px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;
  color:#F0B767}
.ish .cab .t{font-size:19px;font-weight:800;letter-spacing:-.4px;color:#fff;
  line-height:1.2;margin-top:7px}
.ish .cab .duo{display:flex;gap:26px;margin-top:auto;padding-top:13px;
  border-top:1px solid rgba(255,255,255,.14)}
.ish .cab .duo div{min-width:0}
.ish .cab .duo .n{font-size:27px;font-weight:800;letter-spacing:-1px;
  font-variant-numeric:tabular-nums}
.ish .cab .duo .p2 .n{color:#F87171} .ish .cab .duo .p3 .n{color:#4ADE80}
.ish .cab .duo .l{font-size:12px;color:#8B96A8;margin-top:2px}
.ish .cab .duo .l b{color:#C4CDDB;font-weight:700}
"""
    corpo = (
        '<span class="eb">Contextualização do problema</span>'
        '<h1 class="tt">Contexto da operação e causas do '
        '<span class="hl">estouro de OLA</span></h1>'
        '<p class="lead">A Locaweb opera hospedagem e cloud 24 por 7 para pequeno e médio '
        "negócio. O desempenho é medido por um indicador anual de violação de OLA, apurado "
        "por faixa, e a faixa em que o ano fechou só é conhecida na apuração de dezembro.</p>"
        # contexto e fator histórico
        '<div class="ctx">'
        '<div class="c"><div class="k">Base recebida</div>'
        '<div class="v">122.543 <em>incidentes, 2023 a 2025</em></div></div>'
        '<div class="c"><div class="k">Contam para a meta</div>'
        '<div class="v">25.600 <em>elegíveis ao KPI</em></div></div>'
        '<div class="c"><div class="k">Prazo de OLA</div>'
        '<div class="v">4 h <em>no P2</em> · 12 h <em>no P3</em></div></div>'
        '<div class="c hist"><div class="k">Fator histórico · setembro de 2025</div>'
        '<div class="v">A expansão do monitoramento automático levou o registro de '
        "<b>3.996</b> para <b>21.561</b> no mês. A série que conta para a meta foi de "
        "<b>2.330</b> para <b>2.324</b>, praticamente parada.</div></div>"
        "</div>"
        # Ishikawa
        '<div class="diag">'
        + _ossos_svg()
        + _textos_ossos()
        + f'<div class="cab" style="left:{CABECA_X}px;width:{CABECA_W}px;'
        f'top:{ESPINHA_Y - CABECA_H // 2}px;height:{CABECA_H}px">'
        '<span class="k">Efeito</span>'
        '<div class="t">Estouro de OLA no fechamento do ano</div>'
        '<div class="duo">'
        '<div class="p2"><div class="n">42</div>'
        '<div class="l">P2 em 2025 · nota <b>75%</b></div></div>'
        '<div class="p3"><div class="n">196</div>'
        '<div class="l">P3 em 2025 · nota <b>150%</b></div></div>'
        "</div></div>"
        "</div>"
    )
    return CABECA.format(titulo="03 Contexto · C", css=css, classe="ish", n=3, corpo=corpo)


# ═══════════════════════════════════════════════════════════════════════════════
# Slide 04 · problema a ser resolvido
# ═══════════════════════════════════════════════════════════════════════════════
# A régua oficial da Locaweb: (nota, limite superior de violações no ano). O último item é
# a faixa aberta, que não tem limite.
REGUA_P2 = [("150%", 30), ("125%", 35), ("100%", 39), ("75%", 45), ("50%", 53), ("0%", None)]
REGUA_P3 = [("150%", 200), ("125%", 230), ("100%", 263), ("75%", 290), ("50%", 320), ("0%", None)]

ACUM_P2 = [4, 8, 11, 13, 19, 22, 28, 31, 33, 35, 41, 42]
ACUM_P3 = [19, 40, 56, 66, 81, 109, 132, 146, 155, 164, 179, 196]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

# Tom de fundo de cada faixa, do melhor para o pior.
TOM = {
    "150%": "#E4F4EB",
    "125%": "#F1FAF4",
    "100%": "#EEF4FF",
    "75%": "#FDF0EF",
    "50%": "#FADFDE",
    "0%": "#F5CFCE",
}
PLOT_H = 344


def _grafico(nome: str, prazo: str, regua, acum, teto: int, meta: int, fecho: str) -> str:
    """Um gráfico por prioridade: régua como fundo, acumulado como barra."""
    # faixas, de baixo para cima; o corte fica entre dois inteiros para a barra de valor
    # igual ao limite cair dentro da faixa, e não em cima da linha
    faixas, base, anterior = [], 0.0, 0
    for nota, limite in regua:
        topo = teto if limite is None else limite + 0.5
        alt = (topo - base) / teto * PLOT_H
        rot = f"{anterior + 1} ou mais" if limite is None else f"até {limite}"
        faixas.append(
            f'<div class="fx" style="bottom:{base / teto * PLOT_H:.1f}px;'
            f'height:{alt:.1f}px;background:{TOM[nota]}">'
            f'<span class="fl"><b>{nota}</b> · {rot}</span></div>'
        )
        base = topo
        anterior = limite

    limite_faixa = next(l for n, l in regua if n == "125%")
    barras = []
    for mes, v in zip(MESES, acum):
        perdeu = v > limite_faixa
        barras.append(
            f'<div class="col"><span class="bv{" ruim" if perdeu else ""}">{v}</span>'
            f'<div class="bar{" ruim" if perdeu else ""}" '
            f'style="height:{v / teto * PLOT_H:.1f}px"></div>'
            f'<span class="mx">{mes}</span></div>'
        )

    return (
        f'<figure class="gr"><figcaption><span class="gn">{nome}</span>'
        f'<span class="gp">prazo de {prazo}</span>'
        f'<span class="gf">{fecho}</span></figcaption>'
        f'<div class="plot">{"".join(faixas)}'
        f'<div class="meta" style="bottom:{(meta + 0.5) / teto * PLOT_H:.1f}px">'
        f'<span>meta {meta}</span></div>'
        f'<div class="cols">{"".join(barras)}</div></div></figure>'
    )


def slide_04() -> str:
    css = f"""
.kpi .body{{padding:20px 64px 40px}}
.kpi .tt{{font-size:38px}}
.kpi .lead{{font-size:17px;margin-top:11px;max-width:1240px}}
.kpi .como{{font-size:13.5px;color:var(--tx2);margin-top:14px}}
.kpi .como b{{color:var(--tx);font-weight:600}}

.kpi .duo{{display:flex;gap:22px;margin-top:10px}}
.gr{{flex:1;background:#fff;border:1px solid var(--line);border-radius:16px;
  padding:16px 20px 12px;box-shadow:0 16px 38px -30px rgba(15,23,42,.28);min-width:0}}
.gr figcaption{{display:flex;align-items:baseline;gap:10px;margin-bottom:12px}}
.gr .gn{{font-size:20px;font-weight:800;letter-spacing:-.5px;color:var(--head)}}
.gr .gp{{font-size:13.5px;color:var(--tx2)}}
.gr .gf{{margin-left:auto;font-size:13px;font-weight:700;color:var(--tx);
  font-variant-numeric:tabular-nums}}

.plot{{position:relative;height:{PLOT_H}px;margin-right:92px}}
.fx{{position:absolute;left:0;right:-92px;border-radius:3px}}
.fl{{position:absolute;right:6px;top:50%;transform:translateY(-50%);font-size:10px;
  color:var(--tx2);text-align:right;line-height:1;white-space:nowrap;
  font-variant-numeric:tabular-nums}}
.fl b{{font-weight:700;color:var(--tx)}}
.meta{{position:absolute;left:0;right:-92px;border-top:2px dashed var(--accent);z-index:3}}
.meta span{{position:absolute;left:0;top:-9px;background:var(--accent);color:#fff;
  font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:4px;
  font-variant-numeric:tabular-nums}}
.cols{{position:absolute;inset:0;display:flex;align-items:flex-end;gap:6px;z-index:2}}
.col{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;
  min-width:0}}
.bar{{width:100%;border-radius:4px 4px 0 0;background:linear-gradient(180deg,#2FA36A,#15A05B)}}
.bar.ruim{{background:linear-gradient(180deg,#E24B41,#C9372C)}}
.bv{{font-size:12.5px;font-weight:700;color:var(--good);margin-bottom:3px;
  font-variant-numeric:tabular-nums}}
.bv.ruim{{color:var(--bad)}}
.mx{{position:absolute;bottom:-21px;font-size:11.5px;color:var(--tx2)}}
.col{{position:relative}}

.nota{{display:flex;gap:10px;margin-top:30px;font-size:13.5px;line-height:1.45;
  color:var(--tx)}}
.nota b{{color:var(--head);font-weight:700}}
.nota .mk{{flex-shrink:0;width:3px;border-radius:2px;background:var(--accent)}}

.obj{{display:flex;align-items:center;gap:26px;margin-top:auto;background:#fff;
  border:1px solid var(--line);border-radius:15px;padding:16px 22px;
  box-shadow:0 14px 34px -30px rgba(15,23,42,.26)}}
.obj .k{{font-size:11.5px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
  color:var(--accent);width:132px;flex-shrink:0;line-height:1.35}}
.obj p{{font-size:15.5px;line-height:1.45;color:var(--tx);flex:1}}
.obj p b{{color:var(--head);font-weight:700}}
.obj .sep{{width:1px;align-self:stretch;background:var(--line)}}
"""
    corpo = (
        '<span class="eb">Problema a ser resolvido</span>'
        '<h1 class="tt">Atingimento do KPI em 2025 e '
        '<span class="hl">objetivos para 2026</span></h1>'
        '<p class="lead">Nas duas prioridades a nota do ano se decidiu por margem pequena, '
        "e a margem só ficou visível na apuração de dezembro. Antecipar essa leitura é o "
        "problema que o Cronos resolve.</p>"
        '<p class="como">Cada gráfico traz a <b>régua oficial da Locaweb</b> como fundo: '
        "seis faixas de nota por prioridade. A barra é o acumulado de violações no mês, e a "
        "faixa que ela alcança é a nota do ano se ele fechasse ali.</p>"
        '<div class="duo">'
        + _grafico("P2", "4 h", REGUA_P2, ACUM_P2, teto=58, meta=39, fecho="fechou em 42 · nota 75%")
        + _grafico("P3", "12 h", REGUA_P3, ACUM_P3, teto=340, meta=200, fecho="fechou em 196 · nota 150%")
        + "</div>"
        '<div class="nota"><span class="mk"></span><p>O P2 chegou a outubro com <b>35</b> '
        "violações, o limite da faixa de 125%, e a novembro com <b>41</b>, já dentro da "
        "faixa de 75%. Seis violações num mês custaram duas faixas. O P3 fechou em "
        "<b>196</b>, com o limite da faixa de 150% em <b>200</b>.</p></div>"
        '<div class="obj">'
        '<span class="k">Objetivos para 2026</span>'
        "<p>Fechar o ano com até <b>39</b> violações no P2 e até <b>200</b> no P3.</p>"
        '<span class="sep"></span>'
        "<p>Conhecer a faixa projetada <b>antes de novembro</b>, e não na apuração de "
        "dezembro, quando o ano já está formado.</p>"
        "</div>"
    )
    return CABECA.format(titulo="04 Problema · C", css=css, classe="kpi", n=4, corpo=corpo)


def main() -> None:
    arquivos = {"03-contexto-C.html": slide_03(), "04-problema-C.html": slide_04()}
    for nome, html in arquivos.items():
        (SAIDA / nome).write_text(html, encoding="utf-8")
        print(f"  {nome}")

    if "--png" in sys.argv:
        from playwright.sync_api import sync_playwright

        destino = RAIZ / "prototipos" / "slides" / "mvp" / "abertura" / "_png"
        destino.mkdir(exist_ok=True)
        with sync_playwright() as pw:
            nav = pw.chromium.launch(channel="chrome")
            pg = nav.new_context(
                viewport={"width": LARGURA, "height": ALTURA}, device_scale_factor=1
            ).new_page()
            for nome in arquivos:
                pg.goto((SAIDA / nome).resolve().as_uri(), wait_until="load")
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(1100)
                pg.locator(".slide").first.screenshot(
                    path=str(destino / nome.replace(".html", ".png"))
                )
                print(f"  _png/{nome.replace('.html', '.png')}")
            nav.close()


if __name__ == "__main__":
    main()
