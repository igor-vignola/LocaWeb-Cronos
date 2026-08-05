# -*- coding: utf-8 -*-
"""Direcao C · Diagnostico.

Aposta: a tela nao mostra um painel, mostra **um caso por vez**. O heroi e o incidente
aberto de maior risco, com o modelo explicando como chegou naquele numero — cada sinal
votando, a confianca traduzida em frequencia ("em 100 casos parecidos, 56 estouram") e os
passos da analise numerados.

Escura. Assinatura: campo de linhas do proprio historico ao fundo.
Devices: como cada sinal votou e confianca em frequencia (clara-diagnostico-ia), anel com
fracao (plano), trilho lateral de casos, arco com zona nomeada (credify).
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dados import (ATIVOS, DIA_HOJE, ELEG_30, EM_ABERTO, FILA, HIST_ATIVO, HORAS, HORA_RISCO,
                   MEDIA_BASE, MES_LBL, ONTEM, SEM_VIOL, SINAIS, TAXA_30, TOTAL_VIOL, VIOL_30,
                   dm, mil, proj, pt, saude)
from fundo import CSS_CAMPO, campo
from icones import CSS_ICO, chip, ico

OUT = Path.cwd() / 'prototipos' / 'telas' / 'direcoes' / 'c-diagnostico.html'
OUT.parent.mkdir(parents=True, exist_ok=True)

FAIXAS = [(0, 1, 'rotina', 'ok'), (1, 5, 'atenção', 'wn'), (5, 10, 'alta', 'wn'),
          (10, 100, 'crítica', 'no')]
faixa_de = lambda v: next(f for f in FAIXAS if f[0] <= v < f[1])

# os passos que o modelo percorre, para a coluna de explicacao
PASSOS = [
    ('lupa', 'Lê o que existe na abertura',
     'produto, categoria, subcategoria, equipe, dia da semana, hora e histórico do ativo'),
    ('balanca', 'Compara cada sinal com a média do treino',
     'a contribuição é peso × (valor − média), então nada fica escondido'),
    ('tendencia', 'Soma as contribuições em um escore',
     'a soma passa pela curva logística e vira probabilidade'),
    ('alvo', 'Coloca o caso na fila',
     'a ordem é o produto: onde a operação para de descer é decisão dela'),
]


def cronometro(risco, tam=250):
    """Arco de risco com zonas nomeadas. A escala e logaritmica porque a base vive
    embaixo de 1% e o caso interessante vive em 50%."""
    c = tam / 2
    r = tam * .40
    esc = lambda v: min(math.log10(max(v, .1) * 10) / 3, 1)      # 0,1% -> 0 ; 100% -> 1
    ang = lambda v: esc(v) * 250 - 125
    pol = lambda aa, rr=r: (c + rr * math.sin(math.radians(aa)), c - rr * math.cos(math.radians(aa)))
    x1, y1 = pol(-125)
    x2, y2 = pol(125)
    xv, yv = pol(ang(risco))
    xm, ym = pol(ang(MEDIA_BASE))
    grande = 1 if ang(risco) - (-125) > 180 else 0
    zonas = ''.join(
        f'<path class="cr-z z-{k}" d="M{pol(ang(a))[0]:.1f} {pol(ang(a))[1]:.1f} '
        f'A{r} {r} 0 0 1 {pol(ang(min(b, 100)))[0]:.1f} {pol(ang(min(b, 100)))[1]:.1f}"/>'
        for a, b, _, k in FAIXAS)
    return f'''<div class="cr">
      <svg viewBox="0 0 {tam} {tam}">
        <path class="cr-t" d="M{x1:.1f} {y1:.1f} A{r} {r} 0 1 1 {x2:.1f} {y2:.1f}"/>
        {zonas}
        <path class="cr-v" d="M{x1:.1f} {y1:.1f} A{r} {r} 0 {grande} 1 {xv:.1f} {yv:.1f}"/>
        <line class="cr-md" x1="{c}" y1="{c}" x2="{xm:.1f}" y2="{ym:.1f}"/>
        <circle class="cr-p" cx="{xv:.1f}" cy="{yv:.1f}" r="7"/>
      </svg>
      <div class="cr-in"><b>{pt(risco)}<u>%</u></b>
        <span class="cr-f f-{faixa_de(risco)[3]}">faixa {faixa_de(risco)[2]}</span>
        <em>a média da base é {pt(MEDIA_BASE, 2)}%</em></div>
    </div>'''


def votos(sinais, tam=52):
    """Como cada sinal votou, no espirito de clara-diagnostico-ia."""
    mx = max(v for _, v in sinais)
    fora = []
    for j, (nome, v) in enumerate(sinais):
        r = tam / 2 - 4
        ci = 2 * math.pi * r
        forte = 'forte' if v >= 18 else ('medio' if v >= 10 else 'fraco')
        fora.append(f'''<div class="vt" style="--i:{j}">
          <svg class="vt-a t-{forte}" viewBox="0 0 {tam} {tam}" width="{tam}" height="{tam}">
            <circle class="vt-t" cx="{tam/2}" cy="{tam/2}" r="{r}"/>
            <circle class="vt-v" cx="{tam/2}" cy="{tam/2}" r="{r}" stroke-dasharray="{ci:.1f}"
              stroke-dashoffset="{ci:.1f}" style="--f:{ci*(1-v/mx):.1f}"/>
            <text x="{tam/2}" y="{tam/2+3.6}" text-anchor="middle">{v}</text></svg>
          <div class="vt-t2"><em class="v-{forte}">{forte}</em><b>{nome}</b>
            <span>{'puxa o risco para cima' if v >= 10 else 'contribui pouco'}</span></div>
        </div>''')
    return ''.join(fora)


def mini_hist(ativo, w=300, h=54):
    h_ = HIST_ATIVO.get(ativo, [])
    if not h_:
        return ''
    mx = max(m['passagens'] for m in h_) or 1
    lar = w / len(h_)
    barras = ''.join(
        f'<g><rect x="{i*lar+3:.1f}" y="{h - 16 - m["passagens"]/mx*(h-20):.1f}" '
        f'width="{lar-6:.1f}" height="{m["passagens"]/mx*(h-20):.1f}" rx="3" class="mh-p"/>'
        f'<rect x="{i*lar+3:.1f}" y="{h - 16 - (m["violacoes"]/mx*(h-20)):.1f}" '
        f'width="{lar-6:.1f}" height="{m["violacoes"]/mx*(h-20):.1f}" rx="3" class="mh-v"/></g>'
        for i, m in enumerate(h_))
    rot = ''.join(f'<text class="mh-l" x="{i*lar+lar/2:.1f}" y="{h - 2}">'
                  f'{MES_LBL[m["mes"]-1]}</text>' for i, m in enumerate(h_))
    return f'<svg class="mh" viewBox="0 0 {w} {h}">{barras}{rot}</svg>'


CASOS = {c['id']: {**{k: v for k, v in c.items() if k != 'taxa_ativo'},
                   'taxa_ativo': pt(c['taxa_ativo'], 1), 'em100': int(round(c['risco'])),
                   'faixa': faixa_de(c['risco'])[2], 'ftom': faixa_de(c['risco'])[3],
                   'hist': HIST_ATIVO.get(c['ativo'], [])} for c in FILA}
alvo = FILA[0]

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#06070B;--sf:#0D1017;--sf2:#141822;--ln:rgba(255,255,255,.07);
 --ln2:rgba(255,255,255,.15);--tx:#8E97A9;--tx2:#5F697C;--tx3:#414959;--hd:#F1F4F9;
 --ac:#3B7DFF;--no:#F0483E;--wn:#F0A02A;--ok:#22C08A;
 --e:cubic-bezier(.19,1,.22,1);--e2:cubic-bezier(.34,1.56,.64,1)}
html{-webkit-font-smoothing:antialiased;scroll-behavior:smooth}
body{background:var(--bg);color:var(--hd);min-height:100dvh;overflow-x:hidden;
 font-family:'Outfit',system-ui,sans-serif;font-size:15px;letter-spacing:-.011em}
.id{font-weight:600;letter-spacing:.055em;font-variant-numeric:tabular-nums lining-nums}
.sh{position:relative;z-index:1;max-width:1460px;margin:0 auto;padding:0 30px 80px}
/* topo */
.tp{display:flex;align-items:center;gap:14px;padding:16px 0;margin-bottom:8px;position:sticky;
 top:0;z-index:30;background:linear-gradient(180deg,rgba(6,7,11,.96) 58%,transparent);
 backdrop-filter:blur(8px)}
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
 box-shadow:inset 0 1px 0 rgba(255,255,255,.14)}
.pil button:disabled{opacity:.28;cursor:default}
.tp-r{margin-left:auto;display:flex;gap:8px}
.stl{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;color:var(--tx);
 background:rgba(255,255,255,.04);border:1px solid var(--ln);padding:7px 12px;border-radius:999px}
.stl i{width:6px;height:6px;border-radius:50%;background:var(--ok);
 box-shadow:0 0 0 3px rgba(34,192,138,.18);animation:pu 2.6s ease-in-out infinite}
@keyframes pu{50%{opacity:.32}}
/* layout: trilho de casos + caso aberto */
.lay{display:grid;grid-template-columns:300px 1fr;gap:18px;align-items:start}
.tri{position:sticky;top:78px;display:flex;flex-direction:column;gap:8px}
.tri-h{font-size:9.5px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;
 color:var(--tx2);display:flex;align-items:center;gap:8px;padding:0 4px 4px}
.tri-h .ic{color:var(--ac)}
.tri-h span{margin-left:auto;color:var(--tx3);letter-spacing:0;text-transform:none;
 font-weight:500;font-size:10.5px}
.cs{display:flex;align-items:center;gap:11px;background:var(--sf);border:1px solid var(--ln);
 border-radius:15px;padding:11px 13px;cursor:pointer;font:inherit;color:inherit;text-align:left;
 width:100%;transition:all .34s var(--e);animation:sl .5s var(--e) both;
 animation-delay:calc(var(--i)*60ms);position:relative;overflow:hidden}
@keyframes sl{from{opacity:0;transform:translateX(-12px)}}
.cs::before{content:'';position:absolute;inset:0 auto 0 0;width:3px;background:var(--ac);
 transform:scaleY(0);transform-origin:center;transition:transform .35s var(--e)}
.cs:hover{background:var(--sf2);border-color:var(--ln2)}
.cs.on{background:var(--sf2);border-color:rgba(59,125,255,.34)}
.cs.on::before{transform:scaleY(1)}
.cs-r{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;flex-shrink:0;
 font-size:13px;font-weight:700;letter-spacing:-.03em}
.cs-r.no{background:rgba(240,72,62,.17);color:#FF8B84}
.cs-r.wn{background:rgba(240,160,42,.16);color:#FFC176}
.cs-t{flex:1;min-width:0}
.cs-t b{font-size:13px;display:block}
.cs-t span{font-size:11px;color:var(--tx2);display:block;margin-top:1px}
/* caso aberto */
.caso{display:flex;flex-direction:column;gap:16px}
.cb{background:linear-gradient(166deg,var(--sf2),var(--sf));border:1px solid var(--ln);
 border-radius:24px;padding:22px 24px;position:relative;overflow:hidden;
 box-shadow:0 1px 0 rgba(255,255,255,.045) inset,0 24px 54px -32px #000}
.cb::after{content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;
 background:radial-gradient(340px 210px at var(--mx,50%) var(--my,0),rgba(59,125,255,.07),transparent 66%);
 opacity:0;transition:opacity .5s var(--e)}
.cb:hover::after{opacity:1}
.cb>*{position:relative;z-index:1}
.hdr{display:flex;align-items:flex-start;gap:13px;margin-bottom:16px}
.hdr-t{display:flex;gap:10px;flex:1;min-width:0}
.hdr-t .ic{color:var(--ac);margin-top:2px;flex-shrink:0}
.hdr h3{font-size:14.5px;font-weight:650;letter-spacing:-.022em}
.hdr p{font-size:11.5px;color:var(--tx2);margin-top:2px;line-height:1.45}
/* cabecalho do caso */
.ch2{display:grid;grid-template-columns:1fr auto;gap:32px;align-items:center}
.ch2 .kk{font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
 color:var(--ac);display:inline-flex;align-items:center;gap:7px}
.ch2 h1{font-size:40px;font-weight:650;letter-spacing:-.04em;margin-top:11px}
.ch2 .meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:13px}
.tg{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;color:var(--tx);
 background:rgba(255,255,255,.045);border:1px solid var(--ln);padding:6px 11px;border-radius:9px}
.tg .ic{opacity:.6;width:13px;height:13px}
.ch2 .frase{font-size:16px;color:#D5DCE8;line-height:1.6;margin-top:17px;max-width:56ch}
.ch2 .frase b{color:#fff;font-weight:650}
.ch2 .frase .cr2{color:#FF8B84;font-weight:650}
/* cronometro de risco */
.cr{position:relative;width:250px;flex-shrink:0}
.cr svg{width:100%;height:auto;overflow:visible}
.cr-t{fill:none;stroke:rgba(255,255,255,.06);stroke-width:13;stroke-linecap:round}
.cr-z{fill:none;stroke-width:3;opacity:.5;transform:translateY(19px);stroke-linecap:round}
.cr-z.z-ok{stroke:var(--ok)}.cr-z.z-wn{stroke:var(--wn)}.cr-z.z-no{stroke:var(--no)}
.cr-v{fill:none;stroke:url(#gr);stroke-width:13;stroke-linecap:round;stroke-dasharray:700;
 stroke-dashoffset:700;animation:dw 1.7s var(--e) .4s forwards}
.cr-md{stroke:#fff;stroke-width:1.4;stroke-dasharray:2 3;opacity:.42}
.cr-p{fill:#fff;opacity:0;animation:pn .5s var(--e2) 1.6s forwards;
 filter:drop-shadow(0 0 8px rgba(240,72,62,.7))}
.cr-in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
 justify-content:center;pointer-events:none;text-align:center;padding-top:14px}
.cr-in b{font-size:50px;font-weight:700;letter-spacing:-.055em;line-height:1;color:#fff}
.cr-in b u{font-size:22px;text-decoration:none;color:var(--tx2)}
.cr-f{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
 padding:3px 9px;border-radius:7px;margin-top:8px}
.cr-f.f-no{background:rgba(240,72,62,.16);color:#FF8B84}
.cr-f.f-wn{background:rgba(240,160,42,.16);color:#FFC176}
.cr-f.f-ok{background:rgba(34,192,138,.16);color:#3FD69B}
.cr-in em{font-size:10px;color:var(--tx3);font-style:normal;margin-top:5px}
/* a leitura em frequencia: cem quadradinhos */
.cem{display:grid;grid-template-columns:repeat(10,1fr);gap:5px;max-width:290px;
 margin-top:8px}
.cem i{aspect-ratio:1;border-radius:4px;background:rgba(255,255,255,.07);
 animation:pn .3s var(--e2) both;animation-delay:calc(var(--i)*7ms)}
.cem i.on{background:var(--no);box-shadow:0 0 9px rgba(240,72,62,.5)}
.cem-l{display:flex;gap:16px;margin-top:16px;font-size:11.5px;color:var(--tx2);
 flex-wrap:wrap;align-items:center}
.cem-l span{display:inline-flex;align-items:center;gap:6px}
.cem-l i{width:10px;height:10px;border-radius:3px}
/* votos dos sinais */
.vts{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.vt{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.028);
 border:1px solid var(--ln);border-radius:15px;padding:11px 13px;
 animation:sl .5s var(--e) both;animation-delay:calc(200ms + var(--i)*70ms)}
.vt-a .vt-t{fill:none;stroke:rgba(255,255,255,.08);stroke-width:4}
.vt-a .vt-v{fill:none;stroke-width:4;stroke-linecap:round;transform:rotate(-90deg);
 transform-origin:center;animation:ar 1.1s var(--e) .7s forwards}
.vt-a.t-forte .vt-v{stroke:#F0483E}.vt-a.t-medio .vt-v{stroke:#F0A02A}
.vt-a.t-fraco .vt-v{stroke:#5B93FF}
.vt-a text{fill:#fff;font-size:14px;font-weight:650;font-family:'Outfit',sans-serif}
@keyframes ar{to{stroke-dashoffset:var(--f)}}
.vt-t2{flex:1;min-width:0}
.vt-t2 em{font-size:9px;font-style:normal;font-weight:700;letter-spacing:.11em;
 text-transform:uppercase;display:block}
.v-forte{color:#FF8B84}.v-medio{color:#FFC176}.v-fraco{color:#7FA9FF}
.vt-t2 b{font-size:13px;font-weight:600;display:block;margin-top:2px;color:#E4EAF4}
.vt-t2 span{font-size:10.5px;color:var(--tx3);display:block}
/* passos numerados */
.ps{display:flex;flex-direction:column;gap:2px}
.pa{display:flex;gap:13px;padding:11px 0;position:relative}
.pa:not(:last-child)::before{content:'';position:absolute;left:16px;top:40px;bottom:-4px;
 width:1px;background:var(--ln)}
.pa-n{width:33px;height:33px;border-radius:11px;background:rgba(59,125,255,.13);
 border:1px solid rgba(59,125,255,.24);display:grid;place-items:center;flex-shrink:0;
 color:#7FA9FF;position:relative;z-index:1}
.pa-t b{font-size:13.5px;font-weight:600;display:block;color:#E4EAF4}
.pa-t span{font-size:11.5px;color:var(--tx2);display:block;margin-top:2px;line-height:1.5}
/* mini historico */
.mh{width:100%;height:auto;margin-top:8px}
.mh-p{fill:rgba(255,255,255,.13)}.mh-v{fill:#F0483E}
.mh-l{fill:var(--tx3);font-size:9.5px;text-anchor:middle;font-family:'Outfit',sans-serif}
/* comparacao */
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:4px}
.cmp div{background:rgba(255,255,255,.03);border:1px solid var(--ln);border-radius:15px;
 padding:14px 16px}
.cmp em{font-size:9.5px;font-style:normal;letter-spacing:.1em;text-transform:uppercase;
 color:var(--tx2);font-weight:700;display:block}
.cmp b{font-size:27px;font-weight:650;letter-spacing:-.04em;display:block;margin-top:6px;
 line-height:1}
.cmp span{font-size:11px;color:var(--tx3);display:block;margin-top:4px}
.cmp .no b{color:#FF8B84}.cmp .nt b{color:#95A0B4}
.nt2{font-size:11.5px;color:var(--tx2);line-height:1.62;margin-top:14px;padding-top:12px;
 border-top:1px solid var(--ln)}
.nt2 b{color:#C6D0E2;font-weight:600}
/* acoes */
.acs{display:flex;gap:9px;flex-wrap:wrap;margin-top:16px;padding-top:15px;
 border-top:1px solid var(--ln)}
.bt{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:12.5px;font-weight:600;
 padding:11px 16px;border-radius:12px;cursor:pointer;transition:all .3s var(--e)}
.bt.pr{background:var(--ac);border:1px solid var(--ac);color:#fff}
.bt.pr:hover{background:#2E6BE8;transform:translateY(-1px);box-shadow:0 10px 24px -10px rgba(59,125,255,.7)}
.bt.sc{background:rgba(255,255,255,.05);border:1px solid var(--ln);color:var(--tx)}
.bt.sc:hover{background:rgba(255,255,255,.1);color:#fff}
.bt:active{transform:scale(.98)}
@keyframes dw{to{stroke-dashoffset:0}}
@keyframes pn{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
@media (max-width:1080px){.lay{grid-template-columns:1fr}.tri{position:static}
 .ch2,.vts,.cmp{grid-template-columns:1fr}.cr{width:100%;max-width:250px}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}
 .cr-v{stroke-dashoffset:0!important}.cr-p{opacity:1!important}
 .cs,.vt,.cem i{opacity:1!important;transform:none!important}
 .vt-a .vt-v{stroke-dashoffset:var(--f)!important}
 .campo .cv{opacity:var(--o)!important;stroke-dashoffset:0!important}}
"""

