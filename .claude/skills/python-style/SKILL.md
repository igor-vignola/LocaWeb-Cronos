---
name: python-style
description: "Convenções de código Python do projeto Cronos. SEMPRE consulte ao escrever, revisar ou refatorar código Python (.py ou células de código em .ipynb). Use quando o usuário mencionar: código Python, função, classe, módulo, Django, pandas, refatorar, PEP 8, formatação, lint, type hints, docstrings, ou estiver editando qualquer arquivo .py. Garante código uniforme entre notebooks, módulos auxiliares e aplicação Django."
---

# Padrão de Código Python — Cronos

Convenções para código Python em todo o projeto: notebooks, módulos auxiliares (`src/`), e aplicação Django (`web/`).

**Base:** PEP 8 + convenções específicas listadas abaixo.

---

## Naming

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Variáveis e funções | `snake_case` | `incidentes_pai`, `calcular_ola_estourado()` |
| Classes | `PascalCase` | `OlaCalculator`, `MorningBriefBuilder` |
| Constantes | `UPPER_CASE` | `OLA_LIMITES`, `CORES_CRONOS` |
| Variáveis privadas | `_prefixo` | `_cache`, `_resultado_temp` |
| Métodos especiais Django | `padrão Django` | `get_queryset`, `clean_data` |

### DataFrames sempre com prefixo `df_`

```python
df_incidentes     # ✅ tabela bruta de incidentes
df_pai            # ✅ filtrado: só incidentes pai
df_kpi            # ✅ filtrado: entrou no KPI
df_ola_p2         # ✅ filtrado: P2 + entrou no KPI

incidentes        # ❌ ambíguo (dict? lista? Series?)
data              # ❌ ainda mais ambíguo
```

### Nomes em português ou inglês?

- **Domínio do negócio em português**: incidente, ola, prioridade, cascata, briefing. São termos do projeto.
- **Termos técnicos em inglês**: `model`, `predict`, `train_test_split`, `feature`, `target`. Mantém compatibilidade com bibliotecas.
- **Não misturar no mesmo nome**: `treinar_model` é ruim. Escolha um: `treinar_modelo` ou `train_model`.

---

## Imports

Sempre organizados em 3 grupos, com **uma linha em branco** entre eles. Dentro de cada grupo, em ordem alfabética.

```python
# Stdlib
import os
import warnings
from datetime import datetime, timedelta
from pathlib import Path

# Third-party
import numpy as np
import pandas as pd
import plotly.express as px
from prophet import Prophet
from xgboost import XGBRegressor

# Local
from src.features import build_temporal_features
from src.ola import calcular_estourados
```

### Regras adicionais

- **Não usar `from x import *`.** Sempre nomes explícitos.
- **Imports relativos só dentro de pacotes**: `from .features import ...` é OK dentro de `src/`. Fora, usar absoluto.
- **Não importar dentro de função** a menos que seja import condicional ou lazy intencional.
- **Configurações globais** (warnings, pandas options) vão DEPOIS dos imports, em bloco separado.

---

## Linha e formatação

- **Limite de 88 caracteres por linha** (padrão Black, não 79 do PEP 8 estrito).
- **Aspas duplas `"..."`** preferenciais sobre aspas simples. Exceção: strings que contêm aspas duplas.
- **Trailing comma** em listas/dicts/argumentos multi-linha (facilita diff):
  ```python
  CORES = [
      "#2563EB",
      "#DC2626",
      "#444444",  # ← vírgula no último também
  ]
  ```
- **Quebra de linha em chamadas longas**:
  ```python
  resultado = funcao_longa(
      primeiro_arg=valor,
      segundo_arg=outro_valor,
      terceiro_arg=mais_um,
  )
  ```

---

## Strings

**Sempre f-strings** para interpolação. Não `.format()` nem `%`.

```python
# ✅
mensagem = f"Foram detectados {n_incidentes:,} incidentes em {mes}"

# ❌
mensagem = "Foram detectados {} incidentes em {}".format(n_incidentes, mes)
mensagem = "Foram detectados %d incidentes em %s" % (n_incidentes, mes)
```

Para strings de múltiplas linhas, usar `textwrap.dedent` ou parênteses:

```python
mensagem = (
    f"Resumo do dia {data}:\n"
    f"- Total de incidentes: {total}\n"
    f"- OLAs estourados: {ola_estourados}"
)
```

---

## Docstrings

Estilo **Google** (mais legível que NumPy para projetos pequenos).

### Quando obrigatória
- Toda **função pública** (sem prefixo `_`)
- Toda **classe pública**
- Todo **módulo importado** (docstring no topo do arquivo)

### Quando opcional
- Funções privadas (`_funcao`) — só se a lógica não for óbvia pelo nome
- Funções de notebook — só se forem reutilizadas em mais de uma célula

### Padrão

```python
def calcular_ola_estourado(
    df: pd.DataFrame,
    prioridade: str,
    limite_horas: int,
) -> pd.DataFrame:
    """Identifica incidentes com OLA estourado para uma dada prioridade.

    Aplica filtro de incidente pai antes do cálculo (regra confirmada
    pela Locaweb: filhos não entram no KPI).

    Args:
        df: DataFrame com todos os incidentes do dataset.
        prioridade: Código da prioridade ("P1", "P2", "P3", "P4", "P5").
        limite_horas: Tempo máximo permitido em horas para resolução.

    Returns:
        DataFrame contendo apenas os incidentes que estouraram OLA.

    Raises:
        ValueError: Se a prioridade não for um dos códigos válidos.
    """
    if prioridade not in {"P1", "P2", "P3", "P4", "P5"}:
        raise ValueError(f"Prioridade inválida: {prioridade}")
    ...
```

