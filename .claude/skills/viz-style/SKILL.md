---
name: viz-style
description: "Padrão visual obrigatório dos gráficos do projeto Cronos. SEMPRE consulte antes de gerar qualquer visualização. Use quando o usuário mencionar: gráfico, plot, plotly, matplotlib, seaborn, visualização, chart, figura, dashboard, ou pedir para 'plotar', 'gerar gráfico', 'visualizar'. Garante que os gráficos da AED e do dashboard sigam a identidade visual Cronos."
---

# Padrão de Visualizações — Cronos

Todos os gráficos do projeto seguem este padrão. Garante unidade visual entre os notebooks, o PPT e o dashboard final.

## Paleta oficial

| Uso | Cor | Hex |
|-----|-----|-----|
| Texto principal, séries neutras | Preto | `#000000` |
| Texto secundário, eixos | Cinza escuro | `#444444` |
| Linhas de grid, anotações | Cinza médio | `#888888` |
| Fundo de painéis claros, separadores | Cinza claríssimo | `#F7F7F7` |
| Fundo | Branco | `#FFFFFF` |
| **Accent** — destaque, série principal | **Azul Cronos** | `#2563EB` |
| **Perigo** — KPIs críticos, OLAs estourados | **Vermelho** | `#DC2626` |
| Sucesso (uso pontual) | Verde | `#16A34A` |
| Atenção (uso pontual) | Amarelo | `#D97706` |

## Regras de uso da cor

1. **Cinza é o default.** Se a cor não está comunicando nada específico, use cinza.
2. **Azul `#2563EB` é a cor de destaque.** Use para a série principal ou para chamar atenção a uma linha/barra específica.
3. **Vermelho `#DC2626` é APENAS para perigo/crítico.** OLA estourado, KPI em risco, anomalia confirmada. Nunca usar como cor decorativa.
4. **Sem arco-íris.** Não usar paletas categóricas tipo `plotly.colors.qualitative.Plotly` que jogam 8 cores aleatórias.
5. **Para múltiplas categorias**, usar gradiente de cinza ou escala monocromática de azul.

## Tipografia

- **Fonte:** Sora (Google Fonts) quando disponível. Fallback: Inter, system-ui.
- **Título do gráfico:** 16-18pt, peso bold, preto
- **Subtítulo (se houver):** 12-13pt, peso regular, cinza escuro
- **Eixos (labels):** 12pt, peso regular, cinza escuro
- **Ticks dos eixos:** 10-11pt, cinza médio
- **Anotações:** 10pt, cinza escuro
- **Legenda:** 11pt

## Regras de layout

- **Fundo:** branco. Sem grid colorido, sem padrão de quadriculado.
- **Grid:** ativo apenas no eixo Y, cor `#E5E5E5`, linha fina (0.5px).
- **Bordas (spines):** remover top e right. Manter bottom e left em cinza médio.
- **Padding interno generoso.** Não amontoar.
- **Título à esquerda** (alinhado com o início do eixo Y), não centralizado.
- **Sem 3D, sem sombras, sem efeitos.** Flat e limpo.

## Setup Matplotlib

Cole esta função no início de qualquer notebook (ou em `notebooks/_setup.py`):

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

CRONOS_COLORS = {
    'black':      '#000000',
    'dark_gray':  '#444444',
    'mid_gray':   '#888888',
    'light_gray': '#F7F7F7',
    'white':      '#FFFFFF',
    'accent':     '#2563EB',  # azul
    'danger':     '#DC2626',  # vermelho
    'success':    '#16A34A',
    'warning':    '#D97706',
}