HTML = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cronos · diagnóstico</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}{CSS_ICO}{CSS_CAMPO}</style></head><body>
{campo('#3B7DFF', .11)}
<svg width="0" height="0" style="position:absolute"><defs>
  <linearGradient id="gr" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0" stop-color="#3B7DFF"/><stop offset=".55" stop-color="#F0A02A"/>
    <stop offset="1" stop-color="#F0483E"/></linearGradient></defs></svg>
<div class="sh">
  <div class="tp">
    <div class="br"><div class="br-m"><svg viewBox="0 0 28 28" width="18" height="18" fill="none">
      <path d="M6 22L12 14L16 17L22 8" stroke="#0B0D13" stroke-width="2.6" stroke-linecap="round"
        stroke-linejoin="round"/><circle cx="22" cy="8" r="3" stroke="#2563EB" stroke-width="1.9"/>
      <circle cx="22" cy="8" r="1.3" fill="#2563EB"/></svg></div>
      <div><b>Cronos</b><em>VEJA ANTES · AJA ANTES</em></div></div>
    <div class="pil">
      <button>{ico('grade', 15)}Painel</button>
      <button class="on">{ico('lupa', 15)}Diagnóstico</button>
      <button>{ico('coracao', 15)}Saúde</button>
      <button disabled>{ico('previsao', 15)}Volume</button></div>
    <div class="tp-r"><span class="stl"><i></i>{mil(EM_ABERTO)} em atendimento</span>
      <span class="stl">{ico('relogio', 14)}{dm(DIA_HOJE)} · 07h00</span></div>
  </div>

  <div class="lay">
    <div class="tri">
      <div class="tri-h">{ico('fila', 14)}fila de hoje<span>{len(FILA)} casos</span></div>
      {"".join(f"""<button class="cs{' on' if j == 0 else ''}" data-c="{c['id']}" style="--i:{j}">
        <span class="cs-r {'no' if c['risco'] >= 40 else 'wn'}">{pt(c['risco'], 0)}%</span>
        <span class="cs-t"><b class="id">{c['id']}</b>
          <span>{c['produto']} · {c['equipe']}</span></span></button>"""
        for j, c in enumerate(FILA))}
      <div class="tri-h" style="margin-top:14px">{ico('balanca', 14)}referência</div>
      <div class="cs" style="--i:7;cursor:default">
        <span class="cs-r wn" style="background:rgba(255,255,255,.06);color:#95A0B4">1%</span>
        <span class="cs-t"><b>Média da base</b>
          <span>{pt(MEDIA_BASE, 2)}% em {mil(ELEG_30 * 0 + 19973)} elegíveis</span></span></div>
    </div>

    <div class="caso">
      <div class="cb">
        <div class="ch2">
          <div>
            <span class="kk">{ico('alerta', 14)}caso de maior risco na fila de hoje</span>
            <h1 class="id" id="c-id">{alvo['id']}</h1>
            <div class="meta" id="c-meta">
              <span class="tg">{ico('produto', 13)}{alvo['produto']}</span>
              <span class="tg">{ico('pessoas', 13)}{alvo['equipe']}</span>
              <span class="tg">{ico('ativo', 13)}<span class="id">{alvo['ativo']}</span></span>
              <span class="tg">{ico('prazo', 13)}aberto há 4h</span>
            </div>
            <p class="frase" id="c-frase">O modelo estima <b>{pt(alvo['risco'])}% de chance</b> de
              este incidente estourar o prazo. A média da base é {pt(MEDIA_BASE, 2)}%, então este
              caso é <span class="cr2">{int(round(alvo['risco']/MEDIA_BASE))} vezes</span> mais
              provável que o incidente comum.</p>
          </div>
          <div id="c-cr">{cronometro(alvo['risco'])}</div>
        </div>
      </div>

      <div class="cb">
        <div class="hdr"><div class="hdr-t">{ico('pessoas', 16)}
          <div><h3>O que isso quer dizer, em cem casos</h3>
            <p>Cada quadrado é um incidente parecido com este. Os vermelhos são os que o modelo
              espera que estourem o prazo.</p></div></div></div>
        <div class="cem" id="c-cem">{"".join(
          f'<i class="{"on" if k < round(alvo["risco"]) else ""}" style="--i:{k}"></i>'
          for k in range(100))}</div>
        <div class="cem-l">
          <span><i style="background:#F0483E"></i>estouram o prazo</span>
          <span><i style="background:rgba(255,255,255,.1)"></i>fecham dentro</span>
          <span style="margin-left:auto">no incidente comum da base, seria
            <b style="color:#C6D0E2">1 em 100</b></span></div>
      </div>

      <div class="cb">
        <div class="hdr"><div class="hdr-t">{ico('balanca', 16)}
          <div><h3>Como cada sinal votou</h3>
            <p>Peso relativo de cada informação disponível na abertura. A soma das contribuições
              é o escore que virou a porcentagem acima.</p></div></div></div>
        <div class="vts" id="c-vts">{votos(SINAIS)}</div>
        <div class="nt2">Nenhum sinal decide sozinho. O que empurra este caso é a combinação de
          <b>categoria</b> com <b>produto</b> e o <b>histórico do ativo</b> — e é por isso que
          casos do mesmo ativo aparecem juntos no topo da fila.</div>
      </div>

      <div class="cb">
        <div class="hdr"><div class="hdr-t">{ico('ativo', 16)}
          <div><h3>O histórico do ativo <span class="id" id="c-at">{alvo['ativo']}</span></h3>
            <p>Barra clara é o volume do mês, a parte vermelha é quanto violou o prazo.</p></div>
          </div></div>
        <div id="c-mh">{mini_hist(alvo['ativo'], w=760, h=92)}</div>
        <div class="cmp" style="margin-top:14px">
          <div class="no"><em>este ativo</em><b id="c-tx">{pt(alvo['taxa_ativo'], 1)}%</b>
            <span id="c-hh">{alvo['viol']} de {alvo['pass']} passagens violaram</span></div>
          <div class="nt"><em>média da base</em><b>{pt(MEDIA_BASE, 2)}%</b>
            <span>{TOTAL_VIOL} de 19.973 incidentes elegíveis</span></div>
        </div>
        <div class="nt2">O histórico do ativo é um dos sinais do modelo. Um ativo que já falhou
          muito faz qualquer incidente novo nascer com risco alto — mesmo que o incidente em si
          pareça banal.</div>
      </div>

      <div class="cb">
        <div class="hdr"><div class="hdr-t">{ico('lupa', 16)}
          <div><h3>Como o modelo chegou aqui</h3>
            <p>Quatro passos, sem caixa-preta. Regressão logística treinada em 2025, com
              validação fora da amostra.</p></div></div></div>
        <div class="ps">
          {"".join(f'''<div class="pa"><span class="pa-n">{ico(i, 16)}</span>
            <div class="pa-t"><b>{t}</b><span>{d}</span></div></div>'''
            for i, t, d in PASSOS)}
        </div>
        <div class="nt2">Escolhemos logística em vez de XGBoost porque ela mantém a calibração:
          prevê <b>48,1 quebras onde houve 50</b>. O XGBoost com peso de classe previa 1.007 e
          inviabilizava a projeção do ano.</div>
        <div class="acs">
          <button class="bt pr">{ico('pessoas', 15)}Escalar para {alvo['equipe']}</button>
          <button class="bt sc">{ico('sino', 15)}Avisar quando passar de 60%</button>
          <button class="bt sc">{ico('resolvido', 15)}Marcar como tratado</button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
