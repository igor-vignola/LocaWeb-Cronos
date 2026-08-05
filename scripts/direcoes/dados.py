# -*- coding: utf-8 -*-
"""Dados compartilhados pelas tres direcoes de design da aplicacao.

Cada direcao le daqui, entao os numeros sao os mesmos nas tres e saem todos de parquet
gerado por notebook. Nada e digitado a mao a nao ser a fila e a decomposicao, que vem do
notebook 04 (ainda sem parquet proprio) e estao marcadas como tal."""
from pathlib import Path

import pandas as pd

RAIZ = Path.cwd()
DI = RAIZ / 'data' / 'interim'
CORTE = pd.Timestamp('2025-10-01')

# ── formatacao pt-BR ────────────────────────────────────────────────────────
pt = lambda v, c=1: f'{v:.{c}f}'.replace('.', ',')
mil = lambda v: f'{int(v):,}'.replace(',', '.')
dm = lambda t: f'{t.day:02d}/{t.month:02d}'

# ── base ────────────────────────────────────────────────────────────────────
kpi = pd.read_parquet(DI / 'incidentes_kpi.parquet')
kpi.columns = [c.strip() for c in kpi.columns]
COL_ATIVO = next(c for c in kpi.columns if c.lower().startswith('item de config'))
COL_VIOL = next(c for c in kpi.columns if c.lower().startswith('kpi violado'))
kpi['violou'] = kpi[COL_VIOL].astype(str).str.strip().str.upper().eq('SIM')

saude = pd.read_parquet(DI / '07_saude_produto.parquet').sort_values('posicao')
proj = pd.read_parquet(DI / '06_projecao.parquet')
proj = proj[proj['corte'] == CORTE].set_index('prioridade')
causas = pd.read_parquet(DI / '05_causas.parquet')
recor = pd.read_parquet(DI / '05_recorrentes.parquet')
grupos = pd.read_parquet(DI / '05_grupos_criticos.parquet').sort_values('taxa %', ascending=False)
prev = pd.read_parquet(DI / '03_previsao_diaria.parquet').sort_values('dia')

P3 = prev[prev['prioridade'] == 'P3'].reset_index(drop=True)
P2 = prev[prev['prioridade'] == 'P2'].reset_index(drop=True)
REAL3 = P3[P3['tipo'] == 'realizado'].reset_index(drop=True)
FUT3 = P3[P3['tipo'] == 'previsto'].reset_index(drop=True)
ONTEM = REAL3.iloc[-1]
HOJE3 = FUT3.iloc[0]
HOJE2 = P2[P2['tipo'] == 'previsto'].reset_index(drop=True).iloc[0]
DIA_HOJE = HOJE3['dia']

# A base tem registro desde 2023, mas so fica densa em 2025: 87 elegiveis em 2023 e 357 em
# 2024 contra 25.156 em 2025. Misturar os tres achata qualquer media — a media de dia util cai
# de 94 para 43 — e inventa historico de ativo. Todo numero de tela e de 2025.
kpi = kpi[kpi['ano'] == 2025]

# elegiveis totais do dia anterior ao corte, todas as prioridades
ONTEM_TOTAL = int((kpi['dia'] == ONTEM['dia']).sum())
ONTEM_VIOL = int(kpi.loc[kpi['dia'] == ONTEM['dia'], 'violou'].sum())
# em aberto NO corte: abriu antes e nao tinha sido resolvido ainda naquele instante.
# Mesma definicao da parcela 2 da projecao no notebook 06.
_abriu_antes = kpi['dia'] < CORTE
_resolvido_antes = (kpi['Resolvido'] < CORTE).fillna(False)
EM_ABERTO = int((_abriu_antes & ~_resolvido_antes).sum())

# tudo que a tela mostra tem de ser conhecido no corte, senao a tela usa o futuro
ATE_CORTE = kpi[_abriu_antes]
TOTAL_VIOL = int(ATE_CORTE['violou'].sum())      # violacoes conhecidas no corte
ELEGIVEIS = len(ATE_CORTE)

# linha de base recente para comparar ontem: os 20 ultimos dias uteis. A media do ano nao
# serve porque o volume subiu de patamar ao longo de 2025.
_vol = ATE_CORTE.groupby('dia').size()
_vol_util = _vol[_vol.index.dayofweek < 5]
BASE_20 = float(_vol_util.tail(20).mean())

# dias uteis consecutivos sem violacao entre os incidentes abertos no dia
_viol_dia = ATE_CORTE.groupby('dia')['violou'].sum()
_viol_util = _viol_dia[_viol_dia.index.dayofweek < 5]
SEM_VIOL = 0
for _v in _viol_util.iloc[::-1]:
    if _v > 0:
        break
    SEM_VIOL += 1
