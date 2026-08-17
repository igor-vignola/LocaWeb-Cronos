# -*- coding: utf-8 -*-
"""Monta o deck da Sprint 3: HTML de cada slide, PNG de cada HTML e o .pptx final.

A ordem dos slides segue o template oficial da FIAP
(`assets/Templates/03Template_MVP_Preliminar_Challenge_2026_01_locaweb.pptx`), com os
mesmos títulos. Onde o conteúdo pede mais espaço, um item do template vira dois slides.
Foi o que a Sprint 2 fez, e tirou 5,00.

Uso, com o servidor da aplicação já capturado por `captura_telas.py`:

    .venv/Scripts/python scripts/monta_deck_sprint3.py

Saída:
    sprints/sprint-3/slides/*.html   fonte editável de cada slide
    sprints/sprint-3/slides/png/*.png
    sprints/EC_Sprint_3_2TSCOA_Evidencias_Construcao_Cronos_SuperDataBros.pptx

Regra que atravessa o arquivo inteiro: **todo número aqui saiu de célula executada**, e a
origem está anotada no comentário do slide. Métrica de avaliação de modelo (MAE, cobertura,
ROC AUC, PR-AUC, backtest) é assunto de slide, nunca de tela — o sistema simula um relógio
parado em 01/10/2025 15h e não pode exibir realizado posterior ao corte.
"""
from pathlib import Path

from deck_estilo import (
    ALTURA,
    LARGURA,
    URL_APP,
    cabecalho,
    cartao_num,
    cartao_texto,
    pagina,
    slide,
)

RAIZ = Path(__file__).resolve().parents[1]
PRINTS = RAIZ / "sprints" / "sprint-3" / "prints"
SAIDA = RAIZ / "sprints" / "sprint-3" / "slides"
SAIDA_PNG = SAIDA / "png"
PPTX = RAIZ / "sprints" / "EC_Sprint_3_2TSCOA_mvp_preliminar_Cronos_SuperDataBros.pptx"

# O bloco de análise e modelagem não é escrito aqui: ele já existia, construído em julho, e
# mora em `prototipos/slides/mvp/deck/`. São os slides que carregam os gráficos de verdade,
# exportados do matplotlib dos notebooks, e é o que a dica do slide 13 do template pede ao
# listar "algoritmos utilizando modelos matemáticos e estatísticos" e "imagens das
# visualizações obtidas". Aqui entram apenas os identificadores, na ordem do `viewer.html`,
# escolhendo a primeira variação de cada slide, que é a que o viewer abre.
DECK_ANALISE = RAIZ / "prototipos" / "slides" / "mvp" / "deck"
ANALISE = [
    # Análise exploratória
    "d01a", "d02a", "d03m", "d04r", "d04m", "d05m", "d06m", "d07m", "d08m", "d09a",
    "d10a", "d11a",
    # Previsão de volume
    "d12a", "d13a", "d14m", "d15m", "d15n", "d17a",
    # Risco de estouro de OLA
    "d20a", "d21a", "d22a", "d23a", "d24a", "d25a", "d26a", "d27a", "d28a",
    # Causas e recorrência
    "d29a", "d30a", "d31a", "d32a", "d33a",
    # Projeção do KPI e saúde por produto
    "d34a", "d35a", "d36a", "d37a", "d38a",
    # Fechamento do bloco analítico
    "d39a",
]

RODAPE_ESQ = "Cronos · Super Data Bros · 2TSCOA"
RODAPE_DIR = "Challenge FIAP 2026 com Locaweb"

# Cada print vira um slide. A ordem é a da navegação da aplicação: as seis abas na sequência
# em que a decisão acontece no turno, depois os quatro aprofundamentos que abrem por cima.
TELAS = [
    (
        "01-panorama",
        "Panorama",
        "O turno em uma tela",
        "Abre o dia com o que já entrou contra o que o modelo esperava a esta hora, "
        "em <b>P3 e P2</b>. Abaixo, os casos de maior risco agora e as duas metas do ano.",
        "Aba 1 de 6",
    ),
    (
        "02-previsao",
        "Previsão de volume",
        "Quanto entra nos próximos dias",
        "Saída do Prophet. Trinta dias medidos emendados em duas semanas previstas, "
        "cada dia como <b>intervalo</b> e não como número único: é a largura dele que "
        "dimensiona a escala da equipe.",
        "Aba 2 de 6",
    ),
    (
        "03-projecao",
        "Projeção do KPI",
        "Onde o ano fecha",
        "As violações já acumuladas somadas ao risco da fila aberta e ao volume que ainda "
        "entra. <b>P3 projeta 208 e fica dentro dos 100%; P2 projeta 43 e passa do limite "
        "de 39.</b>",
        "Aba 3 de 6",
    ),
    (
        "04-fila",
        "Fila de risco",
        "Em qual caso olhar primeiro",
        "Os 49 casos abertos às 15h, ordenados do maior risco para o menor pela regressão "
        "logística, cada um com o <b>fator que mais pesa</b> e o ativo envolvido.",
        "Aba 4 de 6",
    ),
    (
        "05-saude",
        "Saúde por produto",
        "Que produto está pior",
        "Nota de 0 a 100 nos 15 produtos, com a situação de cada um, o componente que mais "
        "penaliza e as colunas de <b>P3 e P2 separadas</b>. A explicabilidade está na "
        "própria linha.",
        "Aba 5 de 6",
    ),
    (
        "06-causas",
        "Causas e recorrência",
        "O que compensa prevenir",
        "Códigos de fechamento ordenados por <b>taxa de violação, não por volume</b>: é "
        "assim que aparece a causa pequena que viola muito. Falha de Hardware é 0,4% do "
        "volume e viola 8,8 vezes a média.",
        "Aba 6 de 6",
    ),
]

MODAIS = [
    (
        "07-modal-briefing",
        "Diferencial 1 · Morning briefing",
        "O resumo que chega sem ser pedido",
        "Abre sozinho na entrada, com ontem, hoje e para onde ir. É gerado da saída dos "
        "modelos: <b>o Cronos empurra o insight, não espera pergunta.</b>",
        "Modal 1 de 4",
    ),
    (
        "08-modal-escore",
        "Explicabilidade",
        "Por que este caso e não outro",
        "A decomposição do escore: cada sinal entra como <b>peso × desvio da média</b>, e a "
        "soma reconstrói a pontuação exata. Modelo linear é explicável por construção, sem "
        "ferramenta externa.",
        "Modal 2 de 4",
    ),
    (
        "09-modal-produto",
        "Diferencial 2 · Score de saúde",
        "O que forma a nota do produto",
        "Os cinco componentes da nota e quanto cada um pesa, com o histórico do produto. "
        "É o que separa <b>viola muito</b> de <b>vai começar a violar</b>.",
        "Modal 3 de 4",
    ),
    (
        "10-modal-meta",
        "Régua oficial da Locaweb",
        "Como a meta é medida",
        "Os seis degraus da meta anual, direto do dicionário de dados. <b>O Cronos não "
        "define a régua</b>: ele diz em que degrau o ano está e em qual deve terminar.",
        "Modal 4 de 4",
    ),
]


def _img(nome: str) -> str:
    """URI de arquivo do print, para o navegador conseguir carregar na renderização."""
    return (PRINTS / f"{nome}.png").resolve().as_uri()