---

## Type hints

**Obrigatório** em código de produção (módulos `src/`, `web/`).
**Opcional** em código exploratório de notebook (mas recomendado para funções reutilizadas).

### Tipos básicos

```python
def soma(a: int, b: int) -> int: ...

def carregar_dados(caminho: str | Path) -> pd.DataFrame: ...

def filtrar_pais(df: pd.DataFrame, *, inplace: bool = False) -> pd.DataFrame | None: ...
```

### Tipos do pandas / numpy

```python
import pandas as pd
import numpy as np

def normalizar(serie: pd.Series) -> pd.Series: ...
def media_movel(arr: np.ndarray, janela: int = 7) -> np.ndarray: ...
```

### Optional vs `T | None`

Preferir `T | None` (sintaxe moderna, Python 3.10+):

```python
def buscar_incidente(numero: str) -> dict | None:  # ✅
def buscar_incidente(numero: str) -> Optional[dict]:  # ❌ legado
```

---

## Funções

### Funções pequenas e com responsabilidade única

```python
# ✅ Pequeno e focado
def filtrar_pais(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna apenas incidentes pais (sem 'Incidente Pai' preenchido)."""
    return df[df['Incidente Pai'].isna()]

def filtrar_kpi(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna apenas incidentes que entraram no KPI."""
    return df[df['Entrou para KPI?'] == 'SIM']
```

### Argumentos nomeados após os 3 primeiros

Funções com mais de 3 argumentos: usar `*` pra forçar nomeação:

```python
def treinar_modelo(
    df: pd.DataFrame,
    target: str,
    features: list[str],
    *,
    test_size: float = 0.2,
    random_state: int = 42,
    verbose: bool = False,
) -> XGBRegressor:
    ...
```

Uso fica explícito:
```python
modelo = treinar_modelo(df, 'volume', features, test_size=0.3, verbose=True)
```

### Evitar argumentos mutáveis como default

```python
# ❌ Bug clássico — lista é compartilhada entre chamadas
def adicionar(item, lista=[]):
    lista.append(item)
    return lista

# ✅
def adicionar(item, lista: list | None = None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista
```

---

## Classes

Usar classes quando:
- Tem estado que persiste entre chamadas (modelo treinado, configuração)
- Tem várias funções relacionadas operando no mesmo dado
- Vai injetar como serviço Django

Não usar classes só pra agrupar funções sem estado — módulo basta.

### Padrão

```python
class CronosForecaster:
    """Previsão de volume de incidentes via Prophet + XGBoost."""

    def __init__(
        self,
        prophet_params: dict | None = None,
        xgb_params: dict | None = None,
    ) -> None:
        self.prophet_params = prophet_params or {}
        self.xgb_params = xgb_params or {}
        self._prophet_model: Prophet | None = None
        self._xgb_model: XGBRegressor | None = None

    def fit(self, df: pd.DataFrame) -> "CronosForecaster":
        """Treina os dois modelos. Retorna self para encadeamento."""
        ...
        return self

    def predict(self, horizon_days: int = 7) -> pd.DataFrame:
        """Previsão D+1 até D+horizon_days."""
        ...
```

---

## Tratamento de erros

### Levantar exceções específicas, não `Exception` genérica

```python
# ❌
raise Exception("Coluna não encontrada")

# ✅
raise KeyError(f"Coluna '{coluna}' não encontrada no DataFrame")
raise ValueError(f"Prioridade inválida: {prioridade}")
```

### Não capturar exceções silenciosamente

```python
# ❌ Engole o erro
try:
    resultado = operacao_arriscada()
except:
    pass

# ✅ Captura específico e age
try:
    resultado = operacao_arriscada()
except FileNotFoundError as e:
    logger.warning(f"Arquivo não encontrado: {e}")
    resultado = valor_default
```

---

## Ferramentas recomendadas

### Formatador: **Black**
- Roda automaticamente, sem discussão
- Limite 88 caracteres
- Setup: `pip install black` → `black .`

### Linter: **Ruff**
- Linter rápido (substitui flake8, isort, pylint para 90% dos casos)
- Setup: `pip install ruff` → `ruff check .`

### Configuração mínima `pyproject.toml`

```toml
[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "F", "I", "N", "UP", "B"]
```

---

## Padrões específicos do projeto

### 1. Sempre filtrar pai antes de análise de OLA/KPI

```python
# ✅ Padrão correto
df_pai = df[df['Incidente Pai'].isna()]
df_kpi = df_pai[df_pai['Entrou para KPI?'] == 'SIM']
df_ola_p2 = df_kpi[df_kpi['Prioridade'] == '2-Alta']
```

### 2. Features de calendário sempre via lib `holidays`

```python
import holidays

br_holidays = holidays.country_holidays('BR')

df['is_feriado'] = df['Aberto'].dt.date.isin(br_holidays)
df['dia_semana'] = df['Aberto'].dt.day_name()
df['is_fim_semana'] = df['Aberto'].dt.dayofweek >= 5
```

### 3. Datas sempre como `pd.Timestamp`, não string

```python
df['Aberto'] = pd.to_datetime(df['Aberto'])
df['Resolvido'] = pd.to_datetime(df['Resolvido'], errors='coerce')
```

### 4. Constantes do domínio centralizadas

Quando criar `src/constants.py`:
```python
OLA_LIMITES_HORAS = {
    'P1-Crítica':     4,
    'P2-Alta':        4,
    'P3-Média':      12,
    'P4-Baixa':      24,
    'P5-Muito Baixa': 96,
}

PRIORIDADES_KPI = {'P1-Crítica', 'P2-Alta', 'P3-Média'}
```
