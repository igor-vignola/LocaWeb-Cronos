# Deck da Sprint 4 · plano de execução

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** gerar `sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx` com 59 slides no visual da banca, fala nas notas, mais um `deck.html` para revisão no navegador.

**Architecture:** um builder novo (`scripts/monta_deck_sprint4.py`) lê uma lista `ORDEM` de 59 itens de cinco tipos (slide da banca, slide do pitch, bloco próprio, divisória gerada, tela gerada, arquivo da Sprint 3), escreve um HTML autônomo por slide em `prototipos/slides/sprint4/_build/`, fotografa cada um em 1600×900 a 2× com a animação congelada no estado final, monta o `.pptx` com nota por slide e um visualizador de imagens. Bloco próprio cujo arquivo ainda não existe vira slide de espera "Aqui irá ficar: X", o que dá o esqueleto de graça.

**Tech Stack:** Python 3.13 no `.venv`, playwright (Chromium em `ms-playwright/chromium-1217`), python-pptx 1.0.2, Pillow. HTML e CSS no contrato de `prototipos/slides/ao-vivo/CONTRATO.md`.

**Spec:** `docs/superpowers/specs/2026-09-21-deck-sprint4-design.md`

## Global Constraints

- Visual: `prototipos/slides/ao-vivo/_estilo.css` em tudo o que nasce agora; blocos novos em `prototipos/slides/sprint4/blocos/NN-nome.html`, um `<style>` prefixado pela classe do slide e uma `<section class="slide light|dark xx">`, sem `data-quem`.
- Números só de `prototipos/slides/ao-vivo/CONTRATO.md` seção 5 e adendos 7.x. Erro da previsão escreve-se **4,2** e **11,8**. Violações de 2025: **42 de 39** no P2, **196 de 263** no P3. Base: **122.543** registros, **25.600** elegíveis (21%).
- P2 e P3 sempre juntos em todo slide novo. Proibido: "turno", travessão, emoji, ARIMA, SARIMA, Streamlit, DTW, cascata, acúmulo, qualquer realizado posterior a 01/10/2025 15h em tela.
- Endereços: aplicação `igor-vignola.github.io/LocaWeb-Cronos`, vídeo `youtu.be/IeWLVBD0Jas`, repositório `github.com/igor-vignola/LocaWeb-Cronos`.
- Texto: título curto que nomeia o assunto; nada de fragmento com pausa, antítese de dois tempos, vocabulário de IA (crucial, robusto, elevar, garantir como enfeite). Sobre fundo escuro, texto de leitura em `#B7C0CB` ou mais claro; corpo mínimo 12,5px.
- Revisão pelo Igor em lotes de três slides de trabalho, do início ao fim, abrindo `deck.html` no navegador dele (Opera) com `Start-Process`. Nenhum lote começa antes do anterior ser aprovado.
- Commits em PT-BR, Conventional Commits, acentos obrigatórios, sem escopo entre parênteses, terminando em `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Todo slide novo passa por: PNG olhado sozinho em 1600×900 (ferramenta Read), medição de fora do palco e invisível, varredura de texto.

---

## Estrutura de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `scripts/monta_deck_sprint4.py` | **reescrito.** `ORDEM`, leitura das fontes, ajustes e linhas de apoio, slide de espera, HTML por slide, render, notas, `.pptx`, `deck.html`, varredura |
| `scripts/deck_sprint4_telas.py` | **novo.** `TELAS` (dez capturas: texto de uso real), `BALOES` (coordenadas por print), molde da tela na forma A com balões e legenda numerada |
| `prototipos/slides/sprint4/blocos/NN-nome.html` | **novos.** os 13 slides de conteúdo e a divisória-molde, no contrato da banca |
| `prototipos/slides/sprint4/_build/` | gerado, não versionado: um HTML autônomo por slide |
| `prototipos/slides/sprint4/_png/` | gerado: um PNG por slide, 3200×1800 |
| `prototipos/slides/sprint4/deck.html` | gerado: visualizador das imagens |
| `sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx` | a entrega |

Saem do repositório: os 42 HTML antigos em `prototipos/slides/sprint4/` e os PNG de `_png/` da numeração antiga. Ficam `_comparar.py` e saídas até o lote 1 fechar.

---

### Task 1 · Esqueleto: builder novo com slides de espera

**Files:**
- Modify (reescrever): `scripts/monta_deck_sprint4.py`
- Create: `scripts/deck_sprint4_telas.py`
- Delete: `prototipos/slides/sprint4/[0-9][0-9]-*.html`, `prototipos/slides/sprint4/_png/[0-9][0-9]-*.png`
- Modify: `.gitignore` (adicionar `prototipos/slides/sprint4/_build/`)

**Interfaces:**
- Produces: `ORDEM: list[tuple[str, object, str]]` com itens `("banca", n, nome)`, `("pitch", "objetivo", nome)`, `("bloco", nome, nome)`, `("div", n_bloco, nome)`, `("tela", chave, nome)`, `("arquivo", Path, nome)`. `ESPERA: dict[nome, (titulo, conteudo, origem)]`. `AJUSTES: dict[int, list[tuple[str, str]]]`. `APOIO: dict[int, str]`. `NOTAS: dict[nome, str]`. Funções `main()`, `render(caminhos)`, `monta_pptx(pngs, notas)`, `escreve_viewer(itens)`, `varredura(secoes)`.
- Consumes de `deck_sprint4_telas.py`: `TELAS: list[tuple]`, `BALOES: dict[str, list[tuple[float, float, str, str]]]`, `html_tela(chave, pos, total, url) -> str`, `nota_tela(chave) -> str`.

- [ ] **Step 1: Tirar do índice os arquivos gerados pelo builder antigo**

```bash
cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb"
git rm -q prototipos/slides/sprint4/[0-9][0-9]-*.html prototipos/slides/sprint4/_png/[0-9][0-9]-*.png
printf '\n# HTML autônomo por slide, regerado pelo builder\nprototipos/slides/sprint4/_build/\n' >> .gitignore
git status --short | head
```
Expected: 42 `D` de HTML, 42 `D` de PNG, `M .gitignore`.

- [ ] **Step 2: Escrever `scripts/deck_sprint4_telas.py`**

O `TELAS` vem do builder antigo (dez tuplas: arquivo, sobrancelha, título, legenda, quem, como). `BALOES` começa vazio para as dez chaves; os lotes 3 a 6 preenchem. O molde é o `MODELO_TELA` antigo com três acréscimos: `.win{position:relative}`, os balões `<span class="bal" style="left:X%;top:Y%">N</span>` sobre a imagem, e a legenda `<ol class="lg">` na coluna da esquerda.

```python
# -*- coding: utf-8 -*-
"""As dez capturas da aplicação, na forma A da Sprint 3, com balões numerados.

Cada balão aponta uma funcionalidade sobre o print e a legenda diz o que é e qual
modelo está por trás. É a resposta ao feedback da Sprint 3: "faltou detalhar o
funcionamento visual, prints funcionais do MVP em si".

Coordenadas em porcentagem da imagem (3200 × 2000), medidas olhando o print.
"""
from __future__ import annotations

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
.pk .lg{{list-style:none;margin-top:16px;padding-top:14px;border-top:1px solid var(--line)}}
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
.pk .area{{position:absolute;left:0;right:0;top:72px;bottom:0}}
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


