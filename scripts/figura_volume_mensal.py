# -*- coding: utf-8 -*-
"""Volume mensal de incidentes, 2023 a 2025, para o slide da anomalia de setembro.

A figura existia só como saída da célula 18 do `notebooks/01_eda.ipynb`, e a cópia que o
deck usava tinha sido ajustada à mão depois disso, o que a deixava sem script que a
reproduzisse. Este arquivo devolve a reprodutibilidade e corrige as anotações, que
traziam a grandeza sem a unidade ("~4 mil" em vez de "4 mil incidentes").

Estilo idêntico ao do notebook: fundo branco, grade só no eixo Y, moldura só à esquerda e
embaixo, título à esquerda com subtítulo factual, azul `#2563EB` na série.

Uso:
    .venv/Scripts/python scripts/figura_volume_mensal.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "assets" / "Materal LocalWeb" / "LW-DATASET.xlsx"
SAIDA = RAIZ / "prototipos" / "slides" / "mvp" / "deck" / "figs"

AZUL = "#2563EB"
CINZA = "#888888"

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def estilo() -> None:
    mpl.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#444444",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 16,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 16,
        "axes.labelsize": 12,
        "axes.labelcolor": "#444444",
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": "#E5E5E5",
        "grid.linewidth": 0.5,
        "xtick.color": CINZA,
        "ytick.color": CINZA,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "font.family": "sans-serif",
        "font.sans-serif": ["Sora", "Segoe UI", "DejaVu Sans"],
        "font.size": 11,
        "legend.frameon": False,
        "legend.fontsize": 11,
    })
    plt.rcParams["axes.grid.axis"] = "y"


def rotulo_mes(ym: str) -> str:
    ano, mes = ym.split("-")
    return f"{MESES[int(mes) - 1]}/{ano}"


def pt(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def main() -> None:
    estilo()
    df = pd.read_excel(DADOS, sheet_name="Dataset Geral")
    vol = df.groupby(df["Aberto"].dt.to_period("M").astype(str)).size()
    n_23_24 = int((df["Aberto"].dt.year < 2025).sum())
    i_set = list(vol.index).index("2025-09")
    ago, set_ = int(vol["2025-08"]), int(vol["2025-09"])

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(range(len(vol)), vol.values, color=AZUL, lw=2.4)
    ax.scatter([i_set], [vol.iloc[i_set]], color=AZUL, s=45, zorder=3)
    ax.set_title("Volume mensal de incidentes (2023-2025)", loc="left", pad=34,
                 fontsize=15, fontweight="bold", color="#000000")
    ax.text(0, 1.04, "O volume fica baixo até agosto de 2025 e multiplica em setembro.",
            transform=ax.transAxes, fontsize=10.5, color="#5f5f5f", va="bottom")
    ax.set_ylabel("incidentes/mês")
    ax.set_xticks(range(0, len(vol), 3))
    ax.set_xticklabels([rotulo_mes(m) for m in vol.index[::3]], rotation=45, ha="right")

    # As anotações levam a unidade junto do número: sem ela, "4 mil" não diz 4 mil do quê.
    ax.annotate(
        f"set/2025: de {pt(ago)} para {pt(set_)} incidentes no mês",
        xy=(i_set, vol.iloc[i_set]), xytext=(i_set - 15, vol.iloc[i_set] * 0.72),
        fontsize=9, color=AZUL,
        arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.2),
    )
    ax.annotate(
        f"2023 e 2024: {pt(n_23_24)} incidentes no total",
        xy=(8, 300), xytext=(1, 9000), fontsize=9, color=CINZA,
        arrowprops=dict(arrowstyle="->", color=CINZA, lw=1),
    )

    fig.tight_layout()
    SAIDA.mkdir(parents=True, exist_ok=True)
    destino = SAIDA / "41_volume_mensal_r5.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"ago/2025: {pt(ago)} | set/2025: {pt(set_)} ({set_ / ago:.1f}x)")
    print(f"2023+2024: {pt(n_23_24)} de {pt(len(df))}")
    print("gravado:", destino)


if __name__ == "__main__":
    main()
