# -*- coding: utf-8 -*-
"""Views do painel.

Cada aba e uma pagina propria com URL propria — dá para mandar o link da fila filtrada
por P2 para alguem. Os detalhes vem como fragmento, para o modal buscar sem recarregar.
"""
import json

from django.http import Http404, JsonResponse
from django.shortcuts import render

from . import graficos as g
from . import servicos as s


def _base(aba):
    p = s.resumo()
    return {'aba': aba, 'p': p, 'hoje': p['hoje'], 'ontem': p['ontem'], 'base': p['base']}


def _ola(x):
    """Uma prioridade contra a meta de quebras do ano: distancia e geometria da faixa.

    Panorama e Projecao mostram o mesmo fato em profundidades diferentes — o cartao da
    prioridade resume, a aba detalha. A conta mora aqui para as duas telas nao divergirem
    se o corte mudar.
    """
    at = s.atingimento(x['prioridade'], x['projecao'])
    at_ja = s.atingimento(x['prioridade'], x['ja'])

    # A referência deixa de ser o `meta` do parquet e passa a ser o teto do degrau de 100%, que
    # é a meta contratada de fato. O notebook 06 reduziu o KPI a um teto por prioridade e pegou
    # degraus DIFERENTES em cada uma: 200 no P3 é o teto dos 150%, 45 no P2 é o teto dos 75%.
    # Medir uma contra o degrau mais alto e a outra contra o mais baixo é o que fazia a tela
    # inverter os dois vereditos — P3 em âmbar valendo 125%, P2 em verde valendo 75%.
    ref = {**x, 'meta': at['teto_100']}
    d = at['teto_100'] - x['projecao']      # positivo = folga, negativo = estouro
    return {**x, **g.arco_meta(ref), **g.consumo_meta(ref),
            'regua': s.regua_ano(x),
            'meta': at['teto_100'], 'meta_parquet': x['meta'],
            'delta': abs(round(d, 1)), 'folga': d >= 0,
            'at': at, 'at_ja': at_ja,
            # o tom sai do degrau, e não de "passou do teto": 100% é a meta contratada, acima
            # dela o indicador está sendo batido, e 75% é o primeiro degrau de perda
            'tom': 'ok' if at['pc'] >= 100 else ('wn' if at['pc'] >= 75 else 'no')}


def _variante_regua(req):
    """Qual das três direções da régua do KPI renderizar.

    Fica em query param: a decisão acontece com o objeto no lugar e na largura em que ele vai
    viver — dentro da folha, que tem 620px — e não num mockup solto, que é onde esta decisão
    travou duas vezes.

    Padrão: `c`, a escada de degraus. Foi a que respondeu o defeito que motivou a revisão — a
    régua lia como invertida, e nas outras duas o sentido depende de ler um rótulo ("melhor",
    "pior") ou de acompanhar um eixo. Na de degraus a ALTURA é a nota, então "mais violação,
    menos nota" aparece antes de qualquer leitura. Medida na folha de 620px: 637px de altura
    contra 711 da tabela com trilho, e sem estouro horizontal em nenhuma das duas.
    """
    v = req.GET.get('regua', '')
    return v if v in ('a', 'b', 'c') else 'c'


