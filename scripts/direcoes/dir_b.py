# -*- coding: utf-8 -*-
"""Direcao B · Previsao do dia.

Aposta: previsao do tempo, nao painel de BI. Clara, editorial, tipografia grande, uma frase
em linguagem comum antes de qualquer numero. O heroi e o relogio de 24 horas: cada hora do
dia como uma barra radial, a taxa de violacao pintando o anel de fora, e o ponteiro no agora.

Assinatura: campo de linhas do proprio historico ao fundo.
Devices: abas de dia (clima), chips de metrica (ecofarm), um card escuro entre os claros
para a meta (plataforma), anel com fracao (plano), circulos por dia (streak).
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dados import (ATIVOS, BASE_20, COMPONENTES, DELTA_TAXA, DIA_HOJE, ELEG_30, EM_ABERTO, FILA,
                   FUT3, HIST_ATIVO, HORAS, HORA_PICO, HORA_RISCO, HOJE2, HOJE3, LBL_DIA,
                   MEDIA_BASE, MES_LBL, ONTEM, ONTEM_TOTAL, ONTEM_VIOL, REAL3, SEMANA, SEM_VIOL, SINAIS,
                   TAXA_30, TOTAL_VIOL, ULTIMOS_DIAS, VIOL_30, dm, mil, proj, pt, saude)
from fundo import CSS_CAMPO, campo
from icones import CSS_ICO_CLARO, chip, ico

DEST = Path.cwd() / 'prototipos' / 'telas' / 'direcoes'
DEST.mkdir(parents=True, exist_ok=True)
topo = FILA[0]
pior = saude.index[-1]
MX_H = max(x['abertos'] for x in HORAS)


def relogio(tam=340):
    """Relogio de 24 horas: barra radial por hora, anel externo pela taxa de violacao.
    Cronos e tempo — o heroi da tela tinha de ser um relogio."""
    c = tam / 2
    r0, r1, ra = tam * .215, tam * .40, tam * .445
    fatia = 360 / 24
    partes = []
    for x in HORAS:
        a0 = x['h'] * fatia - 90 + 1.4
        a1 = (x['h'] + 1) * fatia - 90 - 1.4
        am = (a0 + a1) / 2
        alt = r0 + (r1 - r0) * (x['abertos'] / MX_H)
        pol = lambda rr, aa: (c + rr * math.cos(math.radians(aa)),
                              c + rr * math.sin(math.radians(aa)))
        x0, y0 = pol(r0, a0)
        x1, y1 = pol(alt, a0)
        x2, y2 = pol(alt, a1)
        x3, y3 = pol(r0, a1)
        tom = 'no' if x['taxa'] >= 1.6 else ('wn' if x['taxa'] >= 1.1 else 'ok')
        partes.append(
            f'<path class="rl-b t-{tom}" data-h="{x["h"]}" style="--i:{x["h"]}"'
            f' d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f} A{alt:.1f} {alt:.1f} 0 0 1 {x2:.1f} {y2:.1f}'
            f' L{x3:.1f} {y3:.1f} A{r0:.1f} {r0:.1f} 0 0 0 {x0:.1f} {y0:.1f} Z">'
            f'<title>{x["h"]:02d}h · {mil(x["abertos"])} abertos · {pt(x["taxa"], 2)}% violaram</title>'
            f'</path>')
        # marca externa nas horas de maior taxa
        if x['taxa'] >= 1.6:
            mx0, my0 = pol(ra, a0)
            mx1, my1 = pol(ra, a1)
            partes.append(f'<path class="rl-m" d="M{mx0:.1f} {my0:.1f} '
                          f'A{ra:.1f} {ra:.1f} 0 0 1 {mx1:.1f} {my1:.1f}"/>')
    rot = ''.join(
        f'<text class="rl-h" x="{c + (ra + 15) * math.cos(math.radians(h * fatia - 90)):.1f}" '
        f'y="{c + (ra + 15) * math.sin(math.radians(h * fatia - 90)) + 4:.1f}">{h:02d}</text>'
        for h in (0, 6, 12, 18))
    ang = 7 * fatia - 90        # o painel abre as 07h00
    ix, iy = c + (r0 - 6) * math.cos(math.radians(ang)), c + (r0 - 6) * math.sin(math.radians(ang))
    px, py = c + (ra + 6) * math.cos(math.radians(ang)), c + (ra + 6) * math.sin(math.radians(ang))
    return f'''<div class="rl">
      <svg viewBox="0 0 {tam} {tam}">
        <circle class="rl-g" cx="{c}" cy="{c}" r="{r1:.1f}"/>
        <circle class="rl-g" cx="{c}" cy="{c}" r="{r0:.1f}"/>
        {''.join(partes)}{rot}
        <line class="rl-p" x1="{ix:.1f}" y1="{iy:.1f}" x2="{px:.1f}" y2="{py:.1f}"/>
        <circle class="rl-c" cx="{px:.1f}" cy="{py:.1f}" r="4.5"/>
        <text class="rl-ag" x="{px:.1f}" y="{py - 12:.1f}">agora</text>
      </svg>
      <div class="rl-in"><b>{pt(HOJE3['valor'], 0)}</b><span>previstos hoje</span>
        <em>faixa de {pt(HOJE3['baixo'], 0)} a {pt(HOJE3['alto'], 0)}</em></div>
    </div>'''



def heroi_linha(tam=360):
    """B1 · A marca virada heroi: a propria linha do Cronos em escala. O medido em traco
    cheio, o no pulsando no agora e a previsao saindo dele."""
    sr = REAL3.tail(24)['valor'].rolling(5, min_periods=1).mean()
    real = REAL3.tail(24).assign(valor=sr).iloc[::2].reset_index(drop=True)
    fut = FUT3.head(6).reset_index(drop=True)
    w, h = tam, tam * .78
    esc = [*real['valor'], *fut['valor'], *fut['alto'], *fut['baixo']]
    lo, hi = min(esc), max(esc)
    vao = (hi - lo) or 1
    n = len(real) + len(fut)
    px = lambda i: 16 + i / (n - 1) * (w - 32)
    py = lambda v: h - 46 - (v - lo) / vao * (h - 98)
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
    return f'''<div class="hl">
      <svg viewBox="0 0 {w:.0f} {h:.0f}">
        <path class="hl-bd" d="{bd}"/>
        <path class="hl-l" d="{suave(pr)}"/>
        <path class="hl-f" d="{suave(pf)}"/>
        <circle class="hl-o3" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="27"/>
        <circle class="hl-o2" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="18"/>
        <circle class="hl-o1" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="10"/>
        <circle class="hl-n" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="5.2"/>
        <text class="hl-x" x="16" y="{h - 14:.0f}">{dm(real['dia'].iloc[0])}</text>
        <text class="hl-x ag" x="{no[0]:.1f}" y="{h - 14:.0f}" text-anchor="middle">agora</text>
        <text class="hl-x" x="{w - 16}" y="{h - 14:.0f}" text-anchor="end">{dm(fut['dia'].iloc[-1])}</text>
      </svg>
      <div class="hl-v"><b>{pt(HOJE3['valor'], 0)}</b>
        <span>previstos hoje · faixa {pt(HOJE3['baixo'], 0)} a {pt(HOJE3['alto'], 0)}</span></div>
    </div>'''


def heroi_faixa(w=360):
    """B2 · O dia esticado em linha reta: mesma informacao do relogio, mas linear.
    Uma barra por hora, altura pelo volume, cor pela taxa de violacao."""
    h = 214
    lar = (w - 20) / 24
    barras = []
    for x in HORAS:
        alt = 12 + (h - 82) * (x['abertos'] / MX_H)
        tom = 'no' if x['taxa'] >= 1.6 else ('wn' if x['taxa'] >= 1.1 else 'ok')
        barras.append(
            f'<rect class="hf-b t-{tom}" style="--i:{x["h"]}" x="{10 + x["h"]*lar + 1.4:.1f}" '
            f'y="{h - 42 - alt:.1f}" width="{lar - 2.8:.1f}" height="{alt:.1f}" rx="3">'
            f'<title>{x["h"]:02d}h · {mil(x["abertos"])} abertos · {pt(x["taxa"], 2)}% violaram</title>'
            f'</rect>')
    rot = ''.join(
        f'<text class="hf-x" x="{10 + hh*lar + lar/2:.1f}" y="{h - 24}" text-anchor="middle">'
        f'{hh:02d}h</text>' for hh in (0, 4, 8, 12, 16, 20))
    ax = 10 + 7 * lar + lar / 2
    return f'''<div class="hf">
      <svg viewBox="0 0 {w} {h}">
        <line class="hf-ag" x1="{ax:.1f}" y1="16" x2="{ax:.1f}" y2="{h - 46}"/>
        {''.join(barras)}{rot}
        <circle class="hf-n" cx="{ax:.1f}" cy="16" r="4"/>
        <text class="hf-al" x="{ax:.1f}" y="8" text-anchor="middle">agora</text>
      </svg>
      <div class="hf-l">
        <span><i class="t-ok"></i>abaixo de 1,1%</span><span><i class="t-wn"></i>1,1 a 1,6%</span>
        <span><i class="t-no"></i>acima de 1,6%</span></div>
      <div class="hf-v"><b>{pt(HOJE3['valor'], 0)}</b><span>previstos hoje no P3</span></div>
    </div>'''


def heroi_medidor(tam=340):
    """B3 · Um veredito em vez de uma distribuicao. Ponteiro no volume previsto e zonas
    nomeadas derivadas da linha de base dos ultimos vinte dias uteis."""
    leve, cheio = BASE_20 * .8, BASE_20 * 1.2
    topo_esc = BASE_20 * 1.55
    c, r = tam / 2, tam * .375
    ang = lambda v: min(v / topo_esc, 1) * 232 - 116
    pol = lambda a, rr=r: (c + rr * math.sin(math.radians(a)), c - rr * math.cos(math.radians(a)))
    zonas = [(0, leve, 'ok', 'dia leve'), (leve, cheio, 'ac', 'dia normal'),
             (cheio, topo_esc, 'no', 'dia cheio')]
    arcos = ''.join(
        f'<path class="md-z z-{k}" d="M{pol(ang(a))[0]:.1f} {pol(ang(a))[1]:.1f} '
        f'A{r} {r} 0 0 1 {pol(ang(b))[0]:.1f} {pol(ang(b))[1]:.1f}"/>' for a, b, k, _ in zonas)
    v = float(HOJE3['valor'])
    xb, yb = pol(ang(HOJE3['baixo']))
    xa, ya = pol(ang(HOJE3['alto']))
    xv, yv = pol(ang(v))
    ix, iy = pol(ang(v), r * .40)
    zona = next(z for z in zonas if z[0] <= v < z[1])
    mx1, my1 = pol(ang(BASE_20), r * .84)
    mx2, my2 = pol(ang(BASE_20), r * 1.13)
    tx, ty = pol(ang(BASE_20), r * 1.3)
    return f'''<div class="mdd">
      <svg viewBox="0 0 {tam} {tam * .8:.0f}">
        {arcos}
        <path class="md-fx" d="M{xb:.1f} {yb:.1f} A{r} {r} 0 0 1 {xa:.1f} {ya:.1f}"/>
        <line class="md-md" x1="{mx1:.1f}" y1="{my1:.1f}" x2="{mx2:.1f}" y2="{my2:.1f}"/>
        <text class="md-ml" x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle">média {pt(BASE_20, 0)}</text>
        <line class="md-p" x1="{ix:.1f}" y1="{iy:.1f}" x2="{xv:.1f}" y2="{yv:.1f}"/>
        <circle class="md-c" cx="{xv:.1f}" cy="{yv:.1f}" r="6.5"/>
      </svg>
      <div class="mdd-in"><b>{pt(v, 0)}</b>
        <span class="mdd-z z-{zona[2]}">{zona[3]}</span>
        <em>faixa de {pt(HOJE3['baixo'], 0)} a {pt(HOJE3['alto'], 0)} · a média dos últimos
          vinte dias úteis é {pt(BASE_20, 0)}</em></div>
    </div>'''



def heroi_completo(tam=380):
    """B1 completa. Tres camadas de tempo: a linha dos ultimos dias com o no no agora,
    o veredito do dia em uma palavra, e as 24 horas de hoje como base."""
    sr = REAL3.tail(24)['valor'].rolling(5, min_periods=1).mean()
    real = REAL3.tail(24).assign(valor=sr).iloc[::2].reset_index(drop=True)
    fut = FUT3.head(6).reset_index(drop=True)
    w, h = tam, 176
    esc = [*real['valor'], *fut['valor'], *fut['alto'], *fut['baixo']]
    lo, hi = min(esc), max(esc)
    vao = (hi - lo) or 1
    n = len(real) + len(fut)
    px = lambda i: 18 + i / (n - 1) * (w - 36)
    py = lambda v: h - 30 - (v - lo) / vao * (h - 66)
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

    # veredito: a mesma regra da B3, derivada da linha de base recente
    v = float(HOJE3['valor'])
    leve, cheio = BASE_20 * .8, BASE_20 * 1.2
    zona = ('ok', 'dia leve') if v < leve else (('ac', 'dia normal') if v < cheio
                                                else ('no', 'dia cheio'))

    # faixa de 24h como base: as horas de hoje, cor pela taxa de violacao
    fw, fh = tam, 62
    lar = (fw - 16) / 24
    barras = ''.join(
        f'<rect class="hc-b t-{"no" if x["taxa"] >= 1.6 else ("wn" if x["taxa"] >= 1.1 else "ok")}"'
        f' style="--i:{x["h"]}" x="{8 + x["h"]*lar + 1.1:.1f}"'
        f' y="{fh - 18 - (6 + 30 * x["abertos"] / MX_H):.1f}" width="{lar - 2.2:.1f}"'
        f' height="{6 + 30 * x["abertos"] / MX_H:.1f}" rx="2.5">'
        f'<title>{x["h"]:02d}h · {mil(x["abertos"])} abertos · {pt(x["taxa"], 2)}% violaram</title>'
        f'</rect>' for x in HORAS)
    ax = 8 + 7 * lar + lar / 2
    marcas = ''.join(
        f'<text class="hc-x" x="{8 + hh*lar + lar/2:.1f}" y="{fh - 4}" text-anchor="middle">'
        f'{hh:02d}h</text>' for hh in (0, 6, 12, 18))
    return f'''<div class="hc">
      <svg class="hc-l" viewBox="0 0 {w:.0f} {h}">
        <path class="hl-bd" d="{bd}"/>
        <path class="hl-l" d="{suave(pr)}"/>
        <path class="hl-f" d="{suave(pf)}"/>
        <circle class="hl-o3" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="27"/>
        <circle class="hl-o2" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="18"/>
        <circle class="hl-o1" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="10"/>
        <circle class="hl-n" cx="{no[0]:.1f}" cy="{no[1]:.1f}" r="5.2"/>
        <text class="hl-x" x="18" y="{h - 6}">{dm(real['dia'].iloc[0])}</text>
        <text class="hl-x ag" x="{no[0]:.1f}" y="{h - 6}" text-anchor="middle">agora</text>
        <text class="hl-x" x="{w - 18:.0f}" y="{h - 6}" text-anchor="end">{dm(fut['dia'].iloc[-1])}</text>
      </svg>
      <div class="hc-v">
        <b>{pt(v, 0)}</b>
        <div class="hc-vt"><span class="hc-z z-{zona[0]}">{zona[1]}</span>
          <em>previstos hoje · faixa {pt(HOJE3['baixo'], 0)} a {pt(HOJE3['alto'], 0)}</em></div>
      </div>
      <div class="hc-f">
        <span class="hc-fl">as 24 horas de hoje</span>
        <svg viewBox="0 0 {fw} {fh}">
          <line class="hc-ag" x1="{ax:.1f}" y1="4" x2="{ax:.1f}" y2="{fh - 16}"/>
          {barras}{marcas}
          <circle class="hc-n" cx="{ax:.1f}" cy="4" r="3.4"/>
        </svg>
      </div>
    </div>'''


def trilho(w=1000, h=150):
    real = REAL3.tail(20).reset_index(drop=True)
    fut = FUT3.head(8).reset_index(drop=True)
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
        <path class="t-a" d="{area}" fill="url(#ga)"/>
        <path class="t-bd" d="{bd}"/>
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


def anel(fr, de, tom='no', tam=54):
    r = tam / 2 - 4
    ci = 2 * math.pi * r
    return (f'<svg class="anr t-{tom}" viewBox="0 0 {tam} {tam}" width="{tam}" height="{tam}">'
            f'<circle class="anr-t" cx="{tam/2}" cy="{tam/2}" r="{r}"/>'
            f'<circle class="anr-v" cx="{tam/2}" cy="{tam/2}" r="{r}" stroke-dasharray="{ci:.1f}"'
            f' stroke-dashoffset="{ci:.1f}" style="--f:{ci*(1-fr/de):.1f}"/>'
            f'<text x="{tam/2}" y="{tam/2+3.6}" text-anchor="middle">{fr}</text></svg>')


MOD_ATIVO = {a: {'nome': a, 'pass': int(r['passagens']), 'viol': int(r['violacoes']),
                 'taxa': pt(r['taxa'], 1), 'x': int(round(r['taxa'] / MEDIA_BASE)),
                 'hist': HIST_ATIVO.get(a, [])} for a, r in ATIVOS.iterrows()}
MOD_INC = {c['id']: {**{k: v for k, v in c.items() if k != 'taxa_ativo'},
                     'taxa_ativo': pt(c['taxa_ativo'], 1), 'sinais': SINAIS,
                     'em100': int(round(c['risco']))} for c in FILA}
MOD_PROD = {p: {'nome': p, 'nota': pt(saude.loc[p, 'nota']), 'pos': int(saude.loc[p, 'posicao']),
                'quad': saude.loc[p, 'quadrante'], 'inc': mil(saude.loc[p, 'incidentes']),
                'viol': int(saude.loc[p, 'violacoes']),
                'comp': [{'rot': rot, 'v': pt(saude.loc[p, k] * mult, 2 if mult == 100 else 1),
                          'u': u, 'pos': round(float(saude.loc[p, 'pos_' + k]) * 100)}
                         for k, rot, u, mult in COMPONENTES]} for p in saude.index}

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{--pg:#F6F7F9;--c:#FFF;--ink:#0C1017;--ln:rgba(12,16,23,.08);--ln2:rgba(12,16,23,.16);
 --tx:#4E586B;--tx2:#7B8598;--tx3:#A3ABBA;--hd:#0C1017;
 --ac:#2563EB;--acl:#EFF4FF;--no:#DC2626;--nol:#FEF2F2;--wn:#B45309;--wnl:#FFFAEC;
 --ok:#059669;--okl:#ECFDF5;
 --e:cubic-bezier(.19,1,.22,1);--e2:cubic-bezier(.34,1.56,.64,1);
 --s1:0 1px 2px rgba(12,16,23,.04),0 10px 26px -14px rgba(12,16,23,.14);
 --s2:0 2px 6px rgba(12,16,23,.06),0 28px 54px -20px rgba(12,16,23,.22)}
html{-webkit-font-smoothing:antialiased;scroll-behavior:smooth}
body{background:var(--pg);color:var(--hd);min-height:100dvh;overflow-x:hidden;
 font-family:'Outfit',system-ui,sans-serif;font-size:15px;letter-spacing:-.011em}
.id{font-weight:600;letter-spacing:.05em;font-variant-numeric:tabular-nums lining-nums}
.nb{font-variant-numeric:tabular-nums lining-nums}
.sh{position:relative;z-index:1;max-width:1420px;margin:0 auto;padding:0 32px 80px}
/* topo */
.tp{display:flex;align-items:center;gap:14px;padding:16px 0;margin-bottom:6px;
 position:sticky;top:0;z-index:30;
 background:linear-gradient(180deg,rgba(246,247,249,.97) 58%,transparent);backdrop-filter:blur(8px)}
.br{display:flex;align-items:center;gap:11px}
.br-m{width:34px;height:34px;border-radius:11px;background:var(--ink);display:grid;
 place-items:center;box-shadow:var(--s1)}
.br b{font-size:17px;font-weight:700;letter-spacing:-.04em;display:block;line-height:1}
.br em{font-size:8.5px;letter-spacing:.16em;color:var(--tx3);font-style:normal;font-weight:600}
.pil{display:flex;gap:2px;background:var(--c);border:1px solid var(--ln);border-radius:13px;
 padding:4px;box-shadow:var(--s1)}
.pil button{display:inline-flex;align-items:center;gap:7px;background:0;border:0;font:inherit;
 font-size:13px;font-weight:500;color:var(--tx2);padding:8px 14px;border-radius:9px;
 cursor:pointer;transition:all .34s var(--e);white-space:nowrap}
.pil button:hover:not(:disabled){color:var(--hd)}
.pil button.on{background:var(--ink);color:#fff}
.pil button:disabled{opacity:.35;cursor:default}
.tp-r{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.stl{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;color:var(--tx);
 background:var(--c);border:1px solid var(--ln);padding:7px 12px;border-radius:999px;
 box-shadow:var(--s1)}
.stl .ic{color:var(--tx3)}
.stl i{width:6px;height:6px;border-radius:50%;background:var(--ok);
 box-shadow:0 0 0 3px rgba(5,150,105,.16);animation:pu 2.6s ease-in-out infinite}
@keyframes pu{50%{opacity:.35}}
/* abas de dia, do app de clima */
.dias{display:flex;gap:6px;margin:18px 0 22px}
.da{background:var(--c);border:1px solid var(--ln);border-radius:15px;padding:11px 17px;
 cursor:pointer;font:inherit;text-align:left;transition:all .36s var(--e);box-shadow:var(--s1)}
.da em{display:block;font-size:9.5px;font-style:normal;letter-spacing:.12em;text-transform:uppercase;
 color:var(--tx3);font-weight:700}
.da b{display:block;font-size:17px;font-weight:650;letter-spacing:-.03em;margin-top:3px}
.da span{font-size:10.5px;color:var(--tx2)}
.da:hover{transform:translateY(-2px);box-shadow:var(--s2)}
.da.on{background:var(--ink);border-color:var(--ink)}
.da.on em{color:rgba(255,255,255,.5)}.da.on b{color:#fff}.da.on span{color:rgba(255,255,255,.62)}
/* hero editorial */
.hr{display:grid;grid-template-columns:1fr auto;gap:44px;align-items:center;margin-bottom:34px}
.hr .kk{font-size:10.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
 color:var(--ac);display:inline-flex;align-items:center;gap:8px}
.hr h1{font-size:47px;font-weight:600;line-height:1.09;letter-spacing:-.042em;margin-top:14px;
 max-width:20ch}
.hr h1 .mu{color:var(--tx3)}
.hr .lead{font-size:17px;color:var(--tx);line-height:1.62;margin-top:18px;max-width:60ch}
.hr .lead b{color:var(--hd);font-weight:650}
.hr .lead .cr{color:var(--no);font-weight:650}
/* chips de metrica */
.chips{display:flex;gap:9px;margin-top:22px;flex-wrap:wrap}
.ch{display:inline-flex;align-items:center;gap:10px;background:var(--c);border:1px solid var(--ln);
 border-radius:14px;padding:9px 14px 9px 10px;box-shadow:var(--s1);
 animation:sl .55s var(--e) both;animation-delay:calc(var(--i,0)*70ms)}
@keyframes sl{from{opacity:0;transform:translateY(9px)}}
.ch .chp{width:30px;height:30px;border-radius:9px}
.ch div em{display:block;font-size:9.5px;font-style:normal;letter-spacing:.09em;
 text-transform:uppercase;color:var(--tx3);font-weight:700}
.ch div b{display:block;font-size:15px;font-weight:650;letter-spacing:-.03em;margin-top:1px;
 font-variant-numeric:tabular-nums}
.ch div b u{font-size:10.5px;font-weight:500;color:var(--tx2);text-decoration:none;margin-left:2px}
/* relogio */
.rl{position:relative;width:340px;flex-shrink:0}
.rl svg{width:100%;height:auto;overflow:visible}
.rl-g{fill:none;stroke:var(--ln);stroke-width:1}
.rl-b{cursor:pointer;transform-origin:center;animation:rb .6s var(--e) both;
 animation-delay:calc(var(--i)*26ms);transition:filter .25s var(--e)}
@keyframes rb{from{opacity:0;transform:scale(.86)}to{opacity:1;transform:scale(1)}}
.rl-b.t-ok{fill:#BFD3FA}.rl-b.t-wn{fill:#F3C98A}.rl-b.t-no{fill:#EF8078}
.rl-b:hover{filter:brightness(.9)}
.rl-m{fill:none;stroke:var(--no);stroke-width:2.6;stroke-linecap:round;opacity:0;
 animation:fd .7s ease 1.1s forwards;--o:.85}
.rl-h{fill:var(--tx3);font-size:11px;font-weight:600;text-anchor:middle;
 font-family:'Outfit',sans-serif}
.rl-p{stroke:var(--ink);stroke-width:2;stroke-linecap:round;transform-origin:center;
 animation:gi 1.2s var(--e) .5s both}
@keyframes gi{from{transform:rotate(-120deg)}to{transform:rotate(0)}}
.rl-c{fill:var(--ink)}
.rl-ag{fill:var(--ink);font-size:10px;font-weight:700;text-anchor:middle;
 letter-spacing:.08em;text-transform:uppercase;font-family:'Outfit',sans-serif}
.rl-in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
 justify-content:center;pointer-events:none;text-align:center}
.rl-in b{font-size:46px;font-weight:650;letter-spacing:-.05em;line-height:1}
.rl-in span{font-size:11px;color:var(--tx2);margin-top:3px}
.rl-in em{font-size:10px;color:var(--tx3);font-style:normal;margin-top:2px}
/* atos */
.ato{display:flex;align-items:flex-start;gap:15px;margin:42px 0 16px}
.ato-n{font-size:11px;font-weight:800;letter-spacing:.1em;color:var(--ac);background:var(--acl);
 border:1px solid rgba(37,99,235,.18);border-radius:9px;padding:5px 10px;flex-shrink:0;margin-top:3px}
.ato h2{font-size:22px;font-weight:650;letter-spacing:-.033em}
.ato p{font-size:13.5px;color:var(--tx2);margin-top:2px}
/* cards */
.gr{display:grid;gap:16px;align-items:stretch}
.g2{grid-template-columns:1.5fr 1fr}
.g3{grid-template-columns:1fr 1fr 1fr}
.cd{display:flex;flex-direction:column;background:var(--c);border:1px solid var(--ln);
 border-radius:22px;padding:20px 22px;box-shadow:var(--s1);position:relative;overflow:hidden;
 transition:box-shadow .5s var(--e),transform .5s var(--e)}
.cd:hover{box-shadow:var(--s2);transform:translateY(-2px)}
.cd>.nt{margin-top:auto}
/* o card escuro no meio dos claros, de plataforma-card-escuro-meta */
.cd.dk{background:var(--ink);border-color:var(--ink);color:#E8ECF3}
.cd.dk .hdr h3{color:#fff}.cd.dk .hdr p{color:#8D97A8}.cd.dk .hdr .ic{color:#6EA0FF}
.cd.dk .nt{color:#8D97A8;border-color:rgba(255,255,255,.1)}.cd.dk .nt b{color:#fff}
.hdr{display:flex;align-items:flex-start;gap:13px;margin-bottom:15px}
.hdr-t{display:flex;gap:10px;flex:1;min-width:0}
.hdr-t .ic{color:var(--ac);margin-top:2px;flex-shrink:0}
.hdr h3{font-size:14.5px;font-weight:650;letter-spacing:-.022em}
.hdr p{font-size:11.5px;color:var(--tx2);margin-top:2px;line-height:1.45}
.fg{display:flex;gap:2px;background:var(--pg);border:1px solid var(--ln);border-radius:10px;
 padding:3px;flex-shrink:0}
.fb{background:0;border:0;font:inherit;font-size:11px;font-weight:600;color:var(--tx2);
 padding:5px 10px;border-radius:7px;cursor:pointer;transition:all .3s var(--e);white-space:nowrap}
.fb:hover{color:var(--hd)}.fb.on{background:var(--c);color:var(--hd);box-shadow:var(--s1)}
.vr{font-size:10.5px;font-weight:700;padding:3px 7px;border-radius:6px;margin-left:6px}
.vr.ok{background:var(--okl);color:var(--ok)}.vr.no{background:var(--nol);color:var(--no)}
/* trilho */
.tr{position:relative;margin-top:8px}
.tr svg{width:100%;height:150px;display:block;overflow:visible}
.t-l{fill:none;stroke:var(--ac);stroke-width:2.4;stroke-linecap:round;stroke-dasharray:1600;
 stroke-dashoffset:1600;animation:dw 1.8s var(--e) .3s forwards}
.t-f{fill:none;stroke:var(--ac);stroke-width:2;stroke-dasharray:5 5;opacity:0;
 animation:fd .8s ease 1.6s forwards;--o:.8}
.t-bd{fill:var(--ac);opacity:0;animation:fd 1s ease 1.7s forwards;--o:.12}
.t-a{opacity:0;animation:fd 1s ease 1.2s forwards;--o:1}
.t-ag{stroke:var(--ln2);stroke-width:1;stroke-dasharray:2 4;opacity:0;
 animation:fd .5s ease 1.5s forwards;--o:1}
.t-n{fill:var(--ac);opacity:0;animation:pn .5s var(--e2) 1.4s forwards}
.t-h{fill:var(--ac);opacity:0;transform-box:fill-box;transform-origin:center;
 animation:hl 3s ease-out 2.1s infinite}
@keyframes hl{0%{opacity:.28;transform:scale(.3)}70%,100%{opacity:0;transform:scale(1.7)}}
@keyframes dw{to{stroke-dashoffset:0}}
@keyframes fd{to{opacity:var(--o,1)}}
@keyframes pn{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
.anp{position:absolute;transform:translateX(-50%);background:var(--acl);
 border:1px solid rgba(37,99,235,.22);color:var(--ac);padding:4px 9px;border-radius:8px;
 font-size:11px;font-weight:650;white-space:nowrap;opacity:0;
 animation:fd .6s ease 2s forwards}
.tr-x{display:flex;justify-content:space-between;font-size:9.5px;color:var(--tx3);
 letter-spacing:.09em;text-transform:uppercase;position:relative;margin-top:2px}
.tr-x .ag{position:absolute;transform:translateX(-50%);color:var(--ac);font-weight:700}
/* linha de metrica */
.ml{display:flex;flex-direction:column;gap:8px}
.mr{display:flex;align-items:center;gap:12px;background:var(--pg);border:1px solid var(--ln);
 border-radius:14px;padding:11px 13px;animation:sl .5s var(--e) both;
 animation-delay:calc(120ms + var(--i,0)*60ms)}
.mr-t{flex:1;min-width:0}
.mr-t b{font-size:13px;font-weight:500;display:block}
.mr-t span{font-size:11px;color:var(--tx2);display:block;margin-top:1px}
.mr-v{font-size:20px;font-weight:650;letter-spacing:-.035em;flex-shrink:0;
 font-variant-numeric:tabular-nums;display:inline-flex;align-items:baseline}
.mr-v u{font-size:11.5px;font-weight:500;color:var(--tx2);text-decoration:none;margin-left:3px}
.mr-v.no{color:var(--no)}.mr-v.ok{color:var(--ok)}
/* circulos por dia */
.dcs{display:flex;gap:6px}
.dc{flex:1;display:flex;flex-direction:column;align-items:center;gap:5px}
.dc i{width:100%;aspect-ratio:1;max-width:38px;border-radius:50%;border:1.5px solid var(--ln2);
 display:grid;place-items:center;font-style:normal;font-size:12px;font-weight:650;
 color:var(--tx3);animation:pn .4s var(--e2) both;animation-delay:calc(var(--i,0)*45ms)}
.dc.vi i{background:var(--nol);border-color:rgba(220,38,38,.42);color:var(--no)}
.dc span{font-size:9.5px;color:var(--tx2)}
.dc em{font-size:9.5px;font-style:normal;color:var(--tx3);font-variant-numeric:tabular-nums}
/* fila */
.fl{display:flex;flex-direction:column;gap:8px}
.it{display:flex;align-items:center;gap:12px;background:var(--pg);border:1px solid var(--ln);
 border-radius:15px;padding:11px 13px;cursor:pointer;transition:all .34s var(--e);width:100%;
 font:inherit;color:inherit;text-align:left;animation:sl .5s var(--e) both;
 animation-delay:calc(140ms + var(--i)*58ms)}
.it:hover{background:var(--c);border-color:var(--ln2);box-shadow:var(--s1);transform:translateX(4px)}
.it-r{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;flex-shrink:0;
 font-size:13.5px;font-weight:700;letter-spacing:-.03em}
.it-r.crit{background:var(--nol);color:var(--no)}.it-r.alta{background:var(--wnl);color:var(--wn)}
.it-t{flex:1;min-width:0}
.it-t b{font-size:13.5px;display:block}
.it-t span{font-size:11.5px;color:var(--tx2);margin-top:2px;display:flex;gap:4px;flex-wrap:wrap;
 align-items:center}
.it-t span .ic{width:12px;height:12px;opacity:.5}
.it-t span u{text-decoration:none;margin-right:7px;display:inline-flex;align-items:center;gap:4px}
.it-b{flex-shrink:0;text-align:right}
.it-b em{font-size:9.5px;font-style:normal;color:var(--tx3);letter-spacing:.07em;
 text-transform:uppercase;display:block}
.it-b b{font-size:12.5px;color:var(--tx);font-weight:600}
.it .sq{color:var(--tx3);transition:transform .3s var(--e),color .3s var(--e)}
.it:hover .sq{color:var(--ac);transform:translateX(3px)}
/* meta no card escuro */
.mt{margin-top:16px}
.mt-h{display:flex;align-items:baseline;gap:9px}
.mt-p{font-size:10.5px;font-weight:700;letter-spacing:.1em;color:#8D97A8}
.mt-v{font-size:29px;font-weight:650;letter-spacing:-.04em;font-variant-numeric:tabular-nums}
.mt-v.ok{color:#37D39B}.mt-v.no{color:#FF7D74}
.mt-l{font-size:12px;color:#8D97A8}
.tg{font-size:9.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;
 border-radius:6px;margin-left:auto}
.tg.ok{background:rgba(55,211,155,.16);color:#37D39B}
.tg.no{background:rgba(255,125,116,.16);color:#FF7D74}
.mt-b{height:13px;border-radius:7px;background:rgba(255,255,255,.09);position:relative;
 margin-top:11px}
.mt-b s{position:absolute;top:0;bottom:0;border-radius:7px;text-decoration:none;
 transform:scaleX(0);transform-origin:left;animation:ab 1s var(--e) .6s forwards}
.mt-b s.ok{background:linear-gradient(90deg,rgba(55,211,155,.4),rgba(55,211,155,.75))}
.mt-b s.no{background:linear-gradient(90deg,rgba(255,125,116,.4),rgba(255,125,116,.75))}
.mt-b i{position:absolute;top:-3px;bottom:-3px;width:3px;border-radius:2px;opacity:0;
 animation:fd .5s ease 1.4s forwards}
.mt-b i.ok{background:#37D39B}.mt-b i.no{background:#FF7D74}
.mt-b u{position:absolute;top:-5px;bottom:-5px;width:2px;background:#fff;opacity:0;
 animation:fd .5s ease 1.2s forwards;--o:.85}
@keyframes ab{to{transform:scaleX(1)}}
.mt-f{font-size:10.5px;color:#8D97A8;margin-top:7px}
/* ranking */
.rw{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid var(--ln);
 cursor:pointer;background:0;border-left:0;border-right:0;border-top:0;width:100%;font:inherit;
 color:inherit;text-align:left;transition:padding .3s var(--e)}
.rw:hover{padding-left:5px}.rw:last-of-type{border-bottom:0}
.rw-p{width:46px;font-weight:650;font-size:12.5px}
.rw-b{flex:1;height:6px;border-radius:3px;background:#EDEFF3;overflow:hidden}
.rw-b i{display:block;height:100%;border-radius:3px;width:0;background:var(--c2);
 animation:gw 1s var(--e) both;animation-delay:calc(400ms + var(--i)*70ms)}
@keyframes gw{to{width:var(--w)}}
.rw-v{width:36px;text-align:right;font-size:13px;font-weight:650;
 font-variant-numeric:tabular-nums}
.rw-q{width:88px;font-size:10px;color:var(--tx3);text-align:right}
.nt{font-size:11.5px;color:var(--tx2);line-height:1.62;margin-top:14px;padding-top:12px;
 border-top:1px solid var(--ln)}
.nt b{color:var(--hd);font-weight:650}
.anr .anr-t{fill:none;stroke:#EDEFF3;stroke-width:4}
.anr .anr-v{fill:none;stroke-width:4;stroke-linecap:round;transform:rotate(-90deg);
 transform-origin:center;animation:ar 1.1s var(--e) .5s forwards}
.anr.t-no .anr-v{stroke:var(--no)}.anr.t-wn .anr-v{stroke:var(--wn)}
.anr text{fill:var(--hd);font-size:15px;font-weight:650;font-family:'Outfit',sans-serif}
@keyframes ar{to{stroke-dashoffset:var(--f)}}
/* modal */
.ov{position:fixed;inset:0;z-index:90;display:grid;place-items:center;padding:28px;
 background:rgba(12,16,23,.42);backdrop-filter:blur(8px);animation:fd .3s ease both;--o:1}
.ov[hidden]{display:none}
.md{width:min(620px,100%);max-height:86dvh;overflow:auto;position:relative;background:var(--c);
 border-radius:26px;padding:26px 28px;box-shadow:0 40px 90px -26px rgba(12,16,23,.4);
 animation:mu .5s var(--e) both}
@keyframes mu{from{opacity:0;transform:translateY(18px) scale(.976)}}
.md-x{position:absolute;top:18px;right:18px;width:32px;height:32px;border-radius:10px;
 background:var(--pg);border:1px solid var(--ln);color:var(--tx);cursor:pointer;display:grid;
 place-items:center;transition:all .3s var(--e)}
.md-x:hover{background:#E9ECF1;color:var(--hd)}
.md-k{font-size:9.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--ac)}
.md h3{font-size:26px;font-weight:650;letter-spacing:-.035em;margin-top:7px}
.md .sub{font-size:13px;color:var(--tx);margin-top:5px}
.md-g{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:20px}
.md-s{background:var(--pg);border:1px solid var(--ln);border-radius:14px;padding:13px 14px}
.md-s em{font-size:9.5px;font-style:normal;letter-spacing:.1em;text-transform:uppercase;
 color:var(--tx3);display:block;font-weight:700}
.md-s b{font-size:23px;font-weight:650;letter-spacing:-.04em;display:block;margin-top:5px;
 line-height:1}
.md-s.no b{color:var(--no)}.md-s.ok b{color:var(--ok)}.md-s.wn b{color:var(--wn)}
.md-h{font-size:10px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--tx3);
 margin:22px 0 11px;display:flex;align-items:center;gap:8px}
.md-h::after{content:'';flex:1;height:1px;background:var(--ln)}
.hb{display:flex;align-items:flex-end;gap:5px;height:74px}
.hb-c{flex:1;display:flex;flex-direction:column;align-items:center;gap:5px;height:100%;
 justify-content:flex-end}
.hb-c i{width:100%;border-radius:5px 5px 2px 2px;background:#E4E8EE;position:relative;
 height:var(--h)}
.hb-c i u{position:absolute;inset:auto 0 0 0;height:var(--v);border-radius:0 0 2px 2px;
 background:var(--no);text-decoration:none}
.hb-c span{font-size:9.5px;color:var(--tx3)}
.sg{display:flex;align-items:center;gap:11px;padding:8px 0}
.sg-t{flex:1;font-size:12.5px}
.sg-b{width:130px;height:6px;border-radius:3px;background:#EDEFF3;overflow:hidden}
.sg-b i{display:block;height:100%;border-radius:3px;background:linear-gradient(90deg,#7DA8FF,#2563EB)}
.sg-v{width:34px;text-align:right;font-size:12.5px;font-weight:650;
 font-variant-numeric:tabular-nums}
.cx{background:var(--acl);border:1px solid rgba(37,99,235,.16);border-radius:15px;padding:14px 16px;
 margin-top:18px;display:flex;gap:12px}
.cx p{font-size:12.5px;color:var(--tx);line-height:1.6}.cx p b{color:var(--hd);font-weight:650}
.md-f{margin-top:20px;padding-top:15px;border-top:1px solid var(--ln);display:flex;gap:9px;
 flex-wrap:wrap}
.bt{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:12.5px;font-weight:600;
 padding:10px 15px;border-radius:11px;cursor:pointer;transition:all .3s var(--e)}
.bt.pr{background:var(--ink);border:1px solid var(--ink);color:#fff}
.bt.pr:hover{transform:translateY(-1px);box-shadow:var(--s2)}
.bt.sc{background:var(--c);border:1px solid var(--ln);color:var(--tx)}
.bt.sc:hover{background:var(--pg);color:var(--hd)}
.bt:active{transform:scale(.98)}

/* B1 · a marca virada heroi */
.hl{position:relative;width:360px;flex-shrink:0}
.hl svg{width:100%;height:auto;overflow:visible}
.hl-l{fill:none;stroke:var(--ac);stroke-width:4.2;stroke-linecap:round;stroke-linejoin:round;
 stroke-dasharray:900;stroke-dashoffset:900;animation:dw 1.9s var(--e) .3s forwards}
.hl-f{fill:none;stroke:var(--ac);stroke-width:3;stroke-linecap:round;stroke-dasharray:7 7;
 opacity:0;animation:fd .9s ease 1.7s forwards;--o:.55}
.hl-bd{fill:var(--ac);opacity:0;animation:fd 1s ease 1.8s forwards;--o:.11}
.hl-n{fill:var(--ac);opacity:0;animation:pn .5s var(--e2) 1.6s forwards}
.hl-o1{fill:none;stroke:var(--ac);stroke-width:2;opacity:0;
 animation:fd .5s ease 1.8s forwards;--o:.45}
.hl-o2,.hl-o3{fill:var(--ac);opacity:0;transform-box:fill-box;transform-origin:center}
.hl-o2{animation:on 3.2s ease-out 2s infinite}
.hl-o3{animation:on 3.2s ease-out 2.5s infinite}
@keyframes on{0%{opacity:.22;transform:scale(.45)}70%,100%{opacity:0;transform:scale(1.5)}}
.hl-x{fill:var(--tx3);font-size:10px;font-weight:600;letter-spacing:.08em;
 text-transform:uppercase;font-family:'Outfit',sans-serif}
.hl-x.ag{fill:var(--ac);font-weight:700}
.hl-v{text-align:center;margin-top:-4px}
.hl-v b{font-size:54px;font-weight:700;letter-spacing:-.05em;line-height:1;display:block}
.hl-v span{font-size:11.5px;color:var(--tx2);display:block;margin-top:6px}
/* B2 · o dia esticado */
.hf{width:360px;flex-shrink:0}
.hf svg{width:100%;height:auto;overflow:visible}
.hf-b{transform-origin:bottom;animation:hb .55s var(--e) both;
 animation-delay:calc(var(--i)*24ms);cursor:pointer;transition:filter .25s var(--e)}
@keyframes hb{from{opacity:0;transform:scaleY(.2)}}
.hf-b:hover{filter:brightness(.88)}
.hf-b.t-ok{fill:#B9CFFA}.hf-b.t-wn{fill:#F2C486}.hf-b.t-no{fill:#EE7C74}
.hf-ag{stroke:var(--ink);stroke-width:1.4;stroke-dasharray:3 3;opacity:0;
 animation:fd .5s ease .9s forwards;--o:.5}
.hf-n{fill:var(--ink);opacity:0;animation:pn .4s var(--e2) 1s forwards}
.hf-al{fill:var(--ink);font-size:9.5px;font-weight:700;letter-spacing:.09em;
 text-transform:uppercase;font-family:'Outfit',sans-serif;opacity:0;
 animation:fd .5s ease 1.1s forwards;--o:1}
.hf-x{fill:var(--tx3);font-size:9.5px;font-weight:600;font-family:'Outfit',sans-serif}
.hf-l{display:flex;gap:13px;justify-content:center;margin-top:4px;flex-wrap:wrap}
.hf-l span{display:inline-flex;align-items:center;gap:5px;font-size:10px;color:var(--tx2)}
.hf-l i{width:9px;height:9px;border-radius:3px}
.hf-l i.t-ok{background:#B9CFFA}.hf-l i.t-wn{background:#F2C486}.hf-l i.t-no{background:#EE7C74}
.hf-v{text-align:center;margin-top:14px}
.hf-v b{font-size:48px;font-weight:700;letter-spacing:-.05em;line-height:1;display:block}
.hf-v span{font-size:11.5px;color:var(--tx2);display:block;margin-top:5px}
/* B3 · o veredito */
.mdd{position:relative;width:340px;flex-shrink:0}
.mdd svg{width:100%;height:auto;overflow:visible}
.md-z{fill:none;stroke-width:16;stroke-linecap:butt;opacity:.22}
.md-z.z-ok{stroke:var(--ok)}.md-z.z-ac{stroke:var(--ac)}.md-z.z-no{stroke:var(--no)}
.md-fx{fill:none;stroke:var(--ac);stroke-width:16;stroke-linecap:round;opacity:0;
 animation:fd .9s ease .7s forwards;--o:.8}
.md-p{stroke:var(--ink);stroke-width:3.2;stroke-linecap:round;transform-origin:center;
 animation:gi 1.3s var(--e) .4s both}
@keyframes gi{from{transform:rotate(-42deg)}to{transform:rotate(0)}}
.md-c{fill:var(--ink);opacity:0;animation:pn .5s var(--e2) 1.3s forwards}
.md-md{stroke:var(--tx3);stroke-width:1.4;stroke-dasharray:2 2}
.md-ml{fill:var(--tx3);font-size:9.5px;font-weight:600;font-family:'Outfit',sans-serif}
.mdd-in{text-align:center;margin-top:-62px}
.mdd-in b{font-size:58px;font-weight:700;letter-spacing:-.055em;line-height:1;display:block}
.mdd-z{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.08em;
 text-transform:uppercase;padding:4px 12px;border-radius:8px;margin-top:10px}
.mdd-z.z-ok{background:var(--okl);color:var(--ok)}
.mdd-z.z-ac{background:var(--acl);color:var(--ac)}
.mdd-z.z-no{background:var(--nol);color:var(--no)}
.mdd-in em{display:block;font-size:10.5px;color:var(--tx3);font-style:normal;margin-top:9px;
 max-width:32ch;margin-inline:auto;line-height:1.55}
@media (max-width:1100px){.hl,.hf,.mdd{width:100%;max-width:360px}}
@media (prefers-reduced-motion:reduce){
 .hl-l{stroke-dashoffset:0!important}
 .hl-f,.hl-bd,.hl-n,.hl-o1,.hf-ag,.hf-n,.hf-al,.md-fx,.md-c{opacity:1!important}
 .hl-bd{opacity:.11!important}.hl-o2,.hl-o3{opacity:0!important}
 .hf-b{opacity:1!important;transform:none!important}.md-p{transform:none!important}}

/* B1 completa · tres escalas de tempo empilhadas */
.hc{width:380px;flex-shrink:0}
.hc svg{width:100%;height:auto;overflow:visible;display:block}
.hc-v{display:flex;align-items:center;gap:14px;justify-content:center;margin-top:2px}
.hc-v b{font-size:58px;font-weight:700;letter-spacing:-.055em;line-height:.9}
.hc-vt{text-align:left}
.hc-z{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;
 text-transform:uppercase;padding:4px 11px;border-radius:8px}
.hc-z.z-ok{background:var(--okl);color:var(--ok)}
.hc-z.z-ac{background:var(--acl);color:var(--ac)}
.hc-z.z-no{background:var(--nol);color:var(--no)}
.hc-vt em{display:block;font-size:10.5px;color:var(--tx3);font-style:normal;margin-top:5px;
 line-height:1.45;max-width:22ch}
.hc-f{margin-top:14px;padding-top:13px;border-top:1px solid var(--ln);position:relative}
.hc-fl{position:absolute;top:-7px;left:50%;transform:translateX(-50%);background:var(--pg);
 padding:0 9px;font-size:9px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
 color:var(--tx3)}
.hc-b{transform-origin:bottom;animation:hb .5s var(--e) both;
 animation-delay:calc(1.9s + var(--i)*20ms);cursor:pointer;transition:filter .25s var(--e)}
@keyframes hb{from{opacity:0;transform:scaleY(.15)}}
.hc-b:hover{filter:brightness(.86)}
.hc-b.t-ok{fill:#BCD1FA}.hc-b.t-wn{fill:#F2C486}.hc-b.t-no{fill:#EE7C74}
.hc-ag{stroke:var(--ink);stroke-width:1.3;stroke-dasharray:2 3;opacity:0;
 animation:fd .5s ease 2.3s forwards;--o:.5}
.hc-n{fill:var(--ink);opacity:0;animation:pn .4s var(--e2) 2.4s forwards}
.hc-x{fill:var(--tx3);font-size:9px;font-weight:600;font-family:'Outfit',sans-serif}
@media (max-width:1100px){.hc{width:100%;max-width:380px}}
@media (prefers-reduced-motion:reduce){
 .hc-b{opacity:1!important;transform:none!important}.hc-ag,.hc-n{opacity:1!important}}
@media (max-width:1100px){.hr,.g2,.g3{grid-template-columns:1fr}.rl{width:100%;max-width:340px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}
 .t-l{stroke-dashoffset:0!important}
 .t-f,.t-bd,.t-a,.t-ag,.t-n,.anp,.rl-m{opacity:1!important}.t-bd{opacity:.12!important}
 .t-h{opacity:0!important}.rw-b i{width:var(--w)!important}
 .it,.mr,.dc i,.ch,.rl-b{opacity:1!important;transform:none!important}
 .mt-b s{transform:none!important}.mt-b i,.mt-b u{opacity:1!important}
 .anr .anr-v{stroke-dashoffset:var(--f)!important}}
"""


