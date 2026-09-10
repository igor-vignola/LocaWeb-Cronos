# -*- coding: utf-8 -*-
"""Gera a decomposição da pontuação de risco de um incidente.

O deck da Sprint 3 tem esta figura (`figs/risco_peso.png`), mas ela ficou para
trás: foi gerada por uma versão anterior do escore e diz categoria 38% e
produto 19%, enquanto o parquet atual diz 45,1% e 27,5%. Copiar a imagem velha
seria pôr na tela um número que o repositório não produz mais.

O peso de cada sinal sai da coluna `sinais` de `04_fila_pontuada.parquet`, que
o notebook 04 grava com a contribuição de cada característica para a nota
daquele incidente. As parcelas somam o escore que o modelo calculou.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_figuras_explica.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"
PARQUET = AQUI.parents[2] / "data" / "interim" / "04_fila_pontuada.parquet"

COR = {"pico": "#DC2626", "resto": "#2563EB", "texto": "#111827", "eixo": "#6B7280"}


def estilo() -> None:
    mpl.rcParams.update({
        "figure.dpi": 100, "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": "#9AA6B6", "axes.linewidth": .8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 16, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.titlepad": 18, "axes.labelsize": 12.5, "axes.labelcolor": "#4A5568",
        "axes.grid": True, "axes.axisbelow": True,
        "grid.color": "#E5E9F0", "grid.linewidth": .6,
        "xtick.color": "#8B96A8", "ytick.color": "#4A5568",
        "xtick.labelsize": 11.5, "ytick.labelsize": 12.5,
        "font.family": "sans-serif",
        "font.sans-serif": ["Sora", "Outfit", "Inter", "DejaVu Sans"],
        "font.size": 12, "legend.frameon": False,
    })
    plt.rcParams["axes.grid.axis"] = "x"


def main() -> int:
    from PIL import Image

    FIGS.mkdir(parents=True, exist_ok=True)
    estilo()
    d = pd.read_parquet(PARQUET).sort_values("posicao")
    r = d.iloc[0]
    sinais = json.loads(r["sinais"])
    # de baixo para cima, para o maior peso ficar no topo do eixo
    nomes = [s["sinal"] for s in sinais][::-1]
    pesos = [s["peso"] for s in sinais][::-1]

    fig, ax = plt.subplots(figsize=(10.4, 5.4))
    cores = [COR["resto"]] * len(pesos)
    cores[-1] = COR["pico"]                       # o maior, que está no topo
    barras = ax.barh(range(len(pesos)), pesos, color=cores, height=.62)
    ax.set_yticks(range(len(nomes)))
    ax.set_yticklabels(nomes)
    ax.set_xlabel("peso na explicação do risco (%)")
    ax.set_title(f"Por que {r['incidente']} está no topo da fila")
    ax.set_xlim(0, max(pesos) * 1.22)

    for b, v in zip(barras, pesos):
        ax.text(b.get_width() + max(pesos) * .022, b.get_y() + b.get_height() / 2,
                f"{v:.1f}%".replace(".", ","), va="center", ha="left",
                fontsize=12.5, fontweight="bold", color=COR["texto"])

    fig.tight_layout()
    destino = FIGS / "12_explica_peso.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    w, h = Image.open(destino).size
    print(f"  {destino.name:24s} {w}x{h}px")
    print(f"\n{r['incidente']} · {r['prioridade']} · {r['produto']} · "
          f"escore {r['risco']} · violou {bool(r['violou'])}")
    print(f"ativo {r['ativo']}: {int(r['ativo_passagens'])} passagens, "
          f"{int(r['ativo_violacoes'])} violações")
    for s in sinais:
        print(f"  {s['sinal']:34s} {s['peso']:5.1f}%")
    print(f"soma dos pesos: {sum(s['peso'] for s in sinais):.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
