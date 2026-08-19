# -*- coding: utf-8 -*-
"""Gera a réplica do quadro Trello do projeto, no estado da Sprint 3.

O template da FIAP pede a imagem do quadro de planejamento. O quadro real
(`Cronos · Challenge FIAP 2026`) parou no estado da Sprint 2, e o print dele hoje mostraria
cartão de maio. Este script desenha como o quadro fica com o trabalho da Sprint 3 lançado:
mesmas cinco listas, mesma linguagem visual do Trello no tema escuro.

Saem três arquivos, todos com 1600px de largura para cair no slide sem recorte:

    quadro.html        o quadro, cinco listas
    card-ppt.html      o cartão aberto de "Montar o PPT da Sprint 3"
    card-modelo.html   o cartão aberto de "Escolher a regressão logística"

O conteúdo dos cartões vem de `sprints/sprint-3/CARDS-TRELLO.md`, que por sua vez saiu do
`context/status.md` e do histórico do repositório: cada cartão descreve trabalho que
aconteceu, com a data real.

Uso:
    .venv/Scripts/python scripts/monta_quadro_trello.py          # só os HTML
    .venv/Scripts/python scripts/monta_quadro_trello.py --png    # HTML + PNG em 2x
"""
from __future__ import annotations

import base64
import sys
from io import BytesIO
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "sprints" / "sprint-3" / "quadro"
FOTO_IGOR = RAIZ / "brand" / "equipe" / "igor.png"

LARGURA = 1600
# O quadro fica raso de propósito: com três cartões por lista, 900px deixariam quase
# metade da imagem em fundo vazio. O cartão aberto precisa da altura cheia para caber.
ALTURA_QUADRO, ALTURA_CARD = 1600 * 7 // 16, 900

# ── identidade ───────────────────────────────────────────────────────────────────────
# Pares (fundo, texto) das etiquetas no tema escuro do Trello. São os valores do próprio
# produto, então a réplica não precisa de ajuste de contraste próprio.
ETIQUETAS = {
    "Sprint 1": ("#216E4E", "#BAF3DB"),
    "Sprint 2": ("#533F04", "#F8E6A0"),
    "Sprint 3": ("#974F0C", "#FEDEC8"),
    "Sprint 4": ("#206A83", "#C6EDFB"),
    "Análise": ("#5E4DB2", "#DFD8FD"),
    "Modelagem": ("#943D73", "#FDD0EC"),
    "Aplicação": ("#09326C", "#CCE0FF"),
    "Entregável": ("#AE2E24", "#FFD5D2"),
}

# No quadro real o Igor usa foto e os outros dois usam inicial. Manter assim é o que faz a
# fileira de avatares do topo bater com a do quadro que já existe.
MEMBROS = {
    "IV": {"nome": "Igor Vignola", "foto": True},
    "BC": {"nome": "Ana Beatriz Costa", "cor": "#6E5DC6"},
    "HA": {"nome": "Hygor Abrantes", "cor": "#0C66E4"},
}

# ── conteúdo do quadro ───────────────────────────────────────────────────────────────
# `total` é quantos cartões a lista tem de verdade; a lista `cartoes` é só o que cabe na
# altura do print. O contador do cabeçalho mostra o total, como no Trello.
LISTAS = [
    {
        "nome": "Backlog",
        "total": 5,
        "cartoes": [
            {
                "titulo": "Publicar a aplicação num provedor",
                "etiquetas": ["Sprint 4", "Aplicação"],
                "descricao": True,
                "membros": ["IV", "HA"],
            },
            {
                "titulo": "Gravar o vídeo pitch de 5 minutos",
                "etiquetas": ["Sprint 4", "Entregável"],
                "descricao": True,
                "membros": ["IV", "BC", "HA"],
            },
            {
                "titulo": "Calcular o custo mensal da Claude API",
                "etiquetas": ["Sprint 4", "Análise"],
                "descricao": True,
                "membros": ["BC"],
            },
        ],
    },
    {
        "nome": "A Fazer",
        "total": 3,
        "cartoes": [
            {
                "titulo": "Atualizar os anexos das Sprints 1 e 2",
                "etiquetas": ["Sprint 3", "Entregável"],
                "descricao": True,
                "data": ("22 de ago.", "prox"),
                "membros": ["BC", "HA"],
            },
            {
                "titulo": "Incluir as referências bibliográficas",
                "etiquetas": ["Sprint 3", "Entregável"],
                "data": ("22 de ago.", "prox"),
                "membros": ["HA"],
            },
            {
                "titulo": "Subir o arquivo final no portal FIAP ON",
                "etiquetas": ["Sprint 3", "Entregável"],
                "data": ("23 de ago.", "prox"),
                "membros": ["IV"],
            },
        ],
    },
    {
        "nome": "Em Andamento",
        "total": 2,
        "cartoes": [
            {
                "titulo": "Montar o PPT da Sprint 3",
                "etiquetas": ["Sprint 3", "Entregável"],
                "descricao": True,
                "comentarios": 3,
                "checklist": "6/7",
                "data": ("23 de ago.", "prox"),
                "membros": ["IV", "BC", "HA"],
            },
            {
                "titulo": "Registrar no notebook o teste que descartou a cascata",
                "etiquetas": ["Sprint 3", "Análise"],
                "descricao": True,
                "checklist": "2/3",
                "data": ("21 de ago.", "prox"),
                "membros": ["HA"],
            },
        ],
    },
    {
        "nome": "Em Revisão",
        "total": 2,
        "cartoes": [
            {
                "titulo": "Conferir o deck com o checklist da sprint",
                "etiquetas": ["Sprint 3", "Entregável"],
                "descricao": True,
                "checklist": "9/12",
                "data": ("22 de ago.", "prox"),
                "membros": ["BC"],
            },
            {
                "titulo": "Revisar os textos dos slides de análise e modelagem",
                "etiquetas": ["Sprint 3", "Entregável"],
                "comentarios": 2,
                "data": ("21 de ago.", "prox"),
                "membros": ["IV", "BC"],
            },
        ],
    },
    {
        "nome": "Concluído",
        "total": 20,
        "cartoes": [
            {
                "titulo": "Tirar os prints da aplicação para a entrega",
                "etiquetas": ["Sprint 3", "Entregável"],
                "descricao": True,
                "completo": True,
                "data": ("17 de ago.", "ok"),
                "membros": ["IV"],
            },
            {
                "titulo": "Revisão visual das seis abas do painel",
                "etiquetas": ["Sprint 3", "Aplicação"],
                "descricao": True,
                "checklist": "32/32",
                "completo": True,
                "data": ("17 de ago.", "ok"),
                "membros": ["IV", "BC"],
            },
            {
                "titulo": "Conferir os números da tela com os notebooks",
                "etiquetas": ["Sprint 3", "Aplicação"],
                "descricao": True,
                "completo": True,
                "data": ("14 de ago.", "ok"),
                "membros": ["HA", "IV"],
            },
        ],
    },
]