def cab(icone, titulo, oque, extra=''):
    return f'''<div class="hdr"><div class="hdr-t">{ico(icone, 16)}
      <div><h3>{titulo}</h3><p>{oque}</p></div></div>{extra}</div>'''


def filtros(nome, opcoes, ativo=0):
    return ('<div class="fg">' + ''.join(
        f'<button class="fb{" on" if i == ativo else ""}" data-g="{nome}" data-v="{v}">{r}</button>'
        for i, (v, r) in enumerate(opcoes)) + '</div>')


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


def pagina(heroi, titulo):
    return f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cronos · {titulo}</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}{CSS_ICO_CLARO}{CSS_CAMPO}</style></head><body>
{campo('#2563EB', .13)}
<div class="sh">
  <div class="tp">
    <div class="br"><div class="br-m"><svg viewBox="0 0 28 28" width="18" height="18" fill="none">
      <path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="2.6" stroke-linecap="round"
        stroke-linejoin="round"/><circle cx="22" cy="8" r="3" stroke="#6EA0FF" stroke-width="1.9"/>
      <circle cx="22" cy="8" r="1.3" fill="#6EA0FF"/></svg></div>
      <div><b>Cronos</b><em>VEJA ANTES · AJA ANTES</em></div></div>
    <div class="pil">
      <button class="on">{ico('agora', 15)}Hoje</button>
      <button>{ico('fila', 15)}Fila</button>
      <button>{ico('coracao', 15)}Saúde</button>
      <button>{ico('lupa', 15)}Causas</button>
      <button disabled>{ico('previsao', 15)}Volume</button></div>
    <div class="tp-r"><span class="stl"><i></i>carga de {dm(ONTEM['dia'])} · 23h59</span></div>
  </div>

  <div class="dias">
    <button class="da"><em>ontem</em><b>{ONTEM_TOTAL}</b><span>entraram · {ONTEM_VIOL} violaram</span></button>
    <button class="da on"><em>hoje · {dm(DIA_HOJE)}</em><b>{pt(HOJE3['valor'], 0)}</b>
      <span>previstos no P3</span></button>
    {"".join(f'''<button class="da"><em>{LBL_DIA[r['dia'].dayofweek]} · {dm(r['dia'])}</em>
      <b>{pt(r['valor'], 0)}</b><span>{pt(r['baixo'], 0)} a {pt(r['alto'], 0)}</span></button>'''
      for _, r in FUT3.iloc[1:5].iterrows())}
  </div>

  <div class="hr">
    <div>
      <span class="kk">{ico('agora', 14)}{DIA_HOJE.day:02d}/{DIA_HOJE.month:02d}/{DIA_HOJE.year} · 07h00</span>
      <h1>Dia de volume normal,<br><span class="mu">com risco concentrado.</span></h1>
      <p class="lead">Devem entrar cerca de <b>{pt(HOJE3['valor'], 0)} incidentes elegíveis</b> no
        P3 e <b>{pt(HOJE2['valor'], 0)}</b> no P2 — dentro do padrão de uma quarta-feira. O que
        pede atenção não é o volume: <span class="cr">cinco dos seis casos mais arriscados da fila
        estão no mesmo ativo</span>, o <b class="id">{topo['ativo']}</b>.</p>
      <div class="chips">
        <div class="ch" style="--i:0">{chip('entrada', 'ac', 16)}
          <div><em>ontem</em><b>{ONTEM_TOTAL}<u>elegíveis</u></b></div></div>
        <div class="ch" style="--i:1">{chip('escudo_ok', 'ok', 16)}
          <div><em>sem violar</em><b>{SEM_VIOL}<u>dias úteis</u></b></div></div>
        <div class="ch" style="--i:2">{chip('fila', 'nt', 16)}
          <div><em>em atendimento</em><b>{mil(EM_ABERTO)}</b></div></div>
        <div class="ch" style="--i:3">{chip('alerta', 'no', 16)}
          <div><em>risco acima de 10%</em><b>4<u>casos</u></b></div></div>
      </div>
    </div>
    {heroi}
  </div>

  <div class="ato"><span class="ato-n">01</span>
    <div><h2>Como o dia se distribui</h2>
      <p>Em que horas o trabalho entra, e em que horas o prazo costuma estourar.</p></div></div>
  <div class="gr g2">
    <div class="cd">
      {cab('previsao', 'O que já entrou e o que vem',
           'A linha cheia é o volume medido. A pontilhada é a previsão, e a área em volta é a '
           'margem de erro do modelo.',
           filtros('per', [('20', '20 dias'), ('45', '45 dias')]))}
      {trilho()}
      <div class="nt">Ontem entraram <b>{ONTEM_TOTAL}</b> contra <b>{pt(BASE_20, 0)}</b> de média
        dos últimos vinte dias úteis. Volume serve para dimensionar a equipe do dia — não diz onde
        o prazo vai estourar.</div>
    </div>
    <div class="cd">
      {cab('relogio', 'A hora importa mais que o volume',
           'O relógio ao lado mostra as duas coisas: o tamanho da fatia é quanto entra, a cor é '
           'quanto viola.')}
      <div class="ml">
        <div class="mr" style="--i:0">{chip('tendencia', 'ac')}
          <div class="mr-t"><b>Hora de maior movimento</b>
            <span>{mil(HORA_PICO['abertos'])} incidentes abertos no ano</span></div>
          <span class="mr-v">{HORA_PICO['h']:02d}<u>h</u></span></div>
        <div class="mr" style="--i:1">{chip('alerta', 'no')}
          <div class="mr-t"><b>Hora de maior taxa de violação</b>
            <span>{pt(HORA_RISCO['taxa'], 2)}% dos {mil(HORA_RISCO['abertos'])} abertos nessa hora</span></div>
          <span class="mr-v no">{HORA_RISCO['h']:02d}<u>h</u></span></div>
        <div class="mr" style="--i:2">{chip('balanca', 'nt')}
          <div class="mr-t"><b>Taxa média da base</b>
            <span>referência para ler qualquer número desta tela</span></div>
          <span class="mr-v">{pt(MEDIA_BASE, 2)}<u>%</u></span></div>
      </div>
      <div class="nt">A madrugada tem pouco volume e a <b>maior taxa do dia</b>: às
        {HORA_RISCO['h']:02d}h a chance de estourar é <b>{pt(HORA_RISCO['taxa']/MEDIA_BASE, 1)}
        vezes</b> a média. É um dos sinais que o modelo usa.</div>
    </div>
  </div>

  <div class="ato"><span class="ato-n">02</span>
    <div><h2>O que fazer hoje</h2>
      <p>Os casos abertos com maior chance de estourar o prazo, na ordem em que valem atenção.</p></div></div>
  <div class="gr g2">
    <div class="cd">
      {cab('fila', 'Fila de risco',
           'Ordenada pela chance de estourar o prazo. Clique em qualquer linha para ver por que '
           'o modelo pontuou assim.',
           filtros('pri', [('t', 'todas'), ('2', 'P2'), ('3', 'P3')]))}
      <div class="fl">
        {"".join(f"""<button class="it" style="--i:{j}" data-mod="inc" data-k="{c['id']}">
          <span class="it-r {'crit' if c['risco'] >= 40 else 'alta'}">{pt(c['risco'], 0)}%</span>
          <span class="it-t"><b class="id">{c['id']}</b>
            <span><u>{ico('produto', 12)}{c['produto']}</u><u>{ico('pessoas', 12)}{c['equipe']}</u>
              <u>{ico('ativo', 12)}<span class="id">{c['ativo']}</span></u></span></span>
          <span class="it-b"><em>no ativo</em><b>{c['viol']}/{c['pass']}</b></span>
          <span class="sq">{ico('seta', 15)}</span></button>""" for j, c in enumerate(FILA))}
      </div>
      <div class="nt">A média da base é <b>{pt(MEDIA_BASE, 2)}%</b>, então um caso de 40% é
        <b>quarenta vezes</b> mais provável que o incidente comum. Nos cinquenta primeiros da fila
        estão <b>15 das 50</b> violações do período.</div>
    </div>
    <div class="cd">
      {cab('prazo', 'Os últimos dez dias úteis',
           'Círculo vazio é dia que fechou sem violação nenhuma. Cheio mostra quantas houve.')}
      <div class="dcs">{"".join(f"""<div class="dc{' vi' if v else ''}"><i>{v if v else ''}</i>
        <span>{LBL_DIA[d.dayofweek]}</span><em>{d.day:02d}/{d.month:02d}</em></div>"""
        for d, v in ULTIMOS_DIAS)}</div>
      <div class="ml" style="margin-top:16px">
        <div class="mr" style="--i:0">{chip('escudo_ok', 'ok')}
          <div class="mr-t"><b>Dias úteis seguidos sem violação</b>
            <span>contando de {dm(DIA_HOJE)} para trás</span></div>
          <span class="mr-v ok">{SEM_VIOL}<u>dias</u></span></div>
        <div class="mr" style="--i:1">{chip('balanca', 'nt')}
          <div class="mr-t"><b>Taxa dos últimos trinta dias</b>
            <span>{VIOL_30} violações em {mil(ELEG_30)} elegíveis</span></div>
          <span class="mr-v">{pt(TAXA_30, 2)}<u>%</u>
            <span class="vr ok">−{pt(abs(DELTA_TAXA), 0)}%</span></span></div>
      </div>
    </div>
  </div>

  <div class="ato"><span class="ato-n">03</span>
    <div><h2>Para onde o ano vai</h2>
      <p>Se nada mudar, onde o KPI fecha em dezembro e quais produtos puxam para baixo.</p></div></div>
  <div class="gr g2">
    <div class="cd dk">
      {cab('alvo', 'Fechamento contra a meta',
           'Soma o que já fechou, o risco da fila aberta e o volume que ainda entra no ano.')}
      {meta('P2')}{meta('P3')}
      <div class="nt">Em três das dez projeções testadas o traço cruzaria a meta sem que o ano
        cruzasse. Por isso a faixa aparece junto: ela é a parte honesta da previsão.</div>
    </div>
    <div class="cd">
      {cab('coracao', 'Produtos com pior nota',
           'Nota de 0 a 100 por posição relativa entre os 17 produtos. Clique para abrir os cinco '
           'componentes.')}
      <div>
        {"".join(f"""<button class="rw" style="--i:{j}" data-mod="prod" data-k="{x}">
          <span class="rw-p id">{x}</span>
          <span class="rw-b"><i style="--w:{saude.loc[x,'nota']:.0f}%;--c2:{'#DC2626' if saude.loc[x,'nota']<40 else '#B45309'}"></i></span>
          <span class="rw-v">{pt(saude.loc[x,'nota'])}</span>
          <span class="rw-q">{pt(saude.loc[x,'taxa_violacao']*100, 2)}% violação</span>
          <span class="sq">{ico('seta', 14)}</span></button>"""
          for j, x in enumerate(saude.index[-5:][::-1]))}
      </div>
      <div class="nt"><b>100 é o melhor dos dezessete</b>, não um produto sem problema. O pior é
        <b class="id">{pior}</b>, com <b>{pt(saude.loc[pior,'prop_inedito']*100, 0)}%</b> de
        problemas inéditos — e o inédito viola <b>4,6 vezes mais</b>.</div>
    </div>
  </div>