def html_tela(chave: str, pos: int, total: int, url: str) -> str:
    t = next(t for t in TELAS if t[0] == chave)
    arquivo, eyebrow, titulo, legenda, quem, como = t
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
    t = next(t for t in TELAS if t[0] == chave)
    import re
    limpa = lambda s: re.sub(r"<[^>]+>", "", s)
    return f"{limpa(t[3])} Quem usa: {t[4]} No dia a dia: {t[5]}"
```

- [ ] **Step 3: Escrever `scripts/monta_deck_sprint4.py`**

```python
# -*- coding: utf-8 -*-
"""Monta o deck da Sprint 4 sobre o deck da banca de 15/09/2026.

Uma lista ORDEM de 59 itens, cinco tipos:
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
    .venv/Scripts/python scripts/monta_deck_sprint4.py --so 5 6   # só as posições 5 e 6
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from deck_sprint4_telas import TELAS, html_tela, nota_tela  # noqa: E402

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


def _nomes_banca() -> dict[int, str]:
    return {int(p.name[:2]): p.stem.split("-", 1)[1] for p in (AO_VIVO / "blocos").glob("[0-9][0-9]-*.html")}


NB = _nomes_banca()

ORDEM: list[tuple[str, object, str]] = (
    [("banca", 1, "capa"), ("div", 1, "div-bloco-1"), ("banca", 2, "equipe"), ("banca", 3, "cronos"),
     ("bloco", "descricao", "descricao"),
     ("div", 2, "div-bloco-2"), ("banca", 4, "prazo"), ("banca", 5, "quebras"), ("banca", 6, "fila-ordem"),
     ("div", 3, "div-bloco-3"), ("pitch", "objetivo", "objetivo"),
     ("div", 4, "div-bloco-4"), ("bloco", "abordagem", "abordagem")]
    + [("banca", n, NB[n]) for n in range(7, 31)]
    + [("arquivo", ABERTURA / "12-codigo-C.html", "codigo-fonte"),
       ("div", 5, "div-bloco-5"), ("banca", 31, "aplicacao"), ("bloco", "mapa-abas", "mapa-abas")]
    + [("tela", t[0], f"tela-{i:02d}-{t[0]}") for i, t in enumerate(TELAS, 1)]
    + [("banca", 33, "acesso"),
       ("bloco", "video", "video"),
       ("div", 7, "div-bloco-7"), ("bloco", "sintese", "sintese"), ("bloco", "aprendizados", "aprendizados"),
       ("bloco", "limitacoes", "limitacoes"), ("bloco", "proximos-passos", "proximos-passos"),
       ("banca", 32, "obrigado")]
)
assert len(ORDEM) == 59, len(ORDEM)

# ── o que cada posição nova vai ter, para o slide de espera ───────────────────
# nome -> (título curto, o que o slide traz, origem do material)
ESPERA: dict[str, tuple[str, str, str]] = {
    "descricao": ("Descrição resumida da solução", "Dois parágrafos: o que o Cronos lê, as três respostas que devolve, e como isso é publicado.", "novo, texto do rascunho conferido no CONTRATO"),
    "abordagem": ("A abordagem de trabalho", "Quatro entregas nas datas da FIAP, hipótese só vira produto com teste no dado, e as duas fontes de dados: a planilha da Locaweb e o calendário de feriados.", "novo"),
    "mapa-abas": ("Mapa da aplicação", "As seis abas e as quatro folhas de detalhe, o que cada uma responde e qual modelo a alimenta.", "novo"),
    "video": ("Link do vídeo pitch", f"O endereço {URL_VIDEO}, cinco minutos, hands on, acesso público.", "novo"),
    "sintese": ("Síntese dos resultados", "O erro da previsão, a fila de risco, a projeção da meta e a aplicação, com os números da banca.", "novo"),
    "aprendizados": ("Aprendizados-chave", "Volume não prevê quebra, o alvo é raro, modelo interpretável sem perda, o campo oficial vale mais que a regra reescrita.", "novo"),
    "limitacoes": ("Limitações enfrentadas", "Cobertura do intervalo no P3, rótulo que só existe após o fechamento, um ano de dado denso, sem custo por violação, resumo ainda sem modelo de linguagem.", "novo"),
    "proximos-passos": ("Próximos passos", "Ler da base interna, reajuste semanal, alarme de calibração, texto do resumo pela Claude API, custo por violação com a Locaweb.", "novo"),
}
for n in (1, 2, 3, 4, 5, 7):
    ESPERA[f"div-bloco-{n}"] = (f"Divisória do bloco {n}", f"Abre o bloco «{BLOCO_NOME[n]}» do template. Desenho próprio, diferente da divisória de seção da banca.", "novo, desenho escolhido no lote 1")
for i, t in enumerate(TELAS, 1):
    ESPERA[f"tela-{i:02d}-{t[0]}"] = (f"{t[1]}: {t[2]}", "Print da aplicação com balões numerados apontando cada funcionalidade e legenda dizendo qual modelo está por trás.", "forma A da Sprint 3, refeita com balões")

# ── ajustes de texto nos slides da banca ──────────────────────────────────────
AJUSTES: dict[int, list[tuple[str, str]]] = {
    2: [("Quem apresenta", "A equipe")],
    31: [("Demonstração ao vivo", "Demonstração da solução")],
}
# linha de apoio abaixo do título, só onde o título sozinho não fecha a mensagem.
# Proposta ao Igor no lote 2; entra aqui depois de aprovada.
APOIO: dict[int, str] = {}

# notas dos slides novos; os da banca vêm do roteiro, as telas do texto de uso real
NOTAS: dict[str, str] = {}

# ── CSS do builder: congelamento, linha de apoio, slide de espera ─────────────
CSS_BUILDER = """
html,body{margin:0;padding:0;background:#fff;overflow:hidden}
.palco{width:1600px;height:900px;position:relative;overflow:hidden}
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
            f'<body><div class="palco">{secao}</div></body></html>')


