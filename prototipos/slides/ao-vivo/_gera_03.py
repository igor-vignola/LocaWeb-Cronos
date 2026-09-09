# -*- coding: utf-8 -*-
"""Gera blocos/03-desafio.html, o slide 3 do deck da banca.

Um assunto só: a quebra é raríssima, e é essa raridade que torna a previsão
difícil. Os números 42 e 196 são o slide 2.

O slide tem dois batimentos, e nenhum deles mora dentro de caixa:

    238    as quebras, contra 25.156 incidentes elegíveis
    99%    o que um classificador que respondesse "não quebra" acertaria

O painel azul de texto que existia aqui foi removido: caixa colorida com
parágrafo dentro é o molde sem graça, e o dono do projeto reprovou. Os dois
números carregam o slide, e a frase que os liga é tipografia, não painel.

    A   os dois números na coluna da esquerda, malha larga à direita
    B   malha larga em cima, os dois números lado a lado embaixo

Nasce de script porque são 400 elementos por variação, e a onda de entrada usa
o índice de cada quadrado como atraso.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_gera_03.py
"""
from __future__ import annotations

from pathlib import Path

AQUI = Path(__file__).parent

COLS_A, LINHAS_A = 25, 16
COLS_B, LINHAS_B = 40, 10
VERMELHOS_A = (57, 148, 263, 331)
VERMELHOS_B = (46, 137, 258, 341)

PERDAS = 238
ELEGIVEIS = 25156

LOGO = (
    '<div class="bi"><svg viewBox="0 0 28 28" fill="none">'
    '<path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="22" cy="8" r="3" stroke="#3B82F6" stroke-width="1.5"/>'
    '<circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg></div>'
)


def cabecalho() -> str:
    return (
        '  <div class="mesh"></div><div class="grid-bg"></div>\n'
        '  <div class="hd">\n'
        f"    {LOGO}\n"
        '    <div class="bn">Cronos</div>'
        '<span class="bt">BANCA FINAL &middot; 15/09/2026</span>\n'
        '    <div class="tag">Base elegível ao KPI &middot; 2025</div>\n'
        "  </div>"
    )


def malha(cols: int, linhas: int, vermelhos: tuple[int, ...], base: int) -> str:
    qd = "".join(
        f'<i class="qd{" perda" if i in vermelhos else ""}" style="--i:{i}"></i>'
        for i in range(cols * linhas)
    )
    return f'<div class="malha" style="--base:{base}ms">{qd}</div>'


CSS = """<style>
/* ═══ slide 3 · o desafio da previsão ════════════════════════════════════════
   Um assunto só: a quebra é raríssima, e essa raridade é o problema de
   modelagem. Os números 42 e 196 ficaram no slide 2, de propósito.

   Dois batimentos, nenhum dentro de caixa: o 238 das quebras e o 99% que um
   classificador burro acertaria. O painel azul com parágrafo dentro que existia
   aqui saiu por ser o molde sem graça.

   A malha existe para a proporção ser VISTA, não lida. Quatro quadrados
   vermelhos em 400 é 1%; a proporção real é 0,95%, e a legenda diz quantos
   incidentes cada quadrado representa para o arredondamento ficar explícito.
   ══════════════════════════════════════════════════════════════════════════ */
.dsf .body{padding-top:14px}
.dsf .tt{font-size:52px;letter-spacing:-1.9px}

.dsf .malha{display:grid}
.dsf .qd{background:#E3E9F2;opacity:0;transform:scale(.4)}
.dsf.is-active .malha .qd{animation:dsfEntra .34s var(--out) forwards;
  animation-delay:calc(var(--base) + var(--i) * 2.1ms)}
@keyframes dsfEntra{to{opacity:1;transform:scale(1)}}
.dsf .qd.perda{background:var(--bad)}
.dsf.is-active .malha .qd.perda{
  animation:dsfEntra .34s var(--out) forwards, dsfPerda .52s var(--spring) forwards;
  animation-delay:calc(var(--base) + var(--i) * 2.1ms), calc(var(--base) + 1180ms)}
@keyframes dsfPerda{0%{transform:scale(1)}44%{transform:scale(1.8)}
  100%{transform:scale(1)}}

.dsf .leg{display:flex;align-items:center;gap:9px;font-size:13px;color:var(--tx2)}
.dsf .leg i{width:13px;height:13px;border-radius:3px;background:#E3E9F2;
  flex-shrink:0}
.dsf .leg b{color:var(--head);font-weight:700}

/* ── os dois batimentos: número grande e rótulo ao lado, sem caixa ── */
.dsf .bat{display:flex;align-items:baseline;gap:20px}
.dsf .bat .v{font-weight:900;line-height:.84;font-variant-numeric:tabular-nums}
.dsf .bat .k{font-size:16.5px;line-height:1.42;color:var(--tx)}
.dsf .bat .k b{color:var(--head);font-weight:700}
.dsf .bat.qb .v{color:var(--bad)}
.dsf .bat.ac .v{color:var(--head)}
.dsf .risca{height:1px;background:#DCE4EF}

/* ── variação A · os dois números à esquerda, malha alta à direita ── */
.ds-a .cena{flex:1;display:flex;align-items:center;gap:60px;margin-top:10px;
  min-height:0}
.ds-a .lado{flex:1;min-width:0;display:flex;flex-direction:column;gap:30px}
.ds-a .bat .v{font-size:132px;letter-spacing:-5.4px}
.ds-a .bat .k{max-width:290px}
.ds-a .quadro{flex-shrink:0;padding:28px;display:flex;flex-direction:column;
  align-items:center;gap:18px}
.ds-a .malha{grid-template-columns:repeat(25,25px);gap:6px}
.ds-a .qd{width:25px;height:25px;border-radius:5px}

/* ── variação B · malha larga em cima, os dois números lado a lado embaixo ── */
.ds-b .cena{flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:38px;margin-top:8px;min-height:0}
.ds-b .quadro{padding:30px 34px 24px;display:flex;flex-direction:column;
  align-items:center;gap:18px}
.ds-b .malha{grid-template-columns:repeat(40,23px);gap:7px}
.ds-b .qd{width:23px;height:23px;border-radius:5px}
.ds-b .dupla{display:flex;align-items:stretch;gap:60px;width:1120px}
.ds-b .bat{flex:1}
.ds-b .bat .v{font-size:104px;letter-spacing:-4.2px}
.ds-b .vfio{width:1px;background:linear-gradient(180deg,transparent,#D9E1EC 18%,
  #D9E1EC 82%,transparent)}
</style>"""


