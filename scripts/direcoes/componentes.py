# -*- coding: utf-8 -*-
"""Componentes compartilhados pelas abas da aplicacao Cronos.

Cinco abas na mesma regua: cada card diz em uma linha o que ele e, cada tela e lida em
atos, e clicar em incidente, ativo ou produto abre um modal com o detalhe e a explicacao
do modelo. Navegacao sem recarregar. Paleta de comando em Ctrl+K.

Todo numero sai de parquet gerado por notebook. Onde o dado nao existe, a tela diz que
nao existe em vez de inventar.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dados import (ACIMA_10, ATIVOS, BASE_20, COMPONENTES, CORTE, DELTA_TAXA, DIA_HOJE, ELEG_30,
                   ELEGIVEIS, EM_ABERTO, FILA_HOJE, FILA_TODA, FUT3, HIST_ATIVO, HORAS,
                   HORA_PICO, HORA_RISCO, HOJE2, HOJE3, LBL_DIA, MEDIA_BASE, MES_LBL, N_FILA,
                   ONTEM, ONTEM_TOTAL, ONTEM_VIOL, REAL3, SEMANA, SEM_VIOL, TAXA_30, TOP50_PEGA,
                   TOTAL_VIOL, ULTIMOS_DIAS, VIOL_30, VIOL_PERIODO, causas, dm, grupos, mil,
                   proj, pt, recor, saude)
from estilo import CSS as CSS_BASE
from fundo import CSS_CAMPO, campo
from icones import CSS_ICO_CLARO, chip, ico

MX_H = max(x['abertos'] for x in HORAS)
TOPO = FILA_TODA.iloc[0]
PIOR = saude.index[-1]
MELHOR = saude.index[0]
HOJE_MAX = float(FILA_HOJE['risco'].max())
HOJE_ACIMA10 = int((FILA_HOJE['risco'] >= 10).sum())


# ══════════ componentes compartilhados ═════════════════════════════════════
def ato(n, titulo, pergunta):
    return (f'<div class="ato"><span class="ato-n">{n}</span>'
            f'<div><h2>{titulo}</h2><p>{pergunta}</p></div></div>')


def cab(icone, titulo, oque, extra=''):
    return (f'<div class="hdr"><div class="hdr-t">{ico(icone, 16)}'
            f'<div><h3>{titulo}</h3><p>{oque}</p></div></div>{extra}</div>')


def filtros(grupo, opcoes, ativo=0):
    return ('<div class="fg">' + ''.join(
        f'<button class="fb{" on" if i == ativo else ""}" data-g="{grupo}" data-v="{v}">{r}</button>'
        for i, (v, r) in enumerate(opcoes)) + '</div>')


def linha_metrica(icone, tom, titulo, sub, valor, unidade='', tom_v='', extra=''):
    return (f'<div class="mr">{chip(icone, tom)}<div class="mr-t"><b>{titulo}</b>'
            f'<span>{sub}</span></div><span class="mr-v {tom_v}">{valor}'
            f'{f"<u>{unidade}</u>" if unidade else ""}{extra}</span></div>')


def vazio(icone, titulo, texto):
    """Estado vazio: a tela diz que nao ha nada, em vez de ficar em branco."""
    return (f'<div class="vz">{chip(icone, "nt", 20)}<b>{titulo}</b><span>{texto}</span></div>')


def barras_mes(hist, w=760, h=92, cls='mh'):
    if not hist:
        return ''
    mx = max(m['passagens'] for m in hist) or 1
    lar = w / len(hist)
    corpo = ''.join(
        f'<g><rect x="{i*lar+3:.1f}" y="{h-16-m["passagens"]/mx*(h-20):.1f}" '
        f'width="{lar-6:.1f}" height="{m["passagens"]/mx*(h-20):.1f}" rx="3" class="mh-p"/>'
        f'<rect x="{i*lar+3:.1f}" y="{h-16-m["violacoes"]/mx*(h-20):.1f}" '
        f'width="{lar-6:.1f}" height="{m["violacoes"]/mx*(h-20):.1f}" rx="3" class="mh-v"/></g>'
        f'<text class="mh-l" x="{i*lar+lar/2:.1f}" y="{h-2}" text-anchor="middle">'
        f'{MES_LBL[m["mes"]-1]}</text>' for i, m in enumerate(hist))
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}">{corpo}</svg>'


def trilho(w=1000, h=150, n_real=20, n_prev=8):
    real = REAL3.tail(n_real).reset_index(drop=True)
    fut = FUT3.head(n_prev).reset_index(drop=True)
    esc = [*real['valor'], *fut['valor'], *fut['baixo'], *fut['alto']]
    lo, hi = min(esc), max(esc)
    vao = (hi - lo) or 1
    n = len(real) + len(fut)
    px = lambda i: 6 + i / (n - 1) * (w - 12)
    py = lambda v: h - 26 - (v - lo) / vao * (h - 56)
    pr = [(px(i), py(v)) for i, v in enumerate(real['valor'])]
    corte = pr[-1]
    pf = [corte] + [(px(len(real) + i), py(v)) for i, v in enumerate(fut['valor'])]
    suave = lambda ps: (f'M{ps[0][0]:.1f} {ps[0][1]:.1f}' + ''.join(
        f' C{(ps[i-1][0]+ps[i][0])/2:.1f} {ps[i-1][1]:.1f} {(ps[i-1][0]+ps[i][0])/2:.1f} '
        f'{ps[i][1]:.1f} {ps[i][0]:.1f} {ps[i][1]:.1f}' for i in range(1, len(ps))))
    hi_p = [(px(len(real) + i), py(v)) for i, v in enumerate(fut['alto'])]
    lo_p = [(px(len(real) + i), py(v)) for i, v in enumerate(fut['baixo'])]
    bd = (f'M{corte[0]:.1f} {corte[1]:.1f} L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in hi_p)
          + ' L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(lo_p)) + ' Z')
    area = suave(pr) + f' L{corte[0]:.1f} {h} L6 {h} Z'
    xh, yh = pf[1]
    return f'''<div class="tr">
      <svg viewBox="0 0 {w} {h}" preserveAspectRatio="none">
        <defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#2563EB" stop-opacity=".2"/>
          <stop offset="1" stop-color="#2563EB" stop-opacity="0"/></linearGradient></defs>
        <path class="t-a" d="{area}" fill="url(#ga)"/><path class="t-bd" d="{bd}"/>
        <line class="t-ag" x1="{corte[0]:.1f}" y1="8" x2="{corte[0]:.1f}" y2="{h-14}"/>
        <path class="t-l" d="{suave(pr)}"/><path class="t-f" d="{suave(pf)}"/>
        <circle class="t-h" cx="{corte[0]:.1f}" cy="{corte[1]:.1f}" r="11"/>
        <circle class="t-n" cx="{corte[0]:.1f}" cy="{corte[1]:.1f}" r="4.5"/>
      </svg>
      <div class="anp" style="left:{xh/w*100:.1f}%;top:{(yh-40)/h*100:.0f}%">
        {pt(HOJE3['valor'], 0)} hoje</div>
      <div class="tr-x"><span>{dm(real['dia'].iloc[0])}</span>
        <span class="ag" style="left:{corte[0]/w*100:.1f}%">{dm(DIA_HOJE)}</span>
        <span>{dm(fut['dia'].iloc[-1])}</span></div>
    </div>'''


def heroi():
    """A linha da marca, grande e sozinha. A faixa de 24h foi para o card da secao 01,
    onde tem espaco — encolher o heroi para caber tres coisas piorava os tres."""
    sr = REAL3.tail(24)['valor'].rolling(5, min_periods=1).mean()
    real = REAL3.tail(24).assign(valor=sr).iloc[::2].reset_index(drop=True)
    fut = FUT3.head(6).reset_index(drop=True)
    w, h = 380, 244
    esc = [*real['valor'], *fut['valor'], *fut['alto'], *fut['baixo']]
    lo, hi = min(esc), max(esc)
    vao = (hi - lo) or 1
    n = len(real) + len(fut)
    px = lambda i: 18 + i / (n - 1) * (w - 36)
    py = lambda v: h - 34 - (v - lo) / vao * (h - 78)
    pr = [(px(i), py(v)) for i, v in enumerate(real['valor'])]
    no = pr[-1]
    pf = [no] + [(px(len(real) + i), py(v)) for i, v in enumerate(fut['valor'])]
    hip = [(px(len(real) + i), py(v)) for i, v in enumerate(fut['alto'])]
    lop = [(px(len(real) + i), py(v)) for i, v in enumerate(fut['baixo'])]
    suave = lambda ps: (f'M{ps[0][0]:.1f} {ps[0][1]:.1f}' + ''.join(
        f' C{(ps[i-1][0]+ps[i][0])/2:.1f} {ps[i-1][1]:.1f} {(ps[i-1][0]+ps[i][0])/2:.1f} '
        f'{ps[i][1]:.1f} {ps[i][0]:.1f} {ps[i][1]:.1f}' for i in range(1, len(ps))))
    bd = (f'M{no[0]:.1f} {no[1]:.1f} L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in hip)
          + ' L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(lop)) + ' Z')
    v = float(HOJE3['valor'])
    leve, cheio = BASE_20 * .8, BASE_20 * 1.2
    zona = ('ok', 'dia leve') if v < leve else (('ac', 'dia normal') if v < cheio
                                                else ('no', 'dia cheio'))
    return f'''<div class="hc">
      <svg class="hc-l" viewBox="0 0 {w} {h}">
        <path class="hl-bd" d="{bd}"/><path class="hl-l" d="{suave(pr)}"/>
        <path class="hl-f" d="{suave(pf)}"/>
        <circle class="hl-o3" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="30"/>
        <circle class="hl-o2" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="20"/>
        <circle class="hl-o1" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="11"/>
        <circle class="hl-n" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="5.6"/>
        <text class="hl-x" x="18" y="{h-8}">{dm(real['dia'].iloc[0])}</text>
        <text class="hl-x ag" x="{no[0]:.1f}" y="{h-8}" text-anchor="middle">agora</text>
        <text class="hl-x" x="{w-18}" y="{h-8}" text-anchor="end">{dm(fut['dia'].iloc[-1])}</text>
      </svg>
      <div class="hc-v"><b>{pt(v, 0)}</b>
        <div class="hc-vt"><span class="hc-z z-{zona[0]}">{zona[1]}</span>
          <em>previstos hoje no P3 · faixa de {pt(HOJE3['baixo'], 0)} a
            {pt(HOJE3['alto'], 0)}</em></div></div>
    </div>'''


def faixa_24h(w=560, h=132):
    lar = (w - 16) / 24
    barras = ''.join(
        f'<rect class="h24 t-{"no" if x["taxa"] >= 1.6 else ("wn" if x["taxa"] >= 1.1 else "ok")}"'
        f' style="--i:{x["h"]}" x="{8 + x["h"]*lar + 1.6:.1f}"'
        f' y="{h - 26 - (10 + (h - 56) * x["abertos"] / MX_H):.1f}" width="{lar - 3.2:.1f}"'
        f' height="{10 + (h - 56) * x["abertos"] / MX_H:.1f}" rx="3">'
        f'<title>{x["h"]:02d}h · {mil(x["abertos"])} abertos · {pt(x["taxa"], 2)}% violaram</title>'
        f'</rect>' for x in HORAS)
    rot = ''.join(
        f'<text class="h24-x" x="{8 + hh*lar + lar/2:.1f}" y="{h - 8}" text-anchor="middle">'
        f'{hh:02d}h</text>' for hh in (0, 3, 6, 9, 12, 15, 18, 21))
    ax = 8 + 7 * lar + lar / 2
    return f'''<div class="fx24">
      <svg viewBox="0 0 {w} {h}">
        <line class="h24-ag" x1="{ax:.1f}" y1="6" x2="{ax:.1f}" y2="{h - 30}"/>
        {barras}{rot}
        <circle class="h24-n" cx="{ax:.1f}" cy="6" r="3.6"/>
        <text class="h24-al" x="{ax + 6:.1f}" y="10">agora</text>
      </svg>
      <div class="h24-l"><span><i class="t-ok"></i>abaixo de 1,1%</span>
        <span><i class="t-wn"></i>1,1 a 1,6%</span><span><i class="t-no"></i>acima de 1,6%</span>
        <span class="dica">passe o cursor em qualquer hora</span></div>
    </div>'''


def meta(p):
    r = proj.loc[p]
    dentro = r['situação projetada'] == 'dentro da meta'
    lim = r['meta máxima']
    esc = lim * 1.35
    k = 'ok' if dentro else 'no'
    return f'''<div class="mt">
      <div class="mt-h"><span class="mt-p">{p}</span>
        <span class="mt-v {k}">{pt(r['projeção'])}</span>
        <span class="mt-l">de {int(lim)}</span>
        <span class="tg {k}">{'dentro' if dentro else 'acima'}</span></div>
      <div class="mt-b">
        <s class="{k}" style="left:{r['faixa baixa']/esc*100:.1f}%;width:{(r['faixa alta']-r['faixa baixa'])/esc*100:.1f}%"></s>
        <i class="{k}" style="left:{r['projeção']/esc*100:.1f}%"></i>
        <u style="left:{lim/esc*100:.1f}%"></u></div>
      <div class="mt-f">a barra é a faixa de {pt(r['faixa baixa'],0)} a {pt(r['faixa alta'],0)} ·
        o traço fino é a projeção · a linha branca é a meta</div>
    </div>'''


def item_fila(r, i):
    tom = 'crit' if r['risco'] >= 10 else ('alta' if r['risco'] >= 3 else 'leve')
    return f'''<button class="it" style="--i:{i}" data-mod="inc" data-k="{r['incidente']}">
      <span class="it-r {tom}">{pt(r['risco'], 0)}%</span>
      <span class="it-t"><b class="id">{r['incidente']}</b>
        <span><u>{ico('produto', 12)}{r['produto']}</u><u>{ico('pessoas', 12)}{r['equipe']}</u>
          <u>{ico('ativo', 12)}<span class="id">{r['ativo'] if r['ativo'] != 'None' else 'sem ativo'}</span></u></span></span>
      <span class="it-b"><em>{dm(r['dia'])} · {int(r['hora']):02d}h</em>
        <b>{r['prioridade']}</b></span>
      <span class="sq">{ico('seta', 15)}</span></button>'''
