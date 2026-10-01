# -*- coding: utf-8 -*-
"""Aba Tendências: categoria, produto e item de configuração.

Lê o pacote tendencias.json, gerado por scripts/gera_tendencias_app.py a partir do notebook 08. A tela
responde uma pergunta só: quantos valores existem em cada dimensão e quanto das violações os 10 do
topo reúnem. Tudo até 30/09/2025, o corte da aplicação.
"""
import json
from functools import lru_cache
from pathlib import Path

from django.conf import settings

from .graficos import cd as _cd

DADOS = Path(settings.DADOS_DIR)
ORDEM = ('produto', 'categoria', 'ic')
PLURAL = {'produto': 'produtos', 'categoria': 'categorias', 'ic': 'itens'}
PLURAL_LONGO = {'produto': 'produtos', 'categoria': 'categorias', 'ic': 'itens de configuração'}
ARTIGO = {'produto': 'o', 'categoria': 'a', 'ic': 'o'}
CELULAS = 100          # cada quadrado vale 1% das violações


@lru_cache(maxsize=1)
def pacote():
    return json.loads((DADOS / 'tendencias.json').read_text(encoding='utf-8'))


def tendencias():
    """O contexto da aba: as três dimensões, cada uma com o peso do topo e a lista dos 10."""
    pac = pacote()
    dims = []
    for chave in ORDEM:
        d = pac['dimensoes'][chave]
        itens = [{**x, 'pct': round(100 * x['violacoes'] / d['total_violacoes'], 1)} for x in d['itens']]
        maior = max(i['pct'] for i in itens) or 1
        for i in itens:
            i['barra'] = _cd(100 * i['pct'] / maior)         # a maior barra ocupa a coluna inteira
        azuis = round(d['topo_pct'])
        dims.append({
            'chave': chave, 'rotulo': d['rotulo'], 'plural': PLURAL[chave],
            'plural_longo': PLURAL_LONGO[chave], 'artigo': ARTIGO[chave],
            'valores': d['valores'], 'com_violacao': d['com_violacao'],
            'sem_violacao': d['valores'] - d['com_violacao'],
            'outros_que_violaram': d['com_violacao'] - pac['topo'],
            'topo': pac['topo'], 'topo_pct': d['topo_pct'], 'resto_pct': round(100 - d['topo_pct'], 1),
            'total': d['total_violacoes'],
            # os 100 quadrados: os primeiros são o peso do topo, em ordem de leitura
            'quadrados': ['a'] * azuis + ['c'] * (CELULAS - azuis),
            'itens': itens,
        })
    return {'dims': dims, 'janela_fim': '30/09/2025',
            'violacoes': pac['dimensoes']['produto']['total_violacoes'],
            'viol_p2': pac['violacoes_p2'], 'viol_p3': pac['violacoes_p3']}