def main() -> int:
    por_quadrado = ELEGIVEIS // (COLS_B * LINHAS_B)
    taxa = f"{PERDAS / ELEGIVEIS * 100:.2f}".replace(".", ",")

    legenda = (
        '<div class="leg rv" style="--d:{d}ms">\n'
        f'          <i></i>Cada quadrado representa <b>{por_quadrado} '
        f"incidentes</b>. As <b>{PERDAS} quebras</b> s&atilde;o "
        f"<b>{taxa}%</b> da base.\n"
        "        </div>"
    )

    bat_quebras = (
        '<div class="bat qb rv3" style="--d:{d}ms">\n'
        '          <span class="v"><span class="ct" data-to="238" '
        'data-delay="{c}">0</span></span>\n'
        '          <span class="k">incidentes <b>passaram do prazo</b> em 2025, '
        f"de <b>{ELEGIVEIS:,}</b> eleg&iacute;veis ao KPI</span>\n".replace(",", ".")
        + "        </div>"
    )

    bat_acuracia = (
        '<div class="bat ac rv3" style="--d:{d}ms">\n'
        '          <span class="v"><span class="ct" data-to="99" '
        'data-delay="{c}">0</span>%</span>\n'
        '          <span class="k">&eacute; o que um classificador acertaria '
        "respondendo <b>n&atilde;o quebra</b> para todos. Por isso "
        "<b>acur&aacute;cia n&atilde;o serve</b> como m&eacute;trica aqui.</span>\n"
        "        </div>"
    )

    a = (
        '<section class="slide light dsf ds-a" data-slide="3" data-var="a" '
        'data-quem="igor">\n'
        + cabecalho()
        + '\n  <div class="body">\n'
        '    <span class="eb"><span class="rv" style="--d:240ms">A raridade do '
        "evento</span></span>\n"
        '    <h1 class="tt"><span class="mask" style="--d:340ms">'
        "<span>O desafio da previsão</span></span></h1>\n"
        '    <div class="cena">\n'
        '      <div class="lado">\n'
        f"        {bat_quebras.format(d=640, c=880)}\n"
        '        <i class="risca rv" style="--d:1500ms"></i>\n'
        f"        {bat_acuracia.format(d=1680, c=1900)}\n"
        "      </div>\n"
        '      <div class="quadro cartao rv3" style="--d:820ms">\n'
        f"        {malha(COLS_A, LINHAS_A, VERMELHOS_A, 980)}\n"
        f"        {legenda.format(d=2320)}\n"
        "      </div>\n"
        "    </div>\n"
        "  </div>\n"
        '  <div class="ft"></div>\n'
        "</section>"
    )

    b = (
        '<section class="slide light dsf ds-b" data-slide="3" data-var="b" '
        'data-quem="igor">\n'
        + cabecalho()
        + '\n  <div class="body">\n'
        '    <span class="eb"><span class="rv" style="--d:240ms">A raridade do '
        "evento</span></span>\n"
        '    <h1 class="tt"><span class="mask" style="--d:340ms">'
        "<span>O desafio da previsão</span></span></h1>\n"
        '    <div class="cena">\n'
        '      <div class="quadro cartao rv3" style="--d:620ms">\n'
        f"        {malha(COLS_B, LINHAS_B, VERMELHOS_B, 780)}\n"
        f"        {legenda.format(d=2100)}\n"
        "      </div>\n"
        '      <div class="dupla">\n'
        f"        {bat_quebras.format(d=2380, c=2560)}\n"
        '        <i class="vfio"></i>\n'
        f"        {bat_acuracia.format(d=2540, c=2720)}\n"
        "      </div>\n"
        "    </div>\n"
        "  </div>\n"
        '  <div class="ft"></div>\n'
        "</section>"
    )

    destino = AQUI / "blocos" / "03-desafio.html"
    destino.write_text(CSS + "\n\n" + a + "\n\n" + b + "\n", encoding="utf-8")

    print(f"{destino.name} escrito, {destino.stat().st_size // 1024} KB")
    print(f"  A: {COLS_A}x{LINHAS_A} = {COLS_A * LINHAS_A} quadrados  ·  "
          f"B: {COLS_B}x{LINHAS_B} = {COLS_B * LINHAS_B}")
    print(f"  proporção real {taxa}%  ·  na malha 4/400 = 1,00%")
    print(f"  cada quadrado representa {por_quadrado} incidentes")
    print("  sem painel azul: os dois números carregam o slide")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
