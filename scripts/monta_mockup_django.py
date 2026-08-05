# -*- coding: utf-8 -*-
"""Cronos · aplicacao. v5 escrita do zero.
Assinatura: trilho de tempo (ontem/agora/previsto) derivado da marca.
Mono apenas em identificador; numero em Geist com tabular-nums."""
import json
from pathlib import Path

import pandas as pd

RAIZ = Path.cwd()
DI = RAIZ / 'data' / 'interim'
OUT = RAIZ / 'prototipos' / 'telas' / 'django-mockup.html'

pt = lambda v, c=1: f'{v:.{c}f}'.replace('.', ',')
mil = lambda v: f'{int(v):,}'.replace(',', '.')

causas = pd.read_parquet(DI / '05_causas.parquet').head(5)
recor = pd.read_parquet(DI / '05_recorrentes.parquet').head(5)
grupos = pd.read_parquet(DI / '05_grupos_criticos.parquet').sort_values('taxa %', ascending=False).head(4)
prev = pd.read_parquet(DI / '03_previsao_diaria.parquet').sort_values('dia')
po = pd.read_parquet(DI / '06_projecao.parquet')
po = po[po['corte'] == pd.Timestamp('2025-10-01')].set_index('prioridade')
saude = pd.read_parquet(DI / '07_saude_produto.parquet').sort_values('posicao')

FILA = [('INC8595245', 56.1, 'Team11', 'lsin', 'IC00840', 21, 66),
        ('INC8607669', 50.4, 'Team11', 'lsin', 'IC00840', 21, 66),
        ('INC8579361', 47.2, 'Team11', 'lsin', 'IC00840', 21, 66),
        ('INC8599520', 42.9, 'Team11', 'lsin', 'IC00840', 21, 66),
        ('INC8601345', 40.4, 'Team11', 'lsin', 'IC00840', 21, 66),
        ('INC8614082', 33.1, 'Team07', 'lhco', 'IC01285', 30, 478)]
PESOS = [('categoria cat31', 38), ('produto lsin', 19), ('subcategoria sub388', 12),
         ('equipe Team11', 11), ('sábado, 19h', 8)]
P3 = prev[prev['prioridade'] == 'P3'].reset_index(drop=True)
P2 = prev[prev['prioridade'] == 'P2'].reset_index(drop=True)
ONTEM_P3 = P3[P3['tipo'] == 'realizado']['valor'].iloc[-1]
HOJE_P3 = P3[P3['tipo'] == 'previsto'].iloc[0]
HOJE_P2 = P2[P2['tipo'] == 'previsto'].iloc[0]
DIA_ONTEM = P3[P3['tipo'] == 'realizado']['dia'].iloc[-1]
DIA_HOJE = HOJE_P3['dia']

I = {'grid': '<rect x="3.5" y="3.5" width="7" height="7" rx="2"/><rect x="13.5" y="3.5" width="7" height="7" rx="2"/><rect x="3.5" y="13.5" width="7" height="7" rx="2"/><rect x="13.5" y="13.5" width="7" height="7" rx="2"/>',
     'target': '<circle cx="12" cy="12" r="8.6"/><circle cx="12" cy="12" r="4.3"/><circle cx="12" cy="12" r="1.2" fill="currentColor" stroke="none"/>',
     'heart': '<path d="M12 20s-6.8-4.5-6.8-9.3A3.9 3.9 0 0 1 12 8.2a3.9 3.9 0 0 1 6.8 2.5C18.8 15.5 12 20 12 20z"/>',
     'search': '<circle cx="10.8" cy="10.8" r="6.2"/><path d="M15.4 15.4L20.4 20.4"/>',
     'trend': '<path d="M3 17l5-5 4 3 6-8"/><path d="M15 7h6v6"/>',
     'arrow': '<path d="M5 12h13M13 6.5l6 5.5-6 5.5"/>',
     'bell': '<path d="M6 9.4a6 6 0 0 1 12 0c0 4.8 2 5.8 2 5.8H4s2-1 2-5.8z"/><path d="M10.2 19.4a2.3 2.3 0 0 0 3.6 0"/>'}
ic = lambda k, c='i': f'<span class="{c}"><svg viewBox="0 0 24 24">{I[k]}</svg></span>'


def spark(serie, n_real=18, n_prev=8, w=1000, h=132):
    """Trilho de tempo: o realizado em linha cheia, o previsto pontilhado com a banda de 80%.
    A divisao entre os dois e o 'agora' — a leitura que da nome ao produto."""
    real = serie[serie['tipo'] == 'realizado'].tail(n_real).reset_index(drop=True)
    fut = serie[serie['tipo'] == 'previsto'].head(n_prev).reset_index(drop=True)
    esc = [*real['valor'], *fut['valor'], *fut['baixo'], *fut['alto']]
    lo, hi = min(esc), max(esc)
    vao = (hi - lo) or 1
    n = len(real) + len(fut)
    px = lambda i: 5 + i / (n - 1) * (w - 10)
    py = lambda v: h - 20 - (v - lo) / vao * (h - 44)

    p_real = [(px(i), py(v)) for i, v in enumerate(real['valor'])]
    corte = p_real[-1]
    p_fut = [corte] + [(px(len(real) + i), py(v)) for i, v in enumerate(fut['valor'])]
    linha = lambda ps: 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in ps)

    altos = [(px(len(real) + i), py(v)) for i, v in enumerate(fut['alto'])]
    baixos = [(px(len(real) + i), py(v)) for i, v in enumerate(fut['baixo'])]
    banda = (f'M{corte[0]:.1f} {corte[1]:.1f} L'
             + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in altos) + ' L'
             + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(baixos)) + ' Z')
    area = linha(p_real) + f' L{corte[0]:.1f} {h} L5 {h} Z'
    return (f'<svg class="spk" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">'
            f'<defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#1E52D6" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="#1E52D6" stop-opacity="0"/></linearGradient></defs>'
            f'<path class="spk-a" d="{area}" fill="url(#sg)"/>'
            f'<path class="spk-bd" d="{banda}"/>'
            f'<line class="spk-ag" x1="{corte[0]:.1f}" y1="6" x2="{corte[0]:.1f}" y2="{h - 8}"/>'
            f'<path class="spk-l" d="{linha(p_real)}"/>'
            f'<path class="spk-f" d="{linha(p_fut)}"/>'
            f'<circle class="spk-h" cx="{corte[0]:.1f}" cy="{corte[1]:.1f}" r="9"/>'
            f'<circle class="spk-n" cx="{corte[0]:.1f}" cy="{corte[1]:.1f}" r="3.6"/></svg>')


def num(v, casas=1, suf=''):
    """Numero com contagem na entrada. O valor final fica no data para o JS."""
    return f'<span class="n" data-n="{v}" data-c="{casas}">{pt(v, casas)}</span>{suf}'


