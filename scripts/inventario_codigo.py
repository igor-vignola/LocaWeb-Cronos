# -*- coding: utf-8 -*-
"""Inventário do código-fonte do projeto, para o slide de evidências de construção.

O slide afirma quantos notebooks, células e linhas existem. A regra do projeto é que
número em slide precisa sair de código executado, e o `verifica_numeros.py` só conhece o
universo dos notebooks. Estes números falam do repositório, não da base, então a origem
deles é este arquivo.

Conta o que é código de verdade: célula de código de notebook (markdown fora), `.py` de
`scripts/` e `webapp/` (cache fora), template do Django e tabela intermediária gravada.

Uso:
    .venv/Scripts/python scripts/inventario_codigo.py
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def pt(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def notebooks() -> tuple[int, int, int]:
    arquivos = sorted((RAIZ / "notebooks").glob("0*.ipynb"))
    celulas = linhas = 0
    for f in arquivos:
        nb = json.loads(f.read_text(encoding="utf-8"))
        codigo = [c for c in nb["cells"] if c["cell_type"] == "code"]
        celulas += len(codigo)
        linhas += sum(len(c["source"]) for c in codigo)
    return len(arquivos), celulas, linhas


def python(pasta: str) -> tuple[int, int]:
    """Conta os `.py` de uma pasta. `webapp` e `scripts` saem separados de proposito: o
    primeiro e a aplicacao entregue, o segundo e ferramenta de deck e de dados, e somar os
    dois em um numero unico faria a aplicacao parecer maior do que e."""
    arquivos = [p for p in (RAIZ / pasta).rglob("*.py") if "__pycache__" not in p.parts]
    linhas = sum(len(p.read_text(encoding="utf-8", errors="replace").splitlines())
                 for p in arquivos)
    return len(arquivos), linhas


def main() -> None:
    n_nb, n_cel, n_lin = notebooks()
    n_app, n_lin_app = python("webapp")
    n_scr, n_lin_scr = python("scripts")
    n_tpl = len(list((RAIZ / "webapp").rglob("*.html")))
    n_parquet = len(list((RAIZ / "data" / "interim").glob("*.parquet")))

    print(f"notebooks:                {n_nb}")
    print(f"celulas de codigo:        {pt(n_cel)}")
    print(f"linhas em notebook:       {pt(n_lin)}")
    print(f"webapp: modulos .py       {n_app}  ({pt(n_lin_app)} linhas)")
    print(f"webapp: templates         {n_tpl}")
    print(f"scripts: modulos .py      {n_scr}  ({pt(n_lin_scr)} linhas)")
    print(f"tabelas em parquet:       {n_parquet}")
    print(f"linhas de codigo do produto (notebooks + webapp): "
          f"{pt(n_lin + n_lin_app)}")


if __name__ == "__main__":
    main()