def resolve_contadores(texto: str) -> str:
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
        raise SystemExit(f"{arquivo.name}: nenhuma <section class=\"slide ...\">")
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
    return resolve_contadores(secao), css


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
    secao, css = secao_e_css(molde)
    return secao.replace("{N}", f"{n_bloco:02d}").replace("{NOME}", BLOCO_NOME[n_bloco]), css


def escreve_build() -> list[tuple[int, str, Path, int]]:
    """Um HTML por slide em _build/. Devolve (posição, nome, caminho, bloco)."""
    BUILD.mkdir(parents=True, exist_ok=True)
    for velho in BUILD.glob("*.html"):
        velho.unlink()
    itens, bloco = [], 1
    for pos, (tipo, ref, nome) in enumerate(ORDEM, 1):
        if tipo == "div":
            bloco = int(ref)
        if nome == "video":
            bloco = 6
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
        elif tipo == "tela":
            pos_tela = int(nome.split("-")[1])
            html = html_tela(str(ref), pos_tela, len(TELAS), URL_APP)
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


def render(itens: list[tuple[int, str, Path, int]], so: set[int] | None) -> list[Path]:
    from playwright.sync_api import sync_playwright
    PNG.mkdir(parents=True, exist_ok=True)
    pngs = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=CHROME)
        pg = nav.new_context(viewport={"width": 1600, "height": 900}, device_scale_factor=2).new_page()
        for pos, nome, caminho, _ in itens:
            destino = PNG / f"{pos:02d}-{nome}.png"
            pngs.append(destino)
            if so and pos not in so and destino.exists():
                continue
            pg.goto(caminho.resolve().as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(450)
            pg.locator(".slide").first.screenshot(path=str(destino))
            avisos = pg.evaluate(MEDIDA)
            print(f"  {pos:02d} {nome:<28}" + ("  " + " | ".join(avisos) if avisos else ""))
        nav.close()
    return pngs


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
        else:
            saida[pos] = NOTAS.get(nome, "Em construção.")
    return saida


def monta_pptx(pngs: list[Path], notas_por_pos: dict[int, str]) -> None:
    from pptx import Presentation
    from pptx.util import Emu
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    branco = prs.slide_layouts[6]
    for pos, png in enumerate(pngs, 1):
        s = prs.slides.add_slide(branco)
        s.shapes.add_picture(str(png), 0, 0, width=prs.slide_width, height=prs.slide_height)
        s.notes_slide.notes_text_frame.text = notas_por_pos.get(pos, "")
    prs.save(PPTX)


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
        texto = re.sub(r"<[^>]+>", " ", texto)
        avisos = []
        if re.search(r"\bturno", texto, re.I): avisos.append("turno")
        if "—" in texto: avisos.append("travessão")
        if EMOJI.search(texto): avisos.append("emoji")
        tem_p3 = re.search(r"\bP3\b|prioridade 3", texto, re.I)
        tem_p2 = re.search(r"\bP2\b|prioridade 2", texto, re.I)
        if tem_p3 and not tem_p2: avisos.append("P3 sem P2")
        if avisos:
            problemas += 1
            print(f"  VARREDURA {pos:02d} {nome}: {', '.join(avisos)}")
    return problemas


def main() -> int:
    so = None
    if "--so" in sys.argv:
        so = {int(x) for x in sys.argv[sys.argv.index("--so") + 1:]}
    print("1/4 · HTML por slide")
    itens = escreve_build()
    esperas = sum(1 for _, n, c, _ in itens if c.parent == BUILD and 'class="slide light esp"' in c.read_text(encoding="utf-8"))
    print(f"     {len(itens)} slides, {esperas} de espera")
    print("2/4 · render")
    pngs = render(itens, so)
    print("3/4 · varredura de texto")
    varredura(itens)
    print("4/4 · notas, pptx e visualizador")
    ns = notas(itens)
    monta_pptx(pngs, ns)
    escreve_viewer(itens, pngs, ns)
    print(f"Pronto: {PPTX.name} ({len(pngs)} slides) · {VIEWER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Rodar o builder**

Run: `cd "C:/Users/igor.vignola/Documents/Personal/FIAP/Challenge-LocaWeb" && PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py`
Expected: `59 slides, 14 de espera` (6 divisórias + 8 blocos; as telas já saem na forma A, sem balões), 59 linhas de render sem `FORA DO PALCO`, varredura sem aviso nos slides da banca, `Pronto: ... (59 slides)`.

- [ ] **Step 5: Conferir o pptx e três PNG**

```bash
PYTHONUTF8=1 .venv/Scripts/python -c "
from pptx import Presentation
p=Presentation('sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx')
print(len(p.slides), p.slide_width, p.slide_height)
print(sum(1 for s in p.slides if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip()), 'com nota')
print(repr(p.slides[3].notes_slide.notes_text_frame.text[:120]))"
```
Expected: `59 12192000 6858000`, `59 com nota`, e a nota do slide 4 começa pela fala do slide 3 da banca ("Cronos" e "deus grego").

Olhar com a ferramenta Read: `_png/05-descricao.png` (espera), `_png/07-prazo.png` (banca, sem marcador de apresentador), `_png/42-tela-01-01-panorama.png` (forma A, sem balões ainda).

- [ ] **Step 6: Abrir para o Igor e registrar**

Run: `powershell -Command "Start-Process 'C:\Users\igor.vignola\Documents\Personal\FIAP\Challenge-LocaWeb\prototipos\slides\sprint4\deck.html'"`

Dizer a ele em duas linhas: 59 slides, setas para navegar, `N` mostra a nota, slides tracejados são os 24 que ainda vêm.

- [ ] **Step 7: Commit**

```bash
git add scripts/monta_deck_sprint4.py scripts/deck_sprint4_telas.py .gitignore prototipos/slides/sprint4/_png prototipos/slides/sprint4/deck.html sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx docs/superpowers
git commit -m "feat: refaz o deck da Sprint 4 sobre o deck da banca, com esqueleto de 59 slides

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2 · Lote 1: divisória de bloco, slide da equipe, descrição resumida

**Files:**
- Create: `prototipos/slides/sprint4/_comparar-divisoria.html` (temporário, via `_comparar.py`)
- Create: `prototipos/slides/sprint4/blocos/00-div-bloco.html` (molde com `{N}` e `{NOME}`)
- Create: `prototipos/slides/sprint4/blocos/05-descricao.html`
- Modify: `scripts/monta_deck_sprint4.py` (`NOTAS["descricao"]`, `NOTAS["div-bloco-N"]`)

**Interfaces:**
- Produces: molde `00-div-bloco.html` com os marcadores literais `{N}` (dois dígitos) e `{NOME}`, que `slide_div()` substitui.

- [ ] **Step 1: Duas propostas de divisória de bloco, ao lado da de seção da banca**

Acrescentar a `_comparar.py` uma terceira página `_comparar-divisoria.html` com três palcos: a divisória de seção 7 da banca (referência), a proposta **clara** e a proposta **escura**. Regras das duas: sem o painel de números à direita, título em duas linhas com o nome do bloco, o número do bloco como objeto dominante, e uma linha de uma frase dizendo o que o bloco cobre.

Clara: fundo `.light`, número «02» em 260px `font-weight:900` cor `var(--accent)` com opacidade .18 atrás do título, `.bl` "Bloco 02 de 07 · Template FIAP", título 84px `var(--head)`, linha 19px `var(--tx)`, rodapé com a lista dos sete blocos em caixa alta e o atual em azul.

Escura: fundo `.dark`, composição centralizada (não à esquerda como a de seção), número «02» em 120px `#60A5FA` acima do título, título 84px branco sem gradiente (o gradiente é assinatura da divisória de seção), linha 19px `#B7C0CB`, filete de 1px acima do rodapé e a lista dos sete blocos.

Rodar, olhar os três PNG com Read, abrir a página no Opera e perguntar ao Igor qual fica.

- [ ] **Step 2: Escrever o molde escolhido em `blocos/00-div-bloco.html`**

Estrutura do arquivo, com a composição vencedora dentro:

```html
<style>
/* ═══ divisória de bloco do template da Sprint 4 · molde ═══
   {N} e {NOME} são trocados pelo builder. Sem painel de números: o que
   distingue esta da divisória de seção é a ausência dele e o número grande. */
.dvb ...
</style>
<section class="slide light dvb" data-slide="0" data-var="a">
  <div class="mesh"></div><div class="grid-bg"></div>
  <div class="hd">...<div class="tag">Bloco {N} &middot; Template FIAP</div></div>
  <div class="body">
    <div class="num">{N}</div>
    <div class="bl">Bloco {N} de 07</div>
    <h1 class="tt"><span class="mask"><span>{NOME}</span></span></h1>
    <p class="lead">{LINHA}</p>
  </div>
  <div class="ft"><span>...</span></div>
</section>
```

A linha `{LINHA}` por bloco entra em `slide_div()` por um dicionário `DIV_LINHA` no builder:

```python
DIV_LINHA = {
    1: "Quem fez, o nome da solução e o que ela entrega, em dois parágrafos.",
    2: "O cenário, o problema nomeado, o efeito no indicador e por que resolver agora.",
    3: "O objetivo geral e as duas respostas que o sistema devolve.",
    4: "A abordagem, o que o dado mostrou, cada modelo por vez, o que a operação recebe, a arquitetura e a stack.",
    5: "O endereço da aplicação, as seis abas e as quatro folhas, cada uma com quem usa e como.",
    7: "O que ficou pronto, o que a equipe aprendeu, os limites que continuam de pé e o que vem em seguida.",
}
```
e `slide_div()` passa a fazer também `.replace("{LINHA}", DIV_LINHA[n_bloco])`.

- [ ] **Step 3: Escrever `blocos/05-descricao.html`**

Bloco 1 do template pede "descrição resumida em no máximo 2 parágrafos". Composição: dois parágrafos à esquerda em 18px, e à direita uma coluna estreita com quatro números rotulados empilhados com fio de 1px (não três cartões iguais em fileira). Texto:

> O Cronos é um sistema de previsão de incidentes operacionais construído sobre o histórico da Locaweb. Ele lê os **122.543 incidentes** registrados entre janeiro de 2023 e dezembro de 2025, recorta pelo campo oficial **Entrou para KPI?** os **25.600** que contam para o indicador de OLA, e devolve três respostas que hoje só existem na apuração de fim de ano: quantos incidentes entram nos próximos sete dias, qual incidente aberto tem maior probabilidade de estourar o prazo, e em que posição a meta anual de **P2 e de P3** deve fechar.

> São dois modelos, dois cálculos e uma aplicação. O Prophet prevê o volume diário de cada prioridade; uma regressão logística estima o risco de violação de cada incidente aberto; a projeção soma realizado, fila aberta e volume que ainda entra; e a nota de saúde ordena os produtos. A saída é publicada em uma aplicação **Django de seis abas**, em contêiner Docker e sem dependência de provedor de nuvem, com um resumo escrito no início do dia que chega ao gestor sem que ele precise consultar nada.

Números da coluna: `122.543` registros · `25.600` elegíveis, 21% · `4,2 · 11,8` erro por dia, P2 e P3 · `6 abas` em um contêiner.

`NOTAS["descricao"]` = os dois parágrafos sem marcação.

- [ ] **Step 4: Rodar, medir, olhar**

Run: `PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py --so 2 3 5 6 10 12 39 54`
Expected: nenhuma linha com `FORA DO PALCO`, `FORA DO CORPO` ou `INVISIVEL` nas posições 2, 5, 6; varredura limpa. Read em `_png/02-div-bloco-1.png`, `_png/03-equipe.png` (deve dizer "A equipe"), `_png/05-descricao.png`.

- [ ] **Step 5: Abrir `deck.html#2` no Opera e esperar o veredito do Igor**

Ajustar o que ele pedir, rodar de novo, reabrir. Só então:

- [ ] **Step 6: Commit**

```bash
git add prototipos/slides/sprint4/blocos scripts/monta_deck_sprint4.py prototipos/slides/sprint4/_png prototipos/slides/sprint4/deck.html sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx
git rm -q prototipos/slides/sprint4/_comparar.py prototipos/slides/sprint4/_comparar-*.html 2>/dev/null; rm -rf prototipos/slides/sprint4/_png/_comparar
git commit -m "feat: entram a divisória de bloco, a descrição resumida e o slide da equipe

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 3 · Lote 2: objetivo com verbo, abordagem, linhas de apoio da banca

**Files:**
- Modify: `scripts/monta_deck_sprint4.py` (`APOIO`, `AJUSTES_PITCH`, `NOTAS["objetivo"]`, `NOTAS["abordagem"]`)
- Create: `prototipos/slides/sprint4/blocos/13-abordagem.html`

- [ ] **Step 1: Linha de apoio no objetivo**

O template pede "comece com um verbo de ação". Em `slide_pitch()`, depois de ler a seção, inserir após `</h1>`:

```python
APOIO_PITCH = {
    "objetivo": "<b>Desenvolver</b> um sistema que antecipe a violação de OLA e a projeção da meta anual da Locaweb, entregando a leitura do ano antes da apuração de dezembro, nas prioridades <b>P2</b> e <b>P3</b>.",
}
```
`secao = secao.replace("</h1>", f'</h1><p class="apoio rv">{APOIO_PITCH[nome]}</p>', 1)`. O `.cena` do slide tem `flex:1`; se o corpo transbordar, reduzir `.obja .tt` para 46px no CSS do builder (`.obja .tt{font-size:46px}`).

- [ ] **Step 2: Escrever `blocos/13-abordagem.html`**

Bloco 4 pede abordagem, tecnologia, fontes de dados, análises e indicadores. Este slide responde abordagem e fontes; os demais itens já estão nos 24 da banca. Composição: trilho horizontal das quatro entregas em cima, e embaixo dois cartões assimétricos (um largo, um estreito).

Trilho: `27/04 · Ideação · nota 5,00` · `24/05 · Arquitetura · nota 5,00` · `23/08 · MVP preliminar · nota 9,5` · `21/09 · Solução final · esta entrega`. Cartão largo, "Como o trabalho andou": três linhas curtas: escopo fechado por sprint e avaliado antes da seguinte; toda hipótese passou por medição no dado antes de virar tela; sete notebooks analisam e gravam Parquet, a aplicação Django só lê. Cartão estreito, "Fontes de dados": `LW-DATASET.xlsx`, 122.543 linhas e 19 campos, 2023 a 2025; calendário de feriados nacionais do Brasil, pela biblioteca `holidays`, como regressor do Prophet.

`NOTAS["abordagem"]`: um parágrafo dizendo o mesmo.

- [ ] **Step 3: Propor ao Igor as linhas de apoio dos slides da banca**

Gerar a lista com as `chaves` do roteiro (`falas_da_banca()` devolve só a fala; para as chaves, ler `versoes[0].chaves`). Candidatas iniciais, para ele aprovar, cortar ou reescrever:

| Slide | Linha proposta |
|---|---|
| 8 | O total registrado saltou 5,4 vezes de agosto para setembro; a série que conta para a meta ficou em 2.330 e 2.324. |
| 9 | 98,3% dos incidentes elegíveis estão em 2025, então o treino usa só 2025 e a sazonalidade anual fica desligada. |
| 13 | 116 das 238 quebras de 2025 foram em item de configuração que já tinha quebrado antes. |
| 15 | A causa mais frequente tem taxa de violação abaixo da média; a ordenação certa é por taxa, não por volume. |
| 17 | 13 dos 14 dias da semana seguinte caíram dentro da faixa prevista em 1º de outubro. |
| 18 | Erro médio de 4,2 por dia no P2 e 11,8 no P3, contra 4,9 e 11,3 do melhor baseline. |
| 20 | 13 quebras nos 50 primeiros da fila de risco; ordenando por prioridade, nenhuma. |
| 21 | A regressão logística empata com o XGBoost em ROC AUC, vence em PR-AUC e prevê 48,1 quebras onde houve 50. |
| 26 | Em 1º de outubro a projeção já dizia P2 acima do limite e P3 dentro, e o ano fechou em 42 e 196. |
| 27 | A nota junta cinco medidas de P2 e P3; a posição diz o tamanho do problema e a cor diz o tipo. |
| 29 | Dois modelos e dois cálculos leem o histórico e a fila aberta e devolvem a situação da meta antes da apuração. |
| 30 | Uma imagem Docker com Django, Prophet e scikit-learn, sem serviço proprietário de nuvem. |

Mostrar a tabela no chat. As aprovadas entram em `APOIO`. Slides com `.sub` ou `.fecho` que já dizem a mensagem (4, 5, 6, 10, 11, 14, 23, 25) ficam fora.

- [ ] **Step 4: Rodar, medir, olhar, abrir, esperar veredito**

Run: `PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py`
Read em `_png/11-objetivo.png`, `_png/13-abordagem.png` e nos slides que ganharam apoio. Atenção a `FORA DO CORPO`: a linha empurra o conteúdo; onde transbordar, reduzir `.tt` daquele slide via CSS do builder prefixado pela classe do slide.

- [ ] **Step 5: Commit**

```bash
git add scripts/monta_deck_sprint4.py prototipos/slides/sprint4 sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx
git commit -m "feat: objetivo com verbo, slide de abordagem e linhas de apoio nos slides da banca

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 4 · Lote 3: pastilha do slide 31, mapa das abas, Panorama com balões

**Files:**
- Create: `prototipos/slides/sprint4/blocos/41-mapa-abas.html`
- Modify: `scripts/deck_sprint4_telas.py` (`BALOES["01-panorama"]`)
- Modify: `scripts/monta_deck_sprint4.py` (`NOTAS["mapa-abas"]`)

- [ ] **Step 1: Conferir o ajuste do slide 31**

`AJUSTES[31]` já troca a pastilha. Read em `_png/40-aplicacao.png`: a pastilha diz "Demonstração da solução".

- [ ] **Step 2: Escrever `blocos/41-mapa-abas.html`**

Composição: grade 3 × 2 das seis abas, cada célula com nome da aba, a pergunta que responde em uma linha e a pastilha do modelo em mono; abaixo, uma linha com as quatro folhas de detalhe e de qual aba cada uma abre. Texto:

| Aba | Responde | Modelo ou fonte |
|---|---|---|
| Panorama | Como está o dia agora, em P2 e P3, e onde agir primeiro | Prophet, regressão logística |
| Previsão | Quantos incidentes chegam nos próximos sete dias, por prioridade | Prophet, faixa de 80% |
| Projeção | Em que degrau a meta do ano vai fechar, em P2 e P3 | realizado + fila × risco + volume previsto |
| Fila de risco | Qual incidente aberto tem mais chance de estourar o prazo | regressão logística |
| Saúde por produto | Qual dos 15 produtos precisa de atenção primeiro | nota de 0 a 100, cinco componentes |
| Causas | Qual código de fechamento compensa prevenir | taxa de violação por código |

Folhas: Resumo do dia (do Panorama) · Régua da meta (da Projeção) · Explicabilidade do escore (da Fila) · Detalhe do produto (da Saúde).

`NOTAS["mapa-abas"]`: "Seis abas e quatro folhas. Cada aba responde uma pergunta do dia e é alimentada por um modelo ou um cálculo derivado. As dez capturas seguintes mostram uma por vez, com balões apontando onde cada funcionalidade está."

- [ ] **Step 3: Balões do Panorama**

Abrir `sprints/sprint-3/prints/01-panorama.png` com Read e medir, em % da imagem, o centro de cada objeto. Pontos de partida (conferir na imagem e ajustar):

```python
BALOES["01-panorama"] = [
    (46, 9,  "Previstos hoje, P3 e P2, com a faixa do dia", "Prophet"),
    (84, 9,  "Violações de ontem e dias úteis sem violação", "base elegível ao KPI"),
    (22, 45, "Registrados até as 15h contra o previsto para a hora", "Prophet, curva de chegada"),
    (50, 82, "Casos abertos ordenados por risco", "regressão logística"),
]
```
Regra: quatro a cinco balões por tela, nunca sobre texto pequeno, sempre com os dois P2 e P3 nomeados quando o objeto tem os dois.

- [ ] **Step 4: Rodar, medir, olhar, abrir, esperar veredito**

Run: `PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py --so 40 41 42`
Read em `_png/41-mapa-abas.png` e `_png/42-tela-01-01-panorama.png`: cada balão cai sobre o objeto que a legenda descreve. Abrir `deck.html#40`.

- [ ] **Step 5: Commit**

```bash
git add scripts prototipos/slides/sprint4 sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx
git commit -m "feat: mapa das abas e a primeira captura com balões numerados

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 5 · Lote 4: telas 2, 3 e 4 (resumo, Previsão, Projeção)

**Files:**
- Modify: `scripts/deck_sprint4_telas.py` (`BALOES` das três chaves)

- [ ] **Step 1: Medir e escrever os balões**

Read em cada print e preencher. O que cada balão tem de apontar:

`07-modal-briefing`: a frase de abertura do resumo (montada por regra sobre a saída dos modelos, nunca por modelo de linguagem: adendo 7.25); o bloco "Ontem" com registrados e violações; o bloco "Hoje" com as faixas previstas em P3 e P2 (Prophet); o botão que leva à tela de origem.

`02-previsao`: a faixa dos sete dias em P3 e em P2 (Prophet, banda de 80%); o padrão semanal; a curva de chegada ao longo do dia, que difere entre as prioridades (às 06h o P3 tem 11% do dia e o P2 tem 23%).

`03-projecao`: o acumulado até 30/09 em P2 e P3; as três parcelas da soma (realizado, fila × risco, volume previsto); o veredito por prioridade contra o limite (39 e 263); o link para a régua da meta.

- [ ] **Step 2: Rodar, olhar, abrir, esperar veredito**

Run: `PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py --so 43 44 45`
Read nos três PNG. Abrir `deck.html#43`.

- [ ] **Step 3: Commit**

```bash
git add scripts/deck_sprint4_telas.py prototipos/slides/sprint4 sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx
git commit -m "feat: balões nas capturas do resumo, da Previsão e da Projeção

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 6 · Lote 5: telas 5, 6 e 7 (régua da meta, Fila, explicabilidade)

**Files:**
- Modify: `scripts/deck_sprint4_telas.py`

- [ ] **Step 1: Medir e escrever os balões**

`10-modal-meta`: os seis degraus da escada oficial (dicionário de dados da Locaweb); a altura do degrau como a própria nota; onde o ano está e onde deve terminar, em P2 e P3.

`04-fila`: a probabilidade de estouro de cada caso (regressão logística); a ordenação do maior para o menor; o fator que mais pesa em cada linha; o item de configuração e a equipe.

`08-modal-escore`: cada sinal como peso × desvio da média; a soma que reconstrói a pontuação; o sinal que mais empurrou o caso para o topo.

- [ ] **Step 2: Rodar, olhar, abrir, esperar veredito**

Run: `PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py --so 46 47 48`

- [ ] **Step 3: Commit**

```bash
git add scripts/deck_sprint4_telas.py prototipos/slides/sprint4 sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx
git commit -m "feat: balões na régua da meta, na Fila e na explicabilidade do escore

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7 · Lote 6: telas 8, 9 e 10 (Saúde, detalhe do produto, Causas)

**Files:**
- Modify: `scripts/deck_sprint4_telas.py`

- [ ] **Step 1: Medir e escrever os balões**

`05-saude`: a nota de 0 a 100 dos 15 produtos; as colunas de P3 e P2 separadas; o componente que mais penaliza; quem atende (Grupo designado).

`09-modal-produto`: os cinco componentes da nota e o peso de cada um; o histórico do produto; o que separa "viola muito" de "vai começar a violar".

`06-causas`: os códigos de fechamento ordenados por taxa de violação; a taxa contra a média da base; o volume, mostrado para provar que a ordenação não é por ele.

- [ ] **Step 2: Rodar, olhar, abrir, esperar veredito**

Run: `PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py --so 49 50 51`

- [ ] **Step 3: Commit**

```bash
git add scripts/deck_sprint4_telas.py prototipos/slides/sprint4 sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx
git commit -m "feat: balões na Saúde, no detalhe do produto e nas Causas

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 8 · Lote 7: acesso, vídeo, síntese

**Files:**
- Create: `prototipos/slides/sprint4/blocos/53-video.html`
- Create: `prototipos/slides/sprint4/blocos/55-sintese.html`
- Modify: `scripts/monta_deck_sprint4.py` (`NOTAS`)

- [ ] **Step 1: Conferir o slide 33 da banca como link funcional**

Read em `_png/52-acesso.png`. Ele já traz QR, `igor-vignola.github.io/LocaWeb-Cronos`, `github.com/igor-vignola/LocaWeb-Cronos` e as seis rotas. Nada a mudar.

- [ ] **Step 2: Escrever `blocos/53-video.html`**

Escuro, o único do bloco 6. Título "Vídeo pitch", o endereço `https://youtu.be/IeWLVBD0Jas` em mono 36px `#93C5FD`, selo "Publicado no YouTube, com acesso público", e uma linha: cinco minutos, formato hands on, a aplicação navegada com as seis abas. Nada de três cartões iguais em fileira: o endereço é o objeto dominante e a linha vem embaixo.

`NOTAS["video"]`: "O vídeo tem cinco minutos, em formato hands on, e está público no YouTube no endereço do slide."

- [ ] **Step 3: Escrever `blocos/55-sintese.html`**

Título "O que ficou pronto". Quatro números rotulados, em duas linhas de dois, cada um com P2 e P3 quando cabe:

- `4,2 · 11,8` erro médio por dia da previsão, P2 e P3, de D+1 a D+7
- `13 de 50` quebras encontradas nos 50 primeiros da fila de risco; por prioridade, nenhuma
- `2 meses` de antecedência na chamada da meta, certa nas duas prioridades: P2 acima do limite, P3 dentro
- `6 abas` em um contêiner Docker, sem provedor de nuvem amarrado

Linha de fecho: "O modelo de risco tem ROC AUC de 0,869 e prevê 48,1 quebras onde houve 50."

`NOTAS["sintese"]`: os quatro itens em prosa.

- [ ] **Step 4: Rodar, medir, olhar, abrir, esperar veredito**

Run: `PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py --so 52 53 55`

- [ ] **Step 5: Commit**

```bash
git add scripts prototipos/slides/sprint4 sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx
git commit -m "feat: slide do vídeo pitch e síntese dos resultados

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 9 · Lote 8: aprendizados, limitações, próximos passos

**Files:**
- Create: `prototipos/slides/sprint4/blocos/56-aprendizados.html`
- Create: `prototipos/slides/sprint4/blocos/57-limitacoes.html`
- Create: `prototipos/slides/sprint4/blocos/58-proximos-passos.html`
- Modify: `scripts/monta_deck_sprint4.py` (`NOTAS`)

- [ ] **Step 1: `blocos/56-aprendizados.html`**

Quatro itens empilhados com fio de 1px, número mono à esquerda, título curto e uma frase:

1. **Testar a hipótese óbvia antes de construir sobre ela.** O volume do dia explica 2,5% da variação das quebras (r = 0,159; p = 0,011). Isso definiu o papel de cada modelo: volume dimensiona a carga, risco aponta o caso.
2. **Com evento raro, acurácia premia quem não avisa.** Uma quebra a cada 103 incidentes; não sinalizar nada dá 99,04% de acurácia e encontra zero quebras. A medida certa é quantas quebras aparecem nas primeiras posições da fila.
3. **Modelo interpretável não custou desempenho.** Regressão logística e XGBoost empatam em ROC AUC (0,869 e 0,868); a logística vence em PR-AUC (0,296 contra 0,253) e fica calibrada (48,1 previstas onde houve 50).
4. **O campo oficial do cliente vale mais que a regra reescrita.** `Entrou para KPI?` devolve 25.600 elegíveis; reimplementar só por `Incidente Pai` vazio devolveria 107.416, 88% da base.

- [ ] **Step 2: `blocos/57-limitacoes.html`**

Cinco itens em grade 3 + 2, cada um com o número que o mede:

1. **A faixa do P3 subestima a incerteza.** Cobertura entre 59% e 61% dos dias de teste no P3, contra 86% a 88% no P2, quando a base muda de patamar em novembro e dezembro.
2. **O rótulo só existe depois do fechamento.** `Entrou para KPI?` é preenchido quando o incidente encerra; em operação, os últimos dias da série ficam incompletos.
3. **Um ano de dado denso, não três.** 98% dos elegíveis estão em 2025; há dado para o padrão de semana e feriado, não para o padrão de ano, e a sazonalidade anual ficou desligada de propósito.
4. **Sem número financeiro no dataset.** Não há custo por violação; o benefício está medido em violações e em posição na meta, nunca em moeda.
5. **O resumo do dia ainda não usa modelo de linguagem.** A frase de abertura é montada por regra sobre a saída dos modelos; a Claude API é próximo passo, não entrega.

- [ ] **Step 3: `blocos/58-proximos-passos.html`**

Cada passo responde a um limite do slide anterior, e o slide diz isso na linha de apoio. Cinco itens:

1. **Ler direto da base interna da Locaweb**, no lugar da planilha, o nó tracejado do fluxograma da arquitetura.
2. **Reajuste semanal em janela consolidada**, descartando os últimos dias, para a cauda incompleta do rótulo e para a cobertura do intervalo no P3.
3. **Alarme de calibração**: monitorar a cobertura da faixa semana a semana e avisar quando cair do nominal.
4. **Gerar a frase de abertura do resumo pela Claude API**, nos bastidores, sem interface de conversa.
5. **Levantar o custo por violação com a Locaweb**, para o ganho sair em reais e não só em posição na meta.

- [ ] **Step 4: Rodar, medir, olhar, abrir, esperar veredito**

Run: `PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py --so 56 57 58`

- [ ] **Step 5: Commit**

```bash
git add scripts prototipos/slides/sprint4 sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx
git commit -m "feat: aprendizados, limitações e próximos passos fecham o bloco 7

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 10 · Fecho: deck completo, varredura, contexto

**Files:**
- Modify: `context/status.md`, `CLAUDE.md` (estrutura do projeto: `prototipos/slides/sprint4/blocos/`)

- [ ] **Step 1: Rodar tudo do zero**

Run: `PYTHONUTF8=1 .venv/Scripts/python scripts/monta_deck_sprint4.py`
Expected: `59 slides, 0 de espera`; nenhum `FORA DO PALCO`, `FORA DO CORPO` ou `INVISIVEL`; varredura sem aviso.

- [ ] **Step 2: Conferir o pptx**

```bash
PYTHONUTF8=1 .venv/Scripts/python -c "
from pptx import Presentation
p=Presentation('sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx')
assert len(p.slides)==59; assert (p.slide_width,p.slide_height)==(12192000,6858000)
assert all(len(s.shapes)==1 for s in p.slides)
vazias=[i for i,s in enumerate(p.slides,1) if not s.notes_slide.notes_text_frame.text.strip() or s.notes_slide.notes_text_frame.text.strip()=='Em construção.']
print('notas vazias ou de espera:', vazias)"
```
Expected: `notas vazias ou de espera: []`.

Também: `grep -c "youtu.be/IeWLVBD0Jas" prototipos/slides/sprint4/_build/53-video.html` dá 1, e `grep -l "igor-vignola.github.io/LocaWeb-Cronos" prototipos/slides/sprint4/_build/*.html | wc -l` dá pelo menos 11 (o acesso e as dez telas).

- [ ] **Step 3: Abrir o deck inteiro para o Igor**

`deck.html` do slide 1, e o `.pptx` no PowerPoint: `powershell -Command "Start-Process 'C:\...\sprints\EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx'"`. Esperar a passada final dele.

- [ ] **Step 4: Atualizar o contexto**

`context/status.md`: seção "Sessão de 21/09/2026" com o que foi feito, os 59 slides, o que sai no `.zip` e o que falta para o envio (rodar `scripts/monta_zip_sprint4.py`, anexar no portal). `CLAUDE.md`: acrescentar `prototipos/slides/sprint4/blocos/` na árvore.

- [ ] **Step 5: Commit**

```bash
git add -A prototipos/slides/sprint4 scripts sprints/EC_Sprint_4_2TSCOA_SolucaoFinal_Cronos_SuperDataBros.pptx context CLAUDE.md
git commit -m "feat: fecha o deck da Sprint 4 com 59 slides e a fala nas notas

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```
