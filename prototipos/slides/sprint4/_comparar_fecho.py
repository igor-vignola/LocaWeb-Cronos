# -*- coding: utf-8 -*-
"""Os dois slides que faltam: a descrição resumida e a conclusão.

O template pede os dois por escrito, e os dois saíram do deck no caminho. Aqui
eles voltam com a regra que o Igor deu: pouco texto, imersivo, bonito.

  descricao-A · Uma frase, três provas
      Uma frase grande diz o que o Cronos é. Embaixo, três números. Nada mais.
      Entra como último slide do bloco 1, depois do slide do nome.

  descricao-B · As três respostas
      As três perguntas que o sistema responde, cada uma com o modelo que a
      responde. Quase sem prosa: quem lê entende o produto pela pergunta.

  conclusao · O que fica
      Escura, que é o único slide escuro do fecho e marca o fim depois de
      setenta telas claras. Três números grandes, uma linha cada, e os limites
      numa frase só.

Números conferidos em prototipos/slides/ao-vivo/CONTRATO.md, seções 5 e 7.

Uso:
    .venv/Scripts/python.exe prototipos/slides/sprint4/_comparar_fecho.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
import monta_deck_sprint4 as mk  # noqa: E402

PNG = AQUI / "_png" / "_comparar"

LOGO_CLARO = ('<svg viewBox="0 0 28 28" fill="none"><path d="M6 22L12 14L16 17L22 8" stroke="#fff" '
              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="8" '
              'r="3" stroke="#3B82F6" stroke-width="1.5"/><circle cx="22" cy="8" r="1.2" fill="#3B82F6"/></svg>')
LOGO_ESCURO = (LOGO_CLARO.replace('stroke="#fff"', 'stroke="#0A0E17"').replace("#3B82F6", "#2563EB"))


def moldura(classe: str, tag: str, corpo: str, rodape: str, escuro: bool = False) -> str:
    logo = LOGO_ESCURO if escuro else LOGO_CLARO
    tema = "dark" if escuro else "light"
    return (f'<section class="slide {tema} {classe}" data-slide="0" data-var="a">'
            '<div class="mesh"></div><div class="grid-bg"></div>'
            f'<div class="hd"><div class="bi">{logo}</div><div class="bn">Cronos</div>'
            f'<div class="tag">{tag}</div></div>'
            f'<div class="body">{corpo}</div>'
            f'<div class="ft"><span>{rodape}</span></div></section>')


# ═════════════════════════════════════════════════════════════════════════════
# descrição · A — uma frase, três provas
# ═════════════════════════════════════════════════════════════════════════════
CSS_DA = """
/* a descrição resumida como citação: a aspa é o único ornamento, e a frase
   ocupa o slide sozinha. Sem números, a pedido do Igor em 21/09. */
.dsA .body{padding-top:14px;justify-content:center;align-items:center;text-align:center}
.dsA .cit{position:relative;width:1180px;max-width:100%;padding-top:34px}
.dsA .cit::before{content:"“";position:absolute;left:50%;top:-56px;transform:translateX(-50%);
  font-size:210px;font-weight:900;line-height:1;color:var(--accent);opacity:.16;
  font-family:var(--font)}
.dsA .cit p{font-size:60px;font-weight:800;letter-spacing:-2.3px;line-height:1.18;
  color:var(--head);position:relative}
.dsA .cit p b{color:var(--accent);font-weight:800}
.dsA .assina{display:inline-flex;align-items:center;gap:13px;margin-top:52px;font-size:14px;
  font-weight:700;letter-spacing:1.9px;text-transform:uppercase;color:var(--tx2)}
.dsA .assina i{display:block;width:44px;height:2px;border-radius:2px;background:var(--accent);
  opacity:.6}
