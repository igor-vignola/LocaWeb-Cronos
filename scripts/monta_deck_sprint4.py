# -*- coding: utf-8 -*-
"""Monta o deck da Sprint 4 sobre o deck da banca de 15/09/2026.

Uma lista ORDEM de 59 itens, seis tipos:
  ("banca", n, nome)        slide n de prototipos/slides/ao-vivo/blocos/, byte a byte
  ("pitch", "objetivo", .)  o slide próprio do vídeo pitch, versão A
  ("bloco", nome, nome)     bloco novo em prototipos/slides/sprint4/blocos/NN-nome.html;
                            se o arquivo não existe, vira slide de espera "Aqui irá ficar"
  ("div", n_bloco, nome)    divisória de bloco do template, gerada de um molde
  ("tela", chave, nome)     captura da aplicação na forma A, com balões (deck_sprint4_telas)
  ("arquivo", Path, nome)   HTML pronto da Sprint 3, renderizado onde está

Cada slide vira um HTML autônomo em sprint4/_build/, fotografado em 1600x900 a 2x com a
animação congelada no estado final, e entra no .pptx com a fala nas notas. O deck.html é
um visualizador das imagens, para o Igor revisar com as setas.

Uso:
    .venv/Scripts/python scripts/monta_deck_sprint4.py            # tudo
    .venv/Scripts/python scripts/monta_deck_sprint4.py --so 5 6   # só renderiza as posições 5 e 6
"""
from __future__ import annotations

import html as _html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deck_sprint4_pptx import monta as monta_pptx  # noqa: E402
from deck_sprint4_telas import (  # noqa: E402
    RECORTES, TELAS, html_tela, nota_recorte, nota_tela, secao_recorte, secao_tela_inteira,
)

RAIZ = Path(__file__).resolve().parents[1]
SLIDES = RAIZ / "prototipos" / "slides"
AO_VIVO = SLIDES / "ao-vivo"
PITCH = SLIDES / "pitch"
ABERTURA = SLIDES / "mvp" / "abertura"
SAIDA = SLIDES / "sprint4"
BLOCOS = SAIDA / "blocos"
BUILD = SAIDA / "_build"
PNG = SAIDA / "_png"
VIEWER = SAIDA / "deck.html"
PPTX = RAIZ / "sprints" / "EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx"
PRINTS_DIR = RAIZ / "sprints" / "sprint-3" / "prints"
CHROME = (r"C:\Users\igor.vignola\AppData\Local\ms-playwright"
          r"\chromium-1217\chrome-win64\chrome.exe")

URL_APP = "igor-vignola.github.io/LocaWeb-Cronos"
URL_VIDEO = "youtu.be/IeWLVBD0Jas"
REPO = "github.com/igor-vignola/LocaWeb-Cronos"

FONTES = ('<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600'
          '&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')
LOGO_CLARO = ('<svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" '
              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" '
              'r="3" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg>')
LOGO_ESCURO = LOGO_CLARO.replace('stroke="#fff"', 'stroke="#0A0E17"').replace("#3B82F6", "#2563EB")

RE_STYLE = re.compile(r"<style>(.*?)</style>", re.S)
RE_SECTION = re.compile(r'(<section class="slide.*?</section>)', re.S)

# ── os sete blocos do template ────────────────────────────────────────────────
BLOCO_NOME = {
    1: "Detalhes iniciais da equipe e do projeto",
    2: "Compreendendo o desafio",
    3: "Objetivo atual do projeto",
    4: "Detalhes do projeto realizado",
    5: "Demonstração da solução",
    6: "Link do vídeo pitch",
    7: "Conclusão e próximos passos",
}
# uma frase por divisória, dizendo o que o bloco cobre
DIV_LINHA = {
    1: "Quem fez, o nome da solução e o que ela entrega, em dois parágrafos.",
    2: "O cenário, o problema nomeado, o efeito no indicador e por que resolver agora.",
    3: "O objetivo geral e as duas respostas que o sistema devolve.",
    4: "A abordagem, o que o dado mostrou, cada modelo por vez, o que a operação recebe, a arquitetura e a stack.",
    5: "O endereço da aplicação, as seis abas e as quatro folhas, cada uma com quem usa e como.",
    7: "O que ficou pronto, o que a equipe aprendeu, os limites que continuam de pé e o que vem em seguida.",
}
# o título da divisória: mais curto que o nome oficial, que fica na pastilha do topo
BLOCO_TITULO = {
    1: "Equipe e projeto",
    2: "Compreendendo o desafio",
    3: "Objetivo do projeto",
    4: "Detalhes do projeto realizado",
    5: "Demonstração da solução",
    7: "Conclusão e próximos passos",
}
# a fila dos sete blocos no pé da divisória
BLOCO_CURTO = {1: "Equipe e projeto", 2: "O desafio", 3: "Objetivo", 4: "Projeto realizado",
               5: "Demonstração", 6: "Vídeo pitch", 7: "Conclusão"}


