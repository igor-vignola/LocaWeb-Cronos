---
name: notebook-style
description: "Estrutura e padrão obrigatório dos notebooks Jupyter do projeto Cronos. SEMPRE consulte antes de criar ou editar arquivos .ipynb. Use quando o usuário mencionar: notebook, jupyter, .ipynb, AED, EDA, análise exploratória, modelagem, features, clusterização, SHAP, ou qualquer trabalho de análise de dados em Python. Use também ao gerar o primeiro notebook de uma nova etapa (01_eda, 02_features, etc.)."
---

# Padrão de Notebooks — Cronos

Todos os notebooks do projeto seguem esta estrutura. Garante que Ana, Hygor e Igor consigam abrir qualquer notebook e entender em minutos onde está cada coisa.

## Convenção de nomenclatura

Notebooks ficam em `notebooks/` com prefixo numérico:

```
notebooks/
├── 01_eda.ipynb          ← análise exploratória
├── 02_features.ipynb     ← engenharia de features
├── 03_modelagem.ipynb    ← treinamento dos modelos
├── 04_ola.ipynb          ← análise específica de OLA
├── 05_cluster.ipynb      ← clusterização DTW
└── 06_shap.ipynb         ← explicabilidade
```

**Por que prefixo numérico:** ordenação visual no explorador + indica ordem lógica de execução.

---

## Estrutura obrigatória do notebook

### Célula 1 — Cabeçalho (markdown)

```markdown
# 01 · Análise Exploratória de Dados (AED)

**Projeto:** Cronos · Challenge FIAP 2026 com Locaweb
**Autor(es):** Igor Vignola
**Data de criação:** 14/05/2026
**Última atualização:** 14/05/2026

## Objetivo

Explorar o LWDATASET para identificar padrões, sazonalidades, distribuições por
produto/categoria/prioridade, e investigar a anomalia de incidentes em setembro/2025
(pedido explícito da Locaweb).

## Dependências

- Python 3.11+
- pandas, numpy, matplotlib, seaborn, plotly
- holidays (para feriados BR)

## Entradas

- `data/raw/LWDATASET.xlsx`

## Saídas

- `data/interim/incidentes_limpo.parquet`
- Gráficos exportados para `notebooks/figures/01_eda/`
- Insights documentados em `context/sprints/02-arquitetura.md`
```

### Célula 2 — Imports (código)

Sempre na segunda célula, sempre agrupados em 3 blocos com linha em branco entre eles:

```python
# Stdlib
import os
import warnings
from pathlib import Path

# Third-party
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import holidays

# Local (quando houver módulos do projeto)
# from src.features import build_temporal_features

# Configurações
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
```

### Seções padronizadas (markdown como `## N. Título`)

Toda análise segue esta sequência mínima:

```
## 1. Setup
## 2. Carga dos dados
## 3. Visão geral
## 4. Análises (subdividido conforme necessário)
## 5. Conclusões e próximos passos
```

#### Seção 1 — Setup
Definir caminhos, configurações de visualização, paleta. Aplicar `setup_cronos_style()` da skill `viz-style`.

#### Seção 2 — Carga dos dados
Apenas leitura. **Não fazer transformação aqui.**

```python
df = pd.read_excel('../data/raw/LWDATASET.xlsx')
print(f"Linhas: {len(df):,} | Colunas: {df.shape[1]}")
```

#### Seção 3 — Visão geral (validação obrigatória)
Sempre rodar estas três células antes de qualquer análise:

```python
df.head()
```
```python
df.info()
```
```python
df.describe(include='all').T
```

E mais um diagnóstico mínimo:
```python
# Faltantes por coluna
df.isna().sum().sort_values(ascending=False)
```

#### Seção 4 — Análises
Subdividir conforme o tópico, usando `### 4.1 Subtítulo`, `### 4.2 Subtítulo`, etc.

Cada subseção deve seguir o padrão:
1. **Pergunta** em markdown (o que estamos investigando)
2. **Código** que responde a pergunta
3. **Achado** em markdown logo após (o que descobrimos)

Exemplo:
```markdown
### 4.3 Distribuição de incidentes por dia da semana

**Pergunta:** existe sazonalidade real por dia da semana ou só em feriados/fim de semana?
```
```python
# código de análise
```
```markdown
**Achado:** confirmado que a sazonalidade não é "segunda vs quinta", e sim
"dia útil vs feriado/fim de semana". Sexta e segunda têm padrões muito similares.
```

#### Seção 5 — Conclusões e próximos passos

**Obrigatória** ao final do notebook. Estrutura:

```markdown
## 5. Conclusões e próximos passos

### Principais achados
1. ...
2. ...

### Decisões que isso implica
- Para modelagem: ...
- Para arquitetura: ...

### Próximos passos
- [ ] ...
- [ ] ...

### Pontos abertos / dúvidas
- ...
```

---

## Regras de boa prática

### 1. DataFrames têm prefixo `df_`
```python
df_incidentes      # ✅
df_pai             # ✅ filtrado só pais
df_ola_p2          # ✅ filtrado P2 + entrou no KPI
incidentes         # ❌ ambíguo
data               # ❌ ainda mais ambíguo
```

### 2. Filtros explícitos com nome semântico
```python
# ✅ Bom — nome descreve o filtro
df_pai = df[df['Incidente Pai'].isna()]
df_kpi = df_pai[df_pai['Entrou para KPI?'] == 'SIM']

# ❌ Ruim — sem documentar o filtro
df2 = df[df['Incidente Pai'].isna() & (df['Entrou para KPI?'] == 'SIM')]
```

### 3. Não rodar células que demoram >30s sem cache
Para operações pesadas (treino, agregação massiva), salvar resultado intermediário em `data/interim/` e recarregar.

### 4. Não imprimir DataFrames gigantes
```python
df.head(20)           # ✅
df.sample(50)         # ✅
df                    # ❌ joga 122k linhas no output
```

### 5. Outputs gigantes não vão pro Git
Antes de commitar, **limpar outputs grandes** (gráficos enormes em base64, DataFrames de 10k+ linhas). Use:
```bash
jupyter nbconvert --clear-output --inplace notebooks/*.ipynb
```
Ou configurar `nbstripout` no Git (recomendado pra projeto colaborativo).

### 6. Comentários explicam o "porquê", não o "o quê"
```python
# ❌ Comentário óbvio
# Filtra incidentes pais
df_pai = df[df['Incidente Pai'].isna()]

# ✅ Comentário útil
# Confirmado pela Locaweb: apenas incidentes pai entram no KPI.
# Filhos não devem ser contados na análise de OLA.
df_pai = df[df['Incidente Pai'].isna()]
```

### 7. Marcar TODOs explicitamente
```python
# TODO(igor): investigar se setembro/2025 é mudança de processo ou de categorização
# FIXME: filtro abaixo está pegando NaN como string vazia em algumas linhas
```

---

## Template inicial pronto pra usar

Quando criar um notebook novo, partir desta base e ajustar:

````markdown
# NN · Título do notebook

**Projeto:** Cronos · Challenge FIAP 2026 com Locaweb
**Autor(es):** [nome]
**Data de criação:** [DD/MM/AAAA]
**Última atualização:** [DD/MM/AAAA]

## Objetivo

[1-2 frases sobre o que este notebook responde]

## Dependências

- [libs principais]

## Entradas

- [arquivos lidos]

## Saídas

- [arquivos gerados, gráficos, documentação atualizada]

---
## 1. Setup

## 2. Carga dos dados

## 3. Visão geral

## 4. Análises

### 4.1 [primeira pergunta]

## 5. Conclusões e próximos passos
````
