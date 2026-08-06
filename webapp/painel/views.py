# -*- coding: utf-8 -*-
"""Views do painel.

Cada aba e uma pagina propria com URL propria — dá para mandar o link da fila filtrada
por P2 para alguem. Os detalhes vem como fragmento, para o modal buscar sem recarregar.
"""
from django.http import Http404, JsonResponse
from django.shortcuts import render

from . import graficos as g
from . import servicos as s


def _base(aba):
    p = s.resumo()
    return {'aba': aba, 'p': p, 'hoje': p['hoje'], 'ontem': p['ontem'], 'base': p['base']}


def hoje(req):
    p = s.resumo()
    ac = p['acompanhamento']
    ctx = _base('hoje')
    ctx.update({
        'heroi': g.heroi(p['trilho']['realizado'], p['trilho']['previsto']),
        'faixa': g.faixa_24h(p['horas'], ac['hora_agora']),
        'acomp': g.acompanhamento(ac),
        'ac': ac,
        'fila': s.fila_de_hoje(6),
        'ultimos': p['ultimos_dias'],
        'ativos': sorted(p['ativos'], key=lambda a: -a['taxa'])[:4],
        'piores': sorted(p['saude'], key=lambda x: x['nota'])[:5],
        'projecao': [{**x, **g.arco_meta(x)} for x in p['projecao']],
        'hora_pico': p['hora_pico'], 'hora_risco': p['hora_risco'],
        'calmo': not any(f['risco'] >= 10 for f in s.fila_de_hoje(200)),
        'maior_hoje': max((f['risco'] for f in s.fila_de_hoje(200)), default=0),
    })
    return render(req, 'painel/hoje.html', ctx)


def fila(req):
    pagina = max(1, int(req.GET.get('p', 1) or 1))
    dados = s.fila_pagina(prioridade=req.GET.get('pri', ''), faixa=req.GET.get('faixa', ''),
                          busca=req.GET.get('q', ''), pagina=pagina)
    ctx = _base('fila')
    ctx.update({
        **dados, 'faixas': s.contagem_por_faixa(), 'grupos': s.painel()['grupos'],
        'pri': req.GET.get('pri', ''), 'faixa_sel': req.GET.get('faixa', ''),
        'q': req.GET.get('q', ''),
        'anterior': pagina - 1 if pagina > 1 else 0,
        'proxima': pagina + 1 if pagina < dados['paginas'] else 0,
    })
    return render(req, 'painel/fila.html', ctx)


def saude(req):
    p = s.resumo()
    quad = req.GET.get('quad', '')
    lista = sorted(p['saude'], key=lambda x: x['posicao'])
    if quad:
        lista = [x for x in lista if quad in x['quadrante']]
    ctx = _base('saude')
    ctx.update({'lista': lista, 'quad': quad, 'total': len(p['saude']),
                'latentes': [x for x in p['saude'] if x['quadrante'] == 'risco latente'][:4]})
    return render(req, 'painel/saude.html', ctx)


def causas(req):
    p = s.resumo()
    ctx = _base('causas')
    ctx.update({'causas': p['causas'], 'recorrentes': p['recorrentes']})
    return render(req, 'painel/causas.html', ctx)


def previsao(req):
    p = s.resumo()
    ac = p['acompanhamento']
    ctx = _base('previsao')
    ctx.update({
        'trilho': g.trilho(p['trilho']['realizado'], p['trilho']['previsto'], n_real=30),
        'acomp': g.acompanhamento(ac, h=210), 'ac': ac,
        'proximos': p['trilho']['previsto'][:8],
        'semana': p['semana'], 'max_semana': max(x['media'] for x in p['semana']),
    })
    return render(req, 'painel/previsao.html', ctx)


# ── fragmentos que o modal busca ───────────────────────────────────────────
def det_incidente(req, codigo):
    inc = s.incidente(codigo)
    if not inc:
        raise Http404('incidente não encontrado')
    return render(req, 'painel/_det_incidente.html',
                  {'c': inc, 'base': s.painel()['base'],
                   'hist': g.barras_mes(inc['hist_ativo']), 'meses': s.painel()['meses']})


def det_ativo(req, codigo):
    a = s.ativo(codigo)
    if not a:
        raise Http404('ativo não encontrado')
    return render(req, 'painel/_det_ativo.html',
                  {'a': a, 'base': s.painel()['base'],
                   'hist': g.barras_mes(a['hist']), 'meses': s.painel()['meses']})


def det_produto(req, codigo):
    p = s.produto(codigo)
    if not p:
        raise Http404('produto não encontrado')
    return render(req, 'painel/_det_produto.html', {'p': p, 'total': len(s.painel()['saude'])})


def busca(req):
    return JsonResponse({'itens': s.indice_busca()})