"""

DESCRICAO_A = moldura("dsA", "Solução final &middot; descrição resumida", """
    <span class="eb"><span class="rv" style="--d:240ms">1 &middot; A solução</span></span>
    <div class="cit rv" style="--d:460ms">
      <p>O Cronos lê o histórico de incidentes da Locaweb e diz, <b>antes de o prazo estourar</b>, onde a operação precisa agir.</p>
    </div>
    <span class="assina rv" style="--d:1000ms"><i></i>Cronos &middot; veja antes, aja antes</span>""",
    "Challenge FIAP 2026 com Locaweb &middot; Super Data Bros, turma 2TSCOA")


# ═════════════════════════════════════════════════════════════════════════════
# descrição · B — as três respostas
# ═════════════════════════════════════════════════════════════════════════════
CSS_DB = """
.dsB .body{padding-top:14px;justify-content:center}
.dsB .tt{font-size:50px;letter-spacing:-1.9px}
.dsB .tres{display:flex;gap:0;margin-top:56px}
.dsB .rp{flex:1;padding:0 40px;border-right:1px solid #DCE4EF}
.dsB .rp:first-child{padding-left:0} .dsB .rp:last-child{border-right:none;padding-right:0}
.dsB .rp .ip{width:52px;height:52px;border-radius:15px;background:var(--accent-l);
  border:1px solid #BFDBFE;display:flex;align-items:center;justify-content:center}
.dsB .rp .ip svg{width:25px;height:25px;color:var(--accent);stroke:currentColor;fill:none;
  stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.dsB .rp .q{font-size:25px;font-weight:800;letter-spacing:-.7px;line-height:1.25;color:var(--head);
  margin-top:26px}
.dsB .rp .m{display:inline-block;font-family:var(--mono);font-size:13px;color:var(--accent);
  background:var(--accent-l);border:1px solid #BFDBFE;border-radius:9px;padding:7px 13px;
  margin-top:20px}
.dsB .base{display:flex;align-items:center;gap:14px;margin-top:58px;padding-top:22px;
  border-top:1px solid #DCE4EF;font-size:16.5px;line-height:1.45;color:var(--tx)}
.dsB .base b{color:var(--head);font-weight:700}
.dsB .base .ic{width:20px;height:20px;color:var(--accent);flex-shrink:0}
"""
DESCRICAO_B = moldura("dsB", "Solução final &middot; descrição resumida", """
    <span class="eb"><span class="rv" style="--d:240ms">1 &middot; A solução</span></span>
    <h1 class="tt"><span class="mask" style="--d:360ms"><span>Três respostas que hoje só existem em dezembro</span></span></h1>
    <div class="tres">
      <div class="rp rv3" style="--d:700ms">
        <span class="ip"><svg viewBox="0 0 24 24"><path d="M3 16.5c3.2 0 4.6-9 8.2-9 3.7 0 4.3 9 8.2 9"/><circle cx="19.4" cy="16.5" r="2.1"/></svg></span>
        <p class="q">Quantos incidentes chegam nos próximos sete dias?</p>
        <span class="m">Prophet</span>
      </div>
      <div class="rp rv3" style="--d:820ms">
        <span class="ip"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.4"/><circle cx="12" cy="12" r="3.4"/><path d="M12 1.8v2.6M12 19.6v2.6M1.8 12h2.6M19.6 12h2.6"/></svg></span>
        <p class="q">Qual incidente aberto vai estourar o prazo?</p>
        <span class="m">Regressão logística</span>
      </div>
      <div class="rp rv3" style="--d:940ms">
        <span class="ip"><svg viewBox="0 0 24 24"><path d="M3 20.4h5v-5h5v-5h5v-5h3"/></svg></span>
        <p class="q">Onde a meta do ano vai fechar, em P2 e P3?</p>
        <span class="m">Projeção da meta</span>
      </div>
    </div>
    <div class="base rv" style="--d:1200ms">
      <svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5.6" rx="7.4" ry="2.8"/><path d="M4.6 5.6v12.2c0 1.5 3.3 2.8 7.4 2.8s7.4-1.3 7.4-2.8V5.6"/><path d="M4.6 11.7c0 1.5 3.3 2.8 7.4 2.8s7.4-1.3 7.4-2.8"/></svg>
      <span>Sobre <b>122.543 incidentes</b> de três anos, dos quais <b>25.600</b> contam para o indicador. Entregue em uma aplicação Django, num contêiner.</span>
    </div>""",
    "Base elegível pelo campo oficial Entrou para KPI?")


# ═════════════════════════════════════════════════════════════════════════════
# conclusão · O que fica
# ═════════════════════════════════════════════════════════════════════════════
CSS_CC = """
/* O fecho conversa com a descrição resumida: também é uma frase, e o número
   mora dentro dela em vez de virar cartão. Escura, que é o único slide escuro
   deste trecho e marca o fim depois de setenta telas claras. */
.ccF .body{padding-top:14px;justify-content:center}
.ccF .frase{font-size:62px;font-weight:800;letter-spacing:-2.4px;line-height:1.24;color:#E8ECF3;
  max-width:26ch;margin-top:22px}
.ccF .frase .n{font-size:118px;font-weight:900;letter-spacing:-4.6px;color:#60A5FA;
  font-variant-numeric:tabular-nums;line-height:.9}
.ccF .frase b{color:#fff;font-weight:800}
.ccF .frase .z{color:#8E99A8;font-weight:800}
.ccF .apoio2{display:flex;gap:0;margin-top:54px;padding-top:24px;
  border-top:1px solid rgba(255,255,255,.14)}
.ccF .ap{flex:1;padding-right:42px;border-right:1px solid rgba(255,255,255,.14)}
.ccF .ap:last-child{border-right:none;padding-right:0}
.ccF .ap:not(:first-child){padding-left:42px}
.ccF .ap .v{font-size:31px;font-weight:900;letter-spacing:-1.2px;color:#fff;line-height:1;
  font-variant-numeric:tabular-nums}
.ccF .ap p{font-size:15px;line-height:1.5;color:#A6B0BD;margin-top:11px}
.ccF .ap p b{color:#E8ECF3;font-weight:700}
"""

CONCLUSAO = moldura("ccF", "7 &middot; Conclusão", """
    <span class="eb"><span class="rv" style="--d:240ms">7 &middot; Conclusão</span></span>
    <p class="frase rv" style="--d:420ms">Nos 50 primeiros casos da fila, o Cronos encontra <span class="n">13</span> violações.<br>A ordem de hoje encontra <span class="z">nenhuma</span>.</p>
    <div class="apoio2">
      <div class="ap rv" style="--d:1000ms"><div class="v">3 meses</div>
        <p>de antecedência na leitura da meta do ano, <b>certa nas duas prioridades</b></p></div>
      <div class="ap rv" style="--d:1100ms"><div class="v">6 abas</div>
        <p>no ar em um contêiner, <b>sem provedor de nuvem amarrado</b></p></div>
      <div class="ap rv" style="--d:1200ms"><div class="v">59 a 61%</div>
        <p>de cobertura da faixa no P3, contra 86% a 88% no P2: <b>o limite que fica</b></p></div>
    </div>""",
    "Base de avaliação: 5.183 incidentes e 50 violações, fora do período de treino", escuro=True)


PECAS = [
    ("descricao-A", "Descrição resumida · versão A", "A frase, como citação",
     "A definição do produto ocupa o slide sozinha, em forma de citação. Sem números.",
     DESCRICAO_A, CSS_DA),
    ("descricao-B", "Descrição resumida · versão B", "As três respostas",
     "As três perguntas que o sistema responde, cada uma com o modelo que a responde. "
     "Quem lê entende o produto pela pergunta, sem prosa.", DESCRICAO_B, CSS_DB),
    ("conclusao", "Conclusão", "O número dentro da frase",
     "Mesma linguagem da descrição: uma frase, com o número morando dentro dela. Três apoios "
     "no pé, sendo o último o limite que continua de pé.", CONCLUSAO, CSS_CC),
]

CSS_PAGINA = """
body{background:#2A2F38;overflow:auto;padding:34px 0 60px}
.palco{width:1600px;height:900px;position:relative;overflow:hidden;margin:0 auto 34px;
  box-shadow:0 30px 90px -40px rgba(0,0,0,.7);background:#fff}
.sec{width:1600px;margin:0 auto 22px;color:#fff;font-family:var(--font);font-size:30px;
  font-weight:800;letter-spacing:-.8px}
.sec small{display:block;font-size:16px;font-weight:400;color:rgba(255,255,255,.62);margin-top:7px;
  letter-spacing:0;line-height:1.45;max-width:1100px}
"""


def main() -> int:
    estilo = (mk.AO_VIVO / "_estilo.css").read_text(encoding="utf-8")
    congela = mk.CSS_BUILDER.replace("#palco{", ".palco-x{")
    PNG.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=mk.CHROME)
        pg = nav.new_page(viewport={"width": 1700, "height": 1000})
        for chave, titulo, nome, desc, secao, css in PECAS:
            s = secao.replace('class="slide', 'class="is-active slide', 1)
            html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
                    f"<title>{titulo} &middot; {nome}</title>{mk.FONTES}"
                    f"<style>{estilo}\n{css}\n{congela}\n{CSS_PAGINA}</style></head><body>"
                    f'<div class="sec">{titulo} &middot; {nome}<small>{desc}</small></div>'
                    f'<div class="palco">{s}</div></body></html>')
            destino = AQUI / f"_fecho-{chave}.html"
            destino.write_text(html, encoding="utf-8")
            pg.goto(destino.as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(700)
            pg.query_selector(".palco").screenshot(path=str(PNG / f"fecho-{chave}.png"))
            print(f"{destino.name}")
        nav.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
