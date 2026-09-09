# -*- coding: utf-8 -*-
"""Gera as tiras de quadrados da fila de risco, uma por ordenação.

Cada quadrado é uma posição na fila. Vermelho quer dizer que aquele incidente
passou do prazo. Percorrendo as 50 primeiras posições de cada ordenação, dá para
ver de longe quantas quebras cada critério encontra — e é isso que o slide 8
precisa mostrar sem tabela nenhuma.

As quatro ordenações, todas recomputadas de data/interim/04_fila_pontuada.parquet:

    modelo       pela pontuação da regressão logística
    time         pela taxa histórica de quebra do time
    ativo        pelo número de quebras que o ativo já teve
    prioridade   P2 antes de P3, que é o que a operação faz hoje

O acaso não vira tira: nas 50 primeiras ele encontra meia quebra, e meia quebra
não se desenha. Ele entra como número no pé do slide.

Uso:
    .venv/Scripts/python.exe prototipos/slides/ao-vivo/_fila_quadros.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

AQUI = Path(__file__).parent
PARQUET = AQUI.parents[2] / "data" / "interim" / "04_fila_pontuada.parquet"

POSICOES = 50  # quantas posições da fila entram na tira

ORDENACOES = (
    ("modelo", "Fila do modelo de risco", ["risco"], [False]),
    ("time", "Regra: time com mais quebra", ["taxa_time"], [False]),
    ("ativo", "Regra: ativo mais crônico", ["ativo_violacoes"], [False]),
    ("prioridade", "Regra: prioridade 2 primeiro", ["ordem_pri"], [False]),
)


def main() -> int:
    d = pd.read_parquet(PARQUET).copy()
    d["violou"] = d["violou"].astype(bool)
    total = int(d["violou"].sum())
    d["taxa_time"] = d["equipe"].map(d.groupby("equipe")["violou"].mean())
    d["ordem_pri"] = (d["prioridade"] == "P2").astype(int)

    atraso = 700
    for chave, rotulo, por, asc in ORDENACOES:
        # desempate estável pela ordem original, para a tira ser reprodutível
        s = d.sort_values(por + ["incidente"], ascending=asc + [True])
        marcas = s["violou"].to_numpy()[:POSICOES]
        achadas = int(marcas.sum())

        print(f'      <div class="tira {chave}">')
        print(f'        <div class="cab">'
              f'<span class="rt rv" style="--d:{atraso}ms">{rotulo}</span>'
              f'<span class="ct2 rv" style="--d:{atraso + 60}ms">'
              f'<b><span class="ct" data-to="{achadas}" '
              f'data-delay="{atraso + 900}">0</span></b> quebras encontradas'
              f'</span></div>')
        print('        <div class="qd">')
        linha = []
        for i, quebrou in enumerate(marcas):
            # o quadrado entra, e o vermelho vira depois: a sala vê a diferença
            entra = atraso + 160 + i * 11
            vira = atraso + 900 + i * 9
            classe = ' class="q"' if quebrou else ""
            estilo = f"--d:{entra}ms" + (f";--dq:{vira}ms" if quebrou else "")
            linha.append(f'<i{classe} style="{estilo}"></i>')
        print("          " + "".join(linha))
        print("        </div>")
        print("      </div>")
        atraso += 480

    print(f"\n<!-- base: {len(d):,} incidentes, {total} quebras -->"
          .replace(",", "."))
    print(f"<!-- pelo acaso, nas {POSICOES} primeiras: "
          f"{POSICOES * total / len(d):.1f} quebras -->")
    for chave, rotulo, por, asc in ORDENACOES:
        s = d.sort_values(por + ["incidente"], ascending=asc + [True])
        seguidas = 0
        for v in s["violou"].to_numpy():
            if not v:
                break
            seguidas += 1
        print(f"<!-- {rotulo}: {int(s['violou'].to_numpy()[:POSICOES].sum())} "
              f"nas {POSICOES} primeiras, {seguidas} seguidas desde a posição 1 -->")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