def trilho():
    d = lambda t: f'{t.day:02d}/{t.month:02d}'
    cut = (5 + 17 / 25 * 990) / 10          # em % da largura, mesma conta do spark
    return f'''<div class="rail" data-rev style="--cut:{cut:.1f}%">
      <div class="rail-h">
        <span class="rail-t">P3 · elegíveis por dia</span>
        <div class="rail-m">
          <span class="m ok"><i></i>ontem <b>{num(ONTEM_P3, 0)}</b></span>
          <span class="m ac"><i></i>previsto hoje <b>{num(HOJE_P3['valor'])}</b></span>
          <span class="m dim"><i></i>faixa <b>{pt(HOJE_P3['baixo'], 0)} a {pt(HOJE_P3['alto'], 0)}</b></span>
        </div>
      </div>
      {spark(P3)}
      <div class="rail-x"><span>18 dias observados</span>
        <span class="agora">{d(DIA_HOJE)} · agora</span>
        <span>8 dias previstos</span></div>
    </div>'''


def meta(p):
    r = po.loc[p]
    dentro = r['situação projetada'] == 'dentro da meta'
    lim = r['meta máxima']
    esc = lim * 1.3
    return f'''<div class="mt" data-rev>
      <div class="mt-h"><span class="mt-p">{p}</span>
        <span class="mt-v {'ok' if dentro else 'no'}">{num(r['projeção'])}</span>
        <span class="mt-l">de {int(lim)}</span>
        <span class="tag {'ok' if dentro else 'no'}">{'dentro' if dentro else 'acima'}</span></div>
      <div class="mt-b">
        <s class="{'ok' if dentro else 'no'}" style="left:{r['faixa baixa']/esc*100:.1f}%;
          width:{(r['faixa alta']-r['faixa baixa'])/esc*100:.1f}%"></s>
        <i class="{'ok' if dentro else 'no'}" style="left:{r['projeção']/esc*100:.1f}%"></i>
        <u style="left:{lim/esc*100:.1f}%"></u></div>
      <div class="mt-f">a barra é a faixa de {pt(r['faixa baixa'],0)} a {pt(r['faixa alta'],0)} ·
        o traço fino é a projeção · a meta é {int(lim)}</div>
    </div>'''


def painel():
    piores = saude.index[-4:][::-1]
    lat = saude[saude['quadrante'] == 'risco latente'].sort_values('prop_inedito', ascending=False).head(3)
    return f'''
    {trilho()}
    <div class="grid g-p">
      <article class="c c-a" data-rev style="--d:0">
        <h3 class="lb">Projeção do ano contra a meta</h3>
        {meta('P2')}{meta('P3')}
        <p class="nt">A projeção soma o que já fechou, o risco da fila em aberto e o volume ainda por
          entrar. Em três das dez projeções testadas o traço cruzaria a meta sem que o ano cruzasse.</p>
      </article>

      <article class="c c-b" data-rev style="--d:1">
        <div class="lb-r"><h3 class="lb">Início da fila de risco</h3>
          <button class="lk" data-go="fila">fila completa{ic('arrow','i xs')}</button></div>
        <ol class="fq">
          {"".join(f'''<li style="--d:{j}"><span class="fq-o">{j+1}</span>
            <span class="fq-i"><b class="mono">{n}</b><em>{eq} · {pr} · ativo {at}</em></span>
            <span class="fq-v">{num(v)}<small>%</small></span></li>'''
            for j, (n, v, eq, pr, at, q, t) in enumerate(FILA[:5]))}
        </ol>
        <p class="nt">Os cinco primeiros estão no mesmo ativo. Nos cinquenta primeiros da fila estão
          <b>15 das 50</b> violações do período.</p>
      </article>

      <article class="c c-c" data-rev style="--d:2">
        <h3 class="lb">Na fila de hoje</h3>
        <div class="kd"><span class="kv no">{num(4, 0)}</span>
          <span class="kl">com risco acima de 10%<em>faixa em que o modelo mais acerta</em></span></div>
        <div class="kd"><span class="kv">{num(1129, 0)}</span>
          <span class="kl">em atendimento<em>abertos e não resolvidos</em></span></div>
        <p class="nt">A média da base é <b>0,97%</b>. Um risco de 10% é dez vezes essa média, e é por
          isso que a faixa alta tem poucos casos e merece atenção.</p>
      </article>

      <article class="c c-d" data-rev style="--d:3">
        <div class="lb-r"><h3 class="lb">Piores notas de saúde</h3>
          <button class="lk" data-go="saude">ranking{ic('arrow','i xs')}</button></div>
        {"".join(f'''<div class="sr" style="--d:{j}"><span class="sr-p mono">{x}</span>
          <span class="sr-b"><i style="--w:{saude.loc[x,'nota']:.0f}%;--c:{'#DC2626' if saude.loc[x,'nota']<40 else '#C2751A'}"></i></span>
          <span class="sr-v">{num(saude.loc[x,'nota'])}</span></div>''' for j, x in enumerate(piores))}
      </article>

      <article class="c c-e" data-rev style="--d:4">
        <h3 class="lb">Risco latente</h3>
        <p class="ex">Muito problema novo e violação ainda baixa. O inédito viola <b>4,6 vezes mais</b>,
          então estes produtos carregam exposição que não se materializou.</p>
        <div class="lt-r">
          {"".join(f'''<div class="lt" style="--d:{j}"><b class="mono">{x}</b>
            <span>{num(r['prop_inedito']*100)}% novos</span>
            <em>violação {num(r['taxa_violacao']*100, 2)}%</em></div>'''
            for j, (x, r) in enumerate(lat.iterrows()))}
        </div>
      </article>
    </div>'''