# ── cartões abertos ──────────────────────────────────────────────────────────────────
CARD_PPT = {
    "arquivo": "card-ppt.html",
    "titulo": "Montar o PPT da Sprint 3",
    "lista": "Em Andamento",
    "etiquetas": ["Sprint 3", "Entregável"],
    "membros": ["IV", "BC", "HA"],
    "data": ("23 de agosto de 2026 às 23:59", "prox"),
    "descricao": [
        "Montar o PPT da Sprint 3 na ordem do template da FIAP, juntando num arquivo só os "
        "slides de análise e modelagem e os prints da aplicação. Formato .pptx, 16:9.",
        "O que sai deste cartão: o arquivo .pptx com o nome no padrão da FIAP, os prints "
        "da aplicação e os anexos atualizados das sprints anteriores.",
    ],
    "checklist": {
        "nome": "Conferência do template",
        "itens": [
            ("Identificação da equipe com RM em ordem alfabética", True),
            ("Contextualização, problema e proposta atualizados", True),
            ("Arquitetura da solução e descrição das tecnologias", True),
            ("Prints da aplicação com explicação de cada tela", True),
            ("Amostra dos dados utilizados", True),
            ("Imagem do quadro de planejamento", True),
            ("Anexos atualizados das Sprints 1 e 2", False),
        ],
    },
    "comentario": {
        "autor": "IV",
        "quando": "há 2 horas",
        "texto": "Bloco de análise e prints da aplicação fechados. Falta atualizar os "
        "anexos das Sprints 1 e 2.",
    },
}

CARD_MODELO = {
    "arquivo": "card-modelo.html",
    "titulo": "Escolher a regressão logística no lugar do XGBoost",
    "lista": "Concluído",
    "etiquetas": ["Sprint 3", "Modelagem"],
    "membros": ["HA", "IV"],
    "data": ("3 de agosto de 2026", "ok"),
    "descricao": [
        "Comparar regressão logística e XGBoost no risco de quebra de OLA e decidir qual "
        "dos dois vai para a aplicação. A quebra é rara, então quem decide é o PR-AUC.",
        "Medição: ROC AUC 0,869 contra 0,868, empate. PR-AUC 0,296 contra 0,253, vantagem "
        "de 17% para a logística. A logística prevê 48,1 quebras onde houve 50; o XGBoost "
        "com scale_pos_weight prevê 1.007 e inviabiliza a projeção do KPI.",
        "Decisão: logística no MVP, XGBoost fica no notebook como baseline de comparação.",
    ],
    "checklist": {
        "nome": "Validação do modelo",
        "itens": [
            ("Treino e teste separados por data, sem vazamento", True),
            ("PR-AUC e ROC AUC medidos nos dois modelos", True),
            ("Calibração conferida contra o realizado", True),
            ("Decisão registrada em context/decisoes-tecnicas.md", True),
        ],
    },
    "comentario": {
        "autor": "HA",
        "quando": "3 de ago. às 18:42",
        "texto": "Com 0,97% de positivos, acurácia não separa modelo bom de modelo que só "
        "responde “não quebra”. Por isso a decisão saiu pelo PR-AUC.",
    },
}