def _entrada(aba):
    """Contexto da tela de entrada.

    Nasceu como construtor compartilhado por duas versões da tela em avaliação — a de coluna
    única e a de dois eixos — para as duas lerem as mesmas contas e nunca divergirem num número.
    A escolha ficou na coluna única, com a cabeça baixa da outra. Continua função separada da
    view porque é aqui que mora a composição de todos os blocos da entrada, e ler isso junto do
    `render` é mais fácil do que caçar em cinco lugares.
    """
    p = s.resumo()
    ac = p['acompanhamento']
    rg = s.reguas()
    # cada cartão de prioridade carrega os dois horizontes do MESMO assunto: quanto entra
    # hoje e se isso ainda cabe na meta do ano. A régua "contra o normal" saiu de dentro do
    # cartão — o selo dentro/fora do normal já é o veredito dela, e o detalhe mora na aba
    # Previsão. Quem quer o fechamento do ano em profundidade clica em Projeção.
    ola = {x['prioridade']: _ola(x) for x in p['projecao']}
    for x in rg:
        x['ola'] = ola[x['pri']]
    # o brief mostra UMA prioridade no cartão do ano: a mais apertada contra a própria meta.
    # A folga em porcentagem da meta, e não em quebras, porque a meta do P3 é 4x a do P2 e
    # comparar valor absoluto elegeria o P3 sempre.
    ola_ano = min(ola.values(), key=lambda x: (x['meta'] - x['projecao']) / x['meta'])
    alertas = s.alertas()
    # o veredito fala das duas prioridades juntas: dizer "dentro do normal" olhando só o
    # P3 e deixar o P2 fora seria esconder metade do KPI
    fora = [x['pri'] for x in rg if not x['normal']]
    # o corte no relógio não é detalhe: a tela se apresenta como sendo das 15h, e listar caso
    # aberto depois disso é mostrar futuro
    do_dia = s.fila_de_hoje(400, ate_hora=ac['hora_agora'])
    maior = max((f['risco'] for f in do_dia), default=0)
    dia_semana = rg[0]['dia_semana']
    ctx = _base(aba)
    ctx.update({
        'ac': ac,
        'ac2': p['acompanhamento_p2'],
        'reguas': rg,
        # as DUAS prioridades do KPI, uma placa cada, lado a lado e do mesmo tamanho. Era só o
        # P3 ocupando a largura inteira — e o P2, que também entra no KPI e tem meta própria,
        # aparecia na tela apenas como um número previsto, sem curva para comparar contra ele.
        #
        # viewBox de 640: com as duas placas lado a lado cada uma ocupa ~900px na tela, e um
        # viewBox largo demais achata a curva a ponto de a diferença entre previsto e realizado
        # sumir na espessura do traço.
        'acomp': g.acompanhamento(ac, w=640, h=230),
        'acomp2': g.acompanhamento(p['acompanhamento_p2'], w=640, h=230),
        # o título fala do volume das DUAS prioridades juntas: dizer "dentro do normal"
        # olhando só o P3 e deixar o P2 fora seria esconder metade do KPI
        'titulo': ('Dia dentro do normal' if not fora
                   else 'Volume fora do normal no ' + ' e no '.join(fora)),
        'sub': (f'Volume de uma {dia_semana} comum nas duas prioridades do KPI.'
                if not fora else
                f'Comparado a uma {dia_semana} típica nas prioridades do KPI.'),
        # o que a navbar não dá: os casos concretos que pedem ação hoje
        'fila': do_dia[:6],
        'n_hoje': len(do_dia),
        # o tamanho da fila do trimestre inteiro, só para o link dizer que ele troca a
        # população. Sem isso o leitor sai daqui vendo 8,1% como maior risco e chega numa tela
        # cujo topo passa de 60% — dois números certos que, sem escopo escrito, leem como erro.
        'fila_total': s.fila_total(),
        'maior_hoje': maior,
        # a régua contra a qual o bloco da fila compara o maior caso do dia: a taxa média da
        # base e o corte da faixa crítica, ambos na mesma escala das barras. É o que responde
        # "8,1% é muito?" sem precisar do parágrafo que respondia isso em prosa.
        #
        # `g.cd` e não número cru: valor que entra em `style` tem de ser string com ponto
        # decimal, senão a localização pt-BR devolve "width:9,7%" e o navegador ignora a regra.
        'media_x': g.cd(p['base']['media_violacao'] / s.CORTE_CRITICO * 100),
        'corte_critico': s.CORTE_CRITICO,
        # de que LADO da faixa o ritmo do dia está caindo. "fora da faixa" não distingue: às 15h
        # o ritmo projeta 58,3 contra faixa de 58,8 a 95,9, ou seja meio incidente abaixo do
        # piso — dia mais calmo que o previsto, e não alarme. Escrever só "fora" faria o leitor
        # supor o pior lado, que é o único que a palavra sugere.
        'ritmo_lado': 'abaixo' if ac['ritmo_fecha'] < p['hoje']['baixo_p3'] else 'acima',
        # `calmo` tinge o selo do bloco "Onde agir agora" no Panorama
        'calmo': not any(f['risco'] >= 10 for f in do_dia),
        'alertas': alertas,
        # o cartão do ano e a contagem do selo de atenção da cabeça
        'ola_ano': ola_ano,
        'n_atencao': len(alertas) + (0 if ola_ano['folga'] else 1),
        # o que não muda de um dia para o outro, e por isso não vira manchete: o produto que
        # está pior no ranking e a causa que concentra quebra acima do peso dela na base
        'pior': s.pior_produto(),
        'causa': s.pior_causa(),
    })
    return ctx