def fila():
    return f'''
    <div class="grid g-f">
      <article class="c c-a" data-rev style="--d:0">
        <div class="lb-r"><h3 class="lb">Fila ordenada por risco</h3>
          <span class="ct">5.183 incidentes do período</span></div>
        <p class="ex">Os seis primeiros caem todos na faixa acima de 10%, onde estão os casos em que
          o modelo mais acerta. A operação decide onde parar de descer a lista.</p>
        <table class="tb"><thead><tr><th></th><th>Incidente</th><th>Risco</th>
          <th>Equipe</th><th>Produto</th><th>Ativo</th><th>Histórico do ativo</th></tr></thead><tbody>
          {"".join(f'''<tr style="--d:{j}" class="{'hi' if j==0 else ''}">
            <td class="o">{j+1}</td><td><b class="mono">{n}</b></td>
            <td class="rc"><span class="rb"><i style="--w:{v/56.1*100:.0f}%"></i></span>{num(v)}<small>%</small></td>
            <td class="dm">{eq}</td><td class="dm">{pr}</td><td class="dm mono">{at}</td>
            <td class="dm">{q} de {t} violaram</td></tr>'''
            for j, (n, v, eq, pr, at, q, t) in enumerate(FILA))}
        </tbody></table>
        <p class="nt">Onde parar é decisão da operação. Nos cinquenta primeiros há <b>15 das 50</b>
          violações, contra <b>6</b> da melhor regra simples e <b>1</b> da ordenação por prioridade.</p>
      </article>

      <article class="c c-b" data-rev style="--d:1">
        <h3 class="lb">Detalhe · <b class="mono">{FILA[0][0]}</b></h3>
        <div class="bg-r"><span class="bg-v">{num(FILA[0][1])}<small>%</small></span>
          <span class="bg-l">risco estimado<em>a média da base é 0,97%</em></span></div>
        <div class="rt"><i style="--w:{FILA[0][1]:.0f}%"></i><u style="left:0.97%"></u></div>
        <div class="ev">{ic('search','i sm')}<p>Dos <b>{FILA[0][6]}</b> incidentes do ativo
          <b class="mono">{FILA[0][4]}</b>, <b>{FILA[0][5]} violaram</b> o prazo.</p></div>
        <h3 class="lb mt2">O que pesa neste caso</h3>
        {"".join(f'''<div class="pw" style="--d:{j}"><span>{n}</span>
          <span class="pb"><i style="--w:{v/38*100:.0f}%"></i></span>
          <b>{num(v, 0)}%</b></div>''' for j, (n, v) in enumerate(PESOS))}
      </article>

      <article class="c c-c" data-rev style="--d:2">
        <h3 class="lb">Grupos críticos</h3>
        <table class="tb sm"><thead><tr><th>Produto · categoria · prioridade</th><th>Taxa</th>
          <th>vs média</th></tr></thead><tbody>
          {"".join(f'''<tr style="--d:{j}"><td class="mono">{r['grupo']}</td>
            <td class="no">{num(r['taxa %'], 2)}%</td>
            <td class="dm">{num(r['vezes a média'], 2)}x</td></tr>'''
            for j, (_, r) in enumerate(grupos.iterrows()))}</tbody></table>
        <p class="nt">Sete grupos concentram <b>13%</b> das violações em <b>5%</b> da base. O modelo
          concentra <b>72%</b> nos vinte por cento de maior risco.</p>
      </article>
    </div>'''


def tela_saude():
    # o nome do quadrante e longo demais para caber na coluna: rotulo curto na celula,
    # nome completo no title
    QT = {'risco latente': ('wn', 'latente'), 'problema já materializado': ('no', 'materializado'),
          'problema conhecido e recorrente': ('ac', 'recorrente'), 'estável': ('ok', 'estável')}
    return f'''
    <div class="grid g-s">
      <article class="c c-a" data-rev style="--d:0">
        <div class="lb-r"><h3 class="lb">Nota por produto</h3>
          <span class="ct">17 produtos · 95% do volume</span></div>
        <table class="tb"><thead><tr><th></th><th>Produto</th><th>Nota</th><th>Situação</th>
          <th>Incidentes</th><th>Violação</th><th>Novos</th></tr></thead><tbody>
          {"".join(f'''<tr style="--d:{j}"><td class="o">{int(r['posicao'])}</td>
            <td><b class="mono">{x}</b></td>
            <td class="rc"><span class="rb"><i style="--w:{r['nota']:.0f}%;--c:{'#DC2626' if r['nota']<40 else ('#C2751A' if r['nota']<65 else '#0F8A4C')}"></i></span>{num(r['nota'])}</td>
            <td><span class="tag {QT[r['quadrante']][0]}"
              title="{r['quadrante']}">{QT[r['quadrante']][1]}</span></td>
            <td class="dm">{mil(r['incidentes'])}</td>
            <td class="no">{num(r['taxa_violacao']*100, 2)}%</td>
            <td class="dm">{num(r['prop_inedito']*100)}%</td></tr>'''
            for j, (x, r) in enumerate(saude.iterrows()))}</tbody></table>
        <p class="nt">Nota por posição relativa: <b>100 é o melhor dos dezessete</b>, não um produto
          sem problemas. A linha abre a decomposição nos cinco componentes.</p>
      </article>
    </div>'''


def causas_tela():
    return f'''
    <div class="grid g-c">
      <article class="c c-a" data-rev style="--d:0">
        <h3 class="lb">Causas · volume não é risco</h3>
        <table class="tb sm"><thead><tr><th>Causa de fechamento</th><th>% base</th>
          <th>% violações</th><th>Taxa</th><th>vs média</th></tr></thead><tbody>
          {"".join(f'''<tr style="--d:{j}"><td>{r['Código de fechamento']}</td>
            <td class="dm">{num(r['% da base'])}%</td>
            <td class="no">{num(r['% das quebras'])}%</td>
            <td>{num(r['taxa de quebra %'], 2)}%</td>
            <td class="dm">{num(r['vezes a média'], 2)}x</td></tr>'''
            for j, (_, r) in enumerate(causas.iterrows()))}</tbody></table>
        <p class="nt"><b>Outro</b> responde por 7,8% do volume e 21,8% das violações. Campo preenchido
          no fechamento: serve a diagnóstico, não a previsão.</p>
      </article>
      <article class="c c-b" data-rev style="--d:1">
        <h3 class="lb">Problemas que mais repetem</h3>
        {"".join(f'''<div class="rc2" style="--d:{j}">
          <span class="rc2-t mono">{r['problema'][:44]}</span>
          <span class="rc2-m"><b>{mil(r['incidentes'])}</b> vezes · <b>{int(r['ativos'])}</b> ativos ·
            <b class="{'no' if r['quebras'] else 'ok'}">{int(r['quebras'])}</b> violações</span></div>'''
          for j, (_, r) in enumerate(recor.iterrows()))}
        <p class="nt">Os vinte mais recorrentes cobrem <b>26%</b> do volume e violam <b>0,40%</b>,
          menos da metade da média. Candidatos a automação de resposta.</p>
      </article>
    </div>'''


TELAS = {'painel': ('Painel', 'grid', painel()), 'fila': ('Fila de risco', 'target', fila()),
         'saude': ('Saúde por produto', 'heart', tela_saude()),
         'causas': ('Causas e recorrentes', 'search', causas_tela())}

nav = "".join(f'''<button class="nv{' on' if k=='painel' else ''}" data-t="{k}" style="--d:{j}">
  {ic(ic_)}<span>{nm}</span></button>''' for j, (k, (nm, ic_, _)) in enumerate(TELAS.items()))
nav += f'''<button class="nv off" disabled style="--d:4">{ic('trend')}
  <span>Previsão de volume</span><em>fase 2</em></button>'''

