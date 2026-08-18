# -*- coding: utf-8 -*-
"""Reenquadra as fotos da equipe e aplica máscara circular com alpha real.

As originais vêm com o círculo desenhado sobre fundo escuro e alpha 100% opaco. Num slide
claro isso apareceria como um quadrado de cantos sujos, então aqui o círculo passa a ser
alpha de verdade.

As três chegaram com enquadramento desigual: uma de rosto, uma de meio corpo e uma selfie
de espelho. A janela de cada pessoa foi escolhida para as três terem a mesma escala de
rosto, que é o que faz a fileira de avatares parecer intencional.

`janela` é (centro_x, centro_y, lado) em pixel da original. O círculo de saída é inscrito
na janela, e a validação garante que ele cabe dentro do círculo da original: sem isso,
entraria canto escuro no recorte.

Uso:
    .venv/Scripts/python scripts/corta_fotos_equipe.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

SAIDA = 512   # lado do arquivo final, em px
SUAVE = 4     # supersampling da máscara, para a borda não serrar

# origem, destino, janela (cx, cy, lado), círculo da original (cx, cy, raio)
PESSOAS = [
    ("ana_beatriz_costa.png", "ana-beatriz.png", (393, 400, 690), (442, 426, 424)),
    ("hygor_abrantes.png",    "hygor.png",       (526, 296, 422), (510, 430, 424)),
    ("igor_vignola.png",      "igor.png",        (225, 180, 240), (243, 237, 221)),
]


def corta(origem: Path, destino: Path, janela, circulo) -> None:
    cx, cy, lado = janela
    ox, oy, r = circulo
    dist = ((cx - ox) ** 2 + (cy - oy) ** 2) ** 0.5
    folga = r - (dist + lado / 2)
    if folga < 0:
        raise ValueError(
            f"{origem.name}: o círculo de saída estoura o da original em {-folga:.0f}px"
        )

    im = Image.open(origem).convert("RGB")
    caixa = (int(cx - lado / 2), int(cy - lado / 2), int(cx + lado / 2), int(cy + lado / 2))
    im = im.crop(caixa).resize((SAIDA, SAIDA), Image.LANCZOS)

    grande = Image.new("L", (SAIDA * SUAVE, SAIDA * SUAVE), 0)
    ImageDraw.Draw(grande).ellipse((0, 0, SAIDA * SUAVE - 1, SAIDA * SUAVE - 1), fill=255)
    im.putalpha(grande.resize((SAIDA, SAIDA), Image.LANCZOS))
    im.save(destino)
    print(f"  {destino.name:18s} janela de {lado}px, folga de {folga:.0f}px para a borda")


def main() -> None:
    base = Path(__file__).resolve().parents[1] / "brand" / "equipe" / "originais"
    for orig, novo, janela, circulo in PESSOAS:
        corta(base / orig, base.parent / novo, janela, circulo)


if __name__ == "__main__":
    main()
