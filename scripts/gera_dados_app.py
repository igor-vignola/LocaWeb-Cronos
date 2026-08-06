# -*- coding: utf-8 -*-
"""Gera data/app/ — o pacote que a aplicacao Django le em producao.

Tudo que a tela precisa ja vem agregado aqui. O conteiner nao carrega a base bruta de
1,5 MB nem executa pandas pesado a cada requisicao: ele abre um JSON de poucos kB e um
parquet com a fila. Essa separacao e o que permite a imagem rodar em plano gratuito sem
Prophet nem scikit-learn dentro.

Entradas: os parquets de data/interim gerados pelos notebooks 02 a 07 e pelos scripts
gera_previsao_diaria.py e gera_fila_pontuada.py.
"""
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent / 'direcoes'))
from dados import (ATIVOS, BASE_20, CORTE, DELTA_TAXA, DIA_HOJE, ELEG_30, ELEGIVEIS, EM_ABERTO,
                   FILA_TODA, FUT3, HIST_ATIVO, HORAS, HORA_PICO, HORA_RISCO, HOJE2, HOJE3,
                   LBL_DIA, MEDIA_BASE, MES_LBL, ONTEM, ONTEM_TOTAL, ONTEM_VIOL, REAL3, SEMANA,
                   SEM_VIOL, TAXA_30, TOP50_PEGA, TOTAL_VIOL, ULTIMOS_DIAS, VIOL_30,
                   VIOL_PERIODO, ATE_CORTE, COL_ATIVO, causas, grupos, kpi, recor, saude)

RAIZ = Path.cwd()
DESTINO = RAIZ / 'data' / 'app'
DESTINO.mkdir(parents=True, exist_ok=True)
HORA_AGORA = 7          # a aplicacao simula as 07h00 do dia do corte


def acompanhamento_do_dia():
    """Previsto contra realizado ao longo do dia.

    A curva esperada vem da distribuicao historica por hora aplicada ao total previsto
    para hoje. A realizada e o que ja entrou. Assim o turno consegue ver, as 11h, se o
    dia esta no ritmo previsto — que e o que torna a previsao util depois do cafe."""
    total_h = sum(x['abertos'] for x in HORAS)
    share = [x['abertos'] / total_h for x in HORAS]
    acumulado, s = [], 0.0
    for f in share:
        s += f
        acumulado.append(s)

    p3_hoje = kpi[(kpi['dia'] == CORTE) & kpi['Prioridade'].astype(str).str.startswith('3')]
    por_hora = p3_hoje.groupby('hora').size().reindex(range(24), fill_value=0)
    real_acum, t = [], 0
    for h in range(24):
        t += int(por_hora[h])
        real_acum.append(t)

    prev = float(HOJE3['valor'])
    esperado = [round(prev * a, 1) for a in acumulado]
    # projecao do fechamento pelo ritmo observado ate agora
    ate_agora = real_acum[HORA_AGORA]
    frac = acumulado[HORA_AGORA]
    ritmo = round(ate_agora / frac, 1) if frac > 0 else prev
    return {
        'hora_agora': HORA_AGORA,
        'esperado': esperado,
        'realizado': real_acum[:HORA_AGORA + 1],
        'por_hora_real': [int(v) for v in por_hora],
        'previsto': round(prev, 1),
        'baixo': round(float(HOJE3['baixo']), 1),
        'alto': round(float(HOJE3['alto']), 1),
        'ate_agora': ate_agora,
        'esperado_agora': esperado[HORA_AGORA],
        'ritmo_fecha': ritmo,
        'no_ritmo': bool(float(HOJE3['baixo']) <= ritmo <= float(HOJE3['alto'])),
        # quanto do dia ja passou, em volume esperado. Extrapolar com 14% do dia e
        # instavel e a tela precisa dizer isso em vez de fingir precisao.
        'dia_decorrido': round(frac * 100, 1),
        'confiavel': bool(frac >= .35),
    }


def serie(df, campos):
    return [{k: (v.strftime('%Y-%m-%d') if isinstance(v, pd.Timestamp) else
                 (round(float(v), 4) if isinstance(v, float) else
                  (int(v) if isinstance(v, (int, bool)) else str(v))))
             for k, v in r.items() if k in campos} for _, r in df.iterrows()]


