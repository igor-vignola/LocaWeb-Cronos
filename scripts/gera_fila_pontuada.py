# -*- coding: utf-8 -*-
"""Gera data/interim/04_fila_pontuada.parquet.

Reproduz o modelo do notebook 04 — regressao logistica treinada so com o que existe na
abertura, corte temporal em 01/10/2025 — e grava a fila pontuada fora da amostra, com a
decomposicao exata de cada caso.

A decomposicao e possivel porque o modelo e linear: a contribuicao de cada coluna e
peso x (valor - media do treino), e a soma delas mais o intercepto devolve o logito.
O script confere essa reconstrucao antes de gravar.

Sem esse arquivo a aba de fila da aplicacao seria fake e o Django nao teria o que ler.
"""
import json
import warnings
from pathlib import Path

import holidays
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings('ignore')

RAIZ = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'data' / 'interim').exists())
DI = RAIZ / 'data' / 'interim'
CORTE = pd.Timestamp('2025-10-01')
SEMENTE = 42
TOP_SINAIS = 6            # quantas contribuicoes guardar por incidente

# ── base, com os mesmos nomes de coluna do notebook 04 ──────────────────────
df = pd.read_parquet(DI / 'incidentes_kpi.parquet')
df.columns = [c.strip() for c in df.columns]
COL_ATIVO = next(c for c in df.columns if c.lower().startswith('item de config'))
COL_VIOL = next(c for c in df.columns if c.lower().startswith('kpi violado'))
COL_DUR = next(c for c in df.columns if c.lower().startswith('dura'))
df = df[df['ano'] == 2025].copy()
df['violou'] = df[COL_VIOL].astype(str).str.strip().str.upper().eq('SIM')

feriados = holidays.Brazil(years=[2025])
df['is_feriado'] = df['dia'].dt.date.map(lambda d: int(d in feriados))

CATEGORICAS = ['Prioridade', 'Grupo designado', 'Aberto por', 'Produto',
               'Categoria', 'Subcategoria', COL_ATIVO]
NUMERICAS = ['hora', 'dia_semana', 'is_feriado']
CARACTERISTICAS = CATEGORICAS + NUMERICAS
POSTERIORES = [COL_DUR, 'Resolvido', 'Encerrado', 'Status', 'Código de fechamento',
               'Solução', COL_VIOL, 'violou']
assert not set(CARACTERISTICAS) & set(POSTERIORES), 'característica posterior à abertura'

treino = df[df['dia'] < CORTE].copy()
teste = df[df['dia'] >= CORTE].copy()
assert treino['dia'].max() < teste['dia'].min(), 'sobreposição temporal'
y_tr, y_te = treino['violou'].values, teste['violou'].values


def matriz(dados):
    X = dados[CARACTERISTICAS].copy()
    X[CATEGORICAS] = X[CATEGORICAS].astype(str)
    return X


pre = ColumnTransformer([
    ('cat', Pipeline([('imp', SimpleImputer(strategy='constant', fill_value='(vazio)')),
                      ('ohe', OneHotEncoder(handle_unknown='ignore', min_frequency=100))]),
     CATEGORICAS),
    ('num', Pipeline([('imp', SimpleImputer(strategy='median')),
                      ('sc', StandardScaler())]), NUMERICAS),
])
modelo = Pipeline([('pre', pre), ('clf', LogisticRegression(max_iter=5000,
                                                            random_state=SEMENTE))])
modelo.fit(matriz(treino), y_tr)

risco = modelo.predict_proba(matriz(teste))[:, 1]
print(f'treino: {len(treino):,} incidentes até {treino["dia"].max():%d/%m} '
      f'({int(y_tr.sum())} quebras)'.replace(',', '.'))
print(f'teste:  {len(teste):,} de {teste["dia"].min():%d/%m} a {teste["dia"].max():%d/%m} '
      f'({int(y_te.sum())} quebras)'.replace(',', '.'))
print(f'ROC AUC {roc_auc_score(y_te, risco):.4f} | PR-AUC {average_precision_score(y_te, risco):.4f}')
print(f'quebras previstas {risco.sum():.1f} contra {int(y_te.sum())} observadas')

# ── decomposicao exata: contribuicao = peso x (valor - media do treino) ─────
Xt_tr = pre.transform(matriz(treino))
Xt_te = pre.transform(matriz(teste))
Xt_tr = Xt_tr.toarray() if hasattr(Xt_tr, 'toarray') else Xt_tr
Xt_te = Xt_te.toarray() if hasattr(Xt_te, 'toarray') else Xt_te
media = Xt_tr.mean(axis=0)
coef = modelo.named_steps['clf'].coef_[0]
contrib = (Xt_te - media) * coef                       # (n_teste, n_colunas)
base = float(modelo.named_steps['clf'].intercept_[0] + coef @ media)

logito = contrib.sum(axis=1) + base
erro = np.abs(1 / (1 + np.exp(-logito)) - risco).max()
print(f'erro máximo de reconstrução: {erro:.2e}')
assert erro < 1e-9, 'a decomposição não reproduz o escore do modelo'

