# -*- coding: utf-8 -*-
"""Gera blocos/02-problema.html, o slide 2 do deck da banca.

Duas variações do MESMO dado: as 42 e 196 perdas de prazo de 2025, e a raridade
delas dentro dos 25.156 incidentes elegíveis, que dá 0,95%.

    A   os dois números dominam, a malha de 400 quadrados apoia embaixo
    B   a malha domina à esquerda, os dois números apoiam à direita

O alinhamento foi a correção pedida: o rótulo vai EMBAIXO do número e centrado
na coluna, não ao lado. Ao lado, 42 e 196 têm larguras diferentes e a linha de
base do rótulo descasa, que era o defeito visível no print.

São 400 elementos por variação, então o slide nasce de script e não da mão.
"""
from __future__ import annotations

from pathlib import Path

AQUI = Path(__file__).parent
COLS_A, LINHAS_A = 40, 10
COLS_B, LINHAS_B = 25, 16
VERMELHOS_A = (57, 148, 263, 331)
VERMELHOS_B = (73, 168, 241, 356)

PERDAS_2025 = 238
ELEGIVEIS_2025 = 25156

LOGO = (
    '<div class="bi"><svg viewBox="0 0 28 28" fill="none">'
    '<path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="22" cy="8" r="3" stroke="#3B82F6" stroke-width="1.5"/>'
    '<circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg></div>'
)


def cabecalho(tag: str) -> str:
    return (
        '  <div class="mesh"></div><div class="grid-bg"></div>\n'
        '  <div class="hd">\n'
        f"    {LOGO}\n"
        '    <div class="bn">Cronos</div>'
        '<span class="bt">BANCA FINAL &middot; 15/09/2026</span>\n'
        f'    <div class="tag">{tag}</div>\n'
        "  </div>"
    )


def malha(cols: int, linhas: int, vermelhos: tuple[int, ...], base: int) -> str:
    """Os quadradinhos, entrando em onda; os de perda viram no fim da onda."""
    qd = "".join(
        f'<i class="qd{" perda" if i in vermelhos else ""}" style="--i:{i}"></i>'
        for i in range(cols * linhas)
    )
    return f'<div class="malha" style="--base:{base}ms">{qd}</div>'


def par_de_numeros(d1: int, d2: int, c1: int, c2: int) -> str:
    return (
        '<div class="par">\n'
        f'        <div class="un rv3" style="--d:{d1}ms">\n'
        '          <span class="v num p2">'
        f'<span class="ct" data-to="42" data-delay="{c1}">0</span></span>\n'
        '          <span class="rot"><b>Prioridade 2</b>prazo de 4 horas</span>\n'
        "        </div>\n"
        '        <span class="fio"></span>\n'
        f'        <div class="un rv3" style="--d:{d2}ms">\n'
        '          <span class="v num p3">'
        f'<span class="ct" data-to="196" data-delay="{c2}">0</span></span>\n'
        '          <span class="rot"><b>Prioridade 3</b>prazo de 12 horas</span>\n'
        "        </div>\n"
        "      </div>"
    )


CSS = """<style>
/* ═══ slide 2 · os prazos perdidos em 2025 ═══════════════════════════════════
   Regra que este slide obedece: todo número técnico carrega a própria resposta
   ao lado. A malha de 400 existe para a proporção ser vista em vez de lida, e
   por isso a legenda diz quantos incidentes cada quadrado representa.
   O rótulo fica EMBAIXO do número: ao lado, 42 e 196 descasam a linha de base.
   ══════════════════════════════════════════════════════════════════════════ */
.prb .body{padding-top:14px}
.prb .tt{font-size:52px;letter-spacing:-1.9px}

.prb .par{display:flex;align-items:flex-start;justify-content:center;gap:92px}
.prb .un{display:flex;flex-direction:column;align-items:center;width:296px}
.prb .v{font-size:138px;font-weight:900;letter-spacing:-4.8px;line-height:.88}
.prb .p2{color:var(--bad)}
.prb .p3{color:var(--warn)}
.prb .rot{margin-top:12px;font-size:15px;line-height:1.35;color:var(--tx);
  text-align:center}
.prb .rot b{display:block;font-size:19px;font-weight:800;letter-spacing:-.3px;
  color:var(--head);margin-bottom:3px}
.prb .fio{width:1px;height:146px;margin-top:8px;
  background:linear-gradient(180deg,transparent,#D9E1EC 22%,#D9E1EC 78%,transparent)}

/* a malha: um quadrado por 63 incidentes elegíveis de 2025 */
.prb .malha{display:grid;gap:5px}
.prb .qd{border-radius:3px;background:#E3E9F2;opacity:0;transform:scale(.4)}
.prb.is-active .malha .qd{animation:prbEntra .34s var(--out) forwards;
  animation-delay:calc(var(--base) + var(--i) * 2.1ms)}
@keyframes prbEntra{to{opacity:1;transform:scale(1)}}
.prb .qd.perda{background:var(--bad)}
.prb.is-active .malha .qd.perda{
  animation:prbEntra .34s var(--out) forwards, prbPerda .52s var(--spring) forwards;
  animation-delay:calc(var(--base) + var(--i) * 2.1ms), calc(var(--base) + 1180ms)}
@keyframes prbPerda{0%{transform:scale(1)}44%{transform:scale(1.8)}
  100%{transform:scale(1)}}

.prb .leg{display:flex;align-items:center;gap:24px;font-size:13.5px;color:var(--tx2)}
.prb .leg .cx{display:inline-flex;align-items:center;gap:7px}
.prb .leg i{width:12px;height:12px;border-radius:3px;background:#E3E9F2;flex-shrink:0}
.prb .leg i.perda{background:var(--bad)}
.prb .leg b{color:var(--head);font-weight:700}

/* variação A · números em cima, malha larga e baixa embaixo */
.pb-a .cena{flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:48px;min-height:0}
.pb-a .cartao{padding:40px 34px 34px;display:flex;flex-direction:column;
  align-items:center;gap:18px}
.pb-a .malha{grid-template-columns:repeat(40,24px);gap:7px}
.pb-a .qd{width:24px;height:24px;border-radius:5px}

/* variação B · malha quadrada dominando, números na coluna da direita */
.pb-b .cena{flex:1;display:flex;align-items:center;justify-content:center;
  gap:58px;min-height:0}
.pb-b .cartao{padding:38px;display:flex;flex-direction:column;align-items:center;
  gap:16px}
.pb-b .malha{grid-template-columns:repeat(25,26px);gap:6px}
.pb-b .qd{width:26px;height:26px;border-radius:5px}
.pb-b .par{flex-direction:column;align-items:flex-start;gap:32px}
.pb-b .un{align-items:flex-start;width:auto}
.pb-b .rot{text-align:left}
.pb-b .v{font-size:100px;letter-spacing:-3.8px}
.pb-b .fio{width:206px;height:1px;margin:0;
  background:linear-gradient(90deg,#D9E1EC,transparent)}
.pb-b .leg{flex-direction:column;align-items:flex-start;gap:8px}
</style>"""


