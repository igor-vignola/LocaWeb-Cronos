# -*- coding: utf-8 -*-
"""Gera as figuras dos slides de modelo, em alta resolução.

Mesma regra do _figuras.py: matplotlib em dpi 200, padrão da skill viz-style,
cinza como default e azul só onde a cor comunica algo.

    03_semana.png    média por dia da semana com intervalo de 95%, P2 e P3
    04_quartis.png   taxa de perda por quartil de volume diário
    05_fila.png      quebras encontradas conforme a fila de risco avança

Todas as séries vêm de _dados.json, que _dados.py mede no parquet.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_figuras_modelos.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

AQUI = Path(__file__).parent
FIGS = AQUI / "figs"
DADOS = AQUI / "_dados.json"
CURVAS = AQUI.parents[2] / "data" / "app" / "fila_curvas.json"

COR = {
    "preto": "#000000",
    "cinza_escuro": "#444444",
    "cinza_medio": "#888888",
    "cinza_claro": "#E5E5E5",
    "accent": "#2563EB",
    "perigo": "#DC2626",
    "atencao": "#D97706",
}

# quartis de volume dos 261 dias úteis de 2025, medidos em _dados.py
QUARTIS = [
    ("Q1\nmenor volume", 55.5, 0.86),
    ("Q2", 79.0, 0.87),
    ("Q3", 89.6, 0.97),
    ("Q4\nmaior volume", 110.0, 0.72),
]


def estilo() -> None:
    mpl.rcParams.update({
        "figure.dpi": 100,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": COR["cinza_escuro"],
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 15,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 14,
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


def ritmo_da_semana(dados: dict) -> Path:
    """Os cinco dias úteis num patamar só, e o fim de semana em outro.

    O intervalo de 95% é o ponto do gráfico: ele se sobrepõe entre os dias
    úteis, e é por isso que o modelo trata dia útil como um nível único em vez
    de aprender sete perfis.
    """
    fig, eixos = plt.subplots(1, 2, figsize=(12.4, 4.5))
    for ax, chave, titulo in zip(eixos, ("p3", "p2"),
                                 ("Prioridade 3", "Prioridade 2")):
        linhas = dados["semana"][chave]
        dias = [r["dia"] for r in linhas]
        media = [r["media"] for r in linhas]
        ic = [r["ic"] for r in linhas]
        cores = [COR["cinza_escuro"]] * 5 + [COR["cinza_medio"]] * 2
        ax.bar(dias, media, yerr=ic, capsize=5, color=cores, width=0.62,
               error_kw=dict(ecolor=COR["preto"], lw=1.3, capthick=1.3))
        ax.set_title(f"{titulo} · média por dia da semana")
        ax.set_ylabel("incidentes por dia")
        ax.set_ylim(0, max(media) * 1.26)

    fig.tight_layout(w_pad=3.2)
    destino = FIGS / "03_semana.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return destino


def taxa_por_quartil() -> Path:
    """O volume dobra do primeiro para o quarto quartil e a taxa não sobe."""
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    rotulos = [q[0] for q in QUARTIS]
    taxas = [q[2] for q in QUARTIS]
    volumes = [q[1] for q in QUARTIS]
    # azul só no quartil mais cheio, que é o que tem a MENOR taxa
    cores = [COR["cinza_claro"]] * 3 + [COR["accent"]]

    barras = ax.bar(rotulos, taxas, color=cores, width=0.6,
                    edgecolor="white", linewidth=1.2)
    for b, tx in zip(barras, taxas):
        ax.text(b.get_x() + b.get_width() / 2, tx + 0.035,
                f"{tx:.2f}%".replace(".", ","), ha="center", va="bottom",
                fontsize=14, fontweight="bold", color=COR["preto"])
    # o volume vai para o rótulo do eixo, e não para dentro da barra: sobre a
    # barra azul do Q4 o texto escuro ficava com contraste ruim
    ax.set_xticks(range(len(QUARTIS)))
    ax.set_xticklabels([q[0] + "\n" + f"{q[1]:.0f}".replace(".", ",") + " por dia"
                        for q in QUARTIS])

    ax.set_title("Taxa de perda de prazo por quartil de volume diário")
    ax.set_ylabel("taxa de perda de prazo")
    ax.set_ylim(0, max(taxas) * 1.32)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0", "0,25%", "0,50%", "0,75%", "1,00%"])
    ax.tick_params(axis="x", labelsize=12)

    destino = FIGS / "04_quartis.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return destino


def ganho_da_fila() -> Path:
    """Quantas quebras a fila encontra conforme ela avança.

    O eixo x para em 200 incidentes de propósito: é ali que o ganho aparece, e
    esticar até os 5.183 da base achataria a curva do modelo contra o acaso.
    """
    c = json.loads(CURVAS.read_text(encoding="utf-8"))
    corte = next(i for i, x in enumerate(c["x"]) if x > 200)
    x = c["x"][:corte]

    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    ax.plot(x, c["risco"][:corte], color=COR["accent"], linewidth=3,
            label="Fila do modelo de risco")
    ax.plot(x, c["prioridade"][:corte], color=COR["cinza_escuro"], linewidth=2,
            linestyle="--", label="Ordenada por prioridade")
    ax.plot(x, c["acaso"][:corte], color=COR["cinza_medio"], linewidth=1.6,
            linestyle=":", label="Acaso")

    ax.set_title("Quebras encontradas conforme a fila de risco avança")
    ax.set_xlabel("incidentes percorridos na fila")
    ax.set_ylabel("quebras encontradas")
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 22)
    # inteiros: quebra encontrada é contagem, e 17.5 com ponto não é pt-BR
    ax.set_yticks([0, 5, 10, 15, 20])
    ax.set_xticks([0, 25, 50, 75, 100, 125, 150, 175, 200])

    # os nove primeiros da fila eram todos quebra: é o fato que se explica sem jargão
    ax.annotate(
        "os 9 primeiros da fila\neram todos quebra",
        xy=(9, 9), xytext=(38, 4.2),
        color=COR["accent"], fontsize=12.5, fontweight="bold",
        ha="left", va="center",
        arrowprops=dict(arrowstyle="->", color=COR["accent"], linewidth=1.4,
                        shrinkA=4, shrinkB=5, connectionstyle="arc3,rad=0.2"),
    )
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.16), ncol=3)

    destino = FIGS / "05_fila.png"
    fig.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return destino


def main() -> int:
    from PIL import Image

    FIGS.mkdir(parents=True, exist_ok=True)
    estilo()
    dados = json.loads(DADOS.read_text(encoding="utf-8"))

    for fn, arg in ((ritmo_da_semana, dados), (taxa_por_quartil, None),
                    (ganho_da_fila, None)):
        p = fn(arg) if arg is not None else fn()
        w, h = Image.open(p).size
        print(f"  {p.name:22s} {w}x{h}px")

    print("\nconferência dos números que vão nas figuras:")
    p3 = dados["semana"]["p3"]
    print(f"  P3 seg a sex: {[r['media'] for r in p3[:5]]}")
    print(f"  P3 sáb e dom: {[r['media'] for r in p3[5:]]}")
    print(f"  quartis: taxa {[q[2] for q in QUARTIS]}  volume {[q[1] for q in QUARTIS]}")
    c = json.loads(CURVAS.read_text(encoding="utf-8"))
    nove = sum(1 for m in c["marcas"] if m < 9)
    print(f"  primeiras 9 posições da fila: {nove} são quebra de {c['v']} no total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