def panorama(req):
    """A porta de entrada. Coluna única, na ordem em que a decisão acontece dentro de um turno:
    como está o dia, o que pede ação agora, quanto do teto do ano já foi gasto, onde o problema
    mora. A fila vem antes do ano porque é a única coisa da tela em que dá para agir hoje."""
    return render(req, 'painel/panorama.html', _entrada('panorama'))


def projecao(req):
    """O fechamento do ano contra a meta — saída do notebook 06.

    Morava espremida no terceiro ato da antiga aba Hoje. Ganhou página porque é análise
    própria: sair do Panorama sem ter para onde ir a deixaria órfã.
    """
    p = s.resumo()
    ctx = _base('projecao')
    # a régua do KPI viaja dentro de cada prioridade: é ela que deixa o leitor conferir de onde
    # saiu o atingimento do selo, em vez de aceitar o número
    # ordem canônica, e não a ordem em que o parquet gravou: a aba abria com P2 enquanto
    # Panorama e Previsão abriam com P3, na mesma sessão
    ctx.update({
        'projecao': [dict(_ola(x), escada=s.escada_tabela(x), marcas=s.escada_marcas(x))
                     for x in s.por_prioridade(p['projecao'])],
    })
    return render(req, 'painel/projecao.html', ctx)


def fila(req):
    """Os casos abertos hoje, do mais arriscado para o menos.

    A aba perdeu o painel do ganho do modelo — "27× · 13 das 50 violações do trimestre". Aquilo
    é avaliação medida em outubro a dezembro, ou seja, no futuro do relógio da tela, e o lugar
    disso é a apresentação. A paginação também saiu: 49 casos em páginas de 40 deixavam nove
    numa segunda página.
    """
    pri = req.GET.get('pri', '')
    dados = s.fila_pagina(prioridade=pri, faixa=req.GET.get('faixa', ''),
                          busca=req.GET.get('q', ''), pagina=1, por_pagina=500)
    ctx = _base('fila')
    ctx.update({
        **dados,
        # os chips leem o MESMO filtro de prioridade da tabela: sem isso, filtrar P2 dava uma
        # lista de 9 linhas com chips que continuavam somando 49
        'faixas': s.contagem_por_faixa(pri),
        'resumo_fila': s.resumo_fila(),
        'n_ate_agora': len(s.fila_ate_agora()),
        'hora_corte': s.painel()['acompanhamento']['hora_agora'],
        'pri': pri, 'faixa_sel': req.GET.get('faixa', ''),
        'q': req.GET.get('q', ''),
    })
    return render(req, 'painel/fila.html', ctx)


def saude(req):
    """A nota de saúde por produto — o segundo diferencial declarado do produto.

    O filtro por quadrante saiu: cinco botões com recarga de página inteira para filtrar uma
    tabela de 15 linhas que cabe na tela, e cujo estado vazio era inalcançável porque os quatro
    quadrantes têm produto em todos.
    """
    lista = s.saude_lista()
    b = s.painel()['base']
    ctx = _base('saude')
    ctx.update({
        'lista': lista,
        'total': len(lista),
        'latentes': [x for x in lista if x['quadrante'] == 'risco latente'],
        # o veredito da aba, antes das quinze linhas: quantos estão abaixo do meio da régua e
        # qual é o pior. Sem ele, o leitor tem de formar o resumo sozinho.
        'abaixo_40': [x for x in lista if x['nota'] < 40],
        'pior': lista[-1],
        'volume': sum(x['incidentes'] for x in lista),
        'elegiveis': b['elegiveis'],
    })
    return render(req, 'painel/saude.html', ctx)


