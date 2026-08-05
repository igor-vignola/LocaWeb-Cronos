# -*- coding: utf-8 -*-
"""Direcao A · Sala de operacao.

Aposta: o painel e uma parede de NOC, mas lido de cima para baixo como uma historia em
tres atos — o dia de hoje, onde agir agora, para onde o ano vai. Cada card diz em uma
linha o que ele e e para que serve. Clicar em ativo, incidente ou produto abre um modal
com o detalhe e a explicacao do modelo.

Sem monoespacada em lugar nenhum: identificador usa Outfit com espacamento solto.
Objeto de identidade: o mapa de ativos construido do dado. Textura de rack no fundo.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dados import (ATIVOS, BASE_20, COMPONENTES, DELTA_TAXA, DIA_HOJE, ELEG_30, EM_ABERTO, FILA,
                   FUT3, HIST_ATIVO, HOJE2, HOJE3, LBL_DIA, MEDIA_BASE, MES_LBL, ONTEM,
                   ONTEM_TOTAL, REAL3, SEMANA, SEM_VIOL, SINAIS, TAXA_30, TOTAL_VIOL,
                   ULTIMOS_DIAS, VIOL_30, dm, mil, proj, pt, saude)
from icones import CSS_ICO, chip, ico

OUT = Path.cwd() / 'prototipos' / 'telas' / 'direcoes' / 'a-sala-operacao.html'
OUT.parent.mkdir(parents=True, exist_ok=True)

topo = FILA[0]
pior = saude.index[-1]
ZONA = lambda t: 'crit' if t >= 10 else ('alta' if t >= 3 else ('med' if t >= 1 else 'ok'))


# ── componentes de layout ───────────────────────────────────────────────────
def ato(n, titulo, pergunta):
    """Divisoria de ato: da inicio, meio e fim para a leitura da pagina."""
    return f'''<div class="ato">
      <span class="ato-n">{n}</span>
      <div><h2>{titulo}</h2><p>{pergunta}</p></div>
    </div>'''


def cab(icone, titulo, oque, extra=''):
    """Cabecalho de card: o que e isso, em uma linha, sempre."""
    return f'''<div class="hdr">
      <div class="hdr-t">{ico(icone, 16)}<div><h3>{titulo}</h3><p>{oque}</p></div></div>
      {extra}</div>'''


def filtros(nome, opcoes, ativo=0):
    return ('<div class="fg">' + ''.join(
        f'<button class="fb{" on" if i == ativo else ""}" data-g="{nome}" data-v="{v}">{r}</button>'
        for i, (v, r) in enumerate(opcoes)) + '</div>')


def var(v, bom_e_baixo=True):
    bom = (v < 0) if bom_e_baixo else (v > 0)
    return (f'<span class="vr {"ok" if bom else "no"}">{"+" if v > 0 else "−"}'
            f'{pt(abs(v), 0)}%</span>')


def anel(fr, de, tom='no', tam=52):
    r = tam / 2 - 4
    c = 2 * math.pi * r
    return (f'<svg class="anr t-{tom}" viewBox="0 0 {tam} {tam}" width="{tam}" height="{tam}">'
            f'<circle class="anr-t" cx="{tam/2}" cy="{tam/2}" r="{r}"/>'
            f'<circle class="anr-v" cx="{tam/2}" cy="{tam/2}" r="{r}" '
            f'stroke-dasharray="{c:.1f}" stroke-dashoffset="{c:.1f}" '
            f'style="--f:{c*(1-fr/de):.1f}"/>'
            f'<text x="{tam/2}" y="{tam/2+3.4}" text-anchor="middle">{fr}</text></svg>')


def celulas():
    fora = []
    for nome, r in ATIVOS.iterrows():
        z = ZONA(r['taxa'])
        p = 3 if r['passagens'] > 1200 else (2 if r['passagens'] > 400 else 1)
        fora.append(f'''<button class="cel z-{z} p{p}" data-mod="ativo" data-k="{nome}"
          title="{nome} · {pt(r['taxa'], 1)}% de {mil(r['passagens'])} passagens · clique para abrir">
          {f'<b>{nome[-3:]}</b>' if z in ('crit', 'alta') else ''}</button>''')
    return ''.join(fora)


def circulos_dia():
    return ''.join(
        f'''<div class="dc{' vi' if v else ''}"><i>{v if v else ''}</i>
        <span>{LBL_DIA[d.dayofweek]}</span><em>{d.day:02d}/{d.month:02d}</em></div>'''
        for d, v in ULTIMOS_DIAS)


def barras_semana():
    mx = SEMANA.max()
    hoje = DIA_HOJE.dayofweek
    return ''.join(f'''<div class="sm{' ag' if i == hoje else ''}" style="--h:{SEMANA[i]/mx*100:.0f}%">
      <i></i><span>{LBL_DIA[i]}</span><em>{pt(SEMANA[i], 0)}</em></div>''' for i in range(7))


def arco(p, valor, meta, baixo, alto):
    esc = meta * 1.4
    ang = lambda v: min(v / esc, 1) * 240 - 120
    r, cx, cy = 74, 96, 92
    pol = lambda a: (cx + r * math.sin(math.radians(a)), cy - r * math.cos(math.radians(a)))
    x1, y1 = pol(-120)
    x2, y2 = pol(120)
    xv, yv = pol(ang(valor))
    xm, ym = pol(ang(meta))
    xb, yb = pol(ang(baixo))
    xa, ya = pol(ang(alto))
    dentro = valor <= meta
    grande = 1 if ang(alto) - ang(baixo) > 180 else 0
    return f'''<div class="arc {'ok' if dentro else 'no'}">
      <svg viewBox="0 0 192 146">
        <path class="a-t" d="M{x1:.1f} {y1:.1f} A{r} {r} 0 1 1 {x2:.1f} {y2:.1f}"/>
        <path class="a-f" d="M{xb:.1f} {yb:.1f} A{r} {r} 0 {grande} 1 {xa:.1f} {ya:.1f}"/>
        <line class="a-m" x1="{cx}" y1="{cy}" x2="{xm:.1f}" y2="{ym:.1f}"/>
        <circle class="a-v" cx="{xv:.1f}" cy="{yv:.1f}" r="6"/>
      </svg>
      <div class="arc-c"><b>{pt(valor)}</b><span>de {int(meta)}</span></div>
      <div class="arc-l"><span class="pr">{p}</span>
        <span class="zn">{'dentro da meta' if dentro else 'acima da meta'}</span>
        <em>faixa {pt(baixo, 0)} a {pt(alto, 0)}</em></div>
    </div>'''


def trilho(n_real=16, n_prev=7):
    real = REAL3.tail(n_real).reset_index(drop=True)
    fut = FUT3.head(n_prev).reset_index(drop=True)
    esc = [*real['valor'], *fut['valor'], *fut['baixo'], *fut['alto']]
    lo, hi = min(esc), max(esc)
    vao = (hi - lo) or 1
    n = len(real) + len(fut)
    w, h = 1000, 128
    px = lambda i: 4 + i / (n - 1) * (w - 8)
    py = lambda v: h - 20 - (v - lo) / vao * (h - 46)
    pr = [(px(i), py(v)) for i, v in enumerate(real['valor'])]
    corte = pr[-1]
    pf = [corte] + [(px(len(real) + i), py(v)) for i, v in enumerate(fut['valor'])]
    ln = lambda ps: 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in ps)
    hi_p = [(px(len(real) + i), py(v)) for i, v in enumerate(fut['alto'])]
    lo_p = [(px(len(real) + i), py(v)) for i, v in enumerate(fut['baixo'])]
    bd = (f'M{corte[0]:.1f} {corte[1]:.1f} L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in hi_p)
          + ' L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(lo_p)) + ' Z')
    i_max = int(real['valor'].idxmax())
    xm, ym = px(i_max), py(real['valor'][i_max])
    xh, yh = pf[1]
    return f'''<div class="tr" data-tr="{n_real}">
      <svg viewBox="0 0 {w} {h}" preserveAspectRatio="none">
        <path class="t-bd" d="{bd}"/>
        <line class="t-ag" x1="{corte[0]:.1f}" y1="4" x2="{corte[0]:.1f}" y2="{h-6}"/>
        <path class="t-l" d="{ln(pr)}"/><path class="t-f" d="{ln(pf)}"/>
        <g class="an"><line x1="{xm:.1f}" y1="{ym:.1f}" x2="{xm:.1f}" y2="{ym-20:.1f}"/>
          <circle cx="{xm:.1f}" cy="{ym:.1f}" r="3"/></g>
        <circle class="t-h" cx="{corte[0]:.1f}" cy="{corte[1]:.1f}" r="10"/>
        <circle class="t-n" cx="{corte[0]:.1f}" cy="{corte[1]:.1f}" r="4"/>
      </svg>
      <div class="anl" style="left:{xm/w*100:.1f}%;top:{max(ym-40,2)/h*100:.0f}%">dia mais cheio&nbsp;
        <b>{int(real['valor'][i_max])}</b>&nbsp;em {dm(real['dia'][i_max])}</div>
      <div class="anp" style="left:{xh/w*100:.1f}%;top:{(yh-38)/h*100:.0f}%">
        {pt(HOJE3['valor'], 0)} previstos hoje</div>
      <div class="tr-x"><span>{dm(real['dia'].iloc[0])}</span>
        <span class="ag" style="left:{corte[0]/w*100:.1f}%">{dm(DIA_HOJE)} · agora</span>
        <span>{dm(fut['dia'].iloc[-1])}</span></div>
    </div>'''


# ── dados que o modal consome ───────────────────────────────────────────────
MOD_ATIVO = {a: {'nome': a, 'pass': int(r['passagens']), 'viol': int(r['violacoes']),
                 'taxa': pt(r['taxa'], 1), 'x': int(round(r['taxa'] / MEDIA_BASE)),
                 'hist': HIST_ATIVO.get(a, [])}
             for a, r in ATIVOS.iterrows()}
MOD_INC = {c['id']: {**{k: v for k, v in c.items() if k != 'taxa_ativo'},
                     'taxa_ativo': pt(c['taxa_ativo'], 1),
                     'sinais': SINAIS, 'em100': int(round(c['risco']))}
           for c in FILA}
MOD_PROD = {p: {'nome': p, 'nota': pt(saude.loc[p, 'nota']), 'pos': int(saude.loc[p, 'posicao']),
                'quad': saude.loc[p, 'quadrante'], 'inc': mil(saude.loc[p, 'incidentes']),
                'viol': int(saude.loc[p, 'violacoes']),
                'comp': [{'rot': rot, 'v': pt(saude.loc[p, k] * mult, 2 if mult == 100 else 1),
                          'u': u, 'pos': round(float(saude.loc[p, 'pos_' + k]) * 100)}
                         for k, rot, u, mult in COMPONENTES]}
            for p in saude.index}

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#07080C;--sf:#0E1118;--sf2:#151924;--ln:rgba(255,255,255,.075);
 --ln2:rgba(255,255,255,.15);--tx:#8E97A9;--tx2:#5F697C;--tx3:#434B5C;--hd:#F1F4F9;
 --ac:#3B7DFF;--no:#F0483E;--wn:#F0A02A;--ok:#22C08A;
 --e:cubic-bezier(.19,1,.22,1);--e2:cubic-bezier(.34,1.56,.64,1)}
html{-webkit-font-smoothing:antialiased;scroll-behavior:smooth}
body{background:var(--bg);color:var(--hd);min-height:100dvh;overflow-x:hidden;
 font-family:'Outfit',system-ui,sans-serif;font-size:15px;letter-spacing:-.01em}
/* identificador: mesma familia, espacamento solto e numero alinhado. Sem monoespacada. */
.id{font-weight:600;letter-spacing:.055em;font-variant-numeric:tabular-nums lining-nums}
.nb{font-variant-numeric:tabular-nums lining-nums}
/* fundo: textura de rack + brilho */
.rk{position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.55;
 background-image:repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 1px,transparent 1px 19px),
  repeating-linear-gradient(90deg,rgba(255,255,255,.02) 0 1px,transparent 1px 116px);
 mask:radial-gradient(114% 84% at 78% -8%,#000 4%,transparent 66%)}
.wm{position:fixed;inset:auto auto -9vh -2vw;font-size:31vw;font-weight:800;line-height:.7;
 color:#fff;opacity:.016;letter-spacing:-.06em;pointer-events:none;z-index:0;user-select:none}
.gl{position:fixed;inset:0;z-index:0;pointer-events:none;
 background:radial-gradient(50% 38% at 12% 0,rgba(59,125,255,.19),transparent 66%),
  radial-gradient(38% 32% at 88% 6%,rgba(59,125,255,.1),transparent 70%),
  radial-gradient(34% 38% at 60% 100%,rgba(240,72,62,.06),transparent 72%);
 animation:dr 32s ease-in-out infinite alternate}
@keyframes dr{to{transform:translate3d(-3%,2%,0) scale(1.1)}}
.sh{position:relative;z-index:1;max-width:1520px;margin:0 auto;padding:18px 30px 70px}
/* topo */
.tp{display:flex;align-items:center;gap:14px;margin-bottom:22px;flex-wrap:wrap;
 position:sticky;top:0;z-index:20;padding:12px 0;
 background:linear-gradient(180deg,rgba(7,8,12,.96) 55%,transparent);backdrop-filter:blur(6px)}
.br{display:flex;align-items:center;gap:11px}
.br-m{width:34px;height:34px;border-radius:11px;background:linear-gradient(150deg,#fff,#D3E0FF);
 display:grid;place-items:center;box-shadow:0 4px 14px rgba(0,0,0,.55)}
.br b{font-size:17px;font-weight:700;letter-spacing:-.04em;display:block;line-height:1}
.br em{font-size:8.5px;letter-spacing:.16em;color:var(--tx2);font-style:normal;font-weight:600}
.pil{display:flex;gap:3px;background:rgba(255,255,255,.045);border:1px solid var(--ln);
 border-radius:13px;padding:4px;backdrop-filter:blur(14px)}
.pil button{display:inline-flex;align-items:center;gap:7px;background:0;border:0;font:inherit;
 font-size:13px;font-weight:500;color:var(--tx);padding:8px 14px;border-radius:9px;cursor:pointer;
 transition:all .34s var(--e);white-space:nowrap}
.pil button:hover:not(:disabled){color:var(--hd)}
.pil button.on{background:rgba(255,255,255,.1);color:#fff;
 box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 2px 10px rgba(0,0,0,.4)}
.pil button:disabled{opacity:.28;cursor:default}
.tp-r{margin-left:auto;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.stl{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;color:var(--tx);
 background:rgba(255,255,255,.04);border:1px solid var(--ln);padding:7px 12px;border-radius:999px}
.stl .ic{color:var(--tx2)}
.stl i{width:6px;height:6px;border-radius:50%;background:var(--ok);
 box-shadow:0 0 0 3px rgba(34,192,138,.18);animation:pu 2.6s ease-in-out infinite}
@keyframes pu{50%{opacity:.32}}
/* hero */
.hr{position:relative;display:grid;grid-template-columns:1fr auto;gap:26px;align-items:center;
 margin-bottom:8px;padding:24px 28px;border:1px solid var(--ln);border-radius:26px;
 background:linear-gradient(120deg,rgba(21,25,36,.92),rgba(14,17,24,.5));overflow:hidden}
.hr::before{content:'';position:absolute;inset:0;pointer-events:none;
 background:radial-gradient(62% 130% at 100% 50%,rgba(240,72,62,.12),transparent 60%)}
.hr>*{position:relative}
.hr h1{font-size:13.5px;font-weight:600;color:var(--tx);margin-bottom:10px;
 display:flex;align-items:center;gap:8px}
.hr h1 .ic{color:var(--tx2)}
.hr p{font-size:24px;font-weight:500;line-height:1.4;letter-spacing:-.026em;color:#E6EBF5;
 max-width:78ch}
.hr p b{font-weight:650;color:#fff}
.hr p .cr{color:#FF7D74;font-weight:650}.hr p .wr{color:#F5B45C;font-weight:650}
.big{text-align:right;margin-right:-32px;user-select:none}
.big b{font-size:110px;font-weight:800;line-height:.76;letter-spacing:-.06em;color:#fff;
 opacity:.1;display:block}
.big span{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--tx3);
 display:block;margin-top:6px;margin-right:36px}
/* divisoria de ato: da inicio, meio e fim */
.ato{display:flex;align-items:flex-start;gap:15px;margin:34px 0 15px;padding-top:22px;
 border-top:1px solid var(--ln)}
.ato-n{font-size:11px;font-weight:800;letter-spacing:.1em;color:var(--ac);
 background:rgba(59,125,255,.13);border:1px solid rgba(59,125,255,.26);border-radius:9px;
 padding:5px 10px;flex-shrink:0;margin-top:2px}
.ato h2{font-size:19px;font-weight:650;letter-spacing:-.03em;color:#fff}
.ato p{font-size:13px;color:var(--tx2);margin-top:2px}
/* cards */
.gr{display:grid;grid-template-columns:1.46fr 1fr;gap:16px;align-items:stretch}
.cd{display:flex;flex-direction:column;background:linear-gradient(168deg,var(--sf2),var(--sf));
 border:1px solid var(--ln);border-radius:22px;padding:19px 21px;position:relative;
 overflow:hidden;box-shadow:0 1px 0 rgba(255,255,255,.045) inset,0 22px 50px -30px #000}
.cd::after{content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;
 background:radial-gradient(320px 200px at var(--mx,50%) var(--my,0),rgba(59,125,255,.075),transparent 66%);
 opacity:0;transition:opacity .5s var(--e)}
.cd:hover::after{opacity:1}
.cd>*{position:relative;z-index:1}
.cd>.nt{margin-top:auto}
/* cabecalho que diz o que e o card */
.hdr{display:flex;align-items:flex-start;gap:14px;margin-bottom:14px}
.hdr-t{display:flex;gap:10px;flex:1;min-width:0}
.hdr-t .ic{color:var(--ac);margin-top:2px;flex-shrink:0}
.hdr h3{font-size:14.5px;font-weight:650;letter-spacing:-.02em;color:#fff}
.hdr p{font-size:11.5px;color:var(--tx2);margin-top:2px;line-height:1.45}
/* filtros */
.fg{display:flex;gap:2px;background:rgba(255,255,255,.04);border:1px solid var(--ln);
 border-radius:10px;padding:3px;flex-shrink:0}
.fb{background:0;border:0;font:inherit;font-size:11px;font-weight:600;color:var(--tx2);
 padding:5px 10px;border-radius:7px;cursor:pointer;transition:all .3s var(--e);white-space:nowrap}
.fb:hover{color:var(--hd)}
.fb.on{background:rgba(255,255,255,.1);color:#fff}
.vr{font-size:10.5px;font-weight:700;padding:3px 7px;border-radius:6px;letter-spacing:0;
 margin-left:6px}
.vr.ok{background:rgba(34,192,138,.15);color:#3FD69B}
.vr.no{background:rgba(240,72,62,.15);color:#FF7D74}
/* mapa de ativos */
.mp{display:flex;flex-wrap:wrap;gap:5px;align-content:flex-start}
.cel{border:1px solid var(--ln);border-radius:7px;background:rgba(255,255,255,.055);
 cursor:pointer;font:inherit;color:#6C7689;display:grid;place-items:center;
 transition:transform .3s var(--e2),border-color .3s var(--e),opacity .3s var(--e);
 animation:ce .5s var(--e) both;animation-delay:calc(var(--i,0)*11ms)}
@keyframes ce{from{opacity:0;transform:scale(.7)}}
.cel b{font-size:9px;font-weight:600;opacity:.72;letter-spacing:.03em}
.cel.p1{width:30px;height:30px}.cel.p2{width:38px;height:38px}.cel.p3{width:48px;height:48px}
.cel:hover{transform:translateY(-3px) scale(1.07);border-color:var(--ln2);z-index:3}
.cel.z-med{background:rgba(240,160,42,.2);border-color:rgba(240,160,42,.34);color:#E8B878}
.cel.z-alta{background:rgba(240,160,42,.42);border-color:rgba(240,160,42,.6);color:#FFE2B4}
.cel.z-crit{background:rgba(240,72,62,.46);border-color:rgba(240,72,62,.72);color:#FFE0DD}
.cel.off{opacity:.14;pointer-events:none}
.cel.z-crit:first-child{animation:ce .5s var(--e) both,al 2.4s ease-in-out 1s infinite}
@keyframes al{50%{box-shadow:0 0 0 7px rgba(240,72,62,.14),0 0 22px rgba(240,72,62,.45)}}
.mpl{display:flex;gap:15px;margin:15px 0;padding-top:13px;border-top:1px solid var(--ln);
 flex-wrap:wrap;align-items:center}
.mpl span{display:inline-flex;align-items:center;gap:6px;font-size:10.5px;color:var(--tx2)}
.mpl i{width:9px;height:9px;border-radius:3px;flex-shrink:0}
.i-ok{background:rgba(255,255,255,.14)}.i-med{background:rgba(240,160,42,.4)}
.i-alta{background:rgba(240,160,42,.75)}.i-crit{background:rgba(240,72,62,.8)}
.dica{margin-left:auto;font-size:10.5px;color:var(--tx3);display:inline-flex;align-items:center;
 gap:5px}
/* painel do ativo */
.at{margin-top:auto;background:rgba(240,72,62,.06);border:1px solid rgba(240,72,62,.2);
 border-radius:17px;padding:14px 16px;display:flex;align-items:center;gap:15px;cursor:pointer;
 transition:background .4s var(--e),border-color .4s var(--e),transform .3s var(--e)}
.at:hover{transform:translateY(-2px)}
.at-t{flex:1;min-width:0}
.at-t b{font-size:15px;font-weight:650;display:block;color:#fff}
.at-t span{font-size:12px;color:var(--tx);display:block;margin-top:3px}
.at-n{text-align:right;flex-shrink:0}
.at-n b{font-size:26px;font-weight:650;color:#FF7D74;letter-spacing:-.04em;display:block;
 line-height:1;transition:color .4s var(--e)}
.at-n span{font-size:9.5px;color:var(--tx2);letter-spacing:.09em;text-transform:uppercase}
.anr .anr-t{fill:none;stroke:rgba(255,255,255,.09);stroke-width:4}
.anr .anr-v{fill:none;stroke-width:4;stroke-linecap:round;transform:rotate(-90deg);
 transform-origin:center;animation:ar 1.1s var(--e) .5s forwards}
.anr.t-no .anr-v{stroke:#F0483E}.anr.t-wn .anr-v{stroke:#F0A02A}.anr.t-ok .anr-v{stroke:#22C08A}
.anr text{fill:#fff;font-size:15px;font-weight:650;letter-spacing:-.03em;
 font-family:'Outfit',sans-serif}
@keyframes ar{to{stroke-dashoffset:var(--f)}}
/* linha de metrica com icone tingido */
.ml{display:flex;flex-direction:column;gap:7px}
.mr{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.028);
 border:1px solid var(--ln);border-radius:14px;padding:11px 13px;
 animation:sl .5s var(--e) both;animation-delay:calc(150ms + var(--i,0)*55ms)}
@keyframes sl{from{opacity:0;transform:translateX(-12px)}}
.mr-t{flex:1;min-width:0}
.mr-t b{font-size:13px;font-weight:500;color:#DDE4EF;display:block}
.mr-t span{font-size:11px;color:var(--tx2);display:block;margin-top:1px}
.mr-v{font-size:20px;font-weight:650;letter-spacing:-.035em;flex-shrink:0;
 font-variant-numeric:tabular-nums;display:inline-flex;align-items:baseline}
.mr-v u{font-size:11.5px;font-weight:500;color:var(--tx2);text-decoration:none;margin-left:3px}
.mr-v.no{color:#FF7D74}.mr-v.ok{color:#3FD69B}.mr-v.wn{color:#F5B45C}
/* circulo por dia */
.dcs{display:flex;gap:6px}
.dc{flex:1;display:flex;flex-direction:column;align-items:center;gap:5px}
.dc i{width:100%;aspect-ratio:1;max-width:38px;border-radius:50%;border:1.5px solid var(--ln2);
 display:grid;place-items:center;font-style:normal;font-size:12px;font-weight:650;
 color:var(--tx2);animation:pn .4s var(--e2) both;animation-delay:calc(var(--i,0)*45ms)}
.dc.vi i{background:rgba(240,72,62,.2);border-color:rgba(240,72,62,.58);color:#FF9E97}
.dc span{font-size:9.5px;color:var(--tx2);letter-spacing:.03em}
.dc em{font-size:9.5px;font-style:normal;color:var(--tx3);font-variant-numeric:tabular-nums}
/* fila */
.fl{display:flex;flex-direction:column;gap:7px}
.it{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.026);
 border:1px solid var(--ln);border-radius:14px;padding:11px 13px;cursor:pointer;
 transition:all .34s var(--e);animation:sl .5s var(--e) both;text-align:left;
 animation-delay:calc(180ms + var(--i)*58ms);font:inherit;color:inherit;width:100%}
.it:hover{background:rgba(255,255,255,.055);border-color:var(--ln2);transform:translateX(4px)}
.it-r{width:42px;height:42px;border-radius:13px;display:grid;place-items:center;flex-shrink:0;
 font-size:13.5px;font-weight:700;letter-spacing:-.03em}
.it-r.crit{background:rgba(240,72,62,.18);color:#FF8B84}
.it-r.alta{background:rgba(240,160,42,.17);color:#FFC176}
.it-t{flex:1;min-width:0}
.it-t b{font-size:13.5px;display:block;color:#EDF1F8}
.it-t span{font-size:11.5px;color:var(--tx2);margin-top:2px;
 display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.it-t span .ic{width:12px;height:12px;opacity:.55}
.it-t span u{text-decoration:none;margin-right:7px;display:inline-flex;align-items:center;gap:4px}
.it-b{flex-shrink:0;text-align:right}
.it-b em{font-size:9.5px;font-style:normal;color:var(--tx3);letter-spacing:.07em;
 text-transform:uppercase;display:block}
.it-b b{font-size:12.5px;color:var(--tx);font-weight:600}
.it .sq{color:var(--tx3);flex-shrink:0;transition:transform .3s var(--e),color .3s var(--e)}
.it:hover .sq{color:var(--ac);transform:translateX(3px)}
/* arcos */
.arcs{display:flex;gap:6px}
.arc{flex:1;text-align:center}
.arc svg{width:100%;max-width:184px;height:auto;overflow:visible}
.arc .a-t{fill:none;stroke:rgba(255,255,255,.075);stroke-width:11;stroke-linecap:round}
.arc .a-f{fill:none;stroke-width:11;stroke-linecap:round;stroke-dasharray:400;
 stroke-dashoffset:400;animation:dw 1.5s var(--e) .4s forwards}
.arc.ok .a-f{stroke:rgba(34,192,138,.82)}.arc.no .a-f{stroke:rgba(240,72,62,.82)}
.arc .a-m{stroke:#fff;stroke-width:1.6;stroke-dasharray:2 3;opacity:.45}
.arc .a-v{opacity:0;animation:pn .5s var(--e2) 1.3s forwards}
.arc.ok .a-v{fill:var(--ok)}.arc.no .a-v{fill:var(--no)}
@keyframes dw{to{stroke-dashoffset:0}}
@keyframes pn{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
.arc-c{margin-top:-46px}
.arc-c b{font-size:30px;font-weight:650;letter-spacing:-.045em;display:block;line-height:1}
.arc-c span{font-size:11px;color:var(--tx2)}
.arc-l{margin-top:12px}
.arc-l .pr{font-size:10px;font-weight:700;letter-spacing:.12em;color:var(--tx2)}
.arc-l .zn{display:block;font-size:12.5px;font-weight:600;margin-top:3px}
.arc.ok .zn{color:#3FD69B}.arc.no .zn{color:#FF7D74}
.arc-l em{display:block;font-size:10.5px;color:var(--tx3);font-style:normal;margin-top:2px}
/* barra por dia da semana */
.sms{display:flex;align-items:flex-end;gap:8px;height:104px;margin-top:4px}
.sm{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;
 justify-content:flex-end}
.sm i{width:64%;height:var(--h);border-radius:7px 7px 3px 3px;
 background:linear-gradient(180deg,rgba(255,255,255,.2),rgba(255,255,255,.06));
 transform:scaleY(0);transform-origin:bottom;animation:gu .8s var(--e) both;
 animation-delay:calc(350ms + var(--i,0)*55ms)}
@keyframes gu{to{transform:scaleY(1)}}
.sm span{font-size:10px;color:var(--tx2);letter-spacing:.04em}
.sm em{font-size:10.5px;font-style:normal;color:var(--tx3);font-variant-numeric:tabular-nums}
.sm.ag i{background:linear-gradient(180deg,var(--ac),rgba(59,125,255,.45));
 box-shadow:0 0 18px rgba(59,125,255,.3)}
.sm.ag span{color:#7FA9FF;font-weight:600}.sm.ag em{color:#A8C4FF}
/* trilho */
.tr{position:relative;margin-top:16px}
.tr svg{width:100%;height:128px;display:block;overflow:visible}
.t-l{fill:none;stroke:var(--ac);stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round;
 stroke-dasharray:1500;stroke-dashoffset:1500;animation:dw 1.7s var(--e) .3s forwards}
.t-f{fill:none;stroke:var(--ac);stroke-width:1.8;stroke-dasharray:5 4;opacity:0;
 animation:fd .8s ease 1.5s forwards;--o:.85}
.t-bd{fill:var(--ac);opacity:0;animation:fd 1s ease 1.6s forwards;--o:.15}
.t-ag{stroke:var(--ln2);stroke-width:1;stroke-dasharray:2 4;opacity:0;
 animation:fd .5s ease 1.4s forwards;--o:1}
.t-n{fill:#fff;opacity:0;animation:pn .5s var(--e2) 1.3s forwards}
.t-h{fill:var(--ac);opacity:0;transform-box:fill-box;transform-origin:center;
 animation:hl 3s ease-out 2s infinite}
@keyframes hl{0%{opacity:.4;transform:scale(.3)}70%,100%{opacity:0;transform:scale(1.7)}}
@keyframes fd{to{opacity:var(--o,1)}}
.an line{stroke:var(--ln2);stroke-width:1}
.an circle{fill:#fff}
.anl,.anp{position:absolute;transform:translateX(-50%);font-size:10.5px;color:var(--tx2);
 white-space:nowrap;opacity:0;animation:fd .6s ease 1.9s forwards}
.anl b{color:#C6D0E2;font-weight:650}
.anp{background:rgba(59,125,255,.17);border:1px solid rgba(59,125,255,.35);color:#A8C4FF;
 padding:3px 8px;border-radius:7px;font-weight:600;animation-delay:2.1s}
.tr-x{display:flex;justify-content:space-between;font-size:9.5px;color:var(--tx3);
 letter-spacing:.09em;text-transform:uppercase;position:relative;margin-top:2px}
.tr-x .ag{position:absolute;transform:translateX(-50%);color:#7FA9FF;font-weight:600}
/* ranking */
.rw{display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid var(--ln);
 cursor:pointer;background:0;border-left:0;border-right:0;border-top:0;width:100%;font:inherit;
 color:inherit;text-align:left;transition:padding .3s var(--e)}
.rw:hover{padding-left:5px}
.rw:last-of-type{border-bottom:0}
.rw-p{width:46px;font-weight:650;font-size:12.5px;color:#C6D0E2}
.rw-b{flex:1;height:6px;border-radius:3px;background:rgba(255,255,255,.07);overflow:hidden}
.rw-b i{display:block;height:100%;border-radius:3px;width:0;background:var(--c);
 animation:gw 1s var(--e) both;animation-delay:calc(450ms + var(--i)*70ms)}
@keyframes gw{to{width:var(--w)}}
.rw-v{width:36px;text-align:right;font-size:13px;font-weight:650;
 font-variant-numeric:tabular-nums}
.rw-q{width:92px;font-size:10px;color:var(--tx3);text-align:right}
.nt{font-size:11.5px;color:var(--tx2);line-height:1.62;margin-top:13px;padding-top:12px;
 border-top:1px solid var(--ln)}
.nt b{color:#C6D0E2;font-weight:600}
/* modal de aprofundamento */
.ov{position:fixed;inset:0;z-index:90;display:grid;place-items:center;padding:28px;
 background:rgba(4,5,8,.72);backdrop-filter:blur(9px);animation:fd .3s ease both;--o:1}
.ov[hidden]{display:none}
.md{width:min(620px,100%);max-height:86dvh;overflow:auto;position:relative;
 background:linear-gradient(168deg,#181D29,#0F131B);border:1px solid var(--ln2);
 border-radius:26px;padding:26px 28px;box-shadow:0 40px 90px -30px #000;
 animation:mu .5s var(--e) both}
@keyframes mu{from{opacity:0;transform:translateY(20px) scale(.975)}}
.md-x{position:absolute;top:18px;right:18px;width:32px;height:32px;border-radius:10px;
 background:rgba(255,255,255,.05);border:1px solid var(--ln);color:var(--tx);cursor:pointer;
 display:grid;place-items:center;transition:all .3s var(--e)}
.md-x:hover{background:rgba(255,255,255,.11);color:#fff}
.md-k{font-size:9.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
 color:var(--ac)}
.md h3{font-size:26px;font-weight:650;letter-spacing:-.035em;margin-top:7px;color:#fff}
.md .sub{font-size:13px;color:var(--tx);margin-top:5px}
.md-g{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:20px}
.md-s{background:rgba(255,255,255,.035);border:1px solid var(--ln);border-radius:14px;
 padding:13px 14px}
.md-s em{font-size:9.5px;font-style:normal;letter-spacing:.1em;text-transform:uppercase;
 color:var(--tx2);display:block}
.md-s b{font-size:23px;font-weight:650;letter-spacing:-.04em;display:block;margin-top:5px;
 line-height:1}
.md-s.no b{color:#FF7D74}.md-s.ok b{color:#3FD69B}.md-s.wn b{color:#F5B45C}
.md-h{font-size:10px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;
 color:var(--tx2);margin:22px 0 11px;display:flex;align-items:center;gap:8px}
.md-h::after{content:'';flex:1;height:1px;background:var(--ln)}
.hb{display:flex;align-items:flex-end;gap:5px;height:74px}
.hb-c{flex:1;display:flex;flex-direction:column;align-items:center;gap:5px;height:100%;
 justify-content:flex-end}
.hb-c i{width:100%;border-radius:5px 5px 2px 2px;background:rgba(255,255,255,.12);
 position:relative;height:var(--h)}
.hb-c i u{position:absolute;inset:auto 0 0 0;height:var(--v);border-radius:0 0 2px 2px;
 background:#F0483E;text-decoration:none}
.hb-c span{font-size:9.5px;color:var(--tx3)}
.sg{display:flex;align-items:center;gap:11px;padding:8px 0}
.sg-t{flex:1;font-size:12.5px;color:#DDE4EF}
.sg-b{width:130px;height:6px;border-radius:3px;background:rgba(255,255,255,.07);overflow:hidden}
.sg-b i{display:block;height:100%;border-radius:3px;background:linear-gradient(90deg,#5B93FF,#2563EB)}
.sg-v{width:34px;text-align:right;font-size:12.5px;font-weight:650;
 font-variant-numeric:tabular-nums}
.cx{background:rgba(59,125,255,.09);border:1px solid rgba(59,125,255,.2);border-radius:15px;
 padding:14px 16px;margin-top:18px;display:flex;gap:12px}
.cx p{font-size:12.5px;color:#C2CCDC;line-height:1.6}
.cx p b{color:#fff;font-weight:650}
.md-f{margin-top:20px;padding-top:15px;border-top:1px solid var(--ln);display:flex;gap:9px;
 flex-wrap:wrap}
.bt{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:12.5px;
 font-weight:600;padding:10px 15px;border-radius:11px;cursor:pointer;
 transition:all .3s var(--e)}
.bt.pr{background:var(--ac);border:1px solid var(--ac);color:#fff}
.bt.pr:hover{background:#2E6BE8;transform:translateY(-1px)}
.bt.sc{background:rgba(255,255,255,.05);border:1px solid var(--ln);color:var(--tx)}
.bt.sc:hover{background:rgba(255,255,255,.1);color:#fff}
.bt:active{transform:scale(.98)}
@media (max-width:1200px){.gr,.hr{grid-template-columns:1fr}.big{display:none}}
@media (max-width:640px){.md-g{grid-template-columns:1fr 1fr}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}
 .a-f,.t-l{stroke-dashoffset:0!important}
 .t-f,.t-bd,.t-ag,.t-n,.a-v,.anl,.anp,.ov,.md{opacity:1!important}.t-bd{opacity:.15!important}
 .t-h{opacity:0!important}.sm i{transform:none!important}.rw-b i{width:var(--w)!important}
 .cel,.it,.mr,.dc i,.md{transform:none!important;opacity:1!important}
 .anr .anr-v{stroke-dashoffset:var(--f)!important}}
"""

