# -*- coding: utf-8 -*-
"""Gera as versões comparadas do Panorama e da Previsão.

O dono do projeto pediu, em 10/09/2026, uma revisão das duas primeiras abas da
aplicação: *"tem muita coisa com cara de IA, tentando justificar tudo, adentrar
afundo onde não precisa"*, e um HTML em que ele possa transitar entre a versão
atual exata e a proposta.

Cada aba sai em três versões:

  atual        a página exportada, sem um byte de diferença. Carregada por
               iframe a partir de app/, para não haver dúvida de fidelidade.
  enxuta       só cortes e fusões. Nenhum dado novo, nenhum componente novo:
               tudo o que sobra já existe no template e no painel.json, então
               vira Django trocando marcação.
  livre        a tela repensada em torno da pergunta que ela responde. Muda a
               ordem dos blocos, funde seções e aposenta o que é interno do
               modelo.

A regra de corte, ditada por ele: **se a linha existe para explicar o próprio
gráfico, ela sai** — a explicação é falada na banca. Fica o que é dado, rótulo
e unidade.

As duas propostas nascem do HTML exportado, por cirurgia no DOM, e não
reescritas à mão. Assim herdam a folha de estilo real e o que muda entre as
versões é só o que eu mudei de propósito.

Uso:
    .venv/Scripts/python.exe prototipos/telas/revisao/_construir.py
"""
from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup

AQUI = Path(__file__).parent
RAIZ = AQUI.parents[2]
APP = RAIZ / "app"

# a profundidade daqui até app/estatico é a mesma para toda aba, porque o
# caminho é reescrito a partir da raiz de app/ e não da pasta da página
PREFIXO = "../../../app/"


# ── utilidades ──────────────────────────────────────────────────────────────
def carrega(rel: str) -> BeautifulSoup:
    return BeautifulSoup((APP / rel).read_text(encoding="utf-8"), "html.parser")


def reancora(s: BeautifulSoup, rel: str) -> None:
    """Reaponta folhas, scripts e imagens para app/, e mata os links de aba.

    Os links de navegação viram âncoras mortas: a comparação é de duas telas,
    e clicar em "Fila" a partir daqui levaria a lugar nenhum.
    """
    base = PREFIXO
    subiu = "../" if "/" in rel else ""
    for tag, attr in (("link", "href"), ("script", "src"), ("img", "src")):
        for n in s.find_all(tag):
            v = n.get(attr)
            if not v or v.startswith(("http", "//", "data:")):
                continue
            n[attr] = base + v[len(subiu):] if v.startswith(subiu) and subiu else base + v
    for a in s.find_all("a", href=True):
        if not a["href"].startswith("http"):
            a["href"] = "#"


def fora(no) -> None:
    if no is not None:
        no.decompose()


def limpa(s: BeautifulSoup, seletor: str, quantos: int | None = None) -> int:
    alvos = s.select(seletor)
    if quantos is not None:
        alvos = alvos[:quantos]
    for a in alvos:
        a.decompose()
    return len(alvos)


def nota(s: BeautifulSoup, texto: str) -> None:
    """Carimba a versão no rodapé, para não haver dúvida de qual se está vendo."""
    pe = s.select_one(".rod-e, footer .rod-e, footer span")
    if pe:
        pe.string = texto


def salva(s: BeautifulSoup, nome: str) -> None:
    (AQUI / nome).write_text(str(s), encoding="utf-8")
    print(f"  {nome:26s} {len(str(s)) // 1024:4d} kB")


# ═══ ferramentas comuns às propostas ════════════════════════════════════════
def folha(s: BeautifulSoup, livre: bool) -> None:
    """Prende a folha das propostas e carimba a versão no canto."""
    l = s.new_tag("link", rel="stylesheet", href="revisao.css")
    s.head.append(l)
    s.body["data-rv"] = "livre" if livre else "enxuta"