def causas(req):
    """Notebook 05. Onde o diagnóstico falha, e o que vale automatizar.

    A tabela passou a sair ordenada por TAXA, e não por volume. Ordenada por volume e cortada
    em oito, ela eliminava Falha de Hardware — a maior taxa da janela, 8,24%, 8,75 vezes a
    média — porque é 0,4% do volume. O bloco existe para mostrar onde volume e risco não
    coincidem, e o corte removia justamente os casos em que eles não coincidem.
    """
    p = s.resumo()
    rec = p['recorrentes']
    vol = sum(r['incidentes'] for r in rec)
    quebras = sum(r['quebras'] for r in rec)
    # Todas as categorias, sem piso de volume. Um piso de cem incidentes escondia justamente a
    # Falha de Hardware — 85 casos, 7 violações, 8,24% de taxa — que é o exemplo que motiva
    # ordenar por taxa em vez de volume. A coluna de incidentes está na tela ao lado da taxa, e
    # é ela que deixa o leitor pesar quantos eventos sustentam cada percentual.
    tabela = sorted(p['causas'], key=lambda c: c['taxa de quebra %'], reverse=True)
    ctx = _base('causas')
    ctx.update({
        'causas': tabela,
        'n_causas': len(tabela),
        'recorrentes': rec,
        # os dois códigos que não descrevem defeito: registram que o caso foi encerrado sem
        # causa identificada, e a tela precisa dizer isso onde eles aparecem
        'sem_causa': ['Outro', 'Falha não reproduzida'],
        # a nota do rodapé fala de "sem causa identificada", então o número tem de vir DESSA
        # linha. Vinha do máximo de "vezes a média", que hoje é Falha de Hardware — texto de um
        # assunto com o número de outro.
        'outro': next((c for c in tabela
                       if c['Código de fechamento'] == 'Outro'), None),
        'pior_causa': max(p['causas'], key=lambda c: c['vezes a média']),
        'rec_n': len(rec),
        'rec_pc_vol': round(vol / p['base']['elegiveis'] * 100, 1),
        'rec_pc_quebra': round(quebras / vol * 100, 2) if vol else 0,
        'rec_vol': vol,
        'elegiveis': p['base']['elegiveis'],
    })
    return render(req, 'painel/causas.html', ctx)


