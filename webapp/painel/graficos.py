# -*- coding: utf-8 -*-
"""Geometria dos graficos.

Aqui so se calcula coordenada e caminho SVG. A marcacao fica no template, para o
desenho poder mudar sem mexer em Python e para nao existir HTML dentro de string.
"""


# Coordenada de SVG tem de sair como texto com ponto decimal. O Django localiza numero
# em template conforme LANGUAGE_CODE, e em pt-BR "240.6" vira "240,6" — o que quebra todo
# path e todo rect silenciosamente. Devolver string ja formatada imuniza contra isso.
cd = lambda v: f'{float(v):.1f}'


def _suave(pts):
    """Curva de Bezier horizontal entre pontos: evita a poligonal dura."""
    if len(pts) < 2:
        return ''
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        m = (x0 + x1) / 2
        d += f' C{m:.1f} {y0:.1f} {m:.1f} {y1:.1f} {x1:.1f} {y1:.1f}'
    return d


def trilho(realizado, previsto, w=1000, h=150, n_real=20, n_prev=8):
    """Serie diaria: o medido em traco cheio, o previsto pontilhado com a banda."""
    real = realizado[-n_real:]
    fut = previsto[:n_prev]
    vals = ([r['valor'] for r in real] + [f['valor'] for f in fut]
            + [f['baixo'] for f in fut] + [f['alto'] for f in fut])
    lo, hi = min(vals), max(vals)
    vao = (hi - lo) or 1
    n = len(real) + len(fut)
    px = lambda i: 6 + i / (n - 1) * (w - 12)
    py = lambda v: h - 26 - (v - lo) / vao * (h - 56)

    pr = [(px(i), py(r['valor'])) for i, r in enumerate(real)]
    corte = pr[-1]
    pf = [corte] + [(px(len(real) + i), py(f['valor'])) for i, f in enumerate(fut)]
    altos = [(px(len(real) + i), py(f['alto'])) for i, f in enumerate(fut)]
    baixos = [(px(len(real) + i), py(f['baixo'])) for i, f in enumerate(fut)]
    banda = (f'M{corte[0]:.1f} {corte[1]:.1f} L'
             + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in altos) + ' L'
             + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(baixos)) + ' Z')
    return {
        'w': w, 'h': h, 'linha': _suave(pr), 'futuro': _suave(pf), 'banda': banda,
        'area': _suave(pr) + f' L{corte[0]:.1f} {h} L6 {h} Z',
        'cx': cd(corte[0]), 'cy': cd(corte[1]),
        'corte_pc': cd(corte[0] / w * 100),
        'px_hoje': cd(pf[1][0] / w * 100), 'py_hoje': cd((pf[1][1] - 40) / h * 100),
        'ini': real[0]['dia'], 'fim': fut[-1]['dia'],
    }


def heroi(realizado, previsto, w=380, h=244):
    """A marca em escala: doze pontos suavizados, o no no agora e a previsao saindo dele."""
    jan = realizado[-24:]
    suav = []
    for i in range(len(jan)):
        pedaco = jan[max(0, i - 4):i + 1]
        suav.append(sum(p['valor'] for p in pedaco) / len(pedaco))
    real = [{'dia': jan[i]['dia'], 'valor': suav[i]} for i in range(0, len(jan), 2)]
    fut = previsto[:6]
    vals = ([r['valor'] for r in real] + [f['valor'] for f in fut]
            + [f['baixo'] for f in fut] + [f['alto'] for f in fut])
    lo, hi = min(vals), max(vals)
    vao = (hi - lo) or 1
    n = len(real) + len(fut)
    px = lambda i: 18 + i / (n - 1) * (w - 36)
    py = lambda v: h - 34 - (v - lo) / vao * (h - 78)
    pr = [(px(i), py(r['valor'])) for i, r in enumerate(real)]
    no = pr[-1]
    pf = [no] + [(px(len(real) + i), py(f['valor'])) for i, f in enumerate(fut)]
    altos = [(px(len(real) + i), py(f['alto'])) for i, f in enumerate(fut)]
    baixos = [(px(len(real) + i), py(f['baixo'])) for i, f in enumerate(fut)]
    banda = (f'M{no[0]:.1f} {no[1]:.1f} L'
             + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in altos) + ' L'
             + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(baixos)) + ' Z')
    return {'w': w, 'h': h, 'linha': _suave(pr), 'futuro': _suave(pf), 'banda': banda,
            'nx': cd(no[0]), 'ny': cd(no[1]),
            'ini': real[0]['dia'], 'fim': fut[-1]['dia']}