</div>

<div class="ov" id="ov" hidden><div class="md" role="dialog" aria-modal="true">
  <button class="md-x" id="mx" aria-label="fechar">{ico('fechar', 16)}</button>
  <div id="mc"></div></div></div>

<script>
const ATIVO={json.dumps(MOD_ATIVO, ensure_ascii=False)},
      INC={json.dumps(MOD_INC, ensure_ascii=False)},
      PROD={json.dumps(MOD_PROD, ensure_ascii=False)},
      MES={json.dumps(MES_LBL, ensure_ascii=False)},MEDIA={MEDIA_BASE};
['.ch','.mr','.dc','.it'].forEach(s=>
  document.querySelectorAll(s).forEach((e,i)=>e.style.setProperty('--i',i)));
const ov=document.getElementById('ov'),mc=document.getElementById('mc');
const fecha=()=>ov.hidden=true;
document.getElementById('mx').onclick=fecha;
ov.onclick=e=>{{if(e.target===ov)fecha()}};
addEventListener('keydown',e=>{{if(e.key==='Escape')fecha()}});
const nb=v=>String(v).replace('.',',');
const IC={{bal:'{ico("balanca",18)}',alvo:'{ico("alvo",18)}',fila:'{ico("fila",15)}',
  sino:'{ico("sino",15)}',pes:'{ico("pessoas",15)}',res:'{ico("resolvido",15)}',
  lupa:'{ico("lupa",15)}',prev:'{ico("previsao",15)}'}};