def lista_blocos(atual: int) -> str:
    partes = []
    for n in range(1, 8):
        cls = "on" if n == atual else ("ok" if n < atual else "")
        partes.append(f'<span class="{cls}"><b>{n:02d}</b>{BLOCO_CURTO[n]}</span>')
    return "".join(partes)


def render_div(molde: Path, n_bloco: int) -> tuple[str, str]:
    """Troca {N}, {NOME}, {LINHA} e {LISTA} no molde da divisória de bloco."""
    secao, css = secao_e_css(molde)
    secao = (secao.replace("{N}", f"{n_bloco:02d}")
             .replace("{NOME}", BLOCO_TITULO[n_bloco])
             .replace("{LINHA}", DIV_LINHA[n_bloco])
             .replace("{LISTA}", lista_blocos(n_bloco)))
    return secao, css


def _nomes_banca() -> dict[int, str]:
    return {int(p.name[:2]): p.stem.split("-", 1)[1]
            for p in (AO_VIVO / "blocos").glob("[0-9][0-9]-*.html")}


NB = _nomes_banca()

def _telas_e_recortes() -> list[tuple[str, object, str]]:
    """Cada tela inteira seguida dos seus recortes, quando ela tem recortes definidos."""
    itens: list[tuple[str, object, str]] = []
    for i, t in enumerate(TELAS, 1):
        itens.append(("tela", t[0], f"tela-{i:02d}-{t[0]}"))
        for k in range(1, len(RECORTES.get(t[0], [])) + 1):
            itens.append(("recorte", (t[0], k), f"recorte-{i:02d}-{k}-{t[0]}"))
    return itens


# Sem divisória de bloco, sem descrição resumida e sem slide de abordagem: o Igor tirou os
# três em 21/09/2026. A arquitetura volta completa, nos quatro slides da Sprint 3.
ORDEM: list[tuple[str, object, str]] = (
    [("banca", 1, "capa"), ("banca", 2, "equipe"), ("banca", 3, "cronos"),
     ("bloco", "descricao", "descricao"),
     ("banca", 4, "prazo"), ("banca", 5, "quebras"), ("banca", 6, "fila-ordem"),
     ("pitch", "objetivo", "objetivo")]
    + [("banca", n, NB[n]) for n in range(7, 31)]
    + [("arquivo", ABERTURA / "08-arquitetura-D.html", "fontes-de-dados"),
       ("arquivo", ABERTURA / "09-desenho-D.html", "arquitetura-desenho"),
       ("arquivo", ABERTURA / "10-descricao-A.html", "arquitetura-descricao"),
       ("arquivo", ABERTURA / "11-tecnologias-A.html", "arquitetura-tecnologias"),
       ("banca", 31, "aplicacao")]
    + _telas_e_recortes()
    + [("bloco", "acesso", "acesso"),
       ("bloco", "conclusao", "conclusao"),
       ("banca", 32, "obrigado")]
)
# o bloco do template em que cada trecho começa, para a pastilha do slide de espera e o visualizador
BLOCO_INICIO = {"capa": 1, "prazo": 2, "objetivo": 3, "div-analise": 4, "aplicacao": 5,
                "acesso": 6, "conclusao": 7}

# ── o que cada posição nova vai ter, para o slide de espera ───────────────────
# nome -> (título curto, o que o slide traz, origem do material)
ESPERA: dict[str, tuple[str, str, str]] = {
    # Posição cujo bloco ainda não existe vira um slide tracejado com o que vai ter ali.
    # Hoje todos existem, e o dicionário fica como rede de segurança para o próximo que
    # entrar na ORDEM antes de ser desenhado.
}

