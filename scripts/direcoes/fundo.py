# -*- coding: utf-8 -*-
"""Campo de linhas: o fundo das telas e a historia real da operacao.

Cada curva e a serie diaria de um produto em 2025, suavizada. Nao e ruido decorativo —
sao dezesseis produtos reais desenhando-se devagar. Ideia vinda do Background Paths do
21st.dev, mas alimentada com o proprio dado em vez de caminho aleatorio."""
from dados import CURVAS


def campo(cor='#2563EB', opacidade=.1, altura=1000, largura=1800, n=16):
    """SVG de fundo com as curvas empilhadas em profundidades diferentes."""
    linhas = []
    itens = list(CURVAS.items())[:n]
    faixa = altura / (len(itens) + 1)
    for i, (produto, serie) in enumerate(itens):
        base = faixa * (i + 1)
        amp = faixa * 1.65
        passo = largura / (len(serie) - 1)
        pts = [(j * passo, base - v * amp) for j, v in enumerate(serie)]
        # curva suave em vez de poligonal dura
        d = f'M{pts[0][0]:.0f} {pts[0][1]:.1f}'
        for j in range(1, len(pts)):
            x0, y0 = pts[j - 1]
            x1, y1 = pts[j]
            d += f' C{x0 + passo/2:.0f} {y0:.1f} {x1 - passo/2:.0f} {y1:.1f} {x1:.0f} {y1:.1f}'
        # o que esta mais ao fundo anda mais devagar e mais apagado
        prof = i / max(len(itens) - 1, 1)
        linhas.append(
            f'<path class="cv" d="{d}" style="--o:{opacidade * (1 - prof * .55):.3f};'
            f'--d:{28 + i * 3.5:.0f}s;--x:{-14 - i * 2}px;--t:{i * .22:.2f}s"/>')
    return (f'<svg class="campo" viewBox="0 0 {largura} {altura}" preserveAspectRatio="none" '
            f'aria-hidden="true" style="--cv:{cor}">{"".join(linhas)}</svg>')


CSS_CAMPO = """
.campo{position:fixed;inset:-4% -6%;width:112%;height:108%;z-index:0;pointer-events:none}
.campo .cv{fill:none;stroke:var(--cv);stroke-width:1.4;stroke-linecap:round;opacity:0;
 stroke-dasharray:4200;stroke-dashoffset:4200;
 animation:cvd 2.6s cubic-bezier(.19,1,.22,1) var(--t) forwards,
           cvo .9s ease var(--t) forwards,
           cvm var(--d) ease-in-out infinite alternate}
@keyframes cvd{to{stroke-dashoffset:0}}
@keyframes cvo{to{opacity:var(--o)}}
@keyframes cvm{to{transform:translate3d(var(--x),-6px,0)}}
@media (prefers-reduced-motion:reduce){
 .campo .cv{animation:none;opacity:var(--o);stroke-dashoffset:0}}
"""