# ── ícones ───────────────────────────────────────────────────────────────────────────
# Traço de 1.5px em `currentColor`: é o peso que o Trello usa nos badges do cartão, e
# deixa o ícone legível depois de reduzir o print para caber no slide.
ICONES = {
    "olho": '<path d="M2 8s2.2-4 6-4 6 4 6 4-2.2 4-6 4-6-4-6-4Z"/><circle cx="8" cy="8" r="1.8"/>',
    "relogio": '<circle cx="8" cy="8" r="6"/><path d="M8 4.8V8l2.2 1.4"/>',
    "descricao": '<path d="M3 4.5h10M3 8h10M3 11.5h6"/>',
    "checklist": '<rect x="2.5" y="2.5" width="11" height="11" rx="2"/><path d="M5.4 8.2l1.9 1.9 3.4-3.7"/>',
    "comentario": '<path d="M13.5 9.2a2 2 0 0 1-2 2H6l-3 2.3V4.8a2 2 0 0 1 2-2h6.5a2 2 0 0 1 2 2Z"/>',
    "mais": '<path d="M8 3.5v9M3.5 8h9"/>',
    "quadro": '<rect x="2.5" y="3" width="4" height="10" rx="1"/><rect x="9.5" y="3" width="4" height="6.5" rx="1"/>',
    "calendario": '<rect x="2.5" y="3.5" width="11" height="10" rx="2"/><path d="M2.5 6.5h11M5.5 2.2v2.4M10.5 2.2v2.4"/>',
    "raio": '<path d="M9 2 4 9h3.4l-.9 5L12 7H8.5Z"/>',
    "filtro": '<path d="M2.5 4h11l-4.2 4.7V13L6.7 11.6V8.7Z"/>',
    "estrela": '<path d="m8 2.6 1.7 3.5 3.8.5-2.8 2.7.7 3.8L8 11.3l-3.4 1.8.7-3.8-2.8-2.7 3.8-.5Z"/>',
    "globo": '<circle cx="8" cy="8" r="5.6"/><path d="M2.4 8h11.2M8 2.4c1.6 1.8 2.3 3.7 2.3 5.6S9.6 12 8 13.6C6.4 11.8 5.7 9.9 5.7 8S6.4 4.2 8 2.4Z"/>',
    "pessoa_mais": '<circle cx="6.6" cy="5.8" r="2.4"/><path d="M2.4 13.4c0-2.3 1.9-3.8 4.2-3.8 1 0 1.9.3 2.6.8M12.4 9.2v4M10.4 11.2h4"/>',
    "reticencias": '<circle cx="3.6" cy="8" r="1.1" fill="currentColor" stroke="none"/><circle cx="8" cy="8" r="1.1" fill="currentColor" stroke="none"/><circle cx="12.4" cy="8" r="1.1" fill="currentColor" stroke="none"/>',
    "modelo": '<rect x="2.5" y="2.5" width="11" height="11" rx="2"/><path d="M5.2 6h5.6M5.2 9h3.4"/>',
    "caixa": '<path d="M2.4 8h3.2l1 2h2.8l1-2h3.2M2.4 8l2-5h7.2l2 5v4.4a1.2 1.2 0 0 1-1.2 1.2H3.6a1.2 1.2 0 0 1-1.2-1.2Z"/>',
    "trocar": '<path d="M2.6 5.4h8.2M8.6 3.2l2.2 2.2-2.2 2.2M13.4 10.6H5.2M7.4 8.4l-2.2 2.2 2.2 2.2"/>',
    "cartao": '<rect x="2.5" y="3" width="11" height="10" rx="2"/><path d="M5 6.4h6M5 9.2h3.6"/>',
    "membros": '<circle cx="6.2" cy="6" r="2.3"/><path d="M2.6 13c0-2.2 1.7-3.6 3.6-3.6S9.8 10.8 9.8 13"/><path d="M10.4 4.2a2.2 2.2 0 0 1 0 4.2M11.2 13c0-1.5-.4-2.6-1.1-3.3"/>',
    "etiqueta": '<path d="M8.4 2.5H13V7l-6 6-4.5-4.5Z"/><circle cx="10.6" cy="5" r=".9"/>',
    "anexo": '<path d="M10.6 5.4 6.2 9.8a1.7 1.7 0 0 0 2.4 2.4l4.6-4.6a3.2 3.2 0 0 0-4.5-4.5L3.8 8a4.6 4.6 0 0 0 6.5 6.5"/>',
    "local": '<path d="M8 14s4.4-4 4.4-7.2a4.4 4.4 0 0 0-8.8 0C3.6 10 8 14 8 14Z"/><circle cx="8" cy="6.8" r="1.6"/>',
    "capa": '<rect x="2.5" y="3" width="11" height="10" rx="2"/><path d="M2.5 6.6h11"/>',
    "seta": '<path d="M6 3.5 10.5 8 6 12.5"/>',
    "arquivar": '<rect x="2.5" y="3" width="11" height="3" rx="1"/><path d="M3.8 6v6.2c0 .6.5 1.1 1.1 1.1h6.2c.6 0 1.1-.5 1.1-1.1V6M6.4 9h3.2"/>',
    "copiar": '<rect x="5" y="5" width="8.5" height="8.5" rx="1.6"/><path d="M11 5V4a1.6 1.6 0 0 0-1.6-1.6H4A1.6 1.6 0 0 0 2.4 4v5.4A1.6 1.6 0 0 0 4 11h1"/>',
    "compartilhar": '<circle cx="12" cy="4.2" r="1.9"/><circle cx="4" cy="8" r="1.9"/><circle cx="12" cy="11.8" r="1.9"/><path d="M5.7 7.1 10.3 5M5.7 8.9l4.6 2.1"/>',
    "x": '<path d="M4.2 4.2l7.6 7.6M11.8 4.2l-7.6 7.6"/>',
    "sino": '<path d="M4.4 7a3.6 3.6 0 1 1 7.2 0c0 2.6 1 3.6 1 3.6H3.4s1-1 1-3.6Z"/><path d="M6.6 12.4a1.6 1.6 0 0 0 2.8 0"/>',
}