# ── ajustes de texto nos slides da banca ──────────────────────────────────────
AJUSTES: dict[int, list[tuple[str, str]]] = {
    2: [("Quem apresenta", "A equipe")],
    31: [("Demonstração ao vivo", "Demonstração da solução")],
}
# linha de apoio abaixo do título, só onde o título sozinho não fecha a mensagem.
# Proposta ao Igor no lote 2; entra aqui depois de aprovada.
APOIO: dict[int, str] = {
    8: "O total registrado saltou <b>5,4 vezes</b> de agosto para setembro; a série que conta para a meta ficou em 2.330 e 2.324.",
    9: "<b>98,3%</b> dos incidentes elegíveis estão em 2025, então o treino usa só 2025 e a sazonalidade anual fica desligada.",
    10: "No <b>P2</b> o efeito do fim de semana some: 0,75% contra 0,83% no dia útil. O de quem abre vale nas duas prioridades.",
    13: "<b>116 das 238</b> quebras de 2025 foram em item de configuração que já tinha quebrado antes no ano.",
    15: "A causa mais frequente tem taxa de violação abaixo da média da base; a ordenação certa é por taxa, não por volume.",
    17: "<b>13 dos 14</b> dias da semana seguinte caíram dentro da faixa prevista em 1º de outubro, nas duas prioridades.",
    18: "Erro médio de <b>4,2</b> por dia no P2 e <b>11,8</b> no P3, contra 4,9 e 11,3 do melhor baseline de cada série.",
    20: "<b>13 quebras</b> nos 50 primeiros da fila de risco; ordenando por prioridade, como se faz hoje, nenhuma.",
    21: "A regressão logística empata com o XGBoost em ROC AUC, vence em PR-AUC e prevê <b>48,1</b> quebras onde houve 50.",
    26: "Em 1º de outubro a projeção já dizia <b>P2 acima</b> do limite e <b>P3 dentro</b>; o ano fechou em 42 e 196.",
    27: "A nota junta cinco medidas de <b>P2 e P3</b>; a posição diz o tamanho do problema e a cor diz o tipo.",
    # 29 e 30 ficam sem linha: o 29 já traz a mesma frase no corpo, e no 30 a linha encostava
    # no rótulo da caixa da imagem Docker.
}
# o template pede que o objetivo comece por um verbo de ação
APOIO_PITCH: dict[str, str] = {
    "objetivo": "<b>Desenvolver</b> um sistema que antecipe a violação de OLA e a projeção da meta anual da "
                "Locaweb, entregando a leitura do ano antes da apuração de dezembro, nas prioridades "
                "<b>P2</b> e <b>P3</b>.",
}

