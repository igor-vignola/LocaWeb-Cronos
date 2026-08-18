# -*- coding: utf-8 -*-
"""Monta o deck da Sprint 3: HTML de cada slide, PNG de cada HTML e o .pptx final.

A ordem segue o template oficial da FIAP
(`assets/Templates/03Template_MVP_Preliminar_Challenge_2026_01_locaweb.pptx`), com os mesmos
títulos. Onde o conteúdo pede mais espaço, um item do template vira dois slides. Foi o que a
Sprint 2 fez, e tirou 5,00.

O deck tem duas origens:

* **este arquivo** escreve a abertura (identificação, contexto, problema, proposta, gestão e
  arquitetura), os dez prints da aplicação, o mockup, a amostra de dados e o fecho;
* **`prototipos/slides/mvp/deck/`** traz os 38 slides de análise e modelagem construídos em
  julho, que carregam os gráficos exportados dos notebooks. O builder os lê de onde estão,
  sem copiar, para não existir uma segunda cópia envelhecendo em silêncio.

Uso, com a aplicação já capturada por `captura_telas.py` e as figuras por `figuras_deck.py`:

    .venv/Scripts/python scripts/monta_deck_sprint3.py

Duas regras atravessam o arquivo inteiro. **Todo número aqui saiu de célula executada**, e a
origem está anotada no comentário do slide. E métrica de avaliação de modelo é assunto de
slide, nunca de tela: o sistema simula um relógio parado em 01/10/2025 15h.
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
FIGS = SAIDA / "figs"
PPTX = RAIZ / "sprints" / "EC_Sprint_3_2TSCOA_mvp_preliminar_Cronos_SuperDataBros.pptx"

# Os 38 slides de análise e modelagem, na ordem do `viewer.html`, escolhendo a primeira
# variação de cada um, que é a que o viewer abre.
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
        "assim que aparece a causa pequena que viola muito.",
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
    return (PRINTS / f"{nome}.png").resolve().as_uri()


def _fig(nome: str) -> str:
    return (FIGS / f"{nome}.png").resolve().as_uri()


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
# Identificação · template, slides 1 e 2
# ─────────────────────────────────────────────────────────────────────────────
def s01_capa() -> str:
    return (
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
            "Nomes em ordem alfabética, como pede a norma de entrega. O mentor da Locaweb "
            "acompanha pelo Scrum Master do grupo.",
        )
        + '<div class="tw" style="margin-top:26px"><table><thead><tr>'
        '<th>Integrante</th><th style="text-align:right">RM</th><th>Turma</th>'
        f"</tr></thead><tbody>{tabela}</tbody></table></div>"
        + '<div class="stats" style="margin-top:20px">'
        + cartao_num("Solução", "Cronos", "Veja antes. Aja antes.", "focus")
        + cartao_num("Mentor Locaweb", "D. Gouveia", "Gerente Executivo de Operações")
        + cartao_num("Sprints entregues", "2 de 4", "Ideação e Arquitetura, ambas 5,00", "good")
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 2")


# ─────────────────────────────────────────────────────────────────────────────
# Contexto e proposta · template, slides 3, 4 e 5
# ─────────────────────────────────────────────────────────────────────────────
def s03_contexto() -> str:
    """A régua oficial, do `Dicionário de Dados - v2.docx`. O fechado de 2025 sai do parquet."""
    degraus = [
        ("150%", "até 30", "até 200", 150),
        ("125%", "31 a 35", "201 a 230", 125),
        ("100%", "36 a 39", "231 a 263", 100),
        ("75%", "40 a 45", "264 a 290", 75),
        ("50%", "46 a 53", "291 a 320", 50),
        ("0%", "54 ou mais", "321 ou mais", 0),
    ]
    tons = {
        150: ("#DCF2E6", "var(--good)"),
        125: ("#E7F6EE", "var(--good)"),
        100: ("#EEF2F7", "var(--tx)"),
        75: ("#FBF1DC", "var(--warn)"),
        50: ("#FCECEC", "var(--bad)"),
        0: ("#F7DCDC", "var(--bad)"),
    }

    def coluna(pri: str, idx: int, pousou: int, fechou: str) -> str:
        passos = ""
        for nota, faixa_p2, faixa_p3, altura in degraus:
            faixa = faixa_p2 if pri == "P2" else faixa_p3
            fundo, cor = tons[altura]
            # a altura do degrau é a própria nota, então a barra de 150% precisa encostar no
            # topo do cartão para a proporção ser lida sem consultar o rótulo
            px = max(int(altura * 2.32), 30)
            aqui = (
                f'<span class="aq" style="background:{fundo};color:{cor}">'
                f"2025 fechou aqui</span>"
                if altura == pousou
                else '<span class="aq" style="opacity:0">.</span>'
            )
            passos += (
                f'<div class="stp">{aqui}'
                f'<div class="bar" style="height:{px}px;background:{fundo};color:{cor}">'
                f"{nota}</div>"
                f'<span class="rng">{faixa}</span></div>'
            )
        return (
            f'<div class="col"><div class="ch">{pri} · <b>{fechou}</b></div>'
            f'<div class="cs">Violações de OLA no ano, contra os seis degraus.</div>'
            f'<div class="steps">{passos}</div></div>'
        )

    conteudo = (
        cabecalho(
            "Contextualização do problema",
            "O KPI da Locaweb é uma escada de seis degraus",
            "A operação roda 24 por 7 e é medida por quantas violações de OLA acumula no ano. "
            "Passar de uma faixa não zera o indicador: derruba um degrau, e o degrau vale "
            "para o ano inteiro. Entre 39 e 40 violações de P2 existem 25 pontos.",
        )
        + '<div class="duo">'
        + coluna("P3", 1, 150, "fechou 2025 com 196")
        + coluna("P2", 2, 75, "fechou 2025 com 42")
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 3", classe="esc")


def s04_problema() -> str:
    """Figura de `figuras_deck.py`, calculada sobre `incidentes_kpi.parquet`."""
    conteudo = (
        '<div class="row"><div>'
        '<span class="eb">Problema a ser resolvido</span>'
        '<h1 class="tt">O P2 perdeu a meta em novembro, '
        'e ninguém viu chegando</h1></div>'
        '<p class="cap">Até outubro o ano parecia tranquilo nas duas prioridades. '
        "Em trinta dias o P2 atravessou <b>duas faixas de uma vez</b>, e só dava para saber "
        "somando o ano fechado.</p></div>"
        f'<div class="art"><img src="{_fig("ano_virou")}" alt=""></div>'
        '<div class="ps">'
        "<div class=\"pz\"><b>O indicador é anual e a leitura é retrospectiva.</b> "
        "Quem opera vê o incidente de hoje; a conta que decide a nota só fecha em dezembro."
        "</div>"
        "<div class=\"pz\"><b>Seis violações num mês custaram 50 pontos.</b> "
        "Nenhuma delas foi grande o suficiente para chamar atenção sozinha.</div>"
        "<div class=\"pz\"><b>É esse intervalo que o Cronos ataca.</b> "
        "Projetar onde o ano fecha enquanto ainda existe mês para mudar o resultado.</div>"
        "</div>"
    )
    return _sl(conteudo, tag="Template · slide 4", classe="fg")


def s05_solucao() -> str:
    itens = [
        (
            "Antecipar incidentes · D+1 e D+7",
            "Prophet, <em>duas séries</em>",
            "Uma para P3 e outra para P2, com sazonalidade semanal e feriados nacionais. "
            "Erro de <b>11,8 por dia no P3 e 4,2 no P2</b>, medido em rolling backtest.",
        ),
        (
            "Identificar tendência por prioridade",
            "Sazonalidade e <em>saúde por produto</em>",
            "Dia da semana, hora de chegada e a nota de 0 a 100 nos 15 produtos que passam "
            "de 200 incidentes.",
        ),
        (
            "Projetar impacto no KPI",
            "Projeção em <em>três parcelas</em>",
            "O que já tem desfecho é contagem. O que está aberto vai pelo modelo de risco. "
            "O que ainda não entrou vai pelo Prophet.",
        ),
        (
            "Apoiar a decisão operacional",
            "Fila de risco <em>por incidente</em>",
            "Regressão logística sobre 10 características da abertura. Os <b>20% de maior "
            "risco concentram 72% das violações</b>.",
        ),
    ]
    grade = "".join(
        f'<div class="it"><span class="ex">{ex}</span>'
        f'<span class="an">{an}</span><p>{p}</p></div>'
        for ex, an, p in itens
    )
    conteudo = (
        cabecalho(
            "Proposta de solução",
            "O desafio pede quatro coisas",
            "Uma peça responde cada uma. O Cronos não tem caixa de perguntas: ele publica o "
            "que vem pela frente na entrada do turno.",
        )
        + f'<div class="grid">{grade}</div>'
    )
    return _sl(conteudo, tag="Template · slide 5", classe="mp")


def s06_mudou() -> str:
    """Justificativas em `docs/sprint-3-mvp.md`, seção "Testado e descartado"."""
    linhas = [
        (
            "Detector de cascata",
            "Fora do MVP",
            True,
            "<b>87%</b> das violações são de incidentes isolados, e a taxa de escalada "
            "observada é de 21% contra os cerca de 60% que o acaso produziria.",
        ),
        (
            "Clusterização por DTW",
            "Fora do MVP",
            True,
            "Silhueta de <b>0,13</b>, que é ausência de estrutura. O requisito de "
            "classificação passou para o modelo de risco.",
        ),
        (
            "XGBoost no risco",
            "Regressão logística",
            False,
            "PR-AUC <b>17% maior</b> e calibração honesta: prevê 48,1 violações onde houve "
            "50. O XGBoost balanceado prevê 1.007.",
        ),
        (
            "SHAP",
            "Peso × desvio da média",
            False,
            "Em modelo linear a conta é fechada e exata. Conferida uma vez contra o SHAP, "
            "com erro de reconstrução na ordem de <b>10⁻¹⁵</b>.",
        ),
        (
            "Acúmulo de backlog",
            "Sem suporte no dado",
            True,
            "Hipótese levantada na mentoria. Correlação de <b>−0,139</b> entre backlog "
            "diário e violações: o sinal aponta para o lado contrário.",
        ),
    ]
    lst = "".join(
        f'<div class="ln"><span class="de">{de}</span>'
        f'<span class="ar">→</span>'
        f'<span class="pa{" out" if out else ""}">{para}</span>'
        f'<span class="pq">{pq}</span></div>'
        for de, para, out, pq in linhas
    )
    conteudo = (
        cabecalho(
            "Proposta de solução · o que mudou desde a Sprint 2",
            "Cinco ideias foram ao dado e três não voltaram",
            "A arquitetura aprovada em maio declarava detector de cascata, XGBoost, "
            "clusterização e SHAP. Cada uma foi testada.",
        )
        + f'<div class="lst">{lst}</div>'
    )
    return _sl(conteudo, tag="Template · slide 5", classe="dp")


# ─────────────────────────────────────────────────────────────────────────────
# Gestão · template, slides 6 e 7
# ─────────────────────────────────────────────────────────────────────────────
def s07_gestao_doc() -> str:
    marcos = [
        ("27/04/2026", "Ideação", "ok", "Entregue · <b>5,00</b>",
         "Pediram ilustrar o impacto com número e gráfico."),
        ("24/05/2026", "Arquitetura", "ok", "Entregue · <b>5,00</b>",
         "Pediram um slide explícito de gestão ágil."),
        ("23/08/2026", "MVP preliminar", "now", "<b>Esta entrega</b>",
         "Modelos medidos, aplicação de pé e os dois pedidos atendidos."),
        ("08/09/2026", "Solução final", "", "Planejada",
         "Aplicação publicada, vídeo e o custo de operação que o mentor pediu."),
    ]
    linha = "".join(
        f'<div class="mc {cls}"><span class="dt">{dt}</span>'
        f'<div class="nm">{nm}</div><div class="nt">{nota}</div>'
        f'<div class="nt" style="color:var(--tx2)">{obs}</div></div>'
        for dt, nm, cls, nota, obs in marcos
    )
    conteudo = (
        cabecalho(
            "Documentação do gerenciamento de projetos atualizada",
            "O que o professor pediu, e onde está atendido",
            "As duas sprints anteriores fecharam com nota máxima. Os dois ajustes apontados "
            "viraram trabalho nesta entrega.",
        )
        + f'<div class="trilho"><div class="marcos">{linha}</div></div>'
        + '<div class="stats" style="margin-top:auto">'
        + cartao_texto(
            "1",
            "Impacto com número, o pedido da Sprint 1",
            "Todo slide de modelo desta entrega traz a medição ao lado do baseline, e o "
            "bloco analítico tem 38 slides com o gráfico do notebook.",
            "good",
        )
        + cartao_texto(
            "2",
            "Gestão ágil explícita, o pedido da Sprint 2",
            "É o próximo slide: framework, quadro, divisão de trabalho e os marcos "
            "executados com data.",
            "good",
        )
        + cartao_texto(
            "3",
            "O que mudou no escopo desde maio",
            "Três das cinco ideias da arquitetura aprovada caíram no teste. A troca está "
            "declarada no slide anterior, com o número que derrubou cada uma.",
        )
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 6", classe="tl")


def s08_gestao_plano() -> str:
    """Marcos com data conferida em `context/status.md` e no histórico do repositório."""
    passos = [
        ("20 e 21/07", "Alvo e escopo de modelagem fechados com as três fontes oficiais."),
        ("29/07", "Verificações de robustez e dossiê de defesa para a banca."),
        ("03 e 04/08", "Modelo de risco medido. Notebooks <b>04, 05 e 06</b> escritos."),
        ("05/08", "Score de saúde por produto, o segundo diferencial."),
        ("11 a 14/08", "Auditoria dos números e reconstrução das seis abas."),
        ("17/08", "Auditoria visual: 41 capturas, <b>32 achados</b> corrigidos."),
    ]
    lista = "".join(
        f'<div class="ps"><span class="q">{q}</span><span class="o">{o}</span></div>'
        for q, o in passos
    )
    conteudo = (
        cabecalho(
            "Planejamento e gestão do projeto",
            "Uma sprint por entrega da FIAP, num quadro Trello",
            "Cinco colunas, do backlog ao concluído, com etiqueta por sprint, responsável e "
            "checklist de validação por entregável. O Scrum dá a cadência, o quadro mostra "
            "em que pé cada coisa está.",
        )
        + '<div class="duo">'
        + '<div class="passos"><div style="font-size:12px;font-weight:700;letter-spacing:1.5px;'
        'text-transform:uppercase;color:var(--tx2);padding-bottom:8px">'
        "Marcos executados na Sprint 3</div>"
        + lista
        + "</div>"
        + '<div style="width:430px;flex-shrink:0;display:flex;flex-direction:column;gap:12px">'
        + cartao_texto(
            "1",
            "Como o trabalho foi dividido",
            "Base e análise exploratória em dupla. Modelagem e aplicação com revisão "
            "cruzada. O deck e a validação contra o checklist da sprint saem com os três "
            "antes de fechar a entrega.",
        )
        + cartao_texto(
            "2",
            "Canal com a Locaweb",
            "O contato com Douglas Gouveia passa pelo Scrum Master do grupo. Da mentoria "
            "saíram duas hipóteses, e as duas entraram no backlog e foram testadas.",
        )
        + cartao_texto(
            "3",
            "Definição de pronto",
            "Um entregável só fecha quando passa pelo checklist da sprint e quando todo "
            "número afirmado tem célula executada que o produza.",
            "good",
        )
        + "</div></div>"
    )
    return _sl(conteudo, tag="Template · slide 7", classe="kb")


# ─────────────────────────────────────────────────────────────────────────────
# Arquitetura · template, slides 8 a 11
# ─────────────────────────────────────────────────────────────────────────────
def s09_arquitetura() -> str:
    def no(kicker: str, titulo: str, texto: str, acc: bool = False) -> str:
        return (
            f'<div class="nd{" acc" if acc else ""}"><div class="nk">{kicker}</div>'
            f'<div class="nh">{titulo}</div><p>{texto}</p></div>'
        )

    conteudo = (
        '<div class="row" style="display:flex;align-items:flex-end;'
        'justify-content:space-between;gap:40px"><div>'
        '<span class="eb">Arquitetura da solução · desenho</span>'
        '<h1 class="tt" style="font-size:36px">Do arquivo da Locaweb '
        "até a tela do turno</h1></div>"
        '<p style="font-size:15.5px;line-height:1.45;color:var(--tx);text-align:right;'
        'max-width:600px;flex-shrink:0;padding-bottom:3px">'
        "As três etapas do meio rodam fora do ar e gravam arquivo. <b>Só a última fica de "
        "pé em produção</b>, e ela não treina nada: lê 350 kB de Parquet e serve tela.</p>"
        "</div>"
        '<div class="flow">'
        + '<div class="lane"><div class="lk">1 · fonte</div><div class="nodes">'
        + no(
            "Entrada",
            "LW-DATASET.xlsx",
            "122.543 incidentes, 19 colunas, jan/2023 a dez/2025. Arquivo oficial da Locaweb.",
        )
        + no(
            "Fonte externa",
            "holidays BR",
            "Feriados nacionais. O dataset não traz a coluna, e a sazonalidade depende dela.",
        )
        + "</div></div>"
        + '<div class="lane"><div class="lk">2 · preparo</div><div class="nodes">'
        + no(
            "pandas",
            "Base compartilhada",
            "Tipagem, filtro oficial de elegibilidade e cinco colunas de calendário. "
            "Trava com asserts em 122.543 e 25.600.",
            True,
        )
        + "</div></div>"
        + '<div class="lane"><div class="lk">3 · modelos</div><div class="nodes">'
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
        + '<div class="lane"><div class="lk">4 · produto</div><div class="nodes">'
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
    return _sl(conteudo, tag="Template · slides 8 e 9", classe="dg")


def s10_arq_tec() -> str:
    tec = [
        ("pandas · openpyxl · pyarrow", "2.2.3 · 3.1.5 · 25.0",
         "Leem o Excel, tipam as colunas e gravam o Parquet que liga notebook e aplicação"),
        ("holidays", "0.97",
         "Feriados nacionais, que o dataset não traz e a sazonalidade exige"),
        ("Prophet · cmdstanpy", "1.3.0",
         "Preveem o volume por prioridade, com intervalo de 80%"),
        ("scikit-learn", "1.6.1",
         "Regressão logística do risco de OLA, o modelo entregue"),
        ("XGBoost", "3.0.2",
         "Baseline de comparação do risco. Não é o modelo de produção"),
        ("scipy · statsmodels", "1.18 · 0.14.6",
         "Correlações, testes e intervalos das verificações de robustez"),
        ("matplotlib · seaborn · plotly", "3.10 · 0.13 · 6.0",
         "Desenham as figuras dos notebooks e do deck"),
        ("Django", "6.1",
         "Serve as seis abas, uma URL por aba, com fragmento para o detalhe"),
        ("gunicorn · whitenoise", "23.0 · 6.9",
         "Servidor e arquivos estáticos dentro do contêiner"),
        ("Docker", "python:3.13-slim",
         "Empacota a entrega. Um build e a solução roda em qualquer provedor"),
    ]
    corpo_tab = "".join(
        f'<tr><td><b>{n}</b></td>'
        f'<td class="n" style="white-space:nowrap;color:var(--tx2)">{v}</td><td>{p}</td></tr>'
        for n, v, p in tec
    )
    conteudo = (
        cabecalho(
            "Descrição da arquitetura da solução",
            "O que cada tecnologia está fazendo ali",
            "Dez peças, todas com versão travada. A coluna da direita é o motivo de cada uma "
            "estar no projeto.",
        )
        + '<div class="tw" style="margin-top:20px;flex:1;min-height:0;overflow:hidden">'
        "<table><thead><tr><th>Tecnologia</th>"
        '<th style="text-align:right">Versão</th><th>Papel na solução</th></tr></thead>'
        f"<tbody>{corpo_tab}</tbody></table></div>"
    )
    return _sl(conteudo, tag="Template · slide 10")


def s11_arq_dados() -> str:
    conteudo = (
        cabecalho(
            "Descrição da arquitetura da solução · fontes e tratamento",
            "Um campo decide o que entra no KPI",
            "O dataset da Locaweb é a única fonte de incidente, e a biblioteca de feriados a "
            "única fonte externa. Entre as duas está a regra de elegibilidade, e errar nela "
            "contamina todo o resto.",
        )
        + '<div class="stats" style="margin-top:24px">'
        + cartao_num("Linhas lidas", "122.543", "Aba Dataset Geral, 19 colunas originais")
        + cartao_num("Valem para o KPI", "25.600", "Pelo campo oficial Entrou para KPI?", "focus")
        + cartao_num(
            "Se o filtro fosse só Incidente Pai", "107.416", "88% da base. É o erro clássico",
            "bad",
        )
        + "</div>"
        + '<div class="pts" style="margin-top:16px">'
        + cartao_texto(
            "1",
            "O campo oficial, e não a regra reescrita",
            "<b>Entrou para KPI?</b> já codifica as três condições juntas: prioridade 1, 2 ou "
            "3, campo Incidente Pai vazio e status diferente de Sem Intervenção. "
            "Reimplementar a regra criaria uma segunda verdade dentro da casa do cliente.",
        )
        + cartao_texto(
            "2",
            "Cinco colunas de calendário derivadas no preparo",
            "Dia, dia da semana, hora, ano e mês saem da data de abertura. O feriado vem da "
            "biblioteca. São as características que sustentam a sazonalidade do Prophet.",
        )
        + cartao_texto(
            "3",
            "Nenhum dado pessoal na base",
            "Varredura feita antes de publicar: zero e-mail, CPF, telefone ou endereço IP, e "
            "nenhuma coluna identifica pessoa. Os identificadores são de ativo e de equipe, e "
            "o campo de origem só tem Manual e Monitoramento.",
            "good",
        )
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 11")


# ─────────────────────────────────────────────────────────────────────────────
# A aplicação · template, slide 13
# ─────────────────────────────────────────────────────────────────────────────
def s12_div_telas() -> str:
    conteudo = (
        '<div class="lft">'
        + cabecalho(
            "Versão preliminar do MVP · a aplicação",
            "Seis abas, dez telas",
            "Tudo o que vem a seguir é print da aplicação Django rodando, com a saída real "
            "dos modelos. A ferramenta simula um relógio parado em <b>01/10/2025 às 15h</b> "
            "e só mostra o que existiria naquele instante.",
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


def s13_mockup() -> str:
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


def s14_dados() -> str:
    """Amostra real, lida de `data/interim/incidentes_kpi.parquet`."""
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
            "Um notebook produz a base que todos os outros leem. Ele trava o resultado com "
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
        + cartao_num("Preenchimento de Encerrado", "100%", "Conferido antes de acusar o modelo por queda", "good")
        + "</div>"
    )
    return _sl(conteudo, tag="Template · slide 13")


def s15_fecho() -> str:
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
        "solucao": s05_solucao(),
        "mudou": s06_mudou(),
        "gestao-documentacao": s07_gestao_doc(),
        "gestao-planejamento": s08_gestao_plano(),
        "arquitetura": s09_arquitetura(),
        "arquitetura-tecnologias": s10_arq_tec(),
        "arquitetura-dados": s11_arq_dados(),
        "divisoria-telas": s12_div_telas(),
        "mockup": s13_mockup(),
        "dados": s14_dados(),
        "fecho": s15_fecho(),
    }
    for nome, eb, tt, cap, tag in TELAS + MODAIS:
        proprios[nome] = slide_print(nome, eb, tt, cap, tag)
    return proprios


def ordem() -> list[str]:
    """A sequência final do deck, na ordem do template da FIAP."""
    return (
        [
            "capa",                      # template 1 e 2
            "equipe",
            "contexto",                  # template 3
            "problema",                  # template 4
            "solucao",                   # template 5
            "mudou",
            "gestao-documentacao",       # template 6
            "gestao-planejamento",       # template 7
            "arquitetura",               # template 8 e 9
            "arquitetura-tecnologias",   # template 10
            "arquitetura-dados",         # template 11
        ]
        + ANALISE                        # template 12 e 13: a evidência analítica
        + ["divisoria-telas"]            # template 13: a aplicação
        + [nome for nome, *_ in TELAS + MODAIS]
        + ["mockup", "dados", "fecho"]   # template 14
    )


def escreve_html() -> list[tuple[str, Path]]:
    """Grava os slides próprios e devolve a sequência inteira resolvida em caminho.

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