def icone(nome: str, tamanho: int = 16, extra: str = "") -> str:
    """Devolve o SVG do ícone com traço em `currentColor`."""
    return (
        f'<svg class="ic{extra}" width="{tamanho}" height="{tamanho}" viewBox="0 0 16 16" '
        f'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
        f'stroke-linejoin="round">{ICONES[nome]}</svg>'
    )


# ── estilo ───────────────────────────────────────────────────────────────────────────
def css(foto: str, altura: int) -> str:
    """CSS compartilhado pelos três arquivos.

    O fundo do quadro reproduz o gradiente roxo que o Trello aplica por padrão. Ele não é
    escolha de identidade do Cronos: é o que aparece no quadro real, e trocar por outra cor
    faria a réplica deixar de parecer o produto.
    """
    return f"""
:root{{
  --lista:#101204; --cartao:#22272B; --cartao-h:#282E33;
  --txt:#B6C2CF; --txt-forte:#DEE4EA; --sub:#9FADBC;
  --linha:rgba(255,255,255,.10); --modal:#323940;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{LARGURA}px;height:{altura}px;overflow:hidden}}
body{{
  font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;color:var(--txt);
  background:
    radial-gradient(1100px 780px at 12% 118%,rgba(146,74,206,.85),transparent 62%),
    radial-gradient(900px 700px at 52% 128%,rgba(178,86,205,.80),transparent 58%),
    radial-gradient(1000px 900px at 98% 12%,rgba(126,80,214,.75),transparent 62%),
    linear-gradient(148deg,#3a1a5e 0%,#5a2a8d 42%,#7c3aa6 78%,#9247c4 100%);
}}
.ic{{flex-shrink:0;display:block}}

/* ── cabeçalho do quadro ── */
.topo{{height:56px;display:flex;align-items:center;gap:12px;padding:0 12px 0 20px;
  background:rgba(0,0,0,.24);border-bottom:1px solid rgba(255,255,255,.08)}}
.topo .nome{{font-size:18px;font-weight:700;color:#fff;letter-spacing:-.2px}}
.topo .vis{{display:flex;align-items:center;gap:4px;color:#fff;opacity:.9;
  padding:5px 6px;border-radius:4px}}
.topo .vis .cv{{font-size:11px}}
.topo .dir{{margin-left:auto;display:flex;align-items:center;gap:6px}}
.avs{{display:flex;align-items:center;margin-right:6px}}
.avs .av{{margin-left:-6px;border:2px solid rgba(0,0,0,.35)}}
.avs .av:first-child{{margin-left:0}}
.bt-ic{{width:32px;height:32px;border-radius:6px;display:flex;align-items:center;
  justify-content:center;color:#fff;opacity:.92}}
.bt-ic:hover{{background:rgba(255,255,255,.16)}}
.bt-share{{display:flex;align-items:center;gap:7px;height:32px;padding:0 12px;
  border-radius:4px;background:#fff;color:#1D2125;font-size:14px;font-weight:600}}
.bt-share .ic{{stroke-width:1.7}}

/* ── avatar ── */
.av{{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:11px;font-weight:700;color:#fff;flex-shrink:0;
  letter-spacing:.2px;overflow:hidden}}
.av.foto{{background:#1D2125 url('{foto}') center/cover}}
.av.p24{{width:24px;height:24px;font-size:10px}}
.av.p32{{width:32px;height:32px;font-size:12px}}

/* ── listas ── */
.quadro{{height:{altura - 56}px;display:flex;align-items:flex-start;gap:12px;
  padding:14px 0 0 16px;overflow:hidden}}
.lista{{width:272px;flex-shrink:0;background:var(--lista);border-radius:12px;
  padding:8px;max-height:{altura - 56 - 40}px;display:flex;flex-direction:column;
  box-shadow:0 1px 1px rgba(0,0,0,.25)}}
.lista .cab{{display:flex;align-items:center;gap:8px;padding:6px 8px 8px 10px}}
.lista .cab h2{{font-size:14px;font-weight:600;color:var(--txt-forte);letter-spacing:-.1px}}
.lista .cab .qt{{font-size:14px;color:var(--sub);margin-left:auto;
  font-variant-numeric:tabular-nums}}
.lista .cab .men{{width:24px;height:24px;border-radius:4px;display:flex;
  align-items:center;justify-content:center;color:var(--sub)}}
.cartoes{{display:flex;flex-direction:column;gap:8px;overflow:hidden;
  padding:0 2px 2px;position:relative}}
.rodape{{display:flex;align-items:center;gap:8px;padding:8px 8px 4px;color:var(--txt);
  font-size:14px;margin-top:2px}}
.rodape .esp{{margin-left:auto;display:flex;align-items:center;color:var(--sub)}}

/* ── cartão ── */
.cartao{{background:var(--cartao);border-radius:8px;padding:8px 12px 4px;
  box-shadow:0 1px 1px rgba(9,30,66,.25);border:1px solid transparent}}
.cartao .etqs{{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px}}
.etq{{height:16px;padding:0 8px;border-radius:3px;font-size:12px;font-weight:600;
  display:inline-flex;align-items:center;line-height:1;letter-spacing:.1px}}
.cartao .tit{{font-size:14px;line-height:20px;color:var(--txt-forte);
  display:flex;gap:6px;align-items:flex-start}}
.cartao .tit .ok{{flex-shrink:0;margin-top:2px}}
.badges{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:6px;
  min-height:28px;padding-bottom:4px}}
.badges .bd{{display:flex;align-items:center;gap:4px;color:var(--sub);font-size:12px;
  height:24px;border-radius:3px}}
.badges .bd.data{{padding:0 6px;font-weight:500}}
.badges .bd.data.prox{{color:var(--sub)}}
.badges .bd.data.ok{{background:#164B35;color:#7EE2B8}}
.badges .bd.data.venc{{background:#601E16;color:#FD9891}}
.badges .mem{{margin-left:auto;display:flex;gap:4px}}

/* ── barra inferior ── */
.nav{{position:absolute;left:50%;bottom:14px;transform:translateX(-50%);
  display:flex;align-items:center;gap:4px;padding:6px;border-radius:12px;
  background:#1D2125;box-shadow:0 8px 24px rgba(0,0,0,.4)}}
.nav a{{display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:8px;
  color:var(--txt);font-size:14px;font-weight:500;text-decoration:none}}
.nav a.on{{background:#2C333A;color:#fff}}
.add-lista{{width:272px;flex-shrink:0;height:44px;border-radius:12px;
  background:rgba(255,255,255,.24);color:#fff;display:flex;align-items:center;gap:8px;
  padding:0 14px;font-size:14px;font-weight:500}}

/* ── cartão aberto ── */
.veu{{position:absolute;inset:0;background:rgba(0,0,0,.64)}}
.cb{{position:absolute;left:50%;top:26px;transform:translateX(-50%);width:812px;
  max-height:{altura - 52}px;background:var(--modal);border-radius:10px;overflow:hidden;
  box-shadow:0 8px 32px rgba(0,0,0,.5);display:flex;flex-direction:column}}
.cb-topo{{padding:18px 20px 8px 20px;display:flex;gap:14px;align-items:flex-start}}
.cb-topo .ic{{color:var(--sub);margin-top:6px}}
.cb-topo h1{{font-size:20px;font-weight:600;color:var(--txt-forte);line-height:26px}}
.cb-topo .onde{{font-size:14px;color:var(--sub);margin-top:5px}}
.cb-topo .onde u{{text-underline-offset:2px}}
.cb-topo .fechar{{margin-left:auto;color:var(--sub);display:flex;gap:14px;
  padding-top:4px}}
.cb-corpo{{display:flex;gap:16px;padding:4px 20px 20px;overflow:hidden}}
.cb-main{{flex:1;min-width:0;display:flex;flex-direction:column;gap:18px}}
.cb-lado{{width:168px;flex-shrink:0;display:flex;flex-direction:column;gap:6px}}
.cb-lado .rot{{font-size:12px;font-weight:600;color:var(--sub);margin:8px 0 2px}}
.cb-lado .bt{{display:flex;align-items:center;gap:8px;height:32px;padding:0 10px;
  border-radius:4px;background:#A1BDD914;color:var(--txt);font-size:14px;font-weight:500}}

.meta{{display:flex;flex-wrap:wrap;gap:22px}}
.meta .bl .rot{{font-size:12px;font-weight:600;color:var(--sub);margin-bottom:6px}}
.meta .lin{{display:flex;align-items:center;gap:4px}}
.meta .box{{width:32px;height:32px;border-radius:4px;background:#A1BDD914;
  display:flex;align-items:center;justify-content:center;color:var(--txt)}}
.meta .seguir{{display:flex;align-items:center;gap:8px;height:32px;padding:0 12px;
  border-radius:4px;background:#A1BDD914;color:var(--txt);font-size:14px;font-weight:500}}
.meta .dt{{display:flex;align-items:center;gap:8px;height:32px;padding:0 10px;
  border-radius:4px;background:#A1BDD914;color:var(--txt);font-size:14px}}
.meta .dt .marca{{width:16px;height:16px;border-radius:3px;border:2px solid var(--sub);
  display:flex;align-items:center;justify-content:center}}
.meta .dt .marca.on{{background:#4BCE97;border-color:#4BCE97}}
.meta .dt .sel{{font-size:12px;font-weight:600;padding:1px 6px;border-radius:3px}}
.meta .dt .sel.ok{{background:#164B35;color:#7EE2B8}}
.meta .dt .sel.prox{{background:#533F04;color:#F8E6A0}}
.meta .etqs{{display:flex;gap:4px;align-items:center}}
.meta .etq{{height:32px;padding:0 12px;border-radius:4px;font-size:14px;font-weight:600}}

.sec .cab{{display:flex;align-items:center;gap:10px;color:var(--txt-forte);
  margin-bottom:10px}}
.sec .cab .ic{{color:var(--sub)}}
.sec .cab h3{{font-size:16px;font-weight:600}}
.sec .cab .acoes{{margin-left:auto;display:flex;gap:6px}}
.sec .cab .acoes span{{height:32px;padding:0 12px;border-radius:4px;background:#A1BDD914;
  font-size:14px;font-weight:500;color:var(--txt);display:flex;align-items:center}}
.desc{{padding-left:34px;display:flex;flex-direction:column;gap:10px}}
.desc p{{font-size:14px;line-height:21px;color:var(--txt)}}

.chk{{padding-left:34px}}
.chk .prog{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}
.chk .prog .pc{{font-size:11px;color:var(--sub);width:32px;
  font-variant-numeric:tabular-nums}}
.chk .prog .tr{{flex:1;height:8px;border-radius:4px;background:#A1BDD924;overflow:hidden}}
.chk .prog .tr i{{display:block;height:100%;border-radius:4px;background:#4BCE97}}
.chk .it{{display:flex;align-items:flex-start;gap:10px;padding:6px 8px;border-radius:4px}}
.chk .it .cx{{width:16px;height:16px;border-radius:3px;border:2px solid var(--sub);
  flex-shrink:0;margin-top:2px;display:flex;align-items:center;justify-content:center}}
.chk .it .cx.on{{background:#4BCE97;border-color:#4BCE97}}
.chk .it .cx.on svg{{stroke:#1D2125;stroke-width:2.4}}
.chk .it span{{font-size:14px;line-height:20px;color:var(--txt)}}
.chk .it.feito span{{color:var(--sub)}}

.ativ{{display:flex;gap:10px;padding-left:0;align-items:flex-start}}
.ativ .cx{{flex:1;background:#22272B;border-radius:8px;padding:10px 12px;
  box-shadow:0 1px 1px rgba(0,0,0,.25)}}
.ativ .quem{{font-size:14px;font-weight:600;color:var(--txt-forte)}}
.ativ .quando{{font-size:12px;color:var(--sub);margin-left:8px;font-weight:400}}
.ativ p{{font-size:14px;line-height:20px;color:var(--txt);margin-top:6px}}
"""