# notas dos slides novos; os da banca vêm do roteiro, as telas do texto de uso real
NOTAS: dict[str, str] = {
    "objetivo": (
        "Desenvolver um sistema que antecipe a violação de OLA e a projeção da meta anual da Locaweb, "
        "entregando a leitura do ano antes da apuração de dezembro, nas prioridades P2 e P3. O Cronos lê "
        "os 122.543 incidentes do histórico, dos quais 25.600 entram no indicador, e devolve duas "
        "respostas: quais incidentes vão estourar o prazo, pela regressão logística, e quantos incidentes "
        "chegam nos próximos sete dias, pelo Prophet."
    ),
}
NOTAS.update({
    "descricao": (
        "O Cronos lê o histórico de incidentes da Locaweb e diz, antes de o prazo estourar, onde "
        "a operação precisa agir. Ele parte dos 122.543 incidentes registrados entre janeiro de "
        "2023 e dezembro de 2025, recorta pelo campo oficial Entrou para KPI? os 25.600 que "
        "contam para o indicador de OLA, e devolve três respostas: quantos incidentes entram nos "
        "próximos sete dias, qual incidente aberto tem maior probabilidade de estourar o prazo, e "
        "em que posição a meta anual de P2 e de P3 deve fechar. São dois modelos e dois cálculos, "
        "publicados em uma aplicação Django de seis abas, em contêiner Docker e sem dependência "
        "de provedor de nuvem."),
    "conclusao": (
        "Nos 50 primeiros casos da fila de risco, o Cronos encontra 13 das 50 violações de uma "
        "base de avaliação com 5.183 incidentes, fora do período de treino. Ordenando por "
        "prioridade, que é o comportamento padrão da ferramenta de atendimento hoje, essas mesmas "
        "50 posições não trazem nenhuma. Além disso: três meses de antecedência na leitura da "
        "meta do ano, com a chamada certa nas duas prioridades; e seis abas no ar em um "
        "contêiner, sem provedor de nuvem amarrado. O limite que continua de pé é a cobertura da "
        "faixa de 80%, que fica entre 59% e 61% dos dias no P3 contra 86% a 88% no P2."),
    "fontes-de-dados": (
        "Duas fontes. A planilha LW-DATASET.xlsx, com 122.543 incidentes em 19 campos, de janeiro "
        "de 2023 a dezembro de 2025, é a única fonte de incidentes. O calendário de feriados "
        "nacionais entra pela biblioteca holidays, porque o dataset não traz feriado, e vira "
        "regressor do Prophet."),
    "arquitetura-desenho": (
        "O caminho do dado, da planilha ao painel do gestor: carga e tipagem, o filtro de "
        "elegibilidade pelo campo oficial, os notebooks que treinam e gravam Parquet, e a "
        "aplicação Django que apenas lê. O nó tracejado é a leitura direta da base interna da "
        "Locaweb, que é próximo passo."),
    "arquitetura-descricao": (
        "Cada elemento do desenho com o papel que cumpre: a base recortada, os quatro modelos e "
        "cálculos, os artefatos em Parquet e a camada de apresentação. Nada é calculado em tempo "
        "de tela."),
    "arquitetura-tecnologias": (
        "Python, pandas e scikit-learn na análise; Prophet na previsão de volume; Django na "
        "aplicação; Docker na entrega. Nenhum serviço proprietário de nuvem no caminho, então a "
        "mesma imagem roda na Locaweb ou em qualquer provedor."),
})
NOTAS.update({
    "acesso": (
        "Os dois endereços que a entrega exige. A aplicação está em "
        "igor-vignola.github.io/LocaWeb-Cronos, que abre direto no painel operacional, sem "
        "cadastro, com os mesmos dados da demonstração. O vídeo pitch está em "
        "youtu.be/IeWLVBD0Jas, público no YouTube, com cinco minutos em formato hands on. O "
        "código-fonte está em github.com/igor-vignola/LocaWeb-Cronos. Cada código na tela leva "
        "ao endereço escrito ao lado dele."),
})

# ── CSS do builder: congelamento, linha de apoio, slide de espera ─────────────
CSS_BUILDER = """
html,body{margin:0;padding:0;background:#fff;overflow:hidden}
#palco{width:1600px;height:900px;position:relative;overflow:hidden}
.slide{animation:none !important}
.mesh{animation:none !important;transform:none !important}
.is-active *:not(.mesh){animation-duration:.01ms !important;animation-delay:0ms !important}
/* linha de apoio abaixo do título, para o slide lido sem apresentador */
.apoio{font-size:19px;line-height:1.5;color:var(--tx);margin-top:14px;max-width:64ch}
.apoio b{color:var(--head);font-weight:700}
.dark .apoio{color:#B7C0CB} .dark .apoio b{color:#fff}
/* slide de espera do esqueleto */
.esp .body{justify-content:center}
.esp .quadro{border:2px dashed #B9C4D6;border-radius:22px;padding:44px 52px;max-width:1100px}
.esp .tt{font-size:54px}
.esp .tt .hl{color:var(--accent)}
.esp .apoio{font-size:20px;margin-top:22px}
.esp .ori{font-family:var(--mono);font-size:13px;color:var(--tx2);margin-top:26px}
"""


def pagina(css_bloco: str, secao: str) -> str:
    estilo = (AO_VIVO / "_estilo.css").read_text(encoding="utf-8")
    secao = secao.replace('class="slide', 'class="is-active slide', 1)
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">{FONTES}'
            f"<style>{estilo}\n{css_bloco}\n{CSS_BUILDER}</style></head>"
            f'<body><div id="palco">{secao}</div></body></html>')


