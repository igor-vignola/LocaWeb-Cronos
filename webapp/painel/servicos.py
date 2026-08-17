# -*- coding: utf-8 -*-
"""Camada de servico: le o pacote de dados e devolve estrutura pronta para a view.

O conteiner nao treina nada. Prophet e scikit-learn rodam nos notebooks, gravam parquet,
e o script gera_dados_app.py agrega tudo em data/app. Aqui so se abre arquivo.

O pacote e carregado uma vez por processo e fica em memoria: sao 60 kB de JSON e um
parquet de 5.183 linhas, entao nao ha motivo para reler a cada requisicao.
"""
import json
from functools import lru_cache
from pathlib import Path

import pandas as pd
from django.conf import settings

DADOS = Path(settings.DADOS_DIR)

# mesma razao da coordenada de SVG: numero que entra em atributo `style` tem de sair como texto
# com ponto decimal. O Django localiza numero em template conforme LANGUAGE_CODE, e em pt-BR
# `width:81.3%` vira `width:81,3%` — declaracao invalida, que o navegador descarta em silencio.
from .graficos import cd as _css                                       # noqa: E402

DIAS_SEMANA = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']
MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto',
         'setembro', 'outubro', 'novembro', 'dezembro']
# (piso, teto, nome, tom, glifo). O glifo escala junto com o risco e monta uma escada que se le
# sem legenda: escudo fechado, relogio, raio, triangulo. Duas faixas dividem o tom ambar — alta e
# atencao — e sem o glifo elas ficavam com o mesmo selo mudando so a palavra.
#
# `alta` usa raio e nao `prazo`: prazo e relogio sao os dois um circulo com ponteiros, e a 12px de
# selo ficam indistinguiveis. Glifo que nao se diferencia no tamanho em que e usado nao e glifo.
FAIXAS = [(10, 1e9, 'crítica', 'no', 'alerta'), (5, 10, 'alta', 'wn', 'raio'),
          (1, 5, 'atenção', 'wn', 'relogio'), (0, 1, 'rotina', 'ok', 'escudo_ok')]
# o corte da faixa critica e a regua da fila: o risco de um caso so quer dizer alguma coisa
# contra a distancia que falta para ele virar critico
CORTE_CRITICO = FAIXAS[0][0]
# o que fazer com um caso daquela faixa. A fila respondia "quanto" e nao respondia "e dai" —
# e "e dai" e a unica pergunta que um plantao faz diante de uma lista.
ACOES = {'crítica': 'Ação imediata', 'alta': 'Priorizar no turno',
         'atenção': 'Acompanhar no turno', 'rotina': 'Sem ação específica'}

# ── a ordem em que as duas prioridades do KPI aparecem, em TODA a aplicação ──
# Cada tela resolvia isso por conta própria e o resultado eram duas convenções vivas ao mesmo
# tempo: Panorama e Previsão abriam com P3, Projeção e Fila abriam com P2. A regra do projeto é
# dar o mesmo peso às duas — o que não significa alternar a ordem, e sim fixá-la, para o olho
# encontrar a mesma prioridade no mesmo lugar em qualquer aba.
#
# P3 primeiro porque é cerca de cinco vezes o P2 em volume e concentra a fila do turno. Para
# inverter a convenção inteira, basta trocar esta linha.
ORDEM_PRI = ('P3', 'P2')


def por_prioridade(itens, chave='prioridade'):
    """Ordena qualquer lista de dicionários pela ordem canônica das prioridades."""
    return sorted(itens, key=lambda x: ORDEM_PRI.index(x[chave])
                  if x.get(chave) in ORDEM_PRI else len(ORDEM_PRI))