modal = f'''<div class="ov" id="ov"><div class="md" role="dialog" aria-label="Resumo do dia">
  <div class="md-t"><span class="md-s">{DIA_HOJE.day:02d}/{DIA_HOJE.month:02d}/{DIA_HOJE.year} · 07h00</span>
    <span class="ct">redação automática</span></div>
  <h2 class="md-h">Situação da operação<br><span class="mu">em três pontos</span></h2>
  <div class="md-b">
    <p><em>Ontem</em> entraram <b>84</b> incidentes elegíveis, <b>{pt(ONTEM_P3, 0)}</b> no P3 e
       <b>19</b> no P2, dentro do padrão de dia útil.</p>
    <p><em>Hoje</em> a previsão é de <b>{pt(HOJE_P3['valor'], 0)}</b> no P3 e
       <b>{pt(HOJE_P2['valor'], 0)}</b> no P2. A fila começa com
       <b class="mono">{FILA[0][0]}</b>, no ativo <b class="mono">{FILA[0][4]}</b>, que já acumula
       <b>{FILA[0][5]} violações em {FILA[0][6]}</b> passagens. Quatro casos estão acima de 10%.</p>
    <p><em>Atenção</em> ao P3: a projeção de fechamento está em <b>{pt(po.loc['P3','projeção'])}</b>
       contra meta de <b>{int(po.loc['P3','meta máxima'])}</b>. A faixa vai de
       <b>{pt(po.loc['P3','faixa baixa'], 0)}</b> a <b>{pt(po.loc['P3','faixa alta'], 0)}</b>, então
       fechar dentro ainda cabe.</p>
  </div>
  <div class="md-a">
    <button class="ax" data-go="fila" style="--d:0"><span class="ax-d">fila de risco</span>
      Cinco primeiros concentrados no ativo {FILA[0][4]}{ic('arrow','i xs')}</button>
    <button class="ax" data-go="saude" style="--d:1"><span class="ax-d">saúde por produto</span>
      Produto lssl na última posição do ranking{ic('arrow','i xs')}</button>
  </div>
  <div class="md-f"><span class="ct">Sem interação por conversa. O texto é escrito sobre a saída
    dos modelos.</span><button class="bt" id="fx">Abrir o painel{ic('arrow','i xs')}</button></div>
</div></div>'''

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{
 --ink:#090B10;--ink2:#11151D;--pg:#F7F8FA;--c:#FFF;
 --ln:rgba(17,21,29,.075);--ln2:rgba(17,21,29,.17);--tx:#4A5261;--tx2:#7D8697;--hd:#0C1017;
 --ac:#1E52D6;--acl:#EEF3FF;--no:#C4231C;--nol:#FDF1F0;--ok:#0F8A4C;--okl:#EDFAF2;
 --wn:#A85E10;--wnl:#FDF6EA;
 --e:cubic-bezier(.19,1,.22,1);--e2:cubic-bezier(.34,1.56,.64,1);
 --s1:0 1px 2px rgba(12,16,23,.04),0 8px 24px -12px rgba(12,16,23,.10);
 --s2:0 2px 4px rgba(12,16,23,.05),0 24px 48px -18px rgba(12,16,23,.16)}
html{-webkit-font-smoothing:antialiased;scroll-behavior:smooth}
body{background:var(--pg);color:var(--hd);display:flex;min-height:100dvh;
 font-family:'Geist',system-ui,-apple-system,sans-serif;font-size:15px;font-weight:400;
 font-feature-settings:'ss01','cv05';letter-spacing:-.005em}
.mono{font-family:'Geist Mono','JetBrains Mono',ui-monospace,monospace;letter-spacing:-.02em;
 font-weight:500;font-size:.94em}
.n{font-variant-numeric:tabular-nums lining-nums;font-feature-settings:'tnum','lnum'}
/* ══════════ nav */
aside{width:252px;flex-shrink:0;background:var(--ink);padding:26px 16px 22px;display:flex;
 flex-direction:column;gap:3px;position:sticky;top:0;height:100dvh;overflow:hidden}
aside::before{content:'';position:absolute;inset:-40% -60% auto -60%;height:130%;z-index:0;
 background:radial-gradient(46% 42% at 22% 18%,rgba(30,82,214,.42),transparent 66%),
  radial-gradient(38% 36% at 78% 62%,rgba(30,82,214,.2),transparent 68%),
  radial-gradient(30% 34% at 40% 88%,rgba(96,165,250,.14),transparent 70%);
 animation:drift 26s ease-in-out infinite alternate;filter:blur(6px)}
aside::after{content:'';position:absolute;inset:0;z-index:0;
 background:linear-gradient(180deg,transparent 62%,var(--ink) 100%)}
.br{display:flex;align-items:center;gap:11px;padding:2px 10px 24px;position:relative;z-index:2}
.br-m{width:34px;height:34px;border-radius:10px;background:#fff;display:grid;place-items:center;
 box-shadow:0 2px 8px rgba(0,0,0,.3)}
