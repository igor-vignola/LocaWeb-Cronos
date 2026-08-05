# -*- coding: utf-8 -*-
"""Gera data/interim/03_previsao_diaria.parquet com a mesma configuracao do notebook 03.
Serve o trilho de tempo da aplicacao: dias realizados + dias previstos com banda de 80%.
Sem esse arquivo o Django precisaria do Prophet dentro do container."""
import warnings

import pandas as pd
from prophet import Prophet

warnings.filterwarnings('ignore')

CORTE = pd.Timestamp('2025-10-01')      # mesmo corte da projecao do notebook 06
HORIZONTE = 10                          # dias corridos previstos a frente do corte

df = pd.read_parquet('data/interim/incidentes_kpi.parquet')
df['dia'] = pd.to_datetime(df['Aberto']).dt.normalize()
df = df[df['dia'].dt.year == 2025]
idx = pd.date_range('2025-01-01', '2025-12-31', freq='D')

linhas = []
for tag in ('P2', 'P3'):
    d = df[df['Prioridade'].astype(str).str.startswith(tag[1])]
    serie = d.groupby('dia').size().reindex(idx, fill_value=0)

    treino = serie[serie.index < CORTE]
    m = Prophet(weekly_seasonality=True, yearly_seasonality=False,
                daily_seasonality=False, interval_width=0.80)
    m.add_country_holidays(country_name='BR')
    m.fit(pd.DataFrame({'ds': treino.index, 'y': treino.values}))

    futuro = pd.date_range(CORTE, periods=HORIZONTE, freq='D')
    fc = m.predict(pd.DataFrame({'ds': futuro}))

    # dias ja realizados: os 25 ultimos antes do corte
    for dia, valor in treino.tail(25).items():
        linhas.append({'prioridade': tag, 'dia': dia, 'tipo': 'realizado',
                       'valor': float(valor), 'baixo': None, 'alto': None})
    for dia, yhat, lo, hi in zip(futuro, fc['yhat'], fc['yhat_lower'], fc['yhat_upper']):
        linhas.append({'prioridade': tag, 'dia': dia, 'tipo': 'previsto',
                       'valor': max(yhat, 0.0), 'baixo': max(lo, 0.0), 'alto': max(hi, 0.0)})

saida = pd.DataFrame(linhas)
saida.to_parquet('data/interim/03_previsao_diaria.parquet', index=False)

for tag in ('P2', 'P3'):
    s = saida[saida['prioridade'] == tag]
    ult = s[s['tipo'] == 'realizado'].iloc[-1]
    pr1 = s[s['tipo'] == 'previsto'].iloc[0]
    print(f"{tag}: ultimo realizado {ult['dia'].date()} = {ult['valor']:.0f} | "
          f"previsto {pr1['dia'].date()} = {pr1['valor']:.1f} "
          f"(faixa {pr1['baixo']:.0f} a {pr1['alto']:.0f})")
print(f'\n{len(saida)} linhas -> data/interim/03_previsao_diaria.parquet')
