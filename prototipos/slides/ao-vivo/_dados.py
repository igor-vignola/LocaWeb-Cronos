# -*- coding: utf-8 -*-
"""Gera os dados dos gráficos nativos do deck da banca.

Os gráficos deste deck são SVG escrito à mão, não PNG do matplotlib. O motivo é
prático: PNG de 1.100px exibido em tela cheia no Teams fica mole, e não anima.
SVG fica nítido em qualquer resolução e a linha pode se desenhar.

Este script mede as séries no parquet e imprime as coordenadas já prontas para
colar no SVG, junto do número que vai no rótulo. Rodar de novo confirma que o
que está no slide é o que está no dado.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_dados.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
PARQUET = RAIZ / "data" / "interim" / "incidentes_kpi.parquet"
CURVAS = RAIZ / "data" / "app" / "fila_curvas.json"

# medido uma vez do xlsx bruto, que tem 122.543 linhas e leva minutos para abrir
MENSAL_2025 = {
    "01": (3714, 2357), "02": (3553, 2282), "03": (3588, 2130), "04": (3202, 2072),
    "05": (3329, 2247), "06": (3558, 2105), "07": (3448, 2126), "08": (3996, 2330),
    "09": (21561, 2324), "10": (23017, 2126), "11": (21524, 1634), "12": (27321, 1423),
}
TOTAL_ANO = {2023: 110, 2024: 622}


def caminho(vals: list[float], larg: float, alt: float, topo: float) -> str:
    """Vira uma série num atributo d de path, com o eixo y invertido."""
    if len(vals) < 2:
        return ""
    passo = larg / (len(vals) - 1)
    pts = [f"{i * passo:.1f} {alt - (v / topo) * alt:.1f}" for i, v in enumerate(vals)]
    return "M " + " L ".join(pts)


def ritmo_da_semana(df: pd.DataFrame) -> dict:
    """Média por dia da semana, com intervalo de confiança de 95%."""
    d = df[df["ano"] == 2025].copy()
    d["data"] = pd.to_datetime(d["Aberto"]).dt.date
    saida = {}
    for rotulo, pri in [("p2", "2 - Alta"), ("p3", "3 - Média")]:
        porDia = d[d["Prioridade"] == pri].groupby("data").size()
        idx = pd.to_datetime(porDia.index)
        tab = pd.DataFrame({"n": porDia.values, "dow": idx.dayofweek})
        linhas = []
        for dow in range(7):
            g = tab[tab.dow == dow]["n"]
            ic = 1.96 * g.std() / np.sqrt(len(g))
            linhas.append({"dia": "seg ter qua qui sex sáb dom".split()[dow],
                           "media": round(g.mean(), 1), "ic": round(ic, 1),
                           "dias": int(len(g))})
        saida[rotulo] = linhas
    return saida


def main() -> int:
    df = pd.read_parquet(PARQUET)
    out: dict = {}

    # ── slide 3 · o salto de setembro ──
    total = [MENSAL_2025[f"{m:02d}"][0] for m in range(1, 13)]
    eleg = [MENSAL_2025[f"{m:02d}"][1] for m in range(1, 13)]
    out["salto"] = {
        "total": total, "elegivel": eleg, "topo": 28000,
        "path_total": caminho(total, 1000, 300, 28000),
        "path_elegivel": caminho(eleg, 1000, 300, 28000),
        "ago_set_total": f"{total[7]:,} para {total[8]:,}".replace(",", "."),
        "ago_set_eleg": f"{eleg[7]:,} para {eleg[8]:,}".replace(",", "."),
        "fator": round(total[8] / total[7], 1),
        "anos_vazios": TOTAL_ANO,
    }

    # ── slide 4 · o ritmo da semana ──
    out["semana"] = ritmo_da_semana(df)

    # ── slide 7 · o ganho da fila ──
    c = json.loads(CURVAS.read_text(encoding="utf-8"))
    n_pontos = 60  # os 60 primeiros dos 200, que é onde o ganho aparece
    for chave in ("risco", "prioridade", "acaso", "teto"):
        serie = c[chave][:n_pontos]
        out.setdefault("fila", {})[f"path_{chave}"] = caminho(serie, 1000, 300, 50)
    out["fila"]["n"] = c["n"]
    out["fila"]["v"] = c["v"]
    out["fila"]["x_final"] = c["x"][n_pontos - 1]
    out["fila"]["nos_50"] = {k: c[k][min(range(len(c["x"])), key=lambda i: abs(c["x"][i] - 50))]
                             for k in ("risco", "prioridade", "acaso")}

    destino = Path(__file__).parent / "_dados.json"
    destino.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print("── slide 3 · o salto de setembro")
    print(f"   total ago->set: {out['salto']['ago_set_total']}  ({out['salto']['fator']}x)")
    print(f"   elegível ago->set: {out['salto']['ago_set_eleg']}")
    print(f"   2023 inteiro: {TOTAL_ANO[2023]} incidentes · 2024: {TOTAL_ANO[2024]}")
    print("\n── slide 4 · o ritmo da semana")
    for r in out["semana"]["p3"]:
        print(f"   P3 {r['dia']}: {r['media']:5.1f} ± {r['ic']:.1f}  ({r['dias']} dias)")
    print("\n── slide 7 · o ganho da fila")
    print(f"   base {out['fila']['n']:,} incidentes, {out['fila']['v']} perdas")
    print(f"   nos 50 primeiros: {out['fila']['nos_50']}")
    print(f"\ngravado em {destino.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
