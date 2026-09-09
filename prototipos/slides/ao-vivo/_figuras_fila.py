# -*- coding: utf-8 -*-
"""Gera a curva de ganho da fila de risco, com as regras simples como comparação.

O que o gráfico responde: percorrendo a fila do começo, quantas quebras de prazo
você encontra? E o que aconteceria se a fila fosse ordenada por uma regra simples
em vez do modelo?

Cinco ordenações, todas recomputadas de data/interim/04_fila_pontuada.parquet:

    modelo de risco      pela pontuação da regressão logística
    time                 pela taxa histórica de quebra do time
    ativo crônico        pelo número de quebras que o ativo já teve
    prioridade           P2 antes de P3, que é o que a operação faz hoje
    sem ordenação        a diagonal, o que se acha pegando incidente ao acaso

Duas decisões de leitura, porque a primeira versão ficou difícil de entender:

  · o nome vai escrito na ponta de cada linha, e não numa legenda embaixo. Quem
    olha não precisa casar cor com rótulo.
  · cada ordenação tem a sua cor, com o nome na ponta na mesma cor. Uma versão
    toda em cinza ficou sem sal; a cor diz qual regra é qual sem legenda.

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
    "cinza_escuro": "#444444",
    "cinza_medio": "#888888",
    "cinza_claro": "#E5E5E5",
}
LIMITE = 400  # onde o ganho aparece; esticar até 5.183 achata tudo
LEITURA = 50  # a posição da fila que o slide lê em voz alta


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
        "xtick.color": COR["cinza_medio"], "ytick.color": COR["cinza_medio"],
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
    d["taxa_time"] = d["equipe"].map(d.groupby("equipe")["violou"].mean())
    d["ordem_pri"] = (d["prioridade"] == "P2").astype(int)

    # cada ordenação com a sua cor: a cor aqui diz qual regra é qual, e o dono do
    # projeto pediu as linhas coloridas de volta depois de uma versão toda em
    # cinza ter ficado sem sal. O azul continua sendo só do modelo, e é o traço
    # mais grosso.
    #        chave        nome na ponta          coluna             cor      traço  largura  desvio do rótulo
    linhas = [
        ("modelo", "Fila do modelo", ["risco"], COR["modelo"], "-", 3.4, 0),
        ("time", "Regra: time", ["taxa_time"], "#16A34A", (0, (6, 3)), 2.1, 0),
        ("ativo", "Regra: ativo crônico", ["ativo_violacoes"], "#D97706",
         (0, (6, 3)), 2.1, 0),
        ("acaso", "Sem ordenação", None, "#999999", (0, (1, 3)), 1.8, 8),
        ("prioridade", "Regra: prioridade 2", ["ordem_pri"], "#DC2626",
         (0, (2, 3)), 2.1, -8),
    ]

    fig, ax = plt.subplots(figsize=(12.2, 5.2))
    x = np.arange(LIMITE + 1)
    fim = {}

    for chave, nome, por, cor, traco, largura, desvio in linhas:
        if chave == "acaso":
            y = x * total / len(d)
        else:
            # desempate estável pela ordem original, para a curva ser reprodutível
            s = d.sort_values(por + ["incidente"], ascending=[False, True])
            y = acumulado(s["violou"])[: LIMITE + 1]
        ax.plot(x, y, color=cor, linewidth=largura, linestyle=traco,
                zorder=5 if chave == "modelo" else 3)
        fim[chave] = y[LIMITE]
        # o nome vai na ponta da linha, no lugar de uma legenda
        ax.annotate(nome, xy=(LIMITE, y[LIMITE]), xytext=(10, desvio),
                    textcoords="offset points", va="center", color=cor,
                    fontsize=13,
                    fontweight="bold" if chave == "modelo" else "normal")

    ax.axvline(LEITURA, color=COR["cinza_medio"], linewidth=1,
               linestyle=(0, (3, 3)), zorder=1)
    ax.annotate(f"{LEITURA} primeiros", xy=(LEITURA, 29.2), xytext=(7, 0),
                textcoords="offset points", va="top", fontsize=12.5,
                color=COR["cinza_medio"])

    ax.set_title("Quebras encontradas conforme a fila avança")
    ax.set_xlabel("incidentes percorridos na fila")
    ax.set_ylabel("quebras de prazo encontradas")
    ax.set_xlim(0, LIMITE)
    ax.set_ylim(0, 30)
    ax.set_xticks([0, 50, 100, 150, 200, 250, 300, 350, 400])
    ax.set_yticks([0, 5, 10, 15, 20, 25, 30])
    # espaço à direita para os nomes das pontas caberem
    fig.subplots_adjust(right=0.79)

    destino = FIGS / "07_fila_regras.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    w, h = Image.open(destino).size
    print(f"  {destino.name:24s} {w}x{h}px")
    print(f"\nbase de avaliação: {len(d):,} incidentes, {total} quebras"
          .replace(",", "."))
    print("\nquebras encontradas nos primeiros N da fila:")
    cabecalho = " ".join(f"{c:>12s}" for c, _, _, _, _, _, _ in linhas)
    print(f"{'N':>6s} {cabecalho}")
    for n in (25, 50, 100, 200, 400):
        linha = f"{n:>6d} "
        for chave, _, por, _, _, _, _ in linhas:
            if chave == "acaso":
                linha += f"{n * total / len(d):>12.1f} "
            else:
                s = d.sort_values(por + ["incidente"], ascending=[False, True])
                linha += f"{int(acumulado(s['violou'])[n]):>12d} "
        print(linha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
