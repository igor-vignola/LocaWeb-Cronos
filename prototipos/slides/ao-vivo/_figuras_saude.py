# -*- coding: utf-8 -*-
"""Gera o ranking de saúde por produto: quinze notas de 0 a 100, da melhor à pior.

Duas figuras saem daqui:

    10_saude_ranking.png     o ranking, que é o que vai ao slide
    10_saude_quadrantes.png  o plano de quadrantes, guardado para perguntas

O ranking foi escolhido para o slide depois de julgar o plano de quadrantes:
o plano é elegante, mas os rótulos colidem, o tamanho das bolhas adiciona uma
terceira variável sem mensagem, e ele cria uma contradição na sala — o produto
de pior nota (lvps, 21,3) não cai na zona "agir primeiro", porque a taxonomia
dos quadrantes fala do TIPO do problema e a nota fala do TAMANHO. Explicar isso
em vinte segundos é armadilha. O ranking é o que a tela do sistema mostra e
qualquer pessoa lê em dois segundos.

Cor com significado: vermelho só para "problema já materializado", os demais em
três tons de cinza. Isso diz a situação sem virar arco-íris.

Tudo sai de data/interim/07_saude_produto.parquet. A nota soma P2 e P3; as
colunas separadas por prioridade ficam na tela do sistema.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_figuras_saude.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"
PARQUET = AQUI.parents[2] / "data" / "interim" / "07_saude_produto.parquet"

COR_QUADRANTE = {
    "problema já materializado": "#DC2626",
    "problema conhecido e recorrente": "#444444",
    "risco latente": "#8A8A8A",
    "estável": "#C4C4C4",
}
ROTULO = {
    "problema já materializado": "Problema já materializado",
    "problema conhecido e recorrente": "Problema conhecido e recorrente",
    "risco latente": "Risco latente",
    "estável": "Estável",
}


def estilo() -> None:
    mpl.rcParams.update({
        "figure.dpi": 100, "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": "#444444", "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 15, "axes.titleweight": "bold",
        "axes.titlelocation": "left", "axes.titlepad": 14,
        "axes.labelsize": 12.5, "axes.labelcolor": "#444444",
        "axes.grid": True, "axes.axisbelow": True,
        "grid.color": "#E5E5E5", "grid.linewidth": 0.5,
        "xtick.color": "#888888", "ytick.color": "#888888",
        "xtick.labelsize": 12, "ytick.labelsize": 12.5,
        "font.family": "sans-serif",
        "font.sans-serif": ["Sora", "Outfit", "Inter", "DejaVu Sans"],
        "font.size": 12, "legend.frameon": False, "legend.fontsize": 12.5,
    })


def ranking(d: pd.DataFrame) -> Path:
    plt.rcParams["axes.grid.axis"] = "x"
    s = d.sort_values("nota", ascending=True)  # a melhor fica em cima
    y = np.arange(len(s))
    cores = [COR_QUADRANTE[q] for q in s["quadrante"]]

    fig, ax = plt.subplots(figsize=(9.2, 6.4))
    ax.barh(y, s["nota"], color=cores, height=0.66, zorder=3)
    for yi, (produto, r) in zip(y, s.iterrows()):
        ax.text(r["nota"] + 1.2, yi, f"{r['nota']:.1f}".replace(".", ","),
                va="center", fontsize=12.5, color="#222222",
                fontweight="bold" if r["quadrante"].startswith("problema já") else "normal")
    ax.set_yticks(y)
    ax.set_yticklabels(s.index)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("nota de saúde, de 0 a 100")
    ax.set_title("Nota de saúde dos quinze produtos")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

    alcas = [plt.Rectangle((0, 0), 1, 1, color=COR_QUADRANTE[q]) for q in ROTULO]
    ax.legend(alcas, list(ROTULO.values()), loc="upper left",
              bbox_to_anchor=(0, -0.1), ncol=2, columnspacing=1.8)

    destino = FIGS / "10_saude_ranking.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return destino


def quadrantes(d: pd.DataFrame) -> Path:
    """O plano, guardado para perguntas. Sem tamanho de bolha, para os rótulos
    não colidirem."""
    plt.rcParams["axes.grid.axis"] = "y"
    x = d["prop_inedito"] * 100
    y = d["taxa_violacao"] * 100
    med_x, med_y = x.median(), y.median()
    desvio = {"lvps": (8, -4), "lsaa": (-34, 6), "lhvp": (8, 6), "lhco": (8, -10),
              "lrel": (8, 6), "lssl": (8, -10), "lrdo": (8, 4)}

    fig, ax = plt.subplots(figsize=(9.4, 6.2))
    ax.grid(False)
    ax.axvline(med_x, color="#BBBBBB", linewidth=1, linestyle=(0, (4, 3)))
    ax.axhline(med_y, color="#BBBBBB", linewidth=1, linestyle=(0, (4, 3)))
    for quadrante, cor in COR_QUADRANTE.items():
        m = d["quadrante"] == quadrante
        ax.scatter(x[m], y[m], s=90, color=cor, edgecolor="white", linewidth=1.2,
                   label=ROTULO[quadrante], zorder=5)
    for produto, r in d.iterrows():
        dx, dy = desvio.get(produto, (8, 4))
        ax.annotate(produto, (r["prop_inedito"] * 100, r["taxa_violacao"] * 100),
                    xytext=(dx, dy), textcoords="offset points", fontsize=11.5,
                    color=COR_QUADRANTE[r["quadrante"]])
    ax.set_title("Os quinze produtos no plano das duas medianas")
    ax.set_xlabel("problemas inéditos no produto, em % do que chega")
    ax.set_ylabel("taxa de perda de prazo, em %")
    ax.set_xlim(10, 75)
    ax.set_ylim(0, 3.2)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.13), ncol=2, columnspacing=1.8)

    destino = FIGS / "10_saude_quadrantes.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return destino


def main() -> int:
    from PIL import Image

    FIGS.mkdir(parents=True, exist_ok=True)
    estilo()
    d = pd.read_parquet(PARQUET)
    for destino in (ranking(d), quadrantes(d)):
        w, h = Image.open(destino).size
        print(f"  {destino.name:26s} {w}x{h}px")

    print("\npor situação:")
    for q, g in d.groupby("quadrante"):
        print(f"  {q:34s} {len(g)} produtos  {', '.join(sorted(g.index))}")
    print(f"melhor nota {d.nota.max():.1f} ({d.nota.idxmax()}), "
          f"pior {d.nota.min():.1f} ({d.nota.idxmin()}); "
          f"mediana {d.nota.median():.1f}; abaixo de 50: {(d.nota < 50).sum()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
