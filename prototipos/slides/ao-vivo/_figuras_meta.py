# -*- coding: utf-8 -*-
"""Gera o gráfico da projeção da meta anual, nas cinco datas de corte de 2025.

Responde ao pedido que o mentor da Locaweb fez na mentoria: parado no meio do
ano, dá para saber se a meta anual vai fechar? O gráfico mostra, para cada data
de corte, a faixa que a projeção dava naquele dia, a própria projeção, a faixa
da meta e o número em que o ano de fato fechou.

A leitura honesta está desenhada, não escondida:

    P2   a projeção apontou dentro da meta nas cinco datas, e o ano fechou em 42
    P3   apontou estouro em agosto, setembro e outubro, e o ano fechou em 196 —
         errou para o lado pessimista nas três

E a faixa aperta conforme o ano anda: no P2 ela vai de 17 pontos de largura em
agosto para 3 em dezembro; no P3, de 63 para 10. Quanto mais cedo se pergunta,
mais larga é a resposta.

Tudo sai de data/interim/06_projecao.parquet.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_figuras_meta.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"
PARQUET = AQUI.parents[2] / "data" / "interim" / "06_projecao.parquet"

MES = {8: "1º ago", 9: "1º set", 10: "1º out", 11: "1º nov", 12: "1º dez"}

COR = {
    "modelo": "#2563EB",
    "meta": "#16A34A",
    "fora": "#DC2626",
    "real": "#000000",
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


def painel(ax, s: pd.DataFrame, titulo: str, limites: tuple[float, float]) -> None:
    x = np.arange(len(s))
    baixa, alta = s["faixa baixa"], s["faixa alta"]
    real = float(s["real"].iloc[0])
    meta_min = float(s["meta mínima"].iloc[0])
    meta_max = float(s["meta máxima"].iloc[0])

    # três camadas só, para a leitura ser imediata: a zona da meta, a projeção
    # em cada data e a linha de onde o ano fechou. A faixa de incerteza da
    # projeção saiu do gráfico — deixava o slide carregado — e fica para perguntas.
    ax.axhspan(meta_min, meta_max, color=COR["meta"], alpha=0.12, linewidth=0,
               zorder=1, label="Dentro da meta")
    ax.axhline(meta_max, color=COR["meta"], linewidth=1.4, linestyle=(0, (5, 3)),
               zorder=2)
    ax.plot(x, s["projeção"], color=COR["modelo"], linewidth=2.4, marker="o",
            markersize=9, zorder=5, label="O que a projeção dizia naquela data")
    ax.axhline(real, color=COR["real"], linewidth=1.8, zorder=4,
               label="Onde o ano fechou")

    ax.set_title(titulo)
    ax.set_ylim(*limites)
    ax.set_xlim(-0.3, len(s) - 0.7)
    ax.set_xticks(x)
    ax.set_xticklabels([MES[d.month] for d in s["corte"]])
    ax.set_ylabel("violações no ano")

    # o número em que o ano fechou, escrito na própria linha
    ax.annotate(f"{real:.0f}", xy=(len(s) - 0.75, real), xytext=(0, 7),
                textcoords="offset points", fontsize=13, fontweight="bold",
                color=COR["real"], ha="right")


def main() -> int:
    from PIL import Image

    FIGS.mkdir(parents=True, exist_ok=True)
    estilo()
    d = pd.read_parquet(PARQUET)
    d["corte"] = pd.to_datetime(d["corte"])

    fig, eixos = plt.subplots(1, 2, figsize=(13.0, 4.6))
    for ax, (pri, limites, titulo) in zip(eixos, (
            ("P2", (36, 48), "Prioridade 2 · meta de 40 a 45"),
            ("P3", (176, 232), "Prioridade 3 · limite de 200"))):
        painel(ax, d[d.prioridade == pri].sort_values("corte")
                .reset_index(drop=True), titulo, limites)

    alcas, rotulos = eixos[0].get_legend_handles_labels()
    fig.legend(alcas, rotulos, loc="lower center", ncol=3,
               bbox_to_anchor=(0.5, -0.055), columnspacing=2.2)
    fig.subplots_adjust(wspace=0.2)

    destino = FIGS / "09_meta_anual.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    w, h = Image.open(destino).size
    print(f"  {destino.name:24s} {w}x{h}px")

    print("\nchamada da projeção contra o que aconteceu:")
    for pri in ("P2", "P3"):
        s = d[d.prioridade == pri].sort_values("corte")
        real = float(s["real"].iloc[0])
        dentro_real = (s["meta mínima"] <= real) & (real <= s["meta máxima"])
        acertou = (s["situação projetada"] == "dentro da meta") == dentro_real
        largura = s["faixa alta"] - s["faixa baixa"]
        print(f"  {pri}: fechou em {real:.0f}; "
              f"{int(acertou.sum())} de {len(s)} datas com a chamada certa; "
              f"faixa de {largura.iloc[0]:.0f} pontos em agosto "
              f"para {largura.iloc[-1]:.0f} em dezembro")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
