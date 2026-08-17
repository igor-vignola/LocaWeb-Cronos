# -*- coding: utf-8 -*-
"""Gera data/app/ — o pacote que a aplicacao Django le em producao.

Tudo que a tela precisa ja vem agregado aqui. O conteiner nao carrega a base bruta de
1,5 MB nem executa pandas pesado a cada requisicao: ele abre um JSON de poucos kB e um
parquet com a fila. Essa separacao e o que permite a imagem rodar em plano gratuito sem
Prophet nem scikit-learn dentro.

Entradas: os parquets de data/interim gerados pelos notebooks 02 a 07 e pelos scripts
gera_previsao_diaria.py e gera_fila_pontuada.py.
"""
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent / 'direcoes'))
from dados import (ATIVOS, BASE_20, CORTE, DELTA_TAXA, DIA_HOJE, ELEG_30, ELEGIVEIS, EM_ABERTO,
                   FILA_TODA, FUT2, FUT3, HIST_ATIVO, HORAS, HORA_PICO, HORA_RISCO, HOJE2, HOJE3,
                   LBL_DIA, MEDIA_BASE, MES_LBL, ONTEM, ONTEM_TOTAL, ONTEM_VIOL, REAL2, REAL3,
                   SEMANA, SEMANA2,
                   SEM_VIOL, TAXA_30, TOP50_PEGA, TOTAL_VIOL, ULTIMOS_DIAS, VIOL_30,
                   VIOL_PERIODO, ATE_CORTE, COL_ATIVO, causas, grupos, kpi, recor, saude)

RAIZ = Path.cwd()
DESTINO = RAIZ / 'data' / 'app'
DESTINO.mkdir(parents=True, exist_ok=True)
# A aplicacao simula um relogio parado nesta hora do dia do corte, e a escolha muda o que a tela
# consegue dizer. As 7 o dia nao comecou: 5 entrados, 14% do volume, e a curva inteira ainda por
# vir — so ha projecao, nada para comparar. As 15 o dia esta na metade: existe realizado suficiente
# para colocar do lado do previsto, o acompanhamento passa dos 35% que liberam extrapolar o
# fechamento, e a fila tem caso com risco de verdade em vez de uma lista de 0,1%.
HORA_AGORA = 15


def _perfil_hora(pri):
    """A curva de chegada acumulada daquela prioridade, medida na base ate o corte.

    Era uma curva so, calculada em TODAS as prioridades (`HORAS` sai de `ATE_CORTE` inteiro), e
    a tela afirmava que ela tinha sido medida no P3. Nao tinha. O P2 e o P3 chegam em ritmos
    diferentes ao longo do dia, e aplicar a curva do agregado a um deles distribui o volume
    previsto na hora errada — o que estraga justamente a comparacao do meio do turno.
    """
    s = ATE_CORTE[ATE_CORTE['Prioridade'].astype(str).str.startswith(pri)]
    por_hora = s.groupby('hora').size().reindex(range(24), fill_value=0)
    total = int(por_hora.sum()) or 1
    acumulado, a = [], 0.0
    for v in por_hora:
        a += int(v) / total
        acumulado.append(a)
    return acumulado


def acompanhamento_do_dia(pri, hoje):
    """Previsto contra realizado ao longo do dia, para uma prioridade.

    A curva esperada e a distribuicao historica por hora daquela prioridade aplicada ao total
    previsto para hoje. A realizada e o que ja entrou. Assim o turno ve, no meio do dia, se
    esta no ritmo previsto — que e o que torna a previsao util depois do cafe.

    Recebe a prioridade porque as DUAS entram no KPI e as duas precisam aparecer na tela. A
    versao anterior era fixa em P3 e o P2 nao tinha acompanhamento nenhum.
    """
    acumulado = _perfil_hora(pri)

    do_dia = kpi[(kpi['dia'] == CORTE) & kpi['Prioridade'].astype(str).str.startswith(pri)]
    por_hora = do_dia.groupby('hora').size().reindex(range(24), fill_value=0)
    real_acum, t = [], 0
    for h in range(24):
        t += int(por_hora[h])
        real_acum.append(t)

    prev = float(hoje['valor'])
    esperado = [round(prev * a, 1) for a in acumulado]
    # projecao do fechamento pelo ritmo observado ate agora
    ate_agora = real_acum[HORA_AGORA]
    frac = acumulado[HORA_AGORA]
    ritmo = round(ate_agora / frac, 1) if frac > 0 else prev
    return {
        'prioridade': f'P{pri}',
        'hora_agora': HORA_AGORA,
        'esperado': esperado,
        'realizado': real_acum[:HORA_AGORA + 1],
        'por_hora_real': [int(v) for v in por_hora],
        'previsto': round(prev, 1),
        'baixo': round(float(hoje['baixo']), 1),
        'alto': round(float(hoje['alto']), 1),
        'ate_agora': ate_agora,
        'esperado_agora': esperado[HORA_AGORA],
        'ritmo_fecha': ritmo,
        'no_ritmo': bool(float(hoje['baixo']) <= ritmo <= float(hoje['alto'])),
        # quanto do dia ja passou, em volume esperado. Extrapolar com 14% do dia e
        # instavel e a tela precisa dizer isso em vez de fingir precisao.
        'dia_decorrido': round(frac * 100, 1),
        'confiavel': bool(frac >= .35),
    }