# ── montagem ─────────────────────────────────────────────────────────────────────────
def avatar(sigla: str, classe: str = "") -> str:
    """Um avatar: foto para o Igor, círculo com inicial para os outros dois."""
    m = MEMBROS[sigla]
    if m.get("foto"):
        return f'<span class="av foto {classe}" title="{m["nome"]}"></span>'
    return (
        f'<span class="av {classe}" style="background:{m["cor"]}" '
        f'title="{m["nome"]}">{sigla}</span>'
    )


def etiqueta(nome: str, classe: str = "etq") -> str:
    fundo, texto = ETIQUETAS[nome]
    return f'<span class="{classe}" style="background:{fundo};color:{texto}">{nome}</span>'


def monta_cartao(c: dict) -> str:
    """Um cartão da lista, com etiquetas em cima e badges embaixo, como no Trello."""
    etqs = "".join(etiqueta(e) for e in c.get("etiquetas", []))
    etqs = f'<div class="etqs">{etqs}</div>' if etqs else ""

    marca = ""
    if c.get("completo"):
        marca = (
            '<svg class="ic ok" width="16" height="16" viewBox="0 0 16 16" fill="none">'
            '<circle cx="8" cy="8" r="7" fill="#4BCE97"/>'
            '<path d="M4.9 8.2l2 2 4.2-4.4" stroke="#1D2125" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>'
        )

    badges = [f'<span class="bd">{icone("olho", 14)}</span>']
    if c.get("data"):
        texto, estado = c["data"]
        badges.append(
            f'<span class="bd data {estado}">{icone("relogio", 14)}{texto}</span>'
        )
    if c.get("descricao"):
        badges.append(f'<span class="bd">{icone("descricao", 14)}</span>')
    if c.get("comentarios"):
        badges.append(
            f'<span class="bd">{icone("comentario", 14)}{c["comentarios"]}</span>'
        )
    if c.get("checklist"):
        badges.append(
            f'<span class="bd">{icone("checklist", 14)}{c["checklist"]}</span>'
        )
    membros = "".join(avatar(s, "p24") for s in c.get("membros", []))
    badges.append(f'<span class="mem">{membros}</span>')

    return (
        f'<article class="cartao">{etqs}'
        f'<div class="tit">{marca}<span>{c["titulo"]}</span></div>'
        f'<div class="badges">{"".join(badges)}</div></article>'
    )


