# -*- coding: utf-8 -*-
"""Gera a curva de ganho da fila de risco, com as regras simples como comparação.

O que o gráfico responde: percorrendo a fila do começo, quantas quebras de prazo
você encontra? E o que aconteceria se a fila fosse ordenada por uma regra simples
em vez do modelo?

Cinco ordenações, todas recomputadas de data/interim/04_fila_pontuada.parquet:

    modelo de risco      pela pontuação da regressão logística
    ativo crônico        pelo número de quebras que o ativo já teve
    por time             pela taxa histórica de quebra do time
    por prioridade       P2 antes de P3, que é o que a operação faz hoje
    sem ordenação        a diagonal, o que se acha pegando incidente ao caso

A cor aqui está comunicando qual ordenação é qual, então não é decoração. O azul
é o modelo, e a espessura maior é dele de propósito.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_figuras_fila.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"
PARQUET = AQUI.parents[2] / "data" / "interim" / "04_fila_pontuada.parquet"

COR = {
    "modelo": "#2563EB",
    "ativo": "#D97706",
    "time": "#16A34A",
    "prioridade": "#DC2626",
    "acaso": "#888888",
    "cinza_escuro": "#444444",
    "cinza_claro": "#E5E5E5",
    "preto": "#000000",
}
LIMITE = 400  # onde o ganho aparece; esticar até 5.183 achata tudo


def estilo() -> None:
    mpl.rcParams.update({
        "figure.dpi": 100, "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": COR["cinza_escuro"], "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 16, "axes.titleweight": "bold",
        "axes.titlelocation": "left", "axes.titlepad": 16,
        "axes.labelsize": 12.5, "axes.labelcolor": COR["cinza_escuro"],
        "axes.grid": True, "axes.axisbelow": True,
        "grid.color": COR["cinza_claro"], "grid.linewidth": 0.5,
        "xtick.color": "#888888", "ytick.color": "#888888",
        "xtick.labelsize": 12, "ytick.labelsize": 12,
        "font.family": "sans-serif",
        "font.sans-serif": ["Sora", "Outfit", "Inter", "DejaVu Sans"],
        "font.size": 12, "legend.frameon": False, "legend.fontsize": 12.5,
    })
    plt.rcParams["axes.grid.axis"] = "y"


def acumulado(ordem: pd.Series) -> np.ndarray:
    """Quebras encontradas conforme a fila avança, para uma ordenação."""
    return np.concatenate([[0], np.cumsum(ordem.to_numpy(dtype=float))])


def main() -> int:
    from PIL import Image

    FIGS.mkdir(parents=True, exist_ok=True)
    estilo()
    d = pd.read_parquet(PARQUET).copy()
    d["violou"] = d["violou"].astype(bool)
    total = int(d["violou"].sum())

    # taxa histórica por time, que é o que a regra por time usaria
    taxa_time = d.groupby("equipe")["violou"].mean()
    d["taxa_time"] = d["equipe"].map(taxa_time)
    # P2 antes de P3, que é o que a operação faz hoje
    d["ordem_pri"] = (d["prioridade"] == "P2").astype(int)

    ordenacoes = [
        ("modelo", "Fila do modelo de risco", ["risco"], [False], 3.2, "-"),
        ("ativo", "Regra: ativo mais crônico", ["ativo_violacoes"], [False], 2, "--"),
        ("time", "Regra: time com mais quebra", ["taxa_time"], [False], 2, "--"),
        ("prioridade", "Regra: prioridade 2 primeiro", ["ordem_pri"], [False], 2, "--"),
    ]

    fig, ax = plt.subplots(figsize=(12.8, 4.9))
    x = np.arange(LIMITE + 1)

    for chave, rotulo, por, asc, largura, traco in ordenacoes:
        # desempate estável pela ordem original, para a curva ser reprodutível
        s = d.sort_values(por + ["incidente"], ascending=asc + [True])
        ax.plot(x, acumulado(s["violou"])[: LIMITE + 1], color=COR[chave],
                linewidth=largura, linestyle=traco, label=rotulo,
                zorder=5 if chave == "modelo" else 3)

    # sem ordenação: a diagonal do acaso
    ax.plot(x, x * total / len(d), color=COR["acaso"], linewidth=1.6,
            linestyle=":", label="Sem ordenação", zorder=2)

    # a leitura em N=50 vai desenhada dentro do gráfico: é a resposta à
    # pergunta que a banca faz, que é por que não ordenar por prioridade
    ax.axvline(50, color=COR["acaso"], linewidth=1, linestyle=(0, (3, 3)),
               zorder=1)
    ax.annotate("13 das 50 quebras\nnos 50 primeiros", xy=(50, 13),
                xytext=(96, 19.4), fontsize=13, color=COR["modelo"],
                fontweight="bold", va="center",
                arrowprops=dict(arrowstyle="-", color=COR["modelo"],
                                linewidth=1.1, shrinkA=0, shrinkB=4))
    ax.annotate("nenhuma, ordenando\npor prioridade", xy=(50, 0),
                xytext=(96, 5.2), fontsize=13, color=COR["prioridade"],
                fontweight="bold", va="center",
                arrowprops=dict(arrowstyle="-", color=COR["prioridade"],
                                linewidth=1.1, shrinkA=0, shrinkB=4))

    ax.set_title("Quebras encontradas conforme a fila avança")
    ax.set_xlabel("incidentes percorridos na fila")
    ax.set_ylabel("quebras de prazo encontradas")
    ax.set_xlim(0, LIMITE)
    ax.set_ylim(0, 30)
    ax.set_xticks([0, 50, 100, 150, 200, 250, 300, 350, 400])
    ax.set_yticks([0, 5, 10, 15, 20, 25, 30])
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.17), ncol=5,
              columnspacing=1.6, handlelength=2.2)

    destino = FIGS / "07_fila_regras.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    w, h = Image.open(destino).size
    print(f"  {destino.name:24s} {w}x{h}px")
    print(f"\nbase de avaliação: {len(d):,} incidentes, {total} quebras"
          .replace(",", "."))
    print("\nquebras encontradas nos primeiros N da fila:")
    print(f"{'N':>6s} " + " ".join(f"{r:>14s}" for _, r, _, _, _, _ in ordenacoes)
          + f" {'sem ordenação':>14s}")
    for n in (25, 50, 100, 200, 400):
        linha = f"{n:>6d} "
        for chave, _, por, asc, _, _ in ordenacoes:
            s = d.sort_values(por + ["incidente"], ascending=asc + [True])
            linha += f"{int(acumulado(s['violou'])[n]):>14d} "
        linha += f"{n * total / len(d):>14.1f}"
        print(linha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