def serie(df, campos):
    return [{k: (v.strftime('%Y-%m-%d') if isinstance(v, pd.Timestamp) else
                 (round(float(v), 4) if isinstance(v, float) else
                  (int(v) if isinstance(v, (int, bool)) else str(v))))
             for k, v in r.items() if k in campos} for _, r in df.iterrows()]


# ── quem atende cada produto ───────────────────────────────────────────────────
# A tela de Saude lista quinze codigos de quatro letras, todos comecando com `l`, e nada os
# separa: em tipografia de tela o `l` minusculo e o `I` maiusculo sao o mesmo traco.
#
# A ideia original era agrupar por FAMILIA de produto (hospedagem, storage, rede). Nao da: os
# 51 codigos do dataset sao opacos e nao ha dicionario. Fui atras da coluna `Categoria` achando
# que ela salvaria e ela tambem e anonimizada (`cat71`, `cat103`); alem disso o agrupamento por
# categoria dominante devolve 13 grupos para 15 produtos, com dois pares apenas. Nao e familia,
# e ruido.
#
# O que E derivavel, legivel e util no turno: QUEM ATENDE. `Grupo designado` traz nome de
# equipe de verdade, e a dominancia e alta — de 42% (lsin) a 100% (lgoa). Dois produtos do
# mesmo time ficam visivelmente parentes, que era o ganho pedido, e nada e inventado.
#
# Medido na mesma janela da nota: ATE_CORTE, ou seja, so o que existia em 30/09.
def _dono(df):
    fora = {}
    for prod, g in df[df['Produto'].notna()].groupby('Produto'):
        c = g['Grupo designado'].value_counts()
        if c.empty:
            continue
        fora[prod] = {'equipe': str(c.index[0]),
                      'equipe_pc': round(float(c.iloc[0] / c.sum() * 100)),
                      'equipes': int(len(c))}
    return fora


DONO = _dono(ATE_CORTE)