HTML = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cronos · sala de operação</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}{CSS_ICO}</style></head><body>
<div class="rk"></div><div class="wm">CRONOS</div><div class="gl"></div>
<div class="sh">
  <div class="tp">
    <div class="br"><div class="br-m"><svg viewBox="0 0 28 28" width="18" height="18" fill="none">
      <path d="M6 22L12 14L16 17L22 8" stroke="#0B0D13" stroke-width="2.6" stroke-linecap="round"
        stroke-linejoin="round"/><circle cx="22" cy="8" r="3" stroke="#2563EB" stroke-width="1.9"/>
      <circle cx="22" cy="8" r="1.3" fill="#2563EB"/></svg></div>
      <div><b>Cronos</b><em>VEJA ANTES · AJA ANTES</em></div></div>
    <div class="pil">
      <button class="on">{ico('grade', 15)}Sala</button>
      <button>{ico('fila', 15)}Fila</button>
      <button>{ico('coracao', 15)}Saúde</button>
      <button>{ico('lupa', 15)}Causas</button>
      <button disabled>{ico('previsao', 15)}Volume</button></div>
    <div class="tp-r">
      <span class="stl"><i></i>carga de {dm(ONTEM['dia'])} · 23h59</span>
      <span class="stl">{ico('relogio', 14)}turno da manhã</span></div>
  </div>

  <div class="hr">
    <div>
      <h1>{ico('agora', 15)}Situação da operação · {DIA_HOJE.day:02d}/{DIA_HOJE.month:02d}/{DIA_HOJE.year}, 07h00</h1>
      <p>Volume dentro do normal e <b>risco concentrado em um ativo</b>: o
        <b class="id">{topo['ativo']}</b> responde por <span class="cr">{topo['viol']} das
        {TOTAL_VIOL}</span> violações do ano em apenas <b>{topo['pass']}</b> passagens, e cinco
        dos seis primeiros da fila de hoje são dele. No fechamento o
        <span class="wr">P3 projeta {pt(proj.loc['P3','projeção'])}</span> contra meta de
        {int(proj.loc['P3','meta máxima'])}.</p>
    </div>
    <div class="big"><b>{pt(HOJE3['valor'], 0)}</b><span>previstos hoje · P3</span></div>
  </div>

  {ato('01', 'O dia de hoje', 'Quanto vem, quanto veio ontem e como a semana vinha se comportando.')}
  <div class="gr">
    <div class="cd">
      {cab('previsao', 'Quanto trabalho entra hoje',
           'A linha cheia é o que já entrou. A pontilhada é a previsão do modelo, e a faixa '
           'em volta é a margem de erro dele.',
           filtros('per', [('16', '16 dias'), ('30', '30 dias')]))}
      {trilho()}
      <div class="nt">Ontem entraram <b>{ONTEM_TOTAL}</b> elegíveis contra <b>{pt(BASE_20, 0)}</b>
        de média dos últimos vinte dias úteis. Serve para dimensionar a equipe do dia — não diz
        onde o prazo vai estourar.</div>
    </div>

    <div class="cd">
      {cab('prazo', 'Os últimos dez dias úteis',
           'Círculo vazio é dia que fechou sem nenhuma violação de prazo. Cheio mostra quantas '
           'houve naquele dia.')}
      <div class="dcs">{circulos_dia()}</div>
      <div class="ml" style="margin-top:16px">
        <div class="mr">{chip('escudo_ok', 'ok')}
          <div class="mr-t"><b>Dias úteis seguidos sem violação</b>
            <span>contando de {dm(DIA_HOJE)} para trás</span></div>
          <span class="mr-v ok">{SEM_VIOL}<u>dias</u></span></div>
        <div class="mr">{chip('balanca', 'nt')}
          <div class="mr-t"><b>Taxa dos últimos trinta dias</b>
            <span>{VIOL_30} violações em {mil(ELEG_30)} elegíveis</span></div>
          <span class="mr-v">{pt(TAXA_30, 2)}<u>%</u>{var(DELTA_TAXA)}</span></div>
      </div>
    </div>
  </div>

  {ato('02', 'Onde agir agora',
       'Os casos abertos com maior chance de estourar o prazo, e onde eles se concentram.')}
  <div class="gr">
    <div class="cd">
      {cab('grade', 'Mapa de ativos',
           f'Cada quadrado é um dos {len(ATIVOS)} ativos com mais incidentes. O tamanho vem do '
           'volume, a cor vem da taxa de violação. Clique para abrir o histórico.',
           filtros('zona', [('todos', 'todos'), ('risco', 'só em risco')]))}
      <div class="mp">{celulas()}</div>
      <div class="mpl">
        <span><i class="i-ok"></i>abaixo de 1%</span><span><i class="i-med"></i>1 a 3%</span>
        <span><i class="i-alta"></i>3 a 10%</span><span><i class="i-crit"></i>acima de 10%</span>
        <span class="dica">{ico('lupa', 13)}clique para abrir</span></div>
      <button class="at" data-mod="ativo" data-k="{topo['ativo']}">
        {anel(topo['viol'], topo['pass'])}
        <div class="at-t"><b class="id">{topo['ativo']}</b>
          <span>{topo['viol']} de {topo['pass']} passagens violaram o prazo ·
            {int(round(topo['taxa_ativo'] / MEDIA_BASE))} vezes a média da base</span></div>
        <div class="at-n"><b>{pt(topo['taxa_ativo'], 1)}%</b><span>taxa</span></div>
      </button>
    </div>

    <div class="cd">
      {cab('fila', 'Fila de hoje',
           'Incidentes abertos, ordenados pela chance de estourar o prazo. Clique para ver por '
           'que o modelo pontuou assim.',
           filtros('pri', [('t', 'todas'), ('2', 'P2'), ('3', 'P3')]))}
      <div class="fl">
        {"".join(f"""<button class="it" style="--i:{j}" data-mod="inc" data-k="{c['id']}">
          <span class="it-r {'crit' if c['risco'] >= 40 else 'alta'}">{pt(c['risco'], 0)}%</span>
          <span class="it-t"><b class="id">{c['id']}</b>
            <span><u>{ico('produto', 12)}{c['produto']}</u><u>{ico('pessoas', 12)}{c['equipe']}</u>
              <u>{ico('ativo', 12)}<span class="id">{c['ativo']}</span></u></span></span>
          <span class="it-b"><em>no ativo</em><b>{c['viol']}/{c['pass']}</b></span>
          <span class="sq">{ico('seta', 15)}</span>
        </button>""" for j, c in enumerate(FILA))}
      </div>
      <div class="nt">São <b>{mil(EM_ABERTO)}</b> em atendimento agora. A média da base é
        <b>{pt(MEDIA_BASE, 2)}%</b>, então 40% é quarenta vezes a média. Nos cinquenta primeiros
        da fila estão <b>15 das 50</b> violações do período.</div>
    </div>
  </div>

  {ato('03', 'Para onde o ano vai',
       'Se nada mudar, onde o KPI fecha em dezembro e quais produtos puxam para baixo.')}
  <div class="gr">
    <div class="cd">
      {cab('alvo', 'Fechamento contra a meta',
           'A projeção soma o que já fechou, o risco da fila aberta e o volume que ainda entra. '
           'O tracejado é o limite do ano.')}
      <div class="arcs">
        {arco('P2', proj.loc['P2','projeção'], proj.loc['P2','meta máxima'],
              proj.loc['P2','faixa baixa'], proj.loc['P2','faixa alta'])}
        {arco('P3', proj.loc['P3','projeção'], proj.loc['P3','meta máxima'],
              proj.loc['P3','faixa baixa'], proj.loc['P3','faixa alta'])}
      </div>
      <div class="nt">Em três das dez projeções testadas o valor central cruzaria a meta sem que
        o ano cruzasse. Por isso a faixa aparece junto: ela é a parte honesta da previsão.</div>
    </div>

    <div class="cd">
      {cab('coracao', 'Produtos com pior nota',
           'Nota de 0 a 100 por posição relativa entre os 17 produtos. Clique para ver os cinco '
           'componentes que formam a nota.')}
      <div>
        {"".join(f"""<button class="rw" style="--i:{j}" data-mod="prod" data-k="{x}">
          <span class="rw-p id">{x}</span>
          <span class="rw-b"><i style="--w:{saude.loc[x,'nota']:.0f}%;--c:{'#F0483E' if saude.loc[x,'nota']<40 else '#F0A02A'}"></i></span>
          <span class="rw-v">{pt(saude.loc[x,'nota'])}</span>
          <span class="rw-q">{pt(saude.loc[x,'taxa_violacao']*100, 2)}% violação</span>
          <span class="sq">{ico('seta', 14)}</span></button>"""
          for j, x in enumerate(saude.index[-5:][::-1]))}
      </div>
      <div class="nt"><b>100 é o melhor dos dezessete</b>, não um produto sem problema. O pior é
        <b class="id">{pior}</b>, com <b>{pt(saude.loc[pior,'prop_inedito']*100, 0)}%</b> de
        problemas inéditos — e o inédito viola <b>4,6 vezes mais</b> que o rotineiro.</div>
    </div>

    <div class="cd" style="grid-column:1/-1">
      {cab('calendario', 'Carga por dia da semana',
           'Média de incidentes P3 por dia da semana no ano. A barra azul é o dia de hoje.')}
      <div class="sms">{barras_semana()}</div>
      <div class="nt">A diferença que existe é <b>dia útil contra fim de semana</b>, não segunda
        contra quinta: sábado cai a <b>{pt(SEMANA[5], 0)}</b> e domingo a <b>{pt(SEMANA[6], 0)}</b>
        contra <b>{pt(SEMANA[:5].mean(), 0)}</b> nos dias úteis. É por isso que o modelo usa dia da
        semana e feriado como sinal, e não a data em si.</div>
    </div>
  </div>
