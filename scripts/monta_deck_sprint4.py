# -*- coding: utf-8 -*-
"""Monta o deck da Sprint 4: HTML de cada slide, PNG de cada HTML e o .pptx final.

A ordem segue os **sete blocos** do template oficial da Sprint 4, e o rótulo de bloco
aparece no canto superior direito de cada slide novo, para o avaliador localizar o bloco
sem contar slides.

    1. Detalhes iniciais da equipe e do projeto      slides 01 a 03
    2. Compreendendo o desafio                       slides 04 a 08
    3. Objetivo atual do projeto                     slides 09 e 10
    4. Detalhes do projeto realizado                 slides 11 a 23
    5. Demonstração da solução                       slides 24 a 35
    6. Link do vídeo pitch                           slide  36
    7. Conclusão e próximos passos                   slides 37 a 42

Mesmo processo da Sprint 3: um PNG sangrado por slide, renderizado de HTML em 1600 × 900,
colado em página de 13,333 × 7,5 in.

Três fontes se juntam num arquivo só, e o builder é quase só um ordenador:

* **`prototipos/slides/mvp/abertura/`** empresta o contexto, o problema, as fontes de dados,
  a arquitetura, a stack e o código-fonte, pelo mapa `REUSO_ABERTURA`. Esses slides são lidos
  de onde estão, sem cópia: duplicar o HTML criaria uma segunda versão envelhecendo sozinha.
* **`prototipos/slides/mvp/deck/`** empresta quatro slides de análise e de indicador, pelo
  mapa `REUSO_DECK`. São eles que carregam as figuras exportadas do matplotlib dos notebooks.
* **`prototipos/slides/sprint4/`** recebe os slides que nascem aqui, escritos por este
  arquivo, mais a capa e a identificação da equipe, que vêm da Sprint 3 com o rótulo de
  sprint trocado por `deriva_da_sprint3()`.

Duas regras atravessam o arquivo inteiro. **Todo número aqui saiu de material existente e
rastreável**; a origem está anotada no comentário do slide. E métrica de avaliação de modelo
é assunto de slide, nunca de tela: a aplicação simula um relógio parado em 01/10/2025 15h,
então o que ela mostra não passa desse instante, enquanto MAE, cobertura, ROC AUC e backtest
são legítimos aqui, porque aqui o assunto é se o modelo funciona.

Uso, com a aplicação já capturada por `captura_telas.py`:

    .venv/Scripts/python scripts/monta_deck_sprint4.py
"""
from __future__ import annotations

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ABERTURA = RAIZ / "prototipos" / "slides" / "mvp" / "abertura"
DECK = RAIZ / "prototipos" / "slides" / "mvp" / "deck"
SAIDA = RAIZ / "prototipos" / "slides" / "sprint4"
SAIDA_PNG = SAIDA / "_png"
PRINTS = RAIZ / "sprints" / "sprint-3" / "prints"
PPTX = RAIZ / "sprints" / "EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx"

LARGURA = 1600
ALTURA = 900

# Endereço mostrado na moldura de navegador dos dez slides de captura. É o mesmo da Sprint 3,
# escolha do Igor para a tela aparecer publicada. Um lugar só para trocar quando a URL de
# produção estiver confirmada.
# `render.yaml` declara o serviço com o nome `cronos`, então o endereço publicado deve
# sair como `cronos.onrender.com`. Confirmar no primeiro deploy e ajustar aqui se o provedor
# tiver acrescentado sufixo: este é o único ponto do deck que escreve o endereço na moldura.
URL_APP = "cronos.onrender.com"
REPO = "github.com/igor-vignola/LocaWeb-Cronos"

# Os dois espaços que ficam para o Igor preencher. Ficam escritos assim no slide, de
# propósito: espaço em branco passa desapercebido, marcador não.
PLACEHOLDER_APP = "&lt;URL DA APLICAÇÃO&gt;"
PLACEHOLDER_VIDEO = "&lt;URL DO VÍDEO&gt;"

RODAPE_ESQ = "Cronos · Super Data Bros · 2TSCOA"
RODAPE_DIR = "Challenge FIAP 2026 com Locaweb"

FONTE = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    "family=JetBrains+Mono:wght@400;500;600&"
    'family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'
)
# A folha de estilo mora com os protótipos da Sprint 3 e é lida de lá, não copiada: é a
# mesma linguagem visual e ela não deve divergir entre as duas entregas.
BASE_CSS = '<link rel="stylesheet" href="../mvp/abertura/base.css">'

LOGO = (
    '<svg viewBox="0 0 28 28" fill="none">'
    '<path d="M6 22L12 14L16 17L22 8" stroke="{cor}" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="22" cy="8" r="3" fill="none" stroke="#3B82F6" stroke-width="1.5"/>'
    '<circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg>'
)


# ─────────────────────────────────────────────────────────────────────────────
# blocos de montagem
# ─────────────────────────────────────────────────────────────────────────────
def pagina(corpo: str, titulo: str, css: str = "") -> str:
    estilo = f"<style>{css}</style>" if css else ""
    return (
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
        f"<title>{titulo}</title>{FONTE}{BASE_CSS}{estilo}</head>"
        f"<body>{corpo}</body></html>"
    )


def topo(tag: str, escuro: bool = False) -> str:
    cor = "#000" if escuro else "#fff"
    return (
        f'<div class="hd"><span class="bi">{LOGO.format(cor=cor)}</span>'
        f'<span class="bn">Cronos</span>'
        f'<span class="bt">VEJA ANTES · AJA ANTES</span>'
        f'<span class="tag">{tag}</span></div>'
    )


def rodape() -> str:
    return f'<div class="ft"><span>{RODAPE_ESQ}</span><span>{RODAPE_DIR}</span></div>'


def slide(conteudo: str, *, tag: str, escuro: bool = False, classe: str = "") -> str:
    tema = "dark" if escuro else "light"
    return (
        f'<section class="slide {tema} {classe}">'
        '<div class="mesh"></div><div class="grid-bg"></div>'
        f"{topo(tag, escuro)}"
        f'<div class="body">{conteudo}</div>'
        f"{rodape()}</section>"
    )


def cabecalho(eyebrow: str, titulo: str, lead: str = "") -> str:
    html = f'<span class="eb">{eyebrow}</span><h1 class="tt">{titulo}</h1>'
    if lead:
        html += f'<p class="lead">{lead}</p>'
    return html


def cartao_num(rotulo: str, valor: str, legenda: str, tom: str = "") -> str:
    return (
        f'<div class="st {tom}"><span class="sk">{rotulo}</span>'
        f'<span class="sv num">{valor}</span><span class="sl">{legenda}</span></div>'
    )


def cartao_texto(marcador: str, titulo: str, texto: str, tom: str = "") -> str:
    cabeca = f'<div class="ph">{titulo}</div>' if titulo else ""
    return (
        f'<div class="pt {tom}"><span class="ci">{marcador}</span>'
        f'<div class="ptx">{cabeca}<p>{texto}</p></div></div>'
    )


def item_mapa(rotulo: str, titulo: str, texto: str) -> str:
    return (
        f'<div class="it"><span class="ex">{rotulo}</span>'
        f'<div class="an">{titulo}</div><p>{texto}</p></div>'
    )


def divisoria(numero: str, titulo: str, lead: str, pergunta: str, cartoes: str = "") -> str:
    """Slide escuro de abertura de bloco. A cor diz em que parte da entrega você está."""
    # `.dv .rgt` já é coluna com espaçamento próprio, então os cartões entram direto nele.
    direita = f'<div class="rgt">{cartoes}</div>' if cartoes else ""
    return slide(
        f'<div class="lft"><span class="eb">Bloco {numero}</span>'
        f'<h1 class="tt">{titulo}</h1>'
        f'<div class="lead">{lead}</div>'
        f'<div class="chip"><span>A pergunta deste bloco: <b>{pergunta}</b></span></div>'
        f"</div>{direita}",
        tag=f"Template · bloco {numero}",
        escuro=True,
        classe="dv",
    )


