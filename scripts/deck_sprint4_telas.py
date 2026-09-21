# -*- coding: utf-8 -*-
"""As dez capturas da aplicação, na forma A da Sprint 3, com balões numerados.

Cada balão aponta uma funcionalidade sobre o print e a legenda diz o que é e qual
modelo está por trás. É a resposta ao feedback da Sprint 3: "faltou detalhar o
funcionamento visual, prints funcionais do MVP em si".

Coordenadas em porcentagem da área da imagem (3200 × 2000), medidas olhando o print.
"""
from __future__ import annotations

import re

# (arquivo do print, sobrancelha, título, legenda, quem usa, no dia a dia)
TELAS = [
    ("01-panorama", "Aba Panorama", "O dia em uma tela",
     "O previsto para a hora contra o registrado, em <b>P3 e P2</b>. Abaixo, os casos de "
     "maior risco agora e as duas metas do ano.",
     "A coordenação de operações, na primeira meia hora do dia.",
     "Compara o que já entrou com o que o modelo esperava para a hora e decide se o dia "
     "pede reforço. É a única tela que responde as duas perguntas juntas."),
    ("07-modal-briefing", "Panorama · resumo automático", "O resumo do início do dia",
     "Abre sozinho na entrada da ferramenta, com ontem, hoje e onde agir. É gerado da "
     "saída dos modelos: <b>o Cronos empurra o insight, não espera pergunta</b>.",
     "O gestor de operações, antes da primeira reunião.",
     "Lê o resumo já escrito e leva a leitura pronta para a reunião. Não precisa abrir "
     "aba, filtrar período nem pedir relatório a ninguém."),
    ("02-previsao", "Aba Previsão", "Quantos incidentes nos próximos dias?",
     "Saída do Prophet. Trinta dias medidos emendados em duas semanas previstas, cada dia "
     "como <b>intervalo</b>, e não como número único.",
     "Quem dimensiona a equipe da semana.",
     "Escala pelo topo do intervalo, não pela média, e vê a diferença entre P2 e P3 antes "
     "de distribuir gente. A largura do intervalo é a medida da dúvida do modelo."),
    ("03-projecao", "Aba Projeção", "Onde o ano fecha",
     "As violações acumuladas somadas ao risco da fila aberta e ao volume que ainda entra. "
     "<b>P3 projeta 208 e fica dentro do limite; P2 projeta 43 e passa de 39</b>.",
     "O gerente responsável pelo indicador anual.",
     "Acompanha, a cada mês, se o ano fecha dentro do limite nas duas prioridades. É a "
     "informação que hoje só aparece na apuração de dezembro."),
    ("10-modal-meta", "Projeção · régua da meta", "Como a meta é medida",
     "Os seis degraus da meta anual, direto do dicionário de dados da Locaweb. <b>O Cronos "
     "não define a régua</b>: ele diz em que degrau o ano está e em qual deve terminar.",
     "O mesmo gerente, quando precisa justificar a leitura.",
     "Confere degrau por degrau de onde saiu o veredito da tela anterior. A régua é a "
     "oficial da Locaweb, e a folha existe para que a conta não fique numa caixa fechada."),
    ("04-fila", "Aba Fila", "Em qual caso olhar primeiro",
     "Os 49 casos abertos às 15h, ordenados do maior risco para o menor pela regressão "
     "logística, cada um com o <b>fator que mais pesa</b> e o item de configuração.",
     "O analista de operações que está com a fila na mão.",
     "Percorre de cima para baixo até o limite de casos que consegue revisar no dia. Nos "
     "50 primeiros da avaliação, encontra 13 das 50 violações; por prioridade, nenhuma."),
    ("08-modal-escore", "Fila · explicabilidade", "Por que este caso e não outro",
     "A decomposição da pontuação: cada sinal entra como <b>peso vezes desvio da "
     "média</b>, e a soma reconstrói o valor exato. Modelo linear é explicável por "
     "construção.",
     "O mesmo analista, antes de agir sobre o caso.",
     "Lê quais sinais empurraram o incidente para o topo e decide o que fazer com essa "
     "informação. Sem isso, a ordenação seria uma instrução sem argumento."),
    ("05-saude", "Aba Saúde", "Que produto está pior",
     "Nota de 0 a 100 nos 15 produtos, com o componente que mais penaliza cada um e as "
     "colunas de <b>P3 e P2 separadas</b>.",
     "A liderança de produto, na revisão semanal.",
     "Compara os 15 produtos numa escala só e leva o pior da lista para a pauta. As duas "
     "prioridades aparecem em colunas próprias, porque cada uma tem meta própria."),
    ("09-modal-produto", "Saúde · detalhe do produto", "O que forma a nota",
     "Os cinco componentes da nota e quanto cada um pesa, com o histórico do produto. É o "
     "que separa <b>viola muito</b> de <b>vai começar a violar</b>.",
     "Quem responde pelo produto apontado.",
     "Vê qual dos cinco componentes puxa a nota para baixo e onde investir esforço. A nota "
     "sozinha diz que há problema; a decomposição diz qual é."),
    ("06-causas", "Aba Causas", "O que compensa prevenir",
     "Códigos de fechamento ordenados por <b>taxa de violação, não por volume</b>: é assim "
     "que aparece a causa pequena que viola muito.",
     "Quem decide ação preventiva e projeto de melhoria.",
     "Escolhe onde atacar a causa raiz. A ordenação por volume levaria à falha mais "
     "frequente, que tem taxa de violação abaixo da média da base."),
]

# chave do print -> [(x%, y%, rótulo curto, modelo ou fonte)]. Preenchido lote a lote.
BALOES: dict[str, list[tuple[float, float, str, str]]] = {t[0]: [] for t in TELAS}

FONTE = ('<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600'
         '&family=Outfit:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')

# base.css e o print vistos de prototipos/slides/sprint4/_build/, quatro níveis abaixo da raiz
BASE_CSS = "../../mvp/abertura/base.css"
PRINTS = "../../../../sprints/sprint-3/prints"