</div>

<div class="ov" id="ov" hidden><div class="md" id="md" role="dialog" aria-modal="true">
  <button class="md-x" id="mx" aria-label="fechar">{ico('fechar', 16)}</button>
  <div id="mc"></div>
</div></div>

<script>
const ATIVO={json.dumps(MOD_ATIVO, ensure_ascii=False)},
      INC={json.dumps(MOD_INC, ensure_ascii=False)},
      PROD={json.dumps(MOD_PROD, ensure_ascii=False)},
      MES={json.dumps(MES_LBL, ensure_ascii=False)},
      MEDIA={MEDIA_BASE};
['.cel','.sm','.dc','.mr'].forEach(s=>
  document.querySelectorAll(s).forEach((e,i)=>e.style.setProperty('--i',i)));

const ov=document.getElementById('ov'),mc=document.getElementById('mc');
const fecha=()=>ov.hidden=true;
document.getElementById('mx').onclick=fecha;
ov.onclick=e=>{{if(e.target===ov)fecha()}};
addEventListener('keydown',e=>{{if(e.key==='Escape')fecha()}});
const nb=v=>String(v).replace('.',',');

function barras(h){{
  if(!h.length)return '<p class="sub">Sem passagens registradas no período.</p>';
  const mx=Math.max(...h.map(m=>m.passagens))||1;
  return '<div class="hb">'+h.map(m=>`<div class="hb-c">
    <i style="--h:${{Math.max(m.passagens/mx*100,4)}}%">
      <u style="--v:${{m.passagens?m.violacoes/m.passagens*100:0}}%"></u></i>
    <span>${{MES[m.mes-1]}}</span></div>`).join('')+'</div>';
}}