def cabeca_limpa(s: BeautifulSoup) -> None:
    """Os cortes da faixa escura, comuns às duas propostas."""
    # a manchete se explicava a si mesma: "Dia dentro do normal" seguido de
    # "Volume de uma quarta comum nas duas prioridades do KPI"
    limpa(s, ".en-s")
    # a sobrancelha dizia "Incidentes elegíveis ao KPI" e o selo logo abaixo
    # repetia "elegíveis ao KPI". Um dos dois basta, e o selo tem o número.
    ey = s.select_one(".en-ey")
    if ey:
        for t in ey.find_all(string=True):
            if "Incidentes eleg" in t:
                t.replace_with(re.sub(r"·\s*Incidentes eleg[íi]veis ao KPI", "", t))
    # "até o corte" é vocabulário de pipeline; a sobrancelha já diz o dia
    for c in s.select(".en-chips .pn-bh-c"):
        if "elegíveis ao KPI" in c.get_text():
            c.clear()
            c.append(BeautifulSoup("<b>19.973</b> elegíveis ao KPI", "html.parser"))


def corta_repeticoes(s: BeautifulSoup) -> None:
    """O que as duas propostas cortam por ser repetição pura."""
    # as três linhas de método sob os títulos de bloco
    limpa(s, ".en-bl-t p")
    # cada placa do dia repetia "77,4 previstos hoje · Intervalo de 59 a 96",
    # que está na faixa escura 40px acima
    for k in s.select(".en-g-k em"):
        k.decompose()
    # o cartão de risco dizia 8,1% três vezes: no número grande, na barra
    # "Este caso" e no rótulo dela. "8,6× a média da base" já é a comparação.
    limpa(s, ".en-dp-cmp")
    # a coluna "8,0× a média" na lista é o mesmo número da coluna de %
    # dividido pela média da base. Duas codificações do mesmo dado.
    limpa(s, ".en-dp-ix")
    # "Ativo IC01977 · 0 violações em 2 passagens" argumenta contra o próprio
    # cartão: é o maior risco do dia num ativo que nunca violou
    for sp in s.select(".en-dp-f span"):
        if "Ativo" in sp.get_text() and "· 0" in " ".join(sp.get_text().split()):
            sp.decompose()
    # o atingimento projetado aparecia no selo do cabeçalho e outra vez no
    # lado direito da comparação hoje → dezembro
    limpa(s, ".pn-p-e")
    # "Ainda cabem 22,0 violações": casa decimal em contagem de violação, e a
    # régua logo abaixo já desenha a margem
    limpa(s, ".en-meta-t")


# ═══ PANORAMA ═══════════════════════════════════════════════════════════════
def panorama_enxuta() -> None:
    """Só cortes e fusões. Vira Django trocando marcação, sem dado novo."""
    s = carrega("index.html"); reancora(s, "index.html")
    cabeca_limpa(s); corta_repeticoes(s)

    # a legenda da régua dizia em palavra o que a régua mostra em cor; sobra a
    # faixa da projeção, que é a única parte dela que carrega número novo
    for l in s.select(".en-cb-l"):
        alvo = None
        for sp in l.select("span"):
            if "Projeção entre" in sp.get_text():
                alvo = sp
        for sp in list(l.select("span")):
            if sp is not alvo:
                sp.decompose()

    folha(s, livre=False)
    salva(s, "panorama-enxuta.html")


