# -*- coding: utf-8 -*-
"""Extrai as placas de tecnologia do slide de stack da Sprint 2.

O HTML original (`prototipos/slides/tecnologias-slide.html`) puxa os logos de CDN, e o CDN
nao responde no ambiente de build. Mas o PPT entregue na Sprint 2 tem o slide rasterizado em
3200x1800, exatamente 2x do canvas, com os logos ja embutidos.

Entao a fonte de verdade das placas passa a ser esse PNG. As coordenadas abaixo sao os
centros das placas nele. Sete sao logo de marca, cinco sao placa de letra que a Sprint 2
desenhou a mao para bibliotecas sem logo oficial, e as doze vem no mesmo recorte.

Uso:
    .venv/Scripts/python scripts/extrai_placas_stack.py caminho/para/slide03_stack.png
"""
import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "brand" / "logos"

LADO = 130          # tamanho da placa no PNG de 3200x1800
FINAL = 260         # gravamos em 2x para o slide poder crescer sem serrar
COLUNA = {"esq": 181, "dir": 1701}
LINHAS = [419, 662, 906, 1149, 1394, 1637]
NOMES = [
    ("python", "pandas"),
    ("numpy", "holidays"),
    ("prophet", "xgboost"),
    ("tslearn", "shap"),
    ("django", "plotly"),
    ("claude", "docker"),
]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("uso: extrai_placas_stack.py <slide03_stack_tecnologias.png>")
    base = Image.open(sys.argv[1]).convert("RGB")
    if base.size != (3200, 1800):
        raise SystemExit(f"esperava 3200x1800, recebi {base.size[0]}x{base.size[1]}")

    SAIDA.mkdir(parents=True, exist_ok=True)
    for (esq, dir_), y in zip(NOMES, LINHAS):
        for nome, x in ((esq, COLUNA["esq"]), (dir_, COLUNA["dir"])):
            placa = base.crop((x - LADO // 2, y - LADO // 2, x + LADO // 2, y + LADO // 2))
            placa.resize((FINAL, FINAL), Image.LANCZOS).save(SAIDA / f"{nome}.png")
            print(f"  {nome}.png")


if __name__ == "__main__":
    main()
