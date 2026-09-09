# -*- coding: utf-8 -*-
"""Gera o acumulado de quebras de OLA mês a mês em 2025, contra o limite do ano.

É a história do slide 4: a prioridade 3 fecha o ano com folga e a prioridade 2
atravessa o limite em novembro. Em outubro ela estava em 35, dentro; novembro
somou seis de uma vez e o ano fechou em 42, com limite de 39.

A escada de notas do dicionário (150%, 125%, 100%…) fica de fora de propósito.
O dono do projeto disse que ela confunde, e para a mensagem do slide basta uma
linha: o limite do ano. Quem quiser a escada tem a resposta em PERGUNTAS.md.

Tudo sai de data/interim/incidentes_kpi.parquet.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_figuras_ano.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"
PARQUET = AQUI.parents[2] / "data" / "interim" / "incidentes_kpi.parquet"

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
# limite anual de violações para a nota cheia, do dicionário de dados da Locaweb
LIMITE = {"P2": 39, "P3": 263}

COR = {"linha": "#0B1220", "estouro": "#DC2626", "limite": "#8A94A6",
       "dentro": "#15A05B", "cinza": "#888888", "grade": "#E7EBF1"}


def estilo() -> None:
    mpl.rcParams.update({
        "figure.dpi": 100, "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": "#444444", "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 14.5, "axes.titleweight": "bold",
        "axes.titlelocation": "left", "axes.titlepad": 13,
        "axes.labelsize": 12, "axes.labelcolor": "#444444",
        "axes.grid": True, "axes.axisbelow": True,
        "grid.color": COR["grade"], "grid.linewidth": 0.7,
        "xtick.color": COR["cinza"], "ytick.color": COR["cinza"],
        "xtick.labelsize": 11.5, "ytick.labelsize": 11.5,
        "font.family": "sans-serif",
        "font.sans-serif": ["Sora", "Outfit", "Inter", "DejaVu Sans"],
        "font.size": 12, "legend.frameon": False, "legend.fontsize": 12,
    })
    plt.rcParams["axes.grid.axis"] = "y"


def painel(ax, cum: np.ndarray, pri: str, titulo: str) -> None:
    x = np.arange(12)
    limite = LIMITE[pri]
    topo = max(cum[-1] * 1.28, limite * 1.22)
    estourou = cum[-1] > limite

    # o limite do ano: uma linha só, sem escada de notas
    ax.axhline(limite, color=COR["limite"], linewidth=1.4, linestyle=(0, (5, 4)), zorder=2)
    ax.text(11.4, limite, f"limite\n{limite}", va="center", ha="left", fontsize=11.5,
            color=COR["limite"], fontweight="bold", linespacing=1.25)

    ax.plot(x, cum, color=COR["linha"], linewidth=2.6, marker="o", markersize=6,
            markerfacecolor="white", markeredgewidth=2.2, zorder=4)

    if estourou:
        # o trecho que atravessa, em vermelho: é o slide inteiro num ponto só
        corta = int(np.argmax(cum > limite))
        ax.plot(x[corta - 1:], cum[corta - 1:], color=COR["estouro"], linewidth=3,
                marker="o", markersize=6, markerfacecolor="white", markeredgewidth=2.2,
                zorder=5)
        ax.annotate(f"+{cum[corta] - cum[corta-1]} em um mês",
                    xy=(corta, cum[corta]), xytext=(corta - 4.4, cum[corta] * 1.1),
                    fontsize=12.5, color=COR["estouro"], fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=COR["estouro"], linewidth=1.5))

    fecha = COR["estouro"] if estourou else COR["dentro"]
    ax.annotate(f"{cum[-1]}", xy=(11, cum[-1]), xytext=(0, 11), textcoords="offset points",
                ha="center", fontsize=15, fontweight="bold", color=fecha)

    ax.set_title(titulo, color="#0B1220")
    ax.set_xticks(list(x)); ax.set_xticklabels(MESES)
    ax.set_ylim(0, topo); ax.set_xlim(-0.5, 12.6)
    ax.set_ylabel("quebras acumuladas no ano")


def main() -> int:
    from PIL import Image

    FIGS.mkdir(parents=True, exist_ok=True)
    estilo()
    d = pd.read_parquet(PARQUET)
    d["v"] = d["KPI Violado?"].astype(str).str.upper().eq("SIM")
    d["pri"] = d["Prioridade"].astype(str).str.extract(r"(\d)")[0].map({"2": "P2", "3": "P3"})
    d25 = d[d.ano == 2025]

    fig, eixos = plt.subplots(1, 2, figsize=(13.0, 4.6))
    for ax, (pri, titulo) in zip(eixos, (
            ("P2", "Prioridade 2 · passou do limite em novembro"),
            ("P3", "Prioridade 3 · fechou o ano dentro"))):
        cum = (d25[d25.pri == pri].groupby("mes")["v"].sum()
               .reindex(range(1, 13), fill_value=0).cumsum().to_numpy())
        painel(ax, cum, pri, titulo)
        print(f"  {pri}: " + " ".join(f"{m}={v}" for m, v in zip(MESES, cum)))
    fig.subplots_adjust(wspace=0.22)

    destino = FIGS / "11_ano_virou.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    w, h = Image.open(destino).size
    print(f"\n  {destino.name:22s} {w}x{h}px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