pacote = {
    'corte': CORTE.strftime('%Y-%m-%d'),
    'gerado_de': 'data/interim (notebooks 02 a 07)',
    'hoje': {
        'dia': DIA_HOJE.strftime('%Y-%m-%d'),
        'previsto_p3': round(float(HOJE3['valor']), 1),
        'baixo_p3': round(float(HOJE3['baixo']), 1),
        'alto_p3': round(float(HOJE3['alto']), 1),
        'previsto_p2': round(float(HOJE2['valor']), 1),
        'baixo_p2': round(float(HOJE2['baixo']), 1),
        'alto_p2': round(float(HOJE2['alto']), 1),
    },
    'ontem': {'dia': ONTEM['dia'].strftime('%Y-%m-%d'), 'total': ONTEM_TOTAL,
              'violou': ONTEM_VIOL, 'p3': int(ONTEM['valor'])},
    'base': {'media_violacao': MEDIA_BASE, 'elegiveis': ELEGIVEIS, 'violacoes': TOTAL_VIOL,
             'em_atendimento': EM_ABERTO, 'base_20_dias': round(BASE_20, 1),
             'sem_violacao_dias': SEM_VIOL, 'taxa_30': round(TAXA_30, 2),
             'viol_30': VIOL_30, 'eleg_30': ELEG_30, 'delta_taxa': round(DELTA_TAXA, 1),
             'top50_pega': TOP50_PEGA, 'viol_periodo': VIOL_PERIODO},
    'acompanhamento': acompanhamento_do_dia(),
    'horas': HORAS,
    'hora_pico': HORA_PICO,
    'hora_risco': HORA_RISCO,
    'semana': [{'dia': LBL_DIA[i], 'media': float(SEMANA[i])} for i in range(7)],
    'ultimos_dias': [{'dia': d.strftime('%Y-%m-%d'), 'rot': LBL_DIA[d.dayofweek],
                      'dm': f'{d.day:02d}/{d.month:02d}', 'violacoes': v}
                     for d, v in ULTIMOS_DIAS],
    'trilho': {
        'realizado': [{'dia': r['dia'].strftime('%Y-%m-%d'), 'valor': float(r['valor'])}
                      for _, r in REAL3.tail(30).iterrows()],
        'previsto': [{'dia': r['dia'].strftime('%Y-%m-%d'), 'valor': float(r['valor']),
                      'baixo': float(r['baixo']), 'alto': float(r['alto'])}
                     for _, r in FUT3.iterrows()],
    },
    'projecao': [{'prioridade': p, 'projecao': float(r['projeção']),
                  'meta': float(r['meta máxima']), 'baixo': float(r['faixa baixa']),
                  'alto': float(r['faixa alta']),
                  'dentro': r['situação projetada'] == 'dentro da meta'}
                 for p, r in __import__('dados').proj.iterrows()],
    'saude': [{'produto': p, **{k: (float(v) if isinstance(v, float) else
                                    (int(v) if not isinstance(v, str) else v))
                                for k, v in r.items()}} for p, r in saude.iterrows()],
    'ativos': [{'ativo': a, 'passagens': int(r['passagens']), 'violacoes': int(r['violacoes']),
                'taxa': round(float(r['taxa']), 2), 'hist': HIST_ATIVO.get(a, [])}
               for a, r in ATIVOS.iterrows()],
    'causas': serie(causas.head(8), ['Código de fechamento', '% da base', '% das quebras',
                                     'taxa de quebra %', 'vezes a média']),
    'recorrentes': serie(recor.head(8), ['problema', 'incidentes', 'ativos', 'quebras']),
    'grupos': serie(grupos.head(8), ['grupo', 'taxa %', 'vezes a média']),
    'meses': MES_LBL,
    'dias_semana': LBL_DIA,
}

alvo = DESTINO / 'painel.json'
alvo.write_text(json.dumps(pacote, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

# a fila fica em parquet: sao 5.183 linhas e o Django pagina em cima dela
shutil.copy(RAIZ / 'data' / 'interim' / '04_fila_pontuada.parquet', DESTINO / 'fila.parquet')

kb_json = alvo.stat().st_size / 1024
kb_fila = (DESTINO / 'fila.parquet').stat().st_size / 1024
print(f'painel.json  {kb_json:7.1f} kB')
print(f'fila.parquet {kb_fila:7.1f} kB')
print(f'total        {kb_json + kb_fila:7.1f} kB  (contra 1.802 kB da base bruta)')
ac = pacote['acompanhamento']
print(f"\nacompanhamento às {ac['hora_agora']:02d}h: {ac['ate_agora']} entraram, "
      f"{ac['esperado_agora']} esperados")
print(f"ritmo projeta fechar em {ac['ritmo_fecha']} · previsto {ac['previsto']} "
      f"(faixa {ac['baixo']} a {ac['alto']}) · "
      f"{'dentro da faixa' if ac['no_ritmo'] else 'FORA da faixa'}")
