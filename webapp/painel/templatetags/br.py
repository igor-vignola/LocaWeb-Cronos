# -*- coding: utf-8 -*-
"""Filtros de formatacao no padrao pt-BR e um par de utilidades de template."""
import os

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

registro = template.Library()
register = registro


@registro.simple_tag
def folha(caminho):
    """Como o {% static %}, mais a marca de tempo do arquivo.

    Em DEBUG o {% static %} devolve o caminho cru, sem hash. Como a resposta do dev server
    nao traz Cache-Control, o navegador segura a folha antiga e a tela aparece com o HTML
    novo e o CSS velho — sem estilo, sem erro nenhum no log. Isso custou uma ida e volta.

    A marca de tempo troca a URL a cada gravacao, entao um F5 comum ja basta. Em producao o
    ManifestStaticFilesStorage versiona pelo hash e o parametro so acompanha.
    """
    url = static(caminho)
    arq = finders.find(caminho)
    return f'{url}?v={int(os.path.getmtime(arq))}' if arq else url


@registro.filter
def num(v, casas=1):
    """1234.5 -> 1.234,5"""
    try:
        return f'{float(v):,.{int(casas)}f}'.replace(',', '@').replace('.', ',').replace('@', '.')
    except (TypeError, ValueError):
        return v


@registro.filter
def mil(v):
    try:
        return f'{int(v):,}'.replace(',', '.')
    except (TypeError, ValueError):
        return v


@registro.filter
def pc(v, casas=1):
    """Fracao 0..1 para porcentagem."""
    try:
        return num(float(v) * 100, casas)
    except (TypeError, ValueError):
        return v


@registro.filter
def vezes(v, base):
    """Quantas vezes um valor e maior que a referencia."""
    try:
        return round(float(v) / float(base))
    except (TypeError, ValueError, ZeroDivisionError):
        return '—'


@registro.filter
def tom_risco(v):
    v = float(v)
    return 'no' if v >= 10 else ('wn' if v >= 3 else 'ok')


@registro.filter
def tom_nota(v):
    v = float(v)
    return '#DC2626' if v < 40 else ('#B45309' if v < 65 else '#059669')


@registro.filter
def item(d, chave):
    """Acesso por chave em dicionario, que o template do Django nao faz sozinho."""
    try:
        return d[chave]
    except (KeyError, IndexError, TypeError):
        return ''


@registro.simple_tag
def icone(nome, tam=19, classe=''):
    """Referencia um glifo do sprite. O arquivo e injetado uma vez no _campo.html."""
    from django.utils.safestring import mark_safe
    return mark_safe(
        f'<svg class="ic {classe}" width="{tam}" height="{tam}" aria-hidden="true">'
        f'<use href="#i-{nome}"></use></svg>')


@registro.simple_tag
def chip(nome, tom='ac', tam=18):
    """Glifo em recipiente tingido."""
    from django.utils.safestring import mark_safe
    return mark_safe(f'<span class="chp t-{tom}">{icone(nome, tam)}</span>')