MOLDE = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>{titulo}</title>
{fonte}<link rel="stylesheet" href="{base}">
<style>
html,body{{margin:0;padding:0;background:#fff;overflow:hidden}}
.pk .body{{padding:0;flex-direction:row;align-items:center;gap:24px}}
.pk .lado{{width:318px;flex-shrink:0;padding-left:26px}}
.pk .marca{{display:flex;align-items:center;gap:9px}}
.pk .marca .bi2{{width:30px;height:30px;border-radius:8px;background:var(--ink);display:flex;
  align-items:center;justify-content:center}}
.pk .marca .bi2 svg{{width:17px;height:17px}}
.pk .marca span{{font-size:16px;font-weight:800;letter-spacing:-.3px;color:#000}}
.pk .kk{{font-size:11.5px;font-weight:700;letter-spacing:2.4px;text-transform:uppercase;
  color:var(--accent);margin-top:26px}}
.pk h1{{font-size:29px;font-weight:800;letter-spacing:-1.05px;line-height:1.1;color:var(--head);
  margin-top:9px}}
.pk .cap2{{font-size:13.5px;line-height:1.5;color:var(--tx);margin-top:12px}}
.pk .cap2 b{{color:var(--head);font-weight:700}}
/* a legenda dos balões: o número no print e o número aqui são o mesmo objeto */
.pk .lg{{list-style:none;margin:16px 0 0;padding:14px 0 0;border-top:1px solid var(--line)}}
.pk .lg:empty{{display:none}}
.pk .lg li{{display:flex;gap:10px;align-items:flex-start;font-size:12.5px;line-height:1.4;
  color:var(--tx);padding:5px 0}}
.pk .lg li b{{color:var(--head);font-weight:700}}
.pk .lg li i{{display:block;font-style:normal;font-size:11px;color:var(--accent);
  font-family:var(--mono);margin-top:2px}}
.pk .lg .n,.pk .bal{{width:22px;height:22px;border-radius:50%;background:var(--accent);color:#fff;
  font-size:12px;font-weight:800;display:inline-flex;align-items:center;justify-content:center;
  flex-shrink:0;font-family:var(--font)}}
.pk .uso{{margin-top:14px;padding-top:12px;border-top:1px solid var(--line)}}
.pk .uk{{font-size:10.5px;font-weight:700;letter-spacing:1.7px;text-transform:uppercase;
  color:var(--accent)}}
.pk .uso p{{font-size:12.5px;line-height:1.45;color:var(--tx);margin-top:4px}}
.pk .uso .uk+p+.uk{{margin-top:10px}}
.pk .pil{{display:inline-block;margin-top:16px;font-size:12px;font-weight:600;padding:7px 15px;
  border-radius:999px;background:#fff;border:1px solid var(--line);color:var(--accent);
  box-shadow:0 4px 14px -8px rgba(37,99,235,.3)}}
.pk .win{{position:relative;width:1206px;height:826px;flex-shrink:0;border-radius:14px;
  overflow:hidden;background:#fff;border:1px solid rgba(15,23,42,.14);
  box-shadow:0 -1px 0 rgba(255,255,255,.9) inset,0 54px 110px -44px rgba(15,23,42,.44),
  0 18px 40px -22px rgba(15,23,42,.22)}}
.pk .tabs{{height:32px;background:#D9E0EA;display:flex;align-items:flex-end;gap:9px;padding:0 14px}}
.pk .dots{{display:flex;gap:8px;flex-shrink:0;padding-bottom:9px}}
.pk .dots i{{width:11px;height:11px;border-radius:50%}}
.pk .dots i:nth-child(1){{background:#F2645A}}.pk .dots i:nth-child(2){{background:#F4BE4F}}
.pk .dots i:nth-child(3){{background:#5FC466}}
.pk .tab{{height:26px;background:#fff;border-radius:9px 9px 0 0;display:flex;align-items:center;
  gap:9px;padding:0 13px;font-size:12.5px;font-weight:600;color:#33415A;max-width:290px;
  white-space:nowrap}}
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
.pk .addr{{flex:1;max-width:720px;margin:0 auto;height:26px;background:#F1F4F8;border-radius:999px;
  display:flex;align-items:center;gap:9px;padding:0 15px;font-size:13px;color:#5C6B80;
  overflow:hidden;white-space:nowrap}}
.pk .addr svg{{width:13px;height:13px;stroke:#7C8AA0;fill:none;stroke-width:1.8;flex-shrink:0}}
.pk .addr .sch{{color:#9DAABB}} .pk .addr b{{color:#1F2937;font-weight:600}}
.pk .rgt{{display:flex;align-items:center;gap:14px;color:#7F8DA1;flex-shrink:0}}
.pk .rgt svg{{width:17px;height:17px;stroke:currentColor;fill:none;stroke-width:1.9;
  stroke-linecap:round;stroke-linejoin:round}}
.pk .rgt .av{{width:20px;height:20px;border-radius:50%;background:#E3E9F1;border:1px solid #D3DBE6}}
.pk .win img{{display:block;width:100%}}
/* os balões: posicionados em % da área da imagem, que começa depois das duas barras (72px) */
.pk .area{{position:absolute;left:0;right:0;top:72px;bottom:0;pointer-events:none}}
.pk .bal{{position:absolute;transform:translate(-50%,-50%);width:28px;height:28px;font-size:14px;
  box-shadow:0 0 0 3px #fff,0 6px 16px -6px rgba(37,99,235,.7)}}
.pk .ft{{left:26px;right:26px;bottom:9px}}
</style></head><body>
<section class="slide light pk">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="body">
    <div class="lado">
      <div class="marca"><span class="bi2"><svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" r="3" fill="none" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg></span><span>Cronos</span></div>
      <div class="kk">{eyebrow}</div>
      <h1>{titulo}</h1>
      <p class="cap2">{legenda}</p>
      <ol class="lg">{legenda_baloes}</ol>
      <div class="uso">
        <div class="uk">Quem usa</div><p>{quem}</p>
        <div class="uk">No dia a dia</div><p>{como}</p>
      </div>
      <span class="pil">A aplicação · {pos} de {total}</span>
    </div>
    <div class="win">
      <div class="tabs"><span class="dots"><i></i><i></i><i></i></span>
        <span class="tab"><span class="fav"><svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Cronos · Painel operacional<span class="x">&times;</span></span>
        <span class="plus">+</span></div>
      <div class="bar2">
        <span class="nav"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg><svg class="off" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg><svg viewBox="0 0 24 24"><path d="M20.5 12a8.5 8.5 0 1 1-2.6-6.1"/><path d="M20.5 4.5V10h-5.5"/></svg></span>
        <span class="addr"><svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8.5 11V8a3.5 3.5 0 0 1 7 0v3"/></svg><span class="sch">https://</span><b>{url}</b><span class="sch">/</span></span>
        <span class="rgt"><svg viewBox="0 0 24 24"><path d="M12 4l2.4 4.9 5.4.8-3.9 3.8.9 5.4-4.8-2.5-4.8 2.5.9-5.4L4.2 9.7l5.4-.8z"/></svg><span class="av"></span></span>
      </div>
      <img src="{prints}/{arquivo}.png" alt="{eyebrow}">
      <div class="area">{baloes}</div>
    </div>
  </div>
  <div class="ft"><span>Cronos · Super Data Bros · 2TSCOA</span><span>Challenge FIAP 2026 com Locaweb</span></div>
</section></body></html>
"""


def _tela(chave: str) -> tuple:
    try:
        return next(t for t in TELAS if t[0] == chave)
    except StopIteration:
        raise KeyError(f"tela desconhecida: {chave}") from None


def html_tela(chave: str, pos: int, total: int, url: str) -> str:
    arquivo, eyebrow, titulo, legenda, quem, como = _tela(chave)
    bs = BALOES.get(chave, [])
    baloes = "".join(f'<span class="bal" style="left:{x}%;top:{y}%">{i}</span>'
                     for i, (x, y, _, _) in enumerate(bs, 1))
    legenda_baloes = "".join(f'<li><span class="n">{i}</span><div><b>{r}</b><i>{m}</i></div></li>'
                             for i, (_, _, r, m) in enumerate(bs, 1))
    return MOLDE.format(fonte=FONTE, base=BASE_CSS, prints=PRINTS, arquivo=arquivo,
                        eyebrow=eyebrow, titulo=titulo, legenda=legenda, quem=quem, como=como,
                        pos=pos, total=total, url=url, baloes=baloes,
                        legenda_baloes=legenda_baloes)


def nota_tela(chave: str) -> str:
    t = _tela(chave)
    limpa = lambda s: re.sub(r"<[^>]+>", "", s)  # noqa: E731
    return f"{limpa(t[3])} Quem usa: {t[4]} No dia a dia: {t[5]}"


# ═════════════════════════════════════════════════════════════════════════════
# O par "tela inteira + destaques", no visual da banca
#
# Resposta ao feedback da Sprint 3 e ao pedido do Igor de 21/09: primeiro o
# print inteiro, com a explicação geral da página (o que responde, quem usa,
# quando, o que alimenta); depois um slide por destaque, com o recorte ampliado
# e anotações ligadas por linha aos pontos da própria imagem, mais uma frase de
# fecho dizendo o que se faz com aquilo na prática.
#
# Regiões e pontos em fração da imagem inteira (3200 × 2000), medidos olhando o
# print em tamanho real. Recorte largo e baixo usa a composição "wide": imagem
# em cima, anotações embaixo; os demais, imagem à esquerda e anotações à direita.
# ═════════════════════════════════════════════════════════════════════════════
# O par "tela inteira + destaques"
#
# Resposta ao feedback da Sprint 3 ("faltou detalhar o funcionamento visual,
# prints funcionais do MVP em si") e ao pedido do Igor de 21/09: primeiro o print
# inteiro com a explicação geral da página; depois um slide por destaque, com o
# recorte ampliado à direita e uma coluna de passos à esquerda, na ordem de
# leitura da tela. Sem fio puxado e sem contorno sobre a imagem: a ordem dos
# passos e o recorte é que fazem a ligação.
#
# A região de cada destaque vai em fração da imagem inteira (3200 × 2000),
# medida olhando o print em tamanho real.
# ═════════════════════════════════════════════════════════════════════════════
PRINT_W, PRINT_H = 3200, 2000
PALCO_W = 1472            # largura útil do corpo do slide
COL_W = 454               # largura da coluna de passos
GAP = 46                  # respiro entre a coluna e a imagem
ALT_MAX = 520             # altura máxima do recorte
ALT_MIN = 240             # abaixo disso a região cresce, para o recorte não virar uma tira

ICONES = {
    "curva": '<path d="M3 16.5c3.2 0 4.6-9 8.2-9 3.7 0 4.3 9 8.2 9"/><circle cx="19.4" cy="16.5" r="2.1"/>',
    "base": '<ellipse cx="12" cy="5.6" rx="7.4" ry="2.8"/><path d="M4.6 5.6v12.2c0 1.5 3.3 2.8 7.4 2.8s7.4-1.3 7.4-2.8V5.6"/><path d="M4.6 11.7c0 1.5 3.3 2.8 7.4 2.8s7.4-1.3 7.4-2.8"/>',
    "relogio": '<circle cx="12" cy="12" r="8.6"/><path d="M12 6.8V12l3.4 2"/>',
    "alvo": '<circle cx="12" cy="12" r="8.4"/><circle cx="12" cy="12" r="3.4"/><path d="M12 1.8v2.6M12 19.6v2.6M1.8 12h2.6M19.6 12h2.6"/>',
    "peso": '<path d="M4 20V9.5M10 20V4.5M16 20v-7M22 20V6.5"/>',
    "lista": '<path d="M4 6.5h4M4 12h4M4 17.5h4"/><path d="M11.5 6.5h8.5M11.5 12h8.5M11.5 17.5h8.5"/>',
    "balanca": '<path d="M12 3.4v17.2M6 20.6h12"/><path d="M4 8.6h16"/><path d="M4 8.6l-2.4 5.2a3.4 3.4 0 0 0 4.8 0z"/><path d="M20 8.6l2.4 5.2a3.4 3.4 0 0 1-4.8 0z"/>',
    "escada": '<path d="M3 20.4h5v-5h5v-5h5v-5h3"/>',
    "lupa": '<circle cx="10.6" cy="10.6" r="7"/><path d="M15.8 15.8L21 21"/>',
    "saude": '<path d="M20.4 6.6a5 5 0 0 0-8.4-1.8A5 5 0 0 0 3.6 6.6c-1.2 2.6.4 5.4 2.6 7.6L12 19.8l5.8-5.6c2.2-2.2 3.8-5 2.6-7.6z"/>',
    "seta": '<path d="M4 12h15"/><path d="M13.5 6.5L20 12l-6.5 5.5"/>',
    "calendario": '<rect x="3.4" y="5" width="17.2" height="15.6" rx="2.4"/><path d="M3.4 9.8h17.2M8.4 3v4M15.6 3v4"/>',
    "quem": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
}


def _ico(nome: str, classe: str = "ic") -> str:
    return (f'<svg class="{classe}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONES[nome]}</svg>')


def _p(ic: str, t: str, d: str, s: str) -> dict:
    """Um passo: ícone, título, uma linha de explicação e a fonte do dado."""
    return dict(ic=ic, t=t, d=d, s=s)


# a explicação geral de cada tela: o que ela responde, quem usa, quando, o que alimenta
TELA_META: dict[str, dict] = {
    "01-panorama": dict(
        lead="A primeira tela do dia. O previsto contra o registrado até agora, em <b>P3 e P2</b>, "
             "e embaixo os casos abertos de maior risco.",
        quem="Coordenação de operações", quando="Na primeira meia hora do dia",
        modelos="Prophet e regressão logística"),
    "07-modal-briefing": dict(
        lead="Abre sozinho às 07h, com o fechamento de ontem, a faixa prevista para hoje e os "
             "atalhos para a tela de cada assunto.",
        quem="O gestor de operações", quando="Antes da primeira reunião do dia",
        modelos="Prophet e base elegível ao KPI"),
    "02-previsao": dict(
        lead="Trinta dias medidos emendados em duas semanas previstas, cada dia como <b>intervalo</b> "
             "e não como número único, em <b>P3 e P2</b>.",
        quem="Quem dimensiona a equipe da semana", quando="No planejamento da semana",
        modelos="Prophet · sazonalidade semanal e feriados"),
    "03-projecao": dict(
        lead="Onde a meta anual deve fechar em <b>P3 e P2</b>, somando o realizado, o risco da fila "
             "aberta e o volume que ainda entra.",
        quem="O gerente responsável pelo indicador", quando="Na revisão mensal do indicador",
        modelos="Prophet, regressão logística e a régua da Locaweb"),
    "10-modal-meta": dict(
        lead="A escada de seis degraus do indicador, direto do dicionário da Locaweb, com o degrau "
             "de hoje e o degrau projetado.",
        quem="O mesmo gerente, ao justificar a leitura", quando="Quando a projeção precisa de prova",
        modelos="Dicionário de dados da Locaweb"),
    "04-fila": dict(
        lead="Os <b>49 casos abertos</b> até as 15h, do maior risco de estourar o prazo para o menor, "
             "cada um com o fator que mais pesa.",
        quem="O analista com a fila na mão", quando="Durante o dia, a cada caso novo",
        modelos="Regressão logística · risco por incidente"),
    "08-modal-escore": dict(
        lead="Por que um incidente está no topo: cada sinal com o peso que teve, e a frequência "
             "observada em casos parecidos.",
        quem="O mesmo analista, antes de agir", quando="Ao escolher o próximo caso",
        modelos="Regressão logística · pesos do modelo"),
    "05-saude": dict(
        lead="Nota de 0 a 100 nos <b>15 produtos</b>, com o componente que mais penaliza cada um e as "
             "colunas de <b>P3 e P2</b> separadas.",
        quem="A liderança de produto", quando="Na revisão semanal",
        modelos="Nota de saúde · cinco componentes"),
    "09-modal-produto": dict(
        lead="Os cinco componentes que formam a nota de um produto, com a posição relativa de cada "
             "um entre os quinze.",
        quem="Quem responde pelo produto apontado", quando="Depois que o produto entra na pauta",
        modelos="Nota de saúde · cinco componentes"),
    "06-causas": dict(
        lead="Códigos de fechamento ordenados por <b>taxa de violação, não por volume</b>: é assim que "
             "aparece a causa pequena que estoura muito.",
        quem="Quem decide ação preventiva", quando="No planejamento de melhoria",
        modelos="Base elegível ao KPI · 19.973 incidentes"),
}

# chave do print -> destaques; cada um com a região, o título, o fecho e os passos
DESTAQUES: dict[str, list[dict]] = {
    "01-panorama": [
        dict(x=.585, y=.070, w=.345, h=.210,
             titulo="Previsto para hoje e o fechamento de ontem",
             fecho="A coordenação lê em cinco segundos se o dia é normal ou pede reforço.",
             passos=[
                 _p("curva", "Previsto para hoje, em P3 e P2",
                    "77,4 no P3 e 15,8 no P2, cada um com o intervalo em que deve cair.",
                    "Prophet · faixa de 80%"),
                 _p("base", "Como ontem fechou",
                    "84 incidentes registrados e nenhum passou do prazo.",
                    "Base elegível ao KPI"),
                 _p("relogio", "Dias úteis seguidos sem violação",
                    "Quatro, contados até o corte do relógio do sistema.",
                    "Base elegível ao KPI"),
             ]),
        dict(x=.072, y=.295, w=.856, h=.380,
             titulo="O dia hora a hora, P3 e P2",
             fecho="Registrado abaixo da faixa é dia calmo; acima, é hora de olhar a fila.",
             passos=[
                 _p("base", "O que já entrou até as 15h",
                    "A linha cheia é o realizado do dia, acumulado hora a hora.",
                    "Registro da base"),
                 _p("curva", "O esperado para a hora, com a faixa",
                    "A tracejada e a faixa em volta dizem o que era esperado agora.",
                    "Prophet · curva por hora"),
                 _p("alvo", "O P2 ao lado, com meta própria",
                    "As duas prioridades entram no indicador, cada uma com a sua meta.",
                    "Prophet"),
             ]),
        dict(x=.072, y=.690, w=.856, h=.310,
             titulo="Onde agir agora",
             fecho="O topo da fila de risco sem sair do Panorama; a seta abre o detalhe do caso.",
             passos=[
                 _p("alvo", "Probabilidade de estourar o prazo",
                    "Cada caso aberto recebe a sua, e a lista ordena por ela.",
                    "Regressão logística"),
                 _p("peso", "O fator que mais pesa na pontuação",
                    "Produto, equipe ou hora de abertura, com o peso de cada um.",
                    "Explicabilidade do modelo"),
                 _p("lista", "A fila completa, 49 casos às 15h",
                    "O mesmo modelo, com filtro por faixa de risco e por prioridade.",
                    "Aba Fila de risco"),
             ]),
    ],
    "07-modal-briefing": [
        dict(x=.290, y=.415, w=.420, h=.250,
             titulo="Ontem e hoje, em duas linhas",
             fecho="O resumo chega às 07h sem que ninguém abra nada, e é onde o dia começa.",
             passos=[
                 _p("base", "O que fechou ontem",
                    "84 registrados, nenhum violou o prazo, e quatro dias úteis na sequência.",
                    "Base elegível ao KPI"),
                 _p("curva", "O que se espera hoje",
                    "De 59 a 96 no P3 e de 9 a 22 no P2, as duas prioridades juntas.",
                    "Prophet · faixa de 80%"),
                 _p("relogio", "O que já entrou até agora",
                    "40 no P3 e 9 no P2 às 15h, contra 53,1 e 10,9 previstos a esta altura.",
                    "Prophet · curva por hora"),
             ]),
        dict(x=.290, y=.655, w=.420, h=.120,
             titulo="De onde ele veio e para onde leva",
             fecho="O Cronos empurra o insight; quem opera não precisa pedir relatório a ninguém.",
             passos=[
                 _p("seta", "Três atalhos para a tela certa",
                    "Fila de risco, saúde por produto e o painel inteiro, a um toque.",
                    "Painel operacional"),
                 _p("base", "Gerado da saída dos modelos",
                    "Nenhum número é estimado na hora, e nenhuma consulta é feita pelo usuário.",
                    "Prophet e regressão logística"),
             ]),
    ],
    "02-previsao": [
        dict(x=.075, y=.075, w=.850, h=.262,
             titulo="Os números do dia e da semana",
             fecho="Quem escala a equipe usa o topo do intervalo, não a média.",
             passos=[
                 _p("curva", "Previsto para hoje no P3",
                    "77,4 incidentes, num intervalo de 59 a 96, com 40 registrados às 15h.",
                    "Prophet · faixa de 80%"),
                 _p("curva", "E no P2, na própria escala",
                    "15,8 incidentes, de 9 a 22, com 9 registrados às 15h.",
                    "Prophet · faixa de 80%"),
                 _p("calendario", "O dia mais cheio da semana",
                    "Terça 07/10, de 69 a 119 somando as duas prioridades.",
                    "Prophet · D+1 a D+7"),
             ]),
        dict(x=.075, y=.355, w=.850, h=.330,
             titulo="Trinta dias medidos, duas semanas previstas",
             fecho="A largura da faixa é a medida da dúvida do modelo, e ela cresce onde a semana é mais irregular.",
             passos=[
                 _p("base", "O histórico recente, em preto",
                    "Trinta dias de registro até 30 de setembro, em cada prioridade.",
                    "Registro da base"),
                 _p("relogio", "O corte do relógio do sistema",
                    "1º de outubro às 15h: daí para a direita, tudo é previsão.",
                    "Corte em 01/10, 15h"),
                 _p("curva", "Duas semanas à frente, com a faixa",
                    "Cada dia sai como intervalo, e não como número único.",
                    "Prophet · faixa de 80%"),
             ]),
        dict(x=.075, y=.705, w=.850, h=.250,
             titulo="A base da previsão: o padrão da semana",
             fecho="O fim de semana entra com um terço do volume do dia útil, e o modelo já sabe disso.",
             passos=[
                 _p("calendario", "Dia útil no P3",
                    "Média entre 66 e 76 incidentes, de segunda a sexta.",
                    "Sazonalidade semanal"),
                 _p("calendario", "Fim de semana no P3",
                    "Cai para 34 no sábado e 18 no domingo.",
                    "Sazonalidade semanal"),
                 _p("alvo", "No P2 a semana é mais plana",
                    "De 17 a 14 nos dias úteis, 11 e 9 no fim de semana.",
                    "Sazonalidade semanal"),
             ]),
    ],
    "03-projecao": [
        dict(x=.076, y=.236, w=.848, h=.390,
             titulo="Onde o ano está e onde deve fechar",
             fecho="É a leitura que hoje só aparece na apuração de dezembro.",
             passos=[
                 _p("base", "O que já aconteceu no ano",
                    "145 violações no P3 e 33 no P2, até 30 de setembro.",
                    "Base elegível ao KPI"),
                 _p("balanca", "O limite de cada prioridade",
                    "263 no P3 e 39 no P2: acima disso o atingimento cai para 75%.",
                    "Dicionário de dados da Locaweb"),
                 _p("curva", "A projeção para dezembro",
                    "208 no P3, dentro do limite, e 43 no P2, acima dele.",
                    "Projeção da meta"),
             ]),
        dict(x=.076, y=.452, w=.848, h=.152,
             titulo="A conta aberta e o veredito",
             fecho="A conta fica à vista: o Cronos não pede que se acredite no número, ele mostra de onde ele veio.",
             passos=[
                 _p("peso", "As três parcelas da soma",
                    "O que já aconteceu, mais o risco da fila aberta, mais o volume que ainda entra.",
                    "Prophet e regressão logística"),
                 _p("balanca", "O veredito por prioridade",
                    "P3 fica dentro dos 100% com 22,0 de folga; P2 passa por 4,5 violações.",
                    "Projeção da meta"),
             ]),
    ],
    "10-modal-meta": [
        dict(x=.310, y=.356, w=.380, h=.082,
             titulo="A nota de hoje e a projetada",
             fecho="A meta é invertida: quanto menos violação, maior a nota. A folha aberta é a do P3; o P2 tem a sua, com os mesmos seis degraus.",
             passos=[
                 _p("base", "O que já aconteceu",
                    "145 violações no P3 até o corte de 30 de setembro.",
                    "Base elegível ao KPI"),
                 _p("balanca", "A nota de hoje e a do fim do ano",
                    "150% com o realizado de agora, 125% com a projeção até dezembro.",
                    "Projeção da meta"),
             ]),
        dict(x=.310, y=.430, w=.380, h=.242,
             titulo="A escada de seis degraus",
             fecho="O Cronos não define a régua: ele diz em que degrau o ano está e em qual deve terminar, no P3 e no P2.",
             passos=[
                 _p("escada", "Seis degraus, do dicionário oficial",
                    "Até 200 vale 150%; de 201 a 230, 125%; de 231 a 263, 100%; daí para cima cai.",
                    "Dicionário de dados da Locaweb"),
                 _p("relogio", "Onde o ano está agora",
                    "145 violações colocam o P3 no primeiro degrau.",
                    "Base elegível ao KPI"),
                 _p("curva", "Onde ele deve terminar",
                    "208 projetadas levam para o segundo degrau, ainda acima da meta contratada.",
                    "Projeção da meta"),
             ]),
    ],
    "04-fila": [
        dict(x=.075, y=.245, w=.850, h=.200,
             titulo="O topo da fila, em P3 e P2",
             fecho="O maior risco do dia é da prioridade 3, e é lá que a fila começa, não na prioridade mais alta.",
             passos=[
                 _p("alvo", "O maior risco de hoje",
                    "8,1% no P3, que é 8,6 vezes a média da base.",
                    "Regressão logística"),
                 _p("lista", "O caso que está no topo",
                    "INC8552480, produto lsin, equipe Team10, aberto às 15h.",
                    "Fila às 15h"),
                 _p("alvo", "E o topo do P2",
                    "1,2%, que é 1,3 vez a média: a fila do P2 está mais calma hoje.",
                    "Regressão logística"),
             ]),
        dict(x=.075, y=.465, w=.850, h=.535,
             titulo="A fila completa, do maior risco para o menor",
             fecho="Nos 50 primeiros da avaliação o modelo encontra 13 das 50 violações; ordenando por prioridade, nenhuma.",
             passos=[
                 _p("peso", "Quatro faixas, com a contagem de hoje",
                    "Nenhum crítico, 4 altos, 11 em atenção e 34 de rotina.",
                    "Faixas de risco"),
                 _p("alvo", "Ordenada do maior risco para o menor",
                    "É a ordem em que a fila deve ser percorrida, e não a da prioridade.",
                    "Regressão logística"),
                 _p("lupa", "O fator que mais pesa em cada caso",
                    "Produto, equipe ou subcategoria, com a participação na pontuação.",
                    "Explicabilidade do modelo"),
             ]),
    ],
    "08-modal-escore": [
        dict(x=.310, y=.186, w=.380, h=.186,
             titulo="O incidente e o risco dele",
             fecho="Quem abre a folha já sabe de que caso se trata e o quanto ele foge da média.",
             passos=[
                 _p("lista", "Quem é o incidente",
                    "INC8552480, produto lsin, equipe Team10, item de configuração IC01977.",
                    "Fila às 15h"),
                 _p("alvo", "O risco estimado",
                    "8,1% de chance de estourar o prazo, contra 0,94% do incidente médio da base.",
                    "Regressão logística"),
             ]),
        dict(x=.310, y=.376, w=.380, h=.080,
             titulo="O que já aconteceu com casos iguais",
             fecho="A frequência observada é o que torna a probabilidade legível para quem opera.",
             passos=[
                 _p("base", "A leitura em cem casos",
                    "Em 100 casos parecidos, o modelo espera que 8 violem o prazo.",
                    "Regressão logística"),
                 _p("balanca", "A comparação com o caso comum",
                    "No incidente médio da base seriam 0,94 em 100.",
                    "Base elegível ao KPI"),
             ]),
        dict(x=.310, y=.466, w=.380, h=.276,
             titulo="O que pesa neste caso",
             fecho="Modelo linear é explicável por construção: a soma de todas as contribuições reconstrói o escore exato.",
             passos=[
                 _p("peso", "Cada sinal com o seu peso",
                    "Entre os seis sinais: produto lsin com 54,5%, subcategoria com 18,1%, equipe com 16,4%.",
                    "Explicabilidade do modelo"),
                 _p("lupa", "O que a lista cobre",
                    "Juntos, esses seis são 48% de toda a contribuição positiva do modelo.",
                    "Explicabilidade do modelo"),
                 _p("seta", "Para onde a folha leva",
                    "Os outros casos abertos do mesmo item de configuração, e a fila da equipe.",
                    "Painel operacional"),
             ]),
    ],
    "05-saude": [
        dict(x=.088, y=.074, w=.366, h=.314,
             titulo="A nota e a situação de cada produto",
             fecho="Quinze produtos numa escala só, o que o ranking por volume não entrega.",
             passos=[
                 _p("saude", "Nota de 0 a 100",
                    "Relativa ao conjunto: 100 seria o melhor dos quinze em todos os componentes.",
                    "Nota de saúde"),
                 _p("alvo", "Quatro situações possíveis",
                    "Estável, recorrente, risco latente e já materializado.",
                    "Nota de saúde"),
                 _p("lista", "Quem atende cada produto",
                    "A equipe dominante e a fatia do volume que ela responde.",
                    "Campo Grupo designado"),
             ]),
        dict(x=.466, y=.074, w=.460, h=.314,
             titulo="O que penaliza, e as duas prioridades",
             fecho="A nota sozinha diz que há problema; a coluna do componente diz qual é.",
             passos=[
                 _p("peso", "O componente que mais penaliza",
                    "Taxa de violação, problemas inéditos, duração mediana ou tendência.",
                    "Nota de saúde · cinco componentes"),
                 _p("alvo", "P3 e P2 em colunas próprias",
                    "Volume e violações de cada prioridade, porque cada uma tem meta própria.",
                    "Base elegível ao KPI"),
             ]),
        dict(x=.088, y=.826, w=.838, h=.130,
             titulo="O fim da lista é onde se age",
             fecho="A ordem da lista é a ordem da pauta da revisão semanal.",
             passos=[
                 _p("saude", "O pior dos quinze",
                    "lvps, nota 21,3, com taxa de violação de 2,9%, a maior do conjunto.",
                    "Nota de saúde"),
                 _p("lupa", "Dois vizinhos com causas diferentes",
                    "lcsp cai por fechamento sem causa; lrdo, por problemas inéditos.",
                    "Nota de saúde · cinco componentes"),
             ]),
    ],
    "09-modal-produto": [
        dict(x=.310, y=.204, w=.380, h=.186,
             titulo="O produto, a nota e a posição",
             fecho="Abrir um produto responde por que ele está onde está.",
             passos=[
                 _p("saude", "A nota e a posição no conjunto",
                    "lcho tem 69,3 e é o primeiro dos quinze produtos acompanhados.",
                    "Nota de saúde"),
                 _p("base", "O volume por trás da nota",
                    "431 incidentes elegíveis, dos quais 3 violaram o prazo.",
                    "Base elegível ao KPI"),
             ]),
        dict(x=.310, y=.394, w=.380, h=.244,
             titulo="Os cinco componentes da nota",
             fecho="É o que separa o produto que viola muito do produto que vai começar a violar.",
             passos=[
                 _p("peso", "Cinco medidas, cinco posições",
                    "Taxa de violação, problemas inéditos, fechados sem causa, duração e tendência.",
                    "Nota de saúde · cinco componentes"),
                 _p("lupa", "Quanto mais cheia a barra, pior",
                    "A barra é a posição relativa entre os quinze, e a nota é a média delas.",
                    "Nota de saúde"),
             ]),
        dict(x=.310, y=.634, w=.380, h=.084,
             titulo="A nota é relativa, não absoluta",
             fecho="Dizer isso na tela evita a leitura errada de que 100 significa produto sem problema.",
             passos=[
                 _p("balanca", "O que 100 significaria",
                    "Ser o melhor dos quinze em todos os cinco componentes, não a ausência de problemas.",
                    "Nota de saúde"),
             ]),
    ],
    "06-causas": [
        dict(x=.076, y=.226, w=.848, h=.098,
             titulo="O que a tela mede, e o que ela não faz",
             fecho="A tela é de diagnóstico, não de previsão, e diz isso antes de mostrar o primeiro número.",
             passos=[
                 _p("lupa", "Códigos de fechamento, por taxa",
                    "19.973 elegíveis abertos até 30 de setembro; os 19.745 com código formam a tabela.",
                    "Base elegível ao KPI"),
                 _p("relogio", "Preenchido só no encerramento",
                    "Por isso o campo não prevê o caso de hoje, e a tela avisa.",
                    "Campo Código de fechamento"),
             ]),
        dict(x=.076, y=.316, w=.848, h=.266,
             titulo="As causas que mais estouram o prazo",
             fecho="Ordenar por taxa é o que faz a causa pequena de alto risco aparecer.",
             passos=[
                 _p("peso", "Ordenadas por taxa de violação",
                    "Falha de Hardware lidera com 8,24%, em apenas 85 incidentes.",
                    "Base elegível ao KPI"),
                 _p("alvo", "A taxa de cada prioridade ao lado",
                    "Em Falha de Hardware, 4,35% no P3 contra 9,68% no P2.",
                    "Base elegível ao KPI"),
                 _p("lupa", "O volume fica à vista",
                    "A coluna de incidentes mostra que a ordenação não é por tamanho.",
                    "Base elegível ao KPI"),
             ]),
        dict(x=.076, y=.668, w=.848, h=.092,
             titulo="A causa mais frequente não é a que mais estoura",
             fecho="Priorizar por volume levaria a atacar o que já está sob controle.",
             passos=[
                 _p("base", "Falha de Aplicação, a maior em volume",
                    "12.041 incidentes, seis de cada dez da base recortada.",
                    "Base elegível ao KPI"),
                 _p("alvo", "E uma das menores em taxa",
                    "0,82% de violação, abaixo da média e dez vezes menor que a do topo.",
                    "Base elegível ao KPI"),
             ]),
    ],
}

# quantas telas são abas (as folhas de detalhe não contam na numeração "tela N de 6")
ABAS = [t for t in TELAS if not t[0].split("-", 1)[1].startswith("modal")]

LOGO_CLARO = ('<svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" '
              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" '
              'r="3" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg>')

CSS_INTEIRA = """
/* ══ tela inteira: a explicação geral à esquerda, o print grande à direita ══ */
.tli .body{padding-top:14px}
.tli .cena{flex:1;min-height:0;display:flex;gap:34px;align-items:center}
.tli .lado{width:440px;flex-shrink:0;display:flex;flex-direction:column}
.tli .tt{font-size:44px;letter-spacing:-1.7px;line-height:1.06}
.tli .lead{font-size:16.5px;line-height:1.55;color:var(--tx);margin-top:16px}
.tli .lead b{color:var(--head);font-weight:700}
.tli .fatos{margin-top:22px;border-top:1px solid #DCE4EF}
.tli .fato{display:flex;align-items:center;gap:14px;padding:13px 0;border-bottom:1px solid #DCE4EF}
.tli .fato .ic{width:20px;height:20px;color:var(--accent);flex-shrink:0}
.tli .fato .k{font-size:10.5px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
  color:var(--tx2)}
.tli .fato .v{font-size:15px;font-weight:600;color:var(--head);margin-top:2px}
.tli .palco3{flex:1;min-width:0;display:flex;justify-content:flex-end;align-items:center}
.tli .tela{width:980px;border-radius:14px;overflow:hidden;border:1px solid #D6DEE9;background:#fff;
  box-shadow:0 60px 120px -50px rgba(15,23,42,.55),0 0 0 1px rgba(15,23,42,.03)}
.tli .tela img{display:block;width:100%}
"""

CSS_RECORTE = """
/* ══ um destaque: passos à esquerda, recorte ampliado à direita ══
   Sem fio e sem contorno sobre a imagem: os passos entram na ordem de leitura
   da tela, e o recorte mostra só a parte de que eles falam. ══ */
.tlr .body{padding-top:14px}
.tlr .cena{flex:1;min-height:0;display:flex;gap:46px;align-items:center}
.tlr .lado{width:454px;flex-shrink:0;display:flex;flex-direction:column}
.tlr .tt{font-size:38px;letter-spacing:-1.4px;line-height:1.1}
.tlr .passos{margin-top:22px}
.tlr .ps{display:flex;gap:16px;padding:15px 0;align-items:flex-start}
.tlr .ps + .ps{border-top:1px solid #DCE4EF}
.tlr .ps .chip{width:42px;height:42px;border-radius:12px;background:var(--accent-l);
  border:1px solid #BFDBFE;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.tlr .ps .chip .ic{width:21px;height:21px;color:var(--accent)}
.tlr .ps b{display:block;font-size:16.5px;font-weight:700;color:var(--head);letter-spacing:-.25px;
  line-height:1.3}
.tlr .ps p{font-size:14px;line-height:1.45;color:var(--tx);margin-top:5px}
.tlr .ps i{display:block;font-style:normal;font-family:var(--mono);font-size:11.5px;
  color:var(--accent);margin-top:7px}
.tlr .fecho{display:flex;align-items:flex-start;gap:12px;margin-top:18px;padding-top:16px;
  border-top:1px solid #DCE4EF;font-size:15.5px;line-height:1.45;color:var(--tx)}
.tlr .fecho .ic{width:20px;height:20px;color:var(--accent);margin-top:2px;flex-shrink:0}
.tlr .fecho b{color:var(--head);font-weight:700}
.tlr .palco4{flex:1;min-width:0;display:flex;justify-content:flex-end;align-items:center}
.tlr .crop{border-radius:14px;border:1px solid #D6DEE9;background-repeat:no-repeat;
  background-color:#fff;box-shadow:0 40px 90px -46px rgba(15,23,42,.55)}
"""


def _fato(chave_icone: str, k: str, v: str) -> str:
    return (f'<div class="fato">{_ico(chave_icone)}<div><div class="k">{k}</div>'
            f'<div class="v">{v}</div></div></div>')


def secao_tela_inteira(chave: str, url: str = "") -> tuple[str, str]:
    """O print inteiro no visual da banca, com a explicação geral da página ao lado.

    `url` ficou sem uso quando o rodapé de procedência saiu, a pedido do Igor em
    21/09. O endereço da aplicação aparece uma vez, no slide de acesso.
    """
    arquivo, eyebrow, titulo, legenda, quem, _ = _tela(chave)
    meta = TELA_META.get(chave, dict(lead=legenda, quem=quem, quando="No dia", modelos=""))
    pos_aba = next((i for i, t in enumerate(ABAS, 1) if t[0] == chave), None)
    tag = f"Tela {pos_aba} de {len(ABAS)}" if pos_aba else "Folha de detalhe"
    fatos = _fato("quem", "Quem usa", meta["quem"]) + _fato("relogio", "Quando", meta["quando"])
    if meta.get("modelos"):
        fatos += _fato("peso", "O que alimenta", meta["modelos"])
    return f"""<section class="slide light tli" data-slide="0" data-var="a">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="hd"><div class="bi">{LOGO_CLARO}</div><div class="bn">Cronos</div><div class="tag">{tag}</div></div>
  <div class="body">
    <div class="cena">
      <div class="lado">
        <span class="eb"><span class="rv" style="--d:240ms">A aplicação &middot; {eyebrow}</span></span>
        <h1 class="tt"><span class="mask" style="--d:340ms"><span>{titulo}</span></span></h1>
        <p class="lead rv" style="--d:700ms">{meta["lead"]}</p>
        <div class="fatos rv" style="--d:900ms">{fatos}</div>
      </div>
      <div class="palco3">
        <div class="tela rv3" style="--d:500ms" data-morph="{arquivo}" data-crop="0 0 1 1"><img src="{PRINTS}/{arquivo}.png" alt="{eyebrow}"></div>
      </div>
    </div>
  </div>
  <div class="ft"></div>
</section>""", CSS_INTEIRA


def secao_recorte(chave: str, idx: int, url: str = "") -> tuple[str, str]:
    """Um destaque: os passos à esquerda e o recorte ampliado à direita.

    `url` ficou sem uso junto com o rodapé de procedência.
    """
    arquivo, eyebrow, *_ = _tela(chave)
    regs = DESTAQUES[chave]
    r = regs[idx - 1]
    largura = PALCO_W - COL_W - GAP

    # Faixa larga e baixa vira uma tira sem presença no slide. Quando a altura cairia
    # abaixo do mínimo, a região cresce para cima e para baixo em torno do próprio
    # centro, até o recorte ganhar corpo. Isso traz as linhas vizinhas junto, o que
    # ajuda a situar o que está sendo mostrado.
    rw, rh, ry = r["w"], r["h"], r["y"]
    minima = ALT_MIN / largura * PRINT_W / PRINT_H
    if rh / rw < minima:
        centro = ry + rh / 2
        rh = min(rw * minima, 1.0)
        ry = min(max(centro - rh / 2, 0.0), 1.0 - rh)

    razao = (rh * PRINT_H) / (rw * PRINT_W)
    if largura * razao > ALT_MAX:
        largura = ALT_MAX / razao
    altura = largura * razao
    bx = 0 if rw >= 1 else r["x"] / (1 - rw) * 100
    by = 0 if rh >= 1 else ry / (1 - rh) * 100
    crop = (f'<div class="crop rv3" data-morph="{arquivo}" '
            f'data-crop="{r["x"]:.5f} {ry:.5f} {rw:.5f} {rh:.5f}" '
            f'style="--d:500ms;width:{largura:.0f}px;height:{altura:.0f}px;'
            f'background-image:url({PRINTS}/{arquivo}.png);'
            f'background-size:{100 / rw:.3f}% {100 / rh:.3f}%;'
            f'background-position:{bx:.3f}% {by:.3f}%"></div>')
    passos = "".join(
        f'<div class="ps rv" style="--d:{800 + k * 140}ms"><span class="chip">{_ico(p["ic"])}</span>'
        f'<div><b>{p["t"]}</b><p>{p["d"]}</p><i>{p["s"]}</i></div></div>'
        for k, p in enumerate(r["passos"]))
    return f"""<section class="slide light tlr" data-slide="0" data-var="a">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="hd"><div class="bi">{LOGO_CLARO}</div><div class="bn">Cronos</div>
    <div class="tag">Destaque {idx} de {len(regs)}</div></div>
  <div class="body">
    <div class="cena">
      <div class="lado">
        <span class="eb"><span class="rv" style="--d:240ms">{eyebrow}</span></span>
        <h1 class="tt"><span class="mask" style="--d:340ms"><span>{r["titulo"]}</span></span></h1>
        <div class="passos">{passos}</div>
        <div class="fecho rv" style="--d:{800 + len(r["passos"]) * 140}ms">{_ico("alvo")}<span>{r["fecho"]}</span></div>
      </div>
      <div class="palco4">{crop}</div>
    </div>
  </div>
  <div class="ft"></div>
</section>""", CSS_RECORTE


def nota_recorte(chave: str, idx: int) -> str:
    r = DESTAQUES[chave][idx - 1]
    passos = " ".join(f"{p['t']}: {p['d']} ({p['s']})" for p in r["passos"])
    return f"{r['titulo']}. {passos} {r['fecho']}"


# nome antigo, para o builder continuar enxergando a mesma coisa
RECORTES = DESTAQUES