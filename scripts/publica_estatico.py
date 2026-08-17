# -*- coding: utf-8 -*-
"""Publica o CSS e os icones do prototipo para dentro da aplicacao Django.

Fonte unica de verdade: o estilo continua nascendo em scripts/direcoes e o Django recebe
uma copia concatenada. Assim protótipo e aplicacao nao divergem.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'direcoes'))
from estilo import CSS as CSS_BASE
from fundo import CSS_CAMPO, campo
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

# sprite de icones: um <symbol> por glifo, referenciado por <use> no template.
#
# Escrevia em `static/painel/icones.svg`, e NENHUM template referenciava esse arquivo: o
# sprite que a aplicacao inclui e `templates/painel/_sprite.svg`, que nenhum script gerava —
# tinha sido copiado a mao. Consequencia pratica: adicionar um glifo em `direcoes/icones.py` e
# rodar este publicador atualizava o arquivo que ninguem le, e o icone novo simplesmente nao
# aparecia, sem erro nenhum. Agora o gerador escreve no arquivo em uso.
SPRITE = RAIZ / 'webapp' / 'painel' / 'templates' / 'painel' / '_sprite.svg'
simbolos = ''.join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
    for k, v in G.items())
SPRITE.write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" style="display:none">{simbolos}</svg>',
    encoding='utf-8')
# a copia orfa em static/ so gera confusao sobre qual dos dois vale
(DEST / 'icones.svg').unlink(missing_ok=True)

# o campo de linhas do fundo. O template dizia "gerado por publica_estatico.py" desde sempre, mas
# nenhum script o escrevia: era orfao, e mexer nele significava editar SVG a mao. Agora e verdade.
CAMPO = RAIZ / 'webapp' / 'painel' / 'templates' / 'painel' / '_campo.html'
CAMPO.write_text(
    '{% comment %}\n'
    'Campo de linhas: cada curva e a serie diaria real de um produto em 2025, em tres\n'
    'camadas de profundidade. Viajar no tempo desloca as camadas em velocidades\n'
    'diferentes, e e esse paralaxe que produz a sensacao de movimento.\n'
    'Gerado por scripts/publica_estatico.py — nao editar a mao.\n'
    '{% endcomment %}\n'
    '<div hidden>{% include "painel/_sprite.svg" %}</div>\n'
    # 0.13 deixava as curvas no limite do perceptivel e o fundo lia como sujeira de compressao.
    # 0.2 ainda somia atras do vidro dos cartoes, que cobre a maior parte da pagina. 0.3, com o
    # traco em 1.8, e onde a linha existe sem competir com o dado.
    + campo('#2563EB', .3) + '\n',
    encoding='utf-8')

print(f'cronos.css  {(DEST / "cronos.css").stat().st_size / 1024:6.1f} kB')
print(f'_campo.html {CAMPO.stat().st_size / 1024:6.1f} kB')
print(f'_sprite.svg {SPRITE.stat().st_size / 1024:6.1f} kB  ({len(G)} glifos)')
