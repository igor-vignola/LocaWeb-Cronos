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
    ("02-previsao", "Aba Previsão", "Quanto entra nos próximos dias",
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