def panorama_livre() -> None:
    """A tela remontada em torno das três perguntas que ela responde."""
    s = carrega("index.html"); reancora(s, "index.html")
    cabeca_limpa(s); corta_repeticoes(s)

    blocos = s.select("section.en-bl")

    # 1 · a faixa escura e o gráfico do dia viram um bloco só. Eram duas
    # camadas dizendo "quanto entra hoje": a faixa com o número previsto e o
    # gráfico com a chegada hora a hora. Fundidos, some um cabeçalho de seção
    # inteiro, com título, linha de método e um ícone.
    dia = blocos[0]
    cab = dia.select_one(".en-bl-h")
    fita = s.new_tag("div"); fita["class"] = "rv-fita"
    for sel in (".leg", ".pn-lk"):
        n = cab.select_one(sel)
        if n:
            fita.append(n.extract())
    cab.replace_with(fita)
    s.select_one("header.en-h").insert_after(dia)

    # 2 · o cartão herói e a lista eram a mesma fila: o herói é a primeira
    # posição dela, aberta em tamanho grande, e a lista se chamava "os outros
    # 5". Vira uma lista só de seis, com a primeira linha em destaque e o
    # fator dominante nela, que é o único dado que o herói tinha a mais.
    agir = blocos[1]
    heroi, lista = agir.select_one(".en-dp-c"), agir.select_one(".en-dp-r")
    if heroi and lista:
        rot = lista.select_one(".en-dp-rh")
        if rot:
            rot.string = "Casos abertos, do maior risco para o menor"
        # sem tinta e sem borda: o dono do projeto apontou a lista original
        # como referência de ritmo, e ali as seis linhas são iguais. O fator
        # dominante entra na MESMA linha do produto, para não abrir uma
        # terceira linha só na primeira posição.
        topo = BeautifulSoup(
            '<button class="en-dp-i wn" data-mod="incidente" data-k="INC8552480">'
            '<span class="en-dp-iv">8,1<u>%</u></span>'
            '<span class="en-fl-b"><i style="width:81.3%"></i></span>'
            '<span class="en-dp-ic"><b class="id">INC8552480</b>'
            '<em>Lsin · Team10 · 15h · produto lsin, 54% do peso</em>'
            '</span>'
            '<span class="pn-i-s"><svg class="ic" width="15" height="15" aria-hidden="true">'
            '<use href="#i-seta"></use></svg></span></button>', "html.parser")
        rot.insert_after(topo)
        heroi.decompose()
        cx = agir.select_one(".en-dp")
        if cx:
            cx["class"] = ["en-dp", "rv-so-lista"]

    # 3 · a meta perdeu o par de porcentagens de atingimento. Aqui a pergunta
    # é "o ano fecha?", e quem responde é a projeção contra o teto da faixa; a
    # escada de atingimento mora na aba Projeção, com link no cabeçalho.
    for card in s.select(".pn-p"):
        pri = card.select_one(".esc")
        pri = pri.get_text(strip=True) if pri else ""
        proj, teto = ("208", "263") if pri == "P3" else ("43", "39")
        fora_faixa = pri == "P2"
        linha = BeautifulSoup(
            f'<p class="rv-meta-l">'
            f'<span class="{"rv-fora" if fora_faixa else ""}">Projeção de dezembro '
            f'<b>{proj}</b></span>'
            f'<span>Faixa de 100% até <b>{teto}</b></span></p>', "html.parser")
        alvo = card.select_one(".en-meta-c")
        if alvo:
            alvo.replace_with(linha)
        # "Faixa de 100%: até 263" já é a linha nova; sai do número grande
        for em in card.select(".en-meta em"):
            em.decompose()
    limpa(s, ".en-cb-l")

    folha(s, livre=True)
    salva(s, "panorama-livre.html")


# ═══ PREVISÃO ═══════════════════════════════════════════════════════════════
def _previsao_base() -> BeautifulSoup:
    """Os cortes que valem para as duas propostas."""
    s = carrega("previsao/index.html"); reancora(s, "previsao/index.html")

    # "Cada dia sai como intervalo, e não como número único: é a largura dele
    # que dimensiona a escala da equipe." A largura está desenhada.
    limpa(s, ".pv-h-t p")

    # "Trinta dias medidos e duas semanas previstas. A faixa só existe do lado
    # previsto: o que já aconteceu não tem incerteza." E, no bloco seguinte,
    # "O que o modelo enxerga é dia útil contra fim de semana."
    limpa(s, ".pv-bl-h p")

    # cada placa repetia "Intervalo de 59 a 96 · 40 registrados até as 15h",
    # que é palavra por palavra o que a faixa escura diz no topo
    for e in s.select(".pv-tr-h em"):
        e.decompose()

    # "Escala do cartão até 76 incidentes por dia" e "A barra é o intervalo
    # previsto. O tique é a média do dia da semana" — a segunda ainda repetia
    # a linha do cabeçalho do bloco, três parágrafos acima
    limpa(s, ".pv-c-h p")

    # "Dia cheio não é dia de violação. Esta aba dimensiona a equipe. Quem diz
    # em qual caso olhar é a fila." É opinião sobre a própria tela, e o
    # caminho para a fila já está na navegação do topo.
    limpa(s, ".pv-fa")
    return s