.br b{font-size:18px;font-weight:700;color:#fff;letter-spacing:-.035em;display:block;line-height:1.05}
.br em{font-size:9px;letter-spacing:.14em;color:#606C82;font-style:normal;font-weight:600}
.nv{display:flex;align-items:center;gap:12px;background:0;border:0;color:#9AA4B4;font:inherit;
 font-size:14px;font-weight:500;padding:10px 13px;border-radius:11px;cursor:pointer;width:100%;
 text-align:left;position:relative;z-index:2;transition:color .3s var(--e),background .3s var(--e);
 animation:in .6s var(--e) both;animation-delay:calc(var(--d)*60ms);letter-spacing:-.008em}
.nv:hover:not(.off){color:#EBEFF5;background:rgba(255,255,255,.045)}
.nv.on{color:#fff;background:rgba(255,255,255,.07);
 box-shadow:inset 0 1px 0 rgba(255,255,255,.09),inset 1px 0 0 var(--ac)}
.nv.off{opacity:.3;cursor:default}
.nv em{margin-left:auto;font-size:8.5px;font-style:normal;font-weight:700;letter-spacing:.1em;
 text-transform:uppercase;background:rgba(255,255,255,.08);padding:3px 6px;border-radius:4px}
.i{display:inline-grid;place-items:center;width:19px;height:19px;flex-shrink:0}
.i svg{width:19px;height:19px;stroke:currentColor;fill:none;stroke-width:1.6;
 stroke-linecap:round;stroke-linejoin:round}
.i.sm,.i.sm svg{width:15px;height:15px}.i.xs,.i.xs svg{width:13px;height:13px}
.rd{margin-top:auto;font-size:10.5px;color:#4E5768;line-height:1.65;padding:0 11px;
 position:relative;z-index:2}
/* ══════════ shell */
main{flex:1;padding:30px 36px 76px;min-width:0;max-width:1600px;position:relative}
main::before{content:'';position:fixed;inset:0 0 0 252px;z-index:0;pointer-events:none;
 background-image:linear-gradient(rgba(12,16,23,.019) 1px,transparent 1px),
  linear-gradient(90deg,rgba(12,16,23,.019) 1px,transparent 1px);background-size:40px 40px;
 mask:radial-gradient(1000px 680px at 82% -8%,#000 8%,transparent 68%)}
main>*{position:relative;z-index:1}
.hd-r{display:flex;align-items:center;gap:14px;margin-bottom:22px;animation:in .6s var(--e) both}
.hd-r h1{font-size:27px;font-weight:650;letter-spacing:-.032em}
.ct{font-size:11px;font-weight:500;color:var(--tx2);letter-spacing:.01em}
.hd-r .ct{margin-left:auto;background:var(--c);border:1px solid var(--ln);padding:6px 12px;
 border-radius:999px;box-shadow:var(--s1)}
.bl{position:relative;background:var(--c);border:1px solid var(--ln);border-radius:11px;width:36px;
 height:36px;display:grid;place-items:center;cursor:pointer;color:var(--tx);box-shadow:var(--s1);
 transition:all .3s var(--e)}
.bl:hover{color:var(--ac);transform:translateY(-1px);box-shadow:var(--s2)}
.bl b{position:absolute;top:-4px;right:-4px;min-width:16px;height:16px;border-radius:8px;
 background:var(--no);color:#fff;font-size:9.5px;font-weight:700;display:grid;place-items:center;
 box-shadow:0 0 0 2px var(--pg)}
.bl.rd2 b{display:none}
/* ══════════ trilho de tempo · assinatura */
.rail{background:var(--c);border:1px solid var(--ln);border-radius:20px 20px 20px 6px;
 padding:18px 22px 12px;box-shadow:var(--s1);margin-bottom:20px;position:relative;overflow:hidden}
.rail::after{content:'';position:absolute;inset:0;pointer-events:none;
 background:linear-gradient(100deg,transparent 40%,rgba(30,82,214,.04) 68%,transparent 82%)}
.rail-h{display:flex;align-items:baseline;gap:18px;flex-wrap:wrap}
.rail-t{font-size:10.5px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--tx2)}
.rail-m{display:flex;gap:18px;margin-left:auto;flex-wrap:wrap}
.m{display:inline-flex;align-items:center;gap:7px;font-size:12px;color:var(--tx2);font-weight:500}
.m i{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.m.ok i{background:var(--ok)}.m.ac i{background:var(--ac)}
.m.dim i{background:var(--tx2);opacity:.42}
.m b{color:var(--hd);font-weight:650;font-variant-numeric:tabular-nums}
.spk{width:100%;height:132px;margin-top:10px;display:block;overflow:visible}
.spk-l{fill:none;stroke:var(--ac);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;
 stroke-dasharray:1600;stroke-dashoffset:1600;animation:draw 1.6s var(--e) .3s forwards}
.spk-f{fill:none;stroke:var(--ac);stroke-width:1.7;stroke-linecap:round;stroke-dasharray:5 4;
 opacity:0;animation:fade .8s ease 1.5s forwards}
.spk-bd{fill:var(--ac);opacity:0;animation:fade 1s ease 1.65s forwards;--o:.085}
.spk-a{opacity:0;animation:fade .9s ease 1.1s forwards;--o:1}
.spk-ag{stroke:var(--ln2);stroke-width:1;stroke-dasharray:2 4;opacity:0;
 animation:fade .6s ease 1.4s forwards}
.spk-n{fill:var(--ac);opacity:0;animation:pin .5s var(--e2) 1.35s forwards}
.spk-h{fill:var(--ac);opacity:0;transform-box:fill-box;transform-origin:center;
 animation:halo 3.2s ease-out 2s infinite}
.rail-x{display:flex;justify-content:space-between;font-size:9.5px;color:var(--tx2);margin-top:4px;
 letter-spacing:.06em;text-transform:uppercase;font-weight:600;position:relative}
.rail-x .agora{position:absolute;left:var(--cut);transform:translateX(-50%);color:var(--ac);
 white-space:nowrap}
/* ══════════ cards */
.grid{display:grid;gap:18px;align-items:stretch}
.g-p{grid-template-columns:1.22fr 1.46fr .96fr}
.c-d{grid-column:1}.c-e{grid-column:2/4}
.g-f{grid-template-columns:1.5fr 1fr;align-items:start}.g-f .c-a{grid-row:span 2}
.g-c{grid-template-columns:1.06fr 1fr}
.c{background:var(--c);border:1px solid var(--ln);border-radius:20px 20px 20px 6px;padding:22px 24px;
 box-shadow:var(--s1);position:relative;overflow:hidden;min-width:0;
 display:flex;flex-direction:column;
 transition:box-shadow .5s var(--e),transform .5s var(--e)}
.c>.nt{margin-top:auto}   /* a leitura fica ancorada no rodape, o card preenche a linha */
.c::before{content:'';position:absolute;inset:0;pointer-events:none;opacity:0;
 transition:opacity .45s var(--e);border-radius:inherit;
 background:radial-gradient(340px 240px at var(--mx,50%) var(--my,0),rgba(30,82,214,.055),transparent 68%)}
.c:hover{box-shadow:var(--s2);transform:translateY(-2px)}
.c:hover::before{opacity:1}
[data-rev]{opacity:0;transform:translateY(16px)}
[data-rev].sv{animation:in .72s var(--e) both;animation-delay:calc(var(--d,0)*85ms)}
.lb{font-size:10.5px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--tx2);
 display:flex;align-items:center;gap:8px}
.lb::before{content:'';width:4px;height:4px;border-radius:50%;background:var(--ac);flex-shrink:0;
 box-shadow:0 0 0 3px rgba(30,82,214,.12)}
.lb b{color:var(--hd);text-transform:none;letter-spacing:-.02em;font-size:12.5px}
.lb.mt2{margin-top:20px}
.lb-r{display:flex;align-items:center;gap:12px}
.lk{margin-left:auto;display:inline-flex;align-items:center;gap:5px;background:0;border:0;font:inherit;
 font-size:11.5px;font-weight:600;color:var(--ac);cursor:pointer;transition:gap .32s var(--e)}
.lk:hover{gap:9px}
.nt{font-size:12px;color:var(--tx2);line-height:1.62;margin-top:16px;padding-top:13px;
 border-top:1px solid var(--ln)}
.nt b{color:var(--hd);font-weight:600}
.ex{font-size:13.5px;color:var(--tx);line-height:1.6;margin-top:10px}
.ex b{color:var(--hd);font-weight:600}
/* meta */
.mt{margin-top:26px}
.mt:first-of-type{margin-top:18px}
.mt-h{display:flex;align-items:baseline;gap:8px}
.mt-p{font-size:11px;font-weight:700;color:var(--tx2);letter-spacing:.08em}
.mt-v{font-size:25px;font-weight:650;letter-spacing:-.035em;font-variant-numeric:tabular-nums}
.mt-v.ok{color:var(--ok)}.mt-v.no{color:var(--no)}
.mt-l{font-size:12px;color:var(--tx2);font-weight:500}
.tag{font-size:9.5px;font-weight:700;letter-spacing:.06em;padding:3px 7px;border-radius:5px;
 text-transform:uppercase;white-space:nowrap}
.tag.ok{background:var(--okl);color:var(--ok)}.tag.no{background:var(--nol);color:var(--no)}
.tag.wn{background:var(--wnl);color:var(--wn)}.tag.ac{background:var(--acl);color:var(--ac)}
.mt-h .tag{margin-left:auto}
/* a barra mostra o intervalo, nao um preenchimento: a projecao e uma faixa, nao um ponto */
.mt-b{height:14px;border-radius:7px;background:#EFF1F5;position:relative;margin-top:9px}
.mt-b s{position:absolute;top:0;bottom:0;border-radius:7px;text-decoration:none;
 transform:scaleX(0);transform-origin:left;animation:abre 1s var(--e) .5s forwards}
.mt-b s.ok{background:linear-gradient(90deg,rgba(15,138,76,.34),rgba(15,138,76,.62))}
.mt-b s.no{background:linear-gradient(90deg,rgba(196,35,28,.34),rgba(196,35,28,.62))}
.mt-b i{position:absolute;top:-3px;bottom:-3px;width:3px;border-radius:2px;z-index:2;
 opacity:0;animation:fade .5s ease 1.3s forwards}
.mt-b i.ok{background:var(--ok)}.mt-b i.no{background:var(--no)}
.mt-b u{position:absolute;top:-5px;bottom:-5px;width:2px;background:var(--hd);z-index:3;
 opacity:0;animation:fade .5s ease 1.1s forwards}
.mt-b u::after{content:'meta';position:absolute;top:-14px;left:50%;transform:translateX(-50%);
 font-size:8.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2)}
.mt-f{font-size:11px;color:var(--tx2);margin-top:5px;font-variant-numeric:tabular-nums}
/* fila resumo */
.fq{list-style:none;margin-top:12px}
.fq li{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid var(--ln);
 animation:in .55s var(--e) both;animation-delay:calc(280ms + var(--d)*58ms)}
.fq-o{width:16px;font-size:11px;font-weight:600;color:var(--tx2);font-variant-numeric:tabular-nums}
.fq-i{flex:1;min-width:0}
.fq-i b{display:block;font-size:13.5px;font-weight:600;color:var(--hd)}
.fq-i em{font-size:11px;color:var(--tx2);font-style:normal}
.fq-v{font-size:18px;font-weight:650;color:var(--no);letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.fq-v small{font-size:11px;font-weight:600}
/* kpi do dia */
.kd{margin-top:16px;display:flex;align-items:baseline;gap:12px}
.c-c .kd{align-items:center}
.c-d .sr{flex:1}
.kv{font-size:34px;font-weight:650;letter-spacing:-.045em;line-height:.95;font-variant-numeric:tabular-nums}
.kv.no{color:var(--no)}
.kl{font-size:11.5px;color:var(--tx2);font-weight:500;line-height:1.45}
.kl em{display:block;font-style:normal;opacity:.76}
/* saude resumo */
.sr{display:flex;align-items:center;gap:11px;margin-top:11px;
 animation:in .5s var(--e) both;animation-delay:calc(300ms + var(--d)*58ms)}
.sr-p{width:40px;font-size:12.5px;font-weight:600}
.sr-b{flex:1;height:7px;border-radius:4px;background:#EFF1F5;overflow:hidden}
.sr-b i{display:block;height:100%;border-radius:4px;width:0;background:var(--c2,var(--c));
 background:var(--c);animation:gw .95s var(--e) .6s forwards}
.sr-v{width:34px;text-align:right;font-size:13px;font-weight:650;font-variant-numeric:tabular-nums}
/* latente */
.lt-r{display:flex;gap:11px;margin-top:12px;flex-wrap:wrap}
.lt{flex:1;min-width:150px;background:var(--wnl);border:1px solid rgba(168,94,16,.13);
 border-radius:12px;padding:11px 13px;animation:in .55s var(--e) both;
 animation-delay:calc(320ms + var(--d)*66ms)}
.lt b{display:block;font-size:13.5px;color:var(--hd)}
.lt>span{font-size:11.5px;color:var(--wn);font-weight:600;display:block;margin-top:3px}
.lt>em{font-size:11px;color:var(--tx2);font-style:normal;display:block;margin-top:1px}
/* tabelas */
.tb{width:100%;border-collapse:collapse;font-size:13px;margin-top:13px}
.tb.sm{font-size:12.5px}
.tb th{text-align:right;font-size:9.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
 color:var(--tx2);padding:0 7px 9px;border-bottom:1px solid var(--ln);white-space:nowrap}
.tb th:first-child,.tb th:nth-child(2){text-align:left}
.tb td{text-align:right;padding:9px 7px;border-bottom:1px solid var(--ln);
 font-variant-numeric:tabular-nums}
.tb td:first-child,.tb td:nth-child(2){text-align:left}
.tb tbody tr{animation:fade .5s ease both;animation-delay:calc(260ms + var(--d)*38ms);
 transition:background .28s var(--e)}
.tb tbody tr:hover{background:#FAFBFC}
.tb tbody tr.hi{background:linear-gradient(90deg,var(--nol),transparent 74%)}
.o{color:var(--tx2);width:22px;font-size:11px;font-weight:600}
.dm{color:var(--tx2)}
.no{color:var(--no);font-weight:600}.ok{color:var(--ok);font-weight:600}
.rc{display:flex;align-items:center;gap:8px;justify-content:flex-end;font-weight:600}
.rc small{margin-left:-6px;font-size:.78em;font-weight:600;color:var(--tx2)}
.rb{width:56px;height:6px;border-radius:4px;background:#EFF1F5;overflow:hidden;flex-shrink:0}
.rb i{display:block;height:100%;border-radius:4px;width:0;
 background:linear-gradient(90deg,#E85C54,var(--no));animation:gw .9s var(--e) .65s forwards}
.rb i[style*="--c"]{background:var(--c)}
/* detalhe */
.bg-r{display:flex;align-items:flex-end;gap:13px;margin-top:14px}
.bg-v{font-size:46px;font-weight:650;letter-spacing:-.05em;line-height:.88;color:var(--no);
 font-variant-numeric:tabular-nums}
.bg-v small{font-size:19px}
.bg-l{font-size:11.5px;color:var(--tx2);font-weight:500;line-height:1.45;padding-bottom:4px}
.bg-l em{display:block;font-style:normal;opacity:.78}
.rt{height:20px;border-radius:6px;background:#EFF1F5;position:relative;overflow:hidden;margin-top:12px}
.rt i{position:absolute;inset:0 auto 0 0;border-radius:6px;width:0;
 background:linear-gradient(90deg,#E85C54,var(--no));animation:gw 1.05s var(--e) .6s forwards}
.rt u{position:absolute;top:-2px;bottom:-2px;width:2px;background:var(--ac)}
.ev{display:flex;gap:10px;margin-top:14px;background:var(--pg);border:1px solid var(--ln);
 border-radius:12px;padding:12px 14px}
.ev .i{color:var(--ac);margin-top:1px}
.ev p{font-size:13px;color:var(--tx);line-height:1.55}
.ev b{color:var(--hd);font-weight:600}
.pw{display:flex;align-items:center;gap:10px;margin-top:9px;font-size:12.5px;color:var(--tx);
 animation:in .5s var(--e) both;animation-delay:calc(360ms + var(--d)*54ms)}
.pw>span:first-child{width:138px}
.pb{flex:1;height:6px;border-radius:4px;background:#EFF1F5;overflow:hidden}
.pb i{display:block;height:100%;border-radius:4px;width:0;
 background:linear-gradient(90deg,#8FB4FF,var(--ac));animation:gw .85s var(--e) .7s forwards}
.pw b{width:32px;text-align:right;font-weight:650;font-variant-numeric:tabular-nums}
/* recorrentes */
.rc2{margin-top:11px;padding-bottom:11px;border-bottom:1px solid var(--ln);
 animation:in .5s var(--e) both;animation-delay:calc(280ms + var(--d)*56ms)}
.rc2-t{font-size:11.5px;color:var(--tx);display:block;line-height:1.35}
.rc2-m{font-size:11.5px;color:var(--tx2);display:block;margin-top:4px}
.rc2-m b{color:var(--hd);font-weight:650;font-variant-numeric:tabular-nums}
/* ══════════ modal */
.ov{position:fixed;inset:0;z-index:70;display:grid;place-items:center;padding:30px;
 background:rgba(9,11,16,.6);backdrop-filter:blur(9px) saturate(1.2);
 -webkit-backdrop-filter:blur(9px) saturate(1.2);animation:fade .34s ease both}
.ov.off{display:none}
.md{width:min(660px,100%);max-height:88dvh;overflow:auto;background:var(--c);
 border-radius:24px 24px 24px 8px;padding:30px 32px;position:relative;
 box-shadow:0 40px 90px -26px rgba(9,11,16,.52),inset 0 1px 0 rgba(255,255,255,.9);
 animation:pop .58s var(--e) both}
.md::before{content:'';position:absolute;inset:0;border-radius:inherit;pointer-events:none;
 background:radial-gradient(600px 240px at 100% -18%,rgba(30,82,214,.055),transparent 62%)}
.md>*{position:relative}
.md-t{display:flex;align-items:center;gap:12px}
.md-s{font-family:'Geist Mono','JetBrains Mono',monospace;font-size:11px;font-weight:500;
 color:var(--tx2);letter-spacing:.01em}
.md-t .ct{margin-left:auto;background:var(--pg);border:1px solid var(--ln);padding:4px 9px;border-radius:5px}
.md-h{font-size:29px;font-weight:650;letter-spacing:-.038em;margin-top:16px;line-height:1.16}
.md-h .mu{color:var(--tx2);font-weight:400}
.md-b{margin-top:15px}
.md-b p{font-size:14.5px;line-height:1.66;color:var(--tx);margin-bottom:11px}
.md-b b{color:var(--hd);font-weight:600}
.md-b em{font-style:normal;font-weight:650;color:var(--hd)}
.md-a{margin-top:18px;display:flex;flex-direction:column;gap:8px}
.ax{display:flex;align-items:center;gap:11px;font:inherit;font-size:13.5px;color:var(--tx);
 background:var(--pg);border:1px solid var(--ln);border-radius:12px;padding:12px 14px;cursor:pointer;
 text-align:left;transition:all .32s var(--e);animation:in .55s var(--e) both;
 animation-delay:calc(300ms + var(--d)*80ms)}
.ax:hover{background:var(--c);border-color:rgba(30,82,214,.24);color:var(--hd);
 transform:translateX(3px);box-shadow:var(--s1)}
.ax:active{transform:translateX(3px) scale(.99)}
.ax-d{font-size:9.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ac);
 background:var(--acl);padding:4px 7px;border-radius:4px;flex-shrink:0;white-space:nowrap}
.ax .i{margin-left:auto;color:var(--tx2)}
.md-f{display:flex;align-items:center;gap:16px;margin-top:20px;padding-top:16px;
 border-top:1px solid var(--ln)}
.md-f .ct{max-width:32ch;line-height:1.5}
.bt{margin-left:auto;display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:13.5px;
 font-weight:600;color:#fff;background:var(--ac);border:0;border-radius:11px;padding:11px 17px;
 cursor:pointer;transition:all .3s var(--e);white-space:nowrap;
 box-shadow:0 6px 16px -6px rgba(30,82,214,.46)}
.bt:hover{background:#1846BE;transform:translateY(-1px);box-shadow:0 10px 22px -8px rgba(30,82,214,.5)}
.bt:active{transform:translateY(-1px) scale(.985)}
/* ══════════ arq */
.aq{margin-top:26px;background:var(--ink);border-radius:20px 20px 20px 6px;padding:26px 30px;
 color:#E4E9F0;position:relative;overflow:hidden}
.aq::before{content:'';position:absolute;inset:-30% -20% auto -20%;height:120%;
 background:radial-gradient(40% 44% at 84% 16%,rgba(30,82,214,.34),transparent 66%);
 animation:drift 22s ease-in-out infinite alternate-reverse}
.aq>*{position:relative;z-index:1}
.aq h3{font-size:16px;font-weight:650;letter-spacing:-.02em}
.fx{display:flex;align-items:center;gap:10px;margin-top:16px;flex-wrap:wrap}
.st{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);border-radius:11px;
 padding:11px 15px;font-size:13px;color:#CFD6E1;box-shadow:inset 0 1px 0 rgba(255,255,255,.06)}
.st b{display:block;font-size:9px;letter-spacing:.13em;text-transform:uppercase;color:#6E7994;
 margin-bottom:3px;font-weight:600}
.fx .i{color:#4C5568}
.aq p{font-size:13px;color:#8E98AA;line-height:1.66;margin-top:14px;max-width:80ch}
.aq p b{color:#fff;font-weight:600}
/* ══════════ motion */
@keyframes in{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:var(--o,1)}}
@keyframes halo{0%{opacity:.3;transform:scale(.35);transform-origin:center}
 70%,100%{opacity:0;transform:scale(1.6)}}
@keyframes pop{from{opacity:0;transform:translateY(20px) scale(.972)}to{opacity:1;transform:none}}
@keyframes gw{from{width:0}to{width:var(--w)}}
@keyframes abre{to{transform:scaleX(1)}}
/* sem animacao, todo elemento tem de aparecer no estado final — nada depende de keyframe */
@media (prefers-reduced-motion:reduce){
 *{animation:none!important;transition-duration:.01ms!important}
 [data-rev],.fq li,.sr,.lt,.pw,.rc2,.st,.nv,.ac,.mt,.tb tbody tr
 {opacity:1!important;transform:none!important}
 .mt-b s{transform:none!important}.mt-b i,.mt-b u{opacity:1!important}
 .spk-l{stroke-dashoffset:0!important}
 .spk-f,.spk-a,.spk-ag,.spk-n{opacity:1!important}.spk-bd{opacity:.085!important}
 .sr-b i,.rb i,.pb i,.rt i{width:var(--w)!important}}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes pin{from{opacity:0;transform:scale(0)}to{opacity:1;transform:scale(1)}}
@keyframes drift{0%{transform:translate3d(0,0,0) scale(1)}
 50%{transform:translate3d(6%,-4%,0) scale(1.09)}100%{transform:translate3d(-5%,3%,0) scale(1.04)}}
@media (max-width:1240px){.g-p,.g-f,.g-c{grid-template-columns:1fr!important}
 .c-d,.c-e{grid-column:auto}.g-f .c-a{grid-row:auto}}
@media (max-width:820px){body{flex-direction:column}aside{position:static;height:auto;width:100%}
 main{padding:22px 16px 48px}main::before{inset:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}
 [data-rev]{opacity:1;transform:none}}
"""

telas = "".join(f'<section class="tl" id="s-{k}" {"" if k=="painel" else "hidden"}>{h}</section>'
                for k, (_, _, h) in TELAS.items())

JS = r"""
const ov=document.getElementById('ov'),bl=document.getElementById('bl'),T=__TELAS__;
const fecha=()=>{ov.classList.add('off');bl.classList.add('rd2')};
document.getElementById('fx').onclick=fecha;
bl.onclick=()=>{ov.classList.remove('off');bl.classList.remove('rd2')};
ov.onclick=e=>{if(e.target===ov)fecha()};
addEventListener('keydown',e=>{if(e.key==='Escape')fecha()});

// revela no scroll, e conta os numeros quando o cartao entra
const conta=el=>{
  const alvo=parseFloat(el.dataset.n),cs=+el.dataset.c,t0=performance.now(),dur=780;
  const passo=t=>{const p=Math.min((t-t0)/dur,1),v=alvo*(1-Math.pow(1-p,3));
    el.textContent=v.toFixed(cs).replace('.',',');if(p<1)requestAnimationFrame(passo)};
  requestAnimationFrame(passo)};
const obs=new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting)return;
  e.target.classList.add('sv');
  e.target.querySelectorAll('.n[data-n]').forEach((n,i)=>setTimeout(()=>conta(n),120+i*45));
  obs.unobserve(e.target)}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
const liga=r=>r.querySelectorAll('[data-rev]').forEach(x=>obs.observe(x));

// luz que acompanha o cursor na borda do cartao
addEventListener('pointermove',e=>{
  const c=e.target.closest?.('.c');if(!c)return;const b=c.getBoundingClientRect();
  c.style.setProperty('--mx',(e.clientX-b.left)+'px');
  c.style.setProperty('--my',(e.clientY-b.top)+'px')},{passive:true});

function vai(t){
  document.querySelectorAll('.nv').forEach(x=>x.classList.toggle('on',x.dataset.t===t));
  document.querySelectorAll('.tl').forEach(s=>{
    s.hidden=s.id!=='s-'+t;
    if(!s.hidden){s.querySelectorAll('[data-rev]').forEach(x=>x.classList.remove('sv'));liga(s)}});
  document.getElementById('ttl').textContent=T[t];
  scrollTo({top:0,behavior:'smooth'})}
document.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{fecha();vai(b.dataset.go)});
document.querySelectorAll('.nv[data-t]').forEach(b=>b.onclick=()=>vai(b.dataset.t));
liga(document.getElementById('s-painel'));liga(document.querySelector('.aq').parentNode);
""".replace("__TELAS__", json.dumps({k: v[0] for k, v in TELAS.items()}, ensure_ascii=False))

OUT.write_text(f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Cronos</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<aside>
  <div class="br"><div class="br-m"><svg viewBox="0 0 28 28" fill="none" width="19" height="19">
    <path d="M6 22L12 14L16 17L22 8" stroke="#090B10" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="22" cy="8" r="3" fill="none" stroke="#1E52D6" stroke-width="1.8"/>
    <circle cx="22" cy="8" r="1.2" fill="#1E52D6"/></svg></div>
    <div><b>Cronos</b><em>VEJA ANTES · AJA ANTES</em></div></div>
  {nav}
  <div class="rd">Protótipo da aplicação.<br>Os valores vêm dos parquets gerados pelos notebooks
    04 a 07.</div>
</aside>
<main>
  <div class="hd-r"><h1 id="ttl">Painel</h1>
    <span class="ct">corte em {DIA_HOJE.day:02d}/{DIA_HOJE.month:02d}/{DIA_HOJE.year}</span>
    <button class="bl" id="bl" title="reabrir o resumo de hoje">{ic('bell')}<b>1</b></button></div>
  {telas}
  <div class="aq" data-rev>
    <h3>Como a aplicação é servida</h3>
    <div class="fx">
      <div class="st"><b>notebooks</b>treinam e preveem</div>{ic('arrow','i sm')}
      <div class="st"><b>data/interim</b>gravam parquet</div>{ic('arrow','i sm')}
      <div class="st"><b>django</b>lê e renderiza</div>{ic('arrow','i sm')}
      <div class="st"><b>docker</b>URL pública</div>
    </div>
    <p>O contêiner leva apenas <b>django, pandas e pyarrow</b>. Não executa Prophet nem
    scikit-learn, porque as previsões já estão gravadas. A imagem cabe em plano gratuito e a
    entrega por Docker roda em qualquer provedor.</p>
  </div>
</main>
{modal}
<script>{JS}</script></body></html>''', encoding='utf-8')
print(f'v5: {OUT}')