const C={json.dumps(CASOS, ensure_ascii=False)},MEDIA={MEDIA_BASE},
      MES={json.dumps(MES_LBL, ensure_ascii=False)};
const nb=v=>String(v).replace('.',',');
const q=s=>document.getElementById(s);

function pinta(k){{
  const c=C[k];
  q('c-id').textContent=c.id;
  q('c-at').textContent=c.ativo;
  q('c-tx').textContent=c.taxa_ativo+'%';
  q('c-hh').textContent=c.viol+' de '+c.pass+' passagens violaram';
  q('c-frase').innerHTML='O modelo estima <b>'+nb(c.risco)+'% de chance</b> de este incidente '+
    'estourar o prazo. A média da base é '+nb(MEDIA)+'%, então este caso é '+
    '<span class="cr2">'+Math.round(c.risco/MEDIA)+' vezes</span> mais provável que o '+
    'incidente comum.';
  q('c-meta').children[0].innerHTML=q('c-meta').children[0].innerHTML
    .replace(/(<\\/svg>).*$/,'$1'+c.produto);
  q('c-meta').children[1].innerHTML=q('c-meta').children[1].innerHTML
    .replace(/(<\\/svg>).*$/,'$1'+c.equipe);
  q('c-meta').children[2].innerHTML=q('c-meta').children[2].innerHTML
    .replace(/(<\\/svg>).*$/,'$1<span class="id">'+c.ativo+'</span>');
  // cem quadradinhos
  const alvo=Math.round(c.risco);
  [...q('c-cem').children].forEach((e,i)=>e.classList.toggle('on',i<alvo));
  // cronometro: refaz o arco
  const cr=q('c-cr').querySelector('.cr-in');
  cr.querySelector('b').innerHTML=nb(c.risco)+'<u>%</u>';
  const f=cr.querySelector('.cr-f');
  f.textContent='faixa '+c.faixa;f.className='cr-f f-'+c.ftom;
  const arco=q('c-cr').querySelector('.cr-v');
  const esc=v=>Math.min(Math.log10(Math.max(v,.1)*10)/3,1);
  const R=100,cc=125,ang=esc(c.risco)*250-125;
  const pol=a=>[cc+R*Math.sin(a*Math.PI/180),cc-R*Math.cos(a*Math.PI/180)];
  const [x1,y1]=pol(-125),[xv,yv]=pol(ang);
  arco.setAttribute('d',`M${{x1.toFixed(1)}} ${{y1.toFixed(1)}} A${{R}} ${{R}} 0 ${{ang+125>180?1:0}} 1 ${{xv.toFixed(1)}} ${{yv.toFixed(1)}}`);
  const pt2=q('c-cr').querySelector('.cr-p');
  pt2.setAttribute('cx',xv.toFixed(1));pt2.setAttribute('cy',yv.toFixed(1));
  // mini historico
  const h=c.hist,mx=Math.max(...h.map(m=>m.passagens))||1,W=760,H=92,lar=W/h.length;
  q('c-mh').innerHTML=`<svg class="mh" viewBox="0 0 ${{W}} ${{H}}">`+h.map((m,i)=>
    `<g><rect x="${{(i*lar+3).toFixed(1)}}" y="${{(H-16-m.passagens/mx*(H-20)).toFixed(1)}}"
      width="${{(lar-6).toFixed(1)}}" height="${{(m.passagens/mx*(H-20)).toFixed(1)}}" rx="3" class="mh-p"/>
    <rect x="${{(i*lar+3).toFixed(1)}}" y="${{(H-16-m.violacoes/mx*(H-20)).toFixed(1)}}"
      width="${{(lar-6).toFixed(1)}}" height="${{(m.violacoes/mx*(H-20)).toFixed(1)}}" rx="3" class="mh-v"/></g>
    <text class="mh-l" x="${{(i*lar+lar/2).toFixed(1)}}" y="${{H-2}}">${{MES[m.mes-1]}}</text>`).join('')+'</svg>';
  document.querySelectorAll('.bt.pr')[0].innerHTML=
    document.querySelectorAll('.bt.pr')[0].innerHTML.replace(/Escalar para \\w+/,'Escalar para '+c.equipe);
}}
document.querySelectorAll('.cs[data-c]').forEach(b=>b.onclick=()=>{{
  document.querySelectorAll('.cs').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');pinta(b.dataset.c);
  scrollTo({{top:0,behavior:'smooth'}});
}});
addEventListener('pointermove',e=>{{const c=e.target.closest?.('.cb');if(!c)return;
  const b=c.getBoundingClientRect();
  c.style.setProperty('--mx',(e.clientX-b.left)+'px');
  c.style.setProperty('--my',(e.clientY-b.top)+'px');}},{{passive:true}});
</script></body></html>'''

OUT.write_text(HTML, encoding='utf-8')
print(f'C: {OUT}')