def previsao_enxuta() -> None:
    s = _previsao_base()
    salva(s, "previsao-enxuta.html")


def previsao_livre() -> None:
    """A ordem invertida: primeiro o que dimensiona a equipe, depois a prova."""
    s = _previsao_base()

    blocos = s.select("section.pv-bl")
    historico, semana = blocos[0], blocos[1]

    # 1 · "Base da previsão: a sazonalidade semanal" é o modelo explicando a si
    # mesmo. A média por dia da semana já aparece como tique dentro de cada
    # barra dos próximos oito dias — o gráfico de sete barras acima dela só
    # mostra de onde o tique saiu. Sai o gráfico, ficam os oito dias.
    for c in s.select(".pv-sem"):
        c.decompose()
    for card in s.select(".pv-c"):
        velho_h = None
        for h in card.select(".pv-c-h"):
            if "Média por dia da semana" in h.get_text(" ", strip=True):
                velho_h = h
                break
        novo_h = card.select_one(".pv-c-h2")
        if velho_h is None or novo_h is None:
            continue
        # o selo da prioridade morava no cabeçalho que saiu. Sem ele as duas
        # placas ficam idênticas e não dá para saber qual é P3 e qual é P2.
        selo = velho_h.select_one(".esc")
        if selo is not None:
            novo_h.insert(0, selo.extract())
        velho_h.decompose()
        novo_h["class"] = ["pv-c-h", "rv-c-h1"]

    # 2 · a inversão. Quem abre a Previsão quer saber quanto trabalho vem, e
    # isso são os oito dias. O histórico emendado na previsão é a prova de que
    # o número tem lastro, e prova vem depois da afirmação.
    tit = semana.select_one(".pv-bl-h div h2")
    if tit:
        tit.string = "O que vem pela frente"
    tit2 = historico.select_one(".pv-bl-h div h2")
    if tit2:
        tit2.string = "Como o modelo chegou nesses números"
    historico.extract()
    semana.insert_after(historico)

    salva(s, "previsao-livre.html")


# ═══ PROJEÇÃO ══════════════════════════════════════════════════════════════
def _projecao_base() -> BeautifulSoup:
    s = carrega("projecao/index.html"); reancora(s, "projecao/index.html")

    # "As violações de OLA já acumuladas em cada prioridade, e a nota em que
    # dezembro deve terminar." É o título "Onde o ano fecha" outra vez.
    limpa(s, ".pj-h p")

    # a régua já traz "191 a 225" escrito em cima da faixa e "100% até 263" na
    # marca do teto. A legenda de três itens embaixo diz o mesmo em palavra.
    limpa(s, ".pj-rg .pj-lg, .pj-rg-l, .pj-rg > .lg")
    for l in s.select(".pj-rg div, .pj-rg p"):
        if "Já aconteceram" in l.get_text() and "Intervalo da projeção" in l.get_text():
            l.decompose()

    # sob PROJETADAS estava "Entre 191 e 225 até dezembro", que é a mesma
    # faixa desenhada na régua três linhas abaixo
    for e in s.select(".pj-n em, .pj-n small, .pj-n span"):
        if e.get_text(strip=True).startswith("Entre "):
            e.decompose()
    return s


def projecao_enxuta() -> None:
    s = _projecao_base()
    folha(s, livre=False)
    salva(s, "projecao-enxuta.html")


