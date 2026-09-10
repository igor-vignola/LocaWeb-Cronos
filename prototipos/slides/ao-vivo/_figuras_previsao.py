# -*- coding: utf-8 -*-
"""Gera o gráfico dos sete dias previstos pelo Prophet, um dia por caixa.

Cada dia é uma caixa vertical que vai do piso ao teto da faixa prevista, com um
traço na previsão e um ponto no que de fato chegou. É a saída do produto no
instante em que o relógio do sistema está parado, 1º de outubro de 2025.

A forma em caixas foi pedida duas vezes pelo dono do projeto, no lugar de uma
linha com faixa sombreada: a caixa deixa claro que a previsão é um intervalo e
que cada dia é uma leitura independente.

Duas prioridades, dois painéis, o mesmo peso — regra 10. Escalas diferentes
porque os volumes são diferentes, e o eixo de cada painel diz isso.

Cor com significado: azul é o modelo (caixa e traço), preto é o realizado,
vermelho é só o ponto que caiu fora da faixa. Treze dos quatorze caem dentro.

Tudo sai de data/interim/03_previsao_diaria.parquet.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_figuras_previsao.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"
PARQUET = AQUI.parents[2] / "data" / "interim" / "03_previsao_diaria.parquet"

INICIO, FIM = "2025-10-01", "2025-10-07"
DIA_SEMANA = ("seg", "ter", "qua", "qui", "sex", "sáb", "dom")

COR = {
    "faixa": "#2563EB",
    "realizado": "#000000",
    "fora": "#DC2626",
    "cinza_escuro": "#444444",
    "cinza_medio": "#888888",
    "cinza_claro": "#E5E5E5",
}
LARGURA = 0.56  # largura da caixa, em fração do espaço do dia


def estilo() -> None:
    mpl.rcParams.update({
        "figure.dpi": 100, "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": COR["cinza_escuro"], "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 14, "axes.titleweight": "bold",
        "axes.titlelocation": "left", "axes.titlepad": 12,
        "axes.labelsize": 12, "axes.labelcolor": COR["cinza_escuro"],
        "axes.grid": True, "axes.axisbelow": True,
        "grid.color": COR["cinza_claro"], "grid.linewidth": 0.5,
        "xtick.color": COR["cinza_medio"], "ytick.color": COR["cinza_medio"],
        "xtick.labelsize": 12, "ytick.labelsize": 12,
        "font.family": "sans-serif",
        "font.sans-serif": ["Sora", "Outfit", "Inter", "DejaVu Sans"],
        "font.size": 12, "legend.frameon": False, "legend.fontsize": 12.5,
    })
    plt.rcParams["axes.grid.axis"] = "y"


def painel(ax, s: pd.DataFrame, titulo: str, topo: float) -> int:
    """Desenha uma prioridade em caixas e devolve quantos dias caíram dentro."""
    x = np.arange(len(s))
    # a caixa: do piso ao teto da faixa
    ax.bar(x, s.alto - s.baixo, bottom=s.baixo, width=LARGURA,
           color=COR["faixa"], alpha=0.16, linewidth=0, zorder=2)
    # o traço da previsão, dentro da caixa
    ax.hlines(s.valor, x - LARGURA / 2, x + LARGURA / 2, color=COR["faixa"],
              linewidth=3, zorder=4)
    # o realizado: ponto preto dentro, vermelho fora
    dentro = ((s.real >= s.baixo) & (s.real <= s.alto)).to_numpy()
    ax.scatter(x[dentro], s.real[dentro], s=70, color=COR["realizado"], zorder=5)
    if (~dentro).any():
        ax.scatter(x[~dentro], s.real[~dentro], s=70, color=COR["fora"], zorder=6)

    ax.set_title(titulo)
    ax.set_ylabel("incidentes no dia")
    ax.set_ylim(0, topo)
    ax.set_xlim(-0.6, len(s) - 0.4)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{DIA_SEMANA[d.weekday()]}\n{d:%d/%m}" for d in s.dia])
    return int(dentro.sum())


def main() -> int:
    from PIL import Image

    FIGS.mkdir(parents=True, exist_ok=True)
    estilo()
    d = pd.read_parquet(PARQUET)
    d["dia"] = pd.to_datetime(d["dia"])
    d = d[(d.tipo == "previsto") & (d.dia >= INICIO) & (d.dia <= FIM)]

    # duas proporcoes do mesmo desenho: a quadrada, que divide o slide com o
    # texto ao lado, e a larga, para a composicao em que a figura ocupa a
    # largura inteira e o texto vira uma linha embaixo.
    for nome, tamanho, espaco in (("08_previsao_7dias", (13.0, 5.0), 0.22),
                                  ("08_previsao_7dias_largo", (16.4, 4.4), 0.16)):
        total = desenha(d, nome, tamanho, espaco)
    return relatorio(d, total)


def desenha(d, nome, tamanho, espaco) -> int:
    from PIL import Image

    fig, eixos = plt.subplots(1, 2, figsize=tamanho)
    total = 0
    for ax, (pri, topo) in zip(eixos, (("P2", 28), ("P3", 110))):
        s = d[d.prioridade == pri].sort_values("dia").reset_index(drop=True)
        total += painel(ax, s, f"Prioridade {pri[1]}", topo)

    alcas = [
        Patch(facecolor=COR["faixa"], alpha=0.16, label="Faixa prevista para o dia"),
        Line2D([], [], color=COR["faixa"], linewidth=3, label="Previsão do modelo"),
        Line2D([], [], marker="o", color="none", markerfacecolor=COR["realizado"],
               markersize=9, label="O que chegou"),
        Line2D([], [], marker="o", color="none", markerfacecolor=COR["fora"],
               markersize=9, label="Fora da faixa"),
    ]
    fig.legend(handles=alcas, loc="lower center", ncol=4,
               bbox_to_anchor=(0.5, -0.1), columnspacing=2.2)
    fig.subplots_adjust(wspace=espaco)

    destino = FIGS / f"{nome}.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    w, h = Image.open(destino).size
    print(f"  {destino.name:30s} {w}x{h}px")
    return total


def relatorio(d, total) -> int:
    print(f"\n{total} de {len(d)} dias caíram dentro da faixa")
    fora = d[(d.real < d.baixo) | (d.real > d.alto)]
    for _, r in fora.iterrows():
        print(f"  fora: {r.prioridade} {r.dia:%d/%m} chegaram {r.real:.0f} "
              f"contra um teto de {r.alto:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
