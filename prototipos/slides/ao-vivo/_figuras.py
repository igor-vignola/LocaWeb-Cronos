# -*- coding: utf-8 -*-
"""Gera as figuras matplotlib do deck da banca, em alta resolução.

As figuras que existiam vinham dos notebooks com cerca de 1.100px de largura.
Exibidas em tela cheia no Teams ficavam moles, e foi o defeito que o dono do
projeto apontou duas vezes. Aqui elas nascem em dpi 200: uma figura de 10x5
polegadas sai com 2000x1000px e é exibida em cerca de 1000, o que dá 2x de
folga de resolução.

Segue o padrão da skill viz-style: cinza é o default, azul só para a série que
importa, vermelho só para perigo, grade apenas no eixo Y, título à esquerda,
sem borda em cima e à direita.

    01_salto_setembro.png   o volume total contra a série elegível, 2025
    02_elegiveis_por_ano.png  os elegíveis ao KPI em 2023, 2024 e 2025

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_figuras.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"

COR = {
    "preto": "#000000",
    "cinza_escuro": "#444444",
    "cinza_medio": "#888888",
    "cinza_claro": "#E5E5E5",
    "accent": "#2563EB",
    "perigo": "#DC2626",
}

MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]
TOTAL = [3714, 3553, 3588, 3202, 3329, 3558, 3448, 3996, 21561, 23017, 21524, 27321]
ELEGIVEL = [2357, 2282, 2130, 2072, 2247, 2105, 2126, 2330, 2324, 2126, 1634, 1423]
POR_ANO = {"2023": 87, "2024": 357, "2025": 25156}


def estilo() -> None:
    mpl.rcParams.update({
        "figure.dpi": 100,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": COR["cinza_escuro"],
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 17,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 18,
        "axes.labelsize": 12,
        "axes.labelcolor": COR["cinza_escuro"],
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": COR["cinza_claro"],
        "grid.linewidth": 0.5,
        "xtick.color": COR["cinza_medio"],
        "ytick.color": COR["cinza_medio"],
        "xtick.labelsize": 11.5,
        "ytick.labelsize": 11.5,
        "font.family": "sans-serif",
        "font.sans-serif": ["Sora", "Outfit", "Inter", "DejaVu Sans"],
        "font.size": 11.5,
        "legend.frameon": False,
        "legend.fontsize": 12,
    })
    plt.rcParams["axes.grid.axis"] = "y"


def salto_de_setembro() -> Path:
    """O total dispara e a série que entra no KPI não se move."""
    fig, ax = plt.subplots(figsize=(11, 5.0))
    x = range(12)

    # a faixa de setembro em diante, que é onde a instrumentação mudou
    ax.axvspan(7.5, 11.4, color=COR["perigo"], alpha=0.05, zorder=0)

    ax.plot(x, TOTAL, color=COR["cinza_escuro"], linewidth=2.2,
            marker="o", markersize=5, label="Volume total registrado")
    ax.plot(x, ELEGIVEL, color=COR["accent"], linewidth=2.8,
            marker="o", markersize=5, label="Série elegível ao KPI")

    ax.set_title("Volume mensal de incidentes em 2025")
    ax.set_ylabel("incidentes por mês")
    ax.set_xticks(list(x))
    ax.set_xticklabels(MESES)
    ax.set_xlim(-0.4, 11.4)
    ax.set_ylim(0, 30000)
    ax.set_yticks([0, 5000, 10000, 15000, 20000, 25000, 30000])
    ax.set_yticklabels(["0", "5 mil", "10 mil", "15 mil", "20 mil", "25 mil", "30 mil"])

    # a anotação que carrega a mensagem: o salto é monitoramento, não operação
    ax.annotate(
        "o monitoramento automático expande",
        xy=(8, 21561), xytext=(3.5, 26200),
        color=COR["cinza_escuro"], fontsize=12.5, fontweight="bold",
        ha="left", va="center",
        arrowprops=dict(arrowstyle="->", color=COR["cinza_escuro"],
                        linewidth=1.4, shrinkA=0, shrinkB=6,
                        connectionstyle="arc3,rad=-0.16"),
    )
    ax.annotate(
        "a série que entra\nno KPI não se move",
        xy=(8.45, 2324), xytext=(8.85, 8600),
        color=COR["accent"], fontsize=12.5, fontweight="bold",
        ha="left", va="center",
        arrowprops=dict(arrowstyle="->", color=COR["accent"],
                        linewidth=1.4, shrinkA=4, shrinkB=6,
                        connectionstyle="arc3,rad=-0.2"),
    )
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.13), ncol=2)

    destino = FIGS / "01_salto_setembro.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return destino


def elegiveis_por_ano() -> Path:
    """98% dos elegíveis estão em 2025; treinar nos três anos ensina alta falsa."""
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    anos = list(POR_ANO)
    vals = list(POR_ANO.values())
    cores = [COR["cinza_claro"], COR["cinza_claro"], COR["accent"]]

    barras = ax.bar(anos, vals, color=cores, width=0.58,
                    edgecolor="white", linewidth=1.2)
    for b, v in zip(barras, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 620, f"{v:,}".replace(",", "."),
                ha="center", va="bottom", fontsize=14, fontweight="bold",
                color=COR["preto"] if v > 1000 else COR["cinza_escuro"])

    ax.set_title("Incidentes elegíveis ao KPI, por ano")
    ax.set_ylabel("incidentes elegíveis")
    ax.set_ylim(0, 29000)
    ax.set_yticks([0, 5000, 10000, 15000, 20000, 25000])
    ax.set_yticklabels(["0", "5 mil", "10 mil", "15 mil", "20 mil", "25 mil"])
    ax.tick_params(axis="x", labelsize=13)

    destino = FIGS / "02_elegiveis_por_ano.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return destino


def main() -> int:
    FIGS.mkdir(parents=True, exist_ok=True)
    estilo()
    from PIL import Image

    for fn in (salto_de_setembro, elegiveis_por_ano):
        p = fn()
        w, h = Image.open(p).size
        print(f"  {p.name:28s} {w}x{h}px")

    pc = POR_ANO["2025"] / sum(POR_ANO.values()) * 100
    print(f"\n2025 concentra {pc:.1f}% dos elegíveis ao KPI")
    print(f"salto de agosto para setembro: {TOTAL[8] / TOTAL[7]:.1f}x no total, "
          f"{(ELEGIVEL[8] / ELEGIVEL[7] - 1) * 100:+.1f}% no elegível")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