def resolve_contadores(texto: str) -> str:
    """Escreve o valor final onde o contador espera o JS."""
    def valor(m: re.Match) -> str:
        alvo = m.group(2)
        dec = re.search(r'data-dec="(\d+)"', m.group(1))
        if dec and int(dec.group(1)) > 0:
            v = f"{float(alvo.replace(',', '.')):.{int(dec.group(1))}f}".replace(".", ",")
        else:
            v = f"{int(float(alvo.replace(',', '.'))):,}".replace(",", ".")
        return m.group(1) + v + m.group(3)
    return re.sub(r'(<span class="ct"[^>]*data-to="([^"]+)"[^>]*>)[^<]*(</span>)', valor, texto)


def secao_e_css(arquivo: Path) -> tuple[str, str]:
    t = arquivo.read_text(encoding="utf-8")
    css = "\n".join(c.strip() for c in RE_STYLE.findall(t))
    achadas = RE_SECTION.findall(t)
    if not achadas:
        raise SystemExit(f'{arquivo.name}: nenhuma <section class="slide ...">')
    return achadas[0], css


def slide_banca(n: int) -> tuple[str, str]:
    arquivo = next(AO_VIVO.glob(f"blocos/{n:02d}-*.html"))
    secao, css = secao_e_css(arquivo)
    secao = resolve_contadores(secao)
    # _build/ fica na mesma profundidade de ao-vivo/blocos/: só ../figs muda de dono
    secao = secao.replace('src="../figs/', 'src="../../ao-vivo/figs/')
    css = css.replace("url(../figs/", "url(../../ao-vivo/figs/")
    for de, para in AJUSTES.get(n, []):
        if de not in secao:
            raise SystemExit(f"slide {n}: ajuste «{de}» não encontrado")
        secao = secao.replace(de, para)
    if n in APOIO:
        secao = secao.replace("</h1>", f'</h1><p class="apoio rv">{APOIO[n]}</p>', 1)
    return secao, css


def slide_pitch(nome: str) -> tuple[str, str]:
    arquivo = next(PITCH.glob(f"blocos/[0-9][0-9]-{nome}.html"))
    secao, css = secao_e_css(arquivo)
    secao = resolve_contadores(secao)
    if nome in APOIO_PITCH:
        secao = secao.replace("</h1>", f'</h1><p class="apoio rv">{APOIO_PITCH[nome]}</p>', 1)
    return secao, css


def slide_espera(nome: str, bloco: int) -> tuple[str, str]:
    titulo, conteudo, origem = ESPERA[nome]
    secao = (f'<section class="slide light esp"><div class="mesh"></div><div class="grid-bg"></div>'
             f'<div class="hd"><div class="bi">{LOGO_CLARO}</div><div class="bn">Cronos</div>'
             f'<div class="tag">Bloco {bloco} &middot; {BLOCO_NOME[bloco]}</div></div>'
             f'<div class="body"><div class="quadro"><span class="eb">Em construção</span>'
             f'<h1 class="tt">Aqui irá ficar: <span class="hl">{titulo}</span></h1>'
             f'<p class="apoio">{conteudo}</p><p class="ori">Origem: {origem}</p></div></div>'
             f'<div class="ft"><span>Esqueleto do deck da Sprint 4</span></div></section>')
    return secao, ""


def slide_bloco(nome: str, bloco: int) -> tuple[str, str]:
    achados = sorted(BLOCOS.glob(f"[0-9][0-9]-{nome}.html"))
    if not achados:
        return slide_espera(nome, bloco)
    secao, css = secao_e_css(achados[0])
    return resolve_contadores(secao), css


def slide_div(n_bloco: int) -> tuple[str, str]:
    """A divisória de bloco. Até o lote 1 escolher o desenho, é um slide de espera."""
    molde = BLOCOS / "00-div-bloco.html"
    if not molde.exists():
        return slide_espera(f"div-bloco-{n_bloco}", n_bloco)
    return render_div(molde, n_bloco)


