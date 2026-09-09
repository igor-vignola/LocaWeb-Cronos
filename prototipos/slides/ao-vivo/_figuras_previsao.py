# -*- coding: utf-8 -*-
"""Gera o gráfico dos sete dias previstos pelo Prophet, com a faixa de cada dia.

É a saída do produto no instante em que o relógio do sistema está parado, 1º de
outubro de 2025: para cada dia, a faixa que o modelo dá, a previsão dentro dela
e o ponto do que de fato chegou. Treze dos quatorze pontos caem dentro.

Duas prioridades, dois painéis, o mesmo peso visual — regra 10 do CLAUDE.md. As
escalas são diferentes porque os volumes são diferentes, e o eixo de cada painel
diz isso.

Cor com significado, como manda a skill viz-style: azul é o modelo (faixa e
previsão), preto é o realizado, vermelho é só o ponto que caiu fora da faixa.

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

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"
PARQUET = AQUI.parents[2] / "data" / "interim" / "03_previsao_diaria.parquet"

INICIO, FIM = "2025-10-01", "2025-10-07"
DIA_SEMANA = ("seg", "ter", "qua", "qui", "sex", "sáb", "dom")

COR = {
    "modelo": "#2563EB",
    "realizado": "#000000",
    "fora": "#DC2626",
    "cinza_escuro": "#444444",
    "cinza_medio": "#888888",
    "cinza_claro": "#E5E5E5",
}


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
    """Desenha uma prioridade e devolve quantos dias caíram dentro da faixa."""
    x = np.arange(len(s))
    ax.fill_between(x, s.baixo, s.alto, color=COR["modelo"], alpha=0.15,
                    linewidth=0, label="Faixa prevista", zorder=2)
    ax.plot(x, s.valor, color=COR["modelo"], linewidth=2, marker="o",
            markersize=5, label="Previsão do modelo", zorder=4)

    dentro = (s.real >= s.baixo) & (s.real <= s.alto)
    ax.scatter(x[dentro.to_numpy()], s.real[dentro], s=58,
               color=COR["realizado"], zorder=5, label="O que chegou")
    if (~dentro).any():
        ax.scatter(x[(~dentro).to_numpy()], s.real[~dentro], s=58,
                   color=COR["fora"], zorder=6, label="Fora da faixa")

    ax.set_title(titulo)
    ax.set_ylabel("incidentes por dia")
    ax.set_ylim(0, topo)
    ax.set_xlim(-0.4, len(s) - 0.6)
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

    fig, eixos = plt.subplots(1, 2, figsize=(13.0, 4.6))
    total = 0
    for ax, (pri, topo) in zip(eixos, (("P2", 28), ("P3", 110))):
        s = d[d.prioridade == pri].sort_values("dia").reset_index(drop=True)
        total += painel(ax, s, f"Prioridade {pri[1]}", topo)

    # uma legenda só, embaixo, com as quatro chaves do painel da direita
    alcas, rotulos = eixos[1].get_legend_handles_labels()
    alcas_p2, rotulos_p2 = eixos[0].get_legend_handles_labels()
    for alca, rotulo in zip(alcas_p2, rotulos_p2):
        if rotulo not in rotulos:
            alcas.append(alca)
            rotulos.append(rotulo)
    fig.legend(alcas, rotulos, loc="lower center", ncol=4,
               bbox_to_anchor=(0.5, -0.055), columnspacing=2.2)
    fig.subplots_adjust(wspace=0.22)

    destino = FIGS / "08_previsao_7dias.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    w, h = Image.open(destino).size
    print(f"  {destino.name:26s} {w}x{h}px")
    print(f"\n{total} de {len(d)} dias caíram dentro da faixa")
    fora = d[(d.real < d.baixo) | (d.real > d.alto)]
    for _, r in fora.iterrows():
        print(f"  fora: {r.prioridade} {r.dia:%d/%m} chegaram {r.real:.0f} "
              f"contra um teto de {r.alto:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