function barras(h){{
  if(!h.length)return '<p class="sub">Sem passagens no período.</p>';
  const mx=Math.max(...h.map(m=>m.passagens))||1;
  return '<div class="hb">'+h.map(m=>`<div class="hb-c">
    <i style="--h:${{Math.max(m.passagens/mx*100,4)}}%">
      <u style="--v:${{m.passagens?m.violacoes/m.passagens*100:0}}%"></u></i>
    <span>${{MES[m.mes-1]}}</span></div>`).join('')+'</div>';
}}
function abre(tipo,k){{
  let h='';
  if(tipo==='inc'){{const c=INC[k];
    h=`<span class="md-k">incidente em atendimento</span><h3 class="id">${{c.id}}</h3>
      <p class="sub">${{c.produto}} · equipe ${{c.equipe}} · ativo <span class="id">${{c.ativo}}</span></p>
      <div class="md-g"><div class="md-s no"><em>risco</em><b>${{nb(c.risco)}}%</b></div>
        <div class="md-s"><em>no ativo</em><b>${{c.viol}}/${{c.pass}}</b></div>
        <div class="md-s"><em>vs média</em><b>${{Math.round(c.risco/MEDIA)}}x</b></div></div>
      <div class="cx"><span class="chp t-ac">${{IC.alvo}}</span>
        <p>Em <b>100 casos parecidos com este</b>, o modelo espera que
        <b>${{c.em100}} estourem o prazo</b>. A média da base é ${{nb(MEDIA)}} em 100.</p></div>
      <div class="md-h">o que pesa neste caso</div>
      ${{c.sinais.map(([n,v])=>`<div class="sg"><span class="sg-t">${{n}}</span>
        <span class="sg-b"><i style="width:${{v/38*100}}%"></i></span>
        <span class="sg-v">${{v}}%</span></div>`).join('')}}
      <div class="md-h">histórico do ativo ${{c.ativo}}</div>
      ${{barras((ATIVO[c.ativo]||{{}}).hist||[])}}
      <div class="md-f"><button class="bt pr">${{IC.pes}}Escalar para a equipe</button>
        <button class="bt sc">${{IC.res}}Marcar como tratado</button></div>`;}}
  if(tipo==='prod'){{const p=PROD[k];
    h=`<span class="md-k">produto · posição ${{p.pos}} de 17</span><h3 class="id">${{p.nome}}</h3>
      <p class="sub">${{p.quad}} · ${{p.inc}} incidentes elegíveis, ${{p.viol}} violaram o prazo.</p>
      <div class="md-g">
        <div class="md-s ${{parseFloat(p.nota)<40?'no':'wn'}}"><em>nota</em><b>${{p.nota}}</b></div>
        <div class="md-s"><em>posição</em><b>${{p.pos}}º</b></div>
        <div class="md-s"><em>incidentes</em><b>${{p.inc}}</b></div></div>
      <div class="md-h">os cinco componentes da nota</div>
      ${{p.comp.map(c=>`<div class="sg"><span class="sg-t">${{c.rot}}
        <span style="color:#A3ABBA"> ${{c.v}}${{c.u}}</span></span>
        <span class="sg-b"><i style="width:${{c.pos}}%;background:${{c.pos>66?'#DC2626':c.pos>33?'#B45309':'#059669'}}"></i></span>
        <span class="sg-v">${{c.pos}}</span></div>`).join('')}}
      <div class="cx"><span class="chp t-ac">${{IC.bal}}</span>
        <p>A nota é <b>relativa</b>: quanto mais cheia a barra, pior comparado aos outros
        dezesseis. 100 seria o melhor em todos os cinco componentes.</p></div>
      <div class="md-f"><button class="bt pr">${{IC.lupa}}Ver causas deste produto</button>
        <button class="bt sc">${{IC.prev}}Comparar com outro</button></div>`;}}
  mc.innerHTML=h;ov.hidden=false;
}}
document.querySelectorAll('[data-mod]').forEach(b=>b.onclick=()=>abre(b.dataset.mod,b.dataset.k));
document.querySelectorAll('.fb').forEach(b=>b.onclick=()=>{{
  document.querySelectorAll(`.fb[data-g="${{b.dataset.g}}"]`).forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  if(b.dataset.g==='pri')document.querySelectorAll('.it').forEach(i=>
    i.style.display=b.dataset.v==='2'?'none':'flex');
}});
document.querySelectorAll('.da').forEach(b=>b.onclick=()=>{{
  document.querySelectorAll('.da').forEach(x=>x.classList.remove('on'));b.classList.add('on');}});
</script></body></html>'''

VARIANTES = [('b1-completa', heroi_completo, 'previsão do dia'),
             ('b-relogio-24h', relogio, 'previsão do dia · relógio de 24h'),
             ('b1-linha-da-marca', heroi_linha, 'previsão do dia · linha da marca'),
             ('b2-dia-esticado', heroi_faixa, 'previsão do dia · dia esticado'),
             ('b3-veredito', heroi_medidor, 'previsão do dia · veredito')]
for nome, fn, tit in VARIANTES:
    alvo = DEST / f'{nome}.html'
    alvo.write_text(pagina(fn(), tit), encoding='utf-8')
    print(f'  {alvo.name}')
