# -*- coding: utf-8 -*-
"""Figuras do bloco de abertura do deck da Sprint 3.

O bloco analítico de julho já tem as suas, exportadas dos notebooks. Estas aqui existem
porque os slides de contexto e problema estavam contando a história em cartão de texto, e
a história é uma curva: o ano do P2 parecia tranquilo até novembro.

Estilo casado com as figuras de julho: fundo branco, grade só no eixo Y, sem moldura em
cima e à direita, título à esquerda, azul `#2563EB` na série e vermelho `#DC2626` só onde
existe perigo de verdade.

Uso:
    .venv/Scripts/python scripts/figuras_deck.py
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BASE = RAIZ / "data" / "interim" / "incidentes_kpi.parquet"
SAIDA = RAIZ / "sprints" / "sprint-3" / "slides" / "figs"

AZUL = "#2563EB"
VERMELHO = "#DC2626"
VERDE = "#15A05B"
CINZA = "#888888"
CINZA_ESCURO = "#444444"

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

# Metas anuais de violação de OLA, do dicionário de dados da Locaweb. Cada tupla é
# (teto da faixa, nota que a faixa vale).
ESCADA = {
    "2": [(30, 150), (35, 125), (39, 100), (45, 75), (53, 50)],
    "3": [(200, 150), (230, 125), (263, 100), (290, 75), (320, 50)],
}


def estilo() -> None:
    mpl.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": CINZA_ESCURO,
        "axes.linewidth": 0.9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 15,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 14,
        "axes.labelsize": 11.5,
        "axes.labelcolor": CINZA_ESCURO,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": "#E8ECF2",
        "grid.linewidth": 0.8,
        "xtick.color": CINZA,
        "ytick.color": CINZA,
        "xtick.labelsize": 10.5,
        "ytick.labelsize": 10.5,
        "font.size": 11,
        "legend.frameon": False,
        "legend.fontsize": 10.5,
    })
    plt.rcParams["axes.grid.axis"] = "y"


def acumulado_2025() -> dict[str, list[int]]:
    """Violações de OLA acumuladas mês a mês em 2025, por prioridade."""
    df = pd.read_parquet(BASE)
    df.columns = [c.strip() for c in df.columns]
    ano = df[df["Aberto"].dt.year == 2025].copy()
    ano["viol"] = ano["KPI Violado?"].eq("SIM")
    ano["pri"] = ano["Prioridade"].str[0]

    saida = {}
    for pri in ("3", "2"):
        serie = ano[ano["pri"] == pri]
        mes = serie.groupby(serie["Aberto"].dt.month)["viol"].sum()
        saida[pri] = mes.reindex(range(1, 13), fill_value=0).cumsum().astype(int).tolist()
    return saida


def _painel(ax, pri: str, cum: list[int], titulo: str) -> None:
    x = range(12)
    degraus = ESCADA[pri]
    topo = max(cum[-1] * 1.35, degraus[2][0] * 1.15)

    # As faixas da meta desenhadas como fundo. É a régua da Locaweb, não uma escolha nossa.
    limites = [0] + [t for t, _ in degraus] + [topo]
    tons = ["#EAF6EF", "#F0F7F2", "#F7F7F5", "#FDF6E7", "#FBEDED", "#F8E4E4"]
    for i in range(len(limites) - 1):
        ax.axhspan(limites[i], min(limites[i + 1], topo), color=tons[i], zorder=0)

    for teto, nota in degraus:
        if teto > topo:
            continue
        ax.axhline(teto, color="#C9D2DE", linewidth=1, linestyle=(0, (4, 4)), zorder=1)
        ax.text(11.35, teto, f"{nota}%", va="center", ha="left",
                fontsize=10, color=CINZA, fontweight="bold")

    ax.plot(x, cum, color=AZUL, linewidth=2.6, marker="o", markersize=5.5,
            markerfacecolor="white", markeredgewidth=2, zorder=4, label="violações acumuladas")

    ax.set_title(titulo, color="#0B1220")
    ax.set_xticks(list(x))
    ax.set_xticklabels(MESES)
    ax.set_ylim(0, topo)
    ax.set_xlim(-0.4, 12.1)
    ax.set_ylabel("violações de OLA acumuladas no ano")


def figura_ano_virou(cum: dict[str, list[int]]) -> Path:
    """As duas prioridades contra a escada da meta, mês a mês."""
    fig, (a3, a2) = plt.subplots(1, 2, figsize=(13.6, 4.9))

    _painel(a3, "3", cum["3"], "P3 · fechou o ano na melhor faixa")
    a3.annotate(
        f"fecha em {cum['3'][-1]}, abaixo de 201.\nO ano inteiro valeu 150%.",
        xy=(11, cum["3"][-1]), xytext=(6.1, cum["3"][-1] * 0.42),
        fontsize=11, color=VERDE, fontweight="bold",
        arrowprops=dict(arrowstyle="-", color=VERDE, linewidth=1.2, alpha=.55),
    )

    _painel(a2, "2", cum["2"], "P2 · perdeu dois degraus em novembro")
    # Outubro fecha em 35, ainda na faixa de 125%. Novembro entra com 6 violações e
    # atravessa duas faixas de uma vez. É o slide inteiro num ponto só.
    a2.plot([9, 10], [cum["2"][9], cum["2"][10]], color=VERMELHO, linewidth=3.4, zorder=5)
    a2.plot([10], [cum["2"][10]], marker="o", markersize=8, color=VERMELHO, zorder=6)
    a2.annotate(
        f"novembro: +{cum['2'][10] - cum['2'][9]} violações.\n"
        f"De {cum['2'][9]} para {cum['2'][10]}, e a nota\ncai de 125% para 75%.",
        xy=(10, cum["2"][10]), xytext=(3.4, cum["2"][10] * 1.02),
        fontsize=11, color=VERMELHO, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=VERMELHO, linewidth=1.4),
    )

    fig.tight_layout(pad=1.4)
    SAIDA.mkdir(parents=True, exist_ok=True)
    destino = SAIDA / "ano_virou.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return destino


def main() -> None:
    estilo()
    cum = acumulado_2025()
    print("P3 acumulado:", cum["3"])
    print("P2 acumulado:", cum["2"])
    destino = figura_ano_virou(cum)
    print("gravado:", destino)


if __name__ == "__main__":
    main()
