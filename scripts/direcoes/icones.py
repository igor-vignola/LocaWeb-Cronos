# -*- coding: utf-8 -*-
"""Biblioteca de icones do dominio, inline em SVG.

Desenhados no mesmo grid de 24 com traco 1.7 e ponta arredondada, para nao parecer
conjunto de biblioteca generica. Falam de operacao: prazo, ativo, fila, escalada,
sazonalidade, produto. Sem emoji.
Uso: ico('prazo') para o glifo, chip('prazo', 'no') para o glifo em recipiente tingido."""

G = {
    # tempo e prazo
    'prazo': '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.6 1.6"/><path d="M9 3h6"/>',
    'relogio': '<circle cx="12" cy="12" r="8.4"/><path d="M12 7.6V12l3 1.9"/>',
    'calendario': ('<rect x="3.4" y="5.4" width="17.2" height="15.2" rx="3"/>'
                   '<path d="M3.4 10.4h17.2M8.4 3.4v4M15.6 3.4v4"/>'),
    'agora': '<path d="M12 3.6v3M12 17.4v3M3.6 12h3M17.4 12h3"/><circle cx="12" cy="12" r="3.4"/>',
    # infraestrutura
    'ativo': ('<rect x="3.2" y="4.4" width="17.6" height="6.2" rx="2.2"/>'
              '<rect x="3.2" y="13.4" width="17.6" height="6.2" rx="2.2"/>'
              '<path d="M6.8 7.5h.01M6.8 16.5h.01"/>'),
    'servidor': ('<rect x="4.4" y="3.4" width="15.2" height="17.2" rx="2.6"/>'
                 '<path d="M8 7.6h8M8 12h8M8 16.4h4"/>'),
    'rede': ('<circle cx="12" cy="5.2" r="2.4"/><circle cx="5.4" cy="18.4" r="2.4"/>'
             '<circle cx="18.6" cy="18.4" r="2.4"/>'
             '<path d="M10.4 7.1L6.8 16.4M13.6 7.1l3.6 9.3M7.8 18.4h8.4"/>'),
    'disco': ('<ellipse cx="12" cy="6.6" rx="7.8" ry="3.2"/>'
              '<path d="M4.2 6.6v10.8c0 1.8 3.5 3.2 7.8 3.2s7.8-1.4 7.8-3.2V6.6"/>'
              '<path d="M4.2 12c0 1.8 3.5 3.2 7.8 3.2s7.8-1.4 7.8-3.2"/>'),
    'produto': ('<path d="M12 3.2l8 4.2v9.2l-8 4.2-8-4.2V7.4z"/>'
                '<path d="M4 7.4l8 4.2 8-4.2M12 11.6v8.4"/>'),
    # risco e alerta
    'alerta': ('<path d="M12 3.8l8.8 15.4H3.2z"/><path d="M12 10v3.8"/>'
               '<circle cx="12" cy="16.8" r=".9" fill="currentColor" stroke="none"/>'),
    'escudo': '<path d="M12 3.4l7.4 2.8v5.6c0 4.4-3.1 7.4-7.4 8.8-4.3-1.4-7.4-4.4-7.4-8.8V6.2z"/>',
    'escudo_ok': ('<path d="M12 3.4l7.4 2.8v5.6c0 4.4-3.1 7.4-7.4 8.8-4.3-1.4-7.4-4.4-7.4-8.8V6.2z"/>'
                  '<path d="M8.8 11.8l2.4 2.4 4-4.4"/>'),
    'raio': '<path d="M13.4 2.8L5.6 13.6h4.8l-1.4 7.6 8-11.2h-4.8z"/>',
    'alvo': ('<circle cx="12" cy="12" r="8.4"/><circle cx="12" cy="12" r="4.2"/>'
             '<circle cx="12" cy="12" r="1.1" fill="currentColor" stroke="none"/>'),
    # fluxo de trabalho
    'fila': ('<path d="M4 6.4h16M4 12h11M4 17.6h7"/>'
             '<circle cx="19" cy="17.6" r="1.9"/>'),
    'entrada': '<path d="M4 12h11"/><path d="M11 8l4 4-4 4"/><path d="M19 4.6v14.8"/>',
    'resolvido': '<circle cx="12" cy="12" r="8.4"/><path d="M8.4 12.2l2.6 2.6 4.6-5"/>',
    'pessoas': ('<circle cx="9.2" cy="8.6" r="3.2"/>'
                '<path d="M3.6 20c0-3.1 2.5-5.6 5.6-5.6s5.6 2.5 5.6 5.6"/>'
                '<path d="M16.4 6.2a3.2 3.2 0 0 1 0 6.2M17.4 14.8c1.8.7 3 2.4 3 4.4"/>'),
    # analise
    'tendencia': '<path d="M3.4 17.2l5.4-5.4 3.8 3 6.2-8"/><path d="M14.8 6.8h4.6v4.6"/>',
    'previsao': ('<path d="M3.4 15.4l4.6-4.2 3.4 2.4"/><path d="M11.4 13.6l3-3.6"/>'
                 '<path d="M15.4 9.4l5.2 1.2M20.6 10.6l-1.4 5"/>'),
    'balanca': ('<path d="M12 4.2v15.6M6.6 19.8h10.8"/><path d="M4 8.6h16"/>'
                '<path d="M4 8.6l-2.4 4.6h4.8zM20 8.6l-2.4 4.6h4.8z"/>'),
    'lupa': '<circle cx="10.8" cy="10.8" r="6.4"/><path d="M15.4 15.4l4.8 4.8"/>',
    'grade': ('<rect x="3.6" y="3.6" width="7" height="7" rx="2"/>'
              '<rect x="13.4" y="3.6" width="7" height="7" rx="2"/>'
              '<rect x="3.6" y="13.4" width="7" height="7" rx="2"/>'
              '<rect x="13.4" y="13.4" width="7" height="7" rx="2"/>'),
    'coracao': '<path d="M12 20.2S4.8 15.4 4.8 10.4A4.1 4.1 0 0 1 12 7.8a4.1 4.1 0 0 1 7.2 2.6c0 5-7.2 9.8-7.2 9.8z"/>',
    'seta': '<path d="M5 12h13"/><path d="M13 6.4l6 5.6-6 5.6"/>',
    'fechar': '<path d="M6.4 6.4l11.2 11.2M17.6 6.4L6.4 17.6"/>',
    'sino': ('<path d="M6 9.4a6 6 0 0 1 12 0c0 4.8 2 5.8 2 5.8H4s2-1 2-5.8z"/>'
             '<path d="M10.2 19.4a2.3 2.3 0 0 0 3.6 0"/>'),
    # o brief e das 7h: sol diz a hora do dia, sino so diria que algo apitou
    'sol': ('<circle cx="12" cy="12" r="4.3"/>'
            '<path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4"/>'
            '<path d="M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M18.5 5.5l-1.7 1.7'
            'M7.2 16.8l-1.7 1.7"/>'),
    'novo': ('<path d="M12 3.4v4.2M12 16.4v4.2M4.6 12h4.2M15.2 12h4.2"/>'
             '<path d="M6.8 6.8l3 3M14.2 14.2l3 3M17.2 6.8l-3 3M9.8 14.2l-3 3"/>'),
}


