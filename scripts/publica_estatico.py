# -*- coding: utf-8 -*-
"""Publica o CSS e os icones do prototipo para dentro da aplicacao Django.

Fonte unica de verdade: o estilo continua nascendo em scripts/direcoes e o Django recebe
uma copia concatenada. Assim protótipo e aplicacao nao divergem.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'direcoes'))
from estilo import CSS as CSS_BASE
from fundo import CSS_CAMPO
from icones import G, CSS_ICO_CLARO

RAIZ = Path.cwd()
DEST = RAIZ / 'webapp' / 'painel' / 'static' / 'painel'
DEST.mkdir(parents=True, exist_ok=True)

# o CSS da aplicacao (abas, tabela, paleta, brief) mora em monta_app.py
texto = (RAIZ / 'scripts' / 'monta_app.py').read_text(encoding='utf-8')
ini = texto.index('CSS_APP = r"""') + len('CSS_APP = r"""')
CSS_APP = texto[ini:texto.index('"""', ini)]

folha = ('/* Cronos · folha unica. Gerada por scripts/publica_estatico.py.\n'
         '   Nao editar aqui: o estilo nasce em scripts/direcoes/. */\n'
         + CSS_BASE.split('r"""', 1)[-1].rsplit('"""', 1)[0]
         + CSS_ICO_CLARO + CSS_CAMPO + CSS_APP)
(DEST / 'cronos.css').write_text(folha, encoding='utf-8')

# sprite de icones: um <symbol> por glifo, referenciado por <use> no template
simbolos = ''.join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
    for k, v in G.items())
(DEST / 'icones.svg').write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" style="display:none">{simbolos}</svg>',
    encoding='utf-8')

print(f'cronos.css  {(DEST / "cronos.css").stat().st_size / 1024:6.1f} kB')
print(f'icones.svg  {(DEST / "icones.svg").stat().st_size / 1024:6.1f} kB  ({len(G)} glifos)')