ULTIMOS_DIAS = [(d, int(v)) for d, v in _viol_util.tail(10).items()]

# os 30 dias antes do corte contra os 30 anteriores, para o indicador de variacao
_j1 = ATE_CORTE[ATE_CORTE['dia'] >= CORTE - pd.Timedelta(days=30)]
_j0 = ATE_CORTE[(ATE_CORTE['dia'] >= CORTE - pd.Timedelta(days=60))
                & (ATE_CORTE['dia'] < CORTE - pd.Timedelta(days=30))]
TAXA_30 = float(_j1['violou'].mean() * 100)
VIOL_30 = int(_j1['violou'].sum())
ELEG_30 = len(_j1)
DELTA_TAXA = float(_j1['violou'].mean() / _j0['violou'].mean() - 1) * 100
DELTA_VOL = float(len(_j1) / len(_j0) - 1) * 100


# ── grade de ativos: o objeto de identidade construido com dado ─────────────
def grade_ativos(n=112, minimo=6):
    """Ativos com mais violacoes ate o corte, com a taxa de cada.
    Vira a grade que acende onde o problema esta concentrado."""
    g = ATE_CORTE.groupby(COL_ATIVO).agg(passagens=('violou', 'size'), violacoes=('violou', 'sum'))
    g = g[g['passagens'] >= minimo].copy()
    g['taxa'] = g['violacoes'] / g['passagens'] * 100
    return g.sort_values('violacoes', ascending=False).head(n)


ATIVOS = grade_ativos()

# ── sazonalidade por dia da semana, P3 elegiveis de 2025 ───────────────────
LBL_DIA = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
_p3_2025 = ATE_CORTE[(ATE_CORTE['ano'] == 2025)
                     & ATE_CORTE['Prioridade'].astype(str).str.startswith('3')]
_serie = _p3_2025.groupby('dia').size()
_idx = pd.date_range('2025-01-01', CORTE - pd.Timedelta(days=1), freq='D')
_serie = _serie.reindex(_idx, fill_value=0)
SEMANA = _serie.groupby(_serie.index.dayofweek).mean().round(1)

# ── fila pontuada e decomposicao: saida do notebook 04 ─────────────────────
# TODO: trocar por parquet quando o 04 passar a gravar a fila pontuada
FILA = [
    {'id': 'INC8595245', 'risco': 56.1, 'equipe': 'Team11', 'produto': 'lsin',
     'ativo': 'IC00840', 'cat': 'cat31', 'sub': 'sub388'},
    {'id': 'INC8607669', 'risco': 50.4, 'equipe': 'Team11', 'produto': 'lsin',
     'ativo': 'IC00840', 'cat': 'cat31', 'sub': 'sub388'},
    {'id': 'INC8579361', 'risco': 47.2, 'equipe': 'Team11', 'produto': 'lsin',
     'ativo': 'IC00840', 'cat': 'cat31', 'sub': 'sub388'},
    {'id': 'INC8599520', 'risco': 42.9, 'equipe': 'Team11', 'produto': 'lsin',
     'ativo': 'IC00840', 'cat': 'cat31', 'sub': 'sub388'},
    {'id': 'INC8601345', 'risco': 40.4, 'equipe': 'Team11', 'produto': 'lsin',
     'ativo': 'IC00840', 'cat': 'cat31', 'sub': 'sub388'},
    {'id': 'INC8614082', 'risco': 33.1, 'equipe': 'Team07', 'produto': 'lhco',
     'ativo': 'IC01285', 'cat': 'cat74', 'sub': 'sub210'},
]
# o historico do ativo sai do dado, nao de valor digitado: um deles estava errado
_hist = ATE_CORTE.groupby(COL_ATIVO)['violou'].agg(['size', 'sum'])
for _c in FILA:
    _l = _hist.loc[_c['ativo']]
    _c['pass'], _c['viol'] = int(_l['size']), int(_l['sum'])
    _c['taxa_ativo'] = _c['viol'] / _c['pass'] * 100
# peso relativo de cada sinal no escore do primeiro da fila
SINAIS = [('categoria cat31', 38), ('produto lsin', 19), ('subcategoria sub388', 12),
          ('equipe Team11', 11), ('sábado, 19h', 8)]
MEDIA_BASE = 0.97          # taxa de violacao da base elegivel, em %
INEDITO_X = 4.6            # quantas vezes o problema inedito viola mais que o rotineiro

