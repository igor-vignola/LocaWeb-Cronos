# -*- coding: utf-8 -*-
"""Taxa de quebra de OLA por familiaridade, dentro de prioridade e de origem da abertura.

Reproduz a figura 04 da seção 4.6 do `notebooks/05_causas_recorrentes.ipynb`, que no deck
entra como `figs/rec_controles.png`. Três mudanças em relação à saída do notebook:

* os dois painéis usam a mesma forma (barras agrupadas por faixa de familiaridade), em vez
  de barras à esquerda e quatro linhas à direita, porque o slide passou a exibir a figura em
  largura cheia e as quatro linhas com dois tracejados ficavam ilegíveis nesse tamanho;
* a taxa agregada de cada série entra como linha tracejada de referência, que é o contraste
  que sustenta a leitura: no agregado uma série está acima da outra, dentro das faixas de
  menor familiaridade a ordem inverte;
* corpo de texto maior, calibrado para a figura ocupando 1.472 px de largura no slide.

Todo número é conferido contra o output do notebook por `assert`, incluídos os que a figura
não desenha. As duas taxas agregadas por origem (manual e monitoramento) são calculadas
aqui: o notebook publica a composição das quebras por origem (81,4% contra 63,6%), e não a
taxa marginal de cada uma.

Saem dois arquivos, com o mesmo conteúdo em duas proporções, porque as duas composições de
slide em avaliação dão alturas diferentes à figura:

* `rec_controles_r6.png`, 2,7:1, para o slide que ainda leva cartões embaixo;
* `rec_controles_r6b.png`, 2,3:1, para o slide em que a figura vai até o pé.

Uso:
    .venv/Scripts/python scripts/figura_controles.py
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
PARQUET = RAIZ / "data" / "interim" / "incidentes_kpi.parquet"
SAIDA = RAIZ / "prototipos" / "slides" / "mvp" / "deck" / "figs"

AZUL = "#2563EB"
VERMELHO = "#DC2626"
GRAFITE = "#3F4757"
CINZA = "#888888"
CINZA_ESCURO = "#444444"
CINZA_CLARO = "#A8B0BE"

# O corte é o relógio da aplicação: 01/10/2025. Mesmo recorte do notebook 05.
CORTE = pd.Timestamp("2025-10-01")
FAIXAS = [0, 1, 4, 19, 10**9]
ROTULOS = ["único", "2 a 4", "5 a 19", "20 ou mais"]


def estilo() -> None:
    mpl.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": CINZA_ESCURO,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 16,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 14,
        "axes.labelsize": 13,
        "axes.labelcolor": CINZA_ESCURO,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": "#E5E5E5",
        "grid.linewidth": 0.6,
        "xtick.color": CINZA,
        "ytick.color": CINZA,
        "xtick.labelsize": 13,
        "ytick.labelsize": 12,
        "font.family": "sans-serif",
        "font.sans-serif": ["Sora", "Segoe UI", "DejaVu Sans"],
        "font.size": 12,
        "legend.frameon": False,
        "legend.fontsize": 12.5,
    })
    plt.rcParams["axes.grid.axis"] = "y"


def normaliza(texto: str) -> str:
    """Substitui identificadores de ativo e números por marcadores. Igual ao notebook 05."""
    s = re.sub(r"IC\d{4,}", "<ativo>", str(texto))
    s = re.sub(r"\d+", "<n>", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def fmt(x: float, casas: int = 2) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


def base() -> pd.DataFrame:
    bruto = pd.read_parquet(PARQUET)
    bruto["violou"] = (bruto["KPI Violado?"] == "SIM").astype(int)
    assert len(bruto) == 25_600, f"esperadas 25.600 linhas, encontradas {len(bruto)}"

    df = bruto[(bruto["dia"].dt.year == 2025) & (bruto["dia"] < CORTE)].copy()
    df["pri"] = "P" + df["Prioridade"].astype(str).str[0]
    df["problema"] = df["Descrição resumida"].map(normaliza)
    df["vezes"] = df["problema"].map(df["problema"].value_counts())
    df["familiaridade"] = pd.cut(df["vezes"], FAIXAS, labels=ROTULOS)

    assert len(df) == 19_973, f"esperados 19.973 incidentes no recorte, obtidos {len(df)}"
    assert int(df["violou"].sum()) == 188, f"esperadas 188 quebras, obtidas {df['violou'].sum()}"
    return df


def taxas(df: pd.DataFrame, coluna: str, valor: str) -> pd.Series:
    """Taxa de quebra (%) por faixa de familiaridade, dentro de um nível da variável."""
    s = df[df[coluna] == valor]
    g = s.groupby("familiaridade", observed=True)["violou"].mean() * 100
    return g.reindex(ROTULOS).round(2)


def marginal(df: pd.DataFrame, coluna: str, valor: str) -> float:
    s = df[df[coluna] == valor]
    return round(s["violou"].mean() * 100, 2)


def painel(ax, series: list[tuple[str, pd.Series, str]], titulo: str, agregados: list[float],
           ylim: float, com_ylabel: bool) -> None:
    pos = np.arange(len(ROTULOS))
    largura = 0.34
    chaves = []
    for i, ((rotulo, valores, cor), agregado) in enumerate(zip(series, agregados)):
        deslocamento = (i - 0.5) * largura
        barras = ax.bar(pos + deslocamento, valores.values, largura, color=cor, label=rotulo)
        for x, v in zip(pos + deslocamento, valores.values):
            ax.text(x, v + ylim * 0.022, fmt(v), ha="center", fontsize=11.5,
                    fontweight="bold", color=CINZA_ESCURO)
        # A taxa agregada da série entra como referência: é dela que sai a leitura que o
        # estrato desmente. O valor fica na legenda, e não sobre a linha, porque rótulo
        # dentro da área do gráfico colidia com o número da barra vizinha.
        linha = ax.axhline(agregado, color=cor, lw=1.3, ls=(0, (5, 4)), alpha=0.6, zorder=1)
        linha.set_label(f"agregado {fmt(agregado)}%")
        chaves += [barras, linha]

    ax.set_xticks(pos)
    ax.set_xticklabels(ROTULOS)
    ax.set_ylim(0, ylim)
    ax.set_xlabel("vezes que o mesmo problema aparece na base")
    if com_ylabel:
        ax.set_ylabel("taxa de quebra de OLA (%)")
    ax.set_title(titulo, loc="left", color="#0B1220", pad=52)
    ax.legend(handles=chaves, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.135),
              columnspacing=2.6, handlelength=1.9, labelspacing=0.5)


def main() -> None:
    estilo()
    df = base()

    p2, p3 = taxas(df, "pri", "P2"), taxas(df, "pri", "P3")
    man = taxas(df, "Aberto por", "Manual")
    mon = taxas(df, "Aberto por", "Monitoramento")

    assert list(p2) == [2.11, 1.96, 0.81, 0.38], list(p2)
    assert list(p3) == [1.40, 1.33, 1.01, 0.29], list(p3)
    assert list(man) == [1.40, 1.50, 1.45, 0.14], list(man)
    assert list(mon) == [2.92, 1.17, 0.11, 0.38], list(mon)

    ag_p2, ag_p3 = marginal(df, "pri", "P2"), marginal(df, "pri", "P3")
    ag_man = marginal(df, "Aberto por", "Manual")
    ag_mon = marginal(df, "Aberto por", "Monitoramento")
    assert (ag_p2, ag_p3) == (0.84, 0.97), (ag_p2, ag_p3)

    comp = pd.crosstab(df["familiaridade"], df["pri"], normalize="index") * 100
    comp_o = pd.crosstab(df["familiaridade"], df["Aberto por"], normalize="index") * 100
    assert round(comp.loc["único", "P2"], 1) == 7.5, comp.loc["único", "P2"]
    assert round(comp_o.loc["único", "Manual"], 1) == 96.4, comp_o.loc["único", "Manual"]

    SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, tamanho in (("rec_controles_r6", (13.4, 5.0)),
                          ("rec_controles_r6b", (12.4, 5.4))):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=tamanho)
        painel(ax1,
               [("P2 (alta)", p2, VERMELHO), ("P3 (média)", p3, AZUL)],
               "Taxa de quebra por prioridade", [ag_p2, ag_p3], 3.35, True)
        painel(ax2,
               [("Manual", man, GRAFITE), ("Monitoramento", mon, CINZA_CLARO)],
               "Taxa de quebra por origem da abertura", [ag_man, ag_mon], 3.35, False)
        fig.tight_layout(w_pad=3.2)
        fig.savefig(SAIDA / f"{nome}.png", dpi=200, bbox_inches="tight", facecolor="white")
        plt.close(fig)

    print("taxa por faixa de familiaridade (%):")
    print(pd.DataFrame({"P2": p2, "P3": p3, "Manual": man, "Monitoramento": mon}).to_string())
    print()
    print(f"agregado: P2 {fmt(ag_p2)}%  P3 {fmt(ag_p3)}%  "
          f"Manual {fmt(ag_man)}%  Monitoramento {fmt(ag_mon)}%")
    print(f"composição da faixa 'único': {fmt(comp.loc['único', 'P2'], 1)}% é P2, "
          f"{fmt(comp_o.loc['único', 'Manual'], 1)}% é manual")
    print("gravado: rec_controles_r6.png e rec_controles_r6b.png em", SAIDA)


if __name__ == "__main__":
    main()