def _sl(conteudo: str, *, tag: str, escuro: bool = False, classe: str = "") -> str:
    return slide(
        conteudo,
        tag=tag,
        rodape_esq=RODAPE_ESQ,
        rodape_dir=RODAPE_DIR,
        escuro=escuro,
        classe=classe,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Bloco 1 · identificação (template, slides 1 e 2)
# ─────────────────────────────────────────────────────────────────────────────
def s01_capa() -> str:
    corpo = (
        '<section class="slide light cp">'
        '<div class="mesh"></div><div class="grid-bg"></div>'
        '<div class="hd"><span class="bi">'
        '<svg viewBox="0 0 28 28" fill="none">'
        '<path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="22" cy="8" r="3" fill="none" stroke="#3B82F6" stroke-width="1.5"/>'
        '<circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg></span>'
        '<span class="bn">Cronos</span>'
        '<span class="bt">SPRINT 03 · MVP PRELIMINAR</span>'
        '<span class="tag">Challenge FIAP 2026 com Locaweb</span></div>'
        '<div class="body">'
        '<span class="pill">Inteligência preditiva para incidentes</span>'
        '<div class="word">Cronos</div>'
        '<div class="tag2"><b>Veja antes.</b> Aja antes.</div>'
        '<p class="sub2">Lê o histórico de incidentes da Locaweb, prevê o volume dos '
        "próximos dias, aponta qual caso vai estourar o OLA e projeta onde a meta do ano "
        "fecha.</p>"
        '<div class="glass">'
        '<div class="gc"><div class="gk">Equipe · Super Data Bros · 2TSCOA</div>'
        '<div class="gv">Ana Beatriz Costa de Oliveira · Hygor Abrantes · Igor Vignola</div>'
        '<div class="gs">FIAP · Tecnólogo em Data Science</div></div>'
        '<div class="gc"><div class="gk">Mentor Locaweb</div>'
        '<div class="gv">Douglas Gouveia</div>'
        '<div class="gs">Gerente Executivo de Operações</div></div>'
        "</div></div>"
        f'<div class="ft"><span>{RODAPE_ESQ}</span>'
        "<span>Entrega 23/08/2026</span></div>"
        "</section>"
    )
    return corpo


def s02_equipe() -> str:
    linhas = [
        ("Ana Beatriz Costa de Oliveira", "RM561310"),
        ("Hygor Abrantes", "RM565063"),
        ("Igor Vignola", "RM561428"),
    ]
    tabela = "".join(
        f'<tr><td><b>{n}</b></td><td class="n"><b>{rm}</b></td>'
        f"<td>2TSCOA · Tecnólogo em Data Science</td></tr>"
        for n, rm in linhas
    )
    conteudo = (
        cabecalho(
            "Identificação",
            "Equipe Super Data Bros",
            "Nomes em ordem alfabética, como pede a norma de entrega.",
        )
        + '<div class="tw" style="margin-top:26px"><table><thead><tr>'
        '<th>Integrante</th><th style="text-align:right">RM</th><th>Turma</th>'
        f"</tr></thead><tbody>{tabela}</tbody></table></div>"
        + '<div class="stats" style="margin-top:auto">'
        + cartao_num(
            "Solução", "Cronos", "Veja antes. Aja antes.", "focus"
        )
        + cartao_num(
            "Mentor Locaweb",
            "D. Gouveia",
            "Gerente Executivo de Operações",
        )
        + cartao_num("Sprints entregues", "2 de 4", "Ideação e Arquitetura, ambas 5,00", "good")
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 2")


# ─────────────────────────────────────────────────────────────────────────────
# Bloco 2 · contexto (template, slides 3, 4 e 5)
# ─────────────────────────────────────────────────────────────────────────────
def s03_contexto() -> str:
    """Números: notebooks/01_eda.ipynb e 02_base_kpi.ipynb (asserts de invariante)."""
    conteudo = (
        cabecalho(
            "Contextualização do problema",
            "Uma operação 24×7 medida por uma régua anual",
            "A Locaweb responde a incidente o ano inteiro e é cobrada por um KPI de OLA que "
            "conta violações acumuladas no ano, faixa por faixa, em cada prioridade. "
            "Quando a faixa vira, o ano inteiro já passou.",
        )
        + '<div class="stats" style="margin-top:26px">'
        + cartao_num("Base entregue", "122.543", "incidentes registrados entre jan/2023 e dez/2025")
        + cartao_num(
            "Valem para o KPI", "25.600", "21% da base. O resto não conta para a meta", "focus"
        )
        + cartao_num("Violações de OLA", "248", "no período inteiro, ou 0,97% dos elegíveis", "bad")
        + "</div>"
        + '<div class="pts" style="margin-top:16px">'
        + cartao_texto(
            "1",
            "O prazo muda com a prioridade",
            "P2 tem 4 horas para resolver, P3 tem 12. São as duas prioridades que entram no "
            "KPI e cada uma tem meta própria, então toda leitura precisa das duas lado a lado.",
        )
        + cartao_texto(
            "2",
            "A meta é uma escada, não um teto",
            "Passar de uma faixa não zera o indicador: derruba um degrau. No P2 a diferença "
            "entre 39 e 40 violações no ano custa 25 pontos de atingimento.",
        )
        + cartao_texto(
            "3",
            "Setembro de 2025 multiplicou o volume por cinco",
            "De 4 mil para 21,6 mil incidentes no mês. A abertura por monitoramento saltou de "
            "2.404 para 20.008 e o status Sem Intervenção de 47 para 17.838: foi expansão do "
            "monitoramento sobre ativos novos, não piora da operação. "
            "<b>A série que vale para o KPI atravessou intacta, de 2.330 para 2.324.</b>",
            "good",
        )
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 3")


def s04_problema() -> str:
    """Números: 04_risco_ola.ipynb §4.6.3 (AUC das filas) e sprint-3-mvp.md (régua 2025)."""
    linhas = [
        ("Ordenação por prioridade, o padrão de qualquer ITSM", "0,4693", "1", "bad"),
        ("Fila sorteada, sem critério nenhum", "0,5063", "0,5", ""),
        ("Melhor regra simples: ativo crônico e time", "0,7945", "6", ""),
        ("Regressão logística do Cronos", "0,8693", "15", "good"),
    ]
    corpo_tab = "".join(
        f'<tr class="hot"><td><b>{n}</b></td><td class="n">{auc}</td>'
        f'<td class="n"><b style="color:var(--{ "good" if t=="good" else "bad" if t=="bad" else "head"})">{q}</b></td></tr>'
        if t
        else f'<tr><td>{n}</td><td class="n">{auc}</td><td class="n">{q}</td></tr>'
        for n, auc, q, t in linhas
    )
    conteudo = (
        cabecalho(
            "Problema a ser resolvido",
            "A operação descobre o estouro depois que ele acontece",
            "Em 2025 o P2 fechou com <b>42 violações</b> e caiu para a faixa de 75% de "
            "atingimento. O P3 fechou com <b>196</b> e ficou em 150%. A pressão está no P2, "
            "e nada na ferramenta atual avisa isso antes de dezembro.",
        )
        + '<div style="display:flex;gap:22px;margin-top:22px;align-items:flex-start">'
        + '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:13px">'
        + cartao_texto(
            "1",
            "Priorizar não é o mesmo que antecipar",
            "A prioridade é atribuída na abertura e diz a urgência declarada, não a chance de "
            "estourar. Ordenar a fila por ela é o comportamento padrão do ITSM.",
            "bad",
        )
        + cartao_texto(
            "2",
            "E ordenar por prioridade é pior que sortear",
            "Medido no trimestre de teste: a fila por prioridade tem ROC AUC de <b>0,4693</b>, "
            "abaixo dos 0,5063 de uma fila aleatória. Nas 50 primeiras posições dela há "
            "<b>1 violação</b>. Na fila do modelo, 15.",
            "bad",
        )
        + cartao_texto(
            "3",
            "A explicação não é a priorização, é a familiaridade",
            "Controlando pela quantidade de vezes que o problema já apareceu, a vantagem "
            "aparente do P2 desaparece. Apenas <b>7,5% dos casos inéditos são P2</b>, contra "
            "29,9% dos problemas que já repetiram vinte vezes ou mais.",
        )
        + "</div>"
        + '<div class="tw" style="flex:1;min-width:0">'
        '<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;'
        'color:var(--tx2);padding:0 16px 12px">Onde olhar primeiro, entre 5.183 casos de teste'
        "</div><table><thead><tr><th>Critério de ordenação</th>"
        '<th style="text-align:right">ROC AUC</th>'
        '<th style="text-align:right">Violações no top 50</th></tr></thead>'
        f"<tbody>{corpo_tab}</tbody></table>"
        '<p style="font-size:13px;color:var(--tx2);padding:12px 16px 0;line-height:1.45">'
        "Trimestre de out a dez de 2025, com 50 violações em 5.183 incidentes.</p></div>"
        "</div>"
    )
    return _sl(conteudo, tag="Template · slide 4")


def s05_escopo() -> str:
    """Números: sprint-3-mvp.md §Verificações de robustez, medido em 29/07/2026."""
    quartis = [
        ("Q1, volume mais baixo", "64", "58,0", "0,5", "0,8%"),
        ("Q2", "69", "79,6", "0,7", "0,9%"),
        ("Q3", "61", "90,2", "0,9", "1,0%"),
        ("Q4, volume mais alto", "61", "110,0", "0,8", "0,7%"),
    ]
    corpo_tab = "".join(
        f"<tr><td><b>{q}</b></td><td class=\"n\">{d}</td><td class=\"n\">{v}</td>"
        f'<td class="n">{qb}</td><td class="n"><b>{t}</b></td></tr>'
        for q, d, v, qb, t in quartis
    )
    conteudo = (
        cabecalho(
            "Problema a ser resolvido · o achado que define o escopo",
            "Dia cheio não é dia de violação",
            "Antes de construir, testamos a hipótese que parecia óbvia: se o volume sobe, a "
            "violação sobe junto. Em 2025, só em dias úteis, a correlação é <b>r = 0,159</b> "
            "e o volume explica <b>2,5%</b> da variação de violações por dia.",
        )
        + '<div style="display:flex;gap:22px;margin-top:22px;align-items:flex-start">'
        + '<div class="tw" style="flex:1.15;min-width:0">'
        '<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;'
        'color:var(--tx2);padding:0 16px 12px">Dias úteis de 2025, agrupados por volume</div>'
        "<table><thead><tr><th>Quartil</th>"
        '<th style="text-align:right">Dias</th><th style="text-align:right">Volume/dia</th>'
        '<th style="text-align:right">Violações/dia</th>'
        '<th style="text-align:right">Taxa</th></tr></thead>'
        f"<tbody>{corpo_tab}</tbody></table>"
        '<p style="font-size:13px;color:var(--tx2);padding:12px 16px 0;line-height:1.45">'
        "Dias de volume alto concentram cerca de 60% mais violações em absoluto, mas "
        "<b>a taxa fica plana</b>. Mais casos, mesma chance por caso.</p></div>"
        + '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:13px">'
        + cartao_texto(
            "→",
            "A previsão de volume dimensiona a carga",
            "Diz quanta gente o turno precisa e quanto o ano tende a acumular. É o que sustenta "
            "escala de plantão e projeção de meta.",
        )
        + cartao_texto(
            "→",
            "O modelo de risco aponta o caso",
            "Diz qual incidente vai estourar. Não é complemento do primeiro: é a metade que "
            "fecha a proposta.",
            "good",
        )
        + cartao_texto(
            "!",
            "Publicamos o resultado que enfraquece o discurso",
            "Seria mais confortável vender um modelo só. O dado não permite, e a decisão de "
            "escopo saiu do dado.",
            "warn",
        )
        + "</div></div>"
    )
    return _sl(conteudo, tag="Template · slide 4")


def s06_solucao() -> str:
    conteudo = (
        cabecalho(
            "Proposta de solução",
            "Dois modelos, duas entregas proativas, seis telas",
            "O Cronos lê o histórico, publica o que vem pela frente e diz onde agir. "
            "Não tem caixa de perguntas: ele empurra o insight.",
        )
        + '<div style="display:flex;gap:16px;margin-top:24px;flex:1;min-height:0">'
        + '<div style="flex:1;display:flex;flex-direction:column;gap:13px">'
        '<div style="font-size:12px;font-weight:700;letter-spacing:1.6px;'
        'text-transform:uppercase;color:var(--accent)">Os modelos</div>'
        + cartao_texto(
            "1",
            "Prophet · volume diário D+1 a D+7",
            "Uma série para P3 e outra para P2, com sazonalidade semanal, feriados nacionais e "
            "intervalo de 80%. Erro médio de <b>11,8/dia no P3 e 4,2/dia no P2</b>.",
        )
        + cartao_texto(
            "2",
            "Regressão logística · risco por incidente",
            "Probabilidade de violar o OLA calculada na abertura, com 10 características e "
            "nenhuma que vaze desfecho. <b>Os 20% de maior risco concentram 72% das violações.</b>",
        )
        + cartao_texto(
            "3",
            "Projeção do KPI · onde o ano fecha",
            "Soma o que já aconteceu, o risco da fila aberta e o volume que ainda entra. "
            "Devolve faixa, não número único.",
        )
        + "</div>"
        + '<div style="flex:1;display:flex;flex-direction:column;gap:13px">'
        '<div style="font-size:12px;font-weight:700;letter-spacing:1.6px;'
        'text-transform:uppercase;color:var(--accent)">O que o usuário recebe</div>'
        + cartao_texto(
            "★",
            "Morning briefing",
            "Resumo automático de ontem, hoje e para onde ir, na entrada da ferramenta. "
            "Chega sem ninguém perguntar nada.",
            "good",
        )
        + cartao_texto(
            "★",
            "Score de saúde por produto",
            "Nota de 0 a 100 nos 15 produtos com mais de 200 incidentes, com o componente que "
            "puxa a nota para baixo escrito na própria linha.",
            "good",
        )
        + cartao_texto(
            "✓",
            "Explicabilidade em todo lugar",
            "Cada caso da fila abre a decomposição do próprio escore. O desafio pede explicar, "
            "não só prever.",
        )
        + "</div></div>"
    )
    return _sl(conteudo, tag="Template · slide 5")


def s07_mudou() -> str:
    """Justificativas: sprint-3-mvp.md §Testado e descartado; CLAUDE.md regras 1 e 2."""
    conteudo = (
        cabecalho(
            "Proposta de solução · o que mudou desde a Sprint 2",
            "Quatro ideias foram ao dado e três não voltaram",
            "A arquitetura da Sprint 2 declarava detector de cascata, XGBoost para risco, "
            "clusterização por DTW e SHAP. Testamos cada uma. O que sobreviveu mudou.",
        )
        + '<div class="pts" style="margin-top:24px">'
        + cartao_texto(
            "✕",
            "Detector de cascata, o diferencial 2 da Sprint 1, saiu do MVP",
            "A hipótese era que P4 e P5 acumulados escalam para P3 e P2. No dado, <b>87% das "
            "violações são de incidentes isolados</b> e a taxa de escalada observada é de 21%, "
            "contra cerca de 60% que o acaso produziria. O padrão de acúmulo que o mentor "
            "citou também foi testado: correlação de <b>−0,139</b> entre backlog diário e "
            "violações, ou seja, sinal contrário ao esperado.",
            "bad",
        )
        + cartao_texto(
            "✕",
            "Clusterização por DTW não achou grupo nenhum",
            "TimeSeriesKMeans com métrica DTW deu silhueta de <b>0,13</b>, que é ausência de "
            "estrutura. O requisito de classificação ou clusterização passou a ser atendido "
            "pelo classificador de risco, que é onde ele resolve um problema real.",
            "bad",
        )
        + cartao_texto(
            "⇄",
            "XGBoost virou baseline; entrega é a regressão logística",
            "ROC AUC empata dentro do ruído (0,8693 contra 0,8679), mas o PR-AUC da logística é "
            "<b>17% maior</b> (0,2958 contra 0,2526) e é a métrica que vale para evento raro. "
            "Decisivo: a logística prevê <b>48,1 violações onde houve 50</b>; o XGBoost "
            "balanceado prevê 1.007 e inviabiliza a projeção do KPI.",
            "warn",
        )
        + cartao_texto(
            "⇄",
            "SHAP saiu porque em modelo linear ele é conta fechada",
            "A contribuição de cada sinal é <b>peso × desvio da média</b>, exata e sem "
            "amostragem. Conferimos uma vez contra o SHAP: erro de reconstrução na ordem de "
            "10⁻¹⁵. Modelo interpretável por construção em vez de caixa preta com explicação "
            "posterior.",
            "warn",
        )
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 5")


# ─────────────────────────────────────────────────────────────────────────────
# Bloco 3 · gestão (template, slides 6 e 7)
# ─────────────────────────────────────────────────────────────────────────────
def s08_gestao_doc() -> str:
    sprints = [
        ("Sprint 1 · Ideação", "27/04/2026", "Entregue", "5,00", "good"),
        ("Sprint 2 · Arquitetura", "24/05/2026", "Entregue", "5,00", "good"),
        ("Sprint 3 · MVP preliminar", "23/08/2026", "Em entrega", "—", "focus"),
        ("Sprint 4 · Solução final", "08/09/2026", "Planejada", "—", ""),
    ]
    corpo_tab = "".join(
        f"<tr><td><b>{s}</b></td><td>{d}</td><td>{st}</td>"
        f'<td class="n"><b>{n}</b></td></tr>'
        for s, d, st, n, _t in sprints
    )
    conteudo = (
        cabecalho(
            "Documentação do gerenciamento de projetos atualizada",
            "O que foi planejado e o que foi executado",
            "As duas sprints anteriores fecharam com nota máxima. O único ajuste pedido pelo "
            "professor na Sprint 2 foi dedicar um slide explícito à gestão ágil, e é o "
            "próximo slide.",
        )
        + '<div style="display:flex;gap:22px;margin-top:22px;align-items:flex-start">'
        + '<div class="tw" style="flex:1;min-width:0">'
        "<table><thead><tr><th>Sprint</th><th>Entrega</th><th>Situação</th>"
        '<th style="text-align:right">Nota</th></tr></thead>'
        f"<tbody>{corpo_tab}</tbody></table></div>"
        + '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:13px">'
        + cartao_texto(
            "1",
            "Sprint 1 · o que o professor pediu",
            "Ilustrar o impacto para o negócio com números e gráficos. Atendido: a Sprint 3 "
            "traz medição em todo slide de modelo, com baseline ao lado.",
            "good",
        )
        + cartao_texto(
            "2",
            "Sprint 2 · o que o professor pediu",
            "Um slide explícito de gestão ágil. Atendido no slide seguinte, com framework, "
            "quadro e cronograma.",
            "good",
        )
        + cartao_texto(
            "3",
            "Anexos reenviados com a stack corrigida",
            "Os materiais das Sprints 1 e 2 ainda declaravam XGBoost, DTW e cascata. Vão "
            "atualizados junto desta entrega para não contradizer o que foi medido depois.",
            "warn",
        )
        + "</div></div>"
    )
    return _sl(conteudo, tag="Template · slide 6")


def s09_gestao_plano() -> str:
    """Marcos com data conferida em context/status.md e no histórico do repositório."""
    marcos = [
        ("20 e 21/07", "Alvo e escopo de modelagem definidos"),
        ("29/07", "Verificações de robustez e dossiê de defesa"),
        ("03 e 04/08", "Modelo de risco medido; notebooks 04, 05 e 06"),
        ("05/08", "Score de saúde por produto"),
        ("11 a 14/08", "Auditoria dos números e reconstrução das seis abas"),
        ("17/08", "Auditoria visual: 41 capturas, 32 achados corrigidos"),
    ]
    linha_marcos = "".join(
        f'<tr><td class="n" style="white-space:nowrap"><b>{d}</b></td><td>{t}</td></tr>'
        for d, t in marcos
    )
    conteudo = (
        cabecalho(
            "Planejamento e gestão do projeto",
            "Scrum para o ritmo, Kanban para o estado",
            "Quadro no Trello com cinco colunas, do backlog ao concluído, com etiqueta por "
            "sprint, responsável e checklist de validação por entregável. A cadência é de "
            "uma sprint por entrega da FIAP.",
        )
        + '<div style="display:flex;gap:20px;margin-top:20px;flex:1;min-height:0">'
        + '<div style="flex:1.05;min-width:0;display:flex;flex-direction:column;gap:12px">'
        + '<div class="stats">'
        + cartao_num("Framework", "Scrum", "Uma sprint por entrega", "focus")
        + cartao_num("Quadro", "Trello", "Cinco colunas, do backlog ao feito")
        + "</div>"
        + '<div class="tw" style="flex:1;min-height:0">'
        '<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;'
        'text-transform:uppercase;color:var(--tx2);padding:0 16px 10px">'
        "Marcos executados na Sprint 3</div>"
        f"<table><tbody>{linha_marcos}</tbody></table></div>"
        + "</div>"
        + '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:12px">'
        + cartao_texto(
            "1",
            "Como o trabalho foi dividido",
            "Análise exploratória e base compartilhada em dupla; modelagem preditiva e "
            "aplicação com revisão cruzada; deck e validação contra o checklist da sprint "
            "por todos, antes de fechar a entrega.",
        )
        + cartao_texto(
            "2",
            "Canal com a Locaweb",
            "Contato com o mentor Douglas Gouveia pelo Scrum Master do grupo. A mentoria "
            "gerou duas hipóteses que entraram no backlog e foram testadas.",
        )
        + cartao_texto(
            "3",
            "Definição de pronto",
            "Um entregável só fecha quando passa pelo checklist da sprint e quando todo número "
            "afirmado tem célula executada que o produza.",
            "good",
        )
        + "</div></div>"
    )
    return _sl(conteudo, tag="Template · slide 7")


# ─────────────────────────────────────────────────────────────────────────────
# Bloco 4 · arquitetura (template, slides 8 a 11)
# ─────────────────────────────────────────────────────────────────────────────
def s10_arq_visao() -> str:
    conteudo = (
        cabecalho(
            "Arquitetura da solução",
            "Os modelos treinam fora; o contêiner só lê",
            "Prophet, scikit-learn e XGBoost rodam nos notebooks, gravam Parquet e saem de "
            "cena. A aplicação lê arquivo e serve tela. É essa separação que permite entregar "
            "a solução inteira em um contêiner pequeno, sem depender de nuvem específica.",
        )
        + '<div class="stats" style="margin-top:26px">'
        + cartao_num("Pacote lido pelo app", "295 kB", "JSON e Parquet, carregados uma vez por processo", "focus")
        + cartao_num("Abas em produção", "6", "Uma URL por aba, mais quatro rotas de detalhe")
        + cartao_num("Dependências do contêiner", "5", "Django, pandas, pyarrow, gunicorn e whitenoise")
        + "</div>"
        + '<div class="pts" style="margin-top:16px">'
        + cartao_texto(
            "1",
            "Agnóstica de provedor de nuvem",
            "Nenhum serviço proprietário de AWS, Azure ou Google. A Locaweb <b>é</b> uma nuvem: "
            "amarrar a solução a um concorrente inviabilizaria a adoção. O contêiner escuta uma "
            "porta e roda em qualquer lugar.",
        )
        + cartao_texto(
            "2",
            "Sem banco de dados, de propósito",
            "O volume cabe em Parquet e a leitura é feita uma vez por processo. Um banco "
            "acrescentaria operação sem acrescentar capacidade, e tiraria a portabilidade.",
        )
        + cartao_texto(
            "3",
            "Django, e não Streamlit",
            "Decisão tomada na Sprint 1: Streamlit entrega dashboard, não produto. Com Django a "
            "aba tem URL própria, o link da fila filtrada pode ser mandado para alguém e o "
            "detalhe abre como fragmento, sem recarregar a página.",
        )
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 8")


def s11_arq_desenho() -> str:
    def no(kicker: str, titulo: str, texto: str, acc: bool = False) -> str:
        return (
            f'<div class="nd{" acc" if acc else ""}"><div class="nk">{kicker}</div>'
            f'<div class="nh">{titulo}</div><p>{texto}</p></div>'
        )

    conteudo = (
        cabecalho(
            "Desenho da arquitetura da solução",
            "Do arquivo da Locaweb até a tela do turno",
            "Cinco etapas. As três do meio rodam offline e produzem arquivo; só a última fica "
            "de pé em produção.",
        )
        + '<div class="flow">'
        + '<div class="lane"><div class="lk">Etapa 1 · fonte</div><div class="nodes">'
        + no(
            "Entrada",
            "LW-DATASET.xlsx",
            "122.543 incidentes, 19 colunas, jan/2023 a dez/2025. Arquivo oficial entregue "
            "pela Locaweb.",
        )
        + no(
            "Fonte externa",
            "holidays BR",
            "Feriados nacionais. O dataset não traz essa coluna e a sazonalidade depende dela.",
        )
        + "</div></div>"
        + '<div class="lane"><div class="lk">Etapa 2 · preparo</div><div class="nodes">'
        + no(
            "pandas",
            "Base compartilhada",
            "Tipagem das colunas, filtro oficial de elegibilidade e cinco colunas de "
            "calendário. Trava com asserts em 122.543 e 25.600.",
            True,
        )
        + "</div></div>"
        + '<div class="lane"><div class="lk">Etapa 3 · modelos</div><div class="nodes">'
        + no("Prophet", "Volume D+1 a D+7", "Duas séries, P3 e P2, com intervalo de 80%.", True)
        + no(
            "scikit-learn",
            "Risco por incidente",
            "Regressão logística sobre 10 características disponíveis na abertura.",
            True,
        )
        + no(
            "pandas",
            "Projeção, saúde e causas",
            "Fechamento do ano, nota por produto e taxa por código de fechamento.",
            True,
        )
        + "</div></div>"
        + '<div class="lane"><div class="lk">Etapa 4 · pacote</div><div class="nodes">'
        + no(
            "Parquet e JSON",
            "295 kB para a aplicação",
            "Saída dos notebooks agregada num pacote único. O app não treina, não calcula "
            "modelo e não abre o Excel.",
        )
        + "</div></div>"
        + '<div class="lane"><div class="lk">Etapa 5 · produto</div><div class="nodes">'
        + no(
            "Django e Docker",
            "Seis abas no ar",
            "Gráficos desenhados em SVG no servidor. Sobe com um build, em qualquer provedor.",
            True,
        )
        + no(
            "Destinatário",
            "Coordenação de operações",
            "Recebe o briefing na entrada e a fila ordenada durante o turno.",
        )
        + "</div></div></div>"
    )
    return _sl(conteudo, tag="Template · slide 9", classe="dg")


def s12_arq_tec() -> str:
    tec = [
        ("pandas · openpyxl · pyarrow", "2.2.3 · 3.1.5 · 25.0", "Leitura do Excel, tipagem e o Parquet que liga notebook e aplicação"),
        ("holidays", "0.97", "Feriados nacionais, que o dataset não traz e a sazonalidade exige"),
        ("Prophet · cmdstanpy", "1.3.0", "Previsão de volume por prioridade, com intervalo de 80%"),
        ("scikit-learn", "1.6.1", "Regressão logística do risco de OLA, o modelo entregue"),
        ("XGBoost", "3.0.2", "Baseline de comparação do risco. Não é o modelo de produção"),
        ("scipy · statsmodels", "1.18 · 0.14.6", "Correlações, testes e intervalos de confiança das verificações"),
        ("matplotlib · seaborn · plotly", "3.10 · 0.13 · 6.0", "Figuras dos notebooks e do deck"),
        ("Django", "6.1", "Aplicação: seis abas, uma URL por aba, fragmentos para o detalhe"),
        ("gunicorn · whitenoise", "23.0 · 6.9", "Servidor e arquivos estáticos dentro do contêiner"),
        ("Docker", "python:3.13-slim", "Entrega. Um build e a solução roda em qualquer provedor"),
    ]
    corpo_tab = "".join(
        f"<tr><td><b>{n}</b></td><td class=\"n\" style=\"white-space:nowrap;color:var(--tx2)\">{v}</td>"
        f"<td>{p}</td></tr>"
        for n, v, p in tec
    )
    conteudo = (
        cabecalho(
            "Descrição da arquitetura da solução",
            "Cada peça e o problema que ela resolve",
            "Dez tecnologias, todas com versão fixada. Nenhuma entrou por moda: a coluna da "
            "direita é o motivo de existir.",
        )
        + '<div class="tw" style="margin-top:20px;flex:1;min-height:0;overflow:hidden">'
        "<table><thead><tr><th>Tecnologia</th>"
        '<th style="text-align:right">Versão</th><th>Papel na solução</th></tr></thead>'
        f"<tbody>{corpo_tab}</tbody></table></div>"
    )
    return _sl(conteudo, tag="Template · slide 10")


def s13_arq_dados() -> str:
    conteudo = (
        cabecalho(
            "Descrição da arquitetura da solução · fontes e tratamento",
            "Uma fonte oficial, um filtro que decide tudo",
            "O dataset da Locaweb é a única fonte de incidente. A biblioteca de feriados é a "
            "única fonte externa. O que separa os dois é a regra de elegibilidade, e errar "
            "nela contamina todo o resto.",
        )
        + '<div class="stats" style="margin-top:24px">'
        + cartao_num("Linhas lidas", "122.543", "Aba Dataset Geral, 19 colunas originais")
        + cartao_num("Valem para o KPI", "25.600", "Pelo campo oficial Entrou para KPI?", "focus")
        + cartao_num("Se o filtro fosse só Incidente Pai", "107.416", "88% da base. É o erro clássico", "bad")
        + "</div>"
        + '<div class="pts" style="margin-top:16px">'
        + cartao_texto(
            "1",
            "Usamos o campo oficial, não a regra reescrita",
            "O campo <b>Entrou para KPI?</b> já codifica as três condições juntas: prioridade "
            "1, 2 ou 3, campo Incidente Pai vazio e status diferente de Sem Intervenção. "
            "Reimplementar a regra criaria uma segunda verdade dentro da casa do cliente.",
        )
        + cartao_texto(
            "2",
            "Cinco colunas de calendário derivadas na preparação",
            "Dia, dia da semana, hora, ano e mês saem da data de abertura, e o feriado vem da "
            "biblioteca. São as características que sustentam a sazonalidade do Prophet.",
        )
        + cartao_texto(
            "3",
            "Nenhum dado pessoal na base",
            "Varredura feita antes de publicar: zero e-mail, CPF, telefone ou endereço IP; "
            "nenhuma coluna identifica pessoa. Os identificadores são de ativo e de equipe. "
            "O campo de origem só tem Manual e Monitoramento.",
            "good",
        )
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 11")


# ─────────────────────────────────────────────────────────────────────────────
# Bloco 5 · MVP, os modelos (template, slide 12)
# ─────────────────────────────────────────────────────────────────────────────
def s14_div_mvp() -> str:
    conteudo = (
        '<div class="lft">'
        + cabecalho(
            "Versão preliminar do MVP",
            "O que já está de pé",
            "Três modelos medidos contra baseline, duas análises de apoio e uma aplicação "
            "Django com seis abas servindo a saída deles. Daqui em diante, tudo é evidência.",
        )
        + '<div class="chip">Nos próximos slides: <b>a medição de cada modelo</b>, '
        "depois a aplicação, tela por tela.</div></div>"
        + '<div class="rgt">'
        + cartao_num("Notebooks executados", "7", "Da base compartilhada à saúde por produto", "focus")
        + cartao_num("Abas no ar", "6", "Mais quatro aprofundamentos que abrem por cima")
        + cartao_num("Modelos entregues", "3", "Volume, risco por incidente e projeção do KPI", "good")
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 12", escuro=True, classe="dv")


def s15_volume() -> str:
    """Números: 03_previsao_volume.ipynb, rolling backtest e seção 4.10 de robustez."""
    linhas = [
        ("P3 · Média", "11,3", "18,2", "11,8", "empate", ""),
        ("P2 · Alta", "5,7", "4,9", "4,2", "+15%", "good"),
    ]
    corpo_tab = "".join(
        f'<tr><td><b>{p}</b></td><td class="n">{b1}</td><td class="n">{b2}</td>'
        f'<td class="n"><b>{pr}</b></td>'
        f'<td class="n"><b style="color:var(--{"good" if t else "tx2"})">{g}</b></td></tr>'
        for p, b1, b2, pr, g, t in linhas
    )
    conteudo = (
        cabecalho(
            "MVP · modelo 1 de 3",
            "Previsão de volume, medida contra dois baselines",
            "Prophet com sazonalidade semanal ligada, anual desligada, feriados nacionais e "
            "intervalo de 80%. Validado por <b>rolling backtest</b>: retreina a cada semana e "
            "prevê D+1 a D+7, que é como o modelo seria usado de verdade.",
        )
        + '<div style="display:flex;gap:22px;margin-top:20px;align-items:flex-start">'
        + '<div style="flex:1.2;min-width:0;display:flex;flex-direction:column;gap:13px">'
        + '<div class="tw">'
        '<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;'
        'color:var(--tx2);padding:0 16px 12px">Erro médio absoluto por dia, D+1 a D+7</div>'
        "<table><thead><tr><th>Prioridade</th>"
        '<th style="text-align:right">Repete a semana</th>'
        '<th style="text-align:right">Média de 7 dias</th>'
        '<th style="text-align:right">Prophet</th>'
        '<th style="text-align:right">Ganho</th></tr></thead>'
        f"<tbody>{corpo_tab}</tbody></table>"
        '<p style="font-size:13px;color:var(--tx2);padding:12px 16px 0;line-height:1.45">'
        "Os dois baselines aparecem de propósito: o mais forte muda conforme a série, e "
        "comparar só com o mais fraco inflaria o ganho. <b>No P3 o baseline vence por 4,5% e "
        "escrevemos isso.</b></p></div>"
        + cartao_texto(
            "⟳",
            "Como o backtest roda",
            "A origem anda de quatro em quatro dias sobre o período de teste. Em cada parada o "
            "modelo é <b>retreinado do zero</b> com o que existia até ali e prevê os sete dias "
            "seguintes, com o erro medido por horizonte. Um treino único prevendo o trimestre "
            "inteiro daria número melhor e não corresponderia ao uso.",
        )
        + "</div>"
        + '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:12px">'
        + cartao_texto(
            "1",
            "Um ano de dado denso, e o modelo respeita isso",
            "Dos elegíveis ao KPI, 87 estão em 2023, 357 em 2024 e <b>25.156 em 2025</b>. Há "
            "dado para aprender o padrão de dia da semana, não para aprender padrão anual. "
            "Sazonalidade anual desligada por essa razão.",
        )
        + cartao_texto(
            "2",
            "Três métodos batem no mesmo teto",
            "Repetir a semana, Prophet e regressão de calendário chegam ao mesmo erro. O sinal "
            "previsível é o calendário: semana e feriado. O resto não é limite da ferramenta.",
        )
        + cartao_texto(
            "!",
            "A banda do P3 reprova e reportamos assim",
            "Cobertura medida em 92 dias: <b>84,8% no P2</b> contra 80% nominais, calibrada; "
            "<b>60,9% no P3</b>, que subestima a incerteza. A queda de nov e dez estava fora "
            "do que um treino até setembro permitia prever.",
            "warn",
        )
        + "</div></div>"
    )
    return _sl(conteudo, tag="Template · slide 12")


def s16_risco() -> str:
    """Números: 04_risco_ola.ipynb, corte out-of-time 01/10/2025."""
    conteudo = (
        cabecalho(
            "MVP · modelo 2 de 3",
            "Risco de violação por incidente",
            "Regressão logística sobre <b>10 características disponíveis no instante da "
            "abertura</b>. Duração, status e código de fechamento ficaram de fora: são "
            "desfecho, e usá-los seria vazamento. Treino até setembro, teste de outubro a "
            "dezembro com 50 violações em 5.183 incidentes.",
        )
        + '<div class="stats" style="margin-top:22px">'
        + cartao_num("ROC AUC", "0,8693", "Contra 0,8679 do XGBoost, empate dentro do ruído")
        + cartao_num("PR-AUC", "0,2958", "31 vezes a taxa da base, que é 0,0096", "focus")
        + cartao_num("Concentração", "72%", "Das violações estão nos 20% de maior risco", "good")
        + cartao_num("Calibração", "48,1", "Violações previstas onde houve 50", "good")
        + "</div>"
        + '<div style="display:flex;gap:22px;margin-top:16px;flex:1;min-height:0">'
        + '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:12px">'
        + cartao_texto(
            "1",
            "A entrega é a ordenação, não um alarme",
            "Onde cortar a fila é decisão da operação, porque depende da capacidade do dia. "
            "Nas 50 primeiras posições há <b>15 violações</b>: 30% de precisão num evento que "
            "acontece em 0,96% dos casos.",
        )
        + cartao_texto(
            "2",
            "Acurácia não é reportada, e por um motivo",
            "Um classificador que nunca sinaliza nada atinge <b>99,04% de acurácia</b>, acima "
            "do modelo. A métrica premia a inação, então a entrega é a matriz por corte.",
            "warn",
        )
        + "</div>"
        + '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:12px">'
        + cartao_texto(
            "3",
            "Não é memorização",
            "Metade dos incidentes de teste tem combinação de características <b>inédita</b>, "
            "e entre eles estão 27 das 50 violações. Nesse subconjunto o ROC AUC fica em "
            "0,8151.",
            "good",
        )
        + cartao_texto(
            "4",
            "A ordenação é estável em três cortes de data",
            "ROC AUC entre 0,8684 e 0,8774. Já a soma das probabilidades oscila mais, e é por "
            "isso que a projeção do KPI sai como faixa e não como número único.",
        )
        + "</div></div>"
    )
    return _sl(conteudo, tag="Template · slide 12")


def s17_projecao() -> str:
    """Números: 06_projecao_kpi.ipynb, validação em 5 datas × 2 prioridades."""
    conteudo = (
        cabecalho(
            "MVP · modelo 3 de 3",
            "Onde o ano fecha, decomposto em três parcelas",
            "O modelo de risco não pode pontuar incidente que ainda não existe. Então a "
            "projeção separa o que já tem desfecho, o que está aberto e o que ainda vai "
            "entrar, e usa a ferramenta certa em cada parte.",
        )
        + '<div class="pts" style="margin-top:22px">'
        + cartao_texto(
            "1",
            "Já resolvido antes do corte · contagem",
            "Desfecho registrado, sem estimativa nenhuma. Na data simulada são <b>3.884 dos "
            "5.159 incidentes de P2</b> e 14.960 dos 19.997 de P3. A maior parte da projeção "
            "é fato contado, não previsão.",
            "good",
        )
        + cartao_texto(
            "2",
            "Aberto e sem desfecho · modelo de risco",
            "Características conhecidas, resultado não. Cada caso entra pela probabilidade "
            "que o modelo dá a ele.",
        )
        + cartao_texto(
            "3",
            "Ainda não aberto · Prophet mais taxa esperada",
            "Volume previsto multiplicado pela taxa de violação da prioridade. É a única "
            "parcela totalmente estimada.",
        )
        + "</div>"
        + '<div class="stats" style="margin-top:16px">'
        + cartao_num("Projeções validadas", "10", "Cinco datas, de agosto a dezembro, nas duas prioridades")
        + cartao_num("Faixa conteve o real", "7 de 10", "E em 2 das 3 em que o centro cruzou o limite", "focus")
        + cartao_num("Situação acertada", "7 de 10", "Cinco de cinco no P2, dois de cinco no P3", "warn")
        + cartao_num("Erros otimistas", "0", "Todo erro projeta mais violação do que houve", "good")
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 12")


def s18_analises() -> str:
    """Números: 05_causas_recorrentes.ipynb e 07_saude_produto.ipynb, janela jan a set/2025."""
    fam = [
        ("Problema inédito", "38,2%", "59,0%", "1,46%", "bad"),
        ("Repete 2 a 4 vezes", "10,1%", "15,4%", "1,44%", ""),
        ("Repete 5 a 19 vezes", "12,0%", "12,2%", "0,96%", ""),
        ("Repete 20 vezes ou mais", "39,7%", "13,3%", "0,31%", "good"),
    ]
    corpo_tab = "".join(
        f'<tr><td><b>{f}</b></td><td class="n">{v}</td><td class="n">{q}</td>'
        f'<td class="n"><b style="color:var(--{t if t else "head"})">{tx}</b></td></tr>'
        for f, v, q, tx, t in fam
    )
    conteudo = (
        cabecalho(
            "MVP · as duas análises que sustentam as telas",
            "O que a operação já viu, ela resolve",
            "O achado mais forte da análise de causas, e o que justifica a existência do score "
            "de saúde por produto.",
        )
        + '<div style="display:flex;gap:22px;margin-top:20px;align-items:flex-start">'
        + '<div class="tw" style="flex:1.15;min-width:0">'
        '<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;'
        'color:var(--tx2);padding:0 16px 12px">Violação por familiaridade do problema</div>'
        "<table><thead><tr><th>Quantas vezes já apareceu</th>"
        '<th style="text-align:right">Do volume</th>'
        '<th style="text-align:right">Das violações</th>'
        '<th style="text-align:right">Taxa</th></tr></thead>'
        f"<tbody>{corpo_tab}</tbody></table>"
        '<p style="font-size:13px;color:var(--tx2);padding:12px 16px 0;line-height:1.45">'
        "Queda de <b>4,7 vezes</b>, monotônica. Resistiu a três tratamentos de texto e a "
        "quatro estratos de controle, inclusive dentro do P2 e dentro do P3.</p></div>"
        + '<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:12px">'
        + cartao_texto(
            "★",
            "Por isso o score de saúde existe",
            "Quatro produtos estão em <b>risco latente</b>: concentram problema inédito acima "
            "da mediana e ainda violam pouco. <b>Nenhum deles seria sinalizado pelo modelo de "
            "risco</b>, porque a avaliação é por incidente e cada caso isolado tem "
            "probabilidade baixa. O padrão só existe no agregado do produto.",
            "good",
        )
        + cartao_texto(
            "!",
            "Um quinto das violações fecha sem causa",
            "O código Outro é 8,0% do volume e <b>22,9% das violações</b>. O dado não separa "
            "causa difícil de caso que se arrastou sem diagnóstico, e as duas leituras pedem "
            "a mesma ação: melhorar o diagnóstico.",
            "warn",
        )
        + cartao_texto(
            "✓",
            "E o que compensa automatizar",
            "Os vinte problemas mais recorrentes são <b>26% do volume</b> e violam <b>0,29%</b>, "
            "bem abaixo dos 0,94% da base. Volume alto com risco baixo é exatamente o perfil "
            "que dá retorno ao padronizar o atendimento.",
        )
        + "</div></div>"
    )
    return _sl(conteudo, tag="Template · slide 12")


# ─────────────────────────────────────────────────────────────────────────────
# Bloco 6 · MVP, a aplicação tela por tela (template, slide 13)
# ─────────────────────────────────────────────────────────────────────────────
def s19_div_telas() -> str:
    conteudo = (
        '<div class="lft">'
        + cabecalho(
            "Versão preliminar do MVP · a aplicação",
            "Seis abas, dez telas",
            "Tudo o que vem a seguir é print da aplicação Django rodando, com a saída real dos "
            "modelos. A ferramenta simula um relógio parado em <b>01/10/2025 às 15h</b> e só "
            "mostra o que existiria naquele instante.",
        )
        + '<div class="chip">Avaliação de modelo fica no slide. '
        "<b>A tela mostra o turno, não o gabarito.</b></div></div>"
        + '<div class="rgt">'
        + cartao_num("Relógio da aplicação", "01/10/25", "Parado às 15h, com o dia pela metade", "focus")
        + cartao_num("Prioridades em toda tela", "P3 e P2", "Lado a lado, com meta própria cada uma")
        + cartao_num("Vocabulário interno na tela", "0", "Depois da auditoria de linguagem de 17/08", "good")
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 13", escuro=True, classe="dv")


def slide_print(nome: str, eyebrow: str, titulo: str, legenda: str, tag: str) -> str:
    conteudo = (
        '<div class="row"><div>'
        f'<span class="eb">{eyebrow}</span><h1 class="tt">{titulo}</h1></div>'
        f'<p class="cap">{legenda}</p></div>'
        f'<div class="br"><div class="bar"><i></i><i></i><i></i>'
        f'<span class="url">{URL_APP}</span></div>'
        f'<img src="{_img(nome)}" alt=""></div>'
    )
    return _sl(conteudo, tag=tag, classe="pr")


def s30_mockup() -> str:
    conteudo = (
        '<div style="text-align:center">'
        '<span class="eb" style="justify-content:center">A ferramenta em uso</span>'
        '<h1 class="tt" style="font-size:36px">O turno começa aqui</h1></div>'
        '<div class="nb"><div class="scr">'
        f'<img src="{_img("01-panorama")}" alt=""></div>'
        '<div class="base"></div></div>'
        '<p class="cap">A coordenação abre o Cronos, lê o briefing e já sabe onde agir. '
        "<b>Nenhuma pergunta foi feita.</b></p>"
    )
    return _sl(conteudo, tag="Mockup", classe="mk")


def s31_dados() -> str:
    """Amostra real, lida de data/interim/incidentes_kpi.parquet."""
    amostra = [
        ("INC8654075", "2 - Alta", "lrel", "31/12/2025 18:06", "5.443", "NAO"),
        ("INC8653993", "2 - Alta", "lhvp", "31/12/2025 14:45", "2.052", "NAO"),
        ("INC8653923", "2 - Alta", "lhco", "31/12/2025 11:43", "1.382", "NAO"),
        ("INC8653899", "2 - Alta", "lssl", "31/12/2025 11:13", "1.482", "NAO"),
    ]
    corpo_tab = "".join(
        f'<tr><td style="font-family:var(--mono);font-size:13.5px"><b>{a}</b></td>'
        f"<td>{b}</td><td>{c}</td><td>{d}</td>"
        f'<td class="n">{e}</td><td class="n">{f}</td></tr>'
        for a, b, c, d, e, f in amostra
    )
    conteudo = (
        cabecalho(
            "Versão preliminar do MVP · dados utilizados",
            "A base compartilhada, e como ela é conferida",
            "Um notebook só produz a base que todos os outros leem. Ele trava o resultado com "
            "asserts: se o filtro mudar de comportamento, a execução falha em vez de publicar "
            "número errado.",
        )
        + '<div class="tw" style="margin-top:20px">'
        '<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;'
        'color:var(--tx2);padding:0 16px 12px">Amostra do Parquet gerado · 25.600 linhas × 24 colunas'
        "</div><table><thead><tr><th>Número</th><th>Prioridade</th><th>Produto</th>"
        '<th>Aberto</th><th style="text-align:right">Duração (s)</th>'
        '<th style="text-align:right">KPI violado</th></tr></thead>'
        f"<tbody>{corpo_tab}</tbody></table></div>"
        + '<div class="stats" style="margin-top:auto">'
        + cartao_num("Colunas originais", "19", "Como vieram no arquivo da Locaweb")
        + cartao_num("Derivadas no preparo", "5", "Dia, dia da semana, hora, ano e mês", "focus")
        + cartao_num("Asserts de invariante", "2", "Travam 122.543 no total e 25.600 elegíveis", "good")
        + cartao_num("Preenchimento de Encerrado", "100%", "Verificado antes de acusar o modelo por queda", "good")
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 13")


def s32_fecho() -> str:
    conteudo = (
        '<span class="eb">Finalização e agradecimentos</span>'
        '<div class="big">Obrigado.</div>'
        '<p class="lead" style="max-width:840px">Por confiar no Cronos, abrir a operação real '
        "e apontar as hipóteses que valia a pena testar. Duas delas não se confirmaram, e "
        "descobrir isso foi parte do trabalho.</p>"
        '<div class="cards">'
        '<div class="fcd"><div class="fk">Empresa parceira</div>'
        '<div class="fv">Locaweb</div>'
        '<div class="fs">Douglas Gouveia · Gerente Executivo de Operações</div>'
        "<p>Pelo dataset, pela mentoria e pelas duas hipóteses que viraram investigação.</p>"
        "</div>"
        '<div class="fcd"><div class="fk">Instituição</div>'
        '<div class="fv">FIAP</div>'
        '<div class="fs">Tecnólogo em Data Science · Turma 2TSCOA</div>'
        "<p>Pela estrutura, pelos professores tutores e pelo formato que aproxima a "
        "faculdade do mercado.</p></div>"
        '<div class="fcd"><div class="fk">Próxima parada</div>'
        '<div class="fv">Sprint 4</div>'
        '<div class="fs">Solução final · 08/09/2026</div>'
        "<p>Aplicação publicada, vídeo de demonstração e a simulação de custo de operação "
        "que o mentor pediu.</p></div>"
        "</div>"
    )
    return _sl(conteudo, tag="Template · slide 14", escuro=True, classe="fc")


# ─────────────────────────────────────────────────────────────────────────────
def slides_proprios() -> dict[str, str]:
    """Os slides escritos aqui, por nome. O bloco analítico vem pronto de outro lugar."""
    proprios = {
        "capa": s01_capa(),
        "equipe": s02_equipe(),
        "contexto": s03_contexto(),
        "problema": s04_problema(),
        "escopo": s05_escopo(),
        "solucao": s06_solucao(),
        "mudou": s07_mudou(),
        "gestao-documentacao": s08_gestao_doc(),
        "gestao-planejamento": s09_gestao_plano(),
        "arquitetura-visao": s10_arq_visao(),
        "arquitetura-desenho": s11_arq_desenho(),
        "arquitetura-tecnologias": s12_arq_tec(),
        "arquitetura-dados": s13_arq_dados(),
        "divisoria-telas": s19_div_telas(),
        "mockup": s30_mockup(),
        "dados": s31_dados(),
        "fecho": s32_fecho(),
    }
    for nome, eb, tt, cap, tag in TELAS + MODAIS:
        proprios[nome] = slide_print(nome, eb, tt, cap, tag)
    return proprios


def ordem() -> list[str]:
    """A sequência final do deck, na ordem do template da FIAP.

    Os cinco slides de resumo de modelo que existiam aqui saíram: o bloco analítico de julho
    diz a mesma coisa em 38 slides e com os gráficos dos notebooks ao lado. Manter os dois
    seria dizer duas vezes, uma delas pior.
    """
    return (
        [
            "capa",                      # template 1 e 2
            "equipe",
            "contexto",                  # template 3
            "problema",                  # template 4
            "escopo",
            "solucao",                   # template 5
            "mudou",
            "gestao-documentacao",       # template 6
            "gestao-planejamento",       # template 7
            "arquitetura-visao",         # template 8
            "arquitetura-desenho",       # template 9
            "arquitetura-tecnologias",   # template 10
            "arquitetura-dados",         # template 11
        ]
        + ANALISE                        # template 12 e 13: a evidência analítica
        + ["divisoria-telas"]            # template 13: a aplicação
        + [nome for nome, *_ in TELAS + MODAIS]
        + ["mockup", "dados", "fecho"]   # template 14
    )


def escreve_html() -> list[Path]:
    """Grava os slides próprios e devolve a sequência inteira já resolvida em caminho.

    Slide do bloco analítico não é reescrito: ele é lido de onde está. Copiar o HTML para cá
    criaria uma segunda cópia que envelheceria em silêncio.
    """
    SAIDA.mkdir(parents=True, exist_ok=True)
    proprios = slides_proprios()
    caminhos: list[tuple[str, Path]] = []
    for pos, nome in enumerate(ordem(), 1):
        if nome in proprios:
            destino = SAIDA / f"{pos:02d}-{nome}.html"
            destino.write_text(pagina(proprios[nome], nome), encoding="utf-8")
        else:
            destino = DECK_ANALISE / f"{nome}.html"
            if not destino.exists():
                raise FileNotFoundError(f"slide do bloco analítico não encontrado: {destino}")
        caminhos.append((f"{pos:02d}-{nome}", destino))
    return caminhos


def renderiza_png(caminhos: list[tuple[str, Path]]) -> list[Path]:
    """Cada HTML vira um PNG em 2×, que é o que entra no .pptx."""
    from playwright.sync_api import sync_playwright

    SAIDA_PNG.mkdir(parents=True, exist_ok=True)
    pngs = []
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(channel="chrome")
        page = navegador.new_context(
            viewport={"width": LARGURA, "height": ALTURA},
            device_scale_factor=2,
        ).new_page()
        for nome, html in caminhos:
            page.goto(html.resolve().as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(450)
            destino = SAIDA_PNG / f"{nome}.png"
            page.locator(".slide").first.screenshot(path=str(destino))
            pngs.append(destino)
        navegador.close()
    print(f"     {len(pngs)} slides renderizados")
    return pngs


def monta_pptx(pngs: list[Path]) -> None:
    """Um slide por PNG, sangrado. É o mesmo formato entregue na Sprint 2."""
    from pptx import Presentation
    from pptx.util import Emu

    prs = Presentation()
    prs.slide_width = Emu(12192000)  # 13,333 in
    prs.slide_height = Emu(6858000)  # 7,5 in
    branco = prs.slide_layouts[6]
    for png in pngs:
        s = prs.slides.add_slide(branco)
        s.shapes.add_picture(
            str(png), 0, 0, width=prs.slide_width, height=prs.slide_height
        )
    prs.save(PPTX)


def main() -> None:
    print("1/3 · escrevendo HTML dos slides próprios")
    caminhos = escreve_html()
    proprios = sum(1 for _, p in caminhos if p.parent == SAIDA)
    print(f"     {proprios} próprios + {len(caminhos)-proprios} do bloco analítico")
    print("2/3 · renderizando PNG")
    pngs = renderiza_png(caminhos)
    print("3/3 · montando o .pptx")
    monta_pptx(pngs)
    print(f"Pronto: {PPTX.name} ({len(pngs)} slides)")


if __name__ == "__main__":
    main()
