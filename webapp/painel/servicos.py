# -*- coding: utf-8 -*-
"""Camada de servico: le o pacote de dados e devolve estrutura pronta para a view.

O conteiner nao treina nada. Prophet e scikit-learn rodam nos notebooks, gravam parquet,
e o script gera_dados_app.py agrega tudo em data/app. Aqui so se abre arquivo.

O pacote e carregado uma vez por processo e fica em memoria: sao 60 kB de JSON e um
parquet de 5.183 linhas, entao nao ha motivo para reler a cada requisicao.
"""
import json
from functools import lru_cache
from pathlib import Path

import pandas as pd
from django.conf import settings

DADOS = Path(settings.DADOS_DIR)

DIAS_SEMANA = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']
FAIXAS = [(10, 1e9, 'crítica', 'no'), (5, 10, 'alta', 'wn'),
          (1, 5, 'atenção', 'wn'), (0, 1, 'rotina', 'ok')]


@lru_cache(maxsize=1)
def painel():
    """O pacote agregado. Tudo que nao e linha da fila esta aqui."""
    return json.loads((DADOS / 'painel.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def fila():
    """A fila pontuada, 5.183 linhas. Os sinais vem como JSON dentro da coluna."""
    df = pd.read_parquet(DADOS / 'fila.parquet')
    df['sinais'] = df['sinais'].map(json.loads)
    df['ativo'] = df['ativo'].replace('None', '')
    df['dm'] = df['dia'].dt.strftime('%d/%m')
    return df


# ── formatacao pt-BR, usada tambem pelos templates via filtro ──────────────
def num(v, casas=1):
    return f'{float(v):.{casas}f}'.replace('.', ',')


def mil(v):
    return f'{int(v):,}'.replace(',', '.')


def faixa_de(risco):
    return next(f for f in FAIXAS if f[0] <= risco < f[1])


# ── consultas que as views usam ────────────────────────────────────────────
def resumo():
    p = painel()
    d = pd.Timestamp(p['hoje']['dia'])
    p['hoje']['dm'] = f'{d.day:02d}/{d.month:02d}'
    p['hoje']['completo'] = f'{d.day:02d}/{d.month:02d}/{d.year}'
    p['hoje']['dia_semana'] = DIAS_SEMANA[d.dayofweek]
    p['hoje']['largura_p3'] = round(p['hoje']['alto_p3'] - p['hoje']['baixo_p3'], 1)
    p['hoje']['largura_p2'] = round(p['hoje']['alto_p2'] - p['hoje']['baixo_p2'], 1)
    for d in p['trilho']['previsto']:
        dd = pd.Timestamp(d['dia'])
        d['dm'] = f'{dd.day:02d}/{dd.month:02d}'
        d['rot'] = DIAS_SEMANA[dd.dayofweek][:3]
        d['largura'] = round(d['alto'] - d['baixo'], 1)
    o = pd.Timestamp(p['ontem']['dia'])
    p['ontem']['dm'] = f'{o.day:02d}/{o.month:02d}'
    return p


def fila_de_hoje(n=6):
    f = fila()
    hoje = f[f['dia'] == pd.Timestamp(painel()['hoje']['dia'])]
    return hoje.head(n).to_dict('records')


def fila_pagina(prioridade='', faixa='', busca='', pagina=1, por_pagina=40):
    """A fila com filtro e paginacao. Devolve tambem o que sobrou, para a tela poder
    dizer 'nenhum caso nesta faixa' em vez de mostrar tabela vazia."""
    f = fila()
    if prioridade:
        f = f[f['prioridade'] == prioridade]
    if faixa:
        lo, hi, _, _ = next(x for x in FAIXAS if str(x[0]) == faixa)
        f = f[(f['risco'] >= lo) & (f['risco'] < hi)]
    if busca:
        b = busca.strip().lower()
        alvo = (f['incidente'].str.lower() + ' ' + f['produto'].str.lower() + ' '
                + f['equipe'].str.lower() + ' ' + f['ativo'].str.lower())
        f = f[alvo.str.contains(b, regex=False)]
    total = len(f)
    ini = (pagina - 1) * por_pagina
    return {'linhas': f.iloc[ini:ini + por_pagina].to_dict('records'), 'total': total,
            'pagina': pagina, 'paginas': max(1, -(-total // por_pagina)),
            'de': ini + 1 if total else 0, 'ate': min(ini + por_pagina, total)}


def contagem_por_faixa():
    f = fila()
    fora = []
    for lo, hi, rot, k in FAIXAS:
        s = f[(f['risco'] >= lo) & (f['risco'] < hi)]
        fora.append({'lo': lo, 'rot': rot, 'k': k, 'n': len(s),
                     'violou': int(s['violou'].sum())})
    return fora


def incidente(codigo):
    f = fila()
    linha = f[f['incidente'] == codigo]
    if linha.empty:
        return None
    r = linha.iloc[0].to_dict()
    r['faixa'], r['ftom'] = faixa_de(r['risco'])[2], faixa_de(r['risco'])[3]
    r['em100'] = round(r['risco'])
    r['vezes'] = round(r['risco'] / painel()['base']['media_violacao'])
    r['hist_ativo'] = next((a['hist'] for a in painel()['ativos']
                            if a['ativo'] == r['ativo']), [])
    return r


def ativo(codigo):
    a = next((x for x in painel()['ativos'] if x['ativo'] == codigo), None)
    if a:
        a = dict(a)
        a['vezes'] = round(a['taxa'] / painel()['base']['media_violacao']) if a['taxa'] else 0
    return a


def produto(nome):
    p = next((x for x in painel()['saude'] if x['produto'] == nome), None)
    if not p:
        return None
    p = dict(p)
    p['componentes'] = [
        {'rot': 'taxa de violação', 'v': num(p['taxa_violacao'] * 100, 2), 'u': '%',
         'pos': round(p['pos_taxa_violacao'] * 100)},
        {'rot': 'problemas inéditos', 'v': num(p['prop_inedito'] * 100, 1), 'u': '%',
         'pos': round(p['pos_prop_inedito'] * 100)},
        {'rot': 'fechados sem causa', 'v': num(p['prop_sem_causa'] * 100, 1), 'u': '%',
         'pos': round(p['pos_prop_sem_causa'] * 100)},
        {'rot': 'duração mediana', 'v': num(p['duracao_mediana_h'], 1), 'u': 'h',
         'pos': round(p['pos_duracao_mediana_h'] * 100)},
        {'rot': 'tendência', 'v': num(p['tendencia'] * 100, 2), 'u': ' p.p.',
         'pos': round(p['pos_tendencia'] * 100)},
    ]
    return p


def indice_busca():
    """O que a paleta de comando indexa."""
    p = painel()
    f = fila().head(150)
    itens = [{'t': 'aba', 'k': k, 'r': r, 's': 'ir para a aba'} for k, r in
             [('hoje', 'Hoje'), ('fila', 'Fila de risco'), ('saude', 'Saúde por produto'),
              ('causas', 'Causas e recorrentes'), ('previsao', 'Previsão de volume')]]
    itens += [{'t': 'inc', 'k': r['incidente'], 'r': r['incidente'],
               's': f"{r['produto']} · {r['equipe']} · risco {num(r['risco'])}%"}
              for _, r in f.iterrows()]
    itens += [{'t': 'ativo', 'k': a['ativo'], 'r': a['ativo'],
               's': f"{a['violacoes']} de {a['passagens']} passagens violaram"}
              for a in p['ativos'][:60]]
    itens += [{'t': 'prod', 'k': s['produto'], 'r': s['produto'],
               's': f"nota {num(s['nota'])} · posição {int(s['posicao'])} de 17"}
              for s in p['saude']]
    return itens