if __name__ == '__main__':
    print(f'corte {CORTE.date()} | ontem {ONTEM["dia"].date()} = {ONTEM_TOTAL} elegíveis '
          f'({ONTEM["valor"]:.0f} no P3)')
    print(f'previsto hoje: P3 {HOJE3["valor"]:.1f} (faixa {HOJE3["baixo"]:.0f} a {HOJE3["alto"]:.0f}) '
          f'| P2 {HOJE2["valor"]:.1f}')
    print(f'em aberto no corte: {EM_ABERTO}')
    print(f'\ngrade de ativos: {len(ATIVOS)} ativos, '
          f'{ATIVOS["violacoes"].sum()} violações, taxa de {ATIVOS["taxa"].min():.1f}% '
          f'a {ATIVOS["taxa"].max():.1f}%')
    print(ATIVOS.head(6).to_string())
    print('\nmédia por dia da semana (P3):')
    print(' '.join(f'{LBL_DIA[i]} {SEMANA[i]:.1f}' for i in range(7)))
    print(f'\nprojeção P3 {proj.loc["P3", "projeção"]:.1f} de {proj.loc["P3", "meta máxima"]:.0f}'
          f' | P2 {proj.loc["P2", "projeção"]:.1f} de {proj.loc["P2", "meta máxima"]:.0f}')


# ── historico mensal por ativo, para o modal de aprofundamento ──────────────
def historico_mensal(ativos):
    """Passagens e violacoes por mes de cada ativo, para o mini grafico do modal."""
    d = ATE_CORTE[ATE_CORTE[COL_ATIVO].isin(ativos)]
    g = d.groupby([COL_ATIVO, 'mes'])['violou'].agg(['size', 'sum'])
    fora = {}
    for a in ativos:
        if a not in g.index.get_level_values(0):
            fora[a] = []
            continue
        s = g.loc[a].reindex(range(1, CORTE.month), fill_value=0)
        fora[a] = [{'mes': int(m), 'passagens': int(r['size']), 'violacoes': int(r['sum'])}
                   for m, r in s.iterrows()]
    return fora


HIST_ATIVO = historico_mensal(list(ATIVOS.index))

# componentes da nota de saude, com a posicao relativa de cada um (0 melhor, 1 pior)
COMPONENTES = [('taxa_violacao', 'taxa de violação', '%', 100),
               ('prop_inedito', 'problemas inéditos', '%', 100),
               ('prop_sem_causa', 'fechados sem causa', '%', 100),
               ('duracao_mediana_h', 'duração mediana', 'h', 1),
               ('tendencia', 'tendência', '', 1)]
MES_LBL = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']


# ── campo de linhas: a serie diaria real de cada produto vira textura de fundo ──
def curvas_produto(n=16, janela=7):
    """Serie diaria de cada produto, suavizada e normalizada em 0..1.
    Cada curva do fundo e a historia real de um produto, nao ruido decorativo."""
    top = ATE_CORTE['Produto'].value_counts().head(n).index
    fora = {}
    idx = pd.date_range('2025-01-01', CORTE - pd.Timedelta(days=1), freq='D')
    for p in top:
        s = ATE_CORTE[ATE_CORTE['Produto'] == p].groupby('dia').size()
        s = s.reindex(idx, fill_value=0).rolling(janela, min_periods=1).mean()
        s = s.iloc[::3]                       # um ponto a cada tres dias, curva mais limpa
        lo, hi = s.min(), s.max()
        fora[p] = [round(float(v), 4) for v in ((s - lo) / ((hi - lo) or 1))]
    return fora


CURVAS = curvas_produto()

# ── distribuicao por hora do dia, para o relogio de 24h ────────────────────
_h = ATE_CORTE.groupby('hora').agg(abertos=('violou', 'size'), violacoes=('violou', 'sum'))
_h = _h.reindex(range(24), fill_value=0)
HORAS = [{'h': int(i), 'abertos': int(r['abertos']), 'violacoes': int(r['violacoes']),
          'taxa': float(r['violacoes'] / r['abertos'] * 100) if r['abertos'] else 0.0}
         for i, r in _h.iterrows()]
HORA_PICO = max(HORAS, key=lambda x: x['abertos'])
HORA_RISCO = max((x for x in HORAS if x['abertos'] >= 100), key=lambda x: x['taxa'])


# ── fila pontuada fora da amostra (scripts/gera_fila_pontuada.py) ──────────
import json as _json

fila = pd.read_parquet(DI / '04_fila_pontuada.parquet')
fila['sinais'] = fila['sinais'].map(_json.loads)
FILA_TODA = fila
FILA_HOJE = fila[fila['dia'] == CORTE].reset_index(drop=True)
ACIMA_10 = fila[fila['risco'] >= 10]
TOP50_PEGA = int(fila.head(50)['violou'].sum())
VIOL_PERIODO = int(fila['violou'].sum())
N_FILA = len(fila)