def escreve_build() -> list[tuple[int, str, Path, int]]:
    """Um HTML por slide em _build/. Devolve (posição, nome, caminho, bloco)."""
    BUILD.mkdir(parents=True, exist_ok=True)
    for velho in BUILD.glob("*.html"):
        velho.unlink()
    itens, bloco = [], 1
    for pos, (tipo, ref, nome) in enumerate(ORDEM, 1):
        bloco = BLOCO_INICIO.get(nome, bloco)
        if tipo == "banca":
            secao, css = slide_banca(int(ref))
            html = pagina(css, secao)
        elif tipo == "pitch":
            secao, css = slide_pitch(str(ref))
            html = pagina(css, secao)
        elif tipo == "bloco":
            secao, css = slide_bloco(str(ref), bloco)
            html = pagina(css, secao)
        elif tipo == "div":
            secao, css = slide_div(int(ref))
            html = pagina(css, secao)
        elif tipo == "tela" and str(ref) in RECORTES:
            # tela no visual da banca, com marcadores; os recortes vêm nos slides seguintes
            secao, css = secao_tela_inteira(str(ref), URL_APP)
            html = pagina(css, secao)
        elif tipo == "tela":
            # forma A da Sprint 3, enquanto a tela não ganha recortes
            pos_tela = int(nome.split("-")[1])
            html = html_tela(str(ref), pos_tela, len(TELAS), URL_APP)
        elif tipo == "recorte":
            chave, k = ref  # type: ignore[misc]
            secao, css = secao_recorte(str(chave), int(k), URL_APP)
            html = pagina(css, secao)
        elif tipo == "arquivo":
            caminho = Path(ref)
            if not caminho.exists():
                raise SystemExit(f"arquivo não encontrado: {caminho}")
            itens.append((pos, nome, caminho, bloco))
            continue
        else:
            raise SystemExit(f"tipo desconhecido: {tipo}")
        destino = BUILD / f"{pos:02d}-{nome}.html"
        destino.write_text(html, encoding="utf-8")
        itens.append((pos, nome, destino, bloco))
    return itens


MEDIDA = """() => {
  const a = document.querySelector('.slide');
  const corpo = a.querySelector('.body');
  const cr = corpo ? corpo.getBoundingClientRect() : null;
  const achados = [];
  a.querySelectorAll('*').forEach(el => {
    const c = el.className.toString();
    if (/\\b(mesh|grid-bg)\\b/.test(c)) return;
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.height > 0 &&
        (r.left < -1 || r.right > 1601 || r.top < -1 || r.bottom > 901))
      achados.push('FORA DO PALCO ' + el.tagName.toLowerCase() + '.' + c.slice(0, 24));
    if (cr && corpo.contains(el) && r.width > 0 && r.height > 0 && r.bottom > cr.bottom + 2)
      achados.push('FORA DO CORPO ' + el.tagName.toLowerCase() + '.' + c.slice(0, 24) +
        ' (' + Math.round(r.bottom - cr.bottom) + 'px)');
    if (parseFloat(getComputedStyle(el).opacity) === 0 && r.width > 2)
      achados.push('INVISIVEL ' + el.tagName.toLowerCase() + '.' + c.slice(0, 24));
  });
  return achados.slice(0, 6);
}"""


# onde está a captura no slide, para a transição Transformar do .pptx casar os dois
# slides. Devolve a caixa em px do palco e o recorte em fração da imagem.
ONDE_ESTA_A_CAPTURA = """() => {
  const el = document.querySelector('[data-morph]');
  if (!el) return null;
  const r = el.getBoundingClientRect();
  const c = el.getAttribute('data-crop').split(' ').map(Number);
  return {arquivo: el.getAttribute('data-morph'),
          caixa: [r.left, r.top, r.width, r.height], crop: c};
}"""

# esconde só o preenchimento da captura, mantendo o cartão, a borda e a sombra: é
# sobre esse fundo que o .pptx cola a captura como objeto próprio
SEM_A_CAPTURA = """() => {
  document.querySelectorAll('[data-morph]').forEach(el => {
    el.style.backgroundImage = 'none';
    el.querySelectorAll('img').forEach(i => { i.style.visibility = 'hidden'; });
  });
}"""


