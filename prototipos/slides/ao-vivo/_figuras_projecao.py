# -*- coding: utf-8 -*-
"""Gera a figura da projeção do KPI, em alta resolução.

O que o gráfico mostra: em cinco datas de corte de 2025, o que a projeção dizia
que o ano ia fechar, contra o que ele fechou de verdade.

    06_projecao.png    P2 e P3, projeção com banda contra o realizado

Leitura honesta, e ela está no gráfico:
  P2  a projeção caiu dentro da faixa da meta nas cinco datas
  P3  errou em três, e nas três para o lado PESSIMISTA: projetou acima do
      limite quando o ano fechou abaixo. Para um alarme de operação, é o lado
      certo de errar, porque nunca disse que estava tranquilo sem estar.

Números de data/interim/06_projecao.parquet.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_figuras_projecao.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"
PARQUET = AQUI.parents[2] / "data" / "interim" / "06_projecao.parquet"

COR = {
    "preto": "#000000",
    "cinza_escuro": "#444444",
    "cinza_medio": "#888888",
    "cinza_claro": "#E5E5E5",
    "accent": "#2563EB",
    "perigo": "#DC2626",
    "sucesso": "#16A34A",
}

MESES = {"2025-08-01": "ago", "2025-09-01": "set", "2025-10-01": "out",
         "2025-11-01": "nov", "2025-12-01": "dez"}


def estilo() -> None:
    mpl.rcParams.update({
        "figure.dpi": 100, "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": COR["cinza_escuro"], "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": 15, "axes.titleweight": "bold",
        "axes.titlelocation": "left", "axes.titlepad": 14,
        "axes.labelsize": 12, "axes.labelcolor": COR["cinza_escuro"],
        "axes.grid": True, "axes.axisbelow": True,
        "grid.color": COR["cinza_claro"], "grid.linewidth": 0.5,
        "xtick.color": COR["cinza_medio"], "ytick.color": COR["cinza_medio"],
        "xtick.labelsize": 12, "ytick.labelsize": 11.5,
        "font.family": "sans-serif",
        "font.sans-serif": ["Sora", "Outfit", "Inter", "DejaVu Sans"],
        "font.size": 11.5, "legend.frameon": False, "legend.fontsize": 12,
    })
    plt.rcParams["axes.grid.axis"] = "y"


def main() -> int:
    from PIL import Image

    FIGS.mkdir(parents=True, exist_ok=True)
    estilo()
    d = pd.read_parquet(PARQUET)
    d["corte"] = d["corte"].astype(str)

    fig, eixos = plt.subplots(1, 2, figsize=(13.2, 4.6))
    for ax, pri, real, faixa, titulo in [
        (eixos[0], "P2", 42, (40, 45), "Prioridade 2 · faixa da meta entre 40 e 45"),
        (eixos[1], "P3", 196, (0, 200), "Prioridade 3 · faixa da meta abaixo de 200"),
    ]:
        s = d[d["prioridade"] == pri].sort_values("corte")
        x = range(len(s))
        rot = [MESES[c] for c in s["corte"]]

        # a faixa da meta, que é o alvo que a projeção precisa acertar
        ax.axhspan(faixa[0], faixa[1], color=COR["sucesso"], alpha=0.09, zorder=0)
        ax.axhline(faixa[1], color=COR["sucesso"], lw=1.2, ls="--", zorder=1)

        # a banda da projeção em cada data de corte
        ax.fill_between(x, s["faixa baixa"], s["faixa alta"], color=COR["accent"],
                        alpha=0.16, zorder=2, label="Banda da projeção")
        ax.plot(x, s["projeção"], color=COR["accent"], lw=2.6, marker="o",
                markersize=7, zorder=4, label="Projeção do ano")
        ax.axhline(real, color=COR["preto"], lw=2, zorder=3,
                   label=f"Fechou em {real}")

        ax.set_title(titulo)
        ax.set_ylabel("quebras projetadas para o ano")
        ax.set_xlabel("data em que a projeção foi feita, 2025")
        ax.set_xticks(list(x))
        ax.set_xticklabels(rot)
        ax.set_xlim(-0.3, len(s) - 0.7)
        alto = max(s["faixa alta"].max(), faixa[1], real) * 1.1
        baixo = min(s["faixa baixa"].min(), faixa[0], real) * 0.86
        ax.set_ylim(baixo, alto)
        ax.legend(loc="upper left", bbox_to_anchor=(0, -0.24), ncol=3, fontsize=11)

    fig.tight_layout(w_pad=3.4)
    destino = FIGS / "06_projecao.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    w, h = Image.open(destino).size
    print(f"  {destino.name:22s} {w}x{h}px")

    print("\nconferência do que vai no slide:")
    for pri, real, limite in (("P2", 42, (40, 45)), ("P3", 196, (0, 200))):
        s = d[d["prioridade"] == pri]
        acertos = sum(1 for _, r in s.iterrows()
                      if limite[0] <= r["projeção"] <= limite[1])
        pess = sum(1 for _, r in s.iterrows() if r["projeção"] > real)
        print(f"  {pri}: {acertos} de {len(s)} dentro da faixa · "
              f"{pess} de {len(s)} projetaram acima do realizado")
        print(f"      erro % por corte: {[round(v, 1) for v in s['erro %']]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