def previsao(req):
    """Notebook 03. O herói é a máquina do tempo: o modelo medindo a si mesmo, dia a dia.

    `?v=b` mostra a reconstrução da aba enquanto a escolha entre as duas não está feita.

    A versão B é fundada num achado que a versão A tinha no dado e não contava: o volume real
    caiu ao longo do trimestre de teste — 54,5 P3/dia em outubro, 39,5 em novembro, 34,2 em
    dezembro — e a previsão ficou parada em torno de 62. A cobertura da faixa desaba junto:
    90,3%, 53,3%, 35,5%. O mecanismo é rastreável a uma decisão declarada do projeto: o Prophet
    roda com sazonalidade anual desligada, porque há um ano só de base elegível, e foi treinado
    até setembro. Queda de fim de ano está fora do que ele pode ter aprendido.
    """
    p = s.resumo()
    t = p['trilho']
    ctx = _base('previsao')

    # a média histórica do dia da semana viaja junto de cada dia previsto. É ela que mostra que
    # a previsão de um dia É a sazonalidade semanal mais uma tendência: os "próximos oito dias"
    # e a "carga por dia da semana" eram, por construção, o mesmo fato em dois formatos.
    med3 = {x['dia']: x['media'] for x in p['semana']}
    med2 = {x['dia']: x['media'] for x in p['semana_p2']}
    prox3 = [dict(x, media_semana=med3.get(x['rot'], 0)) for x in t['previsto'][:8]]
    prox2 = [dict(x, media_semana=med2.get(x['rot'], 0)) for x in t['previsto_p2'][:8]]

    # o dia mais cheio e o mais vazio dos próximos sete, somando as DUAS prioridades do KPI.
    # É a leitura de escala de equipe: em que dia colocar gente a mais, e em que dia não.
    # Somado, e não só P3, porque quem monta plantão atende os dois.
    proximos = [{'rot': a['rot'], 'dm': a['dm'],
                 'baixo': a['baixo'] + b['baixo'], 'alto': a['alto'] + b['alto']}
                for a, b in zip(prox3[:7], prox2[:7])]

    ctx.update({
        'pico': max(proximos, key=lambda d: d['alto']),
        'vale': min(proximos, key=lambda d: d['alto']),
        # o desenho que existe no relógio da tela: histórico até 30/09 emendado na previsão,
        # uma placa por prioridade do KPI
        'tr3': g.trilho(t['realizado'], t['previsto'], w=640, h=210, n_real=30, n_prev=14),
        'tr2': g.trilho(t['realizado_p2'], t['previsto_p2'], w=640, h=210, n_real=30, n_prev=14),
        'ac': p['acompanhamento'], 'ac2': p['acompanhamento_p2'],
        'hoje': p['hoje'],
        'semana': p['semana'], 'semana_p2': p['semana_p2'],
        'prox3': prox3, 'prox2': prox2,
        # Escala PRÓPRIA por prioridade, e o teto dela escrito no cartão.
        #
        # Com escala compartilhada o P2 vira uma fileira de tocos — ele é cerca de um quinto do
        # P3 em volume — e o que esses dois blocos existem para mostrar é a FORMA, não o nível:
        # onde a semana cai, quanto o intervalo é largo. O nível já está comparado na cabeça, em
        # 77,4 contra 15,8. Escala compartilhada aqui esconderia o achado de que a queda de fim
        # de semana do P2 é bem mais suave que a do P3.
        'max_semana': max(x['media'] for x in p['semana']),
        'max_semana2': max(x['media'] for x in p['semana_p2']),
        'max_prox': max(x['alto'] for x in prox3),
        'max_prox2': max(x['alto'] for x in prox2),
    })
    return render(req, 'painel/previsao.html', ctx)


# ── fragmentos que o modal busca ───────────────────────────────────────────
def det_incidente(req, codigo):
    inc = s.incidente(codigo)
    if not inc:
        raise Http404('incidente não encontrado')
    return render(req, 'painel/_det_incidente.html',
                  {'c': inc, 'base': s.painel()['base'],
                   'hist': g.barras_mes(inc['hist_ativo']), 'meses': s.painel()['meses']})


def det_ativo(req, codigo):
    a = s.ativo(codigo)
    if not a:
        raise Http404('ativo não encontrado')
    return render(req, 'painel/_det_ativo.html',
                  {'a': a, 'base': s.painel()['base'],
                   'hist': g.barras_mes(a['hist']), 'meses': s.painel()['meses']})


def det_meta(req, pri):
    """A regra do KPI de uma prioridade. Saiu do corpo da Projeção e virou aprofundamento.

    Ocupava o último terço dos dois cartões com doze linhas de tabela, para explicar uma regra
    que não muda de um dia para o outro. Quem abre a Projeção quer saber onde o ano fecha; a
    régua só é consultada por quem duvida do número — e para esse, um clique basta.
    """
    x = next((y for y in s.resumo()['projecao'] if y['prioridade'] == pri.upper()), None)
    if not x:
        raise Http404('prioridade não encontrada')
    o = dict(_ola(x), escada=s.escada_tabela(x), marcas=s.escada_marcas(x))
    return render(req, 'painel/_det_meta.html',
                  {'o': o, 'regua': _variante_regua(req)})


def det_produto(req, codigo):
    p = s.produto(codigo)
    if not p:
        raise Http404('produto não encontrado')
    return render(req, 'painel/_det_produto.html', {'p': p, 'total': len(s.painel()['saude'])})


def busca(req):
    return JsonResponse({'itens': s.indice_busca()})