def monta_lista(l: dict) -> str:
    cartoes = "".join(monta_cartao(c) for c in l["cartoes"])
    return (
        f'<section class="lista"><div class="cab"><h2>{l["nome"]}</h2>'
        f'<span class="qt">{l["total"]}</span>'
        f'<span class="men">{icone("reticencias", 16)}</span></div>'
        f'<div class="cartoes">{cartoes}</div>'
        f'<div class="rodape">{icone("mais", 16)}Adicionar um cartão'
        f'<span class="esp">{icone("cartao", 16)}</span></div></section>'
    )


def monta_topo() -> str:
    """Barra do topo do quadro: título, alternador de visão e o bloco da direita."""
    avs = "".join(avatar(s) for s in ("IV", "BC", "HA"))
    ics = "".join(
        f'<span class="bt-ic">{icone(n, 18)}</span>'
        for n in ("calendario", "raio", "filtro", "estrela", "globo")
    )
    return (
        f'<header class="topo"><span class="nome">Cronos · Challenge FIAP 2026</span>'
        f'<span class="vis">{icone("quadro", 17)}<span class="cv">▾</span></span>'
        f'<div class="dir"><div class="avs">{avs}</div>{ics}'
        f'<span class="bt-share">{icone("pessoa_mais", 16)}Compartilhar</span>'
        f'<span class="bt-ic">{icone("reticencias", 18)}</span></div></header>'
    )