def ico(nome, tam=19, extra=''):
    return (f'<svg class="ic {extra}" viewBox="0 0 24 24" width="{tam}" height="{tam}" '
            f'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{G[nome]}</svg>')


def chip(nome, tom='ac', tam=18):
    """Glifo em recipiente tingido, no espirito de treino-linhas-icone."""
    return f'<span class="chp t-{tom}">{ico(nome, tam)}</span>'


CSS_ICO = """
.ic{flex-shrink:0}
.chp{width:34px;height:34px;border-radius:11px;display:grid;place-items:center;flex-shrink:0}
.chp.t-ac{background:rgba(37,99,235,.15);color:#5B93FF}
.chp.t-no{background:rgba(220,38,38,.15);color:#FF7D74}
.chp.t-wn{background:rgba(217,119,6,.16);color:#F5B champion}
.chp.t-ok{background:rgba(5,150,105,.15);color:#3FD69B}
.chp.t-nt{background:rgba(255,255,255,.07);color:#95A0B4}
.chp.lg{width:42px;height:42px;border-radius:13px}
""".replace('#F5B champion', '#F5B45C')

CSS_ICO_CLARO = """
.ic{flex-shrink:0}
.chp{width:34px;height:34px;border-radius:11px;display:grid;place-items:center;flex-shrink:0}
.chp.t-ac{background:#EFF6FF;color:#2563EB}
.chp.t-no{background:#FEF2F2;color:#DC2626}
.chp.t-wn{background:#FFFBEB;color:#B45309}
.chp.t-ok{background:#ECFDF5;color:#059669}
.chp.t-nt{background:#F2F4F7;color:#6B7688}
.chp.lg{width:42px;height:42px;border-radius:13px}
"""

if __name__ == '__main__':
    print(f'{len(G)} ícones: {", ".join(sorted(G))}')