pacote = {
    'corte': CORTE.strftime('%Y-%m-%d'),
    'gerado_de': 'data/interim (notebooks 02 a 07)',
    'hoje': {
        'dia': DIA_HOJE.strftime('%Y-%m-%d'),
        'previsto_p3': round(float(HOJE3['valor']), 1),
        'baixo_p3': round(float(HOJE3['baixo']), 1),
        'alto_p3': round(float(HOJE3['alto']), 1),
        'previsto_p2': round(float(HOJE2['valor']), 1),
        'baixo_p2': round(float(HOJE2['baixo']), 1),
        'alto_p2': round(float(HOJE2['alto']), 1),
    },
    'ontem': {'dia': ONTEM['dia'].strftime('%Y-%m-%d'), 'total': ONTEM_TOTAL,
              'violou': ONTEM_VIOL, 'p3': int(ONTEM['valor'])},
    'base': {'media_violacao': MEDIA_BASE, 'elegiveis': ELEGIVEIS, 'violacoes': TOTAL_VIOL,
             'em_atendimento': EM_ABERTO, 'base_20_dias': round(BASE_20, 1),
             'sem_violacao_dias': SEM_VIOL, 'taxa_30': round(TAXA_30, 2),
             'viol_30': VIOL_30, 'eleg_30': ELEG_30, 'delta_taxa': round(DELTA_TAXA, 1),
             'top50_pega': TOP50_PEGA, 'viol_periodo': VIOL_PERIODO},
    # as DUAS prioridades do KPI acompanhadas hora a hora. Antes existia so a do P3, e o P2
    # aparecia na tela apenas como um numero previsto, sem nada para comparar contra ele.
    'acompanhamento': acompanhamento_do_dia('3', HOJE3),
    'acompanhamento_p2': acompanhamento_do_dia('2', HOJE2),
    'horas': HORAS,
    'hora_pico': HORA_PICO,
    'hora_risco': HORA_RISCO,
    'semana': [{'dia': LBL_DIA[i], 'media': float(SEMANA[i])} for i in range(7)],
    'semana_p2': [{'dia': LBL_DIA[i], 'media': float(SEMANA2[i])} for i in range(7)],
    'ultimos_dias': [{'dia': d.strftime('%Y-%m-%d'), 'rot': LBL_DIA[d.dayofweek],
                      'dm': f'{d.day:02d}/{d.month:02d}', 'violacoes': v}
                     for d, v in ULTIMOS_DIAS],
    'trilho': {
        'realizado': [{'dia': r['dia'].strftime('%Y-%m-%d'), 'valor': float(r['valor'])}
                      for _, r in REAL3.tail(30).iterrows()],
        'realizado_p2': [{'dia': r['dia'].strftime('%Y-%m-%d'), 'valor': float(r['valor'])}
                         for _, r in REAL2.tail(30).iterrows()],
        'previsto': [{'dia': r['dia'].strftime('%Y-%m-%d'), 'valor': float(r['valor']),
                      'baixo': float(r['baixo']), 'alto': float(r['alto'])}
                     for _, r in FUT3.iterrows()],
        # a serie prevista do P2 estava no parquet desde sempre e nunca foi publicada — e por
        # isso as telas de previsao nasceram so com P3
        'previsto_p2': [{'dia': r['dia'].strftime('%Y-%m-%d'), 'valor': float(r['valor']),
                         'baixo': float(r['baixo']), 'alto': float(r['alto'])}
                        for _, r in FUT2.iterrows()],
    },
    # As tres parcelas do notebook 06 sao a resposta para a pergunta que a tela nao conseguia
    # responder: "o OLA ja estourou?". A projecao de 208 no P3 e a soma de 145 quebras que JA
    # aconteceram, 5 do risco da fila aberta no corte e 58 do volume que ainda entra. Sem o 145
    # separado, um numero acima do teto le como teto ja rompido — e no corte de 01/10 faltavam
    # 55 do teto, nao sobravam.
    'projecao': [{'prioridade': p, 'projecao': float(r['projeção']),
                  'meta': float(r['meta máxima']), 'baixo': float(r['faixa baixa']),
                  'alto': float(r['faixa alta']),
                  'dentro': r['situação projetada'] == 'dentro da meta',
                  'ja': float(r['parcela 1']),        # quebras conhecidas no corte
                  'fila': float(r['parcela 2']),      # risco da fila aberta
                  'entra': float(r['parcela 3'])}     # volume que ainda entra
                 for p, r in __import__('dados').proj.iterrows()],
    'saude': [{'produto': p, **DONO.get(p, {}),
               **{k: (float(v) if isinstance(v, float) else
                      (int(v) if not isinstance(v, str) else v))
                  for k, v in r.items()}} for p, r in saude.iterrows()],
    'ativos': [{'ativo': a, 'passagens': int(r['passagens']), 'violacoes': int(r['violacoes']),
                'taxa': round(float(r['taxa']), 2), 'hist': HIST_ATIVO.get(a, [])}
               for a, r in ATIVOS.iterrows()],
    # as 16 causas, e nao as 8 de maior volume. O corte por volume eliminava justamente as de
    # maior taxa — Falha de Hardware viola 8,24%, 8,75 vezes a media da base, e nunca aparecia
    # na tela porque e 0,4% do volume. O bloco existe para mostrar onde volume e risco NAO
    # coincidem, e o corte removia os casos em que eles nao coincidem.
    'causas': serie(causas, ['Código de fechamento', 'incidentes', 'quebras', '% da base',
                             '% das quebras', 'taxa de quebra %', 'vezes a média',
                             'incidentes P2', 'quebras P2', 'taxa P2 %',
                             'incidentes P3', 'quebras P3', 'taxa P3 %']),
    'recorrentes': serie(recor.head(8), ['problema', 'incidentes', 'ativos', 'quebras']),
    'grupos': serie(grupos.head(8), ['grupo', 'taxa %', 'vezes a média']),
    'meses': MES_LBL,
    'dias_semana': LBL_DIA,
}

alvo = DESTINO / 'painel.json'
alvo.write_text(json.dumps(pacote, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

# a fila fica em parquet: sao 5.183 linhas e o Django pagina em cima dela
shutil.copy(RAIZ / 'data' / 'interim' / '04_fila_pontuada.parquet', DESTINO / 'fila.parquet')

kb_json = alvo.stat().st_size / 1024
kb_fila = (DESTINO / 'fila.parquet').stat().st_size / 1024
print(f'painel.json  {kb_json:7.1f} kB')
print(f'fila.parquet {kb_fila:7.1f} kB')
print(f'total        {kb_json + kb_fila:7.1f} kB  (contra 1.802 kB da base bruta)')
ac = pacote['acompanhamento']
print(f"\nacompanhamento às {ac['hora_agora']:02d}h: {ac['ate_agora']} entraram, "
      f"{ac['esperado_agora']} esperados")
print(f"ritmo projeta fechar em {ac['ritmo_fecha']} · previsto {ac['previsto']} "
      f"(faixa {ac['baixo']} a {ac['alto']}) · "
      f"{'dentro da faixa' if ac['no_ritmo'] else 'FORA da faixa'}")
