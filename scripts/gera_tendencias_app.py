# -*- coding: utf-8 -*-
"""Gera data/app/tendencias.json, o pacote da aba Tendências.

Entradas: os dois parquets do notebook 08 (`08_tendencias_ranking` e `08_tendencias_mensal`).
A tela usa só o ranking (quantos valores existem, quantos violaram, o peso do topo) e a série
mensal para contar os valores de cada dimensão.
Nada é recalculado aqui: o script só recorta o topo de cada dimensão e empacota o que a tela lê,
no mesmo espírito do gera_dados_app.py (o contêiner abre um JSON pequeno e não carrega pandas).

O pacote mantém a janela do notebook (01/01 a 30/09/2025), o relógio da aplicação.

Uso:
    .venv/Scripts/python.exe scripts/gera_tendencias_app.py
"""
import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
INTERIM = RAIZ / "data" / "interim"
DESTINO = RAIZ / "data" / "app" / "tendencias.json"

TOPO = 10
# (chave na URL e no JSON, nome como o notebook grava, rótulo da tela)
DIMENSOES = [
    ("produto", "produto", "Produto"),
    ("categoria", "categoria", "Categoria"),
    ("ic", "item de configuração", "Item de configuração"),
]


def main() -> int:
    ranking = pd.read_parquet(INTERIM / "08_tendencias_ranking.parquet")
    mensal = pd.read_parquet(INTERIM / "08_tendencias_mensal.parquet")
    janela = ranking.attrs.get("janela", "2025-01-01 a 2025-09-30")

    por_pri = mensal[mensal["dimensao"] == "produto"].groupby("pri")["violacoes"].sum()
    pacote = {"janela": janela, "topo": TOPO,
              "violacoes_p2": int(por_pri["P2"]), "violacoes_p3": int(por_pri["P3"]),
              "dimensoes": {}}
    for chave, nome, rotulo in DIMENSOES:
        r = ranking[ranking["dimensao"] == nome].sort_values("posicao")
        m = mensal[mensal["dimensao"] == nome]
        total = int(r["violacoes"].sum())
        acumulado = r["violacoes"].cumsum() / total
        topo = r.head(TOPO)

        itens = []
        for _, x in topo.iterrows():
            itens.append({
                "valor": x["valor"],
                "posicao": int(x["posicao"]),
                "incidentes": int(x["incidentes"]),
                "violacoes": int(x["violacoes"]),
                "p2": {"incidentes": int(x["incidentes_p2"]), "violacoes": int(x["violacoes_p2"])},
                "p3": {"incidentes": int(x["incidentes_p3"]), "violacoes": int(x["violacoes_p3"])},
            })

        pacote["dimensoes"][chave] = {
            "rotulo": rotulo,
            # a série mensal guarda todos os valores da dimensão, e o ranking só os que violaram ou
            # passam do piso de volume
            "valores": int(m["valor"].nunique()),
            "total_violacoes": total,
            "com_violacao": int((r["violacoes"] > 0).sum()),
            "topo_pct": round(100 * float(acumulado.iloc[min(TOPO, len(acumulado)) - 1]), 1),
            "itens": itens,
        }
        print(f"{chave:10s} {len(r):5d} valores | topo {TOPO} = {pacote['dimensoes'][chave]['topo_pct']}%")

    DESTINO.write_text(json.dumps(pacote, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"tendencias.json  {DESTINO.stat().st_size / 1024:.1f} kB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
