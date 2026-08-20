# -*- coding: utf-8 -*-
"""Monta o .zip da entrega: o .pptx da sprint e os sete notebooks executados.

Só esses dois itens, por decisão do Igor em 20/08/2026. A primeira versão levava também os
scripts, a aplicação Django e os dados tratados, o que dava 142 arquivos: peso e ruído para
quem só quer conferir a apresentação e a análise que a sustenta.

O portal da FIAP aceita **um** anexo por entrega e o enunciado da Sprint 3 nomeia o arquivo
fonte PowerPoint, então este .zip não é o anexo padrão dessa sprint. Ele serve ao arquivo do
grupo, ao mentor da Locaweb e à Sprint 4, que pede um .zip com o material do projeto.

Os notebooks vão com as saídas preservadas: é o que permite ler a análise sem executar nada,
e é a evidência de que o código rodou.

Uso:
    .venv/Scripts/python scripts/monta_zip_entrega.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PPTX = RAIZ / "sprints" / "EC_Sprint_3_2TSCOA_Evidencias_Construcao_Cronos_SuperDataBros.pptx"
DESTINO = PPTX.with_suffix(".zip")
NOTEBOOKS = RAIZ / "notebooks"


def coleta() -> list[tuple[Path, str]]:
    """Devolve (arquivo em disco, caminho dentro do zip)."""
    itens: list[tuple[Path, str]] = [(PPTX, PPTX.name)]
    cadernos = sorted(NOTEBOOKS.glob("0*.ipynb"))
    if len(cadernos) != 7:
        raise FileNotFoundError(f"esperados 7 notebooks, encontrados {len(cadernos)}")
    itens += [(f, f"notebooks/{f.name}") for f in cadernos]
    return itens


def main() -> None:
    if not PPTX.exists():
        raise FileNotFoundError(
            f"{PPTX.name} não existe. Rode antes: "
            ".venv/Scripts/python scripts/monta_deck_sprint3.py"
        )
    itens = coleta()
    with zipfile.ZipFile(DESTINO, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for arquivo, dentro in itens:
            z.write(arquivo, dentro)

    for _, dentro in itens:
        print(f"  {dentro}")
    print()
    print(f"{DESTINO.name}: {len(itens)} arquivos, "
          f"{DESTINO.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