def render(itens: list[tuple[int, str, Path, int]],
           so: set[int] | None) -> tuple[list[Path], dict[int, dict]]:
    """Fotografa cada slide e, onde há captura, também a versão sem ela.

    A versão cheia é a que o visualizador mostra. A versão sem a captura vira o
    fundo do .pptx, que recebe a captura por cima como objeto solto: é o que
    permite a transição Transformar animar o mesmo objeto entre dois slides.
    """
    from playwright.sync_api import sync_playwright

    PNG.mkdir(parents=True, exist_ok=True)
    pngs: list[Path] = []
    morph: dict[int, dict] = {}
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=CHROME)
        pg = nav.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=2).new_page()
        for pos, nome, caminho, _ in itens:
            destino = PNG / f"{pos:02d}-{nome}.png"
            fundo = PNG / f"{pos:02d}-{nome}_fundo.png"
            pngs.append(destino)
            pular = bool(so) and pos not in so and destino.exists()
            if not pular:
                pg.goto(caminho.resolve().as_uri(), wait_until="networkidle")
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(450)
                pg.locator(".slide").first.screenshot(path=str(destino))
                avisos = pg.evaluate(MEDIDA)
                print(f"  {pos:02d} {nome:<28}" + ("  " + " | ".join(avisos) if avisos else ""))
            else:
                pg.goto(caminho.resolve().as_uri(), wait_until="networkidle")
                pg.wait_for_timeout(120)

            achado = pg.evaluate(ONDE_ESTA_A_CAPTURA)
            if achado:
                if not pular or not fundo.exists():
                    pg.evaluate(SEM_A_CAPTURA)
                    pg.wait_for_timeout(80)
                    pg.locator(".slide").first.screenshot(path=str(fundo))
                morph[pos] = dict(
                    png_fundo=fundo,
                    imagem=PRINTS_DIR / f"{achado['arquivo']}.png",
                    caixa=tuple(achado["caixa"]),
                    crop=tuple(achado["crop"]),
                    grupo=achado["arquivo"],
                )
            elif fundo.exists():
                fundo.unlink()
        nav.close()
    return pngs, morph


def falas_da_banca() -> dict[int, str]:
    """A fala de cada slide da banca, do objeto FALAS do ROTEIRO.html, sem tags."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=CHROME)
        pg = nav.new_page()
        pg.goto((AO_VIVO / "ROTEIRO.html").as_uri())
        bruto = pg.evaluate("JSON.stringify(FALAS)")
        nav.close()
    falas = json.loads(bruto)
    saida = {}
    for n, f in falas.items():
        versoes = f.get("versoes") or []
        texto = " ".join(versoes[0].get("fala", [])) if versoes else ""
        saida[int(n)] = re.sub(r"<[^>]+>", "", texto).strip()
    return saida


def notas(itens) -> dict[int, str]:
    banca = falas_da_banca()
    saida = {}
    for pos, nome, _, _ in itens:
        tipo, ref, _ = ORDEM[pos - 1]
        if tipo == "banca":
            saida[pos] = banca.get(int(ref), "")
        elif tipo == "tela":
            saida[pos] = nota_tela(str(ref))
        elif tipo == "recorte":
            chave, k = ref  # type: ignore[misc]
            saida[pos] = nota_recorte(str(chave), int(k))
        else:
            saida[pos] = NOTAS.get(nome, "Em construção.")
    return saida


def escreve_viewer(itens, pngs: list[Path], notas_por_pos: dict[int, str]) -> None:
    quadros = "".join(
        f'<figure data-n="{pos}" data-bloco="{bloco}"><img src="_png/{png.name}" alt="{nome}">'
        f'<figcaption><b>{pos:02d}</b> {nome} &middot; Bloco {bloco} &middot; {BLOCO_NOME[bloco]}</figcaption>'
        f'<pre>{notas_por_pos.get(pos, "")}</pre></figure>'
        for (pos, nome, _, bloco), png in zip(itens, pngs))
    VIEWER.write_text(f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Cronos · Sprint 4 · {len(pngs)} slides</title>{FONTES}<style>
html,body{{margin:0;height:100%;background:#1B1F26;color:#fff;font-family:Outfit,system-ui,sans-serif;overflow:hidden}}
figure{{display:none;margin:0;position:absolute;inset:0}} figure.on{{display:block}}
figure img{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);max-width:100vw;max-height:calc(100vh - 92px);
  box-shadow:0 40px 130px -50px rgba(0,0,0,.7)}}
figcaption{{position:fixed;left:0;right:0;bottom:0;padding:14px 24px;font-size:13px;color:rgba(255,255,255,.72);
  background:linear-gradient(0deg,rgba(0,0,0,.7),transparent)}}
figcaption b{{color:#FBBF24;font-family:"JetBrains Mono",monospace}}
pre{{display:none;position:fixed;left:24px;right:24px;bottom:48px;max-height:38vh;overflow:auto;white-space:pre-wrap;
  font-family:Outfit,system-ui,sans-serif;font-size:15px;line-height:1.5;color:#E8ECF3;background:rgba(10,14,23,.94);
  border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:16px 20px;margin:0}}
body.notas pre{{display:block}}
#ajuda{{position:fixed;top:12px;right:16px;font-size:12px;color:rgba(255,255,255,.5)}}
</style></head><body>{quadros}
<div id="ajuda">← → slide · N notas · Home/End · F tela cheia</div>
<script>
var f=[].slice.call(document.querySelectorAll('figure')),i=0;
function go(k){{i=(k+f.length)%f.length;f.forEach(function(x,j){{x.classList.toggle('on',j===i)}});location.hash=f[i].dataset.n}}
window.addEventListener('keydown',function(e){{var k=e.key.toLowerCase();
 if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){{e.preventDefault();go(i+1)}}
 else if(e.key==='ArrowLeft'||e.key==='PageUp'){{e.preventDefault();go(i-1)}}
 else if(e.key==='Home')go(0);else if(e.key==='End')go(f.length-1);
 else if(k==='n')document.body.classList.toggle('notas');
 else if(k==='f'){{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}}}});
document.body.addEventListener('click',function(){{go(i+1)}});
go(Math.max(0,(parseInt(location.hash.slice(1),10)||1)-1));
</script></body></html>""", encoding="utf-8")


EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def varredura(itens) -> int:
    problemas = 0
    for pos, nome, caminho, _ in itens:
        t = caminho.read_text(encoding="utf-8")
        s = RE_SECTION.search(t)
        texto = re.sub(r"<style>.*?</style>", "", s.group(1) if s else t, flags=re.S)
        texto = _html.unescape(re.sub(r"<[^>]+>", " ", texto)).replace(" ", " ")
        avisos = []
        if re.search(r"\bturno", texto, re.I):
            avisos.append("turno")
        if "—" in texto:
            avisos.append("travessão")
        if EMOJI.search(texto):
            avisos.append("emoji")
        tem_p3 = re.search(r"\bP3\b|prioridade 3|\bna 3\b", texto, re.I)
        tem_p2 = re.search(r"\bP2\b|prioridade 2|\bna 2\b", texto, re.I)
        if tem_p3 and not tem_p2:
            avisos.append("P3 sem P2")
        if avisos:
            problemas += 1
            print(f"  VARREDURA {pos:02d} {nome}: {', '.join(avisos)}")
    return problemas


def limpa_orfaos(itens) -> int:
    """Apaga PNG de numeração antiga.

    O nome de cada arquivo começa pela posição no deck, então tirar um slide do meio
    renumera tudo o que vem depois e deixaria a versão anterior na pasta, aparecendo
    primeiro para quem abre a pasta para conferir.
    """
    vivos = {f"{p:02d}-{n}.png" for p, n, _, _ in itens}
    vivos |= {f"{p:02d}-{n}_fundo.png" for p, n, _, _ in itens}
    mortos = [x for x in PNG.glob("*.png") if x.name not in vivos]
    for x in mortos:
        x.unlink()
    return len(mortos)


def main() -> int:
    so = None
    if "--so" in sys.argv:
        so = {int(x) for x in sys.argv[sys.argv.index("--so") + 1:]}
    print("1/4 · HTML por slide")
    itens = escreve_build()
    esperas = sum(1 for _, _, c, _ in itens
                  if c.parent == BUILD and 'class="is-active slide light esp"' in c.read_text(encoding="utf-8"))
    print(f"     {len(itens)} slides, {esperas} de espera")
    print("2/4 · render")
    pngs, morph = render(itens, so)
    orfaos = limpa_orfaos(itens)
    if orfaos:
        print(f"     {orfaos} arquivos de numeração antiga removidos")
    print("3/4 · varredura de texto")
    if not varredura(itens):
        print("     limpa")
    print("4/4 · notas, pptx e visualizador")
    ns = notas(itens)
    contagem = monta_pptx(pngs, ns, morph, PPTX)
    escreve_viewer(itens, pngs, ns)
    print(f"     transição: {contagem['morph']} transformar, {contagem['fade']} esmaecer")
    print(f"Pronto: {PPTX.name} ({len(pngs)} slides) · {VIEWER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