def projecao_livre() -> None:
    """A conta da projeção sobe: é ela que responde de onde vem o número."""
    s = _projecao_base()

    # o trio "Já aconteceram / Limite para 100% / Projetadas" repete em número
    # o que a régua desenha logo abaixo, com o agravante de que cada um traz
    # uma linha de apoio própria. A régua fica; a decomposição, que é a única
    # coisa da tela que explica de ONDE sai a projeção, sobe para o lugar dela.
    for card in s.select(".pj-c"):
        trio, dec, regua = (card.select_one(".pj-n"), card.select_one(".pj-dec"),
                            card.select_one(".pj-rg"))
        if not (trio and dec and regua):
            continue
        # a conta fecha na própria linha: o resultado sai do cartão "Projetadas"
        # que estava no trio, e não de soma feita aqui
        proj = ""
        for c in trio.select(".pj-n-c"):
            if "Projetadas" in c.get_text():
                b = c.select_one("b")
                proj = b.get_text(strip=True) if b else ""
        if proj:
            dec.append(BeautifulSoup(
                f'<span class="rv-igual">= <b>{proj}</b> <em>projetadas até dezembro</em>'
                f'</span>', "html.parser"))
        trio.decompose()
        regua.insert_before(dec.extract())

    folha(s, livre=True)
    salva(s, "projecao-livre.html")


# ═══ FILA ══════════════════════════════════════════════════════════════════
def _fila_base() -> BeautifulSoup:
    s = carrega("fila/index.html"); reancora(s, "fila/index.html")

    # "Os 49 casos abertos até as 15h, do maior risco para o menor." é o
    # título "Em qual caso olhar primeiro" dito de novo, e o contador já está
    # nos filtros logo abaixo.
    limpa(s, ".fl-h p")

    # "Escala até o limite de alerta, 10%" no cabeçalho da coluna: as faixas
    # estão nomeadas nos filtros, com os intervalos, dois blocos acima.
    for e in s.select(".fl-tb-h em, .fl-tb-h small, .fl-tb-h span span"):
        if "Escala at" in e.get_text():
            e.decompose()

    # "O desfecho do OLA não é conhecido enquanto o caso está em aberto, então
    # a fila mostra risco, e não violação." Metodologia no pé da tela.
    for frase in s.select("p.fl-tb-f"):
        if "desfecho do OLA" in frase.get_text():
            # sobra a contagem e o corte, que sao fato; sai a explicacao de por
            # que a coluna se chama risco e nao violacao
            frase.string = "49 casos · corte às 15h de hoje."
    return s


def fila_enxuta() -> None:
    s = _fila_base()
    folha(s, livre=False)
    salva(s, "fila-enxuta.html")


def fila_livre() -> None:
    """Trinta e quatro das 49 linhas dizem 'nada aqui'. Elas se recolhem."""
    s = _fila_base()

    # 1 · os dois cartões do topo são as linhas 1 e 13 da tabela, abertas em
    # tamanho grande, com o mesmo 8,1% escrito três vezes em cada um. A tabela
    # já começa pelo maior risco: o cartão não acrescenta posição nenhuma.
    limpa(s, ".fl-rs")

    # 2 · a fila tem 49 casos e 34 deles estão na faixa de rotina, de 0,0% a
    # 1,0% — uma violação a cada mil. Eles ocupam duas telas e meia dizendo
    # que não há o que fazer. Ficam recolhidos atrás de um resumo, e o filtro
    # "Rotina" continua no topo para quem quiser todos.
    linhas = s.select(".fl-tb .fl-l")
    rotina = [l for l in linhas if "rotina" in l.get_text(" ", strip=True).lower()]
    if rotina:
        det = s.new_tag("details"); det["class"] = "rv-rotina"
        res = s.new_tag("summary")
        res.append(BeautifulSoup(
            f"<span><b>{len(rotina)} casos na faixa de rotina</b>, de 0,0% a 1,0% de risco"
            f"</span><em>abrir</em>", "html.parser"))
        det.append(res)
        rotina[0].insert_before(det)
        for l in rotina:
            det.append(l.extract())

    folha(s, livre=True)
    salva(s, "fila-livre.html")


if __name__ == "__main__":
    print("gerando as versões:")
    panorama_enxuta(); panorama_livre()
    projecao_enxuta(); projecao_livre()
    fila_enxuta(); fila_livre()
    previsao_enxuta()