def monta_nav() -> str:
    itens = [
        ("caixa", "Caixa de entrada", False),
        ("calendario", "Planejador", False),
        ("quadro", "Quadro", True),
        ("trocar", "Mudar de quadros", False),
    ]
    return '<nav class="nav">' + "".join(
        f'<a class="{"on" if on else ""}">{icone(ic, 17)}{txt}</a>' for ic, txt, on in itens
    ) + "</nav>"


def pagina(titulo: str, corpo: str, foto: str, altura: int) -> str:
    return (
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
        f"<title>{titulo}</title><style>{css(foto, altura)}</style></head>"
        f"<body>{corpo}</body></html>"
    )


def monta_quadro(foto: str) -> str:
    listas = "".join(monta_lista(l) for l in LISTAS)
    corpo = (
        f'{monta_topo()}<div class="quadro">{listas}'
        f'<div class="add-lista">{icone("mais", 16)}Adicionar outra lista</div></div>'
        f"{monta_nav()}"
    )
    return pagina("Cronos · Challenge FIAP 2026 | Trello", corpo, foto, ALTURA_QUADRO)


def monta_card_aberto(card: dict, foto: str) -> str:
    """O cartão aberto por cima do quadro, que é como o Trello mostra o detalhe."""
    membros = "".join(avatar(s, "p32") for s in card["membros"])
    etqs = "".join(etiqueta(e, "etq") for e in card["etiquetas"])
    data_txt, data_estado = card["data"]
    visto = (
        '<svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="#1D2125" '
        'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3.4 8.4l3 3 6.2-6.6"/></svg>'
    )
    marca = "on" if data_estado == "ok" else ""
    selo = (
        '<span class="sel ok">Concluída</span>' if data_estado == "ok" else ""
    )

    meta = (
        '<div class="meta">'
        f'<div class="bl"><div class="rot">Membros</div><div class="lin">{membros}'
        f'<span class="box">{icone("mais", 16)}</span></div></div>'
        f'<div class="bl"><div class="rot">Etiquetas</div><div class="lin etqs">{etqs}'
        f'<span class="box">{icone("mais", 16)}</span></div></div>'
        f'<div class="bl"><div class="rot">Notificações</div>'
        f'<span class="seguir">{icone("olho", 16)}Seguir</span></div>'
        f'<div class="bl"><div class="rot">Data de entrega</div>'
        f'<span class="dt"><span class="marca {marca}">'
        f'{visto if marca else ""}</span>{data_txt}'
        f'{selo}</span></div></div>'
    )

    paras = "".join(f"<p>{p}</p>" for p in card["descricao"])
    desc = (
        f'<section class="sec"><div class="cab">{icone("descricao", 18)}'
        f'<h3>Descrição</h3><div class="acoes"><span>Editar</span></div></div>'
        f'<div class="desc">{paras}</div></section>'
    )

    itens = card["checklist"]["itens"]
    feitos = sum(1 for _, ok in itens)
    marcados = sum(1 for _, ok in itens if ok)
    pct = round(marcados / feitos * 100)
    linhas = "".join(
        f'<div class="it{" feito" if ok else ""}">'
        f'<span class="cx{" on" if ok else ""}">'
        + (
            '<svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="#1D2125" '
            'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M3.4 8.4l3 3 6.2-6.6"/></svg>'
            if ok
            else ""
        )
        + f"</span><span>{txt}</span></div>"
        for txt, ok in itens
    )
    chk = (
        f'<section class="sec"><div class="cab">{icone("checklist", 18)}'
        f'<h3>{card["checklist"]["nome"]}</h3><div class="acoes">'
        f"<span>Ocultar itens marcados</span><span>Excluir</span></div></div>"
        f'<div class="chk"><div class="prog"><span class="pc">{pct}%</span>'
        f'<span class="tr"><i style="width:{pct}%"></i></span></div>{linhas}</div></section>'
    )

    com = card["comentario"]
    ativ = (
        f'<section class="sec"><div class="cab">{icone("comentario", 18)}'
        f"<h3>Comentários e atividade</h3><div class=\"acoes\">"
        f"<span>Mostrar detalhes</span></div></div>"
        f'<div class="ativ">{avatar(com["autor"], "p32")}<div class="cx">'
        f'<span class="quem">{MEMBROS[com["autor"]]["nome"]}'
        f'<span class="quando">{com["quando"]}</span></span>'
        f'<p>{com["texto"]}</p></div></div></section>'
    )

    lado_add = "".join(
        f'<span class="bt">{icone(ic, 16)}{txt}</span>'
        for ic, txt in (
            ("membros", "Membros"),
            ("etiqueta", "Etiquetas"),
            ("checklist", "Checklist"),
            ("calendario", "Datas"),
            ("anexo", "Anexo"),
            ("local", "Local"),
        )
    )
    lado_acoes = "".join(
        f'<span class="bt">{icone(ic, 16)}{txt}</span>'
        for ic, txt in (
            ("seta", "Mover"),
            ("copiar", "Copiar"),
            ("modelo", "Criar modelo"),
            ("arquivar", "Arquivar"),
            ("compartilhar", "Compartilhar"),
        )
    )
    lado = (
        f'<aside class="cb-lado"><div class="rot">Adicionar ao cartão</div>{lado_add}'
        f'<div class="rot">Ações</div>{lado_acoes}</aside>'
    )

    corpo = (
        f'{monta_topo()}<div class="quadro">'
        + "".join(monta_lista(l) for l in LISTAS[:5])
        + f'</div><div class="veu"></div><div class="cb">'
        f'<div class="cb-topo">{icone("cartao", 20)}<div><h1>{card["titulo"]}</h1>'
        f'<div class="onde">na lista <u>{card["lista"]}</u></div></div>'
        f'<span class="fechar">{icone("reticencias", 18)}{icone("x", 18)}</span></div>'
        f'<div class="cb-corpo"><div class="cb-main">{meta}{desc}{chk}{ativ}</div>'
        f"{lado}</div></div>"
    )
    return pagina(f'{card["titulo"]} | Trello', corpo, foto, ALTURA_CARD)