def setup_cronos_style():
    """Aplica o estilo visual do Cronos ao Matplotlib."""
    mpl.rcParams.update({
        'figure.figsize': (10, 5),
        'figure.dpi': 100,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.edgecolor': '#444444',
        'axes.linewidth': 0.8,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.titlelocation': 'left',
        'axes.titlepad': 16,
        'axes.labelsize': 12,
        'axes.labelcolor': '#444444',
        'axes.grid': True,
        'axes.axisbelow': True,
        'grid.color': '#E5E5E5',
        'grid.linewidth': 0.5,
        'xtick.color': '#888888',
        'ytick.color': '#888888',
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Sora', 'Inter', 'DejaVu Sans'],
        'font.size': 11,
        'legend.frameon': False,
        'legend.fontsize': 11,
        # Remove grid do eixo X (só eixo Y tem grid)
    })
    plt.rcParams['axes.grid.axis'] = 'y'

setup_cronos_style()
```

## Setup Plotly

```python
import plotly.io as pio
import plotly.graph_objects as go

CRONOS_TEMPLATE = go.layout.Template(
    layout=dict(
        font=dict(family='Sora, Inter, sans-serif', size=12, color='#444444'),
        title=dict(font=dict(size=18, color='#000000'), x=0.02, xanchor='left'),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            linecolor='#444444',
            tickcolor='#888888',
            tickfont=dict(size=11, color='#888888'),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            gridwidth=0.5,
            linecolor='#444444',
            tickcolor='#888888',
            tickfont=dict(size=11, color='#888888'),
        ),
        colorway=['#2563EB', '#000000', '#888888', '#DC2626', '#16A34A', '#D97706'],
    )
)
pio.templates['cronos'] = CRONOS_TEMPLATE
pio.templates.default = 'cronos'
```

## Padrões por tipo de gráfico

### Série temporal
- **Linha única importante** → azul `#2563EB`, espessura 2px
- **Comparação de séries** → uma em preto, uma em azul (não use 5 cores)
- **Mostrar anomalia** → linha em vermelho `#DC2626` apenas no trecho anômalo
- **Banda de confiança** → azul com `alpha=0.15`

### Barras
- **Categórico simples** → todas barras em cinza escuro `#444444`
- **Destaque** → uma barra em azul, demais em cinza claro
- **Negativo vs positivo** → vermelho para negativo, cinza ou azul para positivo

### Distribuição (histograma, KDE)
- Cor: cinza escuro `#444444` com borda branca fina
- Sem fill colorido em histograma de uma série só

### Heatmap
- Escala monocromática (`Blues` ou cinza). Não usar `viridis` ou `rainbow`.
- Texto dos valores em preto sobre células claras, branco sobre células escuras.

## Anti-padrões (não fazer)

| ❌ Não fazer | ✅ Fazer em vez |
|------------|---------------|
| Gráficos 3D | Sempre 2D |
| Pizza com mais de 4 fatias | Barras horizontais ordenadas |
| Cores arco-íris pra séries | Cinza + 1 cor de destaque |
| Título centralizado | Título à esquerda |
| Grid em ambos eixos | Grid só no eixo Y |
| Borda em todos os lados | Apenas bottom + left |
| Legenda dentro de caixa com fundo | Legenda sem frame |
| Sombras, efeitos, gradientes | Flat puro |
| `plt.style.use('ggplot')` | `setup_cronos_style()` |

## Salvando figuras

Sempre salvar em alta resolução para uso no PPT:

```python
fig.savefig(
    'figures/01_eda/distribuicao_temporal.png',
    dpi=200,
    bbox_inches='tight',
    facecolor='white',
)
```

Ou Plotly:
```python
fig.write_image('figures/01_eda/distribuicao_temporal.png', width=1200, height=600, scale=2)
```

Diretório padrão de figuras: `notebooks/figures/<numero_notebook>/`

## Checklist antes de mostrar um gráfico

- [ ] Título à esquerda, claro, sem jargão
- [ ] Eixos com labels descritivos (não "x" e "y")
- [ ] Unidade de medida indicada onde aplicável
- [ ] Cor está comunicando algo (não decorativa)
- [ ] Anotações em pontos importantes (anomalia, máximo, marco)
- [ ] Fonte dos dados mencionada se vier de fora
- [ ] Salvo em alta resolução se for pro PPT
