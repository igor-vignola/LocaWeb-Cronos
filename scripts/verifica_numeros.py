# -*- coding: utf-8 -*-
"""Verifica se todo numero afirmado em texto tem lastro na saida de alguma celula.

Regra do projeto: numero em markdown de notebook, em doc ou em slide precisa ser produzido
por codigo. Este script extrai os numeros das duas fontes e reporta os que nao casam.

Uso:  python verifica_numeros.py [--tudo]
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path.cwd()
NOTEBOOKS = sorted(RAIZ.glob('notebooks/0*.ipynb'))
DOCS = [RAIZ / 'docs' / 'sprint-3-mvp.md', RAIZ / 'CLAUDE.md',
        RAIZ / 'context' / 'decisoes-tecnicas.md', RAIZ / 'context' / 'status.md']
SLIDES = sorted((RAIZ / 'prototipos' / 'slides' / 'mvp' / 'deck').glob('d*.html'))

# numeros que nao vale checar: pequenos inteiros, anos, versoes, numeros de secao
IGNORAR_EXATOS = {2023, 2024, 2025, 2026, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 100}
PADRAO_NUM = re.compile(r'\d[\d.,]*\d|\d')


def normaliza(bruto):
    """Converte texto numerico PT-BR ou EN para float. Devolve None se nao for numero."""
    s = bruto.strip().rstrip('.,')
    if not s or not s[0].isdigit():
        return None
    if ',' in s:                                    # virgula = decimal PT-BR
        s = s.replace('.', '').replace(',', '.')
    else:
        partes = s.split('.')
        if len(partes) > 1 and all(len(p) == 3 for p in partes[1:]):
            s = ''.join(partes)                     # 25.600 -> 25600
    try:
        return float(s)
    except ValueError:
        return None


# ruido que nao e afirmacao sobre o dado
RUIDO = [
    re.compile(r'Python\s+3\.\d+'),          # versao de dependencia
    re.compile(r'\d{2}/\d{2}/\d{4}'),        # datas
    re.compile(r'RM\d+'),                    # matricula
    re.compile(r'\|\s*\d\.\d+\s*\|'),        # numero de secao em tabela de sumario
    re.compile(r'se[çc][õo]es?\s+\d\.\d+'),  # referencia a secao no texto
    re.compile(r'ver\s+\d\.\d+'),
    re.compile(r'^#{1,6}\s*\d[\d.]*', re.M), # titulo numerado
]

def limpa_ruido(texto):
    for r in RUIDO:
        texto = r.sub(' ', texto)
    return texto


def extrai(texto):
    """Todos os numeros de um texto, normalizados."""
    saida = set()
    for m in PADRAO_NUM.finditer(texto):
        v = normaliza(m.group(0))
        if v is not None:
            saida.add(round(v, 4))
    return saida


def casa(alvo, universo, tol_rel=0.006):
    """Um numero tem lastro se aparece igual, ou dentro da tolerancia de arredondamento,
    ou como o mesmo valor em outra escala (0,97 e 97 / 4,6 e 460)."""
    for v in universo:
        if abs(alvo - v) < 1e-9:
            return True
        if v != 0 and abs(alvo - v) / abs(v) <= tol_rel:
            return True
        for fator in (100.0, 0.01, 3600.0, 1 / 3600.0):
            alvo2 = alvo * fator
            if v != 0 and abs(alvo2 - v) / abs(v) <= tol_rel:
                return True
    return False


def universo_global(caminhos):
    """Todos os numeros produzidos por qualquer notebook do conjunto."""
    tudo = set()
    for c in caminhos:
        nb = json.loads(c.read_text(encoding='utf-8'))
        for cel in nb['cells']:
            if cel['cell_type'] != 'code':
                continue
            for o in cel.get('outputs', []):
                tudo |= extrai(''.join(o.get('text', [])))
            tudo |= extrai(''.join(cel['source']))
    return tudo


def verifica_notebook(caminho, mostrar_todos=False, global_=None):
    nb = json.loads(caminho.read_text(encoding='utf-8'))
    saidas, markdown = set(), []
    for c in nb['cells']:
        if c['cell_type'] == 'code':
            for o in c.get('outputs', []):
                texto = ''.join(o.get('text', []))
                if not texto:
                    dados = o.get('data', {})
                    texto = ''.join(dados.get('text/plain', '')) if dados else ''
                saidas |= extrai(texto)
            saidas |= extrai(''.join(c['source']))      # constantes do proprio codigo contam
        else:
            markdown.append(''.join(c['source']))

    sem_lastro = []
    for i, t in enumerate(markdown):
        corpo = limpa_ruido(t)
        corpo = re.sub(r'`[^`]*`', ' ', corpo)              # ignora trecho de codigo inline
        corpo = re.sub(r'\[[^\]]*\]\([^)]*\)', ' ', corpo)   # ignora links
        for m in PADRAO_NUM.finditer(corpo):
            v = normaliza(m.group(0))
            if v is None or v in IGNORAR_EXATOS or v != v:
                continue
            if casa(v, saidas):
                continue
            # segunda chance: o numero pode ser produzido por outro notebook do conjunto
            if global_ is not None and casa(v, global_):
                continue
            ini = max(0, m.start() - 48)
            trecho = ' '.join(corpo[ini:m.end() + 34].split())
            sem_lastro.append((m.group(0), trecho))
    return len(saidas), sum(len(t) for t in markdown), sem_lastro


def verifica_texto_externo(caminho, universo_global):
    """Docs e slides: confere contra o universo de numeros de todos os notebooks."""
    if not caminho.exists():
        return []
    bruto = caminho.read_text(encoding='utf-8', errors='ignore')
    if caminho.suffix == '.html':
        bruto = re.sub(r'<style[^>]*>.*?</style>', ' ', bruto, flags=re.S)
        bruto = re.sub(r'<[^>]+>', ' ', bruto)
        bruto = re.sub(r'#[0-9A-Fa-f]{3,8}', ' ', bruto)     # cores
    bruto = re.sub(r'`[^`]*`', ' ', limpa_ruido(bruto))
    fora = []
    for m in PADRAO_NUM.finditer(bruto):
        v = normaliza(m.group(0))
        if v is None or v in IGNORAR_EXATOS:
            continue
        if not casa(v, universo_global):
            ini = max(0, m.start() - 42)
            fora.append((m.group(0), ' '.join(bruto[ini:m.end() + 30].split())))
    return fora


if __name__ == '__main__':
    mostrar = '--tudo' in sys.argv
    print('=' * 96)
    print('VERIFICAÇÃO 1 · todo número em markdown de notebook tem saída que o produz?')
    print('=' * 96)
    universo = universo_global(NOTEBOOKS)
    total_falhas = 0
    for nb_path in NOTEBOOKS:
        n_saidas, n_chars, falhas = verifica_notebook(nb_path, mostrar, global_=universo)
        marca = 'OK' if not falhas else f'{len(falhas)} SEM LASTRO'
        print(f'{nb_path.name:32s} {n_saidas:5d} números em saídas | {marca}')
        for bruto, trecho in falhas[:12 if not mostrar else 999]:
            print(f'      → {bruto:>12s}   ...{trecho}...')
        if len(falhas) > 12 and not mostrar:
            print(f'      (+{len(falhas)-12} outros, use --tudo)')
        total_falhas += len(falhas)
    print()
    print(f'TOTAL: {total_falhas} números sem lastro nos notebooks')
    print(f'universo de números validados: {len(universo)}')
    print()
    print('=' * 96)
    print('VERIFICAÇÃO 2 · números em docs e slides existem em algum notebook?')
    print('=' * 96)
    for caminho in DOCS:
        fora = verifica_texto_externo(caminho, universo)
        nome = str(caminho.relative_to(RAIZ))
        print(f'{nome:38s} {"OK" if not fora else f"{len(fora)} fora do universo"}')
        for bruto, trecho in fora[:10 if not mostrar else 999]:
            print(f'      → {bruto:>12s}   ...{trecho}...')
        if len(fora) > 10 and not mostrar:
            print(f'      (+{len(fora)-10} outros)')
    print()
    n_slides_ruins = 0
    for caminho in SLIDES:
        fora = verifica_texto_externo(caminho, universo)
        if fora:
            n_slides_ruins += 1
            print(f'{caminho.name:14s} {len(fora):3d} fora: '
                  + ' | '.join(b for b, _ in fora[:8]))
    print()
    print(f'slides com número fora do universo: {n_slides_ruins} de {len(SLIDES)}')