def renderiza_png() -> None:
    """Converte os três HTML em PNG 2x, no mesmo enquadramento dos prints da aplicação."""
    from playwright.sync_api import sync_playwright

    destino = SAIDA / "png"
    destino.mkdir(parents=True, exist_ok=True)
    arquivos = [
        ("quadro.html", ALTURA_QUADRO),
        (CARD_PPT["arquivo"], ALTURA_CARD),
        (CARD_MODELO["arquivo"], ALTURA_CARD),
    ]

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(channel="chrome")
        for nome, altura in arquivos:
            contexto = navegador.new_context(
                viewport={"width": LARGURA, "height": altura}, device_scale_factor=2
            )
            page = contexto.new_page()
            page.goto((SAIDA / nome).as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(500)
            page.screenshot(path=destino / nome.replace(".html", ".png"))
            contexto.close()
            print(f"  png/{nome.replace('.html', '.png')}")
        navegador.close()


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    foto = _foto_igor()

    (SAIDA / "quadro.html").write_text(monta_quadro(foto), encoding="utf-8")
    print("  quadro.html")
    for card in (CARD_PPT, CARD_MODELO):
        (SAIDA / card["arquivo"]).write_text(
            monta_card_aberto(card, foto), encoding="utf-8"
        )
        print(f'  {card["arquivo"]}')

    if "--png" in sys.argv:
        renderiza_png()


def _foto_igor() -> str:
    """Devolve a foto do Igor como data URI de 72px — o HTML precisa ser autocontido."""
    from PIL import Image

    img = Image.open(FOTO_IGOR).convert("RGBA").resize((72, 72), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


if __name__ == "__main__":
    main()