def main() -> int:
    por_quadrado = ELEGIVEIS_2025 // (COLS_A * LINHAS_A)

    a = (
        '<section class="slide light prb pb-a" data-slide="2" data-var="a" '
        'data-quem="igor">\n'
        + cabecalho("Base elegível ao KPI &middot; 2025")
        + "\n  <div class=\"body\">\n"
        '    <span class="eb"><span class="rv" style="--d:240ms">O problema</span></span>\n'
        '    <h1 class="tt"><span class="mask" style="--d:340ms">'
        "<span>Os prazos perdidos em 2025</span></span></h1>\n"
        '    <div class="cena">\n'
        f"      {par_de_numeros(700, 820, 900, 1020)}\n"
        '      <div class="cartao rv3" style="--d:1100ms">\n'
        f"        {malha(COLS_A, LINHAS_A, VERMELHOS_A, 1250)}\n"
        '        <div class="leg rv" style="--d:2520ms">\n'
        f'          <span class="cx"><i></i>cada quadrado &eacute; <b>{por_quadrado} '
        "incidentes</b></span>\n"
        '          <span class="cx"><i class="perda"></i><b>238 perdas</b> em 25.156 '
        "eleg&iacute;veis, <b>0,95%</b></span>\n"
        "        </div>\n"
        "      </div>\n"
        "    </div>\n"
        "  </div>\n"
        '  <div class="ft"><span>Ano de 2025 &middot; a meta do KPI &eacute; anual '
        "&middot; a base de tr&ecirc;s anos soma 25.600 eleg&iacute;veis e 248 "
        "perdas</span></div>\n"
        "</section>"
    )

    b = (
        '<section class="slide light prb pb-b" data-slide="2" data-var="b" '
        'data-quem="igor">\n'
        + cabecalho("Base elegível ao KPI &middot; 2025")
        + "\n  <div class=\"body\">\n"
        '    <span class="eb"><span class="rv" style="--d:240ms">O problema</span></span>\n'
        '    <h1 class="tt"><span class="mask" style="--d:340ms">'
        "<span>Os prazos perdidos em 2025</span></span></h1>\n"
        '    <div class="cena">\n'
        '      <div class="cartao rv3" style="--d:680ms">\n'
        f"        {malha(COLS_B, LINHAS_B, VERMELHOS_B, 850)}\n"
        '        <div class="leg rv" style="--d:2300ms">\n'
        f'          <span class="cx"><i></i>cada quadrado &eacute; <b>{por_quadrado} '
        "incidentes</b></span>\n"
        '          <span class="cx"><i class="perda"></i><b>0,95%</b> da base '
        "eleg&iacute;vel</span>\n"
        "        </div>\n"
        "      </div>\n"
        f"      {par_de_numeros(1000, 1120, 1200, 1320)}\n"
        "    </div>\n"
        "  </div>\n"
        '  <div class="ft"><span>238 perdas em 25.156 eleg&iacute;veis em 2025 '
        "&middot; a meta do KPI &eacute; anual &middot; a base de tr&ecirc;s anos "
        "soma 248</span></div>\n"
        "</section>"
    )

    destino = AQUI / "blocos" / "02-problema.html"
    destino.write_text(CSS + "\n\n" + a + "\n\n" + b + "\n", encoding="utf-8")

    print(f"{destino.name} escrito, {destino.stat().st_size // 1024} KB")
    print(f"  A: {COLS_A}x{LINHAS_A} = {COLS_A * LINHAS_A} quadrados, "
          f"{len(VERMELHOS_A)} de perda")
    print(f"  B: {COLS_B}x{LINHAS_B} = {COLS_B * LINHAS_B} quadrados, "
          f"{len(VERMELHOS_B)} de perda")
    print(f"  proporcao real {PERDAS_2025 / ELEGIVEIS_2025 * 100:.2f}%  ·  "
          f"na malha A {len(VERMELHOS_A) / (COLS_A * LINHAS_A) * 100:.2f}%  ·  "
          f"na malha B {len(VERMELHOS_B) / (COLS_B * LINHAS_B) * 100:.2f}%")
    print(f"  cada quadrado da A representa {por_quadrado} incidentes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