function abre(tipo,k){{
  let h='';
  if(tipo==='ativo'){{
    const a=ATIVO[k],t=parseFloat(a.taxa.replace(',','.'));
    const tom=t>=10?'no':t>=1?'wn':'ok';
    h=`<span class="md-k">ativo de configuração</span>
      <h3 class="id">${{a.nome}}</h3>
      <p class="sub">${{a.pass}} incidentes elegíveis passaram por este ativo em 2025 até hoje.</p>
      <div class="md-g">
        <div class="md-s"><em>passagens</em><b>${{a.pass}}</b></div>
        <div class="md-s ${{tom}}"><em>violaram</em><b>${{a.viol}}</b></div>
        <div class="md-s ${{tom}}"><em>taxa</em><b>${{a.taxa}}%</b></div></div>
      <div class="md-h">histórico mês a mês</div>
      ${{barras(a.hist)}}
      <p class="sub" style="margin-top:10px">A barra cinza é o volume do mês.
        A parte vermelha embaixo é a fração que violou o prazo.</p>
      <div class="cx"><span class="chp t-ac">${{'{ico("balanca",18)}'}}</span>
        <p>Este ativo viola <b>${{a.x}} vezes mais</b> que a média da base, que é
        <b>${{nb(MEDIA)}}%</b>. O histórico do ativo é um dos sinais que o modelo usa para
        pontuar um incidente novo — por isso todo caso que passa por aqui já nasce com risco alto.</p></div>
      <div class="md-f"><button class="bt pr">${{'{ico("fila",15)}'}}Ver incidentes deste ativo</button>
        <button class="bt sc">${{'{ico("sino",15)}'}}Avisar quando abrir outro</button></div>`;
  }}
  if(tipo==='inc'){{
    const c=INC[k];
    h=`<span class="md-k">incidente em atendimento</span>
      <h3 class="id">${{c.id}}</h3>
      <p class="sub">${{c.produto}} · equipe ${{c.equipe}} · ativo
        <span class="id">${{c.ativo}}</span></p>
      <div class="md-g">
        <div class="md-s no"><em>risco</em><b>${{nb(c.risco)}}%</b></div>
        <div class="md-s"><em>no ativo</em><b>${{c.viol}}/${{c.pass}}</b></div>
        <div class="md-s"><em>vs média</em><b>${{Math.round(c.risco/MEDIA)}}x</b></div></div>
      <div class="cx"><span class="chp t-ac">${{'{ico("alvo",18)}'}}</span>
        <p>Em <b>100 casos parecidos com este</b>, o modelo espera que
        <b>${{c.em100}} estourem o prazo</b>. A média da base é ${{nb(MEDIA)}} em 100.</p></div>
      <div class="md-h">o que pesa neste caso</div>
      ${{c.sinais.map(([n,v])=>`<div class="sg"><span class="sg-t">${{n}}</span>
        <span class="sg-b"><i style="width:${{v/38*100}}%"></i></span>
        <span class="sg-v">${{v}}%</span></div>`).join('')}}
      <p class="sub" style="margin-top:8px">Peso relativo de cada sinal no escore deste
        incidente. A soma dá o risco acima.</p>
      <div class="md-f"><button class="bt pr">${{'{ico("pessoas",15)}'}}Escalar para a equipe</button>
        <button class="bt sc">${{'{ico("resolvido",15)}'}}Marcar como tratado</button></div>`;
  }}
  if(tipo==='prod'){{
    const p=PROD[k];
    h=`<span class="md-k">produto · posição ${{p.pos}} de 17</span>
      <h3 class="id">${{p.nome}}</h3>
      <p class="sub">${{p.quad}} · ${{p.inc}} incidentes elegíveis, ${{p.viol}} violaram o prazo.</p>
      <div class="md-g">
        <div class="md-s ${{parseFloat(p.nota)<40?'no':'wn'}}"><em>nota</em><b>${{p.nota}}</b></div>
        <div class="md-s"><em>posição</em><b>${{p.pos}}º</b></div>
        <div class="md-s"><em>incidentes</em><b>${{p.inc}}</b></div></div>
      <div class="md-h">os cinco componentes da nota</div>
      ${{p.comp.map(c=>`<div class="sg"><span class="sg-t">${{c.rot}}
        <span style="color:#5F697C"> ${{c.v}}${{c.u}}</span></span>
        <span class="sg-b"><i style="width:${{c.pos}}%;background:${{c.pos>66?'#F0483E':c.pos>33?'#F0A02A':'#22C08A'}}"></i></span>
        <span class="sg-v">${{c.pos}}</span></div>`).join('')}}
      <p class="sub" style="margin-top:8px">A barra mostra a posição relativa entre os 17
        produtos: quanto mais cheia, pior comparado aos outros. A nota é a média dessas posições.</p>
      <div class="cx"><span class="chp t-ac">${{'{ico("balanca",18)}'}}</span>
        <p>A nota é <b>relativa</b>: 100 seria o melhor dos dezessete em todos os cinco
        componentes, não um produto sem nenhum problema.</p></div>
      <div class="md-f"><button class="bt pr">${{'{ico("lupa",15)}'}}Ver causas deste produto</button>
        <button class="bt sc">${{'{ico("previsao",15)}'}}Comparar com outro</button></div>`;
  }}
  mc.innerHTML=h;ov.hidden=false;document.getElementById('md').scrollTop=0;
}}
document.querySelectorAll('[data-mod]').forEach(b=>
  b.onclick=()=>abre(b.dataset.mod,b.dataset.k));

// filtros
document.querySelectorAll('.fb').forEach(b=>b.onclick=()=>{{
  document.querySelectorAll(`.fb[data-g="${{b.dataset.g}}"]`).forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  if(b.dataset.g==='zona'){{
    const so=b.dataset.v==='risco';
    document.querySelectorAll('.cel').forEach(c=>
      c.classList.toggle('off',so&&!/z-(crit|alta)/.test(c.className)));
  }}
  if(b.dataset.g==='pri'){{
    document.querySelectorAll('.it').forEach(i=>
      i.style.display=b.dataset.v==='2'?'none':'flex');
  }}
}});
addEventListener('pointermove',e=>{{const c=e.target.closest?.('.cd');if(!c)return;
  const b=c.getBoundingClientRect();
  c.style.setProperty('--mx',(e.clientX-b.left)+'px');
  c.style.setProperty('--my',(e.clientY-b.top)+'px');}},{{passive:true}});
</script></body></html>'''

OUT.write_text(HTML, encoding='utf-8')
print(f'A: {OUT}')