# nome legivel de cada coluna e a qual campo ela pertence
nomes = list(pre.get_feature_names_out())
CURTO = {'Grupo designado': 'equipe', 'Aberto por': 'origem', 'Item de configuração': 'ativo',
         'Prioridade': 'prioridade', 'Produto': 'produto', 'Categoria': 'categoria',
         'Subcategoria': 'subcategoria', 'hora': 'hora do dia',
         'dia_semana': 'dia da semana', 'is_feriado': 'feriado'}


def rotulo(n):
    corpo = n.split('__', 1)[1]
    for campo, curto in CURTO.items():
        if corpo.startswith(campo + '_'):
            valor = corpo[len(campo) + 1:]
            if valor in ('infrequent_sklearn', '(vazio)'):
                return f'{curto} pouco frequente'
            return f'{curto} {valor}'
        if corpo == campo:
            return curto
    return corpo


ROTULOS = [rotulo(n) for n in nomes]

# ── monta a saida ──────────────────────────────────────────────────────────
saida = pd.DataFrame({
    'incidente': teste['Número'].values,
    'dia': teste['dia'].values,
    'hora': teste['hora'].values,
    'prioridade': teste['Prioridade'].astype(str).str[0].radd('P').values,
    'produto': teste['Produto'].astype(str).values,
    'categoria': teste['Categoria'].astype(str).values,
    'subcategoria': teste['Subcategoria'].astype(str).values,
    'equipe': teste['Grupo designado'].astype(str).values,
    'ativo': teste[COL_ATIVO].astype(str).values,
    'risco': (risco * 100).round(2),
    'violou': y_te,
})

# historico do ativo conhecido no corte: o mesmo sinal que a tela mostra
hist = treino.groupby(COL_ATIVO)['violou'].agg(passagens='size', violacoes='sum')
saida['ativo_passagens'] = saida['ativo'].map(hist['passagens']).fillna(0).astype(int)
saida['ativo_violacoes'] = saida['ativo'].map(hist['violacoes']).fillna(0).astype(int)

# Os sinais que mais pesaram em cada caso.
# So entram colunas que o incidente de fato tem. Uma coluna zerada tambem contribui
# — nao ser da equipe X empurra o risco quando o peso de X e negativo — mas mostrar
# "equipe Team14" num incidente do Team11 confunde qualquer leitor. Ficam de fora.
PRESENTE = Xt_te != 0
positivo = np.where((contrib > 0) & PRESENTE, contrib, 0)
soma_pos = positivo.sum(axis=1)
ordem = np.argsort(-positivo, axis=1)[:, :TOP_SINAIS]
DIAS = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']
NUM_IDX = {n: j for j, n in enumerate(nomes) if n.startswith('num__')}


def rotulo_caso(j, linha_df):
    """Numerica nao tem valor no nome da coluna: coloca o valor do proprio incidente."""
    if j == NUM_IDX.get('num__hora'):
        return f'aberto às {int(linha_df["hora"]):02d}h'
    if j == NUM_IDX.get('num__dia_semana'):
        return DIAS[int(linha_df['dia'].dayofweek)]
    if j == NUM_IDX.get('num__is_feriado'):
        return 'feriado' if linha_df['is_feriado'] else 'dia comum'
    return ROTULOS[j]


te_ref = teste.reset_index(drop=True)
sinais = []
for i in range(len(te_ref)):
    linha = []
    for j in ordem[i]:
        if positivo[i, j] <= 0:
            continue
        peso = positivo[i, j] / soma_pos[i] * 100 if soma_pos[i] else 0
        linha.append({'sinal': rotulo_caso(j, te_ref.iloc[i]), 'peso': round(float(peso), 1),
                      'contrib': round(float(contrib[i, j]), 4)})
    sinais.append(json.dumps(linha, ensure_ascii=False))
saida['sinais'] = sinais

# quanto do empurrao positivo os sinais mostrados explicam: o resto vem de colunas
# ausentes, que sao corretas mas ilegiveis para quem le
todos_pos = np.where(contrib > 0, contrib, 0).sum(axis=1)
saida['sinais_cobertura'] = (soma_pos / np.where(todos_pos > 0, todos_pos, 1) * 100).round(1)

saida = saida.sort_values('risco', ascending=False).reset_index(drop=True)
saida['posicao'] = saida.index + 1
saida.to_parquet(DI / '04_fila_pontuada.parquet', index=False)

hoje = saida[saida['dia'] == CORTE]
print(f'\n{len(saida):,} incidentes pontuados -> 04_fila_pontuada.parquet'.replace(',', '.'))
print(f'{len(hoje)} deles abertos em {CORTE:%d/%m}, {int(hoje["violou"].sum())} violaram')
print(f'acima de 10% de risco: {(saida["risco"] >= 10).sum()} casos, '
      f'{int(saida.loc[saida["risco"] >= 10, "violou"].sum())} violaram')
print(f'nos 50 primeiros da fila: {int(saida.head(50)["violou"].sum())} das '
      f'{int(saida["violou"].sum())} violações do período')
print('\ntopo da fila:')
print(saida.head(6)[['posicao', 'incidente', 'risco', 'produto', 'equipe', 'ativo',
                     'ativo_violacoes', 'ativo_passagens', 'violou']].to_string(index=False))
print('\nsinais do primeiro:')
for s in json.loads(saida.iloc[0]['sinais']):
    print(f"  {s['peso']:5.1f}%  {s['sinal']}")
