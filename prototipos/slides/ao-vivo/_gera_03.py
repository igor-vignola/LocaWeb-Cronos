# -*- coding: utf-8 -*-
"""Gera blocos/03-desafio.html, o slide 3 do deck da banca.

Um assunto só: a quebra é raríssima, e é essa raridade que torna a previsão
difícil. Os números 42 e 196 são o slide 2; aqui o assunto é a proporção deles
dentro da base e a consequência disso para a modelagem.

    A   a malha de 400 quadrados domina, a consequência entra embaixo
    B   a consequência é o objeto dominante, a malha apoia ao lado

Nasce de script porque são 400 elementos por variação, e a onda de entrada usa
o índice de cada quadrado como atraso.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_gera_03.py
"""
from __future__ import annotations

from pathlib import Path

AQUI = Path(__file__).parent

COLS_A, LINHAS_A = 40, 10
COLS_B, LINHAS_B = 20, 20
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
   modelagem. Os números 42 e 196 ficaram no slide 2, de propósito: dividir em
   dois slides limpos vale mais que juntar num amontoado.

   A malha existe para a proporção ser VISTA, não lida. Quatro quadrados
   vermelhos em 400 é 1%; a proporção real é 0,95%, e a legenda diz quantos
   incidentes cada quadrado representa para o arredondamento ficar explícito.

   A consequência é o coração do slide, e está escrita em registro acadêmico:
   um classificador que respondesse sempre "não quebra" acertaria 99% dos casos.
   É por isso que acurácia não serve como métrica aqui.
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

.dsf .leg{display:flex;align-items:center;gap:26px;font-size:13.5px;
  color:var(--tx2)}
.dsf .leg span{display:inline-flex;align-items:center;gap:8px}
.dsf .leg i{width:13px;height:13px;border-radius:3px;background:#E3E9F2;
  flex-shrink:0}
.dsf .leg i.perda{background:var(--bad)}
.dsf .leg b{color:var(--head);font-weight:700}

/* a consequência: a razão pela qual este slide existe */
.dsf .conseq{display:flex;align-items:flex-start;gap:16px;padding:22px 26px;
  background:var(--accent-l);border-radius:14px}
.dsf .conseq .ic{width:22px;height:22px;color:var(--accent);margin-top:3px;
  flex-shrink:0}
.dsf .conseq p{font-size:17px;line-height:1.5;color:var(--tx)}
.dsf .conseq p b{color:var(--head);font-weight:700}
.dsf .conseq .arg{display:block;margin-top:9px;font-size:15.5px;color:var(--tx2)}
.dsf .conseq .arg b{color:var(--head)}

/* ── variação A · malha larga em cima, consequência em faixa embaixo ── */
.ds-a .cena{flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:34px;margin-top:12px;min-height:0}
.ds-a .quadro{padding:34px 34px 26px;display:flex;flex-direction:column;
  align-items:center;gap:20px}
.ds-a .malha{grid-template-columns:repeat(40,24px);gap:7px}
.ds-a .qd{width:24px;height:24px;border-radius:5px}
.ds-a .conseq{width:1030px}

/* ── variação B · a consequência domina à esquerda, malha quadrada à direita ── */
.ds-b .cena{flex:1;display:flex;align-items:center;gap:56px;margin-top:12px;
  min-height:0}
.ds-b .lado{flex:1;min-width:0;display:flex;flex-direction:column;gap:26px}
.ds-b .taxa{display:flex;align-items:baseline;gap:16px}
.ds-b .taxa .v{font-size:126px;font-weight:900;letter-spacing:-5px;line-height:.86;
  color:var(--bad);font-variant-numeric:tabular-nums}
.ds-b .taxa .k{font-size:17px;line-height:1.4;color:var(--tx);max-width:250px}
.ds-b .taxa .k b{color:var(--head);font-weight:700}
.ds-b .conseq{background:transparent;padding:0;border-top:1px solid #DCE4EF;
  padding-top:24px}
.ds-b .quadro{flex-shrink:0;padding:30px;display:flex;flex-direction:column;
  align-items:center;gap:18px}
.ds-b .malha{grid-template-columns:repeat(20,26px);gap:6px}
.ds-b .qd{width:26px;height:26px;border-radius:5px}
.ds-b .leg{flex-direction:column;align-items:flex-start;gap:9px;font-size:13px}
</style>"""

CONSEQ = (
    '<div class="conseq rv" style="--d:{d}ms">\n'
    '        <svg class="ic" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.4"/>'
    '<path d="M12 7.6v4.8"/><path d="M12 16.2h.01"/></svg>\n'
    "        <p>Um classificador que respondesse <b>não quebra</b> para todos os "
    "incidentes acertaria <b>99% dos casos</b>.\n"
    '          <span class="arg">É por isso que <b>acurácia não serve</b> como '
    "métrica aqui, e a avaliação do modelo de risco usa a métrica do evento "
    "raro.</span>\n"
    "        </p>\n"
    "      </div>"
)


def main() -> int:
    por_quadrado = ELEGIVEIS // (COLS_A * LINHAS_A)
    taxa = PERDAS / ELEGIVEIS * 100

    legenda = (
        '<div class="leg rv" style="--d:{d}ms">\n'
        f'          <span><i></i>Cada quadrado representa <b>{por_quadrado} '
        "incidentes</b></span>\n"
        f'          <span><i class="perda"></i>As <b>{PERDAS} quebras</b> são '
        f"<b>{taxa:.2f}%".replace(".", ",") + "</b> da base</span>\n"
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
        '      <div class="quadro cartao rv3" style="--d:620ms">\n'
        f"        {malha(COLS_A, LINHAS_A, VERMELHOS_A, 780)}\n"
        f"        {legenda.format(d=2100)}\n"
        "      </div>\n"
        f"      {CONSEQ.format(d=2400)}\n"
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
        '      <div class="lado">\n'
        '        <div class="taxa rv3" style="--d:640ms">\n'
        '          <span class="v"><span class="ct" data-to="0,95" data-dec="2" '
        'data-delay="860">0,00</span>%</span>\n'
        '          <span class="k">dos incidentes elegíveis ao KPI '
        "<b>passaram do prazo</b> em 2025</span>\n"
        "        </div>\n"
        f"        {CONSEQ.format(d=1500)}\n"
        "      </div>\n"
        '      <div class="quadro cartao rv3" style="--d:900ms">\n'
        f"        {malha(COLS_B, LINHAS_B, VERMELHOS_B, 1060)}\n"
        f"        {legenda.format(d=2400)}\n"
        "      </div>\n"
        "    </div>\n"
        "  </div>\n"
        '  <div class="ft"></div>\n'
        "</section>"
    )

    destino = AQUI / "blocos" / "03-desafio.html"
    destino.write_text(CSS + "\n\n" + a + "\n\n" + b + "\n", encoding="utf-8")

    print(f"{destino.name} escrito, {destino.stat().st_size // 1024} KB")
    print(f"  A: {COLS_A}x{LINHAS_A} quadrados  ·  B: {COLS_B}x{LINHAS_B}")
    print(f"  proporção real {taxa:.2f}%  ·  na malha {len(VERMELHOS_A)}/400 = "
          f"{len(VERMELHOS_A) / 400 * 100:.2f}%")
    print(f"  cada quadrado representa {por_quadrado} incidentes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
