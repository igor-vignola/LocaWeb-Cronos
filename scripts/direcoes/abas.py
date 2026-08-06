# -*- coding: utf-8 -*-
"""As cinco abas da aplicacao Cronos.

Todas na mesma regua: lidas em atos, cada card diz em uma linha o que ele e, e o que da
para aprofundar abre modal. Onde o dado nao existe, a tela diz que nao existe."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from componentes import (ato, barras_mes, cab, chip, faixa_24h, filtros, heroi, ico,
                         item_fila, linha_metrica, meta, trilho, vazio)
from dados import (ACIMA_10, ATIVOS, BASE_20, DELTA_TAXA, DIA_HOJE, ELEG_30, ELEGIVEIS,
                   EM_ABERTO, FILA_HOJE, FILA_TODA, FUT3, HORA_PICO, HORA_RISCO, HOJE2, HOJE3,
                   LBL_DIA, MEDIA_BASE, MES_LBL, N_FILA, ONTEM, ONTEM_TOTAL, ONTEM_VIOL, REAL3,
                   SEMANA, SEM_VIOL, TAXA_30, TOP50_PEGA, TOTAL_VIOL, ULTIMOS_DIAS, VIOL_30,
                   VIOL_PERIODO, causas, dm, grupos, mil, proj, pt, recor, saude)

TOPO = FILA_TODA.iloc[0]
PIOR = saude.index[-1]
HOJE_MAX = float(FILA_HOJE['risco'].max())
HOJE_ACIMA10 = int((FILA_HOJE['risco'] >= 10).sum())
CALMO = HOJE_ACIMA10 == 0


# ══════════ 1 · Hoje ═══════════════════════════════════════════════════════
def aba_hoje():
    proximos = ''.join(
        f'<button class="da"><em>{LBL_DIA[r["dia"].dayofweek]} · {dm(r["dia"])}</em>'
        f'<b>{pt(r["valor"], 0)}</b><span>{pt(r["baixo"], 0)} a {pt(r["alto"], 0)}</span></button>'
        for _, r in FUT3.iloc[1:5].iterrows())
    if CALMO:
        remate = (f'Nenhum caso aberto hoje passa de 10% de risco: o maior está em '
                  f'<b>{pt(HOJE_MAX)}%</b>. Na fila inteira, porém, '
                  f'<span class="cr">cinco dos seis casos mais arriscados estão no mesmo '
                  f'ativo</span>, o <b class="id">{TOPO["ativo"]}</b>.')
    else:
        remate = (f'<span class="cr">{HOJE_ACIMA10} casos passam de 10% de risco</span> e '
                  f'pedem alguém antes do almoço.')
    piores = ''.join(
        f'<button class="rw" style="--i:{j}" data-mod="prod" data-k="{x}">'
        f'<span class="rw-p id">{x}</span>'
        f'<span class="rw-b"><i style="--w:{saude.loc[x, "nota"]:.0f}%;'
        f'--c2:{"#DC2626" if saude.loc[x, "nota"] < 40 else "#B45309"}"></i></span>'
        f'<span class="rw-v">{pt(saude.loc[x, "nota"])}</span>'
        f'<span class="rw-q">{pt(saude.loc[x, "taxa_violacao"] * 100, 2)}% violação</span>'
        f'<span class="sq">{ico("seta", 14)}</span></button>'
        for j, x in enumerate(saude.index[-5:][::-1]))
    ativos_top = ''.join(
        f'<button class="mr cl" data-mod="ativo" data-k="{a}">'
        f'{chip("ativo", "no" if r["taxa"] >= 10 else "wn", 18)}'
        f'<div class="mr-t"><b class="id">{a}</b>'
        f'<span>{int(r["violacoes"])} de {mil(r["passagens"])} passagens violaram</span></div>'
        f'<span class="mr-v {"no" if r["taxa"] >= 10 else ""}">{pt(r["taxa"], 1)}<u>%</u></span>'
        f'<span class="sq">{ico("seta", 14)}</span></button>'
        for a, r in ATIVOS.sort_values('taxa', ascending=False).head(4).iterrows())
    dias = ''.join(
        f'<div class="dc{" vi" if v else ""}"><i>{v if v else ""}</i>'
        f'<span>{LBL_DIA[d.dayofweek]}</span><em>{d.day:02d}/{d.month:02d}</em></div>'
        for d, v in ULTIMOS_DIAS)
    return f'''
  <div class="dias">
    <button class="da"><em>ontem · {dm(ONTEM['dia'])}</em><b>{ONTEM_TOTAL}</b>
      <span>entraram · {ONTEM_VIOL} violaram</span></button>
    <button class="da on"><em>hoje · {dm(DIA_HOJE)}</em><b>{pt(HOJE3['valor'], 0)}</b>
      <span>previstos no P3</span></button>{proximos}
  </div>

  <div class="hr">
    <div>
      <span class="kk">{ico('agora', 14)}{DIA_HOJE.day:02d}/{DIA_HOJE.month:02d}/{DIA_HOJE.year} · 07h00</span>
      <h1>Dia de volume normal,<br><span class="mu">{'sem caso crítico.' if CALMO
        else 'com risco concentrado.'}</span></h1>
      <p class="lead">Devem entrar cerca de <b>{pt(HOJE3['valor'], 0)} incidentes elegíveis</b>
        no P3 e <b>{pt(HOJE2['valor'], 0)}</b> no P2, dentro do padrão de uma quarta-feira.
        {remate}</p>
      <div class="chips">
        <div class="ch">{chip('entrada', 'ac', 16)}
          <div><em>entraram ontem</em><b>{ONTEM_TOTAL}<u>elegíveis</u></b></div></div>
        <div class="ch">{chip('escudo_ok', 'ok', 16)}
          <div><em>sem violar</em><b>{SEM_VIOL}<u>dias úteis</u></b></div></div>
        <div class="ch">{chip('fila', 'nt', 16)}
          <div><em>em atendimento</em><b>{mil(EM_ABERTO)}</b></div></div>
        <div class="ch">{chip('alerta', 'ok' if CALMO else 'no', 16)}
          <div><em>acima de 10% hoje</em><b>{HOJE_ACIMA10}<u>casos</u></b></div></div>
      </div>
    </div>
    {heroi()}
  </div>

  {ato('01', 'Como o dia se distribui',
       'Em que horas o trabalho entra, e em que horas o prazo costuma estourar.')}
  <div class="gr g2">
    <div class="cd">
      {cab('relogio', 'As 24 horas do dia',
           'Cada barra é uma hora. A altura é quanto entra, a cor é a taxa de violação daquela '
           'hora ao longo do ano.')}
      {faixa_24h()}
      <div class="nt">A madrugada tem pouco volume e a <b>maior taxa do dia</b>: às
        {HORA_RISCO['h']:02d}h a chance de estourar é <b>{pt(HORA_RISCO['taxa'] / MEDIA_BASE, 1)}
        vezes</b> a média da base. O pico de movimento é às {HORA_PICO['h']:02d}h, com
        {mil(HORA_PICO['abertos'])} incidentes no ano.</div>
    </div>
    <div class="cd">
      {cab('prazo', 'Os últimos dez dias úteis',
           'Círculo vazio é dia que fechou sem violação nenhuma. Cheio mostra quantas houve.')}
      <div class="dcs">{dias}</div>
      <div class="ml" style="margin-top:16px">
        {linha_metrica('escudo_ok', 'ok', 'Dias úteis seguidos sem violação',
                       f'contando de {dm(DIA_HOJE)} para trás', SEM_VIOL, 'dias', 'ok')}
        {linha_metrica('balanca', 'nt', 'Taxa dos últimos trinta dias',
                       f'{VIOL_30} violações em {mil(ELEG_30)} elegíveis', pt(TAXA_30, 2), '%',
                       '', f'<span class="vr ok">−{pt(abs(DELTA_TAXA), 0)}%</span>')}
      </div>
    </div>
  </div>

  {ato('02', 'O que fazer hoje',
       'Os casos abertos com maior chance de estourar o prazo, na ordem em que valem atenção.')}
  <div class="gr g2">
    <div class="cd">
      {cab('fila', 'Fila de hoje',
           f'Os {len(FILA_HOJE)} incidentes abertos em {dm(DIA_HOJE)}, ordenados pela chance de '
           'estourar. Clique para ver por que o modelo pontuou assim.',
           f'<button class="lk" data-ir="fila">fila completa{ico("seta", 14)}</button>')}
      <div class="fl">{"".join(item_fila(r, i)
        for i, (_, r) in enumerate(FILA_HOJE.head(6).iterrows()))}</div>
      <div class="nt">O maior risco de hoje é <b>{pt(HOJE_MAX)}%</b> contra uma média de base de
        <b>{pt(MEDIA_BASE, 2)}%</b>: alto em termos relativos, longe da faixa crítica. Dizer que
        o dia está calmo também é resposta.</div>
    </div>
    <div class="cd">
      {cab('alerta', 'Onde o risco se concentra',
           'Os ativos com maior taxa de violação conhecida até hoje. Clique para abrir o '
           'histórico mês a mês.')}
      <div class="ml">{ativos_top}</div>
      <div class="nt">O modelo <b>não usa a taxa do ativo como entrada</b>: ele usa a identidade
        do ativo, e só quando ela aparece o bastante para virar coluna própria. O histórico acima
        é contexto para quem decide, não sinal do modelo.</div>
    </div>
  </div>

  {ato('03', 'Para onde o ano vai',
       'Se nada mudar, onde o KPI fecha em dezembro e quais produtos puxam para baixo.')}
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
           'Nota de 0 a 100 por posição relativa entre os dezessete produtos. Clique para abrir '
           'os cinco componentes.',
           f'<button class="lk" data-ir="saude">ranking{ico("seta", 14)}</button>')}
      <div>{piores}</div>
      <div class="nt"><b>100 é o melhor dos dezessete</b>, não um produto sem problema. O pior é
        <b class="id">{PIOR}</b>, com <b>{pt(saude.loc[PIOR, 'prop_inedito'] * 100, 0)}%</b> de
        problemas inéditos, e o inédito viola <b>4,6 vezes mais</b> que o rotineiro.</div>
    </div>
  </div>'''


# ══════════ 2 · Fila de risco ══════════════════════════════════════════════
def aba_fila():
    faixas = [(10, 101, 'crítica', 'no'), (5, 10, 'alta', 'wn'),
              (1, 5, 'atenção', 'wn'), (0, 1, 'rotina', 'ok')]
    resumo = ''.join(
        f'<button class="fx" data-g="faixa" data-v="{lo}">'
        f'<em class="f-{k}">{rot}</em><b>{int(((FILA_TODA["risco"] >= lo) & (FILA_TODA["risco"] < hi)).sum())}</b>'
        f'<span>{int(FILA_TODA.loc[(FILA_TODA["risco"] >= lo) & (FILA_TODA["risco"] < hi), "violou"].sum())} '
        f'violaram</span></button>' for lo, hi, rot, k in faixas)
    linhas = ''.join(
        f'<tr data-mod="inc" data-k="{r["incidente"]}" data-r="{r["risco"]}" '
        f'data-p="{r["prioridade"]}" style="--i:{min(i, 24)}">'
        f'<td class="o">{int(r["posicao"])}</td>'
        f'<td><b class="id">{r["incidente"]}</b></td>'
        f'<td class="rc"><span class="rb"><i style="--w:{min(r["risco"] / 63 * 100, 100):.0f}%;'
        f'--c:{"#DC2626" if r["risco"] >= 10 else ("#B45309" if r["risco"] >= 3 else "#94A3B8")}">'
        f'</i></span>{pt(r["risco"])}<small>%</small></td>'
        f'<td class="dm">{r["prioridade"]}</td><td class="dm">{r["produto"]}</td>'
        f'<td class="dm">{r["equipe"]}</td><td class="dm id">{r["ativo"] if r["ativo"] != "None" else "—"}</td>'
        f'<td class="dm">{dm(r["dia"])} · {int(r["hora"]):02d}h</td>'
        f'<td class="dm">{f'{int(r["ativo_violacoes"])}/{mil(r["ativo_passagens"])}' if r["ativo_passagens"] else "sem histórico"}</td></tr>'
        for i, (_, r) in enumerate(FILA_TODA.head(40).iterrows()))
    return f'''
  {ato('01', 'A fila inteira',
       f'{mil(N_FILA)} incidentes pontuados fora da amostra, do maior para o menor risco.')}
  <div class="fxs">{resumo}</div>
  <div class="gr">
    <div class="cd">
      {cab('fila', 'Incidentes ordenados por risco',
           'O modelo pontua cada caso com o que existia na abertura. Clique em qualquer linha '
           'para abrir a decomposição do escore.',
           filtros('pri', [('t', 'todas'), ('P2', 'P2'), ('P3', 'P3')]))}
      <div class="tbw"><table class="tb">
        <thead><tr><th>#</th><th>Incidente</th><th>Risco</th><th>Prio</th><th>Produto</th>
          <th>Equipe</th><th>Ativo</th><th>Aberto</th><th>Histórico do ativo</th></tr></thead>
        <tbody id="tb-fila">{linhas}</tbody></table></div>
      <div class="tb-vz" id="tb-vazio" hidden>{vazio('lupa', 'Nenhum caso nesta faixa',
        'Troque o filtro acima para ver outras faixas de risco.')}</div>
      <div class="nt">Mostrando os <b>40 primeiros</b> de {mil(N_FILA)}. Nos cinquenta primeiros
        estão <b>{TOP50_PEGA} das {VIOL_PERIODO}</b> violações do período — ordenar por
        prioridade declarada pegaria bem menos.</div>
    </div>
  </div>

  {ato('02', 'Onde a fila se concentra',
       'Os grupos de produto, categoria e prioridade que violam mais que a média.')}
  <div class="gr g2">
    <div class="cd">
      {cab('alvo', 'Grupos críticos',
           'Combinações de produto, categoria e prioridade com taxa acima da média da base.')}
      <table class="tb sm"><thead><tr><th>Produto · categoria · prioridade</th><th>Taxa</th>
        <th>vs média</th></tr></thead><tbody>
        {"".join(f"""<tr><td class="id">{r['grupo']}</td><td class="no">{pt(r['taxa %'], 2)}%</td>
          <td class="dm">{pt(r['vezes a média'], 2)}x</td></tr>"""
          for _, r in grupos.head(6).iterrows())}
      </tbody></table>
      <div class="nt">Sete grupos concentram <b>13%</b> das violações em <b>5%</b> da base.</div>
    </div>
    <div class="cd">
      {cab('balanca', 'Como ler um risco de 10%',
           'A régua que falta na cabeça de quem olha a fila pela primeira vez.')}
      <div class="reg">
        {"".join(f'''<div class="rg-l"><span class="rg-b f-{k}"></span>
          <div><b>{rot}</b><span>{lo}% a {"100" if hi > 100 else hi}% de chance ·
            {int(((FILA_TODA['risco'] >= lo) & (FILA_TODA['risco'] < hi)).sum())} casos</span></div>
          <em>{pt(lo / MEDIA_BASE, 0)}x a média</em></div>''' for lo, hi, rot, k in faixas[::-1])}
      </div>
      <div class="nt">A média da base é <b>{pt(MEDIA_BASE, 2)}%</b>. Um caso de 10% é
        <b>dez vezes</b> mais provável que o incidente comum — por isso a faixa crítica tem
        poucos casos e merece atenção.</div>
    </div>
  </div>'''


# ══════════ 3 · Saúde por produto ══════════════════════════════════════════
def aba_saude():
    QT = {'risco latente': ('wn', 'latente'), 'problema já materializado': ('no', 'materializado'),
          'problema conhecido e recorrente': ('az', 'recorrente'), 'estável': ('ok', 'estável')}
    linhas = ''.join(
        f'<tr data-mod="prod" data-k="{x}" data-q="{QT[r["quadrante"]][1]}" style="--i:{i}">'
        f'<td class="o">{int(r["posicao"])}</td><td><b class="id">{x}</b></td>'
        f'<td class="rc"><span class="rb"><i style="--w:{r["nota"]:.0f}%;'
        f'--c:{"#DC2626" if r["nota"] < 40 else ("#B45309" if r["nota"] < 65 else "#059669")}">'
        f'</i></span>{pt(r["nota"])}</td>'
        f'<td><span class="tag {QT[r["quadrante"]][0]}" title="{r["quadrante"]}">'
        f'{QT[r["quadrante"]][1]}</span></td>'
        f'<td class="dm">{mil(r["incidentes"])}</td>'
        f'<td class="no">{pt(r["taxa_violacao"] * 100, 2)}%</td>'
        f'<td class="dm">{pt(r["prop_inedito"] * 100, 0)}%</td>'
        f'<td class="dm">{pt(r["duracao_mediana_h"], 1)}h</td></tr>'
        for i, (x, r) in enumerate(saude.iterrows()))
    lat = saude[saude['quadrante'] == 'risco latente'].sort_values('prop_inedito', ascending=False)
    return f'''
  {ato('01', 'A nota de cada produto',
       'Dezessete produtos que respondem por 95% do volume, do melhor ao pior.')}
  <div class="gr">
    <div class="cd">
      {cab('coracao', 'Ranking de saúde',
           'A nota combina cinco componentes por posição relativa. Clique em qualquer produto '
           'para ver quanto cada componente pesou.',
           filtros('quad', [('t', 'todos'), ('materializado', 'materializado'),
                            ('latente', 'latente'), ('recorrente', 'recorrente')]))}
      <div class="tbw"><table class="tb">
        <thead><tr><th>#</th><th>Produto</th><th>Nota</th><th>Situação</th><th>Incidentes</th>
          <th>Violação</th><th>Inéditos</th><th>Duração</th></tr></thead>
        <tbody id="tb-saude">{linhas}</tbody></table></div>
      <div class="tb-vz" id="tb-vazio-s" hidden>{vazio('lupa', 'Nenhum produto nesta situação',
        'Troque o filtro para ver os outros quadrantes.')}</div>
      <div class="nt">A nota é <b>relativa</b>: 100 seria o melhor dos dezessete em todos os
        cinco componentes, não um produto sem problema nenhum.</div>
    </div>
  </div>

  {ato('02', 'O que a nota esconde',
       'Produto com pouca violação hoje mas muito problema inédito carrega risco que ainda '
       'não apareceu.')}
  <div class="gr g2">
    <div class="cd">
      {cab('novo', 'Risco latente',
           'Muito problema novo e violação ainda baixa. O inédito viola 4,6 vezes mais que o '
           'rotineiro, então estes produtos carregam exposição não materializada.')}
      <div class="ml">
        {"".join(f'''<button class="mr cl" data-mod="prod" data-k="{x}">
          {chip('novo', 'wn', 18)}<div class="mr-t"><b class="id">{x}</b>
          <span>{pt(r['prop_inedito'] * 100, 0)}% de problemas inéditos ·
            {pt(r['taxa_violacao'] * 100, 2)}% de violação</span></div>
          <span class="mr-v wn">{pt(r['nota'])}</span>
          <span class="sq">{ico('seta', 14)}</span></button>'''
          for x, r in lat.head(4).iterrows()) if len(lat) else vazio('escudo_ok',
            'Nenhum produto em risco latente', 'Todos os produtos com muito problema inédito '
            'já mostram violação compatível.')}
      </div>
    </div>
    <div class="cd">
      {cab('balanca', 'Os cinco componentes',
           'O que entra na nota, e por que cada um está lá.')}
      <div class="cps">
        <div class="cp"><b>Taxa de violação</b><span>o que já estourou o prazo</span></div>
        <div class="cp"><b>Problemas inéditos</b><span>quanto do que entra é problema novo,
          que viola 4,6 vezes mais</span></div>
        <div class="cp"><b>Fechados sem causa</b><span>quanto some do diagnóstico e volta
          depois</span></div>
        <div class="cp"><b>Duração mediana</b><span>quanto tempo o produto ocupa a
          operação</span></div>
        <div class="cp"><b>Tendência</b><span>se a taxa vem subindo ou caindo no ano</span></div>
      </div>
      <div class="nt">Cada componente vira posição relativa entre os dezessete e a nota é a
        média dessas posições. <b>Incidentes por ativo saiu</b> da conta: tinha correlação de
        0,85 com duração e estava contando a mesma coisa duas vezes.</div>
    </div>
  </div>'''


# ══════════ 4 · Causas e recorrentes ═══════════════════════════════════════
def aba_causas():
    lc = ''.join(
        f'<tr><td>{r["Código de fechamento"]}</td><td class="dm">{pt(r["% da base"])}%</td>'
        f'<td class="no">{pt(r["% das quebras"])}%</td><td>{pt(r["taxa de quebra %"], 2)}%</td>'
        f'<td class="dm">{pt(r["vezes a média"], 2)}x</td></tr>'
        for _, r in causas.head(7).iterrows())
    lr = ''.join(
        f'<div class="rc2" style="--i:{i}"><span class="rc2-t id">{r["problema"][:52]}</span>'
        f'<span class="rc2-m"><b>{mil(r["incidentes"])}</b> vezes · <b>{int(r["ativos"])}</b> '
        f'ativos · <b class="{"no" if r["quebras"] else "ok"}">{int(r["quebras"])}</b> '
        f'violações</span></div>' for i, (_, r) in enumerate(recor.head(6).iterrows()))
    return f'''
  {ato('01', 'Por que os incidentes fecham',
       'A causa registrada no fechamento serve a diagnóstico, não a previsão — ela só existe '
       'depois que o caso acabou.')}
  <div class="gr g2">
    <div class="cd">
      {cab('lupa', 'Causa de fechamento',
           'Quanto cada causa representa do volume e quanto representa das violações. Quando '
           'os dois não batem, há concentração de risco.')}
      <table class="tb sm"><thead><tr><th>Causa</th><th>% base</th><th>% violações</th>
        <th>Taxa</th><th>vs média</th></tr></thead><tbody>{lc}</tbody></table>
      <div class="nt"><b>Outro</b> responde por 7,8% do volume e 21,8% das violações. É o campo
        que mais esconde: quando o time não sabe classificar, a chance de ter estourado o prazo
        é quase três vezes a média.</div>
    </div>
    <div class="cd">
      {cab('tendencia', 'Problemas que mais repetem',
           'Texto do problema normalizado — número de chamado e código de ativo trocados por '
           'marcador, para agrupar o que é a mesma coisa.')}
      <div class="rcs">{lr}</div>
      <div class="nt">Os vinte mais recorrentes cobrem <b>26%</b> do volume e violam
        <b>0,40%</b>, menos da metade da média. São candidatos a <b>automação de resposta</b>:
        muito volume, pouco risco, resposta sempre igual.</div>
    </div>
  </div>

  {ato('02', 'O que isso muda na operação',
       'Volume e risco não são a mesma coisa, e tratar os dois igual desperdiça atenção.')}
  <div class="gr">
    <div class="cd dk">
      {cab('balanca', 'A leitura que o dado sustenta',
           'Três achados que mudam onde a equipe gasta tempo.')}
      <div class="ach">
        <div class="ac2"><b>Volume não prevê violação</b>
          <span>R² de 0,025 entre incidentes do dia e violações do dia. O volume dimensiona a
            equipe; ele não aponta o caso.</span></div>
        <div class="ac2"><b>O inédito viola 4,6 vezes mais</b>
          <span>Problema que nunca apareceu antes é o sinal mais forte que encontramos, e
            sobreviveu a sete verificações independentes.</span></div>
        <div class="ac2"><b>O recorrente é barato</b>
          <span>26% do volume com metade da taxa média. Automatizar resposta aqui libera gente
            para o que realmente arrisca.</span></div>
      </div>
    </div>
  </div>'''


# ══════════ 5 · Previsão de volume ═════════════════════════════════════════
def aba_previsao():
    prox = ''.join(
        f'<tr><td>{LBL_DIA[r["dia"].dayofweek]}</td><td class="dm">{dm(r["dia"])}</td>'
        f'<td><b>{pt(r["valor"], 0)}</b></td>'
        f'<td class="dm">{pt(r["baixo"], 0)} a {pt(r["alto"], 0)}</td>'
        f'<td class="dm">{pt(r["alto"] - r["baixo"], 0)}</td></tr>'
        for _, r in FUT3.head(8).iterrows())
    mx = SEMANA.max()
    barras = ''.join(
        f'<div class="sm{" ag" if i == DIA_HOJE.dayofweek else ""}" '
        f'style="--h:{SEMANA[i] / mx * 100:.0f}%;--i:{i}"><i></i>'
        f'<span>{LBL_DIA[i]}</span><em>{pt(SEMANA[i], 0)}</em></div>' for i in range(7))
    return f'''
  {ato('01', 'Quanto trabalho vem',
       'Prophet treinado em 2025 com sazonalidade semanal e feriados nacionais, banda de 80%.')}
  <div class="gr">
    <div class="cd">
      {cab('previsao', 'Volume elegível por dia · P3',
           'A linha cheia é o medido. A pontilhada é a previsão e a área em volta é a margem '
           'de erro do modelo.')}
      {trilho(n_real=30, n_prev=8)}
      <div class="nt">Ontem entraram <b>{ONTEM_TOTAL}</b> elegíveis contra <b>{pt(BASE_20, 0)}</b>
        de média dos últimos vinte dias úteis. A banda é larga de propósito: fingir precisão em
        previsão diária de incidente seria desonesto.</div>
    </div>
  </div>

  <div class="gr g2">
    <div class="cd">
      {cab('calendario', 'Os próximos oito dias',
           'Valor central e faixa de cada dia. A última coluna é a largura da faixa: quanto '
           'maior, menos o modelo sabe.')}
      <table class="tb sm"><thead><tr><th>Dia</th><th>Data</th><th>Previsto</th><th>Faixa</th>
        <th>Largura</th></tr></thead><tbody>{prox}</tbody></table>
    </div>
    <div class="cd">
      {cab('tendencia', 'Carga por dia da semana',
           'Média de incidentes P3 por dia da semana em 2025. A barra azul é hoje.')}
      <div class="sms">{barras}</div>
      <div class="nt">A diferença que existe é <b>dia útil contra fim de semana</b>, não segunda
        contra quinta: sábado cai a <b>{pt(SEMANA[5], 0)}</b> e domingo a <b>{pt(SEMANA[6], 0)}</b>
        contra <b>{pt(SEMANA[:5].mean(), 0)}</b> nos dias úteis. É por isso que o modelo usa dia
        da semana e feriado como sinal, e não a data em si.</div>
    </div>
  </div>

  {ato('02', 'O que a previsão de volume não faz',
       'O limite do modelo, dito antes que alguém descubra sozinho.')}
  <div class="gr">
    <div class="cd">
      {cab('balanca', 'Volume dimensiona carga, não aponta o caso',
           'Testamos se dias mais cheios violam mais. Não violam.')}
      <div class="ml">
        {linha_metrica('tendencia', 'nt', 'Correlação entre volume do dia e violações do dia',
                       'R² de 0,025 — praticamente nenhuma relação', '0,025', '', '')}
        {linha_metrica('novo', 'nt', 'Acúmulo de fila prevendo violação',
                       'testado a pedido da mentoria: r = −0,139 em dias úteis', '−0,139', '', '')}
      </div>
      <div class="nt">Por isso existem dois modelos e não um. O Prophet responde
        <b>quanta gente escalar</b>. A regressão logística responde <b>em qual caso olhar</b>.
        Trocar um pelo outro é o erro mais comum nesse tipo de projeto.</div>
    </div>
  </div>'''


ABAS = [('hoje', 'Hoje', 'agora', aba_hoje),
        ('fila', 'Fila de risco', 'fila', aba_fila),
        ('saude', 'Saúde por produto', 'coracao', aba_saude),
        ('causas', 'Causas e recorrentes', 'lupa', aba_causas),
        ('previsao', 'Previsão de volume', 'previsao', aba_previsao)]