# ─────────────────────────────────────────────────────────────────────────────
# bloco 1 · detalhes iniciais da equipe e do projeto
# ─────────────────────────────────────────────────────────────────────────────
def deriva_da_sprint3(origem: Path) -> str:
    """Reaproveita capa e identificação da equipe trocando o rótulo de sprint.

    O arquivo vive um nível acima na árvore, então os caminhos relativos de folha de estilo
    e de imagem precisam encurtar um passo. Reescrever esses dois slides à mão duplicaria
    cem linhas de CSS que já estão certas.
    """
    html = origem.read_text(encoding="utf-8")
    trocas = [
        ('href="base.css"', 'href="../mvp/abertura/base.css"'),
        ("../../../../brand/", "../../../brand/"),
        ("../../../../sprints/", "../../../sprints/"),
        ("SPRINT 03 · MVP PRELIMINAR", "SPRINT 04 · SOLUÇÃO FINAL"),
        ("Sprint 03 · MVP preliminar", "Sprint 04 · Solução final"),
    ]
    for de, para in trocas:
        html = html.replace(de, para)
    if "SPRINT 04" not in html:
        raise ValueError(f"{origem.name}: o rótulo de sprint não foi encontrado para troca")
    return html


def s03_descricao() -> str:
    """Descrição resumida da solução final, em dois parágrafos.

    Números: 122.543 e 25.600 do `CLAUDE.md` e do `02_base_kpi`; 4,2 e 11,8 do rolling
    backtest em `docs/sprint-3-mvp.md`; 72% da curva de ganho do `04_risco_ola`.
    """
    css = """
.ds .txt{margin-top:22px;display:flex;flex-direction:column;gap:16px;max-width:1180px}
.ds .txt p{font-size:17.5px;line-height:1.62;color:var(--tx)}
.ds .txt p b{color:var(--head);font-weight:700}
.ds .stats{margin-top:36px}
"""
    p1 = (
        "O Cronos é um sistema de previsão de incidentes operacionais construído sobre o "
        "histórico da Locaweb. Ele lê os <b>122.543 incidentes</b> registrados entre janeiro "
        "de 2023 e dezembro de 2025, recorta pelo campo oficial da própria Locaweb os "
        "<b>25.600</b> que contam para o indicador de OLA, e devolve três respostas que hoje "
        "só existem na apuração de fim de ano: quantos incidentes entram nos próximos sete "
        "dias, qual incidente aberto tem maior probabilidade de estourar o prazo, e em que "
        "posição a meta anual de P2 e de P3 deve fechar."
    )
    p2 = (
        "São quatro modelos e uma aplicação. O Prophet prevê o volume diário de cada "
        "prioridade; uma regressão logística estima o risco de violação de cada incidente "
        "aberto; a projeção soma realizado, fila aberta e volume que ainda entra; e a nota de "
        "saúde ordena os produtos. A saída dos quatro é publicada em uma aplicação "
        "<b>Django de seis abas</b>, empacotada em contêiner Docker e sem dependência de "
        "provedor de nuvem, com um resumo escrito no início do dia que chega ao gestor sem "
        "que ele precise consultar nada."
    )
    cartoes = (
        cartao_num("Base analisada", "122.543", "incidentes em 19 colunas, de janeiro de 2023 a dezembro de 2025")
        + cartao_num("Recorte do indicador", "25.600", "elegíveis ao KPI pelo campo oficial <b>Entrou para KPI?</b>", "focus")
        + cartao_num("Erro da previsão", "4,2 · 11,8", "casos por dia no <b>P2</b> e no <b>P3</b>, de D+1 a D+7", "focus")
        + cartao_num("Fila de risco", "72%", "das violações caem nos 20% de maior risco estimado", "good")
    )
    corpo = (
        cabecalho("1 · Detalhes iniciais", "Solução final: descrição resumida")
        + f'<div class="txt"><p>{p1}</p><p>{p2}</p></div>'
        + f'<div class="stats">{cartoes}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 1 · A solução", classe="ds"), "Descrição resumida", css)


# ─────────────────────────────────────────────────────────────────────────────
# bloco 2 · compreendendo o desafio
# ─────────────────────────────────────────────────────────────────────────────
def s04_divisoria() -> str:
    cartoes = (
        cartao_num("Prazo de OLA", "4h · 12h", "tempo de resolução no <b>P2</b> e no <b>P3</b>")
        + cartao_num("Base do indicador", "25.600", "incidentes elegíveis, de 2023 a 2025")
        + cartao_num("Violações no período", "248", "0,97% dos incidentes elegíveis", "bad")
    )
    return pagina(
        divisoria(
            "02",
            "Compreendendo<br>o desafio",
            "O cenário em que o problema acontece, o problema nomeado, o efeito que ele "
            "produz no indicador e por que a hora de resolver é agora.",
            "o que exatamente falha hoje?",
            cartoes,
        ),
        "Divisória bloco 2",
    )


def s08_urgencia() -> str:
    """A urgência, com número.

    35 para 41 no acumulado de P2: `scripts/figuras_deck.py`, o gráfico do slide de problema.
    42 de 39 e 196 de 263: régua de meta de 2025 em `docs/sprint-3-mvp.md`, na faixa de 100%
    fixada pela auditoria de consistência de 19/08. ROC AUC 0,4693 contra 0,5063: seção de
    controle do `04_risco_ola`.
    """
    css = """
.ug .stats{margin-top:24px}
.ug .pts{margin-top:16px}
"""
    cartoes = (
        cartao_num("P2 · fechamento de 2025", "42 de 39", "violações contra o limite do ano. Passou, e a leitura só chegou na apuração de dezembro.", "bad")
        + cartao_num("P3 · fechamento de 2025", "196 de 263", "violações contra o limite do ano. Ficou dentro, e ninguém soube antes de dezembro que ficaria.", "focus")
        + cartao_num("P2 · o mês que virou o ano", "35 &rarr; 41", "acumulado de outubro para novembro. Seis casos em um mês atravessaram duas faixas da meta.", "warn")
    )
    itens = (
        cartao_texto(
            "1",
            "O resultado chega depois de acontecer",
            "A meta é anual e a apuração fecha em dezembro. Durante o ano a operação "
            "acompanha quantas violações já teve, sem estimativa de quantas ainda vai ter.",
            "warn",
        )
        + cartao_texto(
            "2",
            "A ordem de atendimento não é a ordem do estouro",
            "Ordenar a fila por prioridade, o comportamento padrão da ferramenta de "
            "atendimento, tem ROC AUC de <b>0,4693</b>, abaixo dos 0,5063 de uma fila "
            "sorteada.",
            "bad",
        )
    )
    corpo = (
        cabecalho(
            "2 · Compreendendo o desafio",
            "Por que resolver agora",
            "A meta anual muda de faixa em degrau, então um único mês ruim move o ano inteiro.",
        )
        + f'<div class="stats">{cartoes}</div>'
        + f'<div class="pts">{itens}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 2 · A urgência", classe="ug"), "A urgência", css)


# ─────────────────────────────────────────────────────────────────────────────
# bloco 3 · objetivo atual do projeto
# ─────────────────────────────────────────────────────────────────────────────
def s09_divisoria() -> str:
    return pagina(
        divisoria(
            "03",
            "Objetivo atual<br>do projeto",
            "Um objetivo geral e seis específicos. Cada específico traz o indicador que diz "
            "se ele foi cumprido, medido no material de avaliação dos modelos.",
            "o que este projeto se propôs a entregar?",
        ),
        "Divisória bloco 3",
    )


def s10_objetivo() -> str:
    """Objetivo geral e específicos.

    Cada indicador citado sai de célula executada: 4,2 e 11,8 do rolling backtest; 72% da
    curva de ganho; 43,5 e 208,0 da projeção do `06_projecao_kpi`; 15 produtos e 94% do
    `07_saude_produto`; 16 códigos e 439 recorrentes do `05_causas_recorrentes`.
    """
    css = """
.ob .geral{margin-top:20px;background:#fff;border:1px solid #BFDBFE;border-radius:18px;
  padding:24px 28px;box-shadow:0 20px 46px -32px rgba(37,99,235,.36);
  background:linear-gradient(160deg,#fff,#F4F8FF)}
.ob .geral .gk{font-size:11.5px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
  color:var(--accent)}
.ob .geral p{font-size:23px;font-weight:600;line-height:1.4;letter-spacing:-.4px;
  color:var(--head);margin-top:10px}
.ob .geral p b{font-weight:800;color:var(--accent)}
.ob .sk2{font-size:11.5px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
  color:var(--tx2);margin-top:22px}
.ob .grid{margin-top:12px;gap:12px}
.ob .it{padding:14px 18px;gap:6px}
.ob .it .an{font-size:17px}
.ob .it p{font-size:13.5px}
"""
    especificos = (
        item_mapa(
            "Específico 01",
            "<em>Prever</em> o volume diário",
            "Séries separadas de P2 e P3, de D+1 a D+7. Erro médio de <b>4,2</b> casos por "
            "dia no P2 e <b>11,8</b> no P3.",
        )
        + item_mapa(
            "Específico 02",
            "<em>Estimar</em> o risco de cada incidente",
            "Probabilidade de violação por incidente aberto, com a fila ordenada por ela. "
            "<b>72%</b> das violações nos 20% de maior risco.",
        )
        + item_mapa(
            "Específico 03",
            "<em>Projetar</em> o fechamento da meta",
            "Antes da apuração, nas duas prioridades. Projeta <b>43,5</b> no P2 e "
            "<b>208,0</b> no P3, contra 39 e 263 permitidas.",
        )
        + item_mapa(
            "Específico 04",
            "<em>Classificar</em> a saúde dos produtos",
            "Nota de 0 a 100 por produto, com o componente que mais penaliza cada um. "
            "<b>15</b> produtos, <b>94%</b> do volume elegível.",
        )
        + item_mapa(
            "Específico 05",
            "<em>Agrupar</em> as causas recorrentes",
            "Ordenadas por taxa de violação, não por volume. <b>16</b> códigos de fechamento "
            "e <b>439</b> problemas recorrentes catalogados.",
        )
        + item_mapa(
            "Específico 06",
            "<em>Publicar</em> a saída em aplicação web",
            "Django em imagem <b>python:3.13-slim</b>, seis abas com URL própria, sem "
            "provedor de nuvem amarrado.",
        )
    )
    corpo = (
        cabecalho("3 · Objetivo do projeto", "Objetivo geral e específicos")
        + '<div class="geral"><div class="gk">Objetivo geral</div>'
        "<p><b>Desenvolver</b> um sistema preditivo que antecipe a violação de OLA e a "
        "projeção da meta anual da Locaweb, entregando a leitura do ano antes da apuração de "
        "dezembro, nas prioridades <b>P2</b> e <b>P3</b>.</p></div>"
        '<div class="sk2">Objetivos específicos</div>'
        f'<div class="grid">{especificos}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 3 · O objetivo", classe="ob mp"), "Objetivo do projeto", css)


# ─────────────────────────────────────────────────────────────────────────────
# bloco 4 · detalhes do projeto realizado
# ─────────────────────────────────────────────────────────────────────────────
def s11_divisoria() -> str:
    cartoes = (
        cartao_num("Fontes de dados", "2", "a planilha da Locaweb e o calendário de feriados")
        + cartao_num("Ferramentas na stack", "12", "de Python à imagem Docker de entrega")
        + cartao_num("Notebooks executados", "7", "139 células de código e 3.012 linhas")
    )
    return pagina(
        divisoria(
            "04",
            "Detalhes do<br>projeto realizado",
            "A abordagem de trabalho, as hipóteses que caíram no teste, as fontes de dados, "
            "a arquitetura, a stack, o código e os indicadores medidos.",
            "como a solução foi construída, e com o que ela foi medida?",
            cartoes,
        ),
        "Divisória bloco 4",
    )


def s12_abordagem() -> str:
    """Abordagem incremental: quatro entregas, escopo fechado por sprint.

    Datas e situações do cronograma oficial da FIAP em `context/projeto.md`. Notas das
    Sprints 1 e 2 em `context/status.md`.
    """
    css = """
.ab .trilho{margin-top:26px}
.ab .pts{margin-top:20px}
.ab .pt p{font-size:14px}
"""
    marcos = (
        '<div class="mc ok"><div class="dt">27/04/2026</div><div class="nm">Ideação</div>'
        '<div class="nt">Problema, público e proposta. <b>Entregue, nota 5,00</b></div></div>'
        '<div class="mc ok"><div class="dt">24/05/2026</div><div class="nm">Arquitetura</div>'
        '<div class="nt">Desenho da solução, stack e protótipos. <b>Entregue, nota 5,00</b></div></div>'
        '<div class="mc ok"><div class="dt">23/08/2026</div><div class="nm">MVP preliminar</div>'
        '<div class="nt">Modelos treinados e aplicação em contêiner. <b>Entregue</b></div></div>'
        '<div class="mc now"><div class="dt">08/09/2026</div><div class="nm">Solução final</div>'
        '<div class="nt">Consolidação, vídeo de pitch e código no portal. <b>Esta entrega</b></div></div>'
    )
    itens = (
        cartao_texto(
            "1",
            "Escopo fechado por sprint",
            "Cada entrega tem um recorte próprio e é avaliada antes da seguinte. O que não "
            "cabe na sprint fica registrado, não fica pendente sem dono.",
        )
        + cartao_texto(
            "2",
            "Hipótese só entra no produto com teste no dado",
            "Toda ideia de funcionalidade passou por uma medição antes de virar tela. Quatro "
            "delas não sobreviveram, e o slide seguinte mostra o número que derrubou cada uma.",
        )
        + cartao_texto(
            "3",
            "Análise antes de aplicação",
            "Os sete notebooks analisam, treinam e gravam oito tabelas em Parquet. A "
            "aplicação Django apenas lê: nada é calculado em tempo de tela.",
        )
    )
    corpo = (
        cabecalho(
            "4 · Detalhes do projeto realizado",
            "A abordagem: incremental e dirigida por dado",
            "Quatro entregas nas datas da FIAP, com o escopo fechado a cada sprint.",
        )
        + f'<div class="trilho"><div class="marcos">{marcos}</div></div>'
        + f'<div class="pts">{itens}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 4 · A abordagem", classe="ab tl"), "A abordagem", css)


def s13_descartado() -> str:
    """As quatro hipóteses derrubadas, cada uma com o número que a derrubou.

    Cascata e acúmulo: `docs/sprint-3-mvp.md`, seção "Testado e descartado". DTW: mesma
    seção. Logística contra XGBoost: medição de 03/08/2026, corte out-of-time.
    """
    css = """
.ds4 .lst{margin-top:26px}
.ds4 .ln{grid-template-columns:250px 24px 210px 1fr;padding:17px 22px}
.ds4 .pq{font-size:15px}
"""
    linhas = (
        '<div class="ln"><span class="de">Detector de cascata</span><span class="ar">&rarr;</span>'
        '<span class="pa out">Fora do MVP</span>'
        '<span class="pq"><b>87%</b> das violações são de incidentes isolados, e a escalada '
        "observada ficou em 21% contra cerca de 60% esperados por acaso.</span></div>"
        '<div class="ln"><span class="de">Padrão de acúmulo</span><span class="ar">&rarr;</span>'
        '<span class="pa out">Fora do MVP</span>'
        '<span class="pq">Backlog diário contra violações em dias úteis: <b>r = -0,139</b>, '
        "levemente negativo, e o quartil de maior backlog tem menos violações por dia.</span></div>"
        '<div class="ln"><span class="de">Clusterização por DTW</span><span class="ar">&rarr;</span>'
        '<span class="pa out">Fora do MVP</span>'
        '<span class="pq">Silhueta de <b>0,13</b>, sem estrutura de grupos na série. O '
        "requisito de classificação ficou com o modelo de risco por incidente.</span></div>"
        '<div class="ln"><span class="de">XGBoost no risco de OLA</span><span class="ar">&rarr;</span>'
        '<span class="pa">Regressão logística</span>'
        '<span class="pq">Empate em ROC AUC (0,8679 contra <b>0,8693</b>) e vantagem de 17% '
        "para a logística em PR-AUC (0,2526 contra <b>0,2958</b>), que é a métrica de evento "
        "raro.</span></div>"
    )
    corpo = (
        cabecalho(
            "4 · Detalhes do projeto realizado",
            "Testado e descartado, com o número que decidiu",
            "Quatro caminhos entraram em teste antes de virar produto. O número decidiu "
            "contra os quatro.",
        )
        + f'<div class="lst">{linhas}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 4 · O que caiu", classe="ds4 dp"), "Testado e descartado", css)


def s23_indicadores() -> str:
    """Os indicadores medidos, em P2 e P3 lado a lado, mais os do modelo de risco.

    MAE e melhor baseline: tabela do rolling backtest em `docs/sprint-3-mvp.md`. Cobertura
    da banda: seção 4.10.1 do `03_previsao_volume`, reportada em faixa porque a banda vem de
    amostragem. Violações de 2025 e projeção: régua de meta e `06_projecao_kpi`. Métricas do
    risco: corte out-of-time de 03/08/2026, com 5.183 incidentes e 50 violações no teste.
    """
    css = """
.in .tw{margin-top:22px}
.in .tw tbody td{font-size:15.5px;padding:12px 16px}
.in .stats{margin-top:18px}
.in .st{padding:16px 20px}
.in .st .sv{font-size:31px;margin-top:6px}
.in .st .sl{font-size:13.5px}
"""
    tabela = (
        '<div class="tw"><table><thead><tr>'
        "<th>Indicador da previsão de volume</th><th>O que mede</th>"
        '<th class="n">P2 · Alta</th><th class="n">P3 · Média</th>'
        "</tr></thead><tbody>"
        "<tr><td><b>MAE de D+1 a D+7</b></td><td>erro médio da previsão, em casos por dia</td>"
        '<td class="n"><b>4,2</b></td><td class="n"><b>11,8</b></td></tr>'
        "<tr><td>Melhor baseline da série</td><td>referência ingênua da mesma série</td>"
        '<td class="n">4,9</td><td class="n">11,3</td></tr>'
        "<tr><td>Cobertura do intervalo de 80%</td>"
        "<td>dias do teste em que o real caiu dentro da banda</td>"
        '<td class="n">86% a 88%</td><td class="n">59% a 61%</td></tr>'
        "<tr><td>Violações de OLA em 2025</td><td>contagem contra o limite do ano</td>"
        '<td class="n"><b>42 de 39</b></td><td class="n"><b>196 de 263</b></td></tr>'
        "<tr><td>Projeção do fechamento</td>"
        "<td>realizado, mais fila aberta, mais volume que ainda entra</td>"
        '<td class="n">43,5</td><td class="n">208,0</td></tr>'
        "</tbody></table></div>"
    )
    cartoes = (
        cartao_num("Risco · discriminação", "0,8693", "ROC AUC da regressão logística, teste de outubro a dezembro", "focus")
        + cartao_num("Risco · evento raro", "0,2958", "PR-AUC, contra 0,2526 do XGBoost de comparação", "focus")
        + cartao_num("Risco · triagem", "72%", "das violações nos 20% de maior risco estimado", "good")
        + cartao_num("Risco · calibração", "48,1 de 50", "violações previstas contra observadas no período de teste", "good")
    )
    corpo = (
        cabecalho(
            "4 · Detalhes do projeto realizado",
            "Os indicadores usados para medir cada modelo",
            "As duas prioridades entram no indicador da Locaweb e cada uma tem meta própria, "
            "então toda medição é reportada nas duas.",
        )
        + tabela
        + f'<div class="stats">{cartoes}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 4 · Os indicadores", classe="in"), "Indicadores utilizados", css)


# ─────────────────────────────────────────────────────────────────────────────
# bloco 5 · demonstração da solução
# ─────────────────────────────────────────────────────────────────────────────
def s24_divisoria() -> str:
    cartoes = (
        cartao_num("Abas no ar", "6", "cada uma com URL própria, para enviar a alguém")
        + cartao_num("Capturas nesta seção", "10", "seis abas e quatro folhas de detalhe")
        + cartao_num("Artefato lido no arranque", "350 kB", "fila.parquet, painel.json e dias.json")
    )
    return pagina(
        divisoria(
            "05",
            "Demonstração<br>da solução",
            "A aplicação simula um relógio parado em 01/10/2025 às 15h: ela mostra o "
            "histórico até 30/09, o dia corrente até as 15h e a previsão para frente. É o que "
            "existiria na tela de quem opera naquele instante.",
            "o modelo cabe na rotina de quem opera?",
            cartoes,
        ),
        "Divisória bloco 5",
    )


def s25_link() -> str:
    """Link funcional da solução, exigência literal do bloco 5 do template.

    O endereço fica marcado: a publicação é feita fora deste builder e a URL entra depois.
    """
    css = """
.lk2 .caixa{margin-top:26px;background:#fff;border:1px solid var(--line);border-radius:18px;
  padding:30px 34px;box-shadow:0 20px 46px -32px rgba(15,23,42,.3)}
.lk2 .caixa .ck{font-size:11.5px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
  color:var(--tx2)}
.lk2 .url{font-family:var(--mono);font-size:34px;font-weight:600;letter-spacing:-.6px;
  color:var(--accent);margin-top:12px;word-break:break-all}
.lk2 .aviso{display:inline-flex;align-items:center;gap:8px;margin-top:16px;font-size:13.5px;
  font-weight:700;color:var(--warn);background:var(--warn-l);border-radius:999px;
  padding:7px 15px}
.lk2 .duo{display:flex;gap:18px;margin-top:34px}
.lk2 .cx{flex:1;background:#fff;border:1px solid var(--line);border-radius:16px;
  padding:20px 24px;box-shadow:0 16px 38px -30px rgba(15,23,42,.28)}
.lk2 .cx .ck{font-size:11.5px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
  color:var(--tx2)}
.lk2 .cx .cv{font-family:var(--mono);font-size:17px;font-weight:600;color:var(--head);
  margin-top:10px;word-break:break-all}
.lk2 .cx code{display:block;font-family:var(--mono);font-size:14px;color:var(--head);
  background:#F1F5FB;border:1px solid var(--line);border-radius:9px;padding:9px 13px;
  margin-top:8px}
.lk2 .cx p{font-size:13.5px;line-height:1.45;color:var(--tx);margin-top:10px}
"""
    corpo = (
        cabecalho(
            "5 · Demonstração da solução",
            "Link funcional da aplicação",
            "A aplicação sobe em contêiner e não depende de provedor de nuvem: a mesma "
            "imagem roda no provedor de publicação e na infraestrutura da própria Locaweb.",
        )
        + '<div class="caixa"><div class="ck">Endereço da aplicação</div>'
        f'<div class="url">https://{PLACEHOLDER_APP}</div>'
        '<span class="aviso">Espaço reservado: preencher com a URL publicada antes do envio</span>'
        "</div>"
        '<div class="duo">'
        f'<div class="cx"><div class="ck">Repositório público</div><div class="cv">{REPO}</div>'
        "<p>Sete notebooks executados, os scripts que aplicam os modelos e a aplicação "
        "Django, com o Dockerfile.</p></div>"
        '<div class="cx"><div class="ck">Para rodar na própria infraestrutura</div>'
        "<code>docker build -f webapp/Dockerfile -t cronos .</code>"
        "<code>docker run --rm -p 8000:8000 cronos</code>"
        "<p>A imagem carrega Django, pandas e pyarrow. Os modelos ficam nos notebooks, que "
        "gravam Parquet.</p></div>"
        "</div>"
    )
    return pagina(slide(corpo, tag="Bloco 5 · O link", classe="lk2"), "Link da aplicação", css)


# (arquivo do print, sobrancelha, título, legenda, quem usa, como usa no dia a dia)
#
# A legenda vem da Sprint 3, onde cada linha foi conferida contra a tela. O que é novo aqui
# são as duas últimas colunas: o bloco 5 do template pede explicitamente "quem usará, como
# será utilizado no dia a dia e que valor essa solução entrega na prática".
TELAS = [
    (
        "01-panorama", "Aba Panorama", "O dia em uma tela",
        "O previsto para a hora contra o registrado, em <b>P3 e P2</b>. Abaixo, os casos de "
        "maior risco agora e as duas metas do ano.",
        "A coordenação de operações, na primeira meia hora do dia.",
        "Compara o que já entrou com o que o modelo esperava para a hora e decide se o dia "
        "pede reforço. É a única tela que responde as duas perguntas juntas.",
    ),
    (
        "07-modal-briefing", "Panorama · resumo automático", "O resumo do início do dia",
        "Abre sozinho na entrada da ferramenta, com ontem, hoje e onde agir. É gerado da "
        "saída dos modelos: <b>o Cronos empurra o insight, não espera pergunta</b>.",
        "O gestor de operações, antes da primeira reunião.",
        "Lê o resumo já escrito e leva a leitura pronta para a reunião. Não precisa abrir "
        "aba, filtrar período nem pedir relatório a ninguém.",
    ),
    (
        "02-previsao", "Aba Previsão", "Quanto entra nos próximos dias",
        "Saída do Prophet. Trinta dias medidos emendados em duas semanas previstas, cada dia "
        "como <b>intervalo</b>, e não como número único.",
        "Quem dimensiona a equipe da semana.",
        "Escala pelo topo do intervalo, não pela média, e vê a diferença entre P2 e P3 antes "
        "de distribuir gente. A largura do intervalo é a medida da dúvida do modelo.",
    ),
    (
        "03-projecao", "Aba Projeção", "Onde o ano fecha",
        "As violações acumuladas somadas ao risco da fila aberta e ao volume que ainda entra. "
        "<b>P3 projeta 208 e fica dentro do limite; P2 projeta 43 e passa de 39</b>.",
        "O gerente responsável pelo indicador anual.",
        "Acompanha, a cada mês, se o ano fecha dentro do limite nas duas prioridades. É a "
        "informação que hoje só aparece na apuração de dezembro.",
    ),
    (
        "10-modal-meta", "Projeção · régua da meta", "Como a meta é medida",
        "Os seis degraus da meta anual, direto do dicionário de dados da Locaweb. <b>O Cronos "
        "não define a régua</b>: ele diz em que degrau o ano está e em qual deve terminar.",
        "O mesmo gerente, quando precisa justificar a leitura.",
        "Confere degrau por degrau de onde saiu o veredito da tela anterior. A régua é a "
        "oficial da Locaweb, e a folha existe para que a conta não fique numa caixa fechada.",
    ),
    (
        "04-fila", "Aba Fila", "Em qual caso olhar primeiro",
        "Os 49 casos abertos às 15h, ordenados do maior risco para o menor pela regressão "
        "logística, cada um com o <b>fator que mais pesa</b> e o ativo envolvido.",
        "O analista de operações que está com a fila na mão.",
        "Percorre de cima para baixo até o limite de casos que consegue revisar no dia. "
        "Percorrendo os 50 primeiros, encontra 15 das violações do período em vez de meia.",
    ),
    (
        "08-modal-escore", "Fila · explicabilidade", "Por que este caso e não outro",
        "A decomposição da pontuação: cada sinal entra como <b>peso vezes desvio da "
        "média</b>, e a soma reconstrói o valor exato. Modelo linear é explicável por "
        "construção.",
        "O mesmo analista, antes de agir sobre o caso.",
        "Lê quais sinais empurraram o incidente para o topo e decide o que fazer com essa "
        "informação. Sem isso, a ordenação seria uma instrução sem argumento.",
    ),
    (
        "05-saude", "Aba Saúde", "Que produto está pior",
        "Nota de 0 a 100 nos 15 produtos, com o componente que mais penaliza cada um e as "
        "colunas de <b>P3 e P2 separadas</b>.",
        "A liderança de produto, na revisão semanal.",
        "Compara os 15 produtos numa escala só e leva o pior da lista para a pauta. As duas "
        "prioridades aparecem em colunas próprias, porque cada uma tem meta própria.",
    ),
    (
        "09-modal-produto", "Saúde · detalhe do produto", "O que forma a nota",
        "Os cinco componentes da nota e quanto cada um pesa, com o histórico do produto. É o "
        "que separa <b>viola muito</b> de <b>vai começar a violar</b>.",
        "Quem responde pelo produto apontado.",
        "Vê qual dos cinco componentes puxa a nota para baixo e onde investir esforço. A nota "
        "sozinha diz que há problema; a decomposição diz qual é.",
    ),
    (
        "06-causas", "Aba Causas", "O que compensa prevenir",
        "Códigos de fechamento ordenados por <b>taxa de violação, não por volume</b>: é assim "
        "que aparece a causa pequena que viola muito.",
        "Quem decide ação preventiva e projeto de melhoria.",
        "Escolhe onde atacar a causa raiz. A ordenação por volume levaria à falha mais "
        "frequente, que tem taxa de violação abaixo da média da base.",
    ),
]

MODELO_TELA = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>{titulo}</title>
{fonte}
<link rel="stylesheet" href="../mvp/abertura/base.css">
<style>
.pk .body{{padding:0;flex-direction:row;align-items:center;gap:24px}}
.pk .lado{{width:318px;flex-shrink:0;padding-left:26px}}
.pk .marca{{display:flex;align-items:center;gap:9px}}
.pk .marca .bi2{{width:30px;height:30px;border-radius:8px;background:var(--ink);
  display:flex;align-items:center;justify-content:center}}
.pk .marca .bi2 svg{{width:17px;height:17px}}
.pk .marca span{{font-size:16px;font-weight:800;letter-spacing:-.3px;color:#000}}
.pk .kk{{font-size:11.5px;font-weight:700;letter-spacing:2.4px;text-transform:uppercase;
  color:var(--accent);margin-top:30px}}
.pk h1{{font-size:29px;font-weight:800;letter-spacing:-1.05px;line-height:1.1;
  color:var(--head);margin-top:9px}}
.pk .cap2{{font-size:14px;line-height:1.55;color:var(--tx);margin-top:15px}}
.pk .cap2 b{{color:var(--head);font-weight:700}}
/* o bloco de uso real: exigência literal do bloco 5 do template. Fica sempre no mesmo
   lugar em todas as dez capturas, para o leitor achar sem procurar. */
.pk .uso{{margin-top:20px;padding-top:16px;border-top:1px solid var(--line)}}
.pk .uk{{font-size:10.5px;font-weight:700;letter-spacing:1.7px;text-transform:uppercase;
  color:var(--accent)}}
.pk .uso p{{font-size:13px;line-height:1.5;color:var(--tx);margin-top:5px}}
.pk .uso .uk+p+.uk{{margin-top:13px}}
.pk .uso p b{{color:var(--head);font-weight:700}}
.pk .pil{{display:inline-block;margin-top:22px;font-size:12px;font-weight:600;
  padding:7px 15px;border-radius:999px;background:#fff;border:1px solid var(--line);
  color:var(--accent);box-shadow:0 4px 14px -8px rgba(37,99,235,.3)}}

.pk .win{{width:1206px;height:826px;flex-shrink:0;border-radius:14px;overflow:hidden;
  background:#fff;border:1px solid rgba(15,23,42,.14);
  box-shadow:0 -1px 0 rgba(255,255,255,.9) inset,
             0 54px 110px -44px rgba(15,23,42,.44),
             0 18px 40px -22px rgba(15,23,42,.22)}}
.pk .tabs{{height:32px;background:#D9E0EA;display:flex;align-items:flex-end;gap:9px;
  padding:0 14px}}
.pk .dots{{display:flex;gap:8px;flex-shrink:0;padding-bottom:9px}}
.pk .dots i{{width:11px;height:11px;border-radius:50%}}
.pk .dots i:nth-child(1){{background:#F2645A}}
.pk .dots i:nth-child(2){{background:#F4BE4F}}
.pk .dots i:nth-child(3){{background:#5FC466}}
.pk .tab{{height:26px;background:#fff;border-radius:9px 9px 0 0;display:flex;
  align-items:center;gap:9px;padding:0 13px;font-size:12.5px;font-weight:600;color:#33415A;
  max-width:290px;white-space:nowrap}}
.pk .tab .fav{{width:13px;height:13px;border-radius:4px;background:var(--ink);flex-shrink:0;
  display:flex;align-items:center;justify-content:center}}
.pk .tab .fav svg{{width:9px;height:9px}}
.pk .tab .x{{color:#9AA6B6;font-size:13px;margin-left:2px}}
.pk .plus{{color:#7E8B9E;font-size:15px;padding-bottom:6px}}
.pk .bar2{{height:40px;background:#fff;border-bottom:1px solid #E3E9F1;display:flex;
  align-items:center;gap:16px;padding:0 16px}}
.pk .nav{{display:flex;align-items:center;gap:15px;color:#7F8DA1;flex-shrink:0}}
.pk .nav svg{{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.9;
  stroke-linecap:round;stroke-linejoin:round}}
.pk .nav svg.off{{color:#C2CBD8}}
.pk .addr{{flex:1;max-width:720px;margin:0 auto;height:26px;background:#F1F4F8;
  border-radius:999px;display:flex;align-items:center;gap:9px;padding:0 15px;font-size:13px;
  color:#5C6B80;overflow:hidden;white-space:nowrap}}
.pk .addr svg{{width:13px;height:13px;stroke:#7C8AA0;fill:none;stroke-width:1.8;
  flex-shrink:0}}
.pk .addr .sch{{color:#9DAABB}}
.pk .addr b{{color:#1F2937;font-weight:600}}
.pk .rgt{{display:flex;align-items:center;gap:14px;color:#7F8DA1;flex-shrink:0}}
.pk .rgt svg{{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.9;
  stroke-linecap:round;stroke-linejoin:round}}
.pk .rgt .av{{width:20px;height:20px;border-radius:50%;background:#E3E9F1;
  border:1px solid #D3DBE6}}
.pk .win img{{display:block;width:100%}}
.pk .ft{{left:26px;right:26px;bottom:9px}}
</style></head><body>
<section class="slide light pk">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="body">
    <div class="lado">
      <div class="marca">
        <span class="bi2"><svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" r="3" fill="none" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg></span>
        <span>Cronos</span>
      </div>
      <div class="kk">{eyebrow}</div>
      <h1>{titulo}</h1>
      <p class="cap2">{legenda}</p>
      <div class="uso">
        <div class="uk">Quem usa</div>
        <p>{quem}</p>
        <div class="uk">No dia a dia</div>
        <p>{como}</p>
      </div>
      <span class="pil">A aplicação · {pos} de {total}</span>
    </div>

    <div class="win">
      <div class="tabs">
        <span class="dots"><i></i><i></i><i></i></span>
        <span class="tab">
          <span class="fav"><svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          Cronos · Painel operacional<span class="x">&times;</span>
        </span>
        <span class="plus">+</span>
      </div>
      <div class="bar2">
        <span class="nav">
          <svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>
          <svg class="off" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>
          <svg viewBox="0 0 24 24"><path d="M20.5 12a8.5 8.5 0 1 1-2.6-6.1"/><path d="M20.5 4.5V10h-5.5"/></svg>
        </span>
        <span class="addr">
          <svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8.5 11V8a3.5 3.5 0 0 1 7 0v3"/></svg>
          <span class="sch">https://</span><b>{url}</b><span class="sch">/</span>
        </span>
        <span class="rgt">
          <svg viewBox="0 0 24 24"><path d="M12 4l2.4 4.9 5.4.8-3.9 3.8.9 5.4-4.8-2.5-4.8 2.5.9-5.4L4.2 9.7l5.4-.8z"/></svg>
          <span class="av"></span>
        </span>
      </div>
      <img src="../../../sprints/sprint-3/prints/{arquivo}.png" alt="{eyebrow}">
    </div>
  </div>
  <div class="ft"><span>{rod_esq}</span><span>{rod_dir}</span></div>
</section>
</body></html>
"""


def slides_das_telas() -> dict[str, str]:
    """Os dez slides de captura, um por print da aplicação."""
    total = len(TELAS)
    saida: dict[str, str] = {}
    for pos, (arquivo, eyebrow, titulo, legenda, quem, como) in enumerate(TELAS, 1):
        saida[f"tela-{pos:02d}-{arquivo}"] = MODELO_TELA.format(
            fonte=FONTE,
            arquivo=arquivo,
            eyebrow=eyebrow,
            titulo=titulo,
            legenda=legenda,
            quem=quem,
            como=como,
            pos=pos,
            total=total,
            url=URL_APP,
            rod_esq=RODAPE_ESQ,
            rod_dir=RODAPE_DIR,
        )
    return saida


# ─────────────────────────────────────────────────────────────────────────────
# bloco 6 · link do vídeo pitch
# ─────────────────────────────────────────────────────────────────────────────
def s36_video() -> str:
    """Bloco 6 do template. Uma exigência, um slide, e o espaço marcado."""
    css = """
.vd .body{padding:30px 64px 44px;justify-content:flex-start}
.vd .caixa{margin-top:24px;background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.14);border-radius:20px;padding:34px 38px}
.vd .caixa .ck{font-size:11.5px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
  color:#8B96A8}
.vd .url{font-family:var(--mono);font-size:36px;font-weight:600;letter-spacing:-.7px;
  color:#93C5FD;margin-top:13px;word-break:break-all}
.vd .aviso{display:inline-flex;align-items:center;gap:8px;margin-top:18px;font-size:13.5px;
  font-weight:700;color:#F0B767;background:rgba(180,120,10,.22);border-radius:999px;
  padding:8px 16px}
.vd .cards{display:flex;gap:18px;margin-top:34px}
.vd .fcd{flex:1;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);
  border-radius:16px;padding:20px 22px}
.vd .fcd .fk{font-size:11px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
  color:#8B96A8}
.vd .fcd .fv{font-size:22px;font-weight:800;letter-spacing:-.6px;color:#fff;margin-top:8px}
.vd .fcd p{font-size:14px;line-height:1.45;color:#98A2B3;margin-top:9px}
"""
    corpo = (
        cabecalho(
            "6 · Link do vídeo pitch",
            "Vídeo pitch",
            "Cinco minutos em formato hands on, com a aplicação em funcionamento. Hospedado "
            "em nuvem com acesso público, como o enunciado recomenda.",
        )
        + '<div class="caixa"><div class="ck">Endereço do vídeo</div>'
        f'<div class="url">{PLACEHOLDER_VIDEO}</div>'
        '<span class="aviso">Espaço reservado: preencher com a URL do vídeo antes do envio</span>'
        "</div>"
        '<div class="cards">'
        '<div class="fcd"><div class="fk">Duração</div><div class="fv">5 minutos</div>'
        "<p>O limite do enunciado. O roteiro foi escrito e medido em ritmo de leitura calma.</p></div>"
        '<div class="fcd"><div class="fk">Formato</div><div class="fv">Hands on</div>'
        "<p>A aplicação navegada ao vivo, com as seis abas e as folhas de detalhe.</p></div>"
        '<div class="fcd"><div class="fk">Acesso</div><div class="fv">Público</div>'
        "<p>Fora do portal, porque o arquivo final não caberia no envio direto.</p></div>"
        "</div>"
    )
    return pagina(slide(corpo, tag="Bloco 6 · O vídeo", escuro=True, classe="vd"), "Vídeo pitch", css)


# ─────────────────────────────────────────────────────────────────────────────
# bloco 7 · conclusão e próximos passos
# ─────────────────────────────────────────────────────────────────────────────
def s37_divisoria() -> str:
    return pagina(
        divisoria(
            "07",
            "Conclusão e<br>próximos passos",
            "A síntese do que foi entregue, o que a equipe aprendeu no caminho, os limites "
            "que ficaram de pé e para onde a solução cresce.",
            "o que ficou pronto, e o que ainda não está?",
        ),
        "Divisória bloco 7",
    )


def s38_sintese() -> str:
    """Síntese dos resultados.

    Cada número já apareceu no bloco 4 e sai da mesma célula. 139 células, 3.012 linhas, 30
    scripts e 8 tabelas: `scripts/inventario_codigo.py`. 350 kB: os três artefatos que a
    aplicação lê no arranque.
    """
    css = """
.sn .stats{margin-top:24px}
.sn .pts{margin-top:16px}
"""
    cartoes = (
        cartao_num("Previsão de volume", "4,2 · 11,8", "erro médio por dia no <b>P2</b> e no <b>P3</b>. No P2, ganho de 15% sobre o melhor baseline; no P3, empate técnico.", "focus")
        + cartao_num("Risco por incidente", "72%", "das violações nos 20% de maior risco, com 48,1 previstas onde houve 50.", "good")
        + cartao_num("Projeção da meta", "7 de 10", "acertos da situação da meta nas duas prioridades, por data de corte.", "focus")
        + cartao_num("Aplicação", "6 abas", "em contêiner Docker, lendo 350 kB de artefato e sem cálculo em tempo de tela.", "good")
    )
    itens = (
        cartao_texto(
            "1",
            "Quatro modelos alimentam a mesma aplicação",
            "Previsão de volume por prioridade, risco de violação por incidente, projeção do "
            "fechamento anual e nota de saúde por produto. Os quatro leem a mesma base "
            "recortada pelo campo oficial de elegibilidade.",
        )
        + cartao_texto(
            "2",
            "Todo número da tela vem de célula executada",
            "Sete notebooks, 139 células de código e 3.012 linhas produzem a análise, treinam "
            "os modelos e gravam oito tabelas em Parquet. Trinta scripts aplicam o resultado. "
            "A aplicação apenas lê.",
        )
    )
    corpo = (
        cabecalho(
            "7 · Conclusão",
            "Síntese dos resultados",
            "O que existe hoje, medido nos protocolos descritos no bloco anterior.",
        )
        + f'<div class="stats">{cartoes}</div>'
        + f'<div class="pts">{itens}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 7 · Os resultados", classe="sn"), "Síntese dos resultados", css)


def s39_aprendizados() -> str:
    """Aprendizados-chave.

    R² de 0,025: teste de 29/07/2026 em dias úteis de 2025. ROC AUC e PR-AUC: corte
    out-of-time de 03/08/2026. 25.600 contra 107.416: regra 4 do `CLAUDE.md`, confirmada
    pela Locaweb.
    """
    css = """
.ap .pts{margin-top:26px;gap:12px}
.ap .pt{padding:16px 20px}
.ap .pt p{font-size:14.5px}
"""
    itens = (
        cartao_texto(
            "1",
            "Testar a hipótese óbvia antes de construir sobre ela",
            "A suposição de que dia movimentado quebra mais OLA caiu na medição: o volume "
            "diário explica <b>2,5%</b> da variação de violações, com R² de 0,025 em dias "
            "úteis. Publicar isso reduziu o alcance prometido e definiu o papel de cada "
            "modelo.",
        )
        + cartao_texto(
            "2",
            "Modelo interpretável não foi concessão de desempenho",
            "A regressão logística empatou com o XGBoost em ROC AUC (<b>0,8693</b> contra "
            "0,8679), venceu em PR-AUC (<b>0,2958</b> contra 0,2526) e manteve a calibração. "
            "A explicabilidade saiu dos próprios pesos, sem ferramenta intermediária.",
            "good",
        )
        + cartao_texto(
            "3",
            "O campo oficial do cliente vale mais que a regra reescrita",
            "Filtrar por <b>Entrou para KPI?</b> devolve 25.600 elegíveis. Reimplementar a "
            "regra apenas pelo <b>Incidente Pai</b> vazio devolveria 107.416, que é 88% da "
            "base, e todo número seguinte estaria errado.",
        )
        + cartao_texto(
            "4",
            "Resultado negativo também é entrega",
            "Cascata, acúmulo, clusterização por DTW e realocação de equipe foram testados e "
            "descartados com número. O registro do descarte impediu que esses caminhos "
            "fossem reabertos, e é o que sustenta o escopo atual.",
            "warn",
        )
    )
    corpo = (
        cabecalho(
            "7 · Conclusão",
            "Aprendizados-chave",
            "Quatro aprendizados que mudaram decisões de projeto.",
        )
        + f'<div class="pts">{itens}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 7 · Os aprendizados", classe="ap"), "Aprendizados", css)


def s40_limitacoes() -> str:
    """Limitações enfrentadas, cada uma com o número que a mede.

    Cobertura em faixa: seção 4.10.1 do `03_previsao_volume`, porque a banda vem de
    amostragem e a casa decimal não é reprodutível. Cauda do rótulo e faixa de risco alto:
    `context/status.md`. Campos de causa: notebook 05. 98% em 2025: escopo temporal do
    `docs/sprint-3-mvp.md`.
    """
    css = """
.li .grid{margin-top:24px;gap:13px}
.li .it{padding:16px 20px;gap:7px}
.li .it .an{font-size:17.5px}
.li .it p{font-size:14px}
"""
    itens = (
        item_mapa(
            "Limite 01 · previsão",
            "O intervalo do <em>P3</em> subestima a incerteza",
            "A banda de 80% cobriu entre <b>59% e 61%</b> dos dias do período de teste no P3, "
            "contra 86% a 88% no P2. A causa é a queda de nível de novembro e dezembro, que o "
            "treino de janeiro a setembro não podia prever.",
        )
        + item_mapa(
            "Limite 02 · dado",
            "O rótulo só existe depois do fechamento",
            "O campo <b>Entrou para KPI?</b> é preenchido quando o incidente encerra, então "
            "em operação real os últimos dias da série ficam incompletos. O backtest é "
            "otimista nessa medida frente à produção.",
        )
        + item_mapa(
            "Limite 03 · histórico",
            "Um ano de dado denso, não três",
            "<b>98%</b> dos 25.600 elegíveis estão em 2025. Há dado para aprender o padrão de "
            "semana e de feriado, não o padrão de ano, então a sazonalidade anual do Prophet "
            "ficou desligada de propósito.",
        )
        + item_mapa(
            "Limite 04 · risco",
            "A faixa de risco alto não foi calibrada",
            "O desvio de calibração se concentra em <b>31 incidentes</b>. Ajustar sobre esse "
            "volume seria ajustar ruído, então a faixa ficou como está e o limite ficou "
            "declarado em vez de escondido.",
        )
        + item_mapa(
            "Limite 05 · causas",
            "Os campos de causa vêm mascarados",
            "<b>Categoria</b> e <b>Subcategoria</b> chegam anonimizadas, como cat71 e cat103, "
            "e <b>Solução</b> está sem registro em 75,7% dos casos. O agrupamento se sustenta "
            "no código de fechamento, que tem 16 valores legíveis.",
        )
        + item_mapa(
            "Limite 06 · valor",
            "Não há número financeiro no dataset",
            "O dado não traz custo por violação nem horas de retrabalho. O benefício está "
            "medido em violações e em posição na meta anual, nunca em moeda, e assim ficou "
            "declarado em todo o material.",
        )
    )
    corpo = (
        cabecalho(
            "7 · Conclusão",
            "Limitações enfrentadas",
            "Seis limites que continuam de pé, medidos e declarados no material.",
        )
        + f'<div class="grid">{itens}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 7 · Os limites", classe="li mp"), "Limitações", css)


def s41_proximos() -> str:
    """Próximos passos. Cada um responde a um limite declarado no slide anterior."""
    css = """
.px .pts{margin-top:26px;gap:13px}
.px .pt{padding:17px 21px}
.px .pt p{font-size:14.5px}
"""
    itens = (
        cartao_texto(
            "1",
            "Ler direto da base interna da Locaweb",
            "Hoje a entrada é o arquivo <b>LW-DATASET.xlsx</b>. O desenho da arquitetura já "
            "prevê a leitura direta da base operacional, que é o nó tracejado do fluxograma, "
            "e é o que troca uma carga manual por dado quase em tempo real.",
        )
        + cartao_texto(
            "2",
            "Reajustar os modelos em janela consolidada",
            "Reajuste semanal descartando os últimos dias. Resolve a cauda incompleta do "
            "rótulo e deve corrigir a cobertura do intervalo, hoje calibrada no <b>P2</b> e "
            "estreita no <b>P3</b>. É o modo de operação real, e o backtest já foi "
            "construído nesse formato.",
        )
        + cartao_texto(
            "3",
            "Religar a sazonalidade anual quando o histórico permitir",
            "Com dois ou três anos de registro denso, o padrão de ano passa a ser aprendível "
            "e pode ser testado contra a configuração atual pelo mesmo protocolo de backtest.",
        )
        + cartao_texto(
            "4",
            "Gerar o texto do resumo diário pela Claude API",
            "Hoje o resumo do início do dia é montado da saída dos modelos por regra fixa. A "
            "geração de linguagem entra nos bastidores, sem interface de conversa com quem "
            "opera.",
        )
    )
    corpo = (
        cabecalho(
            "7 · Conclusão",
            "Próximos passos e evoluções possíveis",
            "Quatro frentes, e cada uma responde a um dos limites do slide anterior.",
        )
        + f'<div class="pts">{itens}</div>'
    )
    return pagina(slide(corpo, tag="Bloco 7 · O que vem", classe="px"), "Próximos passos", css)


def s42_fecho() -> str:
    css = """
.fc2 .body{padding:34px 64px 44px;justify-content:center}
.fc2 .big{font-size:132px;font-weight:900;letter-spacing:-6px;color:#fff;line-height:1;
  margin-top:10px}
.fc2 .nomes{font-size:20px;color:#98A2B3;margin-top:18px;line-height:1.6}
.fc2 .nomes b{color:#fff;font-weight:700}
.fc2 .cards{display:flex;gap:18px;margin-top:38px}
.fc2 .fcd{flex:1;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);
  border-radius:16px;padding:20px 22px}
.fc2 .fcd .fk{font-size:11px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
  color:#8B96A8}
.fc2 .fcd .fv{font-family:var(--mono);font-size:16px;font-weight:600;color:#fff;
  margin-top:9px;word-break:break-all}
.fc2 .fcd p{font-size:13.5px;line-height:1.45;color:#98A2B3;margin-top:9px}
"""
    corpo = (
        '<span class="eb">Cronos · Veja antes. Aja antes.</span>'
        '<div class="big">Obrigado</div>'
        '<div class="nomes"><b>Super Data Bros</b> · Turma 2TSCOA<br>'
        "Ana Beatriz Costa de Oliveira · Hygor Abrantes · Igor Vignola<br>"
        "Mentor Locaweb: Douglas Gouveia, Gerente Executivo de Operações</div>"
        '<div class="cards">'
        f'<div class="fcd"><div class="fk">Aplicação</div><div class="fv">{PLACEHOLDER_APP}</div>'
        "<p>Seis abas em contêiner Docker, sem provedor de nuvem amarrado.</p></div>"
        f'<div class="fcd"><div class="fk">Vídeo pitch</div><div class="fv">{PLACEHOLDER_VIDEO}</div>'
        "<p>Cinco minutos em formato hands on, com acesso público.</p></div>"
        f'<div class="fcd"><div class="fk">Repositório</div><div class="fv">{REPO}</div>'
        "<p>Sete notebooks executados, os scripts e a aplicação Django.</p></div>"
        "</div>"
    )
    return pagina(
        slide(corpo, tag="Challenge FIAP 2026 com Locaweb", escuro=True, classe="fc fc2"),
        "Fecho",
        css,
    )


# ─────────────────────────────────────────────────────────────────────────────
# a ordem do deck
# ─────────────────────────────────────────────────────────────────────────────
# Slides emprestados dos protótipos da Sprint 3, lidos de onde estão.
#   nome no deck da Sprint 4  ->  arquivo em prototipos/slides/mvp/abertura/
REUSO_ABERTURA = {
    "contexto": "03-contexto-E",
    "contexto-estouro": "03b-causas-H",
    "problema": "04-problema-D",
    "fontes-de-dados": "08-arquitetura-D",
    "arquitetura-desenho": "09-desenho-D",
    "arquitetura-descricao": "10-descricao-A",
    "arquitetura-tecnologias": "11-tecnologias-A",
    "codigo-fonte": "12-codigo-C",
}
#   nome no deck da Sprint 4  ->  arquivo em prototipos/slides/mvp/deck/
# Os quatro que carregam figura exportada do matplotlib e respondem, dois a dois, "quais
# análises embasaram a decisão" e "quais indicadores mediram o resultado".
REUSO_DECK = {
    "analise-volume-quebra": "d17a-r5b",
    "analise-familiaridade": "d22a-r5b",
    "indicador-erro-horizonte": "d15n-r5b",
    "indicador-precisao-cobertura": "d25a-r5a",
}
# Capa e identificação da equipe vêm da Sprint 3 com o rótulo de sprint trocado.
DERIVADOS = {
    "capa": "01-capa-B",
    "equipe": "02-equipe-B",
}


def slides_proprios() -> dict[str, str]:
    proprios = {
        "descricao": s03_descricao(),
        "divisoria-02": s04_divisoria(),
        "urgencia": s08_urgencia(),
        "divisoria-03": s09_divisoria(),
        "objetivo": s10_objetivo(),
        "divisoria-04": s11_divisoria(),
        "abordagem": s12_abordagem(),
        "descartado": s13_descartado(),
        "indicadores": s23_indicadores(),
        "divisoria-05": s24_divisoria(),
        "link-aplicacao": s25_link(),
        "video-pitch": s36_video(),
        "divisoria-07": s37_divisoria(),
        "sintese": s38_sintese(),
        "aprendizados": s39_aprendizados(),
        "limitacoes": s40_limitacoes(),
        "proximos-passos": s41_proximos(),
        "fecho": s42_fecho(),
    }
    proprios.update({n: deriva_da_sprint3(ABERTURA / f"{a}.html") for n, a in DERIVADOS.items()})
    proprios.update(slides_das_telas())
    return proprios


def ordem() -> list[str]:
    """A sequência final, na ordem dos sete blocos do template da Sprint 4."""
    telas = [f"tela-{i:02d}-{t[0]}" for i, t in enumerate(TELAS, 1)]
    return (
        # 1 · detalhes iniciais da equipe e do projeto
        ["capa", "equipe", "descricao"]
        # 2 · compreendendo o desafio
        + ["divisoria-02", "contexto", "problema", "contexto-estouro", "urgencia"]
        # 3 · objetivo atual do projeto
        + ["divisoria-03", "objetivo"]
        # 4 · detalhes do projeto realizado
        + [
            "divisoria-04",
            "abordagem",
            "descartado",
            "fontes-de-dados",
            "arquitetura-desenho",
            "arquitetura-descricao",
            "arquitetura-tecnologias",
            "codigo-fonte",
            "analise-volume-quebra",
            "analise-familiaridade",
            "indicador-erro-horizonte",
            "indicador-precisao-cobertura",
            "indicadores",
        ]
        # 5 · demonstração da solução
        + ["divisoria-05", "link-aplicacao"]
        + telas
        # 6 · link do vídeo pitch
        + ["video-pitch"]
        # 7 · conclusão e próximos passos
        + [
            "divisoria-07",
            "sintese",
            "aprendizados",
            "limitacoes",
            "proximos-passos",
            "fecho",
        ]
    )


# ─────────────────────────────────────────────────────────────────────────────
# execução
# ─────────────────────────────────────────────────────────────────────────────
def confere_prints() -> None:
    faltando = [n for n, *_ in TELAS if not (PRINTS / f"{n}.png").exists()]
    if faltando:
        raise FileNotFoundError(
            "captura ausente: " + ", ".join(faltando) + ". Rode antes: "
            ".venv/Scripts/python scripts/captura_telas.py"
        )


def escreve_html() -> list[tuple[str, Path]]:
    """Grava os slides que nascem aqui e resolve a sequência inteira em caminho."""
    SAIDA.mkdir(parents=True, exist_ok=True)
    confere_prints()
    proprios = slides_proprios()
    caminhos: list[tuple[str, Path]] = []
    for pos, nome in enumerate(ordem(), 1):
        if nome in proprios:
            destino = SAIDA / f"{pos:02d}-{nome}.html"
            destino.write_text(proprios[nome], encoding="utf-8")
        elif nome in REUSO_ABERTURA:
            destino = ABERTURA / f"{REUSO_ABERTURA[nome]}.html"
        elif nome in REUSO_DECK:
            destino = DECK / f"{REUSO_DECK[nome]}.html"
        else:
            raise KeyError(f"slide sem origem declarada: {nome}")
        if not destino.exists():
            raise FileNotFoundError(f"slide não encontrado: {destino}")
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


def limpa_orfaos(caminhos: list[tuple[str, Path]], pngs: list[Path]) -> int:
    """Apaga HTML e PNG de numerações antigas.

    O nome de cada arquivo começa pela posição no deck, então inserir um slide no meio
    renumera tudo o que vem depois e deixaria a versão anterior na pasta, aparecendo
    primeiro para quem abre a pasta para conferir.
    """
    vivos = {c.name for _, c in caminhos} | {p.name for p in pngs}
    mortos = [
        p
        for p in list(SAIDA.glob("*.html")) + list(SAIDA_PNG.glob("*.png"))
        if p.name not in vivos
    ]
    for p in mortos:
        p.unlink()
    return len(mortos)


def monta_pptx(pngs: list[Path]) -> None:
    """Um slide por PNG, sangrado. É o mesmo formato entregue nas Sprints 2 e 3."""
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
    print(f"     {proprios} próprios + {len(caminhos) - proprios} emprestados da Sprint 3")
    print("2/3 · renderizando PNG")
    pngs = renderiza_png(caminhos)
    orfaos = limpa_orfaos(caminhos, pngs)
    if orfaos:
        print(f"     {orfaos} arquivos de numeração antiga removidos")
    print("3/3 · montando o .pptx")
    monta_pptx(pngs)
    print(f"Pronto: {PPTX.name} ({len(pngs)} slides)")


if __name__ == "__main__":
    main()