@lru_cache(maxsize=1)
def painel():
    """O pacote agregado. Tudo que nao e linha da fila esta aqui."""
    return json.loads((DADOS / 'painel.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def dias():
    """Os 92 dias do trimestre com previsão, real, veredito e taxa acumulada."""
    return json.loads((DADOS / 'dias.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def fila():
    """A fila pontuada, 5.183 linhas. Os sinais vem como JSON dentro da coluna."""
    df = pd.read_parquet(DADOS / 'fila.parquet')
    df['sinais'] = df['sinais'].map(json.loads)
    df['ativo'] = df['ativo'].replace('None', '')
    df['dm'] = df['dia'].dt.strftime('%d/%m')
    return df


# ── formatacao pt-BR, usada tambem pelos templates via filtro ──────────────
def num(v, casas=1):
    return f'{float(v):.{casas}f}'.replace('.', ',')


def mil(v):
    return f'{int(v):,}'.replace(',', '.')


def faixa_de(risco):
    return next(f for f in FAIXAS if f[0] <= risco < f[1])


# ── a escada de atingimento do KPI ─────────────────────────────────────────
# (teto de quebras, % de atingimento). Vem do dicionario oficial da Locaweb.
#
# O sistema tratava isso como teto binario — 200 no P3, 45 no P2 — e o efeito era inverter o
# veredito das duas prioridades ao mesmo tempo: 208 quebras de P3 apareciam em ambar, como
# estouro, quando 208 esta na faixa de 201 a 230 e vale 125% de atingimento; e 43,5 de P2
# apareciam em verde, como folga, quando 43,5 esta na faixa de 40 a 45 e vale 75% — o degrau
# mais baixo antes de 50%. A tela mandava correr atras da prioridade que ia bem e ignorar a
# unica sob pressao.
ESCADA = {
    'P2': [(30, 150), (35, 125), (39, 100), (45, 75), (53, 50), (float('inf'), 0)],
    'P3': [(200, 150), (230, 125), (263, 100), (290, 75), (320, 50), (float('inf'), 0)],
}


def atingimento(pri, quebras):
    """Em que degrau da escada do KPI aquele numero de quebras cai.

    Devolve o degrau atual, o proximo degrau abaixo e quantas quebras ainda cabem antes de
    escorregar para ele — que e a leitura que a operacao usa: nao "estourou ou nao", e sim
    "quanto de margem ainda tenho no degrau em que estou".
    """
    degraus = ESCADA[pri]
    for i, (teto, pc) in enumerate(degraus):
        if quebras <= teto:
            piso = degraus[i - 1][0] + 1 if i else 0
            proximo = degraus[i + 1][1] if i + 1 < len(degraus) else None
            return {
                'pc': pc,                                   # atingimento do degrau atual
                'piso': piso,
                'teto': teto if teto != float('inf') else None,
                'proximo_pc': proximo,                      # o degrau logo abaixo
                # quantas quebras ainda cabem antes de cair de degrau
                'margem': round(teto - quebras, 1) if teto != float('inf') else None,
                # o teto do degrau de 100%, que e a meta contratada de fato
                'teto_100': next(t for t, p in degraus if p == 100),
            }
    return {'pc': 0, 'piso': 0, 'teto': None, 'proximo_pc': None, 'margem': None,
            'teto_100': next(t for t, p in degraus if p == 100)}


# os cinco componentes da nota, com o rotulo de tela e como cada valor se le
COMPONENTES = [
    ('taxa_violacao', 'Taxa de violação', 'pc'),
    ('prop_inedito', 'Problemas inéditos', 'pc'),
    ('prop_sem_causa', 'Fechados sem causa', 'pc'),
    ('duracao_mediana_h', 'Duração mediana', 'h'),
    ('tendencia', 'Tendência da taxa', 'pp'),
]


def saude_lista():
    """O ranking de produtos com a explicabilidade DENTRO da linha.

    A promessa declarada do diferencial e "ranking, tendencia e explicabilidade". As duas
    primeiras estavam na tela; a terceira vivia atras de um clique de mouse, num modal que
    listava os cinco componentes em ordem fixa. A pergunta que o leitor faz diante de um ranking
    e "por que este esta mal?", e ela merece resposta na propria linha.

    `pos_*` e a posicao relativa do produto naquele componente, de 0 a 1, onde MAIOR e pior — a
    nota e a media das cinco, invertida. O componente de maior posicao e o que mais puxa a nota
    para baixo.
    """
    # rotulos curtos para a coluna de situacao: "problema conhecido e recorrente" tem 31
    # caracteres em caixa alta de 9,5px e estoura a celula
    curto = {'problema já materializado': 'Já materializado',
             'problema conhecido e recorrente': 'Recorrente',
             'risco latente': 'Risco latente', 'estável': 'Estável'}

    # ── a cor de cada equipe ────────────────────────────────────────────────────
    # O selo do produto carrega a EQUIPE que atende, e a cor é o que faz dois produtos do mesmo
    # time ficarem visivelmente parentes numa lista de quinze códigos de quatro letras.
    #
    # A primeira versão derivava a matiz de um hash do nome — e falhou no caso que mais importa:
    # "Team14" e "Team11" compartilham cinco dos seis caracteres, então o acumulador só divergia
    # no último e as duas equipes saíam a três graus de distância. Cor de identidade que não
    # distingue as duas equipes mais frequentes da base não distingue nada.
    #
    # Aqui a matiz vem da POSIÇÃO no conjunto ordenado de equipes, com passo no ângulo áureo:
    # índices vizinhos caem em lados opostos do círculo de cor, e a separação se mantém
    # independentemente de quantas equipes existam. Ordenado por nome, é determinístico.
    equipes = sorted({x.get('equipe') for x in painel()['saude'] if x.get('equipe')})
    matiz = {e: round(i * 137.508) % 360 for i, e in enumerate(equipes)}

    fora = []
    for x in sorted(painel()['saude'], key=lambda y: y['posicao']):
        pior = max(COMPONENTES, key=lambda c: x.get(f'pos_{c[0]}') or 0)
        campo, rotulo, forma = pior
        v = x.get(campo) or 0
        equipe = x.get('equipe') or ''
        pos = round((x.get(f'pos_{campo}') or 0) * 100)
        # "percentil 93" é a palavra do notebook, e no turno ninguém lê percentil. Aqui ela vira
        # a POSIÇÃO, que é o que o número já é: `pos_*` no parquet é rank/n exato — os quinze
        # produtos ocupam 6,7 · 13,3 · 20,0 … 100,0 em qualquer componente. Então `rank` é
        # recuperado sem aproximação nenhuma, e 100 quer dizer "o pior dos quinze".
        #
        # A primeira tentativa foi uma faixa qualitativa ("entre os piores do conjunto"), e ela
        # colapsou: como a coluna mostra sempre o PIOR componente do produto, a posição é alta
        # por construção e onze das quinze linhas diziam a mesma frase.
        n = len(painel()['saude'])
        rank = n - round(pos * n / 100) + 1
        fora.append({
            **x,
            'equipe_h': matiz.get(equipe, 220),
            # "Team14" -> "14": o prefixo é igual em todas e só gasta espaço no selo
            'equipe_curta': equipe.replace('Team', '') or '—',
            'pior_rot': rotulo,
            'pior_pos': pos,
            'pior_faixa': (f'o pior dos {n}' if rank == 1 else f'{rank}º pior de {n}'),
            # "p.p." é abreviação de estatística. Por extenso ocupa quatro caracteres a mais e
            # não precisa ser decodificada.
            'pior_val': (f'{v * 100:.1f}'.replace('.', ',') + '%' if forma == 'pc'
                         else (f'{v:.1f}'.replace('.', ',') + 'h' if forma == 'h'
                               else f'{v * 100:+.2f}'.replace('.', ',') + ' pontos')),
            'situacao': curto.get(x['quadrante'], x['quadrante'].capitalize()),
            # a duracao de alguns produtos e artefato de encerramento automatico, e a tela tem
            # de dizer isso onde o numero aparece
            'duracao_longa': (x.get('duracao_mediana_h') or 0) > 24,
        })
    # a mediana das notas: e contra ela que a barra compara, porque a nota e relativa ao
    # conjunto. Comparar com zero nao significa nada num indice de percentis.
    notas = sorted(x['nota'] for x in fora)
    med = notas[len(notas) // 2] if len(notas) % 2 else (notas[len(notas) // 2 - 1]
                                                         + notas[len(notas) // 2]) / 2
    for x in fora:
        x['mediana'] = round(med, 1)
    return fora


def escada_tabela(x):
    """A escada do KPI de UMA prioridade, em tabela.

    Uma linha por degrau de atingimento, com a faixa de quebras que vale aquele degrau e as
    marcas de onde o ano esta hoje e onde a projecao cai. E o que transforma a regua num
    instrumento em vez de uma nota de rodape: o cartao responde "quanto" e a tabela responde
    "por que esse veredito" — sem ela, "75% de atingimento" e um numero que o leitor aceita
    sem conferir.
    """
    degraus = ESCADA[x['prioridade']]
    # o fim da escala das variantes que desenham a faixa em largura real: o teto do último
    # degrau fechado, com 9% de folga para o degrau aberto ("Mais de 320") ter corpo
    fim = max(t for t, _ in degraus if t != float('inf')) * 1.09
    linhas = []
    for i, (teto, pc) in enumerate(degraus):        # do maior atingimento para o menor
        piso = degraus[i - 1][0] + 1 if i else 0
        aberto = teto == float('inf')
        linhas.append({
            'pc': pc,
            'k': 'ok' if pc >= 100 else ('wn' if pc >= 75 else 'no'),
            'rot': (f'Mais de {degraus[i - 1][0]}' if aberto
                    else (f'Até {teto}' if not i else f'{piso} a {teto:.0f}')),
            'hoje': piso <= x['ja'] <= (1e9 if aberto else teto),
            'proj': piso <= x['projecao'] <= (1e9 if aberto else teto),
            # ── geometria, para as variantes que desenham a escada em vez de listá-la ──
            # `alt` é a ALTURA do degrau como fração da nota: é o que faz "mais violação, menos
            # nota" virar forma. O piso de 12 existe para o degrau de 0% continuar visível.
            'alt': _css(12 + pc / 150 * 88),
            'ini': _css((0 if not i else degraus[i - 1][0]) / fim * 100),
            'larg': _css(((fim if aberto else teto) - (0 if not i else degraus[i - 1][0]))
                         / fim * 100),
            'teto_num': None if aberto else teto,
        })
    return linhas


def escada_marcas(x):
    """Onde hoje, a projecao e a meta caem na MESMA escala de violacoes da escada.

    Serve as variantes que desenham a escada num eixo continuo: sem isso, cada template
    recalcularia o fim da escala por conta propria e as duas leituras divergiriam por
    arredondamento.
    """
    degraus = ESCADA[x['prioridade']]
    fim = max(t for t, _ in degraus if t != float('inf')) * 1.09
    meta = next(t for t, p in degraus if p == 100)
    pos = lambda v: _css(min(100.0, max(0.0, v / fim * 100)))          # noqa: E731
    return {'ja_x': pos(x['ja']), 'proj_x': pos(x['projecao']),
            'baixo_x': pos(x['baixo']), 'alto_x': pos(x['alto']),
            'faixa_w': _css(max(0.0, (x['alto'] - x['baixo']) / fim * 100)),
            'meta_x': pos(meta), 'meta': meta, 'fim': round(fim),
            # a altura do degrau de 100% na variante de degraus, para a linha da meta pousar
            # exatamente no topo dele. Mesma fórmula do `alt` de escada_tabela — declarada uma
            # vez, e não repetida em CSS, onde ela viraria número mágico.
            'alt_meta': _css(12 + 100 / 150 * 88)}


def regua_ano(x):
    """Uma barra que responde tres perguntas, nesta ordem: quanto ja teve, qual o maximo, e
    quanto esta projetado.

    Foi uma escada de seis degraus antes disto, com cada faixa de atingimento desenhada em
    escala. Era fiel ao KPI e ilegivel: seis blocos, duas marcas e um intervalo tracejado para
    dizer uma coisa que cabe numa barra. Quem opera nao precisa ver os seis degraus — precisa
    saber quanto ja gastou do orcamento de quebras do ano e se a projecao cabe nele.

    A escada continua existindo no dado, em `atingimento()`, que e de onde sai o veredito.
    """
    alvo = next(t for t, p in ESCADA[x['prioridade']] if p == 100)   # teto do degrau de 100%
    fim = max(x['alto'], alvo) * 1.12
    pos = lambda v: _css(min(100, max(0, v / fim * 100)))
    return {
        'alvo': alvo,
        'fim': round(fim),
        # A BARRA E A DECOMPOSICAO. Tres segmentos emendados que somam a projecao: o que ja
        # aconteceu, o risco da fila aberta no corte e o volume que ainda entra. Eram uma barra
        # e uma lista separada dizendo a mesma conta em dois lugares.
        'ja_w': pos(x['ja']),
        'proj_x': pos(x['projecao']),
        'alvo_x': pos(alvo),
        'baixo_x': pos(x['baixo']),
        'faixa_w': _css(max(0, (x['alto'] - x['baixo']) / fim * 100)),
        # quanto ainda cabe ate o maximo, quanto a projecao passa dele, e o incremento previsto
        'cabem': round(alvo - x['ja'], 1),
        'passa': round(x['projecao'] - alvo, 1),
        'a_mais': round(x['projecao'] - x['ja'], 1),
        'estoura': x['projecao'] > alvo,
    }


# ── consultas que as views usam ────────────────────────────────────────────
def resumo():
    p = painel()
    d = pd.Timestamp(p['hoje']['dia'])
    p['hoje']['dm'] = f'{d.day:02d}/{d.month:02d}'
    p['hoje']['completo'] = f'{d.day:02d}/{d.month:02d}/{d.year}'
    # a data por extenso, para a sobrancelha. "01/10/2025 · carga de 30/09 · 23h59" era duas datas
    # e um horario de carga na mesma dobra, e nenhum deles e o que o leitor quer saber: ele quer
    # saber que dia e hoje.
    # o primeiro dia do mes se escreve com ordinal em portugues: "1º de outubro", nao "1 de
    # outubro". E justamente o dia em que o relogio do sistema esta parado, entao a forma errada
    # aparecia na sobrancelha, na barra do topo e no rodape de todas as abas.
    dia_ord = '1º' if d.day == 1 else str(d.day)
    p['hoje']['extenso'] = f'{dia_ord} de {MESES[d.month - 1]} de {d.year}'
    # a versao curta serve a barra do topo, que divide espaco com o controle de tempo. O ano mora
    # no rodape e na sobrancelha; repeti-lo em terceiro lugar nao acrescenta nada.
    p['hoje']['dia_mes'] = f'{dia_ord} de {MESES[d.month - 1]}'
    p['hoje']['dia_semana'] = DIAS_SEMANA[d.dayofweek]
    p['hoje']['largura_p3'] = round(p['hoje']['alto_p3'] - p['hoje']['baixo_p3'], 1)
    p['hoje']['largura_p2'] = round(p['hoje']['alto_p2'] - p['hoje']['baixo_p2'], 1)
    # as DUAS series previstas recebem o mesmo tratamento. So o P3 passava por aqui, e a serie
    # do P2 chegava aos templates sem `dm`, `rot` nem `largura` — quem a usasse quebrava.
    #
    # `ponto`, e nao `d`: o laco reaproveitava o nome do Timestamp de hoje e o deixava valendo um
    # dicionario dali para baixo. Ninguem usava `d` depois, mas a proxima linha acrescentada ali
    # quebraria por um motivo que nao esta a vista.
    for serie in ('previsto', 'previsto_p2'):
        for ponto in p['trilho'].get(serie, []):
            dd = pd.Timestamp(ponto['dia'])
            ponto['dm'] = f'{dd.day:02d}/{dd.month:02d}'
            ponto['rot'] = DIAS_SEMANA[dd.dayofweek][:3]
            ponto['largura'] = round(ponto['alto'] - ponto['baixo'], 1)
    o = pd.Timestamp(p['ontem']['dia'])
    p['ontem']['dm'] = f'{o.day:02d}/{o.month:02d}'
    return p


def regua(pri='P3'):
    """Hoje contra o normal, para uma prioridade. Um numero solto nao diz se esta alto.

    ATENCAO AO ESCOPO: cada regua compara dentro da propria prioridade.
    `base['base_20_dias']` existe e parece servir, mas e todas as prioridades — comparar o
    previsto do P3 contra ela infla a conta e foi o defeito da v1 desta tela. Nao usar.
    """
    p = painel()
    hoje = pd.Timestamp(p['hoje']['dia'])
    k = pri.lower()
    prev = p['hoje'][f'previsto_{k}']
    serie = p['trilho']['realizado' if pri == 'P3' else 'realizado_p2']
    semana = p['semana' if pri == 'P3' else 'semana_p2']
    real = pd.DataFrame(serie)
    real['dia'] = pd.to_datetime(real['dia'])
    util = real[real['dia'].dt.dayofweek < 5]

    refs = []
    rot_dia = DIAS_SEMANA[hoje.dayofweek]
    media_dia = next((s['media'] for s in semana if s['dia'] == rot_dia[:3]), None)
    if media_dia:
        refs.append({'rot': f'média de {rot_dia}', 'det': 'em 2025', 'valor': media_dia,
                     'media': True})

    passada = real[real['dia'] == hoje - pd.Timedelta(days=7)]
    if not passada.empty:
        d = (hoje - pd.Timedelta(days=7))
        refs.append({'rot': f'{rot_dia} passada', 'det': f'{d.day:02d}/{d.month:02d}',
                     'valor': float(passada.iloc[0]['valor']), 'media': False})

    if len(util):
        ini = util['dia'].min()
        refs.append({'rot': 'média recente', 'valor': round(float(util['valor'].mean()), 1),
                     'det': f'{len(util)} dias úteis desde {ini.day:02d}/{ini.month:02d}',
                     'media': True})

    for r in refs:
        r['delta'] = round((prev - r['valor']) / r['valor'] * 100, 1)
        r['acima'] = r['delta'] > 0
        # 8% e o limiar de "vale comentar": abaixo disso a diferenca cabe no erro do modelo
        r['neutro'] = abs(r['delta']) < 8

    # o veredito sai das MEDIAS, nao de um dia solto: um unico dia oscila muito e diria
    # "fora do normal" com frequencia que o dado nao sustenta. O dia solto fica como
    # contexto na tela, sem voto.
    dentro = all(r['neutro'] for r in refs if r['media'])
    return {'pri': pri, 'previsto': prev, 'baixo': p['hoje'][f'baixo_{k}'],
            'alto': p['hoje'][f'alto_{k}'], 'refs': refs, 'dia_semana': rot_dia,
            'normal': dentro, 'estado': 'normal' if dentro else 'fora'}


def reguas():
    """As duas prioridades que entram no KPI. O P3 e cerca de cinco vezes o P2 em volume,
    entao a tela da mais peso a ele — mas nenhuma das duas aparece sem regua."""
    return [regua(p) for p in ORDEM_PRI]


def alertas():
    """So o que esta fora do esperado, com o caminho para o detalhe.

    Substituiu um indice de cinco linhas que listava todas as analises — uma por aba. Como
    a navegacao do topo ja leva a todas, aquilo era menu repetido, nao informacao. O que a
    navbar nao sabe dizer e QUAL delas precisa de atencao hoje.

    A projecao do ano saiu daqui: cada cartao de prioridade passou a mostrar o proprio
    fechamento contra a meta, com faixa e distancia. Repetir o mesmo numero em cartao e em
    alerta na mesma tela nao alerta ninguem — vira moldura.
    """
    p = painel()
    fora = []
    pior = sorted(p['saude'], key=lambda s: s['nota'])[0]
    if pior['nota'] < 40:
        fora.append({
            'aba': 'saude', 'ic': 'coracao', 'tom': 'no', 'rot': 'Saúde por produto',
            'valor': num(pior['nota'], 1),
            'texto': (f"é a nota de {pior['produto']}, o {int(pior['posicao'])}º de "
                      f"{len(p['saude'])} — classificado como {pior['quadrante']}"),
        })
    return fora


def pior_produto():
    """A menor nota de saude. Entra na tela de entrada como aviso estrutural: o dia pode
    estar calmo e um produto continuar apodrecendo devagar."""
    p = painel()
    x = dict(sorted(p['saude'], key=lambda s: s['nota'])[0])
    x['de'] = len(p['saude'])
    return x


def pior_causa():
    """A causa que concentra risco: a maior razao entre quota de quebras e quota de volume.
    Nao e a mais frequente — frequente e "Falha de Aplicacao", que responde por 59% da base
    e quebra menos que a media."""
    return max(painel()['causas'], key=lambda c: c['vezes a média'])


def indice():
    """Uma linha por analise do sistema. O Panorama resume sem detalhar: cada linha
    leva o numero que importa, a sua regua, e o estado. Quem quer profundidade, clica."""
    p = painel()
    d = dias()['resumo']
    pior = sorted(p['saude'], key=lambda x: x['nota'])[0]
    proj = {x['prioridade']: x for x in p['projecao']}['P3']
    causa = max(p['causas'], key=lambda c: c['vezes a média'])
    hoje_fila = fila_de_hoje(400)
    maior = max((f['risco'] for f in hoje_fila), default=0)

    # 'ic' e o glifo do sprite, que nem sempre tem o nome da aba: saude usa coracao e
    # causas usa lupa. Deixar o template adivinhar pelo nome da aba quebra em silencio.
    return [
        {'aba': 'previsao', 'ic': 'previsao', 'rot': 'Previsão',
         'valor': num(p['hoje']['previsto_p3'], 1), 'unid': 'no P3 hoje',
         'regua': f"erro médio de {num(d['mae'])} por dia · cobertura de {num(d['cobertura'])}%",
         'tom': ''},
        {'aba': 'fila', 'ic': 'fila', 'rot': 'Fila',
         'valor': mil(fila_total()), 'unid': 'casos pontuados por risco',
         'regua': f'maior risco aberto hoje: {num(maior)}%', 'tom': ''},
        {'aba': 'projecao', 'ic': 'alvo', 'rot': 'Projeção',
         'valor': num(proj['projecao'], 0), 'unid': 'quebras de P3 até dezembro',
         'regua': f"a meta do ano é {num(proj['meta'], 0)}",
         'tom': 'ok' if proj['dentro'] else 'wn'},
        {'aba': 'saude', 'ic': 'coracao', 'rot': 'Saúde',
         'valor': num(pior['nota'], 1), 'unid': f"é a pior nota · {pior['produto']}",
         'regua': f"{int(pior['posicao'])}º de {len(p['saude'])} produtos", 'tom': 'no'},
        {'aba': 'causas', 'ic': 'lupa', 'rot': 'Causas',
         'valor': num(causa['% das quebras'], 1) + '%', 'unid': 'das quebras vêm daqui',
         'regua': f"“{causa['Código de fechamento']}” é {num(causa['% da base'])}% da base",
         'tom': ''},
    ]


def fila_de_hoje(n=6, ate_hora=None):
    """Os casos abertos hoje, do mais arriscado para o menos.

    `ate_hora` corta no relogio do corte, e existe por um motivo concreto: sem ele a tela
    anuncia a hora corrente no cabecalho e lista, tres centimetros abaixo, caso aberto depois
    dela — hoje o relogio para as 15h, e a fila crua tem caso das 19h e das 23h. A fila
    do parquet traz o dia inteiro porque no historico o dia inteiro ja aconteceu — publicar
    isso e mostrar futuro. Quem opera conhece o proprio turno e percebe na hora.
    """
    f = fila()
    hoje = f[f['dia'] == pd.Timestamp(painel()['hoje']['dia'])]
    if ate_hora is not None:
        hoje = hoje[hoje['hora'] <= ate_hora]
    linhas = hoje.head(n).to_dict('records')
    media = painel()['base']['media_violacao']
    # a faixa e o sinal de maior peso viajam com a linha. Sem eles a fila e seis linhas com a
    # mesma forma, mudando so o numero — e o que diferencia um caso do outro nao e o risco, e o
    # motivo do risco, que e justamente o que o modelo tem de proprio para dizer.
    for r in linhas:
        _, _, rot, tom, glifo = faixa_de(r['risco'])
        r['faixa'], r['ftom'], r['fico'] = rot, tom, glifo
        r['top'] = r['sinais'][0] if r['sinais'] else None
        r['acao'] = ACOES[rot]
        # quantas vezes o caso e a taxa media da base. E o que transforma "8,1%" — um numero
        # que nao diz nada sozinho, porque parece pequeno — em "8x o normal".
        r['vezes'] = round(r['risco'] / media, 1) if media else 0
        # a regua do risco, em porcentagem do corte critico: 8,1% de risco preenche 81% da
        # barra. Sem ela a fila mostra quatro numeros parecidos e deixa a comparacao por conta
        # do leitor — que e justamente o trabalho que a lista existe para poupar.
        r['barra'] = _css(min(100.0, r['risco'] / CORTE_CRITICO * 100))
    return linhas


def fila_total():
    """Quantos incidentes o trimestre de teste pontuou. Denominador do ganho da fila."""
    return len(fila())


@lru_cache(maxsize=1)
def fila_ate_agora():
    """A fila cortada no relogio da tela: so o que ja aconteceu.

    O parquet cobre o trimestre de teste inteiro (01/10 a 31/12) porque e nele que o modelo foi
    medido. Publicar isso como fila operacional mostra futuro — o caso de maior risco do
    periodo, 63,0%, abriu em 08/11 as 19h, 38 dias depois do relogio da tela. Um plantao que ve
    aquilo como "o caso mais critico da fila" nao tem o que fazer com ele: ele nao existe ainda.

    O ganho do modelo continua sendo medido no trimestre inteiro, e a tela diz isso onde o
    numero aparece. Medir fora da amostra e evidencia; listar fora do relogio e erro.
    """
    p = painel()
    hoje = pd.Timestamp(p['hoje']['dia'])
    hora = p['acompanhamento']['hora_agora']
    f = fila()
    f = f[(f['dia'] < hoje) | ((f['dia'] == hoje) & (f['hora'] <= hora))]
    # a `posicao` gravada no parquet e o rank no trimestre inteiro: numa lista que agora so tem
    # o que ja aconteceu, ela apareceria como "46o de 5.183" numa fila de 49 linhas. O rank tem
    # de ser sobre a populacao que esta na tela.
    f = f.sort_values('risco', ascending=False).copy()
    f['posicao'] = range(1, len(f) + 1)
    # a mesma regua do bloco da fila no Panorama: escala ate o corte critico. Numa lista que vai
    # so ate 8,1%, barra de escala 0 a 100% vira fiapo igual em todas as linhas e nao compara
    # nada — e as duas telas passariam a desenhar o mesmo risco em tamanhos diferentes.
    f['barra'] = [_css(min(100.0, r / CORTE_CRITICO * 100)) for r in f['risco']]
    # o tom sai da MESMA tabela de faixas que pinta o bloco da fila no Panorama. A tabela usava
    # `tom_nota`, que e a regua da nota de saude — 0 a 100 onde menos e pior — e por isso
    # devolvia vermelho para qualquer risco abaixo de 40%, ou seja para a fila inteira.
    f['ftom'] = [faixa_de(r)[3] for r in f['risco']]
    # o NOME da faixa viaja com a linha, e nao só o tom.
    #
    # Com uma casa decimal, 1,04% e 0,98% imprimem o mesmo "1,0%", e o corte entre atenção e
    # rotina é exatamente 1%: a lista mostrava dois números idênticos, um laranja e outro verde,
    # sem nada que explicasse a diferença. Quem lê conclui que a tela errou. O nome escrito
    # resolve, e responde a pergunta que o turno faz de verdade — não é "1,04 ou 0,98", é "esse
    # aqui pede ação?".
    f['faixa'] = [faixa_de(r)[2] for r in f['risco']]
    return f


def fila_pagina(prioridade='', faixa='', busca='', pagina=1, por_pagina=40):
    """A fila com filtro e paginacao. Devolve tambem o que sobrou, para a tela poder
    dizer 'nenhum caso nesta faixa' em vez de mostrar tabela vazia.

    Le a fila cortada no relogio, e nao o trimestre inteiro: a tela e operacional."""
    f = fila_ate_agora()
    if prioridade:
        f = f[f['prioridade'] == prioridade]
    if faixa:
        lo, hi = next(x[:2] for x in FAIXAS if str(x[0]) == faixa)
        f = f[(f['risco'] >= lo) & (f['risco'] < hi)]
    if busca:
        b = busca.strip().lower()
        alvo = (f['incidente'].str.lower() + ' ' + f['produto'].str.lower() + ' '
                + f['equipe'].str.lower() + ' ' + f['ativo'].str.lower())
        f = f[alvo.str.contains(b, regex=False)]
    total = len(f)
    ini = (pagina - 1) * por_pagina
    return {'linhas': f.iloc[ini:ini + por_pagina].to_dict('records'), 'total': total,
            'pagina': pagina, 'paginas': max(1, -(-total // por_pagina)),
            'de': ini + 1 if total else 0, 'ate': min(ini + por_pagina, total)}


def contagem_por_faixa(prioridade=''):
    """As faixas da fila que esta na tela — a cortada no relogio, e no mesmo filtro da tabela.

    Duas correcoes em relacao a versao anterior:

    1. Recebe a prioridade. Sem ela, filtrar P2 dava uma tabela de 9 linhas com chips que
       continuavam somando 49 — o filtro contradizia o proprio resultado.

    2. Nao devolve mais `violou`. O desfecho do OLA so se conhece na resolucao: um caso aberto
       as 14h nao violou nem deixou de violar as 15h. Os quatro chips exibiam "0 violaram", que
       o leitor entende como "nenhuma violacao" quando a resposta correta e "ainda nao se sabe".

    O glifo viaja junto porque `alta` e `atencao` compartilham o tom ambar de proposito — e o
    que as separa e o glifo, que a versao anterior descartava.
    """
    f = fila_ate_agora()
    if prioridade:
        f = f[f['prioridade'] == prioridade]
    fora = []
    for lo, hi, rot, k, glifo in FAIXAS:
        s = f[(f['risco'] >= lo) & (f['risco'] < hi)]
        fora.append({'lo': lo, 'hi': None if hi > 100 else hi, 'rot': rot, 'k': k,
                     'ico': glifo, 'n': len(s)})
    return fora


def resumo_fila():
    """O maior risco aberto em CADA prioridade do KPI, com a regua contra a qual ele se le.

    As duas entram no KPI e as duas precisam aparecer. Na fila de hoje o topo e integralmente
    P3 — o maior P2 fica em decimo terceiro — entao quem le so a primeira tela nunca ve um P2 se
    a tabela for a unica fonte.
    """
    f = fila_ate_agora()
    media = painel()['base']['media_violacao']
    fora = []
    for pri in ORDEM_PRI:
        s = f[f['prioridade'] == pri]
        if s.empty:
            fora.append({'pri': pri, 'n': 0, 'maior': None})
            continue
        topo = s.iloc[0]                     # ja vem ordenada por risco
        _, _, rot, tom, glifo = faixa_de(topo['risco'])
        fora.append({
            'pri': pri, 'n': len(s), 'maior': round(float(topo['risco']), 1),
            'incidente': topo['incidente'], 'faixa': rot, 'ftom': tom, 'ico': glifo,
            'barra': topo['barra'], 'vezes': round(topo['risco'] / media, 1) if media else 0,
            'produto': topo['produto'], 'equipe': topo['equipe'], 'hora': int(topo['hora']),
        })
    return {'linhas': fora, 'media': media, 'corte': CORTE_CRITICO,
            'media_x': _css(media / CORTE_CRITICO * 100)}


def incidente(codigo):
    """O caso, com a posição que ele ocupa na fila QUE ESTÁ NA TELA.

    Lia a fila crua, cuja `posicao` é o rank no trimestre inteiro. O efeito era a lista dizer
    "1º de 49" e o modal aberto por aquela mesma linha dizer "46" — dois números certos em
    populações diferentes, que juntos leem como erro de contagem.
    """
    f = fila_ate_agora()
    linha = f[f['incidente'] == codigo]
    if linha.empty:                       # caso fora do relógio: cai para a fila do período
        f = fila()
        linha = f[f['incidente'] == codigo]
    if linha.empty:
        return None
    r = linha.iloc[0].to_dict()
    r['de'] = len(f)
    r['faixa'], r['ftom'] = faixa_de(r['risco'])[2], faixa_de(r['risco'])[3]
    r['em100'] = round(r['risco'])
    r['vezes'] = round(r['risco'] / painel()['base']['media_violacao'])
    r['hist_ativo'] = next((a['hist'] for a in painel()['ativos']
                            if a['ativo'] == r['ativo']), [])
    return r


def ativo(codigo):
    a = next((x for x in painel()['ativos'] if x['ativo'] == codigo), None)
    if a:
        a = dict(a)
        a['vezes'] = round(a['taxa'] / painel()['base']['media_violacao']) if a['taxa'] else 0
    return a


def produto(nome):
    p = next((x for x in painel()['saude'] if x['produto'] == nome), None)
    if not p:
        return None
    p = dict(p)
    p['componentes'] = [
        {'rot': 'taxa de violação', 'v': num(p['taxa_violacao'] * 100, 2), 'u': '%',
         'pos': round(p['pos_taxa_violacao'] * 100)},
        {'rot': 'problemas inéditos', 'v': num(p['prop_inedito'] * 100, 1), 'u': '%',
         'pos': round(p['pos_prop_inedito'] * 100)},
        {'rot': 'fechados sem causa', 'v': num(p['prop_sem_causa'] * 100, 1), 'u': '%',
         'pos': round(p['pos_prop_sem_causa'] * 100)},
        {'rot': 'duração mediana', 'v': num(p['duracao_mediana_h'], 1), 'u': 'h',
         'pos': round(p['pos_duracao_mediana_h'] * 100)},
        {'rot': 'tendência', 'v': num(p['tendencia'] * 100, 2), 'u': ' pontos',
         'pos': round(p['pos_tendencia'] * 100)},
    ]
    return p


def indice_busca():
    """O que a paleta de comando indexa."""
    p = painel()
    f = fila().head(150)
    itens = [{'t': 'aba', 'k': k, 'r': r, 's': 'ir para a aba'} for k, r in
             [('panorama', 'Panorama'), ('fila', 'Fila de risco'), ('saude', 'Saúde por produto'),
              ('causas', 'Causas e recorrentes'), ('previsao', 'Previsão de volume')]]
    itens += [{'t': 'inc', 'k': r['incidente'], 'r': r['incidente'],
               's': f"{r['produto']} · {r['equipe']} · risco {num(r['risco'])}%"}
              for _, r in f.iterrows()]
    itens += [{'t': 'ativo', 'k': a['ativo'], 'r': a['ativo'],
               's': f"{a['violacoes']} de {a['passagens']} passagens violaram"}
              for a in p['ativos'][:60]]
    itens += [{'t': 'prod', 'k': s['produto'], 'r': s['produto'],
               's': f"nota {num(s['nota'])} · posição {int(s['posicao'])} de 17"}
              for s in p['saude']]
    return itens