def faixa_24h(horas, agora=7, w=560, h=132):
    """Uma barra por hora: altura pelo volume, cor pela taxa de violacao."""
    mx = max(x['abertos'] for x in horas) or 1
    lar = (w - 16) / 24
    barras = []
    for x in horas:
        alt = 10 + (h - 56) * x['abertos'] / mx
        barras.append({
            'h': x['h'], 'x': cd(8 + x['h'] * lar + 1.6), 'y': cd(h - 26 - alt),
            'w': cd(lar - 3.2), 'alt': cd(alt), 'abertos': x['abertos'],
            'taxa': x['taxa'],
            'tom': 'no' if x['taxa'] >= 1.6 else ('wn' if x['taxa'] >= 1.1 else 'ok'),
        })
    rotulos = [{'h': f'{hh:02d}h', 'x': cd(8 + hh * lar + lar / 2)}
               for hh in (0, 3, 6, 9, 12, 15, 18, 21)]
    return {'w': w, 'h': h, 'barras': barras, 'rotulos': rotulos,
            'ax': cd(8 + agora * lar + lar / 2), 'y_rot': h - 8, 'y_fim': h - 30}


def acompanhamento(ac, w=560, h=190):
    """Previsto contra realizado ao longo do dia.

    A curva esperada e a distribuicao historica por hora aplicada ao total previsto.
    A realizada para no agora — e o que permite ver, no meio do turno, se o dia esta
    no ritmo."""
    esperado, realizado = ac['esperado'], ac['realizado']
    teto = max(max(esperado), ac['alto'], max(realizado) if realizado else 0) * 1.06
    px = lambda i: 34 + i / 23 * (w - 48)
    py = lambda v: h - 28 - v / teto * (h - 48)
    p_esp = [(px(i), py(v)) for i, v in enumerate(esperado)]
    p_real = [(px(i), py(v)) for i, v in enumerate(realizado)]
    ag = ac['hora_agora']
    # a faixa do dia inteiro, escalada pela mesma curva de chegada
    frac = [e / esperado[-1] if esperado[-1] else 0 for e in esperado]
    altos = [(px(i), py(ac['alto'] * f)) for i, f in enumerate(frac)]
    baixos = [(px(i), py(ac['baixo'] * f)) for i, f in enumerate(frac)]
    banda = ('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in altos) + ' L'
             + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(baixos)) + ' Z')
    marcas = [{'v': int(v), 'y': cd(py(v))}
              for v in (0, round(teto / 2 / 10) * 10, round(teto * .9 / 10) * 10) if v <= teto]
    return {
        'w': w, 'h': h, 'esperado': _suave(p_esp), 'realizado': _suave(p_real), 'banda': banda,
        'ax': cd(px(ag)), 'ay': cd(py(realizado[-1]) if realizado else py(0)),
        'ey': cd(py(ac['esperado_agora'])), 'y_fim': h - 26, 'marcas': marcas,
        'rotulos': [{'h': hh, 'rot': f'{hh:02d}h', 'x': cd(px(hh))}
                    for hh in (0, 6, 12, 18)],
    }


def barras_mes(hist, w=560, h=92):
    """Volume do mes com a fracao que violou por dentro."""
    if not hist:
        return None
    mx = max(m['passagens'] for m in hist) or 1
    lar = w / len(hist)
    return {'w': w, 'h': h, 'barras': [{
        'x': cd(i * lar + 3), 'w': cd(lar - 6),
        'yp': cd(h - 16 - m['passagens'] / mx * (h - 20)),
        'hp': cd(m['passagens'] / mx * (h - 20)),
        'yv': cd(h - 16 - m['violacoes'] / mx * (h - 20)),
        'hv': cd(m['violacoes'] / mx * (h - 20)),
        'cx': cd(i * lar + lar / 2), 'mes': m['mes'],
    } for i, m in enumerate(hist)], 'y_rot': h - 2}


def arco_meta(p, w=560):
    """Barra de intervalo: a projecao e uma faixa, nao um ponto."""
    esc = p['meta'] * 1.35
    return {'baixo_pc': cd(p['baixo'] / esc * 100),
            'largura_pc': cd((p['alto'] - p['baixo']) / esc * 100),
            'proj_pc': cd(p['projecao'] / esc * 100),
            'meta_pc': cd(p['meta'] / esc * 100)}
