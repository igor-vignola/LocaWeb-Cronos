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


# Glifos do redesenho de outubro/2026, desenhados numa grade de 16 px com traço. Moram aqui, e
# não no sprite, porque o traço varia de lugar para lugar (1,6 na navegação, 2,2 no visto do
# selo) e o sprite fixa a espessura no <symbol>.
GLIFOS = {
    'grid': 'M2.5 2.5h4.5v4.5h-4.5zM9 2.5h4.5v4.5H9zM2.5 9h4.5v4.5h-4.5zM9 9h4.5v4.5H9z',
    'trend': 'M2 12 6 8l3 2.5L14 5',
    'trend_up': 'M2 12 6 8l3 2.5L14 5M10 5h4v4',
    'target': 'M8 2a6 6 0 1 0 0 12A6 6 0 0 0 8 2zM8 5a3 3 0 1 0 0 6 3 3 0 0 0 0-6z',
    'list': 'M3 4h10M3 8h10M3 12h6',
    'heart': 'M8 13.5S2.5 10 2.5 6a2.8 2.8 0 0 1 5.5-.8A2.8 2.8 0 0 1 13.5 6c0 4-5.5 7.5-5.5 7.5z',
    'search': 'M7 2.5a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9zM10.5 10.5 13.5 13.5',
    'up': 'M2 11l4-4 3 3 5-5M10 5h4v4',
    'down': 'M2 5l4 4 3-3 5 5M10 11h4V7',
    'check': 'M3 8.5 6.5 12 13 4.5',
    'alert': 'M8 2.5 14 13H2L8 2.5zM8 7v2.5M8 11.3v.2',
    'shield': 'M8 1.8 13 3.8v4c0 3.2-2.2 5.4-5 6.4-2.8-1-5-3.2-5-6.4v-4L8 1.8zM5.8 8l1.6 1.6L10.4 6.6',
    'cal': 'M2.5 4h11v9.5h-11zM2.5 7h11M5.5 2.5v3M10.5 2.5v3',
    'box': 'M8 1.8 13.5 5v6L8 14.2 2.5 11V5L8 1.8zM2.5 5 8 8.2 13.5 5M8 8.2v6',
    'team': 'M6 3a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM1.8 13.5c.5-2.3 2.2-3.5 4.2-3.5s3.7 1.2 4.2 3.5',
    'chip': 'M4 4h8v8H4zM6 1.5v2.5M10 1.5v2.5M6 12v2.5M10 12v2.5',
    'clock': 'M8 2a6 6 0 1 0 0 12A6 6 0 0 0 8 2zM8 5v3l2 1.5',
    'timer': 'M8 3a5.5 5.5 0 1 0 0 11A5.5 5.5 0 0 0 8 3zM8 5.5v3l2 1.5M6.5 1.5h3',
    'bell': 'M4 11V7a4 4 0 0 1 8 0v4l1 1.5H3L4 11ZM6.5 14h3',
    'bars': 'M2 13h12M4 13V8M8 13V4M12 13V6',
    'stack': 'M2.5 3h11v4h-11zM2.5 9h11v4h-11z',
    'x': 'M4 4l8 8M12 4l-8 8',
    'arrow': 'M3 8h10M9 4l4 4-4 4',
    'sun': 'M8 4.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zM8 1v1.5M8 13.5V15M1 8h1.5M13.5 8H15M3 3l1 1M12 12l1 1M13 3l-1 1M4 12l-1 1',
    'info': 'M8 2a6 6 0 1 0 0 12A6 6 0 0 0 8 2zM8 7.2v3.6M8 5.2v.2',
    'refresh': 'M13 8a5 5 0 1 1-1.5-3.6M13 2.5v3h-3',
    'bolt': 'M9 1.5 3.5 9H8l-1 5.5L12.5 7H8l1-5.5z',
    'help': 'M8 2a6 6 0 1 0 0 12A6 6 0 0 0 8 2zM6.3 6.2a1.8 1.8 0 1 1 2.4 1.7c-.5.2-.7.6-.7 1.1v.3M8 11.3v.2',
    'folder': 'M2 4.5h4l1.5 1.5H14v6.5H2z',
    'server': 'M2.5 2.5h11v4h-11zM2.5 9.5h11v4h-11zM5 4.5h.1M5 11.5h.1',
    'sort': 'M5 3v10M2.5 10.5 5 13l2.5-2.5M11 13V3M8.5 5.5 11 3l2.5 2.5',
    'calm': 'M8 2v12M3 9l5 5 5-5',
    'bulb': 'M6 12.5h4M6.5 14.5h3M8 1.5a4.5 4.5 0 0 0-2.5 8.2V11h5V9.7A4.5 4.5 0 0 0 8 1.5z',
    'scale': 'M8 2v12M4 14h8M3 5h10M3 5l-2 5h4zM13 5l-2 5h4z',
    'dot': 'M8 6a2 2 0 1 0 0 4 2 2 0 0 0 0-4z',
    # códigos de fechamento e problemas recorrentes (Causas)
    'c_hw': 'M3 4.5h10v7H3zM5.5 13.5h5M8 11.5v2',
    'c_net': 'M8 2.5v3M3.5 13.5v-3h9v3M8 5.5v5',
    'c_disk': 'M3 4.5c0-1.1 2.2-2 5-2s5 .9 5 2v7c0 1.1-2.2 2-5 2s-5-.9-5-2zM3 4.5c0 1.1 2.2 2 5 2s5-.9 5-2',
    'c_db': 'M3 4.5c0-1.1 2.2-2 5-2s5 .9 5 2v7c0 1.1-2.2 2-5 2s-5-.9-5-2zM3 8c0 1.1 2.2 2 5 2s5-.9 5-2',
    'c_user': 'M8 3a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM3.5 13.5c.5-2.3 2.3-3.5 4.5-3.5s4 1.2 4.5 3.5',
    'c_mon': 'M2 8h3l1.5-3 3 6L11 8h3',
    'c_chg': 'M3 5h8l-2-2M13 11H5l2 2',
    'c_cloud': 'M4.5 12.5a3 3 0 0 1-.3-6 4 4 0 0 1 7.6 1 2.5 2.5 0 0 1 .2 5z',
    'c_app': 'M2.5 3.5h11v9h-11zM2.5 6h11',
    'c_lock': 'M4 7.5h8v6H4zM5.5 7.5V5.5a2.5 2.5 0 0 1 5 0v2',
    'c_os': 'M3 3h10v10H3zM6 6h4v4H6z',
    'c_doc': 'M4 2.5h6l2.5 2.5v8.5H4zM10 2.5V5h2.5',
    'c_list': 'M2.5 3.5h11v9h-11zM5 6.5h6M5 9.5h4',
}


@registro.simple_tag
def ic(nome, tam=15, traco=1.7, classe=''):
    """Glifo do redesenho, em linha, herdando a cor do texto."""
    from django.utils.safestring import mark_safe
    d = GLIFOS.get(nome, '')
    cls = f' class="{classe}"' if classe else ''
    return mark_safe(
        f'<svg{cls} width="{tam}" height="{tam}" viewBox="0 0 16 16" fill="none" '
        f'stroke="currentColor" stroke-width="{traco}" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>')
