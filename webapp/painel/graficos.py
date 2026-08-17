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
    """Serie diaria: o medido em traco cheio, o previsto pontilhado com a banda.

    E o unico desenho da aba Previsao que existe no relogio da tela: passado ate 30/09 de um
    lado, previsao do modelo do outro, emendados no corte. A faixa acompanha so o lado previsto,
    porque incerteza e propriedade da previsao — o que ja aconteceu nao tem intervalo.

    `marcas` e `rotulos` sao opcionais para quem usa o desenho pequeno, e necessarios quando ele
    vira grafico de pagina: sem eixo, o leitor ve a forma e nao consegue ler a altura.
    """
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
    # o eixo vertical em tres alturas redondas dentro da faixa de valores
    passo = max(10, round((hi - lo) / 2 / 10) * 10)
    marcas = [{'v': int(v), 'y': cd(py(v))}
              for v in (round(lo / 10) * 10 + passo * k for k in range(3)) if lo <= v <= hi]
    # um rotulo de data a cada cinco dias, e tres do lado previsto. O realizado vem do pacote
    # so com `dia` em ISO — o `dm` e montado aqui em vez de engordar o JSON com um campo que
    # so serve ao eixo.
    dm = lambda d: f'{d[8:10]}/{d[5:7]}'
    rot = [{'x': cd(px(i)), 'rot': dm(real[i]['dia']), 'fut': False}
           for i in range(0, len(real), 5)]
    rot += [{'x': cd(px(len(real) + i)), 'rot': dm(fut[i]['dia']), 'fut': True}
            for i in range(0, len(fut), max(1, len(fut) // 3))]

    return {
        'w': w, 'h': h, 'linha': _suave(pr), 'futuro': _suave(pf), 'banda': banda,
        'area': _suave(pr) + f' L{corte[0]:.1f} {h} L6 {h} Z',
        'cx': cd(corte[0]), 'cy': cd(corte[1]),
        'corte_pc': cd(corte[0] / w * 100),
        'px_hoje': cd(pf[1][0] / w * 100), 'py_hoje': cd((pf[1][1] - 40) / h * 100),
        'ini': real[0]['dia'], 'fim': fut[-1]['dia'],
        'marcas': marcas, 'rotulos': rot, 'y_fim': h - 22,
        # o campo do que ainda nao aconteceu, tingido: separa passado de aposta sem legenda
        'fut_x': cd(corte[0]), 'fut_w': cd(w - corte[0]),
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

    # a area sob o realizado da peso ao que ja aconteceu. Sem ela, as duas curvas tem o mesmo
    # peso visual e o dia parece nao ter comecado.
    base_y = py(0)
    area = (_suave(p_real) + f' L{p_real[-1][0]:.1f} {base_y:.1f} L{p_real[0][0]:.1f} '
            f'{base_y:.1f} Z') if len(p_real) > 1 else ''

    return {
        'w': w, 'h': h, 'esperado': _suave(p_esp), 'realizado': _suave(p_real), 'banda': banda,
        'area': area,
        'ax': cd(px(ag)), 'ay': cd(py(realizado[-1]) if realizado else py(0)),
        'ey': cd(py(ac['esperado_agora'])), 'y_fim': h - 26, 'marcas': marcas,
        # onde a curva prevista termina: o ponto de fechamento do dia, que ganha rotulo
        'fx': cd(p_esp[-1][0]), 'fy': cd(p_esp[-1][1]),
        # o futuro comeca no agora. Tingir essa faixa e o que separa, sem legenda, o que
        # aconteceu do que o modelo esta apostando.
        'fut_x': cd(px(ag)), 'fut_w': cd(px(23) - px(ag)),
        'topo': cd(py(teto)),
        # a hora do corte, para a leitura poder marcar "agora" em vez de exigir que o leitor
        # compare a posicao dela com a vertical
        'agora': ag,
        # as 24 horas em coordenada e valor, para o cursor poder ler o grafico. Sem isto o
        # desenho e uma foto: o leitor ve a forma e nao consegue perguntar "quanto era as 11h?".
        # `real` vem None nas horas que ainda nao aconteceram — a leitura tem de dizer isso em
        # vez de mostrar zero.
        'pontos': [{'h': i, 'x': round(px(i), 1), 'ye': round(py(esperado[i]), 1),
                    'yr': round(py(realizado[i]), 1) if i < len(realizado) else None,
                    'esp': round(esperado[i], 1),
                    'real': realizado[i] if i < len(realizado) else None,
                    # a faixa de 80% na altura daquela hora, escalada pela mesma curva de
                    # chegada. Sem ela a leitura mostra a distancia entre as duas curvas sem
                    # regua nenhuma — e 3 de diferenca as 6h nao vale o mesmo que as 18h.
                    'bx': round(ac['baixo'] * frac[i], 1),
                    'at': round(ac['alto'] * frac[i], 1),
                    # o que entrou DENTRO da hora. A curva e acumulada e esconde o ritmo: entre
                    # 09h e 10h ela sobe parecido tendo entrado 2 ou 9.
                    'nah': ((realizado[i] - realizado[i - 1]) if i else realizado[i])
                           if i < len(realizado) else None}
                   for i in range(24)],
        'rotulos': [{'h': hh, 'rot': f'{hh:02d}h', 'x': cd(px(hh))}
                    for hh in (0, 3, 6, 9, 12, 15, 18, 21, 23)],
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


def consumo_meta(p):
    """O ano contra o teto, em tres elementos: o que ja teve, o teto, e onde o ano fecha.

    Tres desenhos ja falharam aqui, cada um por um motivo diferente, e vale registrar para nao
    voltar:

    1. escala de 0 a 1,35x o teto com a projecao preenchida — o estouro do P3 e 8 em 200, ou 3%
       da largura, e ninguem achava onde a barra terminava.
    2. a faixa de 80% inteira com o teto cortando ela — legivel, mas respondia "onde a projecao
       cai" quando a pergunta e "o teto ja estourou?".
    3. as tres parcelas somadas (realizado, risco da fila, volume que entra) com a faixa como
       bigode fino embaixo — a soma ficou clara e a FAIXA sumiu: um traco de 3px nao se anuncia
       como sendo o intervalo em que o ano vai cair.

    Agora sao tres elementos, um por pergunta, e nenhum e fino: barra escura para o que ja teve,
    marca vertical para o teto, e um BLOCO para o intervalo, com a projecao central marcada
    dentro dele. As parcelas intermediarias sairam — separar "risco da fila aberta" de "volume
    que ainda entra" e detalhe de notebook, e a aba Projecao existe para isso.

    A escala vai de zero ate a ponta alta do intervalo ou o teto, o que for maior, com 6% de
    folga para o rotulo da ponta caber. Deslocamentos ja vem em porcentagem somada, porque
    template nao soma.
    """
    esc = max(p['alto'], p['meta']) * 1.06
    pc = lambda v: v / esc * 100
    return {
        'ja_pc': cd(pc(p['ja'])),
        'baixo_x': cd(pc(p['baixo'])), 'faixa_pc': cd(pc(p['alto'] - p['baixo'])),
        'proj_x': cd(pc(p['projecao'])), 'meta_x': cd(pc(p['meta'])),
        # a projecao central em porcentagem DENTRO do bloco do intervalo, para a marca poder ser
        # posicionada relativa a ele e nao a barra toda
        'proj_na_faixa': cd((p['projecao'] - p['baixo']) / ((p['alto'] - p['baixo']) or 1) * 100),
        # quanto do teto ainda nao foi gasto. Negativo significa teto ja rompido no corte.
        'sobra': round(p['meta'] - p['ja'], 1),
        'rompido': p['ja'] >= p['meta'],
        # o tom do cartao inteiro: verde quando o ano fecha dentro, ambar quando passa
        'tom': 'ok' if p['projecao'] <= p['meta'] else 'wn',
    }


def arco_meta(p, w=560):
    """Geometria da projecao contra a meta, em duas escalas.

    A escala de 0 a 1,35x a meta (`*_pc`) diz o TAMANHO do numero e serve a aba Projecao,
    que fala do ano inteiro.

    A escala da propria faixa (`*_faixa_pc`) diz a DECISAO, e e a que vale no cartao e no
    brief: mapeia baixo..alto de 0 a 100% e devolve onde a meta corta esse intervalo. Na
    escala absoluta o excesso do P3 e 8 em 200 — 3% da largura, invisivel; na escala da
    faixa a meta cai a 27% dela, e da para ver que a maior parte do intervalo esta acima.

    A meta e recortada nas pontas: se ela cai fora do intervalo, a faixa inteira esta de um
    lado so, e ai a barra fica de uma cor unica em vez de vazar o desenho.
    """
    esc = p['meta'] * 1.35
    faixa = (p['alto'] - p['baixo']) or 1
    corta = min(100.0, max(0.0, (p['meta'] - p['baixo']) / faixa * 100))
    ponto = min(100.0, max(0.0, (p['projecao'] - p['baixo']) / faixa * 100))
    return {'baixo_pc': cd(p['baixo'] / esc * 100),
            'largura_pc': cd((p['alto'] - p['baixo']) / esc * 100),
            'proj_pc': cd(p['projecao'] / esc * 100),
            'meta_pc': cd(p['meta'] / esc * 100),
            'meta_faixa_pc': cd(corta),
            'proj_faixa_pc': cd(ponto)}
